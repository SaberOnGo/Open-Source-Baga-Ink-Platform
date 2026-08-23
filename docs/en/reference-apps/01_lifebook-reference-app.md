# LifeBook Ink Reference App Implementation Specification

> **Document level:** Reference App Implementation Specification  
> **Document ID:** `reference-apps.01`  
> **Locale:** English (`en`)  
> **Status:** Baseline v0.6  
> **Date:** 2026-08-23  
> **Applies to:** LifeBook on Baga Ink Platform  
> **Kindle implementation freeze:** `docs/en/reference-apps/03_baga-ink-kindle-implementation-architecture-freeze.md`  
> **This is not a Baga Ink Standard and cannot override governing Standards.**  
> **Counterpart:** `docs/zh-CN/reference-apps/01_LifeBook参考实现.md`

---

## 0. Purpose

This document defines LifeBook's implementation boundaries as the flagship Baga Ink Reference App, including module boundaries, cross-device rules, UI/Reader/SQLite use, and local-first synchronization strategy.

Core goal:

> **Use a real LifeBook application to prove that the same IKP can span Kindle and Android E-Paper while reusing mature systems such as KOReader, SQLite, and Automerge without inventing unnecessary architecture layers.**

For Kindle bootstrap, Homebrew foundation, KPM/MRPI, `.kpkg` vs `.ikp`, pinned KOReader integration, Home Entry, installation routes, and ABI/build details, this document defers to the Kindle Implementation Architecture Freeze rather than creating a second definition.

---

## 1. Governing documents

LifeBook MUST follow:

```text
00 Standards Index
01 Platform Strategy
02 App Standard
03 API
04 Capability Registry
05 Permission Model
06 IKP Package
07 Device Adapter
08 Compatibility
09 UI
10 BICTS
11 Kindle Adapter
12 Android E-Paper Adapter
13 Standard Libraries and Adopted Components
20–28 Distribution / Signing / Update
```

Authority order:

```text
Baga Ink Standards
  > Kindle Implementation Architecture Freeze (for Kindle implementation work)
  > LifeBook Reference
  > LifeBook implementation
```

---

## 2. LifeBook's role

LifeBook is:

> **The flagship Universal App / Reference App on Baga Ink Platform.**

LifeBook product/business logic stays inside IKP. Platform, Device Adapter, Reader backend, database engine, and general CRDT foundation are not reimplemented by LifeBook.

---

## 3. Overall architecture

```text
LifeBook — lifebook.ikp
        │
        ├─ Baga Ink API        → device / OS / Platform capability
        └─ Baga Lua Profile    → mature Standard Libraries
                │
                ▼
        Baga Ink Platform Core
                │
                ▼
          Device Adapter
        ┌───────┴────────┐
        ▼                ▼
     Kindle        Android E-Paper
```

LifeBook does not directly branch on Kindle, BOOX, or iReader identity.

---

## 4. LifeBook product modules

```text
LifeBook
├─ Account / Session
├─ Library Product Logic
├─ Articles
├─ Q&A / Comments
├─ Public / Community Notes
├─ My Notes / Highlights
├─ Life Records
├─ Time Capsule
├─ AI
├─ Offline Cache Policy
└─ Sync Domain Logic
```

These are LifeBook product concerns.

---

## 5. Platform capabilities and mature libraries used by LifeBook

```text
UI                     → baga.ui / input / display
Reader                 → baga.reader
User Library           → baga.library
Files / downloads      → baga.storage
Network                → baga.network
Sync scheduling        → baga.sync
Power / lifecycle      → baga.power / baga.app
Permissions            → baga.permissions
Logging                → baga.log
Relational local DB    → require("lsqlite3")
Concurrent local-first → Automerge core where appropriate
```

SQLite is LifeBook's relational local-database foundation.

---

## 6. SQLite

LifeBook uses the Baga Lua Profile Standard Library:

```lua
local sqlite3 = require("lsqlite3")
local path = baga.storage.resolve_path("appdata/lifebook.sqlite3")
local db = sqlite3.open(path)
```

LifeBook owns its:

```text
schema
migrations
SQL queries
indexes
FTS
business constraints
```

