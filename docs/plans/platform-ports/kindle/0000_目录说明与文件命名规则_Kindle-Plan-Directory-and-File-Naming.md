# Kindle 实现计划目录说明与文件命名规则 / Kindle Plan Directory and File Naming

> **文档级别：Implementation Plan Directory Rule / 任务目录规则**  
> **状态：Mandatory Naming Rule v0.1**  
> **日期：2026-08-23**  
> **适用范围：`docs/plans/platform-ports/kindle/` 及其全部子目录**

---

## 0. 核心规则

本目录未来可能包含数百甚至数千份 Kindle 实现任务、验证记录、PoC 计划和里程碑文档。

因此，从本规则建立起：

> **本目录及其所有子目录中的计划/任务 Markdown 文件名 MUST 使用“数字前缀 + 下划线 + 描述性文件名”的格式。**

即：

```text
<数字前缀>_<文件名>.md
```

禁止创建没有数字前缀的任务文档，例如：

```text
README.md
Task.md
Kindle-Bringup.md
Adapter-Test-Plan.md
```

正确形式：

```text
0000_目录说明与文件命名规则_Kindle-Plan-Directory-and-File-Naming.md
0010_K1里程碑计划_KOReader-Bringup.md
0020_锁定上游组件与依赖清单_Pin-Upstream-Components.md
0030_kindlehf构建验证_KindleHF-Build-Bringup.md
0040_Baga直接入口PoC_Baga-Direct-Entry-PoC.md
```

---

# 1. 默认使用 4 位数字前缀

新的细分任务目录 SHOULD 默认使用四位零填充编号：

```text
0000_
0010_
0020_
0030_
...
9999_
```

原因：

- 文件系统和 GitHub 页面按名称排序时顺序稳定；
- `0009_`、`0010_`、`0100_`、`1000_` 不会发生字符串排序错乱；
- 单个目录可容纳大量任务；
- 搜索、引用、口头沟通和 AI 定位都更容易；
- 不依赖创建时间或 Git 历史来判断任务顺序。

现有已创建、且已经满足“数字前缀 + `_`”的计划文件可以保留原编号；新创建的细分 Task 文档按本规则使用四位前缀。

---

# 2. 为什么默认按 10 递增

新任务正常使用：

```text
0010_
0020_
0030_
0040_
```

而不是连续使用：

```text
0001_
0002_
0003_
0004_
```

这是为了给后续插入任务留空间。

例如原来：

```text
0010_锁定KOReader版本.md
0020_建立依赖清单.md
```

后来发现两者中间必须增加一个验证任务，可以直接加入：

```text
0015_验证上游Commit可构建.md
```

不需要重命名后面数百份文件。

允许的插入编号包括：

```text
0011_
0012_
0015_
0018_
```

只要保证同一目录内编号清晰、唯一、顺序合理即可。

---

# 3. 每个目录独立编号

编号作用域是**当前目录**，不要求整个 Kindle Port 全局唯一。

例如：

```text
docs/plans/platform-ports/kindle/
├── 0000_目录说明与文件命名规则_....md
├── 00_Kindle实现任务总计划_....md
├── K0_adapter-contract/
│   ├── 0000_K0目录说明与里程碑计划_....md
│   ├── 0010_定义IDL-Schema_....md
│   ├── 0020_固化Root-Core-Types_....md
│   └── 0030_固化Display-Contract_....md
│
└── K1_koreader-bringup/
    ├── 0000_K1目录说明与里程碑计划_....md
    ├── 0010_锁定上游组件_....md
    ├── 0020_建立依赖清单_....md
    └── 0030_kindlehf构建验证_....md
```

因此即使 Kindle 实现最终产生数千份任务文档，也不需要把所有文件挤在一个巨大平铺目录中。

---

# 4. `0000_` 的保留用途

每个任务子目录 SHOULD 把：

```text
0000_
```

保留给该目录的：

```text
目录说明
Milestone 总计划
任务索引
本目录验收 Gate
```

例如：

```text
K2_kindle-adapter/
└── 0000_K2里程碑计划_Kindle-Base-Device-Adapter.md
```

具体执行任务从：

```text
0010_
```

开始。

---

# 5. 文件名必须同时表达“编号 + 任务含义”

数字编号只负责：

```text
排序
快速定位
引用
插入新任务
```

编号不能替代语义名称。

不要创建：

```text
0010_Task.md
0020_Todo.md
0030_Test.md
```

应使用可以脱离聊天上下文理解的名字，例如：

```text
0010_锁定KOReader与koreader-base版本_Pin-KOReader-Dependencies.md
0020_建立Kindle依赖与许可证清单_Kindle-Dependency-License-Manifest.md
0030_验证kindlehf原生构建_KindleHF-Native-Build-Bringup.md
0040_比较Baga直接入口与私有插件_Baga-Entry-PoC-Comparison.md
```

目标是让未来开发者或 AI 只看目录列表，就能大致知道任务是什么。

---

# 6. Task ID 与文件编号是两个概念

Milestone 中可以继续使用逻辑 Task ID：

```text
K0-01
K0-02
K1-01
K2-07
```

它用于架构计划、Issue、Commit、测试记录中的稳定引用。

文件名前缀则用于文件系统排序。

例如：

```text
Task ID: K1-04
File:    0040_Baga-Launch开发入口_Baga-Launch-Development-Entry.md
```

二者 SHOULD 在文档头部同时记录，但不要强迫文件编号与 `K1-04` 数值完全相同。

这样即使后来插入 `K1-03A` 类的新工程任务，也可以通过文件编号顺序自然插入，而无需破坏已有稳定 Task ID。

---

# 7. 文档内引用优先使用完整路径

正式 Plan / Task 文档引用另一份任务时 SHOULD 使用：

```text
docs/plans/platform-ports/kindle/K1_koreader-bringup/0030_kindlehf构建验证_KindleHF-Native-Build-Bringup.md
```

而不是只写：

```text
0030
那个构建任务
前面的任务
```

Task ID 可以作为辅助引用：

```text
K1-03 — `0030_kindlehf构建验证_KindleHF-Native-Build-Bringup.md`
```

---

# 8. 已完成任务不通过重命名改变排序

任务完成后不要把：

```text
0030_某任务.md
```

改成：

```text
DONE_0030_某任务.md
completed_0030_某任务.md
```

也不要为了表示优先级频繁重排已有编号。

完成状态进入：

- Task 文档自身结果/证据；
- `docs/status/00_当前项目状态_Baga-Ink-Project-Status.md`；
- 代码、测试与 Commit；
- 必要时 Compatibility / BICTS evidence。

文件编号表示**稳定的计划/阅读顺序和定位符**，不是动态状态。

---

# 9. 适用于未来所有 Kindle 子任务

后续任何 AI / 开发者在以下目录创建 Markdown 文件前：

```text
docs/plans/platform-ports/kindle/
```

及其任意子目录，必须先遵守本规则。

最重要的检查只有一句：

> **任务文档文件名如果不是以数字和 `_` 开头，就不应该进入这个目录。**

对于预计长期增长的任务目录，默认采用四位零填充 + 10 步进：

```text
0000_
0010_
0020_
0030_
...
```

这样即使 Kindle Port 后续增长到数百、数千份任务文档，目录仍然可以稳定排序、快速搜索和持续插入。