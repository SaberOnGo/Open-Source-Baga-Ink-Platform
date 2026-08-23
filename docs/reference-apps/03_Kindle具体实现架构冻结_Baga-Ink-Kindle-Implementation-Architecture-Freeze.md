# Baga Ink Kindle 具体实现架构冻结 / Baga Ink Kindle Implementation Architecture Freeze

> **文档级别：Kindle Reference Implementation Architecture Freeze / Kindle 参考实现架构冻结**  
> **状态：FROZEN BASELINE v1.0**  
> **日期：2026-08-23**  
> **适用范围：Baga Ink Client、Baga Ink Platform on Kindle、Baga Ink Kindle Adapter、LifeBook (`lifebook.ikp`)**  
> **上位约束：`docs/standards/` 全部当前有效规范**  
> **配套 Reference App：`01_LifeBook参考实现_LifeBook-Reference-App.md`**

---

## 0. 文档地位与冻结规则

本文档把 Baga Ink Standards、LifeBook Reference App、Kindle Homebrew 生态与 2026-08-23 前形成的 Kindle 架构讨论收敛为一套**可直接指导代码开工、依赖选型、打包、安装、启动、更新、回滚与兼容测试的 Kindle 实现基线**。

优先级：

```text
Baga Ink Standards
        >
本 Kindle Implementation Architecture Freeze
        >
其他 Kindle Reference / Product 补充文档
        >
具体代码与原型
```

如果本文件与上位 Standards 冲突，必须先服从 Standards，再修订本文件。

从本文件进入 `FROZEN` 状态后，下列变化不得在代码中静默发生：

- 改变 `.ikp` 与 `.kpkg` 的职责边界；
- 新增 `Baga Runtime / Baga Platform Runtime / LifeBook Runtime` 等正式架构层；
- 让 LifeBook 直接依赖 KOReader / Kindle 私有 API；
- 改变 KPM / MRPI / sh_integration / KUAL / PEKI / KindleTool 的定位；
- 改变 Kindle Native Build Target / ABI Profile；
- 改变 Platform Core 的基本职责；
- 改变 IKP Package Manager 的信任、安装、更新或回滚语义；
- 把某个 jailbreak exploit 固化为 Platform dependency。

如确需改变，必须先形成显式 Architecture Decision，更新本文档，再修改代码与测试。

---

# 1. 一页结论

Kindle 最终实现链冻结为：

```text
                         Baga Ink Client
                                │
                                ▼
                  Detect Kindle / Current State
                                │
                                ▼
                  Installation Route Resolver
                    （仅 Platform 未就绪时）
                                │
          ┌─────────────────────┴─────────────────────┐
          ▼                                           ▼
   Stock / not homebrew-ready                 Already homebrew-ready
          │                                           │
          ▼                                           │
WinterBreak / SpringBreak / Sanctuary / Véra /       │
legacy / future verified route                        │
          │                                           │
          └─────────────────────┬─────────────────────┘
                                ▼
                         Homebrew Ready
                                │
                                ▼
                        KPM compatible?
                   ┌────────────┴────────────┐
                  YES                        NO
                   │                          │
             KPM installed?                  │
             ┌─────┴─────┐                   │
            YES          NO                   │
             │            │                   │
             │      bootstrap/install KPM     │
             │            │                   │
             └─────┬──────┘                   │
                   ▼                          ▼
        baga-platform*.kpkg        MRPI / legacy/manual envelope
                   │                          │
                   └────────────┬─────────────┘
                                ▼
                    Baga Ink Platform on Kindle
                                │
                    ┌───────────┼───────────┐
                    ▼           ▼           ▼
              Platform Core  Kindle Adapter Adopted Components
                    │                       KOReader/FBInk/etc.
                    ▼
               IKP Package Manager
                    │
                    ▼
                lifebook.ikp
                    │
                    ▼
                   LifeBook
```

必须同时冻结以下核心边界：

