# Baga Ink Platform 顶层战略与架构定义

> **文档级别：Strategic Source of Truth / 项目最高层级定义**  
> **状态：Strategic Baseline v0.1**  
> **日期：2026-08-22**  
> **适用项目：Open-Source-Baga-Ink-Platform**

---

## 0. 文档地位

本文档定义 **Baga Ink** 项目的长期战略边界、平台定位、品牌与产品层级、应用模型、开发者模型、设备兼容模型，以及防止生态碎片化的核心约束。

它不是某一款 Kindle、某一家 Android 墨水屏厂商的适配说明，也不是某一个 SDK 版本的 API Reference。它是整个 Baga Ink 项目的**顶层定义文档**。

后续的 README、SDK 文档、IKP Package Specification、Kindle Adapter、Android Adapter、Market 审核规则、Compatibility Test Suite、LifeBook 实现，以及其他子项目的设计，应当与本文档保持一致。

若后续实现与本文档的战略原则发生冲突，应通过正式架构决策更新本文档，而不是在子模块中静默偏离。

### 0.1 规范性用词

本文档中的：

- **MUST / 必须**：平台级硬约束；
- **SHOULD / 应当**：默认应遵守，除非有明确且记录在案的原因；
- **MAY / 可以**：允许的实现选择。

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

Baga Ink 的目标状态是：

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
                 Baga Ink Platform
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

# 2. Baga Ink 的战略目标

Baga Ink 的长期目标不是“兼容尽可能多的设备”这么简单，而是形成一种事实标准：

1. 开发者学习一次 Baga Ink SDK，就可以为多个墨水屏设备开发；
2. 一个符合标准的应用包可以跨 Kindle 与 Android E-Paper 设备运行；
3. 新设备通过实现 Baga Ink Device Adapter 和 Compatibility Standard 接入生态；
4. 第三方应用不需要理解 Kindle 私有机制或 Android 厂商私有刷新接口；
5. 设备厂商最终有动力主动声明并实现 **Baga Ink Compatible**；
6. Baga Ink Market 用兼容规则强化统一标准，而不是成为另一个软件下载站。

最终判断标准：

> **如果开发者仍然必须维护 Kindle、BOOX、iReader、Bigme 等多个应用分支，那么 Baga Ink 尚未真正成为平台。**

---

# 3. 品牌与产品顶层命名

## 3.1 整个生态品牌

整个生态统一使用：

# **Baga Ink**

`Baga Ink` 是品牌级概念，用来承载平台、客户端、应用市场、SDK、API、开发者生态和兼容认证。

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

## 3.2 正式名称

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

## 3.3 名称边界

### Baga Ink Platform

指设备端统一应用平台及其技术规范，包括：

- Runtime / Core；
- App Lifecycle；
- Baga Ink API；
- UI / Display / Input / Storage 等平台能力；
- Capability Model；
- Permission / Sandbox；
- IKP Package Loader；
- Device Adapter；
- Compatibility 机制。

**Baga Ink Platform 不等于 PC 客户端，也不等于应用市场。**

### Baga Ink Client

Windows / macOS 上的设备安装与管理客户端，负责：

- 自动识别连接的 Kindle 或 Android 墨水屏；
- 识别型号、固件、系统与兼容状态；
- 安装、升级、修复或卸载 Baga Ink Platform；
- 执行各设备所需的安全安装流程；
- 管理应用、备份、恢复与未来的设备迁移；
- 作为用户进入 Baga Ink 生态的桌面入口。

### Baga Ink Market

Baga Ink 生态的官方应用与扩展分发市场。

它不仅可以分发应用，未来还可以承载：

- Universal Apps；
- Device Enhanced Apps；
- 字体；
- 词典；
- 主题；
- Reader Extension；
- Device Adapter；
- Capability Provider；
- AI / 云服务入口。

### LifeBook

LifeBook 是 Baga Ink 上的**旗舰 App**，但不是 Platform 本身。

设备 UI 中应用名称保持：

> **LifeBook**

只有在需要区分平台版本或官网介绍时使用：

> **LifeBook for Kindle**

LifeBook 的现有产品品牌不应继续承担平台、SDK、API 或第三方生态的命名责任。

---

# 4. 为什么必须先定义标准，再扩大应用市场

Baga Ink 的核心价值不是“同一个 Market 里有很多 App”。

如果第三方开发者可以自由直接使用：

