# LifeBook for Kindle 产品行为与外设扩展设计 / LifeBook for Kindle Product Behavior and Accessory Extension Design

> **文档级别：LifeBook Reference App 补充设计 / Reference App Design Note**  
> **状态：Design Baseline v0.1**  
> **日期：2026-08-23**  
> **适用对象：LifeBook for Kindle on Baga Ink Platform**  
> **建议路径：`docs/reference-apps/02_LifeBook-Kindle产品行为与外设扩展设计_LifeBook-Kindle-Product-Behavior-and-Accessory-Extension-Design.md`**  
> **本文件不是 Baga Ink Standard，不得覆盖、修改或绕过 `docs/standards/` 中的正式规范。**

---

## 0. 文档目的

本文档整理 LifeBook for Kindle 讨论中已经形成价值的产品与实现设计，重点包括：

- LifeBook 与 Baga Ink Client / Market 的关系；
- Kindle 上的低刷新、低功耗 UI 行为；
- Wi-Fi 与网络使用策略；
- Audio / Bluetooth 能力的渐进增强；
- 面向旧 Kindle 的智能外设与磁吸底座方向；
- 外设通信候选方案及验证边界；
- 后续原型与标准化路径。

本文档只描述 **LifeBook 产品行为、参考实现建议和实验性产品方向**。

任何具有跨 App、跨设备价值的新公共能力，必须先按照 Baga Ink Standards 的治理流程进入 Capability / Permission / API / Device Adapter / Compatibility 体系，LifeBook 不得私自创造长期平台接口。

---

# 1. 上位规范与约束

本文档服从以下现有规范与 Reference App 基线：

```text
docs/standards/
├── 00_规范总览_Baga-Ink-Standards-Index.md
├── 01_顶层战略与架构_Baga-Ink-Platform-Strategy.md
├── 02_应用标准_Baga-Ink-App-Standard.md
├── 03_API规范_Baga-Ink-API-Specification.md
├── 04_能力注册表_Baga-Ink-Capability-Registry.md
├── 05_权限模型_Baga-Ink-Permission-Model.md
├── 06_IKP应用包规范_IKP-Package-Specification.md
├── 07_设备适配器规范_Baga-Ink-Device-Adapter-Specification.md
├── 08_兼容性标准_Baga-Ink-Compatibility-Standard.md
├── 09_UI规范_Baga-Ink-UI-Specification.md
├── 10_兼容性测试套件_Baga-Ink-Compatibility-Test-Suite.md
├── 11_Kindle适配规范_Baga-Ink-Kindle-Adapter.md
├── 20_市场与分发总体架构_Baga-Ink-Market-and-Distribution-Architecture.md
└── 26_分发客户端与离线传输协议_Baga-Ink-Distribution-Client-and-Offline-Transfer-Protocol.md

docs/reference-apps/
└── 01_LifeBook参考实现_LifeBook-Reference-App.md
```

优先级保持：

```text
Baga Ink Standards
        >
01_LifeBook Reference App
        >
本补充设计
        >
具体产品原型与实现
```

本文件不得定义新的 `baga.*` 公共 API、Capability、Permission、IKP 格式或 Device Adapter Contract。

---

# 2. 核心架构结论

## 2.1 LifeBook 不是 Runtime

LifeBook 是 Baga Ink Platform 上的旗舰 Reference App，而不是独立 Runtime、SDK 或设备兼容层。

正确关系：

```text
LifeBook (`lifebook.ikp`)
        │
        ▼
     baga.*
        │
        ▼
Baga Ink Platform Core
        │
        ▼
Baga Ink Device Adapter
        │
        ▼
      Kindle
```

不得重新引入：

```text
LifeBook Runtime
LifeBook Kindle 私有长期 API
LifeBook 自带 Device Adapter
LifeBook 自带大型中间执行环境
```

如果 Kindle 端复用 KOReader、Lua/LuaJIT、FBInk、KUAL/MRPI 或其他 Homebrew 基础设施，这些属于 Platform / Kindle Adapter 的内部实现选择，不属于 LifeBook App Contract。

