import { ApiClient } from '../lib/api';

const getAuthHeaders = () => {
  const token = localStorage.getItem('access_token');
  return {
    Authorization: `Bearer ${token}`,
  };
};

export interface WorkflowStage {
  id: string;
  name: string;
  stage_type: string;
  order: number;
  description: string;
  is_active: boolean;
  style?: {
    icon?: string;
    color?: string;
    background_color?: string;
  };
}

export const workflowStageService = {
  /**
   * Get all stages for a workflow
   */
  getStagesByWorkflow: async (workflowId: string): Promise<WorkflowStage[]> => {
    return ApiClient.get(`/api/workflow-stages/workflow/${workflowId}`, {
      headers: getAuthHeaders(),
    });
  },

  /**
   * Get next stage in workflow by order
   */
  getNextStage: async (workflowId: string, currentOrder: number): Promise<WorkflowStage | null> => {
    const stages = await workflowStageService.getStagesByWorkflow(workflowId);
    const nextStage = stages
      .filter(stage => stage.is_active)
      .sort((a, b) => a.order - b.order)
      .find(stage => stage.order > currentOrder);
    
    return nextStage || null;
  },

  /**
   * Get all FAIL stages (including "Lost")
   */
  getFailStages: async (workflowId: string): Promise<WorkflowStage[]> => {
    const stages = await workflowStageService.getStagesByWorkflow(workflowId);
    return stages
      .filter(stage => stage.is_active && stage.stage_type === 'fail')
      .sort((a, b) => a.order - b.order);
  }
};
