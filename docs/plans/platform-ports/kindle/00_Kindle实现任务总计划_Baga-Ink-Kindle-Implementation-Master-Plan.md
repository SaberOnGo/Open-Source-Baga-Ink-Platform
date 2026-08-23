# Baga Ink Kindle 实现任务总计划 / Baga Ink Kindle Implementation Master Plan

> **文档级别：Implementation Plan / 平台移植实施总计划**  
> **状态：Plan Baseline v0.1**  
> **日期：2026-08-23**  
> **适用范围：Baga Ink Platform on Kindle、Kindle Device Adapter、Kindle Platform packaging/Home Entry、Baga Ink Client Kindle installation flow**  
> **首个目标设备：Homebrew-ready `kindlehf`，优先 firmware >= 5.16.3 的代表设备**

---

## 0. 文档定位

本文不是新的 Standard，也不是新的 Architecture Freeze。

它只回答：

> **在现有 Standards / Approved Design / Kindle Architecture Freeze 已经确定的边界内，Kindle Reference Port 接下来按什么工程顺序实现、验证和扩展。**

权威优先级：

```text
docs/standards/*
        >
docs/reference-apps/03 Kindle Implementation Architecture Freeze
        >
docs/design/*
        >
本 Implementation Plan
        >
具体 Task / Prototype / Code
```

如果实施中发现必须改变已经冻结的边界，MUST 先修改对应 Standard / Design / Architecture Freeze，再修改本计划与代码；不得用 Task 文档静默改变架构。

主要上位依据：

```text
docs/standards/07_设备适配器规范_Baga-Ink-Device-Adapter-Specification.md
docs/standards/11_Kindle适配规范_Baga-Ink-Kindle-Adapter.md
docs/design/02_设备适配器可执行契约与SDK设计_Baga-Ink-Device-Adapter-Executable-Contract-and-SDK-Design.md
docs/reference-apps/03_Kindle具体实现架构冻结_Baga-Ink-Kindle-Implementation-Architecture-Freeze.md
```

---

# 1. 为什么放在 `docs/plans/platform-ports/kindle/`

仓库已经定义：

```text
docs/standards/       → Baga Ink 必须是什么
docs/design/          → 子系统准备怎样实现、为什么
docs/plans/           → 已确认设计按什么工程顺序落地
docs/status/          → 当前真正做到哪里
docs/reference-apps/  → Reference App / LifeBook 如何验证平台及相关冻结
```

因此 Kindle 的**任务规划**不应进入：

```text
docs/standards/
docs/design/
docs/reference-apps/
```

也不需要在仓库根目录再创建一个与 `docs/` 平级的 `tasks/` 或 `roadmap/`。

但 Kindle 只是未来众多设备/OS 家族中的第一个完整 Platform Port，且 Kindle 自身后续会有大量任务，因此不能继续把所有计划平铺在 `docs/plans/` 根目录。

本计划采用：

```text
docs/
└── plans/
    ├── 01_规范可执行化实施计划_...md
    │
    └── platform-ports/
        ├── kindle/
        │   ├── 00_Kindle实现任务总计划_Baga-Ink-Kindle-Implementation-Master-Plan.md
        │   ├── K0_adapter-contract/          # 后续按需要创建
        │   ├── K1_koreader-bringup/          # 后续按需要创建
        │   ├── K2_kindle-adapter/            # 后续按需要创建
        │   ├── K3_minimal-platform/          # 后续按需要创建
        │   ├── K4_ikp-package-manager/       # 后续按需要创建
        │   ├── K5_reader-integration/        # 后续按需要创建
        │   ├── K6_packaging-home-entry/      # 后续按需要创建
        │   └── K7_client-bootstrap/          # 后续按需要创建
        │
        ├── android-e-paper/                  # future
        ├── remarkable/                       # future, if adopted
        └── other-device-family/              # future
```

这里使用 `platform-ports`，而不是 `device-adapters`，因为 Kindle 实现范围明显大于 Device Adapter：

```text
Kindle complete port
├── native Platform build
├── Kindle Device Adapter
├── pinned KOReader / koreader-base / FBInk integration
├── IKP execution
├── KPM / MRPI native packaging
├── Home Entry
├── Compatibility / BICTS
└── Baga Ink Client bootstrap / route resolution
```

Device Adapter 只是其中一个子系统。

---

# 2. Task 文档组织规则

本文件是 Kindle Port 的**长期总计划**。

