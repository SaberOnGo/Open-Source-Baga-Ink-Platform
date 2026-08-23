# Baga Ink 兼容性测试套件 / Baga Ink Compatibility Test Suite

> **文档级别：一级平台规范**  
> **简称：BICTS**  
> **状态：Draft v0.3**  
> **日期：2026-08-23**  
> **上位文档：`08_兼容性标准_Baga-Ink-Compatibility-Standard.md`**  
> **配套规范：`03_API规范_Baga-Ink-API-Specification.md`、`04_能力注册表_Baga-Ink-Capability-Registry.md`、`07_设备适配器规范_Baga-Ink-Device-Adapter-Specification.md`、`09_UI规范_Baga-Ink-UI-Specification.md`、`13_标准库与成熟组件采用规范_Baga-Ink-Standard-Libraries-and-Adopted-Components.md`**

---

## 0. 目的 / Purpose

BICTS 回答：

> **某个“设备 + 固件 + Baga Ink Platform + Device Adapter”组合，是否真的可以称为 Baga Ink Compatible？**

测试必须覆盖两类稳定边界：

```text
Baga Ink API / Capability
Baga Lua Profile / Standard Libraries
```

内部实现可以使用 KOReader、FBInk、SQLite、Automerge 或其他成熟组件；BICTS 测试的是标准可观察语义，不是要求内部代码长得一样。

---

# 1. 测试对象

每次认证对象：

```text
Device Model
+ Firmware / OS Version Range
+ Baga Ink Platform Version
+ Device Adapter Version
+ Baga Lua Profile Version
+ Compatibility Standard Version
+ BICTS Version
```

测试报告 SHOULD 同时记录关键 adopted dependency versions，例如：

```text
SQLite version
lsqlite3 version
Reader implementation/version
Automerge version（若使用）
```

---

# 2. 测试结果

单项状态：

```text
PASS
FAIL
SKIP_NOT_APPLICABLE
BLOCKED
WARNING
```

Base Mandatory Tests MUST 全部 PASS 才能获得 Compatible。

---

# 3. Base Mandatory 与 Feature Test

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

声明 Optional Capability 后自动启用对应 suite：

```text
input.touch             → TOUCH
display.partial_refresh → PARTIAL_REFRESH
input.pen               → PEN
network.https            → HTTPS
audio.output             → AUDIO
light.frontlight         → FRONTLIGHT
storage.user_library     → LIBRARY_BRIDGE
reader.anchor            → READER_ANCHOR
```

---

# 4. CORE 基础测试

至少验证：

```text
CORE-001 Platform boots
CORE-002 Adapter loads
CORE-003 API version readable
CORE-004 Standard Lua entry executes
CORE-005 Unsupported API rejected safely
CORE-006 Internal device/vendor objects do not leak
```

App 无需知道 KOReader / FBInk / Vendor SDK 等内部对象即可运行。

SQLite 与 `lsqlite3` 是正式 Standard Library，因此其公开名称本身不属于“泄漏内部实现”。

---

# 5. Baga Lua Profile 测试

验证基础 Lua Profile 与正式 Standard Libraries。

```text
LUA-001 required base libraries load
LUA-002 dangerous raw shell functions unavailable/restricted
LUA-003 arbitrary native module load blocked
LUA-004 lsqlite3 module loads
LUA-005 standard-library version metadata readable
```

Platform 不得要求 IKP 自己携带 `lsqlite3` native binary 才能通过。

---

# 6. SQLite / `lsqlite3` Profile 测试

`baga.data` 已撤销。结构化数据库测试直接针对 Baga Lua Profile 中的 `lsqlite3` / SQLite。

最低测试：

