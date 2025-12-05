# Diseño: Sistema de Reglas Automáticas de Stage

**Fecha:** 2025-01-25  
**Estado:** 📐 Diseño

---

## 🎯 Objetivo

Diseñar un sistema de reglas que permita:
1. Bloquear transiciones a ciertos tipos de stage
2. Mostrar warnings al usuario sin bloquear
3. Mover automáticamente candidatos cuando se cumplen condiciones
4. Permitir override de reglas por parte del usuario (cuando esté habilitado)

---

## 📐 Modelo de Datos

### StageRule (Entidad Principal)

```python
@dataclass
class StageRule:
    id: StageRuleId
    stage_id: WorkflowStageId
    name: str                              # Nombre identificativo de la regla
    description: str                       # Descripción para el usuario
    
    # Configuración de la regla
    rule_type: StageRuleTypeEnum           # BLOCK, WARNING, AUTO_MOVE
    
    # Para BLOCK: qué bloquea (puede usar uno o ambos)
    blocked_stage_types: list[WorkflowStageTypeEnum]  # Tipos de stage que bloquea
    blocked_stage_ids: list[WorkflowStageId]          # Stages específicos que bloquea
    
    # Para AUTO_MOVE: a dónde mueve
    target_stage_id: Optional[WorkflowStageId]        # Stage destino
    
    # Evaluación
    evaluation_logic: EvaluationLogicEnum  # AND, OR
    validations: list[StageRuleValidation] # Lista de validaciones
    
    # Override
    allow_override: bool                   # Si el usuario puede saltarse la regla
    override_reason_required: bool         # Si requiere motivo al hacer override
    
    # Metadata
    is_active: bool
    priority: int                          # Orden de evaluación
    created_at: datetime
    updated_at: datetime
```

**Lógica de BLOCK:**
- Si `blocked_stage_types` no está vacío → bloquea transición a cualquier stage de esos tipos
- Si `blocked_stage_ids` no está vacío → bloquea transición a esos stages específicos
- Se pueden combinar ambos (OR entre ellos)

### StageRuleTypeEnum

```python
class StageRuleTypeEnum(str, Enum):
    BLOCK = "BLOCK"         # Impide transición a ciertos tipos de stage
    WARNING = "WARNING"     # Muestra advertencia pero no bloquea
    AUTO_MOVE = "AUTO_MOVE" # Mueve automáticamente al target_stage_id
```

**Nota:** La lógica AND/OR se define en `evaluation_logic` de la regla, aplicable a todos los tipos.

### EvaluationLogicEnum

```python
class EvaluationLogicEnum(str, Enum):
    AND = "AND"  # Todas las validaciones deben cumplirse
    OR = "OR"    # Al menos una validación debe cumplirse
```

### StageRuleValidation (Value Object)

```python
@dataclass(frozen=True)
class StageRuleValidation:
    id: str                                # UUID para identificar la validación
    name: str                              # Nombre descriptivo
    
    # Configuración de validación
    validation_type: ValidationTypeEnum    # Tipo de validación
    field_path: str                        # Ruta al campo (ej: "candidate.expected_salary")
    operator: ComparisonOperatorEnum       # Operador de comparación
    expected_value: Any                    # Valor esperado
    
    # Para colecciones (entrevistas, custom fields múltiples)
    aggregator: Optional[AggregatorEnum]   # ALL, ANY, AVG, MIN, MAX, etc.
    filter_field: Optional[str]            # Filtrar colección antes de agregar
    filter_value: Optional[Any]            # Valor del filtro
    
    # Mensaje
    failure_message: str                   # Mensaje cuando no cumple
```

**Ejemplos de `field_path` con agregadores:**

```python
# Sin agregador (campo simple)
field_path = "candidate.expected_annual_salary"

# Con agregador sobre colección
field_path = "interviews.score"
aggregator = AggregatorEnum.AVG  # Promedio de scores

# Con filtro + agregador
field_path = "interviews.score"
filter_field = "interview_type"
filter_value = "TECHNICAL"
aggregator = AggregatorEnum.MIN  # Score mínimo de entrevistas técnicas
```

### ValidationTypeEnum

```python
class ValidationTypeEnum(str, Enum):
    # Campos del candidato
    CANDIDATE_FIELD = "CANDIDATE_FIELD"
    
    # Campos de la aplicación
    APPLICATION_FIELD = "APPLICATION_FIELD"
    
    # Custom fields
    CUSTOM_FIELD = "CUSTOM_FIELD"
    
    # Comparación con la posición
    POSITION_COMPARISON = "POSITION_COMPARISON"
    
    # Estado de entrevistas
    INTERVIEW_STATUS = "INTERVIEW_STATUS"
    
    # Evaluaciones/scorecards
    EVALUATION_SCORE = "EVALUATION_SCORE"
```

### ComparisonOperatorEnum

```python
class ComparisonOperatorEnum(str, Enum):
    # Igualdad
    EQUALS = "EQUALS"
    NOT_EQUALS = "NOT_EQUALS"
    
    # Comparaciones numéricas
    GREATER_THAN = "GREATER_THAN"
    GREATER_THAN_OR_EQUALS = "GREATER_THAN_OR_EQUALS"
    LESS_THAN = "LESS_THAN"
    LESS_THAN_OR_EQUALS = "LESS_THAN_OR_EQUALS"
    
    # Contenido (para strings y listas)
    CONTAINS = "CONTAINS"              # "abc" contains "b" / [1,2,3] contains 2
    NOT_CONTAINS = "NOT_CONTAINS"
    CONTAINS_ALL = "CONTAINS_ALL"      # [a,b,c] contains all of [a,b]
    CONTAINS_ANY = "CONTAINS_ANY"      # [a,b,c] contains any of [x,b]
    
    # Pertenencia a lista
    IN_LIST = "IN_LIST"                # value in [a,b,c]
    NOT_IN_LIST = "NOT_IN_LIST"
    
    # Vacío/Existencia
    IS_EMPTY = "IS_EMPTY"
    IS_NOT_EMPTY = "IS_NOT_EMPTY"
    
    # Regex
    MATCHES_REGEX = "MATCHES_REGEX"
    
    # Temporales (para campos datetime)
    DAYS_AGO_LESS_THAN = "DAYS_AGO_LESS_THAN"        # Hace menos de X días
    DAYS_AGO_GREATER_THAN = "DAYS_AGO_GREATER_THAN"  # Hace más de X días
    HOURS_AGO_LESS_THAN = "HOURS_AGO_LESS_THAN"      # Hace menos de X horas
    HOURS_AGO_GREATER_THAN = "HOURS_AGO_GREATER_THAN"# Hace más de X horas
    BEFORE_DATE = "BEFORE_DATE"                      # Antes de fecha específica
    AFTER_DATE = "AFTER_DATE"                        # Después de fecha específica
    BETWEEN_DATES = "BETWEEN_DATES"                  # Entre dos fechas
```