后续只有当某个 Milestone 真正进入施工时，才在对应目录创建细分 Task 文档；Git 不保留空目录，因此不提前创建一堆空文件夹。

示例：

```text
docs/plans/platform-ports/kindle/K1_koreader-bringup/
├── 00_K1里程碑计划_KOReader-Bringup.md
├── 01_锁定上游组件与依赖清单_Pin-Upstream-Components.md
├── 02_kindlehf构建验证_KindleHF-Build-Bringup.md
└── 03_Baga直接入口PoC_Baga-Direct-Entry-PoC.md
```

Task 文件 SHOULD 包含：

```text
Goal
Authority / Inputs
Dependencies
Files to create/modify
Implementation steps
Tests
Device evidence
Acceptance gate
Out of scope
Risks / rollback
Result / evidence links
```

Task 完成后：

- Task 文件 MAY 保留为实施历史；
- 当前进度 MUST 回写 `docs/status/00_当前项目状态_Baga-Ink-Project-Status.md`；
- 不能让“现在做到哪里”只能从 Task checkbox、Branch 或聊天记录推断。

---

# 3. 总体目标与第一条真实设备链

第一阶段不从完整 LifeBook 业务开始，也不先做自动越狱 Client。

第一条必须跑通的真实链只有：

```text
Homebrew-ready real Kindle (`kindlehf` first)
        ↓
baga-launch / development entry
        ↓
Baga Ink Platform Core
        ↓
Kindle Device Adapter
        ↓
baga-probe.ikp
        ↓
UI visible + input works
        ↓
sleep / wake
        ↓
state remains valid
```

第一份真实 App 应是：

```text
baga-probe.ikp
```

而不是完整 LifeBook。

建议 Probe 页面只验证：

```text
Platform version
Adapter version
Model / firmware / native target
Base capabilities
Display
Input
Storage
Lifecycle
Power
simple persisted counter
```

成功标准示例：

```text
Counter: 1
[ +1 ]
   ↓
Counter: 2
   ↓
sleep
   ↓
wake
   ↓
Counter remains 2
```

这条链一旦在真实 Kindle 上稳定跑通，Baga Ink Platform 才第一次从“规范/架构项目”进入真实设备实现阶段。

---

# 4. 第一台 Bring-up 设备

第一台开发设备 SHOULD 是：

```text
already jailbroken
+
Homebrew-ready
+
firmware >= 5.16.3
+
kindlehf
```

原因：第一阶段不要同时调试：

```text
legacy ABI
+ jailbreak route
+ KPM bootstrap
+ Platform Core
+ KOReader integration
+ Device Adapter
+ IKP
+ LifeBook
```

当前 Kindle Reference engineering target 保持：

```text
kindle-legacy
kindle
kindlepw2
kindlehf
```

首个 `kindlehf` 跑通以后，再按 Compatibility evidence 扩展：

```text
kindlepw2
→ kindle
→ kindle-legacy
```

不得因为同系列相似就直接继承 Compatible 结论。

---

# 5. 第一阶段明确不做什么

Bring-up 阶段先不做：

```text
自动 jailbreak
完整 Baga Ink Client route automation
完整 LifeBook
AI
Sync / Automerge sync protocol
Market
Audio
Bluetooth
Pen
全部历史 Kindle 型号
深度 AppMgr integration
完整 native installer fallback matrix
```

先人为准备一台 Homebrew-ready Kindle。

理由：

```text
jailbreak/bootstrap
```

解决的是：

> Kindle 如何达到 Platform 可以被安装/运行的状态。

而：

```text
Baga Platform + Kindle Adapter + IKP
```

解决的是：

> Platform 本身能否正确工作。

这两个问题必须先解耦。

---

# 6. 目标代码目录（实施时按现有 Design 微调）

当前 Approved Design 已给出机器 Contract / SDK / Adapter 的基础目录。Kindle Port 实施 SHOULD 逐步形成：

```text
spec/
└── adapter/
    ├── contract.yaml
    ├── types.yaml
    ├── descriptor.yaml
    ├── events.yaml
    ├── errors.yaml
    ├── subsystems/
    └── frozen/

sdk/
└── adapter/
    ├── generated/
    ├── mock/
    └── README.md

tools/
└── baga-adapter-codegen/

tests/
├── adapter_contract/
└── adapter_mock/

platform/
├── core/
├── lua/
├── adapters/
│   ├── mock/
│   └── kindle/
│       ├── common/
│       ├── display/
│       ├── input/
│       ├── storage/
│       ├── lifecycle/
│       ├── power/
│       ├── network/
│       ├── light/
│       ├── library/
│       ├── device_profiles/
│       ├── quirks/
│       └── build_targets/
└── vendor/ or components/
    ├── koreader/
    └── fbink/

apps/
├── probe/
└── lifebook/                 # later

client/
└── kindle/                   # K7, later
```

