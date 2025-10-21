# 🚀 Development Guide - CareerPython

This guide contains all the necessary information to set up and develop on the CareerPython project.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Environment Configuration](#environment-configuration)
- [Project Structure](#project-structure)
- [Main Commands](#main-commands)
- [Testing](#testing)
- [Database](#database)
- [Frontend](#frontend)
- [Debugging](#debugging)
- [Linting and Formatting](#linting-and-formatting)
- [Architecture](#architecture)
- [Contributing](#contributing)
- [Troubleshooting](#troubleshooting)

## 🔧 Prerequisites

### Required Software

- **Python 3.13+** (required)
- **Docker** and **Docker Compose** (for services)
- **uv** (Python package manager)
- **Node.js 18+** and **npm** (for frontend)
- **Git**

### Prerequisites Installation

#### macOS
```bash
# Install Python 3.13 with pyenv
brew install pyenv
pyenv install 3.13.7
pyenv global 3.13.7

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Docker Desktop
brew install --cask docker

# Install Node.js
brew install node
```

#### Linux (Ubuntu/Debian)
```bash
# Install Python 3.13
sudo apt update
sudo apt install python3.13 python3.13-venv python3.13-dev

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Docker
sudo apt install docker.io docker-compose

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

## 📦 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/darkspock/CareerPython.git
cd CareerPython
```

### 2. Setup Python Environment
```bash
# Create and activate virtual environment with uv
uv venv
source .venv/bin/activate  # On Linux/macOS
# or .venv\Scripts\activate on Windows

# Install dependencies
uv sync
```

### 3. Configure Environment Variables
```bash
# Copy configuration file
cp .env.example .env

# Edit variables according to your environment
nano .env
```

### 4. Start Services with Docker
```bash
# Start services (PostgreSQL, Redis, etc.)
make start

# Verify services are running
docker-compose ps
```

### 5. Setup Database
```bash
# Run migrations
make migrate

# Optional: Load test data
make seed  # If this command exists
```

## ⚙️ Environment Configuration

### .env File
Configure the following variables in your `.env` file:

```env
# Database
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_DB=careerpython_dev
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Authentication
SECRET_KEY=your_super_secure_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=2880

# External APIs
RAPIDAPI_KEY=your_rapidapi_key
XAI_API_KEY=your_xai_api_key
XAI_API_URL=https://api.x.ai/v1

# Mailgun (optional)
MAILGUN_API_KEY=your_mailgun_key
MAILGUN_DOMAIN=your_domain
MAILGUN_API_URL=https://api.mailgun.net/v3
```

### Frontend (.env.local)
```bash
cd client
cp .env.example .env.local
```

Configure:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🏗️ Project Structure

```
CareerPython/
├── src/                          # Main source code
│   ├── candidate/               # Candidate domain
│   │   ├── application/         # Use cases (Commands/Queries)
│   │   ├── domain/             # Entities and business logic
│   │   ├── infrastructure/     # Implementations (DB, APIs)
│   │   └── presentation/       # Controllers and DTOs
│   ├── user/                   # User domain
│   ├── interview/              # Interview domain
│   ├── shared/                 # Shared code
│   └── ...
├── adapters/                   # HTTP adapters
│   └── http/                   # Controllers and schemas
├── core/                       # Core configuration
├── tests/                      # Unit and integration tests
├── client/                     # Next.js frontend
├── migrations/                 # Alembic migrations
├── docker-compose.yml          # Docker services
├── Makefile                    # Development commands
└── pyproject.toml             # Dependencies configuration
```

## 🛠️ Main Commands

### Backend Development
```bash
# Start services
make start

# Stop services
make stop

# View logs
make logs

# Access container bash
make bash

# Restart services
make restart
```

### Database
```bash
# Create new migration
make revision m="migration description"

# Run migrations
make migrate

# Migration rollback
make downgrade

# Rebuild local virtual environment
make rebuild-venv
```

### Frontend
```bash
cd client

# Development
npm run dev          # http://localhost:5173

# Build
npm run build
npm run start

# Linting
npm run lint
```

## 🧪 Testing

### Backend
```bash
# Run all tests
make test

# Specific tests
pytest tests/unit/candidate/
pytest tests/integration/

# Tests with coverage
pytest --cov=src --cov-report=html

# Tests in watch mode
pytest-watch
```

### Test Types
- **Unit Tests**: `tests/unit/` - Business logic tests
- **Integration Tests**: `tests/integration/` - Integration tests
- **E2E Tests**: `tests/e2e/` - End-to-end tests

### Run Specific Tests
```bash
# By domain
pytest tests/unit/candidate/

# By test type
pytest tests/unit/candidate/commands/
pytest tests/unit/candidate/queries/

# Specific test
pytest tests/unit/candidate/commands/test_create_candidate.py::TestCreateCandidate::test_success
```

## 🗄️ Database

### Migrations
```bash
# Create auto migration
alembic revision --autogenerate -m "description"

# Create empty migration
alembic revision -m "description"

# Apply migrations
alembic upgrade head

# View history
alembic history

# Rollback
alembic downgrade -1
```

### Direct Connection
```bash
# PostgreSQL CLI
docker-compose exec db psql -U your_user -d careerpython_dev

# PgAdmin (if configured)
http://localhost:5050
```

## 🎨 Frontend

### Development
```bash
cd client

# Install dependencies
npm install

# Development mode
npm run dev

# Build for production
npm run build
npm run start
```

### Frontend Technologies
- **Framework**: Next.js 14+ (App Router)
- **Styles**: Tailwind CSS
- **Components**: Base UI
- **Forms**: React Hook Form
- **i18n**: next-i18next (en/es)
- **HTTP**: Axios with centralized API client

## 🐛 Debugging

### Backend
```python
# Logging in code
import logging
logger = logging.getLogger(__name__)
logger.info("Debug message")
```

### VS Code Configuration
Create `.vscode/launch.json`:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/.venv/bin/uvicorn",
            "args": ["main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
            "console": "integratedTerminal",
            "python": "${workspaceFolder}/.venv/bin/python"
        }
    ]
}
```

### Logs
```bash
# View service logs
make logs

# Specific logs
docker-compose logs web
docker-compose logs db
docker-compose logs redis
```

## 🔍 Linting and Formatting

### Python
```bash
# Flake8 (linting)
flake8 src/ tests/

# Autopep8 (formatting)
autopep8 --in-place --recursive src/

# Autoflake (import cleanup)
autoflake --remove-all-unused-imports --in-place --recursive src/

# MyPy (type checking)
mypy src/

# Run all linters
make lint  # If this command exists
```

### Configuration in pyproject.toml
```toml
[tool.mypy]
python_version = "3.13"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

## 🏛️ Architecture

### Clean Architecture
The project follows Clean Architecture principles with DDD:

- **Domain**: Entities, Value Objects, Enums
- **Application**: Use Cases (Commands/Queries), DTOs
- **Infrastructure**: Repositories, External APIs, Database
- **Presentation**: Controllers, HTTP Schemas

### Implemented Patterns
- **CQRS**: Commands/Queries separation
- **Repository Pattern**: Data abstraction
- **Dependency Injection**: Using dependency-injector
- **Event-Driven**: Domain Events
- **Object Mother**: For test data

### Mandatory Data Flow
```
HTTP Request → Controller → Command/Query → Handler → Repository → Database
Database → Repository → Entity → DTO → Response Schema → HTTP Response
```

## 🤝 Contributing

### Workflow
1. **Create branch**: `git checkout -b feature/new-functionality`
2. **Develop**: Follow Clean Architecture principles
3. **Tests**: Write unit and integration tests
4. **Linting**: Run linters and formatters
5. **Commit**: Use descriptive messages
6. **Push**: `git push origin feature/new-functionality`
7. **PR**: Create Pull Request with detailed description

### Code Standards
- **Naming**: snake_case for Python, camelCase for TypeScript
- **Imports**: Alphabetically ordered
- **Docstrings**: For public classes and methods
- **Type Hints**: Mandatory in Python
- **Tests**: Minimum 80% coverage

### Commits
Use conventional format:
```
feat: add new candidate search functionality
fix: resolve authentication token expiration
docs: update API documentation
test: add unit tests for user service
refactor: improve query performance
```

## 🚨 Troubleshooting

### Common Issues

#### Port Already in Use Error
```bash
# Check what's using port 8000
lsof -i :8000

# Kill process
kill -9 PID
```

#### Docker Issues
```bash
# Clean containers
docker-compose down -v
docker system prune -f

# Rebuild images
docker-compose build --no-cache
```

#### Dependency Issues
```bash
# Clean and reinstall
rm -rf .venv
uv venv
uv sync
```

#### Database Issues
```bash
# Reset database
make reset-db  # If exists
# or manually:
docker-compose down -v
docker-compose up -d db
make migrate
```

#### Failing Tests
```bash
# Clear pytest cache
pytest --cache-clear

# Verify test environment
pytest --collect-only
```

### Useful Logs
```bash
# Application logs
tail -f logs/app.log

# Error logs
grep -i error logs/app.log

# Database logs
docker-compose logs db | tail -100
```

## 📚 Additional Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Clean Architecture**: https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html
- **Domain-Driven Design**: https://martinfowler.com/bliki/DomainDrivenDesign.html
- **Next.js Docs**: https://nextjs.org/docs
- **Base UI**: https://base-ui.com/

## 🆘 Help

If you have issues:
1. Check this documentation
2. Review application logs
3. Search repository issues
4. Contact the development team

---

Happy coding! 🎉