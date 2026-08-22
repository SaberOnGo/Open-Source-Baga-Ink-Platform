# IKP Package Specification

> **文档级别：一级平台规范**  
> **状态：Draft v0.1**  
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

IKP 是 Baga Ink App Standard 的载体，不是对 APK、IPK、KUAL extension 或任意压缩包的重新命名。

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

IKP v0.1 SHOULD 使用 **ZIP-compatible container** 作为物理封装。

允许的压缩方式：

```text
STORE
DEFLATE
```

选择 ZIP-compatible container 的原因是：

- 各平台实现成熟；
- 开发工具链简单；
- 易检查、调试和生成；
- 不需要为第一阶段发明新的压缩算法。

但是：

> **IKP 的语义由本规范定义，而不是“任何 ZIP 改个扩展名就是 IKP”。**

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

Manifest MUST 指定入口。

通常：

```text
main.lua
```

Entry MUST 位于 IKP 内部且不得越过包根。

## 4.3 `assets/`

用于静态资源。

## 4.4 `locales/`

用于国际化资源，格式由后续 i18n 规范细化。

## 4.5 `signature/`

用于包内容清单与签名。

Unsigned developer package MAY 在本地开发模式缺少该目录；进入 Baga Ink Market 的正式包 SHOULD 使用签名。

---

# 5. Manifest

`manifest.json` MUST 是 UTF-8 JSON。

最小示例：

```json
{
  "ikp_format": "0.1",
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

包格式版本。

```json
"ikp_format": "0.1"
```

Platform MUST 在解包执行任何 App 代码之前检查该字段。

## 6.2 `id`

稳定 Application ID。

```json
"id": "com.example.reader"
```

要求：

- MUST 在应用生命周期内保持稳定；
- MUST 不因设备不同而改变；
- MUST 与同一 Market 中其他应用不冲突。

## 6.3 `name`

用户可见名称。

```json
"name": "Example Reader"
```

## 6.4 `version`

应用版本。

```json
"version": "1.2.0"
```

SHOULD 使用 `MAJOR.MINOR.PATCH`。

## 6.5 `entry`

Lua 入口文件。

```json
"entry": "main.lua"
```

## 6.6 `baga_api`

声明支持的 Baga Ink API 范围。

```json
"baga_api": {
  "min": "0.1",
  "max_exclusive": "1.0"
}
```

Platform MUST 在执行 App 前确认当前 API 版本处于允许范围。

## 6.7 `permissions`

应用可能使用的权限全集。

```json
"permissions": [
  "network",
  "library.read"
]
```

App 运行时不得申请 Manifest 未声明的权限。

## 6.8 `capabilities`

设备能力要求。

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

这些字段不能改变核心安全语义。

---

# 8. Universal App 的内容限制

一个声称为 Baga Ink Universal 的 IKP MUST 不携带设备相关 native executable / library 作为正常应用逻辑。

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

这里的原则不是禁止包里出现任何具有这些扩展名的静态数据，而是：

> Universal App MUST 不把设备相关 native code 当作执行依赖。

Native Extension / Capability Provider 应使用受控、单独审核的扩展机制。

---

# 9. 依赖模型

IKP v0.1 默认采用 **self-contained application package**。

App MAY：

- 使用 Baga Ink 标准 API；
- 将纯 Lua 第三方库打入自己的包；
- 将自身所需静态资源打入包。

App MUST 不要求用户另外安装随机共享 native library 才能运行。

v0.1 不定义跨 App 的共享 dependency resolver。

这样做是为了：

- 防止 dependency hell；
- 提高离线安装可靠性；
- 提高 Kindle 与 Android 跨平台一致性；
- 让单个 IKP 尽可能自描述、自包含。

未来如果生态需要共享 Package Registry，应通过独立规范设计。

---

# 10. 文件完整性清单

正式签名 IKP SHOULD 包含：

```text
signature/files.json
```

`files.json` 列出除 `signature/` 目录自身签名文件之外，需要被保护的包内容。

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

v0.1 推荐使用：

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

`files.json` 又通过 SHA-256 覆盖所有 payload 文件，因此形成：

```text
Ed25519 Signature
        │
        ▼
signature/files.json
        │
        ▼
SHA-256 of every payload file
```

这样避免“签名文件签自己”的循环问题。

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

v0.1 SHOULD 定义一个 canonical JSON profile：

- UTF-8；
- object key 按字典序；
- 无无意义 whitespace；
- 字符串使用标准 JSON escaping；
- 不允许 NaN / Infinity；
- number 表达规则由后续 schema 限定。

第一版实现也可以采用专门 canonical serializer，避免不同语言 JSON serializer 产生不同签名输入。

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

在任何验证失败时，不得执行 `main.lua`。

---

# 14. 原子安装

安装 SHOULD 使用 staged / atomic 模式。

例如：

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

如果需要 key rotation，应采用明确的授权链，例如：

```text
Old trusted key
      │ signs
      ▼
New key authorization
      │
      ▼
