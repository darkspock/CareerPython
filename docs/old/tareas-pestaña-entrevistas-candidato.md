# Tareas - Pestaña de Entrevistas en Detalle de Candidato

**Proyecto**: CareerPython  
**Requisito**: [requisito-pestaña-entrevistas-candidato.md](requisito-pestaña-entrevistas-candidato.md)  
**Fecha**: 2025-01-28  
**ACTUALIZACIÓN**: workflow_stage_id es OBLIGATORIO - No hay entrevistas globales

---

## ⚠️ ACLARACIÓN IMPORTANTE

**NO** hay entrevistas "globales" sin etapa. Todas las entrevistas **DEBEN** tener `workflow_stage_id` (campo obligatorio).

Lo que se necesita es:
- Mostrar **todas las entrevistas del candidato** (de cualquier etapa)
- Separar visualmente: "Entrevistas de la Etapa Actual" vs "Entrevistas de Otras Etapas"
- Permitir asignar entrevistas a cualquier etapa del workflow, no solo la actual

---

## Resumen

Este documento contiene la lista de tareas necesarias para implementar la pestaña de "Entrevistas" en la página de detalle del candidato.

**Total de tareas**: 15 (reducido de 24)  
**Fases**: 4

---

## Fase 1: Backend - Verificar Queries Existentes

**Objetivo**: Asegurar que las queries permitan obtener todas las entrevistas de un candidato sin filtrar por etapa.

### ✅ BACKEND-1: Verificar ListInterviewsQuery
**Archivo**: `src/interview_bc/interview/application/queries/list_interviews.py`

**Descripción**:
- Verificar que `ListInterviewsQuery` permite filtrar solo por `candidate_id` sin especificar `workflow_stage_id`
- Asegurar que cuando no se especifica `workflow_stage_id`, retorna **todas** las entrevistas del candidato
- Si no funciona así actualmente, ajustar la query para permitirlo

**Criterios de aceptación**:
- [ ] La query acepta `candidate_id` sin requerir `workflow_stage_id`
- [ ] Retorna todas las entrevistas del candidato de todas las etapas
- [ ] Cada entrevista en el resultado incluye su `workflow_stage_id`

---

### ✅ BACKEND-2: Verificar InterviewRepository
**Archivo**: `src/interview_bc/interview/Infrastructure/repositories/interview_repository.py`

**Descripción**:
- Verificar que `find_by_filters_with_joins()` permite filtrar solo por `candidate_id`
- Asegurar que cuando `workflow_stage_id` no está en los filtros, no se aplica esa restricción
- El repositorio debe retornar todas las entrevistas del candidato

**Criterios de aceptación**:
- [ ] El repositorio puede filtrar solo por `candidate_id`
- [ ] No aplica filtro de `workflow_stage_id` si no se proporciona
- [ ] El método `_to_domain()` mapea correctamente el `workflow_stage_id` de cada entrevista

---

### ✅ BACKEND-3: Verificar InterviewController
**Archivo**: `adapters/http/company_app/interview/controllers/interview_controller.py`

**Descripción**:
- Verificar que `list_interviews()` permite llamar con solo `candidate_id`
- Asegurar que retorna todas las entrevistas con sus respectivos `workflow_stage_id`
- Los DTOs deben incluir la información de la etapa para cada entrevista

**Criterios de aceptación**:
- [ ] El controller acepta `candidate_id` sin requerir `workflow_stage_id`
- [ ] Retorna todas las entrevistas del candidato
- [ ] Cada DTO incluye `workflow_stage_id` y opcionalmente `stage_name`

---

### ✅ BACKEND-4: Verificar InterviewRouter y Endpoint
**Archivo**: `adapters/http/company_app/interview/routers/interview_router.py`

**Descripción**:
- Verificar que el endpoint GET de listado acepta `candidate_id` como query param
- `workflow_stage_id` debe ser opcional en el query string
- Documentar en Swagger/OpenAPI el comportamiento

**Criterios de aceptación**:
- [ ] El endpoint GET acepta `candidate_id` sin requerir `workflow_stage_id`
- [ ] Cuando se omite `workflow_stage_id`, retorna todas las entrevistas
- [ ] La documentación está clara

---

### ✅ BACKEND-5: Obtener Información de Etapas
**Archivo**: Verificar queries existentes

