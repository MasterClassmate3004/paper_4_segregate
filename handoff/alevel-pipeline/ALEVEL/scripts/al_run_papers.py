#!/usr/bin/env python3
"""Split A Level question papers and run every QA gate, one paper at a time.

For each canonical source name (e.g. 9702_s24_qp_22.pdf):
  1. al_qp_splitter.py     -> splits/<run>/<PREFIX>/   (+ provenance JSON)
  2. al_verify_leaves.py   -> exact leaf set vs the printed markers
  3. al_verify_coverage.py -> every question word in exactly one crop and
     no crop edge through ink
  4. al_contact_sheet.py   -> review/<run>/<PREFIX>_NN.png (100% visual review)

FAIL-CLOSED (2026-10-10): offloaded iCloud scripts once made every gate run
nothing and exit 0, so a paper "passed" unchecked.  A paper is PASS only when
the source exists, the splitter wrote crops + provenance, the leaf gate
printed an exact match and the coverage gate printed 0/0/0.  Anything else,
including missing or unparsable gate output, is HOLD with the reason.
Results: review/<run>/run_summary.csv.

Usage: al_run_papers.py RUN_NAME [names ...] [--list FILE] [--workers N] [--no-sheets]
Env:   ALEVEL_DATA (default ~/rootatom_data/ALEVEL)
"""

from __future__ import annotations

import csv
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = Path(os.environ.get("ALEVEL_DATA", Path.home() / "rootatom_data" / "ALEVEL"))
PY = str(Path.home() / ".venvs" / "alevel" / "bin" / "python")
SUBJ = {"9702": "PHY", "9701": "CHE", "9700": "BIO", "9709": "MTH", "9231": "FMT"}
NAME_RE = re.compile(r"^(\d{4})_([msw])(\d{2})_qp_(\d{1,2})\.pdf$")
LEAF_OK = re.compile(r"^expected=(\d+) produced=\1 missing=\[\] extra=\[\]$")
COV_OK = re.compile(r"^pages \d+-\d+: missing=0 duplicated=0 sliced_boundaries=0 ")


def prefix_for(name: str) -> str:
    code, sess, yy, comp = NAME_RE.match(name).groups()
    if len(comp) == 1:          # pre-variant papers map to the first variant
        comp = comp + "1"
    return f"AL-{SUBJ[code]}-{yy}{sess}-{comp}-QP"


def run(cmd: list[str]) -> tuple[int, str]:
    p = subprocess.run(cmd, capture_output=True, text=True)
    out = "\n".join(l for l in (p.stdout + p.stderr).splitlines() if "deprecat" not in l.lower())
    return p.returncode, out


