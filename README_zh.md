# JevZoo

[English](README.md) · [GitHub](https://github.com/jinlong17/Jev-Zoo)

资源展示与发现平台 + 可执行、可复现的推理、评测、训练与校准平台。

资源可以先展示，再逐步适配。收录、一手核验、接入、smoke 与全量评测分别记录。

## 浏览主页

中英文主页、可分享的搜索筛选、资源详情、关联资产与训练评测入口均由现有注册表生成。

```bash
python site/build.py --output /absolute/path/outside/git/jevzoo-site --readmes
python -m http.server 8766 --bind 127.0.0.1 --directory /absolute/path/outside/git/jevzoo-site
```

`http://127.0.0.1:8766/en/` · `http://127.0.0.1:8766/zh/`

构建不依赖 Node、GPU 或商业 API。静态主机子路径兼容；部署需沿用具体 release 审批。

## 资源与证据

发现 981 条 · 去重收录 1103 项 · 一手来源 / 本地配方证据 144 项。

| 类型 | 数量 |
|---|---:|
| 应用与演示 | 351 |
| 基准 | 103 |
| Agent 组件 | 236 |
| 数据 | 10 |
| 资源索引 | 42 |
| 框架 | 102 |
| 模型 | 126 |
| 论文 | 48 |
| 配方 | 2 |
| 商业服务 | 5 |
| 工具与 SDK | 78 |

已接入 10 个 checkpoint · 已实现 11 个任务 · 已批准 10 份全量公开集摘要。

全量是注明基准的完整分母，包含错误记录；不表示所有任务通过。JevBench public 不包含 sealed 或官方 composite。

## 运行推理与评测

```bash
python -m pip install '.[eval]'
export JEVZOO_WORKSPACE=/absolute/path/outside/git
jevzoo evaluate --deployment qwen35-4b --suite jevbench-public --profile smoke
jevzoo report --run /absolute/path/to/run
```

[评测协议](docs/evaluation.md) · [模型卡](docs/models/qwen35-4b.md) · [结果摘要](results/published/README.md)

## 训练与校准

Lab 保留完整训练实现。R1 语言 LoRA、R2 candidate head 已有真实梯度与重载 smoke；正式收益、跨源近重复审核及四角色划分仍需完成。校准不使用 test 标签。

[Lab 训练文档（需权限）](https://github.com/jinlong17/Jev-Zoo-Lab/blob/main/docs/training.md)

## 数据维护与发布

[网站构建与维护](site/README_zh.md) · [NOTICE](NOTICE)

商业资源可展示，当前商业推理禁用，不设置本次预算上限。模型、数据、checkpoint、日志和逐样本产物留仓外；公开只导出允许的元数据和具体批准的摘要。

Discovery: [heyjunpenn/awesome-jev](https://github.com/heyjunpenn/awesome-jev/tree/39854d858fff73bf3172949c9f968c6cb12beafa) · MIT · 2026-10-12
