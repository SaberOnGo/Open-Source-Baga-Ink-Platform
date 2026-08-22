# Baga Ink 仓库元数据与索引协议 / Baga Ink Repository Metadata and Index Protocol

> **文档级别：分发层 Wire Protocol / Repository Security Protocol**  
> **状态：Draft v0.1**  
> **日期：2026-08-22**  
> **上位文档：`20_市场与分发总体架构_Baga-Ink-Market-and-Distribution-Architecture.md`**  
> **配套规范：`21_...Publisher-Identity...`、`22_...IKP-Signing...`、`25_...Update...`、`26_...Offline-Transfer...`**

---

## 0. 目的

本文档定义 Baga Ink Repository 的信任根、签名元数据角色、目录布局、目标文件描述、版本与过期规则、内容寻址、客户端验证顺序、第三方仓库、Mirror、离线快照以及低带宽索引机制。

Baga Ink 不自行发明仓库更新密码学。

v0.1 采用：

> **受约束的 TUF 1.0.x Repository Profile。**

凡本规范未明确修改的安全语义，应遵循 TUF 的 Root / Targets / Snapshot / Timestamp 角色与客户端更新顺序。

只有通过对应 TUF Conformance 与 Baga Ink Repository Tests 的实现，才能声称完整兼容本协议。

---

# 1. 协议目标

Repository Protocol 必须保护：

```text
Repository identity
Current repository state
Package digest and length
Release record
Publisher identity references
Channel and release status
Catalog and asset integrity
Metadata consistency
Rollback prevention
Freeze detection
Mirror / CDN substitution
Offline transfer integrity
```

它不替代 IKP Publisher Signature。

正确关系：

```text
Repository Metadata
  proves what repository currently distributes

Publisher Signature
  proves who authorized the IKP
```

设备必须同时验证。

---

# 2. Repository Identity

每个仓库必须拥有独立的 `repository_id`。

推荐计算：

```text
repository_id
=
"repo1_" + base32lower(SHA-256(canonical_root_v1_signed_body))
```

Root v1 一旦发布，Repository ID 不改变。

Repository URL、域名、Mirror、CDN 可以变化，但不得改变 Repository Identity。

设备添加 Repository 时必须保存：

```text
repository_id
trusted_root_version
trusted_root_digest
root key set
highest trusted role versions
last trusted time floor
```

---

# 3. 顶层角色

v0.1 必须实现四个 TUF 顶层角色：

```text
Root
Targets
Snapshot
Timestamp
```

## 3.1 Root

Root 定义：

- Repository ID；
- Root / Targets / Snapshot / Timestamp Public Keys；
- 各角色 Signature Threshold；
- Metadata Format / Spec Version；
- `consistent_snapshot`；
- Root Version 与 Expiration。

Root Private Keys 必须离线或等效保护。

官方 Baga Ink Market 推荐：

```text
Root Threshold: 2-of-3
```

独立小型 Repository 可以使用 1-of-1，但必须明确其较低的妥协韧性。

## 3.2 Targets

Targets 列出允许下载的目标文件：

```text
IKP packages
Release records
Publisher identity documents
App ownership and delegation documents
Catalog indexes / diffs
Catalog app records
Asset descriptors
Withdrawal / revocation records
Review attestations
Transparency checkpoints
```

每个 Target 必须记录：

```text
path
length
sha256
optional custom metadata
```

## 3.3 Snapshot

Snapshot 固定当前仓库中所有 Targets Metadata 的一致视图。

它必须记录：

```text
metadata path
metadata version
metadata length
metadata sha256
```

Snapshot 防止攻击者混合新旧 Targets Metadata。

## 3.4 Timestamp

Timestamp 是最小、最频繁更新的元数据。

它至少指向当前 Snapshot：

```text
snapshot version
snapshot length
snapshot sha256
expiration
generated_at
```

客户端每次在线检查更新时，首先验证 Timestamp。

---

# 4. Root Metadata Profile

概念结构：

```json
{
  "signatures": [],
  "signed": {
    "_type": "root",
    "spec_version": "1.0.x",
    "baga_repository_profile": "0.1",
    "repository_id": "repo1_...",
    "version": 3,
    "expires": "2028-01-01T00:00:00Z",
    "consistent_snapshot": true,
    "keys": {},
    "roles": {
      "root": {"keyids": [], "threshold": 2},
      "targets": {"keyids": [], "threshold": 1},
      "snapshot": {"keyids": [], "threshold": 1},
      "timestamp": {"keyids": [], "threshold": 1}
    }
  }
}
```

