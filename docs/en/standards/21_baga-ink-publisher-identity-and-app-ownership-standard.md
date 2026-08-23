# Baga Ink Publisher Identity and App Ownership Standard

> **Document level:** Core Distribution Security Standard  
> **Document ID:** `standards.21`  
> **Locale:** English (`en`)  
> **Status:** Draft v0.1  
> **Date:** 2026-08-22  
> **Parent:** `docs/en/standards/20_baga-ink-market-and-distribution-architecture.md`  
> **Related:** Standards 22, 23, 27  
> **Counterpart:** `docs/zh-CN/standards/21_发布者身份与应用所有权标准.md`

---

## 0. Purpose

This document defines:

- Publisher Identity;
- the boundary between Developer Account and software-signing identity;
- Application ID ownership;
- Publisher Root Keys;
- App Signing Key Delegation;
- application identity continuity;
- App Transfer;
- key rotation, loss, recovery, and compromise handling;
- device-side installed-identity pinning.

Core security rule:

> **A Market account proves who may operate the service backend; Publisher cryptographic keys prove who authorized software publication. These identities MUST remain separate.**

---

## 1. Identity hierarchy

Baga Ink defines four separate concepts.

### 1.1 Developer Account

A Developer Account authenticates a person/team to Baga Ink Developers or a Market.

It MAY use Email, Passkey, OAuth, organization SSO, and MFA.

It is used for:

- team management;
- app metadata editing;
- uploading already-signed IKPs;
- review/result access;
- initiating publication, transfer, and recovery workflows;
- Market-policy administration.

Compromise of a Developer Account alone MUST NOT be sufficient to produce a device-acceptable formal application update.

### 1.2 Publisher Identity

Publisher Identity is the cryptographic identity of a software publisher.

It consists of:

```text
Publisher Genesis Document
Publisher ID
Publisher Root Key Set
Root Signature Threshold
Recovery Key Set
Recovery Signature Threshold
```

### 1.3 App Ownership

App Ownership binds a Publisher to an `app_id`.

It MUST be authorized by the Publisher Root Threshold and MAY additionally be attested by a Repository / Market.

### 1.4 App Signing Key

An App Signing Key is used for routine release signing.

It MUST be explicitly delegated by the Publisher Root Key Set for a bounded scope:

```text
publisher_id
app_id
channel scope
release-sequence range
validity window
```

Routine release signing SHOULD NOT require frequent use of Publisher Root Private Keys.

---

## 2. Why account identity is not software identity

If a Market login account could directly replace application signing identity, account compromise would become immediate arbitrary-update compromise.

Correct separation:

```text
Developer Account
       │
       ├── upload / manage metadata
       └── request release

Publisher / App Signing Key
       │
       └── authorize software bytes
```

A Market MUST verify both:

1. the account is authorized to manage the Publisher/App; and
2. the IKP cryptographic signature is valid under App Ownership / Delegation.

---

## 3. Publisher Genesis Document

Creating a Publisher Identity MUST begin with a Genesis Document.

Conceptual example:

```json
{
  "type": "baga.publisher-genesis",
  "format": "0.1",
  "display_name": "Example Studio",
  "root_threshold": 1,
  "root_keys": [
    {
      "key_id": "ed25519:...",
      "algorithm": "ed25519",
      "public_key": "base64url..."
    }
  ],
  "recovery_threshold": 1,
  "recovery_keys": [
    {
      "key_id": "ed25519:...",
      "algorithm": "ed25519",
      "public_key": "base64url..."
    }
  ],
  "created_at": "2026-08-22T00:00:00Z"
}
```

The Genesis Document MUST use the canonical JSON profile defined by Baga signing standards.

Publisher ID:

```text
publisher_id
=
"pub1_" + base32lower(SHA-256(canonical_genesis_document))
```

The Publisher ID is immutable. Normal Root Key Rotation does not change it.

---

## 4. Publisher Root Key Set

The Publisher Root Key Set is the highest cryptographic authority for a Publisher.

It primarily authorizes:

- App Ownership;
- App Signing Key Delegation;
- App Signing Key revocation;
- normal Publisher Root rotation;
- App Transfer;
- publisher security-policy changes.

Root Private Keys SHOULD be offline or held in hardware/security key stores or dedicated signing systems.

### 4.1 Recommended individual configuration

```text
Root:      1-of-1
Recovery:  1-of-1 separate offline key
App Key:   1-of-1 routine release key
```

Root and Recovery SHOULD NOT be the same private key.

### 4.2 Recommended organization configuration

```text
Root:      2-of-3
Recovery:  2-of-3
App Key:   1-of-1 or 2-of-2 according to policy
```

Device verification only needs to verify independent Ed25519 signatures and threshold counts; no complex aggregate-signature primitive is required.

---

## 5. Publisher Identity evolution

Every identity update after Genesis creates a new Publisher Identity Document.

Conceptual form:

```json
{
  "type": "baga.publisher-identity",
  "format": "0.1",
  "publisher_id": "pub1_...",
  "sequence": 4,
  "previous_digest": "sha256:...",
  "root_threshold": 2,
  "root_keys": [],
  "recovery_threshold": 2,
  "recovery_keys": [],
  "effective_at": "..."
}
```