1. **`.ikp` 永远不转换为 `.kpkg`。**
2. **KPM 管理 Kindle 原生的 Baga Platform 安装/升级；IKP Package Manager 管理 Baga App。**
3. **“KPM 没安装”与“KPM 不兼容”是完全不同的状态。**
4. KPM-compatible 但未安装 KPM：**先安装 KPM，再走 `.kpkg`**；不得直接降级为长期 MRPI 路线。
5. 只有 KPM 对该设备/ABI/Homebrew 组合**确实不可用或未通过 Baga 验证**时，才采用 MRPI / legacy/manual Platform installer envelope。
6. **LifeBook 是 Universal IKP App，不是 Kindle Homebrew package。**
7. **不存在正式的 `Baga Platform Runtime` 架构层。** Lua/LuaJIT 只是 Platform Core 内部嵌入/复用的执行能力。
8. **KOReader 是 Kindle Platform 内部 Adopted Component，不是 LifeBook API。**
9. Baga 必须管理一份**锁定版本、经过 BICTS 验证的 KOReader/koreader-base 组件集合**；第一版不依赖用户自行安装的 KOReader。
10. **WinterBreak / SpringBreak / Sanctuary / Véra 是 Installation Route records，不是 Platform dependencies。**
11. **Mesquito 不作为 Baga 直接采用模块。** 若某 route 内部使用它，那只是 route implementation detail。
12. **KUAL / PEKI 不是正常用户路径，也不是 LifeBook dependency。** 只允许作为经 Compatibility DB 验证的 legacy/bootstrap/admin fallback。
13. **KindleTool 是构建/打包工具，不是 Runtime，也不是 App Manager。**
14. Kindle Home 正常产品路径必须是：**Kindle Home → LifeBook → Baga launcher → LifeBook**，不暴露 KOReader/KUAL 给普通用户。
15. 第一期首页入口优先采用成熟 `sh_integration` Scriptlet；更深的 AppMgr registration 作为后续可替换增强。

---

# 2. 公共架构与 Kindle 实现映射必须分开

Baga 的公共架构仍然只有：

```text
IKP App
   ↓
Baga Ink API / Baga Lua Profile
   ↓
Baga Ink Platform Core
   ↓
Baga Ink Device Adapter
   ↓
OS / Hardware
```

Kindle 内部可以大量复用：

```text
KOReader
koreader-base
LuaJIT
UIManager / widgets
ReaderUI
CREngine
MuPDF
FBInk
SQLite / lsqlite3 / lua-ljsqlite3
Automerge core（适用时）
KPM
Hotfix / sh_integration
MRPI
KindleTool
KUAL / PEKI（仅 fallback）
```

但这些**不得因为被采用就变成新的 Baga 公共层**。

禁止重新引入：

```text
Baga Runtime
Baga Platform Runtime
LifeBook Runtime
Kindle Runtime
KOReader Runtime Layer（作为 Baga 公共架构层）
Provider Framework（仅因为复用一个库而创造）
Engine Layer（仅因为复用一个库而创造）
```

技术上 LuaJIT 当然是 Lua 的执行环境；KOReader 也拥有 LuaJIT 驱动的脚本环境。但在 Baga 架构中，它们只是 Platform implementation details。

---

# 3. 两套 Package Manager，两个完全不同的层

## 3.1 Kindle Homebrew 层：KPM

KPM 是 Kindle 原生 Homebrew Package Manager。

当前上游 KPM 使用 `.kpkg`，支持 package manifest、version、dependency 与可选的：

```text
install.sh
launch.sh
uninstall.sh
```

这些 hooks 由 Kindle 的 `sh` 执行。

Baga 使用 KPM 的对象是：

```text
baga-platform_<version>_<target>.kpkg
```

它可以包含目标 ABI 对应的：

```text
Baga Platform Core native parts
Kindle Adapter native parts
Baga launcher
pinned KOReader/koreader-base components
Lua/LuaJIT
native libraries
Platform install/update/uninstall hooks
home-entry bootstrap assets
```

KPM **不得成为 Universal App contract**。

## 3.2 Baga Platform 层：IKP Package Manager

IKP Package Manager 是 Platform Core 内部的跨设备 App Package Manager。

它管理：

```text
lifebook.ikp
rss-reader.ikp
notes.ikp
other Universal IKP Apps
```

它不是 KPM fork，也不是 KPM wrapper；可以借鉴成熟 package-manager 设计，但必须遵守 Baga IKP / Signing / Update / Rollback Standards。

## 3.3 明确禁止转换

永远不存在：

```text
lifebook.ikp
    ↓ convert
lifebook.kpkg
```

也不存在：

```text
lifebook.ikp
    ↓ MRPI package
LifeBook.bin
```

正确关系是：

```text
Kindle native infrastructure
baga-platform*.kpkg / *.bin / legacy bundle
        ↓
安装 Baga Ink Platform
        ↓
IKP Package Manager
        ↓
lifebook.ikp
```

---

# 4. KPM capability：必须区分“未安装”与“不兼容”

这是实现状态机中的硬规则。

## 4.1 状态 A：KPM compatible + installed

```text
install/update baga-platform.kpkg
```

这是首选路径。

## 4.2 状态 B：KPM compatible + NOT installed

不得写成：

```text
No KPM → MRPI fallback
```

必须写成：

```text
KPM capable?
    YES
     │
KPM installed?
    NO
     │
bootstrap/install KPM
     │
install baga-platform.kpkg
```

Client 可以随安装介质携带经过验证的 KPM/bootstrap 资源；实际触发方式取决于当前 Homebrew foundation，例如已有 post-jailbreak foundation、sh_integration、MRPI 或其他 Compatibility DB 允许的 bootstrap channel。

