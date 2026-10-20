#!/usr/bin/env python3
"""Remove third-party watermarks layered onto Cambridge source PDFs.

Watermark kinds found on archive copies (2026-10-09 samples):

1. "A-PDF Watermark" overlays (PapaCambridge / StudentBounty ribbons and
   banners): wrapper content of the form
   ``q /GSx gs q <cm> <cm> /QQAPxxxx Do Q Q`` plus link annotations.
2. Acrobat tagged watermarks (XtremePapers diagonal text):
   ``/Artifact <</Subtype /Watermark ...>> BDC ... EMC``.
3. Acrobat tagged header stamps (Dynamic Papers):
   ``/Artifact <</Contents (www.dynamicpapers.com)/Subtype /Header ...>> BDC ... EMC``.
   Header/footer artifacts are removed ONLY when their dictionary names a
   third-party site, so Cambridge's own artifacts are never touched.

Removal is exact: the page's content streams are concatenated (identical PDF
semantics), the watermark blocks are cut out (marked-content nesting is
honoured), and every other operator stays byte-for-byte unchanged.  Foreign
link annotations are deleted.

Verification per page (mandatory): render before / after / watermark-only at
100 dpi.  Every changed pixel must lie in the removed watermark's footprint:
(dilated) ink of the watermark-only render plus the full box of each removed
overlay image (opaque banners hide original content such as the UCLES
footer).  Otherwise the file is rejected (exit 2).  Afterwards
check_source_watermarks.py must report ``clean``.

Usage: ~/.venvs/alevel/bin/python -I strip_overlay_watermarks.py IN.pdf OUT.pdf
"""

from __future__ import annotations

import json
import re
import sys

import numpy as np
import pymupdf as fitz

QQAP_RE = re.compile(rb"q\s+/\w+\s+gs\s+q\s+(?:[-\d.]+\s+){6}cm\s+(?:[-\d.]+\s+){6}cm\s+/QQAP\w+\s+Do\s+Q\s+Q")
ARTIFACT_OPEN = re.compile(rb"/Artifact\s*<<(.*?)>>\s*BDC", re.S)
MC_TOKEN = re.compile(rb"\bBDC\b|\bBMC\b|\bEMC\b")
THIRD_PARTY = re.compile(rb"dynamic\s*papers|papa\s*cambridge|xtreme\s*pape|student\s*bounty|gce\s*guide|max\s*papers|"
                         rb"save\s*my\s*exams|best\s*exam\s*help", re.I)
ALLOWED_LINK = re.compile(r"cambridgeinternational\.org|cie\.org\.uk", re.I)
DPI = 100
STRIP_ANNOTS = {"Stamp", "FreeText", "Watermark", "Text", "Square", "Circle", "Ink", "Highlight", "Underline", "StrikeOut"}


def watermark_artifacts(content: bytes) -> list[tuple[int, int]]:
    """Spans of /Artifact marked-content blocks that are third-party watermarks."""
    spans = []
    for m in ARTIFACT_OPEN.finditer(content):
        props = m.group(1)
        if not (re.search(rb"/Subtype\s*/Watermark", props) or THIRD_PARTY.search(props)):
            continue
        depth = 1
        for tok in MC_TOKEN.finditer(content, m.end()):
            depth += -1 if tok.group(0) == b"EMC" else 1
            if depth == 0:
                spans.append((m.start(), tok.end()))
                break
    spans.sort()
    out: list[tuple[int, int]] = []
    for s in spans:  # drop spans nested inside an earlier one
        if not out or s[0] >= out[-1][1]:
            out.append(s)
    return out


def gray(page: fitz.Page) -> np.ndarray:
    pm = page.get_pixmap(dpi=DPI, colorspace=fitz.csGRAY, alpha=False)
    return np.frombuffer(pm.samples, dtype=np.uint8).reshape(pm.height, pm.width)


def dilate(mask: np.ndarray, r: int = 2) -> np.ndarray:
    out = mask.copy()
    h, w = mask.shape
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            src = mask[max(0, -dy):h - max(0, dy), max(0, -dx):w - max(0, dx)]
            out[max(0, dy):h - max(0, -dy), max(0, dx):w - max(0, -dx)] |= src
    return out


def set_content(doc: fitz.Document, page: fitz.Page, data: bytes) -> None:
    xrefs = page.get_contents()
    doc.update_stream(xrefs[0], data)
    for x in xrefs[1:]:
        doc.update_stream(x, b" ")


