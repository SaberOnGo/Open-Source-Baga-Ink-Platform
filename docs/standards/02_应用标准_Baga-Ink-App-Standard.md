# Baga Ink 应用标准 / Baga Ink App Standard

> **文档级别：一级平台规范**  
> **状态：Draft v0.6**  
> **日期：2026-08-23**  
> **上位文档：`01_顶层战略与架构_Baga-Ink-Platform-Strategy.md`**  
> **配套规范：`03_API规范_Baga-Ink-API-Specification.md`、`04_能力注册表_Baga-Ink-Capability-Registry.md`、`05_权限模型_Baga-Ink-Permission-Model.md`、`06_IKP应用包规范_IKP-Package-Specification.md`、`09_UI规范_Baga-Ink-UI-Specification.md`、`13_标准库与成熟组件采用规范_Baga-Ink-Standard-Libraries-and-Adopted-Components.md`**

---

## 0. 目的

本文档定义第三方应用如何成为一个 **Baga Ink App**，以及什么条件下可以获得 **Baga Ink Universal** 兼容标识。

本标准的首要目标不是提供最多能力，而是建立一个长期稳定的跨设备应用边界，防止 Baga Ink 生态在扩张后重新碎片化。

本规范约束应用开发者；设备厂商与适配层的要求由 Baga Ink Compatibility Standard / Device Adapter Specification 另行定义。

本文中的 MUST / SHOULD / MAY 含义继承顶层战略文档。

正式正文只描述当前有效设计；历史方案由 Git 保存。

---

# 1. 应用类别

Baga Ink 定义三类应用/扩展。

## 1.1 Baga Ink Universal App

Universal App 是平台默认、优先和最重要的应用形态。

Universal App MUST：

- 使用 Baga Lua Profile；
- 以 `.ikp` 包格式发布；
- 仅通过 Baga Ink API 获取设备 / OS / Platform 能力；
- 可以直接使用 Baga Lua Profile 正式 Standard Libraries；
- 使用 Capability Model 判断硬件能力；
- 遵守标准生命周期；
- 遵守权限与沙箱；
- 不直接访问 Vendor / OS 私有 API；
- 不携带平台相关 native binary 作为正常应用逻辑；
- 不携带针对某一设备的 Lua 解释器、设备桥或私有执行组件；
- 不要求开发者为 Kindle、BOOX、iReader 等分别维护应用逻辑分支。

符合全部要求并通过兼容测试的应用 MAY 标记：

> **Baga Ink Universal**

## 1.2 Device Enhanced App

Device Enhanced App 仍以 Baga Ink API 为主要开发边界，但 MAY 使用由 Platform 暴露的标准化扩展 Capability。

例如：

```text
input.pen.low_latency
display.fast_refresh
audio.tts
```

Enhanced App MUST：

- 明确声明 required / optional capabilities；
- 对缺失的 optional capability 优雅降级；
- 不绕开 Platform 直接调用厂商 SDK；
- 在 Baga Ink Market 中清晰显示增强范围。

## 1.3 Native Extension / Capability Provider

Native Extension 用于扩展 Platform 能力，不作为普通 Universal App 的逃生口。

Native Extension MAY 使用：

- Rust；
- C / C++；
- Kotlin / Java；
- JNI；
- Kindle native / shell integration；
- Vendor SDK。

但它必须由 Platform 以受控 Capability 的形式重新暴露给 App。

**内部使用成熟开源库本身不等于 Native Extension，也不意味着每个库都需要一个 Capability Provider。** Platform 可以在现有 Core / Adapter 实现中直接、组合或拆分复用成熟组件。

---

# 2. 应用身份

每个 Baga Ink App MUST 拥有全局稳定的 Application ID。

推荐格式：

```text
com.example.reader
org.example.notes
```

Application ID：

- MUST 由发布者长期控制；
- MUST 在应用更新中保持不变；
- MUST 不强制使用 `baga.*`；
- MUST 不因为运行设备不同而改变；
- SHOULD 与开发者控制的域名或命名空间相关。

---

# 3. 版本与兼容范围

应用版本 SHOULD 使用语义化版本形式：

```text
MAJOR.MINOR.PATCH
```

应用 MUST 在 IKP Manifest 中声明：

- app version；
- IKP format version；
- 所需 Baga Ink API version；
- required capabilities；
- optional capabilities。

