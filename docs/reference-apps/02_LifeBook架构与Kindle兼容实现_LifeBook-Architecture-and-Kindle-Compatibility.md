# LifeBook IKP 架构与 Kindle 兼容实现 / LifeBook IKP Architecture and Kindle Compatibility

> **文档级别：Reference App 技术实现补充 / Reference App Technical Implementation Companion**  
> **状态：Baseline v0.1**  
> **日期：2026-08-23**  
> **适用对象：LifeBook (`lifebook.ikp`) on Baga Ink Platform**  
> **上位文档：`docs/standards/` 全部正式规范**  
> **配套文档：`01_LifeBook参考实现_LifeBook-Reference-App.md`**  
> **本文件不是 Baga Ink Standard，不得覆盖或修改上位标准。**

---

## 0. 目的

本文档总结 LifeBook 墨水屏版本当前确定的技术架构、开源组件选型、Kindle 硬件/固件/ABI 差异处理方式，以及离线优先、阅读、社区内容、其他用户笔记等功能如何落到 Baga Ink Platform。

本文档的核心原则只有一句：

> **LifeBook 只实现 LifeBook；Baga Ink Platform 吸收设备差异；Kindle Adapter 最大化复用 KOReader 与 Kindle Homebrew 生态。**

LifeBook 的最终产品形态不是“KOReader 插件”，也不是“Kindle 私有 App”，而是标准：

```text
lifebook.ikp
```

同一个 IKP 应在所有达到相应 Baga Ink Compatibility 要求的设备上运行。

---

# 1. 规范优先级

本实现必须遵守：

```text
docs/standards/
```

特别是：

```text
01 顶层战略与架构
02 应用标准
03 Baga Ink API
04 Capability Registry
05 Permission Model
06 IKP Package
07 Device Adapter
08 Compatibility Standard
09 UI Specification
10 BICTS
11 Kindle Adapter
20–28 Distribution / Signing / Update
```

优先级：

```text
Baga Ink Standards
        >
01_LifeBook参考实现
        >
本实现补充
        >
LifeBook 代码
```

如果本文档与 Standards 冲突，以 Standards 为准。

---

# 2. 最终架构结论

此前讨论过的：

```text
LifeBook App
  ↓
LifeBook Runtime
  ↓
KOReader
```

**不采用。**

LifeBook 不需要单独的 Runtime，也不需要自己维护 Kindle Compatibility Layer。

正式架构为：

```text
┌────────────────────────────────────────────┐
│          LifeBook — `lifebook.ikp`         │
│                                            │
│ Account / Library / Articles / Q&A         │
│ Comments / Public Notes / My Notes         │
│ Life Records / Time Capsule / AI           │
│ Offline Domain Logic / Sync Merge Logic    │
└───────────────────┬────────────────────────┘
                    │ only baga.*
                    ▼
┌────────────────────────────────────────────┐
│             Baga Ink API                   │
│                                            │
│ app / ui / display / input / device        │
│ storage / network / power / reader         │
│ sync / permissions / log                   │
└───────────────────┬────────────────────────┘
                    ▼
┌────────────────────────────────────────────┐
│          Baga Ink Platform Core            │
│                                            │
│ Baga Lua Profile / IKP / Sandbox           │
│ Permission / UI foundation / Reader        │
│ Package lifecycle / Compatibility hooks    │
└───────────────────┬────────────────────────┘
                    ▼
┌────────────────────────────────────────────┐
│          Baga Ink Kindle Adapter           │
│                                            │
│ display / input / lifecycle / power        │
│ storage / network / frontlight / quirks    │
│ Homebrew integration / reader backend      │
└───────────────────┬────────────────────────┘
                    ▼
┌────────────────────────────────────────────┐
│       Kindle Homebrew Foundation           │
│                                            │
│ KOReader / koreader-base / FBInk           │
│ KPM / Universal Hotfix / system bridge     │
│ KUAL/MRPI compatibility fallback           │
└───────────────────┬────────────────────────┘
                    ▼
                Kindle OS
```

而：

```text
WinterBreak
SpringBreak
Sanctuary
Véra
Legacy routes
```

**不在 LifeBook App 架构内部。**

它们属于设备 Enablement / Installation Route，由 Baga Ink Client 的可更新 Compatibility / Installation Database 管理。

---

# 3. LifeBook IKP 自己真正负责什么

