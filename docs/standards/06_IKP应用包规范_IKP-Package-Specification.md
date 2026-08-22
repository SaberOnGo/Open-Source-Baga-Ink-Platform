# IKP 应用包规范 / IKP Package Specification

> **文档级别：一级平台规范**  
> **状态：Draft v0.4**  
> **日期：2026-08-22**  
> **上位文档：`01_顶层战略与架构_Baga-Ink-Platform-Strategy.md`**  
> **应用规范：`02_应用标准_Baga-Ink-App-Standard.md`**  
> **能力与权限：`04_能力注册表_Baga-Ink-Capability-Registry.md`、`05_权限模型_Baga-Ink-Permission-Model.md`**  
> **身份与签名：`21_发布者身份与应用所有权标准_Baga-Ink-Publisher-Identity-and-App-Ownership-Standard.md`、`22_IKP签名与密钥生命周期标准_Baga-Ink-IKP-Signing-and-Key-Lifecycle-Standard.md`**  
> **发布与更新：`24_应用发布审核与版本政策_Baga-Ink-App-Publishing-Review-and-Version-Policy.md`、`25_应用更新回滚与撤销协议_Baga-Ink-Update-Rollback-and-Revocation-Protocol.md`**

---

## 0. 目的

本文档定义 Baga Ink Universal App 的标准应用包格式：

# **IKP / `.ikp`**

IKP 的目标是提供一种：

- 跨 Kindle 与 Android E-Paper；
- 不绑定 CPU ABI；
- 不绑定 Android APK；
- 不绑定 Kindle Homebrew 目录结构；
- 可签名；
- 可验证；
- 可版本化；
- 易生成、检查和分发；

的统一应用包。

IKP 是 Baga Ink App Standard 的载体，不是 APK、IPK、KUAL Extension 或任意压缩包的改名。

最重要的边界：

> **IKP 只承载应用自身的 Lua 代码、资源、Manifest 和发布者证明。Universal IKP 不携带另一套 Platform Core、Lua 解释器、Device Adapter 或设备私有系统桥。**

---

# 1. 权威边界

本文档负责：

```text
.ikp 文件扩展名
Container
路径规则
目录结构
manifest.json
基础资源限制
Package Validator
Platform 与 IKP 的边界
```

以下内容由专门规范负责：

```text
Publisher Identity / App Ownership       → 21
IKP Publisher Signature / Key Lifecycle  → 22
Repository Metadata / Target Digest      → 23
Release Sequence / Review / Channel      → 24
Stage / Activate / Rollback / Revocation → 25
Client / USB / Offline Transfer          → 26
```

如果本文件与这些专门规范发生冲突，以专门规范为准。

---

# 2. 文件扩展名与 MIME Type

标准扩展名：

```text
.ikp
```

示例：

```text
lifebook.ikp
rss-reader.ikp
notes.ikp
```

`IKP` 是固定格式名称，不要求强行解释成逐字母英文缩写。

建议 MIME Type：

```text
application/vnd.baga.ikp
```

文件扩展名和 MIME Type 只是识别提示，不构成安全验证。

---

# 3. Container

IKP v0.4 使用 **ZIP-compatible container** 作为物理封装。

允许的压缩方式：

```text
STORE
DEFLATE
```

原因：

- 多平台实现成熟；
- 开发工具简单；
- 易调试和检查；
- 不需要为第一阶段发明压缩算法。

但：

> **任何 ZIP 改名都不是合法 IKP。**

Platform 必须校验 Manifest、路径、安全限制、Payload Hash、身份、签名与版本。

---

# 4. 路径规则

IKP 内部路径：

- 必须使用 UTF-8；
- 必须使用 `/` 作为分隔符；
- 必须为相对路径；
- 不得包含 `..` 路径逃逸；
- 不得为绝对路径；
- 不得通过符号链接逃出包根；
- 不得包含重复 Entry；
- 应避免仅大小写不同的重复名称；
- 应使用各目标平台都能稳定处理的名称；
- 路径规范化必须在安全判断前完成。

Validator / Installer 必须防御 Path Traversal 与 Zip Slip。

---

# 5. 标准目录结构

## 5.1 最小开发 IKP

