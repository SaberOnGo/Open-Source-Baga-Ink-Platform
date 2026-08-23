#!/usr/bin/env python3
"""Create compliant Platform Port Task Design / Execution Prompt scaffolding.

Examples:

  python3 tools/new_platform_port_task.py task \
      kindle 0010 适配器契约可执行化 Executable-Adapter-Contract

  python3 tools/new_platform_port_task.py version \
      kindle 0010_适配器契约可执行化_Executable-Adapter-Contract v002

  python3 tools/new_platform_port_task.py execution \
      kindle 0010_适配器契约可执行化_Executable-Adapter-Contract v001

  python3 tools/new_platform_port_task.py prompt \
      kindle 0010_适配器契约可执行化_Executable-Adapter-Contract v001 \
      0010 建立IDL模式与加载器 Create-IDL-Schema-and-Loader

This script never overwrites an existing task/version/prompt. It invokes
`tools/check_platform_port_plans.py` after each successful operation.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import NoReturn

REPO_ROOT = Path(__file__).resolve().parents[1]
BASE = REPO_ROOT / "docs" / "plans" / "platform-ports"
CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
EN_PATTERN = r"[A-Za-z0-9]+(?:[-.][A-Za-z0-9]+)*"
EN_RE = re.compile(rf"^{EN_PATTERN}$")
TASK_DIR_RE = re.compile(
    rf"^(?P<number>\d{{4}})_(?P<zh>[^_]+)_(?P<en>{EN_PATTERN})$"
)
VERSION_RE = re.compile(r"^v\d{3}$")
NUMBER_RE = re.compile(r"^\d{4}$")
CURRENT_VERSION_RE = re.compile(r"(?m)^(> \*\*Current Selected Version:\*\* `)v\d{3}(`\s*)$")

TASK_INDEX = "0000_任务版本索引_Task-Version-Index.md"
TASK_OVERVIEW = "0000_任务设计总纲_Task-Design-Overview.md"
EXEC_INDEX = "0000_执行索引_Execution-Index.md"


def die(message: str) -> NoReturn:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(2)


def validate_number(value: str, *, allow_zero: bool = False) -> str:
    if not NUMBER_RE.fullmatch(value):
        die("number must be exactly four digits, e.g. 0010")
    if not allow_zero and value == "0000":
        die("0000 is reserved for index/overview documents")
    return value


def validate_zh(value: str) -> str:
    if "_" in value or "/" in value or "\\" in value:
        die("Chinese name must not contain '_', '/' or '\\'")
    if any(ch.isspace() for ch in value):
        die("Chinese name must not contain whitespace")
    if not CJK_RE.search(value):
        die("Chinese name must contain at least one Chinese character")
    return value


def validate_en(value: str) -> str:
    if not EN_RE.fullmatch(value):
        die("English name must use ASCII letters/numbers separated only by '-' or '.', with no spaces/underscores")
    return value


def validate_version(value: str) -> str:
    if not VERSION_RE.fullmatch(value):
        die("version must match vNNN, e.g. v001 or v010")
    return value


def platform_root(platform: str) -> Path:
    root = BASE / platform
    if not root.is_dir():
        die(f"platform directory does not exist: {root.relative_to(REPO_ROOT)}")
    for required in (root / "task", root / "execution-prompts"):
        if not required.is_dir():
            die(f"required directory missing: {required.relative_to(REPO_ROOT)}")
    return root


def task_root_from_name(platform: str, task_name: str) -> Path:
    match = TASK_DIR_RE.fullmatch(task_name)
    if not match:
        die("task directory must match NNNN_<中文任务名>_<English-Task-Name>")
    if match.group("number") == "0000":
        die("0000 is reserved and cannot be used as a Task ID")
    if not CJK_RE.search(match.group("zh")):
        die("task directory Chinese-name segment must contain Chinese characters")
    return platform_root(platform) / "task" / task_name


def write_new(path: Path, content: str) -> None:
    if path.exists():
        die(f"refusing to overwrite existing path: {path.relative_to(REPO_ROOT)}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"created {path.relative_to(REPO_ROOT)}")


def make_task_name(number: str, zh: str, en: str) -> str:
    validate_number(number)
    validate_zh(zh)
    validate_en(en)
    return f"{number}_{zh}_{en}"


def task_index_content(task_name: str, version: str) -> str:
    return f"""# 任务版本索引 / Task Version Index

> **Task:** `{task_name}`  
> **Current Selected Version:** `{version}`  
> **Status:** Draft

---

## Version History

- `{version}` — Initial Task Design.

## Governing Sources

- `docs/plans/platform-ports/0000_平台移植计划目录与文件命名规则_Baga-Ink-Platform-Port-Plan-Naming.md`
- platform-specific Standards / Design / Architecture Freeze as applicable

## Rule

When the Task Design changes materially, create a new `vNNN` directory. Do not overwrite historical versions.
"""


def task_overview_content(task_name: str, version: str) -> str:
    return f"""# 任务设计总纲 / Task Design Overview

> **Task:** `{task_name}`  
> **Version:** `{version}`  
> **Status:** Draft

---

## Goal

TBD

## Background / Problem

TBD

## Authority / Inputs

TBD

## Scope

TBD

## Out of Scope

TBD

## Dependencies / Preconditions

TBD

## Implementation Design

TBD

## Files / Modules Involved

TBD

## Test Strategy

TBD

## Debug Strategy

TBD

## Real-device Operations

TBD / Not required

## Data Protection / Rollback

TBD

## Acceptance Gate

TBD

## Known Risks

TBD

## Open Questions

TBD

## Expected Execution-Prompt Groups

TBD
"""


def execution_index_content(platform: str, task_name: str, version: str) -> str:
    source = f"docs/plans/platform-ports/{platform}/task/{task_name}/{version}/"
    return f"""# 执行索引 / Execution Index

