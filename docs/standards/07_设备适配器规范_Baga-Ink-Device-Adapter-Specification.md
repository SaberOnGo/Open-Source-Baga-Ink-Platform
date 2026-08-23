# Baga Ink 设备适配器规范 / Baga Ink Device Adapter Specification

> **文档级别：一级平台规范**  
> **状态：Draft v0.4**  
> **日期：2026-08-23**  
> **上位文档：`01_顶层战略与架构_Baga-Ink-Platform-Strategy.md`**  
> **配套规范：`03_API规范_Baga-Ink-API-Specification.md`、`04_能力注册表_Baga-Ink-Capability-Registry.md`、`08_兼容性标准_Baga-Ink-Compatibility-Standard.md`、`10_兼容性测试套件_Baga-Ink-Compatibility-Test-Suite.md`、`13_标准库与成熟组件采用规范_Baga-Ink-Standard-Libraries-and-Adopted-Components.md`**

---

## 0. 目的

Device Adapter 是 Baga Ink Platform 与具体设备 / OS / Vendor SDK 之间的标准适配边界。

它解决：

> **设备实现可以不同，但上层 `baga.*` 的设备/平台语义保持统一。**

它不负责重新包装 SQLite、Automerge 等成熟通用软件库。

---

# 1. 架构位置

```text
Universal / Enhanced IKP Apps
            │
            ▼
Baga Ink API / Baga Lua Profile
            │
            ▼
   Baga Ink Platform Core
            │
            ▼
   Baga Ink Device Adapter
            │
      ┌─────┴───────────┐
      ▼                 ▼
 Kindle OS /        Android /
 Homebrew           Vendor SDK
```

内部复用 KOReader、FBInk、SQLite、Automerge、Vendor SDK 时，上图不增加新层。

Standard Libraries 由 `13` 规范负责，不是 DeviceAdapter module。

---

# 2. Adapter 职责

```text
Device identification
Capability detection
Display / refresh
Input
Storage sandbox / path mapping
Lifecycle
Power
Network device bridge
Frontlight
Pen
Audio
Bluetooth
System events
Diagnostics
Device quirks
```

Adapter 最重要的责任是准确表达真实设备能力。

---

# 3. 成熟实现优先，但先判断是否属于 Adapter

实现一个需求前必须先判断：

```text
设备 / OS / Vendor 差异？
→ Device Adapter / baga.*

成熟通用软件能力？
→ Standard Library / Adopted Component
```

例子：

```text
Kindle framebuffer / touch / power
→ Adapter，可复用 KOReader / FBInk

BOOX Pen / refresh
→ Adapter，可复用 Vendor SDK

SQLite relational DB
→ Standard Library，不属于 Adapter，不存在 baga.data

Automerge CRDT
→ Adopted Foundation，不属于 Adapter，不等于 baga.sync
```

MUST NOT 因采用一个 library 而机械增加：

```text
Generic Provider Layer
Engine Layer
Runtime Layer
Library Adapter Layer
```

---

# 4. Adapter 不负责什么

禁止：

```text
App → adapter.boox.fastRefresh()
App → adapter.kindle.shell()
App → adapter.koreader.xpointer()
App → adapter.sqlite.query()
App → adapter.automerge.merge()
```

设备能力正确方向：

```text
App → baga.* → Platform Core → Device Adapter → Device/OS
```

成熟标准库正确方向：

```text
App → lsqlite3 / adopted standard library
```

Device Adapter 不负责：

- App 业务逻辑；
- Market 业务；
- LifeBook 私有功能；
- SQLite database semantics；
- CRDT algorithm；
- 将第三方库私有对象变成 Baga API。

---

# 5. Adapter Identity / Device Descriptor

Adapter SHOULD 提供：

```text
adapter_id
adapter_version
device_family
platform_family
supported_firmware_range
compatibility_standard_version
```

Device Descriptor 最低包括：

```text
manufacturer
model
model_id
platform_family
os_or_firmware_version
screen_width
screen_height
orientation
capabilities
```

这些用于诊断；Universal App 核心业务不按 model/vendor 分支。

---

# 6. Capability Detection

```text
has(capability) -> boolean
list_capabilities() -> set
```

Capability 必须：

- 基于当前设备 / 固件真实状态；
- 不因同系列其他设备有就误报；
- 未验证能力不标 stable；
- 不因内部 library 存在就自动声明其所有能力。

SQLite / lsqlite3 / Automerge 不属于 Device Capability。

---

# 7. Display Adapter

最低职责：

```text
get_size()
get_orientation()
refresh(region, mode)
full_refresh()
supports_display_mode(mode)
```

Baga Display Intent：

```text
AUTO
TEXT
QUALITY
FAST
ANIMATION
```

Adapter 可复用 KOReader / FBInk / Vendor E-Paper SDK，但不暴露 waveform ID。

---

# 8. Input Adapter

统一语义：

```text
confirm
back
menu
page_next
page_previous
focus_next
focus_previous
```

来源可以是：

```text
touch
pen
physical_button
keyboard
volume key
```

App 不依赖 Linux/Android/Kindle private keycode。

---

# 9. Touch / Pen

`input.touch` 至少提供：

```text
pointer_down
pointer_move
pointer_up
cancel
```

Pen 可选能力：

```text
input.pen
input.pen.pressure
input.pen.eraser
input.pen.hover
input.pen.low_latency
```

Vendor Pen API 留在 Adapter 内部。

---

# 10. Storage Adapter

逻辑根：

```text
appdata/
cache/
documents/
downloads/
```

Platform / Adapter 共同保证：