如果 MRPI 被用来**第一次把 KPM 装进去**，它只是 bootstrap transporter；后续 Baga Platform 生命周期仍可以回到 KPM。

## 4.3 状态 C：KPM incompatible / unavailable

只有满足下列之一，才允许进入长期 fallback：

- 当前 KPM 没有该 native target；
- 当前设备/ABI/Homebrew combination 未被 KPM upstream 支持；
- Baga Compatibility Record 判定该组合的 KPM 不可靠；
- KPM 安装路径在该设备上无法满足数据保护 / rollback / lifecycle 要求。

此时使用：

```text
MRPI .bin
legacy/manual bundle
other verified native installer envelope
```

但里面安装的仍是**同一 Baga Platform release/source 与 API 语义**，不是另一套 Platform。

## 4.4 当前 KPM 支持基线的事实边界

截至 2026-08-23，上游 KPM 官方 repository 中 KPM 0.2.x artifact 的 `supported_platforms` 为：

```text
kindlepw2
kindlehf
```

KPM 自己的 `package/install.sh` 也只处理这两个 native KPM binary 目录。

KPM helper 虽然允许 package manifest 使用：

```text
kindle
kindle5
kindlepw2
kindlehf
```

但“某个 package manifest 可以声明 target”**不等于当前 KPM 本体已经在所有 target 上可运行**。

因此 Baga Client 不得凭 manifest target 名猜测 KPM capability；KPM capability 必须来自可更新 Compatibility / Installation DB 与 Baga 实测记录。

---

# 5. 一个 Platform Release，多种 native installer envelope

不要建立：

```text
KPM版 Baga
MRPI版 Baga
KUAL版 Baga
WinterBreak版 Baga
```

应该建立：

```text
              Baga Platform Release X
                        │
            ┌───────────┴───────────┐
            ▼                       ▼
     target: kindlepw2        target: kindlehf
            │                       │
     ┌──────┴──────┐         ┌──────┴──────┐
     ▼             ▼         ▼             ▼
   .kpkg          .bin      .kpkg          .bin

legacy targets
→ legacy/manual or MRPI-compatible envelope as validated
```

“同一 Platform”指：

- 同一 source release；
- 同一 Baga API / Lua Profile contract；
- 同一 Platform Core 逻辑与数据格式；
- 同一 IKP semantics；
- 目标 ABI 差异只存在于 native artifacts / adopted binaries。

不要求不同 target 的二进制字节相同。

---

# 6. Kindle Native Build Targets / ABI Profiles

不要再称为“Runtime Build Target”。正式名称：

> **Kindle Native Build Target / ABI Profile**

当前 Reference engineering mapping 继续站在 KOReader / Kindle Homebrew 已长期验证的 target family 上：

| Kindle 工程族 | Reference target | 用途 |
|---|---|---|
| K2 / K3 / DXG 等 legacy | `kindle-legacy` | 旧 ABI / 低资源 legacy build |
| K4 / Touch / PW1 等 classic | `kindle` | classic build / legacy install path |
| PW2+ soft-float 路径 | `kindlepw2` | PW2+ soft-float native build |
| hard-float 路径 | `kindlehf` | hard-float native build |

现有 Baga Kindle Adapter Standard 把 firmware `5.16.3` 作为 soft-float/hard-float 的重要 Reference engineering 边界；它是**native build/compatibility 边界**，不是 LifeBook IKP contract。

任何 native component：

```text
Platform Core native code
KOReader/koreader-base
FBInk
SQLite native library / binding
Automerge native bridge（若采用）
KPM / launcher
```

必须按目标 ABI 构建、锁版本并经过 Compatibility Record + BICTS。

`lifebook.ikp` 不随这些 target 分叉。

---

# 7. Baga Ink Platform Core：冻结为小 Core

Platform Core 不得膨胀为大型“Runtime Framework”。

冻结职责只有以下六类：

```text
Baga Ink Platform Core
│
├─ 1. IKP Package Management
│   ├─ package validation
│   ├─ stage / activate
│   ├─ update / rollback
│   └─ uninstall
│
├─ 2. App Registry
│   ├─ installed apps
│   ├─ active release
│   └─ package/data state
│
├─ 3. App Lifecycle
│   ├─ start / resume / pause
│   ├─ sleep / wake
│   └─ stop / update / uninstall
│
├─ 4. Embedded Lua Host
│   ├─ Baga Lua Profile
│   └─ load validated entry main.lua
│
├─ 5. Permission / Sandbox / Capability
│   ├─ permission enforcement
│   ├─ app-private paths
│   └─ capability view
│
└─ 6. Baga API Dispatch
    └─ baga.* → Device Adapter / adopted implementation
```

Platform Core **不包含**：

```text
LifeBook account/business logic
Articles / Q&A / Comments
Life Records / Time Capsule
LifeBook AI
LifeBook cloud product policy
Baga Ink Client
Baga Ink Market
```

