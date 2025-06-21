# LegalDoc Backend with Authentication

This is a FastAPI backend with PostgreSQL authentication system for the LegalDoc project.

## Features

- **User Authentication**: Complete signup/login system with JWT tokens
- **Password Security**: Bcrypt password hashing
- **Database**: PostgreSQL with SQLAlchemy ORM
- **API Documentation**: Auto-generated with FastAPI
- **CORS Support**: Configured for frontend integration

## API Endpoints

### Authentication
- `POST /auth/signup` - Register a new user
- `POST /auth/login` - Login and get access token
- `GET /auth/me` - Get current user profile (requires authentication)

### Request/Response Examples

#### Signup
```bash
curl -X POST "http://localhost:8000/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePass123"
  }'
```

#### Login
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123"
  }'
```

#### Get Profile (with token)
```bash
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Setup Instructions

### 1. Environment Variables

Create a `.env` file in the backend directory with:

```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/auth_db
SECRET_KEY=your-super-secret-key-change-this-in-production
HF_API_KEY=your-huggingface-api-key
```

### 2. Using Docker Compose (Recommended)

```bash
# Start all services
docker-compose up --build

# The API will be available at http://localhost:8000
# API documentation at http://localhost:8000/docs
```

### 3. Manual Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/auth_db"
export SECRET_KEY="your-secret-key"

# Run the application
uvicorn app.main:app --reload
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

## Security Features

- **Password Hashing**: Uses bcrypt for secure password storage
- **JWT Tokens**: Secure token-based authentication
- **Input Validation**: Comprehensive validation for all inputs
- **CORS Protection**: Configured for specific origins
- **Environment Variables**: Sensitive data stored in environment variables

## Password Requirements

Passwords must meet the following criteria:
- At least 8 characters long
- Contains at least one uppercase letter
- Contains at least one lowercase letter
- Contains at least one digit

## Development

### Adding New Endpoints

1. Create new routes in `app/api/` directory
2. Include them in `app/main.py`
3. Add authentication dependencies where needed

### Database Migrations

The current setup creates tables automatically. For production, consider using Alembic for database migrations.

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc 