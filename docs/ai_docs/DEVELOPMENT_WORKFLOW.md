# Development Workflow - CareerPython

Este documento describe el workflow estándar para implementar nuevos módulos o features en CareerPython.

## Filosofía de Desarrollo

El proyecto sigue **Clean Architecture** y **Domain-Driven Design (DDD)** con separación estricta de capas:

```
Domain Layer (Entities, Value Objects, Business Logic)
    ↓
Application Layer (Use Cases, Commands, Queries, DTOs)
    ↓
Infrastructure Layer (Repositories, Database, External Services)
    ↓
Presentation Layer (Controllers, Routers, Schemas)
```

## Proceso de Implementación en 3 Fases

### Fase 1: Domain Layer - Entidades y Lógica de Negocio

**Objetivo**: Crear la representación del negocio sin preocuparse por persistencia o presentación.

#### 1.1. Enums

Ubicación: `src/{module}/domain/enums/`

```python
from enum import Enum

class CompanyStatus(str, Enum):
    """Estados de una empresa"""
    ACTIVE = "active"
    SUSPENDED = "suspended"
    DELETED = "deleted"
```

**Características**:
- Heredar de `str, Enum`
- Documentar cada enum
- Valores en minúsculas con underscores

#### 1.2. Value Objects

Ubicación: `src/{module}/domain/value_objects/`

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class CompanyId:
    """Identificador único de empresa"""
    value: str

    def __post_init__(self):
        if not self.value:
            raise ValueError("CompanyId no puede estar vacío")

    def __str__(self) -> str:
        return self.value
```

**Características**:
- Inmutables (`frozen=True`)
- Encapsulan validaciones
- Representan conceptos del dominio
- Métodos de comparación y conversión

#### 1.3. Entidades

Ubicación: `src/{module}/domain/entities/`

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Company:
    """Entidad de dominio Company"""
    id: CompanyId
    name: str
    domain: str
    logo_url: Optional[str]
    status: CompanyStatus
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        name: str,
        domain: str,
        logo_url: Optional[str] = None,
        id: Optional[CompanyId] = None,
    ) -> "Company":
        """Factory method para crear nueva empresa"""
        # Validaciones de negocio
        if not name or len(name) < 3:
            raise ValueError("El nombre debe tener al menos 3 caracteres")

        if not domain or "@" in domain:
            raise ValueError("El dominio no es válido")

        # Valores por defecto
        now = datetime.now()
        company_id = id or CompanyId(str(uuid4()))

        return cls(
            id=company_id,
            name=name,
            domain=domain,
            logo_url=logo_url,
            status=CompanyStatus.ACTIVE,
            created_at=now,
            updated_at=now,
        )

    def update(
        self,
        name: str,
        domain: str,
        logo_url: Optional[str],
    ) -> "Company":
        """Actualiza la empresa con nuevos valores"""
        # Validaciones
        if not name or len(name) < 3:
            raise ValueError("El nombre debe tener al menos 3 caracteres")

        # Retorna nueva instancia (inmutabilidad)
        return Company(
            id=self.id,
            name=name,
            domain=domain,
            logo_url=logo_url,
            status=self.status,
            created_at=self.created_at,
            updated_at=datetime.now(),
        )

    def suspend(self, reason: Optional[str] = None) -> "Company":
        """Suspende la empresa"""
        if self.status == CompanyStatus.DELETED:
            raise ValueError("No se puede suspender una empresa eliminada")

        return Company(
            id=self.id,
            name=self.name,
            domain=self.domain,
            logo_url=self.logo_url,
            status=CompanyStatus.SUSPENDED,
            created_at=self.created_at,
            updated_at=datetime.now(),
        )

    def activate(self) -> "Company":
        """Activa la empresa"""
        if self.status == CompanyStatus.DELETED:
            raise ValueError("No se puede activar una empresa eliminada")

        return Company(
            id=self.id,
            name=self.name,
            domain=self.domain,
            logo_url=self.logo_url,
            status=CompanyStatus.ACTIVE,
            created_at=self.created_at,
            updated_at=datetime.now(),
        )

    def delete(self) -> "Company":
        """Marca la empresa como eliminada (soft delete)"""
        return Company(
            id=self.id,
            name=self.name,
            domain=self.domain,
            logo_url=self.logo_url,
            status=CompanyStatus.DELETED,
            created_at=self.created_at,
            updated_at=datetime.now(),
        )
```