**Ejemplos de uso temporal:**
```python
# Aplicó hace menos de 30 días
field_path = "application.applied_at"
operator = ComparisonOperatorEnum.DAYS_AGO_LESS_THAN
expected_value = 30

# Lleva más de 7 días en el stage actual
field_path = "stage_history.current_stage_entered_at"
operator = ComparisonOperatorEnum.DAYS_AGO_GREATER_THAN
expected_value = 7

# Última actividad hace más de 48 horas
field_path = "candidate.last_activity_at"
operator = ComparisonOperatorEnum.HOURS_AGO_GREATER_THAN
expected_value = 48
```

### AggregatorEnum (para colecciones como entrevistas)

```python
class AggregatorEnum(str, Enum):
    ALL = "ALL"       # Todas deben cumplir
    ANY = "ANY"       # Al menos una debe cumplir
    NONE = "NONE"     # Ninguna debe cumplir
    COUNT = "COUNT"   # Contar cuántas cumplen
    AVG = "AVG"       # Promedio de valores numéricos
    MIN = "MIN"       # Valor mínimo
    MAX = "MAX"       # Valor máximo
    SUM = "SUM"       # Suma de valores
```

---

## 📋 Campos Nativos Validables

### Candidate

| Campo | Tipo | Ejemplo de validación |
|-------|------|----------------------|
| `first_name` | string | IS_NOT_EMPTY |
| `last_name` | string | IS_NOT_EMPTY |
| `email` | string | MATCHES_REGEX |
| `phone` | string | IS_NOT_EMPTY |
| `city` | string | EQUALS, IN_LIST |
| `country` | string | EQUALS, IN_LIST |
| `work_modality` | enum | EQUALS, IN_LIST |
| `languages` | list[string] | CONTAINS, IN_LIST |
| `expected_annual_salary` | number | comparaciones numéricas |
| `current_annual_salary` | number | comparaciones numéricas |
| `years_experience` | number | comparaciones numéricas |
| `resume_url` | string | IS_NOT_EMPTY |
| `linkedin_url` | string | IS_NOT_EMPTY |
| `portfolio_url` | string | IS_NOT_EMPTY |
| `created_at` | datetime | DAYS_AGO_*, AFTER_DATE |
| `updated_at` | datetime | DAYS_AGO_*, HOURS_AGO_* |
| `last_activity_at` | datetime | HOURS_AGO_*, DAYS_AGO_* |

### CandidateApplication

| Campo | Tipo | Ejemplo de validación |
|-------|------|----------------------|
| `source` | enum | EQUALS, IN_LIST |
| `status` | enum | EQUALS, NOT_EQUALS |
| `applied_at` | datetime | DAYS_AGO_*, AFTER_DATE |
| `cover_letter` | string | IS_NOT_EMPTY |
| `referral_source` | string | EQUALS |
| `created_at` | datetime | DAYS_AGO_* |
| `updated_at` | datetime | DAYS_AGO_*, HOURS_AGO_* |

### StageHistory (tiempos en stages)

| Campo | Tipo | Ejemplo de validación |
|-------|------|----------------------|
| `current_stage_entered_at` | datetime | DAYS_AGO_*, HOURS_AGO_* |
| `days_in_current_stage` | number | Calculado dinámicamente |
| `total_days_in_process` | number | Desde primera aplicación |
| `previous_stage_exited_at` | datetime | DAYS_AGO_* |

### JobPosition (para comparaciones)

| Campo | Tipo | Uso |
|-------|------|-----|
| `min_salary` | number | Comparar con candidate.expected_salary |
| `max_salary` | number | Comparar con candidate.expected_salary |
| `required_languages` | list[string] | Comparar con candidate.languages |
| `work_modality` | enum | Comparar con candidate.work_modality |
| `city` | string | Comparar con candidate.city |
| `country` | string | Comparar con candidate.country |
| `min_experience_years` | number | Comparar con candidate.years_experience |

### Interviews (colección - requiere agregador)

| Campo | Tipo | Agregadores útiles |
|-------|------|-------------------|
| `status` | enum | ALL, ANY, NONE, COUNT |
| `score` | number | ALL, ANY, AVG, MIN, MAX |
| `recommendation` | enum | ALL, ANY, COUNT |
| `completed_at` | datetime | ALL, ANY |
| `interview_type` | enum | Para filtrar antes de agregar |

### Custom Fields

Accesibles por su `field_key` configurado en cada company.

---

## 🔄 Flujos de Evaluación

### Triggers de Evaluación

Las reglas se evalúan en los siguientes momentos:

| Trigger | Descripción | Reglas Evaluadas |
|---------|-------------|------------------|
| `STAGE_CHANGE` | Al intentar cambiar de stage | BLOCK, WARNING |
| `CANDIDATE_UPDATE` | Al editar candidato/application | AUTO_MOVE |
| `INTERVIEW_COMPLETE` | Al completar una entrevista | AUTO_MOVE |
| `CRON_JOB` | Job periódico (configurable) | AUTO_MOVE |

### Flujo: Cambio de Stage Manual

```
Usuario intenta mover candidato de Stage A → Stage B
                    ↓
        Obtener reglas BLOCK del Stage A
                    ↓
        Para cada regla BLOCK:
                    ↓
    ¿Stage B está bloqueado?
    (B.type IN blocked_stage_types OR B.id IN blocked_stage_ids)
                    ↓
              ┌─────┴─────┐
              ↓           ↓
             SI          NO
              ↓           ↓
    Evaluar validaciones  Siguiente regla
              ↓
        ┌─────┴─────┐
        ↓           ↓
    Validaciones  Validaciones
    PASAN         FALLAN
        ↓           ↓
    Siguiente   ¿allow_override?
    regla            ↓
                  ┌──┴──┐
                  ↓     ↓
                 NO    SI
                  ↓     ↓
               ERROR   Pedir confirmación
                            ↓
                       ¿Confirma?
                            ↓
                         ┌──┴──┐
                         ↓     ↓
                        NO    SI
                         ↓     ↓
                      CANCELAR PERMITIR
                               (registrar override)

Si no hay bloqueos → Evaluar reglas WARNING → Mostrar warnings si hay
```

### Flujo: Auto-movimiento

```
Trigger: Candidato editado / Entrevista completada / Cron
                    ↓
    Obtener candidatos en stages con reglas AUTO_MOVE
                    ↓
    Para cada candidato:
                    ↓
    Obtener reglas AUTO_MOVE del stage actual (ordenadas por prioridad)
                    ↓
    Para cada regla AUTO_MOVE:
                    ↓
         ┌─────────┴─────────┐
         ↓                   ↓
  evaluation_logic=AND  evaluation_logic=OR
         ↓                   ↓
    ¿TODAS las          ¿ALGUNA
    validaciones        validación
    cumplen?            cumple?
         ↓                   ↓
       ┌─┴─┐               ┌─┴─┐
       ↓   ↓               ↓   ↓
      NO   SI             NO   SI
       ↓   ↓               ↓   ↓
    Siguiente  Mover a  Siguiente  Mover a
    regla      target   regla      target
```

