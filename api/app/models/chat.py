"""
Chat Models
===========

Chat session and message models for AI interactions.
"""

import enum
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Float, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..core.database import Base


class MessageType(enum.Enum):
    """Message type enumeration."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ChatSession(Base):
    """Chat session model for organizing conversations."""
    
    __tablename__ = "chat_sessions"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Session information
    name = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    
    # Session metadata
    message_count = Column(Integer, default=0)
    total_tokens = Column(Integer, default=0)
    
    # Session settings
    model_settings = Column(JSONB, nullable=True)  # AI model preferences
    context_documents = Column(JSONB, nullable=True)  # Referenced document IDs
    
    # Session status
    is_active = Column(String(20), default="active")  # active, archived, deleted
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_message_at = Column(DateTime(timezone=True), nullable=True)
    
    # Foreign keys
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="chat_sessions")
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")
    
    def __repr__(self):
        """String representation of chat session."""
        return f"<ChatSession(id={self.id}, name={self.name})>"
    
    @property
    def display_name(self) -> str:
        """Get display name for the session."""
        if self.name:
            return self.name
        elif self.created_at:
            return f"Chat {self.created_at.strftime('%Y-%m-%d %H:%M')}"
        else:
            return f"Chat {str(self.id)[:8]}"
    
    def add_document_context(self, document_id: str):
        """Add document to session context."""
        if self.context_documents is None:
            self.context_documents = []
        if document_id not in self.context_documents:
            self.context_documents.append(document_id)
    
    def remove_document_context(self, document_id: str):
        """Remove document from session context."""
        if self.context_documents and document_id in self.context_documents:
            self.context_documents.remove(document_id)
    
    def update_message_stats(self):
        """Update message count and last message timestamp."""
        self.message_count = len(self.messages)
        if self.messages:
            self.last_message_at = max(msg.created_at for msg in self.messages)
    
    def to_dict(self) -> dict:
        """Convert session to dictionary."""
        return {
            "id": str(self.id),
            "name": self.name,
            "display_name": self.display_name,
            "description": self.description,
            "message_count": self.message_count,
            "total_tokens": self.total_tokens,
            "model_settings": self.model_settings,
            "context_documents": self.context_documents or [],
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_message_at": self.last_message_at.isoformat() if self.last_message_at else None,
            "user_id": str(self.user_id)
        }


class ChatMessage(Base):
    """Chat message model for individual messages."""
    
    __tablename__ = "chat_messages"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Message content
    content = Column(Text, nullable=False)
    message_type = Column(String(20), nullable=False)  # user, assistant, system
    
    # AI response metadata
    model_name = Column(String(100), nullable=True)
    token_count = Column(Integer, nullable=True)
    processing_time = Column(Float, nullable=True)
    confidence_score = Column(Float, nullable=True)
    
    # Sources and citations
    sources = Column(JSONB, nullable=True)  # Referenced documents/sections
    citations = Column(JSONB, nullable=True)  # Legal citations
    
    # Message metadata
    message_metadata = Column(JSONB, nullable=True)
    parent_message_id = Column(UUID(as_uuid=True), nullable=True)  # For threading
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Foreign keys
    session_id = Column(UUID(as_uuid=True), ForeignKey("chat_sessions.id"), nullable=False)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=True)
    
    # Relationships
    session = relationship("ChatSession", back_populates="messages")
    document = relationship("Document", back_populates="chat_messages")
    
    def __repr__(self):
        """String representation of chat message."""
        content_preview = self.content[:50] + "..." if len(self.content) > 50 else self.content
        return f"<ChatMessage(id={self.id}, type={self.message_type}, content='{content_preview}')>"
    
    @property
    def is_user_message(self) -> bool:
        """Check if message is from user."""
        return self.message_type == MessageType.USER.value
    
    @property
    def is_assistant_message(self) -> bool:
        """Check if message is from assistant."""
        return self.message_type == MessageType.ASSISTANT.value
    
    @property
    def is_system_message(self) -> bool:
        """Check if message is system message."""
        return self.message_type == MessageType.SYSTEM.value
    
    @property
    def word_count(self) -> int:
        """Get word count of message content."""
        return len(self.content.split()) if self.content else 0
    
    def add_source(self, source_type: str, source_id: str, relevance: float = None):
        """Add source reference to message."""
        if self.sources is None:
            self.sources = []
        
        source = {
            "type": source_type,
            "id": source_id,
            "relevance": relevance
        }
        self.sources.append(source)
    
    def add_citation(self, citation_text: str, citation_type: str = "legal"):
        """Add legal citation to message."""
        if self.citations is None:
            self.citations = []
        
        citation = {
            "text": citation_text,
            "type": citation_type,
            "added_at": datetime.utcnow().isoformat()
        }
        self.citations.append(citation)
    
    def to_dict(self) -> dict:
        """Convert message to dictionary."""
        return {
            "id": str(self.id),
            "content": self.content,
            "message_type": self.message_type,
            "model_name": self.model_name,
            "token_count": self.token_count,
            "processing_time": self.processing_time,
            "confidence_score": self.confidence_score,
            "word_count": self.word_count,
            "sources": self.sources or [],
            "citations": self.citations or [],
            "metadata": self.message_metadata,
            "parent_message_id": str(self.parent_message_id) if self.parent_message_id else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "session_id": str(self.session_id),
            "document_id": str(self.document_id) if self.document_id else None,
            "is_user_message": self.is_user_message,
            "is_assistant_message": self.is_assistant_message,
            "is_system_message": self.is_system_message
        }
