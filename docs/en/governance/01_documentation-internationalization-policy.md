# Documentation Internationalization and Localization Policy

> **Document level:** Project governance  
> **Document ID:** `governance.localization.01`  
> **Locale:** English (`en`)  
> **Status:** Governance Baseline v1.0  
> **Date:** 2026-08-23  
> **Counterpart:** `docs/zh-CN/governance/01_文档国际化与本地化规范.md`

## 0. Purpose

Baga Ink is maintained by contributors from multiple countries and language communities. Public documentation is therefore localized by locale tree instead of mixing multiple human languages in every filename or paragraph.

Goals:

- international contributors can navigate complete English documentation;
- Chinese maintainers can work from complete Simplified Chinese technical documentation;
- human-language editions cannot drift into different protocols or architectures;
- machine-readable contracts, code, tests, identifiers, and tooling remain shared and English/language-neutral;
- high-volume operational engineering tasks do not need wasteful full localization.

## 1. Permanent locale architecture

Public long-lived prose exists only under:

```text
docs/en/
docs/zh-CN/
```

Governed public categories:

```text
standards/
design/
reference-apps/
governance/
status/
```

Historical mixed-language public directories are not supported and MUST NOT exist.

## 2. One logical document, multiple language editions

A localized pair is one logical document with multiple human-language editions.

A locale edition MUST NOT silently introduce a different:

```text
Architecture
Requirement
API Contract
Permission Rule
Compatibility Rule
Signing / Identity Rule
Distribution / Update Rule
Implementation Freeze
```

Authority order:

```text
machine-readable spec / schema / test vector / executable conformance evidence
        ↓ where applicable
approved project semantic decision + stable Document Identity
        ↓
maintained locale editions of that document
```

A prose conflict between maintained locales is a documentation defect and must be reconciled before the affected requirement can be treated as Stable.

## 3. Stable Document Identity

`docs/localization/catalog.json` records each public document's:

```text
id
category
number
en_path
zh_cn_path
status
legacy_path = null
```

The stable number is part of the document identity within its category.

Example:

```text
docs/en/standards/07_baga-ink-device-adapter-specification.md
docs/zh-CN/standards/07_设备适配器规范.md
```

Both represent Standard 07.

## 4. Filename rules

### English

```text
NN_lowercase-kebab-case-name.md
```

Requirements:

- two-digit stable number;
- ASCII lowercase kebab-case descriptive name;
- no Chinese characters;
- no duplicated Chinese + English name in one filename.

### Simplified Chinese

```text
NN_中文名称.md
```

Requirements:

- same stable number as English counterpart;
- Chinese descriptive name;
- canonical technical identities may remain in English where that improves precision;
- no redundant English suffix because the locale directory already identifies the audience.

Root repository exceptions such as `README.md`, `README.zh-CN.md`, `CONTRIBUTING.md`, `CONTRIBUTING.zh-CN.md`, and `AGENTS.md` are governed separately.

## 5. Content-language rules

English public files SHOULD use English prose.

Simplified Chinese files SHOULD explain prose in Chinese, while preserving stable technical identities such as:

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
BICTS
```

Do not mechanically translate identifiers in a way that creates a second technical vocabulary or incompatible API naming.

Canonical terminology is machine-tracked by:

```text
docs/localization/terminology.json
```

## 6. English/language-neutral implementation surfaces

These are not duplicated by locale:

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

Use English for:

- source filenames/directories outside localized prose trees;
- code identifiers, comments, and docstrings;
- public API/module names;
- JSON/YAML/TOML keys and schema IDs;
- machine error codes;
- CLI commands/flags;
- test names;
- dependency manifests;
- commit subjects and release tags.

## 7. Operational engineering plans are different

`docs/plans/` is an engineering work area, not a normative public protocol surface.

It is not required to duplicate every Task Design / AI Execution Prompt across locales.

In particular:

```text
docs/plans/platform-ports/kindle/
```

may remain Chinese-first under its strict searchable bilingual filename convention.

However:

> **A stable design fact that external implementers are expected to rely on MUST be promoted into localized Standards, Design, Reference Apps, Governance, or Status. It cannot remain authoritative only inside a maintainer-language task or prompt.**

## 8. Synchronization rule for maintained pairs

For a Catalog Entry marked `current`, semantic changes SHOULD update all maintained locale editions in the same reviewed PR.

If synchronization genuinely cannot be completed immediately, the Catalog must explicitly mark the affected edition as pending/stale; Stable release processes cannot treat the pair as synchronized.

`superseded` is a valid state for historical compatibility entries that intentionally remain non-authoritative.

## 9. Root repository language model

For international discoverability:

```text
README.md              → English default
README.zh-CN.md        → Simplified Chinese
CONTRIBUTING.md        → English default
CONTRIBUTING.zh-CN.md  → Simplified Chinese
AGENTS.md              → English AI/automation instructions
```

README locale registration lives at:

```text
docs/localization/readme-languages.json
```

Every current README locale must expose the same managed language-switch set.

## 10. Adding future locales

New locales such as `ja`, `de`, `fr`, or `ko` require an explicit governance change.

A maintained locale must have:

- a valid BCP 47-style locale tag;
- a registered README entry when the root README is translated;
- a locale documentation tree under `docs/<locale>/`;
- maintainers/review ownership;
- a glossary/terminology policy where needed;
- explicit Catalog synchronization state;
- CI validation.

Do not create ad-hoc alternatives such as:

```text
chinese/
english/
cn/
zh/
docs/standards/en/
```

## 11. AI / contributor hard gate

Before creating, renaming, moving, translating, or editing public long-lived documentation, contributors and AI agents MUST follow this policy.

Preferred scaffolder:

```text
python3 tools/new_localized_doc.py ...
```

Required validation:

```text
python3 tools/check_docs_i18n.py
```

CI rejects at least:

- recreation of legacy mixed-language public directories;
- invalid locale paths;
- invalid English/Chinese filenames;
- uncataloged public documents;
- duplicate Document IDs/target paths;
- non-null `legacy_path` after migration completion;
- missing counterparts for `current` / `superseded` documents;
- ad-hoc nested category structures.

Agents MUST NOT weaken the guard, broaden allowlists, or modify the Catalog merely to make an invalid layout pass.

## 12. Final rule

> **Public project knowledge is localized by locale tree; protocol and implementation contracts remain one project; operational engineering plans may stay maintainer-language; machine surfaces remain shared and English/language-neutral. No language edition may become a hidden fork of Baga Ink.**
