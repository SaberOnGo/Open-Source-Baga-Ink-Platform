# Baga Ink Capability Registry

> **Document level:** First-level platform standard  
> **Document ID:** `standards.04`  
> **Locale:** English (`en`)  
> **Status:** Draft v0.4  
> **Date:** 2026-08-23  
> **Parent:** `01_baga-ink-platform-strategy.md`  
> **Related:** Standards 03, 07, 08, 13  
> **Counterpart:** `docs/zh-CN/standards/04_能力注册表.md`

---

## 0. Purpose

The Capability Registry defines:

> **Which cross-device capabilities a device or Platform provides and which stable semantic names Apps use to query them.**

It is not a list of open-source libraries, Standard Libraries, databases, or internal implementation names.

Active text contains only currently registered Capabilities and current rules.

---

## 1. Naming rules

Capability names use lowercase dot-separated hierarchy:

```text
category.feature
category.feature.variant
```

Examples:

```text
display.partial_refresh
input.pen.pressure
light.frontlight.temperature
reader.anchor
```

Rules:

- MUST use lowercase ASCII;
- MUST use `.` for hierarchy;
- MUST NOT contain vendor brand names;
- MUST NOT contain internal library/project names;
- MUST describe portable capability semantics rather than implementation APIs;
- published stable Capability names SHOULD not be renamed casually.

SQLite / `lsqlite3` is a Baga Lua Profile Standard Library. Automerge is an Adopted Foundation. Neither belongs in this Registry.

---

## 2. Capability versus Permission

Capability answers whether the device/Platform **can provide** a mechanism.

Permission answers whether an App **may use** a protected resource or user data.

Example:

```text
Capability: network.wifi
Permission: network
```

Authorization behavior is defined by Standard 05.

---

## 3. Base Profile

Every Baga Ink Compatible device MUST provide, or satisfy the standardized fallback semantics for:

```text
display.basic
input.navigation
storage.app_sandbox
power.sleep_wake
platform.lifecycle
```

This baseline allows a basic IKP to display UI, accept navigation, persist state, and survive sleep/wake.

Standard Library availability is defined by **Baga Lua Profile / Platform version** and validated by BICTS, not expressed as Device Capabilities.

The current SQLite Standard Library is loaded with:

```lua
require("lsqlite3")
```

---

## 4. Display Capabilities

```text
display.basic
display.partial_refresh
display.fast_refresh
display.quality_refresh
display.animation
display.grayscale
display.color
display.rotation
```

These describe semantic display behavior and do not expose waveform IDs.

---

## 5. Input Capabilities

```text
input.navigation
input.touch
input.multitouch
input.pen
input.pen.pressure
input.pen.eraser
input.pen.hover
input.pen.low_latency
input.physical_page_key
input.keyboard
input.volume_key
```

Universal Apps SHOULD prefer semantic actions such as `page_next`, `page_previous`, `confirm`, and `back` over raw key codes.

---

## 6. Network Capabilities

```text
network.available
network.wifi
network.http
network.https
network.connectivity_events
```

These indicate that the Platform can provide the corresponding networking behavior; they do not prescribe the internal HTTP/TLS library.

An Automerge sync protocol used by a product is Local-first data-sync behavior, not a network-hardware Capability.

---

## 7. Storage Capabilities

### `storage.app_sandbox`

The Platform can provide a protected logical sandbox for each App. Base Compatible devices MUST support it.

### `storage.user_library`

The Platform can bridge the device's user library through `baga.library`.

### `storage.user_files`

The Platform can provide user-selected/authorized file access.

### `storage.external`

Accessible external storage, for example an SD card, is present.

An App-local SQLite database inside the sandbox is a Standard Library use case and does not require a separate Device Capability.

---

## 8. Power Capabilities

```text
power.sleep_wake
power.battery_level
power.charging_state
power.keep_awake
```

---

## 9. Light Capabilities

```text
light.frontlight
light.frontlight.temperature
```

---

