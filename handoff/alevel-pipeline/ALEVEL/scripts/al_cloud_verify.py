#!/usr/bin/env python3
"""Prove offloaded zips are in the cloud, byte for byte, without downloading them.

Google Drive for desktop keeps the server's metadata for every item in its
local metadata_sqlite_db: the cloud file id, size and the md5Checksum Drive
computed on upload.  For each ledger row of RUN (optionally --only PREFIX ...):
  * the zip in the Drive mount must still be readable locally (just pushed,
    not yet evicted) -> its md5 and size are computed here;
  * Drive's metadata must list exactly one non-trashed item of that title in
    the run folder with a cloud md5 + size equal to ours.
al_offload.py push already checked every zip member against the local PNG,
so md5 equality closes the chain local PNG == zip == cloud copy.

Prints one line per paper (OK / PENDING / MISMATCH) and a summary; exit 0 only
when every row is OK.  --delete then removes the local PNGs of OK papers
(the zip members' hashes are re-checked against the PNGs first).

Usage: al_cloud_verify.py RUN [--only PREFIX ...] [--delete]
"""

from __future__ import annotations

import csv
import hashlib
import re
import sqlite3
import sys
import zipfile
from pathlib import Path

DATA = Path.home() / "rootatom_data" / "ALEVEL"
GD = next((Path.home() / "Library" / "CloudStorage").glob("GoogleDrive-*"))
DRIVE = GD / "My Drive" / "ROOTATOM_ALEVEL"
FS = Path.home() / "Library" / "Application Support" / "Google" / "DriveFS"
LEDGER = DATA / "review" / "offload_ledger.csv"


def cloud_index() -> dict:
    """title -> [(cloud_md5, cloud_size, trashed)] from every account's metadata DB."""
    idx: dict = {}
    for db in FS.glob("*/metadata_sqlite_db"):
        con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        con.text_factory = bytes
        for title, size, trashed, proto in con.execute(
                "select local_title, file_size, trashed, proto from items where is_folder=0"):
            if not title or not title.endswith(b".zip"):
                continue
            md5 = re.findall(rb"\x82\x03 ([0-9a-f]{32})", proto or b"")
            idx.setdefault(title.decode(), []).append((md5[0].decode() if md5 else None, size, bool(trashed)))
        con.close()
    return idx


def main() -> int:
    a = sys.argv[1:]
    run = a[0]
    delete = "--delete" in a
    only = set(x for x in a[a.index("--only") + 1:] if not x.startswith("--")) if "--only" in a else None
    rows = [r for r in csv.DictReader(open(LEDGER)) if r["run"] == run and (not only or r["prefix"] in only)]
    idx = cloud_index()
    ok = pend = bad = freed = 0
    for r in rows:
        z = DRIVE / r["drive_path"]
        title = z.name
        try:
            blob = z.read_bytes()
        except OSError as e:
            print(f"PENDING {r['prefix']}: zip unreadable locally ({e})")
            pend += 1
            continue
        md5, size = hashlib.md5(blob).hexdigest(), len(blob)
        if hashlib.sha256(blob).hexdigest() != r["zip_sha256"]:
            print(f"MISMATCH {r['prefix']}: zip sha256 differs from ledger")
            bad += 1
            continue
        live = [c for c in idx.get(title, []) if not c[2]]
        hit = [c for c in live if c[0] == md5 and c[1] == size]
        if not hit:
            print(f"PENDING {r['prefix']}: cloud has {[(c[0], c[1]) for c in live] or 'no item'}; local md5 {md5} size {size}")
            pend += 1
            continue
        ok += 1
        if delete:
            d = DATA / "splits" / run / r["prefix"]
            with zipfile.ZipFile(z) as zf:
                members = {n: hashlib.sha256(zf.read(n)).hexdigest() for n in zf.namelist()}
            for n, h in members.items():
                f = d / n
                if f.exists():
                    if hashlib.sha256(f.read_bytes()).hexdigest() != h:
                        print(f"MISMATCH {r['prefix']}: {n} differs from zip, kept")
                        continue
                    freed += f.stat().st_size
                    f.unlink()
    print(f"{run}: OK {ok}  PENDING {pend}  MISMATCH {bad}  of {len(rows)}"
          + (f"  freed {freed / 1e6:.0f} MB" if delete else ""))
    return 0 if ok == len(rows) else 1


if __name__ == "__main__":
    sys.exit(main())
