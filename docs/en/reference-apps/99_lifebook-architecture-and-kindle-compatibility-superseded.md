# LifeBook IKP Architecture and Kindle Compatibility — Superseded

> **Document level:** Superseded Compatibility Entry  
> **Document ID:** `reference-apps.99`  
> **Locale:** English (`en`)  
> **Status:** **SUPERSEDED**  
> **Original baseline:** v0.5, 2026-08-23  
> **Replacement:** `docs/en/reference-apps/03_baga-ink-kindle-implementation-architecture-freeze.md`  
> **Counterpart:** `docs/zh-CN/reference-apps/99_旧版LifeBook架构与Kindle兼容实现.md`

---

## Status

This document originally summarized LifeBook IKP and Kindle compatibility implementation, but the 2026-08-23 Kindle Implementation Architecture Freeze completed/corrected critical areas including:

- `.ikp` vs `.kpkg` responsibility boundary;
- KPM vs IKP Package Manager as two package managers at different layers;
- strict distinction between **KPM not installed** and **KPM incompatible with this Kindle/target**;
- KPM / MRPI / legacy installer-envelope state machine;
- minimal Baga Platform Core responsibilities;
- removal of formal `Baga Platform Runtime` / `LifeBook Runtime` terminology;
- pinned/private KOReader reuse inside Kindle Platform with no LifeBook private-API dependency;
- formal roles for sh_integration / AppMgr / KUAL / PEKI / KindleTool;
- WinterBreak / SpringBreak / Sanctuary / Véra only as Client Installation Route records;
- the complete Client → bootstrap → Homebrew foundation → Platform install → IKP transfer → Kindle Home launch chain.

Therefore **this file is no longer an implementation or module-selection authority**.

All subsequent Kindle implementation work MUST use:

```text
docs/en/reference-apps/03_baga-ink-kindle-implementation-architecture-freeze.md
```

Authority order:

```text
Baga Ink Standards
        >
03 Kindle Implementation Architecture Freeze
        >
other Kindle Reference / Product supplemental docs
        >
code and prototypes
```

Historical detail remains available in Git history rather than being repeated here, to prevent developers or AI agents from reviving corrected legacy architecture as a current candidate.
