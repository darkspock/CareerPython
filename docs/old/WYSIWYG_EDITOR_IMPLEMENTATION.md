# Editor WYSIWYG para Descripciones de Posiciones

## Resumen

Se ha implementado un editor WYSIWYG (What You See Is What You Get) para el campo de descripción en la página de creación de posiciones de trabajo. Este editor permite a los usuarios crear contenido rico con formato, imágenes embebidas y estructura HTML.

## Características Implementadas

### ✅ Base de Datos
- **Campo `description`**: Cambiado de `character varying` a `TEXT` en PostgreSQL
- **Capacidad**: Puede almacenar contenido HTML largo sin restricciones de longitud
- **Ubicación**: Tabla `job_positions`, columna `description`

### ✅ Frontend
- **Editor**: @uiw/react-md-editor (licencia MIT)
- **Ubicación**: `client-vite/src/components/common/WysiwygEditor.tsx`
- **Página**: `client-vite/src/pages/company/CreatePositionPage.tsx`
- **Estilos**: `client-vite/src/components/common/WysiwygEditor.css`

## Funcionalidades del Editor

### 🎨 Formato de Texto
- **Negrita** y *cursiva*
- ~~Tachado~~ y <u>subrayado</u>
- Títulos (H1-H6)
- Citas y bloques de código

### 📝 Estructura de Contenido
- Listas con viñetas y numeradas
- Listas de tareas (checkboxes)
- Párrafos y saltos de línea
- Bloques de código con syntax highlighting

### 🖼️ Multimedia
- **Imágenes**: Soporte para URLs y drag & drop
- **Enlaces**: Con apertura en nueva pestaña
- **Tablas**: Con estilos predeterminados

### 🔧 Herramientas Adicionales
- **Modo Edición/Vista Previa**: Toggle entre edición y vista previa
- **Pantalla Completa**: Modo pantalla completa para edición
- **Markdown**: Soporte completo para sintaxis Markdown
- **Atajos de Teclado**: Atajos estándar de Markdown
- **Ayuda**: Guía de atajos integrada

### 🆕 Ventajas del Nuevo Editor

#### ✅ Licencia MIT
- **Completamente gratuito** para uso comercial
- **Sin restricciones** de registro o facturación
- **Código abierto** y mantenido activamente

#### ✅ Compatibilidad
- **React 19**: Compatible con la última versión de React
- **TypeScript**: Soporte nativo para TypeScript
- **Responsive**: Adaptable a diferentes tamaños de pantalla

#### ✅ Funcionalidades Avanzadas
- **Markdown**: Sintaxis Markdown estándar
- **Vista Previa**: Vista previa en tiempo real
- **Drag & Drop**: Arrastrar y soltar imágenes
- **Atajos**: Atajos de teclado intuitivos

## Configuración Técnica

### Dependencias
```json
{
  "@uiw/react-md-editor": "^7.x.x"
}
```

### Configuración del Editor
```typescript
{
  height: 400,
  preview: 'edit', // o 'preview' para solo vista previa
  hideToolbar: false,
  data-color-mode: 'light',
  commands: [
    // Herramientas de formato básico
    'bold',
    'italic',
    'strikethrough',
    'underline',
    'divider',
    
    // Títulos
    'title1',
    'title2',
    'title3',
    'title4',
    'title5',
    'title6',
    'divider',
    
    // Listas
    'unorderedListCommand',
    'orderedListCommand',
    'checkedListCommand',
    'divider',
    
    // Enlaces e imágenes
    'link',
    'image',
    'divider',
    
    // Código
    'codeBlock',
    'code',
    'quote',
    'divider',
    
    // Tabla
    'table',
    'divider',
    
    // Herramientas adicionales
    'fullscreen',
    'preview',
    'divider',
    
    // Ayuda
    'help'
  ]
}
```

## Uso

