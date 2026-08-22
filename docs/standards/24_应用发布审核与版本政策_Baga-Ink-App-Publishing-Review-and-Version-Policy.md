# Baga Ink 应用发布、审核与版本政策 / Baga Ink App Publishing, Review and Version Policy

> **文档级别：分发层发布与治理规范**  
> **状态：Draft v0.1**  
> **日期：2026-08-22**  
> **上位文档：`20_市场与分发总体架构_Baga-Ink-Market-and-Distribution-Architecture.md`**  
> **身份规范：`21_发布者身份与应用所有权标准_Baga-Ink-Publisher-Identity-and-App-Ownership-Standard.md`**  
> **签名规范：`22_IKP签名与密钥生命周期标准_Baga-Ink-IKP-Signing-and-Key-Lifecycle-Standard.md`**

---

## 0. 目的

本文档定义 Baga Ink Market 及兼容第三方 Repository 中应用的注册、上传、版本、Channel、审核、发布、撤回和重新提交规则。

本规范把两类事情明确分开：

```text
协议与身份规则
=
什么软件字节属于谁、什么版本不可变、设备怎样安全验证

Market Policy
=
某个市场愿意收录什么、怎样审核、怎样展示和治理
```

Repository 可以拥有不同内容政策，但不得改变 App Identity、IKP Signature、Release Sequence、Permission、Capability 或 Update Safety 的标准语义。

---

# 1. 发布对象

一个正式发布对象由以下内容组成：

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

Market 必须保持开发者原始 Publisher Signature，不得把 IKP 重新签成 Market 所有。

Market 可以签署：

- Repository Metadata；
- Review Attestation；
- Policy Classification；
- Withdrawal / Revocation Record；
- App Transfer Attestation。

这些声明不能替代 Publisher Signature。

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

官方 Market 注册流程必须检查：

1. App Ownership Statement 签名有效；
2. `app_id` 尚未被其他 Publisher 合法占用；
3. 反向域名命名空间已按适用规则验证；
4. Publisher 账号有权管理该 Publisher Identity；
5. App ID 不冒充 Baga Ink、LifeBook、设备厂商或其他受保护名称；
6. App ID 与用户可见名称的差异不会构成欺骗。

App ID 注册不等于版本审核通过。

---

# 3. 版本的双字段模型

每个 Release 必须同时拥有：

```text
version_name
release_sequence
```

## 3.1 `version_name`

面向用户和开发者的可读版本，例如：

```text
1.4.2
2.0-beta.3
2026.08
```

建议使用语义化版本，但 Market 不把字符串排序作为安全更新顺序。

## 3.2 `release_sequence`

面向设备和仓库的单调递增非负整数。

例如：

```text
140
141
142
```

规则：

- 对同一 `app_id` 全局单调递增；
- 不因 Channel 分开计数；
- 不因 Repository 不同而重置；
- 正式发布后不得复用；
- 新 Release 必须大于 Publisher 已发布的最高 Sequence；
- 设备自动更新只比较受信任 Release Sequence，不解析 `version_name` 大小。

Channel 可以指向不同 Release，但不能改变 Release Sequence 的全局顺序。

---

# 4. Release 不可变性

一个正式发布由以下三元组唯一确定：

```text
app_id
release_sequence
package_sha256
```

一旦进入签名 Repository Metadata：

- 相同 `app_id + release_sequence` 必须永久指向同一个 IKP Digest；
- 不得在 CDN 上静默替换；
- 不得因“只改一行”而保留原 Sequence；
- Catalog 描述可以更正，但不能改变 Package 身份；
- 发现错误必须发布更高 Release Sequence；
- 原 Release 可以 Withdraw 或 Revoke，但不能被改写成另一份字节内容。

如果相同 Sequence 出现不同 Digest，客户端必须把它视为安全冲突并拒绝。

---

# 5. Release Channel

v0.1 标准 Channel：

```text
stable
beta
nightly
```

Repository 可以定义额外 Channel，但必须使用小写 ASCII 名称并在 Catalog 中解释。

规则：

- Channel 不是 App Identity；
- Channel 不是 Permission Boundary；
- Channel 不允许使用不同 Publisher Identity 冒充同一 App；
- 用户默认订阅 `stable`；
- 切换 Channel 必须由用户或受管理设备策略显式执行；
- 从较新 Sequence 的测试 Channel 返回较低 Sequence 的 Stable 属于显式 Downgrade，不是普通自动更新；
- Security Release 可以跨 Channel 推荐，但仍必须满足身份、权限和兼容规则。

---

# 6. 发布前本地验证

Baga Ink SDK 必须提供发布前检查：

```text
baga validate app.ikp
baga inspect app.ikp
baga sign app.ikp
baga verify app.ikp
```

至少检查：

