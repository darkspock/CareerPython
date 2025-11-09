# Análisis del Módulo de Customization

**Fecha**: 2025-01-22  
**Objetivo**: Analizar el estado actual del módulo `src/customization` y planificar su refactorización para hacerlo totalmente personalizable e independiente de workflow.

---

## 📋 Resumen Ejecutivo

El módulo de customization actualmente está **ligado a workflow**, pero se ha iniciado una refactorización para hacerlo **genérico y reutilizable** para cualquier tipo de entidad. El nuevo diseño usa `EntityCustomization` que puede personalizar cualquier entidad del sistema mediante `entity_type` y `entity_id`.

### Estado Actual
- ✅ **Dominio nuevo creado**: `EntityCustomization`, `EntityCustomizationTypeEnum`, `CustomField` (VO)
- ⚠️ **Código antiguo activo**: Todo el código en `src/customization/old/` sigue funcionando y está ligado a workflow
- ⚠️ **Frontend ligado a workflow**: Todos los componentes y servicios usan `workflowId`
- ⚠️ **Base de datos ligada a workflow**: Tablas con `workflow_id` como foreign key

---

## 🏗️ Estructura Actual

### 1. Dominio Nuevo (`src/customization/domain/`)

#### Entidades
- **`EntityCustomization`** (`domain/entities/entity_customization.py`)
  - `id: EntityCustomizationId`
  - `entity_type: EntityCustomizationTypeEnum` (JobPosition, CandidateApplication, Candidate)
  - `entity_id: str` (ID de la entidad personalizada)
  - `fields: List[CustomField]` (Lista de campos personalizados)
  - `validation: str` (JSON-Logic para validaciones)
  - `created_at: int`
  - `updated_at: int`
  - `metadata: Dict[str, Any]` (Metadatos adicionales)

#### Enums
- **`EntityCustomizationTypeEnum`** (`domain/enums/entity_customization_type_enum.py`)
  - `JOB_POSITION = "JobPosition"`
  - `CANDIDATE_APPLICATION = "CandidateApplication"`
  - `CANDIDATE = "Candidate"`

#### Value Objects
- **`CustomFieldId`** (`domain/value_objects/custom_field_id.py`) - Hereda de `BaseId`
- **`EntityCustomizationId`** (`domain/value_objects/entity_customization_id.py`) - Hereda de `BaseId`
- **`CustomField`** (`domain/value_objects/custom_field.py`)
  - `id: str`
  - `field_key: str`
  - `field_name: str`
  - `field_type: str`
  - `field_config: Optional[Dict[str, Any]]`
  - `order_index: int`
  - `created_at: datetime`
  - `updated_at: datetime`

### 2. Código Antiguo (`src/customization/old/`)

#### Estructura
```
old/
├── application/
│   ├── commands/ (Create, Update, Delete, Reorder, ConfigureStageField, UpdateFieldVisibility)
│   ├── queries/ (GetById, ListByWorkflow, ListFieldConfigurationsByStage, GetAllValuesByCompanyCandidate)
│   ├── dtos/ (CustomFieldDto, CustomFieldValueDto, FieldConfigurationDto)
│   └── mappers/
├── infrastructure/
│   └── repositories/
│       ├── custom_field_repository.py
│       ├── custom_field_value_repository.py
│       └── field_configuration_repository.py
├── controllers/ (CustomFieldController, CustomFieldValueController)
├── schemas/ (Requests y Responses)
└── routers/ (Ya movidos a adapters/http/customization/routers/)
```

#### Dependencias con Workflow
**Todas las operaciones están ligadas a `workflow_id`:**

1. **CustomField**:
   - `workflow_id` en DTOs, Commands, Queries
   - `list_by_workflow(workflow_id)` en repositorio
   - `get_by_workflow_and_key(workflow_id, field_key)` en repositorio

2. **CustomFieldValue**:
   - `workflow_id` en DTOs, Commands
   - `get_by_company_candidate_and_workflow(company_candidate_id, workflow_id)` en repositorio
   - `get_all_by_company_candidate()` retorna dict organizado por `workflow_id`