**Reglas de Entidades**:
1. **Constructor sin valores por defecto**: Todos los parámetros requeridos en `__init__`
2. **Propiedades públicas**: No usar `@property` ni getters/setters privados
3. **Factory method `create()`**: Con valores por defecto y validaciones
4. **Factory method `update()`**: Recibe TODOS los atributos actualizables
5. **Métodos específicos para status**: Un método por cada transición de estado
6. **Inmutabilidad**: Los métodos retornan nuevas instancias
7. **Validaciones en métodos**: Lógica de negocio encapsulada

**❌ NO HACER**:
```python
# Mal: Cambio directo de status
company.status = CompanyStatus.SUSPENDED

# Mal: Getters/Setters
@property
def name(self):
    return self._name

def set_name(self, name):
    self._name = name

# Mal: Valores por defecto en constructor
def __init__(self, id, name, status=CompanyStatus.ACTIVE):
    pass
```

**✅ HACER**:
```python
# Bien: Método específico para cambio de status
company = company.suspend()

# Bien: Propiedades públicas
print(company.name)

# Bien: Factory method con valores por defecto
company = Company.create(name="Acme", domain="acme.com")
```

#### Eventos de Dominio (Opcional)

Si la entidad publica eventos:

```python
from core.events import DomainEvent

@dataclass
class CompanyCreated(DomainEvent):
    company_id: str
    company_name: str

# En el método create():
from core.event_bus import EventBus

company = cls(...)
EventBus.dispatch(CompanyCreated(
    company_id=str(company.id),
    company_name=company.name
))
return company
```

**🛑 FIN DE FASE 1** - Confirmar con el usuario antes de continuar a Fase 2

---

### Fase 2: Infrastructure Layer - Persistencia

**Objetivo**: Implementar la persistencia de las entidades sin modificar el dominio.

#### 2.1. Interface del Repositorio

Ubicación: `src/{module}/domain/infrastructure/{entity}_repository_interface.py`

```python
from abc import ABC, abstractmethod
from typing import Optional, List
from ..entities.company import Company
from ..value_objects.company_id import CompanyId

class CompanyRepositoryInterface(ABC):
    """Interface del repositorio de Company"""

    @abstractmethod
    def save(self, company: Company) -> None:
        """Guarda o actualiza una empresa"""
        pass

    @abstractmethod
    def get_by_id(self, company_id: CompanyId) -> Optional[Company]:
        """Obtiene una empresa por ID"""
        pass

    @abstractmethod
    def get_by_domain(self, domain: str) -> Optional[Company]:
        """Obtiene una empresa por dominio"""
        pass

    @abstractmethod
    def list_active(self) -> List[Company]:
        """Lista todas las empresas activas"""
        pass

    @abstractmethod
    def delete(self, company_id: CompanyId) -> None:
        """Elimina una empresa"""
        pass
```

**Características**:
- ABC (Abstract Base Class)
- Métodos @abstractmethod
- Trabaja con entidades de dominio
- Ubicada en domain layer (no en infrastructure)

#### 2.2. Modelo SQLAlchemy

Ubicación: `src/{module}/infrastructure/models/{entity}_model.py`

```python
from sqlalchemy import Column, String, DateTime, Enum as SQLEnum
from core.database import Base
from ...domain.enums.company_status import CompanyStatus

class CompanyModel(Base):
    """Modelo de base de datos para Company"""
    __tablename__ = "companies"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    domain = Column(String, unique=True, nullable=False, index=True)
    logo_url = Column(String, nullable=True)
    status = Column(
        SQLEnum(CompanyStatus, native_enum=False, length=20),
        nullable=False,
        default=CompanyStatus.ACTIVE.value
    )
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    # Relaciones
    # users = relationship("CompanyUserModel", back_populates="company")
```

**Características**:
- Hereda de `Base`
- Define `__tablename__`
- Usa tipos de SQLAlchemy
- Convierte enums de dominio a SQL
- Define índices necesarios

#### 2.3. Implementación del Repositorio

Ubicación: `src/{module}/infrastructure/repositories/{entity}_repository.py`

