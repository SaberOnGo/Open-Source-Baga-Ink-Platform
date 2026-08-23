# Baga Ink Repository Instructions for AI Agents

This file is the first entry point for AI agents and automated contributors working in this repository.

## 1. Single Source of Truth

**`main` is the only long-term source of truth for this project.**

Do not treat feature branches, draft pull requests, old chat context, or branch names as authoritative project state.

A branch may be used temporarily for CI or review, but it must never contain project knowledge that does not also land in `main`.

If a non-`main` branch exists and its content is already merged, treat it as disposable stale infrastructure.

## 2. Required Reading Order

Before making architecture or implementation decisions, read:

1. `docs/00_项目文档入口_Baga-Ink-Documentation-Index.md`
2. `docs/status/00_当前项目状态_Baga-Ink-Project-Status.md`
3. `docs/standards/00_规范总览_Baga-Ink-Standards-Index.md`
4. `docs/governance/00_开发治理_Baga-Ink-Development-Governance.md`

Then read the specific standard/design/plan/reference document relevant to the task.

### Device Adapter / OEM port hard gate

Before any work involving:

- a new device family or OEM port;
- Kindle / Android E-Paper Device Adapter implementation;
- display/input/storage/lifecycle/power/network device abstraction;
- Device Profile / Quirk design;
- Adapter Factory / Descriptor / Capability Snapshot;
- Adapter IDL / Codegen / SDK / Mock Adapter;
- Adapter Contract Tests or BICTS adapter integration;

MUST read and follow:

1. `docs/standards/07_设备适配器规范_Baga-Ink-Device-Adapter-Specification.md`
2. the relevant family standard such as `docs/standards/11_Kindle适配规范_Baga-Ink-Kindle-Adapter.md` or `12_Android墨水屏适配规范_Baga-Ink-Android-E-Paper-Adapter.md`
3. `docs/design/02_设备适配器可执行契约与SDK设计_Baga-Ink-Device-Adapter-Executable-Contract-and-SDK-Design.md` when implementing machine IDL/SDK/codegen/mock infrastructure.

The Device Adapter Contract defines **what a device port must provide**, not that Baga must reimplement existing OS/vendor/homebrew/open-source capabilities. Prefer mature existing implementations and keep device-family Adapters thin.

Do not add Reader/UI frameworks, KPM/MRPI/installation routes, or build tooling into the Device Adapter root contract merely because they are device-related.

### Kindle implementation hard gate

Before any work involving:

- Baga Ink Platform on Kindle;
- Baga Ink Client Kindle detection/bootstrap/install routes;
- KPM / MRPI / KindleTool / KUAL / PEKI / sh_integration / AppMgr decisions;
- KOReader / koreader-base integration or dependency selection;
- Kindle native build target / ABI decisions;
- LifeBook (`lifebook.ikp`) execution, install, update, launch or Kindle-specific integration;

MUST also read and follow:

`docs/reference-apps/03_Kindle具体实现架构冻结_Baga-Ink-Kindle-Implementation-Architecture-Freeze.md`

This Kindle Architecture Freeze is subordinate to `docs/standards/`, but authoritative over older Kindle reference/design notes and implementation prototypes.

Do not silently change a frozen Kindle decision in code. If evidence requires a change, update the architecture decision/freeze first, then code and tests.

### Platform-port Task / AI execution-prompt hard gate

Before creating, renaming, moving, or editing anything under:

```text
docs/plans/platform-ports/
```

MUST read and follow:

```text
docs/plans/platform-ports/0000_平台移植计划目录与文件命名规则_Baga-Ink-Platform-Port-Plan-Naming.md
```

For Kindle work, MUST also read:

```text
docs/plans/platform-ports/kindle/0000_目录说明与文件命名规则_Kindle-Plan-Directory-and-File-Naming.md
docs/plans/platform-ports/kindle/task/0000_任务设计目录说明_Task-Design-Directory-Guide.md
docs/plans/platform-ports/kindle/execution-prompts/0000_AI执行提示目录说明_AI-Execution-Prompt-Directory-Guide.md
```

