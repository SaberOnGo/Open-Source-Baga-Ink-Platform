# Baga Ink 市场目录与应用发现规范 / Baga Ink Catalog and App Discovery Specification

> **文档级别：分发层目录与发现规范**  
> **状态：Draft v0.1**  
> **日期：2026-08-22**  
> **上位文档：`20_市场与分发总体架构_Baga-Ink-Market-and-Distribution-Architecture.md`**  
> **仓库协议：`23_仓库元数据与索引协议_Baga-Ink-Repository-Metadata-and-Index-Protocol.md`**  
> **发布政策：`24_应用发布审核与版本政策_Baga-Ink-App-Publishing-Review-and-Version-Policy.md`**

---

## 0. 目的

本文档定义 Baga Ink Market 与兼容第三方 Repository 的应用目录、应用详情、本地化、分类、搜索、兼容版本发现、低带宽索引、差分更新、离线目录、图片资源、推荐与广告标识规则。

最重要的边界：

> **Catalog 帮助用户发现 App，但不能决定 App 身份、版本真实性或能否覆盖已安装应用。**

最终安装判断必须回到：

```text
Signed Repository Metadata
Release Record
Publisher Identity
IKP Publisher Signature
Local Installed Identity
Compatibility and Permission Check
```

---

# 1. Catalog 与安全元数据分离

## 1.1 Catalog 数据

Catalog 包括：

```text
应用名称
一句话介绍
详细描述
本地化
图标
截图
分类
标签
搜索关键词
Publisher 展示信息
License / Source 信息
隐私摘要
Permission 摘要
兼容性摘要
推荐与榜单
```

## 1.2 安全关键数据

Catalog 不得成为以下内容的唯一来源：

```text
app_id
publisher_id
release_sequence
package_sha256
package_length
App Ownership
App Signing Key
Permission truth
Capability truth
API range
Release revocation status
```

Catalog 可以复制这些字段用于显示，但必须引用不可变 Release Record，并在安装前交叉验证。

---

# 2. Catalog Target

Catalog 文件必须作为 Repository Target，由 Targets Metadata 的 Length 和 SHA-256 保护。

推荐类型：

```text
catalog-root.json
catalog-index.json
catalog-app-record.json
catalog-diff.json
asset-descriptor.json
```

Catalog 不需要单独设计另一套根密钥。

其完整性继承 Repository Root → Targets → Target Digest 信任链。

---

# 3. Catalog Root

概念结构：

```json
{
  "type": "baga.catalog-root",
  "format": "0.1",
  "repository_id": "repo1_...",
  "catalog_sequence": 620,
  "generated_at": "...",
  "index": {
    "path": "catalog/sha256/...json",
    "length": 48291,
    "sha256": "..."
  },
  "shards": [],
  "diffs": [],
  "supported_locales": ["en", "zh-CN", "ja"],
  "default_locale": "en"
}
```

Catalog Sequence 只表示目录数据变化，不是 App Release Sequence。

Catalog 文案更新可以增加 Catalog Sequence，而不发布新 IKP。

---

# 4. App Catalog Record

每个 App 应拥有独立、内容寻址的 Catalog Record。

概念结构：

```json
{
  "type": "baga.catalog-app",
  "format": "0.1",
  "repository_id": "repo1_...",
  "app_id": "com.example.reader",
  "publisher_id": "pub1_...",
  "publisher_display_name": "Example Studio",
  "title": {
    "en": "Example Reader",
    "zh-CN": "示例阅读器"
  },
  "summary": {},
  "description": {},
  "category": "reader",
  "tags": ["epub", "offline"],
  "icon": {
    "path": "assets/sha256/...png",
    "length": 10240,
    "sha256": "..."
  },
  "screenshots": [],
  "license": "MIT",
  "source": {
    "url": "...",
    "verified": false
  },
  "privacy": {},
  "support": {},
  "release_channels": {},
  "review_attestations": [],
  "updated_at": "..."
}
```

Catalog Record 必须引用安全 Release Record，而不是自行声明可安装包路径。

---

# 5. 本地化

本地化字段采用 Locale Map：

```json
{
  "en": "A lightweight reader",
  "zh-CN": "轻量阅读器",
  "ja": "軽量リーダー"
}
```

回退顺序：

```text
Exact locale
→ language-only locale
→ repository default locale
→ first available value
```

规则：

- 未提供本地化时不得自动机器翻译并冒充开发者文本；
- Market 生成的机器翻译必须明确标记；
- App 名称翻译不能改变 App Identity；
- 同一 App 不因地区使用不同 App ID；
- 本地化内容必须经过长度和安全过滤。

---

# 6. 描述文本格式

v0.1 支持受限 Markdown 子集：

```text
Paragraph
Heading
Bold / Italic
Ordered / unordered list
Inline code
Safe HTTPS link
```

禁止：

- 任意 HTML；
- Script；
- iframe；
- 自动播放媒体；
- 外部追踪像素；
- CSS 注入；
- Data URL；
- 自动重定向；
- 设备命令链接；
- 未经确认启动外部应用。

