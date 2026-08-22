# Baga Ink Compatibility Standard

> **文档级别：一级平台规范**  
> **状态：Draft v0.1**  
> **日期：2026-08-22**  
> **上位文档：`BAGA_INK_PLATFORM_STRATEGY.md`**  
> **配套规范：`BAGA_INK_APP_STANDARD.md`、`BAGA_INK_API_SPECIFICATION.md`、`IKP_PACKAGE_SPECIFICATION.md`、`BAGA_INK_DEVICE_ADAPTER_SPECIFICATION.md`**

---

## 0. 目的

本文档定义：

> **什么样的设备、系统组合和 Device Adapter，才可以称为 Baga Ink Compatible。**

Baga Ink 的统一性不能靠“看起来能运行”判断，也不能靠设备品牌白名单判断。

兼容性的唯一基础应当是：

1. Platform Core 能否稳定工作；
2. Device Adapter 是否正确实现平台要求；
3. Capability 声明是否真实；
4. 标准 IKP 是否能按照相同语义运行；
5. 是否通过 Baga Ink Compatibility Test Suite；
6. 是否满足数据安全、更新恢复和墨水屏行为要求。

兼容认证的核心原则是：

> **不要求所有设备拥有相同硬件，但要求相同 API 在已声明能力范围内具有相同语义。**

---

# 1. 适用对象

本规范适用于：

- Kindle 设备上的 Baga Ink Platform；
- Android E-Paper 设备上的 Baga Ink Platform；
- 第三方设备厂商实现的 Baga Ink Device Adapter；
- Baga Ink Client 的设备识别与兼容状态展示；
- Baga Ink Market 的设备兼容标签；
- 后续新增的其他电子纸设备平台。

本规范**不要求所有设备拥有触摸、手写、蓝牙、音频、彩色或快速刷新**。

这些差异应通过 Capability Model 表达，而不是通过排除设备解决。

---

# 2. 兼容性等级

Baga Ink 定义四种设备状态。

## 2.1 Baga Ink Compatible

设备可以正式标记：

> **Baga Ink Compatible**

要求：

- 满足本规范全部 Mandatory Requirements；
- Device Adapter 通过对应版本 Compatibility Test Suite；
- 至少通过官方 Universal Reference Apps 测试；
- 不存在已知的用户数据破坏性安装流程；
- Capability 声明经过验证；
- Platform 更新和失败恢复满足最低要求。

## 2.2 Baga Ink Compatible + Profile

在 Compatible 基础上，可附加能力 Profile，例如：

```text
Baga Ink Compatible · Touch
Baga Ink Compatible · Pen
Baga Ink Compatible · Fast Refresh
Baga Ink Compatible · Color
Baga Ink Compatible · Audio
Baga Ink Compatible · Bluetooth
```

Profile 只表示额外能力，不形成不同的平台分支。

## 2.3 Experimental

可运行 Baga Ink Platform，但尚未达到正式认证要求。

常见原因：

- 新固件未完整验证；
- 某些核心 API 存在已知问题；
- 安装流程尚未达到可恢复要求；
- Capability 信息不完整；
- 只通过部分测试。

Baga Ink Client MUST 明确显示：

> **Experimental / 实验性支持**

不得伪装成正式兼容。

## 2.4 Unsupported

存在以下任一情况时，应标记 Unsupported：

- Platform 无法可靠安装或启动；
- 存在高风险数据破坏；
- 核心 Display / Input / Storage 无法满足基本语义；
- 必须要求用户恢复出厂才能正常工作；
- 设备或固件已知会导致不可恢复故障；
- 无法实现最低 Baga Ink API 基线。

---

# 3. Mandatory Requirements

任何设备要获得 **Baga Ink Compatible**，MUST 满足以下要求。

## 3.1 Platform 可安装与可启动

设备 MUST 能够：

- 安装 Baga Ink Platform；
- 从用户可理解的入口启动；
- 在设备重启后保持正确安装状态；
- 正确加载受支持的 IKP；
- 在 App 崩溃后恢复到可用状态。

安装方式可以因 Kindle / Android 而不同，但 App 层语义不能因此不同。

## 3.2 用户数据安全

标准安装、升级、修复流程 MUST：

- 不删除用户书籍；
- 不删除用户笔记；
- 不默认删除用户个人文档；
- 不要求恢复出厂；
- 不把“清空设备”作为故障修复的正常方案；
- 在失败时尽可能保留原有可工作状态。

