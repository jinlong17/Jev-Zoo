"""Offline evidence and deployment regression tests, including tamper cases."""

import importlib.util
import json
import pathlib
import shutil
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


def module(name, file):
    spec = importlib.util.spec_from_file_location(name, ROOT / "site" / file)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


checks = module("site_checks", "check.py")
deployment = module("site_deployment", "deployment.py")


class ReleaseChecks(unittest.TestCase):
    def test_readme_fact_drift_fails_source_checks(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = pathlib.Path(temp)
            evidence = json.loads((ROOT / "site/approved-results-manifest.json").read_text())
            paths = [
                "catalog/catalog.json",
                "catalog/canonical-resources.json",
                "catalog/status.json",
                "manifests/models.lock.json",
                "manifests/datasets.lock.json",
                "site/approved-results-manifest.json",
                "README.md",
                "README_zh.md",
            ] + list(evidence["files"])
            for relative in paths:
                target = repo / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / relative, target)
            self.assertTrue(checks.verify_source(repo)["passed"])
            (repo / "README_zh.md").write_text("An invented supported-model count")
            with self.assertRaisesRegex(ValueError, "README_zh"):
                checks.verify_source(repo)

    def test_new_public_marker_does_not_relabel_pinned_evidence(self):
        with tempfile.TemporaryDirectory() as temp:
            public = pathlib.Path(temp)
            (public / "release").mkdir()
            (public / "release/approved-files.json").write_text(
                '{"release_id":"unrelated-new-release"}'
            )
            approved, manifest = checks.builder.approved_results(ROOT, public)
            pinned = json.loads((ROOT / "site/approved-results-manifest.json").read_text())
            self.assertEqual(len(pinned["files"]), len(approved))
            self.assertEqual(pinned["release_id"], manifest["release_id"])

    def test_static_byte_drift_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            output = root / "output"
            (output / "assets").mkdir(parents=True)
            (output / "assets/catalog.json").write_text(
                '{"registry_sha256":"synthetic","locales":["en","zh"]}'
            )
            (output / "index.html").write_text("Original page")
            manifest = root / "manifest.json"
            deployment.freeze(output, manifest)
            deployment.verify(output, manifest)
            (output / "index.html").write_text("Changed after review")
            with self.assertRaisesRegex(ValueError, "drift"):
                deployment.verify(output, manifest)

    def test_archive_is_reproducible_and_excludes_diagnostics(self):
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            output = root / "output"
            (output / "assets").mkdir(parents=True)
            (output / "assets/catalog.json").write_text(
                '{"registry_sha256":"synthetic","locales":["en","zh"]}'
            )
            (output / "index.html").write_text("Original page")
            (output / "build-report.json").write_text("diagnostic timestamp")
            manifest = root / "manifest.json"
            contract = deployment.freeze(output, manifest)
            self.assertNotIn("build-report.json", contract["files"])
            first = deployment.archive(output, manifest, root / "one.zip")
            (output / "build-report.json").write_text("another diagnostic timestamp")
            second = deployment.archive(output, manifest, root / "two.zip")
            self.assertEqual(first["archive_sha256"], second["archive_sha256"])


if __name__ == "__main__":
    unittest.main()
