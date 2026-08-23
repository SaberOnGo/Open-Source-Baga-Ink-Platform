# Baga Ink 授权策略

> **文档级别：项目治理 / Licensing Architecture**  
> **Document ID：`governance.licensing.02`**  
> **语言：简体中文（`zh-CN`）**  
> **状态：Governance Baseline v1.1**  
> **日期：2026-08-23**  
> **对应英文版：`docs/en/governance/02_baga-ink-licensing-policy.md`**

## 0. 目的

Baga Ink 采用公开源码、开放开发和社区协作方式，目标用户包括普通用户、个人开发者、研究者、Device Porter、App Developer，以及未来的商业 OEM / 设备厂商。

因此 Baga Ink 明确区分：**社区使用、App 开发生态、商业设备 / Platform 部署、OEM 生态激励、第一方 Proprietary 产品、官方 Baga 服务，以及第三方上游软件**，而不是粗暴地把全部资产套进一张 License。

本文是仓库内授权架构的治理基线，属于工程 / Governance Policy，不构成法律意见。真正进入大规模商业发行前，应对商业协议、第三方依赖和最终分发组合做正式法律审核。

## 1. 核心模型

```text
个人 / 社区 / 研究 / 教育 / 非商业
        → 按适用 Community License 免费使用

普通 Baga IKP App 开发
        → 低门槛；商业 App 不因使用公开 Baga App API 自动产生 OEM / Platform 授权费

商业 OEM / Device / Platform 部署
        → 需要书面 Baga Commercial License
        → 真正帮助扩大设备生态的合格 OEM，可以获得零费用或优惠 Platform 条款

官方 Baga Ink Client / Market / Certification / Hosted Services
        → 可以保持 Proprietary 并由 Baga 强控制

LifeBook 正式产品 App
        → Proprietary / Closed Source

第三方软件
        → 永远保持上游 License
```

README 和普通产品宣传不应把“商业收费”放在第一屏吓退普通用户或个人开发者。首页优先说明 Baga Ink 是什么、解决什么问题、怎样使用和参与；正式 Licensing 页面则必须把真实边界写清楚。

## 2. 资产分层

| Baga 资产 | 默认策略 | 商业策略 |
|---|---|---|
| Baga Ink Standards / Protocol 正文 | 公开阅读，版权保留，按文档策略管理 | 人人可以学习规范、开发 Baga App；商业设备 / Platform 实施和官方兼容品牌另行治理。 |
| Baga Ink Platform Core | 除非文件/目录另有声明，默认 PolyForm Noncommercial 1.0.0 | 商业 OEM / Device / Platform 使用需要书面 Commercial License；合格自研 Port 的 OEM 可获得零费用或优惠 Platform 条款。 |
| Baga Device Adapter Reference Implementation | 默认同 Platform Core | 商业集成 / 出货需要书面条款；自行完成并维护合格 Port 的 OEM 可进入 OEM Enablement。 |
| Baga Adapter SDK / Codegen / Conformance Tooling | 社区开发、测试可访问；具体文件可有独立 License | OEM 量产、闭源集成、商业分发、认证等可单独约定。 |
| BICTS / Compatibility | 测试规范和兼容要求公开；实现代码服从具体 License | `Baga Ink Compatible` 官方认证、品牌和商业认证服务由 Baga Ink 控制。 |
| 官方 Baga Ink Client | 默认 Proprietary / Closed Source，除非某个组件明确另行授权 | Device Management、Bootstrap、Distribution、OEM Integration、Enterprise Management、Support 可作为商业产品/服务。 |
| 官方 Baga Ink Market / Repository / Hosted Services | 可以部分或全部 Proprietary | 官方 Market、企业 Market、Signing / Trust、Hosted Repository、Analytics、Distribution 与 OEM Service 可商业化。 |
| Baga App API / 普通 IKP App SDK | App 开发生态保持低门槛；公开 SDK / Sample 应尽量宽松授权 | **开发并销售只使用公开 Baga App API 的 IKP App，本身不需要购买 Baga OEM / Platform Commercial License。** |
| LifeBook 正式 App | Proprietary / Closed Source | 第一方商业产品，不属于公共 Baga Platform 源码发行内容。 |
| `baga-probe.ikp` / 示例 App | 发布时优先使用 Apache-2.0 等宽松开源许可证 | 用于教学、测试和扩大 App 生态。 |
| KOReader / koreader-base / FBInk / KPM / KindleTool 等 | 只服从上游 License | Baga Community / Commercial License 均不能重新许可第三方代码。 |

