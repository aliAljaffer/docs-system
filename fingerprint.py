"""Print one digest of this repo's HEAD plus the head commit of every remote source branch."""
from __future__ import annotations

import hashlib
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

import fetch


def git(*args: str) -> str:
    return subprocess.run(["git", *args], check=True, capture_output=True, text=True, cwd=fetch.ROOT).stdout.strip()


def remote_line(repo: str, branch: str) -> str:
    try:
        out = git("ls-remote", f"https://github.com/{repo}.git", f"refs/heads/{branch}")
    except subprocess.CalledProcessError as error:
        raise SystemExit(f"{repo} {branch}: git ls-remote failed: {error.stderr.strip()}")
    if not out:
        raise SystemExit(f"{repo} {branch}: branch not found")
    return f"{repo} {branch} {out.split()[0]}"


def main() -> None:
    config = fetch.load()
    pairs = {
        (e["repo"], e["branch"])
        for kind in ("projects", "courses")
        for e in config.get(kind, [])
        if not e.get("local") and "src" not in e
    }
    with ThreadPoolExecutor(max_workers=6) as pool:
        lines = list(pool.map(lambda pair: remote_line(*pair), pairs))
    lines.append(f"HEAD {git('rev-parse', 'HEAD')}")
    print(hashlib.sha256("\n".join(sorted(lines)).encode()).hexdigest())


if __name__ == "__main__":
    sys.exit(main())
