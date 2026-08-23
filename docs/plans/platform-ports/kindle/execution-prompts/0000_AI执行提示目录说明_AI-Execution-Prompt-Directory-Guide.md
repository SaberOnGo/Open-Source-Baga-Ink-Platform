# Kindle AI 执行提示目录说明 / Kindle AI Execution Prompt Directory Guide

> **目录：`docs/plans/platform-ports/kindle/execution-prompts/`**  
> **状态：Mandatory Execution Prompt Workflow v0.1**  
> **日期：2026-08-23**

---

## 0. 这个目录保存什么

`execution-prompts/` 保存的是：

> **AI 根据 `../task/` 中某个已经选定的 Task Version，进一步拆出的可独立执行、测试、调试、验证或真机操作子步骤。**

它对应旧 LifeBookProject 中 `prompt/ai_prompt` 的用途，但这里不再把所有 prompt 平铺在一个目录中，而是按：

```text
Task ID
→ Task Version
→ Execution Prompt Number
```

三层关系组织。

---

# 1. 必须镜像 `/task`

如果 Task 是：

```text
../task/0020_KOReader-KindleHF启动验证_KOReader-KindleHF-Bringup/v002/
```

那么它生成的执行文档 MUST 放在：

```text
0020_KOReader-KindleHF启动验证_KOReader-KindleHF-Bringup/v002/
```

完整路径：

```text
docs/plans/platform-ports/kindle/execution-prompts/
└── 0020_KOReader-KindleHF启动验证_KOReader-KindleHF-Bringup/
    └── v002/
```

不得使用另一套 Task 编号、另一套目录名或模糊的日期目录来代替这个映射。

---

# 2. 每个版本先建执行索引

推荐：

```text
<same Task>/vNNN/
├── 0000_执行索引_Execution-Index.md
├── 0010_....md
├── 0020_....md
├── 0030_....md
└── ...
```

`0000_执行索引_Execution-Index.md` SHOULD 记录：

```text
Task ID
Source Task Version
Execution goal
Prompt list
Prompt dependencies
Parallelizable prompts
Prompts requiring real device
Blocked / completed status summary
Final gate
```

这样即使某个 Task Version 生成数百份执行文档，也不需要靠文件修改时间猜执行顺序。

---

# 3. 每份 Prompt 是一个明确子步骤

一份 execution prompt SHOULD 尽量只完成一个可验证的子目标，例如：

```text
建立 IDL schema loader
写第一组失败测试
实现 Display contract codegen
编译 kindlehf target
采集真实 Kindle 启动日志
验证 sleep/wake event mapping
修复一个明确的 path-containment regression
运行一组 BICTS 子集
```

不要把整个大型 Task 又复制成一份巨大 prompt。

目标是使：

```text
Prompt
→ 执行
→ 验证
→ 记录结果
```

形成小闭环。

---

# 4. 文件名强制格式

本目录所有 Markdown 文件 MUST 使用：

```text
<数字前缀>_<中文名>_<English-Name>.md
```

例如：

```text
0000_执行索引_Execution-Index.md
0010_锁定KOReader与koreader-base版本_Pin-KOReader-Dependencies.md
0020_建立依赖许可证清单_Create-Dependency-License-Manifest.md
0030_验证kindlehf原生构建_Verify-KindleHF-Native-Build.md
0040_建立Baga启动入口_Create-Baga-Launch-Entry.md
0050_执行Kindle真机启动测试_Run-Kindle-Device-Launch-Test.md
```

禁止：

```text
1-handoff.md
100-260414-plan-v1.md
README.md
prompt1.md
0010_Build.md
```

也就是说，旧 LifeBookProject 中那种“数字 + 日期 + 英文描述”的命名方式不在这里沿用。

---

# 5. 编号规则

默认：

```text
0000_  执行索引
0010_  第一个执行步骤
0020_  第二个执行步骤
0030_  第三个执行步骤
...
```

按 10 递增，方便后续插入：

```text
0030_原步骤
0035_后来补充的诊断步骤_Added-Diagnostic-Step.md
0040_原步骤
```

编号是当前 Task Version 内的稳定 Prompt ID，不表示完成状态。

---

# 6. 每份 Prompt 必须写明 Source Task

每份执行文档开头 SHOULD 至少包含：

```text
Task ID
Source Task Path
Source Task Version
Prompt ID
Goal
Dependencies / Preconditions
Files / Components
Device Requirements
Execution Steps
Tests / Verification
Acceptance
Result / Evidence
```

例如：

```text
Task ID: TASK-0020
Source Task: docs/plans/platform-ports/kindle/task/0020_KOReader-KindleHF启动验证_KOReader-KindleHF-Bringup/v002/
Prompt ID: PROMPT-0030
```

禁止只写：

```text
“按上一个聊天里的方案做”
“继续之前那个 Kindle 任务”
```

执行文档必须能够脱离聊天历史重新定位来源。

---

# 7. AI 可以生成很多 Prompt，但不能偷偷改 Task Design

AI 执行过程中可能发现：

```text
原方案不可行
依赖版本不兼容
真实 Kindle 行为与假设不同
验收标准需要调整
需要改变模块边界
```

如果只是实现细节，可以生成新的 execution prompt。

如果影响上位任务设计，则必须：

```text
停止扩大旧 version prompt
        ↓
回到 ../task/<Task>/
        ↓
建立新的 vNNN
        ↓
重新确认 Task Design
        ↓
再在 execution-prompts/<same Task>/<new vNNN>/ 生成新步骤
```

不得让 `v001` 的 execution prompt 最后变成事实上的 `v004` 方案。

---

# 8. 测试、调试、验证、真机操作都可以是 Prompt

Execution Prompt 不等于“写代码”。

它可以专门用于：

```text
测试
调试
日志分析
构建验证
静态检查
依赖验证
真机操作
睡眠/唤醒测试
刷新残影测试
安装/卸载验证
恢复演练
数据保护验证
BICTS / compatibility evidence
```

对于真实 Kindle 操作，Prompt SHOULD 写明：

```text
具体设备型号
固件
native target
Homebrew 状态
是否需要 USB / Wi-Fi
前置备份
操作步骤
停止条件
风险
恢复步骤
证据保存方式
```

---

# 9. Prompt 完成后不要重命名

不要把：

```text
0030_验证kindlehf原生构建_Verify-KindleHF-Native-Build.md
```

改成：

```text
DONE_0030_...
```

完成状态写在：

```text
Prompt Result / Evidence
0000_执行索引_Execution-Index.md
Task 验收记录
docs/status/
代码 / 测试 / Commit
```

这样路径永远稳定。

---

# 10. 推荐执行闭环

一份 Prompt 的理想生命周期：

```text
Read exact Task Version
        ↓
Check dependencies
        ↓
Execute one sub-goal
        ↓
Run verification
        ↓
Record Result / Evidence
        ↓
Update execution index
        ↓
Next prompt
```

如果失败：

```text
failure is implementation detail
→ create/execute diagnostic or fix prompt

failure invalidates Task Design
→ create new Task Version first
```

---

# 11. 最终原则

`execution-prompts/` 是：

> **“如何把某一版 Task Design 一步一步真正做完”的大规模 AI 执行层。**

它可以有几百、几千份文档，但每份都必须能追溯到：

```text
唯一 Task
+
精确 Task Version
+
稳定 Prompt 编号
+
明确验证结果
```

因此 Kindle 的长期工程链固定为：

```text
Master Plan
    ↓
Task Design vNNN
    ↓
Execution Prompts
    ↓
Code / Tests / Debug / Device Operations
    ↓
Evidence / Status / Compatibility
```
