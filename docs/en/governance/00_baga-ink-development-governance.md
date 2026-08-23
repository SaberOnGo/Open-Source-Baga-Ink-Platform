# Baga Ink Development Governance

> **Document level:** Project governance  
> **Document ID:** `governance.00`  
> **Locale:** English (`en`)  
> **Status:** Governance Baseline v0.3  
> **Date:** 2026-08-23  
> **Counterpart:** `docs/zh-CN/governance/00_开发治理.md`

---

## 0. Purpose

This document defines how Baga Ink preserves long-term project facts, organizes Standards / Design / Plans / Status / Reference Apps, uses branches and pull requests, and enables humans and AI agents to continue the project without relying on historical chat context.

The most important rule is:

> **`main` is the long-term source of truth; short-lived branches are construction scaffolding, not project memory.**

Baga Ink is also an international project:

> **Public long-lived documentation is localized by locale, while the protocol, APIs, schemas, code, and tests remain one shared implementation contract.**

---

## 1. Role of `main`

`main` MUST contain all long-lived project material, including:

- approved Standards;
- Approved Design;
- Reference Apps / Architecture Freezes;
- current Project Status;
- Implementation Plans;
- machine-readable specifications, schemas, and test vectors;
- reference / independent implementations;
- tests and CI;
- production/reference Platform, SDK, Client, and Market source code;
- governance and contributor rules;
- licensing, third-party provenance, and release evidence.

If an important conclusion exists only in:

```text
chat history
feature branch
draft PR description
issue comment
personal notes
an AI's temporary context
```

then it has not yet become durable project knowledge.

---

## 2. Official public documentation layout

Public, long-lived prose that external developers may rely on is organized by locale:

```text
docs/en/
docs/zh-CN/
```

Public categories are:

```text
standards/
design/
reference-apps/
governance/
status/
```

English and Chinese editions that share a Document Number / Document ID are editions of the same logical document. They MUST NOT evolve into different protocols or architectures.

Localization rules are defined by:

```text
docs/en/governance/01_documentation-internationalization-policy.md
docs/localization/catalog.json
docs/localization/terminology.json
```

Historical mixed-language directories are currently a migration zone only. New public documents must not be added there.

---

## 3. Different document classes answer different questions

```text
What Baga Ink MUST be
→ docs/<locale>/standards/

How a subsystem is designed and why
→ docs/<locale>/design/

How a Reference App / Reference Platform validates the standards
→ docs/<locale>/reference-apps/

Where the project actually stands now
→ docs/<locale>/status/

How contributors work and how the project is governed
→ docs/<locale>/governance/

How an approved design is implemented next
→ docs/plans/
```

`docs/plans/` is an engineering work area and is not required to translate thousands of Task Design / AI Execution Prompt documents across languages.

However:

> **Any stable fact that external implementers are expected to rely on must be promoted back into Public Localized Docs. It cannot remain authoritative only inside a Chinese task or prompt.**

---

## 4. Branch and PR lifecycle

Feature branches MAY be used for:

- short-term development isolation;
- intentionally RED TDD states;
- PR review;
- CI validation;
- temporary protection around risky refactors.

Feature branches MUST NOT be used as long-term storage for:

- architecture decisions;
- current status;
- roadmaps;
- compatibility matrices;
- hidden requirements;
- context known only to one AI agent.

Normal lifecycle:

```text
main
  ↓
short-lived branch
  ↓
implementation + tests + docs
  ↓
Pull Request
  ↓
Required CI Checks
  ↓
merge main
  ↓
delete branch
```

`main` is protected by a GitHub Ruleset. Administrator convenience is not a reason to bypass the normal PR/CI path.

---

## 5. Responsibility of a PR

A PR is for:

- review;
- diff inspection;
- CI;
- discussion;
- auditable construction history.

A PR is not the project's current-state database.

After merge, current facts must already be represented by:

```text
code
tests
machine-readable specs
Standards / Design / Reference Apps
Status / Plans
```

Future maintainers should not need to read historical PR discussions to reconstruct the current architecture.

---

## 6. Status must be maintained centrally

English status entry point:

```text
docs/en/status/00_baga-ink-project-status.md
```

Simplified Chinese counterpart:

```text
docs/zh-CN/status/00_当前项目状态.md
```

Meaningful milestone changes MUST update Status.

Status should record at least:

- Completed;
- In Progress;
- Next;
- Known Gaps;
- Draft / Stable boundaries;
- Verification Evidence;
- current Compatibility Claim boundaries.

The answer to "where are we now?" must not require inference from commits, branches, or chat history.

---

## 7. AI / automation rules

A new AI agent MUST:

1. use `main` as the baseline;
2. read root `AGENTS.md` first;
3. choose the English or Chinese Documentation Index;
4. use `docs/localization/catalog.json` to resolve the current public-document path;
5. read the Standards / Design / Reference App / Plan relevant to the task;
6. not scan historical branches to guess the active architecture;
7. not assume a file or branch is authoritative merely because it appears newer;
8. pass repository guards / CI for structural changes;
9. update Status / Evidence after meaningful work.

AI agents MUST NOT weaken validators, widen allowlists, rename required checks, or bypass governance simply to make their own invalid layout pass.

---

## 8. High-volume Platform Port engineering material

`docs/plans/platform-ports/` uses a separate high-scale task model because a single device platform may eventually have hundreds of tasks and thousands of AI execution prompts.

Core structure:

```text
platform-port/
├── task/
└── execution-prompts/
```

Rules are defined by:

```text
docs/plans/platform-ports/0000_平台移植计划目录与文件命名规则_Baga-Ink-Platform-Port-Plan-Naming.md
```

The Kindle port also has its own Task / Execution Prompt guides.

These engineering plans are operational context, not public protocol authority.

---

## 9. Draft → Stable

A Standard MUST NOT become Stable merely because its Markdown looks complete.

For executable protocols, a Stable Gate SHOULD/MUST (as defined by the governing Standard) include evidence such as:

```text
Schema Validation
Canonical Test Vectors
Negative Corpus
Reference Implementation
Independent Implementation / Verifier
Cross-language Compatibility
End-to-end Tests
Device / Platform Evidence
CI / Conformance
```

Device Compatibility additionally requires the relevant Adapter Contract Tests / BICTS evidence.

---

## 10. Device Adapter / OEM port governance boundary

The Device Adapter Contract defines:

> **What a device must provide in order to join Baga Ink.**

It does not require Baga to reimplement capabilities already provided by the OS, vendor SDK, homebrew ecosystem, or mature open-source components.

A concrete device port SHOULD remain as thin as practical and concentrate:

```text
model / firmware differences
capability detection
Device Profile
Quirk Set
error / event normalization
```

Reader/UI frameworks, installation routes, KPM/MRPI, and build tooling must not be pushed into the Device Adapter root contract merely because they are device-related.

---

## 11. License and third-party provenance

Baga-authored material defaults to Apache License 2.0 unless a file/directory states otherwise.

Third-party code and components retain their upstream licenses. The Baga repository license does not relicense projects such as KOReader, FBInk, or KPM.

Distributable products must record the actual dependency version, provenance, digest, license, and local patch set.

Repository entry points:

```text
LICENSE
NOTICE
THIRD_PARTY_NOTICES.md
```

When GPL / AGPL or other additional redistribution obligations are involved, licensing compliance is a release gate — not documentation to add after shipping.

---

## 12. Commits, tags, and releases

Commits preserve traceable history. Commit subjects SHOULD be English and describe the actual change, for example:

```text
docs: migrate device adapter standard
spec: add publisher identity schemas
feat: add IKP signature verifier
test: add invalid IKP corpus
```

Tags / releases mark formal baselines, for example:

```text
standards-v0.1
ikp-v1.0
platform-v0.1
sdk-v0.1
```

Historical states should be recoverable from commits, tags, and releases rather than permanent feature branches.

---

## 13. Completion checklist for meaningful work

Before considering a meaningful task complete, verify as applicable:

```text
[ ] valid code is in the PR
[ ] relevant tests / CI pass
[ ] architecture changes are reflected in the governing Standard / Design
[ ] external dependency facts are reflected in Public Docs
[ ] current state is reflected in Status
[ ] required Compatibility / Device Evidence is recorded
[ ] the branch contains no unique long-term knowledge not destined for main
[ ] license / third-party provenance has not been broken
```

---

## 14. Final principle

Baga Ink is intended to be maintained over the long term by different countries, organizations, device vendors, and AI tools.

The repository therefore optimizes for:

> **Read the repository, not someone's memory.**

More precisely:

> **Read Code + Machine Specs + Tests + Approved Public Docs on `main`, not a forest of branches and historical chat logs.**
