# Baga Ink 规范可执行化设计 / Baga Ink Executable Specification Design

> **文档级别：架构实施设计 / Implementation Architecture Design**  
> **状态：Approved Design Baseline v0.1**  
> **日期：2026-08-22**  
> **上位标准：`docs/standards/21–28`**  
> **目标：把分发、身份、签名、仓库、更新与离线传输规范变成可执行、可互操作、可拒绝错误输入的 Conformance Kit。**

---

## 0. 设计目标

本设计把 `21–28` 从文字规范推进为 **Executable Specification**。

目标不是立刻构建完整 Baga Ink Market，而是建立一套足以回答下面问题的可执行基线：

> **同一份 Publisher Identity、IKP、Repository Metadata、Release 与 Update Evidence，是否能被两个独立实现按照相同规则接受或拒绝？**

第一阶段必须交付：

1. JSON Schema；
2. Canonical JSON Test Vectors；
3. 正向密码学向量；
4. 非法样本库；
5. Python Reference Implementation；
6. 最小 Rust Device Verifier；
7. TUF Conformance Adapter；
8. 最小 Repository → Client → Device 验证原型；
9. CI；
10. Stable Gate。

只有上述门槛通过后，相关 Draft 标准才有资格进入 Stable 评审。

---

# 1. 总体方案

采用：

> **语言无关机器规范 + Python Reference Implementation + Rust Independent Device Verifier**

架构：

```text
                  docs/standards/21–28
                           │
                           ▼
                  Machine-readable Spec
                 ┌─────────┴─────────┐
                 │                   │
             JSON Schema         Test Vectors
                 │                   │
                 └─────────┬─────────┘
                           ▼
                 Python Reference Impl
                           │
             ┌─────────────┼─────────────┐
             │             │             │
         IKP Signer    Repository     Client/Device
         /Verifier      Generator      Reference
             │             │             │
             └─────────────┼─────────────┘
                           ▼
                      End-to-End
                           │
                           ▼
                 Rust Device Verifier
                           │
                           ▼
                  Cross-language Tests
```

Python 用于：

- Schema 验证；
- 测试向量生成；
- Publisher / Signing 参考实现；
- IKP 构建与验证；
- TUF Repository / Client；
- 最小分发原型；
- Fixtures 与 CI。

Rust 第一阶段只实现设备端关键验证链：

- strict JSON；
- RFC 8785 JCS；
- SHA-256；
- Ed25519；
- Publisher Genesis；
- App Ownership；
- App Key Delegation；
- Release Statement；
- IKP Payload Hash；
- App Identity consistency。

Rust 不承担 Market、Repository Generator 或审核流程。

---

# 2. 仓库目录

新增：

```text
spec/
├── schemas/
│   ├── identity/
│   ├── signing/
│   ├── repository/
│   ├── publishing/
│   ├── update/
│   ├── transfer/
│   ├── transparency/
│   └── catalog/
│
├── vectors/
│   ├── canonical-json/
│   ├── signatures/
│   ├── key-rotation/
│   ├── app-transfer/
│   └── hashes/
│
└── fixtures/
    ├── ikp/
    │   ├── valid/
    │   └── invalid/
    ├── repository/
    ├── updates/
    └── recovery/

reference/
├── python/
│   ├── pyproject.toml
│   └── src/baga_spec/
│       ├── __init__.py
│       ├── strict_json.py
│       ├── canonical.py
│       ├── schemas.py
│       ├── crypto.py
│       ├── identity.py
│       ├── signing.py
│       ├── ikp.py
│       ├── repository.py
│       ├── client.py
│       ├── device.py
│       └── errors.py
│
└── rust/
    └── baga-verifier/
        ├── Cargo.toml
        └── src/
            ├── main.rs
            ├── canonical.rs
            ├── identity.rs
            ├── signing.rs
            └── ikp.rs

tools/
├── baga-spec
├── tuf-client-under-test
├── generate-vectors
└── build-test-ikp

tests/
├── test_schemas.py
├── test_strict_json.py
├── test_canonical.py
├── test_identity.py
├── test_signing.py
├── test_ikp.py
├── test_invalid_fixtures.py
├── test_repository.py
├── test_update.py
├── test_cross_language.py
└── test_end_to_end.py

.github/workflows/
├── conformance.yml
└── tuf-conformance.yml
```

