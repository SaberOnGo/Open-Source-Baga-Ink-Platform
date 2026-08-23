# Baga Ink 设备适配器契约 / Baga Ink Device Adapter Contract

> **文档级别：一级平台规范 / Platform Standard**  
> **状态：Draft v0.6**  
> **日期：2026-08-23**  
> **上位文档：`01_顶层战略与架构_Baga-Ink-Platform-Strategy.md`**  
> **配套规范：`03_API规范_Baga-Ink-API-Specification.md`、`04_能力注册表_Baga-Ink-Capability-Registry.md`、`08_兼容性标准_Baga-Ink-Compatibility-Standard.md`、`10_兼容性测试套件_Baga-Ink-Compatibility-Test-Suite.md`、`13_标准库与成熟组件采用规范_Baga-Ink-Standard-Libraries-and-Adopted-Components.md`**

---

## 0. 目的

本文档定义 **Baga Ink Device Adapter Contract**：一个设备、OS、固件或厂商平台要接入 Baga Ink Platform 时，设备移植者必须实现的标准设备契约。

核心定义：

> **Baga Device Adapter Contract 定义“设备接入 Baga Ink 必须提供什么”，不规定“这些能力必须怎样重新实现”。**
>
> **Adapter 实现 SHOULD 优先复用设备 OS、Vendor SDK、驱动、Homebrew 与成熟开源项目已有能力，只补 Baga 所需的映射、归一化、Capability 探测、Quirk 修正和测试。**

因此，Device Adapter 的标准可以完整而严格，而某一个具体设备的 Adapter 实现可以非常薄。

本文档面向：

```text
Baga Ink Platform implementer
OEM / device vendor
第三方设备移植者
Device Adapter maintainer
BICTS / compatibility maintainer
```

IKP App 开发者 **不直接调用 Device Adapter**。App 只面对 `baga.*`、Baga Lua Profile 与正式 Standard Libraries。

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
  Baga Device Adapter Contract
            │
      ┌─────┴──────────────┐
      ▼                    ▼
 Kindle OS /           Android / Vendor SDK /
 Homebrew              Other E-Paper OS
```

公开设备能力链保持：

```text
App
 ↓
baga.*
 ↓
Platform Core
 ↓
Device Adapter Contract
 ↓
设备 / OS / 固件 / Vendor 能力
```

成熟通用库不因为被采用而进入 Device Adapter：

```text
SQLite / lsqlite3
Automerge
通用 JSON / crypto / compression
```

Reader/UI 等 Platform shared implementation 也不等于 Device Adapter；它们在需要设备能力时通过 Adapter 获取 Display/Input/Storage/Lifecycle 等机制。

---

# 2. 最重要的设计原则

## 2.1 Contract 重，具体 Adapter 轻

正确方向：

```text
完整、稳定、可测试的 Device Adapter Contract
                    ↓
            很薄的设备实现
                    ↓
        复用现成 OS / SDK / 开源能力
```

错误方向：

```text
为了“实现 Adapter”
→ 重写 framebuffer
→ 重写 input stack
→ 重写 reader
→ 重写 network stack
→ 重写 power manager
```

如果设备已有成熟实现，Adapter SHOULD 包装/调用它，而不是复制其内部能力。

## 2.2 Interfaces, not device conditionals

型号、固件、Vendor 差异 MUST 尽量集中在 Adapter / Device Profile / Quirk Set 内。

禁止让以下判断散落到 Universal App 或 Platform shared code：

```text
if Kindle PW5 ...
if BOOX ...
if iReader ...
if firmware >= ...
```

Platform-neutral 上层代码依赖稳定接口；设备差异由下层实现吸收。

## 2.3 Mechanism, not product policy

Adapter 提供设备机制：

```text
屏幕怎样刷新
输入事件怎样取得
设备怎样休眠/唤醒
存储根在哪里
当前网络是否可用
前光是否可控
```

Adapter 不决定：

```text
LifeBook 产品逻辑
同步业务策略
Market 业务
UI 页面结构
Reader 产品策略
```

## 2.4 不要求独立进程或 IPC

v0.6 Contract 是**语义与实现接口**，不是 IPC 协议。

Reference Platform SHOULD 优先使用：

```text
Platform Core
   ↓ direct typed call
