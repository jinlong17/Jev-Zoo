"""Read-only bilingual registry, README and approved-evidence checks."""

from __future__ import annotations

import argparse
import importlib.util
import json
import pathlib
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("jevzoo_site_build", ROOT / "site/build.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


def verify_source(repo: pathlib.Path):
    data = builder.compile_catalog(repo)
    builder.validate(data)
    with tempfile.TemporaryDirectory(prefix="jevzoo-readme-check-") as temporary:
        expected = pathlib.Path(temporary)
        builder.readmes(data, expected)
        for name in ["README.md", "README_zh.md"]:
            if (repo / name).read_bytes() != (expected / name).read_bytes():
                raise ValueError(f"{name} differs from the bilingual registry projection")
    index = builder.read(repo / "catalog/canonical-resources.json")
    if index.get("derived_from_registry_sha256") != data["registry_sha256"]:
        raise ValueError("Canonical index differs from the registry revision")
    evidence = builder.read(repo / "site/approved-results-manifest.json")
    if len(data["approved_results"]) != len(evidence["files"]):
        raise ValueError("A pinned approved result is missing or its bytes changed")
    for relative, expected_hash in evidence["files"].items():
        path = (repo / relative).resolve()
        if not path.is_relative_to(repo.resolve()) or builder.digest(path) != expected_hash:
            raise ValueError("Approved evidence has changed: " + relative)
    return {
        "passed": True,
        "registry_sha256": data["registry_sha256"],
        "canonical_resources": data["stats"]["cataloged"],
        "locales": data["locales"],
        "approved_summaries": len(data["approved_results"]),
        "approved_full_summaries": data["stats"]["approved_full_summaries"],
        "readmes_match_their_locale_projection": True,
        "no_model_or_network_execution": True,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=pathlib.Path, default=ROOT)
    print(json.dumps(verify_source(parser.parse_args().repo), ensure_ascii=False, indent=2))
