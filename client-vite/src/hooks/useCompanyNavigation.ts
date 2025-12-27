import { useParams, useLocation } from 'react-router-dom';
import { useMemo } from 'react';

/**
 * Hook to provide company-aware navigation paths
 *
 * This hook detects whether we're using the new company-scoped routes
 * (/:companySlug/admin/*) or the legacy routes (/company/*) and
 * provides the correct base path for navigation.
 *
 * Usage:
 * ```tsx
 * const { basePath, getPath, isCompanyScoped, companySlug } = useCompanyNavigation();
 *
 * // Get a full path
 * const dashboardPath = getPath('dashboard'); // "/acme-corp/admin/dashboard" or "/company/dashboard"
 * ```
 */
export function useCompanyNavigation() {
  const { companySlug } = useParams<{ companySlug: string }>();
  const location = useLocation();

  // Determine if we're using company-scoped routes
  const isCompanyScoped = useMemo(() => {
    // Check if current path matches /:companySlug/admin pattern
    const pathParts = location.pathname.split('/').filter(Boolean);
    return pathParts.length >= 2 && pathParts[1] === 'admin';
  }, [location.pathname]);

  // Get the base path for navigation
  const basePath = useMemo(() => {
    if (isCompanyScoped && companySlug) {
      return `/${companySlug}/admin`;
    }
    return '/company';
  }, [isCompanyScoped, companySlug]);

  // Helper to build full paths
  const getPath = (path: string): string => {
    // Remove leading slash from path if present
    const cleanPath = path.startsWith('/') ? path.slice(1) : path;
    return `${basePath}/${cleanPath}`;
  };

  // Helper to check if a path is active
  const isActive = (path: string): boolean => {
    const fullPath = getPath(path);
    return location.pathname === fullPath || location.pathname.startsWith(fullPath + '/');
  };

  // Get login path
  const loginPath = useMemo(() => {
    if (isCompanyScoped && companySlug) {
      return `/${companySlug}/login`;
    }
    return '/company/login';
  }, [isCompanyScoped, companySlug]);

  return {
    basePath,
    getPath,
    isActive,
    isCompanyScoped,
    companySlug: companySlug || null,
    loginPath,
  };
}

export default useCompanyNavigation;
