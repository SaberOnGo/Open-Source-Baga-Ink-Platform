# Third-Party Notices and License Boundary

Baga Ink uses a layered licensing model. The root `LICENSE` applies only to Baga-authored software that falls within its scope and does **not** relicense third-party software, source code, documentation, assets, firmware interfaces, or other works used by, referenced by, vendored into, linked with, or distributed alongside Baga Ink.

A Baga Ink Commercial License likewise applies only to rights the Baga licensor can grant. It cannot waive GPL/AGPL/other upstream obligations.

## Important distribution rule

A concrete Baga release or device distribution MUST comply with every license that applies to the components actually included in that release.

Whether a particular integration creates source-disclosure, attribution, relinking, network-source, or other obligations depends on the actual code, linkage, modification, packaging, process boundary, and distribution model. Release maintainers must review the exact dependency graph rather than relying on this overview.

This file is an engineering notice, not legal advice.

## Upstream projects relevant to the current Kindle design

The Kindle architecture intentionally reuses mature upstream work rather than reimplementing device support from scratch.

| Project | Current upstream license signal | Baga role / relationship |
|---|---|---|
| [KOReader](https://github.com/koreader/koreader) | GNU AGPL v3 | Kindle reader/UI/device knowledge adopted internally; not a Baga public API |
| [koreader-base](https://github.com/koreader/koreader-base) | GNU AGPL v3 | Native/Lua substrate and device support used by KOReader/Baga Kindle integration |
| [FBInk](https://github.com/NiLuJe/FBInk) | GPL-3.0-or-later | E-paper framebuffer/refresh implementation source for supported devices |
| [KPM](https://github.com/KindleModding/KPM) | Repository identifies GPL-3.0; some individual files explicitly use CC0 | Kindle native package-management/bootstrap mechanism; not the IKP package manager |
| [KindleTool](https://github.com/NiLuJe/KindleTool) | GPL-3.0 | Build/package tooling for Kindle update packages |
| [KindleModding Hotfix](https://github.com/KindleModding/Hotfix) | GPL-3.0 | Possible validated Homebrew foundation component, not a Baga public API |

The list above identifies projects already relevant to the architecture. It is **not** a declaration that every listed project is bundled in this repository or every future Baga release.

## Commercial distribution warning

The Baga community/commercial licensing model does not turn a combined work containing strong-copyleft software into proprietary software.

Before a commercial OEM distribution is approved, maintainers MUST answer at least:

```text
Is upstream source copied or vendored?
Is it modified?
Is Baga statically or dynamically linked to it?
Is it loaded as a plugin/module?
Is it invoked as a separate process?
Is it merely interoperated with through an external protocol/interface?
What source / notice / relinking / network-source obligations apply?
Can the intended proprietary boundary legally coexist with the selected upstream integration?
```

If the answer is uncertain, licensing is a **release blocker**, not something to defer until after shipment.

## Per-release license manifest

Every distributable Baga Platform release SHOULD/MUST, as applicable to release policy, record at least:

```text
upstream project
upstream version / commit
source URL
source digest
license / SPDX identifier
local patch set
native target / ABI
which Baga subsystem uses it
whether source is bundled, linked, invoked, or merely interoperated with
required attribution / source-offer / redistribution obligations
```

The release-specific manifest is the authoritative record of what was actually shipped. This repository-level file is only a standing overview.

## Vendored and copied third-party material

When third-party material is copied into this repository:

1. preserve its upstream license and required notices;
2. do not replace the upstream license header with the Baga community license;
3. keep provenance (project, version/commit, source URL, digest where practical);
4. place additional license text/notices beside the vendored component when required;
5. update this file and/or the release dependency manifest when the component becomes part of a distributable product.

## Machine-readable and generated artifacts

Generated code follows the licensing policy defined by its generator/source and generated-file header.

Baga-authored App-facing SDK/example output MAY use an explicit permissive license where the project intends broad App ecosystem adoption. Baga-authored Platform/OEM-side generated code follows the repository default unless its generator/output explicitly states otherwise.

Third-party generated artifacts remain subject to their upstream terms.

## Historical Baga license

Historical Baga-authored material previously published under Apache-2.0 retains the rights already granted for those historical versions. See `LICENSE_HISTORY.md`.

## Questions

For uncertainty involving AGPL/GPL code, static/dynamic linking, plugins, modified upstream components, network-access provisions, or a proprietary/commercial distribution boundary, resolve the question before shipping and obtain qualified legal review where appropriate.
