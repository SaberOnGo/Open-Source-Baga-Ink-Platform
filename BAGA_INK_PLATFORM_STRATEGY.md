# Baga Ink Platform 顶层战略与架构定义

> **文档级别：Strategic Source of Truth / 项目最高层级定义**  
> **状态：Strategic Baseline v0.2**  
> **日期：2026-08-22**  
> **适用项目：Open-Source-Baga-Ink-Platform**

---

## 0. 文档地位

本文档定义 **Baga Ink** 项目的长期战略边界、平台定位、品牌与产品层级、应用模型、开发者模型、设备兼容模型，以及防止生态碎片化的核心约束。

它不是某一款 Kindle、某一家 Android 墨水屏厂商的适配说明，也不是某一个 SDK 版本的 API Reference。它是整个 Baga Ink 项目的**顶层定义文档**。

后续的 README、SDK 文档、IKP Package Specification、Kindle Adapter、Android Adapter、Market 审核规则、Compatibility Test Suite、LifeBook 实现，以及其他子项目的设计，都应当与本文档保持一致。

若后续实现与本文档的战略原则发生冲突，应通过正式架构决策更新本文档，而不是在子模块中静默偏离。

### 0.1 规范性用词

- **MUST / 必须**：平台级硬约束；
- **SHOULD / 应当**：默认应遵守，除非有明确且记录在案的原因；
- **MAY / 可以**：允许的实现选择。

### 0.2 术语原则

Baga Ink 必须坚持轻量平台定位。

设备端统一使用以下术语：

- **Baga Ink Platform**：整个设备端统一平台；
- **Baga Ink Platform Core**：设备端共享核心代码与平台能力；
- **Baga Ink API**：第三方应用唯一稳定公开接口；
- **Baga Lua Profile**：第三方 Lua 应用可使用的语言子集与标准库范围；
- **Embedded Lua Interpreter**：Platform Core 内部嵌入或复用的轻量 Lua 解释器；
- **Baga Ink Device Adapter**：连接 Platform Core 与具体设备/系统能力的适配层。

项目文档不得把 Baga Ink 描述成一个需要额外安装、独立管理、独立升级的通用执行环境或庞大中间层。

对用户而言，设备上只有 **Baga Ink Platform**；对开发者而言，只有 **Baga Ink SDK / API / App Standard**；对平台实现者而言，才需要理解 Platform Core 与 Device Adapter。

---

# 1. 战略愿景

## 1.1 一句话定义

> **Baga Ink Platform 是面向 Kindle 与 Android 墨水屏设备的统一、轻量、跨设备应用平台。**

Baga Ink 要解决的不是“再做一个墨水屏 App”，而是：

> **让今天彼此分散的 Kindle 与 Android 墨水屏设备，在第三方开发者眼中逐渐成为同一个应用平台。**

今天的现实是：

```text
Kindle Homebrew / KUAL / MRPI / KOReader / Shell / Native Binary

Android E-Paper
├─ iReader / 掌阅
├─ BOOX / 文石
├─ Hanvon / 汉王
├─ Bigme
├─ 墨案
└─ 其他 Android 墨水屏

每个设备：
不同系统版本
不同刷新接口
不同输入方式
不同电源策略
不同手写接口
不同安装方式
不同厂商 SDK
```

Baga Ink 的目标状态：

```text
                   Third-party Apps
                          │
                          ▼
                Baga Ink App Standard
                          │
                          ▼
            Baga Ink SDK / Baga Ink API
                          │
                          ▼
                Baga Ink Platform Core
                          │
             ┌────────────┴────────────┐
             │                         │
      Kindle Device Adapter     Android Device Adapter
             │                         │
      Kindle OS / Homebrew       Android / Vendor SDK
```

核心思想：

> **应用不适配设备；设备通过 Baga Ink Device Adapter 适配平台。**

---

# 2. 战略目标

Baga Ink 的长期目标不是“兼容尽可能多的设备”这么简单，而是形成事实标准：

