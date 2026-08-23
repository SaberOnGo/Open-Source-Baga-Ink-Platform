# Baga Ink Device Adapter Contract

> **Document level:** First-level Platform Standard  
> **Document ID:** `standards.07`  
> **Locale:** English (`en`)  
> **Status:** Draft v0.6  
> **Date:** 2026-08-23  
> **Parent:** `01_baga-ink-platform-strategy.md`  
> **Related:** Standards 03, 04, 08, 10, 13  
> **Counterpart:** `docs/zh-CN/standards/07_设备适配器规范.md`

---

## 0. Purpose

This document defines the **Baga Ink Device Adapter Contract**: the standard device-porting contract that a device, OS, firmware family, or vendor platform must implement in order to join Baga Ink Platform.

Core definition:

> **The Baga Device Adapter Contract defines what a device port must provide to Baga Ink; it does not prescribe that those capabilities must be reimplemented from scratch.**
>
> **Adapter implementations SHOULD prefer proven OS, vendor SDK, driver, Homebrew, and mature open-source mechanisms, adding only the mapping, normalization, capability detection, Quirk correction, and tests required by Baga.**

The contract can therefore be complete, strict, and testable while a concrete device Adapter remains very thin.

This document is written for:

```text
Baga Ink Platform implementers
OEM / device vendors
third-party device porters
Device Adapter maintainers
BICTS / compatibility maintainers
```

IKP App developers **do not call Device Adapters directly**. Apps use `baga.*`, Baga Lua Profile, and approved Standard Libraries.

---

## 1. Architectural position

```text
Universal / Enhanced IKP Apps
            │
            ▼
Baga Ink API / Baga Lua Profile
            │
            ▼
   Baga Ink Platform Core
            │
            ▼
  Baga Device Adapter Contract
            │
      ┌─────┴──────────────┐
      ▼                    ▼
 Kindle OS /           Android / Vendor SDK /
 Homebrew              Other E-Paper OS
```

The public device-capability chain remains:

```text
App
 ↓
baga.*
 ↓
Platform Core
 ↓
Device Adapter Contract
 ↓
Device / OS / firmware / vendor capability
```

Mature general-purpose libraries do not become Device Adapter subsystems merely because Baga adopts them:

```text
SQLite / lsqlite3
Automerge
general JSON / crypto / compression
```

Platform-shared Reader/UI implementations are also distinct from the Device Adapter. They obtain Display/Input/Storage/Lifecycle mechanisms through the Adapter where necessary.

---

## 2. Core design principles

### 2.1 Contract heavy, concrete Adapter light

Correct direction:

```text
complete, stable, testable Device Adapter Contract
                    ↓
             thin device implementation
                    ↓
        reuse OS / SDK / mature open-source capability
```

Wrong direction:

```text
"implement the Adapter"
→ rewrite framebuffer stack
→ rewrite input stack
→ rewrite reader engine
→ rewrite network stack
→ rewrite power manager
```

If a mature implementation already exists, the Adapter SHOULD wrap/call it rather than duplicate it.

### 2.2 Interfaces, not device conditionals

Model, firmware, and vendor differences MUST be concentrated as much as possible in Adapter / Device Profile / Quirk Set code.

Do not spread logic such as:

```text
if Kindle PW5 ...
if BOOX ...
if iReader ...
if firmware >= ...
```

through Universal Apps or Platform-neutral shared code.

Upper layers depend on stable interfaces; lower layers absorb device variation.

### 2.3 Mechanism, not product policy

An Adapter provides device mechanisms:

```text
how the screen refreshes
how input events are obtained
how the device sleeps/wakes
where safe storage roots exist
whether network is currently available
whether frontlight is controllable
```

An Adapter does not decide:

```text
LifeBook product logic
sync business policy
Market business behavior
UI page structure
Reader product policy
```

### 2.4 No mandatory separate process or IPC

The v0.6 Contract is a **semantic and implementation interface**, not an IPC protocol.

Reference Platforms SHOULD prefer:

```text
Platform Core
   ↓ direct typed call
Device Adapter
```

Baga does not require Binder, JSON bridges, RPC daemons, or independent Adapter processes merely to imitate another platform architecture.

