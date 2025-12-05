# Proceso de Onboarding para ATS Monkey
**Sistema de Seguimiento de Aplicaciones con IA – Filosofía CRM**  
*Fecha:* 2025-01-XX | *Versión:* 1.0

---

## Resumen Ejecutivo

El **onboarding perfecto** debe ser **rápido, inteligente y personalizado** según el tipo de empresa.  
Aplicamos una **filosofía CRM**:  
- Construir relaciones (candidatos como clientes).  
- Automatización inteligente (IA para sugerencias).  
- Datos accionables desde el Día 1.  
- Experiencia de usuario fluida y escalable.

El proceso se divide en **3 niveles de inicialización**:  
1. **ONBOARDING** → Configuración básica (roles + páginas)  
2. **WORKFLOWS** → Flujos de trabajo de contratación por defecto  
3. **SAMPLE DATA** → Datos de ejemplo opcionales para evaluación

> **Integración de IA**: Durante la creación, la IA analiza el nombre/descripción de la empresa y **sugiere el tipo + contenido inicial**.

---

## Paso 0: Selección del Tipo de Empresa

**Pregunta del asistente durante la creación de la empresa**:  
> *"¿Qué describe mejor tu empresa?"*

| Tipo | Características | Ejemplo |
|------|----------------|---------|
| **Startup / Pequeña Empresa** | 1–50 empleados, contratación rápida, usuarios multi-rol | Startup tecnológica, agencia local |
| **Empresa Mediana** | 51–500 empleados, estructurada pero flexible | SaaS en crecimiento, cadena minorista |
| **Empresa / Gran Corporación** | 501+ empleados, cumplimiento estricto, aprobaciones complejas | Fortune 500, empresa global |
| **Agencia de Reclutamiento** | Cualquier tamaño, alto volumen, enfocada en clientes | Empresa de staffing, headhunting |

> **Por defecto**: Empresa Mediana  
> **Sugerencia de IA**: Si el usuario omite, la IA predice según el nombre (ej: "TechFlow Inc." → Startup).

---

## 1. ONBOARDING – Configuración Básica (Roles + Páginas)

### Roles

**Enfoque CRM**: Los roles enfatizan la **experiencia del candidato** y la **propiedad de la relación**.

| Rol | Responsabilidades |
|------|-------------------|
| **Gerente de RRHH** | Estrategia, comunicación, etapa de oferta |
| **Reclutador** | Búsqueda, selección, engagement |
| **Líder Técnico** | Evaluaciones técnicas |
| **Gerente de Contratación** | Decisiones específicas de posición |
| **Entrevistador** | Realiza entrevistas |
| **Jefe de Departamento** | Aprobaciones de alto nivel |
| **CTO / C-Level** | Contrataciones senior |

#### **Diferenciación por Tipo de Empresa**

| Tipo | Ajustes de Roles |
|------|-----------------|
| **Startup/Pequeña** | Combinar Gerente de RRHH + Reclutador → **Generalista de RRHH**<br>Agregar **Fundador** para aprobaciones |
| **Mediana** | Agregar **Especialista en Adquisición de Talento** |
| **Empresa** | Agregar **Oficial de Diversidad e Inclusión**, **Revisor Legal** |
| **Agencia** | Agregar **Gerente de Cliente**, **Sourcer** |

> **Implementación**: Primer usuario = Admin. La IA sugiere asignaciones de roles al invitar al equipo.

---

### Páginas por Defecto

5 páginas creadas automáticamente. Todas soportan **HTML, SEO, versionado, multi-idioma** y **editor Unlayer**.

| Página | Propósito | Endpoint Público |
|--------|-----------|------------------|
| `public_company_description` | Descripción pública de la empresa | `/public/company/{id}/pages/public_company_description` |
| `job_position_description` | Beneficios/cultura en publicaciones de trabajo | Mismo |
| `data_protection` | Política de privacidad (GDPR/CCPA) | Mismo |
| `terms_of_use` | Términos legales de la plataforma | Mismo |
| `thank_you_application` | Mensaje post-aplicación | Mismo |

