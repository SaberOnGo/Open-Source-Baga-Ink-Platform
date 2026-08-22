# Baga Ink Device Adapter Specification

> **文档级别：一级平台规范**  
> **状态：Draft v0.1**  
> **日期：2026-08-22**  
> **上位文档：`BAGA_INK_PLATFORM_STRATEGY.md`**  
> **配套规范：`BAGA_INK_COMPATIBILITY_STANDARD.md`、`BAGA_INK_API_SPECIFICATION.md`、`BAGA_INK_APP_STANDARD.md`、`IKP_PACKAGE_SPECIFICATION.md`**

---

## 0. 目的

本文档定义 **Baga Ink Device Adapter** 的职责、边界和最小接口语义。

Device Adapter 是 Baga Ink Platform 与具体设备 / OS / Vendor SDK 之间的唯一标准适配边界。

它解决的问题是：

> **Kindle、BOOX、iReader、Bigme、汉王及其他墨水屏设备，底层实现可以完全不同，但上层 Baga Ink API 必须保持统一。**

Device Adapter 不服务于某一个 App，也不服务于 LifeBook 私有需求。

它服务于：

```text
所有符合 Baga Ink App Standard 的 IKP App
```

---

# 1. 架构位置

```text
Universal / Enhanced IKP Apps
            │
            ▼
       Baga Ink API
            │
            ▼
   Baga Ink Platform Core
            │
            ▼
   Baga Ink Device Adapter
            │
      ┌─────┴───────────┐
      │                 │
 Kindle OS /        Android /
 Homebrew Layer     Vendor SDK
      │                 │
      ▼                 ▼
  Hardware           Hardware
```

Device Adapter MUST 隐藏设备私有实现细节。

第三方 Universal App MUST 不直接依赖 Adapter 私有接口。

---

# 2. Adapter 的职责

Device Adapter 负责把设备能力映射为 Baga Ink 标准语义。

主要职责：

```text
Device identification
Capability detection
Display / refresh
Input
Storage mapping
Lifecycle
Power
Network
Frontlight
Pen
Audio
Bluetooth
System event bridge
Diagnostics
```

并不是所有设备都必须实现全部 Optional Capability。

Adapter 最重要的责任不是“尽量返回支持”，而是：

> **准确表达真实能力。**

---

# 3. Adapter 不负责什么

Device Adapter MUST 不成为第二套应用 API。

禁止方向：

```text
App → adapter.boox.fastRefresh()
App → adapter.kindle.shell()
App → adapter.ireader.privateApi()
```

正确方向：

```text
App
 ↓
baga.display.refresh({ mode = "FAST" })
 ↓
Platform Core
 ↓
Device Adapter
 ↓
设备私有实现
```

Device Adapter 也不负责：

- App 业务逻辑；
- App Market 逻辑；
- LifeBook 私有功能；
- IKP 内部依赖管理；
- 将 Vendor API 直接暴露给 Universal App。

---

# 4. Adapter Identity

每个 Adapter SHOULD 提供稳定元数据。

概念结构：

```text
adapter_id
adapter_version
device_family
platform_family
supported_firmware_range
compatibility_standard_version
```

示例：

```json
{
  "adapter_id": "org.baga.kindle.paperwhite5",
  "adapter_version": "0.1.0",
  "device_family": "kindle",
  "platform_family": "kindle_os",
  "compatibility_standard": "0.1"
}
```

实际 schema 由实现规范进一步冻结。

---

# 5. Device Descriptor

Adapter MUST 能向 Platform Core 提供 Device Descriptor。

最低信息：

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

Device Descriptor 可以包含用于诊断的信息，但第三方 Universal App 的核心业务逻辑不应依赖具体 manufacturer / model。

---

# 6. Capability Detection

Adapter MUST 实现真实 Capability 检测。

概念接口：

```text
has(capability) -> boolean
list_capabilities() -> set
```

例如：

```text
display.partial_refresh
display.fast_refresh
display.color
input.touch
input.pen
input.pen.pressure
audio.output
bluetooth
network.wifi
light.frontlight
```

Capability MUST：

- 基于当前设备和当前固件真实状态；
- 在启动时可检测；
- 在能力动态变化时可更新（若适用）；
- 不因为“同系列其他型号有此功能”而误报；
- 不把未经验证的能力标记为正式支持。

---

# 7. Display Adapter

Display Adapter 是所有墨水屏设备的核心模块。

最低职责：

```text
get_size()
get_orientation()
set_orientation()          optional
refresh(region, mode)
full_refresh()
supports_display_mode(mode)
```

Baga Ink Display Mode：

```text
AUTO
TEXT
QUALITY
FAST
ANIMATION
```

Adapter 负责将这些语义映射到具体设备行为。

