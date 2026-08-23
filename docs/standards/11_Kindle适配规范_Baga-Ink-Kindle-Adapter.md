# Baga Ink Kindle 适配规范 / Baga Ink Kindle Adapter

> **文档级别：首发设备适配规范**  
> **状态：Draft v0.3**  
> **日期：2026-08-23**  
> **上位文档：`07_设备适配器规范_Baga-Ink-Device-Adapter-Specification.md`**  
> **认证依据：`08_兼容性标准_Baga-Ink-Compatibility-Standard.md`、`10_兼容性测试套件_Baga-Ink-Compatibility-Test-Suite.md`**

---

## 0. 目的 / Purpose

本文档定义 Kindle 系列如何实现 Baga Ink Device Adapter。

它不定义某一个具体越狱漏洞，也不把任何单一 Homebrew 工具绑定成永久平台标准。

原因：

> **越狱入口会随固件变化，但 Baga Ink Adapter 的上层契约必须稳定。**

因此 Kindle Adapter 分成两部分理解：

```text
Baga Ink Kindle Adapter Contract     ← 本规范
Kindle Installation Route Database   ← Baga Ink Client 动态维护
```

同样重要的是：

> **KOReader、koreader-base、FBInk、SQLite、Automerge、KPM、Hotfix 等是 Kindle 上实现 Baga Ink 能力时可直接复用的成熟组件，不构成新的 Baga Ink 公共架构层。**

---

# 1. 架构位置

```text
IKP Apps
   │
   ▼
Baga Ink API
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

Kindle Adapter 内部负责或协助实现：

```text
Kindle display / framebuffer
Kindle input
lifecycle / power
storage mapping
network
frontlight / optional capabilities
system integration
quirks
```

Platform Core 与 Kindle Adapter 可以按工程需要直接调用成熟开源组件；内部依赖树不改变上述公共架构。

IKP App 不应该知道当前底层使用的是 KUAL、MRPI、KPM、Hotfix、KOReader、FBInk、SQLite、Automerge、某种 Launcher 或某种具体 jailbreak。

---

# 2. 设计原则

Kindle Adapter / Kindle Platform implementation MUST / SHOULD：

1. **最大化复用成熟 Kindle Homebrew / KOReader 能力；**
2. 不重新实现已经稳定存在的显示、输入、阅读、文档定位等基础设施；
3. 隔离型号 / 固件 / ABI 差异；
4. 不让 IKP App 直接调用 Kindle Shell；
5. 不要求 LifeBook 自己维护一套 Kindle 私有 API；
6. 能由 Baga Ink Client 检测兼容状态；
7. 安装失败不得破坏用户书籍与笔记；
8. 优先使用成熟数据库、网络、Reader 和同步算法，而不是为了“Baga 自研”重新造轮子；
9. 不因采用某个开源项目而创建新的公共 `Provider / Engine / Runtime` 层；
10. 所有公开能力仍由 `baga.*` 和 Capability Registry 定义。

---

# 3. Kindle 支持对象

认证对象不是“所有 Kindle”一句话，而是：

```text
model family
+ firmware version/range
+ homebrew foundation state
+ Kindle Adapter version
+ Baga Ink Platform version
+ BICTS version
```

Adapter MUST 提供：

```text
model_id
model_name
firmware_version
cpu_arch
platform_variant
adapter_version
capabilities
```

内部可进一步记录：

```text
soft-float / hard-float
screen backend
input backend
reader backend version
homebrew foundation version
known quirks
```

这些用于诊断和兼容数据库，不成为 IKP 业务契约。

---

# 4. 安装入口与 Adapter 分离

Baga Ink Client 负责判断：

```text
当前 Kindle 是否已有可用 Homebrew 基础？
是否已安装 Baga Ink Platform？
需要哪条受支持安装路线？
是否只能显示 Experimental / Unsupported？
```

Kindle Adapter 本身不应该写死：

```text
firmware X = 必须使用某漏洞 Y
```

WinterBreak、SpringBreak、Sanctuary、Véra 以及后续路线进入独立可更新的 Compatibility / Installation Database，而不是 `baga.*` API 或 LifeBook 代码。

这样 Amazon 固件变化不会迫使 Baga Ink API 或 Adapter Contract 改版本。

---

# 5. 现有生态复用原则

Kindle 当前成熟生态和通用开源组件提供了大量可以复用的基础设施。

优先评估：

```text
KOReader / koreader-base
├── Kindle device knowledge
├── display / input
├── ReaderUI
├── annotation / highlight / position
├── CREngine
└── MuPDF integration

