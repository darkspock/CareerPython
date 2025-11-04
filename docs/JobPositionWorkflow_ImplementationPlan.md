# Plan de Implementación: Job Position Workflow

## Análisis del Estado Actual

### Elementos que DEBEN ELIMINARSE

#### Backend - Domain Layer
1. **JobPosition Entity** (`src/job_position/domain/entities/job_position.py`)
   - ❌ Campo `status: JobPositionStatusEnum` (línea 44)
   - ❌ Método `activate()` (línea 113-123)
   - ❌ Método `pause()` (línea 125-130)
   - ❌ Método `resume()` (línea 132-137)
   - ❌ Método `close()` (línea 139-146)
   - ❌ Método `archive()` (línea 148-153)
   - ❌ Métodos helper: `is_draft()`, `is_active()`, `is_paused()`, `is_closed()`, `is_archived()` (si existen)
   - ✅ **AGREGAR**: Campo `workflow_id: JobPositionWorkflowId` (opcional)
   - ✅ **AGREGAR**: Campo `stage_id: StageId` (opcional)
   - ✅ **AGREGAR**: Campo `custom_fields_values: Dict[str, Any]` (JSON)
   - ✅ **AGREGAR**: Método `get_status() -> JobPositionStatusEnum` (obtiene status desde stage)

#### Backend - Application Layer
2. **Commands** (`src/job_position/application/commands/approve_job_position.py`)
   - ❌ `ActivateJobPositionCommand` y `ActivateJobPositionCommandHandler`
   - ❌ `PauseJobPositionCommand` y `PauseJobPositionCommandHandler`
   - ❌ `ResumeJobPositionCommand` y `ResumeJobPositionCommandHandler`
   - ❌ `CloseJobPositionCommand` y `CloseJobPositionCommandHandler`
   - ❌ `ArchiveJobPositionCommand` y `ArchiveJobPositionCommandHandler`
   - ✅ **CREAR**: `MoveJobPositionToStageCommand` y handler (nuevo comando para mover entre stages)

3. **UpdateJobPositionCommand** (`src/job_position/application/commands/update_job_position.py`)
   - ❌ Llamada a `job_position.activate()` (línea 95)
   - ✅ Modificar para no usar métodos de status

4. **DeleteJobPositionCommand** (`src/job_position/application/commands/delete_job_position.py`)
   - ❌ Llamada a `job_position.close_position()` (línea 32)
   - ✅ Revisar si necesita modificación

#### Backend - Infrastructure Layer
5. **JobPositionModel** (`src/job_position/infrastructure/models/job_position_model.py`)
   - ❌ Campo `status: Mapped[JobPositionStatusEnum]` (línea 58-61)
   - ✅ **AGREGAR**: `workflow_id: Mapped[Optional[str]]` (ForeignKey, nullable)
   - ✅ **AGREGAR**: `stage_id: Mapped[Optional[str]]` (String, nullable)
   - ✅ **AGREGAR**: `custom_fields_values: Mapped[Optional[Dict[str, Any]]]` (JSON, nullable)

6. **Migraciones**
   - ✅ **CREAR**: Migración para agregar columnas `workflow_id`, `stage_id`, `custom_fields_values`
   - ✅ **CREAR**: Migración para eliminar columna `status` (o mantener como computed)

#### Backend - Presentation Layer
7. **JobPositionController** (`adapters/http/admin/controllers/job_position_controller.py`)
   - ❌ Método `activate_position()` (línea 410)
   - ❌ Método `pause_position()` (línea 430)
   - ❌ Método `resume_position()` (línea 450)
   - ❌ Método `close_position()` (línea 470)
   - ❌ Método `archive_position()` (línea 490)
   - ✅ **CREAR**: Método `move_to_stage(position_id, stage_id)`