## 3. 默认软件 License

仓库根 `LICENSE` 使用**未经修改的 PolyForm Noncommercial License 1.0.0**。

除非文件或目录明确声明其他 License，从授权切换后首次发布的 Baga 自研 Platform / OEM 侧软件默认采用该 License。

不得修改 PolyForm 正文后仍声称它是 PolyForm。Baga 自己的资产范围、例外、商业授权、OEM 激励和产品政策均放在本文或单独协议中，而不是修改 PolyForm 标准文本。

## 4. 商业使用仍然需要书面协议

Community License 不是 OEM Commercial License。

通常需要单独书面商业协议的场景包括：

```text
在商业设备上预装 Baga Ink Platform
销售 / 出货包含 Baga Platform 自研代码的设备或产品
商业分发 Baga Platform / Device Adapter 实现
把 Baga Platform 自研代码用于收费 Managed Device / Platform 服务
OEM 基于 Baga 自研 Platform / Adapter 做 Proprietary Integration
官方商业 Compatibility / Certification 合作
```

即便最后 Platform Commercial Fee 为零，也必须有书面 Agreement，用来明确授权范围、第三方 License、Compatibility Evidence、品牌使用边界以及未来新产品线是否覆盖。

## 5. OEM Enablement Program

Baga Ink 不应该因为一个设备厂商主动帮助扩大生态，就让厂商同时承担“自己做 Adapter 的开发成本 + 再交一笔平台门票费”。

正式策略：

> **合格 OEM 如果自行投入资源，完成、验证并持续维护符合要求的 Baga Platform Port / Device Adapter，可以针对书面约定的明确范围获得零费用或优惠的 Baga Platform Commercial License。**

是否符合条件，可以考虑：

```text
OEM 自行实现并持续维护 Device Adapter / Platform Port
要求的 Adapter Contract Tests PASS
适用 BICTS Profile PASS
Compatibility Record 可复现并持续更新
Firmware Regression 得到维护
第三方 License 义务得到满足
未经授权不使用 Baga Trademark / Certification Claim
```

Agreement 可以限定：

```text
Device Model / SKU
Firmware Range
Baga Platform Version / Range
地区
Shipment / Product Family
Distribution Channel
Support Level
Term
```

零费用 License 不是“未来所有设备、所有 Firmware、所有产品线、所有 Baga Release 永久免费”的自动权利。它的目标是奖励真正有价值的设备移植贡献，同时保留对 Scope 和 Official Services 的控制。

## 6. Platform Royalty 为零时，Baga 仍可以对哪些价值收费

零费用 Platform License 不等于 Baga 的全部商业价值免费。

可以独立收费的产品 / 服务包括：

```text
由 Baga 团队代做 Device Adapter / Platform Port
OEM Customization / White-label Integration
Refresh / Power / Sleep-Wake / Performance / Compatibility Tuning
官方 Certification 与 Compatibility Mark 授权
官方 Baga Ink Client Integration / Enterprise Device Management
官方 Market / Repository / Signing / Trust Integration
Hosted Services
Support / Maintenance / SLA
Managed Deployment
```

公开策略的核心是降低“帮助扩生态的 OEM”的进入成本，而不是把所有官方 Baga 服务都免费送出。

## 7. 普通 App 开发者与 OEM 必须分开

一个开发者写并销售 `weather.ikp`、`calendar.ikp`、`rss-reader.ikp`、`dictionary.ikp`，并不等于他在商业部署 Baga Platform。

> **只使用公开 Baga App API 并生成或销售 IKP App，本身不触发 OEM / Platform Commercial License。**

未来发布 App SDK、Template、`baga-probe.ikp`、Sample App 时，SHOULD 在具体目录或文件中明确使用 Apache-2.0 等宽松许可证；这些局部 License 优先于 Platform 默认 License。

本规则不授权复制 Proprietary LifeBook 源码，也不授予 Baga Certification Mark 或第三方代码超出原许可证的权利。

## 8. Official Client / Market / Control Plane 边界

官方 **Baga Ink Client** 是第一方产品和生态 Control Surface，不意味着 Baga 的 Distribution Protocol 必须闭源。

Baga 可以保持 Official Client Proprietary，同时公开互操作所需要的 Protocol。第三方可以基于公开 Protocol 做 Compatible Tool，但不会因此获得 Official Baga Services 的权利。

