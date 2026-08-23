# Baga Ink 当前项目状态 / Baga Ink Project Status

> **文档级别：项目状态唯一入口 / Canonical Project Status**  
> **状态：Living Status v0.2**  
> **日期：2026-08-23**  
> **权威分支：`main`**

---

## 0. 最重要的状态规则

本文件回答：

> **Baga Ink 现在真正做到哪里。**

任何 Feature Branch、聊天记录、PR 标题或旧计划都不能覆盖本文件与 `main` 中实际代码/测试所表达的当前状态。

如果本文件与实际 `main` 代码明显不一致，应优先核对代码与测试，并立即修正本文件。

---

# 1. 项目总状态

当前阶段：

> **平台标准体系已经建立；分发安全规范已经进入“可执行规范 / Conformance Kit”实施阶段；Kindle Reference Implementation 架构与 Device Adapter Contract 已形成明确基线，但真实 Kindle Platform / Adapter 产品代码尚未进入实现完成阶段。**

还没有进入：

- Baga Ink Platform 正式产品实现完成；
- Baga Ink Device Adapter SDK / IDL / Codegen 实现完成；
- Kindle Reference Adapter 实现完成；
- Baga Ink Client 正式产品实现完成；
- Baga Ink Market 正式产品实现完成；
- LifeBook 在真实 Kindle + Android E-Paper 上的完整跨设备产品闭环完成；
- Standards Stable 发布。

当前主线仍是：

> **完成 21–28 号身份、签名、Repository、更新与分发规范的机器可执行验证。**

同时，Kindle Platform 开工所需的 Device Adapter 标准边界已经补齐，不再需要从历史聊天推断“Adapter 到底是什么”。

---

# 2. 已完成：顶层标准体系

`docs/standards/` 已建立以下正式 Draft / Baseline 文档：

## 平台核心 00–09

```text
00 规范总览
01 顶层战略与架构
02 应用标准
03 API 规范
04 Capability 能力注册表
05 Permission 权限模型
06 IKP 应用包规范
07 Device Adapter Contract
08 Compatibility 兼容性标准
09 UI 规范
```

## 测试、设备适配与标准库 10–13

```text
10 BICTS 兼容性测试套件
11 Kindle Device Adapter
12 Android E-Paper Adapter
13 Standard Libraries / Adopted Components
```

## Market / Distribution / Signing 20–28

```text
20 市场与分发总体架构
21 Publisher Identity / App Ownership
22 IKP Signing / Key Lifecycle
23 Repository Metadata / Index Protocol
24 Publishing / Review / Version Policy
25 Update / Rollback / Revocation Protocol
26 Distribution Client / Offline Transfer
27 Transparency / Security Audit
28 Catalog / App Discovery
```

这些标准目前仍处于 Draft / Baseline 阶段；不能因为文件存在就宣称生产稳定。

---

# 3. 已完成：Reference App、Kindle Freeze 与 Device Adapter Contract

## 3.1 LifeBook Reference App

Reference App 主入口：

```text
docs/reference-apps/
01_LifeBook参考实现_LifeBook-Reference-App.md
```

已经锁定核心关系：

```text
LifeBook
   ↓
同一个 lifebook.ikp
   ↓
Baga Ink API / Baga Lua Profile
   ↓
Baga Ink Platform
   ↓
Device Adapter Contract
   ↓
Kindle / Android E-Paper
```

LifeBook 是旗舰 / Reference App，不是 Baga Ink Platform 本身。

## 3.2 Kindle Reference Implementation Architecture Freeze

已建立：

```text
docs/reference-apps/
03_Kindle具体实现架构冻结_Baga-Ink-Kindle-Implementation-Architecture-Freeze.md
```

状态：

> **FROZEN BASELINE v1.0.1**

该文档冻结：

```text
Client → jailbreak/bootstrap → Homebrew foundation
→ native Platform installer → Baga Ink Platform
→ IKP Package Manager → lifebook.ikp → Kindle Home Entry
```

核心边界包括：

