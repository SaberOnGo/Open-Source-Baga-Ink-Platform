# Baga Ink Standard Libraries and Adopted Components

> **Document level:** First-level Platform Standard / Standard Library and Mature Component Policy  
> **Document ID:** `standards.13`  
> **Locale:** English (`en`)  
> **Status:** Draft v0.5  
> **Date:** 2026-08-23  
> **Parent:** `01_baga-ink-platform-strategy.md`  
> **Related:** Standards 02, 03, 04, 07, 08, 10  
> **Counterpart:** `docs/zh-CN/standards/13_标准库与成熟组件采用规范.md`

---

## 0. Purpose

This document defines how Baga Ink evaluates, adopts, exposes, versions, tests, and replaces mature general-purpose libraries and open-source components.

Core principle:

> **If a mature library already provides a strong, widely understood, portable abstraction, Baga SHOULD adopt that abstraction directly rather than inventing a weaker Baga-specific wrapper.**

At the same time:

> **Using a library internally does not automatically make that library a public Baga API or a new architecture layer.**

Baga therefore distinguishes:

```text
Standard Library
→ a mature developer-facing API deliberately made part of the Baga Lua Profile / public platform contract

Adopted Foundation / Adopted Component
→ a mature implementation/protocol/library deliberately reused by Platform/App internals, with a controlled public boundary

Device/Platform implementation source
→ mature project or OS/vendor mechanism used below the Baga public contract
```

This policy exists to prevent both reinvention and accidental coupling.

---

## 1. Why this Standard exists

Without an explicit policy, platform projects tend to fail in one of two ways.

### Failure mode A — unnecessary reinvention

```text
SQLite already exists
→ invent BagaKV

Automerge already exists
→ invent a generic Baga CRDT

KOReader already knows Kindle display/input/reader behavior
→ rewrite those stacks from zero
```

This creates weaker abstractions, more bugs, more compatibility burden, and less developer familiarity.

### Failure mode B — uncontrolled leakage

```text
Baga uses KOReader internally
→ Apps start importing KOReader private Lua modules

Baga uses a vendor SDK
→ vendor objects become public App types

Baga adopts a library
→ its current internal directory layout becomes a permanent Baga architecture layer
```

This destroys portability.

The correct direction is:

> **Reuse mature capability aggressively while standardizing only the public semantics Baga needs.**

---

## 2. Classification model

Every third-party capability considered for Baga SHOULD be classified before integration.

### 2.1 Standard Library

Use when:

- the upstream API is already a good developer abstraction;
- semantics are portable across Baga target platforms;
- the API is mature and documented;
- the project can pin a compatible version/profile;
- security/sandbox constraints can be enforced;
- compatibility can be tested.

Example:

```text
SQLite + lsqlite3
```

### 2.2 Adopted Foundation

Use when a mature library/protocol is valuable as a reusable foundation but the developer-facing Baga API is not yet frozen or Baga only needs selected modules.

Example:

```text
Automerge core
```

Baga may adopt:

```text
document / merge / history
binary persistence
sync protocol
C FFI
patch / cursor
```

without adopting every layer of `automerge-repo`.

### 2.3 Platform / Adapter implementation source

Use when the project supplies mature device/platform behavior below the public Baga contract.

Examples:

```text
KOReader / koreader-base Kindle device knowledge
FBInk
MuPDF / CREngine
Android OS APIs
Vendor SDKs
Kindle OS / Homebrew mechanisms
```

These do not automatically become Standard Libraries.

---

## 3. Decision questions before adding a Baga wrapper

Before creating a new `baga.*` abstraction or private wrapper, answer:

1. Is the problem already solved by a mature general-purpose library?
2. Is the upstream abstraction stronger/more familiar than the proposed Baga abstraction?
3. Does Baga need to normalize a real device/OS difference, or merely rename an existing software concept?
4. Can the mature API be made available safely under Baga sandbox/permission rules?
5. Can the project pin and test a stable version/profile?
6. Does the upstream license fit the intended integration/distribution model?
7. Will direct adoption reduce long-term compatibility burden?
8. If only part of the project is useful, can Baga adopt selected modules rather than the entire architecture?

If the mature abstraction already fits, a second Baga object model SHOULD NOT be created.

---

## 4. Stable Standard Library: SQLite / lsqlite3

Baga Lua Profile adopts SQLite as the standard local relational database and `lsqlite3` as the stable Lua-facing API.

Developer-facing usage:

```lua
local sqlite3 = require("lsqlite3")
local path = baga.storage.resolve_path("appdata/app.sqlite3")
local db = sqlite3.open(path)
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
WAL where enabled by the pinned profile
```

Baga MUST NOT replace this with a weaker proprietary abstraction such as:

```text
Baga KV store
Baga collection database
Baga document wrapper around basic SQLite
```

unless a genuinely different product capability is being standardized.

---

## 5. Why `lsqlite3` is the public baseline

The public module name is:

```lua
require("lsqlite3")
```

Rationale:

- widely recognizable LuaSQLite3 semantics;
- mature direct access to SQLite;
- suitable for application-owned structured local data;
- avoids coupling third-party Apps to KOReader-private database bindings;
- can be implemented across Kindle and Android E-Paper with a pinned SQLite runtime.

A Kindle implementation MAY internally reuse another SQLite Lua binding such as KOReader's validated `lua-ljsqlite3` where appropriate for Platform internals, but third-party IKP Apps target the Baga Lua Profile `lsqlite3` contract.

Internal binding choice does not redefine the public module.

---

## 6. SQLite runtime profile

Every Baga Platform Release that exposes the SQLite Standard Library MUST pin and record:

```text
SQLite version
lsqlite3 version / source commit
compile options
FTS profile
JSON support
threading mode where relevant
WAL / journaling behavior
loadable-extension policy
VFS / sandbox policy
patch set
source digest
license
```

The Platform should not simply inherit an arbitrary OEM SQLite build and assume compatible behavior.

Baga SDK / diagnostics SHOULD expose the effective Standard Library profile for testing and support.

---

## 7. SQLite sandbox rules

Direct adoption of SQLite does not mean unrestricted filesystem access.

Apps receive an authorized path through Baga Storage semantics:

```lua
local path = baga.storage.resolve_path("appdata/app.sqlite3")
```

The Platform must ensure that SQLite operations remain inside the authorized App sandbox.

At minimum consider:

```text
main DB
ATTACH DATABASE
rollback journal
WAL
SHM
temporary DB / temp files
URI filename parameters
VFS override
symlink / canonical path escape
loadable extensions
```

### 7.1 Strong OS sandbox

On Android, the implementation MAY rely substantially on the OS application sandbox plus Baga path mapping.

### 7.2 Weak OS sandbox

On Kindle or similar environments, Baga MUST provide a sandbox-aware SQLite VFS or equivalent I/O confinement where necessary.

Returning a "safe" initial path is insufficient if SQLite can later open another path through ATTACH, URI options, temp files, extension loading, or equivalent mechanisms.

---

## 8. SQLite and BICTS

Because SQLite / lsqlite3 is a Stable Standard Library, compatibility tests MUST cover the pinned profile.

Minimum categories:

```text
module load
version/profile report
open authorized DB
schema creation
prepared statements
transactions
indexes
foreign keys
BLOB
FTS / JSON where included in profile
close/reopen durability
error behavior
sandbox escape attempts
ATTACH / journal / WAL / SHM / temp behavior
loadable-extension restriction
sleep/wake / restart durability
```

Changing the SQLite or lsqlite3 baseline requires regression testing.

Mature adoption reduces implementation work; it does not remove the need for compatibility evidence.

---

## 9. Adopted Foundation: Automerge core

Baga adopts **Automerge core** as the preferred Local-first / CRDT foundation for data that genuinely needs concurrent offline editing and automatic merge.

This does **not** mean:

```text
all Baga data must be CRDT-based
every App must use Automerge
Baga must adopt the entire automerge-repo architecture
Automerge becomes a Device Capability
```

Instead, Baga MAY use the whole core or selected modules according to need.

Useful capability areas include:

```text
document model
concurrent change merge
change history
binary save/load
sync protocol
patch generation
cursor/position support
Rust core
C FFI
```

---

## 10. Automerge use cases and non-use cases

Good candidates include true multi-device concurrent offline-edit scenarios such as:

```text
notes
life records
long-form drafts
shared editable structures
```

Examples that often do not need a CRDT:

```text
reading position
→ simple product merge policy

server-authoritative feeds/comments/public notes
→ server authority + local SQLite cache

book files
→ content hash + file transfer

immutable release packages
→ signed package/update protocol
```

The decision is driven by data semantics, not by the attractiveness of CRDT technology.

---

## 11. Automerge persistence and SQLite

Automerge and SQLite are complementary rather than competing technologies.

A practical pattern MAY be:

```text
SQLite
→ object index / metadata / queryable fields / cache / transactional app state

Automerge binary document
→ stored as SQLite BLOB or controlled file
→ concurrent-edit history / merge state
```

Baga does not require a product to replace its relational model with CRDT documents merely because Automerge is available.

---

## 12. Automerge sync protocol

If independent Baga implementations exchange Automerge sync protocol or Automerge binary documents directly, the Platform/App contract MUST pin the compatible Automerge protocol/data-format expectations.

Do not specify:

```text
"use latest Automerge"
```

