# JevZoo-Eval v0.1

Python 3.12；参考运行时为 PyTorch、Transformers、Datasets、PEFT、Accelerate、Safetensors。
锁定版本见 `manifests/` 与每次运行的环境记录。先下载全部模型、数据及官方 worker：

```bash
jevzoo fetch --manifest manifests/models.lock.json
jevzoo fetch --manifest manifests/datasets.lock.json
jevzoo fetch --manifest manifests/workers.lock.json
CUDA_VISIBLE_DEVICES=0 jevzoo evaluate --deployment qwen35-4b --suite jevbench-public --profile smoke
CUDA_VISIBLE_DEVICES=0 jevzoo evaluate --deployment qwen35-4b --suite jevbench-public --profile full
jevzoo evaluate --deployment qwen35-4b --suite jevzoo-eval-v0.1 --profile smoke
jevzoo report --run /absolute/path/to/workspace/run
```

| 数据源 | 正式划分 | 请求 / decisions | 标签与协议 |
|---|---|---:|---|
| JevBench | original/easy/hard 公开文件 | 231 / 231 | 仅公开集；复用官方 Brier、10-bin ECE、ordinal MAE、macro accuracy，不生成 sealed/composite 官方分数 |
| Typed Decisions | all/test | 400 / 2,000 | teacher agreement，软 gold 保留 |
| JEVal | test | 11,257 / 11,257 | 中英文、多任务 |
| DecisionBench | eval | 23,900 / 23,900 | 原候选 ID、软分布、numeric ordinal values 保留 |
| MMStar | val | 1,500 / 1,500 | 原图与原题；A/B/C/D 直接选项概率 |
| Sys1Cal-v1 | tiny_cleanvars_parallel_primitives | 365 / 1,095 | 同潜在状态三种表示；score 的期望映射到真值概率，TV/OVL 与离散准确率分开 |
| Banking77 | test | 3,080 / 3,080 | 原作者 GitHub CSV；HF repo 只含 loader |
| CLINC150 | plus/test | 5,500 / 5,500 | 包含 OOS，151 候选 |
| SST-2 | validation | 872 / 872 | test 无 gold，不用于监督评测 |
| BoolQ | validation | 3,270 / 3,270 | Boolean |
| ARC | ARC-Challenge/test | 1,172 / 1,172 | 动态多选 |

首期下载所有公开文件。正式全量运行不接受 `--max-samples`；smoke 默认从完整划分等间隔选 16 个请求。
`--max-samples` 只调整诊断样本，不改变正式分母。

## 输入、读出与评分

`DecisionRequest` 只含 state/questions/assets；gold、teacher 分布、group 与 task 标签留在
`SupervisedExample`，不传给 adapter。候选 ID、Boolean 语义、ordinal 数值与原始顺序显式保存。
支持单 token 全候选 logits，以及多 token 候选完整序列的累计 log likelihood 后归一化；不以 top-k 近似完整概率。
这类概率是候选条件概率，不宣称为未经约束的生成概率。

- Clef：官方 joint head 严格加载，原始 softmax，完整状态先编码再检查上限。
- imajev：官方 Torch + PEFT + decision readout；raw 单次读出。unknown 质量单独保留；指标使用 known 条件分布，不称为无条件概率。
- H2O：官方 formatter 与标签边界的 HF reference；同时记录官方温度与 noul floor 对应结果。性能不代表官方 vLLM。
- OneJev：官方 MMDecisionEngine，sequential fork、debias=1、无 CUDA graphs。
- Perplexity：checkpoint 内官方 autojev + readout；保存官方 temperature，raw 与官方校准分组。
- 基座：冻结模型、完整候选 logits/sequence probability；没有专用 head 的模型不冒充原生 JEV。

通用 NLL、multiclass sum Brier、15-bin ECE、失败率、ordinal MAE 与 request P50/P95 分开记录。
JevBench 原指标另外保存 `official_metrics.json`；可公开复现的集成结果不等于官方完整 leaderboard。
Sys1Cal 是已知概率任务，accuracy/ECE 为 N/A；score 先取期望再映射二元概率。不同基准不合成一个名次。

## 恢复和产物

每请求原子写 receipt；每题都进入结果或 error 分母。运行目录含 manifest、固定样本、receipts、rows、metrics、
分任务指标和报告。`--resume` 必须保持模型、数据、代码、worker、输入选择、硬件入口一致，否则建立新 run。
加载失败独立记录；中断后重跑未完成请求，已记录失败不自动掩盖。未知 cost 保留 null。

计时是包含处理与同步的 client wall time；加载时间独立保存。初次 kernel 初始化与测量条件保留，smoke 延迟不作为正式性能排名。
每次运行只用明确分配的一张 GPU；外部日志与逐样本产物禁止公开导出。

Image JevBench 当前仅 8 个 public_examples，完整资产与协议未就绪，视觉正式路径用 MMStar。
训练数据使用 Typed Decisions train / OneJev-Data；测试标签不参与 checkpoint、阈值或温度选择。

作者模型的训练数据与这些公开题可能有重叠。目录和报告不以公开集准确率证明未见泛化，也不声称各模型训练预算相等。
训练污染是否排除在没有上游证据时记录为 unknown；新训练实验的拆分与去重另行记录。

## 完整结果的执行代码快照

正式 JevBench 结果引用 `fixtures/reproduction/<code_hash>/` 中的精确执行器与锁清单。
这是对应结果的历史参考实现；当前 `src/jev_zoo` 可继续维护。原始 run 保存同一源文件 hash，不能用新实现冒充旧执行器。

```bash
# 在已安装 eval 依赖的环境中，按某个摘要的 protocol.executor_snapshot 选择目录
export JEVZOO_WORKSPACE=/absolute/path/outside/git
PYTHONPATH=fixtures/reproduction/<code_hash>/src python -m jev_zoo.cli \
  --repo fixtures/reproduction/<code_hash> evaluate \
  --deployment qwen35-4b --suite jevbench-public --profile full
```

历史 smoke 的精确源快照不全部可用，摘要相应标明 `exact_source_available=false`；正式结果有完整公开执行器快照。
