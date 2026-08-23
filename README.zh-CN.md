# Baga Ink Platform

Baga Ink 是一个面向墨水屏 / E-Paper 设备的开放平台项目。目标是让应用只面对稳定的 Baga Ink API 与 Device Adapter Contract，而 Kindle、Android E-Paper 等设备/系统差异由各自 Platform Port 吸收。

项目当前处于 Standards、可执行 Conformance、首个 Kindle Reference Port 的建设阶段。

**简体中文文档：** [`docs/zh-CN/00_项目文档入口.md`](docs/zh-CN/00_项目文档入口.md)  
**English documentation:** [`docs/en/00_baga-ink-documentation-index.md`](docs/en/00_baga-ink-documentation-index.md)  
**English README:** [`README.md`](README.md)

## 仓库结构

```text
spec/        机器可读规范与 Test Vector
reference/   Reference / Independent Implementation
tests/       Conformance 与 Regression Tests
docs/en/     英文公共文档
docs/zh-CN/  简体中文公共文档
docs/plans/  工程实施计划
```

公共正文按语言维护，但 Baga Ink 只有一套协议、API 和架构。机器 Schema、API Identifier、代码、测试、Error Code 与工具保持语言无关/英文。

参与开发前，请先阅读 [`AGENTS.md`](AGENTS.md)，然后选择自己熟悉的文档语言入口。