If a future OS requires process isolation, it may implement that internally while preserving Contract semantics.

---

## 3. Base Contract and optional subsystems

Baga uses:

> **Root Adapter + Typed Subsystem Interfaces**

rather than an ever-growing monolithic `DeviceAdapter` class.

Logical structure:

```text
BagaDeviceAdapter
│
├── Identity / Descriptor                MUST
├── Capability Snapshot                  MUST
├── DisplayAdapter                       MUST
├── InputAdapter                         MUST
├── StorageAdapter                       MUST
├── LifecycleAdapter                     MUST
├── PowerAdapter                         MUST
│
├── NetworkAdapter                       OPTIONAL
├── LightAdapter                         OPTIONAL
├── AudioAdapter                         OPTIONAL
├── BluetoothAdapter                     OPTIONAL
└── UserLibraryBridge                    OPTIONAL
```

Pen / Touch / Keyboard are optional capabilities of `InputAdapter`; they do not require separate top-level Adapter types.

Reader is not a top-level Device Adapter subsystem.

Base Compatibility corresponds to the current Capability Registry baseline:

```text
display.basic
input.navigation
storage.app_sandbox
power.sleep_wake
platform.lifecycle
```

If an optional subsystem is absent, the implementation must explicitly report `not_supported` / absent; it must not fabricate capability.

---

## 4. Adapter Factory and loading model

### 4.1 v0.6 default: built/packaged with the Platform

First-phase Adapters SHOULD follow:

```text
Adapter source
   ↓
Baga Adapter SDK / generated interfaces
   ↓
compile/link/package with Platform
```

Examples:

```text
Kindle Adapter
→ baga-platform.kpkg / native Platform envelope

Android Adapter
→ Baga Ink Platform APK
```

v0.6 **does not define a downloadable third-party Native Adapter plugin ABI based on arbitrary `dlopen()`**.

If Baga later supports independently signed native Adapter modules, a separate standard must define ABI, signing, dependencies, crash isolation, and supply-chain policy.

### 4.2 Root Factory

A Platform may include one or more Adapter Factories.

Logical interface:

```text
AdapterFactory
├── probe(BootstrapDeviceInfo) -> ProbeResult
└── create(AdapterCreateContext, ProbeResult) -> BagaDeviceAdapter
```

`probe()` MUST:

- use only information safely available during Platform bootstrap;
- not modify user data;
- not assume other models in the same product family are equivalent;
- explicitly return unknown / unsupported for unknown devices/firmware;
- provide the evidence needed to select a Device Profile and Quirk Set.

A Platform build serving one device family may contain only one Factory.

---

## 5. Root Adapter lifecycle

Language-neutral logical interface:

```text
BagaDeviceAdapter
├── contract_version() -> AdapterContractVersion
├── adapter_version() -> Version
├── descriptor() -> DeviceDescriptor
├── capabilities() -> CapabilitySnapshot
├── init(AdapterHost) -> Result
├── self_test(SelfTestMode) -> SelfTestReport
├── subsystem(name) -> typed subsystem / absent
└── shutdown() -> Result
```

Initialization sequence:

```text
Platform bootstrap
      ↓
AdapterFactory.probe
      ↓
AdapterFactory.create
      ↓
Adapter.init
      ↓
Adapter.descriptor + capability snapshot
      ↓
Adapter self-test
      ↓
Platform Core ready
      ↓
IKP Apps may start
```

A Platform MUST NOT mark the device `Baga Ink Compatible` while Base Mandatory subsystems are not ready.

---

## 6. DeviceDescriptor

An Adapter MUST return a stable structured device description.

Minimum logical fields:

```text
adapter_contract_version
adapter_id
adapter_version

device_family
manufacturer
model
model_id
firmware_or_os_version

cpu_arch
native_target / abi_profile     when applicable

screen
input_summary

profile_id                      when a profile model is used
quirk_set_id                    when a quirk set is active
compatibility_record_id         when available
```

`screen` includes at least:

```text
pixel_width
pixel_height
orientation
```

The Descriptor is used by Platform, Client, diagnostics, and Compatibility. It is not a Universal App entry point for model branching.

By default it MUST NOT expose:

```text
device serial number
Amazon / Google / OEM user account
user book contents
user note contents
user credentials
```

If diagnostics genuinely require a unique device identifier, use a separately controlled privacy mechanism.

---

## 7. Capability Snapshot versus Runtime State

The implementation MUST distinguish:

```text
Capability Snapshot
→ what this device/Platform combination can do

Runtime State
→ what the current state is right now
```

Examples:

```text
Capability: network.wifi = supported
Runtime State: offline
```

```text
Capability: power.battery_level = supported
Runtime State: battery = 72%
```

Capability names come from Standard 04.

An Adapter MUST NOT declare capability merely because an internal library is present.

The Capability Snapshot SHOULD remain stable during a Platform session. If firmware behavior or hot-plugged peripherals truly change capability, Platform must regenerate the snapshot through an explicit capability-change event rather than silently changing behavior.

---

## 8. AdapterHost and event model

Platform Core provides a controlled `AdapterHost` during `init()`.

Logical responsibilities:

```text
AdapterHost
├── emit(AdapterEvent)
├── monotonic_time()
├── platform_log(...)
└── controlled scheduling / wake hook as implemented
```

Core rule:

> **An Adapter / vendor callback MUST NOT call an IKP App directly. All device events enter Platform Core first.**

An Adapter may receive callbacks from arbitrary OS/device threads, but it must:

- convert them into typed `AdapterEvent` values;
- submit them to Platform Core;
- let Platform Core handle App-side ordering, deduplication, and lifecycle dispatch;
- not implement a second App event loop merely because the backend uses callbacks.

Typical events:

```text
LifecycleEvent
NavigationEvent
PointerEvent
KeyboardEvent
PenEvent
PowerStateEvent
NetworkStateEvent
DisplayStateEvent
LightStateEvent
BluetoothStateEvent
CapabilityChangedEvent     rare / explicit
```

---

## 9. Stable error model

Backend errors must be normalized into stable machine semantics before Platform Core maps them into public `baga.*` errors.

Recommended v0.6 base codes:

```text
not_supported
not_ready
invalid_argument
invalid_state
out_of_bounds
busy
timeout
io_error
storage_full
offline
device_error
permission_unavailable
```

Rules:

- do not expose raw vendor integer error codes as the Universal App contract;
- Adapter MAY retain backend codes in diagnostics;
- raw backend codes cannot become App business-logic branches;
- recoverability must be explicit.

---

## 10. DisplayAdapter Contract

`DisplayAdapter` provides **device display and refresh mechanisms**. It is not a complete UI framework and does not imply a separate rendering engine.

Logical interface:

```text
DisplayAdapter
├── info() -> DisplayInfo
├── supports(intent) -> boolean
└── refresh(RefreshRequest) -> Result
```

`DisplayInfo` includes at least:

```text
pixel_width
pixel_height
logical_width
logical_height
orientation
grayscale_levels       if known
color                   boolean / profile
```

`RefreshRequest`:

```text
regions[]
intent
```

Standard intents:

```text
AUTO
TEXT
QUALITY
FAST
ANIMATION
```

`regions` use the current Baga logical display coordinate space. Out-of-range requests must be rejected or safely clipped; they must never write beyond framebuffer boundaries.

Device internals may use:

```text
Kindle waveform
FBInk
KOReader display backend
BOOX refresh mode
Vendor SDK
Linux framebuffer/DRM
```

These do not leak into the standard interface.

If a device only supports full-screen refresh, the Adapter may safely downgrade a region refresh to full refresh, but capabilities must reflect the actual behavior.

---

## 11. InputAdapter Contract

`InputAdapter` normalizes raw device input into Baga input semantics.

Base Mandatory support must be able to produce at least:

```text
confirm
back
menu               if the device/platform provides an equivalent semantic action
page_next
page_previous
focus_next
focus_previous
```

A device without a dedicated `menu` key may expose an equivalent Platform/UI interaction; the Adapter does not need to invent a physical button.

Standard event families:

```text
NavigationAction
PointerEvent
KeyboardEvent
PenEvent
```

Pointer phases:

```text
down
move
up
cancel
```

Pen pressure / eraser / hover / low-latency data is provided only when truly supported and accompanied by the corresponding Capability declaration.

