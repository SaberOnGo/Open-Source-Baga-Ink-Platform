# Baga Ink Android 墨水屏适配规范 / Baga Ink Android E-Paper Adapter

> **文档级别：首发设备适配规范**  
> **状态：Draft v0.1**  
> **日期：2026-08-22**  
> **上位文档：`07_设备适配器规范_Baga-Ink-Device-Adapter-Specification.md`**  
> **认证依据：`08_兼容性标准_Baga-Ink-Compatibility-Standard.md`、`10_兼容性测试套件_Baga-Ink-Compatibility-Test-Suite.md`**

---

## 0. 目的 / Purpose

本文档定义 Android 墨水屏设备如何接入 Baga Ink Platform。

这里的 Android E-Paper 包括但不限于：

```text
iReader / 掌阅
BOOX / 文石
Bigme
Hanvon / 汉王
墨案
其他基于 Android 的电子纸设备
```

核心目标：

> **Android 底层可以继续使用 Kotlin / Java / JNI / Vendor SDK，但 IKP App 只能看到统一的 Baga Ink API。**

---

# 1. 架构位置

```text
IKP Apps
   │
   ▼
Baga Ink API
   │
   ▼
Baga Ink Platform Core
   │
   ▼
Android E-Paper Adapter
   │
   ├── Generic Android bridge
   ├── Vendor refresh provider
   ├── Vendor pen provider
   ├── Vendor frontlight provider
   └── Device quirks
   │
   ▼
Android OS + Vendor SDK + Hardware
```

Baga Ink Platform 本身可以作为 Android APK 安装。

第三方 IKP 不需要再做独立 APK。

---

# 2. 设计原则

Android Adapter MUST：

1. 先实现 Generic Android Base；
2. 再通过 Vendor Provider 增强墨水屏私有能力；
3. 不要求每个 IKP App 引入厂商 SDK；
4. 不把 Android Context 直接暴露给 Universal App；
5. 不把厂商 refresh mode 名称变成公共 API；
6. Capability 必须基于真实设备检测；
7. 同一 `.ikp` 应能跨多个厂商运行。

---

# 3. Platform APK

Android 设备端 SHOULD 以一个受控 Platform APK 提供：

```text
Platform Core
Embedded Lua Interpreter
Baga Lua Profile
Baga Ink API
IKP package manager
App sandbox
Device Adapter
Market integration
```

这些共同组成一个 Baga Ink Platform 产品。

用户不需要安装第二套额外中间层。

---

# 4. Android Base Adapter

Generic Android Adapter SHOULD 尽量使用 Android 公共能力实现：

```text
app lifecycle
filesystem sandbox
network
battery / charging
orientation
basic touch
keyboard
Bluetooth（如系统允许）
audio（如系统允许）
```

E-Paper 特有刷新、低延迟 Pen、前光等能力再交给 Vendor Provider。

---

# 5. Vendor Provider 模型

推荐：

```text
Android Adapter Common
      │
      ├── Generic Android Provider
      ├── BOOX Provider
      ├── iReader Provider
      ├── Bigme Provider
      ├── Hanvon Provider
      └── Future Vendor Provider
```

Provider 是 Device Adapter 内部插件点，不是第三方 IKP 插件 API。

---

# 6. Vendor Detection

Platform MAY 根据：

```text
manufacturer
brand
model
system properties
available classes / SDK
feature probe
```

选择 Vendor Provider。

但检测必须保守。

禁止：

```text
只因为 Build.MANUFACTURER = xxx
→ 就声明所有该厂商高级能力
```

真实 capability 必须 feature probe 或机型白名单验证。

---

# 7. Display Base

所有支持设备 MUST 实现：

```text
display.basic
```

Android View / Surface 的普通 redraw 不自动等于：

```text
display.partial_refresh
display.fast_refresh
```

这些必须通过实际 E-Paper 控制能力验证。

---

# 8. Vendor Refresh Mapping

厂商可能提供不同概念：

```text
partial
regal
GC
GU
A2
speed
animation
quality
```

Baga Ink 只暴露：

```text
AUTO
TEXT
QUALITY
FAST
ANIMATION
```

Adapter 负责映射。

例如某设备底层拥有多个更新模式时，可映射为：

```text
Vendor partial/text mode → TEXT
Vendor full/quality mode → QUALITY
Vendor A2/fast mode → FAST / ANIMATION
```

但映射是设备实现细节，不写进 App。

---

# 9. BOOX / Onyx Provider 原则