## 2.2 LifeBook 不拥有安装器和市场

早期产品讨论中的 “LifeBook Installer for Kindle” 所承载的通用能力，在 Baga Ink 正式架构中应归属：

```text
Baga Ink Client
├── 设备识别
├── 安装路线判断
├── Platform 安装
├── Compatibility 检查
├── IKP 传输
└── 管理与诊断

Baga Ink Market
├── App 发现
├── 安装入口
├── 更新入口
└── 第三方应用生态
```

LifeBook 可以作为：

- 首个旗舰 App；
- 首次安装完成后的推荐 App；
- Reference App；
- Baga Ink Market 中的第一方产品。

但 LifeBook 不应把 Baga Ink Client / Market 变成自己的私有子系统。

## 2.3 开放生态的正确理解

用户安装 Baga Ink Platform 后，可以进一步安装 LifeBook 和第三方 IKP App。

第三方开发者面向：

```text
Baga Ink App Standard
Baga Ink SDK / API
IKP
Capability / Permission
```

而不是面向 LifeBook 开发。

已有 Kindle Homebrew 项目可以被 Platform 内部复用，或未来通过受控桥接方式接入，但一个任意 Shell/KUAL/Native Homebrew 包不能仅因为“能在 Kindle 上运行”就自动成为标准 Baga Ink App。

---

# 3. Kindle UI：事件驱动，而不是持续刷新

## 3.1 产品原则

LifeBook for Kindle SHOULD 采用 **event-driven static UI**。

正确思路：

```text
用户操作 / 数据变化
        ↓
更新必要 UI 状态
        ↓
提交最小 Dirty Region
        ↓
表达 Refresh Intent
        ↓
Platform / Adapter 决定实际刷新方式
        ↓
画面重新静止
```

避免：

```text
持续 UI Loop
高频 Timer 重绘
手机式 Loading Spinner
渐变 / 位移动画
持续 Skeleton Animation
无意义全屏刷新
```

LifeBook 不直接选择 Kindle waveform，也不自己实现 “每 N 次 full refresh”。

残影、局刷、质量刷新和 waveform 映射继续由 Baga Ink Platform / Kindle Adapter 负责。

## 3.2 AI 流式输出

AI 是 LifeBook 中最容易产生高频刷新的一类场景。

LifeBook SHOULD 对 token 流做显示合并，而不是每个 token 触发一次 E-Ink 刷新。

建议产品策略：

```text
LLM token stream
      ↓
Memory buffer
      ↓
满足任一条件后提交 UI：
- 累计约 20–50 个中文字符；或
- 距离上次可见更新约 500–1000 ms
      ↓
局部更新回答区域
```

上述数值是 LifeBook 的初始产品调优范围，不是 Baga Ink Standard。

设备较慢时可以进一步降低频率；具有 `display.fast_refresh` / `display.animation` 能力的设备可以渐进增强。

AI 回复完成后，LifeBook 只表达内容稳定或质量需求，由 Platform 决定是否需要质量刷新。

## 3.3 长列表与文章

LifeBook 的文章、问答、评论、书库和搜索结果 SHOULD：

- 优先分页或 step scroll；
- 避免手机式惯性连续滚动作为唯一模式；
- 长列表使用虚拟化；
- focus 改变只更新对应区域；
- 翻页使用 `page_next` / `page_previous` 语义动作；
- 不把 Touch 作为唯一交互入口。

---

# 4. Wi-Fi 与网络：短连接窗口 + Offline-first

## 4.1 为什么不能照搬手机在线模型

Kindle 的长期续航依赖：

```text
E-Ink 静态显示
+
CPU / 系统进入休眠
+
无线模块低活动或断开
```

因此 LifeBook SHOULD NOT 默认长期维持：

```text
WebSocket 永久在线
频繁心跳
高频后台轮询
只为即时通知持续保持 Wi-Fi
持续 keep-awake
```

## 4.2 推荐网络模型

