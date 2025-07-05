from sqlalchemy.orm import Session
from sqlalchemy import func, desc, Integer
from . import models, schemas
from passlib.context import CryptContext
from typing import Optional, List
from datetime import datetime, timedelta
import uuid

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """Get user by email"""
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    """Get user by username"""
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """Create a new user"""
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str) -> Optional[models.User]:
    """Authenticate user with email and password"""
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

# Document CRUD operations
def check_duplicate_document(db: Session, file_hash: str, user_id: str) -> Optional[models.Document]:
    """Check if a document with the same hash already exists for the user"""
    return db.query(models.Document).filter(
        models.Document.file_hash == file_hash,
        models.Document.user_id == user_id
    ).first()

def get_user_documents(db: Session, user_id: str) -> List[models.Document]:
    """Get all documents for a specific user"""
    return db.query(models.Document).filter(models.Document.user_id == user_id).all()

def create_document(db: Session, document: schemas.DocumentCreate) -> models.Document:
    """Create a new document"""
    db_document = models.Document(
        filename=document.filename,
        original_filename=document.original_filename,
        file_hash=document.file_hash,
        file_size=document.file_size,
        file_type=document.file_type,
        user_id=document.user_id
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

def delete_document(db: Session, document_id: str, user_id: str) -> bool:
    """Delete a document (only if owned by user)"""
    document = db.query(models.Document).filter(
        models.Document.id == document_id,
        models.Document.user_id == user_id
    ).first()
    
    if document:
        db.delete(document)
        db.commit()
        return True
    return False

# Enhanced User operations
def update_user_last_login(db: Session, user_id: str) -> None:
    """Update user's last login timestamp"""
    db.query(models.User).filter(models.User.id == user_id).update(
        {models.User.last_login: datetime.utcnow()}
    )
    db.commit()

def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    """Get all users (admin only)"""
    return db.query(models.User).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: str, user_update: schemas.UserUpdate) -> Optional[models.User]:
    """Update user information"""
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return None
    
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

