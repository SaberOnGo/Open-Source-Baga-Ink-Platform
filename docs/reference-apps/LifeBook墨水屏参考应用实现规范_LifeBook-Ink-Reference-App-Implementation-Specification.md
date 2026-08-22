# LifeBook 墨水屏参考应用实现规范 / LifeBook Ink Reference App Implementation Specification

> **文档级别：参考应用实现规范 / Reference App Implementation Specification**  
> **状态：Baseline v0.1**  
> **日期：2026-08-22**  
> **适用对象：LifeBook on Baga Ink Platform**  
> **本文件不是 Baga Ink Standard，不得覆盖或修改上位标准。**

---

## 0. 文档目的

本文档规定 **LifeBook** 作为 Baga Ink Platform 旗舰参考应用（Reference App）的实现边界、模块划分、跨设备原则、UI/Reader/同步策略，以及它与 Baga Ink Std 的关系。

LifeBook 的任务不是创造另一套平台标准，而是：

> **用一个真实、完整、长期维护的旗舰应用实现和验证 Baga Ink Std，证明同一套 Baga Ink App 代码可以运行在 Kindle 与多种 Android E-Paper 设备上。**

因此，本文件解决的是：

```text
Baga Ink Std 已经定义了什么
        │
        ▼
LifeBook 应该怎样按标准实现
        │
        ▼
通过真实产品验证 API / Capability / Permission / IKP / Adapter 边界
```

如果 LifeBook 的需求与现有 Baga Ink 标准发生冲突，**LifeBook MUST 服从上位标准**。如果确有新的跨设备公共能力需要标准化，应先通过 Baga Ink 标准治理流程更新对应标准，再由 LifeBook 使用；不得通过 LifeBook 私有接口静默绕过标准。

---

# 1. 上位规范与优先级

LifeBook 实现 MUST 遵守 `docs/standards/` 中的正式规范。

当前上位文件包括：

```text
00_规范总览_Baga-Ink-Standards-Index.md
01_顶层战略与架构_Baga-Ink-Platform-Strategy.md
02_应用标准_Baga-Ink-App-Standard.md
03_API规范_Baga-Ink-API-Specification.md
04_能力注册表_Baga-Ink-Capability-Registry.md
05_权限模型_Baga-Ink-Permission-Model.md
06_IKP应用包规范_IKP-Package-Specification.md
07_设备适配器规范_Baga-Ink-Device-Adapter-Specification.md
08_兼容性标准_Baga-Ink-Compatibility-Standard.md
```

优先级原则：

```text
Baga Ink Standards
        >
本 LifeBook 实现规范
        >
LifeBook 具体代码与产品实现
```

本文中的 MUST / SHOULD / MAY 沿用 Baga Ink 顶层规范含义。

---

# 2. LifeBook 的正式定位

## 2.1 LifeBook 是 App，不是 Platform

LifeBook 是：

> **Baga Ink Platform 上的旗舰 App / Reference App。**

LifeBook MUST NOT 被描述或实现为：

- Baga Ink Platform 本身；
- Baga Ink Platform Core；
- Baga Ink Device Adapter；
- Baga Ink SDK；
- Baga Ink Market；
- 独立的通用 Runtime；
- Kindle / Android Vendor SDK 的统一封装层。

用户可见正式名称保持：

> **LifeBook**

需要区分 Kindle 产品版本时，可以使用上位标准已经定义的描述：

> **LifeBook for Kindle**

“LifeBook Ink App”在工程讨论中可以表示 LifeBook 的墨水屏应用实现，但不替代正式产品名称。

## 2.2 LifeBook 是 Baga Ink 的 Reference App

LifeBook SHOULD 同时承担两类职责：

1. 提供真正可长期使用的 LifeBook 产品功能；
2. 作为 Baga Ink 的真实参考应用，持续验证跨设备应用边界是否成立。

判断标准：

> 如果 LifeBook 为 Kindle、BOOX、iReader、Bigme 等设备维护不同的核心业务分支，那么 Baga Ink 的统一应用边界尚未实现。

---

# 3. 正确的总体架构

LifeBook 的标准关系如下：

