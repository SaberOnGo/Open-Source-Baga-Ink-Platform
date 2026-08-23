# Baga Ink 规范总览 / Baga Ink Standards Index

> **目录级别：规范入口 / Standards Entry Point**  
> **状态：Living Index v0.5**  
> **日期：2026-08-23**

---

## 0. 目的 / Purpose

`docs/standards/` 是 Baga Ink Platform 的唯一正式规范目录。

编号表达规范重要性、依赖顺序和领域分组，不是创建时间。

正式规范只描述**当前有效设计**。被替换、否决或未采用的接口名、namespace、架构草案不保留在正文中；历史由 Git commit / diff 保存。

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
├── 测试、设备适配与标准库 10–19
│   ├── 10 Compatibility Test Suite
│   ├── 11 Kindle Adapter
│   ├── 12 Android E-Paper Adapter
│   └── 13 Standard Libraries / Adopted Components
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
App Standard
   ↓
Baga Ink API + Baga Lua Profile / Standard Libraries
   ↓
Baga Ink Platform Core
   ↓
Device Adapter
   ↓
Kindle / Android E-Paper
   ↓
Compatibility Standard + BICTS
```

关键区分：

```text
baga.*
→ 统一设备 / OS / Platform 差异

Standard Libraries / Adopted Components
→ 直接采用成熟通用软件能力
```

当前重要例子：

```text
SQLite + lsqlite3
→ Stable Standard Library

Automerge core
→ Adopted Local-first / CRDT Foundation
→ 可整体采用，也可拆模块采用

KOReader / FBInk
→ Kindle Platform / Adapter 内部成熟实现来源
```

如果这个闭环被 App 或设备私有接口绕开，平台会重新碎片化；如果成熟通用库被无意义重新包装，平台也会产生不必要的重复抽象。

---

# 3. 分发安全闭环 / Distribution Security Loop

```text
Publisher Identity
        ↓
App Ownership + App Key Delegation
        ↓
Publisher-signed IKP
        ↓
Signed Repository Metadata
        ↓
Baga Ink Client / Device Direct / Offline Snapshot
        ↓
Device Final Verification
        ↓
