# Sistema de Flujos de Trabajo - Guía de Negocio

**Versión**: 1.0
**Fecha**: 2025-10-26

---

## Introducción

El Sistema de Flujos de Trabajo de CareerPython permite a las empresas gestionar todo el ciclo de vida de un candidato desde que entra en contacto con la empresa hasta que es contratado (o descartado). Este sistema es completamente personalizable y se adapta a las necesidades específicas de cada empresa y tipo de posición.

---

## Conceptos Principales

### ¿Qué es un Flujo de Trabajo?

Un flujo de trabajo es una **plantilla** que define las etapas por las que pasa un candidato durante el proceso de selección. Cada empresa puede crear múltiples flujos según sus necesidades.

**Ejemplos de flujos de trabajo:**
- **Contratación Estándar**: Screening → Entrevista RH → Entrevista Técnica → Entrevista Final → Oferta → Contratado
- **Contratación Técnica**: Revisión CV → Prueba Técnica → Entrevista Técnica → Entrevista con Líder → Reunión con CTO → Oferta → Contratado
- **Contratación Rápida**: Entrevista → Oferta → Contratado

### Tipos de Flujos de Trabajo

Existen dos tipos principales:

1. **Prospección (Sourcing)**: Para gestionar candidatos que aún no han aplicado a una posición específica
   - Búsqueda activa de talento
   - Head hunting
   - Gestión de leads
   - Pool de talento

2. **Selección (Evaluation)**: Para gestionar candidatos que ya aplicaron a una posición específica
   - Proceso de entrevistas
   - Evaluaciones técnicas
   - Negociación de oferta
   - Pre-onboarding

---

## El Flujo Completo: De Candidato a Empleado

### 1. Sourcing - Captación y Screening

Esta es la primera fase donde se identifican y filtran candidatos potenciales.

**Etapas típicas:**
- **Pendiente**: Candidato recién ingresado al sistema
- **Screening**: Revisión inicial del perfil
- **Descartado**: No cumple requisitos mínimos
- **En Espera**: Buen perfil pero sin vacante inmediata
- **A Pool de Talento**: Candidatos destacados que se guardan para futuras oportunidades

**Características:**
- Este flujo NO es personalizable (por ahora)
- Es el punto de entrada de todos los candidatos
- Los candidatos pueden venir de diferentes fuentes:
  - Aplicación directa a la web
  - Ingreso manual por el equipo de RH
  - Referencias
  - Head hunting

**Información capturada:**
- Datos básicos del candidato
- CV/Resume
- Fuente de reclutamiento
- Notas iniciales
- Prioridad del candidato

**Resultado:**
- Los candidatos **aceptados** pasan al siguiente flujo (Evaluation)
- Los candidatos descartados quedan registrados con motivo
- Los candidatos en pool quedan disponibles para futuras posiciones

### 2. Evaluation - Proceso de Selección

Una vez que un candidato es aceptado en el Sourcing (o aplica directamente a una posición), entra al flujo de evaluación.

**Etapas personalizables:**
Cada empresa define sus propias etapas según el tipo de posición. Ejemplos:

- **Entrevista con RH**: Primera entrevista para validar fit cultural
- **Prueba Técnica**: Evaluación de habilidades específicas
- **Entrevista Técnica**: Entrevista en profundidad con el equipo técnico
- **Entrevista con Gerente**: Validación final con el responsable del área
- **Referencias**: Validación de referencias laborales
- **Negociación**: Discusión de condiciones y expectativas

**Características:**
- Cada etapa puede tener:
  - Duración estimada (ej: 3 días)
  - Fecha límite obligatoria (ej: 5 días máximo)
  - Costo estimado (para calcular costo total de contratación)
  - Responsables asignados
  - Plantilla de email automático
  - Campos personalizados para capturar información

**Información capturada:**
- Resultados de evaluaciones
- Notas de entrevistadores
- Calificaciones
- Comentarios internos
- Documentos adjuntos
- Información específica según campos personalizados

### 3. Offer and Pre-Onboarding - Oferta y Preparación

La última fase del proceso donde se formaliza la contratación.

**Etapas personalizables:**
- **Propuesta de Oferta**: Se prepara la oferta inicial
- **Negociación**: Se discuten términos y condiciones
- **Envío de Documentos**: Candidato envía documentación requerida
- **Verificación de Documentos**: Validación de la documentación
- **Firma de Contrato**: Formalización de la relación laboral