- App sandbox；
- path normalization；
- `..` / unauthorized absolute path rejection；
- disk-full error；
- Platform update 不默认删除 App data。

## 10.1 Standard Library path bridge

`baga.storage.resolve_path()` MAY 为 `lsqlite3` 等正式 Standard Library 提供当前 App 被授权的运行时路径。

但：

> **`resolve_path()` 不是弱 OS sandbox 平台的完整安全边界。**

在 Kindle 等系统上，SQLite 还必须通过 sandbox-aware VFS / 等价 I/O confinement 约束 `ATTACH`、journal、WAL、temp DB 等所有文件访问。

详细规则见 `13`。

---

# 11. User Library Bridge

用户书库通过：

```text
baga.library
+ storage.user_library
+ library.read / library.write
```

暴露。

IKP 不扫描 Kindle `/documents` 或 Android Vendor private path/database。

---

# 12. Lifecycle / Power

Adapter 将底层事件转换为：

```text
start
resume
pause
sleep
wake
stop
```

Power MAY 提供：

```text
battery_level
charging_state
keep_awake
```

不支持返回 `not_supported/unknown`，不得伪造。

---

# 13. Network Adapter

声明网络能力后，Adapter 必须处理：

```text
connectivity state
network change
sleep/wake disruption
DNS / TLS / timeout error mapping
```

HTTP/TLS stack 可以复用成熟实现；App 只看 `baga.network`。

Automerge sync protocol（若使用）是 Local-first protocol，不属于 Network Adapter API。

---

# 14. Frontlight / Audio / Bluetooth

只有真实可控时才声明：

```text
light.frontlight*
audio.output
bluetooth.*
```

具体 Vendor API 不穿透。

---

# 15. Error / Event / Main Loop

Adapter 将底层错误映射成稳定 Baga error semantics。

Event SHOULD：

- 有序；
- 可去重；
- 先进入 Platform Core；
- 不让 Vendor/library callback 直接进入 App。

Adapter MAY 复用 Android main thread、KOReader event loop 等，无需再造 “Baga Event Engine”。

---

# 16. Logging / Self-check

Diagnostics SHOULD 记录：

```text
model / firmware
adapter version
capability detection
screen/input/network backend
display/input failures
power/network events
unexpected vendor errors
```

普通日志不得写用户正文/笔记/凭据。

Self-check 至少验证：

```text
Device identity
Display
Input
Storage sandbox
Lifecycle
Capability consistency
```

SQLite Profile 由 BICTS / Standard Library test 验证，而不是 Adapter Self-check 重新定义。

---

# 17. Kindle / Android 设备规范

Kindle：见 `11_Kindle适配规范_Baga-Ink-Kindle-Adapter.md`。

Android E-Paper：见 `12_Android墨水屏适配规范_Baga-Ink-Android-E-Paper-Adapter.md`。

---

# 18. Android Vendor Specialization

Android 内部 MAY：

```text
Generic Android Adapter
├─ BOOX specialization
├─ iReader specialization
├─ Bigme specialization
└─ Other vendor specialization
```

这些只处理真实 Vendor SDK / hardware differences。

---

# 19. Capability Provider 的严格边界

Capability Provider 只用于**确实需要受控扩展的设备/厂商高级能力**，例如某些 Vendor Pen / E-Paper 特性。

它：

- MUST 通过标准 Capability/API 暴露；
- MUST 不成为任意 Library 的包装惯例；
- MUST 不用于 SQLite、Automerge、KOReader 仅仅因为它们是库；
- MUST 不泛化为所有 Baga API 的必经层。

错误机械分层：

```text
KOReaderProvider
SQLiteProvider
AutomergeProvider
```

如果这些名字只是“用了某库”，它们不属于 Baga 公共架构。

---

# 20. Adapter Versioning / Compatibility

Compatibility Record SHOULD 记录：

```text
Device Model
Firmware Range
Platform Version
Adapter Version
Lua Profile Version
Compatibility Standard Version
BICTS Version
```

Adapter 更新后运行受影响的 BICTS。

---

# 21. 安全原则

Adapter 位于高权限边界：

- 不暴露 arbitrary shell；
- 不暴露 Android Context；
- 不暴露 Vendor SDK object；
- 不暴露内部高权限 library escape；
- 校验 path/region/arguments；
- 遵守 Platform Policy。

---

# 22. OEM 实现流程

```text
Vendor hardware/firmware
  ↓
Implement Adapter
  ↓
Reuse mature components
  ↓
Self-check
  ↓
BICTS
  ↓
Declare verified capabilities
  ↓
Baga Ink Compatible
```

OEM 不需要修改第三方 IKP。

---

# 23. 顶层 Adapter 模型

```text
DeviceAdapter
├─ Identity
├─ Capabilities
├─ Display
├─ Input
├─ Storage/Sandbox
├─ Lifecycle
├─ Power
├─ Network       optional
├─ Touch/Pen     optional
├─ Frontlight    optional
├─ Audio         optional
└─ Bluetooth     optional
```

不包含：

```text
SQLite
Automerge
Reader database
CRDT engine
```

这些不是 Device Adapter 层次。

---

# 24. 最终验收标准

> **正确的 Adapter 让 IKP 用统一 `baga.*` 获得设备能力，同时不妨碍 IKP 直接使用 Baga Lua Profile 已正式采用的成熟 Standard Libraries。**

如果 App 必须知道这是 Kindle/BOOX/iReader 才能工作，Adapter 失败；如果一个成熟通用库被无意义塞进 Adapter/Provider 才能使用，标准分层也失败。