def strip(src: str, dst: str) -> dict:
    doc = fitz.open(src)
    ref = fitz.open(src)   # untouched, for "before" renders
    wm = fitz.open(src)    # watermark-only renders
    rep = {"file": src, "pages": doc.page_count, "qqap_removed": 0, "artifact_removed": 0,
           "links_removed": 0, "pages_changed": 0, "violations": []}
    after: dict[int, np.ndarray] = {}
    for pno, page in enumerate(doc):
        content = b"\n".join(doc.xref_stream(x) or b"" for x in page.get_contents())
        spans = watermark_artifacts(content)
        removed = [content[a:b] for a, b in spans]
        keep, last = [], 0
        for a, b in spans:
            keep.append(content[last:a])
            last = b
        keep.append(content[last:])
        new = b" ".join(keep)
        qq = QQAP_RE.findall(new)
        removed += qq
        new = QQAP_RE.sub(b" ", new)
        for link in page.get_links():
            if link.get("uri") and not ALLOWED_LINK.search(link["uri"]):
                page.delete_link(link)
                rep["links_removed"] += 1
        # Archive-added annotations (e.g. a "Second variant Mark Scheme"
        # stamp).  Cambridge question papers/mark schemes carry none of these.
        annot_boxes = []
        for annot in list(page.annots() or []):
            if annot.type[1] in STRIP_ANNOTS:
                annot_boxes.append(fitz.Rect(annot.rect) * page.rotation_matrix)
                page.delete_annot(annot)
                rep["annots_removed"] = rep.get("annots_removed", 0) + 1
        if not removed and not annot_boxes:
            continue
        if removed:
            set_content(doc, page, new)
            set_content(wm, wm[pno], b"q\n" + b"\n".join(removed) + b"\nQ")
        else:
            set_content(wm, wm[pno], b" ")
        rep["qqap_removed"] += len(qq)
        rep["artifact_removed"] += len(spans)
        rep["pages_changed"] += 1

        a, b, c = gray(ref[pno]), gray(page), gray(wm[pno])
        after[pno] = b
        if a.shape != b.shape:
            rep["violations"].append({"page": pno + 1, "error": "render size changed"})
            continue
        foot = c < 255
        k = DPI / 72
        for r in annot_boxes:
            x0, y0, x1, y1 = (int(v * k) for v in r)
            foot[max(0, y0 - 2):max(0, y1 + 3), max(0, x0 - 2):max(0, x1 + 3)] = True
        for info in wm[pno].get_image_info():
            x0, y0, x1, y1 = (int(v * k) for v in info["bbox"])
            foot[max(0, y0):max(0, y1 + 1), max(0, x0):max(0, x1 + 1)] = True
        bad = int(((a != b) & ~dilate(foot)).sum())
        if bad:
            rep["violations"].append({"page": pno + 1, "pixels_changed_outside_watermark": bad})
    # Acrobat puts header/footer and watermark stamps on their own optional
    # content layer.  Once the stamps are gone, drop the layer definition, but
    # only when every layer is of that kind and switched on (so removing
    # /OCProperties cannot change what is visible).  Re-verified below.
    ocgs = doc.get_ocgs() or {}
    if rep["pages_changed"] and ocgs and all(o["name"] in {"Headers/Footers", "Watermark", "Background"} and o["on"] for o in ocgs.values()):
        doc.xref_set_key(doc.pdf_catalog(), "OCProperties", "null")
        rep["ocg_layers_removed"] = [o["name"] for o in ocgs.values()]
    if rep["pages_changed"] or rep["links_removed"]:
        meta = dict(doc.metadata or {})
        meta["producer"] = "rootatom overlay-strip v2 (third-party overlays removed)"
        doc.set_metadata({k: v for k, v in meta.items()
                          if k in {"title", "author", "subject", "keywords", "creator", "producer", "creationDate", "modDate"}})
    doc.save(dst, garbage=3, deflate=True, encryption=fitz.PDF_ENCRYPT_NONE)
    # The saved file must render exactly like the verified in-memory result.
    saved = fitz.open(dst)
    for pno, b in after.items():
        if not np.array_equal(gray(saved[pno]), b):
            rep["violations"].append({"page": pno + 1, "error": "saved render differs from verified render"})
    return rep


def main() -> int:
    rep = strip(sys.argv[1], sys.argv[2])
    print(json.dumps(rep))
    return 2 if rep["violations"] else 0


if __name__ == "__main__":
    sys.exit(main())
