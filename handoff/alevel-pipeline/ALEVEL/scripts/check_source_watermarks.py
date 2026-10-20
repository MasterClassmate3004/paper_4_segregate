#!/usr/bin/env python3
"""Phase 0 watermark / provenance gate for source PDFs.

For every PDF: sha256, metadata, page count, text-layer coverage (scanned
detection), third-party URL/watermark strings, link annotations, optional
content layers, rotated/diagonal text, large overlay images, and pages with no
UCLES/Cambridge furniture (inserted advert pages).  Writes one JSON record per
file and a CSV summary.  Verdicts:

  clean               no third-party marker found
  watermark_suspect   at least one marker found -> visual review required
  scanned             little or no text layer -> OCR adapter, deferred
  unreadable          PDF failed to open

Run with the project venv (PyMuPDF):  .venv/bin/python3 -I check_source_watermarks.py PDF_DIR OUT_DIR
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import sys
from pathlib import Path

import pymupdf as fitz

ALLOWED_HOSTS = re.compile(r"cambridgeinternational\.org|cie\.org(?:\.uk)?|ucles\.org(?:\.uk)?|cambridgeassessment\.org\.uk|cambridge\.org", re.I)
URL_RE = re.compile(r"(?:https?://|www\.)[^\s)]+|\b[a-z0-9-]+\.(?:com|net|org|co\.uk|rs|cc|in|pk)\b", re.I)
MARKERS = re.compile(r"papa\s*cambridge|xtreme\s*pape|dynamic\s*papers|gce\s*guide|save\s*my\s*exams|max\s*papers|best\s*exam\s*help|"
                     r"physicsandmathstutor|znotes|downloaded\s+from|for\s+more\s+(?:papers|resources)|visit\s+us|whatsapp|telegram", re.I)
FURNITURE = re.compile(r"UCLES|Cambridge|University of Cambridge|©", re.I)
ACK_PAGE = re.compile(r"Copyright Acknowledgements|Permission to reproduce items", re.I)
LEGIT_ROTATED = re.compile(r"DO NOT WRITE IN THIS MARGIN|^\s*$|^\W+$", re.I)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def scan(path: Path) -> dict:
    rec: dict = {"file": path.name, "path": str(path), "size_bytes": path.stat().st_size, "sha256": sha256(path)}
    try:
        doc = fitz.open(path)
    except Exception as exc:
        rec.update(verdict="unreadable", error=str(exc))
        return rec
    rec["pages"] = doc.page_count
    rec["metadata"] = {k: v for k, v in (doc.metadata or {}).items() if v}
    if re.search(r"watermark", (doc.metadata or {}).get("producer", "") or "", re.I):
        pass  # recorded below as a finding
    rec["ocg_layers"] = list((doc.get_ocgs() or {}).values()) if hasattr(doc, "get_ocgs") else []
    findings: list[str] = []
    producer = (doc.metadata or {}).get("producer", "") or ""
    if re.search(r"watermark", producer, re.I):
        findings.append(f"producer '{producer.strip()}'")
    text_pages = 0
    no_furniture_pages: list[int] = []
    for pno, page in enumerate(doc):
        text = page.get_text()
        if len(text.strip()) > 80:
            text_pages += 1
        for m in MARKERS.finditer(text):
            findings.append(f"p{pno + 1}: marker '{m.group(0)}'")
        ack_page = bool(ACK_PAGE.search(text))
        for m in URL_RE.finditer(text):
            if not ALLOWED_HOSTS.search(m.group(0)) and not ack_page:
                findings.append(f"p{pno + 1}: url '{m.group(0)}'")
        if pno > 0 and text.strip() and not FURNITURE.search(text):
            no_furniture_pages.append(pno + 1)
        for link in page.get_links():
            uri = link.get("uri") or ""
            if uri and not ALLOWED_HOSTS.search(uri):
                findings.append(f"p{pno + 1}: link '{uri}'")
        content = b"".join(doc.xref_stream(x) or b"" for x in page.get_contents())
        if b"/QQAP" in content:
            findings.append(f"p{pno + 1}: A-PDF overlay stream")
        if re.search(rb"/Subtype\s*/Watermark", content):
            findings.append(f"p{pno + 1}: tagged watermark artifact")
        for annot in page.annots() or []:
            findings.append(f"p{pno + 1}: annotation {annot.type[1]}")
        # rotated / diagonal text that is not Cambridge's margin strip
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                dx, dy = line["dir"]
                ang = abs(math.degrees(math.atan2(dy, dx))) % 180
                if 5 < ang < 85 or 95 < ang < 175:
                    t = "".join(s["text"] for s in line["spans"])
                    # Rotated axis/diagram labels ("1996", "G") are real
                    # content; only flag diagonal text naming a site/marker.
                    if not LEGIT_ROTATED.search(t) and (MARKERS.search(t) or URL_RE.search(t)):
                        findings.append(f"p{pno + 1}: diagonal text '{t[:40]}' ({ang:.0f}deg)")
        # very large images covering most of a text page = possible overlay
        parea = page.rect.width * page.rect.height
        for info in page.get_image_info(xrefs=True):
            x0, y0, x1, y1 = info["bbox"]
            if (x1 - x0) * (y1 - y0) > 0.6 * parea and len(text.strip()) > 200:
                findings.append(f"p{pno + 1}: page-size image over text (xref {info.get('xref')})")
    rec["text_pages"] = text_pages
    rec["pages_without_ucles"] = no_furniture_pages
    rec["findings"] = sorted(set(findings))
    if text_pages < max(1, doc.page_count // 2):
        rec["verdict"] = "scanned"
    elif rec["findings"] or rec["ocg_layers"]:
        rec["verdict"] = "watermark_suspect"
    else:
        rec["verdict"] = "clean"
    return rec


def main() -> int:
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    recs = [scan(p) for p in sorted(src.rglob("*.pdf"))]
    with open(out / "watermark_scan.json", "w") as fh:
        json.dump(recs, fh, indent=1)
    with open(out / "watermark_scan.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["file", "verdict", "pages", "text_pages", "pages_without_ucles", "n_findings", "first_findings", "producer", "sha256"])
        for r in recs:
            w.writerow([r["path"], r["verdict"], r.get("pages"), r.get("text_pages"), r.get("pages_without_ucles"),
                        len(r.get("findings", [])), " | ".join(r.get("findings", [])[:3]),
                        r.get("metadata", {}).get("producer", ""), r["sha256"]])
    for r in recs:
        print(f"{r['verdict']:18} {Path(r['path']).parent.name}/{r['file']}  pages={r.get('pages')} "
              f"noUCLES={r.get('pages_without_ucles')} {r.get('findings', [])[:3]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