Device Adapter
```

不得为了模仿其他平台架构而强制加入 Binder、JSON bridge、RPC daemon 或独立 Adapter process。

未来如某 OS 需要进程隔离，可在保持 Contract 语义的前提下由该平台内部实现。

---

# 3. Base Contract 与 Optional Subsystems

Baga Device Adapter 使用：

> **Root Adapter + Typed Subsystem Interfaces**

而不是一个不断膨胀的万能 `DeviceAdapter` 类。

逻辑结构：

```text
BagaDeviceAdapter
│
├── Identity / Descriptor                MUST
├── Capability Snapshot                  MUST
├── DisplayAdapter                       MUST
├── InputAdapter                         MUST
├── StorageAdapter                       MUST
├── LifecycleAdapter                     MUST
├── PowerAdapter                         MUST
│
├── NetworkAdapter                       OPTIONAL
├── LightAdapter                         OPTIONAL
├── AudioAdapter                         OPTIONAL
├── BluetoothAdapter                     OPTIONAL
└── UserLibraryBridge                    OPTIONAL
```

Pen / Touch / Keyboard 属于 `InputAdapter` 的可选能力，不必形成单独顶层 Adapter。

Reader 不属于 Device Adapter 顶层 subsystem。

Baga Base Compatibility 对应当前 Capability Registry：

```text
display.basic
input.navigation
storage.app_sandbox
power.sleep_wake
platform.lifecycle
```

Optional subsystem 不存在时必须明确返回 `not_supported` / absent，不得伪造。

---

# 4. Adapter Factory 与加载模型

## 4.1 v0.6 默认：随 Platform 构建/打包

第一阶段 Adapter SHOULD：

```text
Adapter source
   ↓
Baga Adapter SDK / generated interfaces
   ↓
compile/link/package with Platform
```

例如：

```text
Kindle Adapter
→ baga-platform.kpkg / native Platform envelope

Android Adapter
→ Baga Ink Platform APK
```

v0.6 **不定义第三方下载后 `dlopen()` 的动态 Native Adapter Plugin ABI**。

未来若要允许独立签名 Native Adapter Module，必须单独定义：ABI、签名、依赖、崩溃隔离和供应链策略。

## 4.2 Root Factory

Platform 可以包含一个或多个 Adapter Factory。逻辑接口：

```text
AdapterFactory
├── probe(BootstrapDeviceInfo) -> ProbeResult
└── create(AdapterCreateContext, ProbeResult) -> BagaDeviceAdapter
```

`probe()` MUST：

- 只使用 Platform bootstrap 阶段安全可得的信息；
- 不修改用户数据；
- 不假设同系列其他型号等价；
- 对未知设备/固件明确返回 unknown / unsupported；
- 提供选择 Device Profile / Quirk 的必要证据。

如果一个 Platform build 只服务单一设备家族，也可以只有一个 Factory。

---

# 5. Root Adapter 生命周期

语言无关逻辑接口：

```text
BagaDeviceAdapter
├── contract_version() -> AdapterContractVersion
├── adapter_version() -> Version
├── descriptor() -> DeviceDescriptor
├── capabilities() -> CapabilitySnapshot
├── init(AdapterHost) -> Result
├── self_test(SelfTestMode) -> SelfTestReport
├── subsystem(name) -> typed subsystem / absent
└── shutdown() -> Result
```

初始化顺序：

```text
Platform bootstrap
      ↓
AdapterFactory.probe
      ↓
AdapterFactory.create
      ↓
Adapter.init
      ↓
Adapter.descriptor + capability snapshot
      ↓
Adapter self-test
      ↓
Platform Core ready
      ↓
IKP Apps may start
```

在 Base Mandatory subsystem 尚未就绪时，Platform MUST NOT 把设备标记为 `Baga Ink Compatible`。

---

# 6. DeviceDescriptor

Adapter MUST 返回稳定、结构化的设备描述。

最小逻辑字段：

```text
adapter_contract_version
adapter_id
adapter_version

device_family
manufacturer
model
model_id
firmware_or_os_version

cpu_arch
native_target / abi_profile     when applicable

screen
input_summary

