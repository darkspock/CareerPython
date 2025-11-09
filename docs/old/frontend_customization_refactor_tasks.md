# Tareas: Refactor de Customization en el Frontend

**Objetivo:** Desacoplar el sistema de customization del frontend para que sea genérico e independiente, similar al refactor del backend.

---

## Fase 1: Tipos Genéricos

### ✅ Tarea 1.1: Crear tipos de customization genéricos
**Archivo:** `client-vite/src/types/customization.ts`

- [ ] Crear `EntityCustomizationType` type
- [ ] Crear `CustomField` interface (sin `workflow_id`)
- [ ] Crear `EntityCustomization` interface
- [ ] Crear `FieldConfiguration` interface (con `context_type` y `context_id`)
- [ ] Crear `CreateEntityCustomizationRequest` interface
- [ ] Crear `UpdateEntityCustomizationRequest` interface
- [ ] Crear `CreateCustomFieldRequest` interface (sin `workflow_id`)
- [ ] Exportar todos los tipos

### ✅ Tarea 1.2: Actualizar tipos en workflow.ts
**Archivo:** `client-vite/src/types/workflow.ts`

- [ ] Marcar `CustomField` (viejo) como deprecated
- [ ] Marcar `FieldConfiguration` (viejo) como deprecated
- [ ] Agregar comentarios indicando usar tipos de `customization.ts`
- [ ] Mantener tipos viejos para compatibilidad temporal

---

## Fase 2: Servicio Genérico

### ✅ Tarea 2.1: Crear servicio de entity customization
**Archivo:** `client-vite/src/services/entityCustomizationService.ts`

- [ ] Crear clase `EntityCustomizationService`
- [ ] Implementar `getCustomization(entityType, entityId)`
- [ ] Implementar `getCustomizationById(id)`
- [ ] Implementar `createCustomization(request)`
- [ ] Implementar `updateCustomization(id, request)`
- [ ] Implementar `deleteCustomization(id)`
- [ ] Implementar `addFieldToEntity(customizationId, field)`
- [ ] Implementar `listFieldsByEntity(entityType, entityId)`

### ✅ Tarea 2.2: Actualizar customFieldService.ts
**Archivo:** `client-vite/src/services/customFieldService.ts`

- [ ] Marcar clase como `@deprecated`
- [ ] Agregar comentarios indicando usar `EntityCustomizationService`
- [ ] Opcional: Crear wrappers que usen el nuevo servicio internamente

---

## Fase 3: Componentes Genéricos

### ✅ Tarea 3.1: Crear EntityCustomFieldEditor
**Archivo:** `client-vite/src/components/customization/EntityCustomFieldEditor.tsx`

- [ ] Crear componente genérico basado en `CustomFieldEditor`
- [ ] Usar `entityType` y `entityId` en lugar de `workflowId`
- [ ] Usar `EntityCustomizationService` en lugar de `CustomFieldService`
- [ ] Mantener misma funcionalidad (crear, editar, eliminar, reordenar)
- [ ] Usar tipos de `customization.ts`

### ✅ Tarea 3.2: Crear FieldVisibilityMatrix genérico
**Archivo:** `client-vite/src/components/customization/FieldVisibilityMatrix.tsx`

- [ ] Crear componente genérico basado en `FieldVisibilityMatrix`
- [ ] Usar `entityType`, `entityId`, `contextType`, `contexts` en lugar de `workflowId` y `stages`
- [ ] Usar `EntityCustomizationService` para configuraciones
- [ ] Mantener misma funcionalidad (matriz de visibilidad)
- [ ] Usar tipos de `customization.ts`

### ✅ Tarea 3.3: Crear index de componentes
**Archivo:** `client-vite/src/components/customization/index.ts`

- [ ] Exportar `EntityCustomFieldEditor`
- [ ] Exportar `FieldVisibilityMatrix`
- [ ] Exportar otros componentes relacionados si existen

---

## Fase 4: Actualizar Páginas

### ✅ Tarea 4.1: Actualizar WorkflowAdvancedConfigPage
**Archivo:** `client-vite/src/pages/workflow/WorkflowAdvancedConfigPage.tsx`

