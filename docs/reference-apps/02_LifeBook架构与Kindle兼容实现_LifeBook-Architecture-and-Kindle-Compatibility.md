# LifeBook IKP 架构与 Kindle 兼容实现 / LifeBook IKP Architecture and Kindle Compatibility

> **文档级别：Reference App 技术实现补充 / Reference App Technical Implementation Companion**  
> **状态：Baseline v0.3**  
> **日期：2026-08-23**  
> **适用对象：LifeBook (`lifebook.ikp`) on Baga Ink Platform**  
> **上位文档：`docs/standards/` 全部正式规范**  
> **配套文档：`01_LifeBook参考实现_LifeBook-Reference-App.md`**  
> **本文件不是 Baga Ink Standard，不得覆盖或修改上位标准。**

---

## 0. 目的

本文档总结 LifeBook 墨水屏版本当前确定的技术架构、开源组件选型、Kindle 硬件/固件/ABI 差异处理方式，以及离线优先、阅读、社区内容、其他用户笔记等功能如何落到 Baga Ink Platform。

本次 v0.2 的关键澄清是：

> **KOReader、SQLite、Automerge、FBInk、KPM、Hotfix 等是 Baga Ink 在 Kindle 上实现标准 API 时复用的成熟组件，不是 Baga Ink 新增的架构层。**

本文件严格遵守：

> **Reuse before reimplement. Standardize semantics, not internal implementation layering.**

---

# 1. 最终架构不变

此前讨论过：

```text
LifeBook App
  ↓
LifeBook Runtime
  ↓
KOReader
```

**不采用。**

也不采用：

```text
Baga API
  ↓
Provider Layer
  ↓
Engine Layer
  ↓
Device Adapter
```

仅因为内部用了某个开源库，不应人为增加一层。

正式架构仍然是 Baga Ink Standards 定义的四段关系：

```text
┌────────────────────────────────────────────┐
│          LifeBook — `lifebook.ikp`         │
│                                            │
│ Account / Library / Articles / Q&A         │
│ Comments / Public Notes / My Notes         │
│ Life Records / Time Capsule / AI           │
│ Offline Domain Logic / Sync Domain Logic   │
└───────────────────┬────────────────────────┘
                    │ only baga.*
                    ▼
┌────────────────────────────────────────────┐
│             Baga Ink API                   │
│                                            │
│ app / ui / display / input / device        │
│ storage / data / library / network         │
│ power / reader / sync / permissions / log  │
└───────────────────┬────────────────────────┘
                    ▼
┌────────────────────────────────────────────┐
│          Baga Ink Platform Core            │
└───────────────────┬────────────────────────┘
                    ▼
┌────────────────────────────────────────────┐
│          Baga Ink Kindle Adapter           │
└───────────────────┬────────────────────────┘
                    ▼
                Kindle OS
```

**这张图是架构。**

KOReader、koreader-base、FBInk、SQLite、Automerge、KPM、Hotfix、KUAL、MRPI 等属于上图内部具体实现和设备基础设施，不在这里再画成一层。

---

# 2. LifeBook IKP 自己负责什么

`lifebook.ikp` 只负责产品业务与跨设备逻辑。

```text
LifeBook
├── Account / Session
├── Library Product Logic
├── Articles
├── Q&A
├── Comments
├── Public / Community Notes
├── My Notes / Highlights
├── Life Records
├── Time Capsule
├── AI
├── Offline Product Logic
└── Sync Domain Logic
```

LifeBook 不负责：

```text
Kindle framebuffer
Kindle touch/keycode
Kindle sleep/wake bridge
Kindle system path
EPUB/PDF/MOBI parser
数据库引擎
通用 CRDT 算法
Kindle Homebrew 生命周期
具体越狱/Enablement Route
```

推荐 IKP 目录：

```text
lifebook.ikp
├── manifest.json
├── main.lua
├── src/
│   ├── application/
│   ├── domain/
│   ├── views/
│   ├── persistence/
│   ├── reader/
│   └── sync/
├── assets/
├── locales/
└── signature/
```

Universal IKP MUST NOT 打入 Kindle native bridge、KOReader binary、SQLite native binary、Automerge native runtime、Device Adapter 或 Platform Core。

---

# 3. “充分复用成熟轮子”的正确理解

