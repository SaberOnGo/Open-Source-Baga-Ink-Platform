#!/usr/bin/env python3
"""Validate Baga Ink repository licensing architecture.

This is a structural/governance guard, not a legal-opinion engine. It protects
intentional repository facts from accidental drift: the default PolyForm text,
localized licensing policy, historical cutover, README presentation, LifeBook
public-source boundary, OEM Enablement model, private-business-document
boundary, and third-party license separation.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EXPECTED_POLYFORM_SHA256 = "c0ea4a896d2c8c394b29f9427589996db826cd501c512279ff0ed3ef48fabbe5"

REQUIRED_FILES = [
    "LICENSE",
    "NOTICE",
    "LICENSE_HISTORY.md",
    "COMMERCIAL_LICENSE.md",
    "COMMERCIAL_LICENSE.zh-CN.md",
    "THIRD_PARTY_NOTICES.md",
    ".gitignore",
    "docs/en/governance/02_baga-ink-licensing-policy.md",
    "docs/zh-CN/governance/02_Baga-Ink授权策略.md",
]


def fail(message: str) -> None:
    raise SystemExit(f"[licensing-guard] ERROR: {message}")


def read(path: str) -> str:
    p = ROOT / path
    if not p.is_file():
        fail(f"required file missing: {path}")
    return p.read_text(encoding="utf-8")


def main() -> None:
    for path in REQUIRED_FILES:
        if not (ROOT / path).is_file():
            fail(f"required file missing: {path}")

    license_bytes = (ROOT / "LICENSE").read_bytes()
    digest = hashlib.sha256(license_bytes).hexdigest()
    if digest != EXPECTED_POLYFORM_SHA256:
        fail(
            "root LICENSE must remain the unmodified PolyForm Noncommercial "
            f"License 1.0.0 text (expected sha256 {EXPECTED_POLYFORM_SHA256}, got {digest})"
        )

    notice = read("NOTICE")
    if "Required Notice:" not in notice:
        fail("NOTICE must contain a PolyForm Required Notice line")
    if "COMMERCIAL_LICENSE.md" not in notice or "LICENSE_HISTORY.md" not in notice:
        fail("NOTICE must point to commercial licensing and license history")

    third_party = read("THIRD_PARTY_NOTICES.md")
    if "Baga Ink's original project material is licensed under the Apache License 2.0" in third_party:
        fail("THIRD_PARTY_NOTICES.md still claims Apache-2.0 is the current Baga default")
    for required in ["Commercial License", "AGPL", "GPL", "LICENSE_HISTORY.md"]:
        if required not in third_party:
            fail(f"THIRD_PARTY_NOTICES.md missing required boundary text: {required}")

    readme = read("README.md")
    readme_zh = read("README.zh-CN.md")
    for name, text in [("README.md", readme), ("README.zh-CN.md", readme_zh)]:
        if "License-Apache--2.0" in text or "License: Apache-2.0" in text:
            fail(f"{name} must not show the obsolete Apache license badge")
        if "COMMERCIAL_LICENSE" not in text:
            fail(f"{name} must link the commercial licensing entry point in its later Licensing section")
        if "LICENSE_HISTORY.md" not in text:
            fail(f"{name} must link license history")
        if "LifeBook" not in text or ("Proprietary" not in text and "proprietary" not in text):
            fail(f"{name} must preserve the proprietary LifeBook boundary")

    # Commercial licensing should be documented, but not promoted in the README hero.
    first_50_en = "\n".join(readme.splitlines()[:50])
    first_50_zh = "\n".join(readme_zh.splitlines()[:50])
    for name, text in [("README.md", first_50_en), ("README.zh-CN.md", first_50_zh)]:
        if "COMMERCIAL_LICENSE" in text or "Commercial License" in text or "商业授权" in text:
            fail(f"{name} promotes commercial licensing too prominently in the first 50 lines")

    en_policy = read("docs/en/governance/02_baga-ink-licensing-policy.md")
    zh_policy = read("docs/zh-CN/governance/02_Baga-Ink授权策略.md")
    commercial = read("COMMERCIAL_LICENSE.md")
    commercial_zh = read("COMMERCIAL_LICENSE.zh-CN.md")

    for required in ["OEM Enablement Program", "no-fee", "Baga Ink Client", "proprietary"]:
        if required not in en_policy:
            fail(f"English licensing policy missing OEM/control-plane boundary: {required}")
    for required in ["OEM Enablement Program", "零费用", "Baga Ink Client", "Proprietary"]:
        if required not in zh_policy:
            fail(f"zh-CN licensing policy missing OEM/control-plane boundary: {required}")
    for required in ["OEM Enablement Program", "$0", "official Baga Ink Client"]:
        if required not in commercial:
            fail(f"COMMERCIAL_LICENSE.md missing OEM Enablement term: {required}")
    for required in ["OEM Enablement Program", "零费用", "Baga Ink Client"]:
        if required not in commercial_zh:
            fail(f"COMMERCIAL_LICENSE.zh-CN.md missing OEM Enablement term: {required}")

    catalog = json.loads(read("docs/localization/catalog.json"))
    matches = [d for d in catalog.get("documents", []) if d.get("id") == "governance.licensing.02"]
    if len(matches) != 1:
        fail("localization catalog must contain exactly one governance.licensing.02 entry")
    entry = matches[0]
    expected = {
        "category": "governance",
        "number": "02",
        "zh_cn_path": "docs/zh-CN/governance/02_Baga-Ink授权策略.md",
        "en_path": "docs/en/governance/02_baga-ink-licensing-policy.md",
        "status": "current",
    }
    for key, value in expected.items():
        if entry.get(key) != value:
            fail(f"catalog governance.licensing.02 has wrong {key}: {entry.get(key)!r}")

    history = read("LICENSE_HISTORY.md")
    if "3517970a221dd2e40d8931e1f68399032c343789" not in history:
        fail("LICENSE_HISTORY.md must preserve the pre-cutover main commit")
    if "Apache-2.0" not in history or "PolyForm" not in history:
        fail("LICENSE_HISTORY.md must explain both historical Apache and current PolyForm defaults")

    # The production LifeBook app is intentionally not public source in this repository.
    forbidden_lifebook_source_roots = [
        ROOT / "apps" / "lifebook",
        ROOT / "platform" / "lifebook",
        ROOT / "lifebook-src",
    ]
    for path in forbidden_lifebook_source_roots:
        if path.exists():
            fail(
                f"production LifeBook source path is public ({path.relative_to(ROOT)}); "
                "publish only with an explicit architecture/licensing decision"
            )

    # Confidential business/monetization strategy belongs only in a local ignored
    # directory or a separate private repository. The public checkout must never
    # contain a tracked private/ tree.
    gitignore = read(".gitignore")
    if "/private/" not in gitignore:
        fail(".gitignore must ignore the root /private/ directory for confidential local strategy docs")
    if (ROOT / "private").exists():
        fail("private/ content is present in the tracked checkout; confidential strategy must not be committed")

    print("[licensing-guard] OK")


if __name__ == "__main__":
    main()