### En CreatePositionPage
```tsx
<WysiwygEditor
  value={formData.description}
  onChange={(content) => setFormData({ ...formData, description: content })}
  placeholder="Describe the role, responsibilities, and what you're looking for..."
  height={400}
  className="w-full"
/>
```

### Props del Componente
- `value`: Contenido HTML actual
- `onChange`: Callback cuando cambia el contenido
- `placeholder`: Texto de placeholder
- `height`: Altura del editor en píxeles
- `disabled`: Deshabilitar el editor
- `className`: Clases CSS adicionales

### Props Válidas del MDEditor
- `value`: Contenido del editor
- `onChange`: Callback de cambio
- `height`: Altura del editor
- `preview`: Modo de vista ('edit' o 'preview')
- `hideToolbar`: Ocultar barra de herramientas
- `data-color-mode`: Tema ('light' o 'dark')
- `textareaProps`: Props del textarea interno
- `commands`: Array de comandos de la barra de herramientas

### Props No Válidas (Removidas)
- `visibleDragBar`: No reconocida en versiones recientes
- `toolbarHeight`: No reconocida en versiones recientes

## Almacenamiento de Imágenes

### Estado Actual
- Las imágenes se convierten a base64 y se almacenan directamente en el HTML
- No hay límite de tamaño específico (limitado por el campo TEXT de PostgreSQL)

### Futuras Mejoras
- Integración con servicio de almacenamiento (S3/Local)
- Compresión automática de imágenes
- Gestión de archivos multimedia
- CDN para imágenes

## Validación

### Frontend
- El campo es requerido (marcado con asterisco rojo)
- Validación de contenido HTML válido
- Sanitización automática por TinyMCE

### Backend
- El campo se almacena como HTML en la base de datos
- No hay validación adicional de contenido HTML

## Consideraciones de Seguridad

### Sanitización
- TinyMCE incluye sanitización básica de HTML
- Se recomienda validación adicional en el backend para contenido sensible

### XSS Prevention
- El contenido se renderiza como HTML en el frontend
- Se recomienda usar `dangerouslySetInnerHTML` con precaución

## Testing

### Pruebas Manuales
1. Acceder a `http://localhost:5173/company/positions/create`
2. Verificar que el editor WYSIWYG aparece en lugar del textarea
3. Probar formato de texto (negrita, cursiva, etc.)
4. Probar inserción de imágenes
5. Probar creación de listas y tablas
6. Verificar que el contenido se guarda correctamente

### Pruebas de Base de Datos
```sql
-- Verificar que el campo puede almacenar HTML
SELECT description FROM job_positions WHERE description LIKE '%<h1>%';

-- Verificar longitud del contenido
SELECT LENGTH(description) as content_length FROM job_positions;
```

## Próximos Pasos

### Mejoras Sugeridas
1. **Integración con Storage Service**: Para manejo profesional de imágenes
2. **Plantillas**: Plantillas predefinidas para descripciones de trabajo
3. **Vista Previa**: Vista previa en tiempo real del contenido
4. **Historial**: Historial de cambios en el contenido
5. **Colaboración**: Edición colaborativa en tiempo real

### Optimizaciones
1. **Lazy Loading**: Cargar TinyMCE solo cuando sea necesario
2. **Compresión**: Comprimir imágenes automáticamente
3. **Caché**: Caché de contenido procesado
4. **CDN**: CDN para recursos estáticos del editor

## Archivos Modificados

### Backend
- `job_positions.description`: Cambiado a tipo TEXT

### Frontend
- `client-vite/src/components/common/WysiwygEditor.tsx`: Nuevo componente
- `client-vite/src/components/common/index.ts`: Exportación del componente
- `client-vite/src/pages/company/CreatePositionPage.tsx`: Integración del editor
- `client-vite/package.json`: Nueva dependencia

## Conclusión

El editor WYSIWYG está completamente funcional y permite crear descripciones de trabajo ricas y profesionales. El campo de base de datos puede manejar contenido HTML largo sin problemas, y la interfaz de usuario es intuitiva y fácil de usar.
