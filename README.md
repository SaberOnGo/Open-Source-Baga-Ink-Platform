# Baga Ink Platform

Baga Ink is an open platform project for E-Paper devices. Its goal is to let applications target a stable Baga Ink API and Device Adapter Contract while device-specific differences are absorbed by platform ports such as Kindle and Android E-Paper.

The project is currently in the Standards / executable-conformance / first Kindle reference-port stage.

**English documentation:** [`docs/en/00_baga-ink-documentation-index.md`](docs/en/00_baga-ink-documentation-index.md)  
**简体中文文档:** [`docs/zh-CN/00_项目文档入口.md`](docs/zh-CN/00_项目文档入口.md)  
**中文 README:** [`README.zh-CN.md`](README.zh-CN.md)

## Repository model

```text
spec/        machine-readable specifications and vectors
reference/   reference / independent implementations
tests/       conformance and regression tests
docs/en/     English public documentation
docs/zh-CN/  Simplified Chinese public documentation
docs/plans/  engineering implementation plans
```

Public prose is localized, but Baga Ink has one protocol/API/architecture. Machine-readable schemas, API identifiers, code, tests, error codes, and tooling remain language-neutral/English.

Before contributing, read [`AGENTS.md`](AGENTS.md) and the documentation entry for your preferred language.
