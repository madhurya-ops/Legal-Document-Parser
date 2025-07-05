"""Chat Service for LegalDoc application."""

import logging
import asyncio
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional, AsyncGenerator
from sqlalchemy.orm import Session

from ..exceptions import NotFoundError, ValidationError, DatabaseError
from ..models import ChatSession, ChatMessage, MessageType, User
from ..schemas import ChatSessionCreate, ChatMessageCreate
from .ai_service import AIService
from .document_service import DocumentService

logger = logging.getLogger(__name__)


class ChatResponse:
    """Chat response wrapper."""
    
    def __init__(
        self,
        success: bool,
        message: Optional[str] = None,
        sources: Optional[List[Dict[str, Any]]] = None,
        suggested_questions: Optional[List[str]] = None,
        error: Optional[str] = None
    ):
        self.success = success
        self.message = message
        self.sources = sources or []
        self.suggested_questions = suggested_questions or []
        self.error = error


class WebSocketManager:
    """WebSocket connection manager."""
    
    def __init__(self):
        self.active_connections: Dict[str, Any] = {}
        self.message_queues: Dict[str, asyncio.Queue] = {}
    
    async def connect(self, client_id: str, websocket: Any = None):
        """Register new WebSocket connection."""
        if websocket:
            self.active_connections[client_id] = websocket
        self.message_queues[client_id] = asyncio.Queue()
    
    async def disconnect(self, client_id: str):
        """Remove WebSocket connection."""
        if client_id in self.active_connections:
            del self.active_connections[client_id]
        if client_id in self.message_queues:
            del self.message_queues[client_id]
    
    async def send(self, client_id: str, message: Dict[str, Any]):
        """Send message to specific client."""
        if client_id in self.message_queues:
            await self.message_queues[client_id].put(message)
    
    async def listen(self, client_id: str) -> AsyncGenerator[Dict[str, Any], None]:
        """Listen for messages from a specific client."""
        if client_id not in self.message_queues:
            raise ValueError(f"No message queue for client {client_id}")
        
        while True:
            try:
                message = await self.message_queues[client_id].get()
                if message is None:  # Signal to stop
                    break
                yield message
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in WebSocket listener: {str(e)}")
                break


