# Baga Ink Platform Strategy & Architecture

> **Document level:** Strategic Source of Truth / highest-level project definition  
> **Document ID:** `standards.01`  
> **Locale:** English (`en`)  
> **Status:** Strategic Baseline v0.6  
> **Date:** 2026-08-23  
> **Standards index:** `00_baga-ink-standards-index.md`  
> **Counterpart:** `docs/zh-CN/standards/01_顶层战略与架构.md`

---

## 0. Authority of this document

This document defines the long-term strategic boundary of **Baga Ink**: platform positioning, ecosystem naming, application model, developer model, device-compatibility model, and anti-fragmentation principles.

It is the highest-level technical strategy document in the Baga Ink Standards set.

Lower-level Standards, SDKs, Platform Core, Device Adapters, Baga Ink Client, Baga Ink Market, LifeBook Reference App, and future OEM ports MUST NOT silently violate it.

### 0.1 Normative language

- **MUST**: platform-level hard requirement.
- **SHOULD**: expected default unless there is a justified exception.
- **MAY**: permitted implementation choice.

### 0.2 Lightweight terminology principle

At the device side, the conceptual platform should remain understandable as:

```text
Baga Ink Platform
├── Baga Ink Platform Core
├── Embedded Lua Interpreter
├── Baga Lua Profile
├── Baga Ink API
├── IKP Package Manager
└── Baga Ink Device Adapter
```

The Lua interpreter is a lightweight implementation capability embedded or reused inside Platform Core. It is not a separate product layer that users must install, understand, or maintain.

Baga MUST NOT be presented as requiring an additional heavyweight middleware/runtime product simply to run applications.

### 0.3 Mature implementation reuse

Baga Standards define:

```text
public APIs
cross-device semantics
Capability / Permission rules
compatibility and security boundaries
Baga Lua Profile / Standard Libraries
```

They **do not prescribe the internal software layering of every Platform implementation**, and they do not require mature capabilities to be reimplemented from zero.

Platform Core, Device Adapters, and official device ports SHOULD first evaluate mature, actively maintained, license-compatible, empirically verified components. Reuse MAY include:

```text
adopt the project as a whole
compose selected components
extract stable modules
use a mature upstream API directly
reuse an existing protocol / data format / algorithm
wrap an existing device mechanism
```

When a general-purpose library already provides a stable, portable, widely adopted abstraction, Baga SHOULD prefer direct adoption as a **Standard Library / Adopted Component** instead of inventing a weaker Baga-specific wrapper.

Current examples:

```text
SQLite + lsqlite3
→ Standard database library for Baga Lua Profile
→ developers use SQLite / SQL semantics directly

Automerge core
→ preferred Local-first / CRDT foundation
→ may be used as a whole or by selected document/merge, binary, sync, C FFI, patch/cursor modules

KOReader / koreader-base / FBInk
→ mature implementation sources for Kindle Platform / Adapter work
```

Reuse of such projects:

- MUST NOT automatically create a new public Baga architecture layer;
- MUST NOT create a `Provider`, `Engine`, or `Runtime` layer merely because a library is used;
- MUST NOT automatically expose the library's private objects, terminology, internal file formats, or APIs as `baga.*` standards;
- MAY make a mature upstream API/protocol/format part of Baga Standard Libraries only after an explicit standards decision;
- MUST NOT require IKP Apps to know the concrete device implementation below the Platform;
- MUST NOT bypass BICTS, Permission, Sandbox, or Compatibility requirements.

Principle:

> **Reuse before reimplement. Standardize semantics, not internal implementation layering.**

Detailed adopted-component rules are defined by Standard 13.

Active Standards / Reference Apps describe only the current approved design. Historical proposals remain in Git history.

---

## 1. One-sentence definition

> **Baga Ink Platform is a unified, lightweight, cross-device application platform for Kindle and Android e-paper devices.**

The goal is not to build one more e-paper app. The goal is:

> **Make fragmented Kindle Homebrew and Android E-Paper devices look progressively like one application platform to third-party developers.**

---

## 2. The strategic problem

The e-paper ecosystem is highly fragmented.

```text
Kindle
├── many device generations
├── many firmware generations
├── Homebrew / KUAL / MRPI / KOReader infrastructure
└── different display / input / system behaviors

Android E-Paper
├── iReader
├── BOOX
├── Bigme
├── Hanvon
├── Moaan
└── other vendors
    ├── different Android versions
    ├── different refresh APIs
    ├── different Pen SDKs
    └── different power / frontlight / system APIs
```

