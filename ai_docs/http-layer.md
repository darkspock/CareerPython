# HTTP Layer

Complete guide to Controllers, Routers, Request/Response patterns in FastAPI.

## Overview

The HTTP Layer contains:
- **Routers** - FastAPI route definitions
- **Controllers** - Business orchestration using Command/Query bus
- **Schemas** - Pydantic request/response models (simple, no magic)
- **Mappers** - Explicit DTO → Response conversion

---

## Layer Structure

```
adapters/http/
├── company_app/               # Company-facing API
│   └── {domain}/
│       ├── controllers/       # Business orchestration
│       ├── routers/           # FastAPI routes
│       ├── schemas/           # Pydantic request/response models
│       └── mappers/           # DTO → Response mappers
├── candidate_app/             # Candidate-facing API
└── public_app/                # Public API
```

---

## Routers

### Router Location

Located in: `adapters/http/{app}/{domain}/routers/` or `presentation/routers/`

### Router Structure

```python
from fastapi import APIRouter, Depends, HTTPException, status
from dependency_injector.wiring import inject, Provide

router = APIRouter(
    prefix="/api/candidates",
    tags=["candidates"]
)

@router.get(
    "/{candidate_id}",
    response_model=CandidateResponse,
    summary="Get a candidate by ID"
)
@inject
def get_candidate(
    candidate_id: str,
    controller: CandidateController = Depends(Provide[Container.candidate_controller])
) -> CandidateResponse:
    """Get a candidate by ID"""
    result = controller.get_candidate(candidate_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )
    return result


@router.post(
    "/",
    response_model=CandidateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new candidate"
)
@inject
def create_candidate(
    request: CreateCandidateRequest,
    controller: CandidateController = Depends(Provide[Container.candidate_controller])
) -> CandidateResponse:
    """Create a new candidate"""
    try:
        return controller.create_candidate(request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
```

### Router Rules

1. **Routers define HTTP endpoints** - Routes, methods, status codes
2. **Routers are thin** - Delegate to controllers
3. **Routers handle HTTP concerns** - Status codes, error responses
4. **Routers use dependency injection** - `@inject` decorator

---

## Controllers

### Controller Location

Located in: `adapters/http/{app}/{domain}/controllers/` or `presentation/controllers/`

### Controller Structure

```python
from typing import Optional, List

class CandidateController:
    """Controller for candidate operations"""

    def __init__(
        self,
        command_bus: CommandBus,
        query_bus: QueryBus
    ):
        self.command_bus = command_bus
        self.query_bus = query_bus

    def get_candidate(self, candidate_id: str) -> CandidateResponse:
        """Get a candidate by ID"""
        # 1. Execute query (returns DTO with Value Objects)
        dto: Optional[CandidateDto] = self.query_bus.query(
            GetCandidateByIdQuery(id=CandidateId(candidate_id))
        )

        if not dto:
            raise CandidateNotFoundException(candidate_id)

        # 2. Convert DTO to Response via explicit Mapper
        return CandidateMapper.dto_to_response(dto)

    def create_candidate(self, request: CreateCandidateRequest) -> CandidateResponse:
        """Create a new candidate"""
        # 1. Generate ID before command (as ValueObject)
        candidate_id = CandidateId.generate()

        # 2. Execute command (returns None)
        self.command_bus.execute(
            CreateCandidateCommand(
                id=candidate_id,
                name=request.name,
                email=request.email
            )
        )

        # 3. Query to get created entity
        dto = self.query_bus.query(
            GetCandidateByIdQuery(id=candidate_id)
        )

        # 4. Convert to response via explicit Mapper
        return CandidateMapper.dto_to_response(dto)

    def update_candidate(
        self,
        candidate_id: str,
        request: UpdateCandidateRequest
    ) -> CandidateResponse:
        """Update a candidate"""
        id = CandidateId(candidate_id)

        # 1. Execute command
        self.command_bus.execute(
            UpdateCandidateCommand(
                id=id,
                name=request.name,
                email=request.email
            )
        )

        # 2. Query updated entity
        dto = self.query_bus.query(
            GetCandidateByIdQuery(id=id)
        )

        # 3. Convert to response via explicit Mapper
        return CandidateMapper.dto_to_response(dto)

    def list_candidates(self, company_id: str) -> List[CandidateResponse]:
        """List all candidates for a company"""
        # 1. Execute query
        dtos = self.query_bus.query(
            ListCandidatesByCompanyQuery(company_id=CompanyId(company_id))
        )

        # 2. Convert to responses via Mapper
        return CandidateMapper.dto_list_to_response(dtos)
```