约束：

- `platform/adapters/kindle/` MUST 保持 Device Adapter 边界；
- ReaderUI / UIManager / KPM / MRPI / jailbreak routes 不得因为与 Kindle 有关就塞入 Adapter；
- pinned KOReader / koreader-base 是 Platform internal adopted components，不是 IKP API；
- `lifebook.ikp` 不得直接 import KOReader / Kindle private API。

---

# 7. Milestone 总览

原始规划使用 `K0` 到 `K7` 编号。该编号实际包含 **8 个 Milestone**；本文保留 K0–K7，不重新编号，避免后续 Task/Commit/Issue 引用混乱。

| Milestone | 目标 | 主要验收 |
|---|---|---|
| **K0** | Adapter Contract 机器化基础 | Base Contract + generated interface + Mock/Test foundation 可执行 |
| **K1** | pinned KOReader KindleHF Bring-up | Kindle 上可从 Baga entry 进入受控 Platform bootstrap，不暴露 KOReader 产品 UI |
| **K2** | Kindle Base Device Adapter | Display/Input/Storage/Lifecycle/Power 等 Base Contract 通过 Adapter tests |
| **K3** | Minimal Platform Core + Probe IKP | 真正 `.ikp` 可启动、交互、持久化并经历 sleep/wake |
| **K4** | IKP stage/activate + device verifier | 签名验证、staging、atomic activation、rollback 基础链成立 |
| **K5** | `baga.reader` → KOReader reader stack | EPUB/PDF 等阅读能力通过 Baga API 进入 ReaderUI/CREngine/MuPDF |
| **K6** | KPM/native package + Home Entry | `baga-platform*.kpkg` 可安装，Kindle Home 可进入 LifeBook/Probe，不暴露底层工具 |
| **K7** | Baga Ink Client + Route DB + bootstrap automation | Client 可检测精确状态、选择 route、确保 Platform、传输/安装 IKP |

---

# 8. K0 — Adapter Contract 可执行基础

## Goal

把 `07 Device Adapter Contract` 的 Base Mandatory surface 变成机器可读、可生成、可测试的最小闭环。

Base Mandatory：

```text
Identity / Descriptor
Capability Snapshot
Display
Input
Storage
Lifecycle
Power
```

对应 Base Compatibility：

```text
display.basic
input.navigation
storage.app_sandbox
power.sleep_wake
platform.lifecycle
```

## K0 Tasks

```text
K0-01  建立 `spec/adapter/` IDL schema / loader
K0-02  固化 Root + Descriptor + Capability + Error + Event core types
K0-03  固化 Base subsystem IDL：Display/Input/Storage/Lifecycle/Power
K0-04  freeze `spec/adapter/frozen/v0.1/`
K0-05  生成第一份 Reference interface
K0-06  实现 Mock / Headless Adapter
K0-07  建立 Adapter Contract Test harness
K0-08  加入 IDL compatibility / reproducibility CI
```

## Lua 注意事项

Kindle 内部大量复用 KOReader Lua/LuaJIT，因此可以实验：

```text
Kindle-specific Lua binding/stub
```

但必须区分：

```text
General Adapter SDK generated contract
        ≠
Kindle Platform internal Lua binding
```

当前 Approved Design 已明确 Rust/C/Kotlin generated interface 方向；如果未来要把 Lua 正式提升为通用 generated SDK target，SHOULD 先更新 `docs/design/02`，而不是只在 Kindle Task 中静默扩大 SDK contract。

## K0 Gate

- Machine IDL 能表达 Base Contract；
- Frozen snapshot 可比较；
- Generated output 可重复；
- Mock Adapter 通过 Base Adapter Contract Tests；
- error/event semantics 与 `07` 一致；
- 不引入 RPC/daemon/JSON bridge 新架构层。

---

# 9. K1 — pinned KOReader / KindleHF Bring-up

## Goal

先证明：

> **Baga 可以在一台真实 `kindlehf` 上复用 pinned KOReader/koreader-base 的成熟 Kindle substrate，进入 Baga 自己的受控启动路径。**

此阶段还不要求完整 IKP Package Manager。

## K1 Tasks

