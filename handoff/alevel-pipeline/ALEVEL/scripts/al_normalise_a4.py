#!/usr/bin/env python3
"""Normalise A3-sized canonical sources to A4 (in place, original kept).

A few 2015-16 papers are distributed as A3 pages (842 x 1191 pt) holding the
uniformly enlarged A4 layout; every splitter works in A4 points.  Each page is
placed, scaled by 595.28/842, on an A4 page (vector + text preserved: a form
XObject).  The original moves to source_papers/canonical_original/ and a row
is appended to derived_sources.csv (parent sha256 -> derived sha256).

Usage: al_normalise_a4.py FILE.pdf ...      (names inside canonical/)
"""
import csv, hashlib, shutil, sys
from pathlib import Path
import pymupdf as fitz

SRC = Path.home() / "rootatom_data" / "ALEVEL" / "source_papers"
A4 = fitz.paper_rect("a4")


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    orig_dir = SRC / "canonical_original"
    orig_dir.mkdir(exist_ok=True)
    for name in sys.argv[1:]:
        cur = SRC / "canonical" / name
        src = fitz.open(cur)
        if all(abs(p.rect.width - A4.width) < 2 for p in src):
            print(name, "already A4"); continue
        if not all(abs(p.rect.width / p.rect.height - A4.width / A4.height) < 0.01 for p in src):
            print(name, "not an A-series page: left alone"); continue
        out = fitz.open()
        for i in range(src.page_count):
            out.new_page(width=A4.width, height=A4.height).show_pdf_page(A4, src, i)
        keep = orig_dir / name
        shutil.move(cur, keep)
        out.save(cur, garbage=3, deflate=True)
        with open(SRC / "derived_sources.csv", "a", newline="") as fh:
            csv.writer(fh).writerow([name, f"canonical_original/{name}", sha(keep), f"1-{src.page_count}",
                                     sha(cur), "A3 page size scaled to A4 (x0.7071), vector"])
        print(name, "->", "A4", src.page_count, "pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