profile_id                      if profile model is used
quirk_set_id                    if quirk set is active
compatibility_record_id         when available
```

`screen` 至少包括：

```text
pixel_width
pixel_height
orientation
```

Adapter Descriptor 用于 Platform、Client、诊断和 Compatibility，不是 Universal App 的型号分支入口。

默认 MUST NOT 包含：

```text
设备序列号
Amazon / Google / OEM 用户账号
用户书籍正文
用户笔记正文
用户凭据
```

如诊断确需设备唯一标识，必须另走隐私受控机制。

---

# 7. Capability Snapshot 与 Runtime State 分离

必须区分：

```text
Capability Snapshot
→ 这个设备/Platform 组合“能不能做”

Runtime State
→ 当前“是什么状态”
```

例如：

```text
Capability: network.wifi = supported
Runtime State: offline
```

```text
Capability: power.battery_level = supported
Runtime State: battery = 72%
```

Capability 名称必须来自 `04 Capability Registry`。

Adapter MUST 不因为内部存在某个库就自动声明能力。

Capability Snapshot SHOULD 在一次 Platform Session 中保持稳定；如果固件/外设热插拔导致能力真正变化，Platform 必须通过明确 capability-change 事件重新生成快照，而不是静默改变行为。

---

# 8. AdapterHost 与事件模型

Platform Core 在 `init()` 时提供受控 `AdapterHost`。

逻辑职责：

```text
AdapterHost
├── emit(AdapterEvent)
├── monotonic_time()
├── platform_log(...)
└── controlled scheduling / wake hook as implemented
```

核心规则：

> **Adapter / Vendor callback MUST NOT 直接调用 IKP App。所有设备事件先进入 Platform Core。**

Adapter 可以从设备/OS 任意线程收到 callback，但：

- 必须把事件转换为 typed `AdapterEvent`；
- 必须提交给 Platform Core；
- Platform Core 负责应用侧的排序、去重和生命周期派发；
- v0.6 不要求 Adapter 自己实现第二套 App event loop。

典型事件：

```text
LifecycleEvent
NavigationEvent
PointerEvent
KeyboardEvent
PenEvent
PowerStateEvent
NetworkStateEvent
DisplayStateEvent
LightStateEvent
BluetoothStateEvent
CapabilityChangedEvent     rare / explicit
```

---

# 9. 通用错误模型

Adapter 的内部错误必须被归一化为稳定机器语义，再由 Platform Core 映射为 `baga.*` 错误。

v0.6 推荐基础错误码：

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

规则：

- 不把 Vendor 原始整数错误码作为 Universal App contract；
- Adapter MAY 在 diagnostics 中保留 raw backend code；
- raw code 不能成为 App 业务分支依据；
- 错误必须明确可恢复性。

---

# 10. DisplayAdapter Contract

DisplayAdapter 负责**设备显示与刷新机制**，不等于完整 UI framework，也不强制拥有一套独立 rendering engine。

逻辑接口：

```text
DisplayAdapter
├── info() -> DisplayInfo
├── supports(intent) -> boolean
└── refresh(RefreshRequest) -> Result
```

`DisplayInfo` 至少：

```text
pixel_width
pixel_height
logical_width
logical_height
orientation
grayscale_levels       if known
color                   boolean / profile
```

`RefreshRequest`：

```text
regions[]
intent
```

标准 intent：

```text
AUTO
TEXT
QUALITY
FAST
ANIMATION
```

`regions` 使用当前 Baga display logical coordinate space；越界必须拒绝或安全裁剪，不能写出 framebuffer 边界。

设备内部可以使用：

```text
Kindle waveform
FBInk
KOReader display backend
BOOX refresh mode
Vendor SDK
Linux framebuffer/DRM
```

这些不得泄漏为标准接口。

如果某设备只能全刷，Adapter 可以把 region refresh 安全降级为 full refresh，但 Capability 必须如实声明。

---

# 11. InputAdapter Contract

InputAdapter 负责把设备原始输入归一化为 Baga 输入语义。

Base Mandatory 至少能产生：

```text
confirm
back
menu               if device/platform provides semantic equivalent
page_next
page_previous
focus_next
focus_previous
```

没有独立 `menu` 键的设备可以通过 Platform/UI 提供等价交互，不要求伪造物理键。

标准事件族：

```text
NavigationAction
PointerEvent
KeyboardEvent
PenEvent
```

Pointer：

```text
down
move
up
cancel
```

Pen 的 pressure / eraser / hover / low-latency 只在真实支持并声明对应 Capability 时提供。

Adapter MUST 不把 Kindle keycode、Android KeyEvent、Vendor MotionEvent object 等直接暴露给 IKP。

---

# 12. StorageAdapter Contract

StorageAdapter 提供 Platform 在该设备上建立安全逻辑存储的设备机制。

Platform 对 App 暴露的逻辑路径仍是：

```text
appdata/
cache/
documents/
downloads/
```

Adapter MUST 至少提供：

```text
storage_info()
platform_private_root()
app_private_root(app_id)
canonicalize / containment mechanism
free_space()                 if reliably available
atomic-replace capability metadata
fsync/durability profile     if applicable
```

这里的 `root` 是 Platform 内部 NativePathHandle / equivalent，不是给 IKP 直接读取的稳定真实路径。

Platform / Adapter 共同保证：

- path normalization；
- `..` escape 拒绝；
- unauthorized absolute path 拒绝；
- symlink/canonical escape 防护；
- disk-full error；
- Platform update 不默认删除 App data；
- staged package 与 App data 分离。

对于 Kindle 等弱 OS sandbox 平台，SQLite 仍必须满足 `13` 与 BICTS 定义的 VFS / 等价 I/O confinement；仅返回一个合法目录不足以构成完整 sandbox。

---

# 13. LifecycleAdapter Contract

LifecycleAdapter 把 OS/设备事件映射为 Platform 可依赖的生命周期事实。

必须支持：

```text
sleep
wake
```

并为 Platform 构造：

```text
start
resume
pause
sleep
wake
stop
```

提供底层信号。

规则：

- SHOULD 使用事件/回调，不应高频轮询；
- wake 后设备状态可能变化，Platform 可重新检查 network/power；
- Adapter 不直接调用 App lifecycle handler；
- Platform Core 负责 App lifecycle 顺序。

---

# 14. PowerAdapter Contract

Base Mandatory：

```text
power.sleep_wake
```

可选接口：

```text
battery_level()
charging_state()
request_keep_awake(reason)
release_keep_awake(token)
```

只有真实可实现时才声明：

```text
power.battery_level
power.charging_state
power.keep_awake
```

Platform 可以拒绝 keep-awake；App 不能假设请求一定成功。

---

# 15. NetworkAdapter Contract（Optional）

NetworkAdapter 负责**设备/OS 网络状态与必要平台桥接**，不要求每个 Adapter 自己重写完整 HTTP/TLS stack。

最小逻辑接口：

```text
connectivity_state()
network_info()
```

并通过 AdapterEvent 上报：

```text
online
offline
network_changed
```

具体 Platform 可以：

```text
共享成熟 HTTP/TLS library
或
调用 OS network stack
```

只要最终 `baga.network` 语义与 BICTS 成立即可。

不得因为 NetworkAdapter 存在就把 Automerge sync protocol、HTTP client policy 或 LifeBook 同步策略塞入 Adapter。

---

# 16. Light / Audio / Bluetooth Optional Contracts

## LightAdapter

可选：

```text
get_level()
set_level(level)
get_temperature()
set_temperature(value)
```

仅在真实可控时声明 `light.frontlight*`。

## AudioAdapter

只提供 Platform 需要的设备音频输出/输入机制；TTS engine 本身可以属于 Platform shared implementation。

## BluetoothAdapter

只提供设备 Bluetooth 可用性与标准化事件/能力，不把 Vendor private object 暴露给 App。

---

# 17. UserLibraryBridge（Optional）

User Library 是强设备相关能力，因此允许 Device Adapter 提供桥接，但 `baga.library` 的产品/语义 API 属于 Platform。

逻辑 Bridge 能力：

```text
enumerate library items
open opaque source handle
import/remove when supported and permitted
rescan/refresh
```

规则：

- Item ID / source handle 对 App opaque；
- 不把 Kindle `/documents` 或 Android Vendor DB path 作为 Universal contract；
- 权限由 Platform Permission Model 控制；
- Reader 可以接收 opaque source handle；
- Library Bridge 不等于 Reader engine。

---

# 18. Reader 与 UI 不属于 Device Adapter

必须保持以下边界：

```text
baga.ui
  ↓