class ChatService:
    """Chat service for managing conversations and AI interactions."""
    
    def __init__(self):
        self.ai_service = AIService()
        self.document_service = None  # Will be initialized when needed
        self.websocket_manager = WebSocketManager()
    
    async def create_session(
        self,
        user_id: str,
        session_name: Optional[str] = None,
        db: Session = None
    ) -> ChatSession:
        """
        Create new chat session.
        
        Features:
        - Session initialization
        - Context setup
        - User association
        """
        try:
            if not session_name:
                session_name = f"Session {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}"
            
            session = ChatSession(
                id=uuid.uuid4(),
                user_id=uuid.UUID(user_id),
                session_name=session_name,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            if db:
                db.add(session)
                db.commit()
                db.refresh(session)
            
            logger.info(f"Created chat session {session.id} for user {user_id}")
            return session
            
        except Exception as e:
            logger.error(f"Error creating chat session: {str(e)}")
            if db:
                db.rollback()
            raise DatabaseError(f"Failed to create chat session: {str(e)}")
    
    async def send_message(
        self,
        session_id: str,
        user_id: str,
        message: str,
        document_ids: Optional[List[str]] = None,
        db: Session = None
    ) -> ChatResponse:
        """
        Process and respond to user messages.
        
        Features:
        - Context-aware responses
        - Document reference
        - Error handling
        """
        try:
            # Validate session exists and belongs to user
            session = await self._get_session(session_id, user_id, db)
            if not session:
                raise NotFoundError("ChatSession", session_id)
            
            # Get relevant document context if documents are referenced
            context = ""
            if document_ids and self.document_service:
                context = await self.document_service.get_document_context(
                    document_ids, message
                )
            
            # Get conversation history
            chat_history = await self._get_chat_history_for_ai(session_id, db)
            
            # Generate AI response with context
            ai_response = await self.ai_service.generate_response(
                query=message,
                context=context,
                conversation_history=chat_history,
                user_id=user_id
            )
            
            # Save user message
            if db:
                user_msg = ChatMessage(
                    id=uuid.uuid4(),
                    session_id=uuid.UUID(session_id),
                    message_type=MessageType.USER,
                    content=message,
                    timestamp=datetime.utcnow()
                )
                db.add(user_msg)
                
                # Save AI response
                ai_msg = ChatMessage(
                    id=uuid.uuid4(),
                    session_id=uuid.UUID(session_id),
                    message_type=MessageType.ASSISTANT,
                    content=ai_response.text,
                    sources=ai_response.sources,
                    confidence_score=ai_response.confidence,
                    timestamp=datetime.utcnow()
                )
                db.add(ai_msg)
                
                # Update session timestamp
                session.updated_at = datetime.utcnow()
                db.commit()
            
            return ChatResponse(
                success=True,
                message=ai_response.text,
                sources=ai_response.sources,
                suggested_questions=ai_response.suggested_questions
            )
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            if db:
                db.rollback()
            return ChatResponse(
                success=False,
                error=f"Failed to process message: {str(e)}"
            )
    
    async def stream_response(
        self,
        session_id: str,
        user_id: str,
        message: str,
        document_ids: Optional[List[str]] = None,
        db: Session = None
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Stream AI response in real-time.
        
        Features:
        - Token-by-token streaming
        - Partial updates
        - Error handling
        - Performance optimization
        """
        try:
            # Initialize streaming session
            stream_id = str(uuid.uuid4())
            await self.websocket_manager.connect(stream_id)
            
            # Process message in background
            asyncio.create_task(
                self._process_stream(
                    stream_id, session_id, user_id, message, document_ids, db
                )
            )
            
            # Stream response chunks
            async for chunk in self.websocket_manager.listen(stream_id):
                yield chunk
                
        except Exception as e:
            logger.error(f"Stream error: {str(e)}")
            yield {"type": "error", "content": "Stream error occurred"}
            
        finally:
            await self.websocket_manager.disconnect(stream_id)
    
    async def get_chat_history(
        self,
        session_id: str,
        user_id: str,
        limit: int = 20,
        offset: int = 0,
        db: Session = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve chat history with pagination.
        
        Features:
        - Pagination support
        - Efficient querying
        - Message formatting
        """
        try:
            if not db:
                return []
            
            # Verify session belongs to user
            session = db.query(ChatSession).filter(
                ChatSession.id == uuid.UUID(session_id),
                ChatSession.user_id == uuid.UUID(user_id)
            ).first()
            
            if not session:
                raise NotFoundError("ChatSession", session_id)
            
            # Get messages with pagination
            messages = db.query(ChatMessage).filter(
                ChatMessage.session_id == uuid.UUID(session_id)
            ).order_by(ChatMessage.timestamp.asc()).offset(offset).limit(limit).all()
            
            return [
                {
                    "id": str(msg.id),
                    "type": msg.message_type.value,
                    "content": msg.content,
                    "sources": msg.sources,
                    "confidence": msg.confidence_score,
                    "timestamp": msg.timestamp.isoformat()
                }
                for msg in messages
            ]
            
        except Exception as e:
            logger.error(f"Error fetching chat history: {str(e)}")
            return []
    
    async def get_user_sessions(
        self,
        user_id: str,
        limit: int = 20,
        offset: int = 0,
        db: Session = None
    ) -> List[Dict[str, Any]]:
        """Get user's chat sessions."""
        try:
            if not db:
                return []
            
            sessions = db.query(ChatSession).filter(
                ChatSession.user_id == uuid.UUID(user_id)
            ).order_by(ChatSession.updated_at.desc()).offset(offset).limit(limit).all()
            
            return [
                {
                    "id": str(session.id),
                    "name": session.session_name,
                    "created_at": session.created_at.isoformat(),
                    "updated_at": session.updated_at.isoformat() if session.updated_at else None,
                    "message_count": len(session.messages)
                }
                for session in sessions
            ]
            
        except Exception as e:
            logger.error(f"Error fetching user sessions: {str(e)}")
            return []
    
    async def delete_session(
        self,
        session_id: str,
        user_id: str,
        db: Session = None
    ) -> bool:
        """
        Delete chat session and associated messages.
        
        Features:
        - Session removal
        - Message cleanup
        - Associated data cleanup
        """
        try:
            if not db:
                return False
            
            # Verify session belongs to user
            session = db.query(ChatSession).filter(
                ChatSession.id == uuid.UUID(session_id),
                ChatSession.user_id == uuid.UUID(user_id)
            ).first()
            
            if not session:
                raise NotFoundError("ChatSession", session_id)
            
            # Delete messages first (due to foreign key constraints)
            db.query(ChatMessage).filter(
                ChatMessage.session_id == uuid.UUID(session_id)
            ).delete()
            
            # Delete session
            db.delete(session)
            db.commit()
            
            logger.info(f"Deleted chat session {session_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting session: {str(e)}")
            if db:
                db.rollback()
            return False
    
    async def _get_session(
        self, 
        session_id: str, 
        user_id: str, 
        db: Session = None
    ) -> Optional[ChatSession]:
        """Helper method to retrieve and validate session."""
        if not db:
            return None
        
        return db.query(ChatSession).filter(
            ChatSession.id == uuid.UUID(session_id),
            ChatSession.user_id == uuid.UUID(user_id)
        ).first()
    
    async def _get_chat_history_for_ai(
        self,
        session_id: str,
        db: Session = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get recent chat history formatted for AI context."""
        if not db:
            return []
        
        messages = db.query(ChatMessage).filter(
            ChatMessage.session_id == uuid.UUID(session_id)
        ).order_by(ChatMessage.timestamp.desc()).limit(limit).all()
        
        # Reverse to get chronological order
        messages.reverse()
        
        return [
            {
                "role": "user" if msg.message_type == MessageType.USER else "assistant",
                "content": msg.content
            }
            for msg in messages
        ]
    
    async def _process_stream(
        self,
        stream_id: str,
        session_id: str,
        user_id: str,
        message: str,
        document_ids: Optional[List[str]] = None,
        db: Session = None
    ) -> None:
        """Background task to process and stream response."""
        try:
            # Validate session
            session = await self._get_session(session_id, user_id, db)
            if not session:
                await self.websocket_manager.send(stream_id, {
                    "type": "error",
                    "content": "Session not found"
                })
                return
            
            # Save user message
            if db:
                user_msg = ChatMessage(
                    id=uuid.uuid4(),
                    session_id=uuid.UUID(session_id),
                    message_type=MessageType.USER,
                    content=message,
                    timestamp=datetime.utcnow()
                )
                db.add(user_msg)
                db.commit()
            
            # Get document context if available
            context = ""
            if document_ids and self.document_service:
                context = await self.document_service.get_document_context(
                    document_ids, message
                )
            
            # Get conversation history
            chat_history = await self._get_chat_history_for_ai(session_id, db)
            
            # Generate and stream AI response
            full_response = ""
            async for chunk in self.ai_service.stream_response(
                message=message,
                context=context,
                chat_history=chat_history,
                user_id=user_id
            ):
                full_response += chunk
                await self.websocket_manager.send(stream_id, {
                    "type": "chunk",
                    "content": chunk
                })
            
            # Save complete AI response
            if db and full_response:
                ai_msg = ChatMessage(
                    id=uuid.uuid4(),
                    session_id=uuid.UUID(session_id),
                    message_type=MessageType.ASSISTANT,
                    content=full_response,
                    timestamp=datetime.utcnow()
                )
                db.add(ai_msg)
                
                # Update session timestamp
                session.updated_at = datetime.utcnow()
                db.commit()
            
            # Mark end of stream
            await self.websocket_manager.send(stream_id, {
                "type": "end"
            })
            
        except Exception as e:
            logger.error(f"Error in stream processing: {str(e)}")
            await self.websocket_manager.send(stream_id, {
                "type": "error",
                "content": "An error occurred while processing your request"
            })
        finally:
            await self.websocket_manager.disconnect(stream_id)
# update Sun Jul  6 02:54:59 IST 2025
