"""al_ms_regress.py -- perceptual MS regression: for every paper of NEW_RUN whose crops differ from the
approved hashes (REF_KEY), re-render it with a reference splitter (REF_PY) into a temp
dir and report crops that differ visibly (shape change or a pixel changing >= 40).
Usage: regr_cmp.py QP_RUN NEW_RUN REF_KEY REF_PY"""
import csv, glob, hashlib, json, os, shutil, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image

S = Path.home() / "rootatom_data/alevel-pipeline/ALEVEL/scripts"
sys.path.insert(0, str(S))
import al_run_ms as R

qp_run, new_run, ref_key, ref_py = sys.argv[1:5]
DATA = R.DATA
# REF_KEY: a key of reviewed_crop_hashes.json, or a JSON file {prefix: {crop: sha256}}
H = json.load(open(ref_key)) if ref_key.endswith(".json") else json.load(open(DATA / "review/reviewed_crop_hashes.json"))[ref_key]
rows = {r["prefix"]: r for r in csv.DictReader(open(DATA / "review" / new_run / "ms_summary.csv"))}
srcs = {r["prefix"][:-3] + "-MS": r["source"] for r in csv.DictReader(open(DATA / "review" / qp_run / "run_summary.csv"))}
tmp = Path(sys.argv[5] if len(sys.argv) > 5 else DATA / "review" / "_regr_ref")
real, faint = [], 0
for p, ref in H.items():
    nd = DATA / "splits" / new_run / p
    cur = {os.path.basename(f): hashlib.sha256(open(f, "rb").read()).hexdigest() for f in glob.glob(f"{nd}/*-Q*.png")}
    if cur == ref:
        continue
    if not cur and p not in rows:
        continue                     # no longer run (alias)
    if set(cur) != set(ref):
        real.append((p, "crop set differs", sorted(set(cur) ^ set(ref))))
        continue
    ms, comp = R.ms_source(srcs[p])
    q = p[:-3] + "-QP"
    shutil.rmtree(tmp, ignore_errors=True); tmp.mkdir(parents=True)
    cmd = [R.PY, "-I", ref_py, str(R.CANON / ms), str(DATA / "splits" / qp_run / q / f"{q}-split-provenance.json"), str(tmp), p]
    if comp: cmd += ["--component", comp]
    ov = S.parent / "manual_specs" / "ms" / f"{p}.json"
    if ov.exists(): cmd += ["--overrides", str(ov)]
    if R.NAME_RE.match(srcs[p]).group(3)[0] == "1" and srcs[p][:4] in {"9702", "9701", "9700"}: cmd.append("--mcq")
    subprocess.run(cmd, capture_output=True)
    for k in sorted(cur):
        if cur[k] == ref[k]:
            continue
        rf = tmp / k
        if not rf.exists() or hashlib.sha256(rf.read_bytes()).hexdigest() != ref[k]:
            real.append((p, k, "reference splitter does not reproduce the approved crop")); continue
        a = np.asarray(Image.open(rf).convert("L")).astype(int)
        b = np.asarray(Image.open(nd / k).convert("L")).astype(int)
        if a.shape != b.shape:
            real.append((p, k, f"shape {a.shape} -> {b.shape}"))
        elif np.abs(a - b).max() >= 40:
            d = np.argwhere(np.abs(a - b) >= 40)
            real.append((p, k, f"{len(d)} px rows {d[:,0].min()}-{d[:,0].max()} cols {d[:,1].min()}-{d[:,1].max()}"))
        else:
            faint += 1
shutil.rmtree(tmp, ignore_errors=True)
print(f"{ref_key}: faint-only crops {faint}; visible differences {len(real)}")
for r in real:
    print(r)
