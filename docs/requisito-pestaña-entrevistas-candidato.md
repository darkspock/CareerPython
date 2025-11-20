# Requisito: Pestaña de Entrevistas en Detalle de Candidato

## Descripción del Requisito

Se necesita agregar una nueva pestaña "Entrevistas" en la página de detalle del candidato (`/company/candidates/{id}`) que permita:

1. **Visualizar entrevistas**:
   - **Entrevistas de la etapa actual** del candidato
   - **Entrevistas de otras etapas** (etapas pasadas o futuras del workflow)
   - Todas las entrevistas DEBEN estar asociadas a una etapa específica (`workflow_stage_id` es obligatorio)

2. **Asignar nueva entrevista** mediante un botón que abra un formulario con:
   - **Etapa del workflow** (obligatorio - puede ser la actual o cualquier otra)
   - **Tipo de entrevista** (obligatorio)
   - **Plantilla** (si existe más de una plantilla para el tipo seleccionado, mostrar selector)
   - **Fecha** (opcional)
   - **Roles obligatorios**
   - **Participantes** (opcional - lista de usuarios de la empresa por cada uno de los roles seleccionados)

## Análisis del Estado Actual

### Estructura de Entrevistas Existente

#### Backend

**Entidad `Interview`** (`src/interview_bc/interview/domain/entities/interview.py`):
- `id: InterviewId`
- `candidate_id: CandidateId` ✅
- `workflow_stage_id: WorkflowStageId` ✅ **OBLIGATORIO - Siempre debe tener etapa**
- `job_position_id: JobPositionId` ✅
- `required_roles: List[CompanyRoleId]` ✅ **OBLIGATORIO**
- `interview_template_id: Optional[InterviewTemplateId]` ✅ Opcional
- `interview_type: InterviewTypeEnum` ✅
- `scheduled_at: Optional[datetime]` ✅ Opcional
- `deadline_date: Optional[datetime]` ✅ Opcional
- `interviewers: List[str]` ✅ Lista de nombres de entrevistadores

**Comando `CreateInterviewCommand`** (`src/interview_bc/interview/application/commands/create_interview.py`):
- Requiere `workflow_stage_id` (obligatorio) ✅
- Requiere `required_roles` (obligatorio, lista no vacía) ✅
- `interview_template_id` es opcional ✅
- `scheduled_at` es opcional ✅
- `interviewers` es opcional (pero se pasa como lista de nombres, no IDs) ✅

**Query `ListInterviewsQuery`** (`src/interview_bc/interview/application/queries/list_interviews.py`):
- Permite filtrar por `candidate_id` ✅
- Permite filtrar por `workflow_stage_id` (implícito en el repositorio) ✅
- **Necesario**: Listar TODAS las entrevistas del candidato (todas las etapas)

**Repositorio `InterviewRepositoryInterface`**:
- `find_by_filters_with_joins()` permite filtrar por `candidate_id` y otros parámetros
- No tiene método específico para obtener entrevistas globales vs específicas de etapa

#### Frontend

**Servicio `companyInterviewService.ts`**:
- `listInterviews()` - lista entrevistas con filtros
- `createInterview()` - crea una entrevista
- `getInterviewById()` - obtiene una entrevista por ID

**Tipo `Interview`**:
- `workflow_stage_id?: string` - actualmente opcional en el tipo TypeScript
- `required_roles: string[]` - lista de IDs de roles
- `interviewers?: string[]` - lista de IDs de entrevistadores (pero en backend es lista de nombres)

**Página `CandidateDetailPage.tsx`**:
- Actualmente tiene pestañas: `info`, `comments`, `reviews`, `documents`, `history`
- No tiene pestaña de entrevistas

## Cambios Necesarios para la Implementación

### 1. Backend - Modificar Query de Listado

#### 1.1 Actualizar Query de Listado de Entrevistas

**Archivo**: `src/interview_bc/interview/application/queries/list_interviews.py`

**Cambios**:
- Ya permite filtrar por `candidate_id` ✅
- Asegurar que cuando se filtra solo por `candidate_id` (sin `workflow_stage_id`), retorne **todas las entrevistas** del candidato de todas las etapas
- Opcionalmente, agregar parámetro `only_current_stage: bool = False` para filtrar solo la etapa actual

**Archivo**: `src/interview_bc/interview/domain/infrastructure/interview_repository_interface.py`

