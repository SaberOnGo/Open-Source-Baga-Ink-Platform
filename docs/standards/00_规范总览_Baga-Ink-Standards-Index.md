# Baga Ink 规范总览 / Baga Ink Standards Index

> **目录级别：规范入口 / Standards Entry Point**  
> **状态：Living Index v0.1**  
> **日期：2026-08-22**

---

## 0. 目的 / Purpose

本目录 `docs/standards/` 是 Baga Ink Platform 的正式规范目录。

所有战略级、平台级、兼容性和设备适配规范统一放在这里；根目录不再堆放规范文档。

编号表达**规范重要性与依赖顺序**，不是创建时间。

基本原则：

```text
数字越小 → 越接近平台宪法 / 越稳定 / 越应优先阅读
数字越大 → 越接近具体实现 / 设备适配 / 测试执行
```

---

# 1. 规范层级 / Standards Hierarchy

```text
01 顶层战略与架构
        │
        ├── 02 应用标准
        ├── 03 API 规范
        ├── 04 Capability 能力注册表
        ├── 05 Permission 权限模型
        ├── 06 IKP 应用包规范
        ├── 07 Device Adapter 设备适配器规范
        ├── 08 Compatibility 兼容性标准
        ├── 09 UI 规范
        ├── 10 Compatibility Test Suite
        ├── 11 Kindle Adapter
        └── 12 Android E-Paper Adapter
```

关系可概括为：

```text
App Standard 管开发者
        │
        ▼
API + Capability + Permission + UI
        │
        ▼
Platform Core
        │
        ▼
Device Adapter Standard 管设备抽象
        │
        ▼
Kindle / Android Adapter 管具体实现
        │
        ▼
Compatibility Standard + Test Suite 管认证
```

---

# 2. 正式文件清单 / Canonical Documents

| 编号 | 文件 | 定位 |
|---|---|---|
| 00 | `00_规范总览_Baga-Ink-Standards-Index.md` | 规范入口与阅读顺序 |
| 01 | `01_顶层战略与架构_Baga-Ink-Platform-Strategy.md` | 项目最高层级战略与架构定义 |
| 02 | `02_应用标准_Baga-Ink-App-Standard.md` | 第三方 IKP App 的合规边界 |
| 03 | `03_API规范_Baga-Ink-API-Specification.md` | `baga.*` 公开 API 边界 |
| 04 | `04_能力注册表_Baga-Ink-Capability-Registry.md` | Capability 命名、语义、稳定性 |
| 05 | `05_权限模型_Baga-Ink-Permission-Model.md` | 应用权限、授权与最小权限原则 |
| 06 | `06_IKP应用包规范_IKP-Package-Specification.md` | `.ikp` 包结构、签名、安装与更新 |
| 07 | `07_设备适配器规范_Baga-Ink-Device-Adapter-Specification.md` | 设备适配层统一接口与职责 |
| 08 | `08_兼容性标准_Baga-Ink-Compatibility-Standard.md` | `Baga Ink Compatible` 的认证要求 |
| 09 | `09_UI规范_Baga-Ink-UI-Specification.md` | 面向墨水屏的统一 UI 与刷新行为 |
| 10 | `10_兼容性测试套件_Baga-Ink-Compatibility-Test-Suite.md` | BICTS 测试项目、通过规则与报告 |
| 11 | `11_Kindle适配规范_Baga-Ink-Kindle-Adapter.md` | Kindle 系列适配基线 |
| 12 | `12_Android墨水屏适配规范_Baga-Ink-Android-E-Paper-Adapter.md` | Android E-Paper 设备适配基线 |

---

# 3. 阅读顺序 / Reading Order

## 3.1 第一次了解项目

建议：

```text
00 → 01 → 02 → 03 → 07 → 08
```

## 3.2 开发第三方 App

建议：

```text
02 → 03 → 04 → 05 → 06 → 09
```

## 3.3 开发新设备 Adapter

建议：

```text
01 → 04 → 07 → 08 → 10 → 11/12
```

## 3.4 做 OEM / 设备认证

建议：

```text
08 → 10 → 07 → 对应设备 Adapter 规范
```

---

# 4. 命名与目录规则 / Naming Rules

## 4.1 文件名

规范文件 MUST 使用：

```text
NN_中文名_English-Name.md
```

例如：

```text
04_能力注册表_Baga-Ink-Capability-Registry.md
```

规则：

- 两位数字前缀 MUST 保留；
- 中文名用于中文团队快速理解；
- 英文名用于国际开发者与引用；
- 单词间使用 `-`；
- 不使用空格；
- 不以创建日期决定编号。

## 4.2 编号保留区间

建议长期使用：

```text
00        索引
01–09     平台核心标准
10–19     测试与设备适配
20–29     Market / Distribution / Signing
30–39     Sync / Cloud / Account
40–49     Developer Tools / CLI / Simulator
50–59     Optional Extensions
90–99     Experimental / Reserved
```

这样未来扩展规范时不需要重排所有文件。

---

# 5. 术语硬规则 / Terminology Rules

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

项目文档 MUST 不引入一个需要用户额外安装、独立管理、独立升级的庞大中间执行层概念。

Lua 解释器只是 Platform Core 内部的一项轻量实现能力，不是独立产品。

---

# 6. 变更治理 / Change Governance

低编号规范的变更影响面更大。

原则：

- 修改 `01–03` SHOULD 经过架构级讨论；
- 新 Capability MUST 先进入 `04` 再进入 API / Adapter；
- 新 Permission MUST 先进入 `05`；
- 新设备要声称 Compatible，MUST 遵守 `08` 并通过 `10`；
- Kindle / Android 私有能力不得绕过 `07` 直接成为 Universal App API；
- 子规范不得静默违反上位规范。

---

# 7. 核心闭环 / Core Closed Loop

Baga Ink 的标准体系最终必须形成下面这个闭环：

```text
Developer
   │
   ▼
Baga Ink App Standard
   │
   ▼
Baga Ink API
   │
   ├── Capability Registry
   ├── Permission Model
   └── UI Specification
   │
   ▼
Baga Ink Platform Core
   │
   ▼
Baga Ink Device Adapter
   │
   ▼
Kindle / Android E-Paper
   │
   ▼
Compatibility Test Suite
   │
   ▼
Baga Ink Compatible
```

如果这个闭环被绕开，平台就会重新碎片化。

---

**本文件是 `docs/standards/` 的唯一正式目录入口。**