```text
K1-01  选择并锁定 KOReader / koreader-base / FBInk reference commits
K1-02  建立 dependency/license/source-digest manifest
K1-03  验证 `kindlehf` native build / launch baseline
K1-04  建立最小 `baga-launch` development entry
K1-05  实验 Baga Platform private entry technique
K1-06  建立 Platform bootstrap diagnostics / crash log
K1-07  在真实 Kindle 上验证 cold start / exit / relaunch
```

## Baga Entry PoC

Architecture Freeze 允许 `.koplugin` 作为 Platform-private PoC，但没有冻结它必须成为最终方案。

因此 K1 MUST 做证据比较，而不是先把某一种技术写成公共架构：

### Candidate A — direct Baga entry

例如 pinned private KOReader 上增加内部参数：

```text
--baga-app <app-id>
```

概念链：

```text
KOReader bootstrap
→ setup environment / device / screen / input / UI foundation
→ detect Baga private entry
→ baga/bootstrap.lua
→ Platform bootstrap
```

### Candidate B — Platform-private `.koplugin`

```text
baga-launch
→ pinned KOReader substrate
→ private baga.koplugin
→ Platform bootstrap
```

## 选择标准

最终采用哪个 SHOULD 由 PoC 证据决定：

```text
startup determinism
no FileManager flash/exposure
lifecycle correctness
crash recovery
upgrade/patch maintenance cost
ability to keep KOReader private from IKP
```

无论采用哪一种，都必须保持：

```text
implementation technique only
≠ public Baga architecture
≠ IKP API
```

## K1 Gate

真实 `kindlehf` 上能够：

```text
launch Baga-controlled entry
→ initialize pinned Kindle substrate
→ display a Baga-owned test surface
→ receive at least one normalized input path
→ clean exit / relaunch
```

普通用户路径不得要求进入 KOReader FileManager / Plugin Menu。

---

# 10. K2 — Kindle Base Device Adapter

## Goal

实现一份**薄 Kindle Reference Adapter**，最大化包装已有成熟能力，而不是重新实现 Kindle stack。

## K2 Tasks

```text
K2-01  KindleAdapterFactory + conservative probe
K2-02  DeviceDescriptor + exact model/firmware/native-target evidence
K2-03  Device Profile selection
K2-04  Quirk Set selection
K2-05  Capability detection
K2-06  DisplayAdapter → KOReader/FBInk/verified mechanism
K2-07  InputAdapter → KOReader Kindle input knowledge
K2-08  StorageAdapter → Kindle filesystem + Baga containment hooks
K2-09  LifecycleAdapter → Kindle/KOReader/Homebrew events
K2-10  PowerAdapter → validated Kindle mechanisms
K2-11  Error/event normalization
K2-12  QUICK/INTERACTIVE self-test
K2-13  Kindle Adapter Contract Tests
```

禁止优先重写：

```text
framebuffer stack
evdev/input stack
reader engine
network stack
power daemon
```

## K2 Gate

至少满足 `docs/standards/11` 的 Base Adapter tests：

```text
factory exact probe
descriptor completeness
unknown firmware conservative behavior
base capability consistency
display geometry / safe refresh
navigation normalization
storage containment
sleep/wake mapping
power.sleep_wake
profile/quirk separation
backend error normalization
```

通过 Adapter Contract Tests **不等于**可以宣称 Baga Ink Compatible；整机仍需 BICTS。

---

# 11. K3 — Minimal Platform Core + `baga-probe.ikp`

## Goal

第一次运行一个真正的 `.ikp`。

Platform Core v0.0.1 只实现 Probe 所需最小职责：

```text
App Registry
App Context
Embedded Lua Host
Lifecycle dispatch
Adapter dispatch
Permission/Sandbox skeleton

baga.app
baga.device
baga.storage
baga.log
minimal baga.ui
```

暂时不做：

```text
AI
Sync
Market
Automerge sync
Bluetooth
Audio
Pen
full reader
```

## K3 Tasks

```text
K3-01  minimal Platform bootstrap / App Registry
K3-02  App Context + lifecycle dispatcher
K3-03  Embedded Lua Host / Baga Lua Profile minimum
K3-04  `baga.app` / `baga.device` / `baga.storage` / `baga.log`
K3-05  minimal `baga.ui` Kindle backend
K3-06  developer-mode local IKP loading path
K3-07  build `baga-probe.ikp`
K3-08  persistent counter / storage test
K3-09  sleep/wake lifecycle test
K3-10  Base BICTS subset on real device
```

