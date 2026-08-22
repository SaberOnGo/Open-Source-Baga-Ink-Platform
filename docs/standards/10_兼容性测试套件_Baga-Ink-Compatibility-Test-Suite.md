# Baga Ink 兼容性测试套件 / Baga Ink Compatibility Test Suite

> **文档级别：一级平台规范**  
> **简称：BICTS**  
> **状态：Draft v0.2**  
> **日期：2026-08-23**  
> **上位文档：`08_兼容性标准_Baga-Ink-Compatibility-Standard.md`**  
> **配套规范：`03_API规范_Baga-Ink-API-Specification.md`、`04_能力注册表_Baga-Ink-Capability-Registry.md`、`07_设备适配器规范_Baga-Ink-Device-Adapter-Specification.md`、`09_UI规范_Baga-Ink-UI-Specification.md`**

---

## 0. 目的 / Purpose

BICTS 用来回答一个非常具体的问题：

> **某个“设备 + 固件 + Baga Ink Platform + Device Adapter”组合，是否真的可以称为 Baga Ink Compatible？**

兼容不能靠人工感觉，也不能因为“能启动 LifeBook”就算通过。

BICTS 的目标是把兼容性变成：

```text
可自动执行
可重复
可记录
可比较
可回归
可由 OEM 自测
```

BICTS 测试的是 **Baga Ink API / Capability 的公开行为**，不是底层是否使用某个指定开源库。KOReader、SQLite、Automerge、FBInk 等内部实现可以变化，只要相同标准版本的可观察语义保持一致。

---

# 1. 测试对象

每次认证对象是一个确定组合：

```text
Device Model
+ Firmware / OS Version Range
+ Baga Ink Platform Version
+ Device Adapter Version
+ Compatibility Standard Version
+ BICTS Version
```

示例：

```json
{
  "device": "Kindle Paperwhite 5",
  "firmware": "x.y.z",
  "platform": "0.3.0",
  "adapter": "kindle 0.2.0",
  "standard": "0.2",
  "bicts": "0.2"
}
```

设备换固件后 SHOULD 重新执行至少回归子集。

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

认证级别只由强制测试决定。

`WARNING` 不等于 PASS，但 MAY 不阻塞认证。

---

# 3. Mandatory 与 Profile Test

## 3.1 Base Mandatory

所有 Compatible 设备 MUST 通过：

```text
CORE
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

当 Platform 声明支持 Baga API v0.3 中的 `baga.data` 时，还必须通过对应 DATA suite。

## 3.2 Capability / API Feature Test

声明某 Capability 或 API Feature 后，自动启用对应测试。

例如：

```text
input.touch             → TOUCH suite
display.partial_refresh → PARTIAL_REFRESH suite
input.pen               → PEN suite
network.https            → HTTPS suite
audio.output             → AUDIO suite
light.frontlight         → FRONTLIGHT suite
storage.user_library     → LIBRARY_BRIDGE suite
reader.anchor            → READER_ANCHOR suite
```

原则：

> **不声明可以不测；一旦声明，就必须测真。**

---

# 4. CORE 基础测试

验证 Platform Core 能：

- 启动；
- 读取 Adapter descriptor；
- 获取 API version；
- 加载标准 IKP；
- 正确返回统一错误对象；
- 不向 App 泄漏设备私有接口或内部 Library 对象；
- 在冷启动后稳定工作。

示例测试 ID：

```text
CORE-001 Platform boots
CORE-002 Adapter loads
CORE-003 API version readable
CORE-004 Standard Lua entry executes
CORE-005 Unsupported API rejected safely
CORE-006 Internal implementation details do not leak
```

`CORE-006` SHOULD 验证 App 无需知道：

```text
KOReader
SQLite
Automerge
Vendor SDK
raw system path
```

等内部实现名称或对象即可使用标准 API。

---

# 5. IKP 测试

必须验证：

```text
合法 IKP 安装
非法 ZIP 拒绝
path traversal 拒绝
重复 entry 拒绝
错误 format version 拒绝
错误 API range 拒绝
缺少 required capability 拒绝
签名损坏拒绝
升级成功
升级失败回滚
用户数据保留
```

关键测试：

### IKP-UPDATE-ROLLBACK

```text
安装 App v1
写入用户数据
尝试安装故意损坏的 v2
  ↓
