"""Explicit candidate-order averaging and independent post-hoc temperature artifacts."""

from __future__ import annotations

import json
from pathlib import Path

from .calibration import apply_temperature
from .storage import sha256


class Variants:
    def __init__(self, adapter, entry, *, rotations=1, calibration=None):
        if rotations < 1:
            raise ValueError("Rotations must be positive")
        self.adapter = adapter
        self.rotations = rotations
        self.calibrator = None
        self.protocol = {**adapter.protocol, "candidate_order_ensemble": rotations}
        if calibration:
            self.calibrator = json.loads(Path(calibration).read_text())
            if (
                self.calibrator.get("checkpoint_revision") != entry["revision"]
                or self.calibrator.get("partition") != "calibration"
            ):
                raise ValueError(
                    "Temperature artifact must bind this checkpoint and an independent calibration fold"
                )
            self.protocol.update(
                probability_variant="jevzoo-calibrated",
                calibration_sha256=sha256(Path(calibration)),
            )

    def predict(self, request):
        outputs = []
        for shift in range(self.rotations):
            ordered = request.model_copy(deep=True)
            for q in ordered.questions:
                n = len(q.options)
                k = shift % n
                q.options = q.options[k:] + q.options[:k]
            response = self.adapter.predict(ordered)
            response.validate_against(ordered)
            outputs.append(response)
        combined = outputs[0].model_copy(deep=True)
        maps = [{a.question_id: a for a in output.answers} for output in outputs]
        for q, answer in zip(request.questions, combined.answers, strict=True):
            if any(m[q.id].error or m[q.id].probabilities is None for m in maps):
                raise ValueError(
                    "Ensemble/calibration requires complete probabilities in every member"
                )
            p = {
                o.id: sum(m[q.id].probabilities[o.id] for m in maps) / len(maps) for o in q.options
            }
            if self.calibrator:
                answer.metadata["raw_before_jevzoo_calibration"] = p
                p = apply_temperature(p, self.calibrator["temperature"])
                answer.probability_kind = "posthoc_calibrated"
            answer.probabilities = p
            answer.selected_option_id = max(p, key=p.get)
            answer.metadata["candidate_order_members"] = self.rotations
        combined.forward_count = (
            sum(o.forward_count for o in outputs)
            if all(o.forward_count is not None for o in outputs)
            else None
        )
        combined.usage = {
            key: sum(output.usage[key] for output in outputs)
            for key in outputs[0].usage
            if all(isinstance(output.usage.get(key), (int, float)) for output in outputs)
        }
        combined.validate_against(request)
        return combined
