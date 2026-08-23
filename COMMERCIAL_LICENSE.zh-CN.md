# Baga Ink 商业授权入口

Baga Ink 采用公开源码、开放开发和社区协作方式，面向普通用户、个人开发者、研究者、教育机构、社区贡献者、设备移植者和商业设备厂商。

除非具体文件或目录另有声明，Baga 自研 Platform / OEM 侧软件默认采用 **PolyForm Noncommercial License 1.0.0** 作为 Community License。

商业 OEM / Device / Platform 使用需要单独书面商业协议。但“需要 Commercial License”**不等于一定要收 Platform Royalty**：对于真正帮助 Baga Ink 扩大设备生态的合格厂商，可以针对明确范围提供**零费用或优惠的 Platform Commercial License**。

典型 Commercial License 场景包括：

- OEM 在商业设备上预装 Baga Ink Platform；
- 销售 / 出货包含 Baga 自研 Platform / Device Adapter 代码的商业设备；
- 商业再分发 Baga Platform Binary / Source；
- OEM 基于 Baga 自研 Platform / Adapter 代码做 Proprietary Integration；
- 将 Baga 自研 Platform 代码用于收费 Managed Device / Platform Deployment；
- 商业 Compatibility / Certification 合作，以及适用时对受控 Baga 品牌的授权使用。

## OEM Enablement Program

Baga Ink 希望设备厂商有动力主动把自己的阅读器 / 墨水屏设备接入 Baga 生态，而不是“厂商自己出人出钱做完 Adapter，还要再交一笔进入生态的门票费”。

如果设备厂商自行投入资源，完成、测试并持续维护符合要求的 Baga Platform Port / Device Adapter，可以针对双方书面确认的具体 Device Model、Firmware Range、Platform Version、地区或 Distribution Scope，获得 **$0 / 零费用或优惠的 Platform Commercial License**。

是否符合条件，可以综合考虑厂商是否：

- 自行实现并持续维护所需 Device Adapter / Platform Port；
- 为约定设备组合提供可复现的 Compatibility Evidence；
- 通过要求的 Adapter Contract Tests 与适用 BICTS Profile；
- Firmware 变化后持续修复 Regression、维护 Compatibility Record；
- 满足所有适用第三方 License；
- 未经授权不使用 `Baga Ink Compatible` 等受控品牌，也不把未经认证的设备宣传成官方兼容。

零费用 / 优惠 Platform License **不是自动获得**，也不意味着厂商未来所有新设备、所有 Firmware、所有产品线、所有 Baga Release 永久免费。具体授权范围由书面 Commercial Agreement 明确。

## 即使 Platform License 为零费用，哪些仍可收费

即便某个 OEM 获得零费用 Platform Commercial License，下面这些额外价值仍可以独立收费：

- 由 Baga 团队代做 Device Adapter / Platform Port；
- OEM 定制与 Integration；
- Compatibility Investigation、Performance / Refresh / Sleep-Wake Tuning；
- 官方 Certification 与受控 Compatibility Mark 使用；
- 官方 Baga Ink Client Integration 或 Enterprise Device Management；
- 官方 Market / Repository / Hosted Service Integration；
- Support、Maintenance、SLA、White-label、Managed Service。

核心原则是：**不要因为厂商帮助 Baga 扩大设备生态就向他收门票；Baga 应该从额外工程、认证、官方分发、Market、服务和商业价值中获得收入。**

## 普通 App 开发者

仅仅使用公开 Baga App API 开发并销售 IKP App，**本身不需要购买 Baga OEM / Platform Commercial License**。

App-facing SDK、Sample Code、`baga-probe.ikp` 等可以采用独立的宽松许可证；应以具体文件 / 目录声明为准。

## Evaluation / Prototype

商业公司如果希望进行 Evaluation、Prototype、OEM Integration 或 Device Bring-up，应在依赖 Noncommercial Community License 之前与项目联系。Evaluation License 可以单独提供，也可以免费。

## Official Client / Market 边界

官方 **Baga Ink Client**、官方 Market / Repository Service、Signing / Trust Infrastructure、Certification Service、Compatibility Branding、Hosted Service 以及相关商业产品，与公开 Platform Protocol Surface 是不同的资产，可以保持 Proprietary 或由 Baga 强控制。

公开 Distribution Protocol 可以允许第三方实现兼容工具，但实现公开协议并不会自动获得 Official Baga Market、Trust Root、Commercial Account、LifeBook Distribution Rights、Certification 或 Trademark 权利。

## 商业条款

仓库不公开写死商业授权价格。实际条款可以根据 Device Port Contribution、设备出货量、技术支持、定制开发、认证、授权地区、Hosted Service 等因素单独确定。

商业授权可通过项目公开联系渠道，或 GitHub 账号 `SaberOnGo` 联系 Repository Owner / Baga Ink Project Operator。

## 重要边界

Baga Commercial License 只覆盖 Baga Licensor 有权授权的部分，**不能**重新许可 KOReader、koreader-base、FBInk、KPM、KindleTool 等第三方软件。真正发行的 Distribution 必须独立满足全部适用上游 License。

LifeBook 正式产品源码属于 Proprietary 软件，不包含在公共 Baga Ink Platform 源码发行中，除非具体文件明确另行授权。

完整规则参见：

- `docs/zh-CN/governance/02_Baga-Ink授权策略.md`
- `LICENSE_HISTORY.md`
- `THIRD_PARTY_NOTICES.md`

本文只是商业合作入口，不是一份完整 Commercial License Agreement，也不构成法律意见。
