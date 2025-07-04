# JWT Authentication System Setup

## Overview

Your FastAPI backend now includes a complete JWT-based authentication system with the following features:

- ✅ **JWT Token Generation**: Using `python-jose[cryptography]` with HS256 algorithm
- ✅ **15-minute Token Expiry**: Configurable via environment variables
- ✅ **Protected Routes**: `/me` endpoints require valid JWT tokens
- ✅ **Password Hashing**: Bcrypt for secure password storage
- ✅ **Input Validation**: Comprehensive validation for all inputs

## Environment Variables

Create a `.env` file in the `backend` directory with:

```env
# Database Configuration
DATABASE_URL=postgresql://postgres:postgres@db:5432/auth_db

# JWT Authentication Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15

# Gemini API Key (for LLM functionality)
GEMINI_API_KEY=your-gemini-api-key
```

## API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/signup` | Register new user | No |
| POST | `/auth/login` | Login with email/password | No |
| POST | `/login` | Login with email/password (root level) | No |
| GET | `/auth/me` | Get user profile | Yes |
| GET | `/me` | Get user profile (root level) | Yes |

## Testing the JWT System

### 1. Using the Test Script

Run the comprehensive test script:

```bash
cd backend
python test_jwt_auth.py
```

This will test:
- User signup
- JWT token generation
- Protected route access
- Invalid token rejection
- Missing token rejection
- Multiple login support
- Wrong password validation

### 2. Manual Testing with curl

#### Signup
```bash
curl -X POST "http://localhost:8000/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "SecurePass123"
  }'
```

#### Login (get JWT token)
```bash
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123"
  }'
```

#### Access Protected Route
```bash
curl -X GET "http://localhost:8000/me" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

### 3. Using Postman

#### Signup Request
- **Method**: POST
- **URL**: `http://localhost:8000/auth/signup`
- **Headers**: `Content-Type: application/json`
- **Body** (raw JSON):
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "SecurePass123"
}
```

#### Login Request
- **Method**: POST
- **URL**: `http://localhost:8000/login`
- **Headers**: `Content-Type: application/json`
- **Body** (raw JSON):
```json
{
  "email": "test@example.com",
  "password": "SecurePass123"
}
```

#### Protected Route Request
- **Method**: GET
- **URL**: `http://localhost:8000/me`
- **Headers**: 
  - `Content-Type: application/json`
  - `Authorization: Bearer YOUR_JWT_TOKEN_HERE`

## JWT Token Structure

The JWT tokens contain the following payload:

```json
{
  "sub": "user@example.com",
  "exp": 1234567890,
  "iat": 1234567800
}
```

- `sub`: Subject (user's email)
- `exp`: Expiration timestamp
- `iat`: Issued at timestamp

## Security Features

### Password Requirements
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit

### JWT Security
- HS256 algorithm for signing
- 15-minute expiration (configurable)
- Secure secret key from environment
- Token validation on protected routes

### Database Security
- Passwords hashed with bcrypt
- UUID primary keys
- Unique constraints on email and username
- Timestamps for audit trail

## Code Structure

```
backend/app/
├── auth.py              # JWT utilities and authentication logic
├── crud.py              # Database operations
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic schemas
├── database.py          # Database configuration
├── main.py              # FastAPI application
└── api/
    └── auth_routes.py   # Authentication endpoints
```

## Key Functions

### Token Generation
```python
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token with configurable expiry"""
```

### Token Verification
```python
def verify_access_token(token: str, credentials_exception: HTTPException) -> str:
    """Verify JWT token and return subject"""
```

### User Authentication
```python
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current authenticated user from JWT token"""
```

## Troubleshooting

### Common Issues

1. **"email-validator is not installed"**
   - Solution: The package is already included in requirements.txt
   - Rebuild the Docker container: `docker-compose up --build backend -d`

2. **"Could not validate credentials"**
   - Check if the JWT token is valid and not expired
   - Ensure the token is in the correct format: `Bearer <token>`

3. **"Incorrect email or password"**
   - Verify the user exists in the database
   - Check password requirements are met

4. **Database connection issues**
   - Ensure PostgreSQL is running: `docker-compose ps`
   - Check database logs: `docker-compose logs db`

### Logs

View authentication-related logs:
```bash
# Backend logs
docker-compose logs backend

# Database logs
docker-compose logs db
```

## Production Considerations

1. **Change the SECRET_KEY** to a strong, random value
2. **Use HTTPS** in production
3. **Configure proper CORS origins**
4. **Set up database migrations** (consider Alembic)
5. **Add rate limiting** for login endpoints
6. **Implement refresh tokens** for better security
7. **Add logging** for authentication events

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These provide interactive documentation for all endpoints including the JWT authentication system. 