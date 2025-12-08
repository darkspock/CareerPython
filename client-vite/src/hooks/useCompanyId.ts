import { useState } from 'react';

export function useCompanyId(): string | null {
  const [companyId] = useState<string | null>(() => {
    const token = localStorage.getItem('access_token');
    if (!token) return null;
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return payload.company_id;
    } catch {
      return null;
    }
  });
  return companyId;
}
