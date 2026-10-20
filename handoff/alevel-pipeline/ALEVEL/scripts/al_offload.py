#!/usr/bin/env python3
"""Move finished A Level image sets to Google Drive and free the local disk.

push RUN [--only PREFIX ...] [--keep]
    For every paper directory splits/<RUN>/<PREFIX>/: zip its PNGs (stored, PNG
    is already compressed) into the Drive folder
    <DRIVE>/ROOTATOM_ALEVEL/splits/<RUN>/<PREFIX>.zip, read the zip back FROM
    DRIVE and check every member's sha256 against the local file, append a row
    to review/offload_ledger.csv, then delete the local PNGs (unless --keep).
    Provenance JSON, logs and answer CSVs stay local (small; they let any image
    be regenerated from the source PDF and the code).
pull RUN PREFIX ...
    Restore PNGs from Drive into splits/<RUN>/<PREFIX>/ (hash-checked against
    the ledger).

Nothing is deleted unless the read-back from the Drive mount matches.
"""

from __future__ import annotations

import csv
import datetime
import hashlib
import sys
import zipfile
from pathlib import Path

DATA = Path.home() / "rootatom_data" / "ALEVEL"
DRIVE = next((Path.home() / "Library" / "CloudStorage").glob("GoogleDrive-*")) / "My Drive" / "ROOTATOM_ALEVEL"
LEDGER = DATA / "review" / "offload_ledger.csv"
FIELDS = ["run", "prefix", "drive_path", "zip_sha256", "files", "bytes", "members_sha256", "date"]


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def ledger() -> dict:
    if not LEDGER.exists():
        return {}
    return {(r["run"], r["prefix"]): r for r in csv.DictReader(open(LEDGER))}


def push(run: str, only: set | None, keep: bool) -> int:
    src = DATA / "splits" / run
    dst = DRIVE / "splits" / run
    dst.mkdir(parents=True, exist_ok=True)
    led = ledger()
    freed = done = 0
    for d in sorted(p for p in src.iterdir() if p.is_dir()):
        if only and d.name not in only:
            continue
        pngs = sorted(d.glob("*.png"))
        if not pngs:
            continue
        local = {p.name: sha(p.read_bytes()) for p in pngs}
        z = dst / f"{d.name}.zip"
        tmp = dst / f".{d.name}.zip.part"
        with zipfile.ZipFile(tmp, "w", zipfile.ZIP_STORED) as zf:
            for p in pngs:
                zf.write(p, p.name)
        tmp.replace(z)
        # read back from the Drive mount and verify every member
        blob = z.read_bytes()
        with zipfile.ZipFile(z) as zf:
            back = {n: sha(zf.read(n)) for n in zf.namelist()}
        if back != local:
            print(f"VERIFY FAILED {d.name}: kept local copy")
            continue
        members = sha("".join(f"{k}:{v}\n" for k, v in sorted(local.items())).encode())
        led[(run, d.name)] = {"run": run, "prefix": d.name, "drive_path": str(z.relative_to(DRIVE)),
                              "zip_sha256": sha(blob), "files": len(local),
                              "bytes": sum(p.stat().st_size for p in pngs), "members_sha256": members,
                              "date": datetime.date.today().isoformat()}
        with open(LEDGER, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=FIELDS)
            w.writeheader()
            w.writerows(led.values())
        if not keep:
            for p in pngs:
                freed += p.stat().st_size
                p.unlink()
        done += 1
    print(f"{done} papers -> {dst}  freed {freed / 1e6:.0f} MB locally")
    return 0


def pull(run: str, prefixes: list[str]) -> int:
    led = ledger()
    for p in prefixes:
        r = led.get((run, p))
        if not r:
            print(f"{p}: not in ledger")
            continue
        z = DRIVE / r["drive_path"]
        if sha(z.read_bytes()) != r["zip_sha256"]:
            print(f"{p}: Drive copy hash mismatch, not restored")
            continue
        out = DATA / "splits" / run / p
        out.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(z) as zf:
            zf.extractall(out)
        print(f"{p}: {r['files']} files restored")
    return 0


def main() -> int:
    a = sys.argv[1:]
    if a[0] == "push":
        only = set(a[a.index("--only") + 1:]) if "--only" in a else None
        return push(a[1], only, "--keep" in a)
    if a[0] == "pull":
        return pull(a[1], a[2:])
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
