#!/usr/bin/env python3
"""Validate docs/plans/platform-ports task-package structure.

Platform implementation work uses self-contained, flat, versioned task packages
that can be read from top to bottom without chasing per-subtask version trees.

Expected shape:

    docs/plans/platform-ports/<platform>/
    ├── NNNN_中文名_English-Name.md
    └── task/
        └── YYYY-MM-DD_<slug>/
            └── vN/
                └── vN.M/
                    ├── 00_vN.M_....md
                    ├── 01_vN.M_....md
                    └── ...

Run from anywhere inside the repository:

    python3 tools/check_platform_port_plans.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
BASE = REPO_ROOT / "docs" / "plans" / "platform-ports"

EN_PATTERN = r"[A-Za-z0-9]+(?:[-.][A-Za-z0-9]+)*"
ROOT_MARKDOWN_RE = re.compile(
    rf"^(?P<number>\d{{4}})_(?P<zh>[^_]+)_(?P<en>{EN_PATTERN})\.md$"
)
PLATFORM_DIR_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
PACKAGE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}_[a-z0-9][a-z0-9-]*$")
MAJOR_RE = re.compile(r"^v(?P<major>\d+)$")
VERSION_RE = re.compile(r"^v(?P<major>\d+)\.(?P<minor>\d+)$")
TASK_FILE_RE = re.compile(r"^(?P<number>\d{2})_(?P<version>v\d+\.\d+)_(?P<title>.+)\.md$")
CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")

errors: list[str] = []


def fail(path: Path, message: str) -> None:
    try:
        rel = path.relative_to(REPO_ROOT)
    except ValueError:
        rel = path
    errors.append(f"{rel}: {message}")


def has_whitespace(name: str) -> bool:
    return any(ch.isspace() for ch in name)


def validate_root_markdown(path: Path) -> None:
    if has_whitespace(path.name):
        fail(path, "platform-plan root Markdown names must not contain whitespace")
        return
    match = ROOT_MARKDOWN_RE.fullmatch(path.name)
    if not match:
        fail(path, "platform-plan root Markdown must match NNNN_<中文名>_<English-Name>.md")
        return
    if not CJK_RE.search(match.group("zh")):
        fail(path, "the Chinese-name segment must contain Chinese characters")


def validate_leaf(version_dir: Path, expected_version: str) -> None:
    files = sorted(version_dir.iterdir())
    if not files:
        fail(version_dir, "task-package version must contain numbered Markdown documents")
        return

    numbers: set[str] = set()
    has_control = False
    for item in files:
        if item.is_dir():
            fail(item, "task-package version must be flat; nested subdirectories are not allowed")
            continue
        if item.suffix != ".md":
            fail(item, "only Markdown files are allowed in a task-package version")
            continue
        if has_whitespace(item.name):
            fail(item, "task-package Markdown names must not contain whitespace")
            continue
        match = TASK_FILE_RE.fullmatch(item.name)
        if not match:
            fail(item, "task-package file must match NN_vN.M_<title>.md")
            continue
        if match.group("version") != expected_version:
            fail(item, f"filename version must match containing directory {expected_version}")
        number = match.group("number")
        if number in numbers:
            fail(item, f"duplicate document number {number} in task package")
        numbers.add(number)
        if number == "00":
            has_control = True

    if not has_control:
        fail(version_dir, "task-package version must contain a 00_vN.M_* control document")


def validate_package(package_dir: Path) -> None:
    if not PACKAGE_RE.fullmatch(package_dir.name):
        fail(package_dir, "task package must match YYYY-MM-DD_<lowercase-kebab-slug>")
        return

    for entry in package_dir.iterdir():
        if not entry.is_dir():
            fail(entry, "task-package root may contain only vN major-version directories")
            continue
        major_match = MAJOR_RE.fullmatch(entry.name)
        if not major_match:
            fail(entry, "major task directory must match vN, e.g. v1 or v16")
            continue
        major = major_match.group("major")
        found_leaf = False
        for child in entry.iterdir():
            if not child.is_dir():
                fail(child, "major version directory may contain only vN.M directories")
                continue
            version_match = VERSION_RE.fullmatch(child.name)
            if not version_match:
                fail(child, "task-package version directory must match vN.M, e.g. v1.1")
                continue
            if version_match.group("major") != major:
                fail(child, f"version {child.name} must be under matching major directory v{version_match.group('major')}")
            found_leaf = True
            validate_leaf(child, child.name)
        if not found_leaf:
            fail(entry, "major task directory must contain at least one vN.M version")


def validate_platform(platform_dir: Path) -> None:
    if not PLATFORM_DIR_RE.fullmatch(platform_dir.name):
        fail(platform_dir, "platform directory must be lowercase kebab-case")

    task_root = platform_dir / "task"
    if not task_root.is_dir():
        fail(task_root, "required task/ directory is missing")

    for entry in platform_dir.iterdir():
        if entry.is_file():
            if entry.suffix != ".md":
                fail(entry, "only Markdown files are allowed at a platform-plan root")
            else:
                validate_root_markdown(entry)
        elif entry.is_dir() and entry.name != "task":
            fail(entry, "unexpected directory; platform-plan roots use only task/")

    if task_root.is_dir():
        for entry in task_root.iterdir():
            if not entry.is_dir():
                fail(entry, "task/ may contain only dated task-package directories")
            else:
                validate_package(entry)


def main() -> int:
    if not BASE.is_dir():
        print(f"ERROR: missing {BASE.relative_to(REPO_ROOT)}", file=sys.stderr)
        return 2

    for entry in BASE.iterdir():
        if entry.is_file():
            if entry.suffix != ".md":
                fail(entry, "only Markdown files are allowed directly under platform-ports/")
            else:
                validate_root_markdown(entry)
        elif entry.is_dir():
            validate_platform(entry)

    if errors:
        print("Platform-port plan structure check FAILED:\n", file=sys.stderr)
        for error in errors:
            print(f" - {error}", file=sys.stderr)
        print(
            "\nRequired workflow: platform master plan -> task/YYYY-MM-DD_<slug>/vN/vN.M/ "
            "-> flat numbered task documents.",
            file=sys.stderr,
        )
        return 1

    print("Platform-port plan structure check PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
