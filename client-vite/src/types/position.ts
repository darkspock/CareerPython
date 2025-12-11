// Position/Job Opening types - Updated for workflow-based system
// Includes Publishing Flow types (PRD v2.1)

// ==================== KILLER QUESTIONS ====================

/**
 * Killer Question - inline screening question stored in JobPosition
 */
export interface KillerQuestion {
  id: string;
  name: string;
  description?: string;
  data_type: 'short_string' | 'large_string' | 'int' | 'date' | 'scoring';
  scoring_values?: Array<{ label: string; scoring: number }>;
  is_killer?: boolean;
  sort_order: number;
}

// ==================== PUBLISHING FLOW ENUMS ====================

/**
 * Job Position Status - Publishing Flow States
 * Matches backend JobPositionStatusEnum
 */
export const JobPositionStatus = {
  DRAFT: 'draft',
  PENDING_APPROVAL: 'pending_approval',
  APPROVED: 'approved',
  REJECTED: 'rejected',
  PUBLISHED: 'published',
  ON_HOLD: 'on_hold',
  CLOSED: 'closed',
  ARCHIVED: 'archived'
} as const;
export type JobPositionStatus = typeof JobPositionStatus[keyof typeof JobPositionStatus];

/**
 * Closed Reason - Why a position was closed
 * Matches backend ClosedReasonEnum
 */
export const ClosedReason = {
  FILLED: 'filled',
  CANCELLED: 'cancelled',
  BUDGET_CUT: 'budget_cut',
  DUPLICATE: 'duplicate',
  OTHER: 'other'
} as const;
export type ClosedReason = typeof ClosedReason[keyof typeof ClosedReason];

/**
 * Employment Type
 * Matches backend EmploymentTypeEnum
 */
export const EmploymentType = {
  FULL_TIME: 'full_time',
  PART_TIME: 'part_time',
  CONTRACT: 'contract',
  INTERNSHIP: 'internship',
  TEMPORARY: 'temporary',
  FREELANCE: 'freelance'
} as const;
export type EmploymentType = typeof EmploymentType[keyof typeof EmploymentType];

/**
 * Experience Level
 * Matches backend ExperienceLevelEnum
 */
export const ExperienceLevel = {
  INTERNSHIP: 'internship',
  ENTRY: 'entry',
  MID: 'mid',
  SENIOR: 'senior',
  LEAD: 'lead',
  EXECUTIVE: 'executive'
} as const;
export type ExperienceLevel = typeof ExperienceLevel[keyof typeof ExperienceLevel];

/**
 * Work Location Type
 * Matches backend WorkLocationTypeEnum
 */
export const WorkLocationType = {
  ON_SITE: 'on_site',
  HYBRID: 'hybrid',
  REMOTE: 'remote'
} as const;
export type WorkLocationType = typeof WorkLocationType[keyof typeof WorkLocationType];

/**
 * Salary Period
 * Matches backend SalaryPeriodEnum
 */
export const SalaryPeriod = {
  HOURLY: 'hourly',
  MONTHLY: 'monthly',
  YEARLY: 'yearly'
} as const;
export type SalaryPeriod = typeof SalaryPeriod[keyof typeof SalaryPeriod];

// ==================== VALUE OBJECTS ====================

/**
 * Language Requirement - Language + proficiency level
 */
export interface LanguageRequirement {
  language: string;
  level: 'A1' | 'A2' | 'B1' | 'B2' | 'C1' | 'C2' | 'Native';
}

/**
 * Custom Field Definition - Field configuration for job position
 */
export interface CustomFieldDefinition {
  field_key: string;
  label: string;
  field_type: 'TEXT' | 'NUMBER' | 'SELECT' | 'MULTISELECT' | 'DATE' | 'BOOLEAN' | 'URL';
  options?: any[] | null;  // Can be strings or i18n objects {id, sort, labels: [{language, label}]}
  is_required: boolean;
  candidate_visible: boolean;
  validation_rules?: Record<string, unknown> | null;
  sort_order: number;
  is_active: boolean;
}

