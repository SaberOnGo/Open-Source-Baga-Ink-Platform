# Baga Ink Distribution Client and Offline Transfer Protocol

> **Document level:** Distribution Client / Transfer Protocol  
> **Document ID:** `standards.26`  
> **Locale:** English (`en`)  
> **Status:** Draft v0.1  
> **Date:** 2026-08-22  
> **Parent:** `docs/en/standards/20_baga-ink-market-and-distribution-architecture.md`  
> **Repository:** Standard 23  
> **Update:** Standard 25  
> **Counterpart:** `docs/zh-CN/standards/26_分发客户端与离线传输协议.md`

---

## 0. Purpose

This document defines Baga Ink Client and application distribution through direct networking, USB, LAN, local files, and long-offline environments.

Core rule:

> **Baga Ink Client is a device-management tool and courier for trusted data; it is not the final trust root for application identity or repository identity.**

Regardless of which computer, USB drive, network, or mirror carried the package, the Baga Ink Platform on the device MUST perform the same final verification before installation.

---

## 1. Distribution modes

v0.1 defines five modes.

### 1.1 Device Direct

The device directly accesses Repository Metadata and Package Storage.

### 1.2 Managed Transfer

Baga Ink Client obtains Repository data online, then transports it through:

```text
USB
local network
device-specific file bridge
```

### 1.3 Portable Repository Snapshot

Client or management server produces a coherent, portable offline subset of a Repository.

### 1.4 Signed IKP Sideload

The user installs a publisher-signed IKP local file without a complete Repository Metadata chain.

### 1.5 Unsigned Developer Transfer

Unsigned packages used only in Developer Mode.

---

## 2. Trust boundary

### 2.1 Device performs final verification

Client MAY pre-verify:

- Repository Metadata;
- IKP Digest;
- Publisher Signature;
- Compatibility filtering;
- Permission Diff.

The device still MUST independently verify:

```text
Repository Root / Metadata (for Repository install)
Package Length / SHA-256
IKP Publisher Signature
App Identity Continuity
Release Sequence
Revocation Status
API / Capability / Permission
Install State
```

A PC message saying “verified” cannot replace device verification.

### 2.2 Client does not hold highest-authority keys

Baga Ink Client SHOULD NOT hold:

- Repository Root Private Key;
- Publisher Root Private Key;
- Publisher Recovery Private Key;
- Market Review Private Key;
- other publishers' App Signing Private Keys.

Developer signing tools MAY run on the same computer, but that is an explicitly separate developer workflow.

---

## 3. Device Direct flow

```text
Device
  │
  ├── update trusted Repository Metadata
  ├── select latest compatible Release
  ├── display Permission / Compatibility information
  ├── download immutable IKP target
  ├── verify repository digest + publisher signature
  ├── stage
  └── activate according to Update Protocol
```

Direct networking SHOULD support resumable downloads, declared length limits, safe recovery after sleep, low-frequency polling, Wi-Fi/charging policy, Trusted Time Floor, and signed-metadata integrity independent from HTTPS certificates.

---

## 4. Managed Transfer flow

```text
Repository
    │
    ▼
Baga Ink Client
    │
    ├── verify and cache
    ├── identify connected device
    ├── select compatible releases
    └── transfer signed evidence + IKP
    │
    ▼
Baga Ink Platform
    │
    ├── verify again
    ├── stage
    └── activate
```

The device is the final decision-maker.

Client MUST NOT use private commands that tell the device to skip signatures, ignore permissions, or force-activate an unverified package.

---

## 5. Device Handshake

After connection, Client and Platform establish a session.

A device MAY return:

```json
{
  "protocol": "baga-transfer/0.1",
  "device_session_id": "random-session-id",
  "platform_version": "0.1.0",
  "baga_api_version": "0.1",
  "ikp_formats": ["0.2"],
  "capabilities_digest": "sha256:...",
  "compatibility_status": "compatible",
  "free_storage_bytes": 536870912,
  "max_transfer_chunk": 1048576,
  "supported_hashes": ["sha256"],
  "installed_inventory_digest": "sha256:..."
}
```

Rules:

- `device_session_id` is random per session;
- hardware serial number is not required;
- model/firmware facts required for compatibility MAY be exposed in bounded form;
- user account, library contents, and note metadata are not returned by default;
- Client verifies Baga Platform transfer protocol/version, not merely USB Vendor ID.

---

## 6. Device detection and Platform installation route

Client may need to identify devices without Baga Platform installed.

