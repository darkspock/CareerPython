# Tareas de Refactorización del Módulo Customization

**Fecha de creación**: 2025-01-22  
**Objetivo**: Separar el módulo de customization de workflow para hacerlo genérico y reutilizable

---

## 📋 Resumen de Fases

- **Fase 1**: Domain Layer (Completar entidades y value objects)
- **Fase 2**: Infrastructure Layer (Repositorios y modelos)
- **Fase 3**: Application Layer (Commands, Queries, DTOs)
- **Fase 4**: Presentation Layer (Controllers, Routers, Schemas)
- **Fase 5**: Frontend (Componentes, Servicios, Tipos)
- **Fase 6**: Testing y Migración

---

## Fase 1: Domain Layer ✅ COMPLETADA

### 1.1. Completar EntityCustomization ✅

- [x] **Corregir tipos en `EntityCustomization`**
  - [x] Cambiar `created_at: int` → `created_at: datetime`
  - [x] Cambiar `updated_at: int` → `updated_at: datetime`
  - [x] Cambiar `validation: str` → `validation: Optional[str]`
  - [x] Cambiar `metadata: Dict[str, Any]` → `metadata: Dict[str, Any] = field(default_factory=dict)`

- [x] **Agregar método `create()` a `EntityCustomization`**
  - [x] Factory method estático
  - [x] Generar `EntityCustomizationId` si no se proporciona
  - [x] Validar que `entity_type` y `entity_id` sean válidos
  - [x] Validar que `fields` no esté vacío (o permitir vacío)
  - [x] Establecer `created_at` y `updated_at` a `datetime.utcnow()`
  - [x] Validar `validation` si se proporciona (JSON-Logic válido) - TODO: Implementar validación JSON-Logic

- [x] **Agregar método `update()` a `EntityCustomization`**
  - [x] Actualizar `fields` (lista completa)
  - [x] Actualizar `validation` (opcional)
  - [x] Actualizar `metadata` (opcional)
  - [x] Actualizar `updated_at` a `datetime.utcnow()`
  - [x] Retornar `None` (mutabilidad)

- [x] **Agregar métodos de mutación para campos**
  - [x] `add_field(field: CustomField) -> None` - Agregar campo
  - [x] `remove_field(field_id: CustomFieldId) -> None` - Eliminar campo
  - [x] `update_field(field_id: CustomFieldId, field: CustomField) -> None` - Actualizar campo
  - [x] `reorder_fields(field_ids_in_order: List[CustomFieldId]) -> None` - Reordenar campos

### 1.2. Completar CustomField Value Object ✅

- [x] **Corregir `CustomField` para usar `CustomFieldId`**
  - [x] Cambiar `id: str` → `id: CustomFieldId`
  - [x] Asegurar que sea inmutable (`frozen=True`)

- [x] **Agregar validaciones a `CustomField`**
  - [x] Validar que `field_key` sea válido (sin espacios, alfanumérico + underscore)
  - [x] Validar que `field_type` sea uno de los tipos permitidos
  - [x] Validar que `order_index >= 0`

- [x] **Crear factory method `create()` para `CustomField`**
  - [x] Generar `CustomFieldId` si no se proporciona
  - [x] Establecer `created_at` y `updated_at` a `datetime.utcnow()`
  - [x] Validar todos los campos

### 1.3. Completar Enums

- [ ] **Revisar `EntityCustomizationTypeEnum`**
  - [ ] Verificar que todos los valores terminen con el tipo correcto (no solo "Enum")
  - [ ] Agregar documentación a cada valor
  - [ ] Considerar agregar más tipos si es necesario (ej: `COMPANY`, `USER`, etc.)

### 1.4. Crear Excepciones de Dominio ✅

- [x] **Crear `EntityCustomizationNotFound`**
  - [x] Archivo: `src/customization/domain/exceptions/entity_customization_not_found.py`
  - [x] Hereda de `Exception`

- [x] **Crear `CustomFieldNotFound`**
  - [x] Archivo: `src/customization/domain/exceptions/custom_field_not_found.py`
  - [x] Hereda de `Exception`

- [x] **Crear `InvalidCustomFieldType`**
  - [x] Archivo: `src/customization/domain/exceptions/invalid_custom_field_type.py`
  - [x] Hereda de `Exception`

- [x] **Exportar excepciones en `__init__.py`**

---

## Fase 2: Infrastructure Layer

### 2.1. Crear Modelos SQLAlchemy

- [ ] **Crear `EntityCustomizationModel`**
  - [ ] Archivo: `src/customization/infrastructure/models/entity_customization_model.py`
  - [ ] Tabla: `entity_customizations`
  - [ ] Campos:
    - `id: Mapped[str]` (PK)
    - `entity_type: Mapped[str]` (Enum)
    - `entity_id: Mapped[str]` (index)
    - `validation: Mapped[Optional[str]]` (JSON-Logic)
    - `metadata: Mapped[Dict[str, Any]]` (JSON)
    - `created_at: Mapped[datetime]`
    - `updated_at: Mapped[datetime]`
  - [ ] Índice único: `(entity_type, entity_id)`

