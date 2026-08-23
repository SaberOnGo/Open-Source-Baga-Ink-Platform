# Baga Ink 顶层战略与架构 / Baga Ink Platform Strategy & Architecture

> **文档级别：Strategic Source of Truth / 项目最高层级定义**  
> **状态：Strategic Baseline v0.6**  
> **日期：2026-08-23**  
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

### 0.3 成熟实现复用原则 / Mature Implementation Reuse

Baga Ink 标准定义的是：

```text
公开 API
跨设备语义
Capability / Permission
兼容性与安全边界
Baga Lua Profile / Standard Libraries
```

标准 **不规定 Platform 内部必须采用何种软件分层，也不要求已经存在成熟实现的能力重新从零开发。**

Platform Core、Device Adapter 与官方设备实现 SHOULD 优先评估并复用成熟、持续维护、许可证兼容且经过实际验证的开源组件。复用方式 MAY 包括：

```text
整体采用
组合使用
抽取稳定模块
直接采用其成熟 API
调用其已有协议 / 数据格式 / 算法
包装其成熟设备能力
```

如果某个通用库本身已经形成稳定、跨平台且广泛采用的抽象，Baga SHOULD 优先把它作为 **Standard Library / Adopted Component** 直接采用，而不是先发明一个更弱的平台私有包装。

当前明确例子：

```text
SQLite + lsqlite3
→ Baga Lua Profile 的标准数据库库
→ 开发者直接使用 SQLite / SQL 语义

Automerge core
→ Local-first / CRDT 优先基础
→ 可整体采用，也可拆用 document/merge、binary、sync、C FFI 等模块

KOReader / koreader-base / FBInk
→ Kindle Platform / Adapter 的成熟实现来源
```

但这些项目的存在：

- MUST NOT 自动形成新的 Baga Ink 公共架构层；
- MUST NOT 因为“用了一个库”就创造对应的 `Provider / Engine / Runtime` 层；
- MUST NOT 自动把该库的私有对象、术语、文件格式或 API 变成 `baga.*` 标准；
- MAY 在经过正式标准决策后，把成熟库本身的 API / protocol / format 纳入 Baga Standard Library / Profile；
- MUST NOT 要求 IKP App 知道底层具体设备实现；
- MUST NOT 绕过 BICTS、Permission、Sandbox 与 Compatibility 要求。

原则：

> **Reuse before reimplement. Standardize semantics, not internal implementation layering.**  
> **优先复用，不重复造轮子；标准化语义，不标准化内部软件分层。**

标准库与成熟组件的具体规则见：

`13_标准库与成熟组件采用规范_Baga-Ink-Standard-Libraries-and-Adopted-Components.md`

正式 Standards 与 Reference Apps MUST 只描述当前有效设计；历史方案由 Git commit / diff 保存。

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

内部复用 KOReader、SQLite、Automerge、FBInk 或其他组件时，上图不因此增加新的公共层级。

Baga Lua Profile 中的 Standard Libraries 也不是新的架构层；它们只是 App 在稳定运行环境里可直接使用的成熟通用库。

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
| 标准库规范 | **Baga Ink Standard Libraries and Adopted Components** |
| 开发者门户 | **Baga Ink Developers** |
| 旗舰 Reference App | **LifeBook** |
| Kindle 产品描述 | **LifeBook for Kindle** |

---

# 5. Baga Ink Platform 的边界

Baga Ink Platform 包括：

- Platform Core；
- Embedded Lua Interpreter；
- Baga Lua Profile；
- Baga Lua Profile Standard Libraries；
- Baga Ink API；
- App Lifecycle；
- UI / Display / Input / Storage / Library / Network / Power / Reader / Sync 等标准能力；
- Capability Model；
- Permission / Sandbox；
- IKP Package Manager；
- Device Adapter；
- Compatibility hooks。

这些共同组成一个轻量设备端平台。

**Baga Ink Platform 不等于 Baga Ink Client，也不等于 Baga Ink Market。**

具体能力内部可以复用成熟开源实现；这些实现不是额外的产品层。

