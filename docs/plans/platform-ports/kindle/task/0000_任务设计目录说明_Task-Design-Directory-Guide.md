# Kindle 任务设计目录说明 / Kindle Task Design Directory Guide

> **目录：`docs/plans/platform-ports/kindle/task/`**  
> **状态：Mandatory Task Design Workflow v0.1**  
> **日期：2026-08-23**

---

## 0. 这个目录保存什么

`task/` 保存的不是 AI 最终执行步骤，而是：

> **每次准备实现一个明确功能、模块、测试、调试、验证或真机目标之前，人与 AI 先讨论、研究并确定的任务设计总纲。**

它回答：

```text
为什么做？
做什么？
不做什么？
依赖什么？
准备怎样实现？
怎样测试？
怎样调试？
是否需要真实 Kindle？
怎样验收？
失败怎样恢复？
```

一旦 Task Design 选定某个版本，AI 才能据此生成 `../execution-prompts/` 中的执行步骤。

---

# 1. 每个工程目标先建一个 Task 目录

格式：

```text
<四位Task编号>_<中文任务名>_<English-Task-Name>/
```

例如：

```text
0010_适配器契约可执行化_Executable-Adapter-Contract/
0020_KOReader-KindleHF启动验证_KOReader-KindleHF-Bringup/
0030_Kindle基础设备适配器_Kindle-Base-Device-Adapter/
0040_最小平台与Probe应用_Minimal-Platform-and-Probe-App/
```

Task ID 一旦建立保持稳定。

Task 的粒度以“一个清晰工程目标”为准，不要求与 K0/K1/K2 一一对应；一个 Kindle Milestone 可以包含多个 Task。

---

# 2. 每个 Task 都是版本化设计

推荐：

```text
0010_某任务_Some-Task/
├── 0000_任务版本索引_Task-Version-Index.md
├── v001/
│   ├── 0000_任务设计总纲_Task-Design-Overview.md
│   ├── 0010_验收标准_Acceptance-Criteria.md
│   └── 0020_真机验证计划_Real-Device-Validation-Plan.md
├── v002/
│   └── ...
└── v003/
    └── ...
```

版本目录 MUST 使用：

```text
v001
v002
v003
...
```

旧版本不删除、不覆盖。

---

# 3. Task 版本索引

每个 Task 根目录 SHOULD 创建：

```text
0000_任务版本索引_Task-Version-Index.md
```

记录：

```text
Task ID
Task Name
Current Selected Version
Version History
Each version status
Reason for new version
Related Milestone
Related Standards / Design / Freeze
```

示例：

```text
v001  Initial design
v002  Revised after real Kindle launch evidence
v003  Revised acceptance gate after sleep/wake regression
```

不要用“最近修改时间”猜当前该执行哪个版本。

---

# 4. `0000_任务设计总纲` 的最低内容

每个版本 MUST 至少有：

```text
0000_任务设计总纲_Task-Design-Overview.md
```

建议包含：

```text
Task ID / Version
Goal
Background / Problem
Authority / Standards / Design inputs
Scope
Out of Scope
Dependencies / Preconditions
Current evidence
Implementation design
Files / modules involved
Test strategy
Debug strategy
Real-device operations
Data protection / rollback
Acceptance gate
Known risks
Open questions
Expected execution-prompt groups
```

这里允许描述完整方案，但不要把数百个微小执行步骤都塞进总纲。

---

# 5. 什么时候建立新版本

以下变化 SHOULD 创建新版本：

```text
任务范围明显变化
核心实现方案变化
依赖方案变化
测试策略发生结构性变化
真机证据推翻原假设
验收 Gate 改变
恢复/回滚策略改变
需要修改本轮执行顺序的总体结构
```

以下通常不需要新版本：

```text
某个 prompt 已完成
单个测试从 RED 变 GREEN
修正拼写
补充一次日志结果
代码实现中的普通小调整
```

---

# 6. Task Version 与 Execution Prompts 的关系

只有精确选定版本以后，才生成：

```text
../execution-prompts/<same Task directory>/<same vNNN>/
```

例如：

```text
task/
└── 0020_KOReader-KindleHF启动验证_KOReader-KindleHF-Bringup/
    └── v002/

execution-prompts/
└── 0020_KOReader-KindleHF启动验证_KOReader-KindleHF-Bringup/
    └── v002/
```

执行 prompt MUST 指向这一个精确来源。

如果执行过程中发现 Task Design 必须改变，不应继续在旧 prompt 中扩写新架构；应返回本目录创建 `v003`，再生成对应的新 execution prompts。

---

# 7. 文件命名

本目录所有 Markdown 文件 MUST：

```text
数字前缀_中文名_英文名.md
```

例如：

```text
0000_任务版本索引_Task-Version-Index.md
0000_任务设计总纲_Task-Design-Overview.md
0010_验收标准_Acceptance-Criteria.md
0020_真机验证计划_Real-Device-Validation-Plan.md
0030_故障恢复设计_Failure-Recovery-Design.md
```

不要创建：

```text
README.md
plan.md
task-v2.md
0010_Test.md
```

---

# 8. 真机任务也属于 Task Design

Kindle 实现中，以下都可以成为独立 Task：

```text
kindlehf 首次 bring-up
屏幕刷新实测
输入映射验证
睡眠/唤醒稳定性验证
KPM 安装与升级验证
Home Entry 真机验证
某一型号/固件 Compatibility 验证
数据保护/恢复演练
```

Task Design 必须明确：

```text
设备型号
固件版本
Homebrew 状态
前置备份
需要执行的设备动作
可能风险
失败恢复步骤
需要保留的证据
```

不要把真实设备实验写成没有来源的临时聊天指令。

---

# 9. 最终原则

`task/` 是：

> **“这一次工程工作到底准备怎么做”的版本化、可追溯、可讨论的设计来源。**

它比 execution prompt 更稳定，但低于 Standards / Design / Architecture Freeze。

正确链：

```text
Standards / Design / Freeze
        ↓
Kindle Master Plan
        ↓
Task Design vNNN
        ↓
Execution Prompts
        ↓
Implementation / Tests / Device Evidence
```