规范文档仍位于：

```text
docs/standards/
```

机器规范不得替代文字规范；它们是文字规范的可执行对应物。

---

# 3. JSON 与 Canonicalization

## 3.1 自定义 Baga 签名对象

以下自定义签名对象统一采用：

> **RFC 8785 JSON Canonicalization Scheme (JCS)**

签名前必须经过：

```text
UTF-8 decode
→ Strict JSON parse
→ I-JSON constraints
→ Schema validation
→ RFC 8785 canonicalization
→ SHA-256 / Ed25519
```

严格解析必须拒绝：

- 重复 Object Key；
- NaN；
- Infinity；
- `-Infinity`；
- 无效 Unicode；
- 超出 Schema 允许范围的数值；
- 安全关键结构中的未知字段。

## 3.2 TUF Metadata

TUF 元数据不使用 Baga JCS 规则重新签名。

```text
root.json
timestamp.json
snapshot.json
targets.json
```

必须完全遵守所采用 TUF 版本的序列化与签名语义。

Baga Ink 自定义字段只能作为 TUF Profile 允许的位置和方式存在。

---

# 4. JSON Schema 基线

使用：

> **JSON Schema Draft 2020-12**

安全关键对象默认：

```json
{
  "additionalProperties": false
}
```

Schema ID 使用稳定 URN，不提前绑定未确定的公网域名：

```text
urn:baga:schema:<name>:<version>
```

第一批 Schema：

```text
identity/
├── publisher-genesis.schema.json
├── publisher-root-update.schema.json
├── app-ownership.schema.json
├── app-key-delegation.schema.json
└── app-transfer.schema.json

signing/
├── files-manifest.schema.json
├── release-statement.schema.json
└── signature-envelope.schema.json

repository/
├── release-record.schema.json
└── baga-target-custom.schema.json

publishing/
└── review-attestation.schema.json

update/
├── revocation-statement.schema.json
└── update-journal.schema.json

transfer/
├── transfer-session.schema.json
└── offline-snapshot-manifest.schema.json

transparency/
├── transparency-event.schema.json
└── transparency-checkpoint.schema.json

catalog/
├── catalog-root.schema.json
├── catalog-app-record.schema.json
└── catalog-diff.schema.json
```

每个 Schema 必须：

- 指定 `$schema`；
- 指定 `$id`；
- 限定 `type` / `format`；
- 对 Identifier、Digest、Sequence、Timestamp 设置明确格式；
- 明确 required 字段；
- 对安全关键结构禁止未知字段；
- 提供至少一个 valid fixture 与一个 invalid fixture。

---

# 5. Identifier 与基础编码

第一阶段统一：

```text
SHA-256 digest   → lowercase hex，前缀 `sha256:`
Ed25519 key id   → `ed25519:` + lowercase hex SHA-256(public_key_bytes)
Publisher ID     → `pub1_` + base32lower(SHA-256(canonical genesis body))
Repository ID    → `repo1_` + base32lower(SHA-256(canonical trusted root identity body))
Event ID         → `evt1_` + base32lower(SHA-256(canonical event body))
```

Base32：

- lowercase；
- RFC 4648 alphabet；
- no padding。

Base64 字段：

- URL-safe；
- no padding。

Timestamp：

```text
RFC 3339 UTC
YYYY-MM-DDTHH:MM:SSZ
```

第一阶段不允许本地时区 Offset 进入被签名安全对象。

---

# 6. Python Reference Implementation

## 6.1 Python 基线

第一阶段目标：

```text
Python >= 3.12
```

核心依赖：

```text
jsonschema
rfc8785
cryptography
python-tuf
pytest
```

