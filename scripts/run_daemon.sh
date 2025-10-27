#!/bin/bash
# Currency Exchange Rate Monitor Daemon Management Script

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
DAEMON_SCRIPT="$PROJECT_DIR/currency_bot.py"
PID_FILE="$PROJECT_DIR/currency_daemon.pid"
LOG_FILE="$PROJECT_DIR/currency_daemon.log"

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

# Function to check if daemon is running
is_daemon_running() {
    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE")
        if ps -p "$pid" > /dev/null 2>&1; then
            return 0
        else
            rm -f "$PID_FILE"
            return 1
        fi
    else
        return 1
    fi
}

# Function to start daemon
start_daemon() {
    local interval=${1:-60}
    
    if is_daemon_running; then
        print_warning "Currency monitor daemon is already running (PID: $(cat "$PID_FILE"))"
        return 1
    fi
    
    print_status "Starting currency monitor daemon with ${interval}-minute intervals..."
    
    # Set environment variables
    export CAD_RMB_MONITORING_INTERVAL="$interval"
    
    # Start daemon in background
    nohup python3 "$DAEMON_SCRIPT" > "$LOG_FILE" 2>&1 &
    local pid=$!
    
    # Save PID
    echo "$pid" > "$PID_FILE"
    
    # Wait a moment and check if it's still running
    sleep 2
    if is_daemon_running; then
        print_success "Currency monitor daemon started successfully (PID: $pid)"
        print_status "Monitoring RMB-CAD exchange rate every $interval minutes"
        print_status "Log file: $LOG_FILE"
        print_status "PID file: $PID_FILE"
        return 0
    else
        print_error "Failed to start currency monitor daemon"
        rm -f "$PID_FILE"
        return 1
    fi
}

# Function to stop daemon
stop_daemon() {
    if ! is_daemon_running; then
        print_warning "Currency monitor daemon is not running"
        return 1
    fi
    
    local pid=$(cat "$PID_FILE")
    print_status "Stopping currency monitor daemon (PID: $pid)..."
    
    # Try graceful termination first
    kill "$pid"
    
    # Wait for graceful shutdown
    local count=0
    while [ $count -lt 10 ] && is_daemon_running; do
        sleep 1
        count=$((count + 1))
    done
    
    # Force kill if still running
    if is_daemon_running; then
        print_warning "Graceful shutdown failed, forcing termination..."
        kill -9 "$pid"
        sleep 1
    fi
    
    if ! is_daemon_running; then
        print_success "Currency monitor daemon stopped successfully"
        rm -f "$PID_FILE"
        return 0
    else
        print_error "Failed to stop currency monitor daemon"
        return 1
    fi
}

# Function to restart daemon
restart_daemon() {
    local interval=${1:-60}
    print_status "Restarting currency monitor daemon..."
    stop_daemon
    sleep 2
    start_daemon "$interval"
}

# Function to show daemon status
show_status() {
    print_status "Currency Exchange Rate Monitor Daemon Status"
    echo "=================================================="
    
    if is_daemon_running; then
        local pid=$(cat "$PID_FILE")
        print_success "Status: RUNNING (PID: $pid)"
        
        # Show process info
        echo ""
        print_status "Process Information:"
        ps -p "$pid" -o pid,ppid,cmd,etime,pcpu,pmem
        
        # Show configuration
        echo ""
        print_status "Configuration:"
        echo "  Monitoring Interval: ${CAD_RMB_MONITORING_INTERVAL:-60} minutes"
        echo "  Threshold: ${CAD_RMB_THRESHOLD:-5.05}"
        echo "  Log File: $LOG_FILE"
        echo "  PID File: $PID_FILE"
        
        # Show recent log entries
        if [ -f "$LOG_FILE" ]; then
            echo ""
            print_status "Recent Log Entries (last 10 lines):"
            echo "----------------------------------------"
            tail -n 10 "$LOG_FILE"
        fi
    else
        print_error "Status: NOT RUNNING"
        echo ""
        print_status "To start the daemon, run:"
        echo "  $0 start [interval_minutes]"
        echo ""
        print_status "Example:"
        echo "  $0 start 60    # Monitor every 60 minutes"
        echo "  $0 start 30    # Monitor every 30 minutes"
    fi
}

# Function to show logs
show_logs() {
    if [ -f "$LOG_FILE" ]; then
        print_status "Showing currency monitor daemon logs..."
        echo "=============================================="
        tail -f "$LOG_FILE"
    else
        print_error "Log file not found: $LOG_FILE"
        print_status "The daemon may not have been started yet."
    fi
}

# Function to show help
show_help() {
    echo "Currency Exchange Rate Monitor Daemon Management"
    echo "================================================"
    echo ""
    echo "Usage: $0 <command> [options]"
    echo ""
    echo "Commands:"
    echo "  start [interval]  Start the daemon (interval in minutes, default: 60)"
    echo "  stop              Stop the daemon"
    echo "  restart [interval] Restart the daemon (interval in minutes, default: 60)"
    echo "  status            Show daemon status and configuration"
    echo "  logs              Show and follow daemon logs"
    echo "  help              Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 start          # Start with default 60-minute intervals"
    echo "  $0 start 30       # Start with 30-minute intervals"
    echo "  $0 stop           # Stop the daemon"
    echo "  $0 restart 120    # Restart with 120-minute intervals"
    echo "  $0 status         # Check daemon status"
    echo "  $0 logs           # View live logs"
    echo ""
    echo "Environment Variables:"
    echo "  CAD_RMB_MONITORING_INTERVAL  Monitoring interval in minutes"
    echo "  CAD_RMB_THRESHOLD            Exchange rate threshold (default: 5.05)"
    echo "  CAD_RMB_LOG_FILE             Log file path"
    echo "  CAD_RMB_LOG_LEVEL            Log level (DEBUG, INFO, WARNING, ERROR)"
    echo ""
    echo "Configuration:"
    echo "  Copy env.example to .env and configure your settings"
    echo "  Set up email credentials for notifications"
    echo "  Configure exchange rate threshold"
}

# Main script logic
case "${1:-help}" in
    start)
        start_daemon "$2"
        ;;
    stop)
        stop_daemon
        ;;
    restart)
        restart_daemon "$2"
        ;;
    status)
        show_status
        ;;
    logs)
        show_logs
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
