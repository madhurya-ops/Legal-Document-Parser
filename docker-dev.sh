#!/bin/bash

# LegalDoc Docker Development Management Script
# This script helps manage the Docker development environment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info >/dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker Desktop."
        exit 1
    fi
}

# Function to create necessary directories
create_directories() {
    print_status "Creating necessary directories..."
    mkdir -p backend/vector_store
    mkdir -p backend/uploads
    mkdir -p backend/logs
    mkdir -p nginx/ssl
    print_success "Directories created successfully"
}

# Function to build all services
build_services() {
    print_status "Building Docker services..."
    docker-compose build --no-cache
    print_success "All services built successfully"
}

# Function to start development environment
start_dev() {
    print_status "Starting LegalDoc development environment..."
    
    create_directories
    
    # Start services
    docker-compose up -d
    
    # Wait for services to be ready
    print_status "Waiting for services to be ready..."
    sleep 10
    
    # Check service health
    print_status "Checking service health..."
    
    # Check database
    if docker-compose exec -T db pg_isready -U legaldoc_user -d legaldoc_db >/dev/null 2>&1; then
        print_success "Database is ready"
    else
        print_warning "Database is still starting up..."
    fi
    
    # Check backend
    if curl -f http://localhost:8000/health >/dev/null 2>&1; then
        print_success "Backend is ready"
    else
        print_warning "Backend is still starting up..."
    fi
    
    # Check frontend
    if curl -f http://localhost:3000 >/dev/null 2>&1; then
        print_success "Frontend is ready"
    else
        print_warning "Frontend is still starting up..."
    fi
    
    print_success "Development environment started!"
    print_status "Frontend: http://localhost:3000"
    print_status "Backend API: http://localhost:8000"
    print_status "API Docs: http://localhost:8000/docs"
    print_status "Database: localhost:5432"
    print_status "Redis: localhost:6379"
}

# Function to stop development environment
stop_dev() {
    print_status "Stopping LegalDoc development environment..."
    docker-compose down
    print_success "Development environment stopped"
}

# Function to restart development environment
restart_dev() {
    print_status "Restarting LegalDoc development environment..."
    docker-compose restart
    print_success "Development environment restarted"
}

# Function to view logs
view_logs() {
    if [ -z "$1" ]; then
        print_status "Showing logs for all services..."
        docker-compose logs -f
    else
        print_status "Showing logs for $1..."
        docker-compose logs -f "$1"
    fi
}

# Function to run setup admin script
setup_admin() {
    print_status "Setting up admin users..."
    docker-compose exec backend python setup_admin.py
    print_success "Admin users setup completed"
}

# Function to run database migrations
migrate_db() {
    print_status "Running database migrations..."
    docker-compose exec backend python migrate_database.py
    print_success "Database migrations completed"
}

# Function to clean up Docker resources
cleanup() {
    print_status "Cleaning up Docker resources..."
    docker-compose down -v --remove-orphans
    docker system prune -f
    print_success "Cleanup completed"
}

# Function to show service status
status() {
    print_status "Docker service status:"
    docker-compose ps
    
    print_status "\nContainer health status:"
    docker-compose exec db pg_isready -U legaldoc_user -d legaldoc_db 2>/dev/null && echo "✅ Database: Healthy" || echo "❌ Database: Unhealthy"
    curl -f http://localhost:8000/health 2>/dev/null && echo "✅ Backend: Healthy" || echo "❌ Backend: Unhealthy"
    curl -f http://localhost:3000 2>/dev/null && echo "✅ Frontend: Healthy" || echo "❌ Frontend: Unhealthy"
}

# Function to show help
show_help() {
    echo "LegalDoc Docker Development Management Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  start       Start the development environment"
    echo "  stop        Stop the development environment"
    echo "  restart     Restart the development environment"
    echo "  build       Build all Docker services"
    echo "  logs [service]   View logs (all services or specific service)"
    echo "  status      Show service status"
    echo "  setup-admin Setup admin users"
    echo "  migrate     Run database migrations"
    echo "  cleanup     Clean up Docker resources"
    echo "  help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 start                 # Start development environment"
    echo "  $0 logs backend          # View backend logs"
    echo "  $0 logs                  # View all logs"
    echo "  $0 setup-admin           # Setup admin users"
}

# Main script logic
case "$1" in
    start)
        check_docker
        start_dev
        ;;
    stop)
        check_docker
        stop_dev
        ;;
    restart)
        check_docker
        restart_dev
        ;;
    build)
        check_docker
        build_services
        ;;
    logs)
        check_docker
        view_logs "$2"
        ;;
    status)
        check_docker
        status
        ;;
    setup-admin)
        check_docker
        setup_admin
        ;;
    migrate)
        check_docker
        migrate_db
        ;;
    cleanup)
        check_docker
        cleanup
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        if [ -z "$1" ]; then
            show_help
        else
            print_error "Unknown command: $1"
            show_help
            exit 1
        fi
        ;;
esac
