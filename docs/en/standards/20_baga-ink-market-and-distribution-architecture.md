# Baga Ink Market and Distribution Architecture

> **Document level:** Distribution Architecture  
> **Document ID:** `standards.20`  
> **Locale:** English (`en`)  
> **Status:** Draft v0.1  
> **Date:** 2026-08-22  
> **Parent standard:** `docs/en/standards/01_baga-ink-platform-strategy.md`  
> **Related standards:** Standards 21–28  
> **Counterpart:** `docs/zh-CN/standards/20_市场与分发总体架构.md`

---

## 0. Purpose

This document defines the complete Baga Ink application distribution architecture from publisher to user device.

It answers:

> **How can a developer deliver a signed IKP safely, audibly, and rollbackably to Kindle and Android E-Paper devices while keeping the ecosystem open and avoiding a new form of fragmentation?**

The distribution layer must support:

- the official Baga Ink Market;
- third-party Baga Ink Repositories;
- direct online installation by a device;
- Baga Ink Client transfer over USB / LAN;
- long-offline devices;
- local sideloading of signed IKPs;
- unsigned test packages in Developer Mode.

Regardless of the transport path, the device MUST perform the same final identity, signature, repository-metadata, compatibility, permission, and installation validation.

---

## 1. Design conclusions

Baga Ink intentionally combines mature security practices rather than copying one platform wholesale:

1. **TUF** — separation of Root / Targets / Snapshot / Timestamp roles, monotonically increasing metadata versions, expiration checks, target hash/length verification, rollback and freeze resistance;
2. **Uptane** — full verification even for offline update, recovery-oriented update behavior, exact hardware/target matching;
3. **Apple Code Signing** — application identity is the combination of a stable identifier and a signing identity, not a display name;
4. **Android APK Signature Scheme v3** — signing-key rotation requires a verifiable continuity chain;
5. **APT / F-Droid** — signed repository indexes, package hashes, third-party repositories, incremental metadata;
6. **OCI / Nix / OSTree** — content-addressing, immutable objects, digest/size verification, offline static deltas;
7. **RAUC / Mender / A/B update systems** — verify before switching, keep the previous known-good version, confirm health, roll back on failure;
8. **Sigstore Rekor** — append-only transparency logging, inclusion proofs, independent monitoring;
9. **Sparkle** — independent publisher signatures, human version vs machine version, channels, staged rollout, full-package fallback after delta failure;
10. **Ubuntu Core Assertions** — signed statements for account, key, application declaration, revision, and policy.

Core rule:

> **Reuse proven security models; do not invent new cryptography. Keep device-side verification narrow and auditable instead of embedding full marketplace business logic into the device.**

---

## 2. Product and protocol are different things

### 2.1 Baga Ink Market

Baga Ink Market is a product visible to users and developers. It may include:

```text
search
categories / recommendations
app detail pages
localized descriptions
screenshots / icons
developer information
review status
install / update entry points
future ratings / comments / payment features
```

### 2.2 Baga Ink Repository Protocol

The Repository Protocol is the open distribution substrate:

```text
repository trust root
signed metadata
publisher identity
IKP digest and size
release records
channels
update state
withdrawal / revocation
catalog indexes and diffs
mirrors / CDN
offline repository snapshots
```

The official Market MUST use this protocol, but the protocol is not exclusive to the official Market.

```text
Baga Ink Repository Protocol
            │
      ┌─────┴────────────┐
      │                  │
Baga Ink Market     Third-party Repository
Official default    Community / OEM / Enterprise
```

A third-party repository MUST NOT redefine IKP, App Standard, API, Capability, or Permission semantics.

---

## 3. Three-layer trust model

Baga Ink distribution verifies three independent trust layers.

### 3.1 Publisher Trust

Proves:

> **This IKP was authorized by the publisher that owns the application identity.**

Built from:

```text
Publisher Identity
Publisher Root Key Set
App Ownership Statement
App Signing Key Delegation
IKP Release Signature
```

### 3.2 Repository Trust

Proves:

> **This release, digest, length, channel, state, and repository decision belong to the current trusted repository state.**

Implemented through a constrained TUF-style role set:

```text
root.json
timestamp.json
snapshot.json
targets.json
```

### 3.3 Local Installed Identity

Proves:

> **An already-installed app can only be replaced by the same continuous identity or by a formally transferred identity.**

The device stores at least:

```text
app_id
publisher_id
publisher_lineage
source_repository_id
current_release_sequence
current_package_digest
current_channel
last_known_good_release
permissions_granted
```

