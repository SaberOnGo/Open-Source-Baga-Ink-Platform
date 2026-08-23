# Baga Ink 当前项目状态 / Baga Ink Project Status

> **文档级别：项目状态唯一入口 / Canonical Project Status**  
> **状态：Living Status v0.1**  
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

> **平台标准体系已经建立；分发安全规范已经进入“可执行规范 / Conformance Kit”实施阶段；Kindle Reference Implementation 的具体架构已经形成 FROZEN BASELINE，但 Kindle 产品代码尚未进入正式实现完成阶段。**

还没有进入：

- Baga Ink Platform 正式产品实现完成；
- Baga Ink Client 正式产品实现完成；
- Baga Ink Market 正式产品实现完成；
- LifeBook 在真实 Kindle + Android E-Paper 上的完整跨设备产品闭环完成；
- Standards Stable 发布。

当前重点仍是：

> **先证明 21–28 号身份、签名、Repository、更新与分发规范能够被机器严格执行，再继续扩大实现。**

Kindle 代码未来开工时，必须以已经落库的 Kindle Architecture Freeze 为实现与模块选型基线，不再从历史聊天恢复架构。

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
07 Device Adapter 设备适配器规范
08 Compatibility 兼容性标准
09 UI 规范
```

## 测试与设备适配 10–12

```text
10 BICTS 兼容性测试套件
11 Kindle Adapter
12 Android E-Paper Adapter
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

# 3. 已完成：Reference App 与 Kindle 实现架构冻结

Reference App 主入口：

```text
docs/reference-apps/
01_LifeBook参考实现_LifeBook-Reference-App.md
```

已经锁定的核心关系：

```text
LifeBook
   ↓
同一个 lifebook.ikp
   ↓
Baga Ink API / Baga Lua Profile
   ↓
Baga Ink Platform
   ↓
Device Adapter
   ↓
Kindle / Android E-Paper
```

LifeBook 是旗舰 / Reference App，不是 Baga Ink Platform 本身。

## 3.1 Kindle Reference Implementation Architecture Freeze

已建立：

```text
docs/reference-apps/
03_Kindle具体实现架构冻结_Baga-Ink-Kindle-Implementation-Architecture-Freeze.md
```

状态：

> **FROZEN BASELINE v1.0**

该文档已经冻结后续 Kindle 代码开工必须遵守的关键实现边界，包括：

```text
Client → jailbreak/bootstrap → Homebrew foundation
→ native Platform installer → Baga Ink Platform
→ IKP Package Manager → lifebook.ikp → Kindle Home launch
```

以及：

- `.ikp` 不转换成 `.kpkg`；
- KPM 管 Platform native package，IKP Package Manager 管 Baga App；
- KPM 未安装与 KPM 不兼容严格分离；
- KPM-compatible 但缺失时先 bootstrap KPM；
- KPM-incompatible / unvalidated target 才使用 MRPI / legacy Platform installer envelope；
- 不建立 `Baga Platform Runtime` / `LifeBook Runtime` 正式架构层；
- Platform Core 保持最小职责；
- KOReader / koreader-base 由 Baga 私有、锁版本复用，LifeBook 不直接依赖 private API；
- sh_integration 作为第一阶段 Home/Library 入口；AppMgr 深化集成后续验证；
- KUAL / PEKI 为 legacy/admin/bootstrap fallback，不是正常 LifeBook 路径；
- KindleTool 是 build/package tooling；
- WinterBreak / SpringBreak / Sanctuary / Véra 只属于 Client Installation Route DB；
- Mesquito 不作为 Baga 直接采用模块；
- 同一个 `lifebook.ikp` 不随 `kindlepw2` / `kindlehf` 等 native target 分叉；
- Platform update 与 IKP App update 分离；
- USB Mass Storage 使用文件式 handshake/mailbox，不假设 remote exec；
- 用户书籍、Kindle 笔记、App data / SQLite DB 必须受到保护。

旧：

```text
02_LifeBook架构与Kindle兼容实现_LifeBook-Architecture-and-Kindle-Compatibility.md
```

已标记 `SUPERSEDED / 兼容入口`，只指向 `03`，不再作为独立 Kindle implementation baseline。

`01_LifeBook参考实现...` 已同步修正其 Kindle Homebrew / KPM / MRPI / KUAL / KOReader 角色表述，避免与 `03` 竞争。

**注意：架构冻结完成不等于 Kindle Platform 产品实现完成，也不等于任何具体 Kindle model/firmware 已通过 BICTS。**

