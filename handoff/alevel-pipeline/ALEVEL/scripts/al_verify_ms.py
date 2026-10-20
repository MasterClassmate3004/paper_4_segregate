#!/usr/bin/env python3
"""Independent coverage gate for a split mark scheme.

Reads only the MS source and the splitter's provenance (segment rectangles,
masks, recorded drops).  On every page from the first to the last segment
page, each word must be either
  * furniture: running header block, footer, a Question|Answer|Mark(s)
    column-header row, a whited-out mask (key labels, Section/Option headings,
    [Total] lines), or inside a recorded dropped preamble/appendix slice; or
  * inside exactly one MS segment rectangle (centre test).
Also: no segment edge slices a word (a word straddling a segment's top or
bottom edge by more than 2 pt on both sides), and no two different segments
overlap.  Words left of every segment on a page (the key column) count as
furniture only if they are key labels (masked).

Prints 'pages A-B: missing=M duplicated=D sliced=S overlaps=O' and the first
offenders; the runner treats 0/0/0/0 as pass.

Usage: al_verify_ms.py MS_PDF MS_DIR PREFIX
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import numpy as np
import pymupdf as fitz

HEAD_WORDS = {"Page", "Mark", "Scheme", "Scheme:", "Syllabus", "Paper", "PUBLISHED", "GCE",
              "Cambridge", "International", "Teachers’", "version"}
FOOT = re.compile(r"^(©|&|UCLES|Cambridge|University|Press|Assessment|International|Examinations|"
                  r"of|Page|\d{1,4}|\[Turn|over\]?|\d{4}/\d{1,2}(/.*)?|Local|Examinations|Syndicate)$")


def rows(ws, tol=4.0):
    out = []
    for w in sorted(ws, key=lambda w: (w[1] + w[3]) / 2):
        yc = (w[1] + w[3]) / 2
        if out and yc - out[-1][0] <= tol:
            out[-1][1].append(w)
        else:
            out.append([yc, [w]])
    return [r[1] for r in out]


def inside(w, r, tol=0.6) -> bool:
    cx, cy = (w[0] + w[2]) / 2, (w[1] + w[3]) / 2
    return r[0] - tol <= cx <= r[2] + tol and r[1] - tol <= cy <= r[3] + tol


def main() -> int:
    src, d, prefix = sys.argv[1:4]
    prov = json.load(open(Path(d) / f"{prefix}-ms-provenance.json"))
    if prov.get("kind") == "mcq_key":
        print("pages -: missing=0 duplicated=0 sliced=0 overlaps=0 furniture=0 (mcq key)")
        return 0
    doc = fitz.open(src)
    for p in doc:
        if p.rotation:
            p.remove_rotation()
    segs = []                                   # (key, page0, rect)
    for key, ss in prov["segments"].items():
        for s in ss:
            segs.append((key, s["pdf_page"] - 1, s["clip_points"]))
    masks = [(m[0], m[1:5]) for m in prov.get("masks", [])]
    dropped = []
    for a in prov.get("dropped_appendix", {}).values():
        for pno, y0, y1 in a["slices"]:
            dropped.append((pno, [0, y0, 1e4, y1]))
    pages = sorted({s[1] for s in segs})
    if not pages:
        print("pages -: missing=0 duplicated=0 sliced=0 overlaps=0 furniture=0 (no segments)")
        return 1
    pre_txt = " ".join(prov.get("dropped_preamble", {}).values()).split()
    missing, dup, sliced, overlaps, furniture = [], [], [], [], []
    grays = {}

    def ink_both_sides(pno, w, edge):
        """a word box straddling an edge is sliced only if its INK lies on both
        sides (superscript boxes overlap the neighbouring line without ink there)"""
        if pno not in grays:
            pix = doc[pno].get_pixmap(dpi=144, colorspace=fitz.csGRAY)
            grays[pno] = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width)
        g, sc = grays[pno], 2.0
        x0, x1 = int(w[0] * sc), int(w[2] * sc) + 1
        e = int(edge * sc)
        above = g[max(0, int(w[1] * sc)):max(0, e - 1), x0:x1]
        below = g[e + 1:int(w[3] * sc) + 1, x0:x1]
        # a glyph tip of under 2 pt on one side (touching lines in old layouts) is not a slice
        ra = np.where((above < 160).any(axis=1))[0]
        rb = np.where((below < 160).any(axis=1))[0]
        return len(ra) and len(rb) and (above.shape[0] - ra[0]) >= 4 and (rb[-1] + 1) >= 4
    for pno in range(pages[0], pages[-1] + 1):
        pg = doc[pno]
        ps = [s for s in segs if s[1] == pno]
        if not ps:
            continue                            # a page of another component / blank page
        ws = [w for w in pg.get_text("words") if w[4].strip()]
        if len(ws) < 5 and pg.get_images():          # scanned page: OCR words
            tp = pg.get_textpage_ocr(dpi=300, full=True, tessdata="/opt/homebrew/share/tessdata")
            ws = [w for w in pg.get_text("words", textpage=tp) if w[4].strip()]
            pb = float(prov.get("overrides", {}).get("page_bottom", {}).get(str(pno + 1), pg.rect.height - 70))
            furn_band = [w for w in ws if w[1] < 72 or w[1] > max(pg.rect.height - 70, pb)]   # garbled header/footer
            ocr_page = True
        else:
            furn_band = []
            ocr_page = False
        h = pg.rect.height
        furn = {id(w) for w in furn_band}
        for r in rows([w for w in ws if w[1] < 90]):
            if any(w[4] in HEAD_WORDS for w in r) or any(re.match(r"^9\d{3}(/\d\d)?$", w[4]) for w in r):
                furn.update(id(w) for w in r)
        pbo = prov.get("overrides", {}).get("page_bottom", {}).get(str(pno + 1))
        for r in rows([w for w in ws if w[1] > h - 80 and (pbo is None or w[1] > float(pbo))]):
            # a lone mark '1' low on a landscape page is not the footer
            if all(FOOT.match(w[4]) for w in r) and (any(not re.fullmatch(r"\d", w[4]) for w in r)
                                                     or min(w[1] for w in r) > h - 40):
                furn.update(id(w) for w in r)
        head_tops = []
        for r in rows(ws):
            t = {w[4] for w in r}
            if re.match(r"^(Part\s+)?Mark\s+Expected\s+Answer(\s+Additional\s+Guidance)?$",
                        " ".join(w[4] for w in sorted(r, key=lambda w: w[0]))):
                furn.update(id(w) for w in r)       # Paper 5 table column headings
        # header rows: 'Question' may sit 6 pt below 'Answer Mark' (9701/41/O/N/16)
        for r in rows(ws, tol=7.0):
            t = {w[4].lower() for w in r}
            if "question" in t and t & {"answer", "answers", "marking"} and t & {"marks", "mark"} and len(r) <= 6:
                furn.update(id(w) for w in r)
                head_tops.append(min(w[1] for w in r))
        if head_tops:       # notes printed above a page's first answer table (marking notation)
            furn.update(id(w) for w in ws if w[3] <= min(head_tops) + 0.5)
        for w in ws:
            if id(w) in furn:
                if any(inside(w, r) for _, _, r in ps) and not any(
                        m[0] == pno and inside(w, m[1], 1.0) for m in masks):
                    furniture.append((pno + 1, round(w[1]), w[4]))
                continue
            if any(m[0] == pno and inside(w, m[1], 1.0) for m in masks):
                continue
            if any(dp == pno and inside(w, r) for dp, r in dropped):
                continue
            if ocr_page and w[0] < 110 and re.fullmatch(r"\(?\d{0,2}\)?\s*\(?[a-h]?\)?\s*\(?[ivx]{1,4}\)?\d?\.?|\(?[a-h]\)", w[4]):
                continue                    # scans: a key label (removed by design) placed loosely by OCR
            if ocr_page and re.fullmatch(r"[.,'`_|:;\-~\\—–o]+", w[4]):
                continue                    # scan specks read as punctuation
            hits = {k for k, _, r in ps if inside(w, r)}
            rects = {tuple(r) for _, _, r in ps if inside(w, r)}   # one slice shared by several parts is fine
            if not hits:
                if w[4] in pre_txt:
                    pre_txt.remove(w[4])
                    continue
                missing.append((pno + 1, round(w[1]), w[4]))
            elif len(rects) > 1 and not (ocr_page and any(
                    abs((w[1] + w[3]) / 2 - e) < 1.5 for r in rects for e in (r[1], r[3]))):
                dup.append((pno + 1, round(w[1]), w[4], sorted(hits)))
            if furn_band is not None and ocr_page:
                continue                    # scans: slicing is checked on pixels below
            for k, _, r in ps:
                if r[0] - 1 < (w[0] + w[2]) / 2 < r[2] + 1:
                    for edge in (r[1], r[3]):
                        if w[1] + 2 < edge < w[3] - 2 and ink_both_sides(pno, w, edge):
                            sliced.append((pno + 1, round(w[1]), w[4], k))
        if ocr_page:
            # a segment edge on a scan is sliced if its pixel row carries ink
            if pno not in grays:
                pix = doc[pno].get_pixmap(dpi=144, colorspace=fitz.csGRAY)
                grays[pno] = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width)
            g = grays[pno]
            for k, _, r in ps:
                for edge in (r[1], r[3]):
                    yy = int(edge * 2)
                    if any(m[0] == pno and m[1][1] - 1 <= edge <= m[1][3] + 1 for m in masks):
                        continue            # the edge runs through a whited-out heading/label
                    if 0 <= yy < g.shape[0] and (g[yy, int(r[0] * 2):int(r[2] * 2)] < 150).sum() > 20:
                        sliced.append((pno + 1, round(edge), "pixel row", k))
        for i, (k1, _, r1) in enumerate(ps):
            for k2, _, r2 in ps[i + 1:]:
                if k1 != k2 and tuple(r1) != tuple(r2) and min(r1[3], r2[3]) - max(r1[1], r2[1]) > 1.5 and \
                        min(r1[2], r2[2]) - max(r1[0], r2[0]) > 1.5:
                    overlaps.append((pno + 1, k1, k2))
    acc = prov.get("overrides", {}).get("accept_sliced", {})     # recorded, with a reason
    sliced = sorted(set(x for x in sliced if x[3] not in acc))
    print(f"pages {pages[0] + 1}-{pages[-1] + 1}: missing={len(missing)} duplicated={len(dup)} "
          f"sliced={len(sliced)} overlaps={len(overlaps)} furniture={len(furniture)}")
    for name, lst in (("MISSING", missing), ("DUP", dup), ("SLICED", sliced), ("OVERLAP", overlaps), ("FURNITURE", furniture)):
        for x in lst[:8]:
            print(" ", name, x)
    return 0


if __name__ == "__main__":
    sys.exit(main())
