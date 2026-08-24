# Baga Ink 平台移植任务包目录规则 / Baga Ink Platform Port Task Package Rule

> **文档级别：Implementation Plan Directory Rule / 平台移植计划目录规则**  
> **状态：Mandatory Naming Rule v1.0**  
> **日期：2026-08-24**  
> **适用范围：`docs/plans/platform-ports/` 及未来所有设备/OS 平台子目录**

---

## 0. 核心目标

Platform Port 的任务资料采用便于 GitHub 浏览和实现 Agent 连续阅读的自包含任务包。每个实现版本把研究、差距、裁决、实现计划、Write Scope、测试矩阵、真机验证和执行入口放在同一个扁平目录中，不再拆成 `Task ID → Task Version → Execution Prompt` 镜像树。

```text
docs/plans/platform-ports/<platform>/
├── 0000_...md
├── 0010_...md
└── task/
    └── YYYY-MM-DD_<task-slug>/
        └── vN/
            └── vN.M/
                ├── 00_vN.M_总控_....md
                ├── 01_vN.M_....md
                ├── 02_vN.M_....md
                ├── ...
                ├── 18_vN.M_下一位AI直接执行Prompt.md
                └── 19_vN.M_....md
```

---

# 1. 命名规则

Platform Port 根目录的长期 Plan/Rule 文档继续使用：

```text
NNNN_中文名_English-Name.md
```

Task Package 内部采用：

```text
NN_vN.M_<语义标题>.md
```

例如：

```text
00_v1.1_总控_范围边界与执行纪律.md
01_v1.1_KOReader与Kindle实现链路研究基线.md
13_v1.1_分批实施计划与WriteScope.md
14_v1.1_RED_GREEN测试与验收矩阵.md
18_v1.1_下一位AI直接执行Prompt.md
19_v1.1_源码核验后逐项自检表.md
```

Task Package 文件名不强制中英双语并列。该区域属于快速变化的公开工程施工资料，语义标题优先保证目录可扫描性。稳定公共结论仍应提升到 `docs/en/` 与 `docs/zh-CN/` 的长期文档。

---

# 2. Task Package 与 Version

Task Package 根目录：

```text
YYYY-MM-DD_<lowercase-kebab-slug>/
```

版本结构：

```text
v1/
└── v1.1/

v2/
└── v2.1/
```

`vN.M/` 是可直接交付给实现 Agent 的具体任务版本。目录内部必须扁平，不再创建 `task/`、`execution-prompts/`、`handoff/` 或其他子目录。需要保留新的设计版本时，新建新的 `vN.M`，不覆盖历史版本。

---

# 3. 推荐文档职责

大型实现任务 SHOULD 覆盖以下职责；编号可按任务需要调整：

```text
00  总控 / Scope / 执行纪律 / 阅读顺序
01  上游源码与实现链路研究
02  当前仓库现状与差距
03  实现裁决
04  目录结构与模块边界
05+ 各 Milestone 实现计划
13  Batch / Write Scope
14  RED/GREEN 测试与验收矩阵
15  真机验证 / Evidence / Recovery
16  Dependency / License / Patch / Build Assets
17  实现前最终裁决
18  下一位 AI 直接执行入口
19  逐项自检表 / 覆盖矩阵
```

`00` 是强制入口。实现者不应依赖提交时间或目录外的临时说明判断当前任务。

---

# 4. 不再建立独立 Execution Prompt 树

Platform Port 不再使用：

```text
task/<Task-ID>/vNNN/
execution-prompts/<same Task-ID>/vNNN/
```

执行入口直接位于当前 Task Package，例如：

```text
18_v1.1_下一位AI直接执行Prompt.md
```

Batch 写范围与测试门禁分别进入同一目录中的对应编号文档。一个实现 Agent 定位到一个 `vN.M` 目录即可获得完整上下文。

---

# 5. 权威边界

```text
Standards
  > Approved Design / Architecture Freeze
  > Platform Master Plan
  > current Task Package
  > implementation / tests / device evidence
```

Task Package 可以固定本轮实现选择，但不能静默改变上位公共 Contract。实现证据要求改变上位语义时，应先或同步修订对应长期文档。

---

# 6. 自动校验

所有修改必须通过：

```bash
python3 tools/check_platform_port_plans.py
python3 tools/check_public_writing.py
```

创建新 Task Package 可使用：

```bash
python3 tools/new_platform_port_task.py <platform> <YYYY-MM-DD> <slug> <vN> <vN.M>
```

校验器检查 package naming、`vN/vN.M` 层级、版本目录扁平性、`NN_vN.M_*` 文件名一致性、`00` 总控存在性和编号唯一性。

---

# 7. 最终原则

```text
进入一个 vN.M 目录
→ 从 00 开始
→ 按编号读完研究、差距、裁决、实现与测试
→ 从 Batch 0 开始执行
→ 证据回写同一任务体系
```

目录本身就是实现导航，不再要求在多套索引和镜像树之间重建上下文。