## 7.1 Refresh Region

统一区域使用逻辑屏幕坐标：

```text
x
y
width
height
```

Adapter MUST：

- 处理越界裁剪；
- 正确处理当前屏幕方向；
- 避免负坐标导致底层异常；
- 对不支持局部刷新的设备合理降级到全刷新。

## 7.2 Refresh Mode Mapping

Adapter MAY：

- 将多个 Baga Ink mode 映射到同一个底层模式；
- 根据设备状态调整刷新方式；
- 在残影累积后自动插入质量刷新。

Adapter MUST 不：

- 把 Vendor waveform ID 当作公开 API；
- 假装设备支持不存在的模式。

## 7.3 Ghosting Management

Platform 可以表达刷新意图，Adapter 可以参与清残影策略。

例如：

```text
N 次 FAST partial update
      ↓
自动 QUALITY / full refresh
```

具体策略 MAY 因设备而异，但不应改变 App 业务语义。

---

# 8. Input Adapter

Input Adapter 负责把设备原始输入映射为 Baga Ink 统一事件。

支持类别 MAY 包括：

```text
touch
pen
physical_button
keyboard
```

核心语义动作：

```text
confirm
back
menu
page_next
page_previous
```

Adapter MUST：

- 将设备物理翻页键映射为 page_next / page_previous；
- 在 Android 设备需要时将允许的按键转换为统一动作；
- 避免 App 直接依赖 Linux keycode / Android keycode / Kindle 私有键码；
- 正确处理重复按键；
- 正确处理触摸坐标和屏幕方向。

---

# 9. Touch Adapter

声明 `input.touch` 后 MUST 支持：

```text
pointer_down
pointer_move
pointer_up
cancel
```

至少提供：

```text
x
y
```

可选：

```text
pressure
contact_size
pointer_id
```

Adapter MUST 保证坐标与 Baga Ink UI 使用的逻辑屏幕坐标一致。

---

# 10. Pen Adapter

如果声明 `input.pen`，Adapter MUST 至少区分 Pen 与普通 Touch。

可选能力：

```text
input.pen.pressure
input.pen.eraser
input.pen.hover
input.pen.low_latency
```

低延迟手写属于增强能力，不属于 Base Profile。

Vendor 专用手写接口 MAY 在 Adapter 内使用，但对 App 应以标准 Capability 暴露。

---

# 11. Storage Adapter

Storage Adapter 把 Baga Ink 逻辑路径映射到设备存储。

最低逻辑根：

```text
appdata/
cache/
documents/
downloads/
```

Adapter / Platform Core 共同保证：

- App 沙箱隔离；
- 路径规范化；
- 防止 `..` 路径逃逸；
- 磁盘空间错误可检测；
- 写入失败返回统一错误；
- Platform 更新不默认清除 App 数据。

设备真实路径 MUST 不成为 Baga Ink 公共契约。

---

# 12. User Library Bridge

用户书库不是普通 App 沙箱的一部分。

Adapter MAY 负责发现设备已有书库位置，但 Platform Core MUST 通过标准化权限与 Reader / Library API 暴露。

正确关系：

```text
Device filesystem / Kindle documents / Android storage
                    │
                    ▼
              Device Adapter
                    │
                    ▼
         Baga Ink Library abstraction
                    │
                    ▼
                 App
```

Universal App 不应自行扫描 Kindle `/documents` 或 Android 厂商私有路径。

---

# 13. Lifecycle Adapter

Adapter 必须将底层生命周期事件转换为：

```text
start
resume
pause
sleep
wake
stop
```

底层来源 MAY 完全不同：

```text
Kindle system events
Android lifecycle
OS power event
Process restart
```

但 App 看到的语义必须稳定。

Adapter MUST 防止：

- 一次 wake 触发多次重复事件；
- sleep 时遗漏必要通知；
- 设备旋转被误认为 App restart；
- 底层事件顺序异常导致 App 状态损坏。

---

# 14. Power Adapter

最低接口语义：

```text
battery_level()
is_charging()
request_keep_awake()
release_keep_awake()
```

硬件不支持的字段可返回：

```text
not_supported
unknown
```

不得伪造数值。

Adapter MAY 根据 OS 能力实现：

- 延迟休眠；
- 临时保持唤醒；
- 充电状态监听；
- 电量变化事件。

---

# 15. Network Adapter

设备声明网络能力后，Adapter 必须支持：

```text
connectivity_state
network_change_event
HTTP transport bridge
```

Platform Core 可以在此之上实现统一 Network API。

Adapter MUST 正确处理：

- Wi-Fi 关闭；
- 设备休眠；
- 网络重新连接；
- 请求中途断网；
- DNS / TLS / timeout 错误映射。

不得要求 App 调用设备自己的连接管理 API。

