"""Shell lexer for the docs site. Colours a command, its first subcommand, flags, strings and placeholders.

Fences use the alias `docs-shell`. The build rewrites bash, sh, shell, console and zsh fences to it.
"""
from pygments.lexer import RegexLexer, Whitespace, default, include
from pygments.token import Comment, Keyword, Name, Number, Operator, String, Text


class DocsShellLexer(RegexLexer):
    name = "Docs shell"
    aliases = ["docs-shell"]
    filenames = []

    tokens = {
        "space": [
            (r"[ \t]+", Whitespace),
            (r"\\\n", Text),
            (r"#.*$", Comment.Single),
        ],
        "separator": [
            (r"\|\||&&|[|;&()]", Operator, "root"),
            (r"\n", Text, "root"),
        ],
        "root": [
            include("space"),
            include("separator"),
            (r"[\w.+-]+", Name.Function, "subcommand"),
            (r"\S", Text, "args"),
        ],
        "subcommand": [
            include("space"),
            include("separator"),
            (r"[\w.+-]+", Keyword, "args"),
            default("args"),
        ],
        "args": [
            include("space"),
            include("separator"),
            include("values"),
        ],
        "values": [
            (r'"(\\.|[^"\\])*"', String.Double),
            (r"'[^']*'", String.Single),
            (r"\$\{[^}]*\}|\$[A-Za-z_]\w*|\$[0-9?#!$@*]", Name.Variable),
            (r"<[^>\s]+>", Name.Variable),
            (r"--?[A-Za-z][\w-]*", Name.Builtin),
            (r"\b\d+\b", Number),
            (r"[<>]+", Operator),
            (r"[^\s|&;()\"'<>$#\n]+", Text),
        ],
    }
