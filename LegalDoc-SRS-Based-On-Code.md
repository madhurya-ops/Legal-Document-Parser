# LegalDoc: Software Requirements Specification (SRS)
### Based on Current Implementation Analysis

## 1. Introduction

### 1.1 Purpose
This Software Requirements Specification (SRS) document provides a comprehensive blueprint for the LegalDoc application based on the current implementation analysis. LegalDoc is an AI-powered legal document analysis platform designed to transform legal practice by providing instant insights, summaries, and actionable recommendations while maintaining enterprise-grade security and cost-effectiveness.

### 1.2 Scope
LegalDoc serves legal professionals including lawyers, paralegals, law students, and legal teams across India. The platform leverages Gemini AI with RAG (Retrieval-Augmented Generation) to analyze contracts, agreements, and legal documents with precision, offering features like clause extraction, document summarization, and legal precedent recommendations.

### 1.3 Current System Overview
Based on code analysis, the system consists of:
- **Frontend**: React.js application with Tailwind CSS
- **Backend**: FastAPI with PostgreSQL database
- **AI/ML**: Gemini API integration with FAISS vector database
- **Authentication**: JWT-based with OAuth 2.0 support
- **Deployment**: Frontend on Vercel, Backend on Render

## 2. System Architecture Analysis

### 2.1 Current Frontend Architecture

#### 2.1.1 Technology Stack
- **Framework**: React.js 19.1.0 with functional components
- **Styling**: Tailwind CSS 3.4.17 with custom design system
- **Icons**: Lucide React for consistent iconography
- **State Management**: React hooks (useState, useEffect)
- **Routing**: Single-page application with conditional rendering
- **Build Tool**: Create React App (react-scripts 5.0.1)

#### 2.1.2 Component Architecture
```
src/
├── components/
│   ├── ui/                    # Reusable UI components
│   │   ├── button.js         # Button component
│   │   ├── card.js           # Card layouts
│   │   ├── badge.js          # Status badges
│   │   └── textarea.js       # Text input areas
│   ├── AuthPage.js           # Authentication interface
│   ├── HomePage.js           # Landing page with features
│   ├── AboutPage.js          # About section
│   ├── ChatInterface.js      # Main chat functionality
│   ├── FileUpload.js         # Document upload interface
│   └── ThemeToggle.js        # Dark/light mode toggle
├── App.js                    # Main application component
├── api.js                    # API integration layer
└── ThemeProvider.js          # Theme management
```

#### 2.1.3 Current UI/UX Features
- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **Dark/Light Mode**: Toggle theme support with CSS variables
- **Animation System**: Fade-in animations and hover effects
- **Accessibility**: ARIA labels and keyboard navigation
- **Progressive Loading**: Lazy loading for heavy components

### 2.2 Current Backend Architecture

#### 2.2.1 Technology Stack
- **Framework**: FastAPI 0.110.2 for high-performance APIs
- **Database**: PostgreSQL with SQLAlchemy 2.0.27 ORM
- **Authentication**: JWT tokens with python-jose
- **Password Security**: Bcrypt hashing with passlib
- **AI/ML Libraries**:
  - langchain 0.2.17 for document processing
  - sentence-transformers 4.1.0 for embeddings
  - faiss-cpu 1.8.0 for vector search
  - transformers 4.41.2 for NLP
- **Document Processing**: pypdf 5.6.0 for PDF handling

#### 2.2.2 API Architecture
```
app/
├── api/
│   ├── routes.py             # Main API endpoints
│   └── auth_routes.py        # Authentication endpoints
├── core/
│   ├── vector_store.py       # FAISS vector operations
│   └── logging_config.py     # Logging configuration
├── models.py                 # SQLAlchemy database models
├── schemas.py                # Pydantic request/response models
├── crud.py                   # Database operations
├── auth.py                   # JWT authentication logic
├── database.py               # Database configuration
└── main.py                   # FastAPI application setup
```

#### 2.2.3 Current API Endpoints
1. **Authentication**:
   - `POST /auth/signup` - User registration
   - `POST /auth/login` - User authentication
   - `GET /auth/me` - Get current user profile

2. **Document Processing**:
   - `POST /upload` - Document upload with duplicate detection
   - `GET /documents` - Get user documents
   - `DELETE /documents/{id}` - Delete user document

3. **AI Analysis**:
   - `POST /ask` - Query documents with AI analysis

4. **System**:
   - `GET /` - API root endpoint
   - `GET /health` - Health check

