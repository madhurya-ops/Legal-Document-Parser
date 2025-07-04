# LegalDoc Docker Setup Guide

This guide will help you set up and run the LegalDoc application using Docker for both development and production environments.

## 🐳 Prerequisites

- **Docker Desktop** (version 4.0+)
- **Docker Compose** (version 2.0+)
- **Git** (for cloning the repository)
- **8GB+ RAM** (recommended for optimal performance)

### Verify Prerequisites

```bash
# Check Docker version
docker --version
docker-compose --version

# Ensure Docker is running
docker info
```

## 🚀 Quick Start (Development)

### 1. Clone and Setup

```bash
git clone <repository-url>
cd Legal-Document-Parser
```

### 2. Use the Management Script

We've provided a convenient script to manage the Docker environment:

```bash
# Make script executable (if not already)
chmod +x docker-dev.sh

# Start the development environment
./docker-dev.sh start

# Check status
./docker-dev.sh status

# View logs
./docker-dev.sh logs

# Setup admin users
./docker-dev.sh setup-admin
```

### 3. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Database**: localhost:5432
- **Redis**: localhost:6379

## 📋 Management Script Commands

```bash
./docker-dev.sh start        # Start development environment
./docker-dev.sh stop         # Stop development environment
./docker-dev.sh restart      # Restart development environment
./docker-dev.sh build        # Build all Docker services
./docker-dev.sh logs         # View all service logs
./docker-dev.sh logs backend # View specific service logs
./docker-dev.sh status       # Show service status
./docker-dev.sh setup-admin  # Setup admin users
./docker-dev.sh migrate      # Run database migrations
./docker-dev.sh cleanup      # Clean up Docker resources
./docker-dev.sh help         # Show help
```

## ⚙️ Manual Docker Commands

If you prefer to use Docker Compose directly:

### Development Environment

```bash
# Start all services
docker-compose up -d

# Build and start
docker-compose up -d --build

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Check service status
docker-compose ps

# Execute commands in containers
docker-compose exec backend python setup_admin.py
docker-compose exec backend python migrate_database.py
docker-compose exec db psql -U legaldoc_user -d legaldoc_db
```

## 🏭 Production Deployment

### 1. Environment Variables

Create a `.env.prod` file with production values:

```bash
# Database
POSTGRES_DB=legaldoc_prod
POSTGRES_USER=legaldoc_prod_user
POSTGRES_PASSWORD=your_secure_db_password_here

# Redis
REDIS_PASSWORD=your_secure_redis_password_here

# JWT & Security
SECRET_KEY=your_super_secret_jwt_key_for_production

# AI Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Domains
FRONTEND_URL=https://yourdomain.com
PRODUCTION_URL=https://yourdomain.com
FRONTEND_API_URL=https://api.yourdomain.com

# System Prompt (optional)
SYSTEM_PROMPT=Your custom system prompt for production
```

### 2. Deploy Production

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Start production environment
docker-compose -f docker-compose.prod.yml up -d

# Check production status
docker-compose -f docker-compose.prod.yml ps

# View production logs
docker-compose -f docker-compose.prod.yml logs -f
```

### 3. SSL Setup (Production)

For HTTPS in production, you'll need to:

1. Set up SSL certificates (Let's Encrypt recommended)
2. Configure the Nginx reverse proxy
3. Update DNS records

```bash
# Create SSL directory
mkdir -p nginx/ssl

# Place your SSL certificates in nginx/ssl/
# - certificate.crt
# - private.key
```

## 🗄️ Database Operations

### Backup Database

```bash
# Create backup
docker-compose exec db pg_dump -U legaldoc_user legaldoc_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore from backup
docker-compose exec -T db psql -U legaldoc_user legaldoc_db < backup_file.sql
```

### Access Database

```bash
# Access PostgreSQL shell
docker-compose exec db psql -U legaldoc_user -d legaldoc_db

# Run SQL commands
docker-compose exec db psql -U legaldoc_user -d legaldoc_db -c "SELECT COUNT(*) FROM users;"
```

### Reset Database

```bash
# Stop services
docker-compose down

# Remove database volume
docker volume rm legal-document-parser_postgres_data

# Start fresh
docker-compose up -d
./docker-dev.sh setup-admin
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Port Conflicts

If ports 3000, 8000, 5432, or 6379 are already in use:

```bash
# Check what's using the port
lsof -i :3000
lsof -i :8000
lsof -i :5432
lsof -i :6379

# Stop conflicting services or modify docker-compose.yml ports
```

#### 2. Docker Out of Space

