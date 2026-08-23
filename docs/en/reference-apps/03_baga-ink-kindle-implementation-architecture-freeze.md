# Baga Ink Kindle Implementation Architecture Freeze

> **Document level:** Kindle Reference Implementation Architecture Freeze  
> **Document ID:** `reference-apps.03`  
> **Locale:** English (`en`)  
> **Status:** **FROZEN BASELINE v1.0.1**  
> **Date:** 2026-08-23  
> **Applies to:** Baga Ink Client, Baga Ink Platform on Kindle, Baga Ink Kindle Adapter, LifeBook (`lifebook.ikp`)  
> **Governing authority:** all current Baga Ink Standards  
> **Reference App:** `docs/en/reference-apps/01_lifebook-reference-app.md`  
> **Counterpart:** `docs/zh-CN/reference-apps/03_Kindle具体实现架构冻结.md`

---

## 0. Status and freeze rule

This document converges Baga Ink Standards, the LifeBook Reference App, Kindle Homebrew ecosystem knowledge, and Kindle architecture decisions made through 2026-08-23 into one baseline that can directly guide code start, dependency selection, packaging, installation, launch, update, rollback, and compatibility testing.

Authority order:

```text
Baga Ink Standards
        >
this Kindle Implementation Architecture Freeze
        >
other Kindle Reference / Product supplemental documents
        >
concrete code and prototypes
```

If this document conflicts with governing Standards, the Standards win and this Freeze must be amended.

After this file enters `FROZEN` status, code MUST NOT silently:

- change the `.ikp` / `.kpkg` responsibility boundary;
- introduce formal `Baga Runtime`, `Baga Platform Runtime`, or `LifeBook Runtime` layers;
- make LifeBook depend directly on KOReader / Kindle private APIs;
- change the role of KPM / MRPI / sh_integration / KUAL / PEKI / KindleTool;
- change Kindle Native Build Target / ABI Profile semantics;
- change the basic responsibility of Platform Core;
- change IKP Package Manager trust/install/update/rollback semantics;
- hard-code a jailbreak exploit as a Platform dependency.

If a real implementation requires such a change, first record an explicit Architecture Decision, update this Freeze, then modify code and tests.

---

## 1. One-page architecture

The final Kindle implementation chain is frozen as:

```text
                         Baga Ink Client
                                │
                                ▼
                  Detect Kindle / Current State
                                │
                                ▼
                  Installation Route Resolver
                    (only when Platform not ready)
                                │
          ┌─────────────────────┴─────────────────────┐
          ▼                                           ▼
   Stock / not homebrew-ready                 Already homebrew-ready
          │                                           │
          ▼                                           │
WinterBreak / SpringBreak / Sanctuary / Véra /       │
legacy / future verified route                        │
          │                                           │
          └─────────────────────┬─────────────────────┘
                                ▼
                         Homebrew Ready
                                │
                                ▼
                        KPM compatible?
                   ┌────────────┴────────────┐
                  YES                        NO
                   │                          │
             KPM installed?                  │
             ┌─────┴─────┐                   │
            YES          NO                  │
             │            │                   │
             │      bootstrap/install KPM     │
             │            │                   │
             └─────┬──────┘                   │
                   ▼                          ▼
        baga-platform*.kpkg        MRPI / legacy/manual envelope
                   │                          │
                   └────────────┬─────────────┘
                                ▼
                    Baga Ink Platform on Kindle
                                │
                    ┌───────────┼───────────┐
                    ▼           ▼           ▼
              Platform Core  Kindle Adapter Adopted Components
                    │                       KOReader/FBInk/etc.
                    ▼
               IKP Package Manager
                    │
                    ▼
                lifebook.ikp
                    │
                    ▼
                   LifeBook
```

The following boundaries are simultaneously frozen:

1. **`.ikp` is never converted into `.kpkg`.**
2. **KPM manages native Baga Platform install/update on Kindle; IKP Package Manager manages Baga Apps.**
3. **“KPM not installed” and “KPM incompatible” are entirely different states.**
4. If KPM is compatible but absent: **install/bootstrap KPM first, then use `.kpkg`**. Do not permanently fall back to MRPI merely because KPM is missing.
5. Use MRPI / legacy/manual Platform installer envelopes only when KPM is genuinely unavailable/incompatible/unvalidated for that device/ABI/Homebrew combination.
6. **LifeBook is a Universal IKP App, not a Kindle Homebrew package.**
7. There is **no formal `Baga Platform Runtime` layer**. Lua/LuaJIT is an embedded/reused execution capability inside Platform Core.
8. **KOReader is an adopted internal Kindle Platform component, not a LifeBook API.**
9. Baga manages a **pinned KOReader/koreader-base component set validated by BICTS**. v1 does not rely on user-managed KOReader.
10. **WinterBreak / SpringBreak / Sanctuary / Véra are Installation Route records, not Platform dependencies.**
11. **Mesquito is not directly adopted by Baga.** If an upstream route uses it internally, it remains a route implementation detail.
12. **KUAL / PEKI are not the normal user path or LifeBook dependencies.** They are allowed only as Compatibility-DB-validated legacy/bootstrap/admin fallbacks.
13. **KindleTool is build/package tooling, not Runtime and not App Manager.**
14. The **user-facing product path** from Kindle Home MUST be **Kindle Home → LifeBook**. The **internal execution chain** is `Kindle Home → LifeBook Home Entry → baga-launch com.lifebook → Baga Ink Platform Core → active lifebook.ikp → main.lua → LifeBook`. Ordinary users must not see KOReader, KUAL, KPM, MRPI, or other Homebrew internals.
15. Phase-one Home/Library entry should prefer mature `sh_integration` Scriptlets. Deeper AppMgr registration is a later replaceable enhancement.

---

## 2. Public architecture and Kindle implementation mapping stay separate

The public Baga architecture remains:

```text
IKP App
   ↓
Baga Ink API / Baga Lua Profile
   ↓
Baga Ink Platform Core
   ↓
Baga Ink Device Adapter
   ↓
OS / Hardware
```

Kindle internals may heavily reuse:

```text
KOReader
koreader-base
LuaJIT
UIManager / widgets
ReaderUI
CREngine
MuPDF
FBInk
SQLite / lsqlite3 / lua-ljsqlite3
Automerge core where appropriate
KPM
Hotfix / sh_integration
MRPI
KindleTool
KUAL / PEKI fallback only
```

Adoption does **not** create new public Baga layers.

Do not reintroduce:

```text
Baga Runtime
Baga Platform Runtime
LifeBook Runtime
Kindle Runtime
KOReader Runtime Layer as public Baga architecture
Provider Framework merely because a library is reused
Engine Layer merely because a library is reused
```

Technically LuaJIT is a Lua execution environment and KOReader has a LuaJIT-driven scripting environment, but in Baga these are Platform implementation details.

---

## 3. Two package managers at two completely different layers

### 3.1 Kindle Homebrew layer: KPM

KPM is a native Kindle Homebrew Package Manager.

Its `.kpkg` package may contain package manifest, version, dependency metadata, and optional shell hooks such as:

```text
install.sh
launch.sh
uninstall.sh
```

Baga uses KPM for:

```text
baga-platform_<version>_<target>.kpkg
```

which may contain target-ABI-specific:

```text
Baga Platform Core native parts
Kindle Adapter native parts
baga-launch launcher component
pinned KOReader/koreader-base components
Lua/LuaJIT
native libraries
Platform install/update/uninstall hooks
Home-entry bootstrap assets
```

`baga-launch` is a small internal launcher component/command, not a separate public “Baga Launcher” product or architecture layer.

KPM MUST NOT become Universal App Contract.

### 3.2 Baga Platform layer: IKP Package Manager

IKP Package Manager is an internal cross-device App Package Manager in Platform Core.

It manages:

```text
lifebook.ikp
rss-reader.ikp
notes.ikp
other Universal IKP Apps
```

It is not a KPM fork or wrapper. It may learn from mature package-manager design but must implement Baga IKP / Signing / Update / Rollback Standards.

### 3.3 Conversion is forbidden

There is never:

```text
lifebook.ikp → lifebook.kpkg
```

and never:

```text
lifebook.ikp → MRPI package / LifeBook.bin
```

Correct layering:

```text
Kindle native infrastructure
baga-platform*.kpkg / *.bin / legacy bundle
        ↓
installs Baga Ink Platform
        ↓
IKP Package Manager
        ↓
lifebook.ikp
```

---

## 4. KPM capability: missing is not incompatible

This is a hard state-machine rule.

### State A: KPM compatible + installed

```text
install/update baga-platform.kpkg
```

Preferred path.

### State B: KPM compatible + NOT installed

Do NOT implement:

```text
No KPM → permanent MRPI fallback
```

