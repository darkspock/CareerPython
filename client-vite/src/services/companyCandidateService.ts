import { ApiClient } from '../lib/api';
import type {
  CompanyCandidate,
  CreateCompanyCandidateRequest,
  UpdateCompanyCandidateRequest,
  AssignWorkflowRequest,
  ChangeStageRequest,
  CandidateFilters
} from '../types/companyCandidate';

const getAuthHeaders = () => {
  const token = localStorage.getItem('access_token');
  return {
    Authorization: `Bearer ${token}`,
  };
};

export const companyCandidateService = {
  /**
   * Create a new company candidate relationship
   */
  create: async (data: CreateCompanyCandidateRequest): Promise<CompanyCandidate> => {
    return ApiClient.post('/api/company-candidates/', data, {
      headers: getAuthHeaders(),
    });
  },

  /**
   * Get company candidate by ID
   */
  getById: async (companyCandidateId: string): Promise<CompanyCandidate> => {
    return ApiClient.get(`/api/company-candidates/${companyCandidateId}`, {
      headers: getAuthHeaders(),
    });
  },

  /**
   * Get company candidate by company ID and candidate ID
   */
  getByCompanyAndCandidate: async (
    companyId: string,
    candidateId: string
  ): Promise<CompanyCandidate> => {
    return ApiClient.get(
      `/api/company-candidates/company/${companyId}/candidate/${candidateId}`,
      {
        headers: getAuthHeaders(),
      }
    );
  },

  /**
   * List all candidates for a specific company
   */
  listByCompany: async (
    companyId: string,
    filters?: CandidateFilters
  ): Promise<CompanyCandidate[]> => {
    const queryParams = filters
      ? '?' + new URLSearchParams(filters as any).toString()
      : '';
    return ApiClient.get(`/api/company-candidates/company/${companyId}${queryParams}`, {
      headers: getAuthHeaders(),
    });
  },

  /**
   * List all company relationships for a specific candidate
   */
  listByCandidate: async (candidateId: string): Promise<CompanyCandidate[]> => {
    return ApiClient.get(`/api/company-candidates/candidate/${candidateId}`, {
      headers: getAuthHeaders(),
    });
  },

  /**
   * Update company candidate
   */
  update: async (
    companyCandidateId: string,
    data: UpdateCompanyCandidateRequest
  ): Promise<CompanyCandidate> => {
    return ApiClient.request(`/api/company-candidates/${companyCandidateId}`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
    });
  },

  /**
   * Candidate confirms/accepts company invitation
   */
  confirm: async (companyCandidateId: string): Promise<CompanyCandidate> => {
    return ApiClient.post(
      `/api/company-candidates/${companyCandidateId}/confirm`,
      {},
      {
        headers: getAuthHeaders(),
      }
    );
  },

  /**
   * Candidate rejects company invitation
   */
  reject: async (companyCandidateId: string): Promise<CompanyCandidate> => {
    return ApiClient.post(
      `/api/company-candidates/${companyCandidateId}/reject`,
      {},
      {
        headers: getAuthHeaders(),
      }
    );
  },

  /**
   * Archive a company candidate relationship
   */
  archive: async (companyCandidateId: string): Promise<CompanyCandidate> => {
    return ApiClient.post(
      `/api/company-candidates/${companyCandidateId}/archive`,
      {},
      {
        headers: getAuthHeaders(),
      }
    );
  },

  /**
   * Transfer ownership from company to user
   */
  transferOwnership: async (companyCandidateId: string): Promise<CompanyCandidate> => {
    return ApiClient.post(
      `/api/company-candidates/${companyCandidateId}/transfer-ownership`,
      {},
      {
        headers: getAuthHeaders(),
      }
    );
  },

  /**
   * Assign a workflow to a company candidate
   */
  assignWorkflow: async (
    companyCandidateId: string,
    data: AssignWorkflowRequest
  ): Promise<CompanyCandidate> => {
    return ApiClient.post(
      `/api/company-candidates/${companyCandidateId}/assign-workflow`,
      data,
      {
        headers: getAuthHeaders(),
      }
    );
  },

  /**
   * Change the workflow stage of a company candidate
   */
  changeStage: async (
    companyCandidateId: string,
    data: ChangeStageRequest
  ): Promise<CompanyCandidate> => {
    return ApiClient.post(
      `/api/company-candidates/${companyCandidateId}/change-stage`,
      data,
      {
        headers: getAuthHeaders(),
      }
    );
  },
};
