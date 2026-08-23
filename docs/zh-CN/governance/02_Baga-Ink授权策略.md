# Baga Ink 授权策略

> **文档级别：项目治理 / Licensing Architecture**  
> **Document ID：`governance.licensing.02`**  
> **语言：简体中文（`zh-CN`）**  
> **状态：Governance Baseline v1.2**  
> **日期：2026-08-23**  
> **对应英文版：`docs/en/governance/02_baga-ink-licensing-policy.md`**

## 0. 目的

Baga Ink 采用公开源码和开放协作方式，面向普通用户、个人开发者、研究者、Device Porter、App Developer 以及商业设备厂商。

项目根据资产性质分别定义授权规则。社区使用、App 开发、商业 Device / Platform 部署、OEM Enablement、第一方 Proprietary 产品、官方 Baga 服务以及第三方上游软件，可以适用不同的 License 与商业条款。

本文是仓库内上述授权边界的正式 Governance Policy，不是一份完整 Commercial Agreement，也不构成法律意见。商业发行与商业协议应结合适用法律以及全部第三方 License 义务进行审核。

## 1. 核心模型

```text
个人 / 社区 / 研究 / 教育 / 非商业
        → 按适用 Community License 使用

普通 Baga IKP App 开发
        → App 授权与 OEM / Platform 授权分离

商业 OEM / Device / Platform 部署
        → 需要书面 Baga Commercial License
        → 符合条件的 OEM Port 可获得零费用或优惠 Platform 条款

官方 Baga Ink Client / Market / Certification / Hosted Services
        → 可以保持 Proprietary 并独立管理商业条款

LifeBook 正式产品 App
        → Proprietary / Closed Source

第三方软件
        → 保持上游 License
```

## 2. 资产分层

| Baga 资产 | 默认策略 | 商业策略 |
|---|---|---|
| Baga Ink Standards / Protocol 正文 | 公开阅读，版权保留，按 Documentation Policy 管理 | 可用于学习规范、Baga App 开发与互操作；商业 Device / Platform 部署和官方 Compatibility Branding 另行治理。 |
| Baga Ink Platform Core | 除非明确覆盖，默认 PolyForm Noncommercial 1.0.0 | 商业 OEM / Device / Platform 使用需要书面 Commercial License；符合条件的 OEM 可在约定范围获得零费用或优惠 Platform 条款。 |
| Baga Device Adapter Reference Implementation | 除非明确覆盖，默认同 Platform Core | 商业集成和出货需要书面条款；自行实现并维护 Conforming Port 的 OEM 可申请 OEM Enablement 条款。 |
| Baga Adapter SDK / Codegen / Conformance Tooling | 具体文件或目录可采用独立 License | OEM 量产、Proprietary Integration、Certification 或 Commercial Redistribution 可适用单独条款。 |
| BICTS / Compatibility | Test Specification 与兼容要求公开；实现代码服从具体 License | 官方 `Baga Ink Compatible` Certification、Mark 与商业认证服务由 Baga Ink 项目管理。 |
| 官方 Baga Ink Client | 默认 Proprietary / Closed Source，除非具体组件明确另行授权 | Device Management、Bootstrap、Distribution、OEM Integration、Enterprise Management 与 Support 可作为商业产品或服务。 |
| 官方 Baga Ink Market / Repository / Hosted Services | 可以部分或全部 Proprietary | 官方 Market、Enterprise Market、Signing / Trust、Hosted Repository、Analytics、Distribution 与 OEM Service 可作为商业产品。 |
| Baga App API / 普通 IKP App SDK | App 开发与 OEM / Platform 授权分离；公开 SDK / Sample Source 应明确具体 License | **开发并销售使用公开 Baga App API 的 IKP App，本身不需要 Baga OEM / Platform Commercial License。** |
| LifeBook 正式 App | Proprietary / Closed Source | 第一方商业产品，不属于公共 Baga Platform 源码发行。 |
| `baga-probe.ikp` / 示例 App | 发布时优先明确 Apache-2.0 等宽松 License | 用于开发、测试、示例和互操作。 |
| KOReader / koreader-base / FBInk / KPM / KindleTool 等第三方代码 | 仅适用上游 License | Baga Community / Commercial License 不重新许可第三方代码。 |

