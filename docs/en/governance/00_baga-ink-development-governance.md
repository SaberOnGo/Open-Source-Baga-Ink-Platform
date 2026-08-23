# Baga Ink Development Governance

> **Document level:** Project governance  
> **Document ID:** `governance.00`  
> **Locale:** English (`en`)  
> **Status:** Governance Baseline v0.4  
> **Date:** 2026-08-23  
> **Counterpart:** `docs/zh-CN/governance/00_开发治理.md`

---

## 0. Purpose

This document defines how Baga Ink preserves long-lived project facts, organizes Standards / Design / Plans / Status / Reference Apps, manages branches and pull requests, and supports collaboration among independent contributors and AI agents.

Core principles:

> **`main` is the long-term source of truth.**

> **Every tracked document in this public repository is public-facing material.**

> **Public documentation is written for repository users, contributors, implementers, OEM engineers, reviewers, and other third parties—not as a transcript of private project discussions.**

---

## 1. Role of `main`

`main` MUST contain the durable project state that is intended to be public, including as applicable:

- approved Standards;
- Approved Design;
- Reference Apps / Architecture Freezes;
- current Project Status;
- Implementation Plans;
- machine-readable specifications, schemas, and test vectors;
- public/reference implementations;
- tests and CI;
- public Platform / SDK / tooling source intended for this repository;
- governance and contributor rules;
- licensing, third-party provenance, and release evidence.

Proprietary first-party products and confidential commercial material are not required to be stored in this public repository.

If a public technical conclusion exists only in a feature branch, draft PR discussion, issue comment, chat transcript, or private notes, it has not yet become durable public project knowledge.

---

## 2. Official public documentation layout

Long-lived localized prose is organized under:

```text
docs/en/
docs/zh-CN/
```

Localized public categories are:

```text
standards/
design/
reference-apps/
governance/
status/
```

English and Chinese editions sharing a Document Number / Document ID represent the same logical document and MUST NOT evolve into different protocols or architectures.

Localization rules are defined by:

```text
docs/en/governance/01_documentation-internationalization-policy.md
docs/localization/catalog.json
docs/localization/terminology.json
```

The former mixed-language public directories are retired and MUST NOT be recreated.

---

## 3. Public repository writing rule

The public/private boundary is determined by repository visibility and Git tracking, not by document category.

Therefore all tracked prose in this public repository—including:

```text
README files
CONTRIBUTING files
AGENTS.md
COMMERCIAL_LICENSE files
docs/en/
docs/zh-CN/
docs/plans/
Platform Port Task Designs
AI Execution Prompts
other tracked Markdown documentation
```

MUST be suitable for external publication.

Public repository prose MUST:

- address its actual public audience or state project policy in an institutional voice;
- distinguish normative requirements from informative rationale;
- describe architecture, implementation plans, compatibility, licensing, and project status directly;
- remain understandable without access to private conversations;
- avoid references to private discussions, author-specific advice, or private commercial strategy.

Public repository prose MUST NOT contain:

- conversational responses addressed to the repository owner;
- phrases whose meaning depends on a prior chat or private decision discussion;
- private audience-management reasoning such as speculation about whether wording will annoy, scare, persuade, or discourage users or vendors;
- confidential monetization strategy, negotiation tactics, internal pricing logic, or unpublished business priorities;
- personal advisory language such as `I recommend`, `we think`, or equivalent private-discussion phrasing when a project requirement or rationale can be stated directly.

Normative instructions addressed to the intended public role remain valid. For example:

```text
Contributors MUST run the validator.
OEM ports SHOULD publish reproducible Compatibility Evidence.
A Task Design MUST define acceptance criteria.
```

`docs/plans/` may use direct operational engineering language, but it remains public documentation and follows the same publication standard.

Confidential material belongs outside the tracked public repository, for example in an ignored local `private/` directory or a separate private repository.

Repository validation:

```text
python3 tools/check_public_writing.py
```

---

## 4. Document classes

Different document classes answer different questions:

```text
What Baga Ink MUST be
→ docs/<locale>/standards/

How a subsystem is designed and why
→ docs/<locale>/design/

How a Reference App / Reference Platform validates the standards
→ docs/<locale>/reference-apps/

Where the project stands now
→ docs/<locale>/status/

How contributors work and how the project is governed
→ docs/<locale>/governance/

How an approved design is implemented and verified
→ docs/plans/
```

`docs/plans/` is public operational engineering material. It is not required to duplicate every Task Design / AI Execution Prompt across human languages, but its technical conclusions are not a substitute for localized public Standards or Design when external implementers depend on those conclusions.

A stable external contract MUST be represented in the appropriate Standards / Design / Reference Apps / Governance / Status documents rather than remaining authoritative only in a platform-port task.

---

## 5. Branch and PR lifecycle

Feature branches MAY be used for short-term development isolation, TDD intermediate states, PR review, CI validation, and temporary refactoring work.