Platform MUST 在启动应用前完成兼容检查。

Standard Libraries 的版本由 Baga Platform / Lua Profile 版本锁定并可查询，不要求每个 IKP 自带 native copy。

---

# 4. Baga Lua Profile

Universal App 的第一官方语言为 Lua，但应用不是面向“任意 Lua 环境”，而是面向 **Baga Lua Profile**。

Baga Lua Profile 是语言、Standard Libraries 与 API 的规范边界，不是一个需要用户单独安装或管理的产品层。

Platform Core 内部 MAY：

- 在 Kindle 上复用 KOReader 等现有项目已经验证过的 Lua / LuaJIT 能力；
- 在 Android 上嵌入轻量 Lua 解释器；
- 未来替换底层 Lua 实现，只要保持 Baga Lua Profile 兼容。

第三方 App 不得依赖具体 Lua 解释器品牌、编译方式或设备实现。

## 4.1 基础库

Baga Lua Profile SHOULD 提供安全、可移植的基础库，例如：

```text
string
table
math
utf8
coroutine
```

具体 Lua 版本由 SDK 版本定义。

## 4.2 Adopted Standard Libraries

Baga Ink 不要求所有通用能力都重新包装成 `baga.*`。

如果上游库本身已经具有成熟、稳定、跨平台的抽象，Baga MAY 将其直接纳入 Baga Lua Profile Standard Libraries。

当前正式数据库标准库：

```lua
local sqlite3 = require("lsqlite3")
```

开发者直接使用成熟 SQLite 语义：

```text
SQL
schema
prepared statement
transaction
index
foreign key
BLOB
FTS
JSON
```

Baga 不在 SQLite 上重新发明 KV / collection 数据库 API。

Automerge core 已被 Baga 正式采纳为 Local-first / CRDT 优先基础；可整体采用，也可拆用 document/merge、binary persistence、sync protocol、C FFI、patch/cursor 等模块。developer-facing Lua binding 当前仍为 provisional；在成熟接口确定前，Platform / App 通过受控集成使用 Automerge。

详细规则见 `13_标准库与成熟组件采用规范_Baga-Ink-Standard-Libraries-and-Adopted-Components.md`。

## 4.3 默认禁止的系统逃逸能力

Universal App MUST 不依赖：

```text
os.execute
io.popen
raw shell
raw process spawn
raw filesystem outside sandbox
Android Context
Java reflection
direct JNI
Kindle private framework
raw framebuffer
direct vendor SDK
/proc
/sys
```

`os`、`io`、`package`、`debug` 等 Lua 标准库中的危险部分 MAY 被 Platform 删除、替换或限制。

应用不得假设标准桌面 Lua 的完整库集合存在。

SQLite loadable native extension 默认不得成为绕过 IKP native-code / sandbox 限制的入口。

---

# 5. 应用生命周期

Baga Ink App MUST 使用统一生命周期模型。

第一阶段语义事件：

```text
install
start
resume
pause
sleep
wake
stop
update
uninstall
```

应用 MUST：

- 在 `sleep` 前快速保存必要状态；
- 不假设网络长期在线；
- 不假设进程永久驻留；
- 不依赖 Android Activity 或 Kindle 私有进程模型；
- 在 `wake` 后重新验证网络与设备能力状态。

Platform MAY 因设备限制合并某些底层事件，但对 App 暴露的语义必须保持一致。

---

# 6. Capability Model

## 6.1 基本原则

应用 MUST 查询“设备 / Platform 具有什么能力”，而不是“设备是什么品牌”或“底层用了什么库”。

推荐：

```lua
if baga.device.has("input.pen") then
    enable_pen_ui()
end

if baga.device.has("reader.anchor") then
    enable_anchor_navigation()
end
```

不推荐：

```lua
if device.vendor == "BOOX" then ... end
if reader_impl == "KOReader" then ... end
```

SQLite / lsqlite3 不是设备 Capability；它是 Baga Lua Profile Standard Library。

## 6.2 Required Capability

如果应用没有某能力就无法工作，应在 Manifest 中声明 required capability。

Platform MUST 在安装或启动前提示不兼容，而不是允许应用运行后随机崩溃。

## 6.3 Optional Capability

可增强体验但不是必需能力的，应声明 optional capability。