```text
example.ikp
├── manifest.json
└── main.lua
```

只允许用于 Developer Mode 或后续签名工具的输入。

## 5.2 正式签名 IKP

```text
example.ikp
├── manifest.json
├── main.lua
├── src/
│   ├── app.lua
│   └── views/
├── assets/
│   ├── icon.png
│   └── images/
├── locales/
│   ├── en.json
│   └── zh-CN.json
└── signature/
    ├── files.json
    ├── publisher-identity.json
    ├── app-ownership.json
    ├── app-key-delegation.json
    ├── release-statement.json
    └── signatures.json
```

签名目录的精确语义由 `22` 号规范定义。

## 5.3 Entry Point

Manifest 必须指定入口，通常为：

```text
main.lua
```

Entry 必须：

- 位于 IKP Payload 内；
- 不得越过包根；
- 不得指向 `signature/`；
- 不得指向 Native Executable；
- 在执行前完成全部验证。

---

# 6. `manifest.json`

`manifest.json` 必须位于包根目录，并使用 UTF-8 JSON。

最小正式示例：

```json
{
  "ikp_format": "0.4",
  "id": "com.example.reader",
  "name": "Example Reader",
  "version_name": "1.0.0",
  "release_sequence": 1,
  "channel": "stable",
  "entry": "main.lua",
  "baga_api": {
    "min": "0.2",
    "max_exclusive": "1.0"
  },
  "permissions": [],
  "capabilities": {
    "required": [],
    "optional": []
  },
  "data_schema_version": 1,
  "rollback": {
    "mode": "safe",
    "minimum_compatible_schema": 1
  }
}
```

---

# 7. Manifest 必填字段

必须包含：

```text
ikp_format
id
name
version_name
release_sequence
channel
entry
baga_api
permissions
capabilities
data_schema_version
rollback
```

## 7.1 `ikp_format`

声明 IKP Schema Major / Minor。

不支持的 Format Major 必须拒绝。

## 7.2 `id`

稳定 Application ID。

必须与 App Ownership、Release Statement 与 Release Record 一致。

不得因设备、Channel 或 Repository 改变。

## 7.3 `name`

用户可见名称，不构成 App Identity。

## 7.4 `version_name`

人类可读版本，不用于安全排序。

## 7.5 `release_sequence`

单调递增整数；精确规则由 `24` 号规范定义。

## 7.6 `channel`

Release 所属 Channel。

v0.1 标准值：

```text
stable
beta
nightly
```

## 7.7 `entry`

应用 Lua 入口文件。

## 7.8 `baga_api`

声明支持的 Baga Ink API 范围。

Platform 必须在执行应用代码前验证。

## 7.9 `permissions`

权限名称必须来自 `05` 号 Permission Registry。

App 不能在运行时申请 Manifest 未声明的 Permission。

## 7.10 `capabilities`

Capability 名称必须来自 `04` 号 Registry。

缺少 Required Capability 时，Platform 必须报告 Incompatible。

缺少 Optional Capability 时，App 必须可降级运行。

## 7.11 `data_schema_version` 与 `rollback`

用于 staged update、数据迁移和回滚判断；语义由 `25` 号规范定义。

---

# 8. 推荐字段

可以包括：

```json
{
  "description": "A minimal Baga Ink reader",
  "publisher_display_name": "Example Studio",
  "homepage": "https://example.com",
  "license": "MIT",
  "source_repository": "https://example.com/source",
  "icon": "assets/icon.png",
  "locales": ["en", "zh-CN"],
  "category": "reader",
  "support": "https://example.com/support"
}
```

这些字段可以帮助 Catalog 生成，但不能改变应用身份与签名语义。

Market 目录的正式字段由 `28` 号规范定义。

---

# 9. Manifest 与签名内容交叉验证

Platform 必须把 Manifest 与 `signature/release-statement.json` 交叉检查。

至少包括：

```text
app_id
version_name
release_sequence
channel
ikp_format
baga_api
permissions
capabilities
data_schema_version
rollback policy
manifest digest
```

发生不一致必须拒绝。

Manifest 不能通过修改绕过签名 Release Statement。

---

# 10. Universal IKP 内容限制

Universal IKP 不得把设备相关 Native Executable / Library 当作正常应用逻辑。

