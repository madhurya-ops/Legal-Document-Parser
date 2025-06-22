from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext
from typing import Optional, List
import hashlib

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
def calculate_file_hash(file_content: bytes) -> str:
    """Calculate SHA-256 hash of file content"""
    return hashlib.sha256(file_content).hexdigest()

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