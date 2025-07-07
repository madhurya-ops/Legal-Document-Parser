# LegalDoc Project

A comprehensive legal document processing application with user authentication.

## Features

- **Frontend**: React-based web interface
- **Backend**: FastAPI with PostgreSQL authentication
- **Document Processing**: AI-powered legal document analysis
- **User Management**: Complete authentication system with JWT tokens

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Node.js (for local frontend development)
- Python 3.11+ (for local backend development)

### Using Docker Compose (Recommended)

1. **Clone and navigate to the project:**
   ```bash
   cd legaldoc
   ```

2. **Start all services:**
   ```bash
   docker-compose up --build
   ```

3. **Access the applications:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Manual Setup

#### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create environment file:**
   ```bash
   # Create .env file with the following content:
   DATABASE_URL=postgresql://postgres:postgres@localhost:5432/auth_db
   SECRET_KEY=your-super-secret-key-change-this-in-production
   HF_API_KEY=your-huggingface-api-key
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start PostgreSQL (if not using Docker):**
   ```bash
   # Using Docker for PostgreSQL only
   docker run --name postgres -e POSTGRES_DB=auth_db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:15
   ```

5. **Initialize database:**
   ```bash
   python init_db.py
   ```

6. **Start the backend:**
   ```bash
   uvicorn app.main:app --reload
   ```

#### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd my-app
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the frontend:**
   ```bash
   npm start
   ```

## Authentication System

The backend includes a complete authentication system with the following features:

### API Endpoints

- `POST /auth/signup` - Register a new user
- `POST /auth/login` - Login and get access token
- `GET /auth/me` - Get current user profile

### Security Features

- **Password Hashing**: Bcrypt for secure password storage
- **JWT Tokens**: Secure token-based authentication
- **Input Validation**: Comprehensive validation for all inputs
- **CORS Protection**: Configured for specific origins

### Testing the Authentication

1. **Start the services:**
   ```bash
   docker-compose up --build
   ```

2. **Run the test script:**
   ```bash
   cd backend
   python test_auth.py
   ```

3. **Or test manually using curl:**
   ```bash
   # Signup
   curl -X POST "http://localhost:8000/auth/signup" \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "email": "test@example.com", "password": "TestPass123"}'

   # Login
   curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"email": "test@example.com", "password": "TestPass123"}'
   ```

## Project Structure

```
legaldoc/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Core functionality
│   │   ├── auth.py         # Authentication logic
│   │   ├── crud.py         # Database operations
│   │   ├── database.py     # Database configuration
│   │   ├── models.py       # SQLAlchemy models
│   │   ├── schemas.py      # Pydantic schemas
│   │   └── main.py         # FastAPI application
│   ├── requirements.txt    # Python dependencies
│   ├── Dockerfile          # Backend container
│   ├── init_db.py          # Database initialization
│   └── test_auth.py        # Authentication tests
├── my-app/                 # React frontend
├── docker-compose.yml      # Docker services
└── README.md              # This file
```

## Database Schema

### Users Table
- `id` (UUID, Primary Key)
- `username` (String, Unique)
- `email` (String, Unique)
- `hashed_password` (String)
- `is_active` (Boolean)
- `created_at` (DateTime)
- `updated_at` (DateTime)

## Environment Variables

### Backend (.env)
```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/auth_db
SECRET_KEY=your-super-secret-key-change-this-in-production
HF_API_KEY=your-huggingface-api-key
```

## Development

### Adding New Features

1. **Backend**: Add new routes in `backend/app/api/`
2. **Frontend**: Add new components in `my-app/src/components/`
3. **Database**: Add new models in `backend/app/models.py`

### Database Migrations

The current setup creates tables automatically. For production, consider using Alembic for database migrations.

## Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Ensure PostgreSQL is running
   - Check DATABASE_URL in environment variables
   - Verify Docker services are up: `docker-compose ps`

2. **Authentication Errors**
   - Check SECRET_KEY is set
   - Verify JWT token format
   - Ensure CORS is properly configured

3. **Port Conflicts**
   - Change ports in docker-compose.yml if needed
   - Ensure no other services are using ports 3000, 8000, or 5432

### Logs

View logs for specific services:
```bash
# Backend logs
docker-compose logs backend

# Database logs
docker-compose logs db

# All logs
docker-compose logs
```

## Security Notes

- Change the default SECRET_KEY in production
- Use strong passwords for database access
- Configure proper CORS origins for production
- Consider using HTTPS in production
- Regularly update dependencies

## License

This project is licensed under the MIT License.
