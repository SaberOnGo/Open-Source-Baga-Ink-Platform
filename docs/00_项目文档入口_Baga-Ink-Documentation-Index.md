# Baga Ink 项目文档入口 / Baga Ink Documentation Index

> **文档级别：项目总入口 / Project Documentation Entry Point**  
> **状态：Living Index v0.1**  
> **日期：2026-08-23**

---

## 0. 核心规则

本仓库的长期事实来源只有：

> **`main` 分支中的代码、测试与正式文档。**

任何 Feature Branch、Draft PR、聊天记录或分支名称都不是项目知识的长期存储位置。

未来开发者或 AI 不应通过“猜某个分支是干什么的”来恢复上下文。

---

# 1. 第一次进入项目应该读什么

推荐顺序：

```text
AGENTS.md
   │
   ▼
本文件
   │
   ▼
docs/status/00_当前项目状态_Baga-Ink-Project-Status.md
   │
   ▼
docs/standards/00_规范总览_Baga-Ink-Standards-Index.md
   │
   ▼
docs/governance/00_开发治理_Baga-Ink-Development-Governance.md
   │
   ▼
与当前任务相关的 Standard / Design / Plan / Reference App 文档
```

这样应当能够在不依赖聊天历史和历史分支的前提下理解项目。

---

# 2. 文档目录职责

## `docs/status/`

保存**项目现在做到哪里**。

唯一正式状态入口：

```text
00_当前项目状态_Baga-Ink-Project-Status.md
```

该文件回答：

- 当前已经完成什么；
- 哪些东西只是 Draft；
- 当前正在做什么；
- 下一阶段是什么；
- 哪些测试已经有证据；
- 哪些关键工作尚未开始。

---

## `docs/standards/`

保存 Baga Ink 的正式标准与规范。

入口：

```text
00_规范总览_Baga-Ink-Standards-Index.md
```

这里回答：

> **Baga Ink 应该是什么、App/设备/分发系统必须遵守什么。**

标准不是项目进度日志。

---

## `docs/design/`

保存已经讨论并确认的架构实施设计。

Design 回答：

> **某个子系统准备怎样实现，以及为什么这样设计。**

Design 不取代上位 Standard。

---

## `docs/plans/`

保存具体 Implementation Plan。

Plan 回答：

> **已经确认的设计下一步按什么工程顺序落地和验证。**

Plan 可以完成后保留作为实施历史，但当前进度必须回写 `docs/status/`。

---

## `docs/reference-apps/`

保存旗舰 / Reference App 如何遵守并验证 Baga Ink 标准。

当前第一份：

```text
01_LifeBook参考实现_LifeBook-Reference-App.md
```

LifeBook 是 App，不是 Baga Ink Platform。

---

## `docs/governance/`

保存项目治理、文档治理、分支与发布管理规则。

入口：

```text
00_开发治理_Baga-Ink-Development-Governance.md
```

---

# 3. 代码与机器规范目录

```text
spec/
```

保存机器可读规范，包括 JSON Schema、测试向量和非法样本。

```text
reference/
```

保存规范 Reference Implementation / Independent Verifier。

```text
tests/
```

保存可执行规范测试、互操作测试与回归测试。

```text
.github/workflows/
```

保存 CI / Conformance 自动验证。

这些内容和 `docs/standards/` 相互约束；不能让机器格式与文字规范长期漂移成两套协议。

---

# 4. Git 信息的职责

Git Commit / Tag / Release 用来保存历史与发布点。

Feature Branch 只用于短期施工隔离，例如：

```text
创建临时 Branch
      ↓
开发 / CI / Review
      ↓
合并 main
      ↓
删除 Branch
```

历史由 Commit / PR 记录保存，不需要长期保留 Feature Branch。

---

# 5. AI Handoff 原则

任何 AI 完成重要阶段后，必须确保以下信息已经存在 `main`：

1. 重要架构决定进入 Standard 或 Design；
2. 实际完成状态进入 Status；
3. 可执行行为进入代码、Schema 或 Test；
4. 下一阶段进入 Status / Plan；
5. 不留下“只有这个聊天知道”的关键要求；
6. 不留下“只有某个 Branch 知道”的项目状态。

目标是：

> **一个完全没有聊天上下文的新 AI，只读取 `main`，也能继续 Baga Ink。**

---

# 6. 当前最重要入口

```text
Project status
→ docs/status/00_当前项目状态_Baga-Ink-Project-Status.md

Platform standards
→ docs/standards/00_规范总览_Baga-Ink-Standards-Index.md

Development governance
→ docs/governance/00_开发治理_Baga-Ink-Development-Governance.md

Executable specification design
→ docs/design/01_规范可执行化_Baga-Ink-Executable-Specification-Design.md

Executable specification implementation plan
→ docs/plans/01_规范可执行化实施计划_Baga-Ink-Executable-Specification-Implementation-Plan.md

LifeBook reference application
→ docs/reference-apps/01_LifeBook参考实现_LifeBook-Reference-App.md
```

---

**本文件是 Baga Ink 仓库所有项目文档的总入口。**