---

## 📋 Casos de Uso

### Caso 1: Bloqueo por Tipo de Stage

**Escenario:** En la fase de Sourcing, si el candidato no cumple requisitos mínimos, no puede pasar a ningún stage de tipo SUCCESS.

```yaml
StageRule:
  name: "Requisitos Mínimos Sourcing"
  rule_type: BLOCK
  blocked_stage_types: [SUCCESS]     # Bloquea TODOS los stages tipo SUCCESS
  blocked_stage_ids: []              # No bloquea stages específicos
  evaluation_logic: AND
  allow_override: false
  validations:
    - name: "Salario dentro del rango"
      validation_type: POSITION_COMPARISON
      field_path: "candidate.expected_annual_salary"
      operator: LESS_THAN_OR_EQUALS
      expected_value: "position.max_salary"
    - name: "Idioma requerido"
      validation_type: CANDIDATE_FIELD
      field_path: "candidate.languages"
      operator: CONTAINS
      expected_value: "English"
```

### Caso 1b: Bloqueo por Stage Específico

**Escenario:** No puede pasar al stage "Entrevista con CEO" sin haber aprobado la entrevista técnica.

```yaml
StageRule:
  name: "Requiere Técnica Aprobada para CEO"
  rule_type: BLOCK
  blocked_stage_types: []                           # No bloquea por tipo
  blocked_stage_ids: ["uuid-entrevista-ceo"]        # Solo bloquea este stage específico
  evaluation_logic: AND
  allow_override: true                              # Pero se puede hacer override
  override_reason_required: true
  validations:
    - name: "Entrevista técnica completada"
      validation_type: INTERVIEW_STATUS
      field_path: "interviews.technical"
      operator: EQUALS
      expected_value: "COMPLETED"
    - name: "Score técnico mínimo"
      validation_type: EVALUATION_SCORE
      field_path: "interviews.technical.score"
      operator: GREATER_THAN_OR_EQUALS
      expected_value: 6
```

### Caso 1c: Bloqueo Combinado (Tipo + Específico)

**Escenario:** Sin experiencia mínima, no puede pasar a SUCCESS ni a ningún stage de entrevistas senior.

```yaml
StageRule:
  name: "Experiencia Mínima Requerida"
  rule_type: BLOCK
  blocked_stage_types: [SUCCESS]                    # Bloquea SUCCESS
  blocked_stage_ids: [                              # Y también estos específicos
    "uuid-entrevista-senior",
    "uuid-entrevista-lead"
  ]
  evaluation_logic: AND
  allow_override: true
  validations:
    - name: "Años de experiencia"
      validation_type: CANDIDATE_FIELD
      field_path: "candidate.years_experience"
      operator: GREATER_THAN_OR_EQUALS
      expected_value: 3
```

### Caso 2: Warning de Salario

**Escenario:** Mostrar warning si el salario deseado está por encima del presupuesto, pero permitir continuar.

```yaml
StageRule:
  name: "Salario Recomendado"
  rule_type: WARNING
  evaluation_logic: AND
  allow_override: true
  override_reason_required: true
  validations:
    - name: "Salario dentro del presupuesto"
      validation_type: POSITION_COMPARISON
      field_path: "candidate.expected_annual_salary"
      operator: LESS_THAN_OR_EQUALS
      expected_value: "position.max_salary"
      failure_message: "El salario esperado ({value}) excede el presupuesto máximo ({expected})"
```

### Caso 3: Auto-descarte en Sourcing (AND - todas deben fallar)

**Escenario:** Al añadir un candidato, si NO cumple los requisitos mínimos, mover automáticamente a Descartado.

```yaml
StageRule:
  name: "Auto-descarte por incumplimiento"
  rule_type: AUTO_MOVE
  target_stage_id: "stage_descartado_uuid"
  evaluation_logic: AND              # Mueve si TODAS las validaciones pasan
  allow_override: false              # (en este caso, si fallan = no tiene CV ni email)
  validations:
    - name: "NO tiene CV"            # Validación inversa
      validation_type: CANDIDATE_FIELD
      field_path: "candidate.resume_url"
      operator: IS_EMPTY             # Si está vacío, pasa la validación → descarte
    - name: "Email inválido"
      validation_type: CANDIDATE_FIELD
      field_path: "candidate.email"
      operator: IS_EMPTY
```

**Nota:** Para auto-descarte, las validaciones se escriben en "negativo" (lo que NO queremos).

### Caso 4: Auto-avance por Entrevistas Completadas (AND)

**Escenario:** Cuando TODAS las entrevistas del stage están completadas con score >= 7, mover al siguiente stage.

```yaml
StageRule:
  name: "Avance por entrevistas completadas"
  rule_type: AUTO_MOVE
  target_stage_id: "siguiente_stage_uuid"
  evaluation_logic: AND              # TODAS deben cumplirse
  allow_override: true
  validations:
    - name: "Todas las entrevistas completadas"
      validation_type: INTERVIEW_STATUS
      field_path: "interviews.all"
      operator: EQUALS
      expected_value: "COMPLETED"
    - name: "Score mínimo en entrevistas"
      validation_type: EVALUATION_SCORE
      field_path: "interviews.average_score"
      operator: GREATER_THAN_OR_EQUALS
      expected_value: 7
```

### Caso 5: Auto-avance por CUALQUIER Entrevista Aprobada (OR)

**Escenario:** Si ALGUNA entrevista técnica tiene score >= 8, avanzar automáticamente.

```yaml
StageRule:
  name: "Avance por entrevista técnica destacada"
  rule_type: AUTO_MOVE
  target_stage_id: "siguiente_stage_uuid"
  evaluation_logic: OR               # Basta con que UNA cumpla
  allow_override: true
  validations:
    - name: "Alguna técnica con score alto"
      validation_type: INTERVIEW_STATUS
      field_path: "interviews.score"
      filter_field: "interview_type"
      filter_value: "TECHNICAL"
      aggregator: ANY                # ALGUNA entrevista técnica
      operator: GREATER_THAN_OR_EQUALS
      expected_value: 8
```

---

## 🎯 Casos de Uso: Validaciones con Entrevistas

### Caso 6: Bloquear SUCCESS si ALGUNA entrevista tiene score bajo

**Escenario:** No puede pasar a SUCCESS si alguna entrevista tiene score < 5.

```yaml
StageRule:
  name: "Sin entrevistas con score bajo"
  rule_type: BLOCK
  blocked_stage_types: [SUCCESS]
  evaluation_logic: AND
  allow_override: true
  override_reason_required: true
  validations:
    - name: "Ninguna entrevista con score bajo"
      validation_type: INTERVIEW_STATUS
      field_path: "interviews.score"
      aggregator: NONE               # NINGUNA debe cumplir esto
      operator: LESS_THAN
      expected_value: 5
      failure_message: "Hay entrevistas con score inferior a 5"
```