8. **Admin Router** (`adapters/http/admin/routes/admin_router.py`)
   - ❌ Endpoint `POST /positions/{position_id}/activate` (línea 610)
   - ❌ Endpoint `POST /positions/{position_id}/pause` (línea 621)
   - ❌ Endpoint `POST /positions/{position_id}/resume` (línea 632)
   - ❌ Endpoint `POST /positions/{position_id}/close` (línea 643)
   - ❌ Endpoint `POST /positions/{position_id}/archive` (línea 654)
   - ✅ **CREAR**: Endpoint `POST /positions/{position_id}/move-to-stage`

9. **Container** (`core/container.py`)
   - ❌ `activate_job_position_command_handler` (línea 1517)
   - ❌ `pause_job_position_command_handler` (línea 1522)
   - ❌ `resume_job_position_command_handler` (línea 1527)
   - ❌ `close_job_position_command_handler` (línea 1532)
   - ❌ `archive_job_position_command_handler` (línea 1537)
   - ✅ **CREAR**: `move_job_position_to_stage_command_handler`

#### Backend - Queries
10. **Queries que filtran por status**
    - Revisar `ListJobPositionsQuery` - actualizar filtros
    - Revisar `ListPublicJobPositionsQuery` - actualizar para usar stage.status_mapping
    - Revisar `GetPublicJobPositionQuery` - actualizar validación de status
    - Revisar `GetJobPositionsStatsQuery` - actualizar para usar stage.status_mapping

#### Frontend
11. **PositionService** (`client-vite/src/services/positionService.ts`)
    - ❌ `activatePosition()`
    - ❌ `pausePosition()`
    - ❌ `resumePosition()`
    - ❌ `closePosition()`
    - ❌ `archivePosition()`
    - ✅ **CREAR**: `moveToStage(positionId, stageId)`

12. **PositionsListPage** (`client-vite/src/pages/company/PositionsListPage.tsx`)
    - ❌ `handleActivate()`
    - ❌ `handlePause()`
    - ❌ `handleResume()`
    - ❌ `handleClose()`
    - ❌ `handleArchive()`
    - ❌ Botones de acción basados en status
    - ✅ **CREAR**: Sistema de drag & drop para Kanban (mover entre stages)
    - ✅ **CREAR**: Botones/acciones basados en stage actual y transiciones válidas

13. **EditPositionPage** (`client-vite/src/pages/company/EditPositionPage.tsx`)
    - ❌ Lógica de auto-activación cuando `is_public` es true
    - ✅ Revisar y adaptar para workflows

14. **Types** (`client-vite/src/types/position.ts`)
    - ❌ Campo `status` en interface `Position`
    - ✅ **AGREGAR**: `workflow_id: string | null`
    - ✅ **AGREGAR**: `stage_id: string | null`
    - ✅ **AGREGAR**: `stage: Stage | null` (objeto completo del stage)
    - ✅ **AGREGAR**: `custom_fields_values: Record<string, any> | null`

---

## Plan de Trabajo por Fases

### FASE 1: Domain Layer (Entidades y Lógica de Negocio)

#### Tarea 1.1: Crear Enums y Value Objects
- [ ] Crear `JobPositionWorkflowId` value object
- [ ] Crear `StageId` value object
- [ ] Crear `ViewType` enum (KANBAN | LIST)
- [ ] Crear `KanbanDisplay` enum (VERTICAL | HORIZONTAL_BOTTOM | HIDDEN)

#### Tarea 1.2: Crear WorkflowStage Value Object
- [ ] Crear `WorkflowStage` value object en `src/job_position/domain/value_objects/workflow_stage.py`
  - `id: StageId`
  - `name: str`
  - `icon: str`
  - `background_color: str`
  - `text_color: str`
  - `role: CompanyRole` (responsable)
  - `status_mapping: JobPositionStatusEnum`
  - `kanban_display: KanbanDisplay`
  - `field_visibility: Dict[str, bool]`
  - `field_validation: Dict[str, ValidationRule]`

#### Tarea 1.3: Crear JobPositionWorkflow Entity
- [ ] Crear `JobPositionWorkflow` entity en `src/job_position/domain/entities/job_position_workflow.py`
  - `id: JobPositionWorkflowId`
  - `company_id: CompanyId`
  - `name: str`
  - `workflow_type: str` (enum)
  - `default_view: ViewType`
  - `stages: List[WorkflowStage]`
  - `custom_fields_config: Dict[str, Any]` (JSON)
  - Factory methods: `create()`, `update()`
  - Métodos para agregar/remover stages