要求：

- `consistent_snapshot` 必须为 `true`；
- Root Version 从 1 开始单调递增；
- 所有历史 Root 版本必须继续可获取；
- Root 更新必须逐版本验证；
- 新 Root 必须同时满足旧 Root 与新 Root Threshold；
- Repository ID 必须与 Root v1 推导值一致。

---

# 5. Consistent Snapshot

Baga Ink Repository 必须使用一致快照。

Metadata 文件：

```text
<version>.snapshot.json
<version>.targets.json
<version>.<delegated-role>.json
```

不可变目标文件必须使用内容摘要路径，例如：

```text
packages/sha256/ab/abcdef...1234.ikp
releases/sha256/12/123456...abcd.json
catalog/sha256/34/345678...abcd.json
assets/sha256/56/567890...abcd.png
```

Repository 更新新状态时，不修改旧的不可变文件。

这防止客户端在仓库发布过程中读到“半新半旧”状态。

---

# 6. 推荐目录布局

```text
repository/
├── metadata/
│   ├── root.json
│   ├── 1.root.json
│   ├── 2.root.json
│   ├── timestamp.json
│   ├── <version>.snapshot.json
│   ├── <version>.targets.json
│   └── delegated/
│       └── <version>.<role>.json
│
└── targets/
    ├── packages/sha256/
    ├── releases/sha256/
    ├── publishers/sha256/
    ├── catalog/sha256/
    ├── assets/sha256/
    ├── revocations/sha256/
    └── attestations/sha256/
```

`root.json` 可以作为最新 Root 的便利入口，但客户端 Root 更新必须按 `N.root.json` 顺序验证。

---

# 7. Release Record Target

每个正式 IKP Release 必须有一个不可变 Release Record。

概念结构：

```json
{
  "type": "baga.release",
  "format": "0.1",
  "app_id": "com.example.reader",
  "publisher_id": "pub1_...",
  "version_name": "1.4.2",
  "release_sequence": 142,
  "channel": "stable",
  "published_at": "...",
  "package": {
    "path": "packages/sha256/ab/abcdef...1234.ikp",
    "length": 2837461,
    "sha256": "abcdef...1234"
  },
  "publisher_identity_digest": "sha256:...",
  "app_ownership_digest": "sha256:...",
  "app_key_delegation_digest": "sha256:...",
  "baga_api": {
    "min": "0.1",
    "max_exclusive": "1.0"
  },
  "capabilities": {
    "required": [],
    "optional": []
  },
  "permissions": [],
  "data_schema_version": 1,
  "update_policy": {},
  "status": "active"
}
```

Release Record 本身作为 Target 受 Repository Metadata 保护。

Release Record 不替代 IKP 内的 Publisher Release Signature；二者必须交叉一致。

---

# 8. Targets Custom Metadata

Targets Entry 可以使用轻量 Custom Metadata 快速筛选：

```json
{
  "length": 2837461,
  "hashes": {"sha256": "..."},
  "custom": {
    "kind": "ikp-package",
    "app_id": "com.example.reader",
    "publisher_id": "pub1_...",
    "release_sequence": 142,
    "channel": "stable",
    "release_record": "releases/sha256/...json"
  }
}
```

客户端不得只依赖 Custom Metadata 跳过 Release Record 或 Publisher Signature 验证。

Custom Metadata 是索引优化，不是额外信任根。

---

# 9. Delegated Targets

v0.1 客户端必须支持：

```text
Top-level Targets
+
optional one-level Delegated Targets
```

官方 Market 可以按 App ID Hash 前缀分片：

```text
apps-00
apps-01
...
apps-ff
```

也可以按内容类型分片：

```text
packages
catalog
revocations
attestations
```

规则：

- Delegation Path / Hash Prefix 必须无重叠歧义；
- Terminating Delegation 的行为必须明确；
- Delegation Key 不能扩大超过上级授权范围；
- v0.1 最大 Delegation Depth 为 1；
- 更深 Delegation 需要后续 Profile 版本。

Publisher Signature 已经承担 App 发布者身份，因此 v0.1 不要求把每个 Publisher Key 直接变成 TUF Delegated Role。

---

# 10. Metadata Version 与回滚保护

客户端必须为每个 Repository 保存最高已信任版本：

```text
root_version
snapshot_version
targets_version
delegated_role_versions
timestamp_version
```

客户端必须拒绝：

