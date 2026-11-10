#!/usr/bin/env python3
"""Validate sources.yaml."""
import sys

import fetch

REQUIRED = ("slug", "repo", "branch", "path")


def main() -> int:
    errors, slugs = [], set()
    config = fetch.load()
    for kind in ("projects", "courses"):
        for entry in config.get(kind, []):
            label = f"{kind}: {entry.get('slug', '?')}"
            required = ("slug", "title") if entry.get("local") else REQUIRED
            errors += [f"{label} missing {key}" for key in required if key not in entry]
            if entry.get("local") and not (fetch.ROOT / "content" / "en" / entry.get("slug", "")).is_dir():
                errors.append(f"{label} missing content/en folder")
            if entry.get("slug") in slugs:
                errors.append(f"{label} duplicate slug")
            slugs.add(entry.get("slug"))
    print("\n".join(errors) or f"{len(slugs)} sources ok")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