**Cambios**:
- Verificar que `find_by_filters_with_joins()` permita filtrar solo por `candidate_id` sin especificar `workflow_stage_id`
- Cuando no se especifica `workflow_stage_id`, debe retornar todas las entrevistas del candidato

**Archivo**: `src/interview_bc/interview/Infrastructure/repositories/interview_repository.py`

**Cambios**:
- Asegurar que el filtrado por `candidate_id` retorne todas las entrevistas (de todas las etapas)
- No aplicar filtro de `workflow_stage_id` si no se proporciona

#### 1.2 Mantener Schema de Request (sin cambios)

**Archivo**: `adapters/http/company_app/interview/schemas/interview_management.py`

**Cambios**:
- Hacer `workflow_stage_id` opcional en `InterviewCreateRequest`
- Agregar validación: si `workflow_stage_id` es `None`, la entrevista es global

#### 1.5 Actualizar Controller

**Archivo**: `adapters/http/company_app/interview/controllers/interview_controller.py`

**Cambios**:
- Actualizar `create_interview()` para manejar `workflow_stage_id` opcional
- Actualizar `list_interviews()` para aceptar parámetros `include_global` y `workflow_stage_id`

**Archivo**: `adapters/http/company_app/interview/routers/interview_router.py`

**Cambios**:
- Actualizar endpoints para aceptar `workflow_stage_id` opcional
- Agregar parámetro `include_global` en el endpoint de listado

### 2. Frontend - Nueva Pestaña de Entrevistas

#### 2.1 Crear Hook para Entrevistas

**Archivo**: `client-vite/src/hooks/useCandidateInterviews.ts` (nuevo)

**Funcionalidad**:
- Cargar **todas las entrevistas** del candidato (de todas las etapas)
- Separar entrevistas de la etapa actual de las de otras etapas
- Función para crear nueva entrevista (requiere especificar etapa)
- Estados de loading y error

**Estructura**:
```typescript
interface UseCandidateInterviewsProps {
  candidateId: string | undefined;
  companyCandidateId: string | undefined;
  currentStageId: string | null | undefined;
}

export function useCandidateInterviews({
  candidateId,
  companyCandidateId,
  currentStageId,
}: UseCandidateInterviewsProps) {
  const [allInterviews, setAllInterviews] = useState<Interview[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Computed: entrevistas de la etapa actual
  const currentStageInterviews = allInterviews.filter(
    i => i.workflow_stage_id === currentStageId
  );
  
  // Computed: entrevistas de otras etapas
  const otherStagesInterviews = allInterviews.filter(
    i => i.workflow_stage_id !== currentStageId
  );

  const loadInterviews = useCallback(async () => {
    // Cargar TODAS las entrevistas del candidato (sin filtrar por etapa)
  }, [candidateId]);

  const createInterview = useCallback(async (data: CreateInterviewData) => {
    // Crear nueva entrevista (workflow_stage_id es obligatorio)
  }, []);

  return {
    allInterviews,
    currentStageInterviews,
    otherStagesInterviews,
    loading,
    error,
    loadInterviews,
    createInterview,
  };
}
```

#### 2.2 Crear Componente de Lista de Entrevistas

**Archivo**: `client-vite/src/components/candidate/CandidateInterviewsSection.tsx` (nuevo)

**Funcionalidad**:
- Mostrar dos secciones: 
  - **"Entrevistas de la Etapa Actual"** (si el candidato tiene etapa actual)
  - **"Entrevistas de Otras Etapas"** (expandible/colapsable)
- Mostrar lista de entrevistas con información relevante:
  - Nombre de la etapa asociada
  - Tipo de entrevista
  - Estado (PENDING, IN_PROGRESS, COMPLETED)
  - Fecha programada (si existe)
  - Participantes/roles requeridos
- Botón para asignar nueva entrevista (requiere seleccionar etapa)

**Estructura**:
```typescript
interface CandidateInterviewsSectionProps {
  candidateId: string;
  companyCandidateId: string;
  currentStageId: string | null | undefined;
  currentWorkflowId: string | null | undefined;
  availableStages: WorkflowStage[]; // Para selector en modal
}

export default function CandidateInterviewsSection({
  candidateId,
  companyCandidateId,
  currentStageId,
  currentWorkflowId,
  availableStages,
}: CandidateInterviewsSectionProps) {
  const interviewsHook = useCandidateInterviews({
    candidateId,
    companyCandidateId,
    currentStageId,
  });

  const [showAssignModal, setShowAssignModal] = useState(false);

  return (
    <div>
      {/* Sección de Entrevistas de la Etapa Actual */}
      {/* Sección de Entrevistas de Otras Etapas (colapsable) */}
      {/* Botón para asignar entrevista */}
      {/* Modal de asignación */}
    </div>
  );
}
```

