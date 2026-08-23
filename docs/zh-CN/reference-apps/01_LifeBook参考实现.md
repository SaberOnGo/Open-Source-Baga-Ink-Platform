# LifeBook 墨水屏参考应用实现规范 / LifeBook Ink Reference App Implementation Specification

> **文档级别：参考应用实现规范 / Reference App Implementation Specification**  
> **状态：Baseline v0.6**  
> **日期：2026-08-23**  
> **适用对象：LifeBook on Baga Ink Platform**  
> **Kindle 具体实现冻结：`03_Kindle具体实现架构冻结_Baga-Ink-Kindle-Implementation-Architecture-Freeze.md`**  
> **本文件不是 Baga Ink Standard，不得覆盖或修改上位标准。**

---

## 0. 文档目的

本文档规定 LifeBook 作为 Baga Ink Platform 旗舰 Reference App 的实现边界、模块划分、跨设备原则、UI / Reader / SQLite / Local-first 同步策略。

核心目标：

> **用真实 LifeBook 证明：同一份 IKP 可以跨 Kindle 与 Android E-Paper，同时充分复用 KOReader、SQLite、Automerge 等成熟轮子，而不增加多余架构层。**

正式正文只描述当前有效设计。

对于 Kindle 的 bootstrap、Homebrew foundation、KPM / MRPI、`.kpkg` / `.ikp`、KOReader pinned integration、Home Entry、Installation Route 与 ABI build 等具体实现，本文不另建第二套定义，统一服从 `03_Kindle具体实现架构冻结_Baga-Ink-Kindle-Implementation-Architecture-Freeze.md`。

---

# 1. 上位规范

LifeBook MUST 遵守：

```text
00 Standards Index
01 Platform Strategy
02 App Standard
03 API
04 Capability Registry
05 Permission Model
06 IKP Package
07 Device Adapter
08 Compatibility
09 UI
10 BICTS
11 Kindle Adapter
12 Android E-Paper Adapter
13 Standard Libraries and Adopted Components
20–28 Distribution / Signing / Update
```

优先级：

```text
Baga Ink Standards
  > Kindle Implementation Architecture Freeze（Kindle 实现任务）
  > LifeBook Reference
  > LifeBook implementation
```

---

# 2. LifeBook 定位

LifeBook 是：

> **Baga Ink Platform 上的旗舰 Universal App / Reference App。**

LifeBook 业务保持在 IKP 内；Platform、Device Adapter、Reader backend、数据库引擎和通用 CRDT 基础不由 LifeBook 重新实现。

---

# 3. 总体架构

```text
LifeBook — lifebook.ikp
        │
        ├─ Baga Ink API        → 设备 / OS / Platform 能力
        └─ Baga Lua Profile    → 成熟 Standard Libraries
                │
                ▼
        Baga Ink Platform Core
                │
                ▼
          Device Adapter
        ┌───────┴────────┐
        ▼                ▼
     Kindle        Android E-Paper
```

LifeBook 不直接判断当前是 Kindle / BOOX / iReader。

---

# 4. LifeBook 业务模块

```text
LifeBook
├─ Account / Session
├─ Library Product Logic
├─ Articles
├─ Q&A / Comments
├─ Public / Community Notes
├─ My Notes / Highlights
├─ Life Records
├─ Time Capsule
├─ AI
├─ Offline Cache Policy
└─ Sync Domain Logic
```

这些属于 LifeBook 产品业务。

---

# 5. LifeBook 使用的平台能力与成熟库

```text
UI                     → baga.ui / input / display
Reader                 → baga.reader
User Library           → baga.library
Files / downloads      → baga.storage
Network                → baga.network
Sync scheduling        → baga.sync
Power / lifecycle      → baga.power / baga.app
Permissions            → baga.permissions
Logging                → baga.log
Relational local DB    → require("lsqlite3")
Concurrent local-first → Automerge core（适用对象）
```

SQLite 本身是 LifeBook 的关系数据库基础。

---

# 6. SQLite

LifeBook 使用 Baga Lua Profile 标准库：

```lua
local sqlite3 = require("lsqlite3")
local path = baga.storage.resolve_path("appdata/lifebook.sqlite3")
local db = sqlite3.open(path)
```

LifeBook 自己维护：

```text
schema
migration
SQL queries
indexes
FTS
business constraints
```

## 6.1 适合 SQLite 的 LifeBook 数据

