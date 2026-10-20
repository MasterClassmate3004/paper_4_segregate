#!/usr/bin/env python3
"""Archive local pipeline folders/files to Google Drive as verified zips.

push [--tag DATE]
    Zip every archive unit (below) into <DRIVE>/ROOTATOM_ALEVEL/archive/<DATE>/<unit>.zip
    (images/PDFs stored, text deflated; written as .part then renamed), read each zip back
    from the Drive mount and check every member's sha256 against the local file.
verify [--tag DATE]
    Prove each zip is in the cloud: Drive's own metadata (al_cloud_verify.cloud_index) must
    list exactly one non-trashed item with that name and the same md5 + size. Writes
    review/archive_ledger.csv (tag, unit, drive_path, zip_md5, files, bytes, status).
    Exit 0 only when every unit is OK (PENDING = still uploading: run verify again later).

Units (one zip each; names are unique so Drive's metadata can be matched by title):
  splits__<run>       every file under ALEVEL/splits/<run>/  (PNGs, provenance JSON, gate logs)
  review__<dir>       every file under ALEVEL/review/<dir>/  (sheets, groups, verdicts, summaries)
  review__files       files directly in ALEVEL/review/ (approval record, ledgers, lists)
  ALEVEL__toplevel    files directly in ALEVEL/ (run logs, lists)
  classification, manual_specs (ALEVEL/manual), frozen, ref
  alevel-pipeline     a git bundle of the pipeline repo (full history) + its working tree
Nothing is deleted here: deletion is a separate, deliberate step after verify passes.

Usage: al_archive.py push|verify [--tag 2026-10-21]
"""
from __future__ import annotations

import csv
import datetime
import hashlib
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from al_cloud_verify import DRIVE, cloud_index  # noqa: E402

ROOT = Path.home() / "rootatom_data"
DATA = ROOT / "ALEVEL"
LEDGER = DATA / "review" / "archive_ledger.csv"
STORED = {".png", ".jpg", ".jpeg", ".pdf", ".zip", ".gz", ".bundle"}


def units() -> dict[str, list[tuple[str, Path]]]:
    """unit name -> [(member name, local file)]"""
    u: dict[str, list] = {}

    def tree(name, base: Path, root_for_names: Path):
        files = [f for f in sorted(base.rglob("*")) if f.is_file() and f.name != ".DS_Store" and not f.name.endswith(".part")]
        if files:
            u[name] = [(str(f.relative_to(root_for_names)), f) for f in files]

    for d in sorted((DATA / "splits").iterdir()):
        if d.is_dir():
            tree(f"splits__{d.name}", d, DATA)
    for d in sorted((DATA / "review").iterdir()):
        if d.is_dir():
            tree(f"review__{d.name}", d, DATA)
    u["review__files"] = [(str(f.relative_to(DATA)), f) for f in sorted((DATA / "review").iterdir())
                          if f.is_file() and f.name != ".DS_Store"]
    u["ALEVEL__toplevel"] = [(f.name, f) for f in sorted(DATA.iterdir()) if f.is_file() and f.name != ".DS_Store"]
    tree("classification", DATA / "classification", DATA)
    tree("manual_specs", DATA / "manual", DATA)
    tree("frozen", ROOT / "frozen", ROOT)
    tree("ref", ROOT / "ref", ROOT)
    return {k: v for k, v in u.items() if v}


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def md5_file(p: Path) -> str:
    h = hashlib.md5()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def write_zip(z: Path, members: list[tuple[str, Path]]) -> bool:
    tmp = z.with_name(f".{z.name}.part")
    local = {n: sha256_file(p) for n, p in members}
    with zipfile.ZipFile(tmp, "w") as zf:
        for n, p in members:
            zf.write(p, n, compress_type=zipfile.ZIP_STORED if p.suffix.lower() in STORED else zipfile.ZIP_DEFLATED)
    tmp.replace(z)
    with zipfile.ZipFile(z) as zf:
        back = {n: hashlib.sha256(zf.read(n)).hexdigest() for n in zf.namelist()}
    return back == local


def push(tag: str) -> int:
    dest = DRIVE / "archive" / tag
    dest.mkdir(parents=True, exist_ok=True)
    bad = 0
    all_units = units()
    with tempfile.TemporaryDirectory() as td:
        b = Path(td) / "alevel-pipeline.bundle"
        subprocess.run(["git", "-C", str(ROOT / "alevel-pipeline"), "bundle", "create", str(b), "--all"],
                       check=True, capture_output=True)
        repo = ROOT / "alevel-pipeline"
        tracked = subprocess.run(["git", "-C", str(repo), "ls-files"], check=True, capture_output=True, text=True).stdout.split()
        all_units["alevel-pipeline"] = [("alevel-pipeline.bundle", b)] + [(f"tree/{t}", repo / t) for t in tracked]
        for name, members in all_units.items():
            ok = write_zip(dest / f"{name}.zip", members)
            size = sum(p.stat().st_size for _, p in members)
            print(f"{'OK ' if ok else 'BAD'} {name}: {len(members)} files, {size / 1e6:.1f} MB", flush=True)
            bad += not ok
    return 1 if bad else 0


def verify(tag: str) -> int:
    dest = DRIVE / "archive" / tag
    idx = cloud_index()
    rows, bad = [], 0
    for z in sorted(dest.glob("*.zip")):
        ours = (md5_file(z), z.stat().st_size)
        live = [(m, s) for m, s, t in idx.get(z.name, []) if not t]
        if len(live) == 1 and live[0][0] and (live[0][0], int(live[0][1] or -1)) == ours:
            status = "OK"
        elif not live or not live[0][0]:
            status = "PENDING"
        else:
            status = f"MISMATCH cloud={live}"
        bad += status != "OK"
        with zipfile.ZipFile(z) as zf:
            n = len(zf.namelist())
        rows.append({"tag": tag, "unit": z.stem, "drive_path": f"archive/{tag}/{z.name}", "zip_md5": ours[0],
                     "files": n, "bytes": ours[1], "status": status})
        print(f"{status:8s} {z.stem}", flush=True)
    old = [r for r in csv.DictReader(open(LEDGER))] if LEDGER.exists() else []
    old = [r for r in old if r["tag"] != tag]
    with open(LEDGER, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["tag", "unit", "drive_path", "zip_md5", "files", "bytes", "status"])
        w.writeheader()
        w.writerows(old + rows)
    print(f"{len(rows) - bad}/{len(rows)} OK")
    return 1 if bad else 0


def main() -> int:
    a = sys.argv[1:]
    if not a or a[0] not in ("push", "verify"):
        print(__doc__)
        return 2
    tag = a[a.index("--tag") + 1] if "--tag" in a else datetime.date.today().isoformat()
    return push(tag) if a[0] == "push" else verify(tag)


if __name__ == "__main__":
    raise SystemExit(main())
