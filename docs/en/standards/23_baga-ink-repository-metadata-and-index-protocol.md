# Baga Ink Repository Metadata and Index Protocol

> **Document level:** Distribution Wire / Repository Security Protocol  
> **Document ID:** `standards.23`  
> **Locale:** English (`en`)  
> **Status:** Draft v0.1  
> **Date:** 2026-08-22  
> **Parent:** `docs/en/standards/20_baga-ink-market-and-distribution-architecture.md`  
> **Related:** Standards 21, 22, 25, 26  
> **Counterpart:** `docs/zh-CN/standards/23_仓库元数据与索引协议.md`

---

## 0. Purpose

This document defines the Baga Ink Repository trust root, signed metadata roles, repository layout, target descriptions, version/expiration rules, content addressing, client verification order, third-party repositories, mirrors, offline snapshots, and low-bandwidth catalog indexing.

Baga Ink does not invent a repository-update cryptographic model.

v0.1 adopts:

> **A constrained TUF 1.0.x Repository Profile.**

Unless this profile explicitly changes a behavior, Root / Targets / Snapshot / Timestamp role semantics and client update order follow TUF.

An implementation MUST pass the applicable TUF conformance behavior plus Baga Ink Repository tests before claiming full compatibility.

---

## 1. Protocol goals

Repository Protocol protects:

```text
Repository identity
current repository state
package digest and length
Release Record
Publisher Identity references
Channel / release status
Catalog / asset integrity
metadata consistency
rollback resistance
freeze detection
mirror / CDN substitution
offline transfer integrity
```

It does not replace IKP Publisher Signature.

```text
Repository Metadata
→ proves what the repository currently distributes

Publisher Signature
→ proves who authorized the IKP
```

The device verifies both.

---

## 2. Repository Identity

Every repository MUST have an independent `repository_id`.

Recommended derivation:

```text
repository_id
=
"repo1_" + base32lower(SHA-256(canonical_root_v1_signed_body))
```

After Root v1 is published, Repository ID does not change.

Repository URL, domain, mirror, and CDN MAY change without changing Repository Identity.

When a device trusts a Repository, it stores at least:

```text
repository_id
trusted_root_version
trusted_root_digest
root key set
highest trusted role versions
last_trusted_time_floor
```

---

## 3. Required top-level roles

v0.1 MUST implement the four TUF top-level roles:

```text
Root
Targets
Snapshot
Timestamp
```

### 3.1 Root

Root defines:

- Repository ID;
- Root / Targets / Snapshot / Timestamp Public Keys;
- Signature Threshold for each role;
- Metadata Format / Spec Version;
- `consistent_snapshot`;
- Root Version and Expiration.

Root Private Keys MUST be offline or equivalently protected.

Recommended official Market root:

```text
Root Threshold: 2-of-3
```

A small independent repository MAY use 1-of-1, but that weaker compromise resilience should be explicit.

### 3.2 Targets

Targets may list trusted downloadable objects such as:

```text
IKP packages
Release Records
Publisher Identity documents
App Ownership / Delegation documents
Catalog indexes / diffs
Catalog app records
Asset descriptors
Withdrawal / Revocation records
Review Attestations
Transparency checkpoints
```

Every target MUST include:

```text
path
length
sha256
optional custom metadata
```

### 3.3 Snapshot

Snapshot pins a coherent view of Targets Metadata.

For each referenced metadata file it records:

```text
metadata path
metadata version
metadata length
metadata sha256
```

Snapshot prevents an attacker from mixing new and old Targets Metadata.

### 3.4 Timestamp

Timestamp is the smallest and most frequently refreshed metadata.

At minimum it describes the current Snapshot:

```text
snapshot version
snapshot length
snapshot sha256
expiration
generated_at
```

An online client verifies Timestamp first.

---

## 4. Root Metadata Profile

Conceptual form:

```json
{
  "signatures": [],
  "signed": {
    "_type": "root",
    "spec_version": "1.0.x",
    "baga_repository_profile": "0.1",
    "repository_id": "repo1_...",
    "version": 3,
    "expires": "2028-01-01T00:00:00Z",
    "consistent_snapshot": true,
    "keys": {},
    "roles": {
      "root": {"keyids": [], "threshold": 2},
      "targets": {"keyids": [], "threshold": 1},
      "snapshot": {"keyids": [], "threshold": 1},
      "timestamp": {"keyids": [], "threshold": 1}
    }
  }
}
```