- [ ] **Refactorizar `CustomFieldModel`**
  - [ ] Archivo: `src/customization/infrastructure/models/custom_field_model.py`
  - [ ] Cambiar `workflow_id` → `entity_customization_id`
  - [ ] Cambiar FK de `workflows` → `entity_customizations`
  - [ ] Mantener `field_key`, `field_name`, `field_type`, `field_config`, `order_index`
  - [ ] Actualizar constraint único: `(entity_customization_id, field_key)`

- [ ] **Refactorizar `CustomFieldValueModel`**
  - [ ] Archivo: `src/customization/infrastructure/models/custom_field_value_model.py`
  - [ ] Cambiar estructura:
    - Eliminar `workflow_id`
    - Agregar `entity_type: Mapped[str]` (index)
    - Agregar `entity_id: Mapped[str]` (index)
  - [ ] Mantener `company_candidate_id` (para compatibilidad temporal, luego eliminar)
  - [ ] Mantener `values: Mapped[Dict[str, Any]]` (JSON)
  - [ ] Actualizar constraint único: `(entity_type, entity_id)` o `(company_candidate_id, entity_type, entity_id)`

- [ ] **Refactorizar `FieldConfigurationModel`**
  - [ ] Archivo: `src/customization/infrastructure/models/field_configuration_model.py`
  - [ ] Cambiar estructura:
    - Eliminar `stage_id` (o hacerlo opcional)
    - Agregar `entity_customization_id: Mapped[str]` (FK a `entity_customizations`)
    - Agregar `context_type: Mapped[Optional[str]]` (ej: "stage", "view", etc.)
    - Agregar `context_id: Mapped[Optional[str]]` (ej: stage_id, view_id, etc.)
  - [ ] Mantener `custom_field_id`, `visibility`
  - [ ] Actualizar constraint único: `(entity_customization_id, custom_field_id, context_type, context_id)`

### 2.2. Crear Interfaces de Repositorio

- [ ] **Crear `EntityCustomizationRepositoryInterface`**
  - [ ] Archivo: `src/customization/domain/interfaces/entity_customization_repository_interface.py`
  - [ ] Métodos:
    - `save(entity_customization: EntityCustomization) -> None`
    - `get_by_id(id: EntityCustomizationId) -> Optional[EntityCustomization]`
    - `get_by_entity(entity_type: EntityCustomizationTypeEnum, entity_id: str) -> Optional[EntityCustomization]`
    - `list_by_entity_type(entity_type: EntityCustomizationTypeEnum) -> List[EntityCustomization]`
    - `delete(id: EntityCustomizationId) -> None`

- [ ] **Refactorizar `CustomFieldRepositoryInterface`**
  - [ ] Archivo: `src/customization/domain/interfaces/custom_field_repository_interface.py`
  - [ ] Cambiar métodos:
    - `list_by_workflow(workflow_id)` → `list_by_entity_customization(entity_customization_id: EntityCustomizationId)`
    - `get_by_workflow_and_key(workflow_id, field_key)` → `get_by_entity_customization_and_key(entity_customization_id, field_key)`
  - [ ] Mantener: `save()`, `get_by_id()`, `delete()`

- [ ] **Refactorizar `CustomFieldValueRepositoryInterface`**
  - [ ] Archivo: `src/customization/domain/interfaces/custom_field_value_repository_interface.py`
  - [ ] Cambiar métodos:
    - `get_by_company_candidate_and_workflow()` → `get_by_entity(entity_type, entity_id)`
    - `get_all_by_company_candidate()` → `get_all_by_entity_type_and_id(entity_type, entity_id)`
  - [ ] Agregar: `save()`, `get_by_id()`, `delete()`

- [ ] **Refactorizar `FieldConfigurationRepositoryInterface`**
  - [ ] Archivo: `src/customization/domain/interfaces/field_configuration_repository_interface.py`
  - [ ] Cambiar métodos:
    - `list_by_stage(stage_id)` → `list_by_entity_customization(entity_customization_id, context_type=None, context_id=None)`
  - [ ] Mantener: `save()`, `get_by_id()`, `delete()`

### 2.3. Implementar Repositorios

- [ ] **Implementar `EntityCustomizationRepository`**
  - [ ] Archivo: `src/customization/infrastructure/repositories/entity_customization_repository.py`
  - [ ] Implementar todos los métodos de la interface
  - [ ] Métodos `_to_domain()` y `_to_model()`
  - [ ] Manejar conversión de `EntityCustomizationTypeEnum` ↔ `str`

