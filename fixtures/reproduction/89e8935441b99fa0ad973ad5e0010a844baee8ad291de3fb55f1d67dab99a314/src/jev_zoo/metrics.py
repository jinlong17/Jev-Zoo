from __future__ import annotations

import math
import random
import statistics
from collections import defaultdict


def probability_metrics(prediction: dict[str, float], gold: dict[str, float]) -> dict:
    if not set(gold).issubset(prediction):
        raise ValueError("Prediction does not cover gold candidates")
    # Proper scoring uses sum-of-squares multiclass Brier. Clip only inside logs.
    brier = sum((p - gold.get(key, 0.0)) ** 2 for key, p in prediction.items())
    nll = -sum(
        target * math.log(max(prediction[key], 1e-12)) for key, target in gold.items() if target > 0
    )
    kl = sum(
        target * math.log(target / max(prediction[key], 1e-12))
        for key, target in gold.items()
        if target > 0
    )
    tv = 0.5 * sum(abs(p - gold.get(key, 0.0)) for key, p in prediction.items())
    return {"brier": brier, "nll": nll, "kl": kl, "tv": tv, "ovl": 1.0 - tv}


def summarize(rows: list[dict], *, requested: int | None = None) -> dict:
    valid = [row for row in rows if not row.get("error")]
    diagnostic = bool(rows) and all(
        row.get("label_semantics") == "known_probability" for row in rows
    )
    correct = sum(
        row["selected_option_id"] == max(row["gold"], key=row["gold"].get) for row in valid
    )
    result = dict(
        eligible=requested if requested is not None else len(rows),
        attempted=len(rows),
        valid=len(valid),
        correct=correct,
        errors=len(rows) - len(valid),
        accuracy=correct / len(valid) if valid else None,
        accuracy_including_errors=correct / len(rows) if rows else None,
        failure_rate=(len(rows) - len(valid)) / len(rows) if rows else None,
    )
    probabilistic = [row for row in valid if row.get("probabilities") is not None]
    scores = []
    for row in probabilistic:
        prediction, gold = row["probabilities"], row["gold"]
        if row.get("label_semantics") == "known_probability" and row.get("levels"):
            # Sys1Cal score is a scalar probability representation, not a gold 10-way class distribution.
            mu = sum(row["levels"][key] * p for key, p in prediction.items())
            target = sum(row["levels"][key] * p for key, p in gold.items())
            prediction, gold = {"true": mu, "false": 1 - mu}, {"true": target, "false": 1 - target}
        scores.append(probability_metrics(prediction, gold))
    result["probability_valid"] = len(scores)
    for key in ["brier", "nll", "kl", "tv", "ovl"]:
        result[key] = statistics.mean(score[key] for score in scores) if scores else None
    if scores:
        bins = [[] for _ in range(15)]
        for row in probabilistic:
            confidence = max(row["probabilities"].values())
            is_correct = int(row["selected_option_id"] == max(row["gold"], key=row["gold"].get))
            bins[min(int(confidence * 15), 14)].append((confidence, is_correct))
        result["ece"] = sum(
            len(bucket)
            / len(scores)
            * abs(statistics.mean(p for p, _ in bucket) - statistics.mean(c for _, c in bucket))
            for bucket in bins
            if bucket
        )
        ordered = sorted(
            probabilistic, key=lambda row: max(row["probabilities"].values()), reverse=True
        )
        risks, errors = [], 0
        for count, row in enumerate(ordered, 1):
            errors += row["selected_option_id"] != max(row["gold"], key=row["gold"].get)
            risks.append(errors / count)
        result["aurc"] = statistics.mean(risks)
    else:
        result.update(ece=None, aurc=None)
    ordinal_errors = []
    for row in valid:
        levels = row.get("levels")
        if levels:
            expected_gold = sum(levels[key] * value for key, value in row["gold"].items())
            predicted = (
                sum(levels[key] * value for key, value in row["probabilities"].items())
                if row.get("probabilities")
                else levels[row["selected_option_id"]]
            )
            ordinal_errors.append(abs(predicted - expected_gold))
    result["ordinal_mae"] = statistics.mean(ordinal_errors) if ordinal_errors else None
    if diagnostic:
        result.update(
            accuracy=None, accuracy_including_errors=None, correct=None, ece=None, aurc=None
        )
    return result


def grouped_accuracy_interval(rows: list[dict], samples: int = 1000, seed: int = 42) -> list | None:
    if not rows or all(row.get("label_semantics") == "known_probability" for row in rows):
        return None
    groups = defaultdict(list)
    for row in rows:
        groups[row["group_id"]].append(row)
    if len(groups) < 2:
        return None
    groups = list(groups.values())
    generator = random.Random(seed)
    values = []
    for _ in range(samples):
        draw = [row for group in generator.choices(groups, k=len(groups)) for row in group]
        score = sum(
            not row.get("error")
            and row["selected_option_id"] == max(row["gold"], key=row["gold"].get)
            for row in draw
        ) / len(draw)
        values.append(score)
    values.sort()
    return [values[int(samples * 0.025)], values[min(int(samples * 0.975), samples - 1)]]


def timing_summary(events: list[dict]) -> dict:
    values = sorted(event["client_e2e_s"] for event in events if "client_e2e_s" in event)
    return {
        "timing_requests": len(values),
        "p50_client_e2e_s": statistics.median(values) if values else None,
        "p95_client_e2e_s": values[min(math.ceil(len(values) * 0.95) - 1, len(values) - 1)]
        if values
        else None,
    }


def cost_per_correct(total_cost: float | None, correct: int) -> float | None:
    return total_cost / correct if total_cost is not None and correct > 0 else None
