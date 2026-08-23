# Baga Ink 文档国际化迁移计划 / Documentation Internationalization Migration Plan

> **文档级别：Implementation Plan / 文档基础设施迁移计划**  
> **状态：Plan Baseline v0.3**  
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
- `docs/plans/` 不因国际化而复制几千份 Task / AI Execution Prompt；
- Machine Spec、Reference Implementation、Tests、API / Schema / Code 保持英文或语言无关；
- 迁移过程中不通过盲目批量重命名/翻译破坏文档引用和架构边界。

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

最终删除旧公共目录：

```text
docs/standards/
docs/design/
docs/reference-apps/
docs/governance/
docs/status/
docs/00_项目文档入口_Baga-Ink-Documentation-Index.md
```

旧路径只在迁移阶段暂时存在，并由 Legacy Lock 冻结。

## 2. Naming rules

English public docs:

```text
NN_lowercase-kebab-case-name.md
```

Simplified Chinese public docs:

```text
NN_中文名称.md
```

同一 Category 内，中英文 Counterpart MUST 使用同一个稳定 `NN` / Document ID。

`docs/plans/platform-ports/` 继续使用自己的四位 Task / Prompt 编号规则。

---

## 3. Phase M0 — Internationalization foundation — COMPLETE

已经建立：

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

### M0 Gate

- [x] Final locale path model documented
- [x] New public docs cannot be added to legacy directories
- [x] Localized filename rules machine-checked
- [x] Catalog tracks migration/translation state
- [x] Terminology registry exists
- [x] Legacy public contents locked against in-place evolution
- [x] CI rejects invalid layouts
- [x] Kindle Task / Execution Prompt model remains independent
- [x] Root README is English default with scalable language switching
- [x] Apache-2.0 / third-party license boundaries explicit

---

## 4. Phase M1 — Move public working editions

每个批次建立可维护的中文版本与完整英文 Counterpart，并更新 Catalog / Index / references。

迁移必须：

1. 保留已批准的语义边界；
2. 不为了“中文化”改写 Canonical English technical identity；
3. 英文版必须完整可独立阅读，不能用空 Stub 冒充完成；
4. 修复相关相对链接与硬编码路径；
5. 更新 Documentation Index / Status / Plans / AGENTS 中的重要引用；
6. 更新 Catalog status；
7. 通过 Documentation Guard 与现有 Conformance CI；
8. 在所有旧引用迁完之前，Legacy Path MAY 暂时保留为冻结兼容入口。

### M1-A — Governance + Status + Documentation Index — COMPLETE

正式入口：

```text
docs/en/governance/00_baga-ink-development-governance.md
docs/zh-CN/governance/00_开发治理.md

docs/en/status/00_baga-ink-project-status.md
docs/zh-CN/status/00_当前项目状态.md

docs/en/00_baga-ink-documentation-index.md
docs/zh-CN/00_项目文档入口.md
```

Catalog 中 `governance.00` / `status.00` 已为 `current`。

### M1-B1 — Standards 00–06 — COMPLETE

已建立完整双语对：

```text
00 Standards Index
01 Platform Strategy / Architecture
02 App Standard
03 API Specification
04 Capability Registry
05 Permission Model
06 IKP Package Specification
```

English:

```text
docs/en/standards/00_baga-ink-standards-index.md
docs/en/standards/01_baga-ink-platform-strategy.md
docs/en/standards/02_baga-ink-app-standard.md
docs/en/standards/03_baga-ink-api-specification.md
docs/en/standards/04_baga-ink-capability-registry.md
docs/en/standards/05_baga-ink-permission-model.md
docs/en/standards/06_ikp-package-specification.md
```

Simplified Chinese:

```text
docs/zh-CN/standards/00_规范总览.md
docs/zh-CN/standards/01_顶层战略与架构.md
docs/zh-CN/standards/02_应用标准.md
docs/zh-CN/standards/03_API规范.md
docs/zh-CN/standards/04_能力注册表.md
docs/zh-CN/standards/05_权限模型.md
docs/zh-CN/standards/06_IKP应用包规范.md
```