If every app developer adapts independently to every device, fragmentation becomes a permanent property of the application ecosystem.

Baga's strategy is:

> **Compress fragmentation below the Device Adapter boundary instead of spreading it through every application.**

---

## 3. Public architecture

```text
                   Third-party IKP Apps
                          │
                          ▼
                Baga Ink App Standard
                          │
                          ▼
            Baga Ink SDK / Baga Ink API
                          │
                          ▼
                Baga Ink Platform Core
                          │
                          ▼
                Baga Ink Device Adapter
                     ┌────┴────┐
                     │         │
                     ▼         ▼
                  Kindle    Android E-Paper
```

Core rule:

> **Apps do not adapt to devices; devices adapt to the platform through a Baga Device Adapter.**

Reusing KOReader, SQLite, Automerge, FBInk, or other components inside an implementation does not add public layers to this architecture.

Baga Lua Profile Standard Libraries are likewise not another architecture layer; they are mature libraries made predictably available inside the application environment.

---

## 4. Brand and product hierarchy

```text
                         Baga Ink
                  ecosystem / project brand
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
 Baga Ink Platform   Baga Ink Client   Baga Ink Market
  device platform      PC / Mac          app ecosystem
          │
          ▼
        Apps
          │
    ┌─────┼───────────────┐
    │     │               │
 LifeBook RSS / Reader   Notes / AI / ...
```

Canonical names:

| Object | Canonical name |
|---|---|
| Ecosystem / project brand | **Baga Ink** |
| Unified device-side platform | **Baga Ink Platform** |
| PC / Mac client | **Baga Ink Client** |
| App market | **Baga Ink Market** |
| SDK | **Baga Ink SDK** |
| API | **Baga Ink API** |
| Application standard | **Baga Ink App Standard** |
| Capability standard | **Baga Ink Capability Registry** |
| Permission standard | **Baga Ink Permission Model** |
| App package format | **IKP / `.ikp`** |
| Device-port boundary | **Baga Ink Device Adapter** |
| Compatibility standard | **Baga Ink Compatibility Standard** |
| Test suite | **Baga Ink Compatibility Test Suite / BICTS** |
| Standard library policy | **Baga Ink Standard Libraries and Adopted Components** |
| Developer portal | **Baga Ink Developers** |
| Flagship Reference App | **LifeBook** |
| Kindle product description | **LifeBook for Kindle** |

---

## 5. Baga Ink Platform boundary

Baga Ink Platform includes:

- Platform Core;
- Embedded Lua Interpreter;
- Baga Lua Profile;
- Baga Lua Profile Standard Libraries;
- Baga Ink API;
- App Lifecycle;
- standardized UI / Display / Input / Storage / Library / Network / Power / Reader / Sync capabilities;
- Capability Model;
- Permission / Sandbox;
- IKP Package Manager;
- Device Adapter;
- Compatibility hooks.

These together form one lightweight device-side platform.

**Baga Ink Platform is not Baga Ink Client and is not Baga Ink Market.**

The internal implementation of these capabilities may reuse mature projects. Those projects are not extra product layers.

---

## 6. Universal App model

### 6.1 Primary application language

The first official Universal App language is:

> **Lua / Baga Lua Profile**

Baga Lua Profile defines:

- allowed language features;
- baseline standard-library surface;
- Adopted Standard Libraries;
- `baga.*` API;
- lifecycle;
- security restrictions;
- system-escape restrictions.

A Kindle implementation MAY reuse the proven Lua / LuaJIT environment of KOReader or related projects. An Android Baga Platform APK MAY embed a lightweight Lua interpreter directly.

Third-party Apps do not depend on where the interpreter came from.

Current stable external Standard Library:

```text
lsqlite3
→ mature SQLite / SQL semantics exposed directly
```

Current Adopted Foundation:

```text
Automerge core
→ preferred Local-first / CRDT foundation
→ developer-facing Lua binding is not yet frozen
```

Detailed rules are defined by Standard 13.

### 6.2 Why Kotlin / Java is not the universal app boundary

Android naturally supports Kotlin / Java; Kindle is not Android.

Making Kotlin / Java the cross-device app language would force a heavyweight implementation layer onto legacy Kindle devices and conflict with Baga's lightweight, installed-base strategy.

### 6.3 Role of Rust

Rust is well suited to implementation areas such as:

```text
Platform Core
network / sync infrastructure
parsers
security-sensitive components
Device Adapter
Automerge core / C FFI integration
```

Platform internals MAY use Rust, C/C++, Kotlin/Java, JNI, Shell, or other device-appropriate implementation languages.

> **Language unification happens at the third-party App boundary, not across all low-level implementation code.**

The same applies to internal library selection: internal components do not create new boundaries third-party Apps must understand.

---

## 7. IKP: portable application distribution unit

The Universal App package format is:

> **IKP / `.ikp`**

Examples:

```text
lifebook.ikp
rss-reader.ikp
notes.ikp
```

The same IKP is intended to run across Kindle and Android E-Paper where capabilities allow.

Typical contents:

```text
manifest.json
main.lua
src/
assets/
locales/
signature/
```

A Universal IKP MUST NOT use the following as normal app-execution dependencies:

```text
device-specific native binary
Android APK / DEX business logic
Kindle shell bridge
BOOX / iReader private SDK wrapper
its own Lua interpreter
its own Device Adapter
its own Platform Core
```

Principle:

> **Application code/resources belong in IKP; device compatibility and shared platform capabilities belong in Baga Ink Platform.**

Standard Libraries provided by Baga Lua Profile do not need to be duplicated in every IKP.

---

## 8. Capability-first development

Universal Apps MUST query capabilities, not brands.

Correct:

```lua
if baga.device.has("input.pen") then
    enable_pen_ui()
end

if baga.device.has("display.fast_refresh") then
    enable_fast_interaction()
end
```

Incorrect:

```lua
if vendor == "BOOX" then ... end
if device == "Kindle" then ... end
```

Canonical capabilities are defined only by Standard 04, the Capability Registry.

Base Profile:

```text
display.basic
input.navigation
storage.app_sandbox
power.sleep_wake
platform.lifecycle
```

Typical optional capabilities:

```text
display.partial_refresh
display.fast_refresh
display.color
input.touch
input.pen
input.pen.low_latency
input.physical_page_key
network.wifi
light.frontlight
audio.output
bluetooth.available
```

SQLite / lsqlite3 is a Baga Lua Profile Standard Library, not a hardware capability.

---

## 9. Permission and Capability are different

Capability answers: **can the device/platform do it?**

Permission answers: **may this App access it?**

Example:

```text
Capability: network.wifi
Permission: network
```

Permissions are predeclared in the Manifest and follow least-privilege principles. Standard 05 defines the model.

---

## 10. Baga Ink API is the stable device/platform App boundary

Public namespaces:

```lua
baga.api
baga.app
baga.ui
baga.display
baga.input
baga.device
baga.storage
baga.library
baga.network
baga.power
baga.reader
baga.sync
baga.permissions
baga.log
```

Relational structured data uses the Baga Lua Profile Standard Library `lsqlite3` / SQLite directly.

The stable developer environment therefore contains two distinct concepts:

```text
baga.*
→ normalizes device / OS / Platform differences

lsqlite3 / adopted libraries
→ directly expose mature general-purpose software capabilities
```

Baga MUST NOT expose a universal escape hatch for arbitrary shell execution, Android Context access, or direct Vendor SDK access.

New platform capability flow:

```text
real requirement
  ↓
is it already solved by a mature general-purpose library?
  ↓
yes → Standard Library / Adopted Component
no, and it represents device/platform variation → Capability / Baga Ink API
  ↓
Platform implementation
  ↓
BICTS
```

Internal implementation may directly reuse mature projects without adding artificial public `Provider` / `Engine` layers.

---

## 11. UI strategy

Baga UI is not a mechanical mobile-UI port.

Core principles:

- high contrast;
- page-oriented / stable layouts first;
- Focus is a first-class concept;
- touch and physical navigation unify at the semantic level;
- minimal animation;
- minimal full-screen refresh;
- Dirty Region updates;
- App expresses refresh intent; Platform chooses the actual refresh mechanism;
- Color / Pen / Fast Refresh are progressive enhancement.

Standard 09 defines the normative behavior.

---

## 12. Device Adapter strategy

```text
Baga Ink Platform Core
        │
        ├── Kindle Adapter
        └── Android E-Paper Adapter
             ├── Generic Android
             ├── BOOX specialization
             ├── iReader specialization
             ├── Bigme specialization
             ├── Hanvon specialization
             └── future vendor specializations
```

The Adapter absorbs differences in:

```text
Display / refresh
Input
Storage mapping
Lifecycle
Power
Network
Frontlight
Pen
Audio
Bluetooth
Device quirks
Firmware differences
```

The Adapter MUST NOT become a second App API.

Vendor-specialized providers inside the Android Adapter are implementation details for private vendor capabilities; they do not imply that all `baga.*` calls need a generic Provider layer.

---

## 13. Kindle strategy

The existing Kindle Homebrew ecosystem is a foundation to reuse, not something Baga intends to replace from scratch.

Baga SHOULD reuse mature capabilities such as:

```text
KOReader device / reader / display / input / annotation knowledge
koreader-base / MuPDF / CREngine reader foundations
KUAL / PEKI-class launch/bootstrap capabilities where applicable
MRPI / KPM / Hotfix-class installation and Homebrew foundations
FBInk / framebuffer display capabilities
Kindle system-service bridges
KOReader's existing libsqlite3
KOReader internal lua-ljsqlite3 where it remains an implementation detail
Baga IKP standard SQLite binding: lsqlite3
Automerge core when Local-first / CRDT behavior is actually required
```

All of these are **implementation and Standard Library supply choices inside Baga Ink Platform on Kindle**; they do not automatically create public architecture layers.

Third-party IKP Apps see:

```text
device capabilities → baga.*
relational database → require("lsqlite3")
```

They do not need to know whether KOReader internally still uses another SQLite Lua binding.

The Kindle Adapter specification and the mutable jailbreak/installation route database MUST remain separate. Jailbreak routes vary by exact device/firmware; the Platform contract must remain stable.

---

## 14. Android E-Paper strategy

Conceptually:

```text
Baga Ink Platform.apk
        │
        ├── Platform Core
        ├── Baga Ink API
        ├── Baga Lua Profile / Standard Libraries
        ├── Embedded Lua Interpreter
        └── Android E-Paper Adapter
        │
        ▼
      *.ikp
```

Generic Android provides common Android capabilities. Vendor specialization adds private e-paper refresh, Pen, frontlight, and similar capabilities.

Android-version and vendor fragmentation must stop below the Adapter boundary.

Android implementations SHOULD also reuse mature system/open-source capabilities rather than reimplement databases, networking, document engines, or synchronization merely to make internal code look uniform.

Baga Platform pins a predictable SQLite runtime for IKP Apps through `lsqlite3` instead of relying on arbitrary OEM SQLite versions.

---

## 15. Baga Ink Client strategy

Baga Ink Client is the planned Windows/macOS device entry point.

Core flow:

```text
connect device
  ↓
detect model / firmware / system
  ↓
query Compatibility / Installation Database
  ↓
Compatible / Experimental / Unsupported
  ↓
safely install / repair / update Baga Ink Platform
  ↓
install LifeBook / Market Apps
```

Hard rules:

- do not delete user books;
- do not delete user notes;
- factory reset is not a standard solution;
- failure should be recoverable where practical;
- unvalidated combinations must not be presented as supported.

---

## 16. Baga Ink Market strategy

Market is not merely an APK/script download site.

It reinforces platform standards through:

```text
IKP validation
publisher signature
API compatibility
Capability compatibility
Permission disclosure
Universal / Enhanced labels
update / rollback
Compatibility data
```

Long-term Market MAY also distribute fonts, dictionaries, themes, Device Adapters, Capability Providers, and service extensions, provided they follow the appropriate controlled standards.

---

## 17. Compatibility must be verifiable

A device does not become Compatible merely because it can launch LifeBook once.

Formal compatibility is based on:

> **Baga Ink Compatibility Test Suite / BICTS**

A compatibility statement binds:

```text
Device Model
+ Firmware / OS Range
+ Platform Version
+ Adapter Version
+ Compatibility Standard Version
+ BICTS Version
```

States:

```text
Baga Ink Compatible
Experimental
Unsupported
```

Standards 08 and 10 define the detailed rules.

Standard Libraries also require consistency tests, including lsqlite3 behavior, SQLite compile profile, and sandbox behavior.

---

## 18. Strategic role of LifeBook

LifeBook is:

> **Baga Ink's flagship Reference App.**

LifeBook must obey the same core rules as a third-party Universal App instead of depending on privileged shortcuts.

Target:

```text
same lifebook.ikp
      │
      ├── Kindle
      └── Android E-Paper
```

When LifeBook exposes a missing general capability, first decide:

```text
device/platform difference → baga.* / Capability
mature general-purpose capability → Standard Library / Mature Component
```

Do not add vendor-specific business branches or duplicate mature infrastructure.

---

## 19. Open ecosystem, controlled boundaries

Baga SHOULD allow:

- third-party IKP Apps;
- third-party Device Adapter contributions;
- OEM-maintained Adapters;
- controlled Capability Provider contributions;
- third-party SDK / Platform Core contributions;
- Standard Library integration / compatibility-test contributions.

Openness does not mean absence of standards.

Fundamental principle:

> **Allow diversity below; preserve unity above.**

```text
App layer          highly unified
API layer          highly stable
Standard Libraries direct mature semantics
Capability layer   standardized device/platform extensions
Adapter layer      device diversity allowed
OS layer           may differ completely
Hardware layer     may differ completely
```

Internal dependency graphs and source-directory structures are not part of the public layer model.

---

## 20. Initial implementation roadmap

### Phase 0 — Standards

Establish:

```text
App Standard
API
Standard Libraries / Adopted Components
Capability Registry
Permission Model
IKP
Device Adapter Standard
Compatibility Standard
UI Standard
BICTS
Kindle Adapter
Android E-Paper Adapter
```

### Phase 1 — Reference Platforms

Build:

```text
Kindle Reference Adapter
+
Android E-Paper Reference Adapter
```

Prove that the same IKP can execute across two fundamentally different platform families.

Also validate:

```text
lsqlite3 + pinned SQLite
KOReader reader/UI integration
Automerge core feasibility on representative hardware
```

### Phase 2 — LifeBook Reference App

Build the LifeBook Universal Skeleton + Reading Core.

### Phase 3 — SDK / CLI / Simulator

Make it possible for ordinary developers to build IKPs without knowing Kindle/private vendor interfaces.

### Phase 4 — Market / Compatibility

Build signing, distribution, BICTS, and Compatible certification.

### Phase 5 — OEM adoption

Enable vendors to implement Adapters, run the conformance suite, and declare support for Baga Ink Apps.

---

## 21. Long-term moat

The durable value is the network of:

```text
unified standards
+
IKP
+
API
+
Standard Libraries
+
Capability Registry
+
Device Adapters
+
BICTS
+
installed-device coverage
+
Market
+
developers
+
OEM support
```

Network effect:

```text
more devices
  ↓
more users
  ↓
more developers
  ↓
more IKP Apps
  ↓
Baga compatibility becomes more valuable
  ↓
more OEMs choose to implement the platform contract
```

---

## 22. Non-goals

Baga Ink is not currently trying to:

1. build a complete custom e-paper OS;
2. replace Android;
3. replace Kindle OS;
4. rewrite the entire Kindle Homebrew ecosystem;
5. force all low-level code to use Lua;
6. force Platform Core to use one implementation language;
7. allow Universal Apps to escape arbitrarily into the host system;
8. maintain separate application business-logic forks per device brand;
9. turn LifeBook-private requirements into platform standards automatically;
10. build a redundant heavyweight middleware product that must be separately maintained;
11. create a new public architecture layer merely because an open-source library is used;
12. reimplement readers, databases, merge algorithms, or device infrastructure purely for "full self-development" when mature license-compatible verified implementations exist;
13. wrap SQLite into a weaker proprietary KV/collection database abstraction;
14. make all data CRDT-based or mechanically adopt every `automerge-repo` layer merely because Automerge is strong technology.

---

## 23. Strategic success criterion

The decisive question is:

> **Can a third-party developer learn one Baga Ink SDK / Lua Profile, build one `.ikp`, and run it on Kindle and multiple Android E-Paper devices without learning each device's private implementation?**

Mature general-purpose capabilities should continue to reuse mature ecosystems:

```text
relational data → SQLite / lsqlite3
Reader → Baga Reader API backed internally by mature engines such as KOReader
Local-first CRDT → Automerge core preferred when actually needed
```

If a developer still needs separate business-code trees for Kindle, BOOX, iReader, Bigme, and others, Baga has failed to become a true application platform and remains only an aggregation layer.

---

## 24. Long-term direction

Baga Ink aims to become:

> **A lightweight E-Paper Application Platform above existing operating systems.**

It does not require identical hardware, identical OSes, or identical implementation languages.

It requires one essential thing:

> **Third-party applications face the same stable platform and can directly reuse mature general-purpose software ecosystems.**