Implement:

```text
KPM capable?
    YES
     │
KPM installed?
    NO
     │
bootstrap/install KPM
     │
install baga-platform.kpkg
```

Client may carry verified KPM/bootstrap assets. The trigger depends on current Homebrew foundation, e.g. post-jailbreak foundation, sh_integration, MRPI, or another Compatibility-DB-approved bootstrap channel.

If MRPI is used once to install KPM, MRPI is only the bootstrap transporter. Later Baga Platform lifecycle can return to KPM.

### State C: KPM incompatible / unavailable

Only use a long-term fallback when one of these is true:

- KPM has no native target for the combination;
- device/ABI/Homebrew combination is not supported upstream;
- Baga Compatibility Record says KPM is unreliable there;
- KPM installation cannot satisfy data-protection / rollback / lifecycle requirements.

Then use:

```text
MRPI .bin
legacy/manual bundle
other verified native installer envelope
```

But it installs the **same Baga Platform release/source/API semantics**, not another Platform variant.

### Current KPM-support fact boundary

As of 2026-08-23, upstream KPM 0.2.x artifacts list `kindlepw2` and `kindlehf` as supported platforms, and KPM's installer only handles those native KPM binary directories.

KPM helper/package manifests may contain target names such as:

```text
kindle
kindle5
kindlepw2
kindlehf
```

but “a package manifest can name a target” does **not** prove the KPM program itself runs on that target.

Therefore Baga Client MUST obtain KPM capability from an updateable Compatibility / Installation DB and Baga test evidence, not infer it from manifest target names.

---

## 5. One Platform release, multiple native installer envelopes

Do not create separate product concepts such as:

```text
KPM Baga
MRPI Baga
KUAL Baga
WinterBreak Baga
```

Use:

```text
              Baga Platform Release X
                        │
            ┌───────────┴───────────┐
            ▼                       ▼
     target: kindlepw2        target: kindlehf
            │                       │
     ┌──────┴──────┐         ┌──────┴──────┐
     ▼             ▼         ▼             ▼
   .kpkg          .bin      .kpkg          .bin

legacy targets
→ validated legacy/manual or MRPI-compatible envelope
```

“Same Platform” means:

- same source release;
- same Baga API / Lua Profile contract;
- same Platform Core logic/data formats;
- same IKP semantics;
- native-target differences only in native artifacts/adopted binaries.

Binary bytes do not need to be identical across targets.

---

## 6. Kindle Native Build Targets / ABI Profiles

Do not call them “Runtime Build Targets.” Formal name:

> **Kindle Native Build Target / ABI Profile**

Reference mapping:

| Kindle engineering family | Reference target | Purpose |
|---|---|---|
| K2 / K3 / DXG and legacy | `kindle-legacy` | old ABI / low-resource legacy build |
| K4 / Touch / PW1 classic | `kindle` | classic build / legacy install path |
| PW2+ soft-float path | `kindlepw2` | PW2+ soft-float native build |
| hard-float path | `kindlehf` | hard-float native build |

The Kindle Adapter Standard treats firmware `5.16.3` as an important reference engineering boundary between soft-float/hard-float paths. This is a native build/compatibility boundary, not LifeBook IKP Contract.

Every native component—Platform native code, KOReader/koreader-base, FBInk, SQLite native library/binding, Automerge native bridge if adopted, KPM/launcher—must be built/pinned/tested for the target ABI and recorded in Compatibility + BICTS evidence.

`lifebook.ikp` does not fork by target.

---

## 7. Baga Ink Platform Core stays small

Platform Core MUST NOT expand into a heavyweight Runtime Framework.

Frozen responsibility groups:

```text
Baga Ink Platform Core
│
├─ 1. IKP Package Management
│   ├─ package validation
│   ├─ stage / activate
│   ├─ update / rollback
│   └─ uninstall
│
├─ 2. App Registry
│   ├─ installed apps
│   ├─ active release
│   └─ package/data state
│
├─ 3. App Lifecycle
│   ├─ start / resume / pause
│   ├─ sleep / wake
│   └─ stop / update / uninstall
│
├─ 4. Embedded Lua Host
│   ├─ Baga Lua Profile
│   └─ load validated entry main.lua
│
├─ 5. Permission / Sandbox / Capability
│   ├─ permission enforcement
│   ├─ app-private paths
│   └─ capability view
│
└─ 6. Baga API Dispatch
    └─ baga.* → Device Adapter / adopted implementation
```