### 6.1 LifeBook data suited to SQLite

```text
library metadata
account/session metadata
reading progress
cached articles
cached Q&A / comments
public-note cache
sync metadata
local indexes
full-text search index
Automerge document/change metadata or BLOBs
```

### 6.2 Large files

Books, images, and large attachments remain under `baga.storage`; SQLite stores metadata, indexes, and relationships.

---

## 7. Automerge

For objects with real multi-device concurrent offline editing, prefer Automerge core.

Candidates:

```text
My Notes
Life Records
Time Capsule drafts
Article drafts
other genuinely concurrent editable objects
```

Usually not necessary:

```text
Reading Position
→ simple domain merge

Feed / Comments / Public Notes
→ server authoritative + SQLite cache

Book Files
→ content hash + file transfer
```

### 7.1 Whole or modular adoption

LifeBook / Platform MAY:

```text
use complete Automerge core
use only document / merge / history
use only binary persistence
use only sync protocol
bridge through automerge-c / Rust
use only patches / cursors
```

Full `automerge-repo` is not required.

### 7.2 SQLite + Automerge

```text
SQLite
├─ ordinary relational data
├─ cache / index / FTS
└─ Automerge document/change BLOB metadata

Automerge
└─ genuinely concurrent local-first objects
```

They are complementary.

---

## 8. Sync boundary

```text
SQLite
→ local persistence / query / transaction

Automerge (where applicable)
→ CRDT merge / history / optional sync protocol

baga.sync
→ when_online / wifi_only / charging / sleep-wake / trigger / retry

LifeBook Domain
→ authoritative policy / object identity / business conflict policy
```

Confirmed local user actions must be durably persisted before waiting for network synchronization.

---

## 9. Reader

LifeBook book/document reading uses `baga.reader`.

The first Kindle implementation should reuse KOReader heavily; Android may use another mature implementation.

LifeBook does not depend on KOReader private Lua objects or sidecar schemas.

The Reader contract is not EPUB-centric.

---

## 10. Reader Anchor / Public Notes

```text
book/document content → baga.reader
public note body       → LifeBook Domain / Server
```

The two are associated using a Baga Reader Anchor.

LifeBook stores/synchronizes the Anchor and gives it back to the Reader. It does not parse XPointer, PDF boxes, EPUB CFI, or Readium Locator.

The Kindle implementation should reuse KOReader's mature rolling/paging position mechanisms. Readium/W3C models are design references only.

---

## 11. `baga.library`

User-library access:

```text
baga.library.list/get/open/import/remove
```

LifeBook does not scan Kindle `/documents` or understand Android vendor bookshelf databases.

Library Items use opaque IDs/source handles that can be passed to `baga.reader`.

---

## 12. LifeBook UI

Articles, Q&A, comments, Life Records, Time Capsule, and AI follow:

```text
LifeBook Domain
   ↓
baga.ui
```

They do not need to be converted to EPUB and do not pass through ReaderUI.

UI principles:

- high contrast;
- page-first interaction;
- Touch + Focus;
- semantic physical-page-key actions;
- little animation;
- minimal full-screen refresh;
- progressive enhancement for Color / Pen / Fast Refresh.

---

## 13. Mature component reuse on Kindle

The Kindle Implementation Architecture Freeze is authoritative for concrete module adoption and installation roles.

At LifeBook level:

```text
baga.reader
→ pinned KOReader / ReaderUI / CREngine / MuPDF / Annotation inside Kindle Platform

baga.ui/display/input
→ KOReader UIManager / widgets / Kindle device knowledge / FBInk inside Kindle Platform

Baga Lua Profile lsqlite3
→ Platform-managed libsqlite3

KOReader internals
→ lua-ljsqlite3
→ may share the verified Platform libsqlite3 with lsqlite3

Automerge core
→ true Local-first objects; whole/modular adoption, not the default engine for all data
```

Frozen Homebrew/install roles:

```text
KPM
→ Baga Platform native install/update manager on KPM-compatible targets
→ does not manage lifebook.ikp

Hotfix / sh_integration
→ Homebrew foundation / visible launcher integration

MRPI / KindleTool
→ KPM-incompatible/legacy Platform install, bootstrap, or build/package tooling

KUAL / PEKI
→ legacy/admin/bootstrap fallback only
→ normal LifeBook path does not depend on them

WinterBreak / SpringBreak / Sanctuary / Véra
→ records in Baga Ink Client Installation Route DB only

Mesquito
→ not a Baga-adopted module; if used internally by an upstream route, it remains an upstream implementation detail
```

These are Kindle Platform / Client implementation details, not LifeBook App Contract and not a new Runtime layer.

---

## 14. Mature component reuse on Android

```text
lsqlite3
→ Baga Platform pins SQLite runtime
→ IKP does not depend on OEM system SQLite version variance

Reader
→ mature Android/native implementation

Automerge
→ may use mature Rust/C/Java/JS bindings/bridges
```

Here `SQLite runtime` means the SQLite library implementation only; it is not a `Baga Platform Runtime` architecture layer.

The LifeBook IKP does not fork by platform.

---

## 15. Permission baseline

Declare permissions gradually by feature:

```text
network
library.read
notes.read
notes.write
```

Add only when needed:

```text
library.write
user_files.read
user_files.write
audio.output
bluetooth
frontlight.control
power.keep_awake
```

LifeBook's private SQLite database lives inside the App sandbox and does not require additional user-data permission.

---

## 16. Offline-first behavior

After initial account setup, offline mode should still support:

- opening LifeBook;
- browsing local library;
- reading;
- viewing cached articles/Q&A/comments/public notes;
- creating/editing local notes;
- creating Life Records;
- editing drafts that permit offline work.

Synchronization resumes when networking returns.

---

## 17. Hardware progressive enhancement

LifeBook branches on Capability, not model:

```text
input.touch
input.physical_page_key
input.pen*
display.fast_refresh
display.color
light.frontlight*
audio.output
bluetooth.*
```

Fewer capabilities mean graceful feature reduction, not a different LifeBook codebase.

---

## 18. LifeBook product phases

### Phase A

```text
LifeBook skeleton
baga.ui
lifecycle
storage
lsqlite3
SQLite schema/migration
offline start
```

### Phase B

```text
baga.library
baga.reader
reading progress
notes/highlights
Reader Anchor
```

### Phase C

```text
Articles
Q&A
Comments
Public Notes
SQLite cache / FTS
```

### Phase D

```text
Life Records
Time Capsule
Automerge prototype for truly concurrent objects
```

### Phase E

```text
AI
Pen / Color / Audio enhancements
```

Kindle Platform/Client engineering order is not defined by this section; it follows the Kindle Freeze's compatibility-first substrate phases.

---

## 19. Acceptance baseline

LifeBook Reference baseline SHOULD satisfy:

1. same `lifebook.ikp` across Kindle / Android E-Paper;
2. core business logic does not branch by Vendor;
3. device/platform capabilities only through `baga.*`;
4. relational data uses formal `lsqlite3` / SQLite;
5. SQLite schema/migration survives update/restart reliably;
6. Reader is not bound to EPUB;
7. Reader Anchor does not depend on KOReader private schema;
8. true CRDT cases prefer Automerge rather than a new generic CRDT;
9. Automerge may be whole/modular; `automerge-repo` is not mandatory;
10. offline start works;
11. sync failure does not damage committed local data;
12. sleep/wake restores correctly;
13. failed update does not delete books, notes, or SQLite DB;
14. relevant BICTS passes;
15. Kindle build does not let LifeBook directly import KOReader / KPM / MRPI / KUAL / sh_integration private interfaces;
16. the same `lifebook.ikp` does not fork for `kindlepw2`, `kindlehf`, or other native targets.

---

## 20. Final rule

> **LifeBook implements LifeBook product logic; device differences belong to Baga Ink; mature general software capabilities reuse mature ecosystems directly. Use SQLite as SQLite, prefer Automerge where CRDT is genuinely needed, and reuse KOReader deeply inside the Kindle Platform.**

> **For Kindle bootstrap, KPM/MRPI, Home Entry, KOReader pinning, Platform Core, and IKP Package Manager boundaries, the Kindle Implementation Architecture Freeze is the code-starting baseline.**
