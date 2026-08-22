# Baga Ink 兼容性标准 / Baga Ink Compatibility Standard

> **文档级别：一级平台规范**  
> **状态：Draft v0.2**  
> **日期：2026-08-22**  
> **上位文档：`01_顶层战略与架构_Baga-Ink-Platform-Strategy.md`**  
> **配套规范：`04_能力注册表_Baga-Ink-Capability-Registry.md`、`07_设备适配器规范_Baga-Ink-Device-Adapter-Specification.md`、`10_兼容性测试套件_Baga-Ink-Compatibility-Test-Suite.md`**

---

## 0. 目的

本文档定义：

> **什么样的设备、系统组合和 Device Adapter，才可以称为 Baga Ink Compatible。**

Baga Ink 的统一性不能靠“看起来能运行”判断，也不能靠设备品牌白名单判断。

兼容性的基础是：

1. Platform Core 能否稳定工作；
2. Device Adapter 是否正确实现平台要求；
3. Capability 声明是否真实；
4. 标准 IKP 是否能按照相同语义运行；
5. 是否通过 Baga Ink Compatibility Test Suite；
6. 是否满足数据安全、更新恢复和墨水屏行为要求。

核心原则：

> **不要求所有设备拥有相同硬件，但要求相同 API 在已声明能力范围内具有相同语义。**

---

# 1. 适用对象

本规范适用于：

- Kindle 设备上的 Baga Ink Platform；
- Android E-Paper 设备上的 Baga Ink Platform；
- 第三方厂商实现的 Baga Ink Device Adapter；
- Baga Ink Client 的设备识别与兼容状态展示；
- Baga Ink Market 的设备兼容标签；
- 后续新增的其他电子纸设备平台。

本规范不要求所有设备拥有触摸、手写、蓝牙、音频、彩色或快速刷新。

这些差异必须通过 Capability Model 表达。

---

# 2. 兼容性等级

## 2.1 Baga Ink Compatible

要求：

- 满足全部 Mandatory Requirements；
- Device Adapter 通过对应版本 BICTS；
- 至少通过官方 Universal Reference Apps；
- 不存在已知用户数据破坏性安装流程；
- Capability 声明经过验证；
- Platform 更新和失败恢复满足最低要求。

## 2.2 Baga Ink Compatible + Profile

可附加：

```text
Touch
Pen
Fast Refresh
Color
Audio
Bluetooth
```

Profile 只表示额外能力，不形成平台分叉。

## 2.3 Experimental

可运行 Platform，但尚未达到正式认证要求。

Baga Ink Client MUST 清楚显示实验性支持，不能伪装成正式兼容。

## 2.4 Unsupported

存在以下任一情况时应标记 Unsupported：

- Platform 无法可靠安装或启动；
- 存在高风险数据破坏；
- 核心 Display / Input / Storage 无法满足基本语义；
- 必须恢复出厂才能正常工作；
- 设备或固件已知会导致不可恢复故障；
- 无法实现最低 API 基线。

---

# 3. Base Compatibility Profile

所有 Compatible 设备必须满足：

```text
display.basic
input.navigation
storage.app_sandbox
power.sleep_wake
platform.lifecycle
```

正式语义以 `04_能力注册表_Baga-Ink-Capability-Registry.md` 为准。

Base Profile 不要求触摸、音频、Pen、彩色或蓝牙。

---

# 4. Platform 可安装与可启动

设备 MUST：

- 能安装 Baga Ink Platform；
- 从用户可理解入口启动；
- 重启后保持正确安装状态；
- 正确加载受支持 IKP；
- App 崩溃后恢复到可用状态。

安装方式可以因 Kindle / Android 不同，但 App 层语义不能不同。

---

# 5. 用户数据安全

安装、升级、修复流程 MUST：

- 不删除用户书籍；
- 不删除用户笔记；
- 不默认删除用户个人文档；
- 不要求恢复出厂；
- 不把清空设备作为正常故障修复方案；
- 失败时尽量保留原有可工作状态。

任何已知数据破坏风险都会阻止正式 Compatible 标签。

---

# 6. IKP 一致性

同一个 Universal IKP：

- MUST 不因设备品牌改变包内容；
- MUST 不要求 Kindle / Android 各自打不同 IKP；
- MUST 不要求 App 内含设备私有执行桥；
- SHOULD 在 Capability 条件相同的设备上呈现相同业务语义。

---

# 7. API 基线

设备 MUST 实现对应 Platform 版本声明的 Mandatory API Surface。

若某能力无法提供：

- Adapter MUST 不伪造支持；
- `baga.device.has()` MUST 返回真实结果；
- API SHOULD 返回 `not_supported`；
- Market / Client SHOULD 基于 Capability 阻止不兼容 App 安装。

---

# 8. Capability Truthfulness

Capability 声明必须真实、稳定、可测试。

禁止：

- 因为同系列理论上有某硬件就声明支持；
- 因厂商宣传页写了某功能就直接声明；
- 某固件不可用时仍保持 true；
- 用 true 表示“可能支持”。

如果能力依赖固件版本，Adapter MUST 按实际系统状态报告。

---

# 9. Display Compatibility

Adapter MUST 提供：

- 屏幕尺寸；
- 可用显示区域；
- 方向信息；
- 基本刷新；
- 支持时的局部刷新；
- 支持时的快速刷新；
- Display Mode 到设备实现的映射。

App 使用的语义模式：

```text
AUTO
TEXT
QUALITY
FAST
ANIMATION
```

