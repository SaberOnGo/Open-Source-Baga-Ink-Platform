# Baga Ink Device Adapter Executable Contract and SDK Design

> **Document level:** Approved Design / Implementation Design  
> **Document ID:** `design.02`  
> **Locale:** English (`en`)  
> **Status:** Design Baseline v0.1  
> **Date:** 2026-08-23  
> **Governing standard:** `docs/en/standards/07_baga-ink-device-adapter-specification.md`  
> **Device references:** Standards 11 and 12  
> **Counterpart:** `docs/zh-CN/design/02_设备适配器可执行契约与SDK设计.md`

---

## 0. Purpose

Standard 07 already defines the semantic Device Adapter Contract.

This design specifies how to turn that contract into:

```text
machine-readable definition
+ generated SDK
+ Mock Adapter
+ Contract Tests
+ Kindle / Android implementation skeletons
```

Goal:

> **An OEM or third-party developer who did not participate in Baga's historical discussions should be able to read the Standard and generated SDK and implement a Device Adapter without copying Kindle code to guess the interface.**

This design does not introduce a new public architecture layer and does not change `baga.*`, IKP, or Device Adapter semantics.

---

## 1. Why an executable Contract is needed

Markdown-only maintenance eventually causes drift:

```text
Rust interface differs from docs
C header differs from Kotlin interface
Kindle / Android interpret error enums differently
new fields break old Adapters
Mock behavior differs from real implementation
BICTS cannot automatically identify Contract version
```

Therefore create a single machine source under:

```text
spec/adapter/
```

and generate language interfaces, documentation tables, and test fixtures from it.

The prose Standard remains semantic authority. Machine IDL must track the Standard rather than becoming a second protocol.

---

## 2. Explicit v0.1 non-goals

Do not build:

```text
dynamically downloaded Native Adapter plugins
stable cross-compiler C++ ABI
arbitrary third-party dlopen adapters
Adapter daemon / Binder / RPC
JSON serialization bridge between Core and Adapter
one process per subsystem
```

Phase one:

```text
machine-readable IDL
      ↓
codegen
      ↓
compile-time / package-time Adapter implementation
      ↓
direct typed calls
```

A future independently signed Native Adapter Module requires a separate ABI/supply-chain design.

---

## 3. Proposed repository layout

```text
spec/adapter/
├── contract.yaml
├── types.yaml
├── descriptor.yaml
├── events.yaml
├── errors.yaml
├── subsystems/
│   ├── display.yaml
│   ├── input.yaml
│   ├── storage.yaml
│   ├── lifecycle.yaml
│   ├── power.yaml
│   ├── network.yaml
│   ├── light.yaml
│   ├── audio.yaml
│   ├── bluetooth.yaml
│   └── user_library.yaml
└── frozen/v0.1/

sdk/adapter/
├── generated/{rust,c,kotlin}/
├── mock/
└── README.md

tools/baga-adapter-codegen/

tests/
├── adapter_contract/
└── adapter_mock/

platform/adapters/
├── mock/
├── kindle/
└── android/
```

Implementation may refine paths, but these responsibility boundaries should remain.

---

## 4. What the IDL describes

The IDL contains only stable Contract surface:

```text
interfaces
methods
types / enums
required vs optional
errors
events
version introduced
deprecation metadata
default / absent semantics
```

It does NOT describe:

```text
Kindle waveform
BOOX SDK class
KOReader object
thread implementation
Rust allocator
Android Context
build-toolchain detail
```

Those are implementation details.

---

## 5. Contract-root example

Conceptual YAML:

```yaml
contract:
  name: baga.device_adapter
  version: 0.1

root:
  interface: BagaDeviceAdapter
  required:
    - descriptor
    - capabilities
    - init
    - self_test
    - shutdown

subsystems:
  display: {required: true}
  input: {required: true}
  storage: {required: true}
  lifecycle: {required: true}
  power: {required: true}
  network: {required: false}
  light: {required: false}
  audio: {required: false}
  bluetooth: {required: false}
  user_library: {required: false}
```

This is a design example; final schema is frozen through tests.

---

## 6. Generated Rust interface

A target form may resemble:

```rust
pub trait DeviceAdapter: Send {
    fn descriptor(&self) -> &DeviceDescriptor;
    fn capabilities(&self) -> &CapabilitySnapshot;
    fn init(&mut self, host: &dyn AdapterHost) -> AdapterResult<()>;
    fn self_test(&mut self, mode: SelfTestMode) -> SelfTestReport;
    fn display(&mut self) -> &mut dyn DisplayAdapter;
    fn input(&mut self) -> &mut dyn InputAdapter;
    fn storage(&mut self) -> &mut dyn StorageAdapter;
    fn lifecycle(&mut self) -> &mut dyn LifecycleAdapter;
    fn power(&mut self) -> &mut dyn PowerAdapter;
    fn network(&mut self) -> Option<&mut dyn NetworkAdapter>;
    fn shutdown(&mut self) -> AdapterResult<()>;
}
```