BOOX 是一个典型 Vendor Provider 参考。

公开 Onyx Android SDK 已提供 EPD 更新、刷新模式、前光和 Pen / Scribble 等接口，因此 Baga Ink Provider 可以封装这些能力。

但：

```text
EpdController
UpdateMode.GC
UpdateMode.GU
REGAL
TouchHelper
```

等 Onyx 概念 MUST 留在 Provider 内部。

Universal App 仍然只调用：

```lua
baga.display.refresh(...)
baga.device.has("display.fast_refresh")
baga.device.has("input.pen.low_latency")
```

---

# 10. iReader / 其他厂商 Provider

如果厂商存在私有刷新或手写接口：

```text
Vendor API
   ↓
Vendor Provider
   ↓
Baga Ink standard capability
```

如果没有稳定公开接口，则可以：

- 只使用 Generic Android Base；
- 不声明高级 capability；
- 将实验性适配标记 Experimental；
- 等验证完成再进入 Stable Registry。

不能为了“支持列表更好看”伪报能力。

---

# 11. Touch

Android Touch 通常可由标准事件获得。

Adapter MUST：

- 归一化坐标；
- 处理 orientation；
- 把系统 pointer 映射成 Baga Ink 事件；
- 不让 App 依赖 MotionEvent；
- 正确处理 cancel / multi-touch。

只有实际可用才声明：

```text
input.touch
input.multitouch
```

---

# 12. Pen

Android E-Paper Pen 可能通过：

```text
Android stylus event
Vendor SDK
low-latency native path
```

Adapter MUST 统一映射：

```text
input.pen
input.pen.pressure
input.pen.eraser
input.pen.hover
input.pen.low_latency
```

低延迟 Pen Provider SHOULD 与普通 UI 渲染解耦，以避免厂商“直写电子纸”路径与 Android View 延迟冲突。

---

# 13. Low-latency Ink

低延迟笔迹属于增强能力。

标准思路：

```text
Pen raw input
   ↓
Vendor low-latency path
   ↓
即时电子纸 stroke
   ↓
stroke data 同步给 Platform canvas
```

Baga Ink MUST 定义统一 stroke 语义后再暴露给 App。

不得让 App 自己初始化 BOOX / iReader 专用 scribble controller。

---

# 14. Storage

Android Platform 使用自己的 App sandbox 作为基础。

Baga Ink 再定义逻辑目录：

```text
appdata/
cache/
documents/
downloads/
```

这些不等价于 Android 真实路径。

用户文件 SHOULD 通过：

```text
Storage Access Framework
Media / Documents provider
Vendor library bridge
```

等安全方式接入，但 App 只看到 Baga Ink Storage API。

---

# 15. Android Scoped Storage

Platform SHOULD 遵守现代 Android scoped storage 原则。

Baga Ink 不应为了统一文件访问而要求：

```text
MANAGE_EXTERNAL_STORAGE
```

成为所有设备默认前提。

只有在明确必要、合规且用户知情时才考虑更广权限。

---

# 16. User Library Bridge

不同厂商书库位置可能不同。

推荐：

```text
Vendor bookshelf / filesystem
        │
        ▼
Android Vendor Provider
        │
        ▼
Baga Library abstraction
        │
        ▼
IKP App
```

平台可以支持用户导入自己的 EPUB/PDF，而不要求获取厂商私有书城数据。

---

# 17. Network

Android Base Adapter SHOULD 提供：

```text
network.available
network.http
network.https
network.connectivity_events
```

若 Wi-Fi 存在：

```text
network.wifi
```

App 不直接依赖 Android ConnectivityManager。

Platform SHOULD 处理：

- doze / background restrictions；
- Wi-Fi disconnect；
- network switching；
- timeout；
- TLS error；
- offline-first policy。

---

# 18. Lifecycle

Android Activity / Service 生命周期必须归一化为：

```text
start
resume
pause
sleep
wake
stop
```

App 不知道：

```text
onCreate
onStart
onResume
onPause
onStop
```

等 Android 细节。

屏幕熄灭 / 设备休眠与 Activity pause 不是完全同义，Adapter 必须正确区分。

---

# 19. Power

Android Base Adapter SHOULD 支持：

```text
power.battery_level
power.charging_state
power.sleep_wake
```

`power.keep_awake` 必须由 Platform policy 控制。

App 不直接持有 Android WakeLock。

---

# 20. Frontlight

Android 系统亮度不一定等于电子纸前光。

只有 Vendor Provider 能可靠控制时才声明：

