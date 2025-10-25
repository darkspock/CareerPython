# Company Module - Modelo Final (3 Niveles + 2 Productos)

**Fecha**: 2025-01-XX
**Versión**: 3.0 - FINAL

## 🎯 Estrategia de Producto

### Dos Productos Separados

#### Producto 1: **Head Hunting / Talent Sourcing**
- **Target**: Recruiters, Talent Acquisition, Executive Search firms
- **Funcionalidad**: Prospección, sourcing, tracking de leads, outreach
- **Pricing**: Premium add-on
- **Value prop**: "Encuentra y gestiona talento antes de que apliquen"

#### Producto 2: **ATS (Applicant Tracking System)**
- **Target**: HR Managers, Hiring Managers, empresas en general
- **Funcionalidad**: Gestión de candidaturas, entrevistas, evaluaciones, hiring
- **Pricing**: Core product
- **Value prop**: "Gestiona tus procesos de selección de forma eficiente"

**Punto de integración**: CompanyCandidate (puede venir de Lead o aplicación directa)

---

## 📊 Modelo de Datos Completo (3 Niveles)

```
Lead (Head Hunting)
  ↓ [conversión manual]
CompanyCandidate (ATS - Account)
  ↓ [aplicación a posición]
CompanyApplication (ATS - Opportunity)
```

---

## 1. Lead (Head Hunting Product)

**Prospecto sin consentimiento explícito - Solo datos públicos o con cesión GDPR**

```python
Lead:
  - id: UUID
  - company_id: UUID (FK → Company)
  - created_by_user_id: UUID (FK → CompanyUser)

  # Datos básicos (públicos o con cesión)
  - first_name: String
  - last_name: String
  - email: String
  - phone: String (nullable)
  - linkedin_url: String (nullable)
  - current_company: String (nullable)
  - current_position: String (nullable)
  - location: String (nullable)

  # Sourcing info
  - source: Enum [linkedin, referral, github, twitter, conference, other]
  - source_url: String (nullable - link al perfil original)
  - tags: Array[String] (privados de la empresa)
  - internal_notes: Text (privados)
  - priority: Enum [low, medium, high]

  # GDPR Compliance ⚖️
  - gdpr_compliant: Boolean (empresa confirma base legal)
  - gdpr_compliance_note: Text (nullable - ej: "Cesión de datos de cliente X")
  - candidate_notified: Boolean (si se envió notificación)
  - candidate_notified_at: DateTime (nullable)
  - notification_token: String (nullable - para link de respuesta)
  - candidate_response: Enum [pending, accepted, rejected, no_response] (nullable)
  - candidate_response_at: DateTime (nullable)

  # Estado del lead
  - status: Enum [new, contacted, interested, not_interested, converted, archived]
  - contacted_at: DateTime (nullable)
  - converted_to_candidate_id: UUID (FK → CompanyCandidate, nullable)
  - converted_at: DateTime (nullable)

  # Workflow de prospección
  - workflow_id: UUID (FK → CompanyWorkflow, nullable)
  - current_stage_id: UUID (FK → WorkflowStage, nullable)

  # Resume (con restricciones)
  - resume_url: String (nullable - S3 path)
  - resume_uploaded_at: DateTime (nullable)

  # Timestamps
  - created_at: DateTime
  - updated_at: DateTime
  - archived_at: DateTime (soft delete)
```

### Restricciones de Negocio

**Para subir CV (`resume_url`)**:
- ❌ Prohibido si: `candidate_notified = false` AND `gdpr_compliant = false`
- ✅ Permitido si: `gdpr_compliant = true` (cesión de datos)
- ✅ Permitido si: `candidate_notified = true` AND `candidate_response = accepted`

**Para convertir a Candidato**:
- ❌ Prohibido si: `candidate_response = rejected`
- ⚠️ Warning si: `candidate_notified = false` AND `gdpr_compliant = false`
- ✅ Permitido si: `candidate_response = accepted` OR `gdpr_compliant = true`

---

## 2. CompanyCandidate (ATS Product)

**Candidato confirmado - Ya sea convertido de Lead o aplicación directa**

```python
CompanyCandidate:
  - id: UUID
  - company_id: UUID (FK → Company)
  - candidate_id: UUID (FK → Candidate, nullable - si está registrado en plataforma)
  - created_by_user_id: UUID (FK → CompanyUser)
  - lead_id: UUID (FK → Lead, nullable - si vino de conversión)

  # Datos básicos (copiados del Lead o de aplicación)
  - first_name: String
  - last_name: String
  - email: String
  - phone: String (nullable)
  - country: String (nullable)
  - linkedin_url: String (nullable)

  # Origen
  - source: Enum [lead_conversion, direct_application, referral, manual_entry]
  - source_details: Text (nullable)

  # Datos de gestión CRM
  - tags: Array[String] (privados)
  - internal_notes: Text (privados)
  - position_interest: String (nullable)
  - department: String (nullable)
  - priority: Enum [low, medium, high]
  - salary_expectation: String (nullable)
  - availability: String (nullable)

  # Estado
  - status: Enum [active, in_process, offer_made, hired, rejected, archived]

  # Workflow (para candidatos sin aplicación específica)
  - workflow_id: UUID (FK → CompanyWorkflow, nullable)
  - current_stage_id: UUID (FK → WorkflowStage, nullable)

  # Resume
  - resume_url: String (nullable - S3 path)
  - resume_uploaded_by: Enum [company, candidate] (nullable)
  - resume_uploaded_at: DateTime (nullable)

  # Timestamps
  - created_at: DateTime
  - updated_at: DateTime
  - archived_at: DateTime (soft delete)
```

---

## 3. Position (Posición/Vacante)

