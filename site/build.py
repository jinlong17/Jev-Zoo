"""Static bilingual projection of the existing registry and approved runtime evidence.

Uses the standard library only. Does not import evaluator code, scan raw runs,
download assets, or execute a model. Generated files belong outside the checkout.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import pathlib
import re
import shutil
from collections import Counter
from datetime import datetime
from zoneinfo import ZoneInfo

ROOT = pathlib.Path(__file__).resolve().parents[1]
PUBLIC = "https://github.com/jinlong17/Jev-Zoo"
LAB = "https://github.com/jinlong17/Jev-Zoo-Lab"
TYPE_LABELS = {
    "model": ("Models", "模型"),
    "paper": ("Papers", "论文"),
    "tool": ("Tools & SDKs", "工具与 SDK"),
    "framework": ("Frameworks", "框架"),
    "benchmark": ("Benchmarks", "基准"),
    "dataset": ("Data", "数据"),
    "component": ("Agent components", "Agent 组件"),
    "application": ("Applications & demos", "应用与演示"),
    "service": ("Services", "商业服务"),
    "recipe": ("Recipes", "配方"),
    "directory": ("Discovery lists", "资源索引"),
}
USE_LABELS = {
    "routing": ("Routing", "路由"),
    "judging": ("Judging", "评判"),
    "verification": ("Verification & safety", "验证与安全"),
    "memory": ("Memory & retrieval", "记忆与检索"),
    "training": ("Training & distillation", "训练与蒸馏"),
    "evaluation": ("Evaluation & calibration", "评测与校准"),
    "deployment": ("Inference & deployment", "推理与部署"),
    "automation": ("Agents & automation", "Agent 与自动化"),
    "simulation": ("Games & simulation", "游戏与模拟"),
    "discovery": ("Resource discovery", "资源发现"),
}
OPEN_LABELS = {
    "code_open": ("Open code", "开源代码"),
    "weights_open": ("Open weights", "开放权重"),
    "data_public": ("Public data", "公开数据"),
    "closed_api": ("Closed API", "闭源 API"),
    "public_paper": ("Public paper", "公开论文"),
    "unknown": ("Not verified", "未核验"),
    "restricted_code": ("Restricted code (Lab)", "受限代码（Lab）"),
}
FORM_LABELS = {
    "repository": ("Repository", "代码仓库"),
    "download": ("Downloadable asset", "可下载资产"),
    "hosted_api": ("Hosted API", "托管 API"),
    "managed_platform": ("Managed platform", "商业平台"),
    "lab_only": ("Lab only", "仅 Lab"),
}


IMPLEMENTED_TASKS = {
    "typed-decisions",
    "jeval",
    "decisionbench",
    "mmstar",
    "banking77",
    "clinc150",
    "sst2",
    "boolq",
    "arc",
    "jevbench-public",
    "sys1cal",
}


def read(path, default=None):
    return json.loads(path.read_text()) if path.exists() else default


def format_accuracy(value):
    return "N/A" if value is None else f"{float(value) * 100:.2f}%"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(url):
    url = str(url or "").strip().rstrip("/").removesuffix(".git")
    if not url.startswith(("https://", "http://")):
        return ""
    url = re.sub(
        r"github.com/amazingljy1206/InnerJev",
        "github.com/amazingljy1206/SII-Decision",
        url,
        flags=re.I,
    )
    url = re.sub(
        r"huggingface.co/jylin001206/InnerJev",
        "huggingface.co/jylin001206/SII-Decision",
        url,
        flags=re.I,
    )
    return url.casefold()


def slug(identity):
    return (
        re.sub(r"[^a-z0-9]+", "-", identity.casefold()).strip("-")
        + "-"
        + hashlib.sha1(identity.encode()).hexdigest()[:6]
    )


def h(value):
    return html.escape(str(value), quote=True)


def tr(record, key, locale):
    value = record.get(key, "")
    return value.get(locale, value.get("en", "")) if isinstance(value, dict) else value


def link_kind(url):
    if (
        "arxiv.org/" in url
        or "doi.org/" in url
        or "aclanthology.org/" in url
        or "proceedings.mlr.press/" in url
    ):
        return "paper"
    if "huggingface.co/datasets/" in url:
        return "data"
    if "huggingface.co/spaces/" in url:
        return "demo"
    if "huggingface.co/" in url and "/docs/" not in url:
        return "weights"
    if "github.com/" in url:
        return "code"
    return "docs"


def source_links(entry, sources):
    links = {}
    for kind, values in entry.get("links", {}).items():
        for url in values if isinstance(values, list) else [values]:
            if canonical(url):
                links.setdefault(kind, []).append(url)
    urls = [entry["source_url"]] if entry.get("source_url") else []
    urls += [sources[key]["url"] for key in entry.get("source_ids", []) if key in sources]
    for url in urls:
        if canonical(url):
            links.setdefault(link_kind(url), []).append(url)
    return {key: list(dict.fromkeys(values)) for key, values in links.items()}


def approved_results(repo, public_repo, approved_manifest=None):
    """Require summary bytes to match exact approved release hashes, never filename alone."""
    # Prefer the committed evidence projection so identical source produces identical
    # pages before and after a newer public release marker is written.
    manifest = (
        read(approved_manifest)
        if approved_manifest
        else read(repo / "site/approved-results-manifest.json")
    )
    if manifest is None and public_repo:
        approval = read(public_repo / "release/approved-files.json", {})
        release_id = approval.get("release_id")
        workspace = pathlib.Path(
            __import__("os").environ.get("JEVZOO_WORKSPACE", str(repo.parent / "jev-zoo-workspace"))
        )
        manifest = (
            read(workspace / "releases" / str(release_id) / "candidate.json")
            if release_id
            else None
        )
    if not manifest or not isinstance(manifest.get("files"), dict):
        return [], None
    result = []
    for relative, expected in manifest["files"].items():
        if not relative.startswith("results/published/") or not relative.endswith(".json"):
            continue
        file = repo / relative
        if not file.exists() or digest(file) != expected:
            continue
        item = read(file, {})
        if not {"model_id", "benchmark_id", "profile", "metrics", "checkpoint_revision"}.issubset(
            item
        ):
            continue
        result.append(
            {
                key: item[key]
                for key in [
                    "model_id",
                    "benchmark_id",
                    "profile",
                    "metrics",
                    "checkpoint_revision",
                    "dataset_revision",
                    "protocol",
                ]
                if key in item
            }
            | {
                "approval_release_id": manifest["release_id"],
                "summary_sha256": expected,
                "source_path": relative,
            }
        )
    return result, {
        "release_id": manifest["release_id"],
        "content_hash": manifest["content_hash"],
        "files": {r["source_path"]: r["summary_sha256"] for r in result},
    }


def compile_catalog(repo, public_repo=None, approved_manifest=None):
    catalog = read(repo / "catalog/catalog.json")
    models = read(repo / "manifests/models.lock.json")["entries"]
    datasets = read(repo / "manifests/datasets.lock.json")["entries"]
    approved, approval = approved_results(repo, public_repo, approved_manifest)
    records = {}
    redirects = {}
    dispositions = []
    sources = catalog["sources"]

    def add(record, prefer=False):
        primary = canonical(record.get("canonical_url")) or "unresolved:" + record["id"]
        old = records.get(primary)
        if old:
            winner = old
            redirects[record["id"]] = winner["id"]
            winner["aliases"] = list(
                dict.fromkeys(
                    winner.get("aliases", [])
                    + [record["id"], record["name"]]
                    + record.get("aliases", [])
                )
            )
            for key, values in record.get("links", {}).items():
                winner["links"][key] = list(dict.fromkeys(winner["links"].get(key, []) + values))
            winner["purposes"] = list(
                dict.fromkeys(winner["purposes"] + record.get("purposes", []))
            )
            winner["related_ids"] = list(
                dict.fromkeys(winner.get("related_ids", []) + record.get("related_ids", []))
            )
            winner["source_record_ids"] = list(
                dict.fromkeys(
                    winner["source_record_ids"] + record.get("source_record_ids", [record["id"]])
                )
            )
            if prefer:
                for key in [
                    "name",
                    "publisher",
                    "description",
                    "limitations",
                    "resource_type",
                    "tier",
                    "evidence_level",
                    "verified_on",
                    "modalities",
                    "service_form",
                    "licenses",
                    "openness",
                    "publication_date",
                    "updated_on",
                    "source_revision",
                    "selection_reason",
                    "runtime",
                    "subtype",
                    "asset_metadata",
                ]:
                    if record.get(key) not in [None, "", [], {}]:
                        if key in ["description", "limitations"] and record.get("runtime", {}).get(
                            "deployment_id"
                        ):
                            continue
                        winner[key] = record[key]
            dispositions.append(
                {
                    "resource_id": record["id"],
                    "disposition": "merged_alias",
                    "canonical_id": winner["id"],
                    "reason": "Same normalized primary URL; metadata merged, discovery retained.",
                }
            )
            return winner
        record.setdefault("aliases", [])
        record.setdefault("related_ids", [])
        record.setdefault("source_record_ids", [record["id"]])
        record.setdefault(
            "runtime",
            {
                "cataloged": True,
                "source_verified": record.get("evidence_level") == "primary_source",
                "adapter_implemented": False,
                "smoke_tested": False,
                "fully_evaluated": False,
                "blocked_reason": {
                    "en": "Not integrated in JevZoo.",
                    "zh": "尚未在 JevZoo 内接入。",
                },
                "evaluated_scopes": [],
            },
        )
        record["slug"] = slug(record["id"])
        records[primary] = record
        redirects[record["id"]] = record["id"]
        return record

    for entry in catalog["discovery_resources"]:
        p = entry.get("presentation", {})
        ptype = p.get("resource_type", "tool")
        license = entry.get("code_license")
        add(
            {
                "id": entry["id"],
                "name": entry["name"],
                "publisher": p.get("publisher", entry["id"].split("/")[0]),
                "canonical_url": entry["url"],
                "resource_type": ptype,
                "subtype": "repository",
                "description": p.get(
                    "description", {"en": entry["description"], "zh": entry["description"]}
                ),
                "purposes": p.get("purposes", ["discovery"]),
                "tier": p.get("tier", "review"),
                "selection_reason": p.get("selection_reason", {}),
                "evidence_level": p.get("evidence_level", "unverified"),
                "verified_on": entry.get("checked_on"),
                "publication_date": None,
                "updated_on": entry.get("upstream_pushed_at"),
                "added_on": entry.get("upstream_added_on"),
                "source_revision": entry.get("site_primary_review", {}).get("readme_blob_revision")
                or catalog["upstream_revision"],
                "source_revision_kind": "README Git blob"
                if entry.get("site_primary_review")
                else "discovery commit",
                "source_name": catalog["upstream"],
                "original_category": entry.get("category"),
                "links": {
                    "code": [entry["url"]],
                    **(
                        {"docs": [entry["site_primary_review"]["readme_url"]]}
                        if entry.get("site_primary_review", {}).get("readme_url")
                        else {}
                    ),
                },
                "modalities": ["unknown"],
                "service_form": "repository",
                "openness": ["code_open"]
                if license and license not in ["NOASSERTION", "unknown", "other"]
                else ["unknown"],
                "licenses": {"code": license or "unverified"},
                "limitations": p.get("limitations", {}),
                "link_status": entry.get("link_status", "unverified"),
                "language": entry.get("language"),
                "aliases": entry.get("aliases", []),
            }
        )
    for entry in catalog["curated_resources"] + catalog["papers"] + catalog["benchmarks"]:
        if entry.get("proposal"):
            dispositions.append(
                {
                    "resource_id": entry["id"],
                    "disposition": "excluded",
                    "reason": "Unbuilt proposed benchmark; no public asset. Retained in planning, not represented as a real catalog asset.",
                }
            )
            continue
        links = source_links(entry, sources)
        p = entry.get("presentation", {})
        kind = entry.get("kind", "paper" if entry in catalog["papers"] else "benchmark")
        ptype = p.get("resource_type", "paper" if kind == "paper" else "benchmark")
        ptype = "paper" if entry["id"] == "visual-jev-paper" else ptype
        order = (
            ["paper", "code", "weights", "docs", "data"]
            if ptype == "paper"
            else ["data", "code", "docs", "weights", "paper"]
            if ptype in ["benchmark", "dataset"]
            else ["weights", "code", "docs", "paper", "data"]
            if kind == "open_weight_model"
            else ["code", "docs", "weights", "paper", "data"]
        )
        primary = (
            entry.get("canonical_url")
            or entry.get("source_url")
            or next((links[key][0] for key in order if links.get(key)), None)
        )
        if entry["id"] in [
            "onejev",
            "imajev",
            "innerjev",
            "strands-decider",
            "rsi-jev",
            "intern-decision",
            "bespoke-nimble",
            "visual-jev-paper",
        ]:
            if ptype == "paper" and links.get("paper"):
                primary = links["paper"][0]
            elif links.get("code"):
                primary = links["code"][0]
        if entry["id"] == "qwen35-frozen":
            primary = "https://github.com/QwenLM/Qwen3.5"
            links.setdefault("code", []).append(primary)
        license = entry.get("weight_license") or (
            "apache-2.0" if entry["id"] in ["clef", "clef-flash", "h2o-lightning"] else None
        )
        openness = (
            ["closed_api"]
            if kind in ["closed_api", "platform_function"]
            else ["weights_open"]
            if kind == "open_weight_model"
            and entry.get("evidence_status") in ["official_model_card", "source_reviewed"]
            and entry["id"] not in ["laya-vision", "startlux", "jpt"]
            else ["public_paper"]
            if ptype == "paper"
            else ["unknown"]
        )
        if entry.get("code_license"):
            openness.append("code_open")
        subtype = (
            "checkpoint"
            if str(primary).startswith("https://huggingface.co/")
            and "/datasets/" not in str(primary)
            else "family"
            if ptype == "model"
            else "resource"
        )
        add(
            {
                "id": entry["id"],
                "name": entry["name"],
                "publisher": entry.get("publisher")
                or (
                    str(primary).split("/")[3]
                    if "github.com/" in str(primary) or "huggingface.co/" in str(primary)
                    else entry["name"].split()[0]
                ),
                "canonical_url": primary,
                "resource_type": ptype,
                "subtype": subtype,
                "description": p.get(
                    "description",
                    {
                        "en": entry.get("name"),
                        "zh": entry.get("why") or entry.get("notes") or entry.get("name"),
                    },
                ),
                "purposes": p.get(
                    "purposes", ["evaluation"] if ptype == "benchmark" else ["discovery"]
                ),
                "tier": p.get("tier", "featured"),
                "selection_reason": p.get(
                    "selection_reason",
                    {"en": "Selected existing protocol or resource.", "zh": "现有精选协议或资源。"},
                ),
                "evidence_level": p.get(
                    "evidence_level", "primary_source" if entry.get("source_ids") else "unverified"
                ),
                "verified_on": entry.get("verified_on") or "2026-10-06",
                "publication_date": entry.get("publication_date"),
                "publication_date_kind": entry.get("publication_date_kind"),
                "model_release_date": entry.get("model_release_date"),
                "created_on": entry.get("created_on"),
                "updated_on": entry.get("updated_on"),
                "source_revision": entry.get("revision"),
                "source_name": "Official primary sources",
                "links": links,
                "modalities": entry.get(
                    "modalities_declared", ["text"] if ptype == "paper" else ["unknown"]
                ),
                "service_form": "hosted_api"
                if kind == "closed_api"
                else "managed_platform"
                if kind == "platform_function"
                else "download"
                if subtype == "checkpoint"
                else "repository",
                "openness": openness,
                "licenses": {
                    "weights": license or "unverified",
                    "code": entry.get("code_license") or "unverified",
                },
                "limitations": p.get(
                    "limitations",
                    {
                        "en": "Source licenses, protocol and asset availability require separate review.",
                        "zh": entry.get("notes") or "源许可、协议与资产可用性需要独立核验。",
                    },
                ),
                "aliases": entry.get("aliases", []),
                "related_ids": entry.get("related_ids", []),
                "link_status": "unverified" if not primary else "primary_source",
                "asset_metadata": {
                    key: entry.get(key)
                    for key in ["base_model", "parameter_scale_label", "training_access"]
                },
                "benchmark_metadata": {
                    key: entry[key] for key in ["reported_size_or_version", "scope"] if key in entry
                },
            },
            prefer=not (
                ptype == "benchmark"
                and records.get(canonical(primary), {}).get("resource_type")
                in ["paper", "model", "component", "application"]
            ),
        )
    model_records = {}
    deployed = []
    for model in models:
        relevant = [
            r
            for r in approved
            if r["model_id"] == model["id"] and r["checkpoint_revision"] == model["revision"]
        ]
        full = [
            r
            for r in relevant
            if r["profile"] == "full"
            and r["metrics"].get("eligible", 0) > 0
            and r["metrics"].get("attempted") == r["metrics"].get("eligible")
        ]
        smoke = any(r["profile"] == "smoke" and r["metrics"].get("errors") == 0 for r in relevant)
        state = {
            "cataloged": True,
            "source_verified": True,
            "adapter_implemented": bool(relevant),
            "smoke_tested": smoke,
            "fully_evaluated": bool(full),
            "blocked_reason": None
            if relevant
            else {
                "en": "No approved execution evidence for this checkpoint. Integration requires a separate code review.",
                "zh": "该 checkpoint 暂无已批准执行证据；接入实现需独立代码审查。",
            },
            "evaluated_scopes": [
                {
                    "benchmark": r["benchmark_id"],
                    "requests": r["metrics"].get("eligible"),
                    "errors": r["metrics"].get("errors"),
                    "approval_release_id": r["approval_release_id"],
                }
                for r in full
            ],
            "checkpoint_revision": model["revision"],
            "deployment_id": model["id"],
        }
        parent = (
            "qwen35-frozen"
            if model["backend"] == "frozen_hf"
            else "onejev"
            if model["backend"] == "onejev"
            else "imajev"
            if model["backend"] == "imajev"
            else "pplx-decider"
            if model["backend"] == "pplx"
            else "h2o-lightning"
            if model["backend"] == "h2o"
            else model["id"]
        )
        record = add(
            {
                "id": "checkpoint-" + model["id"],
                "name": model["repo_id"].split("/")[-1],
                "publisher": model["repo_id"].split("/")[0],
                "canonical_url": "https://huggingface.co/" + model["repo_id"],
                "resource_type": "model",
                "subtype": "checkpoint",
                "asset_metadata": {
                    "base_model": model.get("base_model"),
                    "parameter_scale_label": model["repo_id"].split("/")[-1],
                    "training_access": "See component terms / 见组件条款",
                },
                "description": {
                    "en": f"A pinned {model['backend']} deployment in JevZoo, with independent checkpoint and task evidence.",
                    "zh": f"JevZoo 已接入的 {model['backend']} 部署，按 checkpoint 与任务分别记录证据。",
                },
                "purposes": ["deployment", "evaluation", "training"]
                if model["backend"] == "frozen_hf"
                else ["deployment", "evaluation"],
                "tier": "featured",
                "evidence_level": "primary_source",
                "verified_on": catalog["as_of"],
                "source_revision": model["revision"],
                "source_name": "Official model card and JevZoo approved summaries",
                "links": {"weights": ["https://huggingface.co/" + model["repo_id"]]},
                "modalities": ["text", "image"]
                if model["backend"] != "onejev"
                else ["text", "image", "video"],
                "service_form": "download",
                "openness": ["weights_open"],
                "licenses": {
                    "weights": model.get("license", "unverified"),
                    "base": "separate component terms",
                },
                "limitations": {
                    "en": "Full evaluation is scoped to listed approved benchmarks. HF client latency is not a controlled service comparison.",
                    "zh": "全量证据仅限列明并批准的基准；HF 客户端延迟不是受控服务性能比较。",
                },
                "related_ids": [parent],
                "runtime": state,
            },
            prefer=True,
        )
        record["links"].setdefault("results", []).extend(
            PUBLIC + "/blob/main/" + x["source_path"] for x in full
        )
        model_records[model["id"]] = record
        if state["adapter_implemented"]:
            deployed.append(
                {
                    "deployment_id": model["id"],
                    "resource_id": record["id"],
                    "checkpoint_revision": model["revision"],
                    "backend": model["backend"],
                    "runtime": state,
                }
            )
    dataset_records = {}
    tasks = []
    for dataset in datasets:
        sid = dataset["id"]
        url = (
            "https://huggingface.co/datasets/"
            if dataset["source"] == "huggingface"
            else "https://github.com/"
        ) + dataset["repo_id"]
        name = {
            "typed-decisions": "Typed Decisions",
            "jeval": "JEVal",
            "decisionbench": "DecisionBench data",
            "mmstar": "MMStar",
            "banking77": "Banking77",
            "clinc150": "CLINC150 + OOS",
            "sst2": "SST-2",
            "boolq": "BoolQ",
            "arc": "ARC-Challenge",
            "onejev-data": "OneJev-Data",
            "jevbench-public": "JevBench public",
            "sys1cal": "Sys1Cal-v1",
        }[sid]
        r = add(
            {
                "id": "data-" + sid,
                "name": name,
                "publisher": dataset["repo_id"].split("/")[0],
                "canonical_url": url,
                "resource_type": "dataset",
                "subtype": "dataset",
                "description": {
                    "en": "Pinned public data used by the evaluation or training platform. Original split, target semantics and component licenses stay explicit.",
                    "zh": "训练评测平台采用的固定版本公开数据；保留原划分、标签语义与来源许可。",
                },
                "purposes": ["training"]
                if sid == "onejev-data"
                else ["evaluation", "training"]
                if sid == "typed-decisions"
                else ["evaluation"],
                "tier": "featured",
                "evidence_level": "primary_source",
                "verified_on": catalog["as_of"],
                "source_revision": dataset["revision"],
                "source_name": "Official data source and pinned manifest",
                "links": {"data": [url]},
                "modalities": ["text", "image"]
                if sid == "mmstar"
                else ["text", "image", "video"]
                if sid == "onejev-data"
                else ["text"],
                "service_form": "download",
                "openness": ["data_public"],
                "licenses": {"data": dataset.get("license") or "unverified"},
                "limitations": {
                    "en": "Public visibility is not a blanket data license. Teacher distributions and known probabilities are distinct from reference labels.",
                    "zh": "公开可见不代表统一许可；teacher 分布、已知概率与参考标签分别解释。",
                },
                "related_ids": [],
            },
            prefer=False,
        )
        dataset_records[sid] = r
        if sid in IMPLEMENTED_TASKS:
            task_approved = [
                x
                for x in approved
                if x["benchmark_id"] == sid and x.get("dataset_revision") == dataset["revision"]
            ]
            task_smoke = any(
                x["profile"] == "smoke" and x["metrics"].get("errors") == 0 for x in task_approved
            )
            task_full = [
                x
                for x in task_approved
                if x["profile"] == "full"
                and x["metrics"].get("eligible", 0) > 0
                and x["metrics"].get("attempted") == x["metrics"].get("eligible")
            ]
            r["evidence_level"] = "primary_source"
            r["source_revision"] = dataset["revision"]
            r["source_revision_kind"] = "data source revision"
            r["openness"] = list(dict.fromkeys(r["openness"] + ["data_public"]))
            r["licenses"]["data"] = dataset.get("license") or "unverified"
            r["runtime"].update(
                adapter_implemented=True,
                smoke_tested=task_smoke,
                fully_evaluated=bool(task_full),
                blocked_reason=None,
                evaluated_scopes=[
                    {
                        "benchmark": sid,
                        "model": x["model_id"],
                        "requests": x["metrics"].get("eligible"),
                        "errors": x["metrics"].get("errors"),
                        "approval_release_id": x["approval_release_id"],
                    }
                    for x in task_full
                ],
            )
            r["links"].setdefault("docs", []).append(PUBLIC + "/blob/main/docs/evaluation.md")
            r["links"].setdefault("results", []).extend(
                PUBLIC + "/blob/main/" + x["source_path"] for x in task_full
            )
            tasks.append(
                {
                    "task_id": sid,
                    "resource_id": r["id"],
                    "adapter_implemented": True,
                    "smoke_tested": task_smoke,
                    "fully_evaluated": bool(task_full),
                }
            )
    for recipe in catalog.get("recipes", []):
        add(
            {
                "id": recipe["id"],
                "name": recipe["name"],
                "publisher": "JevZoo",
                "canonical_url": LAB + "/blob/main/" + recipe["config_path"],
                "resource_type": "recipe",
                "subtype": "lab_recipe",
                "description": recipe["description"],
                "purposes": recipe["purposes"],
                "tier": "featured",
                "evidence_level": "local_smoke",
                "verified_on": catalog["as_of"],
                "source_name": "Lab training documentation",
                "links": {
                    "docs": [LAB + "/blob/main/docs/training.md"],
                    "code": [LAB + "/blob/main/" + recipe["config_path"]],
                },
                "modalities": ["text"],
                "service_form": "lab_only",
                "openness": ["restricted_code"],
                "licenses": {
                    "code": "Apache-2.0 repository terms; Lab access required; training data has separate terms"
                },
                "limitations": recipe["limitations"],
                "related_ids": recipe["related_ids"],
                "runtime": {
                    "cataloged": True,
                    "source_verified": True,
                    "adapter_implemented": True,
                    "smoke_tested": True,
                    "fully_evaluated": False,
                    "blocked_reason": {
                        "en": "Formal training requires data audit and controlled experiments. Lab access required.",
                        "zh": "正式训练仍需数据审核与受控实验；此入口需要 Lab 权限。",
                    },
                    "evaluated_scopes": [],
                },
            }
        )
    by_id = {r["id"]: r for r in records.values()}
    for entry in (
        catalog["curated_resources"]
        + catalog["papers"]
        + catalog["benchmarks"]
        + catalog.get("recipes", [])
    ):
        for target in entry.get("related_ids", []):
            if target not in redirects:
                raise ValueError(
                    "Unresolved registry relationship: " + entry["id"] + " -> " + target
                )
    relationships = {
        "jeval-paper": [
            "innerjev",
            "asset-inner-4b-lora",
            "asset-inner-4b-full",
            "data-jeval",
            "data-typed-decisions",
        ],
        "visual-jev-paper": ["guanxuyu-sv/visual-jev", "qwen35-frozen", "data-mmstar"],
        "onejev": ["data-onejev-data", "checkpoint-onejev-08b", "checkpoint-onejev-4b"],
        "imajev": ["checkpoint-imajev-2b", "checkpoint-imajev-4b", "data-mmstar"],
        "qwen35-frozen": [
            "checkpoint-qwen35-2b",
            "checkpoint-qwen35-4b",
            "recipe-r1-language-lora",
            "recipe-r2-candidate-head",
        ],
        "hanno-decisionbench": ["data-decisionbench"],
        "strands-decider": ["asset-strands-current"],
        "pplx-decider": ["asset-pplx-v11"],
        "innerjev": ["asset-inner-4b-lora", "asset-inner-4b-full", "jeval-paper"],
        "intern-decision": ["asset-intern-4b"],
        "rsi-jev": ["asset-rsi4"],
        "llm2jev-paper": ["qwen35-frozen", "recipe-r1-language-lora", "asset-ci-qwen4b"],
    }
    for alias, related in relationships.items():
        target = by_id.get(redirects.get(alias, alias))
        if target:
            target["related_ids"] += related
    for r in records.values():
        related = [redirects.get(x, x) for x in r["related_ids"]]
        r["related_ids"] = list(dict.fromkeys(x for x in related if x in by_id and x != r["id"]))
    # Connect source references to canonical resources without conflating different assets.
    url_ids = {
        canonical(r.get("canonical_url")): r["id"]
        for r in records.values()
        if canonical(r.get("canonical_url"))
    }
    for r in records.values():
        for values in r["links"].values():
            for url in values:
                related = url_ids.get(canonical(url))
                if related and related != r["id"] and related not in r["related_ids"]:
                    r["related_ids"].append(related)
    for r in list(records.values()):
        for target in r["related_ids"]:
            if r["id"] not in by_id[target]["related_ids"]:
                by_id[target]["related_ids"].append(r["id"])
    for r in records.values():
        r["runtime"]["source_verified"] = r["evidence_level"] in ["primary_source", "local_smoke"]
    resources = sorted(
        records.values(), key=lambda r: (r["tier"] != "featured", r["name"].casefold())
    )
    visible = [r for r in resources if r["tier"] != "excluded"]
    stats = {
        "discovered": len(catalog["discovery_resources"]),
        "cataloged": len(visible),
        "by_type": dict(Counter(r["resource_type"] for r in visible)),
        "by_tier": dict(Counter(r["tier"] for r in resources)),
        "source_verified": sum(r["runtime"]["source_verified"] for r in visible),
        "link_checked_discovery": sum(
            r.get("link_status") == "reachable" for r in catalog["discovery_resources"]
        ),
        "discovery_failed": sum(
            r.get("link_status") != "reachable" for r in catalog["discovery_resources"]
        ),
        "adapter_checkpoints": len(deployed),
        "smoke_checkpoints": sum(d["runtime"]["smoke_tested"] for d in deployed),
        "evaluated_checkpoints_at_least_one_approved_scope": sum(
            d["runtime"]["fully_evaluated"] for d in deployed
        ),
        "implemented_tasks": len(tasks),
        "approved_full_summaries": sum(r["profile"] == "full" for r in approved),
        "formal_training_recipes": 0,
        "smoke_only_recipes": len(catalog.get("recipes", [])),
        "canonical_merges": sum(x["disposition"] == "merged_alias" for x in dispositions),
        "excluded_unbuilt_proposals": sum(x["disposition"] == "excluded" for x in dispositions),
    }
    return {
        "schema_version": "1.0",
        "locales": ["en", "zh"],
        "updated_on": catalog["site_contract"]["updated_on"],
        "upstream": {
            "repo": catalog["upstream"],
            "revision": catalog["upstream_revision"],
            "commit_date": catalog["upstream_commit_date"],
            "license": "MIT",
            "formal_categories": len({r["category"] for r in catalog["discovery_resources"]}),
            "active_repositories": sum(
                not r.get("upstream_removed_at_revision") for r in catalog["discovery_resources"]
            ),
        },
        "registry_sha256": digest(repo / "catalog/catalog.json"),
        "stats": stats,
        "resources": resources,
        "redirects": redirects,
        "deployed_models": deployed,
        "tasks": tasks,
        "approved_results": approved,
        "approval": approval,
        "unresolved_keywords": catalog["site_contract"]["unresolved_keywords"],
        "dispositions": dispositions,
    }


def labels(locale):
    return {
        "en": {
            "home": "Home",
            "catalog": "Explore",
            "platform": "Train & evaluate",
            "about": "About",
            "title": "Decision models. Connected.",
            "intro": "Find the models, papers and tools behind typed decisions. Explore the ecosystem, then move into reproducible evaluation and training.",
            "explore": "Explore resources",
            "run": "Open the platform",
            "featured": "A few good starting points",
            "featured_note": "Curated resources, with source evidence and an honest view of what runs.",
            "categories": "Find your next building block",
            "updates": "Recently verified",
            "two": "Explore broadly. Run deliberately.",
            "two_note": "A resource can be useful long before an adapter exists. Discovery, implementation and measurements are separate evidence.",
            "search": "Search resources, publishers or ideas…",
            "skip": "Skip to content",
            "types": "Resource types",
            "back": "Back to catalog",
            "what": "What it does",
            "why": "Why it belongs here",
            "start": "Start here",
            "limits": "What to keep in mind",
            "links": "Original sources",
            "related": "Keep exploring",
            "evidence": "Evidence & support",
            "open": "Components & access",
            "clear": "Clear filters",
            "unknown": "Not verified",
            "link_checked": "Link checked",
            "verified": "Primary source checked",
            "not_integrated": "Not integrated",
            "smoke": "Smoke tested",
            "evaluated": "Evaluated in a listed scope",
            "family": "Family / implementation",
            "checkpoint": "Checkpoint",
            "protocol": "Read the evaluation protocol",
            "approved": "Approved result summaries",
            "lab": "Lab training recipes",
            "noresults": "No matching resources",
            "reset": "Try another query or clear your filters.",
            "all": "All",
            "browse": "Browse",
            "count": "resources",
            "source": "Source",
            "published": "Paper publication / submission",
            "updated": "Source updated",
            "checked": "Verified on",
        },
        "zh": {
            "home": "首页",
            "catalog": "探索资源",
            "platform": "训练与评测",
            "about": "关于",
            "title": "发现决策模型，连接每一环。",
            "intro": "从模型、论文到工具，发现类型化决策的完整生态。了解资源，再进入可复现的评测与训练。",
            "explore": "探索资源目录",
            "run": "进入训练评测平台",
            "featured": "从这些资源开始",
            "featured_note": "精选资源、直接来源，以及清楚的运行支持状态。",
            "categories": "找到下一块构建模块",
            "updates": "最近核验",
            "two": "广泛发现，逐步验证。",
            "two_note": "资源可以先展示，再接入运行。目录收录、实现状态与实际测量分别记录。",
            "search": "搜索名称、发布者或关键词…",
            "skip": "跳到主要内容",
            "types": "资源类型",
            "back": "返回资源目录",
            "what": "它能做什么",
            "why": "为什么与 JEV 相关",
            "start": "从这里开始",
            "limits": "使用前需要了解",
            "links": "原始来源",
            "related": "继续探索关联资源",
            "evidence": "证据与运行支持",
            "open": "组件与开放状态",
            "clear": "清除筛选",
            "unknown": "尚未核验",
            "link_checked": "链接已检查",
            "verified": "一手来源已核验",
            "not_integrated": "尚未接入",
            "smoke": "Smoke 已通过",
            "evaluated": "已在列明范围评测",
            "family": "系列 / 实现",
            "checkpoint": "Checkpoint",
            "protocol": "查看评测协议",
            "approved": "已批准的结果摘要",
            "lab": "Lab 训练配方",
            "noresults": "没有匹配的资源",
            "reset": "尝试其他关键词或清除筛选。",
            "all": "全部",
            "browse": "浏览",
            "count": "项资源",
            "source": "来源",
            "published": "论文发表 / 提交",
            "updated": "来源更新",
            "checked": "核验日期",
        },
    }[locale]


def resource_badge(r, locale):
    t = labels(locale)
    state = r["runtime"]
    if state["fully_evaluated"]:
        return '<span class="badge verified">' + t["evaluated"] + "</span>"
    if state["smoke_tested"]:
        return '<span class="badge verified">' + t["smoke"] + "</span>"
    if r["evidence_level"] == "primary_source":
        return '<span class="badge">' + t["verified"] + "</span>"
    return (
        '<span class="badge muted">'
        + (t["link_checked"] if r["evidence_level"] == "link_checked" else t["unknown"])
        + "</span>"
    )


def resource_card(r, locale, base="", compact=False):
    title = TYPE_LABELS[r["resource_type"]][locale == "zh"]
    uses = " · ".join(USE_LABELS.get(x, (x, x))[locale == "zh"] for x in r["purposes"][:2])
    return f'<article class="resource-row"><div class="resource-symbol" aria-hidden="true">{h(r["name"][:1].upper())}</div><div class="resource-body"><div class="resource-meta">{h(title)} <span>·</span> {h(r["publisher"])}</div><h3><a href="{base}resources/{r["slug"]}/">{h(r["name"])}</a></h3><p>{h(tr(r, "description", locale))}</p><div class="resource-foot">{resource_badge(r, locale)}<span>{h(uses)}</span></div></div><a class="row-arrow" href="{base}resources/{r["slug"]}/" aria-label="{h(r["name"])}">↗</a></article>'


def shell(locale, section, content, depth=0, title=None, other_path=None):
    t = labels(locale)
    base = "../" * depth
    root = base + "../"
    other = "zh" if locale == "en" else "en"
    nav = "".join(
        f'<a href="{base}{path}" '
        + ('aria-current="page"' if section == key else "")
        + f">{t[key]}</a>"
        for key, path in [("catalog", "catalog/"), ("platform", "platform/"), ("about", "about/")]
    )
    return f'''<!doctype html><html lang="{"zh-Hans" if locale == "zh" else "en"}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{h(t["intro"])}"><title>{h(title or t["title"])} · JevZoo</title><link rel="icon" href="{root}assets/favicon.svg"><link rel="stylesheet" href="{root}assets/styles.css"><script type="module" src="{root}assets/app.js"></script></head><body data-locale="{locale}" data-page="{section}" data-catalog-url="{root}assets/catalog.json" data-base="{base}"><a class="skip-link" href="#main">{t["skip"]}</a><header class="site-header"><div class="header-inner"><a class="brand" href="{base}" aria-label="JevZoo {t["home"]}"><span class="brand-mark" aria-hidden="true">j<span>z</span></span>JevZoo<span class="brand-note">{"决策生态" if locale == "zh" else "decision ecosystem"}</span></a><button class="menu-toggle" aria-label="{"导航菜单" if locale == "zh" else "Navigation menu"}" aria-expanded="false">☰</button><nav class="main-nav" aria-label="{"主导航" if locale == "zh" else "Main navigation"}">{nav}<a class="language-switch" href="{root}{other}/{other_path or ""}" data-language-switch lang="{other}">{"EN" if locale == "zh" else "中文"}</a><a class="github-link" href="{PUBLIC}" target="_blank" rel="noopener noreferrer">GitHub ↗</a></nav></div></header><main id="main">{content}</main><footer class="site-footer"><div><a class="brand" href="{base}">JevZoo</a><p>{"资源展示与发现 + 可复现训练评测。" if locale == "zh" else "Resource discovery + reproducible training and evaluation."}</p></div><div><a href="{base}about/">{"来源与维护" if locale == "zh" else "Sources & maintenance"}</a><a href="{PUBLIC}/blob/main/NOTICE" target="_blank" rel="noopener noreferrer">{"许可与署名" if locale == "zh" else "Licenses & attribution"}</a><span>{"独立社区项目。收录不代表可运行。" if locale == "zh" else "Independent community project. Listed does not mean runnable."}</span></div></footer></body></html>'''


def home(data, locale):
    t = labels(locale)
    stats = data["stats"]
    featured = [
        r
        for r in data["resources"]
        if set(r["source_record_ids"])
        & {"clef-flash", "onejev", "imajev", "llm2jev-paper", "jeval-paper", "vllm"}
    ][:6]
    if len(featured) < 6:
        featured += [r for r in data["resources"] if r["tier"] == "featured" and r not in featured][
            : 6 - len(featured)
        ]
    categories = [
        (
            "model",
            "Models",
            "模型",
            "Open checkpoints, model families and decision readouts.",
            "开放 checkpoint、模型系列与决策读出。",
        ),
        (
            "paper",
            "Papers",
            "论文",
            "Methods, evidence and the questions still open.",
            "方法、证据与仍待回答的问题。",
        ),
        (
            "tools",
            "Tools",
            "工具",
            "SDKs, runtimes, training and evaluation frameworks.",
            "SDK、运行时、训练与评测框架。",
        ),
        (
            "data",
            "Benchmarks & data",
            "基准与数据",
            "Protocols, reference labels and training assets.",
            "协议、参考标签与训练资产。",
        ),
        (
            "application",
            "Applications",
            "应用",
            "Agents, browser use, memory, demos and games.",
            "Agent、浏览器操作、记忆、演示与游戏。",
        ),
    ]
    tiles = ""
    for key, en, zh, den, dzh in categories:
        count = sum(
            stats["by_type"].get(k, 0)
            for k in (
                ["tool", "framework"]
                if key == "tools"
                else ["benchmark", "dataset"]
                if key == "data"
                else [key]
            )
        )
        tiles += f'<a class="category-tile" href="catalog/?type={key}"><span class="tile-icon" aria-hidden="true">{dict(model="◈", paper="▤", tools="⌘", data="▦", application="↗")[key]}</span><h3>{zh if locale == "zh" else en} <span>↗</span></h3><p>{dzh if locale == "zh" else den}</p><strong>{count} <small>{t["count"]}</small></strong></a>'
    recent = [
        r
        for r in data["resources"]
        if r["id"] in ["asset-pplx-v11", "asset-d3-mini", "asset-inner-4b-lora"]
    ]
    update = "".join(
        f'<a class="update-row" href="resources/{r["slug"]}/"><span>{h(r.get("verified_on") or data["updated_on"])}</span><div><strong>{h(r["name"])}</strong><p>{h(tr(r, "description", locale))}</p></div><span>↗</span></a>'
        for r in recent
    )
    flow_labels = (
        ["Paper", "Code", "Model", "Data", "Recipe", "Result"]
        if locale == "en"
        else ["论文", "代码", "模型", "数据", "配方", "结果"]
    )
    return f'''<section class="hero wrap"><div class="hero-copy"><h1>{t["title"]}</h1><p>{t["intro"]}</p><div class="hero-actions"><a class="button primary" href="catalog/">{t["explore"]} <span>↗</span></a><a class="button secondary" href="platform/">{t["run"]} →</a></div><form class="hero-search" action="catalog/"><label class="sr-only" for="home-search">{t["search"]}</label><span aria-hidden="true">⌕</span><input type="search" id="home-search" name="q" placeholder="{t["search"]}"><button aria-label="{"搜索" if locale == "zh" else "Search"}">→</button></form><p class="hero-note">{"中英文同步 · 一项资源，一个 canonical 身份。" if locale == "zh" else "English + 中文. One canonical identity for every resource."}</p></div><div class="ecosystem-panel"><div class="ecosystem-title"><span class="live-dot"></span>{"从发现到验证" if locale == "zh" else "From discovery to evidence"}</div><div class="asset-flow">{"".join(f"<span>{x}</span>" for x in flow_labels)}</div><div class="ecosystem-bottom"><span>{"共享状态，清晰决策。" if locale == "zh" else "Shared state. Explicit decisions."}</span><code>Choice · Boolean · Score</code></div><div class="ecosystem-line"></div><div class="mini-status"><span>{"资源有来源" if locale == "zh" else "Sources attached"}</span><span>{"运行有证据" if locale == "zh" else "Runs have evidence"}</span></div></div></section><section class="stats-strip wrap"><div><strong>{stats["cataloged"]:,}</strong><span>{"目录资源" if locale == "zh" else "catalog resources"}</span></div><div><strong>{stats["by_type"].get("paper", 0)}</strong><span>{"论文与方法" if locale == "zh" else "papers & methods"}</span></div><div><strong>{stats["adapter_checkpoints"]}</strong><span>{"已接入 checkpoint" if locale == "zh" else "implemented checkpoints"}</span></div><div><strong>{stats["implemented_tasks"]}</strong><span>{"已实现评测任务" if locale == "zh" else "implemented tasks"}</span></div><a href="about/">{"查看统计口径 →" if locale == "zh" else "How we count →"}</a></section><section class="section wrap"><div class="section-heading"><div><h2>{t["categories"]}</h2><p>{"按资源类型进入，再按用途深入查找。" if locale == "zh" else "Start with a resource type, then narrow by what you need."}</p></div><a href="catalog/">{t["all"]} →</a></div><div class="category-grid">{tiles}</div></section><section class="section wrap"><div class="section-heading"><div><h2>{t["featured"]}</h2><p>{t["featured_note"]}</p></div><a href="catalog/?tier=featured">{"全部精选 →" if locale == "zh" else "All curated →"}</a></div><div class="featured-grid">{"".join(resource_card(r, locale) for r in featured)}</div></section><section class="platform-banner wrap"><div><span class="section-label">{"训练与评测" if locale == "zh" else "TRAIN & EVALUATE"}</span><h2>{t["two"]}</h2><p>{t["two_note"]}</p><a class="button primary" href="platform/">{t["run"]} →</a></div><div class="platform-mini"><div><span>01</span><strong>{"推理与评测" if locale == "zh" else "Inference & evaluation"}</strong><small>{stats["adapter_checkpoints"]} checkpoints · {stats["implemented_tasks"]} tasks</small></div><div><span>02</span><strong>{"训练与校准" if locale == "zh" else "Training & calibration"}</strong><small>{"Lab smoke 已验证；正式训练待完成" if locale == "zh" else "Lab smoke verified; formal training pending"}</small></div><div><span>03</span><strong>{"已批准的结果" if locale == "zh" else "Approved scoped results"}</strong><small>{stats["approved_full_summaries"]} {"份全量公开集摘要" if locale == "zh" else "full-public summaries"}</small></div></div></section><section class="section wrap"><div class="section-heading"><div><h2>{t["updates"]}</h2><p>{"官方更新与核验日期，不冒充模型发布时间。" if locale == "zh" else "Official updates, with verification dates rather than invented release dates."}</p></div><a href="catalog/?sort=verified">{"继续浏览 →" if locale == "zh" else "Keep browsing →"}</a></div>{update}</section>'''


def catalog_page(data, locale):
    t = labels(locale)
    options = "".join(
        f'<option value="{key}">{value[locale == "zh"]}</option>'
        for key, value in USE_LABELS.items()
    )
    types = "".join(
        f'<button class="type-filter" data-type="{key}" type="button"><span>{value[locale == "zh"]}</span><small>{data["stats"]["by_type"].get(key, 0)}</small></button>'
        for key, value in TYPE_LABELS.items()
    )
    names = {
        "modality": ("Modality", "模态"),
        "openness": ("Component access", "组件开放状态"),
        "form": ("Delivery", "服务形态"),
        "evidence": ("Evidence", "核验程度"),
        "runtime": ("JevZoo support", "JevZoo 运行支持"),
        "tier": ("Selection", "收录分层"),
    }
    values = {
        "modality": [
            ("text", "Text", "文本"),
            ("image", "Image", "图像"),
            ("video", "Video", "视频"),
            ("audio", "Audio", "音频"),
            ("unknown", "Not verified", "未核验"),
        ],
        "openness": [
            ("code_open", "Open code", "开源代码"),
            ("weights_open", "Open weights", "开放权重"),
            ("data_public", "Public data", "公开数据"),
            ("closed_api", "Closed API", "闭源 API"),
            ("public_paper", "Public paper", "公开论文"),
            ("unknown", "Not verified", "未核验"),
            ("restricted_code", "Restricted code (Lab)", "受限代码（Lab）"),
        ],
        "form": [
            ("repository", "Repository", "代码仓库"),
            ("download", "Downloadable asset", "可下载资产"),
            ("hosted_api", "Hosted API", "托管 API"),
            ("managed_platform", "Managed platform", "商业平台"),
            ("lab_only", "Lab only", "仅 Lab"),
        ],
        "evidence": [
            ("primary_source", "Primary source", "一手来源"),
            ("link_checked", "Link checked only", "仅链接核验"),
            ("unverified", "Needs verification", "待核验"),
            ("local_smoke", "Local smoke evidence", "本地 smoke 证据"),
        ],
        "runtime": [
            ("implemented", "Implemented", "已接入"),
            ("smoke", "Smoke tested", "Smoke 通过"),
            ("evaluated", "Evaluated, scoped", "已评测，范围明确"),
            ("unimplemented", "Not integrated", "尚未接入"),
        ],
        "tier": [
            ("featured", "Curated", "重点精选"),
            ("broad", "Broad directory", "广覆盖目录"),
            ("review", "Needs review / invalid", "待核验 / 失效"),
        ],
    }
    advanced = "".join(
        f'<label>{names[key][locale == "zh"]}<select data-filter="{key}" id="filter-{key}"><option value="">{t["all"]}</option>'
        + "".join(
            f'<option value="{v}">{zh if locale == "zh" else en}</option>'
            for v, en, zh in values[key]
        )
        + "</select></label>"
        for key in names
    )
    return f'''<section class="catalog-heading wrap"><h1>{"探索 JEV 的完整生态。" if locale == "zh" else "Explore the decision ecosystem."}</h1><p>{"按用途发现资源，按证据判断支持状态。" if locale == "zh" else "Find by purpose. Decide with evidence."}</p></section><div class="catalog-layout wrap"><aside class="filter-rail"><button class="filter-mobile-toggle" aria-expanded="false">{"筛选与分类" if locale == "zh" else "Filters & categories"} ▾</button><div class="filter-content"><h2>{t["types"]}</h2><button class="type-filter active" data-type="" type="button"><span>{t["all"]}</span><small>{data["stats"]["cataloged"]}</small></button>{types}<label class="purpose-filter">{"使用目的" if locale == "zh" else "Use case"}<select data-filter="use" id="filter-use"><option value="">{t["all"]}</option>{options}</select></label><details class="advanced-filters"><summary>{"更多筛选" if locale == "zh" else "More filters"}</summary>{advanced}</details><button class="clear-filters" type="button">{t["clear"]} ↺</button><p class="filter-hint">{"一个资源可以有多个用途；运行状态独立核验。" if locale == "zh" else "Resources can serve many purposes. Runtime support is verified separately."}</p></div></aside><section class="catalog-results"><div class="catalog-toolbar"><label class="search-control" for="catalog-search"><span aria-hidden="true">⌕</span><input id="catalog-search" type="search" placeholder="{t["search"]}" autocomplete="off"><kbd>/</kbd></label><label class="sort-control"><span class="sr-only">{"排序" if locale == "zh" else "Sort"}</span><select id="sort"><option value="relevance">{"精选优先" if locale == "zh" else "Curated first"}</option><option value="name">{"名称 A–Z" if locale == "zh" else "Name A–Z"}</option><option value="verified">{"最近核验" if locale == "zh" else "Recently verified"}</option></select></label></div><div class="result-status"><p id="result-count" role="status" aria-live="polite">{data["stats"]["cataloged"]} {t["count"]}</p><button class="share-button" type="button">{"复制浏览链接" if locale == "zh" else "Copy view link"} ↗</button></div><div id="active-filters" class="active-filters"></div><div id="resource-list">{"".join(resource_card(r, locale, "../") for r in data["resources"][:24] if r["tier"] != "excluded")}</div><div id="empty-state" class="empty-state" hidden><span aria-hidden="true">⌕</span><h2>{t["noresults"]}</h2><p>{t["reset"]}</p><button class="button secondary clear-filters">{t["clear"]}</button></div><nav id="pagination" class="pagination" aria-label="{"目录分页" if locale == "zh" else "Catalog pages"}"></nav><noscript><p>JavaScript is needed for filtering. Static resource pages remain readable.</p></noscript></section></div>'''


def detail(data, r, locale):
    t = labels(locale)
    related = {x["id"]: x for x in data["resources"]}
    state = r["runtime"]
    kind_names = {
        "paper": ("Paper", "论文"),
        "code": ("Code", "代码"),
        "weights": ("Weights", "权重"),
        "data": ("Data", "数据"),
        "docs": ("Docs", "文档"),
        "demo": ("Demo", "演示"),
        "results": ("Results", "结果"),
    }
    links = "".join(
        f'<a class="source-link" href="{h(url)}" target="_blank" rel="noopener noreferrer"><span>{kind_names.get(key, (key, key))[locale == "zh"]}</span><strong>{h(url.replace("https://", "")[:105])}</strong><span>↗</span></a>'
        for key, urls in r["links"].items()
        for url in urls
    )
    evidence_flags = [
        ("cataloged", "Cataloged", "已收录"),
        ("source_verified", "Primary source verified", "一手来源核验"),
        ("adapter_implemented", "JevZoo adapter implemented", "JevZoo 已实现接入"),
        ("smoke_tested", "Real smoke tested", "真实 smoke 通过"),
        ("fully_evaluated", "Full evaluation in listed scope", "列明范围的全量评测"),
    ]
    flags = "".join(
        f'<li><span class="state-dot {"yes" if state.get(key) else "no"}" aria-hidden="true"></span><span>{zh if locale == "zh" else en}</span><strong>{("是" if locale == "zh" else "Yes") if state.get(key) else ("未建立证据" if locale == "zh" else "No evidence")}</strong></li>'
        for key, en, zh in evidence_flags
    )
    scope = "".join(
        f'<p class="scope-note">{h(s["benchmark"] + (" · " + s["model"] if s.get("model") else ""))} · {s["requests"]} requests · {s["errors"]} errors</p>'
        for s in state.get("evaluated_scopes", [])
    )
    if state.get("blocked_reason"):
        scope += f'<p class="scope-note">{h(tr(state, "blocked_reason", locale))}</p>'
    license_rows = "".join(
        f"<div><dt>{h(key)}</dt><dd>{h(json.dumps(value, ensure_ascii=False) if isinstance(value, list) else value)}</dd></div>"
        for key, value in r["licenses"].items()
    )
    date_fields = (
        [(t["published"], "publication_date")]
        if r["resource_type"] == "paper"
        else [(("模型发布日期" if locale == "zh" else "Model release date"), "model_release_date")]
        if r["resource_type"] == "model"
        else []
    )
    if r.get("created_on"):
        date_fields.append(
            (
                "HF 仓库创建（不是模型发布日期）"
                if locale == "zh"
                else "HF repository created (not model release)",
                "created_on",
            )
        )
    date_fields += [(t["updated"], "updated_on"), (t["checked"], "verified_on")]
    date_rows = "".join(
        f"<div><dt>{h(label)}</dt><dd>{h(r.get(field) or t['unknown'])}</dd></div>"
        for label, field in date_fields
    )
    modality_names = {
        "text": ("Text", "文本"),
        "image": ("Image", "图像"),
        "video": ("Video", "视频"),
        "audio": ("Audio", "音频"),
        "unknown": ("Not verified", "未核验"),
    }
    facts = (
        '<dl class="metadata-list"><div><dt>'
        + (
            "上游声明模态（实测见范围）"
            if locale == "zh"
            else "Declared modality (tested scope separately)"
        )
        + "</dt><dd>"
        + h(
            " · ".join(modality_names.get(x, (x, x))[locale == "zh"] for x in r["modalities"])
            or t["unknown"]
        )
        + "</dd></div>"
    )
    if r["resource_type"] == "model":
        for key, en, zh in [
            ("base_model", "Base model", "基座"),
            ("parameter_scale_label", "Scale / checkpoint label", "规模 / checkpoint 标签"),
        ]:
            facts += (
                "<div><dt>"
                + (zh if locale == "zh" else en)
                + "</dt><dd>"
                + h(r.get("asset_metadata", {}).get(key) or t["unknown"])
                + "</dd></div>"
            )
    facts += "</dl>"
    cards = "".join(
        resource_card(related[x], locale, "../../") for x in r["related_ids"][:12] if x in related
    )
    return f"""<section class="detail-heading wrap"><a class="back-link" href="../../catalog/">← {t["back"]}</a><div class="resource-meta">{TYPE_LABELS[r["resource_type"]][locale == "zh"]} · {h(r["publisher"])}</div><h1>{h(r["name"])}</h1><p>{h(tr(r, "description", locale))}</p><div class="detail-actions">{resource_badge(r, locale)}<span class="badge muted">{h(t["checkpoint"] if r["subtype"] == "checkpoint" else t["family"] if r["resource_type"] == "model" else FORM_LABELS.get(r["service_form"], (r["service_form"], r["service_form"]))[locale == "zh"])}</span>{'<a class="button small primary" href="../../platform/#' + h(state.get("deployment_id", "")) + '">' + t["platform"] + " →</a>" if state["adapter_implemented"] else ""}</div></section><div class="detail-layout wrap"><div><section class="detail-section"><h2>{t["what"]}</h2><p>{h(tr(r, "description", locale))}</p><h3>{t["why"]}</h3><p>{h(" · ".join(USE_LABELS.get(x, (x, x))[locale == "zh"] for x in r["purposes"]))}</p><h3>{t["start"]}</h3><p>{"先查看下方一手入口和组件许可；已有 JevZoo 接入时，可在训练评测页选择对应任务。" if locale == "zh" else "Start with the original sources and component terms below. For integrated models, choose a task on the platform page."}</p></section><section class="detail-section"><h2>{t["links"]}</h2>{links or "<p>" + t["unknown"] + "</p>"}</section><section class="detail-section limit-section"><h2>{t["limits"]}</h2><p>{h(tr(r, "limitations", locale))}</p><p>{"商业推理未执行。资源收录不代表免费、开源权重或适用于所有任务。" if locale == "zh" else "Commercial inference is not run. Catalog inclusion does not imply free access, open weights or suitability for every task."}</p></section><section class="detail-section"><h2>{t["related"]}</h2><div class="related-list">{cards or "<p>" + ("暂无经过确认的关联；可从目录按用途继续查找。" if locale == "zh" else "No verified asset link yet. Continue by use case in the catalog.") + "</p>"}</div></section></div><aside class="evidence-rail"><section><h2>{t["evidence"]}</h2><ul class="support-states">{flags}</ul>{scope}<p class="evidence-note">{"全量只代表列明划分，包含错误分母；不等于所有任务通过。" if locale == "zh" else "Full evaluation means the named split, including error denominators. It does not mean every task passed."}</p></section><section><h2>{t["open"]}</h2>{facts}<div class="tag-list">{"".join('<span class="badge muted">' + h(OPEN_LABELS.get(x, (x, x))[locale == "zh"]) + "</span>" for x in r["openness"])}</div><dl class="metadata-list">{license_rows}</dl></section><section><h2>{"来源记录" if locale == "zh" else "Provenance"}</h2><dl class="metadata-list">{date_rows}<div><dt>{"版本" if locale == "zh" else "Revision"}</dt><dd class="mono">{h((r.get("source_revision_kind", "") + " · " if r.get("source_revision_kind") else "") + (r.get("source_revision") or t["unknown"]))}</dd></div></dl><details><summary>{"别名与来源身份" if locale == "zh" else "Aliases & source identities"}</summary><p>{h(", ".join(r["aliases"]) or "—")}</p><p>{h(", ".join(r["source_record_ids"]))}</p></details></section></aside></div>"""


def platform(data, locale):
    t = labels(locale)
    resources = {r["id"]: r for r in data["resources"]}
    zh = locale == "zh"
    models = "".join(
        f'<tr id="{h(m["deployment_id"])}"><td><a href="../resources/{resources[m["resource_id"]]["slug"]}/">{h(resources[m["resource_id"]]["name"])}</a><small>{h(m["backend"])}</small></td><td>{"✓" if m["runtime"]["smoke_tested"] else "—"}</td><td>{h(", ".join(s["benchmark"] for s in m["runtime"]["evaluated_scopes"]) or ("未建立" if zh else "Pending"))}</td><td class="mono">{m["checkpoint_revision"][:12]}</td></tr>'
        for m in data["deployed_models"]
    )
    tasks = "".join(
        f'<a class="task-link" href="../resources/{resources[x["resource_id"]]["slug"]}/"><strong>{h(x["task_id"])}</strong><span>{"已实现 importer" if zh else "Importer implemented"}</span><span>↗</span></a>'
        for x in data["tasks"]
    )
    results = "".join(
        f'<tr><td>{h(x["model_id"])}</td><td>{h(x["benchmark_id"])}</td><td>{x["metrics"].get("attempted")} / {x["metrics"].get("eligible")}</td><td>{x["metrics"].get("errors")}</td><td>{format_accuracy(x["metrics"].get("accuracy_including_errors"))}</td><td><a href="{PUBLIC}/blob/main/{x["source_path"]}" target="_blank" rel="noopener noreferrer">JSON ↗</a></td></tr>'
        for x in data["approved_results"]
        if x["profile"] == "full"
    )
    recipes = "".join(
        resource_card(r, locale, "../") for r in data["resources"] if r["resource_type"] == "recipe"
    )
    code = "python -m pip install '.[eval]'\nexport JEVZOO_WORKSPACE=/absolute/path/outside/git\njevzoo evaluate --deployment qwen35-4b --suite jevbench-public --profile smoke\njevzoo report --run /absolute/path/to/run"
    return f'''<section class="page-heading wrap"><h1>{"发现之后，开始验证。" if zh else "From discovery to reproducible runs."}</h1><p>{"同一资源身份，连接模型、数据、任务与证据。此页面提供入口，不在浏览器执行 GPU 任务。" if zh else "The same resource identities connect models, data, tasks and evidence. This page opens workflows; it does not launch GPU jobs."}</p></section><div class="platform-content wrap"><div class="platform-notice">{("已接入 " + str(data["stats"]["adapter_checkpoints"]) + " 个 checkpoint，已实现 " + str(data["stats"]["implemented_tasks"]) + " 个任务。正式训练配方验证尚未完成。") if zh else f"{data['stats']['adapter_checkpoints']} implemented checkpoints, {data['stats']['implemented_tasks']} implemented tasks. Formal training recipe validation is pending."}</div><section class="detail-section"><div class="section-heading"><h2>{"运行入口" if zh else "Start a local evaluation"}</h2><a href="{PUBLIC}/blob/main/docs/evaluation.md" target="_blank" rel="noopener noreferrer">{t["protocol"]} ↗</a></div><div class="code-panel"><button class="copy-code" type="button">{"复制命令" if zh else "Copy commands"}</button><pre><code>{h(code)}</code></pre></div><p>{"命令需要本地环境与仓外资产。目录展示不会启动下载或运行；商业 API 当前禁用。" if zh else "Commands require a local environment and external assets. Browsing never triggers downloads or execution; commercial APIs remain disabled."}</p></section><section class="detail-section"><h2>{"已接入的 checkpoint" if zh else "Implemented checkpoints"}</h2><p>{"Smoke 与全量证据按 checkpoint、基准和版本分别核验；不是所有基准完成声明。" if zh else "Smoke and full evidence are scoped by checkpoint, benchmark and revision; these are not all-benchmark completion claims."}</p><div class="table-scroll"><table><thead><tr><th>Checkpoint</th><th>Smoke</th><th>{"已批准全量范围" if zh else "Approved full scope"}</th><th>Revision</th></tr></thead><tbody>{models}</tbody></table></div></section><section class="detail-section"><h2>{"任务与数据入口" if zh else "Tasks and data"}</h2><div class="task-grid">{tasks}</div></section><section class="detail-section"><h2>{t["lab"]}</h2><p>{"语言 LoRA 与 candidate head 已有真实梯度 / 重载 smoke，尚无正式训练收益结论。校准数据必须独立。完整训练实现保留在私有 Lab。" if zh else "Language LoRA and a candidate head have real-gradient/reload smoke evidence, not formal training-gain results. Calibration needs an independent fold. Full training code remains in the private Lab."}</p><div class="featured-grid">{recipes}</div><a href="{LAB}/blob/main/docs/training.md" target="_blank" rel="noopener noreferrer">{"Lab 训练与校准说明（需权限）" if zh else "Lab training & calibration guide (access required)"} ↗</a></section><section class="detail-section" id="results"><h2>{t["approved"]}</h2><p>{"只展示与具体已批准 release hash 匹配的摘要。JevBench public 不是封存题或完整官方 composite。以下为不同模型自有协议的记录，非同训练预算排名。" if zh else "Only summaries matching an exact approved release hash are shown. JevBench public is not the sealed suite or official composite. These are model-specific protocol records, not a matched-training leaderboard."}</p><div class="table-scroll"><table><thead><tr><th>Model</th><th>Benchmark</th><th>Attempts</th><th>Errors</th><th>Accuracy*</th><th>Source</th></tr></thead><tbody>{results or '<tr><td colspan="6">' + ("暂无符合批准 hash 的全量摘要。" if zh else "No full summaries match an approved hash.") + "</td></tr>"}</tbody></table></div><small>* {"含错误分母的 argmax accuracy。概率与官方指标见对应 JSON，协议不同不混排。" if zh else "Argmax accuracy including error denominators. Probability/official metrics and protocol differences are in each JSON."}</small></section></div>'''


def about(data, locale):
    zh = locale == "zh"
    s = data["stats"]
    types = "".join(
        f"<tr><td>{TYPE_LABELS[k][zh]}</td><td>{v}</td></tr>"
        for k, v in sorted(s["by_type"].items())
    )
    tiers = "".join(
        f"<tr><td>{dict(featured=('Curated', '重点精选'), broad=('Broad directory', '广覆盖目录'), review=('Needs review', '待核验 / 失效'))[k][zh]}</td><td>{v}</td></tr>"
        for k, v in s["by_tier"].items()
    )
    return f'''<section class="page-heading wrap"><h1>{"有来源的目录，有证据的平台。" if zh else "A sourced catalog. An evidenced platform."}</h1><p>{"JevZoo 是独立社区项目：资源展示与发现、可执行训练评测两条线同步建设。" if zh else "JevZoo is an independent community project developing resource discovery and executable training/evaluation together."}</p></section><div class="about-content wrap"><section class="detail-section"><h2>{"如何收录与核验" if zh else "Inclusion and evidence"}</h2><p>{"重点精选直接帮助模型使用、训练、评测与典型应用。广覆盖目录保留用途明确的工程和应用；链接失效或身份不清进入待核验层。明显重复进行 canonical 合并，原发现记录与理由不删除。" if zh else "Curated resources directly help model use, training, evaluation and representative applications. The broad directory retains useful engineering and applications; invalid or unresolved sources stay in a review lane. Canonical duplicates are merged without deleting discovery evidence or reasons."}</p><p>{"链接可达、一手能力声明、loader 可见、真实 smoke 与正式全量是不同证据。免费、开源代码、开放权重、公开数据与商业托管分别记录。" if zh else "Reachable links, primary capability claims, visible loaders, real smoke and full evaluations are different evidence. Free access, open code, open weights, public data and hosted services are recorded separately."}</p></section><section class="detail-section"><h2>{"数量与范围" if zh else "Counts and scope"}</h2><div class="about-tables"><table><thead><tr><th>{"主要类型" if zh else "Primary type"}</th><th>Count</th></tr></thead><tbody>{types}</tbody></table><div><table><thead><tr><th>{"收录层次" if zh else "Selection tier"}</th><th>Count</th></tr></thead><tbody>{tiers}</tbody></table><p>{s["discovered"]} discovery records · {s["cataloged"]} canonical resources · {s["canonical_merges"]} merged aliases · {s["excluded_unbuilt_proposals"]} unbuilt proposals excluded.</p></div></div><p>{s["source_verified"]} {"个资源有一手来源或本地配方证据；运行接入为" if zh else "resources have primary-source or local-recipe evidence; runtime integration covers"} {s["adapter_checkpoints"]} checkpoints. {s["approved_full_summaries"]} {"份已批准全量摘要仅限其注明范围。" if zh else "approved full summaries are scoped to their named datasets."}</p></section><section class="detail-section"><h2>{"发现源与版本" if zh else "Discovery source and version"}</h2><p><a href="https://github.com/{data["upstream"]["repo"]}/tree/{data["upstream"]["revision"]}" target="_blank" rel="noopener noreferrer">{h(data["upstream"]["repo"])} ↗</a> · MIT</p><dl class="metadata-list"><div><dt>Commit</dt><dd class="mono">{data["upstream"]["revision"]}</dd></div><div><dt>Commit date (UTC)</dt><dd>{data["upstream"]["commit_date"]}</dd></div><div><dt>{"目录核验日期" if zh else "Catalog verification date"}</dt><dd>{data["updated_on"]}</dd></div></dl><p>{f"原快照的 {data['upstream']['formal_categories']} 个正式分类含 {data['upstream']['active_repositories']} 个唯一 GitHub 仓库；文末另 3 条代码参考不计入。JevZoo 的 canonical 计数还包含独立论文、模型/data/recipe 资产，不能称为已支持模型数量。" if zh else f"The original snapshot has {data['upstream']['active_repositories']} unique GitHub repositories in {data['upstream']['formal_categories']} formal categories; three trailing code references are excluded. JevZoo additionally links independent paper, model, data and recipe assets; its canonical total is not a supported-model count."}</p></section><section class="detail-section"><h2>{"维护、更新与许可" if zh else "Maintenance, updates and licenses"}</h2><p>{"网站与中英文 README 从现有注册表生成。数据变更后重建，并校验 canonical/alias、关联 ID、语言一致性与批准摘要 hash。作者成绩、外部测量、JevZoo 实测不互换。公开发布仍需要批准具体 release 与文件 hash。" if zh else "The site and both READMEs are generated from the existing registry. Rebuild after metadata changes; validate canonical aliases, relationships, locale parity and approved-summary hashes. Author reports, external measurements and JevZoo runs are not interchangeable. Publication still needs approval of the exact release and file hashes."}</p><p>ETHACC — {"待消歧关键词，未推测含义；不影响其他分类继续建设。" if zh else "an unresolved keyword retained without guessing; other categories continue normally."}</p><a href="{PUBLIC}/blob/main/NOTICE" target="_blank" rel="noopener noreferrer">{"来源署名与 NOTICE" if zh else "Attribution and NOTICE"} ↗</a></section></div>'''


def readmes(data, repo):
    for locale, name in [("en", "README.md"), ("zh", "README_zh.md")]:
        zh = locale == "zh"
        s = data["stats"]
        other = "README.md" if zh else "README_zh.md"
        language = "English" if zh else "简体中文"
        lines = [
            "# JevZoo",
            "",
            f"[{language}]({other}) · [GitHub]({PUBLIC})",
            "",
            (
                "资源展示与发现平台 + 可执行、可复现的推理、评测、训练与校准平台。"
                if zh
                else "Resource discovery + executable, reproducible inference, evaluation, training and calibration."
            ),
            "",
            (
                "资源可以先展示，再逐步适配。收录、一手核验、接入、smoke 与全量评测分别记录。"
                if zh
                else "Resources can be listed before integration. Catalog inclusion, primary-source review, implementation, smoke and full evaluation are separate evidence."
            ),
            "",
            ("## 浏览主页" if zh else "## Browse the site"),
            " ",
            (
                "中英文主页、可分享的搜索筛选、资源详情、关联资产与训练评测入口均由现有注册表生成。"
                if zh
                else "English and Chinese homepages, shareable search/filter views, resource details, related assets and platform routes are generated from the existing registry."
            ),
            "",
            "```bash",
            "python site/build.py --output /absolute/path/outside/git/jevzoo-site --readmes",
            "python -m http.server 8766 --bind 127.0.0.1 --directory /absolute/path/outside/git/jevzoo-site",
            "```",
            "",
            "`http://127.0.0.1:8766/en/` · `http://127.0.0.1:8766/zh/`",
            "",
            (
                "构建不依赖 Node、GPU 或商业 API。静态主机子路径兼容；部署需沿用具体 release 审批。"
                if zh
                else "Builds need no Node, GPU or commercial API. Static hosting subpaths are supported; deployment follows the exact-release approval contract."
            ),
            "",
            ("## 资源与证据" if zh else "## Resources and evidence"),
            " ",
            (
                f"发现 {s['discovered']} 条 · 去重收录 {s['cataloged']} 项 · 一手来源 / 本地配方证据 {s['source_verified']} 项。"
                if zh
                else f"{s['discovered']} discovery records · {s['cataloged']} canonical resources · {s['source_verified']} primary-source/local-recipe evidence records."
            ),
            "",
            ("| 类型 | 数量 |" if zh else "| Type | Count |"),
            "|---|---:|",
        ]
        lines += [f"| {TYPE_LABELS[k][zh]} | {v} |" for k, v in sorted(s["by_type"].items())]
        lines += [
            "",
            (
                f"已接入 {s['adapter_checkpoints']} 个 checkpoint · 已实现 {s['implemented_tasks']} 个任务 · 已批准 {s['approved_full_summaries']} 份全量公开集摘要。"
                if zh
                else f"{s['adapter_checkpoints']} implemented checkpoints · {s['implemented_tasks']} implemented tasks · {s['approved_full_summaries']} approved full-public summaries."
            ),
            "",
            (
                "全量是注明基准的完整分母，包含错误记录；不表示所有任务通过。JevBench public 不包含 sealed 或官方 composite。"
                if zh
                else "Full evaluation covers the named split and its error denominator; it does not imply every task passed. JevBench public excludes sealed tasks and the official composite."
            ),
            "",
            ("## 运行推理与评测" if zh else "## Inference and evaluation"),
            "",
            "```bash",
            "python -m pip install '.[eval]'",
            "export JEVZOO_WORKSPACE=/absolute/path/outside/git",
            "jevzoo evaluate --deployment qwen35-4b --suite jevbench-public --profile smoke",
            "jevzoo report --run /absolute/path/to/run",
            "```",
            "",
            f"[{'评测协议' if zh else 'Evaluation protocol'}](docs/evaluation.md) · [{'模型卡' if zh else 'Model cards'}](docs/models/qwen35-4b.md) · [{'结果摘要' if zh else 'Result summaries'}](results/published/README.md)",
            "",
            ("## 训练与校准" if zh else "## Training and calibration"),
            "",
            (
                "Lab 保留完整训练实现。R1 语言 LoRA、R2 candidate head 已有真实梯度与重载 smoke；正式收益、跨源近重复审核及四角色划分仍需完成。校准不使用 test 标签。"
                if zh
                else "The Lab retains full training code. R1 language LoRA and an R2 candidate head have real-gradient/reload smoke; formal gains, cross-source near-duplicate audits and four-role split review remain pending. Calibration never fits test labels."
            ),
            "",
            f"[{'Lab 训练文档（需权限）' if zh else 'Lab training docs (access required)'}]({LAB}/blob/main/docs/training.md)",
            "",
            ("## 数据维护与发布" if zh else "## Maintenance and publication"),
            "",
            f"[{'网站构建与维护' if zh else 'Site build and maintenance'}](site/README{'_zh' if zh else ''}.md) · [NOTICE](NOTICE)",
            "",
            (
                "商业资源可展示，当前商业推理禁用，不设置本次预算上限。模型、数据、checkpoint、日志和逐样本产物留仓外；公开只导出允许的元数据和具体批准的摘要。"
                if zh
                else "Commercial resources are browsable; commercial inference is disabled, with no budget cap in this task. Models, data, checkpoints, logs and row-level artifacts stay outside Git; public export includes allowed metadata and exactly approved summaries."
            ),
            "",
            f"Discovery: [{data['upstream']['repo']}](https://github.com/{data['upstream']['repo']}/tree/{data['upstream']['revision']}) · MIT · {data['updated_on']}",
        ]
        (repo / name).write_text("\n".join(line.rstrip() for line in lines) + "\n")


def validate(data):
    ids = {r["id"] for r in data["resources"]}
    urls = [canonical(r["canonical_url"]) for r in data["resources"] if r["canonical_url"]]
    if len(ids) != len(data["resources"]) or len(urls) != len(set(urls)):
        raise ValueError("Duplicate canonical resource identity")
    for r in data["resources"]:
        if r["resource_type"] not in TYPE_LABELS:
            raise ValueError("Unknown resource type")
        if any(x not in USE_LABELS for x in r["purposes"]):
            raise ValueError("Unknown purpose")
        if not all(tr(r, "description", locale) for locale in ["en", "zh"]):
            raise ValueError("Missing bilingual description: " + r["id"])
        if any(x not in ids for x in r["related_ids"]):
            raise ValueError("Unresolved relationship")
        if r["runtime"]["fully_evaluated"] and not r["runtime"]["evaluated_scopes"]:
            raise ValueError("Unscoped full evaluation")
        if r["runtime"]["smoke_tested"] and not r["runtime"]["adapter_implemented"]:
            raise ValueError("Smoke without implementation")
        for values in r["links"].values():
            if any(not canonical(x) for x in values):
                raise ValueError("Unsafe external URL")


def build(
    repo, output, public_repo=None, approved_manifest=None, write_readmes=False, write_index=True
):
    output = output.resolve()
    repo = repo.resolve()
    if output.is_relative_to(repo):
        raise ValueError("Build output must remain outside the Git checkout")
    data = compile_catalog(repo, public_repo, approved_manifest)
    validate(data)
    output.mkdir(parents=True, exist_ok=True)
    assets = output / "assets"
    assets.mkdir(exist_ok=True)
    for f in ["styles.css", "app.js", "favicon.svg"]:
        shutil.copyfile(repo / "site" / f, assets / f)
    (assets / "catalog.json").write_text(
        json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    )
    (assets / "approved-results-manifest.json").write_text(
        json.dumps(data["approval"] or {}, indent=2)
    )
    for locale in ["en", "zh"]:
        folder = output / locale
        folder.mkdir(exist_ok=True)
        (folder / "index.html").write_text(shell(locale, "home", home(data, locale)))
        for route, func, title in [
            ("catalog", catalog_page, labels(locale)["catalog"]),
            ("platform", platform, labels(locale)["platform"]),
            ("about", about, labels(locale)["about"]),
        ]:
            target = folder / route
            target.mkdir(exist_ok=True)
            (target / "index.html").write_text(
                shell(locale, route, func(data, locale), 1, title, route + "/")
            )
        for r in data["resources"]:
            target = folder / "resources" / r["slug"]
            target.mkdir(parents=True, exist_ok=True)
            (target / "index.html").write_text(
                shell(
                    locale,
                    "detail",
                    detail(data, r, locale),
                    2,
                    r["name"],
                    "resources/" + r["slug"] + "/",
                )
            )
    (output / "index.html").write_text(
        '<!doctype html><html lang="en"><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=en/"><title>JevZoo</title><p><a href="en/">English</a> · <a href="zh/">简体中文</a></p></html>'
    )
    (output / "404.html").write_text(
        '<!doctype html><html><meta charset="utf-8"><title>JevZoo · Not found</title><h1>Page not found / 页面不存在</h1><a href="./">JevZoo</a></html>'
    )
    (output / ".nojekyll").write_text("")
    if write_readmes:
        readmes(data, repo)
    discovery_ids = {r["id"] for r in read(repo / "catalog/catalog.json")["discovery_resources"]}
    curated_ids = {r["id"] for r in read(repo / "catalog/catalog.json")["curated_resources"]}
    canonical_map = {
        canonical(r["canonical_url"]): {
            "resource_id": r["id"],
            "url": r["canonical_url"],
            "aliases": r["aliases"],
            "source_record_ids": r["source_record_ids"],
            "discovery_id": next((x for x in r["source_record_ids"] if x in discovery_ids), None),
            "curated_ids": [x for x in r["source_record_ids"] if x in curated_ids],
        }
        for r in data["resources"]
        if r["canonical_url"]
    }
    # Preserve the legacy all-source URL index as well as primary identities.
    for r in data["resources"]:
        for values in r["links"].values():
            for url in values:
                key = canonical(url)
                index = canonical_map.setdefault(
                    key,
                    {
                        "resource_id": r["id"],
                        "url": url,
                        "aliases": [],
                        "source_record_ids": [],
                        "discovery_id": None,
                        "curated_ids": [],
                    },
                )
                index["related_resource_ids"] = list(
                    dict.fromkeys(index.get("related_resource_ids", []) + [r["id"]])
                )
                index["curated_ids"] = list(
                    dict.fromkeys(
                        index["curated_ids"]
                        + [x for x in r["source_record_ids"] if x in curated_ids]
                    )
                )
    if write_index:
        (repo / "catalog/canonical-resources.json").write_text(
            json.dumps(
                {
                    "schema_version": "1.1",
                    "by_url": canonical_map,
                    "unique_source_urls": len(canonical_map),
                    "derived_from_registry_sha256": data["registry_sha256"],
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n"
        )
    report = {
        "built_utc": datetime.now(ZoneInfo("UTC")).isoformat(),
        "registry_sha256": data["registry_sha256"],
        "stats": data["stats"],
        "locales": ["en", "zh"],
        "html_pages": 2 * (4 + len(data["resources"])) + 2,
        "approval": data["approval"],
        "no_model_or_api_execution": True,
        "type_labels": TYPE_LABELS,
    }
    (output / "build-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(
        json.dumps(
            {
                "output": str(output),
                "stats": data["stats"],
                "html_pages": report["html_pages"],
                "catalog_bytes": (assets / "catalog.json").stat().st_size,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return data


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--repo", type=pathlib.Path, default=ROOT)
    p.add_argument("--output", type=pathlib.Path)
    p.add_argument("--public-repo", type=pathlib.Path)
    p.add_argument("--approved-manifest", type=pathlib.Path)
    p.add_argument("--readmes", action="store_true")
    p.add_argument(
        "--no-source-write",
        action="store_true",
        help="Build without changing READMEs or the canonical index",
    )
    a = p.parse_args()
    if a.no_source_write and a.readmes:
        p.error("--readmes cannot be combined with --no-source-write")
    workspace = pathlib.Path(
        __import__("os").environ.get("JEVZOO_WORKSPACE", str(a.repo.parent / "jev-zoo-workspace"))
    )
    output = a.output or workspace / "builds/jevzoo-site"
    public = a.public_repo or (
        a.repo.parent / "Jev-Zoo" if (a.repo.parent / "Jev-Zoo").exists() else None
    )
    build(a.repo, output, public, a.approved_manifest, a.readmes, not a.no_source_write)


if __name__ == "__main__":
    main()
