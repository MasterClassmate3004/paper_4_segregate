#!/usr/bin/env python3
"""Split an A Level mark scheme into one image per question-paper leaf.

The mark scheme is cut by its PRINTED keys ("1(c)(ii)", "1 (a) (i)",
"(i)1", "2(b)(i)1."), never by order.  A candidate key is accepted only if it
names a node of the approved QP label tree (from the QP provenance), comes
after the previous key in QP reading order, and (for a bare question number
in a non-table layout) sits in the question-number column.  Each key's row is
cropped without the key column, so no question number is visible:

  * table layouts (2018+ landscape, any page with a Question|Answer|Marks
    table): rows end at the horizontal rule that spans the question column;
    the crop is the Answer..Marks columns;
  * prose layouts (2002-2017): rows end in the blank gap above the next key's
    line; the crop starts at the row's own content (labels are left of it).

Mapping per QP leaf (stems are never mapped):
  exact                            MS key == QP leaf
  parent_ms_covers_child_qp        nearest MS ancestor key covers the leaf
  children_ms_merged_for_parent_qp MS keys below the leaf, stacked in order
  unresolved                       nothing (blocks the paper)
An MS key no leaf uses is an orphan (also blocks).

Science Paper 1 (MCQ): the answer key is read into answers.csv; no crops.

Usage: al_ms_splitter.py MS_PDF QP_PROVENANCE OUTDIR PREFIX [--component N] [--mcq]
"""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

import numpy as np
import pymupdf as fitz
from PIL import Image

DPI = 220
K = DPI / 72.0
SEP_PT = 8
PAD_PT = 4
ROMANS = ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x"]

HEADER_WORDS = {"Page", "Mark", "Scheme", "Scheme:", "Syllabus", "Paper", "PUBLISHED",
                "GCE", "Cambridge", "International"}
FOOTER_RE = re.compile(r"^(©|&|UCLES|Cambridge|University|Press|Assessment|International|Local|Syndicate|"
                       r"Examinations|Page|of|\d{1,2}|\d{4}|\[Turn|over\]?|\d{4}/\d{1,2}(/.*)?)$")
# section and option headings (old Chemistry Paper 6 options: 9701/06/O/N/06)
SECTION_RE = re.compile(r"^(Section\s+[AB]|Uncertainties\s+in\s+Question\s+\d+|Option\s*[A-Z](\s+[-–]\s+.+|\W*)"
                        r"|Biochemistry|Environmental\s+Chemistry|Phase\s+Equilibria|Spectroscopy"
                        r"|Transition\s+(Elements|Metals)|Applications\s+of\s+Chemistry)$", re.I)

P_Q = re.compile(r"^(\d{1,2})$")
P_COMPOUND = re.compile(r"^(\d{1,2})\(?([a-k])\)?((?:\([ivx]{1,4}\))?)(?:([1-9])\.?)?$")
P_L = re.compile(r"^\(([a-h])\)$")
P_R = re.compile(r"^\(([ivx]{1,4})\)(?:([1-9])\.?)?$")
P_T = re.compile(r"^([1-9])\.$")
P_QWORD = re.compile(r"^Question$")
COLHEAD_RE = re.compile(r"^(Part\s+)?Mark\s+Expected\s+Answer(\s+Additional\s+Guidance)?$")
HEADING_RE = re.compile(r"^[A-Z][A-Za-z ,/&\-]*\(\d+\s*marks?\)$")
# question totals in every printed form: "[Total: 8]", "[Total: 15 max]", "[Total: max 10]",
# "Total: 8", "Total [8]", "Question 3 Total [15]", "Qn 2 Total 12" (furniture, whited out)
TOTAL_RE = re.compile(r"^(\d+\s+marks\s+in\s+total\.?|\[\d+\s*max\s*\d+\]|\[\s*Total\s*:?\s*\d+\s*max\.?\s*\d+\s*\]|\[\s*Total\s*:?\s*(max\.?\s*)?\d+\s*(marks?|max\.?)?\s*\]"
                      r"|((Question|Qn)\s*\d+\s+)?Total\s*(marks?)?\s*[:=]?\s*\[?\d+\]?\s*(marks?|max)?"
                      # 2002-03: 'Total: 13, max 12', 'Total for Question 1 = 10', 'Total for Question 2
                      # is 10 and for the Paper 25', 'Total for Paper: 30', '[Maximum Total: 8]'
                      r"|Total\s*:?\s*\d+\s*,?\s*max\.?\s*\d+"
                      r"|\[?\s*Total\s+for\s+(Question\s*\d+|(the\s+)?Paper)(\s*(is|[:=])?\s*\[?\d+\]?)?\s*(marks?)?"
                      r"(\s+and\s+for\s+the\s+Paper\s*\d+)?\s*\]?"
                      r"|\[\s*Maximum\s+Total\s*:?\s*\d+\s*\])$", re.I)
MARK_RE = re.compile(r"^(\[\d+\]|[A-Z]\d|\d)$")


# ---------------------------------------------------------------- QP tree
def label_tuple(lab: str) -> tuple:
    return tuple(lab[1:].split("."))


def tuple_label(t: tuple) -> str:
    return "Q" + ".".join(t)


def qp_tree(prov: dict) -> tuple[list[tuple], dict[tuple, int]]:
    """Leaves (non-stem labels) in order, and every node's reading-order index."""
    leaves, order = [], {}
    for lab in prov["outputs"]:
        t = label_tuple(lab)
        if t[-1] == "stem":
            t = t[:-1]
        else:
            leaves.append(t)
        for k in range(1, len(t) + 1):
            order.setdefault(t[:k], len(order))
    return leaves, order


# ---------------------------------------------------------------- page geometry
TESSDATA = "/opt/homebrew/share/tessdata"
OCR_LABEL = re.compile(r"^[\(\{\[]([a-zA-Z1|]{1,4})[\)\}\]]+$")
OCR_DIGIT = {"§": "5", "S": "5", "l": "1", "I": "1", "|": "1", "Z": "2", "O": "0"}


def ocr_fix(t: str) -> str:
    """OCR misreads of part labels: (b} -> (b), (il) / (Ii) -> (ii)."""
    if t in OCR_DIGIT:
        return OCR_DIGIT[t]
    m = OCR_LABEL.match(t)
    if not m:
        return t
    inner = m.group(1)
    rom = re.sub(r"[lI1|tj]", "i", inner).lower()
    if rom in ROMANS:
        return f"({rom})"
    if len(inner) <= 2 and inner[-1].lower() in "abcdefgh":
        return f"({inner[-1].lower()})"
    return t


def ocr_labels(page) -> list:
    """Second OCR pass over the label strip only (x < 140): no dot leaders
    there, so the part labels that the full-page pass drops are read."""
    import csv as _csv
    import io
    import subprocess
    import tempfile
    pix = page.get_pixmap(dpi=300, clip=fitz.Rect(0, 0, 140, page.rect.height))
    with tempfile.NamedTemporaryFile(suffix=".png") as f:
        pix.save(f.name)
        tsv = subprocess.run(["tesseract", f.name, "stdout", "--psm", "6", "tsv"],
                             capture_output=True, text=True).stdout
    k, out = 72 / 300, []
    for r in _csv.DictReader(io.StringIO(tsv), delimiter="\t", quoting=_csv.QUOTE_NONE):
        t = (r.get("text") or "").strip()
        if not t or float(r["conf"]) < 0:
            continue
        t = ocr_fix(t)
        x0, y0 = int(r["left"]) * k, int(r["top"]) * k
        x1, y1 = x0 + int(r["width"]) * k, y0 + int(r["height"]) * k
        if x1 < 130 and (P_Q.match(t) or P_L.match(t) or P_R.match(t) or P_T.match(t)):
            out.append((x0, y0, x1, y1, t, 0, 0, 0))
    return out


def words(page) -> list:
    """Text-layer words; a scanned page (no text layer) is read by OCR."""
    ws = [w for w in page.get_text("words") if w[4].strip()]
    if len(ws) < 5 and page.get_images():
        tp = page.get_textpage_ocr(dpi=300, full=True, tessdata=TESSDATA)
        ws = [w[:4] + (ocr_fix(w[4]),) + tuple(w[5:]) for w in page.get_text("words", textpage=tp) if w[4].strip()]
        labs = ocr_labels(page)
        ws = [w for w in ws if not any(min(w[2], l[2]) - max(w[0], l[0]) > 1 and
                                       min(w[3], l[3]) - max(w[1], l[1]) > 1 for l in labs)] + labs
        OCR_PAGES.add(page.number)
    return ws


OCR_PAGES: set = set()


def rows_of(ws: list, tol: float = 4.0) -> list[list]:
    rows: list[list] = []
    for w in sorted(ws, key=lambda w: (w[1] + w[3]) / 2):
        yc = (w[1] + w[3]) / 2
        if rows and yc - rows[-1][0] <= tol:
            rows[-1][1].append(w)
        else:
            rows.append([yc, [w]])
    return [sorted(r[1], key=lambda w: w[0]) for r in rows]


