# Baga Ink Documentation Index

> **Document level:** Project documentation entry point  
> **Document ID:** `docs.index.00`  
> **Locale:** English (`en`)  
> **Status:** Living Index v0.7  
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

## Localized public documentation — complete pairs

The maintained locale trees are:

```text
docs/en/
docs/zh-CN/
```

The following public categories now have maintained English and Simplified Chinese editions:

```text
Standards       00–13, 20–28
Design          01–02
Reference Apps  01, 02, 03, 99
Governance      00–01
Status          00
Documentation Index 00
```

`reference-apps.99` is intentionally marked `superseded`; it is a compatibility/history entry, not a current Kindle implementation baseline.

## Key Standards

```text
App developers
→ docs/en/standards/02_baga-ink-app-standard.md
→ docs/en/standards/03_baga-ink-api-specification.md
→ docs/en/standards/06_ikp-package-specification.md

Device / OEM porters
→ docs/en/standards/07_baga-ink-device-adapter-specification.md
→ docs/en/standards/10_baga-ink-compatibility-test-suite.md

Kindle Adapter
→ docs/en/standards/11_baga-ink-kindle-adapter.md

Android E-Paper Adapter
→ docs/en/standards/12_baga-ink-android-e-paper-adapter.md

Distribution / Market
→ docs/en/standards/20_baga-ink-market-and-distribution-architecture.md
→ Standards 21–28
```

## Key Design

```text
Executable Specification Design
→ docs/en/design/01_baga-ink-executable-specification-design.md

Device Adapter IDL / SDK Design
→ docs/en/design/02_baga-ink-device-adapter-executable-contract-and-sdk-design.md
```

## Reference Apps

```text
LifeBook Reference App
→ docs/en/reference-apps/01_lifebook-reference-app.md

LifeBook Kindle product behavior / accessories
→ docs/en/reference-apps/02_lifebook-kindle-product-behavior-and-accessory-extension-design.md

Kindle Implementation Architecture Freeze
→ docs/en/reference-apps/03_baga-ink-kindle-implementation-architecture-freeze.md

Superseded compatibility entry
→ docs/en/reference-apps/99_lifebook-architecture-and-kindle-compatibility-superseded.md
```

For Kindle implementation, **03 Kindle Implementation Architecture Freeze** is the current implementation baseline subordinate to Standards.

## Engineering plans

`docs/plans/` remains operational engineering material and is not fully mirrored by locale. Kindle work remains under:

```text
docs/plans/platform-ports/kindle/
```

Stable external-facing conclusions MUST be promoted into localized public docs.

## Next: final migration cleanup

All maintained public-document pairs now exist. The remaining documentation-internationalization task is M4:

```text
update remaining old-path references
set Catalog legacy_path values to null
delete old mixed-language public trees
retire legacy-lock.json
change CI from legacy-lock mode to legacy-path-forbidden mode
```

Migration plan:

```text
docs/plans/02_文档国际化迁移计划_Documentation-Internationalization-Migration-Plan.md
```
