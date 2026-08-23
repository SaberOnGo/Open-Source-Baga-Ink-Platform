# TASK-0020 v001 任务设计总纲 / KOReader KindleHF Bring-up Task Design

> **Task ID：`TASK-0020`**  
> **Version：`v001`**  
> **Milestone：K1 — pinned KOReader / KindleHF Bring-up**  
> **状态：Selected Planning Baseline**  
> **日期：2026-08-23**

---

## 0. Goal

在真实 `kindlehf` 上建立可重复的 Baga-controlled development launch path：

```text
real Homebrew-ready Kindle
        ↓
baga-launch / development entry
        ↓
pinned KOReader/koreader-base Kindle substrate
        ↓
Baga-private bootstrap
        ↓
Baga-owned test surface
```

K1 只验证 substrate、private entry、基础输入/显示路径与进程生命周期，不要求完整 Device Adapter、IKP Package Manager 或 LifeBook。

---

# 1. Authority and Architecture Boundary

权威输入：

```text
docs/zh-CN/standards/11_Kindle适配规范.md
docs/zh-CN/reference-apps/03_Kindle具体实现架构冻结.md
docs/zh-CN/standards/13_标准库与成熟组件采用规范.md
```

固定边界：

```text
KOReader / koreader-base / FBInk
→ Kindle Platform internal Adopted Components

KOReader private entry technique
→ Kindle implementation detail

IKP App
→ 不直接调用 KOReader private API
```

K1 不新增 `KOReader Runtime Layer`、`Kindle Runtime` 等公共架构层。

---

# 2. Preconditions

首台开发设备：

```text
already Homebrew-ready
firmware >= 5.16.3
kindlehf
known recovery/reboot path
USB or other verified development transfer path
```

设备型号、固件、序列化日志所需信息、Homebrew foundation 状态必须在测试记录中明确保存。

K1 不负责把 stock Kindle 自动转换为 Homebrew-ready；该自动化属于 K7。

---

# 3. Scope

`v001` 覆盖：

```text
1. 选择并锁定 KOReader / koreader-base / FBInk reference commits
2. dependency / license / source digest manifest
3. 验证 kindlehf native build artifacts 与依赖
4. 建立最小 baga-launch development entry
5. 比较两类 Baga-private entry PoC
6. 建立 bootstrap diagnostics / crash log
7. 真机 cold start / exit / relaunch 验证
8. 建立最小 Baga-owned test surface
9. 验证至少一条受控输入路径
```

---

# 4. Out of Scope

```text
完整 Device Adapter Base Contract implementation
baga-probe.ikp
生产级 IKP signature/stage/activation
KPM `.kpkg` 产品化
Kindle Home 用户入口
自动 jailbreak / Client Route DB
ReaderUI product integration
完整 LifeBook
历史 ABI target 扩展
```

这些由后续 Task 处理。

---

# 5. Upstream Pin and Dependency Manifest

Baga 采用的 Kindle substrate 必须可重建、可审计、可升级比较。至少记录：

```text
project/repository
pinned commit/tag
source digest where applicable
license
local patch set
native target/toolchain assumption
build instructions
known Baga-specific deviation
```

第一版不依赖用户自行安装的 KOReader。Baga 使用自己锁定并验证的 private component set。

---

# 6. Private Entry PoC

K1 比较两个 implementation candidates；选择只基于真机证据，不写入公共 App Contract。

## Candidate A — direct Baga entry

概念形态：

```text
private KOReader bootstrap
→ setup environment/device/screen/input/UI foundation
→ detect Baga-private launch argument
→ baga/bootstrap.lua
→ Baga-owned surface
```

可采用类似：

```text
--baga-app <app-id>
```

的私有启动参数，但名称与实现细节在 PoC 后再固定。

## Candidate B — Platform-private plugin entry

概念形态：

```text
baga-launch
→ private KOReader substrate
→ Baga-private plugin/bootstrap
→ Baga-owned surface
```

该方案只作为 Platform implementation candidate，不把 LifeBook 建模为 KOReader plugin。

## Selection Criteria

```text
startup determinism
是否出现 FileManager/Plugin UI 闪现
lifecycle correctness
clean exit / relaunch
crash recovery
patch maintenance cost
upstream upgrade cost
ability to keep KOReader private from IKP
```

