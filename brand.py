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
OPTIONAL = ("paper_2", "paper_3", "ink_strong", "ink_soft", "ink_faint", "rule", "accent_ink", "code")
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
    fonts: dict[str, str]
    stylesheets: list[str]
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
    return colours


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
    if not icon or not (path.parent / icon).is_file():
        raise SystemExit(f"brand.json: icon file not found: {icon}")
    return Brand(
        modes={mode: resolve(raw, mode) for mode in MODES},
        fonts=fonts,
        stylesheets=list(raw.get("stylesheets", [])),
        favicon=icon,
        source=path.parent,
    )


def font_stack(name: str, family: str) -> str:
    return f'"{family}", ' + ("monospace" if name == "code" else "system-ui, sans-serif")


def custom_properties(colours: dict[str, str]) -> str:
    lines = [f"  --brand-{key.replace('_', '-')}: {value};\n" for key, value in colours.items()]
    lines += [f"  --brand-{key.replace('_', '-')}-rgb: {rgb(colours[key]).replace(',', '')};\n" for key in TRIPLETS]
    return "".join(lines)


def css(brand: Brand) -> str:
    families = "".join(f"  --brand-font-{name}: {font_stack(name, family)};\n" for name, family in brand.fonts.items())
    light = custom_properties(brand.modes["light"])
    night = custom_properties(brand.modes["night"])
    return (
        f":root,\n[data-md-color-scheme=\"default\"] {{\n{light}{families}}}\n\n"
        f"[data-md-color-scheme=\"slate\"] {{\n{night}}}\n"
    )


def rgb(colour: str) -> str:
    return ", ".join(str(int(colour[i:i + 2], 16)) for i in (1, 3, 5))


def asset_url(entry: str, site_url: str) -> str:
    return entry if re.match(r"https?://", entry) else f"{site_url}/assets/brand/{entry}"


def giscus_css(brand: Brand, mode: str, site_url: str) -> str:
    colours = brand.modes[mode]
    values = {key: value for key, value in colours.items()}
    values.update(accent_rgb=rgb(colours["accent"]), paper_rgb=rgb(colours["paper"]))
    values.update(GISCUS_MODE[mode], font_text=font_stack("text", brand.fonts["text"]))
    values["imports"] = "".join(f"@import url(\"{asset_url(e, site_url)}\");\n" for e in brand.stylesheets)
    return Template(GISCUS_TEMPLATE.read_text()).substitute(values)


def compile(brand: Brand, assets: Path, site_url: str) -> None:
    target = assets / "brand"
    shutil.copytree(brand.source, target, ignore=shutil.ignore_patterns("brand.json"))
    (assets / "brand.css").write_text(css(brand))
    for mode, name in MODES.items():
        (assets / f"giscus-{name}.css").write_text(giscus_css(brand, mode, site_url))


def asset_inputs(brand: Brand) -> list[Path]:
    return sorted(p for p in brand.source.rglob("*") if p.is_file()) + [GISCUS_TEMPLATE]
