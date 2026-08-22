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

Then read the specific standard/design/plan relevant to the task.

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
- Baga Ink Device Adapter
- IKP / `.ikp`

LifeBook is the flagship/reference App, not the platform itself.

## 5. Before Claiming Work Is Complete

Check the current status document and run/inspect the relevant tests or CI evidence.

Do not mark a Draft standard Stable merely because prose is complete. The executable-specification Stable Gate must be satisfied where applicable.

## 6. Updating Project State

When a meaningful milestone is completed, update:

`docs/status/00_当前项目状态_Baga-Ink-Project-Status.md`

so the next human or AI can understand the repository without reconstructing history from branches or conversations.