**Características:**
- Este flujo también es personalizable
- Se pueden definir fechas límite para cada etapa
- Se puede automatizar el envío de documentos

---

## Gestión de Etapas

### ¿Qué se puede configurar en cada etapa?

Cada etapa del flujo puede ser configurada con gran detalle:

#### 1. Información Básica
- **Nombre**: Cómo se llamará la etapa (ej: "Entrevista Técnica")
- **Descripción**: Qué sucede en esta etapa
- **Tipo**: Inicial, Intermedia, Final o Personalizada
- **Orden**: Posición en el flujo

#### 2. Temporalidad
- **Duración Estimada**: Cuánto tiempo suele tomar esta etapa (ej: 5 días)
- **Fecha Límite**: Tiempo máximo para completar la etapa (ej: 7 días)
  - Esto ayuda a priorizar tareas
  - Se calculan automáticamente alertas por vencimiento

#### 3. Responsabilidades
- **Roles Predeterminados**: Qué roles deberían manejar esta etapa
  - Ejemplos: "Reclutador", "Líder Técnico", "Gerente de RH"
- **Personas Asignadas**: Usuarios específicos siempre asignados
  - Útil cuando una persona siempre debe estar involucrada

#### 4. Comunicación
- **Plantilla de Email**: Email automático que se envía al candidato
  - Se puede personalizar con variables (nombre, posición, etc.)
- **Texto Adicional**: Mensaje específico adicional para incluir en el email
- **Variables Disponibles**:
  - Nombre del candidato
  - Título de la posición
  - Nombre de la empresa
  - Nombre de la etapa
  - Texto personalizado

#### 5. Costos
- **Costo Estimado**: Costo de realizar esta etapa
  - Útil para calcular el costo total de contratación
  - Ejemplo: costo de pruebas técnicas, entrevistas, verificaciones

#### 6. Campos Personalizados

Cada flujo puede tener campos personalizados para capturar información específica:

**Tipos de campos:**
- **Texto**:
  - Texto corto
  - Texto largo (área de texto)
- **Respuestas Fijas**:
  - Lista desplegable
  - Casillas de verificación
  - Botones de radio
- **Fecha y Hora**:
  - Fecha y hora completa
  - Solo hora
- **Archivo**: Para adjuntar documentos
- **Números**:
  - Moneda (ej: expectativa salarial)
  - Entero
  - Decimal
  - Porcentaje

**Configuración de campos por etapa:**
Cada campo puede tener diferentes comportamientos según la etapa:
- **Oculto**: No se muestra en esta etapa
- **Obligatorio**: Debe llenarse para avanzar
- **Recomendado**: Se sugiere llenarlo pero no es obligatorio
- **Opcional**: Se puede llenar si se desea

**Ejemplo práctico:**
Campo: "Expectativa Salarial"
- En Screening: Oculto
- En Primera Entrevista: Recomendado
- En Negociación: Obligatorio
- En Oferta Final: Opcional (ya se negoció)

---

## Asignación de Responsables

### ¿Cómo se asignan personas a las etapas?

Cuando se crea una **posición vacante**, se debe:

1. **Seleccionar un flujo de trabajo** de las plantillas disponibles
2. **Asignar usuarios a cada etapa** del flujo

**Ejemplo:**
```
Posición: "Desarrollador Python Senior"
Flujo: "Contratación Técnica" (6 etapas)

Asignaciones:
- Etapa 1 (Screening RH)        → María (Reclutadora)
- Etapa 2 (Prueba Técnica)      → Juan (Líder Técnico), Ana (Desarrolladora Senior)
- Etapa 3 (Entrevista Técnica)  → Juan (Líder Técnico), Ana (Desarrolladora Senior)
- Etapa 4 (Entrevista con CTO)  → Carlos (CTO)
- Etapa 5 (Verificación)        → María (Reclutadora)
- Etapa 6 (Oferta)              → María (Reclutadora), Carlos (CTO)
```

**Características:**
- Se pueden asignar **múltiples personas** a la misma etapa (trabajo colaborativo)
- Las personas pueden **cambiarse en cualquier momento**
- Solo las personas asignadas pueden **mover candidatos** a la siguiente etapa
- Los administradores siempre pueden ver todo (pero no mover candidatos a menos que estén asignados)

---

## Sistema de Tareas

### ¿Cómo saben los usuarios qué tienen que hacer?

