# Análisis y Mejora de Dependency Injection (DI)

## Estado Actual

### Implementación Actual
- **Framework**: `dependency-injector` (python-dependency-injector)
- **Tipo de Container**: `DeclarativeContainer`
- **Ubicación**: `core/container.py` (~2494 líneas)
- **Patrón**: Container monolítico con todos los providers en un solo archivo

### Lo que está bien ✅

1. **Uso de `DeclarativeContainer`**: Correcto para proyectos grandes
2. **`Singleton` para servicios core**: `database`, `event_bus`, `email_service`, `ai_service`, `storage_service` están bien como singletons
3. **`Factory` para repositorios y handlers**: Correcto para crear instancias por request
4. **Wiring centralizado**: `container.wire()` en `main.py` es correcto

### Problemas Identificados ❌

1. **Archivo monolítico muy grande** (~2494 líneas): Viola Single Responsibility Principle
2. **Instancias locales del container**: En `query_bus.py` y `command_bus.py` se crean nuevas instancias (`container = Container()`)
3. **Falta `providers.Configuration`**: La configuración debería venir del container
4. **Uso de strings para imports lazy**: Menos type-safe
5. **Métodos estáticos para factories**: `_get_email_service()`, `_get_ai_service()` podrían ser más explícitos
6. **Falta de `providers.Resource`**: Para recursos con lifecycle (startup/shutdown)

---

## Plan de Mejora: Contenedores Modulares

### Estructura Propuesta

```
core/
├── containers/
│   ├── __init__.py              # Exporta Container principal
│   ├── main_container.py        # Container principal que compone los demás
│   ├── auth_container.py        # Auth BC: User, Staff, Authentication
│   ├── company_container.py     # Company BC: Company, CompanyUser, CompanyRole
│   ├── candidate_container.py   # Candidate BC: Candidate, Resume, Application
│   ├── interview_container.py  # Interview BC: Interview, InterviewTemplate
│   ├── job_position_container.py # JobPosition BC
│   ├── workflow_container.py    # Workflow BC: Workflow, Stage, Phase
│   └── shared_container.py     # Servicios compartidos: Database, EventBus, Email, AI, Storage
```

---

## Instrucciones de Implementación

### Fase 1: Crear Estructura de Contenedores Modulares

#### Paso 1.1: Crear directorio y archivos base

```bash
mkdir -p core/containers
touch core/containers/__init__.py
touch core/containers/shared_container.py
touch core/containers/auth_container.py
touch core/containers/company_container.py
touch core/containers/candidate_container.py
touch core/containers/interview_container.py
touch core/containers/job_position_container.py
touch core/containers/workflow_container.py
touch core/containers/main_container.py
```

#### Paso 1.2: Crear `shared_container.py` (Servicios Core)

```python
# core/containers/shared_container.py
from dependency_injector import containers, providers
from core.database import SQLAlchemyDatabase
from core.event_bus import EventBus
from core.config import settings

class SharedContainer(containers.DeclarativeContainer):
    """Container para servicios compartidos (Database, EventBus, Email, AI, Storage)"""
    
    # Configuration
    config = providers.Configuration()
    
    # Core Services (Singletons)
    database = providers.Singleton(SQLAlchemyDatabase)
    event_bus = providers.Singleton(EventBus)
    
    # Email Service Factory
    @staticmethod
    def _get_email_service():
        from src.framework.infrastructure.services.email.mailgun_service import MailgunService
        from src.framework.infrastructure.services.email.smtp_service import SMTPEmailService
        
        if settings.EMAIL_SERVICE == "mailgun":
            return MailgunService()
        else:
            return SMTPEmailService()
    
    email_service = providers.Singleton(_get_email_service)
    
    # AI Service Factory
    @staticmethod
    def _get_ai_service():
        if settings.AI_AGENT.lower() == "groq":
            from src.framework.infrastructure.services.ai.groq_service import GroqResumeAnalysisService
            return GroqResumeAnalysisService()
        else:
            from src.framework.infrastructure.services.ai.xai_service import XAIResumeAnalysisService
            return XAIResumeAnalysisService()
    
    ai_service = providers.Singleton(_get_ai_service)
    
    # Storage Service Factory
    @staticmethod
    def _get_storage_service():
        from src.framework.domain.infrastructure.storage_service_interface import StorageConfig
        from src.framework.infrastructure.services.storage.storage_factory import StorageFactory
        
        allowed_extensions = [ext.strip() for ext in settings.ALLOWED_FILE_EXTENSIONS.split(',')]
        config = StorageConfig(
            max_file_size_mb=settings.MAX_FILE_SIZE_MB,
            allowed_extensions=allowed_extensions
        )
        
        return StorageFactory.create_storage_service(
            storage_type=settings.STORAGE_TYPE,
            config=config
        )
    
    storage_service = providers.Singleton(_get_storage_service)
    
    # Async Job Services
    async_job_repository = providers.Factory(
        'src.framework.infrastructure.repositories.async_job_repository.AsyncJobRepository',
        database=database
    )
    
    async_job_service = providers.Factory(
        'src.framework.infrastructure.services.async_job_service.AsyncJobService',
        repository=async_job_repository
    )
    
    # PDF Processing Service
    pdf_processing_service = providers.Factory(
        'src.framework.infrastructure.services.pdf_processing_service.PDFProcessingService'
    )
```

