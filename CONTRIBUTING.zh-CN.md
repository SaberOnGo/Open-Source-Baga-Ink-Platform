# 参与 Baga Ink 开发

感谢参与 Baga Ink。这个项目从一开始就按长期、多人、多设备平台、多语言、人类 + AI 协作来治理。

**English:** [`CONTRIBUTING.md`](CONTRIBUTING.md)

## 开始之前

先阅读：

1. [`AGENTS.md`](AGENTS.md)
2. [`docs/README.zh-CN.md`](docs/README.zh-CN.md)
3. 与当前工作相关的 Standards / Design / Reference App

文档国际化迁移期间，通过 [`docs/localization/catalog.json`](docs/localization/catalog.json) 查当前公共文档的真实路径，不要凭旧聊天或旧路径猜。

## Branch / PR 流程

`main` 已受保护，开发流程应为：

```text
main
  ↓
短期 feature/task branch
  ↓
实现 + 测试 + 文档
  ↓
Pull Request
  ↓
Required CI Checks
  ↓
merge main
```

不要把长期 Feature Branch 当项目知识库。

## 文档语言

公共、长期正文按语言放在：

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

禁止继续往旧的“中文 + 英文混合文件名”公共目录新增文档。

`docs/plans/` 属于工程施工资料，不要求把每份 Task / AI Execution Prompt 做双语复制。

## 代码和机器接口语言

源码 Identifier、Comment / Docstring、Public API、Schema Key / ID、Machine Error Code、CLI Command / Flag、Test Name、Dependency Manifest、Commit Subject 使用英文。

中文文档可以用中文解释，但稳定技术标识符不要强行翻成另一套名字。

## 强制检查

提交文档/计划相关改动前，根据范围运行：

```bash
python3 tools/check_docs_i18n.py
python3 tools/check_platform_port_plans.py
```

创建新的 Public Localized Doc 优先使用：

```bash
python3 tools/new_localized_doc.py ...
```

创建 Platform Port Task / execution prompt 优先使用：

```bash
python3 tools/new_platform_port_task.py ...
```

不得为了让错误目录或文件名通过而削弱 Validator。

## 架构变化

如果真实实现证据要求改变已经批准的 Standard、Design 或 Architecture Freeze，应先修改对应上位文档（或在同一个受审查 PR 中同步修改），不能只在代码里静默换架构。

## 完成标准

“能编译”不等于完成。应运行相关 Tests，需要时记录真机 / Conformance Evidence，并在重要里程碑改变时更新当前 Project Status。