1. 开发者学习一次 Baga Ink SDK，就可以为多个墨水屏设备开发；
2. 一个符合标准的 IKP 应用包可以跨 Kindle 与 Android E-Paper 设备运行；
3. 新设备通过实现 Baga Ink Device Adapter 和 Compatibility Standard 接入生态；
4. 第三方应用不需要理解 Kindle 私有机制或 Android 厂商私有刷新接口；
5. 设备厂商最终有动力主动声明并实现 **Baga Ink Compatible**；
6. Baga Ink Market 用兼容规则强化统一标准，而不是成为另一个软件下载站。

最终判断标准：

> **如果开发者仍然必须维护 Kindle、BOOX、iReader、Bigme 等多个应用分支，那么 Baga Ink 尚未真正成为平台。**

---

# 3. Baga Ink 生态品牌架构

```text
                         Baga Ink
                      整个生态品牌
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
 Baga Ink Platform   Baga Ink Client   Baga Ink Market
      设备端平台         PC / Mac            应用市场
          │
          ▼
        Apps
          │
    ┌─────┼───────────────┐
    │     │               │
 LifeBook RSS / Reader   Notes / AI / ...
```

## 3.1 正式命名

| 对象 | 正式名称 |
|---|---|
| 整个生态品牌 | **Baga Ink** |
| 统一设备端平台 | **Baga Ink Platform** |
| 应用市场 | **Baga Ink Market** |
| Windows / macOS 客户端 | **Baga Ink Client** |
| 开发工具包 | **Baga Ink SDK** |
| 平台 API | **Baga Ink API** |
| 应用标准 | **Baga Ink App Standard** |
| 兼容性标准 | **Baga Ink Compatibility Standard** |
| 设备适配层 | **Baga Ink Device Adapter** |
| 开发者门户 | **Baga Ink Developers** |
| 旗舰应用 | **LifeBook** |
| Kindle 版本描述 | **LifeBook for Kindle** |

## 3.2 Baga Ink Platform 的边界

Baga Ink Platform 包括：

- Platform Core；
- Embedded Lua Interpreter；
- Baga Lua Profile；
- App Lifecycle；
- Baga Ink API；
- UI / Display / Input / Storage / Network / Power / Reader 等平台能力；
- Capability Model；
- Permission / Sandbox；
- IKP Package Loader；
- Device Adapter；
- Compatibility 机制。

这些都是同一个轻量设备端平台的组成部分，不应被拆成需要用户额外安装和理解的独立产品层。

**Baga Ink Platform 不等于 PC 客户端，也不等于应用市场。**

## 3.3 Baga Ink Client

Windows / macOS 上的设备安装与管理客户端，负责：

- 自动识别 Kindle 或 Android 墨水屏；
- 识别型号、固件、系统与兼容状态；
- 安装、升级、修复或卸载 Baga Ink Platform；
- 执行设备所需的安全安装流程；
- 管理应用、备份、恢复与未来设备迁移；
- 作为用户进入 Baga Ink 生态的桌面入口。

## 3.4 Baga Ink Market

Baga Ink 官方应用与扩展分发市场，可承载：

- Universal Apps；
- Device Enhanced Apps；
- 字体；
- 词典；
- 主题；
- Reader Extension；
- Device Adapter；
- Capability Provider；
- AI / 云服务入口。

## 3.5 LifeBook

LifeBook 是 Baga Ink 上的**旗舰 App**，不是 Platform 本身。

设备中显示：

> **LifeBook**

只有在需要区分版本时使用：

> **LifeBook for Kindle**

LifeBook 不承担平台 SDK、API 或第三方生态的命名空间责任。

---

# 4. 为什么必须先定义标准

如果第三方开发者可以自由直接使用：

- Kindle Shell；
- Kindle private framework；
- Android Context；
- BOOX 私有 SDK；
- iReader 私有接口；
- Vendor Refresh API；
- 自定义安装方式和包格式；

那么 Baga Ink 最终只会成为统一下载入口，而不是统一平台。

