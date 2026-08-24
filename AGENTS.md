# Baga Ink Repository Instructions for AI Agents

This file is the first entry point for AI agents and automated contributors.

## 1. Source of truth

**`main` is the only long-term source of truth.** Feature branches, draft PRs, chat history, and old branch names are construction history, not authoritative project memory.

Long-lived localized documentation exists in:

```text
docs/en/
docs/zh-CN/
```

Legacy mixed-language public directories are forbidden.

## 2. Required reading order

Before architecture or implementation work, read:

```text
README.md or README.zh-CN.md
→ docs/en/00_baga-ink-documentation-index.md
  or docs/zh-CN/00_项目文档入口.md
→ current Project Status
→ relevant Standards
→ relevant Design / Reference App / Plan
```

Use `docs/localization/catalog.json` for stable localized Document Identity and locale counterpart mapping.

## 3. Documentation structure hard gate

Governance:

```text
docs/en/governance/00_baga-ink-development-governance.md
docs/en/governance/01_documentation-internationalization-policy.md
```

or the corresponding Simplified Chinese editions.

Localized public categories:

```text
standards/
design/
reference-apps/
governance/
status/
```

Hard rules:

- Localized public docs MUST live under `docs/en/<category>/` or `docs/zh-CN/<category>/`.
- `docs/standards/`, `docs/design/`, `docs/reference-apps/`, `docs/governance/`, `docs/status/`, and the old mixed-language root documentation index MUST NOT exist.
- Do not invent `english/`, `chinese/`, `cn/`, `zh/`, or per-document language subtrees.
- English localized public filenames: `NN_lowercase-kebab-case-name.md`.
- Simplified Chinese localized public filenames: `NN_中文名称.md`.
- Counterparts share one stable Document ID / number and MUST NOT become different protocols or architectures.
- A semantic change to a `current` localized document SHOULD update both maintained locales in the same reviewed PR.
- Machine-readable specs, code, tests, API identifiers, schema keys, error codes, CLI flags, comments/docstrings, test names, dependency manifests, and commit subjects remain English/language-neutral.
- `docs/plans/` is operational engineering material and is not required to duplicate every versioned Task Package by locale. Stable facts required by external implementers MUST be promoted into localized public docs.

Create new localized public docs with the scaffolder when available:

```text
python3 tools/new_localized_doc.py <category> <NN> <中文名称> <english-kebab-name> <document-id>
```

Mandatory validation for localized public docs:

```text
python3 tools/check_docs_i18n.py
```

Do not weaken validators or add exceptions merely to make invalid structure pass.

## 4. Repository-wide public writing hard gate

**Every documentation file tracked in this public repository is public-facing material.** This includes `docs/plans/`, Platform Port Task Packages, AI execution-entry documents, README files, contributor guides, licensing pages, and `AGENTS.md` itself.

There is no tracked “private notes” area inside this public repository.

All tracked documentation MUST:

- be written for its actual external audience;
- state project facts, requirements, decisions, plans, and rationale directly;
- remain understandable without access to private conversations;
- use institutional/project language rather than private advisory or chat-transcript language.

Tracked documentation MUST NOT contain:

- personal advice addressed to the repository owner;
- references to private conversation context such as “as we discussed”, “just mentioned”, or equivalent wording;
- private audience-management reasoning about whether wording will annoy, scare, persuade, or discourage users, developers, or OEMs;
- confidential monetization strategy, negotiation tactics, unpublished pricing logic, or private business priorities;
- private-consultation phrases such as `I recommend`, `we think`, or equivalent wording when the project requirement, policy, or rationale can be stated directly.

Normative instructions addressed to a documented public role are valid, for example:

```text
Contributor MUST run the validator.
OEM Port SHOULD publish reproducible Compatibility Evidence.
Task Package MUST define Acceptance Criteria.
```

`docs/plans/` may use direct engineering instructions, but it remains public and follows the same writing rule.

Confidential strategy MUST stay outside Git tracking, for example in the ignored local `private/` directory or a separate private repository.

