# Baga Ink Standards Index

> **Document level:** Standards entry point  
> **Document ID:** `standards.00`  
> **Locale:** English (`en`)  
> **Status:** Living Index v0.7  
> **Date:** 2026-08-23  
> **Counterpart:** `docs/zh-CN/standards/00_规范总览.md`

---

## 0. Purpose

`docs/en/standards/` is the English public standards surface for Baga Ink. Its Simplified Chinese counterpart is `docs/zh-CN/standards/`.

The two locale trees describe the **same standards and document identities**. They are not separate protocol branches. Migration/synchronization state is tracked by `docs/localization/catalog.json`.

Standard numbers express importance, dependency order, and domain grouping — not creation time.

The normative standards describe the **currently approved design**. Rejected or superseded interfaces, namespace names, and architecture drafts belong in Git history rather than the active standards text.

---

## 1. Standards hierarchy

```text
01 Platform Strategy & Architecture
│
├── Platform and App Layer 02–09
│   ├── 02 App Standard
│   ├── 03 API Specification
│   ├── 04 Capability Registry
│   ├── 05 Permission Model
│   ├── 06 IKP Package Specification
│   ├── 07 Device Adapter Contract
│   ├── 08 Compatibility Standard
│   └── 09 UI Specification
│
├── Tests, Device Reference Ports, Standard Libraries 10–19
│   ├── 10 Compatibility Test Suite / BICTS
│   ├── 11 Kindle Device Adapter
│   ├── 12 Android E-Paper Adapter
│   └── 13 Standard Libraries / Adopted Components
│
└── Market and Distribution Security 20–29
    ├── 20 Market & Distribution Architecture
    ├── 21 Publisher Identity & App Ownership
    ├── 22 IKP Signing & Key Lifecycle
    ├── 23 Repository Metadata & Index Protocol
    ├── 24 Publishing / Review / Version Policy
    ├── 25 Update / Rollback / Revocation Protocol
    ├── 26 Distribution Client / Offline Transfer
    ├── 27 Transparency / Security Audit
    └── 28 Catalog / App Discovery
```

---

## 2. Platform core loop

```text
App Standard
   ↓
Baga Ink API + Baga Lua Profile / Standard Libraries
   ↓
Baga Ink Platform Core
   ↓
Device Adapter Contract
   ↓
Kindle / Android E-Paper / future OEM devices
   ↓
Adapter Contract Tests + Compatibility Standard + BICTS
```

Three concepts must remain distinct:

```text
baga.*
→ normalizes device / OS / Platform differences

Device Adapter Contract
→ defines what a new device port must provide

Standard Libraries / Adopted Components
→ directly adopt mature, general-purpose software capabilities
```

Important examples:

```text
SQLite + lsqlite3
→ Stable Standard Library

Automerge core
→ Adopted Local-first / CRDT Foundation
→ may be adopted as a whole or by selected modules

KOReader / FBInk / Vendor SDK / OS mechanisms
→ mature implementation sources inside a device/platform port
→ do not become new public architecture layers merely because Baga reuses them
```

If an app bypasses this loop through private device interfaces, Baga becomes fragmented again. If mature general-purpose libraries are wrapped without reason, Baga creates unnecessary duplicate abstractions.

---

## 3. Formal role of the Device Adapter

Standard 07, the Device Adapter Contract, is written for:

```text
Baga Platform implementers
OEM / device vendors
third-party device porters
Adapter maintainers
```

It defines:

```text
Root Adapter / Factory
DeviceDescriptor
Capability Snapshot
Display / Input / Storage / Lifecycle / Power typed subsystems
Optional Network / Light / Audio / Bluetooth / UserLibrary subsystems
Event / Error model
Device Profile / Quirk Set
Self-test
Contract Versioning
Adapter Contract Tests
```

Core rule:

> **The contract defines what must be provided; it does not require reimplementing capabilities the device already has.**

For example, the Kindle Adapter SHOULD reuse mature KOReader, FBInk, Kindle OS, and Homebrew mechanisms and add only the thin Baga mapping, normalization, Profile/Quirk handling, and tests required by the contract.

---

## 4. Distribution security loop

```text
Publisher Identity
        ↓
App Ownership + App Key Delegation
        ↓
Publisher-signed IKP
        ↓
Signed Repository Metadata
        ↓
Baga Ink Client / Device Direct / Offline Snapshot
        ↓
Device Final Verification
        ↓
Staged Install → Health Check → Active / Rollback
```