`lifebook.ikp` 只负责产品业务和跨设备逻辑。

推荐目录：

```text
lifebook.ikp
├── manifest.json
├── main.lua
├── src/
│   ├── application/
│   │   ├── bootstrap.lua
│   │   ├── navigation.lua
│   │   └── session.lua
│   ├── domain/
│   │   ├── account/
│   │   ├── library/
│   │   ├── articles/
│   │   ├── qa/
│   │   ├── comments/
│   │   ├── notes/
│   │   ├── life-records/
│   │   ├── time-capsule/
│   │   └── ai/
│   ├── views/
│   │   ├── home/
│   │   ├── library/
│   │   ├── article/
│   │   ├── question/
│   │   ├── comments/
│   │   ├── notes/
│   │   ├── life/
│   │   └── ai/
│   ├── reader/
│   │   ├── reader-service.lua
│   │   └── public-notes.lua
│   ├── persistence/
│   │   ├── repository.lua
│   │   ├── cache.lua
│   │   └── sync-journal.lua
│   └── sync/
│       ├── transport.lua
│       ├── conflict.lua
│       └── merge.lua
├── assets/
├── locales/
└── signature/
```

LifeBook IKP MUST NOT 携带：

```text
Kindle shell bridge
KOReader native binaries
FBInk binaries
Android APK/DEX
Vendor SDK wrapper
Lua interpreter
Device Adapter
Platform Core
CPU ABI-specific business binary
```

---

# 4. LifeBook 产品功能边界

LifeBook 不是单纯 Reader。

核心业务包括：

```text
LifeBook
├── 书库 / 阅读
├── 文章
├── 问答
├── 评论
├── 其他用户公开笔记
├── 我的笔记 / 高亮
├── 用户主页 / 社区内容
├── 人生记录
├── 时间胶囊
├── AI
└── 跨设备同步
```

因此 KOReader 的正确位置是：

```text
LifeBook
├── Article / Q&A / Comment UI  → baga.ui
├── Life / AI UI                → baga.ui
└── Book Reader                 → baga.reader
                                      │
                                      ▼
                              Kindle implementation
                                      │
                                      ▼
                                   KOReader
```

LifeBook **不是**：

```text
LifeBook → KOReader private UI → Kindle
```

长期 API 必须保持：

```text
LifeBook → baga.* → Platform
```

---

# 5. E-Ink UI 的实现决定

LifeBook IKP 使用：

```text
baga.ui
baga.input
baga.display
```

而不是直接 import KOReader widget。

但 Kindle Platform 的第一实现可以在内部大量复用 KOReader：

```text
LifeBook baga.ui Page/List/Text/Dialog
                │
                ▼
       Baga UI implementation
                │
                ▼
 KOReader Lua UI / Widget / UIManager
                │
                ▼
          Kindle framebuffer
```

这能同时满足：

1. LifeBook 不绑定 KOReader 私有 API；
2. Kindle 不重写一整套 E-Ink GUI；
3. 未来 Android E-Paper 可以使用完全不同 UI backend；
4. 未来 Kindle 也可以替换底层 renderer，而不重写 LifeBook。

LifeBook 页面原则：

- 高对比度；
- 页面式/稳定布局优先；
- 长列表虚拟化；
- Touch 与 Focus 同时成立；
- 物理翻页键映射语义动作；
- 不依赖颜色；
- App 只给 Display Intent；
- ghosting / waveform 归 Platform/Adapter。

---

# 6. Book Reader 的实现决定

Kindle 上第一 Reader backend 正式选择：

> **KOReader / koreader-base**

公开关系严格保持：

```text
LifeBook
   │
   ▼
baga.reader
   │
   ▼
Baga Reader Abstraction
   │
   ▼
KOReader-derived Kindle Reader Backend
```

LifeBook 不依赖：

```text
ReaderUI private object
KOReader plugin object
KOReader internal path
KOReader private annotation schema
```

需要标准化的能力通过 `baga.reader` 演进。

---

# 7. 具体采纳的开源组件地图

## 7.1 Production / First-class

