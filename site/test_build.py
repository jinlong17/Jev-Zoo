"""Offline tests for catalog identity and publication evidence; no model imports."""

import contextlib
import hashlib
import importlib.util
import io
import json
import pathlib
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("jevzoo_site", ROOT / "site/build.py")
site = importlib.util.module_from_spec(spec)
spec.loader.exec_module(site)


class CatalogContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = site.compile_catalog(ROOT)

    def test_assets_are_deduplicated_without_losing_provenance(self):
        site.validate(self.data)
        ids = {r["id"] for r in self.data["resources"]}
        for r in self.data["resources"]:
            self.assertTrue(r["source_record_ids"])
            self.assertTrue(set(r["related_ids"]).issubset(ids))
        self.assertEqual(48, self.data["stats"]["by_type"]["paper"])
        self.assertEqual(981, self.data["stats"]["discovered"])

    def test_reachable_upstream_does_not_grant_runtime_support(self):
        rows = [r for r in self.data["resources"] if r["evidence_level"] == "link_checked"]
        self.assertTrue(rows)
        self.assertTrue(
            all(
                not r["runtime"]["source_verified"] and not r["runtime"]["adapter_implemented"]
                for r in rows
            )
        )
        self.assertEqual(0, self.data["stats"]["formal_training_recipes"])
        for r in self.data["resources"]:
            if r["runtime"]["fully_evaluated"]:
                self.assertTrue(r["runtime"]["evaluated_scopes"])

    def test_paper_model_and_recipe_relations_exist_in_both_locales(self):
        r = next(r for r in self.data["resources"] if "llm2jev-paper" in r["source_record_ids"])
        self.assertEqual("paper", r["resource_type"])
        self.assertTrue(r["related_ids"])
        for locale in ["en", "zh"]:
            page = site.detail(self.data, r, locale)
            self.assertIn("../../resources/", page)
            self.assertIn("https://arxiv.org/abs/2610.02076", page)
        self.assertNotEqual(site.home(self.data, "en"), site.home(self.data, "zh"))

    def test_invalid_relationship_and_unscoped_green_status_are_rejected(self):
        data = json.loads(json.dumps(self.data))
        data["resources"][0]["related_ids"].append("invented-resource")
        with self.assertRaisesRegex(ValueError, "Unresolved"):
            site.validate(data)
        data = json.loads(json.dumps(self.data))
        data["resources"][0]["runtime"]["fully_evaluated"] = True
        data["resources"][0]["runtime"]["evaluated_scopes"] = []
        with self.assertRaisesRegex(ValueError, "Unscoped"):
            site.validate(data)

    def test_only_exact_approved_bytes_enter_public_results(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = pathlib.Path(temp)
            summary = repo / "results/published/test.json"
            summary.parent.mkdir(parents=True)
            summary.write_text(
                json.dumps(
                    {
                        "model_id": "test",
                        "benchmark_id": "test",
                        "profile": "full",
                        "metrics": {},
                        "checkpoint_revision": "rev",
                    }
                )
            )
            manifest = repo / "approval.json"
            manifest.write_text(
                json.dumps(
                    {
                        "release_id": "approved-release",
                        "content_hash": "hash",
                        "files": {
                            "results/published/test.json": hashlib.sha256(
                                summary.read_bytes()
                            ).hexdigest()
                        },
                    }
                )
            )
            approved, _ = site.approved_results(repo, None, manifest)
            self.assertEqual(1, len(approved))
            summary.write_text(summary.read_text() + " ")
            approved, _ = site.approved_results(repo, None, manifest)
            self.assertEqual([], approved)

    def test_download_manifest_alone_cannot_grant_implemented_status(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = pathlib.Path(temp)
            for relative in [
                "catalog/catalog.json",
                "catalog/status.json",
                "manifests/models.lock.json",
                "manifests/datasets.lock.json",
            ]:
                target = repo / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((ROOT / relative).read_bytes())
            data = site.compile_catalog(repo)
            self.assertEqual(0, data["stats"]["adapter_checkpoints"])
            self.assertTrue(
                all(
                    not r["runtime"]["adapter_implemented"]
                    for r in data["resources"]
                    if r["runtime"].get("deployment_id")
                )
            )
        self.assertEqual("N/A", site.format_accuracy(None))
        self.assertEqual("0.00%", site.format_accuracy(0))

    def test_registry_update_reaches_both_pages_json_and_readmes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            repo = root / "source"
            for folder in ["site", "catalog", "manifests"]:
                (repo / folder).mkdir(parents=True, exist_ok=True)
            for name in ["styles.css", "app.js", "favicon.svg"]:
                (repo / "site" / name).write_bytes((ROOT / "site" / name).read_bytes())
            registry = json.loads((ROOT / "catalog/catalog.json").read_text())
            registry["discovery_resources"] = registry["discovery_resources"][:1]
            for key in ["curated_resources", "papers", "benchmarks", "recipes"]:
                registry[key] = []
            for name in ["models", "datasets"]:
                (repo / "manifests" / (name + ".lock.json")).write_text('{"entries":[]}')
            registry["discovery_resources"][0]["presentation"].update(
                resource_type="model",
                description={"en": "Updated actionable description.", "zh": "更新后的可执行介绍。"},
            )
            (repo / "catalog/catalog.json").write_text(json.dumps(registry))
            with contextlib.redirect_stdout(io.StringIO()):
                data = site.build(repo, root / "output", write_readmes=True)
            slug = data["resources"][0]["slug"]
            self.assertIn(
                "Updated actionable description.",
                (root / "output/en/resources" / slug / "index.html").read_text(),
            )
            self.assertIn(
                "更新后的可执行介绍。",
                (root / "output/zh/resources" / slug / "index.html").read_text(),
            )
            self.assertIn("| Models | 1 |", (repo / "README.md").read_text())
            self.assertIn("| 模型 | 1 |", (repo / "README_zh.md").read_text())
            projection = json.loads((root / "output/assets/catalog.json").read_text())
            self.assertEqual("model", projection["resources"][0]["resource_type"])


if __name__ == "__main__":
    unittest.main()