```text
                Baga Ink Standards
                       │
                       ▼
              Baga Ink App Standard
                       │
                       ▼
                 LifeBook App
                `lifebook.ikp`
                       │
                 only `baga.*`
                       │
                       ▼
                Baga Ink API
                       │
                       ▼
             Baga Ink Platform Core
                       │
                       ▼
             Baga Ink Device Adapter
                 ┌─────┴─────┐
                 │           │
                 ▼           ▼
              Kindle      Android E-Paper
                              │
                   ┌──────────┼──────────┐
                   │          │          │
                Generic    iReader     BOOX
                Android      /掌阅       /文石
                   │          │          │
                  ...       Moaan      Hanvon
                             /墨案       /汉王
                                         │
                                       Bigme
```

核心规则：

> **LifeBook 适配 Baga Ink API；设备适配 Baga Ink Platform。LifeBook 不直接适配设备。**

---

# 4. 对此前讨论架构的标准化修正

此前讨论曾使用过类似结构：

```text
LifeBook E-Ink.apk / .ipk
├── Baga Ink Platform Core
├── E-Ink UI
├── Book Reader
└── Device Adapter
    ├── Generic AOSP
    ├── iReader
    ├── BOOX
    ├── Moaan
    ├── Hanvon
    └── Bigme
```

按照当前 Baga Ink Std，该表达 MUST 修正。

## 4.1 `.apk` / `.ipk` 修正为 `.ikp`

LifeBook 作为 Baga Ink Universal App 的标准应用包为：

```text
lifebook.ikp
```

IKP 是跨 Kindle 与 Android E-Paper 的应用包格式。

Android 设备上，**Baga Ink Platform 本身** MAY 以 Android APK 等系统允许的形式安装；但 LifeBook 的 Universal App 逻辑不应因此变成一套 Android 专用 APK 业务实现。

同理，Kindle 的 Platform 安装方式可以完全不同，但 LifeBook App 层仍应尽可能使用同一份 IKP 与同一份应用代码。

## 4.2 “Baga Ink Platform Core”不属于 LifeBook

LifeBook 内部的账号、文章、问答、笔记等属于：

> **LifeBook Application / Domain Core**

而不是 Baga Ink Platform Core。

`Baga Ink Platform Core` 是所有 Baga Ink App 共享的平台层，必须独立于 LifeBook 私有业务。

## 4.3 Device Adapter 不属于 LifeBook

Generic Android、iReader、BOOX、Moaan、Hanvon、Bigme、Kindle 等 Device Adapter：

> **属于 Baga Ink Platform，不属于 LifeBook。**

LifeBook MUST NOT 包含：

```text
if vendor == "BOOX" then ...
if vendor == "iReader" then ...
if is_kindle then ...
```

作为核心业务兼容逻辑。

LifeBook MUST 使用 Capability：

```lua
if baga.device.has("display.fast_refresh") then
    -- 使用快速交互策略
end

if baga.device.has("input.pen") then
    -- 启用标准笔输入相关功能
end
```

设备品牌与私有 API 的处理只能发生在 Platform / Device Adapter 层。

## 4.4 Reader 不直接绑定 KOReader internals

LifeBook SHOULD 使用：

```text
LifeBook
   │
   ▼
baga.reader
   │
   ▼
Reader implementation
   │
   ├─ KOReader-based implementation
   ├─ MuPDF-based implementation
   └─ future implementation
```

LifeBook MUST NOT 因某个平台内部复用了 KOReader，就直接把 KOReader 私有 Lua 对象作为自身长期 API 依赖。

---

# 5. LifeBook App 内部模块

LifeBook 建议按应用职责组织，而不是按设备品牌组织。

概念结构：

```text
LifeBook (`lifebook.ikp`)
│
├── LifeBook Application Core
│   ├── Account / Session
│   ├── Library
│   ├── Articles
│   ├── Q&A / Comments
│   ├── Notes
│   ├── Life Records
│   ├── Time Capsule
│   ├── AI
│   └── Sync Domain Logic
│
├── LifeBook E-Ink UI
│   ├── Library UI
│   ├── Reader-related UI
│   ├── Article UI
│   ├── Q&A / Comment UI
│   ├── Notes UI
│   ├── Life Record UI
│   ├── Time Capsule UI
│   └── AI UI
│
├── LifeBook Reader Integration
│   └── `baga.reader`
│
└── Baga Ink API Integration
    ├── baga.app
    ├── baga.ui
    ├── baga.display
    ├── baga.input
    ├── baga.device
    ├── baga.storage
    ├── baga.network
    ├── baga.power
    ├── baga.reader
    ├── baga.sync
    ├── baga.permissions
    └── baga.log
```

模块边界原则：

