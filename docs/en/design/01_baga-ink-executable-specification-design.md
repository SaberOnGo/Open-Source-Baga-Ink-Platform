# Baga Ink Executable Specification Design

> **Document level:** Implementation Architecture Design  
> **Document ID:** `design.01`  
> **Locale:** English (`en`)  
> **Status:** Approved Design Baseline v0.1  
> **Date:** 2026-08-22  
> **Governing standards:** `docs/en/standards/21...28`  
> **Counterpart:** `docs/zh-CN/design/01_规范可执行化设计.md`

---

## 0. Goal

This design turns Standards 21–28 from prose into an **Executable Specification**.

The immediate goal is not to build the complete Baga Ink Market. It is to establish an executable baseline able to answer:

> **Given the same Publisher Identity, IKP, Repository Metadata, Release, and update evidence, do two independent implementations accept and reject the same inputs under the same rules?**

Phase-one deliverables:

1. JSON Schemas;
2. Canonical JSON test vectors;
3. positive cryptographic vectors;
4. invalid / negative corpus;
5. Python Reference Implementation;
6. minimal independent Rust Device Verifier;
7. TUF Conformance adapter;
8. minimal Repository → Client → Device prototype;
9. CI;
10. Stable Gate.

Draft standards become eligible for Stable review only after the required executable gates pass.

---

## 1. Overall approach

Use:

> **Language-neutral machine specification + Python Reference Implementation + Rust Independent Device Verifier.**

```text
                  Standards 21–28
                         │
                         ▼
               Machine-readable Spec
              ┌──────────┴──────────┐
              │                     │
          JSON Schema           Test Vectors
              │                     │
              └──────────┬──────────┘
                         ▼
              Python Reference Impl
                         │
           ┌─────────────┼─────────────┐
           │             │             │
       IKP signer     Repository     Client/Device
       / verifier      generator       reference
           │             │             │
           └─────────────┼─────────────┘
                         ▼
                    End-to-End
                         │
                         ▼
              Rust Device Verifier
                         │
                         ▼
               Cross-language Tests
```

Python handles Schema validation, vectors, identity/signing reference behavior, IKP build/verification, TUF Repository/Client, minimal distribution prototypes, fixtures, and CI.

Rust phase one implements only device-critical verification semantics:

```text
strict JSON
RFC 8785 JCS
SHA-256
Ed25519
Publisher Genesis
App Ownership
App Key Delegation
Release Statement
IKP Payload Hash
App Identity consistency
```

Rust does not implement Market, Repository Generator, or review workflows in phase one.

---

## 2. Repository structure

```text
spec/
├── schemas/
│   ├── identity/
│   ├── signing/
│   ├── repository/
│   ├── publishing/
│   ├── update/
│   ├── transfer/
│   ├── transparency/
│   └── catalog/
├── vectors/
│   ├── canonical-json/
│   ├── signatures/
│   ├── key-rotation/
│   ├── app-transfer/
│   └── hashes/
└── fixtures/
    ├── ikp/{valid,invalid}/
    ├── repository/
    ├── updates/
    └── recovery/

reference/
├── python/
│   ├── pyproject.toml
│   └── src/baga_spec/
│       ├── strict_json.py
│       ├── canonical.py
│       ├── schemas.py
│       ├── crypto.py
│       ├── identity.py
│       ├── signing.py
│       ├── ikp.py
│       ├── repository.py
│       ├── client.py
│       ├── device.py
│       └── errors.py
└── rust/
    └── baga-verifier/

tools/
├── baga-spec
├── tuf-client-under-test
├── generate-vectors
└── build-test-ikp

tests/
├── test_schemas.py
├── test_strict_json.py
├── test_canonical.py
├── test_identity.py
├── test_signing.py
├── test_ikp.py
├── test_invalid_fixtures.py
├── test_repository.py
├── test_update.py
├── test_cross_language.py
└── test_end_to_end.py

.github/workflows/
├── conformance.yml
└── tuf-conformance.yml
```

Prose Standards remain public authority. Machine specifications are executable counterparts, not a separate protocol.

---

## 3. JSON and canonicalization

### 3.1 Baga signed objects

Custom Baga signed JSON uses:

> **RFC 8785 JSON Canonicalization Scheme (JCS).**

Signing path:

```text
UTF-8 decode
→ Strict JSON parse
→ I-JSON constraints
→ Schema validation
→ RFC 8785 canonicalization
→ SHA-256 / Ed25519
```

Strict parsing rejects duplicate object keys, NaN, Infinity, invalid Unicode, out-of-schema numeric values, and unknown fields in security-critical structures.

### 3.2 TUF Metadata

TUF Metadata is NOT re-signed using Baga JCS rules.

```text
root.json
timestamp.json
snapshot.json
targets.json
```

follow the selected TUF version's own serialization/signing semantics. Baga custom data exists only where the TUF Profile permits it.

---

## 4. JSON Schema baseline

Use JSON Schema Draft 2020-12.

Security-critical objects default to:

```json
{"additionalProperties": false}
```

Stable Schema IDs use URNs:

```text
urn:baga:schema:<name>:<version>
```

Initial Schemas:

```text
identity/
  publisher-genesis.schema.json
  publisher-root-update.schema.json
  app-ownership.schema.json
  app-key-delegation.schema.json
  app-transfer.schema.json

signing/
  files-manifest.schema.json
  release-statement.schema.json
  signature-envelope.schema.json

repository/
  release-record.schema.json
  baga-target-custom.schema.json

publishing/review-attestation.schema.json
update/{revocation-statement,update-journal}.schema.json
transfer/{transfer-session,offline-snapshot-manifest}.schema.json
transparency/{transparency-event,transparency-checkpoint}.schema.json
catalog/{catalog-root,catalog-app-record,catalog-diff}.schema.json
```

Every Schema specifies `$schema`, `$id`, `type`/`format`, explicit identifier/digest/sequence/timestamp formats, required fields, strict unknown-field policy where security-critical, and at least one valid plus one invalid fixture.

---

## 5. Identifiers and basic encoding

Phase-one conventions:

```text
SHA-256 digest   → lowercase hex with `sha256:` prefix
Ed25519 key id   → `ed25519:` + lowercase hex SHA-256(public_key_bytes)
Publisher ID     → `pub1_` + base32lower(SHA-256(canonical genesis body))
Repository ID    → `repo1_` + base32lower(SHA-256(canonical trusted-root identity body))
Event ID         → `evt1_` + base32lower(SHA-256(canonical event body))
```

Base32 uses RFC 4648 lowercase alphabet without padding. Base64 fields use URL-safe encoding without padding.

Signed timestamps use RFC 3339 UTC:

```text
YYYY-MM-DDTHH:MM:SSZ
```

Local timezone offsets are not used in phase-one signed security objects.

---

## 6. Python Reference Implementation

Target:

```text
Python >= 3.12
```

Core dependencies:

```text
jsonschema
rfc8785
cryptography
python-tuf
pytest
```

Dependency API changes may require implementation adaptation but MUST NOT change protocol semantics.

### 6.1 `strict_json.py`

Only:

- UTF-8 decode;
- duplicate-key rejection;
- non-finite-number rejection;
- nesting/input-size limits;
- return ordinary Python structures.

Schema validation is separate.

### 6.2 `canonical.py`

- RFC 8785 JCS;
- unique UTF-8 bytes;
- canonical hash helper.

A home-grown “sorted JSON” serializer is not acceptable as JCS.

### 6.3 `schemas.py`

- load `spec/schemas/`;
- Draft 2020-12 validation;
- unified Schema errors;
- no silent input repair.

### 6.4 `crypto.py`

Only wraps:

```text
SHA-256
Ed25519 sign
Ed25519 verify
key fingerprint
```

No new cryptographic algorithm.

### 6.5 `identity.py`

Implements Publisher ID, Publisher Genesis, App Ownership, App Key Delegation, Root/App Key rotation, App Transfer, and Identity Lineage verification.

### 6.6 `signing.py`

Implements Release Statement and signature envelope. Inputs first pass Strict JSON + Schema validation.

### 6.7 `ikp.py`

Implements:

```text
ZIP safe parsing
Duplicate Entry detection
Path traversal rejection
uncompressed-size limits
manifest validation
files.json validation
Payload Hash
Publisher Identity Chain
Release Signature
Manifest / Release consistency
```

### 6.8 `repository.py`

Uses `python-tuf` for TUF semantics. Baga-specific code handles Target custom metadata, Release Records, content-addressed layout, and offline snapshot export/import.

