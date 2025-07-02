# MDMSGA Quick Start Guide

Get MDMSGA running in minutes with this quick start guide.

## Option 1: Using Docker (Recommended)

### Prerequisites

- Docker and Docker Compose installed
- Git

### Steps

1. **Clone and setup**

   ```bash
   git clone <repository-url>
   cd mdmsga
   cp env.example .env
   ```

2. **Start services**

   ```bash
   docker-compose up -d
   ```

3. **Initialize database**

   ```bash
   docker-compose exec api alembic upgrade head
   ```

4. **Create superuser**

   ```bash
   docker-compose exec api python -m mdmsga.cli create-superuser
   ```

5. **Access the application**
   - Web Interface: http://localhost:8000
   - Dashboard: http://localhost:8000/dashboard
   - API: http://localhost:8000/api/v1
   - API Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Option 2: Local Development

### Prerequisites

- Python 3.11+
- PostgreSQL 14+
- Valkey 7+ (Redis-compatible)
- uv (Astral package manager)

### Steps

1. **Run setup script**

   ```bash
   ./setup.sh
   ```

2. **Configure environment**

   ```bash
   # Edit .env file with your database credentials
   nano .env
   ```

3. **Start PostgreSQL and Valkey**

   ```bash
   # Using Docker for databases only
   docker-compose up -d postgres valkey

   # Or install locally
   # sudo apt-get install postgresql
   # Valkey: https://valkey.io/docs/getting-started/installation/
   ```

4. **Initialize database**

   ```bash
   alembic upgrade head
   ```

5. **Create superuser**

   ```bash
   python -m mdmsga.cli create-superuser
   ```

6. **Start development server**

   ```bash
   uvicorn mdmsga.main:app --reload
   ```

7. **Access the application**

   - Web Interface: http://localhost:8000
   - Dashboard: http://localhost:8000/dashboard
   - API: http://localhost:8000/api/v1
   - API Docs: http://localhost:8000/docs

8. **Start Celery workers (optional)**

   ```bash
   # Terminal 1: Celery worker
   celery -A mdmsga.celery_app worker --loglevel=info

   # Terminal 2: Celery beat (scheduler)
   celery -A mdmsga.celery_app beat --loglevel=info
   ```

## Web Interface

MDMSGA includes a modern HTMX-based web interface that works on desktop and mobile devices.

### Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Progressive Web App**: Can be installed on mobile devices
- **Offline Support**: Basic functionality works without internet
- **Real-time Updates**: HTMX provides dynamic content updates
- **Touch-friendly**: Optimized for touch interactions

### Access Points

- **Dashboard**: http://localhost:8000/dashboard
- **Inventory**: http://localhost:8000/inventory
- **Customers**: http://localhost:8000/customers
- **Sales**: http://localhost:8000/sales
- **Service**: http://localhost:8000/service

## API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Authentication

1. **Register a user**

   ```bash
   curl -X POST "http://localhost:8000/api/v1/auth/register" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "admin@mdmsga.com",
       "password": "password123",
       "first_name": "Admin",
       "last_name": "User"
     }'
   ```

2. **Login to get token**

   ```bash
   curl -X POST "http://localhost:8000/api/v1/auth/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin@mdmsga.com&password=password123"
   ```

3. **Use token in requests**
   ```bash
   curl -X GET "http://localhost:8000/api/v1/users/me" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
   ```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=mdmsga

# Run specific test
pytest tests/test_auth.py -v
```

## Development Commands

```bash
# Format and lint code
ruff check --fix mdmsga tests

# Format code only
ruff format mdmsga tests

# Type checking
mypy mdmsga

# Run pre-commit hooks
pre-commit run --all-files
```

## Project Structure

```
mdmsga/
├── mdmsga/                    # Main application
│   ├── api/                # API endpoints
│   ├── core/               # Core configuration
│   ├── models/             # Database models
│   ├── schemas/            # Pydantic schemas
│   ├── crud/               # Database operations
│   └── services/           # Business logic
├── tests/                  # Test suite
├── docker/                 # Docker configuration
├── alembic/               # Database migrations
└── uploads/               # File uploads
```

## Troubleshooting

### Common Issues

1. **Database connection error**

   - Check PostgreSQL is running
   - Verify database credentials in `.env`
   - Ensure database exists

2. **Valkey connection error**

   - Check Valkey is running
   - Verify Valkey configuration in `.env`

3. **Import errors**

   - Ensure virtual environment is activated
   - Run `uv sync` to install dependencies

4. **Permission errors**
   - Check file permissions
   - Ensure uploads directory exists

### Getting Help

- Check the logs: `docker-compose logs api`
- Review the documentation
- Create an issue in the repository

## Next Steps

1. **Explore the API**: Visit http://localhost:8000/docs
2. **Create test data**: Use the API to create dealerships, vehicles, customers
3. **Build frontend**: Start developing the React frontend
4. **Add features**: Implement additional DMS modules
5. **Deploy**: Set up production deployment

Happy coding!