如依赖实际包 API 与预期不一致，以兼容当前稳定版为原则调整实现，但不得改变规范语义。

## 6.2 `strict_json.py`

职责只有：

- UTF-8 decode；
- Duplicate Key rejection；
- 非有限数 rejection；
- 解析深度与输入大小限制；
- 返回普通 Python 数据结构。

它不负责 Schema。

## 6.3 `canonical.py`

职责：

- RFC 8785 JCS；
- 输出唯一 UTF-8 bytes；
- 提供 canonical hash helper。

禁止把自制排序 JSON 当作 JCS。

## 6.4 `schemas.py`

职责：

- 加载本仓库 `spec/schemas/`；
- Draft 2020-12 验证；
- 统一 Schema 错误模型；
- 禁止自动修复输入。

## 6.5 `crypto.py`

只封装：

```text
SHA-256
Ed25519 sign
Ed25519 verify
key fingerprint
```

不发明密码算法。

## 6.6 `identity.py`

实现：

- Publisher ID；
- Publisher Genesis 验证；
- App Ownership；
- App Key Delegation；
- Root / App Key rotation；
- App Transfer；
- Identity Lineage 验证。

## 6.7 `signing.py`

实现 Release Statement 和签名 Envelope。

输入必须先通过 strict JSON + Schema。

## 6.8 `ikp.py`

实现：

- ZIP 安全解析；
- Duplicate Entry detection；
- Path traversal rejection；
- 解压大小限制；
- `manifest.json` 验证；
- `files.json` 验证；
- Payload Hash；
- Publisher Identity Chain；
- Release Signature；
- Manifest / Release consistency。

## 6.9 `repository.py`

使用 `python-tuf` 作为 TUF 核心。

Baga 层只处理：

- Baga Target Custom metadata；
- Release Record；
- Content-addressed target layout；
- Offline snapshot export/import。

## 6.10 `client.py`

模拟 Baga Ink Client 的可信数据搬运逻辑：

- Refresh Repository；
- Select Release；
- Download Target；
- 验证 Repository Evidence；
- 生成 Transfer Session；
- 不作为最终信任根。

## 6.11 `device.py`

模拟设备端最终验证：

```text
Repository Evidence
+ IKP
+ Installed Identity
+ Compatibility Profile
+ Granted Permissions
→ ACCEPT / REQUIRE_APPROVAL / REJECT
```

---

# 7. Rust Independent Device Verifier

第一阶段二进制：

```text
baga-verifier
```

命令：

```text
baga-verifier canonical <json>
baga-verifier verify-statement <statement> <signature-envelope>
baga-verifier verify-ikp <file.ikp>
```

Rust 必须读取与 Python 完全相同的：

```text
spec/vectors/
spec/fixtures/
```

第一阶段 Rust 不实现：

- Market API；
- TUF Repository Generator；
- Catalog；
- Transparency Log Server；
- Review Policy。

目标是证明**设备关键签名语义具有跨语言互操作性**。

---

# 8. Canonical Test Vectors

每个向量目录包含：

```text
input.json
canonical.bin / canonical.hex
sha256.txt
metadata.json
```

第一批至少覆盖：

```text
empty object
nested object
unicode
escaped characters
object key ordering
arrays
integer boundaries
negative zero handling
non-ascii keys
publisher genesis
app ownership
app key delegation
release statement
app transfer
```

非法 JCS / I-JSON 输入单独进入 invalid corpus，不生成 canonical output。

Python 与 Rust 必须产生逐字节相同 canonical bytes 与 SHA-256。

---

# 9. 密码学测试向量

每套向量必须固定：

```text
private key seed（只允许测试用途）
public key
key id
canonical statement bytes
statement sha256
signature
expected verification result
```

生产实现禁止加载测试私钥。

第一批：

```text
Publisher Genesis
App Ownership
App Signing Delegation
Release Statement
App Key Rotation
Publisher Root Rotation
App Transfer
Revocation Statement
```

---

# 10. 非法样本库

非法样本是规范的一等资产。

