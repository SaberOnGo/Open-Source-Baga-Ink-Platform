# TASK-0020 v002 任务设计总纲 / KOReader KindleHF Bring-up Task Design

> **Task ID：`TASK-0020`**  
> **Version：`v002`**  
> **Milestone：K1 — pinned KOReader / KindleHF Bring-up**  
> **状态：Selected Planning Baseline**  
> **日期：2026-08-23**

---

## 0. Goal

在真实 `kindlehf` 上建立可重复的 Baga-controlled development launch path，并把 K1 的语言与启动方案从“开放候选”收敛为默认实现基线：

```text
real Homebrew-ready Kindle
        ↓
baga-launch / development entry
        ↓
pinned KOReader/koreader-base substrate
        ↓
direct Baga private entry
        ↓
baga/bootstrap.lua
        ↓
Baga-owned test surface
```

K1 只验证 substrate、private entry、基础输入/显示路径和进程生命周期，不要求完整 Device Adapter、IKP Package Manager 或 LifeBook。

---

# 1. Authority and Fixed Implementation Inputs

```text
docs/zh-CN/standards/11_Kindle适配规范.md
docs/zh-CN/reference-apps/03_Kindle具体实现架构冻结.md
docs/zh-CN/standards/13_标准库与成熟组件采用规范.md
docs/plans/platform-ports/kindle/0020_Kindle实现语言与绑定裁决_Kindle-Implementation-Language-and-Binding-Decision.md
```

固定解释：

- KOReader / koreader-base / FBInk 是 Kindle Platform internal Adopted Components；
- Kindle Bring-up 不为了语言统一重写这些组件；
- KOReader 已有 Lua/LuaJIT 初始化环境时，Baga bootstrap 优先使用 Lua；
- shell 仅用于必要的启动/环境准备；
- native C/Rust 只在已有 native component 或真实阻塞需要时使用窄 binding；
- IKP App 不直接调用 KOReader private API。

---

# 2. Preconditions

首台开发设备：

```text
already Homebrew-ready
firmware >= 5.16.3
native target: kindlehf
known recovery/reboot path
verified development transfer path
```

K1 不负责把 stock Kindle 自动转换为 Homebrew-ready；该自动化属于 K7。

---

# 3. Scope

`v002` 覆盖：

```text
1. 锁定 KOReader / koreader-base / FBInk reference commits
2. dependency / license / source digest manifest
3. 验证 kindlehf native build artifacts
4. 建立最小 baga-launch development entry
5. 实现 direct Baga private entry baseline
6. 实现 Lua/LuaJIT Baga bootstrap
7. bootstrap diagnostics / crash log
8. 真机 cold start / exit / relaunch
9. 最小 Baga-owned test surface
10. 至少一条受控输入路径
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
为了 K1 新建通用 Lua SDK codegen
```

---

# 5. Language / Binding Baseline

K1 默认选择：

| Area | Baseline |
|---|---|
| KOReader environment/bootstrap integration | **Lua/LuaJIT** |
| Baga bootstrap | **Lua** |
| launch wrapper | minimal shell / existing native launcher mechanism |
| display/input smoke path | reuse KOReader existing Lua-facing device knowledge |
| FBInk | keep existing native C implementation; use only where needed through existing/narrow binding |

执行者不得先进行一次新的“Rust vs Lua vs C”选型研究。

只有真实 build/ABI/crash/performance evidence 证明默认路径不可行时，才允许提出偏离，并回到 Task Design 建立新版本。

---

# 6. Direct Entry Is the Default

`v001` 曾把 direct entry 与 Platform-private `.koplugin` 并列为 PoC candidates。`v002` 收敛为：

> **direct Baga private entry 是默认实现；`.koplugin` 只保留为有证据的 fallback。**

默认链：

```text
private KOReader bootstrap
→ setup environment/device/screen/input foundation
→ detect Baga private launch argument
→ baga/bootstrap.lua
→ Baga-owned surface
```

可使用类似：

```text
--baga-app <app-id>
```

的私有参数；参数名不是公共 API，可在实现中微调。

只有以下情形才启动 `.koplugin` fallback PoC：

```text
direct entry 无法避免 FileManager/Plugin UI 暴露
direct entry 生命周期无法稳定控制
crash recovery 无法可靠实现
upstream patch 维护成本明显不可接受
真实设备上 direct entry 无法完成稳定启动
```

且必须有日志/真机证据。没有证据时，不重新比较两种方案。

---

# 7. Diagnostics and Evidence

最小诊断信息：

```text
Baga build/version
pinned component versions
model / firmware / native target
launch timestamp
bootstrap stage markers
Lua bootstrap stage
screen initialization result
input initialization result
exit reason
last error
```

真机证据至少保留：

```text
build command/result
artifact digest
device facts
launch log
Baga-owned surface evidence
input result
exit/relaunch result
known warnings
```

---

# 8. Real-device Procedure

```text
1. 记录 model / firmware / Homebrew state
2. 备份本 Task 会修改的开发文件
3. 部署 pinned development build
4. 从 baga-launch 启动 direct private entry
5. 确认不进入普通 KOReader FileManager 产品路径
6. 确认 baga/bootstrap.lua 执行
7. 显示 Baga-owned test surface
8. 验证至少一条输入路径
9. clean exit
10. relaunch
11. 收集 crash/recovery evidence
12. 恢复测试文件并确认 Kindle 正常工作
```

---

# 9. Data Protection / Recovery

- 不覆盖用户书籍、笔记或 Kindle 数据库；
- 开发文件使用独立 Baga/pinned component 路径；
- 修改前保存可恢复副本；
- crash 后必须保留日志且可以回到 Kindle Home；
- 不把 reset/factory reset 作为普通恢复步骤。

---

# 10. Acceptance Gate

真实 `kindlehf` 上必须完成：

```text
baga-launch
→ pinned KOReader substrate initializes
→ direct Baga private entry
→ Lua Baga bootstrap runs
→ Baga-owned surface visible
→ at least one controlled input path works
→ clean exit
→ relaunch works
```

并且：

- 普通路径不要求进入 KOReader FileManager / Plugin menu；
- 没有为了语言统一增加不必要 FFI；
- `.koplugin` 未在无 blocker 证据时成为默认实现；
- 设备数据保持安全。

---

# 11. Expected Execution-Prompt Groups

```text
upstream pin / license manifest
kindlehf build baseline
baga-launch wrapper
direct private entry patch
Lua bootstrap
diagnostics
real-device launch/exit/relaunch
fallback trigger criteria validation
```

Execution Prompt 必须引用 Kindle Language and Binding Decision，不重新做语言或 direct-entry 方案选型。
