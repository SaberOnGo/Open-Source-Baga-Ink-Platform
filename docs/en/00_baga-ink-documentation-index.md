# Baga Ink Documentation Index

> **Document level:** Project documentation entry point  
> **Locale:** English (`en`)  
> **Status:** Internationalization foundation v0.1  
> **Date:** 2026-08-23

## 1. Source-of-truth order

The long-term source of truth is the `main` branch: code, tests, machine-readable specifications, and approved documentation. Feature branches, chat history, and draft PR descriptions are not authoritative project memory.

Recommended reading order for international contributors:

```text
AGENTS.md
   ↓
docs/README.md
   ↓
docs/en/00_baga-ink-documentation-index.md
   ↓
docs/en/status/...
   ↓
docs/en/standards/...
   ↓
docs/en/governance/...
   ↓
relevant Design / Reference App / Plan
```

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

A document number is a stable identity within its category. Example target pair:

```text
docs/en/standards/07_baga-ink-device-adapter-specification.md
docs/zh-CN/standards/07_设备适配器规范.md
```

Both are language editions of the same Standard 07. They are not separate protocols.

## 3. Filename rules

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

Canonical technical names such as `Baga Ink`, `IKP`, `Device Adapter Contract`, `Capability`, `SQLite`, `Automerge`, `KOReader`, `FBInk`, and API identifiers may remain in English when translation would obscure identity.

## 4. Machine-readable and code surfaces

The following remain English/language-neutral and are not duplicated by locale:

```text
spec/
reference/
tests/
tools/
.github/
platform/     (future product source)
sdk/          (future SDK source)
client/       (future client source)
```

Public API names, schema keys, error codes, CLI flags, source identifiers, code comments/docstrings, commit subjects, and machine-readable metadata should use English.

## 5. Engineering plans are different

`docs/plans/` is a working engineering area, not a normative public protocol surface. It is not required to duplicate thousands of Task Design or AI Execution Prompt documents across languages.

In particular, `docs/plans/platform-ports/kindle/` may remain Chinese-first with bilingual semantic filenames because it is the maintainer's operational work area. Stable decisions that external developers must rely on must be reflected in localized Standards, Design, Reference Apps, Governance, or Status documents.

## 6. Migration status

The original public documentation currently lives in the legacy directories:

```text
docs/standards/
docs/design/
docs/reference-apps/
docs/governance/
docs/status/
```

Those directories are frozen as a migration zone. Their exact files and target locale paths are tracked by `docs/localization/catalog.json`.

Migration proceeds according to:

```text
docs/plans/02_文档国际化迁移计划_Documentation-Internationalization-Migration-Plan.md
```

Until a document is marked `current` in the localization catalog, its English edition may still be pending. Pending translation must be explicit; it must never be presented as a finished English Standard.

## 7. Localization policy

Read:

```text
docs/en/governance/01_documentation-internationalization-policy.md
```

It defines language authority, synchronization, terminology, file naming, migration, and CI rules.