- `.ikp` 不转换成 `.kpkg`；
- KPM 管 Platform native package，IKP Package Manager 管 Baga App；
- KPM 未安装与 KPM 不兼容严格分离；
- KPM-compatible 但缺失时先 bootstrap KPM；
- KPM-incompatible / unvalidated target 才使用 MRPI / legacy Platform installer envelope；
- 不建立 `Baga Platform Runtime` / `LifeBook Runtime` 正式架构层；
- Platform Core 保持最小职责；
- KOReader / koreader-base 由 Baga 私有、锁版本复用，LifeBook 不直接依赖 private API；
- sh_integration 作为第一阶段 Home/Library 入口；AppMgr 深化集成后续验证；
- KUAL / PEKI 为 legacy/admin/bootstrap fallback；
- KindleTool 是 build/package tooling；
- WinterBreak / SpringBreak / Sanctuary / Véra 只属于 Client Installation Route DB；
- Mesquito 不作为 Baga 直接采用模块；
- 同一个 `lifebook.ikp` 不随 native target 分叉；
- Platform update 与 IKP App update 分离；
- USB Mass Storage 使用文件式 handshake/mailbox，不假设 remote exec；
- 用户书籍、Kindle 笔记、App data / SQLite DB 必须受到保护；
- 用户产品路径是 `Kindle Home → LifeBook`，内部才经过 `LifeBook Home Entry → baga-launch → Platform → active lifebook.ikp`。

旧架构兼容入口已经移动为：

```text
99_旧版LifeBook架构与Kindle兼容实现_LifeBook-Architecture-and-Kindle-Compatibility-Superseded.md
```

它不再作为独立 Kindle implementation baseline。

## 3.3 Device Adapter Contract

`07` 已从“职责说明”升级为真正的：

> **Baga Ink Device Adapter Contract / Device Porting Contract**

已定义：

```text
AdapterFactory / probe / create
Root Adapter lifecycle
DeviceDescriptor
Capability Snapshot vs Runtime State
AdapterHost + typed event model
stable error model
Display/Input/Storage/Lifecycle/Power contracts
Optional Network/Light/Audio/Bluetooth/UserLibrary contracts
Native Build Target vs Device Profile vs Quirk
self-test
contract versioning
Adapter Contract Tests vs BICTS
Mock/Headless Adapter requirement
OEM/第三方移植流程
```

核心原则已经明确：

> **Device Adapter Contract 定义“设备要提供什么”，不要求重新实现已有设备能力。具体 Adapter SHOULD 最大复用 OS、Vendor SDK、Homebrew 和成熟开源项目。**

## 3.4 Kindle Device Adapter Reference Port

`11 Kindle Device Adapter` 已同步升级。

冻结 Kindle Adapter 的主要参考结构：

```text
common/
display/
input/
storage/
lifecycle/
power/
network/
light/
library/
device_profiles/
quirks/
build_targets/
```

明确：

```text
KOReader / FBInk / Kindle OS mechanisms
→ 可被 Device Adapter 复用

KOReader UIManager / ReaderUI / CREngine / MuPDF
→ Platform UI/Reader shared implementation，不是 Device Adapter 根契约

KPM / MRPI / sh_integration / Hotfix
→ install/bootstrap/Homebrew foundation，不是 Device Adapter

KindleTool
→ build/package tooling

Jailbreak routes
→ Client Installation Route DB
```

**注意：标准与架构完成不等于 Kindle Adapter 代码完成，也不等于任何具体 Kindle model/firmware 已通过 Contract Tests / BICTS。**

---

# 4. 已完成：Device Adapter Executable Contract / SDK Design

新增：

```text
docs/design/
02_设备适配器可执行契约与SDK设计_Baga-Ink-Device-Adapter-Executable-Contract-and-SDK-Design.md
```

Design Baseline 已确定下一阶段方向：

```text
spec/adapter machine-readable IDL
        ↓
codegen
        ├── Rust interfaces
        ├── C interfaces
        └── Kotlin interfaces
        ↓
Mock/Headless Adapter
        ↓
Adapter Contract Test harness
        ↓
Kindle / Android Adapter skeleton
```

第一阶段明确不做：

```text
dynamic native Adapter plugin ABI
Binder/RPC/JSON bridge
Adapter daemon
arbitrary dlopen third-party native module
```