> **Task:** `{task_name}`  
> **Source Task Version:** `{version}`  
> **Status:** Draft

---

## Source

`{source}`

## Execution Goal

TBD

## Prompt Order / Dependencies

TBD

## Parallelizable Steps

TBD

## Real-device Steps

TBD / None

## Final Gate

TBD
"""


def prompt_content(task_name: str, version: str, number: str, zh: str, en: str, platform: str) -> str:
    source = f"docs/plans/platform-ports/{platform}/task/{task_name}/{version}/"
    return f"""# {zh} / {en.replace('-', ' ').replace('.', ' ')}

> **Task:** `{task_name}`  
> **Source Task:** `{source}`  
> **Source Task Version:** `{version}`  
> **Prompt ID:** `PROMPT-{number}`  
> **Status:** Pending

---

## Goal

TBD

## Dependencies / Preconditions

TBD

## Files / Components

TBD

## Device Requirements

TBD / None

## Execution Steps

TBD

## Tests / Verification

TBD

## Acceptance

TBD

## Result / Evidence

Pending execution.
"""


def cmd_task(args: argparse.Namespace) -> None:
    root = platform_root(args.platform)
    task_name = make_task_name(args.number, args.zh, args.en)
    version = validate_version(args.version)
    task_root = root / "task" / task_name
    if task_root.exists():
        die(f"task already exists: {task_root.relative_to(REPO_ROOT)}")

    write_new(task_root / TASK_INDEX, task_index_content(task_name, version))
    write_new(task_root / version / TASK_OVERVIEW, task_overview_content(task_name, version))


def cmd_version(args: argparse.Namespace) -> None:
    task_root = task_root_from_name(args.platform, args.task_name)
    if not task_root.is_dir():
        die(f"task does not exist: {task_root.relative_to(REPO_ROOT)}")

    index = task_root / TASK_INDEX
    if not index.is_file():
        die(f"task index missing: {index.relative_to(REPO_ROOT)}")

    version = validate_version(args.version)
    version_dir = task_root / version
    if version_dir.exists():
        die(f"Task Design version already exists: {version_dir.relative_to(REPO_ROOT)}")

    write_new(version_dir / TASK_OVERVIEW, task_overview_content(args.task_name, version))

    existing = index.read_text(encoding="utf-8")
    if f"`{version}`" in existing:
        die(f"version {version} is already recorded in the task index")

    existing, replacements = CURRENT_VERSION_RE.subn(rf"\g<1>{version}\g<2>", existing, count=1)
    if replacements != 1:
        die("task index does not contain a valid Current Selected Version line")

    marker = "## Governing Sources"
    addition = f"- `{version}` — New Task Design version.\n\n"
    if marker in existing:
        existing = existing.replace(marker, addition + marker, 1)
    else:
        existing += "\n" + addition
    index.write_text(existing, encoding="utf-8")
    print(f"updated {index.relative_to(REPO_ROOT)}")


def cmd_execution(args: argparse.Namespace) -> None:
    root = platform_root(args.platform)
    task_root = task_root_from_name(args.platform, args.task_name)
    version = validate_version(args.version)
    source = task_root / version / TASK_OVERVIEW
    if not source.is_file():
        die(f"source Task Design version does not exist: {source.relative_to(REPO_ROOT)}")

    exec_dir = root / "execution-prompts" / args.task_name / version
    write_new(exec_dir / EXEC_INDEX, execution_index_content(args.platform, args.task_name, version))


def cmd_prompt(args: argparse.Namespace) -> None:
    root = platform_root(args.platform)
    task_root = task_root_from_name(args.platform, args.task_name)
    version = validate_version(args.version)
    number = validate_number(args.number)
    zh = validate_zh(args.zh)
    en = validate_en(args.en)

    source = task_root / version / TASK_OVERVIEW
    if not source.is_file():
        die(f"source Task Design version does not exist: {source.relative_to(REPO_ROOT)}")

    exec_dir = root / "execution-prompts" / args.task_name / version
    if not (exec_dir / EXEC_INDEX).is_file():
        die("execution version/index does not exist; run the 'execution' subcommand first")

    filename = f"{number}_{zh}_{en}.md"
    write_new(exec_dir / filename, prompt_content(args.task_name, version, number, zh, en, args.platform))


def run_guard() -> None:
    subprocess.run(
        [sys.executable, str(REPO_ROOT / "tools" / "check_platform_port_plans.py")],
        cwd=REPO_ROOT,
        check=True,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    task = sub.add_parser("task", help="create a new Task with its initial Task Design version")
    task.add_argument("platform")
    task.add_argument("number")
    task.add_argument("zh")
    task.add_argument("en")
    task.add_argument("--version", default="v001")
    task.set_defaults(func=cmd_task)

    version = sub.add_parser("version", help="add a new Task Design version to an existing Task")
    version.add_argument("platform")
    version.add_argument("task_name")
    version.add_argument("version")
    version.set_defaults(func=cmd_version)

    execution = sub.add_parser("execution", help="create the mirrored execution version/index")
    execution.add_argument("platform")
    execution.add_argument("task_name")
    execution.add_argument("version")
    execution.set_defaults(func=cmd_execution)

    prompt = sub.add_parser("prompt", help="create one numbered bilingual execution prompt")
    prompt.add_argument("platform")
    prompt.add_argument("task_name")
    prompt.add_argument("version")
    prompt.add_argument("number")
    prompt.add_argument("zh")
    prompt.add_argument("en")
    prompt.set_defaults(func=cmd_prompt)

    return parser


def main() -> int:
    args = build_parser().parse_args()
    args.func(args)
    run_guard()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
