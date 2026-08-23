# TASK-0020 任务版本索引 / Task Version Index

> **Task ID：`TASK-0020`**  
> **任务：KOReader KindleHF 启动验证 / KOReader KindleHF Bring-up**  
> **关联 Milestone：K1**  
> **当前选定版本：`v001`**  
> **状态：Selected Planning Baseline**  
> **日期：2026-08-23**

---

## 1. Task 目标

在一台真实、Homebrew-ready、firmware >= 5.16.3 的 `kindlehf` 设备上，锁定并验证 Baga 私有采用的 KOReader/koreader-base/FBInk substrate，并建立可重复的 Baga-controlled development entry。

目标是证明 Kindle 上的基础启动环境可由 Baga Platform 受控使用，而不是把 KOReader 作为面向 IKP App 的公共 API。

---

## 2. Version History

| Version | Status | Summary | Reason |
|---|---|---|---|
| `v001` | Selected | upstream pin、native bring-up、Baga private entry PoC、诊断与真机证据 | 首个 Kindle 真机 bring-up 版本 |

---

## 3. Authority / Inputs

```text
docs/zh-CN/standards/11_Kindle适配规范.md
docs/zh-CN/reference-apps/03_Kindle具体实现架构冻结.md
docs/zh-CN/standards/13_标准库与成熟组件采用规范.md
docs/plans/platform-ports/kindle/0010_Kindle实现任务总计划_Baga-Ink-Kindle-Implementation-Master-Plan.md
```

---

## 4. Preconditions

首个验证设备基线：

```text
real Kindle
Homebrew-ready
firmware >= 5.16.3
native target: kindlehf
```

已安装的 KPM/sh_integration 可以作为开发便利条件，但 K1 的核心 bring-up 不依赖最终 `.kpkg` 产品化流程。

---

## 5. Current Selected Version

当前设计来源：

```text
v001/0000_任务设计总纲_Task-Design-Overview.md
```

如真机证据推翻 private entry 方案、upstream pin 策略、日志/恢复方案或验收 Gate，应建立 `v002`。

---

## 6. Downstream

通过后为以下 Task 提供真实 substrate 证据：

```text
TASK-0030 Kindle Base Device Adapter
TASK-0040 Minimal Platform Core + Probe IKP
TASK-0070 KPM Packaging + Kindle Home Entry
```
