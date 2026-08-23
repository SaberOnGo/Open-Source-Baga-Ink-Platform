# Baga Ink App Standard

> **Document level:** First-level platform standard  
> **Document ID:** `standards.02`  
> **Locale:** English (`en`)  
> **Status:** Draft v0.6  
> **Date:** 2026-08-23  
> **Parent:** `01_baga-ink-platform-strategy.md`  
> **Related:** Standards 03, 04, 05, 06, 09, 13  
> **Counterpart:** `docs/zh-CN/standards/02_应用标准.md`

---

## 0. Purpose

This document defines how a third-party application becomes a **Baga Ink App** and under what conditions it may claim **Baga Ink Universal** compatibility.

The primary objective is not to expose the maximum possible device capability. It is to establish a durable cross-device application boundary so that the ecosystem does not fragment again as device coverage grows.

This Standard constrains application developers. Device vendors and Platform/Adapter implementers are governed by the Device Adapter and Compatibility standards.

`MUST`, `SHOULD`, and `MAY` inherit their normative meanings from Standard 01.

Active text describes only the current approved design; Git preserves historical proposals.

---

## 1. Application categories

Baga Ink defines three application/extension classes.

### 1.1 Baga Ink Universal App

Universal App is the default, preferred, and most important application form.

A Universal App MUST:

- use Baga Lua Profile;
- be distributed as `.ikp`;
- obtain device / OS / Platform capabilities only through public Baga Ink APIs;
- MAY directly use official Baga Lua Profile Standard Libraries;
- use the Capability Model to detect hardware/platform capability;
- follow the standard lifecycle;
- obey Permission and Sandbox rules;
- not call Vendor / OS private APIs directly;
- not carry platform-specific native binaries as normal application business logic;
- not carry a device-specific Lua interpreter, private bridge, Device Adapter, or Platform Core;
- not require separate Kindle / BOOX / iReader business-logic branches.

An app that satisfies all requirements and passes the required compatibility validation MAY be labeled:

> **Baga Ink Universal**

### 1.2 Device Enhanced App

A Device Enhanced App still uses Baga Ink API as its primary boundary but MAY use standardized optional/extended Capabilities exposed by the Platform.

Examples:

```text
input.pen.low_latency
display.fast_refresh
audio.tts
```

An Enhanced App MUST:

- declare required and optional Capabilities;
- degrade gracefully when optional capabilities are absent;
- not bypass the Platform to call a vendor SDK directly;
- clearly disclose the enhanced requirements/range in Baga Ink Market.

### 1.3 Native Extension / Capability Provider

Native Extensions add Platform capability; they are not escape hatches for ordinary Universal Apps.

A Native Extension MAY use:

- Rust;
- C / C++;
- Kotlin / Java;
- JNI;
- Kindle native / shell integration;
- Vendor SDKs.

The Platform must re-expose relevant behavior as controlled standardized capabilities/APIs.

Using a mature open-source library internally does not by itself create a Native Extension or imply that every library requires a Capability Provider. Platform Core / Adapter implementations may directly compose or selectively reuse mature components.

---

## 2. Application identity

Every Baga Ink App MUST have a globally stable Application ID.

Recommended form:

```text
com.example.reader
org.example.notes
```

The Application ID:

- MUST remain under long-term publisher control;
- MUST remain stable across updates;
- MUST NOT be forced into the `baga.*` namespace;
- MUST NOT vary by device;
- SHOULD be associated with a namespace/domain controlled by the developer.

---

## 3. Version and compatibility declaration

Application versions SHOULD use semantic form:

```text
MAJOR.MINOR.PATCH
```

The IKP Manifest MUST declare:

- app version;
- IKP format version;
- required Baga Ink API range;
- required Capabilities;
- optional Capabilities.

The Platform MUST perform compatibility checks before launching the app.

Standard Library versions are pinned/provided by the Baga Platform / Lua Profile and do not require every IKP to bundle another native copy.

---

## 4. Baga Lua Profile

Lua is the first official Universal App language, but apps target **Baga Lua Profile**, not an arbitrary Lua environment.

Baga Lua Profile defines the language, Standard Libraries, and public API boundary; it is not a separate user-installed product layer.

Platform Core MAY:

- reuse a proven Lua/LuaJIT environment on Kindle;
- embed a lightweight Lua interpreter on Android;
- replace the underlying Lua implementation later if Baga Lua Profile compatibility remains intact.

Apps MUST NOT depend on the concrete interpreter brand, build, or device implementation.

### 4.1 Baseline language libraries

A safe portable profile SHOULD expose appropriate libraries such as:

```text
string
table
math
utf8
coroutine
```

The exact Lua language baseline is versioned by the SDK/Profile.