Baga Ink 统一的是开发者 API，而不是要求底层全部自研。

Kindle 实现可以直接这样工作：

```text
baga.reader
→ 内部复用 KOReader / koreader-base / CREngine / MuPDF

baga.ui / display / input
→ 内部复用 KOReader UIManager / widgets / Kindle device knowledge / FBInk

baga.data
→ 内部使用 SQLite 或其他经过验证的事务数据库

需要并发离线合并的具体业务
→ 内部评估 Automerge 等成熟 Local-first / CRDT 实现

Kindle Platform / Homebrew 生命周期
→ 内部复用 KPM / Hotfix / MRPI / KUAL 等成熟基础
```

这并不意味着存在：

```text
KOReader Layer
SQLite Layer
Automerge Layer
Homebrew Layer
Provider Layer
```

开发者永远只面对：

```text
baga.*
```

---

# 4. LifeBook 不只是 Reader

LifeBook 的内容类型至少包括：

```text
Books / Documents
Articles
Q&A
Comments
Other users' notes
My notes / highlights
Life Records
Time Capsule
AI
Profiles / community content
```

所以：

```text
文章 / 问答 / 评论 / 人生记录 / AI
→ LifeBook Domain + baga.ui

书籍 / 文档阅读
→ baga.reader
```

文章、问答、评论不需要转 EPUB，更不需要先进入 KOReader ReaderUI。

---

# 5. E-Ink UI 实现

LifeBook IKP 只使用：

```text
baga.ui
baga.input
baga.display
```

Kindle 第一实现内部可以大量复用 KOReader 的 Lua UI / widget / UIManager。

正确理解：

```text
LifeBook 调 baga.ui
        ↓
Baga Ink Kindle implementation
        ↓
内部可以直接调用/组合 KOReader UI 代码
```

而不是把“KOReader UI”提升成开发者必须理解的中间层。

UI 产品原则：

- 高对比；
- page-first；
- 长列表虚拟化；
- Touch + Focus；
- 物理翻页键映射语义动作；
- 少动画；
- dirty region；
- ghosting / waveform 归 Platform / Adapter；
- Color / Pen / Fast Refresh 均为渐进增强。

---

# 6. Reader：正式采用 KOReader，但不泄漏 KOReader API

Kindle 上第一 Reader 实现正式优先采用：

> **KOReader / koreader-base**

LifeBook 只调用：

```lua
baga.reader.supports(source)
baga.reader.open(source)
```

以及 Reader Session 的标准能力。

Kindle 内部可以直接复用：

```text
ReaderUI
CREngine
MuPDF
ReaderHighlight
ReaderAnnotation
ReaderBookmark
Reader position / search / selection
```

LifeBook 不依赖：

```text
ReaderUI private object
KOReader plugin object
KOReader internal path
KOReader sidecar schema
CREngine object
MuPDF object
```

---

# 7. LifeBook / Baga Reader 绝不以 EPUB 为中心

LifeBook 的 Reader 抽象不是：

> “EPUB Reader + 其他格式兼容”

而是：

> **当前 Baga Reader implementation 能稳定支持什么文档，LifeBook 就通过统一 API 使用什么文档。**

KOReader 本身已经支持多种 reflowable 与 fixed-page 文档类型，因此应充分利用其成熟能力。

典型可支持范围可能包括：

```text
EPUB
PDF
MOBI / AZW family（按实际实现）
FB2
TXT / HTML
DjVu
CBZ / comic
其他 Reader implementation 已支持格式
```

格式清单属于 implementation capability，不应把 LifeBook 产品定义冻结成 EPUB。

---

# 8. Reader Anchor：不重新发明格式定位算法

这是“其他用户笔记”功能的关键。

## 8.1 KOReader 已经做了什么

KOReader 已有成熟的阅读位置、Bookmark、Highlight 与 Annotation 体系。

其内部并没有假装所有格式共用一种 Locator，而是根据 Reader 模型使用适合的机制：

```text
rolling / reflowable
→ XPointer-like start/end position 等

paging / fixed-page
→ page number + page-local position / boxes 等
```

这正说明 Baga Ink 不应该自己分别重写：

```text
EPUB locator
PDF locator
MOBI locator
FB2 locator
TXT locator
DjVu locator
CBZ locator
```

## 8.2 Baga Reader Anchor

