# Baga Ink Kindle 适配规范 / Baga Ink Kindle Adapter

> **文档级别：首发设备适配规范**  
> **状态：Draft v0.4**  
> **日期：2026-08-23**  
> **上位文档：`07_设备适配器规范_Baga-Ink-Device-Adapter-Specification.md`**  
> **认证依据：`08_兼容性标准_Baga-Ink-Compatibility-Standard.md`、`10_兼容性测试套件_Baga-Ink-Compatibility-Test-Suite.md`**  
> **标准库依据：`13_标准库与成熟组件采用规范_Baga-Ink-Standard-Libraries-and-Adopted-Components.md`**

---

## 0. 目的 / Purpose

本文档定义 Kindle 系列如何实现 Baga Ink Device Adapter，以及 Kindle Reference Platform 如何复用成熟 Kindle / Lua / SQLite / Automerge 生态。

它不定义某一个具体越狱漏洞，也不把任何单一 Homebrew 工具绑定成永久平台标准。

核心边界：

```text
Baga Ink Kindle Adapter Contract
+
Baga Lua Profile / Standard Libraries
+
Kindle Installation Route Database
```

其中：

- Adapter Contract 稳定；
- Standard Libraries 由 Platform Release 锁定版本；
- Installation Route 随 Kindle 型号 / 固件持续更新。

---

# 1. 架构位置不变

```text
IKP Apps
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
Kindle OS / supported Homebrew environment
```

KOReader、koreader-base、FBInk、SQLite、lsqlite3、lua-ljsqlite3、Automerge、KPM、Hotfix 等都**不是新架构层**。

它们只是现有 Platform / Adapter / Standard Library 的具体实现与复用组件。

---

# 2. 设计原则

Kindle implementation MUST / SHOULD：

1. 最大化复用成熟 Kindle Homebrew / KOReader 能力；
2. 不重新实现已经稳定存在的显示、输入、阅读、Annotation、文档定位基础设施；
3. SQLite 直接作为成熟标准数据库使用，不再经过 `baga.data`；
4. IKP 标准 SQLite binding 使用 `lsqlite3`；
5. KOReader 内部原有 `lua-ljsqlite3` 可以继续保留，不要求迁移；
6. `lsqlite3` 与 KOReader 内部 `lua-ljsqlite3` SHOULD 共享同一 Platform-managed `libsqlite3`；
7. Local-first / CRDT 场景优先采用 Automerge core，可整体或拆模块复用；
8. 不把 `automerge-repo` 的层次结构机械复制成 Baga 架构；
9. 隔离型号 / 固件 / ABI 差异；
10. 不让 IKP App 直接调用 Kindle Shell / private framework；
11. 所有公开设备能力仍由 `baga.*` / Capability Registry 定义；
12. 所有兼容声明必须通过 BICTS。

---

# 3. Kindle Reference Implementation Mapping

> **本图是 Kindle 参考实现映射，不是 Baga Ink 的新架构层。**

```text
Baga Ink on Kindle
│
├─ baga.reader
│   └─ 主要复用 KOReader
│       ├─ CREngine
│       ├─ MuPDF
│       ├─ ReaderUI
│       ├─ annotation / bookmark / highlight
│       └─ position / search / selection / anchor
│
├─ baga.ui
│   └─ 可复用 KOReader Lua UI / widget / UIManager
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
├─ Baga Lua Profile: lsqlite3
│   └─ 共享 Platform-managed libsqlite3
│       └─ LifeBook / IKP 直接使用 SQL / transaction / FTS / JSON
│
├─ KOReader internals
│   └─ 继续使用 lua-ljsqlite3
│       └─ 同样链接上面的 libsqlite3
│
├─ baga.sync
│   └─ 联网 / Wi-Fi / sleep-wake / trigger / retry policy
│
├─ Automerge core（适用业务）
│   ├─ document / merge / history
│   ├─ binary persistence
│   ├─ sync protocol（可选）
│   ├─ automerge-c / Rust core bridge
│   └─ patches / cursors（按需）
│
├─ baga.network
│   └─ 成熟 HTTP / TLS / Kindle 网络桥接
│
└─ baga.power
    └─ Kindle 系统能力 / KOReader 已验证 lifecycle / power 机制
```

