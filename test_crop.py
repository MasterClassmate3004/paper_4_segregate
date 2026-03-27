import fitz

doc = fitz.open('0625_m25_qp_42.pdf')
out_doc = fitz.open()

safe_rect = fitz.Rect(45, 75, 550, 780)

for p in range(1, 4):  # Let's test on page 2, 3, 4 (index 1, 2, 3)
    page = doc[p]
    
    # We want to find the union of bboxes for all content within safe_rect
    content_rect = fitz.Rect(550, 780, 45, 75) # Inverse rect to start
    
    # 1. Text blocks
    for b in page.get_text("blocks"):
        r = fitz.Rect(b[:4])
        # If it intersects safe_rect and is mostly inside
        if safe_rect.intersects(r):
            # To avoid the side margins being caught if they overlap slightly
            if r.x0 >= 40 and r.x1 <= 560 and r.y0 >= 70 and r.y1 <= 790:
                content_rect |= r
                
    # 2. Drawings
    for d in page.get_drawings():
        r = d["rect"]
        if safe_rect.intersects(r):
            if r.x0 >= 40 and r.x1 <= 560 and r.y0 >= 70 and r.y1 <= 790:
                content_rect |= r
                
    # 3. Images
    for img in page.get_images():
        r = page.get_image_bbox(img)
        if safe_rect.intersects(r):
             if r.x0 >= 40 and r.x1 <= 560 and r.y0 >= 70 and r.y1 <= 790:
                content_rect |= r
                
    if content_rect.is_empty or content_rect.x0 >= content_rect.x1 or content_rect.y0 >= content_rect.y1:
        # Fallback to safe_rect if nothing found
        content_rect = safe_rect
    else:
        # Add a small padding (e.g., 10 points)
        content_rect = content_rect + (-10, -10, 10, 10)
        # Ensure it doesn't exceed the page or safe_rect totally
        content_rect &= fitz.Rect(0, 0, page.rect.width, page.rect.height)
        
    print(f"Page {p+1} content rect: {content_rect}")
    page.set_cropbox(content_rect)
    out_doc.insert_pdf(doc, from_page=p, to_page=p)

out_doc.save("test_crop_output.pdf")
out_doc.close()
doc.close()
