# Baga Ink Kindle 适配规范 / Baga Ink Kindle Adapter

> **文档级别：首发设备适配规范**  
> **状态：Draft v0.5**  
> **日期：2026-08-23**  
> **上位文档：`07_设备适配器规范_Baga-Ink-Device-Adapter-Specification.md`**  
> **认证依据：`08_兼容性标准_Baga-Ink-Compatibility-Standard.md`、`10_兼容性测试套件_Baga-Ink-Compatibility-Test-Suite.md`**  
> **标准库依据：`13_标准库与成熟组件采用规范_Baga-Ink-Standard-Libraries-and-Adopted-Components.md`**

---

## 0. 目的

本文档定义 Kindle 系列如何实现 Baga Ink Device Adapter，以及 Kindle Reference Platform 如何复用成熟 Kindle、KOReader、SQLite 与 Automerge 生态。

正式正文只描述当前有效设计；历史方案由 Git 保存。

---

# 1. 架构

```text
IKP Apps
   ↓
Baga Ink API / Baga Lua Profile
   ↓
Baga Ink Platform Core
   ↓
Baga Ink Kindle Adapter
   ↓
Kindle OS / supported Homebrew environment
```

KOReader、koreader-base、FBInk、SQLite、lsqlite3、lua-ljsqlite3、Automerge、KPM、Hotfix 等是现有 Platform / Adapter / Standard Library 的实现与复用组件，不形成新的公共架构层。

---

# 2. 设计原则

Kindle implementation MUST / SHOULD：

1. 最大化复用成熟 Kindle Homebrew / KOReader 能力；
2. 不重复实现显示、输入、阅读、Annotation、文档定位基础设施；
3. IKP 结构化关系数据直接使用 SQLite / `lsqlite3`；
4. KOReader 内部可继续使用 `lua-ljsqlite3`；
5. `lsqlite3` 与 KOReader 内部 binding SHOULD 共享同一 Platform-managed `libsqlite3`；
6. Local-first / CRDT 场景优先采用 Automerge core，可整体或拆模块复用；
7. 隔离型号、固件与 ABI 差异；
8. IKP 不直接调用 Kindle 私有系统接口；
9. 所有公开设备能力由 `baga.*` / Capability Registry 定义；
10. 所有兼容声明必须通过 BICTS。

---

# 3. Kindle Reference Implementation Mapping

> **本图是实现映射，不是公共架构图。**

```text
Baga Ink on Kindle
│
├─ baga.reader
│   └─ KOReader
│       ├─ ReaderUI
│       ├─ CREngine
│       ├─ MuPDF
│       ├─ annotation / bookmark / highlight
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
│       └─ shared Platform-managed libsqlite3
│
├─ baga.sync
│   └─ online / Wi-Fi / sleep-wake / trigger / retry / charging policy
│
├─ Automerge core（适用业务）
│   ├─ document / merge / history
│   ├─ binary persistence
│   ├─ sync protocol（可选）
│   ├─ automerge-c / Rust core bridge
│   └─ patches / cursors（按需）
│
├─ baga.network
│   └─ mature HTTP / TLS / Kindle network bridge
│
└─ baga.power
    └─ Kindle system / validated KOReader/Homebrew mechanisms
```

---

# 4. SQLite

IKP 使用：

```lua
local sqlite3 = require("lsqlite3")
local path = baga.storage.resolve_path("appdata/app.sqlite3")
local db = sqlite3.open(path)
```

KOReader 内部继续使用其现有 `lua-ljsqlite3` 实现，不要求迁移。

Reference implementation SHOULD：

```text
Platform-managed libsqlite3
├─ lsqlite3       → IKP Standard Library
└─ lua-ljsqlite3  → KOReader internals
```

Kindle 缺乏现代 Android 式 per-App OS sandbox，因此 SQLite MUST 通过 sandbox-aware VFS 或等价 I/O confinement 限制数据库、ATTACH、journal、WAL、SHM、temp file 与 path/URI 访问，并通过 BICTS。

---

# 5. 支持与兼容对象

认证对象：

```text
model family
+ firmware version/range
+ homebrew foundation state
+ CPU/ABI
+ Kindle Adapter version
+ Platform version
+ Baga Lua Profile version
+ BICTS version
```

诊断 SHOULD 记录：model、firmware、CPU/ABI、screen/input/reader backend、SQLite/lsqlite3 版本、Automerge 版本（如采用）、已知 quirks。

安装入口与 Adapter contract 分离；具体设备启用/安装路线由可更新 Compatibility / Installation Database 管理。

---

# 6. Display / Input / Hardware

Kindle Adapter MUST 实现 `display.basic`，并按真实设备能力声明局部刷新、快速刷新、灰阶、旋转、彩色等增强能力。

