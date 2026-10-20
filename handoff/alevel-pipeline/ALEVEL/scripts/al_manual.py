#!/usr/bin/env python3
"""Manual split specs for papers the automatic splitter holds.

A spec (ALEVEL/manual/<PREFIX>.json) lists each output crop as segments of a
source page, plus optional extra white masks:

    {"source": "9702_s02_qp_6.pdf", "prefix": "AL-PHY-02s-61-QP",
     "crops": {"Q1.a": [[4, 61.0, 140.5], [5, 60.0, 98.0, 40, 560]], ...},
     "masks": [[5, 528, 300, 560, 330], ...]}

Segment = [page (1-based), y0, y1] or [page, y0, y1, x0, x1] (points).
Rendering applies the SAME furniture masking as the splitter
(mask_alevel_furniture: barcodes, margin strips, [Total], mark boxes, corner
marks), hides every question number in the 40-62 pt gutter, applies the
spec's masks, and writes PNGs + the standard provenance JSON, so the normal
gates (al_verify_leaves.py, al_verify_coverage.py) and visual review apply
unchanged.  Nothing is accepted without passing those gates.

Commands:
  al_manual.py lines SRC PAGE                print text rows (y0 y1 x0 text) to author a spec
  al_manual.py init PREFIX RUN               draft spec from an existing split's provenance
  al_manual.py render SPEC OUTDIR            render crops + provenance
  al_manual.py run PREFIX                    render manual/<PREFIX>.json into splits/manual/<PREFIX>,
                                             then run both gates and print their verdict lines
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

DATA = Path.home() / "rootatom_data" / "ALEVEL"
HERE = Path(__file__).resolve().parent
CANON = DATA / "source_papers" / "canonical"
MANUAL = DATA / "manual"
DPI = 220
SEP_PT = 8


def load_splitter(src: str, prefix: str):
    """Import the splitter in A Level mode (its config reads sys.argv)."""
    saved = sys.argv
    sys.argv = ["al_qp_splitter.py", src, "/tmp/unused", prefix]
    sys.path.insert(0, str(HERE))
    import importlib
    mod = importlib.import_module("al_qp_splitter")
    sys.argv = saved
    return mod


def cmd_lines(src: str, page: int) -> None:
    import pymupdf as fitz
    sys.path.insert(0, str(HERE))
    import fused_marks
    fused_marks.install()
    pg = fitz.open(CANON / src if not Path(src).exists() else src)[page - 1]
    rows: dict[int, list] = {}
    for w in pg.get_text("words"):
        rows.setdefault(round(w[1] / 3), []).append(w)
    for k in sorted(rows):
        ws = sorted(rows[k], key=lambda w: w[0])
        y0, y1 = min(w[1] for w in ws), max(w[3] for w in ws)
        print(f"{y0:7.1f} {y1:7.1f} {ws[0][0]:6.1f}  {' '.join(w[4] for w in ws)[:110]}")
    big = [d["rect"] for d in pg.get_drawings() if d.get("rect") is not None
           and (d["rect"].width > 30 or d["rect"].height > 30)]
    if big:
        ys = sorted({(round(r.y0), round(r.y1)) for r in big})
        print("drawings y-ranges:", ys[:40])


def cmd_init(prefix: str, run: str) -> None:
    prov = json.load(open(DATA / "splits" / run / prefix / f"{prefix}-split-provenance.json"))
    crops = {lab: [[s["pdf_page"], s["clip_points"][1], s["clip_points"][3],
                    s["clip_points"][0], s["clip_points"][2]] for s in segs]
             for lab, segs in prov["outputs"].items()}
    # carry the splitter's dotted-answer-row masks over, or the spec re-exposes them
    masks = [[int(m[0]), *m[1:5]] for m in prov.get("manual_masks", [])]
    spec = {"source": Path(prov["source_pdf"]).name, "prefix": prefix, "crops": crops, "masks": masks}
    MANUAL.mkdir(parents=True, exist_ok=True)
    out = MANUAL / f"{prefix}.json"
    out.write_text(json.dumps(spec, indent=1) + "\n")
    print(out)


def render(spec_path: str, outdir: str) -> None:
    import numpy as np
    import pymupdf as fitz
    from PIL import Image
    spec = json.load(open(spec_path))
    src = str(CANON / spec["source"])
    prefix = spec["prefix"]
    sp = load_splitter(src, prefix)
    doc = fitz.open(src)
    # pages whose right-margin drawings are figure parts, not mark boxes
    sp.AL_NO_MARK_BOX_PAGES = {int(k) for k in spec.get("no_mark_box_pages", {})}
    sp.mask_alevel_furniture(doc)
    # hide question numbers: a 1-2 digit token at x 40-62 starting a row
    qnums = {int(re.match(r"Q(\d+)", lab).group(1)) for lab in spec["crops"]}
    # where each question starts: its first crop (page, y0).  A question number
    # is printed on that first row; the same digit lower down is a label
    # inside a figure/table (map circle '1', 9700/42/F/M/21 Q2(c); Table 3.1
    # row labels 1-3 in the gutter, 9700/52/F/M/22 Q3)
    qstart = {}
    for lab, segs in spec["crops"].items():
        n = int(re.match(r"Q(\d+)", lab).group(1))
        for sg in segs:
            if n not in qstart or (sg[0], sg[1]) < qstart[n]:
                qstart[n] = (sg[0], sg[1])
    for page in doc:
        if page.number == 0:
            continue
        ws = page.get_text("words")
        for w in ws:
            # a question NUMBER: one of this paper's questions, full-size
            # (a superscript '2' of 'T2' beside a graph is not), leftmost on its line
            if (re.fullmatch(r"\d{1,2}", w[4]) and int(w[4]) in qnums and 40 <= w[0] <= 62
                    and qstart[int(w[4])][0] == page.number + 1 and w[1] >= qstart[int(w[4])][1] - 20
                    and not any(re.fullmatch(r"\d{1,2}", v[4]) and v[4] == w[4] and 40 <= v[0] <= 62
                                and qstart[int(w[4])][1] - 20 <= v[1] < w[1] - 1 for v in ws)
                    and 55 <= w[1] <= 790 and (w[3] - w[1]) >= 9
                    # (the rotated margin strip at x<38 is not a word on the line)
                    and not any(v is not w and abs(v[1] - w[1]) < 3 and v[2] <= w[0] and v[0] >= 38 for v in ws)):
                page.draw_rect(fitz.Rect(34, w[1] - 1.5, w[2] + 3, w[3] + 1.5),
                               color=None, fill=(1, 1, 1), width=0, overlay=True)
    for m in spec.get("masks", []):
        doc[m[0] - 1].draw_rect(fitz.Rect(m[1:5]), color=None, fill=(1, 1, 1), width=0, overlay=True)
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    for f in out.glob(f"{prefix}-Q*.png"):
        f.unlink()
    k = DPI / 72.0
    prov = {}
    for label, segs in spec["crops"].items():
        images, lefts = [], []
        segs = sorted(segs, key=lambda s: (s[0], s[1]))   # page order, whatever the spec order
        for seg in segs:
            pno, y0, y1 = seg[0], seg[1], seg[2]
            x0, x1 = (seg[3], seg[4]) if len(seg) == 5 else (sp.CONTENT_L, sp.CONTENT_R)
            pix = doc[pno - 1].get_pixmap(clip=fitz.Rect(x0, y0, x1, y1), dpi=DPI)
            im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
            a = np.asarray(im.convert("L"))
            rows = np.where((a < 235).any(axis=1))[0]
            if not len(rows):
                raise SystemExit(f"{label}: empty segment {seg}")
            pad = int(4 * k)
            im = im.crop((0, max(0, rows[0] - pad), im.width, min(im.height, rows[-1] + pad + 1)))
            images.append(im)
            lefts.append(x0)
            prov.setdefault(label, []).append({"pdf_page": pno, "clip_points": [x0, y0, x1, y1],
                                               "semantic_bounds_points": [y0, y1],
                                               "two_dimensional_seam": False, "manual": True})
        left0 = min(lefts)
        offs = [round((lx - left0) * k) for lx in lefts]
        width = max(im.width + o for im, o in zip(images, offs))
        sep = round(SEP_PT * k)
        height = sum(im.height for im in images) + sep * (len(images) - 1)
        final = Image.new("RGB", (width, height), "white")
        y = 0
        for im, o in zip(images, offs):
            final.paste(im, (o, y))
            y += im.height + sep
        final.save(out / f"{prefix}-{label}.png", optimize=True)
    (out / f"{prefix}-split-provenance.json").write_text(json.dumps(
        {"source_pdf": src, "prefix": prefix, "manual_spec": str(Path(spec_path).resolve()),
         "accepted_blank_bands": spec.get("accept_blank", {}),
         "manual_masks": spec.get("masks", []),
         "accepted_plain_rows": spec.get("accept_plain", {}),
         "accepted_absent_leaves": spec.get("accept_absent_leaves", {}),
         "outputs": prov}, indent=1) + "\n")
    print(f"{len(spec['crops'])} crops -> {out}")


def cmd_run(prefix: str) -> int:
    spec = MANUAL / f"{prefix}.json"
    out = DATA / "splits" / "manual" / prefix
    render(str(spec), str(out))
    src = str(CANON / json.load(open(spec))["source"])
    py = sys.executable
    l1 = subprocess.run([py, "-I", str(HERE / "al_verify_leaves.py"), src, str(out), prefix],
                        capture_output=True, text=True).stdout
    l2 = subprocess.run([py, "-I", str(HERE / "al_verify_coverage.py"), src, str(out), prefix],
                        capture_output=True, text=True).stdout
    (out / "gates.log").write_text(l1 + "\n" + l2)
    print([l for l in l1.splitlines() if l.startswith("expected=")][-1:])
    print([l for l in l2.splitlines() if not l.startswith("pages ")][:12])
    print([l for l in l2.splitlines() if l.startswith("pages ")][-1:])
    rev = DATA / "review" / "manual"
    rev.mkdir(parents=True, exist_ok=True)
    for f in rev.glob(f"{prefix}_*.jpg"):
        f.unlink()
    subprocess.run([py, "-I", str(HERE / "al_contact_sheet.py"), str(out), prefix, str(rev / prefix),
                    "--per", "9", "--width", "1000"], stdout=subprocess.DEVNULL)
    return 0


def main() -> int:
    cmd = sys.argv[1]
    if cmd == "lines":
        cmd_lines(sys.argv[2], int(sys.argv[3]))
    elif cmd == "init":
        cmd_init(sys.argv[2], sys.argv[3])
    elif cmd == "render":
        render(sys.argv[2], sys.argv[3])
    elif cmd == "run":
        return cmd_run(sys.argv[2])
    return 0


if __name__ == "__main__":
    sys.exit(main())
