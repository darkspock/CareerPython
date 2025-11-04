# Stage Style Implementation Plan

## Objetivo
Agregar un atributo `style` a nivel de `WorkflowStage` que permita personalizar la apariencia visual de cada stage en el Kanban board y otras interfaces.

## Value Object: StageStyle

### Propiedades
- **icon**: `str` - Puede ser emoji, HTML icon, o SVG HTML embebido
- **color**: `str` - Color del texto (hex, rgb, o nombre de color CSS)
- **background_color**: `str` - Color de fondo (hex, rgb, o nombre de color CSS)

## Tareas de Implementación

### Fase 1: Domain Layer - Value Object y Entidad

#### 1.1 Crear Value Object StageStyle
- [x] Crear `src/company_workflow/domain/value_objects/stage_style.py`
  - Clase `StageStyle` con validaciones
  - Métodos de validación para colores
  - Método `create()` con valores por defecto
  - Método `update()` para modificar estilos

#### 1.2 Actualizar Entidad WorkflowStage
- [x] Modificar `src/company_workflow/domain/entities/workflow_stage.py`
  - Agregar campo `style: StageStyle`
  - Actualizar método `create()` para incluir `style`
  - Actualizar método `update()` para incluir `style`
  - Actualizar todos los métodos que crean instancias (reorder, activate, deactivate, etc.)

### Fase 2: Infrastructure Layer - Base de Datos

#### 2.1 Migración de Base de Datos
- [x] Crear migración para agregar columna `style` a `workflow_stages`
  - Tipo: `JSON`
  - Estructura: `{"icon": "string", "color": "string", "background_color": "string"}`
  - Ejecutar: `make revision m="add style to workflow_stages"`
  - Ejecutar: `make migrate`

#### 2.2 Modelo SQLAlchemy
- [x] Actualizar `src/company_workflow/infrastructure/models/workflow_stage_model.py`
  - Agregar campo `style: Mapped[dict | None] = mapped_column(JSON)`
  - Configurar serialización/deserialización

#### 2.3 Repositorio
- [x] Actualizar `src/company_workflow/infrastructure/repositories/workflow_stage_repository.py`
  - Método `_to_domain()`: convertir JSON a `StageStyle`
  - Método `_to_model()`: convertir `StageStyle` a JSON

### Fase 3: Application Layer - DTOs y Mappers

#### 3.1 DTO
- [x] Actualizar `src/company_workflow/application/dtos/workflow_stage_dto.py`
  - Agregar campo `style: dict`

#### 3.2 Mappers
- [x] Actualizar `src/company_workflow/application/mappers/workflow_stage_mapper.py`
  - `entity_to_dto()`: convertir `StageStyle` a dict
  - `dto_to_entity()`: convertir dict a `StageStyle`

### Fase 4: Presentation Layer - API

#### 4.1 Response Schema
- [x] Actualizar `src/company_workflow/presentation/schemas/workflow_stage_response.py`
  - Agregar campo `style: dict`

#### 4.2 Request Schema (opcional)
- [x] Crear `src/company_workflow/presentation/schemas/stage_style_request.py`
  - Schema para actualizar estilos de stages

### Fase 5: Frontend - TypeScript y UI

#### 5.1 Tipos TypeScript
- [x] Crear `client-vite/src/types/stageStyle.ts`
  ```typescript
  export interface StageStyle {
    icon: string;
    color: string;
    background_color: string;
  }
  ```

#### 5.2 Actualizar WorkflowStage Type
- [x] Modificar `client-vite/src/types/workflow.ts`
  - Agregar campo `style: StageStyle`

#### 5.3 Componentes Kanban
- [x] Actualizar `client-vite/src/pages/company/WorkflowBoardPage.tsx` (StageColumn)
  - Aplicar estilos dinámicos del stage
  - Usar `style.color` para texto
  - Usar `style.background_color` para fondo
  - Renderizar `style.icon` en el header

