#!/usr/bin/env python3
"""Validate docs/plans/platform-ports structure and naming.

This guard prevents humans or AI agents from creating ad-hoc task folders,
ambiguous version folders, invalid bilingual file names, or execution prompts
that cannot be traced to an approved Task Design version.

Run from anywhere inside the repository:

    python3 tools/check_platform_port_plans.py

The script uses only the Python standard library and exits non-zero on any
violation so it can be used locally and in GitHub Actions.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
BASE = REPO_ROOT / "docs" / "plans" / "platform-ports"

EN_PATTERN = r"[A-Za-z0-9]+(?:[-.][A-Za-z0-9]+)*"
MARKDOWN_RE = re.compile(
    rf"^(?P<number>\d{{4}})_(?P<zh>[^_]+)_(?P<en>{EN_PATTERN})\.md$"
)
TASK_DIR_RE = re.compile(
    rf"^(?P<number>\d{{4}})_(?P<zh>[^_]+)_(?P<en>{EN_PATTERN})$"
)
VERSION_RE = re.compile(r"^v\d{3}$")
PLATFORM_DIR_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")

ALLOWED_PLATFORM_SUBDIRS = {"task", "execution-prompts"}

TASK_VERSION_INDEX = "0000_任务版本索引_Task-Version-Index.md"
TASK_DESIGN_OVERVIEW = "0000_任务设计总纲_Task-Design-Overview.md"
EXECUTION_INDEX = "0000_执行索引_Execution-Index.md"

errors: list[str] = []


def fail(path: Path, message: str) -> None:
    try:
        rel = path.relative_to(REPO_ROOT)
    except ValueError:
        rel = path
    errors.append(f"{rel}: {message}")


def has_whitespace(name: str) -> bool:
    return any(ch.isspace() for ch in name)


def validate_bilingual_markdown(path: Path) -> None:
    name = path.name
    if has_whitespace(name):
        fail(path, "file name must not contain whitespace")
        return

    match = MARKDOWN_RE.fullmatch(name)
    if not match:
        fail(
            path,
            "Markdown file name must match 'NNNN_<中文名>_<English-Name>.md'",
        )
        return

    if not CJK_RE.search(match.group("zh")):
        fail(path, "the Chinese-name segment must contain at least one Chinese character")


def validate_task_dir_name(path: Path) -> bool:
    name = path.name
    if has_whitespace(name):
        fail(path, "task directory name must not contain whitespace")
        return False

    match = TASK_DIR_RE.fullmatch(name)
    if not match:
        fail(
            path,
            "task directory must match 'NNNN_<中文任务名>_<English-Task-Name>'",
        )
        return False

    if match.group("number") == "0000":
        fail(path, "0000 is reserved for directory/index documents, not a task directory")

    if not CJK_RE.search(match.group("zh")):
        fail(path, "task directory Chinese-name segment must contain Chinese characters")
    return True


def validate_task_tree(platform_dir: Path) -> dict[str, set[str]]:
    task_root = platform_dir / "task"
    task_versions: dict[str, set[str]] = {}
    if not task_root.exists():
        fail(task_root, "required directory is missing")
        return task_versions

    for entry in task_root.iterdir():
        if entry.is_file():
            if entry.suffix != ".md":
                fail(entry, "only Markdown files are allowed directly under task/")
            else:
                validate_bilingual_markdown(entry)
            continue

        if not entry.is_dir():
            fail(entry, "unsupported filesystem entry")
            continue

        if not validate_task_dir_name(entry):
            continue

        version_index = entry / TASK_VERSION_INDEX
        if not version_index.is_file():
            fail(version_index, f"every task directory must contain {TASK_VERSION_INDEX}")

        versions: set[str] = set()
        for child in entry.iterdir():
            if child.is_file():
                if child.suffix != ".md":
                    fail(child, "only Markdown files are allowed in a task root")
                else:
                    validate_bilingual_markdown(child)
                continue

            if not child.is_dir():
                fail(child, "unsupported filesystem entry")
                continue

            if not VERSION_RE.fullmatch(child.name):
                fail(child, "Task Design version directory must match vNNN, e.g. v001")
                continue

            versions.add(child.name)
            overview = child / TASK_DESIGN_OVERVIEW
            if not overview.is_file():
                fail(overview, f"every Task Design version must contain {TASK_DESIGN_OVERVIEW}")

            for item in child.iterdir():
                if item.is_dir():
                    fail(item, "Task Design version directories may not contain ad-hoc subdirectories")
                elif item.is_file():
                    if item.suffix != ".md":
                        fail(item, "only Markdown files are allowed in a Task Design version")
                    else:
                        validate_bilingual_markdown(item)

        if not versions:
            fail(entry, "task directory must contain at least one vNNN Task Design version")
        task_versions[entry.name] = versions

    return task_versions


def validate_execution_tree(platform_dir: Path, task_versions: dict[str, set[str]]) -> None:
    exec_root = platform_dir / "execution-prompts"
    if not exec_root.exists():
        fail(exec_root, "required directory is missing")
        return

    for entry in exec_root.iterdir():
        if entry.is_file():
            if entry.suffix != ".md":
                fail(entry, "only Markdown files are allowed directly under execution-prompts/")
            else:
                validate_bilingual_markdown(entry)
            continue

        if not entry.is_dir():
            fail(entry, "unsupported filesystem entry")
            continue

        if not validate_task_dir_name(entry):
            continue

        if entry.name not in task_versions:
            fail(entry, "execution prompt task has no exact mirror under ../task/")
            source_versions: set[str] = set()
        else:
            source_versions = task_versions[entry.name]

        for child in entry.iterdir():
            if not child.is_dir():
                fail(child, "execution task directory may contain only vNNN directories")
                continue

            if not VERSION_RE.fullmatch(child.name):
                fail(child, "Execution Prompt version directory must match vNNN, e.g. v001")
                continue

            if child.name not in source_versions:
                fail(child, "execution prompt version has no exact Task Design version mirror")

            index = child / EXECUTION_INDEX
            if not index.is_file():
                fail(index, f"every execution version must contain {EXECUTION_INDEX}")

            for item in child.iterdir():
                if item.is_dir():
                    fail(item, "execution prompt version directories may not contain ad-hoc subdirectories")
                elif item.is_file():
                    if item.suffix != ".md":
                        fail(item, "only Markdown files are allowed in execution prompt versions")
                    else:
                        validate_bilingual_markdown(item)


def validate_platform(platform_dir: Path) -> None:
    if not PLATFORM_DIR_RE.fullmatch(platform_dir.name):
        fail(platform_dir, "platform directory must be lowercase kebab-case, e.g. kindle or android-e-paper")

    for entry in platform_dir.iterdir():
        if entry.is_file():
            if entry.suffix != ".md":
                fail(entry, "only Markdown files are allowed at a platform plan root")
            else:
                validate_bilingual_markdown(entry)
        elif entry.is_dir() and entry.name not in ALLOWED_PLATFORM_SUBDIRS:
            fail(
                entry,
                "unexpected platform-plan directory; only task/ and execution-prompts/ are allowed",
            )

    task_versions = validate_task_tree(platform_dir)
    validate_execution_tree(platform_dir, task_versions)


def main() -> int:
    if not BASE.is_dir():
        print(f"ERROR: missing {BASE.relative_to(REPO_ROOT)}", file=sys.stderr)
        return 2

    for entry in BASE.iterdir():
        if entry.is_file():
            if entry.suffix != ".md":
                fail(entry, "only Markdown files are allowed directly under platform-ports/")
            else:
                validate_bilingual_markdown(entry)
        elif entry.is_dir():
            validate_platform(entry)

    if errors:
        print("Platform-port plan structure check FAILED:\n", file=sys.stderr)
        for error in errors:
            print(f" - {error}", file=sys.stderr)
        print(
            "\nRequired workflow: Master Plan -> task/<NNNN_中文_English>/vNNN -> "
            "execution-prompts/<same-task>/vNNN.",
            file=sys.stderr,
        )
        return 1

    print("Platform-port plan structure check PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
