import fitz
doc = fitz.open('0625_m25_qp_42.pdf')

for page_num in range(15, 20):
    if page_num >= len(doc): break
    page = doc[page_num]
    blocks = page.get_text("blocks")
    for b in blocks:
        if b[6] == 0:  # text block
            text = b[4].strip()
            x0 = b[0]
            if x0 < 80.0 and text.startswith("10"):
                print(f"PAGE {page_num+1} -- X0: {x0:.2f} -- TEXT: {repr(text[:50])}")