#### 2.3 Crear Modal de Asignación de Entrevista

**Archivo**: `client-vite/src/components/candidate/AssignInterviewModal.tsx` (nuevo)

**Funcionalidad**:
- Formulario para crear nueva entrevista
- **Selector de etapa del workflow** (obligatorio - pre-seleccionar etapa actual si existe)
- Selector de tipo de entrevista (obligatorio)
- Selector de plantilla (si hay más de una para el tipo seleccionado)
- Selector de fecha (opcional, con date picker)
- Selector de roles obligatorios (obligatorio - al menos uno)
- Selector de participantes (opcional, multi-select de usuarios)

**Estructura**:
```typescript
interface AssignInterviewModalProps {
  candidateId: string;
  companyCandidateId: string;
  currentStageId: string | null | undefined;
  currentWorkflowId: string | null | undefined;
  availableStages: WorkflowStage[]; // Todas las etapas disponibles del workflow
  jobPositionId?: string;
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

export default function AssignInterviewModal({
  candidateId,
  companyCandidateId,
  currentStageId,
  currentWorkflowId,
  availableStages,
  jobPositionId,
  isOpen,
  onClose,
  onSuccess,
}: AssignInterviewModalProps) {
  const [workflowStageId, setWorkflowStageId] = useState<string>(currentStageId || ''); // Pre-seleccionar etapa actual
  const [interviewType, setInterviewType] = useState<string>('');
  const [templateId, setTemplateId] = useState<string | null>(null);
  const [scheduledAt, setScheduledAt] = useState<Date | null>(null);
  const [participants, setParticipants] = useState<string[]>([]);
  const [requiredRoles, setRequiredRoles] = useState<string[]>([]);

  // Cargar etapas disponibles del workflow
  // Cargar tipos de entrevista disponibles
  // Cargar plantillas según el tipo seleccionado
  // Cargar usuarios disponibles para participantes
  // Cargar roles disponibles
  // Validar formulario (workflow_stage_id y required_roles obligatorios)
  // Enviar creación de entrevista

  return (
    <Modal isOpen={isOpen} onClose={onClose}>
      {/* Formulario */}
    </Modal>
  );
}
```

#### 2.4 Actualizar Servicio de Entrevistas

**Archivo**: `client-vite/src/services/companyInterviewService.ts`

**Cambios**:
- ✅ Mantener `createInterview()` sin cambios (`workflow_stage_id` es obligatorio)
- Verificar/agregar método `listInterviewsByCandidate(candidateId: string)` que retorne **todas** las entrevistas del candidato
- Asegurar que los tipos TypeScript incluyen `workflow_stage_id: string` (obligatorio)

#### 2.5 Integrar en CandidateDetailPage

**Archivo**: `client-vite/src/pages/company/CandidateDetailPage.tsx`

**Cambios**:
- Agregar `'interviews'` al tipo de `activeTab`
- Agregar botón de pestaña "Entrevistas" en el nav
- Agregar contenido de la pestaña con `CandidateInterviewsSection`
- Pasar `candidate.current_stage_id` y `candidate.current_workflow_id` al componente

### 3. Servicios Adicionales Necesarios

#### 3.1 Obtener Tipos de Entrevista Disponibles

**Backend**:
- Crear query `GetAvailableInterviewTypesQuery` que retorne los tipos disponibles
- O usar el enum `InterviewTypeEnum` directamente en el frontend

**Frontend**:
- Usar el enum `InterviewType` existente o crear servicio para obtener tipos disponibles

#### 3.2 Obtener Plantillas por Tipo

**Backend**:
- Ya existe `ListInterviewTemplatesQuery`
- Filtrar por `template_type` o `interview_type` si está disponible

**Frontend**:
- Usar servicio existente `companyInterviewTemplateService.listTemplates()`
- Filtrar por tipo de entrevista seleccionado

#### 3.3 Obtener Usuarios de la Empresa

**Backend**:
- Ya existe query para obtener usuarios de la empresa
- Usar `ListCompanyUsersQuery` o similar

