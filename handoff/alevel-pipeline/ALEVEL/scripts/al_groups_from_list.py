#!/usr/bin/env python3
"""Contact sheets + review groups for an explicit list of papers.

For every prefix in LIST (first word of each line), render the labelled
contact sheets of splits/<CROPS_RUN>/<PREFIX>/ into review/<REVIEW_RUN>/ and
write review groups review/<REVIEW_RUN>/_review_groups/group_NN.txt in the
layout REVIEW_AGENT_PROMPT_QP.txt and al_check_verdicts.py expect
(one line per paper: PREFIX followed by its sheet paths).

Groups are filled up to --max-sheets contact sheets (default 40): review
agents that read more images than that stall or hit the image request limit.

Usage: al_groups_from_list.py CROPS_RUN REVIEW_RUN LIST [--start N] [--max-sheets 40]
  CROPS_RUN  e.g. bio_b1 (automatic run) or manual (crops of manual specs)
  --start    first group number (default: one past the highest existing group)
"""
from __future__ import annotations

import argparse
import glob
import re
import subprocess
from pathlib import Path

DATA = Path.home() / "rootatom_data" / "ALEVEL"
HERE = Path(__file__).resolve().parent
PY = str(Path.home() / ".venvs" / "alevel" / "bin" / "python")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("crops_run")
    ap.add_argument("review_run")
    ap.add_argument("list")
    ap.add_argument("--start", type=int)
    ap.add_argument("--max-sheets", type=int, default=40)
    a = ap.parse_args()
    rev = DATA / "review" / a.review_run
    groups = rev / "_review_groups"
    groups.mkdir(parents=True, exist_ok=True)
    (rev / "_verdicts").mkdir(exist_ok=True)
    prefixes = [l.split()[0] for l in open(a.list) if l.strip()]
    lines = []
    for p in prefixes:
        crops = DATA / "splits" / a.crops_run / p
        if not crops.is_dir():
            print("no crops:", crops)
            continue
        subprocess.run([PY, "-I", str(HERE / "al_contact_sheet.py"), str(crops), p, str(rev / p)],
                       capture_output=True)
        sheets = sorted(glob.glob(str(rev / f"{p}_*.jpg")))
        if not sheets:
            print("no sheets rendered:", p)
            continue
        lines.append((p, sheets))
    existing = [int(m.group(1)) for g in groups.glob("group_*.txt") if (m := re.search(r"(\d+)", g.stem))]
    n = a.start if a.start is not None else (max(existing) + 1 if existing else 1)
    cur, count, made = [], 0, []
    for p, sheets in lines:
        if cur and count + len(sheets) > a.max_sheets:
            (groups / f"group_{n:02d}.txt").write_text("\n".join(cur) + "\n")
            made.append(n); n += 1; cur, count = [], 0
        cur.append(p + " " + " ".join(sheets)); count += len(sheets)
    if cur:
        (groups / f"group_{n:02d}.txt").write_text("\n".join(cur) + "\n")
        made.append(n)
    print(f"{len(lines)} papers -> {len(made)} groups"
          + (f" ({made[0]:02d}-{made[-1]:02d})" if made else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
