# Baga Ink 透明日志与安全审计标准 / Baga Ink Transparency and Security Audit Standard

> **文档级别：分发层透明性与审计标准**  
> **状态：Draft v0.1**  
> **日期：2026-08-22**  
> **上位文档：`20_市场与分发总体架构_Baga-Ink-Market-and-Distribution-Architecture.md`**  
> **身份规范：`21_发布者身份与应用所有权标准_Baga-Ink-Publisher-Identity-and-App-Ownership-Standard.md`**  
> **仓库协议：`23_仓库元数据与索引协议_Baga-Ink-Repository-Metadata-and-Index-Protocol.md`**

---

## 0. 目的

本文档定义 Baga Ink 生态中 Publisher、App ID、密钥、Release、审核、转移、恢复、撤回和安全撤销事件的公开透明记录与独立审计机制。

该机制借鉴追加式 Merkle Transparency Log 的成熟思想。

核心原则：

> **重要身份和安全事件不能只存在于某个 Market 私有数据库中；它们必须留下可验证、不可静默改写的公共历史。**

透明日志是审计证据，不是设备安装时唯一的信任根。

---

# 1. 目标

透明与审计层必须提供：

```text
Append-only event history
Event inclusion proof
Tree consistency proof
Signed tree checkpoints
Independent monitoring
Publisher and app history lookup
Key compromise investigation
Repository publication audit
Review attestation audit
Privacy-preserving public records
```

它应帮助发现：

- Market 私自替换 Publisher Identity；
- App ID 发生未授权转移；
- App Key Delegation 被异常创建；
- Publisher Root 恢复流程被滥用；
- 同一 Release Sequence 出现不同 Digest；
- 已发布版本或撤销记录被从历史中删除；
- Repository 对不同观察者展示冲突历史。

---

# 2. 非目标

透明日志 v0.1 不用于：

- 记录用户安装了哪些 App；
- 记录用户账号；
- 记录设备序列号；
- 记录阅读历史、笔记或书库；
- 代替 Repository Root；
- 代替 Publisher Signature；
- 代替 Security Revocation；
- 强迫每台 Kindle 每次安装都联网查询日志；
- 作为远程删除用户应用的控制通道。

---

# 3. 必须记录的事件

官方 Baga Ink Market Transparency Log 必须记录：

```text
publisher_genesis
publisher_identity_update
publisher_root_rotation
publisher_recovery_started
publisher_recovery_completed
publisher_recovery_cancelled
app_id_registered
app_ownership_created
app_key_delegated
app_key_retired
app_key_revoked
app_transfer_started
app_transfer_completed
release_published
release_withdrawn
release_unlisted
security_revocation_published
review_attestation_published
repository_root_rotated
```

Market Policy 可以增加其他事件，但不能省略上述安全事件。

---

# 4. Event Envelope

所有事件使用统一 Envelope。

概念结构：

```json
{
  "type": "baga.transparency-event",
  "format": "0.1",
  "event_type": "release_published",
  "event_id": "evt1_...",
  "subject": {
    "publisher_id": "pub1_...",
    "app_id": "com.example.reader",
    "release_sequence": 142
  },
  "statement": {
    "path": "releases/sha256/...json",
    "length": 1842,
    "sha256": "..."
  },
  "repository_id": "repo1_...",
  "observed_at": "2026-08-22T00:00:00Z",
  "critical": true
}
```

Event ID 计算：

```text
event_id
=
"evt1_" + base32lower(SHA-256(CanonicalJSON(event_body_without_event_id)))
```

事件只引用已签名 Statement Digest，不复制所有敏感或冗长数据。

---

# 5. Merkle Log

日志是按 Leaf Index 排序的追加式 Merkle Tree。

每个 Leaf 包含：

```text
Canonical event bytes
or
event digest + immutable event target
```

实现必须提供：

- Tree Size；
- Root Hash；
- Signed Tree Head / Checkpoint；
- Inclusion Proof；
- Consistency Proof；
- Leaf Index 查询；
- Event ID 查询；
- Subject 查询索引。

Baga Ink 不在 v0.1 自行设计 Merkle Hash 细节。

实现应采用成熟、公开评审的 Merkle Transparency Log 算法和库，例如与 Rekor / Trillian 类模型等价的实现。

---

# 6. Signed Checkpoint

Log Operator 必须定期发布签名 Checkpoint。

概念结构：

```json
{
  "type": "baga.transparency-checkpoint",
  "format": "0.1",
  "log_id": "log1_...",
  "tree_size": 128394,
  "root_hash": "base64url...",
  "timestamp": "...",
  "previous_checkpoint_digest": "sha256:...",
  "signing_key_id": "ed25519:..."
}
```