- [ ] **Refactorizar `CustomFieldRepository`**
  - [ ] Archivo: `src/customization/infrastructure/repositories/custom_field_repository.py`
  - [ ] Actualizar para usar `EntityCustomizationId` en lugar de `WorkflowId`
  - [ ] Actualizar métodos `_to_domain()` y `_to_model()`
  - [ ] Eliminar dependencias de `workflow` domain

- [ ] **Refactorizar `CustomFieldValueRepository`**
  - [ ] Archivo: `src/customization/infrastructure/repositories/custom_field_value_repository.py`
  - [ ] Actualizar para usar `entity_type` + `entity_id` en lugar de `workflow_id`
  - [ ] Actualizar métodos `_to_domain()` y `_to_model()`
  - [ ] Eliminar dependencias de `workflow` domain

- [ ] **Refactorizar `FieldConfigurationRepository`**
  - [ ] Archivo: `src/customization/infrastructure/repositories/field_configuration_repository.py`
  - [ ] Actualizar para usar `entity_customization_id` + `context_type` + `context_id`
  - [ ] Actualizar métodos `_to_domain()` y `_to_model()`

### 2.4. Crear Migración de Base de Datos

- [ ] **Crear migración Alembic**
  - [ ] Comando: `make revision m="refactor_customization_to_entity_based"`
  - [ ] Archivo: `alembic/versions/XXXXX_refactor_customization_to_entity_based.py`

- [ ] **Pasos de la migración**:
  - [ ] Crear tabla `entity_customizations`
  - [ ] Migrar datos de `workflow_custom_fields`:
    - [ ] Para cada `workflow_id`, crear `EntityCustomization` con `entity_type=CANDIDATE_APPLICATION`, `entity_id=workflow_id`
    - [ ] Migrar campos a nueva estructura con `entity_customization_id`
  - [ ] Actualizar tabla `custom_field_values`:
    - [ ] Agregar columnas `entity_type` y `entity_id`
    - [ ] Migrar datos: `workflow_id` → `entity_type=CANDIDATE_APPLICATION`, `entity_id=workflow_id`
    - [ ] Eliminar columna `workflow_id` (o mantener temporalmente)
  - [ ] Actualizar tabla `stage_field_configurations`:
    - [ ] Agregar columnas `entity_customization_id`, `context_type`, `context_id`
    - [ ] Migrar datos: `stage_id` → `context_type=stage`, `context_id=stage_id`
    - [ ] Obtener `entity_customization_id` desde `custom_field_id` → `entity_customization_id`
  - [ ] Actualizar tabla `custom_fields`:
    - [ ] Agregar columna `entity_customization_id`
    - [ ] Migrar datos: obtener `entity_customization_id` desde `workflow_id`
    - [ ] Eliminar columna `workflow_id` (o mantener temporalmente)
  - [ ] Crear índices necesarios
  - [ ] Validar integridad de datos

- [ ] **Testing de migración**:
  - [ ] Probar en base de datos de desarrollo
  - [ ] Verificar que todos los datos se migraron correctamente
  - [ ] Verificar que no hay datos huérfanos
  - [ ] Verificar que las foreign keys funcionan correctamente

---

## Fase 3: Application Layer

### 3.1. Commands

- [ ] **Crear `CreateEntityCustomizationCommand`**
  - [ ] Archivo: `src/customization/application/commands/create_entity_customization_command.py`
  - [ ] Campos: `entity_type: EntityCustomizationTypeEnum`, `entity_id: str`, `fields: List[CustomField]`, `validation: Optional[str]`, `metadata: Optional[Dict[str, Any]]`
  - [ ] Handler: `CreateEntityCustomizationCommandHandler`
  - [ ] Usar `EntityCustomization.create()`
  - [ ] Guardar en repositorio

- [ ] **Crear `UpdateEntityCustomizationCommand`**
  - [ ] Archivo: `src/customization/application/commands/update_entity_customization_command.py`
  - [ ] Campos: `id: EntityCustomizationId`, `fields: Optional[List[CustomField]]`, `validation: Optional[str]`, `metadata: Optional[Dict[str, Any]]`
  - [ ] Handler: `UpdateEntityCustomizationCommandHandler`
  - [ ] Usar `EntityCustomization.update()`
  - [ ] Guardar en repositorio

- [ ] **Crear `AddCustomFieldToEntityCommand`**
  - [ ] Archivo: `src/customization/application/commands/add_custom_field_to_entity_command.py`
  - [ ] Campos: `entity_customization_id: EntityCustomizationId`, `field: CustomField`
  - [ ] Handler: `AddCustomFieldToEntityCommandHandler`
  - [ ] Usar `EntityCustomization.add_field()`
  - [ ] Guardar campo en repositorio

