# Baga Ink 文档

Baga Ink 的公共、长期文档采用独立语言目录，避免让中文开发者阅读全英文文档，也避免国际开发者面对“中文 + 英文混合文件名”和中英混排正文。

**English:** [`docs/en/00_baga-ink-documentation-index.md`](en/00_baga-ink-documentation-index.md)  
**简体中文:** [`docs/zh-CN/00_项目文档入口.md`](zh-CN/00_项目文档入口.md)

## 文档结构

```text
docs/
├── en/                    # 英文公共文档
│   ├── standards/
│   ├── design/
│   ├── reference-apps/
│   ├── governance/
│   └── status/
├── zh-CN/                 # 简体中文公共文档
│   ├── standards/
│   ├── design/
│   ├── reference-apps/
│   ├── governance/
│   └── status/
├── plans/                 # 工程施工计划；不要求按语言复制
└── localization/          # 本地化目录、迁移与同步元数据
```

Standards、Design、Reference Apps、Governance、Status 的中英文版本属于**同一个文档身份的不同语言版本**，不是两套协议，也不是两套架构。

机器可读规范、Schema、Test Vector、Reference Implementation、Tests、API 名称、Error Code、代码标识符继续保持语言无关/英文，放在本地化正文目录之外。

## 当前迁移状态

本项目早期主要以中文编写，并在 `docs/standards/`、`docs/design/`、`docs/reference-apps/`、`docs/governance/`、`docs/status/` 使用“中文 + 英文”混合文件名。这些目录现在定义为 **Legacy Migration Zone / 旧文档迁移区**，不再允许继续新增公共文档。

新的公共文档必须进入 `docs/en/` 或 `docs/zh-CN/`。现有文档按照 `docs/plans/02_文档国际化迁移计划_Documentation-Internationalization-Migration-Plan.md` 逐份迁移、校对和建立英文版本。

文档国际化规范：

- English: [`docs/en/governance/01_documentation-internationalization-policy.md`](en/governance/01_documentation-internationalization-policy.md)
- 简体中文: [`docs/zh-CN/governance/01_文档国际化与本地化规范.md`](zh-CN/governance/01_文档国际化与本地化规范.md)
