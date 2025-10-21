# Tareas de Implementación - Módulo Company

Este documento contiene las tareas para implementar el sistema de empresas en CareerPython.

## Estructura de Implementación

Cada módulo se implementa en **3 fases** que deben completarse en orden:

```
Fase 1: Domain Layer (Entidades, Value Objects, Enums)
   ↓ STOP - Confirmar con usuario
Fase 2: Infrastructure (Repositorios, Mappers, Modelos, Migraciones)
   ↓ STOP - Confirmar con usuario
Fase 3: Application & Presentation (Endpoints, Commands, Queries)
   ↓ DONE ✅
```

---

## Módulo 1: Company (Empresas)

### Tarea 1.1: Domain Layer - Entidades, Value Objects y Enums

**Objetivo**: Crear la representación del dominio de Company sin preocuparse por persistencia.

**Archivos a crear**:

#### Enums
- [ ] `src/company/domain/enums/company_status.py`
  ```python
  class CompanyStatus(str, Enum):
      ACTIVE = "active"
      SUSPENDED = "suspended"
      DELETED = "deleted"
  ```

- [ ] `src/company/domain/enums/company_user_role.py`
  ```python
  class CompanyUserRole(str, Enum):
      ADMIN = "admin"
      RECRUITER = "recruiter"
      VIEWER = "viewer"
  ```

#### Value Objects
- [ ] `src/company/domain/value_objects/company_id.py`
  ```python
  @dataclass(frozen=True)
  class CompanyId:
      value: str
  ```

- [ ] `src/company/domain/value_objects/company_settings.py`
  ```python
  @dataclass(frozen=True)
  class CompanySettings:
      # Configuraciones personalizadas de la empresa
      pass
  ```

#### Entidades
- [ ] `src/company/domain/entities/company.py`
  - Constructor con todos los parámetros (sin defaults)
  - Propiedades públicas
  - Factory method `create()` con defaults y validaciones
  - Factory method `update()` recibe todos los atributos actualizables
  - Método `suspend()` para cambiar a SUSPENDED
  - Método `activate()` para cambiar a ACTIVE
  - Método `delete()` para cambiar a DELETED (soft delete)

- [ ] `src/company/domain/entities/company_user.py`
  - Constructor con todos los parámetros
  - Propiedades públicas
  - Factory method `create()`
  - Factory method `update()` para actualizar role y permissions
  - Método `activate()`
  - Método `deactivate()`

#### Tests
- [ ] `tests/unit/company/domain/entities/test_company.py`
- [ ] `tests/unit/company/domain/entities/test_company_user.py`

**🛑 FIN DE FASE 1 - Confirmar con usuario antes de continuar**

---

### Tarea 1.2: Infrastructure - Repositorios, Mappers, Modelos y Migraciones

**Objetivo**: Implementar la persistencia sin modificar el dominio.

**Archivos a crear**:

#### Interfaces de Repositorio
- [ ] `src/company/domain/infrastructure/company_repository_interface.py`
  - `save(company: Company) -> None`
  - `get_by_id(company_id: CompanyId) -> Optional[Company]`
  - `get_by_domain(domain: str) -> Optional[Company]`
  - `list_all() -> List[Company]`
  - `list_active() -> List[Company]`
  - `delete(company_id: CompanyId) -> None`

- [ ] `src/company/domain/infrastructure/company_user_repository_interface.py`
  - `save(company_user: CompanyUser) -> None`
  - `get_by_id(user_id: str) -> Optional[CompanyUser]`
  - `list_by_company(company_id: CompanyId) -> List[CompanyUser]`
  - `get_by_company_and_user(company_id: CompanyId, user_id: str) -> Optional[CompanyUser]`
  - `delete(user_id: str) -> None`

#### Modelos SQLAlchemy
- [ ] `src/company/infrastructure/models/company_model.py`
  - Tabla `companies`
  - Columnas: id, name, domain, logo_url, settings (JSON), status, created_at, updated_at
  - Índice en `domain` (unique)
  - Relación con `company_users`