Platform Core does NOT contain LifeBook account/business logic, Articles/Q&A/Comments, Life Records/Time Capsule, LifeBook AI, LifeBook cloud product policy, Baga Ink Client, or Baga Ink Market.

Nor does adoption of KOReader, MuPDF, CREngine, SQLite, Automerge, or FBInk create a same-named public architecture layer.

---

## 8. IKP Package Manager implementation freeze

IKP Package Manager is a Platform Core component, not a user-facing product and not necessarily a background daemon.

### 8.1 What to learn from KPM

May borrow:

```text
package identity
manifest
version/release state
installed-package registry
stage/install/update/uninstall lifecycle
simple repository/package separation
```

### 8.2 What MUST NOT be copied from KPM

IKP cannot expose arbitrary:

```text
install.sh
launch.sh
uninstall.sh
raw shell hook
```

Universal IKP executes only validated App code constrained by Baga Lua Profile and Permission/Sandbox.

### 8.3 v1 responsibilities

```text
IKP Package Manager
├─ Container Reader
├─ Manifest Validator
│   ├─ app id / version / release_sequence
│   ├─ entry
│   ├─ Baga API range
│   ├─ permissions
│   └─ required/optional capabilities
├─ Security Validator
│   ├─ canonical path / Zip Slip protection
│   ├─ decompression limits
│   ├─ payload hash
│   ├─ publisher/signing chain
│   └─ revocation / identity continuity
├─ Compatibility Check
├─ Staging / Atomic Activation
├─ Rollback / Last-known-good
├─ Uninstall
└─ App Registry
```

Explicitly NOT in v1:

```text
APT-style dependency solver
cross-App shared native dependency resolver
arbitrary install-script system
background package daemon
App-to-App private-directory dependency
```

### 8.4 Mature library reuse

IKP Package Manager does not reimplement ZIP, JSON, SHA-256, signing algorithms, or SQLite. Use mature license-compatible pinned implementations and test them against governing Standards.

App Registry MAY use Platform-managed SQLite as an implementation choice; that does not change IKP Contract.

### 8.5 Recommended directory semantics

```text
/mnt/us/baga/
├─ bin/
├─ platform/
├─ apps/
│  └─ <app-id>/
│     ├─ releases/
│     │  └─ <release-sequence>/
│     ├─ active.json / equivalent registry state
│     └─ data/
├─ staging/
├─ inbox/
├─ outbox/
└─ device.json
```

Physical paths MAY change for safety/filesystem reasons, but these semantics do not:

- package and App-private data are separate;
- release directories are immutable or equivalently protected;
- activation is atomic or crash-consistent;
- rollback does not delete user data;
- staging does not automatically become active.

---

## 9. LifeBook IKP normal execution chain

Canonical package:

```text
lifebook.ikp
```

Contains:

```text
manifest.json
main.lua
src/
assets/
locales/
signature/
```

Does NOT contain:

```text
Kindle native executable
Kindle shell bridge
KPM package
MRPI package
KOReader binary/runtime copy
Device Adapter
Platform Core
```

User-facing path:

```text
Kindle Home
    ↓
LifeBook
```

Internal execution chain:

```text
Kindle Home
    ↓
LifeBook Home Entry
    ↓
/mnt/us/baga/bin/baga-launch com.lifebook
    ↓
Platform Core
    ├─ read App Registry
    ├─ verify active release state
    ├─ create App Context
    ├─ apply Permission / Sandbox / Capability view
    └─ initialize Baga Lua Profile
    ↓
active lifebook.ikp / validated main.lua
    ↓
LifeBook
```

KPM is **not** in the normal App-launch hot path.

---

## 10. KOReader: reuse heavily, remain invisible to LifeBook

### 10.1 Frozen adoption strategy

Kindle Reference Platform SHOULD maximize reuse of:

```text
KOReader / koreader-base
LuaJIT
UIManager / widgets
ReaderUI
CREngine
MuPDF
Annotation / Highlight / Bookmark
position / search / selection
Kindle device/input/display knowledge
FBInk where appropriate
```

LifeBook IKP MUST NOT contain direct imports such as:

```lua
require("ui/uimanager")
require("apps/reader/readerui")
```

or depend on KOReader private sidecars/internal objects as Universal Contract.

Correct path:

```text
LifeBook
  ├─ baga.ui
  ├─ baga.reader
  ├─ baga.display
  └─ baga.input
       ↓
Baga Kindle implementation
       ↓
KOReader / koreader-base / FBInk internals
```

