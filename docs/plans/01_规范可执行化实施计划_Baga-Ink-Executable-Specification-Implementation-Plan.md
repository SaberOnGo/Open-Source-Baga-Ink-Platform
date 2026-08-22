# Baga Ink 规范可执行化实施计划 / Baga Ink Executable Specification Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans or superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把 `docs/standards/21–28` 变成可执行、可互操作、可自动拒绝错误输入的 Conformance Kit，并跑通最小 Repository → Client → Device 验证链。

**Architecture:** 机器规范位于 `spec/`；Python 是权威参考实现与 TUF 集成层；Rust 只实现独立设备关键验证链；两种语言共享相同测试向量与非法样本。所有自定义签名 JSON 使用 RFC 8785 JCS；TUF 元数据保持 TUF 自己的签名/序列化规则。

**Tech Stack:** Python 3.12+, pytest, jsonschema Draft 2020-12, rfc8785, cryptography, python-tuf, Rust stable, serde/serde_json, ed25519-dalek, sha2, zip, GitHub Actions, theupdateframework/tuf-conformance@v2.

**Spec:** `docs/design/01_规范可执行化_Baga-Ink-Executable-Specification-Design.md`

## Global Constraints

- 不引入新的重型中间执行层；实现属于 Baga Ink 标准/验证工具，不改变 Platform 的轻量定位。
- 自定义 Baga 签名对象 MUST 使用 RFC 8785 JCS；TUF metadata MUST 不经过 Baga JCS 重签。
- JSON Schema 使用 Draft 2020-12；安全关键对象默认 `additionalProperties: false`。
- 摘要使用 SHA-256；应用签名使用 Ed25519。
- Python Reference 与 Rust Verifier MUST 对同一 canonical/signature vectors 得到一致结果。
- 生产代码必须由先失败的自动化测试驱动；非法样本必须永久保留作为 regression corpus。
- TUF 客户端必须提供官方 conformance harness 要求的 `init`、`refresh`、`download` 命令。
- 21–28 保持 Draft；Stable Gate 全绿前不得改为 Stable。

---

## File Map

```text
spec/
  schemas/{identity,signing,repository,publishing,update,transfer,transparency,catalog}/
  vectors/{canonical-json,signatures,key-rotation,app-transfer,hashes}/
  fixtures/{valid,invalid}/
reference/python/
  pyproject.toml
  src/baga_spec/{errors,strict_json,canonical,schemas,crypto,identity,signing,ikp,repository,client,device}.py
reference/rust/baga-verifier/
  Cargo.toml
  src/{main,canonical,identity,signing,ikp}.rs
tools/{baga-spec,tuf-client-under-test,generate-vectors,build-test-ikp}
tests/
  test_strict_json.py
  test_schemas.py
  test_canonical.py
  test_crypto_vectors.py
  test_identity.py
  test_signing.py
  test_ikp.py
  test_invalid_fixtures.py
  test_repository.py
  test_update.py
  test_cross_language.py
  test_end_to_end.py
.github/workflows/{conformance,tuf-conformance}.yml
```

---

### Task 1: Python test harness + RED baseline

**Files:**
- Create: `reference/python/pyproject.toml`
- Create: `tests/conftest.py`
- Create: `tests/test_strict_json.py`
- Create: `.github/workflows/conformance.yml`

**Interfaces:**
- Produces `baga_spec.strict_json.loads_strict(data: str | bytes) -> object` contract for Task 2.

- [ ] Add Python project metadata and dependencies `pytest`, `jsonschema`, `rfc8785`, `cryptography`, `tuf`.
- [ ] Add failing tests asserting duplicate keys, NaN, Infinity and invalid UTF-8 are rejected and ordinary JSON parses.
- [ ] Add GitHub Actions job running `python -m pytest -q` on Python 3.12 and `cargo test` only when Rust project exists.
- [ ] Push test-only commit and verify CI fails because `baga_spec.strict_json` does not exist.