更新必须失败
  ↓
v1 仍可启动
  ↓
用户数据仍存在
```

---

# 6. Lifecycle 测试

必须验证事件语义：

```text
start
resume
pause
sleep
wake
stop
```

重点：

- sleep 只触发合理次数；
- wake 后 App 状态恢复；
- 网络状态重新评估；
- App 不因系统短暂后台切换丢数据；
- 重启后可恢复持久状态。

---

# 7. Display Base 测试

必须验证：

- 基础页面可见；
- 坐标正确；
- 屏幕尺寸正确；
- orientation descriptor 正确；
- Text UI 不出现严重裁切；
- Display API 不崩溃；
- `AUTO/TEXT/QUALITY` 至少能合理映射或降级。

墨水屏特有测试 SHOULD 观察：

- 不发生无意义连续全刷；
- 页面切换后内容完整；
- refresh region 越界时安全裁剪。

---

# 8. Partial Refresh 测试

设备声明 `display.partial_refresh` 时 MUST：

1. 渲染固定页面；
2. 修改小区域；
3. 请求局部刷新；
4. 验证未修改主体区域不需要完整重绘；
5. 连续执行多次；
6. 验证 Adapter 不崩溃、不出现永久损坏状态。

自动化无法完全判断残影质量时，可加入视觉人工检查项，但功能语义仍必须自动验证。

---

# 9. Fast Refresh 测试

声明 `display.fast_refresh` 时：

- FAST 请求必须比完全不支持时具有实际实现；
- 不得只是 capability=true 但永远走同一 unsupported path；
- 连续列表导航稳定；
- 最终 QUALITY refresh 后内容应恢复可读质量。

不冻结具体毫秒指标，设备 Profile MAY 后续定义性能阈值。

---

# 10. Input Navigation 测试

Base Compatible MUST 能完成：

```text
focus_next
focus_previous
confirm
back
page_next
page_previous
```

实现方式可以不同。

测试 Reference UI：

```text
进入列表
选择第二项
打开页面
翻下一页
返回
```

至少存在一条当前硬件可用输入路径完成整个流程。

---

# 11. Touch 测试

声明 `input.touch` 时：

- down/move/up 顺序正确；
- 坐标与 UI 一致；
- 屏幕旋转后坐标正确；
- 点击 Button 可触发一次且仅一次；
- cancel 可终止手势；
- 不产生明显 ghost duplicate event。

---

# 12. Pen 测试

声明 `input.pen` 时：

- Pen 与 Touch 可区分；
- 坐标正确；
- 笔画连续；
- sleep/wake 后可重新使用。

子能力：

```text
pressure → 压力值变化验证
eraser → eraser state 验证
hover → hover event 验证
low_latency → 专门性能与绘制路径验证
```

---

# 13. Storage Sandbox 测试

必须验证 App A：

- 可以读写自己的 `appdata/`；
- 不可以读取 App B private data；
- `../` 不可逃逸；
- 删除 cache 不删除 documents；
- Platform 更新不清空数据；
- 磁盘满时返回标准错误。

---

# 14. Structured Data / `baga.data` 测试

当 Platform 提供 `baga.data` 时 MUST 验证：

```text
DATA-001 open isolated store
DATA-002 put/get round trip
DATA-003 delete semantics
DATA-004 transaction commit is atomic
DATA-005 transaction abort leaves no partial writes
DATA-006 process crash/restart preserves committed transaction
DATA-007 platform restart preserves committed data
DATA-008 app A cannot read app B data
DATA-009 quota/disk-full returns standard error
DATA-010 platform update preserves app data
```

关键原子性测试：

```text
初始 A=1, B=1
  ↓
transaction:
  A=2
  B=2
  ↓
在提交中间注入失败/中断
  ↓
重启后必须是：
(A=1,B=1) 或 (A=2,B=2)