---

# 6. 官方 Universal App 模型

## 6.1 官方语言

第一官方 Universal App 语言：

> **Lua / Baga Lua Profile**

Baga Lua Profile 定义：

- 可使用的 Lua 语言特性；
- 基础标准库范围；
- Adopted Standard Libraries；
- `baga.*` API；
- 生命周期；
- 安全限制；
- 系统逃逸限制。

Kindle MAY 复用 KOReader 等成熟项目已经验证的 Lua 能力；Android Baga Ink Platform APK MAY 直接嵌入轻量 Lua 解释器。

第三方 App 不依赖具体解释器来源。

当前正式外部 Standard Library：

```text
lsqlite3
→ 直接使用成熟 SQLite / SQL 语义
```

当前 Adopted Foundation：

```text
Automerge core
→ Local-first / CRDT 优先基础
→ developer-facing Lua binding 尚未冻结
```

详细定义见 `13_标准库与成熟组件采用规范_Baga-Ink-Standard-Libraries-and-Adopted-Components.md`。

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
Automerge core / C FFI bridge 等成熟库集成
```

Platform 内部允许 Rust、C/C++、Kotlin/Java、JNI、Shell 等按实际设备使用。

**语言统一发生在第三方 App 边界，不发生在所有底层代码。**

同理，内部实现所选开源库也不构成第三方 App 必须理解的新边界。

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

由 Baga Lua Profile 正式提供的标准库不需要被每个 IKP 重复打包。

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

SQLite / lsqlite3 不是硬件 Capability，而是 Baga Lua Profile Standard Library。

---

# 9. Permission 与 Capability 必须分离

Capability：设备**能不能**。

Permission：App **允不允许**。

例如：

```text
Capability: network.wifi
Permission: network
```

权限必须由 Manifest 预声明，并遵循最小权限原则。

正式定义见：

`05_权限模型_Baga-Ink-Permission-Model.md`

---

# 10. Baga Ink API 是唯一稳定设备/平台 App 边界

公开 namespace：

```lua
baga.api
baga.app
baga.ui
baga.display
baga.input
baga.device
baga.storage
baga.library
baga.network
baga.power
baga.reader
baga.sync
baga.permissions
baga.log
```

结构化关系数据直接使用 Baga Lua Profile 标准库 `lsqlite3` / SQLite。

Baga Ink API 与 Baga Lua Profile Standard Libraries 共同构成开发者稳定运行环境，但概念上必须区分：

```text
baga.*
→ 统一设备 / OS / Platform 差异

lsqlite3 / adopted libraries
→ 直接采用成熟通用软件能力
```

v0.x 允许快速演进，但最终必须长期版本化。

Baga Ink MUST 不提供一个任意执行 Shell、获取 Android Context、直接调用 Vendor SDK 的万能系统逃生口。

新增平台能力的正确流程：

```text
真实需求
  ↓
先判断：已有成熟通用库，还是设备/平台差异？
  ↓
成熟通用库 → Standard Library / Adopted Component
设备/平台差异 → Capability / Baga Ink API
  ↓
Platform implementation
  ↓
BICTS
```

内部实现可以直接复用成熟开源组件，不要求先人为增加新的公共 `Provider / Engine` 架构层。

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

这里的 Vendor Provider 是 Android Adapter 内部对厂商私有能力的 specialization，不代表所有 Baga Ink API 都必须经过通用 Provider 层。

---

# 13. Kindle 战略

Kindle 现有 Homebrew 生态是重要基础，不是要从零推翻的对象。

Baga Ink SHOULD 尽量复用：

```text
KOReader device / reader / display / input / annotation knowledge
koreader-base / MuPDF / CREngine 等已有阅读基础
KUAL / PEKI 类启动基础
MRPI / KPM / Hotfix 类安装与 Homebrew 基础
FBInk / framebuffer 相关显示能力
Kindle 系统服务桥接
KOReader 已有 libsqlite3
KOReader 内部现有 lua-ljsqlite3（仅内部继续使用）
Baga IKP 标准 SQLite binding：lsqlite3
Automerge core（确有 Local-first / CRDT 需求时整体或拆模块采用）
```

这些全部属于 **Baga Ink Platform on Kindle 的内部实现与标准库供给选择**；不因此形成新的公共架构层。

第三方 IKP App：

```text
设备能力 → baga.*
关系数据库 → require("lsqlite3")
```

不需要知道 KOReader 内部仍使用 `lua-ljsqlite3`。

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
        ├── Baga Lua Profile / Standard Libraries
        ├── Embedded Lua Interpreter
        └── Android E-Paper Adapter
        │
        ▼
      *.ikp
```

