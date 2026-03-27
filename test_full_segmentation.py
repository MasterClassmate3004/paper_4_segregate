import fitz
import re
import os

doc = fitz.open('0625_s25_qp_42.pdf')
question_pages = {}
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
                        question_pages[str(q_num)] = page_num
                        expected_q_num += 1

sorted_q = sorted([(int(k), v) for k, v in question_pages.items()])
output_files = []

for i in range(len(sorted_q)):
    q_num = sorted_q[i][0]
    start_page = sorted_q[i][1]
    if i + 1 < len(sorted_q):
        next_start = sorted_q[i+1][1]
        end_page = next_start - 1
        if end_page < start_page:
            end_page = start_page
    else:
        end_page = len(doc) - 1
        
    q_doc = fitz.open()
    for p in range(start_page, end_page + 1):
        page = doc[p]
        if "BLANK PAGE" not in page.get_text().upper():
            content_rect = None
            for b in page.get_text("blocks"):
                r = fitz.Rect(b[:4])
                if r.x0 > 30 and r.x1 < 570 and r.y0 > 60 and r.y1 < 800:
                    content_rect = r if content_rect is None else content_rect | r
                    
            for d in page.get_drawings():
                r = d["rect"]
                if r.x0 > 30 and r.x1 < 570 and r.y0 > 60 and r.y1 < 800:
                    content_rect = r if content_rect is None else content_rect | r
                    
            for img in page.get_image_info():
                r = fitz.Rect(img["bbox"])
                if r.x0 > 30 and r.x1 < 570 and r.y0 > 60 and r.y1 < 800:
                    content_rect = r if content_rect is None else content_rect | r
                    
            if content_rect is None or content_rect.is_empty:
                content_rect = fitz.Rect(45, 75, 550, 780)
            else:
                content_rect = content_rect + (-15, -2, 15, 15)  # Changed crop adjustment
                content_rect &= fitz.Rect(0, 0, page.rect.width, page.rect.height)
            
            q_doc.insert_pdf(doc, from_page=p, to_page=p)
            q_doc[-1].set_cropbox(content_rect)
    
    out_filename = f"out_q{q_num}.pdf"
    q_doc.save(out_filename)
    q_doc.close()
    output_files.append(out_filename)

print("Generated:", output_files)