If any trust layer fails, installation or update MUST stop.

---

## 4. Application identity

An application is not identified by its display name alone.

```text
App Identity
=
Application ID
+
Publisher ID
+
Publisher Identity Lineage
```

Two repositories can both contain `com.example.reader`; they may be considered the same application only if Publisher ID and identity lineage are consistent.

A repository MUST NOT overwrite an installed app merely because `app_id` matches.

---

## 5. The Market does not re-sign every app as Baga-owned

A published IKP retains the publisher signature.

```text
Publisher App Signing Key
          │
          ▼
       app.ikp
          │
          ├── Publisher signature
          └── Publisher identity chain

Baga Ink Market
          │
          └── signs repository metadata and review attestations
```

The Market MUST NOT remove the publisher signature and re-sign all applications as if Baga owned them.

This preserves publisher identity across repositories, prevents repositories from impersonating developers, keeps identity independent from Market delisting, and avoids unnecessary lock-in.

Review attestations MAY be added independently, but they do not replace Publisher Signature.

---

## 6. Content addressing and immutable releases

Every formal IKP MUST be identified by SHA-256 digest.

Recommended storage path:

```text
packages/sha256/ab/abcdef...1234.ikp
```

Release Record example:

```json
{
  "sha256": "abcdef...1234",
  "length": 2837461
}
```

The same digest always means the same bytes.

After publication, the tuple:

```text
app_id + release_sequence
```

MUST permanently map to one IKP digest. Changed content requires a new Release Sequence; it may not silently replace old bytes.

Consequences:

- CDN / mirrors need not be trust roots;
- packages naturally deduplicate;
- old versions remain auditable;
- resumable download is possible;
- the output of any delta can still be verified against the complete target digest.

---

## 7. Security metadata and catalog presentation data are separate

### 7.1 Security-critical metadata

Includes:

```text
repository root
role keys and thresholds
release digest and length
release sequence
publisher identity references
channel
withdrawal / revocation state
metadata version and expiration
```

Devices MUST verify these strictly.

### 7.2 Product/catalog data

Includes:

```text
description
screenshots
icons
categories
recommendation text
search keywords
ratings / comments
editorial recommendation
```

Catalog data needs integrity protection but cannot be the sole authority for installation identity or update identity.

A search service may say that a release is installable; the device still returns to signed Repository Metadata for the final decision.

---

## 8. Distribution paths

### 8.1 Direct device online install

```text
Baga Ink Platform
       │
       ├── fetch signed repository metadata
       ├── select compatible release
       ├── download IKP from CDN / mirror
       └── verify and activate locally
```

### 8.2 Baga Ink Client over USB / LAN

```text
Repository
    │
    ▼
Baga Ink Client
    │  courier + management UI
    ▼
Device
    │
    └── performs final verification again
```

The PC/Mac client MAY pre-verify and filter data, but it is not the device's final trust root.

### 8.3 Offline repository snapshot

A Client MAY package:

```text
trusted root
repository metadata chain
required release records
IKP blobs
catalog subset
```

into a portable offline snapshot. Import MUST apply the same version, expiration, digest, publisher, permission, and compatibility checks as online mode.

### 8.4 Local signed IKP sideloading

Without Repository Metadata, an explicit sideload flow MAY:

- verify the IKP Publisher Signature;
- display Publisher ID / fingerprint;
- require the user to establish or confirm local trust;
- avoid implying Baga Market review approval;
- pin future updates to the same Publisher Identity by default.

### 8.5 Unsigned developer packages

Allowed only in Developer Mode:

- explicitly enabled by the user;
- visibly warned by both Client and device;
- never presented as a Market install;
- MUST NOT overwrite a formally signed app unless the user explicitly clears prior identity and acknowledges risk.

---

## 9. Third-party repositories and source pinning

Every Repository has an independent:

```text
repository_id
root metadata
root fingerprint
metadata version state
```

The official Market root MAY be preinstalled with the Platform.

Adding a third-party Repository MUST:

- show repository name and Root Fingerprint;
- require explicit user confirmation;
- persist local Repository Trust;
- not treat a matching URL as a matching Root Identity;
- rotate Root only through the signed root chain.

The first install records:

```text
source_repository_id
```

Automatic update defaults to that repository or a mirror under the same Root Trust.

Cross-repository migration requires all of:

1. same Publisher Identity or a valid App Transfer Chain;
2. explicit user approval for source change;
3. valid Release Sequence and security state in the new repository;
4. no weakening of existing identity/permission protection.