Requirements:

- `consistent_snapshot` MUST be `true`;
- Root Version begins at 1 and increases monotonically;
- historical Root versions MUST remain retrievable;
- Root updates are verified sequentially;
- a new Root MUST satisfy both old-Root and new-Root Threshold rules;
- Repository ID MUST match the value derived from Root v1.

---

## 5. Consistent Snapshot

Baga Ink Repository MUST use consistent snapshots.

Versioned metadata examples:

```text
<version>.snapshot.json
<version>.targets.json
<version>.<delegated-role>.json
```

Immutable targets use content-addressed paths, for example:

```text
packages/sha256/ab/abcdef...1234.ikp
releases/sha256/12/123456...abcd.json
catalog/sha256/34/345678...abcd.json
assets/sha256/56/567890...abcd.png
```

Publishing a new repository state MUST NOT mutate historical immutable targets.

This prevents clients from observing a half-new / half-old publication state.

---

## 6. Recommended layout

```text
repository/
├── metadata/
│   ├── root.json
│   ├── 1.root.json
│   ├── 2.root.json
│   ├── timestamp.json
│   ├── <version>.snapshot.json
│   ├── <version>.targets.json
│   └── delegated/
│       └── <version>.<role>.json
│
└── targets/
    ├── packages/sha256/
    ├── releases/sha256/
    ├── publishers/sha256/
    ├── catalog/sha256/
    ├── assets/sha256/
    ├── revocations/sha256/
    └── attestations/sha256/
```

`root.json` MAY be a convenience alias to the latest root, but client Root update MUST walk `N.root.json` sequentially.

---

## 7. Release Record target

Every formal IKP Release MUST have an immutable Release Record.

```json
{
  "type": "baga.release",
  "format": "0.1",
  "app_id": "com.example.reader",
  "publisher_id": "pub1_...",
  "version_name": "1.4.2",
  "release_sequence": 142,
  "channel": "stable",
  "published_at": "...",
  "package": {
    "path": "packages/sha256/ab/abcdef...1234.ikp",
    "length": 2837461,
    "sha256": "abcdef...1234"
  },
  "publisher_identity_digest": "sha256:...",
  "app_ownership_digest": "sha256:...",
  "app_key_delegation_digest": "sha256:...",
  "baga_api": {
    "min": "0.1",
    "max_exclusive": "1.0"
  },
  "capabilities": {
    "required": [],
    "optional": []
  },
  "permissions": [],
  "data_schema_version": 1,
  "update_policy": {},
  "status": "active"
}
```

The Release Record is a Repository target and is protected by Repository Metadata.

It does not replace the Publisher Release Signature inside the IKP; the two MUST cross-check consistently.

---

## 8. Targets custom metadata

A Targets entry MAY carry lightweight custom metadata for fast filtering:

```json
{
  "length": 2837461,
  "hashes": {"sha256": "..."},
  "custom": {
    "kind": "ikp-package",
    "app_id": "com.example.reader",
    "publisher_id": "pub1_...",
    "release_sequence": 142,
    "channel": "stable",
    "release_record": "releases/sha256/...json"
  }
}
```

A client MUST NOT use Custom Metadata as a reason to skip Release Record or Publisher Signature validation.

Custom Metadata is an indexing optimization, not a new trust root.

---

## 9. Delegated Targets

v0.1 clients MUST support:

```text
Top-level Targets
+
optional one-level Delegated Targets
```

An official Market MAY shard by App ID hash prefix:

```text
apps-00
apps-01
...
apps-ff
```

or by content kind:

```text
packages
catalog
revocations
attestations
```

Rules:

- Delegation path/hash-prefix scopes MUST NOT be ambiguously overlapping;
- Terminating Delegation behavior MUST be explicit;
- a Delegation Key cannot expand beyond the parent's authorized scope;
- maximum delegation depth in v0.1 is 1;
- deeper delegation requires a later Baga Repository Profile.

Publisher Signature already provides application publisher identity, so v0.1 does not require every Publisher Key to become a TUF delegated role.