目录按期望拒绝原因分组：

```text
spec/fixtures/invalid/
├── json/
├── schema/
├── identity/
├── signing/
├── ikp/
├── repository/
├── update/
└── transfer/
```

第一阶段至少包含：

```text
duplicate-json-key
nan-number
infinity-number
unknown-critical-field
wrong-app-id
wrong-publisher-id
wrong-package-hash
wrong-package-length
invalid-ed25519-signature
undelegated-app-key
expired-delegation
revoked-key
broken-key-rotation-chain
unauthorized-app-transfer
release-sequence-rollback
same-sequence-different-digest
path-traversal-ikp
duplicate-zip-entry
zip-bomb-limit
permission-not-in-manifest
repository-mix-and-match
expired-timestamp
rollback-root
rollback-snapshot
offline-snapshot-incomplete
```

每个 invalid fixture 必须声明：

```json
{
  "expected": "reject",
  "error_code": "...",
  "standard": "22",
  "rule": "..."
}
```

测试不得只断言“抛异常”，还要断言稳定错误类别。

---

# 11. 错误模型

Reference Implementation 统一错误码：

```text
invalid_json
invalid_schema
non_canonical_input
invalid_identifier
invalid_hash
invalid_signature
unknown_key
undelegated_key
expired_delegation
revoked_key
identity_mismatch
sequence_rollback
sequence_conflict
unsafe_path
duplicate_entry
resource_limit
repository_untrusted
metadata_expired
metadata_rollback
metadata_inconsistent
permission_escalation
incompatible
revoked_release
internal_error
```

Rust 与 Python 对同一 fixture 应返回同一错误类别；具体错误文字可以不同。

---

# 12. TUF Conformance

提供：

```text
tools/tuf-client-under-test
```

实现官方 Conformance CLI：

```text
init
refresh
download
```

CI 使用：

```text
theupdateframework/tuf-conformance@v2
```

规则：

- TUF 规范 MUST 项不得 xfail；
- Baga Repository Profile MUST 项不得 xfail；
- Baga 明确不支持的可选算法或可选功能可以在 `.xfails` 中登记；
- 每个 xfail 必须带注释说明为什么不是 Baga Profile Requirement；
- Unexpected Pass 必须触发人工检查是否应该删除 xfail。

---

# 13. 最小 Repository

构建一个本地静态 Repository：

```text
examples/minimal-repository/
├── metadata/
│   ├── root.json
│   ├── timestamp.json
│   ├── snapshot.json
│   └── targets.json
└── targets/
    ├── packages/sha256/...ikp
    ├── releases/sha256/...json
    └── publishers/sha256/...json
```

它必须使用真实 Ed25519 测试密钥和真实 TUF Metadata。

Repository 不需要 Web Application Server；测试可以通过本地 HTTP Server 提供静态文件。

---

# 14. 最小 Client

Reference Client 不实现完整 UI。

只实现：

```text
repo init
repo refresh
app list
app fetch
app prepare-transfer
```

输出机器可读 JSON。

它负责：

- TUF Refresh；
- 选择 Release；
- 下载目标；
- 验证 Digest；
- 生成 Transfer Session。

它不能告诉设备“跳过最终验证”。

---

# 15. 最小 Device Prototype

不模拟 Kindle GUI 或 Android GUI。

设备原型只模拟信任与安装状态：

```text
state/
├── repositories/
├── installed-apps/
├── staging/
└── active/
```

命令：

```text
device import-transfer
device verify
device stage
device activate
device health-ok
device health-fail
device rollback
```

状态改变必须可观察并持久化。

第一阶段使用普通文件系统模拟原子激活指针。

---

# 16. End-to-End 场景

必须至少自动化以下场景。

## E2E-001 首次安装

```text
Publisher → Sign IKP → Repository → Client → Device → Active
```

预期：PASS。

## E2E-002 正常更新

```text
Release Sequence 1 → 2
```

预期：新版本进入 ACTIVE，旧版本保留为 Last Known Good。

