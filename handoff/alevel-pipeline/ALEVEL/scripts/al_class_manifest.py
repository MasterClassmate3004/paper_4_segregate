#!/usr/bin/env python3
"""Build the classification manifest for a finished subject (read-only on the pipeline).

One row per approved QP crop (leaf, .stem, MCQ item) of the unique (non-alias)
approved papers, with everything a classifier needs and nothing it must guess:
  qp_id, paper, label, kind (leaf|stem|mcq|mcq_stem), source_pdf, segments
  (JSON list of [page, x0, y0, x1, y1] in PDF points, rotation removed),
  qp_png (member name), qp_zip (Google Drive path, relative to
  My Drive/ROOTATOM_ALEVEL), ms_status, ms_pdf, ms_segments, ms_png, ms_zip,
  mcq_answer.
Crops whose part has no mark scheme were removed (review/removed_no_ms.csv)
and are not listed.

Usage: al_class_manifest.py SUBJECT(chem|phy) OUT.csv
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

DATA = Path.home() / "rootatom_data" / "ALEVEL"
SETS = {   # QP runs (later wins) and MS runs per subject
    "chem": (["chem_b2", "manual"], ["chem_ms1", "chem_ms2"], "AL-CHE-", ["chem_b1", "chem_b2", "manual"]),
    "phy": (["phy_b10"], ["phy_ms4"], "AL-PHY-", ["phy_batch9"]),
}


def main() -> int:
    subj, out = sys.argv[1], sys.argv[2]
    qp_runs, ms_runs, pre, alias_runs = SETS[subj]
    H = json.load(open(DATA / "review" / "reviewed_crop_hashes.json"))
    alias = {r["alias"] for run in alias_runs for r in csv.DictReader(open(DATA / "review" / run / "duplicates.csv"))}
    led = {}
    for r in csv.DictReader(open(DATA / "review" / "offload_ledger.csv")):
        led.setdefault(r["prefix"], {})[r["run"]] = r["drive_path"]
    removed = {(r["prefix"], r["label"]) for r in csv.DictReader(open(DATA / "review" / "removed_no_ms.csv"))}
    qp_run = {}
    for run in qp_runs:
        for p in H.get(run, {}):
            if p.startswith(pre) and p not in alias:
                qp_run[p] = run
    ms_ok = {}
    for run in ms_runs:
        for r in csv.DictReader(open(DATA / "review" / run / "ms_summary.csv")):
            if r["status"] == "PASS":
                ms_ok[r["prefix"]] = run
    rows, skipped = [], []
    for p, run in sorted(qp_run.items()):
        prov_f = DATA / "splits" / run / p / f"{p}-split-provenance.json"
        if not prov_f.exists():
            skipped.append((p, "no provenance"))
            continue
        prov = json.load(open(prov_f))
        crops = H[run][p]
        zipq = led.get(p, {}).get(run) or next(iter(led.get(p, {}).values()), "")
        msp = p[:-3] + "-MS"
        mrun = ms_ok.get(msp)
        if not mrun:
            skipped.append((p, "no mark scheme"))
            continue
        mprov = json.load(open(DATA / "splits" / mrun / msp / f"{msp}-ms-provenance.json"))
        answers = mprov.get("answers", {})
        mcq = mprov.get("kind") == "mcq_key"
        for png in sorted(crops):
            lab = png[len(p) + 1:-4]
            if (p, lab) in removed:
                continue
            outs = prov.get("outputs", {}).get(lab, [])
            segs = [[s["pdf_page"]] + [round(c, 2) for c in s["clip_points"]] for s in outs]
            stem = lab.endswith(".stem") or lab.startswith("SecB")
            kind = ("mcq_stem" if stem else "mcq") if mcq else ("stem" if stem else "leaf")
            m = mprov.get("mapping", {}).get(lab, {}) if not mcq else {}
            mseg = []
            for k in m.get("ms_keys", []) or [lab]:
                for s in mprov.get("segments", {}).get(k, []):
                    mseg.append([s["pdf_page"]] + [round(c, 2) for c in s["clip_points"]])
            num = lab[1:].split(".")[0]
            rows.append({
                "qp_id": f"{p}-{lab}", "paper": p, "label": lab, "kind": kind,
                "source_pdf": Path(prov["source_pdf"]).name, "segments": json.dumps(segs),
                "qp_png": png, "qp_zip": zipq,
                "ms_status": "mcq_key" if mcq else ("" if stem else m.get("status", "")),
                "ms_pdf": Path(mprov.get("source_pdf", "")).name,
                "ms_segments": "" if (mcq or stem) else json.dumps(mseg),
                "ms_png": "" if (mcq or stem) else m.get("file", ""),
                "ms_zip": led.get(msp, {}).get(mrun, ""),
                "mcq_answer": answers.get(num, "") if (mcq and not stem) else "",
            })
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    kinds = {}
    for r in rows:
        kinds[r["kind"]] = kinds.get(r["kind"], 0) + 1
    print(f"{subj}: {len({r['paper'] for r in rows})} papers, {len(rows)} rows {kinds}; skipped {skipped}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
