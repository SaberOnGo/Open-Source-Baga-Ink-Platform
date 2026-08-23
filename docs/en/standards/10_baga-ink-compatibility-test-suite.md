# Baga Ink Compatibility Test Suite (BICTS)

> **Document level:** First-level Platform Standard / Compatibility Test Suite  
> **Document ID:** `standards.10`  
> **Locale:** English (`en`)  
> **Status:** Draft v0.4  
> **Date:** 2026-08-23  
> **Parent:** `01_baga-ink-platform-strategy.md`  
> **Related:** Standards 04, 07, 08, 13  
> **Counterpart:** `docs/zh-CN/standards/10_兼容性测试套件.md`

---

## 0. Purpose

BICTS, the **Baga Ink Compatibility Test Suite**, is the primary executable evidence for whether a concrete Device / Firmware / Platform / Adapter combination may claim Baga Ink compatibility.

It validates not only the public Baga API, but the whole contract chain:

```text
Device Adapter
→ Platform Core
→ Baga Ink API / Baga Lua Profile
→ Standard Libraries
→ IKP execution
→ lifecycle / data safety / recovery
```

Core rule:

> **Documentation and successful compilation are not compatibility evidence. A compatibility claim requires test evidence against the exact combination being certified.**

---

## 1. Test layers

BICTS must remain distinct from lower-level Adapter Contract Tests.

### 1.1 Adapter Contract Tests

Directly validate Adapter implementation semantics such as:

```text
Factory / probe
Descriptor
Capability consistency
Display / Input / Storage / Lifecycle / Power interfaces
Error normalization
Profile / Quirk selection
Self-test
```

These answer:

> **Does the Adapter correctly implement Standard 07?**

### 1.2 BICTS

BICTS validates the full public behavior of:

```text
Device
+ Firmware / OS
+ Baga Platform
+ Device Adapter
+ Baga Lua Profile
+ Standard Libraries
```

These answer:

> **Can this concrete combination actually behave like the Baga Ink Platform contract exposed to Apps?**

Both layers are expected for formal compatibility evidence.

---

## 2. Test identity and result model

Every test SHOULD have a stable Test ID, for example:

```text
BICTS-BASE-001
BICTS-DISPLAY-003
BICTS-STORAGE-007
BICTS-SQLITE-011
BICTS-READER-005
```

Result states:

```text
PASS
FAIL
SKIP
NOT_APPLICABLE
BLOCKED
```

A formal report must not silently omit mandatory tests.

---

## 3. Certification tuple

Every BICTS report MUST bind at least:

```text
Device family
Device model / model_id
Firmware / OS exact version or verified range
Native Build Target / ABI Profile when applicable
Device Profile version
Quirk Set version
Baga Platform version
Device Adapter version
Adapter Contract version
Baga Lua Profile version
Standard Library versions/profiles
BICTS version
```

Where relevant, include adopted-component versions/commits and source digests.

---

## 4. Base Compatibility suite

Base Compatible devices MUST pass tests covering:

```text
display.basic
input.navigation
storage.app_sandbox
power.sleep_wake
platform.lifecycle
```

as well as the mandatory Baga Lua Profile / Standard Libraries for the declared Platform version.

The Base suite is the minimum cross-device loop for a portable IKP.

---

## 5. Platform startup and Probe IKP

A Reference Probe IKP SHOULD verify:

```text
Platform starts
Adapter resolves
Descriptor is readable
Capability Snapshot is available
basic UI can render
navigation input works
App-local state persists
sleep / wake works
App can restart without corruption
```

A Probe app is a platform diagnostic/reference application. It does not replace the formal suite.

---

## 6. Display tests

Minimum display coverage includes:

```text
screen dimensions valid
orientation valid
basic visible refresh works
TEXT / QUALITY refresh intent safe
region bounds safe
partial refresh only declared when actually supported
unsupported intent downgrades safely or returns not_supported
no vendor waveform ID leaks through public API
```

If declared, test:

```text
display.partial_refresh
display.fast_refresh
display.quality_refresh
display.animation
display.grayscale
display.color
display.rotation
```

Tests SHOULD include a visual/human-verifiable mode on real e-paper devices where automated bitmap comparison cannot prove physical refresh behavior.

---

## 7. Input tests

Base tests verify semantic navigation such as:

```text
confirm
back
page_next
page_previous
focus_next
focus_previous
```

Test optional input only when declared:

```text
input.touch
input.multitouch
input.pen
input.pen.pressure
input.pen.eraser
input.pen.hover
input.pen.low_latency
input.physical_page_key
input.keyboard
```

Raw Kindle keycodes, Android KeyEvent, or vendor event objects must not leak into Universal App semantics.

---

## 8. Lifecycle tests

Verify the semantic lifecycle:

```text
start
resume
pause
sleep
wake
stop
```

Tests SHOULD include:

- repeated sleep/wake;
- wake after network-state change;
- App restart after sleep;
- no high-frequency polling requirement;
- no direct device callback into App bypassing Platform Core.

---

## 9. Power tests

Base:

```text
power.sleep_wake
```

Optional when declared:

```text
power.battery_level
power.charging_state
power.keep_awake
```

Verify that:

- values are plausible;
- unsupported features are not falsely advertised;
- keep-awake may be refused by Platform policy;
- release of keep-awake restores normal behavior;
- sleep/wake does not corrupt confirmed App data.

---

## 10. Storage sandbox tests

Base storage tests must verify:

```text
App has an authorized private root
logical roots map safely
`..` escape rejected
unauthorized absolute paths rejected
symlink / canonical-path escape rejected
App package and App data separated
disk-full maps to stable error
Platform update does not delete App data by default
```

Cross-App private-data access MUST fail unless a future explicit shared-data standard allows it.

---

## 11. SQLite / lsqlite3 mandatory profile tests

For Platforms declaring the current Baga Lua Profile, BICTS MUST validate the mandatory `lsqlite3` Standard Library against the pinned SQLite profile.

Coverage includes at least:

```text
require("lsqlite3") succeeds
SQLite version/profile reported correctly
open authorized appdata DB
create table
prepared statements
transactions
indexes
foreign keys
BLOB
basic JSON/FTS behavior when part of the pinned profile
close/reopen durability
error semantics
```

### 11.1 Sandbox / VFS coverage

The test suite must attempt unauthorized escape through SQLite-specific I/O paths, not only through `baga.storage`.

At minimum test:

```text
main database path
ATTACH DATABASE
rollback journal
WAL
SHM
temporary database / temp files
URI filename / vfs override where applicable
symlink / canonical escape
loadable extension
```

On weak-OS-sandbox platforms such as Kindle, a legal `resolve_path()` path is not sufficient evidence. SQLite itself must be confined by a sandbox-aware VFS or equivalent mechanism.

### 11.2 Transaction / lifecycle durability

Verify that a committed transaction remains valid across:

```text
close/reopen
App restart
sleep/wake
normal device restart where the durability profile requires it
```

---

## 12. IKP execution tests

Verify:

```text
valid IKP launches
invalid format rejected
unsafe path rejected
forbidden native executable rejected
unsupported API range rejected
missing required Capability rejected
undeclared Permission cannot be acquired
publisher/signature validation enforced where required
main.lua never executes before validation succeeds
```

Developer Mode exceptions must remain clearly separated from production-signed behavior.

---

## 13. Permission tests

At minimum verify:

```text
undeclared permission request denied
denied permission produces stable error
revocation becomes effective
App cannot bypass Permission through Lua standard environment
library/user-file access respects scope
high-risk device controls require their declared permission
```

The lack of an Android-style system permission dialog does not exempt Kindle or other platforms from enforcing the Baga Permission Model.

---

## 14. Network tests

Only required when corresponding network Capabilities are declared.

Coverage SHOULD include:

```text
offline state
online state
connectivity-change event
DNS failure
TLS failure
request timeout
cancelled request
sleep/wake reconnect behavior
```

Apps must not require device-private network APIs.

Automerge sync behavior, when a concrete feature adopts it, belongs to the relevant Local-first/sync test group rather than network-hardware capability tests.

---

## 15. Frontlight / Audio / Bluetooth tests

When declared, verify standardized behavior for:

```text
light.frontlight*
audio.*
bluetooth.*
```

The suite must not infer capability merely from product-generation marketing information.

---

## 16. Reader tests

Reader tests apply only to declared Reader capabilities.

Coverage SHOULD span multiple source types where supported, for example:

```text
EPUB
PDF
TXT
other formats claimed by the Platform
```

Core checks:

```text
supports(source_or_format)
open(source)
position / goto
next_page / previous_page
search where declared
selection where declared
highlight / note where declared
close
```

Apps must not depend on KOReader / MuPDF / CREngine private objects.

---

## 17. Reader Anchor tests

If `reader.anchor` is declared, test:

```text
create_anchor
serialize/pass anchor as opaque Baga value
goto_anchor
resolve_anchor
```

The suite must verify that:

- App does not parse implementation-private locator fields;
- EPUB/PDF/other formats may use different mature internal locator strategies;
- exact resolution and approximate recovery are distinguishable;
- an implementation does not falsely return approximate recovery as exact;
- anchors remain usable across ordinary reopen/relaunch within the declared compatibility range.

`reader.anchor` remains provisional until representative Kindle/Android multi-format evidence exists.

---

## 18. Automerge tests

Automerge is not Base Mandatory.

Run Automerge-related tests only for features/platform modules that actually adopt it.

Possible coverage:

```text
document create/edit
concurrent merge
binary save/load
change history
patch/cursor semantics where used
sync protocol interoperability where explicitly adopted
```