```text
用户打开 / 唤醒 LifeBook
        ↓
Platform 报告可联网
        ↓
批量完成必要同步
├── 阅读进度
├── 笔记
├── 文章 / 评论缓存
├── 用户操作队列
└── 必要元数据
        ↓
用户继续本地阅读 / 编辑
        ↓
网络空闲
        ↓
允许 Platform 正常进入低功耗策略
```

LifeBook 不直接控制 Kindle Wi-Fi 驱动，而是通过标准 Network / Lifecycle / Sync 能力工作。

## 4.3 允许持续联网的场景

以下场景可以在用户主动使用期间保持网络会话：

- AI 对话；
- 用户主动刷新社区内容；
- 大文件下载；
- 明确的同步操作；
- 登录 / 授权流程。

会话结束后，应尽快释放不再需要的连接和 keep-awake 请求。

## 4.4 离线优先

即使 Wi-Fi 不可用，LifeBook 核心功能仍 SHOULD 可用：

```text
本地书库
继续阅读
阅读位置
已缓存文章
本地笔记
人生记录
时间胶囊草稿
待同步操作
```

用户操作优先可靠写本地，再进入同步队列。

---

# 5. Audio / Bluetooth：只能渐进增强

Kindle 各代硬件差异很大。

LifeBook MUST 不假设：

```text
所有 Kindle 都有 Bluetooth
所有 Kindle 都能连接 Bluetooth 输入设备
所有 Kindle 都有音频输出
所有 Kindle 都有麦克风
```

LifeBook 只能查询标准 Capability，例如：

```text
audio.output
audio.tts
audio.microphone
bluetooth.available
bluetooth.audio
bluetooth.input_device
```

## 5.1 可用时的产品增强

如果存在 `audio.output`：

- 书籍 / 文章 TTS；
- AI 回答朗读；
- 有声内容；
- 单词发音。

如果存在 `audio.microphone`：

- 语音搜索；
- AI 语音输入；
- 语音笔记。

如果能力不存在，相关入口应隐藏或明确降级，不应模拟一个实际不存在的硬件能力。

---

# 6. 智能外设与磁吸底座：产品方向

## 6.1 目标

一个值得探索的方向是：

> **通过外部 Dock / Accessory 给旧 Kindle 增加现代交互能力，使廉价存量 Kindle 成为可扩展的低功耗 E-Ink 终端。**

概念结构：

```text
               Kindle
        ┌─────────────────┐
        │  Baga Ink       │
        │  + LifeBook     │
        └────────┬────────┘
                 │
          Data / Power
                 │
        ┌────────▼────────┐
        │  Accessory Dock │
        │                 │
        │ Buttons         │
        │ Speaker         │
        │ Microphone      │
        │ Battery         │
        │ Wi-Fi (optional)│
        │ BLE (optional)  │
        │ Sensors(optional)│
        └─────────────────┘
```

磁吸只解决 **机械固定和对位**；数据通信和供电必须独立设计。

## 6.2 外设不是 LifeBook 核心依赖

LifeBook Base Experience MUST 不依赖 Dock。

Dock 只能提供 Optional Enhancement：

```text
无 Dock
→ LifeBook 仍可正常阅读和使用基础功能

有 Dock
→ 获得额外输入 / 音频 / 网络 / 电源等增强
```

---

# 7. 外设通信候选方案

当前阶段不得把任何一种方案写成正式 Baga Ink Accessory Standard。

## 7.1 Bluetooth / BLE

优点：

- 无线；
- 低功耗；
- 适合按键、遥控器和小数据；
- 硬件成本低。

限制：

> **大量旧 Kindle 不具备可供 Platform 使用的 Bluetooth，因此 BLE 不能成为跨代 Kindle 的唯一基础通信方案。**

正确使用方式：

```text
if baga.device.has("bluetooth.input_device") then
    enable_supported_remote_input()
end
```

LifeBook 不直接与某个私有 BLE GATT UUID 建立长期跨设备 Contract。

如果未来需要标准化 Baga Ink 外设协议，应先进入 `90–99 Experimental` 或 `50–59 Optional Extensions` 的标准治理流程。

