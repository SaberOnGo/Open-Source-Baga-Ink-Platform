# Baga Ink 兼容性测试套件 / Baga Ink Compatibility Test Suite

> **文档级别：一级平台规范**  
> **简称：BICTS**  
> **状态：Draft v0.6**  
> **日期：2026-08-23**  
> **上位文档：`08_兼容性标准_Baga-Ink-Compatibility-Standard.md`**  
> **配套规范：`03_API规范_Baga-Ink-API-Specification.md`、`04_能力注册表_Baga-Ink-Capability-Registry.md`、`07_设备适配器规范_Baga-Ink-Device-Adapter-Specification.md`、`09_UI规范_Baga-Ink-UI-Specification.md`、`13_标准库与成熟组件采用规范_Baga-Ink-Standard-Libraries-and-Adopted-Components.md`**

---

## 0. 目的

BICTS 验证某个：

```text
Device + Firmware/OS + Platform + Adapter + Lua Profile
```

组合是否真正符合 Baga Ink。

测试覆盖：

```text
Baga Ink API / Capability
Baga Lua Profile / Standard Libraries
Device Adapter integration
Sandbox / Security
IKP install/update/recovery
Lifecycle / Power
Reference App behavior
```

内部可以用 KOReader、FBInk、SQLite、Automerge 或其他成熟组件；BICTS 测试的是公开语义、安全边界和整机组合。

正式测试文档只覆盖当前有效设计。

---

# 1. Adapter Contract Tests 与 BICTS 必须分开

Device Adapter 开发存在两个不同测试层级。

## 1.1 Adapter Contract Tests

直接针对 `07 Device Adapter Contract` 的实现。

它回答：

> **这个 Adapter 是否正确实现了 Device Adapter Contract？**

覆盖：

```text
Factory / probe
Descriptor
Capability consistency
Display subsystem
Input normalization
Storage containment
Lifecycle mapping
Power contract
Optional subsystems
Error normalization
Device Profile / Quirk selection
Self-test
```

Adapter Contract Tests 可以大量在 host/mock 环境和真实设备上运行。

## 1.2 BICTS

BICTS 回答：

> **这个 Device + Firmware/OS + Platform + Adapter + Lua Profile 组合能否宣称 Baga Ink Compatible？**

因此：

```text
Adapter Contract Tests PASS
≠
Baga Ink Compatible
```

正式认证仍必须通过 BICTS。

同样，如果某设备 BICTS 出现 Adapter 相关故障，SHOULD 回落到 Adapter Contract Tests 定位具体 subsystem，而不是只在 LifeBook 业务里调试。

---

# 2. 测试对象 / 报告

认证记录 SHOULD 包括：

```text
Device Model
Firmware / OS Range
Platform Version
Adapter Contract Version
Adapter Version
Device Profile Version
Quirk Set Version
Baga Lua Profile Version
Compatibility Standard Version
BICTS Version
SQLite / lsqlite3 version
Reader implementation/version
Automerge version（若实际采用）
```

结果：

```text
PASS
FAIL
SKIP_NOT_APPLICABLE
BLOCKED
WARNING
```

Adapter Contract Test evidence SHOULD 与最终 Compatibility Report 关联。

---

# 3. Base Mandatory

所有 Compatible 设备 MUST 通过：

```text
ADAPTER_INTEGRATION
CORE
LUA_PROFILE
SQLITE_PROFILE
LIFECYCLE
DISPLAY_BASE
INPUT_NAVIGATION
STORAGE_SANDBOX
IKP_INSTALL
IKP_UPDATE
PERMISSION_BASE
POWER_SLEEP_WAKE
ERROR_MODEL
RECOVERY
REFERENCE_APP_BASE
```

Optional Capability 存在时运行对应 suite，例如：

```text
input.touch             → TOUCH
input.pen               → PEN
display.partial_refresh → PARTIAL_REFRESH
network.https           → HTTPS
storage.user_library    → LIBRARY_BRIDGE
reader.anchor           → READER_ANCHOR
```

---

# 4. ADAPTER_INTEGRATION

整机 BICTS 至少验证：

```text
ADAPTER-001 Platform loads selected Adapter
ADAPTER-002 Adapter Contract major is compatible
ADAPTER-003 DeviceDescriptor readable and coherent
ADAPTER-004 Base mandatory subsystems present
ADAPTER-005 Capability Snapshot matches subsystem availability
ADAPTER-006 unknown/unsupported device state fails conservatively
ADAPTER-007 Device Profile / Quirk metadata is diagnosable
ADAPTER-008 Adapter event enters Platform Core, not App directly
ADAPTER-009 raw Vendor/OS object does not leak to App
ADAPTER-010 quick self-test completes non-destructively
```

Device-family specific Contract Tests 由对应 `11/12/...` 文档扩展。

---

# 5. CORE / Lua Profile

至少验证：

```text
CORE-001 Platform boots
CORE-002 Adapter loads
CORE-003 API version readable
CORE-004 Standard IKP Lua entry executes
CORE-005 unsupported API fails safely
CORE-006 device/vendor private objects do not leak

LUA-001 required base libraries load
LUA-002 dangerous raw shell unavailable/restricted
LUA-003 arbitrary native module load blocked
LUA-004 require("lsqlite3") succeeds
LUA-005 Standard Library version metadata readable
```

