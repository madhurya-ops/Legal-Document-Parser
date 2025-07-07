from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, status
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
import logging

from app.services.ai_service import ai_service
from app.utils.pdf_parser import extract_text_from_pdf, is_pdf_file
from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models import User

router = APIRouter(prefix="/query", tags=["query"])
logger = logging.getLogger(__name__)

class QueryRequest(BaseModel):
    question: str
    file_content: Optional[str] = None
    file_name: Optional[str] = None
    tool_type: Optional[str] = None

@router.post("/ask")
async def ask_question(
    query_data: QueryRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Ask a question with optional file context"""
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
        
        # Use the AI service to generate response
        result = await ai_service.generate_response(
            user_query=query_data.question,
            context=context,
            document_type=query_data.tool_type
        )
        
        return {
            "answer": result["response"],
            "confidence_score": result["confidence_score"],
            "sources": result["sources"],
            "citations": result["citations"],
            "metadata": result["metadata"]
        }
        
    except Exception as e:
        logger.error(f"Error in /ask endpoint: {e}")
        return {
            "answer": f"I encountered an error processing your request. Please try again. Error: {str(e)[:100]}",
            "confidence_score": 0.0,
            "sources": [],
            "citations": [],
            "metadata": {"error": str(e)}
        }

@router.post("/extract-pdf-text")
async def extract_pdf_text(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user)
):
    """Extract text content from uploaded PDF file"""
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
