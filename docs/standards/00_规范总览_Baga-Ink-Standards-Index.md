# Baga Ink 规范总览 / Baga Ink Standards Index

> **目录级别：规范入口 / Standards Entry Point**  
> **状态：Living Index v0.3**  
> **日期：2026-08-22**

---

## 0. 目的 / Purpose

`docs/standards/` 是 Baga Ink Platform 的唯一正式规范目录。

编号表达**规范重要性、依赖顺序和领域分组**，不是创建时间。

```text
数字越小
→ 越接近平台宪法
→ 影响范围越大
→ 越应优先阅读

同一编号区间
→ 属于同一规范领域
```

---

# 1. 规范总层级 / Standards Hierarchy

```text
01 顶层战略与架构
│
├── 平台与应用层 02–09
│   ├── 02 应用标准
│   ├── 03 API 规范
│   ├── 04 Capability 能力注册表
│   ├── 05 Permission 权限模型
│   ├── 06 IKP 应用包规范
│   ├── 07 Device Adapter 设备适配器规范
│   ├── 08 Compatibility 兼容性标准
│   └── 09 UI 规范
│
├── 测试与设备适配层 10–19
│   ├── 10 Compatibility Test Suite
│   ├── 11 Kindle Adapter
│   └── 12 Android E-Paper Adapter
│
└── 市场与分发安全层 20–29
    ├── 20 市场与分发总体架构
    ├── 21 Publisher Identity 与 App Ownership
    ├── 22 IKP Signing 与 Key Lifecycle
    ├── 23 Repository Metadata 与 Index Protocol
    ├── 24 Publishing / Review / Version Policy
    ├── 25 Update / Rollback / Revocation Protocol
    ├── 26 Distribution Client / Offline Transfer
    ├── 27 Transparency / Security Audit
    └── 28 Catalog / App Discovery
```

---

# 2. 平台核心闭环 / Platform Core Loop

```text
App Standard 管开发者
        │
        ▼
API + Capability + Permission + UI
        │
        ▼
Baga Ink Platform Core
        │
        ▼
Device Adapter Standard 管设备抽象
        │
        ▼
Kindle / Android Adapter 管具体实现
        │
        ▼
Compatibility Standard + BICTS 管认证
```

如果这个闭环被 App 或设备私有接口绕开，平台就会重新碎片化。

---

# 3. 分发安全闭环 / Distribution Security Loop

```text
Publisher Identity
        │
        ▼
App Ownership + App Key Delegation
        │
        ▼
Publisher-signed IKP
        │
        ▼
Signed Repository Metadata
        │
        ▼
Baga Ink Client / Device Direct / Offline Snapshot
        │
        ▼
Device Final Verification
        │
        ▼
Staged Install → Health Check → Active / Rollback
```

三层信任：

```text
Publisher Signature
证明软件由谁授权

Repository Metadata
证明仓库当前分发什么

Local Installed Identity
证明什么身份可以覆盖已安装应用
```

三层必须同时成立。

---

# 4. 正式文件清单 / Canonical Documents

## 4.1 平台核心标准 00–09

| 编号 | 文件 | 定位 |
|---|---|---|
| 00 | `00_规范总览_Baga-Ink-Standards-Index.md` | 唯一规范入口与阅读顺序 |
| 01 | `01_顶层战略与架构_Baga-Ink-Platform-Strategy.md` | 项目最高层级战略与架构定义 |
| 02 | `02_应用标准_Baga-Ink-App-Standard.md` | 第三方 IKP App 的合规边界 |
| 03 | `03_API规范_Baga-Ink-API-Specification.md` | `baga.*` 公开 API 边界 |
| 04 | `04_能力注册表_Baga-Ink-Capability-Registry.md` | Capability 命名、语义与稳定性 |
| 05 | `05_权限模型_Baga-Ink-Permission-Model.md` | 应用权限、授权与最小权限原则 |
| 06 | `06_IKP应用包规范_IKP-Package-Specification.md` | `.ikp` 包结构与基础验证边界 |
| 07 | `07_设备适配器规范_Baga-Ink-Device-Adapter-Specification.md` | Device Adapter 统一职责和接口 |
| 08 | `08_兼容性标准_Baga-Ink-Compatibility-Standard.md` | `Baga Ink Compatible` 认证要求 |
| 09 | `09_UI规范_Baga-Ink-UI-Specification.md` | 面向墨水屏的统一 UI 与刷新行为 |