- [ ] `src/company/infrastructure/models/company_user_model.py`
  - Tabla `company_users`
  - Columnas: id, company_id, user_id, role, permissions (JSON), status, created_at, updated_at
  - FK a `companies` y `users`
  - Índice compuesto en (company_id, user_id) unique

#### Repositorios
- [ ] `src/company/infrastructure/repositories/company_repository.py`
  - Implementa `CompanyRepositoryInterface`
  - Métodos `_to_domain()` y `_to_model()`

- [ ] `src/company/infrastructure/repositories/company_user_repository.py`
  - Implementa `CompanyUserRepositoryInterface`
  - Métodos `_to_domain()` y `_to_model()`

#### DTOs
- [ ] `src/company/application/dtos/company_dto.py`
- [ ] `src/company/application/dtos/company_user_dto.py`

#### Mappers
- [ ] `src/company/application/mappers/company_mapper.py`
  - `entity_to_dto(entity: Company) -> CompanyDto`

- [ ] `src/company/application/mappers/company_user_mapper.py`
  - `entity_to_dto(entity: CompanyUser) -> CompanyUserDto`

- [ ] `src/company/presentation/mappers/company_mapper.py`
  - `dto_to_response(dto: CompanyDto) -> CompanyResponse`

- [ ] `src/company/presentation/mappers/company_user_mapper.py`
  - `dto_to_response(dto: CompanyUserDto) -> CompanyUserResponse`

#### Migraciones
- [ ] Ejecutar: `make revision m="add companies and company_users tables"`
- [ ] Revisar migración generada
- [ ] Ejecutar: `make migrate`

#### Tests
- [ ] `tests/integration/company/infrastructure/test_company_repository.py`
- [ ] `tests/integration/company/infrastructure/test_company_user_repository.py`

**🛑 FIN DE FASE 2 - Confirmar con usuario antes de continuar**

---

### Tarea 1.3: Application & Presentation - Endpoints, Commands y Queries

**Objetivo**: Exponer la funcionalidad a través de API.

**Archivos a crear**:

#### Commands (Escritura)
- [ ] `src/company/application/commands/create_company_command.py`
  - Command dataclass
  - CommandHandler (void)

- [ ] `src/company/application/commands/update_company_command.py`
- [ ] `src/company/application/commands/suspend_company_command.py`
- [ ] `src/company/application/commands/activate_company_command.py`
- [ ] `src/company/application/commands/delete_company_command.py`
- [ ] `src/company/application/commands/add_company_user_command.py`
- [ ] `src/company/application/commands/update_company_user_command.py`
- [ ] `src/company/application/commands/remove_company_user_command.py`

#### Queries (Lectura)
- [ ] `src/company/application/queries/get_company_by_id_query.py`
  - Query dataclass
  - QueryHandler retorna CompanyDto

- [ ] `src/company/application/queries/get_company_by_domain_query.py`
- [ ] `src/company/application/queries/list_companies_query.py`
- [ ] `src/company/application/queries/list_company_users_query.py`
- [ ] `src/company/application/queries/get_company_user_query.py`

#### Schemas (Requests y Responses)
- [ ] `src/company/presentation/schemas/company_request.py`
  - `CreateCompanyRequest`
  - `UpdateCompanyRequest`

- [ ] `src/company/presentation/schemas/company_response.py`
  - `CompanyResponse`
  - `CompanyListResponse`

- [ ] `src/company/presentation/schemas/company_user_request.py`
  - `AddCompanyUserRequest`
  - `UpdateCompanyUserRequest`

- [ ] `src/company/presentation/schemas/company_user_response.py`
  - `CompanyUserResponse`
  - `CompanyUserListResponse`

#### Controllers
- [ ] `src/company/presentation/controllers/company_controller.py`
  - `create_company()`
  - `update_company()`
  - `get_company()`
  - `list_companies()`
  - `suspend_company()`
  - `activate_company()`
  - `delete_company()`

