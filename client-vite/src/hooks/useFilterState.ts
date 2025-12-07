/**
 * useFilterState Hook
 * Manages filter state with URL persistence and saved filter presets
 */

import { useState, useEffect, useCallback, useMemo } from 'react';
import { useSearchParams } from 'react-router-dom';

export interface FilterConfig {
  key: string;
  type: 'string' | 'array' | 'boolean' | 'number';
  defaultValue?: any;
}

export interface SavedFilter {
  id: string;
  name: string;
  filters: Record<string, any>;
  createdAt: string;
  isDefault?: boolean;
}

interface UseFilterStateOptions {
  /** Filter configuration defining keys and types */
  config: FilterConfig[];
  /** Storage key for saved filters (defaults to window.location.pathname) */
  storageKey?: string;
  /** Whether to persist filters in URL (default: true) */
  persistToUrl?: boolean;
  /** Whether to persist filters in localStorage (default: false) */
  persistToStorage?: boolean;
}

interface UseFilterStateReturn<T extends Record<string, any>> {
  /** Current filter values */
  filters: T;
  /** Set a single filter value */
  setFilter: (key: keyof T, value: any) => void;
  /** Set multiple filter values at once */
  setFilters: (newFilters: Partial<T>) => void;
  /** Clear all filters to defaults */
  clearFilters: () => void;
  /** Check if any filters are active (non-default) */
  hasActiveFilters: boolean;
  /** Count of active filters */
  activeFilterCount: number;
  /** Saved filter presets */
  savedFilters: SavedFilter[];
  /** Save current filters as a preset */
  saveFilter: (name: string) => void;
  /** Load a saved filter preset */
  loadFilter: (filterId: string) => void;
  /** Delete a saved filter preset */
  deleteFilter: (filterId: string) => void;
  /** Set a filter as default */
  setDefaultFilter: (filterId: string | null) => void;
  /** Get filter values as URL search params string */
  getUrlParams: () => string;
}

