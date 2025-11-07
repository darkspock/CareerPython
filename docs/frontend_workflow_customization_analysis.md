# Análisis: Desacoplamiento de Customization en el Frontend

**Fecha:** 2024  
**Objetivo:** Analizar el código del frontend en `client-vite/src/pages/workflow` y proponer cómo hacerlo independiente del sistema de customization, similar al refactor del backend.

---

## 📊 Estado Actual

### Estructura Actual del Frontend

```
client-vite/src/
├── pages/workflow/
│   ├── CreateWorkflowPage.tsx
│   ├── EditWorkflowPage.tsx
│   ├── WorkflowAdvancedConfigPage.tsx  ← Usa CustomFieldEditor
│   ├── WorkflowBoardPage.tsx
│   └── WorkflowsSettingsPage.tsx
│
├── components/workflow/
│   ├── CustomFieldEditor.tsx  ← Acoplado a workflow_id
│   ├── FieldVisibilityMatrix.tsx  ← Acoplado a workflow_id
│   ├── ValidationRuleEditor.tsx
│   └── ...
│
├── services/
│   ├── companyWorkflowService.ts  ← Solo workflow/stages
│   ├── customFieldService.ts  ← Acoplado a workflows
│   └── customFieldValueService.ts
│
└── types/
    └── workflow.ts  ← Contiene tipos de CustomField acoplados a workflow_id
```

---

## 🔍 Problemas Identificados

### 1. **Tipos Acoplados a Workflow**

**Ubicación:** `client-vite/src/types/workflow.ts`

```typescript
export interface CustomField {
  id: string;
  workflow_id: string;  // ❌ Acoplado a workflow
  field_key: string;
  field_name: string;
  field_type: FieldType;
  field_config: Record<string, any> | null;
  order_index: number;
  created_at: string;
  updated_at: string;
}

export interface FieldConfiguration {
  id: string;
  stage_id: string;  // ❌ Acoplado a stage
  custom_field_id: string;
  visibility: FieldVisibility;
  created_at: string;
  updated_at: string;
}
```

**Problema:** Los tipos están diseñados específicamente para workflows, no son genéricos.

---

### 2. **Servicio Acoplado a Workflow**

**Ubicación:** `client-vite/src/services/customFieldService.ts`

```typescript
export class CustomFieldService {
  private static readonly BASE_PATH = '/api/custom-fields';  // ❌ Endpoint viejo

  static async listCustomFieldsByWorkflow(workflowId: string): Promise<CustomField[]> {
    // ❌ Usa endpoint específico de workflow
    return api.authenticatedRequest(`${this.BASE_PATH}/workflow/${workflowId}`);
  }
}
```

**Problema:** 
- Usa endpoints antiguos (`/api/custom-fields`) que están acoplados a workflows
- No usa el nuevo sistema de entity customization (`/api/entity-customizations`)

---

### 3. **Componentes Acoplados a Workflow**

**Ubicación:** `client-vite/src/components/workflow/CustomFieldEditor.tsx`

```typescript
interface CustomFieldEditorProps {
  workflowId: string;  // ❌ Requiere workflowId específico
  onFieldsChange?: (fields: CustomField[]) => void;
}
```

**Problema:** El componente solo funciona con workflows, no es genérico.

**Ubicación:** `client-vite/src/components/workflow/FieldVisibilityMatrix.tsx`

```typescript
interface FieldVisibilityMatrixProps {
  workflowId: string;  // ❌ Requiere workflowId
  stages: WorkflowStage[];  // ❌ Requiere stages de workflow
  fields: CustomField[];
  onConfigurationsChange?: (configurations: FieldConfiguration[]) => void;
}
```

**Problema:** Está diseñado específicamente para workflows y stages.

---

### 4. **Páginas que Usan Customization**

**Ubicación:** `client-vite/src/pages/workflow/WorkflowAdvancedConfigPage.tsx`

```typescript
// ❌ Usa CustomFieldEditor directamente acoplado a workflow
<CustomFieldEditor
  workflowId={workflowId!}
  onFieldsChange={setCustomFields}
/>

// ❌ Usa FieldVisibilityMatrix acoplado a workflow
<FieldVisibilityMatrix
  workflowId={workflowId!}
  stages={stages}
  fields={customFields}
  onConfigurationsChange={setFieldConfigurations}
/>
```

**Problema:** Las páginas están acopladas a la implementación específica de workflow.

---

## 🎯 Propuesta de Refactor

### Fase 1: Crear Tipos Genéricos