### 2.3 Current Database Schema

#### 2.3.1 Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid4(),
    username VARCHAR UNIQUE NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);
```

#### 2.3.2 Documents Table
```sql
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT uuid4(),
    filename VARCHAR NOT NULL,
    original_filename VARCHAR NOT NULL,
    file_hash VARCHAR UNIQUE NOT NULL,
    file_size VARCHAR NOT NULL,
    file_type VARCHAR NOT NULL,
    user_id UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);
```

### 2.4 Current AI/ML Implementation

#### 2.4.1 Vector Store Configuration
- **Embedding Model**: sentence-transformers/paraphrase-MiniLM-L3-v2 (fallback: all-MiniLM-L6-v2)
- **Vector Database**: FAISS with IndexFlatIP for similarity search
- **Document Processing**: Lightweight processing with configurable limits
- **Chunk Size**: 100-1500 characters (configurable)
- **Search Results**: k=5 most relevant documents

#### 2.4.2 LLM Integration (Gemini)
- **API**: Google Generative AI (Gemini 1.5 Flash)
- **Max Output Tokens**: 500
- **Temperature**: 0.7
- **Context Limit**: 2500 characters
- **Prompt Limit**: 800 characters
- **Timeout**: 30 seconds

#### 2.4.3 Current System Prompts
```
You are a helpful, friendly, and professional legal assistant.
You may respond to greetings, small talk, and polite conversation in a natural, human-like way but only very short answers only. Greeting and small talks must not be more than 1 line.
Do not give any information unless asked by the user explicitly, answer or talk only as much as required.
For legal or document-related questions, answer only if the information is present in the provided context/database.
If you do not know the answer or it is not present in the context, say 'I don't know' or politely indicate you cannot answer.
Do not make up information or hallucinate. Stay within the scope of the provided legal documents and data.
If a user asks something completely out of scope (not a greeting, small talk, or legal/document question), politely decline to answer.
```

## 3. Enhanced Requirements Based on Current Implementation

### 3.1 Frontend Enhancements Required

#### 3.1.1 Admin Dashboard Implementation
**Current State**: Not implemented
**Required Features**:
- Admin role detection and routing
- Usage metrics visualization (charts/graphs)
- User management interface
- Vector database management tools
- System performance monitoring
- Document processing analytics

#### 3.1.2 Chat Interface Enhancements
**Current State**: Basic chat with file context
**Required Features**:
- Chat history persistence (currently in localStorage)
- Message export functionality (PDF, DOCX, TXT)
- Advanced message formatting for legal responses
- Source citation display with confidence scores
- Document section referencing
- Multi-document context support

#### 3.1.3 Document Management Improvements
**Current State**: Basic upload/display/delete
**Required Features**:
- Document analysis results caching
- Batch document operations
- Document categorization and tagging
- Advanced search and filtering
- Document comparison tools
- Template document library

#### 3.1.4 Enhanced User Experience
**Current State**: Basic responsive design
**Required Features**:
- Advanced loading states and progress indicators
- Offline capability for previously analyzed documents
- Keyboard shortcuts for power users
- Customizable dashboard layouts
- Real-time collaboration features
- Document annotation tools

### 3.2 Backend Enhancements Required

#### 3.2.1 Advanced AI Features
**Current State**: Basic query with RAG
**Required Features**:

1. **Clause Extraction Engine**:
   ```python
   class ClauseExtractor:
       def extract_clauses(self, document_text: str) -> List[ExtractedClause]:
           # Extract: Termination, Indemnity, Jurisdiction, Force Majeure
           # Risk assessment based on precedent databases
           # Confidence scoring for each identified clause
           # Highlighting of potentially problematic language
   ```

2. **Document Summarization Service**:
   ```python
   class DocumentSummarizer:
       def generate_summary(self, document: str, summary_type: str) -> Summary:
           # Types: layman, legal, academic, executive
           # Include key dates, parties, obligations
           # Risk assessment and compliance notes
   ```

3. **Legal Precedent Recommendation**:
   ```python
   class PrecedentEngine:
       def find_relevant_precedents(self, document_context: str) -> List[Precedent]:
           # Search Indian case law databases
           # Relevance scoring and precedent strength indicators
           # Integration with public legal databases
   ```

4. **Compliance Checker**:
   ```python
   class ComplianceChecker:
       def check_compliance(self, document: str, jurisdiction: str) -> ComplianceReport:
           # FDI, SEBI, employment law compliance
           # Missing clause identification
           # Regulatory requirement mapping
   ```

#### 3.2.2 Enhanced Database Schema

```sql
-- Add admin role support
ALTER TABLE users ADD COLUMN role VARCHAR DEFAULT 'user';
ALTER TABLE users ADD COLUMN last_login TIMESTAMP;

