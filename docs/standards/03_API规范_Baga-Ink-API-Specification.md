# Baga Ink API 规范 / Baga Ink API Specification

> **文档级别：一级平台规范**  
> **状态：Draft v0.5**  
> **日期：2026-08-23**  
> **上位文档：`01_顶层战略与架构_Baga-Ink-Platform-Strategy.md`**  
> **配套规范：`02_应用标准_Baga-Ink-App-Standard.md`、`04_能力注册表_Baga-Ink-Capability-Registry.md`、`05_权限模型_Baga-Ink-Permission-Model.md`、`06_IKP应用包规范_IKP-Package-Specification.md`、`09_UI规范_Baga-Ink-UI-Specification.md`、`13_标准库与成熟组件采用规范_Baga-Ink-Standard-Libraries-and-Adopted-Components.md`**

---

## 0. 目的

本文档定义 Baga Ink Universal App 面向的公开 `baga.*` API 边界。

目标不是复制 Android SDK，也不是把所有通用软件能力都重新包装成 `baga.*`，而是建立一套：

- 足够薄；
- 足够稳定；
- 适合墨水屏；
- 可运行于 Kindle 与 Android E-Paper；
- 不泄漏底层设备差异；
- 可长期版本化；

的统一平台接口。

必须同时理解：

```text
Baga Ink API
→ 统一设备 / OS / Platform 差异

Baga Lua Profile Standard Libraries
→ 直接采用成熟通用软件能力
```

SQLite 作为成熟跨平台数据库，通过 Baga Lua Profile Standard Library `lsqlite3` 直接提供给应用。

正式正文只描述当前有效 API；历史方案由 Git 保存。

---

# 1. 总体设计原则

## 1.1 API namespace

公开平台 API 统一使用：

```lua
baga.*
```

核心 namespace：

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

结构化关系数据直接使用 Baga Lua Profile Standard Library：

```lua
local sqlite3 = require("lsqlite3")
```

## 1.2 没有万能系统逃生口

v0.5 不提供可以执行任意系统命令、获取 Android Context、调用 Kindle Shell 的通用公开系统接口。

真正需要的新能力应该先判断性质：

```text
需求
  ↓
已有成熟通用库？
  ├─ 是 → Standard Library / Adopted Component
  └─ 否，且是设备/平台差异 → Capability / Baga Ink API
```

设备私有能力不得成为 App 绕过 Platform 的捷径。

## 1.3 公开 API 与成熟库复用

Baga Ink API 定义**开发者可依赖的平台行为契约**，不定义 Platform 内部必须使用多少层软件，也不要求底层能力重新实现。

Platform MAY 直接、组合或拆分复用成熟开源项目，例如：

```text
KOReader / koreader-base
FBInk
SQLite / lsqlite3
Automerge
MuPDF / CREngine
Android / Vendor SDK
```

但必须区分两种情况。

### A. Platform implementation detail

例如 KOReader、FBInk、Vendor SDK。App 只看到 `baga.*`。

### B. Adopted Standard Library

如果成熟库本身已经拥有适合开发者直接使用的跨平台抽象，Baga MAY 直接采用其上游 API，而不再包一层。

当前正式例子：

```text
SQLite / lsqlite3
```

因此：

- App 可以直接使用 SQL；
- App 可以直接使用 transaction / prepared statement / index / FTS；
- Baga 不把 SQLite 降级成自研 KV / collection API；
- Baga 只补平台必须统一的 path sandbox、version profile、compile options 与测试。

Automerge core 已正式采用为 Local-first / CRDT 优先基础；developer-facing Lua binding 尚未冻结，当前通过受控集成按需整体或拆模块使用。

---

# 2. Baga Lua Profile 与 Standard Libraries

Universal App 面向受限、可移植的 Baga Lua Profile。

## 2.1 基础库

建议：

```lua
string
table
math
utf8
coroutine
```

## 2.2 正式 Adopted Standard Library：`lsqlite3`

Baga Lua Profile MUST 在支持 Universal App 的 Reference Platform 上提供：

```lua
local sqlite3 = require("lsqlite3")
```

API SHOULD 与上游 LuaSQLite3 / `lsqlite3` 保持兼容，不重新命名、不重新设计 query object。

典型使用：

```lua
local sqlite3 = require("lsqlite3")
local path = baga.storage.resolve_path("appdata/app.sqlite3")
local db = sqlite3.open(path)

db:exec([[
  CREATE TABLE IF NOT EXISTS notes (
    id TEXT PRIMARY KEY,
    body TEXT NOT NULL
  )
]])
```