def rules(page) -> tuple[list, list]:
    """Horizontal (y, x0, x1) and vertical (x, y0, y1) rules from drawings."""
    hs, vs = [], []
    for d in page.get_drawings():
        for it in d["items"]:
            if it[0] == "l":
                a, b = it[1], it[2]
                if abs(a.y - b.y) < 1 and abs(a.x - b.x) > 8:
                    hs.append((a.y, min(a.x, b.x), max(a.x, b.x)))
                elif abs(a.x - b.x) < 1 and abs(a.y - b.y) > 8:
                    vs.append((a.x, min(a.y, b.y), max(a.y, b.y)))
            elif it[0] == "re":
                r = it[1]
                if r.height < 2.5 and r.width > 8:
                    hs.append(((r.y0 + r.y1) / 2, r.x0, r.x1))
                elif r.width < 2.5 and r.height > 8:
                    vs.append(((r.x0 + r.x1) / 2, r.y0, r.y1))
                elif r.width > 8 and r.height > 8:
                    hs += [(r.y0, r.x0, r.x1), (r.y1, r.x0, r.x1)]
                    vs += [(r.x0, r.y0, r.y1), (r.x1, r.y0, r.y1)]
    return hs, vs


class PageInfo:
    def __init__(self, page):
        self.page = page
        self.no = page.number
        self.h = page.rect.height
        self.w = page.rect.width
        self.words = words(page)
        self.drawings = page.get_drawings()
        # symbol-font glyphs coded as control characters (a Delta as '\x03', 9701/04/M/J/03
        # 2(c)(i)) are dropped by word extraction: keep their boxes for the crop edges
        self.ctrl = [fitz.Rect(c["bbox"]) for b in page.get_text("rawdict")["blocks"]
                     for l in b.get("lines", []) for sp in l["spans"] for c in sp["chars"]
                     if ord(c["c"][:1] or " ") < 32 and c["c"] not in "\t\n\r"
                     and c["bbox"][2] - c["bbox"][0] > 1]
        self.hrules, self.vrules = rules(page)
        self.table = None          # (qcol_x0, qcol_x1, right_x) for table pages
        self.top, self.bottom = self._furniture()
        if self.no in OCR_PAGES:
            # scans: OCR garbles the running header/footer, so take them by position
            head = [w[3] for w in self.words if w[1] < 72]
            foot = [w[1] for w in self.words if w[1] > self.h - 70]
            self.top = max(self.top, max(head) + 2) if head else self.top
            self.bottom = min(self.bottom, min(foot) - 2) if foot else self.bottom
            # the scanned header table's bottom rule: start below it, on a blank pixel row
            g = gray(page, dpi=144)
            self.raw_gray = g                    # before any label is whited out
            dark = (g[:, int(45 * 2):int((self.w - 30) * 2)] < 150).sum(axis=1)
            y = int(self.top * 2)
            while y < int(self.top * 2) + 40 and y < len(dark) and dark[y] > 2:
                y += 1
            self.top = y / 2
            self.bands = [(self.top, self.bottom)]

    def _furniture(self) -> tuple[float, float]:
        ws = self.words
        top = 30.0
        for r in rows_of([w for w in ws if w[1] < 85]):
            if any(w[4] in HEADER_WORDS for w in r) or any(re.match(r"^9\d{3}(/\d\d)?$", w[4]) for w in r):
                top = max(top, max(w[3] for w in r) + 1)
        # header-table rules just below the header text
        for y, x0, x1 in self.hrules:
            if top - 2 < y < top + 8 and x1 - x0 > 150:
                top = max(top, y + 0.8)
        bottom = self.h - 30
        foot = [r for r in rows_of([w for w in ws if w[1] > self.h - 75])
                if all(FOOTER_RE.match(w[4]) for w in r) and any(w[4] in ("©", "UCLES", "Page") for w in r)]
        if foot:
            bottom = min(min(w[1] for w in r) for r in foot) - 1
        self.bands = [(top, bottom)]
        # answer tables: header row Question | Answer(s) | Mark(s), possibly
        # several tables on one page; content = the table bodies only
        heads = []
        # (tolerance 7: 'Question' may sit 6 pt below 'Answer Mark', 9701/41/O/N/16)
        for r in rows_of([w for w in ws if 15 < w[1] < bottom], tol=7.0):
            t = {w[4].lower() for w in r}       # 'Expected answer' in lower case too (9701/52/O/N/16)
            j = "".join(w[4] for w in r)
            # "Question | Marking Point | Marks | Total Marks" (9701/4x 2015) is a header too
            if ("question" in t and t & {"answer", "answers", "marking"} and t & {"marks", "mark"}) or (
                    # rotated pages print the header in split glyph runs:
                    # 'Que estion Answer Ma arks' (9701/21/O/N/18 p.5)
                    re.search(r"Que.{0,2}stion", j) and "Answer" in j and re.search(r"Ma.{0,2}rks?", j)):
                heads.append(r)
        bands = []
        for i, r in enumerate(heads):
            qw = next((w for w in r if w[4].startswith("Que")), r[0])
            rb = max(w[3] for w in r)
            below = sorted(y for y, x0, x1 in self.hrules if rb - 1 < y < rb + 14 and x0 <= qw[0])
            btop = (below[0] + 0.8) if below else rb + 2
            if self.table is None:
                xs = sorted({round(x) for x, y0, y1 in self.vrules if y1 - y0 > 8 and y0 < btop + 60 and y1 > btop - 20})
                left = [x for x in xs if x <= qw[0] + 1]
                mid = [x for x in xs if x > qw[2] - 1]
                if left and len(mid) >= 2:
                    # double rules: crop inside both lines of a pair
                    inner_l = max(x for x in mid if x - mid[0] <= 6)
                    inner_r = min(x for x in mid if mid[-1] - x <= 6)
                    self.table = (left[-1], inner_l, inner_r)
            nxt = min(w[1] for w in heads[i + 1]) - 2 if i + 1 < len(heads) else bottom
            bands.append([btop, nxt])
        if self.table and bands:
            q0, _, rx = self.table
            full = self.spanning(q0 + 2, rx - 2)
            for b in bands:
                tb = [y for y in full if b[0] < y <= b[1] + 1]
                if tb:
                    b[1] = max(tb) - 0.8
            self.bands = [tuple(b) for b in bands]
            top, bottom = bands[0][0], bands[-1][1]
        return top, bottom

    def spanning(self, x0: float, x1: float) -> list[float]:
        """y of horizontal rules covering x0..x1 (rules drawn cell by cell are joined)."""
        out = []
        for y in sorted({round(y, 1) for y, a, b in self.hrules}):
            segs = sorted((a, b) for yy, a, b in self.hrules if abs(yy - y) < 0.7)
            reach = None
            for a, b in segs:
                if reach is None:
                    if a > x0 + 1:
                        break
                    reach = b
                elif a <= reach + 1.5:
                    reach = max(reach, b)
            if reach is not None and reach >= x1 - 1 and (not out or y - out[-1] > 0.7):
                out.append(y)
        return out

    def in_band(self, y0: float, y1: float) -> bool:
        return any(b0 - 1 <= y0 and y1 <= b1 + 1 for b0, b1 in self.bands)


def inherit_tables(pages: list) -> None:
    """A table continued on a page without a repeated header row (9701/51/M/J/14
    p.3) is still a table: same Question-column rules as the page before."""
    prev = None
    for pi in pages:
        if pi.table:
            prev = pi.table
            continue
        if prev is None or pi.no in OCR_PAGES:
            continue
        q0, ql, rx = prev
        # this page's own vertical rules: the table's left rule (same x as the
        # previous page's) and a Question-column rule 30-100 pt right of it; the
        # column can be narrower than on the header page (9701/41/M/J/15 p.6-9:
        # 104 vs 112) and the rules short (9701/51/M/J/13 p.3)
        lens: dict = {}
        for xx, y0, y1 in pi.vrules:
            if y0 >= pi.top - 2:
                lens[round(xx)] = lens.get(round(xx), 0) + (y1 - y0)
        left = [x for x, L in lens.items() if abs(x - q0) <= 5 and L > 40]
        inner = [x for x, L in lens.items() if left and left[0] + 30 < x < left[0] + 100 and L > 40]
        if left and inner:
            qx = min(inner, key=lambda x: abs(x - ql))
            pi.table = (min(left), qx, rx)
            full = [y for y in pi.spanning(min(left) + 2, rx - 2) if pi.top - 2 < y <= pi.bottom + 1]
            # the last spanning rule closes the table only when no content follows it
            # (9701/51/M/J/13 p.3: a row rule at y159, the answers run on below)
            if full and not any(max(full) + 3 < w[1] < pi.bottom for w in pi.words):
                pi.bottom = max(full) - 0.8
            pi.bands = [(pi.top, pi.bottom)]
            prev = pi.table


# ---------------------------------------------------------------- keys
class Key:
    def __init__(self, path, pno, row, label_ws):
        self.path = path
        self.pno = pno
        self.row = row
        self.label_ws = label_ws
        self.top = min(w[1] for w in row)
        self.x = label_ws[0][0]
        self.printed = None