- [ ] `src/company/presentation/controllers/company_user_controller.py`
  - `add_user()`
  - `update_user()`
  - `remove_user()`
  - `list_users()`
  - `get_user()`

#### Routers
- [ ] `src/company/presentation/routers/company_router.py`
  - `POST /companies` - Crear empresa
  - `GET /companies` - Listar empresas
  - `GET /companies/{id}` - Obtener empresa
  - `PUT /companies/{id}` - Actualizar empresa
  - `POST /companies/{id}/suspend` - Suspender empresa
  - `POST /companies/{id}/activate` - Activar empresa
  - `DELETE /companies/{id}` - Eliminar empresa (soft)

- [ ] `src/company/presentation/routers/company_user_router.py`
  - `POST /companies/{company_id}/users` - Agregar usuario
  - `GET /companies/{company_id}/users` - Listar usuarios
  - `GET /companies/{company_id}/users/{user_id}` - Obtener usuario
  - `PUT /companies/{company_id}/users/{user_id}` - Actualizar usuario
  - `DELETE /companies/{company_id}/users/{user_id}` - Eliminar usuario

#### Dependency Injection
- [ ] Actualizar `core/container.py`
  - Registrar `CompanyRepository`
  - Registrar `CompanyUserRepository`
  - Registrar todos los CommandHandlers
  - Registrar todos los QueryHandlers
  - Registrar Controllers

#### Tests
- [ ] `tests/integration/company/presentation/test_company_router.py`
- [ ] `tests/integration/company/presentation/test_company_user_router.py`

**✅ FIN DE TAREA 1.3 - Módulo Company completo**

---

## Módulo 2: CompanyCandidate (Relación Empresa-Candidato)

### Tarea 2.1: Domain Layer - Entidades, Value Objects y Enums

**Archivos a crear**:

#### Enums
- [ ] `src/company_candidate/domain/enums/company_candidate_status.py`
  ```python
  class CompanyCandidateStatus(str, Enum):
      PENDING_INVITATION = "pending_invitation"
      PENDING_CONFIRMATION = "pending_confirmation"
      ACTIVE = "active"
      REJECTED = "rejected"
      ARCHIVED = "archived"
  ```

- [ ] `src/company_candidate/domain/enums/ownership_status.py`
  ```python
  class OwnershipStatus(str, Enum):
      COMPANY_OWNED = "company_owned"
      USER_OWNED = "user_owned"
  ```

- [ ] `src/company_candidate/domain/enums/invitation_type.py`
  ```python
  class InvitationType(str, Enum):
      NEW_USER = "new_user"
      EXISTING_USER = "existing_user"
  ```

- [ ] `src/company_candidate/domain/enums/invitation_status.py`
  ```python
  class InvitationStatus(str, Enum):
      PENDING = "pending"
      ACCEPTED = "accepted"
      REJECTED = "rejected"
      EXPIRED = "expired"
  ```

- [ ] `src/company_candidate/domain/enums/comment_visibility.py`
  ```python
  class CommentVisibility(str, Enum):
      PRIVATE = "private"
      SHARED_WITH_CANDIDATE = "shared_with_candidate"
  ```

- [ ] `src/company_candidate/domain/enums/priority.py`
  ```python
  class Priority(str, Enum):
      LOW = "low"
      MEDIUM = "medium"
      HIGH = "high"
  ```

#### Value Objects
- [ ] `src/company_candidate/domain/value_objects/visibility_settings.py`
  ```python
  @dataclass(frozen=True)
  class VisibilitySettings:
      education: bool
      experience: bool
      projects: bool
      skills: bool
      certifications: bool
      languages: bool
      contact_info: bool
  ```

#### Entidades
- [ ] `src/company_candidate/domain/entities/company_candidate.py`
  - Constructor con todos los parámetros
  - Factory method `create()`
  - Factory method `update()` (position, department, priority, tags, notes)
  - Método `confirm()` - confirma invitación y cambia a ACTIVE
  - Método `reject()` - rechaza invitación
  - Método `archive()` - archiva relación
  - Método `transfer_ownership_to_user()` - cambia a USER_OWNED
  - Método `update_visibility_settings()`