Market UI 必须使用安全 Renderer。

---

# 7. 分类

v0.1 顶层分类建议：

```text
reader
library
notes
writing
education
reference
rss-news
productivity
calendar
utilities
accessibility
communication
ai-tools
system-tools
other
```

规则：

- 每个 App 一个 Primary Category；
- 可以有多个 Tags；
- Category 不用于授予 Permission；
- Category 不用于替代 Capability 声明；
- 新 Category 由 Market Catalog Registry 版本化；
- 第三方 Repository 可以扩展显示分类，但应映射到标准顶层分类以便跨仓库搜索。

---

# 8. Publisher 展示

Catalog 应显示：

```text
Publisher display name
Publisher ID short form
Verified domain（如有）
Official Market verification（如有）
Source repository（如有）
Support URL
Security contact
```

“Verified”必须说明验证了什么：

```text
Domain verified
Publisher identity verified
Market review passed
Reproducible build verified
```

不得用一个模糊蓝色勾同时暗示全部信任。

---

# 9. Permission 摘要

Catalog 必须从 Release Record / Manifest 生成 Permission 摘要。

不得由开发者自由输入一段与真实 Permission 不一致的描述。

至少显示：

```text
Network
Read library
Modify library
Read notes
Modify notes
Read user-selected files
Modify user-selected files
Bluetooth
Audio output
Frontlight control
Keep awake
```

对于每个 Release，Permission 可能不同。

Catalog 应显示：

- 当前 Stable Permission；
- 相对用户已安装版本的 Permission Diff；
- 被用户拒绝后 App 是否仍可运行（如声明）。

---

# 10. Capability 与兼容性摘要

Catalog 可以显示：

```text
Requires touch
Optional pen support
Supports physical page keys
Supports color enhancement
Requires network
Works offline
Fast refresh enhanced
```

但真实判断来自 Release Record 与设备 Capability Set。

应用详情必须区分：

```text
Latest overall release
Latest compatible release for this device
Installed release
```

如果最新版本不兼容，用户仍应能看到最新兼容旧版和不兼容原因。

---

# 11. Release Channel 展示

Catalog 可显示：

```text
Stable
Beta
Nightly
```

默认只突出 Stable。

Beta / Nightly 必须显示：

- 稳定性风险；
- 是否自动更新；
- 当前 Release Sequence；
- Permission Diff；
- 返回 Stable 可能触发 Downgrade；
- 数据 Schema 风险。

Channel 不是独立 App 条目，除非产品 UI 有明确原因；它们共享同一 App Identity。

---

# 12. Catalog Index

Catalog Index 用于快速列出 App，而不是存放全部详情。

建议字段：

```json
{
  "app_id": "com.example.reader",
  "publisher_id": "pub1_...",
  "record": {
    "path": "catalog/sha256/...json",
    "length": 3200,
    "sha256": "..."
  },
  "category": "reader",
  "title_sort_key": "example reader",
  "latest_stable_release_sequence": 142,
  "updated_at": "..."
}
```

客户端按需下载单 App Record。

低内存设备不应一次加载所有描述和截图。

---

# 13. 分片

大型 Repository 可以按 App ID Hash 前缀分片：

```text
catalog-00
catalog-01
...
catalog-ff
```

也可以额外提供：

```text
category indexes
recently-updated index
featured index
security-updates index
```

这些索引全部作为普通 Target 验证。

分片规则必须稳定，避免每次更新大量搬移条目。

---

# 14. Catalog Diff

Catalog Diff 减少 Kindle 与低带宽设备下载量。

概念结构：

```json
{
  "type": "baga.catalog-diff",
  "format": "0.1",
  "repository_id": "repo1_...",
  "base_sequence": 619,
  "target_sequence": 620,
  "base_catalog_sha256": "...",
  "target_catalog_sha256": "...",
  "operations": [
    {"op": "upsert", "app_id": "...", "record": {}},
    {"op": "remove", "app_id": "..."}
  ]
}
```

客户端只有在：

- 本地 Sequence 与 Base 一致；
- Base Digest 一致；
- Diff Target Digest 经 Repository 验证；
- 应用 Diff 后完整 Catalog Digest 等于目标值；

时才接受。

失败后必须下载完整 Catalog。

---

# 15. Asset

图标、截图与其他媒体使用内容寻址：

```text
assets/sha256/<digest>.<ext>
```

Asset Descriptor 至少记录：

```text
length
sha256
media_type
width
height
purpose
```

Market 应提供适合墨水屏的 Asset Variant：

```text
monochrome / grayscale icon
low-resolution screenshot
high-resolution screenshot
color original
```

设备根据 Capability 与网络条件选择合适版本。

同一 Digest 不得被替换为另一张图。

---

# 16. E-Paper 目录 UI

Baga Ink Market 在设备端应遵守：

