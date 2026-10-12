"""Pinned downloads with independent per-file verification and resumable Hub transport."""

from __future__ import annotations

import fnmatch
import hashlib
import json
import os
import shutil
import subprocess
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from .storage import append_jsonl, canonical_hash, safe_child, sha256, workspace, write_json

MODEL_SPECS = [
    ("qwen35-2b", "Qwen/Qwen3.5-2B", "A", "frozen_hf"),
    ("qwen35-4b", "Qwen/Qwen3.5-4B", "A", "frozen_hf"),
    ("onejev-08b", "OmniJev/OneJev-0.8B", "A", "onejev"),
    ("onejev-4b", "OmniJev/OneJev-4B", "A", "onejev"),
    ("imajev-2b", "mohit67890/imajev-2b", "A", "imajev"),
    ("imajev-4b", "mohit67890/imajev-4b", "A", "imajev"),
    ("clef-flash", "Cloudflare/clef-flash", "A", "clef"),
    ("h2o-lightning-4b", "h2oai/h2o-lightning-4b", "A", "h2o"),
    ("clef", "Cloudflare/clef", "B", "clef"),
    ("pplx-decider-27b", "perplexity-ai/pplx-decider-v1-27b", "B", "pplx"),
]
DATASET_SPECS = [
    ("typed-decisions", "LocalLLaMA/typed-decisions", ["all/*.parquet", "README.md", "eval.yaml"]),
    ("jeval", "carlosxiang/JEVal", ["data/*.parquet", "README.md", "citation.bib"]),
    (
        "decisionbench",
        "Hanno-Labs/decision-bench",
        ["data/*.parquet", "README.md", "provenance/*", "artifact/manifest.json"],
    ),
    ("mmstar", "Lin-Chen/MMStar", ["mmstar.parquet", "README.md"]),
    (
        "clinc150",
        "clinc/clinc_oos",
        ["*.parquet", "*.json", "*.jsonl", "*.csv", "*.txt", "README.md", "*.py"],
    ),
    ("sst2", "stanfordnlp/sst2", ["*.parquet", "*.json", "README.md", "*.py"]),
    ("boolq", "google/boolq", ["*.parquet", "*.jsonl", "README.md", "*.py"]),
    ("arc", "allenai/ai2_arc", ["ARC-Challenge/*", "README.md"]),
    (
        "onejev-data",
        "OmniJev/OneJev-Data",
        ["data/*.parquet", "licenses.csv", "README.md", "sample/sample-100.parquet"],
    ),
]
GITHUB_DATASET_SPECS = [
    (
        "jevbench-public",
        "fstandhartinger/jevbench",
        [
            "datasets/public/original.jsonl",
            "datasets/public/easy.jsonl",
            "datasets/public/hard.jsonl",
            "datasets/manifest.json",
            "LICENSE",
            "README.md",
        ],
    ),
    (
        "sys1cal",
        "little-g-ai/Sys1Cal-v1",
        [
            "datasets/generated/v0.1.0_tiny_cleanvars_binary.jsonl",
            "datasets/generated/v0.1.0_tiny_cleanvars_parallel_primitives.jsonl",
            "hf/Sys1Cal-v1/README.md",
            "README.md",
        ],
    ),
    (
        "banking77",
        "PolyAI-LDN/task-specific-datasets",
        [
            "banking_data/categories.json",
            "banking_data/train.csv",
            "banking_data/test.csv",
            "README.md",
        ],
    ),
]


