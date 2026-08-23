# Baga Ink 兼容性标准 / Baga Ink Compatibility Standard

> **文档级别：一级平台规范**  
> **状态：Draft v0.4**  
> **日期：2026-08-23**  
> **上位文档：`01_顶层战略与架构_Baga-Ink-Platform-Strategy.md`**  
> **配套规范：`04_能力注册表_Baga-Ink-Capability-Registry.md`、`07_设备适配器规范_Baga-Ink-Device-Adapter-Specification.md`、`10_兼容性测试套件_Baga-Ink-Compatibility-Test-Suite.md`、`13_标准库与成熟组件采用规范_Baga-Ink-Standard-Libraries-and-Adopted-Components.md`**

---

## 0. 目的

本文档定义什么样的设备 / OS / Platform / Adapter 组合可以称为 **Baga Ink Compatible**。

兼容性不能只靠“LifeBook 能启动”，必须同时验证：

1. Platform Core；
2. Device Adapter；
3. Capability 真实性；
4. Baga Lua Profile；
5. 正式 Standard Libraries；
6. IKP 行为；
7. BICTS；
8. 数据安全与更新恢复。

核心原则：

> **硬件可以不同，内部库可以不同，但同一 Baga API / Lua Profile / Standard Library 契约必须成立。**

正式正文只描述当前有效兼容契约。

---

# 1. 适用对象

适用于 Kindle、Android E-Paper、第三方 Device Adapter、Baga Ink Client / Market 兼容展示，以及未来电子纸平台。

不要求所有设备具备 Touch / Pen / Color / Audio / Bluetooth；这些通过 Capability 表达。

---

# 2. 兼容等级

## 2.1 Baga Ink Compatible

要求：

- Base Mandatory Requirements 全部满足；
- Baga Lua Profile 通过对应 BICTS；
- Stable Standard Libraries 通过对应 BICTS；
- Adapter / Capability 通过验证；
- Universal Reference Apps 可运行；
- 安装/更新无已知高风险数据破坏；
- Recovery 满足最低要求。

## 2.2 Compatible + Profile

可附加 Touch、Pen、Fast Refresh、Color、Audio、Bluetooth 等 Profile；Profile 不形成平台分叉。

## 2.3 Experimental

Platform 可运行但尚未达到正式认证要求。

## 2.4 Unsupported

包括无法可靠安装/启动、核心 Display/Input/Storage 无法满足、存在高风险数据破坏、必须恢复出厂、最低 Platform/Lua Profile 基线无法实现等情况。

---

# 3. Base Compatibility Profile

设备必须满足：

```text
display.basic
input.navigation
storage.app_sandbox
power.sleep_wake
platform.lifecycle
```

并同时提供当前 Baga Lua Profile 的 Mandatory Standard Libraries。

当前 Reference Baseline 包括：

```text
require("lsqlite3")
+
符合 13 / BICTS 的 SQLite Profile
```

SQLite/lsqlite3 不是 Device Capability；它们属于 Lua Profile Standard Library。

Automerge 不属于 Base Mandatory Standard Library：它是 Adopted Foundation，只在实际采用相关功能时测试。

---

# 4. Platform 可安装与可启动

设备 MUST 可安装 Platform、有用户可理解启动入口、重启后保持状态、能加载标准 IKP，并在 App crash 后恢复可用。

安装路径可以不同，App contract 不能不同。

---

# 5. 用户数据安全

安装 / 更新 / 修复 MUST：

- 不删除用户书籍；
- 不删除用户笔记；
- 不默认删除用户文档；
- 不恢复出厂；
- 失败保留上一可工作状态；
- Platform/App 更新不无故删除 App-private SQLite databases；
- SQLite migration / rollback 失败不得留下半迁移数据。

任何已知 Critical data-loss 阻止 Compatible。

---

# 6. IKP 一致性

同一个 Universal IKP：

- 不因品牌改变包内容；
- Kindle / Android 不打不同业务包；
- 不携带设备私有执行桥；
- 在 Capability 相同时保持相同业务语义；
- 可以依赖 Platform 正式提供的 Baga Lua Profile Standard Libraries，不需要把它们打进 IKP。

---

# 7. API / Lua Profile / Standard Library 基线

设备 MUST 实现 Platform 版本声明的 Mandatory API Surface 与 Baga Lua Profile。

必须区分：

```text
设备/OS能力
→ baga.* / Capability

成熟通用库
→ Baga Lua Profile Standard Library
```

当前 SQLite 基线：

```text
lsqlite3 API-compatible module
Platform-managed SQLite runtime
Pinned version / compile options
Sandbox-safe file access
```

---

# 8. Capability Truthfulness

Capability 声明必须真实、稳定、可测。

禁止同系列推断、宣传页代替实测、固件不可用仍 true，以及把 SQLite/Automerge/KOReader 名称注册成 Capability。

---

# 9. Storage / SQLite Sandbox Compatibility

Platform MUST 提供 App sandbox：

```text
appdata/
cache/
documents/
downloads/
```

对于正式 SQLite Standard Library：

### Android / 强 OS sandbox

可主要依靠 OS app sandbox + Baga private path mapping。

