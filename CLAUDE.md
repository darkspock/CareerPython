# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CareerPython is a career management platform with a FastAPI backend implementing Clean Architecture and SOLID principles, 
paired with a Next.js TypeScript frontend.

La documentación de negocio está en ./BUSINESS.md
El modelo de datos está en ./DATA_MODEL.md


## Development Commands

### Backend (Python/FastAPI)
```bash
# Start development environment
make start

# Stop environment  
make stop

# View logs
make logs

# Run database migrations
make migrate

# Create new migration
make revision m="migration message"

# Build containers
make build

# Run tests
make test

# Access container bash
make bash

# Local development with uv
uv venv                    # Create virtual environment
uv pip install -r pyproject.toml  # Install dependencies
make rebuild-venv          # Rebuild local venv
```

### Frontend (React with Vue)

UI framework https://base-ui.com/llms.txt

```bash
cd client
npm run dev     # Start development server
npm run build   # Build for production
npm run start   # Start production server
npm run lint    # Run ESLint
```

#### Environment Configuration
- Copy `.env.example` to `.env.local` and configure API URL
- For development: `NEXT_PUBLIC_API_URL=http://localhost:8000`
- For production: `NEXT_PUBLIC_API_URL=https://api.yourdomain.com`

#### API Client
- Use `@/lib/api` for all API calls instead of hardcoded URLs
- Example: `api.createAccountFromLanding(formData)` instead of direct fetch

### Testing
- Backend tests: `make test` (runs test_solid_architecture.py)
- Test files located in `tests/` directory
- Uses pytest framework

## Architecture

### Clean Architecture Structure
The backend follows Clean Architecture with clear separation of concerns:

```
src/
├── [domain]/                    # Business domains (candidate, user, interview, menu)
│   ├── application/
│   │   ├── commands/           # Write operations (CQRS)
│   │   ├── queries/            # Read operations (CQRS)
│   │   └── handlers/           # Event handlers
│   ├── domain/
│   │   ├── entities/           # Core business entities
│   │   ├── enums/              # Domain enums
│   │   ├── events.py           # Domain events
│   │   └── exceptions/         # Domain-specific exceptions
│   ├── infrastructure/
│   │   ├── models/             # SQLAlchemy ORM models
│   │   └── repositories/       # Data access implementations
│   └── presentation/
│       ├── controllers/        # HTTP controllers
│       └── routers/           # FastAPI routers
```

### Key Architectural Patterns
- **CQRS**: Commands for writes, Queries for reads
- **Event-Driven**: Domain events handled by event bus (core/event_bus.py)
- **Dependency Injection**: Using dependency-injector library (core/container.py)
- **Repository Pattern**: Data access abstraction
- **Domain Events**: Business events published from entities

### CQRS Implementation - MANDATORY INHERITANCE RULES

**CRITICAL**: All Commands, Queries, and their Handlers MUST inherit from base classes. This is MANDATORY for the CommandBus and QueryBus to work correctly.

#### Commands Must Inherit from Command Base Class

**Location**: `src/shared/application/command_bus.py`

```python
from dataclasses import dataclass
from src.framework.application.command_bus import Command, CommandHandler

@dataclass
class CreatePhaseCommand(Command):  # MUST inherit from Command
    """Command to create a new phase"""
    company_id: CompanyId
    name: str
    # ... other fields

class CreatePhaseCommandHandler(CommandHandler[CreatePhaseCommand]):  # MUST inherit from CommandHandler with generic type
    """Handler for CreatePhaseCommand"""

    def __init__(self, repository: PhaseRepositoryInterface):
        self.repository = repository

    def execute(self, command: CreatePhaseCommand) -> None:  # Commands MUST NOT return values
        # Implementation
        pass
```

**Rules**:
- ALL Commands MUST inherit from `Command` base class
- ALL CommandHandlers MUST inherit from `CommandHandler[TCommand]` with the specific command type as generic parameter
- CommandHandler's `execute` method MUST return `None` (no return value)
- Commands are used for write operations and side effects

#### Queries Must Inherit from Query Base Class

