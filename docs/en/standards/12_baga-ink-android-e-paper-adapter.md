# Baga Ink Android E-Paper Device Adapter

> **Document level:** Reference Device-Family Adapter Standard  
> **Document ID:** `standards.12`  
> **Locale:** English (`en`)  
> **Status:** Draft v0.6  
> **Date:** 2026-08-23  
> **Parent Contract:** Standard 07 — Baga Ink Device Adapter Contract  
> **Certification:** Standards 08 / 10  
> **Standard Libraries:** Standard 13  
> **Counterpart:** `docs/zh-CN/standards/12_Android墨水屏适配规范.md`

---

## 0. Purpose

This document defines how **Android e-paper devices** implement the Baga Device Adapter Contract.

Android gives Baga a much stronger common OS baseline than Kindle, but the e-paper layer remains fragmented across vendors. Different products expose different refresh APIs, Pen paths, frontlight controls, library integrations, power behavior, Android versions, and vendor SDKs.

The reference strategy is therefore:

> **Implement a Generic Android Base Adapter for common Android behavior, then add vendor specializations only for the capabilities that genuinely differ on e-paper hardware.**

The Adapter should not become a wrapper around the entire Android SDK and should not force every vendor difference into Universal Apps.

---

## 1. Authority boundary

Keep three levels distinct:

```text
Standard 07 — Device Adapter Contract
→ what every Baga device port must provide

Standard 12 — Android E-Paper Adapter
→ how Android e-paper devices implement Standard 07

Vendor specialization
→ BOOX / iReader / Bigme / Hanvon / Moaan / future vendor-specific mechanisms
```

Vendor SDK objects and private Android APIs remain implementation details below the Adapter. They do not become Baga App APIs.

---

## 2. Reference architecture

Recommended internal organization:

```text
Baga Android E-Paper Device Adapter
│
├── factory/
│   ├── probe
│   └── create
│
├── common/
│   ├── descriptor
│   ├── capability_detection
│   ├── error_mapping
│   ├── event_normalization
│   └── self_test
│
├── generic/
│   ├── display
│   ├── input
│   ├── storage
│   ├── lifecycle
│   ├── power
│   ├── network
│   ├── audio
│   └── bluetooth
│
├── vendors/
│   ├── boox/
│   ├── ireader/
│   ├── bigme/
│   ├── hanvon/
│   ├── moaan/
│   └── ...
│
├── library/
├── device_profiles/
└── quirks/
```

This is an internal Reference implementation structure, not a public API.

---

## 3. Generic Android versus vendor specialization

### 3.1 Generic Android responsibilities

Generic Android SHOULD implement common Android mechanisms wherever the public Baga semantics can be satisfied without vendor-private behavior.

Typical responsibilities:

```text
App/process lifecycle integration
Android app-private storage
files / content URI bridging
common touch / key / keyboard input
connectivity state
battery / charging state
Android audio
Android Bluetooth
basic display information
OS-level permission/sandbox integration
```

### 3.2 Vendor specialization responsibilities

Vendor specialization SHOULD be limited to real e-paper/vendor differences, for example:

```text
partial / fast / quality refresh APIs
vendor waveform / refresh mode selection
Pen low-latency path
frontlight / warm-light controls
vendor power optimizations
vendor library bridge
special key mappings
vendor-specific lifecycle quirks
```

Do not create a vendor specialization merely because a vendor class name exists. If generic Android already satisfies the Contract correctly, use the generic implementation.

---

## 4. AndroidAdapterFactory

Reference factory:

```text
AndroidAdapterFactory
├── probe(BootstrapDeviceInfo)
└── create(...)
```

`probe()` SHOULD collect safe bootstrap facts such as:

```text
manufacturer
brand
model
product / device identifiers
Android version / API level
CPU ABI
screen characteristics
known vendor SDK availability
known Device Profile match
```

It MUST:

- avoid destructive probing;
- handle unknown models conservatively;
- not infer a vendor SDK is usable merely from `Build.MANUFACTURER`;
- choose Generic Android when vendor specialization is not validated;
- select Device Profile / Quirk Set from evidence.

