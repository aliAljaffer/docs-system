"""Diff lexer for the docs site. Adds `~` changed lines to the standard diff rules.

Fences use the alias `docs-diff`. The build rewrites diff fences to it.
"""
from pygments.lexer import inherit
from pygments.lexers.diff import DiffLexer
from pygments.token import Generic


class DocsDiffLexer(DiffLexer):
    name = "Docs diff"
    aliases = ["docs-diff"]
    filenames = []
    mimetypes = []

    tokens = {
        "root": [
            (r"~.*\n", Generic.Changed),
            inherit,
        ],
    }
