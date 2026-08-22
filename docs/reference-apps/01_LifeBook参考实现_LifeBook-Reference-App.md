# LifeBook 墨水屏参考应用实现规范 / LifeBook Ink Reference App Implementation Specification

> **文档级别：参考应用实现规范 / Reference App Implementation Specification**  
> **状态：Baseline v0.3**  
> **日期：2026-08-23**  
> **适用对象：LifeBook on Baga Ink Platform**  
> **本文件不是 Baga Ink Standard，不得覆盖或修改上位标准。**

---

## 0. 文档目的

本文档规定 **LifeBook** 作为 Baga Ink Platform 旗舰 Reference App 的实现边界、模块划分、跨设备原则、UI / Reader / 本地数据 / 同步策略，以及它与 Baga Ink Standards 的关系。

LifeBook 的任务不是创造另一套平台标准，而是：

> **用一个真实、完整、长期维护的旗舰应用验证 Baga Ink Standards，证明同一份 IKP 应用代码可以运行在 Kindle 与多种 Android E-Paper 设备上。**

如果 LifeBook 的需求与现有 Baga Ink 标准发生冲突，LifeBook MUST 服从上位标准。新的跨设备公共能力必须先进入标准治理流程，不得通过 LifeBook 私有接口静默绕过标准。

---

# 1. 上位规范与优先级

LifeBook MUST 遵守 `docs/standards/` 中的正式规范：

```text
00_规范总览_Baga-Ink-Standards-Index.md
01_顶层战略与架构_Baga-Ink-Platform-Strategy.md
02_应用标准_Baga-Ink-App-Standard.md
03_API规范_Baga-Ink-API-Specification.md
04_能力注册表_Baga-Ink-Capability-Registry.md
05_权限模型_Baga-Ink-Permission-Model.md
06_IKP应用包规范_IKP-Package-Specification.md
07_设备适配器规范_Baga-Ink-Device-Adapter-Specification.md
08_兼容性标准_Baga-Ink-Compatibility-Standard.md
09_UI规范_Baga-Ink-UI-Specification.md
10_兼容性测试套件_Baga-Ink-Compatibility-Test-Suite.md
11_Kindle适配规范_Baga-Ink-Kindle-Adapter.md
12_Android墨水屏适配规范_Baga-Ink-Android-E-Paper-Adapter.md
```

优先级：

```text
Baga Ink Standards
        >
本 LifeBook 实现规范
        >
LifeBook 具体代码与产品实现
```

---

# 2. LifeBook 的正式定位

LifeBook 是：

> **Baga Ink Platform 上的旗舰 App / Reference App。**

LifeBook MUST NOT 被描述或实现为：

- Baga Ink Platform 本身；
- Baga Ink Platform Core；
- Baga Ink Device Adapter；
- Baga Ink SDK；
- Baga Ink Market；
- Kindle / Android Vendor SDK 的统一封装层；
- 另一套需要单独安装和维护的平台中间系统；
- 只支持 EPUB 的 Reader App；
- KOReader 的产品外壳或必须依赖 KOReader 私有 API 的插件。

用户可见正式名称保持：

> **LifeBook**

需要区分 Kindle 产品版本时使用：

> **LifeBook for Kindle**

LifeBook SHOULD 同时承担：

1. 真正可长期使用的产品功能；
2. Baga Ink 的真实 Reference App，持续验证平台边界是否成立。

---

# 3. 正确总体架构

```text
                Baga Ink Standards
                       │
                       ▼
              Baga Ink App Standard
                       │
                       ▼
                 LifeBook App
                `lifebook.ikp`
                       │
                 only `baga.*`
                       │
                       ▼
                Baga Ink API
                       │
                       ▼
             Baga Ink Platform Core
                       │
                       ▼
             Baga Ink Device Adapter
                 ┌─────┴─────┐
                 │           │
                 ▼           ▼
              Kindle      Android E-Paper
```

核心规则：

> **LifeBook 适配 Baga Ink API；设备适配 Baga Ink Platform。LifeBook 不直接适配设备。**

KOReader、SQLite、Automerge、FBInk 等可能出现在具体 Platform 实现内部，但它们不构成 LifeBook 可见的新层。

---

# 4. LifeBook 与 Platform 的边界