```python
Position:
  - id: UUID
  - company_id: UUID (FK → Company)
  - title: String (ej: "Senior Backend Developer")
  - description: Text
  - department: String (nullable)
  - location: String
  - employment_type: Enum [full_time, part_time, contract, internship, temporary]
  - remote_type: Enum [on_site, remote, hybrid]
  - salary_range_min: Decimal (nullable)
  - salary_range_max: Decimal (nullable)
  - salary_currency: String (ej: "USD", "EUR")
  - requirements: Text
  - responsibilities: Text
  - benefits: Text (nullable)
  - status: Enum [draft, active, paused, closed, cancelled]
  - is_public: Boolean (si se muestra en job board público)
  - workflow_id: UUID (FK → CompanyWorkflow, nullable - workflow por defecto)
  - created_by_user_id: UUID (FK → CompanyUser)
  - published_at: DateTime (nullable)
  - closed_at: DateTime (nullable)
  - created_at: DateTime
  - updated_at: DateTime
```

---

## 4. CompanyApplication (Candidatura Formal)

```python
CompanyApplication:
  - id: UUID
  - company_candidate_id: UUID (FK → CompanyCandidate)
  - candidate_id: UUID (FK → Candidate, required - debe estar registrado)
  - company_id: UUID (FK → Company)
  - position_id: UUID (FK → Position)

  # Workflow de selección
  - workflow_id: UUID (FK → CompanyWorkflow, nullable)
  - current_stage_id: UUID (FK → WorkflowStage, nullable)

  # Datos compartidos por candidato (autorización explícita)
  - shared_data: JSON
    {
      "basic_info": bool,        # nombre, email, teléfono, país, linkedin
      "education": bool,         # títulos académicos
      "experience": bool,        # experiencia laboral
      "projects": bool,          # proyectos
      "skills": bool,            # habilidades
      "certifications": bool,    # certificaciones
      "languages": bool,         # idiomas
      "resume_url": string       # CV específico para esta aplicación
    }

  # Estado de la candidatura
  - status: Enum [active, offer_made, accepted, rejected, withdrawn, archived]
  - applied_at: DateTime
  - source: Enum [direct_application, invitation_response, referral, linkedin]

  # Datos de seguimiento
  - tags: Array[String]
  - internal_notes: Text
  - priority: Enum [low, medium, high]
  - salary_offered: Decimal (nullable)

  # Timestamps
  - created_at: DateTime
  - updated_at: DateTime
  - archived_at: DateTime (soft delete)
```

---

## 5. Entidades de Soporte

### CandidateComment (Comentarios)

```python
CandidateComment:
  - id: UUID
  - lead_id: UUID (FK → Lead, nullable)
  - company_candidate_id: UUID (FK → CompanyCandidate, nullable)
  - company_application_id: UUID (FK → CompanyApplication, nullable)
  # Solo UNO de los tres debe estar presente

  - author_user_id: UUID (FK → CompanyUser)
  - comment: Text
  - visibility: Enum [internal, shared_with_candidate]
  - context: String (nullable - ej: "interview", "screening", "review")
  - created_at: DateTime
  - updated_at: DateTime
  - deleted_at: DateTime (soft delete)
```

### LeadNotification (Notificaciones de Lead)

```python
LeadNotification:
  - id: UUID
  - lead_id: UUID (FK → Lead)
  - email: String
  - token: String (único para respuesta)
  - status: Enum [sent, opened, accepted, rejected, expired]
  - sent_at: DateTime
  - opened_at: DateTime (nullable)
  - responded_at: DateTime (nullable)
  - expires_at: DateTime (now + 30 días)
```

---

## 🔄 Flujos de Negocio Completos

### Flujo 1: Head Hunting - Agregar Lead

```
┌─────────────────────────────────────────────────────────┐
│ 1. Recruiter encuentra perfil en LinkedIn              │
│    - Nombre: John Doe                                   │
│    - Email: john@example.com (público)                  │
│    - LinkedIn: linkedin.com/in/johndoe                  │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 2. Click "Agregar Lead" en dashboard Head Hunting      │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 3. Sistema muestra formulario:                          │
│                                                          │
│    Nombre: [John Doe                ]                   │
│    Email:  [john@example.com        ]                   │
│    Tel:    [                        ] (opcional)        │
│    LinkedIn: [linkedin.com/in/...   ]                   │
│    Source: [LinkedIn ▼]                                 │
│    Tags: [Python, Senior, Remote    ]                   │
│    Notes: [Found via search "python senior"  ]          │
│                                                          │
│    ┌─ GDPR Compliance ─────────────────────────┐       │
│    │                                             │       │
│    │ ☐ Cumplo con GDPR (cesión de datos)       │       │
│    │   Nota: [______________________]           │       │
│    │                                             │       │
│    │ ☐ Notificar al candidato                   │       │
│    │   Se enviará email solicitando consent     │       │
│    └─────────────────────────────────────────────┘       │
│                                                          │
│    [ Cancelar ]  [ Guardar Lead ]                       │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 4. Recruiter marca "Notificar al candidato" y guarda   │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 5. Sistema crea Lead:                                   │
│    - status = new                                       │
│    - candidate_notified = true                          │
│    - gdpr_compliant = false                             │
│    - candidate_response = pending                       │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 6. Sistema envía email a john@example.com:             │
│                                                          │
│    Subject: "Empresa X está interesada en tu perfil"   │
│                                                          │
│    Hola John,                                           │
│                                                          │
│    La empresa X ha agregado tu perfil...               │
│                                                          │
│    [ Aceptar ]  [ Rechazar ]                            │
│                                                          │
│    Link: /lead-response/abc123token                     │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 7. Lead visible en dashboard Head Hunting              │
│    Badge: ⏳ Notificación pendiente                     │
└─────────────────────────────────────────────────────────┘
```

---

### Flujo 2: Lead acepta notificación