Platform Core 也不会因为采用下列项目就增加同名架构层：

```text
KOReader
MuPDF
CREngine
SQLite
Automerge
FBInk
```

---

# 8. IKP Package Manager：具体实现冻结

IKP Package Manager 是 Platform Core 的一个组件，不是独立用户产品，也不要求后台 daemon。

## 8.1 可以向 KPM 学什么

可以借鉴：

```text
package identity
manifest
version/release state
installed package registry
stage/install/update/uninstall lifecycle
simple repository/package separation
```

## 8.2 绝不能照搬 KPM 的什么

IKP 不允许 KPM 式任意：

```text
install.sh
launch.sh
uninstall.sh
raw shell hook
```

Universal IKP 只执行经过验证、受 Baga Lua Profile 与 Permission/Sandbox 约束的 App code。

## 8.3 第一版职责

```text
IKP Package Manager
│
├─ Container Reader
│   └─ ZIP-compatible IKP
│
├─ Manifest Validator
│   ├─ app id / version / release_sequence
│   ├─ entry
│   ├─ Baga API range
│   ├─ permissions
│   └─ required/optional capabilities
│
├─ Security Validator
│   ├─ canonical path / Zip Slip prevention
│   ├─ decompression limits
│   ├─ payload hash
│   ├─ publisher/signing chain
│   └─ revocation / identity continuity
│
├─ Compatibility Check
│
├─ Staging / Atomic Activation
│
├─ Rollback / Last-known-good
│
├─ Uninstall
│
└─ App Registry
```

第一版明确**不做**：

```text
APT-style dependency solver
cross-App shared native dependency resolver
arbitrary install script system
background package daemon
App-to-App private directory dependency
```

## 8.4 成熟库复用

IKP Package Manager 不自行重新实现 ZIP、JSON、SHA-256、签名算法、SQLite。

应直接采用成熟、许可证兼容、可锁版本的实现，并按上位 Signing / IKP / Standard Libraries 规范测试。

App Registry MAY 使用 Platform-managed SQLite；这属于实现选择，不改变 IKP contract。

## 8.5 推荐目录语义

逻辑结构冻结为：

```text
/mnt/us/baga/
├─ bin/
├─ platform/
├─ apps/
│  └─ <app-id>/
│     ├─ releases/
│     │  └─ <release-sequence>/
│     ├─ active.json / equivalent registry state
│     └─ data/                  # package 与 data 必须分离
├─ staging/
├─ inbox/
├─ outbox/
└─ device.json
```

精确物理目录 MAY 因安全/文件系统要求调整，但以下语义不可改变：

- installed package 与 App private data 分离；
- release 目录应不可变或按等价语义保护；
- activation 必须可原子切换或具备等价崩溃一致性；
- rollback 不得删除用户数据；
- staging 不得直接成为 active package。

---

# 9. LifeBook IKP：正常执行链

LifeBook 正式包始终是：

```text
lifebook.ikp
```

包含：

```text
manifest.json
main.lua
src/
assets/
locales/
signature/
```

不包含：

```text
Kindle native executable
Kindle shell bridge
KPM package
MRPI package
KOReader binary/runtime copy
Device Adapter
Platform Core
```

安装后启动链：

```text
Kindle Home
    │
    ▼
LifeBook Home Entry
    │
    ▼
/mnt/us/baga/bin/baga-launch com.lifebook
    │
    ▼
Platform Core
    │
    ├─ read App Registry
    ├─ verify active release state
    ├─ create App Context
    ├─ apply Permission / Sandbox / Capability view
    └─ initialize Baga Lua Profile
    │
    ▼
validated main.lua
    │
    ▼
LifeBook
```

正常 App 启动时 **KPM 不在热路径中**。

---

# 10. KOReader：大量复用，但必须对 LifeBook 隐身

## 10.1 冻结采用策略

Kindle Reference Platform SHOULD 最大化复用：

```text
KOReader / koreader-base
LuaJIT
UIManager / widgets
ReaderUI
CREngine
MuPDF
Annotation / Highlight / Bookmark
position / search / selection
Kindle device/input/display knowledge
FBInk（适用时）
```

但 LifeBook IKP 不得出现：

```lua
require("ui/uimanager")
require("apps/reader/readerui")
```

也不得依赖 KOReader private sidecar / internal object 作为 Universal contract。

正确路径：

```text
LifeBook
  │
  ├─ baga.ui
  ├─ baga.reader
  ├─ baga.display
  └─ baga.input
        │
        ▼
Baga Kindle implementation
        │
        ▼
KOReader / koreader-base / FBInk internals
```

## 10.2 pinned private copy

第一版 Baga 必须管理自己的 pinned KOReader/koreader-base 组件集合。

禁止默认依赖：

```text
/mnt/us/koreader/
用户 nightly
用户 userpatch
用户第三方 plugin
用户自行升级后的 KOReader ABI/API
```

