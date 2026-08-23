# TASK-0030 任务版本索引 / Task Version Index

> **Task ID：`TASK-0030`**  
> **任务：Kindle 基础设备适配器 / Kindle Base Device Adapter**  
> **关联 Milestone：K2**  
> **当前选定版本：`v001`**  
> **状态：Planned Baseline — dependency-gated**  
> **日期：2026-08-23**

---

## 1. Task 目标

实现符合 Baga Device Adapter Contract 的薄 Kindle Reference Adapter，最大化复用 KOReader/koreader-base、FBInk、Kindle OS 与经验证的 Homebrew 机制，将型号、固件和底层实现差异归一化为稳定 Baga 语义。

---

## 2. Version History

| Version | Status | Summary | Reason |
|---|---|---|---|
| `v001` | Planned | Base Adapter：probe/profile/quirk/capability/display/input/storage/lifecycle/power/self-test | 首个 Kindle Adapter 任务设计 |

---

## 3. Dependency Gate

进入功能实现前需要：

```text
TASK-0010 K0 Base Contract baseline available
TASK-0020 K1 pinned kindlehf substrate bring-up evidence available
```

K0/K1 Gate 未通过时，本 Task 只允许研究与测试准备，不建立独立私有 Contract。

---

## 4. Authority / Inputs

```text
docs/zh-CN/standards/07_设备适配器规范.md
docs/zh-CN/standards/11_Kindle适配规范.md
docs/zh-CN/reference-apps/03_Kindle具体实现架构冻结.md
docs/zh-CN/design/02_设备适配器可执行契约与SDK设计.md
```

---

## 5. Current Design

当前设计来源：

```text
v001/0000_任务设计总纲_Task-Design-Overview.md
```

真机证据若要求改变 profile/quirk 分层、Base subsystem backend 或 Gate，应创建新版本。
