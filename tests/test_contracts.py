import pytest
from pydantic import ValidationError

from jev_zoo.adapters import FrozenHF, native_answer
from jev_zoo.domain import Answer, DecisionRequest, Option, Question, wire_question
from jev_zoo.tasks import _target, synthetic


def choice():
    return Question(
        id="route",
        type="choice",
        instructions="Which?",
        options=[Option(id=str(i), text=str(i)) for i in range(77)],
    )


def test_large_candidate_mapping_complete():
    q = choice()
    p = {str(i): 1 / 77 for i in range(77)}
    a = native_answer(q, p)
    a.validate_against(q)
    assert len(FrozenHF.labels(151)) == 151 and len(set(FrozenHF.labels(151))) == 151
    assert FrozenHF.labels(27)[-1] == "AA"


@pytest.mark.parametrize(
    "bad",
    [
        {"0": 1},
        {"0": float("nan"), **{str(i): 0 for i in range(1, 77)}},
        {str(i): 0.5 for i in range(77)},
    ],
)
def test_reject_incomplete_invalid_probability(bad):
    a = Answer(
        question_id="route", selected_option_id="0", probabilities=bad, probability_kind="native"
    )
    with pytest.raises(ValueError):
        a.validate_against(choice())


def test_ordinal_preserves_ids_and_numeric_order():
    q = Question(
        id="score",
        type="ordinal_score",
        instructions="Score",
        options=[Option(id="high", text="high", level=10), Option(id="low", text="low", level=-1)],
    )
    assert wire_question(q)["criteria"] == ["low", "high"]
    a = native_answer(q, {"0": 0.2, "1": 0.8})
    assert a.probabilities == {"low": 0.2, "high": 0.8}


def test_boolean_semantics_with_native_ids():
    q = Question(
        id="b",
        type="boolean",
        instructions="Yes?",
        options=[
            Option(id="c000", text="No", boolean_value=False),
            Option(id="c001", text="Yes", boolean_value=True),
        ],
    )
    assert native_answer(q, {"true": 0.9, "false": 0.1}).selected_option_id == "c001"
    with pytest.raises(ValidationError):
        Question(
            id="b",
            type="boolean",
            instructions="?",
            options=[Option(id="a", text="a"), Option(id="b", text="b")],
        )


def test_gold_never_in_request_and_no_truthiness_bug():
    e = synthetic()[0]
    payload = e.inference_payload()
    assert set(payload) == {"request_id", "state", "questions", "assets"}
    assert "gold" not in payload
    q = Question(
        id="x",
        type="boolean",
        instructions="?",
        options=[Option(id="true", text="Yes"), Option(id="false", text="No")],
    )
    assert _target("no", q) == {"false": 1}
    assert _target("false", q) == {"false": 1}
    with pytest.raises(ValueError):
        _target("unknown", q)


def test_strict_request_rejects_annotations():
    request = synthetic()[0].inference_payload()
    request["gold"] = "leak"
    with pytest.raises(ValidationError):
        DecisionRequest.model_validate(request)
