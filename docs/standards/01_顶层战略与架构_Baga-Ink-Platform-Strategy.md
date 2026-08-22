# Baga Ink 顶层战略与架构 / Baga Ink Platform Strategy & Architecture

> **文档级别：Strategic Source of Truth / 项目最高层级定义**  
> **状态：Strategic Baseline v0.3**  
> **日期：2026-08-22**  
> **规范入口：`00_规范总览_Baga-Ink-Standards-Index.md`**

---

## 0. 文档地位

本文档定义 **Baga Ink** 的长期战略边界、平台定位、生态品牌、应用模型、开发者模型、设备兼容模型与防碎片化原则。

它是 `docs/standards/` 中的最高层级技术战略文档。

下位规范、SDK、Platform Core、Device Adapter、Baga Ink Client、Baga Ink Market、LifeBook Reference App 以及未来 OEM 接入方案都不得静默违反本文件。

### 0.1 规范性用词

- **MUST / 必须**：平台级硬约束；
- **SHOULD / 应当**：默认应遵守；
- **MAY / 可以**：允许的实现选择。

### 0.2 轻量术语原则

设备端只需要理解：

```text
Baga Ink Platform
├── Baga Ink Platform Core
├── Embedded Lua Interpreter
├── Baga Lua Profile
├── Baga Ink API
├── IKP Package Manager
└── Baga Ink Device Adapter
```

Lua 解释器只是 Platform Core 内部嵌入或复用的一项轻量能力，不是独立产品层。

项目不得把 Baga Ink 描述成需要用户额外安装、独立理解和独立维护的庞大中间执行系统。

---

# 1. 一句话定义

> **Baga Ink Platform 是面向 Kindle 与 Android 墨水屏设备的统一、轻量、跨设备应用平台。**

目标不是再做一个墨水屏 App，而是：

> **让分散的 Kindle Homebrew 与 Android E-Paper 设备，在第三方开发者眼中逐渐成为同一个应用平台。**

---

# 2. 战略问题

今天的墨水屏生态高度碎片化：

```text
Kindle
├── 不同型号
├── 不同固件
├── Homebrew / KUAL / MRPI / KOReader 等基础设施
└── 不同显示 / 输入 / 系统行为

Android E-Paper
├── iReader / 掌阅
├── BOOX / 文石
├── Bigme
├── Hanvon / 汉王
├── 墨案
└── 其他厂商
    ├── 不同 Android 版本
    ├── 不同刷新接口
    ├── 不同 Pen SDK
    └── 不同电源 / 前光 / 系统接口
```

如果每个开发者都逐设备适配，生态会持续碎片化。

Baga Ink 的战略是：

> **把碎片化压缩到 Device Adapter 以下，而不是让它扩散到每一个 App。**

---

# 3. 总体架构

```text
                   Third-party IKP Apps
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
                          ▼
                Baga Ink Device Adapter
                     ┌────┴────┐
                     │         │
                     ▼         ▼
                  Kindle    Android E-Paper
```

核心原则：

> **应用不适配设备；设备通过 Baga Ink Device Adapter 适配平台。**

---

# 4. Baga Ink 品牌与产品层级

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

正式名称：

| 对象 | 正式名称 |
|---|---|
| 整个生态品牌 | **Baga Ink** |
| 统一设备端平台 | **Baga Ink Platform** |
| PC / Mac 客户端 | **Baga Ink Client** |
| 应用市场 | **Baga Ink Market** |
| SDK | **Baga Ink SDK** |
| API | **Baga Ink API** |
| 应用标准 | **Baga Ink App Standard** |
| 能力标准 | **Baga Ink Capability Registry** |
| 权限标准 | **Baga Ink Permission Model** |
| 包格式 | **IKP / `.ikp`** |
| 设备适配层 | **Baga Ink Device Adapter** |
| 兼容性标准 | **Baga Ink Compatibility Standard** |
| 测试套件 | **Baga Ink Compatibility Test Suite / BICTS** |
| 开发者门户 | **Baga Ink Developers** |
| 旗舰 Reference App | **LifeBook** |
| Kindle 产品描述 | **LifeBook for Kindle** |