**Nota:** Usamos `aggregator: NONE` con `LESS_THAN 5` = "ninguna entrevista debe tener score < 5"

### Caso 7: Requiere promedio mínimo en entrevistas técnicas

**Escenario:** Para pasar a la fase de Offer, el promedio de entrevistas técnicas debe ser >= 7.

```yaml
StageRule:
  name: "Promedio técnico mínimo para Offer"
  rule_type: BLOCK
  blocked_stage_types: [SUCCESS]
  blocked_stage_ids: ["uuid-offer-stage"]
  evaluation_logic: AND
  allow_override: true
  validations:
    - name: "Promedio técnico >= 7"
      validation_type: INTERVIEW_STATUS
      field_path: "interviews.score"
      filter_field: "interview_type"
      filter_value: "TECHNICAL"
      aggregator: AVG                # PROMEDIO de técnicas
      operator: GREATER_THAN_OR_EQUALS
      expected_value: 7
      failure_message: "Promedio de entrevistas técnicas: {value}, mínimo requerido: 7"
```

### Caso 8: Todas las entrevistas deben estar completadas

**Escenario:** No puede avanzar si hay entrevistas pendientes.

```yaml
StageRule:
  name: "Todas las entrevistas completadas"
  rule_type: BLOCK
  blocked_stage_types: [SUCCESS, IN_PROGRESS]
  evaluation_logic: AND
  allow_override: false              # No se puede saltar
  validations:
    - name: "Entrevistas completadas"
      validation_type: INTERVIEW_STATUS
      field_path: "interviews.status"
      aggregator: ALL                # TODAS deben cumplir
      operator: EQUALS
      expected_value: "COMPLETED"
      failure_message: "Hay entrevistas pendientes de completar"
```

### Caso 9: Al menos 2 entrevistadores recomiendan

**Escenario:** Para pasar a Offer, al menos 2 entrevistadores deben recomendar "STRONG_YES" o "YES".

```yaml
StageRule:
  name: "Mínimo 2 recomendaciones positivas"
  rule_type: BLOCK
  blocked_stage_types: [SUCCESS]
  evaluation_logic: AND
  allow_override: true
  validations:
    - name: "Cuenta de recomendaciones positivas"
      validation_type: INTERVIEW_STATUS
      field_path: "interviews.recommendation"
      aggregator: COUNT              # CONTAR cuántas cumplen
      operator: IN_LIST
      expected_value: ["STRONG_YES", "YES"]
      # El resultado del COUNT se compara después:
      count_operator: GREATER_THAN_OR_EQUALS
      count_value: 2
      failure_message: "Solo {value} entrevistadores recomiendan al candidato, se requieren al menos 2"
```

### Caso 10: Score mínimo más bajo no puede ser < 4

**Escenario:** Incluso si el promedio es bueno, si alguna entrevista tiene score muy bajo (< 4), bloquear.

```yaml
StageRule:
  name: "Score mínimo aceptable"
  rule_type: BLOCK
  blocked_stage_types: [SUCCESS]
  evaluation_logic: AND
  allow_override: true
  validations:
    - name: "Score mínimo >= 4"
      validation_type: INTERVIEW_STATUS
      field_path: "interviews.score"
      aggregator: MIN                # El MÍNIMO de todos los scores
      operator: GREATER_THAN_OR_EQUALS
      expected_value: 4
      failure_message: "Hay una entrevista con score {value}, mínimo aceptable: 4"
```

### Caso 11: Comparación con requisitos de la posición

**Escenario:** El salario esperado del candidato no puede exceder el máximo de la posición.

```yaml
StageRule:
  name: "Salario dentro del presupuesto"
  rule_type: BLOCK
  blocked_stage_types: [SUCCESS]
  evaluation_logic: AND
  allow_override: true
  override_reason_required: true
  validations:
    - name: "Salario <= máximo de posición"
      validation_type: POSITION_COMPARISON
      field_path: "candidate.expected_annual_salary"
      operator: LESS_THAN_OR_EQUALS
      expected_value: "position.max_salary"  # Referencia a campo de posición
      failure_message: "Salario esperado ({value}) excede el máximo ({expected})"
```

### Caso 12: Idiomas requeridos por la posición

**Escenario:** El candidato debe tener todos los idiomas requeridos por la posición.

```yaml
StageRule:
  name: "Idiomas requeridos"
  rule_type: BLOCK
  blocked_stage_types: [SUCCESS, IN_PROGRESS]
  evaluation_logic: AND
  allow_override: true
  validations:
    - name: "Tiene idiomas requeridos"
      validation_type: POSITION_COMPARISON
      field_path: "candidate.languages"
      operator: CONTAINS_ALL         # Contiene TODOS los del expected
      expected_value: "position.required_languages"
      failure_message: "Faltan idiomas requeridos: {missing}"
```

---

## ⏰ Casos de Uso: Validaciones Temporales

### Caso 13: Aplicación reciente (menos de 30 días)

**Escenario:** Solo procesar candidatos que aplicaron hace menos de 30 días.

```yaml
StageRule:
  name: "Aplicación vigente"
  rule_type: BLOCK
  blocked_stage_types: [SUCCESS, IN_PROGRESS]
  evaluation_logic: AND
  allow_override: true
  validations:
    - name: "Aplicó hace menos de 30 días"
      validation_type: APPLICATION_FIELD
      field_path: "application.applied_at"
      operator: DAYS_AGO_LESS_THAN
      expected_value: 30
      failure_message: "La aplicación tiene más de 30 días (aplicó el {value})"
```

### Caso 14: Auto-descarte por inactividad

**Escenario:** Si el candidato lleva más de 14 días en el stage actual sin actividad, mover a "En espera".

```yaml
StageRule:
  name: "Auto-mover por inactividad"
  rule_type: AUTO_MOVE
  target_stage_id: "uuid-stage-en-espera"
  evaluation_logic: AND
  allow_override: false
  validations:
    - name: "Más de 14 días en stage actual"
      validation_type: CANDIDATE_FIELD
      field_path: "stage_history.current_stage_entered_at"
      operator: DAYS_AGO_GREATER_THAN
      expected_value: 14
      failure_message: "Candidato inactivo por más de 14 días"
```

### Caso 15: Urgencia - entrevista pendiente más de 48h

**Escenario:** Warning si una entrevista lleva más de 48 horas sin completarse.

```yaml
StageRule:
  name: "Entrevista pendiente demasiado tiempo"
  rule_type: WARNING
  evaluation_logic: OR               # Cualquier entrevista que cumpla
  allow_override: true
  validations:
    - name: "Entrevista pendiente > 48h"
      validation_type: INTERVIEW_STATUS
      field_path: "interviews.created_at"
      filter_field: "status"
      filter_value: "PENDING"
      aggregator: ANY
      operator: HOURS_AGO_GREATER_THAN
      expected_value: 48
      failure_message: "Hay entrevistas pendientes hace más de 48 horas"
```