// ==================== STATUS HELPERS ====================

/**
 * Get display label for JobPositionStatus
 */
export function getJobPositionStatusLabel(status: JobPositionStatus | string): string {
  const labels: Record<string, string> = {
    [JobPositionStatus.DRAFT]: 'Draft',
    [JobPositionStatus.PENDING_APPROVAL]: 'Pending Approval',
    [JobPositionStatus.APPROVED]: 'Approved',
    [JobPositionStatus.REJECTED]: 'Rejected',
    [JobPositionStatus.PUBLISHED]: 'Published',
    [JobPositionStatus.ON_HOLD]: 'On Hold',
    [JobPositionStatus.CLOSED]: 'Closed',
    [JobPositionStatus.ARCHIVED]: 'Archived'
  };
  return labels[status] || status;
}

/**
 * Get color classes for JobPositionStatus badge
 */
export function getJobPositionStatusColor(status: JobPositionStatus | string): string {
  const colors: Record<string, string> = {
    [JobPositionStatus.DRAFT]: 'bg-gray-100 text-gray-800',
    [JobPositionStatus.PENDING_APPROVAL]: 'bg-yellow-100 text-yellow-800',
    [JobPositionStatus.APPROVED]: 'bg-blue-100 text-blue-800',
    [JobPositionStatus.REJECTED]: 'bg-red-100 text-red-800',
    [JobPositionStatus.PUBLISHED]: 'bg-green-100 text-green-800',
    [JobPositionStatus.ON_HOLD]: 'bg-orange-100 text-orange-800',
    [JobPositionStatus.CLOSED]: 'bg-gray-100 text-gray-600',
    [JobPositionStatus.ARCHIVED]: 'bg-purple-100 text-purple-800'
  };
  return colors[status] || 'bg-gray-100 text-gray-800';
}

/**
 * Get display label for ClosedReason
 */
export function getClosedReasonLabel(reason: ClosedReason | string): string {
  const labels: Record<string, string> = {
    [ClosedReason.FILLED]: 'Position Filled',
    [ClosedReason.CANCELLED]: 'Cancelled',
    [ClosedReason.BUDGET_CUT]: 'Budget Cut',
    [ClosedReason.DUPLICATE]: 'Duplicate',
    [ClosedReason.OTHER]: 'Other'
  };
  return labels[reason] || reason;
}

/**
 * Get display label for EmploymentType
 */
export function getEmploymentTypeLabel(type: EmploymentType | string): string {
  const labels: Record<string, string> = {
    [EmploymentType.FULL_TIME]: 'Full Time',
    [EmploymentType.PART_TIME]: 'Part Time',
    [EmploymentType.CONTRACT]: 'Contract',
    [EmploymentType.INTERNSHIP]: 'Internship',
    [EmploymentType.TEMPORARY]: 'Temporary',
    [EmploymentType.FREELANCE]: 'Freelance'
  };
  return labels[type] || type;
}

/**
 * Get display label for ExperienceLevel
 */
export function getExperienceLevelLabel(level: ExperienceLevel | string): string {
  const labels: Record<string, string> = {
    [ExperienceLevel.INTERNSHIP]: 'Internship',
    [ExperienceLevel.ENTRY]: 'Entry Level',
    [ExperienceLevel.MID]: 'Mid Level',
    [ExperienceLevel.SENIOR]: 'Senior',
    [ExperienceLevel.LEAD]: 'Lead',
    [ExperienceLevel.EXECUTIVE]: 'Executive'
  };
  return labels[level] || level;
}

/**
 * Get display label for WorkLocationType
 */
export function getWorkLocationTypeLabel(type: WorkLocationType | string): string {
  const labels: Record<string, string> = {
    [WorkLocationType.ON_SITE]: 'On-site',
    [WorkLocationType.HYBRID]: 'Hybrid',
    [WorkLocationType.REMOTE]: 'Remote'
  };
  return labels[type] || type;
}

/**
 * Get display label for SalaryPeriod
 */
