#!/usr/bin/env python3
"""Find variants that are the SAME paper (Cambridge reuses papers across
time zones) and record canonical/alias pairs.

Decision 2026-10-11 (user): keep one copy -- the lowest variant is canonical,
the others are aliases (recorded, not reviewed, not classified, not uploaded
as separate questions).

Two papers are the same when every crop label matches, every crop has the same
pixel size, and every crop image is identical up to anti-aliasing: fewer than
0.05% of pixels differ by more than 96 grey levels (a re-typeset PDF of the
same paper renders a few edge pixels differently; any changed word, digit or
figure line differs in far more pixels than that) AND the PDF words inside
every crop's clip rectangles are the same multiset (so a changed number or
word can never be hidden under the pixel tolerance).

Writes review/<RUN>/duplicates.csv: canonical,alias,crops
Usage: al_dedupe.py RUN
"""

from __future__ import annotations

import collections
import csv
import hashlib
import sys

import json

import numpy as np
import pymupdf as fitz
from PIL import Image
from pathlib import Path

DATA = Path.home() / "rootatom_data" / "ALEVEL"


def crops_of(p: Path) -> dict[str, Path]:
    return {f.name.split("-QP-")[1]: f for f in p.glob("*-Q*.png")}


def sha(f: Path) -> bytes:
    return hashlib.sha256(f.read_bytes()).digest()


def near_identical(a: Path, b: Path) -> bool:
    if hashlib.sha256(a.read_bytes()).digest() == hashlib.sha256(b.read_bytes()).digest():
        return True
    x, y = Image.open(a).convert("L"), Image.open(b).convert("L")
    if x.size != y.size:
        return False
    d = np.abs(np.asarray(x, dtype=np.int16) - np.asarray(y, dtype=np.int16))
    return (d > 96).sum() < 0.0005 * d.size


def crop_texts(p: Path) -> dict[str, list[str]]:
    prov = json.load(open(p / f"{p.name}-split-provenance.json"))
    doc = fitz.open(prov["source_pdf"])
    out = {}
    for lab, segs in prov["outputs"].items():
        ws = []
        for sg in segs:
            r = fitz.Rect(sg["clip_points"])
            ws += [w[4] for w in sorted(doc[sg["pdf_page"] - 1].get_text("words"), key=lambda w: (round(w[1]), w[0]))
                   if r.contains(fitz.Point((w[0] + w[2]) / 2, (w[1] + w[3]) / 2))]
        out[lab] = sorted(ws)                 # word multiset: order noise from baseline jitter
    return out


def main() -> int:
    run = sys.argv[1]
    root = DATA / "splits" / run
    # candidate groups: same session + same label set + same crop sizes
    sig = collections.defaultdict(list)
    for p in sorted(root.iterdir()):
        if not (p / f"{p.name}-split-provenance.json").exists():
            continue                          # held / partial split
        crops = crops_of(p)
        if not crops:
            continue
        key = tuple(sorted((lab, Image.open(f).size) for lab, f in crops.items()))
        sig[(p.name.rsplit("-", 2)[0][:-1], key)].append(p)   # AL-PHY-14w-1x
    rows = []
    for members in sig.values():
        members.sort(key=lambda q: q.name)    # lowest variant first
        canon_of: list[Path] = []
        for p in members:
            cp = crops_of(p)
            for c in canon_of:
                cc = crops_of(c)
                exact = all(sha(cc[lab]) == sha(cp[lab]) for lab in cc)
                if exact or (all(near_identical(cc[lab], cp[lab]) for lab in cc)
                             and crop_texts(c) == crop_texts(p)):
                    rows.append({"canonical": c.name, "alias": p.name, "crops": len(cp)})
                    break
            else:
                canon_of.append(p)
    out = DATA / "review" / run / "duplicates.csv"
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["canonical", "alias", "crops"])
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} alias papers -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
