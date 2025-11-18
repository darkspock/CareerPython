import { useState, useEffect, useCallback, useMemo } from 'react';
import { PositionService } from '../services/positionService';
import { CompanyUserService } from '../services/companyUserService';
import { api } from '../lib/api';
import type { CompanyRole } from '../types/company';
import { useCompanyId } from './useCompanyId';

export interface UseInterviewFiltersReturn {
  // Filter maps
  positionMap: Record<string, string>;
  roleMap: Record<string, string>;
  userMap: Record<string, string>;
  
  // Loading state
  loadingFilters: boolean;
  
  // Refresh function
  refreshFilters: () => Promise<void>;
}

export function useInterviewFilters(): UseInterviewFiltersReturn {
  const companyId = useCompanyId();
  const [positionMap, setPositionMap] = useState<Record<string, string>>({});
  const [roleMap, setRoleMap] = useState<Record<string, string>>({});
  const [userMap, setUserMap] = useState<Record<string, string>>({});
  const [loadingFilters, setLoadingFilters] = useState(true);
  
  const loadFilterOptions = useCallback(async () => {
    if (!companyId) {
      setLoadingFilters(false);
      return;
    }
    
    let ignore = false;
    
    try {
      setLoadingFilters(true);
      
      // Load positions for filter dropdown
      const positionMapData: Record<string, string> = {};
      let page = 1;
      let hasMore = true;
      
      while (hasMore && !ignore) {
        const positionsData = await PositionService.getPositions({
          company_id: companyId,
          page: page,
          page_size: 100,
        });
        
        positionsData.positions.forEach((position) => {
          if (position.id && position.title) {
            positionMapData[position.id] = position.title;
          }
        });
        
        hasMore = positionsData.positions.length === 100 && page * 100 < positionsData.total;
        page++;
      }
      
      if (!ignore) {
        setPositionMap(positionMapData);
      }
      
      // Load company roles for filter dropdown
      const rolesData = await api.listCompanyRoles(companyId, true);
      if (ignore) return;
      
      const roleMapData: Record<string, string> = {};
      (rolesData as CompanyRole[]).forEach((role) => {
        if (role.id && role.name) {
          roleMapData[role.id] = role.name;
        }
      });
      if (!ignore) {
        setRoleMap(roleMapData);
      }
      
      // Load company users for filter dropdown
      const usersData = await CompanyUserService.getCompanyUsers(companyId, { active_only: true });
      if (ignore) return;
      
      const userMapData: Record<string, string> = {};
      usersData.forEach((user) => {
        if (user.id && user.email) {
          userMapData[user.id] = user.email;
        }
      });
      if (!ignore) {
        setUserMap(userMapData);
      }
    } catch (err) {
      if (!ignore) {
        console.error('Error loading filter options:', err);
      }
    } finally {
      if (!ignore) {
        setLoadingFilters(false);
      }
    }
    
    return () => {
      ignore = true;
    };
  }, [companyId]);
  
  const refreshFilters = useCallback(async () => {
    await loadFilterOptions();
  }, [loadFilterOptions]);
  
  useEffect(() => {
    loadFilterOptions();
  }, [loadFilterOptions]);
  
  return {
    positionMap,
    roleMap,
    userMap,
    loadingFilters,
    refreshFilters,
  };
}

