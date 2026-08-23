# Baga Ink 应用发布、审核与版本政策 / Baga Ink App Publishing, Review and Version Policy

> **文档级别：分发层发布与治理规范**  
> **状态：Draft v0.2**  
> **日期：2026-08-23**  
> **上位文档：`20_市场与分发总体架构_Baga-Ink-Market-and-Distribution-Architecture.md`**  
> **身份规范：`21_发布者身份与应用所有权标准_Baga-Ink-Publisher-Identity-and-App-Ownership-Standard.md`**  
> **签名规范：`22_IKP签名与密钥生命周期标准_Baga-Ink-IKP-Signing-and-Key-Lifecycle-Standard.md`**  
> **应用与标准库：`02_应用标准_Baga-Ink-App-Standard.md`、`03_API规范_Baga-Ink-API-Specification.md`、`13_标准库与成熟组件采用规范_Baga-Ink-Standard-Libraries-and-Adopted-Components.md`**

---

## 0. 目的

本文档定义 Baga Ink Market 及兼容第三方 Repository 中应用的注册、上传、版本、Channel、审核、发布、撤回和重新提交规则。

本规范把两类事情分开：

```text
协议与身份规则
= 什么软件字节属于谁、什么版本不可变、设备怎样安全验证

Market Policy
= 某个市场愿意收录什么、怎样审核、怎样展示和治理
```

Repository 可以有不同内容政策，但不得改变 App Identity、IKP Signature、Release Sequence、Permission、Capability、Baga Lua Profile / Standard Library 或 Update Safety 的标准语义。

---

# 1. 发布对象

正式发布对象包括：

```text
Publisher Identity
App Ownership
Signed IKP
Release Record
Repository Metadata Entry
Catalog Metadata
Optional Review Attestation
Optional Build / Source Attestation
```

Market 必须保留开发者原始 Publisher Signature，不得把 IKP 重新签成 Market 所有。

Market 可签署 Repository Metadata、Review Attestation、Policy Classification、Withdrawal / Revocation Record、App Transfer Attestation；这些不能替代 Publisher Signature。

---

# 2. App 注册

首次发布前必须注册：

```text
app_id
publisher_id
app_ownership_digest
primary display name
primary category
contact information
```

官方 Market 必须检查：

1. App Ownership 签名有效；
2. `app_id` 未被其他 Publisher 合法占用；
3. 命名空间按适用规则验证；
4. 当前账号有权管理 Publisher；
5. App ID 不冒充 Baga Ink、LifeBook、设备厂商或其他受保护名称；
6. App ID 与可见名称差异不构成欺骗。

---

# 3. 版本双字段模型

每个 Release 必须同时拥有：

```text
version_name
release_sequence
```

`version_name` 面向人类；`release_sequence` 是同一 `app_id` 全局单调递增的安全排序整数。

规则：

- 不因 Channel 分开计数；
- 不因 Repository 不同重置；
- 正式发布后不得复用；
- 自动更新只比较受信任 Release Sequence，不解析 `version_name` 排序。

---

# 4. Release 不可变性

正式发布由：

```text
app_id
release_sequence
package_sha256
```

唯一确定。

一旦进入签名 Repository Metadata：

- 相同 `app_id + release_sequence` 必须永久指向同一 IKP Digest；
- CDN 不得静默替换；
- 任何字节变化必须发布更高 Sequence；
- Catalog 文案可更正，但 Package 身份不能改；
- 原 Release 可 Withdraw / Revoke，但不能被改写。

相同 Sequence 不同 Digest 必须视为安全冲突并拒绝。

---

# 5. Release Channel

v0.x 标准 Channel：

```text
stable
beta
nightly
```

Channel 不是 App Identity、Permission Boundary 或独立 Release Sequence 空间。

用户默认 stable；切换 Channel 必须显式执行。较新测试 Channel 返回较低 Stable Sequence 属显式 Downgrade，不是普通更新。

---

# 6. 发布前本地验证

Baga Ink SDK 必须提供：

```text
baga validate app.ikp
baga inspect app.ikp
baga sign app.ikp
baga verify app.ikp
```

至少检查：

- IKP Container / path safety；
- Manifest Schema；
- App ID / Release Sequence / API Range；
- Capability / Permission；
- Baga Lua Profile 合规性；
- Standard Library 使用是否来自正式 Profile；
- 禁止的设备私有执行依赖；
- 禁止的随机 native dependency / bundled duplicate runtime；
- 文件 Hash；
- Publisher Identity / Ownership / Delegation / Release Signature；
- 基础 Catalog 字段；
- 包大小与资源限制。

特别规则：

