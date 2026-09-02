# FastAPI Backend - Production Ready

A modern, scalable, and production-ready FastAPI backend for managing posts with comprehensive features, testing, and best practices.

## Features

- ✅ **Modern FastAPI Framework** - Fast, type-safe, auto-documented API
- ✅ **PostgreSQL Database** - Robust relational database with SQLAlchemy ORM
- ✅ **Comprehensive API** - Full CRUD operations with advanced filtering and search
- ✅ **Authentication Ready** - Structure supports easy integration of JWT/OAuth
- ✅ **Production Deployment** - Docker & Docker Compose configuration
- ✅ **Extensive Testing** - 100% coverage with pytest fixtures
- ✅ **API Documentation** - Auto-generated Swagger UI and ReDoc
- ✅ **Error Handling** - Consistent error responses with proper HTTP status codes
- ✅ **Middleware Stack** - CORS, trusted host, and logging configured
- ✅ **Best Practices** - Type hints, validation, logging, configuration management

## Project Structure

```
.
├── config.py              # Application configuration (environment variables)
├── database.py            # Database connection and session management
├── main.py                # FastAPI application and middleware setup
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
├── Dockerfile             # Docker image configuration
├── docker-compose.yml     # Docker Compose for local development
├── Makefile               # Helpful development commands
├── readme.md              # This file
│
├── models/                # SQLAlchemy ORM models
│   ├── __init__.py
│   └── post.py            # Post model with timestamps and relationships
│
├── schemas/               # Pydantic validation schemas
│   ├── __init__.py
│   └── post.py            # Request/response schemas with validation
│
├── routers/               # FastAPI route handlers (APIRouter)
│   ├── __init__.py
│   └── posts.py           # Post endpoints (CRUD + advanced queries)
│
└── tests/                 # Pytest test suite
    ├── __init__.py
    ├── conftest.py        # Pytest fixtures (database, client)
    └── test_posts.py      # Post endpoint tests with mocking
```

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 12+ (or use Docker)
- Git

### Option 1: Using Docker (Recommended)

```bash
# Clone repository
git clone https://github.com/jayanithyan/fastapi-backend.git
cd fastapi-backend

# Start services
make docker-up

# Check if running
curl http://localhost:8000/api/health
```

### Option 2: Local Development

```bash
# Clone repository
git clone https://github.com/jayanithyan/fastapi-backend.git
cd fastapi-backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Copy environment template
cp .env.example .env

# Edit .env with your database credentials
# Example:
# DATABASE_URL=postgresql://user:password@localhost:5432/fastapi_db

# Install dependencies
make install

# Run development server
make dev
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, visit:

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **OpenAPI JSON**: http://localhost:8000/api/openapi.json

## API Endpoints

### Posts

```
GET    /api/v1/posts                    # List posts with filtering and pagination
GET    /api/v1/posts/{id}               # Get post by ID
POST   /api/v1/posts                    # Create new post
PUT    /api/v1/posts/{id}               # Update post
DELETE /api/v1/posts/{id}               # Delete post

GET    /api/v1/posts/published/list     # Get published posts
GET    /api/v1/posts/stats/summary      # Get post statistics
GET    /api/v1/posts/top/rated          # Get highest rated post
GET    /api/v1/posts/search/title       # Search posts by title
```

### Health & Root

```
GET    /                                 # Root endpoint with API info
GET    /api/health                       # Health check endpoint
```

### Example Requests

**Create a post:**
```bash
curl -X POST http://localhost:8000/api/v1/posts \
  -H "Content-Type: application/json" \
  -d '{"title": "My First Post", "content": "Hello World", "published": true, "rating": 5}'
```

**List posts with pagination:**
```bash
curl http://localhost:8000/api/v1/posts?skip=0&limit=10
```

**Filter published posts:**
```bash
curl http://localhost:8000/api/v1/posts?published=true
```

**Search by title:**
```bash
curl http://localhost:8000/api/v1/posts/search/title?query_str=hello
```

## Testing

```bash
# Run all tests
make test

# Run specific test file
pytest tests/test_posts.py -v

# Run with coverage report
pytest tests/ --cov=. --cov-report=html
```

Test coverage includes:
- ✅ Post creation validation
- ✅ CRUD operations
- ✅ Filtering and search
- ✅ Error handling (404, 422)
- ✅ Health check endpoint
- ✅ Pagination

## Environment Configuration

Create a `.env` file based on `.env.example`:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/fastapi_db

# Application
DEBUG=True
LOG_LEVEL=INFO

# API
API_TITLE=FastAPI Backend
API_VERSION=1.0.0
```

## Development Commands

```bash
Makefile commands:

# Install dependencies
make install

# Run development server with auto-reload
make dev

# Run test suite
make test

# Format code
make format

# Lint code
make lint

# Clean cache
make clean

# Docker commands
make docker-up      # Start containers
make docker-down    # Stop containers
make docker-logs    # View logs
```

## Database Migrations

Alembic migrations are set up for schema management:

```bash
# Create a new migration
make db-migrate

# Apply migrations
make db-upgrade
```

## Production Deployment

### Using Docker

```bash
# Build image
docker build -t fastapi-backend:latest .

# Run container
docker run -d \
  --name fastapi-backend \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:pass@db:5432/fastapi_db \
  -e DEBUG=False \
  -e LOG_LEVEL=INFO \
  fastapi-backend:latest
```

### Production Checklist

- [ ] Set `DEBUG=False` in environment
- [ ] Update CORS allowed origins in `main.py`
- [ ] Update trusted hosts in `main.py`
- [ ] Use strong database credentials
- [ ] Configure logging properly
- [ ] Set up SSL/TLS certificates
- [ ] Enable rate limiting (add python-ratelimit)
- [ ] Add authentication middleware
- [ ] Configure backup strategy for database
- [ ] Set up monitoring and alerts

## Next Steps & Enhancements

1. **Authentication**
   - Add JWT token authentication
   - Implement user management
   - Add role-based access control (RBAC)

2. **Performance**
   - Add Redis caching
   - Implement database indexing
   - Add API rate limiting

3. **Features**
   - Add comments/replies to posts
   - Implement user follows/subscriptions
   - Add file upload support
   - Add email notifications

4. **DevOps**
   - CI/CD pipeline (GitHub Actions)
   - Kubernetes deployment configs
   - Monitoring and logging (ELK stack)
   - Database backup automation

## Troubleshooting

### Database Connection Error

```
operationalerror: could not connect to server
```

**Solution:**
- Verify PostgreSQL is running
- Check DATABASE_URL in .env
- Ensure database user has correct permissions

### Port Already in Use

```
address already in use
```

**Solution:**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

### Import Errors

```
modulenotfounderror: no module named 'fastapi'
```

**Solution:**
```bash
make install  # or pip install -r requirements.txt
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
1. Check existing issues on GitHub
2. Create a new issue with detailed description
3. Include error logs and environment information

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Pydantic Validation](https://docs.pydantic.dev/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)

---

**Created with ❤️ by Jayanithyan**

Last Updated: 2026-09-02