- [ ] **Refactorizar `UpdateCustomFieldCommand`**
  - [ ] Archivo: `src/customization/application/commands/update_custom_field_command.py`
  - [ ] Actualizar para usar `CustomFieldId` en lugar de `str`
  - [ ] Handler: Actualizar para usar repositorio nuevo

- [ ] **Refactorizar `DeleteCustomFieldCommand`**
  - [ ] Archivo: `src/customization/application/commands/delete_custom_field_command.py`
  - [ ] Actualizar para usar `CustomFieldId`
  - [ ] Handler: Eliminar de `EntityCustomization` y repositorio

- [ ] **Refactorizar `ReorderCustomFieldCommand`**
  - [ ] Archivo: `src/customization/application/commands/reorder_custom_field_command.py`
  - [ ] Actualizar para usar `EntityCustomizationId` y `List[CustomFieldId]`
  - [ ] Handler: Usar `EntityCustomization.reorder_fields()`

- [ ] **Crear `SetCustomFieldValueCommand`**
  - [ ] Archivo: `src/customization/application/commands/set_custom_field_value_command.py`
  - [ ] Campos: `entity_type: EntityCustomizationTypeEnum`, `entity_id: str`, `custom_field_id: CustomFieldId`, `value: Any`
  - [ ] Handler: `SetCustomFieldValueCommandHandler`
  - [ ] Reemplaza `CreateCustomFieldValueCommand` y `UpdateCustomFieldValueCommand`

- [ ] **Refactorizar `DeleteCustomFieldValueCommand`**
  - [ ] Archivo: `src/customization/application/commands/delete_custom_field_value_command.py`
  - [ ] Actualizar para usar `entity_type` + `entity_id` en lugar de `workflow_id`

- [ ] **Refactorizar `ConfigureFieldVisibilityCommand`**
  - [ ] Archivo: `src/customization/application/commands/configure_field_visibility_command.py`
  - [ ] Actualizar para usar `entity_customization_id` + `context_type` + `context_id`
  - [ ] Reemplaza `ConfigureStageFieldCommand`

- [ ] **Crear `UpdateFieldVisibilityCommand`**
  - [ ] Archivo: `src/customization/application/commands/update_field_visibility_command.py`
  - [ ] Actualizar para usar nueva estructura

### 3.2. Queries

- [ ] **Crear `GetEntityCustomizationQuery`**
  - [ ] Archivo: `src/customization/application/queries/get_entity_customization_query.py`
  - [ ] Campos: `entity_type: EntityCustomizationTypeEnum`, `entity_id: str`
  - [ ] Handler: `GetEntityCustomizationQueryHandler`
  - [ ] Retorna: `EntityCustomizationDto`

- [ ] **Crear `GetEntityCustomizationByIdQuery`**
  - [ ] Archivo: `src/customization/application/queries/get_entity_customization_by_id_query.py`
  - [ ] Campos: `id: EntityCustomizationId`
  - [ ] Handler: `GetEntityCustomizationByIdQueryHandler`
  - [ ] Retorna: `EntityCustomizationDto`

- [ ] **Refactorizar `ListCustomFieldsByWorkflowQuery` → `ListCustomFieldsByEntityQuery`**
  - [ ] Archivo: `src/customization/application/queries/list_custom_fields_by_entity_query.py`
  - [ ] Campos: `entity_type: EntityCustomizationTypeEnum`, `entity_id: str`
  - [ ] Handler: `ListCustomFieldsByEntityQueryHandler`
  - [ ] Retorna: `List[CustomFieldDto]`

- [ ] **Refactorizar `GetCustomFieldByIdQuery`**
  - [ ] Archivo: `src/customization/application/queries/get_custom_field_by_id_query.py`
  - [ ] Actualizar para usar `CustomFieldId`

- [ ] **Refactorizar `GetCustomFieldValuesByCompanyCandidateQuery` → `GetCustomFieldValuesByEntityQuery`**
  - [ ] Archivo: `src/customization/application/queries/get_custom_field_values_by_entity_query.py`
  - [ ] Campos: `entity_type: EntityCustomizationTypeEnum`, `entity_id: str`
  - [ ] Handler: `GetCustomFieldValuesByEntityQueryHandler`
  - [ ] Retorna: `Dict[str, Any]` (field_key -> value)

- [ ] **Refactorizar `GetAllCustomFieldValuesByCompanyCandidateQuery` → `GetAllCustomFieldValuesByEntityQuery`**
  - [ ] Archivo: `src/customization/application/queries/get_all_custom_field_values_by_entity_query.py`
  - [ ] Campos: `entity_type: EntityCustomizationTypeEnum`, `entity_id: str`
  - [ ] Handler: `GetAllCustomFieldValuesByEntityQueryHandler`
  - [ ] Retorna: `Dict[str, Dict[str, Any]]` (organizado por entity_customization_id)

