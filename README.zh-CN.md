<div align="center">

# Baga Ink Platform

### 面向墨水屏设备的开放应用平台

**应用只面对一套稳定平台 API；Kindle、Android 墨水屏以及未来设备的差异，由各自 Platform Port / Device Adapter 吸收。**

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](LICENSE)
[![Project status](https://img.shields.io/badge/status-early%20development-orange.svg)](#项目状态)
[![Documentation](https://img.shields.io/badge/docs-简体中文-2ea44f.svg)](docs/zh-CN/00_项目文档入口.md)

<!-- BAGA-LANG-SWITCH:START -->
**语言：** [English](README.md) · **简体中文** · [＋ 增加一种语言](CONTRIBUTING.zh-CN.md#翻译与多语言)
<!-- BAGA-LANG-SWITCH:END -->

</div>

---

## Baga Ink 到底是什么？

**Baga Ink 是一个面向墨水屏 / E-Paper 设备的开放应用平台与兼容性标准。**

今天，如果你为一台墨水屏设备开发应用，通常很难把它原样搬到另一台设备上。Kindle Homebrew、Android 墨水屏、不同厂商 SDK、Linux 墨水屏设备，在下面这些地方都可能完全不同：

- 屏幕刷新机制；
- 触摸、按键、手写笔输入；
- 文件与存储路径；
- Sleep / Wake 生命周期；
- 电源、前光、网络等设备能力；
- 应用安装、更新与打包方式；
- 不同型号和 Firmware 的兼容性问题。

结果就是：**每做一个应用，都可能又做一遍设备适配。**

Baga Ink 想把这件事反过来：

> **应用只适配 Baga Ink；设备差异只在 Baga Ink 的 Platform Port / Device Adapter 中解决一次。**

你可以把它理解成：

> **墨水屏领域的“应用平台 + 设备兼容层 + 可验证兼容性标准”。**

它不是一个新的操作系统，也不是要求用 Baga 替换 Kindle OS 或 Android。

---

## 我们想解决什么问题？

| 现在常见的问题 | Baga Ink 的方向 |
|---|---|
| App 里充斥型号、厂商、Firmware 判断 | 这些差异集中在 Device Adapter / Device Profile / Quirk Set |
| 每家设备都有不同的刷新与输入 API | App 只使用统一的 Baga Ink display / input 语义 |
| 每个平台安装包和更新方式不同 | Baga App 使用跨设备 `.ikp` 应用包 |
| “应该能跑”常靠经验猜 | Capability + Contract Tests + BICTS 提供验证证据 |
| 不断重新实现底层设备能力 | 最大化复用 OS、Vendor SDK、Homebrew 与成熟开源项目 |
| 一个应用移植后就绑死一个设备家族 | 同一个 App Contract 面向 Kindle、Android E-Paper 和未来平台 |

长期目标很直白：

> **一台进入 Baga Ink Compatible 范围的墨水屏设备，应该能够运行同一个 Baga 应用生态，而不是每一个 App 都重新做一套设备移植。**

---

## 架构怎么工作？

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

一个可移植 Baga App 不应该自己写：

```text
if Kindle Paperwhite ...
if BOOX ...
if iReader ...
if firmware >= ...
```

这些东西应该留在 Platform Port、Device Profile、Quirk Set 里。

---

## Baga Ink 不只是一层 API

Baga Ink 最终是一套完整但尽量轻量的开放生态。

### Baga Ink Platform
运行在设备上的平台。负责承载 Baga App、提供 Baga Ink API、处理 App Lifecycle / Permission / Sandbox，并通过 Device Adapter 接入真实设备。

### Baga Device Adapter Contract
设备移植的稳定契约。它规范 Display、Input、Storage、Lifecycle、Power 以及可选设备能力“必须提供什么”，但**不要求为了 Baga 重写设备底层实现**。

### IKP 应用包
Baga 的跨设备应用包格式：`.ikp`。它和 Kindle 的 `.kpkg`、APK、MRPI 等 Native Installer 是不同层级的东西。

### Baga Ink Compatibility / BICTS
用 Capability、Contract Tests、BICTS 与 Compatibility Record 来证明某个 Device + Firmware + Platform + Adapter 组合是否真的兼容。

### Baga Ink Client
计划中的 PC / Mac 客户端，用于设备识别、Bootstrap / Install、离线传输、诊断，以及那些本身不适合承载现代 App Store 的设备。

### Baga Ink Market 与分发协议
定义 Publisher Identity、App Ownership、Signing、Repository Metadata、Update / Rollback / Revocation、Catalog / Discovery、Transparency 与 Offline Transfer。

### Reference App
**LifeBook** 是旗舰 / Reference App，用来证明：业务 App 可以只面对 Baga Ink，而 Kindle、Android 墨水屏和未来设备差异留在平台下面。

---

## 第一个 Reference Platform：Kindle

Kindle 很适合作为第一块“硬骨头”：历史机型多、Firmware 组合复杂、资源有限、Homebrew 安装环境特殊，而且电子墨水刷新本身就很设备化。

但我们的 Kindle 策略不是从零重写一套 Kindle 支持。

Baga 会尽量站在成熟生态上，包括：

- KOReader / koreader-base；
- FBInk；
- Kindle OS 已有机制；
- 经过验证的 Kindle Homebrew 工具链。

理想的 Kindle Device Adapter 应该尽量薄，新增代码主要集中在：

```text
Capability Detection
Device Profile
Quirk Set
Event / Error Normalization
Baga Interface Glue
Self-test
Contract Tests
```

而不是重新造：

```text
Framebuffer Stack
Input Stack
Reader Engine
Network Stack
Power Manager
```

最终普通用户看到的应该只是：

```text
Kindle Home
    ↓
Baga App（例如 LifeBook）
```

而 Jailbreak、KPM、MRPI、KOReader 内部实现等细节都应该藏在平台下面。

---

## Android 墨水屏和未来设备

**Baga Ink 不是一个 Kindle 专用项目。**

同一个 Device Adapter Contract 也面向 Android E-Paper 和未来设备家族。

Android 方向可以由 Generic Android Adapter 提供基础能力，再由 BOOX、iReader、Bigme、Hanvon 等 Vendor Specialization 只覆盖真正不同的部分，例如：

- 墨水屏 Refresh Mode；
- Pen；
- Frontlight；
- Vendor Private API。

增加新设备不应该要求复制一份 LifeBook 或复制一套 Baga App 生态。

---

## 核心设计原则

1. **App 可移植，设备差异下沉**  
   型号、Firmware、Vendor 判断不要扩散到 Portable App。

2. **Contract 重，具体 Adapter 轻**  
   标准必须完整、稳定、可测试，但具体 Adapter 应尽可能薄。

3. **优先复用成熟能力**  
   能复用 KOReader、FBInk、OS、Vendor SDK、Homebrew，就不要为了“看起来完整”重新造轮子。

4. **规范最终要能执行和验证**  
   重要协议不能永远只停留在 Markdown，要落到 Schema、IDL、Canonical Vector、Negative Fixture、Reference Implementation 和 Conformance Test。

5. **针对低资源、低功耗、弱联网现实设计**  
   墨水屏设备往往 CPU、内存、电量、存储、网络都比手机更受限。

6. **Portable App 不直接拿设备私有对象**  
   `.ikp` 不应该直接依赖 Kindle Private API、Android Vendor Object、KOReader Private API 或 Raw Device SDK Type。

7. **开放生态必须可测量兼容性**  
   OEM 和第三方移植者实现的是同一个 Contract，也应该跑同一套测试来证明兼容性。

---

## Baga Ink 不是什么？

Baga Ink **不是**：

- 一个新的 E-Reader 操作系统；
- 把 KOReader 换个名字包装成新平台；
- 要求替代 Kindle OS 或 Android；
- 要求重新实现所有硬件驱动；
- 宣称现在已经支持所有 Kindle / Android 墨水屏；
- 一个当前已经可以给普通用户直接安装使用的成熟发行版。

它正在构建的是：

> **Portable Apps 与高度碎片化的墨水屏设备环境之间那一层稳定平台。**

---

## 项目状态

> **当前处于 Early Development / Standards / Reference Implementation 阶段。**

仓库已经拥有：

- 比较完整的 Draft / Baseline Standards 体系；
- Distribution / Signing / Repository 等方向的可执行 Conformance 基础；
- Baga Device Adapter Contract；
- Kindle / Android E-Paper Adapter 规范；
- Kindle Reference Implementation Architecture Freeze；
- 文档、任务与 AI 执行流程的机器校验规则。

但仍然没有完成：

- Device Adapter Machine IDL + Generated SDK；
- Mock / Headless Adapter 与完整 Adapter Contract Tests；
- 真正的 Kindle Platform / Adapter 产品实现；
- Kindle 真机完整 BICTS；
- Android E-Paper Reference Port；
- Baga Ink Client / Market 产品；
- 全部英文公共技术文档迁移；
- Standards Stable 发布。

**所以现在更应该把这个仓库理解为一个正在实现中的开放平台 / 标准工程，而不是已经完成的用户安装包。**

---

## 我应该从哪里开始？

### 我想先看懂 Baga Ink
从 [简体中文文档入口](docs/zh-CN/00_项目文档入口.md) 开始；英文开发者可进入 [English Documentation](docs/en/00_baga-ink-documentation-index.md)。

### 我想开发一个 Baga App
重点阅读 App Standard、API、Capability、Permission、IKP Package Specification。公共规范目前正在迁移到新的 `docs/zh-CN/` / `docs/en/` 结构中。

### 我想给一个新设备 / OEM 做适配
核心入口是 **Baga Device Adapter Contract**，然后再读对应 Device Family Adapter Standard 与 BICTS。

### 我想参与 Kindle 实现
Kindle 工程任务在 [`docs/plans/platform-ports/kindle/`](docs/plans/platform-ports/kindle/) 中维护，包括 Task Design、Execution Prompt、真机验证与实现计划。

### 我想贡献代码或文档
先读 [`CONTRIBUTING.zh-CN.md`](CONTRIBUTING.zh-CN.md)。AI / 自动化 Agent 还必须遵守 [`AGENTS.md`](AGENTS.md)。

---

## 仓库结构

```text
docs/en/        英文公共文档
docs/zh-CN/     简体中文公共文档
docs/plans/     工程计划、设备移植任务与执行资料

spec/           机器可读 Schema / Vector / Protocol Artifacts
reference/      Reference / Independent Implementation
tests/          Conformance / Negative / Interoperability / Regression Tests
tools/          Repository / Specification Tooling
.github/        CI / Conformance Workflows

platform/       未来 / Reference Platform 实现区域
sdk/            未来 Generated / Platform SDK 区域
client/         未来 Baga Ink Client 实现区域
```

长期目标是让一个完全不了解项目历史的人或 AI，仅通过：

```text
main 中的代码
+ Machine Spec
+ Tests
+ Approved Public Docs
```

就能继续参与开发，而不需要回头翻历史聊天记录。

---

## Roadmap

当前大方向：

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
Client / Market / 更多设备生态
```

扩展设备支持依靠：

```text
Native Build Target
+ Device Profile
+ Quirk Set
+ Test Evidence
```

而不是复制一份 App 代码。

---

## License

Baga Ink 项目**自研内容默认采用 Apache License 2.0**，除非某个文件或目录明确声明了其他许可证。详见 [`LICENSE`](LICENSE) 和 [`NOTICE`](NOTICE)。

Baga 会主动复用大量第三方开源项目，但**不会因为 Baga 自己采用 Apache-2.0，就把第三方项目重新许可成 Apache-2.0**。

例如 KOReader、koreader-base、FBInk、KPM 与 Kindle Homebrew 项目都继续遵守它们各自的上游许可证。某个实际发行版如果把 AGPL / GPL 组件组合进去，就必须同时满足对应的 Copyleft 义务。

详见 [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md)。

---

## 欢迎参与

Baga Ink 从一开始就按照长期多人协作项目来设计。欢迎参与：

- Standard / Protocol 设计与 Review；
- Rust、C/C++、Kotlin/Java、Lua、Python；
- E-Paper Display / Input / Lifecycle Adapter；
- Kindle / Android E-Paper Bring-up；
- Conformance / Interoperability Tests；
- Signing / Update / Repository / Distribution；
- OEM / Device Compatibility 研究；
- 技术文档与多语言翻译。

较大的修改请先阅读 [`CONTRIBUTING.zh-CN.md`](CONTRIBUTING.zh-CN.md)。

---

## 多语言

README 与公共技术文档的结构已经为更多语言预留。

当前维护：

- [English](README.md)
- **简体中文** — 当前页面

后续可以增加：

```text
README.ja.md
README.de.md
README.fr.md
README.ko.md
...
```

并在该语言真正进入项目维护范围时增加对应 Locale Documentation Tree。多语言不能演变成多套协议；不同语言始终描述同一个 Baga Ink Contract。

翻译规则见 [`docs/zh-CN/governance/01_文档国际化与本地化规范.md`](docs/zh-CN/governance/01_文档国际化与本地化规范.md)，参与翻译见 [`CONTRIBUTING.zh-CN.md`](CONTRIBUTING.zh-CN.md#翻译与多语言)。

---

<div align="center">

**Baga Ink：一套可移植应用契约，连接不同墨水屏设备。**

</div>