## E2E-003 下载损坏

预期：Hash 验证失败，不进入 STAGED。

## E2E-004 错误 Publisher

相同 App ID，不同 Publisher，无 Transfer。

预期：REJECT。

## E2E-005 Sequence Rollback

当前 Sequence 2，Repository 提供 Sequence 1。

预期：自动更新 REJECT。

## E2E-006 Permission Escalation

新版新增敏感权限。

预期：`REQUIRE_APPROVAL`，不得静默激活。

## E2E-007 Health Failure

新版激活进入 Probation 后报告失败。

预期：自动回滚上一可用版本。

## E2E-008 Update Interruption

在 Download / Stage / Activate 中断并重新启动 Device Prototype。

预期：恢复到一致状态，不出现半安装版本。

## E2E-009 Offline Snapshot

完整离线 Snapshot 经 Client 搬运到设备。

预期：设备无需信任 Client 即可独立完成验证。

## E2E-010 Security Revocation

当前候选版本被 Security Revoked。

预期：禁止新安装 / 自动更新，并按 25 号协议返回稳定状态。

---

# 17. CI

`conformance.yml`：

```text
Python install
Schema tests
Strict JSON tests
Canonical vectors
Signature vectors
Invalid fixtures
IKP tests
Repository tests
Update tests
Build Rust verifier
Rust tests
Python ↔ Rust cross-language tests
End-to-end tests
```

`tuf-conformance.yml`：

```text
Build / install Python reference client
Run official tuf-conformance@v2
Upload result artifacts on failure
```

CI 必须在 Pull Request 与 `main` push 运行。

---

# 18. Stable Gate

相关规范从 Draft 进入 Stable 前，必须满足：

```text
JSON Schema suite                 PASS
Strict JSON suite                 PASS
RFC 8785 canonical vectors        PASS
Positive signature vectors        PASS
Negative corpus                   PASS
Python IKP verifier               PASS
Rust independent verifier         PASS
Python/Rust byte-for-byte vectors PASS
TUF required conformance          PASS
Minimal Repository E2E            PASS
Offline Transfer E2E              PASS
Update / Rollback E2E             PASS
No unexplained xfail              PASS
```

额外硬规则：

> **任何影响签名字节表示、身份连续性或更新授权的规范，在至少两个独立实现对同一测试向量达成一致前，不得标记 Stable。**

---

# 19. 第一阶段不实现

本阶段明确不实现：

- 完整 Market Web 服务；
- 用户评论与评分；
- 支付；
- DRM；
- 商业授权；
- 完整 Transparency Log Server；
- 完整 OEM Device Adapter；
- Kindle / Android 真机安装器；
- UI Market Client；
- 云账户系统。

这些不影响验证 21–28 的安全与互操作闭环。

---

# 20. 实施顺序

```text
Phase 1
Repository scaffolding + Python project + CI baseline

Phase 2
Strict JSON + RFC8785 + JSON Schema

Phase 3
Identity + Signing + canonical vectors

Phase 4
IKP builder / verifier + invalid corpus

Phase 5
Rust verifier + cross-language vectors

Phase 6
python-tuf Repository + Client + TUF conformance CLI

Phase 7
Device Prototype + staged activation + rollback

Phase 8
End-to-End suite + Stable Gate report
```

每个 Phase 必须先有失败测试，再实现到测试通过。

---

# 21. 成功标准

本阶段完成时，应能够执行一个命令集合，证明：

```text
同一个签名声明
→ Python 与 Rust 得到同一 canonical bytes
→ 两端验证同一 Ed25519 签名

同一个合法 IKP
→ 两端接受

同一个非法 IKP
→ 两端按相同错误类别拒绝

同一个 Repository
→ 官方 TUF Conformance 客户端流程通过

同一个 Release
→ Client 搬运后 Device 独立重验

一个失败更新
→ 不破坏上一可用 App
```

只有做到这些，Baga Ink `21–28` 才从“写得合理的标准”真正变成“可执行、可互操作的标准”。
