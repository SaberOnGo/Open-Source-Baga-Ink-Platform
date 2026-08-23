# Baga Ink Licensing Policy

> **Document level:** Project governance / licensing architecture  
> **Document ID:** `governance.licensing.02`  
> **Locale:** English (`en`)  
> **Status:** Governance Baseline v1.1  
> **Date:** 2026-08-23  
> **Counterpart:** `docs/zh-CN/governance/02_Baga-Ink授权策略.md`

## 0. Purpose

Baga Ink is developed in public and is intended to support a large community of users, individual developers, researchers, device porters, App developers, and commercial OEM partners.

The licensing model separates **community use**, **application development**, **commercial device/platform deployment**, **OEM ecosystem enablement**, **first-party proprietary products**, **official Baga services**, and **third-party upstream software** instead of forcing every asset into one license.

This document is the canonical repository policy for that separation. It is an engineering/governance policy, not legal advice. Commercial agreements and final release obligations should receive legal review before material commercial distribution.

## 1. Core model

```text
Community / personal / research / education
        → free under the applicable community license

Ordinary Baga IKP application development
        → low-friction; commercial apps are allowed without an OEM/platform license

Commercial OEM / device / platform deployment
        → written Baga Commercial License required
        → qualifying ecosystem-building OEMs may receive no-fee or reduced-fee Platform terms

Official Baga Ink Client / Market / certification / hosted services
        → may remain proprietary and commercially controlled

LifeBook production application
        → proprietary / closed-source first-party product

Third-party software
        → always retains its upstream license
```

The project should not make commercial licensing the first message seen by ordinary users or individual developers. README and product communication should lead with what Baga Ink does, how to use it, and how to contribute. Formal licensing pages must nevertheless state the actual terms accurately.

## 2. Asset-by-asset policy

| Asset | Default policy | Commercial model |
|---|---|---|
| Baga Ink Standards / Protocol prose | Publicly readable; copyright retained; documentation policy applies | Anyone may study the standards and build Baga apps. Commercial device/platform implementation and official compatibility branding are separately governed. |
| Baga Ink Platform Core | PolyForm Noncommercial 1.0.0 unless explicitly overridden | Commercial OEM/device/platform use requires a written commercial license; qualifying self-porting OEMs may receive no-fee or reduced-fee Platform terms for an agreed scope. |
| Baga Device Adapter reference implementations | Same default as Platform Core | Commercial integration/shipments require written terms; OEMs that implement and maintain a conforming port may qualify for OEM Enablement terms. |
| Baga Adapter SDK / codegen / conformance tooling | Community development/testing access; file- or directory-specific license may apply | OEM production, proprietary integration, certification, or commercial distribution may require separate terms. |
| BICTS / Compatibility | Specifications and test expectations are public; implementation files follow their stated license | Official `Baga Ink Compatible` certification, marks, and commercial certification services remain controlled by the Baga Ink project. |
| Official Baga Ink Client | Proprietary / closed-source by default unless a component explicitly says otherwise | Official device management, bootstrap, distribution, OEM integration, enterprise management, and support may be commercial products/services. |
| Official Baga Ink Market / Repository / hosted services | May be partially or fully proprietary | Official Market, enterprise Market, signing/trust services, hosted repositories, analytics, distribution, and OEM services may be commercial products. |
| Baga App API / ordinary IKP App SDK | Keep app development low-friction and preferably permissive where source SDK/sample code is provided | Building and selling an IKP app that targets published Baga app APIs does **not by itself** require a Baga OEM/platform commercial license. |
| LifeBook production App | Proprietary / closed source | First-party commercial product; not part of the public Baga Platform source distribution. |
| `baga-probe.ikp` and example apps | Prefer permissive open-source licensing such as Apache-2.0 when published | Intended to teach and test Baga app development. |
| KOReader / koreader-base / FBInk / KPM / KindleTool / other third-party code | Upstream license only | Baga community or commercial licenses never relicense upstream code. |

