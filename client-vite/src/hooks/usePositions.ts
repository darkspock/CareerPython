// Custom hook for managing positions
import { useState, useEffect, useCallback } from 'react';
import PositionService from '../services/positionService';
import type {
  Position,
  PositionFilters,
  PositionStats,
  CreatePositionRequest,
  UpdatePositionRequest,
  PositionListResponse
} from '../types/position';

export interface UsePositionsOptions {
  initialFilters?: PositionFilters;
  autoFetch?: boolean;
}

export interface UsePositionsReturn {
  // Data
  positions: Position[];
  stats: PositionStats | null;
  currentPosition: Position | null;

  // State
  loading: boolean;
  error: string | null;
  filters: PositionFilters;

  // Pagination
  pagination: {
    total: number;
    page: number;
    pageSize: number;
    totalPages: number;
  };

  // Actions
  fetchPositions: () => Promise<void>;
  fetchStats: () => Promise<void>;
  fetchPositionById: (id: string) => Promise<void>;
  createPosition: (data: CreatePositionRequest) => Promise<void>;
  updatePosition: (id: string, data: UpdatePositionRequest) => Promise<void>;
  deletePosition: (id: string) => Promise<void>;
  activatePosition: (id: string) => Promise<void>;
  deactivatePosition: (id: string) => Promise<void>;

  // Bulk actions
  bulkActivate: (ids: string[]) => Promise<void>;
  bulkDeactivate: (ids: string[]) => Promise<void>;
  bulkDelete: (ids: string[]) => Promise<void>;

  // Utility
  setFilters: (filters: PositionFilters) => void;
  clearError: () => void;
  refresh: () => Promise<void>;
  exportData: (format?: 'csv' | 'excel') => Promise<void>;
}

export const usePositions = (options: UsePositionsOptions = {}): UsePositionsReturn => {
  const { initialFilters = {}, autoFetch = true } = options;

  // State
  const [positions, setPositions] = useState<Position[]>([]);
  const [stats, setStats] = useState<PositionStats | null>(null);
  const [currentPosition, setCurrentPosition] = useState<Position | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFiltersState] = useState<PositionFilters>({
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
  const fetchPositions = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      const response: PositionListResponse = await PositionService.getPositions(filters);

      setPositions(response.positions);
      setPagination({
        total: response.total,
        page: response.page,
        pageSize: response.page_size,
        totalPages: response.total_pages
      });
    } catch (err: any) {
      setError(err.message || 'Failed to fetch positions');
      setPositions([]);
    } finally {
      setLoading(false);
    }
  }, [filters]);

  const fetchStats = useCallback(async () => {
    try {
      const statsData = await PositionService.getPositionStats();
      setStats(statsData);
    } catch (err: any) {
      console.error('Failed to fetch stats:', err);
      // Don't set error for stats fetch failure
    }
  }, []);

  const fetchPositionById = useCallback(async (id: string) => {
    try {
      setLoading(true);
      setError(null);
      const position = await PositionService.getPositionById(id);
      setCurrentPosition(position);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch position');
      setCurrentPosition(null);
    } finally {
      setLoading(false);
    }
  }, []);

  const createPosition = useCallback(async (data: CreatePositionRequest) => {
    try {
      setLoading(true);
      setError(null);
      await PositionService.createPosition(data);
      await fetchPositions();
      await fetchStats();
    } catch (err: any) {
      setError(err.message || 'Failed to create position');
      throw err;
    } finally {
      setLoading(false);
    }
  }, [fetchPositions, fetchStats]);

  const updatePosition = useCallback(async (id: string, data: UpdatePositionRequest) => {
    try {
      setLoading(true);
      setError(null);
      await PositionService.updatePosition(id, data);
      await fetchPositions();
      await fetchStats();
    } catch (err: any) {
      setError(err.message || 'Failed to update position');
      throw err;
    } finally {
      setLoading(false);
    }
  }, [fetchPositions, fetchStats]);

  const deletePosition = useCallback(async (id: string) => {
    try {
      setLoading(true);
      setError(null);
      await PositionService.deletePosition(id);
      await fetchPositions();
      await fetchStats();
    } catch (err: any) {
      setError(err.message || 'Failed to delete position');
      throw err;
    } finally {
      setLoading(false);
    }
  }, [fetchPositions, fetchStats]);

  const activatePosition = useCallback(async (id: string) => {
    try {
      setLoading(true);
      setError(null);
      await PositionService.activatePosition(id);
      await fetchPositions();
      await fetchStats();
    } catch (err: any) {
      setError(err.message || 'Failed to activate position');
      throw err;
    } finally {
      setLoading(false);
    }
  }, [fetchPositions, fetchStats]);

  const deactivatePosition = useCallback(async (id: string) => {
    try {
      setLoading(true);
      setError(null);
      await PositionService.deactivatePosition(id);
      await fetchPositions();
      await fetchStats();
    } catch (err: any) {
      setError(err.message || 'Failed to deactivate position');
      throw err;
    } finally {
      setLoading(false);
    }
  }, [fetchPositions, fetchStats]);

  // Bulk actions
  const bulkActivate = useCallback(async (ids: string[]) => {
    try {
      setLoading(true);
      setError(null);
      await PositionService.bulkActivatePositions(ids);
      await fetchPositions();
      await fetchStats();
    } catch (err: any) {
      setError(err.message || 'Failed to bulk activate positions');
      throw err;
    } finally {
      setLoading(false);
    }
  }, [fetchPositions, fetchStats]);

  const bulkDeactivate = useCallback(async (ids: string[]) => {
    try {
      setLoading(true);
      setError(null);
      await PositionService.bulkDeactivatePositions(ids);
      await fetchPositions();
      await fetchStats();
    } catch (err: any) {
      setError(err.message || 'Failed to bulk deactivate positions');
      throw err;
    } finally {
      setLoading(false);
    }
  }, [fetchPositions, fetchStats]);

  const bulkDelete = useCallback(async (ids: string[]) => {
    try {
      setLoading(true);
      setError(null);
      await PositionService.bulkDeletePositions(ids);
      await fetchPositions();
      await fetchStats();
    } catch (err: any) {
      setError(err.message || 'Failed to bulk delete positions');
      throw err;
    } finally {
      setLoading(false);
    }
  }, [fetchPositions, fetchStats]);

  // Utility functions
  const setFilters = useCallback((newFilters: PositionFilters) => {
    setFiltersState(prev => ({ ...prev, ...newFilters }));
  }, []);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  const refresh = useCallback(async () => {
    await Promise.all([fetchPositions(), fetchStats()]);
  }, [fetchPositions, fetchStats]);

  const exportData = useCallback(async (format: 'csv' | 'excel' = 'csv') => {
    try {
      setLoading(true);
      const blob = await PositionService.exportPositions(filters, format);

      // Create download link
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `positions_export.${format}`;
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
      fetchPositions();
    }
  }, [fetchPositions, autoFetch]);

  useEffect(() => {
    if (autoFetch) {
      fetchStats();
    }
  }, [fetchStats, autoFetch]);

  return {
    // Data
    positions,
    stats,
    currentPosition,

    // State
    loading,
    error,
    filters,
    pagination,

    // Actions
    fetchPositions,
    fetchStats,
    fetchPositionById,
    createPosition,
    updatePosition,
    deletePosition,
    activatePosition,
    deactivatePosition,

    // Bulk actions
    bulkActivate,
    bulkDeactivate,
    bulkDelete,

    // Utility
    setFilters,
    clearError,
    refresh,
    exportData
  };
};

export default usePositions;