#### **Comportamiento por Inicialización**

| Modo | Estado | Contenido |
|------|--------|-----------|
| **Básico (sin muestra)** | DRAFT | Vacío, listo para editar |
| **Con Datos de Ejemplo** | PUBLISHED (o DRAFT) | Pre-llenado, personalizable |

#### **Diferenciación por Tipo de Empresa**

| Tipo | Tono y Contenido |
|------|-----------------|
| **Startup/Pequeña** | Energético, corto, emojis: "¡Únete a nuestro cohete!" |
| **Mediana** | Profesional, enfocado en crecimiento: "Trayectorias profesionales + beneficios" |
| **Empresa** | Formal, cumplimiento: EEO, descargos legales |
| **Agencia** | Centrado en el cliente: "Asóciate con nosotros" + placeholder `{{client_name}}` |

> **Característica de IA**: Auto-generar contenido borrador:  
> _"Basado en 'Nexlify AI', aquí está tu descripción pública: 'Estamos construyendo el futuro de...'"_

---

## 2. WORKFLOWS – Procesos de Contratación por Defecto

Utiliza el sistema **CompanyWorkflow + WorkflowStage**.  
**Enfoque CRM**: Cada etapa construye **confianza del candidato** (emails, feedback, transparencia).

### Workflow de Posiciones de Trabajo

**Creado automáticamente**: "Job Positions Workflow" (Kanban)

| Etapa | Tipo | Emoji |
|-------|------|-------|
| Draft | INITIAL | 📝 |
| Under Review | PROGRESS | 🔍 |
| Approved | PROGRESS | ✅ |
| Published | SUCCESS | 🌐 |
| Closed | SUCCESS | 🔒 |
| Cancelled | FAIL | ❌ |

#### **Diferenciación**

| Tipo | Ajustes |
|------|---------|
| **Startup** | Omitir "Under Review" → 4 etapas |
| **Mediana** | Agregar "Budget Approval" |
| **Empresa** | Agregar "Compliance Review" |
| **Agencia** | Agregar "Client Approval" |

---

### Workflows de Aplicación de Candidatos

**3 Fases** con **transiciones automáticas** en SUCCESS.

---

#### **Fase 1: Sourcing** (Kanban)  
*Objetivo: Selección y calificación de leads*

| Etapa | Tipo | Emoji |
|-------|------|-------|
| Pending | INITIAL | 📋 |
| Screening | PROGRESS | 🔍 |
| Qualified | SUCCESS → Fase 2 | ✅ |
| Not Suitable | FAIL | ❌ |
| On Hold | PROGRESS | ⏸️ |

> **Nota**: Las etapas "Not Suitable" y "On Hold" están configuradas con visualización **ROW** en el kanban.

---

#### **Fase 2: Evaluation** (Kanban)  
*Objetivo: Entrevistas y evaluaciones*

| Etapa | Tipo | Emoji |
|-------|------|-------|
| HR Interview | INITIAL | 👥 |
| Manager Interview | PROGRESS | 💼 |
| Assessment Test | PROGRESS | 📝 |
| Executive Interview | PROGRESS | 🎯 |
| Selected | SUCCESS → Fase 3 | ✅ |
| Rejected | FAIL | ❌ |

---

#### **Fase 3: Offer & Pre-Onboarding** (Vista de Lista)  
*Objetivo: Cerrar el trato*

| Etapa | Tipo | Emoji |
|-------|------|-------|
| Offer Proposal | INITIAL | 💌 |
| Negotiation | PROGRESS | 🤝 |
| Document Submission | PROGRESS | 📄 |
| Document Verification | SUCCESS | ✅ |
| Lost | FAIL | ❌ |

---

#### **Diferenciación por Tipo de Empresa**