```text
library metadata
account/session metadata
reading progress
cached articles
cached Q&A / comments
public-note cache
sync metadata
local indexes
full-text search index
Automerge document/change metadata or BLOB
```

## 6.2 大文件

书籍、图片、大型附件仍通过 `baga.storage` 管理；SQLite 保存 metadata / index / relationship。

---

# 7. Automerge

对真正存在多个设备同时离线编辑的对象，优先采用 Automerge core。

候选：

```text
My Notes
Life Records
Time Capsule drafts
Article drafts
其他真实并发可编辑对象
```

通常不需要 Automerge：

```text
Reading Position
→ 简单业务 merge

Feed / Comments / Public Notes
→ Server authoritative + SQLite cache

Book Files
→ content hash + file transfer
```

## 7.1 可整体采用，也可拆模块采用

LifeBook / Platform 可以：

```text
完整使用 Automerge core
只使用 document / merge / history
只使用 binary persistence
只使用 sync protocol
通过 automerge-c / Rust bridge
只使用 patches / cursors
```

不要求使用完整 `automerge-repo`。

## 7.2 SQLite + Automerge

```text
SQLite
├─ 普通关系数据
├─ cache / index / FTS
└─ Automerge document/change BLOB metadata

Automerge
└─ 真正并发 Local-first object
```

SQLite 与 Automerge 互补。

---

# 8. Sync 边界

```text
SQLite
→ 本地持久化 / 查询 / transaction

Automerge（适用时）
→ CRDT merge / history / optional sync protocol

baga.sync
→ when_online / wifi_only / charging / sleep-wake / trigger / retry

LifeBook Domain
→ authoritative policy / object identity / business conflict policy
```

用户本地操作必须优先可靠落盘，再等待网络。

---

# 9. Reader

LifeBook 书籍 / 文档阅读使用 `baga.reader`。

Kindle 第一实现优先复用 KOReader；Android 可以使用自己的成熟实现。

LifeBook 不依赖 KOReader private Lua object / sidecar schema。

Reader 不以 EPUB 为中心。

---

# 10. Reader Anchor / Public Notes

```text
book/document content → baga.reader
public note body       → LifeBook Domain / Server
```

二者通过 Baga Reader Anchor 关联。

LifeBook 保存、同步 Anchor，并把 Anchor 交回 Reader；不解析 XPointer / PDF boxes / EPUB CFI / Readium Locator。

Kindle 优先复用 KOReader rolling/paging 已有定位。Readium/W3C 仅作参考。

---

# 11. `baga.library`

用户书库访问：

```text
baga.library.list/get/open/import/remove
```

LifeBook 不扫描 Kindle `/documents`，也不理解 Android Vendor bookshelf database。

Library Item 使用 opaque ID / source handle，并可交给 `baga.reader`。

---

# 12. LifeBook UI

文章、问答、评论、人生记录、时间胶囊、AI：

```text
LifeBook Domain
   ↓
baga.ui
```

它们不需要转换成 EPUB，也不经过 ReaderUI。

UI 原则：高对比、page-first、Touch + Focus、物理翻页键语义动作、少动画、少全刷、Color/Pen/Fast Refresh 渐进增强。

---

# 13. Kindle 内部成熟组件复用

Kindle 的具体模块采用与安装角色以 `03_Kindle具体实现架构冻结...` 为权威。

LifeBook 层只需要知道：

```text
baga.reader
→ Kindle Platform 内部 pinned KOReader / ReaderUI / CREngine / MuPDF / Annotation

baga.ui/display/input
→ Kindle Platform 内部 KOReader UIManager / widgets / Kindle device knowledge / FBInk

Baga Lua Profile lsqlite3
→ Platform-managed libsqlite3

KOReader internals
→ lua-ljsqlite3
→ 可与 lsqlite3 共享经过验证的 Platform libsqlite3

Automerge core
→ 真正 Local-first 对象，整用/拆用；不是所有数据的默认引擎
```

Kindle Homebrew / 安装模块的冻结定位为：

```text
KPM
→ KPM-compatible target 上的 Baga Platform native install/update manager
→ 不管理 lifebook.ikp

Hotfix / sh_integration
→ Homebrew foundation / visible launcher integration

MRPI / KindleTool
→ KPM-incompatible/legacy Platform install、bootstrap 或 build/package tooling

KUAL / PEKI
→ legacy/admin/bootstrap fallback only
→ LifeBook 正常路径不依赖

WinterBreak / SpringBreak / Sanctuary / Véra
→ Baga Ink Client Installation Route DB records only

Mesquito
→ 不作为 Baga 直接采用模块；若 route 内部使用，只是 upstream implementation detail
```

