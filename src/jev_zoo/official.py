"""Official metric modules loaded from separately pinned upstream source."""

from .adapters import load_module, verified_source


def jevbench_scores(rows, root, repo):
    source = verified_source(root, repo, "jevbench")
    metrics = load_module("jevzoo_official_jevbench_metrics", source / "jevbench/metrics.py")
    pairs, briers, ordinal, family = [], [], [], {}
    for row in rows:
        correct = False
        if not row.get("error"):
            target = max(row["gold"], key=row["gold"].get)
            if row.get("levels") and row.get("probabilities"):
                expected = row["levels"][target]
                predicted = sum(row["levels"][k] * p for k, p in row["probabilities"].items())
                ordinal.append((expected, predicted))
                correct = round(predicted) == expected
            else:
                correct = row["selected_option_id"] == target
            if row.get("probabilities"):
                p = row["probabilities"]
                briers.append(metrics.brier_score(p, target, list(p)))
                pairs.append((max(p.values()), correct))
        record = family.setdefault(row["task_id"], {"n_scorable": 0, "n_correct": 0})
        record["n_scorable"] += 1
        record["n_correct"] += int(correct)
    for record in family.values():
        record["accuracy"] = record["n_correct"] / record["n_scorable"]
    return {
        "scope": "JevBench public files only; no sealed or composite score",
        "macro_accuracy": metrics.macro_accuracy(family),
        "brier": sum(briers) / len(briers) if briers else None,
        "ece_10bins": metrics.ece_top_label(pairs)["ece"] if pairs else None,
        "ordinal_mae": metrics.ordinal_mae(ordinal),
        "per_family": family,
    }
