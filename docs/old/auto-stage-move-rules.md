# Reglas de Movimiento Automático de Candidatos entre Stages

**Fecha de actualización:** 2025-01-24  
**Estado:** 🟡 Parcialmente Implementado

---

## 📋 Objetivo

Implementar reglas que permitan mover automáticamente candidatos entre stages basándose en validaciones y requisitos. El sistema debe poder:

1. Validar requisitos antes de permitir el cambio de stage
2. Rechazar automáticamente candidatos que no cumplan criterios
3. Mover automáticamente a la siguiente etapa si se cumplen todos los requisitos

---

## 🟢 Funcionalidades Implementadas

### 1. Transición Automática de Fases ✅

**Estado:** Completamente implementado  
**Ubicación:** 
- `src/company_bc/company_candidate/application/commands/change_stage_command.py`
- `src/company_bc/candidate_application/application/commands/move_candidate_to_stage_command.py`

**Descripción:**
Cuando un candidato alcanza un stage terminal (SUCCESS o FAIL) que tiene configurado un `next_phase_id`, el sistema automáticamente:
- Obtiene el workflow por defecto de la siguiente fase
- Encuentra el stage INITIAL de ese workflow
- Mueve al candidato al stage inicial de la nueva fase

**Ejemplo de flujo:**
```
Candidato en "Final Interview" (SUCCESS) → 
  next_phase_id configurado → 
  Se mueve automáticamente a "Offer Review" (INITIAL de siguiente fase)
```

### 2. Creación Automática de Entrevistas ✅

**Estado:** Completamente implementado  
**Ubicación:** `src/company_bc/company_candidate/application/commands/change_stage_command.py`

**Descripción:**
Cuando un candidato se mueve a un nuevo stage, el sistema:
- Verifica si el stage tiene `interview_configurations` configuradas
- Para cada configuración con modo `AUTOMATIC`:
  - Obtiene el template de entrevista
  - Verifica que el stage tenga `default_role_ids` configurados
  - Crea automáticamente la entrevista en estado PENDING
  - Asigna los roles requeridos del stage

**Requisitos para que funcione:**
- El stage debe tener `interview_configurations` no vacías
- Cada configuración debe tener `mode: 'AUTOMATIC'`
- El stage debe tener `default_role_ids` definidos (obligatorio para entrevistas)
- El candidato debe tener al menos una aplicación activa (para obtener `job_position_id`)

### 3. Validación de Consistencia Stage-Phase ✅

**Estado:** Implementado  
**Ubicación:** `src/shared_bc/customization/workflow/domain/services/stage_phase_validation_service.py`

**Descripción:**
Valida que un stage pertenezca al workflow correcto dentro de la phase especificada.

**Lógica:**
```
stage_id → WorkflowStage.workflow_id → Workflow.phase_id == phase_id
```

### 4. Validación de Entrevistas Pendientes ✅

**Estado:** Implementado  
**Ubicación:** `src/shared_bc/customization/field_validation/application/services/interview_validation_service.py`

**Descripción:**
Antes de permitir cambiar de stage, valida que no haya entrevistas pendientes en el stage actual. Si hay entrevistas pendientes, rechaza el cambio.

### 5. Detección de Aplicaciones Duplicadas ✅

**Estado:** Implementado  
**Ubicación:** `src/company_bc/candidate_application/application/commands/create_candidate_application.py`

**Descripción:**
Al crear una aplicación, verifica si el candidato ya tiene una aplicación a la misma posición y previene duplicados.

---

## 🟡 Funcionalidades Parcialmente Implementadas

### 6. Sistema de ValidationRules ⚠️

**Estado:** Estructura implementada, evaluación pendiente  
**Ubicación:** 
- `src/shared_bc/customization/field_validation/domain/entities/validation_rule.py`
- `src/shared_bc/customization/workflow/domain/entities/workflow_stage.py`

**Qué está implementado:**
- ✅ Entidad `ValidationRule` con:
  - `rule_type`: Tipo de validación
  - `comparison_operator`: Operador de comparación
  - `severity`: WARNING o ERROR
  - `auto_reject`: Flag para rechazo automático
  - `rejection_reason`: Razón del rechazo
- ✅ Campos en `WorkflowStage`:
  - `validation_rules`: Reglas JsonLogic obligatorias
  - `recommended_rules`: Reglas JsonLogic recomendadas

**Qué falta:**
- ❌ Evaluador JsonLogic funcional (actualmente es un placeholder/TODO)
- ❌ Aplicación automática del `auto_reject` cuando falla una validación
- ❌ Servicio que ejecute las validaciones antes de cambiar de stage