### Caso 16: Límite de tiempo total en proceso

**Escenario:** Bloquear si el candidato lleva más de 60 días en el proceso total.

```yaml
StageRule:
  name: "Límite tiempo en proceso"
  rule_type: BLOCK
  blocked_stage_types: [SUCCESS]
  evaluation_logic: AND
  allow_override: true
  override_reason_required: true
  validations:
    - name: "Menos de 60 días en proceso"
      validation_type: APPLICATION_FIELD
      field_path: "application.created_at"
      operator: DAYS_AGO_LESS_THAN
      expected_value: 60
      failure_message: "Candidato lleva {value} días en proceso (máximo: 60)"
```

### Caso 17: Candidato nuevo - no contactar antes de 24h

**Escenario:** Warning si se intenta mover a un candidato que aplicó hace menos de 24 horas (dar tiempo a que complete el perfil).

```yaml
StageRule:
  name: "Esperar 24h antes de procesar"
  rule_type: WARNING
  evaluation_logic: AND
  allow_override: true
  validations:
    - name: "Aplicó hace más de 24h"
      validation_type: APPLICATION_FIELD
      field_path: "application.applied_at"
      operator: HOURS_AGO_GREATER_THAN
      expected_value: 24
      failure_message: "El candidato aplicó hace menos de 24 horas, puede estar completando su perfil"
```

### Caso 18: Cron - Recordatorio de candidatos estancados

**Escenario:** (Para cron) Identificar candidatos que llevan más de 7 días sin movimiento.

```yaml
StageRule:
  name: "Alerta candidatos estancados"
  rule_type: WARNING                 # Solo genera alerta, no mueve
  evaluation_logic: AND
  validations:
    - name: "Más de 7 días sin cambio de stage"
      validation_type: CANDIDATE_FIELD
      field_path: "stage_history.current_stage_entered_at"
      operator: DAYS_AGO_GREATER_THAN
      expected_value: 7
    - name: "Sin actividad reciente"
      validation_type: CANDIDATE_FIELD
      field_path: "candidate.last_activity_at"
      operator: DAYS_AGO_GREATER_THAN
      expected_value: 5
```

### Caso 19: Ventana de contratación

**Escenario:** La posición tiene fecha límite. Bloquear si ya pasó.

```yaml
StageRule:
  name: "Dentro de ventana de contratación"
  rule_type: BLOCK
  blocked_stage_types: [SUCCESS]
  evaluation_logic: AND
  allow_override: true
  override_reason_required: true
  validations:
    - name: "Posición aún abierta"
      validation_type: POSITION_COMPARISON
      field_path: "NOW"              # Fecha actual
      operator: BEFORE_DATE
      expected_value: "position.deadline_date"
      failure_message: "La fecha límite de la posición ya pasó ({expected})"
```

### Caso 20: Última entrevista completada recientemente

**Escenario:** Para avanzar a Offer, la última entrevista debe haberse completado en los últimos 7 días (información fresca).

```yaml
StageRule:
  name: "Entrevistas recientes para Offer"
  rule_type: BLOCK
  blocked_stage_ids: ["uuid-offer-stage"]
  evaluation_logic: AND
  allow_override: true
  validations:
    - name: "Última entrevista < 7 días"
      validation_type: INTERVIEW_STATUS
      field_path: "interviews.completed_at"
      aggregator: MAX                # La más reciente
      operator: DAYS_AGO_LESS_THAN
      expected_value: 7
      failure_message: "La última entrevista fue hace más de 7 días, considere re-entrevistar"
```

---

## 📦 Plantillas de Reglas Predefinidas

Las plantillas son reglas pre-configuradas que las companies pueden activar con un click. Cada company puede personalizar los valores después de activarlas.

### RuleTemplate (Entidad)

```python
@dataclass
class RuleTemplate:
    id: RuleTemplateId
    code: str                          # Identificador único (ej: "TPL_SALARY_CHECK")
    name: str                          # Nombre visible
    description: str                   # Descripción para el admin
    category: RuleTemplateCategoryEnum # Categoría para organizar
    
    # Configuración base de la regla
    rule_type: StageRuleTypeEnum
    blocked_stage_types: list[WorkflowStageTypeEnum]
    evaluation_logic: EvaluationLogicEnum
    allow_override: bool
    override_reason_required: bool
    
    # Validaciones con placeholders
    validation_templates: list[ValidationTemplate]
    
    # Valores por defecto editables
    default_values: dict[str, Any]     # Valores que la company puede cambiar
    
    # Metadata
    is_system: bool                    # True = no se puede eliminar
    recommended_stage_types: list[WorkflowStageTypeEnum]  # Dónde se recomienda usar
    recommended_phases: list[str]      # Fases sugeridas (SOURCING, SCREENING, etc.)


@dataclass
class ValidationTemplate:
    """Validación con placeholders para valores configurables."""
    name: str
    validation_type: ValidationTypeEnum
    field_path: str
    operator: ComparisonOperatorEnum
    
    # Placeholder para valor configurable
    value_key: str                     # Ej: "max_salary", "min_experience"
    default_value: Any                 # Valor por defecto
    
    aggregator: Optional[AggregatorEnum]
    filter_field: Optional[str]
    filter_value_key: Optional[str]    # Placeholder para filtro configurable
    
    failure_message_template: str      # Con placeholders: "Salario {value} excede {max_salary}"
```

### RuleTemplateCategoryEnum

```python
class RuleTemplateCategoryEnum(str, Enum):
    QUALIFICATION = "QUALIFICATION"       # Requisitos mínimos
    COMPENSATION = "COMPENSATION"         # Salario y beneficios
    INTERVIEW = "INTERVIEW"               # Relacionadas con entrevistas
    TIMELINE = "TIMELINE"                 # Tiempos y plazos
    COMPLIANCE = "COMPLIANCE"             # Cumplimiento y documentación
    QUALITY = "QUALITY"                   # Calidad del candidato
    AUTOMATION = "AUTOMATION"             # Auto-movimientos
```

---

### Plantillas: Categoría QUALIFICATION

#### TPL_REQUIRED_CV
```yaml
code: "TPL_REQUIRED_CV"
name: "CV Obligatorio"
description: "Bloquea avance si el candidato no tiene CV cargado"
category: QUALIFICATION
rule_type: BLOCK
blocked_stage_types: [SUCCESS, IN_PROGRESS]
evaluation_logic: AND
allow_override: true
recommended_phases: [SOURCING, SCREENING]

validation_templates:
  - name: "Tiene CV"
    field_path: "candidate.resume_url"
    operator: IS_NOT_EMPTY
    failure_message_template: "El candidato no tiene CV cargado"

default_values: {}  # Sin valores configurables
```