## 3. 默认软件 License

仓库根 `LICENSE` 使用未经修改的 **PolyForm Noncommercial License 1.0.0**。

除非文件或目录明确声明其他 License，License Cutover 后首次发布的 Baga 自研 Platform / OEM 侧软件采用该默认 License。

Baga 自身的资产范围、例外、Commercial Terms、OEM Enablement 与产品策略由项目 Policy 或独立 Agreement 定义。仓库在继续使用 PolyForm Noncommercial 1.0.0 名称时，MUST 保持其标准 License 文本不变。

## 4. 商业使用

Community License 不是 OEM Commercial Deployment License。

通常需要单独书面 Commercial Agreement 的场景包括：

```text
在商业设备上预装 Baga Ink Platform
销售 / 出货包含 Baga 自研 Platform 代码的商业设备
商业再分发 Baga Platform / Device Adapter 实现
使用 Baga 自研 Platform 代码提供收费 Managed Device / Platform Service
OEM 基于 Baga 自研 Platform / Adapter 做 Proprietary Integration
官方商业 Compatibility / Certification 合作
```

即使最终 Platform License Fee 为零，也需要书面 Agreement。Agreement 用于确定 Device / Product Scope、适用版本、第三方 License 义务、Compatibility Evidence、Brand Permission、Support 条款以及其他商业条件。

商业授权入口见 `COMMERCIAL_LICENSE.md`。

## 5. OEM Enablement Program

自行实现并维护合格 Baga Platform Port / Device Adapter 的设备厂商，可以申请零费用或优惠的 Platform Commercial License。

资格条件可以包括：

```text
OEM 实现并持续维护 Device Adapter / Platform Port
要求的 Adapter Contract Tests PASS
适用 BICTS Profile PASS
Compatibility Record 可复现
支持范围内 Firmware Revision 得到持续维护
满足适用的第三方 License 义务
遵守 Baga Trademark / Certification Rules
```

Commercial Agreement 可以限定：

```text
Device Model / SKU
Firmware Range
Baga Platform Version / Version Range
地区
Shipment / Product Family
Distribution Channel
Support Level
Term
```

零费用或优惠条款只适用于书面 Agreement 明确的 Scope，不自动扩展到未来 Device Model、Firmware Revision、Product Family、Service 或 Baga Release。

## 6. 独立商业产品与服务

零费用 Platform License 不包含 Baga 的全部商业产品与服务。

以下项目可以适用独立商业条款：

```text
由 Baga 提供 Device Adapter / Platform Port Engineering
OEM Customization / White-label Integration
Refresh、Power、Sleep/Wake、Performance、Compatibility Engineering
官方 Certification 与 Compatibility Mark Authorization
官方 Baga Ink Client Integration / Enterprise Device Management
官方 Market / Repository / Signing / Trust Integration
Hosted Services
Support / Maintenance / SLA
Managed Deployment
```

## 7. App Developer

App Developer 与 OEM / Platform Licensee 属于不同授权类别。

> **使用公开 Baga App API 开发或销售 IKP App，本身不需要 OEM / Platform Commercial License。**

未来发布 Reusable App SDK Source、Template、`baga-probe.ikp` 和 Example App 时，SHOULD 为对应文件或目录声明明确 License；具体 Local License 对该资产生效。

本规则不授予 Proprietary LifeBook Source、Baga Certification Mark、Trademark 或第三方代码超出其适用 License 的权利。

## 8. Official Client / Market / Service 边界

官方 **Baga Ink Client** 是第一方产品，可以保持 Proprietary。Baga Distribution / Interoperability Protocol 可以独立保持公开，并不要求公开 Official Client 的产品源码。

第三方实现公开 Protocol，并不会自动获得：

```text
Official Baga Ink Market
Official Repository / Signing Infrastructure
Baga Trust Root / Commercial Account
LifeBook Distribution Rights
Baga Ink Compatible Certification
Baga Trademark / Logo
Official Hosted Service / Analytics / Recommendation System
```

官方 Baga Ink Market、Repository、Signing / Trust Infrastructure、Certification Service、Compatibility Branding、Hosted Service、Enterprise Management 等可以适用独立条款。

