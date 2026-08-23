# TASK-0070 任务版本索引 / Task Version Index

> **Task ID：`TASK-0070`**  
> **任务：KPM 打包与 Kindle 首页入口 / KPM Packaging and Kindle Home Entry**  
> **关联 Milestone：K6**  
> **当前选定版本：`v001`**  
> **状态：Planned Baseline — dependency-gated**  
> **日期：2026-08-23**

---

## 1. Task 目标

把已在开发 Kindle 上稳定运行的 Baga Platform/Adapter/Reader 组件包装为 Kindle native Platform package，并建立普通用户可从 Kindle Home 一次进入 Baga App 的产品入口。

---

## 2. Version History

| Version | Status | Summary | Reason |
|---|---|---|---|
| `v001` | Planned | `.kpkg`、install/launch/uninstall、health check、sh_integration Home Entry、data preservation | 首个 Kindle Platform 产品化安装任务设计 |

---

## 3. Dependency Gate

```text
K1 substrate/entry stable
K2 Adapter stable
K3 Probe chain stable
K4 IKP installer/verifier stable
K5 Reader baseline stable where included in package
```

---

## 4. Authority / Inputs

```text
docs/zh-CN/reference-apps/03_Kindle具体实现架构冻结.md
docs/zh-CN/standards/11_Kindle适配规范.md
current Platform update / recovery standards
```

---

## 5. Current Design

```text
v001/0000_任务设计总纲_Task-Design-Overview.md
```

若 KPM compatibility、Home Entry backend、update/uninstall data policy 或 fallback envelope 发生结构性变化，应创建新版本。
