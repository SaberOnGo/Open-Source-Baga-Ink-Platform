# TASK-0080 v001 任务设计总纲 / Baga Ink Client Kindle Automation Task Design

> **Task ID：`TASK-0080`**  
> **Version：`v001`**  
> **Milestone：K7 — Baga Ink Client + Installation Route DB**  
> **状态：Planned Baseline — dependency-gated**  
> **日期：2026-08-23**

---

## 0. Goal

在设备端 Platform 已稳定后，把 Kindle enablement/install/transfer 收敛为 Baga Ink Client 的可验证自动化流程：

```text
Detect Kindle
→ collect exact model / firmware / current state
→ resolve verified Installation Route when required
→ reach/confirm Homebrew-ready
→ ensure KPM state when compatible
→ install/verify Baga Platform
→ transfer signed IKP
→ device-side re-verify/install
→ confirm launch/result
```

Client 内部保持两个独立职责：

```text
A. Ensure Baga Platform
B. Transfer / Install IKP
```

---

# 1. Dependencies and Authority

前置至少包括：

```text
TASK-0070 K6 verified Platform package/Home Entry path
TASK-0050 K4 verified IKP install/verify path
```

权威输入：

```text
docs/zh-CN/reference-apps/03_Kindle具体实现架构冻结.md
current Compatibility / Distribution / Client design
verified installation-route records and evidence
```

Jailbreak/enablement 项目是 Installation Route records，不是 Platform Core/Adapter dependencies。

---

# 2. Scope

```text
USB/transport Kindle detection
exact model/firmware/current-state collection
Installation Route DB schema
route matching/ranking
Homebrew foundation state detection
KPM-compatible vs KPM-installed distinction
KPM bootstrap where verified compatible
verified fallback envelope where KPM unavailable/unvalidated
Platform version/state detection
ensure/install/verify Platform
filesystem mailbox or equivalent controlled handshake
signed IKP transfer
on-device re-verification/install result
result outbox/evidence
recovery/data-protection UX
route regression matrix by exact model + firmware
```

---

# 3. Out of Scope

```text
creating new jailbreak exploits
embedding exploit logic into Platform Core
making one route a permanent Platform dependency
guessing support for unknown firmware
changing Device Adapter Contract
changing IKP trust semantics
using Client success as substitute for BICTS/Compatibility evidence
```

Unknown combinations default to Unsupported/Experimental according to current compatibility policy until verified.

---

# 4. Device State Model

Client 至少区分：

```text
Stock / not Homebrew-ready
Homebrew-ready
KPM compatible + installed
KPM compatible + not installed
KPM unavailable/unvalidated
Baga Platform absent
Baga Platform installed but unhealthy/outdated
Baga Platform healthy
IKP absent/staged/installed/failed
```

不得把“KPM 未安装”与“KPM 不兼容”合并为一个状态。

---

# 5. Installation Route DB

Route record 应能表达：

```text
route id/version
supported exact model families
firmware range or exact constraints
required current state
transport prerequisites
steps/runner reference
expected state transitions
verification checks
recovery path
known risks
source/evidence provenance
status: verified / experimental / deprecated / blocked
```

可记录 WinterBreak、SpringBreak、Sanctuary、Véra、legacy/future verified routes，但 route 名称本身不等于支持声明。

---

# 6. Route Resolution

解析顺序：

```text
collect exact evidence
→ determine current state
→ filter routes by explicit constraints
→ reject ambiguous/unknown combinations
→ select highest-confidence verified route
→ execute state transition
→ verify resulting state before next stage
```

Client 不应仅依据“型号相似”“版本大概在范围内”推断可执行 route。

---

# 7. Ensure Platform Flow

```text
if Platform healthy and compatible:
    keep existing Platform
else:
    if not Homebrew-ready:
        resolve verified enablement route
    determine KPM compatibility
    if KPM compatible but not installed:
        bootstrap/ensure KPM
    if KPM verified available:
        install baga-platform*.kpkg
    else if a verified fallback exists:
        use fallback Platform installer envelope
    verify Platform health/version
```

