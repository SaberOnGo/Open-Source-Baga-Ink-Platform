# Baga Ink API 规范 / Baga Ink API Specification

> **文档级别：一级平台规范**  
> **状态：Draft v0.3**  
> **日期：2026-08-23**  
> **上位文档：`01_顶层战略与架构_Baga-Ink-Platform-Strategy.md`**  
> **配套规范：`02_应用标准_Baga-Ink-App-Standard.md`、`04_能力注册表_Baga-Ink-Capability-Registry.md`、`05_权限模型_Baga-Ink-Permission-Model.md`、`06_IKP应用包规范_IKP-Package-Specification.md`、`09_UI规范_Baga-Ink-UI-Specification.md`**

---

## 0. 目的

本文档定义 Baga Ink Universal App 面向的公开 API 边界。

目标不是复制 Android SDK，而是建立一套：

- 足够薄；
- 足够稳定；
- 适合墨水屏；
- 可运行于 Kindle 与 Android E-Paper；
- 不泄漏底层设备差异；
- 可长期版本化；

的统一应用接口。

本文档为 v0.3 Draft。函数名称和细节可以在实现验证中调整，但顶层命名空间、Capability-first 原则、沙箱原则、无 Vendor API 穿透原则以及“公开语义与内部实现分离”属于稳定方向。

---

# 1. 总体设计原则

## 1.1 API namespace

公开 API 统一使用：

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
baga.data
baga.library
baga.network
baga.power
baga.reader
baga.sync
baga.permissions
baga.log
```

## 1.2 没有 `baga.system` 万能逃生口

v0.3 不提供一个可以执行任意系统命令、获取 Android Context、调用 Kindle Shell 的通用 `baga.system` API。

原因是这样的 API 会立即破坏跨设备边界。

真正需要的新能力应该：

```text
需求
 ↓
标准 Capability / API 语义
 ↓
Baga Ink API
 ↓
Platform Core / Device Adapter 内部实现
```

而不是：

```text
App
 ↓
万能 system escape hatch
 ↓
Vendor-specific implementation
```

## 1.3 公开 API 与内部实现复用

Baga Ink API 定义**开发者可依赖的行为契约**，不定义 Platform 内部必须使用多少层软件，也不要求底层能力重新实现。

Platform MAY 直接、组合或拆分复用成熟开源项目，例如：

```text
KOReader / koreader-base
FBInk
SQLite
Automerge
MuPDF / CREngine
Android / Vendor SDK
其他经过验证的成熟组件
```

但：

- 使用某个组件 MUST NOT 自动产生新的公开 `Provider / Engine / Runtime` 层；
- App MUST NOT 因内部采用 KOReader 而依赖 KOReader Lua 对象；
- App MUST NOT 因内部采用 SQLite 而依赖 SQL、数据库路径或 SQLite-specific pragma；
- App MUST NOT 因内部采用 Automerge 而被强制理解 Automerge change graph、binary format 或 Sync Protocol；
- 只有被本规范或其他正式 Baga Ink 标准明确采纳并版本化的外部协议，才属于稳定跨实现契约。

原则：

> **`baga.*` 是稳定边界；成熟开源库是实现工具，不是自动新增的架构层。**

---

# 2. Baga Lua Profile

Universal App 面向受限、可移植的 Baga Lua Profile。

## 2.1 默认可用基础库

建议：

```lua
string
table
math
utf8
coroutine
```

## 2.2 受限库

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

文件、网络、设备、进程级能力必须通过公开 Baga Ink API 获得。

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

应用 MUST 不依赖厂商原始错误码作为业务逻辑。

---

# 4. 异步任务模型

网络、同步、耗时 Reader 操作等不应阻塞 UI。

v0.3 使用轻量 Task 模型。

概念接口：

```lua
local task = baga.network.request({...})

task:on_success(function(response)
    -- handle response
end)

task:on_error(function(err)
    -- handle error
end)