Baga Ink Client MUST 在执行高风险步骤前拒绝或明确阻止不安全组合。

## 3.3 IKP 一致性

同一个符合 Baga Ink App Standard 的 Universal IKP：

- MUST 不因设备品牌改变包内容；
- MUST 不要求 Kindle / Android 各自打不同 IKP；
- MUST 不要求 App 内含设备私有执行桥；
- SHOULD 在 Capability 条件相同的设备上呈现相同业务语义。

## 3.4 API 基线

设备 MUST 实现对应 Platform 版本声明的 Mandatory API Surface。

若某一能力无法提供：

- Device Adapter MUST 不伪造支持；
- `baga.device.has()` MUST 返回真实结果；
- API SHOULD 返回 `not_supported`，而不是静默失败；
- Market / Client SHOULD 可基于 Capability 阻止不兼容 App 安装。

---

# 4. Capability Truthfulness

Capability 声明必须真实、稳定、可测试。

例如：

```text
display.partial_refresh = true
```

意味着 Compatibility Test Suite 可以实际调用并验证该能力。

禁止：

- 因为某型号理论上有某硬件就声明支持；
- 因厂商宣传页写了某功能就直接声明；
- 某固件版本不可用时仍保持 `true`；
- 用 `true` 表示“可能支持”。

如果能力依赖固件版本，Adapter MUST 按实际系统状态报告。

---

# 5. Base Compatibility Profile

所有 **Baga Ink Compatible** 设备必须满足 Base Profile。

Base Profile 不要求触摸、音频、手写、彩色或蓝牙。

最低要求包括：

```text
Display output
Basic semantic input
App lifecycle
App sandbox storage
Device information
Power state awareness
Clock / time access through platform facilities
IKP validation and loading
Capability reporting
Stable error handling
```

其中“Basic semantic input”可以来自：

- Touch；
- Physical key；
- Keyboard；
- 设备已有的其他可映射输入。

但设备必须至少存在一种可以完成基本 App 导航的输入方式。

---

# 6. Display Compatibility

显示是墨水屏兼容性的核心。

Device Adapter MUST 提供：

- 屏幕尺寸；
- 可用显示区域；
- 方向信息；
- 基本刷新；
- 全刷新能力；
- 支持时的局部刷新；
- 支持时的快速刷新；
- Display Mode 到设备实现的映射。

Baga Ink App 使用的语义模式：

```text
AUTO
TEXT
QUALITY
FAST
ANIMATION
```

这些是**显示意图**，不是硬件 waveform ID。

Adapter MUST：

- 不把厂商私有 waveform ID 泄漏给 Universal App；
- 对不支持的模式进行合理降级；
- 避免因 App 普通 UI 更新造成不必要全屏刷新；
- 正确处理刷新区域越界；
- 在设备需要周期性清残影时实现合理策略。

Compatibility Test SHOULD 包括：

- 文本翻页；
- 菜单打开/关闭；
- 局部区域更新；
- 连续操作后的残影处理；
- 横竖屏变化（设备支持时）。

---

# 7. Input Compatibility

Device Adapter 必须把设备输入转换成 Baga Ink 统一语义。

核心语义动作：

```text
confirm
back
menu
page_next
page_previous
```

设备 MAY 额外提供：

```text
touch
pen
keyboard
physical_button
```

Adapter MUST：

- 不要求 Universal App 使用 Android keycode；
- 不要求 Universal App 使用 Kindle 私有键值；
- 正确处理按下、释放、重复触发；
- 避免一次物理操作触发多次语义事件；
- 在支持触摸时正确报告坐标系统。

---

# 8. Storage Compatibility

设备 MUST 支持 Baga Ink App 沙箱。

至少提供逻辑空间：

```text
appdata/
cache/
documents/
downloads/
```

Platform / Adapter MUST：

- 将逻辑路径映射到设备可用存储；
- 阻止 App 通过路径逃逸访问任意系统目录；
- 保证一个 App 不能直接修改另一个 App 的私有数据；
- 在正常 Platform 更新时保留 App 数据；
- 正确处理磁盘空间不足；
- 返回统一错误码。

设备真实路径不是公开兼容接口的一部分。

---

# 9. Lifecycle Compatibility

设备 MUST 能把其底层系统行为映射到 Baga Ink 生命周期语义：