推荐内部目录名：

```text
platform/components/koreader/
platform/vendor/koreader/
```

避免把目录命名为 `runtime/koreader`，防止重新制造 “Baga Runtime” 概念。

未来只有在**精确版本/commit/ABI/patch set 与 Baga 验证矩阵完全匹配**时，MAY 共享用户 KOReader；第一版不做此优化。

## 10.3 `baga.koplugin` 的位置

将 Baga Kindle integration 做成 Platform 私有 `.koplugin` 是一个允许验证的轻量 PoC：

```text
baga-launch
  ↓
pinned KOReader substrate
  ↓
Platform-private baga.koplugin
  ↓
Baga root UI / reader integration
```

但它必须被标记为：

> **implementation technique, not public architecture and not IKP API**

如果后续发现直接调用内部模块比 plugin lifecycle 更稳定，可以替换，不需要改变 LifeBook 或 Baga API。

---

# 11. Kindle Home Entry：sh_integration 优先，AppMgr 后续深化

产品长期体验必须是：

```text
Kindle Home
   ↓ one action
LifeBook
```

普通用户不得必须经过：

```text
KUAL
KOReader File Manager
KOReader Plugin Menu
KPM CLI
```

## Phase 1：sh_integration Scriptlet

优先采用成熟 `sh_integration`：

```text
/documents/LifeBook.sh
    ↓
/mnt/us/baga/bin/baga-launch com.lifebook
```

`sh_integration` 已解决 Kindle Library 中 shell script 的注册/提取/启动问题，并有成熟 AppMgr/scanner 研究基础。

第一版不要直接自行编辑：

```text
appreg.db
cc.db
```

## Phase 2：更原生 AppMgr entry

如果产品体验确有必要，可在验证后复用 `sh_integration` 已有的 AppMgr registration 机制，形成更原生的 Kindle application entry。

该优化必须保持：

```text
Home entry
→ baga-launch <app-id>
```

不得让 LifeBook 自己获得 Kindle AppMgr 私有依赖。

---

# 12. Homebrew Foundation：复用，不再造一套

Baga 不创建新的：

```text
Baga Kindle Homebrew Foundation
```

而是识别并复用已验证的 Kindle Homebrew foundation，例如其组合中的：

```text
Hotfix
sh_integration
KPM（目标兼容时）
MRPI（需要时）
```

Baga Client 负责识别 foundation state；LifeBook IKP 完全不感知。

Homebrew foundation 只是 Kindle implementation prerequisite，不是 Baga App contract。

---

# 13. KPM / MRPI / KindleTool / KUAL / PEKI：最终定位

| 项目 | 冻结定位 | 正常 LifeBook 启动依赖？ |
|---|---|---|
| **KPM** | KPM-compatible Kindle 上首选 Baga Platform native install/update manager | 否 |
| **MRPI** | 非 KPM / legacy Platform installer fallback；也可在特定流程充当 bootstrap transporter | 否 |
| **KindleTool** | CI/build/package tooling，用于构建/检查 Kindle OTA/MRPI `.bin` 等 | 否 |
| **sh_integration** | 首选 Home/Library Scriptlet integration；可提供 bootstrap execution point | 间接作为 Kindle integration，但对 LifeBook API 隐身 |
| **Hotfix** | Homebrew persistence/foundation 的 upstream 组成部分，按 Compatibility DB 识别 | 否 |
| **KUAL** | legacy/fallback admin/launcher/bootstrap 工具；不是现代产品入口 | 否 |
| **PEKI** | 某些组合的 KUAL/bootstrap compatibility tool，仅 route DB 允许时采用 | 否 |

禁止写出：

```text
LifeBook depends on KUAL
LifeBook package = KPM package
KPM not installed → permanent MRPI path
KindleTool Runtime
MRPI App Manager for IKP
```

---

# 14. WinterBreak / SpringBreak / Sanctuary / Véra：Installation Routes only

这些项目不属于：

```text
Platform Core
device-facing Baga API
LifeBook IKP dependency
Baga Runtime
```

它们只解决：

> **如何让某个精确 Kindle model + firmware + current state 达到 homebrew-ready。**

冻结模型：

```text
Baga Installation Route DB
│
├─ WinterBreak
├─ SpringBreak
├─ Sanctuary
├─ Véra
├─ legacy routes
└─ future routes
```

每个 route record 至少记录：

```text
route_id
upstream source/version
supported model(s)
exact firmware/range
current state prerequisites
registration requirement
Wi-Fi requirement
PC/USB requirement
free-space / device-state requirement
known risks
Baga tested status
last verified date
preferred/fallback priority
```

Route Resolver 排序原则：

