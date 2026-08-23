# Baga Ink 文档国际化迁移计划 / Documentation Internationalization Migration Plan

> **文档级别：Implementation Plan / 文档基础设施迁移计划**  
> **状态：Plan Baseline v0.2**  
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
- Machine Spec、Reference Implementation、Tests、API/Schema/Code 保持英文/语言无关；
- 迁移过程中不通过盲目批量重命名/翻译破坏文档引用和架构边界。

## 1. Final target structure

```text
docs/
├── README.md
├── README.zh-CN.md
│
├── en/
│   ├── 00_baga-ink-documentation-index.md
│   ├── standards/
│   ├── design/
│   ├── reference-apps/
│   ├── governance/
│   └── status/
│
├── zh-CN/
│   ├── 00_项目文档入口.md
│   ├── standards/
│   ├── design/
│   ├── reference-apps/
│   ├── governance/
│   └── status/
│
├── plans/
│   └── ...
│
└── localization/
    ├── catalog.json
    ├── terminology.json
    └── legacy-lock.json
```

最终必须删除旧公共目录：

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

### English public docs

```text
NN_lowercase-kebab-case-name.md
```

### Simplified Chinese public docs

```text
NN_中文名称.md
```

同一 Category 内，中英文 Counterpart MUST 使用相同 `NN`。

Public Doc 的两位编号是稳定 Document Number，不是 Task 排序号，因此不机械改成四位。

`docs/plans/platform-ports/` 的四位编号规则继续独立生效，因为那里是大量 Task / Prompt 的工程工作区。

## 3. Phase M0 — Internationalization foundation — COMPLETE

已经建立：

```text
README.md / README.zh-CN.md
CONTRIBUTING.md / CONTRIBUTING.zh-CN.md

docs/en/00_baga-ink-documentation-index.md
docs/zh-CN/00_项目文档入口.md

docs/en/governance/01_documentation-internationalization-policy.md
docs/zh-CN/governance/01_文档国际化与本地化规范.md

docs/localization/catalog.json
docs/localization/terminology.json
docs/localization/legacy-lock.json
docs/localization/readme-languages.json

tools/check_docs_i18n.py
tools/check_readme_languages.py
tools/new_localized_doc.py

CI integration
AGENTS hard gate
GitHub main Ruleset / Required Check
```

旧公共目录已成为受 Machine Guard 约束的 Legacy Migration Zone。

### M0 Gate

- [x] Final path model documented
- [x] New public docs cannot be added to legacy directories
- [x] New localized docs have enforced filename rules
- [x] Catalog tracks migration/translation state
- [x] Terminology registry exists
- [x] Legacy public contents are locked against in-place evolution
- [x] CI rejects invalid layouts
- [x] Existing Kindle Task/Execution Prompt model remains independent
- [x] Root README is English default with scalable locale switching
- [x] Apache-2.0 / third-party license boundaries are explicit

## 4. Phase M1 — Move public working editions

迁移不是简单 `git mv`。每个批次同时建立可维护的中文版本和完整英文 Counterpart，并更新 Catalog / Index / references。

迁移时必须：

1. 保留已批准的语义边界；
2. 不为了“中文化”改写 Canonical English technical identity；
3. 英文版必须完整可独立阅读，不能用空 Stub 伪装成完成；
4. 修复所有相关相对链接和硬编码路径；
5. 更新 AGENTS / Documentation Index / Status / Plans 中的引用；
6. 更新 Catalog status；
7. 运行 Documentation Guard 与现有 Conformance CI；
8. 在所有旧引用迁完之前，Legacy Path MAY 暂时保留为冻结兼容入口。

### M1-A — Governance + Status + Documentation Index — COMPLETE

新正式入口：

```text
docs/en/governance/00_baga-ink-development-governance.md
docs/zh-CN/governance/00_开发治理.md

docs/en/status/00_baga-ink-project-status.md
docs/zh-CN/status/00_当前项目状态.md

docs/en/00_baga-ink-documentation-index.md
docs/zh-CN/00_项目文档入口.md
```

Catalog 中 `governance.00` 与 `status.00` 进入 `current`。