FBInk
└── framebuffer / refresh / bootstrap / diagnostics

KPM / Universal Hotfix / MRPI / KUAL
└── Homebrew installation / lifecycle / fallback / maintenance

KindleTool / koxtoolchain
└── package / device / cross-build tooling

SQLite or equivalent mature DB
└── baga.data transactional local storage implementation

Automerge or equivalent mature Local-first CRDT
└── only where a higher-level feature truly needs concurrent offline merge
```

复用这些组件时：

- MAY 整体使用；
- MAY 只拆用某些稳定模块；
- MAY 用其代码/协议/算法作为某项 Baga API 的内部实现；
- MUST 遵守许可证；
- MUST 锁定并记录实际 dependency version / commit；
- MUST 通过 BICTS 验证 Baga 语义；
- MUST NOT 把其私有 API 直接交给 IKP。

错误理解：

```text
Baga API
  ↓
KOReader Provider Layer
  ↓
SQLite Provider Layer
  ↓
Automerge Provider Layer
  ↓
Kindle Adapter
```

正确理解：

```text
Baga Ink Platform on Kindle
  ├── baga.reader 的实现可以大量复用 KOReader
  ├── baga.ui/display/input 的实现可以复用 KOReader / FBInk
  ├── baga.data 的实现可以使用 SQLite
  └── 需要 CRDT 的具体同步逻辑可以复用 Automerge
