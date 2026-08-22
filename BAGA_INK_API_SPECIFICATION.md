# Baga Ink API Specification

> **文档级别：一级平台规范**  
> **状态：Draft v0.1**  
> **日期：2026-08-22**  
> **上位文档：`BAGA_INK_PLATFORM_STRATEGY.md`**  
> **配套规范：`BAGA_INK_APP_STANDARD.md`、`IKP_PACKAGE_SPECIFICATION.md`**

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

本文档为 v0.1 Draft。函数名称和细节可以在实现验证中调整，但顶层命名空间、Capability-first 原则、沙箱原则、无 Vendor API 穿透原则属于稳定方向。

---

# 1. 总体设计原则

## 1.1 API namespace

公开 API 统一使用：

```lua
baga.*
```

第一阶段核心 namespace：

```lua
baga.api
baga.app
baga.ui
baga.display
baga.input
baga.device
baga.storage
baga.network
baga.power
baga.reader
baga.sync
baga.permissions
baga.log
```

## 1.2 没有 `baga.system` 万能逃生口

v0.1 不提供一个可以执行任意系统命令、获取 Android Context、调用 Kindle Shell 的通用 `baga.system` API。

原因是这样的 API 会立即破坏跨设备边界。

真正需要的新能力应该：

```text
需求
 ↓
标准 Capability
 ↓
Baga Ink API
 ↓
Device Adapter / Capability Provider
```

而不是：

```text
App
 ↓
万能 system escape hatch
 ↓
Vendor-specific implementation
```

---

# 2. Baga Lua Profile

Universal App 运行于受限的 Lua 环境。

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

v0.1 使用轻量 Task 模型。

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

Capability 命名必须稳定且语义化。

初始类别：

```text
display.*
input.*
audio.*
network.*
light.*
storage.*
bluetooth.*
power.*
reader.*
```

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

具体布局系统需要单独 UI Specification 定义。

v0.1 原则：

- App 描述 UI 状态；
- UI engine 决定实际绘制；
- Display layer 决定刷新策略；
- App 不直接操作 framebuffer。

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

用户书库等共享资源 SHOULD 通过专门 API / Permission 暴露，而不是映射成可任意遍历的真实系统目录。

---

# 12. `baga.permissions`

建议接口：

```lua
baga.permissions.check(name)
baga.permissions.request(name)
baga.permissions.list()
```

`request()` MAY 返回 Task，因为不同平台的用户授权方式不同。

应用 MUST 先在 IKP Manifest 声明权限；运行时 request 不能申请 Manifest 中不存在的权限。

示例：

```lua
if not baga.permissions.check("network") then
    local task = baga.permissions.request("network")
end
```

在某些 Kindle 环境中没有系统级 permission dialog 时，Baga Ink Platform MAY 自己实现统一授权 UI。

---

# 13. `baga.network`

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

v0.1 SHOULD 支持 HTTPS。

App MUST 不自行绕过 Platform 的 TLS / proxy / connectivity policy。

Baga Ink MAY 对后台请求实行功耗和频率限制。

---

# 14. `baga.power`

建议接口：

```lua
baga.power.battery()
baga.power.is_charging()
baga.power.request_keep_awake(opts)
baga.power.release_keep_awake(token)
```

示例：

```lua
local battery = baga.power.battery()
```

Keep-awake 是请求，不是命令。

Platform MAY 因系统策略、电量或设备能力拒绝。

---

# 15. `baga.reader`

Reader API 的目的是避免每个 App 重做 EPUB / PDF / 阅读位置 / 标注基础设施。

建议接口：

```lua
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
session:add_highlight(range, opts)
session:add_note(range, text)
session:close()
```

`source` SHOULD 是 Baga Ink 可访问的逻辑资源，而不是任意 OS 文件路径。

Reader implementation MAY 来自 KOReader、MuPDF 或其他组件，但这些内部实现不属于公开 API contract。

---

# 16. `baga.sync`

Sync API 为离线优先应用提供平台级触发与策略，不在 v0.1 定义复杂 CRDT 协议。

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

真正的数据合并语义由 App 或后续独立同步标准定义。

Platform SHOULD 提供可靠的任务调度和网络状态桥接，而不是强制所有 App 使用同一种数据模型。

---

# 17. `baga.log`

统一日志 API：

```lua
baga.log.debug(message, fields)
baga.log.info(message, fields)
baga.log.warn(message, fields)
baga.log.error(message, fields)
```

日志 MAY 被 Baga Ink Client / Developer Tools 收集。

Universal App MUST 不依赖厂商日志系统作为正常功能的一部分。

敏感用户数据 SHOULD 不写入普通日志。

---

# 18. Capability 命名规范

Capability 使用小写点分层级：

```text
category.feature
category.feature.variant
```

例如：

```text
display.partial_refresh
display.fast_refresh
display.color
input.touch
input.pen
input.physical_page_key
light.frontlight
audio.output
network.wifi
bluetooth
power.battery_level
```

Capability 名称描述“能力”，而不是实现来源。

禁止把以下形式作为标准 Capability：

```text
boox.fast_refresh
kindle.page_key
ireader.pen
```

如果厂商特性最终值得成为平台能力，应抽象成中立语义名称。

---

# 19. Permission 命名规范

Permission 同样使用稳定、语义化名称。

第一阶段候选：

```text
network
library.read
library.write
notes.read
notes.write
user_files.read
user_files.write
clipboard
audio.output
bluetooth
```

权限 SHOULD 尽量面向用户可理解的资源类别，而不是底层 OS permission 名称。

---

# 20. API 版本兼容

IKP Manifest MUST 声明 API compatibility。

建议表达：

```json
"baga_api": {
  "min": "0.1",
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

# 21. Thread / Event Loop 原则

Baga Ink 不要求 App 理解底层线程模型。

App SHOULD 把 UI handler 视为轻量事件回调。

耗时任务必须使用 Task /异步机制。

Platform MAY 在 Kindle 和 Android 使用完全不同的线程实现，但必须保持上层语义一致。

---

# 22. API 与 Device Adapter 的关系

每个公开能力都应能映射到 Device Adapter 或 Platform Core。

例如：

```text
baga.display.refresh("FAST")
          │
          ▼
Baga Ink Display Service
          │
     ┌────┴─────┐
     │          │
Kindle       Android
Adapter      Adapter
     │          │
Kindle       Vendor / Generic
refresh      refresh
```

App 永远不应该看到最后一层。

---

# 23. v0.1 API 最小闭环

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
network
permissions
power
reader
sync
```

这种顺序可以优先验证“统一平台是否真的成立”，而不是先堆功能。

---

# 24. API 设计的最终判断标准

任何新增 API 在进入 Baga Ink 之前，都应该回答四个问题：

1. 它表达的是跨设备语义，还是某厂商实现细节？
2. Kindle 与 Android E-Paper 是否都能合理实现，或至少能明确返回 `not_supported`？
3. 它是否会成为开发者绕开 Capability / Permission / Sandbox 的后门？
4. 这个 API 是否值得未来多年承担兼容责任？

如果答案不理想，宁可先做受控 Extension，也不要污染核心 API。
