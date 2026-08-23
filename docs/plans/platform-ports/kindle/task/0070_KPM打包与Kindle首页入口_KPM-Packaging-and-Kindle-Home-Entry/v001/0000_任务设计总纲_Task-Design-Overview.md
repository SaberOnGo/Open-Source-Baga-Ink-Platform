# TASK-0070 v001 任务设计总纲 / KPM Packaging and Kindle Home Entry Task Design

> **Task ID：`TASK-0070`**  
> **Version：`v001`**  
> **Milestone：K6 — KPM/native packaging + Kindle Home Entry**  
> **状态：Planned Baseline — dependency-gated**  
> **日期：2026-08-23**

---

## 0. Goal

将已验证的 Kindle Platform 组件从开发部署方式收敛为正常 Kindle native installation flow：

```text
baga-platform_<version>_kindlehf.kpkg
        ↓
install / health check
        ↓
Baga Ink Platform on Kindle
        ↓
sh_integration Home Entry
        ↓
Kindle Home → LifeBook / Probe
        ↓
baga-launch <app-id>
```

KPM 管理 Kindle native Baga Platform；IKP Package Manager 管理 `lifebook.ikp` 等 Baga Apps。两层包管理职责保持分离。

---

# 1. Dependencies and Authority

K1–K5 的设备侧基础链应已稳定，特别是 K3 Probe 与 K4 IKP installer/verifier。

权威输入：

```text
docs/zh-CN/reference-apps/03_Kindle具体实现架构冻结.md
docs/zh-CN/standards/11_Kindle适配规范.md
current Platform update/recovery standards
```

固定关系：

```text
KPM `.kpkg`
→ Baga Platform native package

IKP
→ Baga App package
```

不存在 `lifebook.ikp → lifebook.kpkg` 的转换链。

---

# 2. Scope

```text
build `baga-platform_<version>_kindlehf.kpkg`
package manifest/dependency metadata
pinned component manifest
install.sh / launch.sh / uninstall.sh
post-install Platform health check
safe update path
sh_integration Scriptlet Home Entry
Kindle Home → App entry → baga-launch <app-id>
update preserves user books/notes/App data
uninstall behavior follows explicit data policy
KPM unavailable/unvalidated fallback envelope research/validation
optional AppMgr Phase 2 research after baseline
```

---

# 3. Out of Scope

```text
automatic jailbreak route selection
Baga Ink Client implementation
new KPM fork/protocol
turning IKP into Kindle native package
making KUAL/MRPI normal user UI
full AppMgr integration as baseline blocker
support for every legacy ABI in v001
```

首个 package target 为 `kindlehf`。

---

# 4. Package Contents Boundary

`.kpkg` 可以包含目标 ABI 对应的：

```text
Baga Platform Core native parts
Kindle Adapter parts
baga-launch
pinned KOReader/koreader-base/FBInk-related components
Lua/LuaJIT and required native libraries
Platform install/update/uninstall hooks
Home Entry assets
component/version/license manifest
```

IKP App package与 mutable App data 不打包进 Platform release 作为不可分离状态。

---

# 5. Install / Update / Uninstall Design

## Install

```text
preflight
→ verify target/required Homebrew foundation
→ stage Platform package files
→ install/activate Platform
→ register Home Entry assets
→ health check
→ report result
```

## Update

```text
preserve user books/notes
preserve IKP App data
preserve compatible active App state
replace Platform release atomically/recoverably
run health check
rollback Platform release if required
```

Platform rollback 与 IKP App rollback 是两个不同事务。

## Uninstall

必须明确区分：

```text
remove Platform binaries/components
remove Home Entry
remove caches/logs according to policy
retain or remove Baga App data only according to explicit user/data policy
never remove Kindle books/notes
```

---

# 6. Home Entry

第一期按 Architecture Freeze 优先使用成熟 `sh_integration` Scriptlet。

用户产品路径：

```text
Kindle Home
   ↓
LifeBook
```

内部执行链：

```text
LifeBook Home Entry
→ baga-launch com.lifebook
→ Baga Platform Core
→ active lifebook.ikp
→ main.lua
```

Probe 调试环境可使用等价入口，但正常用户不需要进入 KOReader FileManager、KUAL、KPM CLI 或 MRPI UI。

---

# 7. KPM Compatibility and Fallback

状态必须区分：

```text
KPM compatible + installed
KPM compatible + not installed
KPM unavailable/unvalidated for this exact combination
```

对于 KPM-compatible 但未安装的设备，长期路线是先确保 KPM，再安装 `.kpkg`；只有在 KPM 对该组合确实不可用或未通过 Baga 验证时，才研究 MRPI/legacy/manual Platform installer envelope。

Fallback 不是 IKP 包格式，也不改变 Platform/App 边界。

---

# 8. Test Strategy

至少覆盖：

```text
fresh install
reinstall same version
upgrade version
failed health check
rollback Platform release
launch from Home Entry
exit/relaunch
sleep/wake after Home launch
uninstall
reinstall after uninstall
missing/corrupt package part
insufficient space handling
```

每个测试都应验证 Kindle 用户书籍/笔记与 Baga App data 的保留策略。

---

# 9. Real-device Validation

首个真机：已通过 K1–K5 的精确 `kindlehf` 组合。

证据：

```text
package filename/version/digest
device model/firmware/native target
pre-install state
install log
health-check result
Home Entry evidence
launch result
App data checksum/state before/after update
Kindle book/note preservation check
uninstall result
recovery result
```

---

# 10. Failure Recovery and Data Protection

K6 的恢复标准必须高于开发 bring-up：

- 安装失败不清除用户书籍、笔记或恢复出厂。
- update 失败应保留或恢复上一可用 Platform release。
- Home Entry 失败不得阻止 Kindle 正常 Home 的基本使用。
- uninstall 不应清除 Kindle 原生用户内容。
- App data 的删除必须来自明确的数据策略，而不是 package hook 的副作用。

---

# 11. Acceptance Gate

- [ ] `baga-platform_<version>_kindlehf.kpkg` 可重复构建并记录 components/digests/licenses。
- [ ] install/launch/uninstall hooks 行为可验证。
- [ ] fresh install 后 Platform health check 通过。
- [ ] Kindle Home 可一次进入 Probe/LifeBook 对应 Baga App。
- [ ] 普通用户路径不要求 KOReader FileManager、KUAL、KPM CLI、MRPI。
- [ ] update 后 Kindle 用户书籍/笔记保持。
- [ ] update/rollback 后 Baga App data 按策略保持。
- [ ] Platform update 与 IKP App update 仍是两个事务。
- [ ] failed install/update 有可执行恢复路径。
- [ ] KPM compatibility 状态没有把“未安装”误判成“不兼容”。

---

# 12. Known Risks

主要风险：KPM/firmware compatibility、Home Entry 在不同 Amazon UI/framework 代际变化、package hook 中断、空间不足、Platform rollback 与 App data policy 混淆、fallback 路线被错误升级为默认架构。

---

# 13. Expected Execution-Prompt Groups

```text
A. KPM compatibility/package-format audit
B. package manifest + component lock
C. install/launch/uninstall hooks
D. health check + Platform rollback
E. sh_integration Home Entry
F. update/data-preservation tests
G. uninstall/reinstall tests
H. fallback envelope evidence if required
I. real-device K6 Gate
```
