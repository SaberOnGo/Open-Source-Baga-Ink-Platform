# Baga Ink 发布者身份与应用所有权标准 / Baga Ink Publisher Identity and App Ownership Standard

> **文档级别：分发层核心安全标准**  
> **状态：Draft v0.1**  
> **日期：2026-08-22**  
> **上位文档：`20_市场与分发总体架构_Baga-Ink-Market-and-Distribution-Architecture.md`**  
> **配套规范：`22_...IKP-Signing...`、`23_...Repository...`、`27_...Transparency...`**

---

## 0. 目的

本文档定义：

- Publisher Identity；
- Developer Account 与软件签名身份的边界；
- Application ID 的所有权；
- Publisher Root Key；
- App Signing Key Delegation；
- 应用身份连续性；
- App Transfer；
- 密钥轮换、丢失、恢复与泄露处置；
- 设备本地身份钉扎规则。

最核心的安全原则：

> **Market 账号证明“谁可以操作后台”；Publisher 密钥证明“谁授权发布软件”。二者必须分离。**

---

# 1. 身份层级

Baga Ink 定义四个不同概念。

## 1.1 Developer Account

Developer Account 是 Baga Ink Developers / Market 中的登录账号。

它可以使用：

```text
Email
Passkey
OAuth
Organization SSO
Multi-factor authentication
```

Developer Account 用于：

- 团队成员管理；
- 应用资料编辑；
- 上传待发布 IKP；
- 查看审核结果；
- 发起发布、转移和恢复流程；
- 管理 Market Policy 相关内容。

Developer Account 被盗，不能单独生成一个设备可接受的正式 IKP 更新。

## 1.2 Publisher Identity

Publisher Identity 是软件发布者的密码学身份。

它由：

```text
Publisher Genesis Document
Publisher ID
Publisher Root Key Set
Root Signature Threshold
Recovery Key Set
Recovery Signature Threshold
```

组成。

## 1.3 App Ownership

App Ownership 是 Publisher 对某个 `app_id` 的控制关系。

它必须由 Publisher Root Key Threshold 签名，并可以被 Repository / Market 另行确认。

## 1.4 App Signing Key

App Signing Key 用于日常版本发布。

它必须由 Publisher Root Key Set 正式委托给指定：

```text
publisher_id
app_id
channel scope
sequence range
validity window
```

日常发布不应频繁使用 Publisher Root Private Key。

---

# 2. 为什么不把账号当作软件身份

如果 Market 登录账号可以直接替换应用签名身份，那么：

```text
账号密码泄露
        ↓
攻击者登录后台
        ↓
发布恶意更新
```

会形成单点失陷。

正确关系：

```text
Developer Account
       │
       ├── Upload / manage metadata
       └── Request release

Publisher / App Signing Key
       │
       └── Authorize software bytes
```

Market 必须同时验证：

1. 当前账号有权管理该 Publisher / App；
2. IKP 的密码学签名与 App Ownership / Delegation 一致。

---

# 3. Publisher Genesis Document

Publisher Identity 第一次创建时，必须生成 Genesis Document。

概念结构：

```json
{
  "type": "baga.publisher-genesis",
  "format": "0.1",
  "display_name": "Example Studio",
  "root_threshold": 1,
  "root_keys": [
    {
      "key_id": "ed25519:...",
      "algorithm": "ed25519",
      "public_key": "base64url..."
    }
  ],
  "recovery_threshold": 1,
  "recovery_keys": [
    {
      "key_id": "ed25519:...",
      "algorithm": "ed25519",
      "public_key": "base64url..."
    }
  ],
  "created_at": "2026-08-22T00:00:00Z"
}
```

Genesis Document 必须采用规范化 JSON 编码。

Publisher ID 计算为：

```text
publisher_id
=
"pub1_" + base32lower(SHA-256(canonical_genesis_document))
```

Publisher ID 一旦生成不得改变。

后续 Root Key Rotation 不改变 Publisher ID。

---

# 4. Publisher Root Key Set

Publisher Root Key Set 是 Publisher Identity 的最高控制权。

Root Key 主要用于：

