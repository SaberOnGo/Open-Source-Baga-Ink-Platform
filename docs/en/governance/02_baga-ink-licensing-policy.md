# Baga Ink Licensing Policy

> **Document level:** Project governance / licensing architecture  
> **Document ID:** `governance.licensing.02`  
> **Locale:** English (`en`)  
> **Status:** Governance Baseline v1.2  
> **Date:** 2026-08-23  
> **Counterpart:** `docs/zh-CN/governance/02_Baga-Ink授权策略.md`

## 0. Purpose

Baga Ink is developed in public for users, individual developers, researchers, device porters, application developers, and commercial device makers.

The project applies different licensing policies to different asset classes. Community use, application development, commercial device/platform deployment, OEM enablement, first-party proprietary products, official Baga services, and third-party upstream software are governed separately where appropriate.

This document is the canonical repository policy for those licensing boundaries. It is an engineering and governance policy, not a complete commercial agreement or legal opinion. Commercial releases and agreements should be reviewed against applicable law and all third-party license obligations.

## 1. Core model

```text
Community / personal / research / education
        → available under the applicable community license

Ordinary Baga IKP application development
        → application licensing is separate from OEM/platform licensing

Commercial OEM / device / platform deployment
        → written Baga Commercial License required
        → qualifying OEM ports may receive no-fee or reduced-fee Platform terms

Official Baga Ink Client / Market / certification / hosted services
        → may remain proprietary and commercially controlled

LifeBook production application
        → proprietary / closed-source first-party product

Third-party software
        → retains its upstream license
```

## 2. Asset-by-asset policy

| Asset | Default policy | Commercial model |
|---|---|---|
| Baga Ink Standards / Protocol prose | Publicly readable; copyright retained; documentation policy applies | Standards may be studied and used for Baga application development and interoperability. Commercial device/platform deployment and official compatibility branding are governed separately. |
| Baga Ink Platform Core | PolyForm Noncommercial 1.0.0 unless explicitly overridden | Commercial OEM/device/platform use requires a written commercial license. Qualifying OEMs may receive no-fee or reduced-fee Platform terms for an agreed scope. |
| Baga Device Adapter reference implementations | Same default as Platform Core unless explicitly overridden | Commercial integration and shipment require written terms. OEMs that implement and maintain a conforming port may qualify for OEM Enablement terms. |
| Baga Adapter SDK / codegen / conformance tooling | File- or directory-specific license may apply | OEM production, proprietary integration, certification, or commercial redistribution may require separate terms. |
| BICTS / Compatibility | Specifications and test expectations are public; implementation files follow their stated license | Official `Baga Ink Compatible` certification, marks, and commercial certification services remain controlled by the Baga Ink project. |
| Official Baga Ink Client | Proprietary / closed-source by default unless a component explicitly states otherwise | Device management, bootstrap, distribution, OEM integration, enterprise management, and support may be offered as commercial products or services. |
| Official Baga Ink Market / Repository / hosted services | May be partially or fully proprietary | Official Market, enterprise Market, signing/trust services, hosted repositories, analytics, distribution, and OEM services may be commercial products. |
| Baga App API / ordinary IKP App SDK | Application development remains independent from OEM/platform licensing; reusable SDK/sample source should use an explicit license | Building and selling an IKP application that targets the published Baga App APIs does **not by itself** require a Baga OEM/platform commercial license. |
| LifeBook production App | Proprietary / closed source | First-party commercial product; not part of the public Baga Platform source distribution. |
| `baga-probe.ikp` and example apps | Prefer an explicit permissive license such as Apache-2.0 when published | Intended for development, testing, examples, and interoperability. |
| KOReader / koreader-base / FBInk / KPM / KindleTool / other third-party code | Upstream license only | Baga community or commercial licenses do not relicense upstream code. |

## 3. Default software license

The root `LICENSE` contains the unmodified **PolyForm Noncommercial License 1.0.0**.

Unless a file or directory explicitly states another license, Baga-authored Platform/OEM-side software first published after the licensing cutover is offered under that license.

Baga-specific scope, exceptions, commercial terms, OEM Enablement terms, and product policies are defined in project policy documents or separate agreements. The PolyForm license text itself MUST remain unmodified while the repository identifies it as PolyForm Noncommercial 1.0.0.

## 4. Commercial use

The community license is not an OEM commercial deployment license.

Typical uses requiring a separate written commercial agreement include:

```text
preinstallation of Baga Ink Platform on a commercial device
shipment of a commercial device containing Baga-authored Platform code
commercial redistribution of Baga Platform or Device Adapter implementation
paid managed-device or managed-platform services using Baga-authored Platform code
OEM proprietary integration based on Baga-authored Platform or Adapter code
official commercial compatibility or certification arrangements
```

A written agreement is required even when the Platform license fee is zero. The agreement defines the licensed device/product scope, applicable versions, third-party obligations, compatibility evidence, brand permissions, support terms, and other commercial conditions.

See `COMMERCIAL_LICENSE.md` for the commercial licensing entry point.

## 5. OEM Enablement Program

Baga Ink may provide no-fee or reduced-fee Platform commercial licensing to device makers that independently implement and maintain a conforming Baga Platform Port / Device Adapter.

Eligibility may include:

```text
OEM implementation and maintenance of the Device Adapter / Platform Port
required Adapter Contract Tests passing
applicable BICTS profiles passing
reproducible Compatibility Records
maintenance across supported firmware revisions
compliance with applicable third-party licenses
compliance with Baga trademark and certification rules
```