def parse_lead(row: list, xmax: float) -> tuple[dict, list] | None:
    """Label pieces at the start of a row -> ({q,l,r,t}, label words)."""
    got: dict = {}
    used = []
    level = 0                      # 1 q, 2 l, 3 r, 4 t
    for w in row:
        if w[0] > xmax:
            break
        s = w[4].replace("–", "-").strip()
        if level == 0 and re.match(r"^[,;]\d", s):
            s = s[1:]                    # ',4(d)(i)': stray comma glued to the key (9701/42/F/M/17)
        if level == 0 and w[0] < 60 and re.fullmatch(r"\d{1,2}\.", s):
            s = s[:-1]                   # question number printed '2.' in the question column (9701/41/M/J/12)
        if level == 0 and P_QWORD.match(s):
            used.append(w)
            continue
        m = P_COMPOUND.match(s)
        if m and level == 0:
            got["q"], got["l"] = m.group(1), m.group(2)
            if m.group(3):
                got["r"] = m.group(3)[1:-1]
            if m.group(4):
                got["t"] = m.group(4)
            used.append(w)
            level = 4 if m.group(4) else (3 if m.group(3) else 2)
            continue
        m = re.match(r"^\(([a-h])\)\(([ivx]{1,4})\)(?:([1-9])\.?)?$", s)
        if m and level < 2:              # fused "(a)(i)"
            got["l"], got["r"] = m.group(1), m.group(2)
            if m.group(3):
                got["t"] = m.group(3)
            used.append(w)
            level = 4 if m.group(3) else 3
            continue
        m = P_Q.match(s)
        if m and level == 0:
            got["q"] = m.group(1)
            used.append(w)
            level = 1
            continue
        m = P_L.match(s)
        if m and level < 2:
            got["l"] = m.group(1)
            used.append(w)
            level = 2
            continue
        m = P_R.match(s)
        if m and level < 3:
            got["r"] = m.group(1)
            if m.group(2):
                got["t"] = m.group(2)
            used.append(w)
            level = 4 if m.group(2) else 3
            continue
        m = P_T.match(s) or (level == 3 and re.match(r"^([1-9])$", s))
        if m and level < 4:
            got["t"] = m.group(1)
            used.append(w)
            level = 4
            continue
        break
    if not got or (used and used[0][4] == "Question" and "q" not in got):
        return None
    return got, used


def resolve(got: dict, cur: tuple) -> tuple:
    """Fill the levels a key leaves out from the current key."""
    if "q" in got:
        base = (got["q"],)
    elif "l" in got:
        base = cur[:1]
    elif "r" in got:
        base = cur[:2]
    else:
        base = cur[:3]
    out = list(base)
    for k in ("l", "r", "t"):
        if k in got:
            out.append(got[k])
    return tuple(out)


CONT_LABELS: list = []


def find_keys(pages: list[PageInfo], order: dict, leaves: list[tuple]) -> list[Key]:
    keys: list[Key] = []
    cur: tuple = ()
    cur_idx = -1
    qcol = None
    task_parents = {t[:3] for t in leaves if len(t) == 4}
    leafset = set(leaves)
    if any(pi.table for pi in pages):
        # table mark schemes: keys live only in the Question column of the
        # answer tables (front pages number their marking principles 1, 2, ...)
        pages = [pi for pi in pages if pi.table]
    # "Question 2" headings (Paper 5): then a bare number starting a line is a
    # numbered marking point ("2 Polarity of LED correct ..."), never a question
    qword_style = any(len(r) > 1 and r[0][4] == "Question" and P_Q.match(r[1][4]) and r[0][0] < 80
                      for pi in pages if not pi.table for r in rows_of(pi.words))
    # numbered marking points ("1 Repeat experiment ...", "2 ...", "3 ...") form
    # runs of consecutive integers in one column: never question numbers
    listitems = set()
    appendix_q = None
    for pi in pages:
        # on table pages only numbers well right of the question number's own
        # position can be marking points ('1 ... 8' at x101 in the Question
        # column, 9701/51/M/J/13 p.2)
        if pi.table and not any(P_Q.match(w[4]) and w[0] > pi.table[0] + 25 and w[0] < pi.table[1]
                                for w in pi.words):
            continue
        lead = [w for w in pi.words if P_Q.match(w[4]) and w[0] < (pi.table[1] if pi.table else 100)
                and (not pi.table or w[0] > pi.table[0] + 25)
                and not any(v[2] <= w[0] and abs((v[1] + v[3]) / 2 - (w[1] + w[3]) / 2) < 3 for v in pi.words)]
        for x in {round(w[0]) for w in lead}:
            col = sorted([w for w in lead if abs(w[0] - x) <= 3], key=lambda w: w[1])
            run = [col[0]] if col else []
            for w in col[1:] + [None]:
                if w is not None and int(w[4]) == int(run[-1][4]) + 1 and w[1] - run[-1][1] < 80:
                    run.append(w)
                    continue
                if len(run) >= 3:
                    listitems.update(id_of(v) for v in run)
                run = [w] if w is not None else []
    for pi in pages:
        xmax = pi.table[1] if pi.table else 160
        if pi.no in OCR_PAGES:
            qcol = None              # scans sit at a different offset on every page
        for row in rows_of([w for w in pi.words if pi.in_band(w[1], w[3])]):
            if pi.table and row[0][0] > pi.table[1]:
                continue
            if re.match(r"^Uncertainties\s+in\s+Question\s+\d+$", " ".join(w[4] for w in row)):
                appendix_q = cur[:1] if cur else None   # what follows refers back to parts
                continue
            parsed = parse_lead(row, xmax)
            if not parsed:
                continue
            got, used = parsed
            if not used or id_of(used[0]) in listitems:
                continue
            nxt_t = str(int(cur[3]) + 1) if len(cur) == 4 else "1"
            if (set(got) == {"q"} and len(cur) >= 3 and cur[:3] in task_parents and qcol is not None
                    and used[0][0] > qcol + 25 and got["q"] == nxt_t):
                got = {"t": got["q"]}       # "2 E = mc2": task 2 printed without its dot
            if "t" in got and resolve(got, cur)[:3] not in task_parents and used and \
                    re.match(r"^[1-9]\.?$", used[-1][4]):
                # "(ii) 8 Hz": a number after a roman is the answer, unless the QP numbers tasks here
                got = {k: v for k, v in got.items() if k != "t"}
                used = used[:-1]
                if not got:
                    continue
            path = resolve(got, cur)
            # "(i)" after "(h)" is the letter part (i) where the QP has one
            # (9701 Paper 5 Q1(i)); a QP letter (i) and roman (i) under the
            # question both give the path (q, "i")
            if path not in order and set(got) == {"r"} and cur and (cur[0], got["r"]) in order \
                    and got["r"] in ("i", "j", "k"):
                path = (cur[0], got["r"])
            # a task "1." only where the QP itself has numbered task leaves
            if "t" in got and "r" not in got and "l" not in got and "q" not in got:
                if path[:3] not in task_parents:
                    continue
            node = path if path in order else None
            printed = None
            if node is None and len(path) == 4 and path[:3] in order:
                node = path            # MS splits a QP leaf into numbered tasks
            if node is None and path[:-1] in leafset and path[-1] in ("i", "1"):
                # misprinted key: "2(a)(i)" where the QP part 2(a) has no (i)
                printed, path = path, path[:-1]
                node = path
            if node is None:
                continue
            if (len(path) == 1 and keys and keys[-1].path == path and abs(used[0][0] - keys[-1].x) < 10
                    and not pi.table):
                # the same bare question number again before any of its parts:
                # the earlier one was a numbered marking point of the previous
                # question ("2 Additional detail ..."); the later one is the heading
                keys[-1] = Key(path, pi.no, row, used)
                continue
            idx = order.get(node, order.get(node[:3], -1) + 0.5 + (int(node[3]) / 100 if len(node) == 4 else 0))
            if path == cur:
                CONT_LABELS.append((pi.no, used))   # key printed again (continuation page / next row)
                continue
            if appendix_q and path[:1] == appendix_q and node is not None and "q" not in got:
                keys.append(Key(path, pi.no, row, used))
                keys[-1].revisit = True
                cur, cur_idx = path, max(cur_idx, idx)
                continue
            if idx <= cur_idx:
                # a second pass over parts already keyed in this question (old
                # Paper 5 "Treatment of errors": (b) ... (c)(i) ... (d) again):
                # the rows are appended to that part.  Only at a key column
                # already used, and only for the current question.
                seen = [k for k in keys if k.path == path]
                if (seen and path[0] == cur[0] and not pi.table
                        and any(abs(used[0][0] - k.x) < 8 for k in keys if len(k.label_ws) and
                                k.label_ws[0][4] == used[0][4])):
                    keys.append(Key(path, pi.no, row, used))
                    keys[-1].revisit = True
                    cur, cur_idx = path, idx
                continue
            if cur and path[0] != cur[0] and int(path[0]) != int(cur[0]) + 1 and not (
                    pi.no in OCR_PAGES and int(path[0]) == int(cur[0]) + 2 and "q" in got):
                continue
            if qword_style and not pi.table and "q" in got and used[0][4] != "Question":
                continue
            if not pi.table and "q" in got and len(used) and P_Q.match(used[0][4]):
                if qcol is not None and abs(used[0][0] - qcol) > 18:
                    continue
                if qcol is None:
                    qcol = used[0][0]
            keys.append(Key(path, pi.no, row, used))
            keys[-1].printed = printed
            if appendix_q and path[:1] != appendix_q:
                appendix_q = None              # a real next question ends the appendix
            cur, cur_idx = path, idx
    return keys


