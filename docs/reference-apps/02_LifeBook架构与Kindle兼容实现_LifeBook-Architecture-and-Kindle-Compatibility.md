# LifeBook IKP 架构与 Kindle 兼容实现 / LifeBook IKP Architecture and Kindle Compatibility

> **文档级别：Reference App 技术实现补充**  
> **状态：Baseline v0.4**  
> **日期：2026-08-23**  
> **适用对象：LifeBook (`lifebook.ikp`) on Baga Ink Platform**  
> **上位文档：`docs/standards/` 全部正式规范**  
> **配套文档：`01_LifeBook参考实现_LifeBook-Reference-App.md`**

---

## 0. 本轮关键纠偏

本版本正式撤销此前 `baga.data → SQLite` 的设计。

当前结论：

```text
设备 / OS / Platform 差异
→ baga.*

关系数据库
→ Baga Lua Profile Standard Library: lsqlite3 / SQLite

Local-first / CRDT
→ Automerge core 为正式 Adopted Foundation，可整体或拆模块复用

Reader / Kindle UI / device knowledge
→ 最大化复用 KOReader / koreader-base / FBInk
```

原则：

> **SQLite 就直接用 SQLite；Automerge 就充分复用 Automerge；不为了“Baga 风格统一”再套一层更弱抽象。**

---

# 1. 架构不变

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

没有：

```text
LifeBook Runtime
SQLite Layer
Automerge Layer
KOReader Provider Layer
CRDT Engine Layer
```

Standard Library 也不是新架构层。

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

LifeBook 不负责：

```text
Kindle framebuffer
Kindle input
Kindle sleep/wake
文档 parser/render engine
SQLite database engine
通用 CRDT 算法
Kindle Homebrew 生命周期
jailbreak / enablement route
```

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
│   └─ 成熟 HTTP / TLS / Kindle 网络桥接
│
└─ baga.power
    └─ Kindle 系统能力 / KOReader/Homebrew 已验证机制
```

### 3.1 绝不能误读

```text
lsqlite3
≠ baga.data

Automerge
≠ baga.sync

KOReader
≠ Baga Reader 公共层
```

---

# 4. SQLite binding 决策

## 4.1 IKP 对外：`lsqlite3`

正式选择：

```lua
local sqlite3 = require("lsqlite3")
```

原因：

- thin wrapper；
- 保留成熟 SQLite 模型；
- MIT/X11；
- 支持普通 Lua 5.1–5.5，不把 Baga Lua Profile 永久锁死 LuaJIT；
- 动态链接 Platform SQLite；
- 仍有活跃维护。

LifeBook 可以直接写：

```lua
local path = baga.storage.resolve_path("appdata/lifebook.sqlite3")
local db = sqlite3.open(path)

db:exec([[CREATE TABLE ...]])
```

## 4.2 KOReader 内部：继续 `lua-ljsqlite3`

KOReader 已经长期使用：

```lua
require("lua-ljsqlite3/init")
```

Baga 不要求把 KOReader 内部代码迁移到 `lsqlite3`。

正确实现：

```text
Platform-managed libsqlite3
├─ lsqlite3       → IKP / LifeBook
└─ lua-ljsqlite3  → KOReader internals
```

## 4.3 不用 `lsqlite3complete`

避免在同一 Platform 进程静态塞入第二份 SQLite runtime。

---

# 5. LifeBook SQLite Schema Philosophy

LifeBook 自己决定 schema，而 Baga 不包一层 database repository API。

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

这不是标准 schema，只是 LifeBook 产品实现。

SQLite 的 transaction、JOIN、INDEX、foreign key、FTS5、JSON 等成熟能力都可正常利用。

---

# 6. SQLite 文件路径与 Sandbox

```lua
local path = baga.storage.resolve_path("appdata/lifebook.sqlite3")
```

`resolve_path()` 只做：

```text
Baga logical app path
→ 当前设备安全真实路径
```

不做数据库抽象。

在 Kindle 上必须额外验证：

- `../` 逃逸；
- absolute path；
- ATTACH database path；
- URI/path trick；
- SQLite extension loading；
- other-App private DB access。

因为 Kindle 不像 Android 那样天然拥有现代 per-App sandbox。

---

# 7. Automerge 正式采纳哲学

Automerge 不是“参考思想”，而是优先成熟基础实现。

但采用 Automerge 不表示把整个生态一股脑全搬进来。

LifeBook / Platform MAY：

```text
A 完整 core：document + merge + binary + sync
B 只用 document / merge / history
C Automerge binary 存 SQLite BLOB / file
D 只用 sync protocol
E 通过 automerge-c / Rust core
F 只用 patches / cursors
```

不强制采用 `automerge-repo`。

---

# 8. 为什么不把 automerge-repo 变成 Baga 架构

Automerge Repo 是高层多文档 / storage adapter / network adapter 管理库。

它很优秀，但并不等于 Automerge core，而且不同 Repo 语言实现的 filesystem layout / network protocol 可能并不兼容。

所以 Baga 不复制：

```text
Automerge Repo
  ↓