不得出现：
(A=2,B=1)
```

BICTS MUST NOT 通过查询 SQLite 文件、SQL schema 或 WAL 来判断成功；只验证 `baga.data` 的公开语义。

---

# 15. Permission 测试

必须验证：

```text
Manifest 未声明 → request 被拒绝
已声明未授权 → not_granted
用户拒绝 → denied
授权 → granted
撤销后 → 立即不可访问
```

同时测试绕过路径：

```text
raw io
os.execute
package native load
```

在 Universal Profile 中必须不可形成权限逃逸。

---

# 16. Library Bridge / `baga.library` 测试

声明 `storage.user_library` 时 MUST 运行 Library Bridge suite。

至少验证：

```text
LIBRARY-001 list returns standard Library Item
LIBRARY-002 item id is usable without exposing raw OS path
LIBRARY-003 get/open obey library.read permission
LIBRARY-004 import/remove obey library.write permission
LIBRARY-005 open handle can be passed to baga.reader when supported
LIBRARY-006 unsupported document is reported cleanly
LIBRARY-007 device library rescan does not corrupt app state
```

测试 MUST 不要求：

```text
EPUB-only
Kindle /documents path
Android vendor bookshelf path
某一种厂商数据库 schema
```

测试出版物/文档格式应从当前 Reader implementation 声明支持的格式集合中选择。

---

# 17. Network 测试

声明网络能力时：

- online state 正确；
- offline state 正确；
- Wi-Fi 断开事件正确；
- HTTPS 请求可成功；
- DNS failure 映射为统一错误；
- timeout 正确；
- sleep 中断请求后不损坏 App；
- wake 后可重新请求。

---

# 18. Reader 基础与 Anchor 测试

## 18.1 Reader Base

声明 `reader.open` 时，至少使用一个当前实现声明支持的测试文档验证：

```text
open
next_page / previous_page
position
close
reopen
restore position
```

**测试不得把 EPUB 作为 Baga Ink Reader 的固定或默认格式要求。**

## 18.2 `reader.anchor`

声明 `reader.anchor` 时 MUST 验证：

```text
READER-ANCHOR-001 create anchor from current position/selection
READER-ANCHOR-002 anchor is Baga-serializable
READER-ANCHOR-003 close/reopen then goto_anchor
READER-ANCHOR-004 resolve_anchor returns explicit accuracy/result state
READER-ANCHOR-005 invalid/stale anchor fails safely
READER-ANCHOR-006 app need not inspect reader-private fields
```

如果当前 Reader 实现同时声明支持：

```text
reflowable/rolling 类文档
+
fixed-page/paging 类文档
```

BICTS SHOULD 至少各选一种真实支持格式执行 Anchor round-trip，以验证公开 Anchor 语义没有被错误绑定到某一格式。

例如 Kindle/KOReader 实现可以内部使用：

```text
rolling → XPointer-like native position
paging  → page + local position / boxes
```

但测试只观察：

```text
create → serialize → reopen → resolve/goto
```

不把 XPointer、pboxes、EPUB CFI 或 Readium Locator 本身作为 Baga 公共测试输入。

---

# 19. Power 测试

必须验证：

- sleep/wake；
- App 状态保存；
- battery capability 如声明则数值有效；
- charging capability 如声明则状态有效；
- keep-awake 请求可拒绝且 App 正确处理。

测试不得长期阻止设备正常休眠。

---

# 20. Frontlight 测试

声明 `light.frontlight`：

- get value；
- set value（若 policy 允许）；
- 超界值正确裁剪 / 拒绝；
- 不因调用造成系统服务异常；
- App 无权限时拒绝。

测试结束 MUST 恢复用户原前光设置。

---

# 21. Audio / Bluetooth 测试

能力存在才运行。

Audio：

```text
open
play
stop
error recovery
sleep behavior
```

Bluetooth：

```text
availability
permission
connection state
input mapping（如声明）
```

测试必须避免修改用户长期配对状态，除非用户明确允许。

---

# 22. Sync / Offline-first 行为测试

`baga.sync` 测试的是调度和设备策略语义，不强制某一种 CRDT。

SHOULD 验证：

```text
offline state does not block local app startup
when_online trigger resumes after reconnect
sleep does not corrupt queued work
wake can resume/retry safely
wifi_only respects network policy
cancel/retry returns standard state
```

如果某 Reference App 声称支持并发离线编辑，应另行测试其业务合并结果；底层可以使用 Automerge 或其他成熟实现，但 BICTS 不因库名决定 PASS/FAIL。

---

# 23. UI Reference Test

官方维护一组小型 IKP Reference Apps：

```text
HelloInk
ListNavigation
ReaderMini
StorageProbe
DataProbe
LibraryProbe
PermissionProbe
DisplayProbe
LifecycleProbe
```

它们只使用公开 Baga Ink API。

任何 Base Compatible 设备 MUST 能运行规定的 Base Reference Apps；API/Capability 相关 Probe 按对应版本和声明运行。

---

# 24. LifeBook Reference Smoke Test

LifeBook 是旗舰 Reference App，但不能成为认证的唯一依据。

Smoke Test MAY 包括：

```text
启动
打开书库
打开一个当前 Reader implementation 声明支持的测试文档/出版物
翻页
保存阅读位置
创建笔记
创建并恢复 Reader Anchor（若声明 reader.anchor）
sleep/wake
恢复阅读位置
离线启动
```

测试文档不得固定为 EPUB；应根据被测 Reader 的真实支持能力选择，并在支持多类文档时覆盖代表性类别。

如果 LifeBook 通过而基础 Probe 失败，设备仍不能认证 Compatible。

---

# 25. 数据安全测试

尤其针对 Baga Ink Client / Kindle 安装流程，必须验证：

```text
安装 Platform 不清用户书籍
不清用户笔记
不恢复出厂
失败后设备仍可正常启动
失败可重新执行或恢复
卸载 Platform 不误删用户资料
```

任何已知数据破坏风险都阻止正式 Compatible 标签。

---

# 26. Firmware Regression

固件升级后最少运行：

```text
CORE
LIFECYCLE
DISPLAY
INPUT
STORAGE
DATA（如果 API 版本包含 baga.data）
IKP
RECOVERY
```

如果厂商固件改动 Reader、书库、显示或系统服务，还必须执行相关 Capability / API suite。

认证对象 SHOULD 记录经过验证的固件范围。

---

# 27. 自动化与人工测试边界

尽量自动化：

```text
API semantics
file integrity
data transaction atomicity
permission
lifecycle
input events
reader anchor round-trip
network errors
update rollback
capability truth
```

可能需要人工 / 视觉辅助：

```text
ghosting severity
visual clipping
pen perceived latency
frontlight physical response
```

人工项必须有结构化结果，不能只写“感觉正常”。

---

# 28. 测试报告

标准报告 SHOULD 包含：

```json
{
  "device": {},
  "firmware": "...",
  "platform_version": "...",
  "adapter_version": "...",
  "standard_version": "...",
  "bicts_version": "0.2",
  "capabilities": [],
  "tests": {
    "passed": 120,
    "failed": 0,
    "warnings": 3
  }
}
```

每个 FAIL 必须记录：

```text
test_id
expected
actual
logs
device state
repro steps
```

---

# 29. Certification Gate

正式 **Baga Ink Compatible**：

- Base Mandatory Tests MUST 100% PASS；
- 所声明 Stable Capability 对应 Mandatory Test MUST PASS；
- Platform 所声明 API 版本的 mandatory service tests MUST PASS；
- 不得存在 Critical data-loss issue；
- 不得通过伪造 capability 跳过测试；
- WARNING 必须记录；
- Experimental / Provisional Capability 不得伪装为 Stable Profile。

---

# 30. BICTS 版本

BICTS 自己必须版本化：

```text
BICTS 0.1
BICTS 0.2
...
```

认证结果必须同时记录：

```text
Compatibility Standard version
BICTS version
```

防止“通过旧测试”被误认为永远兼容。

---

# 31. OEM Self-Test

未来厂商 SHOULD 可以：

```text
实现 Adapter / Platform integration
  ↓
复用适合的成熟组件
  ↓
本地运行 BICTS
  ↓
生成 signed report
  ↓
提交 Baga Ink certification
```

BICTS 不要求 OEM 使用某个指定内部 Library，只要求公开行为满足标准。

---

# 32. 核心原则 / Core Rule

> **Compatible 不是营销词，而是可重复执行的公开语义测试结果。**

只要 BICTS 足够严格，Baga Ink 就可以允许大量设备、不同内部实现和成熟开源组件进入生态，而不重新碎片化。