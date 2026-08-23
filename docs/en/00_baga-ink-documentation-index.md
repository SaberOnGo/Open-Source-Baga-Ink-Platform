# Baga Ink Documentation Index

> **Document level:** Project documentation entry point  
> **Document ID:** `docs.index.00`  
> **Locale:** English (`en`)  
> **Status:** Living Index v0.2  
> **Date:** 2026-08-23

---

## 1. Start here

The long-term source of truth is the `main` branch: code, tests, machine-readable specifications, and approved documentation. Feature branches, chat history, and draft PR descriptions are not authoritative project memory.

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
relevant Standards
   ↓
relevant Design / Reference App / Plan
   ↓
docs/en/governance/00_baga-ink-development-governance.md
```

Current maintained governance:

```text
docs/en/governance/00_baga-ink-development-governance.md
docs/en/governance/01_documentation-internationalization-policy.md
```

---

## 2. Public documentation locales

Public, long-lived prose is organized by locale:

```text
docs/en/
docs/zh-CN/
```

Each locale mirrors these public categories:

```text
standards/
design/
reference-apps/
governance/
status/
```

A document number is a stable identity within its category. Example pair:

```text
docs/en/standards/07_baga-ink-device-adapter-specification.md
docs/zh-CN/standards/07_设备适配器规范.md
```

Both are editions of the same Standard 07, not separate protocols.

---

## 3. What is already migrated?

Current localized documents include:

```text
Documentation Index
→ docs/en/00_baga-ink-documentation-index.md

Development Governance
→ docs/en/governance/00_baga-ink-development-governance.md

Documentation i18n Policy
→ docs/en/governance/01_documentation-internationalization-policy.md

Project Status
→ docs/en/status/00_baga-ink-project-status.md
```

Standards, Design, and Reference Apps are being migrated in controlled batches. Their current paths and migration states are machine-tracked by:

```text
docs/localization/catalog.json
```

Do not treat a translation-pending document as a completed English Standard.

---

## 4. Filename rules

English public documents:

```text
NN_lowercase-kebab-case-name.md
```

Examples:

```text
00_baga-ink-standards-index.md
07_baga-ink-device-adapter-specification.md
11_baga-ink-kindle-adapter.md
```

Simplified Chinese public documents:

```text
NN_中文名称.md
```

Canonical technical identities such as `Baga Ink`, `IKP`, `Device Adapter Contract`, `Capability`, `SQLite`, `Automerge`, `KOReader`, `FBInk`, and API identifiers remain recognizable across locales.

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

API names, schema keys, error codes, CLI flags, source identifiers, code comments/docstrings, test names, dependency manifests, and commit subjects should use English.

---

## 6. Engineering plans are different

`docs/plans/` is a working engineering area, not a normative public protocol surface. It is not required to duplicate thousands of Task Design or AI Execution Prompt documents across languages.

In particular:

```text
docs/plans/platform-ports/kindle/
```

may remain Chinese-first with its governed bilingual semantic filename convention.

A stable fact that external implementers must rely on MUST be promoted into localized Standards, Design, Reference Apps, Governance, or Status rather than remaining authoritative only in an engineering task.

---

## 7. Migration status

The historical mixed-language public directories are frozen migration inputs:

```text
docs/standards/
docs/design/
docs/reference-apps/
docs/governance/
docs/status/
```

Their files are registered by `docs/localization/catalog.json` and protected by `docs/localization/legacy-lock.json` so agents cannot silently keep evolving the old layout.

Migration plan:

```text
docs/plans/02_文档国际化迁移计划_Documentation-Internationalization-Migration-Plan.md
```

Current milestone:

```text
M0   internationalization foundation       COMPLETE
M1-A governance + status + index           IN PROGRESS / first localized pair complete
M1-B Standards 00–13                       NEXT
```

---

## 8. Governance and contributing

Read:

```text
CONTRIBUTING.md
docs/en/governance/00_baga-ink-development-governance.md
docs/en/governance/01_documentation-internationalization-policy.md
```

AI / automation contributors MUST also follow:

```text
AGENTS.md
```

The repository guards documentation structure, language paths, README locale switching, and high-volume Platform Port task layout in CI.