Storage Adapter
  ↓
Network Adapter
```

成为自己的公共层级。

能复用模块就复用模块，需要跨实现互操作时锁定明确 core binary/sync protocol 版本。

---

# 9. Automerge Lua API 状态

当前尚未发现足够成熟、官方维护且适合 Baga 的 Automerge Lua binding。

因此当前是：

```text
Automerge Foundation → ADOPTED
Developer-facing Lua binding → PROVISIONAL / NOT FROZEN
```

绝不为了“完整”现在生造：

```text
baga.automerge
baga.crdt
```

Kindle 第一阶段可以研究：

```text
automerge-c
Rust core bridge
LuaJIT FFI
其他受控集成
```

重点实测二进制体积、RAM、CPU、armel/armhf 构建。

---

# 10. SQLite + Automerge 组合

两者是天然互补：

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

# 11. Offline-first 三个问题

```text
1. Local persistence
   → SQLite / files

2. Concurrent merge
   → business rule / Automerge（适用时）

3. Scheduling / transport
   → baga.sync + baga.network
```

这三个不能混成一个 `Data/Sync Engine`。

---

# 12. 阅读位置同步

Reading Position 通常不需要 CRDT。

例如两台设备：

```text
Kindle → 40%
Phone  → 70%
```

可以通过明确业务规则选择更靠后的有效阅读位置，并保留 timestamp/device history。

复杂文本笔记才更可能需要 Automerge。

---

# 13. Reader / KOReader

Kindle Reader 第一选择 KOReader。

LifeBook 只调用：

```lua
baga.reader.supports(source)
baga.reader.open(source)
```

KOReader 内部可完整复用：

```text
ReaderUI
CREngine
MuPDF
Annotation
Highlight
Bookmark
Search
Selection
Position
```

LifeBook 不依赖其 private object。

---

# 14. Reader 不以 EPUB 为中心

实际支持范围来自当前 Reader implementation。

可能包括：

```text
EPUB
PDF
MOBI/AZW family
FB2
TXT/HTML
DjVu
CBZ/comics
其他 KOReader 已支持格式
```

LifeBook 产品定义不冻结成 EPUB Reader。

---

# 15. Reader Anchor

KOReader 已有不同定位模型：

```text
rolling/reflowable
→ XPointer-like positions

paging/fixed-page
→ page + local positions / boxes
```

Baga `reader.anchor` 直接站在这些能力上，不重写各格式 Locator。

LifeBook 只保存 opaque Anchor。

Readium Locator / EPUB CFI / W3C Annotation 只作设计参考。

---

# 16. LifeBook 文章/Q&A/评论

这些不是 Book Reader 文档。

```text
LifeBook Server / SQLite Cache
        ↓
LifeBook Domain
        ↓
baga.ui
```

不转 EPUB，不经过 KOReader ReaderUI。

---

# 17. `baga.library`

```text
Kindle existing books
       ↓
Kindle Adapter / Platform
       ↓
baga.library
       ↓
