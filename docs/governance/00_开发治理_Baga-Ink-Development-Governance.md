# Baga Ink 开发治理 / Baga Ink Development Governance

> **文档级别：项目治理规范 / Project Governance**  
> **状态：Governance Baseline v0.3**  
> **日期：2026-08-23**  
> **国际化规则：`docs/zh-CN/governance/01_文档国际化与本地化规范.md` / `docs/en/governance/01_documentation-internationalization-policy.md`**

---

## 0. 目的

本文档规定 Baga Ink 仓库如何保存长期事实、如何使用 Git Branch / Pull Request、如何交接给未来开发者和 AI，以及什么信息必须进入 `main`。

最重要的治理原则：

> **`main` 是唯一长期事实来源。Branch 是施工脚手架，不是知识库。**

---

# 1. `main` 的地位

`main` MUST 保存所有长期有效内容：

- 当前正式 Standards；
- Approved Design；
- Implementation Plan；
- 当前项目状态；
- Reference Implementation；
- JSON Schema / Test Vector / Fixture；
- 测试；
- CI；
- Reference App 文档；
- 未来正式 Platform / Client / Market 源代码。

任何正式架构结论如果只存在于：

```text
聊天记录
Feature Branch
Draft PR 描述
Issue 评论
个人笔记
```

都不算完成项目知识沉淀。

---

# 2. Feature Branch 的唯一用途

Feature Branch MAY 用于：

- 短期开发隔离；
- 故意 RED 的 TDD 中间状态；
- PR Review；
- CI 验证；
- 危险重构的临时保护。

Feature Branch MUST NOT 用于长期保存：

- 架构定义；
- 当前状态；
- 路线图；
- 兼容性矩阵；
- 隐藏需求；
- AI 上下文；
- “以后再来看的实现”。

正确生命周期：

```text
main
 │
 ├── create temporary branch
 │       │
 │       ▼
 │    implement / test / review
 │       │
 │       ▼
 └──── merge back to main
             │
             ▼
        delete branch
```

一旦内容已经进入 `main`，Branch 就不再拥有信息价值。

---

# 3. Branch 数量原则

仓库 SHOULD 长期尽量只保留：

```text
main
```

以及确实正在施工、尚未合并的极少数短期 Branch。

禁止形成需要人或 AI 猜用途的 Branch 森林，例如：

```text
feat-a
feat-b
feat-c-v2
old-architecture
new-architecture
working-final
final-v2
ai-test
```

如果工具或权限暂时无法删除已经合并的 Branch：

1. 该 Branch MUST 不包含 main 之外的唯一内容；
2. SHOULD 将它明确标记为 merged/disposable；
3. 后续有删除权限时 SHOULD 删除；
4. AI MUST 忽略它，不把它当作上下文来源。

---

# 4. Pull Request 与 main Ruleset

PR 是 Review / CI / Diff / Discussion 记录，不是长期项目状态数据库。

PR 完成后：

```text
merge → main
```

当前 `main` 使用 GitHub Ruleset 保护，目标行为包括：

```text
Require Pull Request
Require required status checks
Require branch up to date
Restrict deletion
Block force push
No bypass by default
```

Required status check 当前包含：

```text
Validate task/prompt layout
```

该 Job 名保持稳定，内部同时执行文档结构 Guard 与 Platform Port Plan Guard。

---

# 5. 项目状态必须集中维护

项目当前状态属于 Public Localized Docs。

最终路径：

```text
docs/en/status/00_baga-ink-project-status.md
docs/zh-CN/status/00_当前项目状态.md
```

国际化迁移期间，Catalog 可能仍指向旧路径：

```text
docs/status/00_当前项目状态_Baga-Ink-Project-Status.md
```

AI / 开发者 MUST 通过：

```text
docs/localization/catalog.json
```

解析当前有效路径，而不是硬编码旧路径。

重要里程碑至少记录：

- Completed；
- In Progress；
- Next；
- Known Gaps；
- Draft / Stable 边界；
- Verification Evidence。

---

# 6. 架构知识保存规则

长期公共知识按类别保存，但公共正文已经进入 Locale Tree 模型：

```text
What Baga Ink MUST be
→ docs/<locale>/standards/

How a subsystem is designed
→ docs/<locale>/design/

Where the project currently stands
→ docs/<locale>/status/

How contributors work
→ docs/<locale>/governance/

How LifeBook / Reference Apps validate the platform
→ docs/<locale>/reference-apps/

How an approved design is implemented
→ docs/plans/
```

其中：

```text
<locale> = en | zh-CN
```

`docs/plans/` 属于工程施工区，不要求把每一份 Task / AI Prompt 做双语镜像。

---

# 7. 文档国际化规则

公共长期文档必须遵守：

```text
docs/zh-CN/governance/01_文档国际化与本地化规范.md
docs/en/governance/01_documentation-internationalization-policy.md
```

核心规则：

