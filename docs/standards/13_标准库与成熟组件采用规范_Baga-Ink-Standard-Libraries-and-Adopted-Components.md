# Baga Ink 标准库与成熟组件采用规范 / Baga Ink Standard Libraries and Adopted Components

> **文档级别：一级平台规范 / Platform Standard**  
> **状态：Draft v0.2**  
> **日期：2026-08-23**  
> **上位文档：`01_顶层战略与架构_Baga-Ink-Platform-Strategy.md`**  
> **配套规范：`02_应用标准_Baga-Ink-App-Standard.md`、`03_API规范_Baga-Ink-API-Specification.md`、`10_兼容性测试套件_Baga-Ink-Compatibility-Test-Suite.md`**

---

## 0. 目的

本文档定义 Baga Ink 如何采用 SQLite、Automerge 等已经成熟、跨平台、设计优秀的通用开源库，同时避免：

1. 已有成熟轮子却重新发明 Baga 私有数据库 / CRDT；
2. 因采用一个库就增加新的公共架构层；
3. 为了 Sandbox 而破坏成熟库本身优秀的 API / 数据模型。

核心原则：

> **标准化真正需要跨设备统一的边界；成熟通用库能直接采用时就直接采用。**

> **Reuse mature libraries directly where appropriate; do not hide them behind weaker Baga-specific abstractions.**

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

不应仅因“跨设备”就自动包装成：

```text
baga.data
baga.database
baga.crdt
baga.automerge
```

如果上游库本身已经拥有成熟跨平台抽象，Baga SHOULD 优先直接采用其 API / 数据模型 / protocol / format，或只拆用真正需要的模块。

---

# 2. `baga.data` 正式撤销

此前 Draft 曾提出：

```text
baga.data
```

并定义 `get / put / list / transaction` 一类 Baga 私有 KV/Collection 接口。

该设计正式撤销。

原因：

- `data` 语义过宽；
- SQLite 已经提供 SQL、transaction、prepared statement、index、foreign key、BLOB、FTS、JSON 等成熟模型；
- 再包一层会丢失 SQLite 能力并增加维护成本；
- Android、Flutter、Linux 和 KOReader 都普遍直接使用 SQLite 或 SQLite binding；
- Baga 真正需要补的是 Sandbox、版本 Profile、编译选项和测试，而不是数据库语义。

> **`baga.data` MUST NOT 进入 Baga Ink v0.x 正式 API。**

---

# 3. SQLite：Baga 正式 Standard Library 基础

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

Baga 不重新定义这些语义。

---

# 4. Lua binding 决策：`lsqlite3`

Baga Lua Profile 的 developer-facing SQLite binding 选择：

> **LuaSQLite3 / `lsqlite3`**

使用上游模块名：

```lua
local sqlite3 = require("lsqlite3")
local db = sqlite3.open(filename)
```

Baga 不改名为 `baga.sqlite`，也不发明另一套 query API。

## 4.1 选择理由

`lsqlite3`：

- 是 SQLite thin wrapper；
- 保留 database / statement / SQL / transaction 模型；
- 采用宽松 MIT 风格许可；
- 0.9.7 已测试 Lua 5.5，并设计兼容 Lua 5.4/5.3/5.2/5.1；
- 动态链接 `libsqlite3`；
- 不要求 LuaJIT FFI，因此不把 Baga Lua Profile 永久锁死 LuaJIT。

## 4.2 KOReader 为什么继续 `lua-ljsqlite3`

KOReader 已经长期使用 `lua-ljsqlite3`，其现有代码直接使用：

```text
open / exec / prepare / bind / step / rowexec
```

它是很有价值的 LuaJIT SQLite binding，KOReader 内部 SHOULD 原样继续使用。

但它与 LuaJIT/FFI 强相关，不适合作为 Baga 所有未来 Lua runtime 的 developer-facing 公共契约。

因此：

```text
IKP Developer
└─ lsqlite3

KOReader internals
└─ lua-ljsqlite3

两者
└─ SHOULD 共享同一 Platform-managed libsqlite3
```

---

# 5. 单一 SQLite runtime：不默认采用 `lsqlite3complete`

Reference Platform SHOULD：

```text
lsqlite3
+
单一 Platform-managed libsqlite3
```

而不是默认使用：

```text
lsqlite3complete
```

LuaSQLite3 官方文档明确说明：`lsqlite3` 动态链接 SQLite，而 `lsqlite3complete` 静态嵌入另一份 SQLite；同一进程中存在多份 SQLite runtime 会增加不必要的复杂性和风险。

Kindle SHOULD 优先复用 KOReader/koreader-base 已经验证的 `libsqlite3`。

Android SHOULD 由 Baga Platform 自己锁定 SQLite runtime，而不是让 Universal IKP 依赖 OEM/Android 系统中变化的 SQLite 版本。

---

# 6. Baga SQLite Profile

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

# 7. SQLite Sandbox：保持 API，限制 VFS

这是弱 OS sandbox 平台（尤其 Kindle）的关键安全设计。

仅提供：

```text
baga.storage.resolve_path()
```

**不足以成为 SQLite 的完整安全边界**，因为 SQLite 本身还可以通过 `ATTACH DATABASE` 等操作继续打开文件。

SQLite 已经提供成熟的 OS abstraction：

> **SQLite VFS (`sqlite3_vfs`)**