- Domain Core SHOULD 不知道当前运行在 Kindle 还是 Android；
- UI SHOULD 面向 Baga Ink UI / Display 语义；
- Reader Integration SHOULD 面向 `baga.reader`；
- Sync Domain Logic 可以拥有 LifeBook 自己的数据合并规则，但底层调度、网络状态与平台生命周期应使用 Baga Ink API；
- Device / Vendor 私有逻辑 MUST NOT 进入 LifeBook IKP。

---

# 6. LifeBook Application Core

## 6.1 Account / Session

LifeBook 可以拥有自己的用户账户与云服务账户体系。

账号逻辑属于 LifeBook 业务层，而不是 Baga Ink Platform 账号标准。

实现 MUST：

- 通过 `baga.network` 访问 LifeBook 服务端；
- 正确处理长期离线；
- 不把“必须在线登录”作为已经登录用户每次启动 App 的前提；
- 不通过 Android Context、Kindle Shell 或 Vendor API 获取网络；
- 不把认证 token、用户隐私数据写入普通日志。

如果未来 Baga Ink 标准定义统一 Secret Storage / Account API，LifeBook SHOULD 迁移到该标准能力。

## 6.2 Library / Book Data

LifeBook SHOULD 通过 Baga Ink 的 Library / Reader / Storage 标准能力访问书籍。

LifeBook MUST NOT：

- 直接扫描 Kindle `/documents` 作为跨设备正常逻辑；
- 直接扫描 Android 厂商私有书库路径；
- 假设所有设备拥有相同真实文件系统结构。

用户书库访问必须遵守 `library.read` / `library.write` 等 Permission 规则。

## 6.3 Articles / Q&A / Comments

文章、问答和评论属于 LifeBook 网络业务模块。

它们 SHOULD：

- 支持离线缓存；
- 支持断网后继续浏览已经缓存的内容；
- 避免高频后台轮询；
- 在网络恢复时再进行增量更新；
- 为墨水屏优先提供分页或低重绘交互，而不是依赖连续动画式信息流。

## 6.4 Notes

LifeBook Notes 包括阅读标注、用户笔记以及与 LifeBook 内容相关的笔记能力。

若使用 Baga Ink 标准笔记资源，必须遵守：

```text
notes.read
notes.write
```

权限模型。

笔记内容的云同步、冲突合并和版本管理属于 LifeBook Domain Logic；不得因设备不同而采用不同数据语义。

## 6.5 Life Records / 人生记录

人生记录属于 LifeBook 私有业务能力。

其数据模型 SHOULD：

- offline-first；
- 本地修改先落盘；
- 网络恢复后再同步；
- 不因睡眠、断网或 App 被系统终止丢失已经确认的用户输入。

## 6.6 Time Capsule / 时间胶囊

时间胶囊属于 LifeBook 私有业务能力，不应被误写成 Baga Ink 标准 API。

需要网络、时间、存储等平台能力时，仅通过 Baga Ink 公开能力获得。

## 6.7 AI

AI 是 LifeBook 业务能力，不属于 Baga Ink Platform 的强制组成部分。

LifeBook AI SHOULD：

- 通过标准网络 API 调用服务；
- 在网络不可用时明确降级；
- 不让 AI 网络请求阻塞基本阅读功能；
- 避免高频刷新造成墨水屏功耗与残影问题；
- 将流式输出节奏适配电子纸显示，而不是照搬手机端逐 token 高频重绘。

---

# 7. E-Ink UI 实现原则

LifeBook 的 UI 是专门为 E-Ink 产品设计的独立 UI，不应直接复制普通 Android 手机 App UI。

但实现边界仍然是：

```text
LifeBook UI
    │
    ▼
baga.ui / baga.input / baga.display
    │
    ▼
Platform
    │
    ▼
Device Adapter
```

## 7.1 UI 基本要求

LifeBook SHOULD：

- 以高对比度黑白 / 灰阶为默认设计；
- 避免无意义动画；
- 避免持续滚动动画；
- 优先翻页、分页和稳定静态布局；
- 减少大面积高频重绘；
- 使用适合墨水屏的大触控目标；
- 支持 `page_next` / `page_previous` 等语义输入；
- 让无快速刷新能力的设备仍然可以完成核心操作；
- 对彩色、手写、快速刷新等能力做 Optional Capability 增强，而不是将它们变成默认前提。

## 7.2 Display 只表达意图

LifeBook MAY 请求：

```text
AUTO
TEXT
QUALITY
FAST
ANIMATION
```

