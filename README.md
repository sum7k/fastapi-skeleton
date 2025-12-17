# **fa-skeleton — Production-Ready FastAPI Skeleton with Auth & Observability**

**fa-skeleton** is a **reusable FastAPI application skeleton** designed to jumpstart your next Python API project with enterprise-grade features built in from day one.

Stop starting from scratch. **fa-skeleton** provides:

* JWT-based authentication with role-based access control
* Database migrations with Alembic
* Structured logging and observability hooks
* Modern Python patterns (async/await, dependency injection)
* Comprehensive test setup with pytest
* Pre-configured CI/CD workflows

Built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**, this skeleton follows best practices for maintainability, scalability, and security.

Whether you're building an internal tool, a SaaS product, or a microservice, fa-skeleton gives you the foundation to focus on your business logic instead of boilerplate.

---

# ⭐ **What fa-skeleton Provides**

### 🔹 **1. Complete Authentication System**

Out-of-the-box JWT authentication with:

* User registration and login
* Token generation and validation
* Role-based access control (RBAC)
* Password hashing with bcrypt
* Token expiration and refresh patterns
* Secure credential storage

### 🔹 **2. Database Layer**

Production-ready database setup:

* Async SQLAlchemy ORM
* PostgreSQL support
* Alembic migrations
* Repository pattern implementation
* Clean separation of models, schemas, and domain logic
* Database connection pooling

### 🔹 **3. Project Structure**

Well-organized, scalable architecture:

* Feature-based module organization
* Separation of concerns (models, repositories, services, routers)
* Domain-driven design patterns
* Dependency injection with FastAPI
* Type hints throughout
* Comprehensive test coverage

### 🔹 **4. Developer Experience**

Everything you need to move fast:

* Makefile for common tasks
* Pre-configured pytest setup
* Factory pattern for test data
* Code quality tools (linting, formatting)
* Environment variable management
* Development and production configurations

---

# 🧩 **Architecture Overview**

```
FastAPI Router Layer
       ↓
Service Layer (Business Logic)
       ↓
Repository Layer (Data Access)
       ↓
Database Models (SQLAlchemy)
       ↓
PostgreSQL Database
```

Clean separation of concerns with dependency injection throughout.

---

# 🔐 **Authentication**

fa-skeleton uses **JWT (JSON Web Tokens)** for secure API authentication with role-based access control.

### Required Environment Variables

```bash
# Copy .env.example to .env and update values
cp .env.example .env

# Or set manually:
export JWT_SECRET_KEY="your-super-secret-key-here-min-32-chars"
export DB_HOST="localhost"
export DB_PORT="5432"
export DB_NAME="your_db_name"
export DB_USER="user"
export DB_PASSWORD="pass"

# Optional: Enable distributed tracing with OpenTelemetry
export OTLP_ENDPOINT="http://localhost:4318/v1/traces"  # For Jaeger/OTLP collector

# Generate a secure secret key with:
openssl rand -hex 32
```

Check your setup with:
```bash
make setup
```

### Local Development - Generate Test Tokens

**Option 1: Using the helper script**

```bash
# Generate token with default user (dev@example.com, MEMBER role)
make token

# Generate token for specific email
python scripts/generate_token.py --email admin@example.com --role ADMIN

# Generate token with custom expiry (default: 24 hours)
python scripts/generate_token.py --email user@example.com --hours 48
```

**Option 2: Register via API**

```bash
# Register a new user
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "Pass123!"}'

# Login to get token
curl -X POST http://localhost:8000/auth/token \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "Pass123!"}'
```

### Using Protected Endpoints

```bash
# Test authentication with /auth/me endpoint
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  http://localhost:8000/auth/me
```

### Available Roles

- **OWNER** - Full access to all resources
- **ADMIN** - Administrative access
- **MEMBER** - Standard user access
- **VIEWER** - Read-only access
- **API_KEY** - Programmatic access

---

# 🛠️ **Tech Stack**

### **Backend**

* FastAPI (async)
* Python 3.10+
* SQLAlchemy (async)
* PostgreSQL
* Pydantic v2
* Alembic migrations

### **Authentication & Security**

* JWT tokens with python-jose
* Password hashing with passlib + bcrypt
* Role-based access control (RBAC)
* Secure environment variable management

### **Development & Testing**

* pytest with async support
* Factory Boy for test data
* Pre-configured CI/CD workflows
* Make commands for common tasks

### **Observability**

* OpenTelemetry (OTEL) instrumentation
* Distributed tracing with Jaeger support
* Prometheus metrics
* Structured logging with correlation IDs

### **Infrastructure Ready**

* Docker support
* Environment-based configuration
* Health check endpoints
* Production-ready patterns

fa-skeleton is designed to be forked, customized, and extended for your specific needs.

---

# 🚀 **Getting Started**

## **1. Clone or fork the repository**

```bash
git clone https://github.com/your-username/fa-skeleton.git
cd fa-skeleton
```

## **2. Install Poetry** (if not already installed)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

## **3. Install dependencies**

```bash
poetry install
```

## **4. Configure environment variables**