Expected failing assertion/import reason: `ModuleNotFoundError: No module named 'baga_spec'`.

---

### Task 2: Strict JSON parser

**Files:**
- Create: `reference/python/src/baga_spec/__init__.py`
- Create: `reference/python/src/baga_spec/errors.py`
- Create: `reference/python/src/baga_spec/strict_json.py`
- Modify: `tests/test_strict_json.py`

**Interfaces:**
- `class BagaSpecError(ValueError)`
- `class StrictJSONError(BagaSpecError)`
- `loads_strict(data: str | bytes) -> object`

- [ ] Implement duplicate-key detection with `object_pairs_hook`.
- [ ] Implement `parse_constant` rejection for NaN/Infinity.
- [ ] Decode bytes as strict UTF-8 and reject invalid sequences.
- [ ] Add nesting/input-size guards with conservative test values exposed as constants.
- [ ] Run tests; all strict-json tests must pass.

---

### Task 3: RFC 8785 canonicalization + deterministic vectors

**Files:**
- Create: `reference/python/src/baga_spec/canonical.py`
- Create: `tests/test_canonical.py`
- Create: `spec/vectors/canonical-json/README.md`
- Create deterministic vector files under `spec/vectors/canonical-json/`.

**Interfaces:**
- `canonicalize(value: object) -> bytes`
- `canonical_sha256(value: object) -> str` returning `sha256:<lowercase hex>`.

- [ ] Write failing RFC 8785-oriented tests for key ordering, Unicode, escapes, arrays and representative Publisher Genesis object.
- [ ] Implement by calling the `rfc8785` package rather than hand-written JSON sorting.
- [ ] Generate checked-in input/canonical-hex/SHA-256 vectors.
- [ ] Re-read vectors in tests and verify byte-for-byte output.

---

### Task 4: JSON Schema registry for 21–28

**Files:**
- Create 18 Draft 2020-12 schemas under `spec/schemas/` as defined by the design.
- Create: `reference/python/src/baga_spec/schemas.py`
- Create: `tests/test_schemas.py`
- Create representative valid/invalid JSON fixtures.

**Interfaces:**
- `schema_path(name: str) -> pathlib.Path`
- `validate_schema(name: str, instance: object) -> None`

- [ ] Start with tests for Publisher Genesis, App Ownership, App Key Delegation, Release Statement, Signature Envelope, Release Record, Revocation Statement, Transfer Session, Transparency Event and Catalog App Record.
- [ ] Require `$schema = https://json-schema.org/draft/2020-12/schema`, stable `urn:baga:schema:*` `$id`, required `type`/`format`, and `additionalProperties: false` on signed/security-critical objects.
- [ ] Add formats/patterns for `sha256:`, `ed25519:`, `pub1_`, non-negative sequence and UTC RFC3339 `...Z` timestamps.
- [ ] Expand to remaining schemas and ensure every schema has at least one valid and one invalid fixture.

---

### Task 5: Crypto primitives + Publisher identity chain

**Files:**
- Create: `reference/python/src/baga_spec/crypto.py`
- Create: `reference/python/src/baga_spec/identity.py`
- Create: `tests/test_crypto_vectors.py`
- Create: `tests/test_identity.py`
- Create fixed test-only vectors under `spec/vectors/signatures/`, `key-rotation/`, `app-transfer/`.

**Interfaces:**
- `sha256_digest(data: bytes) -> str`
- `ed25519_key_id(public_key: bytes) -> str`
- `sign_ed25519(seed32: bytes, message: bytes) -> bytes`
- `verify_ed25519(public_key: bytes, message: bytes, signature: bytes) -> None`
- `publisher_id(genesis: object) -> str`
- `verify_app_ownership(...) -> None`
- `verify_app_key_delegation(...) -> None`
- `verify_identity_chain(...) -> VerifiedIdentity`

