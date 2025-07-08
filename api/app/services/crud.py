from sqlalchemy.orm import Session
from sqlalchemy import func, desc, Integer
from typing import Optional, List
from datetime import datetime, timedelta
import uuid

from ..models import User, Document, ChatSession, ChatMessage, DocumentAnalysis
from ..schemas import UserCreate, UserUpdate, DocumentCreate, ChatMessageCreate, DocumentAnalysisCreate
from ..core.security import get_password_hash, verify_password

# User CRUD operations
async def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()

def get_user_by_auth0_sub(db: Session, auth0_sub: str) -> Optional[User]:
    """Get user by Auth0 subject ID"""
    return db.query(User).filter(User.auth0_sub == auth0_sub).first()

def create_user_from_auth0(db: Session, auth0_sub: str, email: str, name: Optional[str] = None) -> User:
    """Create a new user from Auth0 authentication"""
    from ..models.user import UserRole
    
    # Extract username from email or name
    username = name or email.split('@')[0]
    
    # Ensure username is unique
    base_username = username
    counter = 1
    while db.query(User).filter(User.username == username).first():
        username = f"{base_username}{counter}"
        counter += 1
    
    db_user = User(
        username=username,
        email=email,
        auth0_sub=auth0_sub,
        hashed_password=None,  # No password for Auth0 users
        role=UserRole.USER
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

async def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Get user by username"""
    return db.query(User).filter(User.username == username).first()

async def create_user(db: Session, user: UserCreate) -> User:
    """Create a new user"""
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

async def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Authenticate user with email and password"""
    user = await get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

async def update_user_last_login(db: Session, user_id: str) -> None:
    """Update user's last login timestamp"""
    db.query(User).filter(User.id == user_id).update(
        {User.last_login: datetime.utcnow()}
    )
    db.commit()

async def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """Get all users (admin only)"""
    return db.query(User).offset(skip).limit(limit).all()

async def update_user(db: Session, user_id: str, user_update: UserUpdate) -> Optional[User]:
    """Update user information"""
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None
    
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

# Document CRUD operations
async def check_duplicate_document(db: Session, file_hash: str, user_id: str) -> Optional[Document]:
    """Check if a document with the same hash already exists for the user"""
    return db.query(Document).filter(
        Document.file_hash == file_hash,
        Document.user_id == user_id
    ).first()

async def get_user_documents(db: Session, user_id: str) -> List[Document]:
    """Get all documents for a specific user"""
    return db.query(Document).filter(Document.user_id == user_id).all()

async def create_document(db: Session, document: DocumentCreate) -> Document:
    """Create a new document"""
    db_document = Document(
        filename=document.filename,
        original_filename=document.original_filename,
        file_path=document.file_path,
        file_hash=document.file_hash,
        file_size=document.file_size,
        file_type=document.file_type,
        user_id=document.user_id
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

async def delete_document(db: Session, document_id: str, user_id: str) -> bool:
    """Delete a document (only if owned by user)"""
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == user_id
    ).first()
    
    if document:
        db.delete(document)
        db.commit()
        return True
    return False

# Chat Session CRUD operations
async def create_chat_session(db: Session, user_id: str, session_name: Optional[str] = None) -> ChatSession:
    """Create a new chat session"""
    db_session = ChatSession(
        user_id=user_id,
        session_name=session_name or f"Chat {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}"
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

async def get_user_chat_sessions(db: Session, user_id: str) -> List[ChatSession]:
    """Get all chat sessions for a user"""
    return db.query(ChatSession).filter(
        ChatSession.user_id == user_id
    ).order_by(desc(ChatSession.updated_at)).all()

async def get_chat_session(db: Session, session_id: str, user_id: str) -> Optional[ChatSession]:
    """Get a specific chat session"""
    return db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == user_id
    ).first()

async def delete_chat_session(db: Session, session_id: str, user_id: str) -> bool:
    """Delete a chat session"""
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == user_id
    ).first()
    
    if session:
        db.delete(session)
        db.commit()
        return True
    return False

