import { useState, useEffect, useCallback } from 'react';
import { companyCandidateService } from '../services/companyCandidateService';
import { PositionService } from '../services/positionService';
import { companyInterviewTemplateService } from '../services/companyInterviewTemplateService';
import { CompanyUserService } from '../services/companyUserService';
import { api } from '../lib/api';
import type { CompanyCandidate } from '../types/companyCandidate';
import type { Position } from '../types/position';
import type { InterviewTemplate } from '../services/companyInterviewTemplateService';
import type { CompanyRole } from '../types/company';
import type { CompanyUser } from '../types/companyUser';
import { useCompanyId } from './useCompanyId';

export interface UseInterviewFormDataReturn {
  candidates: CompanyCandidate[];
  positions: Position[];
  templates: InterviewTemplate[];
  roles: CompanyRole[];
  companyUsers: CompanyUser[];
  loading: boolean;
  error: string | null;
  refresh: () => Promise<void>;
}

export function useInterviewFormData(): UseInterviewFormDataReturn {
  const companyId = useCompanyId();
  const [candidates, setCandidates] = useState<CompanyCandidate[]>([]);
  const [positions, setPositions] = useState<Position[]>([]);
  const [templates, setTemplates] = useState<InterviewTemplate[]>([]);
  const [roles, setRoles] = useState<CompanyRole[]>([]);
  const [companyUsers, setCompanyUsers] = useState<CompanyUser[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  const loadData = useCallback(async () => {
    if (!companyId) {
      setError('Company ID not found');
      setLoading(false);
      return;
    }
    
    try {
      setLoading(true);
      setError(null);
      
      // Load all data in parallel
      const [candidatesData, positionsData, templatesData, rolesData, usersData] = await Promise.all([
        companyCandidateService.listByCompany(companyId),
        PositionService.getPositions({
          company_id: companyId,
          is_active: true,
          page_size: 100,
        }),
        companyInterviewTemplateService.listTemplates({
          status: 'ENABLED',
          page_size: 100,
        }),
        api.listCompanyRoles(companyId, true),
        CompanyUserService.getCompanyUsers(companyId, { active_only: true }),
      ]);
      
      setCandidates(candidatesData);
      setPositions(positionsData.positions);
      setTemplates(templatesData);
      setRoles(rolesData as CompanyRole[]);
      setCompanyUsers(usersData);
    } catch (err: any) {
      const errorMessage = err.message || 'Error al cargar los datos';
      setError(errorMessage);
      console.error('Error loading data:', err);
    } finally {
      setLoading(false);
    }
  }, [companyId]);
  
  const refresh = useCallback(async () => {
    await loadData();
  }, [loadData]);
  
  useEffect(() => {
    loadData();
  }, [loadData]);
  
  return {
    candidates,
    positions,
    templates,
    roles,
    companyUsers,
    loading,
    error,
    refresh,
  };
}

