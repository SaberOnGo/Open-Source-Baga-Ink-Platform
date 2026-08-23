# Baga Ink 标准库与成熟组件采用规范 / Baga Ink Standard Libraries and Adopted Components

> **文档级别：一级平台规范 / Platform Standard**  
> **状态：Draft v0.1**  
> **日期：2026-08-23**  
> **上位文档：`01_顶层战略与架构_Baga-Ink-Platform-Strategy.md`**  
> **配套规范：`02_应用标准_Baga-Ink-App-Standard.md`、`03_API规范_Baga-Ink-API-Specification.md`、`10_兼容性测试套件_Baga-Ink-Compatibility-Test-Suite.md`**

---

## 0. 目的

本文档定义 Baga Ink 如何采用 SQLite、Automerge 等已经成熟、跨平台、设计优秀的通用开源库，同时避免两个相反错误：

1. 已经存在成熟轮子，却重新发明一套 Baga 私有数据库 / CRDT / Reader 基础；
2. 因为采用某个库，就把该库机械地变成新的 Baga Ink 公共架构层。

核心原则：

> **标准化真正需要跨设备统一的边界；直接采用已经成熟的通用库语义。**

> **Reuse mature libraries directly where appropriate; do not hide a mature standard library behind a weaker Baga-specific abstraction.**

---

# 1. `baga.*` 与 Standard Libraries 必须区分

`baga.*` 主要解决：

```text
设备 / OS / Platform 差异
UI / Display / Input
Reader
Library
Storage sandbox
Network
Power
Lifecycle
Permission
Sync scheduling
```

而成熟通用软件能力，例如：

```text
SQLite relational database
Automerge local-first / CRDT
JSON / compression / cryptography libraries
```

不应仅因为需要跨设备使用，就自动被重新包装成：

```text
baga.data
baga.database
baga.crdt
baga.automerge
```

如果上游库本身已经拥有成熟、稳定、跨平台的抽象，Baga SHOULD 优先直接采用其 API / 数据模型 / 协议或其中合适模块。

这不是新增架构层。

---

# 2. `baga.data` 正式撤销

此前 Draft v0.3 曾提出：

```text
baga.data
```

并定义 `get / put / list / transaction` 一类 Baga 私有结构化数据 API。

经过与 Android、Flutter、Linux、KOReader 和 SQLite 生态的重新比较，本设计正式撤销。

原因：

- `data` 语义过宽；
- SQLite 已经提供成熟的 SQL、transaction、prepared statement、index、foreign key、BLOB、FTS 等模型；
- 再定义一套 Baga KV / collection API 会削弱 SQLite，而不是增强可移植性；
- Android、Flutter、Linux 与 KOReader 的成熟实践都是直接使用 SQLite 或 SQLite binding，而不是先人为屏蔽 SQLite；
- Baga 应统一 App 沙箱、路径与兼容 Profile，而不是重新定义关系数据库。

因此：

> **`baga.data` MUST NOT 进入 Baga Ink v0.x 正式 API。已有文档中与本规范冲突的 `baga.data` Draft 描述由本规范撤销。**

---

# 3. SQLite：正式 Standard Library

Baga Ink 正式采用 SQLite 作为 Universal App 的标准结构化本地数据库基础。

SQLite 本身是成熟的 in-process、serverless、ACID、跨平台嵌入式数据库，因此 Baga 不再在其上定义另一套数据库语义。

开发者应直接使用 SQL 与 SQLite transaction model。

---

# 4. Lua binding 决策：采用 `lsqlite3`

Baga Lua Profile 的正式 SQLite binding 选择：

> **LuaSQLite3 / `lsqlite3`**

标准使用方式保持上游命名：

```lua
local sqlite3 = require("lsqlite3")
local db = sqlite3.open(path)
```

Baga 不重新命名为 `baga.sqlite`，也不发明另一套 query API。

## 4.1 为什么选 `lsqlite3`

`lsqlite3`：

- 是 SQLite 的 thin wrapper；
- 直接保留 SQL、database、statement、transaction 等 SQLite 模型；
- MIT/X11 许可；
- 当前 0.9.7 支持 Lua 5.1–5.5；
- 2026 年仍有维护更新；
- 可动态链接平台提供的单一 `libsqlite3`；
- 不要求 LuaJIT FFI，因此不会把 Baga Lua Profile 永久锁死在 LuaJIT。

## 4.2 为什么不把 `lua-ljsqlite3` 作为公共标准

KOReader 当前已经长期实际使用：

```text
lua-ljsqlite3
```

它是非常有价值、经过 Kindle/Android 实践验证的 LuaJIT SQLite binding，KOReader 内部 SHOULD 继续使用，不需要为了 Baga 重写 KOReader。

