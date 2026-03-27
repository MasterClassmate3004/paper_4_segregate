import fitz, re

doc = fitz.open('0625_m25_qp_42.pdf')
expected_q_num = 1
for page_num in range(len(doc)):
    page = doc[page_num]
    blocks = page.get_text("blocks")
    for b in blocks:
        if b[6] == 0:
            text = b[4].strip()
            x0 = b[0]
            if x0 < 55.0:
                match = re.match(r'^(\d+)\s', text)
                if match:
                    q_num = int(match.group(1))
                    if q_num == expected_q_num:
                        print(f"Matched Q{q_num} on page {page_num+1}")
                        expected_q_num += 1
                    else:
                        print(f"  Passed by: {q_num} on page {page_num+1} (expected {expected_q_num}): {repr(text[:20])}")
