# Baga Ink 分发客户端与离线传输协议 / Baga Ink Distribution Client and Offline Transfer Protocol

> **文档级别：分发层客户端与传输协议**  
> **状态：Draft v0.1**  
> **日期：2026-08-22**  
> **上位文档：`20_市场与分发总体架构_Baga-Ink-Market-and-Distribution-Architecture.md`**  
> **仓库协议：`23_仓库元数据与索引协议_Baga-Ink-Repository-Metadata-and-Index-Protocol.md`**  
> **更新协议：`25_应用更新回滚与撤销协议_Baga-Ink-Update-Rollback-and-Revocation-Protocol.md`**

---

## 0. 目的

本文档定义 Baga Ink Client 以及设备直接联网、USB、局域网、本地文件和长期离线环境中的应用分发流程。

核心原则：

> **Baga Ink Client 是设备管理工具和可信数据的搬运者，不是应用身份或仓库身份的最终信任根。**

无论包经过什么电脑、U 盘、网络或 Mirror，最终安装前必须由设备上的 Baga Ink Platform 按相同标准重新验证。

---

# 1. 支持的分发模式

v0.1 定义五种模式。

## 1.1 Device Direct

设备直接访问 Repository 与 Package Storage。

## 1.2 Managed Transfer

Baga Ink Client 在线获取 Repository 数据，再通过：

```text
USB
Local network
Device-specific file bridge
```

传输到设备。

## 1.3 Portable Repository Snapshot

Baga Ink Client 或管理服务器生成一个自洽、可离线携带的 Repository 子集。

## 1.4 Signed IKP Sideload

用户通过本地文件安装带 Publisher Signature 的 IKP，但没有完整 Repository Metadata。

## 1.5 Unsigned Developer Transfer

仅 Developer Mode 使用的未签名测试包。

---

# 2. 信任边界

## 2.1 设备必须最终验证

Baga Ink Client 可以提前执行：

- Repository Metadata 验证；
- IKP Digest 验证；
- Publisher Signature 验证；
- Compatibility 筛选；
- Permission Diff 计算。

但设备仍必须重新验证：

```text
Repository Root / Metadata（Repository 安装时）
Package Length / SHA-256
IKP Publisher Signature
App Identity Continuity
Release Sequence
Revocation Status
API / Capability / Permission
Install State
```

PC 的“验证通过”消息不能替代设备验证。

## 2.2 Client 不持有最高密钥

Baga Ink Client 不应持有：

- Repository Root Private Key；
- Publisher Root Private Key；
- Publisher Recovery Private Key；
- Market Review Private Key；
- 其他开发者 App Signing Private Key。

开发者专用签名工具可以与 Client 同机运行，但必须是明确分离的开发者流程。

---

# 3. Device Direct 流程

```text
Device
  │
  ├── Update trusted Repository Metadata
  ├── Select latest compatible Release
  ├── Display Permission / Compatibility information
  ├── Download immutable IKP target
  ├── Verify repository digest and publisher signature
  ├── Stage
  └── Activate according to Update Protocol
```

设备直接联网时仍应：

- 支持断点续传；
- 限制下载长度；
- 休眠后安全恢复；
- 避免持续轮询；
- 优先 Wi-Fi / 充电策略；
- 保存 Trusted Time Floor；
- 不把 HTTPS 证书替代 Repository Signature。

---

# 4. Managed Transfer 流程

```text
Repository
    │
    ▼
Baga Ink Client
    │
    ├── Verify and cache
    ├── Identify connected device
    ├── Select compatible releases
    └── Transfer signed evidence + IKP
    │
    ▼
Baga Ink Platform
    │
    ├── Verify again
    ├── Stage
    └── Activate
```

Baga Ink Client 必须把设备当作最终决策者。

Client 不能通过私有参数命令设备“跳过签名”“忽略权限”或“强制激活未验证包”。

---

# 5. Device Handshake

设备连接后，Baga Ink Client 与 Platform 建立会话。

设备可以返回：

```json
{
  "protocol": "baga-transfer/0.1",
  "device_session_id": "random-session-id",
  "platform_version": "0.1.0",
  "baga_api_version": "0.1",
  "ikp_formats": ["0.2"],
  "capabilities_digest": "sha256:...",
  "compatibility_status": "compatible",
  "free_storage_bytes": 536870912,
  "max_transfer_chunk": 1048576,
  "supported_hashes": ["sha256"],
  "installed_inventory_digest": "sha256:..."
}
```

原则：

- `device_session_id` 每次会话随机生成；
- 不要求暴露硬件序列号；
- Device Descriptor 中用于兼容判断的型号/固件信息可以按必要范围提供；
- 默认不把用户账号、书库内容或笔记元数据发给 Client；
- Client 必须验证设备上的 Platform 协议版本，而不是只识别 USB Vendor ID。

---

# 6. 设备识别与安装路线

Baga Ink Client 可能需要先识别尚未安装 Platform 的设备。

这类安装路线属于：

