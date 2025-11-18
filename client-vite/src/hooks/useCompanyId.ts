import { useMemo } from 'react';

/**
 * Custom hook to get the current company ID from the JWT token
 * Memoized to prevent unnecessary recalculations
 * 
 * @returns The company ID from the token, or null if not found
 */
export function useCompanyId(): string | null {
  return useMemo(() => {
    const token = localStorage.getItem('access_token');
    if (!token) return null;
    
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return payload.company_id || null;
    } catch {
      return null;
    }
  }, []);
}