Create a `.env` file:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_db
DB_USER=user
DB_PASSWORD=pass
JWT_SECRET_KEY=your-secret-key-here-min-32-chars
```

## **5. Run database migrations**

```bash
poetry run alembic upgrade head
```

## **6. Start the backend**

```bash
make dev
```

## **7. Test the API**

```bash
# Visit the interactive API docs
open http://localhost:8000/docs
```

---

# 🧪 **Development Commands**

### **Core Commands**

```bash
make dev          # Start development server with hot reload
make test         # Run all tests with pytest
make lint         # Run linting and formatting checks
make setup        # Check required environment variables
```

### **Database Management**

```bash
make db-start     # Start PostgreSQL in Docker
make db-stop      # Stop PostgreSQL container
make db-restart   # Restart PostgreSQL container
make db-logs      # View PostgreSQL logs
make db-status    # Check database status
make db-destroy   # Remove database container and data

make migrate      # Run database migrations
make migrate-create  # Create new migration (autogenerate)
make migrate-downgrade  # Rollback last migration
```

### **Authentication Tokens**

```bash
make token        # Generate JWT token (default: dev@example.com, MEMBER)
make token-admin  # Generate admin token (admin@example.com, ADMIN)
```

### **Observability - Jaeger Tracing**

```bash
make jaeger-start # Start Jaeger UI + OTLP collector
make jaeger-stop  # Stop and remove Jaeger container
make jaeger-logs  # View Jaeger logs

# After starting Jaeger:
# - UI: http://localhost:16686
# - Set OTLP_ENDPOINT=http://localhost:4318/v1/traces
```

---

# 📄 **Core API Endpoints**

| Method       | Endpoint            | Description                    |
| ------------ | ------------------- | ------------------------------ |
| `POST`       | `/auth/register`    | Register a new user            |
| `POST`       | `/auth/token`       | Login and get JWT token        |
| `GET`        | `/auth/me`          | Get current user info          |
| `GET`        | `/health`           | Health check endpoint          |
| `GET`        | `/metrics`          | Prometheus metrics             |

OpenAPI docs available at:

```
http://localhost:8000/docs
http://localhost:8000/redoc
```

---

# 📈 **Observability & Monitoring**

fa-skeleton comes with production-ready observability powered by **OpenTelemetry**:

### Distributed Tracing with OpenTelemetry

* **Automatic instrumentation** for FastAPI, SQLAlchemy, and HTTP requests
* **Console exporter** for development (traces logged to stdout)
* **OTLP exporter** for production (configurable endpoint)
* **Jaeger integration** - view traces in Jaeger UI
* Automatic trace context propagation
* Service name auto-detected from pyproject.toml

**Configure OTLP endpoint** in `.env` (optional):
```bash
# Send traces to Jaeger, Tempo, or any OTLP collector
export OTLP_ENDPOINT="http://localhost:4318/v1/traces"
```

**Run Jaeger locally** for trace visualization:
```bash
# Easy way - using make command
make jaeger-start

# Or manually with Docker
docker run -d --name jaeger \
  -p 16686:16686 \
  -p 4318:4318 \
  jaegertracing/all-in-one:latest

# View traces at http://localhost:16686
# Stop with: make jaeger-stop
```

### Logging

* Structured logging with correlation IDs
* Request/response logging
* Error tracking with full context
* Trace context included in logs

### Metrics with Prometheus

fa-skeleton automatically exposes **Prometheus-compatible metrics** at the `/metrics` endpoint.

**Available Metrics:**
* `request_count` - Total HTTP requests by method, path, and status code
* `error_count` - Total 5xx errors by method, path, and status code
* `request_latency_seconds` - HTTP request latency histogram
* `db_query_duration_seconds` - Database query duration histogram
* `db_errors_total` - Database query errors

**View metrics:**
```bash
# Check metrics endpoint
curl http://localhost:8000/metrics
```

**Integrate with Prometheus:**

Create a `prometheus.yml` configuration:
```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'fa-skeleton'
    static_configs:
      - targets: ['host.docker.internal:8000']
```

Run Prometheus:
```bash
docker run -d --name prometheus \
  -p 9090:9090 \
  -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus

# Prometheus UI: http://localhost:9090
```

**Visualize with Grafana:**
```bash
docker run -d --name grafana \
  -p 3000:3000 \
  grafana/grafana

# Grafana UI: http://localhost:3000 (admin/admin)
# Add Prometheus as data source: http://prometheus:9090
```

### Health Checks

* Database connectivity
* Application health status
* Dependency health

All observability features work seamlessly together for full-stack visibility.

---

# 📦 **Why fa-skeleton?**

Starting a new FastAPI project shouldn't mean writing the same authentication, database setup, and project structure over and over.

**fa-skeleton gives you a head start** with production-ready patterns that have been battle-tested.

Use it as:

* A starting point for new API projects
* A learning resource for FastAPI best practices
* A template for microservices
* A foundation for SaaS products
* A reference implementation for clean architecture

---

# 🤝 Contributing

Contributions are welcome!

* Open issues
* Submit PRs
* Suggest improvements
* Add new features

See **CONTRIBUTING.md** for guidelines.

---

# 📝 License

This is free and unencumbered software released into the public domain.

---

# 🌟 Extending fa-skeleton

fa-skeleton is designed to be extended. Add your own features:

* Additional authentication providers (OAuth, SAML)
* Rate limiting and throttling
* Caching layer (Redis)
* Background task processing (Celery, RQ)
* File uploads and storage
* Email notifications
* Websocket support
* GraphQL endpoints
* Multi-tenancy
* Audit logging
* API versioning
* Frontend (React, Vue, Svelte)
* Comprehensive API documentation
* Additional database support (MySQL, SQLite)