Platform UI implementation/backend
  ↓
Device Adapter: Display + Input
```

```text
baga.reader
  ↓
Platform Reader implementation
  ↓
Device Adapter: Display + Input + Storage + Lifecycle
```

因此：

- KOReader ReaderUI / CREngine / MuPDF 可以是 Kindle Platform Reader implementation；
- KOReader UIManager/widgets 可以是 Kindle Platform UI implementation；
- 它们可以大量复用 Adapter 下层的 Kindle device knowledge；
- 但 `ReaderAdapter` / `UIAdapter` 不应因为实现方便而被机械塞进 Device Adapter 根契约。

Reader Capability 继续由 `04` 与 `03` 定义。

---

# 19. Native Build Target、Device Profile、Quirk Set 必须分开

这是设备适配的三个不同维度。

## 19.1 Native Build Target / ABI Profile

回答：

> **Native binary 怎么编译/链接？**

例如 Kindle：

```text
kindle-legacy
kindle
kindlepw2
kindlehf
```

它不是设备型号本身。

## 19.2 Device Profile

回答：

> **某 model + firmware 组合的已知设备事实、backend 选择与能力预期是什么？**

Profile SHOULD 是数据驱动记录，例如：

```text
profile_id
match: model / firmware range
native_target
screen expectations
input expectations
baseline capability expectations
preferred backend choices
known validation status
```

Profile 不是 Compatibility 认证结果；最终仍以实测 Capability + BICTS 为准。

## 19.3 Quirk Set

回答：

> **这个精确组合有哪些偏离标准行为、需要在 Adapter 内修正的问题？**

Quirk 记录 SHOULD 包含：

```text
quirk_id
match condition
reason
workaround
scope
introduced/verified firmware range
test reference
```

Quirk 可以处理：

```text
touch correction
refresh workaround
frontlight behavior
sleep event issue
network issue
library bridge difference
```

Quirk MUST 不成为公开 Capability，也不得泄漏到 IKP 业务代码。

---

# 20. Installation Route 与 Adapter 分离

设备“怎样获得 Baga Platform”不等于“Platform 运行后怎样访问设备”。

因此：

```text
Jailbreak / bootstrap / KPM / MRPI / APK install
→ Installation / Platform bootstrap