Mandatory validation for all tracked Markdown documentation:

```text
python3 tools/check_public_writing.py
```

Do not weaken this guard to preserve conversational or private-strategy prose in the public repository.

## 5. Licensing / provenance hard gate

Before changing code, SDK output, examples, dependencies, packaging, distributable artifacts, LifeBook boundaries, or license/notice files, MUST read:

```text
docs/en/governance/02_baga-ink-licensing-policy.md
or
docs/zh-CN/governance/02_Baga-Ink授权策略.md
```

Canonical licensing/governance entry points:

```text
LICENSE
NOTICE
COMMERCIAL_LICENSE.md
LICENSE_HISTORY.md
THIRD_PARTY_NOTICES.md
```

Hard rules:

- The root `LICENSE` is the unmodified PolyForm Noncommercial License 1.0.0 for Baga-authored Platform/OEM-side software unless a file/directory explicitly states another license.
- Do not edit the PolyForm text and still call the result PolyForm.
- Ordinary IKP App development is separate from OEM/platform licensing. Do not add an OEM commercial-license requirement merely because an App uses documented Baga App APIs.
- App-facing SDK/examples such as future `baga-probe.ikp` MAY use an explicit permissive license; that exception must be stated locally.
- LifeBook production source is proprietary and MUST NOT be added to this public repository without an explicit owner decision and file-specific license.
- Third-party code always retains its upstream license. Never replace GPL/AGPL/other upstream notices with the Baga community or commercial license.
- A Baga Commercial License cannot waive third-party copyleft/source obligations.
- Historical Apache-2.0 rights already granted before the cutover remain historical rights; do not rewrite license history.
- External contributions to dual-licensed Baga Platform/Adapter code may require a legally reviewed CLA before merge. Do not accept code under terms that prevent intended distribution/relicensing of the target component.
- Trademark/certification claims such as `Baga Ink Compatible` are not granted merely by possessing source code.

Mandatory validation:

```text
python3 tools/check_licensing.py
```

Do not weaken licensing/provenance guards merely to merge a contribution or dependency.

## 6. Device Adapter / OEM port hard gate

Before device/OEM Adapter work, MUST read:

```text
docs/en/standards/07_baga-ink-device-adapter-specification.md
or docs/zh-CN/standards/07_设备适配器规范.md

relevant family Standard:
docs/en/standards/11_baga-ink-kindle-adapter.md
docs/en/standards/12_baga-ink-android-e-paper-adapter.md
or their zh-CN counterparts

for IDL / SDK / codegen / Mock / Contract Tests:
docs/en/design/02_baga-ink-device-adapter-executable-contract-and-sdk-design.md
or docs/zh-CN/design/02_设备适配器可执行契约与SDK设计.md
```

The Device Adapter Contract defines **what a port must provide**, not that Baga must reimplement existing OS/vendor/homebrew/open-source capabilities. Prefer mature existing mechanisms and keep concrete Adapters thin.

Do not add Reader/UI frameworks, KPM/MRPI/installation routes, Home Entry, or build tooling to the Device Adapter root contract merely because they are device-related.

## 7. Kindle implementation hard gate

Before work involving Kindle Platform, Client bootstrap/install routes, KPM/MRPI/KindleTool/KUAL/PEKI/sh_integration/AppMgr, KOReader/koreader-base integration, native build targets/ABI, or LifeBook Kindle execution/install/update/launch, MUST read:

```text
docs/en/reference-apps/03_baga-ink-kindle-implementation-architecture-freeze.md
or
docs/zh-CN/reference-apps/03_Kindle具体实现架构冻结.md
```

This Freeze is subordinate to Standards but authoritative over older Kindle Reference notes and prototypes.

Do not silently change a frozen decision in code. Update the governing decision/Freeze first, then implementation and tests.

Key frozen boundaries include:

- `.ikp` is never converted to `.kpkg`;
- KPM manages native Platform packages; IKP Package Manager manages Baga Apps;
- KPM missing != KPM incompatible;
- LifeBook does not import KOReader / Kindle private APIs;
- no formal `Baga Runtime`, `Baga Platform Runtime`, or `LifeBook Runtime` layer;
- Reader/UI, jailbreak routes, KPM/MRPI, Home Entry, and build tooling remain outside Device Adapter root contract;
- Kindle Adapter should maximize reuse of pinned KOReader/koreader-base/FBInk/Kindle OS mechanisms.

## 8. Platform-port Task Package hard gate

Before changing anything under:

```text
docs/plans/platform-ports/
```

read:

```text
docs/plans/platform-ports/0000_平台移植计划目录与文件命名规则_Baga-Ink-Platform-Port-Plan-Naming.md
```

For Kindle also read:

```text
docs/plans/platform-ports/kindle/0000_目录说明与文件命名规则_Kindle-Plan-Directory-and-File-Naming.md
docs/plans/platform-ports/kindle/0010_Kindle实现任务总计划_Baga-Ink-Kindle-Implementation-Master-Plan.md
```

Required physical workflow:

```text
Platform Master Plan
→ task/YYYY-MM-DD_<slug>/vN/vN.M/
→ flat numbered documents inside one self-contained task-package version
→ 00 control document is the entry point
```

Task-package version files use:

```text
NN_vN.M_<semantic-title>.md
```

The version directory MUST be flat. Do not create a mirrored `execution-prompts/` tree or per-Milestone `TASK-NNNN/vNNN` hierarchy. Detailed Batch write scopes, RED/GREEN tests, device evidence, implementation decisions, and the direct AI execution entry belong in the same task-package version directory.

Use the scaffolder when available:

```text
python3 tools/new_platform_port_task.py <platform> <YYYY-MM-DD> <slug> <vN> <vN.M>
```

Hard rules:

- Platform port root directories contain only root Plan Markdown plus `task/`.
- Task packages use `YYYY-MM-DD_<lowercase-kebab-slug>`.
- Versions use `vN/vN.M`, matching the version token in every file name.
- Every task-package version has a `00_vN.M_*` control document.
- Numeric file prefixes are unique inside a version.
- Task-package version directories contain files only; no ad-hoc subdirectories.
- Implementation evidence that changes an approved task decision MUST update the task package/version before the architectural change proceeds.
- Task Package prose MUST satisfy the repository-wide public writing rule.

Mandatory validation:

```text
python3 tools/check_platform_port_plans.py
python3 tools/check_public_writing.py
```

## 9. Branch / PR governance

Branches are short-lived construction scaffolding only.

Normal flow:

```text
main
→ short-lived branch
→ implementation + tests + docs
→ Pull Request
→ required CI
→ merge main
→ delete branch
```

Do not preserve unique architecture/status/compatibility knowledge only in a branch or PR discussion.

## 10. Project terminology

Use established terminology:

- Baga Ink Platform
- Baga Ink Platform Core
- Embedded Lua Interpreter
- Baga Lua Profile
- Baga Ink API
- Baga Ink Device Adapter Contract
- IKP / `.ikp`

Do not introduce `Baga Runtime`, `Baga Platform Runtime`, or `LifeBook Runtime` as formal layers.

LifeBook is the flagship/reference App, not the Platform.

## 11. Completion claims

Before claiming work complete:

- inspect current Project Status;
- run/inspect relevant tests/CI;
- do not mark a Draft Standard Stable because prose is complete;
- Device Adapter compilation/documentation alone is not Compatibility evidence;
- formal device compatibility requires relevant Adapter Contract Tests + BICTS evidence;
- localized public-doc structure changes require `tools/check_docs_i18n.py`;
- all tracked Markdown changes require `tools/check_public_writing.py`;
- licensing/provenance changes require `tools/check_licensing.py`;
- platform-port plan changes require `tools/check_platform_port_plans.py`.

## 12. Update Project Status

Meaningful milestones MUST update:

```text
docs/en/status/00_baga-ink-project-status.md
docs/zh-CN/status/00_当前项目状态.md
```

so a new human or AI can continue from `main` without reconstructing history from private conversations.