```text
Device Model
+
Firmware / OS Version
+
Current installation state
+
Verified installation route record
```

Client 必须显示：

```text
Compatible
Experimental
Unsupported
```

Platform 安装过程和 App 分发过程必须分开记录。

设备完成 Platform 安装后，IKP 分发只使用本规范，不因 Kindle / Android 底层安装方式不同而改变应用信任规则。

---

# 7. Transfer Session

每次传输应建立 Session Manifest。

概念结构：

```json
{
  "type": "baga.transfer-session",
  "format": "0.1",
  "session_id": "...",
  "repository_id": "repo1_...",
  "created_at": "...",
  "items": [
    {
      "kind": "ikp",
      "app_id": "com.example.reader",
      "release_sequence": 142,
      "path": "targets/packages/sha256/...ikp",
      "length": 2837461,
      "sha256": "..."
    }
  ]
}
```

Session Manifest 用于：

- 进度；
- 缓存；
- 断点续传；
- 用户确认；
- 诊断。

它不是安全信任根；其中每个 Item 必须由 Repository Metadata 或 IKP Publisher Signature 独立验证。

---

# 8. Chunked Transfer

大文件传输可以分块。

每块至少包含：

```text
session_id
item_digest
chunk_offset
chunk_length
chunk_bytes
```

接收端必须：

- 检查 Offset / Length 越界；
- 不允许重叠块产生歧义；
- 写入 staging；
- 保存已接收范围；
- 完成后计算整个 Target SHA-256；
- 不把单块校验替代最终完整 Digest；
- 设备重启后只恢复有完整 Journal 的传输。

可选 Chunk Hash 只用于快速检测传输错误，不替代最终 Repository Target Digest。

---

# 9. 断点续传

断点续传必须绑定：

```text
repository_id
item_sha256
item_length
release_sequence
session protocol version
```

如果任一值变化，旧 Partial File 必须废弃。

HTTP Range、USB Chunk 或局域网 Resume 都不得把不同版本的字节拼在一起。

完成后必须从头到尾重新计算完整 SHA-256。

---

# 10. Portable Repository Snapshot

离线 Repository Snapshot 是一个目录或归档容器。

v0.1 不锁死文件扩展名，逻辑结构如下：

```text
baga-offline-snapshot/
├── transfer-manifest.json
├── metadata/
│   ├── 1.root.json
│   ├── ...
│   ├── timestamp.json
│   ├── <version>.snapshot.json
│   ├── <version>.targets.json
│   └── delegated/
└── targets/
    ├── packages/sha256/
    ├── releases/sha256/
    ├── publishers/sha256/
    ├── revocations/sha256/
    ├── catalog/sha256/
    └── assets/sha256/
```

`transfer-manifest.json` 只是清单和用户体验辅助。

真正安全依据仍是：

```text
Trusted Repository Root
→ Timestamp
→ Snapshot
→ Targets
→ Target Digest
→ IKP Publisher Signature
```

---

# 11. Offline Snapshot 生成

生成离线快照时，Client 必须：

1. 使用本地 Trusted Root 验证最新 Repository Metadata；
2. 选择目标设备或 Profile 需要的 Release；
3. 收集完整 Root Update Chain；
4. 收集 Timestamp、Snapshot、Targets / Delegated Targets；
5. 收集 Release Record、Publisher Documents、Revocation Record；
6. 收集 IKP 与必要 Catalog / Asset；
7. 验证所有 Target Digest；
8. 生成 Transfer Manifest；
9. 不修改原 Repository Metadata；
10. 将快照写入新目录并最终原子完成。

快照可以是完整仓库，也可以是目标设备所需子集；子集仍必须包含可验证该 Target 的完整元数据链。

---

# 12. Offline Snapshot 导入

设备导入时必须：

1. 从本地 Trusted Root 开始；
2. 顺序验证更新的 Root；
3. 验证 Timestamp / Snapshot / Targets；
4. 检查 Metadata Version 不回退；
5. 检查 Trusted Time Floor；
6. 验证 Release Record 与 Revocation；
7. 验证 IKP Digest；
8. 验证 Publisher Identity 与 Signature；
9. 重新检查 Compatibility / Permission；
10. 按 `25` 号协议安装。

离线文件所在 U 盘、PC 或局域网共享目录不需要被信任。

---

# 13. Trusted Time

Baga Ink Client 不得把普通 PC 系统时间当作设备可信时间。

在线或离线传输必须携带 Repository Timestamp Metadata 中被签名的 `generated_at`。

设备仅在验证 Timestamp Signature 后提高：

```text
last_trusted_time_floor
```

PC 可以显示“本机时间可能不正确”，但不能通过传一个未签名日期绕过 Metadata Expiration。

---

# 14. Signed IKP Sideload

用户直接选择一个 `.ikp` 文件时：

```text
No Repository Metadata
        │
        ▼
Verify Publisher Signature
        │
        ▼
Display App ID / Publisher ID / Fingerprint
        │
        ▼
Check against installed identity
        │
        ▼
User confirms trust and permissions
        │
        ▼
Stage and activate
```