- Kindle Shell；
- Kindle private framework；
- Android Context；
- BOOX 私有 SDK；
- iReader 私有接口；
- 各种 Vendor Refresh API；
- 自定义安装器和包格式；

那么生态最终仍会碎片化，只是多了一个统一下载入口。

因此：

> **统一标准 MUST 先于应用数量扩张。**

Baga Ink Market SHOULD 强化标准，而不是绕开标准。

---

# 5. 平台核心原则

## 5.1 一次开发，多设备运行

符合 Baga Ink App Standard 的 Universal App 应当满足：

```text
一份应用源代码
+
一个 IKP 应用包
=
Kindle + 多种 Android E-Paper 设备运行
```

第三方开发者 SHOULD 不需要为 BOOX、iReader、Kindle 等设备维护独立业务代码分支。

## 5.2 Capability，而不是 Vendor

应用 MUST 优先查询设备能力，而不是判断品牌或型号。

错误方向：

```lua
if vendor == "BOOX" then
    ...
end

if device == "Kindle" then
    ...
end
```

标准方向：

```lua
if baga.device.has("pen") then
    -- 启用手写能力
end

if baga.device.has("audio.output") then
    -- 启用音频能力
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

新增设备只要正确实现 Adapter 与 Capability 声明，上层应用原则上无需知道设备品牌。

## 5.3 Platform API 是稳定边界

第三方 Universal App 面向：

```text
Baga Ink API
```

而不是面向：

```text
KOReader internals
Kindle system internals
Android Context
Vendor SDK
Shell
Linux device nodes
Raw framebuffer
```

平台内部实现 MAY 改变，但公开 API SHOULD 尽可能保持长期稳定并版本化。

---

# 6. 官方应用开发语言

## 6.1 Universal App：Lua

Baga Ink 的第一官方跨设备应用语言采用 **Lua**。

但 Baga Ink App 面向的不是“任意 Lua 环境”，而是一个受平台约束的：

> **Baga Lua Profile**

Baga Lua Profile 由 Baga Ink SDK 定义，包括：

- 允许的 Lua 语言特性；
- 标准库范围；
- 禁止或受限的系统访问；
- Baga Ink API；
- 生命周期；
- 权限模型；
- 版本兼容规则。

具体 Lua / LuaJIT 基线属于 SDK 实现决策，不在本顶层战略文档中锁死。

## 6.2 为什么不是 Kotlin / Java 作为统一语言

Android 墨水屏可以天然运行 Kotlin / Java，但 Kindle 并不是 Android。

如果把 Kotlin / Java 作为统一应用语言，就需要让 Kindle 承担 JVM / Android Runtime 级别的复杂度，违背 Baga Ink 的轻量目标。

Lua 的战略优势：

- Runtime 很小；
- 易嵌入 Rust / C / C++；
- 跨 CPU / OS 分发简单；
- 适合事件驱动 UI 与业务逻辑；
- KOReader 已经证明 Lua 前端可以长期运行在 Kindle、Android、Kobo、PocketBook 等多类墨水屏设备上。

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

因此，Baga Ink 的“语言统一”发生在**第三方应用边界**，而不是要求平台内部所有代码只能使用一种语言。

---

# 7. Baga Ink SDK 与 API

Baga Ink SDK MUST 保持薄、稳定、可理解。

第一阶段 API 顶层命名空间建议：

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
local page = baga.ui.page({
    title = "Hello Ink"
})

baga.display.set_mode("text")

if baga.device.has("pen") then
    -- Enable pen UI
end
```

正式产品名称：

> **Baga Ink API**

代码命名空间：

> **`baga.*`**

二者不冲突。

第三方应用自己的 Application ID MUST 不强制使用 `baga.*` 前缀，应用身份应属于对应开发者，例如：

```text
com.example.reader
com.example.notes
```

---

# 8. 第一阶段平台能力边界

以下模块属于第一阶段 SDK / API 的顶层能力划分，具体函数签名由 API Reference 单独定义。

## 8.1 App Lifecycle

```text
install
launch
pause
resume
sleep
wake
update
uninstall
```

应用不得自行依赖 Kindle 或 Android 私有生命周期实现。

## 8.2 UI

Baga Ink UI 必须针对墨水屏，而不是简单复制手机 UI。

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

抽象能力包括：

```text
refresh
partial_refresh
full_refresh
set_mode
invalidate_region
```

典型显示意图：

```text
AUTO
TEXT
QUALITY
FAST
ANIMATION
```

