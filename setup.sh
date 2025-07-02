#!/bin/bash

# XDMS Setup Script
# This script sets up the XDMS project with uv package manager

set -e

echo "Setting up XDMS - Modern Dealer Management System"
echo "=================================================="

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "uv is not installed. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    echo "uv installed successfully"
else
    echo "uv is already installed"
fi

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.11"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "Python $required_version or higher is required. Current version: $python_version"
    exit 1
else
    echo "Python version $python_version is compatible"
fi

# Create virtual environment and install dependencies
echo "Creating virtual environment and installing dependencies..."
uv venv
source .venv/bin/activate

echo "Installing project dependencies..."
uv sync

echo "Installing development dependencies..."
uv sync --group dev

# Create .env file from template
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp env.example .env
    echo ".env file created. Please edit it with your configuration."
else
    echo ".env file already exists"
fi

# Create uploads directory
echo "Creating uploads directory..."
mkdir -p uploads

# Initialize git repository if not already done
if [ ! -d .git ]; then
    echo "Initializing git repository..."
    git init
    echo "Git repository initialized"
fi

# Create pre-commit hooks
echo "Setting up pre-commit hooks..."
uv run pre-commit install

echo ""
echo "XDMS setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your database and other configuration"
echo "2. Set up PostgreSQL database"
echo "3. Set up Valkey server (Redis-compatible)"
echo "4. Run database migrations: alembic upgrade head"
echo "5. Create superuser: python -m xdms.cli create-superuser"
echo "6. Start development server: uvicorn xdms.main:app --reload"
echo ""
echo "Documentation:"
echo "- API docs: http://localhost:8000/docs"
echo "- ReDoc: http://localhost:8000/redoc"
echo ""
echo "Happy coding!" 