"""Immutable run contracts, per-request atomic receipts and resumable offline evaluation."""

from __future__ import annotations

import datetime
import importlib.metadata
import json
import os
import platform
import shutil
import time
from pathlib import Path

from .adapters import create_adapter
from .metrics import grouped_accuracy_interval, summarize, timing_summary
from .storage import canonical_hash, read_jsonl, safe_child, sha256, workspace, write_json
from .tasks import load_suite


def code_hash(repo):
    return canonical_hash(
        {
            str(p.relative_to(repo)): sha256(p)
            for p in sorted((repo / "src/jev_zoo").glob("*.py"))
            if p.name not in {"training.py", "catalog.py", "release.py"}
        }
    )


def run(
    repo: Path,
    model_id: str,
    suite: str,
    *,
    profile="smoke",
    resume=None,
    max_samples=None,
    max_tokens=32768,
    adapter=None,
    root=None,
    calibration_data=None,
    rotations=1,
    calibration=None,
):
    root = workspace(root)
    if calibration_data is not None:
        from .domain import SupervisedExample

        calibration_data = Path(calibration_data).resolve()
        if suite != "calibration" or not calibration_data.is_relative_to(root / "checkpoints"):
            raise ValueError("Calibration input must be a saved independent training fold")
        examples = [SupervisedExample.model_validate(row) for row in read_jsonl(calibration_data)]
        if not examples or any(e.split != "calibration" for e in examples):
            raise ValueError("Every calibration example must have calibration provenance")
        training_contract = json.loads(
            (calibration_data.parent / "training-contract.json").read_text()
        )
        if (
            canonical_hash([e.model_dump() for e in examples])
            != training_contract["calibration_hash"]
        ):
            raise ValueError("Calibration fold changed after training partition")
    else:
        examples = load_suite(suite, root)
    if profile == "full" and max_samples is not None:
        raise ValueError("A full run cannot reduce its official split")
    if model_id == "mock" and suite != "synthetic-smoke":
        raise ValueError("Mock backend is restricted to synthetic fixtures")
    lock = json.loads((repo / "manifests/models.lock.json").read_text())
    entry = (
        {"id": "mock", "revision": "synthetic", "backend": "mock"}
        if model_id == "mock"
        else next((e for e in lock["entries"] if e["id"] == model_id), None)
    )
    if entry is None:
        deployment = safe_child(root, "deployments/" + model_id + ".json")
        entry = json.loads(deployment.read_text())
        if entry["id"] != model_id:
            raise ValueError("Deployment ID mismatch")
    dl = json.loads((repo / "manifests/datasets.lock.json").read_text())
    data_entry = next((e for e in dl["entries"] if e["id"] == suite), {"revision": "synthetic"})
    if calibration_data is not None:
        data_entry = {"revision": sha256(calibration_data)}
    original_count = len(examples)
    if profile != "full":
        # Stable, evenly spaced selection covers the entire split rather than its prefix.
        count = min(max_samples or (16 if profile == "smoke" else 32), len(examples))
        indices = sorted({int(i * (len(examples) - 1) / max(count - 1, 1)) for i in range(count)})
        examples = [examples[i] for i in indices]
    source_hash = code_hash(repo)
    contract = {
        "model_id": model_id,
        "checkpoint_revision": entry["revision"],
        "backend": entry["backend"],
        "suite": suite,
        "split": "calibration" if calibration_data is not None else "evaluation",
        "dataset_revision": data_entry["revision"],
        "profile": profile,
        "examples_hash": canonical_hash([e.model_dump() for e in examples]),
        "repo_root": str(repo),
        "code_hash": source_hash,
        "workers_hash": sha256(repo / "manifests/workers.lock.json"),
        "max_tokens": max_tokens,
        "candidate_order_ensemble": rotations,
        "calibration_sha256": sha256(Path(calibration)) if calibration else None,
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
        "selected_requests": len(examples),
        "full_split_requests": original_count,
        "eligible": sum(len(e.request.questions) for e in examples),
    }
    run_key = canonical_hash(contract)
    if resume:
        directory = Path(resume).resolve()
        if not directory.is_relative_to(root / "runs"):
            raise ValueError("Resume must reference an external workspace run")
        manifest = json.loads((directory / "manifest.json").read_text())
        if manifest["contract_hash"] != run_key:
            raise ValueError(
                "Model, data, code, protocol or hardware contract changed; create a new run"
            )
    else:
        stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        directory = safe_child(root, f"runs/{model_id}/{suite}/{stamp}-{run_key[:10]}")
        manifest = dict(
            contract,
            run_id=directory.name,
            contract_hash=run_key,
            state="running",
            environment={
                "python": platform.python_version(),
                "packages": {
                    name: importlib.metadata.version(name)
                    for name in ["pydantic", "torch", "transformers", "peft", "accelerate"]
                    if importlib.util.find_spec(name) is not None
                },
            },
        )
    write_json(directory / "manifest.json", manifest)
    if not resume:
        for source in (repo / "src/jev_zoo").glob("*.py"):
            destination = directory / "source/jev_zoo" / source.name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
        write_json(
            directory / "source/receipt.json",
            {
                "code_hash": source_hash,
                "eval_source_files": {
                    p.name: sha256(p)
                    for p in (repo / "src/jev_zoo").glob("*.py")
                    if p.name not in {"training.py", "catalog.py", "release.py"}
                },
            },
        )
    for e in examples:
        write_json(
            directory / "samples" / f"{canonical_hash(e.request.request_id)}.json", e.model_dump()
        )
    load_start = time.perf_counter()
    if entry["backend"] != "mock":
        import torch

        torch.set_num_threads(4)
        torch.cuda.reset_peak_memory_stats()
    try:
        adapter = adapter or create_adapter(entry, root, repo, max_tokens=max_tokens)
        if rotations != 1 or calibration:
            from .variants import Variants

            adapter = Variants(adapter, entry, rotations=rotations, calibration=calibration)
        manifest["protocol"] = adapter.protocol
        manifest["load_seconds"] = time.perf_counter() - load_start
        if entry["backend"] != "mock":
            manifest["environment"]["gpu"] = torch.cuda.get_device_name(0)
            manifest["environment"]["torch_cuda"] = torch.version.cuda
        write_json(directory / "manifest.json", manifest)
        for index, example in enumerate(examples):
            receipt = directory / "receipts" / f"{canonical_hash(example.request.request_id)}.json"
            if receipt.exists():
                continue
            request = example.request.model_copy(deep=True)
            request_hash = canonical_hash(request.model_dump())
            start, started_at = time.perf_counter(), time.time()
            try:
                if entry["backend"] != "mock":
                    torch.cuda.synchronize()
                    start = time.perf_counter()
                response = adapter.predict(request)
                response.validate_against(request)
                if response.resolved_revision != entry["revision"]:
                    raise ValueError("Unresolved or unexpected checkpoint revision")
                if canonical_hash(request.model_dump()) != request_hash:
                    raise ValueError("Adapter mutated inference request")
                if entry["backend"] != "mock":
                    torch.cuda.synchronize()
                elapsed = time.perf_counter() - start
                event = {
                    "request_id": request.request_id,
                    "started_at_unix": started_at,
                    "ended_at_unix": time.time(),
                    "client_e2e_s": elapsed,
                    "response": response.model_dump(),
                    "execution_attempts": 1,
                    "error": None,
                }
            except Exception as error:
                elapsed = time.perf_counter() - start
                # Offline exceptions only. No URL, credentials or request text in error summaries.
                event = {
                    "request_id": request.request_id,
                    "started_at_unix": started_at,
                    "ended_at_unix": time.time(),
                    "client_e2e_s": elapsed,
                    "error": type(error).__name__,
                    "error_detail": str(error)[:400],
                    "execution_attempts": 1,
                    "response": None,
                }
            write_json(receipt, event)
            print(
                f"{model_id}/{suite}: {index + 1}/{len(examples)} error={event['error']}",
                flush=True,
            )
        manifest["state"] = "completed"
        if entry["backend"] != "mock":
            manifest["peak_allocated_gib"] = torch.cuda.max_memory_allocated() / 2**30
    except BaseException as error:
        manifest["state"] = (
            "interrupted" if isinstance(error, (KeyboardInterrupt, SystemExit)) else "load_failed"
        )
        manifest["error"] = type(error).__name__
        manifest["error_detail"] = str(error)[:800]
        raise
    finally:
        write_json(directory / "manifest.json", manifest)
        report(directory)
    return directory