Staged Install → Health Check → Active / Rollback
```

三层信任：Publisher Signature、Repository Metadata、Local Installed Identity 必须同时成立。

---

# 4. 正式文件清单 / Canonical Documents

## 4.1 平台核心标准 00–09

| 编号 | 文件 | 定位 |
|---|---|---|
| 00 | `00_规范总览_Baga-Ink-Standards-Index.md` | 唯一规范入口与阅读顺序 |
| 01 | `01_顶层战略与架构_Baga-Ink-Platform-Strategy.md` | 项目最高层级战略与架构定义 |
| 02 | `02_应用标准_Baga-Ink-App-Standard.md` | 第三方 IKP App 合规边界 |
| 03 | `03_API规范_Baga-Ink-API-Specification.md` | `baga.*` 公开平台 API |
| 04 | `04_能力注册表_Baga-Ink-Capability-Registry.md` | Capability 命名、语义与稳定性 |
| 05 | `05_权限模型_Baga-Ink-Permission-Model.md` | Permission 与最小权限原则 |
| 06 | `06_IKP应用包规范_IKP-Package-Specification.md` | `.ikp` 包结构与验证 |
| 07 | `07_设备适配器规范_Baga-Ink-Device-Adapter-Specification.md` | Device Adapter 边界 |
| 08 | `08_兼容性标准_Baga-Ink-Compatibility-Standard.md` | `Baga Ink Compatible` 认证要求 |
| 09 | `09_UI规范_Baga-Ink-UI-Specification.md` | E-Paper UI 与刷新行为 |

## 4.2 测试、设备适配与标准库 10–19

| 编号 | 文件 | 定位 |
|---|---|---|
| 10 | `10_兼容性测试套件_Baga-Ink-Compatibility-Test-Suite.md` | API/Profile/Standard Library 测试 |
| 11 | `11_Kindle适配规范_Baga-Ink-Kindle-Adapter.md` | Kindle 适配与成熟组件复用 |
| 12 | `12_Android墨水屏适配规范_Baga-Ink-Android-E-Paper-Adapter.md` | Android E-Paper 适配 |
| 13 | `13_标准库与成熟组件采用规范_Baga-Ink-Standard-Libraries-and-Adopted-Components.md` | SQLite/lsqlite3、Automerge 等成熟通用库采用原则 |
| 14–19 | Reserved | 后续设备、Runtime Profile、测试补充 |

## 4.3 市场与分发安全 20–29

| 编号 | 文件 | 定位 |
|---|---|---|
| 20 | `20_市场与分发总体架构_Baga-Ink-Market-and-Distribution-Architecture.md` | Distribution architecture |
| 21 | `21_发布者身份与应用所有权标准_Baga-Ink-Publisher-Identity-and-App-Ownership-Standard.md` | Publisher / App Ownership |
| 22 | `22_IKP签名与密钥生命周期标准_Baga-Ink-IKP-Signing-and-Key-Lifecycle-Standard.md` | IKP signing / keys |
| 23 | `23_仓库元数据与索引协议_Baga-Ink-Repository-Metadata-and-Index-Protocol.md` | Repository / TUF profile |
| 24 | `24_应用发布审核与版本政策_Baga-Ink-App-Publishing-Review-and-Version-Policy.md` | Publishing / review / version |
| 25 | `25_应用更新回滚与撤销协议_Baga-Ink-Update-Rollback-and-Revocation-Protocol.md` | Update / rollback / revocation |
| 26 | `26_分发客户端与离线传输协议_Baga-Ink-Distribution-Client-and-Offline-Transfer-Protocol.md` | Client / offline transfer |
| 27 | `27_透明日志与安全审计标准_Baga-Ink-Transparency-and-Security-Audit-Standard.md` | Transparency / audit |
| 28 | `28_市场目录与应用发现规范_Baga-Ink-Catalog-and-App-Discovery-Specification.md` | Catalog / discovery |
| 29 | Reserved | Distribution future |

---

# 5. Reference Apps

Reference App 不属于 Standards，不得覆盖上位规范。

```text
docs/reference-apps/
├── 01_LifeBook参考实现_LifeBook-Reference-App.md
└── 02_LifeBook架构与Kindle兼容实现_LifeBook-Architecture-and-Kindle-Compatibility.md
```

LifeBook 是第一个旗舰 Reference App，用真实产品验证同一个 `lifebook.ikp` 跨 Kindle / Android E-Paper。

---

# 6. 阅读顺序 / Reading Order

## 6.1 第一次了解 Baga Ink

```text
00 → 01 → 02 → 03 → 13 → 07 → 08 → 20
```

## 6.2 开发第三方 App

```text
02 → 03 → 13 → 04 → 05 → 06 → 09
```

开发者必须理解：

```text
设备能力 → baga.*
关系数据库 → require("lsqlite3")
Automerge → Adopted Foundation
```

准备发布继续：

```text
21 → 22 → 24 → 25 → 28
```

## 6.3 开发 Device Adapter

```text
01 → 03 → 13 → 04 → 07 → 08 → 10 → 11/12
```

## 6.4 OEM / 设备认证

```text
08 → 10 → 07 → 13 → 对应 Device Adapter
```

## 6.5 Market / Repository

```text
20 → 21 → 22 → 23 → 24 → 25 → 27 → 28
```

## 6.6 Baga Ink Client

```text
20 → 23 → 25 → 26 → 28
```

---

# 7. 文件命名与编号区间

规范文件使用：

```text
NN_中文名_English-Name.md
```

编号区间：

```text
00        Index
01–09     Platform Core Standards
10–19     Tests / Device Adapters / Runtime Profiles / Standard Libraries
20–29     Market / Distribution / Signing / Supply Chain
30–39     Sync / Cloud / Account / Cross-device Data Protocols
40–49     Developer Tools / CLI / Simulator
50–59     Optional Extensions
60–69     OEM / Enterprise
70–79     Operations / Observability
80–89     Reserved
90–99     Experimental
```

---

# 8. 规范权威边界 / Authority Boundaries

```text
01 负责：顶层战略 / 公共架构
02 负责：合规 Baga Ink App
03 负责：公开 baga.* API
04 负责：Capability
05 负责：Permission
06 负责：IKP
07 负责：Device Adapter
08 / 10 负责：Compatible / tests
11 / 12 负责：具体设备家族
13 负责：Standard Libraries / Adopted Mature Components
20–28 负责：分发、安全、更新、Catalog
```

关键规则：

> **新增平台抽象前，必须先查看 `13`：如果成熟通用库已经有更好的抽象，应优先直接采用，而不是重新包装。**

---

# 9. 变更治理 / Change Governance

- 修改 `01–03` 应经过架构级讨论；
- Standard Library / Adopted Component 决策更新 `13`；
- 新 Capability 更新 `04`；
- 新 Permission 更新 `05`；
- IKP 变化更新 `06`；
- Adapter 变化更新 `07/11/12`；
- Compatible 行为变化更新 `08/10`；
- SQLite / lsqlite3 baseline 变化必须跑 BICTS regression；
- Automerge 若升级为 developer-facing 稳定 Lua module 或正式 wire protocol，必须明确版本与 migration，不能写“最新版”；
- 被替换或否决的接口名、namespace、架构草案 MUST 从 Standards 与 Reference Apps 正文移除，历史只保留在 Git。

---

# 10. 两个核心闭环

## 10.1 开发与设备闭环

```text
Developer
  ↓
App Standard
  ↓
Baga API + Lua Profile / Standard Libraries
  ↓
Platform Core
  ↓
Device Adapter
  ↓
Kindle / Android
  ↓
BICTS
```

## 10.2 发布与更新闭环

```text
Publisher
  ↓
Signed IKP
  ↓
Repository + Review
  ↓
Catalog / Client / Offline Transfer
  ↓
Device Verification
  ↓
Stage / Activate / Health Check / Rollback
```

---

# 11. 核心判断

Baga Ink 的统一来自：

```text
设备差异 → 稳定 Baga API
成熟通用软件能力 → 直接采用优秀 Standard Library / Foundation
安装/更新/权限/兼容 → 统一协议与测试
```

**本文件是 `docs/standards/` 的唯一正式目录入口。**
