#!/usr/bin/env python3
"""Redo an approved, offloaded QP set for the D6 marks fix (7e57f2d), in chunks.

For each chunk of approved non-alias papers of OLD_RUN (excluding manual-spec
papers): al_run_papers.py NEW_RUN <sources> --no-sheets, pull the approved
OLD_RUN crops from Google Drive, and classify every paper:
  unchanged  - crops byte-identical to the approved hashes
  marks_only - every changed crop keeps its old segments in order and only adds
               segments that a dot mask (provenance manual_masks) covers, and the
               old image survives pixel-for-pixel as the top of the new one
  other      - anything else (needs eyes), or not PASS
unchanged + marks_only are approved under NEW_RUN and pushed to Drive; the
pulled OLD_RUN PNGs are deleted again; 'other' papers stay local for review.

Usage: al_marks_redo.py OLD_RUN NEW_RUN [--chunk 40] [--max-chunks N] [--out results.json]
"""
from __future__ import annotations

import csv
import glob
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
DATA = Path.home() / "rootatom_data" / "ALEVEL"
PY = str(Path.home() / ".venvs" / "alevel" / "bin" / "python")
SPL = DATA / "splits"


def sha(p: str) -> str:
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def classify(old_run: str, new_run: str, p: str, ref: dict) -> tuple[str, str]:
    nd, od = SPL / new_run / p, SPL / old_run / p
    cur = {os.path.basename(f): sha(f) for f in glob.glob(f"{nd}/*-Q*.png") + glob.glob(f"{nd}/*-SecB*.png")}
    if cur == ref:
        return "unchanged", ""
    if set(cur) != set(ref):
        return "other", "label set changed"
    po = json.load(open(od / f"{p}-split-provenance.json"))["outputs"]
    pn_all = json.load(open(nd / f"{p}-split-provenance.json"))
    pn, mm = pn_all["outputs"], pn_all.get("manual_masks", [])
    for f, h in sorted(cur.items()):
        if h == ref[f]:
            continue
        lab = f[len(p) + 1:-4]
        so = [(s["pdf_page"], [round(c, 1) for c in s["clip_points"]]) for s in po[lab]]
        sn = [(s["pdf_page"], [round(c, 1) for c in s["clip_points"]]) for s in pn[lab]]
        extra = [s for s in sn if s not in so]
        if [s for s in sn if s in so] != so or not extra:
            return "other", f"{lab}: segments changed"
        for pg, c in extra:
            if not any(m[0] == pg and c[1] - 2 <= m[2] and m[4] <= c[3] + 2 for m in mm):
                return "other", f"{lab}: extra segment without a dot mask"
        if not (od / f).exists():
            return "other", f"{lab}: approved image not restored"
        a = np.asarray(Image.open(od / f).convert("L")).astype(int)
        b = np.asarray(Image.open(nd / f).convert("L")).astype(int)
        if a.shape[1] != b.shape[1] or b.shape[0] < a.shape[0]:
            return "other", f"{lab}: shape {a.shape}->{b.shape}"
        h = a.shape[0] - 12             # the last few px may be re-padded
        if h > 0 and np.abs(a[:h] - b[:h]).max() > 40:
            return "other", f"{lab}: top differs"
    return "marks_only", ""


def main() -> int:
    a = sys.argv[1:]
    old_run, new_run = a[0], a[1]
    chunk = int(a[a.index("--chunk") + 1]) if "--chunk" in a else 40
    max_chunks = int(a[a.index("--max-chunks") + 1]) if "--max-chunks" in a else 10 ** 6
    out = Path(a[a.index("--out") + 1]) if "--out" in a else DATA / "review" / new_run / "marks_redo.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    H = json.load(open(DATA / "review" / "reviewed_crop_hashes.json"))
    ref_all, manual = H[old_run], set(H.get(f"_{old_run}_manual", []))
    alias = {r["alias"] for r in csv.DictReader(open(DATA / "review" / old_run / "duplicates.csv"))}
    src = {r["prefix"]: r["source"] for r in csv.DictReader(open(DATA / "review" / old_run / "run_summary.csv"))}
    todo = [p for p in sorted(ref_all) if p not in alias and p not in manual]
    res = json.load(open(out)) if out.exists() else {"unchanged": [], "marks_only": [], "other": {}}
    done = set(res["unchanged"]) | set(res["marks_only"]) | set(res["other"])
    todo = [p for p in todo if p not in done]
    sys.path.insert(0, str(HERE))
    import al_space
    for i in range(0, min(len(todo), chunk * max_chunks), chunk):
        part = todo[i:i + chunk]
        if not al_space.ok():
            print(f"disk guard: {al_space.free_gb():.2f} GB free; stopping", flush=True)
            break
        lst = DATA / "review" / new_run / "_chunk.txt"
        lst.write_text("\n".join(src[p] for p in part) + "\n")
        subprocess.run([PY, str(HERE / "al_run_papers.py"), new_run, "--list", str(lst), "--no-sheets",
                        "--workers", "3"], capture_output=True)
        subprocess.run([PY, str(HERE / "al_offload.py"), "pull", old_run] + part, capture_output=True)
        st = {r["prefix"]: r["status"] for r in csv.DictReader(open(DATA / "review" / new_run / "run_summary.csv"))}
        ok = []
        for p in part:
            if st.get(p) != "PASS":
                res["other"][p] = f"not PASS ({st.get(p)})"
                continue
            kind, why = classify(old_run, new_run, p, ref_all[p])
            if kind == "other":
                res["other"][p] = why
            else:
                res[kind].append(p)
                ok.append(p)
        for p in part:                   # the approved copies are on Drive
            for f in glob.glob(str(SPL / old_run / p / "*.png")):
                os.remove(f)
        if ok:
            subprocess.run([PY, str(HERE / "al_approve.py"), new_run] + ok, capture_output=True)
            subprocess.run([PY, str(HERE / "al_offload.py"), "push", new_run, "--only"] + ok, capture_output=True)
        json.dump(res, open(out, "w"), indent=1)
        print(f"chunk {i // chunk + 1}: unchanged {len(res['unchanged'])} marks_only {len(res['marks_only'])} "
              f"other {len(res['other'])}  free {al_space.free_gb():.2f} GB", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
