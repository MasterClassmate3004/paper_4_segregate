#!/usr/bin/env python3
"""QP regression against approved hashes, in chunks, under the disk guard.

Re-splits every approved non-alias paper of APPROVED_RUN (its hashes in
reviewed_crop_hashes.json) into the scratch run NEW_RUN, 40 papers at a time,
and compares each paper's crops with the approved hashes.  Labels removed for
having no mark scheme (review/removed_no_ms.csv) are ignored.  PNGs of
identical papers are deleted at once; changed papers are kept for a look and
listed.  Papers whose approved crops came from manual specs (_<run>_manual)
are skipped (they are rendered by al_manual.py, not the splitter).

Usage: al_qp_regress.py APPROVED_RUN NEW_RUN [--prefix AL-CHE-] [--chunk 40]
"""
from __future__ import annotations

import csv
import glob
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = Path.home() / "rootatom_data" / "ALEVEL"
PY = str(Path.home() / ".venvs" / "alevel" / "bin" / "python")


def main() -> int:
    a = sys.argv[1:]
    run, new = a[0], a[1]
    pre = a[a.index("--prefix") + 1] if "--prefix" in a else "AL-"
    chunk = int(a[a.index("--chunk") + 1]) if "--chunk" in a else 40
    H = json.load(open(DATA / "review" / "reviewed_crop_hashes.json"))
    ref = {p: h for p, h in H[run].items() if p.startswith(pre)}
    manual = set(H.get(f"_{run}_manual", []))
    src = {}
    own = DATA / "review" / run / "run_summary.csv"      # the approved run's own sources first
    for f in [str(own)] + sorted(glob.glob(str(DATA / "review" / "*" / "run_summary.csv"))):
        if Path(f).exists():
            for r in csv.DictReader(open(f)):
                src.setdefault(r["prefix"], r["source"])
    removed = {(r["prefix"], r["label"]) for r in csv.DictReader(open(DATA / "review" / "removed_no_ms.csv"))}
    todo = [p for p in sorted(ref) if p not in manual and p in src]
    sys.path.insert(0, str(HERE))
    import al_space
    same, changed, hold = 0, [], []
    (DATA / "review" / new).mkdir(parents=True, exist_ok=True)
    for i in range(0, len(todo), chunk):
        part = todo[i:i + chunk]
        if not al_space.ok():
            print(f"disk guard {al_space.free_gb():.2f} GB: stopping at {i}", flush=True)
            break
        lst = DATA / "review" / new / "_chunk.txt"
        lst.write_text("\n".join(src[p] for p in part) + "\n")
        subprocess.run([PY, str(HERE / "al_run_papers.py"), new, "--list", str(lst), "--no-sheets", "--workers", "3"],
                       capture_output=True)
        st = {r["prefix"]: r["status"] for r in csv.DictReader(open(DATA / "review" / new / "run_summary.csv"))}
        for p in part:
            d = DATA / "splits" / new / p
            if st.get(p) != "PASS":
                hold.append(p)
                continue
            cur = {os.path.basename(f): hashlib.sha256(open(f, "rb").read()).hexdigest()
                   for f in glob.glob(f"{d}/*-Q*.png") + glob.glob(f"{d}/*-SecB*.png")
                   if (p, os.path.basename(f)[len(p) + 1:-4]) not in removed}
            if cur == ref[p]:
                same += 1
                shutil.rmtree(d, ignore_errors=True)
            else:
                changed.append(p)
        print(f"chunk {i // chunk + 1}: same {same} changed {len(changed)} hold {len(hold)}", flush=True)
    print("CHANGED", " ".join(changed))
    print("HOLD", " ".join(hold))
    return 0


if __name__ == "__main__":
    sys.exit(main())
