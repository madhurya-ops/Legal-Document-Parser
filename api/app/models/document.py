"""
Document Model
==============

Document data model for file management and analysis.
"""

import enum
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Text, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..core.database import Base


class DocumentStatus(enum.Enum):
    """Document processing status."""
    UPLOADING = "uploading"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    ARCHIVED = "archived"


class DocumentType(enum.Enum):
    """Document type classification."""
    CONTRACT = "contract"
    LEGAL_BRIEF = "legal_brief"
    CASE_FILE = "case_file"
    REGULATION = "regulation"
    POLICY = "policy"
    OTHER = "other"


class Document(Base):
    """Document model for file storage and metadata."""
    
    __tablename__ = "documents"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # File information
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_hash = Column(String(64), unique=True, index=True, nullable=False)
    file_size = Column(Integer, nullable=False)
    file_type = Column(String(10), nullable=False)  # .pdf, .docx, etc.
    mime_type = Column(String(100), nullable=True)
    
    # Document classification
    document_type = Column(String(50), default=DocumentType.OTHER.value)
    title = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    
    # Processing status
    status = Column(String(20), default=DocumentStatus.UPLOADING.value)
    processing_error = Column(Text, nullable=True)
    
    # Content
    extracted_text = Column(Text, nullable=True)
    text_preview = Column(String(1000), nullable=True)  # First 1000 chars
    page_count = Column(Integer, nullable=True)
    word_count = Column(Integer, nullable=True)
    
    # Metadata
    document_metadata = Column(JSONB, nullable=True)
    tags = Column(JSONB, nullable=True)  # User-defined tags
    
    # Privacy and sharing
    is_public = Column(Boolean, default=False)
    shared_with = Column(JSONB, nullable=True)  # List of user IDs
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_accessed = Column(DateTime(timezone=True), nullable=True)
    
    # Foreign keys
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="documents")
    analyses = relationship("DocumentAnalysis", back_populates="document", cascade="all, delete-orphan")
    chat_messages = relationship("ChatMessage", back_populates="document")
    
    def __repr__(self):
        """String representation of document."""
        return f"<Document(id={self.id}, filename={self.filename})>"
    
    @property
    def size_mb(self) -> float:
        """Get file size in MB."""
        return round(self.file_size / (1024 * 1024), 2)
    
    @property
    def is_processed(self) -> bool:
        """Check if document processing is completed."""
        return self.status == DocumentStatus.COMPLETED.value
    
    @property
    def has_error(self) -> bool:
        """Check if document processing failed."""
        return self.status == DocumentStatus.FAILED.value
    
    def update_last_accessed(self):
        """Update last accessed timestamp."""
        self.last_accessed = datetime.utcnow()
    
    def add_tag(self, tag: str):
        """Add a tag to the document."""
        if self.tags is None:
            self.tags = []
        if tag not in self.tags:
            self.tags.append(tag)
    
    def remove_tag(self, tag: str):
        """Remove a tag from the document."""
        if self.tags and tag in self.tags:
            self.tags.remove(tag)
    
    def set_metadata(self, key: str, value):
        """Set metadata value."""
        if self.document_metadata is None:
            self.document_metadata = {}
        self.document_metadata[key] = value
    
    def get_metadata(self, key: str, default=None):
        """Get metadata value."""
        if self.document_metadata:
            return self.document_metadata.get(key, default)
        return default
    
    def to_dict(self) -> dict:
        """Convert document to dictionary."""
        return {
            "id": str(self.id),
            "filename": self.filename,
            "original_filename": self.original_filename,
            "file_size": self.file_size,
            "size_mb": self.size_mb,
            "file_type": self.file_type,
            "mime_type": self.mime_type,
            "document_type": self.document_type,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "is_processed": self.is_processed,
            "has_error": self.has_error,
            "processing_error": self.processing_error,
            "text_preview": self.text_preview,
            "page_count": self.page_count,
            "word_count": self.word_count,
            "tags": self.tags or [],
            "is_public": self.is_public,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_accessed": self.last_accessed.isoformat() if self.last_accessed else None,
            "user_id": str(self.user_id)
        }
