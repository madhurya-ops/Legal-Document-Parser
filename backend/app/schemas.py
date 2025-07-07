from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
import uuid

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class MessageType(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"

class AnalysisType(str, Enum):
    CLAUSE_EXTRACTION = "clause_extraction"
    DOCUMENT_SUMMARY = "document_summary"
    COMPLIANCE_CHECK = "compliance_check"
    PRECEDENT_SEARCH = "precedent_search"
    RISK_ASSESSMENT = "risk_assessment"

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
    role: UserRole
    last_login: Optional[datetime] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    role: Optional[UserRole] = None

class Token(BaseModel):
    access_token: str
    token_type: str

# Document schemas
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

# Chat schemas
class ChatSessionCreate(BaseModel):
    session_name: Optional[str] = None

class ChatSessionResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    session_name: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

class ChatMessageCreate(BaseModel):
    session_id: uuid.UUID
    message_type: MessageType
    content: str
    sources: Optional[Dict[str, Any]] = None
    confidence_score: Optional[float] = None

class ChatMessageResponse(BaseModel):
    id: uuid.UUID
    session_id: uuid.UUID
    message_type: MessageType
    content: str
    sources: Optional[Dict[str, Any]] = None
    confidence_score: Optional[float] = None
    timestamp: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Document Analysis schemas
class DocumentAnalysisCreate(BaseModel):
    document_id: uuid.UUID
    analysis_type: AnalysisType
    results: Dict[str, Any]
    confidence_score: Optional[float] = None

class DocumentAnalysisResponse(BaseModel):
    id: uuid.UUID
    document_id: uuid.UUID
    analysis_type: AnalysisType
    results: Dict[str, Any]
    confidence_score: Optional[float] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Vector Collection schemas
class VectorCollectionCreate(BaseModel):
    collection_name: str
    description: Optional[str] = None

class VectorCollectionResponse(BaseModel):
    id: uuid.UUID
    collection_name: str
    description: Optional[str] = None
    document_count: int
    created_by: uuid.UUID
    created_at: datetime
    last_updated: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

# Legal Analysis schemas
class ClauseExtractionRequest(BaseModel):
    document_content: str
    document_id: Optional[uuid.UUID] = None

class ClauseExtractionResponse(BaseModel):
    clauses: List[Dict[str, Any]]
    confidence_scores: Dict[str, float]
    risk_assessment: Dict[str, Any]  # Changed from Dict[str, str] to Dict[str, Any]
    recommendations: List[str]

class ComplianceCheckRequest(BaseModel):
    document_content: str
    jurisdiction: str = "india"
    document_id: Optional[uuid.UUID] = None

class ComplianceCheckResponse(BaseModel):
    compliance_status: str
    missing_clauses: List[str]
    regulatory_requirements: List[Dict[str, Any]]
    recommendations: List[str]
    confidence_score: float

class PrecedentSearchRequest(BaseModel):
    query: str
    jurisdiction: str = "india"
    document_type: Optional[str] = None

class PrecedentSearchResponse(BaseModel):
    precedents: List[Dict[str, Any]]
    relevance_scores: List[float]
    citations: List[str]

# System Metrics schemas
class SystemMetricCreate(BaseModel):
    metric_name: str
    metric_value: Dict[str, Any]

class SystemMetricResponse(BaseModel):
    id: uuid.UUID
    metric_name: str
    metric_value: Dict[str, Any]
    recorded_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Admin Dashboard schemas
class UserStatsResponse(BaseModel):
    total_users: int
    active_users: int
    new_users_this_month: int
    user_growth_rate: float

class DocumentStatsResponse(BaseModel):
    total_documents: int
    documents_this_month: int
    total_storage_used: str
    popular_document_types: Dict[str, int]

class SystemStatsResponse(BaseModel):
    api_calls_today: int
    average_response_time: float
    system_uptime: str
    active_sessions: int

class AdminDashboardResponse(BaseModel):
    user_stats: UserStatsResponse
    document_stats: DocumentStatsResponse
    system_stats: SystemStatsResponse
    recent_activities: List[Dict[str, Any]]
# update Sun Jul  6 02:54:59 IST 2025
# update Sun Jul  6 02:56:34 IST 2025
