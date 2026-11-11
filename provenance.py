"""Stamp pages with the last commit date and GitHub edit link of their source file."""
from __future__ import annotations

import subprocess
from pathlib import Path
from typing import NamedTuple
from urllib.parse import quote

from frontmatter import join_meta, split_meta


SELF_REPO = "aliAljaffer/docs-system"
SELF_BRANCH = "main"


class Origin(NamedTuple):
    repo: str
    branch: str
    prefix: str

    def edit_url(self, rel: str) -> str:
        parts = [] if self.prefix in ("", ".") else self.prefix.strip("/").split("/")
        path = "/".join(quote(part) for part in [*parts, *rel.split("/")])
        return f"https://github.com/{self.repo}/edit/{self.branch}/{path}"


def local_origin(prefix: str) -> Origin:
    return Origin(SELF_REPO, SELF_BRANCH, prefix)


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-c", "core.quotepath=off", "-C", str(repo), *args],
        check=True, capture_output=True, text=True,
    )
    return result.stdout


def commit_dates(repo: Path, subpath: str) -> dict[str, str]:
    if git(repo, "rev-parse", "--is-shallow-repository").strip() == "true":
        raise SystemExit(f"{repo}: shallow clone, commit dates would be wrong. Fetch full history.")
    prefix = "" if subpath == "." else subpath.rstrip("/") + "/"
    dates: dict[str, str] = {}
    date = ""
    for line in git(repo, "log", "--format=@%cs", "--name-only", "--", subpath).splitlines():
        if line.startswith("@"):
            date = line[1:]
        elif line and line.startswith(prefix):
            dates.setdefault(line[len(prefix):], date)
    return dates


def stamp(dst: Path, dates: dict[str, str], origin: Origin) -> None:
    for page in dst.rglob("*.md"):
        rel = page.relative_to(dst).as_posix()
        date = dates.get(rel)
        if not date:
            continue
        meta, body = split_meta(page.read_text())
        meta.setdefault("updated", date)
        meta.setdefault("edit_url", origin.edit_url(rel))
        page.write_text(join_meta(meta, body))