这些是显示意图，不是硬件 waveform ID。

---

# 10. Input Compatibility

核心语义动作：

```text
confirm
back
menu
page_next
page_previous
```

设备 MAY 额外提供 touch / pen / keyboard / physical_button。

App 不得依赖 Android keycode 或 Kindle 私有键值。

---

# 11. Storage Compatibility

设备 MUST 支持 Baga Ink App 沙箱。

至少提供：

```text
appdata/
cache/
documents/
downloads/
```

Platform / Adapter MUST：

- 防止路径逃逸；
- 隔离不同 App 私有数据；
- Platform 更新时保留 App 数据；
- 正确处理磁盘不足；
- 返回统一错误码。

---

# 12. Lifecycle Compatibility

设备 MUST 映射：

```text
start
resume
pause
sleep
wake
stop
```

Universal App 不得因为 Android Activity 或 Kindle 私有进程模型不同而需要两套业务逻辑。

---

# 13. Power Compatibility

设备 MUST 至少提供：

- sleep / wake 状态桥接；
- 电量读取（可用时）；
- 充电状态（可用时）；
- keep-awake 请求的支持/不支持结果。

Platform MAY 根据系统策略、电量与用户设置拒绝请求。

---

# 14. Network Compatibility

网络不是 Base Profile 必需硬件。

设备如果声明网络 Capability，则 MUST：

- 正确报告 online / offline；
- 通过 Baga Ink Network API 发起受支持请求；
- 正确处理断网与 sleep/wake；
- 不要求 App 直接调用 Android 或 Kindle 网络接口。

---

# 15. Optional Capability Profiles

Profile 基于 Capability Registry 自动形成。

典型：

```text
Touch       → input.touch
Pen         → input.pen
FastRefresh → display.fast_refresh
Color       → display.color
Audio       → audio.output
Bluetooth   → bluetooth.available
```

声明某 Profile 必须通过对应 BICTS suite。

---

# 16. Performance 与资源约束

Compatible 不要求所有设备拥有相同 CPU、RAM、存储和刷新速度。

但设备必须达到“可稳定运行标准 Reference Apps”的最低可用性。

具体性能阈值 SHOULD 在 Test Profile 中按设备类别定义，而不是按品牌硬编码。

---

# 17. Upgrade 与 Recovery

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

Platform / Client SHOULD 保留上一已知可用版本，并在升级后重新验证 Capability。

---

# 18. Security Baseline

Compatible 设备必须满足：

- IKP 执行前验证；
- 路径安全检查；
- App 沙箱隔离；
- 权限声明检查；
- 不默认允许 arbitrary shell；
- 不默认允许 App 直接访问 Vendor API；
- 正确处理恶意或损坏 IKP；
- App 崩溃不破坏 Platform 主体。

---

# 19. BICTS

正式认证必须基于：

> **Baga Ink Compatibility Test Suite (BICTS)**

完整定义见 `10_兼容性测试套件_Baga-Ink-Compatibility-Test-Suite.md`。

测试结果必须可机器读取、可回归、可绑定设备/固件/Adapter/Platform 版本。

---

# 20. Reference Apps

Baga Ink SHOULD 维护：

```text
HelloInk
ListNavigation
ReaderMini
StorageProbe
PermissionProbe
DisplayProbe
LifecycleProbe
LifeBook Reference App
```

单纯逐 API 测试不足以证明真实兼容。

LifeBook 是重要真实场景，但认证规则不能只围绕 LifeBook 私有需求设计。

---

# 21. Firmware / OS Version 维度

Compatibility 是：

> **Device Model + OS/Firmware Range + Platform Version + Adapter Version**

的组合，而不是只按设备型号判断。

同一型号不同固件可以分别是 Compatible / Experimental / Unsupported。

---

# 22. Baga Ink Client 兼容展示

Client SHOULD 对普通用户展示：

```text
✓ Baga Ink Compatible
△ Experimental
✕ Unsupported
```

并展示附加 Profile。

不应向普通用户暴露复杂 Adapter 内部实现。

---

# 23. Market 兼容判断

Market 安装判断应基于：

```text
App Manifest
+ Device Capability Set
+ Baga Ink API Version
+ Compatibility Status
```

而不是型号白名单作为正常机制。

型号黑名单 MAY 仅作为严重缺陷的临时安全措施。

---

# 24. 厂商认证流程

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

长期目标是从 Baga Ink 主动适配厂商，转为厂商主动适配 Baga Ink Standard。

---

# 25. Certification Artifact

每次正式认证 SHOULD 生成机器可读报告，例如：

```json
{
  "device_family": "kindle",
  "model": "example",
  "firmware_range": ">=x <y",
  "baga_platform": "0.x",
  "adapter_version": "0.x",
  "compatibility_standard": "0.2",
  "status": "compatible",
  "profiles": ["touch", "fast_refresh"],
  "test_suite": "0.1",
  "tested_at": "2026-08-22"
}
```

---

# 26. 标准版本化

设备认证必须明确基于哪个版本：

```text
Baga Ink Compatibility Standard
Baga Ink API
Baga Ink Device Adapter Specification
BICTS
```

新标准版本不得无理由让已工作的旧设备全部失效。

平台 SHOULD 尽量保持存量设备价值。

---

# 27. 顶层原则总结

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
        │
        ▼
BICTS
        │
        ▼
Baga Ink Compatible
```

最终，一个设备被称为 **Baga Ink Compatible**，意味着：

> **第三方开发者可以相信 Baga Ink 标准，而不用重新学习这台设备。**
