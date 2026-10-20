#!/usr/bin/env python3
"""Render a source page with every crop rectangle drawn on it (debug aid).

Usage: al_overlay.py RUN PREFIX PAGE OUT.png [--dpi 70]
Each crop's clip is outlined in a colour and labelled at its top-left.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pymupdf as fitz

DATA = Path.home() / "rootatom_data" / "ALEVEL"
COLOURS = [(1, 0, 0), (0, 0.5, 1), (0, 0.6, 0), (0.8, 0, 0.8), (1, 0.5, 0)]


def main() -> int:
    run, prefix, page, out = sys.argv[1:5]
    dpi = int(sys.argv[sys.argv.index("--dpi") + 1]) if "--dpi" in sys.argv else 70
    prov = json.load(open(DATA / "splits" / run / prefix / f"{prefix}-split-provenance.json"))
    doc = fitz.open(prov["source_pdf"])
    pg = doc[int(page) - 1]
    k = 0
    for label, segs in prov["outputs"].items():
        for s in segs:
            if s["pdf_page"] != int(page):
                continue
            r = fitz.Rect(s["clip_points"])
            c = COLOURS[k % len(COLOURS)]
            pg.draw_rect(r, color=c, width=1.2)
            pg.insert_text((r.x0 + 2, r.y0 + 7), label, fontsize=7, color=c)
            k += 1
    pg.get_pixmap(dpi=dpi).save(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
