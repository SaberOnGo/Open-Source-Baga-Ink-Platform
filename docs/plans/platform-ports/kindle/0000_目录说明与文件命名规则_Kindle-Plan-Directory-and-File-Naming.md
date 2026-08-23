# Kindle 实现计划目录说明与文件命名规则 / Kindle Plan Directory and File Naming

> **文档级别：Implementation Plan Directory Rule / 任务目录规则**  
> **状态：Mandatory Naming Rule v0.3**  
> **日期：2026-08-23**  
> **适用范围：`docs/plans/platform-ports/kindle/` 及其全部子目录**  
> **上位规则：`../0000_平台移植计划目录与文件命名规则_Baga-Ink-Platform-Port-Plan-Naming.md`**

---

## 0. Kindle 目录的长期结构

Kindle Port 后续会产生大量功能实现、测试、调试、验证、真机操作、兼容性与恢复任务。为了避免“总计划、任务设计、AI 执行子步骤”混在一起，本目录固定分成三层：

```text
docs/plans/platform-ports/kindle/
├── 0000_目录说明与文件命名规则_Kindle-Plan-Directory-and-File-Naming.md
├── 0010_Kindle实现任务总计划_Baga-Ink-Kindle-Implementation-Master-Plan.md
│
├── task/
│   └── ...
│
└── execution-prompts/
    └── ...
```

其中：

```text
Kindle Implementation Master Plan
→ Kindle Port 的长期路线图 / Milestone / 依赖与 Gate

/task
→ 每次准备真正实现某个功能、模块或验证目标前，人与 AI 先讨论并确定的任务设计总纲

/execution-prompts
→ AI 根据 /task 中某个精确版本生成的具体执行子步骤文档
```

`execution-prompts/` 对应旧 LifeBookProject 的 `prompt/ai_prompt` 用途，但这里采用更明确的名称，强调这些文档是**可执行步骤**，不是泛用 Prompt 收藏。

---

# 1. 文件名硬规则

本目录及所有子目录中的 Markdown 文件 MUST 使用：

> **`数字前缀_中文名_英文名.md`**

格式：

```text
<数字前缀>_<中文名>_<English-Name>.md
```

正确：

```text
0000_任务设计总纲_Task-Design-Overview.md
0010_锁定KOReader上游版本_Pin-KOReader-Upstream-Version.md
0020_验证kindlehf原生构建_Verify-KindleHF-Native-Build.md
0030_运行真机睡眠唤醒测试_Run-Device-Sleep-Wake-Test.md
```

禁止：

```text
README.md
0010_Task.md
0010_Pin-KOReader.md
0010_锁定KOReader.md
```

即：数字、中文名、英文名三部分都必须存在。

新的大规模目录 MUST 使用四位零填充：

```text
0000_
0010_
0020_
0030_
...
```

默认按 10 递增，以便后续插入 `0015_` 等步骤。

---

# 2. `/task` 的职责

`task/` 保存的是：

> **先通过人与 AI 的讨论、研究和设计，明确“这一次要实现什么、为什么这样实现、怎样验证”的任务设计总纲。**

每次开始一个新的明确工作目标时，先在 `task/` 新建一个 Task 目录。

Task 可以以任何真正工程目标为单位，包括：

```text
实现一个功能
实现一个模块
做一次架构 PoC
修一个复杂问题
建立一套测试
调试真实设备问题
跑一轮兼容性验证
做真机操作与证据采集
建立恢复/回滚流程
```

Task 目录 MUST 使用：

```text
<四位Task编号>_<中文任务名>_<English-Task-Name>/
```

例如：

```text
task/
├── 0000_任务设计目录说明_Task-Design-Directory-Guide.md
├── 0010_适配器契约可执行化_Executable-Adapter-Contract/
├── 0020_KOReader-KindleHF启动验证_KOReader-KindleHF-Bringup/
├── 0030_Kindle基础设备适配器_Kindle-Base-Device-Adapter/
└── 0040_最小平台与Probe应用_Minimal-Platform-and-Probe-App/
```

这个四位 Task 编号是稳定 ID；一旦建立不得因为优先级、完成状态或版本变化而重编号。

---

# 3. 一个 Task 可以有多个版本

