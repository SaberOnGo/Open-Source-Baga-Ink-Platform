# Baga Ink 市场与分发总体架构 / Baga Ink Market and Distribution Architecture

> **文档级别：分发层顶层设计 / Distribution Architecture**  
> **状态：Draft v0.1**  
> **日期：2026-08-22**  
> **上位规范：`01_顶层战略与架构_Baga-Ink-Platform-Strategy.md`**  
> **配套规范：`21–28` 分发层规范**

---

## 0. 目的

本文档定义 Baga Ink 应用从开发者到用户设备的完整分发架构。

它回答：

> **一个开发者怎样把已经签名的 IKP，安全、可审计、可回滚地送到 Kindle 与 Android 墨水屏设备，同时保持开放生态而不重新碎片化。**

分发层必须同时支持：

- Baga Ink Market 官方市场；
- 第三方 Baga Ink Repository；
- 设备直接联网安装；
- Baga Ink Client 经 USB / 局域网传输；
- 长期离线设备；
- 本地签名 IKP 侧载；
- 开发者模式下的未签名测试包。

无论经过哪条传输路径，设备端必须执行同一套身份、签名、仓库元数据、兼容性、权限与安装验证。

---

# 1. 研究后的设计结论

Baga Ink 不照搬单一平台，而采用以下成熟实践的组合：

1. **TUF**：Root / Targets / Snapshot / Timestamp 角色分离、版本单调递增、过期检查、目标文件 Hash 与长度、抗回滚与冻结；
2. **Uptane**：离线更新仍执行完整验证、更新失败不应让设备进入不可恢复状态、设备/硬件适配必须准确匹配；
3. **Apple Code Signing**：应用身份不是名称本身，而是稳定标识符与签名主体共同构成；
4. **Android APK v3**：签名密钥轮换必须有可验证的连续授权关系；
5. **APT / F-Droid**：签名仓库索引、包 Hash、第三方仓库、增量索引；
6. **OCI / Nix / OSTree**：内容寻址、不可变对象、摘要与大小验证、离线静态增量包；
7. **RAUC / Mender / Raspberry Pi A/B**：先验证后切换、保留上一可用版本、健康确认、失败回退；
8. **Sigstore Rekor**：追加式透明日志、包含证明与独立监控；
9. **Sparkle**：独立发布签名、人类版本号与机器版本号分离、Channel、分阶段发布、Delta 失败后回退完整包；
10. **Ubuntu Core Assertions**：账号、密钥、应用声明、版本确认与策略分别使用签名声明表达。

Baga Ink 的原则是：

> **复用经过验证的安全模型，不自行发明密码学；保持设备验证代码足够窄，不把完整商店业务塞入设备。**

---

# 2. 产品与协议必须分开

## 2.1 Baga Ink Market

Baga Ink Market 是用户与开发者看到的产品，包括：

```text
应用搜索
分类与推荐
应用详情
本地化描述
截图与图标
开发者信息
审核状态
安装与更新入口
评论、评分、付费等未来产品能力
```

## 2.2 Baga Ink Repository Protocol

Repository Protocol 是底层开放分发协议，包括：

```text
Repository trust root
Signed metadata
Publisher identity
IKP digest and size
Release records
Channels
Update state
Withdrawal / revocation
Catalog indexes and diffs
Mirrors / CDN
Offline repository snapshots
```

Baga Ink Market 必须使用该协议，但该协议不只服务于官方 Market。

第三方仓库也可以实现相同协议：

```text
Baga Ink Repository Protocol
            │
      ┌─────┴────────────┐
      │                  │
Baga Ink Market     Third-party Repository
Official default    Community / OEM / Enterprise
```

第三方仓库不得改变 IKP、App Standard、API、Capability 或 Permission 的语义。

---

# 3. 三层信任模型

Baga Ink 分发必须同时验证三层信任。

## 3.1 Publisher Trust

证明：

> **这个 IKP 确实由拥有该 App 的发布者授权。**

由以下内容实现：

