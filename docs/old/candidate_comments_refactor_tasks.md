# Candidate Comments & Reviews Refactor Tasks

## Objetivo
Refactorizar el sistema de comentarios de candidatos y agregar un nuevo sistema de reviews con puntuación.

## Fase 1: Eliminación de Pestaña "Notas"

### Backend
- [ ] Eliminar endpoints relacionados con "notas" (internal_notes) si existen
- [ ] Quitar `internal_notes` en `CompanyCandidate`
- [ ] Asegurar que los comentarios sigan funcionando correctamente

### Frontend
- [ ] Eliminar la pestaña "notas" del componente `CandidateDetailPage.tsx`
- [ ] Eliminar el estado `isEditingNotes`, `notesText`, `savingNotes` y funciones relacionadas
- [ ] Eliminar la sección "Internal Notes Section" del render
- [ ] Actualizar las pestañas para que solo muestren: Información, Documentos, Historia

## Fase 2: Reubicación de Comentarios a Pestaña "Información"

### Frontend
- [ ] Mover el componente de comentarios que hay debajo del card de "información", y convertirlo en una pestaña que estará junto a información. Mismo nivel de jerarquia visual.
- [ ] Asegurar que se pueden agregar comentarios en el carda de abajo.
- [ ] Mantener el contador de comentarios pendientes en el header si es necesario
- [ ] Mostrar junto al card de añadir comentarios, el total que hay y un link a la pestaña. Si hay 0 no poner.

## Fase 3: Refactorización de Comentarios con 3 Pestañas

### Frontend - Componente de Comentarios
- [ ] Actualizar `CandidateCommentsSection` para tener 3 pestañas:
  - **Etapa Actual**: Filtra comentarios por `stage_id` actual
  - **Globales**: Muestra comentarios que no pertenecen a ninguna etapa específica (`stage_id` es null o diferente)
  - **Todos**: Muestra todos los comentarios sin filtro
- [ ] Implementar lógica de filtrado en cada pestaña
- [ ] Actualizar el servicio `candidateCommentService` si es necesario para soportar estos filtros

### Backend (si es necesario)
- [ ] Verificar que los endpoints de comentarios soporten filtrado por etapa
- [ ] Agregar endpoint para obtener comentarios globales si no existe
- [ ] Agregar endpoint para obtener todos los comentarios si no existe

## Fase 4: Formulario de Comentarios Debajo del Card

### Frontend
- [ ] Modificar `CandidateCommentsSection` para que:
  - El formulario de agregar comentario esté siempre visible debajo del card
  - NO muestre la lista de comentarios anteriores en la vista principal
  - Muestre solo un contador de comentarios (ej: "5 comentarios")
  - Al hacer clic en el contador o en un botón "Ver comentarios", mostrar la lista completa con las 3 pestañas
- [ ] Crear un estado colapsable/expandible para la lista de comentarios
- [ ] Mantener el formulario siempre visible para facilitar la adición rápida

## Fase 5: Nueva Entidad CandidateReview

### Backend - Domain Layer

#### 5.1 Enums
- [ ] Crear `src/candidate_review/domain/enums/review_status_enum.py`:
  - `ReviewStatusEnum` con valores: `PENDING`, `REVIEWED`
- [ ] Crear `src/candidate_review/domain/enums/review_score_enum.py`:
  - `ReviewScoreEnum` con valores: `ZERO`, `THREE`, `SIX`, `TEN`
  - Valores numéricos: 0, 3, 6, 10

#### 5.2 Value Objects
- [ ] Crear `src/candidate_review/domain/value_objects/candidate_review_id.py`:
  - `CandidateReviewId(BaseId)`

#### 5.3 Entidades
- [ ] Crear `src/candidate_review/domain/entities/candidate_review.py`:
  - Campos:
    - `id: CandidateReviewId`
    - `company_candidate_id: CompanyCandidateId`
    - `score: ReviewScoreEnum` (0, 3, 6, 10)
    - `comment: str | None` (opcional)
    - `workflow_id: WorkflowId | None`
    - `stage_id: WorkflowStageId | None`
    - `review_status: ReviewStatusEnum`
    - `created_by_user_id: UserId`
    - `created_at: datetime`
    - `updated_at: datetime`
  - Métodos:
    - `create()`: Factory method
    - `update()`: Actualizar score y comment
    - `mark_as_reviewed()`: Cambiar status a REVIEWED
    - `mark_as_pending()`: Cambiar status a PENDING

### Backend - Infrastructure Layer

#### 5.4 Repository Interface
- [ ] Crear `src/candidate_review/domain/infrastructure/candidate_review_repository_interface.py`:
  - Métodos:
    - `get_by_id(review_id: CandidateReviewId) -> CandidateReview | None`
    - `get_by_company_candidate(company_candidate_id: CompanyCandidateId) -> List[CandidateReview]`
    - `get_by_stage(company_candidate_id: CompanyCandidateId, stage_id: WorkflowStageId) -> List[CandidateReview]`
    - `get_global_reviews(company_candidate_id: CompanyCandidateId) -> List[CandidateReview]`
    - `create(review: CandidateReview) -> None`
    - `update(review: CandidateReview) -> None`
    - `delete(review_id: CandidateReviewId) -> None`