task:on_complete(function()
    -- optional cleanup
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
```

示例：

```lua
local version = baga.api.version()

if baga.api.has("reader.highlight") then
    -- enable highlight feature
end
```

IKP Manifest 中声明的 API version 是安装/启动前兼容判断的主要依据；运行时 feature query 用于更细粒度兼容。

---

# 6. `baga.app`

应用身份与生命周期。

建议接口：

```lua
baga.app.info()
baga.app.on(event_name, handler)
baga.app.quit()
```

`baga.app.info()` 返回：

```lua
{
    id = "com.example.reader",
    name = "Example Reader",
    version = "1.0.0"
}
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

示例：

```lua
baga.app.on("sleep", function()
    save_state()
end)

baga.app.on("wake", function()
    refresh_connectivity()
end)
```

`install` / `uninstall` 是否直接暴露给普通应用代码应谨慎；平台 SHOULD 避免让卸载代码拥有扩大权限。

---

# 7. `baga.device`

这是跨设备兼容最重要的 API 之一。

建议接口：

```lua
baga.device.info()
baga.device.has(capability)
baga.device.capabilities()
```

示例：

```lua
if baga.device.has("display.fast_refresh") then
    enable_fast_navigation()
end
```

`baga.device.info()` MAY 返回用于显示或诊断的信息：

```lua
{
    family = "kindle",
    model = "...",
    platform = "..."
}
```

但 Universal App 的核心业务逻辑 SHOULD 不依赖 `family` / `model`。

Capability 命名以 `04_能力注册表_Baga-Ink-Capability-Registry.md` 为唯一注册来源。

---

# 8. `baga.ui`

Baga Ink UI 是面向墨水屏的轻量 UI 层。

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

典型用法：

```lua
local page = baga.ui.page({
    title = "Library"
})

page:add(baga.ui.text({
    text = "Hello Ink"
}))

page:show()
```

UI 对象 SHOULD 支持：

```lua
view:show()
view:hide()
view:update(props)
view:invalidate()
view:focus()
```

具体布局、Focus、刷新行为以 `09_UI规范_Baga-Ink-UI-Specification.md` 为准。

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

示例：

```lua
baga.display.mode("TEXT")
baga.display.refresh({ full = false })
```

局部刷新：

```lua
baga.display.refresh({
    region = { x = 0, y = 0, width = 600, height = 120 },
    mode = "FAST"
})
```

Platform MAY 根据设备约束忽略或调整 App 的具体请求。

App MUST 把 mode 理解为“目标效果”，而不是硬件保证。

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

原始输入类别：

```text
touch
pen
keyboard
physical_button
```

示例：

```lua
baga.input.on("page_next", function()
    reader:next_page()
end)
```

Universal App SHOULD 优先监听语义动作，而不是硬编码平台 keycode。

---

# 11. `baga.storage`

`baga.storage` 负责文件 / 字节级逻辑存储；它不是结构化数据库 API。

所有路径均为 Baga Ink 逻辑路径，不等价于真实 OS 路径。

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
```

示例：

```lua
local text, err = baga.storage.read_text("appdata/settings.json")
```

逻辑根：

```text
appdata/
cache/
documents/
downloads/
```

用户书库等共享资源 SHOULD 通过 `baga.library` / 专门 API 与 Permission 暴露，而不是映射成可任意遍历的真实系统目录。

---

# 12. `baga.data`

`baga.data` 为 offline-first App 提供**应用私有的结构化、事务型、可靠本地数据**。

它解决的是：

> **数据在当前设备上如何可靠落盘、原子修改和崩溃恢复。**

它不等于：

```text
云同步
CRDT
冲突合并
远程数据库
文件系统
```

概念接口：

```lua
local store = baga.data.open("main")

store:get(collection, key)
store:put(collection, key, value)
store:delete(collection, key)
store:list(collection, opts)
store:transaction(function(tx)
    -- tx:get / tx:put / tx:delete
end)
```

v0.3 原则：

- `transaction()` SHOULD 提供 all-or-nothing 原子语义；
- API 返回成功前，平台 SHOULD 保证该事务已经达到平台承诺的持久化边界；
- App 崩溃或设备重启后，不得出现“半个事务”；
- Value SHOULD 使用 Baga 可序列化的结构化类型；
- 大型二进制对象 SHOULD 使用 `baga.storage`，而不是塞入结构化记录；
- App 数据默认属于自身沙箱，不需要额外用户权限；
- Platform 更新不得默认清除 App Data。

实现上，Platform SHOULD 优先复用 SQLite 等成熟事务存储，而不是自行发明数据库；Android 与 Kindle 可以使用不同内部实现，只要 API 语义一致。

App MUST NOT 假设底层一定是 SQLite，也不得依赖 SQL、真实数据库路径、WAL 文件或 SQLite-specific 行为。

---

# 13. `baga.library`

`baga.library` 是用户可见书籍 / 文档资源的标准书库接口，用来解决当前 `storage.user_library` Capability 与 `library.read/write` Permission 已存在、但公开 API 缺失的问题。

概念接口：

```lua
baga.library.list(opts)
baga.library.get(item_id)
baga.library.open(item_id)
baga.library.import(source, opts)
baga.library.remove(item_id, opts)
```

书库 Item SHOULD 使用稳定、opaque 的 `item_id`，而不是公开真实系统路径。

概念描述：

```lua
{
    id = "opaque-library-id",
    title = "...",
    authors = {"..."},
    media_type = "...",
    format = "...",
    size = 123456,
    modified_at = "..."
}
```

规则：

- `list/get/open` 受 `library.read` Permission 控制；
- `import/remove` 等修改操作受 `library.write` Permission 控制；
- `open()` SHOULD 返回可传给 `baga.reader.open()` 的逻辑 source / handle；
- Universal App MUST 不扫描 Kindle `/documents`、Android vendor bookshelf 或真实 filesystem path；
- Device Adapter 可以在内部索引厂商书库，但 App 只看到统一 Library Item；
- `storage.user_library` Capability 表示 Platform 可以桥接设备现有用户书库；它不是 `baga.library` namespace 本身是否存在的同义词。

`baga.library` 不限定 EPUB，也不限定任何单一文件格式。实际可打开格式由 Reader implementation 与 `baga.reader.supports()` 判断。

---

# 14. `baga.permissions`

建议接口：

```lua
baga.permissions.check(name)
baga.permissions.request(name)
baga.permissions.list()
```

`request()` MAY 返回 Task，因为不同平台的用户授权方式不同。

应用 MUST 先在 IKP Manifest 声明权限；运行时 request 不能申请 Manifest 中不存在的权限。

权限正式定义以 `05_权限模型_Baga-Ink-Permission-Model.md` 为准。

---

# 15. `baga.network`

建议接口：

```lua
baga.network.state()
baga.network.request(opts)
baga.network.is_online()
```

请求示例：

```lua
local task = baga.network.request({
    method = "GET",
    url = "https://example.com/data",
    headers = {},
    timeout_ms = 15000
})
```

响应对象建议：

```lua
{
    status = 200,
    headers = {},
    body = "..."
}
```

v0.3 SHOULD 支持 HTTPS。

App MUST 不自行绕过 Platform 的 TLS / proxy / connectivity policy。

Baga Ink MAY 对后台请求实行功耗和频率限制。

---

# 16. `baga.power`

建议接口：

```lua
baga.power.battery()
baga.power.is_charging()
baga.power.request_keep_awake(opts)
baga.power.release_keep_awake(token)
```

Keep-awake 是请求，不是命令。

Platform MAY 因系统策略、电量或设备能力拒绝。

---

# 17. `baga.reader`

Reader API 的目的是避免每个 App 重做**文档打开、格式处理、阅读位置、选择、搜索、标注和锚点定位基础设施**。

Baga Ink Reader 不以 EPUB 为中心，也不把任何单一格式或单一 Locator 体系作为 Reader 抽象本身。

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

`source` SHOULD 是 Baga Ink 可访问的逻辑资源，而不是任意 OS 文件路径。

## 17.1 Reader Position 与 Anchor

Reader Position / Anchor 用于：

```text
恢复阅读位置
高亮 / 笔记定位
跨设备阅读同步
公开笔记关联正文
重新打开文档后的定位恢复
```

它的标准原则是：

> **定位算法归 Reader implementation；App 只保存和传递 Baga Reader 返回的可序列化位置对象。**

App MUST 把 Anchor 视为 opaque、可序列化的 Baga 值，不解析其中的 Reader-engine 私有字段。

Platform / Reader implementation MAY 在内部复用最适合当前格式的成熟定位机制，例如：

```text
KOReader / CREngine XPointer 类位置
PDF page + page-local position / boxes
固定页文档 page / region
其他 Reader 已有原生 locator
quote / context / progression 等恢复证据
```

KOReader 当前对 reflowable / rolling 文档与 fixed-page / paging 文档本来就使用不同的成熟位置模型；Baga Ink SHOULD 复用这些既有能力，而不是为 EPUB、PDF、MOBI、FB2、TXT、DjVu、CBZ 等格式分别重新发明定位算法。

Readium Locator、EPUB CFI、W3C Web Annotation 等 MAY 作为数据模型与恢复策略的设计参考，但 **任何单一外部体系都不是 Baga Reader 的默认格式边界或强制实现。**

如果某个 Anchor 在另一 Reader implementation 中无法精确解析，Platform SHOULD 按标准化恢复策略尝试已有 fallback evidence；无法可靠恢复时必须返回明确错误或降级结果，不能伪造“精确定位”。

## 17.2 Reader 实现边界

Reader implementation MAY 来自 KOReader、MuPDF、CREngine 或其他成熟组件，也 MAY 组合复用它们。

这些内部实现不属于公开 API contract。

特别是：

```text
LifeBook / IKP
      ↓
baga.reader
      ↓
Baga Ink Platform on current device
      ↓
内部复用 KOReader / MuPDF / CREngine / other implementation
```

内部库不构成一层新的公开架构。

---

# 18. `baga.sync`

`baga.sync` 为离线优先应用提供平台级同步**触发、调度与设备策略**，不把所有 App 强制到一种 CRDT 或业务合并算法。

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
baga.data
→ 当前设备上的可靠本地事务数据

baga.sync
→ 联网状态、同步任务触发、功耗/网络策略和生命周期协调

App Domain Sync Logic
→ 哪些对象同步、幂等、版本历史、业务冲突规则
```

对于确实存在**多设备并发离线修改**的数据，Platform / App implementation SHOULD 优先评估 Automerge 等成熟 Local-first / CRDT 实现，而不是自行发明通用 CRDT 算法。

但 Automerge 不适用于所有数据：

- 阅读进度可以采用简单、明确的业务 merge；
- Server-authoritative Feed / 评论 / 他人公开笔记通常只需要本地 cache；
- 书籍文件同步适合内容 Hash / 文件传输；
- 笔记、人生记录、文章草稿等并发可编辑对象才可能真正需要 CRDT。

Baga Ink v0.3 不规定所有 App 必须使用 Automerge，也不把 Automerge 私有对象直接暴露给 IKP。

如果未来需要让多个独立实现直接交换同一种 CRDT wire format，必须通过独立、版本化标准明确采用的外部协议版本与迁移规则；不能用“依赖最新版 Automerge”代替规范。

---

# 19. `baga.log`

统一日志 API：

```lua
baga.log.debug(message, fields)
baga.log.info(message, fields)
baga.log.warn(message, fields)
baga.log.error(message, fields)
```

日志 MAY 被 Baga Ink Client / Developer Tools 收集。

敏感用户数据 SHOULD 不写入普通日志。

---

# 20. Capability 命名规范

Capability 使用小写点分层级：

```text
category.feature
category.feature.variant
```

正式 Capability 集合由 `04_能力注册表_Baga-Ink-Capability-Registry.md` 维护。

禁止标准 Capability 使用：

```text
boox.*
kindle.*
ireader.*
```

如果厂商特性值得成为平台能力，应抽象成中立语义名称。

---

# 21. Permission 命名规范

Permission 同样使用稳定、语义化名称，正式注册表由 `05_权限模型_Baga-Ink-Permission-Model.md` 维护。

---

# 22. API 版本兼容

IKP Manifest MUST 声明 API compatibility。

建议表达：

```json
"baga_api": {
  "min": "0.3",
  "max_exclusive": "1.0"
}
```

在 v0.x 期间允许快速演进。

进入稳定 major 后：

- Minor SHOULD 只增加向后兼容能力；
- Patch MUST 不引入 breaking API；
- Breaking change 应进入新的 major；
- Deprecated API 应保留合理迁移周期。

Platform MUST 在 App 启动前做版本检查。

---

# 23. Thread / Event Loop 原则

Baga Ink 不要求 App 理解底层线程模型。

App SHOULD 把 UI handler 视为轻量事件回调。

耗时任务必须使用 Task / 异步机制。

Platform MAY 在 Kindle 和 Android 使用完全不同的线程实现，但必须保持上层语义一致。

---

# 24. API 与 Device Adapter 的关系

每个公开能力都应能映射到 Platform Core、Device Adapter 或二者协作的内部实现。

例如：

```text
baga.display.refresh("FAST")
          │
          ▼
Baga Ink Platform
          │
     ┌────┴─────┐
     │          │
Kindle       Android
Adapter      Adapter
     │          │
Kindle       Vendor / Generic
refresh      refresh
```

又例如：

```text
baga.data
   ↓
Platform Core
   ↓
SQLite / other mature transactional storage
```

`baga.data` 不需要为了 SQLite 再产生一个公开 “SQLite Provider Layer”。

App 永远不应该看到最后一层具体实现。

---

# 25. v0.3 API 最小闭环

Reference Implementation 的第一阶段不需要一次实现全部 API。

最小可验证闭环 SHOULD 是：

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

然后用同一个简单 `.ikp` Demo 在：

```text
Kindle Reference Device
+
Android E-Paper Reference Device
```

运行成功。

第二批再加入：

```text
baga.data
baga.library
baga.network
baga.permissions
baga.power
baga.reader
baga.sync
```

---

# 26. API 设计的最终判断标准

任何新增 API 在进入 Baga Ink 之前，都应该回答：

1. 它表达的是跨设备语义，还是某厂商实现细节？
2. Kindle 与 Android E-Paper 是否都能合理实现，或至少能明确返回 `not_supported`？
3. 它是否会成为开发者绕开 Capability / Permission / Sandbox 的后门？
4. 这个 API 是否值得未来多年承担兼容责任？
5. 这个需求是否已经有成熟、许可证兼容、可验证的实现可以直接或部分复用，从而避免重新造轮子？
6. 采用该开源实现时，能否保持 `baga.*` 契约稳定，而不把其私有对象模型泄漏给 App？

如果答案不理想，宁可先做受控 Extension，也不要污染核心 API。