# Job Position Workflow Status Implementation

## Summary

Se ha agregado un campo `status` a `JobPositionWorkflow` para gestionar el ciclo de vida de los flujos de trabajo. Los valores son:
- `draft`: Flujo en borrador (no visible para usuarios finales)
- `published`: Flujo publicado (disponible para uso)
- `deprecated`: Flujo obsoleto (no se puede usar para nuevas posiciones)

Además, se modificó el proceso de inicialización de flujos predeterminados para **borrar workflows existentes** antes de crear los nuevos.

## Changes Implemented

### 1. Domain Layer

#### 1.1. Enum: `JobPositionWorkflowStatusEnum`
**File**: `src/job_position/domain/enums/job_position_workflow_status.py`
- Valores: `DRAFT`, `PUBLISHED`, `DEPRECATED`
- Hereda de `str, Enum`

#### 1.2. Entity: `JobPositionWorkflow`
**File**: `src/job_position/domain/entities/job_position_workflow.py`
- ✅ Agregado campo `status: JobPositionWorkflowStatusEnum`
- ✅ Actualizado método `create()` con parámetro `status` (default: `PUBLISHED`)

### 2. Infrastructure Layer

#### 2.1. Model: `JobPositionWorkflowModel`
**File**: `src/job_position/infrastructure/models/job_position_workflow_model.py`
- ✅ Agregado campo `status` (Enum no nativo, VARCHAR(20), indexed)
- ✅ Valor por defecto: `JobPositionWorkflowStatusEnum.PUBLISHED.value`

#### 2.2. Repository: `JobPositionWorkflowRepository`
**File**: `src/job_position/infrastructure/repositories/job_position_workflow_repository.py`
- ✅ Actualizado `_to_domain()` para mapear el campo `status`
- ✅ Actualizado `_to_model()` para incluir `status.value`
- ✅ Actualizado `_update_model_from_entity()` para actualizar el campo `status`

#### 2.3. Migration
**File**: `alembic/versions/e6e09165ad42_add_status_to_job_position_workflows.py`
- ✅ Agrega columna `status` a la tabla `job_position_workflows`
- ✅ Crea índice en `status`
- ✅ Valor por defecto: `'published'`

### 3. Application Layer

#### 3.1. DTO: `JobPositionWorkflowDto`
**File**: `src/job_position/application/dtos/job_position_workflow_dto.py`
- ✅ Agregado campo `status: str`
- ✅ Actualizado método `from_entity()` para mapear `status.value`

#### 3.2. Command: `DeleteJobPositionWorkflowCommand`
**File**: `src/job_position/application/commands/delete_job_position_workflow_command.py`
- ✅ **NUEVO**: Comando para eliminar workflows
- ✅ Handler que llama a `repository.delete()`

### 4. Presentation Layer

#### 4.1. Schema: `JobPositionWorkflowResponse`
**File**: `adapters/http/admin/schemas/job_position_workflow.py`
- ✅ Agregado campo `status: str`

#### 4.2. Controller: `JobPositionWorkflowController`
**File**: `adapters/http/admin/controllers/job_position_workflow_controller.py`
- ✅ Actualizado `_dto_to_response()` para incluir `status`
- ✅ **MODIFICADO**: `initialize_default_workflows()` ahora:
  - Borra todos los workflows existentes de la empresa
  - Crea 3 flujos predeterminados:
    1. **Proceso de Contratación Estándar** (5 etapas)
    2. **Flujo Simplificado** (3 etapas)
    3. **General** (4 etapas: Borrador, Pendiente de Aprobación, Publicado, Descartado)

### 5. Dependency Injection

**File**: `core/container.py`
- ✅ Agregado import de `DeleteJobPositionWorkflowCommandHandler`
- ✅ Registrado `delete_job_position_workflow_command_handler` como Factory

### 6. Frontend (TypeScript)

