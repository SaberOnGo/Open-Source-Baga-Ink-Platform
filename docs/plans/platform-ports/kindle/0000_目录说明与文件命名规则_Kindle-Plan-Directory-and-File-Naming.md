# Kindle 实现计划目录说明与文件命名规则 / Kindle Plan Directory and File Naming

> **文档级别：Implementation Plan Directory Rule / Kindle 任务目录规则**  
> **状态：Mandatory Naming Rule v1.0**  
> **日期：2026-08-24**  
> **适用范围：`docs/plans/platform-ports/kindle/` 及其全部子目录**  
> **上位规则：`../0000_平台移植计划目录与文件命名规则_Baga-Ink-Platform-Port-Plan-Naming.md`**

---

## 0. Kindle 任务资料结构

Kindle Port 使用一个长期 Master Plan，加若干按日期建立、按版本演进的自包含 Task Package：

```text
docs/plans/platform-ports/kindle/
├── 0000_目录说明与文件命名规则_Kindle-Plan-Directory-and-File-Naming.md
├── 0010_Kindle实现任务总计划_Baga-Ink-Kindle-Implementation-Master-Plan.md
└── task/
    └── 2026-08-24_kindle-platform/
        └── v1/
            └── v1.1/
                ├── 00_v1.1_总控_范围边界与执行纪律.md
                ├── 01_v1.1_KOReader与Kindle实现链路研究基线.md
                ├── ...
                ├── 18_v1.1_下一位AI直接执行Prompt.md
                └── 19_v1.1_源码核验后逐项自检表.md
```

不再维护独立 `execution-prompts/`，也不再把 K0–K7 分成八个需要分别进入 `TASK-NNNN/vNNN` 的目录。

---

# 1. Kindle Task Package 的组织原则

一个 Kindle 实现版本是一个完整任务包。K0–K7 是同一个实现路线中的 Milestone，在当前 `vN.M` 目录内分别由编号文档描述。

这样可以直接得到：

```text
00  总控
01  上游研究
02  仓库差距
03  关键实现裁决
04  代码模块边界
05  K0
06  K1
07  K2
08  K3
09  K4
10  K5
11  K6
12  K7
13  Batch / Write Scope
14  RED/GREEN tests
15  Real-device evidence / recovery
16  Dependencies / licenses / patches / build assets
17  Pre-implementation rulings
18  Direct AI execution prompt
19  Final checklist
```

单个 Milestone 的方案发生变化时，优先修订当前任务包并形成新的 `vN.M`，而不是再创建一套平行 Task 树。

---

# 2. 当前 Kindle 实现任务包

当前首个完整任务包：

```text
docs/plans/platform-ports/kindle/task/
└── 2026-08-24_kindle-platform/
    └── v1/
        └── v1.1/
```

首轮工程重点仍是：

```text
K0  Adapter Contract 可执行基础
+
K1  pinned KOReader / kindlehf bring-up
```

K2–K7 的计划同时保存在同一个版本目录中，便于理解全链路和后续依赖，但不得绕过前置 Gate 提前实施。

---

# 3. 文件命名

Kindle 根目录长期文档：

```text
NNNN_中文名_English-Name.md
```

Task Package 内：

```text
NN_vN.M_<语义标题>.md
```

Task Package 的语义标题可以使用中文和稳定技术标识，例如：

```text
05_v1.1_K0_AdapterContract可执行化计划.md
06_v1.1_K1_KOReaderKindleHF启动计划.md
14_v1.1_RED_GREEN测试与验收矩阵.md
```

---

# 4. 实现 Agent 阅读规则

实现工作开始时，先定位当前 `vN.M` 任务包，不再遍历旧 Task ID。

当前 v1.1 的入口顺序：

```text
00 → 01 → 02 → 03 → 04 → 13 → 14 → 17 → 19
```

需要执行时再读取：

```text
05–12  对应 Milestone 计划
15     真机与恢复
16     上游依赖
18     直接执行入口
```

`00` 和 `17` 的当前裁决优先于本任务包中的早期研究描述；如果证据推翻裁决，先形成新的任务包版本再继续实现。

---

# 5. 第一阶段真机与版本原则

首台 Bring-up 基线：

```text
Homebrew-ready real Kindle
firmware >= 5.16.3
native target = kindlehf
```

先跑通 `kindlehf`，再按 Compatibility evidence 扩展 `kindlepw2 → kindle → kindle-legacy`。具体 model + firmware + native target 必须分别保留证据，不以相似型号推断 Compatible。

---

# 6. 校验

Kindle Task Package 必须通过：

```bash
python3 tools/check_platform_port_plans.py
python3 tools/check_public_writing.py
```

创建新版本包可使用：

```bash
python3 tools/new_platform_port_task.py kindle <YYYY-MM-DD> <slug> <vN> <vN.M>
```
