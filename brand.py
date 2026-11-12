"""Compile brand/brand.json into the CSS the site and the Giscus iframe consume."""
from __future__ import annotations

import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from string import Template

ROOT = Path(__file__).resolve().parent
BRAND_DIR = ROOT / "brand"
GISCUS_TEMPLATE = ROOT / "templates" / "giscus.css.tmpl"
MODES = {"light": "light", "night": "dark"}
REQUIRED = ("paper", "ink", "accent")
OPTIONAL = ("paper_2", "paper_3", "ink_strong", "ink_soft", "ink_faint", "rule", "accent_ink", "code", "accent_fill", "on_accent")
SYNTAX = ("bg", "text", "keyword", "function", "string", "number", "type", "comment", "punctuation")
SHAPE_DEFAULTS = {"radius": "0", "radius_lg": "0", "label_size": "11px", "shadow": False, "headings": "text"}
SIZE = re.compile(r"^(0|\d+(\.\d+)?px)$")
TRIPLETS = ("paper", "paper_2", "ink", "accent")
HEX = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")
GISCUS_MODE = {
    "light": {
        "gray_step": "gray-1",
        "blue_step": "blue-1",
        "loader_line": "https://github.com/images/modules/pulls/progressive-disclosure-line.svg",
        "loader_image": "https://github.githubassets.com/images/mona-loading-default.gif",
    },
    "night": {
        "gray_step": "gray-7",
        "blue_step": "blue-8",
        "loader_line": "https://github.com/images/modules/pulls/progressive-disclosure-line-dark.svg",
        "loader_image": "https://github.githubassets.com/images/mona-loading-dark.gif",
    },
}


@dataclass(frozen=True)
class Brand:
    modes: dict[str, dict[str, str]]
    syntax: dict[str, dict[str, str]]
    shape: dict[str, object]
    fonts: dict[str, str]
    stylesheets: list[str]
    logo: str
    favicon: str
    source: Path


def normalize_hex(value: object, where: str) -> str:
    if not isinstance(value, str) or not HEX.match(value):
        raise SystemExit(f"brand.json: {where} must be a hex colour like #1a2b3c, got {value!r}")
    value = value.lower()
    return "#" + "".join(c * 2 for c in value[1:]) if len(value) == 4 else value


def mix(ink: str, percent: int, paper: str) -> str:
    return f"color-mix(in srgb, {ink} {percent}%, {paper})"


def resolve(raw: dict, mode: str) -> dict[str, str]:
    if not isinstance(raw.get(mode), dict):
        raise SystemExit(f"brand.json: missing '{mode}' colours")
    given = raw[mode]
    for key in REQUIRED:
        if key not in given:
            raise SystemExit(f"brand.json: {mode}.{key} is required")
    unknown = set(given) - set(REQUIRED) - set(OPTIONAL)
    if unknown:
        raise SystemExit(f"brand.json: unknown {mode} keys: {', '.join(sorted(unknown))}")
    colours = {key: normalize_hex(value, f"{mode}.{key}") for key, value in given.items()}
    paper, ink, accent = (colours[k] for k in REQUIRED)
    colours.setdefault("paper_2", paper)
    colours.setdefault("paper_3", colours["paper_2"])
    colours.setdefault("ink_strong", ink)
    colours.setdefault("ink_soft", mix(ink, 70, paper))
    colours.setdefault("ink_faint", mix(ink, 55, paper))
    colours.setdefault("rule", mix(ink, 14, paper))
    colours.setdefault("accent_ink", accent)
    colours.setdefault("code", colours["accent_ink"])
    colours.setdefault("accent_fill", accent)
    colours.setdefault("on_accent", paper)
    return colours


def resolve_syntax(raw: dict, mode: str, colours: dict[str, str]) -> dict[str, str]:
    """Code colours. Missing keys fall back to the roles the theme always used (keyword = code, function = accent_ink)."""
    defaults = {
        "bg": colours["paper_2"], "text": colours["ink"],
        "keyword": colours["code"], "number": colours["code"],
        "function": colours["accent_ink"], "type": colours["accent_ink"],
        "string": colours["ink_soft"], "comment": colours["ink_soft"], "punctuation": colours["ink_soft"],
    }
    given = (raw.get("syntax") or {}).get(mode) or {}
    unknown = set(given) - set(SYNTAX)
    if unknown:
        raise SystemExit(f"brand.json: unknown syntax.{mode} keys: {', '.join(sorted(unknown))}")
    return {**defaults, **{k: normalize_hex(v, f"syntax.{mode}.{k}") for k, v in given.items()}}


def resolve_shape(raw: dict) -> dict[str, object]:
    shape = {**SHAPE_DEFAULTS, **(raw.get("shape") or {})}
    unknown = set(shape) - set(SHAPE_DEFAULTS)
    if unknown:
        raise SystemExit(f"brand.json: unknown shape keys: {', '.join(sorted(unknown))}")
    for key in ("radius", "radius_lg", "label_size"):
        if not isinstance(shape[key], str) or not SIZE.match(shape[key]):
            raise SystemExit(f"brand.json: shape.{key} must be 0 or a px size like 12px, got {shape[key]!r}")
    if shape["headings"] not in ("text", "display"):
        raise SystemExit("brand.json: shape.headings must be 'text' or 'display'")
    return shape


