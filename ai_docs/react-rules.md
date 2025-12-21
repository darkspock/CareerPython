# React Rules and Best Practices

This document outlines the mandatory React patterns and rules for the CareerPython frontend.

## Rules of Hooks

Hooks must follow strict rules to ensure React can properly track component state.

### 1. Call Hooks at the Top Level

Hooks must be called at the top level of function components, before any conditional logic or early returns.

```javascript
// ✅ CORRECT: Hooks at top level
function Counter() {
  const [count, setCount] = useState(0);
  const [name, setName] = useState('');

  if (!isSpecial) {
    return null;  // Early return AFTER hooks
  }

  return <div>{name}: {count}</div>;
}

// ❌ WRONG: Hook after conditional
function Counter() {
  if (!isSpecial) {
    return null;
  }
  const [count, setCount] = useState(0);  // Hook after early return
}
```

### 2. Only Call Hooks from React Functions

Hooks must only be called from React function components or custom hooks.

```javascript
// ✅ CORRECT: Hook in component
function FriendList() {
  const [onlineStatus, setOnlineStatus] = useOnlineStatus();
}

// ✅ CORRECT: Hook in custom hook
function useWindowWidth() {
  const [width, setWidth] = useState(window.innerWidth);
  // ...
}

// ❌ WRONG: Hook in regular function
function setOnlineStatus() {
  const [onlineStatus, setOnlineStatus] = useOnlineStatus();
}
```

## Component Definition Rules

### 1. Define Components at Module Level

Components must be defined at the module level, not inside other components or functions.

```javascript
// ✅ CORRECT: Component at module level
function Component({ defaultValue }) {
  // ...
}

// ✅ CORRECT: Custom hook at module level
function useData(endpoint) {
  // ...
}

// ❌ WRONG: Component defined inside component
function Parent() {
  function Child() {
    // Creates new instance every render
  }
  return <Child />;
}

// ❌ WRONG: Factory function creating components
function createComponent(defaultValue) {
  return function Component() {
    // ...
  };
}
```

### 2. Never Create Hook Factories

Do not create functions that return hooks.

```javascript
// ❌ WRONG: Hook factory function
function createCustomHook(endpoint) {
  return function useData() {
    // ...
  };
}

// ✅ CORRECT: Pass configuration to hook
function useData(endpoint) {
  // Configuration as parameter
}
```

## Props and Hooks

### Never Pass Hooks as Props

Hooks should not be passed as props for dependency injection.

```javascript
// ❌ WRONG: Passing hook as prop
function ChatInput() {
  return <Button useData={useDataWithLogging} />;
}

// ✅ CORRECT: Use hook directly in component
function ChatInput() {
  return <Button />;
}

function Button() {
  const data = useDataWithLogging();
}
```

## Custom Hooks

### 1. Naming Convention

Custom hooks must start with the `use` prefix.

```javascript
// ✅ CORRECT
function useChatRoom({ roomId, serverUrl }) {
  // ...
}

// ❌ WRONG
function chatRoomConnection({ roomId, serverUrl }) {
  // ...
}
```

### 2. Encapsulate Reusable Logic

Use custom hooks to abstract complex logic from components.

```javascript
// Custom hook encapsulates connection logic
function useChatRoom({ roomId, serverUrl }) {
  useEffect(() => {
    const connection = createConnection(serverUrl, roomId);
    connection.connect();
    return () => connection.disconnect();
  }, [roomId, serverUrl]);
}

// Component stays clean and focused on rendering
export default function ChatRoom({ roomId }) {
  const [serverUrl, setServerUrl] = useState('https://localhost:1234');

  useChatRoom({
    roomId: roomId,
    serverUrl: serverUrl
  });

  return (
    <>
      <label>
        Server URL:
        <input value={serverUrl} onChange={e => setServerUrl(e.target.value)} />
      </label>
      <h1>Welcome to the {roomId} room!</h1>
    </>
  );
}
```

## The `use` Hook (React 19)

The `use` hook is special - it CAN be called conditionally, unlike other hooks.

```javascript
function Component({ isSpecial, shouldFetch, fetchPromise }) {
  // ✅ Standard hooks at top level
  const [count, setCount] = useState(0);
  const [name, setName] = useState('');

  if (!isSpecial) {
    return null;
  }

  if (shouldFetch) {
    // ✅ `use` can be conditional
    const data = use(fetchPromise);
    return <div>{data}</div>;
  }

  return <div>{name}: {count}</div>;
}
```

## Summary of Rules

| Rule | Description |
|------|-------------|
| Top-level hooks | Call hooks before any conditions or early returns |
| React functions only | Only call hooks from components or custom hooks |
| Module-level definitions | Define components at module level, not inside functions |
| No hook factories | Don't create functions that return hooks |
| No hooks as props | Don't pass hooks as props for dependency injection |
| `use` prefix | Custom hooks must start with `use` |
| `use` hook exception | The `use` hook can be called conditionally |

## Common Mistakes to Avoid

1. **Defining components inside other components** - Causes new instances on every render, performance problems, and state loss
2. **Calling hooks after early returns** - React cannot track hook state correctly
3. **Creating hook factories** - Breaks the rules of hooks
4. **Passing hooks as props** - Use hooks directly where needed
5. **Forgetting the `use` prefix** - React won't recognize it as a hook

## Session/Auth Management in localStorage

### Single Source of Truth Pattern

All session-related localStorage keys MUST be defined in a single location: `utils/jwt.ts`.

```typescript
// utils/jwt.ts - THE ONLY PLACE to define session keys
const SESSION_KEYS = [
  "access_token",
  "candidate_id",
  "job_position_id",
  "application_id",
  "wants_cv_help",
] as const;

export function clearAuthData(): void {
  SESSION_KEYS.forEach(key => localStorage.removeItem(key));
}
```

### Rules

| Rule | Description |
|------|-------------|
| Add keys to SESSION_KEYS | When adding new session-related localStorage items, add them to `SESSION_KEYS` in `utils/jwt.ts` |
| Use clearAuthData() | Always use `clearAuthData()` for logout/session cleanup, never manually remove individual keys |
| No scattered cleanup | Never write `localStorage.removeItem("access_token")` directly - use the centralized function |

### When to Clear Session

Always clear the session before:
- **Login flows** - Prevent mixing sessions
- **Verification links** - Ensure clean state regardless of who was logged in
- **Logout** - Complete cleanup

```typescript
// ✅ CORRECT: Use centralized function
import { clearAuthData } from "../utils/jwt";

function VerifyRegistrationPage() {
  useEffect(() => {
    clearAuthData();  // Clean slate before verification
    // ... verification logic
  }, []);
}

// ❌ WRONG: Manual removal (fragile, might miss keys)
function VerifyRegistrationPage() {
  useEffect(() => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("candidate_id");
    // Forgot job_position_id! Bug!
  }, []);
}
```

### Adding New Session Data

When you need to store new session-related data:

1. Add the key to `SESSION_KEYS` in `utils/jwt.ts`
2. Use `localStorage.setItem()` / `localStorage.getItem()` as normal
3. The key will automatically be cleared by `clearAuthData()`

```typescript
// Step 1: Add to SESSION_KEYS in utils/jwt.ts
const SESSION_KEYS = [
  "access_token",
  "candidate_id",
  "job_position_id",
  "application_id",
  "wants_cv_help",
  "new_session_data",  // ← Add new key here
] as const;

// Step 2: Use normally in your component
localStorage.setItem("new_session_data", value);
const data = localStorage.getItem("new_session_data");

// Step 3: It's automatically cleared by clearAuthData() - no extra work!
```