#### 6.1. Type: `JobPositionWorkflow`
**File**: `client-vite/src/types/position.ts`
- ✅ Agregado campo `status: string` (valores: `'draft' | 'published' | 'deprecated'`)

## Workflow Initialization Behavior

### Old Behavior ❌
- Verificaba si existían workflows
- Si existían, retornaba array vacío `[]`
- No eliminaba workflows obsoletos

### New Behavior ✅
- **Elimina todos los workflows existentes** de la empresa
- Crea 3 flujos predeterminados desde cero:
  1. **Proceso de Contratación Estándar**: 5 etapas (Borrador, Publicada, En Revisión, Pausada, Cerrada)
  2. **Flujo Simplificado**: 3 etapas (Borrador, Activa, Cerrada)
  3. **General**: 4 etapas (Borrador, Pendiente de Aprobación, Publicado, Descartado)
- Todos los workflows se crean con status `published` por defecto

## Database Migration

### Migration File
`alembic/versions/e6e09165ad42_add_status_to_job_position_workflows.py`

### Apply Migration
```bash
cd /Users/juanmacias/Projects/CareerPython
alembic upgrade head
```

### Changes Applied
1. **Added column**: `job_position_workflows.status` (VARCHAR(20), NOT NULL, default: 'published')
2. **Added index**: `ix_job_position_workflows_status`
3. **Existing records**: Will have `status = 'published'` (by default)

## Testing

### Backend (mypy)
```bash
python -m mypy adapters/http/admin/controllers/job_position_workflow_controller.py
# ✅ Success: no issues found
```

### Frontend (TypeScript)
```bash
cd client-vite && npm run build
# ✅ built in 3.47s
```

## API Impact

### Response Changes
All endpoints returning `JobPositionWorkflowResponse` now include:
```json
{
  "id": "01H...",
  "company_id": "01H...",
  "name": "General",
  "default_view": "kanban",
  "status": "published",  // ← NEW FIELD
  "stages": [...],
  "custom_fields_config": {...},
  "created_at": "2025-01-01T00:00:00",
  "updated_at": "2025-01-01T00:00:00"
}
```

### Affected Endpoints
- `GET /admin/workflows?company_id={id}` - List workflows
- `GET /admin/workflows/{id}` - Get workflow by ID
- `POST /admin/workflows/initialize?company_id={id}` - Initialize defaults (**⚠️ DESTRUCTIVE**)
- `POST /admin/workflows` - Create workflow
- `PUT /admin/workflows/{id}` - Update workflow

## Notes

### ⚠️ Breaking Change: Initialize Workflows
El endpoint `/admin/workflows/initialize` ahora:
- **Elimina todos los workflows existentes** antes de crear los nuevos
- Esto es **DESTRUCTIVO** y no se puede deshacer
- Los Job Positions asociados a workflows eliminados quedarán sin workflow

### Recommendations
1. Implementar confirmación explícita en el frontend antes de llamar `initialize`
2. Considerar agregar un endpoint separado para "reset completo" vs "crear si no existen"
3. Agregar backup automático antes de eliminar workflows
4. Implementar soft-delete (`status = deprecated`) en lugar de hard-delete

## Future Enhancements

### Possible Features
1. **Soft Delete**: En lugar de eliminar, marcar workflows como `deprecated`
2. **Workflow Versioning**: Crear versiones de workflows en lugar de reemplazarlos
3. **Workflow Templates**: Permitir clonar workflows existentes
4. **Status Validation**: Prevenir eliminación de workflows en uso (con job positions activas)
5. **Audit Log**: Registrar cambios de status de workflows

### Status Lifecycle
```
draft → published → deprecated
  ↓         ↓            ↓
can edit  in use     archived
```

## Related Documentation
- `docs/JobPositionWorkflow.md` - Workflow system overview
- `docs/JobPositionWorkflow_ImplementationPlan.md` - Implementation phases
- `.cursorrules` - Development workflow rules
- `docs/ai_docs/DEVELOPMENT_WORKFLOW.md` - Coding standards

