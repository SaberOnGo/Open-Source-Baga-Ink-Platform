# TASK-0060 任务版本索引 / Task Version Index

> **Task ID：`TASK-0060`**  
> **任务：Kindle 阅读器 Provider / Kindle Reader Provider**  
> **关联 Milestone：K5**  
> **当前选定版本：`v001`**  
> **状态：Planned Baseline — dependency-gated**  
> **日期：2026-08-23**

---

## 1. Task 目标

在 Platform/Probe 基础链稳定后，把标准 `baga.reader` 能力映射到 Kindle Platform 内部采用的 KOReader ReaderUI / CREngine / MuPDF stack，而不是另写一套 EPUB/PDF 阅读器。

---

## 2. Version History

| Version | Status | Summary | Reason |
|---|---|---|---|
| `v001` | Planned | Reader bridge、EPUB/TXT/PDF、position/search/selection、lifecycle persistence | 首个 Kindle Reader Provider 任务设计 |

---

## 3. Dependency Gate

```text
TASK-0040 K3 Platform/Probe accepted
TASK-0050 K4 App lifecycle/install baseline accepted or stable enough for controlled reader tests
```

---

## 4. Authority / Inputs

```text
docs/zh-CN/standards/03_API规范.md
docs/zh-CN/standards/13_标准库与成熟组件采用规范.md
docs/zh-CN/standards/11_Kindle适配规范.md
docs/zh-CN/reference-apps/03_Kindle具体实现架构冻结.md
```

---

## 5. Current Design

```text
v001/0000_任务设计总纲_Task-Design-Overview.md
```

如 `baga.reader` 公共 Contract 需要新增稳定语义，应先修订上位 Standard/Design，再新建本 Task Version。
