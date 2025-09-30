# FastAPI Basic Template

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![Poetry](https://img.shields.io/badge/Poetry-dependency%20management-blue.svg)](https://python-poetry.org/)
[![Code style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

A modern, production-ready **FastAPI** template with **Poetry** for dependency management and **pyenv** for Python version management. This template provides a solid foundation for building scalable REST APIs with best practices built-in.

## ✨ Features

- **🚀 FastAPI**: Modern, fast (high-performance) web framework for building APIs
- **📦 Poetry**: Dependency management and packaging made easy
- **🐍 pyenv**: Python version management for consistent environments
- **🧹 Ruff**: Ultra-fast Python linter and formatter
- **🧪 pytest**: Testing framework with fixtures and coverage
- **🔧 Makefile**: Convenient commands for common development tasks
- **📝 Pre-configured**: Ready-to-use project structure with best practices

## 🏗️ Project Structure

```
fastapi-basic-template/
├── app/                    # Application code
│   ├── __init__.py
│   ├── main.py            # FastAPI application entry point
│   ├── api/               # API routes
│   ├── core/              # Core functionality (config, security)
│   ├── models/            # Database models
│   ├── schemas/           # Pydantic schemas
│   └── services/          # Business logic
├── tests/                 # Test files
├── docs/                  # Documentation
├── pyproject.toml         # Poetry configuration
├── Makefile              # Development commands
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## 🚀 Prerequisites

Make sure you have the following installed on your system:

- **[pyenv](https://github.com/pyenv/pyenv)** - Python version management
- **[Poetry](https://python-poetry.org/)** - Dependency management
- **Python >= 3.11** - Required Python version
- **Make** - For running development commands (usually pre-installed)

### Installation Links

- **pyenv**: [Installation Guide](https://github.com/pyenv/pyenv#installation)
- **Poetry**: [Installation Guide](https://python-poetry.org/docs/#installation)

## ⚙️ Quick Start

### 1. Clone the template

```bash
git clone <your-repo-url> your-project-name
cd your-project-name
```

### 2. Setup the environment

```bash
make setup
```

This command will:

- Install Python 3.11.7 using pyenv
- Create a virtual environment named `fastapi-template`
- Install all project dependencies via Poetry

### 3. Start development server

```bash
make dev
```

The API will be available at:

- **API**: <http://127.0.0.1:8000>
- **Interactive Docs (Swagger)**: <http://127.0.0.1:8000/docs>
- **Alternative Docs (ReDoc)**: <http://127.0.0.1:8000/redoc>

## 🛠️ Development Commands

This template includes a comprehensive Makefile with useful commands:

### Environment & Dependencies

```bash
make setup      # Setup Python environment and install dependencies
make update     # Update all dependencies to latest versions
```

### Development

```bash
make dev        # Start development server with auto-reload
```

### Code Quality

```bash
make lint       # Check code style and potential issues
make format     # Format code using Ruff
make fix        # Auto-fix linting issues
make check      # Format and fix all issues at once
```

### Testing

```bash
make test       # Run all tests with verbose output
```

### Build & Deployment

```bash
make build      # Build distribution packages
make clean      # Clean cache files and build artifacts
```

## 🧪 Testing

The template is configured with pytest for testing:

```bash
# Run all tests
make test

# Run tests with coverage
poetry run pytest --cov=app --cov-report=html

# Run specific test file
poetry run pytest tests/test_main.py
```

## 📝 Code Style

This project uses [Ruff](https://github.com/astral-sh/ruff) for linting and formatting, which is:

- **10-100x faster** than existing tools
- **Drop-in replacement** for Flake8, isort, pydocstyle, and more
- **Zero configuration** required

```bash
# Check code style
make lint

# Format code
make format

# Fix issues automatically
make fix
```

## 🔧 Configuration

### Poetry Configuration

The `pyproject.toml` file contains all project configuration:

```toml
[project]
name = "fastapi-basic-template"
version = "0.1.0"
description = "Basic template for FastAPI project with Poetry"
requires-python = ">=3.11"
```

### Environment Variables

Create a `.env` file in the root directory for environment-specific settings:

```bash
# Database
DATABASE_URL=sqlite:///./app.db

# API Settings
API_V1_PREFIX=/api/v1
PROJECT_NAME="FastAPI Template"
VERSION="0.1.0"

# Security
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 🚀 Deployment

### Using Docker (Recommended)

```dockerfile
# Dockerfile example
FROM python:3.11-slim

WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev

# Copy application
COPY app/ ./app/

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and ensure tests pass: `make test`
4. Format your code: `make check`
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

## 📚 Resources

- **[FastAPI Documentation](https://fastapi.tiangolo.com/)**
- **[Poetry Documentation](https://python-poetry.org/docs/)**
- **[Ruff Documentation](https://docs.astral.sh/ruff/)**
- **[pytest Documentation](https://docs.pytest.org/)**
- **[pyenv Documentation](https://github.com/pyenv/pyenv)**

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙋‍♂️ Support

If you have any questions or run into issues, please:

1. Check the [documentation](https://fastapi.tiangolo.com/)
2. Search [existing issues](https://github.com/your-username/fastapi-basic-template/issues)
3. Create a new issue if needed

---

**Happy coding! 🚀**
