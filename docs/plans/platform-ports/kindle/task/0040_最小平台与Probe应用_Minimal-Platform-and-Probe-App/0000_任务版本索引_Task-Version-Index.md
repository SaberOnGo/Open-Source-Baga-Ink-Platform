# TASK-0040 任务版本索引 / Task Version Index

> **Task ID：`TASK-0040`**  
> **任务：最小平台与 Probe 应用 / Minimal Platform and Probe App**  
> **关联 Milestone：K3**  
> **当前选定版本：`v001`**  
> **状态：Planned Baseline — dependency-gated**  
> **日期：2026-08-23**

---

## 1. Task 目标

实现最小 Baga Ink Platform Core 与首个真正的 `baga-probe.ikp`，在真实 Kindle 上完成 UI、Input、Storage、Lifecycle、Power 的第一条端到端平台链。

---

## 2. Version History

| Version | Status | Summary | Reason |
|---|---|---|---|
| `v001` | Planned | minimal Core、Lua Host、Base `baga.*`、minimal UI、developer IKP loading、Probe、sleep/wake | 首个真实 IKP 端到端任务设计 |

---

## 3. Dependency Gate

```text
TASK-0010 K0 Contract baseline accepted
TASK-0020 K1 kindlehf substrate accepted
TASK-0030 K2 Base Kindle Adapter accepted
```

---

## 4. Authority / Inputs

```text
docs/zh-CN/standards/02_应用标准.md
docs/zh-CN/standards/03_API规范.md
docs/zh-CN/standards/05_权限模型.md
docs/zh-CN/standards/06_IKP应用包规范.md
docs/zh-CN/standards/07_设备适配器规范.md
docs/zh-CN/standards/10_兼容性测试套件.md
docs/zh-CN/reference-apps/03_Kindle具体实现架构冻结.md
```

---

## 5. Current Design

```text
v001/0000_任务设计总纲_Task-Design-Overview.md
```

若最小 Platform Core 职责、Probe Gate、developer-mode loading 边界或 sleep/wake 验收发生结构性变化，应新建 Task Version。
