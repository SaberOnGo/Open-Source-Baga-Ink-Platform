# LifeBook IKP 架构与 Kindle 兼容实现 / LifeBook IKP Architecture and Kindle Compatibility

> **状态：SUPERSEDED / 兼容入口**  
> **原 Baseline：v0.5，2026-08-23**  
> **替代文档：`03_Kindle具体实现架构冻结_Baga-Ink-Kindle-Implementation-Architecture-Freeze.md`**

---

## 0. 文档状态

本文件原先用于整理 LifeBook IKP 与 Kindle 兼容实现，但 2026-08-23 的进一步架构冻结已经补齐并修正以下关键问题：

- `.ikp` 与 `.kpkg` 的职责边界；
- KPM 与 IKP Package Manager 是不同层的两个 Package Manager；
- **KPM 未安装**与**该 Kindle/KPM target 不兼容**必须严格区分；
- KPM / MRPI / legacy installer envelope 的选择状态机；
- Baga Platform Core 的最小职责；
- 正式架构中不再使用 `Baga Platform Runtime` / `LifeBook Runtime`；
- KOReader 必须由 Kindle Platform 私有、锁版本复用，LifeBook 不直接依赖其 private API；
- sh_integration / AppMgr / KUAL / PEKI / KindleTool 的正式定位；
- WinterBreak / SpringBreak / Sanctuary / Véra 仅属于 Client Installation Route DB；
- Client → bootstrap → Homebrew foundation → Platform install → IKP transfer → Kindle Home launch 的完整执行链。

因此，**本文件不再作为 Kindle 代码实现或模块选型依据。**

后续所有 Kindle implementation work 必须读取：

```text
docs/reference-apps/03_Kindle具体实现架构冻结_Baga-Ink-Kindle-Implementation-Architecture-Freeze.md
```

权威优先级：

```text
Baga Ink Standards
        >
03 Kindle Implementation Architecture Freeze
        >
其他 Kindle Reference / Product 补充文档
        >
代码与原型
```

历史内容由 Git commit / diff 保留，不在当前正式正文继续保存，以避免开发者或 AI 把已经修正的旧表述重新当成候选架构。