3. **FieldConfiguration**:
   - Ligado a `stage_id` (que pertenece a un workflow)
   - `list_by_stage(stage_id)` en repositorio

### 3. Presentación (`adapters/http/customization/`)

#### Routers
- **`custom_field_router.py`**: 9 endpoints
  - `POST /api/custom-fields/` - Crear campo
  - `GET /api/custom-fields/{field_id}` - Obtener por ID
  - `GET /api/custom-fields/workflow/{workflow_id}` - Listar por workflow ⚠️
  - `PUT /api/custom-fields/{field_id}` - Actualizar
  - `PATCH /api/custom-fields/{field_id}/reorder` - Reordenar
  - `DELETE /api/custom-fields/{field_id}` - Eliminar
  - `POST /api/custom-fields/configurations` - Configurar campo en stage
  - `PATCH /api/custom-fields/configurations/{config_id}/visibility` - Actualizar visibilidad
  - `GET /api/custom-fields/configurations/stage/{stage_id}` - Listar configuraciones por stage

- **`custom_field_value_router.py`**: 6 endpoints
  - `POST /api/company-workflow/custom-field-values` - Crear valor
  - `GET /api/company-workflow/custom-field-values/{value_id}` - Obtener por ID
  - `GET /api/company-workflow/custom-field-values/company-candidate/{company_candidate_id}` - Valores por candidato (workflow actual)
  - `GET /api/company-workflow/custom-field-values/company-candidate/{company_candidate_id}/all` - Todos los valores organizados por workflow
  - `PUT /api/company-workflow/custom-field-values/{value_id}` - Actualizar
  - `PUT /api/company-workflow/custom-field-values/company-candidate/{company_candidate_id}/field/{custom_field_id}` - Upsert single field
  - `DELETE /api/company-workflow/custom-field-values/{value_id}` - Eliminar

---

## 🎨 Frontend

### Componentes Principales

1. **`CustomFieldEditor.tsx`** (`client-vite/src/components/workflow/CustomFieldEditor.tsx`)
   - **Props**: `workflowId: string` ⚠️
   - **Funcionalidad**: Editor completo de campos personalizados
   - **Dependencias**: `CustomFieldService.listCustomFieldsByWorkflow(workflowId)`

2. **`DynamicCustomFields.tsx`** (`client-vite/src/components/jobPosition/DynamicCustomFields.tsx`)
   - **Props**: `workflow`, `currentStage`, `customFieldsValues`
   - **Funcionalidad**: Renderiza campos dinámicos basados en configuración del workflow
   - **Dependencias**: `workflow.custom_fields_config`, `currentStage.field_visibility`

3. **`CustomFieldsCard.tsx`** (`client-vite/src/components/candidate/CustomFieldsCard.tsx`)
   - **Props**: `customFieldValues`, `onUpdateValue`, `isEditable`
   - **Funcionalidad**: Muestra campos personalizados en vista de candidato

### Servicios

**`CustomFieldService`** (`client-vite/src/services/customFieldService.ts`)
- `listCustomFieldsByWorkflow(workflowId: string)` ⚠️
- `createCustomField(request: CreateCustomFieldRequest)` - Request incluye `workflow_id` ⚠️
- `updateCustomField(fieldId, request)` 
- `deleteCustomField(fieldId)`
- `reorderCustomField(fieldId, request)`
- `configureStageField(request)` - Request incluye `stage_id` ⚠️
- `updateFieldVisibility(configId, visibility)`
- `listFieldConfigurationsByStage(stageId)` ⚠️

**`CustomFieldValueService`** (implícito en código)
- `getCustomFieldValuesByCompanyCandidate(companyCandidateId)` - Retorna valores del workflow actual
- `getAllCustomFieldValuesByCompanyCandidate(companyCandidateId)` - Retorna dict por `workflow_id`

### Tipos TypeScript