#### Paso 1.3: Crear `auth_container.py` (Auth Bounded Context)

```python
# core/containers/auth_container.py
from dependency_injector import containers, providers
from adapters.http.auth.controllers.user import UserController

class AuthContainer(containers.DeclarativeContainer):
    """Container para Auth Bounded Context"""
    
    # Dependencias compartidas (se inyectarán desde MainContainer)
    shared = providers.DependenciesContainer()
    
    # Repositories
    user_repository = providers.Factory(
        'src.auth_bc.user.infrastructure.repositories.user_repository.SQLAlchemyUserRepository',
        database=shared.database
    )
    
    staff_repository = providers.Factory(
        'src.auth_bc.staff.infrastructure.repositories.staff_repository.SQLAlchemyStaffRepository',
        database=shared.database
    )
    
    user_asset_repository = providers.Factory(
        'src.auth_bc.user.infrastructure.repositories.user_asset_repository.SQLAlchemyUserAssetRepository',
        database=shared.database
    )
    
    # Query Handlers
    authenticate_user_query_handler = providers.Factory(
        'src.auth_bc.user.application.queries.authenticate_user_query.AuthenticateUserQueryHandler',
        user_repository=user_repository
    )
    
    check_user_exists_query_handler = providers.Factory(
        'src.auth_bc.user.application.queries.check_user_exists_query.CheckUserExistsQueryHandler',
        user_repository=user_repository
    )
    
    get_current_user_from_token_query_handler = providers.Factory(
        'src.auth_bc.user.application.queries.get_current_user_from_token_query.GetCurrentUserFromTokenQueryHandler',
        user_repository=user_repository
    )
    
    create_access_token_query_handler = providers.Factory(
        'src.auth_bc.user.application.queries.create_access_token_query.CreateAccessTokenQueryHandler'
    )
    
    get_user_language_query_handler = providers.Factory(
        'src.auth_bc.user.application.queries.get_user_language_query.GetUserLanguageQueryHandler',
        user_repository=user_repository
    )
    
    get_user_by_email_query_handler = providers.Factory(
        'src.auth_bc.user.application.queries.get_user_by_email_query.GetUserByEmailQueryHandler',
        user_repository=user_repository
    )
    
    # Command Handlers
    create_user_command_handler = providers.Factory(
        'src.auth_bc.user.application.commands.create_user_command.CreateUserCommandHandler',
        user_repository=user_repository
    )
    
    create_user_automatically_command_handler = providers.Factory(
        'src.auth_bc.user.application.commands.create_user_automatically_command.CreateUserAutomaticallyCommandHandler',
        user_repository=user_repository
    )
    
    request_password_reset_command_handler = providers.Factory(
        'src.auth_bc.user.application.commands.request_password_reset_command.RequestPasswordResetCommandHandler',
        user_repository=user_repository,
        email_service=shared.email_service
    )
    
    reset_password_with_token_command_handler = providers.Factory(
        'src.auth_bc.user.application.commands.reset_password_with_token_command.ResetPasswordWithTokenCommandHandler',
        user_repository=user_repository
    )
    
    update_user_password_command_handler = providers.Factory(
        'src.auth_bc.user.application.commands.update_user_password_command.UpdateUserPasswordCommandHandler',
        user_repository=user_repository
    )
    
    update_user_language_command_handler = providers.Factory(
        'src.auth_bc.user.application.commands.update_user_language_command.UpdateUserLanguageCommandHandler',
        user_repository=user_repository
    )
    
    # Controllers
    user_controller = providers.Factory(
        UserController,
        command_bus=shared.command_bus,
        query_bus=shared.query_bus
    )
```

