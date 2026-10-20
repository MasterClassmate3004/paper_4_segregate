#!/usr/bin/env python3
"""Disk guard for the A Level pipeline.

The disk has filled up twice mid-run (iCloud's CloudKit cache grows on its own),
so every batch runner calls ok() before each paper and stops cleanly when free
space falls below AL_MIN_FREE_GB (default 4).  report() prints free space and
what the pipeline itself occupies.

Usage: al_space.py            -> report, exit 3 if below the floor
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

HOME = Path.home()
DATA = HOME / "rootatom_data"
MIN_FREE_GB = float(os.environ.get("AL_MIN_FREE_GB", "4"))


def free_gb() -> float:
    return shutil.disk_usage(HOME).free / 1e9


def ok() -> bool:
    return free_gb() >= MIN_FREE_GB


def used_gb(path: Path = DATA) -> float:
    out = subprocess.run(["du", "-sk", str(path)], capture_output=True, text=True).stdout.split()
    return int(out[0]) / 1e6 if out else 0.0


def report() -> int:
    f = free_gb()
    print(f"free {f:.1f} GB (floor {MIN_FREE_GB:.0f} GB) | rootatom_data {used_gb():.2f} GB")
    return 0 if f >= MIN_FREE_GB else 3


if __name__ == "__main__":
    sys.exit(report())
