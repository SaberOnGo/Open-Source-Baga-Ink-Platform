# Baga Ink 应用更新、回滚与撤销协议 / Baga Ink Update, Rollback and Revocation Protocol

> **文档级别：分发层核心设备协议**  
> **状态：Draft v0.1**  
> **日期：2026-08-22**  
> **上位文档：`20_市场与分发总体架构_Baga-Ink-Market-and-Distribution-Architecture.md`**  
> **仓库协议：`23_仓库元数据与索引协议_Baga-Ink-Repository-Metadata-and-Index-Protocol.md`**  
> **发布政策：`24_应用发布审核与版本政策_Baga-Ink-App-Publishing-Review-and-Version-Policy.md`**

---

## 0. 目的

本文档定义 Baga Ink Platform 如何：

- 发现更新；
- 选择与设备兼容的候选版本；
- 比较应用身份、权限和数据 Schema；
- 下载完整 IKP 或 Delta；
- staged install；
- 原子激活；
- 健康确认；
- 自动回滚；
- 显式降级；
- 处理 Withdrawn、Unlisted、Security Revoked 等状态；
- 在断网、断电、存储不足和设备休眠下保持可恢复。

核心原则：

> **下载不是安装，验证不是激活，激活不是健康；每一步都必须独立成功。**

---

# 1. 更新身份前提

更新候选必须先证明它有权覆盖当前安装应用。

默认要求：

```text
candidate.app_id == installed.app_id
candidate.publisher_id == installed.publisher_id
Publisher Identity Chain valid
App Ownership valid
App Signing Key Delegation valid
Repository Source Policy valid
```

Publisher 发生变化时，必须存在完整有效 App Transfer Chain。

相同 `app_id`、不同 Publisher Identity 的包不得作为更新；它只能在用户显式清除原应用身份后按新应用处理。

---

# 2. 本地安装记录

Platform 必须为每个正式 App 保存：

```json
{
  "app_id": "com.example.reader",
  "publisher_id": "pub1_...",
  "source_repository_id": "repo1_...",
  "channel": "stable",
  "current_release_sequence": 142,
  "current_version_name": "1.4.2",
  "current_package_sha256": "...",
  "current_data_schema_version": 4,
  "permissions_granted": [],
  "last_known_good_release": 141,
  "update_state": "idle"
}
```

该记录必须原子持久化，并与实际激活包进行一致性检查。

Platform 不得只根据目录名猜测当前版本。

---

# 3. 候选版本选择

Repository 可以包含多个 Release。

Platform / Baga Ink Client 筛选顺序：

```text
1. Repository Metadata trusted
2. Release status installable
3. App Identity continuity valid
4. Source Repository policy valid
5. Channel selected
6. Release Sequence higher than current
7. Baga API range compatible
8. Required Capabilities satisfied
9. Device compatibility status allows install
10. Package not security-revoked
11. Rollout cohort eligible
12. Permission and data migration policy acceptable
```

如果最新总体版本不兼容，选择：

> **Latest Compatible Release**

而不是简单报告 App 不可用。

---

# 4. Release Sequence

自动更新必须满足：

```text
candidate.release_sequence > current.release_sequence
```

`version_name` 不用于安全排序。

相同 Release Sequence：

- 相同 Digest：视为同一版本；
- 不同 Digest：安全冲突，拒绝；
- 不得通过不同 Channel 复用；
- 不得通过不同 Repository 复用为另一份字节内容。

较低 Release Sequence 只能通过显式 Downgrade 或自动 Rollback 到本地上一已知可用版本。

---

# 5. 更新状态机

标准状态：

```text
IDLE
  │
  ▼
METADATA_VERIFIED
  │
  ▼
CANDIDATE_SELECTED
  │
  ▼
AWAITING_USER_APPROVAL      optional
  │
  ▼
DOWNLOADING
  │
  ▼
PACKAGE_VERIFIED
  │
  ▼
STAGED
  │
  ▼
ACTIVATING
  │
  ▼
PROBATION
  │
  ├── healthy ───────→ ACTIVE
  │
  └── failed ────────→ ROLLING_BACK
                              │
                              ▼
                         PREVIOUS_ACTIVE
```