Platform Release 必须锁定 SQLite / lsqlite3 版本与 compile profile。详细规则见 Standard Libraries 规范。

## 2.3 Automerge 状态

`automerge/automerge` core 是正式 Adopted Foundation，可整体或拆模块用于：

```text
document / merge / history
binary persistence
sync protocol
C FFI
patches / cursors
```

当前没有冻结 developer-facing Lua module。

LifeBook / Platform 可以通过 Rust core、C FFI、LuaJIT FFI 或其他受控内部集成使用 Automerge；未来若形成成熟 Lua binding，应尽量沿用 Automerge 上游概念与格式。

## 2.4 受限库

以下库 MAY 被裁剪或包装：

```lua
os
io
package
debug
```

App MUST 不依赖：

```lua
os.execute
io.popen
load arbitrary native module
raw process spawn
raw filesystem escape
```

文件、网络、设备能力必须通过公开 Baga Ink API 获得。

---

# 3. 通用返回值与错误模型

Baga Ink API SHOULD 尽量遵循 Lua 容易理解的模式。

成功：

```lua
local value = operation()
```

可能失败的同步操作：

```lua
local value, err = operation()

if not value then
    baga.log.error(err.code, err.message)
end
```

标准错误对象建议：

```lua
{
    code = "permission_denied",
    message = "Network permission is not granted",
    recoverable = true,
    details = {}
}
```

稳定错误 code SHOULD 使用机器可读的小写 snake_case。

常见 code：

```text
not_supported
permission_denied
not_found
invalid_argument
busy
offline
timeout
cancelled
io_error
quota_exceeded
incompatible
internal_error
```

SQLite 自身错误可由 `lsqlite3` 按其成熟 API 暴露；App 不应把 SQLite 错误当作设备能力错误。

---

# 4. 异步任务模型

网络、同步、耗时 Reader 操作等不应阻塞 UI。

v0.5 使用轻量 Task 模型。

概念接口：

```lua
local task = baga.network.request({...})

task:on_success(function(response)
end)

task:on_error(function(err)
end)

task:on_complete(function()
end)
```

Task SHOULD 支持：

```lua
task:cancel()
task:is_done()
```

在允许 coroutine await 的上下文中，SDK MAY 提供：

```lua
local result, err = task:await()
```

`await()` 不能阻塞底层 UI 事件循环。

---

# 5. `baga.api`

用于 API 版本协商与特性检测。

建议接口：

```lua
baga.api.version()
baga.api.has(feature)
baga.api.standard_library(name)
```

`standard_library(name)` MAY 返回当前 Platform 对正式 Standard Library 的版本描述，例如：

```lua
{
    name = "lsqlite3",
    version = "0.9.7",
    sqlite_version = "3.53.4"
}
```

实际版本由 Platform Release 决定，示例不构成永久冻结值。

---

# 6. `baga.app`

应用身份与生命周期。

建议接口：

```lua
baga.app.info()
baga.app.on(event_name, handler)
baga.app.quit()
```

第一阶段事件：

```text
start
resume
pause
sleep
wake
stop
update
```

App 不假设进程永久存在。

---

# 7. `baga.device`

跨设备兼容查询。

建议接口：

```lua
baga.device.info()
baga.device.has(capability)
baga.device.capabilities()
```

Universal App 的核心业务逻辑 SHOULD 不依赖具体 family / model。

SQLite / lsqlite3 不是 Device Capability。

---

# 8. `baga.ui`

Baga Ink UI 是面向墨水屏的轻量 UI API。

第一阶段组件方向：

```lua
baga.ui.page(opts)
baga.ui.text(opts)
baga.ui.image(opts)
baga.ui.button(opts)
baga.ui.list(opts)
baga.ui.menu(opts)
baga.ui.dialog(opts)
baga.ui.toolbar(opts)
```

UI 对象 SHOULD 支持：

```lua
view:show()
view:hide()
view:update(props)
view:invalidate()
view:focus()
```

具体布局、Focus、刷新行为以 UI Specification 为准。

---

# 9. `baga.display`

Display API 表达刷新意图，不暴露厂商 waveform ID。

建议接口：

```lua
baga.display.size()
baga.display.mode(mode)
baga.display.refresh(opts)
baga.display.invalidate(region)
baga.display.has(mode_or_feature)
```

模式：

```text
AUTO
TEXT
QUALITY
FAST
ANIMATION
```

App MUST 把 mode 理解为目标效果，而不是硬件保证。

---

# 10. `baga.input`