Rules:

- `sequence` MUST increase monotonically;
- `previous_digest` MUST reference the previously trusted document;
- normal update MUST satisfy the previous Root Threshold;
- a changed Root Set MUST also satisfy the new Root Threshold acceptance;
- a device MUST reject an identity document below the highest trusted local sequence.

Normal Root rotation therefore uses dual authorization:

```text
Old Root Threshold signs new identity
+
New Root Threshold signs acceptance
```

---

## 6. Application ID

Every Baga Ink App MUST have a globally stable `app_id`.

Recommended style:

```text
com.example.reader
org.example.notes
```

Requirements:

- lowercase ASCII letters, digits, dots, and permitted hyphens only;
- at least two hierarchy components;
- MUST NOT change across device, channel, or CPU architecture;
- MUST NOT change when Publisher ownership is transferred;
- one formal release maps to exactly one `app_id`.

### 6.1 Domain namespace verification

If a real reverse-domain namespace is used, an official Market MAY require DNS TXT or HTTPS well-known verification to reduce namespace impersonation.

### 6.2 Developers without domains

A Market MAY allocate a stable Publisher Namespace. Allocation MUST NOT imply ownership of an unverified domain, MUST remain stable across display-name changes, MUST bind to Publisher ID, and MUST remain traceable through Publisher Transfer.

---

## 7. App Ownership Statement

When a Publisher first acquires an App ID, it MUST create an App Ownership Statement.

```json
{
  "type": "baga.app-ownership",
  "format": "0.1",
  "publisher_id": "pub1_...",
  "app_id": "com.example.reader",
  "ownership_sequence": 1,
  "status": "active",
  "created_at": "..."
}
```

The statement MUST:

- satisfy Publisher Root Threshold signatures;
- correspond to a current Publisher Identity Document;
- pass official Market App ID conflict checks where applicable;
- be represented in Transparency Log evidence;
- be referenced by Repository Release Records.

Ownership is not the same thing as Market listing approval.

---

## 8. App Signing Key Delegation

Routine IKPs are signed by App Signing Keys. A key receives authority only through a Delegation.

```json
{
  "type": "baga.app-key-delegation",
  "format": "0.1",
  "publisher_id": "pub1_...",
  "app_id": "com.example.reader",
  "delegation_sequence": 7,
  "key_id": "ed25519:...",
  "public_key": "base64url...",
  "signature_threshold": 1,
  "allowed_channels": ["stable", "beta"],
  "min_release_sequence": 100,
  "max_release_sequence": 999,
  "valid_from": "...",
  "valid_until": "...",
  "status": "active"
}
```

Delegation MUST satisfy Publisher Root Threshold signatures.

The key may sign only within the delegated app, channel, release-sequence range, and validity window.

A device MUST NOT allow a key delegated to one app to sign another app merely because both apps belong to the same Publisher.

---

## 9. Formal installed application identity

A device decides whether two releases are the same logical application using:

```text
Installed App Identity
=
app_id
+
publisher_id
+
Publisher Identity Lineage
```

Publisher ID remains stable through normal Root Key rotation. App Signing Keys MAY rotate when the new key has a valid Delegation.

Display name, icon, Market URL, and Repository URL are not application identity.

---

## 10. Device-side identity pinning

After first formal installation, the device MUST persist identity state such as:

```json
{
  "app_id": "com.example.reader",
  "publisher_id": "pub1_...",
  "publisher_identity_sequence": 4,
  "publisher_identity_digest": "sha256:...",
  "app_ownership_sequence": 1,
  "app_signing_key_id": "ed25519:...",
  "source_repository_id": "repo1_...",
  "current_release_sequence": 126,
  "current_package_digest": "sha256:..."
}
```

A repository entry with the same App ID MUST NOT overwrite this identity unless:

- Publisher ID is unchanged and the signing chain is valid; or
- a complete valid App Transfer Chain exists; or
- the user explicitly resets the previous application identity and handles its data as a new-app trust decision.

---

## 11. App Signing Key Rotation

Normal rotation:

1. Publisher Root signs a new App Signing Key Delegation;
2. the Delegation Sequence increases;
3. Repository publishes the new Delegation;
4. Transparency Log records the event;
5. future IKP is signed by the new App Signing Key;
6. device verifies Root → Delegation → IKP Signature.

Old keys may be:

```text
active
retired
revoked
```

`retired` means no new signing but historical signatures remain valid. `revoked` means compromise is suspected/confirmed and additional security handling applies.

---

## 12. Publisher Root Rotation

Normal Root Rotation MUST:

- preserve Publisher ID;
- increment Identity Sequence;
- reference previous identity digest;
- satisfy old Root Threshold;
- satisfy new Root Threshold;
- be published through Repository and Transparency evidence;
- not skip required intermediate sequence continuity.

---

## 13. Recovery Keys

Recovery Keys are for exceptional cases only:

- all Root Private Keys lost;
- Root compromise;
- team lost access to original secure devices;
- normal Root Rotation is impossible.

Recovery Keys are not routine app-release keys.

Emergency recovery requires at least:

```text
Recovery Threshold Signature
+
Market / Repository Security Recovery Attestation
+
Public Cooling Period
+
Transparency Log Event
```

Recovery statement includes:

```text
publisher_id
last_trusted_identity_digest
new_root_key_set
new_recovery_key_set
reason
incident_reference
recovery_sequence
not_before
```

An official Market MUST NOT silently replace Publisher Root solely through account-support procedures when no Recovery Key authorization exists.

---

## 14. Loss of both Root and Recovery Keys

If both Root and Recovery private keys are lost, the new key cannot automatically prove continuity with the old Publisher Identity.

Allowed paths are limited to:

1. re-publish under a new Publisher / new app identity;
2. a high-assurance dispute-resolution process requiring explicit user trust reset on device;
3. a previously registered and cryptographically verifiable organization recovery mechanism.

Control of the original email, GitHub account, or backend account information is not sufficient for a silent key takeover.

---

## 15. App Transfer

Transferring an app from Publisher A to Publisher B requires a bilateral chain.

### 15.1 Transfer Out

Publisher A Root Threshold signs:

```text
app_id
old_publisher_id
new_publisher_id
transfer_sequence
last_release_sequence
transfer_nonce
```

### 15.2 Transfer In

Publisher B Root Threshold signs matching:

```text
app_id
transfer_nonce
old_publisher_id
new_publisher_id
```

### 15.3 Repository Attestation

Repository confirms:

- current App ID ownership change;
- validity of both sides' signatures;
- absence of conflicting parallel transfer;
- establishment of a new Publisher App Signing Key Delegation.

### 15.4 Device behavior

Only a complete valid Transfer Chain allows Publisher ID change to continue as the same application.

Transfer MUST NOT automatically expand permissions. The transfer event MUST be auditable through Transparency.

---

## 16. Team/account roles

Market account roles MAY include:

```text
Owner
Security Admin
Release Manager
Metadata Editor
Reviewer Liaison
Viewer
```

These are account permissions, not cryptographic signing authority.

Recommended boundaries:

- Metadata Editor cannot sign IKPs;
- Release Manager can upload signed IKPs but cannot alter Publisher Root;
- Security Admin can administer Root/Recovery workflows but does not automatically receive payment authority;
- high-risk actions SHOULD require MFA and dual approval;
- Publisher Root Private Keys MUST NOT be uploaded to Market servers.

---

## 17. Cross-repository identity

Publisher Identity and IKP Signature are not owned by a particular Repository.

The same valid IKP may be distributed by multiple repositories.

Device replacement decisions combine:

```text
App Identity Continuity
+
Repository Source Policy
+
Release Validity
```

A Repository cannot impersonate a Publisher by rewriting Publisher metadata. Root documents and Delegations must be signed by the Publisher.

---

## 18. Market responsibilities and limits

A Baga Ink Market MAY:

- validate Publisher Identity;
- validate domains;
- prevent App ID conflicts in that Market;
- review IKPs;
- sign Repository Metadata;
- issue Review / Recovery / Transfer Attestations;
- record Transparency events.

It MUST NOT:

- generate unauthorized IKP signatures for developers;
- replace an App Signing Key without Publisher authorization;
- bypass Publisher Root based only on account login;
- turn third-party apps into Baga-owned apps;
- let a same-named App ID overwrite a different Publisher Identity.

---

## 19. Security incident classes

### Account Compromise

Market account compromised, Publisher keys safe: freeze backend operations, revoke sessions, recover the account. Installed app identity does not change.

### App Signing Key Compromise

Revoke Delegation, create a new Delegation, publish security notice, investigate suspicious Releases.

### Publisher Root Compromise

Use normal dual Root Rotation or Recovery flow; all new identity documents become transparency events.

### Repository Key Compromise

Rotate/update Repository Root roles. Publisher Identity is unaffected.

### Market Policy Dispute

A Market may delist an app, but it cannot forge Publisher Signature or silently rewrite installed identity.

---

## 20. Versioning and compatibility

Publisher Identity, App Ownership, Delegation, and Transfer Statement are independently versioned.

Devices store the highest accepted Sequence and reject lower versions.

- optional fields MAY be added compatibly;
- security-semantic changes require a Format Major change;
- unknown Critical fields MUST cause rejection;
- unknown ordinary metadata MAY be retained but MUST NOT alter identity decisions.

---

## 21. Final verification rule

For an IKP to be considered a release of an application, the verifier must establish:

```text
Publisher Genesis
      │
      ▼
Current Publisher Identity
      │
      ▼
App Ownership
      │
      ▼
App Signing Key Delegation
      │
      ▼
IKP Release Signature
```

and verify:

```text
app_id consistency
publisher_id consistency or valid Transfer Chain
monotonic non-rollback Sequences
all signature Thresholds met
supported signature algorithms
valid validity windows and revocation states
```

No Repository or account is allowed to replace this cryptographic identity chain.