```python
from typing import Optional, List
from sqlalchemy.orm import Session
from ...domain.entities.company import Company
from ...domain.value_objects.company_id import CompanyId
from ...domain.infrastructure.company_repository_interface import CompanyRepositoryInterface
from ..models.company_model import CompanyModel
from ...domain.enums.company_status import CompanyStatus

class CompanyRepository(CompanyRepositoryInterface):
    """Implementación del repositorio de Company"""

    def __init__(self, session: Session):
        self.session = session

    def save(self, company: Company) -> None:
        """Guarda o actualiza una empresa"""
        model = self._to_model(company)
        self.session.merge(model)
        self.session.flush()

    def get_by_id(self, company_id: CompanyId) -> Optional[Company]:
        """Obtiene una empresa por ID"""
        model = self.session.query(CompanyModel).filter(
            CompanyModel.id == str(company_id)
        ).first()
        return self._to_domain(model) if model else None

    def get_by_domain(self, domain: str) -> Optional[Company]:
        """Obtiene una empresa por dominio"""
        model = self.session.query(CompanyModel).filter(
            CompanyModel.domain == domain
        ).first()
        return self._to_domain(model) if model else None

    def list_active(self) -> List[Company]:
        """Lista todas las empresas activas"""
        models = self.session.query(CompanyModel).filter(
            CompanyModel.status == CompanyStatus.ACTIVE
        ).all()
        return [self._to_domain(m) for m in models]

    def delete(self, company_id: CompanyId) -> None:
        """Elimina una empresa"""
        self.session.query(CompanyModel).filter(
            CompanyModel.id == str(company_id)
        ).delete()
        self.session.flush()

    def _to_domain(self, model: CompanyModel) -> Company:
        """Convierte modelo a entidad de dominio"""
        return Company(
            id=CompanyId(model.id),
            name=model.name,
            domain=model.domain,
            logo_url=model.logo_url,
            status=model.status,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _to_model(self, entity: Company) -> CompanyModel:
        """Convierte entidad de dominio a modelo"""
        return CompanyModel(
            id=str(entity.id),
            name=entity.name,
            domain=entity.domain,
            logo_url=entity.logo_url,
            status=entity.status,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
```

**Características**:
- Implementa la interface del dominio
- Recibe Session en constructor
- Métodos `_to_domain()` y `_to_model()` privados
- Convierte entre modelos y entidades
- Nunca expone modelos fuera del repositorio

#### 2.4. Mappers

**Application Mapper** (Entity → DTO)

Ubicación: `src/{module}/application/mappers/{entity}_mapper.py`

```python
from ..dtos.company_dto import CompanyDto
from ...domain.entities.company import Company

class CompanyMapper:
    """Mapper para convertir entidades a DTOs"""

    @staticmethod
    def entity_to_dto(entity: Company) -> CompanyDto:
        """Convierte entidad a DTO"""
        return CompanyDto(
            id=str(entity.id),
            name=entity.name,
            domain=entity.domain,
            logo_url=entity.logo_url,
            status=entity.status.value,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
```

**Presentation Mapper** (DTO → Response)

Ubicación: `src/{module}/presentation/mappers/{entity}_mapper.py`

```python
from ..schemas.company_response import CompanyResponse
from ...application.dtos.company_dto import CompanyDto

class CompanyResponseMapper:
    """Mapper para convertir DTOs a Responses"""

    @staticmethod
    def dto_to_response(dto: CompanyDto) -> CompanyResponse:
        """Convierte DTO a Response"""
        return CompanyResponse(
            id=dto.id,
            name=dto.name,
            domain=dto.domain,
            logo_url=dto.logo_url,
            status=dto.status,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
        )
```

#### 2.5. Migración

```bash
# Crear migración
make revision m="add companies table"

# Revisar archivo generado en migrations/versions/

# Aplicar migración
make migrate
```

**🛑 FIN DE FASE 2** - Confirmar con el usuario antes de continuar a Fase 3

---

### Fase 3: Application & Presentation - API

**Objetivo**: Exponer la funcionalidad a través de endpoints HTTP.

#### 3.1. DTOs (Data Transfer Objects)

Ubicación: `src/{module}/application/dtos/{entity}_dto.py`

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class CompanyDto:
    """DTO para transferir datos de Company"""
    id: str
    name: str
    domain: str
    logo_url: str | None
    status: str
    created_at: datetime
    updated_at: datetime
