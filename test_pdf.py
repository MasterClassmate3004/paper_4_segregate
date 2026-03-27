import fitz
doc = fitz.open('0625_m25_qp_42.pdf')
for i in range(min(5, len(doc))):
    page = doc[i]
    print(f"--- PAGE {i+1} ---")
    blocks = page.get_text("blocks")
    for b in blocks:
        if b[6] == 0: # text block
            text = b[4].strip()
            if text:
                print(f"X0: {b[0]:.2f}, Y0: {b[1]:.2f} - TEXT: {repr(text[:50])}")