This is not frozen source code; it is a target shape for code generation.

Generated Rust interfaces and the machine IDL MUST not be manually maintained as independent contracts.

---

## 7. Generated C interface

To integrate mature C/C++/Homebrew code, generate a C contract.

Target shape:

```c
struct baga_display_adapter_v1 {
    int (*get_info)(void *ctx, struct baga_display_info *out);
    int (*refresh)(void *ctx, const struct baga_refresh_request *req);
};

struct baga_device_adapter_v1 {
    void *ctx;
    const struct baga_display_adapter_v1 *display;
    const struct baga_input_adapter_v1 *input;
    const struct baga_storage_adapter_v1 *storage;
    const struct baga_lifecycle_adapter_v1 *lifecycle;
    const struct baga_power_adapter_v1 *power;
    const struct baga_network_adapter_v1 *network; /* nullable */
};
```

The C ABI only needs to work inside the same Platform build in v0.1. Arbitrary third-party cross-version `dlopen` compatibility is not promised.

---

## 8. Generated Kotlin interface

Android target shape:

```kotlin
interface DeviceAdapter {
    val descriptor: DeviceDescriptor
    val capabilities: CapabilitySnapshot

    fun init(host: AdapterHost): AdapterResult<Unit>
    fun selfTest(mode: SelfTestMode): SelfTestReport

    val display: DisplayAdapter
    val input: InputAdapter
    val storage: StorageAdapter
    val lifecycle: LifecycleAdapter
    val power: PowerAdapter
    val network: NetworkAdapter?

    fun shutdown(): AdapterResult<Unit>
}
```

Generic Android and Vendor specializations implement the same contract.

---

## 9. AdapterFactory is first-class

Generated SDK should include:

```text
probe
create
```

Factory prevents Platform Core from hard-coding models and supports:

- multiple implementations in one build;
- Generic Android + Vendor specialization;
- Kindle Device Profile / Quirk runtime selection;
- Mock Adapter.

`probe()` must be non-destructive.

---

## 10. Event code generation

IDL defines tagged typed events rather than arbitrary maps/JSON.

```text
AdapterEvent
├── LifecycleEvent
├── NavigationEvent
├── PointerEvent
├── PenEvent
├── PowerStateEvent
├── NetworkStateEvent
└── CapabilityChangedEvent
```

Codegen produces equivalent Rust enum / C union / Kotlin sealed class.

Flow:

```text
OS / Vendor callback
      ↓
Adapter normalization
      ↓
Generated AdapterEvent
      ↓
AdapterHost.emit
      ↓
Platform Core
```

It does not jump directly into Lua/IKP.

---

## 11. Error code generation

Machine source defines stable errors:

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

Backends MAY retain diagnostics:

```text
backend_name
raw_backend_code
backend_message
```

but generated public mapping stays consistent.

---

## 12. Version freeze and compatibility checks

Support:

```text
spec/adapter/current/
spec/adapter/frozen/v0.1/
```

Tooling:

```text
baga-adapter-codegen check-compat
baga-adapter-codegen freeze
baga-adapter-codegen generate
```

Minor-compatible changes MAY:

```text
add optional method
add optional/defaulted field
add enum value only when unknown-value handling is defined
```

Minor MUST NOT:

```text
delete/rename method
change existing field meaning
silently turn a previously optional behavior into an impossible required behavior
```

Breaking changes require explicit Major-version architecture review.

CI compares Current with the latest frozen contract.

---

## 13. Mock Adapter

Mock Adapter is the Device Adapter Contract's Reference Implementation, not merely a test helper.

Recommended:

```text
MockDeviceAdapter
├── descriptor from fixture
├── capability fixture
├── DisplayAdapter
│   ├── in-memory surface
│   └── PNG/tree snapshot output
├── InputAdapter
│   └── scripted events
├── StorageAdapter
│   └── temporary sandbox
├── LifecycleAdapter
│   └── synthetic sleep/wake
├── PowerAdapter
│   └── synthetic battery/charging
└── NetworkAdapter
    └── synthetic online/offline
```

Example profile:

```yaml
device_family: mock
screen:
  width: 1072
  height: 1448
capabilities:
  - display.basic
  - input.navigation
  - storage.app_sandbox
  - power.sleep_wake
  - platform.lifecycle
```

Uses:

- Core development;
- UI/IKP host tests;
- SDK tutorial;
- reference results for Contract Tests;
- CI.

---

## 14. Kindle Adapter skeleton

Phase-one `platform/adapters/kindle/` should create only the Contract skeleton first:

```text
factory.*
adapter.*
common/
display/
input/
storage/
lifecycle/
power/
network/
light/
library/
device_profiles/
quirks/
build_targets/
```

Display/Input implementation begins by binding:

```text
pinned KOReader / FBInk / Kindle mechanism
→ normalize
→ satisfy generated interface
```

not by rebuilding equivalent stacks.

---

## 15. Android Adapter skeleton

```text
platform/adapters/android/
├── factory
├── common
├── generic
├── vendors/
│   ├── boox
│   ├── ireader
│   ├── bigme
│   └── hanvon
└── quirks
```

Generic Android implements Base Contract. Vendor specialization covers only real E-Paper differences such as refresh, pen, and frontlight.

---

## 16. Contract Test structure

```text
tests/adapter_contract/
├── test_root
├── test_descriptor
├── test_capabilities
├── test_display
├── test_input
├── test_storage
├── test_lifecycle
├── test_power
├── test_events
├── test_errors
├── test_profiles
└── test_quirks
```

The same definition SHOULD run against:

```text
Mock Adapter
Kindle Adapter
Android Adapter
future OEM Adapter
```

Hardware behaviors that cannot be validated on host are completed by device-runner / BICTS.

---

## 17. Adapter SDK developer experience

Target workflow:

```text
baga adapter new my-device
baga adapter generate
baga adapter check
baga adapter test --mock
baga adapter test --device <id>
baga adapter report
```

`new` generates:

```text
factory skeleton
required subsystem stubs
descriptor/profile fixture
contract tests
README
```

The goal is to reduce the cost of implementing/verifying a Baga device port, not to clone a generic cross-platform framework.

---

## 18. Adapter → BICTS evidence

Adapter Contract Test summary SHOULD emit machine-readable evidence:

```json
{
  "adapter_contract": "0.1",
  "adapter_id": "org.baga.adapter.kindle",
  "adapter_version": "0.1.0",
  "profile_id": "...",
  "quirk_set_id": "...",
  "tests": {}
}
```

BICTS Compatibility Report references this artifact rather than manually re-entering Adapter facts.

---

## 19. Dependency / License Manifest

Every Reference Adapter release SHOULD generate an Adapter Dependency Manifest containing:

```text
upstream project
version / commit
source digest
license
patch set
native target
subsystem using it
```

Kindle examples:

```text
KOReader → shared display/input/device knowledge
FBInk → display backend
Kindle OS mechanism → lifecycle/power/light
```

KPM/KindleTool and other non-Adapter components belong in Platform build/install manifests, not incorrectly in Adapter dependency manifest.

---

## 20. CI Gate

Before merging an Adapter implementation:

```text
IDL schema valid
IDL compatibility check PASS
generated outputs clean / reproducible
Mock Adapter Contract Tests PASS
host tests PASS where possible
target build PASS
Device Contract Tests PASS for supported target
BICTS required suite PASS before Compatible claim
```

Writing Adapter docs or compiling does not mean Compatible.

---

## 21. Recommended implementation order

```text
Task 1  define spec/adapter IDL schema
Task 2  freeze v0.1 Root + core types
Task 3  generate Rust interface
Task 4  implement Mock Adapter
Task 5  build Contract Test harness
Task 6  generate C interface
Task 7  create KindleHF Adapter skeleton
Task 8  bind pinned KOReader / FBInk
Task 9  run Kindle Base Contract Tests
Task 10 run Baga Probe + Base BICTS
Task 11 then generate Kotlin / Android interface
```

Do not begin by supporting every historical Kindle model simultaneously.

---

## 22. Design references, not dependencies

Engineering ideas are informed by:

- Android Stable AIDL — structured/frozen interfaces and automated compatibility checks;
- Zephyr Device Driver Model — typed subsystem APIs plus device-specific implementation;
- Chromium Ozone — interfaces not ifdefs, mechanism not policy, centralized platform ports;
- Qt QPA — platform backend and minimal/headless implementations.

Baga does not adopt their IPC, driver ABI, window system, or runtime as mandatory dependencies.

---

## 23. Final rule

> **The Device Adapter Contract must become machine-checkable without expanding into a new Runtime/IPC system. IDL/codegen exist to prevent contract drift so Kindle, Android, and future OEM implementations share one real Porting Contract.**
