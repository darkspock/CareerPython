# Nuevo flujo
El objetivo es reducir los tiempos de espera del usuario, necesitamos que el usuario no abandone la página.

1. Usuario introduce su email y PDF
http://localhost:5173/

2. Se lanza el proceso en la cola para analizar el PDF y al mismo tiempo se navega a:
http://localhost:5173/candidate/onboarding/complete-profile

3. Se muestra un mensaje con TOAST o similar: "Estamos analizando el PDF, mientras tanto vaya rellenando la información".

El botón de siguiente estará deshabilitado, con un contador de 60s a 0s. Con el texto "Analizando PDF",

4. Cuando el PDF se analiza se actualizan los datos de experencia y educación. SOLO ESOS. NO actualizar datos básicos.
5. El botón de siguiente se habilita.

## LISTA DE CAMBIOS PENDIENTES (Enero 2025)

### 🔄 Backend Changes Needed

1. **Fix Population Command** - `src/candidate/application/commands/populate_candidate_from_pdf_analysis.py`
   - ❌ CRÍTICO: Actualmente actualiza datos básicos (nombre, teléfono, email, etc.)
   - ✅ REQUERIDO: Solo actualizar experiencias y educación
   - Comentar/deshabilitar el método `_update_candidate_basic_info`
   - Mantener solo `_create_candidate_experiences` y `_create_candidate_educations`

2. **Navigation Response** - `presentation/candidate/controllers/onboarding_controller.py`
   - ❌ Actualmente devuelve success=true sin redirección
   - ✅ REQUERIDO: Devolver URL de redirección a `/candidate/onboarding/complete-profile`
   - Incluir `analysis_job_id` en respuesta para tracking

3. **User Creation** - `src/user/application/commands/create_user_from_landing.py`
   - ❌ Actualmente usa regex para extraer nombre que genera "JuanMaciasjmacias"
   - ✅ REQUERIDO: Partir el nombre si está en camelCase como el ejemplo. Usar `nameparser` os similar para separar nombre y apellidos correctamente. Extraer teléfono. Extrar Linkedin

### 🎨 Frontend Changes Needed

4. **Landing Page Navigation** - `client-vite/src/pages/LandingPage.tsx`
   - ❌ Actualmente se queda en la misma página después de submit
   - ✅ REQUERIDO: Navegar automáticamente a `/candidate/onboarding/complete-profile`
   - Pasar `analysis_job_id` como parámetro de URL o estado

5. **Complete Profile Page** - `client-vite/src/pages/CompleteProfilePage.tsx`
   - ❌ No existe lógica de análisis PDF
   - ✅ REQUERIDO: Implementar polling del `analysis_job_id`
   - Mostrar toast: "Estamos analizando el PDF, mientras tanto vaya rellenando la información"
   - Deshabilitar botón "Siguiente" con countdown 60s → 0s
   - Mostrar texto "Analizando PDF" en botón
   - Habilitar botón cuando análisis complete
   - Si termina de analizarse antes de los 60s habilitar botón y cambiar texto por "Siguiente"

6. **Job Status Polling** - `client-vite/src/lib/api.ts`
   - ❌ No existe endpoint para consultar estado de job
   - ✅ REQUERIDO: Agregar función `getJobStatus(jobId)`
   - Implementar polling cada 2-3 segundos
   - Backend: Crear endpoint GET `/jobs/{job_id}/status`

7. **Toast Notifications** - Frontend general
   - ✅ YA EXISTE: Sistema de toast implementado
   - ✅ REQUERIDO: Usar toast existente para mostrar progreso de análisis PDF
   - Mostrar mensaje: "Estamos analizando el PDF, mientras tanto vaya rellenando la información"
   - Confirmar cuando análisis complete

### 📊 Database/API Changes Needed

8. **Job Status Endpoint** - `presentation/candidate/routers/`
   - ✅ REQUERIDO: GET `/jobs/{job_id}/status` endpoint
   - Devolver: `{status, progress, message, completed_at, results}`
   - Usar `AsyncJobService` para consultar estado

9. **Profile Update Logic**
   - ❌ Actualmente se actualiza todo automáticamente
   - ✅ REQUERIDO: Solo pre-llenar experiencias/educación
   - Usuario debe poder editar datos básicos manualmente
   - Datos básicos no se sobreescriben

### ⚠️ Rollback Actions Required

10. **Revert Basic Info Updates**
    - El trabajo reciente (Enero 2025) hizo que se actualicen datos básicos
    - ESTO VIOLA LA ESPECIFICACIÓN del punto 4
    - Necesario revertir la lógica agresiva de actualización básica
    - Mantener solo experiencias y educación

### 🧪 Testing Needed

11. **End-to-End Flow Testing**
    - Probar flujo completo: Landing → Complete Profile
    - Verificar que solo se actualizan experiencias/educación
    - Verificar countdown y habilitación de botón
    - Probar con diferentes tipos de PDF

### 📝 Priority Order
1. **CRÍTICO**: Fix population command (punto 1)
2. **ALTO**: Navigation response (punto 2)
3. **ALTO**: Complete Profile polling (punto 5)
4. **MEDIO**: Frontend navigation (punto 4)
5. **MEDIO**: Job status endpoint (punto 8)
6. **BAJO**: Toast system (punto 7)