---

# 4. 已完成：Executable Specification 设计与实施计划

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

# 5. 已完成：机器可读规范基础

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

---

# 6. 已完成：Python Reference Implementation 基础

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

目前已经实现的能力包括：

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

# 7. 已完成：自动化测试基础

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

已经观察到的验证里程碑：

- Strict JSON / JCS / Schema / Identity / Signing 第一阶段通过 Python CI；
- IKP Validator 阶段通过 Python CI；
- 非法样本库已经并入当前 `main` baseline。

**注意：这不等于 Stable Gate 已通过。**

---

# 8. 尚未完成：Executable Specification 关键剩余项

以下是当前最重要的未完成工作。

## 8.1 TUF Repository / Client

尚未完成正式 Reference Implementation：

```text
reference/python/src/baga_spec/repository.py
reference/python/src/baga_spec/client.py
```

需要：

- 使用当前 `python-tuf` 官方 API；
- 真实生成 Root / Targets / Snapshot / Timestamp；
- Repository Target / Baga custom metadata；
- 客户端 Refresh / Download；
- Rollback / Freeze / Mix-and-match 负向测试。

## 8.2 TUF Official Conformance

尚未完成：

```text
tools/tuf-client-under-test
.github/workflows/tuf-conformance.yml
```

必须实现官方 Harness 要求的：

```text
init
refresh
download
```

并运行 TUF 官方 Conformance Suite。

## 8.3 Rust Independent Verifier

尚未完成：

```text
reference/rust/baga-verifier/
```

目标不是重写 Market，而是独立验证设备关键安全语义：

- Strict JSON；
- JCS；
- SHA-256；
- Ed25519；
- Publisher Identity；
- Ownership；
- Delegation；
- Release Signature；
- IKP Payload Hash。

## 8.4 Cross-language Test Vectors

尚未完成完整 Python ↔ Rust 双实现一致性 Gate。

要求：

```text
same valid vectors  → both ACCEPT
same invalid vectors → both REJECT
same canonical bytes → exact byte equality
```

## 8.5 Minimal Repository → Client → Device E2E

尚未完成完整闭环：

```text
Publisher
  ↓
Signed IKP
  ↓
TUF Repository
  ↓
Reference Client
  ↓
Device Verifier
  ↓
Stage / Activate / Rollback
```

## 8.6 Offline Transfer

26 号标准已经存在，但最小 Portable Repository Snapshot / USB transfer 原型尚未完成。

## 8.7 Stable Gate

尚未达到。

21–28 不能提升为 Stable。

---

# 9. 当前下一步 / Next

当前工程优先级仍然是：

```text
1. 完成 python-tuf Reference Repository
2. 完成 TUF Reference Client
3. 接入官方 tuf-conformance
4. 完成 Rust Independent Verifier
5. 跑 Python ↔ Rust Test Vectors
6. 跑 Repository → Client → Device E2E
7. 跑离线 Transfer / Update / Rollback
8. 修正文档与机器格式之间剩余漂移
9. Stable Gate 全绿后再评审 21–28 Stable
```

在此之前，不应优先扩展 Market UI、付费、DRM 等非核心功能。

当进入 Kindle 产品实现阶段时，第一入口不是重新做架构讨论，而是直接按：

```text
docs/reference-apps/03_Kindle具体实现架构冻结_Baga-Ink-Kindle-Implementation-Architecture-Freeze.md
```

中已经定义的 Compatibility/Bootstrap PoC → Minimum Platform Core → KOReader mapping → LifeBook skeleton → 多设备扩展顺序执行。

---

# 10. Git / Branch 当前状态

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

# 11. 当前文档入口

```text
总文档入口
→ docs/00_项目文档入口_Baga-Ink-Documentation-Index.md

当前状态
→ 本文件

标准
→ docs/standards/00_规范总览_Baga-Ink-Standards-Index.md

开发治理
→ docs/governance/00_开发治理_Baga-Ink-Development-Governance.md

LifeBook Reference App
→ docs/reference-apps/01_LifeBook参考实现_LifeBook-Reference-App.md

Kindle Implementation Architecture Freeze
→ docs/reference-apps/03_Kindle具体实现架构冻结_Baga-Ink-Kindle-Implementation-Architecture-Freeze.md
```

---

# 12. 什么时候更新本文件

以下事件发生时 SHOULD / MUST 更新：

- 一个 Standards 区间完成；
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