```bash
# Clean up Docker resources
docker system prune -a

# Remove unused volumes
docker volume prune

# Use our cleanup script
./docker-dev.sh cleanup
```

#### 3. Services Not Starting

```bash
# Check Docker logs
docker-compose logs

# Check specific service
docker-compose logs backend

# Restart specific service
docker-compose restart backend
```

#### 4. Database Connection Issues

```bash
# Check database health
docker-compose exec db pg_isready -U legaldoc_user -d legaldoc_db

# Reset database
docker-compose down
docker volume rm legal-document-parser_postgres_data
docker-compose up -d db
```

#### 5. Build Issues

```bash
# Clean build (removes cache)
docker-compose build --no-cache

# Remove all containers and rebuild
docker-compose down
docker system prune -a
docker-compose up -d --build
```

### Health Checks

The application includes built-in health checks:

```bash
# Check all service health
curl http://localhost:8000/health  # Backend
curl http://localhost:3000/health  # Frontend
curl http://localhost:3000/        # Frontend home

# Docker health status
docker-compose ps
```

### Performance Optimization

#### Memory Usage

```bash
# Monitor container resource usage
docker stats

# Limit container memory (add to docker-compose.yml)
services:
  backend:
    mem_limit: 1g
    memswap_limit: 1g
```

#### Logs Management

```bash
# Limit log file sizes (add to docker-compose.yml)
services:
  backend:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

## 🔐 Security Considerations

### Development Environment

- Uses default passwords (change for production)
- CORS allows localhost origins
- Debug mode enabled

### Production Environment

- **Always change default passwords**
- Use environment variables for secrets
- Enable SSL/HTTPS
- Configure proper CORS origins
- Disable debug mode
- Regular security updates

### Default Admin Credentials (Development)

After running `./docker-dev.sh setup-admin`:

- **admin1@legaldoc.com** / AdminPass123!
- **admin2@legaldoc.com** / AdminPass456!
- **admin3@legaldoc.com** / AdminPass789!
- **admin4@legaldoc.com** / AdminPass101!

**⚠️ Change these in production!**

## 📊 Monitoring

### View Real-time Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend

# With timestamps
docker-compose logs -f -t

# Last 100 lines
docker-compose logs --tail=100 -f
```

### Resource Monitoring

```bash
# Container resource usage
docker stats

# Detailed container info
docker-compose exec backend df -h
docker-compose exec backend free -h
docker-compose exec backend ps aux
```

## 🔄 Updates and Maintenance

### Update Application

```bash
# Pull latest code
git pull origin main

# Rebuild with latest changes
docker-compose build --no-cache

# Restart with new images
docker-compose down
docker-compose up -d
```

### Database Maintenance

```bash
# Run database optimizations
docker-compose exec db psql -U legaldoc_user -d legaldoc_db -c "VACUUM ANALYZE;"

# Update statistics
docker-compose exec db psql -U legaldoc_user -d legaldoc_db -c "SELECT maintain_database();"
```

## 💡 Development Tips

### Live Development

For active development with live reloading:

```bash
# Mount source code as volumes (add to docker-compose.yml)
services:
  backend:
    volumes:
      - ./backend:/app
      - /app/.venv  # Exclude virtual environment
  
  frontend:
    volumes:
      - ./my-app/src:/app/src
      - ./my-app/public:/app/public
```

### Debug Mode

```bash
# Start with debug output
docker-compose up

# Access container shell
docker-compose exec backend bash
docker-compose exec frontend sh

# Run commands inside container
docker-compose exec backend python -c "import sys; print(sys.path)"
```

### Testing

```bash
# Run backend tests
docker-compose exec backend python -m pytest

# Run frontend tests
docker-compose exec frontend npm test

# Run integration tests
docker-compose exec backend python -m pytest tests/integration/
```

## 📞 Support

If you encounter issues:

1. Check this README for troubleshooting steps
2. Check the application logs: `./docker-dev.sh logs`
3. Verify Docker is running: `docker info`
4. Try cleaning up: `./docker-dev.sh cleanup`
5. Rebuild from scratch: `docker-compose build --no-cache`

## 🎯 Next Steps

1. **Development**: Start with `./docker-dev.sh start`
2. **Setup Admins**: Run `./docker-dev.sh setup-admin`
3. **Access Application**: Visit http://localhost:3000
4. **View API Docs**: Visit http://localhost:8000/docs
5. **Upload Documents**: Test the file upload functionality
6. **Test Chat**: Try asking questions about legal documents

Happy coding! 🚀
