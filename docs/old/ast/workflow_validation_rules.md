# Reglas de Validación: Stage-Phase Consistency
**CareerPython ATS - Documento de Arquitectura**  
*Fecha:* 2025-11-10 | *Versión:* 1.0

---

## Reglas de Negocio

### Regla 1: Presencia Obligatoria de Stage y Phase
**Enunciado**: Un `JobPosition` o `CompanyCandidate` **siempre** debe tener `stage_id` y `phase_id` cuando está en un workflow activo.

**Excepciones**:
- Un `CompanyCandidate` puede crearse sin workflow inicialmente (se asigna después)
- Un `JobPosition` puede crearse sin workflow inicialmente (se asigna después)

### Regla 2: Consistencia Stage-Phase
**Enunciado**: El `stage_id` debe pertenecer a un workflow que pertenezca al `phase_id` especificado.

**Lógica**:
```
stage_id → WorkflowStage.workflow_id → Workflow.phase_id == phase_id
```

---

## Ubicación de Validaciones según DDD

### Principio: Domain Service (Domain Layer)

Según los principios de **Domain-Driven Design (DDD)**, las reglas de negocio deben estar en el **Domain Layer** para evitar el "anemic domain model". 

**Solución**: Crear un **Domain Service** que encapsule la lógica de validación.

**Razón**: 
- Las reglas de negocio pertenecen al dominio, no a la aplicación
- Un Domain Service puede recibir repositorios como dependencias (inyección de dependencias)
- Evita que las entidades tengan dependencias de repositorios directamente
- Los Command Handlers (Application Layer) orquestan y llaman al Domain Service
- Mantiene el dominio rico en lógica de negocio

**Arquitectura**:
```
Domain Layer (Domain Service)
    ↓ (llamado por)
Application Layer (Command Handlers)
    ↓ (usa)
Infrastructure Layer (Repositories)
```

---

## Puntos de Validación Requeridos

### 1. CreateJobPositionCommandHandler

**Ubicación**: `src/company_bc/job_position/application/commands/create_job_position.py`

**Validaciones a agregar**:
```python
# Si se proporciona stage_id, debe:
# 1. Existir el stage
# 2. El stage debe pertenecer a un workflow
# 3. El workflow debe tener phase_id
# 4. Si se proporciona phase_id en phase_workflows, debe coincidir

if command.stage_id:
    # Validar que stage existe y pertenece a workflow con phase_id
    stage = self.stage_repository.get_by_id(command.stage_id)
    if not stage:
        raise JobPositionValidationError("Stage not found")
    
    workflow = self.workflow_repository.get_by_id(stage.workflow_id)
    if not workflow:
        raise JobPositionValidationError("Workflow not found for stage")
    
    if not workflow.phase_id:
        raise JobPositionValidationError("Workflow must belong to a phase")
    
    # Si hay phase_workflows configurado, verificar consistencia
    if command.phase_workflows:
        workflow_phase_id = workflow.phase_id.value
        if workflow_phase_id not in command.phase_workflows:
            raise JobPositionValidationError(
                f"Stage belongs to workflow in phase {workflow_phase_id}, "
                f"but phase_workflows does not include this phase"
            )
```

**Nota**: `JobPosition` no tiene `phase_id` directamente, pero el workflow tiene `phase_id`. La validación debe asegurar que si hay `stage_id`, el workflow del stage tenga `phase_id`.

---

### 2. CreateCompanyCandidateCommandHandler

**Ubicación**: `src/company_bc/company_candidate/application/commands/create_company_candidate_command.py`

**Validaciones a agregar**:
```python
# Cuando se asigna workflow (después de crear el candidato):
# 1. El initial_stage_id debe pertenecer al workflow_id
# 2. El workflow debe tener phase_id
# 3. El phase_id del candidato debe coincidir con el phase_id del workflow

if workflow_id and initial_stage_id:
    # Validar que stage pertenece al workflow
    stage = self._stage_repository.get_by_id(initial_stage_id)
    if not stage:
        raise ValueError("Initial stage not found")
    
    if stage.workflow_id.value != workflow_id.value:
        raise ValueError(
            f"Stage {initial_stage_id.value} does not belong to workflow {workflow_id.value}"
        )
    
    # Validar que workflow tiene phase_id
    workflow = self._workflow_repository.get_by_id(workflow_id)
    if not workflow:
        raise ValueError("Workflow not found")
    
    if not workflow.phase_id:
        raise ValueError("Workflow must belong to a phase")
    
    # Validar que phase_id coincide
    if phase_id and phase_id.value != workflow.phase_id.value:
        raise ValueError(
            f"Phase ID mismatch: candidate phase {phase_id.value} != workflow phase {workflow.phase_id.value}"
        )
```

