# State inventory and integration handoff

[中文](STATUS_AND_HANDOFF_zh.md)

Cutoff: 2026-10-12 America/Los_Angeles / 2026-10-13 UTC. This is a site-content snapshot; active evaluation progress continues to change.

## Existing state and reuse

- Initial Lab HEAD `ceb69c29e490ef4d4391bf575ca1106baba588a1` had parallel evaluation WIP. Public HEAD `a67c531e29a467ec3df3a882b4717f85efbf9949` was clean, with release `jevzoo-v0.1-173cb3e6133c95aa-3e6821ed`.
- Discovery already lived in `catalog/catalog.json`: 981 entries (966 reachable, 15 HTTP 404), 45 curated records, nine papers, 17 benchmark/proposal records and 73 sources. The renderer produced discovery/curated/model cards, category Markdown and a canonical index. Both READMEs were identical mixed-language text; no frontend/site existed.
- No parallel registry. Existing records gained bilingual text, types/purposes, component terms, verification, links and curation reasons. Current arrays contain 981 discovery, 68 curated, 48 papers, 17 benchmarks and two recipes; overlapping asset references are canonically merged, not added as model counts.
- Runtime links use manifests, adapters/tasks and result evidence. At initial inspection the status document reported 82/110 full combinations and 110/110 error-free interface smokes. These are Lab status, not new runs or wholly approved public scores. The site selects 120 summaries matching existing approved hashes (10 full, 110 smoke); full summaries cover 231 JevBench public requests. All 120 approved summaries are included; the pending full matrix is excluded.

## Implemented surface and counts

- Standard-library static generation and native HTML/CSS/JS: English/Chinese home, catalog, details, platform and provenance pages. Bilingual name/description/publisher/alias search; type/purpose filters and expanded modality/access/form/evidence/runtime filters; pagination, clear/empty/share states, keyboard and mobile navigation.

| Primary resource type | Count |
|---|---:|
| Apps & demos | 351 |
| Benchmark/protocol projects | 103 |
| Agent components | 236 |
| Independent data assets | 10 |
| Discovery lists | 42 |
| Frameworks | 102 |
| Model families/checkpoints/readout projects | 126 |
| Papers | 48 |
| Recipes | 2 |
| Services | 5 |
| Tools & SDKs | 78 |

981 discovered; 1103 cataloged canonical resources; 144 primary-source/local-recipe evidence records. Tiers: 143 curated, 944 broad, 16 review/invalid. 33 overlapping-record merges; two unbuilt proposals excluded and retained in planning.

10 implemented checkpoints, 10 with approved smoke evidence and 10 with at least one approved full scope; 11 implemented tasks. Two private Lab recipe smokes, zero formally validated training recipes. These denominators remain separate.

## Additions and integration priority

- P1: pplx v1.1 versus v1; SII-Decision 4B LoRA/full (renamed InnerJev, merged BF16); Candidate Isolation Qwen4B. Version/readout/distillation/order controls need separate deployments, native components and frozen controls. No new checkpoint was integrated/downloaded here.
- P2: d3-mini/d3, InternDecision, current Strands checkpoint and RSI v6.1-VL. Audit joint questions/head/attention/processor/temperature/exit protocol first; do not reuse existing deployment IDs.
- Fourteen mainstream tools added: Transformers, PEFT, Accelerate, TRL, Datasets, vLLM, SGLang, lmms-eval, VLMEvalKit, EvalScope, Inspect AI, LLaMAFactory, ms-swift and Safetensors. Code licenses do not establish native JEV-head support.
- Ten representative app/tool READMEs reviewed separately; nine confirm identifiable JEV integration. OpenWork README evidence is insufficient; the inherited claim stays explicit pending code inspection. Official URLs, README blob SHAs and times are retained in the same records.

## Main-window integration

- Ready to adopt: new site source, bilingual pages/READMEs, registry presentation fields, site docs, attribution, standalone build and offline audit. Do not hand-edit build output; rebuild after registry changes.
- Integrate additive changes in two mixed WIP files: catalog.py metadata-preservation/bilingual-generation hook, and public_manifest.py site/docs whitelist additions. Candidate records initial file hashes; never overwrite later main-window changes with whole snapshots.
- Plan addendum: dual roles in parallel, bilingual parity, one canonical registry, independent display/runtime evidence, commercial-service inclusion, actual HTML/browser acceptance and exact-approved deployment. Existing staged runs/asset contracts remain valid; old planning counts are not current facts. Historical MANIFEST/run contracts are not rewritten.
- The site and release checks are integrated on isolated Lab branch codex/jevzoo-site-release-2026-10-12; active evaluation and uncommitted WIP are excluded. The existing release prepare command binds the clean committed source and still requires exact-release/hash approval. No public push, DNS or deployment occurred.

## Validation and limits

- 2,216 HTML pages and 1,103 resource details per locale; all internal paths and locale routes audited. Eleven offline contracts cover identity/relations, link-only evidence, approval byte matching, download-only support denial and N/A accuracy. Chromium covers 1440×1000, 390×844 and 768×1024 navigation/search/filter/share/relations/results/responsiveness; reports/screenshots stay in external QA.
- No new model/data binary download, GPU/training/commercial inference or evaluation restart/termination. Six protected evaluator files and three asset locks retain their initial hashes; public repository retains its baseline.
- Most broad entries have only links/upstream descriptions; purposes include heuristic editorial tags. They receive no runnable badges. Unknown component terms, failed links, training contamination, OpenWork integration and ETHACC remain unresolved. New paper/model inclusion is not independent replication.
- Next experiments: same-base frozen/R1/R2 controls, independent calibration, order/menu-size/label-template perturbations, joint versus isolated questions and image-removal/shared-prefix ablations. Assess accuracy, NLL/Brier, coverage/error denominators and controlled latency, not smoke/public-subset alone. Existing literature evidence supports the detailed experiment plan; this window ran none of these experiments.

Browser acceptance: 45 core interactions plus six subpath/relationship checks, all passed with zero console/page errors. Eleven offline tests passed. The current static artifact passed 2,216-page internal-link and locale audit. Broad entries remain unexecuted; formal training is pending.

2026-10-13 integration: 37 baseline offline tests and 11 site tests pass. Explicit public scope excludes the full-evaluation WIP. The deployment manifest binds 2,222 static files, including 2,216 HTML pages; the proposed Pages URL is not published. The previous 40-summary handoff count is corrected to 120 formally approved summaries.