```

这些都属于同一个现有 Baga Ink Platform / Kindle Adapter 架构内部。

---

# 6. Lua 实现

Kindle 上 SHOULD 优先复用已经验证的 Lua / LuaJIT 能力，而不是为了 Baga Ink 再复制一整套大型基础设施。

Platform Core 只要求：

```text
能够执行 Baga Lua Profile
能够绑定 baga.* API
```

具体解释器来源、构建方式属于 Kindle Platform implementation detail。

第三方 IKP 不携带自己的 Lua 解释器。

---

# 7. Display Adapter

Kindle Adapter MUST 实现：

```text
display.basic
```

并根据型号真实能力声明：

```text
display.partial_refresh
display.fast_refresh
display.quality_refresh
display.grayscale
display.rotation
display.color            when actually supported/tested
```

实现 SHOULD 优先复用 KOReader Kindle device/display knowledge、koreader-base、FBInk 或经过验证的 Kindle framebuffer 接口。

Adapter MUST：

- 正确识别逻辑屏幕尺寸；
- 正确处理 orientation；
- 把 `AUTO/TEXT/FAST/QUALITY/ANIMATION` 映射到适当 Kindle 刷新方式；
- 对不支持模式合理降级；
- 不将 waveform ID 暴露给 App；
- 控制残影清理策略。

---

# 8. Kindle 刷新策略

默认目标：

```text
文字翻页 → TEXT / QUALITY policy
菜单 focus → partial / FAST when supported
输入交互 → FAST when appropriate
累积残影 → Adapter 自动质量刷新
```

App 只表达 intent。

Kindle Adapter 负责具体 waveform / framebuffer 行为。

如果 KOReader / FBInk 已经稳定解决某个设备族的刷新行为，SHOULD 直接复用或包装这些实现，而不是重新逆向一套。

---

# 9. Input Adapter

不同 Kindle 可能拥有：

```text
Touch
Physical Page Keys
D-pad / Keyboard（旧机型）
No Touch + Buttons
```

必须统一映射为：

```text
confirm
back
menu
page_next
page_previous
focus_next
focus_previous
```

Capability 根据真实硬件声明：

```text
input.touch
input.physical_page_key
input.keyboard
```

Universal App 不使用 Kindle 私有 keycode。

KOReader 已有 Kindle input 处理可以作为首选实现来源。

---

# 10. Touch

Touch 设备必须：

- 归一化坐标；
- 处理 orientation；
- 过滤异常重复事件；
- 在 sleep/wake 后恢复；
- 保证坐标与 Baga Ink UI 一致。

---

# 11. Physical Page Keys

拥有物理翻页键的 Kindle SHOULD 声明：

```text
input.physical_page_key
```

并映射：

```text
left/previous key → page_previous
right/next key → page_next
```

实际物理位置或键码不得成为 App contract。

---

# 12. Storage 与 `baga.data`

Kindle Adapter MUST 为 Baga Ink 提供逻辑沙箱。

建议设备端内部布局由 Platform 管理，例如：

```text
Baga platform area
├── apps/
├── appdata/
├── cache/
├── platform/
└── logs/
```

具体真实路径不属于公共标准。

## 12.1 文件 / 字节存储

`baga.storage` 通过 Kindle 文件系统实现逻辑路径与沙箱。

用户已有 Kindle 内容目录不得直接暴露给 IKP。

## 12.2 事务型本地数据

`baga.data` 属于 Platform Core 标准服务，不需要为 Kindle 创建新的数据库架构层。

Kindle implementation SHOULD 优先使用：

> **SQLite 或其他在目标 Kindle 上经过资源/ABI/可靠性验证的成熟事务存储。**

必须保证：

```text
transaction atomicity
crash safety
sleep/restart durability
app sandbox isolation
platform update preserves app data
```

IKP 不知道底层数据库名称、路径、SQL schema 或 WAL 状态。

如果老 Kindle 的资源/ABI 对某 SQLite 构建有限制，可以更换内部实现或编译目标，但 `baga.data` 契约不改变。

---

# 13. 用户数据保护

这是 Kindle Adapter 的硬要求。

安装 / 更新 / 卸载 MUST：

- 不删除用户书籍；
- 不删除用户 Kindle 笔记；
- 不清空 `/documents` 等用户内容区域；
- 不恢复出厂；
- 不把删除系统关键文件作为标准安装步骤；
- 失败后尽可能保留可启动状态；
- 更新失败保留上一可用 Platform / App 版本。

任何不满足这些条件的设备组合只能进入 Experimental / Unsupported。

---

# 14. User Library Bridge / `baga.library`

Kindle Adapter MAY 索引 Kindle 已有书籍 / 文档或授权的用户内容，但上层只看到 `baga.library` 的统一对象。

```text
Kindle books/files/library metadata
             │
             ▼
     Kindle Adapter / Platform
             │
             ▼
         baga.library
             │
             ▼
      LifeBook / other IKP
```

规则：

- 设备有稳定现有书库桥接能力时声明 `storage.user_library`；
- `baga.library.list/get/open` 受 `library.read` Permission 控制；
- import/remove 等修改行为受 `library.write` Permission 控制；
- Library Item 使用 opaque Baga ID；
- IKP 不扫描 Kindle `/documents`；
- IKP 不解析 Kindle 私有书库数据库；
- Library source/handle 可以交给 `baga.reader.open()`；
- 不限定 EPUB 或任何单一文档格式。

---

# 15. Reader Integration

Baga Ink Kindle 版本 SHOULD **最大程度复用 KOReader ReaderUI / document engine / annotation / position 等成熟阅读能力**。

公开关系保持：

```text
IKP App
  ↓
baga.reader
  ↓
Baga Ink Platform on Kindle
```

当前 Kindle 实现内部：

```text
baga.reader
  → KOReader / koreader-base / CREngine / MuPDF 等既有能力