Input API 同时支持硬件事件与语义动作。

建议接口：

```lua
baga.input.on(event_or_action, handler)
baga.input.off(token)
baga.input.has(input_type)
```

语义动作：

```text
page_next
page_previous
confirm
back
menu
```

Universal App SHOULD 优先监听语义动作，而不是硬编码平台 keycode。

---

# 11. `baga.storage`

`baga.storage` 负责文件 / 字节资源、逻辑路径与沙箱桥接；它不是数据库 API。

建议接口：

```lua
baga.storage.read_text(path)
baga.storage.write_text(path, text)
baga.storage.read_bytes(path)
baga.storage.write_bytes(path, bytes)
baga.storage.exists(path)
baga.storage.list(path)
baga.storage.mkdir(path)
baga.storage.remove(path)
baga.storage.move(from, to)
baga.storage.copy(from, to)
baga.storage.resolve_path(path)
```

逻辑根：

```text
appdata/
cache/
documents/
downloads/
```

## 11.1 `resolve_path()`

用于需要真实平台路径的正式 Standard Library / native-backed library，例如 SQLite。

```lua
local path = baga.storage.resolve_path("appdata/lifebook.sqlite3")
```

规则：

- 只允许解析当前 App 已授权逻辑路径；
- MUST 进行路径规范化和 sandbox 检查；
- 返回值只用于当前设备运行时，不得作为跨设备持久业务 ID；
- App 不应推断路径中的 Vendor / OS 结构；
- Kindle 等缺乏 per-App OS sandbox 的环境必须由 Platform 通过校验、受限 VFS 或等价机制确保数据库无法逃逸；
- Android 等强 OS sandbox 平台可以同时依靠 OS sandbox。

`resolve_path()` 不是万能 raw filesystem escape hatch。

---

# 12. `baga.library`

`baga.library` 是用户可见书籍 / 文档资源的标准书库接口。

概念接口：

```lua
baga.library.list(opts)
baga.library.get(item_id)
baga.library.open(item_id)
baga.library.import(source, opts)
baga.library.remove(item_id, opts)
```

Library Item 使用稳定、opaque 的 `item_id`，不暴露真实系统路径。

规则：

- `list/get/open` 受 `library.read` Permission 控制；
- `import/remove` 受 `library.write` Permission 控制；
- `open()` SHOULD 返回可传给 `baga.reader.open()` 的逻辑 source / handle；
- Universal App MUST 不扫描 Kindle `/documents`、Android vendor bookshelf 或真实 filesystem path；
- 不限定 EPUB 或任何单一文档格式。

---

# 13. `baga.permissions`

建议接口：

```lua
baga.permissions.check(name)
baga.permissions.request(name)
baga.permissions.list()
```

应用 MUST 先在 IKP Manifest 声明权限。

SQLite database 位于 App 自己的 sandbox 时，不需要额外用户数据权限。

---

# 14. `baga.network`

建议接口：

```lua
baga.network.state()
baga.network.request(opts)
baga.network.is_online()
```

v0.5 SHOULD 支持 HTTPS。

App MUST 不自行绕过 Platform 的 TLS / proxy / connectivity policy。

---

# 15. `baga.power`

建议接口：

```lua
baga.power.battery()
baga.power.is_charging()
baga.power.request_keep_awake(opts)
baga.power.release_keep_awake(token)
```

Keep-awake 是请求，不是命令。

---

# 16. `baga.reader`

Reader API 的目的是避免每个 App 重做**文档打开、格式处理、阅读位置、选择、搜索、标注和锚点定位基础设施**。

Baga Ink Reader 不以 EPUB 为中心。

建议接口：

```lua
baga.reader.supports(source_or_format)
baga.reader.open(source, opts)
```

返回 Reader Session：

```lua
session:position()
session:goto(position)
session:next_page()
session:previous_page()
session:search(query)
session:get_selection()
session:create_anchor(target)
session:goto_anchor(anchor)
session:resolve_anchor(anchor)
session:add_highlight(range, opts)
session:add_note(range, text)
session:close()
```

## 16.1 Reader Position 与 Anchor

定位算法归 Reader implementation；App 只保存和传递 Baga Reader 返回的可序列化位置对象。

Platform / Reader implementation MAY 在内部复用：

```text
KOReader / CREngine XPointer-like position
PDF page + page-local position / boxes
固定页文档 page / region
其他 Reader 原生 locator
quote / context / progression fallback evidence
```

Readium Locator、EPUB CFI、W3C Web Annotation MAY 作为设计参考，但任何单一体系都不是 Baga Reader 默认格式边界。

