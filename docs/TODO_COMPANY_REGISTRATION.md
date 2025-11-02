# ⚠️ Pendientes: Registro de Empresas

## Estado Actual

✅ **Frontend:** Completado al 100%
- Landing page implementada
- Formulario de registro multi-step funcional
- Validaciones y manejo de errores
- Componentes y servicios creados

❌ **Backend:** Endpoints faltantes

---

## 🔴 CRÍTICO: Endpoints del Backend Faltantes

### 1. Endpoint de Registro Principal
**Frontend espera:** `POST /company/register`
**Estado:** ❌ No existe en el backend

**Endpoint actual del backend:**
- `POST /companies` - Requiere autenticación, solo crea empresa (no usuario)

**Acción requerida:**
Crear endpoint público `POST /company/register` que:
- Cree un nuevo usuario
- Cree una nueva empresa
- Asocie el usuario a la empresa
- Ejecute scripts de inicialización (flujos, roles)
- Opcionalmente incluya datos de ejemplo si `include_example_data: true`

**Request esperado:**
```typescript
{
  email: string;
  password: string;
  full_name: string;
  company_name: string;
  domain: string;
  logo_url?: string;
  contact_phone?: string;
  address?: string;
  include_example_data: boolean;
  accept_terms: boolean;
  accept_privacy: boolean;
}
```

**Response esperado:**
```typescript
{
  company_id: string;
  user_id: string;
  message: string;
  redirect_url?: string;
}
```

---

### 2. Endpoint para Vincular Usuario Existente
**Frontend espera:** `POST /company/register/link-user`
**Estado:** ❌ No existe en el backend

**Acción requerida:**
Crear endpoint público `POST /company/register/link-user` que:
- Autentique usuario existente (email + password)
- Cree nueva empresa
- Vincule usuario existente a la nueva empresa
- Ejecute scripts de inicialización

**Request esperado:**
```typescript
{
  email: string;
  password: string;
  company_name: string;
  domain: string;
  logo_url?: string;
  contact_phone?: string;
  address?: string;
  include_example_data: boolean;
  accept_terms: boolean;
  accept_privacy: boolean;
}
```

---

### 3. Endpoint para Verificar Email (Opcional)
**Frontend espera:** `GET /users/check-email?email={email}`
**Estado:** ❌ No existe en el backend (actualmente tiene fallback)

**Acción requerida:**
Crear endpoint público opcional `GET /users/check-email?email={email}` que:
- Verifique si el email ya está registrado
- Retorne si el usuario puede vincularse

**Response esperado:**
```typescript
{
  exists: boolean;
  can_link: boolean;
}
```

**Nota:** El frontend tiene fallback, así que este endpoint es opcional pero recomendado.

---

## 🟡 IMPORTANTE: Upload de Logo Durante Registro

**Estado actual:** ⚠️ Parcialmente implementado

**Problema:**
- El componente `CompanyDataForm` acepta un `onLogoUpload` handler
- Pero en `CompanyRegisterPage` NO se está pasando ningún handler
- Actualmente el logo se guarda como base64 (data URL) en `logo_url`
- Esto puede ser problemático para logos grandes (>5MB)

**Opciones:**

### Opción 1: Upload después del registro (Recomendado)
- Permitir que el usuario suba el logo después de crear la cuenta
- Usar el endpoint existente `POST /companies/{company_id}/upload-logo`

### Opción 2: Endpoint público para upload temporal
- Crear endpoint público que acepte logo y retorne URL temporal
- Usar esa URL en el request de registro
- Backend descarga y procesa el logo después

### Opción 3: Aceptar base64 directamente
- Backend acepta `logo_url` como base64
- Backend procesa y guarda el logo automáticamente
- Validar tamaño máximo en backend

**Acción recomendada:** Implementar Opción 1 o 3.

---

## 📋 Checklist de Implementación Backend

### Fase 1: Endpoint de Registro
- [ ] Crear router público `/company/register` (sin autenticación)
- [ ] Crear schema de request `CompanyRegistrationRequest`
- [ ] Crear schema de response `CompanyRegistrationResponse`
- [ ] Crear Command `RegisterCompanyWithUserCommand`
- [ ] Crear CommandHandler que:
  - [ ] Cree usuario nuevo
  - [ ] Cree empresa nueva
  - [ ] Vincule usuario a empresa (role principal)
  - [ ] Ejecute scripts de inicialización
  - [ ] Opcionalmente agregue datos de ejemplo
- [ ] Agregar validaciones (email único, dominio único)
- [ ] Manejo de errores

### Fase 2: Endpoint de Vinculación
- [ ] Crear router público `/company/register/link-user` (sin autenticación)
- [ ] Crear schema de request `LinkUserRequest`
- [ ] Crear Command `LinkUserToCompanyCommand`
- [ ] Crear CommandHandler que:
  - [ ] Autentique usuario existente
  - [ ] Cree empresa nueva
  - [ ] Vincule usuario existente a empresa
  - [ ] Ejecute scripts de inicialización
- [ ] Manejo de errores (credenciales inválidas, etc.)

### Fase 3: Endpoint de Verificación de Email (Opcional)
- [ ] Crear router público `/users/check-email`
- [ ] Crear Query `CheckEmailExistsQuery`
- [ ] Crear QueryHandler que verifique existencia
- [ ] Retornar si puede vincularse

### Fase 4: Manejo de Logo (Recomendado)
- [ ] Decidir estrategia (Opción 1, 2 o 3)
- [ ] Si Opción 1: Documentar flujo en frontend
- [ ] Si Opción 2: Crear endpoint público de upload temporal
- [ ] Si Opción 3: Validar base64 en backend y procesar

---

## 🧪 Testing Requerido

### Tests de Integración
- [ ] Test registro exitoso con usuario nuevo
- [ ] Test registro exitoso con datos de ejemplo
- [ ] Test registro fallido (email duplicado)
- [ ] Test registro fallido (dominio duplicado)
- [ ] Test vinculación exitosa de usuario existente
- [ ] Test vinculación fallida (credenciales inválidas)
- [ ] Test verificación de email existente
- [ ] Test verificación de email nuevo

### Tests de Scripts de Inicialización
- [ ] Verificar que se crean flujos por defecto
- [ ] Verificar que se crean roles por defecto
- [ ] Verificar datos de ejemplo (si se solicita)

---

## 📝 Notas Adicionales

1. **Scripts de Inicialización:**
   - Los scripts deben ejecutarse automáticamente después del registro
   - Verificar que funcionan correctamente
   - Documentar qué se crea por defecto

2. **Seguridad:**
   - Los endpoints de registro deben ser públicos (sin autenticación)
   - Pero deben tener rate limiting para prevenir spam
   - Validar todos los inputs del lado del servidor

3. **Mensajes de Error:**
   - El frontend espera mensajes en español para:
     - "Este dominio ya está en uso"
     - "Este email ya está registrado"
     - "Email o contraseña incorrectos"
   - Asegurar que el backend retorne mensajes claros

4. **Flujo Post-Registro:**
   - Después del registro exitoso, el usuario debe estar autenticado automáticamente
   - Redirigir al dashboard de la empresa
   - Mostrar mensaje de bienvenida

---

## 🎯 Prioridad

1. **🔴 ALTA:** Crear endpoint `POST /company/register`
2. **🟡 MEDIA:** Crear endpoint `POST /company/register/link-user`
3. **🟢 BAJA:** Crear endpoint `GET /users/check-email` (opcional)
4. **🟡 MEDIA:** Decidir y implementar estrategia de upload de logo

---

**Última actualización:** $(date)