#### TPL_MIN_EXPERIENCE
```yaml
code: "TPL_MIN_EXPERIENCE"
name: "Experiencia Mínima"
description: "Requiere años mínimos de experiencia"
category: QUALIFICATION
rule_type: BLOCK
blocked_stage_types: [SUCCESS]
evaluation_logic: AND
allow_override: true
recommended_phases: [SOURCING, SCREENING]

validation_templates:
  - name: "Años de experiencia"
    field_path: "candidate.years_experience"
    operator: GREATER_THAN_OR_EQUALS
    value_key: "min_years"
    default_value: 2
    failure_message_template: "Experiencia: {value} años, mínimo requerido: {min_years}"

default_values:
  min_years: 2
```

#### TPL_REQUIRED_LANGUAGES
```yaml
code: "TPL_REQUIRED_LANGUAGES"
name: "Idiomas Requeridos"
description: "Verifica que el candidato tenga los idiomas de la posición"
category: QUALIFICATION
rule_type: BLOCK
blocked_stage_types: [SUCCESS, IN_PROGRESS]
evaluation_logic: AND
allow_override: true
recommended_phases: [SOURCING]

validation_templates:
  - name: "Idiomas de la posición"
    validation_type: POSITION_COMPARISON
    field_path: "candidate.languages"
    operator: CONTAINS_ALL
    value_key: "position.required_languages"
    failure_message_template: "Faltan idiomas requeridos"

default_values: {}
```

#### TPL_LOCATION_MATCH
```yaml
code: "TPL_LOCATION_MATCH"
name: "Ubicación Compatible"
description: "Verifica país/ciudad del candidato vs posición"
category: QUALIFICATION
rule_type: WARNING
evaluation_logic: OR
allow_override: true
recommended_phases: [SOURCING]

validation_templates:
  - name: "País coincide"
    validation_type: POSITION_COMPARISON
    field_path: "candidate.country"
    operator: EQUALS
    value_key: "position.country"
    failure_message_template: "País del candidato ({value}) diferente al de la posición"
  - name: "Modalidad remota permite"
    field_path: "position.work_modality"
    operator: EQUALS
    value_key: "remote_modality"
    default_value: "REMOTE"

default_values:
  remote_modality: "REMOTE"
```

---

### Plantillas: Categoría COMPENSATION

#### TPL_SALARY_IN_BUDGET
```yaml
code: "TPL_SALARY_IN_BUDGET"
name: "Salario Dentro del Presupuesto"
description: "Verifica que el salario esperado no exceda el máximo"
category: COMPENSATION
rule_type: BLOCK
blocked_stage_types: [SUCCESS]
evaluation_logic: AND
allow_override: true
override_reason_required: true
recommended_phases: [SOURCING, SCREENING, OFFER]

validation_templates:
  - name: "Salario <= máximo"
    validation_type: POSITION_COMPARISON
    field_path: "candidate.expected_annual_salary"
    operator: LESS_THAN_OR_EQUALS
    value_key: "position.max_salary"
    failure_message_template: "Salario esperado ({value}) excede presupuesto ({position.max_salary})"

default_values: {}
```

#### TPL_SALARY_WARNING
```yaml
code: "TPL_SALARY_WARNING"
name: "Alerta Salario Alto"
description: "Warning si el salario está cerca del máximo (>80%)"
category: COMPENSATION
rule_type: WARNING
evaluation_logic: AND
allow_override: true
recommended_phases: [SCREENING]

validation_templates:
  - name: "Salario < 80% del máximo"
    validation_type: POSITION_COMPARISON
    field_path: "candidate.expected_annual_salary"
    operator: LESS_THAN
    value_key: "salary_threshold_percent"
    default_value: 0.8  # Se calcula: position.max_salary * 0.8
    failure_message_template: "Salario esperado está por encima del 80% del presupuesto"

default_values:
  salary_threshold_percent: 0.8
```

---

### Plantillas: Categoría INTERVIEW

#### TPL_ALL_INTERVIEWS_COMPLETED
```yaml
code: "TPL_ALL_INTERVIEWS_COMPLETED"
name: "Todas las Entrevistas Completadas"
description: "Bloquea avance si hay entrevistas pendientes"
category: INTERVIEW
rule_type: BLOCK
blocked_stage_types: [SUCCESS, IN_PROGRESS]
evaluation_logic: AND
allow_override: false
recommended_phases: [INTERVIEW, EVALUATION]

validation_templates:
  - name: "Sin entrevistas pendientes"
    field_path: "interviews.status"
    aggregator: ALL
    operator: EQUALS
    value_key: "completed_status"
    default_value: "COMPLETED"
    failure_message_template: "Hay entrevistas pendientes de completar"

default_values:
  completed_status: "COMPLETED"
```

#### TPL_MIN_INTERVIEW_SCORE
```yaml
code: "TPL_MIN_INTERVIEW_SCORE"
name: "Score Mínimo en Entrevistas"
description: "Requiere score promedio mínimo en entrevistas"
category: INTERVIEW
rule_type: BLOCK
blocked_stage_types: [SUCCESS]
evaluation_logic: AND
allow_override: true
recommended_phases: [EVALUATION, OFFER]

validation_templates:
  - name: "Promedio >= mínimo"
    field_path: "interviews.score"
    aggregator: AVG
    operator: GREATER_THAN_OR_EQUALS
    value_key: "min_avg_score"
    default_value: 7
    failure_message_template: "Promedio de entrevistas: {value}, mínimo: {min_avg_score}"

default_values:
  min_avg_score: 7
```

#### TPL_NO_LOW_SCORES
```yaml
code: "TPL_NO_LOW_SCORES"
name: "Sin Scores Bajos"
description: "Bloquea si alguna entrevista tiene score muy bajo"
category: INTERVIEW
rule_type: BLOCK
blocked_stage_types: [SUCCESS]
evaluation_logic: AND
allow_override: true
override_reason_required: true
recommended_phases: [EVALUATION, OFFER]

validation_templates:
  - name: "Score mínimo aceptable"
    field_path: "interviews.score"
    aggregator: MIN
    operator: GREATER_THAN_OR_EQUALS
    value_key: "min_acceptable_score"
    default_value: 4
    failure_message_template: "Hay una entrevista con score {value}, mínimo aceptable: {min_acceptable_score}"

default_values:
  min_acceptable_score: 4
```

#### TPL_MIN_POSITIVE_RECOMMENDATIONS
```yaml
code: "TPL_MIN_POSITIVE_RECOMMENDATIONS"
name: "Mínimo de Recomendaciones Positivas"
description: "Requiere X entrevistadores recomendando al candidato"
category: INTERVIEW
rule_type: BLOCK
blocked_stage_types: [SUCCESS]
evaluation_logic: AND
allow_override: true
recommended_phases: [OFFER]

validation_templates:
  - name: "Recomendaciones positivas"
    field_path: "interviews.recommendation"
    aggregator: COUNT
    operator: IN_LIST
    value_key: "positive_recommendations"
    default_value: ["STRONG_YES", "YES"]
    count_operator: GREATER_THAN_OR_EQUALS
    count_value_key: "min_count"
    failure_message_template: "Solo {value} recomendaciones positivas, se requieren {min_count}"

default_values:
  positive_recommendations: ["STRONG_YES", "YES"]
  min_count: 2
```

