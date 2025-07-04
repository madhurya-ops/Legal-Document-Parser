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
from ..utils.pdf_parser import extract_text_from_pdf, is_pdf_file

# Optional: Import new AI service
try:
    from ..services.ai_service import ai_service
    AI_SERVICE_AVAILABLE = True
except ImportError:
    AI_SERVICE_AVAILABLE = False

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
    file_name: Optional[str] = None
    tool_type: Optional[str] = None

@router.post("/ask")
async def ask_question(query_data: Query):
    try:
        context = ""
        
        # If file content is provided, use it as primary context
        if query_data.file_content:
            # Enhanced file content processing for better analysis
            file_content = query_data.file_content[:2000]  # Increased for better context
            context = file_content
            logger.info(f"Using provided file content (length: {len(file_content)})")
        else:
            # No file content - enable general legal question answering
            context = ""
            logger.info("No file content provided, enabling general legal question mode")
        
        # Query the LLM with context (or empty context for general questions)
        answer = query(context, query_data.question)
        
        # Quick validation and response
        if answer and str(answer).strip():
            # Check if it's an error message or valid response
            answer_str = str(answer).strip()
            if len(answer_str) > 10 and not answer_str.startswith("Error:"):
                return {"answer": answer_str}
        
        # Provide immediate fallback without additional API calls
        if context and context.strip():
            # Extract key information from context for quick response
            context_preview = context[:500] + "..." if len(context) > 500 else context
            fallback_answer = f"I'm analyzing your document but experiencing some delays. Based on the content I can see: {context_preview}. Please try asking a more specific question about the document."
        else:
            fallback_answer = "I'm experiencing some technical difficulties. Please try again in a moment or rephrase your question."
        
        return {"answer": fallback_answer}
    except Exception as e:
        logger.error(f"Error in /ask endpoint: {e}")
        return {"answer": f"I encountered an error processing your request. Please try again. Error: {str(e)[:100]}"}

@router.post("/extract-pdf-text")
async def extract_pdf_text(file: UploadFile = File(...)):
    """Extract text content from uploaded PDF file."""
    try:
        # Validate file type
        if not is_pdf_file(file.filename):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File must be a PDF"
            )
        
        # Check file size
        file_size = 0
        file_content = b""
        
        # Read file content in chunks to avoid memory issues
        chunk_size = 8192
        max_size = 50 * 1024 * 1024  # 50MB limit
        
        while True:
            chunk = await file.read(chunk_size)
            if not chunk:
                break
            file_size += len(chunk)
            if file_size > max_size:
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail="File too large. Maximum size is 50MB."
                )
            file_content += chunk
        
        if not file_content:
            return {"text": "", "message": "Empty file received"}
        
        logger.info(f"Processing PDF file: {file.filename}, size: {file_size} bytes")
        
        # Extract text from PDF with timeout handling
        try:
            extracted_text = extract_text_from_pdf(file_content)
        except Exception as extraction_error:
            logger.error(f"PDF extraction error: {extraction_error}")
            return {
                "text": "", 
                "message": f"Failed to extract text: {str(extraction_error)[:200]}"
            }
        
        if not extracted_text or not extracted_text.strip():
            return {
                "text": "", 
                "message": "No text could be extracted from this PDF. The file may contain only images or be corrupted."
            }
        
        # Limit response size
        max_response_length = 50000  # 50KB of text
        if len(extracted_text) > max_response_length:
            extracted_text = extracted_text[:max_response_length] + "\n\n[Content truncated - document is very long]"
        
        logger.info(f"Successfully extracted {len(extracted_text)} characters from PDF")
        
        return {
            "text": extracted_text,
            "length": len(extracted_text),
            "message": "Text extracted successfully"
        }
        
    except Exception as e:
        logger.error(f"Error extracting PDF text: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to extract text from PDF: {str(e)}"
        )
    finally:
        await file.close()

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