## 10. Audio Capabilities

```text
audio.output
audio.tts
audio.microphone
```

---

## 11. Bluetooth Capabilities

```text
bluetooth.available
bluetooth.input_device
bluetooth.audio
```

---

## 12. Reader Capabilities

Reader capabilities are higher-level Platform capabilities. The Device Adapter itself does not need to implement the entire Reader stack.

```text
reader.open
reader.search
reader.selection
reader.highlight
reader.note
reader.position
reader.anchor
```

Apps query Reader semantics, not implementation names such as KOReader, MuPDF, or CREngine.

### 12.1 `reader.anchor`

Indicates that the Reader can:

```text
create_anchor
serialize/pass an opaque anchor
goto_anchor
resolve_anchor
```

Semantics:

- not EPUB-specific;
- not PDF-specific;
- does not require all formats to share one underlying locator representation;
- implementations may reuse KOReader XPointer-like positions, PDF positions/boxes, or other mature mechanisms;
- Apps do not parse Reader-private fields;
- approximate recovery must be explicit and must not pretend to be exact.

`reader.anchor` remains **provisional** in v0.4 until multi-format Kindle/Android BICTS evidence exists.

---

## 13. Lifecycle Capability

```text
platform.lifecycle
```

Provides semantic lifecycle events:

```text
start
resume
pause
sleep
wake
stop
```

Base Compatible devices MUST satisfy this capability.

---

## 14. Capability lifecycle state

Registered Capabilities may be:

```text
experimental
provisional
stable
deprecated
removed
```

Once a Capability becomes stable, it should receive a reasonable compatibility/migration period before removal or incompatible change.

---

## 15. Capability registration process

Before adding a Capability:

```text
requirement appears
  ↓
is this merely a mature Standard Library problem?
  ├─ yes → handle under Standard 13
  └─ no → is it a real portable device/platform capability?
            ↓
       define vendor-neutral semantics
            ↓
       validate multiple device/implementation paths
            ↓
       register as experimental/provisional
            ↓
       API / Adapter / BICTS evidence
            ↓
       promote to stable when justified
```

Vendor-private API names, internal library names, and open-source project names must not directly become standard Capability names.

---

## 16. Vendor extensions

Before standardization, controlled private experimental naming MAY use:

```text
x.vendor.feature
```

Such names do not qualify for Universal stable certification.

---

## 17. v0.4 Registry summary

```text
Base
├─ display.basic
├─ input.navigation
├─ storage.app_sandbox
├─ power.sleep_wake
└─ platform.lifecycle

Display
├─ display.partial_refresh
├─ display.fast_refresh
├─ display.quality_refresh
├─ display.animation
├─ display.grayscale
├─ display.color
└─ display.rotation

Input
├─ input.touch
├─ input.multitouch
├─ input.pen
├─ input.pen.pressure
├─ input.pen.eraser
├─ input.pen.hover
├─ input.pen.low_latency
├─ input.physical_page_key
└─ input.keyboard

Network
├─ network.available
├─ network.wifi
├─ network.http
├─ network.https
└─ network.connectivity_events

Storage
├─ storage.user_library
├─ storage.user_files
└─ storage.external

Power
├─ power.battery_level
├─ power.charging_state
└─ power.keep_awake

Light
├─ light.frontlight
└─ light.frontlight.temperature

Audio
├─ audio.output
├─ audio.tts
└─ audio.microphone

Bluetooth
├─ bluetooth.available
├─ bluetooth.input_device
└─ bluetooth.audio

Reader
├─ reader.open
├─ reader.search
├─ reader.selection
├─ reader.highlight
├─ reader.note
├─ reader.position
└─ reader.anchor      provisional
```

---

## 18. Core rule

> **Capability Registry is a semantic contract for portable device/platform capabilities; it is not a registry of mature open-source libraries or implementation components.**

SQLite, Automerge, KOReader, and similar projects are governed respectively by Standard Library, Adopted Component, or Platform implementation boundaries.