关键：

```text
SQLite / lsqlite3
≠ baga.data

Automerge
≠ baga.sync

KOReader
≠ Baga Reader Layer
```

它们分别是成熟 Standard Library、Adopted Foundation 或内部实现来源。

---

# 4. Lua / SQLite 实现

Kindle 上 SHOULD 优先复用 KOReader/koreader-base 已验证 LuaJIT、SQLite 和 native foundation。

## 4.1 IKP developer-facing SQLite

Baga Lua Profile 对 IKP 提供：

```lua
local sqlite3 = require("lsqlite3")
```

数据库路径：

```lua
local path = baga.storage.resolve_path("appdata/app.sqlite3")
local db = sqlite3.open(path)
```

开发者可直接使用标准 SQL 与 SQLite API。

## 4.2 KOReader internal SQLite

KOReader 当前已有大量代码直接使用：

```lua
require("lua-ljsqlite3/init")
```

以及：

```text
open
exec
prepare
bind
step
rowexec
```

Baga 不要求 KOReader 为统一表面 API 而重写这些内部模块。

## 4.3 单一 `libsqlite3`

Reference implementation SHOULD 避免同一进程加载多份不同 SQLite runtime。

推荐：

```text
Platform-managed libsqlite3
        ├─ lsqlite3          → IKP Standard Library
        └─ lua-ljsqlite3     → KOReader internals
```

不采用 `lsqlite3complete` 作为默认 Reference 方案。

---

# 5. Kindle 支持对象

认证对象不是笼统“支持 Kindle”，而是：

```text
model family
+ firmware version/range
+ homebrew foundation state
+ CPU/ABI
+ Kindle Adapter version
+ Baga Ink Platform version
+ Baga Lua Profile version
+ BICTS version
```

Platform / Adapter SHOULD 记录：

```text
model_id
model_name
firmware_version
cpu_arch
soft-float / hard-float
screen backend
input backend
reader backend/version
SQLite version
lsqlite3 version
Automerge version（如采用）
homebrew foundation status
known quirks
```

这些用于诊断，不成为 IKP 业务分支。

---

# 6. 安装入口与 Adapter 分离

Baga Ink Client 负责：

```text
识别 model / firmware
判断已有 Homebrew 基础
查询 Installation Route Database
显示 Compatible / Experimental / Unsupported
安装 / 修复 / 升级 Platform
```

WinterBreak、SpringBreak、Sanctuary、Véra 等只属于可更新安装路线，不属于 `baga.*` 或 LifeBook。

---

# 7. Display

Kindle Adapter MUST 实现：

```text
display.basic
```

并按真实能力声明：

```text
display.partial_refresh
display.fast_refresh
display.quality_refresh
display.grayscale
display.rotation
display.color
```

实现 SHOULD 优先复用 KOReader Kindle device/display knowledge、koreader-base、FBInk。

App 只表达：

```text
AUTO
TEXT
QUALITY
FAST
ANIMATION
```

具体 waveform / framebuffer 行为不暴露给 IKP。

---

# 8. Input

不同 Kindle 可能拥有：

```text
Touch
Physical Page Keys
D-pad / Keyboard
No Touch + Buttons
```

统一映射为：

```text
confirm
back
menu
page_next
page_previous
focus_next
focus_previous
```

KOReader 已有 Kindle input 处理 SHOULD 作为首选实现来源。

---

# 9. Storage / Sandbox

Kindle Platform MUST 为每个 IKP 提供逻辑沙箱。

```text
appdata/
cache/
documents/
downloads/
```

`baga.storage.resolve_path()` 可为 `lsqlite3` 等正式 Standard Library 提供当前 App 的真实运行时路径。

Kindle 缺乏现代 Android 式 per-App OS sandbox，因此 Platform MUST 额外保证：