应用 MUST 对 optional capability 缺失提供合理降级。

---

# 7. 权限模型

Capability 与 Permission 是两个不同概念：

- **Capability**：设备 / Platform 是否具备某能力；
- **Permission**：应用是否被允许使用某资源或用户数据。

例如：

```text
Capability: network.wifi
Permission: network
```

第一阶段权限类别 MAY 包括：

```text
network
library.read
library.write
notes.read
notes.write
clipboard
user_files.read
user_files.write
audio.output
bluetooth
```

权限 MUST 在 Manifest 中声明。

Platform SHOULD 采用最小权限原则。

未声明权限的应用 MUST 不得通过其他方式绕过平台权限系统。

应用自己的 SQLite database 属于 App sandbox private data，不需要额外用户资料权限。

---

# 8. Storage、SQLite、Library 与沙箱

每个 App MUST 拥有独立应用沙箱。

逻辑路径：

```text
appdata/
cache/
documents/
downloads/
```

应用必须区分：

```text
baga.storage
→ 文件 / 字节资源、逻辑路径与平台沙箱桥接

lsqlite3 / SQLite
→ App 自己的结构化关系数据库

baga.library
→ 经权限控制的用户书库 / 文档资源
```

应用：

- MUST 不假设 Android 或 Kindle 的真实文件路径；
- MUST 不直接扫描系统目录；
- SHOULD 使用 `baga.storage` 处理文件/字节；
- SHOULD 直接使用 `lsqlite3` / SQLite 处理结构化关系数据；
- MUST 使用 `baga.library` 与 `library.read/write` Permission 访问用户书库；
- MUST 不直接访问厂商书库数据库作为 Universal App contract。

数据库路径通过一个很薄的平台路径桥获得，例如：

```lua
local sqlite3 = require("lsqlite3")
local path = baga.storage.resolve_path("appdata/app.sqlite3")
local db = sqlite3.open(path)
```

`resolve_path()` 的职责只是把当前 App 已授权逻辑路径安全映射为供标准库使用的平台路径；它不重新包装 SQLite。

卸载应用时，Platform SHOULD 区分：

- 可安全删除的 cache；
- app private data / SQLite databases；
- 用户主动创建且可能需要保留的 documents。

---

# 9. Network、Offline-first、SQLite 与 Automerge

墨水屏经常处于断网或低频联网状态，因此 Baga Ink App SHOULD 默认采用 offline-first 思维。

应用 MUST：

- 正确处理无网络；
- 不把网络在线作为正常启动前提；
- 不持续高频轮询；
- 本地用户确认操作 SHOULD 先可靠持久化，再等待同步；
- 不因同步失败破坏本地数据；
- 使用 Baga Ink Network / Sync API，而不是直接依赖设备私有网络接口。

必须区分：

```text
SQLite / lsqlite3
→ 本地关系数据、事务、查询、索引、FTS、缓存 metadata

baga.sync
→ 网络/电源/生命周期下的同步触发和调度

Automerge core（适用时）
→ 多设备并发离线编辑、CRDT merge、change history、可选 sync protocol

App business policy
→ 哪些对象 authoritative、哪些对象 CRDT、版本历史和产品语义
```

对于真正有多设备并发离线编辑需求的数据，App / Platform implementation SHOULD 优先采用 Automerge core，而不是自行发明通用 CRDT。

采用方式可以是：

```text
完整 core
只用 document / merge / history
Automerge binary 存 SQLite BLOB
只用 Automerge sync protocol
通过 automerge-c / Rust core 接入
只用 patch / cursor 等模块
```

任何具体模块都不应被机械用于所有数据。

例如：

```text
Reading Position
→ 简单业务 merge

Feed / Comments / Public Notes
→ Server authoritative + local cache / SQLite

Book Files
→ content hash + file transfer

Notes / Life Records / Drafts
→ 真正并发编辑时 Automerge 候选
```

长时间任务 SHOULD 支持重试、取消以及睡眠/唤醒后的恢复。

---

# 10. UI 与墨水屏行为

Baga Ink App 的 UI SHOULD 以电子纸显示特性为基本设计约束。

应用 SHOULD：

- 使用高对比度界面；
- 避免无意义动画；
- 避免持续滚动动画；
- 避免大面积高频重绘；
- 使用合理的大触控目标；
- 支持物理翻页键映射；
- 在无触摸设备上保留基础可操作性（当应用声明支持该类设备时）；
- 让 Platform 决定实际刷新波形和厂商接口。

