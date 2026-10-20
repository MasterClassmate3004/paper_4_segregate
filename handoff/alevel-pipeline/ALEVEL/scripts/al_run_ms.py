#!/usr/bin/env python3
"""Split the mark schemes of an approved QP run, one paper at a time.

For each unique (non-alias) PASS paper of QP_RUN, find its mark scheme in the
canonical set (exact component, else the pre-2010 single-digit component file,
else a combined all-components booklet filtered by the page-header paper
number), run al_ms_splitter.py into splits/<MS_RUN>/<PREFIX>-MS/ and record
review/<MS_RUN>/ms_summary.csv.  PASS only on the splitter's explicit MS_OK
line (fail-closed, like al_run_papers.py).

Usage: al_run_ms.py QP_RUN MS_RUN [--only PREFIX ...] [--workers N]
"""

from __future__ import annotations

import csv
import os
import re
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = Path(os.environ.get("ALEVEL_DATA", Path.home() / "rootatom_data" / "ALEVEL"))
CANON = DATA / "source_papers" / "canonical"
PY = str(Path.home() / ".venvs" / "alevel" / "bin" / "python")
NAME_RE = re.compile(r"^(\d{4})_([msw]\d{2})_qp_(\d{1,2})\.pdf$")


def ms_source(qp_name: str) -> tuple[str | None, str | None]:
    """(ms file, component filter or None)."""
    code, ses, comp = NAME_RE.match(qp_name).groups()
    for c in [f"{code}_{ses}_ms_{comp}.pdf"] + ([f"{code}_{ses}_ms_{comp[0]}.pdf"] if len(comp) == 2 else []):
        if (CANON / c).exists():
            # a component file shared by variants (9702_s09_ms_2 holds 21 and 22)
            return c, (comp if c.endswith(f"_ms_{comp[0]}.pdf") and len(comp) == 2 else None)
    for c in (f"{code}_{ses}_ms.pdf", f"{code}_{ses}_ms_1+2+3+4+5+6.pdf"):
        if (CANON / c).exists():
            if c.endswith("_ms.pdf") and (CANON / f"{code}_{ses}_ms_1+2+3+4+5+6.pdf").exists():
                import pymupdf
                if len(pymupdf.open(CANON / c)) < 3:
                    continue    # a one-page stub beside the full booklet (9701_w03_ms.pdf)
            return c, comp[0]
    return None, None


def one(args) -> dict:
    sys.path.insert(0, str(HERE)); import al_space
    if not al_space.ok():        # disk guard
        return {"source": args[2], "prefix": args[3][:-3] + "-MS", "ms_source": "", "status": "HOLD",
                "result": f"disk guard: only {al_space.free_gb():.1f} GB free", "coverage": ""}
    qp_run, ms_run, src, qprefix = args
    prefix = qprefix[:-3] + "-MS"
    row = {"source": src, "prefix": prefix, "ms_source": "", "status": "HOLD", "result": "", "coverage": ""}
    ms, comp = ms_source(src)
    if not ms:
        row["result"] = "no mark scheme in canonical set"
        return row
    row["ms_source"] = ms + (f" (component {comp})" if comp else "")
    out = DATA / "splits" / ms_run / prefix
    out.mkdir(parents=True, exist_ok=True)
    for f in out.iterdir():
        f.unlink()
    qprov = DATA / "splits" / qp_run / qprefix / f"{qprefix}-split-provenance.json"
    cmd = [PY, "-I", str(HERE / "al_ms_splitter.py"), str(CANON / ms), str(qprov), str(out), prefix]
    if comp:
        cmd += ["--component", comp]
    ov = HERE.parent / "manual_specs" / "ms" / f"{prefix}.json"
    if ov.exists():
        cmd += ["--overrides", str(ov)]
    if NAME_RE.match(src).group(3)[0] == "1" and src[:4] in {"9702", "9701", "9700"}:
        cmd.append("--mcq")
    p = subprocess.run(cmd, capture_output=True, text=True)
    log = p.stdout + p.stderr
    (out / "ms_splitter.log").write_text(log)
    lines = [l for l in log.splitlines() if l.strip()]
    row["result"] = next((l for l in lines if l.startswith(("keys=", "MCQ ", "ERROR"))), (lines or ["no output"])[-1])[:400]
    g = subprocess.run([PY, "-I", str(HERE / "al_verify_ms.py"), str(CANON / ms), str(out), prefix],
                       capture_output=True, text=True)
    (out / "ms_gate.log").write_text(g.stdout + g.stderr)
    gl = next((l for l in g.stdout.splitlines() if l.startswith("pages ")), "NO OUTPUT")
    row["coverage"] = gl
    if p.returncode == 0 and "MS_OK" in lines and g.returncode == 0 and \
            re.search(r"missing=0 duplicated=0 sliced=0 overlaps=0 furniture=0", gl):
        row["status"] = "PASS"
    return row


def main() -> int:
    a = sys.argv[1:]
    qp_run, ms_run = a[0], a[1]
    workers = int(a[a.index("--workers") + 1]) if "--workers" in a else 6
    only = set(a[a.index("--only") + 1:]) if "--only" in a else None
    if only is not None and not only:
        sys.exit("--only given with no prefixes (an empty list would run the whole QP run)")
    rev = DATA / "review" / qp_run
    alias = {r["alias"] for r in csv.DictReader(open(rev / "duplicates.csv"))}
    jobs = []
    for r in csv.DictReader(open(rev / "run_summary.csv")):
        if r["status"] != "PASS" or r["prefix"] in alias:
            continue
        if only and r["prefix"] not in only and r["prefix"][:-3] + "-MS" not in only:
            continue
        jobs.append((qp_run, ms_run, r["source"], r["prefix"]))
    if only:
        hit = {j[3] for j in jobs} | {j[3][:-3] + "-MS" for j in jobs}
        if only - hit:
            sys.exit(f"--only: {len(only - hit)} prefix(es) match no PASS non-alias paper of {qp_run}: "
                     + " ".join(sorted(only - hit)[:10]))
    with ProcessPoolExecutor(workers) as ex:
        rows = list(ex.map(one, jobs))
    out = DATA / "review" / ms_run
    out.mkdir(parents=True, exist_ok=True)
    path = out / "ms_summary.csv"
    old = {}
    if only and path.exists():
        old = {r["prefix"]: r for r in csv.DictReader(open(path))}
    for r in rows:
        old[r["prefix"]] = r
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["source", "prefix", "ms_source", "status", "result", "coverage"])
        w.writeheader()
        w.writerows(sorted(old.values(), key=lambda r: r["prefix"]))
    n = sum(r["status"] == "PASS" for r in old.values())
    print(f"{n}/{len(old)} PASS -> {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
