// Company Interview API service
import { ApiClient } from '../lib/api';

export type InterviewStatus = 'PENDING' | 'IN_PROGRESS' | 'FINISHED' | 'DISCARDED' | 'PAUSED';
export type InterviewType = 'CUSTOM' | 'TECHNICAL' | 'BEHAVIORAL' | 'CULTURAL_FIT' | 'KNOWLEDGE_CHECK' | 'EXPERIENCE_CHECK';
export type InterviewProcessType = 'CANDIDATE_SIGN_UP' | 'CANDIDATE_APPLICATION' | 'SCREENING' | 'INTERVIEW' | 'FEEDBACK';

export type Interview = {
  id: string;
  candidate_id: string;
  candidate_name?: string; // From ReadModel
  candidate_email?: string; // From ReadModel
  required_roles: string[]; // List of CompanyRole IDs (obligatory)
  required_role_names?: string[]; // From ReadModel - List of CompanyRole names
  interview_type: InterviewType;
  interview_mode?: 'AUTOMATIC' | 'AI' | 'MANUAL';
  process_type?: InterviewProcessType;
  status: InterviewStatus;
  job_position_id?: string;
  job_position_title?: string; // From ReadModel
  application_id?: string;
  interview_template_id?: string;
  interview_template_name?: string; // From ReadModel
  workflow_stage_id?: string; // ID of the workflow stage where this interview is conducted
  workflow_stage_name?: string; // From ReadModel
  title?: string;
  description?: string;
  scheduled_at?: string;
  deadline_date?: string; // New field
  started_at?: string;
  finished_at?: string;
  completed_at?: string;
  duration_minutes?: number;
  score?: number;
  notes?: string;
  interviewer_notes?: string;
  candidate_notes?: string;
  feedback?: string;
  interviewers?: string[]; // List of interviewer IDs
  interviewer_names?: string[]; // From ReadModel - List of interviewer names/emails
  metadata?: Record<string, any>;
  created_at: string;
  updated_at: string;
  created_by?: string;
  updated_by?: string;
  link_token?: string;
  link_expires_at?: string;
  shareable_link?: string;
  is_incomplete?: boolean; // True if has scheduled_at but missing required_roles or interviewers
};

export type InterviewListResponse = {
  interviews: Interview[];
  total: number;
  page: number;
  page_size: number;
};

export type InterviewStatsResponse = {
  total_interviews: number;
  scheduled_interviews: number;
  in_progress_interviews: number;
  completed_interviews: number;
  average_score?: number;
  average_duration_minutes?: number;
  // New statistics fields
  pending_to_plan?: number; // No scheduled_at or no interviewers
  planned?: number; // Have scheduled_at and interviewers
  recently_finished?: number; // Finished in last 30 days
  overdue?: number; // deadline_date < now and not finished
  pending_feedback?: number; // Finished but no score or feedback
};

export type InterviewActionResponse = {
  message: string;
  status: string;
  interview_id?: string;
};

export type InterviewScoreSummaryResponse = {
  interview_id: string;
  overall_score?: number;
  total_questions: number;
  answered_questions: number;
  average_answer_score?: number;
  completion_percentage: number;
};

// Interview filter enum values (matches backend InterviewFilterEnum)
export type InterviewFilterEnum = 
  | 'PENDING_TO_PLAN' 
  | 'PLANNED' 
  | 'IN_PROGRESS' 
  | 'RECENTLY_FINISHED' 
  | 'OVERDUE' 
  | 'PENDING_FEEDBACK';

export type InterviewFilters = {
  candidate_id?: string;
  candidate_name?: string; // Search by candidate name
  job_position_id?: string;
  interview_type?: InterviewType | 'all';
  process_type?: InterviewProcessType | 'all';
  status?: InterviewStatus | 'all';
  required_role_id?: string; // Filter by CompanyRole ID
  interviewer_user_id?: string; // Filter by interviewer (CompanyUserId)
  from_date?: string;
  to_date?: string;
  filter_by?: InterviewFilterEnum; // Filter name from InterviewFilterEnum
  limit?: number;
  offset?: number;
};

export type InterviewMode = 'AUTOMATIC' | 'AI' | 'MANUAL';

