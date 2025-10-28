/**
 * Phase Types
 * Phase 12: Multi-phase recruitment workflow system
 */

export enum DefaultView {
  KANBAN = 'KANBAN',
  LIST = 'LIST',
}

export enum PhaseStatus {
  DRAFT = 'DRAFT',
  ACTIVE = 'ACTIVE',
  ARCHIVED = 'ARCHIVED',
}

export interface Phase {
  id: string;
  company_id: string;
  name: string;
  sort_order: number;
  default_view: DefaultView;
  status: PhaseStatus;
  objective: string | null;
  created_at: string;
  updated_at: string;
}

export interface CreatePhaseRequest {
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