| 项目 | 仓库 | 许可证 | 所在层 | LifeBook/Baga Ink 用途 | 结论 |
|---|---|---|---|---|---|
| KOReader | https://github.com/koreader/koreader | AGPL-3.0 | Kindle Platform / Reader Backend | EPUB/PDF/MOBI/FB2 等阅读、ReaderUI、Kindle 输入/显示经验、Lua UI 基础 | **正式采纳** |
| koreader-base | https://github.com/koreader/koreader-base | AGPL-3.0 | Kindle Platform / Device foundation | LuaJIT、文档引擎、底层 Kindle target、native device foundation | **正式采纳** |
| FBInk | https://github.com/NiLuJe/FBInk | GPL-3.0-or-later | Kindle Adapter / bootstrap / diagnostics | framebuffer、文字/图片输出、刷新辅助、故障提示、低层显示 fallback | **正式采纳为底层工具，不作为 LifeBook UI API** |
| KPM | https://github.com/KindleModding/KPM | GPL-3.0 | Kindle Homebrew foundation | Kindle 侧 Platform 组件安装/启动/卸载生命周期 | **采纳为 Platform 内部组件；不是 IKP 格式** |
| Universal Hotfix | https://github.com/KindleModding/Hotfix | GPL-3.0 | Kindle Homebrew foundation | armel/armhf 基础、KPM、系统桥、跨架构持久化 | **优先复用** |
| KindleTool | https://github.com/NiLuJe/KindleTool | GPL-3.0+ | Build / Client tooling | Kindle update container、设备/包格式、工程工具链 | **采纳为开发/部署工具，不进入 lifebook.ikp** |
| koxtoolchain | https://github.com/koreader/koxtoolchain | 开源；按仓库许可证 | Build tooling | armel / armhf 交叉编译环境 | **需要 native Platform 组件时复用** |

这些项目预计可省掉的不是 LifeBook 业务代码，而是大量最昂贵的底层工作：

```text
阅读排版与格式支持
Kindle framebuffer
Touch / physical input
E-Ink refresh quirks
ARM toolchain
Kindle package/update format
Homebrew component lifecycle
跨固件/架构基础适配
```

## 7.2 Compatibility / Fallback

| 项目 | 用途 | 决策 |
|---|---|---|
| KUAL | 传统 Homebrew Launcher | 仅内部维护/故障 fallback；正常用户不经过 KUAL 打开 LifeBook |
| MRPI | 传统 Kindle package installation bridge | 兼容旧生态；不成为 IKP App contract |
| sh_integration | 从 Kindle Library 启动 shell/app 的集成路径 | **技术上非常有价值，但正式打包前必须完成许可证与长期维护审查** |

长期产品体验目标始终是：

```text
Kindle Home
    ↓
LifeBook 图标/入口
    ↓
LifeBook
```

用户不需要知道 KUAL、MRPI、KPM、Hotfix、KOReader。

## 7.3 不作为主架构

| 项目 | 原因 | 决策 |
|---|---|---|
| Mesquito | 固件范围受限、Web Runtime 老、项目已归档 | 可研究/兼容，不作为 LifeBook 主 UI |
| KWebBrew | 依赖特定旧 Web 环境 | 不作为 Universal Kindle UI |
| PEKI | 许可证存在 NonCommercial 条款，不适合商业 LifeBook 默认打包 | 不采纳 |
| slint-kindle-backend | 架构很漂亮，但设备覆盖仍有限 | R&D 候选，不作为当前 Universal Kindle backend |
| KindleForge / 其他 App Store | 参考 ABI / UI / 更新思路 | 不作为 Baga Ink Platform 基础 |

---

# 8. 许可证边界

LifeBook 本身是 IKP，原则上不直接静态合并 Kindle native 项目。

推荐边界：

```text
lifebook.ikp
    │
    │ public Baga API
    ▼
Baga Ink Platform
    │
    ├── KOReader / AGPL
    ├── FBInk / GPL
    ├── KPM / GPL
    └── Hotfix / GPL
```

这样可把许可证责任集中在 Platform / Adapter 层，而不是让每个 IKP App 处理设备端 copyleft 依赖。

发布前仍应对所有实际打包方式做一次正式开源许可证审计。

---

# 9. Kindle 硬件与 ABI 分层

LifeBook 不按每个 Kindle 型号维护一套 App。

Kindle Adapter 使用：

```text
Common Kindle Adapter
        │
        ├── legacy backend
        ├── classic soft-float backend
        ├── PW2+ soft-float optimized backend
        ├── hard-float backend
        └── model/firmware quirks
```