**Location**: `src/shared/application/query_bus.py`

```python
from dataclasses import dataclass
from typing import Optional
from src.framework.application.query_bus import Query, QueryHandler

@dataclass
class GetPhaseByIdQuery(Query):  # MUST inherit from Query
    """Query to get a phase by ID"""
    phase_id: PhaseId

class GetPhaseByIdQueryHandler(QueryHandler[GetPhaseByIdQuery, Optional[PhaseDto]]):  # MUST inherit from QueryHandler with query type and return type
    """Handler for GetPhaseByIdQuery"""

    def __init__(self, repository: PhaseRepositoryInterface):
        self.repository = repository

    def handle(self, query: GetPhaseByIdQuery) -> Optional[PhaseDto]:  # Queries MUST return DTOs
        # Implementation
        return dto
```

**Rules**:
- ALL Queries MUST inherit from `Query` base class
- ALL QueryHandlers MUST inherit from `QueryHandler[TQuery, TResult]` with the specific query type and return type as generic parameters
- QueryHandler's `handle` method MUST return a DTO (or List[DTO], Optional[DTO], etc.)
- Queries are used for read operations only

#### Why This is Mandatory

The `CommandBus` and `QueryBus` use automatic handler discovery by convention:
1. They look up handlers by name: `{CommandName}Handler` or `{QueryName}Handler`
2. They rely on type checking to ensure correct handler types
3. Without proper inheritance, the buses cannot find or invoke handlers correctly

**Common Mistakes to Avoid**:
- ❌ `class CreatePhaseCommand:` - Missing `(Command)` inheritance
- ❌ `class CreatePhaseCommandHandler:` - Missing `(CommandHandler[CreatePhaseCommand])` inheritance
- ❌ `class GetPhaseQuery:` - Missing `(Query)` inheritance
- ❌ `class GetPhaseQueryHandler:` - Missing `(QueryHandler[GetPhaseQuery, PhaseDto])` inheritance
- ❌ `def execute(self, command) -> PhaseDto:` - Commands must NOT return values
- ❌ `def handle(self, query) -> Phase:` - Queries must return DTOs, NOT entities

## DDD Layer Communication - MANDATORY PATTERNS

**CRITICAL**: These patterns are MANDATORY and must NEVER be changed. Follow them exactly as specified.

### 1. Repository Pattern (Domain Interface + Infrastructure Implementation)

**Repository Interface Location**: `domain/infrastructure/{entity}_repository_interface.py`
- MUST be an abstract base class (ABC) with @abstractmethod decorators
- MUST define all repository methods as abstract
- MUST return domain entities, NOT models or DTOs

**Repository Implementation Location**: `infrastructure/repositories/{entity}_repository.py`
- MUST implement the interface from domain layer
- MUST convert database models to domain entities
- MUST convert domain entities to database models
- MUST handle all database operations

### 2. Data Flow - STRICT TRANSFORMATION CHAIN

**Database → Entity → DTO → Response**

```
Database Model → Repository → Domain Entity → Query Handler → DTO → Controller → Response Schema
```

**Repository Layer**:
- Input: Database Model
- Output: Domain Entity
- Responsibility: Convert models to entities and vice versa

**Query Handler Layer**:
- Input: Domain Entity (from repository)
- Output: DTO
- Responsibility: Convert entities to DTOs for application consumption

**Controller Layer**:
- Input: DTO (from query handler)
- Output: Response Schema
- Responsibility: Convert DTOs to API response schemas
- MUST use Mapper services for DTO to Response Schema conversion
- Routers must not have logic, just pass and return data to/from controllers

**Mapper Pattern (Mandatory)**:
- Location: `presentation/mappers/{domain}_mapper.py`
- Purpose: Reusable DTO to Response Schema conversion
- MUST be in presentation layer (not in Response Schema classes)
- Controllers MUST use mappers instead of `Response.from_dto()` methods

### 3. Command and Query Patterns

**Commands**:
- MUST NOT return values (void return)
- Handler naming: `{CommandName}CommandHandler`
- Location: `application/commands/{command_name}.py`
- Purpose: Write operations, side effects