def get_json(url: str) -> dict:
    headers = {"User-Agent": "JevZoo/0.1"}
    if url.startswith("https://api.github.com/") and os.getenv("GITHUB_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def freeze(repo: Path) -> tuple[Path, Path]:
    models, datasets = [], []
    for identifier, hub_id, batch, backend in MODEL_SPECS:
        info = get_json(f"https://huggingface.co/api/models/{hub_id}?blobs=true")
        files = []
        for item in info["siblings"]:
            name = item["rfilename"]
            if "/" in name and not (
                name.startswith("processor/")
                or (backend == "pplx" and name.startswith("source/src/autojev/"))
            ):
                continue
            if not (
                name.endswith((".safetensors", ".json", ".py", ".jinja", ".txt", ".model"))
                or name in {"README.md", "LICENSE"}
            ):
                continue
            if name.endswith(".bin"):
                continue
            files.append(_hub_file(item))
        card = info.get("cardData") or {}
        models.append(
            dict(
                id=identifier,
                repo_id=hub_id,
                revision=info["sha"],
                repo_type="model",
                source="huggingface",
                batch=batch,
                backend=backend,
                license=card.get("license"),
                base_model=card.get("base_model"),
                files=files,
                total_bytes=sum(f["size"] for f in files),
            )
        )
        print(f"Frozen model {identifier}: {len(files)} files", flush=True)
    for identifier, hub_id, patterns in DATASET_SPECS:
        info = get_json(f"https://huggingface.co/api/datasets/{hub_id}?blobs=true")
        files = [
            _hub_file(item)
            for item in info["siblings"]
            if any(fnmatch.fnmatch(item["rfilename"], pattern) for pattern in patterns)
        ]
        datasets.append(
            dict(
                id=identifier,
                repo_id=hub_id,
                revision=info["sha"],
                repo_type="dataset",
                source="huggingface",
                files=files,
                license=(info.get("cardData") or {}).get("license"),
                total_bytes=sum(f["size"] for f in files),
            )
        )
    for identifier, github_id, filenames in GITHUB_DATASET_SPECS:
        branch = get_json(f"https://api.github.com/repos/{github_id}")["default_branch"]
        info = get_json(f"https://api.github.com/repos/{github_id}/commits/{branch}")
        revision = info["sha"]
        files = []
        for filename in filenames:
            url = f"https://raw.githubusercontent.com/{github_id}/{revision}/{filename}"
            with urllib.request.urlopen(url, timeout=60) as response:
                data = response.read()
            files.append(
                dict(path=filename, size=len(data), sha256=hashlib.sha256(data).hexdigest())
            )
        datasets.append(
            dict(
                id=identifier,
                repo_id=github_id,
                revision=revision,
                source="github",
                repo_type="dataset",
                files=files,
                total_bytes=sum(f["size"] for f in files),
            )
        )
    root = repo / "manifests"
    model_path, data_path = root / "models.lock.json", root / "datasets.lock.json"
    for path, entries, kind in [(model_path, models, "models"), (data_path, datasets, "datasets")]:
        write_json(
            path,
            dict(
                schema_version="1.0",
                as_of="2026-10-12",
                kind=kind,
                entries=entries,
                manifest_hash=canonical_hash(entries),
            ),
        )
    return model_path, data_path


def _hub_file(item: dict) -> dict:
    lfs = item.get("lfs") or {}
    return dict(
        path=item["rfilename"],
        size=item.get("size") or lfs.get("size", 0),
        sha256=lfs.get("oid") or lfs.get("sha256"),
        git_oid=item.get("blobId"),
    )


def verify_file(path: Path, spec: dict) -> str:
    if not path.is_file() or path.is_symlink():
        raise ValueError("Missing file or unexpected symlink")
    if spec.get("size") and path.stat().st_size != spec["size"]:
        raise ValueError("File size mismatch")
    digest = sha256(path)
    if spec.get("sha256") and digest != spec["sha256"]:
        raise ValueError("SHA-256 mismatch")
    if not spec.get("sha256") and spec.get("git_oid"):
        data = path.read_bytes()
        git_oid = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        if git_oid != spec["git_oid"]:
            raise ValueError("Git blob checksum mismatch")
    return digest


def fetch_manifest(manifest_path: Path, *, only: list[str] | None = None, workers: int = 4) -> dict:
    root = workspace()
    manifest = json.loads(manifest_path.read_text())
    if manifest.get("manifest_hash") != canonical_hash(manifest["entries"]):
        raise ValueError("Lock manifest was changed without recomputing its hash")
    entries = [e for e in manifest["entries"] if not only or e["id"] in only]
    required = sum(entry["total_bytes"] for entry in entries)
    if shutil.disk_usage(root).free < required:
        raise ValueError("Insufficient free space for the locked download manifest")
    event_path = root / "downloads/events.jsonl"
    summary = {}
    for entry in entries:
        destination = safe_child(root, f"{manifest['kind']}/{entry['id']}")
        destination.mkdir(parents=True, exist_ok=True)
        state_path = root / "downloads" / f"{entry['id']}.json"
        previous = json.loads(state_path.read_text()) if state_path.exists() else {}
        verified = (
            previous.get("files", {}) if previous.get("revision") == entry["revision"] else {}
        )
        state = dict(
            id=entry["id"], revision=entry["revision"], status="downloading", files=verified
        )
        write_json(state_path, state)
        failures = []

        def download(spec: dict) -> tuple[str, dict]:
            target = safe_child(destination, spec["path"])
            old = verified.get(spec["path"])
            if old and target.is_file() and target.stat().st_size == old["size"]:
                digest = verify_file(target, spec)
                if digest != old["sha256"]:
                    raise ValueError("Previously downloaded file was changed")
                return spec["path"], old
            if entry["source"] == "huggingface":
                from huggingface_hub import hf_hub_download

                result = hf_hub_download(
                    repo_id=entry["repo_id"],
                    repo_type=entry["repo_type"],
                    revision=entry["revision"],
                    filename=spec["path"],
                    local_dir=destination,
                )
                target = Path(result)
            else:
                url = f"https://raw.githubusercontent.com/{entry['repo_id']}/{entry['revision']}/{spec['path']}"
                target.parent.mkdir(parents=True, exist_ok=True)
                with urllib.request.urlopen(url, timeout=60) as response:
                    data = response.read()
                temporary = target.with_suffix(target.suffix + ".part")
                temporary.write_bytes(data)
                temporary.replace(target)
            digest = verify_file(target, spec)
            return spec["path"], dict(size=target.stat().st_size, sha256=digest)

        with ThreadPoolExecutor(max_workers=workers) as pool:
            jobs = {pool.submit(download, spec): spec for spec in entry["files"]}
            for job in as_completed(jobs):
                spec = jobs[job]
                try:
                    name, information = job.result()
                    state["files"][name] = information
                    append_jsonl(
                        event_path,
                        dict(
                            event="file_verified",
                            id=entry["id"],
                            file=name,
                            revision=entry["revision"],
                            time=time.time(),
                        ),
                    )
                except Exception as error:
                    # Exception class is safe; signed URLs/auth-bearing exception strings are not logged.
                    failures.append(dict(file=spec["path"], error_type=type(error).__name__))
                write_json(state_path, state)
        state["status"] = "failed" if failures else "downloaded"
        state["errors"] = failures
        state["completed_at"] = time.time()
        state["manifest_entry_hash"] = canonical_hash(entry)
        write_json(state_path, state)
        summary[entry["id"]] = state["status"]
        print(
            f"{entry['id']}: {state['status']} ({len(state['files'])}/{len(entry['files'])})",
            flush=True,
        )
    return summary


def fetch_workers(manifest_path: Path) -> dict:
    """Pin upstream source clones independently of model weights; never install globally."""
    root = workspace()
    lock = json.loads(manifest_path.read_text())
    if lock["manifest_hash"] != canonical_hash(lock["workers"]):
        raise ValueError("Worker manifest checksum mismatch")
    statuses = {}
    for name, spec in lock["workers"].items():
        target = safe_child(root, spec["path"])
        if not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(["git", "clone", "--quiet", spec["repository"], str(target)], check=True)
            subprocess.run(
                ["git", "-C", str(target), "checkout", "--quiet", spec["revision"]], check=True
            )
        for relative, digest in spec["files"].items():
            if sha256(safe_child(target, relative)) != digest:
                raise ValueError(f"Unexpected upstream source: {name}/{relative}")
        statuses[name] = "downloaded"
    return statuses
