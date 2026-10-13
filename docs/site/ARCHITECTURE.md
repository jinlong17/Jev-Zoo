# JevZoo discovery site / 展示平台架构

JevZoo develops two connected surfaces: broad resource discovery and reproducible inference/evaluation/training/calibration. Browsable does not imply runnable. This static site reads the existing catalog and runtime evidence; it introduces no account, backend, parallel hand-maintained registry, or new model run.

JevZoo 同时建设广覆盖资源发现与可复现训练评测。本轮采用 Python 标准库静态构建 + 原生 HTML/CSS/JavaScript：不新增前端框架依赖，页面可部署到 GitHub Pages 或任意静态主机，支持子路径。代码原生版式先固定信息结构与设计tokens，再实现交互；遵守本轮商业推理禁用要求，不调用图像生成服务。

## Fact sources / 事实来源

- `catalog/catalog.json`: existing discovery, curated, paper, benchmark and source records, extended in place with bilingual presentation, curation reasons, aliases, links and relations. Raw discovery evidence remains; invalid and duplicate entries have recorded dispositions.
- `catalog/canonical-resources.json`: existing generated URL mapping; the site derives canonical identity from catalog URLs and explicit aliases. Generated site JSON is a projection, never a separately edited fact database.
- `manifests/models.lock.json`, `manifests/datasets.lock.json`: deployed checkpoint/data identities and revisions, read only. Runtime capabilities come from implemented backends and task IDs, independently of upstream capability claims.
- `catalog/status.json`: cached evidence, checked against checkpoint revision. Result numbers shown on the site require exact hashes matching the last approved release/public manifest. Pending Lab results remain outside the published result list.
- Recipe records point to existing Lab configs/docs and disclose smoke-only validation and formal-training limits. No training implementation is automatically published.

## Routes and journeys / 页面与浏览路径

| Route (both `/en/` and `/zh/`) | Purpose |
|---|---|
| Home | Two project roles; Models, Papers, Tools, Benchmarks & Data, Applications entrances; featured resources, updates and the runnable platform |
| `catalog/` | Search name, publisher, bilingual description, aliases and keywords; type/purpose filters; collapsible modality/openness/form/evidence/runtime filters; sorting, pagination, reset, empty state and shareable query string |
| `resources/<stable-slug>/` | What/why/start/limitations, component openness/license, original paper/code/weights/data/docs/demo, evidence and checkpoint status, related assets |
| `platform/` | Supported checkpoints/tasks, approved scoped results, inference/evaluation examples and Lab training/calibration recipes; no GPU execution in browser |
| `about/` | Inclusion rules, counts, provenance, date semantics, maintenance and attribution |

Home → category → filtered catalog → detail → source / related paper-model-data-recipe / platform. Language switching preserves the logical route and catalog query. One canonical record can have multiple purposes; its primary resource type determines exclusive type counts. Checkpoint assets and model families remain distinct labels. Support states are independent evidence flags, not a marketing ladder.

## Design spec / 页面方案

Ivory/light-blue surfaces, deep navy text, royal-blue links, restrained mint for verified runtime evidence. Wide 1,240px reading container; 72px top navigation; generous type-led homepage, an understated connected-asset panel, editorial featured rows, category entry tiles and platform block. Catalog uses a compact filter rail and paginated readable resource rows; details emphasize source actions and relationships. No giant all-resource homepage, fake performance totals or sponsored rankings.

CSS tokens: background `#f8fafc`, surface `#ffffff`, ink `#152842`, muted `#62738a`, accent `#2456df`, border `#dce5ef`, radius 12px; native system Latin/CJK fonts, consistent 8px spacing. Native controls, visible focus, skip link, `/` search shortcut, responsive navigation/filter panel, reduced-motion support. Internal implementation hashes live in evidence details rather than the hero.

## Reference decisions / 参考源码分析

Reference: `heyjunpenn/awesome-jev@39854d858fff73bf3172949c9f968c6cb12beafa`, MIT. Its code is Astro static output with Cloudflare adapter, localized README parsing, per-locale routes/messages, category navigation, client filtering/keyboard controls, catalog JSON endpoints and URL-normalized inclusion dates. It validates locale row/order/URL parity. Stars sort and initial row limits keep long directories manageable. GitHub provides sources/submission paths.

Borrow the navigation, bilingual identity parity, compact search, progressive disclosure and attribution ideas. Reuse only MIT-licensed catalog descriptions and Chinese translations with the retained notice; original JevZoo UI/build implementation. Do not import the sponsor checkout/Stripe/D1/KV/traffic stack, flags-as-language UI, copied branding or stars as a capability ranking. The reference has duplicated hard-coded navigation counts (962) while the README snapshot contains981; JevZoo computes counts from its generated canonical view.

The live reference URL was text-accessible; rendered inspection and screenshot evidence are recorded separately in workspace QA. A live website snapshot can differ from its repository HEAD. Neither proves JEV integration or open weights for every linked project.

## Update and publication / 更新与公开

Edit existing catalog records, run the metadata validation and site builder, then browser QA. The README/Chinese README and site resource pages are generated from the same normalized catalog view. Existing catalog-rendering flow calls the site generator when present, avoiding a second manually maintained README. Runtime snapshots update only from current evidence and approved summary hashes.

Build output and QA/screenshots live outside Git. A site content candidate provides explicit paths/hashes for integration with the existing publisher. Official release preparation continues to require reviewed committed clean Lab, current checks, public baseline and exact release approval. Current unrelated evaluation WIP is preserved; no public push/deploy is authorized by this task.

Release integration (2026-10-13): source is isolated on a Lab branch; main evaluation WIP is not staged. The formal whitelist includes a deterministic static payload manifest. Build verification is read-only (`--no-source-write`), and both README locale projections are checked instead of comparing the two languages byte-for-byte. Public publication and Pages deployment require the exact release/content approval.