```

**Características**:
- Dataclass simple
- Tipos primitivos (str, int, datetime)
- No lógica de negocio

#### 3.2. Commands (Escritura)

Ubicación: `src/{module}/application/commands/create_{entity}_command.py`

```python
from dataclasses import dataclass
from typing import Optional
from core.command_bus import Command, CommandHandler
from ...domain.entities.company import Company
from ...domain.infrastructure.company_repository_interface import CompanyRepositoryInterface

@dataclass
class CreateCompanyCommand(Command):
    """Comando para crear una empresa"""
    name: str
    domain: str
    logo_url: Optional[str] = None

class CreateCompanyCommandHandler(CommandHandler[CreateCompanyCommand]):
    """Handler para crear empresa"""

    def __init__(self, repository: CompanyRepositoryInterface):
        self.repository = repository

    def execute(self, command: CreateCompanyCommand) -> None:
        """Ejecuta el comando - NO retorna valor"""
        # Validaciones de negocio adicionales
        existing = self.repository.get_by_domain(command.domain)
        if existing:
            raise ValueError(f"Ya existe una empresa con el dominio {command.domain}")

        # Crear entidad usando factory method
        company = Company.create(
            name=command.name,
            domain=command.domain,
            logo_url=command.logo_url,
        )

        # Persistir
        self.repository.save(company)
```

**Características Commands**:
- Dataclass con datos necesarios
- Handler NO retorna valores (void)
- Usa repositorio a través de interface
- Lógica de negocio en entidad

#### 3.3. Queries (Lectura)

Ubicación: `src/{module}/application/queries/get_{entity}_by_id_query.py`

```python
from dataclasses import dataclass
from typing import Optional
from core.query_bus import Query, QueryHandler
from ..dtos.company_dto import CompanyDto
from ..mappers.company_mapper import CompanyMapper
from ...domain.value_objects.company_id import CompanyId
from ...domain.infrastructure.company_repository_interface import CompanyRepositoryInterface

@dataclass
class GetCompanyByIdQuery(Query):
    """Query para obtener empresa por ID"""
    company_id: str

class GetCompanyByIdQueryHandler(QueryHandler[GetCompanyByIdQuery, Optional[CompanyDto]]):
    """Handler para obtener empresa por ID"""

    def __init__(self, repository: CompanyRepositoryInterface):
        self.repository = repository

    def handle(self, query: GetCompanyByIdQuery) -> Optional[CompanyDto]:
        """Ejecuta la query - retorna DTO"""
        company_id = CompanyId(query.company_id)
        entity = self.repository.get_by_id(company_id)

        if not entity:
            return None

        return CompanyMapper.entity_to_dto(entity)
```

**Características Queries**:
- Dataclass con criterios de búsqueda
- Handler retorna DTOs
- Convierte entidad → DTO usando mapper

#### 3.4. Request Schemas

Ubicación: `src/{module}/presentation/schemas/{entity}_request.py`

```python
from pydantic import BaseModel, Field, validator

class CreateCompanyRequest(BaseModel):
    """Request para crear empresa"""
    name: str = Field(..., min_length=3, max_length=100)
    domain: str = Field(..., min_length=3, max_length=100)
    logo_url: str | None = Field(None, max_length=500)

    @validator('domain')
    def validate_domain(cls, v):
        if '@' in v:
            raise ValueError('El dominio no debe contener @')
        return v.lower()

class UpdateCompanyRequest(BaseModel):
    """Request para actualizar empresa"""
    name: str = Field(..., min_length=3, max_length=100)
    domain: str = Field(..., min_length=3, max_length=100)
    logo_url: str | None = Field(None, max_length=500)
```

#### 3.5. Response Schemas

Ubicación: `src/{module}/presentation/schemas/{entity}_response.py`

```python
from pydantic import BaseModel
from datetime import datetime

class CompanyResponse(BaseModel):
    """Response de empresa"""
    id: str
    name: str
    domain: str
    logo_url: str | None
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

#### 3.6. Controller

Ubicación: `src/{module}/presentation/controllers/{entity}_controller.py`

