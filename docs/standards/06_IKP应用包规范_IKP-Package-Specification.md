# IKP 应用包规范 / IKP Package Specification

> **文档级别：一级平台规范**  
> **状态：Draft v0.3**  
> **日期：2026-08-22**  
> **上位文档：`01_顶层战略与架构_Baga-Ink-Platform-Strategy.md`**  
> **配套规范：`02_应用标准_Baga-Ink-App-Standard.md`、`03_API规范_Baga-Ink-API-Specification.md`、`04_能力注册表_Baga-Ink-Capability-Registry.md`、`05_权限模型_Baga-Ink-Permission-Model.md`**

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

IKP v0.3 SHOULD 使用 **ZIP-compatible container** 作为物理封装。

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

`manifest.json` MUST 位于包根目录。Entry MUST 位于 IKP 内部且不得越过包根。

---

# 5. Manifest

最小示例：

```json
{
  "ikp_format": "0.3",
  "id": "com.example.reader",
  "name": "Example Reader",
  "version": "1.0.0",
  "entry": "main.lua",
  "baga_api": {
    "min": "0.2",
    "max_exclusive": "1.0"
  },
  "permissions": [],
  "capabilities": {
    "required": [],
    "optional": []
  }
}
```

Capability 名称 MUST 来自 `04_能力注册表_Baga-Ink-Capability-Registry.md`；Permission 名称 MUST 来自 `05_权限模型_Baga-Ink-Permission-Model.md`。

---

# 6. Manifest 必填字段

必须包含：

```text
ikp_format
id
name
version
entry
baga_api
permissions
capabilities
```

Application ID MUST 稳定且不因设备不同而改变。

缺少 required capability 时，Platform MUST 报告 incompatible。

缺少 optional capability 时，App MUST 可降级运行。

---

# 7. 推荐字段

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

---

# 8. Universal IKP 内容限制

Universal IKP MUST 不把设备相关 native executable / library 当作正常应用逻辑。

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

限制的是**执行依赖和设备私有依赖**，不是普通静态资源。

---

# 9. 依赖模型

IKP 默认采用 self-contained application package。

这里的 self-contained 只表示：

> **应用自己的代码与资源尽量自包含。**

App MAY：

- 使用 Baga Ink 标准 API；
- 将纯 Lua 第三方库打入自己的包；
- 将自身所需静态资源打入包。

App MUST 不要求用户另外安装随机共享 native library 才能运行。

第一阶段不定义跨 App shared dependency resolver。

---

# 10. 文件完整性清单

正式签名 IKP SHOULD 包含：

```text
signature/files.json
```

建议使用 SHA-256 对 payload 文件计算摘要。

Validator MUST 验证：

- 缺失文件；
- 未声明额外文件；
- 重复路径；
- 文件大小；
- 哈希一致性。

---

# 11. 数字签名

v0.3 推荐：

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

签名 MUST 覆盖内容清单的规范字节表示。

Market 发布时 MAY 使用 Market 账户与可信发布者 key registry，而不是完全信任包内自声明 public key。

---

# 12. Canonical Encoding

为了获得可重复签名，签名输入必须有唯一字节表示。

SHOULD 使用 canonical JSON profile：

- UTF-8；
- object key 按字典序；
- 无无意义 whitespace；
- 标准 JSON escaping；
- 不允许 NaN / Infinity。

---

# 13. 安装验证顺序

推荐：

```text
1. 检查容器
2. 检查路径安全
3. 读取 manifest.json
4. 检查 IKP format version
5. 检查 Application ID / app version
6. 检查 Baga Ink API compatibility
7. 检查 required capabilities
8. 检查 permissions declaration
9. 检查 package size / resource limits
10. 验证 files.json hashes
11. 验证 publisher signature
12. 分配 / 更新 app sandbox
13. 原子安装
14. 允许启动
```

任何验证失败时，不得执行 `main.lua`。

---

# 14. 原子安装与回滚

安装 SHOULD 使用 staged / atomic 模式。

更新失败必须尽量保留上一可用版本。

更新不得默认删除用户数据。

---

# 15. Publisher Key 连续性

同一 Application ID 的新版本 SHOULD 保持可信发布者 key 连续性。

Key rotation 需要明确授权链或 Market recovery policy。

---

# 16. 包大小与解压安全

Validator MUST 防御：

- zip bomb；
- 极端压缩比；
- 超大单文件；
- 超大总解压尺寸；
- 重复 entry；
- path traversal；
- 恶意文件名；
- 过深目录嵌套。

资源上限属于 Platform Compatibility Profile，不应由 App 猜测设备型号。

---

# 17. 安装位置

IKP 中不得硬编码真实安装路径。

App 只面对逻辑资源与沙箱路径。

实际 Android / Kindle 文件路径由 Platform Core 与 Device Adapter 决定。

---

# 18. IKP 与 Baga Lua Profile

同一个 IKP 不应以以下模式长期维护：

```text
main-kindle.lua
main-boox.lua
main-ireader.lua
```

设备差异应通过 Capability Model 和标准 API 消化。

---

# 19. IKP 与 Platform 的关系

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

平台能力共享，设备适配属于 Platform，不属于 Universal IKP。

---

# 20. Android APK 与 IKP

Android 上：

```text
Baga Ink Platform.apk
        │
        ▼
      *.ikp
```

第三方 Universal App 不需要为了 Android 墨水屏再次生成 APK。

---

# 21. Kindle 与 IKP

Kindle 上：

```text
Kindle OS / Homebrew
        │
        ▼
Baga Ink Platform Core
        │
        ▼
      *.ikp
```

第三方 IKP 不需要知道 KUAL、MRPI、Framebuffer 等底层细节。

---

# 22. Developer Mode

开发阶段 MAY 允许 unsigned IKP，但 Developer Mode MUST 与正式 Market 安装清晰区分。

设备可以要求用户显式启用开发者模式或通过 Baga Ink Client 确认。

---

# 23. Validator

Baga Ink SDK SHOULD 提供：

```text
baga validate app.ikp
```

Validator SHOULD 检查：

- 容器；
- Manifest schema；
- Application ID；
- API version；
- Capability / Permission naming；
- unsafe paths；
- forbidden executable dependency；
- 是否私带 Lua 解释器或设备桥；
- hash；
- signature；
- resource limits。

---

# 24. LifeBook Reference IKP

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

# 25. 暂不定义

第一阶段暂不锁死：

- shared dependency registry；
- native extension package format；
- delta update format；
- paid app receipt；
- DRM；
- cloud backup format；
- Market server protocol；
- multi-process app model。

---

# 26. 核心原则

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
