# Baga Ink 设备适配器可执行契约与 SDK 设计 / Baga Ink Device Adapter Executable Contract and SDK Design

> **文档级别：Approved Design / 实施设计**  
> **状态：Design Baseline v0.1**  
> **日期：2026-08-23**  
> **上位规范：`../standards/07_设备适配器规范_Baga-Ink-Device-Adapter-Specification.md`**  
> **设备参考：`../standards/11_Kindle适配规范_Baga-Ink-Kindle-Adapter.md`、`../standards/12_Android墨水屏适配规范_Baga-Ink-Android-E-Paper-Adapter.md`**

---

## 0. 目的

`07 Device Adapter Contract` 已经定义设备移植者必须实现的语义契约。

本文档设计下一阶段如何把该 Contract 转换成：

```text
机器可读定义
+ generated SDK
+ Mock Adapter
+ Contract Tests
+ Kindle/Android implementation skeleton
```

目标：

> **让一个没有参与 Baga Ink 历史讨论的 OEM/第三方开发者，只读取规范和生成的 SDK，就能实现一个设备 Adapter，而不需要靠复制 Kindle 代码猜接口。**

本文档不是新的公共架构层，不改变 `baga.*`、IKP 或 Device Adapter 的规范语义。

---

# 1. 为什么需要可执行 Contract

仅靠 Markdown 长期会出现：

```text
Rust interface 与文档漂移
C header 与 Kotlin interface 不一致
Kindle/Android 对 error enum 理解不同
新增字段破坏旧 Adapter
Mock 与真实实现行为不一致
BICTS 无法自动确认 Adapter contract version
```

因此 SHOULD 建立单一机器源：

```text
spec/adapter/
```

由它生成语言接口、文档表和测试 fixture。

文字规范 `docs/standards/07` 仍然是语义权威；机器格式必须与文字规范同步，不能成为第二套协议。

---

# 2. v1 不做什么

明确不做：

```text
动态下载 Native Adapter plugin
稳定跨编译器 C++ ABI
dlopen arbitrary third-party adapter
Adapter 独立 daemon / Binder / RPC
JSON serialization bridge between Core and Adapter
每个 subsystem 独立进程
```

第一阶段采用：

```text
machine-readable IDL
       ↓
codegen
       ↓
compile-time / package-time Adapter implementation
       ↓
direct typed calls
```

如果未来要支持动态 Native Adapter Module，单独设计供应链与 ABI，不在 v0.1 偷渡。

---

# 3. Proposed Repository Layout

建议：

```text
spec/
└── adapter/
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
    └── frozen/
        └── v0.1/

sdk/
└── adapter/
    ├── generated/
    │   ├── rust/
    │   ├── c/
    │   └── kotlin/
    ├── mock/
    └── README.md

tools/
└── baga-adapter-codegen/

tests/
├── adapter_contract/
└── adapter_mock/

platform/
└── adapters/
    ├── mock/
    ├── kindle/
    └── android/
```

目录可以在实施中微调，但职责分离 SHOULD 保持。

---

# 4. IDL 应描述什么

IDL 只描述稳定 Contract surface：

```text
interfaces
methods
types/enums
required vs optional
errors
events
version introduced
deprecation metadata
default/absent semantics
```

IDL 不描述：

```text
Kindle waveform
BOOX SDK class
KOReader object
thread implementation
Rust allocator
Android Context
build toolchain detail
```

这些属于实现。

---

# 5. Contract Root 示例

概念 YAML：

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
  display:
    required: true
  input:
    required: true
  storage:
    required: true
  lifecycle:
    required: true
  power:
    required: true
  network:
    required: false
  light:
    required: false
  audio:
    required: false
  bluetooth:
    required: false
  user_library:
    required: false
```

这只是设计示例；实际 schema 需测试驱动冻结。

---

# 6. Generated Rust Interface

Rust 适合作为 Baga Reference Platform Core / Kindle native glue 的候选语言之一。

Codegen 目标形态可类似：

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

这不是当前冻结源码，而是 Codegen 输出形态目标。

Rust trait 版本与机器 IDL 必须一致，不能人工另维护一份。

---

# 7. Generated C Interface

为了兼容成熟 C/C++/Homebrew 生态，SHOULD 生成 C contract。

目标形式：

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

C ABI 在同一个 Platform build 内使用即可；v0.1 不承诺任意第三方二进制跨版本 `dlopen` 兼容。

---

# 8. Generated Kotlin Interface

Android Platform SHOULD 能生成：

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

Generic Android 与 BOOX/iReader specialization 均实现同一 Contract。

---

# 9. AdapterFactory 生成契约

Factory SHOULD 是 SDK 的第一等接口：

```text
probe
create
```

目的：

- 不让 Platform Core 硬编码型号；
- 支持一个 build 中包含多个 Adapter/implementation；
- 支持 Generic Android + Vendor specialization；
- 支持 Kindle profile/quirk runtime selection；
- 支持 Mock Adapter。

Factory probe 必须是非破坏性的。

---

# 10. Event Codegen

IDL SHOULD 定义 tagged typed event，而不是 arbitrary map/JSON。

概念：

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

Codegen 为 Rust/C/Kotlin 生成等价 enum/union/sealed class。

规则：

```text
OS/Vendor callback
      ↓
Adapter normalization
      ↓
Generated AdapterEvent
      ↓
AdapterHost.emit
      ↓