That bootstrap/install decision uses:

```text
Device Model
+
Firmware / OS Version
+
Current installation state
+
Verified installation route record
```

Client displays:

```text
Compatible
Experimental
Unsupported
```

Platform installation and App distribution are separately recorded workflows.

After Platform is installed, IKP distribution follows this protocol regardless of Kindle/Android bootstrap differences.

---

## 7. Transfer Session

Each transfer SHOULD have a Session Manifest:

```json
{
  "type": "baga.transfer-session",
  "format": "0.1",
  "session_id": "...",
  "repository_id": "repo1_...",
  "created_at": "...",
  "items": [
    {
      "kind": "ikp",
      "app_id": "com.example.reader",
      "release_sequence": 142,
      "path": "targets/packages/sha256/...ikp",
      "length": 2837461,
      "sha256": "..."
    }
  ]
}
```

Session Manifest helps with progress, cache, resume, user confirmation, and diagnostics. It is not a security trust root; every item is independently validated through Repository Metadata and/or Publisher Signature.

---

## 8. Chunked Transfer

Large objects MAY be chunked.

Each chunk carries at least:

```text
session_id
item_digest
chunk_offset
chunk_length
chunk_bytes
```

Receiver MUST:

- validate offset/length bounds;
- reject ambiguous overlapping chunks;
- write only to staging;
- track received ranges;
- compute complete target SHA-256 at finish;
- never substitute per-chunk checks for final complete Digest;
- resume after reboot only from a complete transfer Journal.

Optional chunk hashes are error-detection aids, not replacements for the final Repository Target Digest.

---

## 9. Resume

Resume state binds:

```text
repository_id
item_sha256
item_length
release_sequence
session protocol version
```

If any differs, discard the old partial object.

HTTP Range, USB chunks, and LAN resume MUST NOT combine bytes from different releases. On completion, recompute full SHA-256 from beginning to end.

---

## 10. Portable Repository Snapshot

An offline Repository Snapshot is a directory/archive whose logical structure is:

```text
baga-offline-snapshot/
├── transfer-manifest.json
├── metadata/
│   ├── 1.root.json
│   ├── ...
│   ├── timestamp.json
│   ├── <version>.snapshot.json
│   ├── <version>.targets.json
│   └── delegated/
└── targets/
    ├── packages/sha256/
    ├── releases/sha256/
    ├── publishers/sha256/
    ├── revocations/sha256/
    ├── catalog/sha256/
    └── assets/sha256/
```

v0.1 does not freeze a filename extension for the outer container.

`transfer-manifest.json` is an inventory/UX aid. Security still follows:

```text
Trusted Repository Root
→ Timestamp
→ Snapshot
→ Targets
→ Target Digest
→ IKP Publisher Signature
```

---

## 11. Offline Snapshot generation

Client MUST:

1. validate latest Repository Metadata from its Trusted Root;
2. select Releases required by target device/profile;
3. collect the complete Root Update Chain;
4. collect Timestamp, Snapshot, Targets / Delegated Targets;
5. collect Release Records, Publisher documents, Revocation records;
6. collect IKPs and required Catalog/assets;
7. verify every Target Digest;
8. generate Transfer Manifest;
9. leave original Repository Metadata unchanged;
10. write snapshot to a new destination and finalize atomically.

Snapshot may contain a complete repository or a device-specific subset, but a subset still carries the complete metadata chain required to verify its selected targets.

---

## 12. Offline Snapshot import

Device MUST:

1. begin at locally Trusted Root;
2. sequentially verify newer Root versions;
3. verify Timestamp / Snapshot / Targets;
4. reject Metadata Version rollback;
5. evaluate Trusted Time Floor;
6. validate Release Record and Revocation;
7. verify IKP Digest;
8. verify Publisher Identity and Signature;
9. re-check Compatibility / Permission;
10. install according to Standard 25.

The USB drive, PC, or LAN share carrying the snapshot need not itself be trusted.

---

## 13. Trusted Time

Client's ordinary PC system clock is not device Trusted Time.

Online or offline transfer carries Repository Timestamp Metadata with signed `generated_at`.

Only after Timestamp Signature verification may the device advance:

```text
last_trusted_time_floor
```

Client MAY warn that the host clock seems wrong, but MUST NOT bypass Metadata Expiration using an unsigned date.

---

## 14. Signed IKP Sideload

