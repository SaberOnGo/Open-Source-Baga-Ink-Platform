# TASK-0060 v001 任务设计总纲 / Kindle Reader Provider Task Design

> **Task ID：`TASK-0060`**  
> **Version：`v001`**  
> **Milestone：K5 — `baga.reader` → KOReader reader stack**  
> **状态：Planned Baseline — dependency-gated**  
> **日期：2026-08-23**

---

## 0. Goal

通过 Baga `baga.reader` API 复用 Kindle Platform 内部的成熟 KOReader reader stack：

```text
IKP App
   ↓
baga.reader
   ↓
Baga Platform Reader implementation
   ↓
ReaderUI / CREngine / MuPDF
   ↓
Kindle Device Adapter
```

ReaderUI/CREngine/MuPDF 是 Platform internal adopted components；IKP App 不直接依赖其 Lua module、对象或文件布局。

---

# 1. Dependencies and Authority

前置：K3 Platform/Probe 链稳定，K4 的 App release/lifecycle 基础可用于受控测试。

权威输入：

```text
docs/zh-CN/standards/03_API规范.md
docs/zh-CN/standards/11_Kindle适配规范.md
docs/zh-CN/standards/13_标准库与成熟组件采用规范.md
docs/zh-CN/reference-apps/03_Kindle具体实现架构冻结.md
```

公共 `baga.reader` 语义高于 KOReader 私有实现。

---

# 2. Scope

`v001` 至少覆盖：

```text
minimal internal Reader bridge
opaque source handle → reader open
EPUB / TXT bring-up via CREngine
PDF bring-up via MuPDF
page / position mapping
search mapping
selection mapping
bookmark/highlight/annotation mapping where current Baga API requires
suspend/resume
position persistence
reader regression tests
relevant BICTS subset
```

---

# 3. Out of Scope

```text
重新实现 EPUB/PDF engine
把 KOReader private API 暴露给 IKP
LifeBook 社区文章/问答/评论 UI
跨设备公共笔记的新 ContentAnchor 标准
未进入当前 baga.reader Contract 的新 API
完整 TTS/Audio/Bluetooth 扩展
KOReader FileManager 用户路径
```

LifeBook 的社区内容使用 `baga.ui`；传统书籍才进入 `baga.reader`。

---

# 4. Implementation Boundary

禁止 IKP：

```lua
require("ui/uimanager")
require("apps/reader/readerui")
```

允许的内部关系：

```text
baga.reader.open(source)
→ Platform Reader bridge
→ private ReaderUI/CREngine/MuPDF operations
→ normalized Baga result/events
```

KOReader object lifetime、document object、XPointer 等私有表示不得直接成为跨平台 App Contract。

---

# 5. Source and Storage Handling

App 向 `baga.reader` 提供 Standard 允许的 source/handle；Platform 转换为 Reader backend 所需内部来源。

至少验证：

```text
valid local EPUB
valid local TXT
valid local PDF
missing/unreadable source
unsupported/corrupt source
source lifecycle across suspend/resume
```

Reader 临时文件、cache 与 App data 的边界应明确，不覆盖原始用户书籍。

---

# 6. Position and Event Mapping

优先实现当前 Contract 已定义的稳定语义：

```text
open/close
current position
position changed
search
selection
highlight/note/bookmark where required
```

KOReader 私有定位格式可保留在 Provider 内部；如未来跨设备公共笔记需要新的稳定 anchor/range 语义，应进入上位 Standard 设计流程，而不是在本 Task 私自定义。

---

# 7. E-Ink UI and Refresh

Reader stack 仍通过 Kindle Adapter 的 Display/Input/Lifecycle 能力工作。Reader Provider 不绕过 Adapter 建立第二套设备 contract。

验证重点：

```text
page turn refresh behavior
full/partial refresh safety
navigation/touch consistency
reader overlays/selection visibility
suspend/resume redraw
```

具体 waveform/backend 细节保持为 Kindle implementation detail。

---

# 8. Test Strategy

## Host/Integration

```text
Reader bridge lifecycle
source conversion
format routing
normalized result/events
position persistence serialization
error mapping
```

## Real Kindle

```text
open EPUB/TXT/PDF
page navigation
search
selection
position save/restore
sleep/wake
close/reopen
multiple consecutive opens
```

至少使用小型固定测试书作为 reproducible fixture，不以用户私人书籍作为唯一证据。

---

# 9. Debug Strategy

```text
baga.reader API input
→ Platform Reader bridge
→ ReaderUI/document backend
→ Kindle Adapter display/input
→ normalized event/result
```

每层需要独立日志 tag，避免把 reader-engine error、display error 与 App API error 混为同一类。

---

# 10. Real-device Evidence and Data Protection

保留：

```text
format/file fixture id
reader backend/version
open result
position before/after
search/selection result
sleep/wake result
reopen result
crash/error log
```

测试不修改原始书籍；annotation fixture 应使用专用测试数据。失败恢复可清理 Provider cache/test state，而不删除用户书库。

---

# 11. Acceptance Gate

- [ ] IKP 仅通过 `baga.reader` 使用阅读能力。
- [ ] EPUB/TXT 可通过 CREngine backend 打开并翻页。
- [ ] PDF 可通过 MuPDF backend 打开并翻页。
- [ ] page/position/search/selection 至少达到当前 API 要求。
- [ ] position 在 close/reopen 后可恢复。
- [ ] sleep/wake 后 Reader 可恢复到有效状态。
- [ ] Reader Provider 通过 Kindle Adapter 使用设备能力，不建立第二套 display/input contract。
- [ ] KOReader FileManager/Plugin UI 不成为用户产品路径。
- [ ] KOReader private module/object 不泄漏到 IKP API。
- [ ] reader 相关 BICTS/regression tests 通过。

---

# 12. Known Risks

主要风险：KOReader private API 随 upstream pin 更新变化、不同格式 position 语义不一致、selection 几何映射、ReaderUI 生命周期与 Platform 生命周期冲突、Reader cache/data 边界混乱。

这些风险应尽量封装在 Platform Reader implementation 内，避免传播到 Universal IKP。

---

# 13. Expected Execution-Prompt Groups

```text
A. Reader API/KOReader boundary audit
B. minimal internal bridge
C. EPUB/TXT bring-up
D. PDF bring-up
E. position/search/selection mapping
F. persistence + lifecycle
G. annotation-related current-contract mapping
H. real-device reader regression / K5 Gate
```
