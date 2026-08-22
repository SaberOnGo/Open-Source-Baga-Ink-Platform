# Baga Ink IKP 签名与密钥生命周期标准 / Baga Ink IKP Signing and Key Lifecycle Standard

> **文档级别：分发层核心密码学标准**  
> **状态：Draft v0.1**  
> **日期：2026-08-22**  
> **上位文档：`20_市场与分发总体架构_Baga-Ink-Market-and-Distribution-Architecture.md`**  
> **身份规范：`21_发布者身份与应用所有权标准_Baga-Ink-Publisher-Identity-and-App-Ownership-Standard.md`**  
> **包结构规范：`06_IKP应用包规范_IKP-Package-Specification.md`**

---

## 0. 目的

本文档定义 IKP 的发布者签名格式、验证算法、文件完整性清单、App Signing Key Delegation、Publisher Root 轮换、紧急恢复以及设备验证顺序。

该标准只采用成熟密码学原语，不自行设计新的加密算法。

核心目标：

> **IKP 无论从官方 Market、第三方 Repository、USB、局域网或本地文件获得，都可以独立证明其应用身份和内容完整性。**

---

# 1. v0.1 密码学基线

Baga Ink v0.1 必须支持：

```text
Content digest: SHA-256
Digital signature: Ed25519
Text encoding: UTF-8
Binary-to-text encoding: unpadded base64url
Signed structured data: Baga Canonical JSON Profile
```

实现必须拒绝：

- 未声明的签名算法；
- 算法名称大小写或别名混淆；
- 未知 Critical 字段；
- 重复 JSON Object Key；
- 非法 UTF-8；
- NaN / Infinity；
- 不符合规范化规则的签名输入。

未来新增算法必须通过新 Format 版本和明确迁移规范，不得静默替换。

---

# 2. Key ID

Ed25519 Key ID 定义为：

```text
key_id
=
"ed25519:" + base64url(SHA-256(raw_32_byte_public_key))
```

规则：

- Public Key 必须是 32-byte Ed25519 Raw Public Key；
- Key ID 只用于标识与索引，不能替代签名验证；
- 解析器必须重新计算 Key ID 并与声明值比较；
- 同一个 Public Key 永远生成同一个 Key ID。

---

# 3. Baga Canonical JSON Profile

所有被签名的 JSON Body 必须有唯一字节表示。

v0.1 规则：

- UTF-8；
- Object Key 按 Unicode Code Point 升序；
- 不输出无意义空白；
- 不允许重复 Key；
- String 使用标准 JSON Escape；
- Object 与 Array 顺序按语义保留；
- Integer 使用十进制最短形式；
- v0.1 安全声明不得使用 Floating Point；
- 文档末尾不加入额外换行；
- 签名输入为 Canonical JSON 的原始 UTF-8 Bytes。

SDK 必须提供唯一官方 Serializer / Validator，避免不同语言实现产生不同签名字节。

---

# 4. IKP 签名目录

正式签名 IKP 建议包含：

```text
signature/
├── files.json
├── publisher-identity.json
├── app-ownership.json
├── app-key-delegation.json
├── release-statement.json
└── signatures.json
```

其中：

- `files.json`：应用 Payload 文件 Hash 清单；
- `publisher-identity.json`：当前 Publisher Identity 文档或必要链；
- `app-ownership.json`：App ID 所有权声明；
- `app-key-delegation.json`：App Signing Key 授权；
- `release-statement.json`：本次 IKP Release 的规范签名 Body；
- `signatures.json`：对 Release Statement 的签名集合。

身份链文件可以采用完整链或最小证明链；设备必须能连接到已信任或首次安装时确认的 Publisher Genesis。

---

# 5. `files.json`

`files.json` 必须列出所有应用 Payload 文件。

Payload 文件定义为：

> IKP 中除 `signature/` 目录之外的全部文件。

概念结构：

```json
{
  "type": "baga.ikp-files",
  "format": "0.1",
  "hash_algorithm": "sha256",
  "files": [
    {
      "path": "manifest.json",
      "length": 642,
      "sha256": "..."
    },
    {
      "path": "main.lua",
      "length": 1830,
      "sha256": "..."
    }
  ]
}
```

规则：

- 路径必须规范化；
- 使用 `/` 分隔；
- 不允许绝对路径、`..` 或符号链接逃逸；
- 每个 Payload 文件恰好出现一次；
- 不允许额外未声明 Payload；
- 文件按 UTF-8 Path Bytes 升序排列；
- Hash 对解压后的原始文件 Bytes 计算；
- `length` 必须与实际长度一致。

`files.json` 自身不列入其 `files` 数组。

---

# 6. `release-statement.json`

Release Statement 是 App Signing Key 真正签署的 Body。

概念结构：

