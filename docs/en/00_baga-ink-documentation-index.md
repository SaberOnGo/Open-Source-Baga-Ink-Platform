# Baga Ink Documentation Index

> **Document level:** Project documentation entry point  
> **Document ID:** `docs.index.00`  
> **Locale:** English (`en`)  
> **Status:** Living Index v0.6  
> **Date:** 2026-08-23

## Start here

```text
README.md
→ docs/en/status/00_baga-ink-project-status.md
→ docs/en/standards/00_baga-ink-standards-index.md
→ relevant Design / Reference App / Plan
→ docs/en/governance/00_baga-ink-development-governance.md
```

AI / automation contributors also read `AGENTS.md`.

## Public locale model

```text
docs/en/{standards,design,reference-apps,governance,status}/
docs/zh-CN/{standards,design,reference-apps,governance,status}/
```

Matching Document ID / number means one logical document, not a language fork.

## Current Standards

All Standards 00–13 and 20–28 are `current` in both maintained locales.

Key English entry points:

```text
App / API / IKP
→ docs/en/standards/02_baga-ink-app-standard.md
→ docs/en/standards/03_baga-ink-api-specification.md
→ docs/en/standards/06_ikp-package-specification.md

Device / OEM porting
→ docs/en/standards/07_baga-ink-device-adapter-specification.md
→ docs/en/standards/10_baga-ink-compatibility-test-suite.md

Kindle
→ docs/en/standards/11_baga-ink-kindle-adapter.md

Android E-Paper
→ docs/en/standards/12_baga-ink-android-e-paper-adapter.md

Distribution / Market
→ docs/en/standards/20_baga-ink-market-and-distribution-architecture.md
→ Standards 21–28
```

## Current Design — CURRENT

```text
Executable Specification Design
→ docs/en/design/01_baga-ink-executable-specification-design.md

Device Adapter Executable Contract / SDK Design
→ docs/en/design/02_baga-ink-device-adapter-executable-contract-and-sdk-design.md
```

Both have maintained Simplified Chinese counterparts and Catalog status `current`.

## Next localization work

```text
M1-E  Reference Apps
M4    remove Legacy Public Trees and forbid them in CI
```

Reference Apps include LifeBook and the Kindle Implementation Architecture Freeze.

## Engineering plans

`docs/plans/` is operational engineering material and is not fully locale-mirrored. `docs/plans/platform-ports/kindle/` may remain Chinese-first under its strict bilingual filename / Task / Execution Prompt rules. Stable external-facing decisions MUST be promoted into localized public docs.

## Machine/code surfaces

`spec/`, `reference/`, `tests/`, `tools/`, `.github/`, `platform/`, `sdk/`, and `client/` remain English/language-neutral.

## Migration governance

Until final cleanup, old mixed-language public paths are frozen migration inputs tracked by `docs/localization/catalog.json` and `docs/localization/legacy-lock.json`.

Migration plan:

```text
docs/plans/02_文档国际化迁移计划_Documentation-Internationalization-Migration-Plan.md
```

Current milestones:

```text
M0    Foundation                    COMPLETE
M1-A  Governance / Status / Index   COMPLETE
M1-B1 Standards 00–06               COMPLETE
M1-B2 Standards 07–13               COMPLETE
M1-C  Standards 20–28               COMPLETE
M1-D  Design                        COMPLETE
M1-E  Reference Apps                NEXT
M4    Legacy removal                PENDING
```