**Descripción**:
- Asegurar que existe una forma de obtener las etapas disponibles de un workflow
- Necesario para el selector de etapas en el modal de asignación
- Probablemente ya existe en `WorkflowStageService` o similar

**Criterios de aceptación**:
- [ ] Existe query/service para obtener etapas de un workflow
- [ ] Retorna información suficiente (id, name, order)
- [ ] El frontend puede consumir esta información

---

## Fase 2: Frontend - Componentes Base

**Objetivo**: Crear los componentes y servicios base para mostrar entrevistas.

### ✅ FRONTEND-1: Crear useCandidateInterviews Hook
**Archivo**: `client-vite/src/hooks/useCandidateInterviews.ts` (nuevo)

**Descripción**:
- Crear custom hook para gestionar entrevistas del candidato
- Cargar **todas las entrevistas** del candidato (sin filtrar por etapa)
- Separar computacionalmente:
  - `currentStageInterviews`: entrevistas donde `workflow_stage_id === currentStageId`
  - `otherStagesInterviews`: entrevistas donde `workflow_stage_id !== currentStageId`
- Función para crear nueva entrevista (con `workflow_stage_id` obligatorio)
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
  const currentStageInterviews = useMemo(() => 
    allInterviews.filter(i => i.workflow_stage_id === currentStageId),
    [allInterviews, currentStageId]
  );
  
  // Computed: entrevistas de otras etapas
  const otherStagesInterviews = useMemo(() =>
    allInterviews.filter(i => i.workflow_stage_id !== currentStageId),
    [allInterviews, currentStageId]
  );

  const loadInterviews = useCallback(async () => {
    // Cargar TODAS las entrevistas del candidato (sin filtro de etapa)
    // GET /api/interviews?candidate_id={candidateId}
  }, [candidateId]);

  const createInterview = useCallback(async (data: CreateInterviewData) => {
    // data.workflow_stage_id es obligatorio
  }, [candidateId]);

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

**Criterios de aceptación**:
- [ ] El hook carga todas las entrevistas del candidato
- [ ] Separa correctamente por etapa actual vs otras
- [ ] La función `createInterview` valida que `workflow_stage_id` esté presente
- [ ] Los estados de loading y error funcionan
- [ ] Se recarga cuando cambian las dependencias

---

### ✅ FRONTEND-2: Crear CandidateInterviewsSection Component
**Archivo**: `client-vite/src/components/candidate/CandidateInterviewsSection.tsx` (nuevo)

**Descripción**:
- Crear componente principal de la sección de entrevistas
- Mostrar dos subsecciones:
  - **"Entrevistas de la Etapa Actual"**: `{stageName}` (si hay)
  - **"Entrevistas de Otras Etapas"**: Expandible/colapsable
- Para cada entrevista mostrar:
  - Nombre de la etapa asociada
  - Tipo de entrevista (TECHNICAL, BEHAVIORAL, etc.)
  - Estado (PENDING, IN_PROGRESS, COMPLETED)
  - Fecha programada (si existe)
  - Participantes/roles requeridos
  - Acciones (ver detalles, editar si aplica)
- Botón "Asignar Entrevista" que abre modal
- Estados de loading y error

**Estructura**:
```typescript
interface CandidateInterviewsSectionProps {
  candidateId: string;
  companyCandidateId: string;
  currentStageId: string | null | undefined;
  currentWorkflowId: string | null | undefined;
  availableStages: WorkflowStage[]; // Para mostrar nombres y para el modal
}

export default function CandidateInterviewsSection({ ... }) {
  const interviewsHook = useCandidateInterviews({ ... });
  const [showAssignModal, setShowAssignModal] = useState(false);
  const [showOtherStages, setShowOtherStages] = useState(false);

  return (
    <div>
      {/* Sección: Entrevistas de la Etapa Actual */}
      <div>
        <h3>Entrevistas de {currentStageName}</h3>
        {interviewsHook.currentStageInterviews.map(interview => (
          <InterviewCard key={interview.id} interview={interview} />
        ))}
      </div>

      {/* Sección: Entrevistas de Otras Etapas (colapsable) */}
      {interviewsHook.otherStagesInterviews.length > 0 && (
        <div>
          <button onClick={() => setShowOtherStages(!showOtherStages)}>
            Otras Etapas ({interviewsHook.otherStagesInterviews.length})
          </button>
          {showOtherStages && interviewsHook.otherStagesInterviews.map(...)}
        </div>
      )}

      {/* Botón para asignar */}
      <button onClick={() => setShowAssignModal(true)}>
        Asignar Entrevista
      </button>

      {/* Modal */}
      <AssignInterviewModal ... />
    </div>
  );
}
```

