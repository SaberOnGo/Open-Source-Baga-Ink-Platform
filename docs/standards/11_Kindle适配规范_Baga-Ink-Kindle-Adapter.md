# Baga Ink Kindle 适配规范 / Baga Ink Kindle Adapter

> **文档级别：首发设备适配规范**  
> **状态：Draft v0.1**  
> **日期：2026-08-22**  
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
   ├── Kindle display / framebuffer bridge
   ├── Kindle input bridge
   ├── Kindle lifecycle / power bridge
   ├── Kindle storage bridge
   ├── Kindle network bridge
   └── Homebrew integration
   │
   ▼
Kindle OS + supported Homebrew foundation
```

Kindle App 不应该知道当前底层使用的是 KUAL、PEKI、MRPI、某种 Launcher 或某种具体 jailbreak。

---

# 2. 设计原则

Kindle Adapter MUST：

1. 最大化复用成熟 Kindle Homebrew / KOReader 能力；
2. 不重新实现已经稳定存在的显示、输入、阅读基础设施；
3. 隔离型号 / 固件差异；
4. 不让 IKP App 直接调用 Kindle Shell；
5. 不要求 LifeBook 自己维护一套 Kindle 私有 API；
6. 能由 Baga Ink Client 检测兼容状态；
7. 安装失败不得破坏用户书籍与笔记。

---

# 3. Kindle 支持对象

认证对象不是“所有 Kindle”一句话，而是：

```text
model family
+ firmware version/range
+ homebrew foundation
+ Kindle Adapter version
+ Baga Ink Platform version
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

这类信息进入独立可更新的 Compatibility / Installation Database。

这样 Amazon 固件变化不会迫使 Baga Ink API 或 Adapter Contract 改版本。

---

# 5. 现有生态复用原则

Kindle 当前成熟 Homebrew 生态提供了大量可复用经验和基础设施，例如：

```text
KUAL / PEKI 类启动入口
MRPI 类包安装基础
KOReader Kindle platform/device layer
FBInk / framebuffer 相关显示能力
Kindle input/event 处理
LIPC 等系统服务桥接（在可用设备上）
```

这些可以作为 Adapter 内部实现基础。

但：

> **Baga Ink App Standard 不依赖任何一个具体 Homebrew 项目。**

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
```

实现 MAY 复用 KOReader / FBInk 等成熟 Kindle 显示抽象。

Adapter MUST：

- 正确识别逻辑屏幕尺寸；
- 正确处理 orientation；
- 把 `AUTO/TEXT/FAST/QUALITY` 映射到适当 Kindle 刷新方式；
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

# 12. Storage Adapter

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

用户已有 Kindle 书籍目录只通过：

```text
storage.user_library
library.read / write permission
```

标准化暴露。

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

# 14. User Library Bridge

Kindle Adapter MAY 索引 Kindle 已有书籍，但上层只看到统一书库对象。

```text
Kindle books/files
      │
      ▼
Kindle Adapter
      │
      ▼
Baga Library API
      │
      ▼
LifeBook / other IKP
```

不能要求 IKP 自己扫描 Kindle 真实文件系统。

---

# 15. Reader Integration

Baga Ink Kindle 版本 SHOULD 尽量复用 KOReader ReaderUI / document engine 等成熟阅读能力。

但公开关系必须保持：

```text
IKP App
  ↓
baga.reader
  ↓
Platform Reader abstraction
  ↓
KOReader-derived implementation
```

第三方 App 不依赖 KOReader internal object。

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

---

# 17. Lifecycle / Power

必须稳定映射：

```text
start
resume
pause
sleep
wake
stop
```

Adapter SHOULD 利用 Kindle 可用系统事件，而不是 App 轮询判断。

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

# 18. Battery / Charging

如果 Kindle 系统可以稳定提供电量与充电状态，声明：

```text
power.battery_level
power.charging_state
```

无法可靠取得时返回 unknown，不伪造。

---

# 19. Frontlight

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

# 20. Audio / Bluetooth

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

# 21. Diagnostics

Kindle Adapter SHOULD 提供 Platform 内部诊断：

```text
model
firmware
adapter version
screen backend
input backend
network backend
capabilities
homebrew foundation status
```

这些信息可被 Baga Ink Client 用于支持和故障排查。

App 不应把它们作为跨设备业务逻辑。

---

# 22. Baga Ink Client 的 Kindle 识别流程

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

# 23. Home Screen 启动目标

长期用户体验目标：

```text
Kindle Home
  ↓
LifeBook / Baga Ink entry
```

用户不需要理解 KUAL / MRPI / Shell。

但第一阶段 MAY 使用 Homebrew launcher 作为内部启动桥。

启动方式的演进不得改变 IKP App contract。

---

# 24. Adapter 分层

Kindle 系列差异较多，推荐：

```text
Kindle Adapter Common
      │
      ├── Legacy Kindle backend
      ├── PW2-era backend
      ├── hard-float/new firmware backend
      └── model-specific quirks
```

公共逻辑尽量上提；quirk 只处理无法避免的硬件差异。

禁止把每一款 Kindle 做成完全独立平台代码库。

---

# 25. Quirk Database

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
```

Quirk 不属于公共 Capability 名称。

---

# 26. Kindle Compatible Gate

某 Kindle 组合正式标记 Compatible 前 MUST：

- 通过 Base BICTS；
- Kindle Adapter capability 声明真实；
- 标准 IKP 能安装/更新/回滚；
- sleep/wake 稳定；
- 不清用户书籍/笔记；
- 显示与输入基本可靠；
- 已知固件范围记录明确。

---

# 27. 与 LifeBook 的关系

LifeBook for Kindle 是第一 Reference App。

但 Kindle Adapter：

- MUST 不写 LifeBook 私有接口；
- MUST 服务所有 IKP App；
- LifeBook 遇到通用需求时 SHOULD 推动标准 API，而不是开后门。

---

# 28. 非目标

Kindle Adapter 不负责：

- 定义某个永久越狱方法；
- 替换 Kindle OS；
- 修改 Amazon 云服务；
- 让 IKP 直接执行 Shell；
- 给每个 App 打 Kindle native binary；
- 为单一 LifeBook 功能制造平台私有接口。

---

# 29. 核心原则 / Core Rule

> **Kindle 的复杂性应该停在 Kindle Adapter 和 Baga Ink Client；复杂性不能向上泄漏给 IKP 开发者。**

只要做到这一点，Kindle 才能真正成为 Baga Ink Platform 中的一类设备，而不是一个需要单独开发的孤岛。