- 签署 App Ownership；
- 委托 App Signing Key；
- 撤销 App Signing Key；
- 正常轮换 Publisher Root；
- 批准 App Transfer；
- 修改 Publisher 安全策略。

Root Private Key 应离线或保存在硬件安全设备、系统安全密钥库或专用签名机器中。

## 4.1 个人开发者推荐配置

```text
Root:      1-of-1
Recovery:  1-of-1 separate offline key
App Key:   1-of-1 routine release key
```

Root Key 与 Recovery Key 不应是同一把密钥。

## 4.2 组织推荐配置

```text
Root:      2-of-3
Recovery:  2-of-3
App Key:   1-of-1 or 2-of-2 according to policy
```

设备验证只需要独立验证多份 Ed25519 Signature 并检查 Threshold，不需要复杂联合签名算法。

---

# 5. Publisher Identity Document 的演进

Genesis 后的每次身份更新必须形成新版本 Identity Document。

概念字段：

```json
{
  "type": "baga.publisher-identity",
  "format": "0.1",
  "publisher_id": "pub1_...",
  "sequence": 4,
  "previous_digest": "sha256:...",
  "root_threshold": 2,
  "root_keys": [],
  "recovery_threshold": 2,
  "recovery_keys": [],
  "effective_at": "..."
}
```

规则：

- `sequence` 必须单调递增；
- `previous_digest` 必须指向上一可信文档；
- 正常更新必须满足上一 Root Threshold；
- Root Key 变化时，新 Root Threshold 也必须签署接受；
- 设备必须拒绝低于本地已信任 `sequence` 的身份文档。

正常 Root 轮换采用双向授权：

```text
Old Root Threshold signs new identity document
+
New Root Threshold signs acceptance
```

---

# 6. Application ID

每个 Baga Ink App 必须拥有全局稳定的 `app_id`。

推荐格式：

```text
com.example.reader
org.example.notes
```

要求：

- 只使用小写 ASCII 字母、数字、点和允许的短横线；
- 至少包含两个层级；
- 不因设备、Channel 或架构改变；
- 不因转移 Publisher 而改变；
- 一个正式发布版本只能对应一个 `app_id`。

## 6.1 域名命名空间

如果 `app_id` 使用真实反向域名命名空间，官方 Market 可以要求：

```text
DNS TXT verification
or
HTTPS well-known verification
```

以减少域名冒用。

## 6.2 无域名开发者

Market 可以分配稳定、不可转借的 Publisher Namespace。

分配规则必须：

- 不暗示开发者拥有并未验证的域名；
- 不因账号显示名变化而改变；
- 与 Publisher ID 绑定；
- 在 Publisher Transfer 时保持可追踪。

---

# 7. App Ownership Statement

Publisher 首次取得一个 App ID 时，必须生成 App Ownership Statement。

概念结构：

```json
{
  "type": "baga.app-ownership",
  "format": "0.1",
  "publisher_id": "pub1_...",
  "app_id": "com.example.reader",
  "ownership_sequence": 1,
  "status": "active",
  "created_at": "..."
}
```

该声明必须：

- 由 Publisher Root Threshold 签名；
- 与当前 Publisher Identity Document 对应；
- 在官方 Market 中通过 App ID 冲突检查；
- 写入 Transparency Log；
- 被 Repository Release Record 引用。

App Ownership 不等于 Market 上架许可。

Publisher 可以拥有 App ID，但尚未通过某个 Market 的审核。

---

# 8. App Signing Key Delegation

日常 IKP 使用 App Signing Key 签名。

App Signing Key 必须通过 Delegation 获得权限。

概念结构：

```json
{
  "type": "baga.app-key-delegation",
  "format": "0.1",
  "publisher_id": "pub1_...",
  "app_id": "com.example.reader",
  "delegation_sequence": 7,
  "key_id": "ed25519:...",
  "public_key": "base64url...",
  "signature_threshold": 1,
  "allowed_channels": ["stable", "beta"],
  "min_release_sequence": 100,
  "max_release_sequence": 999,
  "valid_from": "...",
  "valid_until": "...",
  "status": "active"
}
```

Delegation 必须由 Publisher Root Threshold 签名。