#### Tarea 1.4: Modificar JobPosition Entity
- [ ] **ELIMINAR**: Campo `status: JobPositionStatusEnum`
- [ ] **ELIMINAR**: Métodos `activate()`, `pause()`, `resume()`, `close()`, `archive()`
- [ ] **ELIMINAR**: Métodos helper de status (`is_draft()`, `is_active()`, etc.)
- [ ] **AGREGAR**: Campo `workflow_id: Optional[JobPositionWorkflowId]`
- [ ] **AGREGAR**: Campo `stage_id: Optional[StageId]`
- [ ] **AGREGAR**: Campo `custom_fields_values: Dict[str, Any]`
- [ ] **AGREGAR**: Método `get_status() -> JobPositionStatusEnum` (obtiene desde stage)
- [ ] **AGREGAR**: Método `move_to_stage(stage_id: StageId) -> None`
- [ ] Modificar `create()` para no usar status por defecto
- [ ] Modificar `update()` para no usar métodos de status

**FIN DE FASE 1** - Confirmar con el usuario antes de continuar

---

### FASE 2: Infrastructure Layer (Persistencia)

#### Tarea 2.1: Crear Interface del Repositorio
- [ ] Crear `JobPositionWorkflowRepositoryInterface` en `src/job_position/domain/infrastructure/job_position_workflow_repository_interface.py`
  - Métodos: `get_by_id()`, `get_by_company_id()`, `save()`, `delete()`

#### Tarea 2.2: Crear Modelo SQLAlchemy
- [ ] Crear `JobPositionWorkflowModel` en `src/job_position/infrastructure/models/job_position_workflow_model.py`
  - Tabla: `job_position_workflows`
  - Columnas: id, company_id, name, workflow_type, default_view, stages (JSON), custom_fields_config (JSON)

#### Tarea 2.3: Modificar JobPositionModel
- [ ] **ELIMINAR**: Campo `status`
- [ ] **AGREGAR**: `workflow_id: ForeignKey` (nullable)
- [ ] **AGREGAR**: `stage_id: String` (nullable)
- [ ] **AGREGAR**: `custom_fields_values: JSON` (nullable)

#### Tarea 2.4: Crear Repositorio
- [ ] Implementar `JobPositionWorkflowRepository` en `src/job_position/infrastructure/repositories/job_position_workflow_repository.py`
  - Métodos `_to_domain()` y `_to_model()`
  - Serialización/deserialización de stages (JSON)

#### Tarea 2.5: Actualizar JobPositionRepository
- [ ] Modificar `_to_domain()` para no usar `status`
- [ ] Modificar `_to_model()` para no usar `status`
- [ ] Agregar mapeo de `workflow_id`, `stage_id`, `custom_fields_values`
- [ ] Actualizar métodos que filtran por status para usar stage.status_mapping

#### Tarea 2.6: Crear Migración
- [ ] Crear migración Alembic para:
  - Agregar tabla `job_position_workflows`
  - Agregar columnas `workflow_id`, `stage_id`, `custom_fields_values` a `job_positions`
  - Eliminar columna `status` de `job_positions` (o marcarla como deprecated)

**FIN DE FASE 2** - Confirmar con el usuario antes de continuar

---

### FASE 3: Application & Presentation Layer (API)

#### Tarea 3.1: Crear Commands
- [ ] **ELIMINAR**: `approve_job_position.py` completo (o mantener solo estructura)
- [ ] Crear `create_job_position_workflow.py` con command y handler
- [ ] Crear `update_job_position_workflow.py` con command y handler
- [ ] Crear `move_job_position_to_stage.py` con command y handler
- [ ] Crear `update_job_position_custom_fields.py` con command y handler