```json
{
  "type": "baga.ikp-release",
  "format": "0.1",
  "app_id": "com.example.reader",
  "publisher_id": "pub1_...",
  "version_name": "1.4.2",
  "release_sequence": 142,
  "channel": "stable",
  "ikp_format": "0.2",
  "baga_api": {
    "min": "0.1",
    "max_exclusive": "1.0"
  },
  "manifest": {
    "path": "manifest.json",
    "length": 642,
    "sha256": "..."
  },
  "files_manifest": {
    "path": "signature/files.json",
    "length": 1684,
    "sha256": "..."
  },
  "publisher_identity_digest": "sha256:...",
  "app_ownership_digest": "sha256:...",
  "app_key_delegation_digest": "sha256:...",
  "app_signing_key_id": "ed25519:...",
  "created_at": "2026-08-22T00:00:00Z"
}
```

Release Statement 必须与 `manifest.json` 交叉验证：

```text
app_id
version_name
release_sequence
channel
IKP format
Baga API range
permissions
capabilities
```

发生不一致时必须拒绝。

安全关键身份字段以 Release Statement 为签名依据；Manifest 不能通过修改绕过。

---

# 7. `signatures.json`

概念结构：

```json
{
  "type": "baga.signature-set",
  "format": "0.1",
  "signed_object": "signature/release-statement.json",
  "signed_object_sha256": "...",
  "signatures": [
    {
      "key_id": "ed25519:...",
      "algorithm": "ed25519",
      "signature": "base64url..."
    }
  ]
}
```

签名消息为：

```text
CanonicalJSON(release-statement.json)
```

而不是 `signatures.json` 自身。

规则：

- 每个 Key ID 最多出现一次；
- 多签名必须来自 Delegation 中允许的 Key；
- 有效签名数必须达到 Delegation Threshold；
- 无效或未知签名不能计入 Threshold；
- 额外未知签名可以忽略，但不得改变验证结果。

---

# 8. App Signing Key Delegation 验证

设备必须验证：

1. Delegation 的 `publisher_id` 与 Release 一致；
2. Delegation 的 `app_id` 与 Release 一致；
3. Delegation 由当前可信 Publisher Root Threshold 签名；
4. App Signing Key ID 与 Public Key 匹配；
5. Channel 在允许范围；
6. Release Sequence 在允许范围；
7. Delegation Status 为 `active`；
8. Delegation 未被更高 Sequence 撤销或替代；
9. 有效期检查通过；
10. Release Signature Threshold 满足。

App Signing Key 不因同属一个 Publisher 自动获得其他 App 的签名权限。

---

# 9. Publisher Identity Chain

设备必须能够验证：

```text
Trusted Publisher Genesis
         │
         ▼
Identity Update Sequence 2
         │
         ▼
Identity Update Sequence 3
         │
         ▼
Current Publisher Identity
```

每个更新文档必须：

- 引用上一文档 Digest；
- Sequence 递增 1；
- 满足上一 Root Threshold；
- Root Key 发生变化时满足新 Root Threshold；
- Publisher ID 不变。

设备不得跳过缺失的 Identity Sequence，除非一个明确的 Compact Proof 格式在后续规范中定义。

---

# 10. 正常 App Key Rotation

正常轮换不要求旧 App Signing Key 为新 Key 背书。

权威授权来自 Publisher Root：

```text
Publisher Root
      │
      ├── Delegation N → App Key A
      └── Delegation N+1 → App Key B
```

当 Delegation N+1 生效后：

- App Key A 可以标记 `retired`；
- 历史 Release 保持可验证；
- 新 Release 使用 App Key B；
- 设备保留旧 Delegation 用于验证已安装历史包。

如果 App Key A 被标记 `revoked`，应同时发布安全处置声明，并检查其签署 Release 是否需要撤销。

---

# 11. Publisher Root Rotation

正常 Root Rotation 必须使用 `publisher-identity` 更新链。

验证要求：

```text
Old Root Threshold
        signs
New Identity Document
        and
New Root Threshold
        signs acceptance
```

只有两侧 Threshold 都满足，设备才更新 Root Trust。

旧 Root 可以被移出当前 Key Set，但历史签名链必须可验证。

---

# 12. Emergency Recovery

当正常 Root Rotation 不可用时，使用 Recovery Statement。

概念结构：

```json
{
  "type": "baga.publisher-recovery",
  "format": "0.1",
  "publisher_id": "pub1_...",
  "recovery_sequence": 2,
  "last_trusted_identity_digest": "sha256:...",
  "new_identity_digest": "sha256:...",
  "reason": "root-key-loss",
  "incident_reference": "...",
  "not_before": "...",
  "created_at": "..."
}
```

必须同时满足：

```text
Publisher Recovery Threshold
+
Repository Security Recovery Attestation
+
Transparency Log publication
+
not_before cooling period
```

设备不得只凭 Market 账号或客服记录接受 Publisher Root 替换。

已长期离线设备第一次看到 Recovery 时，必须同时获得完整 Recovery Evidence。

---

# 13. App Transfer 签名

App Transfer 必须包含：

```text
Transfer-Out Statement signed by Old Publisher Root
Transfer-In Statement signed by New Publisher Root
Repository Transfer Attestation
```

新的 IKP Release Statement 使用新 Publisher ID。

设备只有在验证完整 Transfer Chain 后，才允许新 Publisher 的 App Signing Key 覆盖原 App。

Transfer 不自动授予新增权限，也不允许 Release Sequence 回退。

