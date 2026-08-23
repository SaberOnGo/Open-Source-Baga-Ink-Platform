# Baga Ink Documentation Index

> **Document level:** Project documentation entry point  
> **Document ID:** `docs.index.00`  
> **Locale:** English (`en`)  
> **Status:** Living Index v0.8  
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

## Public documentation architecture

The permanent maintained locale trees are:

```text
docs/en/
docs/zh-CN/
```

Current localized public coverage:

```text
Standards       00–13, 20–28
Design          01–02
Reference Apps  01, 02, 03, 99
Governance      00–02
Status          00
Documentation Index 00
```

The old mixed-language public directories are gone and CI rejects their recreation.

`reference-apps.99` is intentionally `superseded`; it is a history/compatibility entry, not the current Kindle implementation baseline.

## App developers

```text
App Standard
→ docs/en/standards/02_baga-ink-app-standard.md

API Specification
→ docs/en/standards/03_baga-ink-api-specification.md

Capability Registry
→ docs/en/standards/04_baga-ink-capability-registry.md

Permission Model
→ docs/en/standards/05_baga-ink-permission-model.md

IKP Package Specification
→ docs/en/standards/06_ikp-package-specification.md

Standard Libraries
→ docs/en/standards/13_baga-ink-standard-libraries-and-adopted-components.md
```

## Device / OEM porters

```text
Device Adapter Contract
→ docs/en/standards/07_baga-ink-device-adapter-specification.md

BICTS
→ docs/en/standards/10_baga-ink-compatibility-test-suite.md

Kindle Adapter
→ docs/en/standards/11_baga-ink-kindle-adapter.md

Android E-Paper Adapter
→ docs/en/standards/12_baga-ink-android-e-paper-adapter.md

Device Adapter IDL / SDK Design
→ docs/en/design/02_baga-ink-device-adapter-executable-contract-and-sdk-design.md
```

## Market / distribution implementers

Start with:

```text
docs/en/standards/20_baga-ink-market-and-distribution-architecture.md
```

then Standards 21–28 for Publisher Identity, Signing, Repository, Publishing, Update/Rollback/Revocation, Offline Transfer, Transparency, and Catalog/Discovery.

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

For Kindle implementation, **Reference App 03** is the current frozen implementation baseline subordinate to Standards.

## Governance

```text
Development Governance
→ docs/en/governance/00_baga-ink-development-governance.md

Documentation i18n / localization
→ docs/en/governance/01_documentation-internationalization-policy.md

Licensing architecture
→ docs/en/governance/02_baga-ink-licensing-policy.md
```

Commercial licensing entry point:

```text
COMMERCIAL_LICENSE.md
```

Historical license cutover:

```text
LICENSE_HISTORY.md
```

## Engineering plans

`docs/plans/` remains operational engineering material and is not fully mirrored by locale.

Kindle engineering work remains under:

```text
docs/plans/platform-ports/kindle/
```

Stable facts required by external implementers MUST be promoted into localized Standards / Design / Reference Apps / Governance / Status.

## Machine / code surfaces

These remain English/language-neutral:

```text
spec/
reference/
tests/
tools/
.github/
platform/
sdk/
client/
```

API identifiers, schema keys, source identifiers, machine error codes, code comments/docstrings, test names, dependency manifests, and commit subjects use English.

## Current project state

Canonical status:

```text
docs/en/status/00_baga-ink-project-status.md
```

The project is still in Standards + Executable Conformance + Reference Platform implementation preparation. Documentation internationalization is complete; real device implementation and formal Compatibility evidence remain in progress.
