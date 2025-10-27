#!/bin/bash
# Pre-commit hooks setup script for CAD-RMB Currency Bot

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print functions
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

print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================${NC}"
}

# Check if pre-commit is installed
check_precommit() {
    if command -v pre-commit &> /dev/null; then
        print_success "Pre-commit is already installed"
        pre-commit --version
        return 0
    else
        print_warning "Pre-commit is not installed"
        return 1
    fi
}

# Install pre-commit
install_precommit() {
    print_status "Installing pre-commit..."

    if command -v pip3 &> /dev/null; then
        pip3 install pre-commit
    elif command -v pip &> /dev/null; then
        pip install pre-commit
    else
        print_error "Neither pip nor pip3 found. Please install Python pip first."
        exit 1
    fi

    if check_precommit; then
        print_success "Pre-commit installed successfully"
    else
        print_error "Failed to install pre-commit"
        exit 1
    fi
}

# Install pre-commit hooks
install_hooks() {
    print_status "Installing pre-commit hooks..."

    if [ ! -f ".pre-commit-config.yaml" ]; then
        print_error ".pre-commit-config.yaml not found!"
        exit 1
    fi

    pre-commit install
    print_success "Pre-commit hooks installed successfully"
}

# Update pre-commit hooks
update_hooks() {
    print_status "Updating pre-commit hooks..."
    pre-commit autoupdate
    print_success "Pre-commit hooks updated successfully"
}

# Run pre-commit on all files
run_all() {
    print_status "Running pre-commit hooks on all files..."
    pre-commit run --all-files
    print_success "Pre-commit checks completed"
}

# Run pre-commit on staged files only
run_staged() {
    print_status "Running pre-commit hooks on staged files..."
    pre-commit run
    print_success "Pre-commit checks completed"
}

# Clean pre-commit cache
clean_cache() {
    print_status "Cleaning pre-commit cache..."
    pre-commit clean
    print_success "Pre-commit cache cleaned"
}

# Uninstall pre-commit hooks
uninstall_hooks() {
    print_warning "This will remove pre-commit hooks from this repository"
    read -p "Are you sure? (y/N): " confirm

    if [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]]; then
        print_status "Uninstalling pre-commit hooks..."
        pre-commit uninstall
        print_success "Pre-commit hooks uninstalled"
    else
        print_status "Cancelled"
    fi
}

# Show pre-commit configuration
show_config() {
    print_status "Pre-commit configuration:"
    if [ -f ".pre-commit-config.yaml" ]; then
        cat .pre-commit-config.yaml
    else
        print_error ".pre-commit-config.yaml not found!"
    fi
}

# Show help
show_help() {
    echo "Pre-commit hooks setup script for CAD-RMB Currency Bot"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  install     Install pre-commit and hooks"
    echo "  update      Update pre-commit hooks to latest versions"
    echo "  run         Run pre-commit hooks on staged files"
    echo "  run-all     Run pre-commit hooks on all files"
    echo "  clean       Clean pre-commit cache"
    echo "  uninstall   Remove pre-commit hooks"
    echo "  config      Show pre-commit configuration"
    echo "  status      Check pre-commit installation status"
    echo "  help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 install    # Install pre-commit and setup hooks"
    echo "  $0 run        # Run hooks on staged files"
    echo "  $0 run-all    # Run hooks on all files"
}

# Main script logic
main() {
    print_header "CAD-RMB Currency Bot - Pre-commit Setup"

    case "${1:-help}" in
        install)
            if ! check_precommit; then
                install_precommit
            fi
            install_hooks
            print_success "Pre-commit setup complete!"
            echo ""
            print_status "Next steps:"
            echo "1. Stage your files: git add ."
            echo "2. Commit: git commit -m 'Your message'"
            echo "3. Pre-commit hooks will run automatically"
            ;;
        update)
            check_precommit || install_precommit
            update_hooks
            ;;
        run)
            check_precommit || install_precommit
            run_staged
            ;;
        run-all)
            check_precommit || install_precommit
            run_all
            ;;
        clean)
            check_precommit || install_precommit
            clean_cache
            ;;
        uninstall)
            check_precommit || install_precommit
            uninstall_hooks
            ;;
        config)
            show_config
            ;;
        status)
            if check_precommit; then
                print_status "Pre-commit hooks status:"
                pre-commit --version
                echo ""
                if [ -d ".git/hooks/pre-commit" ]; then
                    print_success "Pre-commit hooks are installed"
                else
                    print_warning "Pre-commit hooks are not installed"
                fi
            fi
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
}

# Run main function with all arguments
main "$@"