---

# 14. 容器 Digest 与逻辑 Payload Signature

Baga Ink 同时使用两种完整性验证：

## 14.1 Repository Container Digest

Repository Metadata 记录整个 `.ikp` 文件的：

```text
SHA-256
length
```

它保证下载到的 Container Bytes 与仓库发布版本完全一致。

## 14.2 Publisher Logical Payload Signature

Publisher Signature 通过 `files.json` 覆盖解包后的全部应用 Payload。

它保证即使 IKP 来自侧载，应用内容仍属于该 Publisher。

因此：

```text
Repository Digest
protects exact distributed container

Publisher Signature
protects app identity and logical payload
```

两者用途不同，不能互相替代。

---

# 15. Deterministic Packaging

Baga Ink SDK SHOULD 支持确定性生成 IKP：

- 固定 ZIP Entry 顺序；
- 固定时间戳策略；
- 固定权限位；
- 固定压缩参数；
- 不写入本地绝对路径；
- 不写入随机未签名字段。

确定性打包有利于：

- 可重复构建；
- 审核；
- 缓存；
- Delta；
- 第三方验证。

但设备的 Publisher Signature 验证必须基于规范逻辑 Payload，不假设所有工具都产生相同 ZIP Bytes。

---

# 16. 设备验证顺序

设备安装正式 IKP 时必须至少执行：

```text
1. 检查 Container 大小上限
2. 检查 ZIP / Path 安全
3. 读取 manifest.json 与 signature files
4. 检查 IKP Format
5. 验证 files.json Schema
6. 验证每个 Payload File Hash 与 Length
7. 验证 Publisher Genesis / Identity Chain
8. 验证 App Ownership
9. 验证 App Key Delegation
10. 验证 Release Statement Schema
11. 验证 Release Signature Threshold
12. 交叉检查 Manifest 与 Release Statement
13. 检查 Release Sequence
14. 检查撤销状态
15. 检查 Baga API / Capability / Permission
16. 才允许进入 staged install
```

如果来自 Repository，还必须在此之前或同时验证 Repository Metadata 与 Container Digest。

---

# 17. Sideload 验证

本地侧载的签名 IKP 没有 Repository Metadata 时：

- 必须完整验证 Publisher Signature；
- 必须显示 Publisher ID、App ID、Key Fingerprint；
- 第一次安装必须由用户确认 Publisher Trust；
- 不显示“Baga Ink Market 已审核”；
- 后续更新必须保持 App Identity；
- Security Revocation 只有在设备再次接入可信 Repository 后才能获得。

---

# 18. 未签名开发包

未签名 IKP 只允许 Developer Mode。

规则：

- 不建立正式 Publisher Identity；
- 不得覆盖正式应用身份；
- 必须显示持续警告；
- 可以使用临时开发者 Fingerprint；
- 退出 Developer Mode 后不能继续自动更新；
- 发布到正式 Repository 前必须重新打包并签名。

---

# 19. Key Storage 指南

Publisher Root / Recovery Key：

- SHOULD 离线；
- SHOULD 有加密备份；
- SHOULD 使用至少两个物理地点；
- MAY 使用硬件安全密钥、HSM、PKCS#11 或系统安全密钥库；
- MUST 不存放在公开 Web / Repository / CDN Server。

App Signing Key：

- MAY 保存在受保护 CI Signing Service；
- SHOULD 限制到具体 App / Channel；
- SHOULD 有最小访问人员；
- SHOULD 记录每次签名审计；
- 不应由 Market 服务器自动代持，除非开发者明确选择受托签名服务并接受相应信任模型。

---

# 20. Key Compromise 响应

## App Key 泄露

1. 立即停止发布；
2. 发布 Delegation Revocation；
3. 用 Root 委托新 App Key；
4. 审计泄露期间 Release；
5. 必要时发布 Security Revocation；
6. 写入 Transparency Log。

## Publisher Root 泄露

1. 如果旧 Threshold 尚未完全失陷，执行正常双向 Root Rotation；
2. 否则执行 Recovery Flow；
3. 冻结新 App Ownership / Transfer；
4. 审计全部 Delegation；
5. 公布恢复证据。

## Repository Key 泄露

不改变 Publisher Signature Chain；由 Repository Root 更新仓库角色密钥。

---

# 21. 版本规则

签名相关文档必须分别包含：

```text
format
sequence
created_at / effective_at
previous_digest（适用时）
critical fields declaration
```

解析器遇到：

- 更高但不支持的 Format Major：拒绝；
- 未知 Critical Field：拒绝；
- 低于本地 Sequence：拒绝；
- 相同 Sequence 不同 Digest：安全冲突，拒绝并报告；
- 相同 Release Sequence 不同 IKP Payload：拒绝。

---

# 22. 核心原则总结

```text
Publisher Root
      │
      ├── App Ownership
      ├── App Key Delegation
      ├── Root Rotation
      └── App Transfer
              │
              ▼
       App Signing Key
              │
              ▼
       IKP Release Statement
              │
              ▼
        files.json Payload
```

Market 可以验证、审核和分发这条链，但不能取代它。