### Kindle / 弱 OS sandbox

必须通过 sandbox-aware SQLite VFS 或等价 I/O confinement 证明 SQLite 无法逃逸当前 App 授权根。

至少覆盖：

```text
main DB
ATTACH DB
journal
WAL
SHM
temporary DB
URI vfs override
symlink / canonical path escape
loadable extension
```

仅 `resolve_path()` 返回合法路径不等于 SQLite Sandbox 兼容。

---

# 10. Display Compatibility

Adapter MUST 提供屏幕尺寸、方向、基本刷新与已声明增强能力。

App 只表达 `AUTO / TEXT / QUALITY / FAST / ANIMATION`，不暴露 waveform ID。

---

# 11. Input Compatibility

核心动作：

```text
confirm
back
menu
page_next
page_previous
```

设备 MAY 提供 touch / pen / keyboard / physical buttons；App 不依赖平台私有 keycode。

---

# 12. Lifecycle / Power

必须映射 `start / resume / pause / sleep / wake / stop`。

已提交 SQLite transaction 必须在正常持久化边界后经 sleep/restart 保持可靠。

Power 请求可以因平台策略被拒绝。

---

# 13. Network Compatibility

网络不是 Base 硬件要求。

声明网络能力时 MUST 正确 online/offline、使用 Baga Network API、处理 sleep/wake/reconnect，并映射 DNS/TLS/timeout。

Automerge sync protocol（若某功能采用）不是网络 Capability 本身。

---

# 14. Reader Compatibility

声明 `reader.open` / `reader.anchor` 时必须通过对应 BICTS。

Reader：

- 不以 EPUB 为固定格式；
- 可以内部复用 KOReader / MuPDF / CREngine；
- Anchor 可使用不同格式的成熟原生 locator；
- App 不解析 Reader private object。

---

# 15. Automerge Compatibility

Automerge core 是 Adopted Local-first Foundation，但不是 Base Compatible 强制组件。

只有实际采用 Automerge 的 Platform/App 功能才运行对应 BICTS：

```text
document / merge
binary persistence
history
sync protocol（若采用）
```

可以整用，也可以拆模块使用；不强制 automerge-repo。

---

# 16. Optional Capability Profiles

典型：Touch→`input.touch`、Pen→`input.pen`、FastRefresh→`display.fast_refresh`、Color→`display.color`、Audio→`audio.output`、Bluetooth→`bluetooth.available`。

声明即必须测试。

---

# 17. Performance / Resource Constraints

Compatible 不要求相同 CPU/RAM/Storage，但必须稳定运行标准 Reference Apps 与 Mandatory SQLite Profile。

Automerge 等非 Base 组件如果在低端设备资源过重，可以不启用对应增强功能，不能因此破坏 Base compatibility。

---

# 18. Upgrade / Recovery

正式兼容设备必须支持 staged update / verify / activation / rollback。

App package 与 App-private data/SQLite DB 分离。

---

# 19. Security Baseline

Compatible 设备必须：

- IKP 执行前验证；
- App sandbox；
- Permission 检查；
- 禁止 arbitrary shell；
- 禁止 Vendor API 直接穿透；
- 禁止 SQLite path/VFS/extension escape；
- 正确处理恶意/损坏 IKP；
- App crash 不破坏 Platform。

---

# 20. BICTS

正式认证必须基于对应版本 BICTS。

测试报告绑定：

```text
Device / Firmware
Platform
Adapter
Lua Profile
SQLite / lsqlite3 baseline
Compatibility Standard
BICTS
```

---

# 21. Reference Apps

Baga SHOULD 维护小型 Probe 与 LifeBook Reference。

LifeBook 不是唯一认证依据。

Reference Smoke Test 应包含 offline start、SQLite read/write/transaction、Reader（若声明）、sleep/wake、update/recovery。

---

# 22. Firmware / OS 维度

Compatibility 是：

```text
Device Model
+ OS/Firmware Range
+ Platform Version
+ Adapter Version
+ Lua Profile Version
+ BICTS Version
```

同一型号不同固件可以分别 Compatible / Experimental / Unsupported。

---

# 23. Client / Market 展示

Client 对普通用户展示 Compatible / Experimental / Unsupported。

Market 安装判断基于 Manifest + Capability + API/Profile compatibility + Compatibility Status，而不是普通型号白名单。

---

# 24. Certification Artifact

报告 SHOULD 包括：

```json
{
  "device_family": "kindle",
  "model": "example",
  "firmware_range": ">=x <y",
  "baga_platform": "0.x",
  "adapter_version": "0.x",
  "lua_profile": "0.x",
  "sqlite_version": "...",
  "lsqlite3_version": "...",
  "compatibility_standard": "0.4",
  "bicts": "0.x",
  "status": "compatible",
  "profiles": []
}
```

---

# 25. 核心原则

> **Baga Ink Compatible 意味着开发者可以相信稳定的 `baga.*`、Baga Lua Profile 与正式 Standard Libraries，而不用重新学习该设备的私有实现。**

内部使用 KOReader、SQLite、Automerge、FBInk、Vendor SDK 都不改变这个定义。