```
┌─────────────────────────────────────────────────────────┐
│ 1. John recibe email y hace click en "Aceptar"         │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 2. Redirect a /lead-response/abc123token                │
│                                                          │
│    ┌─────────────────────────────────────────┐         │
│    │  Empresa X - Consentimiento             │         │
│    │                                          │         │
│    │  ✓ Acepto que Empresa X gestione        │         │
│    │    mi perfil para oportunidades         │         │
│    │                                          │         │
│    │  [ Confirmar ]                           │         │
│    └─────────────────────────────────────────┘         │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 3. Sistema actualiza Lead:                              │
│    - candidate_response = accepted                      │
│    - candidate_response_at = now                        │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 4. Sistema envía email al recruiter:                    │
│    "John Doe aceptó ser contactado"                     │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 5. Dashboard Head Hunting actualiza badge:             │
│    Badge: ✅ Aceptado                                    │
│    Ahora puede: subir CV, convertir a candidato        │
└─────────────────────────────────────────────────────────┘
```

---

### Flujo 3: Recruiter intenta subir CV sin compliance

```
┌─────────────────────────────────────────────────────────┐
│ 1. Recruiter tiene Lead sin notificar:                  │
│    - candidate_notified = false                         │
│    - gdpr_compliant = false                             │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 2. Click "Subir CV" en detalle del Lead                │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 3. Sistema muestra advertencia:                         │
│                                                          │
│    ⚠️  Advertencia Legal                                │
│                                                          │
│    No puedes subir CV sin consentimiento del candidato │
│    o sin base legal GDPR.                               │
│                                                          │
│    Opciones:                                            │
│                                                          │
│    ○ Notificar al candidato                             │
│      Se enviará email solicitando consentimiento.      │
│      Podrás subir CV cuando acepte.                    │
│                                                          │
│    ○ Tengo cesión de datos GDPR                         │
│      Confirmo que tengo base legal (ej: cesión de      │
│      cliente, contrato previo, etc.)                   │
│      Nota obligatoria: [_____________]                 │
│                                                          │
│    [ Cancelar ]  [ Continuar ]                          │
└─────────────────────────────────────────────────────────┘
                          ↓
        ┌────────────────┴────────────────┐
        │                                  │
   Opción A:                          Opción B:
   Notificar                          GDPR Compliant
        │                                  │
        ↓                                  ↓
┌─────────────────┐            ┌─────────────────────┐
│ Envía email     │            │ Marca Lead:         │
│ Lead.candidate_ │            │ gdpr_compliant=true │
│ notified = true │            │ Puede subir CV      │
│ Debe esperar    │            │ inmediatamente      │
└─────────────────┘            └─────────────────────┘
```

---

### Flujo 4: Convertir Lead a Candidato

```
┌─────────────────────────────────────────────────────────┐
│ 1. Recruiter tiene Lead con status = interested        │
│    Badge: ✅ Aceptado o 🛡️ GDPR Compliant               │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 2. Click "Convertir a Candidato"                        │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 3. Sistema valida:                                      │
│    - ¿candidate_response = accepted?                    │
│    - O ¿gdpr_compliant = true?                          │
│                                                          │
│    Si NO → Error: "Requiere consentimiento o GDPR"     │
└─────────────────────────────────────────────────────────┘
                          ↓ (si pasa validación)
┌─────────────────────────────────────────────────────────┐
│ 4. Modal de confirmación:                               │
│                                                          │
│    Convertir John Doe a Candidato                       │
│                                                          │
│    Se creará un CompanyCandidate en tu ATS.            │
│    Se copiarán los datos del Lead.                      │
│    El Lead quedará marcado como "convertido".          │
│                                                          │
│    [ Cancelar ]  [ Convertir ]                          │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 5. Sistema crea CompanyCandidate:                       │
│    - source = lead_conversion                           │
│    - lead_id = ID del Lead                              │
│    - Copia: nombre, email, teléfono, linkedin          │
│    - Copia: resume_url (si existe)                      │
│    - resume_uploaded_by = company                       │
│    - status = active                                    │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 6. Sistema actualiza Lead:                              │
│    - status = converted                                 │
│    - converted_to_candidate_id = nuevo CompanyCandidate │
│    - converted_at = now                                 │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 7. Redirect a vista de CompanyCandidate en ATS         │
│    Banner: "Este candidato vino de Head Hunting"       │
│    [ Ver Lead Original ] (link)                         │
└─────────────────────────────────────────────────────────┘
```

---

### Flujo 5: Candidato aplica directamente (sin Lead previo)

```
┌─────────────────────────────────────────────────────────┐
│ 1. Candidato registrado ve posición pública            │
│    Position: "Senior Backend Developer"                │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 2. Click "Aplicar"                                      │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 3. Sistema muestra formulario de aplicación:           │
│                                                          │
│    Aplicar a: Senior Backend Developer                 │
│                                                          │
│    Datos a compartir:                                   │
│    ☑ Nombre, email, país                                │
│    ☐ Teléfono                                           │
│    ☐ LinkedIn                                           │
│                                                          │
│    Información adicional:                               │
│    ☐ Educación                                          │
│    ☐ Experiencia laboral                                │
│    ☑ Proyectos                                          │
│    ☑ Habilidades                                        │
│                                                          │
│    CV para esta aplicación:                             │
│    [ Upload PDF ] John_Doe_Resume_2025.pdf ✓           │
│                                                          │
│    [ Cancelar ]  [ Enviar Aplicación ]                  │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 4. Sistema verifica:                                    │
│    ¿Existe CompanyCandidate para esta company+candidate?│
│                                                          │
│    NO existe → Crear CompanyCandidate                   │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 5. Sistema crea CompanyCandidate:                       │
│    - source = direct_application                        │
│    - candidate_id = candidato actual                    │
│    - Copia datos básicos seleccionados                  │
│    - resume_url = CV subido                             │
│    - resume_uploaded_by = candidate                     │
│    - status = in_process                                │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 6. Sistema crea CompanyApplication:                     │
│    - company_candidate_id = CompanyCandidate creado    │
│    - position_id = posición aplicada                    │
│    - shared_data = permisos seleccionados en form      │
│    - status = active                                    │
│    - workflow_id = workflow de la Position             │
│    - current_stage_id = etapa inicial                   │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 7. Empresa ve nueva aplicación en ATS                  │
│    - Dashboard: New Applications (1)                    │
│    - Puede ver datos autorizados por candidato         │
└─────────────────────────────────────────────────────────┘
```

---

### Flujo 6: Candidato se registra después (Lead existente)

```
┌─────────────────────────────────────────────────────────┐
│ 1. Lead existe:                                          │
│    - email: john@example.com                            │
│    - candidate_notified = true                          │
│    - candidate_response = accepted                      │
│    - status = interested                                │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 2. John decide registrarse en la plataforma            │
│    - Ingresa: john@example.com                          │
│    - Completa onboarding                                │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 3. Sistema NO hace nada automáticamente:               │
│    ❌ NO vincula candidate_id al Lead                   │
│    ❌ NO notifica a John sobre el Lead                  │
│    ❌ NO notifica a la empresa                          │
│                                                          │
│    Razón: Head Hunting es producto separado            │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 4. Recruiter ve Lead aún sin candidate_id              │
│    - Puede buscar manualmente por email                │
│    - Puede convertir a Candidato (sigue flujo normal)  │
│    - Al convertir, puede vincular al Candidate si      │
│      empresa detecta que existe cuenta con ese email   │
└─────────────────────────────────────────────────────────┘
```

**Justificación**:
- Head Hunting es privado del recruiter
- Separación de productos
- No queremos que candidato sepa que está en sistema de prospección
- Solo se notifica cuando hay acción concreta (conversión, oferta)

---

## 📧 Templates de Email

### Email 1: Notificación a Lead

```html
Subject: La empresa {{company_name}} está interesada en tu perfil

Hola {{first_name}},

La empresa {{company_name}} ha agregado tu perfil a su sistema de gestión
de talento para futuras oportunidades laborales.

──────────────────────────────────────────────────────────────

Información que tienen:
  • Nombre: {{full_name}}
  • Email: {{email}}
  {{#if phone}}• Teléfono: {{phone}}{{/if}}
  {{#if linkedin_url}}• LinkedIn: {{linkedin_url}}{{/if}}
  • Fuente: {{source_display}}

──────────────────────────────────────────────────────────────

Tus opciones:

[ ✓ Aceptar ]
  → Permites que gestionen tu perfil
  → Podrán contactarte para oportunidades relevantes
  → Podrán guardar tu CV si lo proporcionas

[ ✗ Rechazar ]
  → Solicitas eliminación de tus datos
  → Eliminaremos tu información de nuestro sistema
  → No te contactaremos en el futuro

──────────────────────────────────────────────────────────────

Tus derechos bajo GDPR:
  • Derecho de acceso a tus datos
  • Derecho de rectificación
  • Derecho de supresión ("derecho al olvido")
  • Derecho de portabilidad de datos

Más información: {{privacy_policy_url}}

──────────────────────────────────────────────────────────────

Este enlace expira en 30 días.

{{company_name}}
{{company_email}}
```

### Email 2: Confirmación de Aceptación (al Lead)

```html
Subject: Has aceptado el contacto con {{company_name}}

Hola {{first_name}},

Gracias por aceptar que {{company_name}} gestione tu perfil.

✓ Tu información está ahora en nuestro sistema
✓ Te contactaremos cuando tengamos oportunidades relevantes
✓ Puedes revocar este consentimiento en cualquier momento

Si deseas actualizar tu información o ejercer tus derechos GDPR:
→ {{gdpr_portal_url}}

Saludos,
Equipo de {{company_name}}
```

### Email 3: Notificación al Recruiter (Lead aceptó)

```html
Subject: 🎉 {{lead_name}} aceptó ser contactado

Hola {{recruiter_name}},

¡Buenas noticias! {{lead_name}} ha aceptado que gestiones su perfil.

Ahora puedes:
  ✓ Subir su CV
  ✓ Contactarlo para oportunidades
  ✓ Convertirlo a Candidato cuando esté listo

[ Ver Lead ] → {{lead_url}}

──────────────────────────────────────────────────────────────

Sistema de Head Hunting
{{platform_name}}
```

### Email 4: Notificación al Recruiter (Lead rechazó)

```html
Subject: {{lead_name}} rechazó ser contactado

Hola {{recruiter_name}},

{{lead_name}} ha rechazado que gestiones su perfil.

Sus datos serán eliminados en 30 días según política GDPR.

¿Deseas exportar la información antes de la eliminación?
[ Exportar datos ] → {{export_url}}

──────────────────────────────────────────────────────────────

Sistema de Head Hunting
{{platform_name}}
```

---

## 🎨 Impacto en Frontend

### Producto 1: Head Hunting Dashboard

**URL**: `/company/headhunting`