## 4.1 LifeBook Application Core

属于 LifeBook：

```text
Account / Session
Library product logic
Articles
Q&A / Comments
Notes product logic
Public / Community Notes
Life Records
Time Capsule
AI
LifeBook Sync Domain Logic
```

这些是产品业务，不是 Baga Ink 公共标准。

## 4.2 Platform Core 不属于 LifeBook

以下属于 Baga Ink Platform：

```text
Baga Lua Profile
Embedded Lua Interpreter
baga.* API
UI foundation
Display abstraction
Input abstraction
Storage sandbox
Transactional local data service
Library bridge
Reader capability
Permission enforcement
IKP package management
Device Adapter
Compatibility hooks
```

LifeBook 不应复制这些能力。

## 4.3 Device Adapter 不属于 LifeBook

Kindle、Generic Android、BOOX、iReader、Bigme、Hanvon 等适配逻辑属于 Platform。

LifeBook MUST NOT 以长期标准代码维护：

```lua
if vendor == "BOOX" then ... end
if vendor == "iReader" then ... end
if is_kindle then ... end
if reader_impl == "KOReader" then ... end
```

正确方式：

```lua
if baga.device.has("display.fast_refresh") then
    enable_fast_interaction()
end

if baga.device.has("reader.anchor") then
    enable_public_note_jump()
end
```

---

# 5. LifeBook IKP

LifeBook 的标准跨设备包：

```text
lifebook.ikp
```

推荐逻辑结构：

```text
lifebook.ikp
├── manifest.json
├── main.lua
├── src/
│   ├── application/
│   ├── domain/
│   ├── views/
│   ├── reader/
│   ├── persistence/
│   └── sync/
├── assets/
├── locales/
└── signature/
```

Universal LifeBook IKP MUST NOT 携带：

- Android APK / DEX 作为业务执行依赖；
- Kindle shell bridge；
- BOOX / iReader SDK wrapper；
- 自带 Lua 解释器；
- 自带 Platform Core；
- 自带 Device Adapter；
- CPU ABI 相关主业务 native binary；
- KOReader / SQLite / Automerge native runtime 作为 Universal App 私有逃生口。

目标：

```text
                 lifebook.ikp
                     │
          ┌──────────┴──────────┐
          │                     │
          ▼                     ▼
Baga Ink on Kindle     Baga Ink on Android E-Paper
```

---

# 6. LifeBook 内部模块

```text
LifeBook (`lifebook.ikp`)
│
├── Application / Domain Core
│   ├── Account / Session
│   ├── Library Product Logic
│   ├── Articles
│   ├── Q&A / Comments
│   ├── My Notes / Highlights
│   ├── Public / Community Notes
│   ├── Life Records
│   ├── Time Capsule
│   ├── AI
│   └── Sync Domain Logic
│
├── E-Ink UI
│   └── baga.ui / baga.input / baga.display
│
├── Local Data
│   └── baga.data / baga.storage
│
├── Library Integration
│   └── baga.library
│
├── Reader Integration
│   └── baga.reader
│
└── Platform Integration
    ├── baga.app
    ├── baga.device
    ├── baga.network
    ├── baga.power
    ├── baga.sync
    ├── baga.permissions
    └── baga.log
```

Domain Core SHOULD 不知道当前是 Kindle 还是 Android，也不应知道本机具体用了 SQLite、KOReader 或 Automerge。

---

# 7. Reader 实现与格式边界

标准关系：

```text
LifeBook
   │
   ▼
baga.reader
   │
   ▼
Baga Ink Platform on current device
```

设备实现内部可以复用：

```text
KOReader / koreader-base
MuPDF / CREngine
其他成熟 Reader implementation
```

这些是实现细节，不是新的公共 Reader 层。

LifeBook MUST NOT 把 KOReader 私有 Lua 对象、XPointer、pboxes、sidecar schema 等当作长期 App API。

LifeBook 也 MUST NOT 把“EPUB”当作自己的 Reader 抽象边界。

正确语义：

```lua
if baga.reader.supports(source) then
    local session = baga.reader.open(source)
end
```

实际支持 EPUB、PDF、MOBI、FB2、TXT、DjVu、CBZ 或其他格式，由当前 Platform Reader implementation 决定并测试。

---

# 8. Reader Anchor 与其他用户笔记

