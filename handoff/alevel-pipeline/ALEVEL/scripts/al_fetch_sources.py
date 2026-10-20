#!/usr/bin/env python3
"""Rebuild one subject's canonical sources from the Phase 0 originals.

The Phase 0 canonical/ set sits in an iCloud folder that is evicted and whose
downloads stall, so instead: for every in-scope file of SUBJECT that is not
yet in ~/rootatom_data/ALEVEL/source_papers/canonical, re-fetch the SAME
original (URL + raw sha256 from the Phase 0 download ledger, approved
2026-10-09), require the raw sha256 to match, run the same overlay stripper
(its own per-page pixel verification) and watermark rescan, and require the
Phase 0 page count.  The stripper's saved bytes are not deterministic (two
runs on one raw file differ in sha256 yet render pixel- and text-identical to
the Phase 0 canonical, checked on 9701_m16_ms_12), so the new file's own
sha256 is recorded.  Accepted rows are appended to the local
canonical_manifest.csv (other subjects' rows untouched); the raw download is
deleted.  Anything else is reported and left out.

Usage: al_fetch_sources.py SUBJECT [--workers 6] [--exclude _s26_,_m26_] [--read-errors F1,F2] [--recheck-held]

--read-errors: files Phase 0 downloaded but could not open (iCloud read error,
so never classified); they get the same sha256/strip/rescan checks, and only
a non-zero page count (Phase 0 has none to compare).
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import os
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import al_space  # noqa: E402
import check_source_watermarks as scanner  # noqa: E402
import strip_overlay_watermarks as stripper  # noqa: E402

SRC = Path.home() / "rootatom_data" / "ALEVEL" / "source_papers"
LEDGER = HERE.parent / "source_papers_phase0_ledger.csv"
OLDMAN = HERE.parent / "source_papers_phase0_manifest.csv"
UA = "Mozilla/5.0 (rootatom source download)"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def one(led: dict, man: dict) -> tuple[str, str]:
    f = led["filename"]
    if not al_space.ok():
        return f, f"HOLD disk guard ({al_space.free_gb():.1f} GB free)"
    with tempfile.TemporaryDirectory(dir=SRC) as td:
        raw = Path(td) / f
        rc = subprocess.run(["curl", "-sL", "-A", UA, "--max-time", "1800", "--speed-limit", "1024",
                             "--speed-time", "90", "--retry", "3", "-o", str(raw), led["url"]],
                            capture_output=True).returncode
        if rc or not raw.exists():
            return f, f"FAIL curl rc={rc}"
        if sha(raw) != led["sha256"]:
            return f, "FAIL raw sha256 differs from Phase 0 ledger"
        out = Path(td) / ("c_" + f)
        rep = stripper.strip(str(raw), str(out))
        if rep["violations"]:
            return f, f"FAIL strip verification {rep['violations'][:2]}"
        if not (rep["pages_changed"] or rep["links_removed"]):
            out = raw
        rec = scanner.scan(out)
        if rec["verdict"] not in ("clean", "scanned"):
            return f, f"FAIL rescan {rec['verdict']}"
        if man["action"] == "error":    # Phase 0 never opened it (iCloud read error): no page count
            if not rep["pages"]:
                return f, "FAIL no pages"
        elif str(rep["pages"]) != str(man["pages"]):
            return f, f"FAIL pages {rep['pages']} != Phase 0 {man['pages']}"
        dst = SRC / "canonical" / f
        os.replace(out, dst)
    return f, f"OK:{rec['sha256']}:{rep['pages']}:{rec['verdict']}:{'stripped' if out != raw else 'copied'}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("subject")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--exclude", default="_s26_,_m26_")
    ap.add_argument("--recheck-held", action="store_true",
                    help="also fetch Dynamic Papers files Phase 0 held as 'rescan watermark_suspect'; "
                         "accepted only if the current scanner passes them")
    ap.add_argument("--read-errors", default="",
                    help="comma list of files Phase 0 could not open (iCloud read error) to fetch as well")
    a = ap.parse_args()
    excl = [x for x in a.exclude.split(",") if x]
    rerr = {x for x in a.read_errors.split(",") if x}
    man = {r["filename"]: r for r in csv.DictReader(open(OLDMAN))}
    newman = SRC / "canonical_manifest.csv"
    fields = next(csv.reader(open(newman)))
    have = {r["filename"] for r in csv.DictReader(open(newman))}
    led = [r for r in csv.DictReader(open(LEDGER))
           if r["subject_code"] == a.subject and r["status"] in ("downloaded", "present")
           and not any(x in r["filename"] for x in excl)
           and (man.get(r["filename"], {}).get("canonical_path")          # Phase 0 accepted it
                or (r["filename"] in rerr and man.get(r["filename"], {}).get("action") == "error"
                    and "Failed to open file" in man[r["filename"]].get("hold_reason", ""))
                # Phase 0 rescan holds (rotated diagram labels read as diagonal watermarks,
                # since fixed in the scanner); the rescan in one() decides again
                or (a.recheck_held and r["source"] == "dp" and not man.get(r["filename"], {}).get("canonical_path")
                    and man.get(r["filename"], {}).get("hold_reason", "").startswith("rescan")))]
    todo = [r for r in led if r["filename"] not in have]
    print(f"{a.subject}: {len(led)} canonical in Phase 0, {len(todo)} to fetch", flush=True)
    bad = 0
    with ThreadPoolExecutor(a.workers) as pool:
        futs = [pool.submit(one, r, man[r["filename"]]) for r in todo]
        for i, fu in enumerate(as_completed(futs), 1):
            f, st = fu.result()
            if st.startswith("OK:"):
                row = {k: man[f].get(k, "") for k in fields}
                h, pages, verdict, action = st[3:].split(":")
                row["canonical_sha256"] = h
                if man[f]["action"] == "error" or not man[f].get("canonical_path"):   # read error / held: record this fetch
                    row.update(action=action, pages=pages, verdict=verdict, hold_reason="",
                               canonical_path=f"canonical/{f}")
                with open(newman, "a", newline="") as fh:
                    csv.DictWriter(fh, fieldnames=fields).writerow(row)
            else:
                bad += 1
                print(f, st, flush=True)
            if i % 50 == 0:
                print(f"{i}/{len(todo)} (problems {bad})", flush=True)
    print(f"done: {len(todo) - bad} fetched, {bad} problems", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