## 7.2 USB：最值得验证的跨代候选

USB 是旧 Kindle 与新 Kindle 都广泛存在的物理接口类别，但 **“存在 USB 接口”不等于“支持我们需要的 USB 通信角色与协议”**。

因此 USB 目前只能定义为 Research Candidate。

需要分别验证两类架构。

### A. Kindle 作为 USB Host

```text
Kindle USB Host
      │
      ▼
Accessory USB Device
```

可能适合 HID、Serial 或自定义设备。

风险：

- 不同 Kindle USB Controller / Kernel 差异；
- OTG / Host 支持不一致；
- 供电能力不确定；
- sleep/wake 后设备枚举行为不确定。

不得假设全系列成立。

### B. Dock 作为 USB Host，Kindle 作为 USB Device

```text
Accessory Dock / Host
          │
          ▼
       Kindle
     USB Device
```

这是更值得优先研究的方向之一，因为 Kindle 本身长期具有与电脑进行 USB 连接的产品路径。

需要验证越狱后 Platform 是否能在目标机型上安全、稳定地暴露或复用受控通信通道，例如：

```text
USB network-like channel
USB serial-like channel
受控 gadget interface
其他可验证 transport
```

这些只是候选技术，不是已验证事实。

如果可行，Dock 可以承担更多现代硬件职责：

```text
Internet
   │
 Wi-Fi
   │
 Dock
   │ USB data
   │
Kindle
```

从而让旧 Kindle 主要负责：

```text
E-Ink display
Touch / local input
Storage
Baga Ink Platform
LifeBook
```

而 Dock 可以负责：

```text
Wi-Fi / BLE
Microphone
Speaker
Physical buttons
Additional battery
Sensors
```

## 7.3 电容触摸模拟

作为最低级兼容路线，可以存在独立遥控器 + 屏幕边缘触控接收器：

```text
Remote
  ↓ RF
Touch Simulator
  ↓
Kindle Screen
```

优点：

- 不依赖 Kindle Bluetooth；
- 不依赖 Baga Ink Platform；
- 兼容面可能较大。

缺点：

- 本质只模拟屏幕点击；
- 几乎没有双向数据；
- 不适合 AI、麦克风、网络和复杂语义动作。

因此它只适合作为翻页类外围方案，不是 Baga Ink 智能外设架构的核心方向。

---

# 8. LifeBook 与外设的正确软件边界

即使未来 Dock 原型成功，LifeBook SHOULD 看到的也不是：

```text
USB packet
BLE manufacturer data
Kindle /dev/input/eventX
Dock GPIO
Vendor-specific command
```

而应该继续看到标准语义：

```text
page_next
page_previous
confirm
back
menu

或标准 Capability：

audio.output
audio.microphone
network.available
power.charging_state
input.keyboard
```

理想分层：

```text
LifeBook
   │
   │ baga.* / semantic actions
   ▼
Baga Ink Platform
   │
   ▼
Device Adapter / Future Accessory Provider
   │
   ├── USB
   ├── BLE
   ├── HID
   └── other transport
   │
   ▼
Accessory Hardware
```

如果现有 Capability 无法表达新外设能力：

```text
真实原型需求
   ↓
确认具有跨设备 / 跨 App 价值
   ↓
进入 Capability 注册流程
   ↓
Experimental / Provisional
   ↓
API / Adapter / Test
   ↓
LifeBook 再使用
```

不得由 LifeBook 私有实现直接绕过标准。

---

# 9. LifeBook Dock Mini 概念原型

第一代原型 SHOULD 保持克制，先验证最有价值的能力，而不是堆硬件。

候选：

```text
LifeBook Dock Mini

Mechanical
├── Magnetic / stand structure
└── Kindle alignment

Input
├── Previous
├── Next
├── Up
├── Down
├── Confirm
└── Optional AI shortcut

Audio
├── Small speaker (optional)
└── Microphone (experimental)

Connectivity
├── USB data candidate
├── BLE optional
└── Wi-Fi optional

Power
├── Dock battery (optional)
├── USB-C input
└── Kindle charging path (to be verified)
```