---

### Plantillas: Categoría TIMELINE

#### TPL_APPLICATION_NOT_STALE
```yaml
code: "TPL_APPLICATION_NOT_STALE"
name: "Aplicación Vigente"
description: "Bloquea si la aplicación es muy antigua"
category: TIMELINE
rule_type: BLOCK
blocked_stage_types: [SUCCESS]
evaluation_logic: AND
allow_override: true
recommended_phases: [SCREENING, INTERVIEW]

validation_templates:
  - name: "Aplicación reciente"
    field_path: "application.applied_at"
    operator: DAYS_AGO_LESS_THAN
    value_key: "max_days"
    default_value: 30
    failure_message_template: "La aplicación tiene más de {max_days} días"

default_values:
  max_days: 30
```

#### TPL_AUTO_ARCHIVE_INACTIVE
```yaml
code: "TPL_AUTO_ARCHIVE_INACTIVE"
name: "Auto-Archivar Inactivos"
description: "Mueve automáticamente candidatos inactivos a archivo"
category: TIMELINE
rule_type: AUTO_MOVE
target_stage_type: FAIL  # Se asigna al stage FAIL del workflow
evaluation_logic: AND
allow_override: false
recommended_phases: [SOURCING, SCREENING]

validation_templates:
  - name: "Inactivo más de X días"
    field_path: "stage_history.current_stage_entered_at"
    operator: DAYS_AGO_GREATER_THAN
    value_key: "inactive_days"
    default_value: 21
    failure_message_template: "Candidato inactivo por más de {inactive_days} días"

default_values:
  inactive_days: 21
```

#### TPL_INTERVIEW_PENDING_WARNING
```yaml
code: "TPL_INTERVIEW_PENDING_WARNING"
name: "Alerta Entrevista Pendiente"
description: "Warning si hay entrevistas pendientes demasiado tiempo"
category: TIMELINE
rule_type: WARNING
evaluation_logic: OR
allow_override: true
recommended_phases: [INTERVIEW]

validation_templates:
  - name: "Entrevista pendiente > X horas"
    field_path: "interviews.created_at"
    filter_field: "status"
    filter_value: "PENDING"
    aggregator: ANY
    operator: HOURS_AGO_GREATER_THAN
    value_key: "max_pending_hours"
    default_value: 72
    failure_message_template: "Hay entrevistas pendientes hace más de {max_pending_hours} horas"

default_values:
  max_pending_hours: 72
```

#### TPL_FRESH_INTERVIEWS_FOR_OFFER
```yaml
code: "TPL_FRESH_INTERVIEWS_FOR_OFFER"
name: "Entrevistas Recientes para Oferta"
description: "Para hacer oferta, las entrevistas deben ser recientes"
category: TIMELINE
rule_type: BLOCK
blocked_stage_types: [SUCCESS]
evaluation_logic: AND
allow_override: true
override_reason_required: true
recommended_phases: [OFFER]

validation_templates:
  - name: "Última entrevista reciente"
    field_path: "interviews.completed_at"
    aggregator: MAX
    operator: DAYS_AGO_LESS_THAN
    value_key: "max_days_since_interview"
    default_value: 14
    failure_message_template: "La última entrevista fue hace más de {max_days_since_interview} días"

default_values:
  max_days_since_interview: 14
```

---

### Plantillas: Categoría AUTOMATION

#### TPL_AUTO_ADVANCE_ON_INTERVIEWS_DONE
```yaml
code: "TPL_AUTO_ADVANCE_ON_INTERVIEWS_DONE"
name: "Auto-Avanzar al Completar Entrevistas"
description: "Mueve al siguiente stage cuando todas las entrevistas están completadas con buen score"
category: AUTOMATION
rule_type: AUTO_MOVE
evaluation_logic: AND
allow_override: true
recommended_phases: [INTERVIEW]

validation_templates:
  - name: "Todas completadas"
    field_path: "interviews.status"
    aggregator: ALL
    operator: EQUALS
    value_key: "completed_status"
    default_value: "COMPLETED"
  - name: "Promedio aceptable"
    field_path: "interviews.score"
    aggregator: AVG
    operator: GREATER_THAN_OR_EQUALS
    value_key: "min_avg_score"
    default_value: 6

default_values:
  completed_status: "COMPLETED"
  min_avg_score: 6
```

#### TPL_AUTO_REJECT_NO_CV
```yaml
code: "TPL_AUTO_REJECT_NO_CV"
name: "Auto-Rechazar Sin CV"
description: "Rechaza automáticamente candidatos sin CV después de X días"
category: AUTOMATION
rule_type: AUTO_MOVE
target_stage_type: FAIL
evaluation_logic: AND
allow_override: false
recommended_phases: [SOURCING]

validation_templates:
  - name: "Sin CV"
    field_path: "candidate.resume_url"
    operator: IS_EMPTY
  - name: "Más de X días"
    field_path: "application.created_at"
    operator: DAYS_AGO_GREATER_THAN
    value_key: "grace_period_days"
    default_value: 3
    failure_message_template: "Candidato sin CV después de {grace_period_days} días"

default_values:
  grace_period_days: 3
```

---

### Activación de Plantillas

```python
@dataclass
class CompanyRuleFromTemplate:
    """Regla de company creada desde una plantilla."""
    id: StageRuleId
    company_id: CompanyId
    stage_id: WorkflowStageId
    template_id: RuleTemplateId
    
    # Valores personalizados (override de default_values)
    custom_values: dict[str, Any]
    
    # Si está activa
    is_active: bool
    
    created_at: datetime
    updated_at: datetime
```

### API para Plantillas

```
# Listar plantillas disponibles
GET /api/v1/rule-templates
GET /api/v1/rule-templates?category=INTERVIEW

# Ver detalle de plantilla
GET /api/v1/rule-templates/{template_code}

# Activar plantilla en un stage
POST /api/v1/stages/{stage_id}/rules/from-template
Body: {
  template_code: "TPL_MIN_INTERVIEW_SCORE",
  custom_values: {
    min_avg_score: 8  # Override del default 7
  }
}

# Actualizar valores de regla basada en plantilla
PATCH /api/v1/stages/{stage_id}/rules/{rule_id}/values
Body: {
  min_avg_score: 6
}
```

---

### Paquetes de Plantillas Recomendados

Las companies pueden activar "paquetes" de plantillas predefinidos según su caso de uso:

#### Paquete: "Básico"
- TPL_REQUIRED_CV
- TPL_ALL_INTERVIEWS_COMPLETED
- TPL_APPLICATION_NOT_STALE