- [ ] **Refactorizar `ListFieldConfigurationsByStageQuery` → `ListFieldConfigurationsByEntityQuery`**
  - [ ] Archivo: `src/customization/application/queries/list_field_configurations_by_entity_query.py`
  - [ ] Campos: `entity_customization_id: EntityCustomizationId`, `context_type: Optional[str]`, `context_id: Optional[str]`
  - [ ] Handler: `ListFieldConfigurationsByEntityQueryHandler`
  - [ ] Retorna: `List[FieldConfigurationDto]`

### 3.3. DTOs

- [ ] **Crear `EntityCustomizationDto`**
  - [ ] Archivo: `src/customization/application/dtos/entity_customization_dto.py`
  - [ ] Campos: `id: str`, `entity_type: str`, `entity_id: str`, `fields: List[CustomFieldDto]`, `validation: Optional[str]`, `metadata: Dict[str, Any]`, `created_at: datetime`, `updated_at: datetime`

- [ ] **Refactorizar `CustomFieldDto`**
  - [ ] Archivo: `src/customization/application/dtos/custom_field_dto.py`
  - [ ] Cambiar `workflow_id: str` → `entity_customization_id: str`

- [ ] **Refactorizar `CustomFieldValueDto`**
  - [ ] Archivo: `src/customization/application/dtos/custom_field_value_dto.py`
  - [ ] Cambiar `workflow_id: str` → `entity_type: str`, `entity_id: str`
  - [ ] Mantener `values: Dict[str, Any]`

- [ ] **Refactorizar `FieldConfigurationDto`**
  - [ ] Archivo: `src/customization/application/dtos/field_configuration_dto.py`
  - [ ] Cambiar `stage_id: str` → `entity_customization_id: str`, `context_type: Optional[str]`, `context_id: Optional[str]`

### 3.4. Mappers

- [ ] **Crear `EntityCustomizationMapper`**
  - [ ] Archivo: `src/customization/application/mappers/entity_customization_mapper.py`
  - [ ] Métodos: `entity_to_dto()`, `dto_to_entity()` (si es necesario)

- [ ] **Refactorizar `CustomFieldMapper`**
  - [ ] Archivo: `src/customization/application/mappers/custom_field_mapper.py`
  - [ ] Actualizar para usar `entity_customization_id` en lugar de `workflow_id`

- [ ] **Refactorizar `CustomFieldValueMapper`**
  - [ ] Archivo: `src/customization/application/mappers/custom_field_value_mapper.py`
  - [ ] Actualizar para usar `entity_type` + `entity_id`

- [ ] **Refactorizar `FieldConfigurationMapper`**
  - [ ] Archivo: `src/customization/application/mappers/field_configuration_mapper.py`
  - [ ] Actualizar para usar nueva estructura

### 3.5. Registrar en Container

- [ ] **Actualizar `core/container.py`**
  - [ ] Registrar `EntityCustomizationRepository`
  - [ ] Registrar todos los Command Handlers nuevos
  - [ ] Registrar todos los Query Handlers nuevos
  - [ ] Actualizar registros de handlers antiguos (o mantener ambos temporalmente)

---

## Fase 4: Presentation Layer

### 4.1. Schemas

- [ ] **Crear `CreateEntityCustomizationRequest`**
  - [ ] Archivo: `adapters/http/customization/schemas/create_entity_customization_request.py`
  - [ ] Campos: `entity_type: str`, `entity_id: str`, `fields: List[CreateCustomFieldRequest]`, `validation: Optional[str]`, `metadata: Optional[Dict[str, Any]]`

- [ ] **Crear `UpdateEntityCustomizationRequest`**
  - [ ] Archivo: `adapters/http/customization/schemas/update_entity_customization_request.py`
  - [ ] Campos: `fields: Optional[List[CreateCustomFieldRequest]]`, `validation: Optional[str]`, `metadata: Optional[Dict[str, Any]]`

- [ ] **Crear `EntityCustomizationResponse`**
  - [ ] Archivo: `adapters/http/customization/schemas/entity_customization_response.py`
  - [ ] Campos: `id: str`, `entity_type: str`, `entity_id: str`, `fields: List[CustomFieldResponse]`, `validation: Optional[str]`, `metadata: Dict[str, Any]`, `created_at: datetime`, `updated_at: datetime`

- [ ] **Refactorizar `CreateCustomFieldRequest`**
  - [ ] Archivo: `adapters/http/customization/schemas/create_custom_field_request.py`
  - [ ] Cambiar `workflow_id: str` → `entity_customization_id: str`
  - [ ] O alternativamente: `entity_type: str`, `entity_id: str` (para crear campo directamente en entidad)