- 分页优先；
- 避免无限连续滚动动画；
- 列表更新使用 Dirty Region；
- 图标优先灰阶可辨识；
- 不依赖颜色表达审核或风险；
- 搜索结果支持物理按键与焦点导航；
- 截图按需下载；
- 不在列表页自动轮播；
- 下载和安装进度低频刷新；
- 在断网时保留上一次已验证 Catalog。

Catalog 过期不应阻止已安装 App 启动。

---

# 17. 搜索

搜索可以有两种实现。

## 17.1 本地搜索

基于已验证 Catalog：

```text
title
summary
publisher
tags
category
```

适合离线与隐私场景。

## 17.2 远程搜索

远程 Search API 可以提供更强排序和模糊搜索。

但结果是 Advisory：

```text
Search result
      │
      ▼
Resolve app_id to signed Catalog / Release Record
      │
      ▼
Verify before install
```

搜索服务器不能直接返回一条未被 Repository Metadata 保护的 IKP URL并要求设备安装。

---

# 18. Search Privacy

Market 应尽量减少搜索查询与设备身份绑定。

原则：

- 不要求硬件序列号；
- 不要求上传完整已安装 App 清单；
- 可以在本地做 Compatibility Filtering；
- 远程搜索可只接收 Locale、标准 Capability Profile 和 Query；
- Analytics 必须独立授权；
- 不把 LifeBook 用户账号作为 Market 搜索必需条件；
- 日志保留期限与用途应公开。

---

# 19. 排序与推荐

推荐与搜索排序属于 Market Product Policy，不是安全协议。

但必须遵守透明原则：

- 付费推广明确标记；
- 广告不能伪装成系统更新；
- 官方 App 不得通过伪造评分占位；
- 排序不能修改 App Identity；
- 推荐不能绕过 Compatibility；
- 被 Security Revoked 的 Release 不得因推荐继续安装；
- 推荐算法不应要求上传用户书籍和笔记正文。

可以提供：

```text
Featured
Popular
Recently updated
Open source
Offline capable
Made for physical keys
Pen optimized
Kindle compatible
Android E-Paper compatible
```

标签必须有可验证来源或明确属于编辑判断。

---

# 20. Review 与安全标签

标准显示标签可包括：

```text
Baga Ink Universal
Baga Ink Market Reviewed
Publisher Domain Verified
Open Source Declared
Reproducible Build Verified
Experimental
Unlisted
Withdrawn
Security Warning
```

每个标签必须引用：

- Review Attestation；
- Compatibility Test；
- Publisher Verification；
- Build Attestation；
- Release Status Record；

之一。

第三方 Repository 不能自行使用官方 Review 标签。

---

# 21. Offline Catalog

Portable Repository Snapshot 可以包含：

```text
Catalog Root
Catalog Index / selected shards
Selected App Records
Icons
Low-resolution screenshots
Release Records
IKP packages
```

离线 Market 可以：

- 浏览；
- 搜索已携带 Catalog；
- 查看 Permission / Compatibility；
- 安装快照内已验证 IKP。

缺失截图不影响安全安装。

---

# 22. 第三方 Repository

第三方 Repository 可以拥有自己的：

```text
Catalog
Category mapping
Featured lists
Review policy
Localization
```

但必须：

- 显示 Repository Identity；
- 不伪造官方审核；
- Catalog Record 引用真实 Publisher Identity；
- Package 仍通过标准 IKP Signature；
- Release 仍不可变；
- App ID 冲突按 Publisher Identity 区分；
- 搜索结果显示来源 Repository。

跨 Repository 聚合 UI 应同时展示：

```text
App name
Publisher
Repository source
Review status
```

---

# 23. Catalog 更新原子性

Catalog 更新流程：

1. 验证新的 Repository Metadata；
2. 获取 Catalog Root；
3. 获取完整 Index 或适用 Diff；
4. 验证 Target Digest；
5. 在 staging 中构建新本地 Catalog；
6. 验证最终 Catalog Digest；
7. 原子切换 Catalog Pointer；
8. 保留旧 Catalog 直到新 Catalog 完整可用。

断电后只能恢复到完整旧版本或完整新版本。

---

# 24. 资源限制

客户端必须限制：

```text
Catalog Root size
Index size
Shard count
App Record size
Locale count
Description length
Tag count
Screenshot count
Asset size
Markdown nesting
Diff operation count
Search result count
```

超大描述或图片不得让低内存设备失去基本 Market 功能。

---

# 25. Catalog 与安装的最终边界

点击“安装”后必须重新解析：

```text
app_id
publisher_id
selected release
release_sequence
package digest
permission diff
capability requirements
release status
```

这些值必须来自安全 Release Record 与 Repository Metadata。

Catalog Cache 中的显示数据不得直接传给 Package Installer 作为已验证安全字段。

---

# 26. 最终原则

> **Catalog 可以被重新设计、重新排序和重新本地化；App Identity、Release Digest、Permission 与 Update Chain 不能因此改变。**