---

## 5. DeviceDescriptor

Minimum logical descriptor includes:

```text
adapter_contract_version
adapter_id
adapter_version

device_family = android-e-paper
manufacturer
model
model_id / product identity
os_version
api_level
cpu_arch / abi_profile
screen
input_summary
profile_id
quirk_set_id
compatibility_record_id
```

Do not expose Google/OEM account identity, device serials, user documents, or credentials to Apps by default.

---

## 6. Capability detection

Base Baga Compatibility still requires:

```text
display.basic
input.navigation
storage.app_sandbox
power.sleep_wake
platform.lifecycle
```

Typical Android E-Paper optional capabilities include:

```text
display.partial_refresh
display.fast_refresh
display.quality_refresh
display.animation
display.grayscale
display.color
input.touch
input.multitouch
input.pen
input.pen.pressure
input.pen.eraser
input.pen.hover
input.pen.low_latency
input.physical_page_key
network.available
network.wifi
network.http
network.https
light.frontlight
light.frontlight.temperature
audio.output
audio.microphone
bluetooth.available
bluetooth.input_device
bluetooth.audio
storage.user_library
```

Capability evidence priority:

```text
runtime probe / validated SDK behavior
        >
verified Device Profile
        >
marketing/spec assumptions
```

A generic Android API existing in the OS does not automatically mean the e-paper device can satisfy the Baga semantic capability at production quality.

---

## 7. DisplayAdapter

Android `DisplayAdapter` must implement Standard 07 semantic refresh intents:

```text
AUTO
TEXT
QUALITY
FAST
ANIMATION
```

Reference mapping:

```text
Baga refresh intent
        ↓
Android E-Paper DisplayAdapter
        ↓
Generic Android behavior OR vendor specialization
        ↓
BOOX / iReader / Bigme / Hanvon / other refresh API
        ↓
physical E-Paper display
```

Vendor-specific mode names, SDK enums, waveform IDs, and private objects MUST NOT leak to Apps.

### 7.1 Generic fallback

If no validated vendor refresh API is available, the Adapter MAY provide conservative basic display behavior and declare only the capabilities actually supported.

Do not claim `display.fast_refresh` merely because ordinary Android rendering works.

### 7.2 Region safety

Refresh regions must use the Baga logical coordinate space and must be checked/clipped safely before any vendor API receives them.

---

## 8. InputAdapter

Generic Android can normally supply:

```text
touch
multitouch
physical keys
keyboard
navigation actions
```

The Adapter normalizes Android events into Baga semantics and must not expose raw `KeyEvent`, `MotionEvent`, `InputDevice`, or vendor event objects to IKP.

Semantic actions include:

```text
confirm
back
menu
page_next
page_previous
focus_next
focus_previous
```

### 8.1 Pen

Pen support often requires vendor-specific handling for:

```text
pressure
eraser
hover
low-latency ink
```

Declare only the Pen capabilities that are actually validated.

Low-latency Pen paths must remain behind Baga semantics; Universal Apps do not call vendor handwriting SDKs directly.

---

## 9. StorageAdapter

Android has a stronger OS sandbox than Kindle and SHOULD use it rather than recreate another filesystem security model.

Reference behavior:

```text
Platform private root
→ Android app-private storage

App private root
→ Platform-managed subdirectory / protected storage identity

User files
→ controlled Android file/content bridge where applicable
```

The Adapter / Platform must still provide Baga logical roots:

```text
appdata/
cache/
documents/
downloads/
```

Rules:

- IKP Apps do not depend on `/sdcard` or vendor-specific paths;
- Android Content URI / SAF objects are not Universal App contracts;
- path containment remains enforced;
- Platform package updates do not delete IKP App data by default;
- package releases and App data remain separate.

SQLite / lsqlite3 uses the pinned Baga SQLite profile and the Platform's authorized App-private path. It is not a Device Adapter database API.

