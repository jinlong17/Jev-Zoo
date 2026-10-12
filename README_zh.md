# JevZoo

资源发现、开放权重下载与可复现的多模态决策评测。

An independent catalog and reproducible evaluation toolkit for typed decision models.

目录核验日：2026-10-12。发现源：[heyjunpenn/awesome-jev](https://github.com/heyjunpenn/awesome-jev)，
固定提交 `39854d858fff`；导入 981 个独立资源。
作者报告、已下载、本项目冒烟和正式评测分别显示。

## 模型与下载状态

| Checkpoint / 详细卡片 | 批次 | 下载 | 真实冒烟通过 | 已完成的全量基准 |
|---|---|---|---|---|
| [Qwen/Qwen3.5-2B](docs/models/qwen35-2b.md) | A | downloaded | True | jevbench-public |
| [Qwen/Qwen3.5-4B](docs/models/qwen35-4b.md) | A | downloaded | True | jevbench-public |
| [OmniJev/OneJev-0.8B](docs/models/onejev-08b.md) | A | downloaded | True | jevbench-public |
| [OmniJev/OneJev-4B](docs/models/onejev-4b.md) | A | downloaded | True | jevbench-public |
| [mohit67890/imajev-2b](docs/models/imajev-2b.md) | A | downloaded | True | jevbench-public |
| [mohit67890/imajev-4b](docs/models/imajev-4b.md) | A | downloaded | True | jevbench-public |
| [Cloudflare/clef-flash](docs/models/clef-flash.md) | A | downloaded | True | jevbench-public |
| [h2oai/h2o-lightning-4b](docs/models/h2o-lightning-4b.md) | A | downloaded | True | jevbench-public |
| [Cloudflare/clef](docs/models/clef.md) | B | downloaded | True | jevbench-public |
| [perplexity-ai/pplx-decider-v1-27b](docs/models/pplx-decider-27b.md) | B | downloaded | True | jevbench-public |

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

- [Official: 6](docs/resources/official.md)
- [SDKs & clients: 60](docs/resources/sdks-clients.md)
- [Jev-like models: 83](docs/resources/jev-like-models.md)
- [Frameworks & integrations: 88](docs/resources/frameworks-integrations.md)
- [Agent tooling: 236](docs/resources/agent-tooling.md)
- [Browser & computer use: 77](docs/resources/browser-computer-use.md)
- [Applications: 134](docs/resources/applications.md)
- [Games & simulations: 73](docs/resources/games-simulations.md)
- [Demos & playgrounds: 66](docs/resources/demos-playgrounds.md)
- [Benchmarks & research: 116](docs/resources/benchmarks-research.md)
- [Other lists: 42](docs/resources/other-lists.md)

## 论文与训练

资源目录保存论文及训练入口。共同底座为 Python 3.12 / PyTorch / Transformers /
Datasets / PEFT / Accelerate。实验训练代码保留在 Lab；公开版当前发布稳定 eval 与公开示例。

## 来源与状态

模型卡片保留基座、许可、组件、版本和运行证据。下载不等于正确加载，冒烟不等于正式跑分。
本项目独立于模型发布方。上游目录复用内容的 MIT 署名见 [NOTICE](NOTICE)。