### 10.2 Pinned private copy

v1 Baga manages its own pinned KOReader/koreader-base component set.

Do not depend by default on:

```text
/mnt/us/koreader/
user nightly
userpatch
third-party plugin
user-upgraded KOReader ABI/API
```

Recommended internal names:

```text
platform/components/koreader/
platform/vendor/koreader/
```

Avoid `runtime/koreader`, which would recreate the Baga Runtime concept.

Only a future exact commit/version/ABI/patch-set match validated by Baga may share a user KOReader installation; v1 does not optimize for this.

### 10.3 `baga.koplugin`

A Platform-private `.koplugin` is an allowed lightweight PoC:

```text
baga-launch
  ↓
pinned KOReader substrate
  ↓
Platform-private baga.koplugin
  ↓
Baga root UI / reader integration
```

It is an **implementation technique, not public architecture and not IKP API**.

If direct internal-module invocation proves more stable, it may replace the plugin technique without changing LifeBook or Baga API.

---

## 11. Kindle Home Entry: sh_integration first, deeper AppMgr later

Long-term product experience:

```text
Kindle Home
   ↓ one action
LifeBook
```

Ordinary users MUST NOT need to go through:

```text
KUAL
KOReader File Manager
KOReader Plugin Menu
KPM CLI
```

### Phase 1: sh_integration Scriptlet

Prefer mature `sh_integration`:

```text
/documents/LifeBook.sh
    ↓
/mnt/us/baga/bin/baga-launch com.lifebook
```

Do not hand-edit `appreg.db` / `cc.db` as the v1 default while mature sh_integration mechanisms exist.

### Phase 2: more native AppMgr entry

If product UX justifies it, later reuse/validate sh_integration's AppMgr-registration mechanisms for a more native Kindle application entry.

The contract remains:

```text
Home entry → baga-launch <app-id>
```

LifeBook itself does not gain AppMgr private dependencies.

---

## 12. Homebrew Foundation: reuse rather than recreate

Baga does not create a new:

```text
Baga Kindle Homebrew Foundation
```

It detects/reuses a validated existing foundation consisting as applicable of:

```text
Hotfix
sh_integration
KPM when target-compatible
MRPI when needed
```

Baga Client detects foundation state; LifeBook IKP is unaware of it.

Homebrew foundation is a Kindle implementation prerequisite, not Baga App Contract.

---

## 13. Final roles: KPM / MRPI / KindleTool / KUAL / PEKI

| Project | Frozen role | Normal LifeBook launch dependency? |
|---|---|---|
| **KPM** | Preferred Baga Platform native install/update manager on KPM-compatible Kindles | No |
| **MRPI** | Non-KPM/legacy Platform installer fallback; may be a bootstrap transporter | No |
| **KindleTool** | CI/build/package tooling for Kindle OTA/MRPI `.bin` etc. | No |
| **sh_integration** | Preferred phase-one Home/Library Scriptlet integration; may provide bootstrap execution point | Indirect Kindle integration, invisible to LifeBook API |
| **Hotfix** | Upstream persistence/foundation component detected by Client | No |
| **KUAL** | Legacy/fallback admin/launcher/bootstrap tool; not modern product entry | No |
| **PEKI** | KUAL/bootstrap compatibility tool only where route DB allows | No |

Forbidden statements/architectures:

```text
LifeBook depends on KUAL
LifeBook package = KPM package
KPM not installed → permanent MRPI path
KindleTool Runtime
MRPI App Manager for IKP
```

---

## 14. WinterBreak / SpringBreak / Sanctuary / Véra: Installation Routes only

These projects are not Platform Core, device-facing Baga API, LifeBook IKP dependencies, or Baga Runtime.

They answer only:

> **How does an exact Kindle model + firmware + current state become homebrew-ready?**

Frozen model:

```text
Baga Installation Route DB
├─ WinterBreak
├─ SpringBreak
├─ Sanctuary
├─ Véra
├─ legacy routes
└─ future routes
```

Each route record includes at least:

```text
route_id
upstream source/version
supported model(s)
exact firmware/range
current-state prerequisites
registration requirement
Wi-Fi requirement
PC/USB requirement
free-space / device-state requirement
known risks
Baga tested status
last verified date
preferred/fallback priority
```

Resolver ordering:

1. do not jailbreak again if already homebrew-ready;
2. exact model + firmware match;
3. prefer higher-success/lower-recovery-risk Baga-validated route;
4. then consider prerequisites/step complexity;
5. new upstream route starts Experimental before promotion to Preferred;
6. unknown firmware defaults Experimental / Unsupported, never “same family should be close enough.”

Jailbreak support ranges live in updateable Route DB, not Platform Core.

### Mesquito

Mesquito is not directly adopted by Baga.

If an upstream route internally uses it:

```text
WinterBreak = Baga-selectable Installation Route
Mesquito    = upstream route implementation detail
```

Baga validates route preconditions, resulting state, and safety boundary.

---

## 15. Baga Ink Client full state machine

The user action may still be:

```text
Install LifeBook
```

Internally Client executes two independent transactions:

```text
A. Ensure Baga Platform
B. Transfer/Install LifeBook IKP
```

### 15.1 Ensure Platform

```text
Detect device
   ↓
Platform present and healthy?
   ├─ YES → skip bootstrap
   └─ NO
       ↓
Homebrew ready?
   ├─ NO → Installation Route Resolver
   └─ YES
       ↓
KPM compatible?
   ├─ YES
   │    ↓
   │  KPM installed?
   │    ├─ YES
   │    └─ NO → bootstrap KPM
   │             ↓
   │       install baga-platform.kpkg
   │
   └─ NO → MRPI / legacy verified installer envelope
       ↓
Verify Platform health / version / Adapter / BICTS compatibility
```

### 15.2 Transfer LifeBook

```text
Client selects compatible lifebook.ikp
       ↓
Client verifies/caches metadata as allowed
       ↓
transfer signed evidence + .ikp
       ↓
Device Platform verifies again
       ↓
IKP stage
       ↓
atomic activation
       ↓
create/update Home Entry
```

Platform install and App install are recorded/diagnosed independently.

---

## 16. USB Mass Storage: file mailbox / handshake

When a PC sees ordinary Kindle USB Mass Storage, it can reliably read/write files; it cannot assume remote command execution.

Therefore Kindle Reference Implementation SHOULD use a simple file mailbox as the Kindle profile of Standard 26:

```text
/mnt/us/baga/
├─ device.json
├─ inbox/
│  └─ <transfer-id>/
│     ├─ transfer-manifest.json
│     ├─ repository-evidence/...
│     └─ lifebook.ikp
└─ outbox/
   └─ <result-id>.json
```

`device.json` may expose necessary non-sensitive facts such as transfer-protocol version, Platform version, Baga API/Lua Profile version, Kindle native target/ABI profile, firmware Compatibility Record ID, Capability digest, installed-inventory digest, and free storage.

Do not expose account data, book content, or note content by default.

### 16.1 No mandatory daemon

v1 does not need a persistent daemon solely for USB mailbox processing.

Inbox processing may be triggered by Platform startup, LifeBook/Home Entry startup, an explicit Baga Setup/Install Scriptlet, or an existing safe lifecycle hook.

If a daemon is introduced later, first prove its power/sleep/resource/recovery value.

---

## 17. Bootstrap execution point: PC cannot magically execute Kindle commands

Copying files to a Kindle without Platform installed does not mean installation has executed.

A device-side execution point is required, such as:

```text
existing sh_integration Scriptlet
existing MRPI
verified post-jailbreak hook/foundation
other route-specific launcher
```

One recommended modern flow:

```text
Client writes local bootstrap/KPM repo/assets
        ↓
Baga Setup.sh appears in Kindle Library
        ↓ user one-time action
sh_integration executes Setup
        ↓
ensure KPM
        ↓
install baga-platform.kpkg
        ↓
remove/hide one-time Setup entry
```

Concrete bootstrap mechanism is selected by Compatibility / Installation DB and does not become Universal Baga Contract.

---

## 18. Update, rollback, and data protection

### 18.1 Platform update

```text
KPM / MRPI / native installer envelope
→ updates native Baga Platform components
```

Must protect:

```text
Kindle user books
Kindle user notes
Baga App private data
LifeBook SQLite DB
LifeBook local notes / records
last-known-good Platform/App state
```

### 18.2 IKP App update

```text
IKP Package Manager
→ verify
→ stage immutable release
→ migration compatibility check
→ atomic activation
→ probation/health check
→ rollback if needed
```

KPM/MRPI overwrite semantics do not replace IKP Update Protocol.

### 18.3 App package and data always separate