| Tipo | Sourcing | Evaluation | Offer |
|------|----------|------------|-------|
| **Startup** | 3 etapas (rápido) | 4 etapas | 3 etapas |
| **Mediana** | Estándar | + Entrevista de Ajuste al Equipo | Estándar |
| **Empresa** | + Verificación de Antecedentes | + Panel + Referencias | + Revisión de Contrato |
| **Agencia** | + Matching de Cliente | + Entrevista de Cliente | + Tarifa de Colocación |

---

#### **Configuración de Etapas (Por WORKFLOW2.md / WORKFLOW3.md)**

| Config | Detalles |
|--------|----------|
| **Roles** | ej: RRHH en Sourcing, Líder Técnico en Assessment |
| **Emails** | Envío automático al entrar a la etapa (plantillas Unlayer) |
| **Deadline** | ej: 3 días (Sourcing), 7 días (Evaluation) |
| **Costo** | ej: $100 (entrevista), $50 (test) |
| **Campos Personalizados** | Ver abajo |

---

### Campos Personalizados Recomendados (Impulsados por CRM)

| Categoría | Campo | Tipo | Visibilidad | Etapa Sugerida |
|-----------|-------|------|-------------|----------------|
| **Compensación** | Rango Salarial | Texto/Número | Interna | Todas |
| | Salario Actual | Número | Interna | Sourcing |
| | Expectativa Salarial | Número | Interna | Offer |
| **Disponibilidad** | Fecha de Inicio | Fecha | Interna | Offer |
| | Período de Aviso | Texto | Interna | Offer |
| **Evaluación** | Puntuación Técnica | Número (0–100) | Interna | Assessment |
| | Puntuación de Ajuste Cultural | Número (0–100) | Interna | Entrevistas |
| | Feedback | Textarea | Interna | Todas |
| **Oferta** | Oferta Salarial | Número | Interna | Offer |
| | Paquete de Beneficios | Textarea | Interna | Offer |
| | Fecha de Inicio | Fecha | Interna | Offer |
| **Documentos** | Estado del Documento | Select | Interna | Verification |
| | Documentos Faltantes | Texto | Interna | Submission |
| **Fuente** | Fuente de Reclutamiento | Select | Interna | Sourcing |
| | Notas del Reclutador | Textarea | Interna | Todas |

#### **Campos Específicos por Tipo**

| Tipo | Campos Extra |
|------|--------------|
| **Startup** | **Oferta de Equity** (Número/%) |
| **Mediana** | **Asistencia de Reubicación** (Sí/No + Detalles) |
| **Empresa** | **Métricas de Diversidad** (Select: Subrepresentado) – *Obligatorio en Sourcing* |
| **Agencia** | **Puntuación de Ajuste de Cliente**, **Tarifa de Facturación** (Moneda) |

> **Sugerencia de IA**: "¿Para tu startup, agregar campo 'Equity' en etapa Offer?"

---

## 3. SAMPLE DATA – Modo de Evaluación Opcional

| Item | Cantidad | Detalles |
|------|----------|----------|
| Candidatos | 50 | Varias etapas, fuentes, puntuaciones |
| Posiciones de Trabajo | 10 | Draft → Published |
| Usuarios | 10 | Con roles, tareas, comentarios |
| Aplicaciones | 10 | Vinculadas a posiciones + usuarios |

#### **Diferenciación**

| Tipo | Escala | Enfoque |
|------|--------|---------|
| **Startup** | 20 candidatos, 5 posiciones | Contrataciones ágiles y rápidas |
| **Mediana** | Estándar | Análisis diversos |
| **Empresa** | 100 candidatos | Escenarios de cumplimiento |
| **Agencia** | Estándar + etiquetas de cliente | Pipelines multi-cliente |

> **Generado por IA**: Nombres realistas, currículums, comentarios  
> **Opt-in**: Checkbox: "¿Cargar datos de ejemplo?"  
> **Limpieza**: Comando `Reset Company Data`