Publisher Signature, Repository Metadata, and Local Installed Identity form distinct trust layers and must all remain valid where applicable.

---

## 5. Canonical document map

### 5.1 Platform Core Standards 00–09

| No. | English document | Purpose |
|---|---|---|
| 00 | `00_baga-ink-standards-index.md` | Standards entry point and reading order |
| 01 | `01_baga-ink-platform-strategy.md` | Highest-level platform strategy and architecture |
| 02 | `02_baga-ink-app-standard.md` | Compliance boundary for third-party IKP apps |
| 03 | `03_baga-ink-api-specification.md` | Public `baga.*` API |
| 04 | `04_baga-ink-capability-registry.md` | Capability names, semantics, stability |
| 05 | `05_baga-ink-permission-model.md` | Permissions and least-privilege rules |
| 06 | `06_ikp-package-specification.md` | `.ikp` package structure and validation |
| 07 | `07_baga-ink-device-adapter-specification.md` | Device Adapter Porting Contract / OEM implementer contract |
| 08 | `08_baga-ink-compatibility-standard.md` | `Baga Ink Compatible` requirements |
| 09 | `09_baga-ink-ui-specification.md` | E-paper UI and refresh behavior |

### 5.2 Tests, device ports, standard libraries 10–19

| No. | English document | Purpose |
|---|---|---|
| 10 | `10_baga-ink-compatibility-test-suite.md` | Adapter integration + API/Profile/Standard Library device tests |
| 11 | `11_baga-ink-kindle-adapter.md` | First Reference Port of Standard 07; maximizes reuse of mature Kindle capabilities |
| 12 | `12_baga-ink-android-e-paper-adapter.md` | Android E-Paper device-family implementation of Standard 07 |
| 13 | `13_baga-ink-standard-libraries-and-adopted-components.md` | Rules for SQLite/lsqlite3, Automerge, and other mature components |
| 14–19 | Reserved | Future device families / Adapter / Test / Compatibility supplements |

### 5.3 Market and distribution security 20–29

| No. | English document | Purpose |
|---|---|---|
| 20 | `20_baga-ink-market-and-distribution-architecture.md` | Distribution architecture |
| 21 | `21_baga-ink-publisher-identity-and-app-ownership-standard.md` | Publisher / App Ownership |
| 22 | `22_baga-ink-ikp-signing-and-key-lifecycle-standard.md` | IKP signing / keys |
| 23 | `23_baga-ink-repository-metadata-and-index-protocol.md` | Repository / TUF profile |
| 24 | `24_baga-ink-app-publishing-review-and-version-policy.md` | Publishing / review / version |
| 25 | `25_baga-ink-update-rollback-and-revocation-protocol.md` | Update / rollback / revocation |
| 26 | `26_baga-ink-distribution-client-and-offline-transfer-protocol.md` | Client / offline transfer |
| 27 | `27_baga-ink-transparency-and-security-audit-standard.md` | Transparency / audit |
| 28 | `28_baga-ink-catalog-and-app-discovery-specification.md` | Catalog / discovery |
| 29 | Reserved | Future distribution work |

During the documentation migration, some English files listed above are not yet `current`. Always consult `docs/localization/catalog.json` before treating a path as a completed translation.

---

## 6. Reference Apps and Kindle implementation freeze

Reference App documents are not Standards and must not override higher-level standards.

Target English paths:

```text
docs/en/reference-apps/
├── 01_lifebook-reference-app.md
├── 02_lifebook-kindle-product-behavior-and-accessory-extension-design.md
├── 03_baga-ink-kindle-implementation-architecture-freeze.md
└── 99_lifebook-architecture-and-kindle-compatibility-superseded.md
```

Authority boundary:

```text
Standards 07 / 11
→ Device Adapter Contract and Kindle Adapter Reference Port

Reference App 03
→ Kindle-wide Client/bootstrap/KPM/MRPI/Platform/IKP/Home Entry implementation freeze
```

Reference App 03 does not replace Standards 07 or 11.

---

## 7. Approved Design

The Device Adapter implementation program is described by the localized Design document for the executable Adapter Contract and SDK.

It covers:

```text
machine-readable Adapter IDL
Codegen
Rust / C / Kotlin generated interfaces
Mock / Headless Adapter
Adapter SDK
Contract Test harness
Kindle / Android skeletons
```

Design documents explain implementation decisions and must not override Standard 07 semantics.