LifeBook 只做：

```lua
local anchor = session:create_anchor(selection)

save_note({
    anchor = anchor,
    ...
})
```

恢复时：

```lua
session:goto_anchor(anchor)
```

Anchor 对 LifeBook 是 opaque 的 Baga 值。

LifeBook：

- 保存它；
- 同步它；
- 关联公开/个人笔记；
- 把它交还 Reader；
- 不解析其内部 XPointer / pboxes / locator。

Kindle Baga implementation 优先用 KOReader 已有定位实现。

## 8.3 跨 Reader / 跨设备恢复

精确原生位置无法直接跨实现解析时，可以由 `baga.reader.resolve_anchor()` 利用标准 fallback evidence 尝试恢复。

可能参考：

```text
quote/context
page/region
progression
other stable evidence
```

但 approximate 必须明确为 approximate。

Readium Locator、EPUB CFI、W3C Web Annotation 可以提供设计启发，但**只作参考**，不成为 LifeBook/Baga Reader 的默认格式边界。

---

# 9. 具体采纳的开源组件地图

下面的“实现位置”不是新架构层，而是说明某个库在哪里被 Baga Ink Kindle 实现利用。

| 项目 | License | 实现位置 / 用途 | 决策 |
|---|---|---|---|
| KOReader | AGPL-3.0 | `baga.reader`、Kindle Reader/UI/device/input 的主要成熟实现来源 | **正式优先采纳** |
| koreader-base | AGPL-3.0 | LuaJIT、文档引擎、Kindle target、native foundation | **正式优先采纳** |
| MuPDF / CREngine（经 KOReader） | 按各项目许可证 | PDF/fixed-page 与 reflowable 文档能力 | **随 KOReader 复用** |
| FBInk | GPL-3.0-or-later | framebuffer / bootstrap / diagnostics / refresh fallback | **正式复用** |
| SQLite | Public Domain | `baga.data` 的首选 Kindle/Android 事务本地存储候选 | **正式优先评估/采用** |
| Automerge | MIT | 真正存在多设备并发离线编辑的数据 CRDT/Local-first 候选 | **选择性正式评估，禁止全数据滥用** |
| KPM | GPL-3.0 | Kindle Platform/Homebrew 组件安装/启动/卸载 | **内部复用；不是 IKP 包格式** |
| Universal Hotfix | GPL-3.0 | Kindle Homebrew 基础、armel/armhf 环境等 | **优先复用** |
| KindleTool | GPL-3.0+ | Kindle package/device/build tooling | **开发/部署工具** |
| koxtoolchain | 按仓库许可证 | armel / armhf cross-build | **需要 native component 时复用** |
| KUAL | 需按实际版本审查 | legacy launcher / maintenance fallback | **仅 fallback，用户日常不可见** |
| MRPI | 按实际组件许可证 | legacy package/install bridge | **兼容旧生态** |
| sh_integration | 发布前完成许可证审计 | Kindle Home/Library app entry 研究 | **重点研究** |

## 9.1 不作为当前主实现

| 项目 | 原因 |
|---|---|
| Mesquito | 固件范围/Web Runtime/维护状态限制，不适合作为 Universal UI 基础 |
| KWebBrew | 旧 Web 环境限制 |
| PEKI | NonCommercial 许可证风险，不作为商业默认组件 |
| slint-kindle-backend | 方向优秀但 Kindle 覆盖仍不足，可继续 R&D |
| KindleForge 等 | 架构/ABI/Market 设计参考，不作为基础依赖 |

---

# 10. 许可证原则

`lifebook.ikp` 本身不直接携带 Kindle native 开源组件。

许可证责任主要发生在具体 Baga Ink Platform / Kindle implementation 的组合与分发方式上。

发布前必须：

- 锁定实际 tag/commit；
- 记录 dependency manifest；
- 满足 AGPL/GPL/MIT 等要求；
- 对组合/修改/进程边界做正式许可证审查；
- 不使用不适合商业分发的组件作为默认依赖。

---

# 11. Kindle 硬件与 ABI

LifeBook 不按每一款 Kindle 打一个 IKP。

关键工程边界由 Kindle Platform / Adapter 处理。

KOReader 已有 target 是重要实现参考：

