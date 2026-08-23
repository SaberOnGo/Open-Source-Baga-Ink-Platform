# IKP Package Specification

> **Document level:** First-level platform standard  
> **Document ID:** `standards.06`  
> **Locale:** English (`en`)  
> **Status:** Draft v0.4  
> **Date:** 2026-08-22  
> **Parent:** `01_baga-ink-platform-strategy.md`  
> **App Standard:** `02_baga-ink-app-standard.md`  
> **Capability / Permission:** Standards 04 / 05  
> **Identity / Signing:** Standards 21 / 22  
> **Publishing / Update:** Standards 24 / 25  
> **Counterpart:** `docs/zh-CN/standards/06_IKP应用包规范.md`

---

## 0. Purpose

This document defines the standard application package format for Baga Ink Universal Apps:

# **IKP / `.ikp`**

IKP is intended to be:

- portable across Kindle and Android E-Paper;
- independent of CPU ABI;
- independent of Android APK packaging;
- independent of Kindle Homebrew directory layout;
- signable;
- verifiable;
- versionable;
- easy to build, inspect, and distribute.

IKP is the carrier of the Baga Ink App Standard. It is not an APK, IPK, KUAL extension, or arbitrary ZIP renamed to `.ikp`.

Most important boundary:

> **IKP carries the App's own Lua code, resources, Manifest, and publisher evidence. A Universal IKP does not carry another Platform Core, Lua interpreter, Device Adapter, or device-private system bridge.**

---

## 1. Authority boundary

This document owns:

```text
.ikp extension
container
path rules
package layout
manifest.json
baseline resource limits
package validation
Platform / IKP boundary
```

Dedicated standards own:

```text
Publisher Identity / App Ownership       → 21
IKP Publisher Signature / Key Lifecycle  → 22
Repository Metadata / Target Digest      → 23
Release Sequence / Review / Channel      → 24
Stage / Activate / Rollback / Revocation → 25
Client / USB / Offline Transfer          → 26
```

If this document conflicts with a more specialized standard in its own domain, the specialized standard governs.

---

## 2. Extension and MIME type

Canonical extension:

```text
.ikp
```

Examples:

```text
lifebook.ikp
rss-reader.ikp
notes.ikp
```

`IKP` is the fixed format name; the project does not require a forced letter-by-letter expansion.

Recommended MIME type:

```text
application/vnd.baga.ikp
```

Extension/MIME are identification hints, not security validation.

---

## 3. Container

IKP v0.4 uses a **ZIP-compatible container**.

Allowed compression methods:

```text
STORE
DEFLATE
```

Reasons:

- mature multi-platform implementations;
- simple developer tooling;
- easy debugging/inspection;
- no need to invent a compression algorithm for the first format generation.

However:

> **Renaming a ZIP file does not make it a valid IKP.**

Platform must validate the Manifest, paths, security limits, Payload hashes, identity/signature chain, and versions.

---

## 4. Path rules

Paths inside IKP:

- MUST be UTF-8;
- MUST use `/` separators;
- MUST be relative;
- MUST NOT escape through `..`;
- MUST NOT be absolute;
- MUST NOT escape package root through symlinks or equivalent archive behavior;
- MUST NOT contain duplicate entries;
- SHOULD avoid case-only duplicate names;
- SHOULD use names all supported target platforms can process reliably;
- MUST be normalized before security decisions.

Validator / Installer MUST defend against Path Traversal / Zip Slip.

---

## 5. Standard package layout

### 5.1 Minimal development IKP

```text
example.ikp
├── manifest.json
└── main.lua
```

Allowed only as Developer Mode input or signing-tool input.

### 5.2 Signed production IKP

```text
example.ikp
├── manifest.json
├── main.lua
├── src/
│   ├── app.lua
│   └── views/
├── assets/
│   ├── icon.png
│   └── images/
├── locales/
│   ├── en.json
│   └── zh-CN.json
└── signature/
    ├── files.json
    ├── publisher-identity.json
    ├── app-ownership.json
    ├── app-key-delegation.json
    ├── release-statement.json
    └── signatures.json
```

The exact meaning of signature artifacts is defined by Standard 22.

### 5.3 Entry point

The Manifest MUST specify an entry file, normally:

```text
main.lua
```

The entry:

- MUST be inside the IKP Payload;
- MUST NOT escape package root;
- MUST NOT point into `signature/`;
- MUST NOT be a native executable;
- MUST be executed only after all required validation succeeds.

---

## 6. `manifest.json`

`manifest.json` MUST be UTF-8 JSON at package root.

Minimal production example:

```json
{
  "ikp_format": "0.4",
  "id": "com.example.reader",
  "name": "Example Reader",
  "version_name": "1.0.0",
  "release_sequence": 1,
  "channel": "stable",
  "entry": "main.lua",
  "baga_api": {
    "min": "0.2",
    "max_exclusive": "1.0"
  },
  "permissions": [],
  "capabilities": {
    "required": [],
    "optional": []
  },
  "data_schema_version": 1,
  "rollback": {
    "mode": "safe",
    "minimum_compatible_schema": 1
  }
}
```

---