App 提出显示意图，Device Adapter 根据硬件能力选择真正刷新方式。

## 8.4 Input

统一抽象：

```text
touch
pen
keyboard
page_next
page_previous
physical_button
```

## 8.5 Storage

应用默认运行于沙箱中，不得任意扫描系统目录。

逻辑目录可包括：

```text
appdata/
cache/
documents/
books/
downloads/
```

## 8.6 Network

统一 HTTP / connectivity / sync policy 等接口。

平台应允许墨水屏特有策略，例如：

```text
Wi-Fi only
sync when connected
sync when charging
```

## 8.7 Power

墨水屏设备必须把电源作为一等平台能力：

```text
battery
sleep
wake
keep_awake
sync_when_charging
```

## 8.8 Reader

Baga Ink SHOULD 将成熟阅读能力逐渐抽象为平台能力：

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

底层 MAY 复用 KOReader、MuPDF、EPUB 解析器等成熟组件，但第三方 App 不应依赖这些组件的内部 API。

---

# 9. IKP 应用包格式

Baga Ink Universal App 的标准分发包扩展名定义为：

# **`.ikp`**

例如：

```text
lifebook.ikp
rss-reader.ikp
wikipedia.ikp
notes.ikp
```

## 9.1 IKP 的定位

`IKP` 是 Baga Ink 应用包格式的固定格式标识符。

`.ikp` **不要求被机械解释为某个逐字母英文缩写**。它首先是一个稳定、短、独立的平台包扩展名。

选择 `.ikp` 的战略原因：

- 不再绑定 LifeBook，因此不使用 `.lbk` / `.lbapp`；
- 比 `.baga` 更像平台应用包而不是普通品牌数据文件；
- 比 `.inkapp` 更短；
- 避免使用在嵌入式 Linux / OpenWrt 等生态中已有成熟含义的 `.ipk`；
- 可以形成独立的 Baga Ink 应用包身份。

## 9.2 第一阶段逻辑结构

具体压缩、索引、签名、校验与二进制格式由单独的 **Baga Ink IKP Package Specification** 定义。

逻辑结构预计至少包括：

```text
example.ikp
├── manifest.json
├── main.lua
├── src/
├── assets/
├── locales/
└── signature/
```

示例 Manifest：

```json
{
  "id": "com.example.reader",
  "name": "Example Reader",
  "version": "1.0.0",
  "baga_api": "1",
  "entry": "main.lua",
  "permissions": [
    "network",
    "library.read"
  ],
  "capabilities": [
    "display.partial_refresh"
  ]
}
```

字段和语义 MUST 在 Package Specification 中版本化。

---

# 10. Universal App、Enhanced App 与 Native Extension

Baga Ink 不能通过“禁止一切原生能力”来实现统一，也不能允许每个应用自行穿透平台。

因此采用分层生态。

## 10.1 Universal App

这是 Baga Ink 最核心、最高优先级的应用类型。

要求：

- 使用 Baga Lua Profile；
- 以 `.ikp` 分发；
- 使用 Baga Ink API；
- 使用 Capability Model；
- 使用标准 Lifecycle；
- 使用标准 Permission；
- 不直接访问 Vendor / OS 私有 API。

Market 建议标识：

> **Baga Ink Universal**

## 10.2 Device Enhanced App

允许应用使用平台暴露的硬件增强能力，例如：

```text
pen.low_latency
display.vendor_fast_mode
audio.tts
```

但增强能力仍然 SHOULD 通过 Baga Ink Capability Extension 暴露，而不是让普通 App 直接调用厂商 SDK。

Market 必须清晰标识兼容范围，例如：

```text
Universal
Enhanced on BOOX
Requires Pen
Kindle Unsupported
```

## 10.3 Native Extension / Capability Provider

Kotlin / Java / Rust / C / C++ 等原生代码主要存在于此层。

它们的职责是给 Platform 增加标准化能力，而不是让每个应用重新绕开 Platform。

---

# 11. 防碎片化硬规则

以下属于战略级硬约束。

## 11.1 Universal App 默认不得直接调用系统

默认禁止或严格限制：

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

必要能力必须通过 Baga Ink API / Capability Provider 暴露。

## 11.2 设备差异由 Adapter 消化

```text
App
 │
Baga Ink API
 │
Baga Ink Platform
 │
Device Adapter
 │
Vendor / OS
```

不得反过来要求 App 大量识别设备品牌和系统细节。