**Layout**:
```
┌─────────────────────────────────────────────────────────┐
│  [Logo]  Head Hunting               [User ▼] [Help]    │
├─────────────────────────────────────────────────────────┤
│  [ + New Lead ]              [Search...] [Filters ▼]   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Tabs: [All] [New] [Contacted] [Interested] [Converted]│
│                                                          │
│  ┌────────────┬────────────┬────────────┬────────────┐ │
│  │   New      │ Contacted  │ Interested │ Converted  │ │
│  │   (15)     │    (8)     │    (5)     │   (12)     │ │
│  ├────────────┼────────────┼────────────┼────────────┤ │
│  │            │            │            │            │ │
│  │ [Card]     │ [Card]     │ [Card]     │ [Card]     │ │
│  │ John Doe   │ Jane Smith │ Bob Wilson │ Alice Lee  │ │
│  │ ⏳ Pending │ ✅ Accepted│ ✅ Accepted│ ✓ Done     │ │
│  │ LinkedIn   │ Referral   │ GitHub     │ LinkedIn   │ │
│  │ #Python    │ #Sales     │ #DevOps    │ #Manager   │ │
│  │            │            │            │            │ │
│  │ [Card]     │ [Card]     │            │            │ │
│  │ ...        │ ...        │            │            │ │
│  │            │            │            │            │ │
│  └────────────┴────────────┴────────────┴────────────┘ │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

**Acciones por Card**:
- Click → Ver detalle
- Drag & drop → Cambiar stage
- [ 📧 ] → Contactar
- [ 📎 ] → Upload CV (con validaciones)
- [ → ] → Convertir a Candidato
- [ 🗑️ ] → Archivar

**Badges en Cards**:
- ⏳ Notificación pendiente (`candidate_response = pending`)
- ✅ Aceptado (`candidate_response = accepted`)
- ❌ Rechazado (`candidate_response = rejected`)
- 🛡️ GDPR Compliant (`gdpr_compliant = true`)
- 📎 Tiene CV (`resume_url != null`)

---

### Producto 2: ATS Dashboard

**URL**: `/company/ats` o `/company/candidates`

**Layout**:
```
┌─────────────────────────────────────────────────────────┐
│  [Logo]  ATS - Candidates           [User ▼] [Help]    │
├─────────────────────────────────────────────────────────┤
│  [ + Add Candidate ]         [Search...] [Filters ▼]   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Tabs: [All] [Active] [In Process] [Hired] [Archived]  │
│                                                          │
│  ┌────────────┬────────────┬────────────┬────────────┐ │
│  │  Active    │ In Process │ Offer Made │   Hired    │ │
│  │   (20)     │    (12)    │    (3)     │    (8)     │ │
│  ├────────────┼────────────┼────────────┼────────────┤ │
│  │            │            │            │            │ │
│  │ [Card]     │ [Card]     │ [Card]     │ [Card]     │ │
│  │ John Doe   │ Jane Smith │ Bob Wilson │ Alice Lee  │ │
│  │ 🔄 From Lead│ 📝 Applied │ 📝 Applied │ 🎉 Done    │ │
│  │ Backend    │ Frontend   │ DevOps     │ Manager    │ │
│  │ 2 apps     │ 1 app      │ 1 app      │ -          │ │
│  │            │            │            │            │ │
│  └────────────┴────────────┴────────────┴────────────┘ │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

### Detalle de Lead (Head Hunting)

**URL**: `/company/headhunting/leads/:id`

```
┌─────────────────────────────────────────────────────────┐
│  ← Back to Head Hunting                                 │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  John Doe                          ✅ Aceptado          │
│  john@example.com                  🛡️ GDPR Compliant    │
│  linkedin.com/in/johndoe           📎 CV Subido         │
│                                                          │
│  [ Contactar ] [ Upload CV ] [ Convertir a Candidato ] │
│                                                          │
├─────────────────────────────────────────────────────────┤
│  Tabs: [ Overview ] [ Comments ] [ History ]           │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Overview:                                              │
│                                                          │
│  Información Básica                                     │
│  ├─ Nombre: John Doe                                    │
│  ├─ Email: john@example.com                             │
│  ├─ Teléfono: +34 600 000 000                           │
│  ├─ LinkedIn: linkedin.com/in/johndoe                   │
│  ├─ Empresa Actual: Tech Corp                           │
│  └─ Posición Actual: Senior Developer                   │
│                                                          │
│  Sourcing                                               │
│  ├─ Fuente: LinkedIn                                    │
│  ├─ URL Fuente: linkedin.com/in/johndoe                 │
│  ├─ Tags: Python, Senior, Remote                        │
│  ├─ Prioridad: High                                     │
│  └─ Creado por: Maria Garcia (01/12/2024)              │
│                                                          │
│  GDPR Compliance                                        │
│  ├─ GDPR Compliant: ✓ Sí                                │
│  ├─ Nota: "Cesión de datos de cliente TechClient SA"   │
│  ├─ Candidato Notificado: ✓ Sí (05/12/2024)            │
│  └─ Respuesta: Aceptado (06/12/2024)                    │
│                                                          │
│  Resume                                                 │
│  ├─ CV: john_doe_cv.pdf (2.3 MB)                        │
│  ├─ Subido: 07/12/2024                                  │
│  └─ [ Descargar ] [ Ver ]                               │
│                                                          │
│  Notas Internas                                         │
│  ┌────────────────────────────────────────────────┐    │
│  │ Perfil muy interesante para nuestro proyecto  │    │
│  │ de backend. Experiencia en Python/Django.     │    │
│  │ Disponibilidad: Inmediata                     │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 Impacto en Backend

### Módulos a Implementar

#### 1. Lead Module (NUEVO)

**Estructura**:
```
src/lead/
  application/
    commands/
      create_lead_command.py
      update_lead_command.py
      notify_lead_command.py
      mark_gdpr_compliant_command.py
      upload_resume_command.py (con validaciones)
      convert_to_candidate_command.py
      archive_lead_command.py
    queries/
      get_lead_by_id_query.py
      list_leads_by_company_query.py
      check_can_upload_resume_query.py
      check_can_convert_query.py
    dtos/
      lead_dto.py
      lead_list_dto.py
  domain/
    entities/
      lead.py
    value_objects/
      gdpr_compliance.py
    infrastructure/
      lead_repository_interface.py
    exceptions/
      lead_exceptions.py
  infrastructure/
    models/
      lead_model.py
      lead_notification_model.py
    repositories/
      lead_repository.py
  presentation/
    controllers/
      lead_controller.py
    schemas/
      lead_request.py
      lead_response.py
      lead_notification_request.py
    mappers/
      lead_mapper.py
