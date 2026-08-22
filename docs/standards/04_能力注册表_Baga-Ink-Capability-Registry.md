# Baga Ink 能力注册表 / Baga Ink Capability Registry

> **文档级别：一级平台规范**  
> **状态：Draft v0.2**  
> **日期：2026-08-23**  
> **上位文档：`01_顶层战略与架构_Baga-Ink-Platform-Strategy.md`**  
> **配套规范：`03_API规范_Baga-Ink-API-Specification.md`、`07_设备适配器规范_Baga-Ink-Device-Adapter-Specification.md`、`08_兼容性标准_Baga-Ink-Compatibility-Standard.md`**

---

## 0. 目的 / Purpose

Capability Registry 是 Baga Ink 防止设备碎片化的核心注册表。

它回答：

> **设备或 Platform 具有什么能力，应用应该用什么统一名称查询，以及这个名称的语义到底是什么。**

Baga Ink Universal App MUST 查询 Capability，而不是把厂商、型号、固件或内部开源组件名称写进业务逻辑。

例如：

```lua
if baga.device.has("input.pen") then
    enable_pen()
end
```

而不是：

```lua
if vendor == "BOOX" then ... end
if reader_impl == "KOReader" then ... end
```

---

# 1. 命名规则 / Naming

Capability 使用小写点分层级：

```text
category.feature
category.feature.variant
```

例如：

```text
display.partial_refresh
input.pen.pressure
light.frontlight.temperature
reader.anchor
```

规则：

- MUST 使用小写 ASCII；
- MUST 使用 `.` 分层；
- MUST 不包含厂商品牌名作为标准 Capability；
- MUST 不包含内部实现库名作为标准 Capability；
- MUST 描述能力语义，而不是底层 API / Library 名；
- 已发布稳定 Capability SHOULD 不重命名；
- 被替代的 Capability SHOULD 先 deprecated，再删除；
- Vendor 私有实验能力 MUST 不进入 Universal Registry，除非经过标准化。

因此：

```text
reader.anchor          ✓
reader.koreader        ✕
data.sqlite             ✕
sync.automerge         ✕
```

KOReader、SQLite、Automerge 等可以用于实现这些能力，但不是 Capability 名称本身。

---

# 2. Capability 与 Permission 的区别

Capability：设备 / Platform **能不能做**。

Permission：App **允不允许做**。

例如：

```text
Capability: network.wifi
Permission: network
```

设备有 Wi-Fi，不代表某个 App 自动拥有联网权限。

Capability Registry 不定义用户授权规则；授权规则见 `05_权限模型_Baga-Ink-Permission-Model.md`。

---

# 3. Base Profile 必需能力

所有声称 **Baga Ink Compatible** 的设备 MUST 提供或正确降级以下基础语义：

```text
display.basic
input.navigation
storage.app_sandbox
power.sleep_wake
platform.lifecycle
```

这些能力可以由不同硬件方式实现。

例如 `input.navigation` 可以来自：

- Touch；
- 物理翻页键；
- 键盘；
- 设备上的其他标准导航输入。

Base Profile 的目标不是要求相同硬件，而是保证最基本的 IKP App 可操作、可显示、可保存状态、可休眠恢复。

`baga.data` 这类 Platform Core 标准服务不因为底层使用 SQLite 等实现就成为硬件 Capability；其可用性主要由 Baga API 版本约束。

---

# 4. Display / 显示能力

## 4.1 `display.basic`

设备可以完成基础黑白/灰阶 UI 显示。

Compatible 设备 MUST 支持。

## 4.2 `display.partial_refresh`

设备支持对屏幕局部区域发起有效刷新。

语义：

```text
Platform 可以请求 region refresh，Adapter 不必退化为每次全屏刷新。
```

如果设备只能全刷，不得声明该能力。

## 4.3 `display.fast_refresh`

设备存在明显偏向速度、允许牺牲一定画质或残影表现的刷新方式。

这不是某厂商 waveform ID。

App 只能表达：

```text
希望快速交互
```

具体底层模式由 Adapter 决定。

## 4.4 `display.quality_refresh`

设备可显式请求偏向画质 / 清残影的刷新策略。

## 4.5 `display.animation`

设备和 Adapter 可以支持短时连续交互或动画型刷新。

这不表示墨水屏应该鼓励动画，只表示 Platform 可以提供此能力。

## 4.6 `display.grayscale`

设备支持多级灰阶。

更细能力 MAY 包括：

```text
display.grayscale.4
display.grayscale.16
```

但只有在确实需要区分且跨设备语义可稳定时才注册。

## 4.7 `display.color`

设备支持彩色电子纸显示。

应用 MUST 仍保证基本内容在非彩色设备上可合理降级，除非将 `display.color` 声明为 required capability。