```text
start
resume
pause
sleep
wake
stop
update
```

Adapter MUST 正确处理：

- 设备休眠；
- 系统唤醒；
- App 切换；
- Platform 被系统终止；
- 重启后的状态恢复。

Universal App 不得因为 Android Activity 或 Kindle 私有进程模型不同而需要两套业务逻辑。

---

# 10. Power Compatibility

设备 MUST 至少提供：

- 电量读取（硬件可用时）；
- 充电状态（硬件可用时）；
- sleep / wake 状态桥接；
- keep-awake 请求的可支持/不可支持结果。

Adapter MUST 不因为 App 请求 keep-awake 就无条件阻止设备休眠。

Platform MAY 根据：

- 电量；
- 系统策略；
- 用户设置；
- 设备能力；

拒绝请求。

---

# 11. Network Compatibility

网络不是 Base Profile 的硬件必需项。

设备如果声明网络 Capability，则 MUST：

- 正确报告 online / offline；
- 能通过 Baga Ink Network API 发起受支持请求；
- 正确处理断网；
- 不要求 App 直接调用 Android 或 Kindle 网络接口；
- 正确处理设备休眠后的网络状态变化。

如果设备没有网络：

```text
network.* capability = false
```

离线应用仍然可以是 Universal App。

---

# 12. Optional Capability Profiles

以下能力作为 Profile 扩展 Base Profile。

## 12.1 Touch Profile

要求：

```text
input.touch
```

必须测试：

- 坐标范围；
- 点击；
- 基础拖动；
- 屏幕方向变化后的坐标映射。

## 12.2 Pen Profile

要求：

```text
input.pen
```

可以进一步声明：

```text
input.pen.pressure
input.pen.eraser
input.pen.low_latency
```

基础 Pen Profile 不自动意味着低延迟手写。

## 12.3 Fast Refresh Profile

要求：

```text
display.fast_refresh
```

必须验证：

- 模式确实比质量模式更适合快速交互；
- 切换后可以恢复正常质量显示；
- 不会导致长期不可恢复显示异常。

## 12.4 Color Profile

要求：

```text
display.color
```

App 仍应保持灰阶可用性，不应因为 Color Profile 出现而破坏普通黑白设备兼容。

## 12.5 Audio Profile

要求：

```text
audio.output
```

不规定具体扬声器、蓝牙还是其他输出形式，只保证平台语义。

## 12.6 Bluetooth Profile

要求：

```text
bluetooth
```

具体子能力由 API / Capability 规范进一步细分。

---

# 13. Performance 与资源约束

Compatibility 不要求所有设备拥有相同 CPU、RAM、存储和刷新速度。

但 Compatible 设备必须达到“可稳定运行标准参考应用”的最低可用性。

测试重点包括：

- Platform 启动不能频繁失败；
- 基础 UI 操作不能持续锁死；
- IKP 加载不能导致设备进入不可恢复状态；
- 内存不足必须可检测并失败安全；
- App 退出后资源必须能够释放；
- 长时间阅读场景不能出现持续异常功耗。

具体数值阈值 SHOULD 在后续 `Compatibility Test Profile` 中按设备类别定义，而不是在本顶层规范过早锁死。

---

# 14. Upgrade 与 Recovery

正式兼容设备必须支持安全更新原则：

```text
Current working version
        │
        ▼
Stage update
        │
     Verify
        │
   ┌────┴────┐
Success    Failure
   │           │
Switch       Keep old
```

Platform / Client SHOULD：

- 保留上一已知可用版本；
- 发生失败时允许回退；
- 不因 Platform 更新删除用户 App 数据；
- 不因 Adapter 更新删除用户书库；
- 在升级后重新验证设备 Capability。

---

# 15. Security Baseline

Baga Ink Compatible 设备必须满足：

- IKP 在执行前验证；
- 路径安全检查；
- App 沙箱隔离；
- 权限声明检查；
- 不默认允许 arbitrary shell；
- 不默认允许 App 直接访问 Vendor API；
- 正确处理恶意或损坏 IKP；
- App 崩溃不应破坏 Platform 主体。

若底层设备自身无法提供现代 OS 级隔离，Platform Core 仍 MUST 尽可能通过 API 白名单、Lua Profile、逻辑存储边界和包验证建立一致保护边界。

---

# 16. Compatibility Test Suite

正式认证必须基于：

