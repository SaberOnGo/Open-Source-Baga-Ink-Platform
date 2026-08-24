# Baga Ink Kindle 实现任务总计划 / Baga Ink Kindle Implementation Master Plan

> **文档级别：Implementation Master Plan / Kindle 平台移植总计划**  
> **状态：Plan Baseline v1.0**  
> **日期：2026-08-24**  
> **首个目标：Homebrew-ready `kindlehf`，firmware >= 5.16.3 的代表设备**

---

## 0. 文档定位

本文只保存 Kindle Port 的长期路线、Milestone 依赖和当前任务包入口。可直接实施的研究、裁决、Write Scope、测试矩阵与真机步骤集中在一个版本化 Task Package 中。

权威顺序：

```text
Standards
  > Approved Design / Kindle Architecture Freeze
  > 本 Master Plan
  > current Task Package
  > implementation / tests / device evidence
```

主要上位文档：

```text
docs/zh-CN/standards/07_设备适配器规范.md
docs/zh-CN/standards/11_Kindle适配规范.md
docs/zh-CN/design/02_设备适配器可执行契约与SDK设计.md
docs/zh-CN/reference-apps/03_Kindle具体实现架构冻结.md
```

---

# 1. 当前任务包

当前 Kindle 实现工作入口：

```text
docs/plans/platform-ports/kindle/task/
└── 2026-08-24_kindle-platform/
    └── v1/
        └── v1.1/
```

该目录按 `00 → 19` 平铺完整任务资料。实现 Agent 不需要再分别进入 K0/K1/K2 的 Task Version，也不需要访问独立 Execution Prompt 树。

---

# 2. 第一条必须跑通的真实链

第一阶段不以完整 LifeBook 或自动 jailbreak 为验收目标。

```text
Homebrew-ready real Kindle (`kindlehf` first)
        ↓
baga-launch
        ↓
pinned KOReader/koreader-base substrate
        ↓
Baga Ink Platform Core
        ↓
Kindle Device Adapter
        ↓
baga-probe.ikp
        ↓
visible UI + normalized input
        ↓
persisted state
        ↓
sleep / wake
        ↓
state remains valid
```

第一份真实 IKP 是 `baga-probe.ikp`，不是完整 LifeBook。

---

# 3. Milestone 路线

| Milestone | 目标 | 主要 Gate |
|---|---|---|
| **K0** | Adapter Contract 可执行基础 | IDL + generated bindings + Mock + Contract Tests + frozen snapshot |
| **K1** | pinned KOReader `kindlehf` Bring-up | direct Baga private entry 在真实 Kindle 可启动、退出、重启 |
| **K2** | Kindle Base Device Adapter | Display/Input/Storage/Lifecycle/Power 等 Base Contract 通过测试 |
| **K3** | Minimal Platform Core + Probe IKP | 真正 `.ikp` 可交互、持久化并经历 sleep/wake |
| **K4** | IKP staging/activation/verifier | 验证、staging、atomic activation、rollback 成立 |
| **K5** | `baga.reader` 接入 KOReader reader stack | ReaderUI/CREngine/MuPDF 通过 Baga API 使用 |
| **K6** | KPM packaging + Kindle Home Entry | Kindle Home 可直接进入 LifeBook/Probe，不暴露底层工具 |
| **K7** | Baga Ink Client + Route DB automation | 检测精确设备状态、选择已验证 route、确保 Platform 并安装 IKP |

主依赖：

```text
K0 → K1 → K2 → K3 → K4 → K5 → K6 → K7
```

K0 与 K1 的非冲突研究/基础工作可有限并行。

---

# 4. 第一阶段边界

K0–K3 之前不把以下内容作为前置条件：

```text
自动 jailbreak
完整 Baga Ink Client
完整 LifeBook
KPM 产品化安装包
Market
AI
Sync
Audio
Bluetooth
Pen
全部历史 Kindle 型号
```

Jailbreak/bootstrap 解决“设备怎样达到可运行 Platform 的状态”；Platform/Adapter/IKP 解决“Baga Platform 本身是否正确工作”。两类问题先解耦。

---

# 5. Kindle Adapter 实现哲学

Kindle Adapter 保持薄层：

```text
KOReader / koreader-base / FBInk / Kindle OS / validated Homebrew
        ↓
thinnest safe binding / normalization
        ↓
Baga Device Adapter Contract
```

不优先重写 framebuffer、input、reader、power 或已有成熟能力。

Device Adapter Contract 不限制源码语言。Kindle 当前实现默认以 KOReader 已有 Lua/LuaJIT 能力为首选 glue，成熟 native 库继续保持 native；具体裁决已经并入当前 Task Package 的 `03` 与 `17`，避免执行阶段重新选型。

---

# 6. 第一台设备与扩展顺序

首台设备基线：

```text
already jailbroken / Homebrew-ready
firmware >= 5.16.3
native target = kindlehf
```

跑通后按真实证据扩展：

```text
kindlepw2
→ kindle
→ kindle-legacy
```

兼容性结论必须绑定精确 model + firmware + native target，不按设备相似性继承。

---

# 7. 任务包更新规则

当前 `v1.1` 是第一份完整施工包。下列变化需要建立新的 `v1.x` 或后续大版本：

```text
核心启动方案变化
语言/绑定默认矩阵变化
Milestone Scope 或依赖变化
Write Scope 结构变化
真机证据推翻当前裁决
验收 Gate 或恢复策略发生结构性变化
```

普通代码进度、单个测试修复和执行日志不需要创建新 Task Package 版本。
