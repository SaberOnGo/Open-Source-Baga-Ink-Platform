# Kindle 实现语言与绑定裁决 / Kindle Implementation Language and Binding Decision

> **文档级别：Implementation Decision / Kindle 平台移植实施裁决**  
> **状态：Baseline v1.0**  
> **日期：2026-08-23**  
> **适用范围：Baga Ink Platform on Kindle、Kindle Device Adapter、KOReader/FBInk integration、K0–K3 bring-up**

---

## 0. 目的

本文固定 Kindle 实现阶段的语言与绑定选择原则，避免后续执行者在每个 Execution Prompt 中重新讨论“应该用 Lua、Rust、C 还是其他语言”。

核心裁决：

> **Baga Device Adapter Contract 冻结的是接口语义、能力、事件、错误、生命周期、测试与兼容性，不冻结实现语言。**

因此：

```text
Rust / C / Kotlin / Lua / other language
```

都不是“被允许语言白名单”或“唯一正确语言”。

实现语言必须服从目标平台的成熟生态和实际工程成本。一个 Adapter 也可以使用多种语言，只要边界清晰并满足 Contract / Contract Tests / BICTS。

---

# 1. Authority / Inputs

本裁决服从：

```text
docs/zh-CN/standards/07_设备适配器规范.md
docs/zh-CN/standards/11_Kindle适配规范.md
docs/zh-CN/design/02_设备适配器可执行契约与SDK设计.md
docs/zh-CN/reference-apps/03_Kindle具体实现架构冻结.md
docs/plans/platform-ports/kindle/0010_Kindle实现任务总计划_Baga-Ink-Kindle-Implementation-Master-Plan.md
```

本文不改变 Device Adapter Contract，也不新增公共架构层。

`docs/zh-CN/design/02` 当前列出的 Rust/C/Kotlin generated interfaces 应理解为：

> **当前首批官方 codegen / binding targets。**

它们不是 Adapter 实现语言限制。

“Event 不直接进入 Lua/IKP”的语义仍保持：底层事件先由 Adapter 归一化并进入 Platform Core；这不等于禁止 Adapter 内部使用 Lua 实现。

---

# 2. 语言选择优先级

实现某个 subsystem 时，按以下顺序选择语言/绑定方式：

```text
1. 成熟能力本来在哪里，能否直接包装
2. 对目标 Kindle / ABI / firmware 的兼容性与已验证程度
3. glue 层是否最少，是否避免额外 FFI / IPC / 数据转换
4. 可维护性、可调试性、升级 pinned upstream 的成本
5. 启动时间、内存、包体积
6. 实测性能
7. 安全性 / 内存安全要求
```

性能是因素之一，但不是默认第一优先级。

禁止仅因为：

```text
“Rust 更快”
“C 更底层”
“统一语言更整齐”
```

就把已经成熟可复用的 KOReader Lua、FBInk C 或其他模块重新实现一遍。

只有真实 profiling、ABI、兼容性、稳定性或安全证据表明当前方案无法满足要求时，才改变语言或增加 native bridge。

---

# 3. 允许混合语言，不要求 Adapter 单语言化

正确形态可以是：

```text
Kindle Adapter
│
├── common/       Lua
├── display/      Lua + existing FBInk C binding where needed
├── input/        Lua
├── storage/      Lua + existing native/database components where needed
├── lifecycle/    Lua
├── power/        Lua + narrow native mechanism where required
├── network/      Lua / existing Platform networking bridge
├── profiles/     data + Lua loader
└── quirks/       data + Lua glue
```

其他 Platform 子系统可以继续使用最合适的语言，例如：

```text
IKP verifier / cryptography
→ Rust/C/native verified core

KOReader Reader/UI
→ KOReader existing Lua/LuaJIT implementation

FBInk
→ existing C implementation
```

这些不需要为了“语言统一”重写。

---

# 4. Kindle 第一阶段默认实现选择

以下是 K0–K3 的默认实现基线。后续 AI MUST 从这张表开始，不得把语言选择重新作为开放问题。

| Area | Default implementation | Rule |
|---|---|---|
| KOReader bootstrap / Baga private bootstrap | **Lua/LuaJIT first** | 直接复用 KOReader 已有 Lua 初始化环境 |
| Kindle Adapter common glue | **Lua first** | identity、capability、profile、quirk、error/event normalization、self-test 优先薄 Lua glue |
| DisplayAdapter | **Lua wrapper around KOReader first** | 需要 FBInk 时复用现有 C/native binding；不重写 framebuffer stack |
| InputAdapter | **Lua wrapper around KOReader Kindle input** | 不重新实现 evdev / touch calibration，除非有精确 quirk 证据 |
| LifecycleAdapter | **Lua wrapper around KOReader/Kindle/Homebrew events** | 固件差异进入 profile/quirk |
| PowerAdapter | **Lua wrapper first** | 只有已验证机制要求 native 时使用窄 binding，不新建 power daemon |
| Light / network device-state bridge | **Lua wrapper first** | HTTP/TLS 等共享栈不因 Adapter 而重写 |
| StorageAdapter policy/glue | **Lua first** | path containment / policy 在 Platform+Adapter 边界实现；SQLite/native storage 能力继续复用成熟库 |
| Reader/UI provider | **KOReader existing Lua stack** | 属于 Platform Reader/UI implementation，不塞入 Adapter root |
| Crypto / IKP signature verifier | **existing Rust/C/native verified implementation** | 不因为 Kindle 使用 Lua 就把 verifier 改写成 Lua |