```text
apps/<id>/releases/*
        ≠
apps/<id>/data/
```

Rolling back an App package does not automatically roll back user data. Data-schema changes follow IKP migration/snapshot rules.

---

## 19. Compatibility / BICTS: exact combinations only

“Supports this Kindle generation” is not a formal Compatibility Claim.

A publishable record binds at least:

```text
Device Model / family
+ exact Firmware / tested range
+ Homebrew foundation state
+ Native Build Target / ABI Profile
+ Baga Platform version
+ Kindle Adapter version
+ Baga Lua Profile version
+ adopted component versions/commits
+ BICTS version/result
```

States:

```text
Compatible
Experimental
Unsupported
```

Firmware upgrades require regression of at least bootstrap/install, Platform launch, IKP install/update/rollback, lifecycle/sleep/wake, UI/display/input, storage/sandbox/SQLite, Reader/Library/Anchor when declared, network, Home Entry, and recovery/data protection.

---

## 20. Adopted-module matrix

| Module / project | Frozen conclusion | Location |
|---|---|---|
| Baga Ink Platform Core | **Adopt, self-build minimal Core** | Platform |
| IKP Package Manager | **Adopt/implement Standards; learn from KPM but do not fork KPM contract** | Platform Core |
| Lua / LuaJIT | **Adopt/reuse** | Embedded Lua Host implementation |
| KOReader | **Heavy adoption, pinned private** | Kindle Platform internal |
| koreader-base | **Heavy adoption** | Kindle Platform internal |
| KOReader Plugin mechanism | **MAY for internal PoC/integration** | Platform internal only |
| UIManager / widgets | **SHOULD reuse** | `baga.ui` Kindle implementation |
| ReaderUI / CREngine / MuPDF | **SHOULD reuse** | `baga.reader` Kindle implementation |
| FBInk | **SHOULD/MAY reuse according to mapped need** | display/internal |
| KPM | **Preferred Platform installer/update manager on KPM-compatible target** | Homebrew/native install |
| sh_integration | **Preferred phase-one Home Entry / bootstrap trigger** | Kindle integration |
| AppMgr deeper integration | **MAY in Phase 2** | Kindle integration |
| Hotfix | **Reuse upstream foundation; Client detects it** | Homebrew foundation |
| MRPI | **legacy/KPM-incompatible fallback; possible bootstrap transporter** | native install/bootstrap |
| KindleTool | **Adopt** | CI/build/package tooling |
| KUAL | **fallback/admin only** | legacy compatibility |
| PEKI | **fallback/bootstrap only** | legacy compatibility |
| WinterBreak | **route record only** | Client Installation Route DB |
| SpringBreak | **route record only** | Client Installation Route DB |
| Sanctuary | **route record only** | Client Installation Route DB |
| Véra | **route record only** | Client Installation Route DB |
| Mesquito | **not directly adopted** | upstream route implementation detail |
| SQLite / lsqlite3 | **adopt per Standard** | Standard Library / Platform |
| Automerge core | **adopt per Standard where business needs it** | Adopted Foundation |
| user-managed KOReader | **v1 does not depend on it** | outside Baga contract |
| `Baga Platform Runtime` | **forbidden as formal layer/term** | N/A |

---

## 21. Explicit MUST NOT list

Future implementation and AI-generated code MUST NOT:

```text
MUST NOT convert .ikp to .kpkg.
MUST NOT publish LifeBook canonical app as .kpkg.
MUST NOT use KPM as IKP App Package Manager.
MUST NOT create a formal Baga Platform Runtime layer.
MUST NOT require LifeBook to import KOReader private Lua APIs.
MUST NOT require a user-managed KOReader installation in v1.
MUST NOT expose KUAL/PEKI as the normal LifeBook product path.
MUST NOT equate "KPM not installed" with "KPM unsupported".
MUST NOT hardcode jailbreak exploit code into Platform Core.
MUST NOT make WinterBreak/SpringBreak/Sanctuary/Véra Platform dependencies.
MUST NOT directly adopt Mesquito as a Baga module solely because a route uses it.
MUST NOT hand-edit appreg.db/cc.db as the v1 default while mature sh_integration mechanisms exist.
MUST NOT let MRPI/KPM overwrite semantics replace IKP staged update/rollback.
MUST NOT let Kindle model/firmware branches leak into lifebook.ikp business code.
MUST NOT create another Reader engine when KOReader/CREngine/MuPDF already satisfy the mapped need.
```

---