## K3 Gate — 第一条关键验收链

```text
real Kindle
   ↓
baga-launch
   ↓
Baga Platform
   ↓
baga-probe.ikp
   ↓
visible UI
   ↓
input works
   ↓
write state
   ↓
sleep / wake
   ↓
state remains valid
```

这是 Kindle Port 的第一个重大里程碑。

---

# 12. K4 — IKP stage / activate + device verifier

## Goal

从“开发模式能加载 Probe”升级为真正符合 IKP / Signing / Update Standards 的设备端 App 安装链。

现有 `21–28` executable specification / verifier 工作是上游依赖；K4 MUST 复用其稳定 canonicalization、signature、IKP validation 结果，不在 Kindle 端重新发明第二套算法。

## K4 Tasks

```text
K4-01  IKP package reader / strict validation integration
K4-02  device signature verifier integration
K4-03  staging layout
K4-04  immutable release layout
K4-05  App data / package separation
K4-06  atomic activation pointer/state
K4-07  health/probation result
K4-08  rollback to last-known-good
K4-09  corrupted / unsigned / wrong-hash negative tests
K4-10  install/update/rollback BICTS subset
```

## K4 Gate

- invalid IKP cannot activate；
- verified IKP stages before activation；
- activation is atomic/recoverable；
- rollback does not delete App data；
- Kindle verifier and Reference verifier agree on shared vectors；
- Platform update 与 IKP App update 仍是两个不同事务。

---

# 13. K5 — `baga.reader` → KOReader Reader stack

## Goal

Probe 成功以后再接 Reader；不重新写自己的 EPUB/PDF 阅读器。

逻辑链：

```text
IKP
 ↓
baga.reader
 ↓
Platform Reader implementation
 ↓
ReaderUI / CREngine / MuPDF
 ↓
Kindle Adapter Display/Input/Storage/Lifecycle
```

## K5 Tasks

```text
K5-01  define minimal internal Reader bridge
K5-02  opaque source handle → Reader open
K5-03  EPUB / TXT bring-up via CREngine
K5-04  PDF bring-up via MuPDF
K5-05  page/position/search/selection mapping
K5-06  bookmark/highlight/annotation mapping as required
K5-07  suspend/resume + position persistence
K5-08  reader BICTS / regression tests
```

LifeBook IKP MUST NOT：

```lua
require("ui/uimanager")
require("apps/reader/readerui")
```

KOReader private API stays inside Kindle Platform implementation.

---

# 14. K6 — KPM/native packaging + Kindle Home Entry

## Goal

当开发 Kindle 上的 Platform/Probe 已稳定后，再把它包装成正常 Kindle Platform installation product flow。

## K6 Tasks

```text
K6-01  build `baga-platform_<version>_kindlehf.kpkg`
K6-02  install / launch / uninstall hooks
K6-03  package pinned component manifest
K6-04  Platform health check after install/update
K6-05  sh_integration Scriptlet Home Entry
K6-06  `Kindle Home → LifeBook/Probe → baga-launch <app-id>`
K6-07  update preserves Kindle books/notes/App data
K6-08  uninstall preserves user data according to policy
K6-09  validate MRPI/legacy envelope only where KPM is unavailable/unvalidated
K6-10  optional AppMgr Phase 2 research, not baseline blocker
```

冻结关系：

```text
KPM
→ native Baga Platform package manager

IKP Package Manager
→ Baga App package manager
```

永远不存在：

```text
lifebook.ikp → lifebook.kpkg
```

## K6 Gate

用户产品路径：

```text
Kindle Home
   ↓
LifeBook
```

内部才是：

```text
LifeBook Home Entry
→ baga-launch com.lifebook
→ Platform Core
→ active lifebook.ikp
```

普通用户不需要看见 KUAL / KOReader FileManager / KPM CLI / MRPI。

---

# 15. K7 — Baga Ink Client + Installation Route DB

## Goal

只有设备端 Platform 已经稳定，才自动化前面的 jailbreak/bootstrap/install/transfer 流程。

Client 内部必须拆成：

```text
A. Ensure Baga Platform
B. Transfer / Install IKP
```

## K7 Tasks

```text
K7-01  USB Kindle detection + model/firmware/current-state collection
K7-02  Installation Route DB schema
K7-03  exact route matching / ranking
K7-04  detect Homebrew foundation state
K7-05  distinguish KPM-compatible vs KPM-installed
K7-06  KPM bootstrap flow where compatible
K7-07  KPM-incompatible verified fallback envelope
K7-08  filesystem mailbox / handshake
K7-09  transfer signed IKP + evidence
K7-10  device-side re-verification and result outbox
K7-11  install/recovery/data-protection UX
K7-12  route regression matrix by exact model + firmware
```