**Criterios de aceptación**:
- [ ] Muestra correctamente entrevistas de la etapa actual
- [ ] Muestra correctamente entrevistas de otras etapas
- [ ] La sección de "Otras Etapas" es colapsable
- [ ] Cada entrevista muestra toda la información necesaria
- [ ] El botón de asignar abre el modal

---

### ✅ FRONTEND-3: Verificar/Actualizar companyInterviewService
**Archivo**: `client-vite/src/services/companyInterviewService.ts`

**Descripción**:
- Verificar que existe método para listar entrevistas por candidato
- Si no existe, crear `listInterviewsByCandidate(candidateId: string): Promise<Interview[]>`
- El método debe llamar al endpoint sin especificar `workflow_stage_id`
- Asegurar que el tipo `Interview` incluye `workflow_stage_id: string` (obligatorio)
- El método `createInterview()` ya debe tener `workflow_stage_id` como obligatorio

**Criterios de aceptación**:
- [ ] Existe método para listar todas las entrevistas de un candidato
- [ ] El tipo TypeScript refleja `workflow_stage_id` como obligatorio
- [ ] Las llamadas HTTP son correctas
- [ ] Manejo de errores implementado

---

### ✅ FRONTEND-4: Integrar Pestaña en CandidateDetailPage
**Archivo**: `client-vite/src/pages/company/CandidateDetailPage.tsx`

**Descripción**:
- Agregar `'interviews'` al tipo de `activeTab`
- Agregar botón de pestaña "Entrevistas" en la navegación de tabs
- Agregar contenido de la pestaña con `<CandidateInterviewsSection />`
- Pasar props necesarios:
  - `candidateId={candidate.candidate_id}`
  - `companyCandidateId={id}`
  - `currentStageId={candidate.current_stage_id}`
  - `currentWorkflowId={candidate.current_workflow_id}`
  - `availableStages={availableStages}` (ya existe en el componente)
- Agregar traducciones si es necesario

**Criterios de aceptación**:
- [ ] La pestaña "Entrevistas" aparece en el nav de tabs
- [ ] Al hacer clic se muestra el contenido correcto
- [ ] Los datos se cargan correctamente
- [ ] La navegación entre tabs funciona
- [ ] Las traducciones están implementadas

---

## Fase 3: Frontend - Modal de Asignación

**Objetivo**: Crear el modal para asignar nuevas entrevistas.

### ✅ FRONTEND-5: Crear AssignInterviewModal - Estructura Base
**Archivo**: `client-vite/src/components/candidate/AssignInterviewModal.tsx` (nuevo)

**Descripción**:
- Crear modal para asignar nueva entrevista
- Formulario con campos:
  1. **Etapa del workflow** (select, obligatorio, pre-seleccionar etapa actual)
  2. **Tipo de entrevista** (select, obligatorio)
  3. **Plantilla** (select condicional según tipo)
  4. **Roles obligatorios** (multi-select, obligatorio - al menos uno)
  5. **Fecha programada** (date picker, opcional)
  6. **Participantes** (multi-select usuarios, opcional)
- Botones: "Cancelar" y "Asignar Entrevista"

**Estructura**:
```typescript
interface AssignInterviewModalProps {
  candidateId: string;
  companyCandidateId: string;
  currentStageId: string | null | undefined;
  currentWorkflowId: string | null | undefined;
  availableStages: WorkflowStage[];
  jobPositionId?: string;
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

export default function AssignInterviewModal({ ... }) {
  const [workflowStageId, setWorkflowStageId] = useState<string>(
    currentStageId || (availableStages[0]?.id || '')
  );
  const [interviewType, setInterviewType] = useState<string>('');
  const [templateId, setTemplateId] = useState<string | null>(null);
  const [requiredRoles, setRequiredRoles] = useState<string[]>([]);
  const [scheduledAt, setScheduledAt] = useState<Date | null>(null);
  const [participants, setParticipants] = useState<string[]>([]);

  // ... state para loading, errors, listas de opciones, etc.

  return (
    <Modal isOpen={isOpen} onClose={onClose} size="large">
      <form onSubmit={handleSubmit}>
        {/* Campos del formulario */}
      </form>
    </Modal>
  );
}
```

