from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, status
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
import os
import uuid

from app.core.vector_store import get_retriever
from llm.client import query
from .. import crud, schemas, auth
from ..database import get_db

router = APIRouter()

# Initialize retriever once at module level
retriever = get_retriever(k=5)

class Query(BaseModel):
    question: str
    file_content: Optional[str] = None

@router.post("/ask")
async def ask_question(query_data: Query):
    try:
        docs = retriever.get_relevant_documents(query_data.question)
        context = "\n\n".join([doc.page_content for doc in docs])
        if query_data.file_content:
            context = f"{query_data.file_content}\n\n{context}"
        answer = query(context, query_data.question)
        if not answer or not str(answer).strip():
            answer = "Sorry, the language model did not return a valid response. Please try again later."
        return {"answer": answer}
    except Exception as e:
        print("Error in /ask endpoint:", e)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload", response_model=schemas.DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    current_user: schemas.UserResponse = Depends(auth.get_current_active_user),
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
    
    # Read file content
    file_content = await file.read()
    
    # Calculate file hash for duplicate detection
    file_hash = crud.calculate_file_hash(file_content)
    
    # Check for duplicate document (same user, same hash)
    existing_document = crud.check_duplicate_document(db, file_hash, str(current_user.id))
    
    if existing_document:
        return schemas.DocumentUploadResponse(
            message="Document already exists. Duplicate upload prevented.",
            document=schemas.DocumentResponse.from_orm(existing_document),
            is_duplicate=True
        )
    
    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    
    # Create document record
    document_data = schemas.DocumentCreate(
        filename=unique_filename,
        original_filename=file.filename,
        file_hash=file_hash,
        file_size=str(len(file_content)),
        file_type=file_extension,
        user_id=current_user.id
    )
    
    # Save document to database
    db_document = crud.create_document(db, document_data)
    
    # Save file to disk
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    file_path = os.path.join(upload_dir, unique_filename)
    with open(file_path, "wb") as f:
        f.write(file_content)
    
    return schemas.DocumentUploadResponse(
        message="Document uploaded successfully",
        document=schemas.DocumentResponse.from_orm(db_document),
        is_duplicate=False
    )

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
