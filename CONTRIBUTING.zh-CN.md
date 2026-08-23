# 参与 Baga Ink 开发

感谢参与 Baga Ink。这个项目从一开始就按长期、多设备平台、多国家、多语言、人类 + AI 协作来治理。

**English:** [`CONTRIBUTING.md`](CONTRIBUTING.md)

## 开始之前

先阅读：

1. [`README.zh-CN.md`](README.zh-CN.md)
2. AI / Automation Contributor 还必须阅读 [`AGENTS.md`](AGENTS.md)
3. [`docs/zh-CN/00_项目文档入口.md`](docs/zh-CN/00_项目文档入口.md)
4. 与当前工作相关的 Standard / Design / Reference App / Plan

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
```

创建新的 Public Localized Doc 优先使用：

```bash
python3 tools/new_localized_doc.py ...
```

创建 Platform Port Task / Execution Prompt 优先使用：

```bash
python3 tools/new_platform_port_task.py ...
```

不得为了让错误目录或文件名通过而削弱 Validator。

## 架构变化

如果真实实现证据要求改变 Approved Standard、Design 或 Architecture Freeze，应先修改对应 Governing Decision（或在同一个受 Review PR 中同步修改），不能只在代码或 Execution Prompt 里静默换架构。

## License / Provenance

Baga 自研内容默认使用 Apache License 2.0，除非具体文件/目录明确说明其他 License。

第三方依赖保持上游许可证。新增/变更依赖时，应记录足够的 Provenance：

```text
Project / Source
Version / Commit
License
Where Used
Bundled / Modified / Linked / External Invocation
Required Notice / Source Obligation
```

参见：

```text
LICENSE
NOTICE
THIRD_PARTY_NOTICES.md
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

“能编译”不等于完成。应运行相关 Tests，需要时记录真机 / Conformance Evidence，并在重要 Milestone 改变时更新 Project Status。