**`workflow.ts`** (`client-vite/src/types/workflow.ts`)
```typescript
export interface CustomField {
  id: string;
  workflow_id: string;  // ⚠️ Ligado a workflow
  field_key: string;
  field_name: string;
  field_type: FieldType;
  field_config?: Record<string, any>;
  order_index: number;
  created_at: string;
  updated_at: string;
}

export interface FieldConfiguration {
  id: string;
  stage_id: string;  // ⚠️ Ligado a stage (workflow)
  custom_field_id: string;
  visibility: FieldVisibility;
  created_at: string;
  updated_at: string;
}
```

---

## 🗄️ Base de Datos

### Tablas Actuales

#### 1. `workflow_custom_fields`
```sql
CREATE TABLE workflow_custom_fields (
    id VARCHAR(255) PRIMARY KEY,
    workflow_id VARCHAR(255) NOT NULL REFERENCES candidate_application_workflows(id) ON DELETE CASCADE,  -- ⚠️ FK a workflow
    field_key VARCHAR(100) NOT NULL,
    field_name VARCHAR(255) NOT NULL,
    field_type VARCHAR(50) NOT NULL,
    field_config JSONB,
    order_index INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    CONSTRAINT unique_workflow_field_key UNIQUE(workflow_id, field_key)
);
```

**Problemas**:
- Foreign key a `candidate_application_workflows` (tabla antigua)
- No puede usarse para otras entidades
- `workflow_id` es obligatorio

#### 2. `custom_field_values`
```sql
CREATE TABLE custom_field_values (
    id VARCHAR(255) PRIMARY KEY,
    company_candidate_id VARCHAR(255) NOT NULL REFERENCES company_candidates(id) ON DELETE CASCADE,
    workflow_id VARCHAR(255) NOT NULL REFERENCES candidate_application_workflows(id) ON DELETE CASCADE,  -- ⚠️ FK a workflow
    values JSONB NOT NULL DEFAULT '{}',  -- {field_key: value}
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    CONSTRAINT unique_company_candidate_workflow UNIQUE(company_candidate_id, workflow_id)
);
```

**Problemas**:
- Foreign key a `candidate_application_workflows` (tabla antigua)
- Solo funciona para `company_candidates`
- `workflow_id` es obligatorio
- Estructura JSON `{field_key: value}` está bien, pero la FK limita su uso

#### 3. `stage_field_configurations`
```sql
CREATE TABLE stage_field_configurations (
    id VARCHAR(255) PRIMARY KEY,
    stage_id VARCHAR(255) NOT NULL REFERENCES workflow_stages(id) ON DELETE CASCADE,  -- ⚠️ FK a stage
    custom_field_id VARCHAR(255) NOT NULL REFERENCES workflow_custom_fields(id) ON DELETE CASCADE,
    visibility VARCHAR(50) NOT NULL,  -- 'HIDDEN', 'VISIBLE', 'REQUIRED'
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    CONSTRAINT unique_stage_field UNIQUE(stage_id, custom_field_id)
);
```

**Problemas**:
- Ligado a `workflow_stages` (solo para workflows)
- No puede usarse para otras entidades

---

## 🔄 Plan de Refactorización

### Objetivos
1. **Separar completamente de workflow**: Usar `EntityCustomization` con `entity_type` y `entity_id`
2. **Hacer genérico**: Poder personalizar cualquier entidad (JobPosition, Candidate, CandidateApplication, etc.)
3. **Mantener compatibilidad**: Migrar datos existentes de workflow a la nueva estructura
4. **Actualizar frontend**: Cambiar de `workflowId` a `entityType` + `entityId`

### Fase 1: Domain Layer (Nuevo) ✅

**Estado**: Completado
- ✅ `EntityCustomization` entity
- ✅ `EntityCustomizationTypeEnum` enum
- ✅ `CustomField` value object
- ✅ `CustomFieldId` y `EntityCustomizationId` value objects