Catalog 状态：`current`。

旧 `docs/standards/00...06...` 文件继续保持 Legacy Lock，只用于尚未迁移的旧路径兼容，不再原位演进。

### M1-B2 — Standards 07–13 — NEXT

```text
07 Device Adapter Contract
08 Compatibility Standard
09 UI Specification
10 BICTS
11 Kindle Adapter
12 Android E-Paper Adapter
13 Standard Libraries / Adopted Components
```

这是 OEM / third-party device porter 真正进入 Baga Device Porting 工作前最重要的国际化批次。

### M1-C — Standards 20–28

```text
Market / Distribution
Publisher Identity / Ownership
Signing / Key Lifecycle
Repository Metadata
Publishing / Version Policy
Update / Rollback / Revocation
Offline Transfer
Transparency / Security Audit
Catalog / Discovery
```

### M1-D — Design

```text
Executable Specification Design
Device Adapter Executable Contract / SDK Design
```

### M1-E — Reference Apps

```text
LifeBook Reference App
LifeBook Kindle Product Behavior / Accessories
Kindle Implementation Architecture Freeze
Superseded compatibility document
```

---

## 5. English edition quality rule

English is not considered complete merely because machine translation exists.

Translation MUST preserve:

- normative `MUST` / `SHOULD` / `MAY` semantics;
- API identifiers;
- field names;
- code blocks;
- version numbers;
- error codes;
- package names;
- project/library names;
- architecture boundaries.

AI MAY accelerate translation, but a document only becomes Catalog `current` after it is reviewed against the Chinese edition and relevant Machine Contract / Tests.

---

## 6. Phase M2 — Pair synchronization guard

Once a document is `current`:

```text
zh-CN semantic change
      ↕
English semantic change
```

SHOULD be updated in the same PR.

Guard SHOULD progressively add:

```text
pair identity check
same category/number check
translation state check
stale counterpart detection
broken-link detection
public terminology lint where practical
```

---

## 7. Phase M4 — Remove Legacy Migration Zone

A Legacy Document may be deleted only after:

```text
localized pair exists
+
important links updated
+
Catalog state explicit
+
CI pass
+
no remaining repository dependency on the old path
```

When migration is complete, delete:

```text
docs/standards/
docs/design/
docs/reference-apps/
docs/governance/
docs/status/
old documentation index
```

Then change the Guard from “locked Legacy list” to:

> **Legacy public directories MUST NOT exist.**

---

## 8. Plans / Kindle special rule

`docs/plans/platform-ports/kindle/` is not fully mirrored by locale.

Reason:

```text
hundreds of Task Designs
thousands of Execution Prompts
frequent debugging / real-device steps
```

Existing rule remains:

```text
NNNN_中文名_English-Name.md
```

Body may remain Chinese-first.

But:

```text
stable fact required by external implementers
      ↓
MUST be promoted into Public Localized Docs
```

---

## 9. Root repository internationalization

Current entrypoints:

```text
README.md              English default
README.zh-CN.md        Simplified Chinese
CONTRIBUTING.md        English default
CONTRIBUTING.zh-CN.md  Simplified Chinese
AGENTS.md              English AI/Automation entry
```

README locale registry:

```text
docs/localization/readme-languages.json
```

Future locales can add `README.ja.md`, `README.de.md`, `README.fr.md`, etc. through the governed registry rather than ad-hoc files.

---

## 10. Completion Gate

Public Documentation internationalization is complete only when:

```text
[ ] locale tree stable
[ ] filename rules enforced
[ ] legacy public dirs accept no new docs
[ ] public doc catalog complete
[ ] Chinese public editions migrated
[ ] English Standards complete
[ ] critical Design / Reference Apps complete in English
[ ] README / CONTRIBUTING locale model stable
[ ] CI checks locale structure and language switching
[ ] no Stable Standard relies on a stale required locale edition
[ ] legacy public directories removed
```

Final goal:

> **A Chinese maintainer and an international developer can understand and implement the same Baga Ink Platform from their own language entrypoint without causing protocol, code, test, or architecture forks.**
