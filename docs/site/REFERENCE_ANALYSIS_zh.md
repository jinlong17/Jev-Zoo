# 参考 codebase 实现分析

[English](REFERENCE_ANALYSIS.md)。核验于 2026-10-12 洛杉矶时间（2026-10-13 UTC）。实际固定源码为 [awesome-jev@39854d858fff73bf3172949c9f968c6cb12beafa](https://github.com/heyjunpenn/awesome-jev/tree/39854d858fff73bf3172949c9f968c6cb12beafa)，提交时间 2026-10-04 15:58:17 UTC。文本源码、HTTP 和浏览器证据留在仓外 site-development。目录介绍与中文翻译为 MIT，保留[原许可](https://github.com/heyjunpenn/awesome-jev/blob/39854d858fff73bf3172949c9f968c6cb12beafa/LICENSE)；未复制其媒体或 UI 代码。

| 要点 | 已检查的实际实现 | JevZoo 采用方式 |
|---|---|---|
| 首页与入口 | Hero、仓库分类栏、目录、showcase、更新记录、赞助与 GitHub 提交入口 | 首页 → 类型/用途 → 详情 → 原始来源/关联资产/训练评测；不引入赞助支付 |
| 数据 schema | `src/lib/catalog.ts` 解析各语言 README 的名称、仓库 URL、介绍、语言、stars；JSON 保存收录日期 | 复用现有 JSON 注册表，原位扩展双语字段，不另维护 README 型事实库 |
| 分类与身份 | 导航配置、URL 规范化、分类路由、语言目录数据 | 一个 canonical 资产、一个主类型、多用途与关联 ID；合并有理由和来源，数量由数据计算 |
| 搜索筛选排序 | 客户端文本搜索、语言/分类筛选、stars 排序、分批展示 | 搜索双语介绍/名称/发布者/别名；优先类型和用途，展开模态/开放/证据/运行筛选；24 项分页 |
| 详情与 showcase | 仓库原始入口、展示 dialog/feed/分类页；视频文字和标签按用途发现 | 预生成资源详情及关联资产；精选应用只展示文字证据与原始链接，不转存视频 |
| 多语言同步 | en 默认语言，以及 zh/ja/ko/es/pt-BR；配置语言 README 与 messages，测试数量/顺序/URL 一致 | 中英文完整页面，共享相同资源 ID，语言切换保留浏览条件 |
| 更新与链接维护 | 收录日期同步、changelog、维护脚本、测试、GitHub 贡献入口 | 保留失效/移除记录及审查理由，记录来源版本；stars 与可达性不代表能力 |
| 构建部署 | Astro 7.3.3、Cloudflare adapter、Node ≥22、Stripe/D1 赞助接口；手动 Worker 部署和迁移 | Python 标准库静态构建 + 原生 JS，无后台；公开部署仍走具体 release 审批 |

直接源码：[目录解析](https://github.com/heyjunpenn/awesome-jev/blob/39854d858fff73bf3172949c9f968c6cb12beafa/src/lib/catalog.ts)、[导航配置](https://github.com/heyjunpenn/awesome-jev/blob/39854d858fff73bf3172949c9f968c6cb12beafa/src/data/catalog-navigation.ts)、[多语言配置](https://github.com/heyjunpenn/awesome-jev/blob/39854d858fff73bf3172949c9f968c6cb12beafa/src/i18n/config.ts)、[站点说明](https://github.com/heyjunpenn/awesome-jev/blob/39854d858fff73bf3172949c9f968c6cb12beafa/SITE_README.md)、[Astro 配置](https://github.com/heyjunpenn/awesome-jev/blob/39854d858fff73bf3172949c9f968c6cb12beafa/astro.config.mjs)、[部署流程](https://github.com/heyjunpenn/awesome-jev/blob/39854d858fff73bf3172949c9f968c6cb12beafa/.github/workflows/deploy.yml)。

该源码 README 的 11 个正式分类有 **981 个唯一仓库**，文末三条代码参考另计。导航写死 **962**，核验时[线上站点](https://jevbest.com/)标题和分类栏也显示 962，不能把当前 HEAD 与线上快照当成同一版本，更不能叫“已支持模型”。另外，[showcase JSON](https://github.com/heyjunpenn/awesome-jev/blob/39854d858fff73bf3172949c9f968c6cb12beafa/src/data/showcase.json)有 **2,091 条视频/帖子**、10 个用途分类，更新时间为 2026-09-25。字段含标题、译文、作者、原帖、媒体 URL、时长和尺寸。这些是社会化演示，不是独立 checkpoint、代码资产或核验跑分，单独分析，不整批加入 canonical 计数。

已使用 Chromium 检查线上页面，关闭首次引导后保存无遮挡截图；并分析 showcase 数据与实现。未下载视频或把演示当作能力验证。借鉴用途导航、分层发现、回到原始入口；不复制品牌与媒体，不导入无关支付栈，不以流行度或原帖时间/费用声称代替实测。JevZoo 采用精选应用 + 广覆盖仓库层，真实运行证据在独立训练评测入口展示。
