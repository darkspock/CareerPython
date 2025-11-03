// Company authentication utilities
import { decodeJWTPayload } from './jwt';

export interface CompanyAuthInfo {
  userId: string;
  companyId: string;
  email?: string;
}

/**
 * Get company ID from JWT token
 */
export function getCompanyId(): string | null {
  const token = localStorage.getItem('access_token');
  if (!token) return null;
  
  try {
    const payload = decodeJWTPayload(token);
    return payload?.company_id || null;
  } catch {
    return null;
  }
}

/**
 * Get user ID from JWT token
 */
export function getUserId(): string | null {
  const token = localStorage.getItem('access_token');
  if (!token) return null;
  
  try {
    const payload = decodeJWTPayload(token);
    return payload?.sub || payload?.user_id || payload?.id || null;
  } catch {
    return null;
  }
}

/**
 * Get company authentication info (user ID and company ID)
 */
export function getCompanyAuthInfo(): CompanyAuthInfo | null {
  const token = localStorage.getItem('access_token');
  if (!token) return null;
  
  try {
    const payload = decodeJWTPayload(token);
    const userId = payload?.sub || payload?.user_id || payload?.id;
    const companyId = payload?.company_id;
    
    if (!userId || !companyId) {
      return null;
    }
    
    return {
      userId,
      companyId,
      email: payload?.email
    };
  } catch {
    return null;
  }
}

/**
 * Check if user has a specific permission
 * Note: This is a basic check. You may need to fetch permissions from API
 */
export function hasPermission(permission: string): boolean {
  const token = localStorage.getItem('access_token');
  if (!token) return false;
  
  try {
    const payload = decodeJWTPayload(token);
    // Check if token has permissions array or object
    const permissions = payload?.permissions;
    if (Array.isArray(permissions)) {
      return permissions.includes(permission);
    }
    if (typeof permissions === 'object' && permissions !== null) {
      return permissions[permission] === true;
    }
    return false;
  } catch {
    return false;
  }
}