## 3. Default software license

The root `LICENSE` contains the unmodified **PolyForm Noncommercial License 1.0.0**.

Unless a file or directory explicitly states another license, Baga-authored Platform/OEM-side software first published after the licensing cutover is offered under that license.

The project MUST NOT modify the PolyForm license text while continuing to call the result PolyForm. Baga-specific scope, exceptions, commercial terms, OEM incentives, and product policy belong in this document or separate agreements.

## 4. Commercial use still requires a written agreement

The community license is not a commercial OEM license.

Examples that generally require a separate written commercial agreement include:

```text
preinstalling Baga Ink Platform on a commercial device
shipping a device or product containing Baga-authored Platform code
commercial redistribution of Platform or Device Adapter implementation
using Baga Platform code in a paid managed device/platform service
OEM proprietary integration based on Baga-authored Platform/Adapter code
official commercial compatibility/certification arrangements
```

A written agreement is required even when the commercial Platform fee is zero. This preserves clear scope, third-party compliance obligations, compatibility evidence, branding boundaries, and future product-line decisions.

## 5. OEM Enablement Program

Baga Ink should not discourage a device maker from expanding the ecosystem by forcing the OEM to both fund the Device Adapter work and pay an additional platform-entry royalty.

Policy:

> **A qualified OEM that independently funds, implements, validates, and maintains a conforming Baga Platform Port / Device Adapter may receive a no-fee or reduced-fee Baga Platform commercial license for a specifically agreed scope.**

Eligibility may include:

```text
OEM implements and maintains the Device Adapter / Platform Port
required Adapter Contract Tests pass
applicable BICTS profile passes
Compatibility Records are reproducible and kept current
firmware regressions are addressed
third-party license obligations are satisfied
Baga trademarks/certification claims are not used without authorization
```

The agreement may be scoped by:

```text
Device Model / SKU
Firmware range
Baga Platform version/range
territory
shipment/product family
distribution channel
support level
term
```

A no-fee license is not an automatic or perpetual right for every future model, firmware, service, or Baga release. The goal is to reward useful ecosystem porting while preserving control over scope and official services.

## 6. What Baga may charge for even when Platform royalty is zero

A no-fee Platform license does not mean all Baga commercial value is free.

Separate paid products/services may include:

```text
Baga-provided Device Adapter / Platform Port engineering
OEM customization / white-label integration
refresh, power, sleep/wake, performance and compatibility tuning
official certification and compatibility-mark authorization
official Baga Ink Client integration / enterprise device management
official Market / Repository / signing / trust integration
hosted services
support / maintenance / SLA
managed deployment
```

The public policy is therefore to reduce the **entry cost for ecosystem-building OEMs**, not to give away every official Baga service.

## 7. Ordinary App developers are different from OEMs

A developer who writes and sells an IKP application is not automatically an OEM/platform licensee.

> **Using the documented Baga app APIs and producing or selling an IKP application does not by itself trigger an OEM/platform commercial license.**

When Baga publishes reusable App SDK source, templates, `baga-probe.ikp`, or example apps, those assets SHOULD carry an explicit permissive license where practical. Their local license/header overrides the Platform default for those files.

This policy does not grant rights to copy proprietary LifeBook code, use Baga certification marks, or use third-party code beyond its own license.

## 8. Official Client, Market, and control-plane boundary

The official **Baga Ink Client** is a first-party product and control surface, not a requirement that all Baga distribution protocols be closed.

The project may keep the official Client proprietary while publishing the protocols required for interoperability. Third parties may therefore be able to implement compatible tooling without receiving rights to official Baga services.

Implementing a public protocol does **not** automatically grant access to:

```text
Official Baga Ink Market
Official Repository / signing infrastructure
Baga trust roots or commercial accounts
LifeBook distribution rights
Baga Ink Compatible certification
Baga trademarks / logos
official hosted services / analytics / recommendation systems
```