```python
from typing import Optional
from core.command_bus import CommandBus
from core.query_bus import QueryBus
from ...application.commands.create_company_command import CreateCompanyCommand
from ...application.queries.get_company_by_id_query import GetCompanyByIdQuery
from ..schemas.company_request import CreateCompanyRequest
from ..schemas.company_response import CompanyResponse
from ..mappers.company_mapper import CompanyResponseMapper

class CompanyController:
    """Controller de empresas"""

    def __init__(
        self,
        command_bus: CommandBus,
        query_bus: QueryBus
    ):
        self.command_bus = command_bus
        self.query_bus = query_bus

    def create_company(self, request: CreateCompanyRequest) -> CompanyResponse:
        """Crea una nueva empresa"""
        # Crear comando
        command = CreateCompanyCommand(
            name=request.name,
            domain=request.domain,
            logo_url=request.logo_url,
        )

        # Ejecutar comando (no retorna valor)
        self.command_bus.dispatch(command)

        # Query separado para obtener la empresa creada
        # (en producción, el command podría retornar el ID)
        query = GetCompanyByIdQuery(company_id=command.company_id)
        dto = self.query_bus.query(query)

        # Convertir DTO a Response usando mapper
        return CompanyResponseMapper.dto_to_response(dto)

    def get_company(self, company_id: str) -> Optional[CompanyResponse]:
        """Obtiene una empresa por ID"""
        query = GetCompanyByIdQuery(company_id=company_id)
        dto = self.query_bus.query(query)

        if not dto:
            return None

        return CompanyResponseMapper.dto_to_response(dto)
```

**Características**:
- Orquesta Commands y Queries
- Usa CommandBus y QueryBus
- Usa mappers para conversiones
- NO lógica de negocio

#### 3.7. Router

Ubicación: `src/{module}/presentation/routers/{entity}_router.py`

```python
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
from ..controllers.company_controller import CompanyController
from ..schemas.company_request import CreateCompanyRequest, UpdateCompanyRequest
from ..schemas.company_response import CompanyResponse
from core.dependencies import get_company_controller

router = APIRouter(prefix="/companies", tags=["companies"])

@router.post(
    "",
    response_model=CompanyResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear empresa"
)
def create_company(
    request: CreateCompanyRequest,
    controller: CompanyController = Depends(get_company_controller)
) -> CompanyResponse:
    """Crea una nueva empresa"""
    try:
        return controller.create_company(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get(
    "/{company_id}",
    response_model=CompanyResponse,
    summary="Obtener empresa"
)
def get_company(
    company_id: str,
    controller: CompanyController = Depends(get_company_controller)
) -> CompanyResponse:
    """Obtiene una empresa por ID"""
    result = controller.get_company(company_id)
    if not result:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    return result
```

**Características**:
- Define endpoints HTTP
- Valida requests con Pydantic
- Maneja excepciones
- Usa dependency injection
- NO lógica, solo paso de datos

#### 3.8. Registrar en Container

Ubicación: `core/container.py`

```python
from dependency_injector import containers, providers
from company.infrastructure.repositories.company_repository import CompanyRepository
from company.application.commands.create_company_command import CreateCompanyCommandHandler
from company.application.queries.get_company_by_id_query import GetCompanyByIdQueryHandler
from company.presentation.controllers.company_controller import CompanyController

class Container(containers.DeclarativeContainer):
    # ... existing code ...

    # Repositories
    company_repository = providers.Factory(
        CompanyRepository,
        session=database.session
    )

    # Command Handlers
    create_company_handler = providers.Factory(
        CreateCompanyCommandHandler,
        repository=company_repository
    )

    # Query Handlers
    get_company_by_id_handler = providers.Factory(
        GetCompanyByIdQueryHandler,
        repository=company_repository
    )

    # Controllers
    company_controller = providers.Factory(
        CompanyController,
        command_bus=command_bus,
        query_bus=query_bus
    )
```

**✅ FIN DE FASE 3** - Feature completamente implementada

---

## Data Flow Completo

```
1. Cliente hace POST /companies
   ↓
2. Router valida CreateCompanyRequest
   ↓
3. Router llama CompanyController.create_company()
   ↓
4. Controller crea CreateCompanyCommand
   ↓
5. Controller ejecuta command via CommandBus
   ↓
6. CreateCompanyCommandHandler recibe command
   ↓
7. Handler crea entidad Company usando Company.create()
   ↓
8. Handler persiste via CompanyRepository.save()
   ↓
9. Repository convierte Entity → Model y guarda en DB
   ↓
10. Controller ejecuta GetCompanyByIdQuery via QueryBus
   ↓
11. GetCompanyByIdQueryHandler obtiene entity del repositorio
   ↓
12. Handler convierte Entity → DTO usando mapper
   ↓
13. Controller convierte DTO → Response usando mapper
   ↓
14. Router retorna CompanyResponse al cliente
```

