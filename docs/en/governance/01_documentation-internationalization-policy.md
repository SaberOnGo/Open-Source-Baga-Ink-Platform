# Documentation Internationalization and Localization Policy

> **Document level:** Project governance  
> **Locale:** English (`en`)  
> **Status:** Governance baseline v0.1  
> **Date:** 2026-08-23  
> **Counterpart:** `docs/zh-CN/governance/01_文档国际化与本地化规范.md`

## 0. Purpose

Baga Ink is intended to be maintained by contributors from multiple countries and language communities. The repository therefore separates public documentation by locale instead of mixing Chinese and English in every filename or paragraph.

The goals are:

- Chinese maintainers can read and author complete technical explanations without working from an English-only repository;
- international contributors can navigate complete English documentation without parsing Chinese filenames;
- the two languages must not drift into separate protocols or architectures;
- machine-readable contracts, code, tests, identifiers, and tooling remain language-neutral/English;
- high-volume engineering work logs and AI execution prompts do not need wasteful full duplication across locales.

## 1. Locale architecture

Public, long-lived prose uses parallel locale trees:

```text
docs/en/
docs/zh-CN/
```

The following categories are public-localized categories:

```text
standards/
design/
reference-apps/
governance/
status/
```

The trees SHOULD mirror category and stable document number.

Example:

```text
docs/en/standards/07_baga-ink-device-adapter-specification.md
docs/zh-CN/standards/07_设备适配器规范.md
```

Both represent the same Standard 07.

## 2. There is one document identity, not one protocol per language

A localized pair is one logical document with multiple language editions.

A language edition MUST NOT silently introduce a different architecture, requirement, API contract, permission rule, compatibility rule, or implementation freeze.

Baga does **not** declare English or Chinese to be a separate semantic authority. The project authority order is:

```text
machine-readable specification / schema / test vector / executable conformance evidence
        ↓ where applicable
approved project semantic decision and stable document identity
        ↓
English and Chinese maintained editions of that same document
```

Where a prose-only semantic point is not covered by machine-readable material, a conflict between locales is an unresolved documentation defect. It MUST be reconciled before that requirement can be treated as a Stable release baseline.

## 3. Bootstrap migration exception

The repository existed before the locale split. During the one-time migration, an entry in `docs/localization/catalog.json` MAY be marked:

```text
migration-pending
translation-pending
```

This is a temporary bootstrap state, not permission for indefinite drift.

A pending English translation must be explicitly shown as pending and MUST NOT masquerade as a completed English Standard.

After a catalog entry reaches `current`, semantic changes SHOULD update both maintained locale editions in the same PR. If synchronization cannot be completed, the catalog MUST explicitly mark the counterpart stale/pending; a Stable release gate may not treat the pair as synchronized.

## 4. Filename rules

### English public documents

```text
NN_lowercase-kebab-case-name.md
```

Examples:

```text
00_baga-ink-standards-index.md
07_baga-ink-device-adapter-specification.md
11_baga-ink-kindle-adapter.md
```

Rules:

- the numeric prefix is the stable document number within the category;
- the descriptive name is ASCII lowercase kebab-case;
- no Chinese characters;
- no duplicated Chinese + English filename.

### Simplified Chinese public documents

```text
NN_中文名称.md
```

Examples:

```text
00_规范总览.md
07_设备适配器规范.md
11_Kindle适配规范.md
```

Rules:

- use the same stable document number as the English counterpart;
- use Chinese for the descriptive filename;
- canonical product/project/library/API terms may remain in English when they are technical identities;
- do not append a redundant English translation to the Chinese filename because the locale directory already identifies the audience.

## 5. Content-language rules

English files SHOULD be written in English. Chinese text is allowed only when it is literal user-facing data, a quoted proper name, or a language-specific example.

Chinese files SHOULD explain prose in Chinese. Do not mechanically translate stable technical identities when that reduces precision. Prefer forms such as:

```text
Baga Ink Platform
Baga Ink API
Baga Device Adapter Contract
IKP
Capability
Permission
SQLite
Automerge
KOReader
FBInk
KPM
MRPI
```

A Chinese document may explain these terms in Chinese, but the canonical identifiers themselves should remain recognizable.

## 6. Language-neutral / English-only engineering surfaces

The following are not duplicated by locale:

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

The following SHOULD use English:

- source filenames and directory names outside localized prose trees;
- code identifiers, comments, and docstrings;
- public API names and module names;
- JSON/YAML/TOML keys and schema identifiers;
- machine-readable error codes;
- CLI commands and flags;
- test names;
- dependency manifests;
- commit subjects and release tags.

This rule keeps the implementation interoperable even when maintainers speak different human languages.

## 7. Engineering plans are not required to be fully localized

`docs/plans/` is a working engineering area. It may contain maintainer-language material and is not required to duplicate every task and AI prompt across locales.

In particular, `docs/plans/platform-ports/kindle/` may remain Chinese-first with the existing searchable bilingual filename convention.

However:

> A design fact that external implementers are expected to rely on MUST eventually be reflected in localized Standards, Design, Reference Apps, Governance, or Status. It cannot remain authoritative only inside a Chinese Task Design or AI execution prompt.

## 8. Root repository language

For international discoverability:

```text
README.md              → English default
README.zh-CN.md        → Simplified Chinese counterpart
CONTRIBUTING.md        → English default when added
CONTRIBUTING.zh-CN.md  → Simplified Chinese counterpart when added
AGENTS.md              → English AI/automation instructions
```

This convention is an intentional exception to numbered public-document filenames.

## 9. Localization catalog

`docs/localization/catalog.json` tracks public-document identity and migration/synchronization state.

Each entry SHOULD include:

```text
id
category
number
legacy_path              when still migrating
zh_cn_path
en_path
status
```

Allowed lifecycle states include:

```text
migration-pending
translation-pending
current
stale
superseded
```

The catalog is machine-checked and must not be used to hide missing translation work.

## 10. AI and contributor workflow

Before creating or renaming a public documentation file, contributors and AI agents MUST read this policy and run the documentation guard.

When repository command execution is available, use the public-document scaffolder rather than inventing paths manually.

Required validation:

```text
python3 tools/check_docs_i18n.py
```

The CI gate must reject:

- new public docs created in legacy mixed-language directories;
- invalid locale directory names;
- mixed bilingual filenames inside locale trees;
- English public filenames containing Chinese;
- Chinese public filenames using a redundant English suffix convention;
- mismatched category/document number for a maintained pair;
- execution/public docs placed in the wrong documentation class;
- catalog entries pointing to impossible or conflicting paths.

Agents MUST NOT weaken the guard or edit the catalog merely to make an invalid layout pass.

## 11. Adding future locales

The initial maintained locales are:

```text
en
zh-CN
```

Future locales such as Japanese may be added only through an explicit governance change. A new locale must have:

- a locale directory using a valid BCP 47-style tag;
- maintainers/review ownership;
- a localization guide or glossary where needed;
- explicit synchronization status in the catalog;
- CI validation.

Do not create ad-hoc `chinese/`, `english/`, `cn/`, `zh/`, or language folders inside individual Standards.

## 12. Final rule

> **Public project knowledge is localized by locale tree; implementation contracts remain one project; working plans may stay maintainer-language; machine surfaces remain English/language-neutral; no language edition is allowed to become a hidden fork of Baga Ink.**
