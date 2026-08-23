# Baga Ink Kindle Device Adapter

> **Document level:** Reference Device-Family Adapter Standard  
> **Document ID:** `standards.11`  
> **Locale:** English (`en`)  
> **Status:** Draft v0.6  
> **Date:** 2026-08-23  
> **Parent Contract:** Standard 07 — Baga Ink Device Adapter Contract  
> **Certification:** Standards 08 / 10  
> **Standard Libraries:** Standard 13  
> **Kindle implementation freeze:** localized Reference App 03 when current  
> **Counterpart:** `docs/zh-CN/standards/11_Kindle适配规范.md`

---

## 0. Purpose

This document defines how the Kindle device family implements the Baga Device Adapter Contract.

Core rule:

> **The Baga Kindle Device Adapter does not rewrite Kindle. It reuses mature capability from KOReader, koreader-base, FBInk, Kindle OS, and validated Homebrew mechanisms, then normalizes device / firmware / system differences into the Baga Device Adapter Contract.**

Therefore the Kindle Adapter SHOULD remain thin.

New Baga-specific code SHOULD concentrate on:

```text
Baga interface glue
Capability normalization
Device detection / profile selection
Quirk selection and correction
Error / event normalization
Self-test / diagnostics
Contract Tests
```

It SHOULD NOT begin by reimplementing:

```text
framebuffer stack
input stack
reader engine
E-Ink refresh algorithms
network stack
power manager
```

If a mature verified mechanism already exists, the Adapter should wrap/call it rather than duplicate it.

---

## 1. Authority boundary

Three document classes must remain distinct:

```text
Standard 07 — Device Adapter Contract
→ what every device port must provide

Standard 11 — Kindle Device Adapter
→ how Kindle implements Standard 07

Kindle Implementation Architecture Freeze
→ Client/bootstrap/KPM/MRPI/Platform/IKP/Home Entry and other Kindle-wide implementation decisions
```

Therefore:

- Standard 07 is the highest authority for the Device Adapter Contract;
- this Standard is the Kindle-family implementation mapping;
- the Kindle implementation freeze does not redefine the Adapter Contract and instead governs the wider Kindle implementation architecture.

---

## 2. Reference Kindle Adapter structure

Recommended internal organization:

```text
Baga Kindle Device Adapter
│
├── common/
│   ├── identity
│   ├── capability_detection
│   ├── error_mapping
│   ├── event_normalization
│   └── self_test
│
├── display/
│   ├── KOReader Kindle display knowledge
│   └── FBInk / verified Kindle mechanisms
│
├── input/
│   └── KOReader Kindle input knowledge
│
├── storage/
│   ├── Kindle filesystem
│   └── sandbox enforcement hooks
│
├── lifecycle/
│   └── Kindle / KOReader / Homebrew events
│
├── power/
│   └── Kindle validated mechanisms
│
├── network/
│   └── Kindle connectivity bridge
│
├── light/
│   └── frontlight backend
│
├── library/
│   └── Kindle user-library bridge
│
├── device_profiles/
│   ├── model + firmware records
│   └── capability expectations / backend choices
│
├── quirks/
│   └── model + firmware corrections
│
└── build_targets/
    ├── kindle-legacy
    ├── kindle
    ├── kindlepw2
    └── kindlehf
```

This is an internal Reference implementation organization, not a Universal App API.

---

## 3. Boundary between Kindle Adapter and mature components

### 3.1 Mature capability that may implement Device Adapter subsystems

```text
KOReader / koreader-base Kindle device knowledge
FBInk
Kindle OS interfaces
validated Homebrew mechanisms
```

These may provide implementation sources for:

```text
Display
Input
Lifecycle
Power
Frontlight
some network/device detection
```

### 3.2 Kindle components that are not Device Adapter root subsystems

#### KOReader Reader/UI shared implementation

```text
ReaderUI / CREngine / MuPDF
UIManager / widgets
```

These may implement Baga Platform Reader/UI behavior, but Reader/UI themselves are **not** top-level Device Adapter subsystems.

