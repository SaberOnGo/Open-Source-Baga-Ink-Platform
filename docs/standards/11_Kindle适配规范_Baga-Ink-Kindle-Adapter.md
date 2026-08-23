# Baga Ink Kindle 设备适配规范 / Baga Ink Kindle Device Adapter

> **文档级别：首发设备家族参考适配规范 / Reference Device-Family Adapter Standard**  
> **状态：Draft v0.6**  
> **日期：2026-08-23**  
> **上位契约：`07_设备适配器规范_Baga-Ink-Device-Adapter-Specification.md`**  
> **认证依据：`08_兼容性标准_Baga-Ink-Compatibility-Standard.md`、`10_兼容性测试套件_Baga-Ink-Compatibility-Test-Suite.md`**  
> **标准库依据：`13_标准库与成熟组件采用规范_Baga-Ink-Standard-Libraries-and-Adopted-Components.md`**  
> **Kindle 实现冻结：`../reference-apps/03_Kindle具体实现架构冻结_Baga-Ink-Kindle-Implementation-Architecture-Freeze.md`**

---

## 0. 目的

本文档定义 Kindle 系列如何实现 `07 Device Adapter Contract`。

核心原则：

> **Baga Kindle Device Adapter 不重写 Kindle。它利用 KOReader、koreader-base、FBInk、Kindle OS/Homebrew 已有成熟能力，把不同 Kindle 的硬件、固件和系统差异归一化为 Baga Device Adapter Contract。**

因此 Kindle Adapter SHOULD 尽量薄。

真正新增代码 SHOULD 主要集中在：

```text
Baga interface glue
Capability normalization
Device detection / profile selection
Quirk selection and correction
Error/event normalization
Self-test / diagnostics
Contract tests
```

而不是重新实现：

```text
framebuffer stack
input stack
reader engine
E-Ink refresh algorithms
network stack
power manager
```

如果已有成熟实现满足需要，优先包装/调用它。

---

# 1. 权威边界

必须区分三类文档：

```text
07 Device Adapter Contract
→ 所有设备必须实现什么

11 Kindle Device Adapter
→ Kindle 如何实现 07

03 Kindle Implementation Architecture Freeze
→ Kindle 的 Client/bootstrap/KPM/MRPI/Platform/IKP/Home Entry 等整体实现冻结
```

因此：

- `07` 是 Device Adapter Contract 的最高权威；
- 本 `11` 是 Kindle 家族实现规范；
- `reference-apps/03` 不重新定义 Adapter Contract，只定义 Kindle 整体实现边界和成熟模块采用关系。

---

# 2. Kindle 实现总体结构

推荐内部代码组织：

```text
Baga Kindle Device Adapter
│
├── common/
│   ├── identity
│   ├── capability_detection
│   ├── error_mapping
│   ├── event_normalization
│   └── self_test
│
├── display/
│   ├── KOReader Kindle display knowledge
│   └── FBInk / verified Kindle mechanisms
│
├── input/
│   └── KOReader Kindle input knowledge
│
├── storage/
│   ├── Kindle filesystem
│   └── sandbox enforcement hooks
│
├── lifecycle/
│   └── Kindle / KOReader / Homebrew events
│
├── power/
│   └── Kindle validated mechanisms
│
├── network/
│   └── Kindle connectivity bridge
│
├── light/
│   └── frontlight backend
│
├── library/
│   └── Kindle user-library bridge
│
├── device_profiles/
│   ├── model + firmware records
│   └── capability expectations / backend choices
│
├── quirks/
│   └── model + firmware corrections
│
└── build_targets/
    ├── kindle-legacy
    ├── kindle
    ├── kindlepw2
    └── kindlehf
```

这只是 Reference implementation 的内部组织，不是 Universal App 公开 API。

---

# 3. Kindle Adapter 与其他成熟组件的边界

## 3.1 可以帮助实现 Device Adapter 的成熟能力

```text
KOReader / koreader-base Kindle device knowledge
FBInk
Kindle OS interfaces
validated Homebrew mechanisms
```

这些可用于：

```text
Display
Input
Lifecycle
Power
Frontlight
部分 network/device detection
```

## 3.2 不属于 Device Adapter 的 Kindle 组件