这里的 “Lua first” 表示：

> **当成熟 Kindle 能力已经通过 KOReader Lua/LuaJIT 暴露时，优先直接用最薄 Lua glue 归一化为 Baga 语义。**

它不表示“所有代码必须 Lua”。

---

# 5. Codegen 与实现语言必须分开理解

机器 Contract：

```text
spec/adapter/*
```

是语言无关的单一语义源。

Generated SDK / binding 是开发便利层，不是实现资格门槛。

当前 Approved Design 列出的：

```text
Rust
C
Kotlin
```

继续作为首批官方 generated targets。

对 K0–K3 的明确裁决：

1. **不得因为当前没有通用 generated Lua SDK，就禁止 Kindle Adapter 用 Lua。**
2. **不得把“先新增通用 Lua codegen”设为 Kindle Bring-up 的前置条件。**
3. Kindle 可以使用由机器 Contract 语义和 Contract Tests 约束的薄 Lua binding/glue。
4. 如果未来希望把 Lua 提升为所有设备移植者都可依赖的正式 generated SDK target，应先修改 Approved Design，再创建新的 Task Version；这属于工具链能力扩展，不是 Kindle Adapter 使用 Lua 的许可条件。
5. 未来 Zig、Swift、Go 等 binding 也同理；官方是否生成某语言 binding，不决定该语言是否可以实现 Adapter。

---

# 6. K1 启动方案默认裁决

K1 不再把 direct entry 与 `.koplugin` 视为两个长期同等候选，让每个执行者重新选择。

默认方案固定为：

```text
pinned private KOReader bootstrap
        ↓
direct Baga private entry
        ↓
baga/bootstrap.lua
        ↓
Baga-owned surface / Platform bootstrap
```

可使用类似：

```text
--baga-app <app-id>
```

的 private argument，具体参数名可以在实现中微调。

Platform-private `.koplugin` 只作为 **fallback PoC**：

- direct entry 在真实 Kindle 上出现具体不可接受 blocker；
- blocker 有日志/真机证据；
- 例如无法避免 FileManager 暴露、生命周期不可控、升级 patch 成本明显更高或启动链无法可靠恢复。

没有上述证据时，执行者不得重新把 `.koplugin` 提升为默认方案。

---

# 7. K2 Kindle Adapter 的禁止事项

后续实现不得为了语言偏好而做以下工作：

```text
用 Rust/C 重写 KOReader 已成熟的 Kindle input stack
用 Rust/C 重写 KOReader 已成熟的 lifecycle/device knowledge
用 Lua 重写 FBInk
为了统一语言新增多层 FFI
让 LifeBook/IKP 直接 require KOReader private module
把 KOReader Lua object 暴露成公共 Baga API
把某一种实现语言写入 Device Adapter Contract
```

目标始终是：

```text
mature Kindle capability
        ↓
thinnest safe binding/glue
        ↓
Baga Device Adapter Contract
```

---

# 8. 什么时候允许偏离默认语言/方案

只有以下证据可以触发偏离：

```text
目标 ABI 无法构建/加载
目标 firmware API 不可用
真实 crash / lifecycle failure
真实性能 profiling 显示瓶颈
内存/启动时间超出明确 Gate
现有 binding 引入不可接受安全风险
成熟 upstream 已改变最佳接入层
```

偏离流程：

```text
Evidence
  ↓
更新 Task Design，创建新的 vNNN
  ↓
重新定义 affected subsystem 的实现方案与 Gate
  ↓
再生成新的 execution-prompts
```

Execution Prompt 或实现 Agent 不得在单次执行中静默改语言、改 backend 或重构整个接入层。

---

# 9. 执行 Prompt 必须怎样写

后续 K1/K2/K3 execution prompt 在涉及实现语言时 SHOULD 直接写：

```text
Use the Kindle implementation language/binding baseline.
Do not perform a new language-selection exercise.
Prefer Lua/LuaJIT thin glue when wrapping KOReader Kindle capability.
Reuse existing C/native libraries where that is the mature implementation.
Do not add FFI or rewrite components merely for language uniformity.
Any deviation requires concrete evidence and a new Task Design version.
```

这样语言选择成为上位设计输入，而不是每次编码前重新做架构决策。

---

# 10. 一句话裁决

> **Baga Device Adapter 是语言无关的 Contract；Kindle Reference Adapter 第一阶段采用“KOReader 能直接用 Lua 包装的地方优先 Lua、成熟 native 库保持 native、真正需要 native 的地方才加窄 binding”的混合实现。不要为了语言统一制造新的层，也不要让每个执行 AI 临时重新选型。**