def load(path: Path = BRAND_DIR / "brand.json") -> Brand:
    try:
        raw = json.loads(path.read_text())
    except (OSError, ValueError) as error:
        raise SystemExit(f"brand.json: {error}")
    fonts = raw.get("fonts") or {}
    if not fonts.get("text"):
        raise SystemExit("brand.json: fonts.text is required")
    fonts = {"text": fonts["text"], "code": fonts.get("code", fonts["text"]), "display": fonts.get("display", fonts["text"])}
    icon = raw.get("icon")
    favicon = raw.get("favicon", icon)
    for key, name in (("icon", icon), ("favicon", favicon)):
        if not name or not (path.parent / name).is_file():
            raise SystemExit(f"brand.json: {key} file not found: {name}")
    modes = {mode: resolve(raw, mode) for mode in MODES}
    return Brand(
        modes=modes,
        syntax={mode: resolve_syntax(raw, mode, modes[mode]) for mode in MODES},
        shape=resolve_shape(raw),
        fonts=fonts,
        stylesheets=list(raw.get("stylesheets", [])),
        logo=icon,
        favicon=favicon,
        source=path.parent,
    )


def font_stack(name: str, family: str) -> str:
    return f'"{family}", ' + ("monospace" if name == "code" else "system-ui, sans-serif")


def custom_properties(colours: dict[str, str]) -> str:
    lines = [f"  --brand-{key.replace('_', '-')}: {value};\n" for key, value in colours.items()]
    lines += [f"  --brand-{key.replace('_', '-')}-rgb: {rgb(colours[key]).replace(',', '')};\n" for key in TRIPLETS]
    return "".join(lines)


def shadow(colours: dict[str, str], mode: str, on: bool) -> str:
    if not on:
        return "none"
    r, g, b = rgb(colours["ink"]).split(", ")
    return f"0 1px 2px rgba({r}, {g}, {b}, 0.04), 0 6px 18px rgba({r}, {g}, {b}, {0.05 if mode == 'light' else 0.3})"


def mode_properties(brand: Brand, mode: str) -> str:
    lines = custom_properties(brand.modes[mode])
    lines += "".join(f"  --brand-syntax-{key}: {value};\n" for key, value in brand.syntax[mode].items())
    lines += f"  --brand-shadow: {shadow(brand.modes[mode], mode, bool(brand.shape['shadow']))};\n"
    return lines


def css(brand: Brand) -> str:
    families = "".join(f"  --brand-font-{name}: {font_stack(name, family)};\n" for name, family in brand.fonts.items())
    families += f"  --brand-font-heading: var(--brand-font-{brand.shape['headings']});\n"
    families += "".join(f"  --brand-{key.replace('_', '-')}: {brand.shape[key]};\n" for key in ("radius", "radius_lg", "label_size"))
    light = mode_properties(brand, "light")
    night = mode_properties(brand, "night")
    return (
        f":root,\n[data-md-color-scheme=\"default\"] {{\n{light}{families}}}\n\n"
        f"[data-md-color-scheme=\"slate\"] {{\n{night}}}\n"
    )


def rgb(colour: str) -> str:
    return ", ".join(str(int(colour[i:i + 2], 16)) for i in (1, 3, 5))


def asset_url(entry: str, site_url: str, version: str) -> str:
    return entry if re.match(r"https?://", entry) else f"{site_url}/assets/brand/{entry}?v={version}"


def giscus_css(brand: Brand, mode: str, site_url: str, version: str) -> str:
    colours = brand.modes[mode]
    values = {key: value for key, value in colours.items()}
    values.update({f"syntax_{key}": value for key, value in brand.syntax[mode].items()})
    values.update(accent_rgb=rgb(colours["accent"]), paper_rgb=rgb(colours["paper"]))
    values.update(GISCUS_MODE[mode], font_text=font_stack("text", brand.fonts["text"]))
    values["imports"] = "".join(f"@import url(\"{asset_url(e, site_url, version)}\");\n" for e in brand.stylesheets)
    return Template(GISCUS_TEMPLATE.read_text()).substitute(values)


def compile(brand: Brand, assets: Path, site_url: str, version: str) -> None:
    target = assets / "brand"
    shutil.copytree(brand.source, target, ignore=shutil.ignore_patterns("brand.json"))
    (assets / "brand.css").write_text(css(brand))
    for mode, name in MODES.items():
        (assets / f"giscus-{name}.css").write_text(giscus_css(brand, mode, site_url, version))


def asset_inputs(brand: Brand) -> list[Path]:
    return sorted(p for p in brand.source.rglob("*") if p.is_file()) + [GISCUS_TEMPLATE]
