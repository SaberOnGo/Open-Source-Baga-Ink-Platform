# Baga Ink 文档国际化迁移计划 / Documentation Internationalization Migration Plan

> **文档级别：Implementation Plan / 文档基础设施迁移计划**  
> **状态：Plan Baseline v0.4**  
> **日期：2026-08-23**  
> **上位治理：`docs/en/governance/01_documentation-internationalization-policy.md` / `docs/zh-CN/governance/01_文档国际化与本地化规范.md`**

## 0. Goal

把早期以中文为主、文件名中英混合的公共文档体系迁移为：

```text
docs/en/
docs/zh-CN/
```

同时保证：

- Standards / Design / Reference Apps / Governance / Status 形成稳定国际化入口；
- 中英文属于同一 Document Identity，不形成两套协议；
- `docs/plans/` 不复制几千份 Task / AI Execution Prompt；
- Machine Spec、Reference Implementation、Tests、API / Schema / Code 保持英文或语言无关；
- 迁移不改变已批准的协议和架构语义；
- 完成迁移后删除 Legacy Public Trees，并让 CI 禁止它们重新出现。

---

## 1. Final target structure

```text
docs/
├── README.md
├── README.zh-CN.md
├── en/
│   ├── 00_baga-ink-documentation-index.md
│   ├── standards/
│   ├── design/
│   ├── reference-apps/
│   ├── governance/
│   └── status/
├── zh-CN/
│   ├── 00_项目文档入口.md
│   ├── standards/
│   ├── design/
│   ├── reference-apps/
│   ├── governance/
│   └── status/
├── plans/
└── localization/
    ├── catalog.json
    ├── terminology.json
    ├── legacy-lock.json
    └── readme-languages.json
```

最终删除：

```text
docs/standards/
docs/design/
docs/reference-apps/
docs/governance/
docs/status/
docs/00_项目文档入口_Baga-Ink-Documentation-Index.md
```

---

## 2. Naming rules

English public docs:

```text
NN_lowercase-kebab-case-name.md
```

Simplified Chinese public docs:

```text
NN_中文名称.md
```

同一 Category 的 Counterpart MUST 使用同一个稳定 `NN` / Document ID。

`docs/plans/platform-ports/` 保持独立的四位 Task / Prompt 编号规则。

---

## 3. Completed foundation — M0

已完成：

```text
README.md / README.zh-CN.md
CONTRIBUTING.md / CONTRIBUTING.zh-CN.md
LICENSE / NOTICE / THIRD_PARTY_NOTICES.md

docs/en/ + docs/zh-CN/
docs/localization/catalog.json
docs/localization/terminology.json
docs/localization/legacy-lock.json
docs/localization/readme-languages.json

tools/check_docs_i18n.py
tools/check_readme_languages.py
tools/new_localized_doc.py

AGENTS hard gate
Repository Documentation Guard
GitHub main Ruleset / Required Check
```

Apache-2.0 是 Baga 自研内容默认许可证；第三方依赖保持各自上游许可证。

---

## 4. M1 — Public working editions

每个迁移批次必须：

1. 保留已批准语义；
2. 中文版不强行翻译 Canonical Technical Identity；
3. 英文版必须完整可独立阅读，不允许空 Stub；
4. 保留 `MUST` / `SHOULD` / `MAY`、API Identifier、Field Name、Error Code、Version、Package Name；
5. 更新 Catalog / Documentation Index / Status；
6. 通过 Documentation Guard 与现有 Conformance CI；
7. 在旧引用仍存在时，Legacy File 只能保持 hash-locked 兼容入口，不得继续原位演进。

### M1-A — Governance + Status + Documentation Index — COMPLETE

```text
docs/en/governance/00_baga-ink-development-governance.md
docs/zh-CN/governance/00_开发治理.md

docs/en/status/00_baga-ink-project-status.md
docs/zh-CN/status/00_当前项目状态.md

docs/en/00_baga-ink-documentation-index.md
docs/zh-CN/00_项目文档入口.md
```