# ---------------------------------------------------------------- geometry of segments
def gray(page, clip=None, dpi=72) -> np.ndarray:
    pix = page.get_pixmap(clip=clip, dpi=dpi, colorspace=fitz.csGRAY)
    return np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width)


def cut_above(pi: PageInfo, key: Key, prev_top: float, img: np.ndarray) -> tuple[float, float]:
    """(end of the previous row, start of this key's row): table -> either
    side of the row rule; prose -> the middle of the blank gap above the line."""
    lt = min(w[1] for w in key.label_ws)
    lb = max(w[3] for w in key.label_ws)
    # the key's own line: words centred in the label band (superscripts) and
    # fraction numerators sitting on a short bar drawn within the line
    own = [w for w in pi.words if lt <= (w[1] + w[3]) / 2 <= lb + 2
           or (w[3] > lt + 1.5 and w[1] < lb and w[0] >= key.label_ws[-1][2])]
    for y, x0, x1 in pi.hrules:
        if x1 - x0 < 400 and lt - 2 <= y <= lb + 2 and x0 >= key.label_ws[-1][2]:
            own += [w for w in pi.words if y - 20 <= w[1] and w[3] <= y + 1 and w[0] < x1 and w[2] > x0]
    top = min([lt] + [w[1] for w in own])
    ownset = {id_of(w) for w in own}
    above = [w[3] for w in pi.words if w[1] >= prev_top - 1 and (w[1] + w[3]) / 2 < lt and w[3] < lb
             and id_of(w) not in ownset]
    prev_bottom = max(above) if above else max(prev_top, pi.top)
    if not pi.table:
        # a skill heading right above the key ("Graph (3 marks)") introduces it
        prior = rows_of([w for w in pi.words if w[1] >= prev_top - 1 and w[3] <= lt + 0.5
                         and id_of(w) not in ownset and w[1] > max(prev_top, pi.top) - 1])
        if prior and HEADING_RE.match(" ".join(w[4] for w in prior[-1])) and len(prior) > 1:
            head = prior[-1]
            top = min(top, min(w[1] for w in head))
            ownset |= {id_of(w) for w in head}
            rest = [w[3] for r in prior[:-1] for w in r]
            prev_bottom = max(rest) if rest else max(prev_top, pi.top)
    if pi.no in OCR_PAGES:
        # scans: OCR boxes are a few points off; find the printed line around the
        # label in the pixels and cut in the blank gap above it
        sc = img.shape[0] / pi.h
        # OCR boxes can sit several points off the printed line: snap the label to
        # the ink line in its own column nearest to where OCR put it
        lx0 = int(max(0, min(w[0] for w in key.label_ws) - 2) * sc)
        lx1 = int((max(w[2] for w in key.label_ws) + 2) * sc)
        raw = getattr(pi, "raw_gray", img)
        if raw.shape != img.shape:
            raw = img
        col = (raw[:, lx0:lx1] < 150).sum(axis=1) > 0
        runs, y = [], int((lt - 12) * sc)
        while y < min(len(col), int((lb + 12) * sc)):
            if col[y]:
                y0 = y
                while y < len(col) and col[y]:
                    y += 1
                if y - y0 >= 4:
                    runs.append((y0, y))
            y += 1
        if runs:
            cy = (lt + lb) / 2 * sc
            r0, r1 = min(runs, key=lambda r: abs((r[0] + r[1]) / 2 - cy))
            lt, lb = r0 / sc, r1 / sc
        # the line's own top: ascenders/superscripts of its text reach above the label
        rawd = (raw[:, int(45 * sc):int((pi.w - 30) * sc)] < 150).sum(axis=1)
        t = int(lt * sc)
        while t - 1 > int(max(prev_top + 2, pi.top) * sc) and rawd[t - 1] > 2 and int(lt * sc) - t < int(2.5 * sc):
            t -= 1
        lt = t / sc
        x0, x1 = int(45 * sc), int((pi.w - 30) * sc)
        dark = (img[:, x0:x1] < 150).sum(axis=1)
        blank = dark <= 2
        y = int((lt + lb) / 2 * sc)
        floor = int(max(prev_top + 2, pi.top) * sc)
        while y > floor and not blank[y]:
            y -= 1
        hi = y
        while y > floor and blank[y - 1]:
            y -= 1
        if blank[hi] and hi > floor and hi >= int((lt - 4) * sc):
            c = (y + hi + 1) / 2 / sc
            return c, c
        if blank[hi] and hi > floor:
            # the gap above is far up (an empty band): cut just above this line's top
            c = max((y + hi + 1) / 2 / sc, lt - 2.5)
            return c, c
        # lines touch (superscripts, dot leaders): least-ink row just above the label
        a0, a1 = int((lt - 6) * sc), int((lt + 1) * sc)
        a0 = max(a0, floor)
        if a1 > a0:
            yy = a0 + int(np.argmin(dark[a0:a1 + 1]))
            c = (yy + 0.5) / sc
            return c, c
    if pi.table:
        q0, q1, _ = pi.table
        cands = [y for y in pi.spanning(q0 + 3, q1 - 3) if prev_bottom - 2 <= y <= lt + 1.5]
        if cands:
            return max(cands) - 0.8, max(cands) + 0.8
    sc = img.shape[0] / pi.h
    cols = np.zeros(img.shape[1], bool)
    cols[int(40 * sc):int((pi.w - 30) * sc)] = True
    for x, y0, y1 in pi.vrules:          # grid columns of prose-page tables never count as ink
        if y1 - y0 > 20:
            cols[max(0, int((x - 1) * sc)): int((x + 1.5) * sc)] = False

    def blank(y):
        return 0 <= y < img.shape[0] and (img[y, cols] > 235).all()

    def least_ink(a, b):
        """lines touch: the pixel row with the least ink near the join."""
        a, b = max(0, int(a * sc)), min(img.shape[0] - 1, int(b * sc))
        if b <= a:
            return (a + b) / 2 / sc
        ink = [(img[y, cols] < 200).sum() for y in range(a, b + 1)]
        return (a + int(np.argmin(ink)) + 0.5) / sc

    if prev_bottom >= top:                       # lines touch: no gap to find
        c = least_ink(top - 2.5, prev_bottom + 2.5)
        return c, c
    lo, hi = int(prev_bottom * sc), int(top * sc)
    best = None
    for y in range(hi - 1, lo - 1, -1):
        if blank(y):
            best = y
            break
    if best is None:
        c = least_ink(prev_bottom - 2.5, top + 2.5)
        return c, c
    run_lo = best
    while run_lo - 1 >= lo and blank(run_lo - 1):
        run_lo -= 1
    c = (run_lo + best + 1) / 2 / sc
    return c, c


def build_segments(pages: list[PageInfo], keys: list[Key]) -> dict[tuple, list]:
    by_no = {pi.no: pi for pi in pages}
    imgs = {pi.no: gray(pi.page, dpi=144) for pi in pages}
    cuts = []
    for i, k in enumerate(keys):
        pi = by_no[k.pno]
        prev = [kk for kk in keys[:i] if kk.pno == k.pno]
        prev_top = min(w[1] for w in prev[-1].label_ws) if prev else pi.top - 2
        cuts.append(cut_above(pi, k, prev_top, imgs[k.pno]))
    for i in range(1, len(keys)):        # keys printed on one line share one cut
        if keys[i].pno == keys[i - 1].pno and abs(keys[i].top - keys[i - 1].top) < 4:
            c = (min(cuts[i - 1][0], cuts[i][0]), min(cuts[i - 1][1], cuts[i][1]))
            cuts[i - 1] = cuts[i] = c
    order = [pi.no for pi in pages]
    segs: dict[tuple, list] = {}
    for i, k in enumerate(keys):
        start_p, start_y = k.pno, cuts[i][1]
        if i + 1 < len(keys):
            end_p, end_y = keys[i + 1].pno, cuts[i + 1][0]
        else:
            end_p, end_y = order[-1], by_no[order[-1]].bottom
        out = []
        for pno in order[order.index(start_p): order.index(end_p) + 1]:
            pi = by_no[pno]
            y0 = start_y if pno == start_p else pi.top
            y1 = end_y if pno == end_p else pi.bottom
            for b0, b1 in pi.bands:          # table bodies only (header rows are furniture)
                a, b = max(y0, b0), min(y1, b1)
                if b - a >= 2:
                    out.append([pno, a, b])
        segs.setdefault(k.path, []).extend(out)
    return segs