for a long-lived interoperable protocol.

A stable developer-facing module, if standardized later, must define:

```text
module/API version
Automerge core version range
binary format expectations
sync protocol expectations
migration behavior
resource limits
error mapping
sandbox implications
```

Until then, the Automerge bridge remains an Adopted Foundation / implementation boundary rather than a frozen Baga Lua Profile module.

---

## 13. Automerge FFI / language integration

Baga implementations MAY integrate Automerge through:

```text
Rust native core
C FFI / automerge-c
LuaJIT FFI
JNI / Kotlin bridge
another controlled Platform-internal binding
```

The bridge is an implementation choice unless/until a public Standard Library module is explicitly frozen.

The implementation SHOULD prefer upstream concepts and binary/protocol semantics rather than inventing a second incompatible CRDT model.

---

## 14. KOReader / koreader-base

KOReader and koreader-base are mature sources for reader/UI/device knowledge, especially on Kindle.

Baga MAY reuse:

```text
Kindle device detection
Display / input knowledge
UIManager / widgets
ReaderUI
CREngine
MuPDF integration
Annotation / Highlight / Bookmark
position / search / selection / anchor mechanisms
```

But boundaries remain:

```text
KOReader device knowledge
→ may implement Kindle Device Adapter subsystems

KOReader UI/Reader stack
→ may implement Platform UI/Reader capability

KOReader private Lua API
→ NOT a Universal IKP API
```

LifeBook and third-party Apps must not directly import private KOReader modules.

---

## 15. FBInk

FBInk may be adopted as a mature display/backend component where it provides a verified, maintainable mechanism for a device family.

Baga uses it below the DisplayAdapter/public display contract.

Raw FBInk API names, waveform IDs, private structs, or device-specific assumptions do not become `baga.display` semantics.

---

## 16. Reader engines: MuPDF / CREngine and similar projects

Reader engines MAY be reused inside Platform Reader implementations.

The public boundary remains:

```text
baga.reader
```

rather than engine-specific objects.

Different document formats may use different mature internal engines/position systems as long as the Baga Reader contract remains stable.

---

## 17. General mature libraries

Baga SHOULD prefer mature components for areas such as:

```text
JSON parsing / canonicalization
cryptography
compression
HTTP / TLS
Unicode / text handling
image decoding
PDF / document rendering
```

Before adding a Baga-specific abstraction, classify whether the capability is:

```text
A. general-purpose software semantics
   → likely direct library adoption

B. device/OS/platform variation
   → likely baga.* / Device Adapter normalization

C. product/business behavior
   → keep in App/product layer
```

---

## 18. Pinning and reproducibility

Every production/reference Platform Release SHOULD record adopted-component identity:

```text
upstream project
version / commit
source URL
source digest
license
local patch set
build profile
native target / ABI where applicable
which Platform subsystem uses it
BICTS / contract-test evidence where relevant
```

Do not base a compatibility claim on an unpinned nightly or "latest" dependency.

---

## 19. License boundary

Adopting a mature component does not relicense it under the Baga repository license.

Baga-authored material defaults to Apache-2.0, while third-party components retain their upstream licenses.

Concrete distributions must satisfy the licenses of the components actually shipped, including source/offering, notices, modification obligations, or other terms where applicable.

The repository tracks high-level upstream license boundaries in:

```text
THIRD_PARTY_NOTICES.md
```

Release-specific dependency/license manifests remain required.

---

## 20. Public API promotion criteria

An Adopted Component should become a stable developer-facing Standard Library only after evidence supports:

```text
portable value across target platforms
mature/stable upstream semantics
reasonable resource use
clear security/sandbox boundary
pinned compatibility profile
cross-device test coverage
long-term maintenance feasibility
license/distribution feasibility
```

Do not promote an internal convenience binding merely because one Reference Platform uses it.

---

## 21. Replacing an adopted component

Baga public contracts should make internal replacement possible.

If Baga replaces:

```text
FBInk with another display backend
one HTTP/TLS library with another
one Reader engine with another
```

Universal Apps should not need to change as long as public Baga semantics remain stable.

For a direct Standard Library such as SQLite/lsqlite3, replacement is different because the upstream semantics are intentionally public. In that case Baga must preserve API/data compatibility or explicitly version the Standard Library contract.

---

## 22. Version policy

Three version layers must remain distinguishable:

```text
Baga Platform / Lua Profile version
Standard Library public contract/profile version
underlying upstream component version/commit
```

For example:

```text
Baga Lua Profile: 0.x
lsqlite3 public module profile: pinned compatibility baseline
SQLite runtime: exact version/compile options
```

Do not collapse these into a single ambiguous "library version" field.

---

## 23. Security review

Mature open-source software is not automatically safe merely because it is widely used.

