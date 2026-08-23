# Baga Ink Project Status

> **Document level:** Canonical Project Status  
> **Document ID:** `status.00`  
> **Locale:** English (`en`)  
> **Status:** Living Status v0.5  
> **Date:** 2026-08-23  
> **Counterpart:** `docs/zh-CN/status/00_当前项目状态.md`  
> **Authoritative branch:** `main`

---

## 0. Current summary

> **Baga Ink is in Standards + Executable Conformance + Reference Platform implementation preparation. All public Standards 00–13 and 20–28 now have maintained English and Simplified Chinese editions, but production Platform / Kindle / Android E-Paper / Client / Market implementations and formal device Compatibility evidence are not complete.**

Current baselines include:

```text
complete Draft/Baseline Standards 00–28 in both maintained locales
machine-readable distribution/signing/repository specification foundation
Python reference implementation + conformance tests
Device Adapter Contract
Kindle / Android E-Paper adapter standards
Kindle Implementation Architecture Freeze
Device Adapter executable-contract / SDK design
Kindle implementation plans + governed Task/Execution Prompt model
English-default README + scalable locale switching
Apache-2.0 + explicit third-party licensing boundary
protected main + required CI
```

The project cannot yet claim production completeness or formal device compatibility.

---

## 1. Standards

All current public Standards are now localized and marked `current` in `docs/localization/catalog.json`.

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

This does **not** mean the standards are Stable. Stable still requires executable evidence where applicable.

---

## 2. Executable distribution-specification status

Implemented foundations include strict JSON/JCS, SHA-256/Ed25519, JSON Schema, Publisher Identity, App Ownership, App Signing Delegation, IKP payload/signature validation, ZIP/path safety, invalid fixtures, and Python CI.

Still required for Stable distribution claims:

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

## 3. Device Adapter / SDK status

Standard 07 defines the device porting contract. The frozen principle is:

> **Define what the device must provide; reuse proven OS, Vendor SDK, Homebrew, and mature open-source mechanisms instead of reimplementing the device.**

Still missing:

```text
spec/adapter machine IDL
code generation
generated SDK interfaces
Mock / Headless Adapter
reusable Adapter Contract Test Harness
```

---

## 4. Kindle status

Kindle is the first Reference Platform Port.

Frozen implementation direction includes:

```text
Client / bootstrap
→ Homebrew-ready device
→ KPM or validated legacy installer envelope
→ Baga Ink Platform
→ IKP Package Manager
→ lifebook.ikp / other Baga Apps
→ Kindle Home Entry
```

Important boundaries remain:

- `.ikp` is not converted to `.kpkg`;
- KPM manages native Platform, IKP Package Manager manages Baga Apps;
- KOReader / koreader-base / FBInk are mature internal mechanisms, not LifeBook APIs;
- Kindle Adapter should remain thin and reuse them;
- Reader/UI, jailbreak routes, KPM/MRPI, and Home Entry are not Device Adapter root subsystems;
- first real bring-up targets a representative `kindlehf` path and a Probe IKP before full LifeBook.

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

## 5. Android E-Paper status

The standard defines Generic Android Base + Vendor Specialization. A production Android Reference Adapter and real BICTS evidence are still pending.

---

## 6. Documentation internationalization

Completed:

```text
M0    locale architecture / README / licensing / guards
M1-A  Governance + Status + Index
M1-B1 Standards 00–06
M1-B2 Standards 07–13
M1-C  Standards 20–28
```

Next:

```text
M1-D  Design
M1-E  Reference Apps
M4    remove Legacy Public Trees and forbid them in CI
```

---

## 7. Governance / license

`main` is protected by GitHub Ruleset. Required documentation job:

```text
Validate task/prompt layout
```

It covers public-doc i18n, README locale switching, and Platform Port task/prompt structure.

Baga-authored material defaults to Apache License 2.0. Third-party projects retain their upstream licenses. See:

```text
LICENSE
NOTICE
THIRD_PARTY_NOTICES.md
```

---

## 8. Compatibility claim boundary

There is currently no formal claim that a specific Kindle, BOOX, iReader, or Android E-Paper combination is `Baga Ink Compatible`.

A formal record must bind exact Device / Firmware / Platform / Adapter / Profile / Quirk / Contract / Lua Profile / BICTS evidence.

---

## 9. Current priorities

```text
A. Distribution Conformance
   Reference Repository / Client
   Independent verifier
   Cross-language vectors
   E2E / offline / rollback

B. Documentation
   Design → Reference Apps → Legacy removal

C. Device Adapter / Kindle
   IDL → generated interfaces → Mock Adapter → Contract Tests
   → kindlehf bring-up → Base Kindle Adapter → Probe IKP → BICTS
```

Do not begin with full LifeBook feature work or automated jailbreak Client flow before the substrate is proven.

---

## 10. Entry points

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

## 11. Final status rule

> **A document existing does not mean the implementation is complete; code compiling does not mean a device is Compatible; one successful launch does not mean Stable.**

Project state must ultimately be supported by code, machine-readable specs, tests, device evidence, conformance, and approved public documentation.