def _cell_rule(pi, r):
    """A thin horizontal running from one table rule to the next: a row rule piece."""
    cols = [x for x, n in pi._vcount.items() if n >= 3]
    return any(abs(r.x0 - c) < 2 for c in cols) and any(abs(r.x1 - c) < 2 for c in cols)


def x_range(pi: PageInfo, y0: float, y1: float, label_ids: set) -> tuple[float, float] | None:
    ws = [w for w in pi.words if y0 <= (w[1] + w[3]) / 2 <= y1 and (pi.no, id_of(w)) not in label_ids]
    if not ws:
        # nothing but rules / whited-out labels, unless a drawing (an MS sketch) sits here
        figs = [d["rect"] for d in pi.drawings if d["rect"].width > 6 and d["rect"].height > 6
                and d["rect"].y0 >= y0 - 1 and d["rect"].y1 <= y1 + 1]
        if not figs and pi.no in OCR_PAGES and y1 - y0 > 4:
            # scan: OCR may drop a whole line; trust the pixels
            g = gray(pi.page, fitz.Rect(60, y0 + 1, pi.w - 30, y1 - 1), dpi=72)
            if (g < 160).sum() > 30:
                return 30.0, pi.w - 1
        if not figs:
            return None
        if pi.table:
            return pi.table[1] + 1.0, pi.table[2] - 1.0
        return min(r.x0 for r in figs) - 3, max(r.x1 for r in figs) + 3
    if pi.table and not getattr(pi, "full_width", False):
        # a drawn structure in the Answer cell may start left of the column rule
        # (9701/21/M/J/12 5(c)(i)): widen over it, never over full-row rectangles
        if not hasattr(pi, "_figs"):
            # thin vertical segments that recur at one x down the page are table rules
            pi._vcount = {}
            for d in pi.drawings:
                if d["rect"].width < 1.5 and d["rect"].height > 2:
                    # a tall line is a rule on its own
                    pi._vcount[round(d["rect"].x0)] = pi._vcount.get(round(d["rect"].x0), 0) + \
                        (3 if d["rect"].height > 40 else 1)
            pi._figs = [fitz.Rect(i["bbox"]) for i in pi.page.get_image_info()] + \
                       [d["rect"] for d in pi.drawings if (d["rect"].width > 2 or d["rect"].height > 2)
                    # never table rules: a thin vertical recurring at one x (3+ segments) or over 40 pt, or a horizontal
                    # line over 120 pt (a skeletal bond can be a 54 pt line, 9701/23/O/N/13 5(a))
                    and not (d["rect"].width < 1.5 and pi._vcount.get(round(d["rect"].x0), 0) >= 3)
                    and not (d["rect"].height < 1.5 and (d["rect"].width > 120 or _cell_rule(pi, d["rect"])))]
        # (never a cell's own box or fill, which starts on the rule: 9702/42/M/J/17)
        figs = [r for r in pi._figs if y0 <= (r.y0 + r.y1) / 2 <= y1 and pi.table[0] + 2 < r.x0 < pi.table[1] - 1
                and r.width < (pi.table[2] - pi.table[1]) * 0.6 and not (r.width < 1.5 and r.height > (y1 - y0) * 0.8)]
        # answer text set a point or two left of the Question-column rule
        # (9701/41/M/J/15 p.6-9: rule at 104, text from ~102)
        near = [w[0] for w in ws if pi.table[1] - 8 < w[0] < pi.table[1] + 1]
        x0 = min([pi.table[1] + 1.0] + [r.x0 - 2 for r in figs] + [x - 1.5 for x in near])
        xr = pi.table[2] - 1.0
        # a cell box's edge 6 pt inside the drawn right rule reads as a double rule and
        # cut the Marks digits (9700/52/O/N/23): widen over words the edge cuts, never
        # onto the next rule
        cut = [w[2] for w in ws if w[0] < xr < w[2]]
        if cut:
            outer = [x for x, a, b in pi.vrules if pi.table[2] + 1 < x <= pi.table[2] + 10]
            xr = min([max(cut) + 0.8] + [x - 0.8 for x in outer])
        return x0, xr
    if pi.table:
        # override full_width_pages: an answer table that spans the Question
        # column too (9701/53/O/N/12 p.3): from the table's left rule
        return pi.table[0] + 1.0, pi.table[2] - 1.0
    x0 = min(w[0] for w in ws) - (8 if pi.no in OCR_PAGES else 3)
    lead = [r.x0 for r in pi.ctrl if y0 <= (r.y0 + r.y1) / 2 <= y1 and x0 - 12 < r.x0 < x0 + 3]
    if lead:
        x0 = min(lead) - 3
    right = max([w[2] for w in pi.words if pi.top <= w[1] <= pi.bottom] + [w[2] for w in ws])
    if pi.no in OCR_PAGES:
        # scans: OCR boxes are loose and lines can be lost: take the left edge from the
        # ink right of the (whited-out) label column, and the full width on the right
        lab = max([w[2] for w in pi.words if (pi.no, id_of(w)) in label_ids and y0 - 2 <= w[1] <= y1] + [30.0])
        g = gray(pi.page, fitz.Rect(lab + 1, y0 + 0.5, x0 + 8, y1 - 0.5), dpi=144)
        cols = np.where((g < 150).sum(axis=0) > 1)[0]
        if len(cols):
            x0 = min(x0, lab + 1 + cols[0] / 2 - 4)
        return max(30.0, x0), pi.w - 1
    # pictures and drawings in the band count too: a pasted structure or a graph's
    # axis title can start left of every word (9701/06/M/J/05 1(a)(ii), 9701/06/O/N/04 1(b)(i))
    if not hasattr(pi, "_figs"):
        # thin vertical segments that recur at one x down the page are table rules
        pi._vcount = {}
        for d in pi.drawings:
            if d["rect"].width < 1.5 and d["rect"].height > 2:
                # a tall line is a rule on its own
                pi._vcount[round(d["rect"].x0)] = pi._vcount.get(round(d["rect"].x0), 0) + \
                    (3 if d["rect"].height > 40 else 1)
        pi._figs = [fitz.Rect(i["bbox"]) for i in pi.page.get_image_info()] + \
                   [d["rect"] for d in pi.drawings if (d["rect"].width > 2 or d["rect"].height > 2)
                    # never table rules: a thin vertical recurring at one x (3+ segments) or over 40 pt, or a horizontal
                    # line over 120 pt (a skeletal bond can be a 54 pt line, 9701/23/O/N/13 5(a))
                    and not (d["rect"].width < 1.5 and pi._vcount.get(round(d["rect"].x0), 0) >= 3)
                    and not (d["rect"].height < 1.5 and (d["rect"].width > 120 or _cell_rule(pi, d["rect"])))]
    # thin bond lines count too (a structure drawn from 0.5 pt strokes, 9701/21/M/J/12
    # 5(c)(i)), but only within 80 pt of the text and never a full-height column rule
    band = [r for r in pi._figs if y0 <= (r.y0 + r.y1) / 2 <= y1 and r.x0 > 35 and r.width < pi.w * 0.8
            and not (r.width < 1.5 and r.height > (y1 - y0) * 0.8)]
    # a sizeable drawing counts wherever it is (a structure left of a lone '(1)',
    # 9701/21/O/N/12 4(b)(i)); thin strokes only within 80 pt of what is already in
    big = [r for r in band if r.width > 6 and r.height > 6]
    if big:
        x0 = min(x0, min(r.x0 for r in big) - 3)
    figs = big + [r for r in band if not (r.width > 6 and r.height > 6) and r.x0 > x0 - 80]
    if figs:
        x0 = min(x0, min(r.x0 for r in figs) - 3)
        right = max(right, max(r.x1 for r in figs))
    # a pasted picture is never a rule, however wide (9700/22/O/N/13 6(a): antibody
    # diagram 488 pt wide ran past the crop and its labels were cut)
    pics = [fitz.Rect(i["bbox"]) for i in pi.page.get_image_info()]
    pics = [r for r in pics if y0 <= (r.y0 + r.y1) / 2 <= y1 and r.width > 40 and r.height > 40]
    if pics:
        right = max(right, max(r.x1 for r in pics))
    # the 15 pt page-edge margin never cuts the band's own words (9700/21/M/J/15 2(c):
    # a ';' printed to x580.6)
    return x0, min(max(pi.w - 15, right + 1), pi.w - 2, right + 3)


def id_of(w) -> tuple:
    return (round(w[0], 1), round(w[1], 1), w[4])


