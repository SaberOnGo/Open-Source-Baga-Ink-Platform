# Baga Ink Compatibility Standard

> **Document level:** First-level Platform Standard  
> **Document ID:** `standards.08`  
> **Locale:** English (`en`)  
> **Status:** Draft v0.4  
> **Date:** 2026-08-23  
> **Parent:** `01_baga-ink-platform-strategy.md`  
> **Related:** Standards 04, 07, 10, 13  
> **Counterpart:** `docs/zh-CN/standards/08_兼容性标准.md`

---

## 0. Purpose

This document defines when a concrete Device / OS / Platform / Adapter combination may be called **Baga Ink Compatible**.

Compatibility is not proven merely because "LifeBook launches". Formal compatibility must validate, as applicable:

1. Platform Core;
2. Device Adapter;
3. truthful Capability declarations;
4. Baga Lua Profile;
5. mandatory Standard Libraries;
6. IKP behavior;
7. BICTS;
8. data safety and update/recovery behavior.

Core rule:

> **Hardware and internal libraries may differ, but the same Baga API / Lua Profile / Standard Library contract must hold.**

---

## 1. Scope

This Standard applies to Kindle, Android E-Paper, third-party Device Adapters, compatibility information presented by Baga Ink Client / Market, and future e-paper platforms.

It does not require every device to support Touch, Pen, Color, Audio, or Bluetooth. Those are expressed as Capabilities.

---

## 2. Compatibility levels

### 2.1 Baga Ink Compatible

Requires:

- all Base Mandatory Requirements satisfied;
- Baga Lua Profile passes the corresponding BICTS coverage;
- mandatory Stable Standard Libraries pass the corresponding BICTS coverage;
- Adapter and Capability declarations validated;
- Universal Reference Apps can run;
- installation/update has no known high-risk data-destruction behavior;
- minimum recovery requirements satisfied.

### 2.2 Compatible + Profile

A compatible device may additionally advertise profiles such as Touch, Pen, Fast Refresh, Color, Audio, or Bluetooth. Profiles do not create platform forks.

### 2.3 Experimental

The Platform runs, but formal certification requirements have not yet been fully met.

### 2.4 Unsupported

Includes combinations where Baga cannot be installed/launched reliably, core Display/Input/Storage cannot satisfy the contract, known high-risk data destruction exists, factory reset is required as a normal recovery path, or the minimum Platform/Lua Profile baseline cannot be implemented.

---

## 3. Base Compatibility Profile

A compatible device must satisfy:

```text
display.basic
input.navigation
storage.app_sandbox
power.sleep_wake
platform.lifecycle
```

and provide the mandatory Standard Libraries of the current Baga Lua Profile.

Current reference database baseline:

```text
require("lsqlite3")
+
a SQLite Profile conforming to Standard 13 / BICTS
```

SQLite/lsqlite3 are not Device Capabilities; they are Baga Lua Profile Standard Libraries.

Automerge is not a Base Mandatory Standard Library. It is an Adopted Foundation and is tested only where a concrete feature actually uses it.

---

## 4. Platform installation and startup

A compatible combination MUST allow Baga Platform to be installed, provide a user-understandable launch path, preserve state across reboot, load standard IKPs, and recover usable Platform behavior after an App crash.

Installation mechanisms may differ by device; the App contract must not.

---

## 5. User-data safety

Install / update / repair workflows MUST:

- not delete user books;
- not delete user notes;
- not delete user documents by default;
- not require factory reset as the normal solution;
- preserve the last known working state after failure where the Standard requires recovery;
- not delete App-private SQLite databases merely because Platform/App packages update;
- not leave half-migrated data after SQLite migration/rollback failure.

Any known Critical data-loss defect blocks a Compatible claim.

---

## 6. IKP consistency

The same Universal IKP:

- does not change package contents by device brand;
- does not ship separate Kindle/Android business packages;
- does not carry device-private execution bridges;
- preserves the same business semantics when Capabilities are equivalent;
- may rely on mandatory Baga Lua Profile Standard Libraries provided by Platform instead of bundling them into every IKP.

---

## 7. API / Lua Profile / Standard Library baseline

A compatible Platform MUST implement the Mandatory API Surface and Baga Lua Profile declared by its version.

The following distinction remains mandatory:

```text
device / OS capability
→ baga.* / Capability

mature general-purpose library
→ Baga Lua Profile Standard Library
```

Current SQLite baseline:

```text
lsqlite3 API-compatible module
Platform-managed SQLite runtime
pinned version / compile options
sandbox-safe file access
```

---

## 8. Capability truthfulness

Capability declarations must be true, stable enough for the declared compatibility range, and testable.

Forbidden practices include:

- inheriting capability from another model without evidence;
- using marketing specifications as a substitute for runtime/device testing;
- leaving a Capability true when firmware makes it unusable;
- registering implementation/library names such as SQLite, Automerge, or KOReader as Capabilities.

---

## 9. Storage / SQLite sandbox compatibility

Platform MUST provide App sandbox roots:

```text
appdata/
cache/
documents/
downloads/
```

For the SQLite Standard Library:

### Android / strong OS sandbox

The implementation may primarily rely on the OS application sandbox plus Baga private-path mapping.

### Kindle / weak OS sandbox

The implementation must prove, through a sandbox-aware SQLite VFS or equivalent I/O confinement, that SQLite cannot escape the current App's authorized roots.