```

**Endpoints**:
```python
# CRUD básico
POST   /api/company/{company_id}/leads
GET    /api/company/{company_id}/leads
GET    /api/leads/{lead_id}
PUT    /api/leads/{lead_id}
DELETE /api/leads/{lead_id}

# Acciones específicas
POST   /api/leads/{lead_id}/notify
POST   /api/leads/{lead_id}/mark-gdpr-compliant
POST   /api/leads/{lead_id}/upload-resume
POST   /api/leads/{lead_id}/convert-to-candidate
POST   /api/leads/{lead_id}/archive

# Validaciones
GET    /api/leads/{lead_id}/can-upload-resume
GET    /api/leads/{lead_id}/can-convert

# Endpoints públicos (sin auth)
GET    /api/public/lead-response/{token}
POST   /api/public/lead-response/{token}/accept
POST   /api/public/lead-response/{token}/reject
```

#### 2. CompanyCandidate Module (ACTUALIZAR)

**Cambios necesarios**:
- Añadir campo `lead_id` (FK → Lead, nullable)
- Añadir `source` enum con valor `lead_conversion`
- Actualizar CreateCompanyCandidateCommand para soportar conversión desde Lead
- Query para verificar si candidato ya existe por email

**Nuevo Command**:
```python
@dataclass(frozen=True)
class CreateCandidateFromLeadCommand(Command):
    lead_id: str
    # Los datos se copian del Lead automáticamente
```

#### 3. Position Module (YA PLANEADO)

Sin cambios adicionales.

#### 4. CompanyApplication Module (YA PLANEADO)

Sin cambios adicionales.

#### 5. File Storage Service (NUEVO)

**Para gestión de PDFs en S3**:

```python
# src/shared/infrastructure/storage/s3_service.py

class S3Service:
    def upload_lead_resume(
        self,
        company_id: str,
        lead_id: str,
        file: UploadFile
    ) -> str:
        """
        Sube CV de lead a S3
        Path: s3://bucket/company/{company_id}/leads/{lead_id}/resume.pdf
        Returns: URL del archivo
        """
        pass

    def upload_candidate_resume(
        self,
        company_id: str,
        candidate_id: str,
        file: UploadFile
    ) -> str:
        """
        Sube CV de candidato a S3
        Path: s3://bucket/company/{company_id}/candidates/{candidate_id}/resume.pdf
        Returns: URL del archivo
        """
        pass

    def upload_application_resume(
        self,
        company_id: str,
        application_id: str,
        file: UploadFile
    ) -> str:
        """
        Sube CV específico de aplicación a S3
        Path: s3://bucket/company/{company_id}/applications/{application_id}/resume.pdf
        Returns: URL del archivo
        """
        pass

    def delete_file(self, file_url: str) -> bool:
        """Elimina archivo de S3"""
        pass

    def get_presigned_url(self, file_url: str, expires_in: int = 3600) -> str:
        """Genera URL firmada temporal para descarga"""
        pass
```

#### 6. Email Service (ACTUALIZAR)

**Nuevos templates**:
- `lead_notification.html` - Email al lead
- `lead_accepted.html` - Confirmación al lead
- `lead_rejected.html` - Confirmación de rechazo
- `recruiter_lead_accepted.html` - Notificación al recruiter
- `recruiter_lead_rejected.html` - Notificación al recruiter

---

## 📋 Migrations

### Migration 1: Create Lead Table

```python
"""Create lead table

Revision ID: xxx_create_lead_table
"""

