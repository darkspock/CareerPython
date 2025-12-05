# 🧪 Plan de Testing - Pestaña de Entrevistas

## Objetivos
Validar que la nueva funcionalidad de gestión de entrevistas funciona correctamente en todos los escenarios.

---

## Pre-requisitos

1. **Backend y Frontend corriendo**:
   ```bash
   # Terminal 1: Backend
   make run
   
   # Terminal 2: Frontend
   cd client-vite && npm run dev
   ```

2. **Datos de prueba**:
   - Una empresa con al menos un candidato
   - Un workflow con múltiples etapas
   - Al menos 2 roles de empresa creados
   - Al menos 2 usuarios de empresa activos
   - Al menos 1 plantilla de entrevista habilitada

3. **URL de prueba**:
   ```
   http://localhost:5173/company/candidates/{CANDIDATE_ID}
   ```
   Reemplazar `{CANDIDATE_ID}` con un ID real de candidato.

---

## TEST-1: Crear entrevistas en diferentes etapas

### Objetivo
Verificar que se pueden crear entrevistas para distintas etapas del workflow.

### Pasos:
1. **Navegar a la página del candidato**
   - Abrir `http://localhost:5173/company/candidates/{CANDIDATE_ID}`
   - Verificar que la página carga correctamente

2. **Abrir la pestaña "Interviews"**
   - Click en la pestaña "Interviews" (o "Entrevistas")
   - Verificar que se muestra:
     - Sección "Entrevistas de la Etapa Actual" (vacía inicialmente)
     - Botón "Asignar Entrevista" (esquina superior derecha)

3. **Crear entrevista para la etapa actual**
   - Click en "Asignar Entrevista"
   - Verificar que el modal se abre
   - Verificar que la etapa actual está pre-seleccionada
   - Completar el formulario:
     - **Etapa**: Dejar la actual
     - **Tipo**: Seleccionar "Technical" o "Behavioral"
     - **Plantilla**: Verificar que se carga automáticamente si solo hay una, o seleccionar una si hay varias
     - **Roles Obligatorios**: Seleccionar al menos 1 rol (✓ obligatorio)
     - **Fecha**: (Opcional) Seleccionar una fecha futura
     - **Participantes**: (Opcional) Seleccionar algunos usuarios
   - Click en "Asignar Entrevista"
   - Verificar que el modal se cierra
   - **✅ Resultado esperado**: La entrevista aparece en "Entrevistas de la Etapa Actual"

4. **Crear entrevista para otra etapa**
   - Click en "Asignar Entrevista" nuevamente
   - Cambiar la **Etapa** a una diferente a la actual
   - Completar el resto del formulario
   - Guardar
   - **✅ Resultado esperado**: La entrevista NO aparece en "Entrevistas de la Etapa Actual", sino en la sección "Otras Etapas" (colapsada inicialmente)

5. **Crear múltiples entrevistas**
   - Crear al menos 3 entrevistas más:
     - 2 para la etapa actual
     - 1 para otra etapa
   - **✅ Resultado esperado**: Se organizan correctamente por sección

### Validaciones:
- [ ] El modal se abre y cierra correctamente
- [ ] Los campos obligatorios están marcados con `*`
- [ ] No se puede guardar sin seleccionar etapa, tipo y al menos 1 rol
- [ ] Las plantillas se cargan según el tipo seleccionado
- [ ] Si hay solo 1 plantilla, se auto-selecciona
- [ ] Si hay 0 plantillas, muestra mensaje "No templates available"
- [ ] Si hay 2+ plantillas, muestra un selector
- [ ] La fecha programada debe ser futura (error si es pasada)
- [ ] Las entrevistas se separan correctamente por etapa

---

## TEST-2: Listado y separación por etapas

### Objetivo
Verificar que las entrevistas se muestran correctamente organizadas.

### Pasos:
1. **Verificar sección "Entrevistas de la Etapa Actual"**
   - Contar el número de entrevistas mostradas
   - **✅ Resultado esperado**: Solo las entrevistas de la etapa actual del candidato

2. **Verificar cada tarjeta de entrevista**
   - Verificar que muestra:
     - Título de la entrevista (si existe)
     - Estado (badge de color): COMPLETED (verde), SCHEDULED (azul), PENDING (gris)
     - Tipo de entrevista
     - Nombre de la etapa (ej: "Etapa: Primera Entrevista")
     - Fecha programada (si existe)
     - Lista de entrevistadores (si existen)
     - Lista de roles obligatorios (si existen)
     - Puntuación (si existe)

3. **Verificar sección "Otras Etapas"**
   - Click en el header de "Otras Etapas" para expandir/colapsar
   - **✅ Resultado esperado**: Se muestra/oculta correctamente
   - Verificar que muestra el contador: "(X)" donde X = número de entrevistas