**Criterios de aceptación**:
- [ ] El modal se abre y cierra correctamente
- [ ] El formulario tiene todos los campos necesarios
- [ ] El diseño es consistente con la app
- [ ] Los botones funcionan

---

### ✅ FRONTEND-6: Implementar Selector de Etapa + Tipos de Entrevista
**Tarea**: Campos básicos del formulario

**Descripción**:
1. **Selector de Etapa**:
   - Usar `availableStages` (pasado como prop)
   - Pre-seleccionar etapa actual si existe
   - Campo obligatorio
   
2. **Selector de Tipo de Entrevista**:
   - Usar enum `InterviewTypeEnum`:
     - `EXTENDED_PROFILE`
     - `POSITION_INTERVIEW`
     - `TECHNICAL`
     - `BEHAVIORAL`
     - `CULTURAL_FIT`
   - Mostrar con traducciones
   - Al seleccionar, disparar carga de plantillas
   - Campo obligatorio

**Criterios de aceptación**:
- [ ] El selector de etapa muestra todas las etapas disponibles
- [ ] Pre-selecciona la etapa actual correctamente
- [ ] El selector de tipo muestra todos los tipos con traducciones
- [ ] Al seleccionar tipo, se dispara carga de plantillas
- [ ] Ambos campos marcan como obligatorios

---

### ✅ FRONTEND-7: Implementar Carga de Plantillas por Tipo
**Servicio**: `companyInterviewTemplateService.listTemplates()`

**Descripción**:
- Al seleccionar tipo de entrevista, cargar plantillas de ese tipo
- Filtrar plantillas por `interview_type` o `template_type`
- **Si hay 0 plantillas**: Permitir crear sin plantilla (templateId = null)
- **Si hay 1 plantilla**: Auto-seleccionarla y ocultarselector o mostrarlo deshabilitado
- **Si hay 2+ plantillas**: Mostrar selector obligatorio
- Mostrar loading mientras se cargan
- Manejar errores de carga

**Criterios de aceptación**:
- [ ] Las plantillas se cargan al seleccionar tipo
- [ ] La lógica de 0/1/2+ plantillas funciona correctamente
- [ ] El selector se muestra/oculta según corresponda
- [ ] Los estados de loading y error se muestran

---

### ✅ FRONTEND-8: Implementar Selector de Roles Obligatorios
**Servicio**: Servicio de roles de la empresa (CompanyRoleService)

**Descripción**:
- Cargar lista de roles disponibles en la empresa
- Mostrar multi-select para seleccionar roles obligatorios
- **Este campo es OBLIGATORIO** (debe haber al menos un rol seleccionado)
- Si la plantilla seleccionada tiene `required_roles`, pre-seleccionarlos
- Validar que no esté vacío antes de enviar
- Mostrar error visible si se intenta enviar sin roles

**Criterios de aceptación**:
- [ ] La lista de roles se carga correctamente
- [ ] El multi-select funciona bien
- [ ] Los roles de la plantilla se pre-seleccionan
- [ ] Validación de al menos un rol funciona
- [ ] Error visible si está vacío al enviar

---

### ✅ FRONTEND-9: Implementar Selectores Opcionales (Fecha + Participantes)
**Servicios**: Date picker + CompanyUserService

**Descripción**:
1. **Fecha Programada** (opcional):
   - Implementar date picker
   - Validar que si se especifica, sea fecha futura
   - Permitir dejar vacío

2. **Participantes** (opcional):
   - Cargar lista de usuarios de la empresa
   - Mostrar multi-select
   - Mostrar nombre y rol de cada usuario
   - Permitir búsqueda/filtrado si hay muchos
   - Permitir dejar vacío

**Criterios de aceptación**:
- [ ] El date picker funciona correctamente
- [ ] Validación de fecha futura funciona
- [ ] La lista de usuarios se carga
- [ ] El multi-select de participantes funciona
- [ ] La búsqueda/filtrado funciona (si aplica)
- [ ] Ambos campos son opcionales

---

### ✅ FRONTEND-10: Implementar Validaciones y Envío
**Descripción**:
- **Validar campos obligatorios**:
  - `workflow_stage_id` (etapa)
  - `interview_type` (tipo)
  - `required_roles` (al menos uno)
  - `template_id` (si hay 2+ plantillas disponibles)
- **Validar campos opcionales**:
  - `scheduled_at` (si se especifica, debe ser futura)