---

## 10. LifecycleAdapter

Generic Android lifecycle mechanisms should be mapped into Baga semantic lifecycle facts:

```text
start
resume
pause
sleep
wake
stop
```

The implementation may use Android process/application/activity/service signals internally, but IKP does not depend on Android lifecycle classes.

E-paper/vendor firmware may introduce unusual suspend/resume behavior; those differences belong in Device Profile / Quirk handling.

---

## 11. PowerAdapter

Generic Android can usually provide:

```text
battery level
charging state
basic sleep/wake integration
```

Vendor specialization MAY provide additional e-paper-specific mechanisms.

`request_keep_awake()` remains a request subject to Platform policy. Universal Apps do not directly acquire Android wake locks.

---

## 12. NetworkAdapter

Generic Android SHOULD use the OS connectivity/network stack rather than build a vendor-specific network stack.

Responsibilities include:

```text
connectivity state
network-change events
sleep/wake disruption mapping
controlled bridge to Platform networking
```

HTTP/TLS may be implemented by Platform-shared libraries or OS facilities.

Automerge sync protocol and product sync policy do not belong in the Adapter.

---

## 13. LightAdapter

Frontlight/warm-light control is not standardized by Android itself across e-paper vendors.

Vendor specialization MAY implement:

```text
get_level()
set_level(level)
get_temperature()
set_temperature(value)
```

Declare only:

```text
light.frontlight
light.frontlight.temperature
```

that are proven for the exact model/firmware range.

---

## 14. Audio / Bluetooth

Android often provides mature OS-level Audio/Bluetooth APIs, so Generic Android SHOULD reuse them where the hardware exposes the capability reliably.

Declare only actual capability:

```text
audio.output
audio.microphone
bluetooth.available
bluetooth.input_device
bluetooth.audio
```

An Android API existing in the SDK does not guarantee the physical device includes the corresponding hardware.

---

## 15. UserLibraryBridge

Android e-paper vendors often maintain their own bookshelf/library databases.

The bridge may use:

```text
validated filesystem/document source
Android content interfaces
vendor library SDK/API where stable and permitted
```

but Apps receive only Baga opaque items/handles through `baga.library`.

Rules:

- do not expose vendor database schemas as a Universal contract;
- do not require Apps to understand Content URI or vendor object types;
- enforce `library.read/write` permissions;
- a source handle may be passed to `baga.reader`;
- Library Bridge is not the Reader engine.

A conservative file-based bridge is acceptable before deeper vendor integration is proven safe.

---

## 16. Vendor specialization model

Reference shape:

```text
GenericAndroidAdapter
        │
        ├── common base behavior
        │
        └── VendorSpecialization (optional)
              ├── display backend
              ├── pen backend
              ├── frontlight backend
              ├── library backend
              └── quirks
```

A vendor specialization SHOULD override only the subsystem behavior that genuinely differs.

Do not copy the entire Adapter per vendor.

---

## 17. Device Profile and Quirk Set

A Device Profile SHOULD describe:

```text
manufacturer / model match
Android version / API range
ABI
screen expectations
input expectations
vendor SDK expectations
baseline capability expectations
preferred display / pen / light backends
validation status
last verified date
```

A Quirk Set records exact deviations such as:

```text
refresh bug
orientation mismatch
pen coordinate correction
frontlight range issue
sleep/wake event issue
vendor firmware behavior change
```

Profiles are evidence-backed data, not marketing tables. Quirks never become public Capabilities.

---

## 18. Generic Android should be useful by itself

The Adapter architecture should avoid a world where every Android e-paper device requires a full vendor fork.

The Generic Adapter SHOULD be able to provide Base Contract behavior on an unknown but sufficiently normal Android device when safe, while vendor specialization adds e-paper enhancements only after validation.

Unknown/vendor-unvalidated devices default to conservative Capability declarations and an Experimental/Unsupported compatibility state as required by Standards 08/10.

---

## 19. Standard Libraries / Reader reuse

Android Platform MAY reuse mature components for:

```text
SQLite / lsqlite3
Automerge
MuPDF / CREngine / KOReader-derived or other reader engines where license/architecture allows
HTTP/TLS
JSON / crypto / compression
```

These components do not become Device Adapter subsystems merely because the Android implementation uses them.

The Device Adapter owns device/OS variation; mature general-purpose libraries remain Standard Libraries or Platform implementation details according to Standard 13.

---

## 20. Self-test

`QUICK` SHOULD validate:

```text
manufacturer/model/OS resolved
Device Profile selected or unknown handled conservatively
vendor specialization selection justified
DisplayAdapter initialized
InputAdapter initialized
Storage sandbox valid
Lifecycle hooks active
Power integration available
Capability/subsystem consistency
backend/SDK version metadata readable where applicable
```

`INTERACTIVE` MAY validate:

```text
visible refresh
touch
physical keys
pen
frontlight
rotation
```

Self-test must not modify user library data.

---

## 21. Android Adapter Contract Tests

Reference coverage includes:

```text
ANDROID-ADAPTER-001 factory probe behavior
ANDROID-ADAPTER-002 descriptor completeness
ANDROID-ADAPTER-003 unknown vendor/model conservative behavior
ANDROID-CAP-001 capability/subsystem consistency
ANDROID-DISPLAY-001 basic display info valid
ANDROID-DISPLAY-002 refresh intent safely mapped
ANDROID-DISPLAY-003 vendor refresh enum does not leak
ANDROID-INPUT-001 semantic navigation normalization
ANDROID-INPUT-002 raw Android event objects do not leak
ANDROID-STORAGE-001 App root containment
ANDROID-STORAGE-002 package/data separation
ANDROID-LIFECYCLE-001 semantic lifecycle mapping
ANDROID-POWER-001 sleep/wake integration
ANDROID-PROFILE-001 profile/quirk selection
ANDROID-VENDOR-001 specialization only selected for validated range
ANDROID-ERROR-001 backend errors normalize
```

Add capability-specific tests for Pen, Frontlight, Audio, Bluetooth, Library, etc.

Passing Adapter Contract Tests does not replace full BICTS.

---

## 22. Compatibility Record

Formal Android E-Paper compatibility binds:

```text
Device Model
+ exact Android / firmware tested range
+ Native ABI/Profile
+ Device Profile version
+ Quirk Set version
+ Vendor specialization version/state
+ Baga Platform version
+ Android Adapter version
+ Adapter Contract version
+ Lua Profile version
+ adopted component versions/commits
+ BICTS version/result
```

States:

```text
Compatible
Experimental
Unsupported
```

An Android OS update or vendor firmware update may invalidate prior evidence.

---

## 23. First-phase implementation priority

Recommended sequence:

```text
1. implement Generic Android Base Adapter
2. pass Base Adapter Contract Tests on a representative Android E-Paper device
3. run Probe IKP + Base BICTS
4. add one vendor specialization for a well-documented/available vendor
5. validate E-Paper refresh + optional Pen/frontlight behavior
6. expand to additional vendors through specialization + Profiles/Quirks
```

Do not start by copying complete per-vendor Adapter trees.

---

## 24. Relationship to Apps

The same Universal IKP should remain unaware of whether it is running on:

```text
Generic Android
BOOX specialization
iReader specialization
Bigme specialization
Hanvon specialization
future vendor specialization
```

Apps only query Baga Capabilities and use stable Baga APIs / Standard Libraries.

If vendor conditionals start appearing in Universal App business code, the Adapter boundary has failed.

---

## 25. Final principle

> **Android gives Baga a common OS baseline; the Android E-Paper Adapter uses that baseline for generic behavior and isolates true vendor e-paper differences behind small, evidence-backed specializations.**

The target is:

```text
Generic Android Base Adapter
+ thin vendor specializations
+ Device Profiles
+ Quirk Sets
+ Contract Tests / BICTS
```

not:

```text
one full Platform fork per e-paper vendor
```