## 22. First implementation order

### Phase 0 — Compatibility / Bootstrap PoC

Prove substrate before writing large LifeBook product logic:

1. Kindle detector + Route DB schema;
2. representative `kindlepw2` and `kindlehf` devices;
3. Homebrew-ready → KPM capability → Platform `.kpkg` install;
4. KPM-compatible but missing KPM bootstrap;
5. at least one non-KPM/legacy installer envelope;
6. sh_integration Home Entry;
7. internal chain `Kindle Home → LifeBook Home Entry → baga-launch <app-id>`, with user-visible path still only `Kindle Home → LifeBook`.

### Phase 1 — Minimum Platform Core

```text
App Registry
IKP package reader/validator
staging / activation / rollback
Embedded Lua Host
minimal baga.app / storage / device / log
Permission/Sandbox skeleton
Kindle Adapter skeleton
filesystem mailbox
```

### Phase 2 — KOReader mapping

```text
pinned KOReader/koreader-base
baga.ui → UIManager/widgets
baga.input → KOReader Kindle input
baga.display → KOReader/FBInk
baga.reader → ReaderUI/CREngine/MuPDF
```

Validate whether Platform-private `.koplugin` is the lightest integration technique; it is not a mandatory architecture choice.

### Phase 3 — LifeBook skeleton IKP

Only:

```text
lifebook.ikp
main.lua
home/navigation
SQLite/offline start
Library/Reader basic
notes basic
```

Confirm the same IKP Contract has no Kindle-private imports.

### Phase 4 — multi-device/firmware expansion

Add exact combinations through Compatibility DB, not by copying LifeBook code branches.

---

## 23. PoC / not-frozen implementation details

The following may be experimented with without changing the frozen boundaries above:

- primary Platform Core implementation language (Rust/C/C++/Lua mix);
- exact IKP App Registry SQLite schema;
- concrete ZIP/JSON/crypto libraries provided Standards/license are met;
- whether `baga.koplugin` remains;
- whether AppMgr Phase 2 is worthwhile;
- exact mailbox filenames/transaction-journal format;
- concrete Automerge C/Rust/Lua bridge on Kindle;
- final legacy `.bin`/manual envelope for each model;
- exact support range and preferred ranking of each jailbreak route.

These are decided by PoC, real Kindles, and BICTS—not by speculation hardened into Platform Contract.

---

## 24. Relationship to other Reference documents

### LifeBook Reference App

Remains the high-level Universal App implementation specification. This Freeze supplies Kindle bootstrap, dual package-manager, Home Entry, native installer envelope, and route-resolver details absent there.

### LifeBook Kindle Product Behavior / Accessory Design

Continues to own low-refresh, low-power, networking, Audio/Bluetooth, accessory/dock product behavior and experiments. It does not override this Kindle install/bootstrap/Platform/IKP freeze.

### Superseded LifeBook Architecture / Kindle Compatibility document

Its valid content is absorbed here. If retained, it is only a compatibility/history entry and not a competing Kindle implementation baseline.

---

## 25. Upstream basis and continuous validation

This Freeze locks **Baga's responsibility boundaries and adoption strategy**, not upstream versions forever.

Main upstream references include KPM, KindleModding repository manifests, sh_integration, KindleModding jailbreak docs/Wizard, KindleTool, KOReader, and koreader-base.

Every Baga Platform Release records:

```text
upstream project
version / commit
source digest
license
native target
Baga patches if any
BICTS result
```

Jailbreak Route DB, KPM capability, and firmware ranges remain independently updateable without changing Universal App Contract.

---

## 26. Final frozen statement

From this document onward, Baga Ink on Kindle is understood as:

> **Baga Ink Client first brings an exact Kindle into a verified Homebrew/Platform-ready state; KPM-compatible devices preferably use KPM to manage the native Baga Platform package, while KPM-incompatible devices use an MRPI/legacy installer envelope; inside Platform Core, a minimal Core + IKP Package Manager + Embedded Lua Host + Kindle Adapter runs Universal IKPs; KOReader/koreader-base are heavily, privately, and version-pinned as the Kindle implementation substrate; LifeBook always remains only `lifebook.ikp`, targets Baga Ink API / Baga Lua Profile, launches from Kindle Home in one user action, and never needs to know jailbreaks, KPM, MRPI, KUAL, KOReader private APIs, or device ABI.**

This is the default baseline for subsequent Kindle code, module adoption, and compatibility implementation.