- [ ] Write tests with fixed private seeds (test fixtures only) and expected public keys, signatures, IDs and hashes.
- [ ] Implement Ed25519 with `cryptography`; no custom crypto.
- [ ] Verify threshold signatures for Publisher Root documents.
- [ ] Verify App Ownership and App Signing Key Delegation scope (`publisher_id`, `app_id`, channel, validity and sequence range).
- [ ] Add negative tests for wrong publisher, wrong app, expired delegation, undelegated key and broken transfer chain.

---

### Task 6: Release signing and IKP verifier

**Files:**
- Create: `reference/python/src/baga_spec/signing.py`
- Create: `reference/python/src/baga_spec/ikp.py`
- Create: `tests/test_signing.py`
- Create: `tests/test_ikp.py`
- Create: `tools/build-test-ikp`
- Create valid and invalid IKP fixtures.

**Interfaces:**
- `build_files_manifest(entries: Mapping[str, bytes]) -> dict`
- `verify_release_statement(...) -> VerifiedRelease`
- `verify_ikp(path: Path, *, limits: IKPLimits = DEFAULT_LIMITS) -> VerifiedIKP`

- [ ] Test safe ZIP layout, payload hashing, manifest/release consistency and publisher signature.
- [ ] Reject path traversal, absolute path, duplicate ZIP entries, disallowed executable dependencies, wrong file hash/size and oversized expansion.
- [ ] Test `release_sequence`, `version_name`, `channel`, `permissions`, capabilities and data schema match between IKP Manifest and signed Release Statement.
- [ ] Build deterministic small `lifebook-demo.ikp` fixture.

---

### Task 7: Permanent invalid corpus

**Files:**
- Create: `spec/fixtures/invalid/**`
- Create: `spec/fixtures/manifest.json`
- Create: `tests/test_invalid_fixtures.py`

**Interfaces:**
- Fixture manifest entry: `{id, kind, path, expected_error_code}`.

- [ ] Add corpus cases: duplicate JSON key, non-finite number, unknown critical field, wrong app/publisher, bad signature, wrong hash/length, undelegated/expired/revoked key, broken rotation, unauthorized transfer, sequence rollback, same-sequence different digest, ZIP traversal, duplicate entry, oversized expansion, permission mismatch.
- [ ] Parameterize tests from the fixture manifest.
- [ ] Require exact stable machine-readable error codes, not string matching only.

---

### Task 8: Minimal TUF Repository + conformance adapter

**Files:**
- Create: `reference/python/src/baga_spec/repository.py`
- Create: `tests/test_repository.py`
- Create: `tools/tuf-client-under-test`
- Create: `.github/workflows/tuf-conformance.yml`

**Interfaces:**
- `build_test_repository(out_dir: Path, targets: Sequence[Target]) -> RepositoryFixture`
- TUF CUT CLI implements official `init`, `refresh`, `download` contract.

- [ ] Write tests that build Root/Targets/Snapshot/Timestamp using `python-tuf`, publish one content-addressed IKP target and refresh/download with a TUF client.
- [ ] Test expired Timestamp, rollback metadata, wrong target digest and mix-and-match rejection.
- [ ] Implement official TUF conformance CLI exactly (`init`, `refresh`, `download`).
- [ ] Add `theupdateframework/tuf-conformance@v2` workflow and allow xfails only for optional features outside the Baga TUF Profile.

---

### Task 9: Client, offline transfer and device decision model

**Files:**
- Create: `reference/python/src/baga_spec/client.py`
- Create: `reference/python/src/baga_spec/device.py`
- Create: `tests/test_update.py`
- Create transfer/offline fixtures.

**Interfaces:**
- `select_release(installed, releases, device_profile) -> ReleaseCandidate | None`
- `build_transfer_session(...) -> dict`
- `device_verify_install(evidence, ikp_path, installed_state) -> Decision`
- `Decision.status ∈ {ACCEPT, REQUIRE_APPROVAL, REJECT}`.