| 平台族 | KOReader target | 典型工程含义 |
|---|---|---|
| Legacy | `kindle-legacy` | Kindle 2 / 3 / DXG 时代；低资源/按键/旧 ABI |
| Classic | `kindle` | K4 / Touch / PW1 等较老环境 |
| PW2+ soft-float | `kindlepw2` | PW2+ soft-float 优化路径 |
| Hard-float | `kindlehf` | Firmware `>= 5.16.3` 的 hard-float 设备族 |

核心：

> **5.16.3 是重要 soft-float / hard-float 工程边界。**

变化发生在：

```text
Platform binary
Kindle Adapter implementation
KOReader build
FBInk/native bridge
Homebrew foundation
```

不发生在：

```text
lifebook.ikp
```

---

# 12. Kindle 硬件能力渐进增强

LifeBook 不按型号判断，而按 Capability。

| 硬件差异 | Baga Capability / 行为 |
|---|---|
| Touch | `input.touch`；点击、选择、软键盘增强 |
| 物理翻页键 | `input.physical_page_key` → page_next/page_previous |
| 非触摸旧机 | `input.navigation` + Focus 完成基础操作 |
| Scribe Pen | `input.pen*` 通过测试后渐进启用 |
| Colorsoft | `display.color` 通过测试后增强；黑白仍完整 |
| Fast Refresh | `display.fast_refresh` 可增强交互 |
| Warm light | `light.frontlight.temperature` |
| Audio | `audio.output` |
| Bluetooth | `bluetooth.*` |

同系列其他机型具备某硬件，不等于当前设备 automatically has capability。

---

# 13. 固件 / OS / 系统差异

兼容性对象必须是：

```text
Device Model
+ Firmware Range
+ Baga Platform Version
+ Kindle Adapter Version
+ BICTS Version
```

同一型号可以：

```text
Firmware A → Compatible
Firmware B → Experimental
Firmware C → Unsupported
```

LifeBook App 内禁止：

```lua
if firmware >= "5.16.4" then ... end
```

需要吸收的差异包括：

```text
soft-float ↔ hard-float
USB Mass Storage ↔ MTP
framebuffer / waveform
Touch controller
physical key
frontlight / warm light
sleep/wake event
system service / LIPC behavior
Home UI / launcher integration
```

归：

```text
Kindle Adapter
Compatibility Database
Quirk Database
Installation Route Database
```

---

# 14. WinterBreak / SpringBreak / Sanctuary / Véra

它们是 Kindle **Enablement / Installation Routes**。

不是：

```text
LifeBook library
Baga Ink API
App architecture layer
```

关系：

```text
WinterBreak / SpringBreak / Sanctuary / Véra / future routes
                 ↓
让具体设备获得可用 Homebrew/Baga installation condition
                 ↓
Baga Ink Platform on Kindle
                 ↓
lifebook.ikp
```

具体型号/固件支持随社区变化，必须由可更新 Installation Route Database 维护，不由 LifeBook 或稳定 API 冻结。

普通用户只应看到：

```text
Compatible
Experimental
Unsupported
```

---

# 15. Offline-first：必须区分三层问题

## 15.1 Local Data

用户操作先落盘：

```text
User Action
   ↓
baga.data transaction
   ↓
commit success
   ↓
UI confirm
```

这叫本地可靠数据，不叫同步。

## 15.2 Sync Scheduling / Transport

```text
baga.network
baga.sync
sleep/wake
wifi_only
when_online
when_charging
retry / cancel
```

负责“什么时候同步”。

## 15.3 Business Merge

LifeBook 负责“同步后数据如何解释”：

```text
object identity
idempotency
version history
business merge
server-authoritative policy
conflict policy
```

这三个概念不得混在一起。

---

# 16. `baga.data`：不自己造数据库

Baga API v0.3 已正式补充事务型 `baga.data`。

LifeBook 使用 Repository abstraction：

```text
LifeBook Domain
      ↓
LifeBook Repository
      ↓
baga.data
```

Kindle/Android 实现内部优先复用 SQLite 或同等级成熟事务数据库。

LifeBook 不知道：

```text
SQL
SQLite DB path
WAL
pragma
Android Room
```

大文件/图片/下载书籍仍使用 `baga.storage`。

---

# 17. Automerge：优先复用，但只用于真正需要 CRDT 的数据

不应自己发明通用 CRDT。

**优先评估 Automerge** 的对象：