---

## 10. Metadata versions and rollback protection

A client stores highest trusted versions per Repository:

```text
root_version
snapshot_version
targets_version
delegated_role_versions
timestamp_version
```

It MUST reject:

- metadata below the locally trusted version;
- same Version with different Digest;
- Timestamp referring to an older Snapshot;
- Snapshot referring to older Targets;
- an automatic update whose Release Sequence is below the installed Release;
- same Release Sequence with a different Digest.

Explicit Downgrade is handled by Standard 25 and MUST NOT be implemented by simply accepting old metadata.

---

## 11. Expiration and freeze detection

All top-level Metadata MUST have Expiration.

Recommended relative cadence:

```text
Timestamp expiration  shortest
Snapshot expiration   longer
Targets expiration    longer
Root expiration       longest
```

Exact durations are Repository Policy, not hard-coded in v0.1.

Expired metadata:

- MUST NOT be used to discover/install a new Release;
- does not disable already-installed Apps;
- should show that repository state requires refresh;
- allows offline devices to keep using existing Apps;
- MUST NOT be used as a remote kill switch for all installed software.

---

## 12. Trusted Time Floor

Kindle and long-offline devices may have unreliable clocks.

Baga Ink therefore persists:

```text
last_trusted_time_floor
```

Timestamp Metadata additionally contains signed:

```text
generated_at
```

After successful Timestamp verification:

```text
last_trusted_time_floor
=
max(previous_floor, verified_generated_at)
```

Expiration uses:

```text
Effective Time
=
max(last_trusted_time_floor, reliable_local_clock)
```

If no reliable local clock exists, the client can still prevent time rollback but cannot prove freshness indefinitely.

In that state:

- installed Apps continue to run;
- new install/update pauses;
- a new signed Timestamp or offline repository snapshot can restore freshness evidence;
- manually setting the device clock backward cannot reduce the trusted time floor.

The Baga Ink Client's ordinary host clock is not itself a trust root; it must transport Repository-signed time evidence.

---

## 13. Metadata client verification order

Repository update MUST follow:

```text
1. load locally trusted Root
2. fetch sequential newer Root versions
3. verify each Root using old + new thresholds
4. fetch Timestamp
5. verify Timestamp signature, version, expiration, Snapshot descriptor
6. fetch versioned Snapshot
7. verify Snapshot length, hash, version, expiration, signature
8. fetch required versioned Targets / Delegated Targets
9. verify Targets against Snapshot
10. resolve target path
11. fetch target within declared length limit
12. verify target length + SHA-256
13. atomically persist new trusted metadata
```

If any step fails:

- do not replace local trusted state;
- do not execute the target;
- allow future retry;
- do not leave the Repository state half-updated.

---

## 14. Target download

A target fetch MUST:

- use the Metadata-declared path;
- enforce a maximum declared download length;
- compute SHA-256 while streaming;
- compare final length and digest;
- not trust HTTP `Content-Type` as a security signal;
- not use redirect destination domain as identity proof;
- not use HTTP ETag as the cryptographic digest;
- write only to staging before verification completes.

HTTPS is the default transport for privacy and server authentication, but integrity ultimately relies on signed Metadata and cryptographic digests.

---

## 15. Mirrors and CDN

A mirror/CDN MAY host:

```text
metadata copies
IKP blobs
Release Records
Catalog files
assets
```

It does not hold Root Private Keys and does not decide the trusted current release.

If Root Trust, metadata signatures, and target digest/length all verify, mirrors can be added/replaced/selected by region without changing trust identity.

Credentials MUST NOT be forwarded across host redirects unless explicitly configured.

---

## 16. Third-party Repository

A third-party Repository MUST implement the same protocol.

Trust enrollment:

```text
Repository URL
      │
      ▼
fetch Root v1 / out-of-band Root
      │
      ▼
display repository_id + Root Fingerprint
      │
      ▼
user confirms trust
      │
      ▼
persist Root Trust
```

Matching URL is not sufficient to replace Root Trust.

An app from a third-party Repository MUST NOT overwrite an installed app with the same App ID but a different Publisher ID.

Official Market review badges cannot be self-declared by third-party repositories.

---

