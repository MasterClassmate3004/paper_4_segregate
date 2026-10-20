#!/usr/bin/env python3
"""Cross-check reviewer-agent verdict files against the real crops/sheets.

A group is ACCEPTED only if, for every paper assigned to it, the agent read
every contact sheet and saw every crop (counts must match exactly).  Papers
with defects are listed for manual inspection.  Groups with no verdict file
or mismatched counts must be re-reviewed.

Usage: al_check_verdicts.py RUN
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

DATA = Path.home() / "rootatom_data" / "ALEVEL"


def main() -> int:
    run = sys.argv[1]
    rev, spl = DATA / "review" / run, DATA / "splits" / run
    groups = sorted((rev / "_review_groups").glob("group_*.txt"))
    accepted, redo, defects, pending = [], [], [], []
    for g in groups:
        n = g.stem.split("_")[1]
        assigned = [line.split()[0] for line in g.read_text().splitlines() if line.strip()]
        vf = rev / "_verdicts" / f"group_{n}.json"
        if not vf.exists():
            pending.append(n)
            continue
        try:
            verdicts = {v["prefix"]: v for v in json.load(open(vf))}
        except Exception as exc:
            redo.append((n, f"unreadable verdict: {exc}"))
            continue
        problems = []
        for p in assigned:
            v = verdicts.get(p)
            real_crops = len(list((spl / p).glob(f"{p}-Q*.png")))
            real_sheets = len(list(rev.glob(f"{p}_*.jpg")))
            if v is None:
                problems.append(f"{p} missing")
            elif v.get("crops_seen") != real_crops or v.get("sheets_read") != real_sheets:
                problems.append(f"{p} seen {v.get('crops_seen')}/{real_crops} crops, "
                                f"{v.get('sheets_read')}/{real_sheets} sheets")
            else:
                for d in v.get("defects", []):
                    defects.append((n, p, d.get("label"), d.get("rule"), d.get("what")))
        (redo if problems else accepted).append((n, problems) if problems else n)
    print(f"groups: {len(groups)}  accepted={len(accepted)}  redo={len(redo)}  pending={len(pending)}")
    for n, why in redo:
        print("  REDO", n, why)
    print(f"defects flagged: {len(defects)}")
    for d in defects:
        print("  DEFECT", *d)
    if pending:
        print("  pending:", " ".join(pending))
    return 0


if __name__ == "__main__":
    sys.exit(main())