- path normalization；
- `..` / absolute escape rejection；
- other-app private path isolation；
- 必要时使用受限 VFS / broker / 等价机制；
- SQLite 不得通过 ATTACH、URI/path trick 或 extension loading 绕过 sandbox。

具体安全策略由实现验证，但最终必须通过 BICTS。

---

# 10. User Library / `baga.library`

Kindle Adapter MAY 索引 Kindle 已有书籍 / 文档，但 App 只看到 `baga.library`。

```text
Kindle books/files/library metadata
        ↓
Kindle Adapter / Platform
        ↓
baga.library
        ↓
IKP App
```

规则：

- Library Item 使用 opaque ID；
- `library.read/write` 继续控制用户书库；
- IKP 不扫描 `/documents`；
- IKP 不读取 Kindle private library DB；
- Library handle 可交给 `baga.reader.open()`；
- 不限定 EPUB 或单一格式。

---

# 11. Reader / KOReader

Kindle 第一 Reader 实现 SHOULD 最大程度复用 KOReader / koreader-base / CREngine / MuPDF。

公开关系：

```text
IKP App
  ↓
baga.reader
  ↓
Baga Ink Platform on Kindle
```

内部复用：

```text
ReaderUI
CREngine
MuPDF
ReaderAnnotation
ReaderHighlight
ReaderBookmark
position/search/selection
```

第三方 App 不依赖 KOReader private object / sidecar schema。

## 11.1 Format-agnostic

Baga Reader 不是 EPUB Reader。

当前 Kindle implementation 可复用 KOReader 支持的多种格式，但实际能力以 `baga.reader.supports()` 为准。

## 11.2 Reader Anchor

KOReader 已经分别处理：

```text
rolling/reflowable → XPointer-like positions
paging/fixed-page → page + local positions / boxes
```

因此 `reader.anchor` SHOULD 直接复用 KOReader 已有成熟定位，不重新为每种格式造 Locator。

Readium Locator / EPUB CFI / W3C Web Annotation 仅作为设计参考。

---

# 12. Network

如果 Wi-Fi 可用，声明：

```text
network.available
network.wifi
network.http
network.https
```

Adapter 必须处理：

- airplane mode；
- sleep 时 Wi-Fi 断开；
- wake 重连；
- DNS / TLS / timeout；
- connectivity events。

成熟网络实现可直接复用；IKP 只看 `baga.network`。

---

# 13. Sync 与 Automerge

`baga.sync` 只负责：

```text
联网状态
Wi-Fi policy
sleep/wake
trigger
retry/cancel
charging policy
```

Automerge 解决的是另一类问题：并发 Local-first state。

对于确有并发离线编辑的业务，MAY：

```text
完整采用 Automerge core
或
只用 document/merge/history
或
只用 binary persistence
或
只用 sync protocol
或
通过 automerge-c 接入
或
只用 patch/cursor 模块
```

Baga v0.x 不强制采用 `automerge-repo`。

如果只采用 Automerge document/merge，网络仍可使用现有 Baga HTTP / server protocol。

如果采用 Automerge sync protocol，它运行在 Baga 提供或 App 选择的可靠 transport 之上。

---

# 14. SQLite + Automerge 在 LifeBook 的组合

典型 Kindle LifeBook 可以：

```text
SQLite
├─ library metadata
├─ account/session metadata
├─ cached articles / Q&A / comments
├─ reading progress
├─ indexes / FTS
└─ Automerge document/change BLOB metadata

Automerge
├─ My Notes（真正并发时）
├─ Life Records
├─ Time Capsule drafts
└─ Article drafts
```

这不是平台强制 schema，仅说明两种成熟轮子可以自然组合。

---

# 15. Lifecycle / Power

Adapter 必须稳定映射：

```text
start
resume
pause
sleep
wake
stop
```

SHOULD 利用 Kindle 系统事件 / KOReader/Homebrew 已验证机制，而不是 App 轮询。

已提交 SQLite transaction 在 sleep/restart 后必须保持可靠。

---

# 16. Hardware / Capability

## 16.1 Touch

真实支持时声明 `input.touch`。

## 16.2 Physical Page Keys

映射到 `page_next / page_previous`。