Task 设计会持续更新，因此 Task 目录内部使用：

```text
v001/
v002/
v003/
...
```

而不是：

```text
v1/
v2/
v10/
```

这样文件系统排序稳定。

推荐结构：

```text
task/
└── 0020_KOReader-KindleHF启动验证_KOReader-KindleHF-Bringup/
    ├── 0000_任务版本索引_Task-Version-Index.md
    ├── v001/
    │   ├── 0000_任务设计总纲_Task-Design-Overview.md
    │   ├── 0010_验收标准_Acceptance-Criteria.md
    │   └── 0020_真机验证计划_Real-Device-Validation-Plan.md
    └── v002/
        ├── 0000_任务设计总纲_Task-Design-Overview.md
        └── ...
```

Task Version 应在以下情况新建：

```text
范围改变
核心方案改变
依赖/前置改变
验收 Gate 改变
真机实测否定了原方案
测试/调试/恢复设计发生重要变化
```

普通执行进度、单个 bug 修复、某个 Prompt 完成，不需要自动创建新 Task Version。

旧版本 MUST 保留，不覆盖历史。

---

# 4. `/execution-prompts` 的职责

`execution-prompts/` 保存 AI 真正执行 Task 时生成的细分步骤。

它不是 Task Design 的替代物。

正确关系：

```text
讨论 / 研究
   ↓
task/<Task-ID>/vNNN
   ↓
冻结本轮任务设计
   ↓
AI 分解
   ↓
execution-prompts/<same-Task-ID>/vNNN/*.md
   ↓
逐份执行
   ↓
代码 / 测试 / 调试 / 真机证据
```

每一份 execution prompt SHOULD 足够具体，使新的 AI / Codex 在读取上位 Task 和必要源码后，可以执行一个明确子步骤并得到可验证结果。

执行步骤可以是：

```text
创建/修改代码
先写失败测试
运行构建
分析日志
修复一个具体故障
制作测试 fixture
执行模拟器验证
执行 Kindle 真机测试
采集版本/设备证据
回归验证
整理结果与 handoff
```

---

# 5. `/task` 与 `/execution-prompts` 必须一一镜像

相同 Task MUST 使用相同目录名：

```text
task/
└── 0030_Kindle基础设备适配器_Kindle-Base-Device-Adapter/

execution-prompts/
└── 0030_Kindle基础设备适配器_Kindle-Base-Device-Adapter/
```

版本也必须镜像：

```text
task/.../v002/
        ↕ exact source
execution-prompts/.../v002/
```

一个 `v001` prompt 不允许静默改去执行 `v002` 的任务设计。

如果执行过程中发现上位 Task Design 必须变化：

```text
停止把新架构决定继续塞进 prompt
        ↓
回到 task/
        ↓
建立 v002 / v003
        ↓
重新生成对应 execution-prompts version
```

这样才能知道任何一份 AI 执行文档究竟基于哪一版任务设计。

---

# 6. Execution Prompt 的目录与编号

推荐：

```text
execution-prompts/
├── 0000_AI执行提示目录说明_AI-Execution-Prompt-Directory-Guide.md
└── 0020_KOReader-KindleHF启动验证_KOReader-KindleHF-Bringup/
    ├── v001/
    │   ├── 0000_执行索引_Execution-Index.md
    │   ├── 0010_锁定KOReader与koreader-base版本_Pin-KOReader-Dependencies.md
    │   ├── 0020_建立依赖许可证清单_Create-Dependency-License-Manifest.md
    │   ├── 0030_验证kindlehf原生构建_Verify-KindleHF-Native-Build.md
    │   ├── 0040_建立Baga启动入口_Create-Baga-Launch-Entry.md
    │   └── 0050_执行Kindle真机启动测试_Run-Kindle-Device-Launch-Test.md
    └── v002/
        └── ...
```

`0000_` 保留给本版本执行索引；真正执行步骤通常从 `0010_` 开始。

如果中间需要插入新步骤，可以：

```text
0030_
0035_新增诊断步骤_Add-Diagnostic-Step.md
0040_
```

不用重命名后面几百份文件。

---

# 7. 每份 Execution Prompt 必须写明上位来源

每份执行文档开头 SHOULD 至少记录：

