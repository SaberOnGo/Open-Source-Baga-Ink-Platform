# Baga Ink Android 墨水屏适配规范 / Baga Ink Android E-Paper Adapter

> **文档级别：首发设备适配规范**  
> **状态：Draft v0.4**  
> **日期：2026-08-23**  
> **上位文档：`07_设备适配器规范_Baga-Ink-Device-Adapter-Specification.md`**  
> **认证依据：`08_兼容性标准_Baga-Ink-Compatibility-Standard.md`、`10_兼容性测试套件_Baga-Ink-Compatibility-Test-Suite.md`**  
> **标准库依据：`13_标准库与成熟组件采用规范_Baga-Ink-Standard-Libraries-and-Adopted-Components.md`**

---

## 0. 目的 / Purpose

本文档定义 Android 墨水屏设备如何接入 Baga Ink Platform。

覆盖包括但不限于：

```text
iReader / 掌阅
BOOX / 文石
Bigme
Hanvon / 汉王
墨案
其他 Android E-Paper
```

核心目标：

> **Android 底层可以继续使用 Kotlin / Java / JNI / Vendor SDK 与成熟开源组件；IKP App 面对统一 Baga Ink API 与 Baga Lua Profile Standard Libraries。**

正式正文只描述当前有效设计。

---

# 1. 架构位置

```text
IKP Apps
   │
   ▼
Baga Ink API / Baga Lua Profile
   │
   ▼
Baga Ink Platform Core
   │
   ▼
Android E-Paper Adapter
   │
   ▼
Android OS + Vendor SDK + Hardware
```

SQLite、lsqlite3、Automerge、Reader libraries、Vendor SDK 不构成新的公共架构层。

---

# 2. 设计原则

Android Adapter / Platform MUST / SHOULD：

1. 先实现 Generic Android Base；
2. 再以内部 specialization 处理 BOOX/iReader/Bigme/Hanvon 等 E-Paper 私有能力；
3. 不要求每个 IKP 引入 Vendor SDK；
4. 不把 Android Context、MotionEvent、Vendor object 暴露给 Universal App；
5. Capability 基于真实 feature probe / verified profile；
6. 同一 `.ikp` 跨厂商运行；
7. 优先复用 Android、SQLite 与成熟开源库；
8. 不因采用 library 就增加 Provider/Engine/Runtime 公共层；
9. IKP 结构化关系数据直接使用 SQLite / `lsqlite3`；
10. Automerge 可整体或拆模块复用，`baga.sync` 继续承担平台调度语义。

---

# 3. Platform APK

Android Platform APK SHOULD 包含：

```text
Platform Core
Embedded Lua Interpreter
Baga Lua Profile
Baga Standard Libraries
Baga Ink API
IKP Package Manager
App Sandbox
Android Device Adapter
Market integration
```

Third-party Baga App = IKP，不需要再做 Baga 专用 APK。

---

# 4. Android Base Adapter

Generic Android SHOULD 使用公共 Android 能力实现：

```text
lifecycle
filesystem sandbox
network
battery / charging
orientation
touch / keyboard
Bluetooth
audio
```

E-Paper refresh、低延迟 Pen、前光等再由厂商内部 specialization 完成。

---

# 5. Vendor Specialization

内部可以组织为：

```text
Android Adapter Common
├─ Generic Android
├─ BOOX specialization
├─ iReader specialization
├─ Bigme specialization
├─ Hanvon specialization
└─ Device quirks
```

这只是 Android Adapter 内部代码组织，不是所有 Baga API 都必须经过的 Provider Layer。

---

# 6. Display / E-Paper Refresh

所有支持设备 MUST 实现 `display.basic`。

按真实能力声明：

```text
display.partial_refresh
display.fast_refresh
display.quality_refresh
display.animation
display.grayscale
display.color
display.rotation
```

厂商内部可能使用 GC / GU / REGAL / A2 / speed / quality 等概念；Baga 只暴露：

```text
AUTO / TEXT / QUALITY / FAST / ANIMATION
```

App 不接触 Vendor waveform 名称。

---

# 7. Touch / Pen / Keys

Adapter 将 Android / Vendor input 归一化到：

```text
touch
pen
keyboard
physical_button
page_next
page_previous
confirm
back
menu
```

Pen 能力按真实实现声明：

```text
input.pen
input.pen.pressure
input.pen.eraser
input.pen.hover
input.pen.low_latency
```

低延迟 Scribble/Ink 可以继续使用 Vendor SDK，但 IKP 只看到标准语义。

---

# 8. Storage / Sandbox

Android Platform 以自身 App sandbox 为基础，再提供逻辑目录：

```text
appdata/
cache/
documents/
downloads/
```

用户文件通过 SAF / Documents Provider / Vendor bridge 等方式接入，但 IKP 只看到 `baga.storage` / `baga.library`。

现代 Android SHOULD 遵守 scoped storage，不把 `MANAGE_EXTERNAL_STORAGE` 变成所有设备默认前提。

---

# 9. SQLite / `lsqlite3`

IKP 直接使用：

```lua
local sqlite3 = require("lsqlite3")
local path = baga.storage.resolve_path("appdata/app.sqlite3")
local db = sqlite3.open(path)
```

## 9.1 可预测 SQLite Runtime

Android/OEM 系统 SQLite 版本和编译选项可能随 Android 版本、厂商和系统更新变化。

Baga Universal App 需要可预测环境，因此 Reference Platform SHOULD：