但它：

- 是 LuaJIT-specific binding；
- 依赖 LuaJIT FFI / 相关 LuaJIT 环境；
- 不适合作为未来可能由 Lua 5.4/5.5 等实现承载的 Baga Lua Profile 公共契约。

因此正确关系：

```text
IKP Developer
  └─ require("lsqlite3")        ← Baga Lua Profile 标准库

Kindle / KOReader internals
  └─ lua-ljsqlite3              ← 继续保留，属于内部实现

两者
  └─ 可共享同一平台 libsqlite3
```

Baga 不要求 KOReader 内部迁移到 `lsqlite3`。

---

# 5. 动态链接：不采用 `lsqlite3complete`

Baga Reference Platform SHOULD 使用：

```text
lsqlite3
+
单一 Platform-managed libsqlite3
```

而不是：

```text
lsqlite3complete
```

LuaSQLite3 官方文档明确区分：`lsqlite3` 动态链接系统/平台 SQLite，而 `lsqlite3complete` 静态包含另一份 SQLite；当进程中已经存在 SQLite 时，多份 SQLite library 可能带来不必要的复杂性和风险。

因此 Baga 的原则是：

> **一个 Platform 进程尽量只维护一份明确版本的 SQLite runtime。**

Kindle Reference Implementation SHOULD 优先复用 KOReader/koreader-base 已经打包并验证的 `libsqlite3`，再为 IKP 暴露 `lsqlite3` binding。

Android Reference Platform SHOULD 随 Baga Platform 锁定 SQLite runtime，而不是让 IKP 依赖不同 Android / OEM 系统中不可预测的 SQLite 版本。

---

# 6. Baga SQLite Profile

Baga 不重新定义 SQL，但必须定义一个可预测的 SQLite Profile。

Platform Release MUST 在 dependency manifest 中记录：

```text
SQLite version
lsqlite3 version
compile options
source digest / commit or release
```

2026-08-23 的 Reference Baseline：

```text
SQLite:   3.53.4
lsqlite3: 0.9.7
```

这只是当前 Reference Baseline；后续 Platform 可以升级，但必须经过 BICTS / migration regression。

Baga SQLite Profile SHOULD 至少保证：

```text
transactions
prepared statements
indexes
foreign keys
BLOB
WAL support
JSON functions (不得 SQLITE_OMIT_JSON)
FTS5
```

动态 loadable extension 对 Universal IKP 默认 MUST 禁止，避免借 SQLite extension 绕过 native-code / sandbox policy。

---

# 7. Database path 与 Sandbox

SQLite database 是文件，因此数据库位置属于 App Sandbox，而不是数据库语义本身。

Baga SHOULD 提供一个很薄的路径桥，例如：

```lua
local path = baga.storage.resolve_path("appdata/lifebook.sqlite3")
local sqlite3 = require("lsqlite3")
local db = sqlite3.open(path)
```

`baga.storage.resolve_path()`：

- 只解析当前 App 被授权的逻辑路径；
- 返回供标准库 / native library 使用的当前平台路径；
- App MUST NOT 持久化、同步或解析该路径的设备特征；
- 不允许用它逃逸到其他 App 或系统目录。

这与 Android `getDatabasePath()`、Flutter `getDatabasesPath()` / path-provider 的成熟做法一致：**平台负责安全位置，SQLite 负责数据库。**

在具有强 OS sandbox 的平台，约束可以由 OS 强制；在 Kindle 等缺少 per-App OS sandbox 的环境，Platform MUST 用路径校验、受限 VFS 或等价机制确保 `lsqlite3` 无法突破 App sandbox。

---

# 8. Automerge：正式 Adopted Local-first Foundation

Baga Ink 正式把 `automerge/automerge` 视为 Local-first / CRDT 场景的优先成熟基础实现。

Automerge 采用 MIT 许可证，当前核心实现位于 Rust，并提供：

```text
CRDT document / merge
change history
compact binary storage format
sync protocol
patches / cursors 等增量能力
C FFI (automerge-c)
JavaScript/WASM binding
其他语言 binding
```

它是优秀基础库，而不是 Baga 要重新仿制的算法参考。

---

# 9. Automerge 可以整体采用，也可以拆模块采用

Baga / LifeBook MAY 按实际需求：

```text
A. 使用完整 Automerge core
   document + merge + binary + sync

B. 只使用 document / merge / history
   网络由现有 Baga network / server protocol 承担

C. 使用 Automerge binary persistence
   存入 SQLite BLOB / app file

D. 使用 Automerge sync protocol
   transport 仍由现有 HTTP/WebSocket/其他可靠通道承担

E. 使用 automerge-c
   通过 C ABI 接入嵌入式/非 JS 环境

F. 使用 patches / cursors 等局部模块
   仅在产品确有需求时采用
```

