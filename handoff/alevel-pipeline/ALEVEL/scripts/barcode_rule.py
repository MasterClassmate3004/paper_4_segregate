"""Shared rule: is a PDF text span a Cambridge barcode/QR glyph run?

Font names cannot be used: 2018-2024 papers put barcodes in the 'AllAndNone'
font, but 2025+ papers set ALL text in a font of that name.  Barcode runs are
recognised by their glyphs (control characters, or mostly Latin-Extended
garbage like 'ĬÑù¿Ġ³íÉ') AND their position in the header/footer band.
"""

import re


def is_barcode_span(text: str, y0: float, y1: float) -> bool:
    t = text.strip()
    if len(t) < 3:
        return False
    if not (y1 < 80 or y0 > 780):
        return False
    # readable words are never a barcode: 2019+ prompts can carry '\x07'
    # tab-marker control characters ('\x07Circle the point ... graph.\x07',
    # 9701/51/O/N/20 Q2(b)(ii) was whited out as a barcode)
    if re.search(r"[A-Za-z]{3,}\s+[A-Za-z]{3,}", t):
        return False
    ctrl = sum(1 for c in t if ord(c) < 32)
    ext = sum(1 for c in t if 0x100 <= ord(c) <= 0x24F or 0x80 <= ord(c) < 0xC0)
    nonascii = sum(1 for c in t if ord(c) > 127)
    return (ctrl >= 2 or ext / len(t) >= 0.5 or (t.startswith(",") and t.endswith(",") and ctrl >= 1)
            or (" " not in t and len(t) >= 8 and nonascii / len(t) >= 0.6))