---

# 16. Frontlight Adapter

如果声明：

```text
light.frontlight
```

Adapter SHOULD 支持：

```text
get_frontlight()
set_frontlight(level)
```

如果支持暖光，可进一步声明：

```text
light.temperature
```

是否允许 App 修改前光属于 Permission / Policy 决策，不代表有 Capability 就自动允许所有 App 控制。

---

# 17. Audio Adapter

如果声明：

```text
audio.output
```

Adapter 应提供统一的音频输出能力桥接。

底层 MAY 是：

- 内置扬声器；
- USB 音频；
- 蓝牙音频；
- 厂商系统服务。

App 不应依赖具体输出介质。

音频格式、解码和 TTS 是否属于 Platform Core 或 Capability Provider，由后续 Audio Specification 定义。

---

# 18. Bluetooth Adapter

如果声明 Bluetooth 能力，Adapter 应把可允许的蓝牙操作标准化。

Bluetooth 不应成为任意 Vendor API 穿透入口。

第一阶段只定义能力边界，不在本规范锁死完整蓝牙协议 API。

---

# 19. Error Mapping

Adapter MUST 把底层错误映射为 Baga Ink 稳定错误语义。

典型错误：

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

Adapter MAY 保留 Vendor debug code 供日志使用，但 Universal App MUST 不依赖该 code。

例如：

```text
VendorError 0x1234
        ↓
Adapter
        ↓
io_error
```

诊断日志可同时保留：

```text
vendor_code = 0x1234
```

---

# 20. Event Model

Adapter 到 Platform Core 的事件 MUST 具有明确生命周期。

典型事件：

```text
input
orientation_changed
network_changed
power_changed
sleep
wake
storage_changed
pen_state_changed
```

事件 SHOULD：

- 有序；
- 可去重；
- 不在 Adapter 中直接调用 App 业务对象；
- 先进入 Platform Core，再转成公开 API 事件。

---

# 21. Threading / Main Loop

不同设备事件模型可能完全不同。

Adapter MAY 使用：

- Android main thread；
- native event loop；
- KOReader 已有 event loop；
- thread / callback；
- platform-specific polling（仅必要时）。

但 Adapter MUST 确保：

- 不让 Vendor callback 直接进入 Universal App；
- UI 更新最终回到 Platform Core 认可的 UI 执行上下文；
- 长任务不阻塞输入事件；
- shutdown 时资源可安全释放。

---

# 22. Logging 与 Diagnostics

Adapter SHOULD 提供诊断日志，包括：

```text
adapter startup
model detection
firmware detection
capability detection
display mapping failures
input mapping failures
power events
network events
unexpected vendor errors
```

日志 MUST 不把用户书籍内容、笔记正文或敏感凭据作为普通诊断信息写入。

Baga Ink Client MAY 收集用户明确允许的诊断报告。

---

# 23. Adapter 初始化

推荐初始化顺序：

```text
1. Detect device / firmware
2. Validate supported range
3. Initialize system bridge
4. Detect capabilities
5. Initialize display
6. Initialize input
7. Initialize storage mapping
8. Initialize lifecycle bridge
9. Initialize optional modules
10. Publish Device Descriptor
11. Run adapter self-check
12. Hand control to Platform Core
```

任何 Mandatory 模块初始化失败时，Adapter MUST 报告明确状态，不得假装成功。

---

# 24. Adapter Self-Check

每个 Adapter SHOULD 提供 self-check。

至少验证：

```text
Device identity
Display basic refresh
Input basic path
Storage sandbox read/write
Lifecycle event bridge
Capability consistency
```

Optional Capability 也应按声明逐项检查。

Self-check 结果可以作为 BICTS 的前置数据。

---

# 25. Kindle Adapter

Kindle Adapter 的原则是：

> **最大化复用已经存在且成熟的 Kindle Homebrew / KOReader 能力，不重复造轮子。**

可能复用：

```text
KOReader device abstraction
KOReader display / input knowledge
KUAL / PEKI launch infrastructure
MRPI installation infrastructure
现有 Kindle system integration
成熟 native libraries
```

Kindle Adapter 负责把这些能力转换为 Baga Ink 标准语义。

第三方 IKP App 不应知道底层究竟使用了：

```text
KUAL
MRPI
Shell
KOReader internal widget
Kindle framebuffer mechanism
```

这些都属于平台实现细节。

---

# 26. Android E-Paper Adapter

Android 设备上的 Baga Ink Platform MAY 以 APK 形式安装。

Android Adapter MAY 使用：

```text
Kotlin
Java
JNI
Rust
C / C++
Android SDK
Vendor E-Paper SDK
```

Adapter 负责屏蔽：

```text
BOOX refresh API
iReader refresh API
Vendor pen SDK
Vendor power API
Android version differences
```