**Nota**: Este handler ya intenta asignar workflow automáticamente, pero falta validar la consistencia.

---

### 3. AssignWorkflowCommandHandler

**Ubicación**: `src/company_bc/company_candidate/application/commands/assign_workflow_command.py`

**Validaciones a agregar**:
```python
# 1. El initial_stage_id debe pertenecer al workflow_id
# 2. El workflow debe tener phase_id
# 3. Si el candidato ya tiene phase_id, debe coincidir con el workflow.phase_id

# Validar que stage pertenece al workflow
stage = self._stage_repository.get_by_id(command.initial_stage_id)
if not stage:
    raise ValueError(f"Stage {command.initial_stage_id.value} not found")

if stage.workflow_id.value != command.workflow_id.value:
    raise ValueError(
        f"Stage {command.initial_stage_id.value} does not belong to workflow {command.workflow_id.value}"
    )

# Validar que workflow tiene phase_id
workflow = self._workflow_repository.get_by_id(command.workflow_id)
if not workflow:
    raise ValueError(f"Workflow {command.workflow_id.value} not found")

if not workflow.phase_id:
    raise ValueError(f"Workflow {command.workflow_id.value} must belong to a phase")

# Validar consistencia de phase_id
if company_candidate.phase_id:
    if company_candidate.phase_id != workflow.phase_id.value:
        raise ValueError(
            f"Phase ID mismatch: candidate phase {company_candidate.phase_id} != "
            f"workflow phase {workflow.phase_id.value}"
        )
```

**Nota**: Este handler actualmente no valida nada. Necesita inyectar `WorkflowRepositoryInterface` y `WorkflowStageRepositoryInterface`.

---

### 4. ChangeStageCommandHandler

**Ubicación**: `src/company_bc/company_candidate/application/commands/change_stage_command.py`

**Validaciones a agregar**:
```python
# Ya valida parcialmente, pero debemos asegurar:
# 1. Si el candidato tiene phase_id, el nuevo stage debe pertenecer a un workflow de esa phase
# 2. Si el stage pertenece a un workflow de diferente phase, actualizar phase_id correctamente

# Validación adicional después de obtener target_stage y target_workflow:
if company_candidate.phase_id:
    current_phase_id = PhaseId.from_string(company_candidate.phase_id)
    
    # Si el target workflow tiene phase_id diferente, debe actualizarse
    if target_workflow.phase_id:
        if current_phase_id and current_phase_id.value != target_workflow.phase_id.value:
            # Esto ya se maneja en el código actual, pero debemos validar que es correcto
            pass
    else:
        raise ValueError(
            f"Target workflow {target_workflow.id.value} must belong to a phase"
        )
```

**Nota**: Este handler ya maneja la transición entre phases, pero falta validar que el workflow siempre tenga `phase_id`.

---

### 5. MoveJobPositionToStageCommandHandler

**Ubicación**: `src/company_bc/job_position/application/commands/move_job_position_to_stage.py`

**Validaciones a agregar**:
```python
# Ya valida que el stage pertenece al workflow, pero debemos asegurar:
# 1. El workflow debe tener phase_id
# 2. Si job_position tiene phase_workflows, debe incluir el phase_id del workflow

# Después de obtener workflow (línea ~88):
if not workflow.phase_id:
    raise JobPositionValidationError(
        "Workflow must belong to a phase",
        {"workflow": ["Workflow must have a phase_id"]}
    )

# Validar consistencia con phase_workflows si existe
if job_position.phase_workflows:
    workflow_phase_id = workflow.phase_id.value
    if workflow_phase_id not in job_position.phase_workflows:
        raise JobPositionValidationError(
            f"Stage belongs to workflow in phase {workflow_phase_id}, "
            f"but job position phase_workflows does not include this phase",
            {"phase": [f"Phase {workflow_phase_id} not in phase_workflows"]}
        )
```

