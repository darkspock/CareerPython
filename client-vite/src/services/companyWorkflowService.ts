import { ApiClient } from '../lib/api';
import type {
  CompanyWorkflow,
  WorkflowStage,
  CreateWorkflowRequest,
  UpdateWorkflowRequest,
  CreateStageRequest,
  UpdateStageRequest,
  ReorderStagesRequest
} from '../types/workflow';
import type { UpdateStageStyleRequest } from '../types/stageStyle';

const getAuthHeaders = () => {
  const token = localStorage.getItem('access_token');
  return {
    Authorization: `Bearer ${token}`,
  };
};

export const companyWorkflowService = {
  // ===== Workflow Management =====

  /**
   * Create a new workflow
   */
  createWorkflow: async (data: CreateWorkflowRequest): Promise<CompanyWorkflow> => {
    return ApiClient.post('/api/company-workflows', data, {
      headers: getAuthHeaders(),
    });
  },

  /**
   * Get workflow by ID
   */
  getWorkflow: async (workflowId: string): Promise<CompanyWorkflow> => {
    return ApiClient.get(`/api/company-workflows/${workflowId}`, {
      headers: getAuthHeaders(),
    });
  },

  /**
   * List workflows for a specific company
   */
  listWorkflowsByCompany: async (companyId: string): Promise<CompanyWorkflow[]> => {
    return ApiClient.get(`/api/company-workflows/company/${companyId}`, {
      headers: getAuthHeaders(),
    });
  },

  /**
   * Update workflow
   */
  updateWorkflow: async (
    workflowId: string,
    data: UpdateWorkflowRequest
  ): Promise<CompanyWorkflow> => {
    return ApiClient.request(`/api/company-workflows/${workflowId}`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
    });
  },

  /**
   * Deactivate workflow
   */
  deactivateWorkflow: async (workflowId: string): Promise<CompanyWorkflow> => {
    return ApiClient.post(
      `/api/company-workflows/${workflowId}/deactivate`,
      {},
      {
        headers: getAuthHeaders(),
      }
    );
  },

  /**
   * Archive workflow
   */
  archiveWorkflow: async (workflowId: string): Promise<CompanyWorkflow> => {
    return ApiClient.post(
      `/api/company-workflows/${workflowId}/archive`,
      {},
      {
        headers: getAuthHeaders(),
      }
    );
  },

  /**
   * Set workflow as default
   */
  setAsDefault: async (workflowId: string): Promise<CompanyWorkflow> => {
    return ApiClient.post(
      `/api/company-workflows/${workflowId}/set-default`,
      {},
      {
        headers: getAuthHeaders(),
      }
    );
  },

  /**
   * Unset workflow as default
   */
  unsetDefault: async (workflowId: string): Promise<CompanyWorkflow> => {
    return ApiClient.post(
      `/api/company-workflows/${workflowId}/unset-default`,
      {},
      {
        headers: getAuthHeaders(),
      }
    );
  },

  /**
   * Delete workflow (archives it)
   */
  deleteWorkflow: async (workflowId: string): Promise<void> => {
    const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/company-workflows/${workflowId}`, {
      method: 'DELETE',
      headers: getAuthHeaders(),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to delete workflow');
    }

    // DELETE returns 204 No Content, so no need to parse response
    return;
  },

  // ===== Stage Management =====

  /**
   * Create a new stage
   */
  createStage: async (data: CreateStageRequest): Promise<WorkflowStage> => {
    return ApiClient.post('/api/workflow-stages', data, {
      headers: getAuthHeaders(),
    });
  },

  /**
   * Get stage by ID
   */
  getStage: async (stageId: string): Promise<WorkflowStage> => {
    return ApiClient.get(`/api/workflow-stages/${stageId}`, {
      headers: getAuthHeaders(),
    });
  },

  /**
   * List stages for a specific workflow
   */
  listStagesByWorkflow: async (workflowId: string): Promise<WorkflowStage[]> => {
    return ApiClient.get(`/api/workflow-stages/workflow/${workflowId}`, {
      headers: getAuthHeaders(),
    });
  },

  /**
   * List stages for a specific phase
   */
  listStagesByPhase: async (phaseId: string): Promise<WorkflowStage[]> => {
    return ApiClient.get(`/api/workflow-stages/phase/${phaseId}`, {
      headers: getAuthHeaders(),
    });
  },

  /**
   * Get initial stage of a workflow
   */
  getInitialStage: async (workflowId: string): Promise<WorkflowStage> => {
    return ApiClient.get(`/api/workflow-stages/workflow/${workflowId}/initial`, {
      headers: getAuthHeaders(),
    });
  },

  /**
   * Get final stages of a workflow
   */
  getFinalStages: async (workflowId: string): Promise<WorkflowStage[]> => {
    return ApiClient.get(`/api/workflow-stages/workflow/${workflowId}/final`, {
      headers: getAuthHeaders(),
    });
  },

  /**
   * Update stage
   */
  updateStage: async (
    stageId: string,
    data: UpdateStageRequest
  ): Promise<WorkflowStage> => {
    return ApiClient.request(`/api/workflow-stages/${stageId}`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
    });
  },

  /**
   * Delete stage
   */
  deleteStage: async (stageId: string): Promise<void> => {
    return ApiClient.request(`/api/workflow-stages/${stageId}`, {
      method: 'DELETE',
      headers: getAuthHeaders(),
    });
  },

  /**
   * Reorder stages
   */
  reorderStages: async (
    workflowId: string,
    data: ReorderStagesRequest
  ): Promise<void> => {
    return ApiClient.post(
      `/api/workflow-stages/workflow/${workflowId}/reorder`,
      data,
      {
        headers: getAuthHeaders(),
      }
    );
  },

  /**
   * Activate stage
   */
  activateStage: async (stageId: string): Promise<WorkflowStage> => {
    return ApiClient.post(
      `/api/workflow-stages/${stageId}/activate`,
      {},
      {
        headers: getAuthHeaders(),
      }
    );
  },

  /**
   * Deactivate stage
   */
  deactivateStage: async (stageId: string): Promise<WorkflowStage> => {
    return ApiClient.post(
      `/api/workflow-stages/${stageId}/deactivate`,
      {},
      {
        headers: getAuthHeaders(),
      }
    );
  },

  /**
   * Update stage style
   */
  updateStageStyle: async (stageId: string, style: UpdateStageStyleRequest): Promise<WorkflowStage> => {
    return ApiClient.authenticatedRequest(
      `/api/workflow-stages/${stageId}/style`,
      {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(style),
      }
    );
  },
};