**Ubicación del TODO:**
```python
# src/company_bc/job_position/application/commands/move_job_position_to_stage.py:206
# TODO: Implement proper JsonLogic validation using a JsonLogic library
```

---

## 🔴 Funcionalidades Pendientes

### 7. Propiedad `auto_move_to_next_stage` ❌

**Estado:** No implementado  
**Descripción requerida:**
Agregar una propiedad booleana a nivel de `WorkflowStage` que indique si automáticamente se debe mover al candidato al siguiente stage si cumple todos los requisitos.

**Cambios necesarios:**

1. **Modelo de Base de Datos:**
```sql
ALTER TABLE workflow_stages 
ADD COLUMN auto_move_to_next_stage BOOLEAN DEFAULT FALSE;
```

2. **Entidad de Dominio:**
```python
# src/shared_bc/customization/workflow/domain/entities/workflow_stage.py
@dataclass
class WorkflowStage:
    ...
    auto_move_to_next_stage: bool  # Nueva propiedad
```

3. **Lógica de Auto-movimiento:**
Crear un servicio/handler que:
- Se ejecute periódicamente (job scheduler/cron)
- O se ejecute cuando se actualiza el candidato
- Para cada candidato en un stage con `auto_move_to_next_stage=True`:
  - Ejecute todas las `validation_rules`
  - Si todas pasan → mover al siguiente stage
  - Si alguna falla con `auto_reject=True` → rechazar/mover a stage FAIL

### 8. Validaciones con Campos Nativos del Candidato ❌

**Estado:** No implementado  
**Campos a validar:**
- `work_modality`: Modalidad de trabajo (remoto, híbrido, presencial)
- `languages`: Idiomas del candidato
- `expected_annual_salary`: Salario esperado
- `current_annual_salary`: Salario actual
- `city`: Ciudad
- `country`: País

**Implementación requerida:**

1. **Crear ValidationRuleType para campos nativos:**
```python
class ValidationRuleType(str, Enum):
    CUSTOM_FIELD = "CUSTOM_FIELD"
    NATIVE_FIELD = "NATIVE_FIELD"  # Nueva
    POSITION_COMPARISON = "POSITION_COMPARISON"
```

2. **Servicio de Validación:**
```python
class NativeFieldValidationService:
    def validate_work_modality(candidate, required_modality) -> ValidationResult
    def validate_languages(candidate, required_languages) -> ValidationResult
    def validate_salary_range(candidate, min_salary, max_salary) -> ValidationResult
    def validate_location(candidate, allowed_countries, allowed_cities) -> ValidationResult
```

3. **Integración en ChangeStageCommand:**
Antes de cambiar de stage, ejecutar validaciones de campos nativos.

### 9. Validación de Aplicaciones Repetidas en Periodo ❌

**Estado:** No implementado  
**Descripción requerida:**
Validar y limitar el número de aplicaciones de un candidato:
- A la misma oferta en un periodo de tiempo (ej: no más de 1 vez cada 30 días)
- A cualquier oferta de la compañía en un periodo de tiempo (ej: no más de 5 veces al mes)

**Implementación requerida:**

1. **Repositorio con queries temporales:**
```python
class CandidateApplicationRepositoryInterface:
    def count_applications_to_position_in_period(
        candidate_id: CandidateId,
        position_id: JobPositionId,
        days: int
    ) -> int
    
    def count_applications_to_company_in_period(
        candidate_id: CandidateId,
        company_id: CompanyId,
        days: int
    ) -> int
```

2. **Servicio de Validación:**
```python
class ApplicationFrequencyValidationService:
    def validate_application_frequency(
        candidate_id: CandidateId,
        position_id: JobPositionId,
        company_id: CompanyId
    ) -> ValidationResult
```

3. **Configuración a nivel de Company:**
```python
class CompanySettings:
    max_applications_per_position_days: int = 30
    max_applications_per_company_days: int = 30
    max_applications_per_company_count: int = 5
```

### 10. Detector de Spam ❌

**Estado:** No implementado  
**Descripción requerida:**
Detectar patrones de spam en aplicaciones de candidatos.

**Indicadores de Spam:**
- Aplicaciones masivas en corto periodo de tiempo
- CV/información duplicada entre múltiples candidatos
- Texto repetitivo o generado automáticamente
- Emails desechables o temporales
- Patrones sospechosos en nombres/datos

**Implementación requerida:**

1. **Servicio de Detección:**
```python
class SpamDetectionService:
    def check_application_rate(candidate_id: CandidateId) -> SpamScore
    def check_duplicate_content(cv_text: str) -> SpamScore
    def check_email_domain(email: str) -> SpamScore
    def check_patterns(candidate_data: dict) -> SpamScore
    def calculate_spam_score(candidate: Candidate) -> float
```

