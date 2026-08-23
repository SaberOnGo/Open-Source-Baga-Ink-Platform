# Baga Ink 商业授权入口

Baga Ink 采用公开源码和开放协作方式，面向普通用户、个人开发者、研究者、教育机构、社区贡献者、设备移植者和商业设备厂商。

除非具体文件或目录另有声明，Baga 自研 Platform / OEM 侧软件默认采用 **PolyForm Noncommercial License 1.0.0** 作为 Community License。

商业 OEM / Device / Platform 使用由单独的书面 Commercial Agreement 管理。根据适用的 OEM Enablement 条款，针对明确 Device / Product Scope 的 Platform License Fee 可以为零或采用优惠条款。

典型 Commercial License 场景包括：

- OEM 在商业设备上预装 Baga Ink Platform；
- 销售 / 出货包含 Baga 自研 Platform / Device Adapter 代码的商业设备；
- 商业再分发 Baga Platform Binary / Source；
- OEM 基于 Baga 自研 Platform / Adapter 代码做 Proprietary Integration；
- 将 Baga 自研 Platform 代码用于收费 Managed Device / Platform Deployment；
- 商业 Compatibility / Certification 合作，以及适用时对受控 Baga Mark 的授权使用。

## OEM Enablement Program

自行投入资源实现、验证并持续维护 Conforming Baga Platform Port / Device Adapter 的设备厂商，可以针对书面约定的 Scope 申请**零费用或优惠的 Platform Commercial License**。

资格条件可以包括：

- 实现并持续维护所需 Device Adapter / Platform Port；
- 为约定设备组合提供可复现 Compatibility Evidence；
- 通过要求的 Adapter Contract Tests 与适用 BICTS Profile；
- 在支持范围内持续维护 Firmware Compatibility；
- 满足全部适用第三方 License；
- 遵守 Baga Trademark 与 Certification Rules。

书面 Agreement 用于明确授权范围，可以包括 Device Model、Firmware Range、Platform Version、地区、Product Family、Distribution Channel、Support Terms 与 Term。

零费用或优惠条款只适用于 Agreement 明确的 Scope，不自动扩展到未来 Device、Firmware Revision、Product Line、Service 或 Baga Release。

## 独立商业产品与服务

即使 Platform License Fee 为零，以下产品与服务仍可以适用独立 Commercial Terms：

- 由 Baga 提供 Device Adapter / Platform Port Engineering；
- OEM Customization 与 White-label Integration；
- Compatibility Investigation、Performance / Refresh / Sleep-Wake Tuning；
- 官方 Certification 与 Compatibility Mark Authorization；
- 官方 Baga Ink Client Integration 或 Enterprise Device Management；
- 官方 Market / Repository / Hosted Service Integration；
- Support、Maintenance、SLA 与 Managed Service。

## App Developer

使用公开 Baga App API 开发并销售 IKP App，**本身不需要 Baga OEM / Platform Commercial License**。

App-facing SDK Source、Template、Sample Code 与 Example App 可以采用独立的宽松 License；对应文件或目录中的 License Notice 对这些资产生效。

## Evaluation / Prototype

Commercial Evaluation、Prototype、OEM Integration 或 Device Bring-up 可以使用单独的 Evaluation Terms。Evaluation Terms 可以不收取 License Fee。

## Official Client / Market 边界

官方 **Baga Ink Client**、官方 Market / Repository Service、Signing / Trust Infrastructure、Certification Service、Compatibility Branding、Hosted Service 以及相关第一方产品，可以保持 Proprietary 或适用独立商业条款。

公开 Distribution / Interoperability Protocol 可以允许第三方实现 Compatible Tool。实现公开 Protocol 不会自动获得 Official Baga Service、Trust Root、Commercial Account、LifeBook Distribution Rights、Certification、Trademark 或 Proprietary Service Implementation 的使用权。

## 商业条款

仓库不固定公开 Commercial Pricing。实际条款可以根据 Licensed Scope、Device Port Contribution、设备出货量、Support、Customization、Certification、Territory、Hosted Service 等因素确定。

商业授权可通过项目公开联系渠道，或 GitHub 账号 `SaberOnGo` 联系 Repository Owner / Baga Ink Project Operator。

## 重要边界

Baga Commercial License 只覆盖 Baga Licensor 有权授权的部分，**不能**重新许可 KOReader、koreader-base、FBInk、KPM、KindleTool 等第三方软件。具体 Distribution 必须独立满足全部适用上游 License。

LifeBook 正式产品源码属于 Proprietary 软件，不包含在公共 Baga Ink Platform 源码发行中，除非具体文件明确另行授权。

完整规则参见：

- `docs/zh-CN/governance/02_Baga-Ink授权策略.md`
- `LICENSE_HISTORY.md`
- `THIRD_PARTY_NOTICES.md`

本文是 Commercial Licensing 信息入口，不是一份完整 Commercial License Agreement，也不构成法律意见。
