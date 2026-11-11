"""Read and write YAML front matter in Markdown pages."""
from __future__ import annotations

import yaml


def split_meta(text: str) -> tuple[dict, str]:
    if text.startswith("---\n") and "\n---\n" in text[4:]:
        end = text.find("\n---\n", 4)
        return yaml.safe_load(text[4:end]) or {}, text[end + 5:]
    return {}, text


def join_meta(meta: dict, body: str) -> str:
    return "---\n" + yaml.safe_dump(meta, sort_keys=False, allow_unicode=True) + "---\n" + body