#### Tarea 3.2: Crear Queries
- [ ] Crear `get_job_position_workflow.py` con query y handler
- [ ] Crear `list_job_position_workflows.py` con query y handler
- [ ] Crear `get_job_positions_by_workflow.py` con query y handler
- [ ] Modificar queries existentes para usar stage.status_mapping en lugar de status directo

#### Tarea 3.3: Crear DTOs
- [ ] Crear `JobPositionWorkflowDto` en `src/job_position/application/dtos/job_position_workflow_dto.py`
- [ ] Crear `WorkflowStageDto` en `src/job_position/application/dtos/workflow_stage_dto.py`
- [ ] Modificar `JobPositionDto` para:
  - Eliminar `status`
  - Agregar `workflow_id`, `stage_id`, `stage`, `custom_fields_values`

#### Tarea 3.4: Crear Request/Response Schemas
- [ ] Crear schemas en `adapters/http/admin/schemas/job_position_workflow.py`:
  - `CreateJobPositionWorkflowRequest`
  - `UpdateJobPositionWorkflowRequest`
  - `JobPositionWorkflowResponse`
  - `WorkflowStageRequest`
  - `WorkflowStageResponse`
- [ ] Modificar `JobPositionResponse` para eliminar `status` y agregar campos nuevos

#### Tarea 3.5: Crear Controllers
- [ ] Crear `JobPositionWorkflowController` en `adapters/http/admin/controllers/job_position_workflow_controller.py`
- [ ] Modificar `JobPositionController`:
  - Eliminar métodos de status
  - Agregar método `move_to_stage()`

#### Tarea 3.6: Crear Routers
- [ ] Crear router para workflows en `adapters/http/admin/routes/job_position_workflow_router.py`
- [ ] Modificar `admin_router.py`:
  - Eliminar endpoints de status
  - Agregar endpoint `POST /positions/{position_id}/move-to-stage`

#### Tarea 3.7: Actualizar Container
- [ ] Eliminar registros de command handlers de status
- [ ] Registrar nuevos command handlers de workflow
- [ ] Registrar repositorio de workflow

**FIN DE FASE 3** - Feature completamente implementada

---

### FASE 4: Frontend

#### Tarea 4.1: Actualizar Types
- [ ] Modificar `client-vite/src/types/position.ts`:
  - Eliminar `status` de interface `Position`
  - Agregar `workflow_id`, `stage_id`, `stage`, `custom_fields_values`
  - Eliminar funciones `getStatusLabel()`, `getStatusColor()`
  - Crear tipos para `JobPositionWorkflow`, `WorkflowStage`, etc.

#### Tarea 4.2: Actualizar Services
- [ ] Modificar `client-vite/src/services/positionService.ts`:
  - Eliminar métodos de status
  - Agregar `moveToStage()`, `getWorkflows()`, `getWorkflow()`, etc.

#### Tarea 4.3: Refactorizar PositionsListPage
- [ ] Eliminar handlers de status
- [ ] Eliminar botones de acción basados en status
- [ ] Crear componente Kanban board (reutilizar de Candidate Workflow)
- [ ] Crear componente List view
- [ ] Implementar switch Kanban/List
- [ ] Implementar drag & drop para mover entre stages
- [ ] Implementar filtros por workflow_type y stage

#### Tarea 4.4: Refactorizar EditPositionPage
- [ ] Eliminar lógica de auto-activación
- [ ] Agregar selector de workflow (si aplica)
- [ ] Agregar selector de stage inicial
- [ ] Agregar formulario dinámico de custom fields basado en workflow

#### Tarea 4.5: Crear Página de Configuración
- [ ] Crear `JobPositionWorkflowConfigPage` en `/company/settings`
- [ ] Implementar CRUD de workflows
- [ ] Implementar editor de stages
- [ ] Implementar editor de custom fields config
- [ ] Implementar editor de field visibility y validation

---

## Checklist de Eliminación

### Archivos a Eliminar o Vaciar
- [ ] `src/job_position/application/commands/approve_job_position.py` (eliminar o reemplazar completamente)