但这些只是显示意图。

LifeBook MUST NOT：

- 使用 BOOX waveform ID；
- 使用 iReader 私有刷新模式编号；
- 直接控制 Kindle framebuffer；
- 在 App 中自己维护 Vendor 刷新 SDK。

真实刷新策略由 Platform / Adapter 决定。

## 7.3 残影控制

LifeBook 可以根据页面语义表达“此处需要质量刷新”或“此处适合快速交互”，但残影累积、周期性全刷以及 Vendor waveform 映射属于平台层职责。

---

# 8. Reader 实现

阅读器是 LifeBook 的核心功能之一，但 Reader Engine 本身不应成为 LifeBook 与某个底层开源项目的永久耦合点。

标准调用关系：

```text
LifeBook Book/Reader UI
          │
          ▼
      baga.reader
          │
          ▼
   Reader implementation
```

LifeBook 第一阶段 SHOULD 以 Baga Ink Reader API 支持的格式为准逐步覆盖：

```text
EPUB
PDF
TXT
MOBI / AZW 等在 Platform Reader 能力支持时接入
其他格式按 Baga Ink Reader 能力演进
```

如果 LifeBook 需要 `baga.reader` 尚未提供的跨设备阅读能力，正确流程是：

```text
LifeBook 真实需求
      │
      ▼
评估是否为跨 App / 跨设备公共能力
      │
      ▼
更新 Baga Ink Standard / API（若应标准化）
      │
      ▼
Platform implementation
      │
      ▼
LifeBook 使用新的 baga.reader 能力
```

禁止流程：

```text
LifeBook
   ↓
直接调用 KOReader private internals
   ↓
形成事实上的 LifeBook 私有平台 API
```

---

# 9. Offline-first 与同步

墨水屏设备经常处于休眠、Wi-Fi 关闭、弱网或长期离线状态，因此 LifeBook MUST 以 offline-first 为核心设计原则。

## 9.1 启动

已经完成初次账户配置的用户，在无网络状态下 SHOULD 仍然能够：

- 打开 LifeBook；
- 访问本地书库；
- 继续阅读；
- 查看已缓存内容；
- 创建本地笔记；
- 创建本地人生记录；
- 修改允许离线修改的数据。

## 9.2 本地优先写入

用户已经确认的本地操作 SHOULD 先可靠写入 App 沙箱或标准数据接口，再进入待同步队列。

禁止把网络成功响应作为本地内容能够保存的必要条件。

## 9.3 Baga Sync 与 LifeBook Sync 的边界

`baga.sync` 提供的是平台级同步触发、网络/电源策略和任务调度能力，不强制所有 App 使用同一种数据模型。

LifeBook 自己负责：

- LifeBook 数据版本；
- 云端协议；
- 幂等请求；
- 冲突检测；
- 笔记等业务对象的合并语义；
- 重试后避免重复创建数据。

Platform 负责：

- online / offline 状态；
- sleep / wake；
- 标准网络请求；
- 同步任务触发；
- 电源与 Wi-Fi policy；
- 统一错误语义。

---

# 10. Capability 与渐进增强

LifeBook 的核心功能 MUST 面向 Baga Ink Base Profile 设计。

额外硬件能力通过 Capability 渐进增强。

例如：

```lua
if baga.device.has("input.touch") then
    enable_touch_controls()
end

if baga.device.has("input.physical_page_key") then
    enable_page_key_hints()
end

if baga.device.has("display.fast_refresh") then
    use_fast_interaction_mode()
end

if baga.device.has("display.color") then
    enable_optional_color_assets()
end
```

LifeBook MUST NOT 把以下等式写入产品逻辑：

```text
BOOX = 有手写
Kindle = 没有蓝牙
iReader = 某种刷新模式
Bigme = 彩色
```

Capability 必须来自当前设备和固件真实检测结果。

---

# 11. Permission 基线

LifeBook Manifest MUST 只声明实际需要的权限。

按功能可能使用：

```text
network
library.read
library.write
notes.read
notes.write
user_files.read
user_files.write
audio.output
bluetooth
frontlight.control
power.keep_awake
```

但某权限进入注册表不代表 LifeBook 必须全部申请。

原则：

- 阅读已有书籍：优先 `library.read`；
- 导入 / 删除 / 移动书籍：需要时使用 `library.write`；
- 标注 / 笔记：按标准使用 `notes.read` / `notes.write`；
- LifeBook 私有 appdata 不需要扩大为整个用户文件系统权限；
- AI / 社区 / 云同步使用 `network`；
- 没有明确功能需求时不得预申请 Bluetooth、前光控制、keep-awake 等高权限。

