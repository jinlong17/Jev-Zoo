from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

from .fetch import get_json
from .storage import workspace, write_json

UPSTREAM = "heyjunpenn/awesome-jev"
PUBLIC_URL = "https://github.com/jinlong17/Jev-Zoo"


def parse_awesome(markdown: str) -> list[dict]:
    category, entries, seen = "other", [], set()
    for line in markdown.splitlines():
        heading = re.match(r"^### (.+?) \((\d+)\)$", line)
        if heading:
            category = heading.group(1)
        if not line.startswith("| ["):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        match = re.match(r"\[([^\]]+)\]\((https://github.com/[^)]+)\)", cells[0])
        if not match or len(cells) != 5:
            continue
        name, url = match.groups()
        url = url.removesuffix("/").removesuffix(".git")
        identity = url.lower()
        if identity in seen:
            continue
        seen.add(identity)
        entries.append(
            dict(
                id=identity.removeprefix("https://github.com/"),
                name=name,
                url=url,
                category=category,
                description=cells[4],
                language=cells[2],
                upstream_added_on=cells[3],
                upstream_stars=cells[1],
                source=UPSTREAM,
                evidence_level="discovered",
                adapter_implemented=False,
                smoke_tested=False,
                evaluated=False,
            )
        )
    if not entries:
        raise ValueError("Upstream catalog parser found no resource rows")
    return entries


def refresh(repo: Path, seed_path: Path, *, verify_links: bool = False) -> dict:
    # A new discovery snapshot must preserve reviewed bilingual metadata and assets.
    prior_path = repo / "catalog/catalog.json"
    prior = json.loads(prior_path.read_text()) if prior_path.exists() else {}
    checked_on = datetime.now(timezone.utc).date().isoformat()
    commit = get_json(f"https://api.github.com/repos/{UPSTREAM}/commits/main")
    revision = commit["sha"]
    url = f"https://raw.githubusercontent.com/{UPSTREAM}/{revision}/README.md"
    with urllib.request.urlopen(url, timeout=60) as response:
        markdown = response.read().decode()
    entries = parse_awesome(markdown)
    if verify_links:

        def inspect(entry: dict) -> tuple[str, dict]:
            try:
                metadata = get_json(f"https://api.github.com/repos/{entry['id']}")
                return entry["id"], dict(
                    link_status="reachable",
                    checked_on=checked_on,
                    stars=metadata["stargazers_count"],
                    upstream_pushed_at=metadata["pushed_at"],
                    archived=metadata["archived"],
                    code_license=(metadata.get("license") or {}).get("spdx_id"),
                )
            except urllib.error.HTTPError as error:
                return entry["id"], dict(link_status=f"http_{error.code}", checked_on=checked_on)
            except Exception as error:
                return entry["id"], dict(link_status="unverified", error_type=type(error).__name__)

        with ThreadPoolExecutor(max_workers=4) as pool:
            jobs = {pool.submit(inspect, entry): entry for entry in entries}
            for job in as_completed(jobs):
                _, metadata = job.result()
                jobs[job].update(metadata)
    if seed_path.exists():
        seed = json.loads(seed_path.read_text())
    else:
        prior = json.loads((repo / "catalog/catalog.json").read_text())
        seed = {
            "entries": prior["curated_resources"],
            "benchmarks": prior["benchmarks"],
            "papers": prior["papers"],
            "sources": prior["sources"],
        }
    curated = seed["entries"]
    additions = [
        dict(
            id="h2o-lightning",
            name="H2O-Lightning-4B",
            kind="open_weight_model",
            source_url="https://huggingface.co/h2oai/h2o-lightning-4b",
            modalities_declared=["text", "image"],
            base_model="Qwen/Qwen3.5-4B",
            verified_on="2026-10-12",
            evidence_status="official_model_card",
            adapter_implemented=False,
            smoke_tested=False,
            benchmark_reproduced=False,
        ),
        dict(
            id="microsoft-decision-1",
            name="Microsoft-Decision-1",
            kind="closed_api",
            source_url="https://commandline.microsoft.com/microsoft-decision-1-model-foundry/",
            modalities_declared=["text"],
            base_model="Qwen3.5-9B",
            verified_on="2026-10-12",
            evidence_status="official_service_announcement",
            weights_status="not_verified_available",
            enable_paid_by_default=False,
            adapter_implemented=False,
            smoke_tested=False,
            benchmark_reproduced=False,
        ),
    ]
    ids = {entry["id"] for entry in curated}
    curated.extend(entry for entry in additions if entry["id"] not in ids)
    catalog = dict(
        schema_version="1.0",
        as_of="2026-10-12",
        upstream=UPSTREAM,
        upstream_revision=revision,
        upstream_commit_date=commit["commit"]["committer"]["date"],
        discovery_resources=entries,
        curated_resources=curated,
        benchmarks=seed["benchmarks"],
        papers=seed["papers"],
        sources=seed["sources"],
        facts_checked="links and metadata; execution requires separate run evidence",
    )
    if prior.get("site_contract"):
        previous = {entry["id"]: entry for entry in prior.get("discovery_resources", [])}
        for entry in entries:
            old = previous.get(entry["id"], {})
            for key in ("presentation", "aliases", "site_primary_review"):
                if key in old:
                    entry[key] = old[key]
            if not verify_links:
                for key in (
                    "link_status",
                    "checked_on",
                    "stars",
                    "upstream_pushed_at",
                    "archived",
                    "code_license",
                ):
                    if key in old:
                        entry[key] = old[key]
            if old.get("description") != entry.get("description"):
                entry.setdefault("presentation", {})["translation_needs_review"] = True
        # Never silently discard failed or removed upstream entries.
        current_ids = {entry["id"] for entry in entries}
        for identity, old in previous.items():
            if identity not in current_ids:
                old["upstream_removed_at_revision"] = revision
                old.setdefault("presentation", {})["tier"] = "review"
                entries.append(old)
        for key in ("curated_resources", "papers", "benchmarks"):
            merged = {entry["id"]: entry for entry in catalog[key]}
            merged.update({entry["id"]: entry for entry in prior.get(key, [])})
            catalog[key] = list(merged.values())
        catalog["sources"].update(prior.get("sources", {}))
        catalog["recipes"] = prior.get("recipes", [])
        catalog["site_contract"] = prior["site_contract"]
        catalog["site_contract"]["updated_on"] = checked_on
        catalog["as_of"] = checked_on
    write_json(repo / "catalog/catalog.json", catalog)
    return catalog


