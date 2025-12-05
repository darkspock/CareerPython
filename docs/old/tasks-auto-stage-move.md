# Tareas: Implementación de Auto-Stage-Move Rules

**Fecha:** 2025-01-24  
**Referencia:** `docs/auto-stage-move-rules.md`

---

## Fase 1: Fundamentos (Prioridad Alta) 🔴

### 1.1 Implementar Evaluador JsonLogic
- [ ] Instalar librería `json-logic-py` en `requirements.txt`
- [ ] Crear servicio `JsonLogicEvaluatorService` en `src/shared_bc/customization/field_validation/application/services/`
- [ ] Implementar método `evaluate(rules: dict, data: dict) -> bool`
- [ ] Reemplazar el placeholder en `move_job_position_to_stage.py:198-224`
- [ ] Crear tests unitarios para el evaluador
- [ ] Integrar en `ChangeStageCommandHandler` para validar antes de cambiar stage

### 1.2 Agregar Propiedad `auto_move_to_next_stage`
- [ ] Crear migración: `make revision m="add auto_move_to_next_stage to workflow_stages"`
  ```sql
  ALTER TABLE workflow_stages ADD COLUMN auto_move_to_next_stage BOOLEAN DEFAULT FALSE;
  ```
- [ ] Actualizar modelo `WorkflowStageModel` en `src/shared_bc/customization/workflow/infrastructure/models/`
- [ ] Actualizar entidad `WorkflowStage` en `src/shared_bc/customization/workflow/domain/entities/`
- [ ] Actualizar DTOs y mappers
- [ ] Actualizar schemas de request/response en adapters
- [ ] Actualizar frontend para mostrar/editar esta propiedad

### 1.3 Crear StageValidationOrchestrator
- [ ] Crear servicio `StageValidationOrchestrator` en `src/shared_bc/customization/workflow/domain/services/`
- [ ] Métodos a implementar:
  - `validate_all(candidate, target_stage) -> List[ValidationResult]`
  - `can_move_to_stage(candidate, target_stage) -> bool`
  - `get_blocking_errors(candidate, target_stage) -> List[str]`
- [ ] Inyectar en `ChangeStageCommandHandler`
- [ ] Integrar con `JsonLogicEvaluatorService`
- [ ] Crear tests de integración

---

## Fase 2: Validaciones de Campos Nativos (Prioridad Media) 🟡

### 2.1 Crear NativeFieldValidationService
- [ ] Crear servicio en `src/shared_bc/customization/field_validation/application/services/native_field_validation_service.py`
- [ ] Implementar validadores:
  - [ ] `validate_work_modality(candidate, required_modalities: List[str]) -> ValidationResult`
  - [ ] `validate_languages(candidate, required_languages: List[str], min_level: str) -> ValidationResult`
  - [ ] `validate_salary_range(candidate, min_salary: float, max_salary: float) -> ValidationResult`
  - [ ] `validate_location(candidate, allowed_countries: List[str], allowed_cities: List[str]) -> ValidationResult`
- [ ] Crear tests unitarios para cada validador

### 2.2 Extender ValidationRuleType
- [ ] Agregar `NATIVE_FIELD = "NATIVE_FIELD"` a `ValidationRuleType` enum
- [ ] Actualizar mappers para manejar el nuevo tipo
- [ ] Crear migración si es necesario para el enum en BD

### 2.3 Integrar en StageValidationOrchestrator
- [ ] Inyectar `NativeFieldValidationService` en el orquestador
- [ ] Agregar lógica para ejecutar validaciones nativas junto con JsonLogic
- [ ] Actualizar tests de integración

### 2.4 UI para Configurar Validaciones Nativas
- [ ] Crear componente `NativeFieldValidationConfig` en frontend
- [ ] Agregar al formulario de edición de Stage
- [ ] Permitir seleccionar campos nativos y definir reglas

---

## Fase 3: Anti-Spam y Límites (Prioridad Baja) 🟢

### 3.1 Validación de Aplicaciones Repetidas
- [ ] Agregar métodos al repositorio `CandidateApplicationRepository`:
  - [ ] `count_applications_to_position_in_period(candidate_id, position_id, days) -> int`
  - [ ] `count_applications_to_company_in_period(candidate_id, company_id, days) -> int`
- [ ] Crear `ApplicationFrequencyValidationService`
- [ ] Crear entidad `CompanyApplicationSettings` con:
  - `max_applications_per_position_days: int`
  - `max_applications_per_company_days: int`
  - `max_applications_per_company_count: int`
- [ ] Integrar validación en `CreateCandidateApplicationCommandHandler`