- [ ] `src/company_candidate/domain/entities/candidate_invitation.py`
  - Constructor
  - Factory method `create()`
  - Método `accept()` - cambia a ACCEPTED
  - Método `reject()` - cambia a REJECTED
  - Método `expire()` - cambia a EXPIRED
  - Método `is_expired()` - verifica si expiró

- [ ] `src/company_candidate/domain/entities/candidate_comment.py`
  - Constructor
  - Factory method `create()`
  - Factory method `update()` (comment text)
  - Método `share_with_candidate()` - cambia visibility
  - Método `make_private()` - cambia visibility
  - Método `soft_delete()`

#### Tests
- [ ] `tests/unit/company_candidate/domain/entities/test_company_candidate.py`
- [ ] `tests/unit/company_candidate/domain/entities/test_candidate_invitation.py`
- [ ] `tests/unit/company_candidate/domain/entities/test_candidate_comment.py`

**🛑 FIN DE FASE 1 - Confirmar con usuario antes de continuar**

---

### Tarea 2.2: Infrastructure - Repositorios, Mappers, Modelos y Migraciones

**Archivos a crear**:

#### Interfaces de Repositorio
- [ ] `src/company_candidate/domain/infrastructure/company_candidate_repository_interface.py`
- [ ] `src/company_candidate/domain/infrastructure/candidate_invitation_repository_interface.py`
- [ ] `src/company_candidate/domain/infrastructure/candidate_comment_repository_interface.py`
- [ ] `src/company_candidate/domain/infrastructure/candidate_access_log_repository_interface.py`

#### Modelos SQLAlchemy
- [ ] `src/company_candidate/infrastructure/models/company_candidate_model.py`
  - Tabla `company_candidates`
  - Todas las columnas según diseño en COMPANY.md
  - FK a companies y candidates
  - FK a workflows (nullable)

- [ ] `src/company_candidate/infrastructure/models/candidate_invitation_model.py`
  - Tabla `candidate_invitations`

- [ ] `src/company_candidate/infrastructure/models/candidate_comment_model.py`
  - Tabla `candidate_comments`

- [ ] `src/company_candidate/infrastructure/models/candidate_access_log_model.py`
  - Tabla `candidate_access_logs`

#### Repositorios
- [ ] Implementar todos los repositorios con métodos `_to_domain()` y `_to_model()`

#### DTOs y Mappers
- [ ] DTOs para cada entidad
- [ ] Mappers en application y presentation layers

#### Migraciones
- [ ] `make revision m="add company_candidate tables"`
- [ ] Revisar y aplicar migración

#### Tests
- [ ] Tests de repositorios

**🛑 FIN DE FASE 2 - Confirmar con usuario antes de continuar**

---

### Tarea 2.3: Application & Presentation - Endpoints, Commands y Queries

**Archivos a crear**:

#### Commands
- [ ] `create_company_candidate_command.py` - Empresa crea/invita candidato
- [ ] `confirm_invitation_command.py` - Candidato confirma invitación
- [ ] `reject_invitation_command.py` - Candidato rechaza invitación
- [ ] `update_company_candidate_command.py` - Actualizar tags, notes, position
- [ ] `archive_company_candidate_command.py` - Archivar relación
- [ ] `update_visibility_settings_command.py` - Candidato actualiza privacidad
- [ ] `add_candidate_comment_command.py` - Agregar comentario
- [ ] `update_candidate_comment_command.py` - Editar comentario
- [ ] `delete_candidate_comment_command.py` - Soft delete de comentario

#### Queries
- [ ] `get_company_candidate_by_id_query.py`
- [ ] `list_company_candidates_query.py` - Lista candidatos de una empresa
- [ ] `list_candidate_companies_query.py` - Lista empresas de un candidato
- [ ] `get_candidate_invitation_query.py` - Obtener invitación por token
- [ ] `list_candidate_comments_query.py` - Listar comentarios
- [ ] `list_candidate_access_logs_query.py` - Historial de accesos

