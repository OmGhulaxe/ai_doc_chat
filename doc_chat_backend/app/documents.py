from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
import os
from unstructured.partition.auto import partition
from datetime import datetime
from app.models import Document
from sqlalchemy.orm import Session
from app.database import get_db
from typing import List
from pydantic import BaseModel
from app import models
from app import schemas
from app.auth import get_current_user
from app.models import User 



class DocumentList(BaseModel):
    documents: List[str]
router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_document(filename: str, content: str, user_id: int, db: Session):
    doc = Document(
        filename=filename,
        content=content,
        user_id=user_id,  # ✅ add user_id here
        is_indexed=False 
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    try:
        elements = partition(filename=file_path)
        full_content = "\n".join([el.text for el in elements if hasattr(el, 'text') and el.text])
        save_document(filename=file.filename, content=full_content, user_id=current_user.id, db=db)
        return {
            "filename": file.filename,
            "content_snippet": full_content or "",
            "uploaded_at": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Parsing failed: {str(e)}")



@router.get("/documents", response_model=List[schemas.DocumentResponse])
def list_documents(db: Session = Depends(get_db)):
    return db.query(models.Document).all()


@router.get("/documents/{document_id}", response_model=schemas.DocumentResponse)
def get_document(document_id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    # Ensure content is not None
    if doc.content is None:
        doc.content = ""
    return doc