核心验证优先级：

```text
1. 可靠按键输入
2. sleep / wake 后自动恢复
3. USB 稳定通信
4. 音频输出
5. 充电 / 数据共存
6. 麦克风
7. Dock 独立联网
```

不应从第一版就同时实现所有能力。

---

# 10. 桌面 E-Ink 终端场景

Dock 的价值不应局限于“翻页器”。

LifeBook + Kindle + Dock 可以探索：

```text
Reading Dashboard
├── 当前阅读
├── 文章
├── Todo
├── 日历摘要
├── 天气缓存
└── AI / TTS
```

其优势在于：

- E-Ink 静态显示；
- 低干扰；
- 长续航；
- 旧设备再利用；
- 外设承担现代输入 / 音频 / 网络能力。

但 Dashboard 不得引入高频时钟秒针、持续动画或高频刷新，从而破坏 E-Ink 低功耗价值。

---

# 11. 开放硬件生态方向

长期如果 Baga Ink 用户规模成立，可以探索类似开放配件生态：

```text
Page Remote
Keyboard
Foot Pedal
Audio Dock
Microphone Dock
Desktop Stand
Charging Dock
Sensor Accessory
```

但当前不应直接发布未经验证的 “Baga Ink Accessory Protocol”。

推荐路径：

```text
LifeBook 原型验证
        ↓
至少两个不同实现证明抽象价值
        ↓
提交 Baga Ink Experimental Extension
        ↓
定义 Capability / Permission / Transport abstraction
        ↓
建立测试 Profile
        ↓
成熟后进入 50–59 Optional Extensions
```

这样可以避免：

```text
LifeBook 私有协议
        ↓
第三方依赖
        ↓
以后无法演进
```

---

# 12. Kindle 外设研究矩阵

在做正式 Dock 之前，必须建立真实机型矩阵，不能用某一代 Kindle 推断全部系列。

至少记录：

| 项目 | 需要验证 |
|---|---|
| Model / Firmware | 精确型号与固件范围 |
| CPU / Kernel | 影响驱动与用户态能力 |
| USB connector | Micro-USB / USB-C |
| USB Device | 可用模式与稳定性 |
| USB Host / OTG | 是否存在、供电、驱动 |
| USB gadget | 可用 function / kernel support |
| Data + Charging | 是否可同时稳定工作 |
| Bluetooth | available / input / audio |
| Audio | output path |
| Microphone | 是否存在可用输入 |
| Wi-Fi | sleep/wake 行为 |
| Power Events | Dock 接入/拔出后的行为 |
| Suspend/Resume | 通信是否自动恢复 |
| Homebrew Foundation | Platform 可安全利用的基础 |

至少应选择：

```text
一个典型旧 Kindle
一个典型 Paperwhite 中期型号
一个较新 USB-C Kindle
```

做首轮原型，不以单机成功宣称全系列支持。

---

# 13. 外设安全原则

未来智能 Dock 可能获得：

- 输入控制；
- 网络；
- 麦克风；
- 文件传输；
- 供电；
- 固件升级能力。

因此必须默认把它视为不可信外部设备，而不是天然可信附件。

未来平台级设计至少需要考虑：

```text
Accessory identity
Pairing / trust
Permission boundary
Firmware authenticity
USB attack surface
Malicious HID
Network bridge isolation
Microphone privacy
Update / revocation
```

LifeBook 不应因为识别到某个 Dock 就自动授予麦克风、网络、文件或系统权限。

这些安全机制如进入公共平台，必须另行标准化；本文件不定义具体协议。

---

# 14. 产品实现阶段

## Phase A — 纯软件低功耗体验

先完成：

```text
LifeBook Universal IKP
Kindle 事件驱动 UI
AI 流式显示合并
Offline-first
低频联网
sleep / wake 恢复
Capability-driven Audio / Bluetooth UI
```

这一阶段完全不依赖外设。

## Phase B — 外设可行性研究

