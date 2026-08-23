# Baga Ink 文档国际化迁移计划 / Documentation Internationalization Migration Plan

> **文档级别：Implementation Plan / 文档基础设施迁移计划**  
> **状态：Plan Baseline v0.5**  
> **日期：2026-08-23**  
> **上位治理：`docs/en/governance/01_documentation-internationalization-policy.md` / `docs/zh-CN/governance/01_文档国际化与本地化规范.md`**

## 0. Goal

把早期中文为主、文件名中英混合的 Public Docs 迁移成稳定的：

```text
docs/en/
docs/zh-CN/
```

并保证两种语言对应同一 Document Identity；Machine Spec / Code / Tests 不按语言分叉；海量工程 Task / Execution Prompt 不强制全文翻译。

---

## 1. Final structure

```text
docs/
├── en/{standards,design,reference-apps,governance,status}/
├── zh-CN/{standards,design,reference-apps,governance,status}/
├── plans/
└── localization/
    ├── catalog.json
    ├── terminology.json
    ├── legacy-lock.json
    └── readme-languages.json
```

最终删除旧：

```text
docs/standards/
docs/design/
docs/reference-apps/
docs/governance/
docs/status/
docs/00_项目文档入口_Baga-Ink-Documentation-Index.md
```

---

## 2. Naming

English:

```text
NN_lowercase-kebab-case-name.md
```

Simplified Chinese:

```text
NN_中文名称.md
```

Counterparts MUST use the same stable number / Document ID.

`docs/plans/platform-ports/` keeps the separate four-digit bilingual task/prompt rule.

---

## 3. Completed milestones

### M0 — Foundation — COMPLETE

```text
README / CONTRIBUTING locale model
Apache-2.0 / NOTICE / third-party boundary
docs/en + docs/zh-CN
catalog / terminology / legacy lock / README locale registry
scaffolders + validators
AGENTS hard gates
Repository Documentation Guard
GitHub main Ruleset / required check
```

### M1-A — Governance + Status + Index — COMPLETE

Maintained bilingual pairs exist for Development Governance, Documentation i18n Policy, Project Status, and Documentation Index.

### M1-B1 — Standards 00–06 — COMPLETE

```text
Standards Index
Platform Strategy / Architecture
App Standard
API Specification
Capability Registry
Permission Model
IKP Package Specification
```

### M1-B2 — Standards 07–13 — COMPLETE

```text
Device Adapter Contract
Compatibility Standard
UI Specification
BICTS
Kindle Device Adapter
Android E-Paper Adapter
Standard Libraries / Adopted Components
```

### M1-C — Standards 20–28 — COMPLETE

```text
Market and Distribution Architecture
Publisher Identity and App Ownership
IKP Signing and Key Lifecycle
Repository Metadata and Index Protocol
App Publishing, Review and Version Policy
Update, Rollback and Revocation Protocol
Distribution Client and Offline Transfer Protocol
Transparency and Security Audit Standard
Catalog and App Discovery Specification
```

All Standards 00–13 and 20–28 now have full maintained English and Simplified Chinese editions and Catalog status `current`.

---

## 4. Next — M1-D Design

Migrate and fully localize:

```text
01 Executable Specification Design
02 Device Adapter Executable Contract / SDK Design
```

Targets:

```text
docs/en/design/01_baga-ink-executable-specification-design.md
docs/zh-CN/design/01_规范可执行化设计.md

docs/en/design/02_baga-ink-device-adapter-executable-contract-and-sdk-design.md
docs/zh-CN/design/02_设备适配器可执行契约与SDK设计.md
```

---

## 5. Then — M1-E Reference Apps

```text
01 LifeBook Reference App
02 LifeBook Kindle Product Behavior / Accessories
03 Kindle Implementation Architecture Freeze
99 Superseded compatibility document
```

The Kindle Architecture Freeze is especially important because international Kindle contributors must be able to read the same frozen implementation decisions as Chinese maintainers.

---

## 6. M4 — Remove Legacy Migration Zone

After all maintained public pairs exist and important references are migrated:

1. update AGENTS / Status / Index / Plans to localized paths;
2. set every Catalog `legacy_path` to `null`;
3. delete old mixed-language public files/directories;
4. remove/retire `legacy-lock.json`;
5. change `tools/check_docs_i18n.py` from legacy-lock mode to **forbid legacy public directories entirely**;
6. run Repository Documentation Guard + all existing Conformance CI;
7. merge only if green.

---

## 7. Pair synchronization rule

For a Catalog Entry marked `current`:

```text
zh-CN semantic change
      ↕
English semantic change
```

SHOULD occur in the same reviewed PR. A language edition cannot silently fork Architecture, Requirement, API Contract, Permission, Compatibility, Signing, or Security semantics.

---

## 8. Kindle engineering-plan exception

`docs/plans/platform-ports/kindle/` remains operational engineering material and does not receive full locale mirroring.

It keeps:

```text
NNNN_中文名_English-Name.md
```

Stable facts required by external implementers MUST be promoted into localized Public Docs.

---

## 9. Completion Gate

```text
[x] locale tree stable
[x] filename rules enforced
[x] README language registry + CI
[x] Governance / Status localized
[x] Standards 00–13 localized
[x] Standards 20–28 localized
[ ] Design localized
[ ] Reference Apps localized
[ ] important old-path references migrated
[ ] Legacy Public Trees removed
[ ] CI forbids Legacy Public Trees
```

Final goal:

> **A Chinese maintainer and an international developer can understand, implement, review, and extend the same Baga Ink Platform from their own language entry point without creating protocol or architecture forks.**
