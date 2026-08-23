# Baga Ink 文档国际化迁移计划 / Documentation Internationalization Migration Plan

> **文档级别：Implementation Plan / 文档基础设施迁移计划**  
> **状态：Plan Baseline v0.7**  
> **日期：2026-08-23**

## Goal

公共长期文档使用 `docs/en/` 与 `docs/zh-CN/`；两种语言共享同一 Document Identity；Machine Spec / Code / Tests 不按语言分叉；高频工程 Task / Execution Prompt 不强制全文翻译。

## Completed localization milestones

```text
M0    Foundation / README / License / Guards          COMPLETE
M1-A  Governance + Status + Documentation Index      COMPLETE
M1-B1 Standards 00–06                                COMPLETE
M1-B2 Standards 07–13                                COMPLETE
M1-C  Standards 20–28                                COMPLETE
M1-D  Design 01–02                                   COMPLETE
M1-E  Reference Apps 01 / 02 / 03 / 99               COMPLETE
```

All maintained public-document locale pairs now exist.

Reference Apps:

```text
01 LifeBook Reference App                    current
02 LifeBook Kindle Product Behavior          current
03 Kindle Implementation Architecture Freeze current
99 Superseded compatibility entry            superseded
```

The current Kindle implementation baseline is:

```text
docs/zh-CN/reference-apps/03_Kindle具体实现架构冻结.md
docs/en/reference-apps/03_baga-ink-kindle-implementation-architecture-freeze.md
```

## Remaining work — M4 only

The internationalization migration is not finished until legacy mixed-language public paths are removed.

M4 sequence:

```text
1. Update AGENTS.md and remaining important old-path references
2. Set every catalog legacy_path to null
3. Delete old docs/standards/
4. Delete old docs/design/
5. Delete old docs/reference-apps/
6. Delete old docs/governance/
7. Delete old docs/status/
8. Delete old docs/00_项目文档入口_Baga-Ink-Documentation-Index.md
9. Remove legacy-lock.json
10. Change check_docs_i18n.py to forbid legacy public paths entirely
11. Update Status / Index / Governance to migration COMPLETE
12. Run Repository Documentation Guard + existing Conformance CI
```

## Permanent naming model

English:

```text
NN_lowercase-kebab-case-name.md
```

Simplified Chinese:

```text
NN_中文名称.md
```

Counterparts share the same stable number / Document ID.

`docs/plans/platform-ports/` retains its independent four-digit bilingual Task / Execution Prompt naming rule.

## Pair synchronization

For any Catalog Entry marked `current`, semantic changes SHOULD update maintained locale counterparts in the same reviewed PR. A language edition MUST NOT silently fork Architecture, Requirement, API Contract, Permission, Compatibility, Signing, Distribution, or Security semantics.

## Completion Gate

```text
[x] locale tree stable
[x] filename rules enforced
[x] README language registry + CI
[x] Governance / Status localized
[x] Standards 00–28 localized
[x] Design localized
[x] Reference Apps localized
[ ] old-path references migrated
[ ] Legacy Public Trees removed
[ ] CI forbids Legacy Public Trees
```

> **Final goal: international and Chinese contributors use different language entry points but implement and review one Baga Ink Platform.**