Installation Route DB 可以记录：

```text
WinterBreak
SpringBreak
Sanctuary
Véra
legacy routes
future verified routes
```

但这些始终只是 Client installation routes，不进入 Platform Core / Device Adapter / IKP contract。

## K7 Gate

Client 可以对一条**精确已验证**的设备组合完成：

```text
Detect
→ determine current state
→ choose exact route if needed
→ reach Homebrew-ready
→ ensure correct Platform installer path
→ install/verify Platform
→ transfer/install IKP
→ verify final launch
```

未知 firmware 默认 Experimental / Unsupported，不猜测继承。

---

# 16. Milestone 依赖关系

主序列：

```text
K0
 ↓
K1
 ↓
K2
 ↓
K3
 ↓
K4
 ↓
K5
 ↓
K6
 ↓
K7
```

其中允许有限并行：

```text
K0 IDL/codegen/mock
      ↘
       K1 upstream pin/build research
```

但：

- K2 不得用 Kindle 私有 ad-hoc API 绕过尚未稳定的 Adapter Contract；
- K3 Probe 不得直接 import KOReader private API；
- K6 packaging 不应成为 K1–K3 bring-up 的前置阻塞；
- K7 jailbreak/client automation 不应成为设备端 Platform 正确性的前置条件。

---

# 17. `kindlehf` 成功后的扩展方式

不要复制 Platform/LifeBook 代码来支持新 Kindle。

正确扩展维度：

```text
Native Build Target
+
Device Profile
+
Quirk Set
+
Compatibility Record
```

建议扩展顺序：

```text
kindlehf representative device
        ↓
more kindlehf model/firmware combinations
        ↓
kindlepw2
        ↓
kindle
        ↓
kindle-legacy
```

每个新组合至少回归：

```text
Platform launch
Adapter Contract Tests
Probe
sleep/wake
storage/data protection
IKP install/update/rollback
UI/display/input
reader/library if claimed
network if claimed
Home Entry
BICTS
```

---

# 18. Completion / Compatibility Gate

不能因为代码“能跑”就宣称 Kindle Compatible。

正式 Compatibility Record 至少绑定：

```text
Device Model
Firmware exact/tested range
Homebrew foundation state
Native Build Target
Device Profile version
Quirk Set version
Baga Platform version
Kindle Adapter version
Adapter Contract version
Baga Lua Profile version
adopted component commits/digests
Adapter Contract Test result
BICTS version/result
```

状态只能是：

```text
Compatible
Experimental
Unsupported
```

---

# 19. 当前立即开工顺序

当前不应该直接开始 LifeBook 业务，也不应该开始自动 jailbreak Client。

立即执行顺序：

```text
1. K0-01 ~ K0-07
   → spec/adapter Base Contract
   → generated interface foundation
   → Mock Adapter
   → Contract Test harness

2. 并行准备 K1-01 ~ K1-03
   → pin KOReader/koreader-base/FBInk
   → dependency manifest
   → kindlehf build baseline

3. K1-04 ~ K1-07
   → baga-launch development entry
   → direct-entry vs private-koplugin PoC
   → real Kindle bootstrap evidence

4. K2
   → thin Kindle Base Adapter

5. K3
   → first real baga-probe.ikp
```

第一阶段真正的关键结果不是“安装器做出来”，而是：

> **一台真实 Kindle 上，Baga Platform 经标准 Device Adapter 启动一个真正的 Probe IKP，并在显示、输入、存储、睡眠/唤醒之后仍保持正确。**

---

# 20. 最终原则

Kindle 是 Baga Ink 的第一份 Reference Platform Port，但不是最终平台边界。

本计划长期坚持：

> **公共 Contract 稳定，具体 Adapter 尽量薄；最大化复用 KOReader、koreader-base、FBInk、Kindle OS/Homebrew 的成熟能力；先证明 Platform 本身，再做安装自动化；先用 Probe 验证平台，再让 LifeBook 成为真正的 Reference App。**

目录同样遵守这一原则：

```text
docs/plans/platform-ports/<device-family>/
```

让 Kindle、Android E-Paper 和未来设备家族共享同一种实施组织方式，而不把 Kindle 特例变成 Baga Ink Platform 的永久结构。