- 低于本地版本的 Metadata；
- 相同 Version 但不同 Digest 的 Metadata；
- Timestamp 指向更旧 Snapshot；
- Snapshot 指向更旧 Targets；
- Release Sequence 低于已安装版本的自动更新；
- 同一 Release Sequence 指向不同 Digest。

显式 Downgrade 由 `25` 号规范单独处理，不能通过接受旧 Metadata 实现。

---

# 11. Expiration 与冻结检测

所有顶层 Metadata 必须包含 Expiration。

推荐关系：

```text
Timestamp expiration  shortest
Snapshot expiration   longer
Targets expiration    longer
Root expiration       longest
```

具体周期由 Repository Policy 定义，不在 v0.1 锁死固定天数。

过期行为：

- 过期 Metadata 不得用于发现或安装新 Release；
- 过期不影响已经安装 App 的正常启动；
- 设备应提示“仓库状态需要刷新”；
- 离线设备仍可使用现有应用；
- 不得因为 Metadata 过期远程禁用全部应用。

---

# 12. Trusted Time Floor

Kindle 与长期离线设备的系统时间可能不可靠。

Baga Ink 必须保存：

```text
last_trusted_time_floor
```

Timestamp Metadata 必须额外包含被 Timestamp Key 签名的：

```text
generated_at
```

客户端成功验证 Timestamp 后：

```text
last_trusted_time_floor
=
max(previous_floor, verified_generated_at)
```

Expiration 判断使用：

```text
Effective Time
=
max(last_trusted_time_floor, reliable_local_clock)
```

如果没有可靠 Local Clock，客户端仍能阻止时间回退，但不能无限证明 Metadata 尚未过期。

此时：

- 已安装 App 继续工作；
- 新安装 / 更新暂停；
- 获得新的签名 Timestamp 或离线仓库快照后恢复；
- 用户手动修改时钟不能降低 Time Floor。

Baga Ink Client 的普通系统时间不是信任根；它必须传递 Repository 签名的时间信息。

---

# 13. Metadata Client Verification Order

客户端更新仓库状态必须按以下顺序：

```text
1. Load locally trusted Root
2. Fetch sequential newer Root versions
3. Verify each Root with old and new thresholds
4. Fetch Timestamp
5. Verify Timestamp signature, version, expiration and Snapshot descriptor
6. Fetch versioned Snapshot
7. Verify Snapshot length, hash, version, expiration and signature
8. Fetch required versioned Targets / Delegated Targets
9. Verify Targets against Snapshot
10. Resolve target path
11. Fetch target only up to declared length limits
12. Verify target length and SHA-256
13. Persist new trusted metadata atomically
```

任何步骤失败：

- 不得替换本地已信任状态；
- 不得执行目标文件；
- 必须允许未来重新尝试；
- 不能让 Repository 状态进入不可恢复半更新。

---

# 14. Target Download

客户端请求 Target 时必须：

- 使用 Metadata 中声明的 Path；
- 设置最大下载长度；
- 流式计算 SHA-256；
- 下载完成后比较 Length 与 Digest；
- 不相信服务器返回的 `Content-Type` 作为安全依据；
- 不相信重定向后的域名作为身份依据；
- 不把 HTTP ETag 当作 Digest；
- 验证完成前只写入 staging。

HTTPS 必须作为默认传输，以保护隐私、认证服务器与降低流量劫持；但安全完整性仍依赖签名 Metadata 与 Digest。

---

# 15. Mirrors 与 CDN

Mirror / CDN 可以托管：

```text
Metadata copies
IKP blobs
Release records
Catalog files
Assets
```

Mirror 不持有 Root Private Key，也不能决定当前可信版本。

只要：

- Root Trust 一致；
- Metadata Signature 有效；
- Target Digest / Length 有效；

Mirror 可以被替换、增加或按地区选择。

客户端跨 Host Redirect 时不得转发认证凭据，除非显式配置。

---

# 16. 第三方 Repository

第三方 Repository 必须遵循相同协议。

添加流程：

```text
Repository URL
      │
      ▼
Fetch Root v1 / out-of-band Root
      │
      ▼
Display repository_id + Root Fingerprint
      │
      ▼
User confirms trust
      │
      ▼
Persist Root Trust
```

禁止仅凭 URL 自动替换 Root。

第三方 Repository 的 App 不得覆盖同 App ID、不同 Publisher ID 的已安装应用。

官方 Market 的审核标识不得被第三方 Repository 自声明。

---

# 17. Repository Source Pinning

首次安装后，设备保存 `source_repository_id`。

默认自动更新只接受：

