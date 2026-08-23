# 参与 Baga Ink 开发

感谢参与 Baga Ink。这个项目从一开始就按长期、多设备平台、多国家、多语言、人类 + AI 协作来治理。

**English:** [`CONTRIBUTING.md`](CONTRIBUTING.md)

## 开始之前

先阅读：

1. [`README.zh-CN.md`](README.zh-CN.md)
2. AI / Automation Contributor 还必须阅读 [`AGENTS.md`](AGENTS.md)
3. [`docs/zh-CN/00_项目文档入口.md`](docs/zh-CN/00_项目文档入口.md)
4. 与当前工作相关的 Standard / Design / Reference App / Plan
5. 如果改动涉及 Code、Dependency、SDK Output、Sample、Packaging 或可发行 Artifact，还必须阅读 [`docs/zh-CN/governance/02_Baga-Ink授权策略.md`](docs/zh-CN/governance/02_Baga-Ink授权策略.md)

通过 [`docs/localization/catalog.json`](docs/localization/catalog.json) 查询稳定 Public Document ID 与各 Locale Path 的映射。

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

不要把永久 Feature Branch 当项目知识库。

## Public Documentation 语言

公共、长期正文只允许存在于：

```text
docs/en/
docs/zh-CN/
```

Public Category 包括 Standards、Design、Reference Apps、Governance、Status。

英文文件名：

```text
NN_lowercase-kebab-case-name.md
```

简体中文文件名：

```text
NN_中文名称.md
```

禁止重新创建早期中英混合 Public Directories，也不要自行发明另一套 Locale Layout。

`docs/plans/` 属于工程施工资料，不要求把每份 Task / AI Execution Prompt 做多语言复制。

## Code / Machine Interface 语言

Source Identifier、Comment / Docstring、Public API、Schema Key / ID、Machine Error Code、CLI Command / Flag、Test Name、Dependency Manifest、Commit Subject 使用英文。

稳定技术 Identifier 不要强行翻成不兼容的另一套名字。

## 强制检查

根据改动范围运行：

```bash
python3 tools/check_docs_i18n.py
python3 tools/check_readme_languages.py
python3 tools/check_platform_port_plans.py
python3 tools/check_licensing.py
```

创建新的 Public Localized Doc 优先使用：

```bash
python3 tools/new_localized_doc.py ...
```

创建 Platform Port Task / Execution Prompt 优先使用：

```bash
python3 tools/new_platform_port_task.py ...
```

不得为了让错误目录、文件名或 License Layout 通过而削弱 Validator。

## 架构变化

如果真实实现证据要求改变 Approved Standard、Design 或 Architecture Freeze，应先修改对应 Governing Decision（或在同一个受 Review PR 中同步修改），不能只在代码或 Execution Prompt 里静默换架构。

## License / Provenance

Baga Ink 采用分层授权模型，不是一张 License 覆盖所有资产。

Baga 自研 Platform / OEM 侧软件默认服从根 Community License，除非具体文件 / 目录另有声明。App-facing SDK / Sample 可以采用单独的宽松许可证。LifeBook 正式产品源码属于 Proprietary，不包含在公共 Baga Platform Source Distribution 中。第三方依赖永远保持上游 License。

参见：

```text
LICENSE
docs/zh-CN/governance/02_Baga-Ink授权策略.md
COMMERCIAL_LICENSE.zh-CN.md
LICENSE_HISTORY.md
THIRD_PARTY_NOTICES.md
```

新增 / 变更依赖时，应记录足够的 Provenance：

```text
Project / Source
Version / Commit
License
Where Used
Bundled / Modified / Linked / External Invocation
Required Notice / Source Obligation
```

## Contribution Rights / 未来 Dual Licensing

Baga Ink 希望同时支持 Community Use 和单独授权的 Commercial OEM / Platform Deployment。要维持这种模式，项目必须拥有足够权利，才能按 Community 与 Commercial Terms 分发 Baga 自研 Contribution。

提交内容时，你必须拥有合法提交权。不要因为第三方代码“在 GitHub 上公开”就直接复制到 Baga 自研文件中。

针对需要 Dual Licensing 的 Baga Platform / Device Adapter 外部代码贡献，merge 前可能需要 Contributor License Agreement（CLA）。在正式、经过法律审核的 CLA 发布并完成签署前，Maintainer 可以暂缓会导致未来 Commercial Relicensing 不可能或不明确的外部代码贡献。

这条规则不意味着普通 App 开发者需要购买 Platform Commercial License。开发并销售一个只使用公开 Baga App API 的 IKP App，与把 Baga Platform / Adapter 代码装进商业设备完全是两件事。

## LifeBook 边界

公共仓库中的 LifeBook Reference App 文档用于验证 Baga Architecture，并不意味着 LifeBook 正式产品源码应进入本仓库。

除非 Project Owner 明确决定公开某个组件并给出具体 License，否则不要向公共仓库提交：

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

增加一个新的 Maintained Locale：

1. 先通过 Documentation Governance 提议；
2. 明确维护 / Review Owner；
3. 建立对应 Locale Tree 与必要 Terminology Guidance；
4. 如果提供 Root README Translation，则登记 Registry；
5. 同步所有受管理 Language Switch Block；
6. 扩展 Localization CI / Registry Rule；
7. 不允许临时手工建另一个语言目录。

翻译是同一个逻辑文档的不同语言版本，不允许借翻译形成第二套 Protocol / Architecture。

## 完成标准

“能编译”不等于完成。应运行相关 Tests，需要时记录真机 / Conformance Evidence；涉及 Distribution 的改动要核对 License / Provenance；重要 Milestone 改变时更新 Project Status。
