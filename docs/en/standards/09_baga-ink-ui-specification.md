# Baga Ink UI Specification

> **Document level:** First-level Platform Standard  
> **Document ID:** `standards.09`  
> **Locale:** English (`en`)  
> **Status:** Draft v0.1  
> **Date:** 2026-08-22  
> **Parent:** `01_baga-ink-platform-strategy.md`  
> **Related:** Standards 02, 03, 04  
> **Counterpart:** `docs/zh-CN/standards/09_UI规范.md`

---

## 0. Purpose

This document defines a unified UI model for third-party IKP Apps across Kindle and Android e-paper devices.

The goal is not to copy Android View, Flutter, or Web UI. Baga UI should be:

- e-paper friendly;
- usable on touch and non-touch devices;
- portable across different resolutions;
- conservative about unnecessary refresh;
- able to map physical page keys;
- independent of vendor-private refresh APIs.

Core principle:

> **Apps describe interface structure and refresh intent; Platform decides how rendering and physical e-paper refresh are performed.**

---

## 1. UI design principles

A Baga Ink App SHOULD:

1. prioritize high contrast;
2. prioritize text readability;
3. prefer page-oriented navigation over continuous animation;
4. prefer local/dirty-region updates over unnecessary full-screen refreshes;
5. never use color as the sole carrier of meaning;
6. never make hover, animation, or gesture the only way to access an action;
7. support semantic navigation;
8. remain operable on low-refresh devices.

---

## 2. Baseline components

v0.1 core semantic components:

```text
Page
Text
Image
Button
List
Menu
Dialog
Toolbar
Input
ReaderView
Spacer
Divider
```

These are semantic UI concepts. Underlying Platforms are not required to use the same rendering library.

---

## 3. `Page`

`Page` is the basic Baga UI page container.

Conceptual usage:

```lua
baga.ui.page({
    title = "Library",
    body = {...},
    toolbar = {...}
})
```

A Page SHOULD support:

- title;
- content/body;
- footer / toolbar;
- focus root;
- lifecycle hooks;
- scroll / paged content policy.

On non-touch devices a Page MUST be able to enter focus-navigation mode.

---

## 4. `Text`

Text MUST support:

```text
text
font_size
weight
align
wrap
max_lines
```

It SHOULD support:

```text
selectable
line_spacing
paragraph_spacing
```

Font APIs must use logical font identities rather than physical system-font paths tied to a device.

---

## 5. `Image`

Image SHOULD support:

```text
source
fit
width
height
alt_text
```

Platform MAY apply:

- grayscale conversion;
- dithering;
- scaling;
- color-device optimization.

Apps must not assume an RGB color screen exists.

---

## 6. `Button`

A Button MUST be activatable through at least one mechanism available on the current device, such as:

- touch;
- semantic `confirm` action;
- keyboard.

Buttons SHOULD expose an obvious focus state.

For e-paper, preferred focus indicators include:

```text
border
inversion
underline
high-contrast background
```

rather than blinking animation.

---

## 7. `List`

List is a core Baga navigation component.

It SHOULD support:

```text
vertical list
paged list
selection/focus
virtualization
page_next/page_previous
```

Long lists MUST avoid rendering the entire dataset at once.

On Kindle-class devices, Platform MAY map scrolling into page-oriented movement.

---

## 8. `Menu`

Menu SHOULD support:

```text
items
selected
shortcut/action
submenu
```

Menus must be operable through semantic actions such as:

```text
up
down
confirm
back
```

---

## 9. `Dialog`

Dialog is used for:

- confirmation;
- permission requests;
- errors;
- simple input;
- destructive-operation confirmation.

Dialog SHOULD:

- avoid deep nesting;
- keep text concise;
- expose an obvious default focus;
- support `back` to close where safe;
- refresh only the necessary display region where practical.

---

## 10. `Toolbar`

Toolbar should not copy animation-heavy mobile bottom navigation.

Recommended direction:

```text
few primary actions
text + simple icons
focus-navigation support
```

On compact Kindle screens Platform MAY collapse a Toolbar into a Menu.

---

## 11. Layout model

v0.1 SHOULD use a simple deterministic layout model:

```text
Row
Column
Stack
Fixed / Flex size
Margin
Padding
Alignment
```

The first phase intentionally avoids a complex CSS layout engine.

Goal:

> **Predictable cross-platform behavior before unlimited layout power.**

---

## 12. Coordinates and sizing

Apps SHOULD use Platform-provided logical dimensions.

Do not:

```text
assume Kindle is always 1072×1448
assume Android has a fixed density
hard-code pixel layouts by model/vendor
```

UI should adapt from:

```text
logical width
logical height
orientation
text scale
input capabilities
```

---

## 13. Responsive profile

Baga does not mechanically copy mobile breakpoints, but MAY define logical screen classes such as:

```text
compact
medium
large
```

Classification is based on usable logical size and typography, not device model names.

Apps SHOULD query layout Profile instead of identifying hardware models.

---

## 14. Focus model

Because some Kindle-class devices do not have touch, or rely heavily on physical navigation, Focus is a first-class UI concept.

Interactive controls MUST be able to participate in:

```text
focus
blur
activate
move_next
move_previous
```

