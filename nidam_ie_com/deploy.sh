#!/bin/bash
#
# Deployment script for nidam-ie-com
#

# Exit on error
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root (optional)
check_root() {
    if [[ $EUID -eq 0 ]]; then
        print_warning "Running as root. This is not recommended for development."
    fi
}

# Check Python version
check_python() {
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed. Please install Python 3.8 or higher."
        exit 1
    fi

    PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    MAJOR_VERSION=$(echo $PYTHON_VERSION | cut -d. -f1)
    MINOR_VERSION=$(echo $PYTHON_VERSION | cut -d. -f2)

    if [[ $MAJOR_VERSION -lt 3 ]] || [[ $MAJOR_VERSION -eq 3 && $MINOR_VERSION -lt 8 ]]; then
        print_error "Python 3.8 or higher is required. Current version: $PYTHON_VERSION"
        exit 1
    fi

    print_status "Python version: $PYTHON_VERSION"
}

# Create virtual environment
create_virtualenv() {
    if [[ -d "venv" ]]; then
        print_warning "Virtual environment already exists. Skipping creation."
    else
        print_status "Creating virtual environment..."
        python3 -m venv venv
        print_status "Virtual environment created successfully."
    fi

    # Activate virtual environment
    source venv/bin/activate
    print_status "Virtual environment activated."
}

# Install dependencies
install_dependencies() {
    print_status "Installing dependencies..."

    if [[ ! -f "requirements.txt" ]]; then
        print_error "requirements.txt not found!"
        exit 1
    fi

    pip install -r requirements.txt
    print_status "Dependencies installed successfully."
}

# Initialize database
initialize_database() {
    print_status "Initializing database..."

    if [[ ! -f "init_db.py" ]]; then
        print_error "init_db.py not found!"
        exit 1
    fi

    python init_db.py
    print_status "Database initialized successfully."
}

# Setup production environment
setup_production() {
    print_status "Setting up production environment..."

    # Create logs directory
    mkdir -p logs

    # Generate a secure secret key
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")

    # Update .env file with production settings
    if [[ -f ".env" ]]; then
        cp .env .env.backup
        sed -i "s/SECRET_KEY=.*/SECRET_KEY=$SECRET_KEY/" .env
        sed -i "s/FLASK_ENV=.*/FLASK_ENV=production/" .env
        print_status "Environment file updated for production."
    else
        print_warning ".env file not found. Creating a new one."
        cat > .env << EOF
SECRET_KEY=$SECRET_KEY
FLASK_ENV=production
DATABASE_URL=sqlite:///nidam_ie_com.db
EOF
        print_status "Created new .env file."
    fi

    print_status "Production environment setup completed."
}

# Start development server
start_development() {
    print_status "Starting development server..."
    python app.py
}

# Show help
show_help() {
    echo "Nidam IE Commerce Deployment Script"
    echo ""
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  setup     Setup development environment (default)"
    echo "  production Setup production environment"
    echo "  run       Start development server"
    echo "  help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0              # Setup development environment"
    echo "  $0 production   # Setup production environment"
    echo "  $0 run          # Start development server"
}

# Main function
main() {
    case "$1" in
        setup|"")
            check_root
            check_python
            create_virtualenv
            install_dependencies
            initialize_database
            print_status "Setup completed successfully! You can now run the application with: $0 run"
            ;;
        production)
            check_root
            check_python
            create_virtualenv
            install_dependencies
            initialize_database
            setup_production
            print_status "Production setup completed successfully!"
            ;;
        run)
            source venv/bin/activate
            start_development
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"