# Chat Session CRUD operations
def create_chat_session(db: Session, user_id: str, session_name: Optional[str] = None) -> models.ChatSession:
    """Create a new chat session"""
    db_session = models.ChatSession(
        user_id=user_id,
        session_name=session_name or f"Chat {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}"
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def get_user_chat_sessions(db: Session, user_id: str) -> List[models.ChatSession]:
    """Get all chat sessions for a user"""
    return db.query(models.ChatSession).filter(
        models.ChatSession.user_id == user_id
    ).order_by(desc(models.ChatSession.updated_at)).all()

def get_chat_session(db: Session, session_id: str, user_id: str) -> Optional[models.ChatSession]:
    """Get a specific chat session"""
    return db.query(models.ChatSession).filter(
        models.ChatSession.id == session_id,
        models.ChatSession.user_id == user_id
    ).first()

def delete_chat_session(db: Session, session_id: str, user_id: str) -> bool:
    """Delete a chat session"""
    session = db.query(models.ChatSession).filter(
        models.ChatSession.id == session_id,
        models.ChatSession.user_id == user_id
    ).first()
    
    if session:
        db.delete(session)
        db.commit()
        return True
    return False

# Chat Message CRUD operations
def create_chat_message(db: Session, message: schemas.ChatMessageCreate) -> models.ChatMessage:
    """Create a new chat message"""
    db_message = models.ChatMessage(
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
    db.query(models.ChatSession).filter(
        models.ChatSession.id == message.session_id
    ).update({models.ChatSession.updated_at: datetime.utcnow()})
    db.commit()
    
    return db_message

def get_chat_messages(db: Session, session_id: str, user_id: str) -> List[models.ChatMessage]:
    """Get all messages for a chat session"""
    # Verify user owns the session
    session = get_chat_session(db, session_id, user_id)
    if not session:
        return []
    
    return db.query(models.ChatMessage).filter(
        models.ChatMessage.session_id == session_id
    ).order_by(models.ChatMessage.timestamp).all()

# Document Analysis CRUD operations
def create_document_analysis(db: Session, analysis: schemas.DocumentAnalysisCreate) -> models.DocumentAnalysis:
    """Create a new document analysis"""
    db_analysis = models.DocumentAnalysis(
        document_id=analysis.document_id,
        analysis_type=analysis.analysis_type,
        results=analysis.results,
        confidence_score=analysis.confidence_score
    )
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    return db_analysis

def get_document_analyses(db: Session, document_id: str, user_id: str) -> List[models.DocumentAnalysis]:
    """Get all analyses for a document"""
    # Verify user owns the document
    document = db.query(models.Document).filter(
        models.Document.id == document_id,
        models.Document.user_id == user_id
    ).first()
    
    if not document:
        return []
    
    return db.query(models.DocumentAnalysis).filter(
        models.DocumentAnalysis.document_id == document_id
    ).order_by(desc(models.DocumentAnalysis.created_at)).all()

def get_analysis_by_type(db: Session, document_id: str, analysis_type: str, user_id: str) -> Optional[models.DocumentAnalysis]:
    """Get the latest analysis of a specific type for a document"""
    # Verify user owns the document
    document = db.query(models.Document).filter(
        models.Document.id == document_id,
        models.Document.user_id == user_id
    ).first()
    
    if not document:
        return None
    
    return db.query(models.DocumentAnalysis).filter(
        models.DocumentAnalysis.document_id == document_id,
        models.DocumentAnalysis.analysis_type == analysis_type
    ).order_by(desc(models.DocumentAnalysis.created_at)).first()

# Vector Collection CRUD operations
def create_vector_collection(db: Session, collection: schemas.VectorCollectionCreate, user_id: str) -> models.VectorCollection:
    """Create a new vector collection"""
    db_collection = models.VectorCollection(
        collection_name=collection.collection_name,
        description=collection.description,
        created_by=user_id
    )
    db.add(db_collection)
    db.commit()
    db.refresh(db_collection)
    return db_collection

def get_vector_collections(db: Session) -> List[models.VectorCollection]:
    """Get all vector collections"""
    return db.query(models.VectorCollection).order_by(desc(models.VectorCollection.created_at)).all()

def update_vector_collection_count(db: Session, collection_id: str, count: int) -> None:
    """Update document count for a vector collection"""
    db.query(models.VectorCollection).filter(
        models.VectorCollection.id == collection_id
    ).update({
        models.VectorCollection.document_count: count,
        models.VectorCollection.last_updated: datetime.utcnow()
    })
    db.commit()

# System Metrics CRUD operations
def create_system_metric(db: Session, metric: schemas.SystemMetricCreate) -> models.SystemMetric:
    """Create a new system metric"""
    db_metric = models.SystemMetric(
        metric_name=metric.metric_name,
        metric_value=metric.metric_value
    )
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    return db_metric

def get_recent_metrics(db: Session, metric_name: str, days: int = 7) -> List[models.SystemMetric]:
    """Get recent metrics for a specific metric name"""
    start_date = datetime.utcnow() - timedelta(days=days)
    return db.query(models.SystemMetric).filter(
        models.SystemMetric.metric_name == metric_name,
        models.SystemMetric.recorded_at >= start_date
    ).order_by(desc(models.SystemMetric.recorded_at)).all()

# Admin Dashboard CRUD operations
def get_user_stats(db: Session) -> dict:
    """Get user statistics for admin dashboard"""
    total_users = db.query(models.User).count()
    active_users = db.query(models.User).filter(models.User.is_active == True).count()
    
    # Users created in the last 30 days
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    new_users_this_month = db.query(models.User).filter(
        models.User.created_at >= thirty_days_ago
    ).count()
    
    # Users created in the previous 30 days for growth rate calculation
    sixty_days_ago = datetime.utcnow() - timedelta(days=60)
    new_users_prev_month = db.query(models.User).filter(
        models.User.created_at >= sixty_days_ago,
        models.User.created_at < thirty_days_ago
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

def get_document_stats(db: Session) -> dict:
    """Get document statistics for admin dashboard"""
    total_documents = db.query(models.Document).count()
    
    # Documents uploaded in the last 30 days
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    documents_this_month = db.query(models.Document).filter(
        models.Document.created_at >= thirty_days_ago
    ).count()
    
    # Calculate total storage (simplified - sum of file sizes)
    total_size = db.query(func.sum(func.cast(models.Document.file_size, Integer))).scalar() or 0
    total_storage_mb = total_size / (1024 * 1024)
    total_storage_used = f"{total_storage_mb:.2f} MB"
    
    # Popular document types
    type_counts = db.query(
        models.Document.file_type,
        func.count(models.Document.file_type)
    ).group_by(models.Document.file_type).all()
    
    popular_document_types = {file_type: count for file_type, count in type_counts}
    
    return {
        "total_documents": total_documents,
        "documents_this_month": documents_this_month,
        "total_storage_used": total_storage_used,
        "popular_document_types": popular_document_types
    }

def get_recent_activities(db: Session, limit: int = 10) -> List[dict]:
    """Get recent activities for admin dashboard"""
    activities = []
    
    # Recent user registrations
    recent_users = db.query(models.User).order_by(
        desc(models.User.created_at)
    ).limit(limit//2).all()
    
    for user in recent_users:
        activities.append({
            "type": "user_registration",
            "description": f"New user registered: {user.username}",
            "timestamp": user.created_at,
            "user_id": str(user.id)
        })
    
    # Recent document uploads
    recent_docs = db.query(models.Document).order_by(
        desc(models.Document.created_at)
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
# update Sun Jul  6 02:54:59 IST 2025