- [ ] **Refactorizar `UpdateCustomFieldRequest`**
  - [ ] Archivo: `adapters/http/customization/schemas/update_custom_field_request.py`
  - [ ] Mantener campos actuales (no necesita workflow_id)

- [ ] **Refactorizar `CustomFieldResponse`**
  - [ ] Archivo: `adapters/http/customization/schemas/custom_field_response.py`
  - [ ] Cambiar `workflow_id: str` → `entity_customization_id: str`

- [ ] **Refactorizar `CreateCustomFieldValueRequest` → `SetCustomFieldValueRequest`**
  - [ ] Archivo: `adapters/http/customization/schemas/set_custom_field_value_request.py`
  - [ ] Cambiar `workflow_id: str` → `entity_type: str`, `entity_id: str`

- [ ] **Refactorizar `CustomFieldValueResponse`**
  - [ ] Archivo: `adapters/http/customization/schemas/custom_field_value_response.py`
  - [ ] Cambiar `workflow_id: str` → `entity_type: str`, `entity_id: str`

- [ ] **Refactorizar `ConfigureStageFieldRequest` → `ConfigureFieldVisibilityRequest`**
  - [ ] Archivo: `adapters/http/customization/schemas/configure_field_visibility_request.py`
  - [ ] Cambiar `stage_id: str` → `entity_customization_id: str`, `context_type: Optional[str]`, `context_id: Optional[str]`

- [ ] **Refactorizar `FieldConfigurationResponse`**
  - [ ] Archivo: `adapters/http/customization/schemas/field_configuration_response.py`
  - [ ] Cambiar `stage_id: str` → `entity_customization_id: str`, `context_type: Optional[str]`, `context_id: Optional[str]`

### 4.2. Controllers

- [ ] **Crear `EntityCustomizationController`**
  - [ ] Archivo: `adapters/http/customization/controllers/entity_customization_controller.py`
  - [ ] Métodos:
    - [ ] `create_entity_customization(request: CreateEntityCustomizationRequest) -> EntityCustomizationResponse`
    - [ ] `get_entity_customization(entity_type: str, entity_id: str) -> EntityCustomizationResponse`
    - [ ] `get_entity_customization_by_id(id: str) -> EntityCustomizationResponse`
    - [ ] `update_entity_customization(id: str, request: UpdateEntityCustomizationRequest) -> EntityCustomizationResponse`
    - [ ] `delete_entity_customization(id: str) -> None`

- [ ] **Refactorizar `CustomFieldController`**
  - [ ] Archivo: `adapters/http/customization/controllers/custom_field_controller.py`
  - [ ] Actualizar métodos:
    - [ ] `create_custom_field()`: Usar `entity_type` + `entity_id` o `entity_customization_id`
    - [ ] `list_custom_fields_by_workflow()` → `list_custom_fields_by_entity()`: Usar `entity_type` + `entity_id`
    - [ ] Mantener otros métodos (ya usan field_id)

- [ ] **Refactorizar `CustomFieldValueController`**
  - [ ] Archivo: `adapters/http/customization/controllers/custom_field_value_controller.py`
  - [ ] Actualizar métodos:
    - [ ] `create_custom_field_value()` → `set_custom_field_value()`: Usar `entity_type` + `entity_id`
    - [ ] `get_custom_field_values_by_company_candidate()` → `get_custom_field_values_by_entity()`: Usar `entity_type` + `entity_id`
    - [ ] `get_all_custom_field_values_by_company_candidate()` → `get_all_custom_field_values_by_entity()`: Usar `entity_type` + `entity_id`
    - [ ] `upsert_single_field_value()`: Usar `entity_type` + `entity_id`

### 4.3. Routers

- [ ] **Crear `entity_customization_router.py`**
  - [ ] Archivo: `adapters/http/customization/routers/entity_customization_router.py`
  - [ ] Endpoints:
    - [ ] `POST /api/entity-customizations` - Crear personalización
    - [ ] `GET /api/entity-customizations/{entity_type}/{entity_id}` - Obtener por entidad
    - [ ] `GET /api/entity-customizations/{id}` - Obtener por ID
    - [ ] `PUT /api/entity-customizations/{id}` - Actualizar
    - [ ] `DELETE /api/entity-customizations/{id}` - Eliminar

- [ ] **Refactorizar `custom_field_router.py`**
  - [ ] Archivo: `adapters/http/customization/routers/custom_field_router.py`
  - [ ] Actualizar endpoints:
    - [ ] `GET /api/custom-fields/workflow/{workflow_id}` → `GET /api/custom-fields/entity/{entity_type}/{entity_id}`
    - [ ] `POST /api/custom-fields/`: Actualizar request schema
    - [ ] Mantener otros endpoints (usan field_id)

