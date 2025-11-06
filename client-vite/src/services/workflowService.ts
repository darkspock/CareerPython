/**
 * Workflow Service
 * Service for workflow operations with filtering capabilities
 */

import { ApiClient } from '../lib/api';
import type { CandidateApplicationWorkflow } from '../types/workflow';

interface ListWorkflowsFilters {
  phase_id?: string;
  status?: 'active' | 'draft' | 'archived';
}

export const workflowService = {
  /**
   * List workflows with optional filters
   * @param companyId - Company ID (not used in current implementation, kept for consistency)
   * @param filters - Optional filters for phase_id and status
   */
  async listWorkflows(
    companyId: string,
    filters?: ListWorkflowsFilters
  ): Promise<CandidateApplicationWorkflow[]> {
    // Build query parameters
    const params = new URLSearchParams();

    if (filters?.phase_id) {
      params.append('phase_id', filters.phase_id);
    }

    if (filters?.status) {
      params.append('status', filters.status);
    }

    const queryString = params.toString();
    const url = queryString
      ? `/api/company-workflows?${queryString}`
      : `/api/company-workflows/company/${companyId}`;

    return ApiClient.get<CandidateApplicationWorkflow[]>(url);
  },
};
