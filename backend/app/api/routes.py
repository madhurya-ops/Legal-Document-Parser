from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, status
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
import os
import uuid
import hashlib
import logging
import gc

from app.core.vector_store import get_retriever, add_documents_to_vector_store
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

async def process_document_to_vector_store(file_path: str, file_extension: str):
    """Process uploaded document and add it to the vector store"""
    try:
        logger.info(f"Processing document: {file_path} (type: {file_extension})")
        
        if file_extension.lower() == '.pdf':
            from pypdf import PdfReader
            
            # Check if file exists and is readable
            if not os.path.exists(file_path):
                logger.error(f"File does not exist: {file_path}")
                return
            
            file_size = os.path.getsize(file_path)
            logger.info(f"Processing PDF file: {file_path} (size: {file_size} bytes)")
            
            reader = PdfReader(file_path)
            text = ""
            total_pages = len(reader.pages)
            logger.info(f"PDF has {total_pages} pages")
            
            for page_num, page in enumerate(reader.pages):
                page_text = page.extract_text()
                text += page_text + "\n"
                logger.info(f"Extracted {len(page_text)} chars from page {page_num + 1}")
                
                # Log preview of each page's content
                page_preview = page_text[:150] if page_text else "[EMPTY PAGE]"
                logger.info(f"Page {page_num + 1} preview: {page_preview}...")
                
                # Check if extraction appears to have failed
                if len(page_text.strip()) < 10:
                    logger.warning(f"Page {page_num + 1} has very little text, extraction may have failed")
        elif file_extension.lower() == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            logger.info(f"Read {len(text)} chars from TXT file")
        elif file_extension.lower() == '.docx':
            try:
                from docx import Document as DocxDocument
                doc = DocxDocument(file_path)
                text = ""
                for paragraph in doc.paragraphs:
                    text += paragraph.text + "\n"
                logger.info(f"Extracted {len(text)} chars from DOCX file using python-docx")
            except ImportError:
                logger.warning("python-docx not installed, falling back to basic text extraction")
                # Fallback: try to read as plain text (will likely produce garbage)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()
                logger.info(f"Read {len(text)} chars from DOCX file (basic text mode - may be garbled)")
        else:
            logger.warning(f"Unsupported file type: {file_extension}")
            return
            
        logger.info(f"Total extracted text length: {len(text)} characters")
        logger.info(f"Text preview (first 200 chars): {text[:200]}...")
        
        if text.strip():
            await add_documents_to_vector_store(text, file_path)
            logger.info(f"Successfully added document {file_path} to vector store")
        else:
            logger.warning(f"No text extracted from document {file_path}")
            
    except Exception as e:
        logger.error(f"Error processing document {file_path}: {e}")
        raise

class Query(BaseModel):
    question: str
    file_content: Optional[str] = None

@router.post("/ask")
async def ask_question(query_data: Query):
    try:
        # Get retriever only when needed
        retriever = get_lazy_retriever()
        docs = retriever.invoke(query_data.question)
        
        # Debug: Log what we retrieved with enhanced debugging
        logger.info(f"Retrieved {len(docs)} documents for query: {query_data.question[:50]}...")
        for i, doc in enumerate(docs):
            doc_source = doc.metadata.get('source', 'unknown')
            doc_content = doc.page_content
            doc_preview = doc_content[:200] if doc_content else "[EMPTY CONTENT]"
            
            logger.info(f"Doc {i}: Source={doc_source}, Content length={len(doc_content)}")
            logger.info(f"Doc {i} Preview: {doc_preview}...")
            
            # Check if the content looks like PDF metadata instead of extracted text
            if any(indicator in doc_content.lower() for indicator in ['%pdf', 'obj', 'endobj', 'stream', 'endstream']):
                logger.warning(f"Doc {i} appears to contain PDF metadata instead of extracted text!")
            
            # Check if content is meaningful text
            if len(doc_content.strip()) < 50:
                logger.warning(f"Doc {i} has very short content, might be empty or corrupted")
        
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
        logger.info(f"Final context length: {len(context)} chars")
        
        # Check if we only have system/default messages (no real documents)
        has_real_documents = any(
            doc.metadata.get('source', '') != 'system' and 
            doc.metadata.get('source', '') != 'fallback' and
            len(doc.page_content.strip()) > 20 and  # Reduced threshold for smaller test documents
            'Welcome to LegalDoc' not in doc.page_content
            for doc in docs
        )
        
        if not has_real_documents and any(
            phrase in query_data.question.lower() 
            for phrase in ['this file', 'this document', 'the pdf', 'analyze', 'contents of']
        ):
            logger.info("User asking about documents but no real documents found")
            context = "NO_DOCUMENTS_UPLOADED: The user is asking about documents but no documents have been uploaded to the system yet."
        
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
    logger.info(f"Received file upload: {file.filename} from user {current_user.username}")
    
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
        
        # Process the document and add to vector store
        try:
            await process_document_to_vector_store(final_path, file_extension)
            logger.info(f"Successfully processed document {unique_filename} into vector store")
        except Exception as e:
            logger.error(f"Failed to process document into vector store: {e}")
            # Don't fail the upload if vector processing fails
        
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
