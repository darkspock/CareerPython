## Job Position Opening Workflow
Companies may have different workflows types for job opening. For example, sales and technical are different.

We are going to allow different workflows different job positions.

So we are going to support kanban boards, and lists.

A workflow consists in several stage.
Each workflow can choose a default kanban board or list.
Each stage:
* Will have an icon and back/fore color. Look for the existing "Edit Stage Style" modal. try to reuse it.
* Will have a role, responsible of the stage.
* Is mapped to a JobPositionStatusEnum
* KanbanDisplay property. Vertical, horizontal on the bottom, and hidden.
* Will have custom fields. Like we have with "CustomField" in Candidate Workflow. But we are going to use a differente approach.
* We will store the custom fields in a JSON format in the JobPositionWorkflow entity, and we will store values in json in Job Position
* Need visibility by stage and validatoin by stage, the same way is done with Candidate Workflow. Field Visibility by Stage
* in http://localhost:5173/company/workflows/01K8VGTMH198G5E6FP84BWBGBA/advanced-config

No migration from current data is needed.

# Frontend
## Configuration
Add configuration inside http://localhost:5173/company/settings
## Workflow
Add the workflow here:
http://localhost:5173/company/positions
Shows the default view. Kanban or List. Can switch between them.
Have a global search, the result is always a list.
A filter by workflow type and status.

---

## Análisis Técnico

### Arquitectura Propuesta

#### 1. **Entidades y Dominio**
- **JobPositionWorkflow**: Nueva entidad que almacenará la configuración del workflow
  - Campos JSON para custom fields (más flexible que relaciones separadas)
  - Mapeo Stage → JobPositionStatusEnum
  - Configuración de visualización (Kanban/List)
  - Configuración de roles por stage

- **JobPosition**: 
  - **NO tiene status directamente** - tiene un `stage_id` que referencia al Stage del workflow
  - El status se obtiene del mapeo del Stage → JobPositionStatusEnum
  - Necesita almacenar valores de custom fields en JSON
  - Necesita referencia al workflow_id y stage_id actual
  - **No se requiere migración de datos** - la tabla está vacía

#### 2. **Ventajas del Enfoque JSON para Custom Fields**
- ✅ Flexibilidad: Cada workflow puede tener campos diferentes sin crear nuevas tablas
- ✅ Performance: Menos JOINs necesarios
- ✅ Escalabilidad: Fácil agregar nuevos campos sin migraciones complejas
- ⚠️ Trade-off: Validación más compleja (necesita validación en aplicación)
- ⚠️ Búsqueda: Búsquedas en JSON pueden ser más lentas que índices en columnas

#### 3. **Reutilización de Componentes Existentes**
- **Edit Stage Style Modal**: Ya existe en Candidate Workflow
  - Reutilizar componente `EditStageStyleModal` o similar
  - Asegurar que los estilos sean consistentes entre Candidate y JobPosition workflows

- **Field Visibility by Stage**: Sistema existente en Candidate Workflow
  - Reutilizar lógica de visibilidad/validación por stage
  - Adaptar para JobPosition custom fields

#### 4. **Consideraciones de Implementación**

**Backend (Fase 1 - Domain Layer):**
```
1. JobPositionWorkflow Entity
   - id: JobPositionWorkflowId
   - company_id: CompanyId
   - name: str
   - workflow_type: str (enum)
   - default_view: ViewType (KANBAN | LIST)
   - stages: List[WorkflowStage]
   - custom_fields_config: JSON (schema de campos)
   
2. WorkflowStage Value Object
   - id: StageId
   - name: str
   - icon: str
   - background_color: str
   - text_color: str
   - role: CompanyRole (responsable)
   - status_mapping: JobPositionStatusEnum (mapeo personalizable)
   - kanban_display: KanbanDisplay (VERTICAL | HORIZONTAL_BOTTOM | HIDDEN)
   - field_visibility: Dict[str, bool] (qué campos son visibles)
   - field_validation: Dict[str, ValidationRule] (reglas de validación)
   
3. JobPosition Entity (modificaciones)
   - REMOVER: status: JobPositionStatusEnum (ya no existe directamente)
   - AGREGAR: workflow_id: JobPositionWorkflowId (opcional, puede ser None)
   - AGREGAR: stage_id: StageId (opcional, puede ser None para posiciones sin workflow)
   - AGREGAR: custom_fields_values: Dict[str, Any] (JSON)
   - MÉTODO: get_status() -> JobPositionStatusEnum
     - Si tiene stage_id, retorna stage.status_mapping
     - Si no tiene stage_id, retorna DRAFT por defecto (o lanza error)
```

**Backend (Fase 2 - Infrastructure):**
```
1. JobPositionWorkflowModel
   - custom_fields_config: JSON column
   - stages: JSON column (serialized WorkflowStage list)
   
2. JobPositionModel
   - REMOVER: status column (ya no existe, tabla está vacía)
   - AGREGAR: workflow_id: ForeignKey (nullable)
   - AGREGAR: stage_id: String (nullable, referencia al Stage ID)
   - AGREGAR: custom_fields_values: JSON column
   - MIGRACIÓN: Solo para agregar columnas (workflow_id, stage_id, custom_fields_values)
   - **No se requiere migración de datos** - tabla está vacía
```

**Backend (Fase 3 - Application/Presentation):**
```
1. Commands:
   - CreateJobPositionWorkflowCommand
   - UpdateJobPositionWorkflowCommand
   - UpdateJobPositionCustomFieldsCommand
   
2. Queries:
   - GetJobPositionWorkflowQuery
   - ListJobPositionWorkflowsQuery
   - GetJobPositionsByWorkflowQuery
   
3. Endpoints:
   - POST /api/company/workflows/job-position
   - PUT /api/company/workflows/job-position/{id}
   - GET /api/company/positions?workflow_type={type}
```

