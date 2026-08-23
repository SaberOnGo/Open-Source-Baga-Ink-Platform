# Baga Ink IKP Signing and Key Lifecycle Standard

> **Document level:** Core Distribution Cryptography Standard  
> **Document ID:** `standards.22`  
> **Locale:** English (`en`)  
> **Status:** Draft v0.1  
> **Date:** 2026-08-22  
> **Parent:** `docs/en/standards/20_baga-ink-market-and-distribution-architecture.md`  
> **Identity:** `docs/en/standards/21_baga-ink-publisher-identity-and-app-ownership-standard.md`  
> **Package:** `docs/en/standards/06_ikp-package-specification.md`  
> **Counterpart:** `docs/zh-CN/standards/22_IKP签名与密钥生命周期标准.md`

---

## 0. Purpose

This document defines the publisher signature format for IKP, verification rules, file-integrity manifests, App Signing Key Delegation, Publisher Root rotation, emergency recovery, and device verification order.

Baga Ink uses mature cryptographic primitives and does not invent a new cryptographic algorithm.

Core goal:

> **An IKP obtained from the official Market, a third-party Repository, USB, LAN, or a local file must be independently able to prove its application identity and logical payload integrity.**

---

## 1. v0.1 cryptographic baseline

Baga Ink v0.1 MUST support:

```text
Content digest: SHA-256
Digital signature: Ed25519
Text encoding: UTF-8
Binary-to-text encoding: unpadded base64url
Signed structured data: Baga Canonical JSON Profile
```

Implementations MUST reject:

- undeclared/unsupported signature algorithms;
- algorithm-name case or alias ambiguity;
- unknown Critical fields;
- duplicate JSON object keys;
- invalid UTF-8;
- NaN / Infinity;
- signed inputs that do not satisfy the canonicalization profile.

A future algorithm requires an explicit new format/version and migration rule; it MUST NOT silently replace the v0.1 baseline.

---

## 2. Key ID

For Ed25519:

```text
key_id
=
"ed25519:" + base64url(SHA-256(raw_32_byte_public_key))
```

Rules:

- the public key MUST be the raw 32-byte Ed25519 public key;
- Key ID is an identifier/index, not a substitute for signature verification;
- a parser MUST recompute the Key ID and compare it with the declared value;
- the same public key always produces the same Key ID.

---

## 3. Baga Canonical JSON Profile

Every signed JSON body MUST have one unique byte representation.

v0.1 rules:

- UTF-8;
- object keys sorted ascending by Unicode code point;
- no insignificant whitespace;
- duplicate keys forbidden;
- standard JSON string escaping;
- array order and semantic object content preserved;
- integers encoded in shortest decimal form;
- security statements in v0.1 MUST NOT use floating point;
- no extra trailing newline;
- signature input is the raw UTF-8 bytes of canonical JSON.

The SDK MUST provide a single official serializer/validator profile so different language implementations do not sign different bytes for the same logical object.

---

## 4. IKP signature directory

A formally signed IKP SHOULD contain:

```text
signature/
├── files.json
├── publisher-identity.json
├── app-ownership.json
├── app-key-delegation.json
├── release-statement.json
└── signatures.json
```

Roles:

- `files.json` — hashes/lengths for application Payload files;
- `publisher-identity.json` — current Publisher Identity document or required proof chain;
- `app-ownership.json` — App ID ownership statement;
- `app-key-delegation.json` — authorization of the App Signing Key;
- `release-statement.json` — canonical body signed for this IKP release;
- `signatures.json` — signature set over the Release Statement.

Identity material MAY carry a full chain or a minimal proof chain, but the device must be able to connect it to a trusted Publisher Genesis (or a Genesis first explicitly trusted on initial install).

---

## 5. `files.json`

`files.json` MUST enumerate every application Payload file.

Payload means every file in the IKP except files under `signature/`.

Example:

```json
{
  "type": "baga.ikp-files",
  "format": "0.1",
  "hash_algorithm": "sha256",
  "files": [
    {
      "path": "manifest.json",
      "length": 642,
      "sha256": "..."
    },
    {
      "path": "main.lua",
      "length": 1830,
      "sha256": "..."
    }
  ]
}
```

Rules:

- paths MUST be normalized;
- `/` is the separator;
- absolute paths, `..`, and symlink escape are forbidden;
- every Payload file appears exactly once;
- no undeclared extra Payload is allowed;
- entries are sorted ascending by UTF-8 path bytes;
- the hash is calculated over decompressed raw file bytes;
- `length` MUST match the actual file length.

`files.json` itself is not listed inside its own `files` array.

---

## 6. `release-statement.json`

The Release Statement is the body actually signed by the App Signing Key.

Conceptual example:

```json
{
  "type": "baga.ikp-release",
  "format": "0.1",
  "app_id": "com.example.reader",
  "publisher_id": "pub1_...",
  "version_name": "1.4.2",
  "release_sequence": 142,
  "channel": "stable",
  "ikp_format": "0.2",
  "baga_api": {
    "min": "0.1",
    "max_exclusive": "1.0"
  },
  "manifest": {
    "path": "manifest.json",
    "length": 642,
    "sha256": "..."
  },
  "files_manifest": {
    "path": "signature/files.json",
    "length": 1684,
    "sha256": "..."
  },
  "publisher_identity_digest": "sha256:...",
  "app_ownership_digest": "sha256:...",
  "app_key_delegation_digest": "sha256:...",
  "app_signing_key_id": "ed25519:...",
  "created_at": "2026-08-22T00:00:00Z"
}
```

The Release Statement MUST be cross-checked against `manifest.json`, including at least:

```text
app_id
version_name
release_sequence
channel
IKP format
Baga API range
permissions
capabilities
```

Any inconsistency MUST cause rejection.

Security-critical identity fields are authorized by the signed Release Statement; changing Manifest data cannot bypass the signature chain.

---

## 7. `signatures.json`

Conceptual form:

```json
{
  "type": "baga.signature-set",
  "format": "0.1",
  "signed_object": "signature/release-statement.json",
  "signed_object_sha256": "...",
  "signatures": [
    {
      "key_id": "ed25519:...",
      "algorithm": "ed25519",
      "signature": "base64url..."
    }
  ]
}
```

The signed message is:

```text
CanonicalJSON(release-statement.json)
```

not `signatures.json` itself.

Rules:

- each Key ID appears at most once;
- counted signatures must be from keys authorized by the Delegation;
- valid signature count MUST meet the Delegation Threshold;
- invalid or unknown signatures do not count;
- additional unknown signatures MAY be ignored, but cannot change the verification result.

---

## 8. App Signing Key Delegation verification

A device MUST verify:

1. Delegation `publisher_id` matches the Release;
2. Delegation `app_id` matches the Release;
3. Delegation satisfies the current trusted Publisher Root Threshold;
4. App Signing Key ID matches the Public Key;
5. Channel is in the delegated scope;
6. Release Sequence is in the delegated range;
7. Delegation Status is `active`;
8. Delegation has not been revoked/replaced by a higher Sequence;
9. validity-window checks pass;
10. Release Signature Threshold is satisfied.

A signing key does not gain authority over another application merely because both applications belong to the same Publisher.

---

## 9. Publisher Identity Chain

A device MUST be able to verify:

```text
Trusted Publisher Genesis
         │
         ▼
Identity Update Sequence 2
         │
         ▼
Identity Update Sequence 3
         │
         ▼
Current Publisher Identity
```

Every update document MUST:

- reference the previous document digest;
- increment Sequence by one;
- satisfy the previous Root Threshold;
- when the Root Set changes, satisfy the new Root Threshold as acceptance;
- keep the same Publisher ID.

A device MUST NOT skip missing Identity Sequences unless a future explicitly specified Compact Proof format permits it.

---

## 10. Normal App Signing Key Rotation

The old App Signing Key does not need to authorize the new key. Authority comes from Publisher Root:

```text
Publisher Root
      │
      ├── Delegation N   → App Key A
      └── Delegation N+1 → App Key B
```

After Delegation N+1 becomes active:

- Key A MAY become `retired`;
- historical Releases remain verifiable;
- new Releases use Key B;
- devices retain the old Delegation as required to validate installed/historical packages.

If Key A becomes `revoked`, a security-handling statement SHOULD accompany the revocation and releases signed during the compromise window must be investigated.

---

## 11. Publisher Root Rotation

Normal Root Rotation uses the Publisher Identity update chain.

Verification requires:

```text
Old Root Threshold
        signs
New Identity Document
        and
New Root Threshold
        signs acceptance
```

Only when both thresholds are met does the device update Root Trust.

Old Root keys may be removed from the current set, but historical signature chains must remain verifiable.

---

## 12. Emergency Recovery

When normal Root Rotation is impossible, use a Recovery Statement.

```json
{
  "type": "baga.publisher-recovery",
  "format": "0.1",
  "publisher_id": "pub1_...",
  "recovery_sequence": 2,
  "last_trusted_identity_digest": "sha256:...",
  "new_identity_digest": "sha256:...",
  "reason": "root-key-loss",
  "incident_reference": "...",
  "not_before": "...",
  "created_at": "..."
}
```

Recovery requires all of:

```text
Publisher Recovery Threshold
+
Repository Security Recovery Attestation
+
Transparency Log publication
+
not_before cooling period
```

A device MUST NOT accept Publisher Root replacement based only on Market-account or support-ticket evidence.

A long-offline device seeing a Recovery for the first time MUST receive the complete Recovery Evidence.

---

## 13. App Transfer signatures

App Transfer requires:

```text
Transfer-Out Statement signed by Old Publisher Root
Transfer-In Statement signed by New Publisher Root
Repository Transfer Attestation
```