原则：

> **采用 Automerge 不要求把 Automerge 的每一层、每个 package 都一起采用。**

---

# 10. 不把 `automerge-repo` 强绑成 Baga 标准

`@automerge/automerge-repo` 是非常有价值的高层多文档、Storage Adapter、Network Adapter 管理库，但它不等于 Automerge core。

当前不同语言的 Repo 实现甚至可能具有不同 disk layout / network compatibility；例如 `automerge-repo-rs` 明确说明其 filesystem layout 与 WebSocket protocol 不兼容 JavaScript automerge-repo，并有其他项目在探索兼容实现。

因此 Baga v0.x：

- MUST NOT 把 `automerge-repo` 的 Adapter 架构复制成 Baga 公共架构；
- MUST NOT 规定所有平台必须采用 automerge-repo；
- MAY 参考或直接采用其中适合的模块；
- 跨设备真正需要互操作时，应优先锁定 Automerge core binary / sync protocol 的明确版本，而不是笼统写“使用最新版 Automerge Repo”。

---

# 11. Automerge 与 Baga Lua Profile 的状态

SQLite 已经拥有成熟、持续维护的 Lua binding，因此可以直接进入 Baga Lua Profile Stable Standard Libraries。

Automerge 当前拥有 Rust / C / JS / Swift / Java 等绑定，但**尚未发现足够成熟、官方维护且适合 Baga 的 Lua binding**。

因此：

```text
Automerge foundation: ADOPTED
Automerge developer-facing Lua module: PROVISIONAL / NOT FROZEN
```

Baga MUST NOT 为了“API 看起来完整”现在生造：

```text
baga.automerge
baga.crdt
自定义 Automerge-like Lua API
```

在成熟 Lua binding 出现或 Baga 完成充分跨平台验证前，LifeBook / Platform MAY 通过 Rust core、`automerge-c`、LuaJIT FFI 或其他受控内部方式复用 Automerge。

未来如果选择 developer-facing Lua binding，应尽量保持 Automerge 上游概念和格式，而不是重新发明一套 Baga CRDT 对象模型。

---

# 12. SQLite + Automerge 可以组合，而不是二选一

两者解决不同问题：

```text
SQLite
→ relational local persistence / query / index / FTS

Automerge
→ concurrent local-first state / CRDT merge / change history / sync protocol
```

一个 LifeBook 实现可以自然组合：

```text
SQLite
├─ library metadata
├─ account/session metadata
├─ cached articles/questions/comments
├─ reading progress
├─ indexes / FTS
└─ Automerge document/change BLOB metadata

Automerge
├─ My Notes（确有并发编辑时）
├─ Life Records
├─ Time Capsule drafts
└─ Article drafts
```

然后：

```text
baga.network / baga.sync
→ 负责网络状态、设备生命周期、同步触发与功耗策略

Automerge sync protocol（若采用）
→ 负责 CRDT 增量交换语义
```

这不需要 `baga.data`。

---

# 13. 标准库不是新的架构层

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
├─ Lua standard subset
├─ lsqlite3          stable adopted library
└─ Automerge         adopted foundation; Lua binding provisional
```

这只是 SDK / Runtime 提供的标准库集合，不是：

```text
SQLite Layer
Automerge Layer
Database Provider Layer
CRDT Engine Layer
```

---

# 14. 采用成熟库的通用判定规则

未来遇到类似能力时，先问：

1. 是否已有广泛使用、长期维护、许可证兼容的成熟库？
2. 该库的抽象本身是否已经比 Baga 自定义 API 更成熟？
3. 能否直接采用其 API / protocol / data format？
4. 是否可以只拆用其中需要的模块？
5. 是否会把特定运行时、语言或平台错误升级成 Universal contract？
6. 是否需要 Baga 只补沙箱、路径、权限、生命周期或测试，而不是重写核心能力？

如果成熟库已经解决核心问题，默认答案应是：

> **先复用，再补 Baga 必须统一的边界。**

---

# 15. 参考依据

- SQLite: https://sqlite.org/
- LuaSQLite3 / lsqlite3: https://lua.sqlite.org/
- Automerge core: https://github.com/automerge/automerge
- Automerge Rust docs: https://docs.rs/automerge/
- Automerge Repo: https://github.com/automerge/automerge-repo
- KOReader: https://github.com/koreader/koreader
- KOReader Base: https://github.com/koreader/koreader-base
- Android SQLite APIs: Android `SQLiteDatabase` / `Context.getDatabasePath()`
- Flutter SQLite practice: `sqflite` / `getDatabasesPath()`

实际发布时必须锁定 dependency version / commit，并按许可证与 BICTS 重新验证。