### Controller Rules

1. **Controllers orchestrate** - Command/Query bus calls only
2. **Controllers use Mappers** - For DTO → Response conversion (explicit)
3. **Controllers don't access repositories** - Use query/command bus
4. **Controllers don't contain business logic** - Just orchestration

### ❌ PROHIBITED in Controllers

```python
# ❌ WRONG - Direct repository access
def get_candidate(self, candidate_id: str):
    return self.repository.get_by_id(candidate_id)

# ❌ WRONG - Business logic
def create_candidate(self, request):
    if not request.email or "@" not in request.email:
        raise ValidationError()

# ❌ WRONG - Direct database access
def get_candidate(self, candidate_id: str):
    result = self.session.execute(text("SELECT * FROM candidates"))

# ❌ WRONG - Magic/implicit conversion
def get_candidate(self, candidate_id: str):
    dto = self.query_bus.query(query)
    return CandidateResponse.model_validate(dto)  # Implicit - use Mapper instead
```

### ✅ CORRECT Pattern

```python
def get_candidate(self, candidate_id: str) -> CandidateResponse:
    dto = self.query_bus.query(GetCandidateByIdQuery(id=CandidateId(candidate_id)))
    if not dto:
        raise CandidateNotFoundException(candidate_id)
    return CandidateMapper.dto_to_response(dto)  # Explicit conversion
```

---

## Request Schemas

### Request Location

Located in: `adapters/http/{app}/{domain}/schemas/` or `presentation/schemas/`

### Request Structure

```python
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class CreateCandidateRequest(BaseModel):
    """Request schema for creating a candidate"""
    name: str = Field(..., min_length=2, max_length=255)
    email: EmailStr = Field(...)
    phone: Optional[str] = Field(None, max_length=20)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john@example.com",
                "phone": "+1234567890"
            }
        }


class UpdateCandidateRequest(BaseModel):
    """Request schema for updating a candidate"""
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    email: Optional[EmailStr] = Field(None)
    phone: Optional[str] = Field(None, max_length=20)
```

### Request Rules

1. **Use Pydantic BaseModel** - For validation
2. **Use Field for constraints** - `min_length`, `max_length`, etc.
3. **Use appropriate types** - `EmailStr`, `Optional`, etc.
4. **Add examples** - For OpenAPI documentation

---

## Response Schemas

### Response Location

Located in: `adapters/http/{app}/{domain}/schemas/`

### Response Structure (Simple, No Magic)

**IMPORTANT:** Response schemas are simple Pydantic models. No `field_validator`, no `ConfigDict`. The Mapper handles all conversion.

```python
from typing import Optional
from pydantic import BaseModel

class CandidateResponse(BaseModel):
    """Response schema for candidate data - simple, explicit"""
    id: str
    name: str
    email: str
    status: str
    created_at: str
    updated_at: Optional[str] = None
```

### Response Rules

1. **Use primitives only** - `str`, `int`, `bool` (not ValueObjects)
2. **No field_validators** - Mapper handles conversion
3. **No ConfigDict** - Not needed without model_validate()
4. **Simple and explicit** - Just data structure
5. **No business logic** - Just data representation

---

## Mappers

