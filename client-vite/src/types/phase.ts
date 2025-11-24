/**
 * Phase Types
 * Phase 12: Multi-phase recruitment workflow system
 */

export const DefaultView = {
  KANBAN: 'KANBAN',
  LIST: 'LIST',
} as const;
export type DefaultView = typeof DefaultView[keyof typeof DefaultView];

export const PhaseStatus = {
  DRAFT: 'DRAFT',
  ACTIVE: 'ACTIVE',
  ARCHIVED: 'ARCHIVED',
} as const;
export type PhaseStatus = typeof PhaseStatus[keyof typeof PhaseStatus];

export interface Phase {
  id: string;
  company_id: string;
  workflow_type: string; // 'CA' (Candidate Application), 'PO' (Job Position Opening), 'CO' (Company)
  name: string;
  sort_order: number;
  default_view: DefaultView;
  status: PhaseStatus;
  objective: string | null;
  created_at: string;
  updated_at: string;
}

export const WorkflowType = {
  CA: 'CA',
  PO: 'PO',
  CO: 'CO',
} as const;
export type WorkflowType = typeof WorkflowType[keyof typeof WorkflowType];

export interface CreatePhaseRequest {
  workflow_type: WorkflowType;
  name: string;
  sort_order: number;
  default_view: DefaultView;
  objective?: string;
}

export interface UpdatePhaseRequest {
  name: string;
  sort_order: number;
  default_view: DefaultView;
  objective?: string;
}

export interface PhaseFormData {
  name: string;
  sort_order: number;
  default_view: DefaultView;
  objective: string;
}