App 可以表达刷新**意图**，但 MUST 不直接控制某厂商私有刷新实现。

---

# 11. Display 规则

应用 MAY 请求：

```text
AUTO
TEXT
QUALITY
FAST
ANIMATION
```

这些是语义模式，不是底层 waveform ID。

Platform / Device Adapter 负责把语义模式映射到：

- Kindle 刷新机制；
- Android Generic 行为；
- BOOX / iReader 等私有刷新能力。

应用 MUST 不假设所有设备都拥有相同刷新模式。

---

# 12. Input 规则

应用 SHOULD 围绕语义动作设计交互，例如：

```text
page_next
page_previous
confirm
back
menu
```

而不是将核心操作硬编码成某个物理键码。

Platform 负责把：

```text
touch
pen
physical page key
keyboard
volume key（在允许的设备上）
```

映射到统一输入模型。

---

# 13. 电源规则

Universal App MUST 尊重墨水屏设备的低功耗目标。

应用：

- MUST 不无理由保持设备常亮；
- MUST 不持续后台唤醒；
- SHOULD 让同步任务适配 Wi-Fi / charging policy；
- MUST 在 sleep / wake 生命周期正确处理状态；
- MUST 使用 Baga Ink Power API 请求 keep-awake，而不是直接修改 OS 电源状态。

Platform MAY 拒绝不合理的 keep-awake 请求。

---

# 14. Reader 能力

如果应用使用阅读能力，SHOULD 调用 Baga Ink Reader API。

Reader API 是**格式无关的应用边界**，不以 EPUB 或任意单一文档格式为中心。

应用 SHOULD：

```lua
baga.reader.supports(source_or_format)
baga.reader.open(source)
```

而不是假设某个固定格式一定存在。

应用不应因为 Baga Ink Platform 某一版本内部复用了 KOReader，就直接依赖 KOReader 私有 Lua 对象。

原则：

```text
App → Baga Ink Reader API → Platform implementation
```

而不是：

```text
App → KOReader internals
```

## 14.1 Reader Anchor

当应用需要保存阅读位置、笔记、高亮或把业务对象关联到正文时，应优先使用 `baga.reader` 的标准 Position / Anchor 语义。

App MUST：

- 把 Anchor 视为 opaque、可序列化 Baga 值；
- 不自行解析 XPointer、PDF pboxes、EPUB CFI 等 Reader 私有/外部表示；
- 不为 EPUB/PDF/MOBI/FB2/TXT/DjVu/CBZ 等分别重写 Locator；
- 由 Platform/Reader implementation 负责真正定位和恢复。

Platform 可以在内部复用 KOReader 等成熟 Reader 已有的不同格式位置模型。

---

# 15. 依赖与成熟实现复用规则

为了避免 dependency hell，Universal App SHOULD 默认自包含应用代码与资源，但 **Baga Lua Profile 正式 Standard Libraries 由 Platform 提供，不要求每个 IKP 重复打包。**

App MAY：

- 使用 Baga Ink Platform 标准库；
- 直接使用 Baga Lua Profile Standard Libraries，例如 `lsqlite3`；
- 将纯 Lua 第三方库打入自己的 IKP。

App MUST NOT：

- 依赖用户另行安装的随机 native library；
- 依赖某个厂商系统中“碰巧存在”的动态库；
- 自带另一套 SQLite runtime 与 Platform 的 SQLite 冲突；
- 把 native shared dependency 作为 Universal App 的随机外部前提。

这里的“自包含”指**应用代码与应用资源自包含**，不代表 App 自带一套平台核心、Lua 解释器、设备适配层或系统桥。

成熟组件采用原则：

```text
SQLite / lsqlite3
→ Stable Standard Library

Automerge core
→ Adopted Local-first Foundation
→ 可整用 / 拆用
→ Lua developer binding 尚未冻结

KOReader / FBInk / Vendor SDK
→ Platform / Adapter implementation detail
```

---

# 16. 安全与稳定性

应用 MUST：

- 不尝试突破沙箱；
- 不篡改 Platform；
- 不修改其他 App 私有数据；
- 不通过未声明接口访问敏感资源；
- 不假设可以执行任意 native code；
- 对来自网络、文件和用户输入的数据做基本验证。