1. 已经 homebrew-ready 时不重复 jailbreak；
2. 必须精确匹配 model + firmware；
3. 优先 Baga 已验证成功率更高、恢复风险更低的 route；
4. 再考虑用户前置要求与步骤复杂度；
5. upstream 新路线只进入 Experimental，经过验证后再提升 Preferred；
6. 未知固件默认 Experimental / Unsupported，不按“同系列应该差不多”推断。

不要把某一 jailbreak 当前支持范围硬编码进 Platform Core；范围随 upstream 变化，应更新 Route DB。

## Mesquito

Mesquito 不作为 Baga 直接采用项目。

如果 WinterBreak 等 route 内部利用 Mesquito：

```text
WinterBreak = Baga 可选择的 Installation Route
Mesquito    = upstream route implementation detail
```

Baga 只验证 route 的输入条件、结果状态与安全边界。

---

# 15. Baga Ink Client：从“安装 LifeBook”到设备可启动的完整状态机

用户产品动作可以仍是：

```text
Install LifeBook
```

但 Client 内部必须拆为两个独立事务：

```text
A. Ensure Baga Platform
B. Transfer/Install LifeBook IKP
```

## 15.1 Ensure Platform

```text
Detect device
   ↓
Platform present and healthy?
   ├─ YES → skip bootstrap
   └─ NO
       ↓
Homebrew ready?
   ├─ NO → Installation Route Resolver
   └─ YES
       ↓
KPM compatible?
   ├─ YES
   │    ↓
   │  KPM installed?
   │    ├─ YES
   │    └─ NO → bootstrap KPM
   │             ↓
   │       install baga-platform.kpkg
   │
   └─ NO → MRPI / legacy verified installer envelope
       ↓
Verify Platform health / version / Adapter / BICTS compatibility
```

## 15.2 Transfer LifeBook

```text
Client selects compatible lifebook.ikp
       ↓
Client verifies/cache metadata as allowed
       ↓
transfer signed evidence + .ikp
       ↓
Device Platform verifies again
       ↓
IKP stage
       ↓
atomic activate
       ↓
create/update Home Entry
```

Platform install 与 App install 必须分别记录、分别诊断。

---

# 16. USB Mass Storage：文件式 Handshake / Mailbox

PC 看到普通 Kindle USB Mass Storage 时只能可靠地读写文件，不能假设可以远程 `exec()` Kindle command。

因此 Kindle Reference Implementation SHOULD 采用一个简单文件 mailbox，作为 `26_分发客户端与离线传输协议` 的 Kindle implementation profile：

```text
/mnt/us/baga/
├─ device.json
├─ inbox/
│  └─ <transfer-id>/
│     ├─ transfer-manifest.json
│     ├─ repository-evidence/...
│     └─ lifebook.ikp
└─ outbox/
   └─ <result-id>.json
```

`device.json` 可暴露必要而非敏感的信息，例如：

```text
transfer protocol version
Platform version
Baga API / Lua Profile version
Kindle native target / ABI profile
firmware compatibility record id
Capability digest
installed inventory digest
free storage
```

不得默认暴露用户账号、书库正文、笔记正文。

## 16.1 不要求后台 daemon

第一版不需要为了 USB mailbox 建立常驻 daemon。

处理 inbox 可以由：

- Platform 启动时；
- LifeBook/Home Entry 启动前；
- 明确的 Baga Setup/Install Scriptlet；
- 已有安全 lifecycle hook；

触发。

如果未来引入 daemon，必须先证明其功耗、sleep/wake、资源与恢复价值。

---

# 17. Bootstrap execution point：PC 不能“凭空执行 Kindle 命令”

当 Platform 尚未安装时，Client 复制了文件也不等于安装已执行。

必须存在一个设备端 execution point，例如：

```text
existing sh_integration Scriptlet
existing MRPI
verified post-jailbreak hook/foundation
other route-specific launcher
```

推荐现代流程之一：

```text
Client writes local bootstrap/KPM repo/assets
        ↓
Baga Setup.sh appears in Kindle Library
        ↓ user one-time action
sh_integration executes Setup
        ↓
ensure KPM
        ↓
install baga-platform.kpkg
        ↓
remove/hide one-time Setup entry
```

具体 bootstrap mechanism 由 Compatibility / Installation DB 决定；不成为 Universal Baga contract。

---

# 18. 更新、回滚与数据保护

## 18.1 Platform update

```text
KPM / MRPI / native installer envelope
→ 更新 Baga Platform native components
```

必须保护：

```text
用户 Kindle 书籍
用户 Kindle 笔记
Baga app private data
LifeBook SQLite DB
LifeBook local notes / records
last-known-good Platform/App state
```

## 18.2 IKP App update

```text
IKP Package Manager
→ verify
→ stage immutable release
→ migration compatibility check
→ atomic activation
→ probation/health check
→ rollback if needed
```

KPM/MRPI 的“覆盖文件”语义不得替代 IKP Update Protocol。

## 18.3 App package 与 data 永远分离

```text
apps/<id>/releases/*
        ≠
apps/<id>/data/
```

