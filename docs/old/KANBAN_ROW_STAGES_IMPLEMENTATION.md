# Kanban Row Stages Implementation

## Objetivo
Implementar la funcionalidad para mostrar algunos estados del Kanban como filas debajo del tablero en lugar de columnas, con configuración flexible por stage.

## Especificaciones 


### Comportamiento
- **Configuración**: Cada stage puede configurarse como `column`, `row`, o `none`
- **Display**: Stages en modo `row` se muestran como filas debajo del Kanban
- **Contenido**: En las filas solo se muestra el nombre del candidato
- **Drag & Drop**: Funciona entre columnas y filas
- **Visibilidad**: Las filas están siempre visibles

### Configuración por defecto
- `INITIAL`, `STANDARD`: `column`
- `FAIL`: `row` 
- `SUCCESS`: `column`
- `NONE`: `none`

## Tareas de Implementación

### Fase 1: Backend - Base de Datos y Modelos

#### 1.1 Migración de Base de Datos
- [x] Crear migración para agregar columna `kanban_display` a `workflow_stages`
  - Tipo: `VARCHAR(10)`
  - Default: `'column'`
  - Constraint: `CHECK (kanban_display IN ('column', 'row', 'none'))`
  - Ejecutar: `make revision m="add kanban_display to workflow_stages"`
  - Ejecutar: `make migrate`

#### 1.2 Modelo SQLAlchemy
- [x] Actualizar `WorkflowStageModel` en `src/company_workflow/infrastructure/models/workflow_stage_model.py`
  - Agregar campo `kanban_display`
  - Configurar constraint y default

#### 1.3 Enum TypeScript
- [x] Crear enum `KanbanDisplay` en `client-vite/src/types/workflow.ts`
  ```typescript
  enum KanbanDisplay {
    COLUMN = 'column',
    ROW = 'row', 
    NONE = 'none'
  }
  ```

#### 1.4 Tipo WorkflowStage
- [x] Actualizar interface `WorkflowStage` en `client-vite/src/types/workflow.ts`
  - Agregar campo `kanban_display: KanbanDisplay`

### Fase 2: Frontend - Componentes Base

#### 2.1 Componente RowStageSection
- [x] Crear `client-vite/src/components/kanban/RowStageSection.tsx`
  - Props: `stage: WorkflowStage`, `candidates: CompanyCandidate[]`
  - Renderiza header del stage y lista de candidatos
  - Maneja drag and drop para la zona de drop

#### 2.2 Componente CandidateNameRow
- [x] Crear `client-vite/src/components/kanban/CandidateNameRow.tsx`
  - Props: `candidate: CompanyCandidate`, `onClick?: () => void`
  - Renderiza solo el nombre del candidato
  - Implementa drag and drop
  - Estilos: inline-block, hover effects

#### 2.3 Estilos CSS
- [x] Crear `client-vite/src/components/kanban/kanban-styles.css`
  - Estilos para `.row-stage-section`
  - Estilos para `.candidate-name-row`
  - Hover effects y transiciones

### Fase 3: Frontend - Integración en Kanban

#### 3.1 Modificar WorkflowBoardPage
- [x] Actualizar `client-vite/src/pages/company/WorkflowBoardPage.tsx`
  - Separar stages por `kanban_display`:
    ```typescript
    const columnStages = stages.filter(s => s.kanban_display === 'column');
    const rowStages = stages.filter(s => s.kanban_display === 'row');
    ```
  - Renderizar columnas y filas por separado
  - Importar nuevos componentes

#### 3.2 Layout del Kanban
- [x] Estructurar el layout:
  ```
  ┌─────────────────────────────────────────┐
  │  Header (Workflow Board)              │
  ├─────────────────────────────────────────┤
  │  [Column Stage 1] [Column Stage 2] ... │
  │  (CandidateCard completo)              │
  ├─────────────────────────────────────────┤
  │  Row Stages Section:                   │
  │  ┌─────────────────────────────────┐  │
  │  │ Stage Name                      │  │
  │  │ • Name 1  • Name 2  • Name 3   │  │
  │  └─────────────────────────────────┘  │
  └─────────────────────────────────────────┘
  ```

#### 3.3 Drag and Drop
- [x] Actualizar lógica de drag and drop
  - Manejar drops en zonas de fila
  - Mantener funcionalidad existente para columnas
  - Actualizar `handleDragEnd` para detectar tipo de zona

### Fase 4: Configuración (Opcional para MVP)

#### 4.1 Interface de Configuración
- [ ] Crear página de configuración de stages
  - Dropdown por cada stage: Column/Row/None
  - Guardar configuración en base de datos
  - Validación: al menos una columna debe existir

#### 4.2 Endpoint de Configuración
- [ ] Crear endpoint para actualizar `kanban_display`
  - `PUT /api/workflow-stages/{stage_id}/kanban-display`
  - Validación de configuración
  - Actualizar en base de datos

### Fase 5: Testing y Refinamiento

#### 5.1 Testing
- [ ] Probar drag and drop entre columnas y filas
- [ ] Probar con diferentes configuraciones de stages
- [ ] Probar responsividad en móviles
- [ ] Probar con muchos candidatos en filas

#### 5.2 Refinamiento
- [ ] Ajustar estilos para mejor UX
- [ ] Optimizar rendimiento con muchos candidatos
- [ ] Añadir animaciones de transición
- [ ] Mejorar accesibilidad

## Archivos a Modificar

### Backend
- `alembic/versions/XXX_add_kanban_display_to_workflow_stages.py` (nuevo)
- `src/company_workflow/infrastructure/models/workflow_stage_model.py`
- `src/company_workflow/presentation/schemas/workflow_stage_response.py`

### Frontend
- `client-vite/src/types/workflow.ts`
- `client-vite/src/pages/company/WorkflowBoardPage.tsx`
- `client-vite/src/components/kanban/RowStageSection.tsx` (nuevo)
- `client-vite/src/components/kanban/CandidateNameRow.tsx` (nuevo)
- `client-vite/src/components/kanban/kanban-styles.css` (nuevo)

## Consideraciones Técnicas

### Performance
- Las filas siempre visibles pueden impactar rendimiento con muchos candidatos
- Considerar virtualización si hay >100 candidatos por fila

### UX
- Hover en nombres de candidatos para mostrar info básica
- Click en nombre para ver detalles completos
- Indicadores visuales claros de zonas de drop

### Responsividad
- En móviles, las filas pueden ocupar mucho espacio
- Considerar scroll horizontal o colapsar filas

## Criterios de Aceptación

- [x] Stages configurados como `row` se muestran como filas debajo del Kanban
- [x] Solo se muestra el nombre del candidato en las filas
- [x] Drag and drop funciona entre columnas y filas
- [x] La configuración se persiste en base de datos
- [x] El diseño es responsive
- [x] No hay regresiones en funcionalidad existente

## Estimación de Tiempo

- **Fase 1 (Backend)**: 2-3 horas
- **Fase 2 (Componentes)**: 3-4 horas  
- **Fase 3 (Integración)**: 4-5 horas
- **Fase 4 (Configuración)**: 2-3 horas
- **Fase 5 (Testing)**: 2-3 horas

**Total estimado**: 13-18 horas
