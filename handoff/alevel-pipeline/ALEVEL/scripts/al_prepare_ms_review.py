#!/usr/bin/env python3
"""Paired QP|MS sheets + review groups for every PASS structured mark scheme.

Usage: al_prepare_ms_review.py QP_RUN MS_RUN [--per 6] [--only PREFIX ...]
Sheets: review/<MS_RUN>/<MSPREFIX>_NN.jpg; groups: review/<MS_RUN>/_review_groups/group_KK.txt
"""

from __future__ import annotations

import csv
import json
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

DATA = Path.home() / "rootatom_data" / "ALEVEL"
HERE = Path(__file__).resolve().parent


def main() -> int:
    a = sys.argv[1:]
    qp_run, ms_run = a[0], a[1]
    per = int(a[a.index("--per") + 1]) if "--per" in a else 6
    only = set(a[a.index("--only") + 1:]) if "--only" in a else None
    rev = DATA / "review" / ms_run
    papers = []
    for r in csv.DictReader(open(rev / "ms_summary.csv")):
        p = r["prefix"]
        if r["status"] != "PASS" or (only and p not in only):
            continue
        prov = json.load(open(DATA / "splits" / ms_run / p / f"{p}-ms-provenance.json"))
        if prov.get("kind") == "mcq_key":
            continue
        papers.append(p)

    def sheet(p):
        for old in rev.glob(f"{p}_*.jpg"):
            old.unlink()
        q = p[:-3] + "-QP"
        subprocess.run([sys.executable, "-I", str(HERE / "al_ms_sheet.py"), str(DATA / "splits" / ms_run / p), p,
                        str(DATA / "splits" / qp_run / q), q, str(rev / p), "--per", "7", "--width", "1400"],
                       check=True, stdout=subprocess.DEVNULL)

    with ThreadPoolExecutor(6) as ex:
        list(ex.map(sheet, papers))
    gdir = rev / "_review_groups"
    if gdir.exists() and not only:
        shutil.rmtree(gdir)
    gdir.mkdir(exist_ok=True)
    papers.sort()
    for k in range(0, len(papers), per):
        lines = [" ".join([p] + sorted(str(s) for s in rev.glob(f"{p}_*.jpg"))) for p in papers[k:k + per]]
        (gdir / f"group_{k // per + 1:02d}.txt").write_text("\n".join(lines) + "\n")
    print(f"{len(papers)} papers -> {(len(papers) + per - 1) // per} groups")
    return 0


if __name__ == "__main__":
    sys.exit(main())