export function useFilterState<T extends Record<string, any>>(
  options: UseFilterStateOptions
): UseFilterStateReturn<T> {
  const { config, storageKey, persistToUrl = true, persistToStorage = false } = options;
  const [searchParams, setSearchParams] = useSearchParams();

  // Generate storage key based on pathname if not provided
  const effectiveStorageKey = storageKey || `filters_${window.location.pathname.replace(/\//g, '_')}`;
  const savedFiltersKey = `${effectiveStorageKey}_saved`;

  // Build default values from config
  const defaultValues = useMemo(() => {
    const defaults: Record<string, any> = {};
    config.forEach(({ key, type, defaultValue }) => {
      if (defaultValue !== undefined) {
        defaults[key] = defaultValue;
      } else {
        switch (type) {
          case 'array':
            defaults[key] = [];
            break;
          case 'boolean':
            defaults[key] = false;
            break;
          case 'number':
            defaults[key] = 0;
            break;
          default:
            defaults[key] = '';
        }
      }
    });
    return defaults as T;
  }, [config]);

  // Parse value from URL based on type
  const parseUrlValue = useCallback((value: string | null, type: FilterConfig['type']) => {
    if (value === null || value === '') return null;
    switch (type) {
      case 'array':
        return value.split(',').filter(Boolean);
      case 'boolean':
        return value === 'true';
      case 'number':
        return Number(value);
      default:
        return value;
    }
  }, []);

  // Convert value to URL string based on type
  const valueToUrl = useCallback((value: any, type: FilterConfig['type']): string => {
    if (value === null || value === undefined) return '';
    switch (type) {
      case 'array':
        return Array.isArray(value) ? value.join(',') : '';
      case 'boolean':
        return value ? 'true' : '';
      case 'number':
        return value ? String(value) : '';
      default:
        return String(value);
    }
  }, []);

  // Initialize filters from URL or localStorage
  const initializeFilters = useCallback((): T => {
    const filters: Record<string, any> = { ...defaultValues };

    // First check URL params
    if (persistToUrl) {
      config.forEach(({ key, type }) => {
        const urlValue = searchParams.get(key);
        const parsed = parseUrlValue(urlValue, type);
        if (parsed !== null) {
          filters[key] = parsed;
        }
      });
    }

    // Then check localStorage (URL takes precedence)
    if (persistToStorage) {
      try {
        const stored = localStorage.getItem(effectiveStorageKey);
        if (stored) {
          const storedFilters = JSON.parse(stored);
          config.forEach(({ key }) => {
            if (storedFilters[key] !== undefined && !searchParams.has(key)) {
              filters[key] = storedFilters[key];
            }
          });
        }
      } catch {
        // Ignore parse errors
      }
    }

    return filters as T;
  }, [config, defaultValues, searchParams, persistToUrl, persistToStorage, effectiveStorageKey, parseUrlValue]);

  const [filters, setFiltersState] = useState<T>(initializeFilters);

  // Load saved filters from localStorage
  const [savedFilters, setSavedFilters] = useState<SavedFilter[]>(() => {
    try {
      const stored = localStorage.getItem(savedFiltersKey);
      return stored ? JSON.parse(stored) : [];
    } catch {
      return [];
    }
  });

  // Update URL when filters change
  useEffect(() => {
    if (!persistToUrl) return;

    const newParams = new URLSearchParams(searchParams);

    config.forEach(({ key, type, defaultValue }) => {
      const value = filters[key as keyof T];
      const urlValue = valueToUrl(value, type);
      const defaultUrlValue = valueToUrl(defaultValue ?? defaultValues[key], type);

      if (urlValue && urlValue !== defaultUrlValue) {
        newParams.set(key, urlValue);
      } else {
        newParams.delete(key);
      }
    });

    // Only update if params actually changed
    const currentParamsString = searchParams.toString();
    const newParamsString = newParams.toString();
    if (currentParamsString !== newParamsString) {
      setSearchParams(newParams, { replace: true });
    }
  }, [filters, config, defaultValues, persistToUrl, searchParams, setSearchParams, valueToUrl]);

  // Save to localStorage when filters change
  useEffect(() => {
    if (!persistToStorage) return;
    localStorage.setItem(effectiveStorageKey, JSON.stringify(filters));
  }, [filters, persistToStorage, effectiveStorageKey]);

  // Save savedFilters to localStorage
  useEffect(() => {
    localStorage.setItem(savedFiltersKey, JSON.stringify(savedFilters));
  }, [savedFilters, savedFiltersKey]);

  // Set single filter
  const setFilter = useCallback((key: keyof T, value: any) => {
    setFiltersState(prev => ({ ...prev, [key]: value }));
  }, []);

  // Set multiple filters
  const setFilters = useCallback((newFilters: Partial<T>) => {
    setFiltersState(prev => ({ ...prev, ...newFilters }));
  }, []);

  // Clear all filters
  const clearFilters = useCallback(() => {
    setFiltersState(defaultValues);
  }, [defaultValues]);

  // Check if filters differ from defaults
  const hasActiveFilters = useMemo(() => {
    return config.some(({ key, type }) => {
      const current = filters[key as keyof T];
      const defaultVal = defaultValues[key];

      if (type === 'array') {
        return Array.isArray(current) && current.length > 0;
      }
      return current !== defaultVal && current !== '' && current !== null;
    });
  }, [filters, defaultValues, config]);

  // Count active filters
  const activeFilterCount = useMemo(() => {
    return config.filter(({ key, type }) => {
      const current = filters[key as keyof T];
      const defaultVal = defaultValues[key];

      if (type === 'array') {
        return Array.isArray(current) && current.length > 0;
      }
      return current !== defaultVal && current !== '' && current !== null;
    }).length;
  }, [filters, defaultValues, config]);

  // Save current filters as preset
  const saveFilter = useCallback((name: string) => {
    const newFilter: SavedFilter = {
      id: `filter_${Date.now()}`,
      name,
      filters: { ...filters },
      createdAt: new Date().toISOString()
    };
    setSavedFilters(prev => [...prev, newFilter]);
  }, [filters]);

  // Load saved filter
  const loadFilter = useCallback((filterId: string) => {
    const filter = savedFilters.find(f => f.id === filterId);
    if (filter) {
      setFiltersState(filter.filters as T);
    }
  }, [savedFilters]);

  // Delete saved filter
  const deleteFilter = useCallback((filterId: string) => {
    setSavedFilters(prev => prev.filter(f => f.id !== filterId));
  }, []);

  // Set default filter
  const setDefaultFilter = useCallback((filterId: string | null) => {
    setSavedFilters(prev => prev.map(f => ({
      ...f,
      isDefault: f.id === filterId
    })));
  }, []);

  // Get URL params string
  const getUrlParams = useCallback(() => {
    const params = new URLSearchParams();
    config.forEach(({ key, type }) => {
      const value = filters[key as keyof T];
      const urlValue = valueToUrl(value, type);
      if (urlValue) {
        params.set(key, urlValue);
      }
    });
    return params.toString();
  }, [filters, config, valueToUrl]);

  return {
    filters,
    setFilter,
    setFilters,
    clearFilters,
    hasActiveFilters,
    activeFilterCount,
    savedFilters,
    saveFilter,
    loadFilter,
    deleteFilter,
    setDefaultFilter,
    getUrlParams
  };
}
