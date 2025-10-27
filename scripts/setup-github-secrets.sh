#!/bin/bash

# GitHub Actions Credential Setup Helper for Currency Bot
# This script helps you set up credentials for automated currency monitoring

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

# Function to check if GitHub CLI is installed
check_gh_cli() {
    if ! command -v gh &> /dev/null; then
        print_error "GitHub CLI (gh) is not installed!"
        print_status "Please install it first:"
        print_status "  macOS: brew install gh"
        print_status "  Ubuntu: sudo apt install gh"
        print_status "  Windows: winget install GitHub.cli"
        exit 1
    fi
    print_success "GitHub CLI is installed"
}

# Function to check if user is authenticated
check_gh_auth() {
    if ! gh auth status &> /dev/null; then
        print_error "Not authenticated with GitHub!"
        print_status "Please run: gh auth login"
        exit 1
    fi
    print_success "Authenticated with GitHub"
}

# Function to get repository name
get_repo_name() {
    if [ -d ".git" ]; then
        REPO_NAME=$(git remote get-url origin | sed 's/.*github.com[:/]\([^.]*\).*/\1/')
        print_success "Detected repository: $REPO_NAME"
    else
        print_error "Not in a Git repository!"
        exit 1
    fi
}

# Function to prompt for credentials
prompt_credentials() {
    print_status "Setting up credentials for automated currency monitoring..."
    echo ""
    
    # Currency Bot Credentials
    print_status "=== CAD-RMB Currency Bot Credentials ==="
    read -p "Currency Notification Email (Gmail): " CURRENCY_NOTIFICATION_EMAIL
    read -s -p "Gmail App Password: " CURRENCY_GMAIL_APP_PASSWORD
    echo ""
    read -p "Recipient Emails (comma-separated): " CURRENCY_RECIPIENT_EMAILS
    read -p "CAD-RMB Threshold (default: 5.05): " CAD_RMB_THRESHOLD
    
    # Set defaults
    if [ -z "$CURRENCY_RECIPIENT_EMAILS" ]; then
        CURRENCY_RECIPIENT_EMAILS="$CURRENCY_NOTIFICATION_EMAIL"
    fi
    
    if [ -z "$CAD_RMB_THRESHOLD" ]; then
        CAD_RMB_THRESHOLD="5.05"
    fi
    
    echo ""
    print_status "=== Optional Exchange Rate API Configuration ==="
    read -p "Exchange Rate API Key (optional): " EXCHANGE_API_KEY
}

# Function to set secrets
set_secrets() {
    print_status "Setting GitHub Secrets..."
    
    # Currency Bot Secrets
    gh secret set CURRENCY_NOTIFICATION_EMAIL --body "$CURRENCY_NOTIFICATION_EMAIL"
    gh secret set CURRENCY_GMAIL_APP_PASSWORD --body "$CURRENCY_GMAIL_APP_PASSWORD"
    gh secret set CURRENCY_RECIPIENT_EMAILS --body "$CURRENCY_RECIPIENT_EMAILS"
    gh secret set CAD_RMB_THRESHOLD --body "$CAD_RMB_THRESHOLD"
    
    # Optional API Key
    if [ ! -z "$EXCHANGE_API_KEY" ]; then
        gh secret set EXCHANGE_API_KEY --body "$EXCHANGE_API_KEY"
    fi
    
    print_success "All secrets set successfully!"
}

# Function to verify secrets
verify_secrets() {
    print_status "Verifying secrets..."
    
    # List all secrets
    gh secret list
    
    print_success "Secrets verification complete!"
}

# Function to test workflow
test_workflow() {
    print_status "Testing periodic currency monitoring workflow..."
    
    # Trigger the workflow
    gh workflow run periodic-monitoring.yml
    
    print_success "Workflow triggered! Check the Actions tab for results."
    print_status "You can monitor progress with: gh run list"
}

# Function to show current secrets
show_secrets() {
    print_status "Current GitHub Secrets:"
    gh secret list
}

# Function to delete secrets
delete_secrets() {
    print_warning "This will delete all currency bot secrets!"
    read -p "Are you sure? (y/N): " confirm
    
    if [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]]; then
        print_status "Deleting secrets..."
        
        gh secret delete CURRENCY_NOTIFICATION_EMAIL --confirm
        gh secret delete CURRENCY_GMAIL_APP_PASSWORD --confirm
        gh secret delete CURRENCY_RECIPIENT_EMAILS --confirm
        gh secret delete CAD_RMB_THRESHOLD --confirm
        
        # Try to delete optional secrets (may not exist)
        gh secret delete EXCHANGE_API_KEY --confirm 2>/dev/null || true
        
        print_success "Secrets deleted successfully!"
    else
        print_status "Operation cancelled."
    fi
}

# Function to show help
show_help() {
    echo "GitHub Actions Credential Setup Helper for Currency Bot"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  setup     Interactive setup of all credentials"
    echo "  verify    Verify that secrets are properly set"
    echo "  test      Test the periodic monitoring workflow"
    echo "  list      List all current secrets"
    echo "  delete    Delete all currency bot secrets"
    echo "  help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 setup"
    echo "  $0 verify"
    echo "  $0 test"
    echo "  $0 list"
    echo ""
    echo "Required Secrets:"
    echo "  CURRENCY_NOTIFICATION_EMAIL    - Gmail address for sending notifications"
    echo "  CURRENCY_GMAIL_APP_PASSWORD    - Gmail App Password (not regular password)"
    echo "  CURRENCY_RECIPIENT_EMAILS      - Comma-separated list of recipient emails"
    echo "  CAD_RMB_THRESHOLD              - Exchange rate threshold (default: 5.05)"
    echo ""
    echo "Optional Secrets:"
    echo "  EXCHANGE_API_KEY               - API key for exchangerate-api.com"
}

# Main script logic
case "${1:-help}" in
    setup)
        check_gh_cli
        check_gh_auth
        get_repo_name
        prompt_credentials
        set_secrets
        verify_secrets
        print_success "Setup complete! Your credentials are now securely stored in GitHub Secrets."
        print_status "You can now run: $0 test"
        ;;
    verify)
        check_gh_cli
        check_gh_auth
        verify_secrets
        ;;
    test)
        check_gh_cli
        check_gh_auth
        test_workflow
        ;;
    list)
        check_gh_cli
        check_gh_auth
        show_secrets
        ;;
    delete)
        check_gh_cli
        check_gh_auth
        delete_secrets
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        show_help
        exit 1
        ;;
esac