SQLite / `lsqlite3` 是正式 Standard Library，公开名称不属于 implementation leak。

---

# 6. SQLite / `lsqlite3` Profile

数据库测试直接针对 SQLite / `lsqlite3`。

最低：

```text
SQLITE-001 require("lsqlite3") succeeds
SQLITE-002 open DB in current App sandbox
SQLITE-003 CREATE / INSERT / SELECT raw SQL
SQLITE-004 prepared statement + bind
SQLITE-005 transaction commit atomic
SQLITE-006 rollback leaves no partial writes
SQLITE-007 committed data survives app/process restart
SQLITE-008 DB survives Platform update
SQLITE-009 foreign keys can be enforced
SQLITE-010 BLOB round trip
SQLITE-011 JSON functions available
SQLITE-012 FTS5 available
SQLITE-013 WAL available when filesystem/locking profile allows
SQLITE-014 arbitrary loadable extension disabled
SQLITE-015 App A cannot open App B private DB
SQLITE-016 direct unauthorized absolute/path-traversal DB open rejected
SQLITE-017 disk-full / IO error fails safely
SQLITE-018 ATTACH DATABASE outside sandbox rejected
SQLITE-019 URI filename / vfs= override cannot select unauthorized VFS
SQLITE-020 symlink/canonical-path escape outside sandbox rejected
SQLITE-021 journal/WAL/SHM/temp files remain inside allowed storage boundary
```

## 6.1 Transaction fault injection

```text
A=1, B=1
BEGIN
A=2
B=2
inject failure before/during COMMIT
restart
```

结果只能是：

```text
(A=1,B=1)
或
(A=2,B=2)
```

不得半事务。

## 6.2 Weak-sandbox platforms

Kindle 等缺少 per-App OS sandbox 的设备，MUST 额外证明 sandbox-aware SQLite VFS / 等价 I/O confinement 有效。

测试必须覆盖：

```text
main DB
ATTACH DB
journal
WAL
SHM
temp DB
xOpen/xDelete/xAccess/xFullPathname equivalent behavior
```

仅测试 `baga.storage.resolve_path()` 返回合法路径不足以通过 SQLite Sandbox 测试。

---

# 7. Storage Sandbox

```text
STORAGE-001 appdata read/write
STORAGE-002 no access to other App private data
STORAGE-003 ../ escape rejected
STORAGE-004 unauthorized absolute path rejected
STORAGE-005 cache cleanup does not delete documents/app data
STORAGE-006 Platform update preserves app private data
STORAGE-007 resolve_path only resolves authorized logical paths
STORAGE-008 resolved path is runtime-local, not stable cross-device ID
STORAGE-009 Adapter native root cannot escape configured Platform boundary
STORAGE-010 symlink/canonical containment survives restart
```

---

# 8. IKP Install / Update / Rollback

必须验证：

```text
valid IKP install
invalid container/path rejected
bad API/Profile range rejected
missing required capability rejected
bad signature rejected
update success
update failure rollback
user data / SQLite DB preserved
```

关键场景：

```text
install v1
create SQLite schema + user data
attempt broken v2
update fails
v1 still starts
DB still readable and consistent
```

---

# 9. Lifecycle / Power

验证：

```text
start / resume / pause / sleep / wake / stop
```

重点：

- Adapter sleep/wake event 映射正确；
- committed SQLite data survives sleep/restart；
- wake 后重新评估 network/capability/runtime state；
- App 不依赖永久进程；
- keep-awake 可被拒绝；
- Device callback 不绕过 Platform Core 直接触达 App。

---

# 10. Display / Input

## Display Base

- 页面可见；
- size/orientation 正确；
- `AUTO/TEXT/QUALITY` 可合理实现或安全降级；
- region 越界安全；
- 不发生无意义连续全刷；
- Vendor waveform / refresh ID 不泄漏；
- Adapter capability 与真实 refresh behavior 一致。

## Input Base

```text
focus_next
focus_previous
confirm
back
page_next
page_previous
```

验证：

- raw Kindle/Android/Vendor keycode 不泄漏；
- Pointer/Pen 只在 capability 声明时出现；
- 事件顺序经 Platform Core 归一化。

Touch/Pen/Fast Refresh 等按声明 Capability 加测。

---

# 11. Permission

验证：

```text
Manifest not declared → reject
not granted → not_granted
denied → denied
granted → works
revoked → stops immediately
```

App-private SQLite DB 不需要额外用户资料 Permission，但必须受 Sandbox 约束。

Adapter 不得成为绕过 Permission 的高权限逃生口。

---

# 12. Library Bridge

声明 `storage.user_library`：

```text
LIBRARY-001 list standard Library Item
LIBRARY-002 opaque ID, no raw path
LIBRARY-003 read obeys library.read
LIBRARY-004 write obeys library.write
LIBRARY-005 source can pass to baga.reader
LIBRARY-006 unsupported format fails cleanly
LIBRARY-007 rescan does not corrupt state
LIBRARY-008 Adapter/Vendor private DB object does not leak
```

