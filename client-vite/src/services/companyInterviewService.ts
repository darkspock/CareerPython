// Company Interview API service
import { ApiClient } from '../lib/api';

export type InterviewStatus = 'SCHEDULED' | 'IN_PROGRESS' | 'COMPLETED' | 'CANCELLED' | 'PENDING';
export type InterviewType = 'EXTENDED_PROFILE' | 'POSITION_INTERVIEW' | 'TECHNICAL' | 'BEHAVIORAL' | 'CULTURAL_FIT';

export type Interview = {
  id: string;
  candidate_id: string;
  interview_type: InterviewType;
  status: InterviewStatus;
  job_position_id?: string;
  application_id?: string;
  interview_template_id?: string;
  workflow_stage_id?: string; // ID of the workflow stage where this interview is conducted
  title?: string;
  description?: string;
  scheduled_at?: string;
  started_at?: string;
  completed_at?: string;
  score?: number;
  notes?: string;
  interviewers?: string[];
  metadata?: Record<string, any>;
  created_at: string;
  updated_at: string;
  created_by?: string;
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

export type InterviewFilters = {
  candidate_id?: string;
  job_position_id?: string;
  interview_type?: InterviewType;
  status?: InterviewStatus;
  from_date?: string;
  to_date?: string;
  limit?: number;
  offset?: number;
};

export type CreateInterviewRequest = {
  candidate_id: string;
  interview_type: InterviewType;
  job_position_id?: string;
  application_id?: string;
  interview_template_id?: string;
  workflow_stage_id?: string; // ID of the workflow stage where this interview is conducted
  title?: string;
  description?: string;
  scheduled_at?: string;
  interviewers?: string[];
};

export type UpdateInterviewRequest = {
  title?: string;
  description?: string;
  scheduled_at?: string;
  interviewers?: string[];
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

export const companyInterviewService = {
  /**
   * List all interviews for the company
   */
  async listInterviews(filters?: InterviewFilters): Promise<InterviewListResponse> {
    const queryParams = new URLSearchParams();
    if (filters?.candidate_id) queryParams.append('candidate_id', filters.candidate_id);
    if (filters?.job_position_id) queryParams.append('job_position_id', filters.job_position_id);
    if (filters?.interview_type) queryParams.append('interview_type', filters.interview_type);
    if (filters?.status) queryParams.append('status', filters.status);
    if (filters?.from_date) queryParams.append('from_date', filters.from_date);
    if (filters?.to_date) queryParams.append('to_date', filters.to_date);
    if (filters?.limit) queryParams.append('limit', filters.limit.toString());
    if (filters?.offset) queryParams.append('offset', filters.offset.toString());

    const endpoint = `/api/company/interviews${queryParams.toString() ? `?${queryParams}` : ''}`;
    return ApiClient.authenticatedRequest<InterviewListResponse>(endpoint);
  },

  /**
   * Get interview statistics for the company
   */
  async getInterviewStats(): Promise<InterviewStatsResponse> {
    return ApiClient.authenticatedRequest<InterviewStatsResponse>('/api/company/interviews/stats');
  },

  /**
   * Get a single interview by ID
   */
  async getInterview(interviewId: string): Promise<Interview> {
    return ApiClient.authenticatedRequest<Interview>(`/api/company/interviews/${interviewId}`);
  },

  /**
   * Create a new interview
   */
  async createInterview(data: CreateInterviewRequest): Promise<InterviewActionResponse> {
    return ApiClient.authenticatedRequest<InterviewActionResponse>('/api/company/interviews', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
  },

  /**
   * Update an interview
   */
  async updateInterview(interviewId: string, data: UpdateInterviewRequest): Promise<InterviewActionResponse> {
    return ApiClient.authenticatedRequest<InterviewActionResponse>(`/api/company/interviews/${interviewId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
  },

  /**
   * Start an interview
   */
  async startInterview(interviewId: string, data?: StartInterviewRequest): Promise<InterviewActionResponse> {
    return ApiClient.authenticatedRequest<InterviewActionResponse>(`/api/company/interviews/${interviewId}/start`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data || {}),
    });
  },

  /**
   * Finish an interview
   */
  async finishInterview(interviewId: string, data?: FinishInterviewRequest): Promise<InterviewActionResponse> {
    return ApiClient.authenticatedRequest<InterviewActionResponse>(`/api/company/interviews/${interviewId}/finish`, {
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

    const endpoint = `/api/company/interviews/candidate/${candidateId}${queryParams.toString() ? `?${queryParams}` : ''}`;
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

    const endpoint = `/api/company/interviews/scheduled${queryParams.toString() ? `?${queryParams}` : ''}`;
    return ApiClient.authenticatedRequest<Interview[]>(endpoint);
  },

  /**
   * Get interview score summary
   */
  async getInterviewScoreSummary(interviewId: string): Promise<InterviewScoreSummaryResponse> {
    return ApiClient.authenticatedRequest<InterviewScoreSummaryResponse>(
      `/api/company/interviews/${interviewId}/score-summary`
    );
  },
};