Adoption review SHOULD consider:

```text
input parsing surface
native memory-safety risk
sandbox/VFS behavior
extension/plugin loading
network behavior
cryptographic correctness
supply-chain provenance
update policy
known vulnerabilities
resource exhaustion
```

Baga may disable or restrict upstream features that conflict with Platform security.

Examples:

```text
SQLite loadable extensions disabled/restricted
Lua package/native loading restricted
KOReader private plugin/userpatch behavior not exposed to Universal Apps
vendor SDK objects contained below Adapter
```

---

## 24. Resource constraints

Baga targets low-resource devices, including older Kindle hardware.

A component may be excellent yet unsuitable as a mandatory Base dependency.

Evaluate:

```text
binary size
RAM
startup cost
CPU
storage
background work
battery impact
cross-compilation complexity
```

This is one reason Automerge is an Adopted Foundation rather than a Base Mandatory Standard Library.

---

## 25. Test responsibility

Adopted software must be tested at the Baga boundary.

Examples:

```text
SQLite / lsqlite3
→ Standard Library BICTS

KOReader / FBInk Kindle reuse
→ Kindle Adapter Contract Tests + BICTS

Automerge integration
→ product/module interoperability tests where actually used

Reader engines
→ baga.reader behavior tests
```

Baga does not need to retest every upstream internal detail, but it must verify the semantics Baga depends on.

---

## 26. Dependency graph transparency

Reference releases SHOULD produce machine-readable dependency manifests.

A dependency record SHOULD identify:

```text
component
source
version/commit
digest
license
local modifications
consumer subsystem
distribution form
```

This supports reproducibility, security audit, license compliance, and future backend replacement.

---

## 27. Anti-patterns

Avoid:

### 27.1 Wrapper for wrapper's sake

```text
SQLite
→ BagaDB
→ BagaCollection
→ App
```

when direct SQLite semantics are already better understood and more powerful.

### 27.2 Architecture leakage

```text
Baga uses KOReader
→ LifeBook imports KOReader private modules
```

### 27.3 Automatic all-layer adoption

```text
Automerge is good
→ adopt every automerge-repo layer as Baga architecture
```

### 27.4 Unpinned moving dependency

```text
"latest KOReader"
"latest Automerge"
```

as a compatibility baseline.

### 27.5 License erasure

Copying or bundling third-party code and treating it as Apache-2.0 Baga-authored material.

### 27.6 Capability pollution

Registering implementation/library names as Capabilities:

```text
capability.sqlite
capability.koreader
capability.automerge
```

instead of portable device/platform semantics.

---

## 28. Decision table

| Capability | Preferred Baga treatment |
|---|---|
| Relational local database | SQLite + `lsqlite3` Standard Library |
| Concurrent Local-first document merge | Automerge core Adopted Foundation when actually needed |
| Kindle display/input/device knowledge | KOReader/koreader-base reuse below Device Adapter |
| E-paper framebuffer/refresh mechanism | FBInk / OS / vendor mechanism below DisplayAdapter |
| EPUB/PDF/document rendering | mature Reader engine below `baga.reader` |
| Device/vendor differences | Device Adapter / Capability |
| Product business rules | App/product layer |
| Publisher signing / update / repository | Baga distribution standards, not library wrappers |

---

## 29. Current adopted-component baseline

At the current Draft baseline:

### Stable developer-facing Standard Library

```text
SQLite / lsqlite3
```

### Adopted Foundation

```text
Automerge core
```

### Important Reference Platform implementation sources

```text
KOReader
koreader-base
FBInk
MuPDF / CREngine as used through reader implementations
Android / vendor SDK mechanisms
Kindle OS / validated Homebrew mechanisms
```

Exact versions/commits are release artifacts, not hard-coded forever into this Standard.

---

## 30. Promotion / change governance

A change that affects the public Standard Library surface MUST update this Standard and the relevant App/API/Profile/BICTS documents.

Examples:

```text
change public lsqlite3 compatibility baseline
→ update 13 + API/Profile docs + BICTS

freeze a public Automerge Lua module
→ update 13 + App/API docs + tests + version/migration rules

replace a Kindle display backend internally
→ may only require implementation manifest/tests if public contract is unchanged
```

This distinction prevents internal refactors from becoming unnecessary ecosystem migrations.

---

## 31. Final principle

> **Baga Ink should standardize the interfaces that need cross-device stability and directly reuse mature general-purpose software where its existing abstraction is already the right one.**

The desired outcome is:

```text
less reinvention
+ stronger upstream semantics
+ thin device adapters
+ stable public contracts
+ pinned/tested implementations
+ explicit license/provenance
```

not an ever-growing stack of Baga-specific wrappers around software that already solved the underlying problem well.