## 4.8 `display.rotation`

设备支持 Platform 控制或稳定响应屏幕方向切换。

---

# 5. Input / 输入能力

## 5.1 `input.navigation`

提供基本 confirm / back / page_next / page_previous 等语义导航。

Compatible Base Profile MUST 满足。

## 5.2 `input.touch`

设备拥有可由 Baga Ink Platform 使用的触摸输入。

最低语义：

```text
pointer_down
pointer_move
pointer_up
cancel
```

## 5.3 `input.multitouch`

设备支持稳定多点触摸。

不得因为 Android 系统 API 存在就自动声明；必须在实际硬件上通过测试。

## 5.4 `input.pen`

设备支持可与普通触摸区分的手写笔输入。

可选子能力：

```text
input.pen.pressure
input.pen.eraser
input.pen.hover
input.pen.low_latency
```

### `input.pen.low_latency`

表示 Platform 可通过标准桥接获得明显低延迟笔迹路径。

这是增强能力，不属于 Base Profile。

## 5.5 `input.physical_page_key`

设备存在独立物理翻页键，并能稳定映射到：

```text
page_next
page_previous
```

## 5.6 `input.keyboard`

设备可向 Platform 提供键盘输入。

## 5.7 `input.volume_key`

设备有音量键且 Platform 能在不破坏系统行为的前提下获得输入事件。

Universal App SHOULD 优先监听 `page_next/page_previous` 等语义动作，而不是直接查询此能力。

---

# 6. Network / 网络能力

## 6.1 `network.available`

设备存在可供 Platform 使用的网络连接机制。

## 6.2 `network.wifi`

设备具有可用 Wi-Fi。

## 6.3 `network.http`

Platform 可以提供统一 HTTP 请求能力。

## 6.4 `network.https`

Platform 可以完成符合当前安全基线的 HTTPS 通信。

正式 Baga Ink Compatible 互联网设备 SHOULD 支持。

## 6.5 `network.connectivity_events`

Adapter 可以稳定报告联网、断网、重连等状态变化。

---

# 7. Storage / 存储能力

## 7.1 `storage.app_sandbox`

Platform 可以为每个 App 提供独立逻辑沙箱。

Compatible Base Profile MUST 支持。

## 7.2 `storage.user_library`

Platform 可以以标准方式桥接设备上的用户书库索引或经授权访问书籍 / 文档，并通过 `baga.library` 暴露。

该 Capability 不代表某一种具体书库数据库、文件路径或文档格式。

## 7.3 `storage.user_files`

设备允许 Platform 提供用户选择文件 / 授权文件访问能力。

## 7.4 `storage.external`

存在可访问的扩展存储，例如 SD 卡。

不得把具体挂载路径暴露为标准语义。

---

# 8. Power / 电源能力

## 8.1 `power.sleep_wake`

Platform 能稳定收到 sleep / wake 语义。

Compatible Base Profile MUST 支持。

## 8.2 `power.battery_level`

Platform 可以读取可信电量百分比。

## 8.3 `power.charging_state`

Platform 可以读取并监听充电状态。

## 8.4 `power.keep_awake`

Platform 可以请求短时间阻止休眠。

这只表示设备支持该机制，不表示任何 App 都有无限制使用权。

---

# 9. Light / 前光能力

## 9.1 `light.frontlight`

设备有可由 Platform 查询或控制的前光。

## 9.2 `light.frontlight.temperature`

设备支持暖光 / 色温调节。

具体 0–100 或厂商物理级别由 Platform 归一化。

---

# 10. Audio / 音频能力

## 10.1 `audio.output`

Platform 可以提供音频输出。

底层可能是：

- 内置扬声器；
- 有线；
- USB；
- Bluetooth；
- 厂商系统音频。

## 10.2 `audio.tts`

Platform 存在可调用的文本转语音能力。

如果 TTS 依赖网络或额外服务，Permission / availability 需要另行判断。

## 10.3 `audio.microphone`

设备有可由 Platform 使用的麦克风输入。

此能力不属于早期 Base Profile。

---

# 11. Bluetooth / 蓝牙能力

## 11.1 `bluetooth.available`

设备有 Platform 可使用的蓝牙能力。

## 11.2 `bluetooth.input_device`

Platform 可以通过蓝牙接收键盘、翻页器等标准输入设备。

## 11.3 `bluetooth.audio`

Platform 可以使用蓝牙音频输出。

Bluetooth 权限与扫描规则由 Permission Model 约束。

---

# 12. Reader / 阅读基础能力

Reader 能力属于 Platform 提供的高级标准能力，不一定由 Device Adapter 直接提供。

可注册：