```text
My Notes
Life Records
Time Capsule drafts
Article drafts
其他真正可能在多个离线设备同时修改的可编辑对象
```

通常不需要 Automerge：

```text
Reading Position
→ 简单业务 merge

Feed / Comments / Public Notes
→ Server authoritative + local cache

Book Files
→ content hash + file transfer
```

Automerge 是实现选择，而不是一层，也不是 `baga.sync` 的同义词。

如果未来 Baga 要让不同实现直接交换 Automerge wire format，必须通过独立标准锁定协议版本；不能把“最新版 Automerge”当规范。

老 Kindle 的 CPU/RAM/ABI 必须实测；如果 Automerge binary 对某设备族过重，应允许该功能降级或采用等价内部实现，而不能牺牲 Baga 基础兼容性。

---

# 18. `baga.library`：正式解决书库边界

Baga API v0.3 已正式补充：

```text
baga.library
```

它与现有：

```text
storage.user_library Capability
library.read / library.write Permission
```

形成闭环。

LifeBook：

```text
baga.library.list/get/open
→ 获得 opaque Library Item / source
→ baga.reader.open(source)
```

不再扫描 Kindle `/documents`。

不再让 App 理解 Android vendor bookshelf。

不限定 EPUB。

---

# 19. 文章 / 问答 / 评论 / 社区内容

这些不是 Book Reader 文件。

```text
LifeBook Server / Local Cache
           ↓
     LifeBook Domain
           ↓
        baga.ui
```

离线时显示本地 cache；联网后按业务规则更新。

其他用户的文章、问答、评论、用户主页均属于 LifeBook Domain，不需要 KOReader。

---

# 20. 其他用户笔记

这是 LifeBook 的重要差异化功能。

```text
Book/document content → baga.reader
Public note data      → LifeBook Domain/API
```

关联通过：

```text
Baga Reader Anchor
```

LifeBook Server 可以保存：

```text
publication/document identity
anchor
note body
user / visibility / metadata
```

LifeBook 不把 KOReader private annotation schema 固化成云协议。

在 Kindle 端，Anchor 解析优先利用 KOReader 已有定位能力；在 Android / future Reader 上由对应 Baga implementation 解析。

---

# 21. 首页启动体验

产品目标：

```text
Kindle Home
    ↓ one action
LifeBook
```

用户心理模型：

> “我的 Kindle 安装了 LifeBook App。”

而不是：

```text
KUAL → KOReader → Plugin → LifeBook
```

KUAL/MRPI/KOReader/KPM/Hotfix 对普通用户全部隐身。

具体 Home/App registration 归 Kindle Platform / Adapter implementation。

---

# 22. 更新与回滚

LifeBook 更新完全使用 Baga IKP 标准：

```text
Signed lifebook.ikp
        ↓
Verify identity/signature
        ↓
Stage
        ↓
Health check
   ┌────┴────┐
 success   failure
   │           │
 activate    rollback
```

KPM 等 Kindle package manager 只负责 Kindle Platform/Homebrew 组件，不代替 IKP identity/signature/update protocol。

用户数据与 App package 必须分离。

---

# 23. Manifest Capability 建议

LifeBook Base 应尽量只 Required 必需能力。

Required baseline：

```text
display.basic
input.navigation
storage.app_sandbox
power.sleep_wake
platform.lifecycle
```

Reading 版本可 Required：

```text
reader.open
```

其他尽量 Optional：

```text
reader.anchor
input.touch
input.physical_page_key
display.partial_refresh
display.fast_refresh
display.grayscale
display.color
network.wifi
network.https
storage.user_library
light.frontlight
light.frontlight.temperature
input.pen
audio.output
bluetooth.available
```

“当前 online”不是 capability，也不能成为离线启动的前置条件。

---

# 24. Permission 建议

按功能渐进声明：

```text
network
library.read
notes.read
notes.write
```

写书库/用户文件/设备控制时再加入：

```text
library.write
user_files.read
user_files.write
audio.output
bluetooth
frontlight.control
power.keep_awake
```

`baga.data` 访问 App 自身沙箱数据不需要额外用户资料权限。

---

# 25. 低端 Kindle 降级策略