### 6.9 `client.py`

Models trusted courier logic:

```text
Refresh Repository
Select Release
Download Target
verify Repository evidence
create Transfer Session
```

It is not the final trust root.

### 6.10 `device.py`

Models final device decision:

```text
Repository Evidence
+ IKP
+ Installed Identity
+ Compatibility Profile
+ Granted Permissions
→ ACCEPT / REQUIRE_APPROVAL / REJECT
```

---

## 7. Rust Independent Device Verifier

Phase-one binary:

```text
baga-verifier
```

Commands:

```text
baga-verifier canonical <json>
baga-verifier verify-statement <statement> <signature-envelope>
baga-verifier verify-ikp <file.ikp>
```

Rust reads the exact same:

```text
spec/vectors/
spec/fixtures/
```

It does not implement Market API, TUF Repository Generator, Catalog, Transparency server, or Review Policy.

Its purpose is to prove cross-language interoperability of device-critical verification semantics.

---

## 8. Canonical test vectors

Each vector directory contains:

```text
input.json
canonical.bin or canonical.hex
sha256.txt
metadata.json
```

Initial coverage:

```text
empty object
nested object
unicode
escaped characters
object-key ordering
arrays
integer boundaries
negative-zero handling
non-ASCII keys
Publisher Genesis
App Ownership
App Key Delegation
Release Statement
App Transfer
```

Invalid JCS / I-JSON inputs go to invalid corpus and have no canonical output.

Python and Rust MUST produce byte-for-byte identical canonical bytes and SHA-256.

---

## 9. Cryptographic vectors

Every vector fixes:

```text
test-only private-key seed
public key
key id
canonical statement bytes
statement sha256
signature
expected verification result
```

Production code MUST NOT load test private keys.

Initial vectors:

```text
Publisher Genesis
App Ownership
App Signing Delegation
Release Statement
App Key Rotation
Publisher Root Rotation
App Transfer
Revocation Statement
```

---

## 10. Invalid corpus

Invalid input is a first-class specification asset.

```text
spec/fixtures/invalid/
├── json/
├── schema/
├── identity/
├── signing/
├── ikp/
├── repository/
├── update/
└── transfer/
```

Initial cases include:

```text
duplicate-json-key
nan-number
infinity-number
unknown-critical-field
wrong-app-id
wrong-publisher-id
wrong-package-hash
wrong-package-length
invalid-ed25519-signature
undelegated-app-key
expired-delegation
revoked-key
broken-key-rotation-chain
unauthorized-app-transfer
release-sequence-rollback
same-sequence-different-digest
path-traversal-ikp
duplicate-zip-entry
zip-bomb-limit
permission-not-in-manifest
repository-mix-and-match
expired-timestamp
rollback-root
rollback-snapshot
offline-snapshot-incomplete
```

Each fixture declares:

```json
{
  "expected": "reject",
  "error_code": "...",
  "standard": "22",
  "rule": "..."
}
```

Tests assert stable error category, not merely that an exception occurred.

---

## 11. Error model

Shared error categories:

```text
invalid_json
invalid_schema
non_canonical_input
invalid_identifier
invalid_hash
invalid_signature
unknown_key
undelegated_key
expired_delegation
revoked_key
identity_mismatch
sequence_rollback
sequence_conflict
unsafe_path
duplicate_entry
resource_limit
repository_untrusted
metadata_expired
metadata_rollback
metadata_inconsistent
permission_escalation
incompatible
revoked_release
internal_error
```

Python and Rust should return the same category for the same fixture; human text may differ.

---

## 12. TUF Conformance

Provide:

```text
tools/tuf-client-under-test
```

implementing conformance commands such as:

```text
init
refresh
download
```

CI runs:

```text
theupdateframework/tuf-conformance@v2
```

Rules:

- TUF MUST requirements are not xfailed;
- Baga Repository Profile MUST requirements are not xfailed;
- optional unsupported algorithms/features MAY be explicitly xfailed with an explanation;
- Unexpected Pass triggers review to remove obsolete xfail.

---

## 13. Minimal Repository

Build a static repository fixture:

```text
examples/minimal-repository/
├── metadata/{root,timestamp,snapshot,targets}.json
└── targets/
    ├── packages/sha256/...ikp
    ├── releases/sha256/...json
    └── publishers/sha256/...json
```

