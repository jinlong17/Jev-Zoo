"""Extend the existing registry in place; public text/metadata only, no model execution."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import pathlib
import re
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from zoneinfo import ZoneInfo

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
DATE = datetime.now(ZoneInfo("America/Los_Angeles")).date().isoformat()
TYPES = {
    "Official": "tool",
    "SDKs & clients": "tool",
    "Jev-like models": "model",
    "Frameworks & integrations": "framework",
    "Agent tooling": "component",
    "Browser & computer use": "application",
    "Applications": "application",
    "Games & simulations": "application",
    "Demos & playgrounds": "application",
    "Benchmarks & research": "benchmark",
    "Other lists": "directory",
}
PURPOSES = [
    ("routing", r"route|routing|triage|dispatch|路由|分流"),
    ("judging", r"judge|judgment|rubric|grading|score|评判|评分"),
    ("verification", r"verif|guardrail|moderation|safety|policy|核验|验证|安全"),
    ("memory", r"memory|retriev|rerank|search|记忆|检索"),
    ("training", r"train|fine.tun|lora|distill|训练|微调|蒸馏"),
    ("evaluation", r"bench|eval|calibrat|metric|benchmark|评测|校准"),
    ("deployment", r"inference|runtime|serv|deploy|accelerat|推理|部署"),
    ("automation", r"agent|browser|computer|workflow|automation|自动|浏览器"),
    ("simulation", r"game|doom|chess|simulat|pong|游戏|模拟"),
]


def norm(url):
    return str(url).strip().rstrip("/").removesuffix(".git").casefold()


def bilingual_rows(path):
    result = {}
    for line in path.read_text().splitlines():
        if not line.startswith("| ["):
            continue
        cells = [x.strip() for x in line.strip("|").split("|")]
        match = re.match(r"\[([^\]]+)\]\((https://github.com/[^)]+)\)", cells[0])
        if match and len(cells) == 5:
            result[norm(match[2])] = {"name": match[1], "description": cells[4]}
    return result


CURATED_EN = {
    "typesafe-jev": (
        "Hosted typed decisions for text, with choice, Boolean and ordinal outputs.",
        "Closed service; the proprietary RLCD algorithm and weights are not publicly reproducible.",
    ),
    "openai-decisions": (
        "A hosted Decisions API resource for typed questions over text and images.",
        "Commercial inference is disabled in JevZoo; account access and service capabilities remain separate from catalog inclusion.",
    ),
    "clef-flash": (
        "Cloudflare’s 9B multimodal decision model with a dedicated joint schema head.",
        "Load the official head and processor; local and hosted modality support require separate checks.",
    ),
    "clef": (
        "Cloudflare’s 27B multimodal model for decisions over a shared state and schema.",
        "A dedicated joint head is required; HF reference latency is not hosted-service performance.",
    ),
    "pplx-decider": (
        "Perplexity’s open 27B native decision checkpoint with a separate candidate readout.",
        "Pin the native loader and calibration; v1 and v1.1 are different deployments.",
    ),
    "liquid-d1": (
        "Liquid’s hosted decision service, including a separately documented image path.",
        "Free and paid deployment features differ; no commercial requests are run here.",
    ),
    "together-tev1": (
        "Together’s decision-model training report and experimental model resources.",
        "Checkpoint availability, licenses and modalities must be verified individually.",
    ),
    "bespoke-nimble": (
        "An open decision-model project with dataset conversion and training tools.",
        "Model generations and hosted services can have different license and protocol terms.",
    ),
    "databricks-ai-decide": (
        "A managed SQL function for bounded decisions inside data workflows.",
        "A platform function is not a fixed downloadable model checkpoint.",
    ),
    "onejev": (
        "A multimodal decision-model family with local inference, training code and public training data.",
        "Only part of the original training data is redistributable; backend and checkpoint capabilities differ.",
    ),
    "visual-jev-paper": (
        "Shared visual-context decision research with matched LM-head and typed-head controls.",
        "The paper uses Qwen3-VL; converted Choice tasks are distinct from open-answer VQA.",
    ),
    "imajev": (
        "Language adapters and a decision readout for image-and-record checks, with an explicit unknown option.",
        "Retain unknown mass; rotation ensembles, calibration files and conditional probabilities are separate protocols.",
    ),
    "rsi-jev": (
        "A decision-model research loop with multi-exit readouts and adaptive compute.",
        "Current v6.1-VL resources supersede older text-only versions; exit policies need separate evaluation.",
    ),
    "strands-decider": (
        "A small decision-model family using a dynamic pointer head for runtime options.",
        "The current Qwen model uses a Base backbone; inherited vision support is not image-training evidence.",
    ),
    "kev": (
        "Small trainable decision models and local typed-decision tooling.",
        "Provider confidence and the maximum candidate probability are not interchangeable.",
    ),
    "laya": (
        "An encoder-based typed-decision implementation for classification, routing and scoring.",
        "Reported RLCD training is independent of TypeSafe; calibration claims require empirical validation.",
    ),
    "laya-vision": (
        "A visual extension of the Laya decision-model ecosystem.",
        "Code and weight licenses differ; noncommercial terms must remain visible.",
    ),
    "open-jev": (
        "Open decision-model training and inference resources.",
        "The base model and dedicated components must be pinned; these are not TypeSafe weights.",
    ),
    "jev-omni": (
        "Multimodal decision checkpoints with audio, image and video research paths.",
        "Complete training provenance and modality-specific limits need further review.",
    ),
    "startlux": (
        "A decision-model resource for local research and bounded outputs.",
        "Check each checkpoint’s noncommercial terms and total versus active parameter count.",
    ),
    "innerjev": (
        "Reasoning-to-readout self-distillation, now released under SII-Decision names.",
        "Released LoRA-derived models are merged BF16 weights; the supplied decision interface is text-only.",
    ),
    "intern-decision": (
        "Multiple typed fields scored at decision placeholders in a shared forward pass.",
        "Use the exact prompt, placeholder positions, candidate symbols and calibration.",
    ),
    "mapika-decider": (
        "A family of Qwen-based models and recipes for decision inference.",
        "Frozen recipes, trained checkpoints and visual capabilities require separate evidence.",
    ),
    "nanojev": (
        "A small decision-model project with local inference and interactive demonstrations.",
        "A game demonstration does not establish that the model consumes screenshots.",
    ),
    "jpt": (
        "A Qwen-based decision checkpoint for small-model research.",
        "Noncommercial weight terms and untrained image support remain relevant limits.",
    ),
    "winnow": (
        "A 12B decision-model checkpoint and associated inference resources.",
        "Inherited image interfaces do not prove visual decision quality or full training reproducibility.",
    ),
    "chinese-jev": (
        "A Chinese-language decision training pipeline and benchmark research project.",
        "Dedicated released weights were not verified; do not substitute Laya scores under this model name.",
    ),
    "playjev": (
        "Decision-model learning for games using imitation and interactive data collection.",
        "Game returns and offline classification accuracy are separate outcomes.",
    ),
    "prosodia": (
        "An early audio-oriented decision prototype and engineering resource.",
        "Public implementation and experimental maturity remain limited.",
    ),
    "llm2jev-runtime": (
        "A community runtime that exposes model probabilities through a decision interface.",
        "A runtime is not a new trained checkpoint or the LLM-as-Jev paper implementation.",
    ),
    "cygnet": (
        "A decision inference recipe built on an existing language-model backbone.",
        "Separate gains from the backbone, readout, calibration and execution strategy.",
    ),
    "kalm-jev": (
        "A reranker-based decision runtime and integration resource.",
        "Reusing a reranker does not prove training of a general-purpose decision model.",
    ),
    "diffusion-jev": (
        "A typed-decision runtime over a diffusion-language-model backbone.",
        "This is an independent readout implementation, not TypeSafe’s proprietary RLCD.",
    ),
    "jev-visual-mlx": (
        "An Apple-silicon visual decision demonstration.",
        "This community demo is separate from the authors’ Visual Jev research implementation.",
    ),
    "llm2jev-yinsongxu": (
        "A separate community LLM2Jev inference tool.",
        "Similar names do not establish shared authorship with other runtimes or papers.",
    ),
    "jev-mobile": (
        "A mobile-agent system using low-frequency planning and typed execution decisions.",
        "The VLM handles screenshots; Jev’s text controller is not a native visual checkpoint.",
    ),
    "jev-mem": (
        "A memory system that uses typed decisions for retrieval and stopping.",
        "Measure whole-system query quality and cost under a fixed retrieval/context protocol.",
    ),
    "jev-harness": (
        "An agent harness for composing and measuring bounded decisions.",
        "A harness is a system component rather than a new parameterized model.",
    ),
    "jevnext": (
        "Decision algorithms and numeric typed-output resources, formerly jev-numeric.",
        "Retain the old name as an alias and verify the selected implementation.",
    ),
    "reflex-unresolved": (
        "An unresolved resource name retained for identity review.",
        "No canonical source has been established; no runnable or verified badge is assigned.",
    ),
    "pixeljev": (
        "Visual candidate-readout research separating frozen inference, adaptation and calibration.",
        "The paper is available; an author-linked downloadable checkpoint was not verified.",
    ),
    "llm2jev-paper": (
        "LLM-as-Jev research on frozen numeric candidate readouts and targeted fine-tuning.",
        "Tree-factorized multi-token scoring is not equivalent to a single letter-logit readout.",
    ),
    "qwen35-frozen": (
        "Frozen Qwen3.5 baselines for comparing candidate readouts, language LoRA and decision heads.",
        "Instruction and Base checkpoints are different controls; candidate scores are conditionally normalized.",
    ),
    "h2o-lightning": (
        "H2O.ai’s 4B multimodal decision model and official serving shim.",
        "The local HF reference is distinct from official vLLM serving; preserve type-specific temperatures and floors.",
    ),
    "microsoft-decision-1": (
        "Microsoft’s text-only decision-scoring service built on Qwen3.5-9B.",
        "No independent public weights or self-hosting loader were verified; commercial inference remains disabled.",
    ),
}

PAPER_EN = {
    "2610.02076": "Studies when frozen language-model candidate readouts suffice and when targeted adaptation helps.",
    "2610.03935": "Introduces bilingual JEVal and reasoning-to-readout distillation, including probability and system-level reliability limits.",
    "2609.25845": "Compares visual decision readouts and shared-context execution under matched training controls.",
    "2609.29283": "Separates frozen visual choices, few-shot language adaptation and held-out calibration.",
    "2609.35342": "Tests probability recovery with construction-known targets across Boolean, Choice and Score representations.",
    "2610.02586": "Locates label-versus-definition bias in prompt rendering through controlled interventions.",
    "2609.39496": "Compares rejection when a correct answer is absent with Boolean verification of candidate correctness.",
    "2610.01601": "Uses candidate isolation and positional resets to investigate permutation robustness.",
    "2610.07716": "Separates ranking stability from probability stability under menu interventions and additional compute.",
    "2610.07730": "Investigates recursive latent computation before a typed decision readout.",
    "2610.03387": "Evaluates candidate coverage, natural out-of-scope queries and rejection-policy transfer.",
    "2609.29769": "Compares rubric judges and shows how correlated errors limit escalation cascades.",
    "2609.29429": "Evaluates typed judges for alignment failures while auditing question and context effects.",
    "2609.37647": "Compares frozen templates on full public datasets and distinguishes accuracy, calibration and selective prediction.",
    "2610.11392": "Introduces programmatic policy tasks, framing tests and evaluation of probability-induced decisions.",
    "2610.11379": "Studies history reuse, recurrent state storage and approximate layer pruning in candidate inference.",
    "2610.11436": "Tests interactions between adversarial cues and logically equivalent request presentations.",
    "2610.11978": "Compares specialized decisions with general LLMs across knowledge, reasoning and multilingual tasks.",
    "2610.09188": "Investigates search and fixed-budget multi-teacher distillation for decision evaluators.",
    "2610.09328": "Uses reference-bound visual verification probabilities as generator-training rewards.",
    "2610.13092": "Measures when faster local decisions fail to improve whole-agent delivery and recovery.",
    "2609.30186": "Combines visual planning with bounded mobile-agent execution decisions.",
    "2609.23986": "Uses typed decisions to control an agent memory system.",
    "2609.28613": "Tests whether constrained decision outputs resist malicious instructions in untrusted state.",
    "2609.36965": "Provides Chinese-language decision-model training and benchmark research.",
}

TOOLS = [
    (
        "transformers",
        "Hugging Face Transformers",
        "huggingface/transformers",
        "Model architectures, processors and reference inference.",
        "模型架构、处理器与参考推理。",
        ["deployment", "training"],
    ),
    (
        "peft",
        "Hugging Face PEFT",
        "huggingface/peft",
        "Parameter-efficient adaptation, including language-side LoRA.",
        "参数高效适配与语言侧 LoRA。",
        ["training"],
    ),
    (
        "accelerate",
        "Hugging Face Accelerate",
        "huggingface/accelerate",
        "Device orchestration and training-state management.",
        "设备编排与训练状态管理。",
        ["training"],
    ),
    (
        "trl",
        "Hugging Face TRL",
        "huggingface/trl",
        "Fine-tuning and alignment training utilities.",
        "微调与对齐训练工具。",
        ["training"],
    ),
    (
        "datasets",
        "Hugging Face Datasets",
        "huggingface/datasets",
        "Versioned dataset loading and transformation.",
        "版本化数据加载与转换。",
        ["training", "evaluation"],
    ),
    (
        "vllm",
        "vLLM",
        "vllm-project/vllm",
        "Serving and batching for supported model architectures.",
        "兼容模型的服务化与批处理。",
        ["deployment"],
    ),
    (
        "sglang",
        "SGLang",
        "sgl-project/sglang",
        "Structured serving, scheduling and inference optimization.",
        "结构化服务、调度与推理优化。",
        ["deployment"],
    ),
    (
        "lmms-eval",
        "lmms-eval",
        "EvolvingLMMs-Lab/lmms-eval",
        "Multimodal evaluation tasks and protocol integration.",
        "多模态任务与评测协议集成。",
        ["evaluation"],
    ),
    (
        "vlmevalkit",
        "VLMEvalKit",
        "open-compass/VLMEvalKit",
        "Vision-language evaluation and model integrations.",
        "视觉语言评测与模型集成。",
        ["evaluation"],
    ),
    (
        "evalscope",
        "EvalScope",
        "modelscope/evalscope",
        "Quality evaluation and serving-performance tooling.",
        "质量评测与服务性能工具。",
        ["evaluation", "deployment"],
    ),
    (
        "inspect-ai",
        "Inspect AI",
        "UKGovernmentBEIS/inspect_ai",
        "Evaluation workflows for models, agents and tools.",
        "模型、Agent 与工具的评测流程。",
        ["evaluation", "automation"],
    ),
    (
        "llama-factory",
        "LLaMA-Factory",
        "hiyouga/LLaMA-Factory",
        "A configurable open-model fine-tuning framework.",
        "可配置的开放模型微调框架。",
        ["training"],
    ),
    (
        "ms-swift",
        "ms-swift",
        "modelscope/ms-swift",
        "Open-model training, fine-tuning and deployment tools.",
        "开放模型训练、微调与部署工具。",
        ["training", "deployment"],
    ),
    (
        "safetensors",
        "Safetensors",
        "huggingface/safetensors",
        "A tensor serialization format used by model and head releases.",
        "模型与 head 发布采用的张量序列化格式。",
        ["training", "deployment"],
    ),
]


def purposes(text):
    result = [key for key, pattern in PURPOSES if re.search(pattern, text, re.I)]
    return result or ["discovery"]


def inspect_repo(item):
    sid, name, slug, en, zh, uses = item
    url = "https://api.github.com/repos/" + slug
    record = {
        "id": sid,
        "name": name,
        "kind": "framework",
        "source_url": "https://github.com/" + slug,
        "presentation": {
            "resource_type": "framework",
            "description": {"en": en, "zh": zh},
            "purposes": uses,
            "tier": "featured",
            "selection_reason": {
                "en": "Official tooling directly relevant to the existing runtime or research pipeline.",
                "zh": "与现有运行时或研究流程直接相关的官方工具。",
            },
        },
        "adapter_implemented": False,
        "smoke_tested": False,
        "benchmark_reproduced": False,
    }
    evidence = {"url": url, "checked_on": DATE}
    try:
        with urllib.request.urlopen(
            urllib.request.Request(url, headers={"User-Agent": "JevZoo-catalog-metadata"}),
            timeout=20,
        ) as response:
            data = json.load(response)
        record.update(
            publisher=data["owner"]["login"],
            canonical_url=data["html_url"],
            code_license=(data.get("license") or {}).get("spdx_id"),
            verified_on=DATE,
            evidence_status="official_repository_metadata",
            revision=data.get("pushed_at"),
        )
        record["presentation"]["evidence_level"] = "primary_source"
        evidence.update(
            status=200,
            canonical_url=data["html_url"],
            license=record["code_license"],
            repository_updated_at=data.get("pushed_at"),
        )
    except Exception as error:
        evidence.update(status=getattr(error, "code", None), error_type=type(error).__name__)
        record["presentation"].update(tier="review", evidence_level="unverified")
        record["evidence_status"] = "unverified"
    return record, evidence


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reference", type=pathlib.Path, required=True)
    parser.add_argument("--review", type=pathlib.Path)
    parser.add_argument("--evidence", type=pathlib.Path, required=True)
    args = parser.parse_args()
    path = ROOT / "catalog/catalog.json"
    original = path.read_bytes()
    catalog = json.loads(original)
    zh = bilingual_rows(args.reference / "README.zh-Hans.md")
    seen = set()
    dispositions = []
    for entry in catalog["discovery_resources"]:
        primary = norm(entry["url"])
        text = entry.get("description", "")
        status = entry.get("link_status", "unverified")
        tier = "broad" if status == "reachable" and text.strip() else "review"
        if primary in seen:
            tier = "excluded"
            reason = "Duplicate canonical URL; original discovery record retained."
        elif not text.strip():
            reason = "No identifiable use description; retained for review."
        elif status != "reachable":
            reason = "Link is unresolved or failed; kept visible in the review lane."
        else:
            reason = "A specific use is described upstream and the repository link was checked; capability is not independently certified."
        seen.add(primary)
        ptype = TYPES.get(entry.get("category"), "tool")
        if (
            ptype == "model"
            and re.search(r"wrapper|runtime|api server|inference tool", text, re.I)
            and not re.search(r"weights|checkpoint|fine.tun|trained|parameter", text, re.I)
        ):
            ptype = "tool"
        if (
            ptype == "benchmark"
            and re.search(r"\bmodel\b|fine.tun|trained.*head", text, re.I)
            and not re.search(r"benchmark|evaluation.*dataset|calibration.*test", text, re.I)
        ):
            ptype = "model"
        local = zh.get(primary)
        if not local:
            raise ValueError("Missing Chinese catalog identity: " + entry["id"])
        entry["presentation"] = {
            "resource_type": ptype,
            "description": {"en": text, "zh": local["description"]},
            "localized_name": {"en": entry["name"], "zh": local["name"]},
            "publisher": entry["id"].split("/")[0],
            "purposes": purposes(text + " " + local["description"]),
            "tier": tier,
            "selection_reason": {
                "en": reason,
                "zh": {
                    "broad": "上游有明确用途且仓库链接已检查；能力与运行支持尚未独立认证。",
                    "review": "链接、身份或内容仍需核验，保留失败记录。",
                    "excluded": "重复的 canonical URL；保留原发现记录。",
                }[tier],
            },
            "evidence_level": "link_checked" if status == "reachable" else "unverified",
            "limitations": {
                "en": "Discovery description comes from the upstream catalog; runtime, weights and integration claims need independent evidence.",
                "zh": "介绍来自上游目录；实际能力、权重和集成声明需要独立证据。",
            },
        }
        dispositions.append(
            {
                "resource_id": entry["id"],
                "tier": tier,
                "reason": reason,
                "canonical_url": entry["url"],
                "link_status": status,
            }
        )
    for entry in catalog["curated_resources"]:
        en, limit = CURATED_EN.get(
            entry["id"],
            (
                "A typed-decision ecosystem resource.",
                "Review the original component and release terms.",
            ),
        )
        presentation = entry.setdefault("presentation", {})
        ptype = (
            "service"
            if entry["kind"] in ["closed_api", "platform_function"]
            else "paper"
            if entry["kind"] == "paper_only"
            else "tool"
            if entry["kind"] in ["runtime", "algorithm", "training_project"]
            else "application"
            if entry["kind"] in ["agent_system", "demo"]
            else "model"
        )
        presentation.update(
            resource_type=ptype,
            description={
                "en": en,
                "zh": entry.get("recommended_role")
                or entry.get("notes")
                or "类型化概率决策模型与工具。",
            },
            limitations={
                "en": limit,
                "zh": entry.get("notes") or "作者声明、实际执行与完整评测分别记录。",
            },
            purposes=purposes(en + " " + entry.get("notes", "")),
            tier="review" if entry["id"] == "reflex-unresolved" else "featured",
            evidence_level="unverified" if entry["id"] == "reflex-unresolved" else "primary_source",
            selection_reason={
                "en": "Selected for direct model, method, platform or research relevance.",
                "zh": "与模型使用、训练评测或典型研究路线直接相关的精选资源。",
            },
        )
    if args.review:
        source_dir = args.review / "evidence/public_sources"
        rows = list(
            csv.DictReader((args.review / "02_Evidence_Matrix.csv").open(encoding="utf-8-sig"))
        )
        paper_by_url = {
            norm(catalog["sources"][sid]["url"]): r
            for r in catalog["papers"]
            for sid in r.get("source_ids", [])
            if sid in catalog["sources"] and "/abs/" in catalog["sources"][sid]["url"]
        }
        for row in rows:
            if row["类别"] != "研究工作/论文":
                continue
            link = row["论文链接"]
            existing = paper_by_url.get(norm(link))
            sid = "LR-" + row["ID"]
            catalog["sources"][sid] = {
                "url": link,
                "verified_on": DATE,
                "evidence": "official paper metadata; author claims separated from local execution",
            }
            aid = row["ID"].removeprefix("P-")
            en = PAPER_EN.get(
                aid,
                row["方法"]
                if not re.search(r"[\u4e00-\u9fff]", row["方法"])
                else "Background research on "
                + (
                    "benchmark protocols and reference labels."
                    if "classic" in row["核心范围"]
                    else "probability, adaptation or decision evaluation."
                ),
            )
            paper = existing or {"id": "paper-" + re.sub(r"[^a-z0-9]+", "-", aid.lower())}
            paper.update(
                name=row["标题"],
                publisher=row["作者/机构"],
                source_ids=[sid],
                source_url=link,
                category=row["核心范围"],
                why=row["方法"],
                verified_on=DATE,
                evidence_status="official_paper_metadata",
                publication_date=row["日期"],
                publication_date_kind=row["日期口径"],
                updated_on=row["版本或网页更新时间"],
                links={k: [v] for k, v in {"paper": link, "code": row["代码链接"]}.items() if v},
                presentation={
                    "resource_type": "paper",
                    "description": {"en": en, "zh": row["方法"]},
                    "purposes": purposes(en + " " + row["方法"]),
                    "tier": "featured",
                    "evidence_level": "primary_source",
                    "selection_reason": {
                        "en": "Verified literature relevant to a concrete model, protocol or mechanism.",
                        "zh": "核验过的论文，关联明确模型、协议或机制。",
                    },
                    "limitations": {
                        "en": "Reported results are author claims; this catalog is not an independent reproduction.",
                        "zh": "作者成绩与 JevZoo 实测分开；本目录不代表独立复现。",
                    },
                },
            )
            if not existing:
                catalog["papers"].append(paper)
        # Official new asset records, never mark them runnable.
        candidates = [
            "pplx-v11",
            "d3-mini",
            "d3",
            "inner-4b-lora",
            "inner-4b-full",
            "intern-4b",
            "strands-current",
            "rsi4",
            "ci-qwen4b",
        ]
        known = {
            norm(r.get("source_url", ""))
            for r in catalog["curated_resources"]
            if r.get("source_url")
        }
        for sid in candidates:
            metadata = source_dir / (sid + "_meta.json")
            if not metadata.exists():
                continue
            data = json.loads(metadata.read_text())
            link = "https://huggingface.co/" + data["id"]
            if norm(link) in known:
                continue
            en = {
                "pplx-v11": "An updated native 27B decision checkpoint with noncausal full-attention layers.",
                "d3-mini": "A 4B multimodal Decision 3.0 checkpoint with a dedicated candidate head.",
                "d3": "The 27B multimodal Decision 3.0 checkpoint.",
                "inner-4b-lora": "A merged SII-Decision checkpoint trained by reasoning-to-readout LoRA distillation.",
                "inner-4b-full": "A full-rank SII-Decision checkpoint for a matched adaptation comparison.",
                "intern-4b": "A 4B multi-field placeholder-readout decision model.",
                "strands-current": "The current Qwen2B-Base Strands checkpoint with a dynamic pointer head.",
                "rsi4": "A v6.1 multimodal 4B checkpoint for adaptive-compute research.",
                "ci-qwen4b": "A candidate-independent attention model released as a proof of concept.",
            }[sid]
            item = {
                "id": "asset-" + sid,
                "name": data["id"].split("/")[-1],
                "kind": "open_weight_model",
                "source_url": link,
                "publisher": data["id"].split("/")[0],
                "base_model": data.get("cardData", {}).get("base_model"),
                "modalities_declared": ["text"]
                if sid.startswith("inner") or sid == "ci-qwen4b"
                else ["text", "image"],
                "verified_on": DATE,
                "evidence_status": "official_model_card",
                "revision": data["sha"],
                "code_license": None,
                "weight_license": data.get("cardData", {}).get("license"),
                "created_on": data.get("createdAt"),
                "updated_on": data.get("lastModified"),
                "aliases": ["InnerJev-4B-" + ("LoRA" if "lora" in sid else "Full")]
                if sid.startswith("inner")
                else [],
                "adapter_implemented": False,
                "smoke_tested": False,
                "benchmark_reproduced": False,
                "presentation": {
                    "resource_type": "model",
                    "description": {
                        "en": en,
                        "zh": next(
                            (r["方法"] for r in rows if r["ID"] == "M-" + sid),
                            "专用类型化概率决策模型。",
                        ),
                    },
                    "purposes": ["deployment", "evaluation", "training"],
                    "tier": "featured",
                    "evidence_level": "primary_source",
                    "selection_reason": {
                        "en": "Official update after the discovery snapshot; a useful controlled-comparison candidate.",
                        "zh": "发现快照后的官方更新，适合后续受控对照。",
                    },
                    "limitations": {
                        "en": "Not integrated or run in JevZoo. Preserve the native head, attention, processor and calibration.",
                        "zh": "尚未接入或在 JevZoo 实跑；需要锁定专用 head、注意力、processor 与校准。",
                    },
                },
            }
            catalog["curated_resources"].append(item)
            known.add(norm(link))
    logs = []
    with ThreadPoolExecutor(max_workers=3) as pool:
        for record, evidence in pool.map(inspect_repo, TOOLS):
            if not any(
                norm(r.get("source_url", "")) == norm(record["source_url"])
                for r in catalog["curated_resources"]
            ):
                catalog["curated_resources"].append(record)
            logs.append(evidence)
    for r in catalog["curated_resources"]:
        if r["id"] == "llm2jev-paper":
            r["name"] = "LLM-as-Jev"
            r["aliases"] = ["LLM2Jev paper"]
        if r["id"] == "innerjev":
            r["aliases"] = ["InnerJev", "SII-Decision"]
            r["name"] = "SII-Decision / InnerJev"
        if r["id"] == "rsi-jev":
            r["aliases"] = ["RSI-Jev v6.1-VL", "RSI-Jev v6.0-VL"]
    catalog["recipes"] = [
        {
            "id": "recipe-r1-language-lora",
            "name": "R1 language LoRA",
            "resource_type": "recipe",
            "publisher": "JevZoo",
            "description": {
                "en": "Language-side LoRA with frozen visual components and the original LM head; checkpoint save/reload smoke is verified in Lab.",
                "zh": "冻结视觉与原 LM head 的语言侧 LoRA；Lab 已验证保存、恢复与重载 smoke。",
            },
            "purposes": ["training"],
            "related_ids": ["qwen35-frozen", "typed-decisions", "onejev"],
            "scope": "lab_only",
            "config_path": "configs/training/r1.json",
            "validated": "smoke_only",
            "limitations": {
                "en": "Formal gains are unmeasured; cross-source near-duplicate audit and four-role split review remain prerequisites.",
                "zh": "正式训练收益未测；仍需跨源近重复审核与四类划分审查。",
            },
        },
        {
            "id": "recipe-r2-candidate-head",
            "name": "R2 candidate head",
            "resource_type": "recipe",
            "publisher": "JevZoo",
            "description": {
                "en": "An independent candidate head loaded from an explicit R1 checkpoint; real-gradient and reload smoke exists in Lab.",
                "zh": "从显式 R1 checkpoint 加入独立 candidate head；Lab 已有真实梯度与重载 smoke。",
            },
            "purposes": ["training"],
            "related_ids": ["recipe-r1-language-lora", "qwen35-frozen"],
            "scope": "lab_only",
            "config_path": "configs/training/r2.json",
            "validated": "smoke_only",
            "limitations": {
                "en": "Requires R1 provenance and an equal-step continuation control; this is not a validated full training recipe.",
                "zh": "需要 R1 来源与等步继续训练对照；不是已验证的正式训练配方。",
            },
        },
    ]
    catalog["site_contract"] = {
        "schema_version": "1.0",
        "locales": ["en", "zh"],
        "updated_on": DATE,
        "unresolved_keywords": [
            {
                "term": "ETHACC",
                "status": "needs_disambiguation",
                "note": {
                    "en": "Meaning not established; retained without guessing.",
                    "zh": "含义未消歧，保留关键词，不推测定义。",
                },
            }
        ],
        "counts_semantics": "Canonical resources by primary type; runtime and measurements are independent evidence.",
    }
    args.evidence.mkdir(parents=True, exist_ok=True)
    (args.evidence / "catalog-before.json").write_bytes(original)
    (args.evidence / "registry-enrichment-audit.json").write_text(
        json.dumps(
            {
                "checked_on": DATE,
                "upstream_revision": catalog["upstream_revision"],
                "before_sha256": hashlib.sha256(original).hexdigest(),
                "discovery_dispositions": dispositions,
                "official_tool_checks": logs,
                "translation_source": "awesome-jev README.zh-Hans.md at same SHA; MIT attribution retained",
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    print(
        "Registry enriched:",
        len(catalog["discovery_resources"]),
        "discovery;",
        len(catalog["curated_resources"]),
        "curated;",
        len(catalog["papers"]),
        "papers",
    )


if __name__ == "__main__":
    main()