## 7. Required Manifest fields

Required:

```text
ikp_format
id
name
version_name
release_sequence
channel
entry
baga_api
permissions
capabilities
data_schema_version
rollback
```

### 7.1 `ikp_format`

Declares IKP schema major/minor. Unsupported format major MUST be rejected.

### 7.2 `id`

Stable Application ID.

It MUST match App Ownership, Release Statement, and Release Record, and MUST NOT vary by device, channel, or repository.

### 7.3 `name`

User-visible display name. It does not define identity.

### 7.4 `version_name`

Human-readable version. It is not the security ordering axis.

### 7.5 `release_sequence`

Monotonically increasing integer governed by Standard 24.

### 7.6 `channel`

Release channel. Initial standard values:

```text
stable
beta
nightly
```

### 7.7 `entry`

Lua application entry file.

### 7.8 `baga_api`

Supported Baga Ink API range. Platform MUST validate it before executing App code.

### 7.9 `permissions`

Permission names MUST come from Standard 05. Runtime requests for undeclared permissions are forbidden.

### 7.10 `capabilities`

Capability names MUST come from Standard 04.

Missing Required Capability means Platform reports Incompatible. Missing Optional Capability requires App fallback behavior.

### 7.11 `data_schema_version` and `rollback`

Used by staged update, data migration, and rollback decisions defined by Standard 25.

---

## 8. Recommended fields

Optional metadata MAY include:

```json
{
  "description": "A minimal Baga Ink reader",
  "publisher_display_name": "Example Studio",
  "homepage": "https://example.com",
  "license": "MIT",
  "source_repository": "https://example.com/source",
  "icon": "assets/icon.png",
  "locales": ["en", "zh-CN"],
  "category": "reader",
  "support": "https://example.com/support"
}
```

These fields may help generate Catalog metadata but do not alter App identity or signing semantics. Standard 28 defines the formal Market catalog surface.

---

## 9. Manifest/signature cross-validation

Platform MUST cross-check Manifest against `signature/release-statement.json`.

At minimum:

```text
app_id
version_name
release_sequence
channel
ikp_format
baga_api
permissions
capabilities
data_schema_version
rollback policy
manifest digest
```

Mismatch MUST cause rejection. Modifying Manifest must not bypass signed Release Statement semantics.

---

## 10. Universal IKP content restrictions

A Universal IKP MUST NOT use device-specific native executables/libraries as normal app business logic.

Forbidden normal dependencies include:

```text
.so
ELF executable
APK payload
DEX
JAR used as system escape
Kindle shell executable
vendor-specific binary blob
```

A Universal IKP MUST NOT carry:

- its own Lua interpreter;
- Kindle-specific Device Bridge;
- Android-specific Device Bridge;
- BOOX/iReader private API wrappers as app execution dependencies;
- a system-call layer that bypasses `baga.*`;
- CPU-ABI-specific primary business binaries;
- another Platform Core;
- a Device Adapter.

The restriction concerns executable/device-private dependencies, not ordinary static assets.

Native Extension / Capability Provider packages require a separate controlled standard and must not masquerade as Universal IKP.

---

## 11. Dependency model

The initial IKP model is self-contained for **application code and resources**.

An App MAY:

- use Baga Ink standard APIs;
- use Platform-provided Standard Libraries;
- bundle pure-Lua third-party libraries;
- bundle its own static resources.

An App MUST NOT:

- require users to install arbitrary native libraries;
- depend on a dynamic library that happens to exist on one device;
- depend on another App's private directory;
- download different private system bridges per device.

v0.4 does not define a cross-App Shared Dependency Resolver.

---

## 12. Payload and `files.json`

Payload means:

> all IKP files except the `signature/` directory.

A signed IKP MUST contain `signature/files.json`.

For every Payload file it records:

```text
path
length
sha256
```

Canonicalization, ordering, hashing, and verification details are defined by Standard 22.

Validator MUST reject:

- missing files;
- undeclared extra Payload;
- duplicate path;
- length mismatch;
- hash mismatch;
- path escape.

---

## 13. Publisher signature chain

A signed IKP establishes:

```text
Publisher Identity
      │
      ▼
App Ownership
      │
      ▼
App Signing Key Delegation
      │
      ▼
IKP Release Signature
      │
      ▼
Payload Files
```

Key IDs, canonical JSON, thresholds, rotation, recovery, and transfer are governed by Standards 21/22.

Market accounts, catalog copy, and Repository URLs cannot replace this cryptographic identity chain.

---

## 14. Repository container digest

When distributed through a Repository, Repository Metadata also protects the exact `.ikp` container:

```text
length
sha256
```

The two validation layers serve different purposes:

```text
Repository Digest
→ protects exact distributed container bytes

Publisher Signature
→ protects App identity and logical Payload
```

Neither replaces the other.

---

## 15. Canonical encoding and deterministic packaging

Signed JSON uses the canonical JSON profile defined by Standard 22.

Baga SDK SHOULD support deterministic IKP construction:

- stable entry order;
- stable timestamp policy;
- stable permission bits;
- stable compression parameters;
- no local absolute paths;
- no random unsigned fields.