-- Chat history storage
CREATE TABLE chat_sessions (
    id UUID PRIMARY KEY DEFAULT uuid4(),
    user_id UUID REFERENCES users(id),
    session_name VARCHAR,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE chat_messages (
    id UUID PRIMARY KEY DEFAULT uuid4(),
    session_id UUID REFERENCES chat_sessions(id),
    message_type VARCHAR CHECK (message_type IN ('user', 'assistant')),
    content TEXT NOT NULL,
    sources JSONB,
    confidence_score FLOAT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Document analysis results
CREATE TABLE document_analyses (
    id UUID PRIMARY KEY DEFAULT uuid4(),
    document_id UUID REFERENCES documents(id),
    analysis_type VARCHAR NOT NULL,
    results JSONB NOT NULL,
    confidence_score FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Vector database metadata
CREATE TABLE vector_collections (
    id UUID PRIMARY KEY DEFAULT uuid4(),
    collection_name VARCHAR UNIQUE NOT NULL,
    description TEXT,
    document_count INTEGER DEFAULT 0,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_updated TIMESTAMP WITH TIME ZONE
);

-- System metrics for admin dashboard
CREATE TABLE system_metrics (
    id UUID PRIMARY KEY DEFAULT uuid4(),
    metric_name VARCHAR NOT NULL,
    metric_value JSONB NOT NULL,
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### 3.2.3 Enhanced API Endpoints

```python
# Admin endpoints
@router.get("/admin/users", dependencies=[Depends(require_admin)])
async def get_all_users(db: Session = Depends(get_db)):
    # Return user statistics and management interface

@router.get("/admin/metrics", dependencies=[Depends(require_admin)])
async def get_system_metrics(db: Session = Depends(get_db)):
    # Return system performance and usage metrics

@router.post("/admin/vector-upload", dependencies=[Depends(require_admin)])
async def upload_to_vector_store(files: List[UploadFile]):
    # Upload public legal datasets to vector store

# Enhanced document endpoints
@router.post("/documents/{document_id}/analyze")
async def analyze_document(document_id: str, analysis_type: str):
    # Perform specific analysis on document

@router.get("/documents/{document_id}/download")
async def download_analysis(document_id: str, format: str):
    # Download analysis results in specified format

# Chat enhancements
@router.post("/chat/sessions")
async def create_chat_session(session_data: ChatSessionCreate):
    # Create new chat session

@router.get("/chat/sessions/{session_id}/export")
async def export_chat_session(session_id: str, format: str):
    # Export chat history in various formats

# Legal-specific endpoints
@router.post("/legal/extract-clauses")
async def extract_legal_clauses(document_content: str):
    # Extract and analyze legal clauses

@router.post("/legal/compliance-check")
async def check_compliance(document_content: str, jurisdiction: str):
    # Check regulatory compliance

@router.post("/legal/precedent-search")
async def search_precedents(query: str, jurisdiction: str):
    # Search for relevant legal precedents
```

### 3.3 Enhanced System Prompts for Legal Analysis

#### 3.3.1 Specialized Legal Analysis Prompt
```python
LEGAL_ANALYSIS_PROMPT = """
You are an expert legal analyst specializing in Indian law with deep knowledge of:
- Contract law and commercial agreements
- Corporate compliance (Companies Act 2013, SEBI regulations, FDI policies)
- Employment law and labor regulations
- Intellectual property law
- Real estate and property law
- Dispute resolution and arbitration

ANALYSIS FRAMEWORK:
1. Document Type Identification
2. Key Parties and Relationships
3. Critical Clauses Analysis (Termination, Indemnity, Jurisdiction, Force Majeure, etc.)
4. Risk Assessment (High/Medium/Low with specific concerns)
5. Compliance Verification (relevant Indian laws and regulations)
6. Missing or Weak Provisions
7. Recommendations for Improvement
8. Next Steps and Action Items

RESPONSE FORMAT:
- Provide analysis in the requested format: {analysis_type}
- Include confidence scores for each identified element
- Cite relevant sections from Indian legal statutes
- Flag potential legal risks with severity levels
- Suggest specific improvements with legal reasoning

CONSTRAINTS:
- Base analysis strictly on the provided document content
- Reference only established Indian legal precedents
- Indicate uncertainty when information is incomplete
- Provide actionable recommendations within Indian legal context
"""

CLAUSE_EXTRACTION_PROMPT = """
Extract and analyze the following legal clauses from the provided document:

1. TERMINATION CLAUSES
   - Grounds for termination
   - Notice periods
   - Consequences of termination

2. INDEMNITY AND LIABILITY
   - Indemnification scope
   - Limitation of liability
   - Insurance requirements

3. JURISDICTION AND DISPUTE RESOLUTION
   - Governing law
   - Dispute resolution mechanism
   - Court jurisdiction

4. FORCE MAJEURE
   - Definition of force majeure events
   - Notice requirements
   - Performance suspension terms

5. PAYMENT AND FINANCIAL TERMS
   - Payment schedules
   - Interest on delayed payments
   - Currency and exchange rate provisions

6. INTELLECTUAL PROPERTY
   - IP ownership and licensing
   - Confidentiality obligations
   - Non-disclosure terms

For each clause:
- Provide exact text from document
- Assess completeness and enforceability
- Identify potential risks or ambiguities
- Suggest improvements if needed
- Rate risk level (High/Medium/Low)
"""

COMPLIANCE_CHECK_PROMPT = """
Perform comprehensive compliance analysis for Indian legal requirements:

CORPORATE COMPLIANCE:
- Companies Act 2013 compliance
- Board resolution requirements
- Regulatory approvals needed

EMPLOYMENT LAW:
- Labor law compliance
- Employee benefits and rights
- Termination procedures

REGULATORY COMPLIANCE:
- SEBI regulations (if applicable)
- FDI compliance
- Industry-specific regulations

TAX IMPLICATIONS:
- GST considerations
- Income tax provisions
- Transfer pricing (if applicable)

DATA PROTECTION:
- IT Act 2000 compliance
- Data localization requirements
- Privacy protection measures

Provide:
- Compliance status (Compliant/Non-compliant/Requires Review)
- Specific legal references
- Required actions for compliance
- Risk assessment for non-compliance
"""
```

### 3.4 Document Processing Enhancements

#### 3.4.1 Advanced Document Processing Pipeline
```python
class EnhancedDocumentProcessor:
    def __init__(self):
        self.supported_formats = ['.pdf', '.docx', '.txt', '.doc']
        self.max_file_size = 50 * 1024 * 1024  # 50MB
        self.ocr_enabled = True
    
    async def process_document(self, file: UploadFile, user_id: str) -> ProcessingResult:
        # 1. File validation and security scan
        await self.validate_file(file)
        
        # 2. Text extraction with OCR support
        text_content = await self.extract_text(file)
        
        # 3. Document classification
        doc_type = await self.classify_document(text_content)
        
        # 4. Structured data extraction
        structured_data = await self.extract_structured_data(text_content, doc_type)
        
        # 5. Vector embedding creation
        embeddings = await self.create_embeddings(text_content)
        
        # 6. Store in database and vector store
        result = await self.store_document(file, text_content, structured_data, embeddings, user_id)
        
        return result
    
    async def extract_structured_data(self, text: str, doc_type: str) -> Dict:
        """Extract structured information based on document type"""
        extractors = {
            'contract': self.extract_contract_data,
            'agreement': self.extract_agreement_data,
            'legal_notice': self.extract_notice_data,
            'court_document': self.extract_court_data
        }
        
        extractor = extractors.get(doc_type, self.extract_general_data)
        return await extractor(text)
```

#### 3.4.2 Multi-language Support Implementation
```python
class MultiLanguageProcessor:
    def __init__(self):
        self.supported_languages = ['en', 'hi', 'mr', 'ta', 'te', 'bn']
        self.translators = {
            'hi': HindiTranslator(),
            'mr': MarathiTranslator(),
            # ... other language translators
        }
    
    async def detect_language(self, text: str) -> str:
        # Implement language detection
        pass
    
    async def translate_to_english(self, text: str, source_lang: str) -> str:
        # Translate document to English for analysis
        pass
    
    async def translate_response(self, response: str, target_lang: str) -> str:
        # Translate AI response back to user's language
        pass
```

## 4. Deployment and Infrastructure Enhancements

### 4.1 Current Deployment Analysis
**Frontend**: Deployed on Vercel with automatic deployments
**Backend**: Deployed on Render with PostgreSQL database
**Configuration**: Environment variables for API keys and database URLs

### 4.2 Recommended Infrastructure Improvements

#### 4.2.1 Enhanced Database Options
```yaml
# Current: PostgreSQL on Render
# Recommended: AWS RDS or Google Cloud SQL for better performance

Database Options:
  Production:
    - AWS RDS PostgreSQL with Multi-AZ deployment
    - Read replicas for analytics queries
    - Automated backups and point-in-time recovery
  
  Development:
    - Docker PostgreSQL with persistent volumes
    - Local development with seed data
    
  Staging:
    - Render PostgreSQL (current setup)
    - Copy of production data for testing
```

#### 4.2.2 Enhanced Caching Strategy
```python
# Redis integration for session management and caching
class CacheManager:
    def __init__(self):
        self.redis_client = redis.Redis.from_url(os.getenv('REDIS_URL'))
    
    async def cache_analysis_result(self, doc_hash: str, analysis: dict):
        # Cache analysis results for 24 hours
        await self.redis_client.setex(f"analysis:{doc_hash}", 86400, json.dumps(analysis))
    
    async def get_cached_analysis(self, doc_hash: str) -> Optional[dict]:
        # Retrieve cached analysis
        cached = await self.redis_client.get(f"analysis:{doc_hash}")
        return json.loads(cached) if cached else None
```

#### 4.2.3 Monitoring and Logging
```python
# Enhanced logging configuration
import structlog
from sentry_sdk import init as sentry_init

# Sentry for error tracking
sentry_init(
    dsn=os.getenv('SENTRY_DSN'),
    traces_sample_rate=0.1,
    environment=os.getenv('ENVIRONMENT', 'development')
)

# Structured logging
logger = structlog.get_logger()
```

### 4.3 Cost Optimization Analysis

#### 4.3.1 Current Infrastructure Costs (Monthly)
```
Vercel Pro: $20/month
Render Standard: $25/month  
PostgreSQL on Render: $15/month
Gemini API: $50-100/month (usage-based)
Total: $110-160/month
```

#### 4.3.2 Optimized Infrastructure Costs
```
Frontend (Vercel): $20/month
Backend (Render): $25/month
Database (AWS RDS): $30/month
Redis Cache (Redis Cloud): $10/month
Gemini API: $50-100/month
Monitoring (Sentry): $26/month
Total: $161-211/month

Benefits:
- Better performance and reliability
- Comprehensive monitoring and error tracking
- Scalable caching layer
- Professional database management
```

### 4.4 Scalability Recommendations

#### 4.4.1 Horizontal Scaling Strategy
```python
# Load balancing and auto-scaling configuration
class ScalingManager:
    def __init__(self):
        self.max_instances = 5
        self.min_instances = 1
        self.cpu_threshold = 70
        self.memory_threshold = 80
    
    async def monitor_resources(self):
        # Monitor CPU, memory, and request metrics
        # Auto-scale based on thresholds
        pass
    
    async def scale_vector_store(self):
        # Implement vector store sharding
        # Distribute embeddings across multiple indices
        pass
```

#### 4.4.2 Database Optimization
```sql
-- Performance optimization indexes
CREATE INDEX CONCURRENTLY idx_documents_user_created 
ON documents(user_id, created_at DESC);

CREATE INDEX CONCURRENTLY idx_chat_messages_session_timestamp 
ON chat_messages(session_id, timestamp DESC);

CREATE INDEX CONCURRENTLY idx_users_email_active 
ON users(email, is_active) WHERE is_active = true;

-- Partitioning for large tables
CREATE TABLE chat_messages_y2024m01 PARTITION OF chat_messages
FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
```

## 5. Security and Compliance Enhancements

### 5.1 Current Security Implementation
- JWT authentication with bcrypt password hashing
- CORS protection with specific origins
- Input validation with Pydantic schemas
- Environment variable management

### 5.2 Enhanced Security Requirements

#### 5.2.1 Advanced Authentication
```python
class EnhancedAuth:
    def __init__(self):
        self.mfa_enabled = True
        self.session_timeout = 3600  # 1 hour
        self.password_policy = PasswordPolicy()
    
    async def setup_mfa(self, user_id: str) -> MFASetup:
        # Implement TOTP-based MFA
        pass
    
    async def verify_mfa(self, user_id: str, token: str) -> bool:
        # Verify MFA token
        pass
    
    async def audit_login(self, user_id: str, success: bool, ip_address: str):
        # Log authentication attempts
        pass
```

#### 5.2.2 Data Encryption and Privacy
```python
class DataProtection:
    def __init__(self):
        self.encryption_key = os.getenv('ENCRYPTION_KEY')
        self.fernet = Fernet(self.encryption_key)
    
    def encrypt_sensitive_data(self, data: str) -> str:
        # Encrypt PII and sensitive document content
        return self.fernet.encrypt(data.encode()).decode()
    
    def decrypt_sensitive_data(self, encrypted_data: str) -> str:
        # Decrypt when needed for processing
        return self.fernet.decrypt(encrypted_data.encode()).decode()
    
    async def anonymize_user_data(self, user_id: str):
        # Implement GDPR-compliant data anonymization
        pass
```

#### 5.2.3 Document Security
```python
class DocumentSecurity:
    def __init__(self):
        self.virus_scanner = ClamAVScanner()
        self.content_filter = ContentFilter()
    
    async def scan_document(self, file_content: bytes) -> SecurityScanResult:
        # Virus and malware scanning
        virus_result = await self.virus_scanner.scan(file_content)
        
        # Content filtering for sensitive information
        content_result = await self.content_filter.analyze(file_content)
        
        return SecurityScanResult(virus_result, content_result)
```

## 6. Business Model and Pricing Strategy

### 6.1 Current Implementation Gaps
- No subscription management
- No usage tracking and billing
- No tier-based feature restrictions

### 6.2 Enhanced Business Model Implementation

#### 6.2.1 Subscription Tiers
```python
class SubscriptionTier(Enum):
    FREE = "free"
    PROFESSIONAL = "professional"
    TEAM = "team"
    ENTERPRISE = "enterprise"

class SubscriptionLimits:
    LIMITS = {
        SubscriptionTier.FREE: {
            'documents_per_month': 5,
            'ai_queries_per_month': 50,
            'storage_mb': 100,
            'features': ['basic_analysis', 'document_upload']
        },
        SubscriptionTier.PROFESSIONAL: {
            'documents_per_month': 100,
            'ai_queries_per_month': 1000,
            'storage_mb': 5000,
            'features': ['basic_analysis', 'advanced_analysis', 'clause_extraction', 'export']
        },
        SubscriptionTier.TEAM: {
            'documents_per_month': 500,
            'ai_queries_per_month': 5000,
            'storage_mb': 25000,
            'features': ['all_professional', 'team_collaboration', 'admin_dashboard']
        },
        SubscriptionTier.ENTERPRISE: {
            'documents_per_month': -1,  # Unlimited
            'ai_queries_per_month': -1,
            'storage_mb': -1,
            'features': ['all_features', 'custom_integration', 'priority_support']
        }
    }
```

#### 6.2.2 Usage Tracking and Billing
```python
class UsageTracker:
    def __init__(self):
        self.redis_client = redis.Redis.from_url(os.getenv('REDIS_URL'))
    
    async def track_document_upload(self, user_id: str):
        key = f"usage:{user_id}:documents:{datetime.now().strftime('%Y-%m')}"
        await self.redis_client.incr(key)
        await self.redis_client.expire(key, 86400 * 32)  # 32 days
    
    async def track_ai_query(self, user_id: str):
        key = f"usage:{user_id}:queries:{datetime.now().strftime('%Y-%m')}"
        await self.redis_client.incr(key)
        await self.redis_client.expire(key, 86400 * 32)
    
    async def check_limits(self, user_id: str, action: str) -> bool:
        user_tier = await self.get_user_tier(user_id)
        current_usage = await self.get_current_usage(user_id, action)
        limit = SubscriptionLimits.LIMITS[user_tier][f"{action}_per_month"]
        
        return limit == -1 or current_usage < limit
```

## 7. Testing and Quality Assurance

### 7.1 Current Testing Gaps
Based on code analysis, there are no visible test files or testing infrastructure.

### 7.2 Comprehensive Testing Strategy

#### 7.2.1 Backend Testing Framework
```python
# pytest configuration with FastAPI test client
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db, Base

SQLALCHEMY_DATABASE_URL = "postgresql://test:test@localhost:5432/test_db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(test_db):
    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

# Test cases
class TestAuthentication:
    def test_user_signup(self, client):
        response = client.post("/auth/signup", json={
            "username": "testuser",
            "email": "test@example.com", 
            "password": "TestPass123"
        })
        assert response.status_code == 200
        assert "id" in response.json()

    def test_user_login(self, client):
        # Create user first
        client.post("/auth/signup", json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "TestPass123"
        })
        
        # Test login
        response = client.post("/auth/login", json={
            "email": "test@example.com",
            "password": "TestPass123"
        })
        assert response.status_code == 200
        assert "access_token" in response.json()

class TestDocumentProcessing:
    def test_document_upload(self, client, auth_headers):
        with open("test_document.pdf", "rb") as f:
            response = client.post(
                "/upload",
                files={"file": ("test.pdf", f, "application/pdf")},
                headers=auth_headers
            )
        assert response.status_code == 200
        assert "document" in response.json()

    def test_ai_query(self, client):
        response = client.post("/ask", json={
            "question": "What are the key terms in this contract?",
            "file_content": "Sample contract content..."
        })
        assert response.status_code == 200
        assert "answer" in response.json()
```

#### 7.2.2 Frontend Testing Framework
```javascript
// Jest and React Testing Library setup
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { ChatInterface } from '../src/components/ChatInterface';
import { FileUpload } from '../src/components/FileUpload';

// Mock API calls
jest.mock('../src/api', () => ({
  sendQuery: jest.fn(() => Promise.resolve('Mock AI response')),
  loginUser: jest.fn(() => Promise.resolve({ access_token: 'mock_token' }))
}));

describe('ChatInterface', () => {
  test('renders chat interface correctly', () => {
    render(<ChatInterface uploadedFile={null} messages={[]} setMessages={jest.fn()} />);
    expect(screen.getByText('Welcome to LegalDoc Document Analyzer')).toBeInTheDocument();
  });

  test('sends message and receives response', async () => {
    const setMessages = jest.fn();
    render(<ChatInterface uploadedFile={null} messages={[]} setMessages={setMessages} />);
    
    const input = screen.getByPlaceholderText(/Ask about legal matters/);
    const submitButton = screen.getByRole('button', { name: /send/i });
    
    fireEvent.change(input, { target: { value: 'Test question' } });
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(setMessages).toHaveBeenCalledWith(expect.any(Function));
    });
  });
});

describe('FileUpload', () => {
  test('handles file drop correctly', () => {
    const onFileUpload = jest.fn();
    render(<FileUpload onFileUpload={onFileUpload} />);
    
    const dropzone = screen.getByRole('button', { name: /upload legal document/i });
    const file = new File(['test content'], 'test.pdf', { type: 'application/pdf' });
    
    fireEvent.drop(dropzone, { dataTransfer: { files: [file] } });
    
    expect(onFileUpload).toHaveBeenCalledWith(file);
  });
});
```

#### 7.2.3 Integration Testing
```python
class TestIntegration:
    def test_complete_document_analysis_workflow(self, client, test_user):
        # 1. Upload document
        with open("test_contract.pdf", "rb") as f:
            upload_response = client.post(
                "/upload",
                files={"file": ("contract.pdf", f, "application/pdf")},
                headers=self.get_auth_headers(test_user)
            )
        
        # 2. Query the document
        query_response = client.post("/ask", json={
            "question": "What are the termination clauses?",
            "file_content": "Sample contract with termination clause..."
        })
        
        # 3. Verify analysis quality
        assert "termination" in query_response.json()["answer"].lower()
        
    def test_admin_workflow(self, client, admin_user):
        # 1. Access admin dashboard
        metrics_response = client.get(
            "/admin/metrics",
            headers=self.get_auth_headers(admin_user)
        )
        
        # 2. Upload to vector store
        with open("legal_precedent.pdf", "rb") as f:
            vector_response = client.post(
                "/admin/vector-upload",
                files={"file": ("precedent.pdf", f, "application/pdf")},
                headers=self.get_auth_headers(admin_user)
            )
        
        assert metrics_response.status_code == 200
        assert vector_response.status_code == 200
```

## 8. Performance Optimization

### 8.1 Current Performance Analysis
Based on code review, current optimizations include:
- Lazy loading of embedding models
- Memory management with garbage collection
- Configurable chunk sizes and batch processing
- Redis caching for retriever results

### 8.2 Enhanced Performance Strategies

#### 8.2.1 Database Optimization
```python
class DatabaseOptimizer:
    async def optimize_queries(self):
        # Connection pooling
        engine = create_engine(
            DATABASE_URL,
            pool_size=20,
            max_overflow=0,
            pool_pre_ping=True,
            pool_recycle=300
        )
        
        # Query optimization with indexes
        await self.create_performance_indexes()
        
        # Read replicas for analytics
        self.setup_read_replicas()
    
    async def cache_frequent_queries(self):
        # Cache user documents list
        # Cache analysis results
        # Cache vector search results
        pass
```

#### 8.2.2 AI Model Optimization
```python
class ModelOptimizer:
    def __init__(self):
        self.model_cache = {}
        self.embedding_cache = LRUCache(maxsize=1000)
    
    async def optimize_gemini_calls(self):
        # Batch multiple queries when possible
        # Cache common responses
        # Implement request deduplication
        pass
    
    async def optimize_vector_search(self):
        # Index warming strategies
        # Query result caching
        # Embedding reuse for similar queries
        pass
```

## 9. Future Roadmap and Scalability

### 9.1 Phase 1: Core Enhancements (Months 1-3)
1. **Admin Dashboard Implementation**
   - User management interface
   - Usage analytics and metrics
   - Vector database management
   - System monitoring tools

2. **Enhanced AI Features**
   - Clause extraction engine
   - Document summarization service
   - Compliance checking
   - Legal precedent recommendations

3. **Improved User Experience**
   - Chat history persistence
   - Document export functionality
   - Advanced search and filtering
   - Mobile responsiveness improvements

### 9.2 Phase 2: Advanced Features (Months 4-6)
1. **Multi-language Support**
   - Hindi, Marathi, Tamil, Telugu, Bengali
   - Regional legal document processing
   - Multilingual AI responses

2. **Collaboration Features**
   - Team workspaces
   - Document sharing and comments
   - Real-time collaboration
   - Version control for documents

3. **Advanced Analytics**
   - Document comparison tools
   - Trend analysis
   - Risk assessment dashboards
   - Compliance tracking

### 9.3 Phase 3: Enterprise Features (Months 7-12)
1. **API Platform**
   - Public API with rate limiting
   - Webhook integrations
   - Third-party application support
   - Custom model training

2. **Advanced Security**
   - SSO integration
   - Advanced audit trails
   - Data loss prevention
   - Compliance certifications (SOC 2, ISO 27001)

3. **Scalability Enhancements**
   - Microservices architecture
   - Kubernetes deployment
   - Global CDN integration
   - Advanced caching strategies

## 10. Risk Assessment and Mitigation

### 10.1 Technical Risks

#### 10.1.1 AI Model Accuracy
**Risk**: Inaccurate legal analysis leading to professional liability
**Mitigation**:
- Continuous model validation with legal experts
- Confidence scoring for all outputs
- Clear disclaimers about AI limitations
- Human review workflows for critical analysis

#### 10.1.2 Scalability Limitations
**Risk**: System performance degradation under load
**Mitigation**:
- Comprehensive load testing
- Auto-scaling infrastructure
- Database optimization and indexing
- Caching strategies implementation

#### 10.1.3 Data Security Breaches
**Risk**: Unauthorized access to sensitive legal documents
**Mitigation**:
- End-to-end encryption
- Regular security audits
- Access logging and monitoring
- Compliance with data protection regulations

### 10.2 Business Risks

#### 10.2.1 Regulatory Compliance
**Risk**: Non-compliance with legal industry regulations
**Mitigation**:
- Regular compliance reviews
- Legal expert consultations
- Industry certification pursuit
- Transparent privacy policies

#### 10.2.2 Market Competition
**Risk**: Competition from established legal tech companies
**Mitigation**:
- Focus on Indian legal specificity
- Continuous feature innovation
- Strong customer relationships
- Competitive pricing strategies

## 11. Conclusion

This comprehensive SRS document provides a detailed roadmap for enhancing the current LegalDoc implementation. The analysis reveals a solid foundation with significant opportunities for improvement and expansion.

### 11.1 Key Strengths of Current Implementation
- Robust authentication and user management
- Efficient document processing pipeline
- Modern React frontend with good UX
- Scalable FastAPI backend architecture
- Cost-effective deployment strategy

### 11.2 Critical Enhancement Areas
- Admin dashboard and user management
- Advanced AI-powered legal analysis features
- Comprehensive testing and quality assurance
- Enhanced security and compliance measures
- Performance optimization and scalability

### 11.3 Success Metrics
- **Technical**: 99.9% uptime, <2s response times, >90% analysis accuracy
- **Business**: 1000+ users in 6 months, 80% user retention, profitable operations
- **Legal**: Compliance with Indian legal standards, positive feedback from legal professionals

This SRS serves as a blueprint for transforming LegalDoc from its current state into a comprehensive, enterprise-ready legal document analysis platform that can compete effectively in the Indian legal technology market while maintaining cost-effectiveness and high user satisfaction.