**Queries**:
- MUST return DTOs
- DTOs are strict typed, includes valueObjects and Enums
- Handler naming: `{QueryName}QueryHandler`
- Location: `application/queries/{query_name}.py`
- Purpose: Read operations, data retrieval

### 4. Handler Naming Convention

**Command Handlers**:
```python
# Command: CreateInterviewTemplateCommand
# Handler: CreateInterviewTemplateCommandHandler

class CreateInterviewTemplateCommandHandler(CommandHandler[CreateInterviewTemplateCommand]):
    def execute(self, command: CreateInterviewTemplateCommand) -> None:
        # Implementation - NO return value
        pass
```

**Query Handlers**:
```python
# Query: GetInterviewTemplateByIdQuery
# Handler: GetInterviewTemplateByIdQueryHandler

class GetInterviewTemplateByIdQueryHandler(QueryHandler[GetInterviewTemplateByIdQuery, InterviewTemplateDto]):
    def handle(self, query: GetInterviewTemplateByIdQuery) -> InterviewTemplateDto:
        # Implementation - MUST return DTO
        return dto
```

### 5. Bus Implementations - KEEP SIMPLE

**CommandBus and QueryBus**:
- MUST remain simple dispatcher implementations
- NO complex logic in buses
- NO caching or advanced features
- ONLY responsible for routing to appropriate handlers

### 6. Decoupling Strategy

Each layer MUST only know about the layer below it:

```
Controller → Query/Command → Handler → Repository Interface → Repository Implementation → Database Model
```

**Forbidden Direct Dependencies**:
- Controllers MUST NOT directly access repositories
- Handlers MUST NOT directly access database models
- Controllers MUST NOT directly access domain entities
- DTOs MUST NOT be used in domain layer
- Controllers MUST NOT return DTOs directly - must convert DTOs to Response schemas

### 7. Example Implementation Flow

**Read Operation (Query)**:
```python
# 1. Controller receives request
def get_template(template_id: str) -> InterviewTemplateResponse:
    query = GetInterviewTemplateByIdQuery(template_id)
    dto = query_bus.query(query)  # Returns DTO
    return InterviewTemplateResponse.from_dto(dto)  # Converts DTO to Response

# 2. Query Handler
class GetInterviewTemplateByIdQueryHandler:
    def handle(self, query) -> InterviewTemplateDto:
        entity = repository.get_by_id(query.template_id)  # Returns Entity
        return InterviewTemplateDto.from_entity(entity)  # Converts Entity to DTO

# 3. Repository
class InterviewTemplateRepository:
    def get_by_id(self, id) -> InterviewTemplate:
        model = session.query(InterviewTemplateModel).get(id)  # Database Model
        return self._to_domain(model)  # Converts Model to Entity
```

**Write Operation (Command)**:
```python
# 1. Controller receives request
def create_template(request: CreateInterviewTemplateRequest) -> InterviewTemplateResponse:
    command = CreateInterviewTemplateCommand.from_request(request)
    command_bus.execute(command)  # NO return value

    # Separate query to get created entity
    query = GetInterviewTemplateByIdQuery(command.template_id)
    dto = query_bus.query(query)
    return InterviewTemplateMapper.dto_to_response(dto)

# 2. Command Handler
class CreateInterviewTemplateCommandHandler:
    def execute(self, command) -> None:  # NO return value
        entity = InterviewTemplate.create(...)  # Create Entity
        repository.save(entity)  # Save Entity
        # NO return statement
```

### 8. Violation Examples - FORBIDDEN

**❌ Direct repository access in controller**:
```python
def get_template(self, template_id: str):
    return self.repository.get_by_id(template_id)  # FORBIDDEN
```

**❌ Returning values from commands**:
```python
def execute(self, command: CreateTemplateCommand) -> InterviewTemplate:  # FORBIDDEN
    return self.repository.save(entity)
```

**❌ Returning entities from queries**:
```python
def handle(self, query: GetTemplateQuery) -> InterviewTemplate:  # FORBIDDEN
    return self.repository.get_by_id(query.id)
```

