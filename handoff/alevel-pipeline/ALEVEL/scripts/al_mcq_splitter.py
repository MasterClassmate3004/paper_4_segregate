#!/usr/bin/env python3
"""Split a Cambridge A Level multiple-choice paper (Paper 1) into one PNG per question.

Method (from the igcse-mcq-cropper skill, adapted to the A Level contract):
  * question starts: first token of a row is the next expected number
    (1..N, strictly sequential) in the question column (x 40-60 pt);
  * a question runs to just above the next question's row on the same page;
    the last question on a page runs to the measured footer line, and any
    content at the top of following pages before the next question number
    (options/figure pushed over a page break) is appended as more segments;
  * page furniture (barcode font, caption, margin strips, '[Total: n]') is
    painted white in memory with the same safety checks as al_qp_splitter;
  * the question number is NOT shown: its glyphs are painted white in memory
    (checked to cover nothing else);
  * every segment edge is snapped onto a blank pixel row (majority rule),
    crops are rendered at 220 dpi, outer whitespace trimmed to an even pad,
    multi-segment questions stacked with a small gap.

Writes <PREFIX>-Q<n>.png and <PREFIX>-split-provenance.json (same schema as
al_qp_splitter, so al_verify_leaves / al_verify_coverage apply unchanged).

Usage: al_mcq_splitter.py SOURCE.pdf OUT_DIR PREFIX [--expected 40]
Any doubt raises REVIEW_REQUIRED (exit 1); nothing is guessed.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np
import pymupdf as fitz

sys.path.insert(0, str(Path(__file__).resolve().parent))
from barcode_rule import is_barcode_span  # noqa: E402
from PIL import Image

DPI = 220
SNAP_DPI = 200
CONTENT_L, CONTENT_R = 40.0, 560.0
HEADER_Y = 40.0
Q_COL = (40.0, 60.0)
PAD_PX = 18
BARCODE_CAPTION_RE = re.compile(r"^\*\s*\d{6,}\s*\*$")
MARGIN_STRIP_RE = re.compile(r"DO NOT WRITE IN THIS MARGIN", re.I)
TOTAL_LINE_RE = re.compile(r"^\[Total:\s*\d+\]$")
WORKING_RE = re.compile(r"^Space for working\.?$", re.I)   # 2010s MCQ answer-area label
FOOTER_RE = re.compile(r"UCLES|©|^\d{4}/\d{1,2}/|^\[?Turn$|^over$")


class Review(RuntimeError):
    pass


def gray(page: fitz.Page, dpi: int) -> np.ndarray:
    pm = page.get_pixmap(dpi=dpi, colorspace=fitz.csGRAY, alpha=False)
    return np.frombuffer(pm.samples, np.uint8).reshape(pm.height, pm.width)


def footer_line(doc: fitz.Document) -> float:
    tops = []
    for page in list(doc)[1:]:
        ys = [w[1] for w in page.get_text("words") if w[1] > 740 and FOOTER_RE.search(w[4])]
        # 2025+: corner crop-marks / QR glyphs start above the footer text
        ys += [d["rect"].y0 for d in page.get_drawings() if d.get("rect") is not None
               and d["rect"].y0 > 780 and d["rect"].y1 < 842]
        ys += [sp["bbox"][1] for b in page.get_text("dict")["blocks"] for l in b.get("lines", [])
               for sp in l["spans"] if is_barcode_span(sp["text"], sp["bbox"][1], sp["bbox"][3])
               and sp["bbox"][1] > 780]
        if ys:
            tops.append(min(ys))
    if not tops:
        return 782.0
    tops.sort()
    return max(782.0, min(798.0, tops[len(tops) // 2] - 3))


def mask_rects(page: fitz.Page, rects: list[fitz.Rect], allowed_words: list[fitz.Rect]) -> None:
    """Paint rects white; every touched word must be in allowed_words; render
    must be unchanged outside the rects (same contract as al_qp_splitter)."""
    if not rects:
        return
    for w in page.get_text("words"):
        wr = fitz.Rect(w[:4])
        if wr.y0 > 790 or wr.y1 < 72 or wr.x1 < 35 or wr.x0 > 560:
            continue
        if any(wr.intersects(r) for r in rects):
            c = fitz.Point((w[0] + w[2]) / 2, (w[1] + w[3]) / 2)
            if not any(a.contains(c) for a in allowed_words):
                raise Review(f"mask would cover content word {w[4]!r} on page {page.number + 1}")
    before = gray(page, 100)
    for r in rects:
        page.draw_rect(r, color=None, fill=(1, 1, 1), overlay=True)
    after = gray(page, 100)
    allowed = np.zeros_like(before, dtype=bool)
    k = 100 / 72
    for r in rects:
        allowed[max(0, int(r.y0 * k) - 2):int(r.y1 * k) + 3, max(0, int(r.x0 * k) - 2):int(r.x1 * k) + 3] = True
    if ((before != after) & ~allowed).any():
        raise Review(f"mask changed content on page {page.number + 1}")


def mask_furniture(page: fitz.Page) -> None:
    rects, fspans = [], []
    for block in page.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            ltxt = "".join(sp["text"] for sp in line["spans"]).strip()
            if TOTAL_LINE_RE.match(ltxt):            # split over spans (2025+)
                lb = fitz.Rect(line["bbox"]) + (-1, -1, 1, 1)
                fspans.append(lb)
                rects.append(lb)
                continue
            for span in line["spans"]:
                text, bbox = span["text"].strip(), fitz.Rect(span["bbox"])
                barcode = is_barcode_span(span["text"], bbox.y0, bbox.y1)
                other = ((BARCODE_CAPTION_RE.match(text) and bbox.y1 < 78)
                         or (MARGIN_STRIP_RE.search(text) and (bbox.x1 < 35 or bbox.x0 > 560))
                         or TOTAL_LINE_RE.match(text) or WORKING_RE.match(text))
                if barcode or other:
                    fspans.append(bbox + (-1, -1, 1, 1))
                if barcode:
                    rects.append(fitz.Rect(bbox.x0 - 2, 18, bbox.x1 + 2, bbox.y1 + 1.5) if bbox.y1 < 100
                                 else bbox + (-1, -1, 1, 1))
                elif other:
                    rects.append(bbox + (-1, -1, 1, 1))
    mask_rects(page, rects, fspans)


def page_bottom(page: fitz.Page, footer: float) -> float:
    """Content limit for a page: the footer line, or above Cambridge's
    copyright-acknowledgement block when the page carries it."""
    ws = page.get_text("words")
    tops = [w[1] for w in ws if (w[4] == "Permission" and any(v[4] == "reproduce" and abs(v[1] - w[1]) < 3 for v in ws))
            or (w[4] == "To" and any(v[4] == "disclosure" and abs(v[1] - w[1]) < 3 for v in ws))
            or w[4] == "Acknowledgements:"
            # 2004 wording: 'Every reasonable effort has been made to trace ...'
            or (w[4] == "Every" and w[1] > 600 and any(v[4] == "reasonable" and abs(v[1] - w[1]) < 3 for v in ws))
            or (w[4] == "University" and w[1] > 650 and any(v[4] == "Examinations" and abs(v[1] - w[1]) < 12 for v in ws))
            or (w[4] == "University" and any(v[4] == "Syndicate" and abs(v[1] - w[1]) < 12 for v in ws)
                and w[1] > 600)]          # 'Copyright Acknowledgements:' credit block (12/M/J/13)
    if tops:
        rules = [d["rect"].y0 for d in page.get_drawings()
                 if d.get("rect") is not None and d["rect"].height < 2 and d["rect"].width > 300
                 and min(tops) - 30 < d["rect"].y0 < min(tops)]
        return min(rules + [min(tops)]) - 1.5   # 6 pt cut the bottom of a figure (9702/12/M/J/20 Q40)
    return footer


def find_questions(doc: fitz.Document, footer: float, expected: int) -> list[dict]:
    """Sequential question numbers in the question column with text beside them.

    Rows are matched by baseline proximity (|dy| < 3 pt), not fixed 3 pt
    buckets: '24' at y=346.5 and its stem at y=346.8 fell into different
    buckets in 9702/12/M/J/13 and the number looked alone on its row.
    """
    found, nxt = [], 1
    qfonts: dict = {}               # (font, size) of numbers that have text beside them
    for pno in range(1, doc.page_count):
        words = [w for w in doc[pno].get_text("words")
                 if HEADER_Y <= w[1] < footer and 35 <= w[0] <= 565]   # skip margin strips
        spans = [(fitz.Rect(sp["bbox"]), sp["font"], round(sp["size"], 1))
                 for b in doc[pno].get_text("dict")["blocks"] for ln in b.get("lines", []) for sp in ln["spans"]]

        def font_of(w):
            c = fitz.Point((w[0] + w[2]) / 2, (w[1] + w[3]) / 2)
            return next(((f, z) for r, f, z in spans if r.contains(c)), None)
        for w in sorted(words, key=lambda w: (w[1], w[0])):
            if not (w[4].isdigit() and int(w[4]) == nxt and Q_COL[0] <= w[0] <= Q_COL[1]):
                continue
            beside = [v for v in words if v is not w and abs(v[1] - w[1]) < 3 and v[0] > w[2]]
            left = [v for v in words if v is not w and abs(v[1] - w[1]) < 3 and v[2] <= w[0] + 0.5]
            if left:
                continue
            if beside:
                fk = font_of(w)
                qfonts[fk] = qfonts.get(fk, 0) + 1
            # a question that opens with a diagram has its number alone on the
            # row (9701/01/O/N/04 Q13): accept it in the question-number font
            elif not (qfonts and font_of(w) == max(qfonts, key=qfonts.get)):
                continue
            found.append({"q": nxt, "pno": pno, "y": min([w[1]] + [v[1] for v in beside]),
                          "num_bbox": fitz.Rect(w[:4])})
            nxt += 1
    if len(found) != expected:
        raise Review(f"found {len(found)} question numbers, expected {expected}")
    return found


def page_has_content(img: np.ndarray, y0: float, y1: float) -> bool:
    k = SNAP_DPI / 72
    band = img[int(y0 * k):int(y1 * k), int(CONTENT_L * k):int(CONTENT_R * k)]
    return bool((band < 235).any())


def snap(img: np.ndarray, y0: float, y1: float, pno: int = -1) -> tuple[float, float]:
    k = SNAP_DPI / 72
    inked = (img[:, int(CONTENT_L * k):int(CONTENT_R * k)] < 235).any(axis=1)

    def run(row, limit=14):
        a = b = row
        while a > 0 and inked[a - 1]:
            a -= 1
        while b < len(inked) - 1 and inked[b + 1]:
            b += 1
        if (b - a) / k > limit:
            raise Review(f"no blank row near y={row / k:.1f} on page {pno + 1}")
        return a, b
    r0, r1 = int(round(y0 * k)), int(round(y1 * k))
    if 0 <= r0 < len(inked) and inked[r0]:
        # a question's TOP edge cuts its own first line: a stacked fraction
        # ('What is the ratio 1um/1Gm ?', 9702/1/M/J/07 Q2) makes that line
        # one 20-25 pt ink run.  Keep the whole run in this question; the
        # gate's duplicate-word check guards the previous question.
        a, b = run(r0, limit=40)
        y0 = (a - 1) / k
    if 0 <= r1 < len(inked) and inked[r1]:
        # the BOTTOM edge sits 4 pt above the next number row, which can be
        # inside the next question's raised fraction: a run reaching far
        # below the edge belongs to that next question -> stop above it
        a, b = run(r1, limit=40)
        if (b - a) / k > 14 and (b - r1) > (r1 - a) and (a - 1) / k > y0 + 2:
            y1 = (a - 1) / k
        elif (b - a) / k > 14:
            raise Review(f"no blank row near y={r1 / k:.1f} on page {pno + 1}")
        else:
            y1 = (b + 1) / k if (r1 - a) >= (b - r1) else (a - 1) / k
    return y0, y1


def tighten(img: np.ndarray, y0: float, y1: float) -> tuple[float, float] | None:
    """Shrink [y0,y1] to the ink inside it (None if blank)."""
    k = SNAP_DPI / 72
    band = img[int(y0 * k):int(y1 * k), int(CONTENT_L * k):int(CONTENT_R * k)]
    rows = np.where((band < 235).any(axis=1))[0]
    if not len(rows):
        return None
    return y0 + (rows[0] - 1) / k, y0 + (rows[-1] + 2) / k


def x_extent(page: fitz.Page, y0: float, y1: float) -> tuple[float, float]:
    """Crop width: the 40-560 pt column, widened to content that sits outside
    it (options/diagrams up to ~575 pt: 9702/11/M/J/15 Q39); never into the
    margin-strip zone; our own white masks are ignored."""
    xs = [(w[0], w[2]) for w in page.get_text("words")
          if y0 <= (w[1] + w[3]) / 2 <= y1 and w[0] >= 18 and w[2] <= 577]
    xs += [(d["rect"].x0, d["rect"].x1) for d in page.get_drawings()
           if d.get("rect") is not None and y0 <= d["rect"].y0 and d["rect"].y1 <= y1
           and d["rect"].x0 >= 18 and d["rect"].x1 <= 577
           and not (d.get("fill") in ((1, 1, 1), (1.0, 1.0, 1.0)) and d.get("color") is None)]
    if not xs:
        return CONTENT_L, CONTENT_R
    return min(CONTENT_L, min(a for a, _ in xs) - 2), max(CONTENT_R, max(b for _, b in xs) + 2)


def render(page: fitz.Page, y0: float, y1: float) -> Image.Image:
    xl, xr = x_extent(page, y0, y1)
    pm = page.get_pixmap(clip=fitz.Rect(xl, y0, xr, y1), dpi=DPI, alpha=False)
    im = Image.frombytes("RGB", (pm.width, pm.height), pm.samples)
    a = np.asarray(im.convert("L"))
    rows = np.where((a < 220).any(axis=1))[0]
    if not len(rows):
        raise Review("empty segment render")
    top, bot = max(0, rows[0] - PAD_PX), min(im.height, rows[-1] + PAD_PX + 1)
    im = im.crop((0, top, im.width, bot))
    out = Image.new("RGB", (im.width, im.height + max(0, PAD_PX - rows[0]) ), "white")
    out.paste(im, (0, max(0, PAD_PX - rows[0])))
    return out


SECB_RE = re.compile(r"^Section B$")
REF_PAGE_RE = re.compile(r"Important\s*values,?\s*constants\s*and\s*standards|The\s*Periodic\s*Table|oganesson|"
                         r"Permission\s*to\s*reproduce", re.I)
KEY_START_RE = re.compile(r"^The responses A to D should be selected on the basis of")
KEY_END_RE = re.compile(r"^No other combination of statements is used as a (?:correct|single) response\.?$")


def section_b(doc: fitz.Document) -> tuple[tuple | None, dict]:
    """Pre-2016 9701 Paper 1 Section B (Q31-40, multiple-statement items).

    Returns ((pno, y) of the 'Section B' heading or None, {pno: y below the
    repeated 'The responses A to D ...' key block printed at the top of later
    Section B pages}).  The heading block (instructions + A-D key) is shared
    context for every Section B question -> its own SecB.stem crop; the
    repeated key is page boilerplate and is left out of continuation crops.
    """
    head, key_end = None, {}
    for pno in range(1, doc.page_count):
        rows: dict[int, list] = {}
        for w in doc[pno].get_text("words"):
            rows.setdefault(round(w[1] / 3), []).append(w)
        ordered = sorted(rows.values(), key=lambda ws: min(v[1] for v in ws))
        texts = [(" ".join(v[4] for v in sorted(ws, key=lambda v: v[0])), min(v[1] for v in ws), max(v[3] for v in ws))
                 for ws in ordered]
        for t, y0, _ in texts:
            if head is None and SECB_RE.match(t):
                head = (pno, y0)
        if head and pno != head[0]:
            # the key alone (2006) or the whole Section B block (2012) is
            # reprinted at the top of every later Section B page
            starts = [y0 for t, y0, _ in texts if (KEY_START_RE.match(t) or SECB_RE.match(t)) and y0 < 140]
            if starts:
                ends = [y1 for t, y0, y1 in texts if KEY_END_RE.match(t) and y0 > starts[0]]
                if ends:
                    key_end[pno] = ends[0]
    return head, key_end


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("out")
    ap.add_argument("prefix")
    ap.add_argument("--expected", type=int, default=40)
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(a.src)
    try:
        footer = footer_line(doc)
        secb, key_end = section_b(doc)
        for page in doc:
            mask_furniture(page)
        qs = find_questions(doc, footer, a.expected)
        # hide question numbers (each must cover only its own number)
        by_page: dict[int, list] = {}
        for q in qs:
            by_page.setdefault(q["pno"], []).append(q)
        for pno, items in by_page.items():
            mask_rects(doc[pno], [q["num_bbox"] + (-1, -1, 1, 1) for q in items],
                       [q["num_bbox"] + (-1, -1, 1, 1) for q in items])
        imgs = {}

        def img(p):
            if p not in imgs:
                imgs[p] = gray(doc[p], SNAP_DPI)
            return imgs[p]

        prov = {}
        for i, q in enumerate(qs):
            nq = qs[i + 1] if i + 1 < len(qs) else None
            segs = []
            p = q["pno"]
            y_end = (nq["y"] - 4) if (nq and nq["pno"] == p) else page_bottom(doc[p], footer)
            if secb and secb[0] == p and q["y"] < secb[1] < y_end + 4:
                y_end = secb[1] - 4                    # Section B heading ends Q30
            segs.append((p, q["y"] - 4, y_end))
            if not (nq and nq["pno"] == p) and not (secb and secb[0] == p and q["y"] < secb[1]):
                last_p = nq["pno"] if nq else doc.page_count - 1
                for cp in range(p + 1, last_p + 1):
                    # 2022+ papers append data pages (constants, IR table,
                    # Periodic Table): never part of the last question
                    t_ = doc[cp].get_text()
                    t_ += "".join(chr(ord(c) + 29) if 3 <= ord(c) <= 98 else c for c in t_)   # -29 shifted subset font (9701/12/M/J/23)
                    if REF_PAGE_RE.search(t_):
                        break
                    bottom = page_bottom(doc[cp], footer)      # above any copyright notice
                    top = max(HEADER_Y + 18, key_end.get(cp, 0) + 4)   # below a repeated A-D key
                    body = {w[4] for w in doc[cp].get_text("words")
                            if top <= w[1] < bottom and 35 <= w[0] <= 565}
                    if body <= {"BLANK", "PAGE"}:
                        continue                       # blank page
                    lim = (nq["y"] - 4) if (nq and cp == nq["pno"]) else page_bottom(doc[cp], footer)
                    if secb and cp == secb[0]:
                        lim = min(lim, secb[1] - 4)    # Section B starts on this page
                    if lim - top > 2 and page_has_content(img(cp), top, lim):
                        segs.append((cp, top, lim))
                    if secb and cp == secb[0]:
                        break
            final = []
            for p2, y0, y1 in segs:
                t = tighten(img(p2), y0, y1)
                if t is None:
                    continue
                sy0, sy1 = snap(img(p2), max(HEADER_Y, t[0] - 4), min(y1, t[1] + 4), p2)
                # a continuation sliver above a question that starts at the
                # page top holds only that question's raised fraction; once
                # the edge moves above it nothing is left (9702/13/O/N/15)
                if sy1 - sy0 < 2 or tighten(img(p2), sy0, sy1) is None:
                    continue
                # a number alone on its row (question opening with a diagram) is
                # whited out, so the crop edge can land inside its glyphs; start
                # below the number when nothing else shares that band
                nb = q["num_bbox"]
                if not final and p2 == q["pno"] and sy0 < nb.y1 < sy1 and \
                        tighten(img(p2), sy0, nb.y1 - 2) is None:
                    # midway between the digits' glyph bottom (box bottom less
                    # the descender space) and the first ink below
                    first_ink = tighten(img(p2), nb.y1 - 2, sy1)[0] + 72 / SNAP_DPI
                    sy0 = (nb.y1 - 2 + first_ink) / 2
                final.append((p2, sy0, sy1))
            if not final:
                raise Review(f"Q{q['q']} has no content")
            parts = [render(doc[p2], y0, y1) for p2, y0, y1 in final]
            gap = round(8 * DPI / 72)
            lefts = [x_extent(doc[p2], y0, y1)[0] for p2, y0, y1 in final]
            offs = [round((lx - min(lefts)) * DPI / 72) for lx in lefts]   # keep page x-alignment
            w = max(im.width + o for im, o in zip(parts, offs))
            h = sum(im.height for im in parts) + gap * (len(parts) - 1)
            canvas = Image.new("RGB", (w, h), "white")
            y = 0
            for im, o in zip(parts, offs):
                canvas.paste(im, (o, y))
                y += im.height + gap
            label = f"Q{q['q']}"
            canvas.save(out / f"{a.prefix}-{label}.png")
            prov[label] = [{"pdf_page": p2 + 1, "clip_points": [round(x_extent(doc[p2], y0, y1)[0], 2), round(y0, 2),
                                                               round(x_extent(doc[p2], y0, y1)[1], 2), round(y1, 2)],
                            "semantic_bounds_points": [round(y0, 2), round(y1, 2)], "two_dimensional_seam": False}
                           for p2, y0, y1 in final]
        if secb:
            q31 = next((q for q in qs if q["pno"] == secb[0] and q["y"] > secb[1]), None)
            if q31 is None:
                raise Review("Section B heading without a following question on its page")
            t = tighten(img(secb[0]), secb[1] - 4, q31["y"] - 4)
            sy0, sy1 = snap(img(secb[0]), max(HEADER_Y, t[0] - 4), min(q31["y"] - 4, t[1] + 4), secb[0])
            render(doc[secb[0]], sy0, sy1).save(out / f"{a.prefix}-SecB.stem.png")
            prov["SecB.stem"] = [{"pdf_page": secb[0] + 1,
                                  "clip_points": [round(x_extent(doc[secb[0]], sy0, sy1)[0], 2), round(sy0, 2),
                                                  round(x_extent(doc[secb[0]], sy0, sy1)[1], 2), round(sy1, 2)],
                                  "semantic_bounds_points": [round(sy0, 2), round(sy1, 2)], "two_dimensional_seam": False,
                                  "stem_for": [f"Q{q['q']}" for q in qs if q["q"] >= q31["q"]]}]
        json.dump({"source_pdf": a.src, "prefix": a.prefix, "paper_type": "MCQ", "outputs": prov},
                  open(out / f"{a.prefix}-split-provenance.json", "w"), indent=1)
    except Review as exc:
        print(f"REVIEW_REQUIRED: {exc}", file=sys.stderr)
        return 1
    print(f"{len(qs)} questions -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