Platform MAY 因安全原因终止违反规则的 App。

`lsqlite3` 只能打开 App 被授权的路径；实现必须防止通过数据库路径或 loadable extension 绕过 sandbox。

---

# 17. 签名与发布者身份

进入 Baga Ink Market 的 App SHOULD 使用受支持的数字签名。

应用更新 MUST 保持 Application ID，并 SHOULD 保持发布者签名连续性。

如果签名密钥发生变化，应通过明确的 key rotation / recovery 机制处理。

具体规则由 IKP Package Specification 和 Market Policy 定义。

---

# 18. Market 兼容标签

Baga Ink Market SHOULD 至少支持：

```text
Baga Ink Universal
Enhanced
Requires Pen
Requires Touch
Requires Network
Kindle Compatible
Android E-Paper Compatible
Experimental
```

兼容标签必须来源于 Manifest、Capability Model 和 Compatibility Test，而不是开发者随意填写宣传文字。

---

# 19. Universal 合规硬规则

一个应用要获得 **Baga Ink Universal** 标识，MUST 同时满足：

1. 使用 `.ikp`；
2. 使用 Baga Lua Profile；
3. 只使用公开 Baga Ink API 获取设备 / OS / Platform 能力；
4. 允许使用 Baga Lua Profile 正式 Standard Libraries；
5. 不携带设备相关 native binary 作为正常应用逻辑；
6. 不携带自己的 Lua 解释器、设备适配层或系统桥；
7. 不调用 raw shell / vendor SDK；
8. 使用 Capability Model；
9. 权限完整声明；
10. 使用标准生命周期；
11. 通过 Compatibility Test；
12. 至少在 Kindle 与 Android E-Paper 两个平台家族的参考实现上通过验证，才可使用跨平台 Universal 宣传。

---

# 20. 不能进入 Universal 边界的能力

以下能力不得成为普通 Universal App 默认开发方式：

- 任意 Shell；
- 任意 Java / JNI bridge；
- 自定义 Kernel / Driver；
- 随机跨 App 共享 native dependency；
- Vendor-specific API 直接调用；
- WebView / Chromium 作为平台默认应用执行方式；
- 每个 App 自己实现系统级更新机制；
- 每个 App 自带另一套 Lua 解释器或设备兼容代码；
- 每个 App 自带冲突的 SQLite runtime；
- 自研 SQLite-like KV/Collection API 替代成熟 SQLite；
- 自研通用 CRDT 仅为了替代 Automerge 这类成熟基础。

这些能力如未来需要，应位于受控扩展层、Standard Library 或 Platform 实现层，而不是侵蚀 Universal App 边界。

---

# 21. LifeBook 的参考应用地位

LifeBook 是第一批 Reference App，用于验证 Baga Ink 标准能否真正跨 Kindle 与 Android 墨水屏工作。

LifeBook MUST 遵循与第三方应用相同的核心规则，不能因为它是官方旗舰 App 就大量使用私有捷径，否则 Baga Ink 标准无法被真实验证。

LifeBook：

- 设备能力只通过 `baga.*`；
- 结构化本地关系数据直接使用 `lsqlite3`；
- Reader 使用 `baga.reader`；
- 真正并发离线编辑场景优先采用 Automerge core，而不是自研 CRDT；
- 不需要额外通用中间层。

允许 LifeBook 在早期存在少量内部实验接口，但这些接口：

- MUST 明确标记为 internal / experimental；
- MUST 不被第三方依赖；
- 成熟后要么进入正式 Baga Ink API / Standard Library，要么删除。

---

# 22. 最终目标

Baga Ink App Standard 的目标不是限制创造力，而是把跨设备最痛苦、最容易重复造轮子的部分收敛到平台，并让成熟通用软件能力直接复用成熟生态。

开发者应该把时间花在：

```text
阅读体验
笔记
RSS
AI
知识管理
教育
工具
创作
```

而不是花在：

```text
Kindle framebuffer
BOOX refresh API
iReader private SDK
Android vendor differences
不同设备的安装脚本
文件拼接式“数据库”
自研数据库抽象
每种书籍格式的定位算法
自研通用 CRDT
```

这就是 Baga Ink Universal App 标准存在的根本价值。