### Código a Eliminar
- [ ] Campo `status` de `JobPosition` entity
- [ ] Métodos de status de `JobPosition` entity (5 métodos)
- [ ] Campo `status` de `JobPositionModel`
- [ ] 5 Command handlers de status
- [ ] 5 métodos del controller
- [ ] 5 endpoints del router
- [ ] 5 registros en container
- [ ] Frontend: handlers, botones, servicios relacionados con status

### Código a Modificar
- [ ] Queries que filtran por status
- [ ] DTOs que incluyen status
- [ ] Schemas que incluyen status
- [ ] Frontend types que incluyen status
- [ ] Componentes que muestran/usan status

---

## Sistema de Comentarios y Auditoría

### Sistema de Comentarios (Similar a Candidate Workflow)

#### Componentes a Crear

1. **JobPositionComment Entity** (`src/job_position/domain/entities/job_position_comment.py`)
   - Similar a `CandidateComment`
   - Campos:
     - `id: JobPositionCommentId`
     - `job_position_id: JobPositionId`
     - `comment: str`
     - `workflow_id: Optional[JobPositionWorkflowId]`
     - `stage_id: Optional[StageId]`
     - `created_by_user_id: CompanyUserId`
     - `review_status: CommentReviewStatus` (PENDING | REVIEWED)
     - `visibility: CommentVisibility` (PRIVATE | SHARED_WITH_CANDIDATE)
     - `created_at: datetime`
     - `updated_at: datetime`
   - Métodos:
     - `create()` - Factory method
     - `update()` - Actualizar comentario
     - `mark_as_pending()` - Marcar como pendiente
     - `mark_as_reviewed()` - Marcar como revisado

2. **JobPositionCommentRepository**
   - Interface en domain layer
   - Implementación en infrastructure layer
   - Métodos:
     - `save()`, `get_by_id()`, `delete()`
     - `list_by_job_position()`
     - `list_by_stage()`
     - `count_pending_by_job_position()`

3. **Commands y Queries**
   - `CreateJobPositionCommentCommand` y handler
   - `UpdateJobPositionCommentCommand` y handler
   - `MarkCommentAsPendingCommand` y handler
   - `MarkCommentAsReviewedCommand` y handler
   - `ListJobPositionCommentsQuery` y handler
   - `GetPendingCommentsCountQuery` y handler

4. **API Endpoints**
   - `POST /api/company/positions/{position_id}/comments`
   - `PUT /api/company/positions/{position_id}/comments/{comment_id}`
   - `DELETE /api/company/positions/{position_id}/comments/{comment_id}`
   - `POST /api/company/positions/{position_id}/comments/{comment_id}/mark-pending`
   - `POST /api/company/positions/{position_id}/comments/{comment_id}/mark-reviewed`
   - `GET /api/company/positions/{position_id}/comments`

### Sistema de Auditoría/Historial (Activity Log)

#### Componentes a Crear

1. **JobPositionStageHistory Entity** (`src/job_position/domain/entities/job_position_stage_history.py`)
   - Similar a `CandidateStage` pero enfocado en historial de cambios
   - Campos:
     - `id: JobPositionStageHistoryId`
     - `job_position_id: JobPositionId`
     - `workflow_id: JobPositionWorkflowId`
     - `from_stage_id: Optional[StageId]` (stage anterior)
     - `to_stage_id: StageId` (nuevo stage)
     - `changed_by_user_id: CompanyUserId` (quien hizo el cambio)
     - `comment: Optional[str]` (comentario opcional del cambio)
     - `duration_in_previous_stage: Optional[int]` (minutos en stage anterior)
     - `changed_at: datetime`
     - `created_at: datetime`
   - Métodos:
     - `create()` - Factory method
     - `with_comment()` - Agregar comentario al cambio

2. **JobPositionStageHistoryRepository**
   - Interface en domain layer
   - Implementación en infrastructure layer
   - Métodos:
     - `save()` - Guardar nuevo registro de cambio
     - `get_by_id()`
     - `list_by_job_position()` - Historial completo de un JobPosition
     - `get_last_change()` - Último cambio de stage
     - `get_stage_history()` - Historial de un stage específico