### KOReader Reader/UI shared implementation

```text
ReaderUI / CREngine / MuPDF
UIManager / widgets
```

它们可以作为 Baga Platform 的 Reader/UI implementation，但 **Reader/UI 本身不是 Device Adapter 顶层 subsystem**。

正确关系：

```text
baga.ui
  ↓
Baga UI implementation
  ↓
KOReader UIManager/widgets
  ↓
Kindle Adapter: Display/Input
```

```text
baga.reader
  ↓
Baga Reader implementation
  ↓
KOReader ReaderUI/CREngine/MuPDF
  ↓
Kindle Adapter: Display/Input/Storage/Lifecycle
```

### KPM / MRPI / sh_integration / Hotfix

这些主要属于：

```text
Platform native install/update
Homebrew foundation
Home Entry/bootstrap
```

不是 Display/Input/Power 等 Device Adapter Contract。

### KindleTool

属于：

```text
CI / build / package tooling
```

### WinterBreak / SpringBreak / Sanctuary / Véra

属于：

```text
Baga Ink Client Installation Route DB
```

不是 Adapter。

### Mesquito

不作为 Baga Kindle Adapter 直接依赖；如果某 jailbreak route 内部使用它，只是 upstream implementation detail。

---

# 4. Kindle Adapter Factory

Kindle Platform SHOULD 提供：

```text
KindleAdapterFactory
├── probe(BootstrapDeviceInfo)
└── create(...)
```

`probe()` 目标不是做 jailbreak 选择，而是识别 Platform 已能运行后的设备事实，例如：

```text
Kindle family/model
firmware version
CPU / ABI/native target hints
screen identity
available input class
known device profile
```

Installation Route Resolver 属于 Baga Ink Client，不属于 `KindleAdapterFactory.probe()`。

Factory MUST：

- 对未知 model / firmware 保守处理；
- 不用“同系列大概一样”替代验证；
- 选择匹配的 Device Profile；
- 选择必要 Quirk Set；
- 生成可诊断 ProbeResult。

---

# 5. Kindle DeviceDescriptor

最小逻辑描述：

```text
adapter_contract_version
adapter_id = org.baga.adapter.kindle
adapter_version

device_family = kindle
manufacturer = Amazon
model
model_id
firmware_version

cpu_arch
native_target

screen
input_summary
profile_id
quirk_set_id
compatibility_record_id
```

默认不把 Kindle serial / Amazon account 暴露给 App 或普通 Client handshake。

---

# 6. Native Build Target、Device Profile、Quirk 必须分开

## 6.1 Native Build Target / ABI Profile

回答：

> Native binary 怎么构建？

Reference engineering mapping：

| Kindle 工程族 | Native target | 含义 |
|---|---|---|
| K2 / K3 / DXG 等 legacy | `kindle-legacy` | 旧 ABI / 低资源 |
| K4 / Touch / PW1 等 classic | `kindle` | classic environment |
| PW2+ soft-float 路径 | `kindlepw2` | PW2+ soft-float |
| hard-float 路径 | `kindlehf` | hard-float |

当前 Reference baseline 继续把 firmware `5.16.3` 视为重要 soft-float / hard-float 工程边界；最终仍由 build/test evidence 确认。

## 6.2 Device Profile

回答：

> 某 model + firmware 组合已知什么？

推荐记录：

```text
profile_id
model / model_id match
firmware range
native_target
screen expectations
input expectations
baseline capability expectations
preferred display backend
preferred input backend
frontlight/audio/bluetooth expectations
validation status
last verified date
```

Profile 是 Adapter 的数据，不是 LifeBook 分支。

## 6.3 Quirk Set

回答：

> 这个精确组合需要哪些修正？

典型：

```text
touch coordinate correction
refresh workaround
frontlight behavior
sleep event workaround
network workaround
library bridge difference
```

Quirk MUST 带匹配范围和测试证据，并保持在 Adapter 内。

---

# 7. Capability Detection

Kindle Adapter MUST 以实际 backend/device evidence 生成 `CapabilitySnapshot`。

Base：

```text
display.basic
input.navigation
storage.app_sandbox
power.sleep_wake
platform.lifecycle
```

可选示例：

