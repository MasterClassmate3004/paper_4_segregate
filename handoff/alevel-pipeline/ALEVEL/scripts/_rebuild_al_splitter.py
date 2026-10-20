#!/usr/bin/env python3
"""Re-apply the A Level changes to a pristine copy of ib_aa_p1_splitter.py.

Recovery script (2026-10-10): the working copy of al_qp_splitter.py was
stranded in iCloud.  Each patch must match the base exactly once, otherwise
the rebuild aborts.  The result must reproduce the approved 9702/42/M/J/24
crops byte-for-byte before it is trusted.
"""
import sys
from pathlib import Path

p = Path(sys.argv[1])
s = p.read_text()


def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f"patch anchor found {n}x (expected {count}): {old[:70]!r}")
    s = s.replace(old, new)


# 1. header / Cambridge mode for AL- prefixes
rep('"""ib_aa_p1_splitter.py — Split an IB Mathematics QP into per-subpart PNGs.',
    '"""al_qp_splitter.py — Split a Cambridge A Level QP into per-subpart PNGs (fork of ib_aa_p1_splitter.py).')
rep("import fitz, json, os, re, sys", "import pymupdf as fitz, json, os, re, sys")
rep("IS_IGCSE=PREFIX.startswith('IG-MTH-')",
    """# A Level fork (2026-10-10): Cambridge AS & A Level papers share the IGCSE
# house layout (UCLES footer, margin strips, (a)/(i) columns, [n] marks), so
# the Cambridge code path is enabled for AL- prefixes too.  Source of the
# fork: IB/scripts/ib_aa_p1_splitter.py (unchanged copy in ~/rootatom_data/ref).
IS_IGCSE=PREFIX.startswith(('IG-MTH-', 'AL-'))
IS_ALEVEL=PREFIX.startswith('AL-')""")

# 2. furniture masking (append-only white-out + safety checks)
rep("def main():\n    source_doc=fitz.open(SRC)", '''BARCODE_CAPTION_RE=re.compile(r'^\\*\\s*\\d{6,}\\s*\\*$')
MARGIN_STRIP_RE=re.compile(r'DO NOT WRITE IN THIS MARGIN',re.I)
TOTAL_LINE_RE=re.compile(r'^\\[Total:\\s*\\d+\\]$')
FURNITURE={}   # page number -> furniture rects (A Level); words inside are ignored

def furniture_free(page,bbox):
    rects=FURNITURE.get(page.number)
    if not rects:
        return True
    c=fitz.Point((bbox[0]+bbox[2])/2,(bbox[1]+bbox[3])/2)
    return not any(r.contains(c) for r in rects)

def mask_alevel_furniture(doc):
    """Hide Cambridge page furniture in memory before analysis.

    2018+ A Level papers print a barcode at the top of every page as glyphs of
    a barcode font ('AllAndNone') reaching ~70 pt -- below the 58 pt header
    line inherited from IGCSE -- plus a '* 0019655342313 *' caption, rotated
    'DO NOT WRITE IN THIS MARGIN' strips and '[Total: n]' lines.

    The furniture is painted over with white (an appended drawing; existing
    content is not rewritten) and its words are ignored by analyse().  Text
    REDACTION is deliberately not used: it rewrote neighbouring text and
    shifted a whole line 3.9 pt in 9702/42/M/J/24 p.7, clipping 'with'.
    Safety checks: every word a mask touches must itself be furniture; no
    mask may partly overlap a content drawing; and every page is re-rendered
    and must be unchanged outside the masks.
    """
    for page in doc:
        rects=[]; fspans=[]
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines',[]):
                for span in line['spans']:
                    text=span['text'].strip()
                    bbox=fitz.Rect(span['bbox'])
                    is_furniture=('allandnone' in span['font'].lower()
                        or (BARCODE_CAPTION_RE.match(text) and bbox.y1<HEADER_Y+20)
                        or (MARGIN_STRIP_RE.search(text) and (bbox.x1<35 or bbox.x0>560))
                        or TOTAL_LINE_RE.match(text))
                    if is_furniture:
                        fspans.append(bbox+(-1,-1,1,1))
                    if 'allandnone' in span['font'].lower():
                        if bbox.y1<100:
                            # header barcode: bars rise well above the
                            # font's nominal bbox, up to the page top margin
                            rects.append(fitz.Rect(bbox.x0-2,18,bbox.x1+2,bbox.y1+1.5))
                        else:
                            # footer QR glyphs: mask their own box only
                            rects.append(bbox+(-1,-1,1,1))
                    elif ((BARCODE_CAPTION_RE.match(text) and bbox.y1<HEADER_Y+20)
                            or (MARGIN_STRIP_RE.search(text) and (bbox.x1<35 or bbox.x0>560))
                            or TOTAL_LINE_RE.match(text)):
                        rects.append(bbox+(-1,-1,1,1))
        if not rects:
            continue
        # Safety 1: every word a mask touches must itself be furniture.
        for w in page.get_text('words'):
            wr=fitz.Rect(w[:4])
            if any(wr.intersects(r) for r in rects):
                c=fitz.Point((w[0]+w[2])/2,(w[1]+w[3])/2)
                if not any(f.contains(c) for f in fspans):
                    raise RuntimeError(f'REVIEW_REQUIRED: furniture mask covers content word {w[4]!r} on page {page.number+1}')
        for d in page.get_drawings():
            dr=d.get('rect')
            in_furniture_zone=(dr is not None and (dr.x1<35 or dr.x0>560 or dr.y1<72 or dr.y0>790))
            if (dr is not None and dr.width>2 and dr.height>2 and not in_furniture_zone
                    and any(r.intersects(dr) and not r.contains(dr) for r in rects)):
                raise RuntimeError(f'REVIEW_REQUIRED: furniture mask overlaps a drawing {tuple(round(v) for v in dr)} on page {page.number+1}')
        before=page.get_pixmap(dpi=100,colorspace=fitz.csGRAY,alpha=False)
        for r in rects:
            page.draw_rect(r,color=None,fill=(1,1,1),overlay=True)
        FURNITURE[page.number]=rects
        after=page.get_pixmap(dpi=100,colorspace=fitz.csGRAY,alpha=False)
        a=np.frombuffer(before.samples,np.uint8).reshape(before.height,before.width)
        b=np.frombuffer(after.samples,np.uint8).reshape(after.height,after.width)
        allowed=np.zeros_like(a,dtype=bool); k=100/72
        for r in rects:
            allowed[max(0,int(r.y0*k)-2):int(r.y1*k)+3,max(0,int(r.x0*k)-2):int(r.x1*k)+3]=True
        if ((a!=b)&~allowed).any():
            raise RuntimeError(f'REVIEW_REQUIRED: furniture mask changed content on page {page.number+1}')

def main():
    source_doc=fitz.open(SRC)''')
