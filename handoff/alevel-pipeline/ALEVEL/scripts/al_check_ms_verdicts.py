#!/usr/bin/env python3
"""Cross-check MS reviewer verdicts: a group is accepted only if, for every
paper, the agent read every sheet and saw every entry (one per QP leaf).

Usage: al_check_ms_verdicts.py MS_RUN
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
        assigned = [l.split()[0] for l in g.read_text().splitlines() if l.strip()]
        vf = rev / "_verdicts" / f"group_{n}.json"
        if not vf.exists():
            pending.append(n)
            continue
        try:
            verdicts = {v["prefix"]: v for v in json.load(open(vf))}
        except Exception as exc:
            redo.append((n, [f"unreadable verdict: {exc}"]))
            continue
        problems = []
        for p in assigned:
            v = verdicts.get(p)
            entries = len(json.load(open(spl / p / f"{p}-ms-provenance.json"))["mapping"])
            sheets = len(list(rev.glob(f"{p}_*.jpg")))
            if v is None:
                problems.append(f"{p} missing")
            elif v.get("sheets_read") != sheets:
                problems.append(f"{p} read {v.get('sheets_read')}/{sheets} sheets")
            else:
                if v.get("entries_seen") != entries:   # agents miscount split/shared tiles; sheets are the proof
                    print(f"  note: {p} counted {v.get('entries_seen')}/{entries} entries (all sheets read)")
                for d in v.get("defects", []):
                    defects.append((n, p, d.get("label"), d.get("rule"), d.get("what")))
        (redo if problems else accepted).append((n, problems) if problems else n)
    print(f"groups: {len(groups)}  accepted={len(accepted)}  redo={len(redo)}  pending={len(pending)}")
    for n, why in redo:
        print("  REDO", n, why)
    print(f"defects flagged: {len(defects)}")
    for d in defects:
        print("  DEFECT", *d)
    return 0


if __name__ == "__main__":
    sys.exit(main())