Checkpoint 必须：

- 由 Log Signing Key 签名；
- 作为 Repository Target 发布；
- 可以被独立 Monitor 保存；
- 支持从旧 Tree Size 到新 Tree Size 的 Consistency Proof；
- 不因服务器数据库迁移而重置 Log ID。

---

# 7. Log Identity

每个 Log 必须有稳定 `log_id`。

推荐：

```text
log_id
=
"log1_" + base32lower(SHA-256(log_genesis_document))
```

Log Genesis Document 定义：

```text
Log public key
Log operator
Hash algorithm
Tree algorithm profile
API version
Creation time
```

Log URL 可以变化，但 Log ID 不变。

Log Key Rotation 必须形成签名连续链并记录在 Repository Metadata 与 Transparency Log 自身的外部审计记录中。

---

# 8. Publisher 事件

## 8.1 Publisher Genesis

记录 Publisher Genesis Document Digest 与 Publisher ID。

## 8.2 Identity Update

记录：

```text
publisher_id
identity_sequence
previous_digest
new_identity_digest
```

## 8.3 Root Rotation

记录新旧 Root Key Set 摘要、Identity Sequence 与生效时间。

## 8.4 Recovery

Recovery 必须记录至少三个阶段：

```text
started
completed
cancelled（如适用）
```

`started` 事件在 Cooling Period 开始时发布。

`completed` 只有在 Recovery Threshold、Market Security Attestation 和 `not_before` 均满足后发布。

这使独立 Monitor 有时间发现异常恢复。

---

# 9. App Ownership 与 Transfer

App ID 注册必须记录：

```text
app_id
publisher_id
ownership_statement_digest
```

App Transfer 必须记录：

```text
old_publisher_id
new_publisher_id
transfer_nonce
transfer_out_digest
transfer_in_digest
repository_attestation_digest
```

Transfer Started 后在 Completed 前，Market 可以冻结高风险发布。

同一个 `app_id + transfer_sequence` 出现不同目标 Publisher 时，Monitor 必须报告冲突。

---

# 10. App Key 事件

App Signing Key Delegation 记录：

```text
app_id
publisher_id
key_id
delegation_sequence
allowed_channels
release_sequence_range
validity window
delegation_digest
```

Retired 与 Revoked 是不同事件。

- `retired`：不再授权新 Release，历史签名仍正常；
- `revoked`：Key 可能失陷，需要审计它签过的全部 Release。

Key Revoked 事件必须引用替代 Delegation 或事件处置说明。

---

# 11. Release 事件

每个正式 Release 必须记录：

```text
app_id
publisher_id
release_sequence
version_name
channel
package_sha256
package_length
release_record_digest
publisher_signature_key_id
published_at
```

日志必须检测：

```text
same app_id
+
same release_sequence
+
different package_sha256
```

这种情况是不可接受的 Equivocation，应立即发布安全告警。

---

# 12. Review 事件

Review Attestation 发布时记录：

```text
repository_id
app_id
release_sequence
package_sha256
review_policy_version
result
attestation_digest
```

Review 结果更新不能覆盖旧事件；必须追加新 Attestation，并引用被取代的 Attestation Digest。

这样可以审计：

> 某个版本最初按哪一版政策通过，后来为何被暂停或撤销。

---

# 13. Withdrawal 与 Revocation 事件

Withdrawn、Unlisted、Security Revoked 必须分别记录。

Security Revocation Event 至少包含：

```text
app_id
release_sequence
package_sha256
severity
reason_code
revocation_record_digest
effective_at
replacement_release（如有）
```

后续撤销修正必须追加新事件，不能删除原事件。

如果误报，可以发布：

```text
security_revocation_corrected
```

并明确引用原事件。

---

# 14. Inclusion Proof

任何 Event 查询应能返回：

```text
event
leaf_index
checkpoint
inclusion_proof
```

验证者必须能独立确认：

- Event Digest；
- Leaf 位于该 Tree Size；
- Checkpoint Signature；
- Root Hash 匹配。

Publisher Portal 应允许开发者下载其发布事件的 Inclusion Proof。

---

# 15. Consistency Proof

从 Checkpoint A 到 Checkpoint B：

```text
A.tree_size < B.tree_size
```

日志必须提供 Consistency Proof，证明 B 是 A 的追加扩展，而不是重写历史。

Monitor 必须拒绝：

- Tree Size 增加但无有效 Consistency Proof；
- 相同 Tree Size 不同 Root Hash；
- Checkpoint 时间回退；
- Log ID 突然变化而无迁移声明。

---

# 16. Gossip 与独立 Monitor

Baga Ink SHOULD 支持多种 Checkpoint 传播：

