#!/usr/bin/env python3
"""Draft-and-repair route for papers the automatic splitter holds.

  1. split the paper in DRAFT mode (AL_DRAFT=1: REVIEW_REQUIRED cases are
     logged, not fatal) into splits/draft/<PREFIX>;
  2. turn the draft into a manual spec (manual/<PREFIX>.json, the format of
     al_manual.py) and render it with the manual renderer;
  3. repair what the coverage gate reports, then re-render, up to N rounds:
       MISSING words   -> clustered per page; each cluster joins the crop
                          directly above it (or below, or -- on a page with no
                          crop -- the last item before that page), only when
                          no other crop lies in between;
       sliced edge     -> the edge moves to the nearest fully blank pixel row;
       plain dotted row inside a crop -> its dots / mark are masked white;
       blank band      -> recorded in accept_blank (reason: auto, working
                          space) for the visual reviewer to confirm;
     nothing else is touched (leaf-label mismatches stay HOLD).
  4. print the gate verdict lines.  The result is reviewed like every other
     crop set; nothing is accepted on the gates alone.

Every automatic change is listed in the spec under "autofix" with its reason.

Usage: al_autofix.py PREFIX SOURCE.pdf [--rounds 6]
"""

from __future__ import annotations

import ast
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
import pymupdf as fitz

HERE = Path(__file__).resolve().parent
DATA = Path.home() / "rootatom_data" / "ALEVEL"
CANON = DATA / "source_papers" / "canonical"
MANUAL = DATA / "manual"
PY = sys.executable
DOTS = re.compile(r"^[.…]{3,}")
MARK = re.compile(r"^\[\d+\]$")


def run(cmd, env=None):
    r = subprocess.run(cmd, capture_output=True, text=True, env=env)
    return r.returncode, r.stdout + r.stderr


def gate(src: Path, out: Path, prefix: str):
    _, l1 = run([PY, "-I", str(HERE / "al_verify_leaves.py"), str(src), str(out), prefix])
    _, l2 = run([PY, "-I", str(HERE / "al_verify_coverage.py"), str(src), str(out), prefix, "--verbose"])
    return l1, l2


def parse(l2: str):
    missing, sliced, plain, blank = [], [], [], []
    for line in l2.splitlines():
        s = line.strip()
        try:
            if s.startswith("MISSING"):
                missing.append(ast.literal_eval(s[len("MISSING"):].strip()))
            elif s.startswith("SLICED-BOUNDARY"):
                sliced.append(ast.literal_eval(s[len("SLICED-BOUNDARY"):].strip()))
            elif s.startswith("PLAIN-DOTTED-LINE-IN-CROP"):
                plain.append(ast.literal_eval(s[len("PLAIN-DOTTED-LINE-IN-CROP"):].strip()))
            elif s.startswith("BLANK-BAND"):
                blank.append(ast.literal_eval(s[len("BLANK-BAND"):].strip()))
        except Exception:
            pass
    return missing, sliced, plain, blank


class Ink:
    """the page as the coverage gate sees it: 200 dpi, with the 2010s examiner
    mark boxes and the spec's masks whited out"""
    K = 200 / 72

    def __init__(self, page, masks=()):
        pw = page.get_text("words")
        margin = [d["rect"] for d in page.get_drawings() if d.get("rect") is not None
                  and d["rect"].x0 >= 528 and d["rect"].x1 <= 572 and 60 < d["rect"].y0 and d["rect"].y1 < 790
                  and d["rect"].height <= 40 and d["rect"].width <= 35
                  and not [w for w in pw if fitz.Rect(w[:4]).intersects(d["rect"] + (-2, -2, 2, 2))]]
        pm = page.get_pixmap(dpi=200, colorspace=fitz.csGRAY, alpha=False)
        self.g = np.frombuffer(pm.samples, np.uint8).reshape(pm.height, pm.width).copy()
        k = self.K
        for r in (margin if len(margin) >= 4 else []) + [fitz.Rect(m) for m in masks]:
            self.g[max(0, int((r.y0 - 1) * k)):int((r.y1 + 1) * k) + 1, max(0, int((r.x0 - 1) * k)):int((r.x1 + 1) * k) + 1] = 255

    def blank_col_near(self, x: float, y0: float, y1: float, reach=30.0, prefer=1) -> float | None:
        k = self.K
        cols = (self.g[int(y0 * k):int(y1 * k), :] < 235).any(axis=0)
        c0 = int(round(x * k))
        for d in range(0, int(reach * k) + 1):       # outward only
            c = c0 + (d if prefer > 0 else -d)
            if 0 <= c < len(cols) and not cols[c]:
                return c / k
        return None

    def blank_near(self, y: float, x0: float, x1: float, reach=14.0, prefer=0) -> float | None:
        """nearest fully blank pixel row (inside x0..x1) to y, within reach;
        prefer=-1 searches upward first, +1 downward first"""
        k = self.K
        rows = (self.g[:, int(x0 * k):int(x1 * k)] < 235).any(axis=1)
        r0 = int(y * k)
        order = []
        for d in range(0, int(reach * k) + 1):
            for sgn in ((-1, 1) if prefer <= 0 else (1, -1)):
                order.append(r0 + sgn * d)
        for r in order:
            if 0 <= r < len(rows) and not rows[r]:
                return r / k
        return None


