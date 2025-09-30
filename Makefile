APP_NAME=app.main:app
PYTHON_VERSION=3.11.7

POETRY = poetry
PYTHON = $(POETRY) run python
RUFF = $(POETRY) run ruff
PYTEST = $(POETRY) run pytest

setup:
	pyenv install -s $(PYTHON_VERSION)
	pyenv virtualenv -f $(PYTHON_VERSION) fastapi-template
	pyenv local fastapi-template
	$(POETRY) install

dev:
	$(POETRY) run uvicorn $(APP_NAME) --reload

test:
	$(PYTEST) -v --maxfail=1 --disable-warnings

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