```

这里不再定义一个必须存在的额外“Reader Provider / Reader Engine Layer”。

第三方 App 不依赖：

```text
KOReader internal object
ReaderUI private API
CREngine object
MuPDF object
private sidecar schema
```

## 15.1 格式支持

Baga Reader 不是 EPUB Reader。

Kindle implementation 应通过 KOReader 等成熟 Reader 支持尽可能广的真实格式；例如可包括：

```text
EPUB
PDF
MOBI / AZW family where supported
FB2
TXT / HTML
DjVu
CBZ / comics
其他 KOReader/Reader implementation 实际支持的格式
```

这只是当前实现能力示例，不构成 Baga Ink 只支持这些格式的冻结清单。

App SHOULD 使用：

```lua
baga.reader.supports(source_or_format)
```

判断当前实现，而不是硬编码“LifeBook 支持 EPUB”。

## 15.2 Reader Anchor：复用 KOReader 已有定位

KOReader 已经对不同 Reader 模型实现了成熟的阅读位置和 Annotation 定位：

```text
reflowable / rolling
→ XPointer-like start/end positions 等原生机制

fixed-page / paging
→ page + page-local position / boxes 等原生机制
```

其 annotation 体系本身会处理 rolling 与 paging 位置格式不同的事实。

因此 Kindle implementation SHOULD：

```text
baga.reader.create_anchor()
baga.reader.goto_anchor()
baga.reader.resolve_anchor()
```

直接建立在这些成熟能力之上，而不是重新为 EPUB、PDF、MOBI、FB2、TXT、DjVu、CBZ 等每一种格式发明 Locator。

对 IKP：

- Anchor 是 opaque、可序列化 Baga 值；
- LifeBook 可以把 Anchor 与自己的笔记 / 公开笔记业务对象关联；
- LifeBook 不解析 XPointer / pboxes；
- Reader implementation 负责真正定位；
- 如果跨设备 / 跨 Reader 精确解析失败，可以使用标准 fallback evidence 尝试恢复；
- approximate recovery 必须明确，不得冒充 exact。

Readium Locator、EPUB CFI、W3C Web Annotation 可以作为设计参考，但不得把 Kindle/LifeBook Reader 变成 EPUB-centric 架构。

---

# 16. Network Adapter

如果设备 Wi-Fi 可被 Platform 使用，应声明：

```text
network.available
network.wifi
network.http
network.https
```

Adapter 必须处理：

- Airplane Mode；
- sleep 时 Wi-Fi 断开；
- wake 后重新联网；
- connectivity event；
- timeout / TLS / DNS 错误。

Baga Ink SHOULD 默认适应 Kindle 低频联网，而不是保持 Wi-Fi 常连。

成熟网络实现可以复用，但 IKP 只看到 `baga.network`。

---

# 17. Sync 与 Automerge 的位置

Kindle 上必须区分三个问题：

```text
baga.data
→ 当前设备本地可靠事务存储

baga.sync
→ 联网 / Wi-Fi / sleep-wake / trigger / retry policy

