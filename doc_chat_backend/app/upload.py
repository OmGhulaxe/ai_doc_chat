from fastapi import APIRouter, File, UploadFile
import os
from app.parser import parse_file

router = APIRouter()

UPLOAD_DIR = "uploads"
PARSED_DIR = "parsed"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PARSED_DIR, exist_ok=True)

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    filepath = os.path.join(UPLOAD_DIR, file.filename)
    with open(filepath, "wb") as f:
        f.write(await file.read())
    
    parsed_text = parse_file(filepath)
    
    parsed_path = os.path.join(PARSED_DIR, file.filename + ".txt")
    with open(parsed_path, "w") as f:
        f.write(parsed_text)
    
    return {"filename": file.filename, "parsed": parsed_text[:200] + "..."}