**Nuevo archivo:** `client-vite/src/types/customization.ts`

```typescript
// Entity Types
export type EntityCustomizationType = 'JobPosition' | 'CandidateApplication' | 'Candidate' | 'Workflow';

// Custom Field Types (genéricos, sin workflow_id)
export interface CustomField {
  id: string;
  field_key: string;
  field_name: string;
  field_type: FieldType;
  field_config: Record<string, any> | null;
  order_index: number;
  created_at: string;
  updated_at: string;
}

// Entity Customization
export interface EntityCustomization {
  id: string;
  entity_type: EntityCustomizationType;
  entity_id: string;
  fields: CustomField[];
  validation: string | null;
  metadata: Record<string, any>;
  created_at: string;
  updated_at: string;
}

// Field Configuration (genérico, con context_type y context_id)
export interface FieldConfiguration {
  id: string;
  entity_customization_id: string;
  custom_field_id: string;
  context_type: EntityCustomizationType;  // Puede ser 'WorkflowStage' u otro
  context_id: string;  // ID del contexto (stage_id, etc.)
  visibility: FieldVisibility;
  created_at: string;
  updated_at: string;
}
```

---

### Fase 2: Crear Servicio Genérico de Customization

**Nuevo archivo:** `client-vite/src/services/entityCustomizationService.ts`

```typescript
export class EntityCustomizationService {
  private static readonly BASE_PATH = '/api/entity-customizations';

  /**
   * Get entity customization by entity type and entity ID
   */
  static async getCustomization(
    entityType: EntityCustomizationType,
    entityId: string
  ): Promise<EntityCustomization> {
    return api.authenticatedRequest(
      `${this.BASE_PATH}/${entityType}/${entityId}`
    );
  }

  /**
   * Create entity customization
   */
  static async createCustomization(
    request: CreateEntityCustomizationRequest
  ): Promise<EntityCustomization> {
    return api.authenticatedRequest(this.BASE_PATH, {
      method: 'POST',
      body: JSON.stringify(request)
    });
  }

  /**
   * Update entity customization
   */
  static async updateCustomization(
    customizationId: string,
    request: UpdateEntityCustomizationRequest
  ): Promise<EntityCustomization> {
    return api.authenticatedRequest(`${this.BASE_PATH}/${customizationId}`, {
      method: 'PUT',
      body: JSON.stringify(request)
    });
  }

  /**
   * Add custom field to entity
   */
  static async addFieldToEntity(
    customizationId: string,
    field: CreateCustomFieldRequest
  ): Promise<EntityCustomization> {
    return api.authenticatedRequest(
      `${this.BASE_PATH}/${customizationId}/fields`,
      {
        method: 'POST',
        body: JSON.stringify(field)
      }
    );
  }
}
```

---

### Fase 3: Crear Componentes Genéricos

**Nuevo archivo:** `client-vite/src/components/customization/EntityCustomFieldEditor.tsx`

```typescript
interface EntityCustomFieldEditorProps {
  entityType: EntityCustomizationType;
  entityId: string;
  onFieldsChange?: (fields: CustomField[]) => void;
}

export const EntityCustomFieldEditor: React.FC<EntityCustomFieldEditorProps> = ({
  entityType,
  entityId,
  onFieldsChange
}) => {
  // Similar a CustomFieldEditor pero usa EntityCustomizationService
  // y trabaja con entity_type + entity_id en lugar de workflow_id
}
```

**Nuevo archivo:** `client-vite/src/components/customization/FieldVisibilityMatrix.tsx`

```typescript
interface FieldVisibilityMatrixProps {
  entityType: EntityCustomizationType;
  entityId: string;
  contextType: EntityCustomizationType;  // Tipo del contexto (ej: 'WorkflowStage')
  contexts: Array<{ id: string; name: string }>;  // Lista de contextos (stages, etc.)
  fields: CustomField[];
  onConfigurationsChange?: (configurations: FieldConfiguration[]) => void;
}

export const FieldVisibilityMatrix: React.FC<FieldVisibilityMatrixProps> = ({
  entityType,
  entityId,
  contextType,
  contexts,
  fields,
  onConfigurationsChange
}) => {
  // Similar a FieldVisibilityMatrix pero genérico
  // Usa context_type + context_id en lugar de stage_id
}
```

---

### Fase 4: Actualizar Páginas de Workflow

**Actualizar:** `client-vite/src/pages/workflow/WorkflowAdvancedConfigPage.tsx`

