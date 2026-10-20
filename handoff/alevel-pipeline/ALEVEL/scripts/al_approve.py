#!/usr/bin/env python3
"""Record visually approved papers: their current crop hashes go into
review/reviewed_crop_hashes.json[RUN], so later review rounds skip them while
their crops stay byte-identical (al_prepare_review.py --summary).

Usage: al_approve.py RUN PREFIX ... [--groups NN ...] [--except PREFIX ...] [--revoke PREFIX ...]
  --groups: approve every paper listed in review/RUN/_review_groups/group_NN.txt
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

DATA = Path.home() / "rootatom_data" / "ALEVEL"


def crops(run: str, prefix: str) -> dict:
    d = DATA / "splits" / run / prefix
    return {f.name: hashlib.sha256(f.read_bytes()).hexdigest()
            for f in sorted(list(d.glob(f"{prefix}-Q*.png")) + list(d.glob(f"{prefix}-SecB*.png")))}


def main() -> int:
    a = sys.argv[1:]
    run, rest = a[0], a[1:]
    mode, papers, excl, revoke = "p", [], set(), []
    for t in rest:
        if t in ("--groups", "--except", "--revoke"):
            mode = t
            continue
        if mode == "--groups":
            g = DATA / "review" / run / "_review_groups" / f"group_{int(t):02d}.txt"
            papers += [l.split()[0] for l in open(g) if l.strip()]
        elif mode == "--except":
            excl.add(t)
        elif mode == "--revoke":
            revoke.append(t)
        else:
            papers.append(t)
    hf = DATA / "review" / "reviewed_crop_hashes.json"
    d = json.load(open(hf))
    d.setdefault(run, {})
    n = 0
    for p in papers:
        if p in excl:
            continue
        h = crops(run, p)
        if h:
            d[run][p] = h
            n += 1
    for p in revoke:
        d[run].pop(p, None)
    json.dump(d, open(hf, "w"), indent=0)
    print(f"approved {n}, revoked {len(revoke)}; {run} now has {len(d[run])} approved papers")
    return 0


if __name__ == "__main__":
    sys.exit(main())
