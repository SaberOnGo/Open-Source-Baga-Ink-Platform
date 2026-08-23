# Baga Ink Documentation Index

> **Document level:** Project documentation entry point  
> **Document ID:** `docs.index.00`  
> **Locale:** English (`en`)  
> **Status:** Living Index v0.5  
> **Date:** 2026-08-23

---

## 1. Start here

The long-term source of truth is `main`: code, tests, machine-readable specifications, and approved public documentation.

Recommended reading order:

```text
README.md
  ↓
docs/en/status/00_baga-ink-project-status.md
  ↓
docs/en/standards/00_baga-ink-standards-index.md
  ↓
relevant Design / Reference App / Plan
  ↓
docs/en/governance/00_baga-ink-development-governance.md
```

AI / automation contributors MUST also read `AGENTS.md`.

---

## 2. Locale model

Public long-lived prose lives under:

```text
docs/en/
docs/zh-CN/
```

with mirrored categories:

```text
standards/
design/
reference-apps/
governance/
status/
```

Matching Document ID / number means one logical document, not a language-specific fork.

---

## 3. Standards — all current

### Platform / App / Device — 00–13

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
11 Kindle Device Adapter
12 Android E-Paper Adapter
13 Standard Libraries / Adopted Components
```

### Market / Distribution / Supply Chain — 20–28

```text
20 Market and Distribution Architecture
21 Publisher Identity and App Ownership
22 IKP Signing and Key Lifecycle
23 Repository Metadata and Index Protocol
24 App Publishing, Review and Version Policy
25 Update, Rollback and Revocation Protocol
26 Distribution Client and Offline Transfer Protocol
27 Transparency and Security Audit Standard
28 Catalog and App Discovery Specification
```

All Standards 00–13 and 20–28 have maintained English editions under `docs/en/standards/`, Simplified Chinese counterparts under `docs/zh-CN/standards/`, and `current` status in `docs/localization/catalog.json`.

Key entry points:

```text
App developers
→ docs/en/standards/02_baga-ink-app-standard.md
→ docs/en/standards/03_baga-ink-api-specification.md
→ docs/en/standards/06_ikp-package-specification.md

Device / OEM porters
→ docs/en/standards/07_baga-ink-device-adapter-specification.md
→ docs/en/standards/10_baga-ink-compatibility-test-suite.md

Kindle
→ docs/en/standards/11_baga-ink-kindle-adapter.md

Android E-Paper
→ docs/en/standards/12_baga-ink-android-e-paper-adapter.md

Repository / Market / distribution implementers
→ docs/en/standards/20_baga-ink-market-and-distribution-architecture.md
→ Standards 21–28
```

---

## 4. Next localization work

```text
M1-D  Design
M1-E  Reference Apps
M4    remove Legacy Public Trees and forbid them in CI
```

Design targets include the executable-specification design and Device Adapter IDL/SDK design. Reference Apps include LifeBook and the Kindle Implementation Architecture Freeze.

---

## 5. Engineering plans

`docs/plans/` is operational engineering material and is not fully mirrored by locale.

In particular:

```text
docs/plans/platform-ports/kindle/
```

may remain Chinese-first with governed bilingual semantic filenames, versioned Task Designs, and Execution Prompts.

Stable facts required by external implementers MUST be promoted to localized public Standards / Design / Reference Apps / Governance / Status.

---

## 6. Machine/code surfaces

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

API identifiers, schema keys, machine error codes, source identifiers, code comments/docstrings, test names, dependency manifests, and commit subjects use English.

---

## 7. Migration governance

Historical mixed-language public paths remain temporarily hash-locked migration inputs. Their identity/state is tracked by:

```text
docs/localization/catalog.json
docs/localization/legacy-lock.json
```

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
M1-D  Design                        NEXT
M1-E  Reference Apps                PENDING
M4    Legacy removal                PENDING
```

---

## 8. Governance / contributing

```text
CONTRIBUTING.md
docs/en/governance/00_baga-ink-development-governance.md
docs/en/governance/01_documentation-internationalization-policy.md
```

Repository CI validates documentation locale structure, README language switching, and high-volume Platform Port task/prompt structure.
