# Baga Ink API Specification

> **Document level:** First-level platform standard  
> **Document ID:** `standards.03`  
> **Locale:** English (`en`)  
> **Status:** Draft v0.5  
> **Date:** 2026-08-23  
> **Parent:** `01_baga-ink-platform-strategy.md`  
> **Related:** Standards 02, 04, 05, 06, 09, 13  
> **Counterpart:** `docs/zh-CN/standards/03_API规范.md`

---

## 0. Purpose

This document defines the public `baga.*` API boundary available to Baga Ink Universal Apps.

The goal is not to copy the Android SDK and not to wrap every general-purpose software capability behind a Baga namespace. The API should remain:

- thin;
- stable;
- e-paper appropriate;
- implementable on Kindle and Android E-Paper;
- free of device/vendor implementation leakage;
- versionable over the long term.

Two developer surfaces must remain conceptually distinct:

```text
Baga Ink API
→ normalizes device / OS / Platform differences

Baga Lua Profile Standard Libraries
→ directly expose mature general-purpose software capabilities
```

SQLite is therefore exposed through the Baga Lua Profile Standard Library `lsqlite3`, not reinvented as a `baga.database` abstraction.

Active API text describes the current approved API only; Git preserves historical proposals.

---

## 1. General design principles

### 1.1 Namespace

Public Platform APIs use:

```lua
baga.*
```

Core namespaces:

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

Structured relational data uses the Baga Lua Profile Standard Library directly:

```lua
local sqlite3 = require("lsqlite3")
```

### 1.2 No universal system escape hatch

v0.5 does not expose a generic public API for arbitrary host commands, Android Context, Kindle shell, or direct vendor SDK calls.

When a new capability is needed, classify it first:

```text
requirement
  ↓
is it already solved by a mature general-purpose library?
  ├─ yes → Standard Library / Adopted Component
  └─ no, and it represents device/platform variation
          → Capability / Baga Ink API
```

Private device capability must not become an App shortcut around Platform policy.

### 1.3 Public API versus mature library reuse

Baga API defines the **platform behavior contract** developers may depend on. It does not prescribe the number of internal software layers and does not require underlying capabilities to be reimplemented.

Platform MAY directly, compositionally, or selectively reuse mature projects such as:

```text
KOReader / koreader-base
FBInk
SQLite / lsqlite3
Automerge
MuPDF / CREngine
Android / Vendor SDKs
```

Two cases must remain distinct.

#### A. Platform implementation detail

Examples: KOReader, FBInk, Vendor SDK. Apps only see `baga.*`.

#### B. Adopted Standard Library

When an upstream library already exposes an appropriate portable abstraction, Baga MAY adopt the upstream API directly rather than adding another wrapper.

Current stable example:

```text
SQLite / lsqlite3
```

Therefore Apps may use SQL, transactions, prepared statements, indexes, and FTS directly. Baga only supplies the cross-device pieces that still need standardization: safe paths/sandboxing, pinned version/profile, compile options, and compatibility tests.

Automerge core is adopted as the preferred Local-first / CRDT foundation; the developer-facing Lua binding is not yet frozen.

---

## 2. Baga Lua Profile and Standard Libraries

Universal Apps run inside a restricted, portable Baga Lua Profile.

### 2.1 Baseline libraries

The profile SHOULD provide safe portable libraries such as:

```lua
string
table
math
utf8
coroutine
```

### 2.2 Official adopted database library: `lsqlite3`

Reference Platforms that support Universal Apps MUST provide:

```lua
local sqlite3 = require("lsqlite3")
```

The API SHOULD remain compatible with upstream LuaSQLite3 / `lsqlite3`, not rename methods or invent another query object model.

Typical use:

```lua
local sqlite3 = require("lsqlite3")
local path = baga.storage.resolve_path("appdata/app.sqlite3")
local db = sqlite3.open(path)

db:exec([[
  CREATE TABLE IF NOT EXISTS notes (
    id TEXT PRIMARY KEY,
    body TEXT NOT NULL
  )
]])
```

Each Platform Release must pin the SQLite / lsqlite3 version and compile profile. Standard 13 defines the detailed policy.

### 2.3 Automerge status