App Signing Key 只能签署 Delegation 范围内的：

- 指定 `app_id`；
- 指定 Channel；
- 指定 Release Sequence 范围；
- 指定有效期。

设备不得因为某个 App Signing Key 同属一个 Publisher，就允许它签署其他 App。

---

# 9. 应用身份定义

设备用于判断“是不是同一个应用”的正式身份为：

```text
Installed App Identity
=
app_id
+
publisher_id
+
Publisher Identity Lineage
```

其中 Publisher ID 在正常 Root Key 轮换中保持不变。

App Signing Key 可以更换，只要新 Key 拥有合法 Delegation。

这吸收了成熟平台中“稳定应用标识符 + 签名主体/连续链”的优点。

用户可见名称、图标、Market URL、Repository URL 都不是应用身份。

---

# 10. 设备本地身份钉扎

首次正式安装后，设备必须记录：

```json
{
  "app_id": "com.example.reader",
  "publisher_id": "pub1_...",
  "publisher_identity_sequence": 4,
  "publisher_identity_digest": "sha256:...",
  "app_ownership_sequence": 1,
  "app_signing_key_id": "ed25519:...",
  "source_repository_id": "repo1_...",
  "current_release_sequence": 126,
  "current_package_digest": "sha256:..."
}
```

更新时不得用 Repository 中的同名 App 覆盖该记录，除非：

- Publisher ID 一致并且签名链合法；或
- 存在完整有效 App Transfer Chain；或
- 用户显式执行“清除原应用身份并按新应用安装”，同时处理原用户数据。

---

# 11. App Signing Key Rotation

常规轮换：

1. Publisher Root 签署新的 App Signing Key Delegation；
2. 新 Delegation 的 Sequence 高于旧版本；
3. Repository 发布新的 Delegation；
4. Transparency Log 记录事件；
5. 新 IKP 使用新 App Signing Key；
6. 设备验证 Publisher Root → Delegation → IKP Signature。

旧 Key 可以：

```text
active
retired
revoked
```

`retired`：不再签新版本，但历史签名仍有效。

`revoked`：表示 Key 可能泄露，后续 Release 必须执行额外处置。

---

# 12. Publisher Root Rotation

正常 Publisher Root Rotation 必须：

- 保持 Publisher ID；
- 增加 Identity Sequence；
- 引用上一身份文档 Digest；
- 满足旧 Root Threshold；
- 满足新 Root Threshold；
- 写入 Repository 与 Transparency Log；
- 不允许跳过中间 Sequence。

设备可以逐版本更新 Publisher Identity 文档，类似安全根元数据连续更新。

---

# 13. Recovery Key

Recovery Key 只用于：

- Root Private Key 全部丢失；
- Root Key 被确认泄露；
- 团队失去原安全设备；
- 正常 Root Rotation 已不可完成。

Recovery Key 不用于日常 IKP 发布。

紧急恢复至少要求：

```text
Recovery Threshold Signature
+
Market / Repository Security Recovery Attestation
+
Public Cooling Period
+
Transparency Log Event
```

恢复声明必须包括：

```text
publisher_id
last_trusted_identity_digest
new_root_key_set
new_recovery_key_set
reason
incident_reference
recovery_sequence
not_before
```

官方 Market 不得在没有 Recovery Key 的情况下，仅凭账号客服流程静默替换 Publisher Root。

---

# 14. 无 Recovery Key 的密钥丢失

如果：

```text
Root Keys lost
+
Recovery Keys lost
```

则不能自动证明新的密钥仍属于原 Publisher Identity。

允许路径只有：

1. 作为新 Publisher / 新 App 身份重新发布；或
2. 经过高强度人工争议解决，并要求用户在设备上显式确认信任重置；或
3. 由先前预注册且可验证的组织级外部恢复机制处理。

不得只因：

```text
登录了原邮箱
控制原 GitHub
知道原账号信息
```

就让新密钥无感覆盖所有已安装用户。

---

# 15. App Transfer

App 从 Publisher A 转移到 Publisher B 时，必须存在双向转移链。

## 15.1 Transfer Out

由 A 的 Root Threshold 签署：