#### 5.5 Modelo SQLAlchemy
- [ ] Crear `src/candidate_review/infrastructure/models/candidate_review_model.py`:
  - Tabla: `candidate_reviews`
  - Columnas:
    - `id` (String, PK)
    - `company_candidate_id` (String, FK a `company_candidates`)
    - `score` (Integer, 0, 3, 6, 10)
    - `comment` (Text, nullable)
    - `workflow_id` (String, nullable, FK a `workflows`)
    - `stage_id` (String, nullable, FK a `workflow_stages`)
    - `review_status` (String, enum)
    - `created_by_user_id` (String, FK a `users`)
    - `created_at` (DateTime)
    - `updated_at` (DateTime)
  - Índices:
    - `idx_candidate_review_company_candidate`
    - `idx_candidate_review_stage`
    - `idx_candidate_review_status`

#### 5.6 Repositorio
- [ ] Crear `src/candidate_review/infrastructure/repositories/candidate_review_repository.py`:
  - Implementar `CandidateReviewRepositoryInterface`
  - Métodos `_to_domain()` y `_to_model()`

#### 5.7 Migración
- [ ] Crear migración Alembic: `make revision m="add candidate_reviews table"`
- [ ] Revisar y ajustar la migración generada
- [ ] Ejecutar migración: `make migrate`

### Backend - Application Layer

#### 5.8 Commands
- [ ] Crear `src/candidate_review/application/commands/create_candidate_review_command.py`:
  - `CreateCandidateReviewCommand`:
    - `company_candidate_id: CompanyCandidateId`
    - `score: ReviewScoreEnum`
    - `comment: str | None`
    - `workflow_id: WorkflowId | None`
    - `stage_id: WorkflowStageId | None`
  - `CreateCandidateReviewCommandHandler`: Crea la review

- [ ] Crear `src/candidate_review/application/commands/update_candidate_review_command.py`:
  - `UpdateCandidateReviewCommand`:
    - `review_id: CandidateReviewId`
    - `score: ReviewScoreEnum | None`
    - `comment: str | None`
  - `UpdateCandidateReviewCommandHandler`: Actualiza la review

- [ ] Crear `src/candidate_review/application/commands/delete_candidate_review_command.py`:
  - `DeleteCandidateReviewCommand`:
    - `review_id: CandidateReviewId`
  - `DeleteCandidateReviewCommandHandler`: Elimina la review

- [ ] Crear `src/candidate_review/application/commands/mark_review_as_reviewed_command.py`:
  - `MarkReviewAsReviewedCommand`:
    - `review_id: CandidateReviewId`
  - `MarkReviewAsReviewedCommandHandler`: Marca como revisado

- [ ] Crear `src/candidate_review/application/commands/mark_review_as_pending_command.py`:
  - `MarkReviewAsPendingCommand`:
    - `review_id: CandidateReviewId`
  - `MarkReviewAsPendingCommandHandler`: Marca como pendiente

#### 5.9 Queries
- [ ] Crear `src/candidate_review/application/queries/get_review_by_id_query.py`:
  - `GetReviewByIdQuery`
  - `GetReviewByIdQueryHandler`: Retorna `CandidateReviewDto`

- [ ] Crear `src/candidate_review/application/queries/list_reviews_by_company_candidate_query.py`:
  - `ListReviewsByCompanyCandidateQuery`
  - `ListReviewsByCompanyCandidateQueryHandler`: Retorna `List[CandidateReviewDto]`

- [ ] Crear `src/candidate_review/application/queries/list_reviews_by_stage_query.py`:
  - `ListReviewsByStageQuery`
  - `ListReviewsByStageQueryHandler`: Retorna `List[CandidateReviewDto]`

- [ ] Crear `src/candidate_review/application/queries/list_global_reviews_query.py`:
  - `ListGlobalReviewsQuery`
  - `ListGlobalReviewsQueryHandler`: Retorna `List[CandidateReviewDto]`

#### 5.10 DTOs
- [ ] Crear `src/candidate_review/application/dtos/candidate_review_dto.py`:
  - `CandidateReviewDto`:
    - Todos los campos de la entidad
    - Campos expandidos opcionales: `created_by_user_name`, `workflow_name`, `stage_name`
  - Método `from_entity()`

### Backend - Presentation Layer

#### 5.11 Schemas
- [ ] Crear `src/candidate_review/presentation/schemas/create_review_request.py`:
  - `CreateCandidateReviewRequest` (Pydantic)

- [ ] Crear `src/candidate_review/presentation/schemas/update_review_request.py`:
  - `UpdateCandidateReviewRequest` (Pydantic)