---

# 5. Baga Ink Platform 的边界

Baga Ink Platform 包括：

- Platform Core；
- Embedded Lua Interpreter；
- Baga Lua Profile；
- Baga Ink API；
- App Lifecycle；
- UI / Display / Input / Storage / Network / Power / Reader 等标准能力；
- Capability Model；
- Permission / Sandbox；
- IKP Package Manager；
- Device Adapter；
- Compatibility hooks。

这些共同组成一个轻量设备端平台。

**Baga Ink Platform 不等于 Baga Ink Client，也不等于 Baga Ink Market。**

---

# 6. 官方 Universal App 模型

## 6.1 官方语言

第一官方 Universal App 语言：

> **Lua / Baga Lua Profile**

Baga Lua Profile 定义：

- 可使用的 Lua 语言特性；
- 标准库范围；
- `baga.*` API；
- 生命周期；
- 安全限制；
- 系统逃逸限制。

Kindle MAY 复用 KOReader 等成熟项目已经验证的 Lua 能力；Android Baga Ink Platform APK MAY 直接嵌入轻量 Lua 解释器。

第三方 App 不依赖具体解释器来源。

## 6.2 为什么不是 Kotlin / Java 作为统一 App 语言

Android 可以天然使用 Kotlin / Java，但 Kindle 不是 Android。

把 Kotlin / Java 作为跨平台 App 语言会迫使 Kindle 引入不必要的大型框架层，违背存量设备与轻量化目标。

## 6.3 Rust 的位置

Rust 更适合：

```text
Platform Core
network / sync infrastructure
parsers
security-sensitive components
Device Adapter
Capability Provider
```

Platform 内部允许 Rust、C/C++、Kotlin/Java、JNI、Shell 等按实际设备使用。

**语言统一发生在第三方 App 边界，不发生在所有底层代码。**

---

# 7. IKP：统一应用分发单位

Universal App 标准包格式：

> **IKP / `.ikp`**

例如：

```text
lifebook.ikp
rss-reader.ikp
notes.ikp
```

同一个 IKP 应可以跨 Kindle 与 Android E-Paper 使用。

IKP 主要包含：

```text
manifest.json
main.lua
src/
assets/
locales/
signature/
```

Universal IKP MUST NOT 把以下内容作为正常应用执行依赖：

```text
设备专用 native binary
Android APK / DEX 主逻辑
Kindle shell bridge
BOOX / iReader 私有 SDK wrapper
自己的 Lua 解释器
自己的 Device Adapter
自己的 Platform Core
```

原则：

> **应用代码与资源属于 IKP；设备兼容与共享平台能力属于 Baga Ink Platform。**

---

# 8. Capability-first：防碎片化核心

Universal App MUST 查询能力，而不是品牌。

正确：

```lua
if baga.device.has("input.pen") then
    enable_pen_ui()
end

if baga.device.has("display.fast_refresh") then
    enable_fast_interaction()
end
```

错误：

```lua
if vendor == "BOOX" then ... end
if device == "Kindle" then ... end
```

正式 Capability 只允许来自：

`04_能力注册表_Baga-Ink-Capability-Registry.md`

Base Profile：

```text
display.basic
input.navigation
storage.app_sandbox
power.sleep_wake
platform.lifecycle
```

典型 Optional Capability：

```text
display.partial_refresh
display.fast_refresh
display.color
input.touch
input.pen
input.pen.low_latency
input.physical_page_key
network.wifi
light.frontlight
audio.output
bluetooth.available
```

---

# 9. Permission 与 Capability 必须分离

Capability：设备**能不能**。

Permission：App **允不允许**。

例如：

```text
Capability: network.wifi
Permission: network
```

权限必须由 Manifest 预声明，并遵守最小权限原则。

正式定义见：

`05_权限模型_Baga-Ink-Permission-Model.md`

---

# 10. Baga Ink API 是唯一稳定 App 边界

公开 namespace：

```lua
baga.api
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
baga.permissions
baga.log
```

v0.x 允许快速演进，但最终必须长期版本化。

