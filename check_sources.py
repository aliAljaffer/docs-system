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
            errors += [f"{label} missing {key}" for key in REQUIRED if key not in entry]
            if entry.get("slug") in slugs:
                errors.append(f"{label} duplicate slug")
            slugs.add(entry.get("slug"))
    print("\n".join(errors) or f"{len(slugs)} sources ok")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