Display SHOULD 优先复用 KOReader / koreader-base / FBInk，App 只表达 `AUTO / TEXT / QUALITY / FAST / ANIMATION`。

输入统一为：

```text
confirm
back
menu
page_next
page_previous
focus_next
focus_previous
```

Touch、物理翻页键、D-pad、Keyboard、Pen 都由 Adapter 映射成统一语义。Scribe Pen、Color、Audio、Bluetooth 等只在真实实现并通过 BICTS 后声明对应 Capability。

---

# 7. User Library / Reader

Kindle 现有书籍和文档通过 `baga.library` 暴露，Library Item 使用 opaque ID；IKP 不扫描真实设备目录或读取 Kindle 私有书库数据库。

Kindle 第一 Reader implementation SHOULD 最大程度复用 KOReader / koreader-base / CREngine / MuPDF。

Reader 不以 EPUB 为中心，实际支持格式以 `baga.reader.supports()` 为准。

`reader.anchor` SHOULD 复用 KOReader 已有成熟位置模型：

```text
rolling/reflowable → XPointer-like positions
paging/fixed-page  → page + local positions / boxes
```

Readium Locator、EPUB CFI、W3C Web Annotation 只作设计参考。

---

# 8. Network / Sync / Automerge

`baga.network` 处理 Kindle 网络桥接、online/offline、DNS/TLS/timeout、sleep/wake 后重连。

`baga.sync` 负责联网、Wi-Fi、sleep/wake、trigger、retry/cancel、charging policy。

真正存在并发离线编辑的业务 MAY 整体或拆分采用 Automerge core：document/merge/history、binary persistence、sync protocol、C FFI、patch/cursor 等。Baga 不强制 automerge-repo。

SQLite 与 Automerge 可以自然组合；具体 LifeBook schema 和对象选择属于 LifeBook 产品实现，不是 Kindle Adapter 标准。

---

# 9. Lifecycle / Power / Data Protection

Adapter MUST 稳定映射：

```text
start
resume
pause
sleep
wake
stop
```

SHOULD 利用 Kindle 系统事件或已有成熟 Homebrew/KOReader 机制，而不是 App 轮询。

安装、更新、卸载 MUST：

- 不删除用户书籍；
- 不删除用户 Kindle 笔记；
- 不清用户文档区域；
- 不恢复出厂；
- 更新失败保留上一可用 Platform/App；
- 不无故删除 App SQLite DB；
- migration 失败可恢复或阻止激活。

---

# 10. ABI / 固件

KOReader target 是重要工程参考：

| 平台族 | KOReader target | 工程含义 |
|---|---|---|
| Legacy | `kindle-legacy` | Kindle 2/3/DXG；低资源、旧 ABI |
| Classic | `kindle` | K4/Touch/PW1 等老环境 |
| PW2+ soft-float | `kindlepw2` | PW2+ soft-float 路径 |
| Hard-float | `kindlehf` | Firmware `>= 5.16.3` hard-float |

> **Firmware 5.16.3 是重要 soft-float / hard-float 工程边界。**

变化发生在 Platform native binaries、KOReader/FBInk build、SQLite binding、Automerge native bridge（若采用）和 Homebrew foundation；不改变 `lifebook.ikp` 业务逻辑、SQL 语义或 `baga.*` contract。

---

# 11. Compatibility / Quirk

Compatibility 绑定：

```text
Device Model
+ Firmware Range
+ Platform Version
+ Adapter Version
+ Lua Profile Version
+ BICTS Version
```

Quirk 可以处理 touch correction、refresh workaround、frontlight、sleep event、network、library/reader 差异，但不成为公开 Capability。

---

# 12. Home Screen 与 Compatible Gate

长期用户体验：

```text
Kindle Home
  ↓ one action
LifeBook / Baga Ink App
```

底层 Homebrew/KOReader 工具对普通用户隐身。

正式 Compatible 前 MUST：

- Base BICTS PASS；
- Baga Lua Profile PASS；
- `lsqlite3` / SQLite Profile PASS；
- Capability 声明真实；
- Library / Reader / Anchor（如声明）PASS；
- sleep/wake 稳定；
- IKP install/update/rollback 可靠；
- 不破坏用户书籍、笔记、数据库；
- 固件范围明确。

---

# 13. 核心原则

> **开发者只面对统一 Baga Ink 平台能力与正式 Standard Libraries；Kindle 实现内部应大胆、谨慎地复用 KOReader、FBInk、SQLite、lsqlite3、lua-ljsqlite3、Automerge 与 Homebrew 生态。**

```text
baga.*     → 设备 / OS / Platform 差异
lsqlite3   → 直接使用成熟 SQLite
Automerge  → Local-first / CRDT foundation，可整用/拆用
```
