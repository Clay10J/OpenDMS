# OpenDMS - Modern Dealer Management System

A next-generation Dealer Management System designed to compete with CDK Global, built with modern Python technologies and cloud-native architecture.

## Features

### Core Modules

- **Dealership Management** - Multi-location support, user roles, permissions
- **Inventory Management** - Vehicle tracking, pricing, availability
- **Customer Relationship Management (CRM)** - Lead management, customer profiles
- **Sales Management** - Deal structuring, financing, document management
- **Service Management** - Service scheduling, work orders, parts inventory
- **Financial Management** - Accounting, reporting, analytics
- **Integration Hub** - Third-party integrations (DMS, lenders, manufacturers)
- **Mobile App** - Field service, sales, management access

### Key Advantages

- **Modern Cloud-Native Architecture** - Scalable, secure, always available
- **AI-Powered Insights** - Predictive analytics, automated workflows
- **Real-time Collaboration** - Live updates across all modules
- **Open API Ecosystem** - Easy third-party integrations
- **Mobile-First Design** - Responsive web + native mobile apps

## Tech Stack

### Backend

- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL + Valkey
- **ORM**: SQLAlchemy with Alembic migrations
- **Authentication**: JWT with bcrypt
- **Background Tasks**: Celery
- **Package Manager**: uv (Astral)
- **Linting/Formatting**: Ruff

### Frontend (Coming Soon)

- **Web App**: React with TypeScript, Next.js
- **Mobile**: React Native
- **UI Framework**: Tailwind CSS + Headless UI

### Infrastructure

- **Cloud**: AWS/GCP ready
- **Containerization**: Docker + Kubernetes
- **CI/CD**: GitHub Actions
- **Monitoring**: DataDog/New Relic ready

## Installation

### Prerequisites

- Python 3.11 or higher
- PostgreSQL 14+
- Valkey 7+ (Redis-compatible)
- uv (Astral package manager)

### Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Setup Project

```bash
# Clone the repository
git clone <repository-url>
cd opendms

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv sync

# Install development dependencies
uv sync --group dev
```

### Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
# Database URLs, Redis URL, JWT secrets, etc.
```

### Database Setup

```bash
# Run database migrations
alembic upgrade head

# Create initial superuser
python -m opendms.cli create-superuser
```

## Running the Application

### Development Server

```bash
# Start the FastAPI development server
uvicorn opendms.main:app --reload --host 0.0.0.0 --port 8000

# Start Celery worker (in another terminal)
celery -A opendms.celery_app worker --loglevel=info

# Start Celery beat for scheduled tasks (in another terminal)
celery -A opendms.celery_app beat --loglevel=info
```

### Production

```bash
# Using Gunicorn
gunicorn opendms.main:app -w 4 -k uvicorn.workers.UvicornWorker

# Using Docker
docker-compose up -d
```

### Docker Security

⚠️ **Important Security Notes for Docker:**

1. **Environment Variables**: The docker-compose.yml uses environment variables with fallback values. For production:

   ```bash
   # Set secure environment variables before running
   export POSTGRES_PASSWORD="your-secure-password"
   export SECRET_KEY="your-secure-secret-key"
   docker-compose up -d
   ```

2. **Never commit real passwords**: The docker-compose.yml contains default/development values that are safe to commit, but you should override them in production.

3. **Use Docker secrets**: For production deployments, consider using Docker secrets or external secret management systems.

4. **Network security**: The default setup exposes database ports (5432, 6379) for development. In production, remove these port mappings and use internal networking only.

5. **Development vs Production**: The application uses `DEBUG=true` and allows all hosts in development mode. Ensure these are properly configured for production:
   ```bash
   # Production environment variables
   export DEBUG=false
   export BACKEND_CORS_ORIGINS="https://yourdomain.com,https://api.yourdomain.com"
   ```

## API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=opendms

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v
```

## Development

### Code Quality

```bash
# Format and lint code
ruff check --fix opendms tests

# Format code only
ruff format opendms tests

# Type checking
mypy opendms
```

### Pre-commit Hooks

```bash
# Install pre-commit hooks
pre-commit install

# Run all hooks
pre-commit run --all-files
```

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## Project Structure

```
opendms/
├── opendms/                    # Main application package
│   ├── api/                # API routes and endpoints
│   │   ├── v1/            # API version 1
│   │   └── deps.py        # Dependencies and middleware
│   ├── core/              # Core configuration and utilities
│   │   ├── config.py      # Settings and configuration
│   │   ├── security.py    # Authentication and security
│   │   └── database.py    # Database connection and session
│   ├── models/            # SQLAlchemy models
│   ├── schemas/           # Pydantic schemas
│   ├── services/          # Business logic services
│   ├── crud/              # Database CRUD operations
│   ├── cli/               # Command line tools
│   └── main.py           # FastAPI application entry point
├── tests/                 # Test suite
├── alembic/              # Database migrations
├── docker/               # Docker configuration
├── scripts/              # Utility scripts
├── pyproject.toml        # Project configuration
├── .env.example          # Environment variables template
└── README.md            # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support and questions:

- Create an issue in the GitHub repository
- Contact the development team
- Check the documentation at `/docs`

## Roadmap

- [ ] Core DMS modules implementation
- [ ] Frontend React application
- [ ] Mobile app (React Native)
- [ ] AI-powered analytics
- [ ] Third-party integrations
- [ ] Advanced reporting
- [ ] Multi-tenant architecture
- [ ] Performance optimization
- [ ] Security hardening
- [ ] Production deployment guides