回滚 App package 不应自动回滚用户数据；涉及 data schema 时遵守 IKP Update/Rollback Standard 的 migration/snapshot 规则。

---

# 19. Compatibility / BICTS：支持对象必须是精确组合

“支持某一代 Kindle”不是正式 Compatibility 声明。

一条可发布的 Compatibility Record 至少绑定：

```text
Device Model / family
+ exact Firmware / tested range
+ Homebrew foundation state
+ Native Build Target / ABI Profile
+ Baga Platform version
+ Kindle Adapter version
+ Baga Lua Profile version
+ adopted component versions/commits
+ BICTS version/result
```

状态：

```text
Compatible
Experimental
Unsupported
```

固件升级后至少回归：

```text
bootstrap/install
Platform launch
IKP install/update/rollback
lifecycle sleep/wake
UI/display/input
storage/sandbox/SQLite
reader/library/anchor（如声明）
network
home entry
recovery/data protection
```

---

# 20. 模块采用矩阵

| 模块/项目 | 冻结结论 | 位置 |
|---|---|---|
| Baga Ink Platform Core | **采用，自研最小 Core** | Platform |
| IKP Package Manager | **采用，实现 Standards；参考 KPM 思路但不 fork KPM contract** | Platform Core |
| Lua / LuaJIT | **采用/复用** | Embedded Lua Host implementation |
| KOReader | **大量采用，pinned private** | Kindle Platform internal |
| koreader-base | **大量采用** | Kindle Platform internal |
| KOReader Plugin mechanism | **MAY，用于内部 PoC/集成** | Platform internal only |
| UIManager / widgets | **SHOULD 复用** | `baga.ui` Kindle implementation |
| ReaderUI / CREngine / MuPDF | **SHOULD 复用** | `baga.reader` Kindle implementation |
| FBInk | **SHOULD/MAY 按实际映射复用** | display/internal |
| KPM | **KPM-compatible target 首选 Platform installer/update manager** | Homebrew/native install |
| sh_integration | **首选一期 Home Entry / bootstrap trigger** | Kindle integration |
| AppMgr deeper integration | **Phase 2 MAY** | Kindle integration |
| Hotfix | **复用 upstream foundation，Client 识别** | Homebrew foundation |
| MRPI | **legacy/KPM-incompatible fallback；必要时 bootstrap transporter** | native install/bootstrap |
| KindleTool | **采用** | CI/build/package tooling |
| KUAL | **fallback/admin only** | legacy compatibility |
| PEKI | **fallback/bootstrap only** | legacy compatibility |
| WinterBreak | **route record only** | Client Installation Route DB |
| SpringBreak | **route record only** | Client Installation Route DB |
| Sanctuary | **route record only** | Client Installation Route DB |
| Véra | **route record only** | Client Installation Route DB |
| Mesquito | **不直接采纳** | upstream route implementation detail |
| SQLite / lsqlite3 | **按 Standard 采用** | Standard Library / Platform |
| Automerge core | **按 Standard 采用，适用业务再用** | Adopted Foundation |
| 用户自行安装 KOReader | **第一版不依赖** | outside Baga contract |
| `Baga Platform Runtime` | **禁止作为正式层/术语** | N/A |

---

# 21. 明确禁止清单 / MUST NOT

后续实现与 AI 生成代码不得违反以下规则：

```text
MUST NOT convert .ikp to .kpkg.
MUST NOT publish LifeBook canonical app as .kpkg.
MUST NOT use KPM as IKP App Package Manager.
MUST NOT create a formal Baga Platform Runtime layer.
MUST NOT require LifeBook to import KOReader private Lua APIs.
MUST NOT require a user-managed KOReader installation in v1.
MUST NOT expose KUAL/PEKI as the normal LifeBook product path.
MUST NOT equate "KPM not installed" with "KPM unsupported".
MUST NOT hardcode jailbreak exploit code into Platform Core.
MUST NOT make WinterBreak/SpringBreak/Sanctuary/Véra Platform dependencies.
MUST NOT directly adopt Mesquito as a Baga module solely because a route uses it.
MUST NOT hand-edit appreg.db/cc.db as the v1 default while mature sh_integration mechanisms exist.
MUST NOT let MRPI/KPM overwrite semantics replace IKP staged update/rollback.
MUST NOT let Kindle model/firmware branches leak into lifebook.ikp business code.
MUST NOT create another Reader engine when KOReader/CREngine/MuPDF already satisfy the mapped need.
```

---

# 22. 第一阶段代码开工顺序

## Phase 0：Compatibility / Bootstrap PoC

先证明，而不是先写 LifeBook 大量业务：