#### Schemas, Controllers y Routers
- [ ] Request/Response schemas
- [ ] Controllers para CompanyCandidate, Invitations, Comments
- [ ] Routers:
  - `/companies/{company_id}/candidates`
  - `/candidates/{candidate_id}/companies`
  - `/invitations/{token}`
  - `/companies/{company_id}/candidates/{candidate_id}/comments`

#### Dependency Injection
- [ ] Actualizar `core/container.py`

#### Tests
- [ ] Tests de endpoints

**✅ FIN DE TAREA 2.3 - Módulo CompanyCandidate completo**

---

## Módulo 3: CompanyWorkflow (Flujos de Trabajo)

### Tarea 3.1: Domain Layer - Entidades, Value Objects y Enums

**Archivos a crear**:

#### Enums
- [ ] `src/company_workflow/domain/enums/workflow_status.py`
  ```python
  class WorkflowStatus(str, Enum):
      ACTIVE = "active"
      ARCHIVED = "archived"
  ```

- [ ] Reutilizar `ApplicationStatusEnum` de `candidate_application`

#### Value Objects
- [ ] `src/company_workflow/domain/value_objects/workflow_id.py`
- [ ] `src/company_workflow/domain/value_objects/stage_id.py`

#### Entidades
- [ ] `src/company_workflow/domain/entities/company_workflow.py`
  - Constructor
  - Factory method `create()`
  - Factory method `update()` (name, description, is_default)
  - Método `archive()`
  - Método `activate()`
  - Método `set_as_default()`

- [ ] `src/company_workflow/domain/entities/workflow_stage.py`
  - Constructor
  - Factory method `create()`
  - Factory method `update()` (name, description, color, mapped_status)
  - Validación de mapped_status contra ApplicationStatusEnum

- [ ] `src/company_workflow/domain/entities/workflow_stage_transition.py`
  - Constructor
  - Factory method `create()`
  - Factory method `update()` (name, requires_comment)

- [ ] `src/company_workflow/domain/entities/candidate_stage_history.py`
  - Constructor
  - Factory method `create()` - registra movimiento de candidato
  - Cálculo de `duration_in_previous_stage`

#### Domain Services (Opcional)
- [ ] `src/company_workflow/domain/services/workflow_validator_service.py`
  - Valida que workflow tiene etapa inicial
  - Valida que tiene etapas finales
  - Valida que no hay ciclos infinitos
  - Valida que todos los stages están conectados

#### Tests
- [ ] Tests unitarios de entidades
- [ ] Tests de workflow validator service

**🛑 FIN DE FASE 1 - Confirmar con usuario antes de continuar**

---

### Tarea 3.2: Infrastructure - Repositorios, Mappers, Modelos y Migraciones

**Archivos a crear**:

#### Interfaces de Repositorio
- [ ] `company_workflow_repository_interface.py`
- [ ] `workflow_stage_repository_interface.py`
- [ ] `workflow_stage_transition_repository_interface.py`
- [ ] `candidate_stage_history_repository_interface.py`

#### Modelos SQLAlchemy
- [ ] `company_workflow_model.py`
  - Tabla `company_workflows`
  - FK a companies

- [ ] `workflow_stage_model.py`
  - Tabla `workflow_stages`
  - FK a company_workflows
  - Columna `mapped_status` tipo ApplicationStatusEnum

- [ ] `workflow_stage_transition_model.py`
  - Tabla `workflow_stage_transitions`

- [ ] `candidate_stage_history_model.py`
  - Tabla `candidate_stage_history`
  - FK a company_candidates, workflows, stages

#### Repositorios
- [ ] Implementar todos con conversión entity ↔ model

#### DTOs y Mappers
- [ ] DTOs completos con datos de workflow
- [ ] Mappers entity→dto y dto→response

#### Migraciones
- [ ] `make revision m="add workflow tables"`
- [ ] Actualizar `company_candidate_model.py` para agregar workflow_id y current_stage_id
- [ ] `make revision m="add workflow references to company_candidates"`
- [ ] Aplicar migraciones

