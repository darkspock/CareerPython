import { useState, useEffect, useCallback, useMemo } from 'react';
import { companyInterviewService } from '../services/companyInterviewService';
import type { 
  Interview, 
  InterviewFilters, 
  InterviewStatsResponse,
  InterviewFilterEnum 
} from '../services/companyInterviewService';
import { useCompanyId } from './useCompanyId';

export interface UseInterviewsOptions {
  initialFilters?: InterviewFilters;
  autoFetch?: boolean;
  pageSize?: number;
}

export interface UseInterviewsReturn {
  // Data
  interviews: Interview[];
  stats: InterviewStatsResponse | null;
  calendarInterviews: Interview[];
  
  // State
  loading: boolean;
  calendarLoading: boolean;
  error: string | null;
  filters: InterviewFilters;
  
    // Pagination
    total: number;
    pagination: {
      currentPage: number;
      pageSize: number;
      totalPages: number;
    };
  
  // Actions
  fetchInterviews: (overrideFilters?: {
    status?: string;
    fromDate?: string;
    toDate?: string;
    filterBy?: InterviewFilterEnum;
  }) => Promise<void>;
  fetchStats: () => Promise<void>;
  fetchCalendar: (startDate: Date, endDate: Date) => Promise<void>;
  setFilters: (filters: Partial<InterviewFilters>) => void;
  setCurrentPage: (page: number) => void;
  clearError: () => void;
  refresh: () => Promise<void>;
}

export function useInterviews(options: UseInterviewsOptions = {}): UseInterviewsReturn {
  const { 
    initialFilters = {}, 
    autoFetch = true,
    pageSize: initialPageSize = 20 
  } = options;
  
  const companyId = useCompanyId();
  
  // State
  const [interviews, setInterviews] = useState<Interview[]>([]);
  const [stats, setStats] = useState<InterviewStatsResponse | null>(null);
  const [calendarInterviews, setCalendarInterviews] = useState<Interview[]>([]);
  const [loading, setLoading] = useState(false);
  const [calendarLoading, setCalendarLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize] = useState(initialPageSize);
  
  // Filters state
  const [filters, setFiltersState] = useState<InterviewFilters>({
    limit: pageSize,
    offset: 0,
    ...initialFilters,
  });
  
  // Total state (from API response)
  const [total, setTotal] = useState(0);
  
  // Computed values
  const totalPages = useMemo(() => {
    return Math.ceil(total / pageSize);
  }, [total, pageSize]);
  
  // Fetch interviews
  const fetchInterviews = useCallback(async (overrideFilters?: {
    status?: string;
    fromDate?: string;
    toDate?: string;
    filterBy?: InterviewFilterEnum;
  }) => {
    if (!companyId) return;
    
    try {
      setLoading(true);
      setError(null);
      
      const effectiveFilters: InterviewFilters = {
        ...filters,
        limit: pageSize,
        offset: (currentPage - 1) * pageSize,
      };
      
      // Apply override filters if provided
      if (overrideFilters) {
        if (overrideFilters.status && overrideFilters.status !== 'all') {
          effectiveFilters.status = overrideFilters.status as any;
        }
        if (overrideFilters.filterBy) {
          effectiveFilters.filter_by = overrideFilters.filterBy;
        }
        if (overrideFilters.fromDate) {
          effectiveFilters.from_date = overrideFilters.fromDate;
        }
        if (overrideFilters.toDate) {
          effectiveFilters.to_date = overrideFilters.toDate;
        }
      } else {
        // Apply regular filters
        if (filters.candidate_name) {
          effectiveFilters.candidate_name = filters.candidate_name;
        }
        if (filters.status && filters.status !== 'all') {
          effectiveFilters.status = filters.status;
        }
        if (filters.interview_type && filters.interview_type !== 'all') {
          effectiveFilters.interview_type = filters.interview_type;
        }
        if (filters.process_type && filters.process_type !== 'all') {
          effectiveFilters.process_type = filters.process_type;
        }
        if (filters.job_position_id && filters.job_position_id !== 'all') {
          effectiveFilters.job_position_id = filters.job_position_id;
        }
        if (filters.required_role_id && filters.required_role_id !== 'all') {
          effectiveFilters.required_role_id = filters.required_role_id;
        }
        if (filters.interviewer_user_id && filters.interviewer_user_id !== 'all') {
          effectiveFilters.interviewer_user_id = filters.interviewer_user_id;
        }
        if (filters.from_date) {
          effectiveFilters.from_date = filters.from_date;
        }
        if (filters.to_date) {
          effectiveFilters.to_date = filters.to_date;
        }
        if (filters.filter_by) {
          effectiveFilters.filter_by = filters.filter_by;
        }
      }
      
      const response = await companyInterviewService.listInterviews(effectiveFilters);
      
      setInterviews(response.interviews);
      setTotal(response.total);
    } catch (err: any) {
      setError(err.message || 'Error al cargar las entrevistas');
      setInterviews([]);
    } finally {
      setLoading(false);
    }
  }, [companyId, filters, currentPage, pageSize]);
  
  // Fetch stats
  const fetchStats = useCallback(async () => {
    if (!companyId) return;
    
    try {
      const statsData = await companyInterviewService.getInterviewStats();
      setStats(statsData);
    } catch (err: any) {
      console.error('Error loading stats:', err);
      // Don't set error for stats, just log it
    }
  }, [companyId]);
  
  // Fetch calendar data
  const fetchCalendar = useCallback(async (startDate: Date, endDate: Date) => {
    if (!companyId) return;
    
    try {
      setCalendarLoading(true);
      const calendarData = await companyInterviewService.getInterviewCalendar(
        startDate.toISOString(),
        endDate.toISOString()
      );
      setCalendarInterviews(calendarData);
    } catch (err: any) {
      console.error('Error loading calendar data:', err);
    } finally {
      setCalendarLoading(false);
    }
  }, [companyId]);
  
  // Set filters
  const setFilters = useCallback((newFilters: Partial<InterviewFilters>) => {
    setFiltersState(prev => ({ ...prev, ...newFilters }));
  }, []);
  
  // Clear error
  const clearError = useCallback(() => {
    setError(null);
  }, []);
  
  // Refresh all data
  const refresh = useCallback(async () => {
    await Promise.all([
      fetchInterviews(),
      fetchStats(),
    ]);
  }, [fetchInterviews, fetchStats]);
  
  // Effects
  useEffect(() => {
    if (autoFetch && companyId) {
      fetchInterviews();
    }
  }, [autoFetch, companyId, fetchInterviews]);
  
  useEffect(() => {
    if (autoFetch && companyId) {
      fetchStats();
    }
  }, [autoFetch, companyId, fetchStats]);
  
  return {
    // Data
    interviews,
    stats,
    calendarInterviews,
    
    // State
    loading,
    calendarLoading,
    error,
    filters,
    
    // Pagination
    total,
    pagination: {
      currentPage,
      pageSize,
      totalPages,
    },
    
    // Actions
    fetchInterviews,
    fetchStats,
    fetchCalendar,
    setFilters,
    setCurrentPage,
    clearError,
    refresh,
  };
}

