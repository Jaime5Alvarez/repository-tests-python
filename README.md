# Repository Tests Python

Example project with repository tests using SQLAlchemy, pytest, and testcontainers.

## 📋 Prerequisites

- **Python 3.12+**
- **uv** - Fast Python package manager ([Install uv](https://docs.astral.sh/uv/))
- **Docker** - Required to run testcontainers with PostgreSQL

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/Jaime5Alvarez/repository-tests-python.git
cd repository-tests-python
```

2. Install dependencies with uv:
```bash
uv sync
```

This will automatically create a virtual environment and install all dependencies listed in `pyproject.toml`.

## 🧪 Running Tests

### Run all tests

```bash
uv run pytest
```

### Run tests with verbose output

```bash
uv run pytest -v
```

### Run a specific test file

```bash
uv run pytest src/modules/users/infraestructure/persistance/test_repository.py
```

### Run a specific test

```bash
uv run pytest src/modules/users/infraestructure/persistance/test_repository.py::TestSqlAlchemyUserRepository::test_create_user
```

### Show full output (including prints)

```bash
uv run pytest -s
```

### Run tests in parallel (faster)

```bash
uv run pytest -n auto
```

> **Note:** To run tests in parallel, you need to install `pytest-xdist`:
> ```bash
> uv add pytest-xdist
> ```

## 📊 Useful Pytest Options

| Command | Description |
|---------|-------------|
| `uv run pytest -v` | Verbose mode (shows each test) |
| `uv run pytest -s` | Shows prints and outputs |
| `uv run pytest -x` | Stop on first failure |
| `uv run pytest --lf` | Run only tests that failed last time |
| `uv run pytest --ff` | Run failed tests first |
| `uv run pytest -k "create"` | Run only tests containing "create" in the name |
| `uv run pytest --collect-only` | Show all tests without running them |

## 🐳 About Testcontainers

This project uses **testcontainers** to create ephemeral PostgreSQL containers during tests. Make sure Docker is running before executing tests:

```bash
# Verify Docker is running
docker ps
```

## 📁 Project Structure

```
src/
├── conftest.py                                    # Global pytest fixtures
└── modules/
    ├── shared/
    │   └── database/
    │       └── sql_alchemy_db.py                  # DB session manager
    └── users/
        ├── domain/
        │   ├── entities.py                        # Domain entities
        │   └── interfaces.py                      # Repository interfaces
        └── infraestructure/
            └── persistance/
                ├── models.py                      # SQLAlchemy models
                ├── repository.py                  # Repository implementation
                └── test_repository.py             # Repository tests
```

## 🔧 Additional Configuration

Pytest configuration is located in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
pythonpath = "."
```

## 📝 Main Dependencies

- **pytest** - Testing framework
- **pytest-asyncio** - Support for async tests
- **testcontainers** - Docker containers for integration testing
- **SQLAlchemy** - Python ORM
- **asyncpg** - Async driver for PostgreSQL

---

Need help? Check the [pytest documentation](https://docs.pytest.org/) or [testcontainers documentation](https://testcontainers-python.readthedocs.io/).