Cada usuario tiene un **tablero de tareas** personalizado que muestra:

### 1. Tareas Asignadas Directamente
Candidatos en etapas donde el usuario está específicamente asignado.

### 2. Tareas Disponibles por Rol
Candidatos en etapas que coinciden con los roles del usuario pero aún no tienen persona asignada.

**Ejemplo:**
- María tiene rol "Reclutadora"
- Hay 5 candidatos en etapa "Screening RH" (que requiere rol "Reclutadora")
- María ve esas 5 tareas como "disponibles"
- María puede "reclamar" una tarea para trabajarla
- Una vez reclamada, solo María puede procesarla

### Priorización de Tareas

Las tareas se priorizan automáticamente según:

1. **Fecha límite de la etapa**:
   - Vencida (pasó la fecha límite): +50 puntos de prioridad
   - Vence hoy: +30 puntos
   - Vence en 1-2 días: +20 puntos
   - Vence en 3-5 días: +10 puntos
   - Vence en 6+ días: 0 puntos

2. **Prioridad de la posición**: 0-5 estrellas
   - Multiplica por 10 (0-50 puntos)
   - Útil para posiciones críticas o urgentes

3. **Prioridad del candidato**: 0-5 estrellas
   - Multiplica por 5 (0-25 puntos)
   - Útil para candidatos excepcionales

**Prioridad Total = 100 (base) + fecha límite + posición + candidato**

**Puntuación máxima posible: 225**

### Visualización de Tareas

En el tablero, cada tarea muestra:
- **Nombre y foto del candidato**
- **Posición a la que aplica**
- **Etapa actual**
- **Indicador de prioridad** (color):
  - Rojo: Alta prioridad (175+)
  - Naranja: Media-Alta (150-174)
  - Amarillo: Media (125-149)
  - Gris: Normal (<125)
- **Fecha límite** con indicador de urgencia
- **Tiempo en la etapa**
- **Acciones rápidas**: Ver, Reclamar, Mover a siguiente etapa

---

## Comunicación con Candidatos

### Sistema de Mensajes Pseudo-Chat

El sistema permite comunicación bidireccional entre empresa y candidato:

**¿Cómo funciona?**

1. **Empresa envía mensaje al candidato**:
   - El mensaje se guarda en el sistema
   - Se envía un **email de notificación** al candidato
   - El email incluye un botón "Ver Conversación"

2. **Candidato recibe el email**:
   - Ve un resumen del mensaje
   - Hace clic en "Ver Conversación"
   - Es redirigido a la plataforma (debe iniciar sesión)

3. **Candidato responde en la plataforma**:
   - Ve todo el historial de conversación
   - Escribe su respuesta
   - La respuesta se guarda en el sistema
   - **NO se envía email a la empresa** (evita saturación)

4. **Empresa ve la respuesta**:
   - En su próximo ingreso, ve una notificación
   - Accede a la conversación
   - Puede responder (esto sí envía email al candidato)

**Importante:**
- Todas las respuestas deben hacerse **dentro de la plataforma**
- No se puede responder directamente al email
- Esto mantiene toda la comunicación organizada y trazable

### Emails Automáticos por Etapa

Cuando un candidato avanza a una nueva etapa, se puede enviar automáticamente un email si:
- La etapa tiene configurada una **plantilla de email**
- La plantilla se personaliza con los datos del candidato y posición
- Se puede agregar **texto adicional** específico para esa etapa

---

## Permisos y Visibilidad

### ¿Quién puede ver qué?

#### Usuarios de la Empresa:
- ✅ Pueden ver **todas las aplicaciones** de su empresa
- ✅ Pueden ver **todas las etapas** del flujo
- ✅ Pueden ver **el detalle** de cualquier candidato
- ❌ Solo pueden **mover candidatos** en etapas donde estén asignados

#### Administradores de la Empresa:
- ✅ Pueden ver todo
- ✅ Pueden mover candidatos en cualquier etapa (tienen permiso especial)
- ✅ Pueden cambiar asignaciones de usuarios

#### Candidatos:
- ✅ Pueden ver **sus propias aplicaciones**
- ✅ Pueden ver el **nombre de la etapa actual**
- ✅ Pueden ver el **historial de etapas**
- ❌ No pueden ver **notas internas** o **comentarios privados**
- ❌ No pueden ver **quién está asignado** a las etapas

### Reglas de Movimiento de Candidatos

