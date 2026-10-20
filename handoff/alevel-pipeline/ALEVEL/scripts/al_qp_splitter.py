#!/usr/bin/env python3
"""al_qp_splitter.py — Split a Cambridge A Level QP into per-subpart PNGs (fork of ib_aa_p1_splitter.py).

Naming:  {PREFIX}-Q<n>[.<a>][.<i>][.stem].png   e.g. IB-MAAHL-M22-P1-QP-Q10.c.stem.png

Model (ROOT19 convention):
  Q<n>            single-task question (no parts)
  Q<n>.stem       intro before part (a)  — question number + [Maximum mark] hidden
  Q<n>.<a>        part text only (up to its [mark] + any real diagram) — no answer boxes
  Q<n>.<a>.stem   shared context (mid-question stem) preceding part <a>
  Q<n>.<a>.<i>    roman sub-part; inline "(c) (i)" handled; no empty stems

Techniques:
  * marker anchors (Q number / (a) / (i) / [n]) give the logical structure
  * a rendered ink-projection places cuts in whitespace and sizes crops to true
    ink extent (tall fractions/radicals contained; watermarks render too light
    to count as ink)
  * stops: dotted answer lines, answer-box rects (rect containing dotted lines),
    footer barcode images, "Do not write ..." rows
  * post-render border-trim: a full-width horizontal line at the crop's bottom
    edge with nothing below it (an answer-box top border) is trimmed — unless
    vertical borders run above it (it closes a rectangle, e.g. a sketch box)

Usage: python ib_aa_p1_splitter.py <src.pdf> <outdir> <prefix>
"""
import pymupdf as fitz, json, os, re, sys, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from barcode_rule import is_barcode_span
import fused_marks; fused_marks.install(leaders=len(sys.argv) > 3 and sys.argv[3].startswith(('AL-MTH-','AL-FMT-')))
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw

SRC    = sys.argv[1] if len(sys.argv) > 1 else '/Users/nitya/Documents/Nitya/Projects/rootatom/paper_4_segregate/IB/scripts/_test_AAHL_P1_M22.pdf'
OUTDIR = Path(sys.argv[2] if len(sys.argv) > 2 else '/Users/nitya/Documents/Nitya/Projects/rootatom/paper_4_segregate/IB/scripts/_out')
PREFIX = sys.argv[3] if len(sys.argv) > 3 else 'IB-MAAHL-M22-P1-QP'
OUTDIR.mkdir(parents=True, exist_ok=True)