| 条件 | LifeBook 行为 |
|---|---|
| 低 RAM / 老 CPU | 缩小缓存、图片与并发任务；避免重型同步在前台运行 |
| 无 Touch | Focus + physical navigation |
| 无 Fast Refresh | TEXT/QUALITY 降级，不影响业务 |
| 无 Color | 黑白/灰阶完整使用 |
| 无 Pen | 不显示手写增强 |
| 无 Audio | 隐藏 audio/TTS |
| 无 Bluetooth | 隐藏蓝牙增强 |
| Wi-Fi off | 完整离线启动；同步暂停 |
| Automerge/CRDT 不适合该硬件 | 不影响 Base App；并发编辑功能按产品策略降级 |

核心：

> **能力少意味着渐进降级，不意味着另一份 LifeBook。**

---

# 26. 当前冻结技术决策

1. **LifeBook 正式应用包只有 `lifebook.ikp`。**
2. **没有 LifeBook Runtime。**
3. **LifeBook 不直接适配 Kindle。**
4. **LifeBook 只调用 `baga.*`。**
5. **内部采用成熟库不新增公共架构层。**
6. **Kindle Reader 第一选择 KOReader / koreader-base。**
7. **Kindle UI/display/input 第一实现可大量复用 KOReader / FBInk。**
8. **Reader 不是 EPUB-centric；支持范围来自当前 Reader implementation。**
9. **Reader Anchor 复用 Reader 已有原生定位，不为每种格式重造 Locator。**
10. **`baga.data` 是结构化事务本地存储；内部首选 SQLite 等成熟实现。**
11. **`baga.library` 是标准用户书库边界；App 不扫描真实设备路径。**
12. **`baga.sync` 是调度/策略，不等于 CRDT。**
13. **真正并发离线编辑优先评估 Automerge，而不是自研 CRDT。**
14. **Automerge 不滥用于 Feed、评论、公开笔记 cache、书籍文件、简单阅读进度。**
15. **KPM/Hotfix/MRPI/KUAL 是 Kindle Platform/Homebrew 内部工具，不是 IKP App contract。**
16. **WinterBreak / SpringBreak / Sanctuary / Véra 只属于 Installation Route。**
17. **5.16.3 是重要 soft-float/hard-float 工程边界；IKP 不随 ABI 分叉。**
18. **所有 model/firmware quirks 留在 Adapter / Compatibility DB。**
19. **LifeBook 必须 Offline-first。**
20. **文章/Q&A/评论由 LifeBook + `baga.ui` 渲染。**
21. **Public Notes 用 Baga Reader Anchor 与正文关联。**
22. **Kindle Home 一次点击进入 LifeBook，底层工具隐身。**
23. **更新使用 Baga IKP signing/staging/rollback。**

---

# 27. 本轮 Standards 缺口已经如何解决

此前记录的三个缺口已在 2026-08-23 的 Standards 增强中正式处理：

## 27.1 Transactional Offline Data

原问题：只有 `baga.storage`，缺少结构化事务本地数据。

现结论：

```text
新增 baga.data
```

标准化事务语义，不标准化 SQLite。

内部优先复用 SQLite 等成熟数据库。

## 27.2 Cross-reader Content Anchor

原问题：LifeBook Public Notes 需要跨设备稳定定位正文，但不能固化 KOReader private schema，也不能变成 EPUB-only。

现结论：

```text
reader.anchor Capability
+
baga.reader create_anchor / goto_anchor / resolve_anchor
```

标准化 Reader Anchor 行为，真实定位算法交给 Reader implementation；Kindle 优先复用 KOReader 已有 rolling/paging 位置机制。

## 27.3 Library API

原问题：已有 `storage.user_library` 与 `library.read/write`，但缺少公开 namespace。

现结论：

```text
新增 baga.library
```

统一 list/get/open/import/remove 等书库边界，App 不接触 Kindle/Android 真实路径。

---

# 28. 后续仍需实测，而不是继续造抽象

下一阶段应把精力放在真实验证，而不是继续增加层：

```text
KOReader → baga.reader mapping prototype
KOReader UI → baga.ui mapping prototype
SQLite → baga.data transaction/crash tests
Kindle / Android baga.library bridge prototype
Reader Anchor rolling + paging round-trip
Automerge 在 armel/armhf Kindle 的 binary size / RAM / CPU / merge 性能
Home screen direct LifeBook launch
BICTS regression across representative Kindle families
```

