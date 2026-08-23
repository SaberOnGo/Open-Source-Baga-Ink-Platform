# Baga Ink Permission Model

> **Document level:** First-level platform standard  
> **Document ID:** `standards.05`  
> **Locale:** English (`en`)  
> **Status:** Draft v0.1  
> **Date:** 2026-08-22  
> **Parent:** `01_baga-ink-platform-strategy.md`  
> **Related:** Standards 02, 03, 04  
> **Counterpart:** `docs/zh-CN/standards/05_权限模型.md`

---

## 0. Purpose

Baga Ink Permission Model defines which user data, device capabilities, and Platform resources a third-party IKP App is allowed to access.

Core distinction:

> **Capability answers whether the device can do something; Permission answers whether the App is allowed to use it.**

Baga Ink MUST avoid both extremes:

1. treating every Lua App as a fully trusted system script;
2. interrupting the user with a permission dialog for every minor action.

The model therefore uses:

```text
Manifest pre-declaration
+ least privilege
+ on-demand confirmation for higher-risk access
+ revocable grants
+ Platform-provided authorization UI where the OS lacks one
```

---

## 1. Core rules

1. An App MUST predeclare every permission it may request in its IKP Manifest.
2. An App MUST NOT request a permission absent from its Manifest.
3. Platform MUST deny unauthorized resources by default.
4. Permission and Capability MUST remain separate concepts.
5. Platform MAY use different OS-level authorization mechanisms per device while exposing the same App semantics.
6. After permission revocation, Apps MUST correctly handle `permission_denied`.
7. Universal Apps MUST NOT bypass permission controls via Shell, Vendor API, or native escape mechanisms.

---

## 2. Permission states

Every permission supports at least:

```text
not_declared
not_granted
granted
denied
restricted
```

Meaning:

- `not_declared`: absent from Manifest; cannot be requested at runtime;
- `not_granted`: declared but not yet authorized;
- `granted`: allowed;
- `denied`: rejected by user or policy;
- `restricted`: device/management/Platform policy does not allow the grant.

Platform MAY support grant modes such as:

```text
grant_once
grant_while_using
grant_persistent
```

v0.1 does not require every device family to implement all modes.

---

## 3. API relationship

Standard API:

```lua
baga.permissions.check(name)
baga.permissions.request(name)
baga.permissions.list()
```

`request()` MAY return an asynchronous Task.

Example:

```lua
if not baga.permissions.check("network") then
    baga.permissions.request("network")
end
```

Calling `request()` MUST NOT cause automatic grant.

---

## 4. v0.1 Permission Registry

### 4.1 `network`

Allows an App to issue network requests through Baga Ink Network API.

Does not allow:

- raw sockets that bypass Platform policy;
- modifying system Wi-Fi configuration directly;
- running network commands through Shell.

### 4.2 `library.read`

Allows reading user-library metadata and authorized content exposed by the Platform.

It is not permission to traverse the full filesystem.

### 4.3 `library.write`

Allows standardized mutation of the user library, for example import, delete, or move operations.

Because this can cause user-data loss, Platform SHOULD provide confirmation and/or recoverable trash semantics for dangerous operations.

### 4.4 `notes.read`

Allows reading Baga-standard notes/annotation resources.

### 4.5 `notes.write`

Allows creation and modification of standardized notes/annotations.

### 4.6 `user_files.read`

Allows reading ordinary files explicitly selected or authorized by the user.

MUST NOT mean unrestricted disk read access.

### 4.7 `user_files.write`

Allows writing to locations explicitly selected or authorized by the user.

### 4.8 `clipboard`

Allows access to a unified clipboard capability.

If the underlying device has no system clipboard, Platform MAY provide a lightweight Baga clipboard.

### 4.9 `audio.output`

Allows use of audio output through Baga interfaces.

If the corresponding Capability is absent, an authorized call still returns `not_supported`.

### 4.10 `bluetooth`

Allows access to Bluetooth capabilities exposed by Baga Ink.

Scanning, connection, and other privacy/power-sensitive operations MAY be split into finer permissions later.

### 4.11 `frontlight.control`

Allows modifying device frontlight settings.

Reading the current light value MAY be lower risk; writes require the control permission.

### 4.12 `power.keep_awake`

Allows an App to request temporary keep-awake behavior.