因此：

> **统一标准 MUST 先于应用数量扩张。**

Baga Ink Market SHOULD 强化统一标准，而不是奖励设备私有分叉。

---

# 5. 平台核心原则

## 5.1 一次开发，多设备运行

```text
一份应用源代码
+
一个 IKP 应用包
=
Kindle + 多种 Android E-Paper 设备运行
```

第三方开发者 SHOULD 不需要为 BOOX、iReader、Kindle 等设备维护独立业务代码分支。

## 5.2 Capability，而不是 Vendor

标准方式：

```lua
if baga.device.has("input.pen") then
    enable_pen_ui()
end
```

不推荐：

```lua
if device.vendor == "BOOX" then
    enable_pen_ui()
end
```

典型 Capability：

```text
display.partial_refresh
display.fast_refresh
display.gray16
display.color
input.touch
input.pen
input.physical_page_key
audio.output
bluetooth
network.wifi
light.frontlight
storage.external
```

## 5.3 API 是稳定边界

第三方 Universal App 面向：

```text
Baga Ink API
```

而不是：

```text
KOReader internals
Kindle system internals
Android Context
Vendor SDK
Shell
Linux device nodes
Raw framebuffer
```

平台内部实现可以变化，公开 API 应尽可能长期稳定并版本化。

---

# 6. 官方应用开发语言

## 6.1 Universal App：Lua

第一官方跨设备应用语言采用 **Lua**。

第三方应用面向的是受平台约束的：

> **Baga Lua Profile**

它定义：

- 允许的 Lua 语言特性；
- 标准库范围；
- 禁止或受限的系统访问；
- Baga Ink API；
- 生命周期；
- 权限模型；
- 版本兼容规则。

Lua 只是应用开发语言；它不构成一个额外产品层。

在 Kindle 上，Platform MAY 直接复用 KOReader 等现有项目已经验证过的 Lua 解释器能力；在 Android 上，Baga Ink Platform APK MAY 直接嵌入轻量 Lua 解释器。

无论采用哪种实现，开发者只面对 Baga Lua Profile 和 `baga.*` API。

## 6.2 为什么不是 Kotlin / Java 作为统一应用语言

Android 墨水屏可以天然运行 Kotlin / Java，但 Kindle 并不是 Android。

如果把 Kotlin / Java 作为统一应用语言，就会迫使 Kindle 增加一整套不必要的 JVM / Android 框架级中间层，明显违背轻量原则。

Lua 的战略优势：

- 解释器体积小；
- 易嵌入 Rust / C / C++；
- 同一份应用代码更容易跨 CPU / OS 分发；
- 适合事件驱动 UI 与业务逻辑；
- KOReader 已经证明 Lua 前端可以长期运行于多类墨水屏设备。

## 6.3 Rust 的位置

Rust **不是第一阶段 Universal App 的官方语言**。

Rust 更适合：

- Platform Core；
- 高性能解析；
- 网络与同步；
- 文件处理；
- 安全敏感模块；
- Device Adapter；
- Native Capability Provider。

推荐分层：

```text
第三方 Universal App
        Lua
         │
         ▼
    Baga Ink API
         │
         ▼
 Baga Ink Platform Core
  Rust / C / C++
         │
   ┌─────┴────────────┐
   │                  │
Kindle Adapter    Android Adapter
Rust/C/Shell      Kotlin/Java/JNI/Rust/C
```

语言统一发生在第三方应用边界，而不是要求平台内部所有代码只用一种语言。

---

# 7. Baga Ink SDK 与 API

第一阶段顶层命名空间：

```lua
baga.app
baga.ui
baga.display
baga.input
baga.device
baga.storage
baga.network
baga.power
baga.reader
baga.sync
```

示例：

```lua
local page = baga.ui.page({ title = "Hello Ink" })

baga.display.mode("TEXT")

if baga.device.has("input.pen") then
    enable_pen_ui()
end
```

正式名称：

> **Baga Ink API**

