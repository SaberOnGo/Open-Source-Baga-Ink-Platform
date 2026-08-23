# Baga Ink Catalog and App Discovery Specification

> **Document level:** Distribution Catalog / Discovery Specification  
> **Document ID:** `standards.28`  
> **Locale:** English (`en`)  
> **Status:** Draft v0.1  
> **Date:** 2026-08-22  
> **Parent:** `docs/en/standards/20_baga-ink-market-and-distribution-architecture.md`  
> **Repository:** Standard 23  
> **Publishing:** Standard 24  
> **Counterpart:** `docs/zh-CN/standards/28_市场目录与应用发现规范.md`

---

## 0. Purpose

This document defines application catalog data, app detail records, localization, categories, search, compatible-release discovery, low-bandwidth indexes/diffs, offline catalogs, assets, recommendations, and advertising-label rules for Baga Ink Market and compatible third-party Repositories.

Most important boundary:

> **Catalog helps users discover Apps, but it does not decide application identity, release authenticity, or whether a release may replace an installed App.**

Final install decisions return to:

```text
Signed Repository Metadata
Release Record
Publisher Identity
IKP Publisher Signature
Local Installed Identity
Compatibility / Permission Check
```

---

## 1. Catalog data vs security metadata

### 1.1 Catalog data

Includes:

```text
app name
short summary
full description
localization
icon
screenshots
category
tags / search keywords
Publisher display information
license / source information
privacy summary
Permission summary
Compatibility summary
recommendations / charts
```

### 1.2 Security-critical data

Catalog MUST NOT be the sole authority for:

```text
app_id
publisher_id
release_sequence
package_sha256
package_length
App Ownership
App Signing Key
Permission truth
Capability truth
API range
Release revocation state
```

Catalog MAY copy these fields for display, but it must reference immutable Release Records and they are cross-checked before installation.

---

## 2. Catalog targets

Catalog files are ordinary Repository Targets protected by Targets Metadata length + SHA-256.

Recommended types:

```text
catalog-root.json
catalog-index.json
catalog-app-record.json
catalog-diff.json
asset-descriptor.json
```

Catalog does not create another independent root-key system. Its integrity inherits Repository Root → Targets → Target Digest.

---

## 3. Catalog Root

Conceptual form:

```json
{
  "type": "baga.catalog-root",
  "format": "0.1",
  "repository_id": "repo1_...",
  "catalog_sequence": 620,
  "generated_at": "...",
  "index": {
    "path": "catalog/sha256/...json",
    "length": 48291,
    "sha256": "..."
  },
  "shards": [],
  "diffs": [],
  "supported_locales": ["en", "zh-CN", "ja"],
  "default_locale": "en"
}
```

Catalog Sequence tracks Catalog-data change only. It is not App Release Sequence.

Catalog text may change with a new Catalog Sequence without publishing a new IKP.

---

## 4. App Catalog Record

Each App SHOULD have an independent content-addressed Catalog Record.

```json
{
  "type": "baga.catalog-app",
  "format": "0.1",
  "repository_id": "repo1_...",
  "app_id": "com.example.reader",
  "publisher_id": "pub1_...",
  "publisher_display_name": "Example Studio",
  "title": {
    "en": "Example Reader",
    "zh-CN": "示例阅读器"
  },
  "summary": {},
  "description": {},
  "category": "reader",
  "tags": ["epub", "offline"],
  "icon": {
    "path": "assets/sha256/...png",
    "length": 10240,
    "sha256": "..."
  },
  "screenshots": [],
  "license": "MIT",
  "source": {
    "url": "...",
    "verified": false
  },
  "privacy": {},
  "support": {},
  "release_channels": {},
  "review_attestations": [],
  "updated_at": "..."
}
```

A Catalog Record references security Release Records; it does not invent an installable package URL as authority.

---

## 5. Localization

Localized fields use Locale Maps:

```json
{
  "en": "A lightweight reader",
  "zh-CN": "轻量阅读器",
  "ja": "軽量リーダー"
}
```

Fallback order:

```text
exact locale
→ language-only locale
→ repository default locale
→ first available value
```

Rules:

- missing developer localization MUST NOT be silently machine-translated and presented as developer-authored text;
- Market-generated machine translations must be marked;
- localized App title never changes App Identity;
- one App does not receive a different App ID by region;
- localized content is length-limited and safety-filtered.

---

## 6. Description markup

v0.1 supports a restricted Markdown subset:

```text
paragraph
heading
bold / italic
ordered / unordered list
inline code
safe HTTPS link
```

Forbidden:

- arbitrary HTML;
- Script;
- iframe;
- autoplay media;
- external tracking pixels;
- CSS injection;
- Data URLs;
- automatic redirects;
- device-command links;
- launching external Apps without confirmation.

Market UI MUST use a safe renderer.

---

## 7. Categories

Recommended v0.1 top-level categories:

```text
reader
library
notes
writing
education
reference
rss-news
productivity
calendar
utilities
accessibility
communication
ai-tools
system-tools
other
```

Rules:

- one Primary Category per App;
- multiple Tags allowed;
- Category does not grant Permission;
- Category does not replace Capability declarations;
- new standard categories are versioned by Catalog Registry;
- third-party repositories MAY add display categories but SHOULD map them to standard top-level categories for cross-repository search.

---

## 8. Publisher display

Catalog SHOULD show:

```text
Publisher display name
short Publisher ID
verified domain (if any)
official Market verification (if any)
source repository (if any)
support URL
security contact
```

“Verified” must say what was verified:

```text
Domain verified
Publisher identity verified
Market review passed
Reproducible build verified
```

One vague checkmark MUST NOT imply all trust properties simultaneously.

---

## 9. Permission summary

Catalog MUST derive Permission summary from Release Record / Manifest, not accept arbitrary text that disagrees with real Permissions.

Display at least recognizable user-facing concepts such as:

```text
Network
Read library
Modify library
Read notes
Modify notes
Read user-selected files
Modify user-selected files
Bluetooth
Audio output
Frontlight control
Keep awake
```

Permissions may differ by Release.

Catalog SHOULD show:

- current Stable Permissions;
- Permission Diff relative to installed release;
- whether the App can run with a denied optional Permission when declared.

---

## 10. Capability / Compatibility summary

Catalog MAY display:

```text
Requires touch
Optional pen support
Supports physical page keys
Supports color enhancement
Requires network
Works offline
Fast-refresh enhanced
```

but truth comes from Release Record + device Capability Set.

App detail must distinguish:

```text
Latest overall release
Latest compatible release for this device
Installed release
```

If the newest release is incompatible, users should still see the newest compatible older release and the incompatibility reason.

---

## 11. Release Channel display

Catalog MAY display:

```text
Stable
Beta
Nightly
```

Stable is the default highlighted channel.

Beta/Nightly UI MUST show stability risk, automatic-update behavior, current Release Sequence, Permission Diff, potential Downgrade when returning Stable, and Data Schema risk.

Channels share one App Identity; they are not separate App entries unless a product UI has a clear presentation reason.

---

## 12. Catalog Index

Catalog Index provides fast App listing, not full detail.

Example entry:

```json
{
  "app_id": "com.example.reader",
  "publisher_id": "pub1_...",
  "record": {
    "path": "catalog/sha256/...json",
    "length": 3200,
    "sha256": "..."
  },
  "category": "reader",
  "title_sort_key": "example reader",
  "latest_stable_release_sequence": 142,
  "updated_at": "..."
}
```

Clients fetch individual App Records on demand. Low-memory devices SHOULD NOT load every description and screenshot at once.

---

## 13. Sharding

Large Repositories MAY shard by App ID hash prefix:

```text
catalog-00
catalog-01
...
catalog-ff
```

They MAY additionally publish:

```text
category indexes
recently-updated index
featured index
security-updates index
```

Every index is an ordinary verified Repository Target.

Sharding rules SHOULD be stable enough to avoid moving large portions of the Catalog on every update.

---

## 14. Catalog Diff

Catalog Diff reduces network cost for Kindle/low-bandwidth devices.

```json
{
  "type": "baga.catalog-diff",
  "format": "0.1",
  "repository_id": "repo1_...",
  "base_sequence": 619,
  "target_sequence": 620,
  "base_catalog_sha256": "...",
  "target_catalog_sha256": "...",
  "operations": [
    {"op": "upsert", "app_id": "...", "record": {}},
    {"op": "remove", "app_id": "..."}
  ]
}
```

Client accepts only when:

- local Sequence equals Base Sequence;
- Base Digest matches;
- Diff Target Digest verifies as a Repository Target;
- final complete Catalog Digest equals expected target after applying operations.

Failure falls back to complete Catalog download.

---

## 15. Assets

Icons/screenshots/media use content-addressed paths:

```text
assets/sha256/<digest>.<ext>
```

Asset Descriptor includes at least:

```text
length
sha256
media_type
width
height
purpose
```

Market SHOULD provide E-Paper-oriented variants:

```text
monochrome / grayscale icon
low-resolution screenshot
high-resolution screenshot
color original
```

Device selects according to Capability/network conditions. Same Digest MUST NOT be replaced by different bytes.

---

## 16. E-Paper Catalog UI