任何中间状态都必须可在设备重启后恢复或安全清理。

---

# 6. 状态持久化

每次重要状态变化前后必须记录 Journal：

```text
operation_id
app_id
from_release
candidate_release
state
staging_path
expected_digest
previous_active_path
started_at
last_updated_at
```

恢复规则：

- `DOWNLOADING`：可继续或清理临时文件；
- `PACKAGE_VERIFIED`：可重新检查后继续；
- `STAGED`：可重新验证后激活；
- `ACTIVATING`：检查当前指针与包完整性；
- `PROBATION`：如果设备重启原因未知，可继续健康检查或回滚；
- `ROLLING_BACK`：优先恢复上一可用版本；
- 无完整 Journal 的临时目录不得自动激活。

---

# 7. 下载与缓存

下载必须：

- 只写入 staging；
- 设置 Metadata 声明的最大长度；
- 流式计算 SHA-256；
- 支持安全断点续传；
- 完成后重新检查总长度；
- 不因 HTTP 200 就视为成功；
- 不因文件扩展名正确就视为 IKP；
- 下载失败不修改当前应用；
- 缓存命中仍要重新验证 Digest。

完整 IKP Cache 可以按内容摘要去重。

---

# 8. 完整包验证

进入 `PACKAGE_VERIFIED` 前必须完成：

```text
Repository target length and SHA-256
IKP container and path safety
IKP file manifest hashes
Publisher Identity Chain
App Ownership
App Signing Key Delegation
Release Signature
Manifest / Release Record consistency
Release Sequence
Revocation status
API / Capability / Permission
Resource limits
```

任何失败都不得进入 staged install。

---

# 9. Staged Install

验证后的 IKP 必须安装到新的不可变版本目录，例如：

```text
apps/<app_id>/versions/<release_sequence>-<digest>/
```

当前激活版本使用小型原子指针：

```text
apps/<app_id>/current
```

具体文件系统实现可以不同，但必须满足：

- 旧版本继续完整存在；
- 新版本不能覆盖旧版本文件；
- 新版本写入完成并持久化后才能切换；
- 切换要么完全成功，要么保持旧指针；
- App 私有数据与应用包分离；
- 更新 App 包不默认删除 App 数据。

---

# 10. 激活

激活流程：

```text
1. Stop / pause current App safely
2. Flush current App state
3. Verify staged package digest again if needed
4. Prepare data migration snapshot according to policy
5. Atomically switch active package pointer
6. Start candidate in probation mode
7. Run health checks
8. Mark candidate as last-known-good only after success
```

如果步骤 1–5 失败，继续使用旧版本。

---

# 11. 健康确认

进入 `ACTIVE` 前，候选版本必须通过最小健康确认。

Platform 级健康条件：

```text
Package can be loaded
Entry point starts
No immediate uncaught startup failure
App responds to lifecycle / UI event loop
App sandbox remains accessible
Mandatory startup deadline met
No repeated crash loop
```

App 可以通过标准 API 报告：

```text
startup_ready
basic_state_loaded
migration_complete
```

但 App 自报健康不能替代 Platform 的崩溃和超时判断。

Reference App 或高风险更新可以要求更长 Probation Window。

---

# 12. Crash Loop

Platform 必须检测：

```text
N startup failures within a bounded window
```

具体阈值由 Platform Profile 定义。

检测到候选 Crash Loop 时：

1. 停止继续自动启动候选；
2. 标记 Release 为 local-failed；
3. 回滚到上一已知可用版本；
4. 保留诊断信息；
5. 不删除用户数据；
6. 暂停对同一 Digest 的自动重试；
7. 提示用户可查看详情或重新尝试。

---

# 13. 自动回滚

自动回滚允许的目标：

```text
last_known_good_release
```

它不是一般意义上的自由降级。

自动回滚必须满足：

- 目标包已在本地完整验证；
- Publisher Identity 与原安装一致；
- Package Digest 与本地记录一致；
- 目标没有 Security Revoked；
- 数据 Schema 仍可被旧版安全读取，或存在可恢复快照；
- 回滚原因与结果记录到本地日志。

回滚后不能立刻再次自动安装同一失败 Digest。

---

# 14. 显式 Downgrade

