/**
 * Position Stage Assignment Types
 * Types for managing user assignments to workflow stages for specific positions
 */

export interface PositionStageAssignment {
  id: string;
  position_id: string;
  stage_id: string;
  assigned_user_ids: string[];
  created_at?: string;
  updated_at?: string;
}

export interface AssignUsersToStageRequest {
  position_id: string;
  stage_id: string;
  user_ids: string[];
}

export interface AddUserToStageRequest {
  position_id: string;
  stage_id: string;
  user_id: string;
}

export interface RemoveUserFromStageRequest {
  position_id: string;
  stage_id: string;
  user_id: string;
}

export interface WorkflowStageAssignment {
  stage_id: string;
  default_user_ids: string[];
}

export interface CopyWorkflowAssignmentsRequest {
  position_id: string;
  workflow_assignments: WorkflowStageAssignment[];
}

export interface PositionStageAssignmentResponse {
  id: string;
  position_id: string;
  stage_id: string;
  assigned_user_ids: string[];
  created_at?: string;
  updated_at?: string;
}
