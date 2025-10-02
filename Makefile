.PHONY: install dev test lint format check clean help


APP_NAME=app.main:app
PYTHON_VERSION=3.11.7

POETRY = poetry
PYTHON = $(POETRY) run python
RUFF = $(POETRY) run ruff
PYTEST = $(POETRY) run pytest

.DEFAULT_GOAL := help


setup:
	pyenv install $(PYTHON_VERSION)
	pyenv local $(PYTHON_VERSION)
	$(POETRY) install
	cp .env.example .env

dev:
	$(POETRY) run uvicorn $(APP_NAME) --reload

test:
	$(PYTEST) -v --maxfail=1 --disable-warnings

test-cov:
	$(PYTEST) --cov=app --cov-report=html --cov-report=term

lint:
	$(RUFF) check .

format:
	$(RUFF) format .

fix:
	$(RUFF) check . --fix

check: format fix
	@echo "✅ Code formatted and linted!"

update:
	$(POETRY) update

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf dist build *.egg-info

build:
	$(POETRY) build

## Start database (development)
db-up:
	docker-compose up -d

## Stop database
db-down:
	docker-compose down

## Database migrations
migrate:
	$(POETRY) run alembic upgrade head

## Create new migration
migration:
	$(POETRY) run alembic revision --autogenerate -m "$(msg)"

## Reset database
db-reset:
	$(POETRY) run alembic downgrade base
	$(POETRY) run alembic upgrade head

## Check migration status
db-status:
	$(POETRY) run alembic current

## Show migration history
db-history:
	$(POETRY) run alembic history --verbose

## Show project info
info:
	$(POETRY) show
	@echo "\n📋 Project Info:"
	@echo "Python: $$($(PYTHON) --version)"
	@echo "Poetry: $$($(POETRY) --version)"
	@echo "FastAPI: $$($(PYTHON) -c 'import fastapi; print(fastapi.__version__)')"

## Enter poetry shell
shell:
	$(POETRY) shell

## Update dependencies
update:
	$(POETRY) update

## Install pre-commit hooks
hooks:
	$(POETRY) run pre-commit install

## Run pre-commit on all files
pre-commit:
	$(POETRY) run pre-commit run --all-files

help:
	@echo "🚀 FastAPI Portfolio Backend"
	@echo ""
	@echo "Available commands:"
	@awk 'BEGIN {FS = ":.*##"; printf ""} /^[a-zA-Z_-]+:.*##/ {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)