```text
SQLITE-001 require("lsqlite3") succeeds
SQLITE-002 open database in app sandbox
SQLITE-003 CREATE / INSERT / SELECT raw SQL works
SQLITE-004 prepared statement + bind works
SQLITE-005 explicit transaction commit is atomic
SQLITE-006 rollback leaves no partial writes
SQLITE-007 committed data survives app/process restart
SQLITE-008 database survives Platform update
SQLITE-009 foreign_keys can be enabled and enforced
SQLITE-010 BLOB round trip
SQLITE-011 JSON functions available
SQLITE-012 FTS5 available
SQLITE-013 WAL mode available when filesystem/platform supports required locking semantics
SQLITE-014 loadable native extension disabled for Universal App
SQLITE-015 app A cannot open app B private database
SQLITE-016 path traversal / absolute unauthorized path rejected
SQLITE-017 disk-full / IO errors fail safely
```

## 6.1 原子性测试

```text
初始 A=1, B=1
BEGIN
A=2
B=2
在 commit 前/中注入失败
重启
```

结果只能是：

```text
(A=1,B=1)
或
(A=2,B=2)
```

不得出现半事务。

## 6.2 不测试 Baga 私有数据库语义

BICTS MUST NOT 要求：

```text
store:get
store:put
collection
baga.data
```

这些不是 Baga 正式数据库标准。

BICTS MAY 查询 SQLite version / compile options，以确认 Platform 声明的 SQLite Profile 与实际 runtime 一致。

---

# 7. `baga.storage.resolve_path()` 与 Sandbox 测试

验证：

```text
STORAGE-001 appdata logical path resolves
STORAGE-002 resolved path belongs to current app sandbox
STORAGE-003 ../ cannot escape
STORAGE-004 absolute unauthorized path rejected
STORAGE-005 other-app private path cannot resolve/open
STORAGE-006 resolved path can be used by lsqlite3
STORAGE-007 returned path is runtime-local, not a stable cross-device identifier
```

在 Kindle 等缺乏 OS per-App sandbox 的系统，测试必须验证 Baga Platform 自己的约束真正阻止 SQLite 打开越界路径。

---

# 8. IKP 安装 / 更新 / 回滚

必须验证：

```text
合法 IKP 安装
非法 container/path 拒绝
错误 API/Profile range 拒绝
缺少 required capability 拒绝
签名损坏拒绝
升级成功
升级失败回滚
用户数据/SQLite DB 保留
```

关键回滚测试：

```text
安装 v1
创建 SQLite schema + 用户数据
尝试安装故意损坏的 v2
更新失败
v1 仍可启动
原数据库仍可读取
```

---

# 9. Lifecycle 测试

必须验证：

```text
start
resume
pause
sleep
wake
stop
```

重点：

- sleep/wake 不重复异常触发；
- SQLite 已提交事务不丢失；
- 网络状态 wake 后重新评估；
- App 不依赖进程永久存在。

---

# 10. Display 测试

Base：

- 页面可见；
- 屏幕尺寸/方向正确；
- `AUTO/TEXT/QUALITY` 可合理映射或降级；
- region 越界安全裁剪；
- 不发生无意义连续全刷。

声明 `display.partial_refresh` / `display.fast_refresh` 时执行对应增强 suite。

---

# 11. Input 测试

Base Compatible 必须能完成：

```text
focus_next
focus_previous
confirm
back
page_next
page_previous
```

Touch / Pen / Physical key 能力存在时分别运行对应测试。

---

# 12. Permission 测试

验证：

```text
Manifest 未声明 → request 被拒绝
已声明未授权 → not_granted
用户拒绝 → denied
授权 → granted
撤销后 → 立即不可访问
```

SQLite App-private database 不要求额外用户资料 Permission，但必须受 App Sandbox 约束。

---

# 13. Library Bridge / `baga.library`

声明 `storage.user_library` 时 MUST 验证：

```text
LIBRARY-001 list returns standard Library Item
LIBRARY-002 opaque id，不暴露 raw OS path
LIBRARY-003 read obeys library.read
LIBRARY-004 modification obeys library.write
LIBRARY-005 open handle can pass to baga.reader
LIBRARY-006 unsupported format fails cleanly
LIBRARY-007 rescan does not corrupt state
```

测试不得要求 EPUB-only，也不得依赖 Kindle `/documents` 或 Android vendor database schema。