如果某成熟轮子在特定老 Kindle 不适合，应先换实现或降级 capability，而不是改变 LifeBook IKP 架构。

---

# 29. 最终一句话

> **LifeBook 是一个标准 `lifebook.ikp`；开发者只面对 Baga Ink API；Baga Ink 在 Kindle 上则最大程度直接、组合或拆分复用 KOReader、koreader-base、FBInk、SQLite、Automerge 以及成熟 Homebrew 生态来实现这些 API。标准统一语义，不强迫内部自研，也不因为使用一个优秀开源库就生造一个新的架构层。**

---

# 30. 外部实现参考

- KOReader: https://github.com/koreader/koreader
- KOReader Base: https://github.com/koreader/koreader-base
- FBInk: https://github.com/NiLuJe/FBInk
- SQLite: https://sqlite.org/
- Automerge: https://github.com/automerge/automerge
- Automerge Docs: https://automerge.org/
- KindleTool: https://github.com/NiLuJe/KindleTool
- KOReader Toolchain: https://github.com/koreader/koxtoolchain
- KindleModding KPM: https://github.com/KindleModding/KPM
- KindleModding Universal Hotfix: https://github.com/KindleModding/Hotfix
- KindleModding SH Integration: https://github.com/KindleModding/sh_integration
- KindleModding documentation: https://kindlemodding.org/
- Readium Locator（仅设计参考，不作为 Baga Reader 格式边界）: https://readium.org/architecture/models/locators/
- W3C Web Annotation（仅设计参考）: https://www.w3.org/TR/annotation-model/

外部项目的支持范围、许可证与 API 会变化；实际发布版本必须锁定 tag/commit，并由 Baga Ink Platform dependency manifest 记录。

---

# 31. Kindle Reference Implementation Mapping / Kindle 参考实现映射

本节把前文已经分散说明的 Kindle 复用关系收敛成一张明确的实现映射图，供 LifeBook、Baga Ink Platform 实现者和后续 AI 直接使用。

> **本图不是 LifeBook/Baga Ink 的新架构层，而是 `baga.*` 在 Kindle 上的参考实现映射。**  
> **KOReader、Automerge、SQLite 是 Baga Ink API 在 Kindle 上的具体实现所复用的开源组件。**

```text
Baga Ink on Kindle
│
├─ baga.reader
│   └─ 主要复用 KOReader
│       ├─ CREngine
│       ├─ MuPDF
│       ├─ ReaderUI
│       ├─ annotation / bookmark / highlight
│       └─ position / search / selection / anchor
│
├─ baga.ui
│   └─ 可复用 KOReader Lua UI / widget / UIManager
│
├─ baga.display
│   └─ KOReader Kindle device/display knowledge + FBInk
│
├─ baga.input
│   └─ KOReader Kindle input / key / touch handling
│
├─ baga.data
│   └─ SQLite 或同等级成熟事务存储
│
├─ baga.sync
│   ├─ Baga 标准语义：联网 / Wi-Fi / sleep-wake / trigger / retry policy
│   └─ 真正需要并发离线合并的业务场景：可复用 Automerge
│
├─ baga.network
│   └─ 复用成熟 HTTP / TLS / KOReader 已验证网络能力与 Kindle 网络桥接
│
└─ baga.power
    └─ Kindle 系统能力 / KOReader 已有 lifecycle / power 相关实现
```

对 LifeBook 的含义：

- LifeBook 只调用 `baga.*`；
- LifeBook 不 `require()` KOReader 私有模块，不执行 SQL，不直接调用 Automerge runtime；
- Kindle 平台实现者应先检查 KOReader/SQLite/Automerge/FBInk/Homebrew 生态是否已经有可靠实现，再决定是否编写新代码；
- 某个内部库被替换时，只要 `baga.*` 语义保持一致，`lifebook.ikp` 不应修改；
- 某个旧 Kindle 无法承载某内部实现时，应优先替换实现或降级对应能力，而不是为该型号维护另一份 LifeBook。

这张映射图必须和顶层架构分开理解：

```text
架构：
LifeBook IKP → Baga Ink API → Platform Core → Kindle Adapter → Kindle OS

实现映射：
某个 baga.* 在 Kindle 内部优先复用哪个成熟轮子
```

两者不能混为一谈。