## 16.2 Reader 实现边界

Reader implementation MAY 来自 KOReader、MuPDF、CREngine 或其他成熟组件，也 MAY 组合复用它们。

这些内部实现不属于公开 API contract。

---

# 17. `baga.sync`

`baga.sync` 为离线优先应用提供平台级同步**触发、调度与设备策略**。

建议接口：

```lua
baga.sync.state()
baga.sync.trigger(name, opts)
baga.sync.on(event, handler)
```

策略 MAY 包括：

```text
when_online
wifi_only
when_charging
manual
```

必须区分：

```text
SQLite / lsqlite3
→ 本地关系数据 / transaction / query / index / FTS

baga.sync
→ 联网状态、同步任务触发、功耗/网络策略和生命周期协调

Automerge core（适用时）
→ concurrent local-first state / CRDT merge / history / optional sync protocol

App Domain Logic
→ authoritative policy、对象身份、业务规则
```

Automerge core 可整体或拆模块采用。

Baga v0.5 不规定所有 App 必须使用 Automerge，也不把 `automerge-repo` 的 Storage/Network Adapter 架构变成 Baga 公共架构。

如果未来需要多个独立实现直接交换 Automerge binary/sync protocol，必须锁定明确版本和迁移规则。

---

# 18. `baga.log`

统一日志 API：

```lua
baga.log.debug(message, fields)
baga.log.info(message, fields)
baga.log.warn(message, fields)
baga.log.error(message, fields)
```

敏感用户数据 SHOULD 不写入普通日志。

---

# 19. Capability 命名规范

Capability 使用小写点分层级。

正式 Capability 集合由 Capability Registry 维护。

禁止标准 Capability 使用厂商品牌名或内部库名。

SQLite / lsqlite3 / Automerge 不作为 Device Capability 名称。

---

# 20. Permission 命名规范

Permission 使用稳定、语义化名称，正式注册表由 Permission Model 维护。

---

# 21. API 版本兼容

IKP Manifest MUST 声明 API compatibility。

建议表达：

```json
"baga_api": {
  "min": "0.5",
  "max_exclusive": "1.0"
}
```

Standard Library compatibility 由 Baga Lua Profile / Platform Release 另外记录。

进入稳定 major 后：

- Minor SHOULD 只增加向后兼容能力；
- Patch MUST 不引入 breaking API；
- Breaking change 应进入新的 major；
- Deprecated API 应保留合理迁移周期。

---

# 22. Thread / Event Loop 原则

Baga Ink 不要求 App 理解底层线程模型。

耗时任务必须使用 Task / 异步机制。

SQLite transaction 是应用本地同步调用语义，App 应避免在 UI handler 中运行明显耗时的大查询或 migration。

---

# 23. API、Standard Library 与 Device Adapter 的关系

三者不能混淆：

```text
baga.display
→ Device / OS 差异
→ Platform / Adapter 实现

lsqlite3
→ 成熟通用数据库库
→ 直接使用上游 API
→ Platform 提供 pinned runtime + safe path

Automerge core
→ Adopted mature foundation
→ Platform/App 按需整用或拆用
```

---

# 24. v0.5 API 最小闭环

第一批：

```text
baga.api
baga.app
baga.device
baga.ui
baga.display
baga.input
baga.storage
baga.log
```

第二批：

```text
baga.library
baga.network
baga.permissions
baga.power
baga.reader
baga.sync
```

同时 Baga Lua Profile Reference Platform SHOULD 验证：

```text
lsqlite3 + pinned SQLite
```

Automerge core 的采用范围按具体功能和硬件验证逐步扩大。

---

# 25. API 设计的最终判断标准

任何新增 `baga.*` API 在进入 Baga Ink 之前，都应该回答：

1. 它表达的是设备 / OS / Platform 差异，还是一个已有成熟通用库已经解决的问题？
2. 如果是成熟通用库，是否应该直接纳入 Standard Library，而不是再包一层？
3. Kindle 与 Android E-Paper 是否都能合理实现，或至少明确 `not_supported`？
4. 是否会成为绕开 Capability / Permission / Sandbox 的后门？
5. 是否值得未来多年承担兼容责任？
6. 是否有成熟、许可证兼容、可验证的实现可以整体或部分复用？
7. 采用成熟实现时，是否可以保持它优秀的上游语义，而不是发明更弱的平台私有对象模型？

原则：

> **能直接采用成熟标准库的，就直接采用；真正需要统一设备差异的，才进入 Baga Ink API。**
