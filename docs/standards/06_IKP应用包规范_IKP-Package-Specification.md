# IKP Package Specification

> **文档级别：一级平台规范**  
> **状态：Draft v0.2**  
> **日期：2026-08-22**  
> **上位文档：`BAGA_INK_PLATFORM_STRATEGY.md`**  
> **配套规范：`BAGA_INK_APP_STANDARD.md`、`BAGA_INK_API_SPECIFICATION.md`**

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
- 易于生成、检查和分发；

的统一应用包。

IKP 是 Baga Ink App Standard 的载体，不是 APK、IPK、KUAL extension 或任意压缩包的改名。

最重要的边界：

> **IKP 只承载应用自身的 Lua 代码、资源、Manifest 和签名信息。Universal IKP 不携带另一套平台核心、Lua 解释器、设备适配层或系统桥。**

---

# 1. 文件扩展名

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

`IKP` 在 Baga Ink 中作为固定格式名称使用，不要求强行解释成逐字母英文缩写。

建议 MIME type：

```text
application/vnd.baga.ikp
```

---

# 2. 容器格式

IKP v0.2 SHOULD 使用 **ZIP-compatible container** 作为物理封装。

允许的压缩方式：

```text
STORE
DEFLATE
```

选择 ZIP-compatible container 的原因：

- 各平台实现成熟；
- 开发工具链简单；
- 易检查、调试和生成；
- 不需要为第一阶段发明新的压缩算法。

但是：

> **IKP 的语义由本规范定义，不是“任何 ZIP 改个扩展名就是 IKP”。**

Platform MUST 校验 Manifest、路径、安全规则、版本与签名。

---

# 3. 文件路径规则

IKP 内部路径：

- MUST 使用 UTF-8；
- MUST 使用 `/` 作为目录分隔符；
- MUST 为相对路径；
- MUST 不包含 `..` 路径逃逸；
- MUST 不包含绝对路径；
- MUST 不通过符号链接逃出包根；
- SHOULD 避免仅大小写不同的重复文件名；
- SHOULD 使用可跨平台稳定处理的文件名。

Installer MUST 防御 path traversal / zip slip。

对于重复 ZIP entry，Validator MUST 拒绝，而不是依赖不同解压库的覆盖顺序。

---

# 4. 标准目录结构

最小 IKP：

```text
example.ikp
├── manifest.json
└── main.lua
```

典型 IKP：

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
    ├── signature.ed25519
    └── publisher.json