3. **Commands y Queries**
   - `RecordStageChangeCommand` y handler (llamado automáticamente cuando se mueve)
   - `GetJobPositionHistoryQuery` y handler
   - `GetJobPositionStageHistoryQuery` y handler

4. **Integración con MoveToStageCommand**
   - Cuando se ejecuta `MoveJobPositionToStageCommand`:
     1. Mover JobPosition a nuevo stage
     2. Calcular `duration_in_previous_stage` (si había stage anterior)
     3. Crear registro en `JobPositionStageHistory`
     4. Guardar JobPosition
     5. Guardar historial

5. **API Endpoints**
   - `GET /api/company/positions/{position_id}/history` - Historial completo
   - `GET /api/company/positions/{position_id}/history/stages` - Solo cambios de stage

### Frontend - Componentes

1. **CommentsCard Component**
   - Reutilizar `CommentsCard` de Candidate Workflow
   - Adaptar para JobPosition
   - Mostrar comentarios por stage
   - Permitir marcar como pendiente/revisado
   - Mostrar contador de comentarios pendientes

2. **ActivityHistory Component**
   - Nuevo componente para mostrar historial
   - Timeline de cambios
   - Filtros por tipo de cambio (stage change, comment, etc.)
   - Mostrar quién hizo cada cambio y cuándo

3. **Integración en Pages**
   - Agregar CommentsCard a `JobPositionDetailPage` (si existe) o `EditPositionPage`
   - Agregar ActivityHistory a la página de detalle
   - Mostrar indicador de comentarios pendientes en listado

---

## Actualización del Plan de Trabajo

### FASE 1: Domain Layer - Agregar al Plan Original

#### Tarea 1.5: Crear Enums para Comentarios
- [ ] Crear `CommentReviewStatus` enum (reutilizar de company_candidate o crear nuevo)
  - `REVIEWED = "reviewed"`
  - `PENDING = "pending"`
- [ ] Crear `CommentVisibility` enum (reutilizar de company_candidate o crear nuevo)
  - `PRIVATE = "private"`
  - `SHARED_WITH_CANDIDATE = "shared_with_candidate"` (opcional para JobPosition)

#### Tarea 1.6: Crear Value Objects
- [ ] Crear `JobPositionCommentId` value object
- [ ] Crear `JobPositionStageHistoryId` value object

#### Tarea 1.7: Crear JobPositionComment Entity
- [ ] Crear entity en `src/job_position/domain/entities/job_position_comment.py`
- [ ] Implementar métodos: `create()`, `update()`, `mark_as_pending()`, `mark_as_reviewed()`

#### Tarea 1.8: Crear JobPositionStageHistory Entity
- [ ] Crear entity en `src/job_position/domain/entities/job_position_stage_history.py`
- [ ] Implementar método `create()` con cálculo de duración

#### Tarea 1.9: Modificar MoveToStage
- [ ] Modificar `JobPosition.move_to_stage()` para aceptar `changed_by_user_id` y `comment` opcional
- [ ] O crear método separado `move_to_stage_with_history()`

### FASE 2: Infrastructure Layer - Agregar al Plan Original

#### Tarea 2.7: Crear JobPositionCommentModel
- [ ] Crear modelo en `src/job_position/infrastructure/models/job_position_comment_model.py`
- [ ] Tabla: `job_position_comments`
- [ ] Índices: job_position_id, stage_id, review_status

#### Tarea 2.8: Crear JobPositionStageHistoryModel
- [ ] Crear modelo en `src/job_position/infrastructure/models/job_position_stage_history_model.py`
- [ ] Tabla: `job_position_stage_history`
- [ ] Índices: job_position_id, workflow_id, to_stage_id, changed_at

#### Tarea 2.9: Crear Repositorios
- [ ] Crear `JobPositionCommentRepositoryInterface` y implementación
- [ ] Crear `JobPositionStageHistoryRepositoryInterface` y implementación

#### Tarea 2.10: Actualizar Migración
- [ ] Agregar creación de tablas `job_position_comments` y `job_position_stage_history` a la migración