4. **Verificar entrevistas en "Otras Etapas"**
   - Expandir la sección
   - Verificar que SOLO aparecen entrevistas de etapas diferentes a la actual
   - Verificar que cada tarjeta incluye el nombre de su etapa

### Validaciones:
- [ ] Las secciones están claramente diferenciadas
- [ ] El contador de "Otras Etapas" es correcto
- [ ] El collapse/expand funciona suavemente
- [ ] Todas las tarjetas tienen la información completa
- [ ] Los badges de estado tienen los colores correctos
- [ ] El diseño es responsive (probar en desktop, tablet, mobile)

---

## TEST-3: Cambio de etapa del candidato y reclasificación

### Objetivo
Verificar que las entrevistas se reclasifican correctamente cuando el candidato cambia de etapa.

### Pasos:
1. **Estado inicial**
   - Verificar la etapa actual del candidato (en el header de la página)
   - Contar cuántas entrevistas hay en "Entrevistas de la Etapa Actual"
   - Contar cuántas en "Otras Etapas"

2. **Crear entrevista de prueba**
   - Crear 1 entrevista para la etapa actual
   - Verificar que aparece en "Entrevistas de la Etapa Actual"

3. **Cambiar etapa del candidato**
   - Volver a la pestaña "Info" (primera pestaña)
   - Usar los botones de la barra lateral derecha para mover el candidato a la siguiente etapa
   - **✅ Resultado esperado**: El candidato se mueve correctamente

4. **Verificar reclasificación**
   - Volver a la pestaña "Interviews"
   - **✅ Resultado esperado**:
     - La entrevista que estaba en "Etapa Actual" ahora está en "Otras Etapas"
     - "Entrevistas de la Etapa Actual" está vacía (o con las entrevistas de la nueva etapa si las hay)

5. **Crear entrevista en nueva etapa**
   - Crear una entrevista para la nueva etapa actual
   - **✅ Resultado esperado**: Aparece en "Entrevistas de la Etapa Actual"

6. **Volver a etapa anterior** (si es posible)
   - Mover el candidato de vuelta a la etapa anterior
   - Volver a la pestaña "Interviews"
   - **✅ Resultado esperado**: Las entrevistas se reclasifican nuevamente

### Validaciones:
- [ ] Las entrevistas se mueven de sección al cambiar etapa
- [ ] Los contadores se actualizan correctamente
- [ ] No se pierden entrevistas en el proceso
- [ ] Cada entrevista muestra siempre el nombre correcto de su etapa
- [ ] La reclasificación es inmediata (o se actualiza al refrescar)

---

## TEST-4: UI/UX, Responsive, Traducciones y Accesibilidad

### Objetivo
Verificar la calidad de la interfaz y experiencia de usuario.

### 4.1: Responsive Design
1. **Desktop (1920x1080)**
   - Abrir en pantalla completa
   - Verificar que el modal ocupa un ancho razonable (max-w-2xl)
   - Verificar que las tarjetas de entrevista se ven bien espaciadas

2. **Tablet (768x1024)**
   - Redimensionar ventana o usar DevTools
   - Verificar que el layout se adapta correctamente
   - Verificar que el modal es scrollable si es necesario

3. **Mobile (375x667)**
   - Verificar que las tarjetas de entrevista se apilan verticalmente
   - Verificar que el modal se adapta al ancho de la pantalla
   - Verificar que los botones son suficientemente grandes para tocar
   - Verificar que no hay scroll horizontal

### Validaciones Responsive:
- [ ] Desktop: layout de 2 columnas funciona correctamente
- [ ] Tablet: todo es legible y accesible
- [ ] Mobile: no hay elementos cortados ni overlapping
- [ ] Los selectores y checkboxes son fáciles de usar en touch

### 4.2: Traducciones (i18n)
1. **Español** (idioma por defecto, probablemente)
   - Verificar que todos los textos están en español
   - Buscar textos en inglés que no deberían estar

2. **Inglés** (si está configurado)
   - Cambiar idioma de la aplicación
   - Verificar que todos los textos se traducen

### Textos a verificar:
- [ ] "Entrevistas" / "Interviews"
- [ ] "Asignar Entrevista" / "Assign Interview"
- [ ] "Entrevistas de la Etapa Actual" / "Current Stage Interviews"
- [ ] "Otras Etapas" / "Other Stages"
- [ ] Labels del formulario: "Etapa", "Tipo", "Plantilla", etc.
- [ ] Mensajes de error de validación
- [ ] Tipos de entrevista: "Technical", "Behavioral", etc.
- [ ] Estados: "COMPLETED", "SCHEDULED", "PENDING"

### 4.3: Accesibilidad (a11y)
1. **Navegación por teclado**
   - Abrir el modal
   - Usar `Tab` para navegar entre campos
   - Usar `Space` o `Enter` para seleccionar checkboxes
   - Usar `Escape` para cerrar el modal
   - **✅ Resultado esperado**: Todo es navegable sin mouse

