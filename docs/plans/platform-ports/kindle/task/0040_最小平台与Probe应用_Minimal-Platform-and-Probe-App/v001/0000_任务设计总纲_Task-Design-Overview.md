# TASK-0040 v001 任务设计总纲 / Minimal Platform and Probe App Task Design

> **Task ID：`TASK-0040`**  
> **Version：`v001`**  
> **Milestone：K3 — Minimal Platform Core + `baga-probe.ikp`**  
> **状态：Planned Baseline — dependency-gated**  
> **日期：2026-08-23**

---

## 0. Goal

第一次在真实 Kindle 上运行一个真正的 Baga `.ikp`：

```text
real Kindle
   ↓
baga-launch
   ↓
Baga Ink Platform Core
   ↓
Kindle Device Adapter
   ↓
baga-probe.ikp
   ↓
visible UI + input
   ↓
persist local state
   ↓
sleep / wake
   ↓
state remains valid
```

这是 Kindle Port 从 substrate/adapter 验证进入真正 App Platform 的第一条重大验收链。

---

# 1. Dependencies and Authority

前置：`TASK-0010`、`TASK-0020`、`TASK-0030` Gate 通过。

权威输入：

```text
docs/zh-CN/standards/02_应用标准.md
docs/zh-CN/standards/03_API规范.md
docs/zh-CN/standards/05_权限模型.md
docs/zh-CN/standards/06_IKP应用包规范.md
docs/zh-CN/standards/07_设备适配器规范.md
docs/zh-CN/standards/10_兼容性测试套件.md
docs/zh-CN/reference-apps/03_Kindle具体实现架构冻结.md
```

---

# 2. Scope

Platform Core v0.0.1 只实现 Probe 所需最小职责：

```text
App Registry
App Context
Embedded Lua Host
Lifecycle dispatch
Adapter dispatch
Permission/Sandbox skeleton

baga.app
baga.device
baga.storage
baga.log
minimal baga.ui
```

同时实现：

```text
developer-mode local IKP loading path
manifest + entry parsing needed for local Probe
baga-probe.ikp build
persistent counter
Base capability display
sleep/wake state recovery
Base BICTS subset
```

---

# 3. Probe Definition

第一份真实 IKP 是：

```text
baga-probe.ikp
```

最小可见信息：

```text
Baga Ink Probe
Platform: <version>
Adapter: kindle <version>
Model: <model>
Firmware: <firmware>
Native target: kindlehf

Capabilities:
✓ display.basic
✓ input.navigation
✓ storage.app_sandbox
✓ power.sleep_wake
✓ platform.lifecycle

Counter: 1
[ +1 ]
```

核心行为：点击 `+1` 后持久化为 `2`；设备 sleep/wake 后仍显示 `2`。

Probe 是基础兼容性测试 App，不由 LifeBook 替代。

---

# 4. Out of Scope

```text
生产级 signature verification
完整 IKP staging/activation/rollback
Market/repository client
Sync / Automerge
AI
Audio / Bluetooth / Pen
full baga.reader
完整 LifeBook
KPM packaging
Kindle Home product entry
Client jailbreak/bootstrap automation
```

K3 只提供 developer-mode local IKP 链；生产级安装/验证在 K4。

---

# 5. Implementation Design

## 5.1 Platform Bootstrap

启动职责保持：

```text
baga-launch
→ pinned Kindle substrate
→ Platform Core bootstrap
→ Adapter factory/init
→ App registry/context
→ Lua host
→ selected local IKP entry
```

Platform Core 负责 App/Adapter 分发，不允许 Probe 直接 import KOReader/Kindle private APIs。

## 5.2 Lua Host

Lua Host 只暴露当前 Standard 已定义且 Probe 需要的 Baga API surface。KOReader Lua module path、Device object、UIManager 等均属于 Platform implementation detail。

## 5.3 Minimal `baga.ui`