Feature branches MUST NOT be used as long-term storage for architecture decisions, current status, roadmaps, compatibility matrices, hidden requirements, or context available only to one contributor or AI agent.

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

`main` is protected by a GitHub Ruleset. Repository changes follow the configured PR and CI requirements.

---

## 6. Responsibility of a PR

A PR provides review, diff inspection, CI, discussion, and auditable construction history.

A PR is not the project current-state database.

After merge, current public facts MUST be represented by the appropriate combination of:

```text
code
tests
machine-readable specs
Standards / Design / Reference Apps
Status / Plans
```

Future maintainers should be able to reconstruct the current public architecture without reading historical PR conversations.

---

## 7. Status management

English status entry point:

```text
docs/en/status/00_baga-ink-project-status.md
```

Simplified Chinese counterpart:

```text
docs/zh-CN/status/00_当前项目状态.md
```

Meaningful milestone changes MUST update Status.

Status should record, as applicable:

- Completed;
- In Progress;
- Next;
- Known Gaps;
- Draft / Stable boundaries;
- Verification Evidence;
- current Compatibility Claim boundaries.

---

## 8. AI / automation rules

An AI agent working in this repository MUST:

1. use `main` as the baseline;
2. read root `AGENTS.md` first;
3. select the English or Chinese Documentation Index;
4. use `docs/localization/catalog.json` for public Document Identity and counterpart mapping;
5. read the Standards / Design / Reference App / Plan relevant to the task;
6. not infer current architecture from historical branches or private conversation context;
7. pass applicable repository validators and CI;
8. update Status / Evidence after meaningful work;
9. apply the repository-wide public writing rule to every tracked documentation file it creates or modifies.

AI agents MUST NOT weaken validators, widen allowlists, rename required checks, or bypass governance to make invalid work pass.

---

## 9. High-volume Platform Port engineering material

`docs/plans/platform-ports/` uses a high-scale Task Design / Execution Prompt model because one device family may require many implementation and validation tasks.

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

The Kindle port also has platform-specific Task / Execution Prompt guides.

These plans are public operational engineering context. They do not become private merely because they are implementation-oriented.

---

## 10. Draft → Stable

A Standard MUST NOT become Stable solely because its prose is complete.

For executable protocols, a Stable Gate SHOULD/MUST, as defined by the governing Standard, include evidence such as:

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

## 11. Device Adapter / OEM port governance boundary

The Device Adapter Contract defines what a device port must provide in order to participate in Baga Ink.

It does not require reimplementation of capabilities already provided by the OS, vendor SDK, homebrew ecosystem, or mature open-source components.

A concrete device port SHOULD remain as thin as practical and concentrate device-family differences such as:

```text
model / firmware differences
capability detection
Device Profile
Quirk Set
error / event normalization
```

Reader/UI frameworks, installation routes, KPM/MRPI, and build tooling are not part of the Device Adapter root contract solely because they are device-related.

---

## 12. License and third-party provenance

Current licensing policy:

```text
LICENSE
docs/en/governance/02_baga-ink-licensing-policy.md
COMMERCIAL_LICENSE.md
LICENSE_HISTORY.md
THIRD_PARTY_NOTICES.md
```

Baga-authored Platform/OEM-side software follows the applicable current project license or an explicit file/directory override. Historical Apache-2.0 grants remain governed by `LICENSE_HISTORY.md`.

Third-party code and components retain their upstream licenses. A Baga community or commercial license does not relicense KOReader, FBInk, KPM, or other upstream projects.

Distributable products MUST record applicable dependency versions, provenance, licenses, and local modifications. GPL / AGPL and other redistribution obligations are release-gating requirements.

---

## 13. Commits, tags, and releases

Commit subjects SHOULD be English and describe the actual change, for example:

```text
docs: update device adapter standard
spec: add publisher identity schemas
feat: add IKP signature verifier
test: add invalid IKP corpus
```

Tags / releases identify formal baselines, for example:

```text
standards-v0.1
ikp-v1.0
platform-v0.1
sdk-v0.1
```

Historical states should be recoverable from commits, tags, and releases rather than permanent feature branches.

---

## 14. Completion checklist

Before considering a meaningful task complete, verify as applicable:

```text
[ ] implementation is included in the reviewed change
[ ] relevant tests / CI pass
[ ] architecture changes are reflected in the governing Standard / Design
[ ] external dependency facts are reflected in public documentation
[ ] current state is reflected in Status
[ ] required Compatibility / Device Evidence is recorded
[ ] the branch contains no unique long-term public knowledge absent from main
[ ] license / third-party provenance remains valid
[ ] tracked documentation satisfies the public writing rule
```

---

## 15. Final principle

> **Code + Machine Specs + Tests + approved public documentation on `main` define the public Baga Ink project state. Every tracked document is written for an external repository audience; confidential or private-strategy material remains outside the public repository.**
