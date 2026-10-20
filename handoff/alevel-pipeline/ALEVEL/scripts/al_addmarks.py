#!/usr/bin/env python3
"""Add the marks a manual spec lost to its crops (D6: marks stay visible).

A mark printed at the end of a plain dotted answer row ('.......... [2]') was
dropped by the automatic drafts together with the row.  For every '[n]' the
coverage gate reports MISSING, this tool appends a segment for the mark's
line to the leaf whose crop ends just above it (same page; else the last leaf
on an earlier page) and whites out the row's dots and slot number with a spec
mask, so only the mark shows.  Run al_manual.py run afterwards.

Usage: al_addmarks.py PREFIX
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pymupdf as fitz

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fused_marks  # noqa: E402
fused_marks.install()

DATA = Path.home() / "rootatom_data" / "ALEVEL"
HERE = Path(__file__).resolve().parent
PY = str(Path.home() / ".venvs" / "alevel" / "bin" / "python")
MARK_RE = re.compile(r"^\[\d+\]$")
DOTS_RE = re.compile(r"^[.…]{3,}$")
PLAIN_RE = re.compile(r"^(\d{1,2}\.?|\(\w{1,4}\)|[IVX]{1,4}|[.…,;:]+)$")


def main() -> int:
    prefix = sys.argv[1]
    spec_path = DATA / "manual" / f"{prefix}.json"
    spec = json.load(open(spec_path))
    out = DATA / "splits" / "manual" / prefix
    src = json.load(open(out / f"{prefix}-split-provenance.json"))["source_pdf"]
    g = subprocess.run([PY, "-I", str(HERE / "al_verify_coverage.py"), src, str(out), prefix, "--verbose"],
                       capture_output=True, text=True).stdout
    miss = [(int(m.group(1)), int(m.group(2))) for m in
            re.finditer(r"MISSING \((\d+), (\d+), '\[\d+\]'\)", g)]
    if not miss:
        print(f"{prefix}: no missing marks")
        return 0
    doc = fitz.open(src)
    added = []
    for pg, y in miss:
        ws = doc[pg - 1].get_text("words")
        mk = [w for w in ws if MARK_RE.match(w[4]) and abs(round(w[1]) - y) <= 1]
        if not mk:
            continue
        m = mk[0]
        # the mark's line: dots/slot words that share it; a mark set on the
        # line below the dots takes its own line only
        line = [w for w in ws if w is not m and w[1] < m[3] - 3 and m[1] < w[3] - 3 and w[2] <= m[0] + 1
                and w[0] >= 38 and not re.fullmatch(r"DO|NOT|WRITE|IN|THIS|MARGIN", w[4])]
        if any(not (DOTS_RE.match(w[4]) or PLAIN_RE.match(w[4])) for w in line):
            print(f"{prefix}: p{pg} y{y} mark shares its line with text -- left for hand work")
            continue
        y0 = min([m[1]] + [w[1] for w in line]) - 1.5
        y1 = max([m[3]] + [w[3] for w in line]) + 1.5
        # owner: the non-stem leaf whose segment ends nearest above the mark
        best = None
        for lab, segs in spec["crops"].items():
            if lab.endswith(".stem"):
                continue
            for s in segs:
                key = (s[0], s[2])
                if (s[0] < pg or (s[0] == pg and s[2] <= m[1] + 2)) and (best is None or key > best[0]):
                    best = (key, lab)
        if best is None:
            print(f"{prefix}: p{pg} y{y} no leaf above the mark -- left for hand work")
            continue
        lab = best[1]
        # the leaf's own crop width (560 would cross the examiner-column rule
        # of older papers), widened only as far as the mark needs
        x0 = min(s[3] for s in spec["crops"][lab])
        x1 = max(min(s[4] for s in spec["crops"][lab]), m[2] + 3)
        spec["crops"][lab].append([pg, round(y0, 2), round(y1, 2), x0, round(x1, 2)])
        spec["crops"][lab].sort(key=lambda s: (s[0], s[1]))
        for w in line:
            spec.setdefault("masks", []).append([pg, round(w[0] - 0.5, 2), round(w[1] - 0.5, 2),
                                                 round(min(w[2] + 0.5, m[0] - 0.3), 2), round(w[3] + 0.5, 2)])
        added.append(f"p{pg} y{y} -> {lab}")
    spec.setdefault("autofix", []).append(f"al_addmarks: {len(added)} marks added")
    json.dump(spec, open(spec_path, "w"), indent=1)
    print(f"{prefix}: added {len(added)}/{len(miss)}: " + "; ".join(added))
    return 0


if __name__ == "__main__":
    sys.exit(main())