Correct relationships:

```text
baga.ui
  ↓
Baga UI implementation
  ↓
KOReader UIManager/widgets
  ↓
Kindle Adapter: Display/Input
```

```text
baga.reader
  ↓
Baga Reader implementation
  ↓
KOReader ReaderUI/CREngine/MuPDF
  ↓
Kindle Adapter: Display/Input/Storage/Lifecycle
```

#### KPM / MRPI / sh_integration / Hotfix

These primarily belong to:

```text
native Platform install/update
Homebrew foundation
Home Entry / bootstrap
```

They are not Display/Input/Power Device Adapter subsystems.

#### KindleTool

Belongs to:

```text
CI / build / package tooling
```

#### WinterBreak / SpringBreak / Sanctuary / Véra

Belong to:

```text
Baga Ink Client Installation Route DB
```

They are not Adapter implementations.

#### Mesquito

Baga does not directly adopt Mesquito as a Kindle Adapter dependency. If an upstream jailbreak route internally uses it, that is an upstream implementation detail.

---

## 4. Kindle Adapter Factory

Kindle Platform SHOULD provide:

```text
KindleAdapterFactory
├── probe(BootstrapDeviceInfo)
└── create(...)
```

`probe()` does not choose a jailbreak route. It identifies device facts after Baga Platform can already execute, such as:

```text
Kindle family/model
firmware version
CPU / ABI/native target hints
screen identity
available input class
known Device Profile
```

Installation Route Resolver belongs to Baga Ink Client, not `KindleAdapterFactory.probe()`.

Factory MUST:

- handle unknown model/firmware conservatively;
- not replace validation with "same family should be close enough" assumptions;
- select the matching Device Profile;
- select necessary Quirk Sets;
- produce a diagnosable `ProbeResult`.

---

## 5. Kindle DeviceDescriptor

Minimum logical descriptor:

```text
adapter_contract_version
adapter_id = org.baga.adapter.kindle
adapter_version

device_family = kindle
manufacturer = Amazon
model
model_id
firmware_version

cpu_arch
native_target

screen
input_summary
profile_id
quirk_set_id
compatibility_record_id
```

Kindle serial number and Amazon account identity are not exposed to Apps or ordinary Client handshakes by default.

---

## 6. Native Build Target, Device Profile, and Quirk must stay separate

### 6.1 Native Build Target / ABI Profile

Answers:

> **How is native code built?**

Reference engineering mapping:

| Kindle engineering family | Native target | Meaning |
|---|---|---|
| K2 / K3 / DXG and similar legacy | `kindle-legacy` | old ABI / low-resource legacy |
| K4 / Touch / PW1 and similar classic | `kindle` | classic environment |
| PW2+ soft-float path | `kindlepw2` | PW2+ soft-float native build |
| hard-float path | `kindlehf` | hard-float native build |

The current Reference baseline continues to treat firmware `5.16.3` as an important soft-float / hard-float engineering boundary; final compatibility must still be confirmed by build/test evidence.

### 6.2 Device Profile

Answers:

> **What is known about a specific model + firmware combination?**

Recommended profile data:

```text
profile_id
model / model_id match
firmware range
native_target
screen expectations
input expectations
baseline capability expectations
preferred display backend
preferred input backend
frontlight/audio/bluetooth expectations
validation status
last verified date
```

A Profile belongs to the Adapter. It is not a LifeBook branch.

### 6.3 Quirk Set

Answers:

> **What corrections does this exact combination need?**

Typical examples:

```text
touch coordinate correction
refresh workaround
frontlight behavior
sleep event workaround
network workaround
library bridge difference
```

A Quirk MUST include a match range and test evidence and remain inside the Adapter.

---

## 7. Capability detection

Kindle Adapter MUST build `CapabilitySnapshot` from real device/backend evidence.

Base:

```text
display.basic
input.navigation
storage.app_sandbox
power.sleep_wake
platform.lifecycle
```

Optional examples:

```text
display.partial_refresh
display.fast_refresh
display.quality_refresh
display.grayscale
display.color
input.touch
input.physical_page_key
input.keyboard
input.pen*
network.available
network.wifi
network.http
network.https
light.frontlight*
audio.output
bluetooth.*
storage.user_library
```

Evidence priority:

```text
runtime probe / verified backend
        >
verified Device Profile
        >
marketing/spec assumptions
```

Marketing specs or inference from another device in the family cannot alone support a Stable Capability claim.

---

## 8. DisplayAdapter: prefer KOReader / FBInk

Kindle `DisplayAdapter` MUST implement Standard 07.

Logical chain:

```text
Platform refresh request
        ↓
Kindle DisplayAdapter
        ↓
KOReader / FBInk / verified Kindle mechanism
        ↓
Kindle display
```

Apps/UI express only semantic intents:

```text
AUTO
TEXT
QUALITY
FAST
ANIMATION
```

The Adapter maps those to the actual safe Kindle waveform/refresh mechanisms.

Do not expose:

```text
DU
GC16
A2
REGAL
raw waveform id
```

as the Baga App contract.

The DisplayAdapter SHOULD reuse KOReader's mature Kindle knowledge for:

```text
device detection
screen geometry
orientation
refresh behavior
```

FBInk MAY supplement or provide a more stable framebuffer/refresh mechanism where a concrete target/profile proves it useful.

The Kindle Adapter should not create another framebuffer framework merely to satisfy the Baga contract.

---

## 9. InputAdapter: prefer KOReader Kindle input knowledge

Logical chain:

```text
Kindle raw touch/key/input
        ↓
KOReader / verified Kindle input knowledge
        ↓
Kindle InputAdapter
        ↓
Baga NavigationAction / PointerEvent / PenEvent
        ↓
Platform Core
```

Normalize at least:

```text
confirm
back
page_next
page_previous
focus_next
focus_previous
```

Map `menu` when the system/device offers a reliable semantic equivalent; otherwise upper-layer UI supplies an equivalent entry point.

Touch, D-pad, keyboard, physical page keys, and Pen remain implementation details below the Baga semantic model. IKP does not receive raw keycodes/event objects.

---

## 10. StorageAdapter: Kindle filesystem + Baga sandbox

Kindle lacks a modern Android-style per-App OS sandbox.

Therefore Kindle Adapter / Platform together MUST provide:

```text
platform private root
app private root
path containment
canonical path checking
symlink escape defense
disk-full / IO error mapping
package/data separation
```

Recommended logical layout:

```text
/mnt/us/baga/
├── platform/
├── apps/
│   └── <app-id>/
│      ├── releases/
│      └── data/
├── staging/
└── ...
```

Exact paths may evolve, but semantics must satisfy IKP Update/Rollback requirements.

SQLite `lsqlite3` must still use sandbox-aware VFS or equivalent I/O confinement for ATTACH, journal, WAL, SHM, temp DB, and related escape paths. StorageAdapter does not invent another database API.

---

## 11. LifecycleAdapter

Prefer verified Kindle OS, KOReader, and Homebrew event mechanisms.

The goal is to obtain stable:

```text
sleep
wake
```

signals and support Platform lifecycle:

```text
start
resume
pause
sleep
wake
stop
```

Requirements:

- do not use App-level high-frequency polling;
- Adapter callback enters Platform Core first;
- after wake, Platform may re-check network/power/device state;
- firmware-specific event workarounds belong in Quirk Set.

---

## 12. PowerAdapter

Kindle PowerAdapter SHOULD wrap proven Kindle / KOReader / Homebrew mechanisms.

Base requirement:

```text
power.sleep_wake
```

Declare only actually implemented optional behavior:

```text
power.battery_level
power.charging_state
power.keep_awake
```

`keep_awake` may always be refused by Platform policy.

Do not implement a new independent power daemon unless real PoC evidence proves existing mechanisms cannot satisfy the Contract.

---

## 13. NetworkAdapter

Its primary responsibility is:

```text
connectivity state
sleep/wake disruption mapping
network-change events
necessary Kindle network bridge
```

