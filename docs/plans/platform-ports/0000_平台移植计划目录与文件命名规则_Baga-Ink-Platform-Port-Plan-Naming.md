# Baga Ink 平台移植计划目录与文件命名规则 / Baga Ink Platform Port Plan Naming

> **文档级别：Implementation Plan Directory Rule / 平台移植计划目录规则**  
> **状态：Mandatory Naming Rule v0.1**  
> **日期：2026-08-23**  
> **适用范围：`docs/plans/platform-ports/` 及未来所有设备/OS 平台子目录**

---

## 0. 核心规则

Baga Ink 未来会有 Kindle、Android E-Paper 以及其他设备/OS 家族的 Platform Port。每个平台都可能产生数百甚至数千份实施计划、Task、PoC、验证和兼容性文档。

因此：

> **`docs/plans/platform-ports/` 下所有计划/任务 Markdown 文件 MUST 使用“数字前缀 + 下划线 + 描述性文件名”的命名方式。**

格式：

```text
<数字前缀>_<描述性文件名>.md
```

禁止：

```text
README.md
Task.md
Bringup.md
Adapter-Plan.md
```

正确：

```text
0000_目录说明与文件命名规则_....md
0010_里程碑计划_....md
0020_锁定上游组件_....md
0030_原生构建验证_....md
0040_设备Bringup-PoC_....md
```

---

# 1. 新任务目录默认四位零填充

预计长期增长的目录 SHOULD 使用：

```text
0000_
0010_
0020_
0030_
...
9999_
```

固定宽度可以保证 GitHub、文件系统、搜索工具和 AI 在名称排序时得到稳定顺序。

现有已经采用数字前缀 + `_` 的历史 Plan 文件可以保留；新创建的大规模 Task 文档默认使用四位编号。

---

# 2. 默认按 10 递增

正常新增：

```text
0010_
0020_
0030_
0040_
```

为后续插入任务保留编号空间。

例如：

```text
0010_Task-A.md
0020_Task-B.md
```

中间需要新增任务时：

```text
0015_Task-A1.md
```

无需重命名后续数百份文档。

---

# 3. 每个目录独立编号

编号不要求在整个仓库全局唯一，而是在当前目录内唯一、有序。

推荐结构：

```text
docs/plans/platform-ports/
├── 0000_平台移植计划目录与文件命名规则_....md
│
├── kindle/
│   ├── 0000_目录说明与文件命名规则_....md
│   ├── <数字前缀>_Kindle实现任务总计划_....md
│   ├── K0_adapter-contract/
│   │   ├── 0000_K0里程碑计划_....md
│   │   ├── 0010_....md
│   │   └── 0020_....md
│   └── ...
│
├── android-e-paper/
│   ├── 0000_目录说明与文件命名规则_....md
│   ├── 0010_Android-E-Paper实现总计划_....md
│   └── ...
│
└── future-platform/
    └── ...
```

这样即使整个项目最终有数千甚至更多 Task 文档，也不会依赖一个巨大的全局流水号。

---

# 4. `0000_` 保留给目录入口

每个实施目录 SHOULD 把 `0000_` 用于：

```text
目录说明
命名规则
Milestone 总计划 / 索引
验收 Gate 入口
```

具体执行 Task 通常从：

```text
0010_
```

开始。

如果某目录已经存在更早的数字前缀计划文件，不要求仅为了编号美观破坏历史引用；后续新文件仍必须遵守数字前缀规则。

---

# 5. 数字前缀不能替代语义文件名

禁止：

```text
0010_Task.md
0020_Todo.md
0030_Test.md
```

应使用：

```text
0010_锁定上游依赖_Pin-Upstream-Dependencies.md
0020_建立依赖与许可证清单_Dependency-License-Manifest.md
0030_原生目标构建验证_Native-Target-Build-Bringup.md
```

要求未来开发者或 AI 仅浏览目录名就能大致理解任务内容。

---

# 6. Milestone / Task ID 与文件编号分离

逻辑 Task ID，例如：

```text
K1-04
A2-07
PORT-ANDROID-15
```

用于计划、Issue、Commit 和测试证据的稳定引用。

文件前缀：

```text
0040_
0070_
0150_
```

用于目录排序与查找。

二者不是同一个概念，不必强制数值完全一致。

---

# 7. 完成状态不通过改文件名前缀表达

不要创建：

```text
DONE_0010_....md
COMPLETE_0020_....md
```

也不要任务完成后重新编号。

编号是稳定定位与阅读顺序；状态进入：

```text
Task 文档结果/证据
docs/status/00_当前项目状态_Baga-Ink-Project-Status.md
代码/测试/Commit
Compatibility / BICTS evidence
```

---

# 8. 对所有未来 Platform Port 生效

创建新的平台目录，例如：

```text
docs/plans/platform-ports/android-e-paper/
docs/plans/platform-ports/remarkable/
docs/plans/platform-ports/<future-family>/
```

时，不需要重新讨论是否要编号。

默认规则就是：

> **计划/任务文件必须以数字前缀和 `_` 开头；大规模任务目录默认采用四位零填充、按 10 递增。**

这条规则的目的不是形式主义，而是保证 Baga Ink 在任务规模达到数百、数千份以后，依然能够通过目录排序、数字搜索和稳定路径快速找到对应实现工作。