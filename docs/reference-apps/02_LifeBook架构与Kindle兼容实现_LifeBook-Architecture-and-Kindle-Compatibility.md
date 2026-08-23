# LifeBook IKP 架构与 Kindle 兼容实现 / LifeBook IKP Architecture and Kindle Compatibility

> **文档级别：Reference App 技术实现补充**  
> **状态：Baseline v0.5**  
> **日期：2026-08-23**  
> **适用对象：LifeBook (`lifebook.ikp`) on Baga Ink Platform**  
> **上位文档：`docs/standards/` 全部正式规范**  
> **配套文档：`01_LifeBook参考实现_LifeBook-Reference-App.md`**

---

## 0. 当前技术基线

```text
设备 / OS / Platform 差异
→ baga.*

关系数据库
→ Baga Lua Profile Standard Library: lsqlite3 / SQLite

Local-first / CRDT
→ Automerge core，可整体或拆模块复用

Reader / Kindle UI / device knowledge
→ 最大化复用 KOReader / koreader-base / FBInk
```

原则：

> **SQLite 直接使用 SQLite；Automerge 充分复用 Automerge；KOReader 充分复用 KOReader；只对真正的设备/平台差异建立 Baga API。**

正式正文只描述当前有效设计。

---

# 1. 架构

```text
LifeBook — lifebook.ikp
        │
        ▼
Baga Ink API / Baga Lua Profile
        │
        ▼
Baga Ink Platform Core
        │
        ▼
Baga Ink Kindle Adapter
        │
        ▼
Kindle OS
```

Standard Library、Adopted Foundation 与内部开源组件不是新的公共架构层。

---

# 2. LifeBook 自己负责什么

```text
Account / Session
Library Product Logic
Articles
Q&A / Comments
Public Notes
My Notes / Highlights
Life Records
Time Capsule
AI
Offline Cache Policy
Sync Domain Policy
SQLite schema / migration / queries
```

Kindle framebuffer/input/sleep-wake、文档 parser/render engine、SQLite database engine、通用 CRDT 算法、Homebrew 生命周期与设备安装路线均由平台或成熟基础组件承担。

---

# 3. Kindle Reference Implementation Mapping

> **这是实现映射，不是架构图。**

```text
Baga Ink on Kindle
│
├─ baga.reader
│   └─ KOReader
│       ├─ ReaderUI
│       ├─ CREngine
│       ├─ MuPDF
│       ├─ ReaderAnnotation / Highlight / Bookmark
│       └─ position / search / selection / anchor
│
├─ baga.ui
│   └─ KOReader Lua UI / widget / UIManager
│
├─ baga.display
│   └─ KOReader Kindle device/display knowledge + FBInk
│
├─ baga.input
│   └─ KOReader Kindle input / key / touch handling
│
├─ baga.storage
│   └─ Kindle filesystem + Baga sandbox/path mapping
│
├─ Baga Lua Profile Standard Library
│   └─ lsqlite3
│       └─ Platform-managed libsqlite3
│
├─ KOReader internals
│   └─ lua-ljsqlite3
│       └─ 与 lsqlite3 共享同一 libsqlite3
│
├─ baga.sync
│   └─ when_online / Wi-Fi / sleep-wake / charging / trigger / retry
│
├─ Automerge core（真正需要 Local-first CRDT 的业务）
│   ├─ document / merge / history
│   ├─ binary persistence
│   ├─ sync protocol（可选）
│   ├─ automerge-c / Rust core bridge
│   └─ patch / cursor（按需）
│
├─ baga.network
│   └─ mature HTTP / TLS / Kindle network bridge
│
└─ baga.power
    └─ Kindle system / validated KOReader/Homebrew mechanisms
```

---

# 4. SQLite binding

## 4.1 IKP / LifeBook：`lsqlite3`

```lua
local sqlite3 = require("lsqlite3")
local path = baga.storage.resolve_path("appdata/lifebook.sqlite3")
local db = sqlite3.open(path)
```

选择理由：thin wrapper、保留成熟 SQLite 模型、宽松许可证、支持普通 Lua 5.1–5.5、动态链接 Platform SQLite，不把 Baga Lua Profile 固定到 LuaJIT。

## 4.2 KOReader 内部：`lua-ljsqlite3`

KOReader 已长期使用其现有 LuaJIT SQLite binding，Baga 不要求迁移。

