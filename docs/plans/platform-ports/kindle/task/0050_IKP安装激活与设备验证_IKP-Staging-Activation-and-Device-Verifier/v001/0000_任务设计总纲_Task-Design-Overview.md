# TASK-0050 v001 任务设计总纲 / IKP Staging Activation and Device Verifier Task Design

> **Task ID：`TASK-0050`**  
> **Version：`v001`**  
> **Milestone：K4 — IKP stage / activate + device verifier**  
> **状态：Planned Baseline — dependency-gated**  
> **日期：2026-08-23**

---

## 0. Goal

将 K3 的开发模式 IKP 启动链升级为可验证、可恢复的设备端 App 安装链：

```text
IKP input
   ↓
strict package validation
   ↓
canonical/signature verification
   ↓
staging
   ↓
immutable release
   ↓
atomic activation
   ↓
health/probation
   ↓
active or rollback to last-known-good
```

Kindle 端复用仓库现有 executable specification / reference verifier 的稳定结果，不维护第二套 canonicalization 或 signature 语义。

---

# 1. Dependencies and Authority

前置：`TASK-0040` K3 Gate 通过，并且签名/IKP executable baseline 已有稳定 shared vectors。

权威输入：

```text
docs/zh-CN/standards/06_IKP应用包规范.md
current Publisher / Signing / Repository / Update / Rollback standards
current executable specification and reference verifier
docs/zh-CN/reference-apps/03_Kindle具体实现架构冻结.md
```

Trust 与 update 语义只来自上位规范；Kindle binding 只负责把稳定 verifier/installer 语义落到设备。

---

# 2. Scope

```text
IKP package reader integration
strict manifest/package validation
canonicalization + signature verifier integration
publisher identity result integration
staging layout
immutable release layout
App package / App data separation
atomic active-release state
health/probation result
last-known-good rollback
corrupt/unsigned/wrong-hash negative tests
shared test vectors between device/reference verifier
install/update/rollback BICTS subset
```

---

# 3. Out of Scope

```text
Baga Market discovery UI
remote repository service implementation
Client USB transfer workflow
Platform native `.kpkg` update
LifeBook product update policy
new cryptographic algorithm design
new trust-root model
```

Platform native update 与 IKP App update 保持两个不同事务。

---

# 4. State and Storage Layout

设备端至少区分：

```text
incoming/staging package
verified immutable app release
active release pointer/state
last-known-good release
App mutable data
verification/activation evidence
```

原则：

```text
App package is replaceable/immutable release content
App data survives package update/rollback according to policy
```

不得通过“覆盖当前目录中的一半文件”完成 update。

---

# 5. Verifier Integration

Kindle device verifier 与 reference verifier 必须共享：

```text
strict JSON rules
canonical form rules
signature input bytes
publisher identity semantics
hash calculation
IKP structural validation
error classes/test vectors
```

设备实现可以使用适合 Kindle 的 native/library binding，但验证结果必须与 reference vectors 一致。

---

# 6. Activation Transaction

推荐事务：

```text
receive package
→ validate structure
→ verify trust/signature/hash
→ stage complete release
→ fsync/commit required metadata
→ atomically switch active release state
→ launch probation
→ mark healthy
```

失败时：

```text
before activation
→ old active release untouched

after activation but probation fails
→ restore last-known-good active state
```

具体原子机制由实现与 Kindle filesystem 能力决定，但必须具备测试证据。

---

# 7. Test Strategy

## Shared Host/Reference Tests

```text
valid IKP
invalid JSON/manifest
wrong digest
invalid signature
unknown publisher/trust case
missing entry/resource
unexpected package layout
version/update ordering cases
```

## Device Integration Tests

```text
stage valid package
reject invalid package before activation
activate new release
relaunch active release
probation failure rollback
power interruption at selected transaction points
App data remains separate
last-known-good recovery
```

Power interruption测试只能在已有恢复步骤和隔离测试 App 上执行。

---

# 8. Debug Strategy

日志按事务阶段记录稳定 code：

```text
RECEIVE
PARSE
VALIDATE
VERIFY
STAGE
ACTIVATE
PROBATION
HEALTHY
ROLLBACK
```

错误应保留上位 verifier 的稳定分类，不把所有失败折叠成一个 Kindle-specific message。

---

# 9. Real-device Validation

使用 `baga-probe.ikp` 或专用测试 IKP 验证，不使用正式 LifeBook 用户数据作为破坏性测试对象。

保留证据：

```text
old/new release id
package digest
verification result
activation state before/after
App data checksum/state
probation result
rollback evidence
relaunch result
```

---

# 10. Data Protection and Recovery

- App data 不因 package verification failure 被删除。
- rollback 不删除用户 App data。
- invalid package 不得成为 active release。
- 设备中断后应能确定唯一有效 active/last-known-good 状态。
- Kindle 用户书籍、Amazon 笔记和系统数据不属于 IKP installer 管理范围。

---

# 11. Acceptance Gate

- [ ] invalid IKP 在 activation 前被拒绝。
- [ ] valid IKP 先完成 verification 与完整 staging，再切换 active release。
- [ ] active switch 具备原子/可恢复证据。
- [ ] package/release 与 mutable App data 分离。
- [ ] probation failure 可以恢复 last-known-good。
- [ ] rollback 不删除 App data。
- [ ] Kindle verifier 与 reference verifier 对 shared vectors 结果一致。
- [ ] interruption/relaunch 后 installer state 可恢复或明确失败。
- [ ] Platform native package update 与 IKP update 未混成同一事务。
- [ ] install/update/rollback 相关 BICTS subset 通过。

---

# 12. Known Risks

主要风险是 filesystem 原子性假设、异常断电状态、设备 verifier 与 reference verifier 漂移、App data/release 边界不清，以及在 Kindle 端复制上位验证逻辑后产生长期分叉。

---

# 13. Expected Execution-Prompt Groups

```text
A. Shared verifier/vector audit
B. Device verifier binding
C. staging/release/data layout
D. atomic activation state
E. health/probation
F. rollback
G. negative/interruption tests
H. real-device K4 Gate
```