App domain merge
→ 同一业务对象发生并发修改时如何合并
```

对于真正存在多设备并发离线编辑的问题，例如：

```text
个人笔记
人生记录
时间胶囊草稿
文章草稿
```

Platform / LifeBook implementation SHOULD 优先评估 **Automerge 等成熟 Local-first / CRDT 实现**，而不是自行设计通用 CRDT。

但 Automerge：

- 不是 Kindle Adapter 的新层；
- 不是 `baga.sync` 的同义词；
- 不适用于所有数据；
- 不要求 IKP 直接打包 Rust/JS Automerge runtime；
- 不应把其内部 change graph / binary format 暴露给 App，除非未来 Baga 独立标准明确版本化采纳某种互操作协议。

例如：

```text
阅读位置       → 可以使用简单明确的业务 merge
Feed/评论缓存  → Server authoritative + local cache
他人公开笔记   → Server authoritative + local cache
书籍文件       → content hash + file transfer
并发草稿/笔记  → Automerge/CRDT 候选
```

Automerge 在不同 Kindle CPU/ABI/内存条件上的实际采用范围必须经过目标设备测试；不应为了理论统一牺牲老 Kindle 覆盖。

---

# 18. Lifecycle / Power

必须稳定映射：

```text
start
resume
pause
sleep
wake
stop
```

Adapter SHOULD 利用 Kindle 可用系统事件或 KOReader/Homebrew 已验证机制，而不是 App 轮询判断。

需要正确处理：

```text
屏幕休眠
设备唤醒
Framework 重启
Platform 进程重启
设备关机/重启
```

App 的持久状态不得依赖进程永久存在。

---

# 19. Battery / Charging

如果 Kindle 系统可以稳定提供电量与充电状态，声明：

```text
power.battery_level
power.charging_state
```

无法可靠取得时返回 unknown，不伪造。

---

# 20. Frontlight

有前光且可稳定控制的设备 MAY 声明：

```text
light.frontlight
```

有暖光时 MAY 声明：

```text
light.frontlight.temperature
```

底层等级必须归一化为 Baga Ink 逻辑值。

修改前光需要 Platform policy / permission。

---

# 21. Audio / Bluetooth

Kindle 系列硬件差异较大。

Adapter MUST 只按真实设备能力声明：

```text
audio.output
bluetooth.available
bluetooth.audio
bluetooth.input_device
```

“同系列某机型有”不能推断当前设备有。

没有能力就不声明，不以软件模拟假装有硬件。

---

# 22. Diagnostics

Kindle Adapter SHOULD 提供 Platform 内部诊断：

```text
model
firmware
adapter version
cpu / ABI
screen backend
input backend
reader backend/version
data backend/version
network backend
capabilities
homebrew foundation status
```

这些信息可被 Baga Ink Client 用于支持、许可证清单和故障排查。

App 不应把它们作为跨设备业务逻辑。

---

# 23. Baga Ink Client 的 Kindle 识别流程

建议：

```text
USB 连接
  ↓
只读识别设备
  ↓
读取可安全获得的 model / firmware 信息
  ↓
查 Compatibility Database
  ↓
Supported / Experimental / Unsupported
  ↓
若 Supported：选择安装路径
  ↓
验证文件 hash
  ↓
执行必要用户步骤
  ↓
安装 Platform
  ↓
运行 Kindle BICTS smoke tests
```

Client MUST 不因为“看起来像 Kindle”就盲目写入文件。

---

# 24. Home Screen 启动目标

长期用户体验目标：

```text
Kindle Home
  ↓
LifeBook / Baga Ink App entry
```

用户不需要理解 KUAL / MRPI / Shell / KOReader。

但第一阶段 MAY 使用 Homebrew launcher / system integration 作为内部启动桥。

启动方式的演进不得改变 IKP App contract。

---

# 25. Adapter 内部兼容组织

Kindle 系列差异较多，代码内部可以按真实工程边界组织：

```text
Kindle Adapter Common
      │
      ├── Legacy Kindle handling
      ├── soft-float handling
      ├── hard-float/new firmware handling
      └── model/firmware quirks