**❌ Controllers working with entities**:
```python
def create_template(self, request) -> InterviewTemplate:  # FORBIDDEN
    entity = self.query_bus.query(query)
    return entity
```

**❌ Using from_dto() methods in Response classes**:
```python
def get_template(self, template_id: str) -> InterviewTemplateResponse:
    dto = self.query_bus.query(query)
    return InterviewTemplateResponse.from_dto(dto)  # FORBIDDEN
```

**✅ CORRECT - Using Mapper pattern**:
```python
def get_template(self, template_id: str) -> InterviewTemplateResponse:
    dto = self.query_bus.query(query)
    return InterviewTemplateMapper.dto_to_response(dto)  # CORRECT
```

### 9. Domain Entities

Must include factory methods in entities for creation and updates to encapsulate business logic.
Update always get all attributes. We can split updates into smaller methods is the business logic requires it.
Status is not updatable directly, only through specific methods that encapsulate the logic.
Default values and validations must be handled in the entity factory methods. The constructor should not have default values.
Constructor is only accesible from repositories when hydrating from database. Do not set private properties.

This architecture ensures complete decoupling, testability, and maintainability. DO NOT deviate from these patterns.

### Frontend Structure
- Vite, react  with TypeScript
- User Base UI component library
- Uses App Router
- Tailwind CSS for styling
- React Hook Form for form handling
- i18next for internationalization (en/es)
- Component structure in `src/components/`

## Key Components

### Core Infrastructure
- `core/container.py`: Dependency injection container
- `core/database.py`: Database configuration and base models
- `core/event_bus.py`: Event dispatching system
- `core/config.py`: Environment configuration with Pydantic

### Domain Modules
- **Candidate**: Job applicant management with education, experience, projects
- **User**: User authentication and management  
- **Interview**: Interview templates and answers
- **Profile**: Dynamic profile system with event-driven updates
- **Staff**: Staff management functionality

### Database
- PostgreSQL with SQLAlchemy ORM
- Alembic for migrations
- Models in `infrastructure/models/` directories
- Database URL configured via environment variables

## Environment Setup

### Required Environment Variables
Create `.env` file with:
```
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password  
POSTGRES_DB=your_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
SECRET_KEY=your_secret_key
```

### Command Execution Best Practices

**IMPORTANT**: Always use Makefile commands when available. DO NOT use docker directly or call python commands directly.

**Priority order for command execution**:
1. **First priority**: Use Makefile commands when available
2. **Second priority**: Use `uv run` for Python commands if Makefile command doesn't exist
3. **Last resort**: Direct docker commands (avoid unless necessary)

**Common Makefile commands**:
- `make mypy` - Run type checking with mypy
- `make test` - Run tests
- `make lint` - Run linter
- `make flake8` - Run flake8 linter
- `make format` - Format code
- `make migrate` - Run database migrations
- `make revision m="message"` - Create new migration

**Examples**:
```bash
# ✅ CORRECT - Use Makefile
make mypy
make test
make lint

# ❌ WRONG - Don't use docker directly
docker-compose exec web mypy ...

# ❌ WRONG - Don't call python directly
python -m mypy ...
```

### Docker Setup
- Backend runs on port 8000 (mapped from container port 80)
- PostgreSQL on port 5432
- Frontend development on port 3000
- All services defined in docker-compose.yml

## Development Guidelines

### Code Organization
- Follow existing domain structure when adding new features
- Use dependency injection for all services
- Implement both command and query sides for CQRS
- Add domain events for cross-domain communications
- Keep presentation layer thin, business logic in domain/application layers

### Event System
- Publish domain events from entities when state changes occur
- Handle events in application/handlers/ directories
- Register event handlers in core/container.py
- Use EventBus.dispatch() to publish events

### Database Changes
- Always create migrations with `make revision m="description"`
- Run migrations with `make migrate`
- Model changes go in infrastructure/models/
- Keep domain entities separate from ORM models

### Frontend Development
- Components should be in appropriate directories under src/
- Use TypeScript for all new code
- Follow existing patterns for API communication
- Maintain i18n support for new features
- Use enum_controller for retrieving enums