- [ ] Importar nuevos componentes de `components/customization`
- [ ] Reemplazar `CustomFieldEditor` con `EntityCustomFieldEditor`
- [ ] Reemplazar `FieldVisibilityMatrix` con el nuevo genérico
- [ ] Actualizar props para usar `entityType="Workflow"` y `entityId={workflowId}`
- [ ] Actualizar `contextType="WorkflowStage"` y `contexts={stages}`
- [ ] Probar que funcione correctamente

### ✅ Tarea 4.2: Revisar EditWorkflowPage
**Archivo:** `client-vite/src/pages/workflow/EditWorkflowPage.tsx`

- [ ] Verificar si usa customization
- [ ] Si usa, actualizar para usar nuevos componentes
- [ ] Probar que funcione correctamente

### ✅ Tarea 4.3: Revisar otras páginas
**Archivos:** Todas las páginas en `client-vite/src/pages/`

- [ ] Buscar usos de `CustomFieldEditor`
- [ ] Buscar usos de `FieldVisibilityMatrix`
- [ ] Buscar usos de `CustomFieldService`
- [ ] Actualizar para usar nuevos componentes/servicios

---

## Fase 5: Wrappers de Compatibilidad (Opcional)

### ✅ Tarea 5.1: Crear wrappers en components/workflow
**Archivo:** `client-vite/src/components/workflow/CustomFieldEditor.tsx` (wrapper)

- [ ] Crear wrapper que use `EntityCustomFieldEditor` internamente
- [ ] Mantener misma API (props con `workflowId`)
- [ ] Marcar como deprecated
- [ ] Agregar comentario indicando usar `EntityCustomFieldEditor`

**Archivo:** `client-vite/src/components/workflow/FieldVisibilityMatrix.tsx` (wrapper)

- [ ] Crear wrapper que use el nuevo `FieldVisibilityMatrix` genérico
- [ ] Mantener misma API (props con `workflowId` y `stages`)
- [ ] Marcar como deprecated
- [ ] Agregar comentario indicando usar el nuevo componente

---

## Fase 6: Limpieza y Documentación

### ✅ Tarea 6.1: Actualizar imports
**Archivos:** Todos los archivos que usen customization

- [ ] Actualizar imports para usar tipos de `customization.ts`
- [ ] Actualizar imports para usar `EntityCustomizationService`
- [ ] Actualizar imports para usar componentes de `components/customization`

### ✅ Tarea 6.2: Eliminar código legacy (después de verificar)
**Archivos:** Solo después de verificar que todo funciona

- [ ] Eliminar `customFieldService.ts` (o mantener como deprecated)
- [ ] Eliminar componentes viejos en `components/workflow/` (o mantener como deprecated)
- [ ] Eliminar tipos viejos de `workflow.ts` (o mantener como deprecated)

### ✅ Tarea 6.3: Documentación
**Archivo:** README o documentación del frontend

- [ ] Documentar nuevo sistema de customization
- [ ] Documentar cómo usar `EntityCustomFieldEditor`
- [ ] Documentar cómo usar `FieldVisibilityMatrix` genérico
- [ ] Documentar migración desde sistema viejo

---

## 📋 Checklist de Verificación

Antes de considerar completado:

- [ ] Todos los tipos genéricos creados y exportados
- [ ] Servicio genérico implementado y probado
- [ ] Componentes genéricos creados y funcionando
- [ ] Páginas de workflow actualizadas y funcionando
- [ ] No hay errores de TypeScript
- [ ] No hay errores de linting
- [ ] Funcionalidad de customization sigue funcionando en workflows
- [ ] Código legacy marcado como deprecated o eliminado

---

## 🎯 Orden de Implementación Recomendado

1. **Fase 1** (Tipos) → Crear base sólida
2. **Fase 2** (Servicio) → Implementar comunicación con backend
3. **Fase 3** (Componentes) → Crear componentes genéricos
4. **Fase 4** (Páginas) → Actualizar páginas para usar nuevos componentes
5. **Fase 5** (Wrappers) → Opcional, solo si se necesita compatibilidad
6. **Fase 6** (Limpieza) → Después de verificar que todo funciona

---

## ⚠️ Notas Importantes

1. **Compatibilidad:** Mantener código viejo funcionando durante la transición
2. **Testing:** Probar cada fase antes de continuar
3. **Backend:** Asegurar que el backend ya esté refactorizado (✅ completado)
4. **Endpoints:** Verificar que los endpoints del backend estén disponibles
5. **Tipos:** Mantener sincronizados con los tipos del backend

