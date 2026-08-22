# Baga Ink App Standard

> **文档级别：一级平台规范**  
> **状态：Draft v0.1**  
> **日期：2026-08-22**  
> **上位文档：`BAGA_INK_PLATFORM_STRATEGY.md`**

---

## 0. 目的

本文档定义第三方应用如何成为一个 **Baga Ink App**，以及什么条件下可以获得 **Baga Ink Universal** 兼容标识。

本标准的首要目标不是提供最多能力，而是建立一个长期稳定的跨设备应用边界，防止 Baga Ink 生态在扩张后重新碎片化。

本规范约束应用开发者；设备厂商与适配层的要求由 Baga Ink Compatibility Standard / Device Adapter Specification 另行定义。

本文中的 MUST / SHOULD / MAY 含义继承顶层战略文档。

---

# 1. 应用类别

Baga Ink 定义三类应用/扩展。

## 1.1 Baga Ink Universal App

Universal App 是平台默认、优先和最重要的应用形态。

Universal App MUST：

- 使用 Baga Lua Profile；
- 以 `.ikp` 包格式发布；
- 仅通过 Baga Ink API 获取平台能力；
- 使用 Capability Model 判断硬件能力；
- 遵守标准生命周期；
- 遵守权限与沙箱；
- 不直接访问 Vendor / OS 私有 API；
- 不携带平台相关 native binary；
- 不要求开发者为 Kindle、BOOX、iReader 等分别维护应用逻辑分支。

符合全部要求并通过兼容测试的应用 MAY 标记：

> **Baga Ink Universal**

## 1.2 Device Enhanced App

Device Enhanced App 仍以 Baga Ink API 为主要开发边界，但 MAY 使用由 Platform 暴露的标准化扩展 Capability。

例如：

```text
pen.low_latency
display.vendor_fast_mode
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

例如 LifeBook 可拥有独立 ID，但第三方开发者无需成为 Baga Ink 品牌命名空间的一部分。

---

# 3. 版本

应用版本 SHOULD 使用语义化版本形式：

```text
MAJOR.MINOR.PATCH
```

例如：

```text
1.4.2
```

应用 MUST 在 IKP Manifest 中声明：

- app version；
- IKP format version；
- 所需 Baga Ink API version；
- required capabilities；
- optional capabilities。

Platform MUST 在启动应用前完成兼容检查。

---

# 4. Baga Lua Profile

Universal App 的第一官方语言为 Lua，但应用不是运行在“任意 Lua”上，而是运行于 **Baga Lua Profile**。

## 4.1 允许的基础能力

Baga Lua Profile SHOULD 提供安全、可移植的基础库，例如：

```text
string
table
math
utf8
coroutine
```

具体 Lua 版本由 SDK 版本定义。

## 4.2 默认禁止的系统逃逸能力

Universal App MUST 不依赖以下能力：

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

应用不得假设标准桌面 Lua 环境完整存在。

---

# 5. 应用生命周期

Baga Ink App MUST 使用统一生命周期模型。

第一阶段语义事件包括：

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

- 能够在 `sleep` 前快速保存必要状态；
- 不假设网络长期在线；
- 不假设进程会永久驻留；
- 不依赖某一 Android Activity 或 Kindle 私有进程模型；
- 在 `wake` 后重新验证网络和设备能力状态。

平台 MAY 因设备限制合并某些底层事件，但对 App 暴露的语义必须保持一致。

---

# 6. Capability Model

## 6.1 基本原则

应用 MUST 查询“设备具有什么能力”，而不是“设备是什么品牌”。

推荐：

```lua
if baga.device.has("input.pen") then
    enable_pen_ui()
end
```

不推荐：

```lua
if device.vendor == "BOOX" then
    enable_pen_ui()