---

## 10. Threat model

The distribution architecture must account for at least:

```text
compromised CDN / mirror
compromised repository web server
replay of old valid metadata
mixing old and new metadata
serving an old IKP as a new release
compromised Market account
stolen App Signing Key
lost/stolen Publisher Root Key
third-party repository App ID collision
malware on USB / PC transfer path
interrupted download / storage exhaustion
app fails after update
silent permission expansion
malicious withdrawal / remote-delete controversy
inaccurate device clock / long-offline device
```

Design rule:

> **Compromise of any single server, transport path, or account should not immediately grant the ability to forge updates for every application.**

---

## 11. Update and recovery principles

The distribution layer MUST:

- verify before writing to active location;
- use staging;
- atomically switch the current-version pointer;
- retain the previous known-good IKP;
- not delete the old version until the new version is healthy;
- preserve user data on update failure;
- fall back to full IKP when delta application fails;
- never silently approve newly added sensitive permissions;
- distinguish explicit downgrade from automatic rollback;
- not equate Security Revocation with default silent remote uninstall.

The exact state machine is defined by Standard 25.

---

## 12. Transparency-log role

Transparency events include:

```text
Publisher creation
App ID registration
App Ownership change
Signing Key Delegation
Publisher Root Rotation
Emergency Recovery
Release Publish
App Transfer
Version Withdrawal
Security Revocation
Review Attestation
```

The transparency log is **audit evidence**, not the device's sole install trust root.

A v0.1 device MAY install without querying the log online; Market, publishers, and independent monitors must still be able to verify append-only behavior and inclusion of events.

---

## 13. Component responsibilities

### Baga Ink Developers

- account/team management;
- Publisher Identity creation/display;
- App ID registration;
- release upload;
- review feedback;
- key rotation / recovery flows;
- transparency queries.

### Baga Ink Market Server

- verify Publisher Signature;
- verify App Ownership;
- perform review;
- create Release Record;
- generate signed Repository Metadata;
- publish Catalog;
- issue Withdrawal / Revocation;
- append Transparency events.

### CDN / Mirror

- stores and transports immutable blobs;
- does not decide which release is trusted;
- holds no Publisher Private Key;
- holds no Repository Root Private Key.

### Baga Ink Client

- identify devices;
- fetch/cache/filter repository data;
- provide USB / LAN management;
- show compatibility and permission changes;
- never bypass device final verification.

### Baga Ink Platform

- store Repository Root Trust;
- store Installed Identity;
- verify Repository Metadata;
- verify IKP Publisher Signature;
- re-check Compatibility and Permission;
- perform staged install / atomic switch / rollback;
- keep local audit state required for recovery and diagnosis.

---

## 14. Non-goals for v0.1

This version does not attempt to fully define:

- payment settlement;
- DRM;
- subscription receipts;
- advertising auction;
- comment moderation;
- commercial telemetry systems;
- forcing every third-party repository to adopt official Market policy;
- requiring every device to query Transparency online;
- a complex cross-app dependency resolver.

Future product features MUST NOT weaken Publisher Identity, Repository Trust, or Local Installed Identity.

---

## 15. Distribution standards map

```text
20 Market & Distribution Architecture
│
├── 21 Publisher Identity & App Ownership
├── 22 IKP Signing & Key Lifecycle
├── 23 Repository Metadata & Index Protocol
├── 24 Publishing, Review & Version Policy
├── 25 Update, Rollback & Revocation Protocol
├── 26 Distribution Client & Offline Transfer
├── 27 Transparency & Security Audit
└── 28 Catalog & App Discovery
```

Dependency shape:

```text
Publisher Identity
      │
      ▼
IKP Signature
      │
      ├──────────────┐
      ▼              ▼
Repository       Publishing Review
Metadata             │
      │               ▼
      └────────→ Update / Revocation
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
Distribution Client        Catalog / Discovery
                      │
                      ▼
             Transparency / Audit
```

---

## 16. Research basis

This design draws primarily on TUF, Uptane, Android APK v3 signing, Apple Code Signing, Debian apt-secure, F-Droid, OCI Distribution, OSTree, Mender, RAUC, Sigstore Rekor, Sparkle, Ubuntu Core Assertions, and A/B update practices.

These are design references, not new Baga public runtime layers.

---

## 17. Final rule

> **Publisher proves who released the software; Repository proves what should currently be distributed; local installed state proves what is allowed to replace the installed application.**

Baga Ink installs or updates only when all three trust layers hold.
