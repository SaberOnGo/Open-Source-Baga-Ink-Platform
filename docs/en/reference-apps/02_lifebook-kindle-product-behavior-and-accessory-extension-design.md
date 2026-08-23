# LifeBook for Kindle Product Behavior and Accessory Extension Design

> **Document level:** LifeBook Reference App Supplemental Design Note  
> **Document ID:** `reference-apps.02`  
> **Locale:** English (`en`)  
> **Status:** Design Baseline v0.1  
> **Date:** 2026-08-23  
> **Applies to:** LifeBook for Kindle on Baga Ink Platform  
> **This is not a Baga Ink Standard and cannot override governing Standards.**  
> **Counterpart:** `docs/zh-CN/reference-apps/02_LifeBook-Kindle产品行为与外设扩展设计.md`

---

## 0. Purpose

This note captures valuable product/implementation design conclusions from LifeBook for Kindle work, especially:

- LifeBook's relationship to Baga Ink Client / Market;
- low-refresh, low-power Kindle UI behavior;
- Wi-Fi/network-use strategy;
- progressive Audio / Bluetooth enhancement;
- intelligent accessories / magnetic docks for older Kindles;
- candidate accessory transports and validation boundaries;
- later prototyping and standardization paths.

It describes **LifeBook product behavior, reference-implementation recommendations, and experimental product directions** only.

Any new capability with cross-App / cross-device value must go through Baga Standards governance before becoming Capability / Permission / API / Device Adapter / Compatibility surface. LifeBook must not create a private long-term platform interface.

---

## 1. Governing hierarchy

This design follows the localized Baga Standards, especially App/API/Capability/Permission/IKP/Device Adapter/Compatibility/UI/BICTS/Kindle Adapter/Distribution/Offline Transfer, plus the LifeBook Reference App.

Authority remains:

```text
Baga Ink Standards
        >
LifeBook Reference App
        >
this supplemental design
        >
product prototypes / implementation
```

This document does not define new `baga.*` APIs, Capability names, Permissions, IKP format, or Device Adapter Contract.

---

## 2. Core architecture conclusions

### 2.1 LifeBook is not a Runtime

LifeBook is the flagship Reference App on Baga Ink Platform, not an independent Runtime, SDK, or compatibility layer.

```text
LifeBook (lifebook.ikp)
        │
        ▼
     baga.*
        │
        ▼
Baga Ink Platform Core
        │
        ▼
Baga Ink Device Adapter
        │
        ▼
      Kindle
```

Do not reintroduce:

```text
LifeBook Runtime
private long-lived LifeBook Kindle API
LifeBook-owned Device Adapter
LifeBook-owned heavyweight execution environment
```

KOReader, Lua/LuaJIT, FBInk, KUAL/MRPI, and other Homebrew components used on Kindle remain Platform / Adapter implementation choices, not LifeBook App Contract.

### 2.2 Installation and Market do not belong to LifeBook

Generic capabilities once discussed as a “LifeBook Installer for Kindle” belong to:

```text
Baga Ink Client
├── device identification
├── installation-route selection
├── Platform installation
├── compatibility check
├── IKP transfer
└── management / diagnostics

Baga Ink Market
├── app discovery
├── install entry
├── update entry
└── third-party app ecosystem
```

LifeBook may be the flagship/recommended/reference app but should not turn Client or Market into LifeBook-private subsystems.

### 2.3 Open ecosystem

Third-party developers target:

```text
Baga Ink App Standard
Baga Ink SDK / API
IKP
Capability / Permission
```

not LifeBook.

Existing Kindle Homebrew projects may be reused inside Platform or later integrated through controlled bridges, but arbitrary Shell/KUAL/native Homebrew packages do not become standard Baga Apps merely because they run on Kindle.

---

## 3. Kindle UI: event-driven, not continuously refreshed

### 3.1 Product rule

LifeBook for Kindle SHOULD use an **event-driven static UI**.

```text
user action / data change
        ↓
update required UI state
        ↓
submit minimal Dirty Region
        ↓
express Refresh Intent
        ↓
Platform / Adapter chooses physical refresh
        ↓
screen becomes static again
```

Avoid:

```text
continuous UI loops
high-frequency redraw timers
phone-style loading spinners
gradient / movement animation
continuous skeleton animation
meaningless full-screen refresh
```

LifeBook does not choose Kindle waveform IDs or implement its own “full refresh every N updates” policy. Ghosting / partial refresh / quality refresh / waveform mapping belong to Platform / Kindle Adapter.

### 3.2 AI streaming output

AI token streaming is a high-refresh-risk case. LifeBook SHOULD batch visible updates instead of refreshing per token.