# Chat Message CRUD operations
async def create_chat_message(db: Session, message: ChatMessageCreate) -> ChatMessage:
    """Create a new chat message"""
    db_message = ChatMessage(
        session_id=message.session_id,
        message_type=message.message_type,
        content=message.content,
        sources=message.sources,
        confidence_score=message.confidence_score
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    
    # Update session's updated_at timestamp
    db.query(ChatSession).filter(
        ChatSession.id == message.session_id
    ).update({ChatSession.updated_at: datetime.utcnow()})
    db.commit()
    
    return db_message

async def get_chat_messages(db: Session, session_id: str, user_id: str) -> List[ChatMessage]:
    """Get all messages for a chat session"""
    # Verify user owns the session
    session = await get_chat_session(db, session_id, user_id)
    if not session:
        return []
    
    return db.query(ChatMessage).filter(
        ChatMessage.session_id == session_id
    ).order_by(ChatMessage.timestamp).all()

# Document Analysis CRUD operations
async def create_document_analysis(db: Session, analysis: DocumentAnalysisCreate) -> DocumentAnalysis:
    """Create a new document analysis"""
    db_analysis = DocumentAnalysis(
        document_id=analysis.document_id,
        analysis_type=analysis.analysis_type,
        results=analysis.results,
        confidence_score=analysis.confidence_score
    )
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    return db_analysis

async def get_document_analyses(db: Session, document_id: str, user_id: str) -> List[DocumentAnalysis]:
    """Get all analyses for a document"""
    # Verify user owns the document
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == user_id
    ).first()
    
    if not document:
        return []
    
    return db.query(DocumentAnalysis).filter(
        DocumentAnalysis.document_id == document_id
    ).order_by(desc(DocumentAnalysis.created_at)).all()

async def get_analysis_by_type(db: Session, document_id: str, analysis_type: str, user_id: str) -> Optional[DocumentAnalysis]:
    """Get the latest analysis of a specific type for a document"""
    # Verify user owns the document
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == user_id
    ).first()
    
    if not document:
        return None
    
    return db.query(DocumentAnalysis).filter(
        DocumentAnalysis.document_id == document_id,
        DocumentAnalysis.analysis_type == analysis_type
    ).order_by(desc(DocumentAnalysis.created_at)).first()

# Admin Dashboard CRUD operations
async def get_user_stats(db: Session) -> dict:
    """Get user statistics for admin dashboard"""
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    
    # Users created in the last 30 days
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    new_users_this_month = db.query(User).filter(
        User.created_at >= thirty_days_ago
    ).count()
    
    # Users created in the previous 30 days for growth rate calculation
    sixty_days_ago = datetime.utcnow() - timedelta(days=60)
    new_users_prev_month = db.query(User).filter(
        User.created_at >= sixty_days_ago,
        User.created_at < thirty_days_ago
    ).count()
    
    growth_rate = 0.0
    if new_users_prev_month > 0:
        growth_rate = ((new_users_this_month - new_users_prev_month) / new_users_prev_month) * 100
    
    return {
        "total_users": total_users,
        "active_users": active_users,
        "new_users_this_month": new_users_this_month,
        "user_growth_rate": round(growth_rate, 2)
    }

async def get_document_stats(db: Session) -> dict:
    """Get document statistics for admin dashboard"""
    total_documents = db.query(Document).count()
    
    # Documents uploaded in the last 30 days
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    documents_this_month = db.query(Document).filter(
        Document.created_at >= thirty_days_ago
    ).count()
    
    # Calculate total storage (simplified - sum of file sizes)
    total_size = db.query(func.sum(func.cast(Document.file_size, Integer))).scalar() or 0
    total_storage_mb = total_size / (1024 * 1024)
    total_storage_used = f"{total_storage_mb:.2f} MB"
    
    # Popular document types
    type_counts = db.query(
        Document.file_type,
        func.count(Document.file_type)
    ).group_by(Document.file_type).all()
    
    popular_document_types = {file_type: count for file_type, count in type_counts}
    
    return {
        "total_documents": total_documents,
        "documents_this_month": documents_this_month,
        "total_storage_used": total_storage_used,
        "popular_document_types": popular_document_types
    }

async def get_recent_activities(db: Session, limit: int = 10) -> List[dict]:
    """Get recent activities for admin dashboard"""
    activities = []
    
    # Recent user registrations
    recent_users = db.query(User).order_by(
        desc(User.created_at)
    ).limit(limit//2).all()
    
    for user in recent_users:
        activities.append({
            "type": "user_registration",
            "description": f"New user registered: {user.username}",
            "timestamp": user.created_at,
            "user_id": str(user.id)
        })
    
    # Recent document uploads
    recent_docs = db.query(Document).order_by(
        desc(Document.created_at)
    ).limit(limit//2).all()
    
    for doc in recent_docs:
        activities.append({
            "type": "document_upload",
            "description": f"Document uploaded: {doc.original_filename}",
            "timestamp": doc.created_at,
            "user_id": str(doc.user_id),
            "document_id": str(doc.id)
        })
    
    # Sort by timestamp and return limited results
    activities.sort(key=lambda x: x["timestamp"], reverse=True)
    return activities[:limit]