代码命名空间：

> **`baga.*`**

第三方 Application ID 不强制使用 `baga.*`，例如：

```text
com.example.reader
org.example.notes
```

---

# 8. 第一阶段平台能力边界

## 8.1 App Lifecycle

```text
install
start
resume
pause
sleep
wake
stop
update
uninstall
```

## 8.2 UI

基础组件方向：

```text
Page
Text
Image
List
Button
Menu
Dialog
Toolbar
ReaderView
```

设计原则：

- 高对比度；
- 减少动画；
- 减少无意义刷新；
- 大触控区域；
- 支持无触摸设备；
- 支持物理翻页键；
- UI 状态与实际刷新策略解耦。

## 8.3 Display

```text
refresh
partial_refresh
full_refresh
set_mode
invalidate_region
```

语义模式：

```text
AUTO
TEXT
QUALITY
FAST
ANIMATION
```

App 表达刷新意图，Adapter 根据设备映射实际刷新方式。

## 8.4 Input

```text
touch
pen
keyboard
page_next
page_previous
physical_button
```

## 8.5 Storage

应用默认运行于沙箱：

```text
appdata/
cache/
documents/
downloads/
```

## 8.6 Network

统一连接状态、HTTP 与同步策略。

## 8.7 Power

```text
battery
sleep
wake
keep_awake
sync_when_charging
```

## 8.8 Reader

逐步提供：

```text
open book
current position
goto
selection
highlight
note
search
metadata
```

底层可以复用 KOReader、MuPDF 等成熟组件，但第三方 App 不依赖其内部 API。

---

# 9. IKP 应用包

Baga Ink Universal App 标准扩展名：

# **`.ikp`**

例如：

```text
lifebook.ikp
rss-reader.ikp
notes.ikp
```

IKP 包应主要包含：

```text
example.ikp
├── manifest.json
├── main.lua
├── src/
├── assets/
├── locales/
└── signature/
```

Universal IKP 的重要原则：

> **IKP 是应用代码与资源包，不是设备适配包，不携带自己的设备抽象层，也不携带针对某一设备的私有执行组件。**

Universal IKP 不应包含：

- Android APK / DEX 作为应用主逻辑；
- Kindle 专用 Shell executable；
- BOOX / iReader 专用 native library 作为应用依赖；
- 自己私带一套 Lua 解释器；
- 绕过 Baga Ink API 的系统调用桥。

所有 Universal App 共享设备上 Baga Ink Platform 已提供的 Baga Lua Profile 与 API。

---

# 10. Universal / Enhanced / Native Extension

## 10.1 Universal App

要求：

- Lua / Baga Lua Profile；
- `.ikp`；
- Baga Ink API；
- Capability Model；
- 标准生命周期；
- 标准权限；
- 不直接访问设备私有 API。

## 10.2 Device Enhanced App

允许使用 Platform 暴露的标准 Capability Extension，例如：

```text
pen.low_latency
display.vendor_fast_mode
audio.tts
```

增强能力必须通过平台公开接口获得。

## 10.3 Native Extension / Capability Provider

Kotlin / Java / Rust / C / C++ 等原生代码主要用于扩展 Platform 能力。

原生扩展的目标是：

> **让平台新增一个标准化 Capability，而不是让每个 App 自己绕过平台。**

---

# 11. 防碎片化硬规则

Universal App 默认禁止或严格限制：

```text
os.execute
io.popen
raw shell
Android Context
Java reflection
direct JNI
Kindle private framework
direct /proc
direct /sys
raw framebuffer
vendor SDK
```

设备差异必须沿以下方向消化：

```text
App
 │
Baga Ink API
 │
Platform Core
 │
Device Adapter
 │
Vendor / OS
```

API 和 Capability 必须版本化。

未来建立：

> **Baga Ink Compatibility Test Suite**

以及设备认证：

> **Baga Ink Compatible**

---

# 12. Kindle 平台战略