```text
No Repository Metadata
        │
        ▼
Verify Publisher Signature
        │
        ▼
Display App ID / Publisher ID / Fingerprint
        │
        ▼
Check against installed identity
        │
        ▼
User confirms trust + permissions
        │
        ▼
Stage and activate
```

Sideload UI MUST disclose:

- source is a local file;
- no official Market review when no Attestation exists;
- Publisher ID;
- App ID;
- key fingerprint;
- permissions;
- API / Capability compatibility;
- whether an installed application would be replaced.

Trusting one local-file Publisher MUST NOT automatically trust other Publishers in the same directory.

---

## 15. Developer Mode

Developer Mode requires explicit user enablement.

Unsigned IKPs:

- install only under development namespace / distinct development identity;
- MUST NOT overwrite formal installations;
- show persistent development marking;
- MAY have short retention/expiration;
- cannot participate in ordinary automatic update;
- cannot display official review labels;
- should support one-action removal of all developer packages without affecting formal App data.

For upgrade testing, prefer a local test Publisher Key instead of permanently disabling signatures.

---

## 16. Source Repository Pinning

After formal repository install, the device stores `source_repository_id`.

Client MAY display the same App from other Repositories, but cannot silently switch the device's source.

Source Migration requires device/user confirmation and revalidation of:

```text
Repository Root Trust
Publisher Identity
App Transfer Chain (if any)
Release Sequence
Permission Diff
Revocation
Data Schema
```

Changing Mirror host while Repository ID stays the same is not Source Migration.

---

## 17. Compatibility filtering

Client MAY classify:

```text
installable
update_available
latest_compatible
incompatible
experimental
```

based on device Capability / Platform Version, but the device recalculates the decision.

A Client compatibility database MUST NOT override real Device Adapter Capability detection.

Unknown firmware defaults to Experimental or Unsupported; do not infer from a nearby model and do not automatically run high-risk Platform/App updates.

---

## 18. Permission UI

Client SHOULD show:

```text
Current permissions
Candidate permissions
Added
Removed
Denied
```

Sensitive Permission approval ultimately persists on the device.

A PC click can express transfer intent, but consumer devices SHOULD still show/confirm final sensitive authorization unless a separately trusted enterprise-management policy applies.

---

## 19. Privacy

Client / Device Handshake MUST NOT expose by default:

- user's book list;
- note content;
- reading positions;
- LifeBook life records;
- account tokens;
- device serial number;
- Wi-Fi passwords;
- private file paths.

Minimum compatibility facts MAY include:

```text
device family
model ID
firmware / OS version
Platform version
Capability set or digest
free storage
installed app identities / release sequences
```

Installed inventory should be processed locally as much as possible before Repository queries.

Rollout uses a local random Cohort ID, not a hardware ID.

---

## 20. Client cache

Client MAY cache:

```text
Trusted Repository Metadata
content-addressed IKP
Release Records
Publisher Documents
Catalog Records
assets
Offline Snapshots
```

Cache MUST:

- partition by Repository ID and Digest;
- not substitute filename for Digest;
- re-verify before reuse;
- not discover new Release from expired Metadata;
- MAY retain immutable Targets for offline devices;
- never reuse one Repository's same-path object as another Repository's object.

---

## 21. Error model

Standard machine-readable classes:

```text
device_not_detected
platform_not_installed
platform_incompatible
repository_untrusted
metadata_expired
metadata_rollback
package_digest_mismatch
publisher_untrusted
identity_mismatch
permission_confirmation_required
capability_missing
insufficient_storage
transfer_interrupted
device_busy
install_failed
rollback_completed
```

Client presents understandable user reasons while preserving machine error codes.

---

## 22. Recovery and retry

On transfer failure:

- do not delete current App;
- do not treat partial file as IKP;
- allow resume by Digest;
- survive sleep/wake;
- device may clean expired Sessions after Client disconnect;
- retry MUST NOT duplicate Permission approval;
- failed Candidate is not marked Active;
- Transfer Journal and Update Journal remain separate.

---

## 23. Enterprise / OEM management

Future signed Management Policy MAY cover:

```text
trusted repositories
allowed publishers
required apps
blocked apps
approved permissions
update windows
channel policy
```

Management Policy must use an independent device-management trust root, cannot impersonate Publisher Signature, cannot modify IKP bytes, cannot allow ordinary Repository to self-declare administrator status, and must clearly mark managed state to the device owner.

v0.1 does not define the complete enterprise-policy format.

---

## 24. Final rule

> **Client may make installation easier, but it cannot make verification smaller. Offline operation may change the transport route, but it does not change the trust chain.**
