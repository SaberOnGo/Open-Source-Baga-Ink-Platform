<div align="center">

# Baga Ink Platform

### One open application platform for e-paper devices

**Build an app against one stable platform API. Port the platform to each e-paper device family — instead of rewriting every app for every device.**

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](LICENSE)
[![Project status](https://img.shields.io/badge/status-early%20development-orange.svg)](#project-status)
[![Documentation](https://img.shields.io/badge/docs-English-2ea44f.svg)](docs/en/00_baga-ink-documentation-index.md)

<!-- BAGA-LANG-SWITCH:START -->
**Languages:** **English** · [简体中文](README.zh-CN.md) · [＋ Add a language](CONTRIBUTING.md#translations)
<!-- BAGA-LANG-SWITCH:END -->

</div>

---

## What is Baga Ink?

**Baga Ink is an open application platform and compatibility standard for e-paper devices.**

Today, an app written for one e-reader usually cannot simply run on another. Kindle homebrew, Android e-paper devices, vendor SDKs, Linux-based readers, different screen refresh mechanisms, input stacks, packaging systems, lifecycle rules, and device quirks all expose different interfaces.

Baga Ink moves those differences **out of applications** and into reusable **Platform Ports / Device Adapters**.

The goal is simple:

> **An application should target Baga Ink — not a particular Kindle model, Android vendor, framebuffer API, or proprietary e-paper SDK.**

Think of Baga Ink as a portable **application platform + device compatibility layer + conformance standard** for e-paper hardware. It is **not a replacement operating system**.

---

## The problem we want to solve

The e-paper ecosystem has great hardware, but application development is fragmented.

| Today | Baga Ink direction |
|---|---|
| Apps contain device/model-specific branches | Device differences live behind a stable Device Adapter Contract |
| Every platform exposes different refresh and input APIs | Apps use stable Baga Ink display/input semantics |
| Packaging and installation differ by device | Portable Baga app packages use the `.ikp` format |
| Compatibility is often based on guesswork | Compatibility is backed by capabilities, contract tests, and BICTS |
| Developers repeatedly rebuild low-level device support | Ports reuse mature OS, vendor, homebrew, and open-source mechanisms |
| An app port becomes tied to one product family | The same app contract can target Kindle, Android E-Paper, and future ports |

The long-term user experience we are aiming for is equally simple: **supported e-paper devices should be able to run a shared ecosystem of Baga Ink apps without each app becoming a separate device-porting project.**

---

## How it works

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

An app should not need code like:

```text
if Kindle Paperwhite ...
if BOOX ...
if iReader ...
if firmware >= ...
```

Those differences belong in the platform port, Device Profile, and Quirk Set — not in portable application logic.

---

## What Baga Ink includes

Baga Ink is more than a single library. The project is defining an interoperable ecosystem:

### Baga Ink Platform
The device-side platform that hosts portable Baga applications, provides the Baga Ink API, manages app lifecycle and permissions, and connects apps to the device through the Device Adapter Contract.

### Baga Device Adapter Contract
A stable porting contract for display, input, storage, lifecycle, power, and optional device capabilities. The contract defines **what a device port must provide**, not that Baga must reimplement the device from scratch.

### IKP application package
A portable Baga application package (`.ikp`). Native device installation packages and Baga application packages are deliberately separate concepts.

### Baga Ink Compatibility / BICTS
Machine-checkable compatibility and conformance testing so a device/firmware/platform combination can be validated instead of merely assumed to work.

### Baga Ink Client
A planned desktop-side client for device detection, installation/bootstrap flows, offline transfer, diagnostics, and app delivery where a device cannot provide a modern app-store experience itself.

### Baga Ink Market and distribution protocols
Open specifications for app identity, signing, repository metadata, updates, rollback, revocation, discovery, transparency, and offline transfer.

### Reference applications
**LifeBook** is the flagship/reference app used to prove that a real application can remain portable while Baga absorbs Kindle, Android E-Paper, and future device differences underneath it.

---

## First reference platform: Kindle

Kindle is the first major reference port because it is an unusually demanding test of the architecture: many generations of hardware, different firmware generations, limited resources, homebrew installation constraints, and e-paper-specific display behavior.

The Kindle strategy is **not** to rewrite Kindle support from zero. Baga intends to stand on mature mechanisms from projects and ecosystems such as:

- KOReader / koreader-base
- FBInk
- Kindle OS mechanisms
- validated Kindle homebrew tooling

The Kindle Device Adapter should remain a relatively thin layer of capability detection, normalization, profiles, quirks, error mapping, and tests wherever mature lower-level mechanisms already exist.

The user-facing goal is eventually:

```text
Kindle Home
    ↓
Baga app (for example LifeBook)
```

while the jailbreak, packaging, KOReader-derived internals, KPM/MRPI, and other device-specific machinery remain implementation details below the app contract.

---

## Android E-Paper and future devices

Baga Ink is **not a Kindle-only project**.

The same Device Adapter Contract is intended to support Android e-paper devices and future ports. On Android, a generic adapter can provide the common baseline while vendor-specific adapters specialize only the e-paper features that genuinely differ, such as refresh modes, pen behavior, front light control, or vendor APIs.

Future ports should not require forking the application ecosystem.

---

## Design principles

1. **Portable apps, device-specific ports**  
   Keep model, firmware, and vendor conditionals below the public application API.

2. **Contract heavy, adapter light**  
   Make the compatibility contract strict and testable while keeping individual adapters as thin as the underlying platform allows.

3. **Reuse mature components**  
   Prefer proven OS, vendor, homebrew, and open-source mechanisms over building another framebuffer stack, reader engine, network stack, or power manager.

4. **Executable standards**  
   Important protocol behavior should be backed by schemas, canonical vectors, reference implementations, negative fixtures, and conformance tests — not Markdown alone.

5. **Offline and low-resource friendly**  
   E-paper hardware often has limited CPU, memory, power, storage, and intermittent networking. The platform must be designed for that reality.

6. **No private device APIs in portable apps**  
   A portable `.ikp` app should not import Kindle internals, Android vendor objects, KOReader private APIs, or raw device SDK types.

7. **Open ecosystem, measurable compatibility**  
   OEMs and community porters should be able to implement the same contract and prove compatibility with the same tests.

---

## What Baga Ink is *not*

Baga Ink is **not**:

- a new e-reader operating system;
- a fork of KOReader presented as a new platform;
- a requirement to replace Android or Kindle OS;
- a universal hardware driver rewrite;
- a claim that every Kindle or Android e-reader is already supported;
- production-ready software today.

It is a standards-driven platform project building the layer **between portable apps and fragmented e-paper device environments**.

---

## Project status

> **Early development / standards and reference-implementation stage.**

The repository already contains a substantial Draft/Baseline standards system, executable distribution-security conformance work, the Device Adapter Contract, Kindle/Android E-Paper adapter specifications, and a frozen Kindle reference architecture.

Work still in progress includes, among other things:

- machine-readable Device Adapter IDL and generated SDK interfaces;
- Mock/Headless Adapter and reusable Adapter Contract Tests;
- real Kindle Platform / Device Adapter implementation;
- real-device BICTS evidence;
- Android E-Paper reference implementation;
- Baga Ink Client and Market products;
- completion of the multilingual public documentation migration;
- Stable standards releases.

**This repository should currently be treated as an active platform/standards implementation project, not as an end-user installer release.**

---

## Where to start

### I want to understand the platform
Start with the [English documentation index](docs/en/00_baga-ink-documentation-index.md) or the [简体中文文档入口](docs/zh-CN/00_项目文档入口.md).

### I want to build a Baga app
Follow the App Standard, API, Capability, Permission, and IKP specifications. The English standards are currently being migrated; migration state is tracked explicitly rather than presenting incomplete translations as finished standards.

### I want to port Baga to a device / OEM platform
The key contract is the **Baga Device Adapter Contract**, followed by the relevant device-family adapter specification and compatibility test suite.

### I want to work on Kindle
Read the Kindle Device Adapter standard, the Kindle implementation architecture freeze, and the Kindle implementation plan. Kindle engineering tasks are maintained under [`docs/plans/platform-ports/kindle/`](docs/plans/platform-ports/kindle/).

### I want to contribute code or documentation
Read [`CONTRIBUTING.md`](CONTRIBUTING.md). AI/automation contributors must also follow [`AGENTS.md`](AGENTS.md).

---

## Repository map

```text
docs/en/        English public documentation
docs/zh-CN/     Simplified Chinese public documentation
docs/plans/     engineering plans and device-port execution material

spec/           machine-readable schemas, vectors, and protocol artifacts
reference/      reference / independent implementations
tests/          conformance, negative, interoperability, and regression tests
tools/          repository and specification tooling
.github/        CI and conformance workflows

platform/       future/reference platform implementation area
sdk/            future generated/platform SDK area
client/         future Baga Ink Client implementation area
```

The repository is intentionally moving toward a model where **code + machine-readable specs + tests + approved public docs** can explain the project without requiring access to historical chats or feature branches.

---

## Roadmap

The current engineering direction is roughly:

```text
Standards & executable conformance
        ↓
Machine-readable Device Adapter Contract + SDK
        ↓
Mock Adapter + reusable contract tests
        ↓
Kindle reference platform / adapter + Probe IKP
        ↓
LifeBook reference app on real Kindle
        ↓
Android E-Paper reference port
        ↓
Client / Market / broader device ecosystem
```

Compatibility will expand by **Native Build Target + Device Profile + Quirk Set + test evidence**, not by copying the application codebase for every device.

---

## Licensing

Original Baga Ink project material is licensed under the **Apache License 2.0**, unless a file or directory explicitly states otherwise. See [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE).

Baga Ink intentionally adopts and interoperates with third-party open-source projects. Those projects **retain their own licenses**. Baga's Apache-2.0 license does not relicense KOReader, koreader-base, FBInk, KPM, Kindle homebrew projects, or any other third-party component.

Some components considered for Kindle distributions use strong copyleft licenses (including AGPL/GPL). A concrete binary/source distribution that includes or derives from those components must satisfy their applicable license obligations in addition to the Baga license. See [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

---

## Contributing

Baga Ink is being built as a long-term multi-developer project. Contributions are welcome in areas such as:

- protocol/specification design and review;
- Rust, C/C++, Kotlin/Java, Lua, Python, and tooling;
- e-paper display/input/lifecycle adapters;
- Kindle and Android E-Paper bring-up;
- conformance tests and interoperability tooling;
- security, signing, update, and distribution infrastructure;
- OEM/device compatibility research;
- technical documentation and translation.

Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) before opening a substantial change.

---

## Documentation languages

The public documentation architecture is designed to support many locales without creating different protocols per language.

Currently maintained README languages:

- **English** — this file
- [简体中文](README.zh-CN.md)

Future translations can use files such as `README.ja.md`, `README.de.md`, `README.fr.md`, and corresponding locale documentation trees once a language is adopted by project governance. See the [localization policy](docs/en/governance/01_documentation-internationalization-policy.md) and [translation contribution guide](CONTRIBUTING.md#translations).

---

<div align="center">

**Baga Ink: one portable application contract, many e-paper devices.**

</div>