Platform SHOULD provide default focus traversal.

Apps MAY customize focus order for complex pages.

---

## 15. Semantic actions

UI should be designed around:

```text
confirm
back
menu
page_next
page_previous
focus_next
focus_previous
```

Underlying events may originate from:

- Kindle page buttons;
- touch;
- Android volume keys where mapped by Platform policy;
- keyboard;
- Bluetooth remote.

---

## 16. Refresh Intent

The UI/Display boundary is a key Baga concept.

App/UI MAY express intent such as:

```text
content_changed
small_interaction
page_changed
quality_needed
continuous_interaction
```

Platform maps intent into semantic display modes such as:

```text
AUTO
TEXT
FAST
QUALITY
ANIMATION
```

Apps MUST NOT pass vendor waveform IDs.

---

## 17. Dirty Region

The UI implementation SHOULD track dirty regions.

Example:

```text
button focus changes
→ invalidate only the button-related region
```

not:

```text
any state change
→ full-screen refresh
```

Platform MAY merge multiple dirty regions.

---

## 18. Ghosting policy

Ghosting management primarily belongs to Platform / Device Adapter.

Apps should not implement private policies such as:

```text
force full refresh every N updates
```

Preferred chain:

```text
UI state change
  ↓
Display intent
  ↓
Platform refresh policy
  ↓
Device Adapter
```

This allows each device family to use appropriate ghosting-clearing behavior.

---

## 19. Animation policy

Default principle:

> **No animation is better than bad animation.**

Universal Apps SHOULD NOT depend on animation to communicate state.

Animation MAY be used when:

- the device declares `display.animation`;
- animation materially improves comprehension;
- Platform can safely downgrade it to discrete frames or no animation.

Platform MUST be able to disable animation globally.

---

## 20. Scroll policy

Continuous pixel scrolling is not the default e-paper interaction model.

Platform SHOULD support:

```text
paged
step_scroll
continuous_scroll (optional)
```

Apps SHOULD tolerate downgrade to `paged`.

Reader / long-form content should prefer page-oriented or stepped navigation.

---

## 21. Touch targets

On touch devices, interactive regions SHOULD be large enough for reliable input.

v0.1 does not freeze a specific dp value, but the compatibility/app test suite SHOULD verify:

- controls are not extremely narrow/small;
- primary actions have reasonable spacing;
- the UI does not depend on tiny icon-only hit targets.

---

## 22. Pen UI

If `input.pen` is available:

- UI MAY expose pen input;
- touch and pen SHOULD be distinguishable;
- low-latency ink MUST use a standardized Platform Capability;
- Apps do not call BOOX/iReader private handwriting SDKs directly.

When Pen is absent, Apps must handle required/optional capability semantics correctly.

---

## 23. Color policy

Color is not a baseline assumption.

Apps MUST NOT use color as the only state distinction.

Wrong:

```text
green = success
red = failure
```

Correct:

```text
✓ success
! failure
```

Color is progressive enhancement only.

---

## 24. Icon guidelines

Icons SHOULD:

- have clear outlines;
- remain distinguishable in monochrome;
- avoid dependence on gradients;
- remain legible at low resolution;
- provide text alternatives or accessibility labels.

---

## 25. Permission UI

Permission dialogs are Platform-provided standard UI.

An App MUST NOT imitate/forge the Platform authorization UI.

Permission pages must clearly show:

```text
App name
permission name
purpose
Allow / Deny
```

---

## 26. Error UI

Standard errors SHOULD map to user-meaningful states such as:

```text
offline
permission_denied
not_supported
incompatible
not_found
io_error
```

Apps SHOULD present an actionable next step instead of raw vendor error codes.

---

## 27. Accessibility

Even in the first phase, Baga SHOULD preserve:

- text scaling;
- high contrast;
- focus order;
- icon text alternatives;
- non-color-only meaning;
- keyboard / physical-key navigation.

---

## 28. UI Theme

Baga SHOULD provide baseline theme tokens such as:

```text
background
foreground
border
muted
focus
font.body
font.title
spacing.*
```

Apps SHOULD use tokens instead of hard-coding large amounts of device-specific styling.

A complex theme marketplace is not a first-phase goal.

---

## 29. LifeBook as Reference UI

LifeBook SHOULD be the first major Baga UI Reference App.

Its role is not privileged access. Its role is to validate that experiences such as:

```text
articles
Q&A
comments
notes
book reading
lists
menus
sync status
AI conversation
```

can be implemented using only standard UI/API semantics across Kindle and Android E-Paper.

If LifeBook reveals a missing platform-level UI capability, the preferred response is standardization — not a LifeBook-private escape hatch.

---

## 30. UI compliance testing

Compatibility / App tests SHOULD verify:

- pages render;
- non-touch devices can navigate;
- touch devices can activate controls;
- `page_next` / `page_previous` work;
- focus is visible;
- compact/large screens do not suffer severe overflow;
- information is not lost on monochrome devices;
- Display intent does not leak vendor APIs;
- small-region updates do not cause unnecessary full refreshes.

---

## 31. Core rule

> **Baga Ink UI is not about drawing identical pixels everywhere; it is about preserving the same interaction semantics across devices while allowing each e-paper platform to render and refresh in the most appropriate way.**
