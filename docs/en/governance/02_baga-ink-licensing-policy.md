# Baga Ink Licensing Policy

> **Document level:** Project governance / licensing architecture  
> **Document ID:** `governance.licensing.02`  
> **Locale:** English (`en`)  
> **Status:** Governance Baseline v1.0  
> **Date:** 2026-08-23  
> **Counterpart:** `docs/zh-CN/governance/02_Baga-Ink授权策略.md`

## 0. Purpose

Baga Ink is developed in public and is intended to support a large community of users, individual developers, researchers, device porters, and commercial OEM partners.

The licensing model therefore separates **community use**, **application development**, **commercial device/platform deployment**, **first-party proprietary products**, and **third-party upstream software** instead of forcing every asset into one license.

This document is the canonical repository policy for that separation. It is an engineering/governance policy, not legal advice. Commercial agreements and final release obligations should receive legal review before material commercial distribution.

## 1. Core model

```text
Community / personal / research / education
        → free under the applicable community license

Ordinary Baga IKP application development
        → low-friction; commercial apps are allowed without an OEM/platform license

Commercial OEM / device / platform deployment
        → separate Baga Ink Commercial License required

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
| Baga Ink Platform Core | PolyForm Noncommercial 1.0.0 unless explicitly overridden | Personal/research/education/noncommercial use is free. Commercial OEM/device/platform use requires a commercial license. |
| Baga Device Adapter reference implementations | Same default as Platform Core | Commercial device integration or shipment requires a commercial license unless an explicit permissive exception applies. |
| Baga Adapter SDK / codegen / conformance tooling | Community development/testing access; file- or directory-specific license may apply | OEM production use, commercial distribution, certification services, or proprietary integration may require a commercial license. |
| BICTS / Compatibility | Specifications and test expectations are public; implementation files follow their stated license | Official `Baga Ink Compatible` certification, marks, and commercial certification services remain controlled by the Baga Ink project. |
| Baga Ink Client | May contain public-source and proprietary components | OEM customization, managed deployment, enterprise tooling, or commercial distribution may be separately licensed. |
| Baga Ink Market server/services | May be partially or fully proprietary | Official Market, enterprise Market, hosted services, and OEM services may be commercial products. |
| Baga App API / ordinary IKP App SDK | Keep app development low-friction and preferably permissive where source SDK/sample code is provided | Building and selling an IKP app that targets published Baga app APIs does **not by itself** require a Baga OEM/platform commercial license. |
| LifeBook production App | Proprietary / closed source | First-party commercial product; not part of the public Baga Platform source distribution. |
| `baga-probe.ikp` and example apps | Prefer permissive open-source licensing such as Apache-2.0 when published | Intended to teach and test Baga app development. |
| KOReader / koreader-base / FBInk / KPM / KindleTool / other third-party code | Upstream license only | Baga community or commercial licenses never relicense upstream code. |

## 3. Default software license

The root `LICENSE` contains the unmodified **PolyForm Noncommercial License 1.0.0**.

Unless a file or directory explicitly states another license, Baga-authored Platform/OEM-side software first published after the licensing cutover is offered under that license.

The project MUST NOT modify the PolyForm license text while continuing to call the result PolyForm. Baga-specific scope, exceptions, commercial terms, and product policy belong in this document or separate agreements.

## 4. Commercial use

The community license is not a commercial OEM license.

Examples that generally require a separate written commercial agreement include:

```text
preinstalling Baga Ink Platform on a commercial device
shipping a device or commercial product containing Baga-authored Platform code
commercial redistribution of the Platform or Device Adapter implementation
using Baga Platform code as part of a paid managed device/platform service
OEM proprietary integration based on Baga-authored Platform/Adapter code
official commercial compatibility/certification arrangements
```

Commercial evaluation and prototype licensing may be offered separately, including at no charge, but a company should not assume that anticipated commercial use is covered by the noncommercial community license.

See `COMMERCIAL_LICENSE.md` for the commercial licensing entry point. Pricing is intentionally not embedded in the public repository because commercial terms may depend on shipment volume, support scope, certification, customization, territory, or service obligations.

## 5. Ordinary App developers are different from OEMs

A developer who writes and sells an IKP application is not automatically an OEM/platform licensee.

The project policy is:

> **Using the documented Baga app APIs and producing an IKP application does not by itself trigger an OEM/platform commercial license.**

This distinction is important for ecosystem growth.

When Baga publishes reusable App SDK source code, templates, `baga-probe.ikp`, or example apps, those assets SHOULD carry an explicit permissive license where practical. Their local license/header overrides the Platform default for those files.

This policy does not grant rights to copy proprietary LifeBook code, Baga trademarks, certification marks, or third-party code beyond their own licenses.

## 6. Standards and protocol implementation

Baga Ink Standards are public so independent developers can learn the platform and create interoperable applications.

Copyright protects the authored text and artifacts; it does not magically turn every protocol idea or interface fact into exclusive ownership. Commercial protection for the ecosystem therefore also relies on:

```text
Baga-authored Platform / Adapter software licensing
trademarks and product names
`Baga Ink Compatible` certification / compatibility evidence
future patent rights where applicable
official Market / services / support / OEM agreements
```

A third party does not obtain permission to claim official certification or use protected Baga branding merely by reading or implementing a specification.

## 7. Documentation license

Unless a document says otherwise, Baga-authored public prose under `docs/en/` and `docs/zh-CN/` is published for public reading and community collaboration and is intended to use a noncommercial documentation license model.

Before a formal documentation redistribution license is relied on for a commercial publication, confirm the exact file notice and obtain legal review. This policy intentionally does not pretend that the software-oriented PolyForm text is a complete substitute for a documentation license.

## 8. LifeBook boundary

LifeBook is the flagship/reference product used to validate Baga Ink architecture, but the production LifeBook application is **not** part of the public Baga Platform source distribution.

Public repository content may include:

```text
LifeBook Reference App architecture
LifeBook behavior/design documentation
interoperability examples
mock/sample/probe applications
```

It does not imply publication of LifeBook production source code, backend code, product algorithms, account/community implementation, AI product logic, or commercial assets.

A future public LifeBook-related file must state its own license if it is intentionally released.

## 9. Third-party boundary

Every third-party component keeps its own license. In particular, a Baga commercial license cannot waive or replace GPL/AGPL/other upstream obligations.

A concrete release must record its actual dependency graph and comply with every license that applies to the shipped combination. See `THIRD_PARTY_NOTICES.md`.

Strong-copyleft integration is a release-blocking architecture question and must be reviewed before a proprietary/commercial distribution is shipped.

## 10. Historical Apache-2.0 cutover

Baga-authored material already published under Apache License 2.0 keeps the rights that recipients already received. Those grants cannot be retroactively withdrawn.

The licensing cutover baseline is:

```text
last pre-cutover main commit:
3517970a221dd2e40d8931e1f68399032c343789
```

Historical versions at or before that revision remain available under the license under which they were originally published. New or materially modified Baga-authored Platform/OEM-side material after the cutover follows the new default unless a file/directory explicitly says otherwise.

See `LICENSE_HISTORY.md`.

## 11. Contributions and relicensing

Commercial/community dual licensing only remains practical if the project has sufficient rights to distribute contributed code under both community and commercial terms.

Therefore:

- contributors must own or have authority to submit their contributions;
- third-party code must not be copied into Baga-authored files without compatible licensing/provenance;
- external contributions to dual-licensed Baga Platform/Adapter code may require a Contributor License Agreement (CLA) before merge;
- until a legally reviewed CLA is published and executed, maintainers may defer external code contributions that would prevent future commercial relicensing;
- translation, issue, test-data, or documentation contribution handling may be governed separately when appropriate.

The project MUST NOT casually accept code under terms that make the intended commercial licensing model impossible.

## 12. Trademark / compatibility boundary

Software and documentation licenses do not grant unrestricted trademark rights.

Names and marks such as:

```text
Baga Ink
Baga Ink Platform
Baga Ink Market
Baga Ink Compatible
```

may be subject to separate trademark/brand policy.

In particular, an implementation must not represent itself as officially `Baga Ink Compatible` unless it satisfies the project's compatibility/certification policy and has permission to use the applicable mark.

## 13. README presentation rule

To avoid turning away ordinary users and individual developers:

- do not place commercial pricing or OEM licensing warnings in the README hero/first screen;
- do not use an alarming commercial-license badge as the main project identity;
- the README may simply describe Baga Ink as an open/public-source, community-developed platform;
- keep the precise commercial boundary in the later `Licensing` section and formal policy documents;
- never falsely claim that the license is OSI-approved if it is not.

The goal is **low-friction community participation with clear formal commercial boundaries**, not hiding license terms.

## 14. Final rule

> **Community use should be easy; App development should be easy; commercial OEM exploitation of Baga-authored Platform/Adapter work is separately licensed; LifeBook remains proprietary; third-party code always keeps its upstream license.**