# ---------------------------------------------------------------- render
def edge_fragments(a: np.ndarray, im: Image.Image):
    """White out ink cut by the slice's top/bottom edge (a neighbouring line's
    glyph tips) when that ink piece stays within 3.2 pt of the edge."""
    band = int(3.2 * K)
    h, w = a.shape
    ink = a < 200
    kill = np.zeros_like(ink)
    for edge_rows in (range(0, min(band + 1, h)), range(h - 1, max(h - band - 2, -1), -1)):
        rows = list(edge_rows)
        if not rows:
            continue
        sub = ink[min(rows):max(rows) + 1]
        seen = np.zeros_like(sub)
        start = 0 if rows[0] == min(rows) else sub.shape[0] - 1
        for x in np.where(sub[start])[0]:
            if seen[start, x]:
                continue
            stack, comp, deep = [(start, x)], [], False
            seen[start, x] = True
            while stack:
                y, xx = stack.pop()
                comp.append((y, xx))
                if (start == 0 and y == sub.shape[0] - 1) or (start != 0 and y == 0):
                    deep = True            # reaches past the band: real content
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        ny, nx = y + dy, xx + dx
                        if 0 <= ny < sub.shape[0] and 0 <= nx < w and sub[ny, nx] and not seen[ny, nx]:
                            seen[ny, nx] = True
                            stack.append((ny, nx))
            if not deep and len(comp) < 400:
                off = min(rows)
                for y, xx in comp:
                    kill[off + y, xx] = True
    if kill.any():
        arr = np.array(im)
        arr[kill] = 255
        im = Image.fromarray(arr)
        a = np.asarray(im.convert("L"))
    return a, im


PIXEL_MASKS: list = []     # [pno, x0, y0, x1, y1]: also whitened in the rendered pixels


def render_slices(doc, slices: list) -> Image.Image:
    images, lefts = [], []
    for pno, x0, y0, x1, y1 in slices:
        pix = doc[pno].get_pixmap(clip=fitz.Rect(x0, y0, x1, y1), dpi=DPI)
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        # a white rectangle drawn over text can leave a faint grey ghost of the
        # glyphs (min ~227 of 255, '[Total: 12]' in 9701/21/O/N/05): whiten the
        # masked areas in the pixels as well
        hit = [m for m in PIXEL_MASKS if m[0] == pno and m[1] < x1 and m[3] > x0 and m[2] < y1 and m[4] > y0]
        if hit:
            arr0 = np.array(im)
            for m in hit:
                c0, c1 = int(max(0, (m[1] - x0) * K)), int(min(arr0.shape[1], (m[3] - x0) * K + 1))
                r0, r1 = int(max(0, (m[2] - y0) * K)), int(min(arr0.shape[0], (m[4] - y0) * K + 1))
                # ghost pixels only (~186-254 here, also on the mask's edge rows): the
                # real ink of an abutting row stays (a '[3]' just above a masked
                # 'Total [12]', 9702/02/M/J/04 4(c))
                cell = arr0[r0:r1, c0:c1]
                cell[cell.min(axis=-1) > 150] = 255
            im = Image.fromarray(arr0)
        a = np.asarray(im.convert("L"))
        rule_cols = (a < 160).mean(axis=0) > 0.85        # table column rules run full height
        b = a[:, ~rule_cols] if (~rule_cols).any() else a
        rows = np.where((b < 235).any(axis=1))[0]
        if not len(rows):
            continue
        a, im = edge_fragments(a, im)
        b = a[:, ~rule_cols] if (~rule_cols).any() else a
        rows = np.where((b < 235).any(axis=1))[0]
        if not len(rows):
            continue
        # a sliver (< 2.2 pt) of a neighbouring line's glyphs at the very top or
        # bottom edge, separated by a blank gap, is whited out (touching lines)
        runs = np.split(rows, np.where(np.diff(rows) > 1)[0] + 1)
        thin = 3.2 * K
        arr = np.array(im)
        if len(runs) > 1 and runs[0][-1] - runs[0][0] + 1 < thin and runs[0][0] < 2 * K:
            arr[runs[0][0]:runs[0][-1] + 1, :] = 255
            runs = runs[1:]
        if len(runs) > 1 and runs[-1][-1] - runs[-1][0] + 1 < thin and runs[-1][-1] > a.shape[0] - 1 - 2 * K:
            arr[runs[-1][0]:runs[-1][-1] + 1, :] = 255
            runs = runs[:-1]
        im = Image.fromarray(arr)
        rows = np.concatenate(runs)
        pad = int(PAD_PT * K)
        im = im.crop((0, max(0, rows[0] - pad), im.width, min(im.height, rows[-1] + pad + 1)))
        images.append(im)
        lefts.append(x0)
    if not images:
        return None
    left0 = min(lefts)
    offs = [round((lx - left0) * K) for lx in lefts]
    width = max(im.width + o for im, o in zip(images, offs))
    sep = round(SEP_PT * K)
    final = Image.new("RGB", (width, sum(im.height for im in images) + sep * (len(images) - 1)), "white")
    y = 0
    for im, o in zip(images, offs):
        final.paste(im, (o, y))
        y += im.height + sep
    return final


# ---------------------------------------------------------------- component filter
def page_component(pi: PageInfo) -> str | None:
    for r in rows_of([w for w in pi.words if w[1] < 85]):
        t = [w[4] for w in sorted(r, key=lambda w: w[0])]
        for i, s in enumerate(t):
            m = re.match(r"^9\d{3}/(\d{1,2})$", s)
            if m:
                return m.group(1).lstrip("0")
            if re.match(r"^9\d{3}$", s) and i + 1 < len(t) and re.match(r"^\d{1,2}$", t[i + 1]):
                return t[i + 1].lstrip("0")
    return None


# ---------------------------------------------------------------- MCQ
def mcq(doc, pages: list[PageInfo], leaves: list[tuple], outdir: Path, prefix: str, src: str,
        ov: dict | None = None) -> int:
    # override "absent" {"13": "reason"}: questions the key prints as "Question Discounted" (no answer)
    absent = {k.lstrip("Q"): v for k, v in (ov or {}).get("absent", {}).items()}
    ans: dict[str, str] = {}
    for pi in pages:
        ws = [w for w in pi.words if pi.top <= w[1] <= pi.bottom]
        for w in ws:
            if not re.fullmatch(r"\d{1,2}", w[4]):
                continue
            yc = (w[1] + w[3]) / 2
            right = [v for v in ws if v[0] > w[2] and v[0] - w[2] < 110 and abs((v[1] + v[3]) / 2 - yc) < 7]
            right.sort(key=lambda v: v[0])
            if right and re.fullmatch(r"[A-D](\s*(/|or|and)\s*[A-D])*|[A-D]/[A-D]", right[0][4]):
                ans.setdefault(w[4], right[0][4])
    want = [t[0] for t in leaves]
    with open(outdir / f"{prefix}-answers.csv", "w", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["label", "answer"])
        for q in want:
            wr.writerow([f"Q{q}", ans.get(q, "")])
    missing = [q for q in want if q not in ans and q not in absent]
    extra = sorted(set(ans) - set(want), key=int)
    bad_absent = sorted(q for q in absent if q in ans or q not in want)
    if bad_absent:
        missing += [f"absent-but-{'keyed' if q in ans else 'unknown'}:{q}" for q in bad_absent]
    meta = {"source_pdf": src, "prefix": prefix, "kind": "mcq_key", "answers": ans}
    if absent:
        meta["absent"] = absent
    (outdir / f"{prefix}-ms-provenance.json").write_text(json.dumps(meta, indent=1) + "\n")
    print(f"MCQ answers={len(ans)} expected={len(want)} missing={missing} extra={extra}"
          + (f" absent={sorted(absent, key=int)}" if absent else ""))
    if not missing and not extra:
        print("MS_OK")
    return 0


