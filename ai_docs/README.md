# CareerPython AI Documentation

Complete development documentation for AI assistants working on this recruitment platform.

## Quick Start

**ALWAYS read these first:**
1. [Critical Rules](critical-rules.md) - **MUST READ** before any task
2. [Architecture](architecture.md) - Understand DDD and Clean Architecture

## Documentation Index

### Core Architecture
- **[Critical Rules](critical-rules.md)** - Database Performance, CQRS, Response Patterns (READ FIRST)
- **[Architecture](architecture.md)** - DDD, Clean Architecture, Bounded Contexts
- **[Code Quality](code-quality.md)** - SOLID Principles, Naming Conventions, Best Practices

### Application Layer (CQRS)
- **[Application Layer](application-layer.md)** - Queries, Commands, Events, Handlers

### Infrastructure & HTTP
- **[Infrastructure](infrastructure.md)** - Repositories, Entities, Models, Mappers
- **[HTTP Layer](http-layer.md)** - Controllers, Routers, Request/Response patterns

## Quick Reference by Task

### Adding New Feature
1. Read: [Critical Rules](critical-rules.md) → Database Performance + CQRS
2. Read: [Architecture](architecture.md) → DDD section
3. Design: Define entities, commands, queries first

### Creating New Query
1. Read: [Application Layer](application-layer.md) → Queries section
2. Read: [Critical Rules](critical-rules.md) → Performance rules

### Creating New Command
1. Read: [Application Layer](application-layer.md) → Commands section
2. Read: [Critical Rules](critical-rules.md) → CQRS rules

### Creating Repository or Entity
1. Read: [Infrastructure](infrastructure.md) → Complete guide
2. Read: [Code Quality](code-quality.md) → Domain Layer

### Creating API Endpoint
1. Read: [HTTP Layer](http-layer.md) → Controller patterns
2. Read: [Critical Rules](critical-rules.md) → Response patterns

## File Structure

```
ai_docs/
├── README.md                    # This file - Documentation index
├── critical-rules.md            # MUST READ - Performance, CQRS, Responses
├── architecture.md              # DDD, Clean Architecture, Bounded Contexts
├── application-layer.md         # Queries, Commands, Events, Handlers
├── infrastructure.md            # Repositories, Entities, Models, Mappers
├── code-quality.md              # SOLID, Naming, Best Practices
└── http-layer.md                # Controllers, Routers, Request/Response
```

## Development Environment

- **Python 3.11+**
- **FastAPI** - Modern async web framework
- **SQLAlchemy** - ORM with async support
- **Alembic** - Database migrations
- **Docker** - Development and deployment
- **PostgreSQL** - Primary database
- **DDD + Clean Architecture** - Framework-agnostic domain in `/src`

## Project Structure

```
/Users/juanmacias/Projects/CareerPython/
├── adapters/                    # HTTP layer (FastAPI)
│   └── http/
│       ├── company_app/         # Company-facing API
│       ├── candidate_app/       # Candidate-facing API
│       └── public_app/          # Public API
├── src/                         # DDD domain layer
│   ├── candidate_bc/            # Candidate bounded context
│   ├── company_bc/              # Company bounded context
│   ├── interview_bc/            # Interview bounded context
│   ├── notification_bc/         # Notification bounded context
│   ├── shared_bc/               # Shared bounded context
│   └── framework/               # Framework utilities
├── core/                        # Application core
│   ├── container.py             # Dependency injection
│   ├── containers/              # Domain-specific containers
│   ├── database.py              # Database configuration
│   └── event_bus.py             # Event dispatching
├── alembic/                     # Database migrations
├── client-vite/                 # React frontend
└── tests/                       # Test suite
```

## Key Commands

```bash
# Start development environment
make start

# Stop environment
make stop

# Run database migrations
make migrate

# Create new migration
make revision m="migration message"

# Run type checking
make mypy

# Run tests
make test

# Run linter
make linter
```

---

**Note:** This documentation is optimized for AI consumption and reflects the current state of this recruitment platform.
