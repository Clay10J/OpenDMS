# MDMSGA System Notes

Internal technical documentation for the MDMSGA (Dealer Management System) project.

## Architecture Overview

MDMSGA is a modern DMS built to compete with CDK Global using Python/FastAPI stack.

### Core Stack

- **Backend**: Python 3.11+ with FastAPI
- **Frontend**: HTMX + Jinja2 templates + Tailwind CSS
- **Database**: PostgreSQL 15+ (primary) + Valkey 7+ (cache/queue)
- **Package Manager**: uv (Astral) - 10-100x faster than pip
- **Linting/Formatting**: Ruff (replaces black, isort, flake8)
- **Containerization**: Docker + Docker Compose

## Package Dependencies

### Core Dependencies (pyproject.toml)

#### Web Framework

- `fastapi>=0.104.0` - Modern async web framework
- `uvicorn[standard]>=0.24.0` - ASGI server
- `python-multipart>=0.0.6` - File upload handling

#### Database

- `sqlalchemy>=2.0.0` - ORM with type safety
- `alembic>=1.12.0` - Database migrations
- `psycopg2-binary>=2.9.0` - PostgreSQL adapter
- `redis>=5.0.0` - Redis client (works with Valkey)

#### Authentication & Security

- `python-jose[cryptography]>=3.3.0` - JWT handling
- `passlib[bcrypt]>=1.7.4` - Password hashing
- `email-validator>=2.1.0` - Email validation

#### Background Tasks

- `celery>=5.3.0` - Task queue (uses Valkey as broker)

#### Data Processing

- `pydantic>=2.5.0` - Data validation/serialization
- `pydantic-settings>=2.1.0` - Settings management

#### HTTP Clients

- `httpx>=0.25.0` - Async HTTP client
- `aiohttp>=3.9.0` - Alternative async HTTP client

#### File Handling

- `python-magic>=0.4.27` - File type detection
- `pillow>=10.1.0` - Image processing

#### Frontend & Templates

- `jinja2>=3.1.0` - Template engine for HTMX
- `aiofiles>=23.2.0` - Async file serving for static assets

#### Utilities

- `python-dateutil>=2.8.2` - Date/time utilities
- `python-dotenv>=1.0.0` - Environment loading
- `fastapi-cors>=0.0.6` - CORS middleware

### Development Dependencies

- `pytest>=7.4.0` - Testing framework
- `pytest-asyncio>=0.21.0` - Async test support
- `pytest-cov>=4.1.0` - Coverage reporting
- `ruff>=0.1.0` - Linting/formatting (replaces black, isort, flake8)
- `mypy>=1.7.0` - Type checking
- `pre-commit>=3.6.0` - Git hooks
- `faker>=20.1.0` - Test data generation

## Database Schema

### Core Tables

#### Users (`users`)

- Multi-role authentication system
- Roles: SUPER_ADMIN, DEALER_ADMIN, SALES_MANAGER, etc.
- JWT token management
- Password hashing with bcrypt

#### Dealerships (`dealerships`)

- Multi-location support
- Business information (licenses, tax IDs)
- Contact details and addresses
- Operating hours (JSON)

#### Vehicles (`vehicles`)

- VIN and stock number tracking
- Vehicle specifications (make, model, year, etc.)
- Pricing (cost, sale, MSRP)
- Status tracking (available, sold, reserved, etc.)
- Location tracking

#### Vehicle Images (`vehicle_images`)

- Multiple images per vehicle
- Image type classification (exterior, interior)
- Primary image designation
- Sort order management

#### Customers (`customers`)

- CRM functionality
- Contact information and addresses
- Customer type classification
- Source tracking (walk-in, referral, etc.)

#### Customer Notes (`customer_notes`)

- Interaction history
- Note types (call, email, meeting)
- User attribution

#### Sales (`sales`)

- Deal structuring
- Financing information
- Trade-in tracking
- Document management (JSON URLs)

#### Sale Items (`sale_items`)

- Additional products/services
- Warranties, accessories, etc.
- Quantity and pricing

#### Service Appointments (`service_appointments`)

- Scheduling system
- Service type classification
- Customer concerns tracking
- Reminder system

#### Service Work Orders (`service_work_orders`)