```text
reader.open
reader.search
reader.selection
reader.highlight
reader.note
reader.position
reader.anchor
```

这些 Capability 用于细粒度 API feature detection。

应用不应查询 KOReader、MuPDF、CREngine 等实现名称。

## 12.1 `reader.anchor`

表示当前 Reader implementation 可以通过 `baga.reader`：

```text
create_anchor
serialize/pass anchor as Baga data
goto_anchor / resolve_anchor
```

将正文位置或范围表达为对 App opaque 的标准 Anchor 对象。

关键语义：

- Anchor 不限定 EPUB；
- Anchor 不限定 PDF；
- Anchor 不要求所有格式共享同一种底层 locator；
- Reader 可以为不同文档类别使用不同成熟原生定位机制；
- App 不能解析或依赖 KOReader XPointer、PDF pboxes、EPUB CFI 等私有/外部字段；
- 跨实现恢复可以使用标准化 fallback evidence，但不能把近似定位伪报为精确定位。

实现可以直接复用 KOReader 已有 annotation / position 能力，或其他 Reader 已有成熟 locator；Capability 名称仍然只叫 `reader.anchor`。

---

# 13. Lifecycle / 平台能力

## `platform.lifecycle`

Platform 可以稳定向 App 提供：

```text
start
resume
pause
sleep
wake
stop
```

Compatible Base Profile MUST 满足。

---

# 14. Capability 状态

Registry 中每个能力 SHOULD 拥有状态：

```text
experimental
provisional
stable
deprecated
removed
```

### experimental

尚未承诺兼容性，不允许作为 Universal certification 的强依赖。

### provisional

语义基本稳定，允许试用，但可能在 1.0 前调整。

### stable

正式兼容契约。

### deprecated

仍支持，但不建议新应用使用。

### removed

只允许在明确的主版本升级中移除。

`reader.anchor` 在 v0.2 Registry 中属于 provisional，待跨 Kindle/Android、多格式 BICTS 验证后再升级 stable。

---

# 15. Capability 注册流程

新增标准 Capability MUST 按以下流程：

```text
需求出现
  ↓
确认无法由现有 Capability 表达
  ↓
定义跨设备语义，而不是 Vendor API / Library API
  ↓
优先研究是否有成熟实现可复用
  ↓
至少验证两种不同实现路径，或证明具有通用抽象价值
  ↓
加入 Registry 为 experimental/provisional
  ↓
补充 API / Adapter / Test Case
  ↓
稳定后升级为 stable
```

禁止：

```text
某厂商新增接口
  ↓
直接把厂商接口名塞进 baga.*
```

也禁止：

```text
采用某开源库
  ↓
把库名直接注册成 Capability
```

---

# 16. Vendor Extension

某些能力在标准化前 MAY 使用私有实验命名：

```text
x.vendor.feature
```

但：

- MUST 不用于 Baga Ink Universal 认证；
- MUST 不进入公共稳定 API；
- SHOULD 由 Platform / Adapter 内部使用；
- 一旦形成跨设备需求，应迁移为正式 Capability。

---

# 17. v0.2 Registry 摘要

```text
Base
├─ display.basic
├─ input.navigation
├─ storage.app_sandbox
├─ power.sleep_wake
└─ platform.lifecycle

Display
├─ display.partial_refresh
├─ display.fast_refresh
├─ display.quality_refresh
├─ display.animation
├─ display.grayscale
├─ display.color
└─ display.rotation

Input
├─ input.touch
├─ input.multitouch
├─ input.pen
├─ input.pen.pressure
├─ input.pen.eraser
├─ input.pen.hover
├─ input.pen.low_latency
├─ input.physical_page_key
└─ input.keyboard

Network
├─ network.available
├─ network.wifi
├─ network.http
├─ network.https
└─ network.connectivity_events

Storage
├─ storage.user_library
├─ storage.user_files
└─ storage.external

Power
├─ power.battery_level
├─ power.charging_state
└─ power.keep_awake

Light
├─ light.frontlight
└─ light.frontlight.temperature

Audio
├─ audio.output
├─ audio.tts
└─ audio.microphone

Bluetooth
├─ bluetooth.available
├─ bluetooth.input_device
└─ bluetooth.audio

Reader
├─ reader.open
├─ reader.search
├─ reader.selection
├─ reader.highlight
├─ reader.note
├─ reader.position
└─ reader.anchor        provisional
```

---

# 18. 核心原则 / Core Rule

> **Capability Registry 不是硬件功能清单，也不是开源库清单，而是跨设备语义契约。**

只要这个注册表保持稳定，Baga Ink 就可以不断接入新设备、替换或复用不同成熟实现，而不要求第三方 App 认识新的品牌、型号或内部库。