目标是 direct typed call + compile/package-time Adapter implementation。

---

# 5. 已完成：Executable Specification 设计与实施计划

正式 Design：

```text
docs/design/
01_规范可执行化_Baga-Ink-Executable-Specification-Design.md
```

正式 Plan：

```text
docs/plans/
01_规范可执行化实施计划_Baga-Ink-Executable-Specification-Implementation-Plan.md
```

已确定总体方案：

> **语言无关机器规范 + Python Reference Implementation + Rust Independent Device Verifier。**

---

# 6. 已完成：机器可读规范基础

当前 `main` 已包含 `spec/`，正在将 21–28 转换为可执行规范。

已建立：

- JSON Schema；
- RFC 8785 / JCS Canonical Test Vector 基础；
- 固定 SHA-256 / Ed25519 测试向量；
- Publisher / App 身份相关机器对象；
- IKP Manifest / Signing 相关 Schema；
- Repository / Publishing / Update / Transfer / Transparency / Catalog Schema；
- 第一批 invalid fixtures / negative corpus。

机器格式不能长期与 `docs/standards/` 漂移成另一套协议；实现阶段发现的冲突必须回写文字标准。

`spec/adapter/` 尚未实现，只在 Design 中定义了目标结构。

---

# 7. 已完成：Python Reference Implementation 基础

当前存在：

```text
reference/python/src/baga_spec/
├── __init__.py
├── errors.py
├── strict_json.py
├── canonical.py
├── schemas.py
├── crypto.py
├── identity.py
├── signing.py
└── ikp.py
```

目前已经实现：

## Strict JSON

- UTF-8 严格解析；
- Duplicate Object Key rejection；
- NaN / Infinity rejection；
- 输入大小限制；
- 嵌套深度限制。

## Canonicalization

- RFC 8785 JCS；
- Stable canonical bytes；
- SHA-256 helper。

## Schema

- JSON Schema Draft 2020-12；
- Schema Registry / Loader；
- 安全关键未知字段拒绝。

## Crypto / Identity

- SHA-256；
- Ed25519；
- Key ID；
- Publisher ID；
- Publisher Genesis；
- App Ownership；
- App Signing Key Delegation；
- Delegation Channel / Sequence / Expiry 检查。

## IKP Signing / Validation

- `files.json` Payload Hash；
- Release Statement；
- Signature Set；
- ZIP 安全检查；
- Duplicate ZIP Entry rejection；
- Path Traversal rejection；
- Compression / Size limit；
- Universal IKP Native Executable rejection；
- Publisher → Ownership → Delegation → Release 离线验证链；
- Manifest / Release 交叉一致性检查。

---

# 8. 已完成：自动化测试基础

当前 `tests/` 包含：

```text
test_strict_json.py
test_canonical.py
test_schemas.py
test_crypto_vectors.py
test_identity.py
test_signing.py
test_ikp.py
test_invalid_fixtures.py
```

CI 基础：

```text
.github/workflows/conformance.yml
```

已经观察到：

- Strict JSON / JCS / Schema / Identity / Signing 第一阶段通过 Python CI；
- IKP Validator 阶段通过 Python CI；
- 非法样本库已经并入当前 `main` baseline。

**注意：这不等于 Stable Gate 已通过。**

---

# 9. 尚未完成：关键剩余项

## 9.1 Distribution Executable Specification

尚未完成：

```text
reference/python/src/baga_spec/repository.py
reference/python/src/baga_spec/client.py
tools/tuf-client-under-test
.github/workflows/tuf-conformance.yml
reference/rust/baga-verifier/
Python ↔ Rust cross-language vectors
Repository → Client → Device E2E
Offline Transfer prototype
Stable Gate
```

21–28 不能提升为 Stable。

## 9.2 Device Adapter Executable Contract

尚未完成：

```text
spec/adapter/
tools/baga-adapter-codegen/
sdk/adapter/generated/
Mock Device Adapter
Adapter Contract Test harness
```

## 9.3 Kindle Reference Adapter

尚未完成：

```text
platform/adapters/kindle/
KindleAdapterFactory
Kindle Device Profiles
Kindle Quirk Sets
Display/Input/Storage/Lifecycle/Power bindings
pinned KOReader/FBInk integration
real-device Contract Tests
Base BICTS
```

