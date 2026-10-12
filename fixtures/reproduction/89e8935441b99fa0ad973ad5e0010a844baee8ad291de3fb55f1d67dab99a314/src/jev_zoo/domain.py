from __future__ import annotations

import math
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Option(StrictModel):
    id: str = Field(min_length=1)
    text: str
    level: float | None = None
    boolean_value: bool | None = Field(default=None, strict=True)


class Question(StrictModel):
    id: str = Field(min_length=1)
    type: Literal["choice", "boolean", "ordinal_score"]
    instructions: str
    options: list[Option] = Field(min_length=2)

    @model_validator(mode="after")
    def valid_options(self):
        ids = [option.id for option in self.options]
        if len(ids) != len(set(ids)):
            raise ValueError("Duplicate option IDs")
        if self.type == "boolean":
            if set(ids) == {"true", "false"}:
                for option in self.options:
                    option.boolean_value = option.id == "true"
            if len(ids) != 2 or {option.boolean_value for option in self.options} != {True, False}:
                raise ValueError(
                    "Boolean questions need one explicitly true and one false candidate"
                )
        if self.type == "ordinal_score":
            levels = [option.level for option in self.options]
            if any(level is None or not math.isfinite(level) for level in levels):
                raise ValueError("Ordinal levels must be finite numbers")
            if len(levels) != len(set(levels)):
                raise ValueError("Ordinal levels must be unique")
        return self


class Asset(StrictModel):
    id: str
    path: str
    sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    mime: str


class DecisionRequest(StrictModel):
    request_id: str
    state: dict | str
    questions: list[Question] = Field(min_length=1)
    assets: list[Asset] = Field(default_factory=list)

    @model_validator(mode="after")
    def unique_questions(self):
        ids = [question.id for question in self.questions]
        if len(ids) != len(set(ids)):
            raise ValueError("Duplicate question IDs")
        asset_ids = [asset.id for asset in self.assets]
        if len(asset_ids) != len(set(asset_ids)):
            raise ValueError("Duplicate asset IDs")
        return self


class SupervisedExample(StrictModel):
    request: DecisionRequest
    gold: dict[str, dict[str, float]]
    group_id: str
    task_id: str
    split: str
    label_semantics: str = "reference_label"

    @model_validator(mode="after")
    def validate_targets(self):
        if set(self.gold) != {question.id for question in self.request.questions}:
            raise ValueError("Gold question IDs must match the request")
        for question in self.request.questions:
            target = self.gold[question.id]
            if not set(target).issubset({option.id for option in question.options}):
                raise ValueError("Unknown gold candidate")
            if any(not math.isfinite(p) or p < 0 for p in target.values()):
                raise ValueError("Invalid gold probabilities")
            if abs(sum(target.values()) - 1.0) > 1e-4:
                raise ValueError("Gold distribution must sum to one")
        return self

    def inference_payload(self) -> dict:
        return self.request.model_dump()


class Answer(StrictModel):
    question_id: str
    selected_option_id: str | None = None
    probabilities: dict[str, float] | None = None
    probability_kind: Literal[
        "native",
        "normalized_candidate_logits",
        "candidate_sequence",
        "posthoc_calibrated",
        "label_only",
        "self_reported",
        "unavailable",
    ]
    provider_confidence: float | None = None
    raw_provider_score: float | None = None
    metadata: dict = Field(default_factory=dict)
    error: str | None = None

    def validate_against(self, question: Question) -> None:
        ids = {option.id for option in question.options}
        if self.question_id != question.id:
            raise ValueError("Answer question ID mismatch")
        if self.error:
            return
        if self.selected_option_id not in ids:
            raise ValueError("Unknown selected option")
        if self.probabilities is not None:
            if set(self.probabilities) != ids:
                raise ValueError("Incomplete or unexpected probability candidates")
            if any(not math.isfinite(p) or p < 0 or p > 1 for p in self.probabilities.values()):
                raise ValueError("Invalid probability value")
            if abs(sum(self.probabilities.values()) - 1.0) > 1e-3:
                raise ValueError("Probability distribution does not sum to one")


class DecisionResponse(StrictModel):
    request_id: str
    answers: list[Answer]
    resolved_revision: str
    timing: dict[str, float] = Field(default_factory=dict)
    usage: dict = Field(default_factory=dict)
    forward_count: int | None = None

    def validate_against(self, request: DecisionRequest) -> None:
        if self.request_id != request.request_id:
            raise ValueError("Response request ID mismatch")
        mapping = {answer.question_id: answer for answer in self.answers}
        if len(mapping) != len(self.answers) or set(mapping) != {q.id for q in request.questions}:
            raise ValueError("Missing, duplicate or unexpected answers")
        for question in request.questions:
            mapping[question.id].validate_against(question)


class PublicRunSummary(StrictModel):
    schema_version: Literal["1.0"] = "1.0"
    release_id: str
    model_id: str
    checkpoint_revision: str
    benchmark_id: str
    dataset_revision: str
    profile: Literal["smoke", "full", "diagnostic", "synthetic"]
    metrics: dict[str, float | int | None]
    protocol: dict[str, str | int | float | bool | None]
    reproduction_level: Literal["fully_public", "public_protocol_private_assets", "internal_only"]


def wire_question(question: Question) -> dict:
    typ = {"boolean": "noul", "ordinal_score": "score", "choice": "choice"}[question.type]
    if question.type == "ordinal_score":
        criteria = [
            option.text for option in sorted(question.options, key=lambda option: option.level)
        ]
    elif question.type == "boolean":
        criteria = {
            "true" if option.boolean_value else "false": option.text for option in question.options
        }
    else:
        criteria = {option.id: option.text for option in question.options}
    return {"type": typ, "instructions": question.instructions, "criteria": criteria}
