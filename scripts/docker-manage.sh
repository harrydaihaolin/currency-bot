#!/bin/bash
# Currency Exchange Rate Monitor Docker Management Script

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

print_error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
}

# Function to check if .env file exists
check_env_file() {
    if [ ! -f "$PROJECT_DIR/.env" ]; then
        print_warning ".env file not found. Creating from env.example..."
        cp "$PROJECT_DIR/env.example" "$PROJECT_DIR/.env"
        print_warning "Please edit .env file with your configuration before starting the container."
        return 1
    fi
    return 0
}

# Function to start container
start_container() {
    check_docker
    
    if ! check_env_file; then
        print_error "Please configure .env file first"
        exit 1
    fi
    
    print_status "Starting Currency Exchange Rate Monitor container..."
    
    cd "$PROJECT_DIR"
    docker-compose up -d
    
    if [ $? -eq 0 ]; then
        print_success "Container started successfully"
        print_status "Container name: currency-monitor"
        print_status "To view logs: $0 logs"
        print_status "To check status: $0 status"
    else
        print_error "Failed to start container"
        exit 1
    fi
}

# Function to stop container
stop_container() {
    check_docker
    
    print_status "Stopping Currency Exchange Rate Monitor container..."
    
    cd "$PROJECT_DIR"
    docker-compose down
    
    if [ $? -eq 0 ]; then
        print_success "Container stopped successfully"
    else
        print_error "Failed to stop container"
        exit 1
    fi
}

# Function to restart container
restart_container() {
    print_status "Restarting Currency Exchange Rate Monitor container..."
    stop_container
    sleep 2
    start_container
}

# Function to show container status
show_status() {
    check_docker
    
    print_status "Currency Exchange Rate Monitor Container Status"
    echo "====================================================="
    
    cd "$PROJECT_DIR"
    
    # Check if container is running
    if docker-compose ps | grep -q "Up"; then
        print_success "Status: RUNNING"
        echo ""
        print_status "Container Information:"
        docker-compose ps
        echo ""
        print_status "Resource Usage:"
        docker stats --no-stream currency-monitor
    else
        print_error "Status: NOT RUNNING"
        echo ""
        print_status "To start the container, run:"
        echo "  $0 start"
    fi
}

# Function to show logs
show_logs() {
    check_docker
    
    print_status "Showing Currency Exchange Rate Monitor container logs..."
    echo "============================================================="
    
    cd "$PROJECT_DIR"
    docker-compose logs -f
}

# Function to build container
build_container() {
    check_docker
    
    print_status "Building Currency Exchange Rate Monitor container..."
    
    cd "$PROJECT_DIR"
    docker-compose build --no-cache
    
    if [ $? -eq 0 ]; then
        print_success "Container built successfully"
    else
        print_error "Failed to build container"
        exit 1
    fi
}

# Function to show help
show_help() {
    echo "Currency Exchange Rate Monitor Docker Management"
    echo "==============================================="
    echo ""
    echo "Usage: $0 <command>"
    echo ""
    echo "Commands:"
    echo "  start     Start the container"
    echo "  stop      Stop the container"
    echo "  restart   Restart the container"
    echo "  status    Show container status"
    echo "  logs      Show and follow container logs"
    echo "  build     Build the container image"
    echo "  help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 start     # Start the container"
    echo "  $0 stop      # Stop the container"
    echo "  $0 restart   # Restart the container"
    echo "  $0 status    # Check container status"
    echo "  $0 logs      # View live logs"
    echo "  $0 build     # Rebuild container image"
    echo ""
    echo "Configuration:"
    echo "  Copy env.example to .env and configure your settings"
    echo "  Set up email credentials for notifications"
    echo "  Configure exchange rate threshold"
    echo ""
    echo "Environment Variables (in .env file):"
    echo "  RMB_CAD_MONITORING_INTERVAL  Monitoring interval in minutes"
    echo "  RMB_CAD_THRESHOLD            Exchange rate threshold (default: 5.05)"
    echo "  CURRENCY_NOTIFICATION_EMAIL  Email to send notifications from"
    echo "  CURRENCY_GMAIL_APP_PASSWORD Gmail App Password"
    echo "  CURRENCY_RECIPIENT_EMAILS    Comma-separated recipient emails"
}

# Main script logic
case "${1:-help}" in
    start)
        start_container
        ;;
    stop)
        stop_container
        ;;
    restart)
        restart_container
        ;;
    status)
        show_status
        ;;
    logs)
        show_logs
        ;;
    build)
        build_container
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