> **Baga Ink Compatibility Test Suite (BICTS)**

BICTS SHOULD 包含以下类别：

```text
Platform startup
IKP install / validate / launch
API baseline
Capability truthfulness
Display
Input
Storage
Lifecycle
Power
Network（when declared）
Touch（when declared）
Pen（when declared）
Color（when declared）
Audio（when declared）
Bluetooth（when declared）
Upgrade / rollback
Crash recovery
Reference Apps
```

测试结果必须可机器读取并可保存版本信息。

---

# 17. Reference Apps

单纯逐 API 测试不足以证明真实兼容。

Baga Ink SHOULD 维护少量 Reference Apps，例如：

```text
Hello Ink
Reference Reader
Reference Notes
Reference Network App
Reference Input Tester
LifeBook（旗舰真实应用）
```

设备要获得正式 Compatible，至少必须通过：

- API 测试；
- 合成 UI 测试；
- 一个真实阅读场景；
- 一个真实离线/恢复场景。

LifeBook 可以作为重要真实世界验证对象，但认证规则不能只围绕 LifeBook 私有需求设计。

---

# 18. Firmware / OS Version 维度

Compatibility 是：

> **Device Model + OS/Firmware Range + Baga Ink Platform Version**

的组合，而不是只按设备型号判断。

例如同一 Kindle 型号：

```text
Firmware A → Compatible
Firmware B → Experimental
Firmware C → Unsupported
```

Baga Ink Client MUST 根据实际设备状态判断，而不是只读取市场型号。

---

# 19. Baga Ink Client 的兼容展示

Client SHOULD 对普通用户只展示清晰状态：

```text
✓ Baga Ink Compatible
△ Experimental
✕ Unsupported
```

并展示附加 Profile：

```text
Touch
Pen
Fast Refresh
Color
Audio
Bluetooth
```

不应向普通用户暴露复杂的 Adapter 内部实现细节。

---

# 20. Baga Ink Market 的兼容判断

Market 安装判断应基于：

```text
App Manifest
      +
Device Capability Set
      +
Baga Ink API Version
      +
Compatibility Status
```

而不是：

```text
if device == specific_model then allow
```

型号黑名单 MAY 作为已知严重缺陷的临时安全机制，但不应成为正常兼容体系。

---

# 21. 厂商认证流程

未来 OEM / 厂商主动接入时，推荐流程：

```text
1. 实现 Baga Ink Device Adapter
2. 提交 Device Descriptor
3. 运行 BICTS
4. 修复失败项
5. 运行 Reference Apps
6. 生成 Compatibility Report
7. 审核 Capability 声明
8. 获得 Baga Ink Compatible 标识
9. 固件更新后执行回归测试
```

这样平台关系最终从：

> Baga Ink 主动适配厂商

逐步转为：

> 厂商主动适配 Baga Ink Standard。

---

# 22. Certification Artifact

每次正式认证 SHOULD 生成机器可读报告，例如：

```json
{
  "device_family": "kindle",
  "model": "example",
  "firmware_range": ">=x <y",
  "baga_platform": "0.x",
  "compatibility_standard": "0.1",
  "status": "compatible",
  "profiles": ["touch", "fast_refresh"],
  "test_suite": "0.1",
  "tested_at": "2026-08-22"
}
```

真实 schema 由 Compatibility Test Suite 规范进一步定义。

---

# 23. 兼容标准的版本化

本规范与 API、IKP、Adapter Specification 分别版本化。

设备认证必须明确基于哪个版本：

```text
Baga Ink Compatibility Standard 0.1
Baga Ink API 0.x
Baga Ink Device Adapter Specification 0.1
```

新标准版本不得无理由让已工作的旧设备全部失效。

平台 SHOULD 尽量通过兼容窗口和 Profile 演进保持存量设备价值。

---

# 24. 顶层原则总结

Baga Ink Compatibility Standard 的核心不是要求所有墨水屏变成同一种硬件。

它要求：

```text
不同硬件
不同 OS
不同 Vendor SDK
不同输入与显示能力
        │
        ▼
Baga Ink Device Adapter
        │
        ▼
统一 Capability 语义
统一 Baga Ink API
统一 IKP 行为
```

最终，一个设备被称为 **Baga Ink Compatible**，意味着：

> **第三方开发者可以相信 Baga Ink 标准，而不用重新学习这台设备。**