1. **Solo usuarios asignados pueden mover**: Un usuario solo puede avanzar/retroceder un candidato si está asignado a la etapa actual

2. **Solo movimientos adyacentes**: No se pueden saltar etapas
   - Si estás en etapa 2, solo puedes ir a etapa 1 (retroceder) o etapa 3 (avanzar)

3. **Etapas finales son terminales**: Las etapas marcadas como "final" no permiten avanzar
   - Ejemplos: "Contratado", "Rechazado", "Retirado"

---

## Análisis y Reportes

### Métricas Disponibles

El sistema permite analizar el desempeño de los flujos de trabajo:

#### Métricas por Flujo:
- **Tiempo promedio por etapa**: Cuánto tiempo pasan los candidatos en cada etapa
- **Tasa de conversión por etapa**: Qué porcentaje avanza de una etapa a otra
- **Total de aplicaciones**: Cuántos candidatos han usado este flujo
- **Candidatos activos**: Cuántos están actualmente en proceso
- **Candidatos contratados**: Cuántos completaron exitosamente
- **Candidatos rechazados**: Cuántos fueron descartados

#### Detección de Cuellos de Botella:
- Identifica etapas donde los candidatos se quedan más tiempo del esperado
- Útil para optimizar el proceso

#### Análisis de Costos:
- **Costo por contratación**: Suma de los costos de todas las etapas
- **Costo promedio por flujo**: Ayuda a presupuestar
- **ROI de contratación**: Comparar costo vs. valor del empleado

#### Visualizaciones:
- Embudo de conversión (funnel)
- Gráficas de tiempo por etapa
- Línea de tiempo de costos
- Tablas de cuellos de botella

---

## Casos de Uso Prácticos

### Caso 1: Contratación de Desarrollador

**Contexto:**
- Empresa de tecnología busca un Desarrollador Python Senior
- Proceso técnico riguroso
- Múltiples entrevistadores

**Flujo utilizado:** "Contratación Técnica"

**Etapas y Responsables:**
1. **Screening RH** (3 días) → María (Reclutadora)
2. **Prueba Técnica** (7 días) → Juan y Ana (Equipo Dev)
3. **Entrevista Técnica** (5 días) → Juan y Ana
4. **Entrevista con Líder** (5 días) → Juan
5. **Entrevista con CTO** (5 días) → Carlos
6. **Oferta** (3 días) → María y Carlos

**Experiencia del candidato:**
- Aplica a la posición en la web
- Recibe email automático de confirmación
- María revisa el CV (2 días)
- Recibe email de invitación a prueba técnica
- Completa la prueba (5 días)
- Juan revisa la prueba y envía feedback
- Recibe invitación a entrevista técnica
- Realiza entrevista con Juan y Ana
- Recibe invitación a entrevista con CTO
- Realiza entrevista final
- Recibe oferta de empleo
- Negocia condiciones vía mensajes en la plataforma
- Acepta oferta

**Total: 28 días estimados**

### Caso 2: Contratación Urgente

**Contexto:**
- Reemplazo urgente por renuncia
- Proceso simplificado
- Decisión rápida

**Flujo utilizado:** "Contratación Rápida"

**Etapas:**
1. **Entrevista Inicial** (1 día) → María (RH) + Gerente del área
2. **Oferta** (1 día) → María

**Experiencia del candidato:**
- Aplica en la web
- Recibe llamada el mismo día
- Entrevista al día siguiente
- Recibe oferta 2 horas después
- Acepta la oferta

**Total: 2 días**

### Caso 3: Head Hunting

**Contexto:**
- Búsqueda activa de talento
- Candidato no aplicó, fue contactado
- Proceso de "cortejo"

**Flujo utilizado:** "Prospección" → "Contratación Técnica"

**Etapas de Prospección:**
1. **Identificación**: Reclutador encuentra perfil interesante en LinkedIn
2. **Primer Contacto**: Envía mensaje inicial
3. **Screening**: Llamada informal para conocer interés
4. **A Pool de Talento**: Candidato interesado pero no hay vacante aún

**6 meses después, se abre vacante:**
- Candidato pasa de "Pool de Talento" a "Evaluation"
- Comienza proceso de selección formal
- Sigue flujo "Contratación Técnica" estándar

---

## Beneficios del Sistema

### Para la Empresa:

1. **Estandarización**: Todos los candidatos siguen el mismo proceso
2. **Trazabilidad**: Se registra cada acción y decisión
3. **Colaboración**: Múltiples personas pueden trabajar en el proceso
4. **Automatización**: Emails automáticos ahorran tiempo
5. **Métricas**: Datos para mejorar el proceso continuamente
6. **Flexibilidad**: Cada posición puede tener su propio flujo
7. **Cumplimiento**: Historial completo para auditorías

### Para los Reclutadores:

1. **Claridad**: Saben exactamente qué deben hacer
2. **Priorización**: Las tareas urgentes se destacan automáticamente
3. **Organización**: Toda la información en un solo lugar
4. **Eficiencia**: Menos tiempo buscando información
5. **Seguimiento**: Alertas automáticas de vencimientos

### Para los Candidatos:

1. **Transparencia**: Saben en qué etapa están
2. **Comunicación**: Canal directo con la empresa
3. **Profesionalismo**: Proceso organizado y claro
4. **Rapidez**: Respuestas más rápidas
5. **Experiencia**: Mejor impresión de la empresa

---

## Preguntas Frecuentes

### ¿Puedo cambiar el flujo de una posición después de crearla?
Sí, pero solo afectará a las nuevas aplicaciones. Las aplicaciones existentes seguirán con el flujo original.

### ¿Qué pasa si elimino una etapa de un flujo?
No se puede eliminar una etapa si hay candidatos actualmente en ella. Primero debes mover a los candidatos a otra etapa.

### ¿Puedo tener diferentes flujos para diferentes tipos de posiciones?
Sí, ese es precisamente el objetivo. Por ejemplo: "Contratación Junior", "Contratación Senior", "Contratación Ejecutiva", etc.

### ¿Los candidatos pueden ver quién los está evaluando?
No, los candidatos solo ven el nombre de la etapa pero no quién está asignado ni los comentarios internos.

### ¿Qué pasa si un usuario sale de vacaciones?
Un administrador puede reasignar sus tareas a otra persona temporalmente. Cuando regrese, se le pueden devolver.

### ¿Se pueden hacer entrevistas en grupo?
Sí, puedes asignar múltiples personas a la misma etapa. Todos verán al candidato y pueden dejar comentarios.

### ¿Los campos personalizados son obligatorios?
Depende de cómo se configuren. Pueden ser obligatorios, recomendados u opcionales según la etapa.

### ¿Qué pasa con los candidatos que quedan en el pool de talento?
Quedan guardados en la base de datos y pueden ser contactados en el futuro para nuevas posiciones. Es como una "reserva" de buenos candidatos.

### ¿El sistema envía recordatorios de vencimientos?
Sí, cuando una tarea está próxima a vencer o ya venció, se destaca en color rojo/naranja en el tablero de tareas.

### ¿Puedo exportar reportes?
Sí, el sistema permite exportar reportes en CSV y PDF con las métricas de los flujos.

---

## Glosario de Términos

- **Flujo de Trabajo**: Plantilla que define las etapas del proceso de selección
- **Etapa**: Paso específico dentro de un flujo (ej: "Entrevista Técnica")
- **Candidato**: Persona que aplica o es propuesta para una posición
- **Aplicación**: Vínculo entre un candidato y una posición específica
- **Pool de Talento**: Reserva de candidatos destacados para futuras oportunidades
- **Sourcing**: Proceso de búsqueda y captación de candidatos
- **Screening**: Revisión inicial para filtrar candidatos
- **Evaluation**: Proceso de evaluación formal (entrevistas, pruebas)
- **Tarea**: Acción pendiente en el tablero de un usuario
- **Asignación**: Vínculo entre un usuario y una etapa
- **Prioridad**: Puntuación que determina la urgencia de una tarea
- **Fecha Límite**: Tiempo máximo para completar una etapa
- **Campo Personalizado**: Campo adicional para capturar información específica
- **Plantilla de Email**: Formato predefinido para emails automáticos

---

## Conclusión

El Sistema de Flujos de Trabajo de CareerPython es una herramienta poderosa y flexible que permite a las empresas gestionar su proceso de contratación de manera eficiente, organizada y transparente.

Su diseño modular permite adaptarse a cualquier tipo de empresa y proceso, desde contrataciones rápidas hasta procesos complejos con múltiples etapas y evaluadores.

La automatización de tareas repetitivas, la priorización inteligente y las métricas de desempeño ayudan a los equipos de RH a ser más productivos y efectivos, mientras que los candidatos disfrutan de un proceso más profesional y transparente.
