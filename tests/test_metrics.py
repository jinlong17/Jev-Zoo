import math

import pytest

from jev_zoo.calibration import apply_temperature, fit
from jev_zoo.metrics import (
    cost_per_correct,
    probability_metrics,
    summarize,
)


def row(**extra):
    return dict(
        gold={"a": 1.0},
        probabilities={"a": 0.7, "b": 0.3},
        selected_option_id="a",
        error=None,
        group_id="one",
        **extra,
    )


def test_proper_scores_and_missing_mass():
    m = probability_metrics({"a": 0.7, "b": 0.3}, {"a": 1})
    assert m["brier"] == pytest.approx(0.18)
    assert m["nll"] == pytest.approx(-math.log(0.7))
    assert m["tv"] == pytest.approx(0.3)
    assert m["ovl"] == pytest.approx(0.7)
    with pytest.raises(ValueError):
        probability_metrics({"b": 1}, {"a": 1})


def test_errors_retained_and_unavailable_probabilities_na():
    a = row()
    b = {**row(), "error": "OOM", "probabilities": None, "selected_option_id": None}
    m = summarize([a, b], requested=3)
    assert (m["eligible"], m["attempted"], m["errors"], m["accuracy_including_errors"]) == (
        3,
        2,
        1,
        0.5,
    )
    assert summarize([{**a, "probabilities": None}])["nll"] is None
    assert cost_per_correct(None, 10) is None
    assert cost_per_correct(1, 0) is None


def test_sys1cal_score_is_scalar_probability_not_fake_class_target():
    r = dict(
        gold={"lo": 0.3, "hi": 0.7},
        probabilities={"lo": 0, "mid": 1, "hi": 0},
        levels={"lo": 0, "mid": 0.7, "hi": 1},
        selected_option_id="mid",
        error=None,
        label_semantics="known_probability",
        group_id="x",
    )
    m = summarize([r])
    assert m["tv"] == pytest.approx(0)
    assert m["accuracy"] is None
    assert m["ordinal_mae"] == pytest.approx(0)
    assert m["ece"] is None


def test_calibration_rejects_test_and_preserves_probability_mapping():
    with pytest.raises(ValueError):
        fit([{**row(), "split": "test"}])
    result = fit([{**row(), "split": "calibration"}])
    assert result["calibrated_nll"] <= result["raw_nll"]
    p = apply_temperature({"a": 0.8, "b": 0.2}, 2)
    assert sum(p.values()) == pytest.approx(1)
    assert set(p) == {"a", "b"}
    with pytest.raises(ValueError):
        apply_temperature(p, 0)