上层仍然只看到：

```text
baga.*
```

Generic Android Adapter SHOULD 提供最低通用能力；厂商专用 Adapter MAY 在此之上提供更准确的 E-Paper Capability。

---

# 27. Generic Adapter 与 Vendor Adapter

Android 平台 MAY 存在：

```text
Generic Android Adapter
          │
          ├── BOOX specialization
          ├── iReader specialization
          ├── Bigme specialization
          └── Other vendor specialization
```

但 specialization 只改变底层映射，不得产生不同的公开 App API。

优先级原则：

```text
Verified vendor mapping
        >
Verified generic mapping
        >
Capability unavailable
```

绝不能为了“显示支持更多功能”使用未经验证的猜测。

---

# 28. Adapter 与 IKP 的关系

IKP 不携带 Device Adapter。

正确关系：

```text
Device
 └── Baga Ink Platform
      ├── Platform Core
      ├── Device Adapter
      └── Apps
           ├── LifeBook.ikp
           ├── Notes.ikp
           └── RSS.ikp
```

同一个 `LifeBook.ikp` 在 Kindle 与 Android 上运行时，变化的是设备端 Adapter，不是 App 包。

这是 Baga Ink 防碎片化的核心边界。

---

# 29. Adapter 与 Capability Provider

Device Adapter 是设备基础能力层。

Capability Provider 用于：

- 可选高级能力；
- 独立升级的复杂组件；
- 某些厂商增强功能。

例如：

```text
pen.low_latency
advanced_tts
specialized_audio
```

但 Capability Provider MUST 通过 Baga Ink 标准 Capability 和 API 暴露，不能要求 App 调用私有 native 接口。

---

# 30. Adapter Versioning

Adapter 必须单独版本化。

一个 Compatibility Record SHOULD 记录：

```text
Device Model
Firmware Range
Baga Ink Platform Version
Adapter Version
Compatibility Standard Version
```

Adapter 更新后必须重新运行受影响的 Compatibility Tests。

尤其需要回归：

```text
Display
Input
Storage
Sleep / Wake
Power
Capability detection
```

---

# 31. 安全原则

Adapter 位于高权限边界，因此必须更加谨慎。

Adapter MUST：

- 不把 arbitrary shell 暴露给 Universal App；
- 不把 Android Context 直接暴露给 App；
- 不暴露 Vendor SDK object；
- 对路径、参数、region 做边界检查；
- 对来自 App 的请求进行 Platform Policy 校验；
- 不因为 Vendor API 功能强大就默认全部开放。

原则：

> **底层权限可以很高，公开能力必须很窄。**

---

# 32. BICTS Hook

Adapter MUST 支持 Compatibility Test Suite 所需的测试入口。

至少需要让测试系统验证：

```text
Device Descriptor
Capabilities
Display basic behavior
Input mapping
Storage isolation
Lifecycle mapping
Power state
Optional profiles
```

测试入口不能给普通 App 提供额外特权。

---

# 33. OEM 实现指南

未来硬件厂商主动接入 Baga Ink 时，理想流程：

```text
Vendor hardware / firmware
          │
          ▼
Implement Baga Ink Device Adapter
          │
          ▼
Run Adapter Self-Check
          │
          ▼
Run BICTS
          │
          ▼
Fix failures
          │
          ▼
Declare verified capabilities
          │
          ▼
Baga Ink Compatible
```

OEM 不需要修改第三方 IKP App。

这是平台价值的核心：

> **厂商只适配一次平台，整个 Baga Ink 应用生态即可使用其设备能力。**

---

# 34. 顶层接口模型

概念上，一个完整 Adapter 至少包含：

```text
DeviceAdapter
│
├── Identity
├── Capabilities
├── Display
├── Input
├── Storage
├── Lifecycle
├── Power
│
├── Network       optional
├── Touch         optional
├── Pen           optional
├── Frontlight    optional
├── Audio         optional
└── Bluetooth     optional
```

Base Profile 要求的模块必须实现并通过 Compatibility Test。

Optional 模块只有在 Capability 为 true 时才必须完整实现。

---

# 35. Adapter 的最终验收标准

一个 Adapter 是否设计正确，不应以“能不能跑 LifeBook”作为唯一判断。

真正标准是：

> **它能否让任意符合 Baga Ink App Standard 的 IKP，只依赖 `baga.*` 和 Capability Model，就在这台设备上按标准语义运行。**

如果一个 Adapter 需要第三方 App 知道：

```text
这是 Kindle
这是 BOOX
这是 iReader
```

才能正常工作，那么 Device Adapter 抽象就是失败的。

成功的 Adapter 应让设备差异止步于：

```text
Device Adapter
```

而不继续向 App 层扩散。