### 4.2 Adopted Standard Libraries

Baga does not require every general-purpose capability to be wrapped behind `baga.*`.

When an upstream library already provides a mature, stable, cross-platform abstraction, Baga MAY adopt it directly as part of Baga Lua Profile Standard Libraries.

Current database Standard Library:

```lua
local sqlite3 = require("lsqlite3")
```

Developers use normal SQLite concepts directly:

```text
SQL
schema
prepared statements
transactions
indexes
foreign keys
BLOB
FTS
JSON
```

Baga does not reinvent SQLite as a proprietary KV/collection API.

Automerge core is the adopted preferred Local-first / CRDT foundation and MAY be used as a whole or by selected document/merge, binary persistence, sync, C FFI, patch/cursor modules. The developer-facing Lua binding remains provisional and is not yet a stable public module.

Standard 13 defines the detailed policy.

### 4.3 System escape capabilities are restricted

Universal Apps MUST NOT rely on unrestricted facilities such as:

```text
os.execute
io.popen
raw shell
raw process spawn
filesystem access outside sandbox
Android Context
Java reflection
direct JNI
Kindle private frameworks
raw framebuffer
direct vendor SDK
/proc
/sys
```

Dangerous parts of Lua libraries such as `os`, `io`, `package`, and `debug` MAY be removed, replaced, or restricted by the Platform.

An app must not assume the complete desktop-Lua standard library exists.

SQLite loadable native extensions must not become a route around IKP native-code / sandbox restrictions.

---

## 5. Application lifecycle

Baga Apps MUST use a common semantic lifecycle.

Initial events:

```text
install
start
resume
pause
sleep
wake
stop
update
uninstall
```

Apps MUST:

- persist necessary state quickly before `sleep`;
- not assume permanent network connectivity;
- not assume the process is permanently resident;
- not depend on Android Activity or Kindle-private process semantics;
- re-evaluate network/runtime state after `wake` where necessary.

A Platform MAY collapse lower-level OS events due to device constraints, but the semantic events exposed to Apps must remain consistent.

---

## 6. Capability Model

### 6.1 Core rule

Apps MUST ask **what the device/platform can do**, not **which brand/implementation it is**.

Recommended:

```lua
if baga.device.has("input.pen") then
    enable_pen_ui()
end

if baga.device.has("reader.anchor") then
    enable_anchor_navigation()
end
```

Not recommended:

```lua
if device.vendor == "BOOX" then ... end
if reader_impl == "KOReader" then ... end
```

SQLite / lsqlite3 is not a device Capability; it is a Baga Lua Profile Standard Library.

### 6.2 Required Capability

If an app cannot function without a capability, it must declare that capability as required in the Manifest.

The Platform MUST report incompatibility before normal execution rather than allowing unpredictable runtime failure.

### 6.3 Optional Capability

Capabilities that enhance experience but are not essential should be declared optional.

Apps MUST provide reasonable fallback behavior when optional capabilities are absent.

---

## 7. Permission Model

Capability and Permission are different:

- **Capability**: can this device/platform provide the mechanism?
- **Permission**: may this app use the resource/user data?

Example:

```text
Capability: network.wifi
Permission: network
```

Initial Permission families MAY include:

```text
network
library.read
library.write
notes.read
notes.write
clipboard
user_files.read
user_files.write
audio.output
bluetooth
```

Permissions MUST be declared in the Manifest. Platform SHOULD follow least privilege.

An app MUST NOT bypass undeclared permissions through another mechanism.

An app's own SQLite database inside its private sandbox does not require a separate user-data permission.

---

## 8. Storage, SQLite, Library, and sandbox

Every App MUST have an independent logical sandbox.

Logical roots:

```text
appdata/
cache/
documents/
downloads/
```

Applications must distinguish:

```text
baga.storage
→ files / byte resources / logical paths / sandbox bridge

lsqlite3 / SQLite
→ the app's structured relational database

baga.library
→ permission-controlled user library/document resources
```

An App:

- MUST NOT assume Android/Kindle physical paths;
- MUST NOT scan system directories directly;
- SHOULD use `baga.storage` for files/bytes;
- SHOULD use `lsqlite3` / SQLite directly for structured relational data;
- MUST use `baga.library` plus `library.read/write` permissions for user-library access;
- MUST NOT make a vendor bookshelf/private database part of the Universal contract.

A thin path bridge MAY expose an authorized physical/runtime path to a Standard Library:

```lua
local sqlite3 = require("lsqlite3")
local path = baga.storage.resolve_path("appdata/app.sqlite3")
local db = sqlite3.open(path)
```

`resolve_path()` only maps an already-authorized logical path safely; it does not wrap or replace SQLite.

Uninstall policy SHOULD distinguish disposable cache, app private data/databases, and user-created documents that may need retention.

