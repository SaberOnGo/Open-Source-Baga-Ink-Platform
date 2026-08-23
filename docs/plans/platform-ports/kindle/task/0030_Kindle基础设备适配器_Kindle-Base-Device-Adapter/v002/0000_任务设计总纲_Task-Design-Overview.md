# TASK-0030 v002 任务设计总纲 / Kindle Base Device Adapter Task Design

> **Task ID：`TASK-0030`**  
> **Version：`v002`**  
> **Milestone：K2 — Kindle Base Device Adapter**  
> **状态：Selected Planning Baseline — dependency-gated**  
> **日期：2026-08-23**

---

## 0. Goal

实现符合 Baga Device Adapter Contract 的薄 Kindle Reference Adapter，并固定第一阶段的实现语言与成熟组件接入方式，避免后续 AI 在每个 subsystem 开工时重新做语言选型。

核心实现链：

```text
KOReader / koreader-base / FBInk / Kindle OS / validated Homebrew
        ↓
thin Kindle-specific binding / normalization
        ↓
Baga Device Adapter Contract
        ↓
Platform Core
```

本 Task 的目标不是用某一种语言“重新实现 Kindle”，而是用最短、兼容性最高的路径包装已有成熟能力。

---

# 1. Authority / Dependencies

```text
docs/zh-CN/standards/07_设备适配器规范.md
docs/zh-CN/standards/11_Kindle适配规范.md
docs/zh-CN/reference-apps/03_Kindle具体实现架构冻结.md
docs/zh-CN/design/02_设备适配器可执行契约与SDK设计.md
docs/plans/platform-ports/kindle/0020_Kindle实现语言与绑定裁决_Kindle-Implementation-Language-and-Binding-Decision.md
TASK-0010 current selected design
TASK-0020 current selected design
```

Dependency Gate：

```text
K0 Base Contract baseline available
+
K1 pinned kindlehf substrate / direct-entry evidence available
```

Gate 未通过前只允许准备 fixtures、profiles、tests 和 backend research。

---

# 2. Contract Is Language-Neutral

固定裁决：

> **Device Adapter Contract 规定行为和语义，不规定源码语言。**

因此：

```text
generated Rust/C/Kotlin interfaces
```

是工具链支持，不是 Adapter 允许语言清单。

Kindle Reference Adapter 可以是混合实现。Contract Tests / BICTS 判断是否合格，而不是源码扩展名或语言名称。

---

# 3. Fixed Kindle Implementation Matrix

K2 第一阶段 MUST 使用以下默认矩阵。Execution Prompt 不得重新开展通用语言选型。

| Subsystem / Area | Default language / binding | Mature source | Implementation rule |
|---|---|---|---|
| Factory / probe | **Lua first** | KOReader device facts + verified OS facts | conservative detection；unknown firmware 不猜测 |
| DeviceDescriptor | **Lua first** | probe/profile data | 只归一化 Baga descriptor |
| Capability detection | **Lua first** | runtime evidence + profile | capability 由真实 backend 证据产生 |
| Device profiles | data + **Lua loader** | Baga verified records | model + firmware + native target 分开记录 |
| Quirk selection | data + **Lua glue** | real-device evidence | quirk 必须精确匹配并有测试 |
| Error/event normalization | **Lua first** | KOReader/OS callback | 转成 Baga stable semantics 后进入 Platform Core |
| DisplayAdapter | **Lua wrapper first** | KOReader screen/device knowledge | 不重写 framebuffer stack |
| FBInk display path | existing **C/native** implementation | FBInk | 只有 profile/backend 需要时通过现成或窄 binding 使用 |
| InputAdapter | **Lua wrapper** | KOReader Kindle input | 不重写 evdev/touch calibration |
| StorageAdapter policy | **Lua first** | Kindle filesystem + Platform policy | containment/canonical checks；成熟 native storage library 继续复用 |
| LifecycleAdapter | **Lua wrapper** | KOReader/Kindle/Homebrew events | firmware workaround 放 quirk |
| PowerAdapter | **Lua wrapper first** | KOReader/Kindle mechanisms | native only when proven necessary |
| Network device-state bridge | **Lua / existing Platform bridge** | Kindle connectivity mechanisms | 不重写 HTTP/TLS stack |
| Frontlight | **Lua wrapper first** | validated KOReader/Kindle mechanism | optional capability only after test |
| Self-test / diagnostics | **Lua first** | Adapter subsystem calls | QUICK/INTERACTIVE 统一报告 |

其他不属于 Adapter root 的实现保持各自成熟语言：

```text
FBInk
→ C

KOReader UIManager / ReaderUI
→ existing Lua/LuaJIT stack

IKP verifier / cryptography
→ existing verified Rust/C/native core
```

不为了“Kindle 主体用 Lua”而重写这些组件。

---

# 4. Why Lua First on Kindle

Lua first 不是因为 Lua 在所有指标上比 Rust/C 快，而是因为第一阶段要包装的大量成熟 Kindle 能力已经存在于 KOReader Lua/LuaJIT device environment：

```text
Device
Device.screen
Device.input
UIManager-related lifecycle knowledge
Kindle-specific model / firmware handling
```

因此常见正确链是：

```text
KOReader Lua-facing capability
        ↓
very thin Lua normalization
        ↓
Baga semantic object/event
```

而不是为了语言统一建立：

```text
Rust/C rewrite
→ FFI
→ duplicate Kindle knowledge
→ Baga
```