VFS 的 `xOpen / xDelete / xAccess / xFullPathname` 等方法正是 SQLite 所有数据库、journal、WAL 等文件 I/O 的标准入口。

因此：

## 7.1 Android / 强 OS sandbox 平台

可以主要依赖：

```text
OS App Sandbox
+
Baga app-private directory
+
lsqlite3
```

Baga MAY 提供 `baga.storage.resolve_path()` 作为路径便利函数。

## 7.2 Kindle / 弱 OS sandbox 平台

Baga Reference Platform MUST 使用 **sandbox-aware SQLite VFS 或等价的 SQLite I/O confinement**，确保当前 IKP 只能打开其授权根目录内的数据库及 SQLite 附属文件。

应覆盖：

```text
main database
-journal
-wal
-shm
temporary DB
ATTACH database
xDelete / xAccess / xFullPathname
```

实现 MAY 基于 SQLite 默认 VFS 包一层路径约束。

### 7.2.1 保持 `lsqlite3` API

即使底层使用 Baga sandbox VFS，IKP 仍写：

```lua
local sqlite3 = require("lsqlite3")
local db = sqlite3.open(filename)
```

Baga 可以维护一个**API-compatible build/integration**，让 `sqlite3.open()` 内部选择当前 App 的 sandbox VFS。

这是安全实现细节，不是新的数据库 API。

### 7.2.2 防止绕过 VFS

弱 sandbox 平台 SHOULD：

- 禁止或严格限制 SQLite URI `vfs=` 覆盖；
- 禁止任意 loadable extension；
- 防止 App 选择未授权 VFS；
- 对 absolute path / `..` / symlink escape 做 canonical-path 检查；
- 确保 `ATTACH` 同样经过 sandbox VFS。

`resolve_path()` 可以存在，但**不是唯一安全边界**。

---

# 8. Automerge：正式 Adopted Local-first Foundation

Baga Ink 正式把 `automerge/automerge` core 视为 Local-first / CRDT 场景的优先成熟基础实现。

Automerge 当前核心提供：

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

它是实际采用的优秀基础，不只是“参考思想”。

---

# 9. Automerge 可以整体采用，也可以拆模块采用

Baga / LifeBook MAY：

```text
A. 完整使用 core
   document + merge + binary + sync

B. 只用 document / merge / history

C. 只用 binary persistence
   存 SQLite BLOB / app file

D. 只用 sync protocol
   transport 仍由现有 HTTP/WebSocket/其他可靠通道承担

E. 使用 automerge-c / Rust core bridge

F. 只用 patches / cursors
```

> **采用 Automerge 不要求把其所有 package、repo 层和 adapter 都一起采用。**

---

# 10. 不强绑 `automerge-repo`

`@automerge/automerge-repo` 是高层多文档、Storage Adapter、Network Adapter 管理库，非常有参考价值，但不等于 Automerge core。

不同语言 Repo 实现甚至可能存在不同 disk layout / network compatibility；例如 `automerge-repo-rs` 明确说明其 filesystem layout 和 WebSocket protocol 与 JavaScript automerge-repo 不兼容。

因此 Baga v0.x：

- MUST NOT 复制 automerge-repo 的 Adapter 架构成为 Baga 公共层；
- MUST NOT 强迫所有平台采用 automerge-repo；
- MAY 整体或拆分复用适合模块；
- 真正需要跨实现互操作时，优先锁定 Automerge core binary / sync protocol 的明确版本。

---

# 11. Automerge Lua 状态

SQLite 已有成熟 Lua binding，因此 `lsqlite3` 可以 Stable。

Automerge 当前拥有 Rust / C / JS/WASM 等接口，但**尚未发现足够成熟、官方维护且适合 Baga 的 Lua binding**。

因此：

```text
Automerge Foundation: ADOPTED
Developer-facing Lua module: PROVISIONAL / NOT FROZEN
```

当前 MUST NOT 生造：

```text
baga.automerge
baga.crdt
Automerge-like Baga Lua object model
```

在成熟 Lua binding 出现前，Platform / LifeBook MAY 通过：

```text
Rust core
automerge-c
LuaJIT FFI
其他受控 bridge
```

使用 Automerge。

未来若公开 Lua binding，应尽量保持 Automerge 上游概念与 format/protocol，而不是另造一套语义。

---

# 12. SQLite + Automerge 可以组合

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
└─ Automerge doc/change metadata or BLOB

Automerge
├─ My Notes（真正并发编辑时）
├─ Life Records
├─ Time Capsule drafts
└─ Article drafts
```

`baga.sync` 只负责设备/网络调度；如果采用 Automerge sync protocol，它负责 CRDT 增量交换语义。

---

# 13. Standard Library 不是架构层

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

这些不是：

```text
SQLite Layer
Automerge Layer
Database Provider Layer
CRDT Engine Layer
```

---

# 14. 通用成熟库采用判定

未来新增能力前先问：

1. 是否已有广泛使用、长期维护、许可证兼容的成熟库？
2. 该库的抽象是否已经比自定义 `baga.*` 更成熟？
3. 能否直接采用其 API / data format / protocol？
4. 是否只需要其中一部分模块？
5. Baga 真正需要补的是否只是 sandbox、path、permission、lifecycle、version profile、testing？
6. 能否避免把特定 runtime 错误升级成 Universal contract？

默认原则：

> **先复用成熟库，再只补 Baga 必须统一的边界。**

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