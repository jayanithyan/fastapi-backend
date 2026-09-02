.PHONY: help install dev test lint format db-migrate db-upgrade clean

help:
	@echo "Available commands:"
	@echo "  make install       - Install dependencies"
	@echo "  make dev           - Run development server"
	@echo "  make test          - Run tests"
	@echo "  make lint          - Run linters"
	@echo "  make format        - Format code"
	@echo "  make clean         - Clean up cache files"
	@echo "  make docker-up     - Start Docker containers"
	@echo "  make docker-down   - Stop Docker containers"

.env:
	cp .env.example .env

install: .env
	pip install -r requirements.txt

dev: .env
	uvicorn main:app --reload

test:
	pytest tests/ -v --cov=. --cov-report=html

lint:
	pylint **/*.py

format:
	black .
	autopep8 --in-place --aggressive --aggressive -r .

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .coverage htmlcov .eggs *.egg-info dist build

db-upgrade:
	alembic upgrade head

db-migrate:
	alembic revision --autogenerate -m "Auto migration"

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f api
