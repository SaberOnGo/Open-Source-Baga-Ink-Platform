# Baga Ink Transparency and Security Audit Standard

> **Document level:** Distribution Transparency / Audit Standard  
> **Document ID:** `standards.27`  
> **Locale:** English (`en`)  
> **Status:** Draft v0.1  
> **Date:** 2026-08-22  
> **Parent:** `docs/en/standards/20_baga-ink-market-and-distribution-architecture.md`  
> **Identity:** Standard 21  
> **Repository:** Standard 23  
> **Counterpart:** `docs/zh-CN/standards/27_透明日志与安全审计标准.md`

---

## 0. Purpose

This document defines publicly verifiable history and independent audit for Publisher, App ID, key, Release, review, transfer, recovery, withdrawal, and security-revocation events in the Baga Ink ecosystem.

It uses the mature concept of an append-only Merkle Transparency Log.

Core rule:

> **Important identity and security events cannot exist only inside a Market's private database; they must leave a verifiable history that cannot be silently rewritten.**

Transparency is audit evidence, not the device's sole installation trust root.

---

## 1. Goals

The transparency/audit layer provides:

```text
append-only event history
event inclusion proof
tree consistency proof
signed tree checkpoints
independent monitoring
Publisher / App history lookup
key-compromise investigation
Repository publication audit
Review Attestation audit
privacy-preserving public records
```

It should help detect:

- unauthorized Market replacement of Publisher Identity;
- unauthorized App ID transfer;
- suspicious App Key Delegation creation;
- abuse of Publisher Root recovery;
- different Digests for one Release Sequence;
- deletion of published Releases or Revocation records from history;
- conflicting repository history shown to different observers.

---

## 2. Non-goals

Transparency Log v0.1 does not record:

- which Apps a user installed;
- user accounts;
- device serial numbers;
- reading history, notes, or library contents;
- and does not replace Repository Root, Publisher Signature, or Security Revocation;
- does not require every Kindle to query the log online during every installation;
- is not a remote-uninstall control channel.

---

## 3. Required events

The official Baga Ink Market Transparency Log MUST record:

```text
publisher_genesis
publisher_identity_update
publisher_root_rotation
publisher_recovery_started
publisher_recovery_completed
publisher_recovery_cancelled
app_id_registered
app_ownership_created
app_key_delegated
app_key_retired
app_key_revoked
app_transfer_started
app_transfer_completed
release_published
release_withdrawn
release_unlisted
security_revocation_published
review_attestation_published
repository_root_rotated
```

Market Policy MAY add events but cannot omit these security-relevant classes.

---

## 4. Event Envelope

All events use a common envelope.

```json
{
  "type": "baga.transparency-event",
  "format": "0.1",
  "event_type": "release_published",
  "event_id": "evt1_...",
  "subject": {
    "publisher_id": "pub1_...",
    "app_id": "com.example.reader",
    "release_sequence": 142
  },
  "statement": {
    "path": "releases/sha256/...json",
    "length": 1842,
    "sha256": "..."
  },
  "repository_id": "repo1_...",
  "observed_at": "2026-08-22T00:00:00Z",
  "critical": true
}
```

Event ID:

```text
event_id
=
"evt1_" + base32lower(SHA-256(CanonicalJSON(event_body_without_event_id)))
```

The event references a signed Statement Digest instead of copying all sensitive or lengthy data into the public log.

---

## 5. Merkle Log

The log is an append-only Merkle Tree ordered by Leaf Index.

A Leaf contains canonical event bytes or an event digest referencing an immutable event target.

The implementation MUST provide:

- Tree Size;
- Root Hash;
- Signed Tree Head / Checkpoint;
- Inclusion Proof;
- Consistency Proof;
- Leaf Index lookup;
- Event ID lookup;
- subject search index.

Baga Ink v0.1 does not invent a new Merkle hash construction. The implementation SHOULD use a mature and publicly reviewed transparency-log algorithm/library equivalent in security properties to Rekor/Trillian-style models.

---

## 6. Signed Checkpoint

The Log Operator MUST periodically publish a signed Checkpoint.

