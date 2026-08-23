# Kindle 实现任务规划索引 / Kindle Implementation Task Catalog

> **目录：`docs/plans/platform-ports/kindle/task/`**  
> **文档级别：Task Design Catalog / 任务设计索引**  
> **状态：Planning Baseline v0.1**  
> **日期：2026-08-23**  
> **上位计划：`../0010_Kindle实现任务总计划_Baga-Ink-Kindle-Implementation-Master-Plan.md`**

---

## 0. 目的

本索引把 Kindle Implementation Master Plan 中的 K0–K7 Milestone 映射为可版本化、可追溯的 Task Design。

K0–K7 是 Roadmap / Milestone 编号；真正的工程 Task 使用稳定的 `TASK-NNNN` 编号，并在各自目录中维护 `vNNN` 设计版本。

执行链保持：

```text
Standards / Approved Design / Architecture Freeze
        ↓
Kindle Implementation Master Plan
        ↓
Task Design vNNN
        ↓
Execution Prompts
        ↓
Implementation / Tests / Real-device Evidence
```

Task Design 不改变公共 Standard、IKP Contract、Device Adapter Contract 或 Architecture Freeze。若实现证据要求改变上位架构，相关上位文档应先完成显式修订。

---

# 1. Task Catalog

| Task ID | Milestone | Task | Current Design | Dependency Gate |
|---|---|---|---|---|
| `TASK-0010` | K0 | Adapter Contract 可执行化 | `v001` | Standards 07 + Approved Design 02 |
| `TASK-0020` | K1 | KOReader `kindlehf` Bring-up | `v001` | Homebrew-ready real `kindlehf`; 可与 K0 的非冲突工作有限并行 |
| `TASK-0030` | K2 | Kindle Base Device Adapter | `v001` | K0 Contract baseline + K1 substrate evidence |
| `TASK-0040` | K3 | Minimal Platform Core + Probe IKP | `v001` | K0–K2 gates |
| `TASK-0050` | K4 | IKP staging / activation / device verifier | `v001` | K3 developer-mode IKP chain + signing/update executable baseline |
| `TASK-0060` | K5 | Kindle Reader Provider | `v001` | K3/K4 Platform/App lifecycle stable |
| `TASK-0070` | K6 | KPM packaging + Kindle Home Entry | `v001` | K1–K5 device-side chain stable |
| `TASK-0080` | K7 | Baga Ink Client Kindle automation | `v001` | K6 verified install/home-entry path |

---

# 2. 首个工程焦点

首轮工程重点为：

```text
TASK-0010 / v001   Adapter Contract 可执行化
        +
TASK-0020 / v001   KOReader kindlehf Bring-up
```

两者允许有限并行：K0 建立机器 Contract、codegen、Mock 与 Contract Tests；K1 锁定并验证 Kindle substrate、native target 与 Baga-controlled private entry。

首轮不把以下工作设为前置条件：

```text
完整 LifeBook
自动 jailbreak
Baga Ink Client route automation
KPM 产品化安装包
完整 IKP signature/update pipeline
Reader
AI / Sync / Market
Audio / Bluetooth / Pen
历史 Kindle 全覆盖
```

第一条设备侧产品链仍以 `baga-probe.ikp` 为首个真实 App 验收目标；该链在 `TASK-0040` 完成。

---

# 3. 依赖与推进顺序

主依赖链：

```text
TASK-0010 (K0)
      ↓
TASK-0020 (K1)
      ↓
TASK-0030 (K2)
      ↓
TASK-0040 (K3)
      ↓
TASK-0050 (K4)
      ↓
TASK-0060 (K5)
      ↓
TASK-0070 (K6)
      ↓
TASK-0080 (K7)
```

其中 K0 与 K1 的研究/基础 bring-up 可以有限并行，但后续 Task 不应通过 Kindle 私有 ad-hoc API 绕过尚未稳定的上位 Contract。

---

# 4. 首台真实设备基线

首台 Bring-up 设备使用以下基线：

```text
real Kindle
already jailbroken / Homebrew-ready
firmware >= 5.16.3
native target: kindlehf
```

开发阶段可使用受控 shell/USB/Scriptlet 方式部署测试资产。KPM packaging、Kindle Home 产品入口和 jailbreak/bootstrap 自动化分别属于后续 K6、K7，不作为 K1–K3 的正确性前置条件。

`kindlehf` 跑通后再按真实 Compatibility evidence 扩展：

```text
kindlepw2
→ kindle
→ kindle-legacy
```

兼容性结论按精确 model + firmware + native target 证据建立，不按相似型号直接继承。

---

# 5. Task Version 规则

每个 Task 根目录包含：

```text
0000_任务版本索引_Task-Version-Index.md
v001/
└── 0000_任务设计总纲_Task-Design-Overview.md
```

当范围、核心实现方案、依赖、真机验证策略、验收 Gate 或恢复策略发生结构性变化时，新建 `v002`、`v003` 等版本；旧版本保留。

Execution Prompt 只能从精确选定的 Task Version 派生，并使用同名 Task 目录与同一 `vNNN` 镜像。

---

# 6. 第一条重大验收链

Kindle Port 的第一条重大设备验收链属于 K3 / `TASK-0040`：

```text
real Homebrew-ready Kindle
        ↓
baga-launch
        ↓
Baga Ink Platform Core
        ↓
Kindle Device Adapter
        ↓
baga-probe.ikp
        ↓
visible UI + normalized input
        ↓
persisted counter changes
        ↓
sleep / wake
        ↓
state remains valid
```

在该 Gate 通过前，完整 LifeBook、Reader 产品集成、KPM 产品化和 Client 自动化均不作为基础 bring-up 成功的替代证据。
