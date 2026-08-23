# Baga Ink 商业授权入口

Baga Ink 采用公开源码、开放开发和社区协作方式，面向普通用户、个人开发者、研究者、教育机构、社区贡献者和设备移植者。

除非具体文件或目录另有声明，Baga 自研 Platform / OEM 侧软件默认采用 **PolyForm Noncommercial License 1.0.0** 作为 Community License。

Community License 未覆盖的商业用途，需要单独取得商业协议。典型场景包括：

- OEM 在商业设备上预装 Baga Ink Platform；
- 销售或出货包含 Baga 自研 Platform / Device Adapter 代码的商业设备或产品；
- 商业再分发 Baga Platform Binary / Source；
- OEM 基于 Baga 自研 Platform / Adapter 代码做 Proprietary Integration；
- 将 Baga 自研 Platform 代码用于收费的 Managed Device / Platform Deployment；
- 商业 Compatibility / Certification 合作，以及适用时对受控 Baga 品牌的授权使用。

## 普通 App 开发者

仅仅使用公开 Baga App API 开发并销售 IKP App，**本身不需要购买 Baga OEM / Platform Commercial License**。

App-facing SDK、Sample Code、`baga-probe.ikp` 等可以采用独立的宽松许可证；应以具体文件 / 目录声明为准。

## Evaluation / Prototype

商业公司如果希望进行 Evaluation、Prototype、OEM Integration 或 Device Bring-up，应在依赖 Noncommercial Community License 之前与项目联系。Evaluation License 可以单独提供，也可以免费。

## 商业条款

仓库不公开写死商业授权价格。实际条款可能根据以下因素单独确定：

```text
设备出货量
技术支持
定制开发
Compatibility / Certification
授权地区
Hosted Services
其他商业需求
```

商业授权可通过项目公开的联系渠道，或 GitHub 账号 `SaberOnGo` 联系 Repository Owner / Baga Ink Project Operator。

## 重要边界

Baga Commercial License 只覆盖 Baga Licensor 有权授权的部分，**不能**重新许可 KOReader、koreader-base、FBInk、KPM、KindleTool 等第三方软件。真正发行的 Distribution 必须独立满足全部适用的上游 License。

LifeBook 正式产品源码属于 Proprietary 软件，不包含在公共 Baga Ink Platform 源码发行中，除非某个具体文件明确另行授权。

完整规则参见：

- `docs/zh-CN/governance/02_Baga-Ink授权策略.md`
- `LICENSE_HISTORY.md`
- `THIRD_PARTY_NOTICES.md`

本文只是商业合作入口，不是一份完整 Commercial License Agreement，也不构成法律意见。