KOReader/KOReader Base 当前提供的 target 直接成为重要工程参考：

| Kindle 平台族 | KOReader target | 典型范围 | Baga Ink 实现 |
|---|---|---|---|
| Legacy | `kindle-legacy` | Kindle 2 / Kindle 3 / DXG | Legacy Adapter backend；低资源 profile；键盘/按键优先 |
| Classic | `kindle` | Kindle 4 / Touch / PW1 时代 | soft-float common backend |
| PW2+ soft-float | `kindlepw2` | Paperwhite 2 及之后、仍处于 soft-float 固件的设备 | soft-float optimized backend |
| Hard-float | `kindlehf` | **Firmware >= 5.16.3** | armhf backend；新的 native component 必须使用 hard-float build |

核心规则：

> **5.16.3 是重要 ABI 边界。**

Firmware `>= 5.16.3` 的 Kindle 进入 hard-float 世界；旧 soft-float extension 不应被假设可以继续工作。

但：

```text
lifebook.ikp
```

不因为 armel / armhf 发生变化。

变化只存在于：

```text
Platform binary
Kindle Adapter backend
KOReader package
FBInk / bridge binaries
Homebrew foundation
```

---

# 10. 不同硬件能力如何处理

LifeBook 不判断型号，而查询 Capability。

## 10.1 Touch Kindle

```text
input.touch = true
```

LifeBook 可启用触控菜单、直接点击、选择文本。

## 10.2 带物理翻页键的 Kindle

例如部分 Keyboard / Voyage / Oasis 等设备，可声明：

```text
input.physical_page_key
```

映射为：

```text
page_next
page_previous
```

LifeBook 不读取私有 keycode。

## 10.3 非触摸旧 Kindle

只要 Adapter 能提供：

```text
input.navigation
```

LifeBook Base UI 仍应可通过 Focus 模型操作。

这也是为什么 `baga.ui` 的 Focus 不是可选装饰，而是跨老 Kindle 的关键设计。

## 10.4 Kindle Scribe

Pen 不能因为设备“有笔”就自动进入 Universal 功能。

只有 Kindle Adapter 已稳定实现并通过 BICTS 时才声明：

```text
input.pen
input.pen.pressure
input.pen.eraser
input.pen.low_latency
```

LifeBook 的手写笔记是渐进增强，不影响 Base LifeBook。

## 10.5 Colorsoft / 彩色 Kindle

Adapter 通过测试后声明：

```text
display.color
```

LifeBook 可以增强文章图片、标签和书封，但核心语义必须在黑白 Kindle 完整可用。

## 10.6 Audio / Bluetooth

不同 Kindle 差异很大。

只按真实能力声明：

```text
audio.output
bluetooth.available
bluetooth.audio
bluetooth.input_device
```

LifeBook 不依据代数猜测。

---

# 11. 固件版本处理

兼容性对象必须是：

```text
Device Model
+ Firmware Range
+ Baga Platform Version
+ Kindle Adapter Version
+ BICTS Version
```

同一个 Kindle 型号可能出现：

```text
Firmware A → Compatible
Firmware B → Experimental
Firmware C → Unsupported
```

因此 LifeBook App 内禁止出现：

```lua
if firmware >= "5.16.4" then ... end
```

固件差异归：

```text
Kindle Adapter
Compatibility Database
Quirk Database
Installation Route Database
```

---

# 12. WinterBreak / SpringBreak / Sanctuary / Véra 的正确位置

这些项目是 Kindle Enablement Routes，不是 LifeBook library。

正确关系：

```text
WinterBreak / SpringBreak / Sanctuary / Véra
                  │
                  ▼
      supported Homebrew foundation
                  │
                  ▼
          Baga Ink Platform
                  │
                  ▼
              lifebook.ikp
```

它们的支持范围会持续变化，所以 **绝不写死进 LifeBook，也不写死进 Baga Ink API contract**。

截至本文件日期，公开社区资料体现了以下事实：

- WinterBreak/Mesquito 路线不适用于 firmware `5.18.1+`；
- WinterBreak2 是部分 `<5.16.4` 组合的替代路线；
- SpringBreak、Sanctuary、Véra 针对更新型号/固件提供新的入口；
- Véra 当前引导根据型号 + firmware 动态选择 payload，公开页面覆盖较新的 `5.17–5.19.x` 区间；
- 具体支持组合应始终交给可更新的 Installation Route Database / Wizard，而不是由本文冻结。