The Adapter MUST NOT expose Kindle keycodes, Android `KeyEvent`, vendor `MotionEvent` objects, or similar backend types directly to IKP.

---

## 12. StorageAdapter Contract

`StorageAdapter` provides the device mechanisms required for Platform to establish safe logical storage.

App-visible logical roots remain:

```text
appdata/
cache/
documents/
downloads/
```

The Adapter MUST provide at least:

```text
storage_info()
platform_private_root()
app_private_root(app_id)
canonicalize / containment mechanism
free_space()                 if reliably available
atomic-replace capability metadata
fsync/durability profile     if applicable
```

A `root` is a Platform-internal `NativePathHandle` or equivalent, not a stable physical path exposed to IKP Apps.

Platform + Adapter together enforce:

- path normalization;
- rejection of `..` escape;
- rejection of unauthorized absolute paths;
- symlink/canonical escape protection;
- disk-full errors;
- Platform updates not deleting App data by default;
- staged packages separated from App data.

On weak-OS-sandbox platforms such as Kindle, SQLite must still satisfy Standard 13 and BICTS VFS/equivalent I/O confinement for ATTACH, journal, WAL, SHM, temp DB, and related paths. Merely returning a nominally legal directory is not a complete sandbox.

---

## 13. LifecycleAdapter Contract

`LifecycleAdapter` maps OS/device events into lifecycle facts Platform can rely on.

It MUST support signals sufficient for:

```text
sleep
wake
```

and allow Platform to construct:

```text
start
resume
pause
sleep
wake
stop
```

Rules:

- SHOULD use events/callbacks rather than high-frequency polling;
- after wake, Platform may re-check network/power/device state;
- Adapter callbacks do not call App lifecycle handlers directly;
- Platform Core owns App lifecycle ordering.

---

## 14. PowerAdapter Contract

Base Mandatory capability:

```text
power.sleep_wake
```

Optional logical interface:

```text
battery_level()
charging_state()
request_keep_awake(reason)
release_keep_awake(token)
```

Declare only capabilities that can actually be implemented:

```text
power.battery_level
power.charging_state
power.keep_awake
```

Platform may refuse a keep-awake request; an App must not assume success.

---

## 15. NetworkAdapter Contract (optional)

`NetworkAdapter` provides **device/OS connectivity state and any necessary platform bridge**. It does not require every Adapter to reimplement an HTTP/TLS stack.

Minimum logical interface:

```text
connectivity_state()
network_info()
```

Typical emitted events:

```text
online
offline
network_changed
```

A Platform may:

```text
share a mature HTTP/TLS library
or
use the OS network stack
```

provided public `baga.network` semantics and BICTS requirements hold.

The existence of `NetworkAdapter` must not pull Automerge sync protocol, HTTP client policy, or LifeBook sync business rules into the Device Adapter.

---

## 16. Light / Audio / Bluetooth optional contracts

### 16.1 LightAdapter

Possible methods:

```text
get_level()
set_level(level)
get_temperature()
set_temperature(value)
```

Declare `light.frontlight*` only where actually controllable.

### 16.2 AudioAdapter

Provides only the device audio input/output mechanisms required by Platform. A TTS engine itself may belong to Platform-shared implementation.

### 16.3 BluetoothAdapter

Provides Bluetooth availability, controlled operations, and normalized events/capabilities. Vendor-private objects do not leak to Apps.

---

## 17. UserLibraryBridge (optional)

User Library is strongly device-specific, so the Device Adapter may provide the underlying bridge while the product/semantic `baga.library` API remains a Platform responsibility.

Logical bridge operations:

```text
enumerate library items
open opaque source handle
import/remove when supported and permitted
rescan/refresh
```

Rules:

- item IDs / source handles are opaque to Apps;
- Kindle `/documents` or Android vendor database paths do not become Universal contracts;
- Platform Permission Model controls access;
- Reader may consume an opaque source handle;
- Library Bridge is not the Reader engine.

---

## 18. Reader and UI are not Device Adapter root subsystems

Maintain these boundaries:

```text
baga.ui
  ↓
Platform UI implementation/backend
  ↓
Device Adapter: Display + Input
```