**Nota**: Este handler ya valida que el stage pertenece al workflow, pero falta validar que el workflow tenga `phase_id`.

---

## Domain Service de Validación (Recomendado)

Para evitar duplicación de código y mantener el dominio rico, se debe crear un **Domain Service**:

**Ubicación**: `src/shared_bc/customization/workflow/domain/services/stage_phase_validation_service.py`

**Nota**: Los Domain Services están en el Domain Layer porque encapsulan reglas de negocio que requieren acceso a múltiples entidades o repositorios, pero la lógica pertenece al dominio.

```python
"""
Domain Service for validating stage-phase consistency.

This is a Domain Service because it encapsulates business rules that require
access to multiple domain entities through repositories. The logic belongs to
the domain, not the application layer.
"""
from typing import Optional
from src.shared_bc.customization.workflow.domain.interfaces.workflow_repository_interface import WorkflowRepositoryInterface
from src.shared_bc.customization.workflow.domain.interfaces.workflow_stage_repository_interface import WorkflowStageRepositoryInterface
from src.shared_bc.customization.workflow.domain.value_objects.workflow_stage_id import WorkflowStageId
from src.shared_bc.customization.workflow.domain.value_objects.workflow_id import WorkflowId
from src.shared_bc.customization.phase.domain.value_objects.phase_id import PhaseId


class StagePhaseValidationService:
    """
    Domain Service for validating stage-phase consistency rules.
    
    This service encapsulates the business rule that a stage must belong to
    a workflow that belongs to a phase. It's a Domain Service because:
    - It contains domain logic (business rules)
    - It requires access to repositories to validate across entities
    - It's called from Application Layer (Command Handlers) but the logic is domain logic
    """
    
    def __init__(
        self,
        workflow_repository: WorkflowRepositoryInterface,
        stage_repository: WorkflowStageRepositoryInterface
    ):
        self.workflow_repository = workflow_repository
        self.stage_repository = stage_repository
    
    def validate_stage_belongs_to_phase(
        self,
        stage_id: WorkflowStageId,
        expected_phase_id: Optional[PhaseId] = None
    ) -> tuple[WorkflowId, PhaseId]:
        """
        Validate that a stage belongs to a workflow that belongs to a phase.
        
        Args:
            stage_id: The stage ID to validate
            expected_phase_id: Optional phase ID to check against
            
        Returns:
            Tuple of (workflow_id, phase_id) if valid
            
        Raises:
            ValueError: If validation fails
        """
        # Get stage
        stage = self.stage_repository.get_by_id(stage_id)
        if not stage:
            raise ValueError(f"Stage {stage_id.value} not found")
        
        # Get workflow
        workflow = self.workflow_repository.get_by_id(stage.workflow_id)
        if not workflow:
            raise ValueError(f"Workflow {stage.workflow_id.value} not found for stage {stage_id.value}")
        
        # Validate workflow has phase_id
        if not workflow.phase_id:
            raise ValueError(f"Workflow {workflow.id.value} must belong to a phase")
        
        # Validate phase_id matches if expected
        if expected_phase_id:
            if workflow.phase_id.value != expected_phase_id.value:
                raise ValueError(
                    f"Stage {stage_id.value} belongs to workflow in phase {workflow.phase_id.value}, "
                    f"but expected phase is {expected_phase_id.value}"
                )
        
        return (workflow.id, workflow.phase_id)
    
    def validate_stage_belongs_to_workflow(
        self,
        stage_id: WorkflowStageId,
        workflow_id: WorkflowId
    ) -> None:
        """
        Validate that a stage belongs to a specific workflow.
        
        Args:
            stage_id: The stage ID to validate
            workflow_id: The workflow ID to check against
            
        Raises:
            ValueError: If validation fails
        """
        stage = self.stage_repository.get_by_id(stage_id)
        if not stage:
            raise ValueError(f"Stage {stage_id.value} not found")
        
        if stage.workflow_id.value != workflow_id.value:
            raise ValueError(
                f"Stage {stage_id.value} does not belong to workflow {workflow_id.value}"
            )
```