```

## 4.1 `manifest.json`

MUST 存在于包根目录。

## 4.2 Entry Point

Manifest MUST 指定入口，通常为：

```text
main.lua
```

Entry MUST 位于 IKP 内部且不得越过包根。

## 4.3 `assets/`

用于静态资源。

## 4.4 `locales/`

用于国际化资源。

## 4.5 `signature/`

用于包内容清单与签名。

Unsigned developer package MAY 在本地开发模式缺少该目录；进入 Baga Ink Market 的正式包 SHOULD 使用签名。

---

# 5. Manifest

`manifest.json` MUST 是 UTF-8 JSON。

最小示例：

```json
{
  "ikp_format": "0.2",
  "id": "com.example.reader",
  "name": "Example Reader",
  "version": "1.0.0",
  "entry": "main.lua",
  "baga_api": {
    "min": "0.1",
    "max_exclusive": "1.0"
  },
  "permissions": [],
  "capabilities": {
    "required": [],
    "optional": []
  }
}
```

---

# 6. Manifest 必填字段

## 6.1 `ikp_format`

包格式版本：

```json
"ikp_format": "0.2"
```

Platform MUST 在执行任何 App 代码之前检查该字段。

## 6.2 `id`

稳定 Application ID：

```json
"id": "com.example.reader"
```

要求：

- MUST 在应用生命周期内保持稳定；
- MUST 不因设备不同而改变；
- MUST 与同一 Market 中其他应用不冲突。

## 6.3 `name`

用户可见名称：

```json
"name": "Example Reader"
```

## 6.4 `version`

应用版本：

```json
"version": "1.2.0"
```

SHOULD 使用 `MAJOR.MINOR.PATCH`。

## 6.5 `entry`

Lua 入口文件：

```json
"entry": "main.lua"
```

## 6.6 `baga_api`

声明支持的 Baga Ink API 范围：

```json
"baga_api": {
  "min": "0.1",
  "max_exclusive": "1.0"
}
```

Platform MUST 在执行 App 前确认当前 API 版本处于允许范围。

## 6.7 `permissions`

应用可能使用的权限全集：

```json
"permissions": [
  "network",
  "library.read"
]
```

App 不得申请 Manifest 未声明的权限。

## 6.8 `capabilities`

设备能力要求：

```json
"capabilities": {
  "required": [
    "input.touch"
  ],
  "optional": [
    "input.pen",
    "display.fast_refresh"
  ]
}
```

缺少 required capability 时，Platform MUST 报告 incompatible。

缺少 optional capability 时，App MUST 可降级运行。

---

# 7. Manifest 推荐字段

后续实现 MAY 使用：

```json
{
  "description": "A minimal Baga Ink reader",
  "publisher": "Example Studio",
  "homepage": "https://example.com",
  "license": "MIT",
  "icon": "assets/icon.png",
  "locales": ["en", "zh-CN"],
  "category": "reader"
}
```

这些字段不得改变核心安全语义。

---

# 8. Universal IKP 的内容限制

一个声称为 Baga Ink Universal 的 IKP MUST 不把设备相关 native executable / library 当作正常应用逻辑。

例如不得依赖：

```text
.so
ELF executable
APK payload
DEX
JAR used as native escape
Kindle shell executable
vendor-specific binary blob
```

更明确地说，Universal IKP MUST 不携带：

- 自己的一套 Lua 解释器；
- Kindle 专用设备桥；
- Android 专用设备桥；
- BOOX / iReader 私有接口封装作为 App 内部执行依赖；
- 绕过 `baga.*` API 的系统调用层；
- 针对 CPU ABI 的主业务二进制。

Universal IKP 中 MAY 包含普通静态数据，即使文件扩展名偶然与上述形式相似；真正限制的是**执行依赖和设备私有依赖**。

Native Extension / Capability Provider 应使用受控、单独审核的扩展机制。

---

# 9. 依赖模型

IKP v0.2 默认采用 **self-contained application package**。

这里的 self-contained 只表示：

> **应用自己的代码与资源应尽量自包含。**

它不表示每个 App 自带另一套平台实现。

App MAY：

- 使用 Baga Ink 标准 API；
- 将纯 Lua 第三方库打入自己的包；
- 将自身所需静态资源打入包。

App MUST 不要求用户另外安装随机共享 native library 才能运行。

v0.2 不定义跨 App 的共享 dependency resolver。

这样做是为了：

- 防止 dependency hell；
- 提高离线安装可靠性；
- 提高 Kindle 与 Android 跨平台一致性；
- 让单个 IKP 尽可能自描述、自包含。

---

# 10. 文件完整性清单

正式签名 IKP SHOULD 包含：

```text
signature/files.json
```

`files.json` 列出除签名文件自身之外需要保护的包内容。

建议结构：

```json
{
  "hash": "sha256",
  "files": [
    {
      "path": "manifest.json",
      "size": 412,
      "sha256": "..."
    },
    {
      "path": "main.lua",
      "size": 1200,
      "sha256": "..."
    }
  ]
}
```

规则：

- 每个 payload file MUST 恰好出现一次；
- path MUST 使用规范化 `/` 路径；
- entries SHOULD 按 path 字节序排序；
- hash MUST 对文件解压后的原始 bytes 计算；
- Validator MUST 验证缺失文件和额外未声明文件。

---

# 11. 数字签名

v0.2 推荐：

```text
SHA-256
+
Ed25519
```

正式包可包含：

```text
signature/files.json
signature/signature.ed25519
signature/publisher.json
```

## 11.1 签名覆盖范围

签名 MUST 覆盖 `signature/files.json` 的规范字节表示。

`files.json` 再通过 SHA-256 覆盖所有 payload 文件：

```text
Ed25519 Signature
        │
        ▼