This separation supports an open developer ecosystem while preserving a strongly controlled official distribution and service layer.

## 9. Standards and protocol implementation

Baga Ink Standards are public so independent developers can learn the platform and create interoperable applications.

Copyright protects authored text and artifacts; it does not automatically create exclusive ownership over every protocol idea or interface fact. Commercial protection therefore also relies on Baga-authored software licensing, trademarks, certification, official services, future patent rights where applicable, and OEM agreements.

A third party does not obtain permission to claim official certification or use protected Baga branding merely by reading or implementing a specification.

## 10. Documentation license

Unless a document says otherwise, Baga-authored public prose under `docs/en/` and `docs/zh-CN/` is published for public reading and community collaboration and is intended to use a noncommercial documentation license model.

Before a formal documentation redistribution license is relied on for a commercial publication, confirm the exact file notice and obtain legal review.

## 11. LifeBook boundary

LifeBook is the flagship/reference product used to validate Baga Ink architecture, but the production LifeBook application is **not** part of the public Baga Platform source distribution.

Public repository content may include LifeBook Reference App architecture, product-behavior/design documents, interoperability examples, and mock/sample/probe applications. It does not imply publication of production LifeBook source, backend code, product algorithms, account/community implementation, AI product logic, or commercial assets.

## 12. Third-party boundary

Every third-party component keeps its own license. A Baga commercial license cannot waive or replace GPL/AGPL/other upstream obligations.

A concrete release must record its actual dependency graph and comply with every license that applies to the shipped combination. Strong-copyleft integration is a release-blocking architecture/legal question for proprietary/commercial distributions.

See `THIRD_PARTY_NOTICES.md`.

## 13. Historical Apache-2.0 cutover

Baga-authored material already published under Apache License 2.0 keeps the rights recipients already received. Those grants cannot be retroactively withdrawn.

```text
last pre-cutover main commit:
3517970a221dd2e40d8931e1f68399032c343789
```

Historical versions at or before that revision remain available under the license under which they were originally published. New or materially modified Baga-authored Platform/OEM-side material after the cutover follows the new default unless a file/directory explicitly says otherwise.

See `LICENSE_HISTORY.md`.

## 14. Contributions and relicensing

Commercial/community dual licensing only remains practical if the project has sufficient rights to distribute contributed code under both community and commercial terms.

Therefore contributors must own or have authority to submit their contributions; third-party code must not be copied into Baga-authored files without compatible licensing/provenance; and external contributions to dual-licensed Baga Platform/Adapter code may require a legally reviewed CLA before merge.

The project MUST NOT casually accept code under terms that make the intended commercial licensing model impossible.

## 15. Trademark / compatibility boundary

Software and documentation licenses do not grant unrestricted trademark rights.

Names and marks such as `Baga Ink`, `Baga Ink Platform`, `Baga Ink Market`, and `Baga Ink Compatible` may be subject to separate trademark/brand policy. An implementation must not represent itself as officially `Baga Ink Compatible` unless it satisfies the project's compatibility/certification policy and has permission to use the applicable mark.

## 16. README presentation rule

To avoid turning away ordinary users and individual developers:

- do not place commercial pricing or OEM licensing warnings in the README hero/first screen;
- do not use an alarming commercial-license badge as the main project identity;
- keep precise commercial and OEM Enablement boundaries in the later `Licensing` section and formal policy documents;
- never falsely claim that the license is OSI-approved if it is not.

The goal is low-friction community participation with clear formal commercial boundaries.

## 17. Final rule

> **Community use should be easy; App development should be easy; OEMs that genuinely expand the device ecosystem should not be charged merely for doing the porting work; official engineering, certification, Client, Market, hosted services, support, and other Baga-created commercial value may be monetized separately; LifeBook remains proprietary; third-party code always keeps its upstream license.**
