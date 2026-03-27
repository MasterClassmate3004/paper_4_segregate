import fitz
import re
import traceback

try:
    doc = fitz.open('0625_s25_qp_42.pdf')
    expected_q_num = 1
    found = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("blocks")
        for b in blocks:
            if b[6] == 0:  # text block
                text = b[4].strip()
                x0 = b[0]
                if x0 < 55.0:
                    match = re.match(r'^(\d+)\s', text)
                    if match:
                        q_num = int(match.group(1))
                        if q_num == expected_q_num:
                            found.append((q_num, page_num+1, text[:30]))
                            expected_q_num += 1
                        else:
                            # Log skipped ones just in case
                            print(f"Skipped {q_num} (expected {expected_q_num}) at page {page_num+1}: {repr(text[:30])}")

    for f in found:
        print(f)
except Exception as e:
    traceback.print_exc()
