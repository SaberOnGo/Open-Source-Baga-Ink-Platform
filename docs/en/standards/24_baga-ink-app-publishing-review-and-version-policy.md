# Baga Ink App Publishing, Review and Version Policy

> **Document level:** Distribution Publishing and Governance Standard  
> **Document ID:** `standards.24`  
> **Locale:** English (`en`)  
> **Status:** Draft v0.2  
> **Date:** 2026-08-23  
> **Parent:** `docs/en/standards/20_baga-ink-market-and-distribution-architecture.md`  
> **Identity:** Standard 21  
> **Signing:** Standard 22  
> **App / libraries:** Standards 02, 03, 13  
> **Counterpart:** `docs/zh-CN/standards/24_应用发布审核与版本政策.md`

---

## 0. Purpose

This document defines application registration, upload, versioning, channels, review, publication, withdrawal, and resubmission rules for Baga Ink Market and compatible third-party repositories.

It separates:

```text
Protocol / identity rules
= who owns the software bytes, which release identity is immutable, how a device verifies safely

Market Policy
= what a marketplace chooses to list, how it reviews, displays, and governs content
```

Repositories MAY use different content policies, but MUST NOT redefine App Identity, IKP Signature, Release Sequence, Permission, Capability, Baga Lua Profile / Standard Library semantics, or Update Safety.

---

## 1. Formal publication objects

A formal publication may include:

```text
Publisher Identity
App Ownership
Signed IKP
Release Record
Repository Metadata Entry
Catalog Metadata
Optional Review Attestation
Optional Build / Source Attestation
```

The Market MUST retain the developer's original Publisher Signature. It MUST NOT re-sign the IKP as Market-owned software.

A Market MAY sign Repository Metadata, Review Attestation, Policy Classification, Withdrawal / Revocation Record, and App Transfer Attestation. These do not replace Publisher Signature.

---

## 2. App registration

Before first formal publication, register:

```text
app_id
publisher_id
app_ownership_digest
primary display name
primary category
contact information
```

An official Market MUST check:

1. App Ownership signature is valid;
2. `app_id` is not already legitimately owned by another Publisher;
3. namespace verification as applicable;
4. the current account may manage this Publisher;
5. App ID does not impersonate Baga Ink, LifeBook, device vendors, or protected names;
6. App ID / visible-name differences are not deceptive.

---

## 3. Dual version fields

Every Release MUST have both:

```text
version_name
release_sequence
```

`version_name` is human-facing. `release_sequence` is the globally monotonically increasing security ordering integer for one `app_id`.

Rules:

- channels do not get independent counters;
- a different Repository does not reset the counter;
- a formally published Sequence can never be reused;
- automatic update compares trusted Release Sequence, not semantic parsing of `version_name`.

---

## 4. Release immutability

A formal release is uniquely defined by:

```text
app_id
release_sequence
package_sha256
```

Once referenced by signed Repository Metadata:

- the same `app_id + release_sequence` MUST permanently reference the same IKP Digest;
- CDN bytes MUST NOT be silently replaced;
- any package-byte change requires a higher Release Sequence;
- Catalog copy MAY be corrected without changing package identity;
- a Release MAY be Withdrawn / Revoked but not rewritten.

Same Sequence with different Digest is a security conflict and MUST be rejected.

---

## 5. Release Channels

v0.x standard channels:

```text
stable
beta
nightly
```

Channel is not App Identity, a Permission boundary, or a separate Release Sequence space.

Users default to Stable. Switching channels must be explicit. Moving from a newer testing-channel release to a lower Stable Sequence is an explicit Downgrade, not an ordinary update.

---

## 6. Pre-publication local validation

Baga Ink SDK MUST provide tooling such as:

```text
baga validate app.ikp
baga inspect app.ikp
baga sign app.ikp
baga verify app.ikp
```

Validation includes at least:

- IKP container/path safety;
- Manifest Schema;
- App ID / Release Sequence / API Range;
- Capability / Permission;
- Baga Lua Profile compliance;
- Standard Library usage from the formal Profile;
- forbidden device-private execution dependencies;
- forbidden arbitrary native dependencies / duplicated runtimes;
- file hashes;
- Publisher Identity / Ownership / Delegation / Release Signature;
- base Catalog fields;
- package/resource limits.

Special rules:

```text
require("lsqlite3")
→ allowed formal Baga Lua Profile Standard Library

baga.data
→ withdrawn API; not a formal dependency

App bundles another native libsqlite3 / lsqlite3 runtime
→ not allowed by default for Universal IKP

Automerge native runtime
→ developer-facing Lua Standard Library is not yet frozen; controlled Platform/official integration follows the adopted-component rules, while an ordinary Universal IKP cannot carry random ABI-specific native binaries
```

---

## 7. Market upload intake

Market intake flow:

```text
Receive bytes
  ↓
Calculate SHA-256 / length
  ↓
Store in isolated quarantine
  ↓
Verify Publisher / IKP
  ↓
Create immutable submission record
```

Submission Record includes at least:

```text
submission_id
app_id
publisher_id
release_sequence
version_name
channel
package_sha256
package_length
submitted_at
submitting_account
publisher_key_id
review_state
```

The bytes of an existing Submission cannot be replaced during review. Changed package bytes require a new Release Sequence.

---

## 8. Review pipeline

### 8.1 Identity and Signature

Verify Publisher Identity, App Ownership, App Signing Key Delegation, Release Signature, Release Sequence, and App Transfer Chain when applicable.

### 8.2 Package Structure and Safety

Verify:

- IKP structure;
- path traversal / zip bomb / duplicate entries;
- forbidden executable dependencies;
- no bundled second Platform / Lua interpreter / Device Adapter;
- no arbitrary native Standard Library runtime conflicting with the Baga Platform;
- Manifest / Release Statement consistency;
- Payload Hashes.

Platform-provided Baga Lua Profile Standard Libraries are not IKP-bundled native dependencies.

### 8.3 API, Standard Libraries and Portability

Verify:

- device/OS/Platform capabilities are obtained only through public `baga.*` APIs;
- formal Baga Lua Profile Standard Libraries may be used directly through their upstream-standard API;
- direct `lsqlite3` / SQLite use is valid Universal App behavior;
- withdrawn `baga.data` is not required;
- device-brand checks are not the core portability mechanism;
- Capability / Permission names are registered;
- no direct Vendor SDK, Shell, Android Context, Kindle private bridge;
- no dependency on random native libraries that merely happen to exist on one device;
- Universal claims match the real implementation.

Review tooling MUST NOT interpret “use only public `baga.*` APIs for device/platform capability” as “formal Standard Libraries are forbidden.”

### 8.4 Compatibility

Run as applicable:

- IKP Validator;
- Baga Lua Profile / Standard Library tests;
- SQLite / `lsqlite3` Profile tests;
- Baga Reference Platform tests;
- Manifest Capability filtering;
- representative Kindle / Android E-Paper reference-device tests;
- sleep/wake, offline start, storage, display, input scenarios.

If the App actually uses Automerge functionality, run the tests relevant to the adopted modules. Automerge is not mandatory for every App.

### 8.5 Permission Review

Review least privilege, agreement between feature and permission explanation, sensitive permission additions, file/note/network/Bluetooth use, and Permission Diff.

An App-private SQLite database does not require an additional user-data permission, but it cannot bypass Library/User-files permission boundaries.

### 8.6 Privacy and Network

Review privacy policy, remote-service domains, account requirements, analytics / crash reporting, AI data upload, undisclosed collection, and embedded secrets/private keys.

### 8.7 E-Paper Quality

Review high-frequency refresh, meaningless animation, background wakeups, offline behavior, non-touch navigation, grayscale behavior, low-end-device degradation, and ghosting risk.

### 8.8 Malware and Abuse

Review malicious network behavior, account theft, Sandbox escape, SQLite VFS/path escape, supply-chain risk, deceptive UI, hidden high-risk logic, and Market Policy violations.

### 8.9 Human Review

Complex privacy, deception, trademark, abuse, or user-harm issues that automated review cannot decide move to human review.

---

## 9. Review workflow states

```text
submitted
validating
under_review
needs_changes
approved
rejected
withdrawn_by_publisher
suspended
security_hold
```

These are Market workflow states, not device-side Release Status.

---

## 10. Review Attestation

After approval, a Market MAY issue a Review Attestation binding at least:

```text
repository_id
app_id
publisher_id
release_sequence
package_sha256
review_policy_version
result
compatibility_labels
reviewed_at
```

It is signed by a Market Review Key, does not replace Publisher Signature, and is not a guarantee that software is bug-free.

---

## 11. Market Policy remains separate from protocol

Market Policy may independently version content classification, privacy, ads, AI content, open-source disclosure, ratings/comments, payment, regional availability, review SLA, trademark rules, etc.