如果额外 native 层不能解决明确的兼容性、性能、安全或 ABI 问题，就不应增加。

---

# 5. Scope

`v002` 覆盖：

```text
KindleAdapterFactory
exact probe / DeviceDescriptor
Device Profile selection
Quirk Set selection
Capability detection
DisplayAdapter
InputAdapter
StorageAdapter
LifecycleAdapter
PowerAdapter
Base error/event normalization
QUICK / INTERACTIVE self-test
Adapter Contract Tests
kindlehf real-device verification
```

Base Compatibility：

```text
display.basic
input.navigation
storage.app_sandbox
power.sleep_wake
platform.lifecycle
```

---

# 6. Out of Scope

```text
重写 framebuffer stack
重写 evdev/input stack
重写 reader engine
重写 HTTP/TLS stack
新建 power daemon
完整 optional Audio/Bluetooth/Pen
LifeBook business logic
IKP verifier implementation
KPM packaging
Client jailbreak automation
为了统一语言进行大规模 Rust/C/Lua rewrite
```

---

# 7. Display Design

默认：

```text
Baga RefreshIntent
        ↓
Lua Kindle DisplayAdapter
        ↓
KOReader screen/device knowledge
        ↓
verified refresh backend
```

需要 FBInk 的 profile：

```text
Lua DisplayAdapter
        ↓
narrow existing binding / FFI
        ↓
FBInk C
```

禁止把 DU/GC16/A2/REGAL 等 raw waveform 变成 App contract。

只有真实 target/profile 证据证明某 backend 更稳定时才切换 backend；切换结果进入 Device Profile，而不是 execution prompt 临时判断。

---

# 8. Input Design

默认：

```text
Kindle raw input
        ↓
KOReader Kindle input knowledge
        ↓
Lua InputAdapter normalization
        ↓
Baga NavigationAction / PointerEvent
```

至少归一化：

```text
confirm
back
page_next
page_previous
focus_next
focus_previous
```

触摸坐标、物理键差异和 firmware workaround 进入 profile/quirk，不向 IKP 暴露 raw event。

---

# 9. Storage / Lifecycle / Power

Storage：

- Lua glue 负责 Baga path/policy orchestration；
- canonical path、symlink escape、disk-full、IO error 必须可验证；
- SQLite/文件系统成熟能力继续采用，不创造 `baga.data` 一类平行数据库抽象。

Lifecycle：

```text
KOReader / Kindle / Homebrew event
→ Lua LifecycleAdapter
→ Baga lifecycle event
→ Platform Core
```

Power：

- wrap existing verified mechanism；
- `power.sleep_wake` 为 Base；
- optional battery/charging/keep-awake 只有真实实现后声明；
- 不因为 native code 可能更快就创建新的 power manager。

---

# 10. Language Deviation Gate

只有以下 evidence 可以改变某 subsystem 的默认语言/backend：

```text
build/ABI failure
firmware API unavailable
repeatable crash
lifecycle correctness failure
measured memory/startup violation
profiling-proven performance bottleneck
security issue
upstream API relocation/removal
```

改变流程：

```text
collect evidence
→ update TASK-0030 to v003+
→ state new mapping and acceptance gate
→ generate matching execution-prompts
```

Execution Agent 不得在实现过程中静默从 Lua 改 Rust/C，或反向把成熟 C library 改写成 Lua。

---

# 11. Test Strategy

Host / Contract tests：

```text
factory exact probe
descriptor completeness
unknown firmware conservative behavior
capability consistency
display geometry / refresh intent mapping
navigation normalization
storage containment
lifecycle sleep/wake mapping
power.sleep_wake
profile/quirk separation
error/event normalization
self-test report shape
```

Real-device tests：

```text
kindlehf model + firmware recorded
real display refresh
real navigation/touch where available
sandbox read/write
sleep → wake
resume state
cold relaunch
no user-data damage
```

测试验证语义和设备行为，不把“全部由 Lua 实现”作为验收指标。

---

# 12. Debug / Recovery

诊断必须能输出：

```text
model / firmware / native target
profile_id / quirk_set_id
backend selection
subsystem implementation/binding identifier
capability evidence
raw backend error diagnostics
normalized Baga error
last lifecycle event
self-test result
```

真实 Kindle 调试不得修改用户书籍、笔记或账户数据；任何开发路径修改应可恢复。

---

# 13. Acceptance Gate

K2 完成至少要求：

- Base Adapter Contract tests 通过；
- `kindlehf` 上 Display/Input/Storage/Lifecycle/Power Base 路径有真实证据；
- Adapter 保持薄，未重写 KOReader/FBInk 已有成熟 stack；
- 实现符合本文固定语言/绑定矩阵；
- 没有为语言统一增加无必要 FFI；
- 每个 backend/profile/quirk 可诊断；
- 未经新 Task Version 不发生语言/backend 架构偏移。

通过 Adapter Contract Tests 不等于整机已获得 Baga Ink Compatible；最终兼容性仍由 BICTS 决定。

---

# 14. Expected Execution-Prompt Groups

```text
factory/probe
profile/quirk records
capability detector
Lua common normalization
display KOReader wrapper
optional FBInk narrow binding
input KOReader wrapper
storage containment
lifecycle/power wrappers
self-test
automated Contract Tests
kindlehf real-device validation
```

每份 Execution Prompt 必须引用 `Kindle Implementation Language and Binding Decision`，不得重新把语言选型作为开放任务。