Baga may adopt the full Automerge core or selected modules. `automerge-repo` is not required simply because Automerge is used.

---

## 19. UI tests

Reference UI coverage SHOULD validate:

```text
page renders
focus visible
non-touch semantic navigation works
touch activation works when declared
page_next / page_previous work
monochrome does not lose critical information
compact / larger layouts avoid severe overflow
small interaction does not force unnecessary full refresh
```

Exact pixel-identical rendering across device families is not required.

---

## 20. Update / rollback tests

Where the update protocol applies, test:

```text
stage before activation
invalid update never activates
health check / probation state
last-known-good retained
rollback restores previous package
App data preserved by default
package rollback does not silently roll back user data
migration failure does not leave half-migrated state
```

Platform update and IKP App update are distinct transactions.

---

## 21. Data-protection tests

On supported devices, install/update/repair/uninstall tests MUST confirm that Baga does not unexpectedly delete:

```text
user books
user notes
user documents
App private data
App SQLite databases
```

Any test path that requires factory reset as the normal recovery mechanism blocks a normal Compatible claim.

---

## 22. Error normalization tests

Backend errors must map into stable Baga semantics.

Coverage includes representative failures for:

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

Raw vendor/backend error codes may appear in diagnostics but cannot become the App contract.

---

## 23. Capability truthfulness tests

For each declared Capability, BICTS SHOULD verify that:

- the corresponding subsystem/mechanism exists;
- the advertised semantics can actually be exercised;
- unsupported optional mechanisms return absent / `not_supported`;
- firmware-specific disabled behavior is not still advertised as supported;
- Device Profile expectations do not override contradictory runtime evidence.

---

## 24. Device Profile / Quirk tests

Where Profiles/Quirks are used, verify:

```text
exact match behavior
unknown firmware is conservative
native target / profile / quirk are distinct dimensions
quirk only activates within its declared range
quirk does not leak into public Capability names
```

---

## 25. Security tests

The suite MUST include negative tests for:

```text
path traversal
sandbox escape
malformed refresh region / bounds
malformed IKP
forbidden native payload
permission bypass attempt
raw shell escape attempt
SQLite VFS/extension escape
corrupt state / package recovery
```

A malformed App must not be able to corrupt Platform integrity or arbitrary user data.

---

## 26. Performance / resource evidence

BICTS does not require identical performance across hardware, but the certified combination should record basic evidence such as:

```text
Platform launch viability
Probe IKP viability
mandatory SQLite workload viability
sleep/wake stability
memory/resource behavior on representative use
```

Resource-intensive optional capabilities may have additional profiles/tests.

---

## 27. Reference device matrix

The project SHOULD maintain representative devices across:

```text
Kindle native targets / major firmware families
Generic Android E-Paper
representative vendor-specialized Android devices
```

A single passing device is insufficient evidence for an entire family unless the Compatibility policy explicitly defines a verified range and the evidence supports it.

---

## 28. Host, simulator, and real-device split

Tests SHOULD be divided into:

```text
host/mock
→ deterministic contract logic, parsers, sandbox fixtures, generated interfaces

simulator/emulator
→ Platform/Lua/UI logic where available

real device
→ physical refresh, real input, lifecycle, power, filesystem/vendor behavior
```

A Mock Adapter is excellent for contract development but cannot produce a real-device compatibility certificate.

---

## 29. Automation and artifacts

BICTS SHOULD produce machine-readable artifacts containing:

```text
suite version
certification tuple
individual test results
failure details
Adapter Contract Test reference
logs / screenshots / device evidence references
start/end time
```

CI MAY validate host-side suites automatically. Device labs or controlled manual runners may provide real-device evidence.

---

## 30. Promotion gate

A combination may move:

```text
Unsupported / Unknown
→ Experimental
→ Compatible
```

only when the required evidence for that level exists.

A firmware upgrade, Platform major change, Adapter major change, or meaningful adopted-component change MAY invalidate prior evidence and require regression.

---

## 31. Stable Standard Library regression

If the pinned SQLite / lsqlite3 baseline changes, the corresponding BICTS coverage MUST rerun.

Examples:

```text
SQLite version
compile options
lsqlite3 bridge
sandbox VFS behavior
FTS/JSON profile
```

Mature-library adoption does not remove the need for compatibility evidence.

---

## 32. Minimum evidence for a formal Compatibility Record

A formal record SHOULD reference:

```text
Adapter Contract Test result
Base BICTS result
optional Capability profile results
SQLite / Standard Library profile result
update/recovery/data-protection result
security negative-test result
real-device evidence
```

The report should be reproducible enough for another maintainer/OEM to understand what was actually certified.

---

## 33. Final principle

> **BICTS exists so "Baga Ink Compatible" means a tested public contract, not a hopeful statement that the software happened to launch once.**

Compatibility is a property of an exact, evidenced combination — not of a brand name in the abstract.
