# Baga Ink Project Status

> **Document level:** Canonical Project Status  
> **Document ID:** `status.00`  
> **Locale:** English (`en`)  
> **Status:** Living Status v0.7  
> **Date:** 2026-08-23  
> **Counterpart:** `docs/zh-CN/status/00_当前项目状态.md`  
> **Authoritative branch:** `main`

---

## 0. Current summary

> **Baga Ink is in the Standards + Executable Conformance + Reference Platform implementation-preparation phase. Public documentation internationalization is complete; the licensing architecture has moved to a community/noncommercial + commercial-OEM model; production Platform / Kindle / Android E-Paper / Client / Market implementations and formal device Compatibility evidence are not complete.**

Current baselines include:

```text
Standards 00–28 in English and Simplified Chinese
Design 01–02 in both maintained locales
Reference Apps / Kindle Architecture Freeze in both maintained locales
machine-readable distribution/signing/repository specification foundation
Python reference implementation + conformance tests
Baga Device Adapter Contract
Kindle / Android E-Paper Adapter Standards
Kindle implementation plans + governed Task/Execution Prompt model
English-default README + scalable language switching
community/noncommercial Platform license + separate commercial OEM licensing
proprietary LifeBook production-app boundary
explicit third-party licensing boundary
protected main + required CI
```

The project cannot yet claim production completeness or formal device compatibility.

---

## 1. Public documentation architecture — COMPLETE

Permanent public documentation lives under:

```text
docs/en/{standards,design,reference-apps,governance,status}
docs/zh-CN/{standards,design,reference-apps,governance,status}
```

All maintained public documents are registered in `docs/localization/catalog.json`.

The old mixed-language public directories have been removed and CI rejects their recreation. `docs/plans/`, especially Kindle Platform Port Task/Execution Prompt material, remains operational engineering documentation and is not fully mirrored by locale.

---

## 2. Standards / Design / Reference Apps

Current Standards:

```text
00–13 Platform / App / Device
20–28 Distribution / Market / Supply Chain
```

Current Design:

```text
01 Executable Specification Design
02 Device Adapter Executable Contract / SDK Design
```

Current Reference Apps:

```text
01 LifeBook Reference App
02 LifeBook Kindle Product Behavior / Accessory Design
03 Kindle Implementation Architecture Freeze
99 Superseded Kindle compatibility entry
```

Documentation completeness does **not** mean the Standards are Stable. Stable status still depends on executable evidence and required gates.

---

## 3. Executable distribution-specification status

Implemented foundations include strict JSON/JCS, SHA-256/Ed25519, JSON Schema, Publisher Identity, App Ownership, App Signing Delegation, IKP payload/signature validation, ZIP/path safety, invalid fixtures, and Python CI.

Still required before Stable distribution claims:

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

## 4. Device Adapter / SDK status

The Device Adapter Contract defines what a device port must provide while allowing concrete implementations to reuse proven OS, Vendor SDK, Homebrew, and mature open-source mechanisms.

Still missing:

```text
spec/adapter machine IDL
code generation
generated SDK interfaces
Mock / Headless Adapter
reusable Adapter Contract Test Harness
```

---

## 5. Kindle status

Kindle is the first Reference Platform Port.

Frozen direction:

```text
Client / bootstrap
→ Homebrew-ready device
→ KPM where compatible, validated legacy envelope where required
→ Baga Ink Platform
→ IKP Package Manager
→ lifebook.ikp / other Baga Apps
→ Kindle Home Entry
```

Key boundaries:

- `.ikp` is never converted to `.kpkg`;
- KPM manages native Platform packages; IKP Package Manager manages Baga Apps;
- KPM missing != KPM incompatible;
- KOReader / koreader-base / FBInk are internal implementation sources, not LifeBook APIs;
- Kindle Adapter remains thin and reuses mature mechanisms;
- Reader/UI, jailbreak routes, KPM/MRPI, Home Entry, and build tooling are outside the Device Adapter root contract;
- first real bring-up uses a representative `kindlehf` path and Probe IKP before full LifeBook.

Still missing:

```text
platform/adapters/kindle/
KindleAdapterFactory
real Device Profiles / Quirk Sets
Base Display/Input/Storage/Lifecycle/Power bindings
pinned product integration
real-device Adapter Contract Tests
Base BICTS
baga-probe.ikp on real Kindle
```

---

## 6. Android E-Paper status

The Standard defines Generic Android Base + Vendor Specialization. A production Android Reference Adapter and real BICTS evidence are still pending.

---

## 7. Licensing architecture — CURRENT

Baga Ink now uses a layered licensing model:

```text
Baga-authored Platform/OEM-side software
→ PolyForm Noncommercial 1.0.0 by default
→ separate Commercial License for OEM/device/platform commercial deployment

ordinary IKP App development
→ kept low-friction; selling an App that targets published Baga APIs does not by itself require an OEM/platform license

LifeBook production App
→ proprietary / closed-source first-party product

third-party components
→ retain upstream licenses
```

The licensing cutover preserves all historical rights already granted under Apache-2.0. The last pre-cutover `main` commit is recorded in `LICENSE_HISTORY.md`.

Canonical licensing documents:

```text
LICENSE
docs/en/governance/02_baga-ink-licensing-policy.md
COMMERCIAL_LICENSE.md
LICENSE_HISTORY.md
NOTICE
THIRD_PARTY_NOTICES.md
```

The Repository Documentation Guard now also validates the licensing architecture through `tools/check_licensing.py`.

External code contributions to dual-licensed Platform/Adapter material may require a legally reviewed CLA before merge so the project does not lose future commercial relicensing rights.

---

## 8. Compatibility claim boundary

There is currently no formal claim that a specific Kindle, BOOX, iReader, Bigme, Hanvon, or other Android E-Paper combination is `Baga Ink Compatible`.

A formal record must bind exact Device / Firmware / Platform / Adapter / Profile / Quirk / Contract / Lua Profile / BICTS evidence.

The software license does not by itself grant official `Baga Ink Compatible` branding or certification.

---

## 9. Current priorities

```text
A. Executable Device Adapter Contract
   machine IDL
   generated interfaces
   Mock Adapter
   Contract Test harness

B. Kindle Reference Port
   pinned KOReader/FBInk substrate
   minimal Platform Core
   Kindle Base Adapter
   Probe IKP on real hardware
   Base BICTS

C. Distribution Conformance
   Reference Repository / Client
   independent verifier
   cross-language vectors
   offline/update/rollback E2E

D. Commercial-readiness foundations
   legally reviewed CLA before broad external code contribution
   third-party/copyleft integration review before commercial distribution
   future trademark / certification policy
```

---

## 10. Source of truth

`main` remains the only long-term project source of truth. Branches, PRs, chat history, and temporary AI context are construction scaffolding, not project memory.