```

这些是 Kindle Adapter 的内部代码组织，不是向 App 暴露的多套 Platform。

公共逻辑尽量上提；quirk 只处理无法避免的硬件差异。

禁止把每一款 Kindle 做成完全独立平台代码库。

---

# 26. Quirk Database

允许 Platform 内部维护：

```text
model + firmware → quirks
```

例如：

```text
touch inversion
refresh workaround
frontlight range
sleep event difference
Home integration difference
Reader/library workaround
```

Quirk 不属于公共 Capability 名称。

---

# 27. Kindle Compatible Gate

某 Kindle 组合正式标记 Compatible 前 MUST：

- 通过 Base BICTS；
- Kindle Adapter capability 声明真实；
- 声明的 `baga.data` 行为通过事务/恢复测试；
- 声明的 Library bridge 通过权限与 opaque handle 测试；
- 声明的 Reader / Anchor 能力通过相应 BICTS；
- 标准 IKP 能安装/更新/回滚；
- sleep/wake 稳定；
- 不清用户书籍/笔记；
- 显示与输入基本可靠；
- 已知固件范围记录明确。

底层“KOReader 能启动”或“SQLite 能打开数据库”本身都不足以获得 Compatible 标签。

---

# 28. 与 LifeBook 的关系

LifeBook for Kindle 是第一 Reference App。

但 Kindle Adapter / Platform：

- MUST 不写 LifeBook 私有接口；
- MUST 服务所有 IKP App；
- LifeBook 遇到通用需求时 SHOULD 推动标准 API，而不是开后门；
- MAY 通过 LifeBook 的真实场景验证 KOReader / SQLite / Automerge 等实现组合，但实现选择不能泄漏成 LifeBook contract。

---

# 29. 非目标

Kindle Adapter 不负责：

- 定义某个永久越狱方法；
- 替换 Kindle OS；
- 修改 Amazon 云服务；
- 让 IKP 直接执行 Shell；
- 给每个 App 打 Kindle native binary；
- 为单一 LifeBook 功能制造平台私有接口；
- 为每个成熟 Library 建一个新的公共 Provider/Engine 层；
- 自己重新实现 KOReader 已解决的每种文档格式定位算法；
- 自己重新发明通用数据库或 CRDT 算法。

---

# 30. 核心原则 / Core Rule

> **Kindle 的复杂性应该停在 Baga Ink Platform on Kindle、Kindle Adapter 与 Baga Ink Client；复杂性不能向上泄漏给 IKP 开发者。**

更具体地说：

> **开发者只面对统一 `baga.*`；Kindle 实现内部则应大胆、谨慎地复用 KOReader、FBInk、SQLite、Automerge 与 Homebrew 社区已经验证过的优秀轮子，而不把这些轮子变成新的公共架构层。**

---

# 31. Kindle Reference Implementation Mapping / Kindle 参考实现映射

本节给出当前 **Baga Ink API 在 Kindle 上的参考实现映射**，用于指导 Baga Ink Platform / Kindle Adapter 的工程实现和后续 AI/开发者判断“优先复用什么”。

> **本图不是 Baga Ink 公共架构图，也不定义新的软件层。**  
> **KOReader、Automerge、SQLite 等只是 Baga Ink API 在 Kindle 上的具体实现所复用的开源组件。**

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
├─ baga.data
│   └─ SQLite 或同等级成熟事务存储
│
├─ baga.sync
│   ├─ Baga 标准语义：联网 / Wi-Fi / sleep-wake / trigger / retry policy
│   └─ 真正需要并发离线合并的业务场景：可复用 Automerge
│
├─ baga.network
│   └─ 复用成熟 HTTP / TLS / KOReader 已验证网络能力与 Kindle 网络桥接
│
└─ baga.power
    └─ Kindle 系统能力 / KOReader 已有 lifecycle / power 相关实现
```

映射规则：

1. `baga.*` 是第三方 IKP 开发者可依赖的稳定边界；
2. 上述开源组件是 Kindle implementation detail，可整体采用、组合或拆分复用；
3. 某库被采用，不意味着该库的对象模型、API、术语、文件格式自动成为 Baga Ink 标准；
4. 不应因为采用一个库，就额外创造 `KOReader Layer`、`SQLite Provider`、`Automerge Engine` 等公共层；
5. 如果已有成熟组件能可靠实现某项 `baga.*` 语义，SHOULD 优先复用，而不是为了“完全自研”重新造轮子；
6. 如果某成熟组件在特定 Kindle 硬件/固件/ABI 上不适用，可以替换内部实现或降级对应能力，但不改变 `baga.*` 契约；
7. 所有实现最终仍必须通过 BICTS，兼容性由公开 Baga 语义验证，而不是由“采用了某个知名库”自动获得。

未在上图逐项展开的其他 `baga.*` API 同样遵循这一原则：**先寻找成熟、许可证兼容、可验证的实现；仅在确实缺少可用实现时再开发必要代码，而且不因内部实现方式改变 Baga Ink 的公共架构。**