LifeBook MUST 正确处理 `permission_denied` 和 Capability 不存在两种不同情况。

---

# 12. IKP 包与代码组织原则

LifeBook 正式跨设备应用包 SHOULD 产出：

```text
lifebook.ikp
```

典型概念结构：

```text
lifebook.ikp
├── manifest.json
├── main.lua
├── src/
│   ├── application/
│   ├── domain/
│   ├── views/
│   ├── reader/
│   └── sync/
├── assets/
├── locales/
└── signature/
```

以上为 LifeBook 推荐组织方式，不改变 IKP Package Specification 的正式包规则。

Universal LifeBook IKP MUST NOT 携带：

- Android APK payload 作为应用执行依赖；
- DEX / JAR 逃生逻辑；
- Kindle shell bridge；
- BOOX / iReader SDK wrapper；
- 自带 Lua 解释器；
- 自带 Baga Ink Platform Core；
- 自带 Device Adapter；
- CPU ABI 相关主业务 native binary。

---

# 13. Kindle 与 Android E-Paper 的关系

LifeBook 的目标不是做两套业务 App，而是：

```text
                LifeBook source / lifebook.ikp
                            │
                 ┌──────────┴──────────┐
                 │                     │
                 ▼                     ▼
       Baga Ink Platform        Baga Ink Platform
          on Kindle              on Android E-Paper
                 │                     │
          Kindle Adapter          Android Adapter
                                       │
                              Vendor-specific adapters
```

## 13.1 Kindle

Kindle 的越狱、Homebrew、KUAL/MRPI、系统桥、文件路径、刷新机制等属于 Baga Ink Platform / Kindle Adapter / Installer 范围。

LifeBook App MUST 不直接承担这些职责。

## 13.2 Android E-Paper

Android E-Paper 的 Generic Android、掌阅 iReader、BOOX、墨案 Moaan、汉王 Hanvon、Bigme 等私有 SDK 与刷新接口属于 Baga Ink Android Device Adapter 范围。

Android 端可以使用 APK 作为 **Baga Ink Platform 的系统安装载体**；但 LifeBook 的标准业务 App 仍然保持 IKP / Baga Ink API 边界。

这样才能做到：

> 新增一种 Android 墨水屏设备时，优先增加/改进 Device Adapter，而不是复制一个新的 LifeBook 分支。

---

# 14. 参考应用驱动标准落地

LifeBook 是 Baga Ink 标准落地的重要验证器，但不能反过来绑架标准。

当开发 LifeBook 遇到缺失能力时，必须先判断：

## A. LifeBook 私有业务能力

例如：

```text
人生记录
时间胶囊
LifeBook 社区问答
LifeBook AI 产品逻辑
```

处理方式：

> 留在 LifeBook Domain，不进入 Baga Ink Standard。

## B. 跨 App、跨设备都合理的公共能力

例如某种通用 Reader、Input、Display、Storage 能力。

处理方式：

```text
提出标准需求
  ↓
Capability / Permission / API 设计
  ↓
更新对应 Baga Ink Standard
  ↓
Platform / Adapter 实现
  ↓
Compatibility 测试
  ↓
LifeBook 使用
```

## C. 某一个厂商独有能力

处理方式：

- 先判断能否抽象成标准 Capability；
- 能标准化则通过正式流程进入 Capability / API；
- 不能标准化则留在受控 Device Enhanced / Capability Provider 范围；
- Universal LifeBook 核心业务不得直接依赖厂商私有接口。

---

# 15. 第一阶段实现优先级

LifeBook 作为 Reference App 的第一阶段目标不是一次实现所有产品功能，而是尽快形成完整跨设备闭环。

建议顺序：

## Phase A — Universal Skeleton

必须先验证：

```text
同一个 lifebook.ikp
      │
      ├─ Kindle Baga Ink Platform
      └─ Android E-Paper Baga Ink Platform
```

至少完成：

- App lifecycle；
- 基础 E-Ink UI；
- Storage；
- Network；
- Capability 查询；
- Permission；
- sleep / wake；
- offline start。

## Phase B — Reading Core

加入：

- Library；
- Reader；
- 阅读位置；
- 标注 / Notes；
- 基础云同步。

## Phase C — LifeBook Content

加入：