Kindle backend 可以复用 KOReader UIManager/widgets，但 App 只看到 `baga.ui` 语义。首版只实现 Probe 需要的静态文本、简单布局、按钮/导航和必要刷新。

## 5.4 Storage

Counter 写入 App sandbox。App package 与 App data 分离，为 K4 的 immutable release/staging 设计保留边界。

## 5.5 Lifecycle

Platform 将 Kindle Adapter lifecycle 事件传递给 App context，并保证 sleep/wake 不丢失已确认写入的本地状态。

---

# 6. Proposed Repository Write Scope

预计涉及：

```text
platform/core/
platform/lua/
platform/ui/ or equivalent Kindle UI implementation
apps/probe/
IKP build/package tooling already approved by repo layout
tests/platform_core/
tests/probe/
tests/bicts/ relevant Base subset
```

不在 `apps/probe/` 中放置 Kindle-specific code。

---

# 7. Test Strategy

## Headless / Host

```text
App Registry tests
App Context lifecycle tests
Lua host API exposure tests
Adapter dispatch tests
storage sandbox tests
Probe package structure tests
minimal UI state tests where mockable
```

## Real Kindle

```text
launch
render
input
persist
exit/relaunch
sleep/wake
capability display
error/log visibility
```

至少执行一次冷启动和多次 sleep/wake 循环，避免只验证单次演示。

---

# 8. Debug Strategy

端到端失败按边界定位：

```text
K1 substrate/entry
→ Platform bootstrap
→ Adapter init
→ App registry/context
→ Lua host
→ IKP manifest/entry
→ baga.ui
→ input dispatch
→ storage
→ lifecycle/power
```

任何问题均应在对应层修复；Probe 不通过私有 Kindle 调用绕过 Platform。

---

# 9. Real-device Operations and Evidence

保留：

```text
model/firmware/native target
Platform build id
Adapter build id
Probe package digest
launch log
capability snapshot
counter before/after
sleep/wake timestamps
relaunch result
error log
```

验证过程中只操作专用 App sandbox 与 Baga development assets。

---

# 10. Data Protection and Recovery

- 不清除 Kindle 用户书籍或笔记。
- 不使用恢复出厂作为普通失败恢复方式。
- Probe data 位于独立 sandbox，可单独删除。
- Platform 开发文件可回退到 K2/K1 已验证 baseline。
- sleep/wake 或启动失败时应能通过停止进程/重启设备恢复 Kindle 正常 Home 使用。

---

# 11. Acceptance Gate

- [ ] `baga-probe.ikp` 是符合当前 IKP 开发模式要求的真实 App 包。
- [ ] `baga-launch` 能进入 Platform Core 并启动 Probe。
- [ ] Probe 不直接 import KOReader/Kindle private API。
- [ ] 页面显示 Platform/Adapter/model/firmware/native-target/capability 信息。
- [ ] 输入可触发 `+1` 行为。
- [ ] Counter 从 `1` 持久化为 `2`。
- [ ] exit/relaunch 后 Counter 保持。
- [ ] sleep/wake 后 Counter 保持。
- [ ] Base lifecycle/power 事件可在日志/测试中观察。
- [ ] Base BICTS subset 在真实设备通过。
- [ ] 普通测试路径不出现 KOReader FileManager/Plugin Menu。

---

# 12. Known Risks

主要风险包括 Lua host/API boundary 漂移、最小 UI 过早耦合 KOReader widget、storage package/data 混淆、sleep/wake 时序问题，以及 developer-mode loader 被误当成生产安装链。

K3 的实现应刻意保持最小，以便 K4 在不重写 App Runtime 的前提下增加 verifier/staging/activation。

---

# 13. Expected Execution-Prompt Groups

```text
A. Minimal Platform bootstrap
B. App Registry + App Context
C. Embedded Lua Host
D. minimal baga.* APIs
E. Kindle minimal baga.ui
F. developer-mode IKP loader
G. baga-probe.ikp
H. storage persistence
I. sleep/wake + Base BICTS real-device Gate
```