Future updates signed by New key
```

如果旧 key 丢失，应由 Market 的 recovery policy 处理，不能简单允许任意新 key 替换旧应用。

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

例如 Kindle 与高性能 Android E-Paper 可以拥有不同资源上限，但这类限制应该由 Platform Compatibility Profile 定义，不应该由 App 猜测设备型号。

---

# 18. 资源与图标

App SHOULD 在 Manifest 中声明 icon：

```json
"icon": "assets/icon.png"
```

图标资源 SHOULD：

- 支持高对比度显示；
- 不依赖颜色表达唯一信息；
- 在单色 Kindle 上仍清晰；
- 避免极细线条和复杂半透明效果。

后续 UI Asset Specification 可定义推荐尺寸和格式。

---

# 19. Locale

国际化资源 SHOULD 放在：

```text
locales/
```

例如：

```text
locales/en.json
locales/zh-CN.json
locales/ja.json
```

App MUST 不因缺失系统 locale 对应翻译而无法启动，应提供默认 locale。

---

# 20. 开发包与正式包

## 20.1 Developer IKP

本地开发模式 MAY：

- unsigned；
- 包含 source map / debug metadata；
- 通过 Baga Ink Client 侧载。

设备 MUST 明确标记 Developer Mode。

## 20.2 Market IKP

进入 Baga Ink Market 的正式包 SHOULD：

- 通过 schema validation；
- 通过 Compatibility Test；
- 有可信签名；
- 权限完整声明；
- 通过安全扫描；
- 不包含 Universal 规则禁止的 native escape。

---

# 21. IKP 与平台的关系

IKP MUST 不包含自己的 Baga Ink Runtime。

这是一个重要原则。

错误方向：

```text
App A.ikp → 自带 Runtime A
App B.ikp → 自带 Runtime B
App C.ikp → 自带不同 Lua VM
```

正确方向：

```text
Baga Ink Platform
       │
       ├── App A.ikp
       ├── App B.ikp
       └── App C.ikp
```

所有 App 共享 Platform 提供的标准 Baga Lua Profile 和 Baga Ink API。

这也是防止 Runtime 版本碎片化的重要机制。

---

# 22. IKP 与 Android APK 的关系

Android E-Paper 上：

```text
Baga Ink Platform.apk
       │
       └── *.ikp
```

普通 Universal App 不需要再制作独立 APK。

APK 是 Android 上承载 Baga Ink Platform 的系统分发形式；IKP 是 Baga Ink 的应用分发形式。

二者职责不同。

---

# 23. IKP 与 Kindle 的关系

Kindle 上：

```text
Kindle OS / Homebrew infrastructure
       │
       ▼
Baga Ink Platform
       │
       └── *.ikp
```

IKP 不应该暴露：

```text
KUAL extension layout
MRPI package layout
Kindle model-specific scripts
```

这些属于 Baga Ink Platform / Kindle Adapter 的安装实现。

---

# 24. IKP v0.1 Schema 建议

完整示例：

```json
{
  "ikp_format": "0.1",
  "id": "com.example.reader",
  "name": "Example Reader",
  "version": "1.0.0",
  "description": "A sample Baga Ink application",
  "entry": "main.lua",
  "icon": "assets/icon.png",
  "publisher": "Example Studio",
  "license": "MIT",
  "baga_api": {
    "min": "0.1",
    "max_exclusive": "1.0"
  },
  "permissions": [
    "network",
    "library.read"
  ],
  "capabilities": {
    "required": [],
    "optional": [
      "input.touch",
      "display.fast_refresh"
    ]
  },
  "locales": [
    "en",
    "zh-CN"
  ]
}
```

---

# 25. CLI 目标

Baga Ink SDK 最终 SHOULD 提供：

```text
baga new
baga validate
baga pack
baga sign
baga inspect
baga install
baga test
baga publish
```

示例：

```bash
baga validate ./my-app
baga pack ./my-app --output my-app.ikp
baga inspect my-app.ikp
```

开发者不应需要手工调用 ZIP 命令才能正确生成正式 IKP。

---

# 26. 可重复构建

IKP tooling SHOULD 支持 reproducible build。

同一 source tree、同一 toolchain version、同一 build configuration SHOULD 能生成相同 payload hashes。

为实现该目标，packer SHOULD：

- 固定文件排序；
- 规范化 metadata；
- 避免把本地绝对路径写入包；
- 避免无意义时间戳影响签名；
- 使用 canonical manifest / files manifest。

---

# 27. Future Reserved Areas

以下能力保留给未来规范，不在 v0.1 直接开放：

- Shared package dependencies；
- Native extension payload；
- Encrypted IKP；
- Delta update；
- Multi-package bundle；
- Paid license receipt；
- Enterprise private distribution；
- Capability Provider packaging；
- Device Adapter packaging。

未来引入这些功能时 MUST 不破坏 v0.1 Universal App 的基本安全和跨设备原则。

---

# 28. IKP 的最终判断标准

IKP 的成功标准不是“能装进去”。

而是：

> **同一个 IKP 文件，在不重新打包、不加入设备私有代码的前提下，可以由不同 Baga Ink Platform 实现在 Kindle 与 Android E-Paper 上安全验证并运行。**

这才是 `.ikp` 存在的真正意义。