#### Tests
- [ ] Tests de repositorios

**🛑 FIN DE FASE 2 - Confirmar con usuario antes de continuar**

---

### Tarea 3.3: Application & Presentation - Endpoints, Commands y Queries

**Archivos a crear**:

#### Commands
- [ ] `create_workflow_command.py` - Crear workflow
- [ ] `update_workflow_command.py`
- [ ] `archive_workflow_command.py`
- [ ] `create_workflow_stage_command.py` - Crear etapa
- [ ] `update_workflow_stage_command.py`
- [ ] `delete_workflow_stage_command.py`
- [ ] `create_workflow_transition_command.py` - Crear transición
- [ ] `delete_workflow_transition_command.py`
- [ ] `move_candidate_to_stage_command.py` - Mover candidato entre etapas
- [ ] `assign_candidate_to_workflow_command.py` - Asignar candidato a workflow
- [ ] `change_candidate_workflow_command.py` - Cambiar de workflow

#### Queries
- [ ] `get_workflow_by_id_query.py`
- [ ] `list_company_workflows_query.py`
- [ ] `get_workflow_stages_query.py`
- [ ] `get_workflow_transitions_query.py`
- [ ] `get_available_transitions_for_candidate_query.py` - Transiciones disponibles desde etapa actual
- [ ] `get_candidate_stage_history_query.py` - Historial de movimientos
- [ ] `get_workflow_analytics_query.py` - Métricas del workflow

#### Schemas, Controllers y Routers
- [ ] Request/Response schemas para workflows, stages, transitions
- [ ] Controllers
- [ ] Routers:
  - `/companies/{company_id}/workflows`
  - `/workflows/{workflow_id}/stages`
  - `/workflows/{workflow_id}/transitions`
  - `/companies/{company_id}/candidates/{candidate_id}/move-stage`
  - `/companies/{company_id}/candidates/{candidate_id}/stage-history`

#### Dependency Injection
- [ ] Actualizar `core/container.py`

#### Tests
- [ ] Tests de endpoints de workflows
- [ ] Tests de movimiento de candidatos
- [ ] Tests de validaciones de transiciones

**✅ FIN DE TAREA 3.3 - Módulo CompanyWorkflow completo**

---

## Resumen de Progreso

### Módulo 1: Company
- [ ] Tarea 1.1: Domain Layer
- [ ] Tarea 1.2: Infrastructure
- [ ] Tarea 1.3: Application & Presentation

### Módulo 2: CompanyCandidate
- [ ] Tarea 2.1: Domain Layer
- [ ] Tarea 2.2: Infrastructure
- [ ] Tarea 2.3: Application & Presentation

### Módulo 3: CompanyWorkflow
- [ ] Tarea 3.1: Domain Layer
- [ ] Tarea 3.2: Infrastructure
- [ ] Tarea 3.3: Application & Presentation

---

## Notas Importantes

1. **Orden estricto**: Completar Módulo 1 antes de empezar Módulo 2
2. **Confirmación por fase**: Esperar confirmación del usuario al final de cada fase
3. **Testing**: Crear tests para cada fase antes de continuar
4. **Documentación**: Referirse a `docs/ai_docs/DEVELOPMENT_WORKFLOW.md` para detalles
5. **Reglas**: Seguir `.clinerules` estrictamente

## Dependencias entre Módulos

```
Company (core)
    ↓
CompanyCandidate (depende de Company y Candidate)
    ↓
CompanyWorkflow (depende de CompanyCandidate y ApplicationStatusEnum)
```

---

## Próximos Pasos

1. ✅ Confirmar que el plan está claro
2. ▶️ Comenzar con **Tarea 1.1**: Domain Layer de Company
3. ⏸️ Esperar confirmación antes de Tarea 1.2
4. ⏸️ Esperar confirmación antes de Tarea 1.3
5. 🔄 Repetir para Módulos 2 y 3