```text
Publisher Identity
Publisher Root Key Set
App Ownership Statement
App Signing Key Delegation
IKP Release Signature
```

## 3.2 Repository Trust

证明：

> **这个版本、Digest、长度、Channel、状态和审核信息确实属于当前可信仓库状态。**

由受约束的 TUF 元数据角色实现：

```text
root.json
timestamp.json
snapshot.json
targets.json
```

## 3.3 Local Installed Identity

证明：

> **当前设备已经安装的 App，只能由同一身份连续链或经过正式转移的身份更新。**

设备本地至少保存：

```text
app_id
publisher_id
publisher_lineage
source_repository_id
current_release_sequence
current_package_digest
current_channel
last_known_good_release
permissions_granted
```

任意一层验证失败，安装或更新必须停止。

---

# 4. 应用身份

应用不能只由用户可见名称识别。

Baga Ink 应用身份定义为：

```text
App Identity
=
Application ID
+
Publisher ID
+
Publisher Identity Lineage
```

例如两个仓库都包含：

```text
com.example.reader
```

它们只有在 Publisher ID 与身份连续链一致时，才可能被视为同一个应用。

Repository 不能仅凭相同 `app_id` 覆盖已安装应用。

---

# 5. Market 不重新签成 Baga 所有

开发者发布 IKP 时，IKP 保留发布者签名。

正确关系：

```text
Publisher App Signing Key
          │
          ▼
       app.ikp
          │
          ├── Publisher signature
          └── Publisher identity chain

Baga Ink Market
          │
          └── Signs repository metadata and review attestations
```

Baga Ink Market 不得移除发布者签名后，把所有应用重新签成 Baga 自己所有。

原因：

- 发布者身份可以跨仓库保持；
- 第三方仓库不能冒充开发者；
- Market 下架不等于开发者身份消失；
- 用户可以验证软件究竟由谁发布；
- 官方 Market 与开放生态之间不会形成不必要的身份锁定。

Market 可以附加独立的审核声明，但不得取代 Publisher Signature。

---

# 6. 内容寻址与不可变发布

所有正式 IKP 必须以 SHA-256 内容摘要标识。

推荐路径：

```text
packages/sha256/ab/abcdef...1234.ikp
```

Release Record 引用：

```json
{
  "sha256": "abcdef...1234",
  "length": 2837461
}
```

相同 Digest 永远表示相同字节内容。

正式发布后：

```text
同一个 app_id
+ 同一个 release_sequence
```

必须永久映射到同一个 IKP Digest。

内容变化必须发布新的 Release Sequence，不能静默覆盖旧文件。

这一规则允许：

- CDN 与 Mirror 不必成为信任根；
- 包天然去重；
- 历史版本可审计；
- 下载可断点续传；
- Delta 最终结果可通过完整目标 Digest 验证。

---

# 7. 安全元数据与产品目录分离

## 7.1 安全关键元数据

包括：

```text
Repository root
Role keys and thresholds
Release digest and length
Release sequence
Publisher identity references
Channel
Withdrawal / revocation status
Metadata versions and expiration
```

设备必须严格验证。

## 7.2 产品目录数据

包括：

```text
应用简介
截图
图标
分类
推荐语
搜索关键词
评分
评论
编辑推荐
```

这些数据必须有完整性保护，但不能成为安装身份或更新身份的唯一依据。

搜索服务器返回“某版本可安装”，设备仍必须回到签名 Repository Metadata 做最终判断。

---

# 8. 分发路径

## 8.1 设备直接联网

```text
Baga Ink Platform
       │
       ├── Fetch signed repository metadata
       ├── Select compatible release
       ├── Download IKP from CDN / mirror
       └── Verify and activate locally
```

## 8.2 Baga Ink Client 经 USB / 局域网

```text
Repository
    │
    ▼
Baga Ink Client
    │  acts only as courier and management UI
    ▼
Device
    │
    └── Performs final verification again
```

PC / Mac 可以提前验证和筛选，但不能成为设备的最终信任根。

## 8.3 离线仓库快照

Baga Ink Client 可以把：

