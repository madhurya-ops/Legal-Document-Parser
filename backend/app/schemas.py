from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime
import uuid

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: uuid.UUID
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class DocumentBase(BaseModel):
    original_filename: str
    file_size: str
    file_type: str

class DocumentCreate(DocumentBase):
    filename: str
    file_hash: str
    user_id: uuid.UUID

class DocumentResponse(DocumentBase):
    id: uuid.UUID
    filename: str
    file_hash: str
    user_id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

class DocumentUploadResponse(BaseModel):
    message: str
    document: Optional[DocumentResponse] = None
    is_duplicate: bool = False