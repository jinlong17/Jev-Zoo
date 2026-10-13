# JevZoo 展示站点

[English](README.md) · [信息架构](../docs/site/ARCHITECTURE.md) · [参考源码分析](../docs/site/REFERENCE_ANALYSIS_zh.md)

这是与现有训练评测平台相连的可用中英文静态展示入口。Python 3.10+ 生成 HTML，原生 JavaScript 提供搜索、筛选和分页；无 Node 包、账号、后台、追踪服务或商业推理依赖。可部署在静态主机的子路径下。

```bash
python site/build.py --output /absolute/path/outside/git/jevzoo-site --readmes
python site/check.py
python -m unittest discover -s site -p 'test_*.py' -v
python site/audit.py --output /absolute/path/outside/git/jevzoo-site
python -m http.server 8766 --bind 127.0.0.1 --directory /absolute/path/outside/git/jevzoo-site
```

打开 `http://127.0.0.1:8766/zh/` 或 `/en/`。交互目录通过 HTTP 加载 JSON，不建议直接双击文件；首页与资源详情已预生成。按 `/` 聚焦搜索，筛选状态与页码保存在 URL，切换语言保留当前浏览条件。网页不会执行评测命令。

## 一处维护，同源生成

编辑现有 **`catalog/catalog.json`**，不要手工维护生成的 HTML、README 或网页 JSON。记录稳定 ID、主类型、中英介绍、组件许可、原始来源与关联 ID。用途可多选；类型计数互斥。canonical 映射兼容原有 `discovery_id`、`curated_ids` 字段。

`site/enrich_catalog.py` 可从固定参考源码与已有核验综述导入元数据，只读取公开文本与 GitHub 元数据。重新导入前应保护人工编辑并审查差异；日常维护只需离线构建。现有目录生成器会在旧资源卡生成后调用站点构建；发现源刷新保留双语资料、补充资产和失效/移除记录，来源介绍变化时标记待复查翻译。旧渲染步骤仍会扫描历史 run，评测进行中应直接调用独立站点构建。

来源可达、作者能力声明、loader 可见、接入实现、smoke 和全量分别记录，链接检查不会获得运行标识。公开结果必须与具体批准的 release hash、checkpoint 与数据版本一致；待批准或字节变化的摘要不进入结果表。`site/approved-results-manifest.json` 是既有批准的 hash 投影，不构成新审批；更新只能来自有效审批凭据与候选，不能通过编辑它来批准结果。两个 Lab 配方已有 smoke，正式训练验证仍待完成，入口需要 Lab 权限。

## 构建、部署与审批

输出目录是自包含静态文件，可在批准后部署到 GitHub Pages、Cloudflare Pages 或其他静态 HTTP 主机。本轮未更改 DNS、托管配置或部署站点。建议启用压缩与缓存；目录 JSON 未压缩约 2.3 MB，只在目录页加载。资源详情可直接导航。

沿用既有发布合同：审查并提交的干净 Lab、当前检查通过、公开基线一致、逐文件白名单，以及对具体 release ID/hash 的批准。公开清单生成器已加入站点源码与文档，但这不授权部署。正式候选在 Lab 隔离分支整合、提交并通过检查后，由既有 release prepare 生成；它绑定完整公开文件 hash。主评测工作树和无关 WIP 原样保留。确认具体 release 后才同步公开源码与部署。

## 来源与限制

上游中英文目录文字来自 MIT 许可的 `heyjunpenn/awesome-jev@39854d858fff73bf3172949c9f968c6cb12beafa`，保留 `NOTICE` 与完整许可。页面、构建代码与 favicon 为 JevZoo 原创；未分发上游标志、视频、截图或赞助支付后端。模型、数据及各组件保留各自条款。ETHACC 继续待消歧。广覆盖条目多数只有链接证据，尚无应用实跑或独立能力验证。

## 固定部署内容

`site/deployment-manifest.json` 记录每个静态文件的 SHA-256；该清单本身在正式公开白名单中，因此 release hash 同时绑定网页内容。用 `python site/deployment.py verify --output /absolute/path/outside/git/jevzoo-site` 验证重建；用 `archive` 命令生成稳定 ZIP。诊断报告和时间戳不进入部署，`.nojekyll` 保留。`--no-source-write` 适合干净已提交分支的复验。

计划部署到 `https://jinlong17.github.io/Jev-Zoo/`，使用公开仓库 `gh-pages` 分支根目录；本轮没有创建该分支或更改 Pages 设置。GitHub Pages 即使按分支发布也经过部署 workflow；现有账户 Billing 对 Pages 的影响未经实证，不宣称已上线。批准后只部署 hash 匹配文件，并检查远端 URL、双语页面与资源 JSON。

已批准结果固定为 120 份：110 smoke + 10 JevBench public full。编译优先使用提交内的批准 hash 投影，不随新的公开 release marker 自动重标结果；新增正式结果需独立审查并更新投影。