def report(directory: Path):
    manifest = json.loads((directory / "manifest.json").read_text())
    rows, events = [], []
    for path in sorted((directory / "samples").glob("*.json")):
        example = json.loads(path.read_text())
        receipt = directory / "receipts" / path.name
        if not receipt.exists():
            continue
        event = json.loads(receipt.read_text())
        events.append(event)
        answers = {a["question_id"]: a for a in (event.get("response") or {}).get("answers", [])}
        for q in example["request"]["questions"]:
            answer = answers.get(q["id"], {})
            rows.append(
                {
                    "request_id": example["request"]["request_id"],
                    "question_id": q["id"],
                    "group_id": example["group_id"],
                    "task_id": example["task_id"],
                    "label_semantics": example["label_semantics"],
                    "gold": example["gold"][q["id"]],
                    "levels": {o["id"]: o["level"] for o in q["options"]}
                    if q["type"] == "ordinal_score"
                    else None,
                    "selected_option_id": answer.get("selected_option_id"),
                    "probabilities": answer.get("probabilities"),
                    "error": event["error"]
                    or answer.get("error")
                    or (None if answer else "MissingAnswer"),
                }
            )
    metrics = summarize(rows, requested=manifest["eligible"])
    metrics.update(timing_summary(events), peak_allocated_gib=manifest.get("peak_allocated_gib"))
    # Exact completed denominator always retained; bootstrap resamples at request/group level.
    metrics["accuracy_95ci_group_bootstrap"] = grouped_accuracy_interval(rows)
    groups = {}
    for row in rows:
        groups.setdefault(row["task_id"], []).append(row)
    write_json(directory / "metrics.json", metrics)
    write_json(
        directory / "task_metrics.json", {name: summarize(items) for name, items in groups.items()}
    )
    write_json(directory / "rows.json", rows)
    if manifest["suite"] == "jevbench-public" and rows:
        from .official import jevbench_scores

        root = next(p for p in directory.parents if p.name == "runs").parent
        write_json(
            directory / "official_metrics.json",
            jevbench_scores(rows, root, Path(manifest["repo_root"])),
        )
    coverage = f"{metrics['attempted']}/{metrics['eligible']} decisions, {metrics['errors']} errors"
    text = f"# {manifest['model_id']} × {manifest['suite']}\n\nProfile: `{manifest['profile']}`; state: `{manifest['state']}`.\n\n{coverage}.\n\n"
    text += "\n".join(f"- {key}: `{value}`" for key, value in metrics.items()) + "\n"
    (directory / "REPORT.md").write_text(text)
    return metrics