不得依赖：

```text
.so
ELF executable
APK payload
DEX
JAR used as system escape
Kindle shell executable
vendor-specific binary blob
```

Universal IKP 不得携带：

- 自己的一套 Lua 解释器；
- Kindle 专用 Device Bridge；
- Android 专用 Device Bridge；
- BOOX / iReader 私有接口封装作为应用执行依赖；
- 绕过 `baga.*` API 的系统调用层；
- 针对 CPU ABI 的主业务二进制；
- 另一份 Platform Core；
- Device Adapter。

限制的是执行依赖和设备私有依赖，不是普通静态资源。

Native Extension / Capability Provider 必须使用后续受控规范，不得伪装成 Universal IKP。

---

# 11. 依赖模型

第一阶段 IKP 默认采用应用代码与资源自包含模型。

App 可以：

- 使用 Baga Ink 标准 API；
- 将纯 Lua 第三方库打入自己的包；
- 将自身静态资源打入包。

App 不得：

- 要求用户另外安装随机 Native Library；
- 依赖某设备“碰巧存在”的动态库；
- 依赖其他 App 的私有目录；
- 在不同设备上下载不同私有系统桥。

第一阶段不定义跨 App Shared Dependency Resolver。

---

# 12. Payload 与 `files.json`

Payload 定义为：

> IKP 中除 `signature/` 目录以外的全部文件。

正式 IKP 必须包含 `signature/files.json`。

它必须记录每个 Payload 文件的：

```text
path
length
sha256
```

精确规范化、排序、Hash 与验证规则由 `22` 号规范定义。

Validator 必须拒绝：

- 缺失文件；
- 未声明额外 Payload；
- 重复 Path；
- Length 不一致；
- Hash 不一致；
- Path 逃逸。

---

# 13. Publisher Signature

正式 IKP 必须建立以下证明链：

```text
Publisher Identity
      │
      ▼
App Ownership
      │
      ▼
App Signing Key Delegation
      │
      ▼
IKP Release Signature
      │
      ▼
Payload Files
```

精确 Key ID、Canonical JSON、Threshold、Rotation、Recovery 和 Transfer 规则由 `21`、`22` 号规范定义。

Market 账号、Catalog 文案和 Repository URL 都不能替代该证明链。

---

# 14. Repository Container Digest

通过 Repository 分发时，Repository Metadata 还必须保护整个 `.ikp` 文件的：

```text
length
sha256
```

两层验证用途不同：

```text
Repository Digest
→ 保护分发的精确 Container Bytes

Publisher Signature
→ 保护 App Identity 与逻辑 Payload
```

二者不能互相替代。

---

# 15. Canonical Encoding 与确定性打包

签名 JSON 使用 `22` 号规范定义的 Canonical JSON Profile。

Baga Ink SDK 应支持确定性 IKP 生成：

- 固定 Entry 顺序；
- 固定时间戳策略；
- 固定权限位；
- 固定压缩参数；
- 不写本地绝对路径；
- 不写随机未签名字段。

设备的逻辑 Payload 验证不能假设所有合法打包工具产生完全相同 ZIP Bytes。

---

# 16. 包大小与解压安全

Validator 必须防御：

- Zip Bomb；
- 极端压缩比；
- 超大单文件；
- 超大总解压尺寸；
- 重复 Entry；
- Path Traversal；
- 恶意文件名；
- 过深目录；
- 超大 JSON；
- 超多签名；
- 超多 Payload 文件。

具体上限由 Platform Compatibility Profile 定义，但必须有安全默认值。

---

# 17. 安装前验证顺序

最小顺序：

```text
1. 检查 Container 大小与格式
2. 检查路径安全
3. 读取 Manifest 与 Signature 文件
4. 检查 IKP Format
5. 验证 files.json 与全部 Payload
6. 验证 Publisher Identity Chain
7. 验证 App Ownership
8. 验证 App Signing Key Delegation
9. 验证 IKP Release Signature
10. 交叉检查 Manifest / Release Statement
11. 检查 Release Sequence 与 Revocation
12. 检查 Baga API / Capability / Permission
13. 检查 Data Schema / Rollback Policy
14. 才允许进入 staged install
```

