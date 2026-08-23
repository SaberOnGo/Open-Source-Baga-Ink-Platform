# Baga Ink UI 规范 / Baga Ink UI Specification

> **文档级别：一级平台规范**  
> **状态：Draft v0.1**  
> **日期：2026-08-22**  
> **上位文档：`01_顶层战略与架构_Baga-Ink-Platform-Strategy.md`**  
> **配套规范：`02_应用标准_Baga-Ink-App-Standard.md`、`03_API规范_Baga-Ink-API-Specification.md`、`04_能力注册表_Baga-Ink-Capability-Registry.md`**

---

## 0. 目的 / Purpose

Baga Ink UI Specification 定义第三方 IKP App 在 Kindle 与 Android 墨水屏上的统一界面模型。

目标不是复制 Android View、Flutter 或 Web UI，而是建立一个：

- 对电子纸友好；
- 能跨触摸 / 非触摸设备；
- 能跨不同分辨率；
- 减少无意义刷新；
- 能映射物理翻页键；
- 不把厂商刷新接口暴露给 App；

的轻量 UI 标准。

核心原则：

> **App 描述界面和刷新意图，Platform 决定真正绘制和刷新。**

---

# 1. UI 设计原则

Baga Ink App SHOULD：

1. 高对比度优先；
2. 文本可读性优先；
3. 页面式导航优先于连续动画；
4. 局部更新优先于无意义全刷；
5. 不依赖颜色传递唯一信息；
6. 不把 Hover / 动画 / 手势作为唯一入口；
7. 支持语义导航；
8. 在低刷新率设备上保持可操作。

---

# 2. 基础组件

v0.1 核心组件：

```text
Page
Text
Image
Button
List
Menu
Dialog
Toolbar
Input
ReaderView
Spacer
Divider
```

这些是语义组件，不要求所有底层平台使用同一渲染库。

---

# 3. `Page`

Page 是 Baga Ink UI 的基本页面容器。

建议能力：

```lua
baga.ui.page({
    title = "Library",
    body = {...},
    toolbar = {...}
})
```

Page SHOULD 支持：

- title；
- content/body；
- footer / toolbar；
- focus root；
- lifecycle hooks；
- scroll / paged content policy。

在无触摸设备上，Page MUST 能进入焦点导航模式。

---

# 4. `Text`

Text MUST 支持：

```text
text
font_size
weight
align
wrap
max_lines
```

SHOULD 支持：

```text
selectable
line_spacing
paragraph_spacing
```

字体接口必须是逻辑字体接口，不让 App 依赖某设备系统字体路径。

---

# 5. `Image`

Image SHOULD 支持：

```text
source
fit
width
height
alt_text
```

Platform MAY 对图片进行：

- 灰阶转换；
- 抖动；
- 缩放；
- 彩色设备优化。

App 不应自行假设屏幕一定支持 RGB 彩色。

---

# 6. `Button`

Button MUST 可通过：

- Touch；
- confirm 语义键；
- Keyboard；

至少一种当前设备可用方式触发。

按钮 SHOULD 有明确 focus 状态。

墨水屏 focus 状态优先使用：

```text
边框
反色
下划线
高对比度背景
```

而不是闪烁动画。

---

# 7. `List`

List 是 Baga Ink 的核心导航组件。

SHOULD 支持：

```text
vertical list
paged list
selection/focus
virtualization
page_next/page_previous
```

长列表 MUST 避免一次渲染全部内容。

在 Kindle 等设备上，Platform MAY 将滚动转换为页式移动。

---

# 8. `Menu`

Menu SHOULD 支持：

```text
items
selected
shortcut/action
submenu
```

菜单必须能使用语义动作：

```text
up
down
confirm
back
```

---

# 9. `Dialog`

Dialog 用于：

- 确认；
- 权限请求；
- 错误；
- 简单输入；
- 危险操作确认。

Dialog SHOULD：

- 避免层层嵌套；
- 保持短文本；
- 默认焦点明确；
- 支持返回键关闭（危险确认除外）；
- 尽量只触发必要区域刷新。

---

# 10. `Toolbar`

Toolbar 不应复制手机底部连续动画导航。

建议：

```text
少量主要动作
文本 + 简单图标
可通过 focus 导航
```

在小屏 Kindle 上 MAY 自动折叠成 Menu。

---

# 11. 布局模型

v0.1 SHOULD 使用简单、确定性的布局模型：

```text
Row
Column
Stack
Fixed / Flex size
Margin
Padding
Alignment
```

避免第一阶段实现复杂 CSS Layout。

目标：

> **跨平台可预测，而不是功能无限。**

---

# 12. 坐标与尺寸

App SHOULD 使用 Platform 提供的逻辑尺寸。

不得：

```text
假设 Kindle 固定 1072×1448
假设 Android 固定 density
按厂商型号硬编码像素布局
```

UI SHOULD 根据：

```text
logical width
logical height
orientation
text scale
input capabilities
```

适配。

---

# 13. Responsive Profile

Baga Ink 不照搬手机的 breakpoints，但可以定义逻辑屏幕档位：

```text
compact
medium
large
```

依据有效逻辑尺寸与文本排版能力判断。

App SHOULD 查询布局 Profile，而不是识别型号。

---

# 14. Focus Model

因为部分 Kindle 没有触摸或需要物理键导航，Focus 是一级概念。