Initial product tuning range:

```text
LLM token stream
      ↓
memory buffer
      ↓
visible update when either:
- about 20–50 Chinese characters accumulated; or
- about 500–1000 ms since previous visible update
      ↓
update only the answer region
```

These values are LifeBook tuning parameters, not a Baga Standard.

Slower devices can batch more; devices with `display.fast_refresh` / `display.animation` may progressively enhance behavior.

When a response completes, LifeBook expresses that content is stable / quality is desired; Platform decides whether a quality refresh is needed.

### 3.3 Long lists and articles

Articles, Q&A, comments, library views, and search results SHOULD:

- prefer paging or step-scroll;
- avoid inertial continuous scrolling as the only mode;
- virtualize long lists;
- update only the focus region when focus changes;
- use `page_next` / `page_previous` semantic actions;
- not make touch the only interaction path.

---

## 4. Wi-Fi/network: short active windows + offline-first

### 4.1 Why phone-style always-online behavior is wrong

Kindle battery life depends on static E-Ink display, system sleep, and low wireless activity.

LifeBook SHOULD NOT default to:

```text
permanent WebSocket
frequent heartbeat
high-frequency background polling
keeping Wi-Fi active only for instant notification
continuous keep-awake
```

### 4.2 Recommended network model

```text
LifeBook open / wake
      ↓
Platform reports connectivity
      ↓
batch necessary synchronization
├── reading progress
├── notes
├── article/comment cache
├── queued user operations
└── required metadata
      ↓
continue local reading/editing
      ↓
network becomes idle
      ↓
allow normal low-power Platform policy
```

LifeBook uses standard Network / Lifecycle / Sync capabilities rather than directly controlling Kindle Wi-Fi drivers.

### 4.3 Cases that may stay online while active

- AI conversation;
- user-triggered community refresh;
- large-file download;
- explicit sync;
- login/authorization.

Release unnecessary connections and keep-awake requests when the active operation ends.

### 4.4 Offline-first

Without Wi-Fi, core experience SHOULD still support:

```text
local library
reading
reading position
cached articles
local notes
Life Records
Time Capsule drafts
queued operations
```

User actions are durably stored locally before entering the sync queue.

---

## 5. Audio / Bluetooth: progressive enhancement only

Kindle generations differ substantially. LifeBook MUST NOT assume all Kindles have Bluetooth, Bluetooth input, audio output, or microphones.

Only query standard capabilities:

```text
audio.output
audio.tts
audio.microphone
bluetooth.available
bluetooth.audio
bluetooth.input_device
```

If `audio.output` exists, possible enhancements include book/article TTS, AI answer reading, audio content, and word pronunciation.

If `audio.microphone` exists, possible enhancements include voice search, AI voice input, and voice notes.

Absent capabilities mean hidden/degraded features, not fake hardware emulation.

---

## 6. Intelligent accessory / magnetic dock direction

### 6.1 Goal

A useful research direction is:

> **Use an external Dock / Accessory to add modern interaction to older Kindles, turning inexpensive installed-base devices into extensible low-power E-Ink terminals.**

```text
               Kindle
        ┌─────────────────┐
        │ Baga Ink        │
        │ + LifeBook      │
        └────────┬────────┘
                 │ Data / Power
        ┌────────▼────────┐
        │ Accessory Dock  │
        │ Buttons         │
        │ Speaker         │
        │ Microphone      │
        │ Battery         │
        │ Wi-Fi optional  │
        │ BLE optional    │
        │ Sensors optional│
        └─────────────────┘
```

Magnets solve **mechanical attachment/alignment only**. Data communication and power are separate engineering problems.

### 6.2 Accessory is not a LifeBook base dependency

LifeBook Base Experience MUST work without the Dock.

```text
No Dock → normal reading/basic features
Dock    → optional input/audio/network/power enhancements
```

---

## 7. Candidate accessory transports

No candidate is a formal Baga Accessory Standard at this stage.

### 7.1 Bluetooth / BLE

Benefits: wireless, low-power, suitable for buttons/remotes/small data, low hardware cost.

Limitation:

> **Many older Kindles do not expose usable Bluetooth to the Platform; BLE cannot be the sole cross-generation Kindle foundation.**

Correct consumption remains capability-based, e.g. `bluetooth.input_device`. LifeBook must not make a private GATT UUID a long-term cross-device contract.

If Baga later standardizes an accessory protocol, it enters Experimental / Optional Extension governance first.

### 7.2 USB: strongest cross-generation research candidate

USB hardware is widespread across Kindle generations, but physical USB presence does not prove the required host/device role or protocol.

Two architectures need separate validation.

