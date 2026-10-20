#!/usr/bin/env python3
"""Collect a regression's papers that need visual review into one run.

After al_regress.py, the papers to review (classes newpass + changed) sit in
splits/<NEW>_cNN/.  This moves them into splits/<NEW>/, renders their contact
sheets into review/<NEW>/ and writes review groups of N papers
(review/<NEW>/_review_groups/group_KK.txt: PREFIX followed by sheet paths),
the layout REVIEW_AGENT_PROMPT.txt and al_check_verdicts.py expect.

Usage: al_prepare_review.py NEW [--per 6] [--classes newpass,changed]
       al_prepare_review.py RUN --summary [--per 6]
           (a first batch: every PASS paper of RUN that is not an alias in
            review/RUN/duplicates.csv; nothing is moved)
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("new")
    ap.add_argument("--per", type=int, default=6)
    ap.add_argument("--classes", default="newpass,changed")
    ap.add_argument("--summary", action="store_true")
    a = ap.parse_args()
    want = set(a.classes.split(","))
    rev = DATA / "review" / a.new
    dst = DATA / "splits" / a.new
    dst.mkdir(parents=True, exist_ok=True)
    if a.summary:
        dup = rev / "duplicates.csv"
        aliases = {r["alias"] for r in csv.DictReader(open(dup))} if dup.exists() else set()
        # papers already approved with byte-identical crops need no review
        import hashlib, json
        hf = DATA / "review" / "reviewed_crop_hashes.json"
        approved = json.load(open(hf)).get(a.new, {}) if hf.exists() else {}

        def unchanged(prefix: str) -> bool:
            d = dst / prefix
            now = {f.name: hashlib.sha256(f.read_bytes()).hexdigest()
                   for f in list(d.glob(f"{prefix}-Q*.png")) + list(d.glob(f"{prefix}-SecB*.png"))}
            return bool(approved.get(prefix)) and approved[prefix] == now
        rows = [{"prefix": r["prefix"], "run": a.new} for r in csv.DictReader(open(rev / "run_summary.csv"))
                if r["status"] == "PASS" and r["prefix"] not in aliases and not unchanged(r["prefix"])]
    else:
        rows = [r for r in csv.DictReader(open(rev / "compare.csv")) if r["class"] in want]
    seen = set()
    papers = []
    for r in rows:
        if r["prefix"] in seen:
            continue
        seen.add(r["prefix"])
        src = DATA / "splits" / r["run"] / r["prefix"]
        if src.exists() and src != dst / r["prefix"]:
            if (dst / r["prefix"]).exists():
                shutil.rmtree(dst / r["prefix"])
            shutil.move(str(src), str(dst / r["prefix"]))
        papers.append(r["prefix"])
    for p in papers:
        for old in rev.glob(f"{p}_*.jpg"):
            old.unlink()
        subprocess.run([sys.executable, "-I", str(HERE / "al_contact_sheet.py"), str(dst / p), p,
                        str(rev / p), "--per", "9", "--width", "1000"], check=True,
                       stdout=subprocess.DEVNULL)
    gdir = rev / "_review_groups"
    if gdir.exists():
        shutil.rmtree(gdir)
    gdir.mkdir()
    papers.sort()
    for k in range(0, len(papers), a.per):
        lines = []
        for p in papers[k:k + a.per]:
            sheets = sorted(str(s) for s in rev.glob(f"{p}_*.jpg"))
            lines.append(" ".join([p] + sheets))
        (gdir / f"group_{k // a.per + 1:02d}.txt").write_text("\n".join(lines) + "\n")
    print(f"{len(papers)} papers -> {(len(papers) + a.per - 1) // a.per} groups in {gdir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
