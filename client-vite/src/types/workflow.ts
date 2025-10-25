// Workflow types

export type WorkflowStatus = 'ACTIVE' | 'INACTIVE' | 'ARCHIVED';

export type StageType = 'INITIAL' | 'INTERMEDIATE' | 'FINAL' | 'CUSTOM';

export interface CompanyWorkflow {
  id: string;
  company_id: string;
  name: string;
  description: string | null;
  is_default: boolean;
  status: WorkflowStatus;
  created_at: string;
  updated_at: string;

  // Expanded data
  stages?: WorkflowStage[];
  candidate_count?: number;
}

export interface WorkflowStage {
  id: string;
  workflow_id: string;
  name: string;
  description: string | null;
  stage_type: StageType;
  order: number;
  is_active: boolean;
  required_outcome: string | null;
  estimated_duration_days: number | null;
  created_at: string;
  updated_at: string;

  // Expanded data
  candidate_count?: number;
}

export interface CreateWorkflowRequest {
  company_id: string;
  name: string;
  description?: string;
  is_default?: boolean;
  status?: WorkflowStatus;
}

export interface UpdateWorkflowRequest {
  name?: string;
  description?: string;
  is_default?: boolean;
  status?: WorkflowStatus;
}

export interface CreateStageRequest {
  workflow_id: string;
  name: string;
  description?: string;
  stage_type: StageType;
  order?: number;
  is_active?: boolean;
  required_outcome?: string;
  estimated_duration_days?: number;
}

export interface UpdateStageRequest {
  name?: string;
  description?: string;
  stage_type?: StageType;
  order?: number;
  is_active?: boolean;
  required_outcome?: string;
  estimated_duration_days?: number;
}

export interface ReorderStagesRequest {
  stage_ids: string[]; // Array of stage IDs in desired order
}

// Helper functions
export const getWorkflowStatusColor = (status: WorkflowStatus): string => {
  switch (status) {
    case 'ACTIVE': return 'bg-green-100 text-green-800';
    case 'INACTIVE': return 'bg-gray-100 text-gray-800';
    case 'ARCHIVED': return 'bg-red-100 text-red-800';
    default: return 'bg-gray-100 text-gray-800';
  }
};

export const getStageTypeColor = (type: StageType): string => {
  switch (type) {
    case 'INITIAL': return 'bg-blue-100 text-blue-800';
    case 'INTERMEDIATE': return 'bg-yellow-100 text-yellow-800';
    case 'FINAL': return 'bg-green-100 text-green-800';
    case 'CUSTOM': return 'bg-purple-100 text-purple-800';
    default: return 'bg-gray-100 text-gray-800';
  }
};
