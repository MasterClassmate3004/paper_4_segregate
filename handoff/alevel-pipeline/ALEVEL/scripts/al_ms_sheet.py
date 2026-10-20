#!/usr/bin/env python3
"""Paired QP | MS contact sheets (visual gate for mark-scheme splitting).

One entry per QP leaf: the label and mapping status, the QP crop on the left
and its MS crop on the right, both framed in grey so edges are visible.
Sheets: <OUT_BASE>_01.jpg, _02.jpg, ...

Usage: al_ms_sheet.py MS_DIR MS_PREFIX QP_DIR QP_PREFIX OUT_BASE [--per 8] [--width 1600]
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def fit(im: Image.Image, w: int) -> Image.Image:
    if im.width > w:
        im = im.resize((w, max(1, round(im.height * w / im.width))), Image.LANCZOS)
    return im


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("ms_dir")
    ap.add_argument("ms_prefix")
    ap.add_argument("qp_dir")
    ap.add_argument("qp_prefix")
    ap.add_argument("out")
    ap.add_argument("--per", type=int, default=8)
    ap.add_argument("--width", type=int, default=1600)
    a = ap.parse_args()
    prov = json.load(open(Path(a.ms_dir) / f"{a.ms_prefix}-ms-provenance.json"))
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 22)
    except OSError:
        font = ImageFont.load_default()
    half = (a.width - 30) // 2
    entries = []
    shown = {}                     # MS file -> first label it was shown for
    CH = 2200                      # max MS chunk height on a sheet (px), keeps sheets legible
    for label, m in prov["mapping"].items():
        qp = fit(Image.open(Path(a.qp_dir) / f"{a.qp_prefix}-{label}.png").convert("RGB"), half)
        st, keys = m["status"], ",".join(m["ms_keys"])
        f = m.get("file")
        dk = tuple(m["ms_keys"])       # same MS rows -> same image
        if f and dk in shown:       # identical MS crop already shown (parent covers children)
            ms_parts = [None]
            note = f"same MS crop as {shown[dk]}"
        else:
            ms = fit(Image.open(Path(a.ms_dir) / f).convert("RGB"), half) if f else \
                Image.new("RGB", (half, 60), (255, 220, 220))
            if f:
                shown[dk] = label
            ms_parts = [ms.crop((0, y, ms.width, min(ms.height, y + CH))) for y in range(0, ms.height, CH)]
            note = ""
        for i, ms in enumerate(ms_parts):
            q = qp if i == 0 else None
            hq = q.height if q else 0
            hm = ms.height if ms else 30
            h = 34 + max(hq, hm) + 16
            tile = Image.new("RGB", (a.width, h), "white")
            d = ImageDraw.Draw(tile)
            part = f"  (MS part {i + 1}/{len(ms_parts)})" if len(ms_parts) > 1 else ""
            d.text((8, 4), f"{label}   [{st}]   MS: {keys}{part}",
                   fill=(0, 0, 0) if st == "exact" else (200, 0, 0), font=font)
            if q:
                tile.paste(q, (10, 34))
                d.rectangle([9, 33, 10 + q.width, 34 + q.height], outline=(150, 150, 150))
            if ms:
                tile.paste(ms, (20 + half, 34))
                d.rectangle([19 + half, 33, 20 + half + ms.width, 34 + ms.height], outline=(150, 150, 150))
            else:
                d.text((24 + half, 40), note, fill=(0, 0, 160), font=font)
            d.line([(0, h - 2), (a.width, h - 2)], fill=(60, 60, 200), width=2)
            entries.append(tile)
    # pack by height (and at most --per tiles) so no sheet is too tall to read
    sheets, cur, hcur = [], [], 0
    for t in entries:
        if cur and (hcur + t.height > 4200 or len(cur) >= a.per):
            sheets.append(cur)
            cur, hcur = [], 0
        cur.append(t)
        hcur += t.height
    if cur:
        sheets.append(cur)
    for k, chunk in enumerate(sheets):
        sheet = Image.new("RGB", (a.width, sum(t.height for t in chunk)), "white")
        y = 0
        for t in chunk:
            sheet.paste(t, (0, y))
            y += t.height
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        sheet.save(f"{a.out}_{k + 1:02d}.jpg", quality=85)
    print(f"{len(prov['mapping'])} leaves -> {len(sheets)} sheets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