```text
display.partial_refresh
display.fast_refresh
display.quality_refresh
display.grayscale
display.color
input.touch
input.physical_page_key
input.keyboard
input.pen*
network.available
network.wifi
network.http
network.https
light.frontlight*
audio.output
bluetooth.*
storage.user_library
```

Capability 来源优先级：

```text
runtime probe / verified backend
        >
verified Device Profile
        >
marketing/spec assumptions
```

营销规格或同系列推断不能单独作为 Stable Capability 证据。

---

# 8. DisplayAdapter：优先包装 KOReader / FBInk

Kindle DisplayAdapter MUST 实现 `07 DisplayAdapter Contract`。

逻辑链：

```text
Platform refresh request
        ↓
Kindle DisplayAdapter
        ↓
KOReader / FBInk / verified Kindle mechanism
        ↓
Kindle display
```

App / UI 只表达：

```text
AUTO
TEXT
QUALITY
FAST
ANIMATION
```

Adapter 内部可映射到 Kindle 实际可用的 waveform / refresh mechanism。

禁止把：

```text
DU
GC16
A2
REGAL
raw waveform id
```

作为 Baga App contract。

DisplayAdapter SHOULD 尽量复用 KOReader 已有的：

```text
device detection
screen geometry
orientation
refresh behavior knowledge
```

FBInk MAY 用于补足或提供更稳定的 framebuffer/refresh mechanism；是否使用由具体 target/profile 验证决定。

Kindle Adapter 不应为了满足 Contract 重写一套新的 framebuffer framework。

---

# 9. InputAdapter：优先包装 KOReader Kindle input

逻辑链：

```text
Kindle raw touch/key/input
        ↓
KOReader / verified Kindle input knowledge
        ↓
Kindle InputAdapter
        ↓
Baga NavigationAction / PointerEvent / PenEvent
        ↓
Platform Core
```

必须归一化：

```text
confirm
back
page_next
page_previous
focus_next
focus_previous
```

`menu` 在存在可靠系统/设备语义时映射；否则由上层 UI 提供等价入口。

Touch、D-pad、Keyboard、物理翻页键、Pen 均保持设备内实现，IKP 不看到 raw keycode/event object。

---

# 10. StorageAdapter：Kindle 文件系统 + Baga sandbox

Kindle 缺少现代 Android 式 per-App OS sandbox。

因此 Kindle Adapter / Platform MUST 共同提供：

```text
platform private root
app private root
path containment
canonical path checking
symlink escape defense
disk-full / IO error mapping
package/data separation
```

推荐逻辑：

```text
/mnt/us/baga/
├── platform/
├── apps/
│   └── <app-id>/
│      ├── releases/
│      └── data/
├── staging/
└── ...
```

精确目录可以调整，但语义必须符合 IKP Update/Rollback Standard。

SQLite `lsqlite3` 继续通过 sandbox-aware VFS / 等价 I/O confinement 处理 ATTACH、journal、WAL、SHM、temp DB 等边界；它不是 StorageAdapter 自己重新发明的数据库 API。

---

# 11. LifecycleAdapter

优先复用 Kindle OS、KOReader、Homebrew 已验证的事件机制。

目标是稳定得到：

```text
sleep
wake
```

并支持 Platform 形成：

```text
start
resume
pause
sleep
wake
stop
```

要求：

- 不通过 App 高频轮询；
- Adapter callback 先进入 Platform Core；
- wake 后允许 Platform 重新检查 network/power/device state；
- firmware-specific event workaround 放进 Quirk Set。

---

# 12. PowerAdapter

Kindle PowerAdapter SHOULD 优先包装现有可靠 Kindle/KOReader/Homebrew mechanism。

Base 必须满足：

```text
power.sleep_wake
```

按实际能力再声明：

```text
power.battery_level
power.charging_state
power.keep_awake
```

`keep_awake` MUST 可被 Platform policy 拒绝。

不得为了 Baga 重新实现独立 power daemon，除非真实 PoC 证明现有机制无法满足 Contract。

---

# 13. NetworkAdapter

Kindle NetworkAdapter 的首要任务是：

```text
connectivity state
sleep/wake disruption mapping
network change events
necessary Kindle network bridge
```

