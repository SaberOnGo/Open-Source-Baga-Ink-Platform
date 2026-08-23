# Baga Ink 平台移植计划目录与文件命名规则 / Baga Ink Platform Port Plan Naming

> **文档级别：Implementation Plan Directory Rule / 平台移植计划目录规则**  
> **状态：Mandatory Naming Rule v0.2**  
> **日期：2026-08-23**  
> **适用范围：`docs/plans/platform-ports/` 及未来所有设备/OS 平台子目录**

---

## 0. 核心规则

Baga Ink 未来会有 Kindle、Android E-Paper 以及其他设备/OS 家族的 Platform Port。每个平台都可能产生数百甚至数千份任务设计与 AI 执行文档。

因此，`docs/plans/platform-ports/` 下的 Markdown 文件统一采用：

> **数字前缀 + `_` + 中文名 + `_` + 英文名 + `.md`**

强制格式：

```text
<数字前缀>_<中文名>_<English-Name>.md
```

例如：

```text
0000_目录说明与文件命名规则_Platform-Port-Plan-Naming.md
0010_锁定上游依赖_Pin-Upstream-Dependencies.md
0020_建立依赖与许可证清单_Dependency-License-Manifest.md
0030_原生目标构建验证_Native-Target-Build-Bringup.md
```

禁止：

```text
README.md
Task.md
0010_Task.md
0010_Pin-Upstream-Dependencies.md
0010_锁定上游依赖.md
```

即：**只有数字前缀不够；中文名和英文名都必须存在。**

英文名 SHOULD 使用 ASCII 字母、数字与 `-`，避免空格。

---

# 1. Platform Port 的两层实施资料

每个大型 Platform Port SHOULD 采用两层结构：

```text
<platform>/
├── task/
└── execution-prompts/
```

含义：

```text
task/
→ 人与 AI 先讨论、研究并确定的“任务设计总纲”
→ 以实现一个明确功能/模块/验证目标为单位
→ 可以包含开发、测试、调试、验证、真机操作、回归、恢复等完整目标
→ 一个 Task 可以持续形成 v001 / v002 / ... / vNNN

execution-prompts/
→ AI 根据某个确定的 task/<Task>/vNNN 生成的具体执行步骤
→ 每份文档是一次可独立执行、验证和交接的子步骤
→ 数量可以达到数百、数千份
```

`execution-prompts` 相当于旧项目中的 `prompt/ai_prompt`，但名称明确强调：这里保存的是**由 Task Design 派生的执行指令**，不是聊天记录或泛用 Prompt 收藏。

---

# 2. Task 与 Execution Prompt 必须镜像

推荐结构：

```text
<platform>/
├── task/
│   ├── 0000_任务设计目录说明_Task-Design-Directory-Guide.md
│   └── 0010_适配器契约可执行化_Executable-Adapter-Contract/
│       ├── 0000_任务版本索引_Task-Version-Index.md
│       ├── v001/
│       │   └── 0000_任务设计总纲_Task-Design-Overview.md
│       └── v002/
│           └── 0000_任务设计总纲_Task-Design-Overview.md
│
└── execution-prompts/
    ├── 0000_AI执行提示目录说明_AI-Execution-Prompt-Directory-Guide.md
    └── 0010_适配器契约可执行化_Executable-Adapter-Contract/
        ├── v001/
        │   ├── 0000_执行索引_Execution-Index.md
        │   ├── 0010_建立IDL模式与加载器_Create-IDL-Schema-and-Loader.md
        │   └── 0020_编写失败基线测试_Write-Failing-Baseline-Tests.md
        └── v002/
            └── ...
```

硬规则：

1. `task/0010_.../` 与 `execution-prompts/0010_.../` MUST 使用同一个 Task 目录名；
2. execution prompt MUST 指向一个精确 Task Version，例如 `v002`；
3. 不允许让 `v001` 的执行文档静默改成执行 `v002` 的设计；
4. Task 设计变化时创建新版本，而不是覆盖历史版本；
5. 旧版本及其执行文档保留为实施历史。

---