end
```

## 6.2 Required Capability

如果应用没有某能力就无法工作，应在 Manifest 中声明 required capability。

Platform MUST 在安装或启动前提示不兼容，而不是允许应用运行后随机崩溃。

## 6.3 Optional Capability

可增强体验但不是必需能力的，应声明 optional capability。

应用 MUST 对 optional capability 缺失提供合理降级。

---

# 7. 权限模型

Capability 与 Permission 是两个不同概念：

- **Capability**：设备是否具备某能力；
- **Permission**：应用是否被允许使用某资源或用户数据。

例如：

```text
Capability: network.wifi
Permission: network
```

一个设备可以有 Wi-Fi，但应用没有 network permission。

第一阶段权限类别可包括：

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

---

# 8. Storage 与沙箱

每个 App MUST 拥有独立应用沙箱。

建议逻辑路径：

```text
appdata/
cache/
documents/
downloads/
```

应用：

- MUST 不假设 Android 或 Kindle 的真实文件路径；
- MUST 不直接扫描系统目录；
- SHOULD 使用 Baga Ink Storage API；
- MUST 通过显式权限访问用户书库或用户选择的外部文件。

卸载应用时，Platform SHOULD 明确区分：

- 可安全删除的 cache；
- app private data；
- 用户主动创建且可能需要保留的 documents。

---

# 9. Network 与离线优先

墨水屏经常处于断网或低频联网状态，因此 Baga Ink App SHOULD 默认采用 offline-first 思维。

应用 MUST：

- 正确处理无网络；
- 不把网络在线作为正常启动前提；
- 不持续高频轮询；
- 不因同步失败破坏本地数据；
- 使用 Baga Ink Network / Sync API，而不是直接依赖平台私有网络接口。

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

应用应该围绕语义动作设计交互，例如：

```text
page_next
page_previous
confirm
back
menu
```

而不是将核心操作硬编码成某个物理键码。

Platform 负责将：

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

如果应用使用阅读能力，SHOULD 优先调用 Baga Ink Reader API。

应用不应因为 Baga Ink Platform 某一版本内部复用了 KOReader，就直接依赖 KOReader 私有 Lua 对象。

原则：

```text
App → Baga Ink Reader API → Reader implementation
```

而不是：

```text
App → KOReader internals
```

这保证未来 Reader Engine 可替换或演进。

---

# 15. 依赖规则

为了避免早期生态出现传统包管理器式 dependency hell，Universal App v0.1 SHOULD 默认自包含。

第一阶段：

- App MAY 使用 Baga Ink Platform 标准库；
- App MAY 将纯 Lua 第三方库打入自己的 IKP；
- App MUST 不依赖某个用户另行安装的随机 native library；
- App MUST 不依赖某个厂商系统中“碰巧存在”的动态库；
- 跨 App shared dependency 暂不作为 v0.1 核心能力。

后续如引入共享组件，应由独立版本化规范定义。

---

# 16. 安全与稳定性

应用 MUST：

- 不尝试突破沙箱；
- 不篡改 Platform；
- 不修改其他 App 私有数据；
- 不通过未声明接口访问敏感资源；
- 不假设可执行任意 native code；
- 对来自网络、文件和用户输入的数据做基本验证。

Platform MAY 因安全原因终止违反规则的 App。

---

# 17. 签名与发布者身份

进入 Baga Ink Market 的 App SHOULD 使用受支持的数字签名。

应用更新 MUST 保持 Application ID，并 SHOULD 保持发布者签名连续性。

如果签名密钥发生变化，应通过明确的 key rotation / recovery 机制处理，而不是允许任意新签名覆盖原应用。

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
3. 只使用公开 Baga Ink API；
4. 不携带设备相关 native binary；
5. 不调用 raw shell / vendor SDK；
6. 使用 Capability Model；
7. 权限完整声明；
8. 使用标准生命周期；
9. 通过 Compatibility Test；
10. 至少通过两个不同平台家族的 Reference Test（目标为 Kindle + Android E-Paper）。

第 10 条是非常重要的反碎片化原则：Universal 不应只因为“理论上用了统一 API”就获得认证，而应证明真正跨平台。

---

# 20. 向后兼容原则

在 Baga Ink API 进入稳定版本后：

- Patch / Minor 更新 SHOULD 不破坏已发布的兼容 API；
- 废弃 API 应先标记 deprecated，并提供迁移周期；
- Platform SHOULD 在合理范围内继续运行旧 IKP；
- Breaking change 应通过新的 major API version 引入。

在 `v0.x` 阶段允许更快演进，但所有不兼容变更 MUST 明确记录。

---

# 21. 开发者的核心心智模型

Baga Ink App 开发者应该只需要理解：

```text
Lua
+
Baga Ink SDK
+
Baga Ink API
+
Capability
+
Permission
+
IKP
```

而不需要先学习：

```text
KUAL
MRPI
Kindle framebuffer
BOOX refresh SDK
iReader private API
Android vendor differences
```

如果普通 Baga Ink App 开发仍然必须学习后一组知识，本标准的目标就没有实现。

---

# 22. v0.1 明确不做的事情

本版本暂不把以下能力定义为 Universal App 标准：

- 任意 native binary；
- 任意 Shell；
- 任意 Java / JNI bridge；
- 自定义 Kernel / Driver；
- 跨 App 共享 native dependency；
- Vendor-specific API 直接调用；
- WebView / Chromium 作为默认 App Runtime；
- 每个 App 自己实现系统级更新机制。

这些能力如未来需要，应位于受控扩展层，而不是侵蚀 Universal App 边界。

---

# 23. 合规判断

Baga Ink App Standard 的最终判断问题只有一个：

> **这个应用是否真正面向 Baga Ink Platform 开发，而不是借 Baga Ink Market 分发一个仍然绑定某台设备的应用？**

只有前者，才能构成长期统一的 Baga Ink 生态。