实现公开协议并不会自动获得：

```text
Official Baga Ink Market
Official Repository / Signing Infrastructure
Baga Trust Root / Commercial Account
LifeBook Distribution Rights
Baga Ink Compatible Certification
Baga Trademark / Logo
Official Hosted Service / Analytics / Recommendation System
```

这个分层允许开发生态保持开放，同时让官方 Distribution / Service Layer 由 Baga 强控制。

## 9. Standards / Protocol 边界

Baga Ink Standards 公开，是为了让全球开发者理解平台、开发 App、实现互操作。

协议正文 Copyright 不意味着所有 Protocol Idea / Interface Fact 天然成为独占产权。因此商业护城河还应来自 Baga 自研 Software License、Trademark、Certification、Official Services、未来适用 Patent Rights 和 OEM Agreement。

第三方即使阅读或实现规范，也不会因此自动获得“官方 Baga Ink Compatible”认证或品牌使用权。

## 10. 文档 License

`docs/en/` 与 `docs/zh-CN/` 中 Baga 自研公共正文用于公开阅读与社区协作，并采用非商业文档授权方向。

正式用于商业再发行前，应以具体文件声明和法律审核为准。

## 11. LifeBook 正式边界

LifeBook 是旗舰 / Reference Product，但：

> **LifeBook 正式产品源码不属于公共 Baga Ink Platform 源码发行。**

公共仓库可以包含 LifeBook Reference App Architecture、Product Behavior / Design、Interoperability Example、Mock / Sample / Probe App，但并不意味着公开正式 App 源码、Backend、产品算法、账号 / 社区实现、AI 产品逻辑或商业素材。

## 12. 第三方依赖边界

任何第三方组件都保持自己的 License。Baga Ink Commercial License 也**不能**替厂商免除 GPL / AGPL / 其他上游许可证义务。

每个真正发行的 Baga Platform Distribution 都必须审查实际 Dependency Graph。Strong Copyleft 集成问题在商业 / Proprietary Distribution 出货前属于 Release Blocker。

详见 `THIRD_PARTY_NOTICES.md`。

## 13. Apache-2.0 历史 Cutover

以前已经按 Apache License 2.0 对外发布的 Baga 自研内容，其使用者已经获得的权利不能被ย้อนหลัง撤销。

```text
最后一个切换前 main commit：
3517970a221dd2e40d8931e1f68399032c343789
```

该 revision 及之前历史版本继续保留当时获得的 Apache-2.0 权利。Cutover 之后新增或实质修改的 Baga 自研 Platform / OEM 侧内容，除非文件 / 目录另行声明，采用新的默认授权策略。

详见 `LICENSE_HISTORY.md`。

## 14. 外部贡献与未来 Commercial Relicensing

Commercial / Community 双授权要长期成立，项目必须拥有足够权利对外部 Contribution 做 Community 与 Commercial Distribution。

Contributor 必须拥有提交代码的权利；来源不清或不兼容的第三方代码不能直接复制进 Baga 自研文件；针对需要双授权的 Baga Platform / Adapter 外部代码，merge 前可以要求正式 CLA。

不得为了短期接受一个 PR，长期失去项目自身的商业授权能力。

## 15. Trademark / Compatibility

软件 License 和文档 License 不自动授予 Trademark 权利。

`Baga Ink`、`Baga Ink Platform`、`Baga Ink Market`、`Baga Ink Compatible` 等可以由独立 Brand / Trademark Policy 管理。第三方实现不能仅因为“代码能跑”就声称自己获得官方 `Baga Ink Compatible` 认证。

## 16. README 展示规则

为了避免普通用户和个人开发者看到首页就产生“这是个收费平台”的反感：

- README 第一屏不突出 Commercial Pricing / OEM Licensing；
- 不把醒目的 Commercial License Badge 当项目主身份；
- 精确商业边界和 OEM Enablement 放在 README 后部 `Licensing` 与正式 Policy 中；
- 当前 License 未获得 OSI Approval 时，不得虚假宣称获得 OSI Approval。

## 17. 最终原则

> **个人和社区使用要简单；App 开发要简单；真正帮助扩大设备生态的 OEM 不应因为自己做了 Port 就被额外收“门票费”；Baga 可以从官方工程、Certification、Client、Market、Hosted Services、Support 等真实商业价值中获利；LifeBook 保持 Proprietary；第三方代码永远保持原 License。**