`automerge/automerge` core is an adopted foundation that MAY be used as a whole or by selected capabilities:

```text
document / merge / history
binary persistence
sync protocol
C FFI
patches / cursors
```

No stable developer-facing Lua module is defined yet.

LifeBook / Platform implementations MAY use Rust core, C FFI, LuaJIT FFI, or another controlled internal bridge. If a mature Lua binding is standardized later, it SHOULD preserve upstream Automerge concepts and formats where practical.

### 2.4 Restricted libraries

The Platform MAY remove or restrict:

```lua
os
io
package
debug
```

Apps MUST NOT depend on:

```lua
os.execute
io.popen
loading arbitrary native modules
raw process spawn
filesystem escape
```

Files, network, and device capabilities must be accessed through approved Baga interfaces/Standard Libraries.

---

## 3. Return values and error model

Baga APIs SHOULD use Lua-friendly conventions.

Successful synchronous operation:

```lua
local value = operation()
```

Fallible synchronous operation:

```lua
local value, err = operation()
if not value then
    baga.log.error(err.code, err.message)
end
```

Recommended standard error object:

```lua
{
    code = "permission_denied",
    message = "Network permission is not granted",
    recoverable = true,
    details = {}
}
```

Stable error codes SHOULD use lowercase `snake_case`.

Common codes include:

```text
not_supported
permission_denied
not_found
invalid_argument
busy
offline
timeout
cancelled
io_error
quota_exceeded
incompatible
internal_error
```

SQLite errors may remain exposed through mature `lsqlite3` semantics; they are not device-capability errors.

---

## 4. Asynchronous task model

Network, sync, and expensive Reader operations must not block the UI event loop.

Conceptual v0.5 task model:

```lua
local task = baga.network.request({...})

task:on_success(function(response)
end)

task:on_error(function(err)
end)

task:on_complete(function()
end)
```

Tasks SHOULD support:

```lua
task:cancel()
task:is_done()
```

Where coroutine-based await is safe, the SDK MAY expose:

```lua
local result, err = task:await()
```

`await()` MUST NOT block the underlying UI event loop.

---

## 5. `baga.api`

Version negotiation and feature discovery.

Recommended surface:

```lua
baga.api.version()
baga.api.has(feature)
baga.api.standard_library(name)
```

`standard_library(name)` MAY return a version descriptor:

```lua
{
    name = "lsqlite3",
    version = "0.9.7",
    sqlite_version = "3.53.4"
}
```

Example versions are illustrative; actual values are pinned by the Platform Release.

---

## 6. `baga.app`

Application identity and lifecycle.

Recommended surface:

```lua
baga.app.info()
baga.app.on(event_name, handler)
baga.app.quit()
```

Initial events:

```text
start
resume
pause
sleep
wake
stop
update
```

Apps must not assume permanent process residency.

---

## 7. `baga.device`

Cross-device capability queries.

Recommended surface:

```lua
baga.device.info()
baga.device.has(capability)
baga.device.capabilities()
```

Universal App core logic SHOULD not depend on device family/model.

SQLite / lsqlite3 is not a Device Capability.

---

## 8. `baga.ui`

Baga UI is a lightweight e-paper-oriented UI API.

Initial component direction:

```lua
baga.ui.page(opts)
baga.ui.text(opts)
baga.ui.image(opts)
baga.ui.button(opts)
baga.ui.list(opts)
baga.ui.menu(opts)
baga.ui.dialog(opts)
baga.ui.toolbar(opts)
```

UI objects SHOULD support operations such as:

```lua
view:show()
view:hide()
view:update(props)
view:invalidate()
view:focus()
```

Layout, focus, and refresh behavior are defined by Standard 09.

---

## 9. `baga.display`

Display APIs express semantic refresh intent rather than exposing vendor waveform IDs.

Recommended surface:

```lua
baga.display.size()
baga.display.mode(mode)
baga.display.refresh(opts)
baga.display.invalidate(region)
baga.display.has(mode_or_feature)
```

Semantic modes:

```text
AUTO
TEXT
QUALITY
FAST
ANIMATION
```

Apps MUST interpret a mode as desired behavior, not a hardware guarantee.

---

## 10. `baga.input`

Input supports both hardware events and semantic actions.

Recommended surface:

```lua
baga.input.on(event_or_action, handler)
baga.input.off(token)
baga.input.has(input_type)
```

Semantic actions:

```text
page_next
page_previous
confirm
back
menu
```

Universal Apps SHOULD prefer semantic actions over platform keycodes.

---

## 11. `baga.storage`

`baga.storage` handles files/byte resources, logical paths, and sandbox bridging. It is not a database API.

Recommended surface:

```lua
baga.storage.read_text(path)
baga.storage.write_text(path, text)
baga.storage.read_bytes(path)
baga.storage.write_bytes(path, bytes)
baga.storage.exists(path)
baga.storage.list(path)
baga.storage.mkdir(path)
baga.storage.remove(path)
baga.storage.move(from, to)
baga.storage.copy(from, to)
baga.storage.resolve_path(path)
```

Logical roots:

```text
appdata/
cache/
documents/
downloads/
```

### 11.1 `resolve_path()`

Used when an approved Standard Library/native-backed library requires a concrete runtime path, for example SQLite:

```lua
local path = baga.storage.resolve_path("appdata/lifebook.sqlite3")
```

Rules:

- only authorized logical paths for the current App may be resolved;
- path normalization and sandbox checks are mandatory;
- returned paths are runtime-local and MUST NOT become cross-device business identifiers;
- Apps must not infer Vendor/OS structure from the returned path;
- weak-OS-sandbox environments such as Kindle require Platform-level validation, restricted VFS, or equivalent containment;
- strong OS sandbox environments may additionally rely on the OS sandbox.

`resolve_path()` is not a raw-filesystem escape hatch.

---

## 12. `baga.library`

Standard interface to user-visible books/documents.

Conceptual surface:

```lua
baga.library.list(opts)
baga.library.get(item_id)
baga.library.open(item_id)
baga.library.import(source, opts)
baga.library.remove(item_id, opts)
```

Library items use stable opaque `item_id` values rather than physical paths.

Rules:

- `list/get/open` require `library.read`;
- `import/remove` require `library.write`;
- `open()` SHOULD return a logical source/handle accepted by `baga.reader.open()`;
- Universal Apps MUST NOT scan Kindle `/documents`, Android vendor bookshelves, or physical filesystem paths directly;
- the API is not restricted to EPUB or any single document format.

---

## 13. `baga.permissions`

Recommended surface:

```lua
baga.permissions.check(name)
baga.permissions.request(name)
baga.permissions.list()
```

Permissions must first be declared in the IKP Manifest.

An App-local SQLite database inside the sandbox needs no extra user-data permission.

---

## 14. `baga.network`

Recommended surface:

```lua
baga.network.state()
baga.network.request(opts)
baga.network.is_online()
```

v0.5 SHOULD support HTTPS.

Apps MUST NOT bypass Platform TLS/proxy/connectivity policy through private interfaces.

---

## 15. `baga.power`

Recommended surface:

```lua
baga.power.battery()
baga.power.is_charging()
baga.power.request_keep_awake(opts)
baga.power.release_keep_awake(token)
```

Keep-awake is a request, not a command. Platform policy retains authority.

---

## 16. `baga.reader`

Reader API exists so every App does not independently rebuild document opening, format handling, reading positions, selection, search, annotation, and anchor infrastructure.

The API is format-neutral, not EPUB-centric.

Recommended entry points:

```lua
baga.reader.supports(source_or_format)
baga.reader.open(source, opts)
```

A Reader Session may expose:

```lua
session:position()
session:goto(position)
session:next_page()
session:previous_page()
session:search(query)
session:get_selection()
session:create_anchor(target)
session:goto_anchor(anchor)
session:resolve_anchor(anchor)
session:add_highlight(range, opts)
session:add_note(range, text)
session:close()
```

### 16.1 Position and Anchor

Locator algorithms belong to the Reader implementation. Apps store/pass serializable Baga position values.

Internal implementations MAY reuse:

```text
KOReader / CREngine XPointer-like positions
PDF page + page-local positions / boxes
fixed-page document page / region
other mature reader locators
quote / context / progression fallback evidence
```

Readium Locator, EPUB CFI, or W3C Web Annotation MAY inform design, but no single external locator is the mandatory Baga format boundary.

