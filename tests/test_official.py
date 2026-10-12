from pathlib import Path

import pytest

from jev_zoo.adapters import load_module
from jev_zoo.metrics import probability_metrics


def test_official_brier_parity_and_ordinal():
    scorer = load_module(
        "jevbench_fixture", Path(__file__).parents[1] / "fixtures/official/jevbench_metrics.py"
    )
    for p, expected in [({"yes": 0.8, "no": 0.2}, "yes"), ({"a": 0.1, "b": 0.3, "c": 0.6}, "b")]:
        ours = probability_metrics(p, {expected: 1})
        assert ours["brier"] == pytest.approx(scorer.brier_score(p, expected, list(p)))
    assert scorer.ordinal_mae([(1, 1.2), (3, 2.8)]) == pytest.approx(0.2)
    assert scorer.ece_top_label([(0.8, True), (0.8, False)])["ece"] == pytest.approx(0.3)
