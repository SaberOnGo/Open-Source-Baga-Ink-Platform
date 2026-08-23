# Baga Ink Documentation

Baga Ink maintains public, long-lived documentation in separate locale trees so contributors do not have to parse mixed-language filenames or bilingual prose.

**English:** [`docs/en/00_baga-ink-documentation-index.md`](en/00_baga-ink-documentation-index.md)  
**简体中文:** [`docs/zh-CN/00_项目文档入口.md`](zh-CN/00_项目文档入口.md)

## Documentation model

```text
docs/
├── en/                    # English public documentation
│   ├── standards/
│   ├── design/
│   ├── reference-apps/
│   ├── governance/
│   └── status/
├── zh-CN/                 # Simplified Chinese public documentation
│   ├── standards/
│   ├── design/
│   ├── reference-apps/
│   ├── governance/
│   └── status/
├── plans/                 # engineering work plans; not required to be duplicated by locale
└── localization/          # localization catalog and migration metadata
```

Public Standards, Design, Reference Apps, Governance, and Status documents are maintained as locale editions of the same document identity. A locale is not a separate protocol or architecture.

Machine-readable specifications, schemas, test vectors, reference implementations, tests, API identifiers, error codes, and source code remain language-neutral/English and live outside the localized prose trees.

## Current migration state

The repository was originally authored primarily in Chinese with bilingual filenames under `docs/standards/`, `docs/design/`, `docs/reference-apps/`, `docs/governance/`, and `docs/status/`. Those paths are now a **legacy migration zone**. They are cataloged and may not grow new public documents.

New public documentation must use the locale trees above. Existing documents will be migrated and translated according to `docs/plans/02_文档国际化迁移计划_Documentation-Internationalization-Migration-Plan.md`.

See the documentation internationalization policy:

- English: [`docs/en/governance/01_documentation-internationalization-policy.md`](en/governance/01_documentation-internationalization-policy.md)
- 简体中文: [`docs/zh-CN/governance/01_文档国际化与本地化规范.md`](zh-CN/governance/01_文档国际化与本地化规范.md)