At minimum test:

```text
main DB
ATTACH DB
journal
WAL
SHM
temporary DB
URI vfs override
symlink / canonical path escape
loadable extension
```

A legal `resolve_path()` result alone is not sufficient evidence of SQLite sandbox compatibility.

---

## 10. Display compatibility

The Adapter MUST provide screen dimensions, orientation, basic refresh behavior, and any declared enhanced display capabilities.

Apps express only semantic refresh intents:

```text
AUTO / TEXT / QUALITY / FAST / ANIMATION
```

Vendor/private waveform IDs are not part of the App contract.

---

## 11. Input compatibility

Core navigation actions include:

```text
confirm
back
menu
page_next
page_previous
```

A device MAY provide touch, pen, keyboard, or physical buttons. Apps do not depend on platform-private keycodes.

---

## 12. Lifecycle / power

Platform must provide consistent semantic mapping for:

```text
start / resume / pause / sleep / wake / stop
```

Committed SQLite transactions must remain reliable across sleep/restart after the normal durability boundary.

Power requests may be rejected by Platform policy.

---

## 13. Network compatibility

Network capability is not a Base hardware requirement.

When network capability is declared, the Platform MUST correctly represent online/offline state, use Baga Network API semantics, handle sleep/wake/reconnect, and normalize DNS/TLS/timeout failures as defined by the relevant API/test standards.

An Automerge sync protocol, when used by a product, is not itself a network Capability.

---

## 14. Reader compatibility

If a Platform declares `reader.open`, `reader.anchor`, or related Reader capabilities, it must pass the corresponding BICTS coverage.

Reader compatibility:

- is not EPUB-only;
- may internally reuse KOReader / MuPDF / CREngine;
- may use mature native locator formats per document type;
- does not expose Reader-private objects to Apps.

---

## 15. Automerge compatibility

Automerge core is an Adopted Local-first Foundation, not a Base Compatible mandatory component.

Only Platform/App features that actually use Automerge run the corresponding tests, for example:

```text
document / merge
binary persistence
history
sync protocol (if adopted)
```

Baga may adopt Automerge as a whole or by selected modules. `automerge-repo` is not mandatory.

---

## 16. Optional Capability Profiles

Typical optional profiles include:

```text
Touch       → input.touch
Pen         → input.pen
FastRefresh → display.fast_refresh
Color       → display.color
Audio       → audio.output
Bluetooth   → bluetooth.available
```

If a Capability is declared, it must be tested.

---

## 17. Performance / resource constraints

Compatible devices do not need identical CPU, RAM, or storage, but they must run the required Reference Apps and mandatory SQLite Profile reliably within the supported configuration.

Non-Base components such as Automerge may be omitted from low-resource devices/features if their resource cost is inappropriate. This must not break Base Compatibility.

---

## 18. Upgrade / recovery

Formal Compatible devices must support the staged update / verify / activation / rollback model required by the update standards.

App package bytes and App-private data/SQLite databases remain separate.

---

## 19. Security baseline

A Compatible Platform must:

- validate IKP before execution;
- enforce App sandboxing;
- enforce Permission checks;
- prevent arbitrary shell access from Universal Apps;
- prevent direct Vendor API passthrough to Apps;
- prevent SQLite path/VFS/extension sandbox escape;
- safely handle malicious/corrupt IKPs;
- prevent an App crash from corrupting Platform integrity.

---

## 20. BICTS

Formal certification must be based on the corresponding version of BICTS.

A test report binds at least:

```text
Device / Firmware
Platform
Adapter
Lua Profile
SQLite / lsqlite3 baseline
Compatibility Standard
BICTS
```

---

## 21. Reference Apps

Baga SHOULD maintain a small Probe app and LifeBook as Reference Apps.

LifeBook is not the sole certification criterion.

Reference smoke coverage should include, as applicable:

```text
offline start
SQLite read/write/transaction
Reader behavior when declared
sleep/wake
update/recovery
```

---

## 22. Firmware / OS dimension

Compatibility is a tuple such as:

```text
Device Model
+ OS/Firmware Range
+ Platform Version
+ Adapter Version
+ Lua Profile Version
+ BICTS Version
```

Different firmware on the same model may independently be Compatible, Experimental, or Unsupported.

---

## 23. Client / Market presentation

Baga Ink Client should present user-facing states:

```text
Compatible
Experimental
Unsupported
```

Market install decisions use Manifest + Capability + API/Profile compatibility + Compatibility Status rather than a simplistic model-name whitelist.

---

## 24. Certification artifact

A Compatibility report SHOULD contain structured data such as:

```json
{
  "device_family": "kindle",
  "model": "example",
  "firmware_range": ">=x <y",
  "baga_platform": "0.x",
  "adapter_version": "0.x",
  "lua_profile": "0.x",
  "sqlite_version": "...",
  "lsqlite3_version": "...",
  "compatibility_standard": "0.4",
  "bicts": "0.x",
  "status": "compatible",
  "profiles": []
}
```

---

## 25. Final principle

> **Baga Ink Compatible means a developer may trust the stable `baga.*` API, Baga Lua Profile, and mandatory Standard Libraries without learning the device's private implementation.**

Whether the Platform internally uses KOReader, SQLite, Automerge, FBInk, vendor SDKs, or other mature components does not change that definition.