export function getSalaryPeriodLabel(period: SalaryPeriod | string): string {
  const labels: Record<string, string> = {
    [SalaryPeriod.HOURLY]: 'per hour',
    [SalaryPeriod.MONTHLY]: 'per month',
    [SalaryPeriod.YEARLY]: 'per year'
  };
  return labels[period] || period;
}

/**
 * Check if a field is locked based on position status
 */
export function isFieldLocked(status: JobPositionStatus | string, fieldName: string): boolean {
  const lockedFieldsByStatus: Record<string, string[]> = {
    [JobPositionStatus.DRAFT]: [],
    [JobPositionStatus.PENDING_APPROVAL]: [],
    [JobPositionStatus.APPROVED]: ['budget_max'],
    [JobPositionStatus.REJECTED]: [],
    [JobPositionStatus.PUBLISHED]: ['budget_max', 'custom_fields_config'],
    [JobPositionStatus.ON_HOLD]: ['budget_max', 'custom_fields_config'],
    [JobPositionStatus.CLOSED]: ['budget_max', 'custom_fields_config', 'salary_min', 'salary_max'],
    [JobPositionStatus.ARCHIVED]: ['*'] // All fields locked
  };

  const lockedFields = lockedFieldsByStatus[status] || [];
  if (lockedFields.includes('*')) return true;
  return lockedFields.includes(fieldName);
}

/**
 * Get available status transitions from current status
 */
export function getAvailableTransitions(status: JobPositionStatus | string): JobPositionStatus[] {
  const transitions: Record<string, JobPositionStatus[]> = {
    [JobPositionStatus.DRAFT]: [JobPositionStatus.PENDING_APPROVAL, JobPositionStatus.PUBLISHED],
    [JobPositionStatus.PENDING_APPROVAL]: [JobPositionStatus.APPROVED, JobPositionStatus.REJECTED, JobPositionStatus.DRAFT],
    [JobPositionStatus.APPROVED]: [JobPositionStatus.PUBLISHED, JobPositionStatus.DRAFT],
    [JobPositionStatus.REJECTED]: [JobPositionStatus.DRAFT],
    [JobPositionStatus.PUBLISHED]: [JobPositionStatus.ON_HOLD, JobPositionStatus.CLOSED],
    [JobPositionStatus.ON_HOLD]: [JobPositionStatus.PUBLISHED, JobPositionStatus.CLOSED],
    [JobPositionStatus.CLOSED]: [JobPositionStatus.ARCHIVED, JobPositionStatus.DRAFT],
    [JobPositionStatus.ARCHIVED]: []
  };
  return transitions[status] || [];
}

// ==================== JOB POSITION WORKFLOW TYPES ====================

// Job Position Workflow Types
export interface JobPositionWorkflowStage {
  id: string;
  name: string;
  icon: string;
  background_color: string;
  text_color: string;
  role?: string | null; // CompanyRoleId
  status_mapping: string; // JobPositionStatusEnum value ('draft' | 'active' | 'paused' | 'closed' | 'archived')
  kanban_display: string; // KanbanDisplayEnum value
  field_visibility: Record<string, boolean>;
  field_validation: Record<string, any>;
  field_candidate_visibility?: Record<string, boolean>; // Field visibility for candidates
}

export interface JobPositionWorkflow {
  id: string;
  company_id: string;
  name: string;
  default_view: string; // 'kanban' | 'list'
  status: string; // 'draft' | 'published' | 'deprecated'
  stages: JobPositionWorkflowStage[];
  custom_fields_config: Record<string, any>;
  created_at: string;
  updated_at: string;
}

// Visibility enum values
export type JobPositionVisibility = 'hidden' | 'internal' | 'public';

// Language options
export const LANGUAGE_OPTIONS = [
  { value: 'spanish', label: 'Spanish' },
  { value: 'english', label: 'English' },
  { value: 'french', label: 'French' },
  { value: 'german', label: 'German' },
  { value: 'portuguese', label: 'Portuguese' },
  { value: 'italian', label: 'Italian' },
  { value: 'chinese', label: 'Chinese' },
  { value: 'japanese', label: 'Japanese' }
] as const;