def main() -> int:
    prefix, srcname = sys.argv[1], sys.argv[2]
    rounds = int(sys.argv[sys.argv.index("--rounds") + 1]) if "--rounds" in sys.argv else 6
    src = CANON / srcname
    draft = DATA / "splits" / "draft" / prefix
    draft.mkdir(parents=True, exist_ok=True)
    for f in draft.iterdir():
        f.unlink()
    env = dict(os.environ, AL_DRAFT="1")
    rc, log = run([PY, "-I", str(HERE / "al_qp_splitter.py"), str(src), str(draft), prefix], env=env)
    prov = draft / f"{prefix}-split-provenance.json"
    if not prov.exists():
        print(f"{prefix}: draft split failed: {log.strip().splitlines()[-1][:160] if log.strip() else rc}")
        return 2
    pv = json.load(open(prov))
    crops = {lab: [[s["pdf_page"], s["clip_points"][1], s["clip_points"][3],
                    s["clip_points"][0], s["clip_points"][2]] for s in segs]
             for lab, segs in pv["outputs"].items()}
    # the draft's own dot masks (D6 step 2d: a plain dotted row kept for its
    # mark, dots whited out) carry over; marks themselves are never masked
    spec = {"source": srcname, "prefix": prefix, "crops": crops,
            "masks": [list(m) for m in pv.get("manual_masks", [])],
            "accept_blank": {}, "accept_plain": {}, "autofix": []}
    MANUAL.mkdir(parents=True, exist_ok=True)
    spec_path = MANUAL / f"{prefix}.json"
    doc = fitz.open(src)
    inks: dict[int, Ink] = {}
    out = DATA / "splits" / "manual" / prefix

    def ink(p):
        key = (p, len(spec["masks"]))
        if key not in inks:
            inks[key] = Ink(doc[p - 1], [m[1:5] for m in spec["masks"] if m[0] == p])
        return inks[key]

    def order_key(lab):
        return min((s[0], s[1]) for s in crops[lab])

    def normalise():
        """overlapping segments: same label -> merged; different labels ->
        cut at a blank row inside the overlap (upper ends, lower starts)"""
        for pno in sorted({s[0] for ss in crops.values() for s in ss}):
            items = sorted([(lab, s) for lab, ss in crops.items() for s in ss if s[0] == pno],
                           key=lambda t: (t[1][1], t[1][2]))
            for (la, a), (lb, b) in zip(items, items[1:]):
                if a[2] <= b[1] + 0.5 or min(a[4], b[4]) - max(a[3], b[3]) < 1:
                    continue
                if la == lb:
                    a[2] = max(a[2], b[2]); b[1] = a[1]; b[2] = a[2]
                    spec["autofix"].append(f"p{pno} {la}: overlapping own segments merged")
                else:
                    mid = (b[1] + min(a[2], b[2])) / 2
                    cut = ink(pno).blank_near(mid, max(a[3], b[3]), min(a[4], b[4]),
                                              reach=max(4.0, (min(a[2], b[2]) - b[1]) / 2)) or mid
                    a[2] = cut; b[1] = cut
                    spec["autofix"].append(f"p{pno} {la}/{lb}: overlap cut at {cut:.1f}")
        for lab in crops:      # drop exact duplicates left by merging
            seen, keep = set(), []
            for s in crops[lab]:
                k_ = (s[0], round(s[1], 1), round(s[2], 1))
                if k_ not in seen and s[2] - s[1] > 2:
                    seen.add(k_); keep.append(s)
            crops[lab] = keep

    l1 = l2 = ""
    for rnd in range(rounds):
        normalise()
        spec_path.write_text(json.dumps(spec, indent=1) + "\n")
        rc, rlog = run([PY, "-I", str(HERE / "al_manual.py"), "render", str(spec_path), str(out)])
        if rc:
            print(f"{prefix}: render failed: {rlog.strip().splitlines()[-1][:160]}")
            return 2
        l1, l2 = gate(src, out, prefix)
        missing, sliced, plain, blank = parse(l2)
        changed = False
        # --- a missing word inside a segment's rows but outside its width
        # (a table wider than the 40-560 pt column): widen that segment
        rest = []
        for m in missing:
            pno, y = m[0], m[1]
            if not isinstance(pno, int):
                continue
            ws = [w for w in doc[pno - 1].get_text("words") if abs(w[1] - y) < 2 and w[4].startswith(str(m[2])[:4])]
            hit = False
            for w in ws:
                for lab, ss in crops.items():
                    for sg in ss:
                        if sg[0] == pno and sg[1] - 1 <= (w[1] + w[3]) / 2 <= sg[2] + 1 and not (sg[3] <= w[0] and w[2] <= sg[4]):
                            sg[3] = min(sg[3], round(w[0] - 3, 1)); sg[4] = max(sg[4], round(w[2] + 3, 1))
                            spec["autofix"].append(f"p{pno} {lab}: widened to x {sg[3]}-{sg[4]} for {m[2]!r}")
                            hit = True
                            changed = True
            if not hit:
                rest.append(m)
        missing = rest
        # --- missing words: cluster per page, attach to the adjacent crop
        bypage: dict[int, list] = {}
        for m in missing:
            pno, y = m[0], m[1]
            if isinstance(pno, int):
                bypage.setdefault(pno, []).append(y)
        for pno, ys in bypage.items():
            ys.sort()
            clusters, cur = [], [ys[0]]
            for y in ys[1:]:
                if y - cur[-1] < 30:
                    cur.append(y)
                else:
                    clusters.append(cur)
                    cur = [y]
            clusters.append(cur)
            words = doc[pno - 1].get_text("words")
            for c in clusters:
                ws = [w for w in words if min(c) - 3 <= w[1] <= max(c) + 3]
                if not ws:
                    continue
                c0, c1 = min(w[1] for w in ws), max(w[3] for w in ws)
                segs = [(lab, i, s) for lab, ss in crops.items() for i, s in enumerate(ss) if s[0] == pno]
                above = [t for t in segs if t[2][2] <= c0 + 1]
                below = [t for t in segs if t[2][1] >= c1 - 1]
                target = None
                if above:
                    lab, i, s = max(above, key=lambda t: t[2][2])
                    if not [t for t in segs if t[2][1] > s[2] - 1 and t[2][2] < c0 + 1 and t[0] != lab]:
                        target = (lab, i, "down")
                if target is None and below:
                    lab, i, s = min(below, key=lambda t: t[2][1])
                    if not [t for t in segs if t[2][1] > c1 - 1 and t[2][2] < s[1] + 1 and t[0] != lab]:
                        target = (lab, i, "up")
                if target is None and not segs and re.search(
                        r"Important values, constants and standards|The Periodic Table|oganesson",
                        doc[pno - 1].get_text()):
                    continue        # a data page is reference material, never an item's content
                if target is None and not segs:
                    prev = [lab for lab in crops if order_key(lab) < (pno, 0) and not lab.endswith(".stem")]
                    if prev:
                        lab = max(prev, key=lambda l_: max((s[0], s[2]) for s in crops[l_]))
                        y0 = ink(pno).blank_near(c0 - 2, 40, 560, prefer=-1) or c0 - 3
                        y1 = ink(pno).blank_near(c1 + 2, 40, 560, prefer=1) or c1 + 3
                        crops[lab].append([pno, y0, y1, 40.0, 560.0])
                        spec["autofix"].append(f"p{pno} y{c0:.0f}-{c1:.0f}: unowned region -> {lab} (last item before the page)")
                        changed = True
                    continue
                if target is None:
                    spec["autofix"].append(f"p{pno} y{c0:.0f}-{c1:.0f}: missing words NOT attached (crops on both sides)")
                    continue
                lab, i, way = target
                s = crops[lab][i]
                if way == "down":
                    ny = ink(pno).blank_near(c1 + 2, s[3], s[4], prefer=1) or c1 + 3
                    s[2] = max(s[2], ny)
                else:
                    ny = ink(pno).blank_near(c0 - 2, s[3], s[4], prefer=-1) or c0 - 3
                    s[1] = min(s[1], ny)
                spec["autofix"].append(f"p{pno} y{c0:.0f}-{c1:.0f}: missing words -> {lab} (extended {way})")
                changed = True
        # --- sliced LEFT/RIGHT edges -> nearest blank column outward
        for sl in sliced:
            if len(sl) == 4 and isinstance(sl[0], int) and isinstance(sl[2], str) and sl[2].startswith("x="):
                pno, lab, xe = sl[0], sl[1], float(sl[2][2:])
                for sg in crops.get(lab, []):
                    if sg[0] != pno:
                        continue
                    for j, pref in ((3, -1), (4, 1)):
                        if abs(sg[j] - xe) < 1.5:
                            nx = ink(pno).blank_col_near(xe, sg[1], sg[2], prefer=pref)
                            if nx is not None and abs(nx - xe) > 0.1:
                                sg[j] = round(nx, 2)
                                spec["autofix"].append(f"p{pno} {lab} x-edge {xe:.0f} -> blank column {nx:.1f}")
                                changed = True
        # --- sliced segment edges -> nearest blank row
        for sl in sliced:
            if len(sl) == 4 and isinstance(sl[0], int) and isinstance(sl[2], (int, float)):
                pno, lab, edge = sl[0], sl[1], float(sl[2])
                for s in crops.get(lab, []):
                    if s[0] != pno:
                        continue
                    for j in (1, 2):
                        if abs(s[j] - edge) < 1.5:
                            ny = ink(pno).blank_near(edge, s[3], s[4], prefer=-1 if j == 1 else 1)
                            if ny is not None and abs(ny - edge) > 0.1:
                                s[j] = ny
                                spec["autofix"].append(f"p{pno} {lab} edge {edge:.0f} -> blank row {ny:.1f}")
                                changed = True
        # --- plain dotted rows inside a crop -> mask their dots (the mark stays:
        # D6 keeps every [n], 7e57f2d)
        for pl in plain:
            pno, y = pl[0], pl[1]
            for w in doc[pno - 1].get_text("words"):
                if abs(w[1] - y) < 3 and DOTS.match(w[4]):
                    m = [pno, round(w[0] - 2, 1), round(w[1] - 1.5, 1), round(w[2] + 2, 1), round(w[3] + 1.5, 1)]
                    if m not in spec["masks"]:
                        spec["masks"].append(m)
                        changed = True
            spec["accept_plain"][f"{pno}:{y}"] = "auto: plain answer row inside a prompt region, masked"
            spec["autofix"].append(f"p{pno} y{y}: plain dotted row masked")
        # --- blank bands -> recorded for the reviewer
        for b in blank:
            if b[0] not in spec["accept_blank"]:
                spec["accept_blank"][b[0]] = "auto: blank working space inside the item (visual review confirms)"
                spec["autofix"].append(f"{b[0]}: blank band accepted for review")
                changed = True
        if not changed:
            break
    spec_path.write_text(json.dumps(spec, indent=1) + "\n")
    leaves = next((l for l in l1.splitlines() if l.startswith("expected=")), "NO LEAVES LINE")
    cov = next((l for l in l2.splitlines() if l.startswith("pages ")), "NO COVERAGE LINE")
    print(f"{prefix}: {leaves} | {cov}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