def render(repo: Path) -> None:
    catalog = json.loads((repo / "catalog/catalog.json").read_text())
    model_lock = json.loads((repo / "manifests/models.lock.json").read_text())
    root = workspace()
    model_rows = []
    status_cache = {}
    cache_path = repo / "catalog/status.json"
    cached = json.loads(cache_path.read_text()) if cache_path.exists() else {}

    for entry in model_lock["entries"]:
        state_path = root / "downloads" / f"{entry['id']}.json"
        state = json.loads(state_path.read_text()) if state_path.exists() else {}
        status = (
            state.get("status", "not_downloaded")
            if state.get("revision") == entry["revision"]
            else "not_downloaded"
        )
        evidence = _run_evidence(root, entry)
        if (
            not evidence["records"]
            and cached.get(entry["id"], {}).get("checkpoint_revision") == entry["revision"]
        ):
            evidence = cached[entry["id"]]["evidence"]
        if (
            not state
            and cached.get(entry["id"], {}).get("checkpoint_revision") == entry["revision"]
        ):
            status = cached[entry["id"]]["download"]
        status_cache[entry["id"]] = {
            "checkpoint_revision": entry["revision"],
            "download": status,
            "evidence": {key: value for key, value in evidence.items() if key != "records"},
        }
        card = _model_card(entry, status, evidence)
        card_path = repo / "docs/models" / f"{entry['id']}.md"
        card_path.parent.mkdir(parents=True, exist_ok=True)
        card_path.write_text(card)
        model_rows.append(
            f"| [{entry['repo_id']}](docs/models/{entry['id']}.md) | {entry['batch']} | "
            f"{status} | {evidence['smoke_tested']} | {', '.join(evidence.get('full_benchmarks', [])) or 'pending'} |"
        )
    write_json(cache_path, status_cache)
    curated_index = []
    sources = catalog["sources"]
    canonical = {
        entry["url"].lower().rstrip("/"): {
            "url": entry["url"],
            "discovery_id": entry["id"],
            "curated_ids": [],
        }
        for entry in catalog["discovery_resources"]
    }
    for entry in catalog["curated_resources"]:
        slug = re.sub(r"[^a-z0-9]+", "-", entry["id"].lower()).strip("-")
        links = (
            [entry["source_url"]]
            if entry.get("source_url")
            else [sources[key]["url"] for key in entry.get("source_ids", []) if key in sources]
        )
        for url in links:
            record = canonical.setdefault(
                url.lower().rstrip("/"), {"url": url, "discovery_id": None, "curated_ids": []}
            )
            record["curated_ids"].append(entry["id"])
        fields = {
            key: value
            for key, value in entry.items()
            if key not in {"own_measurements", "notes", "source_ids"}
        }
        card = repo / "docs/curated" / f"{slug}.md"
        card.parent.mkdir(parents=True, exist_ok=True)
        card.write_text(
            f"# {entry['name']}\n\n"
            + entry.get("notes", "")
            + "\n\n"
            + "\n".join(f"- {key}: `{value}`" for key, value in fields.items())
            + "\n\n"
            + "\n".join(f"- Source: {url}" for url in links)
            + "\n\n"
            + "Seed metadata dated 2026-10-06 remains historical; real execution evidence is maintained in the checkpoint cards and approved summaries.\n"
        )
        curated_index.append(f"- [{entry['name']}](../curated/{slug}.md)")
    (repo / "docs/resources/curated.md").write_text(
        "# Curated model/API/runtime/paper entries\n\n" + "\n".join(curated_index) + "\n"
    )
    write_json(
        repo / "catalog/canonical-resources.json",
        {"schema_version": "1.0", "by_url": canonical, "unique_source_urls": len(canonical)},
    )
    counts = {}
    for entry in catalog["discovery_resources"]:
        counts[entry["category"]] = counts.get(entry["category"], 0) + 1
    category_links = []
    for category, count in counts.items():
        slug = re.sub(r"[^a-z0-9]+", "-", category.lower()).strip("-")
        page = repo / "docs/resources" / f"{slug}.md"
        page.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            f"# {category}\n",
            "来源：awesome-jev；链接收录与本项目执行证据独立。\n",
            "| 项目 | 语言 | 描述 | 链接核验 |",
            "|---|---|---|---|",
        ]
        for entry in catalog["discovery_resources"]:
            if entry["category"] == category:
                description = entry["description"].replace("|", "\\|")
                detail_slug = re.sub(r"[^a-z0-9]+", "-", entry["id"].lower()).strip("-")
                detail = repo / "docs/resources/cards" / f"{detail_slug}.md"
                detail.parent.mkdir(parents=True, exist_ok=True)
                detail.write_text(
                    f"# {entry['name']}\n\n{entry['description']}\n\n"
                    f"- Official repository: {entry['url']}\n"
                    f"- Category: {entry['category']}; language: {entry['language']}.\n"
                    f"- GitHub stars at verification: {entry.get('stars', 'unknown')}; last push: {entry.get('upstream_pushed_at', 'unknown')}.\n"
                    f"- Code license metadata: {entry.get('code_license', 'unknown')}; component licenses require the official release.\n"
                    f"- Link check: {entry.get('link_status', 'unknown')} on {entry.get('checked_on', 'unknown')}.\n"
                    f"- Provenance: {UPSTREAM}@{catalog['upstream_revision']}.\n"
                    "- Base / parameters / head / loader: unverified for this discovery record; see curated model cards where available.\n"
                    "- JevZoo execution: catalog discovery; no measured result attached to this record.\n"
                )
                lines.append(
                    f"| [{entry['name']}](cards/{detail_slug}.md) | {entry['language']} | "
                    f"{description} | {entry.get('link_status', 'imported_not_rechecked')} |"
                )
        page.write_text("\n".join(lines) + "\n")
        category_links.append(f"- [{category}: {count}](docs/resources/{slug}.md)")
    intro = f"""# JevZoo

资源发现、开放权重下载与可复现的多模态决策评测。

An independent catalog and reproducible evaluation toolkit for typed decision models.

目录核验日：{catalog["as_of"]}。发现源：[{UPSTREAM}](https://github.com/{UPSTREAM})，
固定提交 `{catalog["upstream_revision"][:12]}`；导入 {len(catalog["discovery_resources"])} 个独立资源。
作者报告、已下载、本项目冒烟和正式评测分别显示。

## 模型与下载状态

| Checkpoint / 详细卡片 | 批次 | 下载 | 真实冒烟通过 | 已完成的全量基准 |
|---|---|---|---|---|
{chr(10).join(model_rows)}

Microsoft-Decision-1 收录为服务条目；目前未核验到可下载的官方 checkpoint。
商业 API 默认禁用，不要求预算字段。未来凭据通过本地未跟踪配置启用。

## Benchmark 与协议

参见 [JevZoo-Eval v0.1](docs/evaluation.md)：JevBench 公开 231 条、Typed Decisions、
JEVal、DecisionBench、MMStar、Sys1Cal，以及 Banking77、CLINC150、SST-2、BoolQ、ARC。
公开集、teacher-agreement、已知概率诊断和视觉任务分别报告，不混排不同协议。

## 使用

```bash
python -m pip install '.[fetch,eval]'
export JEVZOO_WORKSPACE=/absolute/path/outside/git
jevzoo fetch --manifest manifests/models.lock.json
jevzoo fetch --manifest manifests/datasets.lock.json
jevzoo evaluate --suite jevzoo-eval-v0.1 --deployment qwen35-4b --profile smoke
jevzoo report --run /absolute/path/to/run
```

核心可单独安装，不在 import 时加载 Torch。特殊 head 使用固定版本的官方 loader。
真实数据、权重、日志和逐样本结果存仓外；[公开结果](results/published/README.md)由批准的摘要生成。

## 全部资源分类

[详细精选资源卡：种子与新增条目](docs/resources/curated.md)；[框架与数据架构](docs/architecture.md)。

{chr(10).join(category_links)}

## 论文与训练

资源目录保存论文及训练入口。共同底座为 Python 3.12 / PyTorch / Transformers /
Datasets / PEFT / Accelerate。实验训练代码保留在 Lab；公开版当前发布稳定 eval 与公开示例。

## 来源与状态

模型卡片保留基座、许可、组件、版本和运行证据。下载不等于正确加载，冒烟不等于正式跑分。
本项目独立于模型发布方。上游目录复用内容的 MIT 署名见 [NOTICE](NOTICE)。
"""
    (repo / "README.md").write_text(intro)
    (repo / "README_zh.md").write_text(intro)
    # Site output and both READMEs share the same catalog projection. This builder
    # stays outside evaluator code_hash and never launches a model or scans runs.
    if (repo / "site/build.py").exists() and catalog.get("site_contract"):
        import subprocess
        import sys

        subprocess.run(
            [sys.executable, str(repo / "site/build.py"), "--repo", str(repo), "--readmes"],
            check=True,
        )