// Language level options (matching backend LanguageLevelEnum)
export const LANGUAGE_LEVEL_OPTIONS = [
  { value: 'none', label: 'None' },
  { value: 'basic', label: 'Basic' },
  { value: 'conversational', label: 'Conversational' },
  { value: 'professional', label: 'Professional' }
] as const;

// Desired role options (matching backend PositionRoleEnum)
export const DESIRED_ROLE_OPTIONS = [
  { value: 'manage_people', label: 'Manage People' },
  { value: 'lead_initiatives', label: 'Lead Initiatives' },
  { value: 'technology', label: 'Technology' },
  { value: 'sales', label: 'Sales' },
  { value: 'financial', label: 'Financial' },
  { value: 'hr', label: 'HR' },
  { value: 'executive', label: 'Executive' },
  { value: 'operations', label: 'Operations' },
  { value: 'marketing', label: 'Marketing' },
  { value: 'product', label: 'Product' },
  { value: 'legal_compliance', label: 'Legal & Compliance' },
  { value: 'customer_success', label: 'Customer Success' }
] as const;

export interface Position {
  id: string;
  company_id: string;
  job_position_workflow_id?: string | null;  // Workflow system
  stage_id?: string | null;  // Current stage in workflow
  phase_workflows?: Record<string, string> | null;  // Phase 12.8: phase_id -> workflow_id mapping
  custom_fields_values: Record<string, unknown>;  // All removed fields are stored here
  company_name?: string; // Populated when fetching with company info

  // Core fields (simplified)
  title: string;
  description?: string | null;
  job_category: string;
  open_at?: string | null;
  application_deadline?: string | null;
  visibility: JobPositionVisibility;  // 'hidden' | 'internal' | 'public' (replaces is_public)
  public_slug?: string | null;
  created_at?: string;
  updated_at?: string;
  pending_comments_count?: number;  // Number of pending comments

  // ==================== PUBLISHING FLOW FIELDS ====================

  // Publishing Status
  status: JobPositionStatus;
  closed_reason?: ClosedReason | null;
  closed_at?: string | null;
  published_at?: string | null;

  // Financial Fields
  salary_currency?: string | null;
  salary_min?: number | null;
  salary_max?: number | null;
  salary_period?: SalaryPeriod | null;
  show_salary: boolean;
  budget_max?: number | null;
  approved_budget_max?: number | null;
  financial_approver_id?: string | null;
  approved_at?: string | null;

  // Standard Fields
  department_id?: string | null;
  employment_type?: EmploymentType | null;
  experience_level?: ExperienceLevel | null;
  work_location_type?: WorkLocationType | null;
  office_locations: string[];
  remote_restrictions?: string | null;
  number_of_openings: number;
  requisition_id?: string | null;

  // Content Fields
  skills: string[];
  languages?: LanguageRequirement[] | null;

  // Ownership Fields
  hiring_manager_id?: string | null;
  recruiter_id?: string | null;
  created_by_id?: string | null;
  created_by_name?: string | null;  // Populated from user lookup

  // Approval Flow Fields
  submitted_at?: string | null;  // When position was submitted for approval
  rejection_reason?: string | null;  // Reason if position was rejected

  // Custom Fields (Snapshot from workflow)
  custom_fields_config: CustomFieldDefinition[];
  source_workflow_id?: string | null;

  // Pipeline & Screening
  candidate_pipeline_id?: string | null;
  screening_template_id?: string | null;

  // Killer Questions (inline, stored as JSON)
  killer_questions?: KillerQuestion[];

  // Expanded data (when workflow/stage is loaded)
  stage?: JobPositionWorkflowStage;
  workflow?: JobPositionWorkflow;
}

export interface CreatePositionRequest {
  company_id: string;
  job_position_workflow_id?: string | null;  // Workflow system
  stage_id?: string | null;  // Initial stage ID
  phase_workflows?: Record<string, string> | null;  // Phase workflows mapping
  custom_fields_values?: Record<string, unknown>;  // Legacy custom field values
  custom_fields_config?: CustomFieldDefinition[] | null;  // Custom field definitions
  source_workflow_id?: string | null;  // Workflow from which fields were copied