#### 5.4 Componentes Row Stages
- [x] Actualizar `client-vite/src/components/kanban/RowStageSection.tsx`
  - Aplicar estilos dinámicos
  - Usar colores del stage para el header

#### 5.5 Estilos CSS
- [x] Actualizar `client-vite/src/components/kanban/kanban-styles.css`
  - Clases dinámicas para colores
  - Soporte para iconos HTML/SVG

### Fase 6: Configuración (Opcional para MVP)

#### 6.1 Interface de Configuración
- [ ] Crear página de configuración de estilos de stages
  - Selector de colores
  - Editor de iconos
  - Preview en tiempo real

## Estructura del Value Object

```python
@dataclass(frozen=True)
class StageStyle:
    icon: str
    color: str
    background_color: str
    
    @staticmethod
    def create(
        icon: str = "📋",
        color: str = "#374151",
        background_color: str = "#f3f4f6"
    ) -> "StageStyle":
        # Validaciones
        return StageStyle(icon, color, background_color)
    
    def update(
        self,
        icon: str | None = None,
        color: str | None = None,
        background_color: str | None = None
    ) -> "StageStyle":
        return StageStyle(
            icon=icon if icon is not None else self.icon,
            color=color if color is not None else self.color,
            background_color=background_color if background_color is not None else self.background_color
        )
```

## Validaciones

### Icon
- No vacío
- Máximo 1000 caracteres (para SVG HTML)
- Validar que sea emoji válido o HTML válido

### Color
- Formato hex (#RRGGBB), rgb(r,g,b), o nombre CSS válido
- Validar con regex

### Background Color
- Mismas validaciones que color
- Debe contrastar con el color del texto

## Valores por Defecto

```python
DEFAULT_STAGE_STYLE = StageStyle(
    icon="📋",
    color="#374151",  # gray-700
    background_color="#f3f4f6"  # gray-100
)
```

## Testing

### Unit Tests
- [ ] Tests para `StageStyle` value object
- [ ] Tests para validaciones de colores
- [ ] Tests para métodos `create()` y `update()`

### Integration Tests
- [ ] Tests para repositorio con estilos
- [ ] Tests para API endpoints
- [ ] Tests para mappers

### Frontend Tests
- [ ] Tests para componentes con estilos dinámicos
- [ ] Tests para renderizado de iconos

## Consideraciones de UX

### Iconos
- **Emoji**: Simple, universal, no requiere CSS adicional
- **HTML Icons**: FontAwesome, Heroicons, etc.
- **SVG HTML**: Máxima flexibilidad, puede ser personalizado

### Colores
- **Paleta consistente**: Usar colores de la paleta del sistema
- **Contraste**: Asegurar legibilidad
- **Accesibilidad**: Cumplir con WCAG 2.1

### Performance
- **Lazy loading**: Cargar iconos solo cuando se necesiten
- **Caching**: Cachear estilos procesados
- **Minificación**: Optimizar SVG embebidos

## Migración de Datos Existentes

### Script de Migración
- [ ] Crear script para asignar estilos por defecto a stages existentes
- [ ] Basar estilos en `stage_type` (SUCCESS = verde, FAIL = rojo, etc.)
- [ ] Ejecutar después de la migración de base de datos

## Rollback Plan

### Si hay problemas
1. Revertir migración de base de datos
2. Revertir cambios en entidades
3. Revertir cambios en frontend
4. Restaurar backup de base de datos

## Estimación de Tiempo

- **Fase 1-2 (Backend)**: 4-6 horas
- **Fase 3-4 (API)**: 2-3 horas  
- **Fase 5 (Frontend)**: 6-8 horas
- **Fase 6 (Configuración)**: 4-6 horas
- **Testing**: 3-4 horas

**Total estimado**: 19-27 horas

## Dependencias

- Migración de base de datos completada
- Sistema de value objects funcionando
- Frontend Kanban implementado
- Sistema de mappers funcionando