#### Paquete: "Estándar"
- Todo de "Básico" +
- TPL_SALARY_IN_BUDGET
- TPL_MIN_INTERVIEW_SCORE
- TPL_NO_LOW_SCORES
- TPL_AUTO_ARCHIVE_INACTIVE

#### Paquete: "Avanzado"
- Todo de "Estándar" +
- TPL_MIN_EXPERIENCE
- TPL_REQUIRED_LANGUAGES
- TPL_MIN_POSITIVE_RECOMMENDATIONS
- TPL_FRESH_INTERVIEWS_FOR_OFFER
- TPL_AUTO_ADVANCE_ON_INTERVIEWS_DONE

#### Paquete: "Alto Volumen"
- TPL_AUTO_REJECT_NO_CV
- TPL_AUTO_ARCHIVE_INACTIVE
- TPL_SALARY_IN_BUDGET
- TPL_LOCATION_MATCH

---

## 🏗️ Arquitectura de Servicios

### StageRuleEvaluationService

Servicio principal que evalúa reglas.

```python
class StageRuleEvaluationService:
    """Evalúa reglas de stage para un candidato."""
    
    def evaluate_block_rules(
        self,
        candidate_id: CandidateId,
        current_stage_id: WorkflowStageId,
        target_stage_id: WorkflowStageId
    ) -> RuleEvaluationResult:
        """Evalúa reglas de bloqueo para una transición."""
        pass
    
    def evaluate_warning_rules(
        self,
        candidate_id: CandidateId,
        stage_id: WorkflowStageId
    ) -> list[RuleWarning]:
        """Evalúa reglas de warning para un stage."""
        pass
    
    def evaluate_auto_move_rules(
        self,
        candidate_id: CandidateId,
        stage_id: WorkflowStageId
    ) -> Optional[WorkflowStageId]:
        """Evalúa reglas de auto-movimiento. Retorna stage destino o None."""
        pass
```

### RuleEvaluationResult

```python
@dataclass
class RuleEvaluationResult:
    passed: bool
    failed_rules: list[StageRule]
    warnings: list[RuleWarning]
    can_override: bool  # True si TODAS las reglas fallidas permiten override
```

### RuleWarning

```python
@dataclass
class RuleWarning:
    rule: StageRule
    validation: StageRuleValidation
    message: str
    current_value: Any
    expected_value: Any
```

### ValidationEvaluator

```python
class ValidationEvaluator:
    """Evalúa una validación individual."""
    
    def evaluate(
        self,
        validation: StageRuleValidation,
        context: EvaluationContext
    ) -> ValidationResult:
        pass
```

### EvaluationContext

```python
@dataclass
class EvaluationContext:
    """Contexto para evaluar validaciones."""
    candidate: Candidate
    application: CandidateApplication
    position: JobPosition
    interviews: list[Interview]
    custom_field_values: dict[str, Any]
    stage_history: StageHistoryContext
    evaluation_time: datetime          # NOW para comparaciones temporales


@dataclass
class StageHistoryContext:
    """Información temporal del candidato en stages."""
    current_stage_id: WorkflowStageId
    current_stage_entered_at: datetime
    days_in_current_stage: int         # Calculado
    total_days_in_process: int         # Desde application.created_at
    previous_stage_id: Optional[WorkflowStageId]
    previous_stage_exited_at: Optional[datetime]
```

---

## 🔄 Registro de Overrides

Cuando un usuario hace override de una regla, se debe registrar:

```python
@dataclass
class RuleOverride:
    id: RuleOverrideId
    rule_id: StageRuleId
    candidate_id: CandidateId
    user_id: UserId
    reason: Optional[str]
    created_at: datetime
```

Esto permite:
- Auditoría de quién saltó qué reglas
- Análisis de reglas que se saltan frecuentemente
- Posible revisión de reglas poco útiles

---

## 📊 Configuración por Company

```python
@dataclass
class CompanyRuleSettings:
    company_id: CompanyId
    
    # Triggers
    evaluate_on_candidate_update: bool = True
    evaluate_on_interview_complete: bool = True
    cron_evaluation_enabled: bool = False
    cron_evaluation_interval_hours: int = 24
    
    # Comportamiento
    require_override_reason: bool = True
    notify_on_auto_move: bool = True
    notify_on_block: bool = True
```

---

## 📱 API Endpoints

### Gestión de Reglas

```
POST   /api/v1/stages/{stage_id}/rules           # Crear regla
GET    /api/v1/stages/{stage_id}/rules           # Listar reglas del stage
GET    /api/v1/stages/{stage_id}/rules/{rule_id} # Obtener regla
PUT    /api/v1/stages/{stage_id}/rules/{rule_id} # Actualizar regla
DELETE /api/v1/stages/{stage_id}/rules/{rule_id} # Eliminar regla
POST   /api/v1/stages/{stage_id}/rules/reorder   # Reordenar prioridad
```

### Evaluación Manual

```
POST /api/v1/candidates/{id}/evaluate-rules
  Body: { stage_id: string }
  Response: { 
    can_proceed: bool,
    blocked_by: StageRule[],
    warnings: RuleWarning[],
    can_override: bool
  }
```

### Override

```
POST /api/v1/candidates/{id}/override-rule
  Body: { 
    rule_id: string,
    target_stage_id: string,
    reason?: string
  }
```

---

## 🎯 Prioridades de Implementación

### Fase 1: Fundamentos
1. Crear entidades `StageRule`, `StageRuleValidation`
2. Crear enums `StageRuleTypeEnum`, `ValidationTypeEnum`, etc.
3. Implementar `ValidationEvaluator` básico
4. Implementar evaluación de reglas BLOCK

### Fase 2: Warnings y Override
1. Implementar evaluación de reglas WARNING
2. Implementar sistema de override
3. Crear registro de overrides

### Fase 3: Auto-movimiento
1. Implementar AUTO_MOVE con evaluación AND/OR
2. Integrar triggers en eventos de candidato/entrevista
3. Implementar job de cron (opcional)

### Fase 4: UI y Configuración
1. Endpoints de gestión de reglas
2. Configuración por company
3. UI para crear/editar reglas

---

## 🤔 Decisiones Pendientes

1. **¿JsonLogic o estructura propia?**
   - JsonLogic es más flexible pero más complejo
   - Estructura propia es más simple pero menos extensible
   - **Propuesta:** Empezar con estructura propia, migrar a JsonLogic si se necesita más flexibilidad

2. **¿Reglas a nivel de Stage o de Workflow?**
   - A nivel de stage permite más granularidad
   - A nivel de workflow permite reutilización
   - **Propuesta:** A nivel de stage, con posibilidad de "plantillas" de reglas a futuro

3. **¿Notificaciones de auto-movimiento?**
   - ¿Al candidato? ¿Al reclutador? ¿Ambos?
   - **Propuesta:** Configurable por company, por defecto solo al reclutador

4. **¿Límite de reglas por stage?**
   - Evitar stages con cientos de reglas
   - **Propuesta:** Soft limit de 20 reglas por stage, configurable