Market Policy MUST NOT rewrite:

- Publisher Identity;
- App Ownership;
- IKP Signature;
- Release Sequence / Package Digest;
- Permission / Capability;
- Baga Lua Profile / Standard Library semantics;
- update identity;
- Repository Metadata verification.

---

## 12. Permission Diff

The Market MUST compute Permission Diff between the current Stable and candidate Release.

New sensitive Permissions must be prominently displayed. Removed Permissions can apply automatically. Permission names come from the formal Registry.

---

## 13. Capability and compatible release selection

A Release declares:

```text
required capabilities
optional capabilities
Baga API range
```

Baga Lua Profile / Standard Library compatibility is defined by the relevant Platform/API Profile and verified through Reference Platform / BICTS; v0.x does not add a separate Manifest field for every Standard Library.

A Market SHOULD distinguish:

```text
Latest overall release
Latest release compatible with this device/platform profile
```

When a newer release is incompatible with an older device, continue offering the latest compatible release and explain the incompatibility reason.

---

## 14. Data Schema and rollback declaration

A Release SHOULD declare:

```json
{
  "data_schema_version": 4,
  "rollback": {
    "mode": "safe",
    "minimum_compatible_schema": 3
  }
}
```

Modes:

```text
safe
snapshot-required
forward-only
```

- `safe` — old release can read current data;
- `snapshot-required` — snapshot App private data before activation;
- `forward-only` — old release cannot safely read migrated data; must be prominently disclosed and restrict automatic rollout.

For SQLite schema migration, review verifies the declared migration/rollback policy. Automerge persistent-format/protocol changes must similarly define compatibility bounds.

---

## 15. Phased rollout

A Market MAY support:

```text
1% → 5% → 20% → 50% → 100%
```

Phased rollout cannot change Package Digest or make one Sequence refer to different packages. It may pause further installation. A Security Release still satisfies all signature and compatibility checks.

---

## 16. Source / build provenance

Catalog SHOULD support:

```text
license
source_repository
source_commit
build_provenance
reproducible_build_status
sbom
```

If an app claims open source / reproducible build, source commit and build attestation must correspond to the published Package Digest.

SBOM SHOULD distinguish:

```text
IKP-bundled dependencies
Platform-provided Standard Libraries
Platform/Adapter implementation dependencies
```

so Platform-provided SQLite/lsqlite3 is not falsely reported as an App-bundled dependency.

---

## 17. Metadata updates are different from package updates

Catalog text, screenshots, localization, categories, support links, privacy notice, and keywords MAY update without changing the IKP.

Catalog updates MUST NOT change:

```text
App ID
Publisher ID
Release Sequence
Package Digest
Permission
Capability
API Range
Data Schema
Publisher Signature
```

---

## 18. Withdrawal and delisting

Publisher MAY request release withdrawal, app unlisting, or stop-new-installs. A Market MAY suspend listing, apply security hold, or reject future submissions.

These actions use explicit state; history MUST NOT be deleted to fabricate the appearance that a release never existed.

---

## 19. Rejection and appeal

Market Policy SHOULD define rejection reason codes, repairable issues, whether a new Release Sequence is required, human escalation, security fast paths, and audit records.

Changing IKP bytes requires a new Release Sequence; catalog-text-only corrections do not.

---

## 20. Third-party Repository

A third-party Repository MAY use a different review policy but MUST:

- preserve real Publisher Identity;
- verify IKP Signature;
- preserve Release immutability;
- not forge official Review Attestation;
- clearly disclose its review level;
- not silently overwrite same-named different-Publisher apps;
- not alter Baga App / API / Standard Library protocol semantics.

---

## 21. Publication loop

```text
Register App ID
  ↓
Verify App Ownership
  ↓
Build IKP
  ↓
Validate API + Lua Profile / Standard Library usage
  ↓
Sign with delegated App Key
  ↓
Upload immutable package
  ↓
Identity / structure / policy / compatibility review
  ↓
Release Record + Review Attestation
  ↓
Atomic Repository Metadata publication
  ↓
Transparency Event
  ↓
Devices discover/install
```

---

## 22. Final rule

> **A Market may decide whether it lists an application, but it cannot change software identity or platform standards. Universal device capability goes through `baga.*`; formal Baga Lua Profile Standard Libraries may be used through mature upstream APIs. Review must understand both boundaries rather than confusing them.**