## 4.2 测试与设备适配 10–19

| 编号 | 文件 | 定位 |
|---|---|---|
| 10 | `10_兼容性测试套件_Baga-Ink-Compatibility-Test-Suite.md` | BICTS 测试项目、通过规则和报告 |
| 11 | `11_Kindle适配规范_Baga-Ink-Kindle-Adapter.md` | Kindle 系列适配基线 |
| 12 | `12_Android墨水屏适配规范_Baga-Ink-Android-E-Paper-Adapter.md` | Android E-Paper 适配基线 |
| 13–19 | Reserved | 后续设备家族、测试 Profile 与认证补充 |

## 4.3 市场与分发安全 20–29

| 编号 | 文件 | 定位 |
|---|---|---|
| 20 | `20_市场与分发总体架构_Baga-Ink-Market-and-Distribution-Architecture.md` | Market、Repository、Client 与设备的顶层分发架构 |
| 21 | `21_发布者身份与应用所有权标准_Baga-Ink-Publisher-Identity-and-App-Ownership-Standard.md` | Publisher Identity、App ID 所有权、委托、恢复与转移 |
| 22 | `22_IKP签名与密钥生命周期标准_Baga-Ink-IKP-Signing-and-Key-Lifecycle-Standard.md` | IKP Publisher Signature、密钥轮换与验证算法 |
| 23 | `23_仓库元数据与索引协议_Baga-Ink-Repository-Metadata-and-Index-Protocol.md` | 受约束 TUF Profile、Repository Root、Metadata 与 Target |
| 24 | `24_应用发布审核与版本政策_Baga-Ink-App-Publishing-Review-and-Version-Policy.md` | App 注册、不可变 Release、审核、Channel 与 Review Attestation |
| 25 | `25_应用更新回滚与撤销协议_Baga-Ink-Update-Rollback-and-Revocation-Protocol.md` | 候选选择、staged install、健康确认、回滚、降级与撤销 |
| 26 | `26_分发客户端与离线传输协议_Baga-Ink-Distribution-Client-and-Offline-Transfer-Protocol.md` | Baga Ink Client、USB、局域网、侧载与离线 Repository Snapshot |
| 27 | `27_透明日志与安全审计标准_Baga-Ink-Transparency-and-Security-Audit-Standard.md` | 追加式 Merkle Log、Checkpoint、审计与独立 Monitor |
| 28 | `28_市场目录与应用发现规范_Baga-Ink-Catalog-and-App-Discovery-Specification.md` | Catalog、搜索、本地化、低带宽 Diff 与 E-Paper Market UI |
| 29 | Reserved | 预留给未来分发层公共规范；不提前绑定付费或 DRM |

---

# 5. Reference Apps

Reference App 不属于 Baga Ink Standards，不得覆盖上位规范。

当前位置：

```text
docs/reference-apps/
└── 01_LifeBook参考实现_LifeBook-Reference-App.md
```

LifeBook 是第一个旗舰 Reference App，用真实产品验证：

```text
同一个 lifebook.ikp
        │
        ├── Kindle
        └── Android E-Paper
```

---

# 6. 阅读顺序 / Reading Order

## 6.1 第一次了解 Baga Ink

```text
00 → 01 → 02 → 03 → 07 → 08 → 20
```

## 6.2 开发第三方 App

```text
02 → 03 → 04 → 05 → 06 → 09
```

准备发布时继续：

```text
21 → 22 → 24 → 25 → 28
```

## 6.3 开发新设备 Adapter

```text
01 → 04 → 07 → 08 → 10 → 11/12
```

## 6.4 做 OEM / 设备认证

```text
08 → 10 → 07 → 对应 Device Adapter 规范
```

## 6.5 实现 Market / Repository

```text
20 → 21 → 22 → 23 → 24 → 25 → 27 → 28
```

## 6.6 实现 Baga Ink Client

```text
20 → 23 → 25 → 26 → 28
```

## 6.7 做供应链安全审计

```text
21 → 22 → 23 → 24 → 25 → 27
```

---