---

# 10. 当前下一步 / Next

## 主线 A：完成已有 Distribution Conformance 工作

```text
1. 完成 python-tuf Reference Repository
2. 完成 TUF Reference Client
3. 接入官方 tuf-conformance
4. 完成 Rust Independent Verifier
5. 跑 Python ↔ Rust Test Vectors
6. 跑 Repository → Client → Device E2E
7. 跑离线 Transfer / Update / Rollback
8. Stable Gate
```

## 设备平台线 B：Device Adapter / Kindle 开工顺序

当开始设备端实现时，已经不需要继续重新设计 Adapter 概念，按以下顺序：

```text
1. 建立 spec/adapter IDL schema
2. 冻结 Adapter Contract machine v0.1
3. 生成 Rust interface
4. 实现 Mock/Headless Adapter
5. 建立 Adapter Contract Test harness
6. 建立 KindleHF Adapter skeleton
7. 绑定 pinned KOReader / FBInk / Kindle mechanisms
8. 跑 Kindle Base Adapter Contract Tests
9. 跑 Baga Probe IKP
10. 跑 Base BICTS
11. 再扩展 network/light/library 与 kindlepw2/legacy
12. 再生成/验证 Kotlin Android Adapter interface
```

Kindle 具体模块采用仍必须服从：

```text
docs/reference-apps/03_Kindle具体实现架构冻结_Baga-Ink-Kindle-Implementation-Architecture-Freeze.md
```

---

# 11. Git / Branch 当前状态

本轮 Executable Specification 工作原先在临时：

```text
feat/executable-spec-conformance
```

施工。

其有效内容已经通过 PR #1 **Squash Merge 到 `main`**。

因此：

> **该 Feature Branch 不再具有任何项目知识价值。**

当前 GitHub 连接没有提供 Delete Branch Ref 写接口，因此暂时无法从这里直接物理删除它。

已经把该 Branch 强制移动到本轮 Merge 后的 `main` Commit，使其不再包含独立/领先内容。

任何开发者或 AI：

- MUST 忽略该 Branch；
- MUST 以 `main` 为准；
- 有 GitHub 删除权限时 SHOULD 删除该 Branch。

以后不允许 Branch 承担项目上下文保存职责。

---

# 12. 当前文档入口

```text
总文档入口
→ docs/00_项目文档入口_Baga-Ink-Documentation-Index.md

当前状态
→ 本文件

标准
→ docs/standards/00_规范总览_Baga-Ink-Standards-Index.md

Device Adapter Contract
→ docs/standards/07_设备适配器规范_Baga-Ink-Device-Adapter-Specification.md

Kindle Device Adapter
→ docs/standards/11_Kindle适配规范_Baga-Ink-Kindle-Adapter.md

Device Adapter executable contract / SDK design
→ docs/design/02_设备适配器可执行契约与SDK设计_Baga-Ink-Device-Adapter-Executable-Contract-and-SDK-Design.md

开发治理
→ docs/governance/00_开发治理_Baga-Ink-Development-Governance.md

LifeBook Reference App
→ docs/reference-apps/01_LifeBook参考实现_LifeBook-Reference-App.md

Kindle Implementation Architecture Freeze
→ docs/reference-apps/03_Kindle具体实现架构冻结_Baga-Ink-Kindle-Implementation-Architecture-Freeze.md
```

---

# 13. 什么时候更新本文件

以下事件发生时 SHOULD / MUST 更新：

- 一个 Standards 区间完成；
- Device Adapter Contract 正式 revision；
- Adapter IDL/Codegen/Mock milestone 完成；
- 一个 Reference Implementation 阶段完成；
- 重要 CI Gate 通过；
- 新设备 Adapter 正式支持；
- LifeBook 跨设备里程碑完成；
- Kindle Freeze 发生正式 Architecture Decision revision；
- Draft → Stable；
- 当前优先级发生变化；
- 某项“未完成”变为“完成”。

---

**新的开发者或 AI 不需要阅读历史 Branch 或聊天记录；从本文件和 `main` 即可继续项目。**