export type CreateInterviewRequest = {
  candidate_id: string;
  required_roles: string[]; // List of CompanyRole IDs (obligatory)
  interview_type: InterviewType;
  interview_mode: InterviewMode;
  process_type?: InterviewProcessType;
  job_position_id?: string;
  application_id?: string;
  interview_template_id?: string;
  workflow_stage_id?: string; // ID of the workflow stage where this interview is conducted
  title?: string;
  description?: string;
  scheduled_at?: string;
  deadline_date?: string; // New field
  interviewers?: string[];
};

export type UpdateInterviewRequest = {
  title?: string;
  description?: string;
  scheduled_at?: string;
  deadline_date?: string; // New field
  process_type?: InterviewProcessType;
  required_roles?: string[]; // List of CompanyRole IDs
  interviewers?: string[];
  interviewer_notes?: string;
  feedback?: string;
  score?: number;
  notes?: string;
  metadata?: Record<string, any>;
};

export type StartInterviewRequest = {
  started_by?: string;
};

export type FinishInterviewRequest = {
  finished_by?: string;
  score?: number;
  notes?: string;
};

/**
 * Get the company slug from localStorage
 */
function getCompanySlug(): string {
  const slug = localStorage.getItem('company_slug');
  if (!slug) {
    throw new Error('Company slug not found. Please log in again.');
  }
  return slug;
}

/**
 * Get the base path for interview endpoints (company-scoped)
 */
function getInterviewsBasePath(): string {
  return `/${getCompanySlug()}/admin/interviews`;
}

