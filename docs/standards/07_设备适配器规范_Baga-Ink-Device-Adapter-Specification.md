# Baga Ink 设备适配器规范 / Baga Ink Device Adapter Specification

> **文档级别：一级平台规范**  
> **状态：Draft v0.2**  
> **日期：2026-08-22**  
> **上位文档：`01_顶层战略与架构_Baga-Ink-Platform-Strategy.md`**  
> **配套规范：`03_API规范_Baga-Ink-API-Specification.md`、`04_能力注册表_Baga-Ink-Capability-Registry.md`、`08_兼容性标准_Baga-Ink-Compatibility-Standard.md`、`10_兼容性测试套件_Baga-Ink-Compatibility-Test-Suite.md`**

---

## 0. 目的

本文档定义 **Baga Ink Device Adapter** 的职责、边界和最小接口语义。

Device Adapter 是 Baga Ink Platform 与具体设备 / OS / Vendor SDK 之间的唯一标准适配边界。

它解决的问题是：

> **Kindle、BOOX、iReader、Bigme、汉王及其他墨水屏设备，底层实现可以完全不同，但上层 Baga Ink API 必须保持统一。**

Device Adapter 不服务于某一个 App，也不服务于 LifeBook 私有需求，而是服务所有符合 Baga Ink App Standard 的 IKP App。

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

Capability 名称和语义 MUST 以 `04_能力注册表_Baga-Ink-Capability-Registry.md` 为准。

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

每个 Adapter SHOULD 提供稳定元数据：

```text
adapter_id
adapter_version
device_family
platform_family
supported_firmware_range
compatibility_standard_version
```

Adapter 版本 MUST 与设备 Compatibility Record 一起记录。

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

Device Descriptor 可用于诊断，但第三方 Universal App 的核心业务逻辑不应依赖具体 manufacturer / model。

---

# 6. Capability Detection

Adapter MUST 实现真实 Capability 检测。

概念接口：

```text
has(capability) -> boolean
list_capabilities() -> set
```

Capability MUST：

- 基于当前设备和当前固件真实状态；
- 在启动时可检测；
- 在能力动态变化时可更新（若适用）；
- 不因为同系列其他型号有此功能而误报；
- 不把未经验证的能力标记为正式支持。

---

# 7. Display Adapter

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

Refresh Region 使用逻辑屏幕坐标：

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
- 对不支持局部刷新的设备合理降级到全刷新；
- 不把 Vendor waveform ID 当作公开 API；
- 不假装设备支持不存在的模式。

Platform / Adapter MAY 根据残影累积自动插入质量刷新。

---

# 8. Input Adapter

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

至少提供 x / y，并保证坐标与 Baga Ink UI 逻辑坐标一致。

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

Vendor 专用手写接口 MAY 在 Adapter 内使用，但对 App 必须以标准 Capability 暴露。

---

# 11. Storage Adapter

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

底层来源 MAY 完全不同，但 App 看到的语义必须稳定。

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

硬件不支持的字段可返回 `not_supported` / `unknown`，不得伪造数值。

---

# 15. Network Adapter

设备声明网络能力后，Adapter 必须支持：

```text
connectivity_state
network_change_event
HTTP transport bridge
```

Adapter MUST 正确处理 Wi-Fi 关闭、休眠、重连、请求中断以及 DNS / TLS / timeout 错误映射。

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
light.frontlight.temperature
```

是否允许 App 修改前光属于 Permission / Policy 决策。

---

# 17. Audio Adapter

如果声明 `audio.output`，Adapter 应提供统一音频输出能力桥接。

底层 MAY 是：

- 内置扬声器；
- USB 音频；
- 蓝牙音频；
- 厂商系统服务。

App 不应依赖具体输出介质。

---

# 18. Bluetooth Adapter

如果声明 Bluetooth 能力，Adapter 应把可允许的蓝牙操作标准化。

Bluetooth 不应成为任意 Vendor API 穿透入口。

---

# 19. Error Mapping

Adapter MUST 把底层错误映射为 Baga Ink 稳定错误语义，例如：

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

Vendor debug code MAY 保留在日志中，但 Universal App MUST 不依赖它。

---

# 20. Event Model

Adapter 到 Platform Core 的事件 SHOULD：

- 有序；
- 可去重；
- 不在 Adapter 中直接调用 App 业务对象；
- 先进入 Platform Core，再转成公开 API 事件。

---

# 21. Threading / Main Loop

Adapter MAY 使用 Android main thread、native event loop、KOReader 已有 event loop 或其他平台机制。

但 MUST：

- 不让 Vendor callback 直接进入 Universal App；
- UI 更新最终回到 Platform Core 认可的 UI 执行上下文；
- 长任务不阻塞输入事件；
- shutdown 时资源可安全释放。

---

# 22. Logging 与 Diagnostics

Adapter SHOULD 记录：

```text
adapter startup
model / firmware detection
capability detection
display mapping failures
input mapping failures
power / network events
unexpected vendor errors
```

普通日志 MUST 不包含用户书籍正文、笔记正文或敏感凭据。

---

# 23. 初始化与 Self-Check

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

Self-check 至少验证：

```text
Device identity
Display basic refresh
Input basic path
Storage sandbox read/write
Lifecycle event bridge
Capability consistency
```

---

# 24. Kindle Adapter

Kindle Adapter 原则：

> **最大化复用已经存在且成熟的 Kindle Homebrew / KOReader 能力，不重复造轮子。**

具体要求见 `11_Kindle适配规范_Baga-Ink-Kindle-Adapter.md`。

---

# 25. Android E-Paper Adapter

Android Adapter MAY 使用 Kotlin、Java、JNI、Rust、C/C++、Android SDK 和 Vendor E-Paper SDK，但必须屏蔽这些差异。

具体要求见 `12_Android墨水屏适配规范_Baga-Ink-Android-E-Paper-Adapter.md`。

---

# 26. Generic Adapter 与 Vendor Adapter

Android MAY 采用：

```text
Generic Android Adapter
          │
          ├── BOOX specialization
          ├── iReader specialization
          ├── Bigme specialization
          └── Other vendor specialization
```

Specialization 只改变底层映射，不得产生不同的公开 App API。

---

# 27. Adapter 与 IKP 的关系

IKP 不携带 Device Adapter。

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

---

# 28. Capability Provider

Capability Provider 用于可选高级能力，但 MUST 通过 Baga Ink 标准 Capability 和 API 暴露，不能要求 App 调用私有 native 接口。

---

# 29. Adapter Versioning

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

---

# 30. 安全原则

Adapter 位于高权限边界，因此：

- 不把 arbitrary shell 暴露给 Universal App；
- 不把 Android Context 直接暴露给 App；
- 不暴露 Vendor SDK object；
- 对路径、参数、region 做边界检查；
- 对来自 App 的请求进行 Platform Policy 校验。

原则：

> **底层权限可以很高，公开能力必须很窄。**

---

# 31. BICTS Hook

Adapter MUST 支持 `10_兼容性测试套件_Baga-Ink-Compatibility-Test-Suite.md` 所需测试入口。

测试入口不能给普通 App 提供额外特权。

---

# 32. OEM 实现流程

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

---

# 33. 顶层接口模型

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

---

# 34. 最终验收标准

> **一个正确的 Adapter，应让任意符合 Baga Ink App Standard 的 IKP，只依赖 `baga.*` 和 Capability Model，就在这台设备上按标准语义运行。**

如果 App 必须知道“这是 Kindle / BOOX / iReader”才能正常工作，那么 Adapter 抽象就是失败的。