- Technician assignment
- Labor and parts tracking
- Work descriptions and recommendations
- Time tracking

## Frontend Architecture

### HTMX Integration

MDMSGA uses HTMX for dynamic, server-side rendered interfaces that provide:

- **Real-time Updates**: Dynamic content without page reloads
- **Mobile-First Design**: Responsive layouts with touch optimization
- **Progressive Web App**: Installable on mobile devices
- **Offline Support**: Service worker for basic offline functionality

### Template Structure

```text
mdmsga/templates/
├── base.html              # Base template with navigation
├── dashboard.html         # Main dashboard with stats
├── inventory.html         # Vehicle inventory management
├── auth/
│   └── login.html         # Authentication forms
└── offline.html           # Offline page
```

### Static Assets

```text
mdmsga/static/
├── css/
│   └── app.css           # Custom styles with mobile optimizations
├── manifest.json         # PWA manifest
├── sw.js                # Service worker for offline support
└── icons/               # PWA icons (to be added)
```

### Key Features

- **Mobile Navigation**: Hamburger menu + bottom navigation
- **HTMX Attributes**: `hx-get`, `hx-post`, `hx-target` for dynamic updates
- **Loading States**: Built-in loading indicators
- **Modal System**: Dynamic modal forms for CRUD operations
- **Offline Detection**: Visual indicators for connection status
- **Touch Optimization**: 44px minimum touch targets

## API Structure

### Web Interface Routes

- `GET /` - Redirects to dashboard
- `GET /dashboard` - Main dashboard with stats
- `GET /inventory` - Vehicle inventory management
- `GET /customers` - Customer management
- `GET /sales` - Sales management
- `GET /service` - Service management
- `GET /auth/login` - Login page
- `GET /offline.html` - Offline page

### API Endpoints (`/api/v1/`)

#### Authentication Endpoints (`/api/v1/auth/`)

- `POST /login` - OAuth2 token login
- `POST /refresh` - Token refresh
- `POST /register` - User registration
- `GET /me` - Current user info

#### Core Endpoints

- `/users/` - User management
- `/dealerships/` - Dealership operations
- `/inventory/` - Vehicle management
- `/customers/` - CRM operations
- `/sales/` - Sales management
- `/service/` - Service operations

### Response Schemas

- Pydantic models for all requests/responses
- Auto-generated OpenAPI documentation
- Type safety throughout

## Configuration System

### Environment Variables (env.example)

```bash
# Application
APP_NAME=MDMSGA
DEBUG=true
API_V1_STR=/api/v1

# Security
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Database
POSTGRES_SERVER=localhost
POSTGRES_USER=mdmsga_user
POSTGRES_PASSWORD=mdmsga_password
POSTGRES_DB=mdmsga_db

# Valkey (Redis-compatible)
VALKEY_HOST=localhost
VALKEY_PORT=6379
VALKEY_DB=0

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com

# File Storage
UPLOAD_DIR=uploads
MAX_FILE_SIZE=10485760

# Feature Flags
ENABLE_AI_FEATURES=false
ENABLE_REAL_TIME_UPDATES=true
```

### Frontend Configuration

- **HTMX Version**: 1.9.0 (latest stable)
- **Tailwind CSS**: CDN version for rapid development
- **Hyperscript**: 0.9.8 for enhanced interactions
- **PWA Manifest**: Configured for mobile installation
- **Service Worker**: Handles caching and offline functionality

### Settings Class (mdmsga/core/config.py)

- Pydantic BaseSettings for validation
- Auto-assembly of connection strings
- Environment file loading
- Type safety for all config

## Security Implementation

### Authentication Flow

1. User login with email/password
2. Password verification with bcrypt
3. JWT access token generation (30 min)
4. JWT refresh token generation (7 days)
5. Token validation on protected endpoints

### Security Features

- Password hashing with bcrypt
- JWT token expiration
- CORS protection
- Input validation with Pydantic
- SQL injection protection via SQLAlchemy

## Background Tasks (Celery)

### Configuration

- Valkey as message broker
- Valkey as result backend
- Worker processes for task execution
- Beat scheduler for periodic tasks

### Task Types

- Email notifications
- Report generation
- Data processing
- Third-party integrations

## Development Tools

### Ruff Configuration (pyproject.toml)