- IKP Container 与路径安全；
- Manifest Schema；
- App ID；
- Release Sequence；
- API Range；
- Capability 与 Permission 注册状态；
- 禁止的设备私有执行依赖；
- 文件 Hash 清单；
- Publisher Identity Chain；
- App Ownership；
- App Key Delegation；
- Release Signature；
- 图标与基础 Catalog 字段；
- 包大小和资源限制。

本地验证通过不代表 Market 审核通过，但可以提前阻止结构性错误。

---

# 7. Market 上传接收

Market 接收 Release 时必须先执行不可变摄取流程：

```text
Receive bytes
      │
      ▼
Calculate container SHA-256 and length
      │
      ▼
Store in isolated quarantine
      │
      ▼
Verify Publisher / IKP
      │
      ▼
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

上传者不能在审核过程中替换相同 Submission 的 IKP 字节。

修改包内容必须创建新的 Release Sequence 和新 Submission。

---

# 8. 审核流水线

官方 Baga Ink Market 的 v0.1 审核至少包含以下阶段。

## 8.1 Identity and Signature

验证：

- Publisher Identity；
- App Ownership；
- App Signing Key Delegation；
- Release Signature；
- Release Sequence；
- App Transfer Chain（如有）。

## 8.2 Package Structure and Safety

验证：

- IKP 结构；
- 路径逃逸；
- Zip Bomb；
- 重复 Entry；
- 禁止的可执行依赖；
- Manifest 与 Release Statement 一致性；
- Payload Hash。

## 8.3 API and Portability

验证：

- 仅使用公开 `baga.*` API；
- 不使用设备品牌判断作为核心兼容方式；
- Capability / Permission 已注册；
- 不直接调用 Vendor SDK、Shell 或设备私有桥；
- Universal 声明与真实实现一致。

## 8.4 Compatibility

执行：

- IKP Validator；
- Baga Ink Reference Platform Tests；
- Manifest Capability 筛选；
- 必要的 Kindle 与 Android E-Paper Reference Device 测试；
- sleep / wake、offline start、storage、display 和 input 场景。

## 8.5 Permission Review

检查：

- 是否遵守最小权限原则；
- 权限是否与功能说明一致；
- 是否出现高风险新增权限；
- 用户数据写入、网络、蓝牙、文件与笔记权限是否有合理用途；
- Permission Diff 是否准确。

## 8.6 Privacy and Network

检查：

- 隐私政策或数据说明；
- 远程服务域名；
- 账号要求；
- Analytics / Crash Reporting；
- AI 服务与用户数据上传；
- 未经说明的数据收集；
- 明文秘密或嵌入式私钥。

## 8.7 E-Paper Quality

检查：

- 高频刷新；
- 无意义动画；
- 长期后台唤醒；
- 断网行为；
- 触摸以外输入；
- 灰阶可用性；
- 弱设备降级；
- 大面积残影风险。

## 8.8 Malware and Abuse

检查：

- 恶意网络行为；
- 账号窃取；
- 沙箱逃逸尝试；
- 供应链风险；
- 混淆后隐藏的高风险逻辑；
- 欺骗性 UI；
- 违反 Market 内容政策的行为。

## 8.9 Human Review

自动化结果不足以决定复杂隐私、欺骗、品牌冒用和用户伤害问题时，进入人工审核。

---

# 9. 审核状态

标准审核状态：

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

这些是 Market Workflow 状态，不是设备端 Release Status。

设备端 Release Status 由 `25` 号规范定义，例如：

```text
active
withdrawn
unlisted
security-revoked
superseded
```

---

# 10. Review Attestation

审核通过后，Market 可以生成独立 Review Attestation。

概念结构：

```json
{
  "type": "baga.review-attestation",
  "format": "0.1",
  "repository_id": "repo1_...",
  "app_id": "com.example.reader",
  "publisher_id": "pub1_...",
  "release_sequence": 142,
  "package_sha256": "...",
  "review_policy_version": "2026.08",
  "result": "approved",
  "compatibility_labels": ["universal"],
  "reviewed_at": "..."
}
```

Attestation 由 Market Review Key 签署并作为 Repository Target 发布。

它证明：

> 某个 Market 按某一版本政策审核了特定 Digest。

它不证明软件绝对无漏洞，也不替代 Publisher Signature。

第三方 Repository 不得伪造 Baga Ink Market Review Attestation。

---

# 11. Market Policy 与协议分离

以下属于 Market Policy，可以单独版本化：

- 内容分类；
- 隐私政策要求；
- 广告规则；
- AI 内容规则；
- 开源披露；
- 评论与评分；
- 收费和结算；
- 地区可用性；
- 审核时限；
- 品牌与商标规则。

以下属于平台协议，不得被 Market Policy 改写：

- Publisher Identity；
- App Ownership；
- IKP Signature；
- Release Sequence；
- Package Digest；
- Permission / Capability；
- Update Identity；
- Repository Metadata Verification。

---

# 12. Permission Diff

Market 必须计算当前 Stable Release 与新候选 Release 的 Permission Diff。

示例：

```text
Added:
+ bluetooth
+ user_files.write