用户主动安装较低 Release Sequence 属于 Downgrade。

Downgrade 必须：

- 显式显示当前与目标版本；
- 重新验证 Publisher Identity；
- 检查目标是否 Security Revoked；
- 检查数据 Schema；
- 提示可能丢失的新功能或数据；
- 要求用户确认；
- 不通过接受旧 Repository Metadata 实现；
- 使用当前可信 Repository 对历史 Target 的描述，或已验证本地包。

Market / Platform 可以禁止 Downgrade 到已知不安全版本。

---

# 15. 数据 Schema 迁移

Release 必须声明：

```text
data_schema_version
rollback.mode
rollback.minimum_compatible_schema
```

## 15.1 `safe`

候选数据写入仍能被上一版本理解。

自动回滚可以不恢复 App Data Snapshot，但仍应保持写入原子性。

## 15.2 `snapshot-required`

激活前必须创建 App 私有数据快照或等价事务点。

回滚时恢复该快照。

## 15.3 `forward-only`

候选完成迁移后，旧版不能安全读取数据。

要求：

- Stable 自动更新前显著提示；
- 应优先备份可导出用户数据；
- Platform 不能承诺自动回滚；
- 健康确认必须在不可逆提交前尽可能完成；
- App 必须提供恢复或重新同步策略；
- 高风险设备可默认不自动安装。

---

# 16. 迁移的两阶段提交

推荐数据迁移流程：

```text
Prepare migration
      │
      ▼
Create snapshot / transaction
      │
      ▼
Run migration in candidate namespace
      │
      ▼
Validate migrated data
      │
      ▼
Activate candidate
      │
      ▼
Commit migration after health confirmation
```

迁移应：

- 可重入或可检测已完成；
- 不因 sleep / wake 重复破坏数据；
- 使用迁移 Journal；
- 不在包验证前执行；
- 不在用户取消更新后继续后台运行。

---

# 17. Permission Diff

候选版本新增 Permission 时，Platform 必须比较：

```text
current declared permissions
candidate declared permissions
current granted permissions
```

结果分类：

```text
No change
Removed permissions
Added low-risk permissions
Added sensitive permissions
Changed scope / semantics
```

规则：

- 删除 Permission 可以随更新自动收窄；
- 新增 Permission 不自动继承 Grant；
- 新增敏感 Permission 必须由用户确认；
- 用户拒绝新增 Permission 时，更新可以取消，或在 App 明确支持时安装但保持该 Permission denied；
- Permission Registry 语义变化必须触发重新审核；
- App Transfer 不自动继承新增权限。

---

# 18. Channel 与切换

用户订阅某一 Channel 后，自动更新只选择该 Channel 的候选。

Channel 切换：

- Stable → Beta：显式确认；
- Beta → Stable：如果 Stable Sequence 较低，按 Downgrade 规则；
- Nightly：默认关闭自动安装或明确提示高风险；
- Security Revocation：可以推荐其他 Channel 的安全 Release，但不能跳过身份和权限检查。

---

# 19. 分阶段发布

设备是否进入某一 Rollout，使用：

```text
bucket
=
Hash(install_cohort_id || rollout_id) mod 10000
```

规则：

- `install_cohort_id` 本地随机生成；
- 不使用设备序列号、IMEI、广告 ID 或用户账号作为必需输入；
- 同一 `rollout_id` 对同一设备结果稳定；
- Rollout Percentage 只能扩大或暂停，不能让同一 Release 字节变化；
- 已安装设备不因 Rollout 缩小自动回退；
- Rollout 暂停只阻止新激活。

---

# 20. Delta Update

Delta 是可选优化，不是独立版本。

Delta Record 必须声明：

```text
base_package_sha256
base_release_sequence
target_package_sha256
target_release_sequence
delta_sha256
delta_length
algorithm
```

规则：

- 只有本地 Base Digest 精确匹配时才能应用；
- Delta 本身作为 Repository Target 验证；
- 应用完成后必须验证完整 Target IKP 的 Length 与 SHA-256；
- 最终 IKP 仍必须通过 Publisher Signature 验证；
- Delta 失败或空间不足时回退完整 IKP；
- 不允许通过 Delta 绕过 Permission / Manifest / Signature 验证；
- v0.1 不锁死具体 Delta Algorithm。