# 3. Task 目录命名

真正代表一个功能/模块/验证目标的 Task 目录 SHOULD 采用：

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

Task 编号是稳定 ID。Task 完成、阻塞或后来出现新版本时，目录编号不得改变。

结构性目录名称，例如：

```text
task/
execution-prompts/
v001/
v002/
```

不受“中文名 + 英文名”文件命名规则约束；该规则针对 Markdown 文件名。Task 业务目录仍 SHOULD 使用上面的双语命名方式。

---

# 4. Version 目录统一使用 `vNNN`

为了避免：

```text
v1
v10
v2
```

这样的字符串排序问题，新 Task Version MUST 使用三位零填充：

```text
v001
v002
v003
...
v010
...
v999
```

Task 新版本表示**任务设计发生了值得保留的变化**，例如：

- 范围变化；
- 方案变化；
- 验收标准变化；
- 实测发现原方案不可行；
- 真机验证要求变化；
- 测试/恢复策略变化。

普通执行进度不产生新 Task Version。

---

# 5. Markdown 文件默认四位数字前缀

预计长期增长的目录 SHOULD 使用：

```text
0000_
0010_
0020_
0030_
...
9999_
```

`0000_` 通常保留给：

```text
目录说明
版本索引
任务设计总纲
执行索引
验收 Gate 总览
```

具体执行文档通常从：

```text
0010_
```

开始。

默认按 10 递增，为后续插入步骤保留编号：

```text
0010_
0020_
0030_
```

需要插入时可以使用：

```text
0015_
```

无需重命名后续大量文件。

现有已经满足“数字前缀 + 中文名 + 英文名”的历史文件可以保留原位；新文件必须遵守本规则。

---

# 6. 编号作用域

编号不要求整个仓库全局唯一，而是在当前目录 / 当前 Task 语境中稳定。

推荐理解：

```text
Task directory number
→ 这个功能/模块工作包的稳定 ID

Task version
→ 该工作包任务设计的版本

Execution prompt file number
→ 某个 Task Version 内具体执行步骤的稳定顺序
```

例如：

```text
Task:    0030_Kindle基础设备适配器_Kindle-Base-Device-Adapter/
Version: v002
Prompt:  0140_验证睡眠唤醒生命周期_Verify-Sleep-Wake-Lifecycle.md
```

可以形成稳定引用：

```text
TASK-0030 / v002 / PROMPT-0140
```

---

# 7. Execution Prompt 必须声明来源

每份 execution prompt SHOULD 在文档开头记录：

```text
Source Task
Source Task Version
Prompt ID / file path
Goal
Dependencies
Acceptance / verification
```

这样即使单独复制一份文档，也能知道它来自哪个任务设计版本。

如果执行过程中发现需要改变 Task 的架构、范围或验收 Gate，AI MUST 回到 `task/` 形成新版本，而不是在 execution prompt 中偷偷改变上位任务设计。

---

# 8. 完成状态不通过改文件名表达

不要创建：

```text
DONE_0010_....md
COMPLETE_0020_....md
```

也不要完成后重新编号。

编号是稳定定位符与阅读顺序；执行结果进入：

```text
execution prompt 自身的 Result / Evidence
Task 版本的验收记录
docs/status/00_当前项目状态_Baga-Ink-Project-Status.md
代码 / 测试 / Commit
Compatibility / BICTS evidence
```

---

# 9. 对所有未来 Platform Port 生效

未来创建：

```text
docs/plans/platform-ports/android-e-paper/
docs/plans/platform-ports/remarkable/
docs/plans/platform-ports/<future-family>/
```

时，默认继承：

```text
Task Design
      ↓
Versioned Task
      ↓
Execution Prompts
      ↓
Code / Test / Device Evidence
      ↓
Status / Compatibility
```

以及文件名：

> **`数字前缀_中文名_英文名.md`**

这套结构的目标是：即使未来单个平台积累数百个 Task、每个 Task 又派生大量 AI 执行文档，仍然能通过稳定 Task ID、版本号、文件编号和双语语义名快速定位。