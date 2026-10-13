import io
import json
from pathlib import Path

from jev_zoo import catalog


def test_refresh_keeps_editorial_assets_primary_evidence_and_removed_records(tmp_path, monkeypatch):
    root = Path(__file__).resolve().parents[1]
    prior = json.loads((root / "catalog/catalog.json").read_text())
    reviewed = next(
        entry for entry in prior["discovery_resources"] if entry.get("site_primary_review")
    )
    (tmp_path / "catalog").mkdir()
    (tmp_path / "catalog/catalog.json").write_text(json.dumps(prior))
    seed = tmp_path / "old-seed.json"
    seed.write_text('{"entries":[],"papers":[],"benchmarks":[],"sources":{}}')
    markdown = (
        "### Browser & computer use (1)\n"
        f"| [{reviewed['name']}]({reviewed['url']}) | 1 | Python | 2026-10-13 | Changed upstream wording |\n"
    )
    monkeypatch.setattr(
        catalog,
        "get_json",
        lambda _: {
            "sha": "synthetic-commit",
            "commit": {"committer": {"date": "2026-10-13T00:00:00Z"}},
        },
    )
    monkeypatch.setattr(
        catalog.urllib.request, "urlopen", lambda *args, **kwargs: io.BytesIO(markdown.encode())
    )
    refreshed = catalog.refresh(tmp_path, seed)
    entry = next(r for r in refreshed["discovery_resources"] if r["id"] == reviewed["id"])
    assert entry["site_primary_review"] == reviewed["site_primary_review"]
    assert entry["presentation"]["translation_needs_review"] is True
    assert {r["id"] for r in prior["curated_resources"]} <= {
        r["id"] for r in refreshed["curated_resources"]
    }
    assert refreshed["recipes"] == prior["recipes"]
    assert len(refreshed["discovery_resources"]) == len(prior["discovery_resources"])
    assert any(
        r.get("upstream_removed_at_revision") == "synthetic-commit"
        for r in refreshed["discovery_resources"]
    )