## 11.3 API 版本必须稳定且可协商

IKP Manifest 必须声明 API 版本。

平台 MUST 能够判断：

- 当前 App 能否运行；
- 是否缺少 Capability；
- 是否需要兼容层；
- 是否明确拒绝安装。

不能通过“先运行，崩了再说”来处理兼容性。

## 11.4 兼容认证

未来建立：

> **Baga Ink Compatibility Test Suite**

以及设备认证：

> **Baga Ink Compatible**

Universal 标识 MUST 建立在兼容测试之上。

---

# 12. Kindle 平台战略

Kindle 当前 Homebrew 生态是 Baga Ink 的重要基础，但不是未来第三方开发者应该直接面对的统一开发模型。

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

Baga Ink 的策略是：

> **收编和封装现有 Kindle Homebrew 能力，而不是为了“纯洁架构”从零重写整个生态。**

逻辑关系：

```text
现有 Kindle Homebrew 基础设施
            │
            ▼
   Baga Ink Kindle Adapter
            │
            ▼
     Baga Ink Platform
            │
            ▼
         .ikp Apps
```

早期 KUAL、MRPI 等 MAY 继续承担安装、启动或兼容桥梁角色。

长期普通用户应该看到的是：

```text
Kindle Home
    │
    ▼
LifeBook / Baga Ink
    │
    ▼
Baga Ink Market
```

而不是被要求理解 KUAL、MRPI、Shell、Framebuffer 等内部基础设施。

---

# 13. KOReader 的战略位置

KOReader 是 Baga Ink 的重要技术基础和 Reference Implementation 来源，但：

> **Baga Ink API ≠ KOReader API**

Baga Ink MAY 大量复用：

- Lua UI；
- ReaderUI；
- Input abstraction；
- Display / Device abstraction；
- EPUB / PDF 能力；
- 字体与排版；
- Kindle 兼容经验。

但第三方 Baga Ink App MUST 不直接绑定 KOReader 内部对象。

正确关系：

```text
Third-party App
      │
      ▼
Baga Ink API
      │
      ▼
Baga Ink Platform
      │
      ├── KOReader-derived components
      ├── Rust / C Core
      └── Device Adapter
```

这样未来即使重构或替换部分 KOReader 组件，也不会破坏第三方生态。

---

# 14. Android E-Paper 平台战略

Android 墨水屏设备本质仍然运行 Android 应用。

因此：

> **Baga Ink Platform 本身 MAY 作为 Android APK 安装。**

但 Universal Baga Ink App 不要求开发者分别制作 APK。

```text
Android E-Paper Device
        │
        ▼
Baga Ink Platform.apk
        │
        ▼
Baga Runtime / API
        │
        ▼
     .ikp Apps
```

Android Platform 内部 MAY 使用：

- Kotlin；
- Java；
- JNI；
- Rust；
- C / C++；
- 厂商 E-Paper SDK。

这些实现细节被 Device Adapter 封装。

第三方 Universal App 只面对 Baga Ink API。

其战略收益是：

> **Platform 适配一次设备或厂商，所有 Universal Apps 同时获益。**

---

# 15. Baga Ink Client

Baga Ink Client 是 Baga Ink 生态的桌面入口。

首要支持目标：

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

客户端必须坚持以下安全原则：

- MUST 不清除用户书籍；
- MUST 不清除用户笔记；
- MUST 不要求恢复出厂作为标准流程；
- MUST 尽可能做到失败可恢复；
- MUST 对未知或不安全组合明确显示“不支持 / 实验性支持”，不能假装兼容。

Baga Ink Client 是**管理 Baga Ink Platform 的工具**，不是 Platform 本身。

---

# 16. Baga Ink Market

Baga Ink Market 的战略职责不是“收集 APK / 脚本”。

Market 的核心作用包括：

1. 应用发现与分发；
2. 数字签名与开发者身份；
3. API 版本检查；
4. Capability 要求检查；
5. Compatibility Test；
6. 权限展示；
7. 更新、回滚和撤回；
8. Universal / Enhanced 等兼容标签；
9. 应用审核与生态治理。

Market SHOULD 优先鼓励 Universal App，并清晰标记厂商私有依赖。

---

# 17. 开发者体验目标

理想开发流程：

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

第三方开发者 SHOULD 尽可能不需要知道：

- 当前 Kindle 固件私有细节；
- BOOX 私有刷新类；
- 某个 iReader 系统接口；
- 某款设备 CPU ABI；
- Kindle framebuffer；
- Android 厂商 API 差异。