## 16.3 No-touch legacy Kindle

只要 `input.navigation` 成立，Base UI 必须可用 Focus 操作。

## 16.4 Scribe Pen

通过 BICTS 后声明：

```text
input.pen
input.pen.pressure
input.pen.eraser
input.pen.low_latency
```

## 16.5 Colorsoft

通过测试后声明 `display.color`，黑白设备仍完整可用。

## 16.6 Audio / Bluetooth

只按真实当前设备能力声明。

---

# 17. ABI / 固件

KOReader target 是重要工程参考：

| 平台族 | KOReader target | Baga Ink 工程含义 |
|---|---|---|
| Legacy | `kindle-legacy` | Kindle 2/3/DXG；低资源、旧 ABI |
| Classic | `kindle` | K4/Touch/PW1 等老环境 |
| PW2+ soft-float | `kindlepw2` | PW2+ soft-float 路径 |
| Hard-float | `kindlehf` | Firmware `>= 5.16.3` hard-float |

核心：

> **Firmware 5.16.3 是重要 soft-float / hard-float 工程边界。**

变化发生在：

```text
Platform native binaries
KOReader build
FBInk
libsqlite3 / lsqlite3 native binding build
Automerge native bridge（若采用）
Homebrew foundation
```

不发生在：

```text
lifebook.ikp 业务逻辑
SQL schema semantics
baga.* contract
```

---

# 18. Quirk / Compatibility

兼容性对象：

```text
Device Model
+ Firmware Range
+ Platform Version
+ Adapter Version
+ Lua Profile Version
+ BICTS Version
```

Quirk MAY 包含：

```text
touch correction
refresh workaround
frontlight range
sleep event workaround
network service difference
library/reader workaround
```

Quirk 不成为公开 Capability。

---

# 19. Home Screen

长期用户体验：

```text
Kindle Home
  ↓ one action
LifeBook / Baga Ink App
```

KUAL / MRPI / KPM / Hotfix / KOReader 对普通用户隐身。

---

# 20. User Data Protection

安装 / 更新 / 卸载 MUST：

- 不删除用户书籍；
- 不删除用户 Kindle 笔记；
- 不清 `/documents`；
- 不恢复出厂；
- 更新失败保留上一可用 Platform/App；
- Platform/App 更新不得无故删除 App SQLite DB；
- migration 失败必须可恢复或明确阻止激活。

---

# 21. Kindle Compatible Gate

正式 Compatible 前 MUST：

- Base BICTS PASS；
- Baga Lua Profile PASS；
- `lsqlite3` / SQLite Profile PASS；
- capability 声明真实；
- Library bridge（若声明）PASS；
- Reader / Anchor（若声明）PASS；
- sleep/wake 稳定；
- IKP install/update/rollback 可靠；
- 不破坏用户书籍/笔记/数据库；
- 固件范围明确。

底层“KOReader 能启动”或“SQLite 能打开”本身都不足以获得 Compatible。

---

# 22. 非目标

Kindle Adapter 不负责：

- 固定某个永久越狱方法；
- 替换 Kindle OS；
- 让 IKP 执行 arbitrary shell；
- 给每个 App 打 Kindle native binary；
- 为每个成熟库建立一个新的 Provider/Engine 层；
- 用 `baga.data` 再包装 SQLite；
- 重写 KOReader 已解决的每种格式定位；
- 自研通用 CRDT 替代成熟 Automerge；
- 强制整套采用 automerge-repo。

---

# 23. 核心原则

> **开发者只面对统一 Baga Ink 平台能力与正式 Standard Libraries；Kindle 实现内部则应大胆、谨慎地复用 KOReader、FBInk、SQLite、lsqlite3、lua-ljsqlite3、Automerge 与 Homebrew 生态。**

其中：

```text
baga.*
→ 设备/OS/Platform 差异

lsqlite3
→ 直接使用成熟 SQLite

Automerge
→ 优先成熟 Local-first/CRDT foundation，可整用/拆用
```

不要为了“统一外观”牺牲成熟库本来已经优秀的设计。