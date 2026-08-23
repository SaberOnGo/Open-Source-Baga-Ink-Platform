# TASK-0080 任务版本索引 / Task Version Index

> **Task ID：`TASK-0080`**  
> **任务：Baga Ink Client Kindle 自动安装 / Baga Ink Client Kindle Automation**  
> **关联 Milestone：K7**  
> **当前选定版本：`v001`**  
> **状态：Planned Baseline — dependency-gated**  
> **日期：2026-08-23**

---

## 1. Task 目标

在设备端 Platform 安装、启动、Home Entry 与 IKP 安装链均已稳定后，实现 Baga Ink Client 的 Kindle 状态检测、Installation Route DB、Homebrew/KPM bootstrap、Platform ensure 与 IKP transfer/install 自动化。

---

## 2. Version History

| Version | Status | Summary | Reason |
|---|---|---|---|
| `v001` | Planned | detect/state、Route DB、KPM state、Platform ensure、IKP transfer/handshake、recovery UX | 首个 Client Kindle 自动化任务设计 |

---

## 3. Dependency Gate

```text
TASK-0070 K6 verified native package + Home Entry path
TASK-0050 K4 device-side IKP verifier/install chain
```

K7 不作为 K1–K6 设备侧正确性的前置条件。

---

## 4. Authority / Inputs

```text
docs/zh-CN/reference-apps/03_Kindle具体实现架构冻结.md
current Client/Distribution/Compatibility standards and design
verified Kindle installation-route evidence
```

---

## 5. Current Design

```text
v001/0000_任务设计总纲_Task-Design-Overview.md
```

Route schema、state model、recovery contract 或 transfer handshake 发生结构性变化时，应创建新版本。
