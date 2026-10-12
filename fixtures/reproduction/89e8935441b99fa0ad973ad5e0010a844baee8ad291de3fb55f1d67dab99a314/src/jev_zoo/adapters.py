"""Offline local inference; official heads are mandatory, never silently replaced."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

from .domain import Answer, DecisionResponse, wire_question
from .storage import safe_child, sha256


def verified_source(root: Path, repo: Path, name: str) -> Path:
    lock = json.loads((repo / "manifests/workers.lock.json").read_text())["workers"][name]
    directory = safe_child(root, lock["path"])
    for relative, digest in lock["files"].items():
        if sha256(safe_child(directory, relative)) != digest:
            raise ValueError(f"Worker source changed: {name}/{relative}")
    return directory


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def images_for(request, root):
    from PIL import Image

    images = []
    for asset in request.assets:
        path = safe_child(root, asset.path)
        if sha256(path) != asset.sha256:
            raise ValueError("Asset digest mismatch")
        with Image.open(path) as image:
            images.append(image.convert("RGB"))
    return images


def native_answer(question, probabilities, **kwargs):
    """Translate provider IDs into immutable dataset IDs, preserving ordinal levels."""
    if question.type == "boolean":
        mapping = {"true" if o.boolean_value else "false": o.id for o in question.options}
    elif question.type == "ordinal_score":
        mapping = {
            str(i): o.id for i, o in enumerate(sorted(question.options, key=lambda o: o.level))
        }
    else:
        mapping = {o.id: o.id for o in question.options}
    mapped = {mapping[str(key)]: float(p) for key, p in probabilities.items()}
    return Answer(
        question_id=question.id,
        selected_option_id=max(mapped, key=mapped.get),
        probabilities=mapped,
        probability_kind="native",
        **kwargs,
    )


class LocalAdapter:
    def __init__(self, entry, root, repo, *, max_tokens=32768):
        import torch

        self.torch, self.entry, self.root, self.repo = torch, entry, root, repo
        self.path = safe_child(root, "models/" + entry["id"])
        self.max_tokens = max_tokens
        self.protocol = {
            "probability_variant": "raw",
            "device": "cuda:0",
            "dtype": "bfloat16",
            "max_input_tokens": max_tokens,
            "candidate_order_ensemble": 1,
        }

    def response(self, request, answers, forwards, usage=None):
        return DecisionResponse(
            request_id=request.request_id,
            answers=answers,
            resolved_revision=self.entry["revision"],
            forward_count=forwards,
            usage=usage or {},
        )


class FrozenHF(LocalAdapter):
    """Full candidate normalization, including exact multi-token continuation scoring."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from transformers import AutoProcessor, Qwen3_5ForConditionalGeneration

        self.processor = AutoProcessor.from_pretrained(self.path, local_files_only=True)
        self.model = (
            Qwen3_5ForConditionalGeneration.from_pretrained(
                self.path, local_files_only=True, dtype=self.torch.bfloat16
            )
            .to("cuda")
            .eval()
        )
        self.protocol["loader"] = "transformers-frozen-reference"
        # Use all verified single-token codes first; exact sequence likelihood remains the fallback.
        tokenizer = self.processor.tokenizer
        self.single_codes = [
            code
            for code in self.labels(702)
            if len(tokenizer.encode(code, add_special_tokens=False)) == 1
        ]
        self.protocol["candidate_codebook"] = (
            "verified single-token codes then multi-token continuations"
        )

    @staticmethod
    def labels(count):
        result = []
        for i in range(count):
            label, n = "", i
            while True:
                label = chr(65 + n % 26) + label
                n = n // 26 - 1
                if n < 0:
                    break
            result.append(label)
        return result

    def inputs(self, request, question, labels):
        images = images_for(request, self.root)
        state = (
            request.state
            if isinstance(request.state, str)
            else json.dumps(request.state, ensure_ascii=False)
        )
        prompt = (
            "Use the evidence to answer the question. Return only the option code.\n"
            + f"State: {state}\nQuestion: {question.instructions}\n"
            + "\n".join(
                f"{label}: {option.text}" for label, option in zip(labels, question.options)
            )
        )
        messages = [
            {
                "role": "user",
                "content": [{"type": "image"} for _ in images] + [{"type": "text", "text": prompt}],
            }
        ]
        rendered = self.processor.apply_chat_template(
            messages, add_generation_prompt=True, tokenize=False, enable_thinking=False
        )
        inputs = self.processor(text=[rendered], images=images or None, return_tensors="pt")
        if inputs["input_ids"].shape[-1] > self.max_tokens:
            raise ValueError("Input exceeds context policy; no truncation performed")
        return rendered, {k: v.to("cuda") for k, v in inputs.items()}

    def predict(self, request):
        torch = self.torch
        answers, forwards, tokens = [], 0, 0
        for q in request.questions:
            count = len(q.options)
            labels = self.single_codes[:count]
            if len(labels) < count:
                labels += [f"OPT{i}" for i in range(count - len(labels))]
            rendered, inputs = self.inputs(request, q, labels)
            tokenizer = self.processor.tokenizer
            prefix = tokenizer.encode(rendered, add_special_tokens=False)
            continuations = []
            for label in labels:
                full = tokenizer.encode(rendered + label, add_special_tokens=False)
                if full[: len(prefix)] != prefix:
                    raise ValueError("Candidate tokenization changes the prompt boundary")
                continuations.append(full[len(prefix) :])
            if any(not c for c in continuations):
                raise ValueError("Empty candidate sequence")
            with torch.inference_mode():
                if all(len(c) == 1 for c in continuations):
                    logits = (
                        self.model(**inputs, logits_to_keep=1, use_cache=False)
                        .logits[0, -1]
                        .float()
                    )
                    scores = logits[torch.tensor([c[0] for c in continuations], device="cuda")]
                    forwards += 1
                    kind = "normalized_candidate_logits"
                else:
                    scores_list = []
                    # Each continuation includes its entire sequence; no top-k approximation.
                    for continuation in continuations:
                        batch = dict(inputs)
                        extra = torch.tensor([continuation], device="cuda")
                        batch["input_ids"] = torch.cat([inputs["input_ids"], extra], dim=1)
                        for key in ("attention_mask", "mm_token_type_ids"):
                            if key in batch:
                                fill = (
                                    torch.ones_like(extra)
                                    if key == "attention_mask"
                                    else torch.zeros_like(extra)
                                )
                                batch[key] = torch.cat([batch[key], fill], dim=1)
                        if batch["input_ids"].shape[-1] > self.max_tokens:
                            raise ValueError("Candidate continuation exceeds context policy")
                        logits = (
                            self.model(
                                **batch, logits_to_keep=len(continuation) + 1, use_cache=False
                            )
                            .logits[0, :-1]
                            .float()
                            .log_softmax(-1)
                        )
                        index = torch.tensor(continuation, device="cuda")
                        scores_list.append(logits.gather(1, index[:, None]).sum())
                        forwards += 1
                    scores = torch.stack(scores_list)
                    kind = "candidate_sequence"
                p = torch.softmax(scores, dim=0).cpu().tolist()
            probabilities = {o.id: float(value) for o, value in zip(q.options, p, strict=True)}
            answers.append(
                Answer(
                    question_id=q.id,
                    probabilities=probabilities,
                    selected_option_id=max(probabilities, key=probabilities.get),
                    probability_kind=kind,
                )
            )
            tokens += int(inputs["input_ids"].shape[-1])
        return self.response(request, answers, forwards, {"input_tokens": tokens})


