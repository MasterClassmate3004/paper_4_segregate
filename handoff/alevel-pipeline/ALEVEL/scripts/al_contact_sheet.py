#!/usr/bin/env python3
"""Labelled contact sheets of every crop in a split directory (visual QA gate).

Crops are laid out in question order (stems before their children), each with
its label and pixel size above it and a thin grey frame so crop edges are
visible.  Several sheets are written if needed: <out>_01.png, <out>_02.png, ...

Usage: al_contact_sheet.py CROPS_DIR PREFIX OUT_BASE [--width 1400] [--per 14]
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def natkey(name: str):
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", name)]


def label_order(label: str):
    # Q4.stem before Q4.a; Q4.b.stem before Q4.b.i AND before a leaf Q4.b
    # (a part's mid-question stem is printed before it); SecB.stem (9701
    # Paper 1 Section B) sits right before Q31
    if label == "SecB.stem":
        label = "Q31.stem"
    parts = label.split(".")
    if parts[-1] == "stem":
        return [(1, natkey(p)) for p in parts[:-1]] + [(0, "")]
    return [(1, natkey(p)) for p in parts] + [(2, "")]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("crops")
    ap.add_argument("prefix")
    ap.add_argument("out")
    ap.add_argument("--width", type=int, default=1400)
    ap.add_argument("--per", type=int, default=14)
    a = ap.parse_args()
    files = sorted(list(Path(a.crops).glob(f"{a.prefix}-Q*.png")) + list(Path(a.crops).glob(f"{a.prefix}-SecB*.png")),
                   key=lambda f: label_order(f.stem[len(a.prefix) + 1:]))
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 22)
    except OSError:
        font = ImageFont.load_default()
    # pack crops into sheets of at most a.per crops AND at most MAX_H pixels
    # tall, so a viewer never has to downscale a sheet below legibility
    MAX_H = 2300
    chunks, cur, h = [], [], 10
    for f in files:
        w0, h0 = Image.open(f).size
        th = int(h0 * min(1.0, (a.width - 20) / w0)) + 44
        if cur and (len(cur) >= a.per or h + th > MAX_H):
            chunks.append(cur)
            cur, h = [], 10
        cur.append(f)
        h += th
    if cur:
        chunks.append(cur)
    for sheet_no, chunk in enumerate(chunks):
        tiles = []
        for f in chunk:
            im = Image.open(f).convert("RGB")
            scale = min(1.0, (a.width - 20) / im.width)
            im = im.resize((int(im.width * scale), int(im.height * scale)))
            tiles.append((f.stem[len(a.prefix) + 1:], Image.open(f).size, im))
        h = sum(t[2].height + 44 for t in tiles) + 10
        sheet = Image.new("RGB", (a.width, h), "white")
        d = ImageDraw.Draw(sheet)
        y = 5
        for label, size, im in tiles:
            d.rectangle([0, y, a.width, y + 32], fill=(30, 60, 120))
            d.text((10, y + 4), f"{label}   ({size[0]}x{size[1]} px)", fill="white", font=font)
            y += 36
            sheet.paste(im, (10, y))
            d.rectangle([9, y - 1, 10 + im.width, y + im.height], outline=(170, 170, 170))
            y += im.height + 8
        sheet.save(f"{a.out}_{sheet_no + 1:02d}.jpg", quality=88)
    print(f"{len(files)} crops -> {len(chunks)} sheets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
