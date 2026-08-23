# Baga Ink 文档

Baga Ink 的公共、长期文档采用独立 Locale Tree，避免中文开发者面对全英文正文，也避免国际开发者面对中英混合文件名。

**English:** [`docs/en/00_baga-ink-documentation-index.md`](en/00_baga-ink-documentation-index.md)  
**简体中文:** [`docs/zh-CN/00_项目文档入口.md`](zh-CN/00_项目文档入口.md)

## 永久 Documentation Model

```text
docs/
├── en/                    # English Public Documentation
│   ├── standards/
│   ├── design/
│   ├── reference-apps/
│   ├── governance/
│   └── status/
├── zh-CN/                 # 简体中文 Public Documentation
│   ├── standards/
│   ├── design/
│   ├── reference-apps/
│   ├── governance/
│   └── status/
├── plans/                 # Engineering Plans，不强制全文 Locale Mirror
└── localization/          # Catalog / Terminology / README Language Registry
```

Public Standards、Design、Reference Apps、Governance、Status 的中英文版共享同一个 Stable Document Identity。不同 Locale 不是不同 Protocol / Architecture。

早期中英混合 Public Directories 已经删除，并被 CI 永久禁止重新创建。

Machine-readable Specification、Schema、Test Vector、Reference Implementation、Tests、API Identifier、Error Code 和 Source Code 保持 English / Language-neutral，不按语言复制。

## Governance

- 开发治理：[`zh-CN/governance/00_开发治理.md`](zh-CN/governance/00_开发治理.md)
- 文档国际化：[`zh-CN/governance/01_文档国际化与本地化规范.md`](zh-CN/governance/01_文档国际化与本地化规范.md)
- 授权架构：[`zh-CN/governance/02_Baga-Ink授权策略.md`](zh-CN/governance/02_Baga-Ink授权策略.md)

`docs/plans/`，特别是高频 Platform Port Task Design / Execution Prompt，不要求全文翻译；但任何外部实现者长期依赖的 Stable 结论必须提升回 Localized Public Documentation。