“其他用户的笔记”要求把 LifeBook 云端业务对象稳定关联到书中正文，但 LifeBook 不应自己实现不同文件格式的定位算法。

标准关系：

```text
Reader selection / position
        │
        ▼
session:create_anchor(...)
        │
        ▼
Baga Reader Anchor
        │
        ├── LifeBook My Note
        └── LifeBook Public Note
```

LifeBook 对 Anchor 的规则：

- 把 Anchor 当作 opaque、可序列化的 Baga 值；
- 可以保存、同步、传给 `goto_anchor / resolve_anchor`；
- 不解析 Reader 私有字段；
- 不自己针对 EPUB/PDF/MOBI/CBZ 等格式写定位器；
- 当 `resolve_anchor` 只能近似恢复时，产品 UI 应正确处理，而不是声称精准命中。

Kindle 的 Baga implementation SHOULD 充分利用 KOReader 已有位置/annotation 机制：

```text
rolling/reflowable → KOReader/CREngine XPointer-like positions
paging/fixed-page  → page + local position / boxes
```

Readium Locator、EPUB CFI、W3C Web Annotation 只可作为设计参考，不决定 LifeBook 的格式支持边界。

---

# 9. UI 原则

LifeBook 的墨水屏 UI SHOULD：

- 高对比度；
- 减少无意义动画；
- 优先分页和稳定静态布局；
- 减少大面积高频重绘；
- 支持 Touch 与 Focus 导航；
- 支持 `page_next` / `page_previous`；
- 不依赖颜色传递唯一信息；
- 对 Pen / Color / Fast Refresh 做渐进增强；
- 遵守 `09_UI规范_Baga-Ink-UI-Specification.md`。

LifeBook 只表达：

```text
AUTO
TEXT
QUALITY
FAST
ANIMATION
```

等显示意图，不调用 Vendor waveform 或 raw framebuffer。

Kindle Platform 第一实现可以大量复用 KOReader UI/widget/UIManager，但 LifeBook 仍只使用 `baga.ui`。

---

# 10. Offline-first：三个不同问题

墨水屏经常休眠、断网或低频联网，LifeBook MUST 以 offline-first 为核心原则。

必须严格区分：

```text
A. Local Data
   当前设备上的可靠本地持久化

B. Sync Scheduling / Transport
   何时联网、Wi-Fi/充电策略、sleep/wake、retry

C. Business Merge
   两台设备并发改了同一业务对象时如何合并
```

这三个问题不能混成一个“同步模块”。

已完成初次账户配置的用户在离线时 SHOULD 仍能：

- 打开 LifeBook；
- 访问本地书库；
- 继续阅读；
- 查看已缓存内容；
- 创建本地笔记；
- 创建人生记录；
- 修改允许离线修改的数据。

用户确认的本地操作 SHOULD 先可靠落盘，再进入后续同步流程。

---

# 11. Local Data / `baga.data`

LifeBook 自己不实现数据库引擎。

结构化本地业务数据使用：

```text
LifeBook Domain
      │
      ▼
LifeBook Repository abstraction
      │
      ▼
     baga.data
```

例如：

```text
笔记
人生记录
时间胶囊草稿
阅读元数据
业务同步 journal
文章/问答缓存索引
```

大文件、图片、下载书籍仍可使用 `baga.storage`。

Baga Platform 可以在 Kindle / Android 内部直接用 SQLite 等成熟事务数据库实现 `baga.data`。LifeBook 不依赖 SQL、数据库路径或 SQLite-specific 行为。

---

# 12. Library / `baga.library`

LifeBook 的“书库产品逻辑”属于 LifeBook，但设备用户书库访问属于 Baga Platform。

正确关系：

```text
Device user library / imported documents
            │
            ▼
        baga.library
            │
            ▼
LifeBook Library Product Logic
```

LifeBook 使用：

```text
baga.library.list/get/open
```

并在授权后使用 import/remove 等写操作。

LifeBook 不扫描：

```text
Kindle /documents
Android vendor bookshelf path
Vendor database
```

Library Item 是 opaque Baga object；打开后交给 `baga.reader`。

书库与 Reader 都不是 EPUB-specific。

---

# 13. Sync 边界

Platform 负责：