The new IKP Release Statement uses the new Publisher ID.

Only after validating the complete Transfer Chain may a device allow the new Publisher's App Signing Key to replace the old installed identity.

Transfer MUST NOT silently add permissions and MUST NOT roll Release Sequence backward.

---

## 14. Container digest vs logical payload signature

Baga Ink uses two distinct integrity checks.

### 14.1 Repository Container Digest

Repository Metadata protects the complete `.ikp` file:

```text
SHA-256
length
```

It verifies exact downloaded container bytes.

### 14.2 Publisher Logical Payload Signature

Publisher Signature, through `files.json`, protects the unpacked application Payload.

It remains valid for identity verification even when the IKP is obtained by explicit sideloading without repository context.

Therefore:

```text
Repository Digest
→ exact distributed container

Publisher Signature
→ application identity + logical payload
```

They are complementary and do not replace one another.

---

## 15. Deterministic packaging

Baga Ink SDK SHOULD support deterministic IKP production:

- fixed ZIP entry order;
- fixed timestamp policy;
- fixed permission bits;
- fixed compression parameters;
- no local absolute paths;
- no random unsigned fields.

This improves reproducible builds, review, caching, delta generation, and third-party verification.

However Publisher Signature verification is defined over the canonical logical payload proof and MUST NOT assume every legitimate build tool emits byte-identical ZIP containers.

---

## 16. Device verification order

Installing a formal IKP MUST perform at least:

```text
1. enforce container size limit
2. enforce ZIP/path safety
3. read manifest + signature files
4. validate IKP Format
5. validate files.json schema
6. validate every Payload file hash + length
7. validate Publisher Genesis / Identity Chain
8. validate App Ownership
9. validate App Key Delegation
10. validate Release Statement schema
11. validate Release Signature Threshold
12. cross-check Manifest and Release Statement
13. validate Release Sequence
14. validate revocation state
15. validate Baga API / Capability / Permission
16. only then enter staged install
```

For Repository delivery, Repository Metadata and Container Digest validation also applies before/alongside this chain.

---

## 17. Signed sideload verification

A locally sideloaded signed IKP without Repository Metadata:

- MUST fully validate Publisher Signature;
- MUST display Publisher ID, App ID, and key fingerprint;
- on first install MUST require user confirmation of Publisher Trust;
- MUST NOT claim official Market review;
- future updates MUST preserve App Identity;
- Security Revocation can only be learned when the device later reconnects to an appropriate trusted Repository/evidence source.

---

## 18. Unsigned developer packages

Unsigned IKPs are Developer Mode only.

Rules:

- no formal Publisher Identity is established;
- they MUST NOT overwrite formal application identity;
- continuous warning is required;
- a temporary developer fingerprint MAY be shown;
- automatic updates cannot continue after leaving Developer Mode;
- formal Repository publication requires repackaging/signing as a formal release.

---

## 19. Key storage guidance

Publisher Root / Recovery Keys:

- SHOULD be offline;
- SHOULD have encrypted backup;
- SHOULD be stored across at least two physical locations;
- MAY use hardware security keys, HSM, PKCS#11, or OS secure key stores;
- MUST NOT live on public web/repository/CDN servers.

App Signing Keys:

- MAY be held by a protected CI signing service;
- SHOULD be scoped to a specific App / Channel;
- SHOULD have least-privilege human access;
- SHOULD log each signing action;
- SHOULD NOT be silently held by a Market server unless the developer explicitly opts into a custodial signing trust model.

---

## 20. Key compromise response

### App Key compromise

1. stop release immediately;
2. publish Delegation Revocation;
3. delegate a new App Key from Publisher Root;
4. audit releases during the compromise window;
5. issue Security Revocation when required;
6. append Transparency evidence.

### Publisher Root compromise

1. if the old Threshold is not fully compromised, perform normal dual Root Rotation;
2. otherwise perform Recovery Flow;
3. freeze new App Ownership / Transfer operations;
4. audit every Delegation;
5. publish recovery evidence.

### Repository Key compromise

Publisher Signature Chain does not change; Repository Root rotates repository role keys.

---

## 21. Version rules

Signing-related documents have their own:

```text
format
sequence
created_at / effective_at
previous_digest (when applicable)
critical-field declaration
```

Verifier behavior:

- unsupported higher Format Major → reject;
- unknown Critical field → reject;
- sequence below trusted local sequence → reject;
- same Sequence with different Digest → security conflict, reject/report;
- same Release Sequence with different IKP Payload → reject.

---

## 22. Final trust chain

```text
Publisher Root
      │
      ├── App Ownership
      ├── App Key Delegation
      ├── Root Rotation
      └── App Transfer
              │
              ▼
       App Signing Key
              │
              ▼
       IKP Release Statement
              │
              ▼
        files.json Payload
```

The Market may verify, review, and distribute this chain, but it does not replace it.
