from __future__ import annotations

import csv
import hashlib
import io
import json
from pathlib import Path

from .domain import Asset, DecisionRequest, Option, Question, SupervisedExample
from .storage import read_jsonl, safe_child, workspace

SUITES = [
    "jevbench-public",
    "typed-decisions",
    "jeval",
    "decisionbench",
    "mmstar",
    "sys1cal",
    "banking77",
    "clinc150",
    "sst2",
    "boolq",
    "arc",
]


def decode(value):
    if isinstance(value, str):
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return value
    return value


def question_from_wire(identifier: str, value: dict) -> Question:
    typ = str(value["type"]).lower()
    criteria = value.get("criteria", value.get("options"))
    if typ in {"noul", "boolean", "predicate"}:
        options = [
            Option(id="true", text=(criteria or {}).get("true", "True")),
            Option(id="false", text=(criteria or {}).get("false", "False")),
        ]
        typ = "boolean"
    elif typ in {"score", "ordinal_score"}:
        options = [
            Option(id=str(i), text=str(item), level=float(i)) for i, item in enumerate(criteria)
        ]
        typ = "ordinal_score"
    elif typ == "choice":
        if isinstance(criteria, dict):
            options = [
                Option(id=str(key), text=str(description)) for key, description in criteria.items()
            ]
        else:
            options = [
                Option(id=str(i), text=str(description)) for i, description in enumerate(criteria)
            ]
    else:
        raise ValueError(f"Unsupported question type: {typ}")
    instruction = value.get("instructions", value.get("question", "Choose the correct option."))
    if not isinstance(instruction, str):
        instruction = json.dumps(instruction, ensure_ascii=False)
    return Question(id=identifier, type=typ, instructions=instruction, options=options)


def _target(value, question: Question) -> dict[str, float]:
    value = decode(value)
    if isinstance(value, dict) and "probabilities" in value:
        value = value["probabilities"]
    if isinstance(value, dict):
        value = {
            str(key).lower() if question.type == "boolean" else str(key): float(p)
            for key, p in value.items()
        }
        return value
    if isinstance(value, bool):
        key = "true" if value else "false"
    else:
        key = str(value)
        if question.type == "boolean":
            key = {
                "true": "true",
                "false": "false",
                "1": "true",
                "0": "false",
                "yes": "true",
                "no": "false",
            }.get(key.lower(), key.lower())
    ids = [option.id for option in question.options]
    if key not in ids and isinstance(value, int) and 0 <= value < len(ids):
        key = ids[value]
    if key not in ids:
        raise ValueError("Target does not map to a legal option")
    return {key: 1.0}


def _example(
    identifier, state, questions, gold, group, task, split, semantics="reference_label", assets=None
):
    return SupervisedExample(
        request=DecisionRequest(
            request_id=str(identifier), state=state, questions=questions, assets=assets or []
        ),
        gold=gold,
        group_id=str(group or identifier),
        task_id=task,
        split=split,
        label_semantics=semantics,
    )


def _parquet_rows(paths: list[Path]):
    import pyarrow.parquet as parquet

    for path in paths:
        reader = parquet.ParquetFile(path)
        for batch in reader.iter_batches(batch_size=128):
            yield from batch.to_pylist()