def _run_evidence(root: Path, entry: dict) -> dict:
    smoke, full, records = False, False, []
    for path in (root / "runs").glob("**/manifest.json"):
        manifest = json.loads(path.read_text())
        if (
            manifest.get("model_id") != entry["id"]
            or manifest.get("checkpoint_revision") != entry["revision"]
        ):
            continue
        if manifest.get("state") != "completed" or manifest.get("backend") == "mock":
            continue
        metrics_path = path.parent / "metrics.json"
        if not metrics_path.exists():
            continue
        metrics = json.loads(metrics_path.read_text())
        success = metrics.get("valid", 0) > 0 and metrics.get("errors", 0) == 0
        smoke |= success and manifest.get("profile") == "smoke"
        full |= (
            success
            and manifest.get("profile") == "full"
            and metrics.get("attempted") == metrics.get("eligible")
        )
        records.append(
            dict(
                run_id=manifest["run_id"],
                suite=manifest["suite"],
                profile=manifest["profile"],
                metrics=metrics,
                checkpoint_revision=entry["revision"],
            )
        )
    full_benchmarks = sorted(
        {
            r["suite"]
            for r in records
            if r["profile"] == "full"
            and r["metrics"]["errors"] == 0
            and r["metrics"]["attempted"] == r["metrics"]["eligible"]
        }
    )
    return dict(
        smoke_tested=smoke, full_evaluated=full, full_benchmarks=full_benchmarks, records=records
    )


def _model_card(entry: dict, status: str, evidence: dict) -> str:
    # Local paths and private run IDs stay out of the card's public payload.
    return f"""# {entry["repo_id"]}

- 权重与模型卡：https://huggingface.co/{entry["repo_id"]}
- 固定 revision：`{entry["revision"]}`
- 基座：`{entry.get("base_model")}`
- 模型卡许可：`{entry.get("license")}`；代码、数据及组件条件见上游。
- 必需下载：{entry["total_bytes"] / 2**30:.3f} GiB，{len(entry["files"])} 个文件。
- backend：`{entry["backend"]}`；download：`{status}`。
- 真实冒烟：`{evidence["smoke_tested"]}`；全量基准：`{evidence.get("full_benchmarks", [])}`。
- 下载清单：`manifests/models.lock.json`。

原生 head、原始读出、官方校准和候选顺序集成需要独立 deployment。作者结果应通过上游入口查看；
JevZoo 的公开数字只由经过审批的运行摘要生成。
"""
