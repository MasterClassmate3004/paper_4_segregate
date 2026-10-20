#!/usr/bin/env python3
"""Compare a partial re-run against the base run, paper by paper.

For each paper in NEW: status in BASE vs NEW, and whether the crop set (names
+ sha256) is identical.  Classes:
  same       PASS->PASS, identical crops (approval carries over)
  changed    PASS->PASS, crops differ (needs visual re-review)
  newpass    HOLD->PASS (needs visual review)
  regressed  PASS->HOLD (inspect before anything else)
  hold       HOLD->HOLD
Writes review/<NEW>/compare.csv and prints counts + the regressed list.

Usage: al_compare_runs.py BASE NEW
"""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

DATA = Path.home() / "rootatom_data" / "ALEVEL"


def status(run: str) -> dict[str, dict]:
    return {r["prefix"]: r for r in csv.DictReader(open(DATA / "review" / run / "run_summary.csv"))}


def crops(run: str, prefix: str) -> dict[str, str]:
    d = DATA / "splits" / run / prefix
    return {f.name: hashlib.sha256(f.read_bytes()).hexdigest() for f in d.glob(f"{prefix}-Q*.png")}


def prov_sig(run: str, prefix: str) -> str:
    """Segment rectangles + masks: identical provenance renders identical
    crops, so this stands in for the PNGs once a base run is offloaded to
    Drive (al_offload.py keeps provenance local)."""
    f = DATA / "splits" / run / prefix / f"{prefix}-split-provenance.json"
    if not f.exists():
        return ""
    j = json.load(open(f))
    # only what reaches the pixels: page + clip rectangle per segment, masks
    # (semantic_bounds are internal and may move without changing a crop)
    segs = {k: [(s["pdf_page"], [round(x, 2) for x in s["clip_points"]]) for s in v]
            for k, v in (j.get("outputs") or {}).items()}
    return hashlib.sha256(json.dumps([segs, j.get("response_furniture_masks")],
                                     sort_keys=True).encode()).hexdigest()


def same_crops(base: str, new: str, prefix: str) -> bool:
    b = crops(base, prefix)
    if b:
        return b == crops(new, prefix)
    return bool(prov_sig(base, prefix)) and prov_sig(base, prefix) == prov_sig(new, prefix)


def main() -> int:
    base, new = sys.argv[1:3]
    bs, ns = status(base), status(new)
    rows = []
    for p, r in sorted(ns.items()):
        b = bs.get(p, {}).get("status", "MISSING")
        n = r["status"]
        if b == "PASS" and n == "PASS":
            cls = "same" if same_crops(base, new, p) else "changed"
        elif n == "PASS":
            cls = "newpass"
        elif b == "PASS":
            cls = "regressed"
        else:
            cls = "hold"
        rows.append({"prefix": p, "base": b, "new": n, "class": cls, "reason": r.get("reason", "")})
    with open(DATA / "review" / new / "compare.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["prefix", "base", "new", "class", "reason"])
        w.writeheader()
        w.writerows(rows)
    counts: dict[str, int] = {}
    for r in rows:
        counts[r["class"]] = counts.get(r["class"], 0) + 1
    print(counts)
    for r in rows:
        if r["class"] == "regressed":
            print("  REGRESSED", r["prefix"], r["reason"][:120])
    return 0


if __name__ == "__main__":
    sys.exit(main())