### FASE 3: Application & Presentation Layer - Agregar al Plan Original

#### Tarea 3.8: Crear Commands de Comentarios
- [ ] `CreateJobPositionCommentCommand` y handler
- [ ] `UpdateJobPositionCommentCommand` y handler
- [ ] `DeleteJobPositionCommentCommand` y handler
- [ ] `MarkCommentAsPendingCommand` y handler
- [ ] `MarkCommentAsReviewedCommand` y handler

#### Tarea 3.9: Crear Commands de Historial
- [ ] `RecordStageChangeCommand` y handler (llamado automáticamente desde MoveToStageCommandHandler)

#### Tarea 3.10: Crear Queries de Comentarios
- [ ] `ListJobPositionCommentsQuery` y handler
- [ ] `GetPendingCommentsCountQuery` y handler

#### Tarea 3.11: Crear Queries de Historial
- [ ] `GetJobPositionHistoryQuery` y handler
- [ ] `GetJobPositionStageHistoryQuery` y handler

#### Tarea 3.12: Actualizar MoveToStageCommandHandler
- [ ] Modificar para:
  - Calcular duración en stage anterior
  - Crear registro en JobPositionStageHistory
  - Guardar historial después de mover

#### Tarea 3.13: Crear Controllers
- [ ] Crear `JobPositionCommentController`
- [ ] Crear `JobPositionHistoryController`

#### Tarea 3.14: Crear Routers
- [ ] Agregar endpoints de comentarios a `job_position_router.py`
- [ ] Agregar endpoints de historial a `job_position_router.py`

### FASE 4: Frontend - Agregar al Plan Original

#### Tarea 4.6: Crear Types para Comentarios e Historial
- [ ] Crear `JobPositionComment` interface
- [ ] Crear `JobPositionStageHistory` interface
- [ ] Agregar a `Position` type: `comments`, `history`

#### Tarea 4.7: Crear Services
- [ ] Crear `jobPositionCommentService.ts` (similar a `candidateCommentService.ts`)
- [ ] Crear `jobPositionHistoryService.ts`
- [ ] Métodos: create, update, delete, markPending, markReviewed, list, getHistory

#### Tarea 4.8: Crear Componentes
- [ ] Crear `JobPositionCommentsCard.tsx` (reutilizar de `CommentsCard.tsx`)
- [ ] Crear `JobPositionActivityHistory.tsx` (nuevo componente)
- [ ] Crear `PendingCommentsBadge.tsx` (badge con contador)

#### Tarea 4.9: Integrar en Pages
- [ ] Agregar CommentsCard a página de detalle/edición de JobPosition
- [ ] Agregar ActivityHistory a página de detalle
- [ ] Mostrar badge de comentarios pendientes en listado

---

## Notas Importantes

1. **No hay migración de datos**: La tabla `job_positions` está vacía, solo se necesita migración de esquema.

2. **Reutilización**: Aprovechar componentes existentes de Candidate Workflow:
   - Edit Stage Style Modal
   - Kanban Board component
   - List View component
   - Field Visibility configuration
   - **CommentsCard component** (adaptar para JobPosition)
   - **CommentReviewStatus y CommentVisibility enums** (reutilizar o crear nuevos)

3. **Testing**: Crear tests para:
   - Validación de transiciones entre stages
   - Validación de custom fields
   - Búsqueda por stage.status_mapping
   - **Sistema de comentarios** (crear, actualizar, marcar pendiente)
   - **Sistema de historial** (registro de cambios, cálculo de duración)

4. **Backward Compatibility**: Considerar mantener `status` como computed property temporalmente si hay código externo que lo use.

5. **Historial Automático**: El historial se debe crear automáticamente cuando:
   - Se mueve un JobPosition a un nuevo stage
   - Se cambia el workflow
   - Se asigna un workflow inicial

6. **Comentarios Pendientes**: Implementar notificaciones o badges para mostrar comentarios pendientes de revisión.

---

**Última actualización**: 2024
