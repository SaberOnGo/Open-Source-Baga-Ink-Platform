# Baga Ink Project Status

> **Document level:** Canonical Project Status  
> **Document ID:** `status.00`  
> **Locale:** English (`en`)  
> **Status:** Living Status v0.4  
> **Date:** 2026-08-23  
> **Counterpart:** `docs/zh-CN/status/00_当前项目状态.md`  
> **Authoritative branch:** `main`

---

## 0. What this document answers

This document answers one question:

> **Where does Baga Ink actually stand today?**

Feature branches, chat history, PR titles, old tasks, and future roadmaps do not override the actual code, tests, machine-readable specifications, and approved public documentation on `main`.

---

## 1. One-page status

Overall phase:

> **Baga Ink has moved beyond concept discussion into Standards + Executable Conformance + Reference Platform implementation preparation. The public platform contract is now substantial and internationally readable through Standards 00–13, but production Baga Platform / Kindle / Android E-Paper / Client / Market implementations are not complete.**

Meaningful baselines already present:

```text
Draft / Baseline Standards 00–28
maintained English + Simplified Chinese Standards 00–13
machine-readable distribution/signing/repository specification foundation
Python reference implementation + conformance tests
Baga Device Adapter Contract
Kindle / Android E-Paper Device Adapter Standards
Kindle Implementation Architecture Freeze
Device Adapter Executable Contract / SDK Design
Kindle Implementation Master Plan + governed Task/Execution Prompt model
English-default project homepage + scalable locale switch
Apache-2.0 project licensing baseline + third-party license boundary
protected main + required documentation/conformance CI
```

The project **cannot** currently claim:

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

### Standards 00–13

