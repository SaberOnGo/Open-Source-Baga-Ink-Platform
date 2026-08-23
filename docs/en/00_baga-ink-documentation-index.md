# Baga Ink Documentation Index

> **Document level:** Project documentation entry point  
> **Document ID:** `docs.index.00`  
> **Locale:** English (`en`)  
> **Status:** Living Index v0.4  
> **Date:** 2026-08-23

---

## 1. Start here

The long-term source of truth is `main`: code, tests, machine-readable specifications, and approved public documentation. Feature branches, chat history, and draft PR descriptions are not authoritative project memory.

Recommended reading order:

```text
README.md
   ↓
docs/en/00_baga-ink-documentation-index.md
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

## 2. Public documentation locales

Public, long-lived prose is organized by locale:

```text
docs/en/
docs/zh-CN/
```

Each locale mirrors:

```text
standards/
design/
reference-apps/
governance/
status/
```

A shared number / Document ID means one logical document. English and Simplified Chinese editions are not separate protocols.

---

## 3. Current localized public documents

### Governance / Status — CURRENT

```text
Development Governance
→ docs/en/governance/00_baga-ink-development-governance.md

Documentation i18n Policy
→ docs/en/governance/01_documentation-internationalization-policy.md

Project Status
→ docs/en/status/00_baga-ink-project-status.md
```

### Standards 00–13 — CURRENT

```text
00  Standards Index
01  Platform Strategy / Architecture
02  App Standard
03  API Specification
04  Capability Registry
05  Permission Model
06  IKP Package Specification
07  Device Adapter Contract
08  Compatibility Standard
09  UI Specification
10  BICTS / Compatibility Test Suite
11  Kindle Device Adapter
12  Android E-Paper Adapter
13  Standard Libraries / Adopted Components
```

English paths live under `docs/en/standards/`; maintained Simplified Chinese counterparts live under `docs/zh-CN/standards/`. All of Standards 00–13 are marked `current` in `docs/localization/catalog.json`.

For device/OEM work, the most important current English path is:

```text
docs/en/standards/07_baga-ink-device-adapter-specification.md
```

For Kindle work:

```text
docs/en/standards/11_baga-ink-kindle-adapter.md
```

For Android E-Paper work:

```text
docs/en/standards/12_baga-ink-android-e-paper-adapter.md
```

### Next public-document migration batch

```text
Standards 20–28
→ Market / Distribution / Signing / Repository / Update / Catalog
```

Design and Reference Apps follow after the distribution standards batch.

---

## 4. Filename rules

English public docs:

```text
NN_lowercase-kebab-case-name.md
```

Simplified Chinese public docs:

```text
NN_中文名称.md
```

Canonical identities such as `Baga Ink`, `IKP`, `Device Adapter Contract`, `Capability`, `SQLite`, `Automerge`, `KOReader`, and `FBInk` remain recognizable across locales.

---

## 5. Machine-readable and code surfaces

These remain English/language-neutral and are not duplicated by locale:

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

API names, schema keys, error codes, CLI flags, source identifiers, code comments/docstrings, test names, dependency manifests, and commit subjects use English.

---

## 6. Engineering plans are different

`docs/plans/` is a working engineering area, not a normative public protocol surface. It is not required to duplicate thousands of Task Design or AI Execution Prompt documents across languages.

In particular:

```text
docs/plans/platform-ports/kindle/
```

may remain Chinese-first with its governed bilingual semantic filename convention.

A stable fact external implementers must rely on MUST be promoted into localized Standards, Design, Reference Apps, Governance, or Status.

---

## 7. Migration status

Historical mixed-language public directories are frozen migration inputs:

```text
docs/standards/
docs/design/
docs/reference-apps/
docs/governance/
docs/status/
```

They are tracked by `docs/localization/catalog.json` and locked by `docs/localization/legacy-lock.json`.

Migration plan:

```text
docs/plans/02_文档国际化迁移计划_Documentation-Internationalization-Migration-Plan.md
```

Current milestone:

```text
M0    internationalization foundation          COMPLETE
M1-A  Governance + Status + Index              COMPLETE
M1-B1 Standards 00–06                          COMPLETE
M1-B2 Standards 07–13                          COMPLETE
M1-C  Standards 20–28                          NEXT
M1-D  Design                                   PENDING
M1-E  Reference Apps                           PENDING
M4    Remove legacy public trees               PENDING
```

---

## 8. Governance and contributing

Read:

```text
CONTRIBUTING.md
docs/en/governance/00_baga-ink-development-governance.md
docs/en/governance/01_documentation-internationalization-policy.md
```

Repository CI guards public-document paths, locale structure, README language switching, and Platform Port task/prompt layout.