Baga Ink MUST 不提供一个任意执行 Shell、获取 Android Context、直接调用 Vendor SDK 的万能系统逃生口。

新增平台能力的正确流程：

```text
真实需求
  ↓
Capability 语义
  ↓
API
  ↓
Device Adapter / Capability Provider
  ↓
BICTS
```

---

# 11. UI 战略

Baga Ink UI 不是手机 UI 的机械移植。

核心原则：

- 高对比度；
- 页面式 / 稳定布局优先；
- Focus 为一级概念；
- Touch 与物理导航统一；
- 少动画；
- 少全屏刷新；
- Dirty Region；
- App 表达刷新意图，Platform 决定刷新实现；
- Color / Pen / Fast Refresh 都作为渐进增强。

正式定义：

`09_UI规范_Baga-Ink-UI-Specification.md`

---

# 12. Device Adapter 战略

```text
Baga Ink Platform Core
        │
        ├── Kindle Adapter
        └── Android E-Paper Adapter
             ├── Generic Android
             ├── BOOX Provider
             ├── iReader Provider
             ├── Bigme Provider
             ├── Hanvon Provider
             └── Future Providers
```

Adapter 负责吸收：

```text
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
Device quirks
Firmware differences
```

Adapter MUST 不成为第二套应用 API。

---

# 13. Kindle 战略

Kindle 现有 Homebrew 生态是重要基础，不是要从零推翻的对象。

Baga Ink SHOULD 尽量复用：

```text
KOReader device / reader / display / input knowledge
KUAL / PEKI 类启动基础
MRPI 类安装基础
FBInk / framebuffer 相关成熟能力
Kindle 系统服务桥接
```

但这些全部属于 Kindle Adapter / Baga Ink Client 的实现细节。

第三方 IKP App 不需要知道它们存在。

另外：

> **Kindle Adapter 规范与具体 jailbreak / 安装入口数据库必须分离。**

因为越狱入口会随型号和固件变化，而平台契约必须稳定。

---

# 14. Android E-Paper 战略

Android 上：

```text
Baga Ink Platform.apk
        │
        ├── Platform Core
        ├── Baga Ink API
        ├── Embedded Lua Interpreter
        └── Android E-Paper Adapter
        │
        ▼
      *.ikp
```

Generic Android 负责公共 Android 能力；Vendor Provider 负责 E-Paper 私有刷新、Pen、前光等能力。

Android 的版本差异与厂商碎片化必须停在 Adapter 以下。

---

# 15. Baga Ink Client 战略

Baga Ink Client 是 Windows / macOS 上的统一设备入口。

核心流程：

```text
连接设备
  ↓
识别型号 / 固件 / 系统
  ↓
查询 Compatibility / Installation Database
  ↓
Compatible / Experimental / Unsupported
  ↓
安全安装 / 修复 / 升级 Baga Ink Platform
  ↓
安装 LifeBook / Market Apps
```

硬规则：

- 不清用户书籍；
- 不清用户笔记；
- 不把恢复出厂当作标准方案；
- 失败尽可能可恢复；
- 未验证组合不假装支持。

---

# 16. Baga Ink Market 战略

Market 不是 APK / 脚本下载站。

它必须强化平台标准：

```text
IKP validation
publisher signature
API compatibility
Capability compatibility
Permission disclosure
Universal / Enhanced labels
update / rollback
Compatibility data
```

长期 Market MAY 进一步承载字体、词典、主题、Device Adapter、Capability Provider 与服务扩展。

---

# 17. Compatibility：从口号到可验证标准

设备不能因为“能跑 LifeBook”就自动称为 Compatible。

正式兼容必须基于：

> **Baga Ink Compatibility Test Suite / BICTS**

认证对象：

```text
Device Model
+ Firmware / OS Range
+ Platform Version
+ Adapter Version
+ Compatibility Standard Version
+ BICTS Version
```

状态：

```text
Baga Ink Compatible
Experimental
Unsupported
```

正式规则见 `08` 与 `10` 两份规范。

---

# 18. LifeBook 的战略位置

LifeBook 是：

