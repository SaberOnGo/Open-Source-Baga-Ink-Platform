# Baga Ink 开发治理 / Baga Ink Development Governance

> **文档级别：项目治理规范 / Project Governance**  
> **状态：Governance Baseline v0.1**  
> **日期：2026-08-23**

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

禁止形成：

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

这类需要人或 AI 猜用途的 Branch 森林。

如果工具或权限暂时无法删除已经合并的 Branch：

1. 该 Branch MUST 不包含 main 之外的唯一内容；
2. SHOULD 将它指向当前 main 或明确标记为 merged/disposable；
3. 后续有删除权限时 SHOULD 删除；
4. AI MUST 忽略它，不把它当作上下文来源。

---

# 4. Pull Request 的职责

PR 是 Review / CI / Diff / Discussion 记录，不是长期项目状态数据库。

PR 完成后：

```text
merge → main
```

其讨论历史可以保留用于审计，但当前事实必须已经反映在：

- 代码；
- 测试；
- Standards；
- Status；
- Design / Plan。

未来 AI 不需要读取历史 PR 才能理解项目当前状态。

---

# 5. 项目状态必须集中维护

唯一正式状态文件：

```text
docs/status/00_当前项目状态_Baga-Ink-Project-Status.md
```

重要里程碑完成时 MUST 更新该文件。

至少记录：

- Completed；
- In Progress；
- Next；
- Known Gaps；
- Draft / Stable 边界；
- Verification Evidence。

禁止让“现在做到哪里”只能从 Commit、Branch 或聊天中推断。

---

# 6. 架构知识保存规则

不同类型的信息必须进入不同目录：

```text
What Baga Ink MUST be
→ docs/standards/

How a subsystem is designed
→ docs/design/

How an approved design is implemented
→ docs/plans/

Where the project currently stands
→ docs/status/

How contributors work
→ docs/governance/

How LifeBook validates the platform
→ docs/reference-apps/
```

不要用 Branch 名代替这些文档。

---

# 7. AI 工作规则

新的 AI Agent MUST：

1. 以 `main` 为基线；
2. 首先读取根目录 `AGENTS.md`；
3. 再读 `docs/00_项目文档入口_Baga-Ink-Documentation-Index.md`；
4. 再读 Status 和相关 Standard；
5. 不扫描历史 Branch 来猜上下文，除非用户明确要求审查某个未合并 PR；
6. 不因为某个 Branch 名看起来较新就认为它更权威；
7. 重要工作完成后更新 Status。

一个理想的新 AI 不需要任何此前聊天上下文即可继续项目。

---

# 8. Commit / Tag / Release 的职责

## Commit

保存可追踪历史。

Commit Message SHOULD 描述真实变化，例如：

```text
docs: define Baga Ink device adapter standard
spec: add publisher identity schemas
feat: add IKP signature verifier
test: add invalid IKP corpus
```

## Tag / Release

用于正式阶段基线，例如未来：

```text
standards-v0.1
ikp-v1.0
platform-v0.1
sdk-v0.1
```

历史版本应该通过 Git Commit / Tag / Release 恢复，而不是靠永久 Feature Branch。

---

# 9. 标准从 Draft 到 Stable

不能因为文档“写完”就进入 Stable。

对于可执行规范，必须依据相应 Stable Gate，例如：

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

当前状态由 Status 文件记录。

---

# 10. 文档命名

项目正式 Markdown 文档 SHOULD 使用：

```text
NN_中文名称_English-Name.md
```

目录自己的入口从 `00_` 开始。

根目录少数工具约定文件可例外，例如：

```text
AGENTS.md
README.md
LICENSE
CONTRIBUTING.md
```

---

# 11. Branch 清理验收

每次完成一项较大的临时 Branch 工作时，应确认：

```text
[ ] 所有有效代码已进入 main
[ ] 所有测试已进入 main
[ ] 重要架构结论已进入 docs
[ ] 当前进度已更新 status
[ ] Branch 不包含唯一信息
[ ] PR 已 merge/close
[ ] Branch 已删除；若工具权限暂不支持，已明确 disposable
```

---

# 12. 最终原则

Baga Ink 是一个长期项目，可能由不同人、不同 AI、不同工具持续维护。

因此项目必须优化成：

> **读仓库，而不是读人的记忆。**

进一步说：

> **读 `main`，而不是读 Branch 森林。**

只要这条原则成立，未来的开发者和 AI 就不需要知道某个历史 Feature Branch 叫什么，也不会因为上下文丢失而重新发明已经做过的设计。