**Pendiente**:
- ⚠️ `EntityCustomization` necesita métodos `create()` y `update()` (siguiendo reglas del proyecto)
- ⚠️ `CustomField` debería ser un Value Object inmutable completo (actualmente tiene `id: str` en lugar de `CustomFieldId`)
- ⚠️ `EntityCustomization.validation` debería ser `Optional[str]` y `metadata` debería tener valores por defecto
- ⚠️ `created_at` y `updated_at` deberían ser `datetime` en lugar de `int`

### Fase 2: Infrastructure Layer (Nuevo)

**Tareas**:
1. **Crear modelos SQLAlchemy**:
   - `EntityCustomizationModel` - Nueva tabla `entity_customizations`
   - `CustomFieldModel` - Modificar para usar `entity_customization_id` en lugar de `workflow_id`
   - `CustomFieldValueModel` - Modificar para usar `entity_type` + `entity_id` en lugar de `workflow_id`
   - `FieldConfigurationModel` - Modificar para usar `entity_customization_id` + contexto (puede ser stage_id u otro)

2. **Crear interfaces de repositorio**:
   - `EntityCustomizationRepositoryInterface`
   - `CustomFieldRepositoryInterface` (actualizar para usar `EntityCustomizationId`)
   - `CustomFieldValueRepositoryInterface` (actualizar para usar `entity_type` + `entity_id`)

3. **Implementar repositorios**:
   - `EntityCustomizationRepository`
   - `CustomFieldRepository` (refactorizado)
   - `CustomFieldValueRepository` (refactorizado)

4. **Crear migración**:
   - Crear tabla `entity_customizations`
   - Migrar datos de `workflow_custom_fields` a `entity_customizations` + `custom_fields` (nueva estructura)
   - Migrar datos de `custom_field_values` a nueva estructura
   - Opcional: Mantener tablas antiguas por compatibilidad temporal

### Fase 3: Application Layer (Nuevo)

**Tareas**:
1. **Commands**:
   - `CreateEntityCustomizationCommand` (reemplaza `CreateCustomFieldCommand` pero a nivel de entidad)
   - `UpdateEntityCustomizationCommand`
   - `AddCustomFieldToEntityCommand` (agregar campo a una personalización existente)
   - `UpdateCustomFieldCommand` (actualizar campo existente)
   - `DeleteCustomFieldCommand`
   - `ReorderCustomFieldCommand`
   - `SetCustomFieldValueCommand` (reemplaza `CreateCustomFieldValueCommand` y `UpdateCustomFieldValueCommand`)
   - `DeleteCustomFieldValueCommand`
   - `ConfigureFieldVisibilityCommand` (reemplaza `ConfigureStageFieldCommand` pero genérico)

2. **Queries**:
   - `GetEntityCustomizationQuery` (por `entity_type` + `entity_id`)
   - `ListCustomFieldsByEntityQuery` (reemplaza `ListCustomFieldsByWorkflowQuery`)
   - `GetCustomFieldByIdQuery`
   - `GetCustomFieldValuesByEntityQuery` (reemplaza `GetCustomFieldValuesByCompanyCandidate`)
   - `GetAllCustomFieldValuesByEntityQuery`
   - `ListFieldConfigurationsByEntityQuery` (genérico, no solo por stage)

3. **DTOs**:
   - `EntityCustomizationDto`
   - `CustomFieldDto` (actualizar para usar `entity_customization_id` en lugar de `workflow_id`)
   - `CustomFieldValueDto` (actualizar para usar `entity_type` + `entity_id`)
   - `FieldConfigurationDto` (genérico)

4. **Mappers**:
   - `EntityCustomizationMapper`
   - `CustomFieldMapper` (actualizar)
   - `CustomFieldValueMapper` (actualizar)

### Fase 4: Presentation Layer (Nuevo)

