# Baga Ink Update, Rollback and Revocation Protocol

> **Document level:** Core Device Distribution Protocol  
> **Document ID:** `standards.25`  
> **Locale:** English (`en`)  
> **Status:** Draft v0.1  
> **Date:** 2026-08-22  
> **Parent:** `docs/en/standards/20_baga-ink-market-and-distribution-architecture.md`  
> **Repository:** Standard 23  
> **Publishing:** Standard 24  
> **Counterpart:** `docs/zh-CN/standards/25_应用更新回滚与撤销协议.md`

---

## 0. Purpose

This document defines how Baga Ink Platform discovers updates, chooses a device-compatible candidate, compares identity/permissions/data schema, downloads full IKP or optional delta, stages installation, activates atomically, confirms health, rolls back automatically, performs explicit downgrade, handles withdrawal/revocation, and remains recoverable through network loss, power loss, storage exhaustion, and sleep/wake.

Core rule:

> **Download is not installation; verification is not activation; activation is not health. Each stage must succeed independently.**

---

## 1. Update identity prerequisite

A candidate must first prove it is authorized to replace the installed application.

Default requirements:

```text
candidate.app_id == installed.app_id
candidate.publisher_id == installed.publisher_id
Publisher Identity Chain valid
App Ownership valid
App Signing Key Delegation valid
Repository Source Policy valid
```

A changed Publisher requires a complete valid App Transfer Chain.

Same `app_id` under a different Publisher Identity is not an update. It can only be treated as a new trust identity after explicit user reset/handling of the previous application identity and data.

---

## 2. Local installation record

The Platform MUST atomically persist formal installed-app state such as:

```json
{
  "app_id": "com.example.reader",
  "publisher_id": "pub1_...",
  "source_repository_id": "repo1_...",
  "channel": "stable",
  "current_release_sequence": 142,
  "current_version_name": "1.4.2",
  "current_package_sha256": "...",
  "current_data_schema_version": 4,
  "permissions_granted": [],
  "last_known_good_release": 141,
  "update_state": "idle"
}
```

This record MUST be checked against the actually active package. The Platform MUST NOT infer current version merely from a directory name.

---

## 3. Candidate selection

Platform / Client filtering order:

```text
1. Repository Metadata trusted
2. Release status installable
3. App Identity continuity valid
4. Source Repository policy valid
5. selected Channel
6. Release Sequence higher than current
7. Baga API range compatible
8. Required Capabilities satisfied
9. Device compatibility status allows install
10. Package not security-revoked
11. rollout cohort eligible
12. Permission and data-migration policy acceptable
```

When the latest overall release is incompatible, select the **Latest Compatible Release** rather than treating the application as completely unavailable.

---

## 4. Release Sequence

Automatic update requires:

```text
candidate.release_sequence > current.release_sequence
```

`version_name` is not a security ordering field.

For equal Release Sequence:

- equal Digest → same release;
- different Digest → security conflict, reject;
- channel changes do not permit reuse;
- repository changes do not permit different bytes for the same identity/Sequence.

A lower Release Sequence is accepted only through explicit Downgrade or automatic rollback to a locally known-good release.

---

## 5. Update state machine

```text
IDLE
  │
  ▼
METADATA_VERIFIED
  │
  ▼
CANDIDATE_SELECTED
  │
  ▼
AWAITING_USER_APPROVAL      optional
  │
  ▼
DOWNLOADING
  │
  ▼
PACKAGE_VERIFIED
  │
  ▼
STAGED
  │
  ▼
ACTIVATING
  │
  ▼
PROBATION
  │
  ├── healthy ───────→ ACTIVE
  │
  └── failed ────────→ ROLLING_BACK
                              │
                              ▼
                         PREVIOUS_ACTIVE
```

Every intermediate state MUST be recoverable or safely cleanable after reboot.

---

## 6. State persistence / journal

Important transitions persist a Journal containing at least:

```text
operation_id
app_id
from_release
candidate_release
state
staging_path
expected_digest
previous_active_path
started_at
last_updated_at
```

Recovery:

- `DOWNLOADING` → resume or remove temporary data;
- `PACKAGE_VERIFIED` → re-check and continue;
- `STAGED` → re-verify then activate;
- `ACTIVATING` → inspect active pointer and package integrity;
- `PROBATION` → continue health checks or roll back if reboot cause is uncertain;
- `ROLLING_BACK` → prioritize previous known-good recovery;
- temporary directories without a complete Journal MUST NOT auto-activate.

---

## 7. Download and cache

Downloads MUST:

- write only to staging;
- enforce Metadata-declared maximum length;
- stream SHA-256 calculation;
- support safe resume;
- re-check total length after completion;
- not treat HTTP 200 as success by itself;
- not treat file extension as proof of IKP validity;
- never modify the active App on download failure;
- re-verify Digest even for cache hits.

Complete IKP cache MAY deduplicate by content digest.

---

## 8. Full package verification

Before `PACKAGE_VERIFIED`, verify:

```text
Repository target length and SHA-256
IKP container / path safety
IKP file-manifest hashes
Publisher Identity Chain
App Ownership
App Signing Key Delegation
Release Signature
Manifest / Release Record consistency
Release Sequence
Revocation status
API / Capability / Permission
resource limits
```

Any failure blocks staging.

---

## 9. Staged Install

A verified IKP is installed into a new immutable version directory, e.g.:

```text
apps/<app_id>/versions/<release_sequence>-<digest>/
```

The active release is selected by a small atomic pointer:

```text
apps/<app_id>/current
```

Filesystem implementation may differ, but it MUST ensure:

- previous release remains complete;
- new release never overwrites old package files;
- new release is fully persisted before pointer switch;
- pointer switch either completes or leaves old pointer intact;
- App private data is separate from package bytes;
- package update does not delete App data by default.

---

## 10. Activation

```text
1. safely stop/pause current App
2. flush current App state
3. re-verify staged package digest when required
4. prepare data-migration snapshot according to policy
5. atomically switch active package pointer
6. start candidate in probation mode
7. run health checks
8. mark candidate last-known-good only after success
```

If steps 1–5 fail, continue using the previous release.

---

## 11. Health confirmation

Before `ACTIVE`, the candidate passes minimum health checks:

```text
package loads
entry point starts
no immediate uncaught startup failure
App responds to lifecycle / UI event loop
App sandbox accessible
mandatory startup deadline met
no repeated crash loop
```

An App MAY report standardized readiness such as:

```text
startup_ready
basic_state_loaded
migration_complete
```

but self-reported health does not replace Platform crash/timeout detection.

High-risk updates MAY use a longer Probation Window.

---

## 12. Crash Loop

Platform MUST detect a bounded number of startup failures within a bounded time window. Exact thresholds are Platform Profile policy.

On candidate Crash Loop:

1. stop automatic candidate restarts;
2. mark the Release `local-failed`;
3. roll back to previous known-good release;
4. retain diagnostics;
5. preserve user data;
6. suppress immediate automatic retry of the same Digest;
7. tell the user that details/retry are available.

---

## 13. Automatic rollback

Automatic rollback target is:

```text
last_known_good_release
```

not an arbitrary older release.

It requires:

- locally complete and already verified target package;
- same installed Publisher Identity;
- local Package Digest matches recorded value;
- target is not Security Revoked;
- current data schema is safely readable by the old release or a recoverable snapshot exists;
- rollback cause/result recorded in local audit log.

After rollback, the same failed Digest MUST NOT be immediately auto-installed again.

---

## 14. Explicit Downgrade

User-selected lower Release Sequence is a Downgrade.

Downgrade MUST:

- show current and target releases;
- re-verify Publisher Identity;
- reject Security Revoked target;
- evaluate Data Schema compatibility;
- warn about possible feature/data loss;
- require user confirmation;
- NOT be implemented by accepting old Repository Metadata;
- use a target described by current trusted Repository state or an already verified local package.

Market / Platform MAY prohibit downgrade to known-insecure releases.

---

## 15. Data Schema migration

A Release declares:

```text
data_schema_version
rollback.mode
rollback.minimum_compatible_schema
```

### 15.1 `safe`

The previous release can still read candidate-written data. Automatic rollback may not require full App-data restoration, but writes still need atomicity.

### 15.2 `snapshot-required`

Before activation, create an App-private-data snapshot or equivalent transactional recovery point. Rollback restores it.

### 15.3 `forward-only`

After migration, an old release cannot safely read the data.

Requirements:

- prominently disclose before Stable automatic update;
- prefer backup/export of recoverable user data;
- Platform cannot promise automatic rollback;
- perform as much health validation as possible before irreversible commit;
- App provides recovery or re-sync strategy;
- high-risk/low-resource devices MAY disable automatic installation by default.

---

## 16. Two-phase data migration

Recommended:

```text
Prepare migration
      │
      ▼
Create snapshot / transaction
      │
      ▼
Run migration in candidate namespace
      │
      ▼
Validate migrated data
      │
      ▼
Activate candidate
      │
      ▼
Commit migration after health confirmation
```

Migration SHOULD be re-entrant or detect completion, survive sleep/wake without repeated corruption, use its own Journal, never run before package verification, and stop when the update is cancelled.

---

## 17. Permission Diff

Compare:

```text
current declared permissions
candidate declared permissions
current granted permissions
```

Classify:

```text
No change
Removed permissions
Added low-risk permissions
Added sensitive permissions
Changed scope / semantics
```

Rules:

- removed Permissions may be automatically narrowed;
- a newly declared Permission does not inherit an old Grant;
- newly sensitive Permission requires user confirmation;
- user rejection may cancel update or, if the App supports it, install with that Permission denied;
- Permission Registry semantic change requires re-review;
- App Transfer does not automatically grant new permissions.

---

## 18. Channel switching

Automatic update selects candidates only from the subscribed Channel.