LifeBook
```

LifeBook 不扫描 `/documents`，Library handle 可交给 Reader。

---

# 18. Kindle ABI / 固件

LifeBook 不按型号维护 IKP。

KOReader target 是重要工程参考：

| 平台族 | target | 工程含义 |
|---|---|---|
| Legacy | `kindle-legacy` | K2/K3/DXG；旧 ABI / 低资源 |
| Classic | `kindle` | K4/Touch/PW1 |
| PW2+ soft-float | `kindlepw2` | PW2+ soft-float |
| Hard-float | `kindlehf` | Firmware `>=5.16.3` |

> **5.16.3 是 soft-float / hard-float 重要边界。**

SQLite/lsqlite3 与 Automerge bridge 的 native build 也必须跟随对应 ABI，但 SQL / LifeBook 业务代码不分叉。

---

# 19. 不同 Kindle 硬件

| 条件 | LifeBook 行为 |
|---|---|
| Touch | `input.touch` 增强 |
| Physical page keys | page_next/page_previous |
| No touch | Focus + navigation |
| Scribe pen | input.pen* 通过 BICTS 后增强 |
| Colorsoft | display.color 增强，黑白仍完整 |
| No fast refresh | TEXT/QUALITY 降级 |
| No audio | 隐藏 Audio/TTS |
| No Bluetooth | 隐藏 Bluetooth 增强 |
| Low RAM/CPU | 缩小 cache/图片/并发任务 |
| Automerge 太重 | 对应并发编辑增强降级，不影响 Base LifeBook |

---

# 20. Firmware / Installation Route

兼容性对象：

```text
Device Model
+ Firmware Range
+ Platform Version
+ Adapter Version
+ Lua Profile Version
+ BICTS Version
```

WinterBreak / SpringBreak / Sanctuary / Véra 等只属于 Installation Route Database。

LifeBook 不知道使用哪条 enablement route。

---

# 21. Home Screen

目标：

```text
Kindle Home
   ↓ one action
LifeBook
```

用户不经过 KUAL → KOReader → Plugin。

KUAL/MRPI/KPM/Hotfix/KOReader 都是内部工具或实现。

---

# 22. 更新 / Migration / Rollback

LifeBook 更新仍使用 Baga IKP signing/staging/rollback。

SQLite migration 属 LifeBook app-data migration：

- migration 必须事务化；
- 失败不得留下半迁移 schema；
- rollback 到旧 App 前必须确认旧版可读取当前 DB，或恢复 migration snapshot；
- App package 与 DB 分离；
- 更新失败不删除 DB。

Automerge document format 升级同样需要明确版本兼容策略。

---

# 23. 第一阶段实测重点

```text
KOReader → baga.reader mapping
KOReader UI → baga.ui mapping
lsqlite3 → KOReader/koreader-base libsqlite3
SQLite FTS5 / JSON / WAL / transaction tests
Kindle sandbox + resolve_path + SQLite ATTACH/path escape tests
baga.library bridge
Reader Anchor rolling + paging round-trip
Automerge core / automerge-c on armel + armhf
Automerge RAM / CPU / binary size
Home direct LifeBook launch
BICTS across representative Kindle families
```

---

# 24. 当前冻结决策

1. LifeBook 正式包是 `lifebook.ikp`。
2. 没有 LifeBook Runtime。
3. LifeBook 设备能力只调用 `baga.*`。
4. `baga.data` 正式撤销。
5. SQLite 是 Baga Lua Profile Standard Library 基础。
6. Developer-facing SQLite binding 采用 `lsqlite3`。
7. KOReader 内部继续 `lua-ljsqlite3`，不要求迁移。
8. `lsqlite3` 与 `lua-ljsqlite3` 优先共享单一 Platform `libsqlite3`。
9. 不采用 `lsqlite3complete` 作为 Reference 默认方案。
10. LifeBook 直接使用 SQL / transaction / FTS / JSON。
11. Automerge core 正式 Adopted，可整体或拆模块采用。
12. 不强制 automerge-repo。
13. Automerge Lua binding 尚未冻结，不生造 `baga.crdt` / `baga.automerge`。
14. `baga.sync` 只管 scheduling/policy，不等于 Automerge。
15. Reader 第一选择 KOReader。
16. Reader 不以 EPUB 为中心。
17. Reader Anchor 复用 KOReader 原生定位。
18. `baga.library` 是用户书库边界。
19. 5.16.3 是 Kindle ABI 重要边界。
20. 所有 model/firmware quirks 留在 Platform/Adapter。
21. LifeBook 必须 offline-first。
22. Kindle Home 一次操作进入 LifeBook。
23. 更新必须保护书籍、笔记和 SQLite DB。

---

# 25. 最终一句话

> **LifeBook 在 Kindle 上不需要再造 Reader、数据库或 CRDT：Reader 大量复用 KOReader；关系数据直接使用 `lsqlite3` / SQLite；真正 Local-first 并发对象优先复用 Automerge core，并允许整体或拆模块采用。Baga Ink 只统一真正需要统一的设备/平台边界。**