- Articles；
- Q&A；
- Comments；
- 他人笔记 / 社区内容；
- 离线缓存。

## Phase D — Personal Life Features

加入：

- Life Records；
- Time Capsule；
- 更完整的跨设备数据同步。

## Phase E — AI

在不破坏阅读、离线能力和低功耗原则的前提下加入 AI。

---

# 16. Reference App 验收标准

LifeBook 的一个版本如果要作为 Baga Ink Reference App 基线，SHOULD 至少满足：

1. 同一 Application ID；
2. 同一 LifeBook 业务代码基线；
3. 同一 Universal `lifebook.ikp` 可在目标 Kindle 与 Android E-Paper Platform 上加载；
4. 核心业务不判断设备 Vendor；
5. 只通过 `baga.*` 获取平台能力；
6. 缺少 Optional Capability 时可以合理降级；
7. 无网络时核心阅读与本地内容仍可工作；
8. sleep / wake 后状态可恢复；
9. 同步失败不破坏本地用户数据；
10. App 更新失败不应删除既有用户数据；
11. 不直接访问 Vendor SDK / Shell / raw framebuffer / Android Context；
12. Reader 不依赖未标准化的 KOReader 私有 API；
13. 权限符合最小权限原则；
14. 在对应 Baga Ink Compatible 设备上通过 Reference App 场景测试。

最重要的验收问题是：

> **把 LifeBook 的 IKP 拿到另一台已经 Baga Ink Compatible 的设备上，是否无需为该品牌修改 LifeBook 核心业务代码就能运行？**

如果答案是否定的，应优先检查 Baga Ink Platform / API / Capability / Adapter 边界，而不是在 LifeBook 中增加 Vendor 分支。

---

# 17. 明确禁止的架构退化

LifeBook 实现 MUST NOT 演变为以下任何模式：

```text
LifeBook → BOOX SDK
LifeBook → iReader private API
LifeBook → Kindle shell
LifeBook → Android Context
LifeBook → raw framebuffer
LifeBook → KOReader private objects as permanent API
LifeBook → per-vendor business branches
LifeBook → bundled private Platform Core
LifeBook → bundled private Device Adapter
```

也不得出现：

```text
LifeBook for BOOX.ikp
LifeBook for iReader.ikp
LifeBook for Kindle.ikp
```

作为 Universal App 的正常长期分发模型。

设备特有差异应该被 Baga Ink Platform 吸收，而不是重新扩散到 App 层。

---

# 18. 最终架构定义

本实现规范最终将此前 LifeBook E-Ink 讨论收敛为以下结构：

```text
Baga Ink Std
│
├── App Standard
├── API
├── Capability
├── Permission
├── IKP
├── Device Adapter Standard
└── Compatibility Standard
        │
        ▼
LifeBook — Baga Ink Flagship Reference App
`lifebook.ikp`
│
├── LifeBook Application Core
│   ├── Account / Session
│   ├── Library
│   ├── Articles
│   ├── Q&A / Comments
│   ├── Notes
│   ├── Life Records
│   ├── Time Capsule
│   ├── AI
│   └── Sync Domain Logic
│
├── LifeBook E-Ink UI
│   └── only through baga.ui / input / display
│
├── LifeBook Reader Integration
│   └── only through baga.reader
│
└── Baga Ink API Integration
        │
        ▼
Baga Ink Platform Core
        │
        ▼
Baga Ink Device Adapter
├── Kindle Adapter
└── Android E-Paper Adapter
    ├── Generic Android
    ├── iReader
    ├── BOOX
    ├── Moaan
    ├── Hanvon
    ├── Bigme
    └── future devices
```

一句话总结：

> **Baga Ink Std 定义跨设备规则；Baga Ink Platform 实现这些规则并吸收设备差异；LifeBook 作为第一个完整旗舰 Reference App，只面向 Baga Ink API 开发，用真实产品持续证明和推动整个标准闭环成立。**

---

# 19. 本文件的边界

本文件只规定 LifeBook 如何实现 Baga Ink 标准。

它：

- MUST NOT 修改 `docs/standards/` 的规范语义；
- MUST NOT 创造未经标准注册的 `baga.*` 公共 API；
- MUST NOT 把 LifeBook 私有需求升级为事实标准；
- MAY 随 LifeBook 产品实现演进，但任何变化都必须继续服从上位 Baga Ink Standards。

当本文件与 `docs/standards/` 中正式规范产生冲突时：

> **以 `docs/standards/` 为准。**
