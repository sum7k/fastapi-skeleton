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
export DB_URL="postgresql+asyncpg://user:pass@localhost:5432/your_db_name"

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

### **Infrastructure Ready**

* Docker support
* Observability hooks
* Structured logging
* Environment-based configuration

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
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/your_db
JWT_SECRET_KEY=your-secret-key-here-min-32-chars
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
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

## **Run tests**

```bash
make test
```

## **Run linting and formatting**

```bash
make lint
```

## **Start development server**

```bash
make dev
```

---

# 📄 **Core API Endpoints**

| Method       | Endpoint            | Description                    |
| ------------ | ------------------- | ------------------------------ |
| `POST`       | `/auth/register`    | Register a new user            |
| `POST`       | `/auth/token`       | Login and get JWT token        |
| `GET`        | `/auth/me`          | Get current user info          |
| `GET`        | `/health`           | Health check endpoint          |

OpenAPI docs available at:

```
http://localhost:8000/docs
http://localhost:8000/redoc
```

---

# 📈 **Observability & Monitoring**

fa-skeleton includes hooks for:

### Logging

* Structured logging setup
* Request/response logging
* Error tracking
* Correlation IDs

### Metrics

* Request duration
* Error rates
* Authentication attempts
* Database query performance

### Health Checks

* Database connectivity
* Application health status
* Dependency health

Easily integrate with Prometheus, Grafana, DataDog, or your monitoring stack of choice.

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