- **Mostrar errores** de validación en cada campo
- **Deshabilitar botón "Asignar"** si hay errores
- **Enviar formulario**:
  - Llamar a `companyInterviewService.createInterview()`
  - Mostrar loading durante el envío
  - Manejar errores de API
  - Llamar a `onSuccess()` si es exitoso
  - Cerrar modal
- **Limpiar formulario** al cerrar

**Criterios de aceptación**:
- [ ] Todas las validaciones funcionan
- [ ] Los mensajes de error son claros
- [ ] El botón se deshabilita apropiadamente
- [ ] El envío funciona correctamente
- [ ] Los errores de API se muestran al usuario
- [ ] El modal se cierra tras éxito
- [ ] El formulario se limpia

---

## Fase 4: Testing y Ajustes

**Objetivo**: Probar toda la funcionalidad y realizar ajustes finales.

### ✅ TEST-1: Testing de Creación en Diferentes Etapas
**Descripción**:
- Crear entrevista en la etapa actual del candidato
- Crear entrevista en una etapa diferente (pasada o futura)
- Verificar que ambas aparecen en las secciones correctas
- Verificar datos en base de datos (`workflow_stage_id` correcto)
- Probar con diferentes tipos de entrevista
- Probar con y sin plantilla
- Probar con y sin participantes

**Criterios de aceptación**:
- [ ] Las entrevistas se crean en cualquier etapa
- [ ] Aparecen en la sección correcta según su etapa
- [ ] Los datos en BD son correctos
- [ ] Funciona con todas las variaciones de campos

---

### ✅ TEST-2: Testing de Listado y Separación por Etapas
**Descripción**:
- Crear varias entrevistas en diferentes etapas
- Verificar que todas aparecen en la pestaña
- Verificar separación correcta: etapa actual vs otras
- Cambiar candidato de etapa y verificar que la separación se actualiza
- Verificar que entrevistas de etapas pasadas siguen visibles
- Probar expand/collapse de "Otras Etapas"
- Verificar performance con muchas entrevistas (10+)

**Criterios de aceptación**:
- [ ] Todas las entrevistas se listan correctamente
- [ ] La separación por etapas funciona
- [ ] Al cambiar de etapa, la vista se actualiza
- [ ] Las entrevistas históricas son visibles
- [ ] El collapse/expand funciona
- [ ] La performance es aceptable

---

### ✅ TEST-3: Testing de Cambios de Etapa del Candidato
**Descripción**:
- Crear entrevistas en la etapa actual
- Mover candidato a otra etapa (usando botones de la página)
- Verificar que las entrevistas anteriores ahora aparecen en "Otras Etapas"
- La nueva etapa actual debe mostrar sus propias entrevistas (si las hay)
- Verificar que no hay errores de carga
- Verificar que el refresh funciona correctamente

**Criterios de aceptación**:
- [ ] Las entrevistas se reclasifican al cambiar de etapa
- [ ] No hay errores en la UI
- [ ] El refresh de datos funciona
- [ ] La experiencia es fluida

---

### ✅ TEST-4: Testing UI/UX y Ajustes Finales
**Descripción**:
- Revisar diseño visual de la pestaña
- Revisar diseño del modal de asignación
- Verificar textos y traducciones (es/en)
- Verificar comportamiento responsive (desktop/tablet/mobile)
- Ajustar colores e iconos según feedback
- Mejorar mensajes de error si es necesario
- Agregar tooltips o ayuda contextual si hace falta
- Verificar accesibilidad (a11y)

**Criterios de aceptación**:
- [ ] El diseño es consistente con el resto de la app
- [ ] Las traducciones están completas y correctas
- [ ] Es responsive en diferentes pantallas
- [ ] Los iconos y colores son apropiados
- [ ] Los mensajes de error son claros
- [ ] La experiencia de usuario es intuitiva
- [ ] Cumple con estándares de accesibilidad

---

## Preguntas Pendientes de Resolución

1. ✅ **ACLARADO**: No hay entrevistas globales, `workflow_stage_id` es obligatorio

2. **¿De dónde vienen los roles obligatorios?**
   - ¿De la plantilla seleccionada (`template.required_roles`)?
   - ¿El usuario los selecciona manualmente siempre?
   - ¿Hay roles por defecto según el tipo de entrevista?

