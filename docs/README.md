# Baga Ink Documentation

Baga Ink maintains public, long-lived documentation in separate locale trees so contributors do not have to parse mixed-language filenames or bilingual prose.

**English:** [`docs/en/00_baga-ink-documentation-index.md`](en/00_baga-ink-documentation-index.md)  
**简体中文:** [`docs/zh-CN/00_项目文档入口.md`](zh-CN/00_项目文档入口.md)

## Permanent documentation model

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
├── plans/                 # engineering work plans; not fully duplicated by locale
└── localization/          # locale catalog, terminology, README-language registry
```

Public Standards, Design, Reference Apps, Governance, and Status documents are locale editions of the same stable document identity. A locale is not a separate protocol or architecture.

The historical mixed-language public directories have been removed and are forbidden by CI.

Machine-readable specifications, schemas, test vectors, reference implementations, tests, API identifiers, error codes, and source code remain language-neutral/English and live outside the localized prose trees.

## Governance

- Development governance: [`en/governance/00_baga-ink-development-governance.md`](en/governance/00_baga-ink-development-governance.md)
- Documentation localization policy: [`en/governance/01_documentation-internationalization-policy.md`](en/governance/01_documentation-internationalization-policy.md)
- Licensing architecture: [`en/governance/02_baga-ink-licensing-policy.md`](en/governance/02_baga-ink-licensing-policy.md)

Engineering plans under `docs/plans/`, especially high-volume Platform Port Task Designs / Execution Prompts, are not required to be fully translated. Stable external-facing decisions must be promoted into localized public documentation.
