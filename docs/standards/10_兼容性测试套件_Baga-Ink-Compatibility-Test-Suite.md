# Baga Ink 兼容性测试套件 / Baga Ink Compatibility Test Suite

> **文档级别：一级平台规范**  
> **简称：BICTS**  
> **状态：Draft v0.4**  
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
Sandbox / Security
IKP install/update/recovery
```

内部可以用 KOReader、FBInk、SQLite、Automerge 或其他成熟组件；测试的是公开语义与安全边界。

---

# 1. 测试对象 / 报告

认证记录 SHOULD 包括：

```text
Device Model
Firmware / OS Range
Platform Version
Adapter Version
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

---

# 2. Base Mandatory

所有 Compatible 设备 MUST 通过：

```text
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
network.https            → HTTPS
storage.user_library     → LIBRARY_BRIDGE
reader.anchor            → READER_ANCHOR
```

---

# 3. CORE / Lua Profile

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

# 4. SQLite / `lsqlite3` Profile

`baga.data` 已撤销。数据库测试直接针对 SQLite / `lsqlite3`。

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

## 4.1 Transaction fault injection

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

## 4.2 Weak-sandbox platforms

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

# 5. Storage Sandbox

```text
STORAGE-001 appdata read/write
STORAGE-002 no access to other App private data
STORAGE-003 ../ escape rejected
STORAGE-004 unauthorized absolute path rejected
STORAGE-005 cache cleanup does not delete documents/app data
STORAGE-006 Platform update preserves app private data
STORAGE-007 resolve_path only resolves authorized logical paths
STORAGE-008 resolved path is runtime-local, not stable cross-device ID
```

---

# 6. IKP Install / Update / Rollback

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

# 7. Lifecycle / Power

验证：

```text
start / resume / pause / sleep / wake / stop
```

重点：

- committed SQLite data survives sleep/restart；
- wake 后重新评估 network/capability；
- App 不依赖永久进程；
- keep-awake 可被拒绝。

---

# 8. Display / Input

Display Base：

- 页面可见；
- size/orientation 正确；
- `AUTO/TEXT/QUALITY` 可合理实现或降级；
- region 越界安全；
- 不发生无意义连续全刷。

Input Base：

```text
focus_next
focus_previous
confirm
back
page_next
page_previous
```

Touch/Pen/Fast Refresh 等按声明 Capability 加测。

---

# 9. Permission

验证：

```text
Manifest not declared → reject
not granted → not_granted
denied → denied
granted → works
revoked → stops immediately
```

App-private SQLite DB 不需要额外用户资料 Permission，但必须受 Sandbox 约束。

---

# 10. Library Bridge

声明 `storage.user_library`：

```text
LIBRARY-001 list standard Library Item
LIBRARY-002 opaque ID, no raw path
LIBRARY-003 read obeys library.read
LIBRARY-004 write obeys library.write
LIBRARY-005 source can pass to baga.reader
LIBRARY-006 unsupported format fails cleanly
LIBRARY-007 rescan does not corrupt state
```

不得要求 EPUB-only / Kindle `/documents` / Android vendor DB schema。

---

# 11. Network / Offline-first

验证：

- online/offline state；
- Wi-Fi disconnect/reconnect；
- HTTPS；
- DNS/TLS/timeout；
- sleep interruption；
- wake retry；
- offline 不阻塞本地 App 启动。

---

# 12. Reader / Anchor

`reader.open`：

```text
open
next/previous
position
close/reopen
restore
```

不得把 EPUB 固定成测试格式。

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

---

# 13. Automerge Adopted Foundation

Automerge 不是 Base Device Capability，也不是所有 IKP 强制依赖。

实际采用 Automerge 的功能才运行对应测试。

## 13.1 Document / Merge

```text
AM-001 independent changes on two replicas
AM-002 merge converges
AM-003 repeated merge idempotent
AM-004 binary save/load preserves state
AM-005 history survives restart
```

## 13.2 Sync protocol（若采用）

```text
AM-SYNC-001 peers converge over supported transport
AM-SYNC-002 interrupted sync resumes safely
AM-SYNC-003 duplicate messages harmless
AM-SYNC-004 version/protocol mismatch explicit
```

如果只用 document/merge，不用 sync protocol，则 Sync suite 可以 SKIP。

BICTS 不要求 automerge-repo，也不把其 Storage/Network Adapter 架构当标准。

---

# 14. LifeBook Smoke Test

MAY 包括：

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

LifeBook 通过不能替代基础 Probe。

---

# 15. Firmware Regression

固件 / OS 升级最少重跑：

```text
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

---

# 16. Compatibility Report

报告 SHOULD 包括：

```json
{
  "device": {},
  "firmware": "...",
  "platform_version": "...",
  "adapter_version": "...",
  "lua_profile": "...",
  "sqlite_version": "...",
  "lsqlite3_version": "...",
  "reader_backend": "...",
  "automerge_version": null,
  "bicts_version": "0.4",
  "tests": {}
}
```

---

# 17. Certification Gate

正式 Baga Ink Compatible：

- Base Mandatory 100% PASS；
- Lua Profile / SQLite Profile PASS；
- Stable Capability tests PASS；
- 无 Critical data-loss / sandbox escape；
- Experimental/provisional 不冒充 Stable。

---

# 18. 核心原则

> **BICTS 证明的是 Baga Ink API、Lua Profile、Standard Libraries 和安全边界真正成立。SQLite 直接按 SQLite 测；Automerge 按实际采用模块测；不再测试已经撤销的 `baga.data`。**