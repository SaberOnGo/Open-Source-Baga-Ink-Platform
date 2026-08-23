# Baga Ink Project Status

> **Document level:** Canonical Project Status  
> **Document ID:** `status.00`  
> **Locale:** English (`en`)  
> **Status:** Living Status v0.3  
> **Date:** 2026-08-23  
> **Counterpart:** `docs/zh-CN/status/00_当前项目状态.md`  
> **Authoritative branch:** `main`

---

## 0. What this document answers

This document answers one question:

> **Where does Baga Ink actually stand today?**

Feature branches, chat history, PR titles, old tasks, and future roadmaps do not override the actual code, tests, machine-readable specifications, and approved public documentation on `main`.

If this document conflicts with the implementation on `main`, verify the code / tests / conformance evidence first and fix the status document immediately.

---

## 1. One-page status

Overall phase:

> **Baga Ink has moved beyond concept discussion into the Standards + Executable Conformance + Reference Platform Implementation preparation stage. The protocol family, Device Adapter Contract, Kindle reference architecture, and distribution-security machine-spec foundation exist, but there is not yet a production-ready Baga Platform / Kindle port / Market / Client for end users.**

What already exists at a meaningful baseline:

```text
substantial Draft / Baseline Standards system
distribution / signing / repository machine-readable specification foundation
Python reference implementation + tests
Device Adapter Contract
Kindle / Android E-Paper Adapter Standards
Kindle Implementation Architecture Freeze
Device Adapter Executable Contract / SDK Design
Kindle Implementation Master Plan + Task/Execution Prompt governance
public documentation internationalization architecture
repository Ruleset + documentation guards
Apache-2.0 project licensing baseline
```

What the project **cannot** currently claim:

```text
Baga Ink Platform product implementation complete
Kindle Reference Adapter complete
any Kindle formally Baga Ink Compatible
Android E-Paper Reference Adapter complete
Baga Ink Client complete
Baga Ink Market complete
LifeBook proven through the full cross-device Baga loop
Standards Stable release
```

---

## 2. Standards status

The current Draft / Baseline standards cover:

### Platform Core 00–09

```text
00  Standards Index
01  Platform Strategy / Architecture
02  App Standard
03  API Specification
04  Capability Registry
05  Permission Model
06  IKP Package Specification
07  Device Adapter Contract
08  Compatibility Standard
09  UI Specification
```

### Compatibility / Device Adapter / Standard Libraries 10–13

```text
10  BICTS / Compatibility Test Suite
11  Kindle Device Adapter
12  Android E-Paper Adapter
13  Standard Libraries / Adopted Components
```

### Market / Distribution / Signing 20–28

```text
20  Market / Distribution Architecture
21  Publisher Identity / App Ownership
22  IKP Signing / Key Lifecycle
23  Repository Metadata / Index Protocol
24  Publishing / Review / Version Policy
25  Update / Rollback / Revocation
26  Distribution Client / Offline Transfer
27  Transparency / Security Audit
28  Catalog / App Discovery
```

The existence of these documents does not mean they are production-Stable.

Public documentation is currently being migrated from the historical mixed-language layout into:

```text
docs/en/
docs/zh-CN/
```

Migration state is tracked by `docs/localization/catalog.json`.

---

## 3. Completed: executable-specification foundation

The current `main` branch includes:

```text
spec/
reference/python/
tests/
.github/workflows/conformance.yml
```

Important implemented foundations include:

### Strict JSON / canonicalization

- strict UTF-8 parsing;
- duplicate object key rejection;
- NaN / Infinity rejection;
- input size / nesting depth limits;
- RFC 8785 JCS canonicalization;
- SHA-256 helpers.

### Schema / identity / signing

- JSON Schema Draft 2020-12 foundation;
- Schema Registry / Loader;
- Ed25519;
- Publisher ID / Genesis;
- App Ownership;
- App Signing Key Delegation;
- Delegation Channel / Sequence / Expiry;
- IKP `files.json` / Payload Hash / Release Statement / Signature Set.

### IKP Validator foundation

- ZIP safety checks;
- duplicate ZIP entry rejection;
- path traversal rejection;
- compression / size limits;
- Universal IKP native executable rejection;
- Publisher → Ownership → Delegation → Release offline validation chain;
- Manifest / Release cross-consistency checks.

### Tests / negative corpus

Python conformance tests and invalid fixtures are integrated into CI.

However:

> **Passing this stage does not mean Standards 21–28 have passed their Stable Gate.**

---

## 4. Distribution conformance is still in progress

Major remaining work includes:

```text
Reference Repository / Client behavior completion
python-tuf / TUF conformance deepening
Independent Rust Verifier
Python ↔ Rust cross-language vectors
Repository → Client → Device E2E
Offline Transfer prototype
Update / Rollback / Revocation E2E
Stable Gate
```

The target is not "complete-looking Markdown". Distribution security should ultimately be constrained by:

```text
Spec
+ Machine Schema
+ Canonical Vector
+ Reference Implementation
+ Independent Implementation
+ Negative Tests
+ E2E / Conformance
```

---

## 5. Device Adapter Contract status

The `07 Device Adapter Contract` already defines:

```text
AdapterFactory / probe / create
Root Adapter lifecycle
DeviceDescriptor
Capability Snapshot vs Runtime State
AdapterHost / typed event model
stable error model
Display / Input / Storage / Lifecycle / Power
Optional Network / Light / Audio / Bluetooth / UserLibrary
Native Build Target vs Device Profile vs Quirk Set
Self-test
Contract versioning
Adapter Contract Tests vs BICTS
Mock / Headless Adapter requirement
OEM / third-party porting flow
```

The key engineering principle is frozen:

> **The standard defines what a device must provide; a concrete Adapter should stand on proven OS / Vendor SDK / Homebrew / mature open-source mechanisms instead of reimplementing the device.**

Machine IDL / generated SDK / Mock Adapter / reusable Contract Test Harness are not yet complete.

---

## 6. Kindle Reference Platform status

Kindle is the first Reference Platform Port.

The architecture boundary is defined roughly as:

```text
Baga Ink Client
→ jailbreak/bootstrap route when needed
→ Homebrew-ready
→ KPM where compatible, MRPI/legacy envelope where necessary
→ Baga Ink Platform
→ IKP Package Manager
→ lifebook.ikp / other Baga Apps
→ Kindle Home Entry
```

Important frozen decisions include:

- `.ikp` is not converted into `.kpkg`;
- KPM manages the native Baga Platform while the IKP Package Manager manages Baga Apps;
- KPM not installed ≠ KPM incompatible;
- KOReader / koreader-base / FBInk are internal adopted components, not LifeBook APIs;
- LifeBook does not directly depend on Kindle / KOReader private APIs;
- the Kindle Device Adapter maximizes reuse of mature mechanisms;
- `kindlehf` is the first real bring-up path;
- a Probe IKP should validate the Platform before the full LifeBook product is attempted.

The engineering plan lives under:

```text
docs/plans/platform-ports/kindle/
```

with governed Task Design / Version / Execution Prompt / CI rules.

### Not yet complete

```text
platform/adapters/kindle/
KindleAdapterFactory
real Device Profiles / Quirk Sets
Display/Input/Storage/Lifecycle/Power bindings
pinned KOReader/FBInk product integration
real-device Adapter Contract Tests
Base BICTS
real baga-probe.ikp on Kindle
```

Therefore:

> **Architecture readiness ≠ Kindle product implementation completion.**

---

## 7. Android E-Paper status

Android E-Paper already has a Device Family Adapter Standard direction:

```text
Generic Android Base Adapter
+
Vendor Specialization
```

Vendor specialization should cover only real differences such as:

```text
E-Paper Refresh Mode
Pen
Frontlight
Vendor SDK / Private API bridge
```

A complete Reference Implementation / Device BICTS phase has not yet been reached.

---

## 8. Documentation / collaboration infrastructure status

Completed:

```text
README.md                  English default project homepage
README.zh-CN.md            Simplified Chinese homepage
CONTRIBUTING.md / zh-CN
AGENTS.md

docs/en/
docs/zh-CN/
docs/localization/catalog.json
docs/localization/terminology.json
docs/localization/legacy-lock.json

tools/check_docs_i18n.py
tools/check_readme_languages.py
tools/check_platform_port_plans.py
```

`main` is protected by a branch Ruleset requiring the PR / CI flow, an up-to-date branch, force-push protection, and deletion protection.

The required documentation guard job is:

```text
Validate task/prompt layout
```

Public documentation internationalization is currently:

> **M0 complete, M1 started.**

This document and `governance.00` are the first formal M1-A migrated documents.

---

## 9. License status

Baga-authored material currently defaults to:

> **Apache License 2.0**

Repository entry points:

```text
LICENSE
NOTICE
THIRD_PARTY_NOTICES.md
```

Third-party projects retain their upstream licenses.

The Kindle architecture uses or plans to reuse projects with AGPL/GPL licensing, including KOReader / koreader-base / FBInk / KPM-related components. Future concrete Baga Platform releases therefore require release-specific dependency/license manifests and compliance review based on what is actually shipped.

---

## 10. No formal Compatibility Claim exists yet

The project must not currently claim:

```text
All Kindle Compatible
Kindle PW5 Compatible
Android E-Paper Compatible
BOOX Compatible
```

A formal Compatibility Record must bind at least:

```text
Device Model
Firmware / OS tested range
Native Build Target
Device Profile
Quirk Set
Baga Platform Version
Adapter Version
Adapter Contract Version
Lua Profile Version
Adopted Component commits/digests
Adapter Contract Test result
BICTS result
```

Evidence-based states are:

```text
Compatible
Experimental
Unsupported
```

---

## 11. Current priorities

### Track A — Distribution Conformance

Continue:

```text
Repository / Client reference behavior
Independent verifier
Cross-language vectors
E2E / offline transfer / rollback
Stable Gate
```

### Track B — Public Documentation Migration

Follow the migration plan:

```text
M1-A  Governance + Status + Index
M1-B  Standards 00–13
M1-C  Standards 20–28
M1-D  Design
M1-E  Reference Apps
M2    English review / synchronization
M4    remove legacy public trees
```

### Track C — Device Adapter / Kindle

Next implementation sequence:

```text
spec/adapter IDL
→ generated interface
→ Mock Adapter
→ Adapter Contract Test harness
→ kindlehf substrate bring-up
→ Kindle Base Adapter
→ baga-probe.ikp
→ Base BICTS
```

Do not begin with the full LifeBook product or automated jailbreak Client path.

---

## 12. Current project entry points

English:

```text
README.md
docs/en/00_baga-ink-documentation-index.md
docs/en/status/00_baga-ink-project-status.md
docs/en/governance/00_baga-ink-development-governance.md
```

Simplified Chinese:

```text
README.zh-CN.md
docs/zh-CN/00_项目文档入口.md
docs/zh-CN/status/00_当前项目状态.md
docs/zh-CN/governance/00_开发治理.md
```

Standards / Design / Reference Apps still in migration are resolved through:

```text
docs/localization/catalog.json
```

---

## 13. Final status rule

> **A document existing does not mean the implementation is complete; code compiling does not mean a device is Compatible; one successful device launch does not mean Stable.**

Baga Ink status must ultimately be supported by:

```text
Code
+ Machine-readable Spec
+ Tests
+ Device Evidence
+ Conformance
+ Approved Public Docs
```
