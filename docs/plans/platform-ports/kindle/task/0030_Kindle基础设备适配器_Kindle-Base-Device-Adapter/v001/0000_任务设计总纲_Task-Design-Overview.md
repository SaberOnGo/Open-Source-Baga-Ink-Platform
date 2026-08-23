# TASK-0030 v001 任务设计总纲 / Kindle Base Device Adapter Task Design

> **Task ID：`TASK-0030`**  
> **Version：`v001`**  
> **Milestone：K2 — Kindle Base Device Adapter**  
> **状态：Planned Baseline — dependency-gated**  
> **日期：2026-08-23**

---

## 0. Goal

实现一份薄 Kindle Reference Adapter：

```text
Baga Device Adapter Contract
        ↓
Kindle Adapter glue / normalization
        ↓
KOReader / koreader-base / FBInk / verified Kindle mechanisms
        ↓
Kindle hardware + firmware
```

重点是语义映射、能力探测、profile/quirk 选择、错误/事件归一化和自测，不重新实现成熟的 Kindle framebuffer/input/power stack。

---

# 1. Dependencies and Authority

前置 Gate：

```text
TASK-0010/v001 accepted K0 contract baseline
TASK-0020/v001 accepted K1 kindlehf substrate baseline
```

权威输入：

```text
docs/zh-CN/standards/07_设备适配器规范.md
docs/zh-CN/standards/11_Kindle适配规范.md
docs/zh-CN/standards/04_能力注册表.md
docs/zh-CN/standards/08_兼容性标准.md
docs/zh-CN/standards/10_兼容性测试套件.md
docs/zh-CN/reference-apps/03_Kindle具体实现架构冻结.md
```

---

# 2. Scope

Base Adapter 实现：

```text
KindleAdapterFactory
exact/conservative probe
DeviceDescriptor
native target evidence
Device Profile selection
Quirk Set selection
Capability detection
DisplayAdapter
InputAdapter
StorageAdapter
LifecycleAdapter
PowerAdapter
Error mapping
Event normalization
QUICK / INTERACTIVE self-test
Kindle Adapter Contract Tests
```

首个 target：

```text
kindlehf
firmware >= 5.16.3
```

后续 target 扩展不在本版本 Gate 中。

---

# 3. Out of Scope

```text
完整 network adapter
frontlight optional extension
audio / bluetooth / pen
ReaderUI/CREngine/MuPDF reader integration
KPM packaging
Kindle Home Entry
Client jailbreak/bootstrap automation
完整 BICTS certification claim
```

Optional capabilities 在没有可靠证据时默认不声明。

---

# 4. Internal Module Boundary

建议内部结构：

```text
platform/adapters/kindle/
├── common/
│   ├── identity
│   ├── capability_detection
│   ├── error_mapping
│   ├── event_normalization
│   └── self_test
├── display/
├── input/
├── storage/
├── lifecycle/
├── power/
├── device_profiles/
├── quirks/
└── build_targets/
```

Reader/UI、KPM、Home Entry、jailbreak route 不属于 Device Adapter 顶层 subsystem。

---

# 5. Implementation Design

## 5.1 Factory / Probe

Probe 必须偏保守。识别结果至少关联：

```text
model identity
firmware version
native target
profile id
quirk set id
backend availability
```

未知/未验证组合不得猜测为 Compatible。

## 5.2 Profiles and Quirks

保持两层分离：

```text
Device Profile
→ 一组可解释的设备/固件能力与 backend 选择

Quirk Set
→ 对已知偏差做最小修正
```

Quirk 不成为复制整套 Adapter 的理由。

## 5.3 Display

优先包装：

```text
KOReader Kindle screen knowledge
FBInk
verified Kindle mechanisms
```

Baga `RefreshIntent` 只映射到已验证 backend 行为；不得把 Kindle 私有 waveform 名称提升为通用 App API。

## 5.4 Input

优先复用 KOReader Kindle input knowledge，把底层事件归一化为 Baga semantic navigation/pointer event。

不以重新扫描 `/dev/input/*` 作为默认实现路径；只有真实设备 quirk 需要且有证据时才增加底层补充。

## 5.5 Storage

提供 Baga app sandbox/containment 所需文件系统能力，并与 Kindle 用户书库区域保持边界。App package、App data、Kindle 用户书籍不得混放为同一管理域。

## 5.6 Lifecycle / Power

将经验证的 Kindle/KOReader/Homebrew lifecycle 与 power 事件映射为 Baga：

```text
start / resume / pause / sleep / wake / stop
power.sleep_wake
```

不得用固定计时器代替真实生命周期信号。

---

# 6. Test Strategy

分三层：

```text
A. Contract tests against Mock/fakes
B. Kindle backend integration tests
C. real kindlehf tests
```

至少覆盖：

```text
factory exact probe
descriptor completeness
unknown firmware conservative behavior
base capability consistency
display geometry
safe refresh
navigation normalization
storage containment
sleep/wake mapping
profile/quirk separation
backend error normalization
self-test result
```

---

# 7. Real-device Validation

首个真机矩阵至少包含一台已记录精确型号/固件的 `kindlehf`。

设备动作：

```text
1. 记录 device evidence
2. 启动 K1 pinned substrate
3. 初始化 KindleAdapterFactory
4. 保存 descriptor/capability/profile/quirk 结果
5. 验证显示与输入
6. 在隔离 App data 目录验证 storage
7. 执行 sleep/wake
8. 运行 QUICK self-test
9. 运行需人工交互的 INTERACTIVE 项
10. 收集日志并恢复开发状态
```

---

# 8. Data Protection and Recovery

真机测试不应清空用户书籍、笔记或执行恢复出厂。

Storage 测试只使用专用测试 App sandbox；Adapter 失败后应可停止 Platform process、移除测试资产并恢复到 K1 substrate 基线。

---

# 9. Acceptance Gate

- [ ] Factory 对精确测试设备给出稳定 descriptor/profile/quirk/native-target 结果。
- [ ] 未知 firmware 使用保守行为，不自动继承 Compatible。
- [ ] Base capability snapshot 与实际 backend 一致。
- [ ] Display geometry 与安全刷新通过测试。
- [ ] Input 被归一化为 Baga semantic event。
- [ ] Storage containment 通过 Contract Tests。
- [ ] Lifecycle/Power 的 sleep/wake 映射在真实设备成立。
- [ ] Error/Event normalization 与 Contract 一致。
- [ ] QUICK/INTERACTIVE self-test 可执行并产生证据。
- [ ] Kindle Adapter Contract Tests 通过。
- [ ] 未重新实现已有成熟 framebuffer/input/reader/power stack。

Adapter tests 通过不等于整机 BICTS/Compatible 认证通过。

---

# 10. Known Risks and Open Questions

风险集中在：固件差异、同型号跨 ABI 边界、profile/quirk 误分类、刷新语义映射、sleep/wake race、第三方 substrate 更新。

实现期应记录所有需要 Kindle-specific correction 的证据；只有可复用且稳定的语义才进入 Adapter，单次实验性 workaround 不应直接成为长期 Contract。

---

# 11. Expected Execution-Prompt Groups

```text
A. Contract baseline consumption
B. Factory/descriptor/probe
C. Profile + quirk selection
D. capability detection
E. Display
F. Input
G. Storage
H. Lifecycle + Power
I. error/event normalization + self-test
J. Contract tests + real-device K2 Gate
```
