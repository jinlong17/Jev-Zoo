# Agent tooling

来源：awesome-jev；链接收录与本项目执行证据独立。

| 项目 | 语言 | 描述 | 链接核验 |
|---|---|---|---|
| [claude-code-templates](cards/davila7-claude-code-templates.md) | Python | Claude Code configuration toolkit shipping Jev-based model routing, skill suggestion, and tool guardrail modules. | reachable |
| [openwork](cards/different-ai-openwork.md) | TypeScript | Open-source Claude Cowork alternative whose eval testkit can use Jev as a typed verification judge for agent-produced work. | reachable |
| [fast-jev-compaction](cards/tamaratran-fast-jev-compaction.md) | TypeScript | Claude Code plugin that replaces the compaction summary with Jev decisions: every tool call and result is scored in one fast request, stale ones are dropped or truncated, everything kept stays verbatim. | reachable |
| [memsearch](cards/zilliztech-memsearch.md) | Python | Agent memory search with optional Jev relevance judgments to rerank retrieved passages. | reachable |
| [agentconnect](cards/agentconnect-md-agentconnect.md) | TypeScript | Team agent workspace using Jev typed decisions for response routing and model selection. | reachable |
| [jevgrep](cards/dzhng-jevgrep.md) | TypeScript | Semantic code-search CLI for coding agents; Jev selects relevant repository branches, files, and source units for a natural-language behavior query. | reachable |
| [distill](cards/samuelfaj-distill.md) | Rust | Coding-agent runtime using Jev decisions for model routing, context retention, and tool selection. | reachable |
| [vexjoy-agent](cards/notque-vexjoy-agent.md) | Python | VexJoy AI Agent with Jev Intelligent Routing - /do routes plain-English requests to the right specialist agent and gates the work with reviews, tests, and a learning loop. | reachable |
| [foreman](cards/thruwire-foreman.md) | Python | Software Factory Foreman: an agent supervisor that uses Jev decisions to keep coding agents on task. | reachable |
| [jev-review (devagrawal09)](cards/devagrawal09-jev-review.md) | TypeScript | A staged code-review workflow and local dashboard built with TypeSafe Jev. | reachable |
| [hermes-jev-skills](cards/kerpopule-hermes-jev-skills.md) | Python | Hermes plugin and skill suite using Jev for model routing, skill selection, memory filtering, compaction, and GUI actions. | reachable |
| [mu](cards/qybaihe-mu.md) | TypeScript | Coding-agent workspace where Jev or a local Laya judge gates bounded decisions such as context retention, approvals, routing, drift, and inter-agent sharing. | reachable |
| [Keel](cards/codejunkie99-keel.md) | Rust | Local-first coding workspace where Jev or Laya selects an eligible agent/model route and the host validates every choice before execution. | reachable |
| [jev-search](cards/superagents-lab-jev-search.md) | TypeScript | Search the web with TypeSafe's Jev: source selection, query understanding and relevance ranking. Built with Search1API. | reachable |
| [decapod](cards/decapodlabs-decapod.md) | Rust | During assurance evaluation, Jev estimates how likely a proposed agent trajectory is to satisfy its bounded objective. | reachable |
| [Albatross](cards/morganlinton-albatross.md) | Rust | Open source, terminal-first AI coding agent with fully transparent multi-model routing. Local (Ollama, LM Studio, MLX, llama.cpp) or cloud, your keys, one TUI. No black box. | reachable |
| [jev-router (gargpratyush)](cards/gargpratyush-jev-router.md) | JavaScript | Route to the cheapest model in claude code for your task using jev-router. | reachable |
| [jev-gateway](cards/vinilana-jev-gateway.md) | TypeScript | An easy way to use jev with your coding agent for tool calling reasoning. | reachable |
| [Astra-Ares](cards/miuuyy-astra-ares.md) | JavaScript | Adaptive reasoning effort for GPT-6 Astra during Codex tasks, powered by Jev to reduce token usage. | reachable |
| [compact-adviser](cards/kunchenguid-compact-adviser.md) | TypeScript | Agent plugin that uses Jev to judge when a coding session should compact its context. | reachable |
| [jev-review (NiazMorshed2007)](cards/niazmorshed2007-jev-review.md) | TypeScript | Local-first MCP plugin for continuous software-quality review by AI coding agents, powered by Jev. | reachable |
| [abide](cards/coldteadotai-abide.md) | TypeScript | Supervises coding-agent edits and uses Jev to flag violations of project rules. | reachable |
| [glowbom-oss](cards/glowbom-glowbom-oss.md) | Go | Coding agents can ask Jev to judge small workflow decisions, such as whether build results look healthy. | reachable |
| [Anna-Agent](cards/foxtailsss-andy-anna-agent.md) | TypeScript | Anna uses Jev as a fast judgment layer for bounded enterprise-agent recommendations and abstentions. | reachable |
| [jev-pruner](cards/tamaratran-jev-pruner.md) | TypeScript | Claude Code and Codex hooks that ask Jev which parts of long shell output remain relevant before sending them into model context. | reachable |
| [jev-semgrep](cards/uehaj-jev-semgrep.md) | JavaScript | grep by meaning, across languages. TypeSafe Jev scores every line against a meaning; combine meanings with AND/OR/NOT. 意味で探す grep。日本語で英語を、英語で日本語を検索できる | reachable |
| [jev-mcp (jkudish)](cards/jkudish-jev-mcp.md) | TypeScript | Proof of concept MCP for Typesafe's new Jev AI model. | reachable |
| [building-with-jev-skill](cards/dbreunig-building-with-jev-skill.md) | — | A skill for writing and improving programs that call Jev, TypeSafe's System One model. | reachable |
| [typesafe-mcp](cards/itsmostafa-typesafe-mcp.md) | Go | Go CLI and single-binary MCP server exposing TypeSafe judgments to Claude Desktop, Claude Code, and Codex. | reachable |
| [stanley-code](cards/devagrawal09-stanley-code.md) | TypeScript | Bounded TypeSafe Jev workflows for coding agents. | reachable |
| [supercov](cards/supercorp-ai-supercov.md) | Rust | Code-quality and coverage reviewer that uses Jev to judge coding-agent changes. | reachable |
| [deepseek-harness-jev](cards/luobosibing2-dsh-jev-plugin.md) | JavaScript | DeepSeek Harness plugin using Jev for skill and file selection, task supervision, output filtering, and approval assistance; features are disabled by default. | reachable |
| [pi-warden](cards/devmortimer-pi-warden.md) | TypeScript | Guardrails for Pi built on pi-typesafe that steer the agent instead of interrupting you: Jev judges irreversible and off-task tool calls, detects stuck loops, checks unverified done claims, flags slop. | reachable |
| [Building with TypeSafe Jev](cards/aaddrick-building-with-typesafe-jev.md) | Python | Installable agent skill that teaches Jev typed-decision design, validates live API shapes, and indexes reusable patterns from community projects. | reachable |
| [pi-jev (y0usaf)](cards/y0usaf-pi-jev.md) | TypeScript | TypeSafe Jev as a decision layer for the Pi coding agent: a measured tool-call gate plus jev_ask for typed, calibrated answers. | reachable |
| [jevmem](cards/avinash-jetwani-jevmem.md) | TypeScript | Project-memory tooling for coding agents; Jev decides which turns to save, their kind, contradictions, recall relevance, and suspected memory poisoning. | reachable |
| [JevRouter](cards/billionsbobby-jevrouter.md) | TypeScript | A lightweight Jev-powered router for models, tools, and subagents. | reachable |
| [skills](cards/fabricioctelles-skills.md) | Python | Four agent skills use Jev Score and Noul judgments to assess subjective criteria with calibrated probabilities. | reachable |
| [jev-codex-router](cards/0xnatoshi-jev-codex-router.md) | Python | Per-turn model & reasoning routing for Codex, driven by Jev (TypeSafe System One): picks the model, thinking depth and speed mode for every turn. | reachable |
| [jev-code](cards/devagrawal09-jev-code.md) | TypeScript | Bounded TypeSafe Jev workflows for coding agents. | reachable |
| [Quicksilver](cards/uditakhourii-quicksilver.md) | JavaScript | Claude Code skill and CLI that delegates bulk ranking, classification, filtering, and semantic-search judgments to Jev. | reachable |
| [captaincore](cards/captaincore-captaincore.md) | Go | Jev triages malware-scan findings and supplies typed Noul, Choice, and Score decisions for WordPress maintenance. | reachable |
| [grok-bot-jev](cards/bodila51-grok-bot-jev.md) | Python | Grok Bot integration where Jev applies usage gates and routes requests before the generative model runs. | reachable |
| [skillranker](cards/dicklesworthstone-skillranker.md) | Rust | Rust CLI powered by Jev from TypeSafe.ai that ranks agent skills for the next step using live session context. Includes Claude Code hooks, structured JSON, abstention, and local feedback. Requires a TypeSafe API key. | reachable |
| [total-agent-memory](cards/vbcherepanov-total-agent-memory.md) | Python | Jev checks retrieved memories for contradictions before an agent uses them in an answer. | reachable |
| [save-token-jev-clean](cards/iamunbounded-save-token-jev-clean.md) | TypeScript | Portable, Jev-guided context compaction for coding agents. | reachable |
| [jmeter-ai](cards/qainsights-jmeter-ai.md) | Java | Jev classifies JMeter agent intent and selects a focused tool pack, with a full-tool fallback when routing is uncertain. | reachable |
| [weflow-cli](cards/zhuobichen-weflow-cli.md) | Python | When enabled, Jev classifies article topics and relevance for WeChat daily digests. | reachable |
| [agent-router](cards/nidhi-singh02-agent-router.md) | TypeScript | CLI that uses Jev task classification to choose and launch Cursor, Claude Code, Codex, or OpenCode with an appropriate model and effort level. | reachable |
| [oxlint-plugin-jev](cards/wobsoriano-oxlint-plugin-jev.md) | TypeScript | &gt; This package is experimental. Use at your own risk. | reachable |
| [jegrep](cards/can1357-jegrep.md) | Rust | Semantic grep CLI where Jev judges which files and exact line ranges match a natural-language code query. | reachable |
| [jev-lint](cards/mizchi-jev-lint.md) | TypeScript | Text linter that uses Jev Score judgments to evaluate strings embedded in source code against configurable writing rules. | reachable |
| [Canny](cards/qkal-canny.md) | TypeScript | Stops AI coding agents from claiming work is done without evidence. Deterministic hooks decide, TypeSafe's Jev advises. Append-only ledger, zero runtime dependencies. | reachable |
| [jev-recruiter](cards/skeptrunedev-jev-recruiter.md) | Python | A Jev powered LinkedIn recruiting agent. Watch it browse relevant profiles, save links, and review evidence against your hiring brief. | reachable |
| [jev-rules](cards/eliaalberti-jev-rules.md) | JavaScript | Claude Code plugin where Jev decides which project rules apply to each prompt and edited file. | reachable |
| [jev-sift](cards/kbhuw-jev-sift.md) | JavaScript | Agent plugin and MCP tool where Jev classifies batches of text so agents can read only the relevant items. No repository-level license file was found during review. | reachable |
| [duet-agent](cards/dzhng-duet-agent.md) | TypeScript | Full-stack agent harness with memories, long-running tasks, multi-agent relay, and a Jev-backed model-routing table. | reachable |
| [hono-jev-router](cards/yusukebe-hono-jev-router.md) | TypeScript | Route HTTP requests by meaning. A semantic router for Hono powered by Jev. | reachable |
| [JevRev](cards/alex314618-create-jevrev.md) | TypeScript | An LLM + Jev workflow. Boost your vertebrate brain with a spine inside. | reachable |
| [skilled-agent-harness_spec-driven-loops](cards/michelkerkmeester-skilled-agent-harness-spec-driven-loops.md) | TypeScript | The cli-jev transport routes typed-judgment requests from the skill harness to the Jev CLI and MCP interfaces. | reachable |
| [jev-dsh-decision](cards/devin-axis-jev-dsh-decision.md) | JavaScript | Decision plugin for DeepSeek Harness and iPolloWork that lets OpenCode, Codex, and other agents use Jev to select tools, skills, and task owners and evaluate outputs. | reachable |
| [ask-jev-skill](cards/shantanugoel-ask-jev-skill.md) | Python | Skill for Hermes, and other agents, to ask typesafe's jev. | reachable |
| [Jev-Mem](cards/libingzheren-jev-mem.md) | Python | Jev-Mem: System-One Controlled Agentic Memory. | reachable |
| [obsidian-llm-hub](cards/takeshy-obsidian-llm-hub.md) | TypeScript | Obsidian plugin for AI chat, workflow automation, and semantic search — supports Gemini, OpenAI, OpenRouter, Grok, Ollama, and CLI backends. | reachable |
| [jev-skill-suggester](cards/win4r-jev-skill-suggester.md) | Python | 用 TypeSafe Jev 推荐已安装 Skill / Bounded installed-skill recommendations with TypeSafe Jev. Python CLI, Codex skill, bilingual docs and live examples. | reachable |
| [pi-jev-skill-picker](cards/safzanpirani-pi-jev-skill-picker.md) | TypeScript | Rank Pi Agent Skills for the current task with TypeSafe Jev. | reachable |
| [jevgrep](cards/nassim-arifette-jevgrep.md) | TypeScript | Semantic code search CLI and MCP server: Jev scores authorized repository excerpts and returns exact file paths and line numbers to coding agents. | reachable |
| [ai-news-aggregator](cards/flyryan-ai-news-aggregator.md) | Python | Multi-agent AI news pipeline powered by GLM-5.3-Flash and Jev. | reachable |
| [winnow](cards/ghalebdweikat-winnow.md) | Python | A calibrated context sieve for Claude Code: every tool result is judged by a System One model before it enters context. | reachable |
| [jev-judge-mcp](cards/pymodel-jev-judge-mcp.md) | Python | MCP tools that expose Jev for verification, screening, classification, reranking, review, gating, and scoring. | reachable |
| [jev-permission-gate](cards/madisonrickert-jev-permission-gate.md) | TypeScript | Claude Code mod that asks Jev Noul questions about tool-call intent and risk, then allows, denies, or defers to the built-in classifier under explicit thresholds. | reachable |
| [snifftest](cards/danrwilloughby-snifftest.md) | TypeScript | A prose linter that sniffs out AI writing tells. Zero dependencies, countable rules plus one judgment model. | reachable |
| [jev-use](cards/shitianfang-jev-use.md) | JavaScript | Claude Code / Codex / pi plugin that hands agent steps needing no text output to Jev (TypeSafe's judgment model) — measured p50 ~230 ms and ~$0.02 per 1,000 judgments, with typed escalation back to the LLM. | reachable |
| [agent-chaperone](cards/agent-chaperone-agent-chaperone.md) | TypeScript | MCP proxy that uses Jev to screen agent tool calls and tool results. | reachable |
| [jev-agent-design-with-topk-logits-choices](cards/6mikao9-jev-agent-design-with-topk-logits-choices.md) | Python | Jev-native agent design with top-k proposals, fallback decisions, memory, and replanning. | reachable |
| [pi-advisor](cards/philipbrembeck-pi-advisor.md) | TypeScript | Customizable Advisor and Executor workflow for Pi with Jev decision support. | reachable |
| [jev-mcp (burnigtm)](cards/burnigtm-jev-mcp.md) | TypeScript | MCP server that puts TypeSafe Jev on the coding loop in Cursor, Codex, and any MCP client. | reachable |
| [ErisLint](cards/eriskii-erislint.md) | Rust | Rust linter powered by configurable Jev rules, with a VS Code extension. | reachable |
| [Multi-Agent](cards/masonlee39-multi-agent.md) | TypeScript | Multi-agent orchestration engine with warm sessions, a durable mailbox, and per-task token accounting. | reachable |
| [yoshi](cards/compozy-yoshi.md) | TypeScript | Context-pruning proxy for Claude Code and Codex: Jev judges which history is still needed, measured not claimed. POC here now, heading soon into [Compozy](https://github.com/compozy/compozy). | reachable |
| [pi-jev (TheoOliveira)](cards/theooliveira-pi-jev.md) | TypeScript | Semantic tool routing and typed System One decisions for the Pi coding agent using TypeSafe Jev. | reachable |
| [cnki-skills](cards/longkou1988-cnki-skills.md) | Python | The optional cnki-jev package uses Jev for first-pass literature screening and escalates complex cases for model or human review. | reachable |
| [pi-jev-auto-mode](cards/jomatsu-pi-jev-auto-mode.md) | TypeScript | Jev (TypeSafe System One) backed auto mode for the Pi coding agent: semantically auto-approves bash, write, and edit tool calls and fails closed when a decision cannot be made. | reachable |
| [jev-axi](cards/shiftynick-jev-axi.md) | TypeScript | Agent-ergonomic CLI for TypeSafe's Jev: fast calibrated judgments (pick, rate, check, rank, triage, guard) from the shell. | reachable |
| [oh-my-harness](cards/kyu1204-oh-my-harness.md) | TypeScript | Tame your AI coding agents with natural language. Generate enforced guardrails (CLAUDE.md, hooks, settings) from a single command. | reachable |
| [zero-api-key-web-search](cards/wd041216-bit-zero-api-key-web-search.md) | Python | Jev-powered search infrastructure for AI agents: zero API keys, MCP-ready, LLM-context aware, with local neural evidence verification. | reachable |
| [dsh-jev](cards/buberlo-dsh-jev.md) | TypeScript | Jev-powered decision layer for DeepSeek Harness. | reachable |
| [a3m-router](cards/das-rebel-a3m-router.md) | TypeScript | ⚡ Adaptive multi-model LLM router — 80+ providers, Jev System One single-pass routing (model=jev-auto), pheromone-trail failover, parallel ensemble merge. npm: adaptive-memory-multi-model-router. | reachable |
| [jgrep](cards/kyu1204-jgrep.md) | TypeScript | grep for what code does, not what it's called. Semantic code search powered by TypeSafe Jev. | reachable |
| [jev-cli](cards/shaharia-lab-jev-cli.md) | Rust | Command-line tool for TypeSafe AI's Jev model. Ask yes/no, multiple-choice and rubric questions about any text and get calibrated probabilities back. Answers become exit codes for shells and CI, JSON for scripts, and MCP tools for AI agents. | reachable |
| [JevLoop](cards/zjunlp-jevloop.md) | TypeScript | The agent loop where decisions don't cost a large language model call. Zero deps, runs offline, no API key needed. | reachable |
| [deepreseach-learing](cards/1612535983-deepreseach-learing.md) | Python | Jev runs in shadow mode to append structured quality evaluations to generated deep-research reports. | reachable |
| [jev-test-filter](cards/mizchi-jev-test-filter.md) | TypeScript | Score every test against a git diff with Jev, and emit the filter arguments vitest, node:test, Playwright, cargo test and go test already understand. | reachable |
| [jevvy](cards/panachy-jevvy.md) | TypeScript | Jev-powered plugins for coding agents. | reachable |
| [pi-review](cards/zephyrdeng-pi-review.md) | TypeScript | Jev screens likely defects, arbitrates ambiguous findings, classifies scope, and supports cross-round review memory. | reachable |
| [is-malicious](cards/luantak-is-malicious.md) | TypeScript | Scans a codebase for covert, deceptive, or data-stealing behavior with Jev, then reports suspicious files and line ranges before the user runs it. | reachable |
| [pi-jev-router (philippdubach)](cards/philippdubach-pi-jev-router.md) | TypeScript | Pi model router that uses Jev task classification and a measured Pareto frontier over quality, cost, and latency to select an OpenRouter model. | reachable |
| [patdown](cards/tyler-dot-earth-patdown.md) | TypeScript | Block, steer, and "fuzzy lint" with Jev to make agents follow your rules and conventions. CLI, github action, pi package, and more. Built with Effect. | reachable |
| [MetaCog](cards/itiscuthnotcup-metacog.md) | Python | MetaCoginition powered by Reflex 4B. | reachable |
| [Tiermem](cards/freedomintelligence-tiermem.md) | Python | The Jev integration routes agent memory queries between compact Markdown notes and searchable raw history. | reachable |
| [azdaja](cards/kubet-azdaja.md) | Python | Azdaja exposes optional Jev semantic judgments inside a bounded local evaluation surface. | reachable |
| [jevyoumean](cards/syumai-jevyoumean.md) | Go | Semantic "Did you mean?" for any CLI — wraps commands and uses TypeSafe's Jev to match subcommand typos by intent, not edit distance. | reachable |
| [jgrep](cards/keltokhy-jgrep.md) | Python | Grep, but the pattern is a description. Filters lines by meaning with TypeSafe's Jev decision model: ~200 ms and a thousandth of a cent per line. | reachable |
| [jev-code](cards/francoischastel-jev-code.md) | TypeScript | Jev, TypeSafe's System One classifier, as a tool inside Claude Code, Codex, Pi, and OpenCode: typed classify, check, score, rank, and ask, plus one-command setup. | reachable |
| [jevcore](cards/perrylink-jevcore.md) | TypeScript | TypeSafe Jev for DeepSeek Harness, the Model Context Protocol, and plain Node: typed judgments instead of prose, offline by default. | reachable |
| [claude-jev](cards/0x7067-claude-jev.md) | Python | Claude Code plugin that uses Jev for rule checks, verbatim compaction, and prompt routing. | reachable |
| [lintus](cards/virolea-lintus.md) | Rust | Natural-language linter that uses Jev to evaluate code against plain-language rules. | reachable |
| [jev-seo](cards/akashpriyadarshii-jev-seo.md) | Rust | Agent-first SEO and GEO CLI suite and MCP server using DuckDuckGo evidence and Jev scoring. | http_404 |
| [jev-mcp (blakestone-x)](cards/blakestone-x-jev-mcp.md) | Python | MCP server for TypeSafe Jev: typed classify, score, check, match and screen for any agent, with confidence on every answer. | reachable |
| [jev-cli (Nasrallah-AL)](cards/nasrallah-al-jev-cli.md) | TypeScript | Command-line tool for TypeSafe's Jev AI model. | reachable |
| [slop-grader](cards/lukstei-slop-grader.md) | TypeScript | Jev-powered, rule-based grader for text files. Runs every rule against every line in parallel. No skimming, no missed lines. | reachable |
| [cmd-mod-jev-nudge](cards/commandcodeai-cmd-mod-jev-nudge.md) | TypeScript | Command Code mod: nudges the agent to keep going when it stops with work left, judged by Jev. | reachable |
| [eutrya](cards/hellozenstrategist-lab-eutrya.md) | JavaScript | Jev-native AI security harness for autonomous research, multi-agent swarms, persistent hunt boards, and long-running agent workflows. CLI-first, open source, and built for authorized security research. | reachable |
| [pi-jev](cards/madeye-pi-jev.md) | TypeScript | Jev-assisted file retrieval and request caching for faster Pi workflows. | reachable |
| [zevals](cards/opencx-labs-zevals.md) | TypeScript | Jev judges yes-or-no assertions about an agent transcript, and the test passes when its probability reaches the configured threshold. | reachable |
| [pi-jev-router](cards/win4r-pi-jev-router.md) | TypeScript | Task-boundary model routing for Pi Coding Agent, powered by TypeSafe Jev. Conservative policies, exact caching, and observable failover. | reachable |
| [jev (BorisLeMeec)](cards/borislemeec-jev.md) | Go | A claude code plugin for jev. | reachable |
| [jevwire](cards/brainwires-jevwire.md) | TypeScript | Jev decision layer for agents: MCP server, embeddable DecisionModel library, and an escalate-only Claude Code plugin (TypeSafe AI's Jev). | reachable |
| [JevLint](cards/huntedman-jevlint.md) | TypeScript | Configurable semantic linting powered by Jev, with file-level NOUL judgments and a magic-strings plugin. | reachable |
| [jev-guard](cards/leepokai-jev-guard.md) | JavaScript | Prompt-injection and dangerous-action guard for coding agents (Claude Code, Codex, pi, ACP), powered by Jev. | reachable |
| [jcr](cards/niazmorshed2007-jcr.md) | JavaScript | Jev Capability Resolver: agents query a nested capability tree and receive only the deterministic commands and context relevant to the task. | reachable |
| [evoke](cards/evoke-build-evoke.md) | Rust | Software, by reflex. A sentence becomes a call of a small program, chosen by Jev, TypeSafe AI's classifier, and run only when it is sure enough. Reflexes are recipes anyone can write, share and improve. A CLI you talk to, a package manager for reflexes from git, and a TypeScript SDK. | reachable |
| [liteagents](cards/berriai-liteagents.md) | Python | Provider-independent agent SDK that uses typed routing to select a model for each turn. | reachable |
| [jev-belay](cards/valentynkit-jev-belay.md) | JavaScript | Claude Code Stop hook that asks four Jev questions when files changed without a passing check, blocking unverified completion claims while failing open on errors. | reachable |
| [hermes-jev-approvals](cards/anpicasso-hermes-jev-approvals.md) | Python | PoC: TypeSafe Jev as the reviewer for Hermes Agent smart command approvals. 8.7x faster, 4.4x fewer prompts, measured on 153 real commands. Approvals only. | reachable |
| [typesafe-skill-router](cards/decrux9812-typesafe-skill-router.md) | Python | TypeSafe (Jev) skill routing for Hermes Agent: names the one skill worth loading, before the model call. Opt-in, stdlib only, ~$0.001 per routed turn. | reachable |
| [jev-agent-skill-router](cards/godsboy-jev-agent-skill-router.md) | Python | Typed, confidence-aware agent skill routing with TypeSafe Jev. | reachable |
| [pi-quiet-ask](cards/hyunjunjeon-pi-quiet-ask.md) | TypeScript | TypeSafe Jev as the pi coding agent's quiet decision layer. | reachable |
| [hermes-jev](cards/keeltrace-hermes-jev.md) | Python | Typed System One decisions, ranking, verification, and an opt-in Hermes tool gate using TypeSafe Jev. | reachable |
| [jev-router](cards/rajdhakad9826-jev-router.md) | TypeScript | LLM router that picks the cheapest model capable of handling a query, using TypeSafe's Jev for fast classification instead of an LLM call. | reachable |
| [omp-jev-compaction](cards/jerryfane-omp-jev-compaction.md) | TypeScript | Verbatim Jev-scored context reduction for omp, over TypeSafe or OpenRouter. | reachable |
| [pi-jev-router](cards/mejiasd3v-pi-jev-router.md) | JavaScript | Automatic model routing for Pi using TypeSafe's Jev through Vercel AI Gateway. | reachable |
| [clean-code-review](cards/frostney-clean-code-review.md) | TypeScript | Every code file in a pull request, judged against Uncle Bob's Clean Code by TypeSafe's Jev, then reviewed by Luna. Built on eve and Next.js. | reachable |
| [opencompany](cards/useopencompany-opencompany.md) | TypeScript | AI workspace whose approval review uses Jev to gate workspace actions with typed decisions. | reachable |
| [jev-architect](cards/karanb192-jev-architect.md) | HTML | Agent skill for finding, designing, and validating useful Jev decision loops before committing them to an application. | reachable |
| [pi-jev-context](cards/nyarlathoteppppp-pi-jev-context.md) | TypeScript | Model performance first. Token savings second. A Pi extension with freshness-aware read dedupe, Jev log filtering, and searchable verbatim recall. Keeps existing message history intact. | reachable |
| [jev-mcp (arunav25)](cards/arunav25-jev-mcp.md) | JavaScript | Connect JEV to MCP clients and compare its judgments against general-purpose LLMs using shared datasets and measurable accuracy. | reachable |
| [pi-fast-jev-compaction](cards/joelhooks-pi-fast-jev-compaction.md) | TypeScript | Pi extension: verbatim context compaction with TypeSafe Jev decisions. | reachable |
| [riff](cards/scale-venture-partners-riff.md) | Python | A small, fast prose linter: ruff-style rule codes for writing, backed by TypeSafe's Jev model. | reachable |
| [jev-commit](cards/valentynkit-jev-commit.md) | Python | Pre-commit hook where Jev checks the message against the staged diff and flags debug leftovers, unmentioned work, and added credentials. | reachable |
| [bicameral](cards/abdelstark-bicameral.md) | TypeScript | Hybrid coding harness: System 2 writes, System 1 (Jev) runs reflexes. | reachable |
| [jev-superpowers](cards/akashpriyadarshii-jev-superpowers.md) | Shell | Cross-agent software-development skills that add Jev decisions to planning, execution, debugging, and completion gates. | http_404 |
| [slidepilot](cards/harshil1712-slidepilot.md) | TypeScript | Voice-driven semantic auto-advance for Slidev, powered by Cloudflare Agents and TypeSafe AI Jev. | reachable |
| [diffjury](cards/raihankhan-rk-diffjury.md) | TypeScript | DiffJury — TypeSafe Jev PR risk router + code review coach. | reachable |
| [tenet](cards/zoidsh-tenet.md) | Go | Commit-time review gate where Jev judges plain-language rules against agent-written code. | http_404 |
| [jev-spec](cards/nozomi-koborinai-jev-spec.md) | TypeScript | Specification-driven semantic verification engine that uses Jev to check AI-generated code and specs against explicit requirements. | reachable |
| [jev-tool-router](cards/jackbarunz-jev-tool-router.md) | JavaScript | MCP router for Codex that uses Jev to select an external tool on demand instead of exposing the agent to every tool schema. | reachable |
| [jev-pref](cards/doeixd-jev-pref.md) | JavaScript | Turn your AGENTS.md preferences into a fast, Jev-powered AI linter. | reachable |
| [jev-oas-sentinel](cards/shuhansun-jev-oas-sentinel.md) | Python | Catch breaking API behavior hidden in OpenAPI prose with deterministic checks and TypeSafe JEV System One semantic review. | reachable |
| [Augustus](cards/24601-augustus.md) | Python | Agent skill for designing Jev-assisted systems with decision theory, composition patterns, question diagnostics, and validation gates. | reachable |
| [typesafe-cli (geilt)](cards/geilt-typesafe-cli.md) | Python | CLI and agent skill for TypeSafe System One (Jev): typed Choice, Score, and Noul judgments. | reachable |
| [jev-judgment](cards/hyunjunjeon-jev-judgment.md) | Python | Agent Skill: send closed coding-agent judgments to TypeSafe Jev. | reachable |
| [jevex](cards/jvsteiner-jevex.md) | Python | Minimal agent loop where Jev directs control flow and a LangChain chat model writes argument values and the final response. | reachable |
| [fast-dev-compaction](cards/leonaaardob-fast-dev-compaction.md) | TypeScript | Codex plugin: verbatim Jev-guided context restoration around session compaction. Port of tamaratran/fast-jev-compaction to Codex lifecycle hooks. | reachable |
| [pi-heed](cards/nyarlathoteppppp-pi-heed.md) | TypeScript | Runtime constraints for the pi coding agent: checks every side-effecting tool call against what you said, before it runs. Powered by TypeSafe Jev. | reachable |
| [jev-router (prismhq)](cards/prismhq-jev-router.md) | Python | Open-source LLM router that uses TypeSafe's Jev to pick a model, on top of LiteLLM. | reachable |
| [jev-mcp (rashedInt32)](cards/rashedint32-jev-mcp.md) | TypeScript | MCP server exposing TypeSafe Jev as typed, calibrated judgment tools: classify, score, check, batched ask. Ships as a Claude Code plugin. | reachable |
| [open-jev-approvals](cards/alexj11324-open-jev-approvals.md) | Go | Approval gate for Claude Code and Codex: intercepts tool calls, gets a Jev risk judgment, then applies a versioned local allow/deny policy. | reachable |
| [dsh-jev](cards/noetion-dsh-jev.md) | TypeScript | DSH bundle that registers jev_ask for TypeSafe Jev noul, choice, and score answers. | reachable |
| [prompt2jev](cards/sumleo-prompt2jev.md) | Python | Agent skill and CLI that turn natural language, an LLM prompt, or the code that runs one into a TypeSafe Jev decision: typed state, Choice/Score/Noul questions, and a runnable script | reachable |
| [jev-mcp-dispatcher](cards/abhishekashokvkumar-jev-mcp-dispatcher.md) | Python | Natural-language MCP tool dispatcher powered entirely by TypeSafe's Jev — no general-purpose LLM. Discovers a simple MCP server's tool signatures at runtime and uses Jev's typed primitives (Choice/Noul) to pick the right tool and extract its arguments straight out of the sentence. No repository-level license file was found during review. | reachable |
| [hermes-jev-plugin](cards/ajensenwaud-hermes-jev-plugin.md) | Python | TypeSafe Jev (System One) decision tools for Hermes Agent: jev_check / jev_route / jev_score / jev_evaluate | reachable |
| [langchain-skill-router](cards/deyna256-langchain-skill-router.md) | Python | LangChain and deepagents skill router where Jev ranks installed `SKILL.md` files and decides whether and which skills to load for each turn. | reachable |
| [jcm-router](cards/adarshmishra07-jcm-router.md) | TypeScript | Local proxy that picks the Claude model and effort per message using TypeSafe Jev. Routes subagents, leaves your cached main chat alone. | reachable |
| [typesafe-mod](cards/belazy167-typesafe-mod.md) | TypeScript | Claude Code mod that routes decisions to TypeSafe's Jev model: ranks installed skills per prompt, and answers the agent's own this-or-that questions when confident. | reachable |
| [jev-shield](cards/caiovicentino-jev-shield.md) | JavaScript | Semantic MCP firewall powered by Jev — screens every tool call, tool result, and tool description with calibrated System One verification. 94% block recall, 0 false positives, ~$0.00002/check. | reachable |
| [mastra-jev-moderation](cards/codealive-ai-mastra-jev-moderation.md) | TypeScript | Mastra input processor that uses Jev for a typed block decision and moderation category. | reachable |
| [tiershift](cards/iamvatsalpatel-tiershift.md) | TypeScript | Shift every LLM call to the cheapest model that can handle it. Routing decided by TypeSafe Jev in ~180 ms. No training data. Policy in plain YAML. TypeScript and Python. | reachable |
| [skill-router](cards/lomeshdutta-skill-router.md) | Python | Tell Claude Code which installed skill a session needs, using Jev (TypeSafe AI) for the decision and skills.sh for discovery. | reachable |
| [todo-jev](cards/maker-kk-todo-jev.md) | Python | ⚡ Ultra-fast, low-cost intelligent task classifier and 3-tier routing engine powered by TypeSafe Jev (System One). | reachable |
| [jev-workbench](cards/molis-ai-jev-workbench.md) | TypeScript | Build versioned judgment functions on TypeSafe's Jev once, then call the same published version from your backend over HTTP and from coding agents over MCP. The vendor key stays on your machine. | reachable |
| [typesafe-migration-guard](cards/opaielsheikh-typesafe-migration-guard.md) | TypeScript | Automated database migration safety reviewer powered by TypeSafe AI (Jev System One model). | reachable |
| [pi-fast-jev-compaction (QuentinDanblon)](cards/quentindanblon-pi-fast-jev-compaction.md) | TypeScript | Pi context pruning that uses Jev to drop or truncate stale tool calls while preserving retained content verbatim. | reachable |
| [jev-system-architect](cards/samtay32-jev-system-architect.md) | — | System-architecture skill for TypeSafe AI Jev/System One — find fuzzy semantic judgment and turn it into small Choice/Score/Noul primitives. | reachable |
| [jev-skill-gate](cards/shivampansuriya-jev-skill-gate.md) | JavaScript | Cut Claude Code's skill manifest by ~75% with TypeSafe Jev. Scores every installed skill for relevance and hides the rest via skillOverrides — 12,750 → 3,185 tokens on a 217-skill install, for $0.0009 a session. | reachable |
| [ailerix](cards/tylerjharden-ailerix.md) | TypeScript | Type-safe model router. Jev (System One) banks each request to a typed catalog route. | reachable |
| [typesafe-ai-firewall](cards/anshchoudhary-typesafe-ai-firewall.md) | Python | Shadow-mode validation harness for a pre-execution firewall on AI agent tool calls (TypeSafe/Jev). Real run, findings in report.md. No repository-level license file was found during review. | reachable |
| [jev-mcp (freepik-company)](cards/freepik-company-jev-mcp.md) | Go | MCP server for typed decisions with Jev / System One via OpenRouter or TypeSafe | reachable |
| [decision-first](cards/harrymunro-decision-first.md) | Python | Agent skill that spots bounded-judgment steps, tries a typed decision model (TypeSafe's Jev) first, and documents every attempt | reachable |
| [jear](cards/ij03l-jear.md) | Rust | Jev-routed client for NEAR AI Cloud inference and IronClaw agents. | reachable |
| [jev-git](cards/akashpriyadarshii-jev-git.md) | Rust | Sub-second pre-commit and pre-push semantic gate that screens staged diffs with Jev. | http_404 |
| [jev-scout](cards/akashpriyadarshii-jev-scout.md) | Rust | Grounded GitHub and crates.io discovery CLI and MCP server that uses Jev to score architectural fit, licensing, and maintenance. | http_404 |
| [jev-skillful](cards/bestagentkits-jev-skillful.md) | TypeScript | Per-prompt capability router for coding agents: resolves installed skills, MCP servers, agents and commands against your prompt via TypeSafe Jev, and measures whether the injection actually helps. | reachable |
| [jev-triage](cards/cephalization-jev-triage.md) | TypeScript | Uses typeful jev, zero sync to pull and sync large repositories for issue triage. | reachable |
| [jev-predict-skill](cards/danielkillenberger-jev-predict-skill.md) | HTML | Predict another skill's next closed decision with TypeSafe Jev — without running that skill. | reachable |
| [stepwarden](cards/getexcited-stepwarden.md) | TypeScript | Claude Code plugin that has Jev compare each pending tool call with the session plan before allowing, escalating, or blocking it. | reachable |
| [Antigravity-mcp-semantic-search-with-TypeSafeAi](cards/greenyamao-antigravity-mcp-semantic-search-with-typesafeai.md) | Python | Fast semantic code search & diff sanity auditor for AI coding assistants (Antigravity, Cursor, Claude Code) powered by TypeSafe System One. | reachable |
| [pi-jev](cards/iefnaf-pi-jev.md) | TypeScript | Pi extension suite for Jev-powered context compaction and model routing. | reachable |
| [hunch](cards/kelbie-hunch.md) | Python | Semantic code review with Jev, plain-English rules, and installable agent skills. | reachable |
| [limpet](cards/noplan-inc-limpet.md) | Python | A Stop hook that stops your coding agent from stopping too early. Plain-language rules, judged by jev. | reachable |
| [ask-jev](cards/omni-ask-jev.md) | PowerShell | Utilizing Jev, the RLCD-type model provided by TypeSafe AI, to independently and cheaply judge agentic coding sessions. | reachable |
| [jev-flash-router](cards/ravinder82-jev-flash-router.md) | TypeScript | MCP server that uses Jev to route coding-agent decisions such as file selection, task paths, and test-impact checks. | reachable |
| [omp-typesafe](cards/siddicky-omp-typesafe.md) | TypeScript | TypeSafe AI (Jev) adversarial reviewer and typesafe_ask tool for the omp coding agent. | reachable |
| [pi-jev-helm](cards/z761293629-pi-jev-helm.md) | TypeScript | Pi extension that classifies tasks with Jev and routes each run to an explicitly configured model. | reachable |
| [jev-mcp (BYK)](cards/byk-jev-mcp.md) | TypeScript | An eval-first MCP server for TypeSafe's Jev, a System One model that returns typed judgments (noul, choice, score) with probabilities instead of generated text. | reachable |
| [askjev (pZacca)](cards/pzacca-askjev.md) | TypeScript | Unofficial MCP server for Jev (Typesafe AI) | reachable |
| [jev-toolkit](cards/jbt95-jev-toolkit.md) | TypeScript | MCP-first toolkit for TypeSafe/Jev — the System One decision model. One stdio server (jev mcp) serves any MCP-capable harness, backed by one local event log and Prometheus impact metrics you can scrape into your own Grafana. | reachable |
| [jev-skill-router](cards/shimo4228-jev-skill-router.md) | Python | Claude Code plugin: asks TypeSafe Jev which installed skill fits each prompt and logs the answer (shadow-first). A working reference for the skill-suggestion cookbook on Claude Code — the README records why it is unlikely to help a strong model as a router. | reachable |
| [dsh-jev-verify](cards/xienda-dsh-jev-verify.md) | JavaScript | Jev (TypeSafe System One) decision tools + live verification benchmark for DeepSeek Harness: jev_decision (choice/score/noul) and jev_verify, honest by design. | reachable |
| [jevonian](cards/xinyao27-jevonian.md) | TypeScript | Local model-routing proxy where Jev selects the model route and reasoning depth, and also judges which tool history can be compacted. | reachable |
| [jev-routed-agent](cards/liuhongrui087-art-jev-routed-agent.md) | Python | LangChain and Flask agent where Jev chooses among knowledge, calculator, weather, and chat routes, with a local-rule fallback. | reachable |
| [codex-jev-router](cards/suenot-codex-jev-router.md) | JavaScript | Portable Jev router for cost-aware Codex subagent model and reasoning selection. | reachable |
| [XavierJev](cards/liu-x27-xavierjev.md) | TypeScript | Local logprob decision layer and Claude Code permission gate that scores command risks, routes model tiers, and judges retries or stuck runs. | reachable |
| [Jev Deep Research](cards/sunyasheng-jevdeepresearch.md) | TypeScript | Research-agent integration where Jev locates relevant source regions with Choice and Noul, then code returns verbatim passages for verification. | reachable |
| [omp-statify](cards/d3d0n-omp-statify.md) | TypeScript | Oh-my-pi extension that asks Jev batched Noul relevance questions about tool-output and earlier assistant-text chunks before main-model context, with opt-in filtering and recoverable originals. No repository-level license file was found during review. | reachable |
| [Jev Decision Gate](cards/f-tiger-jev-decision-gate.md) | Python | CLI, MCP server, and skill using Jev Choice to classify Issue kind, module, and information sufficiency, with calibrated accept/review policies and an offline rules baseline. | reachable |
| [pi-agent-foreman](cards/alexshpunt-pi-agent-foreman.md) | TypeScript | Send Pi agents back to work when they stop before the job is done. | reachable |
| [switchboard](cards/aniruddh-krovvidi-switchboard.md) | Python | Guardrail + model router for LLM gateways on TypeSafe's Jev (System One model), with an independent accuracy/calibration/latency evaluation. Stdlib Python. | reachable |
| [typesafe-demo-mcp](cards/bestagentkits-typesafe-demo-mcp.md) | TypeScript | MCP server exposing TypeSafe System One judgments (noul, choice, score) as agent tools. | reachable |
| [AskJev-MCP](cards/cbruyndoncx-askjev-mcp.md) | JavaScript | MCP server for typed Jev Choice, Noul, and Score judgments with probabilities and confidence. | reachable |
| [decide-mcp](cards/dakdevs-decide-mcp.md) | TypeScript | Configurable decision MCP server with AI SDK, Jev, percentage scores, and bias-profile routing. | reachable |
| [pi-jev-router (gloridifice)](cards/gloridifice-pi-jev-router.md) | TypeScript | Jev model-routing integration for the Pi coding agent. | http_404 |
| [jevkeep](cards/hatt-io-jevkeep.md) | TypeScript | Codex plugin that uses Jev to preserve useful conversation excerpts alongside compacted summaries. | reachable |
| [pi-jev-code](cards/kamilpostrozny-pi-jev-code.md) | TypeScript | Single-agent Pi coding coprocessor with Jev semantic gates, baseline-to-current diff review, and append-only observability telemetry. | reachable |
| [pi-typesafe-jev](cards/legacybridge-tech-pi-typesafe-jev.md) | TypeScript | A pi extension that exposes TypeSafe (Jev, System One) judgments as five pi tools, so a model can make narrow semantic judgments while your code and your users keep control of thresholds, weights, and actions. | reachable |
| [frost](cards/marcus-frost.md) | Go | A flexible and configurable CLI model router using TypeSafe Jev. | reachable |
| [check-risk](cards/moezubair-check-risk.md) | TypeScript | A CLI and GitHub Action that assesses code-change risk using deterministic rules and TypeSafe Jev, recommending checks and reviewers before merge. | reachable |
| [jev-compaction (picaye)](cards/picaye-jev-compaction.md) | JavaScript | Hermes context compaction that has Jev score tool calls, drops stale content, and preserves everything retained verbatim. | reachable |
| [jev-plugins](cards/pinutss-jev-plugins.md) | — | Cursor and Hermes plugin marketplace for JEV Labs routing tools. | reachable |
| [jev-builder-loop](cards/rainbowpuffpuff-jev-builder-loop.md) | Python | Grok skill: Jev as a judgment sensor in a builder-agent loop (priors × probabilities → next act). | reachable |
| [typesafeai-review](cards/rbalch-typesafeai-review.md) | Python | Using Typesafe.AI to generate diff reviews. | reachable |
| [agent-gate-loop](cards/ripwords-agent-gate-loop.md) | TypeScript | Reusable GitHub Action: agent fix loop gated by checks, an AI reviewer, and TypeSafe Jev. | reachable |
| [omp-jevens-classifier](cards/strml-omp-jevens-classifier.md) | TypeScript | Jev-powered model-judged permission gate for OMP (TypeSafe System One). | reachable |
| [jev-review (thiago-ss)](cards/thiago-ss-jev-review.md) | Python | Autonomous Jev pull-request review with typed decisions, calibrated approval gates, and trusted-owner escalation. | reachable |
| [pi-typesafe](cards/twilwa-pi-typesafe.md) | TypeScript | Pi coding-agent extension built on the TypeSafe AI System One API (Jev). | reachable |
| [hermes-jev-router](cards/ussyverse-hermes-jev-router.md) | Python | Experimental Hermes plugin: Jev-assisted model routing plans with budget and capability constraints. API access pending. | reachable |
| [zcode-jev](cards/zahrannnn-zcode-jev.md) | TypeScript | Typed judgment layer for coding agents — gates from PRD to ship. Jev-ready, provider-agnostic. | reachable |
| [agent-handoff-gate](cards/zsoxi-agent-handoff-gate.md) | Python | Experimental protocol for evidence-aware agent handoffs, with Jev-assisted review before results reach the lead agent. | reachable |
| [jev-agent-kit](cards/walidboulanouar-jev-agent-kit.md) | JavaScript | jevkit: fast typed decisions for agents. CLI and MCP tools (route, triage, guard, grep, rank, compact, judge) on TypeSafe Jev. Zero dependencies. | reachable |
| [Jev-Checkpoint](cards/ashishakkumar-jev-checkpoint.md) | TypeScript | A local MCP server that uses TypeSafe Jev to confidence-gate an AI agent’s next step, routing uncertain decisions to proceed, deeper review, or human input. | http_404 |
| [progressgate](cards/ashutoshvjti-progressgate.md) | TypeScript | Detect semantic stagnation in AI agent loops | reachable |
| [jev-packs](cards/dtduc-git-jev-packs.md) | Python | Evidence-gated registry of Jev question packs — curated questions, golden cases and measured evidence for Jev-compatible decision endpoints | reachable |
| [JevGuard](cards/jhonnyr97-jevguard.md) | TypeScript | Claude Code + Codex CLI plugin that verifies the agent follows project rules through a System One (Jev) model | reachable |
| [jev-atlas](cards/v60samurai-jev-atlas.md) | Python | Map where Jev and System One models actually belong in your project, test the strongest ideas, then implement them. A skill for Claude Code and Codex. | http_404 |
| [jev-retrieval](cards/romeromarcelo-jev-retrieval.md) | Rust | Code and document search CLI combining BM25 recall with Jev verification and calibrated reranking. | reachable |
| [Immune](cards/schwarzschlyle-immune.md) | Python | Python runtime screening for LLM applications where Jev judges suspected threats in prompts, tool calls, and responses before threshold-based actions. | reachable |
