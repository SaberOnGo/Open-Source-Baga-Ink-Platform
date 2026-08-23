# Third-Party Notices and License Boundary

Baga Ink's original project material is licensed under the Apache License 2.0 unless a file or directory explicitly states otherwise.

That license applies to **Baga-authored material only**. It does not relicense third-party software, source code, documentation, assets, firmware interfaces, or other works used by, referenced by, vendored into, linked with, or distributed alongside Baga Ink.

## Important distribution rule

A concrete Baga release or device distribution MUST comply with every license that applies to the components actually included in that release.

In particular, a permissive Baga license does not remove copyleft obligations from a combined work or distribution that incorporates GPL/AGPL-licensed material. Whether a particular form of integration creates additional obligations depends on the actual code, linkage, modification, packaging, and distribution model; release maintainers must review the exact dependency graph rather than relying on this overview.

This file is an engineering notice, not legal advice.

## Upstream projects relevant to the current Kindle design

The current Kindle architecture intentionally plans to reuse mature upstream work rather than reimplementing device support from scratch. Relevant projects include:

| Project | Current upstream license signal | Baga role / relationship |
|---|---|---|
| [KOReader](https://github.com/koreader/koreader) | GNU AGPL v3 | Kindle reader/UI/device knowledge adopted internally; not a Baga public API |
| [koreader-base](https://github.com/koreader/koreader-base) | GNU AGPL v3 | Native/Lua substrate and device support used by KOReader/Baga Kindle integration |
| [FBInk](https://github.com/NiLuJe/FBInk) | GPL-3.0-or-later | E-paper framebuffer/refresh implementation source for supported devices |
| [KPM](https://github.com/KindleModding/KPM) | Repository identifies GPL-3.0; some individual files explicitly use CC0 | Kindle native package-management/bootstrap mechanism; not the IKP package manager |
| [KindleTool](https://github.com/NiLuJe/KindleTool) | GPL-3.0 | Build/package tooling for Kindle update packages |
| [KindleModding Hotfix](https://github.com/KindleModding/Hotfix) | GPL-3.0 | Possible validated Homebrew foundation component, not a Baga public API |

The list above describes projects already relevant to the architecture. It is **not** a declaration that every listed project is currently bundled in this repository or in every future Baga release.

## Per-release license manifest

Every distributable Baga Platform release SHOULD/MUST, as applicable to the release policy, record at least:

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
2. do not replace the upstream license header with `Apache-2.0`;
3. keep provenance (project, version/commit, source URL, digest where practical);
4. place additional license text or notices beside the vendored component when required;
5. update this file and/or the release dependency manifest when the component becomes part of a distributable product.

## Machine-readable and generated artifacts

Generated code inherits the licensing policy defined by its generator/source and generated-file header. A generator that emits Baga-authored interfaces SHOULD emit an appropriate SPDX header where the target format supports comments.

Third-party generated artifacts remain subject to the terms of their upstream source/license.

## Questions

If a future integration model creates uncertainty — especially around AGPL/GPL code, static/dynamic linking, modified upstream components, or network-access provisions — treat licensing as a release-blocking engineering question and resolve it before shipping.
