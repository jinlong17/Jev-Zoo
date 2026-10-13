# JevZoo

[简体中文](README_zh.md) · [GitHub](https://github.com/jinlong17/Jev-Zoo)

Resource discovery + executable, reproducible inference, evaluation, training and calibration.

Resources can be listed before integration. Catalog inclusion, primary-source review, implementation, smoke and full evaluation are separate evidence.

## Browse the site

English and Chinese homepages, shareable search/filter views, resource details, related assets and platform routes are generated from the existing registry.

```bash
python site/build.py --output /absolute/path/outside/git/jevzoo-site --readmes
python -m http.server 8766 --bind 127.0.0.1 --directory /absolute/path/outside/git/jevzoo-site
```

`http://127.0.0.1:8766/en/` · `http://127.0.0.1:8766/zh/`

Builds need no Node, GPU or commercial API. Static hosting subpaths are supported; deployment follows the exact-release approval contract.

## Resources and evidence

981 discovery records · 1103 canonical resources · 144 primary-source/local-recipe evidence records.

| Type | Count |
|---|---:|
| Applications & demos | 351 |
| Benchmarks | 103 |
| Agent components | 236 |
| Data | 10 |
| Discovery lists | 42 |
| Frameworks | 102 |
| Models | 126 |
| Papers | 48 |
| Recipes | 2 |
| Services | 5 |
| Tools & SDKs | 78 |

10 implemented checkpoints · 11 implemented tasks · 10 approved full-public summaries.

Full evaluation covers the named split and its error denominator; it does not imply every task passed. JevBench public excludes sealed tasks and the official composite.

## Inference and evaluation

```bash
python -m pip install '.[eval]'
export JEVZOO_WORKSPACE=/absolute/path/outside/git
jevzoo evaluate --deployment qwen35-4b --suite jevbench-public --profile smoke
jevzoo report --run /absolute/path/to/run
```

[Evaluation protocol](docs/evaluation.md) · [Model cards](docs/models/qwen35-4b.md) · [Result summaries](results/published/README.md)

## Training and calibration

The Lab retains full training code. R1 language LoRA and an R2 candidate head have real-gradient/reload smoke; formal gains, cross-source near-duplicate audits and four-role split review remain pending. Calibration never fits test labels.

[Lab training docs (access required)](https://github.com/jinlong17/Jev-Zoo-Lab/blob/main/docs/training.md)

## Maintenance and publication

[Site build and maintenance](site/README.md) · [NOTICE](NOTICE)

Commercial resources are browsable; commercial inference is disabled, with no budget cap in this task. Models, data, checkpoints, logs and row-level artifacts stay outside Git; public export includes allowed metadata and exactly approved summaries.

Discovery: [heyjunpenn/awesome-jev](https://github.com/heyjunpenn/awesome-jev/tree/39854d858fff73bf3172949c9f968c6cb12beafa) · MIT · 2026-10-12