export const companyInterviewService = {
  /**
   * List all interviews for the company
   */
  async listInterviews(filters?: InterviewFilters): Promise<InterviewListResponse> {
    const queryParams = new URLSearchParams();
    if (filters?.candidate_id) queryParams.append('candidate_id', filters.candidate_id);
    if (filters?.candidate_name) queryParams.append('candidate_name', filters.candidate_name);
    if (filters?.job_position_id) queryParams.append('job_position_id', filters.job_position_id);
    if (filters?.interview_type) queryParams.append('interview_type', filters.interview_type);
    if (filters?.process_type) queryParams.append('process_type', filters.process_type);
    if (filters?.status) queryParams.append('status', filters.status);
    if (filters?.required_role_id) queryParams.append('required_role_id', filters.required_role_id);
    if (filters?.interviewer_user_id) queryParams.append('interviewer_user_id', filters.interviewer_user_id);
    if (filters?.from_date) queryParams.append('from_date', filters.from_date);
    if (filters?.to_date) queryParams.append('to_date', filters.to_date);
    if (filters?.filter_by) queryParams.append('filter_by', filters.filter_by);
    if (filters?.limit) queryParams.append('limit', filters.limit.toString());
    if (filters?.offset) queryParams.append('offset', filters.offset.toString());

    const endpoint = `${getInterviewsBasePath()}${queryParams.toString() ? `?${queryParams}` : ''}`;
    return ApiClient.authenticatedRequest<InterviewListResponse>(endpoint);
  },

  /**
   * Get interview statistics for the company
   */
  async getInterviewStats(): Promise<InterviewStatsResponse> {
    return ApiClient.authenticatedRequest<InterviewStatsResponse>(`${getInterviewsBasePath()}/statistics`);
  },

  /**
   * Get interviews by date range for calendar
   */
  async getInterviewCalendar(fromDate: string, toDate: string): Promise<Interview[]> {
    const queryParams = new URLSearchParams();
    queryParams.append('from_date', fromDate);
    queryParams.append('to_date', toDate);
    queryParams.append('filter_by', 'scheduled');
    return ApiClient.authenticatedRequest<Interview[]>(`${getInterviewsBasePath()}/calendar?${queryParams}`);
  },

  /**
   * Get overdue interviews
   */
  async getOverdueInterviews(): Promise<Interview[]> {
    return ApiClient.authenticatedRequest<Interview[]>(`${getInterviewsBasePath()}/overdue`);
  },

  /**
   * Get a single interview by ID (for editing - only interview fields)
   */
  async getInterview(interviewId: string): Promise<Interview> {
    return ApiClient.authenticatedRequest<Interview>(`${getInterviewsBasePath()}/${interviewId}`);
  },

  /**
   * Get a single interview by ID with full denormalized information (for viewing)
   */
  async getInterviewView(interviewId: string): Promise<Interview> {
    return ApiClient.authenticatedRequest<Interview>(`${getInterviewsBasePath()}/${interviewId}/view`);
  },

  /**
   * Create a new interview
   */
  async createInterview(data: CreateInterviewRequest): Promise<InterviewActionResponse> {
    return ApiClient.authenticatedRequest<InterviewActionResponse>(`${getInterviewsBasePath()}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
  },

  /**
   * Update an interview
   */
  async updateInterview(interviewId: string, data: UpdateInterviewRequest): Promise<InterviewActionResponse> {
    return ApiClient.authenticatedRequest<InterviewActionResponse>(`${getInterviewsBasePath()}/${interviewId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
  },

  /**
   * Cancel an interview (updates status to DISCARDED)
   */
  async cancelInterview(interviewId: string): Promise<InterviewActionResponse> {
    return ApiClient.authenticatedRequest<InterviewActionResponse>(`${getInterviewsBasePath()}/${interviewId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: 'DISCARDED' }),
    });
  },

  /**
   * Start an interview
   */
  async startInterview(interviewId: string, data?: StartInterviewRequest): Promise<InterviewActionResponse> {
    return ApiClient.authenticatedRequest<InterviewActionResponse>(`${getInterviewsBasePath()}/${interviewId}/start`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data || {}),
    });
  },

  /**
   * Finish an interview
   */
  async finishInterview(interviewId: string, data?: FinishInterviewRequest): Promise<InterviewActionResponse> {
    return ApiClient.authenticatedRequest<InterviewActionResponse>(`${getInterviewsBasePath()}/${interviewId}/finish`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data || {}),
    });
  },

  /**
   * Get interviews for a specific candidate
   */
  async getInterviewsByCandidate(
    candidateId: string,
    filters?: { status?: InterviewStatus; interview_type?: InterviewType }
  ): Promise<Interview[]> {
    const queryParams = new URLSearchParams();
    if (filters?.status) queryParams.append('status', filters.status);
    if (filters?.interview_type) queryParams.append('interview_type', filters.interview_type);

    const endpoint = `${getInterviewsBasePath()}/candidate/${candidateId}${queryParams.toString() ? `?${queryParams}` : ''}`;
    return ApiClient.authenticatedRequest<Interview[]>(endpoint);
  },

  /**
   * Get scheduled interviews
   */
  async getScheduledInterviews(filters?: {
    from_date?: string;
    to_date?: string;
    interviewer?: string;
  }): Promise<Interview[]> {
    const queryParams = new URLSearchParams();
    if (filters?.from_date) queryParams.append('from_date', filters.from_date);
    if (filters?.to_date) queryParams.append('to_date', filters.to_date);
    if (filters?.interviewer) queryParams.append('interviewer', filters.interviewer);

    const endpoint = `${getInterviewsBasePath()}/scheduled${queryParams.toString() ? `?${queryParams}` : ''}`;
    return ApiClient.authenticatedRequest<Interview[]>(endpoint);
  },

  /**
   * Get interview score summary
   */
  async getInterviewScoreSummary(interviewId: string): Promise<InterviewScoreSummaryResponse> {
    return ApiClient.authenticatedRequest<InterviewScoreSummaryResponse>(
      `${getInterviewsBasePath()}/${interviewId}/score-summary`
    );
  },

  /**
   * Generate a shareable link for an interview
   */
  async generateInterviewLink(
    interviewId: string,
    expiresInDays: number = 30
  ): Promise<{ message: string; status: string; link?: string; link_token?: string; interview_id?: string; expires_in_days?: number; expires_at?: string }> {
    return ApiClient.authenticatedRequest<{ message: string; status: string; link?: string; link_token?: string; interview_id?: string; expires_in_days?: number; expires_at?: string }>(
      `${getInterviewsBasePath()}/${interviewId}/generate-link?expires_in_days=${expiresInDays}`,
      {
        method: 'POST',
      }
    );
  },
};

