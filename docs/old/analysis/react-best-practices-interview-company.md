# Análisis de Buenas Prácticas de React - Company e Interview

## Resumen Ejecutivo

Este documento analiza los componentes del cliente relacionados con **Company** e **Interview** comparándolos con las mejores prácticas de React según la documentación oficial de React.dev.

## Archivos Analizados

- `client-vite/src/pages/company/CompanyInterviewDetailPage.tsx`
- `client-vite/src/pages/company/CompanyInterviewsPage.tsx`
- `client-vite/src/pages/company/CreateInterviewPage.tsx`
- `client-vite/src/pages/company/EditInterviewPage.tsx`

---

## 🔴 Problemas Críticos Encontrados

### 1. **Falta de Custom Hooks para Lógica Reutilizable**

**Problema**: Los componentes tienen lógica duplicada que debería estar en custom hooks.

**Ejemplo en `CompanyInterviewsPage.tsx`**:
```typescript
// ❌ Lógica duplicada en múltiples componentes
const getCompanyId = () => {
  const token = localStorage.getItem('access_token');
  if (!token) return null;
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    return payload.company_id;
  } catch {
    return null;
  }
};
```

**Mejora según React.dev**:
```typescript
// ✅ Custom hook reutilizable
function useCompanyId() {
  return useMemo(() => {
    const token = localStorage.getItem('access_token');
    if (!token) return null;
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return payload.company_id;
    } catch {
      return null;
    }
  }, []);
}
```