```typescript
// ✅ Usar el nuevo componente genérico
<EntityCustomFieldEditor
  entityType="Workflow"
  entityId={workflowId!}
  onFieldsChange={setCustomFields}
/>

// ✅ Usar el nuevo componente genérico
<FieldVisibilityMatrix
  entityType="Workflow"
  entityId={workflowId!}
  contextType="WorkflowStage"
  contexts={stages.map(s => ({ id: s.id, name: s.name }))}
  fields={customFields}
  onConfigurationsChange={setFieldConfigurations}
/>
```

---

### Fase 5: Mantener Compatibilidad Temporal

**Opción A: Wrapper Components**

Crear wrappers que mantengan la API antigua pero usen el nuevo sistema:

```typescript
// client-vite/src/components/workflow/CustomFieldEditor.tsx (wrapper)
export const CustomFieldEditor: React.FC<CustomFieldEditorProps> = ({
  workflowId,
  onFieldsChange
}) => {
  return (
    <EntityCustomFieldEditor
      entityType="Workflow"
      entityId={workflowId}
      onFieldsChange={onFieldsChange}
    />
  );
};
```

**Opción B: Migración Directa**

Actualizar todas las páginas para usar directamente los nuevos componentes genéricos.

---

## 📋 Plan de Implementación

### Paso 1: Crear Tipos Genéricos
- [ ] Crear `client-vite/src/types/customization.ts`
- [ ] Mover tipos de CustomField a customization.ts
- [ ] Actualizar imports en archivos existentes

### Paso 2: Crear Servicio Genérico
- [ ] Crear `client-vite/src/services/entityCustomizationService.ts`
- [ ] Implementar métodos para entity customization
- [ ] Mantener `customFieldService.ts` como deprecated/wrapper temporal

### Paso 3: Crear Componentes Genéricos
- [ ] Crear `client-vite/src/components/customization/EntityCustomFieldEditor.tsx`
- [ ] Crear `client-vite/src/components/customization/FieldVisibilityMatrix.tsx`
- [ ] Crear `client-vite/src/components/customization/index.ts`

### Paso 4: Actualizar Páginas
- [ ] Actualizar `WorkflowAdvancedConfigPage.tsx` para usar nuevos componentes
- [ ] Actualizar `EditWorkflowPage.tsx` si usa customization
- [ ] Verificar otras páginas que usen customization

### Paso 5: Limpieza
- [ ] Marcar `customFieldService.ts` como deprecated
- [ ] Marcar componentes viejos en `components/workflow/` como deprecated
- [ ] Actualizar documentación

---

## 🔄 Comparación: Antes vs Después

### Antes (Acoplado a Workflow)

```typescript
// Servicio
CustomFieldService.listCustomFieldsByWorkflow(workflowId)

// Componente
<CustomFieldEditor workflowId={workflowId} />

// Tipos
interface CustomField {
  workflow_id: string;  // ❌ Acoplado
}
```

### Después (Genérico)

```typescript
// Servicio
EntityCustomizationService.getCustomization('Workflow', workflowId)

// Componente
<EntityCustomFieldEditor 
  entityType="Workflow" 
  entityId={workflowId} 
/>

// Tipos
interface CustomField {
  // ✅ Sin workflow_id, genérico
}
interface EntityCustomization {
  entity_type: EntityCustomizationType;  // ✅ Genérico
  entity_id: string;  // ✅ Genérico
}
```

---

## ✅ Beneficios

1. **Reutilización:** Los componentes pueden usarse para cualquier entidad (JobPosition, Candidate, etc.)
2. **Consistencia:** Mismo sistema de customization para todas las entidades
3. **Mantenibilidad:** Un solo lugar para mantener la lógica de customization
4. **Escalabilidad:** Fácil agregar nuevos tipos de entidades
5. **Alineación:** Frontend alineado con el backend refactorizado

---

## ⚠️ Consideraciones

1. **Compatibilidad:** Mantener wrappers temporales para no romper código existente
2. **Migración Gradual:** Migrar página por página en lugar de todo a la vez
3. **Testing:** Probar que los workflows existentes sigan funcionando
4. **Documentación:** Actualizar documentación del frontend

---

## 📝 Próximos Pasos

1. Crear tipos genéricos en `types/customization.ts`
2. Crear servicio genérico `entityCustomizationService.ts`
3. Crear componentes genéricos en `components/customization/`
4. Actualizar páginas de workflow para usar los nuevos componentes
5. Eliminar código legacy después de verificar que todo funciona

