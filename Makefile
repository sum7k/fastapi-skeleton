.PHONY: dev test lint token setup migrate migrate-create migrate-downgrade db-start db-stop db-restart db-logs db-destroy db-status

# Run development server
dev:
	poetry run uvicorn main:app --reload

# Run tests
test:
	poetry run pytest

# Run database migrations
migrate:
	poetry run alembic upgrade head

# Create a new migration
migrate-create:
	@read -p "Enter migration message: " msg; \
	poetry run alembic revision --autogenerate -m "$$msg"

# Rollback last migration
migrate-downgrade:
	poetry run alembic downgrade -1

# Run linting
lint:
	poetry run pre-commit run --all-files

# Generate JWT token for local development
token:
	@poetry run python scripts/generate_token.py

# Generate token with custom email
token-admin:
	@poetry run python scripts/generate_token.py --email admin@example.com --role ADMIN

# Setup: Check environment variables
setup:
	@echo "Checking required environment variables..."
	@[ -n "$$JWT_SECRET_KEY" ] && echo "✅ JWT_SECRET_KEY is set" || echo "❌ JWT_SECRET_KEY not set"
	@[ -n "$$DB_URL" ] && echo "✅ DB_URL is set" || echo "❌ DB_URL not set"
	@echo ""
	@echo "If missing, set them with:"
	@echo "  export JWT_SECRET_KEY='your-secret-key-min-32-chars'"
	@echo "  export DB_URL='postgresql+asyncpg://user:pass@localhost/fa-skeleton-db'"

# Database management
db-start:
	@./scripts/local_dev_db.sh start

db-stop:
	@./scripts/local_dev_db.sh stop

db-restart:
	@./scripts/local_dev_db.sh restart

db-logs:
	@./scripts/local_dev_db.sh logs

db-destroy:
	@./scripts/local_dev_db.sh destroy

db-status:
	@./scripts/local_dev_db.sh status
