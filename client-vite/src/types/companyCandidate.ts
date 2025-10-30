// Company Candidate types

export type CompanyCandidateStatus =
  | 'PENDING_INVITATION'
  | 'PENDING_CONFIRMATION'
  | 'ACTIVE'
  | 'REJECTED'
  | 'ARCHIVED';

export type OwnershipStatus = 'COMPANY_OWNED' | 'USER_OWNED';

export type Priority = 'LOW' | 'MEDIUM' | 'HIGH';

export interface VisibilitySettings {
  show_personal_info: boolean;
  show_contact_info: boolean;
  show_work_history: boolean;
  show_education: boolean;
  show_skills: boolean;
  show_projects: boolean;
}

export interface CompanyCandidate {
  id: string;
  company_id: string;
  candidate_id: string;
  status: CompanyCandidateStatus;
  ownership_status: OwnershipStatus;
  priority: Priority;
  tags: string[];
  internal_notes: string | null;
  visibility_settings: VisibilitySettings;
  current_workflow_id: string | null;
  current_stage_id: string | null;
  phase_id: string | null;  // Phase 12: current recruitment phase
  added_by_user_id: string;
  invited_at: string | null;
  confirmed_at: string | null;
  rejected_at: string | null;
  archived_at: string | null;
  created_at: string;
  updated_at: string;

  // Expanded data
  candidate_name?: string;
  candidate_email?: string;
  candidate_phone?: string;
  workflow_name?: string;
  stage_name?: string;
  phase_name?: string;
  // Job position data (from candidate_application)
  job_position_id?: string;
  job_position_title?: string;
  application_status?: string;
  // Custom field values
  custom_field_values?: Record<string, any>;
}

export interface CreateCompanyCandidateRequest {
  company_id: string;
  candidate_id?: string; // If adding existing candidate
  // Or create new candidate with basic info
  candidate_name?: string;
  candidate_email?: string;
  candidate_phone?: string;
  priority?: Priority;
  tags?: string[];
  internal_notes?: string;
  visibility_settings?: Partial<VisibilitySettings>;
}

export interface UpdateCompanyCandidateRequest {
  priority?: Priority;
  tags?: string[];
  internal_notes?: string;
  visibility_settings?: Partial<VisibilitySettings>;
}

export interface AssignWorkflowRequest {
  workflow_id: string;
}

export interface ChangeStageRequest {
  new_stage_id: string;
}

export interface CandidateFilters {
  search?: string;
  status?: CompanyCandidateStatus;
  ownership_status?: OwnershipStatus;
  priority?: Priority;
  tags?: string[];
  workflow_id?: string;
  stage_id?: string;
  page?: number;
  page_size?: number;
}

// Helper functions
export const getCandidateStatusColor = (status: CompanyCandidateStatus): string => {
  switch (status) {
    case 'PENDING_INVITATION': return 'bg-yellow-100 text-yellow-800';
    case 'PENDING_CONFIRMATION': return 'bg-blue-100 text-blue-800';
    case 'ACTIVE': return 'bg-green-100 text-green-800';
    case 'REJECTED': return 'bg-red-100 text-red-800';
    case 'ARCHIVED': return 'bg-gray-100 text-gray-800';
    default: return 'bg-gray-100 text-gray-800';
  }
};

export const getPriorityColor = (priority: Priority): string => {
  switch (priority) {
    case 'HIGH': return 'bg-red-100 text-red-800';
    case 'MEDIUM': return 'bg-yellow-100 text-yellow-800';
    case 'LOW': return 'bg-green-100 text-green-800';
    default: return 'bg-gray-100 text-gray-800';
  }
};

export const getOwnershipColor = (ownership: OwnershipStatus): string => {
  switch (ownership) {
    case 'COMPANY_OWNED': return 'bg-blue-100 text-blue-800';
    case 'USER_OWNED': return 'bg-purple-100 text-purple-800';
    default: return 'bg-gray-100 text-gray-800';
  }
};