2. **Labels y ARIA**
   - Verificar que todos los inputs tienen labels asociados
   - Verificar que los checkboxes tienen texto descriptivo
   - Verificar que los botones tienen tooltips o aria-labels si solo tienen iconos

3. **Contraste de colores**
   - Verificar que los textos tienen suficiente contraste sobre el fondo
   - Verificar que los badges de estado son distinguibles
   - Usar herramientas como WebAIM Contrast Checker si es necesario

### Validaciones a11y:
- [ ] Navegación por teclado funciona en todo el flujo
- [ ] Screen readers pueden leer todos los elementos importantes
- [ ] Los colores tienen suficiente contraste (WCAG AA mínimo)
- [ ] Los errores de validación son claros y se anuncian

### 4.4: Usabilidad general
1. **Estados de carga**
   - Verificar que se muestran spinners al cargar plantillas, roles, usuarios
   - Verificar que el botón de "Asignar Entrevista" se deshabilita mientras está guardando

2. **Mensajes de error**
   - Intentar guardar sin completar campos obligatorios
   - Verificar que los errores aparecen junto a cada campo
   - Verificar que el mensaje de error global aparece si hay error del backend

3. **Feedback visual**
   - Verificar que los botones cambian de color al hacer hover
   - Verificar que los checkboxes muestran el estado checked/unchecked claramente
   - Verificar que los selects muestran el valor seleccionado

4. **Performance**
   - Crear 10+ entrevistas
   - Verificar que la lista sigue siendo fluida
   - Verificar que el filtrado por etapa es instantáneo

### Validaciones Usabilidad:
- [ ] Los loading states son claros
- [ ] Los errores son informativos y útiles
- [ ] El feedback visual es inmediato
- [ ] No hay lag o freezing con muchas entrevistas

---

## Checklist General de Completitud

### Funcionalidad Core
- [ ] Puedo ver la pestaña "Interviews" en la página de detalle del candidato
- [ ] Puedo crear una nueva entrevista usando el modal
- [ ] Las entrevistas se separan correctamente por etapa (actual vs otras)
- [ ] Al cambiar la etapa del candidato, las entrevistas se reclasifican
- [ ] Puedo colapsar/expandir la sección "Otras Etapas"

### Formulario de Asignación
- [ ] Todos los campos obligatorios funcionan correctamente
- [ ] La etapa actual está pre-seleccionada
- [ ] Las plantillas se cargan según el tipo de entrevista
- [ ] Si hay 0 plantillas, muestra un mensaje informativo
- [ ] Si hay 1 plantilla, se auto-selecciona
- [ ] Si hay 2+ plantillas, muestra un selector
- [ ] Los roles se cargan correctamente
- [ ] Los usuarios se cargan correctamente
- [ ] La validación de fecha futura funciona
- [ ] Los mensajes de error son claros

### UX/UI
- [ ] El diseño es responsive (desktop, tablet, mobile)
- [ ] Las traducciones están completas
- [ ] La navegación por teclado funciona
- [ ] Los colores tienen buen contraste
- [ ] Los estados de carga son visibles
- [ ] Los errores son informativos

---

## Reporte de Bugs

Si encuentras bugs durante el testing, repórtalos con el siguiente formato:

```markdown
### Bug #X: [Título descriptivo]

**Severidad**: Alta / Media / Baja

**Descripción**:
[Descripción clara del problema]

**Pasos para reproducir**:
1. ...
2. ...
3. ...

**Resultado esperado**:
[Lo que debería pasar]

**Resultado actual**:
[Lo que está pasando]

**Logs/Screenshots**:
[Si aplica]

**Entorno**:
- OS: macOS / Windows / Linux
- Navegador: Chrome 120 / Firefox 115 / Safari 17
- Tamaño de pantalla: Desktop / Tablet / Mobile
```

---

## Mejoras Sugeridas (Opcional)

Si durante el testing identificas mejoras potenciales, puedes documentarlas aquí:

1. **Mejora en filtros**:
   - Añadir filtro por estado (COMPLETED, SCHEDULED, PENDING)
   - Añadir filtro por tipo de entrevista

2. **Mejora en visualización**:
   - Añadir un timeline visual de entrevistas
   - Añadir iconos distintos por tipo de entrevista

3. **Mejora en acciones**:
   - Botón para editar entrevista
   - Botón para eliminar entrevista
   - Botón para completar/cambiar estado

---

## Notas Finales

- **Testing manual**: Esta funcionalidad requiere testing manual ya que involucra interacción con UI
- **Testing automatizado**: Se recomienda crear tests E2E con Playwright o Cypress en el futuro
- **Documentación**: Actualizar el manual de usuario con la nueva funcionalidad

**Tiempo estimado de testing completo**: 2-3 horas

¡Buena suerte con el testing! 🚀