  // Core fields
  title: string;
  description?: string | null;
  job_category?: string;  // Default: 'other'
  open_at?: string | null;
  application_deadline?: string | null;
  visibility?: JobPositionVisibility;  // Default: 'hidden'
  public_slug?: string | null;

  // Financial fields
  salary_currency?: string | null;
  salary_min?: number | null;
  salary_max?: number | null;
  salary_period?: SalaryPeriod | null;
  show_salary?: boolean;
  budget_max?: number | null;

  // Standard fields
  department_id?: string | null;
  employment_type?: EmploymentType | null;
  experience_level?: ExperienceLevel | null;
  work_location_type?: WorkLocationType | null;
  office_locations?: string[];
  remote_restrictions?: string | null;
  number_of_openings?: number;
  requisition_id?: string | null;

  // Content fields
  skills?: string[];
  languages?: LanguageRequirement[] | null;

  // Ownership fields
  hiring_manager_id?: string | null;
  recruiter_id?: string | null;

  // Pipeline & Screening
  candidate_pipeline_id?: string | null;
  screening_template_id?: string | null;

  // Killer Questions
  killer_questions?: KillerQuestion[];
}

export interface UpdatePositionRequest {
  job_position_workflow_id?: string | null;  // Workflow system
  stage_id?: string | null;  // Stage ID
  phase_workflows?: Record<string, string> | null;  // Phase workflows mapping
  custom_fields_values?: Record<string, unknown>;  // Legacy custom field values
  custom_fields_config?: CustomFieldDefinition[] | null;  // Custom field definitions (only in DRAFT)

  // Core fields
  title?: string;
  description?: string | null;
  job_category?: string;
  open_at?: string | null;
  application_deadline?: string | null;
  visibility?: JobPositionVisibility;
  public_slug?: string | null;

  // Financial fields (budget locked after approval)
  salary_currency?: string | null;
  salary_min?: number | null;
  salary_max?: number | null;
  salary_period?: SalaryPeriod | null;
  show_salary?: boolean;
  budget_max?: number | null;

  // Standard fields
  department_id?: string | null;
  employment_type?: EmploymentType | null;
  experience_level?: ExperienceLevel | null;
  work_location_type?: WorkLocationType | null;
  office_locations?: string[];
  remote_restrictions?: string | null;
  number_of_openings?: number;
  requisition_id?: string | null;

  // Content fields
  skills?: string[];
  languages?: LanguageRequirement[] | null;

  // Ownership fields
  hiring_manager_id?: string | null;
  recruiter_id?: string | null;

  // Pipeline & Screening
  candidate_pipeline_id?: string | null;
  screening_template_id?: string | null;

  // Killer Questions
  killer_questions?: KillerQuestion[];
}

export interface PositionFilters {
  company_id?: string;
  search_term?: string;
  job_category?: string;
  visibility?: JobPositionVisibility;
  is_active?: boolean;
  page?: number;
  page_size?: number;

  // Publishing flow filters
  status?: JobPositionStatus;
  hiring_manager_id?: string;
  recruiter_id?: string;
  employment_type?: EmploymentType;
  experience_level?: ExperienceLevel;
  work_location_type?: WorkLocationType;
}