**Tareas**:
1. **Schemas**:
   - `CreateEntityCustomizationRequest`
   - `UpdateEntityCustomizationRequest`
   - `AddCustomFieldRequest` (actualizar `CreateCustomFieldRequest`)
   - `UpdateCustomFieldRequest` (actualizar)
   - `SetCustomFieldValueRequest` (actualizar `CreateCustomFieldValueRequest`)
   - `ConfigureFieldVisibilityRequest` (genérico)
   - `EntityCustomizationResponse`
   - `CustomFieldResponse` (actualizar)
   - `CustomFieldValueResponse` (actualizar)

2. **Controllers**:
   - `EntityCustomizationController` (nuevo, orquesta personalizaciones completas)
   - `CustomFieldController` (refactorizar para usar `entity_type` + `entity_id`)
   - `CustomFieldValueController` (refactorizar)

3. **Routers**:
   - `entity_customization_router.py` (nuevo)
   - `custom_field_router.py` (actualizar endpoints para usar `entity_type` + `entity_id`)
   - `custom_field_value_router.py` (actualizar)

### Fase 5: Frontend

**Tareas**:
1. **Tipos TypeScript**:
   - Actualizar `CustomField` para usar `entity_customization_id` en lugar de `workflow_id`
   - Crear `EntityCustomization` type
   - Actualizar `CustomFieldValue` para usar `entity_type` + `entity_id`

2. **Servicios**:
   - `EntityCustomizationService` (nuevo)
   - `CustomFieldService` (refactorizar métodos para usar `entityType` + `entityId`)
   - `CustomFieldValueService` (refactorizar)

3. **Componentes**:
   - `EntityCustomizationEditor` (nuevo, editor completo de personalización)
   - `CustomFieldEditor` (refactorizar para usar `entityType` + `entityId` en lugar de `workflowId`)
   - `DynamicCustomFields` (refactorizar para usar `entityCustomization` en lugar de `workflow.custom_fields_config`)
   - `CustomFieldsCard` (actualizar)

---

## 📊 Comparación: Antes vs Después

### Antes (Ligado a Workflow)
```python
# Crear campo personalizado
CreateCustomFieldCommand(
    workflow_id="workflow_123",
    field_key="salary",
    field_name="Salary",
    ...
)

# Obtener campos
ListCustomFieldsByWorkflowQuery(workflow_id="workflow_123")

# Obtener valores
GetCustomFieldValuesByCompanyCandidateQuery(
    company_candidate_id="candidate_456"
)  # Retorna valores del workflow actual del candidato
```

### Después (Genérico)
```python
# Crear personalización de entidad
CreateEntityCustomizationCommand(
    entity_type=EntityCustomizationTypeEnum.JOB_POSITION,
    entity_id="job_123",
    fields=[...],
    ...
)

# Agregar campo a personalización existente
AddCustomFieldToEntityCommand(
    entity_customization_id="customization_789",
    field_key="salary",
    field_name="Salary",
    ...
)

# Obtener campos
ListCustomFieldsByEntityQuery(
    entity_type=EntityCustomizationTypeEnum.JOB_POSITION,
    entity_id="job_123"
)

# Obtener valores
GetCustomFieldValuesByEntityQuery(
    entity_type=EntityCustomizationTypeEnum.CANDIDATE_APPLICATION,
    entity_id="application_456"
)
```

---

## ⚠️ Consideraciones Importantes

### 1. Migración de Datos
- **Workflows existentes**: Cada `workflow` debe convertirse en un `EntityCustomization` con `entity_type=CANDIDATE_APPLICATION` y `entity_id=workflow_id`
- **Valores existentes**: Los `custom_field_values` con `workflow_id` deben migrarse a la nueva estructura usando `entity_type` + `entity_id`
- **Configuraciones de stage**: Deben migrarse a la nueva estructura genérica de `FieldConfiguration`

### 2. Compatibilidad Temporal
- Mantener endpoints antiguos (`/workflow/{workflow_id}`) que internamente usen la nueva estructura
- Crear adaptadores que conviertan `workflow_id` → `entity_type` + `entity_id`
- Deprecar endpoints antiguos gradualmente

### 3. Field Configuration
- Actualmente ligado a `stage_id` (workflow stages)
- Debe hacerse genérico: puede ser para stages, pero también para otros contextos
- Opción: `context_type` + `context_id` en lugar de solo `stage_id`