```text
require("lsqlite3")
→ 正式 Baga Lua Profile Standard Library，允许

baga.data
→ 已撤销 API，不允许作为正式依赖

App 自带另一份 libsqlite3 / lsqlite3 native runtime
→ Universal IKP 默认不允许

Automerge native runtime
→ 当前 developer-facing Lua Standard Library 尚未冻结；若由 Platform/官方受控能力集成则按对应标准审核，普通 IKP 不得随机携带设备 ABI native binary
```

---

# 7. Market 上传接收

Market 接收 Release：

```text
Receive bytes
  ↓
Calculate SHA-256 / length
  ↓
Store in isolated quarantine
  ↓
Verify Publisher / IKP
  ↓
Create immutable submission record
```

Submission Record 至少记录：

```text
submission_id
app_id
publisher_id
release_sequence
version_name
channel
package_sha256
package_length
submitted_at
submitting_account
publisher_key_id
review_state
```

审核过程中不能替换相同 Submission 的 IKP 字节。修改包必须新 Release Sequence。

---

# 8. 审核流水线

## 8.1 Identity and Signature

验证：Publisher Identity、App Ownership、App Signing Key Delegation、Release Signature、Release Sequence、App Transfer Chain（如有）。

## 8.2 Package Structure and Safety

验证：

- IKP 结构；
- 路径逃逸 / Zip Bomb / 重复 Entry；
- 禁止的可执行依赖；
- 不携带另一套 Platform / Lua interpreter / Device Adapter；
- 不携带与 Baga Platform 冲突的随机 native Standard Library runtime；
- Manifest 与 Release Statement 一致；
- Payload Hash。

**由 Platform 提供的 Baga Lua Profile Standard Libraries 不属于 IKP 自带 native dependency。**

## 8.3 API, Standard Libraries and Portability

必须验证：

- **设备 / OS / Platform 能力只通过公开 `baga.*` API 获取；**
- **正式 Baga Lua Profile Standard Libraries 可按上游标准 API 直接使用；**
- `lsqlite3` / SQLite 的直接使用是合法 Universal App 行为；
- 不应要求 App 使用已撤销的 `baga.data`；
- 不使用设备品牌判断作为核心兼容方式；
- Capability / Permission 已注册；
- 不直接调用 Vendor SDK、Shell、Android Context、Kindle private bridge；
- 不依赖设备中“碰巧存在”的随机 native library；
- Universal 声明与真实实现一致。

审核工具 MUST NOT 把“仅使用公开 `baga.*` API”误解为“禁止正式 Standard Libraries”。

## 8.4 Compatibility

执行：

- IKP Validator；
- Baga Lua Profile / Standard Library Tests；
- SQLite / `lsqlite3` Profile Tests；
- Baga Ink Reference Platform Tests；
- Manifest Capability 筛选；
- 必要的 Kindle 与 Android E-Paper Reference Device 测试；
- sleep/wake、offline start、storage、display、input 等场景。

如果 App 实际采用 Automerge 功能，还应按其实际采用模块执行相应 Reference/BICTS 测试；不要求所有 App 使用 Automerge。

## 8.5 Permission Review

检查最小权限、功能与权限说明一致、高风险新增权限、文件/笔记/网络/蓝牙等用途以及 Permission Diff。

App-private SQLite database 本身不需要额外用户资料 Permission，但不能用于绕过 Library/User-files 权限。

## 8.6 Privacy and Network

检查隐私政策、远程服务域名、账号要求、Analytics / Crash Reporting、AI 数据上传、未经说明的数据收集以及嵌入式秘密/私钥。

## 8.7 E-Paper Quality

检查高频刷新、无意义动画、后台唤醒、断网行为、非触摸输入、灰阶、弱设备降级、残影风险。

## 8.8 Malware and Abuse

检查恶意网络、账号窃取、Sandbox escape、SQLite VFS/path escape、供应链风险、欺骗性 UI、隐藏高风险逻辑和 Market Policy 违规。

## 8.9 Human Review

自动化不足以处理复杂隐私、欺骗、品牌冒用和用户伤害问题时进入人工审核。

---

# 9. 审核状态

```text
submitted
validating
under_review
needs_changes
approved
rejected
withdrawn_by_publisher
suspended
security_hold
```

这些是 Market workflow 状态，不是设备端 Release Status。

---

# 10. Review Attestation

审核通过后，Market MAY 生成独立 Review Attestation，至少绑定：

```text
repository_id
app_id
publisher_id
release_sequence
package_sha256
review_policy_version
result
compatibility_labels
reviewed_at
```

Attestation 由 Market Review Key 签署，不能替代 Publisher Signature，也不能证明软件绝对无漏洞。

---

# 11. Market Policy 与协议分离