这就是 Baga Ink Platform 存在的理由。

---

# 18. Baga Ink Device Adapter

每类设备通过 Device Adapter 实现平台要求。

```text
Baga Ink Platform
        │
        ├── Kindle Adapter
        ├── Generic Android Adapter
        ├── BOOX Adapter
        ├── iReader Adapter
        ├── Bigme Adapter
        └── Future Adapters
```

Adapter 负责抽象：

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

长期目标要从：

> Baga Ink 团队主动适配每一家厂商

逐渐转变为：

> 设备厂商主动实现 Baga Ink Device Adapter，并通过 Compatibility Test。

这是平台从“兼容项目”走向“行业事实标准”的关键转折点。

---

# 19. Platform 与操作系统的边界

Baga Ink **不是新的墨水屏操作系统**。

它不试图替换：

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
Baga Ink Platform
 │
Device Adapter
 │
Existing OS / Firmware
 │
Hardware
```

战略理由：

- 能覆盖大量存量 Kindle；
- 能利用现有 Android E-Paper 设备；
- 不承担完整 OS 的巨大维护成本；
- 厂商合作门槛更低；
- 更容易吸引开发者；
- 可以保持 Runtime 足够轻量。

---

# 20. Runtime / Core 的轻量原则

Baga Ink Runtime 不是：

```text
Chromium
Electron
完整 JVM 替代品
完整 Android Runtime
Heavy Web Runtime
```

第一阶段核心组成原则上只是：

```text
Lua VM
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

高性能或系统层模块 MAY 使用 Rust / C / C++。

目标不是制造新的庞大 Runtime，而是提供一条稳定、轻量的跨设备应用边界。

---

# 21. 开放生态与平台控制的平衡

Baga Ink 的开放性不能以失去标准为代价。

平台 SHOULD 允许：

- 第三方开发 App；
- 第三方贡献 Device Adapter；
- 第三方开发 Capability Provider；
- 第三方参与 SDK / Runtime；
- 厂商实现官方设备适配。

但 Universal 标准不能退化为“什么都允许”。

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

# 22. Baga Ink 的长期护城河

Baga Ink 的长期价值不只来自代码。

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

最终目标不是：

> “Baga Ink 团队能适配多少墨水屏。”

而是：

> **“新的墨水屏设备是否愿意主动声明并实现 Baga Ink Compatible。”**

---

# 23. 非目标（Non-Goals）

现阶段 Baga Ink 不以以下事情为目标：

1. 自研完整 E-Paper OS；
2. 替换 Android；
3. 替换 Kindle OS；
4. 强迫所有底层模块使用 Lua；
5. 强迫 Platform Core 只使用一种语言；
6. 将现有 Kindle Homebrew 全部从零重写；
7. 允许 Universal App 任意穿透设备底层；
8. 为每个厂商长期维护第三方 App 分叉；
9. 把 LifeBook 私有 API 当作平台标准；
10. 仅仅做一个聚合 APK / KUAL 应用的下载站。

---

# 24. 第一阶段实施路线

## Phase 0 — Specification First

优先定义：

- Baga Ink App Standard；
- Baga Ink API v0；
- Baga Lua Profile；
- Baga Ink IKP Package Specification；
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

目标不是先支持最多设备，而是证明：

> **同一个 `.ikp` App 可以运行在两个完全不同的系统上。**

## Phase 2 — LifeBook Reference App

LifeBook 作为第一批旗舰 / Reference App：

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

允许并鼓励硬件厂商：

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
| 是否引入重型 Runtime | **否** |

---

# 26. 战略成功标准

Baga Ink Platform 是否成功，不能只看支持了多少设备、Market 有多少应用。

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

那么即使拥有应用市场、客户端和大量兼容脚本，Baga Ink 仍然只是一个聚合层，而不是统一平台。

---

# 27. 项目的长期方向

Baga Ink 的最终战略不是成为“另一个 Kindle 工具”，也不是成为“另一个 Android 墨水屏 Launcher”。

它要逐步建立的是：

> **一个位于现有操作系统之上的轻量 E-Paper Application Platform。**

Baga Ink 不要求所有硬件相同，不要求所有操作系统相同，也不要求底层实现语言相同。

它只要求一件最重要的事情：

> **第三方应用面对同一个稳定平台。**

这条边界，是 Baga Ink 长期必须守住的核心。
