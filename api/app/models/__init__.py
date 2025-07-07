"""
Models Package
==============

Database models for the LegalDoc application.
"""

from .user import User, UserRole
from .document import Document, DocumentStatus, DocumentType
from .chat import ChatSession, ChatMessage, MessageType
from .analysis import DocumentAnalysis, AnalysisType, AnalysisStatus

# Export all models for easy import
__all__ = [
    # User models
    "User",
    "UserRole",
    
    # Document models
    "Document",
    "DocumentStatus", 
    "DocumentType",
    
    # Chat models
    "ChatSession",
    "ChatMessage",
    "MessageType",
    
    # Analysis models
    "DocumentAnalysis",
    "AnalysisType",
    "AnalysisStatus",
]
