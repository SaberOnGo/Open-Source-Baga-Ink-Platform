# TASK-0010 v002 任务设计总纲 / Executable Adapter Contract Task Design

> **Task ID：`TASK-0010`**  
> **Version：`v002`**  
> **Milestone：K0 — Adapter Contract 可执行基础**  
> **状态：Selected Planning Baseline**  
> **日期：2026-08-23**

---

## 0. Goal

建立 Baga Ink Device Adapter Base Contract 的机器可执行闭环，同时明确：

> **Contract 与实现语言解耦。IDL 冻结跨平台语义，不规定 Kindle、Android 或未来设备必须使用哪一种语言。**

基础闭环：

```text
Markdown semantic authority
        ↓
machine-readable IDL
        ↓
deterministic codegen / bindings
        ↓
Mock Adapter
        ↓
Adapter Contract Tests
        ↓
frozen contract snapshot
```

Base Mandatory surface：

```text
DeviceDescriptor / Identity
Capability Snapshot
Display
Input
Storage
Lifecycle
Power
Root init / self-test / shutdown
Error / Event core semantics
```

---

# 1. Authority and Implementation Decision

权威输入：

```text
docs/zh-CN/standards/07_设备适配器规范.md
docs/zh-CN/standards/04_能力注册表.md
docs/zh-CN/standards/08_兼容性标准.md
docs/zh-CN/standards/10_兼容性测试套件.md
docs/zh-CN/design/02_设备适配器可执行契约与SDK设计.md
docs/plans/platform-ports/kindle/0020_Kindle实现语言与绑定裁决_Kindle-Implementation-Language-and-Binding-Decision.md
```

实施解释固定为：

```text
IDL / Contract
→ language-independent semantic source

Generated Rust/C/Kotlin interfaces
→ current first-party codegen targets
→ not an implementation-language whitelist

Kindle Lua/LuaJIT implementation
→ permitted when it is the shortest compatible path to mature Kindle capability
```

“某语言没有官方 generated SDK”不得被解释为“该语言不能实现 Adapter”。

---

# 2. Scope

`v002` 覆盖：

```text
1. `spec/adapter/` schema 与 loader
2. Contract root、descriptor、capability、error、event core types
3. Base subsystem IDL
   - display
   - input
   - storage
   - lifecycle
   - power
4. frozen v0.1 snapshot
5. Approved Design 当前定义的 first-party generated targets
6. Mock / Headless Adapter
7. Adapter Contract Test harness
8. IDL validation / reproducibility / compatibility checks
9. CI gate
10. generator architecture 保持可扩展到未来其他 binding
```

---

# 3. Out of Scope

本版本明确不做：

```text
把某一种语言写进 Device Adapter Contract
要求所有 Adapter 使用同一种语言
把 Rust/C/Kotlin 列表变成允许语言白名单
为了 Kindle Bring-up 强制先完成通用 Lua SDK codegen
Kindle Device Adapter backend 本身
Android E-Paper backend 本身
运行时动态 Adapter daemon/RPC/JSON bridge
BICTS 整机认证
```

---

# 4. Codegen Decision

K0 `v002` 的默认裁决：

1. 继续按 Approved Design 实现当前 first-party generated targets；
2. generator/IDL 设计 MUST 不把语言集合写死成 Contract 语义；
3. 新语言 binding 应可作为工具链 target 增加，而无需修改 Device Adapter semantic Contract；
4. **通用 generated Lua SDK 不是 K1/K2 的前置 Gate**；
5. Kindle 可以通过薄 Lua binding/glue 使用同一 Contract semantics 和 Contract Tests；
6. 如果未来决定把 Lua 提升为正式、对所有第三方移植者承诺的 generated target，应修改 Approved Design 并创建新的 Task Version。

因此后续实现 Agent 不需要在 K0 阶段重新讨论“为了 Kindle 是否必须先做 Lua codegen”。当前答案是：**不必须，不阻塞 Kindle Bring-up。**

---

# 5. Implementation Boundaries

IDL 只描述：

```text
interfaces
methods
types/enums
required/optional
errors
events
version/deprecation/default semantics
```

IDL 不描述：

```text
Kindle waveform
KOReader object
FBInk API
Lua object layout
Rust allocator
Android Context
specific FFI implementation
```

这些属于各 Platform Port 实现。

---

# 6. Mock and Test Strategy

Mock Adapter 必须证明 Contract 与特定实现语言无关：

```text
deterministic descriptor/capability
in-memory display
scripted input
sandbox storage
synthetic lifecycle
synthetic power
stable event/error semantics
```

Contract Tests 验证行为语义，不验证“源码是否使用某一种语言”。

后续 Kindle Adapter 可以通过适合其运行时的 runner/binding 接入同一测试定义。

---

# 7. Compatibility / Reproducibility Gate

必须满足：

```text
same IDL + same generator version
→ same generated output

frozen contract
→ compatibility diff can be checked

unknown/optional semantics
→ deterministic

Mock Adapter
→ Base Contract tests pass
```

语言 binding 的新增不应在没有 semantic Contract 变化时被误判为 Contract breaking change。

---

# 8. Acceptance Gate

`TASK-0010/v002` 完成条件：

- Base Contract 可由机器 IDL 完整表达；
- frozen snapshot 可比较；
- current first-party codegen 可重复；
- Mock Adapter 通过 Base Contract Tests；
- generator 不把 Rust/C/Kotlin 当成 Device Adapter 允许语言白名单；
- 文档与测试明确 implementation language is not a compatibility criterion；
- K1/K2 不因缺少通用 Lua codegen 被阻塞；
- 不引入 daemon/RPC/JSON bridge 新架构层。

---

# 9. Expected Execution-Prompt Groups

后续可拆为：

```text
IDL schema / loader
core types
Base subsystem definitions
first-party codegen
Mock Adapter
Contract Test harness
freeze / compatibility tooling
CI reproducibility
language-neutrality regression checks
```

Execution Prompt 不得重新决定 Kindle Adapter 具体使用 Rust/C/Lua；Kindle 语言选择由 `0020_Kindle实现语言与绑定裁决` 与 `TASK-0030` 控制。
