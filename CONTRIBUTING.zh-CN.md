# 参与 Baga Ink 开发

感谢参与 Baga Ink。项目面向长期、多设备平台、多国家、多语言以及人类 + AI 协作进行治理。

**English:** [`CONTRIBUTING.md`](CONTRIBUTING.md)

## 开始之前

先阅读：

1. [`README.zh-CN.md`](README.zh-CN.md)
2. AI / Automation Contributor 还必须阅读 [`AGENTS.md`](AGENTS.md)
3. [`docs/zh-CN/00_项目文档入口.md`](docs/zh-CN/00_项目文档入口.md)
4. [`docs/zh-CN/governance/00_开发治理.md`](docs/zh-CN/governance/00_开发治理.md)
5. 与当前工作相关的 Standard / Design / Reference App / Plan
6. 如果改动涉及 Code、Dependency、SDK Output、Sample、Packaging 或可发行 Artifact，还必须阅读 [`docs/zh-CN/governance/02_Baga-Ink授权策略.md`](docs/zh-CN/governance/02_Baga-Ink授权策略.md)

通过 [`docs/localization/catalog.json`](docs/localization/catalog.json) 查询 Stable Localized Document ID 与各 Locale Path 的映射。

## Branch / PR 流程

`main` 已受保护：

```text
main
→ short-lived feature/task branch
→ implementation + tests + docs
→ Pull Request
→ Required CI Checks
→ merge main
```

Permanent Feature Branch 不作为项目知识库。

## Public Documentation 语言

长期 Localized Prose 放在：

```text
docs/en/
docs/zh-CN/
```

Localized Public Category 包括 Standards、Design、Reference Apps、Governance、Status。

英文文件名：

```text
NN_lowercase-kebab-case-name.md
```

简体中文文件名：

```text
NN_中文名称.md
```

禁止重新创建早期中英混合 Public Directory，也不得自行引入未经 Governance 定义的 Locale Layout。

`docs/plans/` 属于公开 Operational Engineering Material，不要求把每份 Task / AI Execution Prompt 做多语言复制，但仍然属于 Public Repository Documentation。

## Public Writing Standard

这个 Public Repository 中所有被 Git 跟踪的 Documentation 都面向 External Reader，包括 README、Contributor Guide、Governance、Standards、Design、Reference Apps、Status、`docs/plans/`、Task Design 与 AI Execution Prompt。

Tracked Documentation 必须：

- 直接陈述 Project Requirement、Decision、Implementation Step 与 Rationale；
- 在没有 Private Conversation History 的情况下仍然可以独立理解；
- 使用适合实际 Public Audience 的正式表达；
- 将 Confidential Commercial Strategy 与 Private Project Discussion 保留在 Public Repository 之外。

不得提交：

- 对 Repository Owner 的个人建议或聊天式回复；
- 引用私人对话中“前面 / 刚才 / 上面讨论”的表达；
- 针对用户、Developer 或 OEM 心理反应的私人策略判断；
- Confidential Monetization Rationale、Negotiation Tactics 或未公开 Pricing Strategy；
- `我建议`、`我们认为` 等把私人咨询过程带入正式项目正文的表达。

面向正式 Public Role 的 Normative Instruction 可以正常使用，例如 `Contributor MUST`、`Task MUST`、`OEM Port SHOULD`。

Confidential Material 应保存在被忽略的本地 `private/` 目录或独立 Private Repository。

强制检查：

```bash
python3 tools/check_public_writing.py
```

## Code / Machine Interface 语言

Source Identifier、Comment / Docstring、Public API、Schema Key / ID、Machine Error Code、CLI Command / Flag、Test Name、Dependency Manifest、Commit Subject 使用英文。

Stable Technical Identifier 不应被翻译成不兼容的另一套名称。

## 强制检查

根据改动范围运行：