- [ ] **Refactorizar `custom_field_value_router.py`**
  - [ ] Archivo: `adapters/http/customization/routers/custom_field_value_router.py`
  - [ ] Actualizar endpoints:
    - [ ] `GET /api/company-workflow/custom-field-values/company-candidate/{id}` → `GET /api/custom-field-values/entity/{entity_type}/{entity_id}`
    - [ ] `GET /api/company-workflow/custom-field-values/company-candidate/{id}/all` → `GET /api/custom-field-values/entity/{entity_type}/{entity_id}/all`
    - [ ] `PUT /api/company-workflow/custom-field-values/company-candidate/{id}/field/{field_id}` → `PUT /api/custom-field-values/entity/{entity_type}/{entity_id}/field/{field_id}`
    - [ ] Actualizar otros endpoints

- [ ] **Actualizar `main.py`**
  - [ ] Registrar nuevos routers
  - [ ] Actualizar imports

---

## Fase 5: Frontend

### 5.1. Tipos TypeScript

- [ ] **Actualizar `workflow.ts` o crear `customization.ts`**
  - [ ] Archivo: `client-vite/src/types/customization.ts` (nuevo) o actualizar `workflow.ts`
  - [ ] Crear `EntityCustomization` type:
    ```typescript
    export interface EntityCustomization {
      id: string;
      entity_type: EntityCustomizationType;
      entity_id: string;
      fields: CustomField[];
      validation?: string;
      metadata: Record<string, any>;
      created_at: string;
      updated_at: string;
    }
    ```
  - [ ] Crear `EntityCustomizationType` enum:
    ```typescript
    export type EntityCustomizationType = 'JobPosition' | 'CandidateApplication' | 'Candidate';
    ```
  - [ ] Actualizar `CustomField`:
    - [ ] Cambiar `workflow_id: string` → `entity_customization_id: string`
  - [ ] Actualizar `CustomFieldValue`:
    - [ ] Cambiar `workflow_id: string` → `entity_type: string`, `entity_id: string`
  - [ ] Actualizar `FieldConfiguration`:
    - [ ] Cambiar `stage_id: string` → `entity_customization_id: string`, `context_type?: string`, `context_id?: string`

### 5.2. Servicios

- [ ] **Crear `EntityCustomizationService`**
  - [ ] Archivo: `client-vite/src/services/entityCustomizationService.ts`
  - [ ] Métodos:
    - [ ] `createEntityCustomization(request)`
    - [ ] `getEntityCustomization(entityType, entityId)`
    - [ ] `getEntityCustomizationById(id)`
    - [ ] `updateEntityCustomization(id, request)`
    - [ ] `deleteEntityCustomization(id)`

- [ ] **Refactorizar `CustomFieldService`**
  - [ ] Archivo: `client-vite/src/services/customFieldService.ts`
  - [ ] Actualizar métodos:
    - [ ] `listCustomFieldsByWorkflow(workflowId)` → `listCustomFieldsByEntity(entityType, entityId)`
    - [ ] `createCustomField(request)`: Actualizar request para usar `entity_customization_id` o `entity_type` + `entity_id`
    - [ ] Mantener otros métodos

- [ ] **Refactorizar `CustomFieldValueService`**
  - [ ] Archivo: `client-vite/src/services/customFieldValueService.ts` (crear si no existe)
  - [ ] Métodos:
    - [ ] `setCustomFieldValue(entityType, entityId, fieldId, value)`
    - [ ] `getCustomFieldValuesByEntity(entityType, entityId)`
    - [ ] `getAllCustomFieldValuesByEntity(entityType, entityId)`
    - [ ] `deleteCustomFieldValue(valueId)`

### 5.3. Componentes

- [ ] **Crear `EntityCustomizationEditor`**
  - [ ] Archivo: `client-vite/src/components/customization/EntityCustomizationEditor.tsx`
  - [ ] Props: `entityType: EntityCustomizationType`, `entityId: string`
  - [ ] Funcionalidad: Editor completo de personalización de entidad
  - [ ] Incluir: Lista de campos, agregar/editar/eliminar campos, validaciones, metadata

- [ ] **Refactorizar `CustomFieldEditor`**
  - [ ] Archivo: `client-vite/src/components/workflow/CustomFieldEditor.tsx`
  - [ ] Cambiar props: `workflowId: string` → `entityType: EntityCustomizationType`, `entityId: string`
  - [ ] Actualizar llamadas a servicio: `listCustomFieldsByEntity(entityType, entityId)`
  - [ ] Actualizar creación de campos: usar `entity_customization_id` o `entity_type` + `entity_id`

- [ ] **Refactorizar `DynamicCustomFields`**
  - [ ] Archivo: `client-vite/src/components/jobPosition/DynamicCustomFields.tsx`
  - [ ] Cambiar props: `workflow` → `entityCustomization: EntityCustomization`
  - [ ] Actualizar lógica para usar `entityCustomization.fields` en lugar de `workflow.custom_fields_config`
  - [ ] Mantener compatibilidad con `currentStage.field_visibility` si es necesario

