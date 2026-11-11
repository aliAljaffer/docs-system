"""Clone each repo in sources.yaml and copy its docs into build/en/<kind>/<slug>/."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
CACHE = ROOT / ".cache"
KEEP = {".md", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".html", ".css", ".ttf"}
SKIP_NAMES = {"AGENTS.md", "CLAUDE.md"}


def clone(entry: dict) -> Path:
    if "src" in entry:
        return ROOT / entry["src"]
    dest = CACHE / entry["slug"]
    shutil.rmtree(dest, ignore_errors=True)
    cmd = ["git", "clone", "--quiet", "--depth", "1", "--branch", entry["branch"]]
    if entry["path"] != ".":
        cmd += ["--filter=blob:none", "--sparse"]
    cmd += [f"https://github.com/{entry['repo']}.git", str(dest)]
    subprocess.run(cmd, check=True)
    if entry["path"] != ".":
        subprocess.run(["git", "-C", str(dest), "sparse-checkout", "set", entry["path"]], check=True)
    return dest / entry["path"]


def describe(repo: str) -> str:
    request = urllib.request.Request(f"https://api.github.com/repos/{repo}")
    if os.environ.get("GITHUB_TOKEN"):
        request.add_header("Authorization", f"Bearer {os.environ['GITHUB_TOKEN']}")
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return json.load(response).get("description") or ""
    except OSError:
        return ""


def copy_docs(src: Path, dst: Path, exclude: list[str]) -> int:
    count = 0
    for path in sorted(src.rglob("*")):
        rel = path.relative_to(src)
        if not path.is_file() or path.suffix.lower() not in KEEP:
            continue
        if any(part.startswith(".") for part in rel.parts) or path.name in SKIP_NAMES:
            continue
        if rel.parts[0] in exclude or (rel.parts[0] == "slides" and path.suffix == ".md"):
            continue
        if path.suffix == ".html" and rel.parts[0] != "slides":
            continue
        (dst / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dst / rel)
        count += 1
    return count


def load() -> dict[str, list[dict]]:
    return yaml.safe_load((ROOT / "sources.yaml").read_text())


def dest_of(kind: str, entry: dict) -> str:
    return f"projects/{entry['slug']}" if kind == "projects" else entry["slug"]


def fetch_all(root: Path, config: dict) -> None:
    entries = [(kind, e) for kind in ("projects", "courses") for e in config.get(kind, []) if not e.get("local")]
    # Bounded to 6 concurrent clones: network-bound, one per repo, GitHub tolerates it.
    with ThreadPoolExecutor(max_workers=6) as pool:
        clones = [pool.submit(clone, e) for _, e in entries]
        described = [pool.submit(describe, e["repo"]) for _, e in entries]
        srcs = [f.result() for f in clones]
        descriptions = [f.result() for f in described]
    for (kind, entry), src, description in zip(entries, srcs, descriptions):
        if description:
            entry.setdefault("description", description)
        if not src.is_dir():
            raise SystemExit(f"{entry['repo']}: path not found: {entry['path']}")
        dst = root / dest_of(kind, entry)
        if copy_docs(src, dst, entry.get("exclude", [])) == 0:
            raise SystemExit(f"{entry['repo']}: no docs under {entry['path']}")


if __name__ == "__main__":
    import sys
    fetch_all(Path(sys.argv[1]), load())