Baga 不要求 Kindle Adapter 自己重新实现 HTTP/TLS。

可以：

```text
Platform shared HTTP/TLS stack
+
Kindle network/connectivity bridge
```

最终只要 `baga.network` 与 BICTS 成立。

LifeBook sync policy、Automerge sync protocol 不属于 NetworkAdapter。

---

# 14. Light / Audio / Bluetooth

## Frontlight

如果可通过成熟 Kindle mechanism 稳定控制：

```text
light.frontlight
light.frontlight.temperature
```

按实测声明。

## Audio / Bluetooth

不同 Kindle 差异很大。

只在真实实现并通过 Contract Tests / BICTS 后声明：

```text
audio.output
audio.microphone
bluetooth.available
bluetooth.input_device
bluetooth.audio
```

不能按“较新 Kindle 通常有”推断。

---

# 15. UserLibraryBridge

Kindle 现有用户书籍通过：

```text
Kindle filesystem / library knowledge
        ↓
Kindle UserLibraryBridge
        ↓
Platform baga.library
        ↓
IKP
```

规则：

- IKP 不扫描 `/documents`；
- IKP 不读取 Kindle 私有数据库；
- Library Item 使用 opaque ID / handle；
- `library.read/write` Permission 生效；
- source handle 可以交给 `baga.reader`；
- Bridge 不等于 Reader engine。

第一阶段如果 Kindle 私有书库数据库兼容性风险过高，可以先从已验证文件源建立保守 Bridge，再逐步增强；不得为了“功能齐全”牺牲用户数据安全。

---

# 16. UI / Reader：复用 KOReader，但不放进 Device Adapter 根契约

Kindle Platform SHOULD 最大化复用：

```text
UIManager / widgets
ReaderUI
CREngine
MuPDF
Annotation / Highlight / Bookmark
position / search / selection / anchor
```

但正确分层是：

```text
Platform UI / Reader implementation
        ↓
uses
        ↓
Kindle Device Adapter
```

而不是：

```text
Kindle Device Adapter
└── entire UI / Reader framework
```

LifeBook IKP 仍不得直接：

```lua
require("ui/uimanager")
require("apps/reader/readerui")
```

KOReader private API 只存在于 Kindle Platform implementation 内。

---

# 17. pinned KOReader / koreader-base

Reference Kindle Platform 第一版 MUST 管理自己的 pinned component set。

禁止默认依赖：

```text
用户 /mnt/us/koreader/
nightly
userpatch
第三方 plugin
用户自行升级后的 private API
```

每个 Platform Release MUST 记录：

```text
KOReader version/commit
koreader-base version/commit
FBInk version/commit（若使用）
patch set
license
source digest
native target
BICTS / Contract Test result
```

Adapter 只是调用这些成熟能力，不把 KOReader 变成标准依赖。

---

# 18. Homebrew / Install 组件与 Adapter 的最终边界

| 组件 | Kindle 中的定位 | Device Adapter? |
|---|---|---:|
| KOReader device knowledge | Display/Input/device implementation source | **Yes, 可被 Adapter 复用** |
| FBInk | Display implementation source | **Yes, 可被 Adapter 复用** |
| Kindle OS mechanisms | Lifecycle/Power/Network/Light 等实现来源 | **Yes, 可被 Adapter 包装** |
| KOReader UIManager/widgets | Platform UI implementation | No |
| ReaderUI/CREngine/MuPDF | Platform Reader implementation | No |
| KPM | Platform native install/update | No |
| MRPI | legacy/bootstrap installer envelope | No |
| sh_integration | Home Entry/bootstrap integration | No |
| Hotfix | Homebrew foundation | No |
| KindleTool | build/package tooling | No |
| KUAL / PEKI | legacy/admin/bootstrap fallback | No |
| WinterBreak/SpringBreak/Sanctuary/Véra | Client Installation Route | No |
| Mesquito | upstream route detail | No |

这张表是 Kindle 代码组织时的硬边界参考。

---

# 19. Kindle Adapter Self-test

`QUICK` SHOULD 验证：

```text
model / firmware resolved
device profile selected
native target consistent
quirk set selected
DisplayAdapter initialized
InputAdapter initialized
Storage root contained
Lifecycle hooks registered
Power sleep/wake integration available
Capability/subsystem consistency
backend version metadata readable
```