Device Adapter
→ Platform 已运行后，怎样统一设备/OS/固件差异
```

Kindle 的 WinterBreak / SpringBreak / Sanctuary / Véra、KPM、MRPI、KUAL、PEKI、KindleTool 等不得因为与设备相关就自动进入 Device Adapter Contract。

具体边界由 `11 Kindle Adapter` 与 Kindle implementation freeze 定义。

---

# 21. Self-test

Adapter MUST 提供非破坏性 self-test。

推荐模式：

```text
QUICK
INTERACTIVE
```

`QUICK` 至少检查：

```text
Descriptor consistency
Base subsystem presence
Capability/subsystem consistency
Display info valid
Storage root accessible and contained
Lifecycle hook registered
Power sleep/wake integration initialized
Backend versions readable where applicable
```

`INTERACTIVE` MAY 检查：

```text
visible refresh
navigation keys
touch
pen
frontlight
```

Self-test 不替代 BICTS；它用于安装后诊断与快速判断 Adapter 是否明显损坏。

---

# 22. Adapter Contract Versioning

必须区分：

```text
Adapter Contract Version
→ 本标准接口版本

Adapter Version
→ 某具体 Adapter 实现版本

Device/Firmware Version
→ 设备本身版本
```

Reference 版本模型：

```text
adapter_contract = MAJOR.MINOR
```

规则：

- MAJOR：允许破坏性 Contract 变化；
- MINOR：只允许向后兼容的新增；
- 已冻结 MINOR 中已有字段/方法语义不得静默改变；
- 新 optional method/type field 必须有明确默认/absent 语义；
- Platform MUST 拒绝不支持的 Contract MAJOR；
- Platform SHOULD 能运行其声明支持范围内的较旧 MINOR Adapter。

未来机器可读 IDL / Codegen MUST 保存 frozen contract snapshots，并自动执行兼容性检查。

---

# 23. Adapter Contract Tests 与 BICTS 分工

必须区分两类测试。

## 23.1 Adapter Contract Tests

直接验证 Adapter 本身：

```text
Factory / probe
Descriptor
Capability consistency
Display contract
Input event normalization
Storage containment
Lifecycle event mapping
Power contract
Optional subsystem behavior
Error normalization
Profile / Quirk selection
Self-test
```

它回答：

> **这个 Adapter 是否正确实现了 Device Adapter Contract？**

## 23.2 BICTS

BICTS 验证：

```text
Device + Firmware/OS + Platform + Adapter + Lua Profile
```

整个组合的公开 Baga 行为是否真正成立。

它回答：

> **这台设备能否宣称 Baga Ink Compatible？**

Adapter Contract Tests PASS 不等于 BICTS PASS；反之，正式认证也应有 Adapter Contract evidence。

---

# 24. Mock / Reference Adapter 要求

Baga SHOULD 维护一个：

> **Mock / Headless Device Adapter**

用途：

- Device Adapter Contract 的最小 Reference Implementation；
- Platform Core host-side tests；
- IKP 开发无需真实设备；
- OEM Adapter 开发者可对照实现；
- 自动化 Adapter Contract Tests。

推荐能力：

```text
Display → memory bitmap / PNG snapshot
Input → scripted events
Storage → temp sandbox
Lifecycle → simulated sleep/wake
Power → simulated battery/charging
Network → simulated online/offline
Device Profile → configurable fixture
```

Mock Adapter 不用于宣称真实硬件 Compatible。

---

# 25. 语言与 SDK

Device Adapter Contract 是语言无关的。

Platform 内部 MAY 使用：

```text
Rust
C / C++
Kotlin / Java
JNI
Lua
Shell integration where device-specific and controlled
```

长期 SHOULD 建立机器可读 Adapter Contract / IDL，并生成：

```text
Rust traits/types
C headers/vtables
Kotlin interfaces/data classes
Mock stubs
Contract test fixtures
Documentation tables
```

机器 IDL 是减少 Kindle/Android/OEM 实现漂移的工具，不改变本文档的语义权威。

具体设计见 `docs/design/02_设备适配器可执行契约与SDK设计_Baga-Ink-Device-Adapter-Executable-Contract-and-SDK-Design.md`。

---

# 26. 安全边界

Device Adapter 位于高权限设备边界。

MUST：

- 不向 IKP 暴露 arbitrary shell；
- 不暴露 Android Context / Kindle private framework object / Vendor SDK object；
- 校验 refresh region / path / index / range；
- 不允许 App 通过 Adapter 越过 Permission/Sandbox；
- 不把 raw device callback 直接交给 App；
- 不在普通日志中记录用户正文/笔记/凭据；
- malformed input 不得导致越界硬件访问；
- Adapter crash/failure 应由 Platform 转换成可诊断故障，而不是破坏 App data。

---

# 27. OEM / 第三方设备接入流程

标准流程：

```text
阅读 01 / 03 / 04 / 07
        ↓
