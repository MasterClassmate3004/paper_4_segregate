#!/usr/bin/env python3
"""Disk-frugal regression: re-split a list in chunks, keep only what changed.

For each chunk of the list: run al_run_papers.py (no contact sheets) into
<NEW>_cK, compare with BASE (al_compare_runs.py), delete the split dirs of
papers whose crops are byte-identical ('same') or that stay on hold, and
append the chunk's compare rows to review/<NEW>/compare.csv.  What remains
under splits/<NEW>_cK is exactly the work to look at: changed, newpass,
regressed.

Usage: al_regress.py BASE NEW LIST [--chunk 80] [--workers 6]
"""

from __future__ import annotations

import argparse
import csv
import shutil
import subprocess
import sys
from pathlib import Path

DATA = Path.home() / "rootatom_data" / "ALEVEL"
HERE = Path(__file__).resolve().parent
PY = sys.executable


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("base")
    ap.add_argument("new")
    ap.add_argument("list")
    ap.add_argument("--chunk", type=int, default=80)
    ap.add_argument("--workers", type=int, default=6)
    a = ap.parse_args()
    names = [l.strip() for l in open(a.list) if l.strip()]
    (DATA / "review" / a.new).mkdir(parents=True, exist_ok=True)
    out = DATA / "review" / a.new / "compare.csv"
    all_rows = []
    for k in range(0, len(names), a.chunk):
        run = f"{a.new}_c{k // a.chunk:02d}"
        chunk = DATA / "review" / f"{run}.list"
        chunk.write_text("\n".join(names[k:k + a.chunk]) + "\n")
        subprocess.run([PY, "-I", str(HERE / "al_run_papers.py"), run, "--list", str(chunk),
                        "--workers", str(a.workers), "--no-sheets"], check=True,
                       stdout=subprocess.DEVNULL)
        subprocess.run([PY, "-I", str(HERE / "al_compare_runs.py"), a.base, run], check=True)
        rows = list(csv.DictReader(open(DATA / "review" / run / "compare.csv")))
        for r in rows:
            r["run"] = run
            if r["class"] in ("same", "hold"):
                shutil.rmtree(DATA / "splits" / run / r["prefix"], ignore_errors=True)
        all_rows += rows
        with open(out, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(all_rows[0]))
            w.writeheader()
            w.writerows(all_rows)
    counts: dict[str, int] = {}
    for r in all_rows:
        counts[r["class"]] = counts.get(r["class"], 0) + 1
    print("TOTAL", counts)
    for r in all_rows:
        if r["class"] in ("regressed", "changed", "newpass"):
            print(f"  {r['class'].upper():9s} {r['prefix']} ({r['run']}) {r['reason'][:100]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