### 4. Validaciones
- `EntityCustomization.validation` usa JSON-Logic
- Debe validarse que el JSON-Logic sea válido
- Considerar mover validaciones a un servicio separado

### 5. Metadata
- `EntityCustomization.metadata` permite extensibilidad
- Puede usarse para configuraciones específicas por tipo de entidad
- Ejemplo: Para workflows, metadata puede contener `default_stage_visibility`

---

## ✅ Checklist de Implementación

### Fase 1: Domain Layer
- [x] Crear `EntityCustomization` entity
- [x] Crear `EntityCustomizationTypeEnum`
- [x] Crear `CustomField` value object
- [x] Crear `CustomFieldId` y `EntityCustomizationId`
- [ ] Agregar métodos `create()` y `update()` a `EntityCustomization`
- [ ] Corregir tipos en `EntityCustomization` (datetime, Optional, etc.)
- [ ] Hacer `CustomField` completamente inmutable con `CustomFieldId`

### Fase 2: Infrastructure Layer
- [ ] Crear `EntityCustomizationModel`
- [ ] Crear `EntityCustomizationRepositoryInterface`
- [ ] Implementar `EntityCustomizationRepository`
- [ ] Refactorizar `CustomFieldModel` para usar `entity_customization_id`
- [ ] Refactorizar `CustomFieldRepository` para usar `EntityCustomizationId`
- [ ] Refactorizar `CustomFieldValueModel` para usar `entity_type` + `entity_id`
- [ ] Refactorizar `CustomFieldValueRepository`
- [ ] Refactorizar `FieldConfigurationModel` para ser genérico
- [ ] Crear migración de base de datos

### Fase 3: Application Layer
- [ ] Crear Commands nuevos
- [ ] Crear Command Handlers
- [ ] Crear Queries nuevos
- [ ] Crear Query Handlers
- [ ] Actualizar DTOs
- [ ] Actualizar Mappers
- [ ] Registrar en `core/container.py`

### Fase 4: Presentation Layer
- [ ] Crear schemas nuevos
- [ ] Refactorizar controllers
- [ ] Refactorizar routers
- [ ] Actualizar imports en `main.py`

### Fase 5: Frontend
- [ ] Actualizar tipos TypeScript
- [ ] Refactorizar servicios
- [ ] Refactorizar componentes
- [ ] Actualizar páginas que usan customization

### Fase 6: Testing y Migración
- [ ] Tests unitarios del dominio
- [ ] Tests de repositorios
- [ ] Tests de integración
- [ ] Script de migración de datos
- [ ] Validar migración en ambiente de desarrollo
- [ ] Documentar cambios en API

---

## 🎯 Próximos Pasos Recomendados

1. **Completar Domain Layer**: Arreglar `EntityCustomization` para seguir las reglas del proyecto (métodos `create()`, `update()`, tipos correctos)

2. **Diseñar nueva estructura de BD**: Definir tablas `entity_customizations`, actualizar `custom_fields`, `custom_field_values`, `field_configurations`

3. **Crear migración**: Script para migrar datos existentes de workflow a la nueva estructura

4. **Implementar Fase 2**: Crear repositorios nuevos y refactorizar existentes

5. **Implementar Fase 3**: Crear commands y queries nuevos

6. **Implementar Fase 4**: Actualizar presentación

7. **Actualizar Frontend**: Refactorizar componentes y servicios

8. **Testing**: Validar toda la funcionalidad

---

## 📝 Notas Adicionales

- El código antiguo en `src/customization/old/` debe mantenerse hasta que la migración esté completa
- Considerar crear un módulo de compatibilidad que traduzca llamadas antiguas a nuevas
- La estructura de `CustomField` como Value Object dentro de `EntityCustomization` es correcta
- `FieldConfiguration` puede necesitar un rediseño más genérico si se quiere usar fuera de workflows

---

**Última actualización**: 2025-01-22