每个状态转换都产生可读取结果，避免 Client 只依据超时猜测完成。

---

# 8. IKP Transfer / Install Flow

```text
select signed IKP
→ transfer to controlled inbox/staging location
→ record digest/metadata
→ signal device-side installer
→ device re-verifies package
→ install/activate using K4 transaction
→ write result/outbox
→ Client reads final result
```

Client 的桌面侧预检查不能替代设备侧 verifier。

---

# 9. Transport and Handshake

11th-gen 及更新 Kindle 可能存在 MTP 等电脑侧传输差异。该差异属于 Client/enablement/transport 层，不进入 Universal IKP 或 LifeBook。

Handshake 需要稳定表达：

```text
request id
operation
input digest/version
current device state
result state
error code
logs/evidence pointer where appropriate
```

具体 transport 可替换，但语义状态机保持一致。

---

# 10. Test Strategy

建立 route/state regression matrix：

```text
already Platform-ready device
Homebrew-ready + KPM installed
Homebrew-ready + KPM compatible/not installed
KPM unavailable but verified fallback
stock device with one verified route
unknown firmware
interrupted transfer
failed Platform install
failed IKP verification
reconnect/retry
```

每个自动化场景都应能证明最终设备状态，而不是只检查 Client 进度条。

---

# 11. Real-device Validation

首个 end-to-end Gate 只要求一条**精确已验证**的 model + firmware 组合，不要求一次覆盖全部 Kindle。

证据至少包括：

```text
Client build/version
model/firmware detected
initial state
selected route id/version and evidence basis
state transitions
KPM state
Platform package/version/result
IKP digest/result
final launch verification
recovery result when negative test applies
```

---

# 12. Data Protection and Recovery UX

Client 流程必须以数据保护为基本 Gate：

- 不清除 Kindle 用户书籍。
- 不清除用户笔记。
- 不把恢复出厂作为普通失败处理。
- 每个高风险 route 必须有明确前置条件、停止条件和恢复路径。
- 传输中断后允许安全重试，不留下无法解释的 active App 状态。
- Platform install/update 失败优先恢复上一可用 Platform。
- IKP install 失败服从 K4 staging/rollback 语义。

---

# 13. Acceptance Gate

对至少一条精确 verified Kindle 组合：

- [ ] Client 正确检测 model/firmware/current state。
- [ ] Route resolver 只选择满足明确约束的 verified route。
- [ ] Homebrew-ready 状态可被验证，而不是仅由步骤完成推断。
- [ ] KPM compatible 与 KPM installed 被分别检测。
- [ ] Platform 可被 ensure/install 并通过设备 health check。
- [ ] signed IKP 可传输到受控 inbox/staging。
- [ ] 设备端重新验证并安装 IKP。
- [ ] Client 获得明确设备侧结果。
- [ ] 最终 App 可从已验证入口启动。
- [ ] 失败/中断场景有可执行恢复路径。
- [ ] 未知 firmware 不被静默继承为 supported。
- [ ] 全流程不清除 Kindle 用户书籍或笔记。

---

# 14. Known Risks

主要风险：route evidence 过期、Amazon firmware 更新、PC transport 差异、MTP/USB 行为变化、Client 与 device state 不一致、KPM compatibility 误判、enablement route 中断，以及过度自动化掩盖了真实设备状态。

Route DB 应作为持续维护的数据资产，不能把一次成功记录直接推广到未验证组合。

---

# 15. Expected Execution-Prompt Groups

```text
A. Device detection/state model
B. Route DB schema + fixtures
C. resolver/ranking
D. Homebrew/KPM state checks
E. Ensure Platform flow
F. transfer/mailbox handshake
G. device-side IKP install result integration
H. recovery/data-protection UX
I. exact model+firmware regression matrix
J. end-to-end K7 Gate
```
