# Baga Ink Documentation Index

> **Document level:** Project documentation entry point  
> **Document ID:** `docs.index.00`  
> **Locale:** English (`en`)  
> **Status:** Living Index v0.3  
> **Date:** 2026-08-23

---

## 1. Start here

The long-term source of truth is `main`: code, tests, machine-readable specifications, and approved public documentation. Feature branches, chat history, and draft PR descriptions are not authoritative project memory.

Recommended reading order:

```text
README.md
   ↓
AGENTS.md                         (AI / automation contributors)
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

### Governance / Status

```text
Development Governance
→ docs/en/governance/00_baga-ink-development-governance.md

Documentation i18n Policy
→ docs/en/governance/01_documentation-internationalization-policy.md

Project Status
→ docs/en/status/00_baga-ink-project-status.md
```

### Standards 00–06 — CURRENT

```text
00  docs/en/standards/00_baga-ink-standards-index.md
01  docs/en/standards/01_baga-ink-platform-strategy.md
02  docs/en/standards/02_baga-ink-app-standard.md
03  docs/en/standards/03_baga-ink-api-specification.md
04  docs/en/standards/04_baga-ink-capability-registry.md
05  docs/en/standards/05_baga-ink-permission-model.md
06  docs/en/standards/06_ikp-package-specification.md
```

These have maintained Simplified Chinese counterparts under `docs/zh-CN/standards/` and are marked `current` in `docs/localization/catalog.json`.

### Next standards migration batch

```text
07  Device Adapter Contract
08  Compatibility Standard
09  UI Specification
10  BICTS
11  Kindle Adapter
12  Android E-Paper Adapter
13  Standard Libraries / Adopted Components
```

Until a document is `current` in the catalog, use the catalog to resolve its migration state rather than assuming the new English target path is complete.

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
platform/     future/reference product source
sdk/          future generated/platform SDK
client/       future Baga Ink Client
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
M1-B2 Standards 07–13                          NEXT
```

---

## 8. Governance and contributing

Read:

```text
CONTRIBUTING.md
docs/en/governance/00_baga-ink-development-governance.md
docs/en/governance/01_documentation-internationalization-policy.md
```

AI / automation contributors MUST also follow `AGENTS.md`.

Repository CI guards public-document paths, locale structure, README language switching, and Platform Port task/prompt layout.
