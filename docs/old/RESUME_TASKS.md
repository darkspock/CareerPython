# Plan Detallado - Implementación Nueva Arquitectura CV

## 🎯 Objetivo
Migrar de la estructura fija actual de CV a una arquitectura híbrida con secciones fijas y variables según RESUME.md

## 📊 Estado Actual vs Objetivo

### ❌ Estado Actual (Implementado)
```
ResumeContent {
  experiencia_profesional: string (markdown)
  educacion: string (markdown)
  proyectos: string (markdown)
  habilidades: string (markdown)
  datos_personales: object
}
```

### ✅ Estado Objetivo (RESUME.md)
```
Todo en ingles=>

ResumeContent {
  // Sección Fija
  datos_generales: GeneralDataVO {
    titulo_cv: string
    email: string
    telefono: string
    nombre: string
  }

  // Secciones Variables
  secciones_variables: VariableSection[] {
    key: string
    title: string
    content: string (HTML)
  }
}
```

## 🚧 Tareas de Migración

### FASE 1: Backend - Domain Layer
- [ ] **1.1** Crear `GeneralDataVO` (Value Object para datos fijos)
- [ ] **1.2** Crear `VariableSection` (Value Object para secciones variables)
- [ ] **1.3** Actualizar `ResumeContent` con nueva estructura
- [ ] **1.4** Actualizar `Resume` entity para manejar nueva estructura
- [ ] **1.5** Migrar factory methods existentes

### FASE 2: Backend - Application Layer
- [ ] **2.1** Actualizar `UpdateResumeContentCommand` para nueva estructura
- [ ] **2.2** Actualizar handlers para procesar secciones variables
- [ ] **2.3** Actualizar generation service para nueva estructura
- [ ] **2.4** Crear comandos para agregar/eliminar secciones variables

### FASE 3: Backend - Infrastructure Layer
- [ ] **3.1** Actualizar schema base datos (JSON para secciones variables)
- [ ] **3.2** Crear migración de datos existentes
- [ ] **3.3** Actualizar repository para nueva estructura
- [ ] **3.4** Actualizar mappers y DTOs

### FASE 4: Backend - Presentation Layer
- [ ] **4.1** Actualizar request/response schemas
- [ ] **4.2** Actualizar controllers para manejar secciones variables
- [ ] **4.3** Crear endpoints para CRUD de secciones variables
- [ ] **4.4** Actualizar validaciones

### FASE 5: Frontend - Editor WYSIWYG
- [ ] **5.1** Reemplazar editor actual con editor WYSIWYG (TinyMCE/CKEditor)
- [ ] **5.2** Implementar componente para secciones fijas
- [ ] **5.3** Implementar componente para secciones variables dinámicas
- [ ] **5.4** Funcionalidad agregar/eliminar secciones
- [ ] **5.5** Drag & drop para reordenar secciones

### FASE 6: Frontend - Preview & Export
- [ ] **6.1** Actualizar preview para mostrar nueva estructura
- [ ] **6.2** Actualizar templates para nueva estructura
- [ ] **6.3** Actualizar export functionality

### FASE 7: Data Migration
No hay, no hay CVS ahora mismo

## ⚠️ Riesgos y Consideraciones



## 🤔 Decisiones Pendientes

1. **¿Migrar automáticamente todos los CVs existentes o mantener compatibilidad?**
No migrar
3. **¿Qué editor WYSIWYG usar? (TinyMCE, CKEditor, Quill, etc.)**
¿Alguno fácilmente integrable con React?
3. **¿Cómo manejar el HTML sanitization para seguridad?**
sólo tags básicos, no scripts. 
4. **¿Mantener markdown como opción alternativa?**
No
5. **¿Implementar drag & drop para reordenar secciones?**
En primera versión no.

## 💡 Recomendación

**Propongo implementación incremental**:
1. Empezar con nueva estructura en backend
2. Mantener compatibilidad con estructura actual
3. Implementar frontend progresivamente
4. Migrar datos existentes al final
5. Deprecar estructura antigua gradualmente

¿Quieres que proceda con esta estrategia o prefieres ajustar algún aspecto del plan?