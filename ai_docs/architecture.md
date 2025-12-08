# Architecture

Complete guide to DDD (Domain-Driven Design) and Clean Architecture.

## Overview

This project follows **DDD** with **Clean Architecture** principles:

- **Framework-agnostic domain layer**
- Location: `/src` folder
- Follows Hexagonal Architecture
- Modern, clean Python code
- FastAPI as infrastructure framework

## Clean Architecture Structure

### Folder Structure:
```
src/
├── {bounded_context}_bc/
│   ├── {domain}/
│   │   ├── application/
│   │   │   ├── commands/         # Write operations (CQRS)
│   │   │   ├── queries/          # Read operations (CQRS)
│   │   │   ├── handlers/         # Event handlers
│   │   │   └── dtos/             # Data Transfer Objects
│   │   ├── domain/
│   │   │   ├── entities/         # Core business entities
│   │   │   ├── value_objects/    # Immutable values
│   │   │   ├── enums/            # Domain enumerations
│   │   │   ├── events/           # Domain events
│   │   │   ├── exceptions/       # Domain-specific exceptions
│   │   │   └── interfaces/       # Repository interfaces (ports)
│   │   └── infrastructure/
│   │       ├── models/           # SQLAlchemy ORM models
│   │       └── repositories/     # Repository implementations (adapters)

adapters/http/                    # HTTP Layer (Presentation)
├── {app}/                        # company_app, candidate_app, admin_app, public_app
│   └── {feature}/                # Feature folders (candidate, interview, job_position, etc.)
│       ├── controllers/          # HTTP controllers (may query multiple BCs)
│       ├── routers/              # FastAPI routers
│       ├── schemas/              # Request/Response Pydantic models
│       └── mappers/              # DTO to Response mappers
```

### Key Concepts:

#### Domain Layer
- **Business logic center**
- No external dependencies
- Pure business rules
- Framework-agnostic

#### Ports (Interfaces)
- Interfaces to outside world
- Defined in Domain layer
- Example: `CandidateRepositoryInterface`

#### Adapters (Implementations)
- Specific implementations of ports
- Located in Infrastructure layer
- Example: `CandidateRepository implements CandidateRepositoryInterface`

#### Application Layer (CQRS)
- Communicates domain with infrastructure
- Queries: Read operations (return DTOs)
- Commands: Write operations (return None)
- Handlers: Event handlers

#### Presentation Layer (HTTP Adapters)
- Located in `adapters/http/` (NOT in `src/{bc}/presentation/`)
- FastAPI controllers and routers
- Call Application layer (Queries/Commands)
- Transform DTOs to Response schemas using Mappers

---

## Bounded Contexts

### Current Bounded Contexts:

```
src/
├── candidate_bc/              # Candidate management
│   └── candidate/             # Candidate domain
│
├── company_bc/                # Company management
│   ├── company/               # Company domain
│   ├── company_user/          # Company users
│   ├── company_candidate/     # Company-candidate relationships
│   ├── candidate_stage/       # Stage management
│   └── job_position/          # Job positions
│
├── interview_bc/              # Interview management
│   ├── interview/             # Interview domain
│   └── interview_template/    # Interview templates
│
├── notification_bc/           # Notifications
│   └── notification/          # Email, SMS, etc.
│
├── shared_bc/                 # Shared/cross-cutting
│   └── customization/         # Field validation, etc.
│
└── framework/                 # Framework utilities
    ├── application/           # Base command/query classes
    ├── domain/                # Base entity, value objects
    └── infrastructure/        # Base repository, services
```

### Communication Between Bounded Contexts

#### Primary Method: Query and Command Bus
```python
# From one BC, get data from another BC
candidate = self.query_bus.query(GetCandidateByIdQuery(candidate_id))

# Trigger action in another BC
self.command_bus.execute(SendNotificationCommand(notification_data))
```

### What Can Leave a BC

#### ❌ Cannot Leave (Stay within BC):
- **Repositories** - Data access must stay internal
- **Entities** - Business entities are BC-specific
- **Domain Services** - Business logic stays internal

#### ✅ Can Leave (Can be shared):
- **Simple ValueObjects** - Example: `CandidateId`, `CompanyId`
- **Enums** - Example: `CandidateStatus`, `InterviewStatus`

**Reasoning:** Simple, stable objects can be shared. Complex, evolving ones cannot.

---

## HTTP Layer - Controllers (CRITICAL)

### Controllers Are Thin Orchestrators

**Controllers should have MAX 3 responsibilities:**
1. **Parse request** - Extract data from request
2. **Dispatch Command/Query** - Delegate to Application layer
3. **Return response** - Convert DTO to Response via Mapper

### ❌ PROHIBITED in Controllers

**NEVER do these in Controllers:**