推荐：

```text
Platform-managed libsqlite3
├─ lsqlite3       → IKP / LifeBook
└─ lua-ljsqlite3  → KOReader internals
```

Reference Platform 不默认使用 `lsqlite3complete`，避免在同一进程维护另一份 SQLite runtime。

---

# 5. LifeBook SQLite Schema Philosophy

LifeBook 自己决定 schema / migration / SQL / index / FTS / business constraints。

典型表可能包括：

```text
books / library_index
reading_progress
account_session
cached_articles
cached_questions
cached_comments
public_note_cache
sync_metadata
local_settings
search_index / FTS
Automerge object metadata
```

这不是平台标准 schema。

---

# 6. SQLite 文件路径与 Sandbox

`baga.storage.resolve_path()` 只负责把 Baga logical app path 映射到当前设备安全运行时路径。

Kindle 缺少现代 Android 式 per-App sandbox，因此必须额外验证：

```text
path traversal / absolute path
ATTACH database
URI / VFS override
symlink / canonical path escape
loadable extension
other-App private DB
journal / WAL / SHM / temporary DB
```

平台 SHOULD 使用 sandbox-aware SQLite VFS 或等价 I/O confinement，并通过 BICTS。

---

# 7. Automerge

Automerge 是优先 Local-first / CRDT Foundation。

LifeBook / Platform MAY：

```text
完整 core：document + merge + binary + sync
只用 document / merge / history
Automerge binary 存 SQLite BLOB / file
只用 sync protocol
通过 automerge-c / Rust core
只用 patches / cursors
```

不强制采用 `automerge-repo`。

当前 developer-facing Lua binding 尚未冻结；Kindle 第一阶段重点验证 automerge-c / Rust core bridge / LuaJIT FFI 等受控接入方式的二进制体积、RAM、CPU、armel/armhf 构建与稳定性。

---

# 8. SQLite + Automerge

```text
SQLite
├─ relational metadata
├─ cache
├─ index / FTS
├─ reading progress
└─ Automerge binary/change metadata

Automerge
├─ My Notes（真正并发时）
├─ Life Records
├─ Time Capsule drafts
└─ Article drafts
```

不是所有笔记都必须 CRDT，也不是所有数据都应该 Automerge。

---

# 9. Offline-first 三个问题

```text
Local persistence
→ SQLite / files

Concurrent merge
→ business rule / Automerge（适用时）

Scheduling / transport
→ baga.sync + baga.network
```

阅读位置通常使用明确业务规则即可；复杂可编辑文本对象更可能使用 Automerge。

---

# 10. Reader / KOReader

Kindle Reader 第一选择 KOReader。

LifeBook 调用：

```lua
baga.reader.supports(source)
baga.reader.open(source)
```

KOReader 内部可复用 ReaderUI、CREngine、MuPDF、Annotation、Highlight、Bookmark、Search、Selection、Position 等成熟能力。

LifeBook 不依赖 KOReader private object。

---

# 11. Reader 格式与 Anchor

实际格式支持来自当前 Reader implementation，可包括 EPUB、PDF、MOBI/AZW family、FB2、TXT/HTML、DjVu、CBZ/comics 等；LifeBook 产品定义不绑定某一格式。

KOReader 已有：

```text
rolling/reflowable → XPointer-like positions
paging/fixed-page  → page + local positions / boxes
```

Baga `reader.anchor` 复用这些成熟定位能力。LifeBook 只保存 opaque Anchor。

Readium Locator / EPUB CFI / W3C Annotation 只作设计参考。

---

# 12. LifeBook 内容与书库

文章 / Q&A / 评论：

```text
LifeBook Server / SQLite Cache
        ↓
LifeBook Domain
        ↓
baga.ui
```

它们不转 EPUB，也不经过 KOReader ReaderUI。

用户书库：

```text
Kindle existing books
       ↓
Kindle Adapter / Platform
       ↓
baga.library
       ↓
LifeBook
```

LifeBook 不扫描真实 Kindle 文档目录；Library handle 可交给 Reader。

---

# 13. Kindle ABI / 固件

LifeBook 不按型号维护 IKP。

KOReader target 是重要工程参考：

| 平台族 | target | 工程含义 |
|---|---|---|
| Legacy | `kindle-legacy` | K2/K3/DXG；旧 ABI / 低资源 |
| Classic | `kindle` | K4/Touch/PW1 |
| PW2+ soft-float | `kindlepw2` | PW2+ soft-float |
| Hard-float | `kindlehf` | Firmware `>=5.16.3` |