signature/files.json
        │
        ▼
SHA-256 of every payload file
```

## 11.2 `publisher.json`

可包含：

```json
{
  "key_id": "...",
  "algorithm": "ed25519",
  "public_key": "..."
}
```

Market 发布时 MAY 使用 Market 账户与可信发布者 key registry，而不是完全信任包内自声明 public key。

---

# 12. Manifest 与签名的规范编码

为了获得可重复签名，签名输入必须有唯一字节表示。

v0.2 SHOULD 定义 canonical JSON profile：

- UTF-8；
- object key 按字典序；
- 无无意义 whitespace；
- 字符串使用标准 JSON escaping；
- 不允许 NaN / Infinity；
- number 表达规则由 schema 限定。

---

# 13. 安装验证顺序

Platform / Baga Ink Client 在安装 IKP 时 MUST 先验证，再执行。

推荐顺序：

```text
1. 检查容器是否合法
2. 检查路径安全
3. 读取 manifest.json
4. 检查 IKP format version
5. 检查 Application ID / app version
6. 检查 Baga Ink API compatibility
7. 检查 required capabilities
8. 检查 permissions declaration
9. 检查 package size / resource limits
10. 验证 files.json hashes
11. 验证 publisher signature（正式包）
12. 分配 / 更新 app sandbox
13. 原子安装
14. 允许启动
```

任何验证失败时，不得执行 `main.lua`。

---

# 14. 原子安装

安装 SHOULD 使用 staged / atomic 模式：

```text
下载或读取 IKP
      │
      ▼
临时 staging area
      │
验证通过
      │
      ▼
原子切换为新版本
      │
失败 ─────→ 保留旧版本
```

目标：

> App 更新失败不应让原本可工作的应用消失。

该原则对存量 Kindle 尤其重要。

---

# 15. 更新规则

一个 App 更新 MUST：

- 保持相同 Application ID；
- 使用更高版本号；
- 满足当前 Platform 的 API compatibility；
- 通过签名连续性检查。

Platform SHOULD 保留上一已知可用版本，以便必要时 rollback。

更新不得默认删除用户数据。

---

# 16. Publisher Key 连续性

同一 Application ID 的新版本 SHOULD 使用同一可信发布者 key。

如果需要 key rotation，应采用明确授权链：

```text
Old trusted key
      │ signs
      ▼
New key authorization
      │
      ▼
Future updates signed by New key
```

如果旧 key 丢失，应由 Market recovery policy 处理，不能简单允许任意新 key 替换旧应用。

---

# 17. 包大小与解压安全

IKP Validator MUST 防御：

- zip bomb；
- 极端压缩比；
- 超大单文件；
- 超大总解压尺寸；
- 重复 entry；
- path traversal；
- 恶意文件名；
- 过深目录嵌套。

具体数值限制 MAY 根据设备类别不同。

资源上限属于 Platform Compatibility Profile，不应由 App 猜测设备型号。

---

# 18. 安装位置

IKP 中不得硬编码真实安装路径。

App 只面对：

- 自身包资源；
- `appdata/`；
- `cache/`；
- `documents/`；
- 经授权共享资源。

实际 Android / Kindle 文件路径由 Platform Core 与 Device Adapter 决定。

---

# 19. IKP 与 Baga Lua Profile

IKP 的入口代码使用 Baga Lua Profile。

同一个 IKP 不应因为设备不同而携带：

```text
main-kindle.lua
main-boox.lua
main-ireader.lua
```

作为长期标准开发模式。

设备差异应通过：

```lua
baga.device.has(...)
```

和标准 API 消化。

在极少数情况下，App MAY 对 Capability 做不同体验分支，但不能把品牌判断演化成多套设备版本。

---

# 20. IKP 与 Baga Ink Platform 的关系

正确关系是：

```text
Baga Ink Platform
├── Platform Core
│   ├── Embedded Lua Interpreter
│   ├── Baga Lua Profile
│   ├── Baga Ink API
│   ├── Package Manager
│   └── Device Adapter
│
├── App A.ikp
├── App B.ikp
└── App C.ikp
```

每个 IKP 只提供自己的应用代码和资源。

错误方向是：

```text
App A.ikp → 自带 Lua 解释器 + Kindle bridge
App B.ikp → 自带另一套 Lua 解释器 + Android bridge
App C.ikp → 自带厂商私有接口层
```

如果允许这种模式，设备差异会重新进入 App 包，最终再次形成碎片化。

因此：

> **平台能力共享，应用代码独立；设备适配属于 Platform，不属于 Universal IKP。**

---

# 21. IKP 与 Android APK 的关系

Android 上：

```text
Baga Ink Platform.apk
        │
        ├── Platform Core
        ├── Baga Ink API
        ├── Device Adapter
        └── Embedded Lua Interpreter
        │
        ▼
      *.ikp