#### A. Kindle as USB Host

```text
Kindle USB Host
      ↓
Accessory USB Device
```

Could suit HID, serial, or custom devices. Risks include controller/kernel differences, OTG/Host inconsistency, unknown power capability, and suspend/resume enumeration differences.

No family-wide assumption is allowed.

#### B. Dock as USB Host, Kindle as USB Device

```text
Accessory Dock / Host
          ↓
       Kindle USB Device
```

This deserves priority because Kindle already has a long-standing PC USB product path.

Research must determine whether a jailbroken Platform can safely/reliably expose or reuse controlled channels such as:

```text
USB network-like channel
USB serial-like channel
controlled gadget interface
other verified transport
```

These are candidates, not established facts.

If feasible, the Dock could own more modern hardware functions:

```text
Internet → Wi-Fi → Dock → USB data → Kindle
```

Kindle then primarily provides E-Ink display, local input, storage, Baga Ink Platform, and LifeBook, while Dock can provide Wi-Fi/BLE, microphone, speaker, physical buttons, battery, and sensors.

### 7.3 Capacitive-touch simulation

A low-level compatibility route could use a standalone remote plus touch simulator at the screen edge:

```text
Remote → RF → Touch Simulator → Kindle Screen
```

Benefits: no Kindle Bluetooth dependency and no Baga Platform dependency.

Limitations: essentially simulated taps, almost no bidirectional data, unsuitable for AI/microphone/network/semantic accessory functions.

This is a page-turner-like fallback, not the core intelligent-accessory architecture.

---

## 8. Correct LifeBook/accessory software boundary

Even if a Dock prototype succeeds, LifeBook SHOULD NOT see:

```text
USB packet
BLE manufacturer data
/dev/input/eventX
Dock GPIO
vendor-specific command
```

It should continue seeing semantic actions:

```text
page_next
page_previous
confirm
back
menu
```

or standard Capabilities:

```text
audio.output
audio.microphone
network.available
power.charging_state
input.keyboard
```

Ideal layering:

```text
LifeBook
   ↓ baga.* / semantic actions
Baga Ink Platform
   ↓
Device Adapter / future Accessory Provider
   ↓
USB / BLE / HID / other transport
   ↓
Accessory hardware
```

If existing Capabilities cannot describe a new accessory feature:

```text
real prototype requirement
→ prove cross-device / cross-App value
→ Capability registration process
→ Experimental / Provisional
→ API / Adapter / Test
→ then LifeBook uses it
```

LifeBook does not bypass Standards with a private implementation.

---

## 9. LifeBook Dock Mini prototype

First prototype SHOULD stay small and validate high-value fundamentals first.

```text
LifeBook Dock Mini

Mechanical
├── magnetic / stand structure
└── Kindle alignment

Input
├── Previous / Next
├── Up / Down
├── Confirm
└── optional AI shortcut

Audio
├── small speaker optional
└── microphone experimental

Connectivity
├── USB data candidate
├── BLE optional
└── Wi-Fi optional

Power
├── Dock battery optional
├── USB-C input
└── Kindle charging path to verify
```

Priority:

```text
1 reliable button input
2 automatic reconnect after sleep/wake
3 stable USB communication
4 audio output
5 charging + data coexistence
6 microphone
7 Dock independent networking
```

Do not implement everything in v1.

---

## 10. Desktop E-Ink terminal scenario

Dock should be more than a page-turn remote.

Potential dashboard:

```text
Reading Dashboard
├── current reading
├── articles
├── Todo
├── calendar summary
├── cached weather
└── AI / TTS
```

Value: static E-Ink, low distraction, long battery, reuse of old hardware, externalized modern input/audio/network.

But it must avoid second-hand ticking clocks, continuous animation, or high-frequency updates that destroy E-Ink's power model.

---

## 11. Open accessory ecosystem direction

Longer-term possibilities:

```text
Page Remote
Keyboard
Foot Pedal
Audio Dock
Microphone Dock
Desktop Stand
Charging Dock
Sensor Accessory
```

Do not publish an unvalidated “Baga Ink Accessory Protocol” now.

Recommended path:

```text
LifeBook prototype validation
→ at least two implementations prove abstraction value
→ Baga Ink Experimental Extension proposal
→ Capability / Permission / Transport abstraction
→ test Profile
→ mature into Optional Extensions
```

This avoids creating a LifeBook-private protocol that third parties later depend upon and that becomes impossible to evolve.

---

## 12. Kindle accessory research matrix

Before a formal Dock, establish a real model matrix rather than extrapolating from one Kindle.

Record at least:

```text
Model / Firmware
CPU / Kernel
USB connector
USB Device modes/stability
USB Host / OTG support, power, drivers
USB gadget functions/kernel support
Data + Charging coexistence
Bluetooth available/input/audio
Audio output
Microphone
Wi-Fi sleep/wake behavior
Power events on Dock attach/detach
Suspend/Resume transport recovery
Homebrew foundation
```

First prototypes should cover at least a representative older Kindle, a mid-generation Paperwhite, and a newer USB-C Kindle. One successful model is not family-wide support evidence.

---

## 13. Accessory security principles

A smart Dock could gain input control, network, microphone, file transfer, power, and firmware update. Treat it as an untrusted external device by default.

Future platform-level design must consider:

```text
Accessory identity
pairing / trust
Permission boundary
firmware authenticity
USB attack surface
malicious HID
network-bridge isolation
microphone privacy
update / revocation
```

Detecting a Dock must not automatically grant microphone, network, file, or system permission.

These security mechanisms require separate platform standardization if they become public; this document does not define the protocol.

---

## 14. Product phases

### Phase A — software-only low-power experience

```text
LifeBook Universal IKP
event-driven Kindle UI
AI stream batching
offline-first
low-frequency networking
sleep/wake recovery
Capability-driven Audio / Bluetooth UI
```

No accessory dependency.

### Phase B — accessory feasibility research

Build Kindle Hardware Matrix; validate USB roles/transport, sleep/wake, charging+data, and Bluetooth differences.

### Phase C — Dock prototype

On a small set of representative devices validate physical buttons, bidirectional transport, reconnect after wake, optional audio.

### Phase D — enhanced prototype

Test microphone, Dock Wi-Fi, external battery/charging, sensors.

### Phase E — platformization review

Only cross-App / cross-device proven capabilities become Experimental / Optional Extension proposals.

---

## 15. Acceptance / stop criteria

### 15.1 LifeBook software experience

SHOULD verify:

- static pages do not refresh periodically without cause;
- AI streaming does not refresh per token;
- long reading does not require permanent Wi-Fi;
- local content remains usable offline;
- sleep/wake restores reading and queued sync state;
- no-Bluetooth devices do not expose Bluetooth-required flows;
- no-Audio devices retain core reading functionality.

### 15.2 Dock prototype

Test attach/detach, Kindle sleep/wake, Dock power cycle, interrupted transfer, low battery, communication while charging, Platform restart, App restart, different firmware, malicious/abnormal input, and preservation of Kindle user data after failure.

### 15.3 Stop standardization when

A candidate:

```text
works only on a tiny set of single models
requires LifeBook to call Kindle private system APIs directly
requires disabling Baga Permission / Sandbox
frequently deadlocks after sleep/wake
creates a high risk of unrecoverable device failure
```

Such a solution must not be promoted to public Baga capability just to ship a product feature.

---

## 16. Established conclusions vs unverified hypotheses

### Established design conclusions

```text
LifeBook is not a Runtime.
LifeBook is a Baga Ink Reference App.
Installation/Market capabilities belong to Baga Ink Client / Market.
Kindle UI should be event-driven and low-refresh.
LifeBook should be offline-first with low-frequency networking.
AI token streams should be batched before display refresh.
Do not assume every Kindle has Bluetooth / Audio.
Accessory capabilities reach Apps through Capability / semantic actions.
Magnetic attachment is mechanical, not data transport.
LifeBook Base Experience does not depend on Dock.
```

### Unverified and MUST NOT be treated as facts

```text
whether a specific Kindle supports USB Host / OTG
whether a specific kernel supports the desired gadget function
whether Dock Host ↔ Kindle Device is a stable general transport
whether USB Data + Charging coexist across generations
whether an external Dock can reliably network-bridge Kindle
which Kindles can reliably use USB Audio / HID
whether there is enough cross-device value for a Baga Accessory Standard
```

These require real hardware tests.

---

## 17. Non-goals

This document does not define a new Baga Standard/API/Capability/Permission, USB Accessory Protocol, BLE GATT Protocol, Dock firmware protocol, Kindle jailbreak method, Kindle kernel modification, new Market/Repository rule, or a `Baga Ink Compatible Accessory` certification mark.

Any such work starts only after prototype evidence and normal Standards governance.

---

## 18. Final product principle

> **LifeBook for Kindle should not try to turn Kindle into a low-refresh Android tablet. It should respect Kindle's E-Ink, sleep, and offline characteristics, then progressively enhance them through Baga Ink's unified capability model.**

For accessories:

> **Validate transport and hardware value on real Kindles first; only then abstract reusable capability into a Baga extension. Do not invent a protocol first and search for a use case later.**