1. 建立 Kindle device detector + Route DB schema；
2. 选代表性 `kindlepw2` 与 `kindlehf` 设备；
3. 验证 Homebrew-ready → KPM capability → Platform `.kpkg` 安装；
4. 验证 KPM-compatible but missing KPM 的 bootstrap；
5. 验证至少一个非 KPM/legacy installer envelope；
6. 验证 sh_integration Home entry；
7. 验证 `Kindle Home → baga-launch`。

## Phase 1：Minimum Platform Core

```text
App Registry
IKP package reader/validator
staging / activation / rollback
Embedded Lua Host
minimal baga.app / storage / device / log
Permission/Sandbox skeleton
Kindle Adapter skeleton
filesystem mailbox
```

## Phase 2：KOReader mapping

```text
pinned KOReader/koreader-base
baga.ui → UIManager/widgets
baga.input → KOReader Kindle input
baga.display → KOReader/FBInk
baga.reader → ReaderUI/CREngine/MuPDF
```

验证 Platform-private `.koplugin` 是否是最轻集成方式；它不是必须保留的架构。

## Phase 3：LifeBook skeleton IKP

只做：

```text
lifebook.ikp
main.lua
home/navigation
SQLite/offline start
Library/Reader basic
notes basic
```

确认同一 IKP contract 没有 Kindle private import。

## Phase 4：多机型/固件扩展

按 Compatibility DB 增加设备组合，不通过复制 LifeBook 代码分支扩展。

---

# 23. 仍属于 PoC / 未冻结到具体实现细节的事项

以下内容允许实验，但实验不得改变本文已冻结边界：

- Platform Core 的主要实现语言（Rust/C/C++/Lua 组合）；
- IKP App Registry 的具体 SQLite schema；
- ZIP/JSON/crypto 的具体库，只要符合 Standards 与许可证；
- `baga.koplugin` 是否最终保留；
- AppMgr Phase 2 是否值得做；
- mailbox 的精确文件名/transaction journal 格式；
- Automerge 在 Kindle 的具体 C/Rust/Lua bridge；
- legacy 每个型号最终使用哪个 `.bin`/manual envelope；
- 每个 jailbreak route 当前的精确支持范围与 preferred ranking。

这些必须通过 PoC、真实 Kindle 与 BICTS 决定；不得用猜测提前写死为平台契约。

---

# 24. 与现有 Reference 文档的关系与修正

## `01_LifeBook参考实现_LifeBook-Reference-App.md`

继续作为 LifeBook Universal App 的高层参考实现规范。

本文补足它没有定义的 Kindle bootstrap、KPM/IKP 双 package manager、Home Entry、native installer envelope 与 route resolver 细节。

## `02_LifeBook-Kindle产品行为与外设扩展设计...`

继续负责低刷新、低功耗、网络、Audio/Bluetooth、Accessory/Dock 等产品行为和实验方向。

该文档不得覆盖本文的 Kindle install/bootstrap/Platform/IKP 架构冻结。

## 原 `02_LifeBook架构与Kindle兼容实现...`

其有效内容已由本文吸收；若保留文件名，应作为兼容入口指向本文，避免形成两个互相竞争的 Kindle implementation baseline。

---

# 25. 上游依据与持续验证

本文冻结的是 **Baga 对上游组件的职责边界和采用策略**，不是把上游当前版本永久锁死。

主要上游依据：

- KPM: https://github.com/KindleModding/KPM
- Official KPM repository manifest: https://github.com/KindleModding/repo/blob/main/manifest.v2.json
- sh_integration: https://github.com/KindleModding/sh_integration
- KindleModding jailbreak docs / Wizard: https://kindlemodding.org/
- KindleTool: https://github.com/NiLuJe/KindleTool
- KOReader: https://github.com/koreader/koreader
- koreader-base: https://github.com/koreader/koreader-base

发布每个 Baga Platform Release 时必须记录：

```text
upstream project
version / commit
source digest
license
native target
Baga patches（如有）
BICTS result
```

Jailbreak Route DB、KPM capability 与固件范围必须可以独立更新，不要求修改 Universal App contract。

---

# 26. 最终冻结语句

从本文件开始，Kindle 的 Baga Ink 实现统一理解为：

> **Baga Ink Client 先把精确 Kindle 带到经过验证的 Homebrew/Platform-ready 状态；KPM-compatible 设备优先由 KPM 管理 Baga Platform native package，KPM-incompatible 设备使用 MRPI/legacy installer envelope；Platform Core 内部以最小 Core + IKP Package Manager + Embedded Lua Host + Kindle Adapter 运行 Universal IKP；KOReader/koreader-base 被大量、私有、锁版本地复用作为 Kindle implementation substrate；LifeBook 始终只是 `lifebook.ikp`，只面对 Baga Ink API / Baga Lua Profile，从 Kindle Home 一次操作进入，绝不感知 jailbreak、KPM、MRPI、KUAL、KOReader 私有 API 或设备 ABI。**

这就是后续 Kindle 代码开工、模块采用与兼容实现的默认基线。