## 17. Repository Source Pinning

After first install the device stores `source_repository_id`.

Automatic updates default to:

- same Repository ID;
- a mirror under the same Root Trust;
- or an explicitly approved Source Migration.

Source Migration revalidates:

```text
Publisher Identity
App Transfer Chain (if any)
Release Sequence
Permission Diff
Repository Root Trust
```

A Repository URL change with unchanged Repository ID is not a Source Migration.

---

## 18. Catalog index and diff

Catalog product indexes are ordinary signed Targets, not top-level TUF Metadata.

Low-bandwidth devices MAY consume:

```text
catalog-entry.json
catalog-index.json
catalog-diff-from-<sequence>.json
```

Each Catalog object has:

```text
length
sha256
catalog_sequence
base_sequence (for diff)
```

A client accepts a diff only when:

- Base Sequence matches local state;
- Diff target digest verifies;
- applying the diff produces the expected new Catalog digest.

Otherwise it downloads the complete Catalog.

---

## 19. Revocation and Withdrawal targets

Withdrawal / Revocation records are immutable Targets referenced by current Repository Metadata.

Example:

```json
{
  "type": "baga.release-status",
  "format": "0.1",
  "app_id": "...",
  "release_sequence": 142,
  "package_sha256": "...",
  "status": "security-revoked",
  "severity": "critical",
  "reason_code": "publisher-key-compromise",
  "effective_at": "...",
  "replacement_release_sequence": 143
}
```

Device behavior is defined by Standard 25.

A Repository MUST NOT erase history merely by deleting old Target files. Archive repositories may retain historical releases; current Targets determine whether new installation is allowed.

---

## 20. Offline Repository Snapshot

Offline transfer carries a self-consistent Repository Snapshot:

```text
Trusted Root chain
Timestamp
Snapshot
Targets / Delegated Targets
required immutable Targets
```

The device runs the same signature, version, expiration, digest, and Publisher checks as online mode.

An offline transport manifest cannot override Repository Metadata.

Standard 26 defines the transfer envelope.

---

## 21. Atomic metadata persistence

Local metadata update MUST:

1. download to temporary storage;
2. finish every signature/hash/version/expiration check;
3. fsync or equivalent durability step;
4. atomically switch Trusted Metadata pointer;
5. retain the previous trusted state until the new state is complete.

After power loss/process termination, recovery must yield:

```text
Old complete state
or
New complete state
```

never a mixed state.

---

## 22. Resource limits

A client MUST apply safe limits for untrusted Repository input, including:

```text
Root metadata max size
Timestamp max size
Snapshot max size
Targets max size
Delegation count
Delegation depth
Target path length
JSON nesting depth
Signature count
Target download length
Catalog diff size
Redirect count
```

Exact values may vary by Platform Compatibility Profile, but safe defaults are mandatory.

Low-memory devices SHOULD support streaming parsing or sharded Targets rather than loading an arbitrarily large Catalog into memory.

---

## 23. Repository Key Rotation

Timestamp / Snapshot / Targets keys are rotated through new Root Metadata.

If an online role key is compromised:

1. generate a new Root version;
2. sign it with the Root Threshold;
3. replace affected role keys;
4. increment metadata versions;
5. after Root update, discard caches that a compromised key might have maliciously fast-forwarded;
6. re-fetch a complete trusted chain.

Compromise of the Root Threshold itself requires out-of-band recovery and is not automatically solved by ordinary network update.

---

## 24. Baga Ink TUF Profile boundary

v0.1 fixes:

```text
TUF 1.0.x role semantics
four required top-level roles
consistent snapshots required
SHA-256 target hashes required
canonical JSON metadata
one-level target delegations supported
Baga generated_at time-floor extension required
```

v0.1 does not define:

- unbounded multi-level Delegation;
- custom cryptographic algorithms;
- per-device personalized Targets;
- a separate Director Repository for every device;
- software-license/payment receipts;
- remote device-control commands.

---

## 25. Final rule

> **Repository URL may change, servers may disappear, and mirrors may be replaced; Repository Identity, Metadata Version, Target Digest, and Publisher Identity cannot be silently rewritten.**

A client accepts only repository state that verifies completely from its locally Trusted Root to the final IKP target.