Market Policy 可单独版本化：内容分类、隐私要求、广告、AI 内容、开源披露、评论评分、收费结算、地区可用性、审核时限、品牌商标规则。

Market Policy 不得改写：

- Publisher Identity；
- App Ownership；
- IKP Signature；
- Release Sequence / Package Digest；
- Permission / Capability；
- Baga Lua Profile / Standard Library 的协议语义；
- Update Identity；
- Repository Metadata Verification。

---

# 12. Permission Diff

Market 必须计算当前 Stable 与候选 Release 的 Permission Diff。

新增敏感 Permission 必须显著展示；删除 Permission 可以自动应用；权限名称必须来自正式 Registry。

---

# 13. Capability 与兼容范围

Release 声明：

```text
required capabilities
optional capabilities
Baga API range
```

Baga Lua Profile / Standard Libraries 的兼容基线由对应 Platform/API Profile 版本确定，并在 Reference Platform / BICTS 中验证；当前不为每个 Standard Library 单独增加 Manifest 字段。

Market 应计算：

```text
Latest overall release
Latest release compatible with this device/platform profile
```

老设备不兼容新版时继续提供 Latest Compatible Release，并说明不兼容原因。

---

# 14. Data Schema 与回滚声明

Release 应声明：

```json
{
  "data_schema_version": 4,
  "rollback": {
    "mode": "safe",
    "minimum_compatible_schema": 3
  }
}
```

模式：

```text
safe
snapshot-required
forward-only
```

- `safe`：旧版仍能读取当前数据；
- `snapshot-required`：激活前备份 App 私有数据；
- `forward-only`：迁移后旧版不可安全读取，必须显著提示并限制自动发布。

对于 SQLite schema migration，审核应确认 migration / rollback policy 与声明一致；对 Automerge 持久格式/协议变化也应明确兼容范围。

---

# 15. 分阶段发布

Market MAY 支持：

```text
1% → 5% → 20% → 50% → 100%
```

Phased Rollout 不能改变 Package Digest、不能让相同 Sequence 指向不同包，可以暂停后续安装；Security Release 仍必须满足签名和兼容验证。

---

# 16. 源代码与构建来源

Catalog SHOULD 支持：

```text
license
source_repository
source_commit
build_provenance
reproducible_build_status
sbom
```

App 声称开源/可重复构建时，Source Commit / Build Attestation 必须对应 Package Digest。

SBOM SHOULD 区分：

```text
IKP bundled dependencies
Platform-provided Standard Libraries
Platform/Adapter implementation dependencies
```

避免把 Platform 提供的 SQLite/lsqlite3 错记成 App 自带依赖。

---

# 17. 元数据更新与包更新分离

Catalog 文案、截图、本地化、分类、支持链接、隐私说明、关键词可在不改变 IKP 的前提下更新。

不得通过 Catalog 更新改变：App ID、Publisher ID、Release Sequence、Package Digest、Permission、Capability、API Range、Data Schema、Publisher Signature。

---

# 18. 撤回与下架

Publisher 可请求 withdraw release / unlist app / stop new installs；Market 可 suspend listing / security hold / reject future submissions。

这些行为必须有明确状态，不得删除历史制造“从未存在”的假象。

---

# 19. 拒绝与申诉

Market Policy 应定义拒绝理由 Code、可修复项、是否需要新 Release Sequence、人工复核、安全快速通道和审计记录。

IKP 字节变化必须新 Release Sequence；仅 Catalog 文案修正可不发布新 IKP。

---

# 20. 第三方 Repository

第三方 Repository 可以采用不同审核政策，但必须：

- 使用真实 Publisher Identity；
- 验证 IKP Signature；
- 保持 Release 不可变；
- 不伪造官方 Review Attestation；
- 清晰显示审核级别；
- 不让同名不同 Publisher 静默覆盖；
- 不篡改 Baga App / API / Standard Library 的协议语义。

---

# 21. 发布闭环

```text
Register App ID
  ↓
Verify App Ownership
  ↓
Build IKP
  ↓
Validate API + Lua Profile / Standard Library usage
  ↓
Sign with delegated App Key
  ↓
Upload immutable package
  ↓
Identity / structure / policy / compatibility review
  ↓
Release Record + Review Attestation
  ↓
Atomic Repository Metadata publication
  ↓
Transparency Event
  ↓
Devices discover/install
```

---

# 22. 最终原则

> **Market 可以决定是否收录，但不能改变软件身份或平台标准。Universal App 的设备能力必须经 `baga.*`，而正式 Baga Lua Profile Standard Libraries 可以直接使用成熟上游 API；两者都必须被正确审核，而不能互相混淆。**