可交互控件 MUST 能：

```text
focus
blur
activate
move_next
move_previous
```

Platform SHOULD 提供默认 focus traversal。

App MAY 自定义复杂页面的 focus order。

---

# 15. Semantic Actions

UI 层应该围绕：

```text
confirm
back
menu
page_next
page_previous
focus_next
focus_previous
```

设计。

底层可以来自：

- Kindle 翻页键；
- Touch；
- Android volume key；
- Keyboard；
- Bluetooth remote。

---

# 16. Refresh Intent

UI 与 Display 的边界非常重要。

App / UI MAY 表达：

```text
content_changed
small_interaction
page_changed
quality_needed
continuous_interaction
```

Platform 再映射为：

```text
AUTO
TEXT
FAST
QUALITY
ANIMATION
```

App MUST 不传递 Vendor waveform ID。

---

# 17. Dirty Region

UI engine SHOULD 追踪 dirty region。

原则：

```text
一个按钮 focus 改变
→ 只 invalidate 按钮相关区域
```

而不是：

```text
任意状态改变
→ 全屏刷新
```

Platform MAY 合并多个 dirty region。

---

# 18. Ghosting Policy

残影治理主要属于 Platform / Device Adapter。

App 不应实现：

```text
每 N 次自己 full refresh
```

统一方向：

```text
UI state change
  ↓
Display intent
  ↓
Platform refresh policy
  ↓
Device Adapter
```

这样不同设备可以使用不同清残影策略。

---

# 19. Animation Policy

默认：

> **无动画比差动画更好。**

Universal App SHOULD 不依赖动画表达状态。

允许场景：

- 设备声明 `display.animation`；
- 动画能明显提高可理解性；
- Platform 可自动降级为离散帧 / 无动画。

动画 MUST 可被 Platform 全局禁用。

---

# 20. Scroll Policy

墨水屏上的连续像素滚动不是默认交互。

Platform SHOULD 支持：

```text
paged
step_scroll
continuous_scroll (optional)
```

App SHOULD 允许 `paged` 降级。

Reader / 长文场景优先页式或分段翻动。

---

# 21. Touch Target

Touch 设备上交互区域 SHOULD 足够大。

v0.1 不冻结具体 dp 数值，但测试套件 SHOULD 检查：

- 控件不极端狭小；
- 主要按钮间距合理；
- 不依赖细小 icon-only 点击区。

---

# 22. Pen UI

如果设备有 `input.pen`：

- UI MAY 提供笔输入；
- 普通触摸与 Pen SHOULD 可区分；
- 低延迟笔迹必须通过 Platform 标准 Capability；
- App 不直接调用 BOOX / iReader 私有手写 SDK。

没有 Pen 时，应用必须根据 required/optional capability 正确处理。

---

# 23. Color Policy

彩色设备不是默认前提。

App MUST 不用颜色作为唯一状态区分。

例如错误：

```text
绿色 = 成功
红色 = 失败
```

正确：

```text
✓ 成功
! 失败
```

颜色只作为增强。

---

# 24. 图标规范

图标 SHOULD：

- 轮廓清楚；
- 黑白可辨；
- 不依赖渐变；
- 低分辨率下保持可读；
- 同时提供文本替代或 accessibility label。

---

# 25. 权限 UI

Permission Dialog 由 Platform 提供统一组件。

App 不得伪造系统 / Platform 授权界面。

授权页面必须明确：

```text
App name
permission name
purpose
Allow / Deny
```

---

# 26. Error UI

标准错误 SHOULD 映射为：

```text
offline
permission_denied
not_supported
incompatible
not_found
io_error
```

App SHOULD 给用户可操作的下一步，而不是显示底层 Vendor 错误码。

---

# 27. Accessibility

即使第一阶段规模小，也 SHOULD 保留：

- 文本缩放；
- 高对比度；
- focus 顺序；
- 图标文字替代；
- 不依赖颜色；
- 键盘 / 物理键导航。

---

# 28. UI Theme

Baga Ink SHOULD 提供基础 theme token：

```text
background
foreground
border
muted
focus
font.body
font.title
spacing.*
```

App SHOULD 使用 token 而不是硬编码大量设备相关样式。

第一阶段不追求复杂主题市场。

---

# 29. LifeBook 作为 Reference UI

LifeBook SHOULD 成为 Baga Ink UI 第一 Reference App。

它的任务不是获得特权，而是验证：

```text
文章
问答
评论
笔记
书籍阅读
列表
菜单
同步状态
AI 对话
```

能否只依靠标准 UI/API 在 Kindle 与 Android E-Paper 运行。

任何 LifeBook 需要的平台级 UI 能力 SHOULD 优先标准化，而不是做 LifeBook 私有逃生口。

---

# 30. UI 合规测试

Compatibility / App Test SHOULD 验证：

- 页面可显示；
- 无触摸设备可导航；
- touch 设备可点击；
- page_next / page_previous 正常；
- focus 可见；
- 大小屏不严重溢出；
- 无颜色设备信息不丢失；
- Display intent 不泄漏 Vendor API；
- 更新小区域时不过度全刷。

---

# 31. 核心原则 / Core Rule

> **Baga Ink UI 不是“跨平台画一样的像素”，而是“跨设备保持一样的交互语义，并让每台墨水屏用最合适的方式呈现”。**