```text
Trusted root
Repository metadata chain
Required release records
IKP blobs
Catalog subset
```

打包为可携带的离线仓库快照。

设备导入时执行与在线模式一致的版本、过期、Digest、Publisher、Permission 和 Compatibility 验证。

## 8.4 本地签名 IKP 侧载

没有 Repository Metadata 时，可以作为显式侧载流程：

- 验证 IKP Publisher Signature；
- 显示 Publisher ID 与 Fingerprint；
- 要求用户建立或确认本地信任；
- 不自动获得 Baga Ink Market 审核背书；
- 后续更新默认仍绑定同一 Publisher Identity。

## 8.5 未签名开发包

只允许在 Developer Mode：

- 必须由用户显式开启；
- Baga Ink Client 与设备都显示明显警告；
- 不得伪装成 Market 安装；
- 不得覆盖正式签名应用，除非用户显式清除原身份并确认风险。

---

# 9. 第三方仓库与 Source Pinning

每个 Repository 必须拥有独立：

```text
repository_id
root metadata
root fingerprint
metadata version state
```

官方 Baga Ink Market 的 Root Trust 可以随 Platform 预置。

添加第三方 Repository 必须：

- 显示仓库名称与 Root Fingerprint；
- 由用户显式确认；
- 保存本地 Repository Trust；
- 不允许 URL 相同替代 Root Identity；
- Root 轮换必须按签名链进行。

首次从某仓库安装 App 后，默认保存：

```text
source_repository_id
```

自动更新只从原仓库或同一 Root Trust 的 Mirror 获取。

跨仓库迁移必须满足：

1. Publisher Identity 相同或存在合法 App Transfer Chain；
2. 用户显式批准更换 Source Repository；
3. 新仓库 Release Sequence 与安全状态有效；
4. 新仓库不能降低已有权限与身份保护。

---

# 10. 威胁模型

分发层至少必须应对：

```text
CDN / Mirror 被控制
Repository Web Server 被控制
旧的合法元数据被重复投递
部分新、部分旧元数据混合
旧 IKP 被当作新版本返回
开发者 Market 账号被盗
App Signing Key 被盗
Publisher Root Key 丢失或被盗
第三方仓库 App ID 冲突
USB / PC 被恶意软件控制
下载中断或存储不足
更新后 App 无法启动
新版本偷偷增加权限
恶意撤回或远程删除争议
设备时钟不准确或长期离线
```

设计必须遵循：

> **任何单一服务器、传输通道或账号被攻破，都不应立即获得伪造所有 App 更新的能力。**

---

# 11. 更新与恢复总原则

分发层必须：

- 先验证，再写入正式位置；
- 使用 staging；
- 原子切换当前版本指针；
- 保留上一已知可用 IKP；
- 新版本未确认健康前，不删除旧版；
- 更新失败不删除用户数据；
- Delta 失败后回退到完整 IKP；
- 新增敏感权限不得静默批准；
- 显式 Downgrade 与自动 Rollback 分开处理；
- Security Revocation 不等同于默认远程静默卸载。

具体状态机由 `25_应用更新回滚与撤销协议` 定义。

---

# 12. 透明日志的角色

透明日志用于：

```text
Publisher 创建
App ID 注册
App Ownership 变化
Signing Key Delegation
Publisher Root Rotation
Emergency Recovery
Release Publish
App Transfer
Version Withdrawal
Security Revocation
Review Attestation
```

透明日志是**审计证据**，不是设备安装时唯一信任根。

设备在第一阶段可以不在线查询日志；Market、开发者与独立监控者必须能验证日志追加性和事件包含证明。

---

# 13. 组件职责

## Baga Ink Developers

- 账号与团队管理；
- Publisher Identity 创建与展示；
- App ID 注册；
- Release 上传；
- 审核反馈；
- Key Rotation / Recovery 流程；
- Transparency 查询。

## Baga Ink Market Server

- 验证 Publisher Signature；
- 验证 App Ownership；
- 执行审核；
- 生成 Release Record；
- 生成签名 Repository Metadata；
- 发布 Catalog；
- 生成 Withdrawal / Revocation；
- 写入 Transparency Log。

