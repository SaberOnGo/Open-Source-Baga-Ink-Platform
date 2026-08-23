# Baga Ink 授权策略

> **文档级别：项目治理 / Licensing Architecture**  
> **Document ID：`governance.licensing.02`**  
> **语言：简体中文（`zh-CN`）**  
> **状态：Governance Baseline v1.0**  
> **日期：2026-08-23**  
> **对应英文版：`docs/en/governance/02_baga-ink-licensing-policy.md`**

## 0. 目的

Baga Ink 采用公开源码、开放开发和社区协作方式，目标用户不仅包括普通用户、个人开发者、研究者和设备移植者，也包括未来的商业 OEM / 设备厂商。

因此，Baga Ink 不把所有资产粗暴套进一张 License，而是明确区分：

```text
社区 / 个人使用
App 开发生态
商业设备 / Platform 部署
第一方商业产品
第三方开源组件
```

本文档是仓库内授权架构的治理基线。它属于工程 / 治理规则，不构成法律意见。真正进入大规模商业发行前，应对商业协议、第三方依赖和最终分发组合做正式法律审核。

## 1. 核心模型

```text
个人 / 社区 / 研究 / 教育 / 非商业
        → 按适用 Community License 免费使用

普通 Baga IKP App 开发
        → 低门槛；商业 App 不因使用 Baga App API 自动产生 OEM/Platform 授权费

商业 OEM / 设备 / Platform 部署
        → 需要单独取得 Baga Ink Commercial License

LifeBook 正式产品 App
        → Proprietary / Closed Source

第三方软件
        → 永远保持上游许可证
```

README 和普通产品宣传不应把“商业收费”放在第一屏吓退普通用户或个人开发者。首页应优先说明 Baga Ink 是什么、解决什么问题、怎样使用和参与；正式 Licensing 页面则必须把真实边界写清楚。

## 2. 资产分层

| Baga 资产 | 默认策略 | 商业策略 |
|---|---|---|
| Baga Ink Standards / Protocol 正文 | 公开阅读，版权保留，按文档策略管理 | 人人可以学习规范、开发 Baga App；商业设备 / Platform 实施和官方兼容品牌另行治理。 |
| Baga Ink Platform Core | 除非文件/目录另有声明，默认 PolyForm Noncommercial 1.0.0 | 个人、研究、教育及其他非商业用途免费；OEM / 商业设备 / Platform 使用需要商业授权。 |
| Baga Device Adapter Reference Implementation | 默认同 Platform Core | 商业设备集成、量产或出货需要商业授权，除非具体代码有明确宽松许可证。 |
| Baga Adapter SDK / Codegen / Conformance Tooling | 社区开发、测试可访问；具体文件可有独立 License | OEM 量产、商业分发、认证服务、闭源集成等可要求商业授权。 |
| BICTS / Compatibility | 测试规范和兼容要求公开；实现代码服从具体 License | `Baga Ink Compatible` 官方认证、品牌和商业认证服务由 Baga Ink 控制。 |
| Baga Ink Client | 可以同时包含公开源码和 Proprietary 组件 | OEM 定制、批量部署、Enterprise Tooling、商业发行可另行收费。 |
| Baga Ink Market Server / Services | 可以部分或全部 Proprietary | 官方 Market、企业 Market、Hosted Service、OEM Service 可成为商业产品。 |
| Baga App API / 普通 IKP App SDK | App 开发生态保持低门槛；公开 SDK / Sample 应尽量使用宽松 License | **开发并销售 IKP App，本身不需要购买 Baga OEM / Platform Commercial License。** |
| LifeBook 正式 App | Proprietary / Closed Source | 第一方商业产品，不属于公共 Baga Platform 源码发行内容。 |
| `baga-probe.ikp` / 示例 App | 发布时优先使用 Apache-2.0 等宽松开源许可证 | 用于教学、测试和扩大 App 生态。 |
| KOReader / koreader-base / FBInk / KPM / KindleTool 等 | 只服从上游 License | Baga Community / Commercial License 均不能重新许可第三方代码。 |

## 3. 默认软件 License

仓库根 `LICENSE` 使用**未经修改的 PolyForm Noncommercial License 1.0.0**。

除非文件或目录明确声明其他 License，从授权切换后首次发布的 Baga 自研 Platform / OEM 侧软件默认采用该 License。

不得修改 PolyForm 正文后仍声称它是 PolyForm。Baga 自己的资产范围、例外、商业授权、产品政策均放在本文或单独协议中，而不是篡改 PolyForm 标准文本。

## 4. 哪些商业行为需要单独授权

Community License 不是 OEM Commercial License。

通常需要单独书面商业协议的场景包括：

```text
在商业设备上预装 Baga Ink Platform
销售 / 出货包含 Baga Platform 自研代码的设备或产品
商业分发 Baga Platform / Device Adapter 实现
把 Baga Platform 自研代码用于收费的 Managed Device / Platform 服务
OEM 基于 Baga 自研 Platform / Adapter 做 Proprietary Integration
官方商业 Compatibility / Certification 合作
```

商业公司如果只是 Evaluation / Prototype，可由项目另行提供 Evaluation License，甚至可以免费，但不能默认认为“未来准备商业化”的使用已经被 Noncommercial License 自动覆盖。

商业授权入口见 `COMMERCIAL_LICENSE.md`。仓库不公开写死授权价格，因为实际商业条款可能取决于：

```text
设备出货量
授权范围
定制开发
认证
技术支持
地区
Market / Hosted Service
```

## 5. 普通 App 开发者与 OEM 必须分开

一个开发者写了：

```text
weather.ikp
calendar.ikp
rss-reader.ikp
dictionary.ikp
```