```text
Public long-lived docs
→ locale trees

English:
NN_lowercase-kebab-case-name.md

Simplified Chinese:
NN_中文名称.md
```

中英文是同一 Document Identity 的不同语言版本，不是两套协议。

早期目录：

```text
docs/standards/
docs/design/
docs/reference-apps/
docs/governance/
docs/status/
```

现在是 **Legacy Migration Zone**。不得再新增公共文档。

所有迁移对象、目标路径和状态由：

```text
docs/localization/catalog.json
```

管理。

---

# 8. 代码与机器接口语言

为了国际多人协作，以下内容 SHOULD 使用英文/语言无关形式：

```text
source code identifiers
comments / docstrings
public API names
schema keys / schema IDs
error codes
CLI commands / flags
test names
dependency manifests
commit subjects
release tags
```

以下目录不做多语言复制：

```text
spec/
reference/
tests/
tools/
.github/
platform/
sdk/
client/
```

中文技术文档可以使用中文解释，但 `Baga Ink`、`IKP`、`Device Adapter Contract`、`Capability`、`SQLite`、`Automerge`、`KOReader`、`FBInk` 等稳定技术身份不应为了形式上的“全中文”而强行翻译。

---

# 9. AI 工作规则

新的 AI Agent MUST：

1. 以 `main` 为基线；
2. 首先读取根目录 `AGENTS.md`；
3. 再读 `docs/README.md`；
4. 选择 `docs/en/` 或 `docs/zh-CN/` 入口；
5. 读取 `docs/localization/catalog.json` 解析迁移中的当前文档路径；
6. 再读 Status 和相关 Standard；
7. 不扫描历史 Branch 来猜上下文，除非用户明确要求审查某个未合并 PR；
8. 重要工作完成后更新 Status / Compatibility Evidence。

一个理想的新 AI 不需要任何此前聊天上下文即可继续项目。

---

# 10. Commit / Tag / Release 的职责

## Commit

Commit Subject SHOULD 使用简洁英文，例如：

```text
docs: define Baga Ink device adapter standard
spec: add publisher identity schemas
feat: add IKP signature verifier
test: add invalid IKP corpus
```

## Tag / Release

用于正式阶段基线，例如：

```text
standards-v0.1
ikp-v1.0
platform-v0.1
sdk-v0.1
```

历史版本应该通过 Git Commit / Tag / Release 恢复，而不是靠永久 Feature Branch。

---

# 11. 标准从 Draft 到 Stable

不能因为文档“写完”就进入 Stable。

对于可执行规范，Stable Gate 例如：

```text
Schema validation
Canonical vectors
Negative corpus
Reference verifier
Independent verifier
Cross-language compatibility
TUF conformance
End-to-end tests
CI
```

对于需要双语维护的 Public Standard，还必须满足：

```text
required locale editions are current
no unresolved semantic drift
localization catalog is current
```

---

# 12. Platform Port Task / Execution Prompt 特殊规则

`docs/plans/platform-ports/` 是大规模任务资料的特殊治理区域，继续使用：

```text
NNNN_中文名称_English-Name.md
```

以及：

```text
task/<NNNN_中文任务名_English-Task-Name>/vNNN/
execution-prompts/<same Task>/<same vNNN>/
```

它不因为 Public Docs 国际化而复制成 `en/` 与 `zh-CN/` 两套。

具体规则：

```text
docs/plans/platform-ports/0000_平台移植计划目录与文件命名规则_Baga-Ink-Platform-Port-Plan-Naming.md
```

强制工具：

```text
python3 tools/new_platform_port_task.py ...
python3 tools/check_platform_port_plans.py
```

---

# 13. Documentation i18n Guard

公共文档结构由：

```text
python3 tools/check_docs_i18n.py
```

校验。

新增 Public Localized Doc SHOULD 使用：

```text
python3 tools/new_localized_doc.py ...
```

AI / 开发者不得：

- 在 Legacy Public Docs 目录继续新增文件；
- 乱建 `english/`、`chinese/`、`cn/`、`zh/`；
- 在 `docs/en/` 使用中文混合文件名；
- 在 `docs/zh-CN/` 继续把整段英文文件名重复追加在中文名后；
- 为了让 CI 通过而削弱 Guard 或随意篡改 Catalog。

---

# 14. Branch 清理验收

每次完成一项较大的临时 Branch 工作时，应确认：

```text
[ ] 所有有效代码已进入 main
[ ] 所有测试已进入 main
[ ] 重要架构结论已进入 governed docs
[ ] 当前进度已更新 status
[ ] Branch 不包含唯一信息
[ ] PR 已 merge/close
[ ] Branch 已删除或明确 disposable
```

---

# 15. 最终原则

Baga Ink 是长期、多人、多语言项目，因此必须优化成：

> **读仓库，而不是读人的记忆。**

进一步说：

> **读 `main`，通过 Locale Tree 选择自己能读懂的公共文档；代码与机器协议始终只有一套。**
