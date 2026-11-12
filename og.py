"""Draw the link preview card for every page from brand/og/ (fonts, plate, icon) and the brand colours."""
from __future__ import annotations

import os
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, PAD, PLATE_H, FADE = 1200, 630, 64, 190, 70
KIT_FILES = ("Fraunces.ttf", "Karla.ttf", "SplineSansMono.ttf", "plate.jpg", "icon.png")


@dataclass(frozen=True)
class Card:
    path: str
    title: str
    section: str
    description: str


def rgb(colour: str, fallback: str) -> tuple[int, int, int]:
    value = colour if colour.startswith("#") else fallback
    return tuple(int(value[i:i + 2], 16) for i in (1, 3, 5))


@lru_cache(maxsize=None)
def font(kit: Path, name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(kit / name), size)


@lru_cache(maxsize=None)
def backdrop(kit: Path, paper: tuple, wash_a: tuple, wash_c: tuple, ink_soft: tuple, eyebrow: str) -> Image.Image:
    """Everything that is the same on every card, drawn once per worker."""
    im = Image.new("RGB", (W, H), paper)
    wash = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(wash)
    wd.ellipse((-300, 330, 500, 900), fill=wash_a + (77,))
    wd.ellipse((800, 250, 1600, 750), fill=wash_c + (51,))
    wash = wash.filter(ImageFilter.GaussianBlur(120))
    im.paste(wash, (0, 0), wash)
    plate = Image.open(kit / "plate.jpg").convert("RGB").crop((0, 0, W, PLATE_H))
    fade = Image.new("L", (W, PLATE_H), 255)
    fd = ImageDraw.Draw(fade)
    for y in range(PLATE_H - FADE, PLATE_H):
        fd.line((0, y, W, y), fill=round(255 * (PLATE_H - y) / FADE))
    im.paste(plate, (0, 0), fade)
    icon = Image.open(kit / "icon.png").convert("RGBA").resize((40, 40), Image.LANCZOS)
    im.paste(icon, (PAD, PLATE_H + 28), icon)
    d = ImageDraw.Draw(im)
    mono = font(kit, "SplineSansMono.ttf", 22)
    x = PAD + 54
    for ch in eyebrow:
        d.text((x, PLATE_H + 36), ch, font=mono, fill=ink_soft)
        x += d.textlength(ch, font=mono) + 22 * 0.14
    return im


def wrap(d: ImageDraw.ImageDraw, text: str, face: ImageFont.FreeTypeFont, lines: int) -> list[str]:
    width, out = W - 2 * PAD, [""]
    for word in text.split():
        trial = f"{out[-1]} {word}".strip()
        if d.textlength(trial, font=face) <= width or not out[-1]:
            out[-1] = trial
        else:
            out.append(word)
    if len(out) > lines:
        out = out[:lines]
        while " " in out[-1] and d.textlength(out[-1] + "...", font=face) > width:
            out[-1] = out[-1].rsplit(" ", 1)[0]
        out[-1] += "..."
    return out


def render(kit: Path, colours: dict[str, str], eyebrow: str, card: Card) -> Image.Image:
    ink = colours["ink"]
    tone = lambda key: rgb(colours[key], ink)
    im = backdrop(kit, tone("paper"), tone("wash_a"), tone("wash_c"), tone("ink_soft"), eyebrow).copy()
    d = ImageDraw.Draw(im)
    size = 58 if len(card.title) > 42 else 76
    blocks = [(line, font(kit, "Fraunces.ttf", size), tone("ink_strong"), round(size * 1.1)) for line in wrap(d, card.title, font(kit, "Fraunces.ttf", size), 2)]
    if card.description:
        face = font(kit, "Karla.ttf", 28)
        blocks += [(line, face, tone("ink_soft"), 39) for line in wrap(d, card.description, face, 2)]
    if card.section:
        face = font(kit, "SplineSansMono.ttf", 22)
        blocks += [(line, face, tone("ink_soft"), 31) for line in wrap(d, card.section, face, 1)]
    gaps = sum(1 for i in range(1, len(blocks)) if blocks[i][1] is not blocks[i - 1][1])
    y = H - 52 - sum(b[3] for b in blocks) - 14 * gaps
    for i, (text, face, fill, height) in enumerate(blocks):
        if i and face is not blocks[i - 1][1]:
            y += 14
        d.text((PAD, y), text, font=face, fill=fill)
        y += height
    return im


def _write(job: tuple[Path, dict[str, str], str, Card, Path]) -> None:
    kit, colours, eyebrow, card, site = job
    target = site / card.path / "og.jpg"
    target.parent.mkdir(parents=True, exist_ok=True)
    render(kit, colours, eyebrow, card).save(target, "JPEG", quality=85, optimize=True, progressive=True)


def write_all(kit: Path, colours: dict[str, str], eyebrow: str, cards: list[Card], site: Path) -> int:
    missing = [name for name in KIT_FILES if not (kit / name).is_file()]
    if missing:
        raise SystemExit(f"brand/og is missing {', '.join(missing)}; run make brand")
    with ProcessPoolExecutor(max_workers=os.cpu_count()) as pool:
        list(pool.map(_write, [(kit, colours, eyebrow, card, site) for card in cards], chunksize=8))
    return len(cards)