3. **¿Los participantes deben ser usuarios de la empresa o pueden ser externos?**
   - Actualmente `interviewers` es una lista de nombres (strings)
   - ¿Deberíamos cambiarlo a IDs de usuarios para mejor integración?
   - ¿O mantener la flexibilidad de nombres libres?

4. **¿Qué acciones debe tener cada entrevista en la lista?**
   - ¿Ver detalles (navegar a página de entrevista)?
   - ¿Editar datos de la entrevista?
   - ¿Cambiar estado (iniciar, completar, cancelar)?
   - ¿Eliminar/cancelar entrevista?

5. **¿Se pueden editar entrevistas desde esta vista o solo crear?**
   - Si se pueden editar, ¿se abre un modal similar?
   - ¿O se navega a otra página?

6. **¿Se pueden reasignar entrevistas a otra etapa?**
   - ¿O una vez creada, su etapa es fija?

---

## Notas Técnicas

- ✅ El campo `workflow_stage_id` es y seguirá siendo **OBLIGATORIO**
- ✅ **NO** se requiere migración de base de datos
- ✅ Todas las entrevistas deben estar asociadas a una etapa específica
- El campo `required_roles` es obligatorio (al menos un rol)
- El campo `interviewers` en backend es lista de nombres (strings), no IDs
- Las queries deben obtener **todas** las entrevistas del candidato para mostrarlas agrupadas
- La separación "etapa actual vs otras" es solo visual, hecha en el frontend
- Considerar agregar índice en `candidate_id` en la tabla `interviews` si no existe

---

## Dependencias entre Tareas

```
BACKEND-1 (Verify Query) → BACKEND-2 (Verify Repo)
                            ↓
BACKEND-3 (Verify Controller) → BACKEND-4 (Verify Router)
                            ↓
BACKEND-5 (Get Stages)
                            ↓
FRONTEND-1 (Hook) → FRONTEND-2 (Section) → FRONTEND-4 (Integrate)
    ↑                      ↑
FRONTEND-3 (Service)      |
                          ↓
FRONTEND-5 (Modal Base) → FRONTEND-6 (Stage + Type)
                          ↓
FRONTEND-7 (Templates) → FRONTEND-8 (Roles) → FRONTEND-9 (Optional Fields)
                          ↓
FRONTEND-10 (Validations + Submit)
                          ↓
TEST-1, TEST-2, TEST-3, TEST-4 (Testing)
```

---

## Estimación de Tiempo

| Fase | Tareas | Tiempo Estimado |
|------|--------|----------------|
| Fase 1 - Backend | 5 tareas (verificación) | 2-3 horas |
| Fase 2 - Frontend Base | 4 tareas | 3-4 horas |
| Fase 3 - Frontend Modal | 6 tareas | 4-5 horas |
| Fase 4 - Testing | 4 tareas | 2-3 horas |
| **TOTAL** | **19 tareas** | **11-15 horas** |

---

## Estado del Proyecto

- [ ] Fase 1 completada
- [ ] Fase 2 completada
- [ ] Fase 3 completada
- [ ] Fase 4 completada

**Fecha de inicio**: _Pendiente_  
**Fecha de finalización**: _Pendiente_

---

## Diferencias con Versión Anterior

**Cambios realizados tras aclaración**:

1. ❌ **Eliminado**: Hacer `workflow_stage_id` opcional en entidad/modelo/migración
2. ❌ **Eliminado**: Agregar parámetro `include_global` en queries
3. ❌ **Eliminado**: Lógica para entrevistas "globales" (sin etapa)
4. ✅ **Mantenido**: `workflow_stage_id` es **obligatorio** en toda la entidad
5. ✅ **Agregado**: Selector de etapa en el modal (pre-seleccionar etapa actual)
6. ✅ **Modificado**: Hook separa entrevistas por etapa en el frontend (no en backend)
7. ✅ **Simplificado**: Backend solo necesita verificación, no cambios estructurales

**Reducción**: De 24 tareas a 19 tareas (5 tareas eliminadas)  
**Tiempo**: De 13-18 horas a 11-15 horas

---

## Referencias

- [Requisito completo](requisito-pestaña-entrevistas-candidato.md)
- Entidad Interview: `src/interview_bc/interview/domain/entities/interview.py`
- Repositorio: `src/interview_bc/interview/Infrastructure/repositories/interview_repository.py`
- Controller: `adapters/http/company_app/interview/controllers/interview_controller.py`
- Frontend Page: `client-vite/src/pages/company/CandidateDetailPage.tsx`
