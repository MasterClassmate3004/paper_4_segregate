import fitz  # PyMuPDF
import re
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import os
import shutil

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)
app.mount("/output", StaticFiles(directory=OUTPUT_DIR), name="output")

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    doc = fitz.open(temp_path)
    base_name = os.path.splitext(file.filename)[0]
    
    question_pages = {}
    expected_q_num = 1
    
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
                            question_pages[str(q_num)] = page_num
                            expected_q_num += 1
                            
    if not question_pages:
        doc.close()
        os.remove(temp_path)
        return JSONResponse(status_code=400, content={"message": "No questions detected. Make sure the PDF follows the standard paper format."})
        
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
        
        valid_pages = []
        for p in range(start_page, end_page + 1):
            page = doc[p]
            if "BLANK PAGE" not in page.get_text().upper():
                content_rect = None
                
                # Check all texts, drawings, and images in the safe zone
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
                    # Expand by 15 points on sides, and expand 4 points upwards (-4) for safe text padding
                    content_rect = content_rect + (-15, -4, 15, 15)
                    content_rect &= fitz.Rect(0, 0, page.rect.width, page.rect.height)
                
                valid_pages.append((p, content_rect))
                
        if valid_pages:
            total_height = sum(rect.height for _, rect in valid_pages)
            max_width = max(rect.width for _, rect in valid_pages)
            
            new_page = q_doc.new_page(width=max_width, height=total_height)
            
            current_y = 0
            for p, rect in valid_pages:
                dest_rect = fitz.Rect(0, current_y, rect.width, current_y + rect.height)
                new_page.show_pdf_page(dest_rect, doc, p, clip=rect)
                current_y += rect.height
        
        out_filename = f"{base_name}_q{q_num}.pdf"
        out_path = os.path.join(OUTPUT_DIR, out_filename)
        q_doc.save(out_path)
        q_doc.close()
        output_files.append(out_filename)
        
    doc.close()
    os.remove(temp_path)
    
    return {"message": "Success", "files": output_files}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
