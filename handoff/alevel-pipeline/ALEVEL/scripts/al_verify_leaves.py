#!/usr/bin/env python3
"""Independent leaf-set verifier for Cambridge A Level question-paper splits.

Written separately from the splitter (al_qp_splitter.py) so that it is a real
second opinion.  It derives the expected answerable leaves from the printed
markers only:

  question number  bare integer in the question column   (x ~ 50 pt)
  part             "(a)".."(h)"  in the part column        (x ~ 72 pt)
  roman            "(i)".."(x)"  in the roman column       (x ~ 90-100 pt)

Every token on a row is examined, so inline "1 (a) (i)" is understood.  A
token counts only if it sits in its column AND continues the expected
sequence (Q n -> n+1, (a) -> (b), (i) -> (ii)); numbers inside figures and
tables, cover-page boxes and axis labels fail one of those tests.  Leaves are
the deepest labels; the produced leaf set (crop files that are not .stem) must
match exactly.

Usage: al_verify_leaves.py SOURCE.pdf CROPS_DIR PREFIX   -> exit 0 on exact match
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pymupdf as fitz
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import fused_marks  # noqa: E402
fused_marks.install(leaders=len(sys.argv) > 3 and sys.argv[3].startswith(("AL-MTH-", "AL-FMT-")))

ROMANS = ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x"]
LETTERS = "abcdefghijk"  # (i) after (h) in the PART column is the letter (9701/52/M/J/24 Q1(i)); elsewhere roman
Q_COL = (40, 60)
PART_COL = (62, 82)   # 9702/21/M/J/20 Q5(b) sits at x=63.8
ROMAN_COL = (82, 104)   # wide "(viii)" right-aligned starts at x=83.7 (9701/42/F/M/24), "(vii)" at 82.47 (9701/51/M/J/15)
NUM_COL = (108, 135)   # older papers: "1." "2." tasks under a roman
TOP, BOTTOM = 40, 800


def expected_leaves(pdf: str, maths: bool = False) -> list[str]:
    doc = fitz.open(pdf)
    q = 0
    part = ""
    roman = ""
    num = 0
    labels: list[tuple[str, str, str, str]] = []
    where: dict[tuple[str, str, str, str], tuple[int, float]] = {}
    marks: dict[int, list[float]] = {}
    for pno in range(1, doc.page_count):  # page 1 is the cover
        page = doc[pno]
        # the teacher REPORT FORM (old 9700 Paper 5 last page) has its own
        # (a)-(d) questions for the teacher: not parts of the paper
        if re.search(r"REPORT FORM\s+The teacher responsible for this subject", page.get_text()):
            break
        words = sorted((w for w in page.get_text("words") if TOP <= w[1] <= BOTTOM), key=lambda w: (round(w[1]), w[0]))
        marks[pno] = [w[1] for w in words if re.fullmatch(r"\[\d+\]", w[4])]
        for w in words:
            x, t = w[0], w[4]
            # a key row in a figure ('3 = co-amoxiclav', 9700/51/O/N/18 Fig. 2.1)
            # is not a question number
            nxt_w = min((v for v in words if abs(v[1] - w[1]) < 3 and v[0] > w[2]), key=lambda v: v[0], default=None)
            # old 9700 Paper 5 heads a question 'Question 2 [40 minutes]'
            # instead of a bare number (9700/05/O/N/02)
            heading = (t == "Question" and Q_COL[0] <= x <= Q_COL[1] and nxt_w is not None
                       and nxt_w[4].isdigit() and int(nxt_w[4]) == q + 1)
            if heading or (Q_COL[0] <= x <= Q_COL[1] and t.isdigit() and int(t) == q + 1
                           and not (nxt_w and nxt_w[4] in ("=", "\u2013="))):
                q, part, roman, num = q + 1, "", "", 0
                labels.append((str(q), "", "", ""))
                continue
            nm = re.fullmatch(r"(\d)\.", t)
            # '1. ......' with only dots after it is a numbered ANSWER SLOT
            # ('Suggest two reasons. 1. .... 2. ....'), not a separate task
            rest = [v[4] for v in words if abs(v[1] - w[1]) < 3 and v[0] > w[2]]
            # an answer slot is '1. ..........' (a real leader: >=10 dots,
            # '…' = 3).  A lone '.' or ',' after a stacked fraction ends the
            # task's sentence (9702/21/O/N/18 Q6(b)(iii) 2.)
            slot = (bool(rest) and all(re.fullmatch(r"[.\u2026]+", r) for r in rest)
                    and sum(len(r) + 2 * r.count("\u2026") for r in rest) >= 10)
            if nm and not slot and q and roman and NUM_COL[0] <= x <= NUM_COL[1] and isinstance(num, int) and int(nm.group(1)) == num + 1:
                num += 1
                labels.append((str(q), part, roman, str(num)))
                where[labels[-1]] = (pno, w[1])
                continue
            m = re.fullmatch(r"\(([a-z]{1,4})\)", t)
            if not m or q == 0:
                continue
            tok = m.group(1)
            # Maths: '(a) ... [4]  (b) ... [1]' under a roman are fourth-level
            # tasks (9709/04/O/N/07 Q6(ii)); kept only if separately marked (below)
            if maths and roman and len(tok) == 1 and NUM_COL[0] - 15 <= x <= NUM_COL[1] \
                    and tok == (LETTERS[LETTERS.index(num) + 1] if isinstance(num, str) and num else "a"):
                num = tok
                labels.append((str(q), part, roman, tok))
                where[labels[-1]] = (pno, w[1])
                continue
            # several roman labels on one row are inline labels of a figure
            # ('(i) glycine  (ii) aspartic acid  (iii) lysine', 9701/06/M/J/04)
            if tok in ROMANS[:-1] and any(v is not w and abs(v[1] - w[1]) < 4 and v[0] - x > 40
                                          and v[4] == f"({ROMANS[ROMANS.index(tok) + 1]})" for v in words):
                continue
            nxt_part = LETTERS[LETTERS.index(part) + 1] if part else "a"
            nxt_roman = ROMANS[ROMANS.index(roman) + 1] if roman else "i"
            # a roman followed only by a dotted leader (and a mark) is an
            # answer slot under a shared prompt ('State two ... (i) .....
            # (ii) ..... [2]', 9701/02/M/J/03), like '1. .....' -- not a part
            rest_nm = [r for r in rest if not re.fullmatch(r"\[\d+\]", r)]
            if tok in ROMANS and rest_nm and all(re.fullmatch(r"[.\u2026]+", r) for r in rest_nm) \
                    and sum(len(r) + 2 * r.count("\u2026") for r in rest_nm) >= 10:
                continue
            # 2002-04 papers sometimes print a part label in the question
            # column (9701/04/M/J/02 Q5(c) at x=49.6)
            if ((PART_COL[0] <= x <= PART_COL[1] or (Q_COL[0] <= x <= Q_COL[1] and part)) and tok == nxt_part) or (
                    # an indented letter in the roman column (9701/04/O/N/02 Q1(b) at x=95)
                    ROMAN_COL[0] <= x <= ROMAN_COL[1] and part and tok == nxt_part and tok not in ROMANS):
                part, roman, num = tok, "", 0
                labels.append((str(q), part, "", ""))
            elif (ROMAN_COL[0] <= x <= ROMAN_COL[1] or PART_COL[0] <= x <= PART_COL[1]) and tok == nxt_roman:
                # romans in the PART column: under a part (2008 papers,
                # 9702/02/O/N/08 Q3(b)(i) at x=72) or directly under a
                # question that has no lettered parts (9701/43/O/N/10 Q4)
                roman, num = tok, 0
                labels.append((str(q), part, roman, ""))
    # romans directly under a question number in a question that also has
    # lettered parts are a list in its stem ('... each of the following in
    # sequence: (i) the copper metal, (ii) ... (iii) ...', 9701/52/O/N/14)
    lettered = {l[0] for l in labels if l[1]}
    labels = [l for l in labels if not (l[0] in lettered and not l[1] and l[2])]
    # a numbered run needs >= 2 items (same rule as the splitter); drop
    # lone "1." items, which are prose lists, not a fourth level
    by_parent = {}
    for lab in labels:
        if lab[3]:
            by_parent.setdefault(lab[:3], []).append(lab)
    # numbered tasks are leaves only when separately marked: a [n] must lie
    # between each task and the next (one shared mark -> the roman is one leaf)
    def marked_between(a, b):
        (pa, ya), (pb, yb) = where[a], where[b]
        for pg in range(pa, pb + 1):
            lo = ya - 3 if pg == pa else 0   # the task's own row may hold its mark
            hi = yb if pg == pb else 1e9
            if any(lo < m < hi for m in marks.get(pg, [])):
                return True
        return False
    for parent, kids in list(by_parent.items()):
        if any(not marked_between(kids[i], kids[i + 1]) for i in range(len(kids) - 1)):
            by_parent[parent] = []
    labels = [lab for lab in labels if not lab[3] or len(by_parent[lab[:3]]) >= 2]
    # leaves = labels with no deeper label beneath them
    paths = [".".join(filter(None, lab)) for lab in labels]
    leaves = []
    for p in paths:
        if not any(o != p and o.startswith(p + ".") for o in paths):
            leaves.append("Q" + p)
    return leaves


def produced_leaves(crops: str, prefix: str) -> list[str]:
    out = []
    for f in Path(crops).glob(f"{prefix}-Q*.png"):
        label = f.stem[len(prefix) + 1:]
        if not label.endswith(".stem"):
            out.append(label)
    return out


def main() -> int:
    pdf, crops, prefix = sys.argv[1:4]
    exp = set(expected_leaves(pdf, maths=prefix.startswith(("AL-MTH-", "AL-FMT-"))))
    got = set(produced_leaves(crops, prefix))
    # a manual spec may declare detected 'leaves' that are not answerable
    # (e.g. an '(i) (ii) (iii)' list inside a stem), with a recorded reason
    import json
    pv = Path(crops) / f"{prefix}-split-provenance.json"
    absent = json.load(open(pv)).get("accepted_absent_leaves", {}) if pv.exists() else {}
    for lab, why in absent.items():
        if lab in exp:
            print(f"ACCEPTED-ABSENT-LEAF {lab}: {why}")
            exp.discard(lab)
    missing, extra = sorted(exp - got), sorted(got - exp)
    print(f"expected={len(exp)} produced={len(got)} missing={missing} extra={extra}")
    return 0 if exp and not missing and not extra else 1


if __name__ == "__main__":
    sys.exit(main())