Generic Android 负责公共 Android 能力；Vendor Provider 负责 E-Paper 私有刷新、Pen、前光等能力。

Android 的版本差异与厂商碎片化必须停在 Adapter 以下。

Android 实现同样 SHOULD 优先复用成熟系统能力和开源组件，而不是为了保持“代码看起来统一”重新实现数据库、网络、文档引擎或同步算法。

SQLite 由 Baga Platform 锁定并提供可预测版本，IKP 通过 `lsqlite3` 使用，不依赖 OEM 系统 SQLite 版本差异。

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

Standard Libraries 也必须有独立一致性测试，例如 `lsqlite3` API、SQLite compile profile 与 sandbox 行为。

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

LifeBook 如果遇到通用能力缺失，应先判断：

```text
设备/平台差异 → 推动 baga.* / Capability
成熟通用软件能力 → 优先直接采用 Standard Library / Mature Component
```

而不是加入 Vendor 私有分支或重复造轮子。

具体实现规范位于：

`docs/reference-apps/01_LifeBook参考实现_LifeBook-Reference-App.md`

---

# 19. 开放生态与控制边界

Baga Ink SHOULD 允许：

- 第三方开发 IKP App；
- 第三方贡献 Device Adapter；
- 厂商实现 Adapter；
- 第三方贡献 Capability Provider；
- 第三方参与 SDK / Platform Core；
- 第三方贡献 Standard Library integration / compatibility tests。

但开放不等于没有标准。

根本原则：

> **底层允许多样，上层保持统一。**

```text
App 层           高度统一
API 层           高度稳定
Standard Library 直接采用成熟通用语义
Capability 层    标准化设备/平台扩展
Adapter 层       允许设备差异
OS 层            可以完全不同
Hardware 层      可以完全不同
```

Standard Library 不是新的软件架构层，而是开发环境中的稳定库集合。

内部依赖树、第三方库组合方式与具体源码目录不属于上述公共层级模型。

---

# 20. 第一阶段实施路线

## Phase 0 — Standards

现阶段首先锁定：

```text
App Standard
API
Standard Libraries / Adopted Components
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

同时验证：

```text
lsqlite3 + pinned SQLite
KOReader reader/UI integration
Automerge core 在代表性硬件上的可行性
```

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
Standard Libraries
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
10. 建造重复、庞大、需要额外维护的平台中间系统；
11. 因采用一个开源库而人为增加新的公共架构层；
12. 在已有成熟、许可证兼容且可验证的实现可复用时，仅为了“完全自研”而重新实现 Reader、数据库、同步合并算法或设备基础设施；
13. 把 SQLite 再包装成更弱的私有 KV/Collection 数据库接口；
14. 因 Automerge 很优秀就机械采用 automerge-repo 的所有层或把所有数据都 CRDT 化。

---

# 23. 战略成功标准

最终只看一个问题：

> **第三方开发者能否只学习一次 Baga Ink SDK / Lua Profile，生成一个 `.ikp`，在 Kindle 与多个 Android E-Paper 设备上运行，而不需要理解每台设备的私有实现？**

其中成熟通用能力应该尽量沿用成熟生态：

```text
关系数据 → SQLite / lsqlite3
Reader → Baga Reader API，平台内部复用 KOReader 等
Local-first CRDT → Automerge core 优先
```

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

> **第三方应用面对同一个稳定平台，并能直接复用成熟通用软件生态。**