class Clef(LocalAdapter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ("joint_head_config.json", "joint_head.safetensors"):
            if not (self.path / name).exists():
                raise ValueError("Required Clef joint head missing")
        self.module = load_module("jevzoo_clef_loader", self.path / "joint_schema_model.py")
        self.model, self.processor = self.module.load_release_model(
            str(self.path), device="cuda", dtype=self.torch.bfloat16, local_files_only=True
        )
        self.protocol["loader"] = "official-clef-joint-head"

    def predict(self, request):
        record = {
            "state": request.state,
            "questions": {q.id: wire_question(q) for q in request.questions},
        }
        images = images_for(request, self.root)
        if images:
            record["images"] = images
        encoded = self.module.encode_record(
            self.processor.tokenizer, record, max_length=10**9, processor=self.processor
        )
        if len(encoded.input_ids) > self.max_tokens:
            raise ValueError("Input exceeds context policy; no truncation performed")
        batch = self.module.collate_records(
            [encoded], self.processor.tokenizer.pad_token_id, device="cuda"
        )
        with self.torch.inference_mode():
            logits = self.model(batch)[0]
        answers = []
        for q, native, values in zip(request.questions, encoded.questions, logits, strict=True):
            probabilities = dict(
                zip(
                    native.option_ids,
                    self.torch.softmax(values.float(), -1).cpu().tolist(),
                    strict=True,
                )
            )
            answers.append(native_answer(q, probabilities))
        return self.response(request, answers, 1, {"input_tokens": len(encoded.input_ids)})


class ImaJev(LocalAdapter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        source = verified_source(self.root, self.repo, "imajev")
        sys.path.insert(0, str(source / "src"))
        sys.path.insert(0, str(source / "scripts"))
        from peft import PeftModel
        from torch_decision import TorchDecision

        base = safe_child(
            self.root, "models/qwen35-" + ("2b" if self.entry["id"].endswith("2b") else "4b")
        )
        self.engine = TorchDecision(str(base), "cuda", max_length=self.max_tokens)
        self.engine.model = PeftModel.from_pretrained(
            self.engine.model, str(self.path), local_files_only=True
        ).eval()
        if not self.engine.enable_readout(self.path, trainable=False):
            raise ValueError("Required imajev decision readout missing")
        self.protocol.update(
            loader="official-imajev-torch-lora-readout",
            probability_variant="raw-conditional-known",
            unknown_mass_policy="retain separately; conditional known probabilities",
            rotations=1,
        )

    def predict(self, request):
        from vision_decision.jev_api import to_request
        from vision_decision.scoring import UNKNOWN, compile_question

        native = to_request(
            {
                "state": request.state,
                "questions": {q.id: wire_question(q) for q in request.questions},
            },
            request_id=request.request_id,
            max_options=self.engine.max_options,
        )
        images = images_for(request, self.root)
        answers, tokens = [], 0
        for q, field in zip(request.questions, native.fields, strict=True):
            header, choices, texts = compile_question(
                field, native.state, self.engine.prompt_layout
            )
            labels = self.engine.labels(len(choices), len(images))
            prompt = header + "\n".join(
                f"{label}: {text}" for label, text in zip(labels, texts, strict=True)
            )
            _, inputs, ids = self.engine.prepare(images, prompt, labels)
            with self.torch.inference_mode():
                logits = self.engine.candidate_logits(inputs, ids)
                all_p = self.torch.softmax(logits.float(), -1).cpu().tolist()
            mapping = {
                ("true" if key else "false") if isinstance(key, bool) else str(key): float(p)
                for (key, _), p in zip(choices, all_p, strict=True)
            }
            unknown = mapping.pop(UNKNOWN)
            total = sum(mapping.values())
            if total <= 0:
                raise ValueError("No known probability mass")
            p = {key: value / total for key, value in mapping.items()}
            answers.append(
                native_answer(
                    q,
                    p,
                    metadata={
                        "unknown_probability": unknown,
                        "abstained": unknown >= max(mapping.values()),
                        "unconditional_known": mapping,
                    },
                    provider_confidence=(len(p) * max(p.values()) - 1)
                    / (len(p) - 1)
                    * (1 - unknown),
                )
            )
            tokens += inputs["input_ids"].shape[-1]
        return self.response(request, answers, len(answers), {"input_tokens": int(tokens)})


class H2O(FrozenHF):
    """Official prompt/label contract ported to Transformers. Separate from vLLM results."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.module = load_module("jevzoo_h2o_shim", self.path / "h2o_lightning_shim.py")
        self.contract = self.module.Contract(
            json.loads((self.path / "serve_config.json").read_text()), env={}
        )
        self.protocol.update(
            loader="h2o-hf-reference",
            official_runtime="vllm (not measured here)",
            probability_variant="raw",
            noul_floor=0,
        )

    def predict(self, request):
        answers, tokens = [], 0
        images = images_for(request, self.root)
        state = self.module.render_state(request.state, self.contract.state_compact)
        for q in request.questions:
            native = wire_question(q)
            if images:
                _, rendered, names, _, labels = self.contract.image_prompt(
                    state, native, ["local"] * len(images), q.id
                )
            else:
                rendered, names, _, labels = self.contract.question_prompt(state, native, q.id)
            inputs = self.processor(text=[rendered], images=images or None, return_tensors="pt")
            if inputs["input_ids"].shape[-1] > self.max_tokens:
                raise ValueError("Input exceeds context policy")
            tok = self.processor.tokenizer
            prefix = tok.encode(rendered, add_special_tokens=False)
            ids = []
            for label in labels:
                encoded = tok.encode(rendered + " " + label, add_special_tokens=False)
                if encoded[:-1] != prefix:
                    raise ValueError("H2O label is not one token at its native boundary")
                ids.append(encoded[-1])
            with self.torch.inference_mode():
                logits = (
                    self.model(
                        **{k: v.to("cuda") for k, v in inputs.items()},
                        logits_to_keep=1,
                        use_cache=False,
                    )
                    .logits[0, -1, ids]
                    .float()
                )
                p = logits.softmax(-1).cpu().tolist()
            probabilities = dict(zip(names, p, strict=True))
            typ = native["type"]
            official = self.module.format_answer(
                typ,
                names,
                [o.text for o in q.options],
                logits.cpu().tolist(),
                self.contract.temperature_by_type[typ],
                self.contract.noul_floor,
            )
            answers.append(
                native_answer(q, probabilities, metadata={"official_calibrated_answer": official})
            )
            tokens += int(inputs["input_ids"].shape[-1])
        return self.response(request, answers, len(answers), {"input_tokens": tokens})


class OneJev(LocalAdapter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        source = verified_source(self.root, self.repo, "onejev")
        sys.path.insert(0, str(source))
        from qev.mm_engine import MMDecisionEngine

        self.engine = MMDecisionEngine(
            str(self.path),
            device="cuda:0",
            dtype="bfloat16",
            fork_mode="sequential",
            cuda_graphs=False,
            media_root=str(self.root),
            max_request_tokens=self.max_tokens,
            max_branch_tokens=self.max_tokens,
        )
        self.protocol.update(loader="official-onejev-mm", fork_mode="sequential", debias=1)
        self.forward_calls = 0

        def count_forward(module, args):
            self.forward_calls += 1

        self.engine.model.model.register_forward_pre_hook(count_forward)

    def predict(self, request):
        from qev.schema import SystemOneRequest

        state = request.state
        media = None
        if request.assets:
            images_for(request, self.root)  # verify before official loader reads paths
            state = (
                "\n".join(f"<image:{i + 1}>" for i in range(len(request.assets)))
                + "\n"
                + json.dumps(state, ensure_ascii=False)
            )
            media = [{"type": "image", "path": asset.path} for asset in request.assets]
        native = SystemOneRequest.model_validate(
            {"state": state, "questions": {q.id: wire_question(q) for q in request.questions}}
        )
        self.forward_calls = 0
        output, metadata = self.engine.decide(native, debias=1, media=media)
        answers = []
        for q in request.questions:
            value = output.answers[q.id].model_dump()
            probabilities = (
                {"true": value["noul"], "false": 1 - value["noul"]}
                if q.type == "boolean"
                else value["probabilities"]
            )
            answers.append(
                native_answer(
                    q,
                    probabilities,
                    provider_confidence=value.get("confidence"),
                    raw_provider_score=value.get("score"),
                )
            )
        return self.response(request, answers, self.forward_calls, output.usage.model_dump())


class Pplx(LocalAdapter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sys.path.insert(0, str(self.path / "source/src"))
        from autojev.model import DecisionModel

        self.model = DecisionModel(checkpoint=self.path, device="cuda")
        self.protocol.update(
            loader="official-autojev-readout",
            probability_variant="official-calibrated",
            max_input_tokens=min(self.max_tokens, 8192),
            temperature=self.model.temperature,
        )

    def predict(self, request):
        from autojev.model import answer

        images_for(request, self.root)
        answers = []
        for q in request.questions:
            native = wire_question(q)
            row = {
                "state": request.state
                if isinstance(request.state, str)
                else json.dumps(request.state),
                "question": native,
            }
            if request.assets:
                row["images"] = [safe_child(self.root, asset.path) for asset in request.assets]
            batch = self.model.prepare([row], max_length=min(self.max_tokens, 8192))
            with self.torch.inference_mode():
                logits = self.model(batch)[0, : batch.counts[0]]
                raw = logits.softmax(-1).cpu().tolist()
                values = (logits / self.model.temperature).softmax(-1).cpu().tolist()
            result = answer(native, values)
            probabilities = (
                {"true": result["noul"], "false": 1 - result["noul"]}
                if q.type == "boolean"
                else result["probabilities"]
            )
            answers.append(
                native_answer(
                    q,
                    probabilities,
                    raw_provider_score=result.get("score"),
                    metadata={
                        "raw_probabilities_native_order": raw,
                        "temperature": self.model.temperature,
                    },
                )
            )
        return self.response(request, answers, len(answers))


class Mock:
    protocol = {"loader": "synthetic-mock", "probability_variant": "synthetic"}

    def __init__(self, entry, *args, **kwargs):
        self.entry = entry

    def predict(self, request):
        answers = []
        for q in request.questions:
            selected = str(request.state["selected"])
            p = {o.id: float(o.id == selected) for o in q.options}
            answers.append(
                Answer(
                    question_id=q.id,
                    selected_option_id=selected,
                    probabilities=p,
                    probability_kind="native",
                )
            )
        return DecisionResponse(
            request_id=request.request_id,
            answers=answers,
            resolved_revision="synthetic",
            forward_count=0,
        )


def create_adapter(entry, root, repo, **kwargs):
    classes = {
        "frozen_hf": FrozenHF,
        "clef": Clef,
        "imajev": ImaJev,
        "h2o": H2O,
        "onejev": OneJev,
        "pplx": Pplx,
        "mock": Mock,
        "trained_hf": TrainedHF,
    }
    return classes[entry["backend"]](entry, root, repo, **kwargs)


class TrainedHF(FrozenHF):
    def __init__(self, entry, root, repo, **kwargs):
        from peft import PeftModel

        base_entry = next(
            e
            for e in json.loads((repo / "manifests/models.lock.json").read_text())["entries"]
            if e["id"] == entry["base_model_id"]
        )
        if entry["base_revision"] != base_entry["revision"]:
            raise ValueError("Training base revision changed")
        checkpoint = safe_child(root, entry["checkpoint"])
        for relative, digest in entry["files"].items():
            if sha256(safe_child(checkpoint, relative)) != digest:
                raise ValueError("Trained checkpoint changed")
        super().__init__(base_entry, root, repo, **kwargs)
        self.entry = entry
        self.model = PeftModel.from_pretrained(
            self.model, str(checkpoint), local_files_only=True
        ).eval()
        self.head = None
        if entry["stage"] == "R2":
            from safetensors.torch import load_file

            weight = load_file(str(checkpoint / "decision_head.safetensors"), device="cuda")[
                "weight"
            ]
            self.head = self.torch.nn.Linear(
                weight.shape[1],
                weight.shape[0],
                bias=False,
                device="cuda",
                dtype=self.torch.float32,
            )
            self.head.weight.data.copy_(weight)
            self.head.eval()
        self.protocol.update(
            loader="trained-hf-language-lora", stage=entry["stage"], probability_variant="raw"
        )

    def predict(self, request):
        if self.head is None:
            return super().predict(request)
        answers, tokens = [], 0
        for q in request.questions:
            if len(q.options) > self.head.out_features:
                raise ValueError("Candidate head capacity exceeded")
            _, inputs = self.inputs(request, q, self.labels(len(q.options)))
            with self.torch.inference_mode():
                hidden = (
                    self.model.get_base_model()
                    .model(**inputs, use_cache=False)
                    .last_hidden_state[0, -1]
                    .float()
                )
                p = self.head(hidden)[: len(q.options)].softmax(-1).cpu().tolist()
            probabilities = {o.id: float(value) for o, value in zip(q.options, p, strict=True)}
            answers.append(
                Answer(
                    question_id=q.id,
                    selected_option_id=max(probabilities, key=probabilities.get),
                    probabilities=probabilities,
                    probability_kind="native",
                )
            )
            tokens += inputs["input_ids"].shape[-1]
        return self.response(request, answers, len(answers), {"input_tokens": int(tokens)})
