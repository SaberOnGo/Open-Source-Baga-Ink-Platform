# TASK-0010 v001 任务设计总纲 / Executable Adapter Contract Task Design

> **Task ID：`TASK-0010`**  
> **Version：`v001`**  
> **Milestone：K0 — Adapter Contract 可执行基础**  
> **状态：Selected Planning Baseline**  
> **日期：2026-08-23**

---

## 0. Goal

建立 Baga Ink Device Adapter Base Contract 的首个机器可执行闭环：

```text
Markdown semantic authority
        ↓
machine-readable IDL
        ↓
deterministic codegen
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

完成后，Kindle 与后续设备移植可基于同一 Contract/Test foundation 实现，而不是分别维护接口定义。

---

# 1. Authority and Constraints

权威输入：

```text
docs/zh-CN/standards/07_设备适配器规范.md
docs/zh-CN/standards/04_能力注册表.md
docs/zh-CN/standards/08_兼容性标准.md
docs/zh-CN/standards/10_兼容性测试套件.md
docs/zh-CN/design/02_设备适配器可执行契约与SDK设计.md
```

实施约束：

1. Markdown Standard 仍是语义权威；机器 IDL 不成为第二套独立协议。
2. 第一阶段采用 compile-time/package-time typed integration，不新增 Adapter daemon、RPC、Binder 或 JSON bridge。
3. IDL 只表达跨设备稳定语义，不包含 Kindle waveform、KOReader object、Android Context 等实现细节。
4. 兼容性变化必须可检测；codegen 输出必须可重复。

---

# 2. Scope

`v001` 覆盖：

```text
1. `spec/adapter/` schema 与 loader
2. Contract root、descriptor、capability、error、event core types
3. Base subsystem IDL
   - display
   - input
   - storage
   - lifecycle
   - power
4. `spec/adapter/frozen/v0.1/` 快照
5. Approved Design 已定义的首批 generated interface targets
6. Mock / Headless Adapter
7. Adapter Contract Test harness
8. IDL validation、codegen reproducibility、compatibility checks
9. CI gate
```

Base Compatibility 关注：

```text
display.basic
input.navigation
storage.app_sandbox
power.sleep_wake
platform.lifecycle
```

---

# 3. Out of Scope

本版本不实现：

```text
Kindle Device Adapter backend
Android E-Paper backend
optional device subsystems 的完整实现
运行时动态 Adapter 机制
Adapter 进程间通信层
设备型号 Compatibility DB
BICTS 全套整机认证
LifeBook / IKP App runtime
```

---

# 4. Lua Binding Boundary

Kindle Platform 内部大量复用 KOReader Lua/LuaJIT，因此后续 Kindle integration 可以需要一层 Lua binding/stub。

`v001` 的边界为：

```text
General generated Adapter SDK targets
→ 服从 `docs/zh-CN/design/02_设备适配器可执行契约与SDK设计.md`

Kindle-private Lua binding
→ 可以作为 Platform implementation glue
→ 不自动升级为新的公共 SDK target
```

若计划把 Lua 正式加入通用 generated SDK target，需先更新 Approved Design，再形成新的 Task Version。

---

# 5. Proposed Repository Write Scope

```text
spec/adapter/
├── contract.yaml
├── types.yaml
├── descriptor.yaml
├── events.yaml
├── errors.yaml
├── subsystems/
└── frozen/v0.1/

sdk/adapter/
├── generated/
├── mock/
└── ...

tools/baga-adapter-codegen/

tests/adapter_contract/
tests/adapter_mock/