Platform always retains the right to refuse unreasonable requests.

---

## 5. Permission risk levels

To reduce unnecessary prompts, permissions SHOULD be grouped by risk:

```text
Level 0: Sandbox internal
Level 1: Low-risk shared capability
Level 2: User data access
Level 3: Device control / privacy-sensitive
```

### Level 0

Examples:

```text
appdata
cache
```

No user confirmation is needed because access affects only the App's own sandbox.

### Level 1

For example ordinary network access, which may also be governed by global user policy.

### Level 2

Examples:

```text
library.read
notes.read
user_files.read
```

These expose user data and should be transparently disclosed.

### Level 3

Examples:

```text
library.write
user_files.write
bluetooth
frontlight.control
power.keep_awake
```

Platform SHOULD authorize these more cautiously.

---

## 6. Manifest declaration

Example:

```json
{
  "permissions": [
    "network",
    "library.read",
    "notes.write"
  ]
}
```

Market MUST be able to present a permission summary before installation.

If an update adds permissions, for example:

```text
v1.2: network
v1.3: network + user_files.write
```

Platform / Market SHOULD treat that as an important change and clearly inform the user.

---

## 7. Consistent semantics across Kindle and Android

Underlying authorization mechanisms may differ.

Android may use:

```text
Android permissions / SAF / app sandbox / vendor policy
```

Kindle may use:

```text
Baga Platform permission policy + filesystem isolation + bridge rules
```

But the App-facing semantic surface remains:

```lua
baga.permissions.check(...)
```

The lack of an Android-style OS permission dialog on Kindle MUST NOT automatically grant Kindle Apps broader access.

---

## 8. User authorization UI

Permission UI SHOULD:

- be high contrast;
- use concise text;
- avoid animation dependence;
- explain why access is needed;
- explain the scope of access;
- allow rejection;
- allow later modification in Settings.

Avoid vague prompts such as:

```text
Allow access to all files?
```

Prefer scoped language such as:

```text
Allow Example Reader to read the books you select?
```

The UI wording must match the actual technical scope.

---

## 9. Data-domain isolation

Baga SHOULD distinguish:

```text
App Private Data
User Library
Notes / Highlights
User-selected Files
Shared Platform Data
System / Device Data
```

App Private Data is accessible only to that App by default.

Cross-App sharing MUST use an explicit Platform API rather than a shared physical directory.

---

## 10. Revocation

After the user revokes a permission:

- Platform MUST enforce revocation immediately or at the next safe boundary;
- App SHOULD receive a standard permission-change event;
- handling of already-cached sensitive data is governed by future Data Policy;
- App MUST NOT repeatedly harass the user to re-grant a denied permission.

Platform MAY throttle repeated requests.

---

## 11. Background behavior

Baga Ink targets low-power e-paper hardware; background behavior is restricted by default.

Having `network` permission does not mean an App may communicate indefinitely in the background.

Having `power.keep_awake` does not mean an App may permanently disable sleep.

Platform policy may restrict execution based on:

```text
battery
charging state
Wi-Fi state
sleep policy
user settings
```

---

## 12. High-risk mechanisms do not become ordinary permissions

v0.1 does not expose the following as normal Universal App permissions:

```text
raw shell
process spawn
kernel access
raw framebuffer
Android Context
direct JNI
Vendor SDK
system package install
arbitrary filesystem root
```

These belong to Platform Core / Device Adapter / controlled extension implementation layers.

---

## 13. Permission and Market

Baga Ink Market SHOULD display:

```text
permission name
purpose
version first introduced
risk level
```

Market MAY apply additional review to high-risk permissions.

A Universal label does not mean "zero permissions"; it means permissions are declared transparently and enforced through standard mechanisms.

---

## 14. Permission tests

The Compatibility Test Suite MUST verify at least:

- undeclared permissions cannot be obtained;
- denied state returns correctly;
- sandbox boundaries cannot be crossed;
- revoked access no longer works;
- Kindle and Android expose the same error semantics;
- an App cannot bypass restrictions through the standard Lua environment.

---

## 15. Core rule

> **Capability solves fragmentation; Permission defines access boundaries. The two must remain separate.**

A stable permission model allows Baga Ink to remain open to third-party applications without degenerating into "Lua App = arbitrary system script".