- [ ] Test latest-compatible selection rather than latest-overall selection.
- [ ] Test identity continuity and release-sequence monotonicity.
- [ ] Test new sensitive permissions produce `REQUIRE_APPROVAL`.
- [ ] Test signed offline snapshot survives untrusted transport but fails if any bytes are modified.
- [ ] Test withdrawn/unlisted/security-revoked distinction.

---

### Task 10: Rust independent verifier (RED → GREEN)

**Files:**
- Create: `reference/rust/baga-verifier/Cargo.toml`
- Create: `reference/rust/baga-verifier/src/{main,canonical,identity,signing,ikp}.rs`
- Create: `tests/test_cross_language.py`

**Interfaces:**
- CLI: `baga-verifier canonical <file>`
- CLI: `baga-verifier verify-statement <statement> <envelope>`
- CLI: `baga-verifier verify-ikp <file.ikp>`

- [ ] First add cross-language pytest that attempts to invoke `baga-verifier` and fails before Rust binary exists.
- [ ] Implement RFC 8785 compatible canonicalization using a maintained Rust crate or a narrowly reviewed implementation validated against checked-in vectors.
- [ ] Implement SHA-256 + Ed25519 verification and identity/signing checks.
- [ ] Implement IKP payload hash and core identity checks.
- [ ] Require every valid vector PASS and every supported invalid vector REJECT in both Python and Rust.

---

### Task 11: End-to-end Repository → Client → Device prototype

**Files:**
- Create: `tests/test_end_to_end.py`
- Create: `tools/baga-spec`
- Create: `tools/generate-vectors`
- Create minimal E2E fixtures under `spec/fixtures/e2e/`.

**Interfaces:**
- CLI `baga-spec verify-ikp FILE`
- CLI `baga-spec build-demo-repository DIR`
- CLI `baga-spec simulate-update REPOSITORY DEVICE_STATE`

- [ ] Generate test Publisher identity and signed `lifebook-demo` release 1.
- [ ] Publish into minimal TUF repository; reference client refreshes and downloads exact target.
- [ ] Device verifier accepts and activates release 1.
- [ ] Publish release 2; device selects, verifies, stages and accepts it.
- [ ] Corrupt package → REJECT.
- [ ] Roll back repository metadata → REJECT.
- [ ] Add sensitive permission → REQUIRE_APPROVAL.
- [ ] Simulate probation health failure → previous release remains last-known-good.

---

### Task 12: Stable Gate, CI matrix and documentation

**Files:**
- Modify: `.github/workflows/conformance.yml`
- Modify: `.github/workflows/tuf-conformance.yml`
- Create: `docs/conformance/01_可执行规范与稳定门槛_Baga-Ink-Conformance-and-Stable-Gate.md`
- Modify: `docs/standards/00_规范总览_Baga-Ink-Standards-Index.md`

**Interfaces:**
- Stable Gate is represented by CI job `stable-gate` and machine-readable test summary artifact.

- [ ] CI matrix: Python tests, Rust tests, Python↔Rust vectors, invalid corpus, E2E and TUF conformance.
- [ ] `stable-gate` depends on all required jobs and fails if any required test is skipped/xfail unexpectedly.
- [ ] Document exact promotion checklist; keep 21–28 Draft in this implementation.
- [ ] Verify no banned heavy middle-layer terminology reappears in current standards/docs.
- [ ] Final full test run and commit.

---

## Completion Criteria

Implementation is complete only when:

```text
JSON Schema tests                    PASS
Strict JSON tests                    PASS
RFC 8785 vectors                     PASS
Python crypto/signature vectors      PASS
Invalid corpus                       PASS
IKP verifier                         PASS
Repository/TUF tests                 PASS
TUF required conformance             PASS
Client/offline transfer              PASS
Rust verifier                        PASS
Python↔Rust vectors                  PASS
End-to-end update                    PASS
Stable Gate                          PASS
```

21–28 remain Draft until a later explicit Stable promotion review.