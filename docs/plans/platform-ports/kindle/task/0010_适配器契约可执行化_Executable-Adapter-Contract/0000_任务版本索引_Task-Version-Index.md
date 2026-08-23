# TASK-0010 任务版本索引 / Task Version Index

> **Task ID：`TASK-0010`**  
> **任务：适配器契约可执行化 / Executable Adapter Contract**  
> **关联 Milestone：K0**  
> **当前选定版本：`v001`**  
> **状态：Selected Planning Baseline**  
> **日期：2026-08-23**

---

## 1. Task 目标

把 Baga Ink Device Adapter Base Contract 转换为机器可读、可生成、可 Mock、可自动测试的最小工程闭环，为 Kindle、Android E-Paper 与后续设备移植提供共同的可执行契约基础。

本 Task 不重新定义 Device Adapter 语义；`docs/zh-CN/standards/07_设备适配器规范.md` 仍是语义权威。

---

## 2. Version History

| Version | Status | Summary | Reason |
|---|---|---|---|
| `v001` | Selected | Base Contract IDL、codegen、Mock、Contract Tests、frozen snapshot | 首个可执行化实现版本 |

---

## 3. Authority / Inputs

主要依据：

```text
docs/zh-CN/standards/07_设备适配器规范.md
docs/zh-CN/standards/04_能力注册表.md
docs/zh-CN/standards/08_兼容性标准.md
docs/zh-CN/standards/10_兼容性测试套件.md
docs/zh-CN/design/02_设备适配器可执行契约与SDK设计.md
docs/plans/platform-ports/kindle/0010_Kindle实现任务总计划_Baga-Ink-Kindle-Implementation-Master-Plan.md
```

发生冲突时按上位文档优先级处理，不在本 Task 中形成平行 Contract。

---

## 4. Current Selected Version

当前执行设计来源：

```text
v001/0000_任务设计总纲_Task-Design-Overview.md
```

若机器 schema 范围、正式 codegen target、兼容性策略或 Base Gate 发生结构性变化，应创建新版本，不覆盖 `v001`。

---

## 5. Downstream

本 Task 的 Gate 是以下工作的前置依赖之一：

```text
TASK-0030 Kindle Base Device Adapter
TASK-0040 Minimal Platform Core + Probe IKP
future Android E-Paper Adapter implementation
```

`TASK-0020` 的 KOReader/kindlehf substrate bring-up 可与本 Task 的非冲突工作有限并行。