- [ ] Crear `src/candidate_review/presentation/schemas/review_response.py`:
  - `CandidateReviewResponse` (Pydantic)

- [ ] Crear `src/candidate_review/presentation/schemas/review_list_response.py`:
  - `CandidateReviewListResponse` (Pydantic)

#### 5.12 Controllers
- [ ] Crear `src/candidate_review/presentation/controllers/candidate_review_controller.py`:
  - Métodos:
    - `create_review()`
    - `update_review()`
    - `delete_review()`
    - `get_review_by_id()`
    - `list_reviews_by_company_candidate()`
    - `list_reviews_by_stage()`
    - `list_global_reviews()`
    - `mark_as_reviewed()`
    - `mark_as_pending()`

#### 5.13 Routers
- [ ] Crear `adapters/http/company/routers/candidate_review_router.py`:
  - Endpoints:
    - `POST /api/company/candidates/{candidate_id}/reviews`
    - `PUT /api/company/candidates/reviews/{review_id}`
    - `DELETE /api/company/candidates/reviews/{review_id}`
    - `GET /api/company/candidates/reviews/{review_id}`
    - `GET /api/company/candidates/{candidate_id}/reviews`
    - `GET /api/company/candidates/{candidate_id}/reviews/stage/{stage_id}`
    - `GET /api/company/candidates/{candidate_id}/reviews/global`
    - `POST /api/company/candidates/reviews/{review_id}/mark-reviewed`
    - `POST /api/company/candidates/reviews/{review_id}/mark-pending`

#### 5.14 Container
- [ ] Registrar en `core/container.py`:
  - Repository
  - Command handlers
  - Query handlers
  - Controller

## Fase 6: Frontend - CandidateReview

### 6.1 Types
- [ ] Crear `client-vite/src/types/candidateReview.ts`:
  - `ReviewScore`: 0 | 3 | 6 | 10
  - `ReviewStatus`: 'pending' | 'reviewed'
  - `CandidateReview` interface
  - `CreateCandidateReviewRequest` interface
  - `UpdateCandidateReviewRequest` interface

### 6.2 Service
- [ ] Crear `client-vite/src/services/candidateReviewService.ts`:
  - Métodos:
    - `createReview()`
    - `updateReview()`
    - `deleteReview()`
    - `getReviewById()`
    - `getReviewsByCompanyCandidate()`
    - `getReviewsByStage()`
    - `getGlobalReviews()`
    - `markAsReviewed()`
    - `markAsPending()`

### 6.3 Componentes
- [ ] Crear `client-vite/src/components/candidate/CandidateReviewForm.tsx`:
  - Formulario con botones de puntuación:
    - 0: Icono de ban (prohibido) - `Ban` de lucide-react
    - 3: Mano abajo - `ThumbsDown` de lucide-react
    - 6: Mano arriba - `ThumbsUp` de lucide-react
    - 10: Favorito - `Star` o `Heart` de lucide-react
  - Campo opcional de comentario (textarea)
  - Checkbox para "Marcar como revisado"
  - Botón submit

- [ ] Crear `client-vite/src/components/candidate/CandidateReviewsList.tsx`:
  - Lista de reviews con:
    - Icono de puntuación
    - Comentario (si existe)
    - Fecha y autor
    - Badge de status (pending/reviewed)
    - Acciones: toggle status, eliminar

- [ ] Crear `client-vite/src/components/candidate/CandidateReviewsSection.tsx`:
  - Componente contenedor que combina form y list
  - Similar a `CandidateCommentsSection` pero para reviews
  - 3 pestañas: Etapa Actual, Globales, Todos

### 6.4 Integración en CandidateDetailPage
- [ ] Agregar sección de reviews en la pestaña "Información"
- [ ] Posicionar debajo de los comentarios
- [ ] Mantener el mismo patrón: formulario visible, lista colapsable con contador

## Fase 7: Testing

### Backend
- [ ] Tests unitarios de entidad `CandidateReview`
- [ ] Tests de repositorio
- [ ] Tests de comandos y queries
- [ ] Tests de endpoints

### Frontend
- [ ] Tests de componentes de review
- [ ] Tests de integración con la página de detalle

## Notas de Implementación

### Iconos para Puntuación
- **0 puntos**: `Ban` (lucide-react) - Color rojo
- **3 puntos**: `ThumbsDown` (lucide-react) - Color naranja/amarillo
- **6 puntos**: `ThumbsUp` (lucide-react) - Color azul
- **10 puntos**: `Star` o `Heart` (lucide-react) - Color dorado/verde

### Comportamiento del Formulario de Comentarios
- El formulario está siempre visible debajo del card principal
- Muestra un contador: "X comentarios" (clickeable)
- Al hacer clic, se expande la lista completa con las 3 pestañas
- El formulario permanece visible incluso cuando la lista está expandida

### Comportamiento del Formulario de Reviews
- Similar al de comentarios
- Botones de puntuación grandes y visibles
- Campo de comentario opcional
- Checkbox para marcar como revisado al crear