```text
baga.reader
  ↓
Platform Reader implementation
  ↓
Device Adapter: Display + Input + Storage + Lifecycle
```

Therefore:

- KOReader ReaderUI / CREngine / MuPDF may be the Kindle Platform Reader implementation;
- KOReader UIManager/widgets may be the Kindle Platform UI implementation;
- those layers may reuse the same lower-level Kindle device knowledge as the Adapter;
- `ReaderAdapter` / `UIAdapter` should not be mechanically added to the root Device Adapter Contract merely for implementation convenience.

Reader Capability remains defined by Standards 03/04.

---

## 19. Native Build Target, Device Profile, and Quirk Set are distinct

These are three different dimensions of device support.

### 19.1 Native Build Target / ABI Profile

Answers:

> **How is native code compiled/linked?**

Kindle examples:

```text
kindle-legacy
kindle
kindlepw2
kindlehf
```

A build target is not a device model.

### 19.2 Device Profile

Answers:

> **What verified device facts, backend choices, and capability expectations are known for a specific model + firmware combination?**

A Profile SHOULD be data-driven, for example:

```text
profile_id
match: model / firmware range
native_target
screen expectations
input expectations
baseline capability expectations
preferred backend choices
known validation status
```

A Profile is not a Compatibility certification result. Runtime capability evidence + BICTS still determine compatibility.

### 19.3 Quirk Set

Answers:

> **Which deviations from standard behavior exist for this exact combination, and what corrections must the Adapter apply?**

A Quirk record SHOULD include:

```text
quirk_id
match condition
reason
workaround
scope
introduced/verified firmware range
test reference
```

Typical Quirks:

```text
touch correction
refresh workaround
frontlight behavior
sleep event issue
network issue
library bridge difference
```

A Quirk MUST NOT become a public Capability and MUST NOT leak into IKP business code.

---

## 20. Installation Route is separate from Device Adapter

"How does this device obtain Baga Platform?" is not the same problem as "how does the running Platform access the device?"

Therefore:

```text
jailbreak / bootstrap / KPM / MRPI / APK install
→ Installation / Platform bootstrap

Device Adapter
→ after Platform is running, normalize device / OS / firmware differences
```

Kindle WinterBreak / SpringBreak / Sanctuary / Véra, KPM, MRPI, KUAL, PEKI, KindleTool, and similar mechanisms do not enter the Device Adapter Contract simply because they are device-related.

Standard 11 and the Kindle implementation freeze define the Kindle-specific boundary.

---

## 21. Self-test

Every Adapter MUST provide a non-destructive self-test.

Recommended modes:

```text
QUICK
INTERACTIVE
```

`QUICK` checks at least:

```text
Descriptor consistency
Base subsystem presence
Capability/subsystem consistency
Display info valid
Storage root accessible and contained
Lifecycle hook registered
Power sleep/wake integration initialized
Backend versions readable where applicable
```

`INTERACTIVE` MAY additionally validate:

```text
visible refresh
navigation keys
touch
pen
frontlight
```

Self-test does not replace BICTS. It is an installation/diagnostic mechanism for detecting obvious Adapter breakage.

---

## 22. Adapter Contract versioning

Three versions must remain distinct:

```text
Adapter Contract Version
→ this standard interface version

Adapter Version
→ a concrete Adapter implementation version

Device/Firmware Version
→ the underlying device version
```

Reference model:

```text
adapter_contract = MAJOR.MINOR
```

Rules:

- MAJOR permits breaking Contract changes;
- MINOR permits only backward-compatible additions;
- semantics of existing fields/methods in a frozen MINOR must not change silently;
- new optional methods/type fields require clear default/absent semantics;
- Platform MUST reject unsupported Contract MAJOR versions;
- Platform SHOULD run older MINOR Adapters within its declared compatibility range.

Future machine-readable IDL / Codegen MUST preserve frozen contract snapshots and run compatibility checks automatically.

---

## 23. Adapter Contract Tests versus BICTS

Two test layers are required.

### 23.1 Adapter Contract Tests

Directly validate the Adapter:

```text
Factory / probe
Descriptor
Capability consistency
Display contract
Input event normalization
Storage containment
Lifecycle event mapping
Power contract
Optional subsystem behavior
Error normalization
Profile / Quirk selection
Self-test
```

