"""Independent calibration folds only; versioned temperatures never fit on evaluation labels."""

from __future__ import annotations

import json
import math
from pathlib import Path

from .storage import canonical_hash, write_json


def apply_temperature(probabilities, temperature):
    if not math.isfinite(temperature) or temperature <= 0:
        raise ValueError("Temperature must be finite and positive")
    values = {k: math.log(max(p, 1e-12)) / temperature for k, p in probabilities.items()}
    top = max(values.values())
    exps = {k: math.exp(v - top) for k, v in values.items()}
    total = sum(exps.values())
    return {k: v / total for k, v in exps.items()}


def fit(rows):
    if not rows or any(row.get("split") != "calibration" for row in rows):
        raise ValueError("Every fitting row must belong to the independent calibration partition")

    def loss(log_t):
        total = 0.0
        for row in rows:
            p = apply_temperature(row["probabilities"], math.exp(log_t))
            total -= sum(q * math.log(max(p[k], 1e-12)) for k, q in row["gold"].items())
        return total / len(rows)

    lo, hi = math.log(0.05), math.log(20)
    ratio = (math.sqrt(5) - 1) / 2
    for _ in range(80):
        left, right = hi - ratio * (hi - lo), lo + ratio * (hi - lo)
        if loss(left) < loss(right):
            hi = right
        else:
            lo = left
    candidates = [0, (lo + hi) / 2]
    best = min(candidates, key=loss)
    return {
        "temperature": math.exp(best),
        "raw_nll": loss(0),
        "calibrated_nll": loss(best),
        "count": len(rows),
        "partition": "calibration",
        "fit_hash": canonical_hash(rows),
    }


def fit_from_run(directory: Path, output: Path):
    manifest = json.loads((directory / "manifest.json").read_text())
    if manifest.get("split") != "calibration":
        raise ValueError("Evaluation runs are ineligible for fitting temperatures")
    rows = json.loads((directory / "rows.json").read_text())
    for row in rows:
        row["split"] = "calibration"
    artifact = fit(rows)
    artifact["source_contract_hash"] = manifest["contract_hash"]
    artifact["checkpoint_revision"] = manifest["checkpoint_revision"]
    artifact["model_id"] = manifest["model_id"]
    write_json(output, artifact)
    return artifact