**Frontend**:
- Usar servicio existente `companyUserService.getCompanyUsers()`

#### 3.4 Obtener Roles de la Empresa

**Backend**:
- Ya existe query para obtener roles de la empresa
- Usar `ListCompanyRolesQuery` o similar

**Frontend**:
- Usar servicio existente para obtener roles

### 4. Consideraciones de Validación

#### 4.1 Validaciones en Backend

- Si `workflow_stage_id` es `None`, la entrevista es global
- Si `workflow_stage_id` está presente, debe ser válido y existir
- `required_roles` debe ser una lista no vacía (obligatorio)
- Si se proporciona `interview_template_id`, debe existir y ser válido
- Si la plantilla requiere roles específicos, validar que `required_roles` incluya esos roles

#### 4.2 Validaciones en Frontend

- Tipo de entrevista es obligatorio
- Si hay más de una plantilla para el tipo seleccionado, mostrar selector
- Si hay solo una plantilla, seleccionarla automáticamente
- Si no hay plantillas para el tipo seleccionado, permitir crear sin plantilla
- Validar que si se selecciona fecha, sea en el futuro
- Validar que si se seleccionan participantes, sean válidos

### 5. Orden de Implementación Recomendado

#### Fase 1: Backend - Verificar y Ajustar Queries
1. ✅ Mantener entidad `Interview` con `workflow_stage_id` obligatorio
2. ✅ No se requiere migración de base de datos
3. Verificar que `ListInterviewsQuery` permita filtrar por `candidate_id` sin especificar `workflow_stage_id`
4. Asegurar que el repositorio retorna todas las entrevistas del candidato cuando no se especifica etapa
5. Verificar que el controller y router funcionan correctamente
6. Verificar que los DTOs incluyen información de la etapa

#### Fase 2: Frontend - Componentes Base
1. Crear hook `useCandidateInterviews` (cargar todas las entrevistas y separarlas)
2. Crear componente `CandidateInterviewsSection` (dos secciones: actual y otras)
3. Actualizar servicio `companyInterviewService` si es necesario
4. Integrar en `CandidateDetailPage`

#### Fase 3: Frontend - Modal de Asignación
1. Crear componente `AssignInterviewModal` (incluir selector de etapa)
2. Implementar lógica de carga de etapas disponibles del workflow
3. Implementar lógica de carga de tipos, plantillas, usuarios y roles
4. Implementar validaciones del formulario (etapa y roles obligatorios)
5. Integrar con el hook y servicio

#### Fase 4: Testing y Ajustes
1. Probar creación de entrevistas en diferentes etapas
2. Probar que la entrevista aparece en la sección correcta según su etapa
3. Probar listado completo (etapa actual + otras etapas)
4. Ajustar UI/UX según feedback

## Preguntas Abiertas

1. **¿Qué significa "entrevistas globales"?**
   - ¿Entrevistas que no están asociadas a ninguna etapa (`workflow_stage_id = NULL`)?
   - ¿Entrevistas que se aplican a todas las etapas?
   - ¿Entrevistas que están asociadas a la fase pero no a una etapa específica?

2. **¿Cómo se determinan los roles obligatorios?**
   - ¿Vienen de la plantilla?
   - ¿Se configuran por tipo de entrevista?
   - ¿El usuario los selecciona manualmente?

3. **¿Los participantes son usuarios de la empresa o pueden ser externos?**
   - Actualmente `interviewers` es una lista de nombres (strings)
   - ¿Deberíamos cambiarlo a IDs de usuarios?

4. **¿Qué información mostrar en la lista de entrevistas?**
   - Tipo, estado, fecha, participantes, roles requeridos
   - ¿Acciones disponibles (editar, cancelar, ver detalles)?

5. **¿Se pueden editar entrevistas desde esta vista?**
   - ¿O solo crear nuevas?

## Notas Técnicas

- ✅ El campo `workflow_stage_id` es y seguirá siendo **OBLIGATORIO** en el modelo de dominio
- ✅ **NO** se requiere migración de base de datos
- ✅ Todas las entrevistas deben estar asociadas a una etapa específica del workflow
- El campo `required_roles` es obligatorio y debe tener al menos un rol
- El campo `interviewers` en el backend es una lista de nombres (strings), no IDs de usuarios
- Considerar si esto debería cambiarse a IDs para mejor integración
- Las queries deben permitir obtener todas las entrevistas de un candidato (de todas las etapas) para mostrarlas agrupadas

