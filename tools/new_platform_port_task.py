#!/usr/bin/env python3
"""Create a flat, versioned Platform Port task package.

Example:

    python3 tools/new_platform_port_task.py \
        kindle 2026-08-24 kindle-platform v1 v1.1

The generated package follows the same browse-first pattern used by mature
LifeBook task packages: one version directory, flat numbered documents, and a
single reading order. This script never overwrites an existing package.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
BASE = REPO_ROOT / "docs" / "plans" / "platform-ports"
PLATFORM_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
MAJOR_RE = re.compile(r"^v(?P<major>\d+)$")
VERSION_RE = re.compile(r"^v(?P<major>\d+)\.(?P<minor>\d+)$")


def die(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(2)


def write_new(path: Path, content: str) -> None:
    if path.exists():
        die(f"refusing to overwrite existing path: {path.relative_to(REPO_ROOT)}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"created {path.relative_to(REPO_ROOT)}")


def validate(args: argparse.Namespace) -> Path:
    if not PLATFORM_RE.fullmatch(args.platform):
        die("platform must be lowercase kebab-case")
    if not DATE_RE.fullmatch(args.date):
        die("date must be YYYY-MM-DD")
    if not SLUG_RE.fullmatch(args.slug):
        die("slug must be lowercase kebab-case")
    major = MAJOR_RE.fullmatch(args.major)
    version = VERSION_RE.fullmatch(args.version)
    if not major:
        die("major must match vN, e.g. v1")
    if not version:
        die("version must match vN.M, e.g. v1.1")
    if major.group("major") != version.group("major"):
        die("major and version must use the same major number")

    platform = BASE / args.platform
    task_root = platform / "task"
    if not task_root.is_dir():
        die(f"missing task directory: {task_root.relative_to(REPO_ROOT)}")
    return task_root / f"{args.date}_{args.slug}" / args.major / args.version


def control(version: str) -> str:
    return f"""# {version} 总控：范围边界与执行纪律

**状态**: Draft  
**任务定位**: 本目录是一份自包含 Platform Port 实现任务包。  
**执行方式**: 按编号阅读并按 Batch 推进；不得另建平行 Task Design 或 Execution Prompt 树。

## 1. 范围

TBD

## 2. 不在本轮范围

TBD

## 3. 执行纪律

1. 先完成源码/现状核验，再写功能代码。
2. 当前 Batch Gate 未通过前，不进入下一 Batch。
3. 实现证据若推翻已固定方案，先修订本任务包，再继续实现。

## 4. 文档阅读顺序

以本目录编号为唯一阅读顺序；`00` 为入口。
"""


def direct_prompt(version: str) -> str:
    return f"""# {version} 下一位 AI 直接执行 Prompt

## 目标

从本任务包开始执行，不另建平行任务目录。

## 开始前

1. 阅读 `00_{version}_*` 总控。
2. 阅读研究、差距、裁决、Write Scope、测试矩阵和实现前裁决文档。
3. 从 Batch 0 开始。

## 执行纪律

- 先核验当前源码与依赖版本。
- 每个 Batch 保持 RED → implementation → GREEN → evidence 闭环。
- 遇到架构冲突或真机证据推翻默认方案时，先更新本任务包。
"""


def checklist(version: str) -> str:
    return f"""# {version} 实现前逐项自检表

| 项目 | 状态 | 证据/落点 | Gate |
|---|---|---|---|
| 上游源码核验 | 待完成 | TBD | Batch 0 |
| 当前仓库差距核验 | 待完成 | TBD | Batch 0 |
| 实现方案无开放歧义 | 待确认 | TBD | Batch 0 |
| RED 测试存在 | 待完成 | TBD | 各 Batch |
| GREEN 证据归档 | 待完成 | TBD | 各 Batch |
| 真机证据 | 按需 | TBD | Device Gate |
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("platform")
    parser.add_argument("date")
    parser.add_argument("slug")
    parser.add_argument("major")
    parser.add_argument("version")
    args = parser.parse_args()

    version_dir = validate(args)
    if version_dir.exists():
        die(f"task-package version already exists: {version_dir.relative_to(REPO_ROOT)}")

    write_new(version_dir / f"00_{args.version}_总控_范围边界与执行纪律.md", control(args.version))
    write_new(version_dir / f"18_{args.version}_下一位AI直接执行Prompt.md", direct_prompt(args.version))
    write_new(version_dir / f"19_{args.version}_实现前逐项自检表.md", checklist(args.version))

    subprocess.run(
        [sys.executable, str(REPO_ROOT / "tools" / "check_platform_port_plans.py")],
        cwd=REPO_ROOT,
        check=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