对普通用户的产品文案不使用复杂底层术语，只显示：

```text
Compatible
Experimental
Unsupported
```

---

# 13. Kindle OS / 系统版本差异

Kindle 端需要吸收的差异包括：

```text
soft-float ↔ hard-float
USB Mass Storage ↔ MTP
不同 framebuffer / waveform
不同 touch controller
不同物理按键
不同 frontlight / warm light
不同 sleep/wake event
不同 system service / LIPC behavior
不同 Home UI / launcher integration
```

这些全部停在：

```text
Kindle Adapter
```

或：

```text
Baga Ink Client installation route
```

不得传播到 LifeBook Domain Core。

---

# 14. LifeBook 离线优先架构

离线优先是 LifeBook 的一级设计原则。

核心状态机：

```text
User action
   ↓
Local durable write
   ↓
UI confirms success
   ↓
Sync journal / queue
   ↓
when_online / wifi / charging policy
   ↓
LifeBook Server
   ↓
ACK / conflict / merge
   ↓
Local durable state
```

离线时应支持：

```text
打开 LifeBook
本地书库
继续阅读
查看缓存文章/问答/评论
查看缓存的其他用户笔记
创建/编辑自己的笔记
创建人生记录
允许离线的时间胶囊编辑
```

平台负责：

```text
baga.network
sleep / wake
power policy
baga.sync trigger
standard errors
```

LifeBook 负责：

```text
业务数据模型
幂等 ID
本地 revision
冲突检测
业务 merge
历史版本
同步 journal
retry semantics
```

---

# 15. 本地数据实现边界

当前 Standards 已提供：

```text
baga.storage
baga.sync
```

但尚未冻结事务型数据库 API。

因此当前合规实现原则是：

1. LifeBook Domain 只依赖自己的 Repository interface；
2. 第一阶段通过 `baga.storage` 实现可移植 durable store；
3. 可以在 IKP 内打包纯 Lua 数据/序列化库；
4. 不把 SQLite native binary 带进 Universal IKP；
5. 若实际验证表明需要统一事务数据库，应先提出新的 Baga Ink 标准 API，再由 Platform 在 Kindle/Android 分别实现。

推荐代码边界：

```text
LifeBook Domain
      │
      ▼
LifeBook Repository Interface
      │
      ▼
Baga Storage-backed implementation
```

这样未来出现标准事务存储 API 时只替换 Repository implementation。

---

# 16. 文章 / 问答 / 评论

这些内容不是 Book Reader 文件，不需要转换 EPUB 再交给 KOReader。

正确实现：

```text
LifeBook Server / Local Cache
           │
           ▼
     LifeBook Domain
           │
           ▼
        baga.ui
```

长文章可采用：

```text
paged
step_scroll
```

并遵循 E-Ink refresh intent。

---

# 17. “其他用户的笔记”设计

这是 LifeBook 的重要差异化功能。

用户阅读一本书时：

```text
Book content      → baga.reader
Public notes      → LifeBook Domain/API
```

二者必须通过稳定的 **Content Anchor** 关联，而不是依赖 KOReader 内部页面号或私有对象。

长期目标：

```text
Book fingerprint
+ canonical content location
+ quote/context evidence
        │
        ▼
Cross-device Reader Anchor
        │
        ├── Kindle/KOReader
        └── Android/other Reader backend
```

当前 `baga.reader` 规范尚未完整定义跨 Reader backend 的稳定 Anchor。

因此这是一个明确的 **标准演进需求**：

> 应在 Reader API / Capability Registry 中定义可跨 EPUB 渲染引擎和设备稳定定位正文片段的标准 anchor 语义。

在标准化前，LifeBook 不应把 KOReader 私有 annotation location 固化为云端永久协议。

---

# 18. Reader / Library 相关标准缺口

当前 Standards 中已经存在：

```text
storage.user_library
library.read
library.write
baga.reader
```

同时 Kindle Adapter 文档也描述了 “Baga Library abstraction”。

但 `03_API规范` 当前没有正式 `baga.library` namespace。

因此在实现 LifeBook 私人书库前，应通过标准治理确认以下一种方案：

### 方案 A

正式增加：

```text
baga.library
```

负责标准书库枚举、导入、元数据和资源句柄。

### 方案 B

