# Legal Document Parser - Full Stack Application

🏛️ **AI-powered legal document analysis platform** with comprehensive backend API and modern React frontend.

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+** with pip
- **Node.js 18+** with npm
- **PostgreSQL** (for production) or SQLite (for development)
- **Redis** (optional, for caching)

### Development Setup

1. **Start the Backend API**
   ```bash
   # Navigate to the API directory
   cd api
   
   # Install Python dependencies
   pip install -r requirements.txt
   
   # Copy environment configuration
   cp .env.example .env
   
   # Edit .env with your settings (database, API keys, etc.)
   nano .env
   
   # Run database migrations (if using PostgreSQL)
   alembic upgrade head
   
   # Start the FastAPI server
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Start the Frontend**
   ```bash
   # Navigate to the frontend directory
   cd web/my-app
   
   # Install Node.js dependencies
   npm install
   
   # Start the React development server
   npm start
   ```

3. **Access the Application**
   - **Frontend**: http://localhost:3000
   - **Backend API**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/docs

### Using the Development Script

Alternatively, use the automated development script:

```bash
# Make the script executable
chmod +x start_dev.py

# Run the development environment
python start_dev.py
```

## 🏗️ Architecture

### Backend (FastAPI)
- **Location**: `/api`
- **Features**:
  - RESTful API with automatic OpenAPI documentation
  - JWT-based authentication and authorization
  - Role-based access control (User/Admin)
  - Document upload and management
  - AI-powered legal analysis with Gemini API
  - Vector store integration with FAISS
  - Legal services (clause extraction, compliance checking, precedent search)
  - Admin dashboard with analytics
  - Chat sessions and message history
  - Comprehensive logging and error handling

### Frontend (React)
- **Location**: `/web/my-app`
- **Features**:
  - Modern React 18 with hooks and context
  - Tailwind CSS for responsive design
  - Dark/light theme support
  - Real-time document upload with progress tracking
  - Interactive chat interface
  - Admin dashboard with system metrics
  - Legal analysis tools panel
  - Document management interface
  - User authentication and profile management

## 📁 Project Structure

```
Legal-Document-Parser-test_c/
├── api/                           # FastAPI Backend
│   ├── app/
│   │   ├── api/                   # API route handlers
│   │   │   ├── __init__.py
│   │   │   ├── admin.py          # Admin dashboard endpoints
│   │   │   ├── auth.py           # Authentication endpoints
│   │   │   ├── chat.py           # Chat session management
│   │   │   ├── documents.py      # Document upload/management
│   │   │   ├── legal.py          # Legal analysis endpoints
│   │   │   └── query.py          # AI query processing
│   │   ├── core/                  # Core application components
│   │   │   ├── config.py         # Configuration management
│   │   │   ├── database.py       # Database connection
│   │   │   ├── logging_config.py # Logging setup
│   │   │   └── security.py       # JWT and password handling
│   │   ├── models/                # SQLAlchemy ORM models
│   │   │   ├── __init__.py
│   │   │   ├── analysis.py       # Document analysis models
│   │   │   ├── chat.py           # Chat session models
│   │   │   ├── document.py       # Document models
│   │   │   └── user.py           # User models
│   │   ├── schemas/               # Pydantic schemas
│   │   │   └── __init__.py       # API request/response schemas
│   │   ├── services/              # Business logic services
│   │   │   ├── __init__.py
│   │   │   ├── ai_service.py     # AI integration wrapper
│   │   │   ├── crud.py           # Database operations
│   │   │   ├── legal_analysis.py # Legal analysis services
│   │   │   ├── llm_client.py     # LLM client (Gemini API)
│   │   │   └── vector_store.py   # Vector database operations
│   │   ├── utils/                 # Utility functions
│   │   │   ├── __init__.py
│   │   │   └── pdf_parser.py     # PDF text extraction
│   │   └── main.py               # FastAPI application entry point
│   ├── requirements.txt          # Python dependencies
│   └── .env.example             # Environment configuration template
├── web/my-app/                   # React Frontend
│   ├── public/                   # Static assets
│   ├── src/
│   │   ├── components/           # React components
│   │   │   ├── ui/               # Reusable UI components
│   │   │   ├── AboutPage.js      # About page component
│   │   │   ├── AdminDashboard.js # Admin dashboard
│   │   │   ├── AuthPage.js       # Authentication form
│   │   │   ├── ChatInterface.js  # Chat interface
│   │   │   ├── EnhancedDashboard.js # Main user dashboard
│   │   │   ├── FileUpload.js     # File upload component
│   │   │   ├── HomePage.js       # Landing page
│   │   │   └── ...               # Other components
│   │   ├── api.js                # API client functions
│   │   ├── App.js                # Main application component
│   │   ├── index.js              # React entry point
│   │   └── ...
│   ├── package.json              # Node.js dependencies
│   └── tailwind.config.js        # Tailwind CSS configuration
├── deploy/                       # Deployment configurations
│   ├── docker-compose.yml        # Multi-service Docker setup
│   └── Dockerfile               # Backend container definition
├── config/                       # Configuration files
│   └── production.env           # Production environment variables
├── scripts/                      # Utility scripts
│   └── init-db.sql             # Database initialization
├── start_dev.py                 # Development startup script
└── README.md                    # This file
```

## 🔧 Configuration

### Backend Configuration (`.env`)

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/legaldoc
# or for SQLite: DATABASE_URL=sqlite:///./legal_doc.db

# Security
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI/LLM Configuration
GEMINI_API_KEY=your-gemini-api-key
GEMINI_API_URL=https://generativelanguage.googleapis.com/v1beta

# Redis (optional)
REDIS_URL=redis://localhost:6379/0

# CORS
CORS_ORIGINS=["http://localhost:3000", "http://127.0.0.1:3000"]
ALLOWED_HOSTS=["localhost", "127.0.0.1"]

# Logging
LOG_LEVEL=INFO
DEBUG=true
```

