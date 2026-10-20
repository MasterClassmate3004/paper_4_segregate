#!/usr/bin/env python3
"""Text-coverage + boundary gate for A Level QP splits.

Independent of the splitter: it reads the source PDF's own word positions and
the crop regions recorded in <PREFIX>-split-provenance.json.

Gate 2 (coverage): every question word on every question page lies inside
EXACTLY ONE crop -- the WHOLE word horizontally (a centre test missed a word
clipped at the right edge) and its centre vertically.
Gate 3 (boundaries): every crop segment's top and bottom edge lies on a blank
pixel row of the source page (an edge through ink = a sliced glyph/line).

Excluded from coverage (not question content):
  * pages before the first question / after the last crop segment (cover,
    Data and Formulae, Periodic Table, acknowledgements) and BLANK PAGEs;
  * page furniture: header/footer band, barcode font and caption, page
    numbers, UCLES codes, 'DO NOT WRITE IN THIS MARGIN';
  * the question-number token itself, '[Total: n]';
  * answer rows (within 6 pt of a dotted leader) and stand-alone '[n]' mark
    rows: reported as answer_row_words for the D6 convention, not as misses.

Usage: al_verify_coverage.py SOURCE.pdf CROPS_DIR PREFIX [--verbose]
Exit 0 only when missing == 0, duplicated == 0 and sliced == 0.  The summary
line always starts with 'pages ' -- callers must treat its absence as failure.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import numpy as np
import pymupdf as fitz

sys.path.insert(0, str(Path(__file__).resolve().parent))
from barcode_rule import is_barcode_span  # noqa: E402
import fused_marks  # noqa: E402
fused_marks.install(leaders=len(sys.argv) > 3 and sys.argv[3].startswith(("AL-MTH-", "AL-FMT-")))

HEADER_Y, FOOTER_Y = 40, 800
DOT_RE = re.compile(r"^[.…]{3,}")
MARK_RE = re.compile(r"^\[\d+\]$")
PLAIN_RE = re.compile(r"^(\d{1,2}\.?|\[\d+\]|\(\w{1,4}\)|[.…,;:]+|[•●▪–-])$")
ANSWER_AREA_LABEL_RE = re.compile(r"^(?:Diagram|Working|Answer)\.?:?$", re.I)
INSTRUCTION_RE = re.compile(
    r"^(?:Write your answers in the spaces provided\.?|on (?:the )?page \d+\.?|Use of the Data Booklet (?:may be|is) (?:appropriate|relevant) for some questions\.?|Answer (?:all |any \w+ )?(?:of )?(?:the )?questions?(?: in (?:the spaces provided|Section [A-C]).*)?\.?|It is recommended that you spend.*|The Options are as follows[:.]?|You may not need to use all (?:of )?the materials provided\.?|DO NOT WRITE(?: IN THIS SPACE)?|IN THIS SPACE|Measurements and calculations|Graph grid|"
    r"QUESTION \d+ (?:IS|STARTS|BEGINS|CONTINUES).*|\[?Question \d+ (?:continues|starts|begins).*|"
    r"(?:.* )?BLANK PAGE(?: .*)?|Please turn over.*|\[?Turn over for .*|(?:Question|Section|Option) \S+ (?:starts|begins|continues) on page \d+\.?|Turn over to page \d+ for the next question\.?|\[?Questions? \d+(?:(?:,| and) \d+)* (?:is|are) printed (?:on the next page|overleaf)\.?\]?|OPTION \d+\s*[\u2013-]\s*[A-Z][A-Z ,&-]+|Answer (?:one|two|either|both|all) (?:of the )?(?:following )?questions?\.?|Question \d+\.|_{10,}|This question continues.*|Space for working\.?|Space for (?:a |the |your )?(?:table|diagram|drawing|graph)s?\.?|(?:You may )?use (?:the|this) space (?:below )?for (?:any |your )?working\.?|Use the space below for any diagrams you include in your answer to \(\w+\)\.?|"
    r"\[Total\s*:\s*\d+\]|Total\s*:\s*\[\d+\]|Section [A-C]|Question \d+ \[\d+ minutes\]|"
    # pre-2009 Paper 6 cover list: 'Option A Astrophysics and Cosmology questions 1, 2, 3 and 4'
    r"Option [A-Z] .+ questions? \d+(?:(?:,| and) \d+)*\.?|"
    # pre-2009 Paper 6 option section headings (whole line only)
    r"Option(?: [A-Z])?|Astrophysics and Cosmology|The Physics of Fluids|Medical Physics|"
    r"Environmental Physics|Telecommunications|"
    # pre-2009 9701 Paper 6 option titles + rubric, Paper 4 'Section B - Applications of Chemistry'
    r"BIOCHEMISTRY|ENVIRONMENTAL CHEMISTRY|PHASE EQUILIBRIA|SPECTROSCOPY|TRANSITION ELEMENTS|"
    r"(?:If you attempt this option, )?answer (?:both|all) questions on (?:the paper provided|two of the Options)\.?|"
    r"Section [A-C] [\u2013-] .+)$", re.I)
MCQ_RUBRIC_RE = re.compile(r"^For each question,? there are four possible answers,? A, B, C,? and D\.", re.I)
# Biology essay-section rubric (9700 Paper 4 2004-05 Section B, Paper 6 2002-03),
# possibly wrapped: 'In this section, answers should be illustrated by large,
# clearly labelled diagrams wherever' / 'possible.' -- paper furniture
ESSAY_RUBRIC_RE = re.compile(
    r"^(?:Circle the number of the question(?:s)? you have answered|Answer only one question from this section|Your answers? to Section [A-C] must be in continuous prose|"
    r"(?:In this section, )?answers (?:may|should) be illustrated by large, clearly labelled diagrams|"
    r"The answer to Question \d+ should be illustrated by large, clearly labelled diagrams|"
    r"Your answer must be set out in sections \(a\) and \(b\))", re.I)
LINE_FURNITURE_RE = re.compile(
    r"^(?:Please turn over.*|(?:\[?)Turn over for .*|(?:This|The) question continues.*|"
    r"QUESTION \d+ (?:IS|STARTS|BEGINS|CONTINUES).*|\[?Question \d+ (?:continues|starts|begins).*)$", re.I)
TOTAL_RE = re.compile(r"^\[Total:?(\d+\])?$|^\d+\]$")
FURNITURE_RE = re.compile(r"^(©|UCLES|\[Turn|over|BLANK|PAGE|\*|Cambridge|University|Press|&|Assessment)$|"
                          r"^\d{4}/\d{1,2}(/.*)?$|^[A-Z]/[A-Z]/?\d{2}$|^[MOJN]/[JN]\d{2}$|^\d{4}$|"
                          # footer code broken into pieces ('9702/23/O/' 'N/23')
                          r"^[A-Z]/$|^[A-Z]/\d{2}$")


def shift29(t: str) -> str:
    """Undo a subset font whose codes are offset by -29 ('>7XUQ RYHU' is
    '[Turn over', 9701/12/M/J/23 footers)."""
    return "".join(chr(ord(c) + 29) if 33 <= ord(c) <= 98 else c for c in t)


def is_furniture(span_font: str, text: str, x0: float, y0: float, x1: float, y1: float) -> bool:
    if span_font == "BARCODE" or is_barcode_span(text, y0, y1):
        return True
    if y1 < HEADER_Y + 25 and (text.isdigit() or text.startswith("*") or re.fullmatch(r"\d{6,}", text)):
        return True  # page number / barcode caption
    if (x1 < 35 or x0 > 565) and (re.fullmatch(r"(?:DO|NOT|WRITE|IN|THIS|MARGIN)", text, re.I)
                                  or span_font == "BARCODE" or len(text) <= 2 and not text.isalnum()):
        return True  # margin strips ('DO NOT WRITE IN THIS MARGIN') -- real content
                     # left of 35 pt (a graph's axis label) must still be covered
    if x0 > 515 and text in ("For", "Examiner’s", "Examiner's", "Use"):
        return True  # 2000s-2010s 'For Examiner's Use' column
    if x0 > 520 and re.fullmatch(r"[A-Z]", text):
        return True  # 2002 Paper 5 examiner-column category letters (M R A G)
    if x0 > 528 and re.fullmatch(r"\(?(?:[a-h]|i{1,3}|iv|vi{0,3})\)?", text):
        return True  # 2002-04 examiner marking-box labels (a-g, i-iv) beside the body column
    return y0 > FOOTER_Y - 30 and (bool(FURNITURE_RE.search(text)) or bool(re.fullmatch(r"\d{4}", text)))


def main() -> int:
    pdf, crops, prefix = sys.argv[1:4]
    verbose = "--verbose" in sys.argv
    prov_all = json.load(open(Path(crops) / f"{prefix}-split-provenance.json"))
    prov = prov_all["outputs"]
    manual_masks = prov_all.get("manual_masks", [])
    regions: dict[int, list[tuple[str, fitz.Rect]]] = {}
    for label, segs in prov.items():
        for s in segs:
            regions.setdefault(s["pdf_page"], []).append((label, fitz.Rect(s["clip_points"])))
    if not regions:
        print("no crop regions in provenance")
        return 1
    first_page, last_page = min(regions), max(regions)
    doc = fitz.open(pdf)
    missing, dup, answer_words, plain_in_crop = [], [], [], []
    for pno in range(first_page, last_page + 1):  # 1-based page numbers
        page = doc[pno - 1]
        if re.search(r"Important values, constants and standards|The Periodic Table of (?:the )?Elements", page.get_text()) \
                and not regions.get(pno):
            continue    # a data page inside the paper (9701/22/F/M/25 p.11): reference, not question content
        spans = [("BARCODE" if is_barcode_span(sp["text"], sp["bbox"][1], sp["bbox"][3]) else sp["font"],
                  fitz.Rect(sp["bbox"])) for b in page.get_text("dict")["blocks"]
                 for line in b.get("lines", []) for sp in line["spans"]]

        def font_of(x0, y0, x1, y1):
            c = fitz.Point((x0 + x1) / 2, (y0 + y1) / 2)
            return next((f for f, r in spans if r.contains(c)), "")

        wl = page.get_text("words")
        page_draws = page.get_drawings()
        dot_rows = [w[1] for w in wl if DOT_RE.match(w[4])]
        body = [w for w in wl if HEADER_Y <= w[1] <= FOOTER_Y
                and not is_furniture(font_of(*w[:4]), w[4], *w[:4])]
        # the footer line is furniture as a whole: printer job codes beside
        # '(c) UCLES' ('11_9701_12_2023_1.11R', '03_9701_12_1.18') are split
        # into fragments and some are in a broken glyph encoding ('>7XUQ RYHU'
        # = '[Turn over'), so match the line, not the strings (9701 2023)
        copy_ys = [w[1] for w in wl if w[1] > FOOTER_Y - 30 and w[4] in ("©", "UCLES")]
        body = [w for w in body if not (w[1] > FOOTER_Y - 30 and any(abs(w[1] - y) < 5 for y in copy_ys))
                and not (w[1] >= FOOTER_Y - 15 and w[3] - w[1] < 11)    # 8 pt footer line, even when garbled
                and not (w[1] >= FOOTER_Y - 15 and FURNITURE_RE.search(shift29(w[4])))]
        if {w[4] for w in body} <= {"BLANK", "PAGE"}:
            continue
        # a data table printed below the last question on a question page
        # (9701/22/F/M/25 p.11): reference, not question content
        ref_top = [w[1] for w in body if w[4] == "Important" and any(
            v[4] == "constants" and abs(v[1] - w[1]) < 3 for v in body)]
        if ref_top:
            body = [w for w in body if w[1] < min(ref_top) - 2]
        # Cambridge copyright notice on the last page is furniture
        # (both wordings: 'To avoid the issue of disclosure ...' and
        # 'Permission to reproduce items where third-party owned material ...')
        # (raw page words: 'University' near the footer is itself filtered
        # out of `body` as furniture, which hid the 2004 MCQ notice)
        notice = [w[1] for w in wl if 650 < w[1] <= FOOTER_Y and w[4] == "University" and any(
            v[4] in ("Syndicate", "Examinations") and abs(v[1] - w[1]) < 12 for v in wl)] + \
                 [w[1] for w in body if w[4] == "Acknowledgements:" or (w[4] == "To" and any(
            v[4] == "disclosure" and abs(v[1] - w[1]) < 3 for v in body)) or (w[4] == "Permission" and any(
            v[4] == "reproduce" and abs(v[1] - w[1]) < 3 for v in body)) or (w[4] == "Every" and w[1] > 600 and any(
            v[4] == "reasonable" and abs(v[1] - w[1]) < 3 for v in body))       # 2004 wording
                  # map disclaimer 'The boundaries and names shown ... on this map' (9700/22/M/J/24 p.16)
                  or (w[4] == "boundaries" and any(v[4] == "designations" and 0 <= v[1] - w[1] < 14 for v in body))]
        # 2010s Paper 5 examiner's marking grid (furniture)
        grid = [w[1] for w in body if w[4] == "Defining" and any(
            v[4] == "Safety" and abs(v[1] - w[1]) < 3 for v in body)]
        if grid:
            body = [w for w in body if not (min(grid) - 7 <= w[1] <= min(grid) + 60)]
        if notice:
            body = [w for w in body if w[1] < min(notice) - 1]
        rows: dict[int, list] = {}
        for w in sorted(body, key=lambda w: w[1]):
            key = next((k for k, ws in rows.items() if abs(ws[0][1] - w[1]) < 2.5), len(rows))
            rows.setdefault(key, []).append(w)
        in_mcq_rubric = 0
        in_key = False
        for row in sorted(rows.values(), key=lambda ws: min(w[1] for w in ws)):
            row = sorted(row, key=lambda w: w[0])
            row_text = [w[4] for w in row]
            joined = " ".join(row_text)
            # 9701 Paper 1 Section B answer key ('The responses A to D should be
            # selected on the basis of' + A-D table + 'No other combination ...'),
            # reprinted at the top of every Section B page: boilerplate; the
            # first copy is inside the SecB.stem crop
            if re.match(r"^(?:The responses A to D should be selected on the basis of|For each of the questions in this section, one or more)", joined):
                in_key = True
            if in_key:
                if re.match(r"^No other combination of statements is used as a (?:correct|single) response", joined):
                    in_key = False
                continue
            if INSTRUCTION_RE.match(joined):
                continue  # paper instructions / continuation notes (furniture)
            # the MCQ answering rubric, wrapped over two lines: 'For each question
            # there are four possible answers, A, B, C, and D. Choose the one you
            # consider to' / 'be correct.' (9701 Paper 1 Section A)
            if MCQ_RUBRIC_RE.match(joined):
                in_mcq_rubric = 0 if joined.rstrip().endswith(".") else 2
                continue
            if ESSAY_RUBRIC_RE.match(joined):
                in_mcq_rubric = 0 if joined.rstrip().endswith(".") else 1
                continue
            if in_mcq_rubric:
                in_mcq_rubric = 0 if joined.rstrip().endswith(".") else in_mcq_rubric - 1
                continue
            in_mcq_rubric = 0
            if re.fullmatch(r"Section [A-C]", joined) or re.search(
                    r"^Answer (?:all|any \w+) (?:of )?(?:the )?questions?", joined):
                continue  # section heading / instruction (paper furniture)
            # answer row: within a line-height of a dotted leader (catches
            # raised superscript units such as 's-1' on 'v = .... m s-1')
            answer_row = any(abs(row[0][1] - dy) <= 6 for dy in dot_rows)
            # D6: a LABELLED answer line ('speed = ..... m s-1 [2]') must be in
            # its leaf's crop; plain '..... [1]' / '1. .....' lines are dropped
            labelled_row = answer_row and any(not PLAIN_RE.match(t) and not DOT_RE.match(t)
                                              and not (t in ("For", "Examiner’s", "Examiner's", "Use"))
                                              for t in row_text)
            # a small drawn symbol in the row ('...... <=> ......' equation
            # template, 9701/41/O/N/17) labels it, as in the splitter
            if answer_row and not labelled_row:
                ry0, ry1 = min(w[1] for w in row), max(w[3] for w in row)
                rx0, rx1 = min(w[0] for w in row), max(w[2] for w in row)
                big = [d["rect"] for d in page_draws if d.get("rect") is not None
                       and d["rect"].width > 40 and d["rect"].height > 40]
                labelled_row = any(2 < d["rect"].width <= 40 and d["rect"].height <= 10 and d["rect"].y1 > ry0 - 1
                                   and ry0 - 8 < d["rect"].y0 < ry1 and rx0 - 2 < d["rect"].x0 and d["rect"].x1 < rx1 + 2
                                   and not any(b.intersects(d["rect"]) for b in big)
                                   for d in page_draws if d.get("rect") is not None)
            for i, w in enumerate(sorted(row, key=lambda w: w[0])):
                x0, y0, x1, y1, t = w[:5]
                if TOTAL_RE.match(t) and any(tt.startswith("[Total") for tt in row_text):
                    continue
                if i == 0 and t.isdigit() and 40 <= x0 <= 60:
                    continue  # question number
                # a label can sit 3-4 pt off the leader's baseline ('m =' /
                # 'ω' beside '.....', 9702/52/F/M/18, 9702/04/O/N/03): look
                # along the whole visual line, not just the 2.5 pt row bucket
                line_label = any(abs((v[1] + v[3]) / 2 - (y0 + y1) / 2) < 6 and v is not w
                                 and not PLAIN_RE.match(v[4]) and not DOT_RE.match(v[4])
                                 and not MARK_RE.match(v[4]) for v in body)
                masked = any(m[0] == pno and m[1] - 1 <= x0 and x1 <= m[3] + 1 and m[2] - 1 <= y0 and y1 <= m[4] + 1
                             for m in manual_masks)       # whited out in the crop
                if DOT_RE.match(t) and x1 - x0 > 150 and not labelled_row and not line_label and not masked:
                    cx_, cy_ = (x0 + x1) / 2, (y0 + y1) / 2
                    if any(r.y0 <= cy_ <= r.y1 and r.x0 <= cx_ <= r.x1 for _, r in regions.get(pno, [])):
                        plain_in_crop.append((pno, round(y0)))
                if DOT_RE.match(t) or re.fullmatch(r"[.,;:]", t):
                    continue   # leaders / a stray punctuation mark carry no content
                if len(row) == 1 and ANSWER_AREA_LABEL_RE.match(t):
                    continue  # 'Diagram' / 'Working' heading of an answer space
                cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
                owners = [lab for lab, r in regions.get(pno, [])
                          if r.y0 <= cy <= r.y1 and r.x0 - 0.5 <= x0 and x1 <= r.x1 + 0.5]
                lone_mark = bool(MARK_RE.match(t)) and len(row) == 1
                # a mark printed on a plain dotted row ('........ [2]') is kept
                # even though the row's dots are dropped: it is REQUIRED
                if answer_row and not labelled_row and not lone_mark and not MARK_RE.match(t):
                    answer_words.append((pno, t, owners[:1]))   # plain answer line: dropped by D6
                    if owners and DOT_RE.match(t) is None and False:
                        pass
                    continue
                if answer_row or lone_mark:
                    # labelled answer line / lone mark: REQUIRED (checked below)
                    answer_words.append((pno, t, owners[:1]))
                if owners and MARK_RE.match(t) and any(
                        m[0] == pno and m[1] <= cx <= m[3] and m[2] <= cy <= m[4] for m in manual_masks):
                    owners = []      # a mark whited out by a mask is not visible: missing
                if not owners:
                    missing.append((pno, round(y0), t))
                elif len(owners) > 1:
                    # also twice inside ONE crop (two segments of the same leaf
                    # holding the same rows: 9701/51/O/N/10 Q1(b))
                    dup.append((pno, round(y0), t, sorted(owners)))

    # Gate 3: boundaries on blank rows (barcode glyphs whited out first, as
    # the splitter does).
    sliced = []
    for pno, segs in regions.items():
        page = doc[pno - 1]
        for b in page.get_text("dict")["blocks"]:
            for line in b.get("lines", []):
                for sp in line["spans"]:
                    if is_barcode_span(sp["text"], sp["bbox"][1], sp["bbox"][3]):
                        r = fitz.Rect(sp["bbox"])
                        page.draw_rect(fitz.Rect(r.x0 - 2, 18 if r.y1 < 100 else r.y0 - 1, r.x1 + 2, r.y1 + 1.5),
                                       color=None, fill=(1, 1, 1), overlay=True)
        for d in page.get_drawings():          # 2025+ corner crop-marks (furniture)
            r = d.get("rect")
            if r is not None and r.y0 > 785 and max(r.width, r.height) <= 25 and (r.x1 < 62 or r.x0 > 533):
                page.draw_rect(r + (-2.5, -2.5, 2.5, 2.5), color=None, fill=(1, 1, 1), overlay=True)
        # 2010s examiner mark boxes in the right margin (furniture): an
        # independent copy of the splitter's rule -- >=4 text-free drawings
        # confined to x 528-568, spanning 15-35 pt, not joined to a body line
        pw_ = page.get_text("words")
        margin = [d["rect"] for d in page.get_drawings() if d.get("rect") is not None
                  and d["rect"].x0 >= 528 and d["rect"].x1 <= 572 and 60 < d["rect"].y0 and d["rect"].y1 < 790
                  and d["rect"].height <= 40 and d["rect"].width <= 35
                  and not [w for w in pw_ if fitz.Rect(w[:4]).intersects(d["rect"] + (-2, -2, 2, 2))]]
        if len(margin) >= 4:
            mx0, mx1 = min(r.x0 for r in margin), max(r.x1 for r in margin)
            joined = [d["rect"] for d in page.get_drawings() if d.get("rect") is not None
                      and d["rect"].x0 < mx0 - 3 and abs(d["rect"].x1 - mx0) <= 2.5]
            if 15 <= mx1 - mx0 <= 35 and not joined:
                for r in margin:
                    page.draw_rect(r + (-1, -1, 1, 1), color=None, fill=(1, 1, 1), overlay=True)
        # masks a manual spec applied to its crops (recorded in provenance)
        for m in manual_masks:
            if m[0] == pno:
                page.draw_rect(fitz.Rect(m[1:5]), color=None, fill=(1, 1, 1), overlay=True)
        pm = page.get_pixmap(dpi=200, colorspace=fitz.csGRAY, alpha=False)
        img = np.frombuffer(pm.samples, np.uint8).reshape(pm.height, pm.width)
        k = 200 / 72
        for label, r in segs:
            for y in (r.y0, r.y1):
                row = int(round(y * k))
                if 0 <= row < pm.height:
                    band = img[row, int(r.x0 * k):int(r.x1 * k)]
                    if (band < 235).any():
                        sliced.append((pno, label, round(y, 1), int((band < 235).sum())))
            # left/right edges too: a figure wider than the crop is sliced
            for x in (r.x0, r.x1):
                col = int(round(x * k))
                if 0 <= col < pm.width:
                    band = img[int(r.y0 * k):int(r.y1 * k), col]
                    if (band < 235).any():
                        sliced.append((pno, label, f"x={round(x, 1)}", int((band < 235).sum())))

    # Gate 4: no page furniture inside any crop (copyright notice, footer
    # codes, Turn over, BLANK PAGE, margin strip, [Total]) -- the coverage
    # gate only excused furniture, it never forbade it (Q40 of 12/M/J/24
    # carried the copyright block).
    forbidden = []
    pass
    FORBID = re.compile(r"^(UCLES|BLANK|\[Turn|Permission|disclosure|acknowledgements|Acknowledgements:|Syndicate)$|"
                        r"^\d{4}/\d{2}/[A-Z]/[A-Z]/\d{2}$|^MARGIN$")
    for pno, segs in regions.items():
        pw = doc[pno - 1].get_text("words")
        working = [w for w in pw if w[4] == "Space" and any(
            v[4] == "working" and abs(v[1] - w[1]) < 3 for v in pw)]
        working += [w for w in pw if w[4] == "Question" and any(
            v[4] in ("continues", "continued") and abs(v[1] - w[1]) < 3 and v[0] > w[0] for v in pw)]
        # whole-line instruction furniture: 'Please turn over for Question 11.',
        # 'This question continues on the next page', 'QUESTION 5 STARTS ...'
        lines: dict[int, list] = {}
        for w in pw:
            lines.setdefault(round(w[1]), []).append(w)
        for ws in lines.values():
            ws.sort(key=lambda v: v[0])
            if LINE_FURNITURE_RE.match(" ".join(v[4] for v in ws)):
                working.append(ws[0])
        for w in working:
            c = fitz.Point((w[0] + w[2]) / 2, (w[1] + w[3]) / 2)
            if any(m[0] == pno and m[1] <= c.x <= m[3] and m[2] <= c.y <= m[4] for m in manual_masks):
                continue   # whited out by a spec mask: not in the crop
            for label, r in segs:
                if r.contains(c):
                    forbidden.append((pno, label, "instruction furniture: " + w[4]))
        for w in pw:
            if FORBID.search(w[4]):
                c = fitz.Point((w[0] + w[2]) / 2, (w[1] + w[3]) / 2)
                for label, r in segs:
                    if r.contains(c):
                        forbidden.append((pno, label, w[4]))
    # Gate 5: a part that refers to 'Fig. N' / 'Table N' must be able to see
    # it -- the caption sits in the part itself, an ancestor stem, or an
    # EARLIER crop (an earlier part's figure = dependency).  A caption only in
    # a LATER crop means the figure was given to the wrong owner.
    order = {}
    for label, segs in prov.items():
        s0 = min((sg["pdf_page"], sg["clip_points"][1]) for sg in segs)
        order[label] = s0
    def crop_words(label):
        out = []
        for sg in prov[label]:
            r = fitz.Rect(sg["clip_points"])
            pw = doc[sg["pdf_page"] - 1].get_text("words")
            out += [w for w in pw if r.contains(fitz.Point((w[0] + w[2]) / 2, (w[1] + w[3]) / 2))]
        return out
    words_of = {lab: crop_words(lab) for lab in prov}
    captions = {}
    for lab, ws in words_of.items():
        ws = sorted(ws, key=lambda w: (round(w[1]), w[0]))
        for a, b in zip(ws, ws[1:]):
            row = [w for w in ws if abs(w[1] - a[1]) < 2]
            if a[4] in ("Fig.", "Table") and abs(a[1] - b[1]) < 2 and re.fullmatch(r"\d+\.\d+", b[4]) \
                    and row and row[0] is a and len(row) <= 5 \
                    and not (len(row) > 2 and row[2][4][:1].islower()):   # 'Table 1.1 above.' is prose
                captions.setdefault((a[4].lower().strip("."), b[4]), set()).add(lab)
    misplaced = []
    for lab, ws in words_of.items():
        if lab.endswith(".stem"):
            continue
        parts = lab.split(".")
        allowed = {lab} | {".".join(parts[:k]) + ".stem" for k in range(1, len(parts) + 1)}
        txt = " ".join(w[4] for w in sorted(ws, key=lambda w: (round(w[1]), w[0])))
        for kind, num in set(re.findall(r"\b(Fig|Table)\.?\s+(\d+\.\d+)", txt)):
            owners = captions.get((kind.lower(), num))
            if not owners or owners & allowed:
                continue
            if all(order[o] > order[lab] for o in owners):
                misplaced.append((lab, f"{kind}. {num}", sorted(owners)))
    for m in misplaced[:25]:
        print("  FIGURE-OWNED-LATER", m)
    # Gate 6: no large fully blank band inside a crop (untrimmed working
    # space / page-break gap).  220 dpi crops; 45 pt = 137 px.
    from PIL import Image
    bands = []
    for f in sorted(Path(crops).glob(f"{prefix}-Q*.png")):
        a = np.asarray(Image.open(f).convert("L"))
        ink = (a < 200).any(axis=1)
        idx = np.where(ink)[0]
        if len(idx) < 2:
            continue
        # blank runs inside the crop; a run is WORKING SPACE (defect) when the
        # ink right after it is answer material only: everything starts right
        # of 40% of the width (a '[2]' mark / 'speed = .....' line).  Blank
        # space inside a figure (solenoid interior, wavefront area) is
        # followed by figure/prose ink starting at the left: not flagged.
        top0 = idx[0]
        run, start = 0, None
        for i in range(idx[0], idx[-1] + 1):
            if not ink[i]:
                run += 1
                continue
            if run > 137:
                below = a[i:i + 40] < 200
                cols = np.where(below.any(axis=0))[0]
                if len(cols) and cols[0] > 0.20 * a.shape[1] and cols[-1] > 0.85 * a.shape[1]:
                    bands.append((f.stem[len(prefix) + 1:], round(run * 72 / 220)))
            run = 0
    # a manual spec may accept a band after visual inspection (printed figure
    # or drawing space); the reason is recorded in the provenance
    accepted = json.load(open(Path(crops) / f"{prefix}-split-provenance.json")).get("accepted_blank_bands", {})
    for b in [b for b in bands if b[0] in accepted]:
        print("  ACCEPTED-BLANK-BAND", b, accepted[b[0]])
    bands = [b for b in bands if b[0] not in accepted]
    for b in bands[:25]:
        print("  BLANK-BAND", b)
    sliced += [("blank",) + b for b in bands]
    sliced += [("figure",) + m for m in misplaced]
    for f in forbidden[:25]:
        print("  FURNITURE-IN-CROP", f)
    acc_plain = prov_all.get("accepted_plain_rows", {})
    for pl in [pl for pl in plain_in_crop if f"{pl[0]}:{pl[1]}" in acc_plain]:
        print("  ACCEPTED-PLAIN-ROW", pl, acc_plain[f"{pl[0]}:{pl[1]}"])
    plain_in_crop = [pl for pl in plain_in_crop if f"{pl[0]}:{pl[1]}" not in acc_plain]
    for pl in plain_in_crop[:25]:
        print("  PLAIN-DOTTED-LINE-IN-CROP", pl)
    sliced += [("plain",) + pl for pl in plain_in_crop]
    for a in [a for a in answer_words if a[2]][: (200 if verbose else 0)]:
        print("  ANSWER-ROW WORD IN CROP", a)
    # Gate 1b: pages AFTER the last crop must hold only reference/furniture
    # pages -- a trailing figure page owned by nobody was never checked
    # (9701/22/F/M/17 p.15: infra-red spectra X, Y, Z for Q3(d)(ii))
    doc_all = fitz.open(pdf)
    REF_PAGE_RE = re.compile(r"Important values, constants and standards|The Periodic Table|oganesson|"
                             r"Centre Number|Candidate Number|Additional Page|lined page|Qualitative Analysis Notes|"
                             # teacher report form, old 9700 Paper 5 last page
                             r"REPORT FORM\s+The teacher responsible for this subject", re.I)
    in_notes = False   # 'Qualitative Analysis Notes' run over several pages (9701/05/O/N/03 p.10-11)
    for pno in range(last_page + 1, doc_all.page_count + 1):
        pg = doc_all[pno - 1]
        txt = pg.get_text()
        allw = pg.get_text("words")
        # a page set in the -29 shifted subset font (9701/12/M/J/23 p.15):
        # analyse its decoded words
        dec = lambda t: "".join(chr(ord(c) + 29) if 3 <= ord(c) <= 98 else c for c in t)
        if re.search(r"Permission\s*to\s*reproduce|Important\s*values|Periodic\s*Table", dec(txt), re.I) and not \
                re.search(r"Permission\s*to\s*reproduce|Important\s*values|Periodic\s*Table", txt, re.I):
            txt = dec(txt)
            allw = [tuple(w[:4]) + (dec(w[4]),) + tuple(w[5:]) for w in allw]
        # content ABOVE the copyright notice counts ('Use the data given on
        # page 12', 9701/51/M/J/14: data table + notice share the last page)
        tops = [w[1] for w in allw if (w[4] == "Permission" and any(v[4] == "reproduce" and abs(v[1] - w[1]) < 3 for v in allw))
                or (w[4] == "Every" and any(v[4] == "reasonable" and abs(v[1] - w[1]) < 3 for v in allw))
                or w[4] == "Acknowledgements:"
                or (w[4] == "boundaries" and any(v[4] == "designations" and 0 <= v[1] - w[1] < 14 for v in allw))
                or (w[1] > 600 and w[4] in ("University", "Cambridge") and any(
                    v[4] in ("Syndicate", "part") and abs(v[1] - w[1]) < 14 for v in allw))]
        cap = min(tops) - 1 if tops else FOOTER_Y - 15
        foot = [w[1] for w in allw if w[4] in ("©", "UCLES") and w[1] > 700]     # the (c) footer row
        ws = [w for w in allw if HEADER_Y + 10 <= w[1] <= cap and re.search(r"[A-Za-z]{3,}", w[4])
              and not any(abs(w[1] - y) < 5 for y in foot)
              and not re.fullmatch(r"(?:DO|NOT|WRITE|IN|THIS|MARGIN|BLANK|PAGE)", w[4])]
        if re.search(r"Qualitative Analysis Notes", txt, re.I):
            in_notes = True
        if len(ws) < 4 or REF_PAGE_RE.search(txt) or (in_notes and re.search(r"\b(?:Reactions|Tests) (?:of|for)\b", txt)):
            continue
        for w in ws[:40]:
            missing.append((pno, round(w[1]), w[4] + " [trailing page]"))
    for sl in sliced[:25]:
        print("  SLICED-BOUNDARY", sl)
    for m in missing[: (200 if verbose else 25)]:
        print("  MISSING", m)
    for d in dup[: (200 if verbose else 25)]:
        print("  DUPLICATE", d)
    sliced += [("furniture",) + f for f in forbidden]
    print(f"pages {first_page}-{last_page}: missing={len(missing)} duplicated={len(dup)} sliced_boundaries={len(sliced)} "
          f"answer_row_words={len(answer_words)} (in a crop: {sum(1 for a in answer_words if a[2])})")
    return 0 if not missing and not dup and not sliced else 1


if __name__ == "__main__":
    sys.exit(main())