```text
app_id
old_publisher_id
new_publisher_id
transfer_sequence
last_release_sequence
transfer_nonce
```

## 15.2 Transfer In

由 B 的 Root Threshold 签署，必须引用相同：

```text
app_id
transfer_nonce
old_publisher_id
new_publisher_id
```

## 15.3 Repository Attestation

Repository 必须确认：

- App ID 当前归属变化；
- 两侧签名有效；
- 没有冲突的并行转移；
- 新 Publisher 的 App Signing Key Delegation 已建立。

## 15.4 设备行为

设备只有在完整 Transfer Chain 有效时，才把 Publisher ID 的变化视为同一 App 的合法继续。

转移不得自动扩大权限。

转移事件必须进入 Transparency Log。

---

# 16. 团队与权限

Market 团队角色可以包括：

```text
Owner
Security Admin
Release Manager
Metadata Editor
Reviewer Liaison
Viewer
```

但这些只是账号层权限。

建议：

- Metadata Editor 无权签 IKP；
- Release Manager 可以上传已签 IKP，但不能修改 Publisher Root；
- Security Admin 可以管理 Root / Recovery 流程，但不自动拥有 Market 付款权限；
- 高风险操作要求 MFA 和双人审批；
- Publisher Root 私钥不上传到 Market 服务器。

---

# 17. 跨 Repository 身份

Publisher Identity 与 IKP Signature 不属于某一个 Repository。

同一个合法 IKP 可以被多个 Repository 分发。

设备判断能否覆盖现有 App 时，主要验证：

```text
App Identity Continuity
+
Repository Source Policy
+
Release Validity
```

Repository 之间不能通过修改 Publisher Metadata 伪造同一发布者。

Publisher Root 文档和 Delegation 必须由 Publisher 自己签署。

---

# 18. Market 的职责与边界

Baga Ink Market 可以：

- 验证 Publisher Identity；
- 验证域名；
- 防止官方 Market App ID 冲突；
- 审核 IKP；
- 签署 Repository Metadata；
- 发布 Review / Recovery / Transfer Attestation；
- 记录 Transparency Event。

Baga Ink Market 不可以：

- 替开发者生成未授权 IKP Signature；
- 在 Publisher 不知情时替换 App Signing Key；
- 仅凭账号登录绕过 Publisher Root；
- 把所有第三方 App 重新变成 Baga 所有；
- 让同名 App ID 覆盖不同 Publisher Identity。

---

# 19. 安全事件分类

## Account Compromise

Market 账号被盗，但 Publisher Key 未泄露。

处理：冻结后台操作、撤销会话、恢复账号；已安装 App 身份不变。

## App Signing Key Compromise

撤销 Delegation，创建新 Delegation，发布安全声明，检查可疑 Release。

## Publisher Root Compromise

执行正常双向轮换或 Recovery 流程；所有新身份文档进入透明日志。

## Repository Key Compromise

按 Repository Root 角色更新；不改变 Publisher Identity。

## Market Policy Dispute

可以下架官方 Market 条目，但不能伪造 Publisher Signature 或静默改变已安装身份。

---

# 20. 版本与兼容

Publisher Identity、App Ownership、Delegation 和 Transfer Statement 都必须分别版本化。

设备至少保存自己已经接受的最高 Sequence，拒绝更低版本。

新增字段：

- Optional 字段可以向后兼容增加；
- 改变安全语义必须提高 Format Major；
- 未识别的 Critical 字段必须拒绝；
- 未识别的普通 Metadata 字段可以保留但不得影响身份判断。

---

# 21. 最终验证原则

一个 IKP 被视为属于某个应用，必须能建立：

```text
Publisher Genesis
      │
      ▼
Current Publisher Identity
      │
      ▼
App Ownership
      │
      ▼
App Signing Key Delegation
      │
      ▼
IKP Release Signature
```

同时满足：

```text
app_id 一致
publisher_id 一致或 Transfer Chain 合法
所有 Sequence 单调不回退
所有 Threshold 满足
签名算法受支持
有效期与撤销状态有效
```

任何 Repository 或账号都不得替代这条身份链。
