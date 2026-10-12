# Benchmarks & research

来源：awesome-jev；链接收录与本项目执行证据独立。

| 项目 | 语言 | 描述 | 链接核验 |
|---|---|---|---|
| [NanoJev](cards/tianyucodings-nanojev.md) | Python | Open 0.6B Jev replica with parallel decisions, complete probability distributions, training pipeline, weights, dataset, and live demos. | reachable |
| [jevlike](cards/vinnylarouge-jevlike.md) | Python | Train a small model that chooses among a changing list of text options, one probability per option in a single pass. Includes Doom, chess, and Wikispeedia demos. | reachable |
| [SREGym](cards/sregym-sregym.md) | Python | When enabled for Codex runs, Jev reviews diagnostic tests and incident-resolution submissions from the supplied evidence. | reachable |
| [jev-align](cards/sutro-sh-jev-align.md) | Python | Build calibrated AI Functions from human feedback using Jev and GEPA. | reachable |
| [tasksource](cards/sileod-tasksource.md) | Python | Tasksource recasts hundreds of classification datasets into Jev-compatible typed questions, answers, and procedural training examples. | reachable |
| [jev-visual](cards/hr98w-jev-visual.md) | Python | An educational Jev-like visual inference experiment on Apple Silicon: shared context, direct candidate scoring, and local visual demos. | reachable |
| [Convex Decision Evals](cards/get-convex-convex-evals.md) | TypeScript | Benchmark comparing Jev Choice answers with LLMs on four-option questions about Convex. | reachable |
| [decider](cards/mapika-decider.md) | Python | One-pass typed decisions with calibrated probabilities (System One style model), fine-tuned from Qwen3.5-2B. | reachable |
| [jev-arena](cards/nanmicoder-jev-arena.md) | JavaScript | Jev model introduction and actual measurement: use Choice / Score / Noul to convert natural language into typed judgments and probabilities for classification, scoring and routing; supports comparison of comment marking, speed and results with models such as DeepSeek, including CSV/Excel import, original speed playback and offline reporting.. | reachable |
| [jev-eval-agent](cards/vinilana-jev-eval-agent.md) | HTML | Personal-assistant agent built on Vercel's eve with 100 mocked tools, measuring how many steps it takes when Jev picks the tool versus the LLM. | reachable |
| [reflex](cards/kshetrajna12-reflex.md) | Python | A small open decision model: state + typed questions -> calibrated probabilities. A Jev / System One re-creation on Qwen3.5. | reachable |
| [WindTunnel](cards/nekuda-ai-windtunnel.md) | TypeScript | WebMCP benchmark comparing browser-agent interfaces, with Jev included as one of the evaluated configurations. | reachable |
| [jevbench](cards/fstandhartinger-jevbench.md) | Python | JevBench v1 - a benchmark for Jev-class typed decision models: smart, cheap, fast, reliable, open. | reachable |
| [open-jev (daseinlabs)](cards/daseinlabs-open-jev.md) | Python | One-pass option scoring with a local Gemma 3 4B on Apple silicon via MLX, inspired by jevlike, with a Doom demo. | reachable |
| [jev-dataops](cards/renagao-jev-dataops.md) | Python | An open-source JEV-powered workbench for streaming data selection, quality evaluation, automatic LoRA training and held-out model evaluation. | reachable |
| [jevmlx](cards/bnsd55-jevmlx.md) | Python | Jev-style parallel constrained decisions for any MLX model on Apple Silicon. Typed, schema-valid JSON in one forward pass. | reachable |
| [typesafe-ai-benchmark](cards/iammrduncan-typesafe-ai-benchmark.md) | TypeScript | This is a LLM Gateway that mimics typesafe ai structured output. Like an imposter Jev. | reachable |
| [jev-calibrate](cards/smkrv-jev-calibrate.md) | TypeScript | Calibrate Jev questions against your own labels: tune criteria on labelled examples, confirm on a held-out set, get a verdict per question. Unofficial. | reachable |
| [Verdict-open-jev](cards/heman10x-ngu-verdict-open-jev.md) | Python | Non-autoregressive decision engine on ModernBERT (151M) with calibrated uncertainty (RLCD), TypeSafe AI Jev benchmark audit, and in-browser WebGPU playground. | reachable |
| [mini-jev](cards/r-ms-mini-jev.md) | Python | Mini-Jev: what a Jev-style typed-decision interface looks like on a frozen Qwen3-4B — read the option letter's logits instead of generating JSON. Preregistered experiment, results, teaching bench. | reachable |
| [jev-capability-atlas](cards/zaious-jev-capability-atlas.md) | Python | Independent, evidence-based map of when TypeSafe's Jev actually holds up vs. breaks down — real API-call receipts, not a leaderboard. 中文为主的双语 repo。. | reachable |
| [LitJev](cards/zhengxuyu-litjev.md) | Python | A reproduction of Jev that turns any Qwen model into a fast decision model, serving the same /v1/systemone schema (Choice, Score, Noul) with no training and no generated answer text. | reachable |
| [jev-on-a-laptop](cards/rorshopping-jev-on-a-laptop.md) | Python | Unofficial study: Jev-style parallel typed decisions on stock 1.5B-8B models on an Apple Silicon laptop. Benchmarks, research notes, and a Hugging Face Space demo. | reachable |
| [jev-column-race](cards/goodrahstar-jev-column-race.md) | JavaScript | Jev vs Gemini 3.8 Flash: labelling 1,000 app reviews, 4.1× faster and 7× cheaper. | reachable |
| [open-alternative-jev](cards/ikermoel-open-alternative-jev.md) | Python | Open alternative to Jev: typed, calibrated decisions from any open-weights LLM in one forward pass (HF + vLLM), with benchmarks. | reachable |
| [openjev (zhihz)](cards/zhihz-openjev.md) | Python | Local bilingual probability decisions from context, questions, and candidate answers. Independent research preview inspired by TypeSafe Jev. | reachable |
| [jeval](cards/rlaope-jeval.md) | Python | Measures what your Jev classifier's confidence is really worth, and sets the human hand-off line from what a mistake costs. | reachable |
| [system-one](cards/sgoedecke-system-one.md) | Python | Batched single-token choice inference for open language models, compatible with TypeSafe. | reachable |
| [jev-rag-benchmark](cards/erendikmenn-jev-rag-benchmark.md) | Python | Reproducible benchmark for measuring Jev reranking quality, latency, and cost in RAG. | reachable |
| [system-one-open](cards/mithalouni-system-one-open.md) | Python | Open replica of TypeSafe's Jev: typed calibrated decisions in one forward pass, on Gemma 4 E2B / Gemma 3 270M (Modal). | reachable |
| [jevbetter](cards/olanotolu-jevbetter.md) | Python | A stronger one-pass scorer over a variable list of text options: hashed n-gram encoder, rival-aware attention, gated head, temperature scaling, benchmarked against jevlike. | reachable |
| [TypeAR](cards/zmtomorrow-typear.md) | Python | Type-safe one-decision-per-token decoding engine for autoregressive LLMs, inspired by Jev. | reachable |
| [jev-benchmarks](cards/abdelstark-jev-benchmarks.md) | Python | Probability-aware evaluation for typed decision models: calibration, selective risk, latency, and reproducible benchmarks. | reachable |
| [jev-as-a-judge](cards/danielgshea-jev-as-a-judge.md) | Python | Using Jev as an evaluator. | reachable |
| [Jev_apps](cards/jackzeng-jev-apps.md) | Python | 看看 Jev 能做什么：用中英文讲清热门应用、工作原理和各自优缺点。Explore Jev apps with plain-language examples, explanations, and comparisons. | reachable |
| [dejevu](cards/idovmamane-dejevu.md) | Python | Browser-agent comparison that benchmarks a one-look open-model policy against the Jev demo. | reachable |
| [jevify](cards/altryne-jevify.md) | Python | An agent skill to discover TypeSafe Jev opportunities, design typed questions, and learn from recent community experiments. | reachable |
| [openvons](cards/genai-craft-openvons.md) | Python | Openvons (open-Jev): 有限選択肢に確率で答える判断層 — テキスト / 画像 / 日本語音声コマンド. | reachable |
| [jev_stock](cards/sosopop-jev-stock.md) | Python | An experimental JEV-powered framework for forecasting short-term stock price direction from structured market data. | reachable |
| [jevcal](cards/abhixhek-jevcal.md) | Python | Stop guessing confidence thresholds: calibrate, threshold, and drift-check typed decision models (TypeSafe Jev) against an LLM teacher. | reachable |
| [jevfire](cards/kikoncuo-jevfire.md) | JavaScript | JEV-inspired parallel decisions for CUDA LLMs. One context, many decisions. vLLM API, game-agent examples, and reproducible benchmarks. | reachable |
| [Eikos Arena](cards/caiovicentino-eikos-arena.md) | Python | Reproducible paper-trading arena that gives Eikos and Jev identical market states and typed questions, then compares equity and probability forecasts. | reachable |
| [typesafe-local](cards/aabolfazl-typesafe-local.md) | Python | Inspired by TypeSafe Ai, Ask a local LLM typed questions, get calibrated probabilities instead of text. Structured output without generation or parsing. MLX / Apple Silicon. | reachable |
| [LegalForecastBench](cards/johnhughes3-legalforecastbench.md) | Python | LegalForecast-MTD benchmark alpha and official evaluation workflows. | reachable |
| [jev-korean-benchmark](cards/mahlernim-jev-korean-benchmark.md) | Python | Reproducible early-access evaluation of Jev on Korean understanding and medical text, with runtime and cost evidence. | reachable |
| [jev-lm](cards/y0usaf-jev-lm.md) | TypeScript | A word-level language model whose output layer is Jev: n-gram drafter, Noul chunk verification, bits-per-token eval. | reachable |
| [Decision Index](cards/apolinario-decision-index.md) | Python | Reproduction kit for a 38-benchmark typed-decision index with frozen public-source suites, resumable runners, official scorers, and Jev-compatible HTTP engines. | reachable |
| [daf-jev](cards/docxology-daf-jev.md) | Python | Daf-jev: composable Python toolkit for TypeSafe's Jev (System One) decision API — question builders, confidence gates, evaluator, calibration, CLI, MCP server, agent skill. | reachable |
| [jev-little-airways](cards/lbotinelly-jev-little-airways.md) | HTML | A show-and-tell capability study for Jev, TypeSafe's System One decision model. | reachable |
| [jev-search-rerank-eval](cards/zhuyansen-jev-search-rerank-eval.md) | Python | Does a TypeSafe Jev rerank beat embedding search? Graded relevance eval (9,831 pairs, 164 zh/en queries) over the Agent Skills Hub catalog, with the judge-circularity bias measured. | reachable |
| [jev-ood-calibration](cards/scienthoon-jev-ood-calibration.md) | Python | Reproducible evaluation of Jev calibration on synthetic support tickets and public classification benchmarks. | reachable |
| [jev-chat](cards/adhyaay-karnwal-jev-chat.md) | Python | A chatbot from typed Jev decisions: hierarchical speculative decoding over System One probabilities. | reachable |
| [jev-curate](cards/akashpriyadarshii-jev-curate.md) | Rust | High-throughput synthetic & pretraining dataset sifter powered by TypeSafe AI Jev (api.typesafe.ai). Stream, filter, and score Parquet & JSONL datasets at 1,500+ rows/sec using System One typed decisions (Choice, Score, Noul). | http_404 |
| [jev-harness](cards/antoniocoppe-jev-harness.md) | TypeScript | Decision harness for TypeSafe Jev — confidence gates, shadow mode, recipes, and evals. Claude CLI 48.9s → Jev 1.3s on the same row-filter job. | reachable |
| [openjev (DECRUX9812)](cards/decrux9812-openjev.md) | Python | Open, local reimplementation of a Jev-style decision layer for job postings. | reachable |
| [jev-behavior-study](cards/rinnecoder-jev-behavior-study.md) | Python | Independent Jev 1.13.0 behavior study: report, controlled prompt experiments, raw results, and offline verification. | reachable |
| [jev-dspy-lab](cards/jmanhype-jev-dspy-lab.md) | Python | Reproducible calibration and selective-risk benchmarks for Jev/TypeSafe decisions in DSPy workflows | reachable |
| [system-one-gemma](cards/akash-kamat-system-one-gemma.md) | Python | Open-source Jev-style System One decision model. Gemma 3 270M with a scoring head — fast, calibrated decisions in a single forward pass. No text generation. Inspired by TypeSafe.ai's Jev. | reachable |
| [jev-rerank-bench](cards/anessbelbati-jev-rerank-bench.md) | Python | Can a decision model beat dedicated rerankers? TypeSafe Jev vs Cohere Rerank 4 vs ZeroEntropy zerank-2 vs a chat-model baseline: 14 datasets, every raw API response, bootstrap ranges on every gap. | reachable |
| [jevgpt](cards/bewinxed-jevgpt.md) | TypeScript | A chatbot built on a model that cannot generate text (TypeSafe AI's Jev, driven autoregressively). | reachable |
| [calibre](cards/firassx914-janus.md) | Python | Calibration and confidence-based routing measured on Banking77: 80.2% accuracy at $0.103 per 500 decisions. | reachable |
| [jev-for-engineers](cards/foadsf-jev-for-engineers.md) | Python | Eight minimal working examples of TypeSafe's Jev (a System One model) applied to mechanical and electrical engineering: CAD/CAE/CAM routing, FEM result triage, DFM screening, BOM alignment, hallucination-proof extraction. Zero dependencies. | reachable |
| [jev-sec-bench](cards/gaurav-gosain-jev-sec-bench.md) | Go | Blind security benchmarks for Jev, TypeSafe's System One model: prompt injection and vulnerable code detection, built on jev-go. | reachable |
| [jev-research-eval](cards/jgridifier-jev-research-eval.md) | HTML | Reproducible Jev Ultrafast research-browser eval harness + field note (QC’d cases, suite runner, report generator). Not investment advice. | reachable |
| [trade-jev](cards/justinhe16-trade-jev.md) | Python | Backtest Jev (TypeSafe) as a BUY/SELL/HOLD trader on NQ L10 order-book data. | reachable |
| [mcts-agent](cards/lhemerly-mcts-agent.md) | Python | Discriminative Monte Carlo Tree Search using TypeSafe Jev System One Primitives and Gemini. | reachable |
| [jev-gate](cards/monglong0214-jev-gate.md) | TypeScript | Not every coding task needs your best model. Experimental Jev-powered model routing for Claude Code — V3 prototype runs today, V4 routes at the task boundary. | reachable |
| [jev-exploration](cards/samuelsacco-jev-exploration.md) | Python | Jev (TypeSafe) exploratory thread: claim audit, live demos, and runnable code. | reachable |
| [jev-benchmark](cards/wondertwins-jev-benchmark.md) | Python | Benchmarks and a playground for TypeSafe's Jev (System One) model: chess, and who-is-the-player-talking-to for speech-to-text game NPCs. | reachable |
| [jev-does-not-play-dice](cards/kantahayashiai-jev-does-not-play-dice.md) | JavaScript | Reproducible experiments on Jev probability calibration, uncertainty, and forecast preservation. | reachable |
| [jev-phishing-bench](cards/anisselbd-jev-phishing-bench.md) | Python | Jev (TypeSafe) vs Claude Haiku 4.5 on 2 000 phishing emails: accuracy, calibration, latency, cost. Reproducible benchmark. | reachable |
| [paper-package](cards/completedottech-paper-package.md) | Python | Reproducible Jev research manuscript, evidence, and paper package. | reachable |
| [decisionbridge](cards/grishahq-decisionbridge.md) | HTML | A Jev-inspired decision interface for existing LLMs. Explicit choices, scores, calibration, and review thresholds. | reachable |
| [RISC-jeV](cards/i2cjak-risc-jev.md) | Python | I tortured Jev into being a RISC-V CPU. | reachable |
| [jev-freeform](cards/kesku-jev-freeform.md) | JavaScript | An observable raw-character chat experiment powered entirely by TypeSafe Jev Choice. | reachable |
| [typed-decisions](cards/kotoba-lang-typed-decisions.md) | Python | Jev-shaped typed-decision models with measured latency, accuracy, calibration, and training cost. | reachable |
| [jev-synergy-screening](cards/pistachioaihq-jev-synergy-screening.md) | Python | Jev (TypeSafe System One) × ASReview SYNERGY abstract screening demo — Choice/Noul vs gold labels. | reachable |
| [qwen-rlcd](cards/shamazharikh-qwen-rlcd.md) | Python | Jev-style calibrated decision model (Choice/Score/Noul) on Qwen3.5-0.8B. | reachable |
| [kyotsu-ai-bench](cards/shibadogcap-kyotsu-ai-bench.md) | HTML | AI benchmark on Japan's 2026 Common Test: Jev vs luna-none vs luna-low (static dashboard). | reachable |
| [jev-agent-failure-benchmark](cards/tokentrim-jev-agent-failure-benchmark.md) | Python | Benchmarking Jev (Typesafe.ai) against a strong LLM on the Who&When Pro agent-failure-attribution benchmark (text subset). | reachable |
| [jev-routing-experiment](cards/tokentrim-jev-routing-experiment.md) | Python | Benchmarking TypeSafe's Jev decision model as a cost-efficient LLM router on RouterArena. | reachable |
| [openjev-experiments](cards/zefir1990-openjev-experiments.md) | Python | Experiments with openjev, an open Jev-style option-logit runner, on local models. | reachable |
| [padflow-jev-evals](cards/zsavage8-padflow-jev-evals.md) | Python | Typed-decision benchmark from PadFlow (land development SaaS): schemas, anonymized labeled rows, and a runner for confidence-calibrated models like TypeSafe Jev. | reachable |
| [stuntdouble](cards/reallyartificial-stuntdouble.md) | JavaScript | Drop-in `/v1/systemone` shadow proxy that forwards requests to Jev and local decision models, recording agreement, calibration, latency, cost, and policy-level differences. | reachable |
| [Typesafe_chess_eval](cards/aliceroselia-typesafe-chess-eval.md) | Python | An evaluation of typesafe AI chess. As it turns out, the AI isn't doing really well even though chess is not a particularly open-ended game. Still, it's only a prototype and this probably wasn't optimzied for games. | reachable |
| [jev-spam-eval](cards/bitnovus-jev-spam-eval.md) | Jupyter Notebook | Zero-shot spam filtering with TypeSafe Jev Noul questions, compared with TF-IDF baselines. | reachable |
| [jev-shadcn-lint-eval](cards/blas0-jev-shadcn-lint-eval.md) | JavaScript | A small second eval for shadcn-ui/lint that uses TypeSafe's Jev to judge the linter's own output. | reachable |
| [system-one-adapter-rust](cards/codeitlikemiley-system-one-adapter-rust.md) | Rust | Rust port of TypeSafe system-one-adapter (LLM-backed system_one evaluations). | reachable |
| [jev-deferred-crispification](cards/dnakhoa-jev-deferred-crispification.md) | TeX | Position paper: the Hidden-Markov and fuzzy primitives missing from TypeSafe AI's Jev and System-One decision models. Two lemmas, one principle (Deferred Crispification), one architecture (BSF-S1). | reachable |
| [jev-alpha-bench](cards/gaurav-gosain-jev-alpha-bench.md) | Go | Does Jev predict stock returns from news? It reads the news well; there is no tradeable alpha. Three arms separate reading from recall. | reachable |
| [jev-headline-bench](cards/gaurav-gosain-jev-headline-bench.md) | Go | Can Jev pick the winner of a real headline A/B test? 64.5% across 10,984 Upworthy randomized experiments, 74.7% when the difference was decisive. | reachable |
| [jev-report](cards/hacksing-jev-report.md) | Python | 发明 RLHF 的人，这次做了个不会说话的模型：Jev 独立研究报告。52 页 PDF + 50 条中文实测复现包 + 143 条可回溯数据表. | reachable |
| [jev-playground (hegargarcia)](cards/hegargarcia-jev-playground.md) | TypeScript | Benchmarks Jev against other evaluation models in games with explicit states, legal actions, and measurable outcomes. | reachable |
| [jev-finance-benchmark](cards/hifizz-jev-finance-benchmark.md) | — | Typesafe.ai model jev finance benchmark. | reachable |
| [jev-anotacao-sentencas](cards/lab-dados-jev-anotacao-sentencas.md) | Python | Jev (TypeSafe) vs. Gemini 3.8 Flash vs. GPT-5.6 Luna na anotação estruturada de sentenças do TJSP: qualidade, tempo e custo. | reachable |
| [jev-vs-luna](cards/mameli-jev-vs-luna.md) | Python | Reproducible review-classification comparison measuring Jev and Luna accuracy, latency, and cost. | reachable |
| [jev-lab](cards/menny1337-jev-lab.md) | TypeScript | TypeScript experiments, evaluations, and latency benchmarks for TypeSafe's Jev model. | reachable |
| [misereru-slide-jev](cards/myokoym-misereru-slide-jev.md) | JavaScript | Ongoing Japanese research deck on Jev and System One models, maintained as Markdown slides. | reachable |
| [shade-arena-jev-monitor](cards/nican2018-shade-arena-jev-monitor.md) | Python | Evaluating TypeSafe's Jev as a fast monitor and action gate for agent sabotage in SHADE-Arena, compared with Gemini 2.5 Flash/Pro. | reachable |
| [PocketJev](cards/nullpo-jp-pocketjev.md) | Swift | On-device iPhone visual decision tool using MLX and Qwen3-VL direct option logits. | reachable |
| [jev-jp-address](cards/smasato-jev-jp-address.md) | TypeScript | Jev (TypeSafe) 性能評価プロジェクト — 日本郵便 KEN_ALL をマスタに、AI SDK 経由の Jev が住所のあいまい一致にどこまで使えるかを検証. | reachable |
| [jev-trace-classifier](cards/sypherin-jev-trace-classifier.md) | Python | Application of TypeSafe Jev (noul judgment primitive) on the collusion.wiki corpus: agent vs human page authorship, head-to-head vs local Qwen3.8-Flash-Next. | reachable |
| [jev-secret-detection](cards/teyhouse-jev-secret-detection.md) | Python | Measures how well TypeSafe's RLCD-Jev model spots real secret credentials in file snippets. | reachable |
| [FinancialPredictionJev](cards/thodoh1-financialpredictionjev.md) | Python | Using Jev to test how well it predicts financial markets(just like most llms as of september 2026, it doesnt do that good). | reachable |
| [typesafe-oracles](cards/trophee-bot-typesafe-oracles.md) | JavaScript | Evaluating TypeSafe's System One primitives (Choice/Score/Noul) — where a typed oracle beats an LLM call. | http_404 |
| [jev-pick-and-place-study](cards/tryaksh-jev-pick-and-place-study.md) | Python | A small reproducible MuJoCo pilot comparing Jev, Claude Haiku, and reactive rules for pick-and-place. | reachable |
| [thaiexam-jev-charts](cards/vehas-thaiexam-jev-charts.md) | HTML | Charts: TypeSafe Jev evaluated on Thai standardized exams vs 110 other models. | reachable |
| [jev-calibration-audit](cards/jujumilk3-jev-calibration-audit.md) | Python | Independent API-only calibration audit of TypeSafe AI's Jev decision model | reachable |
| [labs](cards/kiarina-labs.md) | Python | Research workspace containing reproducible TypeSafe Jev evaluation and safety-judgment experiments. | reachable |
| [jev-certify](cards/nikkoxgonzales-jev-certify.md) | Python | Research toolkit applying conformal risk control and prediction-powered inference to certify Jev routing thresholds. | reachable |
| [jevals-data](cards/jevals-jevals-data.md) | — | Independent benchmark data for TypeSafe's Jev (System One model) vs LLMs: accuracy, calibration, cost. Boards + per-decision logs, CC-BY-4.0 | reachable |
| [jev-eval](cards/onlyoneaman-jev-eval.md) | TypeScript | TypeSafe's Jev vs gpt-5.4-mini and gpt-5.6-luna on four public classification sets: cases, per-item answers, scoring, charts | reachable |
| [jev-evaluation](cards/willkelly-jev-evaluation.md) | Python | Adversarial Jev evaluation suite with preregistered predictions, request logs, and reproducible experiment artifacts. | reachable |
| [jev-orderby-bench](cards/yodablocks-jev-orderby-bench.md) | Python | Does ORDER BY over a Jev probability put rows in a defensible order? Independent ranking, calibration and invariant measurements of TypeSafe AI's Jev: passes six pre-registered gates on 360 labeled rows, fails four of six on graded product relevance. | reachable |
| [Jev no ENEM](cards/patryckalves-jev-no-enem.md) | Python | Reproducible evaluation of Jev Choice decisions on 182 valid ENEM 2025 questions, with raw results, accuracy, calibration, and latency analysis. | reachable |
| [jev-skillbench](cards/mohibshaikh-jev-skillbench.md) | Python | Benchmark of Jev as a malicious agent-skill detector on MalSkillBench with verify-and-escalate evaluation. | reachable |