- Stable → Beta: explicit confirmation;
- Beta → Stable with lower Stable Sequence: Downgrade rules;
- Nightly: automatic install off by default or strongly disclosed;
- Security Revocation MAY recommend a safe release from another Channel, but identity/permission checks still apply.

---

## 19. Phased rollout cohort

Eligibility MAY use:

```text
bucket
=
Hash(install_cohort_id || rollout_id) mod 10000
```

Rules:

- `install_cohort_id` is locally random;
- device serial, IMEI, advertising ID, or account is not required input;
- same `rollout_id` gives a stable result on the same install;
- rollout percentage can expand or pause but cannot change the release bytes;
- devices already installed do not roll back merely because rollout percentage shrinks;
- pausing rollout prevents new activation only.

---

## 20. Delta Update

Delta is an optional optimization, not an independent release.

Delta Record:

```text
base_package_sha256
base_release_sequence
target_package_sha256
target_release_sequence
delta_sha256
delta_length
algorithm
```

Rules:

- apply only when local Base Digest exactly matches;
- Delta itself is a verified Repository Target;
- after apply, verify complete target IKP length + SHA-256;
- final IKP still passes Publisher Signature verification;
- on delta failure/storage shortage, fall back to full IKP;
- delta MUST NOT bypass Permission / Manifest / Signature verification;
- v0.1 does not freeze a particular delta algorithm.

---

## 21. Release Status

### `active`

Eligible for discovery, new installation, and update.

### `superseded`

A newer release exists, but this release may remain valid for older compatible devices or safe rollback.

### `withdrawn`

Publisher/Market no longer recommends new installation, typically for an ordinary bug.

Default:

- not recommended to new users;
- installed release continues to run;
- recommend replacement when available;
- local rollback may use it if no security issue exists.

### `unlisted`

Hidden from ordinary search/recommendation, while direct reference, existing-user update, or enterprise deployment may remain allowed by policy.

### `security-revoked`

Malware, key compromise, or serious security defect.

Default:

- block new installation;
- block as automatic rollback target;
- stop update into it;
- show security warning;
- recommend fixed/safe replacement;
- whether launch is blocked depends on severity and Platform Security Policy.

---

## 22. Security Revocation severity

```text
low
medium
high
critical
```

### Low / Medium

Warn, stop new installs, recommend update; do not normally force-stop the installed App.

### High

Strong warning, block new install/reinstall, prohibit rollback into the release, MAY restrict sensitive Permissions, recommend immediate update/disable.

### Critical

For confirmed active malicious behavior, credential theft, or large-scale destructive risk.

Platform MAY:

- block launch;
- revoke sensitive App permissions;
- quarantine package;
- preserve user data for safe migration/export;
- require explicit user disposition.

v0.x does not define “Market silently remotely deletes App and user data” as the default capability.

Any forced action MUST be based on a signed Security Revocation Record and recorded in local audit state.

---

## 23. Revocation Record verification

A Revocation Record MUST:

- be verified as a Repository Target;
- bind App ID, Release Sequence, and Package Digest;
- be signed by Repository Security Role or an explicitly Root-authorized role;
- include Severity, Reason Code, Effective Time;
- MAY point to a replacement Release;
- be represented in Transparency Log;
- not be replaced by ordinary Catalog text.

A Publisher MAY request Security Revocation, but Repository independently signs its publication.

---

## 24. Repository unavailable / long-offline behavior

If Repository is unavailable, Timestamp expired, or device is long offline:

- installed Apps continue to run;
- no new update is discovered;
- inability to prove fresh safety state is not the same as proving the App revoked;
- already trusted local Revocation evidence remains effective;
- Client may import a fresh offline Repository Snapshot;
- setting system clock backward cannot extend trusted Metadata lifetime.

---

## 25. User data

Across update, rollback, withdrawal, or revocation:

- user books are not deleted by default;
- user notes are not deleted by default;
- App-private user data is not deleted by default;
- package bytes and user data remain separate;
- uninstall and clear-data are separate actions;
- even Critical quarantine SHOULD preserve a safe data-export path where possible;
- destructive migrations require explicit disclosure.

---

## 26. Update audit record

Platform SHOULD record:

```text
operation_id
app_id
from_release
to_release
repository_id
package_digest
publisher_id
permission_diff
data_schema_transition
verification_result
activation_result
health_result
rollback_result
timestamps
```

Normal update logs MUST NOT contain book contents, note bodies, tokens, credentials, or other sensitive user content.

---

## 27. Recommended automatic-update policy

Default recommendation:

- Stable Channel;
- same Publisher Identity;
- same Source Repository;
- higher Release Sequence;
- no newly added sensitive Permission without approval;
- Data Schema `safe` or automatically snapshot-able;
- Device Compatibility verified;
- not Security Revoked;
- network/power conditions suitable;
- Platform chooses a low-disruption activation time after download completes.

Otherwise require user confirmation or retain the current release.

---

## 28. Final rule

> **The objective is not to keep every device on the numerically newest release. It is to keep the device on the newest safe release whose identity is correct, compatibility is proven, permissions are acceptable, and user data remains recoverable.**