## CDN / Mirror

- 存储并传输不可变 Blob；
- 不负责决定哪一个版本可信；
- 不持有 Publisher Private Key；
- 不持有 Repository Root Private Key。

## Baga Ink Client

- 识别设备；
- 拉取、缓存、筛选和传输仓库数据；
- 提供 USB / 局域网管理；
- 显示兼容性与权限变化；
- 不替设备跳过最终验证。

## Baga Ink Platform

- 保存 Repository Root Trust；
- 保存 Installed Identity；
- 验证 Repository Metadata；
- 验证 IKP Publisher Signature；
- 重新检查 Compatibility 与 Permission；
- staged install / atomic switch / rollback；
- 保存审计所需的本地安装状态。

---

# 14. 非目标

v0.1 不试图一次定义：

- 付费结算；
- DRM；
- 订阅收据；
- 广告竞价；
- 用户评论治理；
- 设备遥测商业系统；
- 强制所有第三方仓库接受官方 Market Policy；
- 每台设备在线验证 Transparency Log；
- 跨 App 的复杂依赖解析器。

这些能力不得反过来削弱 Publisher Identity、Repository Trust 或本地更新身份。

---

# 15. 分发层规范地图

```text
20 市场与分发总体架构
│
├── 21 Publisher Identity & App Ownership
├── 22 IKP Signing & Key Lifecycle
├── 23 Repository Metadata & Index Protocol
├── 24 Publishing, Review & Version Policy
├── 25 Update, Rollback & Revocation Protocol
├── 26 Distribution Client & Offline Transfer
├── 27 Transparency & Security Audit
└── 28 Catalog & App Discovery
```

依赖关系：

```text
Publisher Identity
      │
      ▼
IKP Signature
      │
      ├──────────────┐
      ▼              ▼
Repository       Publishing Review
Metadata             │
      │               ▼
      └────────→ Update / Revocation
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
Distribution Client        Catalog / Discovery
                      │
                      ▼
             Transparency / Audit
```

---

# 16. 研究依据

本设计主要参考以下官方规范与项目文档：

- [The Update Framework Specification](https://theupdateframework.github.io/specification/)
- [TUF Roles and Metadata](https://theupdateframework.io/docs/metadata/)
- [Uptane Standard](https://uptane.org/docs/2.0.0/standard/uptane-standard)
- [Uptane Offline Updates](https://uptane.org/enhancements/pures/pure2)
- [Android APK Signature Scheme v3](https://source.android.com/docs/security/features/apksigning/v3)
- [Apple Code Signing Guide](https://developer.apple.com/library/archive/documentation/Security/Conceptual/CodeSigningGuide/)
- [Debian apt-secure](https://manpages.debian.org/apt/apt-secure.8.en.html)
- [F-Droid Repository APIs](https://f-droid.org/docs/All_our_APIs/)
- [F-Droid Security Model](https://f-droid.org/docs/Security_Model/)
- [OCI Distribution Specification](https://github.com/opencontainers/distribution-spec/blob/main/spec.md)
- [OSTree Static Deltas](https://ostreedev.github.io/ostree/copying-deltas/)
- [Mender Sign and Verify](https://docs.mender.io/artifact-creation/sign-and-verify)
- [RAUC Documentation](https://rauc.readthedocs.io/)
- [Sigstore Rekor](https://docs.sigstore.dev/logging/overview/)
- [Sparkle Publishing Updates](https://sparkle-project.org/documentation/publishing/)
- [Ubuntu Core Assertions](https://documentation.ubuntu.com/core/reference/assertions/)
- [Raspberry Pi Update Documentation](https://www.raspberrypi.com/documentation/computers/os.html)

---

# 17. 最终原则

> **Publisher 证明软件是谁发布的；Repository 证明当前应当分发什么；设备本地记录证明什么可以覆盖已安装应用。**

只有三层同时成立，Baga Ink 才执行安装或更新。