### 3.2 Detector de Spam Básico
- [ ] Crear servicio `SpamDetectionService` en `src/shared_bc/customization/field_validation/application/services/`
- [ ] Implementar detectores:
  - [ ] `check_application_rate(candidate_id) -> SpamScore` (muchas aplicaciones en poco tiempo)
  - [ ] `check_email_domain(email) -> SpamScore` (dominios desechables)
  - [ ] `calculate_spam_score(candidate) -> float`
- [ ] Crear lista de dominios de email desechables (blacklist)
- [ ] Configuración de umbral de spam por compañía

### 3.3 Dashboard de Spam
- [ ] Crear página `/company/settings/spam` en frontend
- [ ] Mostrar lista de candidatos marcados como spam
- [ ] Permitir marcar como "no spam" (falso positivo)
- [ ] Mostrar estadísticas de spam detectado

---

## Fase 4: Auto-movimiento Automático (Opcional) 🔵

### 4.1 Crear Job de Auto-movimiento
- [ ] Crear comando `AutoMoveEligibleCandidatesCommand`
- [ ] Implementar handler que:
  - Busque candidatos en stages con `auto_move_to_next_stage=True`
  - Ejecute `StageValidationOrchestrator.validate_all()` para cada uno
  - Mueva automáticamente si todas las validaciones pasan
  - Registre logs de movimientos automáticos
- [ ] Configurar job en Dramatiq/Celery para ejecución periódica (cada hora)

### 4.2 Auto-rechazo por Validaciones Fallidas
- [ ] Implementar lógica de auto-rechazo cuando `ValidationRule.auto_reject=True`
- [ ] Crear stage de rechazo por defecto si no existe
- [ ] Enviar notificación al candidato (usar `email_template_id` configurado)
- [ ] Registrar en historial del candidato el motivo del rechazo

### 4.3 Notificaciones de Auto-movimiento
- [ ] Crear templates de email para:
  - Candidato movido automáticamente a siguiente etapa
  - Candidato rechazado automáticamente (con motivo)
- [ ] Integrar con sistema de notificaciones existente
- [ ] Permitir configurar qué notificaciones enviar por stage

### 4.4 Configuración por Company
- [ ] Crear `CompanyAutoMoveSettings`:
  - `enable_auto_move: bool`
  - `auto_move_check_interval_hours: int`
  - `require_manual_review_for_rejections: bool`
- [ ] UI para configurar estas opciones en `/company/settings/automation`

---

## Resumen de Archivos a Crear/Modificar

### Nuevos Archivos:
```
src/shared_bc/customization/field_validation/application/services/
├── json_logic_evaluator_service.py
├── native_field_validation_service.py
├── application_frequency_validation_service.py
└── spam_detection_service.py

src/shared_bc/customization/workflow/domain/services/
└── stage_validation_orchestrator.py

src/company_bc/company/domain/entities/
└── company_application_settings.py

alembic/versions/
└── xxxx_add_auto_move_to_workflow_stages.py
```

### Archivos a Modificar:
```
src/shared_bc/customization/workflow/domain/entities/workflow_stage.py
src/shared_bc/customization/workflow/infrastructure/models/workflow_stage_model.py
src/shared_bc/customization/field_validation/domain/enums/validation_rule_type.py
src/company_bc/company_candidate/application/commands/change_stage_command.py
src/company_bc/candidate_application/infrastructure/repositories/candidate_application_repository.py
core/containers/*.py (para inyección de nuevos servicios)
requirements.txt (agregar json-logic-py)
```

---

## Estimación de Tiempo

| Fase | Duración Estimada | Dependencias |
|------|-------------------|--------------|
| Fase 1 | 2-3 días | Ninguna |
| Fase 2 | 2 días | Fase 1 |
| Fase 3 | 2-3 días | Fase 1 |
| Fase 4 | 3-4 días | Fases 1, 2, 3 |

**Total estimado:** 9-12 días de desarrollo

---

## Criterios de Aceptación

### Fase 1 Completada Cuando:
- [ ] JsonLogic evalúa reglas correctamente en tests
- [ ] La propiedad `auto_move_to_next_stage` aparece en UI
- [ ] El orquestador bloquea cambios de stage cuando hay validaciones fallidas

### Fase 2 Completada Cuando:
- [ ] Se pueden configurar validaciones de campos nativos por stage
- [ ] Las validaciones nativas se ejecutan junto con JsonLogic
- [ ] Los candidatos que no cumplen requisitos son bloqueados/advertidos

### Fase 3 Completada Cuando:
- [ ] No se pueden crear más de X aplicaciones en Y días
- [ ] Se detectan y marcan candidatos con comportamiento de spam
- [ ] El dashboard muestra estadísticas de spam

### Fase 4 Completada Cuando:
- [ ] Los candidatos se mueven automáticamente cada hora (configurable)
- [ ] Los rechazos automáticos generan notificaciones
- [ ] Todo es configurable por company