Removed:
- clipboard
```

规则：

- 新增 Permission 必须在 Catalog 与更新 UI 中展示；
- 新增敏感 Permission 不得静默批准；
- 删除 Permission 可以自动应用；
- 权限名称必须来自正式 Registry；
- Market 文案不能把高风险写权限模糊成一般功能描述。

---

# 13. Capability 与兼容范围

Release 必须声明：

```text
required capabilities
optional capabilities
Baga API range
minimum platform profile（如适用）
```

Market 应计算：

```text
Latest overall release
Latest release compatible with this device
```

老设备不兼容新版时：

- 继续提供最新兼容旧版；
- 不把整个 App 标记为不可用；
- 显示新版为何不兼容；
- Security Revocation 时遵循 `25` 号规范。

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

可用模式：

```text
safe
snapshot-required
forward-only
```

- `safe`：旧版仍能读取当前数据；
- `snapshot-required`：激活前必须备份 App 私有数据；
- `forward-only`：数据迁移后旧版不可安全读取，必须显著提示且限制自动发布。

Market 对 `forward-only` Stable Release 应提高审核级别。

---

# 15. 分阶段发布

Market 可以支持 Phased Rollout：

```text
1%
5%
20%
50%
100%
```

Release Record 必须明确：

```text
rollout_id
rollout_percentage
rollout_start
rollout_pause_state
```

设备资格计算必须使用本地随机 `install_cohort_id` 与 `rollout_id` 的稳定 Hash，不使用设备序列号或硬件标识。

分阶段发布：

- 不能改变 Package Digest；
- 不能让同一 Sequence 指向不同包；
- 可以暂停后续新安装；
- 不能撤回已经成功安装的设备版本；
- Security Release 可以绕过普通阶段，但仍需签名和兼容验证。

---

# 16. 源代码与构建来源

Catalog 应支持：

```text
license
source_repository
source_commit
build_provenance
reproducible_build_status
sbom
```

这些字段可以提高透明度，但 v0.1 不强制所有 App 开源。

如果 App 声称开源或可重复构建：

- Source Commit 必须对应 Release；
- Build Attestation 必须引用 Package Digest；
- Market 不得仅凭仓库 URL 显示“已验证开源”；
- 第三方独立构建结果可以作为额外 Attestation。

---

# 17. 元数据更新与包更新分离

允许在不改变 IKP 的前提下更正：

- 描述；
- 截图；
- 本地化；
- 分类；
- 支持链接；
- 隐私说明；
- 搜索关键词。

不允许通过 Catalog 更新改变：

- App ID；
- Publisher ID；
- Release Sequence；
- Package Digest；
- Package Permission；
- Capability 要求；
- API Range；
- Data Schema；
- Publisher Signature。

安全关键字段只能来自不可变 Release Record 与签名 IKP。

---

# 18. 撤回与下架

Publisher 可以请求：

```text
withdraw release
unlist app
stop new installs
```

Market 可以因政策执行：

```text
suspend listing
security hold
reject future submissions
```

这些行为必须生成明确状态，不得通过删除记录制造“从未存在”的假象。

已经发布的 Package Digest、Publisher Identity 与审核历史应进入长期审计记录。

设备行为由 `25` 号规范决定。

---

# 19. 拒绝与申诉

Market Policy 应定义：

- 拒绝理由 Code；
- 可修复项；
- 是否需要新 Release Sequence；
- 人工复核入口；
- 安全事件快速通道；
- 申诉记录；
- 最终决定的审计信息。

如果 IKP 字节需要修改，必须新建 Release Sequence。

只有 Catalog 文案修正时，才可以不发布新 IKP。

---

# 20. 第三方 Repository

第三方 Repository 可以采用不同审核政策，例如：

```text
open-source-only
enterprise-internal
OEM-curated
community-unreviewed
```

但必须：

- 使用真实 Publisher Identity；
- 验证 IKP Signature；
- 保持 Release 不可变；
- 不伪造官方 Review Attestation；
- 明确显示自己的审核级别；
- 不让同名不同 Publisher App 静默覆盖。

---

# 21. 发布闭环

正式发布流程：

```text
Register App ID
      │
      ▼
Create / verify App Ownership
      │
      ▼
Build IKP
      │
      ▼
Validate and sign with delegated App Key
      │
      ▼
Upload immutable package
      │
      ▼
Identity / structure / policy / compatibility review
      │
      ▼
Create Release Record and Review Attestation
      │
      ▼
Publish Repository Metadata atomically
      │
      ▼
Write Transparency Event
      │
      ▼
Devices may discover and install
```

---

# 22. 最终原则

> **Market 可以决定是否收录，但不能改变软件身份；Publisher 可以发布新版本，但不能改写已发布版本；设备可以选择是否更新，但只能沿合法身份链更新。**
