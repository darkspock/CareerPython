import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import type { ReactNode } from 'react';
import { useParams } from 'react-router-dom';
import { api } from '../lib/api';

export interface CompanyInfo {
  id: string;
  name: string;
  slug: string;
  logo_url: string | null;
}

interface CompanyContextType {
  // Company info from URL slug
  company: CompanyInfo | null;
  companySlug: string | null;
  isLoading: boolean;
  error: string | null;

  // Helper functions
  getCompanyUrl: (path: string) => string;
  refreshCompany: () => Promise<void>;

  // For authenticated users - their company from token
  userCompanyId: string | null;
  userCompanySlug: string | null;
  isOwnCompany: boolean;
}

const CompanyContext = createContext<CompanyContextType | undefined>(undefined);

interface CompanyProviderProps {
  children: ReactNode;
}

/**
 * CompanyProvider - Provides company context from URL slug
 *
 * This provider:
 * 1. Extracts the company slug from the URL (e.g., /acme-corp/admin/...)
 * 2. Fetches company info from the API
 * 3. Compares with the authenticated user's company (if logged in)
 * 4. Provides helper functions for building company-scoped URLs
 */
export const CompanyProvider: React.FC<CompanyProviderProps> = ({ children }) => {
  const { companySlug: urlSlug } = useParams<{ companySlug: string }>();

  const [company, setCompany] = useState<CompanyInfo | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Get user's company info from JWT token
  const [userCompanyId, setUserCompanyId] = useState<string | null>(null);
  const [userCompanySlug, setUserCompanySlug] = useState<string | null>(null);

  // Extract user's company from JWT token
  useEffect(() => {
    try {
      const token = localStorage.getItem('access_token');
      if (token) {
        const payload = JSON.parse(atob(token.split('.')[1]));
        if (payload.company_id) {
          setUserCompanyId(payload.company_id);
          // Note: company_slug might need to be added to JWT payload
          // For now, we'll rely on fetching it or matching by ID
          setUserCompanySlug(payload.company_slug || null);
        }
      }
    } catch (e) {
      console.error('Failed to parse JWT token:', e);
    }
  }, []);

  // Fetch company info when URL slug changes
  const fetchCompany = useCallback(async () => {
    if (!urlSlug) {
      setCompany(null);
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const companyInfo = await api.getPublicCompanyInfo(urlSlug);
      setCompany(companyInfo);

      // If user has a company slug in token, update it
      if (userCompanyId && companyInfo.id === userCompanyId) {
        setUserCompanySlug(companyInfo.slug);
      }
    } catch (err: any) {
      console.error('Failed to fetch company:', err);
      setError(err.message || 'Company not found');
      setCompany(null);
    } finally {
      setIsLoading(false);
    }
  }, [urlSlug, userCompanyId]);

  useEffect(() => {
    fetchCompany();
  }, [fetchCompany]);

  // Helper to build company-scoped URLs
  const getCompanyUrl = useCallback((path: string): string => {
    const slug = urlSlug || userCompanySlug;
    if (!slug) {
      console.warn('No company slug available for URL generation');
      return path;
    }
    // Remove leading slash from path if present
    const cleanPath = path.startsWith('/') ? path.slice(1) : path;
    return `/${slug}/${cleanPath}`;
  }, [urlSlug, userCompanySlug]);

  // Refresh company data
  const refreshCompany = useCallback(async () => {
    await fetchCompany();
  }, [fetchCompany]);

  // Check if current company is the user's own company
  const isOwnCompany = !!(company && userCompanyId && company.id === userCompanyId);

  const value: CompanyContextType = {
    company,
    companySlug: urlSlug || null,
    isLoading,
    error,
    getCompanyUrl,
    refreshCompany,
    userCompanyId,
    userCompanySlug,
    isOwnCompany,
  };

  return (
    <CompanyContext.Provider value={value}>
      {children}
    </CompanyContext.Provider>
  );
};

/**
 * Hook to access company context
 *
 * Usage:
 * ```tsx
 * const { company, companySlug, getCompanyUrl } = useCompany();
 *
 * // Build a company-scoped URL
 * const candidatesUrl = getCompanyUrl('admin/candidates');
 * // Result: "/acme-corp/admin/candidates"
 * ```
 */
export const useCompany = (): CompanyContextType => {
  const context = useContext(CompanyContext);
  if (context === undefined) {
    throw new Error('useCompany must be used within a CompanyProvider');
  }
  return context;
};

/**
 * Hook to require company context - throws error if no company
 */
export const useRequiredCompany = (): CompanyContextType & { company: CompanyInfo } => {
  const context = useCompany();
  if (!context.company) {
    throw new Error('Company context is required but not available');
  }
  return context as CompanyContextType & { company: CompanyInfo };
};

export default CompanyContext;
