<div align="center">

# Baga Ink Platform

### One open application platform for e-paper devices

**Build an app once against a stable platform contract. Port Baga Ink to each e-paper device family instead of rewriting every app for every device.**

[![Project status](https://img.shields.io/badge/status-early%20development-orange.svg)](#project-status)
[![Documentation](https://img.shields.io/badge/docs-English-2ea44f.svg)](docs/en/00_baga-ink-documentation-index.md)

<!-- BAGA-LANG-SWITCH:START -->
[![English](https://img.shields.io/badge/Language-English-111111?style=flat-square)](README.md)
[![简体中文](https://img.shields.io/badge/语言-简体中文-2ea44f?style=flat-square)](README.zh-CN.md)
[![Add a language](https://img.shields.io/badge/＋-Add%20a%20language-lightgrey?style=flat-square)](CONTRIBUTING.md#translations)
<!-- BAGA-LANG-SWITCH:END -->

</div>

---

## What is Baga Ink?

**Baga Ink is an application platform, compatibility contract, and developer ecosystem for e-paper devices.**

Today an app written for one e-reader usually cannot move cleanly to another. Kindle homebrew, Android e-paper devices, vendor SDKs, Linux readers, different refresh mechanisms, input stacks, storage layouts, lifecycle rules, package managers, firmware generations, and device quirks all expose different interfaces.

Baga Ink moves those differences **out of applications** and into reusable **Platform Ports / Device Adapters**.

The goal is simple:

> **Applications target Baga Ink, not a particular Kindle model, Android vendor, framebuffer API, or proprietary e-paper SDK.**

Baga Ink is not a replacement operating system. It is the stable layer between portable applications and fragmented e-paper device environments.

---

## Why this project exists

The e-paper ecosystem has excellent hardware, but software development is fragmented.

| Today | Baga Ink direction |
|---|---|
| Apps contain model/vendor/firmware branches | Device differences live behind one Device Adapter Contract |
| Every platform exposes different refresh/input APIs | Apps use stable Baga display and input semantics |
| Installation and packaging differ by device | Portable Baga apps use the `.ikp` package format |
| Compatibility often means “it should work” | Capability detection + Contract Tests + BICTS provide evidence |
| Teams repeatedly rebuild low-level support | Ports reuse mature OS, vendor, homebrew, and open-source mechanisms |
| One app port becomes tied to one device family | The same app contract can target Kindle, Android E-Paper, and future ports |

The long-term user experience should be equally simple:

> **A Baga-compatible e-paper device should be able to participate in one shared app ecosystem instead of turning every app into another hardware-porting project.**

---

## Architecture in one picture

```text
                  Baga Ink Apps
              (.ikp application packages)
                         │
                         ▼
             Baga Ink API / Baga Lua Profile
                         │
                         ▼
                 Baga Ink Platform Core
                         │
                         ▼
              Baga Device Adapter Contract
                         │
          ┌──────────────┴──────────────┐
          ▼                             ▼
     Kindle Port                 Android E-Paper Port
  KOReader / FBInk /             AOSP / vendor SDKs /
 Kindle OS / Homebrew            e-paper device APIs
          │                             │
          └──────────────┬──────────────┘
                         ▼
                  E-Paper Hardware
```

Portable app code should not need this:

```text
if Kindle Paperwhite ...
if BOOX ...
if iReader ...
if firmware >= ...
```

Those differences belong in the platform port, Device Profile, and Quirk Set.

---

## What Baga Ink includes

### Baga Ink Platform
The device-side platform that hosts portable Baga apps, provides the Baga Ink API, manages lifecycle/permissions/sandboxing, and connects applications to the real device.

### Baga Device Adapter Contract
A typed porting contract for display, input, storage, lifecycle, power, and optional capabilities. It defines **what a device port must provide** without requiring Baga to reimplement capabilities that already exist in the OS, vendor SDK, homebrew stack, or mature open-source projects.

### IKP application packages
`.ikp` is the portable Baga application package. It is intentionally separate from device-native installation packages such as Kindle `.kpkg`, MRPI bundles, or Android APKs.

### BICTS and compatibility evidence
Baga Ink Compatibility is intended to be testable. Device + firmware + Platform + Adapter + Profile combinations should be backed by capability evidence, Contract Tests, BICTS, and explicit compatibility records.

### Baga Ink Client
A planned desktop-side client for device detection, bootstrap/install flows, offline transfer, diagnostics, and app delivery on devices that cannot provide a modern app-store experience themselves.

### Baga Ink Market and distribution protocols
The Standards define publisher identity, signing, repository metadata, app discovery, updates, rollback, revocation, offline transfer, and transparency so an open app ecosystem does not become another fragmented set of incompatible stores.

### Reference apps
LifeBook is the flagship/reference product used to prove that a real, large application can remain portable while Baga absorbs device differences below it. Public reference architecture is kept in this repository; the production LifeBook application is a separate first-party product.

---

## First reference platform: Kindle

Kindle is the first major reference port because it is a hard test of the architecture: many hardware generations, different firmware eras, limited resources, unusual homebrew installation paths, and e-paper-specific display behavior.

The Kindle strategy is **not** to rewrite Kindle support from zero.

Baga intends to reuse mature mechanisms from:

- KOReader / koreader-base;
- FBInk;
- Kindle OS mechanisms;
- validated Kindle homebrew tooling.

The Kindle Device Adapter should stay thin. New Baga-specific code should concentrate on capability detection, normalization, profiles, quirks, error/event mapping, self-test, and Contract Tests whenever mature lower-level mechanisms already exist.

The user-facing goal is eventually:

```text
Kindle Home
    ↓
Baga app (for example LifeBook)
```

while jailbreak routes, KPM/MRPI, KOReader internals, ABI targets, and other Kindle-specific machinery remain below the portable app contract.

---

## Android E-Paper and future devices

Baga Ink is **not a Kindle-only project**.

The same Device Adapter Contract is intended to support Android e-paper devices and future device families. On Android, a Generic Android Adapter can provide common behavior while vendor specializations handle only the e-paper capabilities that really differ, such as refresh modes, pen behavior, front light control, or vendor-specific APIs.

Adding a new device family should not require forking the application ecosystem.

---

## Design principles

1. **Portable apps, device-specific ports**  
   Model, firmware, vendor, and ABI decisions stay below the app API.

2. **Contract heavy, adapter light**  
   Compatibility rules should be precise and testable; individual adapters should be as thin as the underlying platform allows.

3. **Reuse mature components**  
   Do not rebuild a framebuffer stack, reader engine, input stack, network stack, or power manager when a proven implementation already exists.

4. **Executable standards**  
   Important behavior should be backed by schemas, IDL, canonical vectors, negative fixtures, reference implementations, and conformance tests — not Markdown alone.

5. **Offline and low-resource friendly**  
   E-paper hardware often has limited CPU, memory, storage, battery, and intermittent networking. The platform must be designed for that reality.

6. **No private device APIs in portable apps**  
   A portable `.ikp` should not import Kindle internals, Android vendor objects, KOReader private APIs, or raw device SDK types.

7. **One ecosystem, measurable compatibility**  
   Community and OEM ports should implement the same contract and prove compatibility with the same tests.

---

## For app developers

Baga Ink is designed so App developers can focus on applications rather than hardware ports.

A Baga app can use stable platform capabilities such as:

```text
baga.ui
baga.reader
baga.library
baga.storage
baga.network
baga.sync
baga.power
baga.permissions
baga.log
```

and Platform-provided standard libraries such as SQLite bindings where defined by the Baga Lua Profile.

Ordinary IKP App development is intentionally kept separate from OEM/platform licensing. Building and selling an IKP application that simply targets the published Baga App APIs does not by itself require an OEM/platform commercial license.

---

## For device porters and OEM engineers

The main entry point is the **Baga Device Adapter Contract**.

A device port should answer questions like:

```text
What display capabilities are actually available?
How are navigation/touch/pen events normalized?
Where is the app-private storage sandbox?
How does sleep/wake behave?
What power/network/light/audio capabilities exist?
Which Device Profile / Quirk Set is active?
Which Contract Tests and BICTS results prove the combination?
```

It should not leak vendor implementation details into portable apps.

Start with:

- [Device Adapter Contract](docs/en/standards/07_baga-ink-device-adapter-specification.md)
- [BICTS](docs/en/standards/10_baga-ink-compatibility-test-suite.md)
- [Kindle Adapter](docs/en/standards/11_baga-ink-kindle-adapter.md)
- [Android E-Paper Adapter](docs/en/standards/12_baga-ink-android-e-paper-adapter.md)

---

## Project status

> **Early development / Standards + executable conformance + reference-platform implementation preparation.**

Already established:

- full bilingual public Standards 00–13 and 20–28;
- Device Adapter Contract and family standards;
- distribution/signing/repository executable-conformance foundations;
- Python reference verification work;
- Device Adapter executable IDL/SDK design;
- full Kindle Implementation Architecture Freeze;
- governed Kindle Task Design / Execution Prompt workflow;
- protected `main` with required CI guards;
- permanent English / Simplified Chinese public documentation trees.

Still in progress:

- machine-readable Device Adapter IDL and generated interfaces;
- Mock/Headless Adapter and reusable Contract Test harness;
- real Kindle Platform / Device Adapter product implementation;
- real-device BICTS evidence;
- Android E-Paper reference implementation;
- Baga Ink Client / Market products;
- Stable standards releases.

**This repository is an active platform/standards implementation project, not yet an end-user installer release.**

---

## Where to start

### Understand the platform
[English Documentation](docs/en/00_baga-ink-documentation-index.md) · [简体中文文档](docs/zh-CN/00_项目文档入口.md)

### Build a Baga app
Read the App Standard, API Specification, Capability Registry, Permission Model, IKP Package Specification, and Standard Libraries specification.

### Port Baga to a device
Read Standard 07, the relevant device-family standard, Design 02, and BICTS.

### Work on Kindle
Read the Kindle Device Adapter Standard, the [Kindle Implementation Architecture Freeze](docs/en/reference-apps/03_baga-ink-kindle-implementation-architecture-freeze.md), and the engineering plan under [`docs/plans/platform-ports/kindle/`](docs/plans/platform-ports/kindle/).

### Contribute
Read [`CONTRIBUTING.md`](CONTRIBUTING.md). AI/automation contributors must also follow [`AGENTS.md`](AGENTS.md).

---

## Repository map

```text
docs/en/        English public documentation
docs/zh-CN/     Simplified Chinese public documentation
docs/plans/     engineering plans and device-port execution material

spec/           machine-readable schemas, vectors, protocol artifacts
reference/      reference / independent implementations
tests/          conformance, negative, interoperability, regression tests
tools/          repository and specification tooling
.github/        CI and conformance workflows

platform/       Platform implementation area
sdk/            generated/platform SDK area
client/         Baga Ink Client implementation area
```

The long-term source of truth is `main`: code + machine-readable specs + tests + approved public docs.

---

## Roadmap

```text
Standards & executable conformance
        ↓
Machine-readable Device Adapter Contract + SDK
        ↓
Mock Adapter + reusable Contract Tests
        ↓
Kindle reference platform / adapter + Probe IKP
        ↓
LifeBook on real Kindle
        ↓
Android E-Paper reference port
        ↓
Client / Market / broader device ecosystem
```

Compatibility expands by **Native Build Target + Device Profile + Quirk Set + test evidence**, not by copying the application codebase for every device.

---

## Licensing

Baga Ink is developed in public and welcomes personal, educational, research, hobby, and other community use.

Baga-authored Platform/OEM-side software uses the repository's community license unless a file or directory explicitly says otherwise. Commercial OEM/device/platform deployment, preinstallation, shipment, or commercial redistribution requires a separate commercial agreement.

**Ordinary IKP App developers are treated differently from OEMs:** building and selling an App that targets the published Baga App APIs does not by itself require an OEM/platform commercial license.

The production **LifeBook** application is a proprietary first-party product and is not part of the public Baga Platform source distribution.

Third-party components such as KOReader, koreader-base, FBInk, KPM, and KindleTool retain their original upstream licenses.

Details:

- [`LICENSE`](LICENSE)
- [Baga Ink Licensing Policy](docs/en/governance/02_baga-ink-licensing-policy.md)
- [`COMMERCIAL_LICENSE.md`](COMMERCIAL_LICENSE.md)
- [`LICENSE_HISTORY.md`](LICENSE_HISTORY.md)
- [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md)

---

## Contributing

Contributions are welcome in protocol/specification review, Rust/C/C++/Kotlin/Lua/Python tooling, e-paper device ports, conformance tests, security/distribution infrastructure, OEM compatibility research, documentation, and translation.

Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) before opening a substantial change.

---

## Documentation languages

The public documentation model is designed to scale beyond two languages without creating different protocols per locale.

Currently maintained README languages:

- **English** — this file
- [简体中文](README.zh-CN.md)

Future translations can add `README.ja.md`, `README.de.md`, `README.fr.md`, and corresponding locale trees through the localization governance process.

---

<div align="center">

**Baga Ink: one portable application contract, many e-paper devices.**

</div>