```bash
python3 tools/check_docs_i18n.py
python3 tools/check_readme_languages.py
python3 tools/check_platform_port_plans.py
python3 tools/check_licensing.py
python3 tools/check_public_writing.py
```

创建新的 Public Localized Doc 优先使用：

```bash
python3 tools/new_localized_doc.py ...
```

创建 Platform Port Task / Execution Prompt 优先使用：

```bash
python3 tools/new_platform_port_task.py ...
```

不得为了让 Invalid Structure 或 Invalid Content 通过而削弱 Validator。

## 架构变化

如果真实实现证据要求改变 Approved Standard、Design 或 Architecture Freeze，应先修改对应 Governing Decision，或在同一个 Reviewed PR 中同步修改；不能只在 Code 或 Execution Prompt 中静默改变 Architecture。

## License / Provenance

Baga Ink 对不同 Asset Class 采用不同 Licensing Policy。

Baga 自研 Platform / OEM 侧软件默认服从根 Community License，除非具体文件 / 目录另有声明。App-facing SDK / Sample 可以采用独立 Permissive License。LifeBook 正式产品源码属于 Proprietary，不包含在公共 Baga Platform Source Distribution 中。第三方依赖保持上游 License。

参见：

```text
LICENSE
docs/zh-CN/governance/02_Baga-Ink授权策略.md
COMMERCIAL_LICENSE.zh-CN.md
LICENSE_HISTORY.md
THIRD_PARTY_NOTICES.md
```

新增 / 变更依赖时，应记录足够 Provenance：

```text
Project / Source
Version / Commit
License
Where Used
Bundled / Modified / Linked / External Invocation
Required Notice / Source Obligation
```

## Contribution Rights / Dual Licensing

项目同时支持 Community Use 与单独授权的 Commercial OEM / Platform Deployment，因此需要具备按目标 Component 所适用 Community / Commercial Terms 分发 Baga 自研 Contribution 的权利。

提交内容时，Contributor 必须拥有合法提交权。第三方代码不能仅因为公开可见就直接复制进 Baga 自研文件。

针对可能同时采用 Community / Commercial Distribution 的 Baga Platform / Device Adapter 外部代码贡献，merge 前可以要求 Contributor License Agreement（CLA）。在正式、经过法律审核的 CLA 发布并完成签署前，Maintainer 可以暂缓 License Terms 与目标 Component Distribution Model 不兼容的外部 Contribution。

开发并销售一个只使用公开 Baga App API 的 IKP App，与把 Baga Platform / Adapter 代码装进商业设备属于不同授权类别。

## LifeBook 边界

公共仓库中的 LifeBook Reference App 文档用于验证 Baga Architecture。LifeBook 正式产品 Application 是 Proprietary Product，不属于本 Public Repository 的 Platform Source Distribution。

除非某个组件被明确决定公开并给出具体 License，否则不得向 Public Repository 提交：

```text
LifeBook 正式 App Proprietary Source
Backend Source
Product Algorithm
Credentials
Commercial Assets
Private Product Data
```

## 翻译与多语言

根 README 的语言切换由：

```text
docs/localization/readme-languages.json
```

治理。

增加新的 Maintained Locale：

1. 通过 Documentation Governance 提议；
2. 明确 Maintenance / Review Owner；
3. 建立对应 Locale Tree 与必要 Terminology Guidance；
4. 如果提供 Root README Translation，则登记 Registry；
5. 同步所有受管理 Language Switch Block；
6. 扩展 Localization CI / Registry Rule；
7. 不创建 Ad-hoc Language Directory。

Translation 是同一个 Logical Document 的不同 Language Edition，不得形成第二套 Protocol / Architecture。

## 完成标准

Feature 不能仅以“能编译”作为完成条件。应运行相关 Tests，需要时记录 Real-device / Conformance Evidence；涉及 Distribution 的改动应核对 License / Provenance；Tracked Documentation 应通过 Public Writing Validation；重要 Milestone 改变时应更新 Project Status。