**Frontend:**
```
1. Componentes a crear/adaptar:
   - JobPositionWorkflowConfig (en /company/settings)
   - JobPositionKanbanBoard (similar a CandidateKanbanBoard)
   - JobPositionListView (similar a CandidateListView)
   - JobPositionCustomFieldsForm (dinámico basado en workflow config)
   - EditStageStyleModal (reutilizar del Candidate Workflow)
   
2. Páginas:
   - /company/positions (refactorizar para soportar workflows)
   - /company/settings/workflows/job-position (configuración)
```

#### 5. **Desafíos Identificados**

1. **Validación de Custom Fields en JSON**
   - Validar estructura según `custom_fields_config`
   - Validar tipos de datos (string, number, date, etc.)
   - Validar reglas por stage (required, min/max, etc.)
   - Considerar usar Pydantic models para validación

2. **Búsqueda en Custom Fields JSON**
   - PostgreSQL soporta búsqueda JSON con índices GIN
   - Considerar campos de búsqueda frecuente como columnas separadas
   - Implementar búsqueda full-text en JSON si es necesario

3. **Migración de Datos Existentes**
   - **NO REQUERIDA**: La tabla job_positions está vacía
   - Solo se necesita migración de esquema para agregar nuevas columnas:
     - workflow_id (ForeignKey, nullable)
     - stage_id (String, nullable)
     - custom_fields_values (JSON, nullable)
   - No hay datos existentes que migrar

4. **Arquitectura Status vs Stage**
   - **IMPORTANTE**: Un JobPosition NO tiene status directamente
   - JobPosition tiene un **Stage** (del workflow)
   - El Stage tiene un **mapeo a JobPositionStatusEnum** (configurable en el workflow)
   - El status es una propiedad del Stage, no del JobPosition
   - Cuando se mueve un JobPosition a un Stage, el status se obtiene del mapeo del Stage
   - No hay sincronización bidireccional: es una relación unidireccional Stage → Status
   - Las transiciones válidas son entre Stages, no entre Status

5. **Performance con Múltiples Workflows**
   - Cada company puede tener múltiples workflows
   - Caching de configuración de workflows
   - Optimizar queries cuando hay muchos workflows

#### 6. **Recomendaciones**

1. **Validación de Custom Fields**
   ```python
   # Usar Pydantic para validar estructura de custom_fields_config
   class CustomFieldConfig(BaseModel):
       name: str
       type: FieldType  # TEXT, NUMBER, DATE, SELECT, etc.
       required: bool
       default_value: Optional[Any]
       validation_rules: Dict[str, Any]
   ```

2. **Búsqueda Optimizada**
   - Crear índices GIN en columnas JSON para búsqueda rápida
   - Considerar campos de búsqueda frecuente como columnas separadas
   - Implementar búsqueda full-text en JSON si es necesario

3. **UI/UX**
   - Reutilizar componentes de Candidate Workflow para consistencia
   - Implementar drag & drop para Kanban (similar a Candidate Workflow)
   - Permitir personalización de campos por workflow type

4. **Testing**
   - Tests unitarios para validación de custom fields
   - Tests de integración para workflows completos
   - Tests de performance para búsquedas en JSON

#### 7. **Orden de Implementación Sugerido**

1. **Fase 1: Domain Layer**
   - Crear JobPositionWorkflow entity
   - Crear WorkflowStage value object
   - Crear enums necesarios (ViewType, KanbanDisplay, etc.)
   
2. **Fase 2: Infrastructure**
   - Crear JobPositionWorkflowModel
   - Agregar custom_fields_values a JobPositionModel
   - Crear repositorios
   - Migraciones de base de datos
   
3. **Fase 3: Application Layer**
   - Commands y Queries
   - Validación de custom fields
   - Lógica de búsqueda
   
4. **Fase 4: Presentation Layer**
   - Endpoints API
   - Componentes frontend
   - Integración con UI existente

#### 8. **Preguntas Abiertas**

1. ¿Cómo se manejarán los JobPositions existentes sin workflow asignado?
   - **Respuesta**: No aplica - la tabla está vacía, todos los JobPositions nuevos se crearán con workflow

2. ¿Se puede cambiar el workflow de un JobPosition después de crearlo?
   - **Pregunta abierta**: ¿Qué pasa con el stage_id si cambia el workflow?
   - ¿Se resetea el stage o se intenta mapear al stage equivalente?

3. ¿Los custom fields pueden tener valores por defecto?
   - **Pregunta abierta**: ¿Los valores por defecto se aplican al crear el JobPosition?

4. ¿Se pueden tener workflows diferentes para el mismo tipo de posición?
   - **Pregunta abierta**: ¿Un workflow_type puede tener múltiples workflows configurados?

5. ¿Cómo se obtiene el status de un JobPosition?
   - **Respuesta**: `job_position.stage.status_mapping` (a través del stage)
   - Si no tiene stage, ¿retorna None o un status por defecto?

6. ¿Se necesita versionado de workflows para cambios en el futuro?
   - **Pregunta abierta**: ¿Qué pasa si se cambia el mapeo de un stage?
   - ¿Los JobPositions existentes mantienen su stage o se actualizan automáticamente?

---

**Nota**: Este análisis asume que el sistema sigue el patrón DDD establecido en el proyecto, con separación clara entre Domain, Application, Infrastructure y Presentation layers.
