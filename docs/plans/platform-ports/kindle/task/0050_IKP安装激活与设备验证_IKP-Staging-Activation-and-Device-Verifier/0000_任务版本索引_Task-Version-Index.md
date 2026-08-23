# TASK-0050 任务版本索引 / Task Version Index

> **Task ID：`TASK-0050`**  
> **任务：IKP 安装激活与设备验证 / IKP Staging Activation and Device Verifier**  
> **关联 Milestone：K4**  
> **当前选定版本：`v001`**  
> **状态：Planned Baseline — dependency-gated**  
> **日期：2026-08-23**

---

## 1. Task 目标

把 K3 的 developer-mode local IKP loading 升级为符合 Baga IKP、Signing、Update、Rollback 规范的设备端安装闭环：验证、staging、immutable release、atomic activation、health/probation 与 rollback。

---

## 2. Version History

| Version | Status | Summary | Reason |
|---|---|---|---|
| `v001` | Planned | verifier integration、staging、activation、rollback、negative vectors | 首个生产级 IKP 设备安装链任务设计 |

---

## 3. Dependency Gate

```text
TASK-0040 K3 Probe developer-mode chain accepted
Signing / IKP validation / update executable-spec baseline available
```

---

## 4. Authority / Inputs

```text
docs/zh-CN/standards/06_IKP应用包规范.md
current Signing / Publisher / Repository / Update / Rollback standards
current executable specification / verifier reference implementation
docs/zh-CN/reference-apps/03_Kindle具体实现架构冻结.md
```

---

## 5. Current Design

```text
v001/0000_任务设计总纲_Task-Design-Overview.md
```

若 trust model、activation transaction、rollback/data separation 或 shared-vector Gate 发生结构性变化，应创建新版本。