#### 1. NO Direct Database Access
```python
# ❌ WRONG
def get_candidate(self, candidate_id: str):
    result = self.session.execute(text("SELECT * FROM candidates"))
```

#### 2. NO Business Logic
```python
# ❌ WRONG - Validation logic
if not email and not phone:
    raise ValidationException()

# ❌ WRONG - Loops and processing
for candidate in candidates:
    # processing...

# ❌ WRONG - Calculations
total = price * quantity * (1 + tax_rate)
```

#### 3. NO Direct Repository Access
```python
# ❌ WRONG
def get_candidate(self, candidate_id: str):
    return self.repository.get_by_id(candidate_id)
```

### ✅ CORRECT Controller Pattern

```python
class CandidateController:
    def __init__(
        self,
        command_bus: CommandBus,
        query_bus: QueryBus
    ):
        self.command_bus = command_bus
        self.query_bus = query_bus

    def get_candidate(self, candidate_id: str) -> CandidateResponse:
        # 1. Query
        dto = self.query_bus.query(
            GetCandidateByIdQuery(candidate_id=candidate_id)
        )

        # 2. Return via Mapper
        return CandidateMapper.dto_to_response(dto)

    def create_candidate(self, request: CreateCandidateRequest) -> CandidateResponse:
        # 1. Generate ID
        candidate_id = CandidateId.generate()

        # 2. Dispatch command (no return value)
        self.command_bus.execute(
            CreateCandidateCommand(
                candidate_id=candidate_id,
                name=request.name,
                email=request.email
            )
        )

        # 3. Query to get created entity
        dto = self.query_bus.query(
            GetCandidateByIdQuery(candidate_id=candidate_id)
        )

        # 4. Return via Mapper
        return CandidateMapper.dto_to_response(dto)
```

### Where Does Logic Go?

| What | Where | Why |
|------|-------|-----|
| Validation (email required) | Handler or Entity | Business rule |
| Duplicate checking | Repository | Data access logic |
| Loop through items | Handler | Processing logic |
| Insert to database | Repository | Data access |
| Publish events | Handler | Application orchestration |

---

## Layered Dependencies

```
HTTP Layer (FastAPI Controllers/Routers)
    ↓ depends on
Application Layer (Queries, Commands, Handlers)
    ↓ depends on
Domain Layer (Entities, Value Objects, Business Rules)
    ↑ defines interfaces for
Infrastructure Layer (Repositories, External Services)
```

**Key Rule:** Domain layer has NO dependencies. Everything depends on it.

---

## Routers vs Controllers

### Routers
- Define HTTP routes and OpenAPI documentation
- Located in `adapters/http/{app}/{feature}/routers/`
- Minimal logic - just route to controllers
- Handle request parsing and response formatting

### Controllers
- Business orchestration
- Located in `adapters/http/{app}/{feature}/controllers/`
- Call Command/Query bus (can query multiple BCs)
- Use Mappers for response conversion

### Example Structure:

```python
# adapters/http/company_app/candidate/routers/candidate_router.py
router = APIRouter(prefix="/api/candidates", tags=["candidates"])

@router.get("/{candidate_id}", response_model=CandidateResponse)
@inject
def get_candidate(
    candidate_id: str,
    controller: CandidateController = Depends(Provide[Container.candidate_controller])
) -> CandidateResponse:
    return controller.get_candidate(candidate_id)
```

```python
# adapters/http/company_app/candidate/controllers/candidate_controller.py
class CandidateController:
    def __init__(self, query_bus: QueryBus, command_bus: CommandBus):
        self.query_bus = query_bus
        self.command_bus = command_bus

    def get_candidate(self, candidate_id: str) -> CandidateResponse:
        # Controller can query multiple BCs via bus
        candidate = self.query_bus.query(GetCandidateByIdQuery(candidate_id))
        interviews = self.query_bus.query(GetInterviewsByCandidateQuery(candidate_id))
        return CandidateMapper.dto_to_response(candidate, interviews)
```

---

## Development Environment

- **Python 3.11+**
- **Docker** - All code runs in Docker
- **PostgreSQL** - Primary database
- **FastAPI** - Modern async framework
- **SQLAlchemy** - ORM with async support

---

## Architecture Decision Guidelines

### When to Use Full DDD:
- New domain with complex business rules
- Long-term maintainability critical
- Clear bounded context boundaries

### Before Creating New Domain:
1. Identify domain boundaries
2. Define entities, value objects
3. Design commands and queries
4. Identify domain events
5. **Only then start coding**

---

**See also:**
- [Critical Rules](critical-rules.md) - Performance and CQRS rules
- [Application Layer](application-layer.md) - CQRS implementation
- [Infrastructure](infrastructure.md) - Repositories and entities
- [Code Quality](code-quality.md) - SOLID principles