---

# 14. Network / Power / Offline-first

Network suite：

- online/offline state；
- Wi-Fi disconnect/reconnect；
- HTTPS；
- DNS/timeout error；
- sleep 中断；
- wake 后重试。

Power suite：

- sleep/wake；
- charging/battery（若声明）；
- keep-awake 可拒绝；
- 测试不得长期阻止设备正常休眠。

---

# 15. Reader 与 Anchor

声明 `reader.open`：

```text
open
next/previous
position
close/reopen
restore
```

**不得把 EPUB 作为固定测试格式。** 应从当前 Reader implementation 声明支持的格式中选取。

声明 `reader.anchor`：

```text
create anchor
serialize
close/reopen
goto/resolve
invalid/stale anchor safe failure
accuracy/exact-vs-approximate explicit
```

若同时支持 rolling/reflowable 与 paging/fixed-page，SHOULD 各测一种真实格式。

测试不把 XPointer、pboxes、EPUB CFI、Readium Locator 当 Baga 公共输入。

---

# 16. Automerge Adopted Foundation 测试

Automerge **不是 Base Device Capability，也不是所有 IKP 的强制依赖**。

当某个 Reference App / Platform 功能明确采用 Automerge 时，相关测试 SHOULD 针对实际采用模块：

### 16.1 Document / Merge

```text
AM-001 two replicas make independent changes
AM-002 merge converges
AM-003 repeated merge is idempotent
AM-004 binary save/load preserves state
AM-005 change history survives restart
```

### 16.2 Sync Protocol（若采用）

```text
AM-SYNC-001 peers converge over supported transport
AM-SYNC-002 interrupted sync can resume safely
AM-SYNC-003 duplicate messages do not corrupt state
AM-SYNC-004 protocol/version mismatch fails explicitly
```

### 16.3 模块化采用

如果实现只采用 Automerge document/merge 而不用 sync protocol，则 `AM-SYNC-*` 可以 `SKIP_NOT_APPLICABLE`。

BICTS 不要求采用 `automerge-repo`，也不把其 Storage Adapter / Network Adapter 架构当作 Baga 标准。

---

# 17. Reference App Smoke Test

LifeBook Smoke Test MAY 包括：

```text
启动
打开书库
打开一个当前 Reader 支持的文档
翻页
保存阅读位置
创建笔记
写入/读取 SQLite 数据
sleep/wake
恢复状态
离线启动
```

如果 LifeBook 通过而基础 Probe 失败，设备仍不能认证 Compatible。

---

# 18. 数据安全

尤其针对 Client / Kindle 安装流程：

```text
不清用户书籍
不清用户笔记
不恢复出厂
失败后设备仍可启动
卸载 Platform 不误删用户资料
Platform/App 更新不误删 App SQLite DB
```

任何已知数据破坏风险都阻止正式 Compatible。

---

# 19. Firmware Regression

固件升级后最少运行：

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

如果 Reader/Library/网络受影响，还必须运行对应 suite。

---

# 20. 测试报告

报告 SHOULD 包含：

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
  "bicts_version": "0.3",
  "tests": {
    "passed": 0,
    "failed": 0,
    "warnings": 0
  }
}
```

Automerge 未使用时 `automerge_version` 可为空。

---

# 21. Certification Gate

正式 **Baga Ink Compatible**：

- Base Mandatory Tests MUST 100% PASS；
- Baga Lua Profile / SQLite Profile MUST PASS；
- 声明 Stable Capability 对应测试 MUST PASS；
- 不得存在 Critical data-loss issue；
- Experimental / provisional 功能不得冒充 stable。

---

# 22. 核心原则

> **Compatible 证明的是 Baga Ink API、Baga Lua Profile 和 Standard Libraries 的行为成立，不是证明底层采用了某个指定库。**

其中 SQLite 是 Baga 正式采用的 Standard Library 基础，所以测试直接验证 SQLite/`lsqlite3`；Automerge 是 Adopted Foundation，所以只在实际采用的功能范围内验证其对应模块。