This codebase uses **two types of Mappers**:
1. **DtoMapper** (Application layer) - Entity → DTO
2. **ResponseMapper** (Presentation layer) - DTO → Response

### Conversion Flow

```
Entity → DtoMapper → DTO (with Value Objects) → ResponseMapper → Response (primitives)
```

---

### DtoMapper (Entity → DTO)

**Location:** `application/queries/shared/`

```python
class CandidateDtoMapper:
    """Mapper for Entity to DTO conversion"""

    @staticmethod
    def from_model(candidate: Candidate) -> CandidateDto:
        """Convert Candidate entity to CandidateDto"""
        return CandidateDto(
            id=candidate.id,           # Keep as ValueObject
            name=candidate.name,
            email=candidate.email,
            status=candidate.status,   # Keep as Enum
            created_at=candidate.created_at,
            updated_at=candidate.updated_at
        )
```

**Rules:**
- Located in **application layer**
- Keep Value Objects and Enums (don't serialize)
- Used in QueryHandlers

---

### ResponseMapper (DTO → Response)

**Location:** `adapters/http/{app}/{domain}/mappers/` or `presentation/mappers/`

```python
class CandidateMapper:
    """Mapper for DTO to Response conversion - EXPLICIT"""

    @staticmethod
    def dto_to_response(dto: CandidateDto) -> CandidateResponse:
        """Convert CandidateDto to CandidateResponse"""
        return CandidateResponse(
            id=str(dto.id.value),              # ValueObject → string
            name=dto.name,
            email=dto.email,
            status=dto.status.value,           # Enum → string
            created_at=dto.created_at.isoformat(),  # datetime → ISO string
            updated_at=dto.updated_at.isoformat() if dto.updated_at else None
        )

    @staticmethod
    def dto_list_to_response(dtos: List[CandidateDto]) -> List[CandidateResponse]:
        """Convert list of DTOs to list of Responses"""
        return [CandidateMapper.dto_to_response(dto) for dto in dtos]
```

**Rules:**
- Located in **presentation layer**
- Converts Value Objects to primitives (explicit)
- Converts Enums to strings (explicit)
- Converts datetimes to ISO strings (explicit)
- Used in Controllers

---

### Usage Example

```python
# In QueryHandler (application layer):
candidate = self.candidate_repository.get_by_id(query.id)
return CandidateDtoMapper.from_model(candidate)  # Entity → DTO

# In Controller (presentation layer):
dto = self.query_bus.query(query)
return CandidateMapper.dto_to_response(dto)  # DTO → Response (explicit)
```

---

## Error Handling

### HTTP Exception Handling

```python
from fastapi import HTTPException, status

@router.get("/{candidate_id}")
@inject
def get_candidate(candidate_id: str, controller: CandidateController):
    try:
        result = controller.get_candidate(candidate_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Candidate not found"
            )
        return result
    except CandidateNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except InvalidEmailError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
```

### Global Exception Handler

```python
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(CandidateNotFoundException)
async def candidate_not_found_handler(request: Request, exc: CandidateNotFoundException):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)}
    )

@app.exception_handler(InvalidEmailError)
async def invalid_email_handler(request: Request, exc: InvalidEmailError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )
```

---

## Dependency Injection

### Container Registration

```python
# core/containers/candidate_container.py
from dependency_injector import containers, providers

class CandidateContainer(containers.DeclarativeContainer):
    # Repositories
    candidate_repository = providers.Factory(
        CandidateRepository,
        session=session
    )

    # Query Handlers
    get_candidate_query_handler = providers.Factory(
        GetCandidateByIdQueryHandler,
        repository=candidate_repository
    )

    # Command Handlers
    create_candidate_command_handler = providers.Factory(
        CreateCandidateCommandHandler,
        repository=candidate_repository,
        event_bus=event_bus
    )

    # Controllers
    candidate_controller = providers.Factory(
        CandidateController,
        command_bus=command_bus,
        query_bus=query_bus
    )
```

### Using Dependencies in Routers

```python
from dependency_injector.wiring import inject, Provide

@router.get("/{candidate_id}")
@inject
def get_candidate(
    candidate_id: str,
    controller: CandidateController = Depends(Provide[Container.candidate_controller])
) -> CandidateResponse:
    return controller.get_candidate(candidate_id)
```

---

## Complete Flow Example

### 1. Router (HTTP Entry Point)

```python
@router.post("/", response_model=CandidateResponse, status_code=201)
@inject
def create_candidate(
    request: CreateCandidateRequest,
    controller: CandidateController = Depends(Provide[Container.candidate_controller])
) -> CandidateResponse:
    return controller.create_candidate(request)
```

### 2. Controller (Orchestration)

```python
def create_candidate(self, request: CreateCandidateRequest) -> CandidateResponse:
    # Generate ID as ValueObject
    candidate_id = CandidateId.generate()

    self.command_bus.execute(
        CreateCandidateCommand(
            id=candidate_id,
            name=request.name,
            email=request.email
        )
    )

    dto = self.query_bus.query(
        GetCandidateByIdQuery(id=candidate_id)
    )

    return CandidateMapper.dto_to_response(dto)  # Explicit conversion
```

### 3. Command Handler (Business Logic)

```python
# In application/commands/create_candidate.py (same file as command)
def execute(self, command: CreateCandidateCommand) -> None:
    candidate = Candidate.create(
        id=command.id,
        name=command.name,
        email=command.email
    )
    self.candidate_repository.save(candidate)
```

### 4. Query Handler (Data Retrieval)

```python
# In application/queries/get_candidate_by_id.py (same file as query)
def handle(self, query: GetCandidateByIdQuery) -> Optional[CandidateDto]:
    candidate = self.candidate_repository.get_by_id(query.id)
    if candidate:
        return CandidateDtoMapper.from_model(candidate)  # Entity → DTO
    return None
```

### 5. DtoMapper (Entity → DTO)

```python
# In application/queries/shared/candidate_dto_mapper.py
@staticmethod
def from_model(candidate: Candidate) -> CandidateDto:
    return CandidateDto(
        id=candidate.id,        # Keep as ValueObject
        name=candidate.name,
        status=candidate.status, # Keep as Enum
        created_at=candidate.created_at
    )
```

### 6. ResponseMapper (DTO → Response)

```python
# In presentation/mappers/candidate_mapper.py
@staticmethod
def dto_to_response(dto: CandidateDto) -> CandidateResponse:
    return CandidateResponse(
        id=str(dto.id.value),           # Explicit: ValueObject → string
        name=dto.name,
        status=dto.status.value,        # Explicit: Enum → string
        created_at=dto.created_at.isoformat()  # Explicit: datetime → string
    )
```

### 7. Response Schema (Simple)

```python
# In adapters/http/{app}/schemas/candidate.py
class CandidateResponse(BaseModel):
    id: str
    name: str
    status: str
    created_at: str
    # No magic - just data structure
```

---

## Checklist Before Creating Endpoint

- [ ] Router defined with correct prefix and tags
- [ ] Controller method created using Command/Query bus
- [ ] Request schema defined with validation
- [ ] Response schema defined (simple, primitives only)
- [ ] ResponseMapper created for DTO → Response (in presentation layer)
- [ ] DtoMapper created for Entity → DTO (in application layer)
- [ ] Query + Handler in same file
- [ ] Command + Handler in same file
- [ ] Dependencies registered in container
- [ ] Error handling in place
- [ ] OpenAPI documentation (summary, description, examples)

---

**See also:**
- [Architecture](architecture.md) - Overall architecture
- [Application Layer](application-layer.md) - Queries and Commands
- [Infrastructure](infrastructure.md) - Repositories
- [Critical Rules](critical-rules.md) - Controller rules