满足条件时优先选择更直接、用户不可见底层 KOReader UI、维护面更小的方案。

---

# 7. Proposed Repository Write Scope

K1 预计涉及：

```text
platform/vendor/ or platform/components/
platform/kindle bootstrap assets
platform/lua or Baga bootstrap code
platform/adapters/kindle/ only for minimal bring-up glue when contract permits
tools/build/package scripts for kindlehf
tests/bringup or equivalent diagnostics area
```

具体目录以当前仓库实际结构和 Architecture Freeze 为准。Reader、Adapter、package-manager 职责不得因 bring-up 方便而混入同一模块。

---

# 8. Diagnostics and Evidence

最小诊断信息：

```text
Baga build/version
pinned component versions
model / firmware / native target
launch timestamp
bootstrap stage markers
screen initialization result
input initialization result
exit reason
last error
```

真机证据至少保留：

```text
build command/result
artifact digest
设备信息
launch log
Baga-owned surface photo/screenshot if available
input result
exit/relaunch result
known warnings
```

---

# 9. Real-device Test Procedure

顺序保持可恢复：

```text
1. 记录 model / firmware / Homebrew state
2. 备份本 Task 会修改的开发文件
3. 部署 pinned development build
4. 从受控 development entry 启动
5. 确认无 KOReader FileManager 产品路径暴露
6. 显示 Baga-owned test surface
7. 验证至少一条输入路径
8. clean exit
9. relaunch
10. 收集日志与设备状态
11. 移除/恢复开发资产并确认 Kindle 正常使用
```

K1 不要求触碰用户书库、笔记或恢复出厂设置。

---

# 10. Debug Strategy

故障按以下层级拆分：

```text
artifact/toolchain mismatch
        ↓
missing native dependency
        ↓
KOReader bootstrap baseline
        ↓
Baga private entry patch/plugin
        ↓
Baga bootstrap
        ↓
screen/input surface
        ↓
exit/relaunch
```

若 stock KOReader baseline 本身无法在目标设备启动，应先解决/记录 substrate baseline，不把问题归因于 Baga Adapter。

---

# 11. Failure Recovery and Data Protection

K1 必须满足：

```text
不清除 Kindle 用户书籍
不清除用户笔记
不恢复出厂设置作为普通恢复步骤
开发资产位于可识别、可移除位置
失败后可停止 Baga/KOReader private process
可恢复到 Task 开始前的开发文件状态
```

任何可能影响 Home/系统服务的实验应先有独立备份与恢复步骤，再进入真机执行。

---

# 12. Acceptance Gate

`TASK-0020/v001` 通过需满足：

- [ ] KOReader/koreader-base/FBInk reference revisions 已锁定并记录许可证/来源。
- [ ] `kindlehf` build/launch baseline 可重复。
- [ ] 真实 Homebrew-ready Kindle 可从 `baga-launch` 或等价受控入口启动。
- [ ] 启动后进入 Baga-owned test surface，而不是 KOReader FileManager 产品 UI。
- [ ] 至少一条输入路径可被 Baga bootstrap 观察并处理。
- [ ] clean exit 与 relaunch 可重复完成。
- [ ] crash/launch logs 足以定位 bootstrap 阶段。
- [ ] private entry 方案选择有真机证据与维护成本比较。
- [ ] IKP App 未直接依赖 KOReader private API。
- [ ] 测试未损坏 Kindle 用户书籍、笔记或正常 Home 使用。

---

# 13. Known Risks and Open Questions

主要风险：

```text
upstream revision 漂移
Baga patch 随 KOReader 更新产生维护成本
Amazon framework/firmware 影响启动或退出
不同 kindlehf 设备仍存在 profile/quirk 差异
开发入口与最终 Home Entry 行为不同
```

K1 需要通过证据回答的核心问题只有一个：哪种 private entry technique 在真实 Kindle 上最确定、最少暴露 KOReader UI、最易维护。

---

# 14. Expected Execution-Prompt Groups

```text
A. Device/precondition evidence capture
B. Upstream pin + license manifest
C. kindlehf build baseline
D. development baga-launch
E. direct-entry PoC
F. private-plugin PoC
G. diagnostics/crash recovery
H. real-device comparison
I. selected entry implementation + K1 Gate
```