#### Paso 1.4: Crear `interview_container.py` (Interview Bounded Context)

```python
# core/containers/interview_container.py
from dependency_injector import containers, providers
from adapters.http.company_app.interview.controllers.interview_controller import InterviewController
from adapters.http.admin_app.controllers.inverview_template_controller import InterviewTemplateController


class InterviewContainer(containers.DeclarativeContainer):
    """Container para Interview Bounded Context"""

    # Dependencias compartidas
    shared = providers.DependenciesContainer()

    # Repositories
    interview_template_repository = providers.Factory(
        'src.interview_bc.interview_template.infrastructure.repositories.interview_template_repository.InterviewTemplateRepository',
        database=shared.database
    )

    interview_template_section_repository = providers.Factory(
        'src.interview_bc.interview_template.infrastructure.repositories.interview_template_section_repository.InterviewTemplateSectionRepository',
        database=shared.database
    )

    interview_template_question_repository = providers.Factory(
        'src.interview_bc.interview_template.infrastructure.repositories.interview_template_question_repository.InterviewTemplateQuestionRepository',
        database=shared.database
    )

    interview_repository = providers.Factory(
        'src.interview_bc.interview.Infrastructure.repositories.interview_repository.SQLAlchemyInterviewRepository',
        database=shared.database
    )

    interview_answer_repository = providers.Factory(
        'src.interview_bc.interview.Infrastructure.repositories.interview_answer_repository.SQLAlchemyInterviewAnswerRepository',
        database=shared.database
    )

    interview_interviewer_repository = providers.Factory(
        'src.interview_bc.interview.Infrastructure.repositories.interview_interviewer_repository.SQLAlchemyInterviewInterviewerRepository',
        database=shared.database
    )

    # Domain Services
    interview_permission_service = providers.Factory(
        'src.interview_bc.interview.application.services.interview_permission_service.InterviewPermissionService',
        company_user_repository=shared.company_user_repository,
        company_role_repository=shared.company_role_repository
    )

    # Query Handlers (solo los más importantes como ejemplo)
    list_interview_templates_query_handler = providers.Factory(
        'src.interview_bc.interview_template.application.queries.list_interview_templates.ListInterviewTemplatesQueryHandler',
        repository=interview_template_repository
    )

    list_interviews_query_handler = providers.Factory(
        'src.interview_bc.interview.application.queries.list_interviews.ListInterviewsQueryHandler',
        interview_repository=interview_repository
    )

    get_interview_by_id_query_handler = providers.Factory(
        'src.interview_bc.interview.application.queries.get_interview_by_id.GetInterviewByIdQueryHandler',
        interview_repository=interview_repository
    )

    # Command Handlers (solo los más importantes como ejemplo)
    create_interview_template_command_handler = providers.Factory(
        'src.interview_bc.interview_template.application.commands.create_interview_template.CreateInterviewTemplateCommandHandler',
        repository=interview_template_repository
    )

    create_interview_command_handler = providers.Factory(
        'src.interview_bc.interview.application.commands.create_interview.CreateInterviewCommandHandler',
        interview_repository=interview_repository
    )

    # Controllers
    interview_template_controller = providers.Factory(
        InterviewTemplateController,
        command_bus=shared.command_bus,
        query_bus=shared.query_bus
    )

    interview_controller = providers.Factory(
        InterviewController,
        command_bus=shared.command_bus,
        query_bus=shared.query_bus
    )
```

#### Paso 1.5: Crear `main_container.py` (Container Principal)