They answer:

> **Does this Adapter correctly implement the Device Adapter Contract?**

### 23.2 BICTS

BICTS validates the public Baga behavior of the full combination:

```text
Device + Firmware/OS + Platform + Adapter + Lua Profile
```

It answers:

> **May this concrete combination claim Baga Ink Compatible?**

Adapter Contract Tests PASS does not imply BICTS PASS. Formal compatibility should include Adapter Contract evidence as well.

---

## 24. Mock / Reference Adapter requirement

Baga SHOULD maintain a:

> **Mock / Headless Device Adapter**

Purposes:

- minimal Reference Implementation of the Device Adapter Contract;
- Platform Core host-side tests;
- IKP development without real hardware;
- reference for OEM/third-party Adapter developers;
- automated Adapter Contract Tests.

Recommended capabilities:

```text
Display → in-memory bitmap / PNG snapshot
Input → scripted events
Storage → temporary sandbox
Lifecycle → simulated sleep/wake
Power → simulated battery/charging
Network → simulated online/offline
Device Profile → configurable fixture
```

A Mock Adapter cannot be used to claim real-hardware compatibility.

---

## 25. Language and SDK

The Device Adapter Contract is language-neutral.

Platform internals MAY use:

```text
Rust
C / C++
Kotlin / Java
JNI
Lua
controlled device-specific Shell integration
```

Long term, Baga SHOULD maintain a machine-readable Adapter Contract / IDL and generate:

```text
Rust traits/types
C headers/vtables
Kotlin interfaces/data classes
Mock stubs
Contract test fixtures
Documentation tables
```

The machine IDL exists to reduce drift across Kindle/Android/OEM implementations. It does not replace the semantic authority of this Standard.

Implementation design is tracked in the localized Device Adapter Executable Contract / SDK Design document.

---

## 26. Security boundary

The Device Adapter sits on a privileged device boundary.

It MUST:

- not expose arbitrary shell to IKP;
- not expose Android Context, Kindle private framework objects, or vendor SDK objects to Apps;
- validate refresh regions, paths, indexes, ranges, and similar inputs;
- not allow Apps to bypass Permission/Sandbox through the Adapter;
- not deliver raw device callbacks directly to Apps;
- not log user content, notes, or credentials in ordinary diagnostics;
- not allow malformed inputs to cause out-of-bounds hardware access;
- convert Adapter failure/crash into diagnosable Platform faults rather than corrupting App data.

---

## 27. OEM / third-party device-porting flow

Standard workflow:

```text
read Standards 01 / 03 / 04 / 07
        ↓
select/implement Adapter SDK backend
        ↓
implement Base Mandatory subsystems
        ↓
reuse OS / Vendor SDK / mature libraries
        ↓
implement Device Profile / Quirk where required
        ↓
Adapter self-test
        ↓
Adapter Contract Tests
        ↓
implement and declare optional Capabilities
        ↓
BICTS
        ↓
generate Compatibility Record
        ↓
Baga Ink Compatible / Experimental / Unsupported
```

A third-party Adapter does not require modifications to Universal IKP Apps.

---

## 28. Design references (non-normative dependencies)

The Contract is informed by mature platform-abstraction ideas without copying their process models or concrete ABIs:

- Android HAL / Stable AIDL — standard vendor interfaces, freezing, compatibility;
- Zephyr Device Driver Model — generic subsystem API with device-specific implementations;
- Chromium Ozone — interfaces instead of platform `#ifdef`s; mechanism below policy;
- Qt QPA — platform backend / minimal platform implementation experience.

These projects are not Baga runtime dependencies and do not require Baga to adopt their IPC, window system, or driver ABI.

---

## 29. Final principle

> **Baga Device Adapter is the stable Porting Contract by which a device joins Baga Ink Platform. The standard must be complete enough for OEMs/third parties to know what to implement; a concrete Adapter should remain as thin as practical by standing on existing OS, vendor SDK, Homebrew, and mature open-source capabilities.**

In short:

> **Standardize device semantics, not device reimplementation; centralize device variation instead of spreading model/firmware conditionals into Platform and IKP Apps.**