def upgrade():
    # Create enum types
    op.execute("""
        CREATE TYPE lead_source AS ENUM (
            'linkedin', 'referral', 'github', 'twitter', 'conference', 'other'
        );
        CREATE TYPE lead_status AS ENUM (
            'new', 'contacted', 'interested', 'not_interested', 'converted', 'archived'
        );
        CREATE TYPE candidate_response AS ENUM (
            'pending', 'accepted', 'rejected', 'no_response'
        );
    """)

    # Create lead table
    op.create_table(
        'leads',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('company_id', sa.String(), nullable=False),
        sa.Column('created_by_user_id', sa.String(), nullable=False),
        sa.Column('first_name', sa.String(100), nullable=False),
        sa.Column('last_name', sa.String(100), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('phone', sa.String(50), nullable=True),
        sa.Column('linkedin_url', sa.String(500), nullable=True),
        sa.Column('current_company', sa.String(200), nullable=True),
        sa.Column('current_position', sa.String(200), nullable=True),
        sa.Column('location', sa.String(200), nullable=True),
        sa.Column('source', sa.Enum('lead_source'), nullable=False),
        sa.Column('source_url', sa.String(500), nullable=True),
        sa.Column('tags', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('internal_notes', sa.Text(), nullable=True),
        sa.Column('priority', sa.String(20), nullable=False, server_default='medium'),
        sa.Column('gdpr_compliant', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('gdpr_compliance_note', sa.Text(), nullable=True),
        sa.Column('candidate_notified', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('candidate_notified_at', sa.DateTime(), nullable=True),
        sa.Column('notification_token', sa.String(255), nullable=True, unique=True),
        sa.Column('candidate_response', sa.Enum('candidate_response'), nullable=True),
        sa.Column('candidate_response_at', sa.DateTime(), nullable=True),
        sa.Column('status', sa.Enum('lead_status'), nullable=False, server_default='new'),
        sa.Column('contacted_at', sa.DateTime(), nullable=True),
        sa.Column('converted_to_candidate_id', sa.String(), nullable=True),
        sa.Column('converted_at', sa.DateTime(), nullable=True),
        sa.Column('workflow_id', sa.String(), nullable=True),
        sa.Column('current_stage_id', sa.String(), nullable=True),
        sa.Column('resume_url', sa.String(500), nullable=True),
        sa.Column('resume_uploaded_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('archived_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['created_by_user_id'], ['company_users.id']),
        sa.ForeignKeyConstraint(['converted_to_candidate_id'], ['company_candidates.id']),
        sa.ForeignKeyConstraint(['workflow_id'], ['company_workflows.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['current_stage_id'], ['workflow_stages.id'], ondelete='SET NULL'),
    )

    # Indexes
    op.create_index('idx_leads_company_id', 'leads', ['company_id'])
    op.create_index('idx_leads_email', 'leads', ['email'])
    op.create_index('idx_leads_status', 'leads', ['status'])
    op.create_index('idx_leads_notification_token', 'leads', ['notification_token'])
    op.create_index('idx_leads_created_at', 'leads', ['created_at'])

def downgrade():
    op.drop_table('leads')
    op.execute("DROP TYPE lead_source;")
    op.execute("DROP TYPE lead_status;")
    op.execute("DROP TYPE candidate_response;")
```

### Migration 2: Update CompanyCandidate for Lead Integration

```python
"""Add lead_id to company_candidates

Revision ID: xxx_add_lead_id_to_candidates
"""

def upgrade():
    # Add lead_id column
    op.add_column('company_candidates',
        sa.Column('lead_id', sa.String(), nullable=True))

    # Add foreign key
    op.create_foreign_key(
        'fk_company_candidates_lead_id',
        'company_candidates', 'leads',
        ['lead_id'], ['id'],
        ondelete='SET NULL'
    )

    # Update source enum to include lead_conversion
    op.execute("""
        ALTER TYPE company_candidate_source
        ADD VALUE IF NOT EXISTS 'lead_conversion';
    """)

    # Add index
    op.create_index('idx_company_candidates_lead_id',
        'company_candidates', ['lead_id'])

def downgrade():
    op.drop_constraint('fk_company_candidates_lead_id',
        'company_candidates', type_='foreignkey')
    op.drop_column('company_candidates', 'lead_id')
    op.drop_index('idx_company_candidates_lead_id')
```

---

## ✅ Checklist de Implementación

### Backend - Fase 1: Lead Module Core
- [ ] Crear entidad Lead (domain/entities/lead.py)
- [ ] Crear LeadModel (infrastructure/models/lead_model.py)
- [ ] Crear LeadRepository interface + implementation
- [ ] Crear LeadDto
- [ ] Crear migration para tabla leads
- [ ] Ejecutar migration

### Backend - Fase 2: Lead Commands
- [ ] CreateLeadCommand + Handler
- [ ] UpdateLeadCommand + Handler
- [ ] NotifyLeadCommand + Handler (envía email)
- [ ] MarkGDPRCompliantCommand + Handler
- [ ] ArchiveLeadCommand + Handler
- [ ] Registrar handlers en container

### Backend - Fase 3: Lead Queries
- [ ] GetLeadByIdQuery + Handler
- [ ] ListLeadsByCompanyQuery + Handler
- [ ] CheckCanUploadResumeQuery + Handler
- [ ] CheckCanConvertQuery + Handler
- [ ] Registrar handlers en container

### Backend - Fase 4: Lead Conversion
- [ ] ConvertLeadToCandidateCommand + Handler
- [ ] Actualizar CompanyCandidate entity para soportar lead_id
- [ ] Migration para añadir lead_id a company_candidates
- [ ] Ejecutar migration

### Backend - Fase 5: Lead Controller & Router
- [ ] LeadController con todos los métodos
- [ ] LeadRouter con todos los endpoints
- [ ] Schemas de request/response
- [ ] Mapper Lead ↔ DTO ↔ Response
- [ ] Registrar router en main.py

### Backend - Fase 6: Endpoints Públicos
- [ ] Public Lead Response Router
- [ ] GET /public/lead-response/:token (mostrar página)
- [ ] POST /public/lead-response/:token/accept
- [ ] POST /public/lead-response/:token/reject

### Backend - Fase 7: File Upload (S3)
- [ ] S3Service con métodos para upload
- [ ] UploadLeadResumeCommand + Handler (con validaciones GDPR)
- [ ] Endpoint POST /leads/:id/upload-resume
- [ ] Validar permisos antes de upload

### Backend - Fase 8: Email Templates
- [ ] Template: lead_notification.html
- [ ] Template: lead_accepted.html
- [ ] Template: lead_rejected.html
- [ ] Template: recruiter_lead_accepted.html
- [ ] Template: recruiter_lead_rejected.html
- [ ] Integrar con EmailService

### Frontend - Fase 1: Head Hunting Dashboard
- [ ] Página /company/headhunting
- [ ] Lista de Leads (tabla)
- [ ] Kanban de Leads (drag & drop)
- [ ] Filtros (status, source, priority, notified)
- [ ] Badges (notified, accepted, GDPR, has resume)

### Frontend - Fase 2: Lead Forms
- [ ] Modal "Add Lead"
- [ ] Checkbox GDPR Compliance
- [ ] Checkbox Notify Candidate
- [ ] Form validation
- [ ] Guardar Lead (POST /api/company/:id/leads)

### Frontend - Fase 3: Lead Detail
- [ ] Página /company/headhunting/leads/:id
- [ ] Tabs: Overview, Comments, History
- [ ] Botón "Upload CV" (con validaciones)
- [ ] Modal de advertencia GDPR
- [ ] Botón "Convert to Candidate"
- [ ] Modal de confirmación de conversión

### Frontend - Fase 4: Lead Actions
- [ ] Acción: Notify Lead (envía email)
- [ ] Acción: Mark GDPR Compliant (modal con textarea)
- [ ] Acción: Upload Resume (con validaciones frontend)
- [ ] Acción: Convert to Candidate (redirect a ATS)
- [ ] Acción: Archive Lead

### Frontend - Fase 5: Public Lead Response Page
- [ ] Página /lead-response/:token (pública)
- [ ] Mostrar info del lead y empresa
- [ ] Botones Aceptar/Rechazar
- [ ] Thank you page después de responder
- [ ] Error page si token inválido/expirado

### Frontend - Fase 6: ATS Integration
- [ ] Actualizar CompanyCandidate detail para mostrar lead_id
- [ ] Banner: "Este candidato vino de Head Hunting"
- [ ] Link "Ver Lead Original" (si lead_id presente)
- [ ] Badge en lista de candidatos si vino de Lead

### Frontend - Fase 7: Services
- [ ] leadService.ts (todos los métodos API)
- [ ] Tipos TypeScript para Lead
- [ ] Hooks: useLeads, useLeadDetail
- [ ] React Query para caching

### Testing - Fase 1: Backend Unit Tests
- [ ] Tests para Lead entity
- [ ] Tests para LeadRepository
- [ ] Tests para Commands (Create, Update, Notify, etc.)
- [ ] Tests para Queries
- [ ] Tests para conversion logic

### Testing - Fase 2: Backend Integration Tests
- [ ] Test: Crear Lead → Notificar → Aceptar → Convertir
- [ ] Test: Crear Lead → Intentar subir CV sin GDPR (debe fallar)
- [ ] Test: Crear Lead con GDPR → Subir CV (debe funcionar)
- [ ] Test: Lead rechaza notificación → No se puede convertir

### Testing - Fase 3: Frontend Unit Tests
- [ ] Tests para LeadForm component
- [ ] Tests para LeadDetail component
- [ ] Tests para GDPR warning modal
- [ ] Tests para conversion flow

### Testing - Fase 4: E2E Tests
- [ ] E2E: Flujo completo Head Hunting
- [ ] E2E: Candidato responde a notificación
- [ ] E2E: Conversión Lead → Candidate → Application
- [ ] E2E: Upload CV con validaciones

### Compliance & Docs - Fase Final
- [ ] Audit GDPR compliance
- [ ] Privacy Policy actualizada
- [ ] Terms of Service actualizados
- [ ] Data Retention Policy (30 días para rechazados)
- [ ] Cronjob para eliminar leads rechazados después de 30 días
- [ ] Documentación de API (OpenAPI)
- [ ] User Guide para Recruiters
- [ ] Video tutorial Head Hunting

---

## 🎯 Preguntas Pendientes / Decisiones

### 1. ¿Qué pasa con un Lead después de 30 días sin respuesta?

**Opciones**:
- A) Se marca automáticamente como `no_response` pero se mantiene
- B) Se archiva automáticamente
- C) Se envía reminder email
- D) Queda en `pending` indefinidamente

**Recomendación**: A + opción de C (enviar reminder a los 15 días)

---

### 2. ¿Puede un Lead tener múltiples conversiones a Candidato?

**Escenario**: Lead se convierte, luego se archiva, luego recruiter quiere reactivarlo.

**Opciones**:
- A) Solo una conversión (campo `converted_to_candidate_id` único)
- B) Múltiples conversiones (tabla intermedia `lead_conversions`)

**Recomendación**: A (una sola conversión). Si se archiva, se puede reactivar el CompanyCandidate.

---

### 3. ¿Cómo manejar leads duplicados por email?

**Escenario**: Dos recruiters agregan al mismo lead con diferente email (ej: john@gmail.com vs john@company.com)

**Opciones**:
- A) Permitir duplicados (cada recruiter gestiona su lead)
- B) Validar email único por company (un lead por email)
- C) Sugerir al crear si existe lead similar

**Recomendación**: C (sugerir pero permitir crear si recruiter confirma)

---

### 4. ¿Workflows separados para Leads vs Candidates?

**Propuesta**:
- **Lead Workflows**: Prospección (New → Contacted → Interested → Converted)
- **Candidate Workflows**: Evaluación general (Active → Qualified → Ready)
- **Application Workflows**: Selección específica (Applied → Interview → Offer → Hired)

**Pregunta**: ¿Crear tipos de workflow diferentes?

**Recomendación**: Sí, añadir campo `workflow_type: Enum [lead, candidate, application]`

---

### 5. ¿Sistema de puntuación/scoring para Leads?

**Feature**: Lead scoring automático basado en:
- Fuente (LinkedIn = 80, Referral = 100, etc.)
- Respuesta (Aceptó = +50, Rechazó = -100)
- Engagement (Abrió emails, visitó páginas)

**Pregunta**: ¿Implementar en V1 o V2?

**Recomendación**: V2 (nice to have, no crítico)

---

## 📊 Resumen Final

### Modelo de Datos
✅ **3 niveles**: Lead → CompanyCandidate → CompanyApplication
✅ **2 productos**: Head Hunting (Lead) + ATS (Candidate/Application)
✅ **GDPR compliant**: Checkbox + notificaciones + restricciones
✅ **S3 para PDFs**: Paths separados por entidad

### Flujos Clave
✅ Agregar Lead (con opciones GDPR)
✅ Notificar Lead (email con token)
✅ Lead responde (acepta/rechaza)
✅ Upload CV (con validaciones)
✅ Convertir a Candidato
✅ Candidato aplica (con autorización de datos)

### Compliance
✅ Lead puede rechazar
✅ Datos se eliminan en 30 días
✅ Audit trail completo
✅ Emails transaccionales

### Siguiente Paso
Revisar este documento, resolver preguntas pendientes, y comenzar implementación por fases.