```python
# core/containers/main_container.py
from dependency_injector import containers, providers
from core.containers.shared_container import SharedContainer
from core.containers.auth_container import AuthContainer
from core.containers.interview_container import InterviewContainer
# ... importar otros containers

from src.framework.application.command_bus import CommandBus
from src.framework.application.query_bus import QueryBus

class Container(containers.DeclarativeContainer):
    """Container principal que compone todos los bounded contexts"""
    
    # Wiring
    wiring_config = containers.WiringConfiguration(
        modules=[
            "adapters.http.admin_app.routes.admin_router",
            "adapters.http.company_app.interview.routers.company_interview_router",
            # ... todos los módulos que necesitan wiring
        ]
    )
    
    # Shared Container (servicios core)
    shared = containers.Container(SharedContainer)
    
    # Bounded Context Containers
    auth = containers.Container(
        AuthContainer,
        shared=shared
    )
    
    interview = containers.Container(
        InterviewContainer,
        shared=shared
    )
    
    # ... otros containers (company, candidate, job_position, workflow)
    
    # Command Bus y Query Bus (dependen de todos los handlers)
    command_bus = providers.Singleton(
        CommandBus
    )
    
    query_bus = providers.Singleton(
        QueryBus
    )
    
    # Exponer servicios compartidos directamente para compatibilidad
    database = shared.database
    event_bus = shared.event_bus
    email_service = shared.email_service
    ai_service = shared.ai_service
    storage_service = shared.storage_service
    
    # Exponer controllers para compatibilidad
    user_controller = auth.user_controller
    interview_controller = interview.interview_controller
    interview_template_controller = interview.interview_template_controller
    
    # Exponer repositorios para compatibilidad (si se necesitan directamente)
    user_repository = auth.user_repository
    interview_repository = interview.interview_repository
```

#### Paso 1.6: Actualizar `core/containers/__init__.py`

```python
# core/containers/__init__.py
from core.containers.main_container import Container

__all__ = ["Container"]
```

---

### Fase 2: Migrar Providers del Container Actual

#### Paso 2.1: Identificar y agrupar providers por Bounded Context

1. **Auth BC**: `user_repository`, `staff_repository`, `user_asset_repository`, todos los handlers de auth
2. **Company BC**: `company_repository`, `company_user_repository`, `company_role_repository`, etc.
3. **Candidate BC**: `candidate_repository`, `resume_repository`, `candidate_application_repository`, etc.
4. **Interview BC**: `interview_repository`, `interview_template_repository`, etc.
5. **JobPosition BC**: `job_position_repository`, `job_position_comment_repository`, etc.
6. **Workflow BC**: `workflow_repository`, `workflow_stage_repository`, `phase_repository`, etc.
7. **Shared**: `database`, `event_bus`, `email_service`, `ai_service`, `storage_service`

#### Paso 2.2: Migrar providers uno por uno

Para cada provider en `core/container.py`:
1. Identificar a qué Bounded Context pertenece
2. Moverlo al container correspondiente
3. Ajustar dependencias usando `shared.database`, `shared.command_bus`, etc.
4. Actualizar referencias en el código

---

### Fase 3: Corregir Instancias Locales del Container

#### Paso 3.1: Identificar lugares donde se crea `Container()` localmente

Buscar en:
- `src/framework/application/query_bus.py`
- `src/framework/application/command_bus.py`
- Cualquier otro lugar donde se instancie `Container()`

#### Paso 3.2: Inyectar container como dependencia

**Antes:**
```python
# src/framework/application/query_bus.py
class QueryBus:
    def query(self, query: Query):
        from core.container import Container
        container = Container()  # ❌ Nueva instancia
        # ...
```

**Después:**
```python
# src/framework/application/query_bus.py
from dependency_injector.wiring import inject, Provide
from core.containers import Container

class QueryBus:
    @inject
    def __init__(self, container: Container = Provide[Container]):
        self._container = container
    
    def query(self, query: Query):
        # Usar self._container
        # ...
```

O mejor aún, pasar el container desde `main_container.py`:

```python
# core/containers/main_container.py
query_bus = providers.Singleton(
    QueryBus,
    container=providers.Self()  # Se auto-inyecta
)
```