---

## 9. Network, offline-first, SQLite, and Automerge

E-paper devices frequently operate offline or connect infrequently. Baga Apps SHOULD be designed offline-first.

Apps MUST:

- handle offline state correctly;
- not require network connectivity for normal startup unless their declared product purpose truly requires it;
- avoid continuous high-frequency polling;
- persist confirmed local user actions before waiting for sync where practical;
- not corrupt local data when sync fails;
- use Baga network/sync mechanisms instead of device-private network interfaces.

Responsibilities must remain distinct:

```text
SQLite / lsqlite3
→ local relational data, transactions, queries, indexes, FTS, cached metadata

baga.sync
→ sync triggering/scheduling under network/power/lifecycle policy

Automerge core (when applicable)
→ concurrent offline edits, CRDT merge, change history, optional sync protocol

App business policy
→ authoritative ownership, object identity, product/version semantics
```

For data that genuinely requires concurrent offline editing, implementations SHOULD prefer Automerge core over inventing a generic CRDT.

Adoption MAY use the full core or selected capabilities:

```text
document / merge / history
Automerge binary persisted as SQLite BLOB
Automerge sync protocol
Rust core / automerge-c bridge
patch / cursor support
```

Do not mechanically use CRDTs for every data type. Examples:

```text
Reading Position
→ simple business merge

Feed / Comments / Public Notes
→ server authoritative + local SQLite cache

Book Files
→ content hash + file transfer

Notes / Life Records / Drafts
→ Automerge candidate only when true concurrent editing is required
```

Long-running tasks SHOULD support retry, cancellation, and recovery across sleep/wake where appropriate.

---

## 10. UI and e-paper behavior

App UI SHOULD treat e-paper constraints as first-class design requirements.

Apps SHOULD:

- use high-contrast interfaces;
- avoid meaningless animation;
- avoid continuous scrolling animation;
- avoid large high-frequency repaint;
- use reasonable touch targets;
- support semantic physical page-key mappings;
- remain operable without touch when the app claims support for non-touch devices;
- let Platform choose the actual waveform/vendor refresh mechanism.

Apps MAY express refresh **intent** but MUST NOT directly control vendor-private refresh APIs.

---

## 11. Display rules

An App MAY request semantic intents:

```text
AUTO
TEXT
QUALITY
FAST
ANIMATION
```

These are semantic modes, not hardware waveform IDs.

Platform / Device Adapter maps them to Kindle, generic Android, BOOX/iReader, or other device mechanisms.

Apps MUST NOT assume every device supports the same mode with the same fidelity.

---

## 12. Input rules

Apps SHOULD design around semantic actions:

```text
page_next
page_previous
confirm
back
menu
```

rather than hard-coding physical key codes.

The Platform maps touch, pen, physical page keys, keyboard, and (where allowed) volume keys into the common input model.

---

## 13. Power rules

Universal Apps MUST respect low-power e-paper goals.

Apps:

- MUST NOT keep the device awake without justification;
- MUST NOT continuously wake in the background;
- SHOULD align sync work with Wi-Fi / charging policy where appropriate;
- MUST handle sleep/wake correctly;
- MUST request keep-awake through Baga power APIs rather than changing OS power state directly.

The Platform MAY reject unreasonable keep-awake requests.

---

## 14. Reader capability

Apps that need reading features SHOULD use Baga Reader API.

The Reader API is a format-neutral application boundary; it is not centered on EPUB or any other single document format.

Apps SHOULD use concepts such as:

```lua
baga.reader.supports(source_or_format)
baga.reader.open(source)
```

An App must not depend on KOReader private Lua objects merely because a particular Platform version uses KOReader internally.

Correct boundary:

```text
App → Baga Ink Reader API → Platform implementation
```

not:

```text
App → KOReader internals
```

### 14.1 Reader Anchor

When storing reading positions, highlights, notes, or application objects linked to content, Apps should prefer standardized Baga Reader Position / Anchor semantics.

Apps MUST:

- treat Anchor as an opaque serializable Baga value;
- not parse XPointer, PDF boxes, EPUB CFI, or other reader-private representations themselves;
- not reimplement a separate locator per EPUB/PDF/MOBI/FB2/TXT/DjVu/CBZ/etc.;
- let the Platform/Reader implementation perform actual resolution/recovery.

The implementation may reuse mature position models from KOReader or other reader engines.

---

## 15. Dependencies and mature-component reuse

To reduce dependency problems, Universal Apps SHOULD normally be self-contained in their own app code/resources. Baga Lua Profile Standard Libraries are provided by the Platform and should not be redundantly bundled into every IKP.

An App MAY:

- use Baga Platform APIs;
- directly use Profile Standard Libraries such as `lsqlite3`;
- bundle pure-Lua third-party libraries inside its IKP.

An App MUST NOT:

- depend on a randomly user-installed native library;
- depend on a dynamic library that happens to exist on one vendor device;
- bundle another SQLite runtime that conflicts with the Platform SQLite baseline;
- require arbitrary cross-app native shared dependencies.

"Self-contained" means application code/resources are self-contained; it does not mean every App carries its own Platform Core, Lua interpreter, Device Adapter, or system bridge.

Mature-component boundary:

```text
SQLite / lsqlite3
→ Stable Standard Library

Automerge core
→ Adopted Local-first Foundation, whole or selected modules

KOReader / FBInk / Vendor SDK
→ Platform / Adapter implementation detail
```

---

## 16. Security and stability

Apps MUST:

- not attempt to escape sandbox;
- not tamper with Platform;
- not modify other Apps' private data;
- not use undeclared interfaces to access sensitive resources;
- not assume arbitrary native-code execution;
- perform appropriate validation of network/file/user inputs.

Platform MAY terminate Apps that violate these rules.

`lsqlite3` must only open authorized paths; implementations must prevent database paths or loadable extensions from becoming sandbox escapes.

---

## 17. Signing and publisher identity

Apps entering Baga Ink Market SHOULD use supported digital signatures.

Updates MUST preserve Application ID and SHOULD preserve publisher-signing continuity.

Key changes require explicit key rotation/recovery mechanisms. Detailed rules are defined by IKP, identity/signing, and Market standards.

---

## 18. Market compatibility labels

Baga Ink Market SHOULD support labels such as:

```text
Baga Ink Universal
Enhanced
Requires Pen
Requires Touch
Requires Network
Kindle Compatible
Android E-Paper Compatible
Experimental
```

Labels must derive from Manifest, Capability Model, and Compatibility evidence rather than arbitrary marketing text.

---

## 19. Hard requirements for Baga Ink Universal

To claim **Baga Ink Universal**, an App MUST simultaneously:

1. use `.ikp`;
2. use Baga Lua Profile;
3. use only public Baga APIs for device / OS / Platform capability;
4. MAY use official Baga Lua Profile Standard Libraries directly;
5. not carry device-specific native binaries as normal business logic;
6. not carry its own Lua interpreter, Device Adapter, or system bridge;
7. not call raw shell / Vendor SDK directly;
8. use the Capability Model;
9. fully declare permissions;
10. use the standard lifecycle;
11. pass the required Compatibility Tests;
12. pass validation on at least the Kindle and Android E-Paper reference platform families before claiming cross-platform Universal status.

---

## 20. What does not belong in the Universal boundary

The following are not normal Universal App development mechanisms:

- arbitrary Shell;
- arbitrary Java/JNI bridge;
- custom kernel/driver access;
- random cross-app native dependencies;
- direct Vendor API calls;
- WebView/Chromium as the default universal execution model;
- per-App system update infrastructure;
- a separate Lua interpreter/device compatibility layer in each App;
- a conflicting SQLite runtime bundled by each App;
- a Baga-specific SQLite-like KV/collection abstraction that replaces mature SQLite;
- a home-grown generic CRDT created merely to replace a mature foundation such as Automerge.

If such capabilities become necessary, they belong in a controlled extension, Standard Library, or Platform implementation layer — not as erosion of the Universal App contract.

---

## 21. LifeBook as a Reference App

LifeBook is the flagship Reference App used to validate that Baga standards actually work across Kindle and Android E-Paper.

LifeBook MUST follow the same core rules as third-party apps. It must not validate the platform by taking privileged shortcuts unavailable to others.

LifeBook:

- obtains device capabilities only through `baga.*`;
- uses `lsqlite3` for structured local relational data;
- uses `baga.reader` for reader capabilities;
- prefers Automerge core for genuine concurrent offline-editing scenarios rather than inventing a CRDT;
- should not create unnecessary generic middleware layers.

Early internal experimental interfaces are allowed only if they:

- are clearly labeled internal/experimental;
- are not depended on by third parties;
- eventually graduate into formal Baga API/Standard Library or are removed.

---

## 22. Final goal

The App Standard exists to move cross-device friction and repeated low-level work into the Platform while allowing mature general-purpose software to retain its proven abstractions.

Developers should spend their time on:

```text
reading experience
notes
RSS
AI
knowledge management
education
tools
creation
```

rather than:

```text
Kindle framebuffer
BOOX refresh API
iReader private SDK
Android vendor differences
device-specific install scripts
file-stitching "databases"
reinvented database abstractions
per-format locator algorithms
generic CRDT reinvention
```

That is the fundamental value of the Baga Ink Universal App contract.
