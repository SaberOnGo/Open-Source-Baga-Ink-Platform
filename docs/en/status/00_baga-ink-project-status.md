# Baga Ink Project Status

> **Document level:** Canonical Project Status  
> **Document ID:** `status.00`  
> **Locale:** English (`en`)  
> **Status:** Living Status v0.6  
> **Date:** 2026-08-23  
> **Counterpart:** `docs/zh-CN/status/00_当前项目状态.md`  
> **Authoritative branch:** `main`

---

## 0. Current summary

> **Baga Ink is in the Standards + Executable Conformance + Reference Platform implementation-preparation phase. Its long-lived public documentation has completed the English / Simplified Chinese migration, but production Platform / Kindle / Android E-Paper / Client / Market implementations and formal device Compatibility evidence are not complete.**

Current baselines include:

```text
Draft/Baseline Standards 00–28 in both maintained locales
Design 01–02 in both maintained locales
Reference Apps / Kindle Architecture Freeze in both maintained locales
machine-readable distribution/signing/repository specification foundation
Python reference implementation + conformance tests
Baga Device Adapter Contract
Kindle / Android E-Paper Adapter Standards
Kindle implementation plans + governed Task/Execution Prompt model
English-default README + scalable language switching
Apache-2.0 + explicit third-party licensing boundary
protected main + required CI
```

The project cannot yet claim production completeness or formal device compatibility.

---

## 1. Public documentation architecture — COMPLETE

The permanent public-document structure is:

```text
docs/en/
├── standards/
├── design/
├── reference-apps/
├── governance/
└── status/

docs/zh-CN/
├── standards/
├── design/
├── reference-apps/
├── governance/
└── status/
```

All maintained public documents are registered in:

```text
docs/localization/catalog.json
```

The former mixed-language public trees have been removed. CI now rejects recreation of:

```text
docs/standards/
docs/design/
docs/reference-apps/
docs/governance/
docs/status/
old mixed-language root documentation index
```

Engineering plans remain separate. In particular, `docs/plans/platform-ports/kindle/` remains Chinese-first operational material under its strict bilingual filename / Task / Execution Prompt rules.

---

## 2. Standards status

All current Standards are available in maintained English and Simplified Chinese editions and are `current` in the localization catalog.

### Platform / App / Device — 00–13

```text
00 Standards Index
01 Platform Strategy / Architecture
02 App Standard
03 API Specification
04 Capability Registry
05 Permission Model
06 IKP Package Specification
07 Device Adapter Contract
08 Compatibility Standard
09 UI Specification
10 BICTS
11 Kindle Device Adapter
12 Android E-Paper Adapter
13 Standard Libraries / Adopted Components
```

### Distribution / Market / Supply Chain — 20–28

```text
20 Market and Distribution Architecture
21 Publisher Identity and App Ownership
22 IKP Signing and Key Lifecycle
23 Repository Metadata and Index Protocol
24 App Publishing, Review and Version Policy
25 Update, Rollback and Revocation Protocol
26 Distribution Client and Offline Transfer Protocol
27 Transparency and Security Audit Standard
28 Catalog and App Discovery Specification
```

Complete documentation does **not** mean Stable. Standards that require executable evidence must still pass their Stable Gates.

---

## 3. Design / Reference implementation documentation

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

For Kindle implementation, Reference App 03 is the current frozen implementation baseline subordinate to Standards.

---

## 4. Executable distribution-specification status

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

## 5. Device Adapter / SDK status

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

## 6. Kindle status

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

Key boundaries remain:

- `.ikp` is never converted to `.kpkg`;
- KPM manages native Platform packages; IKP Package Manager manages Baga Apps;
- KPM missing != KPM incompatible;
- KOReader / koreader-base / FBInk are mature internal implementation sources, not LifeBook APIs;
- Kindle Adapter should remain thin and reuse mature mechanisms;
- Reader/UI, jailbreak routes, KPM/MRPI, Home Entry, and build tooling are outside the Device Adapter root contract;
- first bring-up should use a representative `kindlehf` path and a Probe IKP before full LifeBook product work.

Not yet implemented:

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

## 7. Android E-Paper status

The Standard defines Generic Android Base + Vendor Specialization. A production Android Reference Adapter and real BICTS evidence are still pending.

---

## 8. Governance and license

`main` is protected by GitHub Ruleset. Required documentation job:

```text
Validate task/prompt layout
```

It validates public-doc localization structure, README locale switching, and Platform Port task/prompt structure.

Baga-authored material defaults to:

> **Apache License 2.0**

Third-party projects retain their upstream licenses. See:

```text
LICENSE
NOTICE
THIRD_PARTY_NOTICES.md
```

---

## 9. Compatibility claim boundary

There is currently no formal claim that a specific Kindle, BOOX, iReader, or other Android E-Paper combination is `Baga Ink Compatible`.

A formal record must bind exact Device / Firmware / Platform / Adapter / Profile / Quirk / Contract / Lua Profile / BICTS evidence.

---

## 10. Current priorities

```text
A. Distribution Conformance
   Reference Repository / Client
   Independent verifier
   Cross-language vectors
   E2E / offline / rollback

B. Device Adapter / Kindle
   IDL → generated interfaces → Mock Adapter → Contract Tests
   → kindlehf bring-up → Base Kindle Adapter → Probe IKP → BICTS

C. Public documentation maintenance
   keep current English / zh-CN pairs synchronized
   add future locales only through governed locale registration
```

Do not begin with full LifeBook feature work or automated jailbreak Client flow before the substrate is proven.

---

## 11. Entry points

English:

```text
README.md
docs/en/00_baga-ink-documentation-index.md
docs/en/standards/00_baga-ink-standards-index.md
docs/en/status/00_baga-ink-project-status.md
```

Simplified Chinese:

```text
README.zh-CN.md
docs/zh-CN/00_项目文档入口.md
docs/zh-CN/standards/00_规范总览.md
docs/zh-CN/status/00_当前项目状态.md
```

---

## 12. Final status rule

> **A document existing does not mean implementation is complete; code compiling does not mean a device is Compatible; one successful launch does not mean Stable.**

Project state must ultimately be supported by code, machine-readable specs, tests, device evidence, conformance, and approved public documentation.