The commercial agreement may be limited by:

```text
Device Model / SKU
Firmware range
Baga Platform version or version range
territory
shipment or product family
distribution channel
support level
term
```

No-fee or reduced-fee terms apply only to the scope stated in the written agreement. They do not automatically extend to future device models, firmware revisions, product families, services, or Baga releases.

## 6. Separately licensed products and services

A no-fee Platform license does not include every Baga commercial product or service.

Separate commercial terms may apply to:

```text
Baga-provided Device Adapter / Platform Port engineering
OEM customization or white-label integration
refresh, power, sleep/wake, performance, and compatibility engineering
official certification and compatibility-mark authorization
official Baga Ink Client integration and enterprise device management
official Market / Repository / signing / trust integration
hosted services
support / maintenance / SLA
managed deployment
```

## 7. Application developers

Application developers and OEM/platform licensees are separate licensing categories.

> **Using the documented Baga App APIs to build or sell an IKP application does not by itself require an OEM/platform commercial license.**

Reusable App SDK source, templates, `baga-probe.ikp`, and example applications SHOULD carry an explicit file- or directory-level license when published. Such local license notices govern those assets.

This policy does not grant rights to proprietary LifeBook source code, Baga certification marks, trademarks, or third-party code beyond their applicable licenses.

## 8. Official Client, Market, and service boundary

The official **Baga Ink Client** is a first-party product and may remain proprietary. Baga distribution and interoperability protocols may remain public independently of the official Client implementation.

A third-party implementation of a public protocol does not automatically receive access to:

```text
Official Baga Ink Market
Official Repository or signing infrastructure
Baga trust roots or commercial accounts
LifeBook distribution rights
Baga Ink Compatible certification
Baga trademarks or logos
official hosted services, analytics, or recommendation systems
```

Official Baga Ink Market, Repository, signing/trust infrastructure, certification services, compatibility branding, hosted services, enterprise management, and related services may be governed by separate terms.

## 9. Standards and protocol implementation

Baga Ink Standards are published for application development, interoperability, compatible implementations, and technical review.

Copyright protects authored text and artifacts but does not by itself create exclusive ownership over every protocol idea or interface fact. Additional project rights may arise from Baga-authored software licenses, trademarks, certification programs, official services, patents where applicable, and commercial agreements.

Implementing a public specification does not grant official certification or permission to use protected Baga branding.

## 10. Documentation licensing

Baga-authored public prose under `docs/en/` and `docs/zh-CN/` is published for public reading and project collaboration. Documentation redistribution rights are governed by the applicable file or project documentation license.

Before relying on documentation redistribution rights for a commercial publication, the applicable notice and license must be identified for that material.

## 11. LifeBook boundary

LifeBook is the flagship/reference product used to validate Baga Ink architecture. The production LifeBook application is **not** part of the public Baga Platform source distribution.

The public repository may contain:

```text
LifeBook Reference App architecture
LifeBook product-behavior and design documents
interoperability examples
mock, sample, or probe applications
```

These materials do not imply publication of production LifeBook source code, backend code, product algorithms, account/community implementation, AI product logic, or commercial assets.

## 12. Third-party boundary

Every third-party component retains its own license. A Baga Commercial License cannot waive or replace GPL, AGPL, or other upstream obligations.

Each concrete distribution must identify its actual dependency graph and satisfy every license applicable to the shipped combination. Strong-copyleft integration is a release-gating architecture and licensing question for proprietary or commercial distributions.

See `THIRD_PARTY_NOTICES.md`.

## 13. Historical Apache-2.0 cutover

Baga-authored material already published under Apache License 2.0 retains the rights granted under that historical license.

```text
last pre-cutover main commit:
3517970a221dd2e40d8931e1f68399032c343789
```

Historical versions at or before that revision remain governed by the license under which they were originally published. New or materially modified Baga-authored Platform/OEM-side material after the cutover follows the current default unless a file or directory explicitly states otherwise.

See `LICENSE_HISTORY.md`.

## 14. Contributions and relicensing

Contributors must own or have authority to submit their contributions. Third-party code must not be incorporated into Baga-authored files without compatible licensing and recorded provenance.

External contributions to Baga Platform / Adapter code that may be distributed under both community and commercial terms may require a legally reviewed Contributor License Agreement before merge.

A contribution MUST NOT be merged if its license terms prevent distribution under the licensing model applicable to the target component.

## 15. Trademark / compatibility boundary

Software and documentation licenses do not grant unrestricted trademark rights.

Names and marks such as:

```text
Baga Ink
Baga Ink Platform
Baga Ink Market
Baga Ink Compatible
```

may be governed by a separate trademark or brand policy.

An implementation must not represent itself as officially `Baga Ink Compatible` unless it satisfies the applicable compatibility/certification requirements and has permission to use the relevant mark.

## 16. README licensing presentation

The root README is the project overview and onboarding entry point. Detailed commercial licensing terms are maintained in the later `Licensing` section and in the dedicated licensing documents.

The README hero does not contain pricing, OEM commercial-license warnings, or a commercial-license badge. Any licensing statements that do appear in the README MUST remain accurate and consistent with this policy.

## 17. Final rule

> **Baga Ink applies separate licensing rules to community use, application development, OEM Platform deployment, official services, first-party proprietary products, and third-party software. Commercial OEM terms are defined by written agreements; qualifying OEM ports may receive no-fee or reduced-fee Platform terms; LifeBook remains proprietary; third-party software retains its upstream license.**