---

## 8. Reading order

### 8.1 First introduction to Baga Ink

```text
00 → 01 → 02 → 03 → 13 → 07 → 08 → 20
```

### 8.2 Third-party app development

```text
02 → 03 → 13 → 04 → 05 → 06 → 09
```

Developers should understand the distinction:

```text
device capabilities → baga.*
relational database → require("lsqlite3")
Automerge → Adopted Foundation
```

For publishing:

```text
21 → 22 → 24 → 25 → 28
```

### 8.3 Device Adapter / OEM port development

```text
01 → 03 → 04 → 07 → 10 → device family 11/12/... → Design 02
```

LifeBook is not the interface specification for implementing a Device Adapter; it is a later smoke/reference validation app.

### 8.4 Kindle Platform / Adapter development

```text
07 → 11 → Reference App 03 → Design 02 → 10
```

Maintain:

```text
Device Adapter
≠ jailbreak/install route
≠ KPM/MRPI
≠ Reader/UI framework
```

### 8.5 OEM/device certification

```text
07 → device-family Adapter → 10 → 08
```

### 8.6 Market / Repository

```text
20 → 21 → 22 → 23 → 24 → 25 → 27 → 28
```

### 8.7 Baga Ink Client

```text
20 → 23 → 25 → 26 → 28
```

---

## 9. Number ranges

```text
00        Index
01–09     Platform Core Standards
10–19     Tests / Device Adapters / Standard Libraries / Compatibility supplements
20–29     Market / Distribution / Signing / Supply Chain
30–39     Sync / Cloud / Account / Cross-device Data Protocols
40–49     Developer Tools / CLI / Simulator
50–59     Optional Extensions
60–69     OEM / Enterprise
70–79     Operations / Observability
80–89     Reserved
90–99     Experimental
```

The numeric prefix is a stable document number, not an execution-task counter.

---

## 10. Authority boundaries

```text
01      top-level strategy / public architecture
02      compliant Baga Ink App
03      public baga.* API
04      Capability
05      Permission
06      IKP
07      Device Adapter Porting Contract
08 / 10 Compatible / tests
11 / 12 device-family mappings of Standard 07
13      Standard Libraries / Adopted Mature Components
20–28   distribution / security / updates / Catalog
```

Before creating another platform abstraction, check Standard 13 first. If a mature general-purpose library already exposes a better abstraction, Baga SHOULD prefer direct adoption over a weaker private wrapper.

Device Adapter implementations follow the same philosophy: reuse OS / Vendor SDK / Homebrew / mature open-source capabilities, then add only the thin contract mapping Baga needs.

---

## 11. Change governance

- Changes to 01–03 require architecture-level review.
- Standard Library / Adopted Component decisions update 13.
- New Capabilities update 04.
- New Permissions update 05.
- IKP changes update 06.
- Device Adapter Contract changes update 07.
- Kindle/Android family implementation mappings update 11/12.
- Adapter machine IDL and code generation must stay synchronized with 07 and pass compatibility checks.
- Compatible behavior changes update 08/10.
- SQLite / lsqlite3 baseline changes require BICTS regression.
- If Automerge becomes a stable developer-facing Lua module or wire protocol, its version and migration rules must be explicit; never specify merely "latest".
- Replaced or rejected API names, namespaces, and architecture drafts MUST be removed from active Standards / Reference Apps; Git preserves history.

---

## 12. Three core loops

### 12.1 App / Platform

```text
Developer
  ↓
App Standard
  ↓
Baga API + Lua Profile / Standard Libraries
  ↓
Platform Core
```

### 12.2 Device Port

```text
Platform Core
  ↓
Device Adapter Contract
  ↓
Device-family Adapter implementation
  ↓
OS / Vendor SDK / mature existing capability
  ↓
Adapter Contract Tests
  ↓
BICTS / Compatible
```

### 12.3 Publishing / updates

```text
Publisher
  ↓
Signed IKP
  ↓
Repository + Review
  ↓
Catalog / Client / Offline Transfer
  ↓
Device Verification
  ↓
Stage / Activate / Health Check / Rollback
```

---

## 13. Core judgment

Baga Ink creates a unified platform by combining:

```text
device differences → Device Adapter Contract → stable Baga API
mature general-purpose software → direct adoption as Standard Library / Foundation
installation / update / permission / compatibility → shared protocols and tests
```

This file is the canonical English entry point for the Baga Ink Standards set.