```text
light.frontlight
light.frontlight.temperature
```

Platform 必须恢复用户设置并避免永久修改厂商偏好。

---

# 21. Audio

如果 Android 设备具备可用音频输出：

```text
audio.output
```

可使用系统 Audio API 实现。

没有扬声器但可蓝牙输出时，能力声明应基于实际可用路径。

---

# 22. Bluetooth

Android Base Adapter MAY 使用系统 Bluetooth API 实现：

```text
bluetooth.available
bluetooth.input_device
bluetooth.audio
```

但授权必须经过 Baga Ink Permission Model，并兼容不同 Android 版本权限变化。

---

# 23. Physical / Volume Keys

某些墨水屏把音量键用于翻页。

Adapter MAY 映射：

```text
volume_up/down
    ↓
page_previous/page_next
```

但这应由设备 Profile / 用户设置决定。

IKP App 只监听语义动作。

---

# 24. Android Version Fragmentation

Baga Ink Platform 必须吸收 Android 版本差异，例如：

```text
permissions
scoped storage
Bluetooth permissions
background execution
notification rules
API deprecation
```

这些差异不能成为 IKP App 的兼容分支。

---

# 25. Vendor Firmware Fragmentation

同一厂商不同固件也可能改变：

```text
refresh SDK behavior
pen API
frontlight API
system property
storage path
```

因此 Compatible 认证必须绑定：

```text
model + firmware range + adapter version
```

不能只写“支持 BOOX”。

---

# 26. Quirk Database

Android Adapter MAY 维护：

```text
manufacturer/model/firmware → quirks
```

例如：

```text
refresh invalidation workaround
coordinate offset
pen palm rejection issue
frontlight range
volume key mapping
```

Quirk 是 Adapter 内部实现，不进入 App API。

---

# 27. Baga Ink Client 安装流程

Android E-Paper 推荐：

```text
USB / ADB / user-selected install route
  ↓
识别 Android device
  ↓
检测 model / firmware / ABI
  ↓
检查 Compatibility Database
  ↓
安装 Baga Ink Platform APK
  ↓
Platform 自检 Adapter
  ↓
运行 BICTS smoke test
  ↓
安装 LifeBook.ikp / Market Apps
```

对于允许直接安装 APK 的普通设备，Client MAY 不是必须的，但它仍可提供统一设备管理体验。

---

# 28. APK 与 IKP 的边界

这是 Android 侧最关键的规则之一：

```text
Baga Ink Platform = APK
Third-party Baga Ink App = IKP
```

第三方 Universal App 不应同时发布一个“Baga Ink 版 APK”。

如果开发者选择发布原生 Android APK，那是 Native Android App，不自动获得 Baga Ink Universal 标签。

---

# 29. Capability Provider

高级厂商能力 SHOULD 通过内部 Provider 标准化：

```text
Vendor SDK
  ↓
Capability Provider
  ↓
Baga capability
  ↓
Baga API
```

Provider 可以用：

```text
Kotlin
Java
JNI
Rust
C/C++
```

但这些实现语言不影响 IKP App 开发语言。

---

# 30. Android Compatible Gate

正式认证前 MUST：

- Base BICTS 全通过；
- Platform APK 安装/更新可靠；
- App sandbox 正确；
- Touch / Input 正确；
- sleep/wake 正确；
- Vendor capability 声明真实；
- 未使用 Vendor Provider 时不伪报高级 E-Paper 能力；
- 固件范围明确；
- IKP 更新失败可恢复。

---

# 31. 与 LifeBook 的关系

LifeBook on Android E-Paper SHOULD 使用与 Kindle 尽可能相同的 IKP 业务代码。

Android Adapter 不为 LifeBook 开私有接口。

如果 LifeBook 需要某个 BOOX / iReader 特性：

```text
先判断是否应标准化为 Capability/API
```

而不是：

```text
LifeBook → 直接调用 Vendor SDK
```

---

# 32. 非目标

Android Adapter 不负责：

- 替换 Android OS；
- 让所有 Android APK 变成 IKP；
- 强迫厂商使用同一个刷新 SDK；
- 向 Universal App 暴露 Android Context；
- 要求所有设备具备 Pen / Color / Audio；
- 让每个 App 自己适配 BOOX / iReader。

---

# 33. 核心原则 / Core Rule

> **Android 的开放和碎片化都留在 Adapter 下面；Adapter 上面只留下 Baga Ink。**

这就是 Baga Ink Platform 对 Android 墨水屏生态最核心的价值。
