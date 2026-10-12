# Jev-like models

来源：awesome-jev；链接收录与本项目执行证据独立。

| 项目 | 语言 | 描述 | 链接核验 |
|---|---|---|---|
| [laya](cards/nandhakishorm-laya.md) | Python | Multilingual, non-autoregressive System 1 decision engine. Typed decisions over 100+ languages in a single forward pass — 33 ms — trained with reinforcement learning against strictly proper scoring rules (RLCD), with a router that picks the right checkpoint per request. | reachable |
| [SemIf-OpenJev](cards/theoleecj-semif-openjev.md) | Python | Open-model semantic-if engine for local Jev-style decisions. | reachable |
| [SemIf](cards/theoleecj-semif.md) | Python | Semantic ifs from open models, on a 3090 at home. Independent; not affiliated with Jev or TypeSafe. | reachable |
| [kev](cards/jaredpalmer-kev.md) | Python | Trainable family of small Qwen-based Jev-like decision models with typed primitives, datasets, evaluation tools, and local inference. | reachable |
| [NeoHorse-Jev](cards/tokenrhythm-neohorse.md) | Python | Open 4B decision model with prefill-only Choice, Noul, and Score inference over text or one image, plus native, vLLM, and SGLang runtimes. | reachable |
| [jevos](cards/feder-cr-jev.md) | Python | Local 1B CPU decision model with Jev-compatible Noul responses; it returns P(yes) and explicitly rejects Choice and Score. | reachable |
| [Jeff](cards/firelex-jeff.md) | Python | Local Qwen3.5 and Gemma 4 fine-tunes with a Jev-compatible API for typed Choice, Noul, and Score decisions in one forward pass. | reachable |
| [LocalJev](cards/githubnext-localjev.md) | TypeScript | Local Jev-compatible System One API that converts typed questions into DiffusionGemma classification prompts and probabilities. | reachable |
| [von](cards/wfzyx-von.md) | Python | The open-source System One decision model. Sub-15ms, non-autoregressive, local drop-in alternative to TypeSafe Jev. | reachable |
| [Simple Jev](cards/featherless-ai-simple-jev.md) | Python | Open-model Jev-style server that reads next-token logits to return typed choices, rubric scores, and truth judgments. | reachable |
| [deepopen](cards/deepopen-com-deepopen.md) | Python | 非自回归System 1决策引擎，专为结构化类型决策场景设计 DeepOpen Multilingual, non-autoregressive System 1 decision engine. | reachable |
| [laya](cards/receptron-laya.md) | TypeScript | Run Laya, the open-source Jev-compatible System-1 decision model, from Node.js / TypeScript via ONNX Runtime. | reachable |
| [Jeeves](cards/posthog-jeeves.md) | Python | Reasoning Jev-style 9B classifier with a diffusion drafter and compatible API for typed Noul, Choice, and Score decisions. | reachable |
| [Intern-Decision](cards/internlm-intern-decision.md) | Python | Multimodal Qwen3.5 decision models that answer multiple typed Choice, Score, and Noul questions with probabilities in one forward pass. | reachable |
| [openjev-sglang](cards/ekzhang-openjev-sglang.md) | Python | Jev-compatible API server built on open models and SGLang, with prefill-only inference and typed decision endpoints. | reachable |
| [agent-jev](cards/malevrigns-agent-jev.md) | Python | AgentJev-0.6B - a fast 'System One' decision model for AI Agents: feed it any unstructured state (diffs, traces, logs) and structured questions, get calibrated probability distributions back in one ~50ms forward pass. Zero output-token decoding. | reachable |
| [Open-Jev](cards/zefan-cai-open-jev.md) | Python | Open probability decisions with Qwen3.5-2B, Qwen3.5-9B and Qwen3.8-27B. | reachable |
| [rizzo-flow](cards/rizzo-ai-academy-rizzo-flow.md) | Python | The open, local take on Jev: typed decisions from an LLM, without generating a single token | reachable |
| [jeff](cards/logan-markewich-jeff.md) | Python | Self-hosted Jev-compatible System One server backed by GLiNER-family models, with batching and typed question support. | reachable |
| [djev-spark](cards/mmastrac-djev-spark.md) | HTML | DiffusionGemma NVFP4 structured decisions on a DGX Spark: container recipe No repository-level license file was found during review. | reachable |
| [openjev](cards/razorback16-openjev.md) | Python | Open, Jev-compatible System One decision server on DiffusionGemma. | reachable |
| [AnyJev](cards/nokia-applied-research-anyjev.md) | Python | Turn any LLM into a Jev-style decision model: typed decisions, real probabilities, no training. (continue updating). | reachable |
| [imajev](cards/mohit67890-imajev.md) | Python | Local multimodal decision models that answer Jev-compatible typed questions over records, text, and up to two images, with explicit abstention. | reachable |
| [laya-ultrafast](cards/ipenywis-laya-ultrafast.md) | Python | Same as jev-ultrafast but using Laya. | reachable |
| [LLM2Jev](cards/yinsongxu-llm2jev.md) | Python | Adapter that turns local language models into Jev-style Choice, Score, and Noul decision engines with typed probabilities. | reachable |
| [CLM](cards/contrastive-lm-clm.md) | Python | Contrastive language model for one-pass typed decisions and option probabilities. | reachable |
| [OpenJev](cards/siliconlabai-openjev.md) | TypeScript | OpenSource Jev. | reachable |
| [open-jev-fast](cards/lyuyiqi-open-jev-fast.md) | Cuda | Specialized CUDA inference backend for Open-Jev-27B with a drop-in Jev-compatible server, prefix-tree reuse, and checked benchmark artifacts. | reachable |
| [jimothy](cards/andrewprifer-jimothy.md) | TypeScript | Train small, insanely fast local classifiers from Jev-compatible examples. Run locally in your browser or Node.js. | reachable |
| [JevEmbed](cards/hitsz-tmg-jevembed.md) | Python | Framework and fine-tuned embedding models that turn cosine similarities into Jev-style Choice, Score, and Noul probabilities. | reachable |
| [JevK5](cards/allebee-jevk5.md) | Python | Open-weight Jev alternative that returns typed decisions with probabilities in one forward pass. | reachable |
| [OpenDecision](cards/deepanwadhwa-opendecision.md) | Python | Open semantic decision engine implementing Choice, Noul, and Score primitives with a TypeSafe comparison harness. | reachable |
| [open-jev-typed-decision-engine](cards/intikhab49-open-jev-typed-decision-engine.md) | Python | Open reproduction of TypeSafe Jev: a 150M typed decision engine (noul/choice/score in one non-autoregressive pass, calibrated confidence). 0.697 vs Jev's 0.727, 2.5x better calibrated, 4x faster, free. Trains on a Colab T4 in 30 min. | reachable |
| [TypeLLM](cards/typellm-typellm.md) | Python | Type-safe language-model generation and structured decisions. | reachable |
| [solar-mini4-jev](cards/hunkim-solar-mini4-jev.md) | Python | Solar Mini–based local model for Jev-style typed decisions. | reachable |
| [laya-server](cards/1panel-dev-laya-server.md) | TypeScript | Self-hosted API and web interface for Laya decision models with a Jev-compatible API shape. | reachable |
| [Open Medical Jev](cards/feiliuem-open-medical-jev.md) | Python | Frozen open-model medical decision stack that scores each exam option, then uses confidence and conformal gates to auto-release or escalate answers. | reachable |
| [OpenJev-Vision](cards/iambusy-openjev-vision.md) | Python | Open visual decision model that encodes an image once and answers multiple structured questions. | reachable |
| [djev](cards/mmastrac-djev.md) | Python | Jev-style structured decisions on DiffusionGemma: the example server from vLLM PR 57250. | reachable |
| [Valen](cards/liuziyu77-valen.md) | Python | Training stack for a multimodal Jev-like System One model with vision. | reachable |
| [jevify](cards/fidecastro-jevify.md) | Python | Supersimple way to serve LLMs as a Jev-like endpoint. | reachable |
| [jev-forge](cards/zwlijay-jev-forge.md) | Python | Training and inference stack for calibrated Jev-style choice models with dynamic candidate sets. | reachable |
| [OpenSourceJev](cards/sabeel111-opensourcejev.md) | Python | Turning an LLM model into a Jev like System. | reachable |
| [typed-decision-bert](cards/hawkymisc-typed-decision-bert.md) | Python | Unofficial PoC: a BERT-style encoder decision engine behind a typed-decision (noul / choice / score) HTTP API. Not affiliated with TypeSafe. | reachable |
| [open-jev](cards/nico-martin-open-jev.md) | TypeScript | open-jev is a browser-focused TypeScript library for typed decisions: one piece of text (the state) plus any number of typed questions go in, and one forward pass returns a calibrated probability distribution per question. Nothing is generated, so an answer is always one of the options you provided. | reachable |
| [OpenThai-SystemOne](cards/iapp-technology-openthai-systemone.md) | Python | Open Thai-English System One model with Choice inference, calibration, evaluation scripts, and a Jev comparison suite. | reachable |
| [MoJev](cards/molemo-lab-mojev.md) | Python | Open model for typed, calibrated decisions in one forward pass. | reachable |
| [OpenJev](cards/zhangcy122-openjev.md) | HTML | Open probabilistic Choice, Noul, and Score API powered by constrained open-model log probabilities. | reachable |
| [gutsy](cards/kouhxp-gutsy.md) | Python | Local Qwen3.5-0.8B decision model using llama.cpp label probabilities for Noul, Choice, and Score, with a Jev-compatible HTTP endpoint. | reachable |
| [sys1](cards/alvarobartt-sys1.md) | Rust | Rust System One–compatible API for open decision models such as Laya. | reachable |
| [Mica v0.1 4B](cards/akivet-mica-v0-1-4b.md) | Python | Open 4B English/Korean decision model with Jev-compatible Choice, Score, and Noul probabilities plus BF16 and GGUF weights. | reachable |
| [arbiter](cards/0xbakeer-arbiter.md) | HTML | Serve typed-decision (System 1) models — Laya or your own — on NVIDIA GPUs or Apple Silicon, with a Jev-compatible API and coding-agent integrations. | reachable |
| [stuntd](cards/bladedevoff-stuntd.md) | Python | Local Jev-compatible proxy that learns an application’s typed decisions and serves them with a Laya head. | reachable |
| [notjev](cards/9pings-notjev.md) | JavaScript | Super fast Jev like server, model agnostic, working with any OpenAI compatible endpoint. | reachable |
| [open-jev (JoshuaSP)](cards/joshuasp-open-jev.md) | Python | Typed JSON inference with DiffusionGemma, with Every and Jev benchmark results. | reachable |
| [JEV-CPU](cards/leesk212-jev-cpu.md) | Python | Run SemIf (Jev-style semantic-if decisions) on a CPU — no GPU. Reads typed option probabilities straight from an open model in one forward pass, plus a web UI. | reachable |
| [snap](cards/emnlmn-snap.md) | Rust | Local Jev-compatible typed decisions from unstructured state in one forward pass. | reachable |
| [ollaya](cards/ollaya-dev-ollaya.md) | Rust | Local decision-model runner with a Jev-compatible System One API. | reachable |
| [Eikos](cards/caiovicentino-eikos.md) | Python | Open decision models for finance with a Jev-compatible typed API and evaluation runners. | reachable |
| [tev1](cards/togethercomputer-tev1.md) | Python | Open-weight Jev-inspired decision model fine-tuned from Qwen3.5 4B. | reachable |
| [laya-mps](cards/afshinm-laya-mps.md) | Python | Run Jev-style typed decisions locally on your Mac with low RAM usage and fast responses. | reachable |
| [blink](cards/sqliteai-blink.md) | C | High-performance System One model with an embeddable C runtime and WebAssembly support. | reachable |
| [JevAny](cards/weitianxin-jevany.md) | Python | Open Jev-style model and training stack for typed decisions and option probabilities. | reachable |
| [Nemotron_Jev](cards/pst2154-nemotron-jev.md) | Python | Ask typed questions about text or JSON and inspect model-derived probability distributions in a browser. One container runs the model, the original Decision Lab explorer, and a TypeSafe-shaped API. | reachable |
| [open-jev](cards/kyegomez-open-jev.md) | Python | an open-source, from-first-principles reconstruction of the ideas behind TypeSafe AI's Jev, written in pytorch. | reachable |
| [snapjudge](cards/micha0827-snapjudge.md) | Python | Typed decisions (choice / score / yes-no) from local Qwen models on Apple Silicon. Probabilities come straight from the logits, no text generation. TypeSafe-compatible HTTP API, runs on MLX. | reachable |
| [jevper](cards/zhulinchng-jevper.md) | Python | Jev-shaped classification wrapper over OpenAI-compatible clients that returns probabilities and confidence. | reachable |
| [Bev](cards/reza2kn-bev.md) | Python | Local Jevfire-style candidate scoring with ternary models and a System One API; probabilities are candidate-relative. | reachable |
| [Vev](cards/xiaooolong-vev.md) | Python | Qwen3.5-based decision models accepting text and images through a Jev-compatible server, with typed answers from label-token probabilities; weights are non-commercial. | reachable |
| [jev-style](cards/lawrence3699-jev-style.md) | Python | Local 0.8B Jev-style model and compatible server for Choice, Score, and Noul decisions, with agent skills and a Claude Code permission guard. | reachable |
| [JEMM](cards/ypcypc-jemm.md) | Python | Open multimodal decision model that returns candidate probabilities for text and screenshots through a Jev-style Choice, Score, and Noul endpoint. | reachable |
| [WaterSheep](cards/samratduttaofficial-watersheep.md) | Python | Local Jev alternative serving Noul, Choice, Score, and multi-label probabilities through a System One-compatible endpoint. | reachable |
| [open-spark-jev](cards/abhishek085-open-spark-jev.md) | Python | Open local System One implementation for NVIDIA DGX Spark, with a Qwen3-based model, Jev-compatible API, architecture notes, and evaluation tooling. | reachable |
| [poorjev](cards/rupeshpoojary9-poorjev.md) | Python | Local Jev-like System One decision layer that returns typed choices and calibrated confidence without a hosted API. | reachable |
| [OpenJev (xingwudao)](cards/xingwudao-openjev.md) | Python | OpenJev: an independent Jev-inspired System One decision API based on TypeSafe.ai concepts. Choice, score and noul primitives, local mock server, Python and TypeScript SDKs. Real inference planned; not affiliated with TypeSafe AI. No repository-level license file was found during review. | reachable |
| [edgejev](cards/yzfly-edgejev.md) | Python | Local Jev-like typed-decision runtime using ONNX and quantized models for offline CPU inference. | reachable |
| [Malkuth](cards/newfull5-malkuth.md) | Python | Open 2B and 4B multilingual decision models focused on Korean, serving Jev-compatible Choice, Score, and Noul probabilities through Kev. | reachable |
| [OneJev](cards/omnijev-onejev.md) | Python | Open multimodal System One model in four sizes that answers typed questions over screenshots, images, video, or text in one forward pass. | reachable |
| [jev-local](cards/us-jev-local.md) | Python | Local Jev-compatible evaluation server: POST /v1/systemone with typed noul/choice/score, open weights, no waitlist No repository-level license file was found during review. | reachable |
| [TinyJev](cards/ankit-aglawe-tinyjev.md) | Python | Local 596M typed-decision model with its own weights, Choice, Score, and Noul support, and a Jev-compatible System One endpoint. | reachable |
| [Diffusion Jev](cards/hangzhi-diffusion-jev-sglang.md) | Python | Independent DiffusionGemma and SGLang typed-decision server for text and images, with a drawing playground and public evaluation artifacts. | reachable |
| [TetraJev](cards/feiliuem-tetrajev.md) | Python | Local decision stack that fuses four readings from two frozen open models, then uses agreement and calibration gates to answer or abstain. | reachable |
| [Verdict](cards/manavarya09-verdict.md) | Python | Independent multilingual decision model with calibrated answers, abstention, and a Jev-compatible API. | reachable |