- [ ] **Refactorizar `CustomFieldsCard`**
  - [ ] Archivo: `client-vite/src/components/candidate/CustomFieldsCard.tsx`
  - [ ] Actualizar para usar `entity_type` + `entity_id` en lugar de `workflow_id`
  - [ ] Actualizar llamadas a servicio

- [ ] **Actualizar páginas que usan customization**
  - [ ] `WorkflowAdvancedConfigPage.tsx`: Actualizar para usar nueva estructura
  - [ ] `CandidateDetailPage.tsx`: Actualizar para usar nueva estructura
  - [ ] Cualquier otra página que use custom fields

---

## Fase 6: Testing y Migración

### 6.1. Tests Unitarios

- [ ] **Tests de Domain Layer**
  - [ ] Tests de `EntityCustomization.create()`
  - [ ] Tests de `EntityCustomization.update()`
  - [ ] Tests de `EntityCustomization.add_field()`, `remove_field()`, `update_field()`, `reorder_fields()`
  - [ ] Tests de `CustomField.create()`
  - [ ] Tests de validaciones

- [ ] **Tests de Repositorios**
  - [ ] Tests de `EntityCustomizationRepository`
  - [ ] Tests de `CustomFieldRepository` (refactorizado)
  - [ ] Tests de `CustomFieldValueRepository` (refactorizado)
  - [ ] Tests de `FieldConfigurationRepository` (refactorizado)

- [ ] **Tests de Commands y Queries**
  - [ ] Tests de todos los Command Handlers nuevos
  - [ ] Tests de todos los Query Handlers nuevos
  - [ ] Tests de conversión de Value Objects

### 6.2. Tests de Integración

- [ ] **Tests de Endpoints**
  - [ ] Tests de `EntityCustomizationController`
  - [ ] Tests de `CustomFieldController` (refactorizado)
  - [ ] Tests de `CustomFieldValueController` (refactorizado)
  - [ ] Tests de todos los routers

- [ ] **Tests de Migración**
  - [ ] Verificar que datos se migraron correctamente
  - [ ] Verificar que no hay datos huérfanos
  - [ ] Verificar que foreign keys funcionan

### 6.3. Scripts de Migración

- [ ] **Crear script de migración de datos**
  - [ ] Archivo: `scripts/migrate_customization_data.py`
  - [ ] Migrar workflows a entity_customizations
  - [ ] Migrar custom_fields
  - [ ] Migrar custom_field_values
  - [ ] Migrar field_configurations
  - [ ] Validar integridad

- [ ] **Crear script de rollback**
  - [ ] Archivo: `scripts/rollback_customization_migration.py`
  - [ ] Revertir cambios si es necesario

### 6.4. Documentación

- [ ] **Actualizar documentación de API**
  - [ ] Documentar nuevos endpoints
  - [ ] Documentar cambios en endpoints existentes
  - [ ] Documentar deprecación de endpoints antiguos

- [ ] **Actualizar guías de desarrollo**
  - [ ] Documentar cómo usar el nuevo sistema de customization
  - [ ] Ejemplos de uso
  - [ ] Migración de código existente

---

## Notas Importantes

### Compatibilidad Temporal

- [ ] **Mantener endpoints antiguos** (opcional, para transición suave)
  - [ ] Crear adaptadores que traduzcan `workflow_id` → `entity_type` + `entity_id`
  - [ ] Marcar endpoints como deprecated
  - [ ] Planificar fecha de eliminación

### Validaciones

- [ ] **Validar JSON-Logic**
  - [ ] Crear servicio de validación de JSON-Logic
  - [ ] Validar en `EntityCustomization.create()` y `update()`

### Metadata

- [ ] **Definir estructura de metadata por tipo de entidad**
  - [ ] Documentar qué metadata se espera para cada `EntityCustomizationType`
  - [ ] Validar metadata en creación/actualización

---

## Priorización

### Alta Prioridad (Bloqueantes)
1. Completar Domain Layer (Fase 1)
2. Crear modelos y repositorios nuevos (Fase 2.1, 2.2, 2.3)
3. Crear migración de base de datos (Fase 2.4)

### Media Prioridad (Funcionalidad Core)
4. Crear Commands y Queries nuevos (Fase 3.1, 3.2)
5. Crear DTOs y Mappers (Fase 3.3, 3.4)
6. Crear Controllers y Routers nuevos (Fase 4.2, 4.3)

### Baja Prioridad (Mejoras y Frontend)
7. Actualizar Frontend (Fase 5)
8. Testing completo (Fase 6)
9. Documentación (Fase 6.4)

---

**Última actualización**: 2025-01-22

