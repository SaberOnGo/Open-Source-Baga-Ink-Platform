# Baga Ink 标准库与成熟组件采用规范 / Baga Ink Standard Libraries and Adopted Components

> **文档级别：一级平台规范 / Platform Standard**  
> **状态：Draft v0.3**  
> **日期：2026-08-23**  
> **上位文档：`01_顶层战略与架构_Baga-Ink-Platform-Strategy.md`**  
> **配套规范：`02_应用标准_Baga-Ink-App-Standard.md`、`03_API规范_Baga-Ink-API-Specification.md`、`10_兼容性测试套件_Baga-Ink-Compatibility-Test-Suite.md`**

---

## 0. 目的

本文档定义 Baga Ink 如何采用 SQLite、Automerge 等成熟、跨平台、设计优秀的通用开源组件。

核心原则：

> **标准化真正需要跨设备统一的边界；成熟通用库能直接采用时就直接采用。**

> **Reuse mature libraries directly where appropriate; do not hide them behind weaker platform-specific abstractions.**

正式规范只描述当前有效设计。已被否决的接口名、假想 namespace、旧架构不保留在规范正文；历史由 Git 提交记录保存。

---

# 1. `baga.*` 与 Standard Libraries 的边界

`baga.*` 主要解决：

```text
设备 / OS / Platform 差异
UI / Display / Input
Reader / Library
Storage sandbox
Network / Power / Lifecycle
Permission
Sync scheduling
```

成熟通用软件能力，例如：

```text
SQLite relational database
Automerge Local-first / CRDT
未来成熟 JSON / compression / crypto libraries
```

如果上游库本身已经拥有成熟跨平台抽象，Baga SHOULD 优先直接采用其 API / 数据模型 / protocol / format，或只拆用真正需要的模块。

---

# 2. SQLite：Baga Lua Profile Standard Library

Baga Ink 正式采用 SQLite 作为 Universal App 的标准结构化本地数据库基础。

开发者直接使用成熟 SQLite：

```text
SQL
schema
transactions
prepared statements
indexes
foreign keys
BLOB
FTS
JSON
```

Baga 不重新定义这些数据库语义。

---

# 3. Lua binding：`lsqlite3`

Baga Lua Profile 的 developer-facing SQLite binding：

> **LuaSQLite3 / `lsqlite3`**

标准模块名保持上游形式：

```lua
local sqlite3 = require("lsqlite3")
local db = sqlite3.open(filename)
```

## 3.1 选择理由

`lsqlite3`：

- 是 SQLite thin wrapper；
- 保留 database / statement / SQL / transaction 模型；
- 采用宽松 MIT 风格许可；
- 0.9.7 已测试 Lua 5.5，并设计兼容 Lua 5.4/5.3/5.2/5.1；
- 动态链接 `libsqlite3`；
- 不要求 LuaJIT FFI，因此不会把 Baga Lua Profile 永久锁死在 LuaJIT。

## 3.2 KOReader 内部继续使用 `lua-ljsqlite3`

KOReader 已长期使用 `lua-ljsqlite3`，并直接使用：

```text
open / exec / prepare / bind / step / rowexec
```

Baga 不要求 KOReader 为了表面统一而迁移其内部数据库 binding。

推荐关系：

```text
IKP Developer
└─ lsqlite3

KOReader internals
└─ lua-ljsqlite3

两者
└─ SHOULD 共享同一 Platform-managed libsqlite3
```

---

# 4. 单一 SQLite runtime

Reference Platform SHOULD 使用：

```text
lsqlite3
+
单一 Platform-managed libsqlite3
```

`lsqlite3complete` 不作为默认 Reference 方案，因为它静态包含另一份 SQLite runtime。

Kindle SHOULD 优先复用 KOReader/koreader-base 已经验证的 `libsqlite3`。

Android SHOULD 由 Baga Platform 锁定 SQLite runtime，而不是让 Universal IKP 依赖不同 Android/OEM 系统中变化的 SQLite 版本与编译选项。

---

# 5. Baga SQLite Profile

Platform Release MUST 记录：

```text
SQLite version
lsqlite3 version
compile options
source release / digest
```

2026-08-23 Reference Baseline：

```text
SQLite:   3.53.4
lsqlite3: 0.9.7
```

这是 Reference Baseline，不是永久冻结版本。

Profile SHOULD 至少保证：

```text
transactions
prepared statements
indexes
foreign keys
BLOB
JSON functions
FTS5
WAL（目标 filesystem/locking 支持时）
```

Universal IKP 默认 MUST NOT 使用任意 SQLite loadable native extension。

---

# 6. SQLite Sandbox：保持 SQLite API，约束文件访问

SQLite database 是 App sandbox 内的文件资源。

开发者可以通过平台提供的安全路径桥取得 App 私有路径，例如：

```lua
local sqlite3 = require("lsqlite3")
local path = baga.storage.resolve_path("appdata/app.sqlite3")
local db = sqlite3.open(path)
```

## 6.1 Android / 强 OS sandbox 平台

可以主要依赖：

```text
OS App Sandbox
+
Baga app-private directory
+
lsqlite3
```

## 6.2 Kindle / 弱 OS sandbox 平台

Baga Reference Platform MUST 使用 sandbox-aware SQLite VFS 或等价的 SQLite I/O confinement，确保当前 IKP 只能访问其授权根目录内的数据库及 SQLite 附属文件。

应覆盖：

