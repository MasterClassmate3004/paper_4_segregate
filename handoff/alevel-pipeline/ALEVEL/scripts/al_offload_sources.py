#!/usr/bin/env python3
"""Copy a subject's canonical source PDFs to Google Drive as one verified zip.

push SUBJECT [SUBJECT ...]
    Zip (stored, PDFs are already compressed) every source_papers/canonical/<SUBJECT>_*.pdf
    into <DRIVE>/ROOTATOM_ALEVEL/sources/<SUBJECT>_canonical.zip (written as .part, then
    renamed), read the zip back from the Drive mount and check every member's sha256
    against the local file. SUBJECT "records" bundles the provenance that belongs with the
    sources instead: canonical_original/, raw_ms_search/, _canonical_records/,
    canonical_manifest.csv, derived_sources.csv, download_ledger.csv
    -> sources/source_records.zip.  Local files are NEVER deleted (the runners read them).
verify SUBJECT [SUBJECT ...]
    Prove the zip is in the cloud: Drive's own metadata (al_cloud_verify.cloud_index) must
    list exactly one non-trashed item of that name with the same md5 and size as the local
    copy in the mount. Only then is a row added/updated in review/sources_offload_ledger.csv
    (subject, drive_path, zip_sha256, files, bytes, members_sha256, date) — the same format
    as the 2026-10-16 Physics row. Exit 0 only when every subject is OK (PENDING = still
    uploading: run verify again later).

Usage: al_offload_sources.py push|verify SUBJECT ...      (e.g. push 9701 9700 9709 records)
"""
from __future__ import annotations

import csv
import datetime
import hashlib
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from al_cloud_verify import DRIVE, cloud_index  # noqa: E402

DATA = Path.home() / "rootatom_data" / "ALEVEL"
SRC = DATA / "source_papers"
LEDGER = DATA / "review" / "sources_offload_ledger.csv"
FIELDS = ["subject", "drive_path", "zip_sha256", "files", "bytes", "members_sha256", "date"]


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def md5(p: Path) -> str:
    h = hashlib.md5()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def members(subject: str) -> dict[str, Path]:
    """zip member name -> local file."""
    if subject == "records":
        out = {}
        for d in ("canonical_original", "raw_ms_search", "_canonical_records"):
            for f in sorted((SRC / d).rglob("*")):
                if f.is_file() and f.name != ".DS_Store":
                    out[str(f.relative_to(SRC))] = f
        for name in ("canonical_manifest.csv", "derived_sources.csv", "download_ledger.csv"):
            if (SRC / name).exists():
                out[name] = SRC / name
        return out
    return {f.name: f for f in sorted((SRC / "canonical").glob(f"{subject}_*.pdf"))}


def zip_name(subject: str) -> str:
    return "source_records.zip" if subject == "records" else f"{subject}_canonical.zip"


def push(subject: str) -> bool:
    m = members(subject)
    if not m:
        print(f"{subject}: no local files — nothing to push")
        return False
    dest_dir = DRIVE / "sources"
    dest_dir.mkdir(parents=True, exist_ok=True)
    z = dest_dir / zip_name(subject)
    tmp = dest_dir / f".{z.name}.part"
    local = {n: sha256(p) for n, p in m.items()}
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_STORED) as zf:
        for n, p in m.items():
            zf.write(p, n)
    tmp.replace(z)
    with zipfile.ZipFile(z) as zf:
        back = {n: hashlib.sha256(zf.read(n)).hexdigest() for n in zf.namelist()}
    if back != local:
        bad = sorted(set(back.items()) ^ set(local.items()))[:5]
        print(f"{subject}: READ-BACK MISMATCH {bad}")
        return False
    size = sum(p.stat().st_size for p in m.values())
    print(f"{subject}: wrote {z.relative_to(DRIVE)} — {len(m)} files, {size / 1e9:.2f} GB, read-back OK "
          f"(now run: verify {subject})")
    return True


def verify(subject: str, idx: dict) -> bool:
    z = DRIVE / "sources" / zip_name(subject)
    if not z.exists():
        print(f"{subject}: MISSING {z}")
        return False
    ours = (md5(z), z.stat().st_size)
    live = [(c_md5, c_size) for c_md5, c_size, trashed in idx.get(z.name, []) if not trashed]
    if len(live) != 1 or live[0][0] is None:
        print(f"{subject}: PENDING (Drive lists {len(live)} item(s) named {z.name}{'' if live else ''}; upload not finished?)")
        return False
    if (live[0][0], int(live[0][1] or -1)) != ours:
        print(f"{subject}: MISMATCH cloud {live[0]} vs local {ours}")
        return False
    m = members(subject)
    with zipfile.ZipFile(z) as zf:
        names = set(zf.namelist())
    if names != set(m):
        print(f"{subject}: zip members differ from local files ({len(names)} vs {len(m)}) — push again")
        return False
    local = {n: sha256(p) for n, p in m.items()}
    row = {"subject": subject, "drive_path": f"sources/{z.name}", "zip_sha256": sha256(z), "files": len(m),
           "bytes": sum(p.stat().st_size for p in m.values()),
           "members_sha256": hashlib.sha256("".join(f"{k}:{v}\n" for k, v in sorted(local.items())).encode()).hexdigest(),
           "date": datetime.date.today().isoformat()}
    rows = list(csv.DictReader(open(LEDGER))) if LEDGER.exists() else []
    rows = [r for r in rows if r["subject"] != subject] + [row]
    with open(LEDGER, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    print(f"{subject}: OK — cloud md5 {ours[0]} size {ours[1]} matches; ledger updated")
    return True


def main() -> int:
    if len(sys.argv) < 3 or sys.argv[1] not in ("push", "verify"):
        print(__doc__)
        return 2
    cmd, subjects = sys.argv[1], sys.argv[2:]
    if cmd == "push":
        ok = [push(s) for s in subjects]
    else:
        idx = cloud_index()
        ok = [verify(s, idx) for s in subjects]
    return 0 if all(ok) else 1


if __name__ == "__main__":
    raise SystemExit(main())
