#!/usr/bin/env python3
"""Re-run an MS run in small chunks under a tight disk budget.

For each chunk of papers: al_run_ms.py QP_RUN MS_RUN --only <chunk>, then compare
every paper's crops with the reference hashes (reviewed_crop_hashes.json[MS_RUN],
plus an optional JSON file of {prefix: {crop: sha256}}).  Byte-identical papers
whose PNGs are already on Google Drive (offload ledger, same members hash) have
their local PNGs deleted again; changed papers are kept and listed.

Usage: al_rerun_chunked.py QP_RUN MS_RUN [--chunk 40] [--ref extra.json] [--out changed.txt]
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

HERE = Path(__file__).resolve().parent
DATA = Path.home() / "rootatom_data" / "ALEVEL"
PY = str(Path.home() / ".venvs" / "alevel" / "bin" / "python")


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> int:
    a = sys.argv[1:]
    qp_run, ms_run = a[0], a[1]
    chunk = int(a[a.index("--chunk") + 1]) if "--chunk" in a else 40
    ref = json.load(open(DATA / "review" / "reviewed_crop_hashes.json")).get(ms_run, {})
    if "--ref" in a:
        ref = {**json.load(open(a[a.index("--ref") + 1])), **ref}
    out = a[a.index("--out") + 1] if "--out" in a else None
    led = {(r["run"], r["prefix"]): r for r in csv.DictReader(open(DATA / "review" / "offload_ledger.csv"))}
    rows = [r for r in csv.DictReader(open(DATA / "review" / ms_run / "ms_summary.csv")) if r["status"] == "PASS"]
    papers = [r["prefix"] for r in rows]
    changed, same, new, fail = [], 0, [], []
    sys.path.insert(0, str(HERE))
    import al_space
    for i in range(0, len(papers), chunk):
        part = papers[i:i + chunk]
        if not al_space.ok():
            print(f"disk guard: {al_space.free_gb():.2f} GB free, stopping at {i}")
            break
        subprocess.run([PY, str(HERE / "al_run_ms.py"), qp_run, ms_run, "--workers", "3", "--only"]
                       + [p[:-3] + "-QP" for p in part], capture_output=True)
        st = {r["prefix"]: r["status"] for r in csv.DictReader(open(DATA / "review" / ms_run / "ms_summary.csv"))}
        for p in part:
            if st.get(p) != "PASS":
                fail.append(p)
                continue
            fs = sorted(glob.glob(str(DATA / "splits" / ms_run / p / "*-Q*.png")))
            cur = {os.path.basename(f): sha(open(f, "rb").read()) for f in fs}
            if p not in ref:
                new.append(p)
            elif cur != ref[p]:
                changed.append(p)
            else:
                same += 1
                r = led.get((ms_run, p))
                allp = sorted(glob.glob(str(DATA / "splits" / ms_run / p / "*.png")))
                loc = {os.path.basename(f): sha(open(f, "rb").read()) for f in allp}
                if r and r["members_sha256"] == sha("".join(f"{k}:{v}\n" for k, v in sorted(loc.items())).encode()):
                    for f in allp:
                        os.remove(f)
        print(f"chunk {i // chunk + 1}: same {same} changed {len(changed)} unreviewed {len(new)} fail {len(fail)}", flush=True)
    print("CHANGED", " ".join(changed))
    print("UNREVIEWED", " ".join(new))
    print("FAIL", " ".join(fail))
    if out:
        Path(out).write_text("\n".join(changed) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
