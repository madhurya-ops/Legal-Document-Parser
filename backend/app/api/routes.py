from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, status
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
import os
import uuid
import hashlib
import logging
import gc

from app.core.vector_store import get_retriever
from llm.client import query
from .. import crud, schemas, auth
from ..database import get_db

router = APIRouter()
logger = logging.getLogger(__name__)

# Lazy loading for retriever to reduce initial memory usage
_retriever = None

def get_lazy_retriever():
    global _retriever
    if _retriever is None:
        _retriever = get_retriever(k=5)  # Keep original k=5 for functionality
    return _retriever

class Query(BaseModel):
    question: str
    file_content: Optional[str] = None

@router.post("/ask")
async def ask_question(query_data: Query):
    try:
        # Get retriever only when needed
        retriever = get_lazy_retriever()
        docs = retriever.get_relevant_documents(query_data.question)
        
        # Limit context size to reduce memory usage while preserving functionality
        context_parts = []
        total_chars = 0
        max_chars = 3000  # Increased from 2000 to preserve more context
        
        for doc in docs:
            if total_chars + len(doc.page_content) > max_chars:
                break
            context_parts.append(doc.page_content)
            total_chars += len(doc.page_content)
        
        context = "\n\n".join(context_parts)
        
        if query_data.file_content:
            # Limit file content size but preserve more content
            file_content = query_data.file_content[:1500]  # Increased from 1000
            context = f"{file_content}\n\n{context}"
        
        answer = query(context, query_data.question)
        if not answer or not str(answer).strip():
            answer = "Sorry, the language model did not return a valid response. Please try again later."
        
        # Clear memory
        del docs, context_parts, context
        gc.collect()
        
        return {"answer": answer}
    except Exception as e:
        logger.error(f"Error in /ask endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload", response_model=schemas.DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    current_user: schemas.UserResponse = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """Upload a document with duplicate detection using memory-efficient streaming."""
    # Validate file type
    allowed_types = ['.pdf', '.docx', '.txt']
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    if file_extension not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type {file_extension} not allowed. Allowed types: {', '.join(allowed_types)}"
        )
    
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    tmp_path = os.path.join(upload_dir, f"tmp_{uuid.uuid4().hex}{file_extension}")
    sha256 = hashlib.sha256()
    file_size = 0

    try:
        # Stream file to a temporary path and calculate hash simultaneously
        with open(tmp_path, "wb") as f:
            while chunk := await file.read(8192):  # Restored to original 8192 for better performance
                sha256.update(chunk)
                f.write(chunk)
                file_size += len(chunk)

        file_hash = sha256.hexdigest()
        
        # Check for duplicate document
        existing_document = crud.check_duplicate_document(db, file_hash, str(current_user.id))
        
        if existing_document:
            return schemas.DocumentUploadResponse(
                message="Document already exists. Duplicate upload prevented.",
                document=schemas.DocumentResponse.from_orm(existing_document),
                is_duplicate=True
            )
        
        # Generate unique filename and rename the temp file
        unique_filename = f"{uuid.uuid4().hex}{file_extension}"
        final_path = os.path.join(upload_dir, unique_filename)
        os.rename(tmp_path, final_path)
        tmp_path = None # Prevent deletion in finally block

        # Create document record
        document_data = schemas.DocumentCreate(
            filename=unique_filename,
            original_filename=file.filename,
            file_hash=file_hash,
            file_size=str(file_size),
            file_type=file_extension,
            user_id=current_user.id
        )
        
        db_document = crud.create_document(db, document_data)
        
        return schemas.DocumentUploadResponse(
            message="Document uploaded successfully",
            document=schemas.DocumentResponse.from_orm(db_document),
            is_duplicate=False
        )
    finally:
        # Ensure temp file is cleaned up on exit (if not renamed)
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)
        await file.close()

@router.get("/documents", response_model=List[schemas.DocumentResponse])
async def get_user_documents(
    current_user: schemas.UserResponse = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all documents for the current user"""
    documents = crud.get_user_documents(db, str(current_user.id))
    return [schemas.DocumentResponse.from_orm(doc) for doc in documents]

@router.delete("/documents/{document_id}")
async def delete_document(
    document_id: str,
    current_user: schemas.UserResponse = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a document (only if owned by user)"""
    success = crud.delete_document(db, document_id, str(current_user.id))
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found or you don't have permission to delete it"
        )
    
    return {"message": "Document deleted successfully"}