existing CI integration
```

目录细节允许按当前仓库结构微调，但职责边界保持不变。

---

# 6. Implementation Design

## 6.1 Schema / Loader

Loader 至少校验：

```text
contract version
unique type/interface names
required/optional markers
method/event/error references
introduced/deprecated metadata
unknown-field handling
stable ordering/canonical representation
```

## 6.2 Core Types

优先冻结 Base subsystem 共同依赖的类型：

```text
DeviceDescriptor
CapabilitySnapshot
AdapterError / ErrorCode
AdapterEvent
SelfTestMode / SelfTestReport
geometry / region / refresh intent
navigation/input semantic events
storage containment semantics
lifecycle events
power state/result
```

## 6.3 Codegen

目标：

```text
same IDL + same generator version
→ stable generated output
```

生成文件带 machine-generated marker 与 contract version，避免手工维护平行接口。

## 6.4 Mock Adapter

Mock 至少能够模拟：

```text
Base capabilities
deterministic display geometry
navigation/input events
app sandbox storage
lifecycle transitions
sleep/wake
backend failure results
```

Mock 用于验证 Contract 与 Platform dispatch，不代替真实 Kindle 证据。

---

# 7. Test Strategy

至少建立：

```text
Schema validation tests
IDL semantic validation tests
Golden/frozen snapshot tests
Codegen reproducibility tests
Generated interface compile tests
Mock Adapter Base Contract Tests
Invalid/incompatible IDL negative tests
Compatibility diff tests
```

每项能力先形成可观察的失败基线，再实现对应行为。任何 schema 变更都应能判断为 backward-compatible、breaking 或 metadata-only。

---

# 8. Debug Strategy

失败按层定位：

```text
source Standard mismatch?
        ↓
IDL schema/loader?
        ↓
semantic validator?
        ↓
codegen?
        ↓
generated compile?
        ↓
Mock behavior / Contract Test?
```

Kindle backend 不应通过私有字段绕过 IDL/Contract 问题。

---

# 9. Real-device Requirement

K0 的核心 Gate 不要求真实 Kindle，可在 CI/headless 环境完成。真实设备证据从 K1/K2 开始。

---

# 10. Data Protection and Rollback

本 Task 不操作 Kindle 用户数据。

IDL/frozen snapshot 更新通过 Git 历史保留；如新 schema/codegen 破坏已冻结行为，应回退相关变更或建立新的明确 Contract version，不覆盖旧 frozen snapshot。

---

# 11. Acceptance Gate

`TASK-0010/v001` 通过需同时满足：

- [ ] Machine IDL 能表达 Device Adapter Base Mandatory surface。
- [ ] Root/descriptor/capability/error/event/Base subsystem 定义与 Standard 07 一致。
- [ ] Frozen `v0.1` snapshot 可生成、可比较。
- [ ] Generated interfaces 从单一 IDL 产生。
- [ ] 相同输入的 codegen 输出可重复。
- [ ] Mock Adapter 完整实现 Base surface。
- [ ] Mock 通过 Base Adapter Contract Tests。
- [ ] invalid/incompatible IDL 有明确失败测试。
- [ ] CI 能阻止 schema/codegen drift。
- [ ] 未引入新的跨进程架构层。

Gate 未通过时，`TASK-0030` 不应建立独立于公共 Contract 的 Kindle 私有接口体系。

---

# 12. Known Risks and Open Questions

主要风险：Markdown/IDL 漂移、schema 过早冻结、不同环境 codegen 差异、optional/absent 语义不一致，以及把 Kindle/KOReader 实现细节错误提升到通用 Contract。

实现期需回答：

1. 首版 schema validator 的实现语言与依赖选择。
2. generated target 的目录与构建集成方式。
3. Kindle-private Lua binding 最适合在 K0 后单独生成，还是在 K2 以薄 binding 实现。

第 3 项不改变当前 Approved Design 的公共 generated SDK target。

---

# 13. Expected Execution-Prompt Groups

```text
A. Source authority audit + failing baseline
B. IDL schema/loader
C. Core types + Base subsystem definitions
D. Frozen snapshot
E. Codegen
F. Mock Adapter
G. Contract Tests
H. Reproducibility/compatibility CI
I. Final K0 Gate review
```