2. **Regla de Rechazo Automático:**
Si `spam_score > threshold` (ej: 0.8):
- Marcar como spam
- Rechazar automáticamente
- Opcional: Bloquear email/candidato

3. **Dashboard de Spam:**
Panel para revisar candidatos marcados como spam y corregir falsos positivos.

---

## 📊 Resumen de Estado

| Funcionalidad | Estado | Prioridad |
|--------------|--------|-----------|
| Transición automática de fases | ✅ Implementado | - |
| Creación automática de entrevistas | ✅ Implementado | - |
| Validación Stage-Phase | ✅ Implementado | - |
| Validación entrevistas pendientes | ✅ Implementado | - |
| Detección aplicaciones duplicadas | ✅ Implementado | - |
| Sistema ValidationRules | ⚠️ Estructura existe | 🟡 Media |
| Evaluador JsonLogic | ❌ Pendiente | 🔴 Alta |
| Auto-movimiento con validaciones | ❌ Pendiente | 🔴 Alta |
| Propiedad `auto_move_to_next_stage` | ❌ Pendiente | 🟡 Media |
| Validaciones campos nativos | ❌ Pendiente | 🟡 Media |
| Validación aplicaciones repetidas | ❌ Pendiente | 🟢 Baja |
| Detector de spam | ❌ Pendiente | 🟢 Baja |

---

## 🏗️ Arquitectura Propuesta

### Flujo de Validación Automática

```
Candidato intenta cambiar a Stage X
         ↓
StageValidationOrchestrator
         ↓
    ┌────┴────┐
    ↓         ↓
JsonLogic   Native
Validator   Field
            Validator
    ↓         ↓
    └────┬────┘
         ↓
  ¿Todas las validaciones pasaron?
         ↓
    ┌────┴────┐
    ↓         ↓
   SÍ        NO
    ↓         ↓
Mover    ¿auto_reject?
stage         ↓
         ┌────┴────┐
         ↓         ↓
        SÍ        NO
         ↓         ↓
    Rechazar  Mostrar
    automát.  warning
```

### Flujo de Auto-movimiento

```
Candidato en Stage X con auto_move_to_next_stage=True
         ↓
    (Trigger: Evento/Cron)
         ↓
StageValidationOrchestrator.validate_all()
         ↓
    ¿Todas pasaron?
         ↓
    ┌────┴────┐
    ↓         ↓
   SÍ        NO
    ↓         ↓
ChangeStage  Mantener
Command      en stage
             actual
```

---

## 📝 Notas Adicionales

### Consideraciones sobre Timing
Como menciona el documento original:
> "En HR no se suelen utilizar reglas en real-time, cuando un candidato se apunta a una oferta, se espera un tiempo hasta que se le notifica el siguiente paso o si está descalificado"

**Opciones de Implementación:**
1. **Real-time:** Validar inmediatamente al aplicar (puede ser muy restrictivo)
2. **Batch/Cron:** Job que se ejecuta periódicamente (ej: cada hora o día)
3. **Manual + Sugerencias:** El sistema sugiere rechazos pero requiere confirmación humana

**Recomendación:** Implementar opción 3 inicialmente, con posibilidad de configurar auto-rechazo por company.

### Librerías Recomendadas

Para JsonLogic:
- **Python:** `json-logic-py` (https://github.com/nadirizr/json-logic-py)
- Permite evaluar reglas JsonLogic en Python de forma segura

Para Spam Detection:
- Análisis de texto repetitivo
- Rate limiting por IP/candidato
- Verificación de dominios de email desechables

---

## 🎯 Próximos Pasos Recomendados

1. **Fase 1 - Fundamentos (Crítico):**
   - [ ] Implementar evaluador JsonLogic funcional
   - [ ] Agregar propiedad `auto_move_to_next_stage` a WorkflowStage
   - [ ] Crear `StageValidationOrchestrator` que coordine todas las validaciones

2. **Fase 2 - Validaciones Nativas (Media):**
   - [ ] Implementar validaciones de campos nativos del candidato
   - [ ] Integrar validaciones en el flujo de change_stage

3. **Fase 3 - Anti-Spam (Baja):**
   - [ ] Implementar detector de spam
   - [ ] Implementar límites de aplicaciones repetidas
   - [ ] Dashboard de revisión de spam

4. **Fase 4 - Auto-movimiento (Opcional):**
   - [ ] Implementar job/cron para auto-movimiento
   - [ ] Configuración por company de reglas de auto-movimiento
   - [ ] Notificaciones cuando se mueve/rechaza automáticamente