# 7. 文件命名规则 / Naming Rules

规范文件必须使用：

```text
NN_中文名_English-Name.md
```

例如：

```text
04_能力注册表_Baga-Ink-Capability-Registry.md
23_仓库元数据与索引协议_Baga-Ink-Repository-Metadata-and-Index-Protocol.md
```

规则：

- 两位数字前缀必须保留；
- 中文名用于中文团队快速理解；
- 英文名用于国际开发者与引用；
- 英文单词间使用 `-`；
- 文件名不使用空格；
- 编号不按日期决定；
- 低编号文件不得被高编号文件静默推翻。

---

# 8. 编号保留区间 / Reserved Number Ranges

```text
00        索引
01–09     平台核心标准
10–19     测试、认证与设备适配
20–29     Market、Distribution、Signing 与 Supply Chain Security
30–39     Sync、Cloud、Account 与跨设备数据
40–49     Developer Tools、CLI、Simulator 与 Build Tooling
50–59     Optional Extensions
60–69     OEM / Enterprise / Managed Device
70–79     Operations / Observability / Reliability
80–89     Reserved
90–99     Experimental / Incubating
```

新增文档应优先使用对应保留区间，不轻易重排现有编号。

---

# 9. 术语硬规则 / Terminology Rules

Baga Ink 坚持轻量平台设计。

设备端统一表达：

```text
Baga Ink Platform
Baga Ink Platform Core
Embedded Lua Interpreter
Baga Lua Profile
Baga Ink API
Baga Ink Device Adapter
```

Lua 解释器只是 Platform Core 内部的一项轻量实现能力，不是独立产品。

项目文档不得把 Baga Ink 描述成需要用户额外安装、独立理解和独立维护的庞大中间执行系统。

---

# 10. 规范权威边界 / Authority Boundaries

```text
02 负责：什么是合规 Baga Ink App
03 负责：公开 baga.* API
04 负责：Capability 名称与语义
05 负责：Permission 名称与授权
06 负责：IKP Container、Manifest 和基础包结构
07 负责：Device Adapter 边界
08 / 10 负责：Compatible 与测试
21 负责：Publisher Identity 与 App Ownership
22 负责：IKP Signature 与 Key Lifecycle
23 负责：Repository Metadata 与 Index
24 负责：Publishing / Review / Version Policy
25 负责：Update / Rollback / Revocation
26 负责：Client / Offline Transfer
27 负责：Transparency / Audit
28 负责：Catalog / Discovery
```

下位文件应引用上位或专门规范，而不是复制并修改同一规则。

---

# 11. 变更治理 / Change Governance

- 修改 `01–03` 应经过架构级讨论；
- 新 Capability 必须先进入 `04`；
- 新 Permission 必须先进入 `05`；
- IKP 包结构变化必须更新 `06`；
- Publisher Identity 变化必须更新 `21`；
- 签名输入或算法变化必须更新 `22`；
- Repository 安全角色变化必须更新 `23`；
- 更新状态机或撤销行为变化必须更新 `25`；
- 新设备要声称 Compatible，必须遵守 `08` 并通过 `10`；
- Kindle / Android 私有能力不得绕过 `07` 直接成为 Universal App API；
- Market Product Policy 不得改写 App Identity 和 Update Identity；
- 子规范不得静默违反上位规范。

安全关键文档进入 Stable 版本后，Breaking Change 必须提高 Major 并提供迁移方案。

---

# 12. 两个核心闭环 / Two Closed Loops

## 12.1 开发与设备闭环

```text
Developer
   │
   ▼
App Standard
   │
   ▼
API / Capability / Permission / UI
   │
   ▼
Platform Core
   │
   ▼
Device Adapter
   │
   ▼
Kindle / Android E-Paper
   │
   ▼
BICTS
   │
   ▼
Baga Ink Compatible
```

## 12.2 发布与更新闭环

```text
Publisher
   │
   ▼
Signed IKP
   │
   ▼
Repository + Review
   │
   ▼
Catalog / Client / Offline Transfer
   │
   ▼
Device Verification
   │
   ▼
Stage / Activate / Health Check
   │
   ├── Success → Active
   └── Failure → Rollback
```

---

**本文件是 `docs/standards/` 的唯一正式目录入口。**