建立 Kindle Hardware Matrix，重点验证：

```text
USB roles
USB transport
sleep / wake
charging + data
Bluetooth capability differences
```

## Phase C — Dock Prototype

只在少数代表机型上完成：

```text
Physical buttons
Bidirectional transport
Reconnect after wake
Optional audio
```

## Phase D — Enhanced Prototype

再测试：

```text
Microphone
Dock Wi-Fi
External battery / charging
Additional sensors
```

## Phase E — 平台化评审

只有当外设能力证明具有跨 App、跨设备价值时，才提交新的 Baga Ink Experimental / Optional Extension 标准提案。

---

# 15. 验收与失败标准

## 15.1 LifeBook 软件体验

SHOULD 验证：

- 静止页面无周期性无意义刷新；
- AI 流式输出不会每 token 刷屏；
- 长时间阅读不要求 Wi-Fi 常连；
- 断网后本地内容继续可用；
- sleep / wake 后恢复阅读和待同步状态；
- 无 Bluetooth 设备不会显示依赖 Bluetooth 的必需流程；
- 无 Audio 设备不会影响核心阅读功能。

## 15.2 Dock 原型

至少测试：

- 接入 / 拔出；
- Kindle sleep / wake；
- Dock 断电 / 重启；
- 数据传输中断；
- 低电量；
- 充电中通信；
- Platform 重启；
- App 重启；
- 不同固件；
- 恶意 / 异常输入；
- 失败后不损坏 Kindle 用户数据。

## 15.3 立即停止标准化的情况

如果某候选方案出现：

```text
只在极少单一型号工作
必须让 LifeBook 直接调用 Kindle 私有系统接口
需要关闭 Baga Ink Permission / Sandbox
经常造成 sleep / wake 后死锁
存在高概率设备不可恢复风险
```

则不得为了产品功能强行提升为公共 Baga Ink 能力。

---

# 16. 已确定结论与实验假设

## 16.1 已确定的设计结论

```text
LifeBook 不是 Runtime。
LifeBook 是 Baga Ink Reference App。
安装与市场能力属于 Baga Ink Client / Market。
Kindle UI 应事件驱动、低刷新。
LifeBook 应 Offline-first、低频联网。
AI token 流应合并后刷新。
不能假设所有 Kindle 有 Bluetooth / Audio。
外设能力必须通过 Capability / semantic actions 暴露给 App。
磁吸只负责机械固定，不等于数据连接。
LifeBook Base Experience 不依赖 Dock。
```

## 16.2 尚未验证、不得视为事实

```text
某一 Kindle 是否支持 USB Host / OTG。
某一 Kernel 是否支持目标 USB gadget function。
Dock Host ↔ Kindle Device 是否可作为稳定通用通道。
USB Data + Charging 是否能在各代设备同时工作。
外部 Dock 是否能稳定为 Kindle 提供网络桥。
哪些 Kindle 可以稳定使用 USB Audio / HID。
是否存在足够跨设备价值来建立 Baga Ink Accessory Standard。
```

这些必须通过真实硬件测试回答。

---

# 17. 非目标

本文档不定义：

- 新 Baga Ink Standard；
- 新 `baga.*` API；
- 新 Capability 名称；
- 新 Permission 名称；
- USB Accessory Protocol；
- BLE GATT Protocol；
- Dock 固件协议；
- Kindle 越狱方法；
- Kindle Kernel 修改方法；
- Market / Repository 新规则；
- Baga Ink Compatible Accessory 认证标志。

这些如有必要，应在原型验证后另行进入 `docs/standards/` 对应保留编号区间。

---

# 18. 核心产品原则

> **LifeBook for Kindle 的目标不是把 Kindle 变成一台低刷新率 Android 平板，而是尊重 Kindle 的 E-Ink、休眠和离线特性，在此基础上通过 Baga Ink 的统一能力模型渐进增强。**

对于外设方向：

> **先用真实 Kindle 验证通信和硬件价值，再把可复用能力抽象成 Baga Ink 平台扩展；不要先发明协议，再寻找使用场景。**
