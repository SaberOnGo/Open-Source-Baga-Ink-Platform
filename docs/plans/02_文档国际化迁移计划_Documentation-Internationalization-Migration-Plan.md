# Baga Ink 文档国际化迁移计划 / Documentation Internationalization Migration Plan

> **文档级别：Implementation Plan / 文档基础设施迁移计划**  
> **状态：Plan Baseline v0.6**  
> **日期：2026-08-23**

## 0. Goal

把公共长期文档稳定迁移到 `docs/en/` 与 `docs/zh-CN/`，两种语言共享同一 Document Identity；Machine Spec / Code / Tests 不按语言分叉；高频工程 Task / Execution Prompt 不强制全文翻译。

## 1. Completed

```text
M0    Foundation / README / License / Guards          COMPLETE
M1-A  Governance + Status + Documentation Index      COMPLETE
M1-B1 Standards 00–06                                COMPLETE
M1-B2 Standards 07–13                                COMPLETE
M1-C  Standards 20–28                                COMPLETE
M1-D  Design 01–02                                   COMPLETE
```

M1-D current pairs:

```text
docs/en/design/01_baga-ink-executable-specification-design.md
docs/zh-CN/design/01_规范可执行化设计.md

docs/en/design/02_baga-ink-device-adapter-executable-contract-and-sdk-design.md
docs/zh-CN/design/02_设备适配器可执行契约与SDK设计.md
```

Catalog marks both Design documents `current`.

## 2. Next — M1-E Reference Apps

Migrate and fully localize:

```text
01 LifeBook Reference App
02 LifeBook Kindle Product Behavior / Accessories
03 Kindle Implementation Architecture Freeze
99 Superseded compatibility document
```

The Kindle Architecture Freeze is critical because international Kindle contributors must read exactly the same frozen implementation decisions as Chinese maintainers.

## 3. Final cleanup — M4

After M1-E:

1. update `AGENTS.md`, Status, Indexes and important Plans to localized paths;
2. set every Catalog `legacy_path` to `null`;
3. delete old `docs/standards/`, `docs/design/`, `docs/reference-apps/`, `docs/governance/`, `docs/status/`, and the old root documentation index;
4. retire/delete `docs/localization/legacy-lock.json`;
5. change `tools/check_docs_i18n.py` from Legacy-lock mode to **Legacy public paths MUST NOT exist**;
6. run Repository Documentation Guard and all existing Conformance CI;
7. merge only when green.

## 4. Permanent naming model

English public docs:

```text
NN_lowercase-kebab-case-name.md
```

Simplified Chinese public docs:

```text
NN_中文名称.md
```

Counterparts use the same stable Document Number / ID.

`docs/plans/platform-ports/` keeps its independent four-digit bilingual task/prompt rule.

## 5. Pair synchronization

For every Catalog Entry marked `current`, semantic changes SHOULD update maintained locale counterparts in the same reviewed PR. A translation cannot silently fork Architecture, Requirement, API Contract, Permission, Compatibility, Signing, or Security semantics.

## 6. Completion Gate

```text
[x] locale tree stable
[x] filename rules enforced
[x] README language registry + CI
[x] Governance / Status localized
[x] Standards 00–28 localized
[x] Design localized
[ ] Reference Apps localized
[ ] important old-path references migrated
[ ] Legacy Public Trees removed
[ ] CI forbids Legacy Public Trees
```

> **Final goal: Chinese and international contributors can implement and review the same Baga Ink Platform from their own language entry points without protocol or architecture forks.**