```json
{
  "type": "baga.transparency-checkpoint",
  "format": "0.1",
  "log_id": "log1_...",
  "tree_size": 128394,
  "root_hash": "base64url...",
  "timestamp": "...",
  "previous_checkpoint_digest": "sha256:...",
  "signing_key_id": "ed25519:..."
}
```

Checkpoint MUST:

- be signed by the Log Signing Key;
- be published as a Repository Target;
- be retainable by independent Monitors;
- support Consistency Proof from prior Tree Size;
- keep the same Log ID across ordinary server/database migrations.

---

## 7. Log Identity

Every log has stable `log_id`.

Recommended:

```text
log_id
=
"log1_" + base32lower(SHA-256(log_genesis_document))
```

Log Genesis Document defines:

```text
Log public key
Log operator
hash algorithm
tree algorithm profile
API version
creation time
```

Log URL MAY change; Log ID does not.

Log Key Rotation requires a signed continuity chain plus repository/public audit evidence.

---

## 8. Publisher events

### 8.1 Publisher Genesis

Record Publisher Genesis Document Digest + Publisher ID.

### 8.2 Identity Update

Record:

```text
publisher_id
identity_sequence
previous_digest
new_identity_digest
```

### 8.3 Root Rotation

Record old/new Root Key Set summaries, Identity Sequence, and effective time.

### 8.4 Recovery

Recovery records at least:

```text
started
completed
cancelled (when applicable)
```

`started` is appended when the Cooling Period begins. `completed` is appended only after Recovery Threshold, Market Security Attestation, and `not_before` requirements hold.

This gives independent Monitors time to detect suspicious recovery.

---

## 9. App Ownership and Transfer

App ID registration records:

```text
app_id
publisher_id
ownership_statement_digest
```

App Transfer records:

```text
old_publisher_id
new_publisher_id
transfer_nonce
transfer_out_digest
transfer_in_digest
repository_attestation_digest
```

Between Transfer Started and Completed, a Market MAY freeze high-risk releases.

Conflicting target Publishers for the same `app_id + transfer_sequence` MUST be reported by Monitors.

---

## 10. App Key events

App Signing Key Delegation event records:

```text
app_id
publisher_id
key_id
delegation_sequence
allowed_channels
release_sequence_range
validity window
delegation_digest
```

Retired and Revoked are separate event types:

- `retired` — no new Releases, historical signatures still valid;
- `revoked` — compromise suspected/confirmed; all Releases signed by the key require investigation.

Key Revoked event SHOULD reference a replacement Delegation or incident-handling statement.

---

## 11. Release events

Every formal Release records:

```text
app_id
publisher_id
release_sequence
version_name
channel
package_sha256
package_length
release_record_digest
publisher_signature_key_id
published_at
```

The log MUST detect:

```text
same app_id
+
same release_sequence
+
different package_sha256
```

This is unacceptable equivocation and should trigger an immediate security alert.

---

## 12. Review events

Publishing a Review Attestation records:

```text
repository_id
app_id
release_sequence
package_sha256
review_policy_version
result
attestation_digest
```

A changed review result MUST append a new Attestation and reference the superseded Attestation Digest; history is never overwritten.

This makes it possible to audit which policy approved a version and why it was later suspended or revoked.

---

## 13. Withdrawal and Revocation events

Withdrawn, Unlisted, and Security Revoked are separately recorded.

Security Revocation Event includes at least:

```text
app_id
release_sequence
package_sha256
severity
reason_code
revocation_record_digest
effective_at
replacement_release (when available)
```

A correction appends a new event rather than deleting history. For example:

```text
security_revocation_corrected
```

with explicit reference to the original event.

---

## 14. Inclusion Proof

Event lookup SHOULD return:

```text
event
leaf_index
checkpoint
inclusion_proof
```

An independent verifier can confirm Event Digest, membership at the given Tree Size, Checkpoint Signature, and Root Hash.

Publisher Portal SHOULD let developers download Inclusion Proofs for their publication events.

---

## 15. Consistency Proof

For checkpoints A and B:

```text
A.tree_size < B.tree_size
```

The log MUST provide a Consistency Proof showing B is an append-only extension of A.

A Monitor MUST reject/report:

- increased Tree Size without valid Consistency Proof;
- same Tree Size with different Root Hash;
- checkpoint time rollback;
- unexplained Log ID change.

---

