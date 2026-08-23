# Baga Ink Repository Instructions for AI Agents

This file is the first entry point for AI agents and automated contributors.

## 1. Source of truth

**`main` is the only long-term source of truth.** Feature branches, draft PRs, chat history, and old branch names are construction history, not authoritative project memory.

Public long-lived documentation exists only in the governed locale trees:

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

Use `docs/localization/catalog.json` for stable Document Identity and locale counterpart mapping.

## 3. Public documentation hard gate

Governance:

```text
docs/en/governance/01_documentation-internationalization-policy.md
docs/zh-CN/governance/01_文档国际化与本地化规范.md
```

Allowed localized public categories:

```text
standards/
design/
reference-apps/
governance/
status/
```

Hard rules:

- Public docs MUST live under `docs/en/<category>/` or `docs/zh-CN/<category>/`.
- `docs/standards/`, `docs/design/`, `docs/reference-apps/`, `docs/governance/`, `docs/status/`, and the old mixed-language root documentation index MUST NOT exist.
- Do not invent `english/`, `chinese/`, `cn/`, `zh/`, or per-document language subtrees.
- English public filenames: `NN_lowercase-kebab-case-name.md`.
- Simplified Chinese public filenames: `NN_中文名称.md`.
- Counterparts share one stable Document ID / number and MUST NOT become different protocols or architectures.
- A semantic change to a `current` document SHOULD update both maintained locales in the same reviewed PR.
- Machine-readable specs, code, tests, API identifiers, schema keys, error codes, CLI flags, comments/docstrings, test names, dependency manifests, and commit subjects remain English/language-neutral.
- `docs/plans/` is engineering material and is not required to duplicate every Task Design / Execution Prompt by locale. Stable facts required by external implementers MUST be promoted into localized public docs.

Create new localized public docs with the scaffolder when available:

```text
python3 tools/new_localized_doc.py <category> <NN> <中文名称> <english-kebab-name> <document-id>
```

Mandatory validation:

```text
python3 tools/check_docs_i18n.py
```

Do not weaken validators or add exceptions merely to make invalid structure pass.

## 4. Device Adapter / OEM port hard gate

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

## 5. Kindle implementation hard gate

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

## 6. Platform-port Task / AI execution-prompt hard gate

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
docs/plans/platform-ports/kindle/task/0000_任务设计目录说明_Task-Design-Directory-Guide.md
docs/plans/platform-ports/kindle/execution-prompts/0000_AI执行提示目录说明_AI-Execution-Prompt-Directory-Guide.md
```

Required physical workflow:

```text
Platform Master Plan
→ task/<NNNN_中文任务名_English-Task-Name>/vNNN/
→ select exact Task Design version
→ execution-prompts/<same Task>/<same vNNN>/
```

Use scaffolding tools when available:

```text
python3 tools/new_platform_port_task.py task ...
python3 tools/new_platform_port_task.py version ...
python3 tools/new_platform_port_task.py execution ...
python3 tools/new_platform_port_task.py prompt ...
```

Hard rules:

- Do not invent parallel task/prompt/handoff/scratch/temp/date/milestone directories under a platform-port root.
- Task directory: `NNNN_中文任务名_English-Task-Name`.
- Version: zero-padded `vNNN` only.
- Every Markdown file under `docs/plans/platform-ports/` uses `NNNN_中文名_English-Name.md`.
- Every Task has `0000_任务版本索引_Task-Version-Index.md` and at least one version.
- Every Task Design version has `0000_任务设计总纲_Task-Design-Overview.md`.
- Execution Prompt task/version exactly mirrors an existing Task Design task/version.
- Every execution version has `0000_执行索引_Execution-Index.md`.
- Execution prompts may refine steps/tests/debug/real-device actions but MUST NOT silently change selected Task Design architecture/scope.

Mandatory validation:

```text
python3 tools/check_platform_port_plans.py
```

## 7. Branch / PR governance

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

## 8. Project terminology

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

## 9. Completion claims

Before claiming work complete:

- inspect current Project Status;
- run/inspect relevant tests/CI;
- do not mark a Draft Standard Stable because prose is complete;
- device Adapter compilation/documentation alone is not Compatibility evidence;
- formal device compatibility requires relevant Adapter Contract Tests + BICTS evidence;
- public-doc changes require `tools/check_docs_i18n.py`;
- platform-port plan changes require `tools/check_platform_port_plans.py`.

## 10. Update Project Status

Meaningful milestones MUST update:

```text
docs/en/status/00_baga-ink-project-status.md
docs/zh-CN/status/00_当前项目状态.md
```

so a new human or AI can continue from `main` without reconstructing history from conversations.