```toml
[tool.ruff]
select = ["E", "W", "F", "I", "B", "C4", "UP"]
ignore = ["E501", "B008", "C901"]
fixable = ["ALL"]
line-length = 88
target-version = "py311"

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

### Pre-commit Hooks (.pre-commit-config.yaml)

- Ruff linting and formatting
- mypy type checking
- Bandit security scanning
- File hygiene checks

### Testing Setup

- pytest with async support
- Coverage reporting
- Faker for test data
- Database fixtures

## Docker Architecture

### Services (docker-compose.yml)

1. **postgres** - PostgreSQL 15 database
2. **valkey** - Valkey 7 cache/queue (Redis-compatible)
3. **api** - FastAPI application
4. **celery_worker** - Background task worker
5. **celery_beat** - Task scheduler

### Volumes

- `postgres_data` - Database persistence
- `valkey_data` - Cache persistence
- `uploads` - File uploads

### Networks

- `mdmsga_network` - Internal communication

## Deployment Considerations

### Production Requirements

- PostgreSQL 15+ with connection pooling
- Valkey 7+ for caching/queuing
- Reverse proxy (nginx/traefik)
- SSL/TLS termination
- Environment-specific configs

### Scaling Strategy

- Horizontal scaling with load balancers
- Database read replicas
- Valkey clustering
- Celery worker scaling

### Monitoring

- Health check endpoints
- Database connection monitoring
- Valkey connection monitoring
- Application metrics

## Key Design Decisions

### Why Python/FastAPI?

- High performance async framework
- Excellent developer experience
- Rich ecosystem for business logic
- Easy to hire developers

### Why PostgreSQL?

- ACID compliance for financial data
- Rich feature set (JSON, full-text search)
- Excellent performance and reliability
- Strong ecosystem

### Why Valkey over Redis?

- Better performance characteristics
- Lower resource usage
- 100% Redis compatibility
- More active development

### Why uv over pip?

- 10-100x faster dependency resolution
- Better caching
- Lock file management
- Modern Python packaging

### Why Ruff over black/isort/flake8?

- Single tool for multiple purposes
- Much faster execution
- Better rule coverage
- Easier configuration

### Why HTMX over React/Vue?

- Server-side rendering with dynamic updates
- No build process required
- Smaller bundle size
- Better SEO and initial load times
- Progressive enhancement approach
- Easier to maintain for internal tools

## Future Enhancements

### Planned Features

- [x] HTMX frontend application (COMPLETED)
- [ ] Mobile app (React Native)
- [ ] AI-powered analytics
- [ ] Advanced reporting system
- [ ] Third-party integrations
- [ ] Multi-tenant architecture
- [ ] Real-time notifications
- [ ] Document management system

### Technical Debt

- [ ] Add comprehensive test coverage
- [ ] Implement API rate limiting
- [ ] Add audit logging
- [ ] Optimize database queries
- [ ] Add caching strategies
- [ ] Implement backup strategies
- [ ] Add PWA icons and screenshots
- [ ] Complete remaining template files (customer, sales, service forms)

## Troubleshooting Notes

### Common Issues

1. **Database connection errors** - Check PostgreSQL is running and credentials
2. **Valkey connection errors** - Check Valkey is running and accessible
3. **Import errors** - Ensure virtual environment is activated and deps installed
4. **Permission errors** - Check file permissions and uploads directory

### Debug Commands

```bash
# Check services
docker-compose ps
docker-compose logs api
docker-compose logs valkey

# Database
docker-compose exec postgres psql -U mdmsga_user -d mdmsga_db

# Valkey
docker-compose exec valkey redis-cli ping

# Application
uvicorn mdmsga.main:app --reload --log-level debug
```

## Performance Notes

### Database Optimization

- Use indexes on frequently queried columns
- Implement connection pooling
- Consider read replicas for scaling
- Monitor slow queries

### Caching Strategy

- Cache frequently accessed data in Valkey
- Use Redis-style patterns for session storage
- Implement cache invalidation strategies

### API Optimization

- Use async/await for I/O operations
- Implement pagination for large datasets
- Use background tasks for heavy operations
- Consider GraphQL for complex queries

---

_Last updated: [Current Date]_
_Version: 0.1.0_