## 9. Standards / Protocol 边界

Baga Ink Standards 用于 App 开发、互操作、Compatible Implementation 与技术 Review。

Copyright 保护具体创作的文档与 Artifact，但并不单独构成对每一个 Protocol Idea 或 Interface Fact 的独占权。项目还可以通过 Baga 自研 Software License、Trademark、Certification Program、Official Service、适用 Patent Rights 与 Commercial Agreement 管理相关权益。

实现公开 Specification 不等于获得官方 Certification，也不授予受保护 Baga Branding 的使用权。

## 10. Documentation License

`docs/en/` 与 `docs/zh-CN/` 中的 Baga 自研公共正文用于公开阅读与项目协作。Documentation Redistribution Rights 由适用于具体材料的文件或项目 Documentation License 决定。

在商业出版或商业再发行中依赖 Documentation Redistribution Rights 前，应确认对应材料的具体 Notice 与 License。

## 11. LifeBook 边界

LifeBook 是用于验证 Baga Ink Architecture 的旗舰 / Reference Product，但正式 LifeBook Product Application **不属于公共 Baga Platform 源码发行**。

公共仓库可以包含：

```text
LifeBook Reference App Architecture
LifeBook Product Behavior / Design Document
Interoperability Example
Mock / Sample / Probe Application
```

这些材料不代表公开正式 LifeBook Source、Backend Code、Product Algorithm、Account / Community Implementation、AI Product Logic 或 Commercial Assets。

## 12. 第三方依赖边界

任何第三方组件都保持自己的 License。Baga Commercial License 不能替代或免除 GPL、AGPL 或其他上游义务。

每个具体 Distribution 都必须识别实际 Dependency Graph，并满足发布组合适用的全部 License。对于 Proprietary / Commercial Distribution，Strong Copyleft Integration 属于 Release Gate 所需审核事项。

详见 `THIRD_PARTY_NOTICES.md`。

## 13. Apache-2.0 历史 Cutover

已经按 Apache License 2.0 发布的 Baga 自研历史版本继续适用当时已经授予的权利。

```text
最后一个切换前 main commit：
3517970a221dd2e40d8931e1f68399032c343789
```

该 Revision 及之前的历史版本继续受其原始 License 管理。Cutover 之后新增或实质修改的 Baga 自研 Platform / OEM 侧内容，除非文件或目录另有明确声明，适用当前默认 License。

详见 `LICENSE_HISTORY.md`。

## 14. 外部贡献与 Relicensing

Contributor 必须拥有或被授权提交其 Contribution。来源不明或 License 不兼容的第三方代码不得直接进入 Baga 自研文件。

对可能同时进行 Community 与 Commercial Distribution 的 Baga Platform / Adapter 外部 Contribution，merge 前可以要求经过法律审核的 Contributor License Agreement。

如果 Contribution 的 License Terms 与目标 Component 的既定分发模型不兼容，该 Contribution MUST NOT merge。

## 15. Trademark / Compatibility 边界

Software License 与 Documentation License 不自动授予 unrestricted Trademark Rights。

以下名称或 Mark 可以由独立 Trademark / Brand Policy 管理：

```text
Baga Ink
Baga Ink Platform
Baga Ink Market
Baga Ink Compatible
```

第三方实现只有在满足适用 Compatibility / Certification Requirement 并取得相关 Mark 使用许可后，才能使用官方 `Baga Ink Compatible` Claim。

## 16. README Licensing 展示

根 README 是项目概览和 Onboarding 入口。详细 Commercial Licensing Terms 放在 README 后部的 `Licensing` Section 与独立 Licensing 文档中。

README Hero 不展示 Pricing、OEM Commercial License Warning 或 Commercial License Badge。README 中出现的任何 Licensing Statement 都 MUST 与本文保持一致。

## 17. 最终规则

> **Baga Ink 分别治理 Community Use、App Development、OEM Platform Deployment、Official Services、第一方 Proprietary Product 与第三方 Software。OEM 商业条款由书面 Agreement 确定；符合条件的 OEM Port 可以获得零费用或优惠 Platform 条款；LifeBook 保持 Proprietary；第三方软件保持其上游 License。**
