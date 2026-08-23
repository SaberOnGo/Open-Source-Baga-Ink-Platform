# Documentation Internationalization and Localization Policy

> **Document level:** Project governance  
> **Document ID:** `governance.localization.01`  
> **Locale:** English (`en`)  
> **Status:** Governance Baseline v1.1  
> **Date:** 2026-08-23  
> **Counterpart:** `docs/zh-CN/governance/01_文档国际化与本地化规范.md`

## 0. Purpose

Baga Ink is maintained by contributors from multiple countries and language communities. Long-lived localized documentation is therefore organized by locale tree instead of mixing multiple human languages in every filename or paragraph.

Goals:

- international contributors can navigate complete English documentation;
- Chinese maintainers can work from complete Simplified Chinese technical documentation;
- human-language editions cannot drift into different protocols or architectures;
- machine-readable contracts, code, tests, identifiers, and tooling remain shared and English/language-neutral;
- high-volume operational engineering documents are not required to be duplicated across every locale;
- every tracked documentation file remains suitable for publication in a public repository.

## 1. Permanent locale architecture

Long-lived localized prose exists under:

```text
docs/en/
docs/zh-CN/
```

Governed localized categories:

```text
standards/
design/
reference-apps/
governance/
status/
```

Historical mixed-language public directories are retired and MUST NOT exist.

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

A prose conflict between maintained locales is a documentation defect and MUST be reconciled before the affected requirement can be treated as Stable.

## 3. Stable Document Identity

`docs/localization/catalog.json` records each localized public document's:

```text
id
category
number
en_path
zh_cn_path
status
legacy_path = null
```

The stable number is part of the Document Identity within its category.

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

- same stable number as the English counterpart;
- Chinese descriptive name;
- canonical technical identities may remain in English where that improves precision;
- no redundant English suffix because the locale directory already identifies the audience.

Root repository documents such as `README.md`, `README.zh-CN.md`, `CONTRIBUTING.md`, `CONTRIBUTING.zh-CN.md`, and `AGENTS.md` are governed separately for filename structure but remain subject to the repository-wide public writing rule.

## 5. Content-language rules

English localized files SHOULD use English prose.

Simplified Chinese files SHOULD use Chinese explanatory prose while preserving stable technical identities such as:

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

Identifiers MUST NOT be mechanically translated in a way that creates a second technical vocabulary or incompatible API naming.

Canonical terminology is machine-tracked by:

```text
docs/localization/terminology.json
```

## 6. Public writing voice applies to the whole repository

This repository is public. Any documentation file committed to it is public-facing material, regardless of whether it is a Standard, Governance document, README, engineering plan, Task Design, or AI Execution Prompt.

The localization model and the publication model are separate concerns:

```text
Localized Standards / Design / Reference Apps / Governance / Status
        → mirrored by maintained locale where required

Operational engineering plans under docs/plans/
        → not required to be mirrored by locale

Both classes
        → public, third-party-readable, publication-quality prose
```

All tracked documentation MUST be understandable without private chat context and MUST use language appropriate to its intended external audience.

Public prose MUST NOT contain private-discussion artifacts such as:

- personal advice to the repository owner;
- references to what was said earlier in a private conversation;
- speculation about whether wording will annoy, frighten, persuade, or discourage users, developers, or OEMs;
- confidential monetization rationale, negotiation tactics, unpublished pricing strategy, or other internal business reasoning;
- conversational authorial phrases such as `I recommend` / `we think` where the project can state a requirement, decision, policy, or rationale directly.

Operational documents may contain imperative engineering instructions when those instructions are addressed to their actual public audience, for example `Contributor MUST`, `Task MUST`, or `OEM Port SHOULD`.

Confidential strategy belongs outside tracked public content, such as an ignored local `private/` directory or a separate private repository.

Required repository-wide writing validation:

```text
python3 tools/check_public_writing.py
```

## 7. English/language-neutral implementation surfaces

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

## 8. Operational engineering plans

`docs/plans/` is an engineering work area, not a normative public protocol surface.

It is not required to duplicate every Task Design / AI Execution Prompt across maintained locales.

In particular:

```text
docs/plans/platform-ports/kindle/
```

may remain Chinese-first under its strict searchable bilingual filename convention.

This does not make `docs/plans/` private. Plans are publicly visible and MUST satisfy the repository-wide public writing rule.

A stable design fact that external implementers are expected to rely on MUST be promoted into localized Standards, Design, Reference Apps, Governance, or Status. It cannot remain authoritative only inside a maintainer-language task or prompt.

## 9. Synchronization rule for maintained pairs

For a Catalog Entry marked `current`, semantic changes SHOULD update all maintained locale editions in the same reviewed PR.

If synchronization cannot be completed immediately, the Catalog MUST explicitly mark the affected edition as pending/stale; Stable release processes cannot treat the pair as synchronized.

`superseded` is a valid state for historical compatibility entries that intentionally remain non-authoritative.

## 10. Root repository language model

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

Every current README locale MUST expose the same managed language-switch set.

## 11. Adding future locales

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

## 12. AI / contributor hard gate

Before creating, renaming, moving, translating, or editing tracked documentation, contributors and AI agents MUST apply the relevant structure rules and the repository-wide public writing rule.

Preferred localized-document scaffolder:

```text
python3 tools/new_localized_doc.py ...
```

Required validation for localized public docs:

```text
python3 tools/check_docs_i18n.py
```

Required validation for all tracked documentation:

```text
python3 tools/check_public_writing.py
```

CI rejects at least:

- recreation of legacy mixed-language public directories;
- invalid locale paths;
- invalid English/Chinese filenames;
- uncataloged localized public documents;
- duplicate Document IDs/target paths;
- non-null `legacy_path` after migration completion;
- missing counterparts for `current` / `superseded` localized documents;
- ad-hoc nested category structures;
- known private-discussion or internal-strategy writing patterns in tracked Markdown.

Agents MUST NOT weaken guards, broaden allowlists, or modify Catalog/validator rules merely to make invalid content pass.

## 13. Final rule

> **Localized project knowledge uses governed locale trees; protocol and implementation contracts remain one project; operational engineering plans may remain maintainer-language but are still public documents; machine surfaces remain shared and English/language-neutral; every tracked document is written for an external repository audience.**