旧 `docs/governance/00_...` 与 `docs/status/00_...` 暂时继续作为 Legacy Compatibility Inputs，因为尚未迁移的 Standards / Plans 中仍可能存在旧路径引用；它们保持 locked，不再原位演进。

### M1-B — Standards 00–13 — NEXT

优先顺序：

```text
00 Standards Index
01 Platform Strategy / Architecture
02 App Standard
03 API Specification
04 Capability Registry
05 Permission Model
06 IKP Package Specification
07 Device Adapter Contract
08 Compatibility Standard
09 UI Specification
10 BICTS
11 Kindle Adapter
12 Android E-Paper Adapter
13 Standard Libraries / Adopted Components
```

这是国际开发者开始真正依据 Baga Ink Protocol / Porting Contract 工作的关键批次。

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

## 5. English edition quality rule

英文版不是机器翻译副本的“完成状态”。Translation MUST preserve:

- RFC 2119-style normative words where applicable (`MUST`, `SHOULD`, `MAY`);
- API identifiers;
- field names;
- code blocks;
- version numbers;
- error codes;
- package names;
- project/library names;
- architecture boundary meaning.

AI translation MAY accelerate work, but a document MUST be reviewed against the Chinese edition and Machine Contract before Catalog status becomes `current`.

## 6. Phase M2 — Pair synchronization guard

当一个文档进入 `current` 后：

```text
zh-CN semantic change
      ↕
English semantic change
```

SHOULD 在同一个 PR 中同步。

Guard 后续 SHOULD 逐步增加：

```text
pair identity check
same category/number check
translation state check
stale counterpart detection
broken link detection
public terminology lint where practical
```

不能把“英文没同步”隐藏成普通 Commit History 问题。

## 7. Phase M4 — Remove Legacy Migration Zone

只有当某个 Legacy Document 已经：

```text
localized pair exists
+
all important links updated
+
Catalog current/stale state explicit
+
CI pass
```

且仓库不再依赖旧路径时，才删除旧文件。

当所有 Legacy Entries 完成以后，整体删除：

```text
docs/standards/
docs/design/
docs/reference-apps/
docs/governance/
docs/status/
old documentation index
```

随后 Guard 从“锁定 Legacy 列表”切换成：

> **Legacy public directories MUST NOT exist.**

## 8. Plans / Kindle special rule

`docs/plans/platform-ports/kindle/` 不做全文双语镜像。

原因：

```text
Task Design 数百份
Execution Prompt 数千份
频繁调试 / 真机步骤
```

全部翻译会形成巨大同步负担，而且这些文档不是 Universal Contract。

现有规则继续：

```text
NNNN_中文名_English-Name.md
```

正文允许中文优先。

但是：

```text
外部实现者需要依赖的稳定结论
      ↓
MUST 回写 Public Localized Docs
```

## 9. Root repository internationalization

当前正式入口：

```text
README.md              English default
README.zh-CN.md        Simplified Chinese
CONTRIBUTING.md        English default
CONTRIBUTING.zh-CN.md  Simplified Chinese
AGENTS.md              English AI/Automation entry
```

README Locale Registry：

```text
docs/localization/readme-languages.json
```

未来可以按治理规则扩展 `README.ja.md`、`README.de.md`、`README.fr.md` 等，而不是临时手工散落语言文件。

## 10. Completion Gate

整个 Public Documentation 国际化完成的最低标准：

```text
[ ] locale tree stable
[ ] filename rules enforced
[ ] legacy public dirs no longer accept new docs
[ ] public doc catalog complete
[ ] Chinese public editions migrated
[ ] English Standards complete
[ ] critical Design / Reference Apps complete in English
[ ] README / CONTRIBUTING locale model stable
[ ] CI checks localization structure and locale switching
[ ] no Stable Standard relies on a stale required locale edition
[ ] legacy public directories removed
```

最终目标不是“翻译得多”，而是：

> **任何中国维护者或国际开发者，都可以从自己能读懂的入口理解同一套 Baga Ink Platform，而代码、协议、测试和文档不会因为语言不同而分叉。**