Baga does not require the Kindle Adapter to reimplement HTTP/TLS.

A valid design may use:

```text
Platform-shared HTTP/TLS stack
+
Kindle network/connectivity bridge
```

provided public `baga.network` semantics and BICTS hold.

LifeBook sync policy and Automerge sync protocol do not belong in `NetworkAdapter`.

---

## 14. Light / Audio / Bluetooth

### Frontlight

When stable control exists through mature Kindle mechanisms, the Adapter may expose:

```text
light.frontlight
light.frontlight.temperature
```

only after testing.

### Audio / Bluetooth

Capabilities vary significantly across Kindle generations.

Declare only after actual implementation + Contract Tests / BICTS, for example:

```text
audio.output
audio.microphone
bluetooth.available
bluetooth.input_device
bluetooth.audio
```

Do not infer support merely because "newer Kindles usually have it."

---

## 15. UserLibraryBridge

Kindle user books are exposed through:

```text
Kindle filesystem / library knowledge
        ↓
Kindle UserLibraryBridge
        ↓
Platform baga.library
        ↓
IKP
```

Rules:

- IKP does not scan `/documents` directly;
- IKP does not read Kindle-private database paths directly;
- Library items use opaque IDs / handles;
- `library.read/write` Permission applies;
- source handles may be passed to `baga.reader`;
- Library Bridge is not the Reader engine.

If Kindle private-library database compatibility is too risky in the first phase, Baga may begin with conservative validated file sources and add deeper integration later. User-data safety outranks superficial feature completeness.

---

## 16. UI / Reader: reuse KOReader, but do not put them in the Adapter root

Kindle Platform SHOULD maximize reuse of:

```text
UIManager / widgets
ReaderUI
CREngine
MuPDF
Annotation / Highlight / Bookmark
position / search / selection / anchor
```

Correct layering:

```text
Platform UI / Reader implementation
        ↓ uses
Kindle Device Adapter
```

not:

```text
Kindle Device Adapter
└── entire UI / Reader framework
```

LifeBook IKP must never directly do things such as:

```lua
require("ui/uimanager")
require("apps/reader/readerui")
```

KOReader private APIs stay inside the Kindle Platform implementation.

---

## 17. Pinned KOReader / koreader-base

The first Reference Kindle Platform MUST manage its own pinned component set.

Do not depend on:

```text
user /mnt/us/koreader/
nightly builds
userpatch
third-party plugins
private APIs from a user-upgraded KOReader
```

Every Platform Release MUST record:

```text
KOReader version/commit
koreader-base version/commit
FBInk version/commit when used
patch set
license
source digest
native target
BICTS / Contract Test result
```

The Adapter invokes mature capabilities; KOReader does not become a Baga standard dependency/API.

---

## 18. Final boundary for Homebrew / install components

| Component | Kindle role | Device Adapter? |
|---|---|---:|
| KOReader device knowledge | Display/Input/device implementation source | **Yes, may be reused by Adapter** |
| FBInk | Display implementation source | **Yes, may be reused by Adapter** |
| Kindle OS mechanisms | Lifecycle/Power/Network/Light implementation source | **Yes, may be wrapped by Adapter** |
| KOReader UIManager/widgets | Platform UI implementation | No |
| ReaderUI/CREngine/MuPDF | Platform Reader implementation | No |
| KPM | Platform native install/update | No |
| MRPI | legacy/bootstrap installer envelope | No |
| sh_integration | Home Entry/bootstrap integration | No |
| Hotfix | Homebrew foundation | No |
| KindleTool | build/package tooling | No |
| KUAL / PEKI | legacy/admin/bootstrap fallback | No |
| WinterBreak/SpringBreak/Sanctuary/Véra | Client Installation Route | No |
| Mesquito | upstream route implementation detail | No |

This table is a hard code-organization boundary for the Kindle implementation.

---

## 19. Kindle Adapter self-test

`QUICK` SHOULD validate:

```text
model / firmware resolved
Device Profile selected
native target consistent
Quirk Set selected
DisplayAdapter initialized
InputAdapter initialized
Storage root contained
Lifecycle hooks registered
Power sleep/wake integration available
Capability/subsystem consistency
backend version metadata readable
```

`INTERACTIVE` MAY validate:

```text
visible refresh
page keys
confirm/back
touch
frontlight
pen
```

Self-test must not modify user books/notes.

---

## 20. Kindle Adapter Contract Tests

Minimum reference coverage:

```text
KINDLE-ADAPTER-001 factory probe exact model/firmware behavior
KINDLE-ADAPTER-002 descriptor completeness
KINDLE-ADAPTER-003 unknown firmware is conservative
KINDLE-ADAPTER-004 base capability consistency
KINDLE-DISPLAY-001 screen geometry valid
KINDLE-DISPLAY-002 TEXT/QUALITY refresh safe
KINDLE-DISPLAY-003 region bounds safe
KINDLE-INPUT-001 navigation action normalization
KINDLE-INPUT-002 raw keycode does not leak
KINDLE-STORAGE-001 app root containment
KINDLE-STORAGE-002 symlink/path escape rejected
KINDLE-LIFECYCLE-001 sleep/wake mapping
KINDLE-POWER-001 sleep/wake available
KINDLE-PROFILE-001 target/profile/quirk separation
KINDLE-QUIRK-001 quirk only applies to declared range
KINDLE-ERROR-001 backend errors normalize
```

Optional capabilities add their corresponding tests.

Passing Adapter Contract Tests does not replace full-device BICTS.

---

## 21. Compatibility Record

Formal Kindle compatibility binds:

```text
Device Model
+ exact Firmware / tested range
+ Homebrew foundation state
+ Native Build Target
+ Device Profile version
+ Quirk Set version
+ Baga Platform version
+ Kindle Adapter version
+ Adapter Contract version
+ Lua Profile version
+ adopted component versions/commits
+ BICTS version/result
```

Status:

```text
Compatible
Experimental
Unsupported
```

Unknown firmware does not inherit Stable certification automatically.

---

## 22. First-phase implementation priority

The first Kindle Adapter does not need to support every historical Kindle model at once.

Recommended sequence:

```text
1. select one Homebrew-ready representative kindlehf device
2. implement Base Mandatory Adapter Contract
   - Identity
   - Capability
   - Display
   - Input
   - Storage
   - Lifecycle
   - Power
3. maximize reuse of pinned KOReader / FBInk / Kindle mechanisms
4. pass Adapter Contract Tests
5. run Baga Probe IKP
6. pass Base BICTS
7. add network / light / library and other optional subsystems
8. expand to kindlepw2 / classic / legacy targets
```

Coverage expands through Device Profile / Quirk / Build Target, not by copying LifeBook or Platform-shared code.

---

## 23. Relationship to the Kindle Implementation Freeze

The Kindle architecture freeze defines the wider chain:

```text
Client
→ jailbreak/bootstrap
→ Homebrew foundation
→ KPM/MRPI native Platform install
→ Baga Platform
→ IKP Package Manager
→ lifebook.ikp
→ Home Entry
```

This Standard is responsible only for:

> **How Kindle hardware/OS/firmware capability satisfies the Device Adapter Contract once Baga Platform is running.**

Therefore:

```text
Installation Route DB ≠ Device Profile
KPM capability ≠ Device Capability Registry
Native installer envelope ≠ Device Adapter
Home Entry ≠ InputAdapter
```

Do not mix these concepts.

---

## 24. Final principle

> **Kindle is the first Reference Port of the Baga Device Adapter Contract; Baga is not building another driver stack from scratch for Kindle.**

The ideal result is:

```text
Baga Kindle Adapter
≈ thin mapping / normalization glue
+ Device Profiles
+ Quirks
+ Contract Tests
```

standing on:

```text
KOReader
koreader-base
FBInk
Kindle OS
validated Homebrew ecosystem
```

As long as Standard 07, Capability semantics, and BICTS remain valid, replacing an internal Kindle backend later should not require changes to `lifebook.ikp` or the public `baga.*` contract.
