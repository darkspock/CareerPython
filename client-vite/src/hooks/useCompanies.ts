// Custom hook for managing companies
import { useState, useEffect, useCallback } from 'react';
import CompanyService from '../services/companyService';
import type {
  Company,
  CompanyFilters,
  CompanyStats,
  CreateCompanyRequest,
  UpdateCompanyRequest,
  CompanyListResponse
} from '../types/company';

export interface UseCompaniesOptions {
  initialFilters?: CompanyFilters;
  autoFetch?: boolean;
}

export interface UseCompaniesReturn {
  // Data
  companies: Company[];
  stats: CompanyStats | null;
  currentCompany: Company | null;

  // State
  loading: boolean;
  error: string | null;
  filters: CompanyFilters;

  // Pagination
  pagination: {
    total: number;
    page: number;
    pageSize: number;
    totalPages: number;
  };

  // Actions
  fetchCompanies: () => Promise<void>;
  fetchStats: () => Promise<void>;
  fetchCompanyById: (id: string) => Promise<void>;
  createCompany: (data: CreateCompanyRequest) => Promise<void>;
  updateCompany: (id: string, data: UpdateCompanyRequest) => Promise<void>;
  deleteCompany: (id: string) => Promise<void>;
  approveCompany: (id: string) => Promise<void>;
  rejectCompany: (id: string, reason: string) => Promise<void>;
  activateCompany: (id: string) => Promise<void>;
  deactivateCompany: (id: string) => Promise<void>;

  // Bulk actions
  bulkApprove: (ids: string[]) => Promise<void>;
  bulkReject: (ids: string[], reason: string) => Promise<void>;
  bulkActivate: (ids: string[]) => Promise<void>;
  bulkDeactivate: (ids: string[]) => Promise<void>;

  // Utility
  setFilters: (filters: CompanyFilters) => void;
  clearError: () => void;
  refresh: () => Promise<void>;
  exportData: (format?: 'csv' | 'excel') => Promise<void>;
}