明确规定这些能力归 `baga.reader + baga.storage` 的组合，不再出现未注册的 “Baga Library API” 表述。

在 Standards 完成决定前，LifeBook IKP 不创造私有 `baga.library` API。

---

# 19. 首页启动设计

产品目标：

```text
Kindle Home
    ↓ one action
LifeBook
```

用户心理模型必须是：

> “我的 Kindle 上安装了 LifeBook App。”

而不是：

```text
KUAL → KOReader → Plugin → LifeBook
```

具体实现归 Kindle Adapter / Platform integration。

优先研究：

```text
Kindle AppMgr / Home registration
sh_integration 类 Library entry
Platform launcher bridge
```

KUAL 只作为兼容 fallback / maintenance entry。

LifeBook IKP 不知道启动入口是如何创建的。

---

# 20. 更新与回滚

LifeBook 更新完全遵守 IKP 标准，不使用 KPM package 代替 IKP。

```text
Signed lifebook.ikp
        │
        ▼
Verify identity / signature
        │
        ▼
Stage new version
        │
        ▼
Health check
   ┌────┴────┐
 success   failure
   │           │
 activate    rollback
```

必须满足：

```text
App 包与用户数据分离
更新失败保留旧版本
不删除用户书籍/笔记
数据 schema 变更可回滚或明确阻止回滚
release_sequence 单调递增
```

KPM 只管理 Kindle Platform/Homebrew 侧组件，不管理 LifeBook 作为 IKP 的身份与签名语义。

---

# 21. LifeBook Manifest Capability 方向

LifeBook Base 版本应尽量只要求 Base Profile。

建议 Required：

```text
display.basic
input.navigation
storage.app_sandbox
power.sleep_wake
platform.lifecycle
```

根据实际版本需要，可加入：

```text
reader.open
```

Optional：

```text
input.touch
input.physical_page_key
display.partial_refresh
display.fast_refresh
display.grayscale
display.color
network.wifi
network.https
light.frontlight
light.frontlight.temperature
input.pen
audio.output
bluetooth.available
```

网络是否为 Required 应慎重：如果 LifeBook 已完成初次登录，本地阅读/缓存功能必须在无网络时仍能启动；因此“当前 online”不能成为启动条件。

---

# 22. Permission 方向

按功能渐进申请，不一次全开。

基础版本可能需要：

```text
network
library.read
notes.read
notes.write
```

只有执行对应功能时才加入：

```text
library.write
user_files.read
user_files.write
audio.output
bluetooth
frontlight.control
power.keep_awake
```

权限新增必须作为重要版本变化向用户展示。

---

# 23. 不同 Kindle 的功能降级策略

| 设备条件 | LifeBook 行为 |
|---|---|
| 低 RAM / 老 CPU | 减少缓存、缩小图片、限制同时保留页面、减少后台任务 |
| 无 Touch | Focus + physical navigation |
| 有 Touch | 点击、选择、软键盘增强 |
| 无 Fast Refresh | 所有页面退化为 TEXT/QUALITY，不影响业务 |
| 无 Color | 黑白/灰阶 UI 完整可用 |
| 无 Pen | 不显示手写入口 |
| 无 Audio | 隐藏 TTS/audio 功能 |
| 无 Bluetooth | 隐藏蓝牙输入/音频增强 |
| Wi-Fi 关闭 | 完整离线启动；只暂停网络同步 |
| sleep/wake 频繁 | 本地状态优先；wake 后重新判断 capability/network |

核心原则：

> **能力少 = 功能渐进降级，不等于维护另一份 LifeBook。**

---

# 24. Compatibility / Quirk 设计

Kindle Adapter 内部允许：

```text
model + firmware → quirks
```

例如：

```text
touch coordinate correction
refresh workaround
frontlight range
sleep event workaround
Home integration method
network service difference
```

但 Quirk 不能变成公开 Capability 名。

正式兼容必须通过：

```text
BICTS
```

而不是“KOReader 能启动所以 LifeBook 就算支持”。

---

# 25. 第一阶段实现建议

## Phase 1 — Platform proof

目标：证明同一个 LifeBook IKP 在至少一台 Kindle 和一台 Android E-Paper 跑通。

```text
LifeBook Home
baga.ui
lifecycle
storage
offline start
network
permission
```

## Phase 2 — Reading