测试格式从当前 Reader implementation 声明支持的格式集合中选择，不固定 EPUB，也不依赖 Kindle `/documents` 或 Android vendor DB schema。

---

# 13. Network / Offline-first

验证：

- online/offline state；
- Adapter network events；
- Wi-Fi disconnect/reconnect；
- HTTPS；
- DNS/TLS/timeout；
- sleep interruption；
- wake retry；
- offline 不阻塞本地 App 启动；
- shared HTTP/TLS stack 与 Adapter connectivity bridge 可以独立实现而不改变 App contract。

---

# 14. Reader / Anchor

`reader.open`：

```text
open
next/previous
position
close/reopen
restore
```

测试使用当前 Reader implementation 实际支持的格式，不把 EPUB 固定成标准格式。

`reader.anchor`：

```text
create
serialize
close/reopen
goto/resolve
stale anchor safe failure
exact/approximate explicit
```

如同时支持 rolling/reflowable 与 paging/fixed-page，SHOULD 各测一种真实支持格式。

不把 XPointer / pboxes / EPUB CFI / Readium Locator 当公共测试输入。

Reader 是 Platform shared capability；BICTS MUST 不要求它作为 Device Adapter 顶层 subsystem。

---

# 15. Automerge Adopted Foundation

Automerge 不是 Base Device Capability，也不是所有 IKP 强制依赖。

实际采用 Automerge 的功能才运行对应测试。

## 15.1 Document / Merge

```text
AM-001 independent changes on two replicas
AM-002 merge converges
AM-003 repeated merge idempotent
AM-004 binary save/load preserves state
AM-005 history survives restart
```

## 15.2 Sync protocol（若采用）

```text
AM-SYNC-001 peers converge over supported transport
AM-SYNC-002 interrupted sync resumes safely
AM-SYNC-003 duplicate messages harmless
AM-SYNC-004 version/protocol mismatch explicit
```

如果只用 document/merge，不用 sync protocol，则 Sync suite 可以 SKIP。

BICTS 不要求 automerge-repo，也不把其 Storage/Network Adapter 架构当标准。

---

# 16. LifeBook / Probe Smoke Test

Baga SHOULD 优先维护一个小型 Probe IKP，验证 Platform 基础能力，再运行 LifeBook smoke test。

Probe SHOULD 覆盖：

```text
start
simple Page/Text/Button/List
navigation
SQLite write/read
sleep/wake
offline start
capability display
```

LifeBook Smoke MAY 包括：

```text
start
open library
open one supported document
page turn
save reading position
create note
SQLite write/read
sleep/wake
restore
offline start
```

LifeBook 通过不能替代 Probe、Adapter Contract Tests 或 Base BICTS。

---

# 17. Device Profile / Quirk Regression

当 Adapter 采用 Device Profile / Quirk 时，测试证据 SHOULD 绑定：

```text
profile_id
quirk_set_id
model
firmware range
adapter version
```

至少验证：

```text
PROFILE-001 exact match selects expected profile
PROFILE-002 unknown firmware is conservative
PROFILE-003 build target is independent from model profile
QUIRK-001 quirk applies only to declared match range
QUIRK-002 quirk does not alter public capability semantics
QUIRK-003 workaround removal/change requires regression evidence
```

---

# 18. Firmware Regression

固件 / OS 升级最少重跑：

```text
ADAPTER_INTEGRATION
CORE
LUA_PROFILE
SQLITE_PROFILE
LIFECYCLE
DISPLAY
INPUT
STORAGE
IKP
RECOVERY
```

Reader/Library/Network 受影响时加跑对应 suite。

如果 Device Profile / Quirk match 发生变化，也必须重跑对应 Adapter Contract Tests。

---

# 19. Compatibility Report

报告 SHOULD 包括：

```json
{
  "device": {},
  "firmware": "...",
  "platform_version": "...",
  "adapter_contract_version": "...",
  "adapter_version": "...",
  "device_profile": "...",
  "quirk_set": "...",
  "lua_profile": "...",
  "sqlite_version": "...",
  "lsqlite3_version": "...",
  "reader_backend": "...",
  "automerge_version": null,
  "bicts_version": "0.6",
  "adapter_contract_tests": {},
  "tests": {}
}
```

---

# 20. Certification Gate

正式 Baga Ink Compatible：

- Adapter Contract major compatible；
- Base Adapter Contract evidence PASS；
- Base Mandatory BICTS 100% PASS；
- Lua Profile / SQLite Profile PASS；
- Stable Capability tests PASS；
- 无 Critical data-loss / sandbox escape；
- Experimental/provisional 不冒充 Stable；
- Device Profile / Quirk / firmware 范围明确；
- Adapter self-test 不存在阻断级故障。

---

# 21. 核心原则

> **Adapter Contract Tests 证明“设备适配实现正确”；BICTS 证明“整台设备上的 Baga Ink Platform 真的兼容”。两层都必须存在，不能让 LifeBook 是否能启动成为唯一兼容判断。**