```text
main database
-journal
-wal
-shm
temporary DB
ATTACH database
xOpen / xDelete / xAccess / xFullPathname
```

弱 sandbox 平台 SHOULD：

- 禁止或严格限制 SQLite URI `vfs=` 覆盖；
- 禁止任意 loadable extension；
- 防止 App 选择未授权 VFS；
- 对 absolute path / `..` / symlink escape 做 canonical-path 检查；
- 确保 `ATTACH` 同样经过 sandbox VFS。

即使底层使用 sandbox VFS，IKP 仍保持标准 `lsqlite3` API。

---

# 7. Automerge：Adopted Local-first Foundation

Baga Ink 正式采用 `automerge/automerge` core 作为 Local-first / CRDT 场景的优先成熟基础实现。

Automerge core 当前提供：

```text
CRDT document / merge
change history
compact binary format
sync protocol
patches / cursors
Rust core
C FFI (`automerge-c`)
JavaScript/WASM interface
```

它是实际采用的成熟基础，而不仅是设计参考。

---

# 8. Automerge 可以整体采用，也可以拆模块采用

Baga / LifeBook MAY：

```text
A. 完整使用 core
   document + merge + binary + sync

B. 只使用 document / merge / history

C. 只使用 binary persistence
   存入 SQLite BLOB / app file

D. 只使用 sync protocol
   transport 由 HTTP/WebSocket/其他可靠通道承担

E. 使用 automerge-c / Rust core bridge

F. 只使用 patches / cursors
```

采用 Automerge 不要求把其所有 package、repo 层和 adapter 一起采用。

---

# 9. `automerge-repo` 的位置

`@automerge/automerge-repo` 是高层多文档、Storage Adapter、Network Adapter 管理库，具有很高参考和复用价值，但不等于 Automerge core。

不同语言 Repo 实现可能存在不同 disk layout / network compatibility。因此 Baga：

- 不强迫所有平台采用 automerge-repo；
- MAY 整体或拆分复用适合模块；
- 真正需要跨实现互操作时，优先锁定 Automerge core binary / sync protocol 的明确版本。

---

# 10. Automerge Lua 状态

Automerge 当前拥有 Rust / C / JS/WASM 等接口，但尚未发现足够成熟、官方维护且适合 Baga 的 Lua binding。

因此当前状态：

```text
Automerge Foundation: ADOPTED
Developer-facing Lua module: PROVISIONAL / NOT FROZEN
```

在成熟 Lua binding 出现前，Platform / LifeBook MAY 通过：

```text
Rust core
automerge-c
LuaJIT FFI
其他受控 bridge
```

复用 Automerge。

未来若公开 Lua binding，应尽量保持 Automerge 上游概念、format 与 protocol。

---

# 11. SQLite + Automerge 组合

两者解决不同问题：

```text
SQLite
→ relational persistence / query / index / FTS

Automerge
→ concurrent local-first state / merge / history / optional sync
```

LifeBook 可以自然组合：

```text
SQLite
├─ library metadata
├─ account/session metadata
├─ server-authoritative cache
├─ reading progress
├─ indexes / FTS
└─ Automerge document/change metadata or BLOB

Automerge
├─ My Notes（真正并发编辑时）
├─ Life Records
├─ Time Capsule drafts
└─ Article drafts
```

`baga.sync` 负责设备/网络调度；如果采用 Automerge sync protocol，则由 Automerge 负责 CRDT 增量交换语义。

---

# 12. Standard Library / Adopted Component 不是新架构层

正确架构仍然是：

```text
IKP App
   ↓
Baga Ink API / Baga Lua Profile
   ↓
Baga Ink Platform Core
   ↓
Device Adapter
   ↓
OS / Hardware
```

其中：

```text
Baga Lua Profile
├─ Lua base subset
└─ lsqlite3        Stable Standard Library

Adopted Foundation
└─ Automerge core  Lua binding provisional
```

内部组件、库或 binding 不因被采用而自动形成新的公共架构层。

---

# 13. 通用成熟库采用判定

未来新增能力前先问：

1. 是否已有广泛使用、长期维护、许可证兼容的成熟库？
2. 该库的抽象是否已经成熟且适合直接采用？
3. 能否直接采用其 API / data format / protocol？
4. 是否只需要其中一部分模块？
5. Baga 真正需要补的是否只是 sandbox、path、permission、lifecycle、version profile、testing？
6. 能否避免把某一设备/Runtime 的实现细节升级成 Universal contract？

默认原则：

> **先复用成熟库，再只补 Baga 必须统一的边界。**

---

# 14. 文档治理

Standards 与 Reference Apps MUST 只描述当前有效设计。

已被替换、否决或未采用的接口名、namespace、架构草案不保留在正式正文中。需要追溯历史时使用 Git commit / diff。

这样可以避免开发者和后续 AI 把历史反例重新理解成候选标准。

---

# 15. 参考依据

- SQLite: https://sqlite.org/
- SQLite VFS: https://sqlite.org/vfs.html
- LuaSQLite3 / lsqlite3: https://lua.sqlite.org/
- Automerge core: https://github.com/automerge/automerge
- Automerge Repo: https://github.com/automerge/automerge-repo
- automerge-repo-rs: https://github.com/automerge/automerge-repo-rs
- KOReader: https://github.com/koreader/koreader
- KOReader Base: https://github.com/koreader/koreader-base

实际发布必须锁定 dependency version / commit，并通过 BICTS。