```text
Repository Target
Baga Ink Developers
Public transparency endpoint
GitHub / public archive mirror
Independent monitors
Security mailing list or feed
```

独立 Monitor 的职责：

- 保存历史 Checkpoint；
- 验证 Consistency；
- 发现同 Tree Size 不同 Root；
- 检测 App ID 冲突；
- 检测同 Sequence 不同 Digest；
- 检测异常 Recovery / Transfer；
- 发布可验证告警证据。

官方 Baga Ink 团队不应成为唯一 Monitor。

---

# 17. Split View 检测

如果 Log 对不同观察者提供不同历史：

```text
Checkpoint A: size 1000, root X
Checkpoint B: size 1000, root Y
```

任何一方只需公开两份有效签名 Checkpoint，即可证明 Log Operator Equivocation。

Repository、Developer Portal 与 Monitor 应交换 Checkpoint，降低 Split View 风险。

设备 v0.1 不要求执行实时 Gossip，但 Baga Ink Client 可以缓存并上传用户明确同意分享的 Checkpoint，不包含用户安装清单。

---

# 18. 隐私

公开事件必须只包含软件供应链所需信息。

禁止写入：

- Developer 私人地址；
- 用户邮箱；
- 用户安装记录；
- Device ID；
- 用户书籍、笔记或阅读数据；
- Private Key；
- 未公开安全漏洞的完整利用细节；
- Market 内部未脱敏审核对话。

可以记录：

- Publisher ID；
- 公钥；
- App ID；
- Digest；
- Release Sequence；
- 标准 Reason Code；
- 公开 Security Advisory Reference。

---

# 19. 数据保留

透明日志事件必须长期保留。

如果主服务停止：

- 最终 Checkpoint 应公开；
- Log 数据应导出到可验证 Archive；
- 现有 Inclusion / Consistency Proof 继续可验证；
- Repository Root 可以指定新的 Log，但必须保留旧 Log ID 和 Checkpoint History；
- 不得通过重建空日志抹掉历史。

---

# 20. 可用性失败

Transparency Log 暂时不可用时：

- 已安装 App 继续运行；
- Repository Metadata 与 Publisher Signature 验证仍可以进行；
- 非关键普通 Release 可以按 Repository Policy 延迟发布，等待 Log 恢复；
- Publisher Recovery、App Transfer、Root Rotation、Security Revocation 等高风险事件在没有日志接收确认时不应完成正式发布；
- Market 必须显示透明服务故障状态。

透明日志不能因短暂不可用成为所有设备的单点停机源。

---

# 21. Log API 最小集合

v0.1 至少提供：

```text
POST /events
GET  /events/{event_id}
GET  /entries/{leaf_index}
GET  /checkpoint
GET  /proof/inclusion?leaf_index=&tree_size=
GET  /proof/consistency?from=&to=
GET  /search?publisher_id=
GET  /search?app_id=
```

实际 URL 可以不同，但协议语义必须稳定。

提交 Event 时，Log 必须验证基础 Schema，但不必取代 Market 对 Statement Signature 的业务验证。

---

# 22. Log Operator Security

Log Operator 应：

- 将 Signing Key 与普通 Web 服务隔离；
- 定期备份 Tree 数据；
- 使用不可变或追加式存储；
- 发布 Checkpoint 到多个独立位置；
- 监控未授权 Key 使用；
- 对高风险事件启用速率限制和人工确认；
- 记录管理员操作审计；
- 不允许数据库管理员静默改写历史后重新计算 Tree 而不暴露变化。

---

# 23. Security Audit Bundle

Market 应能为单个 Release 导出 Audit Bundle：

```text
Publisher Genesis / Identity Chain
App Ownership
App Key Delegation
IKP Release Statement
Repository Release Record
Repository Metadata descriptors
Review Attestation
Transparency Event
Inclusion Proof
Relevant Checkpoint
Withdrawal / Revocation（如有）
```

该 Bundle 允许第三方在不访问 Market 私有数据库的情况下审计 Release。

---

# 24. 设备与 Client 的使用边界

设备安装时不强制查询 Log。

Baga Ink Client 可以：

- 显示 Publisher / App 历史；
- 验证 Release Inclusion Proof；
- 提示异常 Recovery / Transfer；
- 缓存 Checkpoint；
- 导出 Audit Bundle。

但设备最终安装身份仍由：

```text
Publisher Signature
Repository Metadata
Local Installed Identity
```

决定。

Transparency 只增加可发现性和问责，不替代三层信任。

---

# 25. 最终原则

> **签名让伪造变困难；透明日志让隐蔽地滥用合法签名和管理权也变困难。**