# ---------------------------------------------------------------- main
def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    src, qprov, outdir, prefix = args[:4]
    comp = sys.argv[sys.argv.index("--component") + 1] if "--component" in sys.argv else None
    is_mcq = "--mcq" in sys.argv
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    for f in out.glob(f"{prefix}-Q*.png"):
        f.unlink()
    prov = json.load(open(qprov))
    leaves, order = qp_tree(prov)
    doc = fitz.open(src)
    for p in doc:
        if p.rotation:
            p.remove_rotation()
    pages = [PageInfo(p) for p in doc]
    inherit_tables(pages)
    ov = json.load(open(sys.argv[sys.argv.index("--overrides") + 1])) if "--overrides" in sys.argv else {}
    if comp:
        # component_pages: booklet pages of this component whose header misprints another paper
        # number (9700_s04_ms.pdf pp. 8-14 are Paper 2 but headed '9700 4')
        cpages = set(ov.get("component_pages", []))
        pages = [pi for pi in pages if pi.no + 1 in cpages or page_component(pi) == comp.lstrip("0")]
        if not pages:
            print(f"ERROR no pages for component {comp}")
            return 2
    if is_mcq:
        return mcq(doc, pages, leaves, out, prefix, src, ov)

    pages = [pi for pi in pages if pi.no + 1 not in ov.get("skip_pages", [])]   # e.g. a scanned cover
    for pi in pages:                       # full_width_pages: crops from the table's left rule
        if pi.no + 1 in ov.get("full_width_pages", []):
            pi.full_width = True
        # page_bottom {page: y}: on scans every word in the bottom 70 pt is taken as
        # footer; content printed that low (a graph's axis numbers, 9701/06/O/N/02 7(d))
        # is kept by moving the page's content bottom down by hand
        if str(pi.no + 1) in ov.get("page_bottom", {}):
            pi.bottom = float(ov["page_bottom"][str(pi.no + 1)])
            pi.bands = [(pi.top, pi.bottom)]
    keys = find_keys(pages, order, leaves)
    # add_keys {label: [page, y, x_label_end]}: printed keys the text layer/OCR lost
    pidx = {pi.no: i for i, pi in enumerate(pages)}
    for lab, (pg, y, xend) in ov.get("add_keys", {}).items():
        pi = next(pi for pi in pages if pi.no == pg - 1)
        row = min(rows_of(pi.words), key=lambda r: abs(min(w[1] for w in r) - y))
        if abs(min(w[1] for w in row) - y) > 6:
            row = [(30.0, y, float(xend), y + 10, "#")]     # OCR lost this line
        lw = [w for w in row if w[2] <= xend] or [(30.0, y, float(xend), y + 10, "#")]
        if pi.no in OCR_PAGES:
            # mask the printed label area by position (OCR may have merged it with text)
            lw = [w for w in lw if w[4] != "#"] + [(30.0, y - 1.0, float(xend), y + 11.5, "#")]
        k = Key(label_tuple(lab), pg - 1, row, lw)
        k.manual = True
        k.top = min([w[1] for w in row] + [y])
        keys = [kk for kk in keys if kk.path != k.path] + [k]
    keys.sort(key=lambda k: (pidx[k.pno], k.top, len(k.path)))
    for i in range(1, len(keys)):        # same printed line: parent before its child
        a, b = keys[i - 1], keys[i]
        if a.pno == b.pno and abs(a.top - b.top) < 4 and a.path[:len(b.path)] == b.path and len(b.path) < len(a.path):
            keys[i - 1], keys[i] = b, a
    if not keys and not ov.get("segments"):
        print("ERROR no keys found")
        return 2
    allpages = {pi.no: pi for pi in pages}
    first = pages.index(next(pi for pi in pages if pi.no == keys[0].pno)) if keys else 0
    pages = pages[first:]
    # furniture inside the content band: Section headings
    masks = []
    for pi in pages:
        for r in rows_of([w for w in pi.words if pi.top <= w[1] <= pi.bottom]):
            if SECTION_RE.match(" ".join(w[4] for w in r)) or COLHEAD_RE.match(" ".join(w[4] for w in r)):
                masks.append([pi.no, min(w[0] for w in r) - 1, min(w[1] for w in r) - 1,
                              max(w[2] for w in r) + 1, max(w[3] for w in r) + 1])
    # page-qualified: the same label position recurs on other pages (9701/43/O/N/15 p.6/p.7 "(iii)")
    label_ids = {(k.pno, id_of(w)) for k in keys for w in k.label_ws}
    for k in keys:
        for w in k.label_ws:
            masks.append([k.pno, w[0] - 1.5, w[1] - 0.5, w[2] + 1.5, w[3] + 1.0])
        if k.pno in OCR_PAGES and k.label_ws and not getattr(k, "manual", False):
            # scans: OCR misreads a roman such as '(i)' as '@', '®', '(1)': hide such
            # short label-like tokens just right of the key label
            lx1 = max(w[2] for w in k.label_ws)
            ly0, ly1 = min(w[1] for w in k.label_ws), max(w[3] for w in k.label_ws)
            for w in allpages[k.pno].words:
                if (lx1 < w[0] < lx1 + 30 and abs((w[1] + w[3]) / 2 - (ly0 + ly1) / 2) < 8
                        and len(w[4]) <= 5 and re.fullmatch(r"[\(\[{]?[ivxlI1|@®©)]{1,4}[\)\]}]?\.?", w[4])):
                    masks.append([k.pno, w[0] - 1.0, w[1] - 0.5, w[2] + 1.0, w[3] + 1.0])
                    label_ids.add((k.pno, id_of(w)))
    for pno, ws_ in CONT_LABELS:
        for w in ws_:
            # override keep_words [[page, x0, y0]]: a word in the label column that
            # is marking text, not a repeated key ('... volume in (d)', 9701/05/M/J/06)
            if any(k[0] == pno + 1 and abs(k[1] - w[0]) < 2 and abs(k[2] - w[1]) < 2
                   for k in ov.get("keep_words", [])):
                continue
            masks.append([pno, w[0] - 0.5, w[1] - 0.5, w[2] + 0.5, w[3] + 0.5])
            label_ids.add((pno, id_of(w)))
    for m in masks:
        doc[m[0]].draw_rect(fitz.Rect(m[1:5]), color=None, fill=(1, 1, 1), width=0, overlay=True)
    by_no = {pi.no: pi for pi in pages}
    raw = build_segments(pages, keys)
    # "[Total: n]" closes a question: the line itself is whited out, and what
    # follows it before the next question (e.g. "Uncertainties in Question 2"
    # notes spanning several parts) is not part of the last key's answer:
    # it is dropped from the crop and recorded for review.
    appendix = {}
    paths = list(raw)
    # question totals printed in the QP ('[Total: 18]'): a bare '18' / '[18]' row at
    # the end of the question's last MS part equal to it is the total row of the
    # answer table (9701/21/M/J/14), not a mark
    qtot = {}
    try:
        qdoc = fitz.open(prov["source_pdf"])
        tots = [int(m) for pg in qdoc for m in re.findall(r"\[\s*Total\s*:?\s*(\d+)\s*\]", pg.get_text())]
        qnums = list(dict.fromkeys(t[0] for t in leaves))
        if len(tots) == len(qnums):
            qtot = dict(zip(qnums, tots))
    except Exception:
        qtot = {}
    for i, path in enumerate(paths):
        tot_rows = []
        last_of_q = i + 1 == len(paths) or paths[i + 1][0] != path[0]
        # the last slice holding words (an empty slice can follow on the next page)
        inked = [ss for ss in raw[path] if any(w[1] >= ss[1] - 1 and w[3] <= ss[2] + 1 for w in by_no[ss[0]].words)]
        last_slice = tuple(inked[-1][:2]) if inked else None
        for pno, y0, y1 in raw[path]:
            rws = rows_of([w for w in by_no[pno].words if w[1] >= y0 - 1 and w[3] <= y1 + 1])
            for j, r in enumerate(rws):
                txt = " ".join(w[4] for w in r)
                m = re.fullmatch(r"\[?(\d{1,3})\]?", txt)
                if TOTAL_RE.match(txt) or (last_of_q and m and qtot.get(path[0]) == int(m.group(1))
                                           and j == len(rws) - 1 and (pno, y0) == last_slice):
                    tot_rows.append((pno, r))
                else:
                    # a total closing a marking line: '(if SO3 then e.c.f.) Total = [9]'
                    # (9701/02/M/J/04): only those words are whited out
                    for k in (2, 3, 4, 5):
                        tail = r[-k:]
                        if len(r) > k and tail[0][4].lower().startswith("total") and \
                                TOTAL_RE.match(" ".join(w[4] for w in tail)):
                            tot_rows.append((pno, tail))
                            break
        for pno, r in tot_rows:      # bracket glyphs reach ~2 pt below their word box
            # (scans: OCR boxes sit a little off the printed line, so pad above too)
            masks.append([pno, min(w[0] for w in r) - 1, min(w[1] for w in r) + (-2.5 if pno in OCR_PAGES else 0.5),
                          max(w[2] for w in r) + 1, max(w[3] for w in r) + 2.2])
            doc[pno].draw_rect(fitz.Rect(masks[-1][1:5]), color=None, fill=(1, 1, 1), width=0, overlay=True)
        if not tot_rows or not last_of_q:
            continue
        tp, tr = tot_rows[-1]
        ty0, ty1 = min(w[1] for w in tr), max(w[3] for w in tr)
        kept, after = [], []
        for pno, y0, y1 in raw[path]:
            ss = [pno, y0, y1]
            if (pno, y0) < (tp, ty0) <= (pno, y1):
                # the [Total] line itself is whited out, so the kept part may run
                # through it (tight old layouts: the line above touches it)
                kept.append([pno, y0, min(y1, ty1 + 2.2)])
                after.append([pno, ty1 + 2.2, y1])
            elif (pno, y1) <= (tp, ty0):
                kept.append(ss)
            else:
                after.append(ss)
        txt = [w[4] for pno, y0, y1 in after for w in by_no[pno].words if w[1] >= y0 - 1 and w[3] <= y1 + 1]
        if txt:
            appendix[tuple_label(path)] = {"slices": after, "text": " ".join(txt)[:600]}
        raw[path] = [k for k in kept if k[2] - k[1] >= 2]
    segs: dict[tuple, list] = {}
    for path, ss in raw.items():
        full = []
        for pno, y0, y1 in ss:
            xr = x_range(by_no[pno], y0, y1, label_ids)
            if xr is None:
                continue
            full.append([pno, round(xr[0], 2), round(y0, 2), round(xr[1], 2), round(y1, 2)])
        segs[path] = full

    # recorded overrides (ALEVEL/manual_specs/ms/<PREFIX>.json), each with a reason:
    #   drop_keys  auto keys to discard (a label covers its descendants)
    #   segments   {label: [[page, y0, y1], ...]} keys cut by hand
    #   absent     {label: reason} QP leaves the published MS does not mark
    for m in ov.get("masks", []):          # hand masks [page, x0, y0, x1, y1] (printed labels OCR merged)
        masks.append([m[0] - 1] + list(m[1:5]))
        doc[m[0] - 1].draw_rect(fitz.Rect(m[1:5]), color=None, fill=(1, 1, 1), width=0, overlay=True)
    for d in ov.get("drop_keys", []):
        dt = label_tuple(d)
        for p in [p for p in segs if p[:len(dt)] == dt]:
            del segs[p]
    for lab, ss in ov.get("segments", {}).items():
        full = []
        for pg, y0, y1, *xs in ss:
            by_no.setdefault(pg - 1, allpages[pg - 1])
            y0, y1 = max(y0, by_no[pg - 1].top), min(y1, by_no[pg - 1].bottom)   # never header/footer
            # [page, y0, y1, x0, x1]: a column slice, for content that shares a printed row
            # with the next part (9700/51/O/N/07 1(a)(i) graph axis label beside '(ii) 3 of')
            xr = tuple(xs) if len(xs) == 2 else x_range(by_no[pg - 1], y0, y1, label_ids)
            if xr is None:
                continue
            full.append([pg - 1, round(xr[0], 2), y0, round(xr[1], 2), y1])
        segs[label_tuple(lab)] = full
        # hand-cut slices: hide the question number and [Total] lines in them too
        qn = label_tuple(lab)[0]
        for pg, x0, y0, x1, y1 in full:
            pi = by_no[pg]
            for r in rows_of([w for w in pi.words if y0 <= (w[1] + w[3]) / 2 <= y1]):
                lead = [w for w in r[:2] if w[0] < 100 and (w[4] == qn or w[4] == "Question")]
                if lead and r[0] in lead and (r[0][4] == qn or (len(r) > 1 and r[1][4] == qn)):
                    hide = [w for w in r[:2] if w[4] in (qn, "Question")
                            and not any(k[0] == pg + 1 and abs(k[1] - w[0]) < 2 and abs(k[2] - w[1]) < 2
                                        for k in ov.get("keep_words", []))]   # a table cell '2' (9701/05/M/J/08 appendix)
                    if not hide:
                        continue
                elif TOTAL_RE.match(" ".join(w[4] for w in r)) or re.match(
                        r"^(Marking\s+scheme\s+for\s+)?[Qq]uestion\s+\d+\.?$", " ".join(w[4] for w in r)):
                    hide = r
                else:
                    # a trailing total ('1 Total: 12' with an OCR speck in front, 9701/04/O/N/02)
                    hide = next((r[-k:] for k in (2, 3, 4, 5) if len(r) > k and r[-k][4].lower().startswith("total")
                                 and TOTAL_RE.match(" ".join(w[4] for w in r[-k:]))), None)
                    if not hide:
                        continue
                m = [pg, min(w[0] for w in hide) - 0.5, min(w[1] for w in hide) + 0.5,
                     max(w[2] for w in hide) + 0.5, max(w[3] for w in hide) + 2.2]
                masks.append(m)
                doc[pg].draw_rect(fitz.Rect(m[1:5]), color=None, fill=(1, 1, 1), width=0, overlay=True)
                label_ids.update((pg, id_of(w)) for w in hide)
    segs = dict(sorted(segs.items(), key=lambda kv: (kv[1][0][0], kv[1][0][2]) if kv[1] else (0, 0)))
    absent = {label_tuple(k) for k in ov.get("absent", {})}

    # a revisited parent key ("(e) [U5]" in an uncertainty appendix) whose parts
    # are keyed: its rows are appended to each of those parts
    for i, k in enumerate(keys):
        later = any(len(kk.path) > len(k.path) and kk.path[:len(k.path)] == k.path for kk in keys[:i])
        if (getattr(k, "revisit", False) or later) and k.path in segs:
            kids = [p for p in segs if len(p) > len(k.path) and p[:len(k.path)] == k.path]
            if kids and tuple(k.path) not in set(leaves):
                extra = segs.pop(k.path)
                for p in kids:
                    segs[p] = segs[p] + extra
    # mapping
    kset = set(segs)
    mapping, used = {}, set()
    primary = {k.path for k in keys if not getattr(k, "revisit", False)}
    revisit_only = {k.path for k in keys if getattr(k, "revisit", False)} - primary
    for L in leaves:
        if L in revisit_only:
            anc = [L[:k] for k in range(len(L) - 1, 0, -1) if L[:k] in kset]
            if anc:
                mapping[L] = ("parent_ms_covers_child_qp", [anc[0], L])
                continue
        if L in absent and L not in kset:
            mapping[L] = ("ms_absent", [])
            continue
        if L in kset:
            mapping[L] = ("exact", [L])
            continue
        anc = [L[:k] for k in range(len(L) - 1, 0, -1) if L[:k] in kset]
        desc = [p for p in segs if len(p) > len(L) and p[:len(L)] == L]
        if desc:
            mapping[L] = ("children_ms_merged_for_parent_qp", desc)
        elif anc:
            mapping[L] = ("parent_ms_covers_child_qp", [anc[0]])
        else:
            mapping[L] = ("unresolved", [])
    for st, ps in mapping.values():
        used.update(ps)
    # a parent key whose children are keyed too and which no leaf uses: its own
    # rows are a heading (e.g. "2 Analysis, conclusions and evaluation (15 marks)"
    # plus a column-header row).  Dropped when they carry no mark; kept as an
    # orphan (blocking) when they do.
    preamble = {}
    for p in [p for p in segs if p not in used and any(q[:len(p)] == p and q != p for q in segs)]:
        txt = []
        for s_ in segs[p]:
            pi = by_no[s_[0]]
            txt += [w[4] for w in pi.words if w[1] >= s_[2] - 1 and w[3] <= s_[4] + 1
                    and s_[1] - 1 <= w[0] and (pi.no, id_of(w)) not in label_ids]
        if not any(MARK_RE.match(t) for t in txt):
            preamble[tuple_label(p)] = " ".join(txt)
            used.add(p)
    orphans = [p for p in segs if p not in used]
    # a parent key printed on the same line as its first child ("11 (b) (i)") has no
    # rows of its own: not an error
    empty = [p for p, s in segs.items() if not s
             and not any(len(q) > len(p) and q[:len(p)] == p and segs[q] for q in segs)]
    for p in [p for p, s in segs.items() if not s and p not in empty]:
        del segs[p]

    written = {}
    for L, (st, ps) in mapping.items():
        if st in ("unresolved", "ms_absent"):
            continue
        sl = [s for p in ps for s in segs.get(p, [])]   # an emptied parent key has no rows
        PIXEL_MASKS[:] = masks
        im = render_slices(doc, sl)
        if im is None:
            mapping[L] = ("unresolved", ps)
            continue
        name = f"{prefix}-{tuple_label(L)}.png"
        im.save(out / name, optimize=True)
        written[tuple_label(L)] = name
    prov_out = {
        "source_pdf": src, "prefix": prefix, "qp_provenance": str(Path(qprov).resolve()),
        "component": comp, "masks": masks,
        "keys": [{"key": tuple_label(k.path), "page": k.pno + 1, "y": round(k.top, 1),
                  "label": " ".join(w[4] for w in k.label_ws)} for k in keys],
        "segments": {tuple_label(p): [{"pdf_page": s[0] + 1, "clip_points": s[1:]} for s in ss]
                     for p, ss in segs.items()},
        "mapping": {tuple_label(L): {"status": st, "ms_keys": [tuple_label(p) for p in ps],
                                     "file": written.get(tuple_label(L))}
                    for L, (st, ps) in mapping.items()},
        "orphans": [tuple_label(p) for p in orphans],
        "overrides": ov,
        "dropped_preamble": preamble,
        "dropped_appendix": appendix,
        "misprinted_keys": {tuple_label(k.path): tuple_label(k.printed) for k in keys if k.printed},
    }
    (out / f"{prefix}-ms-provenance.json").write_text(json.dumps(prov_out, indent=1) + "\n")
    counts: dict[str, int] = {}
    for st, _ in mapping.values():
        counts[st] = counts.get(st, 0) + 1
    unres = [tuple_label(L) for L, (st, _) in mapping.items() if st == "unresolved"]
    print(f"keys={len(keys)} leaves={len(leaves)} " + " ".join(f"{k}={v}" for k, v in sorted(counts.items()))
          + f" unresolved={unres} orphans={[tuple_label(p) for p in orphans]} empty={[tuple_label(p) for p in empty]}"
          + f" misprinted={[tuple_label(k.printed) for k in keys if k.printed]} appendix={list(appendix)}")
    if not unres and not orphans and not empty:
        print("MS_OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
