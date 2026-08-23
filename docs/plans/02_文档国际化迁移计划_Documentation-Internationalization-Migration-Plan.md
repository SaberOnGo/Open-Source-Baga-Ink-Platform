# Baga Ink 文档国际化迁移计划 / Documentation Internationalization Migration Plan

> **文档级别：Implementation Plan / 文档基础设施迁移计划**  
> **状态：Plan Baseline v0.1**  
> **日期：2026-08-23**  
> **上位治理：`docs/en/governance/01_documentation-internationalization-policy.md` / `docs/zh-CN/governance/01_文档国际化与本地化规范.md`**

## 0. Goal

把当前以中文为主、文件名中英混合的公共文档体系迁移为：

```text
docs/en/
docs/zh-CN/
```

同时保证：

- Standards / Design / Reference Apps / Governance / Status 形成稳定国际化入口；
- 中英文属于同一 Document Identity，不形成两套协议；
- `docs/plans/` 不因国际化而复制几千份 Task / AI Execution Prompt；
- 机器规范、Reference Implementation、Tests、API/Schema/Code 保持英文/语言无关；
- 迁移过程中不通过“盲目批量重命名”破坏文档内部引用和架构边界。

## 1. Final target structure

```text
docs/
├── README.md
├── README.zh-CN.md
│
├── en/
│   ├── 00_baga-ink-documentation-index.md
│   ├── standards/
│   ├── design/
│   ├── reference-apps/
│   ├── governance/
│   └── status/
│
├── zh-CN/
│   ├── 00_项目文档入口.md
│   ├── standards/
│   ├── design/
│   ├── reference-apps/
│   ├── governance/
│   └── status/
│
├── plans/
│   └── ...
│
└── localization/
    └── catalog.json
```

最终必须删除旧公共目录：

```text
docs/standards/
docs/design/
docs/reference-apps/
docs/governance/
docs/status/
docs/00_项目文档入口_Baga-Ink-Documentation-Index.md
```

这些旧路径只在迁移阶段暂时存在。

## 2. Naming rules

### English public docs

```text
NN_lowercase-kebab-case-name.md
```

### Simplified Chinese public docs

```text
NN_中文名称.md
```

同一 category 内，中英文 counterpart MUST 使用相同 `NN`。

Public doc 的两位编号是**稳定 Document Number**，不是 Task 排序号，因此不机械改成四位。

`docs/plans/platform-ports/` 的四位编号规则继续独立生效，因为那里是大量 Task / Prompt 的工程工作区。

## 3. Phase M0 — Internationalization foundation

建立：

```text
docs/README.md
docs/README.zh-CN.md
docs/en/00_baga-ink-documentation-index.md
docs/zh-CN/00_项目文档入口.md
docs/en/governance/01_documentation-internationalization-policy.md
docs/zh-CN/governance/01_文档国际化与本地化规范.md
docs/localization/catalog.json
tools/check_docs_i18n.py
tools/new_localized_doc.py
CI integration
AGENTS hard gate
```

并把旧公共目录冻结为 Legacy Migration Zone。

### M0 Gate

- Final path model is documented;
- new public documents cannot be added to legacy directories;
- new localized docs have enforced filename rules;
- catalog can track migration/translation status;
- CI can reject invalid layout;
- existing Kindle Task/Execution Prompt model is unaffected.

## 4. Phase M1 — Move Chinese authoritative working editions

按 `catalog.json` 一份一份迁移：

```text
legacy_path
   ↓
docs/zh-CN/<category>/<NN_中文名称>.md
```

迁移时必须：

1. 保留原文语义；
2. 不为了“中文化”改写 canonical English technical identity；
3. 修复所有相对链接和硬编码路径；
4. 更新 AGENTS / Documentation Index / Status / Plans 中的引用；
5. 更新 Catalog status；
6. 运行文档链接检查和 CI。

不要把“文件移动”和“架构内容重写”混在同一个迁移步骤里。

### 建议批次

```text
M1-A  Governance + Status + Documentation Index
M1-B  Standards 00–13
M1-C  Standards 20–28
M1-D  Design
M1-E  Reference Apps
```

## 5. Phase M2 — English editions

英文版优先级：

```text
Priority 0
→ Standards Index
→ Strategy / App / API / Capability / Permission / IKP
→ Device Adapter Contract
→ Compatibility / BICTS
→ Kindle / Android E-Paper Adapter

Priority 1
→ Market / Distribution / Signing / Repository / Update protocols

Priority 2
→ Design
→ Reference Apps
→ Governance / Status supporting docs
```

Translation MUST preserve:

- RFC 2119-style normative words where applicable (`MUST`, `SHOULD`, `MAY`);
- API identifiers;
- field names;
- code blocks;
- version numbers;
- error codes;
- package names;
- project/library names;
- architecture boundary meaning.

AI translation MAY accelerate work, but a translation must be reviewed against the Chinese edition and machine-readable contract before Catalog status becomes `current`.

## 6. Phase M3 — Pair synchronization guard

当一个文档进入 `current` 后：

```text
zh-CN semantic change
      ↕
English semantic change
```

SHOULD 在同一个 PR 中同步。

未来 Guard SHOULD 逐步增加：

```text
pair identity check
same category/number check
translation state check
stale counterpart detection
broken link detection
public terminology lint where practical
```

不能把“英文没同步”隐藏成普通 commit history 问题。

## 7. Phase M4 — Remove Legacy Migration Zone

只有当某个 legacy document 已经：

```text
moved to zh-CN
+
all links updated
+
English status explicit
+
Catalog updated
+
CI pass
```

才删除旧文件。

当所有 legacy entries 完成以后，整体删除：

```text
docs/standards/
docs/design/
docs/reference-apps/
docs/governance/
docs/status/
old documentation index
```

随后 Guard 从“冻结 legacy 列表”切换成：

> **Legacy public directories MUST NOT exist.**

## 8. Plans / Kindle special rule

`docs/plans/platform-ports/kindle/` 不做全文双语镜像。

原因：

```text
Task Design 数百份
Execution Prompt 数千份
频繁调试/真机步骤
```

全部翻译会形成巨大的同步负担，而且这些文档不是 Universal Contract。

现有规则继续：

```text
NNNN_中文名_English-Name.md
```

正文允许中文优先。

但是：

```text
外部实现者需要依赖的稳定结论
      ↓
MUST 回写 Public Localized Docs
```

## 9. Root repository internationalization

最终 SHOULD 建立：

```text
README.md              English default
README.zh-CN.md        Chinese
CONTRIBUTING.md        English default
CONTRIBUTING.zh-CN.md  Chinese
```

`AGENTS.md` 保持英文，因为它是 AI/Automation 的机器工作入口；中文维护者通过 `docs/zh-CN/governance/` 获得完整人类可读说明。

## 10. Completion Gate

文档国际化基础完成的最低标准：

```text
[ ] locale tree is stable
[ ] filename rules enforced
[ ] legacy public dirs no longer accept new docs
[ ] public doc catalog complete
[ ] Chinese docs migrated
[ ] English Standards complete
[ ] critical Design / Reference Apps translated
[ ] indexes and root README localized
[ ] CI checks localization structure
[ ] no Stable Standard relies on a stale required locale edition
```

最终目标不是“翻译得多”，而是：

> **任何中国维护者或国际开发者，都可以从自己能读懂的入口理解同一套 Baga Ink Platform，而代码、协议、测试和文档不会因为语言不同而分叉。**