def process(name: str, out_root: Path, rev_root: Path) -> dict:
    sys.path.insert(0, str(HERE)); import al_space
    if not al_space.ok():        # disk guard: stop cleanly instead of filling the disk
        return {"source": name, "prefix": prefix_for(name), "status": "HOLD", "crops": 0,
                "leaves": "", "coverage": "", "reason": f"disk guard: only {al_space.free_gb():.1f} GB free"}
    src = DATA / "source_papers" / "canonical" / name
    prefix = prefix_for(name)
    out = out_root / prefix
    row = {"source": name, "prefix": prefix, "status": "HOLD", "crops": 0,
           "leaves": "", "coverage": "", "reason": ""}
    if not src.exists():
        row["reason"] = "source not in canonical set"
        return row
    if out.exists():
        for f in out.iterdir():
            f.unlink()
    out.mkdir(parents=True, exist_ok=True)
    code, comp = name[:4], NAME_RE.match(name).group(4)
    mcq = code in {"9702", "9701", "9700"} and comp[0] == "1"   # science Paper 1
    splitter = "al_mcq_splitter.py" if mcq else "al_qp_splitter.py"
    rc, log = run([PY, "-I", str(HERE / splitter), str(src), str(out), prefix])
    (out / "splitter.log").write_text(log)
    crops = list(out.glob(f"{prefix}-Q*.png"))
    row["crops"] = len(crops)
    if rc != 0 or not crops or not (out / f"{prefix}-split-provenance.json").exists():
        row["reason"] = "splitter: " + (log.strip().splitlines() or ["no output"])[-1][:200]
        return row
    rc1, l1 = run([PY, "-I", str(HERE / "al_verify_leaves.py"), str(src), str(out), prefix])
    rc2, l2 = run([PY, "-I", str(HERE / "al_verify_coverage.py"), str(src), str(out), prefix])
    row["leaves"] = next((l for l in l1.splitlines() if l.startswith("expected=")), "NO OUTPUT")
    row["coverage"] = next((l for l in l2.splitlines() if l.startswith("pages ")), "NO OUTPUT")
    if not os.environ.get("AL_NO_SHEETS"):   # regression runs: sheets made later, only for changed papers
        run([PY, "-I", str(HERE / "al_contact_sheet.py"), str(out), prefix, str(rev_root / prefix),
             "--per", "9", "--width", "1000"])
    (out / "gates.log").write_text(l1 + "\n" + l2)
    leaves_ok = rc1 == 0 and bool(LEAF_OK.match(row["leaves"]))
    cov_ok = rc2 == 0 and bool(COV_OK.match(row["coverage"]))
    if leaves_ok and cov_ok:
        row["status"] = "PASS"
    else:
        row["reason"] = ("leaves " if not leaves_ok else "") + ("coverage" if not cov_ok else "")
    return row


def main() -> int:
    import argparse
    from concurrent.futures import ThreadPoolExecutor, as_completed
    ap = argparse.ArgumentParser()
    ap.add_argument("run_name")
    ap.add_argument("names", nargs="*")
    ap.add_argument("--list", help="file with one source name per line")
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--no-sheets", action="store_true", help="skip contact sheets (regression runs)")
    a = ap.parse_args()
    if a.no_sheets:
        os.environ["AL_NO_SHEETS"] = "1"
    names = list(a.names) + ([l.strip() for l in open(a.list) if l.strip()] if a.list else [])
    for script in ("al_qp_splitter.py", "al_mcq_splitter.py", "al_verify_leaves.py", "al_verify_coverage.py", "al_contact_sheet.py"):
        if (HERE / script).stat().st_size < 500:
            raise SystemExit(f"refusing to run: {script} looks empty/unreadable")
    out_root, rev_root = DATA / "splits" / a.run_name, DATA / "review" / a.run_name
    rev_root.mkdir(parents=True, exist_ok=True)
    rows = []
    with ThreadPoolExecutor(a.workers) as pool:   # each paper runs in its own subprocesses
        futs = {pool.submit(process, n, out_root, rev_root): n for n in names}
        for i, fut in enumerate(as_completed(futs), 1):
            try:
                row = fut.result()
            except Exception as exc:   # never lose a paper silently
                row = {"source": futs[fut], "prefix": "", "status": "HOLD", "crops": 0,
                       "leaves": "", "coverage": "", "reason": f"runner error: {exc}"}
            rows.append(row)
            print(f"[{i}/{len(names)}] {row['status']} {row['source']} crops={row['crops']} "
                  f"{row['reason'] or ''}", flush=True)
    # merge: a partial re-run (e.g. only the held papers) updates its rows and
    # keeps every other paper's row
    summ = rev_root / "run_summary.csv"
    if summ.exists():
        done = {r["source"] for r in rows}
        rows += [r for r in csv.DictReader(open(summ)) if r["source"] not in done]
    rows.sort(key=lambda r: r["source"])
    with open(summ, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"this run: PASS {sum(r['status'] == 'PASS' for r in rows if r['source'] in names)} / {len(names)}; "
          f"run total PASS {sum(r['status'] == 'PASS' for r in rows)} / {len(rows)}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