def load_suite(suite: str, root: Path | None = None) -> list[SupervisedExample]:
    root = workspace(root)
    location = safe_child(root, f"datasets/{suite}")
    if suite == "synthetic-smoke":
        return synthetic()
    if not location.exists():
        raise ValueError(f"Dataset not downloaded: {suite}")
    examples = []
    if suite == "jevbench-public":
        for path in sorted((location / "datasets/public").glob("*.jsonl")):
            for row in read_jsonl(path):
                q = question_from_wire("decision", row["question"])
                examples.append(
                    _example(
                        row["id"],
                        row["state"],
                        [q],
                        {q.id: _target(row["expected"], q)},
                        row.get("group"),
                        f"jevbench-public/{row.get('family', 'unknown')}",
                        "public",
                    )
                )
    elif suite == "typed-decisions":
        for row in _parquet_rows(sorted((location / "all").glob("test-*.parquet"))):
            questions = [
                question_from_wire(key, value) for key, value in decode(row["questions"]).items()
            ]
            gold = decode(row["gold"])
            examples.append(
                _example(
                    row["id"],
                    decode(row["state"]),
                    questions,
                    {q.id: _target(gold[q.id], q) for q in questions},
                    row["id"],
                    f"typed-decisions/{row['workflow']}",
                    "test",
                    "teacher_agreement",
                )
            )
    elif suite == "jeval":
        for row in _parquet_rows([location / "data/test.parquet"]):
            questions = [
                question_from_wire(key, value)
                for key, value in decode(row["questions_json"]).items()
            ]
            if len(questions) != 1:
                raise ValueError("JEVal importer expects exactly one scored question per row")
            q = questions[0]
            examples.append(
                _example(
                    row["id"],
                    decode(row["state"]),
                    questions,
                    {q.id: _target(decode(row["label_json"]), q)},
                    row["source_item_id"],
                    f"jeval/{row['source']}",
                    "test",
                )
            )
    elif suite == "decisionbench":
        for row in _parquet_rows(sorted((location / "data").glob("eval-*.parquet"))):
            candidates = decode(row["candidates_json"])
            ordinal = row["primitive"] == "ordinal_scoring"
            options = [
                Option(
                    id=str(c["id"]),
                    text=str(c.get("description") or c["label"]),
                    level=float(c["ordinal_value"]) if ordinal else None,
                )
                for c in candidates
            ]
            # Hanno IDs (c000/c001) remain immutable even for its Boolean primitive.
            q = Question(
                id="decision",
                type="ordinal_score" if ordinal else "choice",
                instructions=row["instruction"],
                options=options,
            )
            gold = {
                option.id: float(p)
                for option, p in zip(options, row["gold_probabilities"], strict=True)
            }
            examples.append(
                _example(
                    row["row_id"],
                    decode(row["state_json"]),
                    [q],
                    {q.id: gold},
                    row["row_id"],
                    f"decisionbench/{row['task_id']}",
                    "eval",
                )
            )
    elif suite == "mmstar":
        from PIL import Image

        for row in _parquet_rows([location / "mmstar.parquet"]):
            raw = row["image"]
            raw = raw["bytes"] if isinstance(raw, dict) else raw
            if not isinstance(raw, bytes):
                raise ValueError("MMStar image bytes are missing")
            digest = hashlib.sha256(raw).hexdigest()
            with Image.open(io.BytesIO(raw)) as image:
                mime = Image.MIME.get(image.format, "image/jpeg")
            asset_path = safe_child(root, f"datasets/mmstar/extracted/{digest}.image")
            asset_path.parent.mkdir(exist_ok=True)
            if not asset_path.exists():
                asset_path.write_bytes(raw)
            # Original image MCQ includes its option descriptions. Scoring A/B/C/D
            # reproduces its direct-option protocol without rewriting the question.
            q = Question(
                id="decision",
                type="choice",
                instructions=row["question"],
                options=[Option(id=letter, text=letter) for letter in "ABCD"],
            )
            examples.append(
                _example(
                    f"mmstar-{row['index']}",
                    {},
                    [q],
                    {q.id: {row["answer"]: 1.0}},
                    digest,
                    f"mmstar/{row['category']}",
                    "val",
                    assets=[
                        Asset(
                            id=digest,
                            path=str(asset_path.relative_to(root)),
                            sha256=digest,
                            mime=mime,
                        )
                    ],
                )
            )
    elif suite == "sys1cal":
        path = location / "datasets/generated/v0.1.0_tiny_cleanvars_parallel_primitives.jsonl"
        for row in read_jsonl(path):
            queries = row["queries"]
            questions = []
            for identifier, value in queries.items():
                typ = (
                    "boolean"
                    if identifier == "noul"
                    else "ordinal_score"
                    if identifier == "score"
                    else "choice"
                )
                if typ == "boolean":
                    options = [Option(id="true", text="True"), Option(id="false", text="False")]
                elif typ == "ordinal_score":
                    options = [
                        Option(id=str(i), text=str(text), level=i / 9)
                        for i, text in enumerate(value["levels"])
                    ]
                else:
                    options = [
                        Option(id=str(option).lower(), text=str(option))
                        for option in value["options"]
                    ]
                instruction = " ".join(
                    str(value.get(key, "")) for key in ["question", "proposition"]
                ).strip()
                questions.append(
                    Question(id=identifier, type=typ, instructions=instruction, options=options)
                )
            p = row["gold_distribution"].get("A", row["gold_distribution"].get("True"))
            gold = {
                q.id: (
                    {"true": p, "false": 1 - p}
                    if q.type != "ordinal_score"
                    else {"0": 1 - p, "9": p}
                )
                for q in questions
            }
            examples.append(
                _example(
                    row["instance_id"],
                    row["state"],
                    questions,
                    gold,
                    row["latent_instance_id"],
                    f"sys1cal/{row['family']}",
                    "test",
                    "known_probability",
                )
            )
    elif suite in {"banking77", "clinc150", "sst2", "boolq", "arc"}:
        examples = _classic(suite, location)
    else:
        raise ValueError(f"Unknown suite: {suite}")
    if not examples:
        raise ValueError(f"No examples loaded for {suite}")
    ids = [example.request.request_id for example in examples]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate request IDs in a suite")
    return examples