### Frontend Configuration

Create `web/my-app/.env.local`:

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_API_TIMEOUT=90000
REACT_APP_API_RETRIES=3
```

## 🌟 Key Features

### Authentication & Authorization
- JWT-based authentication
- Role-based access control (User/Admin)
- Secure password hashing
- Session management

### Document Management
- Multi-format file upload (PDF, DOCX, TXT)
- Duplicate detection via file hashing
- Document versioning and metadata
- Secure file storage

### AI-Powered Legal Analysis
- **Clause Extraction**: Identify and categorize legal clauses
- **Compliance Checking**: Verify regulatory compliance
- **Precedent Search**: Find relevant legal precedents
- **Risk Assessment**: Analyze potential legal risks
- **Document Summarization**: Generate concise summaries

### Admin Dashboard
- User management and analytics
- Document statistics and storage metrics
- System health monitoring
- Activity logs and audit trails

### Vector Store Integration
- FAISS-based vector database
- Document embedding and similarity search
- Efficient retrieval of relevant legal documents

## 🚀 Deployment

### Docker Deployment

1. **Build and run with Docker Compose**:
   ```bash
   # Production deployment
   docker-compose -f deploy/docker-compose.yml up -d
   ```

2. **Individual container builds**:
   ```bash
   # Build backend
   docker build -f deploy/Dockerfile -t legal-doc-api .
   
   # Build frontend
   cd web/my-app && docker build -t legal-doc-frontend .
   ```

### Environment-Specific Deployment

- **Development**: Use `start_dev.py` script
- **Staging**: Use `config/staging.env`
- **Production**: Use `config/production.env`

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/signup` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user

### Documents
- `POST /api/documents/upload` - Upload document
- `GET /api/documents/` - List user documents
- `DELETE /api/documents/{id}` - Delete document

### Legal Analysis
- `POST /api/legal/extract-clauses` - Extract legal clauses
- `POST /api/legal/compliance-check` - Check compliance
- `POST /api/legal/precedent-search` - Search precedents

### Admin (Requires admin role)
- `GET /api/admin/dashboard` - Dashboard statistics
- `GET /api/admin/users` - List all users
- `PUT /api/admin/users/{id}` - Update user
- `GET /api/admin/metrics` - System metrics

### AI Query
- `POST /api/query/ask` - Submit AI query
- `POST /api/query/extract-pdf-text` - Extract PDF text

## 🧪 Testing

### Backend Tests
```bash
cd api
pytest tests/ -v
```

### Frontend Tests
```bash
cd web/my-app
npm test
```

## 📊 Monitoring & Logging

- **Structured logging** with configurable levels
- **Request/response tracking** with correlation IDs
- **Performance monitoring** with response time metrics
- **Error tracking** with detailed stack traces
- **Admin analytics** with user and document statistics

## 🔒 Security Features

- **Password hashing** with bcrypt
- **JWT token authentication** with expiration
- **CORS protection** with configurable origins
- **Input validation** with Pydantic schemas
- **SQL injection protection** with SQLAlchemy ORM
- **File upload security** with type validation and size limits

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support, please:
1. Check the [API documentation](http://localhost:8000/docs) when running locally
2. Review the logs in the console output
3. Open an issue on GitHub with detailed error information

---

**🏛️ LegalDoc** - Transforming legal document analysis with AI-powered insights.