**Uso en Command Handlers**:
```python
# Inyectar el servicio en el constructor
def __init__(
    self,
    repository: CompanyCandidateRepositoryInterface,
    validation_service: StagePhaseValidationService
):
    self._repository = repository
    self._validation_service = validation_service

# Usar en execute()
workflow_id, phase_id = self._validation_service.validate_stage_belongs_to_phase(
    command.initial_stage_id,
    expected_phase_id=PhaseId.from_string(company_candidate.phase_id) if company_candidate.phase_id else None
)
```

---

## Resumen de Implementación

### Prioridad ALTA (Crítico)

1. **AssignWorkflowCommandHandler** - No valida nada actualmente
2. **CreateCompanyCandidateCommandHandler** - Valida parcialmente, falta consistencia phase_id
3. **CreateJobPositionCommandHandler** - No valida consistencia stage-phase

### Prioridad MEDIA

4. **ChangeStageCommandHandler** - Ya valida parcialmente, mejorar validación de phase_id
5. **MoveJobPositionToStageCommandHandler** - Ya valida parcialmente, agregar validación de phase_id

### Recomendado (Domain Service)

6. **StagePhaseValidationService** - Crear Domain Service en Domain Layer para encapsular reglas de negocio

---

## Checklist de Implementación

### Para cada Command Handler:

- [ ] Inyectar `WorkflowRepositoryInterface` si no está
- [ ] Inyectar `WorkflowStageRepositoryInterface` si no está
- [ ] Validar que `stage_id` existe
- [ ] Validar que `stage.workflow_id` existe
- [ ] Validar que `workflow.phase_id` existe (no es None)
- [ ] Validar que `workflow.phase_id` coincide con `expected_phase_id` (si se proporciona)
- [ ] Lanzar excepciones apropiadas con mensajes claros

### Para el Domain Service de Validación:

- [ ] Crear carpeta `src/shared_bc/customization/workflow/domain/services/`
- [ ] Crear `StagePhaseValidationService` en Domain Layer
- [ ] Implementar `validate_stage_belongs_to_phase()`
- [ ] Implementar `validate_stage_belongs_to_workflow()`
- [ ] Registrar servicio en `core/container.py` (inyección de dependencias)
- [ ] Actualizar Command Handlers para inyectar y usar el Domain Service

---

## Excepciones a Lanzar

### Para CompanyCandidate:
- `ValueError`: Para errores de validación generales
- `CompanyCandidateValidationError`: Para errores específicos del dominio (si existe)

### Para JobPosition:
- `JobPositionValidationError`: Para errores de validación (ya existe)

**Formato de mensajes**:
- Descriptivos y específicos
- Incluir IDs relevantes para debugging
- Indicar qué se esperaba vs qué se encontró

---

## Notas Finales

1. **Domain Service vs Application Service**: 
   - **Domain Service**: Contiene lógica de negocio del dominio, puede recibir repositorios como dependencias
   - **Application Service (Command Handler)**: Orquesta la lógica, coordina Domain Services y repositorios
   - En este caso, la validación es una **regla de negocio**, por lo que va en un **Domain Service**

2. **No validar en Entidades directamente**: Las entidades no deben tener dependencias de repositorios. Las validaciones complejas que requieren acceso a repositorios van en Domain Services.

3. **Validar en el momento correcto**: Validar cuando se asigna workflow/stage, no en la creación inicial si no se proporciona.

4. **Mensajes de error claros**: Los mensajes deben ayudar a identificar el problema rápidamente.

5. **Consistencia**: Aplicar las mismas validaciones en todos los puntos de entrada usando el mismo Domain Service.

6. **Evitar Anemic Domain Model**: Mantener la lógica de negocio en el Domain Layer (Domain Services) en lugar de moverla toda a la Application Layer.

---

**Última actualización**: 2025-11-10  
**Versión del documento**: 1.0  
**Autor**: CareerPython Development Team