export interface PositionListResponse {
  positions: Position[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface PositionStats {
  total_positions: number;
  active_positions: number;
  inactive_positions: number;
  positions_by_type: Record<string, number>;
  positions_by_level: Record<string, number>;
  positions_by_company: Record<string, number>;
}

export interface PositionActionResponse {
  message: string;
  position?: Position;
}

// ==================== PUBLISHING FLOW ACTION TYPES ====================

/**
 * Request for closing a position
 */
export interface ClosePositionRequest {
  closed_reason: ClosedReason;
  note?: string;
}

/**
 * Request for rejecting a position
 */
export interface RejectPositionRequest {
  reason: string;
}

/**
 * Response from status transition actions
 */
export interface StatusTransitionResponse {
  success: boolean;
  message: string;
  position: Position;
}

/**
 * Request for cloning a position
 */
export interface ClonePositionRequest {
  new_title?: string;
}

/**
 * Position stats by status for dashboard
 */
export interface PositionStatusStats {
  total: number;
  by_status: Record<JobPositionStatus, number>;
}

// Form data type for Position forms (used in admin components)
export interface PositionFormData {
  company_id: string;
  title: string;
  description: string;
  department: string;
  location: string;
  work_location_type: string;
  employment_type: string;
  experience_level: string;
  salary_min: string;
  salary_max: string;
  salary_currency: string;
  requirements: string;
  benefits: string;
  skills: string;
  application_deadline: string;
  application_url: string;
  application_email: string;
  contact_person: string;
  working_hours: string;
  travel_required: boolean;
  visa_sponsorship: boolean;
  reports_to: string;
  number_of_openings: string;
  job_category: string;
  languages_required: Array<{ language: string; level: string }>;
  desired_roles: string[];
}

// Helper functions to access fields from custom_fields_values
export function getCustomField(position: Position, fieldName: string): any {
  return position.custom_fields_values?.[fieldName];
}

export function getDepartment(position: Position): string | undefined {
  return getCustomField(position, 'department') as string | undefined;
}

export function getLocation(position: Position): string | undefined {
  return getCustomField(position, 'location') as string | undefined;
}

export function getWorkLocationType(position: Position): string | undefined {
  return getCustomField(position, 'work_location_type') as string | undefined;
}

export function getEmploymentType(position: Position): string | undefined {
  return getCustomField(position, 'employment_type') as string | undefined;
}

export function getContractType(position: Position): string | undefined {
  return getCustomField(position, 'contract_type') as string | undefined;
}

export function getContractTypeLabel(contractType?: string | null): string {
  if (!contractType) return 'Not specified';
  const labels: Record<string, string> = {
    'full_time': 'Full Time',
    'part_time': 'Part Time',
    'contract': 'Contract',
    'internship': 'Internship',
    'freelance': 'Freelance',
    'temporary': 'Temporary',
    'permanent': 'Permanent',
  };
  return labels[contractType.toLowerCase()] || contractType.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
}

export function getExperienceLevel(position: Position): string | undefined {
  return getCustomField(position, 'experience_level') as string | undefined;
}

export function getPositionLevel(position: Position): string | undefined {
  return getCustomField(position, 'position_level') as string | undefined;
}

export function getSalaryMin(position: Position): number | undefined {
  return getCustomField(position, 'salary_min') as number | undefined;
}

export function getSalaryMax(position: Position): number | undefined {
  return getCustomField(position, 'salary_max') as number | undefined;
}

export function getSalaryCurrency(position: Position): string | undefined {
  return getCustomField(position, 'salary_currency') as string | undefined;
}

export function getSalaryRange(position: Position): { min_amount?: number; max_amount?: number; currency?: string } | undefined {
  return getCustomField(position, 'salary_range') as { min_amount?: number; max_amount?: number; currency?: string } | undefined;
}

export function getRequirements(position: Position): string[] | undefined {
  const reqs = getCustomField(position, 'requirements');
  if (Array.isArray(reqs)) return reqs;
  if (typeof reqs === 'object' && reqs?.requirements) return reqs.requirements;
  return undefined;
}

export function getBenefits(position: Position): string[] | undefined {
  const benefits = getCustomField(position, 'benefits');
  return Array.isArray(benefits) ? benefits : undefined;
}

export function getSkills(position: Position): string[] | undefined {
  const skills = getCustomField(position, 'skills');
  return Array.isArray(skills) ? skills : undefined;
}

export function getApplicationUrl(position: Position): string | undefined {
  return getCustomField(position, 'application_url') as string | undefined;
}

export function getApplicationEmail(position: Position): string | undefined {
  return getCustomField(position, 'application_email') as string | undefined;
}

export function getWorkingHours(position: Position): string | undefined {
  return getCustomField(position, 'working_hours') as string | undefined;
}

export function getTravelRequired(position: Position): boolean | undefined {
  return getCustomField(position, 'travel_required') as boolean | undefined;
}

export function getVisaSponsorship(position: Position): boolean | undefined {
  return getCustomField(position, 'visa_sponsorship') as boolean | undefined;
}

export function getContactPerson(position: Position): string | undefined {
  return getCustomField(position, 'contact_person') as string | undefined;
}

export function getReportsTo(position: Position): string | undefined {
  return getCustomField(position, 'reports_to') as string | undefined;
}

export function getNumberOfOpenings(position: Position): number | undefined {
  return getCustomField(position, 'number_of_openings') as number | undefined;
}

export function getLanguagesRequired(position: Position): Record<string, string> | Array<{ language: string; level: string }> | undefined {
  return getCustomField(position, 'languages_required') as Record<string, string> | Array<{ language: string; level: string }> | undefined;
}

export function getDesiredRoles(position: Position): string[] | undefined {
  const roles = getCustomField(position, 'desired_roles');
  return Array.isArray(roles) ? roles : undefined;
}

export function getIsRemote(position: Position): boolean | undefined {
  return getCustomField(position, 'is_remote') as boolean | undefined;
}

// Helper functions for visibility display
export function getVisibilityLabel(visibility: JobPositionVisibility): string {
  const labels: Record<JobPositionVisibility, string> = {
    'hidden': 'Hidden',
    'internal': 'Internal',
    'public': 'Public',
  };
  return labels[visibility] || visibility;
}

export function getVisibilityColor(visibility: JobPositionVisibility): string {
  const colors: Record<JobPositionVisibility, string> = {
    'hidden': 'bg-gray-100 text-gray-800',
    'internal': 'bg-blue-100 text-blue-800',
    'public': 'bg-green-100 text-green-800',
  };
  return colors[visibility] || 'bg-gray-100 text-gray-800';
}

// Helper function to get status from stage (for backward compatibility if needed)
export function getStatusFromStage(stage?: JobPositionWorkflowStage): string | null {
  return stage?.status_mapping || null;
}

// Helper function to get status label from stage
export function getStatusLabelFromStage(stage?: JobPositionWorkflowStage): string {
  if (!stage) return 'Unknown';
  const status = stage.status_mapping.toLowerCase();
  const labels: Record<string, string> = {
    'draft': 'Draft',
    'active': 'Active',
    'paused': 'Paused',
    'closed': 'Closed',
    'archived': 'Archived',
  };
  return labels[status] || status;
}

// Helper function to get status color from stage
export function getStatusColorFromStage(stage?: JobPositionWorkflowStage): string {
  if (!stage) return 'bg-gray-100 text-gray-800';
  const status = stage.status_mapping.toLowerCase();
  const colors: Record<string, string> = {
    'draft': 'bg-gray-100 text-gray-800',
    'active': 'bg-green-100 text-green-800',
    'paused': 'bg-orange-100 text-orange-800',
    'closed': 'bg-gray-100 text-gray-800',
    'archived': 'bg-purple-100 text-purple-800',
  };
  return colors[status] || 'bg-gray-100 text-gray-800';
}

// Legacy helper functions (deprecated - use getStatusLabelFromStage/getStatusColorFromStage instead)
/** @deprecated Use getStatusLabelFromStage instead */
export function getStatusLabel(status: string): string {
  const labels: Record<string, string> = {
    'draft': 'Draft',
    'active': 'Active',
    'paused': 'Paused',
    'closed': 'Closed',
    'archived': 'Archived',
  };
  return labels[status.toLowerCase()] || status;
}

/** @deprecated Use getStatusColorFromStage instead */
export function getStatusColor(status: string): string {
  const colors: Record<string, string> = {
    'draft': 'bg-gray-100 text-gray-800',
    'active': 'bg-green-100 text-green-800',
    'paused': 'bg-orange-100 text-orange-800',
    'closed': 'bg-gray-100 text-gray-800',
    'archived': 'bg-purple-100 text-purple-800',
  };
  return colors[status.toLowerCase()] || 'bg-gray-100 text-gray-800';
}