```

`.ikp` 不是 APK。

第三方 Universal App 不需要为了 Android 墨水屏再次生成 APK。

---

# 22. IKP 与 Kindle 的关系

Kindle 上：

```text
Kindle OS / Homebrew
        │
        ▼
Baga Ink Platform Core
        │
        ├── Kindle Adapter
        ├── Baga Ink API
        └── 可复用的 Lua 解释器能力
        │
        ▼
      *.ikp
```

Baga Ink SHOULD 尽量复用 KOReader / Homebrew 已有成熟组件，避免重复造轮子。

第三方 IKP 不需要知道 KUAL、MRPI、Framebuffer 等底层细节。

---

# 23. 开发者本地包

开发阶段允许 unsigned IKP：

```text
baga pack --dev
```

Developer Mode MUST 与正式 Market 安装区分。

设备可以要求：

- 用户显式启用 Developer Mode；
- Baga Ink Client 确认；
- 显示 unsigned 警告。

正式 Baga Ink Market 不应把 unsigned developer package 当作普通发布包。

---

# 24. Validator

Baga Ink SDK SHOULD 提供：

```text
baga validate app.ikp
```

Validator SHOULD 检查：

- ZIP/container；
- Manifest schema；
- Application ID；
- API version；
- capability naming；
- permission naming；
- unsafe paths；
- forbidden executable dependency；
- 包内是否私带 Lua 解释器或设备桥；
- hash；
- signature；
- resource limits。

这使大量兼容问题在发布前被发现。

---

# 25. LifeBook 的 IKP

LifeBook 应作为第一批 Reference IKP 验证本规范。

目标：

```text
lifebook.ikp
     │
     ├── Kindle
     └── Android E-Paper
```

同一个 LifeBook IKP 应尽量不含设备私有业务分支。

LifeBook 官方身份不能成为绕过 IKP Standard 的理由。

LifeBook 本身直接使用 Baga Ink Platform 已有 API 与共享组件，不携带另一套通用中间系统。

---

# 26. v0.2 明确不定义的内容

以下暂不锁死：

- shared dependency registry；
- native extension package format；
- delta update format；
- paid app receipt；
- DRM；
- cloud backup format；
- Market server protocol；
- multi-process app model。

这些应在真实实现需要出现后，以独立规范增加。

---

# 27. 核心原则摘要

IKP v0.2 必须守住以下边界：

```text
一个格式：.ikp
一个 Manifest
一个 Application ID
一套 Baga Ink API
一套 Capability Model
应用代码与资源自包含
设备适配不进入 Universal App
设备私有 executable 不进入 Universal App
平台核心不在每个 App 中重复携带
签名可验证
安装可回滚
```

IKP 的价值不在扩展名本身，而在于：

> **让同一个应用包真正成为 Kindle 与 Android 墨水屏之间稳定、可验证、可长期兼容的软件分发单位。**