Logical Payload verification MUST NOT assume every valid packager produces byte-identical ZIP containers.

---

## 16. Resource and decompression safety

Validator MUST defend against:

- Zip Bomb;
- extreme compression ratio;
- oversized single file;
- oversized total extracted size;
- duplicate entries;
- Path Traversal;
- malicious filenames;
- excessive directory depth;
- oversized JSON;
- excessive signatures;
- excessive Payload file count.

Exact limits are defined by Platform Compatibility Profiles, but safe defaults are mandatory.

---

## 17. Pre-install validation order

Minimum order:

```text
1. validate container type/size
2. validate path safety
3. read Manifest and signature artifacts
4. validate IKP Format
5. validate files.json and complete Payload
6. validate Publisher Identity chain
7. validate App Ownership
8. validate App Signing Key Delegation
9. validate IKP Release Signature
10. cross-check Manifest / Release Statement
11. validate Release Sequence and Revocation
12. validate Baga API / Capability / Permission requirements
13. validate Data Schema / Rollback policy
14. only then enter staged install
```

Repository-origin packages additionally require Repository Metadata and Container Digest validation.

No failure path may execute `main.lua`.

---

## 18. Install, update, rollback

Staged install, atomic activation, health confirmation, automatic rollback, explicit downgrade, Permission Diff, and Data Schema Migration are governed by Standard 25.

This document requires only the package-level invariants:

- App Package and App Data remain separate;
- new package bytes do not overwrite the old release in place;
- no activation before verification completes;
- update failure does not delete user data by default;
- last-known-good IKP can be retained for rollback.

---

## 19. Install location

IKP MUST NOT hard-code physical installation paths.

Apps only see:

```text
own package resources
appdata/
cache/
documents/
downloads/
authorized shared resources
```

Android/Kindle physical paths are implementation details of Platform Core / Device Adapter.

---

## 20. IKP and Baga Lua Profile

A Universal IKP should not maintain permanent per-device entry trees such as:

```text
main-kindle.lua
main-boox.lua
main-ireader.lua
```

Device differences are handled through capabilities and standardized APIs:

```lua
baga.device.has(...)
```

A small Capability branch may alter experience; it must not evolve into vendor-specific business forks.

---

## 21. IKP and Platform relationship

```text
Baga Ink Platform
├── Platform Core
│   ├── Embedded Lua Interpreter
│   ├── Baga Lua Profile
│   ├── Baga Ink API
│   ├── IKP Package Manager
│   └── Device Adapter
│
├── App A.ikp
├── App B.ikp
└── App C.ikp
```

Each IKP supplies only its own application code, resources, and publisher evidence.

Shared platform capability and device adaptation belong to Platform, not Universal IKP.

---

## 22. Android, Kindle, and IKP

Android:

```text
Baga Ink Platform.apk
        │
        ▼
      *.ikp
```

Kindle:

```text
Kindle OS / Homebrew
        │
        ▼
Baga Ink Platform Core
        │
        ▼
      *.ikp
```

Third-party IKPs do not need to understand APK, KUAL, MRPI, framebuffer, or Vendor SDK implementation details.

---

## 23. Developer Mode

Unsigned IKP is allowed only in Developer Mode, governed by Standard 26.

Developer Mode must not:

- overwrite a production-signed App identity silently;
- receive official Market review labels;
- participate in ordinary automatic updates as a trusted production release;
- permanently disable signature verification for the device.

---

## 24. Validator tooling

Baga SDK SHOULD provide commands such as:

```text
baga validate app.ikp
baga inspect app.ikp
baga verify app.ikp
```

Validation includes at least:

- Container;
- Manifest Schema;
- Application ID;
- Release Sequence;
- API Version;
- Capability / Permission names;
- unsafe paths;
- forbidden executable dependencies;
- private interpreter/system bridge/Device Adapter detection;
- Payload Hash;
- Publisher Signature;
- Resource Limits.

---

## 25. LifeBook Reference IKP

LifeBook should be one of the first Reference IKPs used to validate this specification.

Target:

```text
lifebook.ikp
     │
     ├── Kindle
     └── Android E-Paper
```

Official status does not allow LifeBook to bypass the IKP Standard.

---

## 26. Not defined in the first phase

The following remain intentionally unfrozen:

- Shared Dependency Registry;
- Native Extension Package Format;
- Delta Algorithm;
- Paid App Receipt;
- DRM;
- Cloud Backup Format;
- Multi-process App Model.

Standard 25 defines the security boundary around delta updates, but the concrete diff algorithm remains an implementation decision pending evidence.

---

## 27. Core principles

```text
one format: .ikp
one Manifest
one App ID
one global Release Sequence axis
one Baga Ink API
one Capability / Permission Model
application code/resources self-contained
device adaptation does not enter Universal IKP
device-private executables do not enter Universal IKP
shared Platform capabilities are not redundantly bundled per App
Publisher Signature is independently verifiable
Repository Container Digest is independently verifiable
installation is staged, health-checked, and rollback-capable
```

> **The same IKP must become the stable, verifiable, long-lived software distribution unit across Kindle and Android e-paper platforms.**