这些都是 Kindle Platform / Client 实现细节，不是 LifeBook App Contract，也不形成新的 `Runtime` 层。

---

# 14. Android 内部成熟组件复用

```text
lsqlite3
→ Baga Platform 锁定 SQLite runtime
→ 不依赖 OEM 系统 SQLite 版本差异

Reader
→ Android/native mature implementation

Automerge
→ 可使用 Rust/C/Java/JS 等成熟 binding/bridge
```

这里的 `SQLite runtime` 仅指 SQLite library implementation，不是 `Baga Platform Runtime` 架构层。

LifeBook IKP 不随平台分叉。

---

# 15. Permission 基线

按功能渐进声明：

```text
network
library.read
notes.read
notes.write
```

需要时再加入：

```text
library.write
user_files.read
user_files.write
audio.output
bluetooth
frontlight.control
power.keep_awake
```

LifeBook 自己的 SQLite database 位于 App sandbox，不需要额外用户资料权限。

---

# 16. Offline-first

已完成初次账户配置后，离线应仍可：

- 打开 LifeBook；
- 浏览本地书库；
- 阅读；
- 查看缓存文章/Q&A/评论/公开笔记；
- 创建/编辑本地笔记；
- 创建人生记录；
- 编辑允许离线的草稿。

网络恢复后再同步。

---

# 17. 硬件渐进增强

LifeBook 不按型号判断，只按 Capability：

```text
input.touch
input.physical_page_key
input.pen*
display.fast_refresh
display.color
light.frontlight*
audio.output
bluetooth.*
```

能力少意味着功能降级，不意味着另一份 LifeBook。

---

# 18. 第一阶段路线

## Phase A

```text
LifeBook skeleton
baga.ui
lifecycle
storage
lsqlite3
SQLite schema/migration
offline start
```

## Phase B

```text
baga.library
baga.reader
reading progress
notes/highlights
Reader Anchor
```

## Phase C

```text
Articles
Q&A
Comments
Public Notes
SQLite cache / FTS
```

## Phase D

```text
Life Records
Time Capsule
Automerge prototype for true concurrent objects
```

## Phase E

```text
AI
Pen / Color / Audio enhancements
```

Kindle Platform/Client 的工程开工顺序不由本节定义，必须使用 `03` Freeze 中的 Kindle Phase 0–4 / Compatibility-first 路线。

---

# 19. 验收标准

LifeBook Reference baseline SHOULD 满足：

1. 同一 `lifebook.ikp` 跨 Kindle / Android E-Paper；
2. 核心业务不判断 Vendor；
3. 设备能力只使用 `baga.*`；
4. 结构化关系数据使用正式 `lsqlite3` / SQLite；
5. SQLite schema/migration 在 update/restart 下可靠；
6. Reader 不绑定 EPUB；
7. Reader Anchor 不依赖 KOReader private schema；
8. 真正 CRDT 场景优先 Automerge，不自研通用 CRDT；
9. Automerge 可以整用/拆用，不强制 automerge-repo；
10. offline start 可用；
11. sync 失败不破坏本地已提交数据；
12. sleep/wake 可恢复；
13. 更新失败不删除书籍、笔记或 SQLite DB；
14. 通过对应 BICTS；
15. Kindle build 中 LifeBook 不直接 import KOReader / KPM / MRPI / KUAL / sh_integration 私有接口；
16. Kindle 上同一 `lifebook.ikp` 不因 `kindlepw2` / `kindlehf` 等 native target 分叉。

---

# 20. 最终原则

> **LifeBook 只实现 LifeBook 产品；设备差异交给 Baga Ink；成熟通用软件能力直接站在成熟生态肩膀上。SQLite 直接使用 SQLite，Automerge 优先复用 Automerge，KOReader 在 Kindle Platform 内部充分复用。**

> **Kindle 的具体 bootstrap、KPM/MRPI、Home Entry、KOReader pinning、Platform Core 与 IKP Package Manager 边界以 `03_Kindle具体实现架构冻结_Baga-Ink-Kindle-Implementation-Architecture-Freeze.md` 为代码开工基线。**