---

### Fase 4: Usar `providers.Configuration` para Configuración

#### Paso 4.1: Crear configuración en `shared_container.py`

```python
# core/containers/shared_container.py
class SharedContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    
    # Cargar desde variables de entorno
    config.email_service.from_env("EMAIL_SERVICE", as_=str, default="smtp")
    config.ai_agent.from_env("AI_AGENT", as_=str, default="xai")
    config.storage_type.from_env("STORAGE_TYPE", as_=str, default="local")
    # ... más configuraciones
```

#### Paso 4.2: Usar configuración en providers

```python
email_service = providers.Singleton(
    _get_email_service,
    email_service_type=config.email_service
)
```

---

### Fase 5: Reemplazar Strings por Imports Directos

#### Paso 5.1: Identificar providers con strings

Buscar todos los `providers.Factory('ruta.completa')` en el container.

#### Paso 5.2: Reemplazar por imports directos

**Antes:**
```python
resume_repository = providers.Factory(
    'src.candidate_bc.resume.infrastructure.repositories.resume_repository.SQLAlchemyResumeRepository',
    database=database
)
```

**Después:**
```python
from src.candidate_bc.resume.infrastructure.repositories.resume_repository import SQLAlchemyResumeRepository

resume_repository = providers.Factory(
    SQLAlchemyResumeRepository,
    database=database
)
```

---

### Fase 6: Usar `providers.Resource` para Recursos con Lifecycle

#### Paso 6.1: Identificar recursos que necesitan startup/shutdown

- Database connections
- Event bus connections
- External service clients

#### Paso 6.2: Convertir a Resource providers

**Antes:**
```python
database = providers.Singleton(SQLAlchemyDatabase)
```

**Después:**
```python
database = providers.Resource(
    SQLAlchemyDatabase,
    init=lambda db: db.connect(),  # Startup
    shutdown=lambda db: db.disconnect()  # Shutdown
)
```

---

### Fase 7: Actualizar `main.py`

#### Paso 7.1: Actualizar import

```python
# main.py
from core.containers import Container  # En lugar de core.container
```

#### Paso 7.2: El resto debería funcionar igual

```python
container = Container()
app.container = container
container.wire(modules=[...])
```

---

## Orden de Migración Recomendado

1. **Crear estructura de contenedores** (Fase 1)
2. **Migrar SharedContainer primero** (servicios core)
3. **Migrar AuthContainer** (más simple, menos dependencias)
4. **Migrar InterviewContainer** (ya parcialmente aislado)
5. **Migrar CompanyContainer**
6. **Migrar CandidateContainer**
7. **Migrar JobPositionContainer**
8. **Migrar WorkflowContainer**
9. **Crear MainContainer** que compone todos
10. **Corregir instancias locales** (Fase 3)
11. **Actualizar configuración** (Fase 4)
12. **Reemplazar strings por imports** (Fase 5)
13. **Convertir a Resource providers** (Fase 6)
14. **Actualizar main.py** (Fase 7)

---

## Ventajas de la Nueva Estructura

1. **Mantenibilidad**: Cada bounded context tiene su propio container
2. **Escalabilidad**: Fácil agregar nuevos bounded contexts
3. **Testabilidad**: Puedes mockear containers individuales
4. **Claridad**: Es más fácil encontrar dónde está cada provider
5. **Reutilización**: Containers pueden reutilizarse en diferentes contextos
6. **Type Safety**: Imports directos en lugar de strings

---

## Notas Importantes

- **Compatibilidad hacia atrás**: El `MainContainer` expone los mismos providers que el container actual para mantener compatibilidad
- **Migración gradual**: Puedes migrar un bounded context a la vez sin romper el resto
- **Testing**: Cada container puede testearse independientemente
- **Documentación**: Cada container debería tener docstrings explicando su propósito

---

## Referencias

- [dependency-injector Documentation](https://python-dependency-injector.ets-labs.org/)
- [Declarative Container](https://python-dependency-injector.ets-labs.org/containers/declarative.html)
- [Providers](https://python-dependency-injector.ets-labs.org/providers/index.html)
- [Wiring](https://python-dependency-injector.ets-labs.org/wiring.html)