# A Level fork (2026-10-10): Cambridge AS & A Level papers share the IGCSE
# house layout (UCLES footer, margin strips, (a)/(i) columns, [n] marks), so
# the Cambridge code path is enabled for AL- prefixes too.  Source of the
# fork: IB/scripts/ib_aa_p1_splitter.py (unchanged copy in ~/rootatom_data/ref).
IS_IGCSE=PREFIX.startswith(('IG-MTH-', 'AL-'))
IS_ALEVEL=PREFIX.startswith('AL-')
# A Level Mathematics / Further Mathematics (9709/9231): uncaptioned diagrams printed above
# 'The diagram shows ...', short symbolic context lines ('The function h is defined by ...')
IS_MATHS=PREFIX.startswith(('AL-MTH-','AL-FMT-'))
DPI=220; HEADER_Y=58; FOOTER_Y=790 if IS_IGCSE else 802; CONTENT_L=float(__import__('os').environ.get('IB_CONTENT_L',40)); CONTENT_R=float(__import__('os').environ.get('IB_CONTENT_R',560))
CONTENT_BOTTOM=782 if IS_IGCSE else 774  # stay above Cambridge/IB footer furniture
if IS_ALEVEL:
    # A Level: measure the footer instead of using the IGCSE 790/782 pt
    # constants -- older papers print answer lines down to ~794 pt
    # (9702/04/O/N/08 p.8 'w = ...... rad s-1 [2]'), which the constants cut.
    def _alevel_footer_top(path):
        tops=[]
        for page in list(fitz.open(path))[1:]:          # skip the cover
            ys=[w[1] for w in page.get_text('words') if w[1]>740 and
                re.search(r'UCLES|©|^\d{4}/\d{1,2}/|^\[?Turn$|^over$',w[4])]
            # (2025+ corner crop-marks and QR glyphs above the footer text are
            #  masked as furniture, so only the footer TEXT bounds content)
            if ys:
                tops.append(min(ys))
        if not tops:
            return 782.0
        tops.sort()
        median=tops[len(tops)//2]          # robust to one odd page
        # footer word bbox tops already include ascenders; 1 pt clearance
        # keeps answer rows that end ~795 pt (9702/42/M/J/10 p.4 'mass = .. kg')
        return max(776.0,min(798.0,median-1))
    FOOTER_Y=CONTENT_BOTTOM=_alevel_footer_top(SRC)
PAD_PT=6; RDPI=150; SC=RDPI/72.0; BIGGAP_PX=13
PART_X_MAX=88 if IS_IGCSE else 96
# A continuation-page roman can be outdented a few points (86.97 pt in
# 0580_w15_qp_41) while remaining clearly to the right of the 70 pt parent
# column.  Sequence validation below rejects variable-like false positives.
ROMAN_X_MIN=int(os.environ.get('IB_ROMAN_X_MIN', 84 if IS_IGCSE else 96))

Q_RE=(re.compile(r'^(\d{1,2})\.?$') if IS_IGCSE else
      re.compile(r'^(\d{1,2})\.$'))
PAR_RE=re.compile(r'^\(([a-z]{1,4})\)$')
MARK_RE=re.compile(r'^\[(\d+)\]$'); ROMANS={'i','ii','iii','iv','v','vi','vii','viii','ix','x'}
STOP_RE=re.compile(r'(Do not write|Please do not write|This question continues|Please turn over|Turn over for (?:Question|Section)|Question \d+ continue[sd]|^Diagram$|^References|Baccalaureate Organization|Answers will not|blank page'
                   # 2001-2005 layout: the answer area is a pair of boxes
                   # introduced by "Working:" / "Answer:" labels instead of
                   # dotted leader lines. Colon required so the instruction
                   # sentence "Working may be continued below the box" (which
                   # appears above question 1) is not mistaken for a stop.
                   r'|\bWorking:|\bAnswer:)', re.I)
CREDIT_START_RE=re.compile(
    r'^\[?\s*(?:Source|Sources|Image source|Photo(?:graph)?(?: credit)?|Copyright)\s*:',
    re.I,
)
CREDIT_CONT_RE=re.compile(
    r'^(?:Licensed under|Licence(?:d)? under|Image adapted|Adapted from|©)\b',
    re.I,
)


def credit_rectangles(page):
    """Bounds of non-question image/source attribution furniture.

    Official papers sometimes place a bracketed source URL and licence over
    two or three compact rows immediately below an illustration.  Those rows
    are not mathematical context and the QA contract excludes copyright
    furniture, but the illustration itself must remain untouched.
    """
    words=[w for w in page.get_text('words')
           if HEADER_Y<=w[1]<=FOOTER_Y and w[0]<=CONTENT_R+12
           and (not IS_IGCSE or w[0]>=CONTENT_L-3)
           and furniture_free(page,w[:4])]
    rows={}
    for w in words: rows.setdefault(round(w[1]/3)*3,[]).append(w)
    rects=[]; active=False; prior_bottom=None
    for _key,ws in sorted(rows.items()):
        ordered=sorted(ws,key=lambda w:w[0])
        text=' '.join(w[4] for w in ordered).strip()
        top=min(w[1] for w in ordered); bottom=max(w[3] for w in ordered)
        start=bool(CREDIT_START_RE.match(text))
        continuation=(active and prior_bottom is not None and top-prior_bottom<12)
        standalone=bool(CREDIT_CONT_RE.match(text))
        if start or continuation or standalone:
            rects.append(fitz.Rect(
                max(CONTENT_L-2,min(w[0] for w in ordered)-2),top-1,
                min(CONTENT_R+2,max(w[2] for w in ordered)+2),bottom+1,
            ))
            if start:
                active=('[' in text and ']' not in text)
            elif continuation:
                active=(']' not in text)
            else:
                active=False
            prior_bottom=bottom
        else:
            active=False; prior_bottom=None
    return rects

def standalone_separator_rects(page):
    """Full-width question separators, excluding tables and examiner rules."""
    drawings=page.get_drawings()
    vrules=[d['rect'] for d in drawings
            if d.get('rect') and d['rect'].height>8 and d['rect'].width<3]
    separators=[]
    for drawing in drawings:
        rect=drawing.get('rect')
        if not rect or rect.y1<HEADER_Y or rect.y0>FOOTER_Y:
            continue
        if rect.width>(CONTENT_R-CONTENT_L)*0.85 and rect.height<3:
            nearby=[v for v in vrules
                    if v.y0-35<=rect.y0<=v.y1+35
                    and not (IS_IGCSE and v.x0>525 and v.height>120)]
            if not nearby:
                separators.append(rect)
    return separators

class Ink:
    """Per-page horizontal ink projection over the content column (rendered)."""
    def __init__(self, page):
        pm=page.get_pixmap(dpi=RDPI, colorspace=fitz.csGRAY)
        arr=(np.frombuffer(pm.samples,dtype=np.uint8)
             .reshape(pm.height,pm.stride)[:,:pm.width].copy())
        self.content_r=CONTENT_R
        if IS_IGCSE:
            # Older Cambridge sheets reserve a right-hand examiner column
            # behind one page-height vertical rule.  That line is rendered
            # page furniture, not question ink, and otherwise makes a fully
            # white left-to-right separator mathematically impossible on
            # every row.  Keep it in the final rendered crop, but exclude it
            # from separator/extent geometry.
            examiner_rules=[d['rect'] for d in page.get_drawings()
                            if d.get('rect') and d['rect'].x0>525
                            and d['rect'].width<3 and d['rect'].height>120]
            if IS_ALEVEL:
                # the examiner column rule runs (nearly) the full page height;
                # shorter verticals here are graph-grid lines (9702/41/M/J/11)
                examiner_rules=[r for r in examiner_rules if r.height>500]
            if IS_ALEVEL and not re.search(r"Examiner", page.get_text()):
                # A Level papers without a 'For Examiner's Use' column: these
                # verticals are figure/graph borders (cut at x=523 before)
                examiner_rules=[]
            if examiner_rules:
                self.content_r=min(self.content_r,
                                   min(r.x0 for r in examiner_rules)-2)
        xa,xb=int(CONTENT_L*SC),int(self.content_r*SC)
        # Standalone question separators and repeated answer leaders are page
        # furniture.  They remain visible in the final source rendering, but
        # must not behave like mathematical glyphs when proving a crop cut.
        for rect in standalone_separator_rects(page):
            ya=max(0,int((rect.y0-1)*SC)); yb=min(pm.height,int((rect.y1+1)*SC)+1)
            arr[ya:yb,xa:xb]=255
        for word in page.get_text('words'):
            if not furniture_free(page,word[:4]):
                continue
            token=word[4].replace(' ','')
            if len(token)<=6:
                continue
            repeated=sum(token.count(ch) for ch in '.·…_')
            if repeated/len(token)<=0.6:
                continue
            wx0=max(xa,int(word[0]*SC)-1); wx1=min(xb,int(word[2]*SC)+2)
            wy0=max(0,int((word[1]-1)*SC)); wy1=min(pm.height,int((word[3]+1)*SC)+1)
            arr[wy0:wy1,wx0:wx1]=255
        self.gray=arr[:,xa:xb]
        # `dark` deliberately ignores pale watermarks for ordinary crop
        # extent detection.  `semantic` is stricter about visible glyph
        # antialiasing and is used only by ownership seams, where leaving even
        # a small cap of a neighbouring bracket is unacceptable.
        self.dark=self.gray<190
        self.semantic=self.gray<230
        self.ink=self.dark.sum(axis=1).astype(int)
        self.H=pm.height; self.W=self.dark.shape[1]
    def _r(self,y): return max(0,min(self.H-1,int(y*SC)))
    def _p(self,r): return r/SC
    def extent(self,y0,y1,thr=1):
        a,b=self._r(y0),self._r(y1); rows=np.where(self.ink[a:b+1]>=thr)[0]
        if len(rows)==0: return None,None
        return self._p(a+rows[0]), self._p(a+rows[-1])
    def content_top(self,y,floor,thr=1):
        r=self._r(y); f=self._r(floor); top=r; gap=0; i=r
        while i>f:
            if self.ink[i]>=thr: top=i; gap=0
            else:
                gap+=1
                if gap>=BIGGAP_PX: break
            i-=1
        return self._p(top)

def leader_run(tok):
    """Longest dot run in a token, counting '…' as three dots (2007 papers
    set leaders as ellipsis characters: '………………………' = 24 dots)."""
    return max((len(m)+2*m.count('…') for m in re.findall(r'[.…]+',tok)),default=0)


def is_leader(w,words=None):
    """An answer leader: >=10 dots AND (>=50 pt wide OR after an '=' label on
    the same line).  Short unlabelled dotted blanks are slots INSIDE printed
    prompt text -- equation blanks ('...... He', 9702/21/O/N/25) and nuclide
    numbers ('............ Fr', 9702/02/O/N/02); 'density = ..... ± .....
    g cm-3' (9702/21/M/J/09) has two short labelled leaders."""
    if not (re.match(r'^[.…]{3,}',w[4]) and leader_run(w[4])>=10):
        return False
    if (w[2]-w[0])>=50:
        return True
    # the '=' must label THIS leader: only dots / '±' may sit between them.  A
    # worked example 'δ = 1.2' further left on a structure diagram's row made
    # the diagram's fill-in blanks answer rows (9701/42/M/J/19 Q5(c)(iii))
    if words is None:
        return False
    # a short slot alone on its row (apart from a mark) is an answer line too:
    # '................  [1]' (9701/21/O/N/13 Q2(a))
    # (body column only: nuclide slots '......' above/below 'Fr' stay with
    # their symbol, 9702/02/O/N/02 Q8(a))
    row=[u for u in words if abs(u[1]-w[1])<4 and u is not w]
    if w[0]<140 and all(re.fullmatch(r'\[\d+\]|[.…]+',u[4]) for u in row):
        return True
    for v in words:
        if v[4].endswith('=') and abs(v[1]-w[1])<4 and v[2]<=w[0]+1:
            between=[u for u in words if abs(u[1]-w[1])<4 and u[0]>=v[2]-0.5 and u[2]<=w[0]+1 and u is not v]
            if all(re.fullmatch(r'[.…]+|±',u[4]) for u in between):
                return True
    return False


def table_cells(page):
    """Geometry used to recognise dotted leaders INSIDE a drawn table.

    Returns (boxes, vlines): framed rectangles and vertical rules.  The
    full-height examiner-column rule is excluded so that it never acts as a
    table's right-hand border.
    """
    # genuine rectangle items only: a compound path of separate rules (table
    # + examiner column + mark boxes, 9702/05/O/N/07 p.6) has a page-sized
    # bounding rect that is not a box
    # (a page-sized frame -- 2006 Paper 5 pages are boxed -- is not a table)
    boxes=[fitz.Rect(it[1]) for d in page.get_drawings() for it in d.get('items',[])
           if it[0]=='re' and it[1].width>60 and 30<it[1].height<500]
    vlines=[]
    for d in page.get_drawings():
        for it in d.get('items',[]):
            if it[0]=='l' and abs(it[1].x-it[2].x)<1.5 and abs(it[1].y-it[2].y)>12:
                vlines.append(fitz.Rect(min(it[1].x,it[2].x),min(it[1].y,it[2].y),
                                        max(it[1].x,it[2].x)+0.1,max(it[1].y,it[2].y)))
            elif it[0]=='re' and it[1].width<2 and it[1].height>12:
                vlines.append(fitz.Rect(it[1]))
    vlines=[v for v in vlines if v.height<500]
    return boxes,vlines


def dot_in_table(dw,geom):
    boxes,vlines=geom
    if any(r.y0-1<=dw[1] and dw[3]<=r.y1+1 and r.x0-1<=dw[0] and dw[2]<=r.x1+1 for r in boxes):
        return True
    cy=(dw[1]+dw[3])/2
    return (any(v.x0<=dw[0] and v.y0<=cy<=v.y1 for v in vlines) and
            any(v.x0>=dw[2] and v.y0<=cy<=v.y1 for v in vlines))


def analyse(page):
    """Anchors (Q/PART/ROMAN), [mark] rows, stop rows, words for one page."""
    TABLE_GEOM=table_cells(page) if IS_ALEVEL else ([],[])
    words=[w for w in page.get_text('words')
           if HEADER_Y<=w[1]<=FOOTER_Y and w[0]<=CONTENT_R+12
           and (not IS_IGCSE or w[0]>=CONTENT_L-3)
           and furniture_free(page,w[:4])]
    font_spans=[]
    for block in page.get_text('dict').get('blocks',[]):
        for line in block.get('lines',[]):
            for span in line.get('spans',[]):
                if span.get('text','').strip() and furniture_free(page,span['bbox']):
                    font_spans.append((
                        fitz.Rect(span['bbox']),span['text'],span.get('font'),
                        span.get('size'),span.get('flags'),
                    ))
    def word_style(word):
        centre=fitz.Point((word[0]+word[2])/2,(word[1]+word[3])/2)
        matches=[(rect.width*rect.height,font,size,flags)
                 for rect,text,font,size,flags in font_spans
                 if rect.contains(centre) and word[4] in text]
        if not matches:
            return None,None,None
        _area,font,size,flags=min(matches,key=lambda item:item[0])
        return font,size,flags
    credits=credit_rectangles(page)
    if credits:
        words=[w for w in words if not any(
            rect.x0-1<=((w[0]+w[2])/2)<=rect.x1+1 and
            rect.y0-1<=((w[1]+w[3])/2)<=rect.y1+1
            for rect in credits
        )]
    rowmap={}
    for w in words: rowmap.setdefault(round(w[1]/3)*3,[]).append(w)
    # A references page may contain numbered citations in the exact left
    # gutter used by question anchors (for example "2. Bermuda Triangle
    # map").  Once the official References heading begins, no later token on
    # that page can be question content.  Enforce that as a structural page
    # boundary instead of merely treating the heading row as a crop stop.
    reference_rows=[]
    for ws in rowmap.values():
        ordered=sorted(ws,key=lambda w:w[0])
        text=' '.join(w[4] for w in ordered)
        if ordered and ordered[0][0]<90 and re.match(r'^References\s*:',text,re.I):
            reference_rows.append(min(w[1] for w in ordered))
    reference_cut=min(reference_rows) if reference_rows else None
    if reference_cut is not None:
        words=[w for w in words if w[1]<reference_cut-1]
        rowmap={}
        for w in words: rowmap.setdefault(round(w[1]/3)*3,[]).append(w)
    anchors=[]; marks=[]; stops=([reference_cut] if reference_cut is not None else []); dot_rows=[]
    row_records=[]
    for w in words:
        if MARK_RE.match(w[4]): marks.append((w[1],w[3]))
    for _,ws in rowmap.items():
        ws.sort(key=lambda w:w[0]); text=' '.join(t[4] for t in ws)
        compact=text.replace(' ',''); dot=sum(compact.count(c) for c in '.·…')
        row_w=(max(w[2] for w in ws)-min(w[0] for w in ws)) if ws else 0
        first_token=ws[0][4] if ws else ''
        row_y0=min(w[1] for w in ws); row_y1=max(w[3] for w in ws)
        row_x0=ws[0][0]
        # A labelled subpart can be almost entirely mathematical notation and
        # a fill-in leader: `(a) P = { ........ }`, `(i) 26 .... B`, etc.
        # The leading structural marker is sufficient proof that this is a
        # prompt row, even when it contains no multi-letter prose.  Treating
        # it as response furniture silently drops the leaf itself.
        semantic_prompt_row=bool(Q_RE.match(first_token) or
                                 PAR_RE.match(first_token))
        # dot-leader detection: some PDFs map the leader glyph to an unmapped
        # Unicode codepoint (renders as U+FFFD / private-use chars) instead of
        # '.', so also flag any row that is one character repeated >60% of its
        # length AND spans most of the content width (a real answer line).
        if not (len(compact)>6 and dot/len(compact)>0.6) and len(compact)>20 and row_w>300:
            from collections import Counter
            top_ch,top_n=Counter(compact).most_common(1)[0]
            if top_n/len(compact)>0.6: dot=top_n
        # A long left-hand label (e.g. `Largest positive first electron
        # affinity:`) can dilute the whole-row dot ratio below 0.6 even
        # though the row's tail is still an unambiguous dotted answer
        # leader spanning most of the content width -- a shorter label on
        # the row above (`Largest first ionization energy:`) passes the
        # ratio test while this one does not, purely because of label
        # length.  Detect that trailing leader directly: a contiguous run
        # of literal-dot glyphs at the row's right-hand end that alone
        # spans a wide swath of the content width is response furniture
        # regardless of what precedes it on the same row.
        trailing_dot_run_w=0
        for tok in reversed(ws):
            if not (len(tok[4])==1 and tok[4] in '.·…'): break
            trailing_dot_run_w=max(w[2] for w in ws)-tok[0]
        has_trailing_leader=(trailing_dot_run_w>150 and not semantic_prompt_row)
        is_dot_row=((len(compact)>6 and dot/len(compact)>0.6) or
                     has_trailing_leader) and not semantic_prompt_row
        if is_dot_row and IS_ALEVEL and not any(is_leader(t,ws) for t in ws):
            is_dot_row=False                # inline equation blanks, not an answer leader
        if is_dot_row and IS_ALEVEL:
            # dotted cells of a table the candidate completes are not an
            # answer area: cutting there slices the table (9702/21/M/J/10
            # Fig. 1.1, 9702/41/M/J/15 Fig. 3.2)
            leaders=[t for t in ws if re.match(r'^[.…]{3,}',t[4])]
            if leaders and all(dot_in_table(t,TABLE_GEOM) for t in leaders):
                is_dot_row=False
        row_records.append((row_y0,row_y1,text.strip(),row_x0,is_dot_row,
                            semantic_prompt_row))
        if is_dot_row:
            y0=min(w[1] for w in ws); stops.append(y0); dot_rows.append(y0); continue
        if STOP_RE.search(text): stops.append(min(w[1] for w in ws)); continue
        left=ws[0]; tok,x0=left[4],left[0]
        if Q_RE.match(tok) and x0<72:
            # Does this row carry question text besides the number and an
            # optional "[Maximum mark: N]"? In 2008+ papers the number sits
            # alone on its own line, so the crop can simply start below it.
            # In 2001-2007 papers there is no [Maximum mark] line and the
            # question's first line of text shares the row with the number --
            # starting below the row would decapitate the question, so those
            # get cropped from the row TOP with the number whited out instead
            # (the convention permits either).
            # Fixed 3-point row bins can put the question number and its
            # same-baseline prompt on opposite sides of a rounding edge
            # (e.g. y=451.48 vs 451.69).  Use actual baseline proximity for
            # inline ownership or an entire one-line question becomes an
            # empty crop after the number row is skipped.
            visual_row=[left]+[t for t in words
                               if t is not left and t[0]>=left[2]-1 and
                               abs(t[1]-left[1])<3]
            rest=[t for t in visual_row[1:]
                  if not MARK_RE.match(t[4]) and not PAR_RE.match(t[4])]
            resttxt=' '.join(t[4] for t in rest)
            inline = bool(re.search(r'[A-Za-z]', resttxt)) and 'Maximum mark' not in resttxt
            inline_lexical_count=sum(
                bool(re.search(r'[A-Za-z]{2,}',t[4])) for t in rest
            )
            font,font_size,font_flags=word_style(left)
            anchors.append({'kind':'Q','label':Q_RE.match(tok).group(1),'y':left[1],
                            'row_y1':max(w[3] for w in visual_row),'x':x0,
                            'font':font,'font_size':font_size,
                            'font_flags':font_flags,'inline':inline,
                            'inline_lexical_count':inline_lexical_count,
                            'nbox':(left[0],left[1],left[2],left[3])})
        else:
            m=PAR_RE.match(tok); ry1=max(w[3] for w in ws)
            # Older A Level papers number fourth-level tasks under a roman:
            # '(i) On Fig. 7.1,  1. draw ... [1]  2. draw ... [1]'
            # (9702/42/M/J/13 Q7(b)(i); 9702/22/M/J/19 Q2(b)(ii) 1.-4.).  Each
            # is separately marked -> a leaf.  Column x~118 pt; the run is
            # validated in drop_false_igcse_subparts (>=2 items from 1, under
            # an open roman).
            nm=re.match(r'^(\d)\.$',tok) if IS_ALEVEL else None
            # an answer slot is '1. ..........' with a real leader; a lone '.'
            # after a stacked fraction ends the task (9702/42/F/M/16 Q1(c)(i) 2.)
            slot=(all(re.fullmatch(r'[.\u2026]+',t[4]) for t in ws[1:])
                  and sum(leader_run(t[4]) for t in ws[1:])>=10) if len(ws)>1 else False
            if nm and 108<=x0<135 and not slot:      # '1. ......' alone = answer slot
                anchors.append({'kind':'SUBPART','label':nm.group(1),
                                'y':left[1],'row_y1':ry1,'x':x0})
            elif (m and IS_IGCSE and m.group(1) in ROMANS and x0>=65 and
                  not (IS_ALEVEL and any(abs(v[1]-left[1])<3 and v[2]<=x0 and v[0]>=CONTENT_L
                                         for v in words if v is not left))):
                # The 2008 extended paper and one 2010 continuation page
                # outdent roman markers all the way to the ordinary part
                # column.  Roman sequence validation below distinguishes
                # them from parenthesised variables such as (x) and (v).
                anchors.append({'kind':'ROMAN','label':m.group(1),
                                'y':left[1],'row_y1':ry1,'x':x0})
            elif m and x0<PART_X_MAX and len(m.group(1))==1 and not (m.group(1) in ROMANS and x0>=ROMAN_X_MIN): anchors.append({'kind':'PART','label':m.group(1),'y':left[1],'row_y1':ry1,'x':x0})
            elif (IS_IGCSE and m and len(m.group(1))==1 and
                  m.group(1) not in ROMANS and
                  PART_X_MAX<=x0<190):
                anchors.append({'kind':'SUBPART','label':m.group(1),
                                'y':left[1],'row_y1':ry1,'x':x0})
            elif m and ROMAN_X_MIN<=x0<160:
                # A Level: a '(i)' raised 1 pt above its line lands in its own
                # 3-pt row bucket; words to its LEFT on the same visual line
                # make it a cross-reference ('in (i) may', 9702/42/M/J/19)
                if IS_ALEVEL and any(abs(v[1]-left[1])<3 and v[2]<=x0 and v[0]>=CONTENT_L
                                     for v in words if v is not left):
                    pass
                else:
                    anchors.append({'kind':'ROMAN','label':m.group(1),'y':left[1],'row_y1':ry1,'x':x0})
        lead_is_q = bool(Q_RE.match(tok)) and x0<72
        for ti,t in enumerate(ws[1:],1):
            if IS_ALEVEL and re.match(r'^\d\.$',t[4]) and 108<=t[0]<135 and \
                    not (all(re.fullmatch(r'[.\u2026]+',v[4]) for v in ws if v[0]>t[0]) and
                         sum(leader_run(v[4]) for v in ws if v[0]>t[0])>=10) and \
                    any(PAR_RE.match(v[4]) and v[4][1:-1] in ROMANS for v in ws if v[0]<t[0]):
                # '(iii) 1. ...' -- first numbered task inline with its roman
                # (9702/22/M/J/11 Q6(a)(iii))
                anchors.append({'kind':'SUBPART','label':t[4][0],'y':t[1],
                                'row_y1':max(w[3] for w in ws),'x':t[0]})
                continue
            mm=PAR_RE.match(t[4])
            if not mm: continue
            if mm.group(1) in ROMANS and ROMAN_X_MIN<=t[0]<170:
                # A Level: only '(a) (i) ...' / '3 (i) ...' -- the roman must
                # directly follow a part marker or the question number; a
                # mid-sentence '(i)' is a cross-reference ('calculated in (i)
                # may be', 9702/42/M/J/19 Q12(c)(ii))
                prev=ws[ti-1][4]
                if IS_ALEVEL and not (PAR_RE.match(prev) or Q_RE.match(prev)):
                    continue
                anchors.append({'kind':'ROMAN','label':mm.group(1),'y':t[1],'row_y1':max(w[3] for w in ws),'x':t[0]})
            elif (IS_MATHS and len(mm.group(1))==1 and t[0]<190 and
                  PAR_RE.match(ws[ti-1][4]) and ws[ti-1][4][1:-1] in ROMANS):
                # '(ii) (a) Find ... [4]' -- first letter task inline with its
                # roman (9709/72/F/M/16 Q6(ii)); kept only if separately marked
                anchors.append({'kind':'SUBPART','label':mm.group(1),'y':t[1],
                                'row_y1':max(w[3] for w in ws),'x':t[0]})
            elif lead_is_q and len(mm.group(1))==1 and t[0]<PART_X_MAX:
                # "16.  (a) Sketch the graph ..." -- number and first part share
                # one row. The row's leading token is the question number, so
                # the part-detection branch above never sees the "(a)"; without
                # this, part (a) is not an anchor at all and its text is
                # silently swallowed into the question stem.
                anchors.append({'kind':'PART','label':mm.group(1),'y':t[1],'row_y1':max(w[3] for w in ws),'x':t[0]})
            elif (IS_IGCSE and not IS_ALEVEL and len(mm.group(1))==1 and
                  PART_X_MAX<=t[0]<190):
                # (A Level: a mid-row '(b)' is a cross-reference -- 'Use data
                # from (b) to determine' hid the 1./2. tasks of 9702/43/O/N/15
                # Q4(c)(i))
                anchors.append({'kind':'SUBPART','label':mm.group(1),
                                'y':t[1],'row_y1':max(w[3] for w in ws),'x':t[0]})
    # A multi-field labelled answer box (e.g. Chemistry's `Protons: / Neutrons:
    # / Electrons:` or `One similarity: <blank line(s)> / One difference:
    # <blank line(s)>`) sometimes puts the label on its OWN row with no dots
    # at all, and the actual dotted leader(s) on a separate row directly
    # below.  Such a label-only row passes none of the compact-dot-ratio or
    # STOP_RE tests above, so it survives as if it were ordinary prose and
    # `midstem_start` mistakes it for the first word of a new shared stem --
    # silently detaching the label (and everything after it, up to the real
    # next sibling) from the part that owns it.  A short, colon-terminated,
    # left/body-column row immediately followed by a genuine dotted row is
    # the same response furniture as an inline `Label: ....` row; treat it
    # identically.  Gated purely on this structural pattern (never on
    # subject/prefix), so it only fires where the pattern actually occurs.
    row_records.sort(key=lambda r:r[0])
    for idx,(ry0,ry1,rtext,rx0,ris_dot,rsemantic) in enumerate(row_records):
        if ris_dot or rsemantic: continue
        if not rtext.endswith(':'): continue
        if len(rtext)>30 or len(rtext.split())>4: continue
        if rx0>200: continue
        nxt=row_records[idx+1] if idx+1<len(row_records) else None
        if nxt and nxt[4] and (nxt[0]-ry1)<12:
            stops.append(ry0); dot_rows.append(ry0)
    # answer boxes = big rects that TIGHTLY wrap dotted answer lines -> stop at top.
    # sketch grids / diagram frames have no dotted lines inside -> keep.
    # Guard against large square watermark artwork (e.g. a logo bounding box)
    # that coincidentally spans/overlaps real dotted lines lower on the page:
    # require a non-square aspect ratio AND that the rect's top sits close to
    # the first dotted line it contains (a real border hugs the box; a
    # watermark shape does not).
    dotted=list(dot_rows)
    for d in page.get_drawings():
        r=d['rect']
        if r.y1<HEADER_Y or r.y0>FOOTER_Y: continue
        if r.width>340 and r.height>55 and abs(r.width-r.height)>20:
            contained=[dl for dl in dotted if r.y0-4<=dl<=r.y1+4]
            if contained and (min(contained)-r.y0)<20:
                stops.append(r.y0)
    # Standalone full-width horizontal rule = a section/end-of-question
    # separator -> stop. A table's rules are the same width, so width can't
    # tell them apart; what distinguishes a table is that it also has VERTICAL
    # rules alongside. Requiring zero nearby verticals keeps table borders
    # intact (bar #7) while still stopping at real separators.
    for rect in standalone_separator_rects(page):
        stops.append(rect.y0)
    for img in page.get_images(full=True):          # footer barcode etc.
        try:
            for rr in page.get_image_rects(img[0]):
                if rr.y0>700 and rr.width>40: stops.append(rr.y0)
        except Exception: pass
    # Order by ROW, then by marker rank, then left-to-right -- not by raw y.
    # On a row like "3.  (a) Express ..." the two tokens have slightly
    # different baselines (the "(a)" can sit a fraction of a point higher), so
    # a plain y-sort can place the part BEFORE its own question number, which
    # hands it to the previous question and leaves this one with no part (a).
    RANK={'Q':0,'PART':1,'ROMAN':2,'SUBPART':3}
    # Fixed rounding bins still split markers only ~1 pt apart when they land
    # on opposite sides of a bin edge (notably N22 Q8 '(b) (i)'). Cluster by
    # actual y-distance first, then apply semantic rank within the cluster.
    clusters=[]
    for a in sorted(anchors,key=lambda a:a['y']):
        if not clusters or a['y']-min(x['y'] for x in clusters[-1])>3.0:
            clusters.append([a])
        else:
            clusters[-1].append(a)
    ordered=[]
    for cluster in clusters:
        ordered.extend(sorted(cluster,key=lambda a:(RANK.get(a['kind'],9),a.get('x',0),a['y'])))
    seen=set(); uniq=[]
    for a in ordered:
        k=(a['kind'],a['label'],round(a['y']))
        if k in seen: continue
        seen.add(k); uniq.append(a)
    return uniq, sorted(marks), sorted(stops), words, dotted

ROMAN_ORDER=['i','ii','iii','iv','v','vi','vii','viii','ix','x']
def drop_false_romans(seq):
    """Reject roman anchors that don't continue a real (i),(ii),(iii) run.

    '(x)' and '(v)' are legitimate roman numerals but also appear constantly
    in maths as a parenthesised variable -- 'f (x)', 'g (x)', '(v)' for
    velocity. A genuine roman list always starts at (i) and advances by one,
    so we keep a roman only if it is 'i' (starting a new run) or is the exact
    successor of the previous roman still open under the same part. Anything
    else is a variable that happens to look like a numeral.
    """
    out=[]; expect=0; last_part=None
    for a in seq:
        if a['kind']=='Q':
            last_part=None
        if a['kind'] in ('Q','PART'):
            if a['kind']=='PART': last_part=a['label']
            expect=0; out.append(a); continue
        if a['kind']!='ROMAN': out.append(a); continue
        lab=a['label']
        # part '(i)' after part '(h)' (and (v)/(x) after (u)/(w)) in the PART
        # column is a letter, not a roman: 9701/52/M/J/24 Q1(i) became Q1(h)(i)
        if (IS_ALEVEL and len(lab)==1 and last_part and ord(lab)==ord(last_part)+1
                and a.get('x',99)<84):
            b=dict(a); b['kind']='PART'; last_part=lab; expect=0; out.append(b); continue
        lab=a['label']
        if lab==ROMAN_ORDER[expect] if expect<len(ROMAN_ORDER) else False:
            expect+=1; out.append(a)
        elif lab=='i':
            expect=1; out.append(a)
        # else: silently drop -- it's a variable, not a subpart marker
    return out

def drop_false_igcse_subparts(seq,marks=None):
    """Keep only real fourth-level Cambridge alphabetic runs.

    A standalone parenthesised variable such as the `(h)` in a frequency
    table occupies the same body column as a nested `(a)` marker.  A genuine
    fourth-level list is always scoped by a roman parent and begins `(a)`,
    followed by at least `(b)`.  Validate that complete run before allowing
    it to alter the hierarchy.
    """
    if not IS_IGCSE:
        return seq
    out=[]; pending=[]; roman_open=False
    def flush():
        nonlocal pending
        labels=[a['label'] for a in pending]
        valid=(roman_open and len(labels)>=2 and (
                   (labels[0]=='a' and labels==[chr(ord('a')+i) for i in range(len(labels))]) or
                   labels==[str(i+1) for i in range(len(labels))]))
        if valid and IS_ALEVEL and marks is not None and labels[0]=='1':
            # numbered tasks are separate leaves only if each is separately
            # marked: a [n] between every task and the next.  '1. ... 2. ...
            # one figure ... [3]' (9702/23/O/N/19 Q4(b)(ii)) is ONE leaf.
            def mark_between(a,b):
                for pno in range(a['pno'],b['pno']+1):
                    lo=a['y']-3 if pno==a['pno'] else 0   # a task's own '[2]' shares its row
                    hi=b['y'] if pno==b['pno'] else 10**6
                    if any(lo<m[0]<hi for m in marks.get(pno,[])):
                        return True
                return False
            valid=all(mark_between(pending[i],pending[i+1]) for i in range(len(pending)-1))
        if valid:
            out.extend(pending)
        pending=[]
    for anchor in seq:
        if anchor['kind']=='SUBPART':
            pending.append(anchor)
            continue
        if (anchor['kind']=='PART' and roman_open and
                [item['label'] for item in pending]==['a'] and
                anchor.get('pno',0)>pending[-1].get('pno',0) and
                anchor['y']<110 and anchor['label']=='b'):
            # At the top of a continuation page Cambridge occasionally
            # outdents a fourth-level `(b)` to the ordinary part column.  The
            # preceding page still supplies an unambiguous nested `(a)` under
            # the open roman item.  Preserve that a,b sequence as fourth-level
            # children instead of emitting a duplicate outer part as a leaf.
            pending.append({**anchor,'kind':'SUBPART'})
            continue
        if anchor['kind'] in ('Q','PART','ROMAN'):
            flush()
            roman_open=anchor['kind']=='ROMAN'
        out.append(anchor)
    flush()
    return out

def drop_false_igcse_parts(seq):
    """Keep only the contiguous outer-part sequence within each question.

    Parenthesised maths variables can sit in the same left column as a part
    marker.  A real Cambridge outer-part list always begins `(a)` and advances
    without gaps; an isolated `(d)` in the prose for a single-task question
    is therefore content, not hierarchy.
    """
    if not IS_IGCSE:
        return seq
    out=[]; expected=None
    for anchor in seq:
        if anchor['kind']=='Q':
            expected='a'; out.append(anchor); continue
        if anchor['kind']!='PART':
            out.append(anchor); continue
        if expected is not None and anchor['label']==expected:
            out.append(anchor)
            expected=chr(ord(expected)+1)
        # Every other parenthesised letter is mathematical content or a
        # malformed hierarchy, and must not manufacture a split.
    return out

def drop_false_igcse_questions(seq):
    """Keep only the official consecutive question-number gutter sequence.

    A bare integer at the start of a wrapped sentence or beside a graph axis
    has the same extracted token shape as a Cambridge question number.  Real
    question numbers, however, form the single 1, 2, 3, ... sequence and stay
    in one fixed left gutter throughout a paper.  Enforce both invariants so
    values such as the `15` inside Q12 or the `9` inside Q21 cannot open fake
    questions.  A missing Q1 is a source/parser error and must fail closed.
    """
    if not IS_IGCSE:
        return seq
    first=next((a for a in seq
                if a['kind']=='Q' and int(a['label'])==1),None)
    if first is None:
        raise RuntimeError('REVIEW_REQUIRED: no Q1 anchor found in IGCSE paper')
    gutter=float(first['x']); question_size=first.get('font_size')
    question_flags=first.get('font_flags'); expected=1; out=[]
    for anchor_index,a in enumerate(seq):
        if a['kind']!='Q':
            out.append(a)
            continue
        label=int(a['label'])
        # Embedded PDF font *names* are not stable typography identifiers.
        # Some official Cambridge papers change subset name on the final
        # question page (e.g. TT105... -> TT107...) although the printed
        # number has the identical size and style.  Compare those visual
        # properties instead; together with exact consecutive numbering and
        # the fixed gutter this still rejects graph-axis and prose integers.
        candidate_size=a.get('font_size')
        same_size=(question_size is None or candidate_size is None or
                   # One official 2016 paper prints Q5 at 12 pt while every
                   # other question number is 11 pt.  This is a harmless
                   # source-typesetting anomaly, not a hierarchy boundary.
                   abs(float(candidate_size)-float(question_size))<=1.25)
        # compare the visible style bits only (bold 16, italic 2): the serif
        # bit (4) is font-metadata noise -- 9702/22/M/J/16 sets Q2 in
        # Arial-BoldMT (flags 16) and Q1/Q3 in Helvetica-Bold (flags 20)
        same_flags=(question_flags is None or a.get('font_flags') is None or
                    (int(a.get('font_flags'))&18)==(int(question_flags)&18))
        same_style=same_size and same_flags
        # A graph-axis tick can accidentally be the next expected integer and
        # even share the official number font.  When the real question number
        # appears later with the same label, prefer the duplicate that sits
        # closest to the established Q1 gutter.  This rejects the false Q10
        # beside the 2011 s41 graph without weakening consecutive numbering.
        if label==expected:
            current_gutter_error=abs(float(a['x'])-gutter)
            better_duplicate=next((candidate for candidate in
                                   seq[anchor_index+1:]
                                   if (candidate['kind']=='Q' and
                                       int(candidate['label'])==label and
                                       not a.get('inline') and
                                       candidate.get('inline') and
                                       candidate.get('inline_lexical_count',0)>=2 and
                                       abs(float(candidate['x'])-gutter)+0.5 <
                                       current_gutter_error)),None)
            if better_duplicate is not None:
                continue
        # Some legacy `qp_2.pdf` files concatenate complete variants 21 and
        # 22.  The runner intentionally maps that source to the established
        # 21 identifier.  Once a same-gutter, same-font Q1 restarts after the
        # first sequence, the remaining anchors belong to the second paper;
        # stopping here prevents its a/b/i/ii markers being attached to the
        # final question of variant 21.
        if label==1 and expected>1 and abs(float(a['x'])-gutter)<=8:
            following_questions=[candidate for candidate in seq[anchor_index:]
                                 if candidate['kind']=='Q'][:3]
            restarted=[int(candidate['label'])
                       for candidate in following_questions]
            same_new_gutter=all(abs(float(candidate['x'])-float(a['x']))<=8
                                for candidate in following_questions)
            if restarted==[1,2,3] and same_new_gutter:
                break
        # A Level: 4 pt -- a leading space inside the number's span moves the
        # word box 3.05 pt right (9702/21/O/N/21 Q3 ' 3 ')
        if label==expected and abs(float(a['x'])-gutter)<=(4 if IS_ALEVEL else 3) and same_style:
            out.append(a); expected+=1
        # Every other isolated integer is page content, not a Q anchor.
    return out

_ORPHAN_LABEL_RE=re.compile(r'^\(?[a-zA-Z]\)?$|^\(?[ivxlcdmIVXLCDM]{1,4}\)?$')

def trim_trailing_orphan_label(image,gutter_frac=0.16,ink_thresh=235):
    """Post-render safety net: if the image's bottommost band of ink is a
    short blob confined to the left gutter (an orphaned part/roman label,
    e.g. the "(d)" left of "(d)  (i) ..." when a two-dimensional seam mask
    hides its paired roman but a curved seam path leaves the label itself
    partially unmasked) with real content clearly above it, crop it away.

    Operates on the FINAL rendered pixels (after seam masks are applied),
    not on PDF geometry: two siblings from an inline label/first-roman
    transition can share the same [cy0,cy1) render window with different
    masks, so a fix at the PDF-coordinate level cannot safely tell which
    of the two crops the leftover ink belongs to. Checking what actually
    survived onto the page sidesteps that ambiguity entirely.

    Geometry alone (short + left-aligned) is not sufficient: a genuinely
    short trailing SENTENCE (e.g. "is given.") is geometrically identical
    to an orphaned "(d)" label. OCR the candidate band and only trim when
    its text actually matches a bare part/roman label, so real short
    prose is never removed.
    """
    arr=np.asarray(image.convert('L'))
    h,w=arr.shape
    dark=arr<ink_thresh
    row_has_ink=dark.any(axis=1)
    ink_rows=np.where(row_has_ink)[0]
    if len(ink_rows)==0:
        return image
    last=int(ink_rows[-1])
    i=last
    while i>0 and row_has_ink[i-1]:
        i-=1
    band_top=i
    if band_top<4:
        return image  # this band starts at the top: nothing above it
    band_cols=np.where(dark[band_top:last+1].any(axis=0))[0]
    if len(band_cols)==0:
        return image
    if int(band_cols[-1])>w*gutter_frac:
        return image  # spans wide: real content, not a bare label
    if not dark[:band_top].any():
        return image  # nothing real above: this band IS the content
    try:
        import pytesseract
        pad=max(0,band_top-4)
        band_img=image.crop((0,pad,image.width,min(h,last+5)))
        # A tightly-cropped, unpadded single short token (e.g. "(d)" alone)
        # is frequently misread as empty by tesseract's default page
        # segmentation; upscale and force single-text-line mode.
        band_img=band_img.resize((band_img.width*2,band_img.height*3))
        text=pytesseract.image_to_string(band_img,config='--psm 7').strip()
    except Exception:
        return image  # can't verify content: never guess a destructive trim
    if not _ORPHAN_LABEL_RE.match(text.replace(' ','')):
        return image  # real short prose, e.g. "is given." -- keep it
    return image.crop((0,0,image.width,band_top))

def trim_bottom_border(pix, page=None, cy0=None, known_stops=None):
    """Remove an answer-box top border (full-width line at bottom edge, white
    below, no closing verticals above). Returns a PIL-free cropped pixmap array."""
    arr=np.frombuffer(pix.samples,dtype=np.uint8).reshape(pix.height,pix.stride)
    ch=pix.n
    W=pix.width; H=pix.height
    gray=arr[:, :W*ch].reshape(H,W,ch)[:,:,:min(3,ch)].mean(axis=2)
    dark=gray<120
    rowfrac=dark.sum(axis=1)/W
    cut=None
    # Maths: answer-box borders span the whole body width; a diagram's ground
    # line under a toppling solid (0.6 of the width, 9709/51/O/N/11 Q4) is content
    full=0.85 if IS_MATHS else 0.5
    for i in range(H-1, max(0,H-46), -1):
        if rowfrac[i]>full:
            below=rowfrac[i+3:]
            if below.size==0 or below.max()<0.02:
                # Closing rectangle? Look for ANY continuous vertical rule in
                # the band just above the line -- a table's or grid's side and
                # column rules are rarely at the crop's extreme edges (the
                # table is inset from the margin), so checking only the far
                # left/right columns misses them and the box loses its bottom
                # border, violating bar #7. An answer-box top border has no
                # verticals above it at all.
                band=dark[max(0,i-22):i+1, :]
                if band.size:
                    # A genuine closing rectangle has a vertical rule that is
                    # CONNECTED to this horizontal row. A nearby mark token
                    # such as "[6]" can also have a tall dark stroke, but it
                    # stops above the rule and must not make an answer-box top
                    # look like a closing rectangle.
                    colfrac=band.mean(axis=0)
                    connected=dark[max(0,i-7):i+1, :].mean(axis=0)
                    if not np.any((colfrac>0.8) & (connected>0.75)):
                        cut=i
            break
    if cut is None: return None
    # Don't trim a real diagram axis: if a short label (a bare variable like
    # "p", "x", "t") sits on the source page right at this row's height, this
    # full-width line is an axis with an arrowhead, not a stray answer-box
    # border -- an answer-box border never has an adjacent 1-3 char label.
    if page is not None and cy0 is not None:
        # `pix` is rendered at DPI, not RDPI -- convert with the pixmap's own
        # scale or the label lookup lands far from the line it belongs to.
        page_y = cy0 + cut*72.0/DPI
        # Some IB answer rectangles are exposed by PyMuPDF as separate line
        # segments rather than one enclosing rect, so analyse() may record the
        # first dotted row but not the box's top itself. A dotted stop shortly
        # BELOW this line is equally strong evidence that it is answer-area
        # furniture, not a labelled graph axis.
        known_answer_border=any(page_y-5<=s<=page_y+22 for s in (known_stops or []))
        if not known_answer_border:
            for w in page.get_text('words'):
                tok=w[4].strip()
                if abs(w[1]-page_y)<18 and len(tok)<=3 and re.search(r'[A-Za-zͰ-Ͽ]',tok) \
                   and not (PAR_RE.match(tok) or Q_RE.match(tok) or MARK_RE.match(tok)):
                    return None
    # new bottom = last inky row above the border + pad
    sub=rowfrac[:max(1,cut-2)]
    inkrows=np.where(sub>0.002)[0]
    newH=(inkrows[-1]+18) if len(inkrows) else cut-3
    newH=min(newH, cut-3)
    return max(20,int(newH))

BARCODE_CAPTION_RE=re.compile(r'^\*\s*\d{6,}\s*\*$')
MARGIN_STRIP_RE=re.compile(r'DO NOT WRITE IN THIS MARGIN',re.I)
TOTAL_LINE_RE=re.compile(r'^\[Total\s*:\s*\d+\]$')    # '[Total : 8]' in 2002-03 papers
FURNITURE={}   # page number -> furniture rects (A Level); words inside are ignored

def furniture_free(page,bbox):
    rects=FURNITURE.get(page.number)
    if not rects:
        return True
    c=fitz.Point((bbox[0]+bbox[2])/2,(bbox[1]+bbox[3])/2)
    return not any(r.contains(c) for r in rects)

def foreign_ink(page,r):
    """True if rendered ink inside r lies outside every character box there."""
    k=4.0
    pm=page.get_pixmap(matrix=fitz.Matrix(k,k),clip=r,colorspace=fitz.csGRAY,alpha=False)
    a=(np.frombuffer(pm.samples,np.uint8).reshape(pm.height,pm.stride)[:,:pm.width]<235)
    raw=page.get_text('rawdict',clip=r+(-1,-1,1,1))
    for b in raw.get('blocks',[]):
        for l in b.get('lines',[]):
            for sp in l.get('spans',[]):
                for ch in sp.get('chars',[]):
                    cb=fitz.Rect(ch['bbox'])+(-0.6,-0.6,0.6,0.6)
                    x0=max(0,int((cb.x0-r.x0)*k)); x1=min(a.shape[1],int((cb.x1-r.x0)*k)+1)
                    y0=max(0,int((cb.y0-r.y0)*k)); y1=min(a.shape[0],int((cb.y1-r.y0)*k)+1)
                    if x1>x0 and y1>y0: a[y0:y1,x0:x1]=False
    return bool(a.any())


def hug_ink(page,box):
    """Tight vertical band of a furniture text box's OWN ink.

    Renders the box (+3 pt above/below) and scans outward from the box's
    middle ink row to the first fully white pixel row on each side.  Returns
    the band as a Rect, or None when it does not close inside the box (the
    furniture's ink touches a neighbour's).  A mask on this band whites out
    only furniture ink, whatever word boxes it overlaps.
    """
    k=4.0; clip=fitz.Rect(box.x0,box.y0-3,box.x1,box.y1+3)
    pm=page.get_pixmap(matrix=fitz.Matrix(k,k),clip=clip,colorspace=fitz.csGRAY,alpha=False)
    a=np.frombuffer(pm.samples,np.uint8).reshape(pm.height,pm.stride)[:,:pm.width]
    ink=(a<235).any(axis=1)
    c=int((box.y0+box.y1)/2-clip.y0)*int(k)
    c=min(max(c,0),len(ink)-1)
    if not ink[c]:
        near=[i for i in range(len(ink)) if ink[i]]
        if not near:
            return None
        c=min(near,key=lambda i:abs(i-c))
    t=c
    while t>0 and ink[t]: t-=1
    b=c
    while b<len(ink)-1 and ink[b]: b+=1
    if ink[t] or ink[b]:
        return None
    # extend into the blank gap on each side by half its height (<=1.5 pt):
    # at the crop's own render resolution the glyphs' antialias halo reaches
    # a little beyond the 4x-render ink rows (the '[Total: 12]' bracket feet
    # survived under 9702/22/F/M/16 Q3(c) and pulled the crop down)
    t2=t
    while t2>0 and not ink[t2-1]: t2-=1
    b2=b
    while b2<len(ink)-1 and not ink[b2+1]: b2+=1
    t=t-min((t-t2)//2,int(1.5*k)); b=b+min((b2-b)//2,int(1.5*k))
    y0=clip.y0+t/k; y1=clip.y0+b/k
    if y0<box.y0-2.5 or y1>box.y1+2.5:
        return None
    return fitz.Rect(box.x0-1,y0,box.x1+1,y1)


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
        if page.number==0:
            continue      # cover page: never cropped (its drawings overlap the margin strip)
        rects=[]; fspans=[]; inkproof=[]
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines',[]):
                # '[Total: 10]' can be split over several spans (2025+)
                ltxt=''.join(sp['text'] for sp in line['spans']).strip()
                if TOTAL_LINE_RE.match(ltxt):
                    lb=fitz.Rect(line['bbox'])
                    hb=hug_ink(page,lb)
                    fspans.append(lb+(-1,-1,1,1))
                    if hb is not None:
                        rects.append(hb); inkproof.append(hb)
                    else:
                        rects.append(lb+(-1,-1,1,1))
                    continue
                for span in line['spans']:
                    text=span['text'].strip()
                    bbox=fitz.Rect(span['bbox'])
                    barcode=is_barcode_span(span['text'],bbox.y0,bbox.y1)
                    is_furniture=(barcode
                        or (BARCODE_CAPTION_RE.match(text) and bbox.y1<HEADER_Y+20)
                        or (MARGIN_STRIP_RE.search(text) and (bbox.x1<35 or bbox.x0>560))
                        or TOTAL_LINE_RE.match(text))
                    if is_furniture:
                        fspans.append(bbox+(-1,-1,1,1))
                    if barcode:
                        if bbox.y1<100:
                            # header barcode: bars rise well above the
                            # font's nominal bbox, up to the page top margin
                            rects.append(fitz.Rect(bbox.x0-2,18,bbox.x1+2,bbox.y1+1.5))
                        else:
                            # footer QR glyphs: mask their own box only
                            rects.append(bbox+(-1,-1,1,1))
                    elif TOTAL_LINE_RE.match(text):
                        hb=hug_ink(page,bbox)
                        if hb is not None:
                            rects.append(hb); inkproof.append(hb)
                        else:
                            rects.append(bbox+(-1,-1,1,1))
                    elif ((BARCODE_CAPTION_RE.match(text) and bbox.y1<HEADER_Y+20)
                            or (MARGIN_STRIP_RE.search(text) and (bbox.x1<35 or bbox.x0>560))):
                        rects.append(bbox+(-1,-1,1,1))
        # 2010s examiner mark boxes in the right margin next to answer lines,
        # drawn as separate line segments (9702/51/M/J/14 p.8): a column of
        # >=4 drawings confined to x>=528 spanning <=35 pt, with no text
        pw_=page.get_text('words')
        margin=[d['rect'] for d in page.get_drawings() if d.get('rect') is not None
                and d['rect'].x0>=528 and d['rect'].x1<=572 and d['rect'].y0>60 and d['rect'].y1<790
                # box edges only: a graph grid's right-hand verticals also sit
                # at x>=528 (9702/42/F/M/24 p.4, 9702/41/M/J/18 p.22)
                and d['rect'].height<=40 and d['rect'].width<=35
                and not [w for w in pw_ if fitz.Rect(w[:4]).intersects(d['rect']+(-2,-2,2,2))]]
        if margin:
            mx0=min(r.x0 for r in margin); mx1=max(r.x1 for r in margin)
            # a body line (e.g. a table row rule) ending at the column's left
            # edge means the verticals are a TABLE border, not mark boxes
            # (9702/42/F/M/26 Table 1.1 lost its right border)
            joined=[d['rect'] for d in page.get_drawings() if d.get('rect') is not None
                    and d['rect'].x0<mx0-3 and abs(d['rect'].x1-mx0)<=2.5]
            if os.environ.get('AL_DEBUG_MARGIN'):
                print('MARGIN page',page.number+1,'n',len(margin),'span',round(mx1-mx0,1),'joined',[[round(v,1) for v in j] for j in joined][:4],file=sys.stderr)
            # a manual spec can declare a page has no mark boxes: small
            # filled shapes of a figure at the margin (butterfly wing spots,
            # 9700/42/F/M/22 p.13) are not boxes
            if len(margin)>=4 and 15<=mx1-mx0<=35 and not joined \
                    and page.number+1 not in globals().get('AL_NO_MARK_BOX_PAGES',()):
                rects.extend(r+(-1,-1,1,1) for r in margin)
        # 2025+ corner crop-marks (small L shapes at the page corners)
        for d in page.get_drawings():
            r=d.get('rect')
            if (r is not None and r.y0>785 and max(r.width,r.height)<=25 and
                    (r.x1<62 or r.x0>533)):
                rects.append(r+(-2.5,-2.5,2.5,2.5))     # stroke width + antialias
        # 2010s Paper 5: examiner's marking grid at the foot of the planning
        # answer page ('Defining the problem | Methods of data collection |
        # Method of analysis | Safety considerations | Additional detail').
        pw=page.get_text('words')
        heads=[w for w in pw if w[4]=='Defining' and any(
            v[4]=='problem' and abs(v[1]-w[1])<14 for v in pw) and any(
            v[4]=='Safety' and abs(v[1]-w[1])<3 for v in pw)]
        if heads:
            top=min(w[1] for w in heads)
            box=[d['rect'] for d in page.get_drawings() if d.get('rect') is not None
                 and d['rect'].y0>=top-8 and d['rect'].y1<=top+60]
            bottom=max([top+24]+[r.y1 for r in box])
            grid=fitz.Rect(45,top-6,555,bottom+2)
            if box:                           # include the examiner total box
                grid=fitz.Rect(min([grid.x0]+[r.x0 for r in box]),min([grid.y0]+[r.y0 for r in box]),
                               max([grid.x1]+[r.x1 for r in box]),max([grid.y1]+[r.y1 for r in box]))
            grid=grid+(-1,-1,1,1)
            rects.append(grid)
            fspans.extend(fitz.Rect(w[:4]) for w in pw if grid.contains(fitz.Point((w[0]+w[2])/2,(w[1]+w[3])/2)))
        if not rects:
            continue
        # Safety 1: every word a mask touches must itself be furniture.
        for w in page.get_text('words'):
            wr=fitz.Rect(w[:4])
            if wr.y0>790 or wr.y1<72 or wr.x1<35 or wr.x0>560:
                continue    # header/footer/margin zones hold only page furniture
            if re.fullmatch(r'[.…]+',w[4]):
                continue    # a dotted leader under the footer QR code (9701/42/F/M/25 p.3): no content
            # an ink-hugged mask (hug_ink) holds only the furniture's own
            # glyph rows between blank pixel rows, so overlapping a
            # neighbour's word BOX ('[Total: 10]' under 'tension = ...
            # N [2]', 9702/23/M/J/20 p.7) cannot white out its glyphs
            if any(wr.intersects(r) and not any(r is q for q in inkproof) for r in rects):
                c=fitz.Point((w[0]+w[2])/2,(w[1]+w[3])/2)
                if not any(f.contains(c) for f in fspans):
                    if os.environ.get('AL_DRAFT'):
                        # draft: never white out content; drop the offending masks
                        rects=[r for r in rects if not wr.intersects(r) or any(r is q for q in inkproof)]
                        continue
                    raise RuntimeError(f'REVIEW_REQUIRED: furniture mask covers content word {w[4]!r} on page {page.number+1}')
        def item_rects(d):
            # per-item geometry: a compound path's overall bbox (a whole
            # table or graph, 9702/41/M/J/18 p.22) says nothing about where
            # its strokes actually are
            out=[]
            for it in d.get('items',[]):
                pts=[v for v in it[1:] if isinstance(v,fitz.Point)]
                if it[0]=='re':
                    out.append(fitz.Rect(it[1]))
                elif it[0]=='qu':
                    out.append(fitz.Quad(it[1]).rect)
                elif pts:
                    out.append(fitz.Rect(min(q.x for q in pts),min(q.y for q in pts),
                                         max(q.x for q in pts),max(q.y for q in pts)))
            return out
        for d in page.get_drawings():
            dr=d.get('rect')
            in_furniture_zone=(dr is not None and (dr.x1<35 or dr.x0>560 or dr.y1<72 or dr.y0>790))
            if dr is None or in_furniture_zone or not any(r.intersects(dr) for r in rects):
                continue
            for ir in item_rects(d):
                ir=ir+(-0.5,-0.5,0.5,0.5)     # stroke width
                hits=[r for r in rects if r.intersects(ir) and not r.contains(ir)]
                # an ink-hugged text mask is judged by pixels, not geometry:
                # clipped hatch lines run (invisibly) under '[Total: 11]' in
                # 9702/22/M/J/20 p.11.  Foreign ink = rendered ink inside the
                # mask outside the furniture's own character boxes.
                hits=[r for r in hits if not (any(r is q for q in inkproof) and not foreign_ink(page,r))]
                if hits:
                    if os.environ.get('AL_DEBUG_MASK'):
                        print('MASKHIT item',[round(v,1) for v in ir],'masks',[[round(v,1) for v in r] for r in rects if r.intersects(ir)],file=sys.stderr)
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
    source_doc=fitz.open(SRC)
    standard_w,standard_h=595.276,841.89
    normalize_geometry=any(
        abs(page.rect.width-standard_w)>8 or abs(page.rect.height-standard_h)>8
        for page in source_doc
    )
    if normalize_geometry:
        # A small official export family uses a uniformly enlarged
        # 642x889-point body while retaining the same IB layout.  Normalize
        # the complete paper in memory so marker columns, right-edge content,
        # answer furniture, and crop constants all stay in one coordinate
        # system.  show_pdf_page preserves text, vector drawings, and images;
        # the source PDF itself is never modified.
        doc=fitz.open()
        for source_pno in range(source_doc.page_count):
            source_page=source_doc[source_pno]
            # Some official exports keep the intended A4 page in an inset
            # TrimBox while the MediaBox includes 21 pt of printer bleed,
            # crop marks, and barcode furniture on every side.  Scaling the
            # MediaBox makes that furniture part of the question image and
            # subtly distorts the page.  Prefer the declared A4 TrimBox when
            # it is itself standard-sized; otherwise preserve the complete
            # source page (the older uniformly enlarged export family has no
            # useful inset trim box).
            trim=source_page.trimbox
            clip=(trim if abs(trim.width-standard_w)<=8 and
                  abs(trim.height-standard_h)<=8 else source_page.rect)
            page=doc.new_page(width=standard_w,height=standard_h)
            page.show_pdf_page(page.rect,source_doc,source_pno,
                               keep_proportion=False,clip=clip)
        source_doc.close()
    else:
        doc=source_doc
    if IS_ALEVEL:
        mask_alevel_furniture(doc)
    if IS_IGCSE:
        # A small third-party Cambridge scan family overlays the same 201x200
        # Papacambridge corner image exactly at the top-right page edge.  It
        # is neither source question content nor a watermark we should emit.
        # Remove only this distinctive edge-locked raster object in memory;
        # ordinary diagrams and all PDF text/vector maths remain untouched.
        for page in doc:
            intrusive=[]
            for image in page.get_images(full=True):
                xref=image[0]
                try:
                    rects=page.get_image_rects(xref)
                except Exception:
                    continue
                if any(rect.y0<=1 and rect.x1>=page.rect.width-1 and
                       150<=rect.width<=260 and 150<=rect.height<=260
                       for rect in rects):
                    intrusive.append(xref)
            for xref in set(intrusive):
                page.delete_image(xref)
    A,M,S,W,DOT,INK,CREDIT={},{},{},{},{},{},{}; seq=[]
    for pno in range(doc.page_count):
        a,m,s,w,dot=analyse(doc[pno])
        for x in a: x['pno']=pno
        if IS_ALEVEL:
            # a roman label with another roman label on its row is an inline
            # label of a figure ('(i) glycine  (ii) aspartic acid  (iii)
            # lysine', 9701/06/M/J/04 Q6(b)), not a subpart
            # (only a LATER numeral to the right: '(iii) Use your answer to
            # (ii)' is a cross-reference, 9701/22/F/M/16)
            def _succ(lab_):
                return ROMAN_ORDER[ROMAN_ORDER.index(lab_)+1] if lab_ in ROMAN_ORDER[:-1] else None
            a=[x for x in a if not (x['kind']=='ROMAN' and any(
                abs(v[1]-x['y'])<4 and v[0]-x.get('x',0)>40 and
                v[4]==f"({_succ(x['label'])})" for v in w))]
        A[pno],M[pno],S[pno],W[pno],DOT[pno]=a,m,s,w,dot
        CREDIT[pno]=credit_rectangles(doc[pno])
        INK[pno]=Ink(doc[pno]); seq.extend(a)
    if os.environ.get('SPLITTER_DEBUG_ANCHORS'):
        for pno in range(doc.page_count):
            if S[pno]:
                print(
                    'RAW_STOPS',pno+1,
                    ','.join(str(round(value,2)) for value in S[pno]),
                    file=sys.stderr,
                )
        for anchor in seq:
            print(
                'RAW_ANCHOR',anchor['pno']+1,anchor['kind'],
                anchor['label'],round(anchor['x'],2),round(anchor['y'],2),
                file=sys.stderr,
            )
    # Remove graph-axis / table integers before validating roman sequences.
    # Otherwise a fake numeric `Q` between real `(i)` and `(ii)` resets the
    # roman run and silently drops `(ii)` (0580_s13_qp_43 Q3(c)).
    seq=drop_false_igcse_questions(seq)
    if IS_MATHS:
        # '6 (i) A man walks ...' inline with the number reads as part '(i)';
        # with '(ii)' following in the same question it is the first roman
        # (9709/04/O/N/07 Q6)
        qs=[i for i,a in enumerate(seq) if a['kind']=='Q']+[len(seq)]
        for qa,qb in zip(qs,qs[1:]):
            grp_=seq[qa:qb]
            parts_=[a for a in grp_ if a['kind']=='PART']
            if parts_ and all(a['label']=='i' for a in parts_) and any(
                    a['kind']=='ROMAN' and a['label']=='ii' for a in grp_):
                for a in parts_:
                    a['kind']='ROMAN'
    if IS_MATHS:
        # '(c) (ii) State ...' -- the part letter reprinted beside a later roman
        # of the same part (9709/15/O/N/25 Q11): drop the repeated part so the
        # roman run (i), (ii) continues
        cur=None; rep=set()
        for i,a in enumerate(seq):
            if a['kind']=='Q':
                cur=None
            elif a['kind']=='PART':
                nxt_=seq[i+1] if i+1<len(seq) else None
                if (cur is not None and a['label']==cur and nxt_ is not None and nxt_['kind']=='ROMAN'
                        and nxt_['pno']==a['pno'] and abs(nxt_['y']-a['y'])<3):
                    rep.add(id(a))
                cur=a['label']
        seq=[a for a in seq if id(a) not in rep]
    seq=drop_false_romans(seq)
    seq=drop_false_igcse_subparts(seq,M)
    seq=drop_false_igcse_parts(seq)
    if IS_MATHS:
        # Older 9709 papers number sub-parts '3 (i) ... (ii) ...' with no letter
        # level (9709/62/M/J/13): a question with romans but no (a)/(b) has the
        # romans as its parts -> Q3.i, Q3.ii (what the leaf gate expects)
        dropped_=set()
        qs=[i for i,a in enumerate(seq) if a['kind']=='Q']+[len(seq)]
        for qa,qb in zip(qs,qs[1:]):
            grp_=seq[qa:qb]
            if not any(a['kind']=='PART' for a in grp_) and any(a['kind']=='ROMAN' for a in grp_):
                # letter tasks are leaves only when separately marked: a [n]
                # between each and the next (one shared mark -> the roman is
                # one leaf, 9709/41/M/J/13 Q7(iii)) -- the leaf gate's rule
                runs_=[]
                for a in grp_:
                    if a['kind']=='ROMAN':
                        runs_.append([])
                    elif a['kind']=='SUBPART' and a['label'].isalpha() and runs_:
                        runs_[-1].append(a)
                def marked_(a,b):
                    for pg in range(a['pno'],b['pno']+1):
                        lo=a['y']-3 if pg==a['pno'] else 0
                        hi=b['y'] if pg==b['pno'] else 1e9
                        if any(lo<my<hi for my,_ in M.get(pg,[])):
                            return True
                    return False
                drop_=[id(a) for kids in runs_ if len(kids)<2 or
                       not all(marked_(x,y) for x,y in zip(kids,kids[1:])) for a in kids]
                if drop_:
                    dropped_.update(drop_)
                    grp_=[a for a in grp_ if id(a) not in drop_]
                for a in grp_:
                    if a['kind']=='ROMAN':
                        a['kind']='PART'
                    elif a['kind']=='SUBPART' and a['label'].isalpha():
                        # '(ii) ... Find (a) ... [4] (b) ... [1]': separately marked
                        # tasks under a roman-as-part are its leaves -> Q6.ii.a, Q6.ii.b
                        # (user decision 2026-10-20; 9709/04/O/N/07 Q6(ii))
                        a['kind']='ROMAN'
        seq=[a for a in seq if id(a) not in dropped_]
    if os.environ.get('SPLITTER_DEBUG_ANCHORS'):
        for anchor in seq:
            print(
                'KEPT_ANCHOR',anchor['pno']+1,anchor['kind'],
                anchor['label'],round(anchor['x'],2),round(anchor['y'],2),
                file=sys.stderr,
            )
    for pno in A: A[pno]=[x for x in seq if x['pno']==pno]

    # A horizontal cut is normally ideal, but typeset mathematics can place a
    # tall expression from the next item above the bottom of the preceding
    # item.  In that case the two semantic owners overlap in y while remaining
    # separated in x.  boundary(..., require_separation=True) records a
    # fail-closed 2-D seam request; the renderer later masks opposite sides of
    # a proven all-white path instead of clipping either expression.
    seam_candidates=[]
    # A few Cambridge response matrices use symbol-font bracket pieces whose
    # visible glyphs extend 10--15 pt above and below their extracted word
    # boxes.  Their caps can therefore overlap the prompt (or the following
    # prompt) in y even though they are safely isolated in the far-right
    # response column.  Record only those raster-proven out-of-box glyphs for
    # a narrow white mask at render time.  This is preferable to a horizontal
    # cut, which would either leave a detached bracket cap or clip real maths.
    response_furniture_masks={}
    DOT_MASKS=[]       # dots of plain answer rows kept for their mark (D6 step 2d), for the gates

    def register_response_rect(pno,rect):
        key=tuple(round(value,2) for value in rect)
        page_masks=response_furniture_masks.setdefault(pno,{})
        page_masks[key]=fitz.Rect(*rect)

    def register_response_word(pno,word,pad_x=1.5,pad_y=1.5):
        rect=(word[0]-pad_x,word[1]-pad_y,
              word[2]+pad_x,word[3]+pad_y)
        register_response_rect(pno,rect)

    def is_private_use(token):
        return any(0xE000<=ord(ch)<=0xF8FF for ch in token)

    def register_out_of_box_response_glyph(pno,word,force=False):
        private_symbol=is_private_use(word[4])
        mapped_far_right_bracket=(
            word[0]>400 and word[2]-word[0]<12 and word[4] in {'f','p'}
        )
        if not (force or private_symbol or mapped_far_right_bracket):
            return
        ink=INK[pno]
        moat_x=3.0
        xa=max(0,int((word[0]-CONTENT_L-moat_x)*SC))
        xb=min(ink.W-1,int((word[2]-CONTENT_L+moat_x)*SC)+1)
        ya=ink._r(max(HEADER_Y,word[1]-32))
        yb=ink._r(min(FOOTER_Y,word[3]+32))
        if xb<xa or yb<ya:
            return
        local=ink.semantic[ya:yb+1,xa:xb+1]
        seed_y0=max(0,ink._r(word[1])-ya)
        seed_y1=min(local.shape[0]-1,ink._r(word[3])-ya)
        seed_x0=max(0,int((word[0]-CONTENT_L)*SC)-xa)
        seed_x1=min(local.shape[1]-1,
                    int((word[2]-CONTENT_L)*SC)-xa+1)
        seed_points=list(zip(*np.where(
            local[seed_y0:seed_y1+1,seed_x0:seed_x1+1]
        )))
        if not seed_points:
            return
        # Keep only rendered ink connected to the extracted glyph.  A nearby
        # prompt row may share the same x-column without belonging to this
        # response object; treating all ink in the scan rectangle as one
        # glyph can create an over-large mask and erase valid question text.
        seen=np.zeros(local.shape,dtype=bool)
        stack=[(seed_y0+int(y),seed_x0+int(x)) for y,x in seed_points]
        for y,x in stack:
            seen[y,x]=True
        cursor=0
        while cursor<len(stack):
            y,x=stack[cursor]; cursor+=1
            for dy in (-1,0,1):
                for dx in (-1,0,1):
                    if dy==0 and dx==0:
                        continue
                    ny,nx=y+dy,x+dx
                    if (0<=ny<local.shape[0] and 0<=nx<local.shape[1]
                            and local[ny,nx] and not seen[ny,nx]):
                        seen[ny,nx]=True; stack.append((ny,nx))
        yy=np.where(seen)[0]
        actual_top=ink._p(ya+int(yy.min()))
        actual_bottom=ink._p(ya+int(yy.max()))
        # Normal font ascenders and antialiasing stay close to the extracted
        # bbox.  A larger excursion is the distinctive Cambridge private-font
        # bracket encoding; fail closed and mask only that object.
        if not (actual_top<word[1]-4 or actual_bottom>word[3]+4):
            return
        rect=(word[0]-moat_x,actual_top-1,
              word[2]+moat_x,actual_bottom+1)
        key=tuple(round(value,2) for value in rect)
        page_masks=response_furniture_masks.setdefault(pno,{})
        page_masks[key]=fitz.Rect(*rect)
        if os.environ.get('SPLITTER_DEBUG_RESPONSE_MASKS'):
            print('RESPONSE_MASK',pno+1,word[4],word[:4],key,
                  file=sys.stderr)

    # Register every explicit legacy response row independently of the crop
    # windows.  A tall matrix can overlap the following sibling in y, so the
    # previous leaf's logical interval may end before its visible Answer(...)
    # furniture even though that furniture still rises into the next crop.
    # Exact response labels are unambiguous; mask their row word-by-word and
    # use connected rendered components for the tall bracket glyphs.
    if IS_IGCSE:
        answer_label_re=re.compile(
            r'^Answer(?:(?:\([a-zivx]+\))+|:)$',re.I)
        for response_pno,page_words in W.items():
            for answer_word in page_words:
                if not answer_label_re.match(answer_word[4]):
                    continue
                later_mark_words=[word for word in page_words
                                  if MARK_RE.match(word[4]) and
                                  answer_word[1]-8<=word[1]<=answer_word[1]+100]
                mark_word=(min(later_mark_words,key=lambda word:word[1])
                           if later_mark_words else None)
                row_bottom=(mark_word[3] if mark_word is not None else
                            answer_word[3]+5)
                row_right=(mark_word[2]+2 if mark_word is not None else
                           min(CONTENT_R,answer_word[2]+220))
                register_response_rect(
                    response_pno,
                    (answer_word[0]-2,answer_word[1]-2,
                     row_right,row_bottom+4),
                )
                for word in page_words:
                    if (word[0]>=answer_word[0]-3 and
                            answer_word[1]-5<=word[1]<=row_bottom+4):
                        register_response_word(response_pno,word)
                for word in page_words:
                    if (word[0]>400 and word[2]-word[0]<12 and
                            (word[4] in {'f','p'} or
                             is_private_use(word[4])) and
                            answer_word[1]-35<=word[1]<=row_bottom+5):
                        register_response_word(response_pno,word)
                        register_out_of_box_response_glyph(
                            response_pno,word,force=True)

    def first_stop(pno,y):
        for v in S[pno]:
            if v>y+2: return v
        return FOOTER_Y
    def last_stop_before(pno,y):
        vals=[v for v in S[pno] if HEADER_Y<=v<y-2]
        return max(vals) if vals else HEADER_Y
    def next_anchor_y(pno,y):
        for a in A[pno]:
            if a['y']>y+2: return a['y']
        return FOOTER_Y
    def mark_bot(pno,y0,y1):
        ms=[m for m in M[pno] if y0-2<=m[0]<=y1]
        return max(ms,key=lambda t:t[0])[1] if ms else None
    def answer_row_top(pno,y0,y1):
        """Top of a dotted answer row carrying this item's mark, if any.

        The mark's position is still needed as a structural boundary when we
        search for later stems.  Only the rendered crop stops before the row.
        Keeping those two roles separate prevents wrapped prompt lines from
        being mistaken for a new sibling stem.
        """
        if not IS_IGCSE:
            return None
        ms=[m for m in M[pno] if y0-2<=m[0]<=y1]
        rows=[dot_y for dot_y in DOT[pno]
              if any(abs(dot_y-m[0])<5 for m in ms)]
        # Older 0580 PDFs omit their visible dotted leaders / matrix answer
        # boxes from text and vector extraction.  They do retain a literal
        # `Answer(a)` token on the mark row, which is an equally authoritative
        # start of the response area.
        legacy_rows=[]
        for answer_word in W[pno]:
            if not (y0-2<=answer_word[1]<=y1 and
                    re.match(r'^Answer(?:(?:\([a-zivx]+\))+|:)$',
                             answer_word[4],re.I)):
                continue
            # The literal response label is authoritative even when a large
            # working area puts its mark allocation more than 40 pt below.
            # Treating mark proximity as mandatory left 150 legacy Answer(...)
            # rows inside otherwise structurally valid crops.
            later_marks=[m for m in ms if answer_word[1]-8<=m[0]<=y1]
            nearby_marks=([min(later_marks,key=lambda m:m[0])]
                          if later_marks else [])
            response_top=answer_word[1]
            register_response_word(pno,answer_word)
            # Remove this response row's mark too.  This matters when a tall
            # matrix answer overlaps the next sibling in y and the crop must
            # retain the next prompt on the left side of the same rows.
            if nearby_marks:
                mark_y=nearby_marks[0][0]
                for mark_word in W[pno]:
                    if (MARK_RE.match(mark_word[4]) and
                            abs(mark_word[1]-mark_y)<2.5):
                        register_response_word(pno,mark_word)
            # A matrix-entry response box can rise above its `Answer(b)`
            # label.  Cambridge encodes the bracket pieces as private-use
            # glyphs, so include their true top as the response-area start.
            mark_y=(nearby_marks[0][0] if nearby_marks else
                    min(y1,answer_word[1]+65))
            bracket_words=[w for w in W[pno]
                           if max(y0,answer_word[1]-35)<=w[1]<=mark_y+5
                           and (is_private_use(w[4]) or
                                (w[0]>400 and w[2]-w[0]<12 and
                                 w[4] in {'f','p'}))]
            if bracket_words:
                response_top=min(response_top,
                                 min(w[1] for w in bracket_words))
                for word in bracket_words:
                    register_response_word(pno,word)
                    register_out_of_box_response_glyph(pno,word,force=True)
            # PDF clip rectangles include antialiased edge pixels at their
            # lower coordinate; leave a small white moat above the response
            # object so a curved bracket cap cannot survive in the prompt.
            legacy_rows.append(max(y0+2,response_top-2))
        # A column-vector / matrix response can be drawn with symbol-font
        # bracket pieces and no dotted leader or `Answer(...)` label.  In the
        # PDF it shares a content block with the right-edge mark allocation.
        # When that whole non-mark block begins well below the prompt row, its
        # top is the authoritative response-area start.  Requiring the block
        # itself (not merely a later line in the prompt block) to begin below
        # the anchor prevents wrapped question prose from being cut away.
        mark_block_rows=[]
        for mark_word in W[pno]:
            # A Level: a numeric prompt line ending in its mark, e.g.
            # '4.0 x 10-6 m, [1]' (9702/42/M/J/13 Q7(b)(i)1.), is question
            # text; this IGCSE-maths matrix-answer heuristic cut it off.
            if IS_ALEVEL:
                break
            if not (MARK_RE.match(mark_word[4]) and
                    y0-2<=mark_word[1]<=y1):
                continue
            block_no=int(mark_word[5])
            other=[word for word in W[pno]
                   if int(word[5])==block_no and word is not mark_word
                   and CONTENT_L<=word[0]<=INK[pno].content_r
                   and not MARK_RE.match(word[4])]
            if (not other or any(re.search(r'[A-Za-z]{2,}',word[4])
                                 for word in other)):
                continue
            block_top=min(word[1] for word in other)
            if block_top>y0+10 and block_top<=mark_word[1]+5:
                for word in other:
                    register_out_of_box_response_glyph(pno,word)
                mark_block_rows.append(max(y0+2,block_top-2))
        # An explicit Answer(...) label is stronger evidence than a dotted
        # row: in compact legacy fill-ins, the answer leader can begin on the
        # same row as `(ii)` and must stay with the prompt, while the literal
        # label below marks the true response-area boundary.
        if legacy_rows:
            return min(legacy_rows)
        rows.extend(mark_block_rows)
        return min(rows) if rows else None
    def on_dot_row(pno,y):
        """True when y falls on a row already recognised as a dotted /
        labelled answer line (DOT[pno]: dot-leader rows AND short-label
        rows like `Working:`, `Answer:`, `Protons:`, `Mg3N2:`, `Reagent:`
        that are >60% repeated-leader-character by the same test used in
        analyse(), or a label-only row immediately above a genuine dotted
        row).  Such rows are response furniture, never shared prose, even
        when their label prefix carries ordinary letters that would
        otherwise look like the start of a mid-question stem sentence.
        """
        return any(abs(y-dy)<=1.5 for dy in DOT[pno])
    def midstem_start(pno,after,ceil,left_max=140,allow_body_indent=False):
        y=_midstem_start_raw(pno,after,ceil,left_max,allow_body_indent)
        if y is None or not IS_ALEVEL:
            return y
        # A Level: a stem never starts mid-sentence.  'Show that ... is' /
        # 'given by the expression' (9702/42/M/J/12 Q4(a)(ii)) was split off
        # as a stem for (b).  Reject when the candidate's first word is
        # lowercase or the previous prose line does not end a sentence.
        row=sorted([w for w in W[pno] if abs(w[1]-y)<4 or (y<=w[1]<y+6)],key=lambda w:(round(w[1]),w[0]))
        first=next((w for w in row if re.search(r'[A-Za-z]',w[4])),None)
        prev=[w for w in W[pno] if after-1<=w[1]<y-3 and not DOTS_RE.match(w[4])]
        if prev:
            last_y=max(w[1] for w in prev)
            last=sorted([w for w in prev if abs(w[1]-last_y)<3],key=lambda w:w[0])[-1][4]
        else:
            last='.'
        if (first is not None and first[4][:1].islower()) or not re.search(r'[.:?!\])]$',last):
            return None
        # a stem never carries a mark: a [n] before the next label means this is
        # the previous item's own later prompt (its second bullet printed at
        # the top of the next page, 9701/53/O/N/14 Q1(a), 9701/42/F/M/19 Q4(a)(ii))
        if any(y-1<w[1]<ceil-2 and MARK_RE.match(w[4]) for w in W[pno]):
            return None
        # nor on an equation/formula row: '___ Ca3(PO4)2 + ___ SiO2 + ...' is
        # the previous item's fill-in answer (9701/41/M/J/10 Q1(b)(i)); the
        # stem starts at the next prose row ('When heated to 400 C ...')
        def prose_row(yy):
            return any(re.fullmatch(r'[a-z]{3,}[.,;:]?',w[4]) for w in W[pno] if abs(w[1]-yy)<3)
        if not prose_row(y):
            nxt=sorted({round(w[1],1) for w in W[pno] if y+3<w[1]<ceil-2 and prose_row(w[1])})
            if not nxt:
                return None
            y=min(w[1] for w in W[pno] if abs(w[1]-nxt[0])<3)
        return y
    def _midstem_start_raw(pno,after,ceil,left_max=140,allow_body_indent=False):
        """Start y of a genuine mid-question stem in (after, ceil), or None.

        `left_max` is the deepest indent that can still count as a stem.
        Callers pass the CURRENT item's label x plus a small tolerance, which
        lands between the label column and the body column (~28pt apart).
        That separates the two cases cleanly: a subpart whose text wraps onto
        a second line puts that continuation at the BODY indent (rejected --
        otherwise the subpart gets cut in half at its line break), while a
        real mid-stem is outdented to the LABEL column (accepted). The
        tolerance absorbs the leading short word of a stem line ("A line
        L2 has equation...") without reaching the body column.
        """
        if after is None: return None
        # A label/atom token that sits on or immediately beside real vector
        # artwork (a structural-formula diagram, a graph, a table rule) is
        # part of that diagram, never the first word of a new shared-context
        # sentence -- even when its glyphs are ordinary letters ("H2C", "O",
        # "CYCLES") and its x-position lands in the label/body column that a
        # genuine stem would use.  Skipping the whole row once any word on it
        # is diagram-anchored prevents a chemistry structural formula (or any
        # other in-body diagram with printed labels) from being mistaken for
        # the start of the NEXT sibling's shared stem, which would otherwise
        # sever the diagram from the part that owns it.
        #
        # `graphical_content_between` flags ANY single vector stroke over
        # ~10pt, which would also flag an ordinary fraction bar in a Maths/
        # Physics equation -- those are common width>10,height<1 strokes
        # with no special surrounding constraint, so using the raw check
        # turns any fraction sitting in the label column into a false
        # "diagram" and silently drops the real prose row it belongs to
        # (e.g. a Maths P1 stem "Let y = ln x / x^4 ..." vanishing
        # entirely). `scaffold_bounds` clusters connected drawings and
        # keeps only genuinely two-dimensional ones, but on a page whose
        # printed border is itself a full-page vector rectangle (common in
        # official IB exports; confirmed on N20 Maths P3 HL/SL), that
        # border rect alone already exceeds scaffold_bounds's own size
        # threshold and overlaps every row's y-window on the page, so
        # scaffold_bounds returns non-None unconditionally there and this
        # gate would wrongly treat EVERY row as diagram-anchored (dropping
        # entire question stems, not just ones with fractions). Use a
        # local variant that additionally excludes any drawing spanning
        # almost the whole page -- that is page furniture, never content
        # belonging to one row.
        def _local_diagram(pno,y0,y1):
            page=doc[pno]
            page_w,page_h=page.rect.width,page.rect.height
            def is_page_furniture(rect):
                return rect.width>=page_w*0.9 and rect.height>=page_h*0.9
            components=[]
            for image in page.get_images(full=True):
                for rect in page.get_image_rects(image[0]):
                    body_overlap=(min(rect.x1,CONTENT_R-40)-
                                  max(rect.x0,CONTENT_L))
                    if (body_overlap>12 and rect.y1>y0+1 and rect.y0<y1-1 and
                            rect.width>12 and rect.height>8 and
                            not is_page_furniture(rect)):
                        components.append(fitz.Rect(rect))
            # Cluster vector strokes over the FULL candidate gap (after..ceil),
            # not just this one row's narrow (y0,y1) slice. A multi-line
            # structural-formula diagram (e.g. a triglyceride's three stacked
            # ester groups) has each row contribute only its own short bond
            # segments -- a double-bond stroke ~10pt tall, a couple of ~11pt
            # horizontal bond fills.  Clustered one row at a time, none of
            # those ever reaches the qualifying 2-D object size, so every row
            # independently looks like ordinary prose and `midstem_start`
            # mistakes the diagram's own first row for the start of a new
            # shared stem -- severing the diagram from the part that owns it
            # (confirmed: IB Chemistry P3 HL M23 Q13(b)'s triglyceride leaking
            # into Q13(c)'s crop). Clustering across the whole gap lets the
            # backbone/double-bond strokes connecting successive rows join
            # into the one connected diagram they actually are; a given row is
            # then "diagram-anchored" only if it falls inside a cluster that
            # is big enough to be a real 2-D object once fully assembled --
            # the same size gate `scaffold_bounds` already uses -- so an
            # isolated fraction bar in an unrelated row still cannot qualify.
            wide0,wide1=min(after,y0),max(ceil,y1)
            drawing_rects=[]
            for drawing in page.get_drawings():
                rect=drawing.get('rect')
                if not rect or is_page_furniture(rect): continue
                body_overlap=(min(rect.x1,CONTENT_R-40)-
                              max(rect.x0,CONTENT_L))
                vertical_body_line=(rect.width<=1 and
                                    CONTENT_L<=rect.x0<=CONTENT_R-40)
                if ((body_overlap>12 or vertical_body_line) and
                        rect.y1>wide0+1 and rect.y0<wide1-1 and
                        (rect.width>6 or rect.height>6)):
                    drawing_rects.append(fitz.Rect(rect))
            clusters=[]
            for rect in sorted(drawing_rects,key=lambda r:(r.y0,r.x0)):
                matches=[idx for idx,cluster in enumerate(clusters)
                         if (rect.y0<=cluster.y1+8 and rect.y1>=cluster.y0-8 and
                             rect.x0<=cluster.x1+12 and rect.x1>=cluster.x0-12)]
                if not matches:
                    clusters.append(fitz.Rect(rect)); continue
                base=matches[0]
                clusters[base]=fitz.Rect(
                    min(clusters[base].x0,rect.x0),min(clusters[base].y0,rect.y0),
                    max(clusters[base].x1,rect.x1),max(clusters[base].y1,rect.y1))
                for idx in reversed(matches[1:]):
                    other=clusters[idx]
                    clusters[base]=fitz.Rect(
                        min(clusters[base].x0,other.x0),min(clusters[base].y0,other.y0),
                        max(clusters[base].x1,other.x1),max(clusters[base].y1,other.y1))
                    del clusters[idx]
            for rect in clusters:
                if (((rect.width>=100 and rect.height>=30) or
                        (rect.width>=50 and rect.height>=50)) and
                        rect.y1>y0+1 and rect.y0<y1-1):
                    components.append(rect)
            return bool(components)
        def _graphic_row(w):
            return _local_diagram(pno,w[1]-1,w[3]+1)
        c=[w[1] for w in W[pno] if after+6<w[1]<ceil-3 and 55<=w[0]<=left_max
           and re.search(r'[A-Za-z]',w[4]) and len(w[4])>1
           and not (PAR_RE.match(w[4]) or Q_RE.match(w[4]) or MARK_RE.match(w[4]))
           and not on_dot_row(pno,w[1]) and not _graphic_row(w)]
        # A genuine context sentence may begin with a number or symbol, so
        # its first alphabetic word can sit to the right of the usual label
        # column: "90% of adult cuttlefish are male" is the shared stem for
        # the following part (c).  Accept such a row when its first token is
        # outdented like a stem and the same row contains real prose.  Bare
        # equations, dotted answer rows, and mark allocations remain excluded.
        rows={}
        for w in W[pno]:
            if after+6<w[1]<ceil-3:
                rows.setdefault(round(w[1]/3)*3,[]).append(w)
        for row_y,ws in rows.items():
            if on_dot_row(pno,row_y): continue
            ordered=sorted(ws,key=lambda w:w[0])
            body=[w for w in ordered if 55<=w[0]<=CONTENT_R]
            if not body or body[0][0]>left_max:
                continue
            if on_dot_row(pno,min(w[1] for w in body)):
                continue
            # Same fraction-bar-vs-diagram discrimination as `_graphic_row`
            # above -- use the border-excluding `_local_diagram` test, not
            # the raw single-stroke `graphical_content_between` (fires on
            # any fraction bar) nor plain `scaffold_bounds` (fires on
            # every row when the page has a full-page border rectangle),
            # or an equation's fraction bar in this row silently drops it.
            if _local_diagram(pno,min(w[1] for w in body)-1,
                                max(w[3] for w in body)+1):
                continue
            lexical=[w for w in body if w[0]<260 and re.search(r'[A-Za-z]',w[4])
                     and len(w[4])>1 and not (PAR_RE.match(w[4]) or
                     Q_RE.match(w[4]) or MARK_RE.match(w[4]))]
            if lexical:
                c.append(min(w[1] for w in body))
        # A shared setup placed after a completed marked sibling may use the
        # ordinary 99 pt body indent instead of the 71 pt label indent.  It is
        # still a stem when it begins in a new PDF content block and ends on a
        # distinct line above the next parent/roman marker.  Requiring a real
        # prose word of at least three letters rejects detached differential,
        # exponent, and denominator fragments that PDF extraction sometimes
        # places below the preceding right-edge mark.
        if allow_body_indent:
            block_tops={}
            for w in W[pno]:
                block=int(w[5])
                block_tops[block]=min(block_tops.get(block,w[1]),w[1])
            body_prose=[w for w in W[pno]
                        if after+6<w[1]<=ceil-10 and 55<=w[0]<=240
                        and re.search(r'[A-Za-z]{3,}',w[4])
                        and not (PAR_RE.match(w[4]) or Q_RE.match(w[4]) or
                                 MARK_RE.match(w[4]))
                        and block_tops[int(w[5])]>after+4
                        and not on_dot_row(pno,w[1])]
            if body_prose:
                # Prefer prose outside a preceding graph/table.  Labels such
                # as "CYCLES" inside a requested transition diagram can
                # otherwise become the first candidate and cause the later,
                # genuine setup for the next sibling to be suppressed with
                # that scaffold.  If every candidate is graphical, keep the
                # earliest one so the existing scaffold-ownership gate can
                # still attach the complete object to its requesting leaf.
                outside_graphics=[w for w in body_prose
                                  if not graphical_content_between(
                                      pno,w[1]-4,w[3]+4)]
                chosen=outside_graphics or body_prose
                c.append(min(w[1] for w in chosen))
        return min(c) if c else None
    def has_prose(pno,y0,y1): return midstem_start(pno,y0-6,y1) is not None
    def head_prose_exists(pno,y0,y1):
        # Real body-text words from the part-label row itself (inclusive) up to
        # the first roman's top. Unlike midstem_start/has_prose (which only
        # look for a NEW row strictly after the anchor), this also catches an
        # intro clause sitting on the SAME row as the part label, e.g.
        # "(b)  For the graph of y = f(x),"  -- that's real shared context for
        # every roman under (b) and must get its own .stem, not be silently
        # merged into the first roman's crop.
        ws=[w for w in W[pno] if y0-2<=w[1]<y1-3 and 55<=w[0]<=200
            and re.search(r'[A-Za-z]',w[4]) and len(w[4])>1
            and not (PAR_RE.match(w[4]) or Q_RE.match(w[4]) or MARK_RE.match(w[4]))]
        return len(ws)>0
    def requests_following_scaffold(pno,y0,y1):
        """Whether the preceding prompt explicitly owns a scaffold below it."""
        tokens=[w[4].lower().strip('.,;:') for w in W[pno]
                if y0-2<=w[1]<=y1+2 and CONTENT_L<=w[0]<=CONTENT_R]
        text=' '.join(tokens)
        if IS_ALEVEL:
            # 'On Fig. 2.1, place a tick ...' with Fig. 2.1 printed BELOW the
            # prompt (before the next label): the figure belongs to this part
            # (9702/04/M/J/03 Q2(a); it had landed in Q2(b)'s stem)
            refs=set(re.findall(r'\b(fig|table)\s+(\d+\.\d+)',text))
            if refs and re.search(r'\b(on|in|complete|tick|mark|draw|label|sketch|plot|place|indicate|show|shade)\b',text):
                ylim=next_anchor_y(pno,y1)
                ws=sorted((w for w in W[pno] if y1<w[1]<ylim),key=lambda w:(round(w[1]),w[0]))
                for a,b in zip(ws,ws[1:]):
                    if (a[4].lower().strip('.') in ('fig','table') and abs(a[1]-b[1])<2 and
                            (a[4].lower().strip('.'),b[4].strip('.')) in refs):
                        return True
        return bool(
            (re.search(r'\bcomplete\b',text) and
             re.search(r'\b(table|diagram|tree|graph)\b',text)) or
            (re.search(r'\b(draw|sketch|plot|label)\b',text) and
             re.search(r'\b(diagram|graph|axes|axis)\b',text))
        )
    def graphical_content_between(pno,y0,y1):
        page=doc[pno]
        for image in page.get_images(full=True):
            for rect in page.get_image_rects(image[0]):
                body_overlap=(min(rect.x1,CONTENT_R-40)-
                              max(rect.x0,CONTENT_L))
                if (body_overlap>12 and
                        rect.y1>y0+1 and rect.y0<y1-1):
                    return True
        for drawing in page.get_drawings():
            rect=drawing.get('rect')
            body_overlap=(min(rect.x1,CONTENT_R-40)-
                          max(rect.x0,CONTENT_L)) if rect else 0
            if (rect and (rect.width>10 or rect.height>10) and
                    body_overlap>12 and
                    rect.y1>y0+1 and rect.y0<y1-1):
                return True
        return False
    def scaffold_bounds(pno,y0,y1):
        """Bounds of substantial table/diagram/axes content in a gap.

        PDF maths glyphs can contain short vector strokes (notably fraction
        bars).  Treating every drawing as a scaffold made a later function
        definition look like part of the preceding requested graph.  Build
        connected drawing clusters and retain only genuinely two-dimensional,
        page-body objects; raster images qualify directly.
        """
        page=doc[pno]; components=[]
        for image in page.get_images(full=True):
            for rect in page.get_image_rects(image[0]):
                body_overlap=(min(rect.x1,CONTENT_R-40)-
                              max(rect.x0,CONTENT_L))
                if (body_overlap>12 and rect.y1>y0+1 and rect.y0<y1-1 and
                        rect.width>12 and rect.height>8):
                    components.append((fitz.Rect(rect),True))
        drawing_rects=[]
        for drawing in page.get_drawings():
            rect=drawing.get('rect')
            body_overlap=(min(rect.x1,CONTENT_R-40)-
                          max(rect.x0,CONTENT_L)) if rect else 0
            vertical_body_line=(rect and rect.width<=1 and
                                CONTENT_L<=rect.x0<=CONTENT_R-40)
            if (rect and (body_overlap>12 or vertical_body_line) and
                    rect.y1>y0+1 and
                    rect.y0<y1-1 and (rect.width>6 or rect.height>6)):
                drawing_rects.append(fitz.Rect(rect))
        clusters=[]
        for rect in sorted(drawing_rects,key=lambda r:(r.y0,r.x0)):
            matches=[idx for idx,cluster in enumerate(clusters)
                     if (rect.y0<=cluster.y1+8 and rect.y1>=cluster.y0-8 and
                         rect.x0<=cluster.x1+12 and rect.x1>=cluster.x0-12)]
            if not matches:
                clusters.append(fitz.Rect(rect))
                continue
            base=matches[0]
            clusters[base]=fitz.Rect(
                min(clusters[base].x0,rect.x0),
                min(clusters[base].y0,rect.y0),
                max(clusters[base].x1,rect.x1),
                max(clusters[base].y1,rect.y1),
            )
            for idx in reversed(matches[1:]):
                other=clusters[idx]
                clusters[base]=fitz.Rect(
                    min(clusters[base].x0,other.x0),
                    min(clusters[base].y0,other.y0),
                    max(clusters[base].x1,other.x1),
                    max(clusters[base].y1,other.y1),
                )
                del clusters[idx]
        for rect in clusters:
            if ((rect.width>=100 and rect.height>=30) or
                    (rect.width>=50 and rect.height>=50)):
                components.append((rect,False))
        if not components:
            return None
        return fitz.Rect(
            min(rect.x0 for rect,_ in components),
            min(rect.y0 for rect,_ in components),
            max(rect.x1 for rect,_ in components),
            max(rect.y1 for rect,_ in components),
        )
    def prose_after_scaffold(pno,y0,y1):
        """First independent prose row below a requested graphic object."""
        scaffold=scaffold_bounds(pno,y0,y1)
        if scaffold is None:
            return None
        graphic_bottom=scaffold.y1
        candidates=[w for w in W[pno]
                    if graphic_bottom+3<w[1]<y1-3 and 55<=w[0]<=240
                    and re.search(r'[A-Za-z]{3,}',w[4])
                    and not (PAR_RE.match(w[4]) or Q_RE.match(w[4]) or
                             MARK_RE.match(w[4]))]
        return min((w[1] for w in candidates),default=None)
    def top_before(pno,my,fl): return INK[pno].content_top(my,fl)-4
    def expand_top(pno,anchor_y,floor):
        # Extend a crop's start UPWARD from the anchor's own text-row y to
        # catch inline content that is visually taller than one text line and
        # sits ABOVE the anchor's baseline on the SAME logical row -- a
        # multi-row column vector/matrix, a tall fraction, etc. (e.g.
        # "(a) (i) Show that AB x AV = -10(matrix)..." where the matrix's top
        # row renders well above the "(a)"/"(i)" token's own y). Safe because
        # `floor` is always the true end of whatever precedes this anchor
        # (previous mark-bottom, or the question-number row), and a genuinely
        # separate block is followed by a real blank-line gap that exceeds
        # the small contiguity tolerance, so the scan stops there rather than
        # bleeding into unrelated earlier content.
        return INK[pno].content_top(anchor_y, floor)
    def note_seam(pno,y_prev,y_next,cut=None,next_anchor=None,owner_pair=None,
                  split_block=None,split_line=None,upper_graphic_regions=None,
                  upper_graphic_word_regions=None):
        cut=float(cut if cut is not None else (y_prev+y_next)/2)
        for c in seam_candidates:
            if c['pno']==pno and abs(c['cut']-cut)<0.5:
                return
        nearby=[a for a in A[pno] if abs(a['y']-y_next)<4]
        anchor=next_anchor or (min(nearby,key=lambda a:abs(a['y']-y_next)) if nearby else None)
        seam_candidates.append({
            'pno':pno,'lo':float(y_prev),'hi':float(y_next),
            'cut':cut,
            'owner_pair':list(owner_pair) if owner_pair else None,
            'next_anchor':({k:anchor.get(k) for k in ('kind','label','x','y')} if anchor else None),
            'split_block':split_block,
            'split_line':split_line,
            'upper_graphic_regions':upper_graphic_regions or [],
            'upper_graphic_word_regions':upper_graphic_word_regions or [],
        })
    def boundary(pno,y_prev,y_next,require_separation=False,
                 owner_pair=None,next_anchor=None):
        """A single cut line in the whitespace separating two consecutive
        anchors. Used as BOTH the previous sibling's end and the next
        sibling's start, so consecutive crops can never overlap (which is
        what puts two subparts in one image) and can never clip each other.

        Anchor y-values are text-baseline rows, which are the wrong boundary:
        a fraction's denominator or a radical's tail on the previous sibling
        hangs BELOW its text row, and a matrix or tall fraction on the next
        sibling rises ABOVE its text row. Cutting on real ink whitespace
        handles both at once. We take the whitespace run nearest the next
        anchor, so tall content belonging to it stays on its side of the cut.
        """
        ink=INK[pno]; a=ink._r(y_prev); b=ink._r(y_next)
        if b<=a: return y_next-PAD_PT
        seg=ink.ink[a:b+1]
        zeros=np.where(seg==0)[0]
        if len(zeros)==0:
            if require_separation:
                note_seam(pno,y_prev,y_next,owner_pair=owner_pair,
                          next_anchor=next_anchor)
                return (y_prev+y_next)/2
            return y_next-PAD_PT
        runs=[]; s=p=zeros[0]
        for z in zeros[1:]:
            if z==p+1: p=z; continue
            runs.append((s,p)); s=p=z
        runs.append((s,p))
        # Ignore a white run that occurs before the first item has placed any
        # ink in this interval.  That is not a separator: it is merely the gap
        # after the question-number row.  Legacy Q10 (N20 SL P2) is the key
        # example: the real shared stem and part (a) overlap vertically, while
        # the only full-width white rows lie above both of them.
        valid=[]
        for s,e in runs:
            before=seg[:s]
            # Marker y is the top/baseline reported by text extraction; the
            # first dark glyph pixels can begin a few points below it.  Probe
            # one text-line past the anchor when proving there is a lower
            # owner, otherwise a genuine final separator (after a large
            # diagram, for example) looks like terminal page whitespace and
            # an earlier internal diagram gap is selected instead.
            probe_hi=min(ink.H-1,ink._r(y_next+14))
            after=ink.ink[a+e+1:probe_hi+1]
            if np.any(before>0) and np.any(after>0): valid.append((s,e))
        if valid:
            s,e=valid[-1]
            return ink._p(a+(s+e)//2)
        if require_separation:
            note_seam(pno,y_prev,y_next,owner_pair=owner_pair,
                      next_anchor=next_anchor)
            return (y_prev+y_next)/2
        s,e=runs[-1]
        return ink._p(a+(s+e)//2)
    def maths_row_gap_cut(pno,ay,row_bottom,y_prev):
        """Maths: a cut in the white run directly above the ink block that holds
        a labelled row (its raised limits / indices / numerators included), or
        None when that block rises more than 25 pt, has no white run above it
        inside (y_prev, ay), or contains a prose row (a stem line touching it)."""
        ink=INK[pno]
        rt,_=ink.extent(ay,row_bottom)
        if rt is None:
            return None
        r=ink._r(rt); lo=ink._r(y_prev)
        while r>lo and ink.ink[r-1]>0:
            r-=1
        top=ink._p(r)
        if top<ay-25 or r<=lo:
            return None
        e=r-1
        while e>lo and ink.ink[e]==0:
            e-=1
        if r-1-e<3 or e<=lo:
            return None          # no white run of >= 3 px with content above it
        raised=[w for w in W[pno] if top-1<=(w[1]+w[3])/2<ay-2]
        if len([w for w in raised if re.search(r'[A-Za-z]{4,}',unicodedata.normalize('NFKC',w[4]))])>=2:
            return None
        return max(ink._p((e+r)//2),top-PAD_PT)
    def semantic_cut_before_anchor(pno,y_prev,anchor,owner_pair=None):
        """Separator between a known shared stem and its labelled child.

        Internal paragraph/diagram whitespace is not an ownership boundary.
        Use raw PDF content-flow block ids to include every fragmented maths
        block before the child's marker block, then compare the two semantic
        hulls.  If the hulls interleave vertically, register a 2-D seam.
        """
        token=f'({anchor["label"]})'
        page_words=W[pno]
        marker=[] if '_split_block' in anchor else [
            w for w in page_words if w[4]==token
            and abs(w[1]-anchor['y'])<4 and abs(w[0]-anchor['x'])<12]
        if '_split_block' in anchor:
            split_block=int(anchor['_split_block'])
            split_line=anchor.get('_split_line')
        elif marker:
            split_block=min(int(w[5]) for w in marker)
            split_line=min(int(w[6]) for w in marker
                           if int(w[5])==split_block)
        else:
            return boundary(pno,y_prev,anchor['y'],require_separation=True,
                            owner_pair=owner_pair,next_anchor=anchor)
        def aligned_child_mark(w):
            return ('_split_block' not in anchor and
                    bool(MARK_RE.match(w[4])) and w[1]>=anchor['y']-8)
        def answer_furniture(w):
            # Dotted answer leaders are text in many Cambridge PDFs; a mark
            # allocation printed on that same row is part of the same answer
            # furniture.  Neither owns mathematical content on either side
            # of a subpart boundary.
            on_dot=any(abs(dot_y-w[1])<5 for dot_y in DOT[pno])
            return on_dot and (bool(MARK_RE.match(w[4])) or
                               len(w[4])>6 and
                               sum(w[4].count(c) for c in '.·…') /
                               max(1,len(w[4]))>0.6)
        semantic_right=INK[pno].content_r
        crossing_grids=[]
        if IS_IGCSE:
            for drawing in doc[pno].get_drawings():
                rect=drawing.get('rect')
                if (rect and len(drawing.get('items',[]))>=8 and
                        rect.y0<anchor['y']<rect.y1):
                    crossing_grids.append(rect)
        def in_crossing_grid(w):
            cx=(w[0]+w[2])/2; cy=(w[1]+w[3])/2
            return any(rect.x0-2<=cx<=rect.x1+2 and
                       rect.y0-2<=cy<=rect.y1+2
                       for rect in crossing_grids)
        def is_upper_owner(w):
            # Cambridge table cells are frequently emitted after their part
            # marker in PDF block order even though they are visibly above
            # it.  That geometry override is valid only inside an actual
            # ruled grid.  Outside a grid, later PDF blocks can be a tall
            # child expression whose cap rises above its printed marker (for
            # example a matrix in 0580_s10_qp_21); assigning that cap to the
            # preceding owner creates a false semantic collision.
            bno=int(w[5])
            if in_crossing_grid(w):
                if w[3]<anchor['y']-10:
                    return True
                if w[1]>=anchor['y']-4:
                    return False
            if IS_ALEVEL and marker:
                # printed geometry beats PDF block order: the last stem line
                # can share the marker's block while the child's stacked
                # fractions come earlier ('where Q is ...' / '(a) A graph of
                # 1/V ...', 9702/52/F/M/17 Q2) -- that made both crops
                # contain both lines
                rt=min(m[1] for m in marker); rb=max(m[3] for m in marker)
                c=(w[1]+w[3])/2
                # a stacked fraction's numerator starts above the marker row
                # but reaches into it, right of the marker ('(i) volume of
                # water vapour / volume of ... water', 9702/02/M/J/07 Q3(c))
                if w[3]>rt+1.5 and w[1]<rb and w[0]>=max(m[2] for m in marker):
                    return False
                if c<rt-1 and w[3]<=rt+2:
                    return True
                if rt-1<=c<=rb and w[1]>=rt-10:
                    return False
            if bno!=split_block:
                return bno<split_block
            if split_line is not None:
                return int(w[6])<int(split_line)
            # Cambridge sometimes emits the final shared-stem line and the
            # first child marker in one PDF text block.  Compare their visual
            # row centres so a low subscript in the stem remains upper-owned
            # while the marker row remains lower-owned.
            return (w[1]+w[3])/2 < anchor['y']-3
        upper=[w for w in page_words if CONTENT_L<=w[0]<=semantic_right
               and is_upper_owner(w) and not aligned_child_mark(w)
               and not answer_furniture(w)
               and w[3]>y_prev-2 and w[1]<anchor['y']+20]
        lower=[w for w in page_words if CONTENT_L<=w[0]<=semantic_right
               and (not is_upper_owner(w) or aligned_child_mark(w))
               and not answer_furniture(w)
               and anchor['y']-35<w[1]<anchor['y']+50]
        if not upper or not lower:
            return boundary(pno,y_prev,anchor['y'],require_separation=True,
                            owner_pair=owner_pair,next_anchor=anchor)
        upper_bottom=max(w[3] for w in upper)
        lower_top=min(w[1] for w in lower)
        if os.environ.get('AL_DEBUG_SEM'):
            print('SEM',anchor.get('label'),'page',pno+1,'marker',bool(marker),'upper_bottom',round(upper_bottom,1),
                  'lower_top',round(lower_top,1),'lower_first',sorted(lower,key=lambda w:w[1])[:3],file=sys.stderr)
        # Images and vector diagrams are indivisible semantic objects.  Text
        # flow alone cannot see their lower edge: in M21 AA HL P3 an Argand
        # diagram occupies y=301..518 before part (a)(i), while the preceding
        # text ends around y=401.  A word-only hull therefore chose y=411 and
        # bisected the diagram.  Any graphic that begins in the proven upper
        # owner's interval and before the child marker extends that owner's
        # hull through its complete bounds.  If it truly overlaps the child,
        # the existing 2-D seam logic must prove a safe path or fail closed.
        page=doc[pno]
        upper_graphic_rects=[]
        def meaningful_body_overlap(rect):
            return (min(rect.x1,CONTENT_R-40)-max(rect.x0,CONTENT_L))>12
        def has_visible_rendered_ink(rect):
            """Reject PDF vector bboxes that render no visible object.

            Several legacy 0580 PDFs contain dark-stroke drawing records
            whose clipping state makes them completely invisible.  Their
            advertised rectangles can overlap the next child by 50+ points;
            treating those metadata boxes as diagrams creates a false owner
            collision.  Ownership is visual, so require rendered pixels in
            the advertised body before accepting a drawing rectangle.
            """
            ink=INK[pno]
            xa=max(0,min(ink.W-1,int((rect.x0-CONTENT_L)*SC)))
            xb=max(0,min(ink.W-1,int((rect.x1-CONTENT_L)*SC)+1))
            ya=ink._r(rect.y0); yb=ink._r(rect.y1)
            if xb<xa or yb<ya:
                return False
            visible=(ink.gray[ya:yb+1,xa:xb+1]<250).copy()
            # A stale/invisible drawing bbox may still enclose ordinary text;
            # page-level ink alone would then be a false proof that the
            # vector object rendered.  Remove extracted word glyph areas and
            # require non-text pixels attributable to the graphic itself.
            for word in page_words:
                wr=fitz.Rect(word[:4])
                if not wr.intersects(rect):
                    continue
                wx0=max(xa,min(xb,int((wr.x0-CONTENT_L)*SC)-2))
                wx1=max(xa,min(xb,int((wr.x1-CONTENT_L)*SC)+2))
                wy0=max(ya,min(yb,ink._r(wr.y0)-2))
                wy1=max(ya,min(yb,ink._r(wr.y1)+2))
                visible[wy0-ya:wy1-ya+1,wx0-xa:wx1-xa+1]=False
            rows,cols=np.where(visible)
            if not len(cols):
                return False
            # Ink from a different nearby object can fall inside a stale
            # bbox.  A drawing that truly rendered must occupy a meaningful
            # fraction of every non-trivial advertised dimension; a thin
            # accidental overlap at only one edge is not sufficient proof.
            span_x=(cols.max()-cols.min()+1)/SC
            span_y=(rows.max()-rows.min()+1)/SC
            if rect.width>4 and span_x<rect.width*0.25:
                return False
            if rect.height>4 and span_y<rect.height*0.25:
                return False
            return True
        seen_xrefs=set()
        for image in page.get_images(full=True):
            xref=image[0]
            if xref in seen_xrefs:
                continue
            seen_xrefs.add(xref)
            for rect in page.get_image_rects(xref):
                # Legacy ROOT19-stamped PDFs can carry a page-wide watermark
                # image that begins above the first child and extends almost
                # to the footer.  It is presentation furniture, not shared
                # mathematical context.  A true whole-page scan would not
                # also provide the text anchors required to reach this code.
                page_watermark=(
                    rect.x0<CONTENT_L-10 and rect.x1>CONTENT_R+10 and
                    rect.height>200
                )
                if (not page_watermark and meaningful_body_overlap(rect) and
                        rect.y0>=y_prev-8 and rect.y0<lower_top-8):
                    upper_graphic_rects.append(rect)
        for drawing in page.get_drawings():
            rect=drawing.get('rect')
            # A diagram frame is often exposed as four zero-thickness line
            # drawings rather than one enclosing rectangle, so either
            # dimension being substantial is enough to make it indivisible.
            child_inside_igcse_grid=bool(
                IS_IGCSE and rect and len(drawing.get('items',[]))>=8 and
                rect.y0<anchor['y']<rect.y1
            )
            fill=drawing.get('fill')
            blank_page_fill=(
                drawing.get('color') is None and fill is not None and
                all(channel>0.95 for channel in fill)
            )
            parts=[rect]
            if IS_ALEVEL and rect is not None and len(drawing.get('items',[]))>1:
                # one path holding several separate fraction bars (stem
                # '1/1600' plus the (i) and (ii) ratio bars, 9702/02/M/J/07
                # p.9): its union bbox is not a diagram -- judge each bar
                its=[]
                for it in drawing['items']:
                    if it[0]=='l' and abs(it[1].y-it[2].y)<1.5:
                        its.append(fitz.Rect(min(it[1].x,it[2].x),min(it[1].y,it[2].y)-0.3,
                                             max(it[1].x,it[2].x),max(it[1].y,it[2].y)+0.3))
                    elif it[0]=='re' and it[1].height<1.5:
                        its.append(fitz.Rect(it[1]))
                    else:
                        its=None; break
                if its:
                    parts=its
            for rect in parts:
                if (rect and not child_inside_igcse_grid and not blank_page_fill and
                        (rect.width>2 or rect.height>2) and
                        meaningful_body_overlap(rect) and
                        has_visible_rendered_ink(rect) and
                        rect.y0>=y_prev-8 and rect.y0<lower_top-8):
                    upper_graphic_rects.append(rect)
        if upper_graphic_rects:
            upper_bottom=max(upper_bottom,max(rect.y1 for rect in upper_graphic_rects))
            # Some official diagrams intentionally fade continuation rays to
            # white.  PDF vector extraction reports only the opaque core, and
            # the watermark-resistant `<190` profile then stops partway down
            # the visible ray.  Continue the *known graphic* through any
            # near-white pixels inside its horizontal body span, but never
            # search into the lower owner's earliest word.  Bounding this
            # softer scan to a proven graphic prevents printer-margin hatch
            # marks or page-wide pale furniture from extending a crop.
            ink=INK[pno]
            ra=ink._r(max(y_prev-2,upper_bottom-1))
            rb=ink._r(lower_top-1)
            if rb>=ra:
                columns=np.zeros(ink.W,dtype=bool)
                for rect in upper_graphic_rects:
                    xa=max(0,min(ink.W-1,int((rect.x0-CONTENT_L)*SC)-2))
                    xb=max(0,min(ink.W-1,int((rect.x1-CONTENT_L)*SC)+2))
                    if xb>=xa: columns[xa:xb+1]=True
                if np.any(columns):
                    # Extend only through pixels that remain connected to the
                    # known graphic.  Taking the last pale row anywhere in
                    # this interval can jump across whitespace into later
                    # text, answer furniture, or a watermark and falsely
                    # assign that unrelated content to the stem.
                    row_has=np.any(ink.gray[ra:rb+1,columns]<250,axis=1)
                    last=-1
                    blank_run=0
                    for offset,has_ink in enumerate(row_has):
                        if has_ink:
                            last=offset
                            blank_run=0
                        else:
                            blank_run+=1
                            if blank_run>4:
                                break
                    if last>=0:
                        upper_bottom=max(upper_bottom,ink._p(ra+last))
        # A few official maths glyphs are absent from PDF text extraction
        # (for example the denominator pi in a typeset fraction).  Follow
        # rendered ink a short distance below the extracted upper-owner hull,
        # but only in columns already occupied by that owner's PDF words.
        # This recovers the missing glyph without absorbing a raised formula
        # from the following part in a different horizontal region.
        ink=INK[pno]
        word_columns=np.zeros(ink.W,dtype=bool)
        for word in upper:
            xa=max(0,min(ink.W-1,int((word[0]-CONTENT_L)*SC)-2))
            xb=max(0,min(ink.W-1,int((word[2]-CONTENT_L)*SC)+2))
            if xb>=xa:
                word_columns[xa:xb+1]=True
        # Never follow rendered ink through columns already occupied by an
        # extracted lower-owner word.  Two tightly led prose rows can have
        # less than the generic four-pixel blank-run moat; without this
        # semantic column exclusion, the lower child's glyphs are mistaken
        # for a missing descender of the stem and manufacture a false 2-D
        # collision (0580_s05_qp_4 Q9(f) is the canonical case).
        lower_columns=np.zeros(ink.W,dtype=bool)
        for word in lower:
            xa=max(0,min(ink.W-1,int((word[0]-CONTENT_L)*SC)-3))
            xb=max(0,min(ink.W-1,int((word[2]-CONTENT_L)*SC)+3))
            if xb>=xa:
                lower_columns[xa:xb+1]=True
        word_columns &= ~lower_columns
        if np.any(word_columns):
            ra=ink._r(max(y_prev-2,upper_bottom-1))
            rb=ink._r(min(anchor['y']+28,FOOTER_Y))
            if rb>=ra:
                row_has=np.any(ink.gray[ra:rb+1,word_columns]<230,axis=1)
                last=-1
                blank_run=0
                for offset,has_ink in enumerate(row_has):
                    if has_ink:
                        last=offset
                        blank_run=0
                    else:
                        blank_run+=1
                        if blank_run>4:
                            break
                if last>=0:
                    upper_bottom=max(upper_bottom,ink._p(ra+last))
        cut=(upper_bottom+lower_top)/2
        if IS_ALEVEL and upper_bottom>=lower_top+3 and upper_bottom<lower_top+24:
            # interleaved stacked fractions ('... in 1/V. [2]' over '(c) (i)
            # Plot ... 1/V', 9702/51/O/N/18 Q2): the word hulls overlap by
            # several points yet fully blank pixel rows can still separate
            # the owners.  Cut there only when every upper word's centre is
            # above the cut and every lower word's centre below it.
            ink=INK[pno]; pale=(ink.gray<245).sum(axis=1)
            uwb=max(w[3] for w in upper)       # upper WORDS' bottom (before ink-following)
            lo,hi=ink._r(min(lower_top,uwb)-2),ink._r(upper_bottom+2)
            blank=[r for r in range(lo,hi+1) if pale[r]==0]
            if blank:
                mid=ink._r((min(uwb,upper_bottom)+lower_top)/2); r=min(blank,key=lambda r:abs(r-mid)); yc=ink._p(r)
                if (all((w[1]+w[3])/2<yc for w in upper) and
                        all((w[1]+w[3])/2>yc for w in lower if w[1]>=anchor['y']-12)):
                    return yc
        if IS_ALEVEL and upper_bottom>=lower_top-0.5 and upper_bottom<lower_top+3:
            # word BOXES touch, but the glyphs may still be separated by
            # fully blank pixel rows (box = line spacing): 'where Q ...' over
            # '(a) ... 1/V' in 9702/52/F/M/17 had a 0.0 pt box margin and an
            # 8 pt blank band.  Cut on the blank row nearest the midpoint
            # instead of building a 2-D seam.
            ink=INK[pno]; rows=ink.semantic.sum(axis=1)
            lo,hi=ink._r(upper_bottom-4),ink._r(lower_top+4)
            blank=[r for r in range(lo,hi+1) if rows[r]==0]
            if blank:
                mid=ink._r(cut)
                return ink._p(min(blank,key=lambda r:abs(r-mid)))
        if IS_MATHS and marker and upper_bottom>=lower_top-0.5:
            # a raised integral limit / superscript on the child's own row
            # ('(i) Use the substitution ... I = integral_1^2 ...', 9709/31/M/J/07
            # Q7) is a separate PDF block and was taken for stem content.  When
            # the ink block holding the marker row has a white run above it and
            # holds no prose row of its own, cut in that run instead of a 2-D seam.
            yc=maths_row_gap_cut(pno,anchor['y'],max(m[3] for m in marker),y_prev)
            if yc is not None:
                return yc
        if upper_bottom>=lower_top-0.5:
            # Limit the 2-D search to the actual semantic collision rather
            # than the entire preceding stem.  This makes the seam solve both
            # stricter and more stable for raised indices, tall brackets and
            # neighbouring formulae whose vertical hulls interleave.
            upper_graphic_regions=[]
            upper_graphic_word_regions=[]
            if upper_graphic_rects:
                upper_graphic_regions=[[
                    rect.x0-2,rect.y0-2,rect.x1+2,rect.y1+2,
                ] for rect in upper_graphic_rects]
                # Diagram vertex/axis labels are separate PDF text objects
                # and routinely sit just outside the vector drawing bbox.
                # Associate a local one-line halo with EACH diagram instead
                # of taking one union rectangle: a union over unrelated page
                # graphics can swallow a child prompt or answer row in the
                # whitespace between them.
                upper_graphic_word_regions=[[
                    max(CONTENT_L,rect.x0-100),rect.y0-14,
                    min(semantic_right,rect.x1+100),rect.y1+14,
                ] for rect in upper_graphic_rects]
            note_seam(pno,lower_top-2,upper_bottom+2,cut=cut,
                      next_anchor=anchor,owner_pair=owner_pair,
                      split_block=split_block,split_line=split_line,
                      upper_graphic_regions=upper_graphic_regions,
                      upper_graphic_word_regions=upper_graphic_word_regions)
        return cut
    def content_cap(pno,y_mark,ceil):     # tight bottom via rendered ink (watermark-immune)
        hi=min(ceil, first_stop(pno,y_mark), CONTENT_BOTTOM, FOOTER_Y)
        ink=INK[pno]; a=ink._r(y_mark); b=ink._r(hi)
        if b<=a: return y_mark
        rows=np.where(ink.ink[a:b+1]>=6)[0]
        return ink._p(a+rows[-1]) if len(rows) else y_mark
    def continued_floor(pno,before):
        """First content y below an official 'Question N continued' header."""
        rows={}
        for w in W[pno]: rows.setdefault(round(w[1]/3)*3,[]).append(w)
        floors=[]
        for ws in rows.values():
            txt=' '.join(w[4] for w in sorted(ws,key=lambda w:w[0]))
            if re.search(r'Question\s+\d+\s+continued',txt,re.I):
                floors.append(max(w[3] for w in ws)+8)
        return max(floors) if floors else HEADER_Y
    def continued_tail(pno,after):
        """Top y of official continuation footer, or the normal content cap."""
        rows={}
        for w in W[pno]: rows.setdefault(round(w[1]/3)*3,[]).append(w)
        tails=[]
        for ws in rows.values():
            txt=' '.join(w[4] for w in sorted(ws,key=lambda w:w[0]))
            if re.search(r'This question continues',txt,re.I):
                y=min(w[1] for w in ws)
                if y>after+2: tails.append(y)
        return min(tails) if tails else min(CONTENT_BOTTOM,FOOTER_Y)
    def segment_has_content(pno,y0,y1):
        if y1-y0<6: return False
        rt,rb=INK[pno].extent(y0,y1)
        return rt is not None and rb is not None and rb-rt>=1

    DOTS_RE=re.compile(r'^[.…]{3,}')
    # '1.' as well as '1': numbered blank answer lines ('1. ......',
    # 8w/41 Q1(c)) are not labelled answer lines
    # a bullet before a dotted line is a plain slot marker ('●  ......',
    # 9701/41/M/J/18 Q3(b)(i)), not a label
    PLAIN_TOKEN_RE=re.compile(r'^(\d{1,2}\.?|\[\d+\]|\(\w{1,4}\)|[.…,;:]+|[•●▪–-])$')
    def answer_rows(pno):
        """Dotted answer rows on a page: dicts y0/y1/labelled.

        Words within 6 pt of a dotted leader belong to its row (raised
        superscript units such as 's-1').  A row is 'labelled' when it
        carries a quantity/unit/label besides dots, numbers and marks, e.g.
        'speed = ...... m s-1 [2]'; plain '...... [1]' and numbered
        '1 ......' rows are not.  Rows inside a drawn table are excluded:
        dotted cells there are part of a table the candidate completes.
        """
        rows=[]
        # leaders only: a run of >=10 dots.  Short dotted blanks are inline
        # slots of a printed equation ('...... He + ...... beta', 9702/21/O/N/25)
        dots=[w for w in W[pno] if is_leader(w,W[pno])]
        # shared table geometry: genuine rect items + vertical rules, the
        # full-height examiner rule excluded (a compound path's page-sized
        # bbox made every leader a 'table cell', so 2006 Paper 5 working
        # lines were never trimmed -- 9702/05/M/J/06)
        geom=table_cells(doc[pno])
        for dw in dots:
            if dot_in_table(dw,geom):
                continue
            # the old 'For Examiner's Use' column header (x>515) shares rows
            # with the first answer slot; it is not a label (9702/22/M/J/10)
            ws=[w for w in W[pno] if (abs(w[1]-dw[1])<=6 or abs(w[3]-dw[3])<=6)
                and not (w[0]>515 and w[4] in ('For','Examiner’s',"Examiner's",'Use'))]
            y0=min(w[1] for w in ws); y1=max(w[3] for w in ws)
            if any(abs(r['line_y0']-y0)<4 for r in rows):
                continue
            line_y0=y0
            labelled=any(not PLAIN_TOKEN_RE.match(w[4]) for w in ws if not DOTS_RE.match(w[4]))
            # a short 'Label:' line set just above the row is its heading
            # ('oxidation number of Bi:' / 'in Bi2O3 .... in NaBiO3 ....',
            # 9701/22/F/M/24 Q1(c)(i)); analyse() already stops crops at it,
            # so it must travel with the row or it is lost
            above={}
            for w in W[pno]:
                if y0-30<w[1]<y0-3: above.setdefault(round(w[1]/3)*3,[]).append(w)
            if above:
                hw=sorted(above[max(above)],key=lambda w:w[0])
                ht=' '.join(w[4] for w in hw)
                if (ht.endswith(':') and len(ht)<=30 and len(ht.split())<=4 and hw[0][0]<=200
                        and y0-max(w[3] for w in hw)<12 and not any(DOTS_RE.match(w[4]) for w in hw)):
                    y0=min(w[1] for w in hw); labelled=True
            # a small drawn symbol in the row ('...... <=> ......', an equation
            # template whose arrow is vector art, 9701/41/O/N/17 Q2(b)(i)) makes
            # it a labelled row, extended over the symbol
            if pno not in SMALL_DRAW:
                allr=[fitz.Rect(d['rect']) for d in doc[pno].get_drawings() if d.get('rect') is not None]
                big=[r for r in allr if r.width>40 and r.height>40]
                # compact symbols only, never part of hatching (whose small
                # strokes overlap long ones: 9702/21/O/N/15 Q3(a))
                SMALL_DRAW[pno]=[r for r in allr if 2<r.width<=40 and r.height<=10
                                 and not any(b.intersects(r) for b in big)]
            for d_ in SMALL_DRAW[pno]:
                if d_.y1>y0-1 and d_.y0<y1 and d_.y0>y0-8 and min(v[0] for v in ws)-2<d_.x0 and d_.x1<max(v[2] for v in ws)+2:
                    labelled=True; y0=min(y0,d_.y0)
            # captions printed under the slots ('...... > ...... > ......' /
            # 'most basic   least basic', 9701/41/M/J/20 Q4(a)): a short line
            # just below, indented inside the row's leader span, is the row's
            leads=[v for v in W[pno] if abs(v[1]-dw[1])<=6 and is_leader(v,W[pno])]
            cap=[v for v in W[pno] if y1-4<=v[1]<=y1+8 and not DOTS_RE.match(v[4])]
            if (leads and cap and len(cap)<=4 and min(v[0] for v in cap)>min(v[0] for v in leads)+10
                    and max(v[2] for v in cap)<=max(v[2] for v in leads)+5
                    # words, not a fraction's letter ('q' over 'm' below a
                    # row: 9702/04/O/N/04, 9702/23/O/N/13)
                    and all(re.fullmatch(r'[A-Za-z][A-Za-z-]{2,}',v[4]) for v in cap)):
                y1=max(y1,max(v[3] for v in cap)); labelled=True
            rows.append({'y0':y0,'y1':y1,'labelled':labelled,'line_y0':line_y0})
        # A mark alone on its row (e.g. '[3]' under a blank working space)
        # is kept with its leaf like a labelled answer line.
        for w in W[pno]:
            if re.fullmatch(r'\[\d+\]',w[4]) and not any(
                    o is not w and abs(o[1]-w[1])<=4 for o in W[pno]):
                if not any(abs(r['y0']-w[1])<4 for r in rows):
                    rows.append({'y0':w[1],'y1':w[3],'labelled':True,'line_y0':w[1]})
        return sorted(rows,key=lambda r:r['y0'])

    def whitespace_bounds(p,y0,y1,reach=8.0):
        """Grow [y0,y1] outward to the nearest fully blank pixel rows.

        Uses the strict (antialias-aware) ink projection, so a thin segment
        never starts inside the descenders of the line above -- a fixed 3 pt
        pad took a sliver of the 'g' in 'Fig. 6.2' (9702/42/M/J/24 Q6(b)(iii)).
        """
        ink=INK[p]; rows=ink.semantic.sum(axis=1)
        y1=min(y1,FOOTER_Y-1)        # never start the downward search inside the footer
        top=ink._r(y0)-1; lim=ink._r(y0-reach)
        while top>lim and rows[top]>0: top-=1
        bot=ink._r(y1)+1; lim=ink._r(y1+reach)
        while bot<lim and rows[bot]>0: bot+=1
        if rows[top]>0 or rows[bot]>0:
            # word boxes include line spacing, so a tightly set row's box edge
            # can already sit inside the NEXT line's glyphs (9702/21/M/J/18
            # 'phase difference = ... [1]' over '(iii) Calculate ...').  Scan
            # outward from inside the row itself (just below its middle, always
            # within its glyphs) to the first blank pixel row on each side.
            # (stricter blank test here: rows of a tightly set neighbour can
            # carry an antialias halo between 230 and 245 that shows in the
            # rendered crop -- '[2]' bracket feet atop 9702/52/F/M/17 (d)(ii))
            pale=(ink.gray<245).sum(axis=1)
            mid=ink._r(y0+0.6*(y1-y0))
            t3=mid
            while t3>ink._r(y0-reach) and pale[t3]>0: t3-=1
            b3=mid
            while b3<ink._r(y1+reach) and pale[b3]>0: b3+=1
            if pale[t3]==0 and pale[b3]==0 and t3<mid<b3:
                return ink._p(t3),ink._p(b3)
        if rows[top]>0 or rows[bot]>0:
            # no fully blank row: accept the faintest row only if it holds no
            # DARK pixel (the gate's slice threshold) -- antialias halo only
            dark=ink.dark.sum(axis=1)
            def faint(a,b):
                band=range(min(a,b),max(a,b)+1)
                best=min(band,key=lambda r:(dark[r],rows[r]))
                return best if dark[best]==0 else None
            if rows[top]>0:
                t2=faint(ink._r(y0-reach),ink._r(y0)-1)
                if t2 is None:
                    if os.environ.get('AL_DRAFT'):
                        print(f'DRAFT: no whitespace around answer row at y={y0:.1f} on page {p+1}',file=sys.stderr)
                        return y0,y1
                    raise RuntimeError(f'REVIEW_REQUIRED: no whitespace around answer row at y={y0:.1f} on page {p+1}')
                top=t2
            if rows[bot]>0:
                b2=faint(ink._r(y1)+1,ink._r(y1+reach))
                if b2 is None:
                    if os.environ.get('AL_DRAFT'):
                        print(f'DRAFT: no whitespace around answer row at y={y0:.1f} on page {p+1}',file=sys.stderr)
                        return y0,y1
                    raise RuntimeError(f'REVIEW_REQUIRED: no whitespace around answer row at y={y0:.1f} on page {p+1}')
                bot=b2
        return ink._p(top),ink._p(bot)

    def band_between_rows(p,b0,b1,lo,hi):
        """Fallback bounds for prompt text that cannot be cut out thinly (its
        words are labels inside a drawn figure/table: 'copper  manganese',
        9701/51/M/J/19): the whole band between the answer rows around it,
        tightened to ink.  Raises when even that band has no blank edge."""
        a=max([lo]+[r['y1'] for r in AR_CACHE[p] if r['y1']<=b0+1])+1
        b=min([hi]+[r['y0'] for r in AR_CACHE[p] if r['y0']>=b1-1])-1
        ink=INK[p]; rows=ink.semantic.sum(axis=1)
        ra,rb_=ink._r(a),ink._r(b)
        while ra<rb_ and rows[ra]>0: ra+=1       # snap INWARD to blank rows
        while rb_>ra and rows[rb_]>0: rb_-=1
        if rb_-ra<2 or ink.extent(ink._p(ra),ink._p(rb_))[0] is None:
            raise RuntimeError(f'REVIEW_REQUIRED: no whitespace around answer row at y={b0:.1f} on page {p+1}')
        return ink._p(ra),ink._p(rb_)

    def alevel_answer_rows(emits):
        """Decision D6 (2026-10-10): question text + labelled answer line(s).

        For every leaf: (1) end each of its segments before an answer area
        that sits at the bottom of the segment (only answer rows / marks /
        blank space below the cut); (2) append, as thin extra segments, the
        labelled answer rows between the leaf and the next emitted item
        ('quantity = ...... unit [n]'), so the expected unit and marks stay
        visible while blank working space and plain dotted lines are dropped.
        """
        AR={p:answer_rows(p) for p in range(doc.page_count)}
        AR_CACHE.clear(); AR_CACHE.update(AR)
        out=[list(e) for e in emits]
        order=sorted(range(len(out)),key=lambda i:(out[i][1],out[i][2]))
        first_seg={}
        for i in order:
            first_seg.setdefault(out[i][0],i)
        def row_words_below(pno,y,ylim):
            return [w for w in W[pno] if y<=w[1]<ylim]
        # (0) a leaf (or stem) must not START with the previous item's mark:
        # '[2]' printed under (d)(i)'s last answer line was the first row of
        # (d)(ii) (9702/52/F/M/17 Q2).  Move the top below any leading
        # mark-only rows; step (2) then gives the mark to the item above.
        for lab in dict.fromkeys(e[0] for e in out):
            i=first_seg[lab]; _,pno,y0,y1=out[i]
            rows={}
            for w in W[pno]:
                # words whose CENTRE is inside the segment (the '[2]' box
                # started 2.5 pt above (d)(ii)'s top yet its glyphs were inside)
                if y0<(w[1]+w[3])/2<y1: rows.setdefault(round(w[1]/3)*3,[]).append(w)
            new_top=None
            for _,ws in sorted(rows.items()):
                # also the previous item's plain '...... [1]' row: a context
                # paragraph before '(iii)' made (iii) start at the stop row
                # above it (9701/42/F/M/19 Q4(c)(iii))
                if all(MARK_RE.match(w[4]) or DOTS_RE.match(w[4]) for w in ws):
                    try:
                        new_top=whitespace_bounds(pno,min(w[1] for w in ws),max(w[3] for w in ws))[1]
                    except RuntimeError:
                        # the mark's glyphs touch this item's first line (no
                        # blank pixel row): white the mark out instead -- it
                        # is the previous item's and must not show here
                        for w in ws:
                            response_furniture_masks.setdefault(pno,{})[('leadmark',round(w[0],1),round(w[1],1))]=\
                                fitz.Rect(w[:4])+(-1,-0.5,1,0.5)
                    continue
                break
            if new_top is not None and new_top<y1-4:
                out[i][2]=new_top
        added=[]; hugged=set()
        leaves=[lab for lab in dict.fromkeys(e[0] for e in out) if not lab.endswith('.stem')]
        for lab in leaves:
            segs=[i for i in order if out[i][0]==lab]
            # (1) trim a trailing answer area out of each prompt segment
            for i in segs:
                _,pno,y0,y1=out[i]
                inside=[r for r in AR[pno] if y0+8<r['y0']<y1]
                # cut at the FIRST answer row below which only answer rows /
                # marks / blank space remain (a region can start above the
                # leaf and contain the previous item's dotted rows: 9702/04/
                # O/N/08 Q10(a)(ii), whose working space then survived)
                for row in inside:
                    cut=row['y0']
                    below=[w for w in row_words_below(pno,cut-1,y1)
                           if not DOTS_RE.match(w[4]) and not any(r['y0']-1<=w[1]<=r['y1']+1 for r in AR[pno])
                           and not re.fullmatch(r'\[Turn|over|©|UCLES|\d{4}|\d{4}/\d+/.*|BLANK|PAGE|\[Total:?|:|\d+\]',w[4])]
                    if os.environ.get('AL_DEBUG_ROWS') and os.environ['AL_DEBUG_ROWS'] in lab:
                        print('TRIM',lab,'cut',round(cut,1),'below',[(round(w[1]),w[4][:10]) for w in below][:8],file=sys.stderr)
                    if not below:
                        out[i][3]=cut-2
                        break
            # (2) labelled answer rows between each of this leaf's segments and
            # the next crop: a mark printed after an EARLIER segment was lost when
            # the leaf continued on a later page (9701/52/F/M/19 Q1(e)(ii): '[2]'
            # under its bullets, then its grid page)
            last_seg=max(segs,key=lambda i:(out[i][1],out[i][3]))
            for last in sorted(segs,key=lambda i:(out[i][1],out[i][2])):
                lpno,ly1=out[last][1],out[last][3]
                # Maths: the next question's window can open above this leaf's
                # provisional end (raised first row) -- it still comes next, so its
                # '[2]' must not be read as this leaf's row (9709/11/M/J/08 Q1/Q2(i))
                after=(lpno,out[last][2]) if IS_MATHS else (lpno,ly1-1)
                later=[i for i in order if (out[i][1],out[i][2])>after and (out[i][0]!=lab if last==last_seg else i!=last)]
                npno,ny0=(out[later[0]][1],out[later[0]][2]) if later else (doc.page_count-1,FOOTER_Y)
                dbg=os.environ.get('AL_DEBUG_ROWS')
                if dbg and dbg in lab:
                    print('ROWS',lab,'last',out[last],'next',(npno,ny0),
                          {p:AR[p] for p in range(lpno,npno+1)},file=sys.stderr)
                # (2b)/(2c) only after the leaf's LAST segment: after an earlier
                # one they re-added rows its later segment already holds
                # (9701/51/O/N/10 Q1(b) showed its graph prompt twice)
                if last==last_seg:
                    # (2b) prompt text interleaved with this leaf's own answer rows on
                    # the same page: '* the intensity ...' / ...... / '* the total
                    # power ...' / ...... / [3] (9702/22/M/J/23 Q7(b)(ii)).  The
                    # leaf ended at its first dotted row; keep every later prompt row
                    # (dotted rows dropped) when the leaf's own mark lies below them.
                    for pp in range(lpno,npno+1):
                        lo0=ly1 if pp==lpno else HEADER_Y
                        hi0=ny0 if pp==npno else FOOTER_Y
                        mark_ys=[w[1] for w in W[pp] if lo0<w[1]<hi0 and MARK_RE.match(w[4])]
                        if not mark_ys:
                            if [w for w in W[pp] if lo0<w[1]<hi0 and not DOTS_RE.match(w[4])
                                    and not any(r['y0']-1<=w[1]<=r['y1']+1 for r in AR[pp])]:
                                break               # unrelated content, no mark: not interleaved
                            continue                # only answer rows: look on the next page
                        mark_y=min(mark_ys)
                        prow={}
                        for w in W[pp]:
                            if not (lo0+1<w[1]<mark_y-2) or DOTS_RE.match(w[4]) or MARK_RE.match(w[4]):
                                continue
                            if any(r['y0']-1<=w[1]<=r['y1']+1 for r in AR[pp]):
                                continue
                            prow.setdefault(round(w[1]/3)*3,[]).append(w)
                        blocks2=[]
                        for _,ws_ in sorted(prow.items()):
                            if all(PLAIN_TOKEN_RE.match(w[4]) for w in ws_):
                                continue            # bare slot numbers '1.' / '2.'
                            y0_,y1_=min(w[1] for w in ws_),max(w[3] for w in ws_)
                            between=[r for r in AR[pp] if (blocks2[-1][1] if blocks2 else y0_)<r['y0']<y0_]
                            if blocks2 and y0_-blocks2[-1][1]<20 and not between:
                                blocks2[-1][1]=max(blocks2[-1][1],y1_)
                            else:
                                blocks2.append([y0_,y1_])
                        got=[]
                        for b0,b1 in blocks2:
                            try:
                                got.append(whitespace_bounds(pp,b0,b1))
                            except RuntimeError:
                                got.append(band_between_rows(pp,b0,b1,lo0,mark_y-2))
                        # a fallback band absorbs the thin slices inside it
                        # (9701/51/O/N/10 Q1(b) held its graph prompt twice)
                        for g in got:
                            if not any(h is not g and h[0]-0.5<=g[0] and g[1]<=h[1]+0.5 and (h[1]-h[0])>(g[1]-g[0])
                                       for h in got):
                                added.append((lab,pp)+tuple(g))
                        break                       # the leaf's own mark ends it
                    # (2c) the figure caption printed just under the leaf's mark
                    # ('... [3]' / 'Fig. 4.4', 9702/23/O/N/19 Q4(b)(ii)): a lone
                    # 'Fig. N.N' / 'Table N.N' row within 20 pt below the leaf
                    hi_c=ny0 if npno==lpno else FOOTER_Y
                    caprow={}
                    for w in W[lpno]:
                        if ly1-2<w[1]<min(ly1+20,hi_c-2):
                            caprow.setdefault(round(w[1]/3)*3,[]).append(w)
                    for _,ws_ in sorted(caprow.items()):
                        ws_=[v for v in ws_ if not MARK_RE.match(v[4])]
                        if not ws_:
                            continue                # the leaf's own '[3]' row
                        txt=' '.join(v[4] for v in sorted(ws_,key=lambda v:v[0]))
                        if re.fullmatch(r'(?:Fig\.|Table)\s*\d+\.\d+',txt):
                            added.append((lab,lpno)+whitespace_bounds(lpno,min(v[1] for v in ws_),max(v[3] for v in ws_)))
                        break
                for p in range(lpno,npno+1):
                    lo=ly1-1 if p==lpno else HEADER_Y
                    hi=ny0 if p==npno else FOOTER_Y
                    # merge answer rows closer than 8 pt into one block: a mark on
                    # its own row 2-4 pt under the last labelled line has no blank
                    # pixel row between them (9702/22/O/N/21 'number of b- particles
                    # = ..... / [2]').  Plain rows inside a block join it.
                    # word boxes include line spacing: a row whose box overlaps the
                    # footer box by a point or two still has its glyphs above it
                    # only LABELLED rows / lone marks are kept or merged; a plain
                    # dotted row ('2. ......') must never ride along with a mark
                    # (9702/22/F/M/20 Q1(a) showed '2. ....' above its '[2]')
                    cand=[r for r in AR[p] if lo<=r['y0'] and r['y0']<hi-4 and r['labelled']]
                    blocks=[]
                    def touching(a,b):
                        # no fully blank pixel row between the two rows
                        ink=INK[p]; rows=ink.semantic.sum(axis=1)
                        lo_r,hi_r=ink._r(a['y1']),ink._r(b['y0'])
                        return hi_r<=lo_r or not (rows[lo_r:hi_r+1]==0).any()
                    for r in cand:
                        if blocks and r['y0']-blocks[-1]['y1']<20 and touching(blocks[-1],r):
                            blocks[-1]={'y0':blocks[-1]['y0'],'y1':max(blocks[-1]['y1'],r['y1']),
                                        'labelled':blocks[-1]['labelled'] or r['labelled']}
                        else:
                            blocks.append(dict(r))
                    for r in blocks:
                        if r['labelled'] and lo<=r['y0'] and r['y0']<hi-4:
                            ink_bottom=(INK[p].extent(out[last][2],min(out[last][3],r['y0']-0.5))[1]
                                        if p==lpno else None)
                            if ink_bottom is not None and r['y0']-ink_bottom<=6:
                                # hugging the leaf's own content (e.g. '[2]' right
                                # under its table, 22/M/J/24 p.16): extend the
                                # crop; final edges are snapped to blank rows
                                out[last][3]=max(out[last][3],r['y1']+1)
                                hugged.add(last)
                                continue
                            try:
                                added.append((lab,p)+whitespace_bounds(p,r['y0'],r['y1']))
                            except RuntimeError:
                                rw=[w for w in W[p] if r['y0']-1<=w[1]<=r['y1']+1]
                                if rw and all(MARK_RE.match(w[4]) for w in rw):
                                    continue    # a lone [n] fused to a plain dotted row: leave it out
                                # a merged block (labelled row + its mark) that
                                # cannot be bounded: retry row by row, leaving out
                                # a lone mark that touches the next item's text
                                # (9702/52/F/M/17 Q2(d)(i) '[2]' over '(ii)')
                                parts=[q for q in cand if r['y0']<=q['y0'] and q['y1']<=r['y1']+0.5]
                                if len(parts)<2:
                                    # a labelled row beside a drawing ('(i) methylbenzene
                                    # <ring> ......', 9701/42/M/J/13 Q6(a)): reach past it
                                    added.append((lab,p)+whitespace_bounds(p,r['y0'],r['y1'],reach=48.0))
                                    continue
                                for q in parts:
                                    try:
                                        added.append((lab,p)+whitespace_bounds(p,q['y0'],q['y1']))
                                    except RuntimeError:
                                        qw=[w for w in W[p] if q['y0']-1<=w[1]<=q['y1']+1]
                                        if not (qw and all(MARK_RE.match(w[4]) for w in qw)):
                                            raise
                    # (2d) the leaf's mark printed at the end of a PLAIN dotted
                    # row ('.......... [2]', after the fused-mark split): D6
                    # keeps the mark, so keep the row with its dots and slot
                    # number whited out (9701/21/M/J/07 Q1(b) lost its [3])
                    kept=[a for a in added if a[0]==lab and a[1]==p]
                    for r in AR[p]:
                        if r['labelled'] or not (lo<=r['y0'] and r['y0']<hi):
                            continue
                        rw=[w for w in W[p] if r['y0']-1<=w[1]<=r['y1']+1 and 38<=w[0] and w[2]<=562
                            and not re.fullmatch(r'\[Turn|over|©|UCLES|\d{4}|\d{4}/\d+/.*',w[4])
                            # the 'For Examiner's Use' margin column (9702/21/O/N/10 p.8)
                            and not (w[0]>520 and re.fullmatch(r"For|Examiner.?s|Use|Examiner.?s\s+Use",w[4]))]
                        mk=[w for w in rw if MARK_RE.match(w[4])]
                        if not mk or any(not (MARK_RE.match(w[4]) or DOTS_RE.match(w[4]) or PLAIN_TOKEN_RE.match(w[4]))
                                         for w in rw):
                            continue
                        if any(a[2]-0.5<=r['y0'] and r['y1']<=a[3]+0.5 for a in kept):
                            continue
                        # the mark already shows in one of the leaf's segments
                        # (a segment extended over it, 9701/41/M/J/18 Q3(b)(i))
                        mcy=[(m[1]+m[3])/2 for m in mk]
                        if all(any(o[0]==lab and o[1]==p and o[2]<=cy<=o[3] for o in out+kept) for cy in mcy):
                            continue
                        dots_=[w for w in rw if not MARK_RE.match(w[4])]
                        same_line=any(m[1]<w[3]-3 and w[1]<m[3]-3 for m in mk for w in dots_)
                        # a mark set on the line BELOW the dots: take its line only
                        ry0,ry1=((min(w[1] for w in rw),max(w[3] for w in rw)) if same_line
                                 else (min(m[1] for m in mk),max(m[3] for m in mk)))
                        try:
                            b=whitespace_bounds(p,ry0,ry1)
                        except RuntimeError:
                            # no blank pixel row (the row touches '[Turn over',
                            # 9701/52/F/M/24 p.3): the row's own word boxes;
                            # the coverage gate checks the cut for slices
                            b=(ry0-1.0,ry1+1.0)
                        for w in rw:
                            if MARK_RE.match(w[4]) or w[3]<=b[0] or w[1]>=b[1]:
                                continue
                            # stop short of a mark on the SAME line only (a mark
                            # set on the line below sits under the dots' end,
                            # 9701/22/F/M/17 Q1(b)(ii))
                            same=[m for m in mk if m[1]<w[3]-3 and w[1]<m[3]-3 and m[0]>w[0]]
                            x1=min([w[2]+0.5]+[m[0]-0.3 for m in same])
                            rect=fitz.Rect(w[0]-0.5,w[1]-0.5,x1,w[3]+0.5)
                            response_furniture_masks.setdefault(p,{})[('slotdots',round(w[0],1),round(w[1],1))]=rect
                            DOT_MASKS.append([p+1,round(rect.x0,2),round(rect.y0,2),round(rect.x1,2),round(rect.y1,2)])
                        added.append((lab,p)+b)
                        kept.append((lab,p)+b)
        AL_BYPASS.update((a[0],a[1],round(a[2],3),round(a[3],3)) for a in added)
        for i in hugged:
            e=out[i]; AL_BYPASS.add((e[0],e[1],round(e[2],3),round(e[3],3)))
        # (3) explicit working space INSIDE a leaf: 'Use the space (below) for
        # any working' followed by blank space and then the table/graph to be
        # completed (9702/22/O/N/25 Q1(a), 9702/42/O/N/24 Q7(c)(i)).  D6 drops
        # working space, so cut the blank band out by splitting the segment:
        # the prompt part ends just under the instruction line and the
        # scaffold part starts just above the scaffold's first ink.
        WORK_RE=re.compile(r'Use the space (?:below )?for (?:any )?working',re.I)
        split=[]
        for i,e in enumerate(out):
            lab,pno,y0,y1=e
            if lab.endswith('.stem'):
                continue
            rows={}
            for w in W[pno]:
                if y0<=w[1]<y1: rows.setdefault(round(w[1]/3)*3,[]).append(w)
            hit=None
            for _,ws in sorted(rows.items()):
                ws.sort(key=lambda w:w[0])
                if WORK_RE.search(' '.join(w[4] for w in ws)):
                    hit=max(w[3] for w in ws)
            if hit is None:
                continue
            ink=INK[pno]; sem=ink.semantic.sum(axis=1)
            a,b=ink._r(hit+1),ink._r(y1)
            nz=np.nonzero(sem[a:b+1])[0]
            if len(nz)==0:
                continue                    # nothing after the gap: (1) handles it
            gap_end=ink._p(a+nz[0])         # first ink below the instruction
            words_in_gap=[w for w in W[pno] if hit+1<=w[1]<gap_end-1]
            if gap_end-hit<40 or words_in_gap:
                continue
            split.append((i,[(lab,pno,y0,hit+PAD_PT),(lab,pno,gap_end-PAD_PT,y1)]))
        # (4) plain dotted answer rows INSIDE a leaf segment with more prompt
        # text below them ('* the number of protons' / ...... / '* the number
        # of neutrons.' / ...... / [2], 9702/22/M/J/23 Q8(a)(i)).  Dotted rows
        # are stop rows, so the later stop clamp would cut the leaf at the
        # first one and drop the rest of its prompt.  Split the segment into
        # prompt pieces with the plain rows removed.
        done={i for i,_ in split}
        for i,e in enumerate(out):
            lab,pno,y0,y1=e
            if i in done or lab.endswith('.stem'):
                continue
            # only rows with a dotted LEADER are stop rows (the clamp's
            # trigger); a lone '[4]' above 'Fig. 10.2' is not -- splitting
            # there only moved the caption (9702/41/M/J/07 Q10(a))
            def has_leader(r):
                return any(is_leader(w,W[pno]) for w in W[pno] if r['y0']-1<=w[1]<=r['y1']+1)
            inner=[r for r in AR[pno] if y0+8<r['y0'] and r['y1']<y1+2 and has_leader(r)]
            plain=[r for r in inner if not r['labelled']]
            labelled=[r for r in inner if r['labelled']]
            if not inner:
                continue
            def is_prompt(w):
                return (not DOTS_RE.match(w[4]) and not MARK_RE.match(w[4])
                        and not any(r['y0']-1<=w[1]<=r['y1']+1 for r in AR[pno]))
            first=min(r['y0'] for r in inner)
            if not [w for w in W[pno] if first<w[1]<y1 and is_prompt(w)
                    and not PLAIN_TOKEN_RE.match(w[4])]:
                continue                    # only answer material below: (1) handles it
            # labelled rows inside ('relative speed of approach = .... m s-1'
            # between two numbered tasks sharing one mark, 9702/21/O/N/18
            # Q2(b)(i)) are kept as their own pieces; plain rows are dropped
            cuts=sorted((r['y0'],r['y1']) for r in inner)
            pieces=[]; top=y0
            for c0,c1 in cuts:
                if c0>top:
                    pieces.append((top,c0-1))
                top=max(top,c1+1)
            if top<y1:
                pieces.append((top,y1))
            segs_=[]
            for a_,b_ in pieces:
                ws_=[w for w in W[pno] if a_<=w[1]<b_ and is_prompt(w) and not PLAIN_TOKEN_RE.match(w[4])]
                has_ink=INK[pno].extent(a_,b_)[0] is not None
                if a_==y0 or ws_ or (has_ink and not [w for w in W[pno] if a_<=w[1]<b_]):
                    if a_!=y0 and ws_:
                        try:
                            a_,b_=whitespace_bounds(pno,min(w[1] for w in ws_),max(w[3] for w in ws_))
                        except RuntimeError:
                            a_,b_=band_between_rows(pno,min(w[1] for w in ws_),max(w[3] for w in ws_),a_,b_)
                    segs_.append((lab,pno,a_,b_))
            for r in labelled:
                segs_.append((lab,pno)+whitespace_bounds(pno,r['y0'],r['y1']))
            segs_.sort(key=lambda t:t[2])
            if len(segs_)>1:
                split.append((i,segs_))
        for i,pieces_ in sorted(split,key=lambda t:-t[0]):
            out[i:i+1]=[list(x) for x in pieces_]
            for e in pieces_:               # the stop clamp would drop the instruction line / later prompt rows
                AL_BYPASS.add((e[0],e[1],round(e[2],3),round(e[3],3)))
        added.sort(key=lambda a:(a[1],a[2]))     # page order within each leaf
        # keep each leaf's appended rows right after its last emitted segment
        final=[]
        last_index={lab:max(i for i,e in enumerate(out) if e[0]==lab) for lab in leaves}
        for i,e in enumerate(out):
            final.append(tuple(e))
            for a in added:
                if a[0]==e[0] and last_index.get(e[0])==i:
                    final.append(a)
        # a leaf's pieces in reading order (page, y): a mark appended after an
        # earlier segment must not follow the leaf's later grid page
        for lab in leaves:
            idx=[i for i,e in enumerate(final) if e[0]==lab]
            for i,e in zip(idx,sorted((final[i] for i in idx),key=lambda e:(e[1],e[2]))):
                final[i]=e
        return final

    SCAFFOLD_PROMPT_RE=re.compile(
        r'\b(?:plot|draw|sketch|complete|mark|label|shade)\b.{0,80}?'
        r'\b(?:graph|grid|axes|fig(?:ure)?\.?|diagram|chart)\b',re.I|re.S)
    ANSWER_AREA_LABEL_RE=re.compile(r'^(?:Diagram|Working|Answer)\.?:?$',re.I)
    ORPHAN_FURNITURE_RE=re.compile(r'^(?:\[Turn over|BLANK PAGE|Please turn over.*|Turn over for (?:[Qq]uestion|Section) \S+|Section [A-C]|'
                                   r'For Examiner.s Use|Answer all (?:the )?questions.*|.*BLANK PAGE.*|'
                                   r'.*\b(?:is|starts|begins|continues) on (?:the )?(?:next|following|opposite) page.*|'
                                   # 'Question 3 starts on page 6.' on a deliberately empty page (9700/42/M/J/24 p.5)
                                   r'(?:Question|Section|Option) \S+ (?:starts|begins|continues) on page \d+\.?|'
                                   r'Turn over to page \d+ for the next question\.?|'
                                   # '[Question 7 is printed on the next page.]', '[Questions 8, 9 and 10
                                   # are printed overleaf.]' (9709/51/M/J/11, 9709/41/M/J/10)
                                   r'\[?Questions? \d+(?:(?:,| and) \d+)* (?:is|are) printed (?:on the next page|overleaf)\.?\]?|'
                                   # Biology Paper 6 option titles (9700/06/O/N/06) and Section B rubric (9700/42/M/J/13)
                                   r'OPTION \d+\s*[\u2013-]\s*[A-Z][A-Z ,&-]+|'
                                   r'Answer (?:one|two|either|both|all) (?:of the )?(?:following )?questions?\.?|'
                                   # pre-2009 9701 Paper 6 option titles + rubric, Paper 4 'Section B - Applications of Chemistry'
                                   r'It is recommended that you spend.*|'
                                   r'(?:You may )?use the space (?:below )?for (?:any )?working\.?|'
                                   r'BIOCHEMISTRY|ENVIRONMENTAL CHEMISTRY|PHASE EQUILIBRIA|SPECTROSCOPY|TRANSITION ELEMENTS|'
                                   r'(?:If you attempt this option, )?answer (?:both|all) questions on (?:the paper provided|two of the Options)\.?|'
                                   r'Section [A-C] [\u2013-] .+)$',re.I)
    def alevel_orphan_pages(emits):
        """A Level: label-less pages that lie between crops.

        Paper 5 prints the plotting grid on its own page after the prompts
        that use it (9702/52/M/J/24 p.7, after Q2(c)(i) 'Plot a graph of
        lg T against lg L ...').  The engine assigns content by labels, so
        such a page belonged to no crop.  Rules:
          * pure answer space (answer rows, a lone 'Diagram'/'Working'
            heading, blank space) is furniture: ignored;
          * a graphic page (grid/figure, little prose) joins the nearest
            preceding leaf of the same question whose prompt asks to
            plot/draw/sketch/complete on a graph/grid/figure (IGCSE rule:
            a graph belongs to the leaf that asks the candidate to draw on
            it; later leaves using it are dependencies, not stems);
          * anything else -> REVIEW_REQUIRED (never guessed).
        """
        pages_with={e[1] for e in emits}
        if not pages_with:
            return emits
        out=list(emits)
        REF_PAGE_RE=re.compile(r'Important values, constants and standards|The Periodic Table|oganesson|'
                               r'Centre Number|Candidate Number|Additional Page|lined page',re.I)
        def notice_top(p):
            ws=W[p]
            tops=[w[1] for w in ws if (w[4]=='Permission' and any(v[4]=='reproduce' and abs(v[1]-w[1])<3 for v in ws))
                  or (w[4]=='Every' and any(v[4]=='reasonable' and abs(v[1]-w[1])<3 for v in ws))
                  or w[4]=='Acknowledgements:'
                  # map disclaimer above the notice (9700/22/M/J/24 p.16)
                  or (w[4]=='boundaries' and any(v[4]=='designations' and 0<=v[1]-w[1]<14 for v in ws))
                  # 'University of Cambridge International Examinations is part
                  # of ... Syndicate' / 'Cambridge ... is part of ...' notices
                  or (w[1]>600 and w[4] in ('University','Cambridge') and any(
                      v[4] in ('Syndicate','part') and abs(v[1]-w[1])<14 for v in ws))]
            return min(tops) if tops else page_cap
        last_crop_page=max(pages_with)
        # pages AFTER the last crop too: a trailing figure page (9701/22/F/M/17
        # p.15, infra-red spectra X, Y, Z for the last leaf Q3(d)(ii))
        for p in range(min(pages_with)+1,doc.page_count):
            if p in pages_with or not segment_has_content(p,HEADER_Y,page_cap):
                continue
            if REF_PAGE_RE.search(doc[p].get_text()):
                continue        # data page inside the paper (9701/22/F/M/25 p.11)
            if p>last_crop_page:
                # trailing page: reference pages are furniture; anything else
                # above the copyright notice is content -- '... Use the data
                # given on page 12' (9701/51/M/J/14 Q1(e)) or a figure page
                if REF_PAGE_RE.search(doc[p].get_text()):
                    continue
                cap_=notice_top(p)
                foot_=[w[1] for w in W[p] if w[4] in ('©','UCLES') and w[1]>700]
                body_=[w for w in W[p] if HEADER_Y+10<=w[1]<cap_-1 and re.search(r'[A-Za-z]{3,}',w[4])
                       and not any(abs(w[1]-y)<5 for y in foot_)
                       and not ORPHAN_FURNITURE_RE.match(w[4]) and w[4] not in ('BLANK','PAGE')]
                if len(body_)<4:
                    continue
                before_=[e for e in out if e[1]<p and not e[0].endswith('.stem')]
                named=[e for e in before_ if re.search(rf'\bpage\s+{p+1}\b',
                       ' '.join(w[4] for w in W[e[1]] if e[2]-1<=w[1]<=e[3]))]
                owner_=(named[0] if named else max(before_,key=lambda e:(e[1],e[3])))[0]
                rt_,rb_=INK[p].extent(HEADER_Y,cap_-2)
                if rt_ is not None:
                    out.append((owner_,p,rt_-2,rb_+2))
                continue
            ar=answer_rows(p)
            def in_ar(w):
                return any(r['y0']-1<=w[1]<=r['y1']+1 for r in ar)
            content=[w for w in W[p] if not DOTS_RE.match(w[4]) and not in_ar(w)]
            per_row={}
            for w in content:
                per_row.setdefault(round(w[1]/3),[]).append(w)
            content=[w for w in content
                     if not (len(per_row[round(w[1]/3)])==1 and ANSWER_AREA_LABEL_RE.match(w[4]))
                     and re.search(r'\w',w[4])]
            # page furniture rows: '[Turn over', 'For Examiner's Use',
            # 'BLANK PAGE', 'Please turn over for Section B', 'Section B'
            rows_txt={}
            for w in content:
                rows_txt.setdefault(round(w[1]/3),[]).append(w)
            content=[w for k,ws in rows_txt.items() for w in ws
                     if not ORPHAN_FURNITURE_RE.match(' '.join(v[4] for v in sorted(ws,key=lambda v:v[0])))
                     and w[4] not in ('[Turn','over','For','Examiner’s',"Examiner's",'Use')]
            if {w[4] for w in content}<={'BLANK','PAGE'}:
                continue                                  # BLANK PAGE
            drawings=[d['rect'] for d in doc[p].get_drawings()
                      if d.get('rect') is not None and d['rect'].width>40 and d['rect'].height>40
                      and d['rect'].x0>=CONTENT_L-5 and d['rect'].x1<=CONTENT_R+15]
            if not drawings:
                # a plotting grid is drawn as many thin lines: use their union
                lines=[d['rect'] for d in doc[p].get_drawings()
                       if d.get('rect') is not None and (d['rect'].width>40 or d['rect'].height>40)
                       and d['rect'].x0>=CONTENT_L-5 and d['rect'].x1<=CONTENT_R+15
                       and HEADER_Y<=d['rect'].y0 and d['rect'].y1<=page_cap]
                if len(lines)>=8:
                    # min/max by hand: Rect union ignores zero-height lines
                    u=fitz.Rect(min(r.x0 for r in lines),min(r.y0 for r in lines),
                                max(r.x1 for r in lines),max(r.y1 for r in lines))
                    if u.width>100 and u.height>100:
                        drawings=[u]
            if not content and not drawings:
                continue                                  # pure answer space
            prose=[w for w in content if re.search(r'[A-Za-z]{4,}',w[4])]
            if os.environ.get('AL_DEBUG_ORPHAN'):
                print('ORPHAN',p+1,'content',[w[4][:15] for w in content][:20],'drawings',
                      [tuple(round(v) for v in r) for r in drawings][:6],file=sys.stderr)
            if not drawings or len(prose)>12:
                # a prose page inside a question with no label of its own:
                # * it carries a mark -> the previous leaf's own task continues
                #   here ('For each of the organelles ... A name ...... [4]',
                #   a part-less Q1, 9700/23/O/N/12 p.3);
                # * else it introduces a later part of the SAME question -> that
                #   part's .stem (context pages, 9700/21/M/J/16 p.8).
                # A page before a new question's number stays REVIEW_REQUIRED.
                before_=[e for e in out if e[1]<p]
                after_=[e for e in out if e[1]>p]
                owner_=idx_=None
                if before_:
                    prev_=max(before_,key=lambda e:(e[1],e[3]))
                    pq=prev_[0].split('.')[0]
                    marks_=[w for w in W[p] if HEADER_Y+10<=w[1]<page_cap and MARK_RE.match(w[4])]
                    nxt_=min(after_,key=lambda e:(e[1],e[2])) if after_ else None
                    if marks_:
                        lv=[e for e in before_ if not e[0].endswith('.stem') and e[0].split('.')[0]==pq]
                        if lv:
                            owner_=max(lv,key=lambda e:(e[1],e[3]))[0]; idx_=len(out)
                    elif nxt_ is not None and nxt_[0].split('.')[0]==pq:
                        try:
                            owner_,idx_=orphan_owner(p,'head',content,nxt_,out)
                        except RuntimeError:
                            owner_=None
                if owner_ is not None:
                    rt_,rb_=INK[p].extent(HEADER_Y,page_cap)
                    if rt_ is not None:
                        if os.environ.get('AL_DEBUG_ORPHAN'):
                            print('ORPHAN-PAGE',p+1,'->',owner_,file=sys.stderr)
                        out.insert(idx_,(owner_,p,rt_-2,rb_+2))
                        continue
                if os.environ.get('AL_DRAFT'):
                    print(f'DRAFT: unlabelled content page {p+1} between crops (skipped)',file=sys.stderr)
                    continue
                raise RuntimeError(f'REVIEW_REQUIRED: unlabelled content page {p+1} between crops')
            before=[e for e in out if e[1]<p]
            question=max(before,key=lambda e:(e[1],e[3]))[0].split('.')[0]
            # Walk back through this question's leaves; once a leaf asks to
            # draw on a graph/grid/figure, keep walking while the previous
            # leaves do too, so the owner is the FIRST leaf that uses it
            # (52/M/J/24: (c)(i) 'Plot a graph', not (c)(ii) 'Draw ... line').
            owner=None
            seen=set()
            for e in sorted(before,key=lambda e:(e[1],e[2]),reverse=True):
                lab=e[0]
                if lab in seen or lab.endswith('.stem') or lab.split('.')[0]!=question:
                    continue
                seen.add(lab)
                prompt=' '.join(w[4] for w in W[e[1]] if e[2]-1<=w[1]<=e[3])
                if SCAFFOLD_PROMPT_RE.search(prompt):
                    owner=lab
                elif owner is not None:
                    break
            if owner is None and p>last_crop_page:
                # a figure page after the paper's last crop serves its last leaf
                lv=[e for e in before if not e[0].endswith('.stem')]
                owner=max(lv,key=lambda e:(e[1],e[3]))[0] if lv else None
            if owner is None:
                if os.environ.get('AL_DRAFT'):
                    print(f'DRAFT: graphic page {p+1} has no owner (skipped)',file=sys.stderr)
                    continue
                raise RuntimeError(f'REVIEW_REQUIRED: graphic page {p+1} has no plotting/drawing prompt to own it')
            rt,rb=INK[p].extent(HEADER_Y,page_cap)
            below=[r['y0'] for r in ar if r['y0']>rt+2]
            tail=min([rb+2]+[y-2 for y in below])
            out.append((owner,p,rt-2,tail))
        return out

    CAPTION_RE=re.compile(r'\b(?:Fig\.|Figure|Table)\s*\d+\.\d+')
    def orphan_owner(p,where,region_ws,nxt_emit,out):
        """Owner of unlabelled context found at the foot/head of page p.

        * a captioned figure/table ('Table 4.1') belongs to the FIRST leaf of
          the question whose own text names it (9701/22/F/M/23 Q4(d)(i): 'Use
          information from Table 4.1 (on page 14)'), even when printed after it;
        * otherwise the next item owns it: the highest part that starts with
          that item and has not started yet -> '<part>.stem' (Q7.b.stem), else
          the next leaf's own lead-in;
        * prose before a NEW question's number is REVIEW_REQUIRED.
        Returns (label, index in `out` to insert the segment at)."""
        nxt=nxt_emit[0]
        q=nxt.split('.')[0]
        # only a region that OPENS with its caption is a floated figure/table;
        # prose-led context ('In both experiments the student ...' with Tables
        # 1.1/1.2 inside, 9701/52/F/M/17 p.2) is shared setup for what follows
        first_row=sorted([w for w in region_ws if abs(w[1]-min(v[1] for v in region_ws))<3],key=lambda w:w[0])
        caps=set(CAPTION_RE.findall(' '.join(w[4] for w in first_row)))
        # a FIGURE caption anywhere in the region also follows its first
        # referencing leaf (the gate's figure-ownership rule; 9701/52/M/J/25
        # Fig. 1.2 named by (h)(i), printed before part (i))
        caps|={c for c in CAPTION_RE.findall(' '.join(w[4] for w in sorted(region_ws,key=lambda w:(round(w[1]/3),w[0]))))
               if not c.startswith('Table')}
        if caps:
            for i,e in enumerate(out):
                lab,pno,y0,y1=e
                if lab.endswith('.stem') or lab.split('.')[0]!=q:
                    continue
                txt=' '.join(w[4] for w in sorted(W[pno],key=lambda w:(round(w[1]),w[0])) if y0-1<=w[1]<=y1)
                if any(c.replace(' ','') in txt.replace(' ','') for c in caps):
                    last=max(j for j,f in enumerate(out) if f[0]==lab)
                    return lab,last+1
        prev=[e for e in out if (e[1],e[2])<(nxt_emit[1],nxt_emit[2])]
        if IS_MATHS and not [e for e in prev if e[0].split('.')[0]==q]:
            # a diagram printed beside / under the question's own number, above
            # its context prose ('4' + tree diagram, then 'Nikita goes shopping
            # ...', 9709/62/M/J/15 p.3) is the start of that question's first crop
            qa=[a for a in A.get(p,[]) if a['kind']=='Q' and f"Q{a['label']}"==q]
            if qa and nxt_emit[1]==p and min(w[1] for w in region_ws)>=qa[0]['y']-12:
                return nxt,out.index(nxt_emit)
        if not prev or max(prev,key=lambda e:(e[1],e[3]))[0].split('.')[0]!=q:
            raise RuntimeError(f'REVIEW_REQUIRED: unlabelled content at {where} of page {p+1} before {nxt}')
        idx=out.index(nxt_emit)
        if nxt.endswith('.stem'):
            return nxt,idx
        started=set()
        for e in prev:
            parts=e[0].replace('.stem','').split('.')
            started.update('.'.join(parts[:k]) for k in range(1,len(parts)+1))
        parts=nxt.split('.')
        fresh=['.'.join(parts[:k]) for k in range(1,len(parts)) if '.'.join(parts[:k]) not in started]
        if fresh and '.' not in fresh[0]:
            raise RuntimeError(f'REVIEW_REQUIRED: unlabelled content at {where} of page {p+1} before new question {fresh[0]}')
        if fresh:
            return fresh[0]+'.stem',idx
        # context before a lettered part that is itself a leaf is that part's
        # mid-question stem (the engine's own Qn.L.stem convention); before a
        # deeper leaf it is the leaf's lead-in
        return (nxt+'.stem' if nxt.count('.')==1 else nxt),idx

    def orphan_prose(p,lo,hi,ar):
        """Context rows in (lo,hi) on page p: prose (>=3 real words) or a
        figure/table caption; furniture, answer rows and marks excluded."""
        def in_ar(w):
            return any(r['y0']-1<=w[1]<=r['y1']+1 for r in ar)
        rows={}
        if IS_MATHS:
            # the copyright notice can close a middle page ('[Questions 10 and 11
            # are printed on the next page.]' + notice, 9709/11/O/N/15 p.3)
            hi=min([hi]+[w[1]-1 for w in W[p] if w[4]=='Permission' and any(
                v[4]=='reproduce' and abs(v[1]-w[1])<3 for v in W[p])])
        for w in W[p]:
            if lo<w[1]<hi and not DOTS_RE.match(w[4]) and not MARK_RE.match(w[4]) \
                    and not in_ar(w) and re.search(r'\w',w[4]):
                rows.setdefault(round(w[1]/3),[]).append(w)
        keep=[]
        for k,ws in sorted(rows.items()):
            txt=' '.join(v[4] for v in sorted(ws,key=lambda v:v[0]))
            if ORPHAN_FURNITURE_RE.match(txt) or ANSWER_AREA_LABEL_RE.match(txt) or STOP_RE.search(txt):
                continue
            if len([v for v in ws if re.search(r'[A-Za-z]{4,}',v[4])])>=3 or CAPTION_RE.fullmatch(txt.strip()):
                keep.append(ws)
            elif IS_MATHS and len([v for v in ws if re.search(r'[A-Za-z]{4,}',unicodedata.normalize('NFKC',v[4]))])>=2:
                # Maths context is short and symbolic: 'The function h is defined by
                # h(x) = 1/(x^2+2) for x >= 0.' (9709/12/M/J/24 p.7) has two long words
                # (NFKC: 'deﬁned' is printed with the fi ligature, 9709/12/F/M/20 p.11)
                keep.append(ws)
            elif IS_MATHS and (re.fullmatch(r'[A-Z][a-z]+(?: \S+){3,}',txt) and
                               re.search(r'[A-Za-z]{4,}',unicodedata.normalize('NFKC',txt)) or
                               re.fullmatch(r'Hence,?',txt)):
                # short sentences 'The median of X is m.' (9709/61/O/N/21 p.7; its
                # raised 'X' / 'm.' fall in the next 3-pt row bucket) and a
                # lone 'Hence' introducing the next romans (9709/61/O/N/17 Q3)
                keep.append(ws)
        return keep

    def figure_top(p,lo,top,ar):
        """A region that opens with a caption ('Fig. 2.1') holds the figure
        ABOVE it: start at the first ink after the last answer row / mark
        between `lo` and the caption (9701/52/M/J/24 p.7, calibration graph
        under (b)'s answer line)."""
        cap=sorted([w for w in W[p] if abs(w[1]-top)<3],key=lambda w:w[0])
        # Maths diagrams carry no caption: the figure sits above 'The diagram shows ...'
        if not IS_MATHS and not CAPTION_RE.fullmatch(' '.join(w[4] for w in cap).strip()):
            return top
        above=[r['y1'] for r in ar if lo<r['y1']<top]+[w[3] for w in W[p] if lo<w[1]<top and MARK_RE.match(w[4])]
        a=max([lo]+above)+1
        rt,_=INK[p].extent(a,top)
        return rt if rt is not None else top

    def alevel_trailing_context(emits):
        """A Level: context for the NEXT item printed after a leaf's answer
        area, at the label column ('(ii) Predict ...' / answer lines / 'In its
        saturated solution, [AgBr(aq)] = 7.1 x 10-7 mol dm-3.' / '(iii) ...',
        9701/41/O/N/05 Q1(b); '(ii) shape ...... [2]' / 'The boiling point of
        lead(IV) chloride ...' + table / '(b)', 9701/04/M/J/04 Q2(a)(ii)).
        A prose row that follows one of the leaf's answer rows or its mark and
        starts left of the leaf's body text cuts the leaf; the rest goes to
        the next item via orphan_owner()."""
        out=[tuple(e) for e in emits]
        ans=[]                                  # (page, y) of answer rows and marks
        for p in range(doc.page_count):
            ans+=[(p,r['y0']) for r in AR_CACHE.get(p,[])]
            ans+=[(p,w[1]) for w in W[p] if MARK_RE.match(w[4])]
        ans.sort()
        for lab in list(dict.fromkeys(e[0] for e in out)):
            if lab.endswith('.stem'):
                continue
            idx=sorted([i for i,e in enumerate(out) if e[0]==lab],key=lambda i:(out[i][1],out[i][2]))
            first=[]
            for i in idx:                       # first words of the leaf (a sliver segment can hold none)
                _,p0,a0,b0=out[i]
                first=sorted([w for w in W[p0] if a0-1<=w[1]<=b0 and re.search(r'\w',w[4])],
                             key=lambda w:(round(w[1]/3),w[0]))
                if first: break
            if not first:
                continue
            # body indent = the first word right of the leaf's OWN label token
            # (a raised word above the label row, 'copper(II)' at x=197 in
            # 9701/41/M/J/19 Q1(a), made the whole leaf look outdented)
            tok=f"({lab.split('.')[-1]})"
            lt=[w for w in first if w[4]==tok]
            if not lt:
                continue
            lt=lt[0]
            right=sorted([w for w in first if abs(w[1]-lt[1])<5 and w[0]>lt[2]+1
                          and w[4] not in ('●','•','▪') and not re.fullmatch(r'\([a-z]{1,4}\)',w[4])],
                         key=lambda w:w[0])
            if not right:
                continue
            body=right[0][0]
            cut=None
            for i in idx:
                _,p,a,b=out[i]
                # emit ranges may still overlap the next label's line before
                # clamping ('(ii) Explain your answer to (i) ...', 9701/02/M/J/06)
                b=min([b]+[e[2] for e in out if e[0]!=lab and e[1]==p and a<e[2]<b])
                geom=table_cells(doc[p])
                rows={}
                for w in W[p]:
                    if a<=w[1]<b-1 and not dot_in_table(w,geom): rows.setdefault(round(w[1]/3),[]).append(w)
                for _,ws in sorted(rows.items()):
                    ws.sort(key=lambda w:w[0]); ry=min(w[1] for w in ws)
                    if (p,ry)<=(p0,first[0][1]+3):
                        continue
                    seen=any((p0,first[0][1]-1)<=pos<(p,ry-2) for pos in ans)
                    prose=len([w for w in ws if re.search(r'[A-Za-z]{4,}',w[4])])>=(2 if IS_MATHS else 3)
                    # a bulleted row continues the leaf's own list ('(a) * ... /
                    # ...... / * Write an equation for ...', 9701/53/O/N/14 Q1(a))
                    bullet=ws[0][4] in ('●','•','▪')
                    if seen and prose and not bullet and ws[0][0]<body-10 and not any(r['y0']-1<=ry<=r['y1']+1 for r in AR_CACHE.get(p,[])):
                        cut=(i,ry); break
                if cut: break
            if not cut:
                continue
            ci,cy=cut
            _,cp,ca,cb=out[ci]
            if IS_MATHS:
                # the uncaptioned diagram above the context row goes with it
                # (9709/12/M/J/24 Q4: (a)'s answer lines / graph of y = g(x) /
                # 'The diagram shows the graph of y = g(x) ...' / (b))
                ft=figure_top(cp,ca,cy,AR_CACHE.get(cp,[]))
                if ca+4<ft<cy:
                    cy=ft
            # a scaffold the leaf asks the candidate to complete ('complete the
            # genetic diagram': key to symbols ...... / parental phenotypes /
            # gametes / offspring / [3], 9700/42/M/J/13 Q7(a)) is the leaf's
            # own, not trailing context, while the leaf's mark is still below
            nx_=[e for e in out if e[0]!=lab and (e[1],e[2])>(cp,cy)]
            nxy=min(((e[1],e[2]) for e in nx_),default=(cp,FOOTER_Y))
            own_mark=any((cp,cy)<(pp,w[1])<nxy for pp in range(cp,nxy[0]+1) for w in W[pp] if MARK_RE.match(w[4]))
            if own_mark and requests_following_scaffold(p0,first[0][1],cy):
                continue
            later=[j for j in idx if (out[j][1],out[j][2])>(cp,ca)]
            moved=[(cp,cy-2,cb)]+[(out[j][1],out[j][2],out[j][3]) for j in later]
            nxt=sorted([e for e in out if e[0]!=lab and (e[1],e[2])>(cp,cy)],key=lambda e:(e[1],e[2]))
            if not nxt:
                continue
            region=[w for (pp,a,b) in moved for w in W[pp] if a<=w[1]<b]
            if os.environ.get('AL_DEBUG_ORPHAN'):
                print('TRAILING',lab,cp+1,round(cy,1),'->',nxt[0][0],file=sys.stderr)
            keep=[e for j,e in enumerate(out) if not (j in later)]
            ki=keep.index(out[ci])
            if cy-2-ca>4:
                keep[ki]=(lab,cp,ca,cy-2)
            else:
                keep.pop(ki)
            try:
                owner,ins=orphan_owner(cp,'mid',region,nxt[0],keep)
            except RuntimeError:
                continue                # ambiguous (e.g. before a new question): leave it with the leaf
            for k,(pp,a,b) in enumerate(moved):
                keep.insert(ins+k,(owner,pp,a,b))
            # reshaped pieces keep the stop-clamp exemption of the segments
            # they came from (else the clamp cut them at their dotted rows)
            if (lab,cp,round(ca,3),round(cb,3)) in AL_BYPASS:
                AL_BYPASS.add((lab,cp,round(ca,3),round(cy-2,3)))
            for (pp,a,b) in moved:
                AL_BYPASS.add((owner,pp,round(a,3),round(b,3)))
            out=keep
        return out

    def alevel_orphan_tails(emits):
        """A Level: shared context printed at the FOOT of a page whose next
        label starts on a later page (9701/42/F/M/19 p.18: 'Ethanedioyl
        dichloride is used in the following synthesis ...' + the reaction
        scheme after (a)(ii); '(b) (i)' opens p.19).  Owner: orphan_owner()."""
        out=list(emits)
        for p in sorted({e[1] for e in emits}):
            on_p=[e for e in out if e[1]==p]
            bottom=max(e[3] for e in on_p)
            later=sorted([e for e in out if e[1]>p],key=lambda e:(e[1],e[2]))
            if not later:
                continue
            ar=answer_rows(p)
            prose_rows=orphan_prose(p,bottom+1,page_cap,ar)
            if not prose_rows:
                continue
            top=min(w[1] for w in prose_rows[0])
            # an answer row or [mark] below it: the previous leaf's own later
            # prompt ('* Calculate the mole fraction ...' / ...... / [3],
            # 9701/22/F/M/17 Q2(c)(iv)); D6 step (2b) keeps it there
            if any(r['y0']>top+2 for r in ar) or any(
                    top<w[1]<page_cap and MARK_RE.match(w[4]) for w in W[p]):
                continue
            rt,rb=INK[p].extent(figure_top(p,bottom+1,top,ar)-1,page_cap)
            if rt is None:
                continue
            try:
                owner,idx=orphan_owner(p,'foot',[w for ws in prose_rows for w in ws],later[0],out)
            except RuntimeError:
                if os.environ.get('AL_DRAFT'):
                    continue        # draft: leave it for the autofix/manual route
                raise
            if os.environ.get('AL_DEBUG_ORPHAN'):
                print('ORPHAN-TAIL',p+1,round(rt,1),round(rb,1),'->',owner,file=sys.stderr)
            out.insert(idx,(owner,p,rt-2,rb+2))
        return out

    def alevel_orphan_heads(emits):
        """A Level: context at the HEAD of a page, above its first crop, that
        no crop owns -- 9701/52/F/M/17 p.4 'The student plotted a graph ...
        as shown.' + the graph, then '(c) Use the graph ...'; 9701/22/F/M/23
        p.14 Table 4.1 (named by (d)(i) on p.13).  Skipped when an answer row
        or mark follows it before the first crop (that is the previous leaf's
        own continued prompt).  Owner: orphan_owner()."""
        out=list(emits)
        for p in sorted({e[1] for e in emits}):
            on_p=sorted([e for e in out if e[1]==p],key=lambda e:e[2])
            first=on_p[0]
            if not [e for e in out if e[1]<p]:
                continue                    # the paper's first content page
            ar=answer_rows(p)
            floor=continued_floor(p,first[2])
            prose_rows=orphan_prose(p,floor-1,first[2]-1,ar)
            if not prose_rows:
                continue
            top=min(w[1] for w in prose_rows[0])
            ends=[r['y1'] for r in ar if top<r['y0']<first[2]]+[w[3] for w in W[p] if top<w[1]<first[2] and MARK_RE.match(w[4])]
            if ends:
                # followed by an answer row / mark: the previous leaf's own
                # continued prompt (its second bullet + '[2]' atop the next
                # page, 9701/53/O/N/14 Q1(a)) -> that leaf, up to its last row
                prev_=[e for e in out if (e[1],e[2])<(p,0) and not e[0].endswith('.stem')]
                last_=max(ends)
                rt0,rb0=INK[p].extent(floor-1,last_+2)
                if prev_ and rt0 is not None:
                    owner0=max(prev_,key=lambda e:(e[1],e[3]))[0]
                    if os.environ.get('AL_DEBUG_ORPHAN'):
                        print('ORPHAN-HEAD-CONT',p+1,round(rt0,1),round(rb0,1),'->',owner0,file=sys.stderr)
                    out.insert(max(i for i,e in enumerate(out) if e[0]==owner0)+1,(owner0,p,rt0-2,rb0+2))
                rest=[ws for ws in prose_rows if min(w[1] for w in ws)>last_+1]
                if not rest:
                    continue
                prose_rows=rest; top=min(w[1] for w in rest[0])
            rt,rb=INK[p].extent(figure_top(p,floor-1,top,ar)-1,first[2]-1)
            if rt is None:
                continue
            try:
                owner,idx=orphan_owner(p,'head',[w for ws in prose_rows for w in ws],first,out)
            except RuntimeError:
                if os.environ.get('AL_DRAFT'):
                    continue        # draft: leave it for the autofix/manual route
                raise
            if os.environ.get('AL_DEBUG_ORPHAN'):
                print('ORPHAN-HEAD',p+1,round(rt,1),round(rb,1),'->',owner,file=sys.stderr)
            out.insert(idx,(owner,p,rt-2,rb+2))
        return out

    def maths_figures_above_context(emits):
        """Maths: content printed after the previous part's answer lines / mark
        and above the next crop belongs to that crop: context prose ('The line
        l2 has equation ...', 9709/32/M/J/24 Q8) with any diagram above it, or an
        uncaptioned diagram above a crop that opens with context prose ('The
        diagram shows the graph of y = g(x) ...', 9709/12/M/J/24 Q4).  Ink alone
        above a crop that opens with its own label is left alone (blank axes
        after '(a) Sketch ... [3]' are (a)'s answer space)."""
        out=list(emits)
        for i,(lab,p,y0,y1) in enumerate(out):
            prev=[(j,e) for j,e in enumerate(out) if j!=i and e[1]==p and e[2]<y0-1]
            if not prev:
                continue
            j,pe=max(prev,key=lambda t:t[1][2])
            first=sorted([w for w in W[p] if y0-1<=w[1]<=y0+12 and re.search(r'\w',w[4])],key=lambda w:w[0])
            if not first:
                continue
            opens_with_label=bool(re.fullmatch(r'\([a-z]{1,4}\)|\d{1,2}',first[0][4]))
            ar=AR_CACHE.get(p,[])
            ends=[r['y1'] for r in ar if pe[2]<r['y1']<y0]+[w[3] for w in W[p] if pe[2]<w[1]<y0 and MARK_RE.match(w[4])]
            if not ends:
                continue
            a=max(ends)+1
            # context prose in the gap ('The line l2 has equation r = ...' between
            # (a)'s answer lines and (b), 9709/32/M/J/24 Q8) goes to the next crop
            # whatever it opens with; ink alone only when the crop opens with prose
            prose=orphan_prose(p,a,y0-1,ar)
            if opens_with_label and not prose:
                continue
            rt,_=INK[p].extent(a,y0-1)
            if rt is None or rt>y0-6:
                continue
            if os.environ.get('AL_DEBUG_ORPHAN'):
                print('MATHS-FIGURE',p+1,round(rt,1),round(y0,1),'->',lab,file=sys.stderr)
            out[i]=(lab,p,rt-2,y1)
            if pe[3]>rt-3:
                out[j]=(pe[0],pe[1],pe[2],rt-3)
        return out

    def maths_raised_question_rows(emits):
        """Maths: a question's first row can rise above its number -- an
        integral's upper limit, a superscript, a stacked numerator ('5 Given
        that integral_0^a 6e^(2x+1) dx = 65', 9709/22/F/M/16).  The previous
        question's last crop ended at the number's row and this one started
        PAD_PT above it, so that ink was sliced or printed in both crops.  Cut
        both in the white run above the row's ink instead."""
        out=list(emits)
        for p,anchors in A.items():
            for q in anchors:
                if q['kind']!='Q':
                    continue
                ay=q['y']; top=ay
                while True:          # words overlapping the number's row, transitively
                    up=[w[1] for w in W[p] if CONTENT_L<=w[0]<=CONTENT_R
                        and ay-30<w[1]<top and w[3]>top+1.5]
                    if not up or min(up)>=top:
                        break
                    top=min(up)
                ink=INK[p]
                rt,_=ink.extent(top,q.get('row_y1',ay+10))
                if rt is None:
                    continue
                r=ink._r(rt); lo=ink._r(ay-30)
                while r>lo and ink.ink[r-1]>0:
                    r-=1
                rt=ink._p(r)
                mine=[i for i,e in enumerate(out) if e[1]==p and e[0].split('.')[0]==f"Q{q['label']}"
                      and min(ay-PAD_PT,rt)-2*PAD_PT<=e[2]<=q.get('row_y1',ay)+2]
                mine=[i for i in mine if out[i][2]==min(out[j][2] for j in mine)]   # the question's first crop
                for i in mine:       # a crop opening inside an ink block (a diagram's
                    r=ink._r(out[i][2])   # 'y' label beside the number row, 9709/21/O/N/14 Q6)
                    if ink.ink[r]>0:
                        while r>lo and ink.ink[r-1]>0:
                            r-=1
                        rt=min(rt,ink._p(r))
                prev=[i for i,e in enumerate(out) if e[1]==p and e[0].split('.')[0]!=f"Q{q['label']}"
                      and e[2]<rt-2 and e[3]>rt-2]
                if not mine:
                    continue
                if all(out[i][2]<=rt-1 for i in mine) and all(out[i][3]<=rt-1 for i in prev):
                    continue         # the row's ink is already inside its own crop only
                cut=boundary(p,max([out[i][2] for i in prev] or [HEADER_Y]),rt)
                if not cut<rt or ink.ink[ink._r(cut):ink._r(rt)].any():
                    continue         # no white run just above the row: leave it to the gate
                cut=max(cut,rt-PAD_PT)   # still inside that white run
                if os.environ.get('AL_DEBUG_ORPHAN'):
                    print('MATHS-RAISED-ROW',p+1,q['label'],round(rt,1),round(cut,1),file=sys.stderr)
                for i in mine:
                    out[i]=(out[i][0],p,cut,out[i][3])
                for i in prev:
                    out[i]=(out[i][0],p,out[i][2],min(out[i][3],cut))
        return out

    def maths_drawings_across_bottom(emits):
        """Maths: a vector drawing that starts inside a crop and runs on below
        its end -- the y-axis of blank sketch axes below the x-axis labels
        ('(b) Sketch the curve.', 9709/11/M/J/23 Q7) -- is kept whole (blank
        answer grids stay in their leaf, user decision 2026-10-20), unless
        another crop starts before the drawing ends."""
        out=list(emits)
        for i,(lab,p,y0,y1) in enumerate(out):
            starts=[e[2] for j,e in enumerate(out) if j!=i and e[1]==p and e[2]>y0+1]
            nxt=min(starts,default=min(CONTENT_BOTTOM,FOOTER_Y))
            low=[d['rect'] for d in doc[p].get_drawings() if d.get('rect') is not None
                 and y0-2<=d['rect'].y0<y1-2 and d['rect'].y1>y1+1 and d['rect'].height<400
                 and CONTENT_L-5<=d['rect'].x0 and d['rect'].x1<=CONTENT_R+15
                 and not (d.get('fill') in ((1,1,1),(1.0,1.0,1.0)) and d.get('color') is None)]
            if not low:
                continue
            bot=max(r.y1 for r in low)
            if bot+2>=nxt or first_stop(p,y1)<bot:
                continue
            if os.environ.get('AL_DEBUG_ORPHAN'):
                print('MATHS-DRAWING-BELOW',p+1,lab,round(y1,1),'->',round(bot+2,1),file=sys.stderr)
            out[i]=(lab,p,y0,bot+2)
        return out

    def maths_axes_after_rows(emits):
        """Maths: blank axes printed after a leaf's answer lines ('Hence sketch a
        displacement-time graph ... [6]', lines, then the axes, 9709/41/M/J/18
        Q5(i)) are that leaf's answer grid: kept as an extra segment (user
        decision 2026-10-20), the dotted lines between stay out.  Only when
        nothing but answer rows / marks lies between the leaf and the axes."""
        out=list(emits)
        for p in sorted({e[1] for e in emits}):
            ar=AR_CACHE.get(p,[])
            big=[d['rect'] for d in doc[p].get_drawings() if d.get('rect') is not None
                 and (d['rect'].width>100 or d['rect'].height>100)
                 and CONTENT_L-5<=d['rect'].x0 and d['rect'].x1<=CONTENT_R+15
                 and not any(e[1]==p and e[2]<=(d['rect'].y0+d['rect'].y1)/2<=e[3] for e in out)]
            if not big:
                continue
            g0=min(r.y0 for r in big); g1=max(r.y1 for r in big)
            above=[i for i,e in enumerate(out) if e[1]==p and e[3]<=g0 and not e[0].endswith('.stem')]
            if not above:
                continue
            i=max(above,key=lambda i:out[i][3])
            ly1=out[i][3]
            if any(e[1]==p and ly1-1<e[2]<g1 for e in out):
                continue
            between=[w for w in W[p] if ly1<w[1]<g0-16 and not DOTS_RE.match(w[4]) and not MARK_RE.match(w[4])
                     and not any(r['y0']-1<=w[1]<=r['y1']+1 for r in ar)]
            if between:
                continue
            lo=max([ly1]+[r['y1']+1 for r in ar if ly1<r['y1']<g0])
            nxt=min([e[2] for e in out if e[1]==p and e[2]>g1]+[min(CONTENT_BOTTOM,FOOTER_Y)])
            rt,rb=INK[p].extent(lo,nxt-1)
            if rt is None or rt>g0+1 or rb<g1-1:
                continue
            if os.environ.get('AL_DEBUG_ORPHAN'):
                print('MATHS-AXES-AFTER-ROWS',p+1,out[i][0],round(rt,1),round(rb,1),file=sys.stderr)
            out.insert(i+1,(out[i][0],p,rt-2,rb+2))
        return out

    def maths_copyright_cap(emits):
        """Maths: the last leaf of a paper ran to the page foot and took in the
        copyright notice printed under it ('Permission to reproduce items ...',
        9709/32/M/J/12 p.4): end every crop above the notice and its rule."""
        out=[]
        for lab,p,y0,y1 in emits:
            tops=[w[1] for w in W[p] if w[4]=='Permission' and any(
                v[4]=='reproduce' and abs(v[1]-w[1])<3 for v in W[p])]
            tops=[t for t in tops if y0<t<y1]
            if tops:
                t=min(tops)
                rules=[d['rect'].y0 for d in doc[p].get_drawings() if d.get('rect') is not None
                       and t-14<d['rect'].y0<t and d['rect'].height<2 and d['rect'].width>200]
                y1=min([t]+rules)-2
                if os.environ.get('AL_DEBUG_ORPHAN'):
                    print('MATHS-COPYRIGHT-CAP',p+1,lab,round(y1,1),file=sys.stderr)
            out.append((lab,p,y0,y1))
        return out

    def maths_gap_above_grid(emits):
        """Maths: '(a) Draw a histogram ... [4]', blank working space, then the
        printed graph-paper grid (9709/52/F/M/22 Q3(a)).  The grid stays in the
        leaf (user decision 2026-10-20); the blank band above it (> 40 pt) is
        cut out: the leaf becomes two segments, prompt + grid."""
        out=[]
        for lab,p,y0,y1 in emits:
            big=[d['rect'] for d in doc[p].get_drawings() if d.get('rect') is not None
                 and d['rect'].width>100 and d['rect'].height>60 and y0+10<d['rect'].y0<y1]
            if lab.endswith('.stem') or not big:
                out.append((lab,p,y0,y1)); continue
            g=min(r.y0 for r in big)
            ink=INK[p]; a=ink._r(y0); b=ink._r(g)
            zs=np.where(ink.ink[a:b+1]==0)[0]
            runs=[]
            if len(zs):
                s=q=zs[0]
                for z in zs[1:]:
                    if z==q+1: q=z; continue
                    runs.append((s,q)); s=q=z
                runs.append((s,q))
            runs=[(s,e) for s,e in runs if s>0 and ink.ink[a:a+s].any() and (e-s)/SC>40]
            if not runs:
                out.append((lab,p,y0,y1)); continue
            s,e=max(runs,key=lambda r:r[1]-r[0])
            if os.environ.get('AL_DEBUG_ORPHAN'):
                print('MATHS-GRID-GAP',p+1,lab,round(ink._p(a+s),1),round(ink._p(a+e),1),file=sys.stderr)
            out.append((lab,p,y0,ink._p(a+s)+3))
            out.append((lab,p,ink._p(a+e)-3,y1))
        return out

    def maths_bracket_hints(emits):
        """Maths: a bracketed hint printed after a leaf's mark ('[The volume of a
        cone is 1/3 pi r^2 h.]', 9709/51/M/J/18 Q7(i); at the end of the
        question, 9709/31/O/N/13 Q10) is part of the leaf printed directly
        above it: extend that crop over the hint (up to 3 wrapped rows)."""
        out=list(emits)
        for p in sorted({e[1] for e in out}):
            ar=AR_CACHE.get(p,[])
            free=[w for w in W[p] if CONTENT_L<=w[0]<=CONTENT_R and HEADER_Y<w[1]<CONTENT_BOTTOM
                  and not any(e[1]==p and e[2]<=(w[1]+w[3])/2<=e[3] for e in out)
                  and not any(r['y0']-1<=w[1]<=r['y1']+1 for r in ar)]
            for w0 in free:
                if not w0[4].startswith('[') or MARK_RE.match(w0[4]) or \
                        [v for v in free if v[2]<=w0[0] and v[1]<w0[3]-2 and v[3]>w0[1]+2]:
                    continue         # not the first word of its row
                top,bot=w0[1],w0[3]; nrows=1
                while True:          # the row (stacked fractions overlap it) + wrapped rows
                    row=[v for v in free if v[1]<bot-2 and v[3]>top+2 and v[0]>=w0[0]-1]
                    bot=max(bot,max(v[3] for v in row)); top=min(top,min(v[1] for v in row))
                    last=max([v for v in row if (v[1]+v[3])/2>bot-9] or row,key=lambda v:v[2])   # end of the LAST row
                    if last[4].endswith(']') or nrows>=3:
                        break
                    nxt=[v for v in free if bot-2<=v[1]<bot+8]
                    if not nxt:
                        break
                    bot=max(v[3] for v in nxt); nrows+=1
                txt=' '.join(v[4] for v in sorted(row,key=lambda v:(round(v[1]/3),v[0])))
                if not last[4].endswith(']') or len(row)<3 or ORPHAN_FURNITURE_RE.match(txt) or STOP_RE.search(txt):
                    continue
                above=[i for i,e in enumerate(out) if e[1]==p and e[3]<=top+1 and not e[0].endswith('.stem')]
                if not above:
                    continue
                i=max(above,key=lambda i:out[i][3])
                between=[r for r in ar if out[i][3]<r['y0']<top]
                if between or top-out[i][3]>30 or any(e[1]==p and out[i][3]<e[2]<bot for e in out):
                    continue
                _,rb=INK[p].extent(top-2,bot+4)
                if os.environ.get('AL_DEBUG_ORPHAN'):
                    print('MATHS-HINT',p+1,round(top,1),'->',out[i][0],file=sys.stderr)
                out[i]=(out[i][0],p,out[i][2],max(bot,rb or bot)+2)
        return out

    page_cap=min(CONTENT_BOTTOM,FOOTER_Y)
    def leaf_continuation_segments(label,pno,y,next_anchor):
        """A Level: the rest of a leaf's prompt printed on following pages.

        Cambridge A Level papers have no 'Question N continued' header.  When
        a leaf's own page holds neither its [mark] nor the start of its
        answer area, the prompt carries on at the top of the next page, e.g.
        9702/42/M/J/24 Q5(b): setup + Fig. 5.2 on p.12, then 'State three
        conclusions ...' on p.13 above the numbered answer lines.  Append that
        content (header -> first answer row / next label) as extra segments of
        the same leaf, page by page, until an answer area or mark is reached.
        """
        if not IS_ALEVEL:
            return []
        if mark_bot(pno,y,page_cap) is not None or first_stop(pno,y)<page_cap:
            return []
        end_pno=next_anchor['pno'] if next_anchor else doc.page_count-1
        segs=[]
        for cpno in range(pno+1,end_pno+1):
            floor=continued_floor(cpno,FOOTER_Y)
            limit=(next_anchor['y']-2 if (next_anchor and cpno==next_anchor['pno'])
                   else page_cap)
            stop=first_stop(cpno,floor)
            tail=min(stop,limit)
            words=[w for w in W[cpno] if floor<=w[1]<tail and re.search(r'\w',w[4])]
            only_answer_label=(bool(words) and all(ANSWER_AREA_LABEL_RE.match(w[4]) for w in words)
                               and not [d for d in doc[cpno].get_drawings()
                                        if d.get('rect') is not None and floor<=d['rect'].y0<tail
                                        and d['rect'].width>40 and d['rect'].height>40])
            if only_answer_label:
                break                       # 'Diagram' heading = start of answer space
            if segment_has_content(cpno,floor,tail):
                segs.append((label,cpno,floor,tail))
            if stop<limit or mark_bot(cpno,floor,limit) is not None:
                break
        return segs

    QNUM={}
    for a in seq:
        # A Level: always hide the number -- '5 (a) (i)' sits 3.9 pt below its
        # prompt text, so the row was not 'inline' and the 5 stayed visible
        # in Q5(a)(i) (9702/41/O/N/17)
        if a['kind']=='Q' and (a.get('inline') or IS_ALEVEL) and a.get('nbox'):
            QNUM.setdefault(a['pno'],[]).append(a['nbox'])
    q_idx=[i for i,a in enumerate(seq) if a['kind']=='Q']; q_idx.append(len(seq))
    emits=[]
    continuation_frame_masks={}

    def append_requested_continuation(qi,qn,question_emit_start):
        """Append an essential scaffold placed on a continuation page.

        IB occasionally puts the diagram named by a leaf prompt on the next
        physical page (for example, "draw ... on the following diagram").
        Such a page has no new part anchor, so an anchor-only splitter would
        silently omit it.  We require both an explicit ownership phrase in the
        final leaf and an official "Question N continued" header, then keep
        only content above the first answer-area stop.
        """
        leaves=[emit for emit in emits[question_emit_start:]
                if not emit[0].endswith('.stem')]
        if not leaves:
            return
        label,pno,y0,y1=leaves[-1]
        prompt=' '.join(w[4] for w in W[pno]
                        if y0-3<=w[1]<=y1+3 and CONTENT_L<=w[0]<=CONTENT_R)
        owns_following=bool(re.search(
            r'\b(?:on|in)\s+the\s+following\s+'
            r'(?:diagram|graph|grid|axes|table)\b',prompt,re.I
        ))
        if not owns_following:
            return
        # Do not mistake a continuation-page answer area for a missing
        # scaffold.  Some papers put the complete requested grid/diagram in
        # the leaf's current segment, then begin the next page with an empty
        # framed working area under the same "Question N continued" header.
        # In that layout the current segment already satisfies the prompt;
        # appending anything from the next page would add answer furniture.
        # Genuine cross-page scaffolds (for example the N21 AI SL Voronoi
        # diagram) have no graphical content in the prompt segment and still
        # pass this gate.
        if graphical_content_between(pno,y0,y1):
            return
        next_index=q_idx[qi+1]
        next_q_pno=(seq[next_index]['pno'] if next_index<len(seq)
                    else doc.page_count)
        for cpno in range(pno+1,next_q_pno):
            page_text=' '.join(w[4] for w in W[cpno])
            if not re.search(fr'Question\s+{re.escape(str(qn))}\s+continued',
                             page_text,re.I):
                continue
            floor=continued_floor(cpno,FOOTER_Y)
            tail=min(first_stop(cpno,floor),continued_tail(cpno,floor))
            if not segment_has_content(cpno,floor,tail):
                continue
            emits.append((label,cpno,floor,tail))
            # The supplied graph may sit inside a large answer-area frame.
            # Keep the mathematical diagram but mask only that outer frame;
            # dotted working rows and the lower answer box are already beyond
            # `tail` because they are stop rows.
            for drawing in doc[cpno].get_drawings():
                rect=drawing.get('rect')
                if (rect and rect.width>(CONTENT_R-CONTENT_L)*0.85 and
                        rect.height>60 and floor-10<=rect.y0 and
                        rect.y1<=tail+10):
                    continuation_frame_masks.setdefault(cpno,[]).append(rect)

    for qi in range(len(q_idx)-1):
        question_emit_start=len(emits)
        grp=seq[q_idx[qi]:q_idx[qi+1]]; qn=grp[0]['label']; qpno=grp[0]['pno']; qbot=grp[0]['row_y1']
        next_q_anchor=seq[q_idx[qi+1]] if q_idx[qi+1]<len(seq) else None
        # qlook stays on the number's own row for "what comes next" lookups;
        # qbot is where the crop starts. For inline layouts the crop must
        # start ABOVE the number's row to keep the question's first line, but
        # searching for the next anchor from there would match the question's
        # own anchor and collapse the crop to nothing.
        qlook=grp[0]['row_y1']
        if grp[0].get('inline'): qbot=grp[0]['y']-PAD_PT
        parts=[a for a in grp if a['kind']=='PART']
        if not parts:
            sp=min(first_stop(qpno,qlook),next_anchor_y(qpno,qlook))
            mb0=mark_bot(qpno,qbot+1,sp)
            answer_top=answer_row_top(qpno,qbot+1,sp)
            if answer_top is not None:
                end=min(sp,answer_top)
            else:
                end=(min(sp, content_cap(qpno,mb0,sp)+PAD_PT+2)
                     if mb0 is not None else sp)
            emits.append((f'Q{qn}',qpno,qbot+1,end))
            append_requested_continuation(qi,qn,question_emit_start)
            continue
        # Ceilings (crop END boundaries, i.e. "stop before the next anchor")
        # use the next anchor's own text-detected y directly rather than a
        # gap-tolerant ink scan: diagrams (graphs, sketches) often have real
        # internal whitespace -- e.g. a gap between a dashed asymptote line
        # and the axis below it -- bigger than the small contiguity
        # tolerance tuned for text line-spacing, so a gap-scan can stop
        # partway through a diagram and truncate it. The renderer's own
        # ink-extent step below (and content_cap for anything after a mark)
        # is gap-immune and finds the true top/bottom within this window
        # regardless of internal sparsity, so we don't need to pre-trim here.
        first_part=parts[0]; first_part_pno=first_part['pno']
        first_gi=grp.index(first_part)
        first_next_i=grp.index(parts[1]) if len(parts)>1 else len(grp)
        first_romans=[a for a in grp[first_gi+1:first_next_i] if a['kind']=='ROMAN']
        first_child_label=(f'Q{qn}.{first_part["label"]}.{first_romans[0]["label"]}'
                           if first_romans else f'Q{qn}.{first_part["label"]}')
        root_owner_pair=(f'Q{qn}.stem',first_child_label)
        question_stem_exists=False
        stem_top=None
        if first_part_pno==qpno:
            # Detect ownership BEFORE choosing a cut.  A tall fraction in the
            # first child may rise above its marker baseline, so a whitespace
            # cut by itself cannot tell whether shared context exists.
            root_start=midstem_start(qpno,qbot-6,first_part['y'],first_part.get('x',88)+14)
            inline_first_part=(IS_IGCSE and
                               abs(first_part['y']-grp[0]['y'])<4)
            # Cambridge's compact `1 (a) ...` layout is semantically the
            # user's `1a)` case: the parent number has no independent text,
            # hence no Q1 stem.  Maths glyphs on that same row can be exposed
            # as vector drawings and must not override the printed hierarchy.
            question_stem_exists=(not inline_first_part and (
                                  root_start is not None or
                                  (grp[0].get('inline') and
                                   abs(first_part['y']-grp[0]['y'])>=4) or
                                  (IS_IGCSE and graphical_content_between(
                                      qpno,qbot,first_part['y']))))
            stem_top=(semantic_cut_before_anchor(qpno,qbot,first_part,root_owner_pair)
                      if question_stem_exists else boundary(qpno,qbot,first_part['y']))
            if question_stem_exists:
                emits.append((f'Q{qn}.stem',qpno,qbot+1,stem_top))
        else:
            # Root context may span a page tail, one or more continuation
            # pages, and the head of the page containing part (a).  Preserve
            # each physical segment and concatenate them under ONE logical
            # filename at render time.
            tail=continued_tail(qpno,qbot)
            if segment_has_content(qpno,qbot+1,tail):
                emits.append((f'Q{qn}.stem',qpno,qbot+1,tail))
                question_stem_exists=True
            for cpno in range(qpno+1,first_part_pno):
                floor=continued_floor(cpno,FOOTER_Y)
                tail=continued_tail(cpno,floor)
                if segment_has_content(cpno,floor,tail):
                    emits.append((f'Q{qn}.stem',cpno,floor,tail))
                    question_stem_exists=True
            floor=continued_floor(first_part_pno,first_part['y'])
            final_has=segment_has_content(first_part_pno,floor,first_part['y']-2)
            stem_top=(semantic_cut_before_anchor(first_part_pno,floor,first_part,root_owner_pair)
                      if final_has else boundary(first_part_pno,floor,first_part['y']))
            if final_has:
                emits.append((f'Q{qn}.stem',first_part_pno,floor,stem_top))
                question_stem_exists=True
        prev_markbot=None; prev_pno=qpno; prev_anchor_bot=qbot
        for i,P in enumerate(parts):
            L=P['label']; pno=P['pno']
            nextP=parts[i+1] if i+1<len(parts) else None
            gi=grp.index(P); gj=grp.index(nextP) if nextP else len(grp)
            romans=[a for a in grp[gi+1:gj] if a['kind']=='ROMAN']
            # safe floor for upward top-expansion: previous mark-bottom if
            # we're past the first part on this page, else the question's
            # own number row (or page top, if this part is on a later page)
            floor0 = prev_markbot if (prev_markbot is not None and prev_pno==pno) else (
                qbot if pno==qpno else continued_floor(pno,P['y']))
            # never let upward expansion cross above the previous anchor's row
            if prev_pno==pno: floor0=max(floor0, prev_anchor_bot)
            span_end = boundary(pno,P['y'],nextP['y']) if (nextP and nextP['pno']==pno) else min(first_stop(pno,P['y']),next_anchor_y(pno,P['y']))
            first_part_cut=stem_top if (i==0 and pno==first_part_pno and question_stem_exists) else None
            lms=None
            if i>=1 and prev_markbot is not None and prev_pno==pno:
                lms=midstem_start(pno,prev_markbot,P['y'],P.get('x',88)+14,
                                  allow_body_indent=True)
            elif i>=1 and prev_pno!=pno:
                # A continued question can begin a new page with shared prose,
                # a table, or a diagram before its next labelled part. Start
                # looking below page furniture / "Question N continued", and
                # keep that material as the next part's .stem.
                page_floor=last_stop_before(pno,P['y'])+12
                lms=midstem_start(pno,page_floor-6,P['y'],P.get('x',88)+14,
                                  allow_body_indent=True)
                if lms is not None:
                    floor0=max(floor0,page_floor)
            # A blank table/graph placed after the previous part's mark is
            # sometimes the object that part explicitly asks the candidate to
            # complete.  It belongs to that answerable leaf, not to a new stem
            # for the following sibling.  Extend the most recent leaf through
            # the complete scaffold and suppress the spurious next-part stem.
            if (i>=1 and lms is not None and prev_markbot is not None and
                    prev_pno==pno and requests_following_scaffold(
                        pno,parts[i-1]['y'],prev_markbot) and
                    scaffold_bounds(pno,prev_markbot,P['y']) is not None):
                later_context=prose_after_scaffold(pno,prev_markbot,P['y'])
                if later_context is not None:
                    # A completed requested scaffold is followed by a new
                    # setup for this sibling.  Start the sibling stem at that
                    # setup, not at table cells or diagram labels above it.
                    lms=later_context
                else:
                    scaffold_end=boundary(pno,prev_markbot,P['y'])
                    for emit_idx in range(len(emits)-1,-1,-1):
                        elabel,epno,ey0,ey1=emits[emit_idx]
                        if epno==pno and not elabel.endswith('.stem'):
                            emits[emit_idx]=(elabel,epno,ey0,max(ey1,scaffold_end))
                            break
                    lms=None
            if romans:
                fr=romans[0]
                roman_owner_pair=(f'Q{qn}.{L}.stem',f'Q{qn}.{L}.{fr["label"]}')
                cross_page_first=fr['pno']!=pno
                same=abs(fr['y']-P['y'])<4 and not cross_page_first
                if cross_page_first:
                    # A parent may begin at the foot of one page while its
                    # first roman child begins on the next (or a later)
                    # continuation page.  Preserve the parent context as one
                    # logical multi-segment stem, but compute every physical
                    # y-coordinate on the page it belongs to.
                    parent_tail=continued_tail(pno,P['y'])
                    parent_has=(head_prose_exists(pno,P['y'],parent_tail) or
                                graphical_content_between(
                                    pno,P.get('row_y1',P['y']),parent_tail))
                    middle_segments=[]
                    for cpno in range(pno+1,fr['pno']):
                        middle_floor=continued_floor(cpno,FOOTER_Y)
                        middle_tail=continued_tail(cpno,middle_floor)
                        if segment_has_content(cpno,middle_floor,middle_tail):
                            middle_segments.append((cpno,middle_floor,middle_tail))
                    final_floor=continued_floor(fr['pno'],fr['y'])
                    final_has=segment_has_content(fr['pno'],final_floor,fr['y']-2)
                    fr_top=(semantic_cut_before_anchor(
                                fr['pno'],final_floor,fr,roman_owner_pair)
                            if final_has else
                            boundary(fr['pno'],final_floor,fr['y']))
                    head_has=parent_has or bool(middle_segments) or final_has
                    if head_has:
                        if parent_has:
                            stem_start=expand_top(pno,P['y'],floor0)-PAD_PT
                            if first_part_cut is not None:
                                stem_start=max(stem_start,first_part_cut)
                            emits.append((f'Q{qn}.{L}.stem',pno,
                                          stem_start,parent_tail))
                        for cpno,middle_floor,middle_tail in middle_segments:
                            emits.append((f'Q{qn}.{L}.stem',cpno,
                                          middle_floor,middle_tail))
                        if final_has:
                            emits.append((f'Q{qn}.{L}.stem',fr['pno'],
                                          final_floor,fr_top))
                    pre_inline_roman_stem=False
                    stem_needed=head_has
                    stem_end=fr_top
                else:
                    head_probe=(not same) and head_prose_exists(
                        pno,(lms if lms is not None else P['y']),fr['y'])
                    head_has=(lms is not None) or head_probe
                    fr_top=(semantic_cut_before_anchor(
                                pno,(lms if lms is not None else P['y']),fr,
                                roman_owner_pair)
                            if (not same and head_probe)
                            else (boundary(pno,P['y'],fr['y'])
                                  if not same else P['y']-PAD_PT))
                    if lms is not None:
                        prior=(prev_markbot if
                               (prev_markbot is not None and prev_pno==pno)
                               else floor0)
                        stem_start=boundary(pno,prior,lms)
                    elif head_probe and prev_pno==pno:
                        prior=prev_markbot if prev_markbot is not None else floor0
                        stem_start=boundary(pno,prior,P['y'])
                    else:
                        stem_start=expand_top(pno,P['y'],floor0)-PAD_PT
                    if first_part_cut is not None:
                        stem_start=max(stem_start,first_part_cut)
                # A shared context block can also appear *before* an inline
                # parent/roman pair, for example:
                #
                #   The regression lines are ...
                #   (b) (i) Estimate ...
                #       (ii) Find ...
                #
                # `same` is true in that layout, so `head_has` deliberately
                # rejects prose on the parent/roman row.  The older logic then
                # let the pre-(b) context bleed into child (i), even though it
                # is needed by both roman children.  `lms` already identifies
                # that genuinely outdented context; emit it as the next
                # parent-part stem and make its end the shared whitespace cut
                # before the inline labels.  The labels stay with child (i),
                # as required for an inline parent/first-roman prompt.
                    pre_inline_roman_stem = same and lms is not None
                    stem_needed = head_has or pre_inline_roman_stem
                    stem_end = (semantic_cut_before_anchor(
                                    pno,lms,P,roman_owner_pair)
                                if pre_inline_roman_stem else fr_top)
                    if stem_needed:
                        emits.append((f'Q{qn}.{L}.stem',pno,stem_start,stem_end))
                pending_roman_prelude=None
                previous_roman_answer_top=None
                for j,R in enumerate(romans):
                    nR=romans[j+1] if j+1<len(romans) else nextP
                    natural_end=(nR['y']-2 if (nR and nR['pno']==R['pno'])
                                 else min(first_stop(R['pno'],R['y']),
                                          next_anchor_y(R['pno'],R['y'])))
                    r_end=(boundary(R['pno'],R['y'],nR['y'])
                           if (nR and nR['pno']==R['pno']) else natural_end)
                    # Search the complete logical sibling interval for its
                    # mark/response furniture.  A matrix or column-vector
                    # answer can occupy every horizontal row and make the
                    # ordinary whitespace boundary collapse back to the
                    # prompt's top; restricting this search to `r_end` would
                    # then erase the real question text.
                    rmb=mark_bot(R['pno'],R['y'],natural_end)
                    r_answer_top=answer_row_top(R['pno'],R['y'],natural_end)
                    rtms=midstem_start(
                        R['pno'],rmb if rmb else R['y'],r_end,
                        R.get('x',99)+14,allow_body_indent=(rmb is not None))
                    r_final = boundary(R['pno'],rmb if rmb else R['y'],rtms) if rtms is not None else r_end
                    if r_answer_top is not None:
                        r_final=r_answer_top
                    elif rmb is not None:
                        r_final=min(r_final, content_cap(R['pno'],rmb,r_final)+PAD_PT+2)
                    # Upward expansion must never cross above the PREVIOUS
                    # sibling's own text row, or a tall-content scan will
                    # swallow that sibling into this crop (two subparts in one
                    # image). Siblings often carry no [mark] of their own --
                    # only the last one does -- so prev_markbot is not a safe
                    # floor on its own; clamp to the previous anchor's row
                    # bottom, which is always below its text and above ours.
                    if j==0:
                        if cross_page_first:
                            r_start=(fr_top if stem_needed else
                                     expand_top(R['pno'],R['y'],
                                                continued_floor(R['pno'],R['y']))-
                                     PAD_PT)
                        elif pre_inline_roman_stem:
                            r_start=stem_end
                        elif head_has:
                            r_start=fr_top
                        elif first_part_cut is not None:
                            r_start=first_part_cut
                        else:
                            r_start=expand_top(pno,P['y'],floor0)-PAD_PT
                    elif pending_roman_prelude is not None and prev_pno==R['pno']:
                        # (a prelude found on the previous roman's page is a y on
                        # THAT page: 9701/52/M/J/18 Q2(f)(ii) on p.11 started at
                        # p.10's y=560 and lost its prompt and grid)
                        r_start=pending_roman_prelude
                    elif (previous_roman_answer_top is not None and
                          prev_pno==R['pno']):
                        r_start=max(
                            previous_roman_answer_top,
                            prev_markbot+2,
                            expand_top(R['pno'],R['y'],prev_markbot)-PAD_PT,
                        )
                    else:
                        prevR=romans[j-1]
                        r_start=boundary(R['pno'],prevR['y'],R['y']) if prevR['pno']==R['pno'] \
                                else expand_top(R['pno'],R['y'],HEADER_Y)-PAD_PT
                    if os.environ.get('SPLITTER_DEBUG_CALC') in {
                            f'Q{qn}.{L}',f'Q{qn}.{L}.{R["label"]}'}:
                        print(
                            'ROMAN_CALC',f'Q{qn}.{L}.{R["label"]}',
                            'page',R['pno']+1,'r_end',r_end,'mark',rmb,
                            'answer_top',r_answer_top,'midstem',rtms,
                            'start',r_start,'end',r_final,
                            file=sys.stderr,
                        )
                    emits.append((f'Q{qn}.{L}.{R["label"]}',R['pno'],r_start,r_final))
                    emits.extend(leaf_continuation_segments(
                        f'Q{qn}.{L}.{R["label"]}',R['pno'],R['y'],nR or next_q_anchor))
                    # the next roman's prelude starts where the context does,
                    # not at this roman's answer-row cut (9701/22/O/N/18
                    # Q4(e)(ii) began with (i)'s 'CH3COCO2H + ......' row)
                    pending_roman_prelude=(boundary(R['pno'],rmb if rmb else R['y'],rtms)
                                           if rtms is not None else None)
                    previous_roman_answer_top=r_answer_top
                    prev_markbot=rmb or R['y']+10; prev_pno=R['pno']
                    prev_anchor_bot=R.get('row_y1',R['y'])
            else:
                if lms is not None:
                    prior=prev_markbot if (prev_markbot is not None and prev_pno==pno) else floor0
                    # STEM_RECLASSIFICATION_PROTOCOL.md sec.1: "The number of
                    # following children does not change the rule. A
                    # non-answerable block that introduces only one later
                    # child is still that child's stem; never hide it inside
                    # the child crop." A detected mid-stem here must therefore
                    # be emitted as its own `Qn.L.stem`, exactly as the
                    # multi-roman branch above does, not folded into this
                    # single leaf's own crop.
                    part_owner_pair=(f'Q{qn}.{L}.stem',f'Q{qn}.{L}')
                    lms_stem_start=boundary(pno,prior,lms)
                    lms_stem_end=semantic_cut_before_anchor(
                        pno,lms,P,part_owner_pair)
                    emits.append((f'Q{qn}.{L}.stem',pno,
                                  lms_stem_start,lms_stem_end))
                    part_start=lms_stem_end
                elif first_part_cut is not None:
                    part_start=first_part_cut
                else:
                    part_start=expand_top(pno,P['y'],floor0)-PAD_PT
                mb=mark_bot(pno,P['y'],span_end)
                part_answer_top=answer_row_top(pno,P['y'],span_end)
                tms=(midstem_start(
                    pno,mb,span_end,P.get('x',88)+14,
                    allow_body_indent=True) if mb is not None else None)
                if (mb is not None and tms is not None and
                        requests_following_scaffold(pno,P['y'],mb) and
                        scaffold_bounds(pno,mb,span_end) is not None):
                    # This part may be the last labelled item on its page. In
                    # that layout there is no next same-page sibling whose
                    # ownership pass can rescue a requested table/diagram.
                    # Keep the scaffold with this leaf; only split again if
                    # genuine prose follows the completed object.
                    later_context=prose_after_scaffold(pno,mb,span_end)
                    tms=later_context
                part_end = boundary(pno,mb if mb else P['y'],tms) if tms is not None else span_end
                if part_answer_top is not None:
                    part_end=min(part_end,part_answer_top)
                elif mb is not None:
                    part_end=min(part_end, content_cap(pno,mb,part_end)+PAD_PT+2)
                if os.environ.get('SPLITTER_DEBUG_CALC') in {
                        f'Q{qn}',f'Q{qn}.{L}'}:
                    print(
                        'PART_CALC',f'Q{qn}.{L}','page',pno+1,
                        'span_end',span_end,'mark',mb,
                        'answer_top',part_answer_top,'midstem',tms,
                        'start',part_start,'end',part_end,
                        file=sys.stderr,
                    )
                emits.append((f'Q{qn}.{L}',pno,part_start,part_end))
                emits.extend(leaf_continuation_segments(
                    f'Q{qn}.{L}',pno,P['y'],nextP or next_q_anchor))
                prev_markbot=mb or (P['y']+10); prev_pno=pno
                prev_anchor_bot=P.get('row_y1',P['y'])

        append_requested_continuation(qi,qn,question_emit_start)

    if os.environ.get('SPLITTER_DEBUG_PHASES'):
        for emit in emits:
            if os.environ['SPLITTER_DEBUG_PHASES'] in emit[0]:
                print('PRE_RECURSION_EMIT',emit,file=sys.stderr)

    # Cambridge occasionally nests alphabetic children below a roman parent:
    # `1 (a) (ii) (a) ... (b) ...`.  Apply the same recursive contract used
    # at the root and part levels: emit the roman parent as `.stem` only when
    # it owns independent shared content, and always emit the answerable
    # alphabetic children as separate leaves.
    nested_groups={}
    current_q=current_part=None; current_roman=None
    for anchor in seq:
        if anchor['kind']=='Q':
            current_q=anchor['label']; current_part=current_roman=None
        elif anchor['kind']=='PART':
            current_part=anchor['label']; current_roman=None
        elif anchor['kind']=='ROMAN':
            current_roman=anchor
        elif (anchor['kind']=='SUBPART' and current_q is not None and
              current_part is not None and current_roman is not None):
            parent=f'Q{current_q}.{current_part}.{current_roman["label"]}'
            group=nested_groups.setdefault(parent,{
                'parent_anchor':current_roman,'children':[]})
            group['children'].append(anchor)

    for parent,group in nested_groups.items():
        parent_indices=[i for i,emit in enumerate(emits) if emit[0]==parent]
        pre_page=[]
        if IS_ALEVEL and len(parent_indices)>1:
            # A Level: the roman's prompt starts on one page and its numbered
            # tasks '1.' '2.' '3.' follow on the next (9702/22/M/J/14
            # Q3(b)(ii)).  Segments on earlier pages are the parent's shared
            # context -> its .stem; the segment on the first task's page is
            # handled below like a single-segment parent.
            cp=group['children'][0]['pno']
            on=[i for i in parent_indices if emits[i][1]==cp]
            if len(on)==1 and all(emits[i][1]<=cp for i in parent_indices):
                pre_page=[i for i in parent_indices if emits[i][1]<cp]
                for i in pre_page:
                    emits[i]=(f'{parent}.stem',)+tuple(emits[i][1:])
                parent_indices=on
        if len(parent_indices)!=1:
            raise RuntimeError(
                f'REVIEW_REQUIRED: nested parent {parent} has '
                f'{len(parent_indices)} physical emit segments')
        emit_idx=parent_indices[0]
        _label,parent_pno,parent_y0,parent_y1=emits[emit_idx]
        parent_anchor=group['parent_anchor']; children=group['children']
        first_child=children[0]
        if first_child['pno']!=parent_pno:
            raise RuntimeError(
                f'REVIEW_REQUIRED: first nested child for {parent} starts '
                f'after its parent page')
        inline_first=abs(first_child['y']-parent_anchor['y'])<4
        stem_exists=(not inline_first and (
            head_prose_exists(parent_pno,parent_anchor['y'],first_child['y']) or
            graphical_content_between(
                parent_pno,parent_anchor.get('row_y1',parent_anchor['y']),
                first_child['y'])))
        replacement=[]
        first_start=parent_y0
        if stem_exists:
            stem_pair=(f'{parent}.stem',f'{parent}.{first_child["label"]}')
            stem_end=semantic_cut_before_anchor(
                parent_pno,parent_anchor['y'],first_child,stem_pair)
            replacement.append((f'{parent}.stem',parent_pno,parent_y0,stem_end))
            first_start=stem_end
        positions={id(anchor):position for position,anchor in enumerate(seq)}
        last_position=positions[id(children[-1])]
        following=next((anchor for anchor in seq[last_position+1:]
                        if anchor['kind']!='SUBPART'),None)
        for child_index,child in enumerate(children):
            child_pno=child['pno']
            if child_index==0:
                start=first_start
            else:
                previous=children[child_index-1]
                start=(boundary(child_pno,previous['y'],child['y'])
                       if previous['pno']==child_pno else
                       expand_top(child_pno,child['y'],
                                  continued_floor(child_pno,child['y']))-PAD_PT)
            next_child=(children[child_index+1]
                        if child_index+1<len(children) else None)
            next_owner=next_child or following
            if next_owner is not None and next_owner['pno']==child_pno:
                end=boundary(child_pno,child['y'],next_owner['y'])
            else:
                # The provisional roman-parent crop may have been clamped at
                # the first nested child's answer row before recursion was
                # known.  Reusing that `parent_y1` for the last child drops
                # a later `(b)` entirely.  Recompute from source structure;
                # the child's own mark/answer-row clamp below will then give
                # it the same tight terminal bound as any ordinary leaf.
                end=min(first_stop(child_pno,child['y']),
                        next_anchor_y(child_pno,child['y']))
            mark_bottom=mark_bot(child_pno,child['y'],end)
            response_top=answer_row_top(child_pno,child['y'],end)
            if response_top is not None:
                end=min(end,response_top)
            elif mark_bottom is not None:
                end=min(end,content_cap(child_pno,mark_bottom,end)+PAD_PT+2)
            replacement.append((f'{parent}.{child["label"]}',
                                child_pno,start,end))
        emits[emit_idx:emit_idx+1]=replacement

    # Consecutive answerable leaves can also contain interleaved stacked
    # formulae (not only stem/child pairs).  The initial emit windows may then
    # overlap because the next leaf's tall maths rises above its label row.
    # Rebuild every such boundary from semantic PDF block ownership and give
    # both owners one shared cut.  If their true hulls interleave, the helper
    # registers the same fail-closed 2-D seam used for stems.
    def output_anchor(label,pno,y0,y1):
        pieces=label.split('.')
        is_stem=pieces[-1:] == ['stem']
        if is_stem:
            if not IS_IGCSE:
                return None
            pieces=pieces[:-1]
        qnum=pieces[0][1:] if pieces and pieces[0].startswith('Q') else None
        if len(pieces)==1:
            kind,target='Q',qnum
        elif len(pieces)>=4:
            kind,target='SUBPART',pieces[-1]
        elif len(pieces)>=3:
            kind,target='ROMAN',pieces[-1]
        else:
            kind,target='PART',pieces[-1]
        candidates=[a for a in A[pno] if a['kind']==kind and a['label']==target
                    and y0-14<=a['y']<=y1+14]
        if not candidates: return None
        return min(candidates,key=lambda a:abs(a['y']-max(y0,a['y'] if a['y']>=y0 else y0)))

    def output_owner_start(label,pno,y0,y1):
        """Semantic start descriptor for the right-hand output at a seam.

        Answerable leaves start at a printed marker, so their marker block is
        authoritative.  A `.stem` starts before its future part marker; use
        the first prose block whose vertical centre lies inside the stem's
        logical window.  Requiring a lexical word rejects raised variables or
        bracket fragments from the preceding leaf that happen to cross the
        provisional horizontal cut.
        """
        anchor=output_anchor(label,pno,y0,y1)
        is_stem=label.endswith('.stem')
        if anchor is not None:
            pieces=label.split('.')
            if (is_stem or len(pieces)>=2) and y0<anchor['y']-8:
                # A standalone paragraph can introduce a later roman child
                # without receiving its own printed label.  When its row is
                # outdented to the roman-marker column, it belongs to the
                # following child.  Use that paragraph block as the semantic
                # owner start so the final mutual-exclusion pass cannot move
                # it backwards into the preceding sibling.
                words=W[pno]
                preludes=[w for w in words
                          if y0+1<=(w[1]+w[3])/2<=anchor['y']-6
                          and 55<=w[0]<=anchor.get('x',99)+16
                          and re.search(r'[A-Za-z]',w[4]) and len(w[4])>1
                          and not (PAR_RE.match(w[4]) or Q_RE.match(w[4]) or
                                   MARK_RE.match(w[4]))]
                if preludes:
                    split_block=min(int(w[5]) for w in preludes)
                    owned=[w for w in words if int(w[5])==split_block and
                           CONTENT_L<=w[0]<=CONTENT_R and
                           w[3]>y0-20 and w[1]<anchor['y']+20]
                    if owned:
                        return {
                            'kind':'BLOCK','label':f'block-{split_block}',
                            'x':min(w[0] for w in owned),
                            'y':min(w[1] for w in owned),
                            '_split_block':split_block,
                        }
            return anchor
        if not is_stem:
            return None
        words=W[pno]
        lexical=[w for w in words
                 if CONTENT_L<=w[0]<=CONTENT_R
                 and y0+1<=(w[1]+w[3])/2<=y1+2
                 and re.search(r'[A-Za-z]',w[4]) and len(w[4])>1
                 and not (PAR_RE.match(w[4]) or Q_RE.match(w[4]) or
                          MARK_RE.match(w[4]))]
        if not lexical:
            return None
        split_block=min(int(w[5]) for w in lexical)
        owned=[w for w in words if int(w[5])==split_block and
               CONTENT_L<=w[0]<=CONTENT_R and w[3]>y0-20 and w[1]<y1+20]
        if not owned:
            return None
        return {
            'kind':'BLOCK','label':f'block-{split_block}',
            'x':min(w[0] for w in owned),
            'y':min(w[1] for w in owned),
            '_split_block':split_block,
        }

    per_page_emit={}
    for idx,(label,pno,y0,y1) in enumerate(emits):
        per_page_emit.setdefault(pno,[]).append(idx)
    for pno,idxs in per_page_emit.items():
        # Emission order is semantic order.  Provisional y-starts are not:
        # every row inside one ruled table can expand upward along the same
        # vertical border and therefore temporarily share the table top.
        idxs.sort()
        for left_idx,right_idx in zip(idxs,idxs[1:]):
            left=list(emits[left_idx]); right=list(emits[right_idx])
            if left[0]==right[0]: continue
            # This repair pass exists only for provisional windows whose
            # vertical ownership interleaves.  Respect an already-proven gap
            # (especially an explicit answer-area stop); recomputing that
            # boundary can expand a clean question crop back over its printed
            # response box in legacy Cambridge layouts.
            if left[3]<=right[2]:
                continue
            # Only impose a semantic ownership seam inside one question.
            # Cross-question boundaries are already hard stops/number rows.
            if left[0].split('.')[0]!=right[0].split('.')[0]:
                continue
            anchor=output_owner_start(right[0],pno,right[2],right[3])
            if anchor is None: continue
            pair=(left[0],right[0])
            existing=[c for c in seam_candidates
                      if c.get('owner_pair')==list(pair) and c['pno']==pno]
            cut=(existing[0]['cut'] if existing else
                 semantic_cut_before_anchor(pno,left[2],anchor,pair))
            # Never invert either logical window.  An impossible semantic cut
            # remains a hard review failure later when no safe seam can bind.
            if left[2]+2<cut<right[3]-2:
                left[3]=cut; right[2]=cut
                emits[left_idx]=tuple(left); emits[right_idx]=tuple(right)

    if os.environ.get('SPLITTER_DEBUG_EMITS'):
        for emit in emits:
            if os.environ['SPLITTER_DEBUG_EMITS'] in emit[0]:
                print('DEBUG_EMIT',emit,file=sys.stderr)
        for candidate in seam_candidates:
            pair=candidate.get('owner_pair') or []
            if any(os.environ['SPLITTER_DEBUG_EMITS'] in owner for owner in pair):
                print('DEBUG_SEAM',candidate,file=sys.stderr)

    AL_BYPASS=set()   # A Level answer-row segments: exempt from stop clamping
    AR_CACHE={}       # answer rows per page, filled by alevel_answer_rows
    SMALL_DRAW={}     # small vector symbols per page (answer_rows)
    if IS_ALEVEL:
        emits=alevel_orphan_pages(emits)
        emits=alevel_orphan_tails(emits)
        emits=alevel_orphan_heads(emits)
        emits=alevel_answer_rows(emits)
        emits=alevel_trailing_context(emits)
        if IS_MATHS:
            emits=maths_figures_above_context(emits)
            emits=maths_raised_question_rows(emits)
            emits=maths_bracket_hints(emits)
            emits=maths_drawings_across_bottom(emits)
            emits=maths_gap_above_grid(emits)
            emits=maths_copyright_cap(emits)
            emits=maths_axes_after_rows(emits)

    # ---- resolve every crop box first, then enforce mutual exclusion --------
    # Keep the true ink extent (rt, rb) alongside the padded box: the padded
    # edges are negotiable, the ink is not. Any later adjustment must move
    # edges within whitespace and never inside [rt, rb].
    boxes=[]
    for emit_order,(label,pno,y0,y1) in enumerate(emits):
        # an appended answer row IS a stop row; clamping it at its own stop
        # erased it (9702/04/O/N/08 Q3(b)(ii)1. 'a = ...... mm [1]')
        bypass_stops=(label,pno,round(y0,3),round(y1,3)) in AL_BYPASS
        y0=max(y0,HEADER_Y); y1=min(y1,FOOTER_Y)
        if y1-y0<6: continue
        top_seams=[c for c in seam_candidates
                   if c['pno']==pno and abs(c['cut']-y0)<1.2]
        bottom_seams=[c for c in seam_candidates
                      if c['pno']==pno and abs(c['cut']-y1)<1.2]
        # A 2-D separator exists precisely because some lower-owner ink rises
        # above the nominal cut while upper-owner ink descends below it.  The
        # extent probe must therefore include the full collision band on both
        # sides; the later semantic mask removes the other owner's pixels.
        # Probing only [y0,y1] would permanently lose a raised upper limit
        # before the mask even had a chance to assign it.
        extent_y0=min([y0]+[min(c['lo'],c['hi'])-4 for c in top_seams])
        extent_y1=max([y1]+[max(c['lo'],c['hi'])+4 for c in bottom_seams])
        rt,rb=INK[pno].extent(extent_y0,extent_y1)
        if rt is None: continue
        stop_below=FOOTER_Y+2 if bypass_stops else first_stop(pno,rt)
        top_is_seam=bool(top_seams)
        bottom_is_seam=bool(bottom_seams)
        # Ordinary semantic separators are hard ownership bounds.  Expanding
        # through them is what made a tall following stem leak backwards into
        # the previous child (legacy Q7 and modern P3 controls).  Only a
        # registered 2-D interleaving may cross its nominal y cut; that pair is
        # subsequently separated by a proven semantic seam.
        lim_lo=HEADER_Y if top_is_seam else y0
        lim_hi=min(FOOTER_Y, CONTENT_BOTTOM, stop_below-2) if bottom_is_seam \
               else min(y1,FOOTER_Y,CONTENT_BOTTOM,stop_below-2)
        # Never cut inside a contiguous run of ink. The emit window is derived
        # from text baselines, so a glyph that rises above or descends below
        # its row (bracket, radical, integral sign, fraction bar) can straddle
        # the window edge -- the extent() call then reports the window edge
        # itself as the ink bound and the glyph gets sliced (bar #3). Walk each
        # edge outward to the first genuinely blank row, bounded by the page
        # header and the next stop so we can't wander into an answer box.
        ink=INK[pno]
        r=ink._r(rt); lo=ink._r(lim_lo)
        while r>lo and ink.ink[r-1]>0: r-=1
        rt=ink._p(r)
        r=ink._r(rb); hi=ink._r(lim_hi)
        while r<hi and ink.ink[r+1]>0: r+=1
        rb=ink._p(r)
        cy0=max(lim_lo, rt-PAD_PT)
        cy1=min(lim_hi, rb+PAD_PT)
        if IS_MATHS:
            # big-bracket pieces of a column vector are text whose box is far
            # taller than its ink ('`' at 56-67 pt over ink from 63 pt,
            # 9709/32/F/M/21 p.12): take in the box centre across white rows
            for w in doc[pno].get_text('words'):   # (not W: a piece can start above HEADER_Y)
                c=(w[1]+w[3])/2
                if len(w[4])>2 or DOTS_RE.match(w[4]) or MARK_RE.match(w[4]):
                    continue         # dotted leaders are erased from the ink map
                if w[3]>cy0+1 and HEADER_Y<c<cy0 and not ink.ink[ink._r(c-1):ink._r(cy0)+1].any():
                    cy0=c-1
                if w[1]<cy1-1 and cy1<c<FOOTER_Y and not ink.ink[ink._r(cy1):ink._r(c+1)+1].any():
                    cy1=c+1
        # [label, page, crop-top, crop-bottom, ink-top, ink-bottom,
        #  logical-order, seam-masks]
        boxes.append([label,pno,cy0,cy1,rt,rb,emit_order,[],y0,y1])

    def ws_cut(pno,lo,hi,fallback):
        """Midpoint of the widest all-white band in [lo,hi]; fallback if none."""
        if hi<=lo: return fallback
        ink=INK[pno]; a=ink._r(lo); b=ink._r(hi)
        if b<=a: return fallback
        seg=ink.ink[a:b+1]; zs=np.where(seg==0)[0]
        if len(zs)==0: return fallback
        runs=[]; s=p=zs[0]
        for z in zs[1:]:
            if z==p+1: p=z; continue
            runs.append((s,p)); s=p=z
        runs.append((s,p))
        s,e=max(runs,key=lambda r:r[1]-r[0])
        return ink._p(a+(s+e)//2)

    def compute_white_seam(candidate):
        """Find a smooth left-to-right path through proven white pixels.

        The path is computed on a one-pixel-dilated ink mask so it keeps a
        safety moat around every glyph and rule.  Any path that touches that
        moat is rejected; callers must quarantine the paper rather than emit
        a visually plausible but clipped crop.
        """
        pno=candidate['pno']; ink=INK[pno]
        extra_top=8 if IS_IGCSE else 3
        extra_bottom=24 if IS_IGCSE else 10
        ylo=max(HEADER_Y,min(candidate['lo'],candidate['hi'])-extra_top)
        yhi=min(FOOTER_Y,max(candidate['lo'],candidate['hi'])+extra_bottom)
        a,b=ink._r(ylo),ink._r(yhi)
        dark=ink.dark[a:b+1,:]
        semantic=ink.semantic[a:b+1,:]
        if dark.shape[0]<8:
            raise RuntimeError(f'REVIEW_REQUIRED: seam band too small on page {pno+1}')
        blocked=semantic.copy()
        # One-pixel 8-neighbour dilation is enough to keep the mask out of
        # antialiased glyph edges while still allowing a path through compact
        # stacked formulae.
        for dy in (-1,0,1):
            for dx in (-1,0,1):
                if dy==0 and dx==0: continue
                ys=slice(max(0,dy), dark.shape[0]+min(0,dy))
                yd=slice(max(0,-dy), dark.shape[0]+min(0,-dy))
                xs=slice(max(0,dx), dark.shape[1]+min(0,dx))
                xd=slice(max(0,-dx), dark.shape[1]+min(0,-dx))
                blocked[yd,xd] |= semantic[ys,xs]
        h,w=blocked.shape

        # The whitespace path is geometrically ambiguous unless it also knows
        # which side owns each formula.  PDF word records carry semantic block
        # order.  Locate the next subpart's marker block, then constrain the
        # seam below every preceding (upper-owner) word and above every word
        # in that marker block and its successors (lower owner).  Per-word
        # ownership is essential, but the extracted font boxes themselves
        # are NOT safe cut geometry: their ascender/descender leading can
        # overlap even when the rendered glyphs do not (adjacent superscripts
        # in M22 AA HL P3 are a real example).  Project each semantic word to
        # its actual dark pixels and constrain the path around those pixels.
        # This preserves ownership without inventing a collision from empty
        # font-box padding.
        anchor=candidate.get('next_anchor')
        if not anchor:
            raise RuntimeError(
                f'REVIEW_REQUIRED: 2-D separator on page {pno+1} has no '
                f'semantic anchor; owners={candidate.get("owner_pair")}; '
                f'band={candidate.get("band",(ylo,yhi))}')
        # A Cambridge table may contain the shared header/example in its top
        # rows and the first labelled child in the next row.  The semantic
        # cut is then allowed to cross only the table's vector rules; text
        # and maths remain blocked.  Keep those rules in the final rendering
        # so both crops retain a complete table edge.
        crossing_grids=[]
        if IS_IGCSE and candidate.get('owner_pair'):
            def clear_rule_segment(point_a,point_b,moat=2):
                x0=int(round((point_a.x-CONTENT_L)*SC))
                x1=int(round((point_b.x-CONTENT_L)*SC))
                yy0=int(round(point_a.y*SC))-a
                yy1=int(round(point_b.y*SC))-a
                if abs(x1-x0)<=2:
                    xa=max(0,min(x0,x1)-moat); xb=min(w,max(x0,x1)+moat+1)
                    ya=max(0,min(yy0,yy1)-moat); yb=min(h,max(yy0,yy1)+moat+1)
                    blocked[ya:yb,xa:xb]=False
                elif abs(yy1-yy0)<=2:
                    xa=max(0,min(x0,x1)-moat); xb=min(w,max(x0,x1)+moat+1)
                    ya=max(0,min(yy0,yy1)-moat); yb=min(h,max(yy0,yy1)+moat+1)
                    blocked[ya:yb,xa:xb]=False
            for drawing in page.get_drawings():
                rect=drawing.get('rect')
                if not (rect and len(drawing.get('items',[]))>=8 and
                        rect.y0<anchor['y']<rect.y1):
                    continue
                crossing_grids.append(rect)
                for item in drawing.get('items',[]):
                    if item[0]=='l':
                        clear_rule_segment(item[1],item[2])
                    elif item[0]=='re':
                        rr=item[1]
                        clear_rule_segment(rr.tl,rr.tr)
                        clear_rule_segment(rr.tr,rr.br)
                        clear_rule_segment(rr.br,rr.bl)
                        clear_rule_segment(rr.bl,rr.tl)
        page_words=W[pno]
        word_block_rects={}
        for block_no in {int(wrd[5]) for wrd in page_words}:
            block_words=[wrd for wrd in page_words if int(wrd[5])==block_no]
            word_block_rects[block_no]=fitz.Rect(
                min(wrd[0] for wrd in block_words),
                min(wrd[1] for wrd in block_words),
                max(wrd[2] for wrd in block_words),
                max(wrd[3] for wrd in block_words),
            )
        direct_split=candidate.get('split_block')
        if direct_split is not None:
            split_block=int(direct_split)
            split_line=candidate.get('split_line')
        else:
            token=(anchor["label"] if anchor.get('kind')=='Q'
                   else f'({anchor["label"]})')
            marker_words=[wrd for wrd in page_words
                          if wrd[4]==token and abs(wrd[1]-anchor['y'])<4
                          and abs(wrd[0]-anchor['x'])<12]
            if not marker_words:
                raise RuntimeError(
                    f'REVIEW_REQUIRED: cannot locate semantic marker {token} on page {pno+1}')
            split_block=min(int(wrd[5]) for wrd in marker_words)
            split_line=min(int(wrd[6]) for wrd in marker_words
                           if int(wrd[5])==split_block)
        lower_bound=np.full(w,-1,dtype=np.int32)
        upper_bound=np.full(w,h,dtype=np.int32)
        upper_graphic_regions=[fitz.Rect(region) for region in
                               candidate.get('upper_graphic_regions',[])]
        upper_graphic_word_regions=[fitz.Rect(region) for region in
                                    candidate.get(
                                        'upper_graphic_word_regions',[])]
        # Vector diagrams remain hard obstacles in `blocked`.  Do not turn a
        # drawing's coarse rectangular bbox into an ownership constraint:
        # curved diagrams often share that bbox with a child sentence in an
        # otherwise white corner.  Instead, constrain the path below the
        # bottommost *rendered diagram pixel in each x-column*.  This keeps a
        # connected cone/hexagon/graph indivisible without claiming its empty
        # rectangular corners (which may legitimately contain child text).
        for region in upper_graphic_regions:
            xa=max(0,min(w-1,int((region.x0-CONTENT_L)*SC)))
            xb=max(0,min(w-1,int((region.x1-CONTENT_L)*SC)+1))
            ya=max(0,min(h-1,int(np.floor(region.y0*SC))-a))
            yb=max(0,min(h-1,int(np.ceil(region.y1*SC))-a))
            if xb<xa or yb<ya:
                continue
            graphic_ink=semantic[ya:yb+1,xa:xb+1].copy()
            # The drawing bbox may share a white corner with the lower
            # question sentence.  Remove all extracted glyph areas before
            # deriving vector ownership; label words are owned separately by
            # the local block rule below.  Otherwise child text inside the
            # coarse bbox is accidentally reclassified as diagram ink.
            for wrd in page_words:
                wr=fitz.Rect(wrd[:4])
                if not wr.intersects(region):
                    continue
                wx0=max(xa,min(xb,int((wr.x0-CONTENT_L)*SC)-2))
                wx1=max(xa,min(xb,int((wr.x1-CONTENT_L)*SC)+2))
                wy0=max(ya,min(yb,int(np.floor(wr.y0*SC))-a-2))
                wy1=max(ya,min(yb,int(np.ceil(wr.y1*SC))-a+2))
                graphic_ink[wy0-ya:wy1-ya+1,
                            wx0-xa:wx1-xa+1]=False
            has_ink=np.any(graphic_ink,axis=0)
            if not np.any(has_ink):
                continue
            last=graphic_ink.shape[0]-1-np.argmax(graphic_ink[::-1,:],axis=0)
            cols=np.flatnonzero(has_ink)
            req=np.minimum(h-1,ya+last[cols]+6)
            # Carry the rendered-pixel ownership into the same horizontal
            # moat used for text.  A diagonal at 220 dpi can occupy a column
            # that is empty in the 144-dpi proof raster; without this moat a
            # one-column cone-edge fragment can survive in the child crop.
            for offset in range(-3,4):
                targets=xa+cols+offset
                valid=(targets>=0)&(targets<w)
                lower_bound[targets[valid]]=np.maximum(
                    lower_bound[targets[valid]],req[valid])
        for wrd in page_words:
            x0,wy0,x1,wy1,_tok,bno,line_no,_word_no=wrd[:8]
            if x1<CONTENT_L or x0>ink.content_r or wy1<ylo or wy0>yhi: continue
            xa=max(0,min(w-1,int((x0-CONTENT_L)*SC)-1))
            xb=max(0,min(w-1,int((x1-CONTENT_L)*SC)+1))
            if xb<xa: continue
            ya=max(0,min(h-1,int(np.floor(wy0*SC))-a))
            yb=max(0,min(h-1,int(np.ceil(wy1*SC))-a))
            if yb<ya: continue
            word_ink=semantic[ya:yb+1,xa:xb+1]
            # Some PDF words are spaces or extraction artefacts with no
            # rendered pixels.  They impose no visual ownership constraint.
            # For real glyphs, use the first/last dark pixel independently in
            # every x column; the one-pixel moat mirrors `blocked` dilation.
            has_ink=np.any(word_ink,axis=0)
            if not np.any(has_ink): continue
            first=np.argmax(word_ink,axis=0)
            last=word_ink.shape[0]-1-np.argmax(word_ink[::-1,:],axis=0)
            child_mark=(direct_split is None and
                        bool(MARK_RE.match(_tok)) and wy0>=anchor['y']-8)
            ink_columns=np.flatnonzero(has_ink)
            # The final crop is rendered at 220 dpi while ownership is
            # analysed at RDPI.  Curved bracket caps can extend a fraction of
            # a point beyond the extraction box / sampled glyph column at the
            # higher resolution.  Carry each semantic column constraint into
            # a three-pixel horizontal moat so those caps cannot survive on
            # the wrong side of an otherwise valid seam.
            cx=(x0+x1)/2; cy=(wy0+wy1)/2
            in_grid=any(rect.x0-2<=cx<=rect.x1+2 and
                        rect.y0-2<=cy<=rect.y1+2
                        for rect in crossing_grids)
            block_no=int(bno)
            block_rect=word_block_rects[block_no]
            # A word near a shared diagram is not automatically a diagram
            # label: a long child sentence can enter the diagram's halo from
            # the left (0580_s08 Q20(a)).  Override PDF block order only when
            # the word's whole text block is substantially local to that
            # diagram.  Genuine vertex/axis/NOT-TO-SCALE label blocks are;
            # question sentences are not.
            inside_upper_graphic=any(
                region.contains(fitz.Point(cx,cy)) and
                (lambda ir: ir.width*ir.height)(region & block_rect) >= block_rect.width*block_rect.height*0.8
                for region in upper_graphic_word_regions)
            if inside_upper_graphic:
                upper_owner=True
            elif child_mark:
                upper_owner=False
            elif in_grid and wy1<anchor['y']-10:
                upper_owner=True
            elif in_grid and wy0>=anchor['y']-4:
                upper_owner=False
            elif block_no!=split_block:
                upper_owner=block_no<split_block
            elif split_line is not None:
                upper_owner=int(line_no)<int(split_line)
            else:
                upper_owner=cy<anchor['y']-3
            # Italic vertex labels can extend farther outside the PDF word
            # bbox at 220 dpi than ordinary text.  Give proven diagram-label
            # blocks a wider local moat so a detached edge of `B`, `C`, etc.
            # cannot survive in the child image.
            semantic_x_moat=6 if inside_upper_graphic else 3
            if upper_owner:
                semantic_y_moat=2
                req=np.minimum(h-1,ya+last+semantic_y_moat)
                for offset in range(-semantic_x_moat,semantic_x_moat+1):
                    targets=xa+ink_columns+offset
                    valid=(targets>=0)&(targets<w)
                    targets=targets[valid]
                    values=req[ink_columns[valid]]
                    lower_bound[targets]=np.maximum(lower_bound[targets],values)
            else:
                req=np.maximum(0,ya+first-2)
                for offset in range(-semantic_x_moat,semantic_x_moat+1):
                    targets=xa+ink_columns+offset
                    valid=(targets>=0)&(targets<w)
                    targets=targets[valid]
                    values=req[ink_columns[valid]]
                    upper_bound[targets]=np.minimum(upper_bound[targets],values)
        impossible=np.where((lower_bound>=0)&(upper_bound<h)&(lower_bound>upper_bound))[0]
        if len(impossible) and os.environ.get('AL_DRAFT'):
            print(f'DRAFT: semantic owners collide on page {pno+1} {candidate.get("owner_pair")} (forced)',file=sys.stderr)
            upper_bound[impossible]=lower_bound[impossible]
            impossible=[]
        if len(impossible):
            raise RuntimeError(
                f'REVIEW_REQUIRED: semantic owners collide in 2-D on page {pno+1}; '
                f'owners={candidate.get("owner_pair")}; '
                f'x={int(impossible[0])}..{int(impossible[-1])}; '
                f'band={candidate.get("band", (ylo,yhi))}')
        rows=np.arange(h,dtype=np.float64)
        center=(h-1)/2.0
        # A very small centrality term prevents the solver from taking the
        # trivial blank route along a band edge; ink avoidance dominates it.
        base=((rows-center)/max(1.0,h))**2*0.08
        invalid=(rows[:,None]<lower_bound[None,:]) | (rows[:,None]>upper_bound[None,:])
        cost=(blocked|invalid).astype(np.float64)*1_000_000.0 + base[:,None]
        cost[:2,:]+=100_000.0; cost[-2:,:]+=100_000.0
        prev=cost[:,0].copy()
        back=np.zeros((h,w),dtype=np.int8)
        # A table corner or steep diagram edge can force the proven white
        # route to change height sharply over only one or two x-columns.  The
        # mask is evaluated independently in every column, so allowing this
        # larger step does not cross ink; every selected pixel is still
        # checked against the dilated semantic obstacle map below.
        offsets=np.arange(-12,13,dtype=np.int8)
        inf=1e30
        for x in range(1,w):
            choices=np.full((len(offsets),h),inf,dtype=np.float64)
            for oi,off in enumerate(offsets):
                o=int(off)
                if o<0:
                    choices[oi,-o:]=prev[:h+o]+abs(o)*0.02
                elif o>0:
                    choices[oi,:h-o]=prev[o:]+abs(o)*0.02
                else:
                    choices[oi,:]=prev
            pick=np.argmin(choices,axis=0)
            prev=cost[:,x]+choices[pick,np.arange(h)]
            back[:,x]=pick.astype(np.int8)
        path=np.empty(w,dtype=np.int32); path[-1]=int(np.argmin(prev))
        for x in range(w-1,0,-1):
            path[x-1]=path[x]+int(offsets[int(back[path[x],x])])
        if np.any((blocked|invalid)[path,np.arange(w)]):
            allowed=~(blocked|invalid)
            reachable=allowed[:,0].copy()
            first_unreachable=None
            for xpos in range(1,w):
                expanded=np.zeros(h,dtype=bool)
                for offset in range(-12,13):
                    if offset<0:
                        expanded[-offset:] |= reachable[:h+offset]
                    elif offset>0:
                        expanded[:h-offset] |= reachable[offset:]
                    else:
                        expanded |= reachable
                reachable=allowed[:,xpos] & expanded
                if not np.any(reachable):
                    first_unreachable=xpos
                    break
            block_x=(first_unreachable if first_unreachable is not None else
                     int(np.flatnonzero((blocked|invalid)[path,np.arange(w)])[0]))
            raise RuntimeError(
                f'REVIEW_REQUIRED: no ink-safe 2-D separator on page {pno+1} '
                f'between y={candidate["lo"]:.2f} and y={candidate["hi"]:.2f}; '
                f'owners={candidate.get("owner_pair")}; '
                f'barrier_x={CONTENT_L+block_x/SC:.2f}; '
                f'allowed_rows={int(allowed[:,block_x].sum())}; '
                f'white_rows={int((~blocked[:,block_x]).sum())}; '
                f'semantic_rows={int((~invalid[:,block_x]).sum())}')
        candidate['path_y']=(a+path)/SC
        candidate['band']=(ylo,yhi)
        return candidate

    def bind_seam(pno,cur,nxt):
        overlap_lo=max(cur[2],nxt[2]); overlap_hi=min(cur[3],nxt[3])
        options=[]
        for c in seam_candidates:
            if c['pno']!=pno or c.get('used'): continue
            if c.get('owner_pair') and c['owner_pair']!=[cur[0],nxt[0]]: continue
            mid=c['cut']
            if c.get('owner_pair')==[cur[0],nxt[0]]:
                in_window=(min(cur[4],nxt[4])-12<=mid<=
                           max(cur[5],nxt[5])+12)
            else:
                in_window=overlap_lo-12<=mid<=overlap_hi+12
            if in_window:
                options.append((abs(mid-(overlap_lo+overlap_hi)/2),c))
        # Cambridge IGCSE question numbers often begin on the same visual row
        # as a tall fraction while the preceding question's right-edge mark
        # hangs a few points lower.  The generic question-to-question path did
        # not request a seam in advance because neither item is a stem.  For a
        # small rendered-ink collision, ask the same fail-closed 2-D solver to
        # prove a separator now; larger collisions still require review.
        if not options and IS_IGCSE and cur[5]-nxt[4] <= 14:
            next_anchor=output_owner_start(
                nxt[0],pno,nxt[8],nxt[9])
            if next_anchor is None:
                next_candidates=[anchor for anchor in A[pno]
                                 if abs(anchor['y']-nxt[4])<24]
                next_anchor=(min(next_candidates,
                                 key=lambda anchor:abs(anchor['y']-nxt[4]))
                             if next_candidates else None)
            candidate={
                'pno':pno,
                'lo':float(nxt[4]-3),
                'hi':float(cur[5]+3),
                'cut':float((cur[5]+nxt[4])/2),
                'owner_pair':[cur[0],nxt[0]],
                'next_anchor':({key:next_anchor.get(key)
                                for key in ('kind','label','x','y')}
                               if next_anchor else None),
                'split_block':(next_anchor.get('_split_block')
                               if next_anchor else None),
                'split_line':(next_anchor.get('_split_line')
                              if next_anchor else None),
            }
            seam_candidates.append(candidate)
            options.append((0.0,candidate))
        if not options and os.environ.get('AL_DRAFT'):
            # draft only: a straight shared cut (the manual/autofix route and
            # visual review decide)
            mid=(max(cur[4],nxt[2])+min(cur[5],nxt[4]))/2 if cur[5]<nxt[4] else (cur[3]+nxt[2])/2
            print(f'DRAFT: no proven separator {cur[0]}/{nxt[0]} p{pno+1}: straight cut {mid:.1f}',file=sys.stderr)
            cur[3]=mid; nxt[2]=mid
            return
        if not options:
            nearby_debug=[(candidate.get('owner_pair'),round(candidate['cut'],2),
                           round(candidate['lo'],2),round(candidate['hi'],2))
                          for candidate in seam_candidates
                          if candidate['pno']==pno and not candidate.get('used')
                          and min(cur[2],nxt[2])-30<=candidate['cut']<=
                              max(cur[3],nxt[3])+30]
            raise RuntimeError(
                f'REVIEW_REQUIRED: vertically overlapping logical crops '
                f'{cur[0]} and {nxt[0]} on page {pno+1} have no proven separator; '
                f'cur_crop={cur[2]:.2f}..{cur[3]:.2f} cur_ink={cur[4]:.2f}..{cur[5]:.2f} '
                f'cur_semantic={cur[8]:.2f}..{cur[9]:.2f}; '
                f'next_crop={nxt[2]:.2f}..{nxt[3]:.2f} next_ink={nxt[4]:.2f}..{nxt[5]:.2f} '
                f'next_semantic={nxt[8]:.2f}..{nxt[9]:.2f}; '
                f'nearby_seams={nearby_debug}')
        try:
            c=compute_white_seam(min(options,key=lambda t:t[0])[1]); c['used']=True
        except RuntimeError:
            if not os.environ.get('AL_DRAFT'):
                raise
            mid=(cur[3]+nxt[2])/2
            print(f'DRAFT: no ink-safe seam {cur[0]}/{nxt[0]} p{pno+1}: straight cut {mid:.1f}',file=sys.stderr)
            cur[3]=mid; nxt[2]=mid
            return
        cur[7].append({'mode':'upper','seam':c})
        nxt[7].append({'mode':'lower','seam':c})

    # Hard guarantee for quality bar #4 ("no two subparts in one image"):
    # two crops on the same page may never share a y-range. Rather than
    # clamping one edge onto the other -- which lands the cut wherever the
    # neighbour's padding happened to start, often mid-glyph (bar #3) -- put a
    # SHARED cut in the whitespace between the two items' real ink. Both
    # invariants then hold at once: no overlap, and no letter sliced.
    bypage={}
    for b in boxes: bypage.setdefault(b[1],[]).append(b)
    for pno,items in bypage.items():
        # Logical emission order is authoritative.  Two owners separated by a
        # 2-D seam intentionally share the same vertical collision band, so
        # sorting by raw ink top can invert them.
        items.sort(key=lambda b:b[6])
        for i in range(len(items)-1):
            cur,nxt=items[i],items[i+1]
            if cur[0]==nxt[0]: continue                 # one multi-segment owner
            nearby_candidates=[c for c in seam_candidates
                               if c['pno']==pno and not c.get('used')
                               and (not c.get('owner_pair') or c['owner_pair']==[cur[0],nxt[0]])
                               and min(cur[2],nxt[2])-12<=c['cut']<=max(cur[3],nxt[3])+12]
            # Text bboxes include font-leading and may overlap by a fraction
            # of a point even when the rendered dark pixels have a genuine
            # horizontal white row.  In that case the raster proof is already
            # stronger than the coarse bbox warning; resolve it as an ordinary
            # shared whitespace cut without applying a mask.
            if nearby_candidates and cur[5]<nxt[4]:
                min(nearby_candidates,key=lambda c:abs(c['cut']-(cur[5]+nxt[4])/2))['used']=True
            if cur[3]<=nxt[2]: continue                  # already disjoint
            if cur[5]>=nxt[4]:
                bind_seam(pno,cur,nxt)
                continue
            cut=ws_cut(pno, cur[5], nxt[4], nxt[4])      # between the two inks
            cur[3]=max(cur[5]+1, min(cur[3], cut))       # never cut into own ink
            nxt[2]=min(nxt[4]-1, max(nxt[2], cut))
    unused=[c for c in seam_candidates if not c.get('used')]
    if unused:
        c=unused[0]
        raise RuntimeError(
            f'REVIEW_REQUIRED: unresolved 2-D separator request on page {c["pno"]+1} '
            f'between y={c["lo"]:.2f} and y={c["hi"]:.2f}; '
            f'owners={c.get("owner_pair")}')
    boxes=[b for b in boxes if b[3]-b[2]>=6]

    # Hide inline question numbers by painting the page white over them once,
    # before any crop is rendered. (Pixmap.set_rect can't be used here: a
    # clipped pixmap carries an origin offset, so rect coordinates don't line
    # up and the call silently no-ops.) The ink profiles were built earlier,
    # so all boundary decisions are unaffected by this cosmetic change; the
    # document is never written back to disk.
    for pno,rects in QNUM.items():
        pg=doc[pno]
        for (nx0,ny0,nx1,ny1) in rects:
            pg.draw_rect(fitz.Rect(CONTENT_L-6,ny0-1.5,nx1+3,ny1+1.5),
                         color=None, fill=(1,1,1), width=0, overlay=True)
    for pno,rects in response_furniture_masks.items():
        pg=doc[pno]
        for rect in rects.values():
            pg.draw_rect(rect,color=None,fill=(1,1,1),width=0,overlay=True)
    for pno,rects in continuation_frame_masks.items():
        pg=doc[pno]
        for rect in rects:
            pg.draw_rect(rect,color=(1,1,1),fill=None,width=3,overlay=True)
    for pno,rects in CREDIT.items():
        pg=doc[pno]
        for rect in rects:
            pg.draw_rect(rect,color=None,fill=(1,1,1),width=0,overlay=True)

    def pix_to_image(pix):
        mode={1:'L',3:'RGB',4:'RGBA'}.get(pix.n)
        if mode is None:
            raise RuntimeError(f'Unsupported pixmap channel count: {pix.n}')
        return Image.frombytes(mode,(pix.width,pix.height),pix.samples).convert('RGB')

    def apply_seam_masks(image,cy0,masks):
        if not masks: return image
        arr=np.array(image,copy=True)
        h,w=arr.shape[:2]
        rr=np.arange(h,dtype=np.int32)[:,None]
        for mask in masks:
            path=mask['seam']['path_y']
            sx=np.linspace(0,len(path)-1,w)
            seam_y=np.interp(sx,np.arange(len(path)),path)
            cut=np.rint((seam_y-cy0)*DPI/72.0).astype(np.int32)[None,:]
            # The proof path runs through a one-pixel moat at the lower
            # analysis resolution.  Do not retain the rounded path row in
            # either 220-dpi output: antialiased diagram edges and glyph caps
            # can otherwise survive as a one-pixel fragment on both sides of
            # an otherwise valid separator (0580_m17 Q10(a) is the control).
            # One proof-mask pixel at 144 dpi covers about 1.5 pixels in the
            # 220-dpi deliverable.  Reserve a one-output-pixel guard on each
            # side so resampling cannot resurrect a cone tip / curved glyph
            # as a detached speck in the opposite crop.
            if mask['mode']=='upper':
                arr[np.broadcast_to(rr>=cut-1,(h,w))]=255
            else:
                arr[np.broadcast_to(rr<=cut+1,(h,w))]=255
        return Image.fromarray(arr,'RGB')

    def trim_outer_whitespace(image,pad_px=18):
        """Remove unexplained outer tail only; never crop through real ink."""
        arr=np.asarray(image)
        gray=arr.mean(axis=2)
        rows=np.where((gray<220).sum(axis=1)>0)[0]
        if len(rows)==0: return image
        top=max(0,int(rows[0])-pad_px)
        bottom=min(image.height,int(rows[-1])+pad_px+1)
        cropped=image.crop((0,top,image.width,bottom))
        top_have=int(rows[0])-top
        bottom_have=bottom-1-int(rows[-1])
        add_top=max(0,pad_px-top_have)
        add_bottom=max(0,pad_px-bottom_have)
        if not (add_top or add_bottom): return cropped
        padded=Image.new('RGB',(cropped.width,cropped.height+add_top+add_bottom),'white')
        padded.paste(cropped,(0,add_top))
        return padded

    SNAP_DPI=200; snap_cache={}
    def snap_edges_to_blank(pno,y0,y1,x1):
        """A Level: move crop edges off glyphs onto blank pixel rows.

        A boundary row touching ink slices a glyph (descenders of 'g'/'y'
        above, the tops of '[2]' brackets below; 7 cases in 9702/42/M/J/24,
        one of which surfaced as a stray dash).  The touched ink run goes to
        the side holding most of it; neighbours sharing an edge apply the
        same rule, so a run is never split or duplicated.  A run taller than
        14 pt means no nearby whitespace: REVIEW_REQUIRED.
        """
        if pno not in snap_cache:
            pm=doc[pno].get_pixmap(dpi=SNAP_DPI,colorspace=fitz.csGRAY,alpha=False)
            snap_cache[pno]=np.frombuffer(pm.samples,np.uint8).reshape(pm.height,pm.width)
        img=snap_cache[pno]; k=SNAP_DPI/72.0
        xa,xb=int(CONTENT_L*k),int(x1*k)
        if (pno,'long') not in snap_cache:
            # vertical ink runs longer than 200 pt are page structure (the
            # old full-height 'For Examiner's Use' column rule), not content:
            # they must not make every row look inked (9701/21/M/J/11 p.8)
            ink_=img<235
            longv=np.zeros_like(ink_)
            lim=int(200*k)
            for c in np.nonzero(ink_.sum(axis=0)>lim)[0]:
                col=ink_[:,c].astype(np.int8)
                d=np.diff(np.concatenate(([0],col,[0])))
                for s_,e_ in zip(np.nonzero(d==1)[0],np.nonzero(d==-1)[0]):
                    if e_-s_>lim: longv[s_:e_,c]=True
            snap_cache[(pno,'long')]=ink_&~longv
        inked=snap_cache[(pno,'long')][:,xa:xb].any(axis=1)   # faint grey figure edges count as ink
        def run(row):
            a=b=row
            while a>0 and inked[a-1]: a-=1
            while b<len(inked)-1 and inked[b+1]: b+=1
            return a,b
        def side(row,a,b,top_edge):
            """Where the edge goes: the touched ink run moves to the side
            holding most of it; a run taller than 14 pt is fine when blank
            space lies within 14 pt on ONE side (an edge just inside a framed
            box or figure, 9701/21/M/J/17 p.3); else REVIEW_REQUIRED."""
            up,down=(row-a)/k,(b-row)/k
            if up>14 and down>14:
                if os.environ.get('AL_DRAFT'):
                    print(f'DRAFT: no blank row near y={row/k:.1f} on page {pno+1} (edge kept)',file=sys.stderr)
                    return row/k
                raise RuntimeError(f'REVIEW_REQUIRED: no blank row near y={row/k:.1f} on page {pno+1}')
            if up<=14 and down<=14:
                go_up=(b-row)>=(row-a) if top_edge else not ((row-a)>=(b-row))
            else:
                go_up=up<=14
            return (a-1)/k if go_up else (b+1)/k
        r0=int(round(y0*k))
        if 0<=r0<len(inked) and inked[r0]:
            a,b=run(r0)
            y0=side(r0,a,b,True)
        r1=int(round(y1*k))
        if 0<=r1<len(inked) and inked[r1]:
            a,b=run(r1)
            y1=side(r1,a,b,False)
        return y0,y1

    def clean_edge_intruders(image,pno,rl,cy0,cy1):
        """White out glyph remnants of a NEIGHBOURING row at a crop edge.

        A word whose centre lies outside [cy0,cy1] but whose box crosses the
        edge can leave faint antialiased feet inside the crop ('[2]' of
        9702/52/F/M/17 Q2(d)(i) atop (d)(ii)).  Paint white the part of that
        word's box inside the crop -- only where no word or drawing of this
        crop shares that area.
        """
        pg=doc[pno]; k=DPI/72.0
        ws=[w for w in pg.get_text('words') if furniture_free(pg,w[:4])]
        own=[fitz.Rect(w[:4]) for w in ws if cy0<=(w[1]+w[3])/2<=cy1]
        drs=[d['rect'] for d in pg.get_drawings() if d.get('rect') is not None]
        out=image
        for w in ws:
            c=(w[1]+w[3])/2
            if cy0<=c<=cy1 or not (w[1]<cy1 and w[3]>cy0):
                continue
            reg=fitz.Rect(w[0]-1,max(w[1],cy0),w[2]+1,min(w[3],cy1))
            if reg.is_empty or any(o.intersects(reg) for o in own) or any(d.intersects(reg) for d in drs):
                continue
            if out is image:
                out=image.copy()
            ImageDraw.Draw(out).rectangle([int((reg.x0-rl)*k),int((reg.y0-cy0)*k),
                                           int((reg.x1-rl)*k)+1,int((reg.y1-cy0)*k)+1],fill='white')
        return out

    rendered={}; provenance={}
    # one leaf's segments that overlap on a page would print the shared rows
    # twice (a graph segment that already holds its axis title, plus the
    # title row added again: 9700/02/O/N/08 Q3(d)): merge them
    merged=[]
    for b in sorted(boxes,key=lambda b:(b[0],b[1],b[2])):
        if merged and not b[7] and not merged[-1][7] and merged[-1][0]==b[0] and merged[-1][1]==b[1] \
                and b[2]<merged[-1][3]-0.5:
            m=merged[-1]
            merged[-1]=(m[0],m[1],m[2],max(m[3],b[3]),m[4],m[5],min(m[6],b[6]),m[7],m[8],
                        b[9] if b[3]>m[3] else m[9])
        else:
            merged.append(b)
    boxes=merged
    for label,pno,cy0,cy1,_rt,_rb,emit_order,masks,hard_y0,hard_y1 in sorted(boxes,key=lambda b:b[6]):
        render_right=INK[pno].content_r
        render_left=CONTENT_L
        if IS_ALEVEL and not masks:
            cy0,cy1=snap_edges_to_blank(pno,cy0,cy1,render_right)
            # widen to content that sits outside the 40-560 pt column
            # (graph axis label at x=34: 9702/42/M/J/10 p.6); stay clear of
            # the margin-strip zone (<18 pt / >577 pt)
            xs=[(w[0],w[2]) for w in doc[pno].get_text('words')
                if cy0<=(w[1]+w[3])/2<=cy1 and furniture_free(doc[pno],w[:4])
                and w[0]>=18 and w[2]<=577]
            # (white-only fills are our own masks, e.g. the hidden question
            #  number at x=34-59 -- not content)
            xs+=[(d['rect'].x0,d['rect'].x1) for d in doc[pno].get_drawings()
                 if d.get('rect') is not None and cy0<=d['rect'].y0 and d['rect'].y1<=cy1
                 and d['rect'].x0>=18 and d['rect'].x1<=577
                 and not (d.get('fill') in ((1,1,1),(1.0,1.0,1.0)) and d.get('color') is None)]
            if os.environ.get('AL_DEBUG_X')==label:
                print('XS',label,pno+1,round(cy0,1),round(cy1,1),sorted(xs)[:4],sorted(xs,key=lambda t:-t[1])[:3],file=sys.stderr)
            if xs:
                render_left=min(CONTENT_L,min(a for a,_ in xs)-2)
                if render_right>=CONTENT_R-0.5:      # no examiner column on this page
                    render_right=max(render_right,max(b for _,b in xs)+2)
        pix=doc[pno].get_pixmap(
            clip=fitz.Rect(render_left,cy0,render_right,cy1),dpi=DPI)
        newH=trim_bottom_border(pix, doc[pno], cy0, S[pno])
        if newH is not None and newH<pix.height:
            frac=newH/pix.height
            new_cy1=cy0+(cy1-cy0)*frac
            pix=doc[pno].get_pixmap(
                clip=fitz.Rect(render_left,cy0,render_right,new_cy1),dpi=DPI)
            cy1=new_cy1
        image=apply_seam_masks(pix_to_image(pix),cy0,masks)
        if IS_ALEVEL and not masks:
            image=clean_edge_intruders(image,pno,render_left,cy0,cy1)
        image=trim_outer_whitespace(image)
        image=trim_trailing_orphan_label(image)
        rendered.setdefault(label,[]).append((emit_order,image,render_left))
        provenance.setdefault(label,[]).append({
            'pdf_page':pno+1,
            'clip_points':[round(render_left,2),round(cy0,2),
                           round(render_right,2),round(cy1,2)],
            'semantic_bounds_points':[round(hard_y0,2),round(hard_y1,2)],
            'two_dimensional_seam':bool(masks),
        })

    made=[]
    separator=max(1,round(8*DPI/72))
    for label,segments in sorted(rendered.items(),key=lambda kv:min(x[0] for x in kv[1])):
        segs=sorted(segments,key=lambda t:t[0])
        images=[im for _,im,_ in segs]
        if len(images)==1:
            final=images[0]
        else:
            # keep page x-alignment when segments have different left edges
            left0=min(lx for _,_,lx in segs)
            offs=[round((lx-left0)*DPI/72) for _,_,lx in segs]
            width=max(im.width+o for im,o in zip(images,offs))
            height=sum(im.height for im in images)+separator*(len(images)-1)
            final=Image.new('RGB',(width,height),'white')
            y=0
            for im,o in zip(images,offs):
                final.paste(im,(o,y)); y+=im.height+separator
        final.save(OUTDIR/f'{PREFIX}-{label}.png',format='PNG',optimize=True)
        made.append(label)
    (OUTDIR/f'{PREFIX}-split-provenance.json').write_text(json.dumps({
        'source_pdf':str(Path(SRC).resolve()),
        'prefix':PREFIX,
        'normalized_geometry':normalize_geometry,
        'response_furniture_masks':{
            str(pno+1):[list(key) for key in sorted(rects)]
            for pno,rects in sorted(response_furniture_masks.items())
        },
        'outputs':provenance,
        'manual_masks':DOT_MASKS,
    },indent=2)+'\n')
    doc.close()
    print(f'produced {len(made)} crops')
    for m in made: print('  ',m)

if __name__=='__main__':
    main()