Device Market UI SHOULD:

- prefer paging;
- avoid infinite continuous-scroll animation;
- use Dirty Regions for list updates;
- keep icons legible in grayscale;
- not rely on color alone for review/risk state;
- support physical-key/focus navigation;
- download screenshots on demand;
- not autoplay carousels on list pages;
- refresh download/install progress at low frequency;
- retain last verified Catalog for offline browsing.

Catalog expiration MUST NOT stop installed Apps from launching.

---

## 17. Search

### 17.1 Local search

Search verified local Catalog fields:

```text
title
summary
publisher
tags
category
```

This supports offline/privacy-preserving discovery.

### 17.2 Remote search

A remote Search API MAY provide better ranking/fuzzy search, but its result is advisory:

```text
Search result
      │
      ▼
Resolve app_id to signed Catalog / Release Record
      │
      ▼
Verify before install
```

Search servers MUST NOT return an arbitrary unprotected IKP URL and instruct the device to install it directly.

---

## 18. Search privacy

Market SHOULD minimize binding search queries to device identity.

Principles:

- no hardware serial required;
- no complete installed-App inventory required;
- Compatibility Filtering can be local;
- remote search MAY receive only Locale, standardized Capability Profile, and Query;
- Analytics requires separate authorization;
- LifeBook user account is not a prerequisite for Market search;
- log retention/use should be public.

---

## 19. Ranking and recommendation

Ranking/recommendation is Market Product Policy, not security protocol.

Transparency rules:

- paid promotion clearly labeled;
- ads MUST NOT impersonate system updates;
- official Apps MUST NOT receive fabricated ratings;
- ranking does not change App Identity;
- recommendation cannot bypass Compatibility;
- Security Revoked Releases cannot continue installation because of recommendation;
- recommendation SHOULD NOT require upload of user's book/note contents.

Possible discovery labels:

```text
Featured
Popular
Recently updated
Open source
Offline capable
Made for physical keys
Pen optimized
Kindle compatible
Android E-Paper compatible
```

Labels need verifiable provenance or must be clearly editorial.

---

## 20. Review / security labels

Standard display labels MAY include:

```text
Baga Ink Universal
Baga Ink Market Reviewed
Publisher Domain Verified
Open Source Declared
Reproducible Build Verified
Experimental
Unlisted
Withdrawn
Security Warning
```

Each label points to one of:

- Review Attestation;
- Compatibility Test;
- Publisher Verification;
- Build Attestation;
- Release Status Record.

Third-party Repositories cannot self-assign the official Market review label.

---

## 21. Offline Catalog

Portable Repository Snapshot MAY include:

```text
Catalog Root
Catalog Index / selected shards
selected App Records
icons
low-resolution screenshots
Release Records
IKP packages
```

An offline Market can browse/search the carried Catalog, show Permission/Compatibility, and install verified IKPs contained in the Snapshot.

Missing screenshots do not affect secure installation.

---

## 22. Third-party Repositories

A third-party Repository MAY have its own Catalog, category mapping, featured lists, review policy, and localization.

It MUST:

- display Repository Identity;
- not forge official review status;
- reference real Publisher Identity;
- distribute packages through standard IKP Signature verification;
- preserve Release immutability;
- distinguish App ID conflicts by Publisher Identity;
- display source Repository in search results.

A cross-repository aggregation UI SHOULD show:

```text
App name
Publisher
Repository source
Review status
```

---

## 23. Catalog update atomicity

Update flow:

1. verify new Repository Metadata;
2. fetch Catalog Root;
3. fetch full Index or applicable Diff;
4. verify Target Digest;
5. construct new local Catalog in staging;
6. verify final Catalog Digest;
7. atomically switch Catalog pointer;
8. keep old Catalog until new one is complete.

After power loss, recover to either complete old or complete new Catalog, never a mixed state.

---

## 24. Resource limits

Client MUST limit at least:

```text
Catalog Root size
Index size
Shard count
App Record size
Locale count
Description length
Tag count
Screenshot count
Asset size
Markdown nesting
Diff operation count
Search result count
```

Oversized descriptions/assets MUST NOT make low-memory devices lose core Market functionality.

---

## 25. Final boundary between Catalog and installation

On Install click, resolve and re-validate:

```text
app_id
publisher_id
selected release
release_sequence
package digest
permission diff
capability requirements
release status
```

These values come from security Release Records / Repository Metadata.

Catalog Cache display objects MUST NOT be passed to Package Installer as already-verified security fields.

---

## 26. Final rule

> **Catalog can be redesigned, re-ranked, and re-localized; App Identity, Release Digest, Permission, and Update Chain cannot change because Catalog presentation changed.**
