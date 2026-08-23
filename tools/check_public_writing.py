#!/usr/bin/env python3
"""Lint tracked Markdown for private-discussion language in the public repository.

This is a repository writing guard, not a general grammar checker. Its purpose
is to prevent a recurring class of documentation errors: text copied from a
private owner/assistant discussion into material that is publicly committed.

All tracked Markdown is in scope, including docs/plans, Task Designs and AI
Execution Prompts. Markdown fenced code blocks, inline code spans, and clearly
curly-quoted prohibited-writing examples are excluded from prose scanning.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# These patterns deliberately target private-advisory / chat-transcript wording,
# not ordinary normative instructions such as "Contributor MUST ...".
CHINESE_PATTERNS: tuple[tuple[str, str], ...] = (
    ("粗暴地", "private/advisory characterization"),
    ("吓退", "audience-psychology reasoning"),
    ("产生反感", "audience-psychology reasoning"),
    ("白嫖", "informal/private commercial wording"),
    ("门票费", "informal/private commercial wording"),
    ("我建议", "personal advisory voice"),
    ("我的建议", "personal advisory voice"),
    ("我认为", "personal advisory voice"),
    ("我觉得", "personal advisory voice"),
    ("我们建议", "private-consultation voice"),
    ("我们认为", "private-consultation voice"),
    ("我们觉得", "private-consultation voice"),
    ("我们刚刚", "private conversation reference"),
    ("刚刚讨论", "private conversation reference"),
    ("刚才讨论", "private conversation reference"),
    ("前面讨论", "private conversation reference"),
    ("上面讨论", "private conversation reference"),
    ("前面说过", "private conversation reference"),
    ("上面说过", "private conversation reference"),
    ("你刚才", "private conversation reference"),
    ("你前面", "private conversation reference"),
    ("对你说", "private conversation reference"),
    ("跟你说", "private conversation reference"),
    ("帮你", "personal assistant voice"),
    ("为了赚钱", "confidential monetization-style reasoning"),
    ("怎么赚钱", "confidential monetization-style reasoning"),
    ("厂商会不愿意", "private audience-psychology reasoning"),
    ("让厂商更愿意", "private audience-psychology reasoning"),
)

ENGLISH_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = tuple(
    (re.compile(pattern, re.IGNORECASE), reason)
    for pattern, reason in (
        (r"\bI\s+(?:recommend|suggest|think|believe|feel)\b", "personal advisory voice"),
        (r"\bwe\s+(?:recommend|suggest|think|believe|feel)\b", "private-consultation voice"),
        (r"\bas\s+we\s+discussed\b", "private conversation reference"),
        (r"\bin\s+our\s+(?:earlier|previous)\s+(?:discussion|conversation)\b", "private conversation reference"),
        (r"\bjust\s+discussed\b", "private conversation reference"),
        (r"\bto\s+avoid\s+turning\s+away\b", "audience-psychology reasoning"),
        (r"\bscare\s+off\b", "audience-psychology reasoning"),
        (r"\balarming\s+commercial(?:-license)?\b", "audience-psychology reasoning"),
        (r"\bforcing\s+every\s+asset\s+into\s+one\s+license\b", "private decision-discussion wording"),
        (r"\bpay(?:ing)?\s+(?:an?\s+)?fee\s+merely\b", "private commercial rationale"),
        (r"\bthe\s+intent\s+is\s+to\s+avoid\s+charging\b", "private commercial rationale"),
        (r"\bwants?\s+device\s+(?:vendors?|makers?)\s+to\s+have\s+a\s+strong\s+reason\b", "private audience-psychology reasoning"),
        (r"\bwe\s+do\s+not\s+want\b", "private-consultation voice"),
        (r"\bwe\s+don't\s+want\b", "private-consultation voice"),
    )
)

CURLY_QUOTED_EXAMPLE_RE = re.compile(r"“[^”]*”|‘[^’]*’")
OPEN_FENCE_RE = re.compile(r"^ {0,3}(?P<fence>`{3,}|~{3,})")
CLOSE_FENCE_RE = re.compile(r"^ {0,3}(?P<fence>`{3,}|~{3,})[ \t]*$")


def tracked_markdown() -> list[Path]:
    """Return tracked Markdown paths without Git C-style path quoting."""
    proc = subprocess.run(
        ["git", "-c", "core.quotepath=false", "ls-files", "-z", "--", "*.md"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    paths: list[Path] = []
    for raw in proc.stdout.split(b"\0"):
        if not raw:
            continue
        paths.append(ROOT / raw.decode("utf-8", errors="strict"))
    return paths


def strip_inline_code_spans(line: str) -> str:
    """Remove valid backtick code spans while preserving ordinary text.

    Markdown code spans are delimited by backtick runs of exactly the same
    length. A shorter run inside a longer-delimited span therefore does not
    close it. Unclosed delimiters remain ordinary text and are scanned.
    """
    chars = list(line)
    length = len(line)
    i = 0

    while i < length:
        if line[i] != "`":
            i += 1
            continue

        opener_start = i
        while i < length and line[i] == "`":
            i += 1
        opener_len = i - opener_start

        search = i
        closing_start: int | None = None
        closing_end: int | None = None
        while search < length:
            next_tick = line.find("`", search)
            if next_tick < 0:
                break
            run_end = next_tick
            while run_end < length and line[run_end] == "`":
                run_end += 1
            run_len = run_end - next_tick
            if run_len == opener_len:
                closing_start = next_tick
                closing_end = run_end
                break
            search = run_end

        if closing_start is None or closing_end is None:
            # CommonMark treats an unmatched opener as literal text.
            continue

        for pos in range(opener_start, closing_end):
            chars[pos] = " "
        i = closing_end

    return "".join(chars)


def visible_lines(path: Path):
    """Yield prose lines while excluding Markdown fenced/code-span content."""
    in_fence = False
    fence_char: str | None = None
    fence_len = 0

    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if in_fence:
            close = CLOSE_FENCE_RE.match(raw)
            if close:
                run = close.group("fence")
                if run[0] == fence_char and len(run) >= fence_len:
                    in_fence = False
                    fence_char = None
                    fence_len = 0
            continue

        opening = OPEN_FENCE_RE.match(raw)
        if opening:
            run = opening.group("fence")
            # A backtick opening fence cannot contain another backtick later in
            # its info string under CommonMark. Treat malformed lines as prose.
            suffix = raw[opening.end():]
            if run[0] == "`" and "`" in suffix:
                pass
            else:
                in_fence = True
                fence_char = run[0]
                fence_len = len(run)
                continue

        line = strip_inline_code_spans(raw)
        line = CURLY_QUOTED_EXAMPLE_RE.sub("", line)
        yield lineno, line


def main() -> int:
    errors: list[str] = []

    for path in tracked_markdown():
        rel = path.relative_to(ROOT).as_posix()
        if rel == "private" or rel.startswith("private/"):
            errors.append(f"{rel}: tracked private material is forbidden in the public repository")
            continue

        for lineno, line in visible_lines(path):
            for needle, reason in CHINESE_PATTERNS:
                if needle in line:
                    errors.append(f"{rel}:{lineno}: {reason}: {needle!r}")
            for pattern, reason in ENGLISH_PATTERNS:
                match = pattern.search(line)
                if match:
                    errors.append(f"{rel}:{lineno}: {reason}: {match.group(0)!r}")

    if errors:
        print("[public-writing-guard] ERROR")
        for error in errors:
            print(f" - {error}")
        print(
            "\nRewrite tracked prose as public project documentation. "
            "Private strategy belongs in ignored private/ or a separate private repository."
        )
        return 1

    print("[public-writing-guard] OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