It uses real Ed25519 test keys and real TUF Metadata. A local HTTP server is sufficient; no application server is required.

---

## 14. Minimal Client

No full UI. Commands:

```text
repo init
repo refresh
app list
app fetch
app prepare-transfer
```

Machine-readable JSON output. Responsibilities: TUF Refresh, Release selection, Target download/digest verification, Transfer Session generation. It cannot tell the device to skip final verification.

---

## 15. Minimal Device Prototype

No Kindle/Android UI emulation. Only trusted install state:

```text
state/
├── repositories/
├── installed-apps/
├── staging/
└── active/
```

Commands:

```text
device import-transfer
device verify
device stage
device activate
device health-ok
device health-fail
device rollback
```

State changes are observable and persistent. Phase one models atomic active-pointer switching on an ordinary filesystem.

---

## 16. Required End-to-End scenarios

```text
E2E-001 first install
Publisher → Sign IKP → Repository → Client → Device → Active

E2E-002 normal update
Release Sequence 1 → 2; new ACTIVE, old remains Last Known Good

E2E-003 corrupted download
Hash failure; never STAGED

E2E-004 wrong Publisher
same App ID, different Publisher, no Transfer → REJECT

E2E-005 Sequence rollback
current 2, repository offers 1 → automatic update REJECT

E2E-006 Permission escalation
new sensitive Permission → REQUIRE_APPROVAL

E2E-007 health failure
candidate fails probation → automatic rollback

E2E-008 interrupted update
download/stage/activate interruption → recover to coherent state

E2E-009 offline snapshot
device independently verifies without trusting Client

E2E-010 Security Revocation
revoked candidate cannot be newly installed/auto-updated
```

---

## 17. CI

`conformance.yml` runs:

```text
Python install
Schema tests
Strict JSON tests
Canonical vectors
Signature vectors
Invalid fixtures
IKP tests
Repository tests
Update tests
Rust verifier build/tests
Python ↔ Rust cross-language tests
End-to-End tests
```

`tuf-conformance.yml` builds/installs the reference client, runs official TUF conformance, and uploads failure artifacts.

Both run on Pull Request and `main` push.

---

## 18. Stable Gate

Before the governed standards can move from Draft to Stable:

```text
JSON Schema suite                 PASS
Strict JSON suite                 PASS
RFC 8785 canonical vectors        PASS
Positive signature vectors        PASS
Negative corpus                   PASS
Python IKP verifier               PASS
Rust independent verifier         PASS
Python/Rust byte-for-byte vectors PASS
TUF required conformance          PASS
Minimal Repository E2E            PASS
Offline Transfer E2E              PASS
Update / Rollback E2E             PASS
No unexplained xfail              PASS
```

Additional hard rule:

> **Any specification affecting signed byte representation, identity continuity, or update authorization MUST NOT be Stable until at least two independent implementations agree on the same vectors.**

---

## 19. Explicit non-goals for this phase

Not implemented in this phase:

- complete Market web service;
- ratings/comments;
- payment;
- DRM;
- commercial licensing;
- complete Transparency Log server;
- complete OEM Device Adapter;
- real Kindle / Android installer;
- Market UI client;
- cloud account system.

These are not required to validate the security/interoperability loop of Standards 21–28.

---

## 20. Implementation order

```text
Phase 1  repository scaffolding + Python project + CI baseline
Phase 2  Strict JSON + RFC8785 + JSON Schema
Phase 3  Identity + Signing + canonical vectors
Phase 4  IKP builder/verifier + invalid corpus
Phase 5  Rust verifier + cross-language vectors
Phase 6  python-tuf Repository + Client + TUF conformance CLI
Phase 7  Device Prototype + staged activation + rollback
Phase 8  End-to-End suite + Stable Gate report
```

Each phase starts with a failing test and ends with that test passing.

---

## 21. Success criteria

At completion we can demonstrate:

```text
same signed statement
→ Python and Rust produce identical canonical bytes
→ both verify the same Ed25519 signature

same valid IKP
→ both accept

same invalid IKP
→ both reject with the same error category

same Repository
→ TUF conformance client flow passes

same Release
→ Client transports evidence and Device independently re-verifies

failed update
→ previous known-good App remains intact
```

Only then do Standards 21–28 become executable and interoperable rather than merely plausible prose.
