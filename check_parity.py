#!/usr/bin/env python3
"""Check each episode page against its video script and the page standard."""
from __future__ import annotations

import re
import sys
from pathlib import Path

FOUR_HATS = Path("/Users/h/mk-project/four-hats")
HQ = Path("/Users/h/mk-project/hq-main")
PAGES = FOUR_HATS / "docs" / "episodes"
COMPOSED = Path("/Users/h/docs-system/build/en/four-hats/episodes")
SCRIPTS = HQ / "scripts"
DIAGRAMS = HQ / "scripts" / "diagrams"

REQUIRED = [
    "What you will be able to do",
    "Before you start",
    "Common mistakes",
    "Check your work",
    "What this unlocks on your CV",
    "Next",
]

STOP = {
    "a", "an", "the", "and", "or", "to", "of", "in", "on", "with", "for",
    "your", "you", "it", "is", "are", "be", "that", "this", "how", "what",
    "why", "from", "as", "at", "by", "not", "do", "does", "can", "will",
    "each", "one", "same", "app", "episode", "complete", "use", "run",
}


def words(text: str) -> set[str]:
    return {
        w for w in re.findall(r"[a-z0-9]+", text.lower())
        if len(w) > 2 and w not in STOP
    }


def fenced(text: str) -> list[str]:
    return re.findall(r"```[a-z]*\n(.*?)```", text, flags=re.S)


def section(text: str, name: str) -> str:
    match = re.search(
        rf"^#{{2,3}} {re.escape(name)}\s*$(.*?)(?=^#{{2,3}} |\Z)", text, flags=re.M | re.S
    )
    return match.group(1) if match else ""


def check(page: Path, script: Path) -> list[str]:
    text = page.read_text()
    src = script.read_text()
    problems: list[str] = []

    for name in REQUIRED:
        if not re.search(rf"^## {re.escape(name)}\s*$", text, flags=re.M):
            problems.append(f"missing section: {name}")

    goals = []
    if "**Learning goals:**" in src:
        block = src.split("**Learning goals:**")[1].split("**Prerequisites:**")[0]
        goals = [g.strip() for g in re.findall(r"^- (.+)$", block, flags=re.M)]
    if len(goals) < 3:
        problems.append(f"script has only {len(goals)} learning goals")
    page_words = words(text)
    for goal in goals:
        goal_words = words(goal)
        hit = len(goal_words & page_words)
        if goal_words and hit / len(goal_words) < 0.6:
            problems.append(f"goal not covered: {goal[:60]}")

    composed_path = COMPOSED / page.name
    composed = composed_path.read_text() if composed_path.exists() else text
    norm_page = re.sub(r"\s+", " ", composed)
    composed_words = words(composed)
    for i, block in enumerate(fenced(src), 1):
        lines = [ln.strip() for ln in block.splitlines() if len(ln.strip()) > 12]
        if len(lines) < 2:
            continue
        found = sum(1 for ln in lines if re.sub(r"\s+", " ", ln) in norm_page)
        tokens = words(block)
        token_hit = len(tokens & composed_words) / len(tokens) if tokens else 1.0
        if found / len(lines) < 0.5 and token_hit < 0.7:
            problems.append(
                f"code block {i} not represented (lines {found}/{len(lines)}, tokens {token_hit:.0%})"
            )

    expects = src.count("**Expect:**") + src.count("**Expected output:**")
    page_expects = len(re.findall(r"Expected output|Expected:|You should see", text, flags=re.M))
    should = section(text, "What you should see")
    page_expects += max(0, len(re.findall(r"^\|", should, flags=re.M)) - 2)
    if expects and page.name.startswith("ep00"):
        expects = 0
    if expects and page_expects < max(3, expects // 3):
        problems.append(f"expected output blocks: {page_expects} for {expects} video checks")

    ep = re.match(r"ep(\d{2})", page.name).group(1)
    if list(DIAGRAMS.glob(f"ep{ep}-*.png")) and f"ep{ep}-" not in text:
        problems.append("diagram exists but page does not reference it")

    mistakes = section(text, "Common mistakes")
    if len(re.findall(r"^- ", mistakes, flags=re.M)) < 3:
        problems.append("fewer than 3 common mistakes")

    checkwork = section(text, "Check your work")
    if len(re.findall(r"^- \[ \]", checkwork, flags=re.M)) < 3:
        problems.append("fewer than 3 checklist items")

    body_words = len(re.findall(r"[A-Za-z0-9']+", text))
    if body_words < 700:
        problems.append(f"page too thin: {body_words} words")

    if "Video coming" in text or "Key idea" in text:
        problems.append("contains generator stub text")

    if "\u2014" in text:
        problems.append("contains an em dash")

    return problems


def main() -> None:
    pages = sorted(PAGES.glob("ep*.md"))
    scripts = {p.stem: p for p in SCRIPTS.glob("ep*.md")}
    if not pages:
        raise SystemExit(f"No pages in {PAGES}")

    failed = 0
    for page in pages:
        problems = check(page, scripts[page.stem]) if page.stem in scripts else [
            "no matching video script"
        ]
        status = "PASS" if not problems else "FAIL"
        print(f"{status} {page.name}")
        for problem in problems:
            print(f"     {problem}")
        failed += bool(problems)

    print(f"\n{len(pages) - failed}/{len(pages)} pages pass")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