Kindle 当前 Homebrew 生态是 Baga Ink 的重要基础，但不是未来第三方开发者应该直接面对的开发模型。

可复用基础包括：

```text
KUAL / PEKI
MRPI
WinterBreak / SpringBreak / Sanctuary / Véra
Mesquito（部分机型 / 固件）
KOReader
Shell / Native binaries
Kindle system services
```

Baga Ink 的策略：

> **收编和封装现有 Kindle Homebrew 能力，而不是从零重写。**

```text
Kindle Homebrew 基础设施
          │
          ▼
Baga Ink Kindle Adapter
          │
          ▼
 Baga Ink Platform Core
          │
          ▼
       .ikp Apps
```

早期 KUAL、MRPI 等可以继续承担安装、启动或兼容桥梁角色。

普通用户不需要理解这些基础设施。

---

# 13. KOReader 的位置

KOReader 是重要技术基础和 Reference Implementation 来源，但：

> **Baga Ink API ≠ KOReader API**

Baga Ink 可以复用：

- Lua UI；
- ReaderUI；
- Input abstraction；
- Display / Device abstraction；
- EPUB / PDF 能力；
- 字体与排版；
- Kindle 兼容经验；
- 现有 Lua 解释器集成方式。

第三方 App 不直接绑定 KOReader internals。

```text
Third-party App
      │
      ▼
Baga Ink API
      │
      ▼
Platform Core
      │
      ├── KOReader-derived components
      ├── Rust / C components
      └── Device Adapter
```

---

# 14. Android E-Paper 平台战略

Baga Ink Platform 在 Android 墨水屏上可以作为一个普通 APK 安装：

```text
Android E-Paper Device
        │
        ▼
Baga Ink Platform.apk
        │
        ├── Platform Core
        ├── Embedded Lua Interpreter
        ├── Baga Ink API
        └── Device Adapter
        │
        ▼
      .ikp Apps
```

Platform APK 内部可以使用 Kotlin、Java、JNI、Rust、C/C++ 与厂商 E-Paper SDK。

第三方 Universal App 不需要知道这些实现细节。

战略收益：

> **Platform 适配一次设备或厂商，所有 Universal Apps 同时获益。**

---

# 15. Baga Ink Client

首要支持：

```text
Windows
macOS
```

核心流程：

```text
连接设备
   │
   ▼
自动识别
   │
   ├── Kindle
   ├── Android E-Paper
   └── Future Device
   │
   ▼
兼容性检查
   │
   ▼
安装 / 修复 / 升级 Baga Ink Platform
   │
   ▼
安装 LifeBook 或 Baga Ink Market 应用
```

客户端必须坚持：

- 不清除用户书籍；
- 不清除用户笔记；
- 不要求恢复出厂作为标准流程；
- 失败尽可能可恢复；
- 未知或不安全组合明确显示“不支持 / 实验性支持”。

---

# 16. Baga Ink Market

Market 的核心职责：

1. 应用发现与分发；
2. 数字签名与开发者身份；
3. API 版本检查；
4. Capability 要求检查；
5. Compatibility Test；
6. 权限展示；
7. 更新、回滚和撤回；
8. Universal / Enhanced 兼容标签；
9. 应用审核与生态治理。

Market SHOULD 优先鼓励 Universal App，并明确标记设备私有依赖。

---

# 17. 开发者体验目标

```text
安装 Baga Ink SDK
        │
        ▼
baga new my-app
        │
        ▼
使用 Lua + baga.* API
        │
        ▼
模拟器 / 真机调试
        │
        ▼
baga test
        │
        ▼
生成 my-app.ikp
        │
        ▼
Compatibility Test
        │
        ▼
发布到 Baga Ink Market
```

开发者 SHOULD 尽可能不需要知道：

- Kindle 固件私有细节；
- BOOX 私有刷新类；
- iReader 系统接口；
- 某款 CPU ABI；
- Kindle framebuffer；
- Android 厂商 API 差异。

---

# 18. Device Adapter 模型