## 16. Gossip and independent monitoring

Baga Ink SHOULD distribute checkpoints through multiple independent channels:

```text
Repository Target
Baga Ink Developers
public transparency endpoint
GitHub / public archive mirror
independent monitors
security mailing list / feed
```

Independent Monitor responsibilities:

- retain historical checkpoints;
- verify consistency;
- detect same-size/different-root split view;
- detect App ID conflicts;
- detect same Sequence/different Digest;
- detect suspicious Recovery / Transfer;
- publish verifiable alert evidence.

The official Baga Ink team SHOULD NOT be the only Monitor.

---

## 17. Split View detection

If different observers receive:

```text
Checkpoint A: size 1000, root X
Checkpoint B: size 1000, root Y
```

publishing the two valid signed checkpoints proves Log Operator equivocation.

Repository, Developer Portal, and Monitors SHOULD exchange Checkpoints to reduce split-view risk.

Devices in v0.1 need not perform real-time gossip. Baga Ink Client MAY cache/share checkpoints with explicit user consent, without including installed-app inventory.

---

## 18. Privacy

Public events contain only software-supply-chain information.

MUST NOT include:

- developer private address;
- user email;
- user installation records;
- Device ID;
- user books/notes/reading data;
- Private Keys;
- full exploit details for embargoed vulnerabilities;
- unredacted private review conversations.

MAY include:

- Publisher ID;
- public keys;
- App ID;
- digests;
- Release Sequence;
- standardized Reason Code;
- public Security Advisory reference.

---

## 19. Retention

Transparency events are long-lived history.

If the primary service ends:

- publish a final Checkpoint;
- export log data to a verifiable Archive;
- existing Inclusion / Consistency Proofs remain verifiable;
- Repository Root MAY designate a successor log while preserving old Log ID / Checkpoint history;
- restarting with an empty log MUST NOT erase supply-chain history.

---

## 20. Availability failure

If Transparency service is temporarily unavailable:

- installed Apps continue to run;
- Repository Metadata and Publisher Signature verification still works;
- low-risk ordinary releases MAY be delayed by Repository Policy;
- Publisher Recovery, App Transfer, Root Rotation, Security Revocation and similar high-risk events SHOULD NOT finalize without log receipt confirmation;
- Market displays transparency-service outage state.

Transparency must not become a single point that stops all devices when temporarily unavailable.

---

## 21. Minimum Log API

v0.1 provides semantics equivalent to:

```text
POST /events
GET  /events/{event_id}
GET  /entries/{leaf_index}
GET  /checkpoint
GET  /proof/inclusion?leaf_index=&tree_size=
GET  /proof/consistency?from=&to=
GET  /search?publisher_id=
GET  /search?app_id=
```

Exact URLs MAY differ; protocol semantics stay stable.

Event submission validates base Schema but does not replace Market validation of referenced Statement signatures/business rules.

---

## 22. Log Operator security

Operator SHOULD:

- isolate Signing Key from ordinary web service;
- back up tree state;
- use immutable/append-only storage where practical;
- publish Checkpoints to independent locations;
- monitor unauthorized key use;
- rate-limit and/or require human confirmation for high-risk events;
- audit administrator actions;
- prevent database operators from silently rewriting history and recomputing the tree without detectable evidence.

---

## 23. Security Audit Bundle

A Market SHOULD be able to export for one Release:

```text
Publisher Genesis / Identity Chain
App Ownership
App Key Delegation
IKP Release Statement
Repository Release Record
Repository Metadata descriptors
Review Attestation
Transparency Event
Inclusion Proof
Relevant Checkpoint
Withdrawal / Revocation (if any)
```

This allows independent audit without access to the Market's private database.

---

## 24. Device / Client boundary

A device is not required to query Transparency during installation.

Baga Ink Client MAY display Publisher/App history, verify Release Inclusion Proof, flag suspicious Recovery/Transfer, cache Checkpoints, and export Audit Bundles.

Device installation identity still derives from:

```text
Publisher Signature
Repository Metadata
Local Installed Identity
```

Transparency adds discoverability/accountability; it does not replace the three-layer trust model.

---

## 25. Final rule

> **Signatures make forgery harder; transparency makes hidden abuse of legitimate signing and administrative authority harder.**