---

## Flujo de Onboarding (Viaje del Usuario)

```mermaid
graph TD
    A[Crear Empresa] --> B[Seleccionar Tipo <br> (IA sugiere)]
    B --> C[Auto-Crear Roles + Páginas]
    C --> D[Auto-Crear Workflows]
    D --> E[¿Ofrecer Datos de Ejemplo?]
    E -->|Sí| F[Cargar Datos Generados por IA]
    E -->|No| G[Ir al Dashboard]
    G --> H[Tour Guiado: "Edita tu primer workflow"]
```

---

## Beneficios del Onboarding Personalizado

### Para Startups / Pequeñas Empresas
- **Configuración rápida**: Sin burocracia innecesaria
- **Roles simplificados**: Menos complejidad, más acción
- **Workflows ágiles**: Menos etapas, decisiones rápidas
- **Contenido energético**: Tono que refleja la cultura startup

### Para Empresas Medianas
- **Estructura balanceada**: Procesos definidos sin rigidez excesiva
- **Roles especializados**: Equipos más grandes, responsabilidades claras
- **Workflows estándar**: Procesos probados y escalables
- **Contenido profesional**: Enfoque en crecimiento y beneficios

### Para Empresas / Grandes Corporaciones
- **Cumplimiento integrado**: Revisión legal, métricas de diversidad
- **Roles de cumplimiento**: Oficiales de diversidad, revisores legales
- **Workflows robustos**: Verificaciones de antecedentes, paneles, referencias
- **Contenido formal**: EEO, descargos legales, políticas claras

### Para Agencias de Reclutamiento
- **Enfoque en clientes**: Gestión multi-cliente desde el inicio
- **Roles especializados**: Gerentes de cliente, sourcers
- **Workflows de colocación**: Matching de clientes, entrevistas de cliente
- **Contenido personalizable**: Placeholders para nombres de clientes

---

## Integración de IA

### Durante el Onboarding

1. **Sugerencia de Tipo de Empresa**
   - Analiza nombre y descripción
   - Sugiere tipo más probable
   - Usuario puede confirmar o cambiar

2. **Generación de Contenido**
   - Auto-genera descripciones de páginas
   - Sugiere campos personalizados relevantes
   - Propone ajustes de workflows

3. **Asignación de Roles**
   - Sugiere roles al invitar usuarios
   - Basado en tipo de empresa y tamaño del equipo

### Post-Onboarding

- **Sugerencias continuas**: "¿Agregar campo X para tu tipo de empresa?"
- **Optimización de workflows**: "Basado en tus datos, considera agregar etapa Y"
- **Análisis de rendimiento**: "Tu proceso de Sourcing toma 5 días en promedio"

---

## Métricas de Éxito del Onboarding

| Métrica | Objetivo |
|---------|----------|
| **Tiempo hasta primer candidato** | < 15 minutos |
| **Tiempo hasta primera publicación** | < 30 minutos |
| **Tasa de finalización** | > 80% |
| **Satisfacción del usuario** | > 4.5/5 |

---

## Próximos Pasos Después del Onboarding

1. **Tour Guiado**: "Edita tu primer workflow"
2. **Primera Publicación**: Asistente para crear primera posición
3. **Invitar Equipo**: Sugerencias de roles basadas en tipo de empresa
4. **Personalizar Páginas**: Editor visual con plantillas
5. **Configurar Campos**: Asistente de IA para campos personalizados

---

## Notas Técnicas

- **Persistencia**: Todos los datos se guardan inmediatamente
- **Reversibilidad**: Comando `Reset Company Data` disponible
- **Escalabilidad**: El sistema crece con la empresa
- **Multi-idioma**: Contenido soportado en múltiples idiomas
- **SEO**: Páginas públicas optimizadas para motores de búsqueda

---

*Documento de Negocio – ATS Monkey Onboarding System*