**Referencia**: [React.dev - Custom Hooks](https://react.dev/learn/reusing-logic-with-custom-hooks)

---

### 2. **useEffect sin Dependencias Correctas**

**Problema**: Varios `useEffect` tienen dependencias faltantes o incorrectas.

**Ejemplo en `CompanyInterviewDetailPage.tsx`**:
```typescript
// ❌ Falta dependencia de loadInterview y loadScoreSummary
useEffect(() => {
  if (interviewId) {
    loadInterview();
    loadScoreSummary();
  }
}, [interviewId]); // loadInterview y loadScoreSummary no están en dependencias
```

**Mejora según React.dev**:
```typescript
// ✅ Funciones memoizadas con useCallback
const loadInterview = useCallback(async () => {
  if (!interviewId) return;
  // ... lógica
}, [interviewId]);

const loadScoreSummary = useCallback(async () => {
  if (!interviewId) return;
  // ... lógica
}, [interviewId]);

useEffect(() => {
  if (interviewId) {
    loadInterview();
    loadScoreSummary();
  }
}, [interviewId, loadInterview, loadScoreSummary]);
```

**Referencia**: [React.dev - Effect Dependencies](https://react.dev/learn/lifecycle-of-reactive-effects)

---

### 3. **Componentes Demasiado Grandes (Violación de Single Responsibility)**

**Problema**: `CompanyInterviewsPage.tsx` tiene más de 1100 líneas con múltiples responsabilidades:
- Gestión de estado
- Lógica de filtrado
- Renderizado de tabla
- Renderizado de calendario
- Manejo de estadísticas

**Mejora según React.dev**:
```typescript
// ✅ Separar en componentes más pequeños
function CompanyInterviewsPage() {
  const { interviews, loading, error, filters, setFilters } = useInterviews();
  
  return (
    <div>
      <InterviewStats stats={stats} onFilterClick={handleFilterByMetric} />
      <InterviewFilters filters={filters} onChange={setFilters} />
      <InterviewCalendar onDateClick={handleDateClick} />
      <InterviewTable interviews={interviews} />
    </div>
  );
}
```

**Referencia**: [React.dev - Component Composition](https://react.dev/learn/describing-the-ui)

---

### 4. **Falta de Memoización de Funciones y Valores**

**Problema**: Funciones y valores calculados se recrean en cada render.

**Ejemplo en `CompanyInterviewsPage.tsx`**:
```typescript
// ❌ Se recrea en cada render
const formatDate = (dateString?: string) => {
  // ... lógica
};

const getStatusBadge = (status: string) => {
  // ... lógica
};
```

**Mejora según React.dev**:
```typescript
// ✅ Memoizar funciones con useCallback
const formatDate = useCallback((dateString?: string) => {
  // ... lógica
}, []);

// ✅ Memoizar valores calculados con useMemo
const statusBadges = useMemo(() => {
  return interviews.reduce((acc, interview) => {
    acc[interview.id] = getStatusBadge(interview.status);
    return acc;
  }, {} as Record<string, JSX.Element>);
}, [interviews]);
```

**Referencia**: [React.dev - useCallback](https://react.dev/reference/react/useCallback), [React.dev - useMemo](https://react.dev/reference/react/useMemo)

---

### 5. **Lógica de Negocio Mezclada con Presentación**

**Problema**: Los componentes tienen lógica de negocio que debería estar en custom hooks.

**Ejemplo en `CreateInterviewPage.tsx`**:
```typescript
// ❌ Lógica de validación y transformación en el componente
const handleToggleRole = (roleId: string) => {
  const currentRoles = formData.required_roles || [];
  // ... 20+ líneas de lógica compleja
};
```

**Mejora según React.dev**:
```typescript
// ✅ Extraer a custom hook
function useInterviewForm() {
  const [formData, setFormData] = useState<CreateInterviewRequest>({...});
  
  const handleToggleRole = useCallback((roleId: string) => {
    // ... lógica
  }, [formData.required_roles]);
  
  return { formData, handleToggleRole, ... };
}

// Componente solo se enfoca en presentación
function CreateInterviewPage() {
  const { formData, handleToggleRole, ... } = useInterviewForm();
  // ... solo JSX
}
```

**Referencia**: [React.dev - Separating Events from Effects](https://react.dev/learn/separating-events-from-effects)

---

### 6. **Falta de Manejo de Cleanup en useEffect**

**Problema**: Algunos efectos no manejan correctamente la limpieza de recursos.

**Ejemplo en `CompanyInterviewsPage.tsx`**:
```typescript
// ✅ Bien implementado - tiene cleanup
useEffect(() => {
  let ignore = false;
  
  async function loadFilterOptions() {
    // ... lógica
    if (!ignore) {
      setPositionMap(positionMapData);
    }
  }
  
  loadFilterOptions();
  
  return () => {
    ignore = true;
  };
}, []);
```

**Pero falta en otros lugares**:
```typescript
// ❌ No tiene cleanup para prevenir race conditions
useEffect(() => {
  loadCalendarData();
}, []);
```

**Mejora**:
```typescript
// ✅ Con cleanup
useEffect(() => {
  let ignore = false;
  
  async function loadCalendarData() {
    try {
      setCalendarLoading(true);
      const calendarData = await companyInterviewService.getInterviewCalendar(...);
      if (!ignore) {
        setCalendarInterviews(calendarData);
      }
    } catch (err) {
      if (!ignore) {
        console.error('Error loading calendar data:', err);
      }
    } finally {
      if (!ignore) {
        setCalendarLoading(false);
      }
    }
  }
  
  loadCalendarData();
  
  return () => {
    ignore = true;
  };
}, []);
```

**Referencia**: [React.dev - Custom Hook Example](https://react.dev/learn/reusing-logic-with-custom-hooks#example-use-data-hook)

---

### 7. **Funciones Helper No Memoizadas**

**Problema**: Funciones helper se recrean en cada render, causando re-renders innecesarios.

**Ejemplo en `CompanyInterviewsPage.tsx`**:
```typescript
// ❌ Se recrea en cada render
const getInterviewsForDate = (date: Date): number => {
  return calendarInterviews.filter(interview => {
    // ... lógica
  }).length;
};
```

**Mejora**:
```typescript
// ✅ Memoizar con useMemo
const interviewsByDate = useMemo(() => {
  const map = new Map<string, number>();
  calendarInterviews.forEach(interview => {
    if (interview.scheduled_at) {
      const dateKey = new Date(interview.scheduled_at).toDateString();
      map.set(dateKey, (map.get(dateKey) || 0) + 1);
    }
  });
  return map;
}, [calendarInterviews]);

const getInterviewsForDate = useCallback((date: Date): number => {
  return interviewsByDate.get(date.toDateString()) || 0;
}, [interviewsByDate]);
```

---

## 🟡 Problemas Moderados

### 8. **Falta de Extracción de Componentes Pequeños**

**Problema**: Componentes grandes con JSX repetitivo que debería ser componentes separados.

**Ejemplo en `CompanyInterviewsPage.tsx`**:
```typescript
// ❌ Todo en un solo componente
{interviews.map((interview) => (
  <TableRow key={interview.id}>
    {/* 100+ líneas de JSX */}
  </TableRow>
))}
```

**Mejora**:
```typescript
// ✅ Componente separado
function InterviewTableRow({ interview, onView, onCopyLink }) {
  return (
    <TableRow>
      {/* JSX específico */}
    </TableRow>
  );
}

// Uso
{interviews.map((interview) => (
  <InterviewTableRow 
    key={interview.id} 
    interview={interview}
    onView={handleViewInterview}
    onCopyLink={handleCopyLink}
  />
))}
```

**Referencia**: [React.dev - Component Composition](https://react.dev/learn/describing-the-ui)

---

### 9. **Falta de useCallback para Handlers**

**Problema**: Handlers de eventos se recrean en cada render.

**Ejemplo en `CompanyInterviewsPage.tsx`**:
```typescript
// ❌ Se recrea en cada render
const handleSearch = () => {
  setCurrentPage(1);
  loadInterviews();
};
```

**Mejora**:
```typescript
// ✅ Memoizado con useCallback
const handleSearch = useCallback(() => {
  setCurrentPage(1);
  loadInterviews();
}, [loadInterviews]);
```

**Referencia**: [React.dev - Memoize Returned Functions](https://react.dev/reference/react/useCallback#memoize-returned-functions-from-custom-react-hooks)

---

### 10. **Estado Duplicado**

**Problema**: Estado que podría derivarse de otros estados.

**Ejemplo en `CreateInterviewPage.tsx`**:
```typescript
// ❌ Estado duplicado
const [selectedInterviewerIds, setSelectedInterviewerIds] = useState<string[]>([]);
const [formData, setFormData] = useState<CreateInterviewRequest>({
  interviewers: [],
});
```

**Mejora**:
```typescript
// ✅ Un solo source of truth
const [formData, setFormData] = useState<CreateInterviewRequest>({
  interviewers: [],
});

// Derivar de formData
const selectedInterviewerIds = formData.interviewers || [];
```

---

## ✅ Buenas Prácticas Encontradas

### 1. **Uso Correcto de Cleanup en useEffect**
```typescript
// ✅ Bien implementado en CompanyInterviewsPage.tsx
useEffect(() => {
  let ignore = false;
  // ... async logic
  return () => {
    ignore = true;
  };
}, []);
```

### 2. **Separación de Concerns en Algunos Lugares**
```typescript
// ✅ Servicios separados
import { companyInterviewService } from '../../services/companyInterviewService';
```

### 3. **Manejo de Estados de Loading y Error**
```typescript
// ✅ Estados bien manejados
const [loading, setLoading] = useState(true);
const [error, setError] = useState<string | null>(null);
```

---

## 📋 Recomendaciones Prioritarias

### Prioridad Alta 🔴

1. **Crear Custom Hook `useInterviews`**
   - Extraer toda la lógica de fetching y estado
   - Similar a `useCompanies` y `usePositions` que ya existen
   - Usar `useCallback` para todas las funciones

2. **Crear Custom Hook `useCompanyId`**
   - Extraer lógica duplicada de `getCompanyId()`
   - Memoizar con `useMemo`

3. **Corregir Dependencias de useEffect**
   - Agregar todas las dependencias faltantes
   - Usar `useCallback` para funciones usadas en efectos

4. **Extraer Componentes Pequeños**
   - `InterviewTableRow`
   - `InterviewFilters`
   - `InterviewStats`
   - `InterviewCalendar`

### Prioridad Media 🟡

5. **Memoizar Funciones Helper**
   - `formatDate` → `useCallback`
   - `getStatusBadge` → `useMemo` o `useCallback`
   - `getInterviewsForDate` → `useMemo` + `useCallback`

6. **Crear Custom Hook `useInterviewForm`**
   - Para `CreateInterviewPage` y `EditInterviewPage`
   - Manejar validación y transformación de datos

7. **Optimizar Re-renders**
   - Usar `React.memo` en componentes hijos
   - Memoizar props que son objetos/funciones

### Prioridad Baja 🟢

8. **Extraer Constantes**
   - `interviewTypes`, `processTypes`, `interviewModes` → archivo separado

9. **Mejorar Tipado**
   - Crear tipos más específicos en lugar de `any`
   - Usar tipos derivados donde sea posible

10. **Documentación**
    - Agregar JSDoc a funciones complejas
    - Documentar custom hooks

---

## 📚 Referencias de React.dev

- [Reusing Logic with Custom Hooks](https://react.dev/learn/reusing-logic-with-custom-hooks)
- [useCallback Hook](https://react.dev/reference/react/useCallback)
- [useMemo Hook](https://react.dev/reference/react/useMemo)
- [Effect Dependencies](https://react.dev/learn/lifecycle-of-reactive-effects)
- [Component Composition](https://react.dev/learn/describing-the-ui)
- [Separating Events from Effects](https://react.dev/learn/separating-events-from-effects)

---

## 🎯 Ejemplo de Refactor Sugerido

### Antes (CompanyInterviewsPage.tsx - 1117 líneas)
```typescript
const CompanyInterviewsPage: React.FC = () => {
  // 50+ líneas de estado
  // 200+ líneas de lógica
  // 800+ líneas de JSX
};
```

### Después (Refactorizado)
```typescript
// hooks/useInterviews.ts
export function useInterviews(filters?: InterviewFilters) {
  // Toda la lógica de estado y fetching
}

// hooks/useCompanyId.ts
export function useCompanyId() {
  // Lógica de obtener company ID
}

// components/InterviewStats.tsx
export function InterviewStats({ stats, onFilterClick }) {
  // Solo presentación
}

// components/InterviewTable.tsx
export function InterviewTable({ interviews, onView, onCopyLink }) {
  // Solo presentación
}

// pages/company/CompanyInterviewsPage.tsx
const CompanyInterviewsPage: React.FC = () => {
  const companyId = useCompanyId();
  const { interviews, loading, error, ... } = useInterviews();
  
  return (
    <div>
      <InterviewStats stats={stats} onFilterClick={handleFilterByMetric} />
      <InterviewFilters filters={filters} onChange={setFilters} />
      <InterviewCalendar onDateClick={handleDateClick} />
      <InterviewTable interviews={interviews} />
    </div>
  );
};
```

---

## Conclusión

Los componentes de Company e Interview tienen **buena estructura general** pero necesitan refactorización para seguir las mejores prácticas de React:

1. ✅ **Bien**: Separación de servicios, manejo de estados básico
2. ❌ **Mejorar**: Extracción de lógica a custom hooks, memoización, componentes más pequeños
3. 🔄 **Prioridad**: Crear `useInterviews` hook similar a `useCompanies` y `usePositions`

El código actual es funcional pero puede mejorarse significativamente en términos de mantenibilidad, reutilización y rendimiento siguiendo las recomendaciones de React.dev.

