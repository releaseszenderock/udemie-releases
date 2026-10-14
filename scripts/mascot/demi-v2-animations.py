#!/usr/bin/env python3
"""Generate transparent looping Animated WebP of Demi for Udemie.

Inputs are the approved v2 SVG-derived PNGs stored in the versioned
udemie-demi-asset-pack-v2.zip. No remote downloads or secrets required.
"""
from __future__ import annotations

import io
import math
import zipfile
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / "design/mascot/demi/v2/udemie-demi-asset-pack-v2.zip"
DEST = ROOT / "design/mascot/demi/v2/animations"
DEST.mkdir(parents=True, exist_ok=True)

def source(name: str) -> Image.Image:
    with zipfile.ZipFile(ARCHIVE) as bundle:
        member = f"demi_v2_assets/png/512/demi-{name}.png"
        return Image.open(io.BytesIO(bundle.read(member))).convert("RGBA")

def pose(sprite: Image.Image, angle: float = 0, rise: float = 0, zoom: float = 1) -> Image.Image:
    base = sprite
    if zoom != 1:
        side = max(1, int(round(512 * zoom)))
        base = base.resize((side, side), Image.Resampling.LANCZOS)
    if angle:
        base = base.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)
    canvas = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    x = (512 - base.width) // 2
    y = (512 - base.height) // 2 + round(rise)
    canvas.alpha_composite(base, (x, y))
    return canvas

def sparkle(draw: ImageDraw.ImageDraw, x: float, y: float, radius: float, color, angle: float = 0):
    pts = []
    for j in range(8):
        t = angle + j * math.pi / 4
        r = radius if j % 2 == 0 else radius * .42
        pts.append((x + r * math.cos(t), y + r * math.sin(t)))
    draw.polygon(pts, fill=color)

def save(name: str, frames: list[Image.Image], duration: int) -> None:
    path = DEST / f"demi-{name}-animated.webp"
    frames[0].save(
        path, format="WEBP", save_all=True, append_images=frames[1:],
        duration=duration, loop=0, quality=90, method=6, lossless=False,
    )
    check = Image.open(path)
    assert check.n_frames >= 12, f"{path}: too few frames"
    assert check.mode == "RGBA", f"{path}: transparency lost"
    check.seek(check.n_frames // 2)
    assert check.getpixel((0, 0))[3] == 0, f"{path}: background not transparent"
    print(f"{path} : {check.n_frames} frames, {path.stat().st_size:,} bytes")

classic, happy = source("classic"), source("happy")
thinking, curious, celebrating = source("thinking"), source("curious"), source("celebrating")

# 1. Gentle welcome / wave loop
frames = []
for i in range(18):
    phase = i * 2 * math.pi / 18
    beat = (1 + math.sin(phase)) / 2
    sprite = Image.blend(classic, happy, 0.15 + beat * .25)
    frame = pose(sprite, angle=2.5 * math.sin(phase), rise=-6 * math.sin(phase))
    draw = ImageDraw.Draw(frame)
    ink = (140, 99, 255, round(110 + 100 * beat))
    draw.arc([396, 118, 475, 198], 300, 70, fill=ink, width=6)
    draw.arc([412, 100, 505, 212], 300, 70, fill=(140, 99, 255, ink[3] - 40), width=5)
    frames.append(frame)
save("waving", frames, 70)

# 2. Quiet thinking loop
frames = []
for i in range(20):
    phase = i * 2 * math.pi / 20
    amt = max(0, math.sin(phase)) * .18
    sprite = Image.blend(thinking, curious, amt)
    frame = pose(sprite, angle=1.5 * math.sin(phase / 2), rise=-4 * math.sin(phase))
    draw = ImageDraw.Draw(frame)
    for j, (x, y, r) in enumerate([(390, 120, 10), (425, 92, 15), (470, 62, 22)]):
        radius = r * (1 + .18 * math.sin(phase + j * .8))
        alpha = round(170 + 60 * math.sin(phase + j))
        draw.ellipse(
            (x-radius, y-radius, x+radius, y+radius),
            fill=(188, 164, 255, max(60, alpha)),
            outline=(140, 99, 255, max(100, alpha)),
        )
    frames.append(frame)
save("thinking", frames, 80)

# 3. Celebration loop
frames = []
positions = [(90, 150), (430, 110), (455, 250), (105, 280), (390, 350)]
colors = [(247,203,83,220), (140,99,255,220), (255,111,170,220)]
for i in range(20):
    phase = i * 2 * math.pi / 20
    jump = max(0, math.sin(phase))
    sprite = Image.blend(celebrating, happy, .12 * (1 - jump))
    frame = pose(sprite, angle=4*math.sin(phase), rise=-25*jump + 6*math.sin(2*phase), zoom=1+.04*jump)
    draw = ImageDraw.Draw(frame)
    for j, (x,y) in enumerate(positions):
        sparkle(draw, x, y, 7*(1+.4*math.sin(2*phase+j)), colors[j%3], phase+j)
    for j in range(8):
        x = 70 + j*48 + 6*math.sin(phase+j)
        y = 70 + (j%3)*30 + 12*jump
        draw.rectangle((x,y,x+5,y+14), fill=colors[j%3])
    frames.append(frame)
save("celebrating", frames, 65)

print("Animated WebP assets ready")