```text
Library bridge
baga.reader → KOReader
reading position
highlight / own notes
sleep/wake resume
basic sync
```

## Phase 3 — LifeBook Content

```text
Articles
Q&A
Comments
Public Notes
Offline content cache
```

## Phase 4 — Life features

```text
Life Records
Time Capsule
richer conflict handling
version history
```

## Phase 5 — AI / enhanced hardware

```text
AI
Scribe pen
Color
Audio/TTS
Bluetooth input
```

---

# 26. 当前冻结的技术决策

以下可视为当前架构 baseline：

1. **LifeBook 的正式应用包是 `lifebook.ikp`。**
2. **LifeBook 不拥有独立 Runtime。**
3. **LifeBook 不直接适配 Kindle。**
4. **LifeBook Universal App 只调用 `baga.*`。**
5. **Kindle Reader backend 第一选择 KOReader。**
6. **Kindle E-Ink UI 第一实现允许在 Platform 内复用 KOReader Lua UI/widget/UIManager。**
7. **FBInk 是 Adapter/bootstrap/diagnostics 底层工具，不是 LifeBook API。**
8. **KPM/Hotfix 属 Kindle Platform/Homebrew 基础，不是 IKP 应用格式。**
9. **KUAL/MRPI 只作为内部兼容/fallback，不成为用户日常路径。**
10. **WinterBreak / SpringBreak / Sanctuary / Véra 只属于 Enablement Route Database。**
11. **5.16.3 是 Kindle soft-float/hard-float 的关键工程边界；IKP 本身不随 ABI 分叉。**
12. **所有型号/固件差异进入 Kindle Adapter + Compatibility/Quirk DB。**
13. **LifeBook 必须 offline-first。**
14. **文章、问答、评论由 LifeBook + `baga.ui` 渲染，不走 Book Reader。**
15. **其他用户笔记由 LifeBook 业务层管理，通过标准 Reader Anchor 与书中正文关联。**
16. **首页目标是一眼可见的 LifeBook 入口，一次操作打开；KOReader/KUAL 等对普通用户隐身。**
17. **更新使用 IKP signing/staging/rollback，不以 Kindle Homebrew package identity 代替 IKP identity。**

---

# 27. 需要进入 Standards 治理的后续问题

不是 LifeBook 私有开后门，而应进入 Standards：

### 27.1 Transactional Local Data

需要评估是否增加标准化：

```text
transaction / kv / embedded database
```

能力，以更好支撑 offline-first 大型应用。

### 27.2 Reader Content Anchor

需要标准化：

```text
EPUB/PDF 内容稳定定位
跨 Reader backend 的 note/highlight anchor
quote/context fallback
```

这是“其他用户笔记”真正跨 Kindle/Android 成立的关键。

### 27.3 Library API 边界

需要解决当前 `storage.user_library` / `library.* permission` 与 `03_API` 未注册 `baga.library` namespace 之间的规范空白。

在这些内容进入正式 Standards 前，LifeBook 不创建事实上的私有 Baga API。

---

# 28. 最终一句话架构

> **LifeBook 是标准 `lifebook.ikp`；Baga Ink Platform 是跨设备应用平台；Kindle Adapter 用 KOReader/koreader-base/FBInk/Homebrew 生态吸收十几年 Kindle 的硬件、ABI、固件和系统差异；WinterBreak、SpringBreak、Sanctuary、Véra 只负责把具体设备带入统一 Homebrew 环境。LifeBook 自己只专注文章、问答、评论、社区笔记、阅读、人生记录、时间胶囊、AI 与离线同步。**

---

# 29. 外部实现参考

- KOReader: https://github.com/koreader/koreader
- KOReader Base: https://github.com/koreader/koreader-base
- FBInk: https://github.com/NiLuJe/FBInk
- KindleTool: https://github.com/NiLuJe/KindleTool
- KOReader Toolchain: https://github.com/koreader/koxtoolchain
- KindleModding KPM: https://github.com/KindleModding/KPM
- KindleModding Universal Hotfix: https://github.com/KindleModding/Hotfix
- KindleModding SH Integration: https://github.com/KindleModding/sh_integration
- KindleModding documentation: https://kindlemodding.org/

这些外部项目的具体支持范围和许可证可能变化；实际发布版本必须锁定 commit/tag，并由 Baga Ink Platform 的 dependency manifest 记录。