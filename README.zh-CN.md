<div align="center">

# Baga Ink Platform

### 面向墨水屏设备的开放应用平台

**应用只面对一套稳定平台 Contract；Kindle、Android 墨水屏以及未来设备的差异，由各自 Platform Port / Device Adapter 吸收。**

[![Project status](https://img.shields.io/badge/status-early%20development-orange.svg)](#项目状态)
[![Documentation](https://img.shields.io/badge/docs-简体中文-2ea44f.svg)](docs/zh-CN/00_项目文档入口.md)

<!-- BAGA-LANG-SWITCH:START -->
**语言：** [English](README.md) · **简体中文** · [＋ 增加一种语言](CONTRIBUTING.zh-CN.md#翻译与多语言)
<!-- BAGA-LANG-SWITCH:END -->

</div>

---

## Baga Ink 到底是什么？

**Baga Ink 是一个面向 E-Paper / 墨水屏设备的应用平台、兼容性 Contract 与开发者生态。**

今天，为一台墨水屏设备开发的 App，通常很难原样搬到另一台设备。Kindle Homebrew、Android 墨水屏、厂商 SDK、Linux Reader，在很多地方都完全不同：

- 屏幕刷新机制；
- Touch / Physical Key / Pen 输入；
- Storage / Sandbox；
- Sleep / Wake Lifecycle；
- Power / Network / Frontlight / Audio 等能力；
- App Packaging / Install / Update；
- 不同 Model / Firmware / ABI 的兼容性与 Quirk。

Baga Ink 想把这些差异从 App 里拿出去，集中放到可复用的 **Platform Port / Device Adapter** 中。

核心目标非常简单：

> **App 只适配 Baga Ink，而不是某一代 Kindle、某一家 Android 墨水屏厂商、某个 Framebuffer API 或私有 E-Paper SDK。**

Baga Ink 不是一个新的操作系统。它是 Portable App 与碎片化墨水屏设备环境之间的稳定平台层。

---

## 为什么要做这个项目？

墨水屏硬件很多，但应用开发生态高度碎片化。

| 现在常见的问题 | Baga Ink 的方向 |
|---|---|
| App 里充斥型号 / 厂商 / Firmware 判断 | 差异集中在 Device Adapter / Device Profile / Quirk Set |
| 每个平台有不同 Refresh / Input API | App 只使用稳定的 Baga Display / Input 语义 |
| 安装包和更新方式各不相同 | Portable Baga App 使用 `.ikp` |
| “应该能跑”常靠经验判断 | Capability + Contract Tests + BICTS 提供证据 |
| 团队反复重新做底层设备支持 | 最大化复用 OS、Vendor SDK、Homebrew 和成熟开源项目 |
| 一个 App Port 完成后仍绑死一个设备家族 | 同一个 App Contract 面向 Kindle、Android E-Paper 和未来设备 |

长期用户体验应该也很简单：

> **一台进入 Baga Ink Compatibility 范围的墨水屏设备，应该可以加入同一个 App 生态，而不是每一个 App 都重新做一次硬件移植。**

---

## 一张图看懂架构

```text
                  Baga Ink Apps
                  （.ikp 应用包）
                         │
                         ▼
             Baga Ink API / Baga Lua Profile
                         │
                         ▼
                 Baga Ink Platform Core
                         │
                         ▼
              Baga Device Adapter Contract
                         │
          ┌──────────────┴──────────────┐
          ▼                             ▼
       Kindle Port                Android E-Paper Port
 KOReader / FBInk /              AOSP / Vendor SDK /
 Kindle OS / Homebrew            墨水屏厂商设备 API
          │                             │
          └──────────────┬──────────────┘
                         ▼
                    E-Paper Hardware
```

Portable App 不应该自己写：

```text
if Kindle Paperwhite ...
if BOOX ...
if iReader ...
if firmware >= ...
```

这些差异应该留在 Platform Port、Device Profile 与 Quirk Set 中。

---

## Baga Ink 包含什么？

### Baga Ink Platform
运行在设备上的平台，负责承载 Portable Baga App、提供 Baga Ink API、处理 Lifecycle / Permission / Sandbox，并通过 Device Adapter 连接真实设备。

### Baga Device Adapter Contract
设备移植的 Typed Contract。它规定 Display、Input、Storage、Lifecycle、Power 以及 Optional Capability“必须提供什么”，但**不要求为了 Baga 重写已经存在的 OS / Vendor / Homebrew / Open Source 能力**。

### IKP 应用包
`.ikp` 是 Baga 的 Portable App Package。它和 Kindle `.kpkg`、MRPI Bundle、Android APK 等 Device-native Installer 是不同层级的东西。

### BICTS / Compatibility Evidence
Baga Ink Compatibility 不是一句“能跑”。目标是让 Device + Firmware + Platform + Adapter + Profile 的组合有 Capability、Contract Tests、BICTS 与明确 Compatibility Record 支撑。

### Baga Ink Client
计划中的 PC / Mac Client，用于 Device Detection、Bootstrap / Install、Offline Transfer、Diagnostics，以及在本身不适合承载现代 App Store 的设备上完成 App Delivery。

### Baga Ink Market 与 Distribution Protocol
Standards 定义 Publisher Identity、Signing、Repository Metadata、Catalog / Discovery、Update / Rollback / Revocation、Offline Transfer 和 Transparency，让开放 App 生态不会再次碎片化。

### Reference App
LifeBook 是旗舰 / Reference Product，用来证明一个真实大型 App 可以保持 Portable，而 Kindle、Android 墨水屏等差异由 Baga 吸收。公共仓库保留 Reference Architecture；LifeBook 正式产品 App 属于独立第一方产品。

---

## 第一个 Reference Platform：Kindle

Kindle 是第一块“硬骨头”：历史机型多、Firmware 组合复杂、资源有限、Homebrew 安装路径特殊，而且 E-Ink Refresh 本身高度设备化。

但 Kindle Strategy 不是从零重写 Kindle 支持。

Baga 会尽量站在成熟生态上，包括：

- KOReader / koreader-base；
- FBInk；
- Kindle OS 已有机制；
- 经过验证的 Kindle Homebrew Tooling。

Kindle Device Adapter 应尽量薄。只要底层已有成熟实现，Baga 新增代码主要集中在 Capability Detection、Normalization、Device Profile、Quirk Set、Error/Event Mapping、Self-test 与 Contract Tests。

最终普通用户看到的应该只是：

```text
Kindle Home
    ↓
Baga App（例如 LifeBook）
```

而 Jailbreak Route、KPM/MRPI、KOReader 内部、ABI Target 等都藏在 Portable App Contract 下面。

---

## Android 墨水屏和未来设备

**Baga Ink 不是 Kindle 专用项目。**

同一个 Device Adapter Contract 也面向 Android E-Paper 和未来设备家族。

Android 可以由 Generic Android Adapter 提供公共 Base，再由 Vendor Specialization 只覆盖真正不同的能力，例如：

- Refresh Mode；
- Pen；
- Frontlight；
- Vendor Private API。

增加一个新设备家族，不应该要求复制一份 App 生态。

---

## 核心设计原则

1. **App Portable，设备差异下沉**  
   Model、Firmware、Vendor、ABI 判断留在 App API 下面。

2. **Contract 重，具体 Adapter 轻**  
   标准必须稳定、完整、可测试；具体 Adapter 尽可能薄。

3. **优先复用成熟能力**  
   如果 KOReader、FBInk、OS、Vendor SDK、Homebrew 已经解决问题，就不要为了“完整”再造一个 Framebuffer / Reader / Input / Network / Power Stack。

4. **规范最终必须可执行**  
   重要行为要落到 Schema、IDL、Canonical Vector、Negative Fixture、Reference Implementation 与 Conformance Tests，而不是只停留在 Markdown。

5. **针对低资源、低功耗、弱联网现实设计**  
   墨水屏设备的 CPU、Memory、Storage、Battery 和 Network 往往比手机更受限。

6. **Portable App 不直接拿设备私有对象**  
   `.ikp` 不应该 import Kindle Private API、Android Vendor Object、KOReader Private API 或 Raw Device SDK Type。

7. **一个生态，兼容性可测量**  
   Community Port 和 OEM Port 实现同一个 Contract，也应该跑同一套 Test 来证明 Compatibility。

---

## 对普通 App 开发者意味着什么？

Baga Ink 的目标就是让 App 开发者尽量只关心 App。

Baga App 可以使用稳定能力，例如：

```text
baga.ui
baga.reader
baga.library
baga.storage
baga.network
baga.sync
baga.power
baga.permissions
baga.log
```

以及 Baga Lua Profile 中正式提供的 Standard Library，例如 SQLite Binding。

普通 IKP App 开发与 OEM / Platform Licensing 是两件不同的事情。**开发并销售一个只使用公开 Baga App API 的 IKP App，本身不需要购买 OEM / Platform Commercial License。**

---

## 对 Device Porter / OEM Engineer 意味着什么？

核心入口是 **Baga Device Adapter Contract**。

一个设备 Port 应回答：

```text
Display 实际有哪些能力？
Navigation / Touch / Pen Event 怎样 Normalize？
App-private Storage Sandbox 在哪里？
Sleep / Wake 怎样工作？
Power / Network / Light / Audio 能力是什么？
哪个 Device Profile / Quirk Set 生效？
哪些 Contract Tests / BICTS Result 证明这个组合？
```

而不是把 Vendor Detail 泄漏到 Portable App。

建议从这些文档开始：

- [Device Adapter Contract](docs/zh-CN/standards/07_设备适配器规范.md)
- [BICTS](docs/zh-CN/standards/10_兼容性测试套件.md)
- [Kindle Adapter](docs/zh-CN/standards/11_Kindle适配规范.md)
- [Android E-Paper Adapter](docs/zh-CN/standards/12_Android墨水屏适配规范.md)

---

## 项目状态

> **当前处于 Early Development / Standards + Executable Conformance + Reference Platform Implementation Preparation 阶段。**

已经建立：

- Standards 00–13 与 20–28 的完整中英文公共版本；
- Device Adapter Contract 与 Kindle / Android E-Paper Family Standards；
- Distribution / Signing / Repository 的 Executable Conformance 基础；
- Python Reference Verification；
- Device Adapter Executable IDL / SDK Design；
- 完整 Kindle Implementation Architecture Freeze；
- 受治理的 Kindle Task Design / Execution Prompt 流程；
- 受保护 `main` 与 Required CI Guard；
- 永久 English / 简体中文 Public Documentation Tree。

仍在进行：

- Machine-readable Device Adapter IDL 与 Generated Interface；
- Mock / Headless Adapter 与可复用 Contract Test Harness；
- 真正 Kindle Platform / Device Adapter 产品实现；
- Kindle 真机 BICTS Evidence；
- Android E-Paper Reference Implementation；
- Baga Ink Client / Market 产品；
- Standards Stable Release。

**当前仓库应被理解为正在实现中的 Platform / Standards Project，而不是已经完成的普通用户安装包。**

---

## 我应该从哪里开始？

### 先看懂平台
[简体中文文档入口](docs/zh-CN/00_项目文档入口.md) · [English Documentation](docs/en/00_baga-ink-documentation-index.md)

### 开发 Baga App
重点阅读 App Standard、API Specification、Capability Registry、Permission Model、IKP Package Specification 和 Standard Libraries Specification。

### 给一个设备做 Port
重点阅读 Standard 07、对应 Device Family Standard、Design 02 与 BICTS。

### 参与 Kindle 实现
阅读 Kindle Device Adapter Standard、[Kindle Implementation Architecture Freeze](docs/zh-CN/reference-apps/03_Kindle具体实现架构冻结.md)，以及 [`docs/plans/platform-ports/kindle/`](docs/plans/platform-ports/kindle/) 下的工程计划。

### 贡献代码或文档
先阅读 [`CONTRIBUTING.zh-CN.md`](CONTRIBUTING.zh-CN.md)。AI / Automation Contributor 还必须遵守 [`AGENTS.md`](AGENTS.md)。

---

## 仓库结构

```text
docs/en/        English Public Documentation
docs/zh-CN/     简体中文 Public Documentation
docs/plans/     Engineering Plans / Device Port Execution Material

spec/           Machine-readable Schema / Vector / Protocol Artifact
reference/      Reference / Independent Implementation
tests/          Conformance / Negative / Interoperability / Regression Test
tools/          Repository / Specification Tooling
.github/        CI / Conformance Workflow

platform/       Platform Implementation
sdk/            Generated / Platform SDK
client/         Baga Ink Client
```

长期 Source of Truth 是 `main`：Code + Machine Spec + Tests + Approved Public Docs。

---

## Roadmap

```text
Standards + Executable Conformance
        ↓
Machine-readable Device Adapter Contract + SDK
        ↓
Mock Adapter + Reusable Contract Tests
        ↓
Kindle Reference Platform / Adapter + Probe IKP
        ↓
LifeBook 在真实 Kindle 上运行
        ↓
Android E-Paper Reference Port
        ↓
Client / Market / 更广泛设备生态
```

兼容设备扩展依靠 **Native Build Target + Device Profile + Quirk Set + Test Evidence**，而不是复制 App Codebase。

---

## Licensing

Baga Ink 采用公开源码、开放开发和社区协作方式，欢迎个人、教育、研究、爱好者及其他 Community Use。

Baga 自研 Platform / OEM 侧软件默认采用仓库 Community License，除非具体文件或目录另有声明。OEM 商业设备 / Platform 的部署、预装、出货或商业再分发，需要单独商业协议。

**普通 IKP App 开发者与 OEM 不同：**只使用公开 Baga App API 开发并销售 App，本身不需要购买 OEM / Platform Commercial License。

正式 **LifeBook** App 属于 Proprietary 第一方产品，不包含在公共 Baga Platform 源码发行中。

KOReader、koreader-base、FBInk、KPM、KindleTool 等第三方组件保持各自上游 License。

详细规则：

- [`LICENSE`](LICENSE)
- [Baga Ink 授权策略](docs/zh-CN/governance/02_Baga-Ink授权策略.md)
- [`COMMERCIAL_LICENSE.zh-CN.md`](COMMERCIAL_LICENSE.zh-CN.md)
- [`LICENSE_HISTORY.md`](LICENSE_HISTORY.md)
- [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md)

---

## 参与开发

欢迎参与 Protocol / Specification Review、Rust/C/C++/Kotlin/Lua/Python Tooling、E-Paper Device Port、Conformance Tests、安全与 Distribution Infrastructure、OEM Compatibility Research、Documentation 与 Translation。

提交较大改动前请先阅读 [`CONTRIBUTING.zh-CN.md`](CONTRIBUTING.zh-CN.md)。

---

## 文档语言

Public Documentation Architecture 从一开始就按未来多语言设计，不允许不同 Locale 演变成不同 Protocol。

当前维护的 Root README：

- [English](README.md)
- **简体中文** — 本文件

未来可以通过 Localization Governance 增加 `README.ja.md`、`README.de.md`、`README.fr.md` 等以及对应 Locale Tree。

---

<div align="center">

**Baga Ink：一套 Portable Application Contract，连接更多 E-Paper Device。**

</div>