def _classic(suite, location):
    examples = []
    if suite == "banking77":
        source = location / "banking_data"
        labels = json.loads((source / "categories.json").read_text())
        with (source / "test.csv").open() as handle:
            rows = list(csv.DictReader(handle))
    else:
        split = "validation" if suite in {"sst2", "boolq"} else "test"
        prefix = "plus" if suite == "clinc150" else "ARC-Challenge" if suite == "arc" else "data"
        rows = list(_parquet_rows(sorted((location / prefix).glob(f"{split}-*.parquet"))))
        if suite == "clinc150":
            info = (
                json.loads((location / "dataset_infos.json").read_text())
                if (location / "dataset_infos.json").exists()
                else None
            )
            labels = (
                info["plus"]["features"]["intent"]["names"] if info else _clinc_labels(location)
            )
    for index, row in enumerate(rows):
        if suite == "banking77":
            options = [Option(id=label, text=label.replace("_", " ")) for label in labels]
            state, instructions, answer = (
                row["text"],
                "Identify the banking customer intent.",
                row["category"],
            )
        elif suite == "clinc150":
            options = [Option(id=label, text=label.replace("_", " ")) for label in labels]
            state, instructions, answer = (
                row["text"],
                "Identify the intent, including out-of-scope requests.",
                labels[row["intent"]],
            )
        elif suite == "sst2":
            options = [
                Option(id="negative", text="Negative"),
                Option(id="positive", text="Positive"),
            ]
            state, instructions, answer = (
                row["sentence"],
                "Classify the sentiment.",
                ["negative", "positive"][row["label"]],
            )
        elif suite == "boolq":
            options = [Option(id="true", text="Yes"), Option(id="false", text="No")]
            state, instructions, answer = (
                row["passage"],
                row["question"],
                "true" if row["answer"] else "false",
            )
        else:
            options = [
                Option(id=label, text=text)
                for label, text in zip(row["choices"]["label"], row["choices"]["text"], strict=True)
            ]
            state, instructions, answer = "", row["question"], row["answerKey"]
        q = Question(
            id="decision",
            type="boolean" if suite == "boolq" else "choice",
            instructions=instructions,
            options=options,
        )
        examples.append(
            _example(
                f"{suite}-{index}",
                state,
                [q],
                {q.id: {answer: 1.0}},
                f"{suite}-{index}",
                suite,
                "validation" if suite in {"sst2", "boolq"} else "test",
            )
        )
    return examples


def _clinc_labels(location):
    import pyarrow.parquet as parquet

    path = next((location / "plus").glob("test-*.parquet"))
    metadata = json.loads(parquet.read_schema(path).metadata[b"huggingface"])
    return metadata["info"]["features"]["intent"]["names"]


def synthetic() -> list[SupervisedExample]:
    examples = []
    for i in range(96):
        typ = ["choice", "boolean", "ordinal_score"][i % 3]
        ids = ["true", "false"] if typ == "boolean" else ["a", "b", "c"]
        q = Question(
            id="decision",
            type=typ,
            instructions="Select the explicitly named option.",
            options=[
                Option(id=key, text=key, level=float(j) if typ == "ordinal_score" else None)
                for j, key in enumerate(ids)
            ],
        )
        selected = ids[(i // 3) % len(ids)]
        examples.append(
            _example(
                f"synthetic-{i:03}",
                {"selected": selected},
                [q],
                {q.id: {selected: 1.0}},
                f"synthetic-{i}",
                "synthetic-smoke",
                "test",
                "synthetic",
            )
        )
    return examples