- 相同 Repository ID；或
- 同一 Root Trust 下的 Mirror；或
- 用户已经批准的 Source Migration。

Source Migration 必须重新验证：

```text
Publisher Identity
App Transfer Chain（如有）
Release Sequence
Permission Diff
Repository Root Trust
```

Repository URL 变化但 Repository ID 相同，不视为 Source Migration。

---

# 18. Catalog Index 与 Diff

Catalog 产品索引不是 TUF 顶层 Metadata。

它必须作为普通 Target 被 Targets Metadata 保护。

低带宽设备可以使用：

```text
catalog-entry.json
catalog-index.json
catalog-diff-from-<sequence>.json
```

每个 Catalog 文件必须有：

```text
length
sha256
catalog_sequence
base_sequence（Diff 时）
```

客户端只有在：

- Diff Base Sequence 与本地一致；
- Diff Target Digest 有效；
- 应用后得到预期新 Catalog Digest；

时才接受 Diff。

失败则下载完整 Catalog。

---

# 19. Revocation 与 Withdrawal Targets

撤回与撤销记录必须是不可变 Target，并由当前 Repository Metadata 引用。

概念记录：

```json
{
  "type": "baga.release-status",
  "format": "0.1",
  "app_id": "...",
  "release_sequence": 142,
  "package_sha256": "...",
  "status": "security-revoked",
  "severity": "critical",
  "reason_code": "publisher-key-compromise",
  "effective_at": "...",
  "replacement_release_sequence": 143
}
```

具体设备行为由 `25` 号规范定义。

Repository 不能通过删除旧 Target 文件隐藏历史事件；历史 Release 可从 Archive Repository 保留，当前 Targets 则决定是否允许新安装。

---

# 20. Offline Repository Snapshot

离线传输必须携带一个自洽的 Repository Snapshot：

```text
Trusted Root chain
Timestamp
Snapshot
Targets / Delegated Targets
Required immutable Targets
```

设备执行与在线模式相同的签名、版本、过期、Digest 与 Publisher 验证。

离线 Snapshot 不能通过修改传输清单绕过 Repository Metadata。

更详细的传输结构由 `26` 号规范定义。

---

# 21. Atomic Metadata Persistence

本地 Metadata 更新必须：

1. 下载到临时目录；
2. 完成全部签名、Hash、Version 与 Expiration 验证；
3. Fsync / 等效持久化；
4. 原子切换 Trusted Metadata Pointer；
5. 保留上一可信状态直到新状态写入成功。

断电或进程退出后，客户端必须恢复到：

```text
Old complete state
or
New complete state
```

不得留下混合状态。

---

# 22. Resource Limits

为防御恶意仓库，客户端必须限制：

```text
Root metadata max size
Timestamp max size
Snapshot max size
Targets max size
Delegation count
Delegation depth
Target path length
JSON nesting depth
Signature count
Target download length
Catalog diff size
Redirect count
```

具体上限可以由 Platform Compatibility Profile 调整，但必须存在安全默认值。

低内存设备应支持流式 JSON / CBOR 解析或分片 Targets，而不是一次加载完整超大 Catalog。

---

# 23. Repository Key Rotation

Timestamp / Snapshot / Targets Key 可以由新 Root Metadata 轮换。

如果这些在线角色密钥被攻破：

1. 生成新 Root 版本；
2. 由 Root Threshold 签署；
3. 替换受影响角色 Key；
4. 增加 Metadata Versions；
5. 客户端更新 Root 后删除可能被攻击者快进的旧 Timestamp / Snapshot 缓存；
6. 重新获取完整可信链。

如果 Root Threshold 被攻破，需要 Out-of-Band Recovery，不在普通网络更新流程中自动解决。

---

# 24. Baga Ink TUF Profile 的边界

v0.1 固定：

```text
TUF 1.0.x role semantics
Four required top-level roles
Consistent snapshots required
SHA-256 target hashes required
Canonical JSON metadata
One-level target delegations supported
Baga generated_at time-floor extension required
```

v0.1 不定义：

- 多层无限 Delegation；
- 自定义密码学算法；
- Repository 端个性化 Targets；
- 每个设备独立 Director Repository；
- 软件许可或付款收据；
- 远程设备控制指令。

---

# 25. 最终原则

> **Repository URL 可以变化，服务器可以失效，Mirror 可以被替换，但 Repository Identity、Metadata Version、Target Digest 与 Publisher Identity 不能被静默改写。**

客户端只接受能够从本地 Trusted Root 完整验证到目标 IKP 的仓库状态。
