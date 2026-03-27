import fitz
import re
doc = fitz.open('0625_m25_qp_42.pdf')

question_pages = {}
for page_num in range(len(doc)):
    page = doc[page_num]
    blocks = page.get_text("blocks")
    for b in blocks:
        if b[6] == 0:  # text block
            text = b[4].strip()
            x0 = b[0]
            if x0 < 55.0:
                match = re.match(r'^(\d+)\s*\n', text)
                if match:
                    q_num = match.group(1)
                    if q_num not in question_pages:
                        question_pages[q_num] = page_num
                        print(f"Matched Q{q_num} on page {page_num+1} with x0={x0:.2f}")

print("Questions found:", question_pages)