Sideload 必须显示：

- 来源：本地文件；
- 未经官方 Market 审核（如果没有 Attestation）；
- Publisher ID；
- App ID；
- Key Fingerprint；
- Permission；
- API / Capability 兼容性；
- 是否覆盖已安装应用。

Sideload 不能自动信任同目录中的其他 Publisher。

---

# 15. Developer Mode

Developer Mode 必须由用户显式开启。

未签名 IKP：

- 只能安装到开发命名空间或独立开发身份；
- 不得覆盖正式安装；
- 显示持续开发标识；
- 可以有较短保留期限；
- 不能参与普通自动更新；
- 不能显示官方审核标签；
- 应支持一键清除全部开发包而不影响正式应用数据。

开发者需要测试升级时，可以使用本地测试 Publisher Key，而不是长期关闭所有签名检查。

---

# 16. Source Repository Pinning

正式 Repository 安装后，设备保存 `source_repository_id`。

Baga Ink Client 可以展示其他 Repository 的同 App，但默认不能替设备静默切换来源。

Source Migration 必须由设备或用户确认，并验证：

- Repository Root Trust；
- Publisher Identity；
- App Transfer Chain（如有）；
- Release Sequence；
- Permission Diff；
- Revocation；
- Data Schema。

Mirror Host 变化但 Repository ID 相同，不算迁移。

---

# 17. Compatibility Filtering

Client 可以根据设备 Capability 和 Platform Version 筛选：

```text
installable
update_available
latest_compatible
incompatible
experimental
```

但设备必须再次计算。

Client 不能因为自己的设备数据库声称“支持”，就覆盖 Device Adapter 的真实 Capability 检测。

对于未知固件：

- 默认 Experimental 或 Unsupported；
- 不以同系列其他型号推测；
- 不自动执行高风险 Platform 安装或 App 更新。

---

# 18. Permission UI

Client 应显示：

```text
Current permissions
Candidate permissions
Added
Removed
Denied
```

新增敏感 Permission 时，用户批准必须最终记录在设备上。

Client 上点击“同意”可以作为传输意图，但设备仍应显示或确认最终授权，除非：

- 设备属于明确的企业管理模式；
- 已存在受信任管理策略；
- Policy Signature 与设备配置匹配。

v0.1 普通消费者设备不默认接受 PC 代替用户授予敏感权限。

---

# 19. Privacy

Client / Device Handshake 默认不得上传或暴露：

- 用户书籍列表；
- 笔记正文；
- 阅读位置；
- LifeBook 人生记录；
- 用户账号 Token；
- 设备序列号；
- Wi-Fi 密码；
- 私有文件路径。

兼容判断需要的最小信息可以包括：

```text
device family
model ID
firmware / OS version
Platform version
Capability set or digest
free storage
installed app identities and release sequences
```

安装清单传给 Repository 前应尽量本地处理。

Rollout 使用本地随机 Cohort ID，不使用硬件 ID。

---

# 20. Baga Ink Client 缓存

Client 可以缓存：

```text
Trusted Repository Metadata
Content-addressed IKP
Release Records
Publisher Documents
Catalog Records
Assets
Offline Snapshots
```

缓存必须：

- 以 Repository ID 和 Digest 分区；
- 不用文件名替代 Digest；
- 重新使用前验证；
- 对过期 Metadata 不发现新 Release；
- 可以保留不可变 Target 供离线设备使用；
- 不把一个 Repository 的同路径文件用于另一个 Repository。

---

# 21. 错误模型

标准错误类别：

```text
device_not_detected
platform_not_installed
platform_incompatible
repository_untrusted
metadata_expired
metadata_rollback
package_digest_mismatch
publisher_untrusted
identity_mismatch
permission_confirmation_required
capability_missing
insufficient_storage
transfer_interrupted
device_busy
install_failed
rollback_completed
```

Client 应向普通用户显示可理解原因，同时保存机器可读错误 Code。

---

# 22. 恢复与重试

传输失败时：

- 不删除当前 App；
- 不把 Partial File 当作 IKP；
- 允许按 Digest 恢复；
- 设备 sleep / wake 后可继续；
- Client 断开后设备可以清理过期 Session；
- 重试不会重复批准 Permission；
- 失败的 Candidate 不被标记为 Active；
- Update Journal 与 Transfer Journal 分开。

---

# 23. 企业 / OEM 管理

未来可支持签名 Management Policy：

```text
trusted repositories
allowed publishers
required apps
blocked apps
approved permissions
update windows
channel policy
```

管理策略必须：

- 使用独立设备管理信任根；
- 不冒充 Publisher Signature；
- 不改变 IKP 字节；
- 不允许普通 Repository 自称设备管理员；
- 向设备所有者清晰标记管理状态。

v0.1 不在本协议定义完整企业管理格式。

---

# 24. 最终原则

> **Client 可以让安装变简单，但不能让验证变少；离线可以改变传输路线，但不能改变信任链。**
