from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
import logging
import json

from app.schemas import ChatSessionCreate, ChatSessionResponse, ChatMessageCreate, ChatMessageResponse
from app.services import crud
from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models import User

router = APIRouter(prefix="/chat", tags=["chat"])
logger = logging.getLogger(__name__)

@router.post("/sessions", response_model=ChatSessionResponse)
async def create_chat_session(
    session_data: ChatSessionCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new chat session"""
    try:
        db_session = await crud.create_chat_session(
            db, 
            str(current_user.id), 
            session_data.session_name
        )
        return ChatSessionResponse.model_validate(db_session)
    except Exception as e:
        logger.error(f"Error creating chat session: {e}")
        raise HTTPException(status_code=500, detail="Failed to create chat session")

@router.get("/sessions", response_model=List[ChatSessionResponse])
async def get_chat_sessions(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all chat sessions for the current user"""
    try:
        sessions = await crud.get_user_chat_sessions(db, str(current_user.id))
        return [ChatSessionResponse.model_validate(session) for session in sessions]
    except Exception as e:
        logger.error(f"Error fetching chat sessions: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch chat sessions")

@router.get("/sessions/{session_id}", response_model=ChatSessionResponse)
async def get_chat_session(
    session_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific chat session"""
    try:
        session = await crud.get_chat_session(db, session_id, str(current_user.id))
        if not session:
            raise HTTPException(status_code=404, detail="Chat session not found")
        return ChatSessionResponse.model_validate(session)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching chat session: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch chat session")

@router.delete("/sessions/{session_id}")
async def delete_chat_session(
    session_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a chat session"""
    try:
        success = await crud.delete_chat_session(db, session_id, str(current_user.id))
        if not success:
            raise HTTPException(status_code=404, detail="Chat session not found")
        return {"message": "Chat session deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting chat session: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete chat session")

@router.post("/sessions/{session_id}/messages", response_model=ChatMessageResponse)
async def create_chat_message(
    session_id: str,
    message_data: ChatMessageCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Add a message to a chat session"""
    try:
        # Verify user owns the session
        session = await crud.get_chat_session(db, session_id, str(current_user.id))
        if not session:
            raise HTTPException(status_code=404, detail="Chat session not found")
        
        # Override session_id in message data
        message_data.session_id = session_id
        
        db_message = await crud.create_chat_message(db, message_data)
        return ChatMessageResponse.model_validate(db_message)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating chat message: {e}")
        raise HTTPException(status_code=500, detail="Failed to create chat message")

@router.get("/sessions/{session_id}/messages", response_model=List[ChatMessageResponse])
async def get_chat_messages(
    session_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all messages for a chat session"""
    try:
        messages = await crud.get_chat_messages(db, session_id, str(current_user.id))
        return [ChatMessageResponse.model_validate(message) for message in messages]
    except Exception as e:
        logger.error(f"Error fetching chat messages: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch chat messages")

@router.get("/sessions/{session_id}/export")
async def export_chat_session(
    session_id: str,
    format: str = "json",
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Export chat session in various formats"""
    try:
        # Verify user owns the session
        session = await crud.get_chat_session(db, session_id, str(current_user.id))
        if not session:
            raise HTTPException(status_code=404, detail="Chat session not found")
        
        # Get all messages
        messages = await crud.get_chat_messages(db, session_id, str(current_user.id))
        
        if format.lower() == "json":
            export_data = {
                "session": {
                    "id": str(session.id),
                    "name": session.session_name,
                    "created_at": session.created_at.isoformat(),
                    "updated_at": session.updated_at.isoformat() if session.updated_at else None
                },
                "messages": [
                    {
                        "id": str(msg.id),
                        "type": msg.message_type.value,
                        "content": msg.content,
                        "timestamp": msg.timestamp.isoformat(),
                        "sources": msg.sources,
                        "confidence_score": msg.confidence_score
                    }
                    for msg in messages
                ]
            }
            return export_data
        
        elif format.lower() == "txt":
            # Generate plain text format
            lines = [f"Chat Session: {session.session_name}"]
            lines.append(f"Created: {session.created_at}")
            lines.append("-" * 50)
            
            for msg in messages:
                role = "You" if msg.message_type.value == "user" else "Assistant"
                lines.append(f"\n[{msg.timestamp}] {role}:")
                lines.append(msg.content)
                if msg.confidence_score:
                    lines.append(f"(Confidence: {msg.confidence_score:.2f})")
            
            return {"content": "\n".join(lines), "format": "text"}
        
        else:
            raise HTTPException(status_code=400, detail="Unsupported export format")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error exporting chat session: {e}")
        raise HTTPException(status_code=500, detail="Failed to export chat session")