Platform Core
```

不直接进入 Lua/IKP。

---

# 11. Error Codegen

机器源定义稳定 error code：

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

各 backend 可以保存：

```text
backend_name
raw_backend_code
backend_message
```

作为 diagnostics metadata，但公共 mapping 由 generated code 保持一致。

---

# 12. Version Freeze / Compatibility Check

借鉴成熟 stable-interface 管理经验，IDl SHOULD 支持：

```text
spec/adapter/current/
spec/adapter/frozen/v0.1/
```

工具：

```text
baga-adapter-codegen check-compat
baga-adapter-codegen freeze
baga-adapter-codegen generate
```

兼容规则：

```text
MINOR:
+ add optional method
+ add optional/defaulted field
+ add enum value only when unknown-value handling is defined

MINOR MUST NOT:
- delete method
- rename method
- change existing field meaning
- change required → impossible new requirement silently

MAJOR:
→ breaking change allowed through explicit architecture review
```

CI 必须比较 current 与 latest frozen contract。

---

# 13. Mock Adapter

Mock Adapter 是 Device Adapter Contract 的 Reference Implementation，不是普通测试小工具。

建议：

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

Mock Profile fixture：

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

用途：

- Core 开发；
- UI/IKP host test；
- Adapter SDK tutorial；
- Contract Test reference result；
- CI。

---

# 14. Kindle Adapter Skeleton

第一阶段 `platform/adapters/kindle/` SHOULD 只建立 Contract skeleton，不先重写底层能力：

```text
platform/adapters/kindle/
├── factory.*
├── adapter.*
├── common/
├── display/
├── input/
├── storage/
├── lifecycle/
├── power/
├── network/
├── light/
├── library/
├── device_profiles/
├── quirks/
└── build_targets/
```

Display/Input 等文件的首要工作是：

```text
bind to pinned KOReader / FBInk / Kindle mechanism
→ normalize
→ satisfy generated interface
```

而不是先自行实现 equivalent stack。

---

# 15. Android Adapter Skeleton

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

Generic Android 实现 Base Contract；Vendor specialization 只覆盖 E-Paper refresh、Pen、frontlight 等真正差异。

---

# 16. Contract Tests 结构

建议：

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

同一测试定义 SHOULD 能作用于：

```text
Mock Adapter
Kindle Adapter
Android Adapter
future OEM Adapter
```

其中 host 无法验证的真实硬件行为，以 device-runner / BICTS 补充。

---

# 17. Adapter SDK Developer Experience

未来开发者体验 SHOULD 接近：

```text
baga adapter new my-device
baga adapter generate
baga adapter check
baga adapter test --mock
baga adapter test --device <id>
baga adapter report
```

`new` 生成：

```text
factory skeleton
required subsystem stubs
descriptor/profile fixture
contract tests
README
```

目标不是复制某个通用跨平台框架，而是降低 Baga 新设备 Port 的实现和验证成本。

---

# 18. Adapter 与 BICTS 数据衔接

Adapter Contract test summary SHOULD 输出机器可读 artifact：

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

BICTS Compatibility Report 引用此 artifact，而不是重新手填一份 Adapter 事实。

---

# 19. Dependency / License Manifest

每个 Reference Adapter release SHOULD 生成：

```text
adapter dependency manifest
```

记录：

```text
upstream project
version / commit
source digest
license
patch set
native target
which subsystem uses it
```

例如 Kindle：

```text
KOReader → display/input shared device knowledge
FBInk → display backend
Kindle OS mechanism → lifecycle/power/light
```

KPM/KindleTool 等若不属于 Adapter，应记录在 Platform build/install manifest，而不是 Adapter dependency manifest 中误归类。

---

# 20. CI Gate

Adapter implementation 合并前 SHOULD：

```text
IDL schema valid
IDL compatibility check PASS
Generated outputs clean / reproducible
Mock Adapter Contract Tests PASS
Target Adapter host tests PASS where possible
Target build PASS
Device Contract Tests PASS for supported device
BICTS required suite PASS before Compatible claim
```

Adapter 文档写完不代表 Adapter Compatible。

---

# 21. 实施顺序

建议下一阶段：

```text
Task 1  定义 spec/adapter IDL schema
Task 2  固化 v0.1 Root + core types
Task 3  生成 Rust interface
Task 4  实现 Mock Adapter
Task 5  建立 Contract Test harness
Task 6  生成 C interface
Task 7  建立 KindleHF Adapter skeleton
Task 8  绑定 pinned KOReader/FBInk
Task 9  跑 Kindle Base Contract Tests
Task 10 跑 Baga Probe + Base BICTS
Task 11 再做 Kotlin/Android generated interface
```

不要一开始同时支持全部 Kindle 历史机型。

---

# 22. 设计参考（非规范依赖）

参考的工程思想：

- Android Stable AIDL：结构化接口、冻结版本、自动兼容性检查；
- Zephyr Device Driver Model：typed subsystem API 与 device-specific implementation；
- Chromium Ozone：interfaces not ifdefs、mechanism not policy、集中 platform port；
- Qt QPA：platform backend 与 minimal/headless implementation。

Baga 不采用这些系统的 IPC、driver ABI、window system 或 runtime 作为强制依赖。

---

# 23. 最终原则

> **Device Adapter Contract 必须机器可检查，但不能因此膨胀成新的 Runtime/IPC 系统。IDL/Codegen 的目的只是让标准不漂移，让 Kindle、Android 和未来 OEM 实现真正共享同一个 Porting Contract。**