选择/实现 Adapter SDK backend
        ↓
实现 Base Mandatory subsystems
        ↓
复用 OS / Vendor SDK / mature libraries
        ↓
实现 Device Profile / Quirk（如需要）
        ↓
Adapter self-test
        ↓
Adapter Contract Tests
        ↓
实现并声明 Optional Capabilities
        ↓
BICTS
        ↓
生成 Compatibility Record
        ↓
Baga Ink Compatible / Experimental / Unsupported
```

第三方 Adapter 不需要修改 Universal IKP。

---

# 28. 设计参考（非规范依赖）

本 Contract 的部分设计原则参考成熟平台抽象体系，但不复制其进程模型或具体 ABI：

- Android HAL / Stable AIDL：标准厂商接口、接口冻结与版本兼容；
- Zephyr Device Driver Model：generic subsystem API、device-specific implementation、config/data/api 分离思想；
- Chromium Ozone：`interfaces, not ifdefs`、platform layer 提供 mechanism 而非上层 policy；
- Qt QPA：platform backend / minimal platform implementation 的工程经验。

这些项目不是 Baga Runtime dependency，也不要求 Baga 采用它们的 IPC、window system 或 driver ABI。

---

# 29. 最终原则

> **Baga Device Adapter 是设备接入 Baga Ink Platform 的稳定 Porting Contract。标准定义必须足够完整，让 OEM/第三方知道“要实现什么”；具体设备实现则应尽量薄，优先站在现有 OS、Vendor SDK、Homebrew 和成熟开源能力之上。**

进一步说：

> **标准化设备语义，不重新实现设备；集中设备差异，不把型号/固件条件扩散到 Platform 与 IKP。**