```text
锁定 SQLite version
锁定 lsqlite3 version
锁定 compile profile
由 Baga Platform APK 提供该 runtime
```

## 9.2 Android OS sandbox

Android 强 OS sandbox 可以直接帮助约束数据库路径。

`baga.storage.resolve_path()` SHOULD 解析到 Platform 为当前 IKP 分配的 private app-data area。

IKP 不应获得其他 Baga App 私有 database path。

## 9.3 SQLite Profile

必须满足 Standard Libraries 规范与 BICTS，包括：

```text
transaction
prepared statement
foreign key
BLOB
JSON
FTS5
WAL（在支持的 filesystem/locking 语义下）
no arbitrary extension loading
```

---

# 10. Automerge

Automerge core 是 Baga 已采用的 Local-first / CRDT 优先基础。

Android implementation MAY：

```text
使用完整 Rust core
使用 JS/WASM binding（如果运行环境合理）
使用 Java/其他成熟 binding
通过 automerge-c
只使用 document/merge/history
只使用 binary persistence
只使用 sync protocol
只使用 patch/cursor 等局部能力
```

采用 Automerge 不要求采用完整 `automerge-repo`。

当前 developer-facing Lua binding 尚未冻结；IKP 在正式公共 binding 确定前通过受控 Platform/App integration 使用 Automerge。

---

# 11. `baga.sync`

Android 上 `baga.sync` 定义：

```text
connectivity state
when_online
wifi_only
when_charging
sleep/wake coordination
trigger / retry / cancel
```

如果应用采用 Automerge sync protocol，则 protocol payload 可以经过 Android/Baga 的 HTTP/WebSocket/其他可靠 transport 传输。

---

# 12. User Library / `baga.library`

不同厂商书库位置/数据库/文件桥可能不同。

```text
Vendor bookshelf / filesystem / SAF
        ↓
Android Adapter internal bridge
        ↓
baga.library
        ↓
IKP App
```

规则：

- 能稳定桥接用户书库时声明 `storage.user_library`；
- Library Item 使用 opaque ID；
- `library.read/write` 控制访问；
- App 不看到真实 Vendor DB/path；
- source/handle 可交给 `baga.reader`；
- 不限定 EPUB/PDF 或其他固定清单。

---

# 13. Reader

公开关系：

```text
IKP App
  ↓
baga.reader
  ↓
Baga Ink Platform on Android
```

内部 Reader 可以使用成熟 Android/native/library 实现。

Reader Anchor 仍然 format-agnostic；实现满足 create/serialize/resolve/goto 语义即可。

---

# 14. Network

Android Base SHOULD 提供：

```text
network.available
network.http
network.https
network.connectivity_events
network.wifi（实际存在时）
```

Platform 处理：

- Doze/background restrictions；
- network switching；
- timeout/TLS/DNS；
- sleep/wake；
- offline-first policy。

---

# 15. Lifecycle / Power

Android Activity / Service 生命周期归一为：

```text
start
resume
pause
sleep
wake
stop
```

App 不知道 `onCreate/onResume/...`。

Power MAY 提供：

```text
power.battery_level
power.charging_state
power.keep_awake
```

App 不直接持有 WakeLock。

---

# 16. Frontlight / Audio / Bluetooth

只有真实可控时才声明：

```text
light.frontlight
light.frontlight.temperature
audio.output
bluetooth.available
bluetooth.input_device
bluetooth.audio
```

厂商接口留在 Adapter 内部。

---

# 17. Android Version / Firmware Fragmentation

Platform / Adapter 吸收：

```text
permissions
scoped storage
Bluetooth permission changes
background execution
notification rules
API deprecation
Vendor refresh behavior
Pen API
frontlight API
system properties
storage paths
```

Compatible 认证绑定：

```text
model
+ firmware / Android range
+ Platform version
+ Adapter version
+ Lua Profile version
+ BICTS version
```

---

# 18. Baga Ink Client 安装

推荐：

```text
识别 Android device
检测 model / firmware / ABI
检查 Compatibility Database
安装 Baga Ink Platform APK
Platform self-check
BICTS smoke test
安装 *.ikp
```

普通允许 APK 安装的设备可以不依赖 Client，但设备端标准不变。

---

# 19. APK 与 IKP

```text
Baga Ink Platform = APK
Baga Ink Universal App = IKP
```

开发者如果单独发布原生 Android APK，那是 Native Android App，不自动获得 Baga Ink Universal 标签。

---

# 20. Android Compatible Gate

正式认证前 MUST：

- Base BICTS PASS；
- Baga Lua Profile PASS；
- `lsqlite3` / SQLite Profile PASS；
- Platform APK install/update reliable；
- App sandbox correct；
- Touch/Input/Lifecycle correct；
- Vendor capability truthfully declared；
- Library/Reader profiles（若声明）PASS；
- 固件范围明确；
- IKP update failure recoverable。

---

# 21. 与 LifeBook 的关系

LifeBook on Android E-Paper SHOULD 使用与 Kindle 同一 IKP 业务代码。

```text
设备能力 → baga.*
关系数据库 → lsqlite3 / SQLite
并发 Local-first 对象 → Automerge core（适用时）
```

Android Adapter 不为 LifeBook 开私有接口。

---

# 22. 核心原则

> **Android 的设备碎片化留在 Adapter 下面；成熟通用软件能力尽量直接采用；Adapter 上面只留下稳定 Baga Ink API 和 Baga Lua Profile。**