The required physical workflow is:

```text
Platform Master Plan
      ↓
task/<NNNN_中文任务名_English-Task-Name>/vNNN/
      ↓
select exact Task Design version
      ↓
execution-prompts/<same Task directory>/<same vNNN>/
```

Hard rules:

- Do not invent another task, prompt, handoff, scratch, plan, notes, temp, date-based, milestone, or AI-output directory under a platform-port root.
- A platform-port root may contain plan Markdown files plus only `task/` and `execution-prompts/` unless the governing rule and validator are deliberately changed first.
- Task directories MUST use `NNNN_中文任务名_English-Task-Name`.
- Task Design versions MUST use zero-padded `vNNN` such as `v001`, `v002`, `v010`; `v1`, `v2`, `v10`, date folders, and ad-hoc version names are forbidden.
- Markdown files MUST use `数字前缀_中文名_English-Name.md`; files inside task/execution trees MUST use four-digit numeric prefixes.
- Every Task directory MUST have `0000_任务版本索引_Task-Version-Index.md` and at least one `vNNN` version.
- Every Task Design version MUST have `0000_任务设计总纲_Task-Design-Overview.md`.
- Every execution-prompt Task/version MUST exactly mirror an existing Task Design Task/version.
- Every execution-prompt version MUST have `0000_执行索引_Execution-Index.md`.
- An execution prompt may refine implementation steps, tests, debugging, validation, or real-device actions; it MUST NOT silently change the selected Task Design architecture/scope. If the design changes materially, create a new Task Design `vNNN` first.

Before claiming any change under `docs/plans/platform-ports/` is complete, MUST run:

```text
python3 tools/check_platform_port_plans.py
```

and require a zero exit code. The same validator runs in `.github/workflows/platform-port-plan-guard.yml`.

If an agent is operating through a tool that cannot execute repository commands, it MUST still conform to the same rules and MUST inspect the CI result before claiming the change is valid. Do not bypass, weaken, or add exceptions to the validator merely to make an invalid layout pass.

## 3. Branches Are Not Knowledge Storage

Feature branches are temporary construction scaffolding only.

They must not be used to preserve:

- architecture decisions;
- current project status;
- future work lists;
- compatibility knowledge;
- hidden implementation requirements;
- AI handoff context.

Those belong in numbered documents under `docs/` and in code/tests on `main`.

## 4. Project Terminology

Baga Ink intentionally uses a lightweight platform architecture.

Do not introduce a separate heavyweight execution-layer product concept. Use the established terminology from the standards, including:

- Baga Ink Platform
- Baga Ink Platform Core
- Embedded Lua Interpreter
- Baga Lua Profile
- Baga Ink API
- Baga Ink Device Adapter Contract
- IKP / `.ikp`

Do not introduce `Baga Runtime`, `Baga Platform Runtime`, or `LifeBook Runtime` as formal architecture layers.

LifeBook is the flagship/reference App, not the platform itself.

## 5. Before Claiming Work Is Complete

Check the current status document and run/inspect the relevant tests or CI evidence.

Do not mark a Draft standard Stable merely because prose is complete. The executable-specification Stable Gate must be satisfied where applicable.

For device ports, Adapter documentation or compilation alone is not enough: relevant Adapter Contract Tests and BICTS evidence are required before claiming compatibility.

For any change under `docs/plans/platform-ports/`, `python3 tools/check_platform_port_plans.py` and the Platform Port Plan Guard CI are mandatory completion gates.

## 6. Updating Project State

When a meaningful milestone is completed, update:

`docs/status/00_当前项目状态_Baga-Ink-Project-Status.md`

so the next human or AI can understand the repository without reconstructing history from branches or conversations.