```text
Baga Ink Platform Core
        │
        ├── Kindle Adapter
        ├── Generic Android Adapter
        ├── BOOX Adapter
        ├── iReader Adapter
        ├── Bigme Adapter
        └── Future Adapters
```

Adapter 负责：

- Display；
- Refresh；
- Input；
- Filesystem；
- Power；
- Sleep / Wake；
- Frontlight；
- Pen；
- Audio；
- Bluetooth；
- Network；
- Device Capability Detection。

长期目标：

> **由设备厂商主动实现 Baga Ink Device Adapter，并通过 Compatibility Test。**

---

# 19. Platform 与操作系统的边界

Baga Ink **不是新的墨水屏操作系统**。

它不替换：

```text
Kindle OS
Android
Vendor firmware
Linux kernel
```

它位于已有系统之上：

```text
Apps
 │
Baga Ink Platform Core
 │
Device Adapter
 │
Existing OS / Firmware
 │
Hardware
```

战略理由：

- 覆盖大量存量 Kindle；
- 利用现有 Android E-Paper 设备；
- 不承担完整 OS 的巨大维护成本；
- 降低厂商合作门槛；
- 保持 Platform 足够轻量。

---

# 20. Platform Core 的轻量原则

Platform Core 不是一个单独产品，也不要求用户额外安装第二套中间系统。

第一阶段核心组成：

```text
Embedded Lua Interpreter
+
Baga Ink API
+
UI / App Lifecycle
+
Security / Permissions
+
IKP Package Manager
+
Device Adapter
```

其中 Kindle 可以尽量复用现有 KOReader / Homebrew 组件；Android 可以把这些能力直接集成进 Baga Ink Platform APK。

高性能或系统层组件可以使用 Rust / C / C++。

目标是：

> **尽量少造轮子、尽量复用成熟组件，只增加真正用于统一设备与开发者接口的薄平台代码。**

LifeBook 同样遵循这一原则，不引入额外的通用执行层。

---

# 21. 开放生态与平台控制

平台允许：

- 第三方开发 App；
- 第三方贡献 Device Adapter；
- 第三方开发 Capability Provider；
- 第三方参与 SDK / Platform Core；
- 厂商实现官方设备适配。

根本原则：

> **底层允许多样，上层保持统一。**

```text
应用层：高度统一
API 层：高度稳定
Capability 层：标准化扩展
Adapter 层：允许设备差异
OS 层：可以完全不同
硬件层：可以完全不同
```

---

# 22. 长期护城河

真正形成生态壁垒的是：

```text
统一标准
+
设备兼容层
+
开发者 SDK
+
IKP 应用包格式
+
兼容测试
+
应用市场
+
存量设备覆盖
+
第三方开发者
+
硬件厂商支持
```

网络效应：

```text
更多兼容设备
      ↓
更多用户
      ↓
开发 Baga Ink App 更有价值
      ↓
更多开发者与应用
      ↓
设备支持 Baga Ink 更有价值
      ↓
更多厂商主动兼容
```

最终目标不是“Baga Ink 团队能适配多少墨水屏”，而是：

> **新的墨水屏设备是否愿意主动声明并实现 Baga Ink Compatible。**

---

# 23. 非目标（Non-Goals）

现阶段 Baga Ink 不以以下事情为目标：

1. 自研完整 E-Paper OS；
2. 替换 Android；
3. 替换 Kindle OS；
4. 强迫所有底层模块使用 Lua；
5. 强迫 Platform Core 只使用一种语言；
6. 将 Kindle Homebrew 全部从零重写；
7. 允许 Universal App 任意穿透设备底层；
8. 为每个厂商长期维护第三方 App 分叉；
9. 把 LifeBook 私有 API 当作平台标准；
10. 创建庞大、重复、需要额外维护的中间系统。

---

# 24. 第一阶段实施路线

## Phase 0 — Specification First

定义：

- Baga Ink App Standard；
- Baga Ink API；
- Baga Lua Profile；
- IKP Package Specification；
- Capability Model；
- App Lifecycle；
- Display / Refresh Model；
- Permission Model；
- Device Adapter Interface。