export const useCompanies = (options: UseCompaniesOptions = {}): UseCompaniesReturn => {
  const { initialFilters = {}, autoFetch = true } = options;

  // State
  const [companies, setCompanies] = useState<Company[]>([]);
  const [stats, setStats] = useState<CompanyStats | null>(null);
  const [currentCompany, setCurrentCompany] = useState<Company | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFiltersState] = useState<CompanyFilters>({
    page: 1,
    page_size: 10,
    ...initialFilters
  });
  const [pagination, setPagination] = useState({
    total: 0,
    page: 1,
    pageSize: 10,
    totalPages: 0
  });

  // Actions
  const fetchCompanies = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      const response: CompanyListResponse = await CompanyService.getCompanies(filters);

      setCompanies(response.companies);
      setPagination({
        total: response.total,
        page: response.page,
        pageSize: response.page_size,
        totalPages: response.total_pages
      });
    } catch (err: any) {
      setError(err.message || 'Failed to fetch companies');
      setCompanies([]);
    } finally {
      setLoading(false);
    }
  }, [filters]);

  const fetchStats = useCallback(async () => {
    try {
      const statsData = await CompanyService.getCompanyStats();
      setStats(statsData);
    } catch (err: any) {
      console.error('Failed to fetch stats:', err);
      // Don't set error for stats fetch failure
    }
  }, []);

  const fetchCompanyById = useCallback(async (id: string) => {
    try {
      setLoading(true);
      setError(null);
      const company = await CompanyService.getCompanyById(id);
      setCurrentCompany(company);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch company');
      setCurrentCompany(null);
    } finally {
      setLoading(false);
    }
  }, []);

  const createCompany = useCallback(async (data: any) => {
    try {
      setLoading(true);
      setError(null);
      await CompanyService.createCompany(data);
      await fetchCompanies();
      await fetchStats();
    } catch (err: any) {
      setError(err.message || 'Failed to create company');
      throw err;
    } finally {
      setLoading(false);
    }
  }, [fetchCompanies, fetchStats]);

  const updateCompany = useCallback(async (id: string, data: UpdateCompanyRequest) => {
    try {
      setLoading(true);
      setError(null);
      await CompanyService.updateCompany(id, data);
      await fetchCompanies();
      await fetchStats();
    } catch (err: any) {
      setError(err.message || 'Failed to update company');
      throw err;
    } finally {
      setLoading(false);
    }
  }, [fetchCompanies, fetchStats]);

  const deleteCompany = useCallback(async (id: string) => {
    try {
      setLoading(true);
      setError(null);
      await CompanyService.deleteCompany(id);
      await fetchCompanies();
      await fetchStats();
    } catch (err: any) {
      setError(err.message || 'Failed to delete company');
      throw err;
    } finally {
      setLoading(false);
    }
  }, [fetchCompanies, fetchStats]);

  const approveCompany = useCallback(async (id: string) => {
    try {
      setLoading(true);
      setError(null);
      await CompanyService.approveCompany(id);
      await fetchCompanies();
      await fetchStats();
    } catch (err: any) {
      setError(err.message || 'Failed to approve company');
      throw err;
    } finally {
      setLoading(false);
    }
  }, [fetchCompanies, fetchStats]);

  const rejectCompany = useCallback(async (id: string, reason: string) => {
    try {
      setLoading(true);
      setError(null);
      await CompanyService.rejectCompany(id, reason);
      await fetchCompanies();
      await fetchStats();
    } catch (err: any) {
      setError(err.message || 'Failed to reject company');
      throw err;
    } finally {
      setLoading(false);
    }
  }, [fetchCompanies, fetchStats]);

  const activateCompany = useCallback(async (id: string) => {
    try {
      setLoading(true);
      setError(null);
      await CompanyService.activateCompany(id);
      await fetchCompanies();
      await fetchStats();
    } catch (err: any) {
      setError(err.message || 'Failed to activate company');
      throw err;
    } finally {
      setLoading(false);
    }
  }, [fetchCompanies, fetchStats]);

  const deactivateCompany = useCallback(async (id: string) => {
    try {
      setLoading(true);
      setError(null);
      await CompanyService.deactivateCompany(id);
      await fetchCompanies();
      await fetchStats();
    } catch (err: any) {
      setError(err.message || 'Failed to deactivate company');
      throw err;
    } finally {
      setLoading(false);
    }
  }, [fetchCompanies, fetchStats]);

  // Bulk actions
  const bulkApprove = useCallback(async (ids: string[]) => {
    try {
      setLoading(true);
      setError(null);
      await CompanyService.bulkApproveCompanies(ids);
      await fetchCompanies();
      await fetchStats();
    } catch (err: any) {
      setError(err.message || 'Failed to bulk approve companies');
      throw err;
    } finally {
      setLoading(false);
    }
  }, [fetchCompanies, fetchStats]);

  const bulkReject = useCallback(async (ids: string[], reason: string) => {
    try {
      setLoading(true);
      setError(null);
      await CompanyService.bulkRejectCompanies(ids, reason);
      await fetchCompanies();
      await fetchStats();
    } catch (err: any) {
      setError(err.message || 'Failed to bulk reject companies');
      throw err;
    } finally {
      setLoading(false);
    }
  }, [fetchCompanies, fetchStats]);

  const bulkActivate = useCallback(async (ids: string[]) => {
    try {
      setLoading(true);
      setError(null);
      await CompanyService.bulkActivateCompanies(ids);
      await fetchCompanies();
      await fetchStats();
    } catch (err: any) {
      setError(err.message || 'Failed to bulk activate companies');
      throw err;
    } finally {
      setLoading(false);
    }
  }, [fetchCompanies, fetchStats]);

  const bulkDeactivate = useCallback(async (ids: string[]) => {
    try {
      setLoading(true);
      setError(null);
      await CompanyService.bulkDeactivateCompanies(ids);
      await fetchCompanies();
      await fetchStats();
    } catch (err: any) {
      setError(err.message || 'Failed to bulk deactivate companies');
      throw err;
    } finally {
      setLoading(false);
    }
  }, [fetchCompanies, fetchStats]);

  // Utility functions
  const setFilters = useCallback((newFilters: CompanyFilters) => {
    setFiltersState(prev => ({ ...prev, ...newFilters }));
  }, []);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  const refresh = useCallback(async () => {
    await Promise.all([fetchCompanies(), fetchStats()]);
  }, [fetchCompanies, fetchStats]);

  const exportData = useCallback(async (format: 'csv' | 'excel' = 'csv') => {
    try {
      setLoading(true);
      const blob = await CompanyService.exportCompanies(filters, format);

      // Create download link
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `companies_export.${format}`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (err: any) {
      setError(err.message || 'Failed to export data');
      throw err;
    } finally {
      setLoading(false);
    }
  }, [filters]);

  // Effects
  useEffect(() => {
    if (autoFetch) {
      fetchCompanies();
    }
  }, [fetchCompanies, autoFetch]);

  useEffect(() => {
    if (autoFetch) {
      fetchStats();
    }
  }, [fetchStats, autoFetch]);

  return {
    // Data
    companies,
    stats,
    currentCompany,

    // State
    loading,
    error,
    filters,
    pagination,

    // Actions
    fetchCompanies,
    fetchStats,
    fetchCompanyById,
    createCompany,
    updateCompany,
    deleteCompany,
    approveCompany,
    rejectCompany,
    activateCompany,
    deactivateCompany,

    // Bulk actions
    bulkApprove,
    bulkReject,
    bulkActivate,
    bulkDeactivate,

    // Utility
    setFilters,
    clearError,
    refresh,
    exportData
  };
};

export default useCompanies;