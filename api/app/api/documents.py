from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, status
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import uuid
import hashlib
import logging

from app.schemas import DocumentCreate, DocumentResponse, DocumentUploadResponse
from app.services import crud
from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models import User

router = APIRouter(prefix="/documents", tags=["documents"])
logger = logging.getLogger(__name__)

@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Upload a document with duplicate detection"""
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
            while chunk := await file.read(8192):
                sha256.update(chunk)
                f.write(chunk)
                file_size += len(chunk)

        file_hash = sha256.hexdigest()
        
        # Check for duplicate document
        existing_document = await crud.check_duplicate_document(db, file_hash, str(current_user.id))
        
        if existing_document:
            return DocumentUploadResponse(
                message="Document already exists. Duplicate upload prevented.",
                document=DocumentResponse.model_validate(existing_document),
                is_duplicate=True
            )
        
        # Generate unique filename and rename the temp file
        unique_filename = f"{uuid.uuid4().hex}{file_extension}"
        final_path = os.path.join(upload_dir, unique_filename)
        os.rename(tmp_path, final_path)
        tmp_path = None  # Prevent deletion in finally block

        # Create document record
        document_data = DocumentCreate(
            filename=unique_filename,
            original_filename=file.filename,
            file_path=final_path,
            file_hash=file_hash,
            file_size=file_size,
            file_type=file_extension,
            user_id=current_user.id
        )
        
        db_document = await crud.create_document(db, document_data)
        
        return DocumentUploadResponse(
            message="Document uploaded successfully",
            document=DocumentResponse.model_validate(db_document),
            is_duplicate=False
        )
    finally:
        # Ensure temp file is cleaned up on exit (if not renamed)
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)
        await file.close()

@router.get("/", response_model=List[DocumentResponse])
async def get_user_documents(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all documents for the current user"""
    documents = await crud.get_user_documents(db, str(current_user.id))
    return [DocumentResponse.model_validate(doc) for doc in documents]

@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a document (only if owned by user)"""
    success = await crud.delete_document(db, document_id, str(current_user.id))
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found or you don't have permission to delete it"
        )
    
    return {"message": "Document deleted successfully"}

@router.get("/{document_id}/analyses")
async def get_document_analyses(
    document_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all analyses for a specific document"""
    try:
        analyses = await crud.get_document_analyses(db, document_id, str(current_user.id))
        return analyses
    except Exception as e:
        logger.error(f"Error fetching document analyses: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch document analyses")