`INTERACTIVE` MAY 验证：

```text
visible refresh
page keys
confirm/back
touch
frontlight
pen
```

Self-test 不修改用户书籍/笔记。

---

# 20. Kindle Adapter Contract Tests

至少覆盖：

```text
KINDLE-ADAPTER-001 factory probe exact model/firmware behavior
KINDLE-ADAPTER-002 descriptor completeness
KINDLE-ADAPTER-003 unknown firmware is conservative
KINDLE-ADAPTER-004 base capability consistency
KINDLE-DISPLAY-001 screen geometry valid
KINDLE-DISPLAY-002 TEXT/QUALITY refresh safe
KINDLE-DISPLAY-003 region bounds safe
KINDLE-INPUT-001 navigation action normalization
KINDLE-INPUT-002 raw keycode does not leak
KINDLE-STORAGE-001 app root containment
KINDLE-STORAGE-002 symlink/path escape rejected
KINDLE-LIFECYCLE-001 sleep/wake mapping
KINDLE-POWER-001 sleep/wake available
KINDLE-PROFILE-001 target/profile/quirk separation
KINDLE-QUIRK-001 quirk only applies to declared range
KINDLE-ERROR-001 backend errors normalize
```

Optional capabilities 加对应 tests。

Adapter Contract Tests PASS 后，还必须运行整机 BICTS。

---

# 21. Compatibility Record

正式 Kindle Compatibility 绑定：

```text
Device Model
+ exact Firmware / tested range
+ Homebrew foundation state
+ Native Build Target
+ Device Profile version
+ Quirk Set version
+ Baga Platform version
+ Kindle Adapter version
+ Adapter Contract version
+ Lua Profile version
+ adopted component versions/commits
+ BICTS version/result
```

状态：

```text
Compatible
Experimental
Unsupported
```

未知 firmware 默认不能自动继承 Stable 认证。

---

# 22. Kindle 第一阶段实现优先级

第一份 Kindle Adapter 不需要一次覆盖所有历史机型。

建议顺序：

```text
1. 选择一个已 Homebrew-ready 的代表性 kindlehf 设备
2. 实现 Base Mandatory Adapter Contract
   - Identity
   - Capability
   - Display
   - Input
   - Storage
   - Lifecycle
   - Power
3. 最大化复用 pinned KOReader / FBInk / Kindle mechanisms
4. 通过 Adapter Contract Tests
5. 运行 Baga Probe IKP
6. 通过 Base BICTS
7. 再增加 network / light / library 等 optional subsystem
8. 再扩展 kindlepw2 / classic / legacy targets
```

设备覆盖通过 Device Profile / Quirk / build target 扩展，不通过复制 LifeBook 或 Platform shared code 扩展。

---

# 23. 与 Kindle Implementation Freeze 的关系

`reference-apps/03` 已冻结：

```text
Client
→ jailbreak/bootstrap
→ Homebrew foundation
→ KPM/MRPI native Platform install
→ Baga Platform
→ IKP Package Manager
→ lifebook.ikp
→ Home Entry
```

本文只负责其中：

> **Baga Platform 已经运行后，Kindle 硬件/OS/固件能力如何满足 Device Adapter Contract。**

因此：

```text
Installation Route DB ≠ Device Profile
KPM capability ≠ Device Capability Registry
Native installer envelope ≠ Device Adapter
Home Entry ≠ InputAdapter
```

这些概念不得混用。

---

# 24. 最终原则

> **Kindle 是 Baga Device Adapter Contract 的第一份 Reference Port，而不是 Baga 为 Kindle 重写的一套驱动系统。**

理想实现结果：

```text
Baga Kindle Adapter
≈ 薄 mapping / normalization glue
+ Device Profiles
+ Quirks
+ Contract Tests
```

下层站在：

```text
KOReader
koreader-base
FBInk
Kindle OS
validated Homebrew ecosystem
```

之上。

只要 `07 Contract`、Capability 与 BICTS 成立，未来内部替换某个 Kindle backend 不应要求修改 `lifebook.ikp` 或公开 `baga.*` Contract。