> **5.16.3 是 soft-float / hard-float 重要工程边界。**

SQLite/lsqlite3 与 Automerge bridge 的 native build 跟随对应 ABI；SQL 与 LifeBook 业务代码不分叉。

---

# 14. Kindle 硬件渐进增强

| 条件 | LifeBook 行为 |
|---|---|
| Touch | `input.touch` 增强 |
| Physical page keys | page_next/page_previous |
| No touch | Focus + navigation |
| Scribe pen | input.pen* 通过 BICTS 后增强 |
| Color | display.color 增强，黑白仍完整 |
| No fast refresh | TEXT/QUALITY 降级 |
| No audio | 隐藏 Audio/TTS |
| No Bluetooth | 隐藏 Bluetooth 增强 |
| Low RAM/CPU | 缩小 cache/图片/并发任务 |
| Automerge 资源不足 | 对应并发编辑增强降级，不影响 Base LifeBook |

---

# 15. Firmware / Installation Route

兼容性对象：

```text
Device Model
+ Firmware Range
+ Platform Version
+ Adapter Version
+ Lua Profile Version
+ BICTS Version
```

WinterBreak / SpringBreak / Sanctuary / Véra 等属于 Installation Route Database；LifeBook 不感知具体路线。

---

# 16. Home Screen

目标：

```text
Kindle Home
   ↓ one action
LifeBook
```

用户不经过底层 Homebrew/Reader 工具链；这些工具对普通用户隐身。

---

# 17. 更新 / Migration / Rollback

LifeBook 更新使用 Baga IKP signing/staging/rollback。

SQLite migration：

- 必须事务化；
- 失败不得留下半迁移 schema；
- 回滚旧 App 前确认旧版可读取当前 DB，或恢复 migration snapshot；
- App package 与 DB 分离；
- 更新失败不删除 DB。

Automerge document format 升级同样需要明确版本兼容策略。

---

# 18. 第一阶段实测重点

```text
KOReader → baga.reader mapping
KOReader UI → baga.ui mapping
lsqlite3 → KOReader/koreader-base libsqlite3
SQLite FTS5 / JSON / WAL / transaction tests
Kindle sandbox + SQLite ATTACH/path escape tests
baga.library bridge
Reader Anchor rolling + paging round-trip
Automerge core / automerge-c on armel + armhf
Automerge RAM / CPU / binary size
Home direct LifeBook launch
BICTS across representative Kindle families
```

---

# 19. 当前冻结决策

1. LifeBook 正式包是 `lifebook.ikp`。
2. LifeBook 设备能力只调用 `baga.*`。
3. SQLite 是 Baga Lua Profile Standard Library 基础。
4. Developer-facing SQLite binding 采用 `lsqlite3`。
5. KOReader 内部继续 `lua-ljsqlite3`。
6. `lsqlite3` 与 `lua-ljsqlite3` 优先共享单一 Platform `libsqlite3`。
7. Reference Platform 不默认采用 `lsqlite3complete`。
8. LifeBook 直接使用 SQL / transaction / FTS / JSON。
9. Automerge core 正式 Adopted，可整体或拆模块采用。
10. 不强制 automerge-repo。
11. Automerge Lua binding 尚未冻结。
12. `baga.sync` 管 scheduling/policy；Automerge 管采用它的 Local-first 数据语义。
13. Reader 第一选择 KOReader。
14. Reader 不以 EPUB 为中心。
15. Reader Anchor 复用 KOReader 原生定位。
16. `baga.library` 是用户书库边界。
17. 5.16.3 是 Kindle ABI 重要边界。
18. 所有 model/firmware quirks 留在 Platform/Adapter。
19. LifeBook 必须 offline-first。
20. Kindle Home 一次操作进入 LifeBook。
21. 更新必须保护书籍、笔记和 SQLite DB。

---

# 20. 最终原则

> **LifeBook 在 Kindle 上不需要再造 Reader、数据库或 CRDT：Reader 大量复用 KOReader；关系数据直接使用 `lsqlite3` / SQLite；真正 Local-first 并发对象优先复用 Automerge core，并允许整体或拆模块采用。Baga Ink 只统一真正需要统一的设备/平台边界。**