来自 Repository 时，还必须验证 Repository Metadata 与 Container Digest。

任何失败都不得执行 `main.lua`。

---

# 18. 安装、更新与回滚

IKP 的 staged install、原子激活、健康确认、自动回滚、显式 Downgrade、Permission Diff 与 Data Schema Migration 全部由 `25` 号协议定义。

本文件只要求：

- App Package 与 App Data 分离；
- 新版本不覆盖旧版本字节；
- 验证完成前不激活；
- 更新失败不默认删除用户数据；
- 上一已知可用 IKP 可以被保留。

---

# 19. 安装位置

IKP 不得硬编码真实安装路径。

App 只面对：

```text
自身包资源
appdata/
cache/
documents/
downloads/
经授权共享资源
```

Android / Kindle 真实路径由 Platform Core 与 Device Adapter 决定。

---

# 20. IKP 与 Baga Lua Profile

同一个 Universal IKP 不应长期采用：

```text
main-kindle.lua
main-boox.lua
main-ireader.lua
```

作为多套设备实现。

设备差异通过：

```lua
baga.device.has(...)
```

和标准 API 消化。

极少数 Capability 分支可以改变体验，但不能演变成 Vendor 分支。

---

# 21. IKP 与 Platform 的关系

```text
Baga Ink Platform
├── Platform Core
│   ├── Embedded Lua Interpreter
│   ├── Baga Lua Profile
│   ├── Baga Ink API
│   ├── IKP Package Manager
│   └── Device Adapter
│
├── App A.ikp
├── App B.ikp
└── App C.ikp
```

每个 IKP 只提供自身应用代码、资源与发布者证明。

平台能力共享，设备适配属于 Platform，不属于 Universal IKP。

---

# 22. Android、Kindle 与 IKP

Android：

```text
Baga Ink Platform.apk
        │
        ▼
      *.ikp
```

Kindle：

```text
Kindle OS / Homebrew
        │
        ▼
Baga Ink Platform Core
        │
        ▼
      *.ikp
```

第三方 IKP 不需要知道 APK、KUAL、MRPI、Framebuffer 或 Vendor SDK 等底层细节。

---

# 23. Developer Mode

未签名 IKP 只允许 Developer Mode。

规则由 `26` 号 Client / Offline Transfer Protocol 定义。

它不得：

- 覆盖正式签名应用；
- 获得官方 Market 审核标识；
- 参加普通自动更新；
- 长期关闭所有签名验证。

---

# 24. Validator

Baga Ink SDK 应提供：

```text
baga validate app.ikp
baga inspect app.ikp
baga verify app.ikp
```

至少检查：

- Container；
- Manifest Schema；
- Application ID；
- Release Sequence；
- API Version；
- Capability / Permission Naming；
- Unsafe Path；
- Forbidden Executable Dependency；
- 是否私带解释器、系统桥或 Device Adapter；
- Payload Hash；
- Publisher Signature；
- Resource Limits。

---

# 25. LifeBook Reference IKP

LifeBook 应作为第一批 Reference IKP 验证本规范。

目标：

```text
lifebook.ikp
     │
     ├── Kindle
     └── Android E-Paper
```

LifeBook 官方身份不能成为绕过 IKP Standard 的理由。

---

# 26. 第一阶段暂不定义

暂不锁死：

- Shared Dependency Registry；
- Native Extension Package Format；
- Delta Algorithm；
- Paid App Receipt；
- DRM；
- Cloud Backup Format；
- Multi-process App Model。

Delta 的安全边界已由 `25` 号协议规定，但具体差分算法留待实现验证。

---

# 27. 核心原则

```text
一个格式：.ikp
一个 Manifest
一个 App ID
一个全局 Release Sequence 轴
一套 Baga Ink API
一套 Capability / Permission Model
应用代码与资源自包含
设备适配不进入 Universal IKP
设备私有 Executable 不进入 Universal IKP
平台共享能力不在每个 App 中重复携带
Publisher Signature 可独立验证
Repository Container Digest 可独立验证
安装可 staged、可健康确认、可回滚
```

> **同一个 IKP 必须成为 Kindle 与 Android 墨水屏之间稳定、可验证、可长期兼容的软件分发单位。**