```text
Task ID
Source Task Path
Source Task Version
Prompt ID / Path
Goal
Dependencies / Preconditions
Files / Device involved
Verification / Acceptance
```

例如：

```text
Task: TASK-0020
Source: docs/plans/platform-ports/kindle/task/0020_KOReader-KindleHF启动验证_KOReader-KindleHF-Bringup/v001/
Prompt: PROMPT-0030
```

这样即使 AI 只拿到单个 Prompt，也能重新找到它的完整任务设计来源。

---

# 8. Kindle Master Plan 与 Task 的关系

K0–K7 继续作为 Kindle 长期 Milestone / Roadmap 语言，但**不再要求直接创建 `K0_adapter-contract/`、`K1_koreader-bringup/` 这类任务文档目录**。

正确做法是：

```text
Master Plan: K0 / K1 / K2 / ...
        ↓
按真正可执行的功能/模块目标
        ↓
task/0010_.../
task/0020_.../
task/0030_.../
        ↓
每个 Task 再有 v001/v002/...
        ↓
execution-prompts 镜像生成执行步骤
```

一个 Milestone 可以包含多个 Task；一个 Task SHOULD 尽量有清晰、可验证的单一工程目标。

因此本文规则覆盖早期 Master Plan 中直接建立 `K0_* / K1_*` 文档目录的示例；K0–K7 保留为逻辑 Milestone，不作为强制物理目录结构。

---

# 9. 状态与历史

不要通过文件改名表达完成状态：

```text
DONE_0030_...
COMPLETE_0040_...
```

禁止。

Task / Prompt 的路径与编号是稳定定位符。

完成结果应写入：

```text
Prompt Result / Evidence
Task 验收记录
代码 / 测试 / Commit
真实 Kindle evidence
Compatibility / BICTS evidence
docs/status/00_当前项目状态_Baga-Ink-Project-Status.md
```

---

# 10. 最终工作流

以后每次开始一项 Kindle 实现工作，默认流程是：

```text
1. 从 Standards / Design / Master Plan 确认边界
        ↓
2. 在 task/ 新建一个双语编号 Task 目录
        ↓
3. 与 AI 讨论并形成 task/<Task>/v001
        ↓
4. 任务设计需要更新时形成 v002 / v003
        ↓
5. 选定本轮精确 Task Version
        ↓
6. AI 在 execution-prompts/<same Task>/<same version>/ 生成细步骤
        ↓
7. 按编号逐步实现 / 测试 / 调试 / 真机验证
        ↓
8. 记录 Result / Evidence
        ↓
9. 若发现上位设计需改变，回到 task/ 新版本
        ↓
10. 完成 Gate 后回写 Status / Compatibility
```

这个结构允许 Kindle 实现长期积累数百个 Task、数千份 execution prompt，而不会失去“为什么做、基于哪一版设计、执行到了哪一步”的追踪关系。

---

# 11. 自动校验与 AI 禁止绕过

Kindle 目录同样由以下脚本自动校验：

```text
tools/check_platform_port_plans.py
```

任何 AI / 开发者修改本目录后，在宣称完成前 MUST 执行：

```bash
python3 tools/check_platform_port_plans.py
```

GitHub CI Gate：

```text
.github/workflows/platform-port-plan-guard.yml
```

会拒绝包括但不限于：

```text
乱建 K0_* / K1_* 物理任务目录
另建 prompt/、ai_prompt/、handoff/、scratch/、temp/、notes/ 等平行执行目录
Task 目录没有四位编号
文件只有中文或只有英文
README.md
v1 / v2 / v10
execution-prompts 没有对应 task
execution version 没有对应 Task Design version
Task 没有版本索引
Task Version 没有任务设计总纲
Execution Version 没有执行索引
```

AI MUST NOT 为了让自己的错误结构通过而：

```text
删除或跳过脚本
修改 CI 让它不运行
增加忽略规则
把非法目录加入 allowlist
把 MUST 改成 SHOULD
```

如果未来确实需要改变目录模型，必须先修改：

```text
上位 platform-ports 命名规则
本 Kindle 规则
AGENTS.md
validator / CI
```

经明确设计后，才允许创建新的目录类型。
