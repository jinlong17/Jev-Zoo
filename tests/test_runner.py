import json

import pytest

from jev_zoo.adapters import Mock
from jev_zoo.runner import run
from jev_zoo.storage import write_json


def setup_repo(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "src/jev_zoo").mkdir(parents=True)
    write_json(repo / "manifests/models.lock.json", {"entries": []})
    write_json(repo / "manifests/datasets.lock.json", {"entries": []})
    write_json(repo / "manifests/workers.lock.json", {"workers": {}})
    return repo


class Interrupting(Mock):
    calls = 0

    def predict(self, request):
        self.calls += 1
        if self.calls == 2:
            raise KeyboardInterrupt()
        return super().predict(request)


def test_resume_skips_completed_and_rejects_contract_changes(tmp_path, monkeypatch):
    monkeypatch.setenv("JEVZOO_WORKSPACE", str(tmp_path / "workspace"))
    repo = setup_repo(tmp_path)
    adapter = Interrupting({"revision": "synthetic"})
    with pytest.raises(KeyboardInterrupt):
        run(repo, "mock", "synthetic-smoke", max_samples=4, adapter=adapter)
    manifest = next((tmp_path / "workspace/runs").rglob("manifest.json"))
    directory = manifest.parent
    assert len(list((directory / "receipts").glob("*.json"))) == 1
    run(repo, "mock", "synthetic-smoke", max_samples=4, adapter=Mock({}), resume=directory)
    assert len(list((directory / "receipts").glob("*.json"))) == 4
    metrics = json.loads((directory / "metrics.json").read_text())
    assert metrics["errors"] == 0
    assert metrics["attempted"] == metrics["eligible"] == 4
    (repo / "src/jev_zoo/changed.py").write_text("# change")
    with pytest.raises(ValueError, match="changed"):
        run(repo, "mock", "synthetic-smoke", max_samples=4, resume=directory)


def test_mock_and_full_subset_rejected(tmp_path, monkeypatch):
    monkeypatch.setenv("JEVZOO_WORKSPACE", str(tmp_path / "workspace"))
    repo = setup_repo(tmp_path)
    with pytest.raises(ValueError, match="full run"):
        run(repo, "mock", "synthetic-smoke", profile="full", max_samples=2)