### 16.2 Reader implementation boundary

A Platform MAY implement Reader functionality using KOReader, MuPDF, CREngine, or combinations of mature components.

Those private implementation objects are not part of the public API contract.

---

## 17. `baga.sync`

`baga.sync` provides platform-level sync **triggering, scheduling, and device policy** for offline-first applications.

Recommended surface:

```lua
baga.sync.state()
baga.sync.trigger(name, opts)
baga.sync.on(event, handler)
```

Possible policies:

```text
when_online
wifi_only
when_charging
manual
```

Responsibilities:

```text
SQLite / lsqlite3
→ local relational state / transactions / queries / indexes / FTS

baga.sync
→ connectivity, task triggering, power/network policy, lifecycle coordination

Automerge core (when applicable)
→ concurrent Local-first state / CRDT merge / history / optional sync protocol

App domain logic
→ authority policy / object identity / business rules
```

Baga v0.5 does not require every App to use Automerge and does not adopt `automerge-repo`'s Storage/Network Adapter architecture as Baga public architecture.

If independent implementations later exchange Automerge binary/sync protocol directly, the protocol version and migration rules must be explicitly pinned.

---

## 18. `baga.log`

Unified logging:

```lua
baga.log.debug(message, fields)
baga.log.info(message, fields)
baga.log.warn(message, fields)
baga.log.error(message, fields)
```

Sensitive user data SHOULD NOT be written to normal logs.

---

## 19. Capability naming

Capabilities use lowercase dot-separated hierarchical names. Standard 04 owns the registry.

Standard capability names MUST NOT contain vendor brands or internal library names.

SQLite / lsqlite3 / Automerge are not Device Capability names.

---

## 20. Permission naming

Permissions use stable semantic names. Standard 05 owns the registry and permission behavior.

---

## 21. API compatibility versioning

The IKP Manifest MUST declare API compatibility.

Recommended form:

```json
"baga_api": {
  "min": "0.5",
  "max_exclusive": "1.0"
}
```

Standard Library compatibility is tracked separately by Baga Lua Profile / Platform Release.

After a stable major exists:

- Minor SHOULD add only backward-compatible capability;
- Patch MUST NOT introduce breaking API changes;
- breaking changes require a new major;
- deprecated APIs should have a reasonable migration window.

---

## 22. Thread / event-loop principle

Apps do not need to understand the underlying OS thread model.

Expensive operations must use Task/asynchronous mechanisms.

SQLite transactions remain local synchronous calls; Apps should avoid obviously expensive queries/migrations inside UI handlers.

---

## 23. API, Standard Library, and Device Adapter are distinct

```text
baga.display
→ device / OS variation
→ Platform / Adapter implementation

lsqlite3
→ mature general-purpose database
→ direct upstream semantics
→ Platform provides pinned runtime + safe path

Automerge core
→ adopted mature foundation
→ Platform/App uses the whole or selected modules as needed
```

---

## 24. v0.5 minimum API loop

First group:

```text
baga.api
baga.app
baga.device
baga.ui
baga.display
baga.input
baga.storage
baga.log
```

Second group:

```text
baga.library
baga.network
baga.permissions
baga.power
baga.reader
baga.sync
```

Reference Platforms supporting Baga Lua Profile SHOULD also validate:

```text
lsqlite3 + pinned SQLite
```

Automerge adoption expands only where actual feature/hardware evidence supports it.

---

## 25. Final test for adding a `baga.*` API

Before a new API enters Baga Ink, answer:

1. Does it represent device / OS / Platform variation, or is the problem already solved by a mature general-purpose library?
2. If a mature library exists, should Baga adopt it directly instead of wrapping it?
3. Can Kindle and Android E-Paper implement the semantics, or at least return a defined `not_supported`?
4. Could the API become a backdoor around Capability / Permission / Sandbox?
5. Is the compatibility burden worth carrying for years?
6. Is there a mature, license-compatible, verifiable implementation that can be reused wholly or partially?
7. If reusing upstream, can Baga preserve its strong semantics instead of inventing a weaker proprietary object model?

Principle:

> **Adopt mature Standard Libraries directly where they fit; reserve Baga Ink API for behavior that truly needs cross-device normalization.**