rep("""    else:
        doc=source_doc
    if IS_IGCSE:
        # A small third-party Cambridge scan family""", """    else:
        doc=source_doc
    if IS_ALEVEL:
        mask_alevel_furniture(doc)
    if IS_IGCSE:
        # A small third-party Cambridge scan family""")

# 3. furniture words ignored by analysis
rep("""    words=[w for w in page.get_text('words')
           if HEADER_Y<=w[1]<=FOOTER_Y and w[0]<=CONTENT_R+12
           and (not IS_IGCSE or w[0]>=CONTENT_L-3)]""", """    words=[w for w in page.get_text('words')
           if HEADER_Y<=w[1]<=FOOTER_Y and w[0]<=CONTENT_R+12
           and (not IS_IGCSE or w[0]>=CONTENT_L-3)
           and furniture_free(page,w[:4])]""", count=2)
rep("""        for word in page.get_text('words'):
            token=word[4].replace(' ','')""", """        for word in page.get_text('words'):
            if not furniture_free(page,word[:4]):
                continue
            token=word[4].replace(' ','')""")
rep("""            for span in line.get('spans',[]):
                if span.get('text','').strip():
                    font_spans.append((""", """            for span in line.get('spans',[]):
                if span.get('text','').strip() and furniture_free(page,span['bbox']):
                    font_spans.append((""")

s_next = Path(sys.argv[2]).read_text()   # helper block (answer rows, continuation)
rep("""    def segment_has_content(pno,y0,y1):
        if y1-y0<6: return False
        rt,rb=INK[pno].extent(y0,y1)
        return rt is not None and rb is not None and rb-rt>=1
""", """    def segment_has_content(pno,y0,y1):
        if y1-y0<6: return False
        rt,rb=INK[pno].extent(y0,y1)
        return rt is not None and rb is not None and rb-rt>=1
""" + s_next)

# 4. continuation segments for leaf parts / romans
rep("""                emits.append((f'Q{qn}.{L}',pno,part_start,part_end))
                prev_markbot=mb or (P['y']+10); prev_pno=pno""", """                emits.append((f'Q{qn}.{L}',pno,part_start,part_end))
                emits.extend(leaf_continuation_segments(
                    f'Q{qn}.{L}',pno,P['y'],nextP or next_q_anchor))
                prev_markbot=mb or (P['y']+10); prev_pno=pno""")
rep("""                    emits.append((f'Q{qn}.{L}.{R["label"]}',R['pno'],r_start,r_final))""",
    """                    emits.append((f'Q{qn}.{L}.{R["label"]}',R['pno'],r_start,r_final))
                    emits.extend(leaf_continuation_segments(
                        f'Q{qn}.{L}.{R["label"]}',R['pno'],R['y'],nR or next_q_anchor))""")
rep("""        grp=seq[q_idx[qi]:q_idx[qi+1]]; qn=grp[0]['label']; qpno=grp[0]['pno']; qbot=grp[0]['row_y1']""",
    """        grp=seq[q_idx[qi]:q_idx[qi+1]]; qn=grp[0]['label']; qpno=grp[0]['pno']; qbot=grp[0]['row_y1']
        next_q_anchor=seq[q_idx[qi+1]] if q_idx[qi+1]<len(seq) else None""")

# 5. D6 answer-row pass
rep("""    # ---- resolve every crop box first, then enforce mutual exclusion --------""",
    """    if IS_ALEVEL:
        emits=alevel_answer_rows(emits)

    # ---- resolve every crop box first, then enforce mutual exclusion --------""")

# 6. snap final crop edges to blank pixel rows
rep("""    rendered={}; provenance={}
    for label,pno,cy0,cy1,_rt,_rb,emit_order,masks,hard_y0,hard_y1 in sorted(boxes,key=lambda b:b[6]):
        render_right=INK[pno].content_r""", Path(sys.argv[3]).read_text().rstrip("\n"))

p.write_text(s)
print("rebuilt", p, len(s.splitlines()), "lines")