```text
network state
sleep / wake
standard network request
sync task trigger
power / Wi-Fi policy
standard error semantics
```

LifeBook 负责：

```text
LifeBook data model
cloud protocol
object identity / idempotency
business merge semantics
version history
server-authoritative rules
retry semantics at business level
```

## 13.1 Automerge 的正确位置

LifeBook SHOULD 避免自行发明通用 CRDT。

对于真正有并发离线编辑价值的数据，SHOULD 优先评估成熟 Automerge 等 Local-first / CRDT 实现，例如：

```text
我的笔记
人生记录
时间胶囊草稿
文章草稿
```

但 Automerge 不应机械用于所有数据：

```text
阅读进度       → 简单业务 merge 即可
Feed           → Server authoritative + cache
评论           → Server authoritative + cache
其他用户笔记   → Server authoritative + cache
书籍文件       → content hash + file sync
```

LifeBook IKP 不需要知道当前 Platform/Server 是否使用 Automerge，也不依赖其私有 binary format，除非未来独立 Baga 同步标准明确版本化采用某种协议。

---

# 14. Capability 渐进增强

LifeBook 核心功能 MUST 面向 Base Profile 设计。

例如：

```lua
if baga.device.has("input.touch") then
    enable_touch_controls()
end

if baga.device.has("input.physical_page_key") then
    enable_page_key_hints()
end

if baga.device.has("display.fast_refresh") then
    use_fast_interaction_mode()
end

if baga.device.has("display.color") then
    enable_optional_color_assets()
end

if baga.device.has("reader.anchor") then
    enable_note_anchor_navigation()
end
```

LifeBook 不得用品牌或内部实现名推断能力。

---

# 15. Permission 基线

LifeBook Manifest MUST 只声明实际使用的权限。

可能包括：

```text
network
library.read
library.write
notes.read
notes.write
user_files.read
user_files.write
audio.output
bluetooth
frontlight.control
power.keep_awake
```

具体行为必须遵守 `05_权限模型_Baga-Ink-Permission-Model.md`。

Capability 不存在与 Permission 被拒绝是两种不同状态，LifeBook 必须分别处理。

`baga.data` 只访问自身 App Private Data 时不需要额外用户数据权限。

---

# 16. Kindle 与 Android E-Paper

## 16.1 Kindle

以下属于 Baga Ink Client / Platform / Kindle Adapter：

```text
installation / enablement route
Homebrew foundation
KUAL / MRPI / KPM / Hotfix integration
system integration
file paths
refresh mechanism
input mapping
power events
Reader implementation
local data backend
```

LifeBook App 不承担这些职责。

## 16.2 Android E-Paper

以下属于 Android Platform / Device Adapter：

```text
Generic Android
BOOX / iReader / Bigme / Hanvon specialization
Vendor APIs
Android version differences
Reader implementation
local data backend
```

Android 端可以用 APK 作为 Baga Ink Platform 的系统安装载体，但 LifeBook Universal App 仍是同一个 IKP。

---

# 17. 成熟开源组件复用原则

LifeBook 不以“自己写了多少底层代码”为目标。

如果 Baga Platform 已经有成熟组件可以实现标准能力，SHOULD 优先复用。

典型：

```text
Reader / Kindle device knowledge → KOReader / koreader-base
Framebuffer / diagnostics        → FBInk
Transactional local data         → SQLite or equivalent
Concurrent local-first merge     → Automerge where appropriate
Kindle Homebrew lifecycle        → mature KindleModding / NiLuJe ecosystem
```

但它们都属于：

> **Baga Ink Platform / Device implementation detail**

它们不会增加：

```text
KOReader Layer
SQLite Layer
Automerge Layer
Provider Layer
LifeBook Runtime
```

LifeBook 永远只面对 `baga.*`。

---

# 18. Reference App 驱动标准落地

LifeBook 遇到需求时分三类：

### A. LifeBook 私有业务

例如人生记录、时间胶囊、社区、LifeBook AI。

→ 留在 LifeBook Domain。

### B. 跨 App / 跨设备公共能力

→ 提出标准需求 → Capability / API / Permission → Platform / Adapter implementation → BICTS → LifeBook 使用。

实现阶段先寻找成熟开源轮子，不默认自己重写。

### C. 单一厂商独有能力