### M1-B1 — Standards 00–06 — COMPLETE

```text
00 Standards Index
01 Platform Strategy / Architecture
02 App Standard
03 API Specification
04 Capability Registry
05 Permission Model
06 IKP Package Specification
```

### M1-B2 — Standards 07–13 — COMPLETE

```text
07 Device Adapter Contract
08 Compatibility Standard
09 UI Specification
10 BICTS
11 Kindle Device Adapter
12 Android E-Paper Adapter
13 Standard Libraries / Adopted Components
```

这意味着国际开发者现在已经可以完整阅读 Baga 的 App / API / IKP / Device Porting / Compatibility / Kindle / Android 核心标准。

Catalog 中 Standards `00–13` 均为 `current`。

### M1-C — Standards 20–28 — NEXT

```text
20 Market / Distribution Architecture
21 Publisher Identity / App Ownership
22 IKP Signing / Key Lifecycle
23 Repository Metadata / Index Protocol
24 Publishing / Review / Version Policy
25 Update / Rollback / Revocation
26 Distribution Client / Offline Transfer
27 Transparency / Security Audit
28 Catalog / App Discovery
```

### M1-D — Design — PENDING

```text
01 Executable Specification Design
02 Device Adapter Executable Contract / SDK Design
```

### M1-E — Reference Apps — PENDING

```text
01 LifeBook Reference App
02 LifeBook Kindle Product Behavior / Accessories
03 Kindle Implementation Architecture Freeze
99 Superseded compatibility document
```

---

## 5. Pair synchronization

一旦 Catalog Entry 为 `current`：

```text
zh-CN semantic change
      ↕
English semantic change
```

SHOULD 在同一个 PR 中同步。

后续 Guard 要逐步增加：

```text
pair identity check
same category/number check
translation state check
stale counterpart detection
broken-link detection
public terminology lint where practical
```

---

## 6. M4 — Remove Legacy Migration Zone

只有当所有公共文档都已有正式 Localized Pair、重要引用都迁移、Catalog 状态明确、CI 通过，才删除 Legacy Trees。

最终删除：

```text
docs/standards/
docs/design/
docs/reference-apps/
docs/governance/
docs/status/
docs/00_项目文档入口_Baga-Ink-Documentation-Index.md
```

之后 `tools/check_docs_i18n.py` MUST 从“锁定 Legacy”切换为：

> **Legacy public directories MUST NOT exist.**

---

## 7. Kindle engineering-plan exception

`docs/plans/platform-ports/kindle/` 不做全文多语言镜像。

继续采用：

```text
NNNN_中文名_English-Name.md
```

正文允许中文优先，因为这里会出现数百 Task / 数千 Execution Prompt。

但：

```text
外部实现者需要依赖的稳定结论
      ↓
MUST 回写 Public Localized Docs
```

---

## 8. Root multi-language entry model

当前：

```text
README.md              English default
README.zh-CN.md        Simplified Chinese
CONTRIBUTING.md        English default
CONTRIBUTING.zh-CN.md  Simplified Chinese
AGENTS.md              English AI/Automation entry
```

语言注册：

```text
docs/localization/readme-languages.json
```

未来可以按治理流程增加 `README.ja.md`、`README.de.md`、`README.fr.md` 等；禁止自行发明另一套语言目录结构。

---

## 9. Completion Gate

Public Documentation 国际化最终完成条件：

```text
[x] locale tree stable
[x] filename rules enforced
[x] README locale registry + CI
[x] Standards 00–13 localized
[ ] Standards 20–28 localized
[ ] Design localized
[ ] Reference Apps localized
[ ] all current pairs synchronized/reviewed
[ ] important old-path references migrated
[ ] legacy public directories removed
[ ] CI forbids legacy public directories
```

最终目标：

> **中国维护者和国际开发者可以从自己的语言入口理解、实现并审查同一套 Baga Ink Platform，而协议、代码、测试和架构不会因语言不同而分叉。**
