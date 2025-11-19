import { useMemo } from 'react';

export function useCompanyId(): string | null {
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