→ 先尝试抽象为标准 Capability；无法稳定标准化时只能进入受控 Enhanced / Capability Provider 路径，不能污染 Universal 核心。

---

# 19. 第一阶段实现优先级

## Phase A — Universal Skeleton

先验证同一个 `lifebook.ikp` 在 Kindle 与 Android E-Paper 上运行。

至少完成：

```text
App lifecycle
基础 E-Ink UI
Storage
Data
Network
Capability query
Permission
sleep / wake
offline start
```

## Phase B — Reading Core

```text
Library
Reader
reading position
Reader Anchor
Notes / Highlights
basic sync
```

测试文档不固定 EPUB，应选择当前 Reader implementation 真正支持的格式。

## Phase C — LifeBook Content

```text
Articles
Q&A
Comments
community notes
offline cache
```

## Phase D — Personal Life Features

```text
Life Records
Time Capsule
fuller cross-device sync
Automerge/CRDT evaluation for concurrent editable data
```

## Phase E — AI

在不破坏阅读、离线和低功耗原则前提下加入 AI。

---

# 20. Reference App 验收标准

一个 LifeBook Reference baseline SHOULD 满足：

1. 同一 Application ID；
2. 同一业务代码基线；
3. 同一 `lifebook.ikp` 在目标 Kindle 与 Android E-Paper 上加载；
4. 核心业务不判断 Vendor；
5. 只通过 `baga.*` 获取平台能力；
6. Optional Capability 缺失时合理降级；
7. 无网络时核心阅读和本地内容可工作；
8. 本地确认写入必须先经可靠事务持久化；
9. sleep / wake 后状态恢复；
10. 同步失败不破坏本地数据；
11. 更新失败不删除既有用户数据；
12. 不直接访问 Vendor SDK / Shell / raw framebuffer / Android Context；
13. Reader 不依赖未标准化 KOReader 私有 API；
14. Reader / Anchor 不以 EPUB 为唯一格式假设；
15. Library 不依赖设备真实文件路径；
16. 符合最小权限原则；
17. 通过对应 BICTS Reference App 场景测试。

最重要问题：

> **把同一个 LifeBook IKP 拿到另一台已经 Baga Ink Compatible 的设备上，是否无需为该品牌、Reader library 或数据库实现修改核心业务代码就能运行？**

---

# 21. 明确禁止的架构退化

LifeBook MUST NOT 演变为：

```text
LifeBook → BOOX SDK
LifeBook → iReader private API
LifeBook → Kindle shell
LifeBook → Android Context
LifeBook → raw framebuffer
LifeBook → KOReader private objects as permanent API
LifeBook → SQL / SQLite internals
LifeBook → Automerge internals as mandatory app contract
LifeBook → EPUB-only locator model
LifeBook → per-vendor business branches
LifeBook → bundled private Platform Core
LifeBook → bundled private Device Adapter
```

也不得把：

```text
LifeBook-for-BOOX.ikp
LifeBook-for-iReader.ikp
LifeBook-for-Kindle.ikp
```

作为 Universal App 的正常长期分发模型。

---

# 22. 最终架构

```text
Baga Ink Standards
│
├── App Standard
├── API
├── Capability Registry
├── Permission Model
├── IKP
├── Device Adapter Standard
├── Compatibility Standard
├── UI Standard
└── BICTS
        │
        ▼
LifeBook — Flagship Reference App
`lifebook.ikp`
        │
        ▼
Baga Ink Platform Core
        │
        ▼
Device Adapter
├── Kindle
└── Android E-Paper
```

一句话：

> **Baga Ink Standards 定义跨设备规则；Baga Ink Platform 实现这些规则并吸收设备差异、充分复用成熟开源能力；LifeBook 作为第一个完整旗舰 Reference App，只面向 Baga Ink API 开发。**

---

# 23. 本文件边界

本文件只规定 LifeBook 如何实现 Baga Ink 标准。

它：

- MUST NOT 修改 `docs/standards/` 的规范语义；
- MUST NOT 创造未经标准注册的 `baga.*` 公共 API；
- MUST NOT 把 LifeBook 私有需求升级为事实标准；
- MAY 随 LifeBook 产品演进，但必须继续服从 Baga Ink Standards。

发生冲突时：

> **以 `docs/standards/` 为准。**