并收费销售，并不等于他在商业部署 Baga Platform。

项目政策明确：

> **只使用公开 Baga App API 并生成 IKP App，本身不触发 OEM / Platform Commercial License。**

这条边界是 Baga Ink App 生态能够增长的前提。

未来发布 App SDK、Template、`baga-probe.ikp`、Sample App 时，SHOULD 在具体目录或文件中明确使用 Apache-2.0 等宽松许可证；这些局部许可证优先于 Platform 默认 License。

本规则不授权复制 Proprietary LifeBook 源码，也不授予 Baga 商标、认证标志或第三方代码超出原许可证的权利。

## 6. Standards / Protocol 的边界

Baga Ink Standards 公开，是为了让全球开发者理解平台、开发 App、实现互操作。

但必须现实地区分：

> **协议正文的 Copyright，并不意味着协议思想、接口事实本身天然成为独占权。**

因此 Baga 的商业护城河不能只依赖“协议是我们写的”，还应建立：

```text
Baga 自研 Platform / Adapter Software License
Baga Ink / Baga Ink Platform 等 Trademark
`Baga Ink Compatible` Compatibility / Certification
未来适用的 Patent Rights
Official Market / Services / Support / OEM Agreements
```

第三方即使阅读或实现了规范，也不会因此自动获得“官方 Baga Ink Compatible”认证或品牌使用权。

## 7. 文档 License

`docs/en/` 与 `docs/zh-CN/` 中 Baga 自研公共正文用于公开阅读与社区协作，并采用非商业文档授权方向。

在正式把某份文档用于商业再发行前，应以具体文件声明和正式法律审核为准。本文不把面向软件的 PolyForm 文本假装成一份完整的文档授权协议。

## 8. LifeBook 的正式边界

LifeBook 是 Baga Ink 的旗舰 / Reference Product，用来验证 Baga Ink 能否承载一个真实大型 App。

但是：

> **LifeBook 正式产品源码不属于公共 Baga Ink Platform 源码发行。**

公共仓库可以包含：

```text
LifeBook Reference App Architecture
LifeBook Product Behavior / Design
Interoperability Example
Mock / Sample / Probe App
```

这并不意味着要公开：

```text
LifeBook 正式 App 源码
后台服务器实现
账号 / 社区业务实现
推荐与产品算法
AI 产品逻辑
商业素材
```

未来如果某个 LifeBook 相关文件确实要公开，则必须对该文件单独声明 License。

## 9. 第三方依赖边界

任何第三方组件都保持自己的 License。

Baga Ink Commercial License 也**不能**替厂商免除 GPL / AGPL / 其他上游许可证义务。

每一个真正发布的 Baga Platform Distribution，都必须对实际 Dependency Graph 做许可证审查。特别是 Strong Copyleft 集成问题，在商业 / Proprietary Distribution 出货前属于 Release Blocker。

详见 `THIRD_PARTY_NOTICES.md`。

## 10. Apache-2.0 历史 Cutover

以前已经按 Apache License 2.0 对外发布的 Baga 自研内容，其使用者已经获得的权利不能被ย้อนหลัง撤销。

License Cutover 的历史基准：

```text
最后一个切换前 main commit：
3517970a221dd2e40d8931e1f68399032c343789
```

该 revision 及之前已经发布的历史版本，继续保留当时获得的 Apache-2.0 权利。

Cutover 之后新增或实质修改的 Baga 自研 Platform / OEM 侧内容，除非文件 / 目录另行声明，采用新的默认授权策略。

详见 `LICENSE_HISTORY.md`。

## 11. 外部贡献与未来 Commercial Relicensing

如果未来全球开发者大量向 Baga Ink Platform Core / Adapter 提交代码，而项目没有取得足够的再授权权利，Commercial Dual Licensing 很容易被自己锁死。

因此：

- Contributor 必须拥有提交代码的权利；
- 不得把来源不清或不兼容的第三方代码直接复制进 Baga 自研文件；
- 针对需要 Community + Commercial 双授权的 Baga Platform / Adapter 代码，外部 Contribution 在 merge 前可能需要签署 Contributor License Agreement（CLA）；
- 在正式、经过法律审核的 CLA 发布并签署前，Maintainer 可以暂缓会阻碍未来 Commercial Relicensing 的外部代码贡献；
- Translation、Issue、Test Data、文档等可以按其实际性质采用不同贡献流程。

不得为了短期接受一个 PR，长期失去项目自身的商业授权能力。

## 12. Trademark / Compatibility

软件 License 和文档 License 不自动授予 Trademark 权利。

例如：

```text
Baga Ink
Baga Ink Platform
Baga Ink Market
Baga Ink Compatible
```

可以由未来的 Trademark / Brand Policy 单独管理。

尤其是：一个第三方实现不得仅因为“代码能跑”就声称自己获得官方 `Baga Ink Compatible` 认证。

## 13. README 展示规则

为避免普通用户和个人开发者看到首页就产生“这是个收费平台”的反感：

- README 第一屏不突出 Commercial Pricing / OEM Licensing；
- 不把醒目的“Commercial License” Badge 当项目主身份；
- README 可以自然描述 Baga Ink 是开放开发、公开源码、社区协作的平台；
- 精确的商业边界放在 README 后部 `Licensing` 与正式 Policy 中；
- 不能声称当前许可证获得了 OSI Approval，除非事实确实如此。

原则是：

> **社区参与低摩擦，但商业边界不能含糊。**

## 14. 最终原则

> **个人和社区使用要简单；App 开发要简单；OEM 商业使用 Baga 自研 Platform / Adapter 必须单独授权；LifeBook 保持 Proprietary；第三方代码永远保持原许可证。**
