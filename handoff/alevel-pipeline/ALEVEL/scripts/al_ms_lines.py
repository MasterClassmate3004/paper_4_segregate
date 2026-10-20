#!/usr/bin/env python3
"""Text rows of a mark-scheme page in the splitter's own coordinates.

al_ms_splitter.py removes page rotation before reading words (landscape
2018+ mark schemes), so overrides must use the derotated coordinates this
tool prints: one row per line, 'y0 y1 x0 text' in points, page 1-based.
With --png OUT it also saves a 70 dpi picture of the derotated page.

Usage: al_ms_lines.py MS_PDF PAGE [--png OUT.png]
"""

from __future__ import annotations

import sys
from pathlib import Path

import pymupdf as fitz

CANON = Path.home() / "rootatom_data" / "ALEVEL" / "source_papers" / "canonical"


def main() -> int:
    src, page = sys.argv[1], int(sys.argv[2])
    doc = fitz.open(src if Path(src).exists() else CANON / src)
    pg = doc[page - 1]
    if pg.rotation:
        pg.remove_rotation()
    rows: list[list] = []
    for w in sorted(pg.get_text("words"), key=lambda w: (w[1] + w[3]) / 2):
        yc = (w[1] + w[3]) / 2
        if rows and yc - rows[-1][0] <= 4:
            rows[-1][1].append(w)
        else:
            rows.append([yc, [w]])
    for _, ws in rows:
        ws.sort(key=lambda w: w[0])
        print(f"{min(w[1] for w in ws):7.1f} {max(w[3] for w in ws):7.1f} {ws[0][0]:6.1f}  "
              + " ".join(w[4] for w in ws))
    if "--png" in sys.argv:
        pg.get_pixmap(dpi=70).save(sys.argv[sys.argv.index("--png") + 1])
    return 0


if __name__ == "__main__":
    sys.exit(main())