The following have maintained English and Simplified Chinese editions and are `current` in `docs/localization/catalog.json`:

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
10  BICTS / Compatibility Test Suite
11  Kindle Device Adapter
12  Android E-Paper Device Adapter
13  Standard Libraries / Adopted Components
```

English:

```text
docs/en/standards/
```

Simplified Chinese:

```text
docs/zh-CN/standards/
```

### Standards 20–28

These exist as Draft/Baseline legacy documents and are the next public-document localization batch:

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

They are not Stable merely because machine-readable implementation work has begun.

---

## 3. Executable-specification foundation

The repository contains:

```text
spec/
reference/python/
tests/
.github/workflows/conformance.yml
```

Implemented foundations include:

- strict UTF-8 JSON parsing;
- duplicate-key / NaN / Infinity rejection;
- size / nesting limits;
- RFC 8785 JCS canonicalization;
- SHA-256 and Ed25519 helpers;
- JSON Schema Draft 2020-12 registry/loader;
- Publisher Identity / Genesis;
- App Ownership;
- App Signing Key Delegation;
- IKP `files.json`, payload hashing, Release Statement, Signature Set;
- ZIP safety, duplicate-entry rejection, path traversal protection, resource limits;
- Publisher → Ownership → Delegation → Release offline validation;
- invalid fixtures / negative corpus in CI.

Still required before distribution Standards can be called Stable:

```text
Reference Repository / Client completion
TUF conformance deepening
Independent Rust verifier
Python ↔ Rust vectors
Repository → Client → Device E2E
Offline Transfer prototype
Update / Rollback / Revocation E2E
Stable Gate evidence
```

---

## 4. Device Adapter Contract status

Standard 07 now has maintained English and Chinese editions and defines:

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

Frozen engineering principle:

> **The Contract defines what a device must provide; a concrete Adapter should reuse proven OS, Vendor SDK, Homebrew, and mature open-source mechanisms rather than reimplement the device.**

Not yet complete:

```text
spec/adapter machine IDL
code generation
generated SDK interfaces
Mock / Headless Adapter
reusable Adapter Contract Test Harness
```

---

## 5. Kindle Reference Platform status

Kindle is the first Reference Platform Port.

Frozen architecture direction:

```text
Baga Ink Client
→ jailbreak/bootstrap route when needed
→ Homebrew-ready device
→ KPM where compatible; MRPI/legacy envelope where required
→ Baga Ink Platform
→ IKP Package Manager
→ lifebook.ikp / other Baga Apps
→ Kindle Home Entry
```

Important decisions:

- `.ikp` is not converted to `.kpkg`;
- KPM manages the native Baga Platform; IKP Package Manager manages Baga Apps;
- KPM missing and KPM incompatible are different states;
- KOReader / koreader-base / FBInk are internal adopted mechanisms, not LifeBook APIs;
- LifeBook does not directly depend on Kindle or KOReader private APIs;
- the Kindle Device Adapter maximizes mature capability reuse;
- `kindlehf` is the first representative real-device bring-up path;
- a Probe IKP should validate the Platform before full LifeBook product work.

Engineering plan:

```text
docs/plans/platform-ports/kindle/
```

Not yet implemented:

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

Architecture readiness is not product completion.

---

## 6. Android E-Paper status

The Android E-Paper Standard defines:

```text
Generic Android Base Adapter
+
Vendor Specialization
```

Vendor specialization should absorb only true differences such as refresh modes, pen, front light, and vendor APIs.

A complete Android Reference Adapter / BICTS implementation is not yet present.

---

## 7. Public documentation internationalization

Completed:

```text
M0    locale architecture / governance / guards / README / licensing
M1-A  Governance + Status + Documentation Index
M1-B1 Standards 00–06
M1-B2 Standards 07–13
```

Next:

```text
M1-C  Standards 20–28
M1-D  Design
M1-E  Reference Apps
M4    remove legacy public trees and forbid them in CI
```

The historical mixed-language trees remain hash-locked migration inputs until all important references have moved.

---

## 8. Repository governance and licensing

`main` is protected by a GitHub Ruleset requiring the normal PR / CI path. The required documentation job remains:

```text
Validate task/prompt layout
```

That job now covers public-doc i18n validation, README locale-switch validation, and Platform Port task/prompt layout validation.

Baga-authored material defaults to:

> **Apache License 2.0**

Repository license entry points:

```text
LICENSE
NOTICE
THIRD_PARTY_NOTICES.md
```

Third-party projects retain their upstream licenses. Concrete releases that bundle or derive from AGPL/GPL components such as KOReader / koreader-base / FBInk / KPM-related software must satisfy the relevant upstream obligations.

---

## 9. No formal Compatibility Claim exists yet

The project must not currently claim:

```text
All Kindle Compatible
Kindle PW5 Compatible
Android E-Paper Compatible
BOOX Compatible
```

A formal Compatibility Record must bind real test evidence to the exact Device / Firmware / Platform / Adapter / Profile / Quirk / Contract / Lua Profile / BICTS combination.

Evidence-based states are:

```text
Compatible
Experimental
Unsupported
```

---

## 10. Current priorities

### Track A — Distribution Conformance

```text
Reference Repository / Client
Independent verifier
Cross-language vectors
E2E / offline transfer / rollback
Stable Gate
```

### Track B — Documentation migration

```text
Standards 20–28
→ Design
→ Reference Apps
→ remove Legacy Public Trees
```

### Track C — Device Adapter / Kindle

```text
spec/adapter IDL
→ generated interface
→ Mock Adapter
→ Adapter Contract Test Harness
→ kindlehf substrate bring-up
→ Kindle Base Adapter
→ baga-probe.ikp
→ Base BICTS
```

Do not begin with the full LifeBook product or automated jailbreak Client path.

---

## 11. Current project entry points

English:

```text
README.md
docs/en/00_baga-ink-documentation-index.md
docs/en/status/00_baga-ink-project-status.md
docs/en/standards/00_baga-ink-standards-index.md
docs/en/governance/00_baga-ink-development-governance.md
```

Simplified Chinese:

```text
README.zh-CN.md
docs/zh-CN/00_项目文档入口.md
docs/zh-CN/status/00_当前项目状态.md
docs/zh-CN/standards/00_规范总览.md
docs/zh-CN/governance/00_开发治理.md
```

---

## 12. Final status rule

> **A document existing does not mean the implementation is complete; code compiling does not mean a device is Compatible; one successful launch does not mean Stable.**

Baga Ink status must ultimately be supported by:

```text
Code
+ Machine-readable Spec
+ Tests
+ Device Evidence
+ Conformance
+ Approved Public Docs
```