---

# 21. Release Status

标准状态：

## `active`

允许发现、新安装和更新。

## `superseded`

存在更新版本，但该 Release 仍可用于兼容旧设备和回滚。

## `withdrawn`

开发者或 Market 不再推荐新安装，通常因为普通 Bug。

默认行为：

- 不向新用户推荐；
- 已安装版本继续运行；
- 如果有替代版本，推荐更新；
- 本地回滚可以在无安全问题时继续使用。

## `unlisted`

不出现在普通搜索或推荐中，但直接引用、已有用户更新或企业部署可按 Policy 继续。

## `security-revoked`

存在恶意代码、密钥泄露或严重安全问题。

默认行为：

- 禁止新安装；
- 禁止作为自动回滚目标；
- 停止向该版本更新；
- 显示安全警告；
- 优先推荐修复版本或安全旧版；
- 是否阻止启动取决于严重级别和平台安全政策。

---

# 22. Security Revocation 严重级别

```text
low
medium
high
critical
```

## Low / Medium

- 警告；
- 停止新安装；
- 推荐更新；
- 默认不强制停止当前 App。

## High

- 强警告；
- 停止新安装和重新安装；
- 禁止回滚到该版本；
- 可限制敏感权限；
- 推荐立即更新或停用。

## Critical

适用于已确认的主动恶意行为、凭据窃取或大规模破坏风险。

Platform 可以：

- 阻止启动；
- 撤销 App 的敏感权限；
- 隔离包；
- 保留用户数据等待安全迁移；
- 要求用户明确处置。

但第一阶段不把“Market 可以无提示远程删除用户 App 和数据”作为默认能力。

任何强制措施必须基于签名 Security Revocation Record，并保留本地审计记录。

---

# 23. 撤销记录验证

Revocation Record 必须：

- 作为 Repository Target 验证；
- 引用 App ID、Release Sequence 和 Package Digest；
- 由 Repository Security Role 或受 Root 授权的专用 Role 签名；
- 包含 Severity、Reason Code、Effective Time；
- 可引用替代 Release；
- 写入 Transparency Log；
- 不通过普通 Catalog 文案代替。

Publisher 可以请求 Security Revocation，但 Repository 必须独立签署发布。

---

# 24. Repository 不可用

Repository 暂时不可用、Timestamp 过期或设备长期离线时：

- 已安装 App 继续运行；
- 不发现新更新；
- 不把“无法证明当前安全状态”等同于“当前 App 已被撤销”；
- 本地已有签名 Revocation 继续生效；
- 用户可以通过 Baga Ink Client 导入新的离线 Repository Snapshot；
- 不能通过把系统时钟调回过去延长 Metadata 有效期。

---

# 25. 用户数据

无论更新、回滚、撤回或撤销：

- 默认不删除用户书籍；
- 默认不删除用户笔记；
- 默认不删除 App 私有用户数据；
- App 包与用户数据分开；
- 卸载和清除数据必须是不同动作；
- Critical Revocation 隔离 App 时仍应尽量允许安全导出用户数据；
- 任何破坏性迁移必须显式说明。

---

# 26. 更新审计记录

Platform 应记录：

```text
operation_id
app_id
from_release
to_release
repository_id
package_digest
publisher_id
permission_diff
data_schema_transition
verification_result
activation_result
health_result
rollback_result
timestamps
```

不得在普通更新日志中记录用户书籍内容、笔记正文、Token 或其他敏感数据。

---

# 27. 自动更新默认政策

建议默认：

- Stable Release；
- 同一 Publisher Identity；
- 同一 Source Repository；
- 更高 Release Sequence；
- 无新增敏感 Permission；
- Data Schema 为 `safe` 或可自动 Snapshot；
- Device Compatibility 通过；
- 非 Security Revoked；
- 网络与电源条件适合；
- 下载完成后由 Platform 自主选择低干扰激活时机。

不满足时进入用户确认或保持当前版本。

---

# 28. 最终原则

> **更新的目标不是让设备永远追上最新版本，而是让设备始终运行“身份正确、设备兼容、权限可接受、数据可恢复”的最新安全版本。**