> **Baga Ink 的旗舰 Reference App。**

LifeBook 必须像第三方 Universal App 一样遵守标准，而不是依赖官方特权。

核心目标：

```text
同一个 lifebook.ikp
      │
      ├── Kindle
      └── Android E-Paper
```

LifeBook 如果遇到通用能力缺失，应推动标准 API / Capability，而不是加入 Vendor 私有分支。

具体实现规范位于：

`docs/reference-apps/01_LifeBook墨水屏参考应用实现规范_LifeBook-Ink-Reference-App-Implementation-Specification.md`

---

# 19. 开放生态与控制边界

Baga Ink SHOULD 允许：

- 第三方开发 IKP App；
- 第三方贡献 Device Adapter；
- 厂商实现 Adapter；
- 第三方贡献 Capability Provider；
- 第三方参与 SDK / Platform Core。

但开放不等于没有标准。

根本原则：

> **底层允许多样，上层保持统一。**

```text
App 层           高度统一
API 层           高度稳定
Capability 层    标准化扩展
Adapter 层       允许设备差异
OS 层            可以完全不同
Hardware 层      可以完全不同
```

---

# 20. 第一阶段实施路线

## Phase 0 — Standards

现阶段首先锁定：

```text
App Standard
API
Capability Registry
Permission Model
IKP
Device Adapter Standard
Compatibility Standard
UI Standard
BICTS
Kindle Adapter
Android E-Paper Adapter
```

## Phase 1 — Reference Platforms

建立：

```text
Kindle Reference Adapter
+
Android E-Paper Reference Adapter
```

证明同一个 IKP 能在两种完全不同系统上运行。

## Phase 2 — LifeBook Reference App

完成 LifeBook Universal Skeleton + Reading Core。

## Phase 3 — SDK / CLI / Simulator

让普通开发者不需要掌握 Kindle / Vendor 私有接口即可创建 IKP。

## Phase 4 — Market / Compatibility

建立签名、分发、BICTS、Compatible 认证。

## Phase 5 — OEM Adoption

让厂商主动实现 Adapter、跑测试、声明支持 Baga Ink Apps。

---

# 21. 长期护城河

真正的壁垒不是某一个 App，而是：

```text
统一标准
+
IKP
+
API
+
Capability Registry
+
Device Adapters
+
BICTS
+
存量设备覆盖
+
Market
+
开发者
+
OEM 支持
```

形成网络效应：

```text
更多设备
  ↓
更多用户
  ↓
更多开发者
  ↓
更多 IKP Apps
  ↓
设备兼容 Baga Ink 更有价值
  ↓
更多 OEM 主动适配
```

---

# 22. 非目标 / Non-Goals

Baga Ink 当前不以以下为目标：

1. 自研完整 E-Paper OS；
2. 替换 Android；
3. 替换 Kindle OS；
4. 从零重写整个 Kindle Homebrew 生态；
5. 强迫所有底层代码使用 Lua；
6. 强迫 Platform Core 只使用一种语言；
7. 允许 Universal App 任意穿透系统；
8. 为每个品牌维护一套 App 分支；
9. 把 LifeBook 私有需求当作平台标准；
10. 建造重复、庞大、需要额外维护的平台中间系统。

---

# 23. 战略成功标准

最终只看一个问题：

> **第三方开发者能否只学习一次 Baga Ink SDK，生成一个 `.ikp`，在 Kindle 与多个 Android E-Paper 设备上运行，而不需要理解每台设备的私有实现？**

如果答案是“是”，Baga Ink 是平台。

如果仍需要：

```text
Kindle 一套业务代码
BOOX 一套
iReader 一套
Bigme 一套
```

那么即使拥有 Client、Market 和兼容脚本，Baga Ink 仍然只是聚合层。

---

# 24. 长期方向

Baga Ink 最终要建立的是：

> **一个位于现有操作系统之上的轻量 E-Paper Application Platform。**

它不要求硬件相同，不要求 OS 相同，也不要求底层实现语言相同。

它只要求最重要的一件事：

> **第三方应用面对同一个稳定平台。**
