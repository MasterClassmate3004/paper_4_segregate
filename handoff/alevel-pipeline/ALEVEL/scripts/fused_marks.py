"""Split dotted-leader tokens that carry a fused mark into two words.

Many Cambridge PDFs set the mark with no space after the answer line, so
PyMuPDF returns one word '..........[3]' (1,683 tokens in 134 9702 papers).
Every mark-based rule (part ends at its [n]; lone [n] kept under the prompt)
then misses the mark -- 9702/42/O/N/16 Q11(b) lost its prompt to a phantom
(c) stem.  install() wraps Page.get_text so 'words' output returns
'..........' and '[3]' as separate words, with exact boxes taken from the
PDF's own character positions.  Splitter and verifiers all call install(),
so they see identical words.
"""

from __future__ import annotations

import re

import pymupdf as fitz

FUSED_RE = re.compile(r"^(.*?[.…]{3,})(\[\d+\])$")
# a label fused to its answer leader: 'AB.........' ('Distance from AB......',
# 9709/51/M/J/19 Q6(i)) -> 'AB' + the leader; opt-in (Maths), see install()
LEADER_RE = re.compile(r"^(.*?[^.…\s])([.…]{10,})$")
_orig = fitz.Page.get_text
_leaders = False


def _char_split_x(page, rect, mark):
    """x of the '[' that starts `mark` inside `rect`, from rawdict chars."""
    raw = _orig(page, "rawdict", clip=fitz.Rect(rect) + (-1, -1, 1, 1))
    # only this row's characters: a '[Turn over' just below would otherwise
    # interleave with the mark (9700/42/F/M/18 p9)
    chars = [c for b in raw.get("blocks", []) for l in b.get("lines", [])
             for s in l.get("spans", []) for c in s.get("chars", [])
             if rect[1] <= (c["bbox"][1] + c["bbox"][3]) / 2 <= rect[3]]
    chars.sort(key=lambda c: c["bbox"][0])
    text = "".join(c["c"] for c in chars)
    k = text.rfind(mark)
    if k < 0:
        return None
    return chars[k]["bbox"][0]


def _split_words(page, words):
    out = []
    for w in words:
        if _leaders and isinstance(w[4], str):
            ml = LEADER_RE.match(w[4])
            if ml and re.search(r"[A-Za-z0-9)]$", ml[1]):
                x = _char_split_x(page, w[:4], ml[2])
                if x is not None and w[0] < x < w[2]:
                    out.append((w[0], w[1], x, w[3], ml[1]) + tuple(w[5:]))
                    w = (x, w[1], w[2], w[3], ml[2]) + tuple(w[5:])
        m = FUSED_RE.match(w[4]) if isinstance(w[4], str) else None
        if not m:
            out.append(w)
            continue
        x = _char_split_x(page, w[:4], m[2])
        if x is None or not (w[0] < x < w[2]):
            out.append(w)
            continue
        out.append((w[0], w[1], x, w[3], m[1]) + tuple(w[5:]))
        out.append((x, w[1], w[2], w[3], m[2]) + tuple(w[5:]))
    return out


def _get_text(self, option="text", *args, **kwargs):
    res = _orig(self, option, *args, **kwargs)
    if option == "words":
        res = _split_words(self, res)
    return res


def install(leaders: bool = False) -> None:
    """leaders=True also splits label-fused leaders (Maths prefixes only, so
    approved Physics/Chemistry/Biology words are unchanged)."""
    global _leaders
    _leaders = leaders
    if fitz.Page.get_text is not _get_text:
        fitz.Page.get_text = _get_text