## Phase 1 — 两条 Reference Platform

至少建立：

```text
Kindle Reference Adapter
+
Android E-Paper Reference Adapter
```

证明：

> **同一个 `.ikp` App 可以运行在两个完全不同的系统上。**

## Phase 2 — LifeBook Reference App

```text
LifeBook for Kindle
LifeBook on Android E-Paper
```

尽可能共用 Baga Ink App 层代码。

## Phase 3 — SDK 与第三方开发者

发布：

```text
Baga Ink SDK
CLI
Simulator
Examples
Developer Documentation
```

关键验证问题：

> 一个不熟悉 Kindle 和各 Android 墨水屏私有接口的开发者，是否能只学习 Baga Ink 就完成一个跨设备应用？

## Phase 4 — Market 与 Compatibility

建立：

- Baga Ink Market；
- 数字签名；
- Compatibility Test Suite；
- Universal App 标签；
- Baga Ink Compatible 设备认证。

## Phase 5 — OEM Adoption

鼓励硬件厂商：

- 官方实现 Adapter；
- 预装 Baga Ink Platform；
- 使用 Compatibility Test；
- 宣布设备支持 Baga Ink Apps。

---

# 25. 顶层技术决策摘要

| 事项 | 顶层决定 |
|---|---|
| 生态品牌 | **Baga Ink** |
| 设备端平台 | **Baga Ink Platform** |
| PC / Mac 客户端 | **Baga Ink Client** |
| 应用市场 | **Baga Ink Market** |
| SDK | **Baga Ink SDK** |
| API | **Baga Ink API** |
| API namespace | **`baga.*`** |
| 官方 Universal App 语言 | **Lua / Baga Lua Profile** |
| Lua 实现 | **Platform Core 内部嵌入或复用轻量 Lua 解释器** |
| Platform Core 新代码方向 | **Rust 优先，允许 C/C++ 等成熟组件** |
| Android Adapter | **Kotlin / Java / JNI / Rust / C/C++ 按需使用** |
| Kindle Adapter | **Rust / C/C++ / Shell 等按实际设备需要** |
| Universal App 包格式 | **IKP / `.ikp`** |
| 应用标准 | **Baga Ink App Standard** |
| 兼容性标准 | **Baga Ink Compatibility Standard** |
| 设备适配层 | **Baga Ink Device Adapter** |
| 设备抽象 | **Capability Model** |
| 防碎片化核心 | **Universal App 不直接依赖 Vendor / OS 私有 API** |
| LifeBook 定位 | **Baga Ink 旗舰 App，而非 Platform 本身** |
| Kindle 产品描述 | **LifeBook for Kindle** |
| 是否自研新 OS | **否** |
| 是否引入额外庞大中间层 | **否** |

---

# 26. 战略成功标准

真正的验收标准是：

> **第三方开发者能否只学习一次 Baga Ink SDK，生成一个 `.ikp`，在 Kindle 与多个 Android 墨水屏设备上运行，而不需要理解每台设备的私有实现。**

如果答案是“是”，Baga Ink 是平台。

如果开发者仍然需要：

```text
Kindle 一套代码
BOOX 一套代码
iReader 一套代码
Bigme 一套代码
```

那么即使拥有应用市场、客户端和大量兼容脚本，Baga Ink 仍然只是聚合层，而不是统一平台。

---

# 27. 长期方向

Baga Ink 的最终战略不是成为“另一个 Kindle 工具”，也不是成为“另一个 Android 墨水屏 Launcher”。

它要逐步建立的是：

> **一个位于现有操作系统之上的轻量 E-Paper Application Platform。**

Baga Ink 不要求所有硬件相同，不要求所有操作系统相同，也不要求底层实现语言相同。

它只要求最重要的一件事：

> **第三方应用面对同一个稳定平台。**

这条边界，是 Baga Ink 长期必须守住的核心。