## Testing

### Tests Unitarios (Fase 1)

```python
# tests/unit/company/domain/entities/test_company.py

def test_company_create():
    company = Company.create(
        name="Acme Inc",
        domain="acme.com"
    )
    assert company.name == "Acme Inc"
    assert company.status == CompanyStatus.ACTIVE

def test_company_suspend():
    company = Company.create(name="Acme", domain="acme.com")
    suspended = company.suspend()
    assert suspended.status == CompanyStatus.SUSPENDED

def test_cannot_suspend_deleted_company():
    company = Company.create(name="Acme", domain="acme.com")
    deleted = company.delete()
    with pytest.raises(ValueError):
        deleted.suspend()
```

### Tests de Repositorio (Fase 2)

```python
# tests/integration/company/infrastructure/test_company_repository.py

def test_save_and_get_company(db_session):
    repo = CompanyRepository(db_session)
    company = Company.create(name="Acme", domain="acme.com")

    repo.save(company)
    retrieved = repo.get_by_id(company.id)

    assert retrieved is not None
    assert retrieved.name == "Acme"
```

### Tests de API (Fase 3)

```python
# tests/integration/company/presentation/test_company_router.py

def test_create_company(client):
    response = client.post("/companies", json={
        "name": "Acme Inc",
        "domain": "acme.com"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Acme Inc"
    assert data["status"] == "active"
```

## Checklist de Implementación

### Fase 1: Domain
- [ ] Crear enums en `domain/enums/`
- [ ] Crear value objects en `domain/value_objects/`
- [ ] Crear entidades en `domain/entities/`
  - [ ] Constructor sin valores por defecto
  - [ ] Propiedades públicas
  - [ ] Factory method `create()`
  - [ ] Factory method `update()`
  - [ ] Métodos específicos para cambios de status
- [ ] Tests unitarios de entidades
- [ ] ✋ **STOP - Confirmar con usuario**

### Fase 2: Infrastructure
- [ ] Crear interface de repositorio en `domain/infrastructure/`
- [ ] Crear modelo SQLAlchemy en `infrastructure/models/`
- [ ] Implementar repositorio en `infrastructure/repositories/`
  - [ ] Métodos `_to_domain()` y `_to_model()`
- [ ] Crear mappers (Entity → DTO, DTO → Response)
- [ ] Crear migración con `make revision`
- [ ] Aplicar migración con `make migrate`
- [ ] Tests de repositorio
- [ ] ✋ **STOP - Confirmar con usuario**

### Fase 3: Application & Presentation
- [ ] Crear DTOs en `application/dtos/`
- [ ] Crear Commands en `application/commands/`
  - [ ] Command dataclass
  - [ ] CommandHandler (void)
- [ ] Crear Queries en `application/queries/`
  - [ ] Query dataclass
  - [ ] QueryHandler (retorna DTO)
- [ ] Crear Request schemas en `presentation/schemas/`
- [ ] Crear Response schemas en `presentation/schemas/`
- [ ] Crear Controller en `presentation/controllers/`
- [ ] Crear Router en `presentation/routers/`
- [ ] Registrar en `core/container.py`
  - [ ] Repository
  - [ ] Handlers
  - [ ] Controller
- [ ] Tests de API
- [ ] ✅ **DONE**

## Resumen Visual

```
📁 src/{module}/
├── 📂 domain/
│   ├── 📂 entities/          ← Fase 1
│   ├── 📂 value_objects/     ← Fase 1
│   ├── 📂 enums/             ← Fase 1
│   └── 📂 infrastructure/
│       └── {entity}_repository_interface.py  ← Fase 2
│
├── 📂 application/
│   ├── 📂 commands/          ← Fase 3
│   ├── 📂 queries/           ← Fase 3
│   ├── 📂 dtos/              ← Fase 3
│   └── 📂 mappers/           ← Fase 2
│
├── 📂 infrastructure/
│   ├── 📂 models/            ← Fase 2
│   └── 📂 repositories/      ← Fase 2
│
└── 📂 presentation/
    ├── 📂 controllers/       ← Fase 3
    ├── 📂 routers/           ← Fase 3
    ├── 📂 schemas/           ← Fase 3
    └── 📂 mappers/           ← Fase 2
```

---

**Recuerda**: Implementar fase por fase, confirmando con el usuario al final de cada una.
