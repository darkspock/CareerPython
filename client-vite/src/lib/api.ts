import { API_BASE_URL } from '../config/api';
import type {
  UpdateResumeContentRequest,
  AddVariableSectionRequest,
  UpdateVariableSectionRequest,
  RemoveVariableSectionRequest,
  ReorderVariableSectionsRequest
} from '../types/resume';

export class ApiClient {
  private static baseURL = API_BASE_URL;

  static async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;

    // Only set Content-Type for requests with a body
    const hasBody = options.body !== undefined && options.body !== null;
    const headers: HeadersInit = {
      ...(hasBody && { 'Content-Type': 'application/json' }),
      ...options.headers,
    };

    let response: Response;
    try {
      response = await fetch(url, {
        ...options,
        headers,
      });
    } catch (error: any) {
      // Handle network errors (CORS, connection refused, etc.)
      if (error instanceof TypeError && error.message === 'Failed to fetch') {
        throw new Error(`Network error: Unable to reach server at ${url}. Please check if the server is running and CORS is configured correctly.`);
      }
      throw error;
    }

    if (!response.ok) {
      let errorMessage = `API Error: ${response.status} ${response.statusText}`;

      try {
        const errorData = await response.json();

        // Handle new error format from global exception handler
        if (errorData.error && errorData.error.message) {
          errorMessage = errorData.error.message;
        }
        // Handle validation errors (array of error objects)
        else if (Array.isArray(errorData.detail)) {
          const validationErrors = errorData.detail.map((err: any) => {
            const fieldPath = Array.isArray(err.loc) ? err.loc.slice(1).join('.') : 'field';
            return `${fieldPath}: ${err.msg}`;
          });
          errorMessage = `Validation errors: ${validationErrors.join(', ')}`;
        }
        // Fallback to old format for compatibility
        else if (errorData.detail) {
          errorMessage = typeof errorData.detail === 'string' ? errorData.detail : JSON.stringify(errorData.detail);
        }
      } catch (e) {
        // Si no se puede parsear el JSON, usar el mensaje por defecto
      }

      throw new Error(errorMessage);
    }

    // Handle 204 No Content responses
    if (response.status === 204 || response.headers.get('content-length') === '0') {
      return undefined as T;
    }

    // Check if response has JSON content
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('application/json')) {
      return response.json();
    }

    // Return undefined for non-JSON responses
    return undefined as T;
  }

  static async get<T>(endpoint: string, options?: RequestInit): Promise<T> {
    return this.request<T>(endpoint, { ...options, method: 'GET' });
  }

  static async post<T>(
    endpoint: string,
    data?: any,
    options?: RequestInit
  ): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  static async postFormData<T>(
    endpoint: string,
    formData: FormData,
    options?: RequestInit
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;

    const response = await fetch(url, {
      method: 'POST',
      body: formData,
      // Don't set Content-Type for FormData - let browser set it with boundary
      ...options,
    });

    if (!response.ok) {
      let errorMessage = `API Error: ${response.status} ${response.statusText}`;

      try {
        const errorData = await response.json();

        // Handle new error format from global exception handler
        if (errorData.error && errorData.error.message) {
          errorMessage = errorData.error.message;
        }
        // Handle validation errors (array of error objects)
        else if (Array.isArray(errorData.detail)) {
          const validationErrors = errorData.detail.map((err: any) => {
            const fieldPath = Array.isArray(err.loc) ? err.loc.slice(1).join('.') : 'field';
            return `${fieldPath}: ${err.msg}`;
          });
          errorMessage = `Validation errors: ${validationErrors.join(', ')}`;
        }
        // Fallback to old format for compatibility
        else if (errorData.detail) {
          errorMessage = typeof errorData.detail === 'string' ? errorData.detail : JSON.stringify(errorData.detail);
        }
      } catch (e) {
        // Si no se puede parsear el JSON, usar el mensaje por defecto
      }

      throw new Error(errorMessage);
    }

    return response.json();
  }

  static async put<T>(
    endpoint: string,
    data?: any,
    options?: RequestInit
  ): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  static async patch<T>(
    endpoint: string,
    data?: any,
    options?: RequestInit
  ): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: 'PATCH',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  static async delete<T>(endpoint: string, options?: RequestInit): Promise<T> {
    return this.request<T>(endpoint, { ...options, method: 'DELETE' });
  }

  // Helper for authenticated requests
  static async authenticatedRequest<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const token = localStorage.getItem('access_token');
    return this.request<T>(endpoint, {
      ...options,
      headers: {
        Authorization: token ? `Bearer ${token}` : '',
        ...options.headers,
      },
    });
  }
}

// Convenience functions for common API patterns
export const api = {
  // Landing page
  createAccountFromLanding: (formData: FormData) =>
    ApiClient.postFormData('/landing/create-account', formData),

  // Registration Flow with email verification
  initiateRegistration: (formData: FormData) =>
    ApiClient.postFormData<{
      success: boolean;
      message: string;
      registration_id: string;
    }>('/candidate/registration', formData),

  verifyRegistration: (token: string) =>
    ApiClient.get<{
      success: boolean;
      message: string;
      user_id: string | null;
      candidate_id: string | null;
      is_new_user: boolean;
      has_job_application: boolean;
      job_position_id: string | null;
      access_token: string | null;
      redirect_url: string;
      wants_cv_help: boolean;
      has_pdf: boolean;
    }>(`/candidate/registration/verify/${token}`),

  getRegistrationStatus: (registrationId: string) =>
    ApiClient.get<{
      registration_id: string;
      status: string;
      processing_status: string;
      is_verified: boolean;
      is_expired: boolean;
      has_pdf: boolean;
      preview_data: {
        name?: string;
        email?: string;
        phone?: string;
      } | null;
    }>(`/candidate/registration/${registrationId}/status`),

  // Files
  uploadPDF: (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    return ApiClient.authenticatedRequest('/files/upload-pdf', {
      method: 'POST',
      body: formData,
    });
  },

  // Auth
  login: (credentials: { username: string; password: string }) => {
    const formData = new URLSearchParams();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);
    return ApiClient.request('/candidate/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: formData,
    });
  },

  adminLogin: (credentials: { username: string; password: string }) => {
    const formData = new URLSearchParams();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);
    return ApiClient.request('/admin/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: formData,
    });
  },

  companyLogin: (credentials: { username: string; password: string }) => {
    const formData = new URLSearchParams();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);
    return ApiClient.request('/companies/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: formData,
    });
  },

  register: (userData: { email: string; password: string; full_name?: string }) =>
    ApiClient.post('/auth/register', userData),

  resetPasswordWithToken: (token: string, newPassword: string) =>
    ApiClient.post('/user/password-reset/confirm', {
      reset_token: token,
      new_password: newPassword,
    }),

  // Candidates
  getCandidates: () =>
    ApiClient.authenticatedRequest('/admin/candidates'),

  updateCandidateStatus: (candidateId: string, status: string) =>
    ApiClient.authenticatedRequest(`/admin/candidates/${candidateId}/status`, {
      method: 'PUT',
      body: JSON.stringify({ status }),
    }),

  createCandidate: (candidateData: any) =>
    ApiClient.authenticatedRequest('/candidate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(candidateData),
    }),

  // Profile
  getMyProfile: () =>
    ApiClient.authenticatedRequest('/candidate/profile'),

  getMyProfileSummary: () =>
    ApiClient.authenticatedRequest('/candidate/profile/summary'),

  // Applications (Global - all applications across all companies)
  getMyApplications: (params?: { status?: string; limit?: number }) => {
    let endpoint = '/candidate/application';
    if (params) {
      const queryParams = new URLSearchParams();
      if (params.status) queryParams.append('status', params.status);
      if (params.limit) queryParams.append('limit', params.limit.toString());
      const queryString = queryParams.toString();
      if (queryString) {
        endpoint += `?${queryString}`;
      }
    }
    return ApiClient.authenticatedRequest<{
      id: string;
      job_title: string;
      company_name: string;
      status: string;
      created_at: string;
      updated_at: string | null;
      applied_at: string | null;
      has_customized_content: boolean;
    }[]>(endpoint);
  },

  // Company-scoped Applications (applications to a specific company)
  getCompanyApplications: (companySlug: string, params?: { status?: string; limit?: number }) => {
    let endpoint = `/${companySlug}/candidate/applications`;
    if (params) {
      const queryParams = new URLSearchParams();
      if (params.status) queryParams.append('status', params.status);
      if (params.limit) queryParams.append('limit', params.limit.toString());
      const queryString = queryParams.toString();
      if (queryString) {
        endpoint += `?${queryString}`;
      }
    }
    return ApiClient.authenticatedRequest<{
      id: string;
      job_position_id: string;
      job_title: string;
      company_name: string;
      status: string;
      task_status: string;
      created_at: string;
      updated_at: string | null;
      applied_at: string | null;
      has_customized_content: boolean;
    }[]>(endpoint);
  },

  // Apply to a position at a specific company
  applyToPosition: (companySlug: string, positionId: string, coverLetter?: string) => {
    let endpoint = `/${companySlug}/candidate/apply/${positionId}`;
    if (coverLetter) {
      endpoint += `?cover_letter=${encodeURIComponent(coverLetter)}`;
    }
    return ApiClient.authenticatedRequest<{
      message: string;
      position_id: string;
      company: {
        id: string;
        name: string;
        slug: string;
      };
    }>(endpoint, { method: 'POST' });
  },

  // Get company info for candidate portal
  getCompanyInfoForCandidate: (companySlug: string) =>
    ApiClient.request<{
      id: string;
      name: string;
      slug: string;
      logo_url: string | null;
    }>(`/${companySlug}/candidate/company-info`),

  // Get positions at a specific company (public - candidate portal)
  getCompanyPositions: (companySlug: string) =>
    ApiClient.request<{
      company: {
        id: string;
        name: string;
        slug: string;
      };
      positions: Array<{
        id: string;
        title: string;
        description: string;
        location: string;
        employment_type: string;
        status: string;
      }>;
      total: number;
    }>(`/${companySlug}/candidate/positions`),

  // ==================== PUBLIC COMPANY-SCOPED API ====================
  // These endpoints are public (no authentication required) and use company slug

  // Get company basic info (public)
  getPublicCompanyInfo: (companySlug: string) =>
    ApiClient.request<{
      id: string;
      name: string;
      slug: string;
      logo_url: string | null;
    }>(`/${companySlug}`),

  // List published positions at a company (public)
  getPublicCompanyPositions: (companySlug: string, params?: {
    search?: string;
    page?: number;
    page_size?: number;
  }) => {
    let endpoint = `/${companySlug}/positions`;
    if (params) {
      const queryParams = new URLSearchParams();
      if (params.search) queryParams.append('search', params.search);
      if (params.page) queryParams.append('page', params.page.toString());
      if (params.page_size) queryParams.append('page_size', params.page_size.toString());
      const queryString = queryParams.toString();
      if (queryString) endpoint += `?${queryString}`;
    }
    return ApiClient.request<{
      company: {
        id: string;
        name: string;
        slug: string;
        logo_url: string | null;
      };
      positions: Array<{
        id: string;
        title: string;
        description: string;
        location: string;
        employment_type: string;
        job_category: string;
        status: string;
      }>;
      total: number;
      page: number;
      page_size: number;
      total_pages: number;
    }>(endpoint);
  },

  // Get a specific position at a company (public)
  getPublicCompanyPosition: (companySlug: string, positionId: string) =>
    ApiClient.request<{
      id: string;
      title: string;
      description: string;
      location: string;
      employment_type: string;
      job_category: string;
      required_experience: string | null;
      salary_range: string | null;
      benefits: string | null;
      requirements: string | null;
      responsibilities: string | null;
      status: string;
      public_slug: string | null;
      created_at: string | null;
      company: {
        id: string;
        name: string;
        slug: string;
        logo_url: string | null;
      };
    }>(`/${companySlug}/positions/${positionId}`),

  // Get company about page (public)
  getPublicCompanyAbout: (companySlug: string) =>
    ApiClient.request<{
      company: {
        id: string;
        name: string;
        slug: string;
        logo_url: string | null;
      };
      page: {
        type: string;
        title: string;
        content: string | null;
        sections: Array<{
          title: string;
          content: string;
        }>;
      };
    }>(`/${companySlug}/about`),

  updateMyProfile: (candidateData: any) =>
    ApiClient.authenticatedRequest('/candidate/profile', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(candidateData),
    }),

  // PDF Analysis - Job-based processing
  getAnalysisStatus: (jobId: string) =>
    ApiClient.authenticatedRequest(`/api/files/analysis-status/${jobId}`),

  getAnalysisResults: (jobId: string) =>
    ApiClient.authenticatedRequest(`/api/files/analysis-results/${jobId}`),

  // Job Status Polling - New unified endpoint for frontend polling
  getJobStatus: (jobId: string) =>
    ApiClient.get(`/api/jobs/${jobId}/status`),

  getJobResults: (jobId: string) =>
    ApiClient.get(`/api/jobs/${jobId}/results`),

  // Work Experience
  getExperiences: () =>
    ApiClient.authenticatedRequest('/candidate/experience'),

  createExperience: (experienceData: any) =>
    ApiClient.authenticatedRequest('/candidate/experience', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(experienceData),
    }),

  createMultipleExperiences: (experiences: any[]) =>
    ApiClient.authenticatedRequest('/candidate/experience/bulk', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(experiences),
    }),

  updateExperience: (experienceId: string, experienceData: any) =>
    ApiClient.authenticatedRequest(`/candidate/experience/${experienceId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(experienceData),
    }),

  // Education
  getEducations: () =>
    ApiClient.authenticatedRequest('/candidate/education'),

  createEducation: (educationData: any) =>
    ApiClient.authenticatedRequest('/candidate/education', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(educationData),
    }),

  // Projects
  getProjects: () =>
    ApiClient.authenticatedRequest('/candidate/projects'),

  createProject: (projectData: any) =>
    ApiClient.authenticatedRequest('/candidate/projects', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(projectData),
    }),

  // Resume Management
  getResumes: (params?: { resume_type?: string; limit?: number }) => {
    let endpoint = '/candidate/resume/';  // Fixed: Added trailing slash
    if (params) {
      const queryParams = new URLSearchParams();
      if (params.resume_type) queryParams.append('resume_type', params.resume_type);
      if (params.limit) queryParams.append('limit', params.limit.toString());
      if (queryParams.toString()) endpoint += `?${queryParams}`;
    }
    return ApiClient.authenticatedRequest(endpoint);
  },

  getResumeById: (resumeId: string) =>
    ApiClient.authenticatedRequest(`/candidate/resume/${resumeId}`),

  // Alias for getResumeById for consistency with editor
  getResume: (resumeId: string) =>
    ApiClient.authenticatedRequest(`/candidate/resume/${resumeId}`),

  getResumeContent: (resumeId: string, params?: {
    include_ai_content?: boolean;
    include_custom_content?: boolean;
    include_formatting?: boolean;
  }) => {
    let endpoint = `/candidate/resume/${resumeId}/content`;
    if (params) {
      const queryParams = new URLSearchParams();
      if (params.include_ai_content !== undefined) {
        queryParams.append('include_ai_content', params.include_ai_content.toString());
      }
      if (params.include_custom_content !== undefined) {
        queryParams.append('include_custom_content', params.include_custom_content.toString());
      }
      if (params.include_formatting !== undefined) {
        queryParams.append('include_formatting', params.include_formatting.toString());
      }
      if (queryParams.toString()) endpoint += `?${queryParams}`;
    }
    return ApiClient.authenticatedRequest(endpoint);
  },

  createGeneralResume: (data: {
    candidate_id: string;
    name: string;
    general_data?: Record<string, any>;
    include_ai_enhancement?: boolean;
  }) =>
    ApiClient.authenticatedRequest('/candidate/resume/general', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    }),

  // Simplified create resume function that automatically gets candidate_id
  createResume: async (data: {
    name: string;
    general_data?: Record<string, any>;
    include_ai_enhancement?: boolean;
  }) => {
    try {
      // First get the candidate profile to extract candidate_id
      const profile = await ApiClient.authenticatedRequest('/candidate/profile');

      // Then create the resume with the candidate_id
      return ApiClient.authenticatedRequest('/candidate/resume/general', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          candidate_id: (profile as { id?: string })?.id || '',
          ...data
        }),
      });
    } catch (error) {
      console.error('Error creating resume:', error);
      throw error;
    }
  },

  updateResumeContent: (resumeId: string, data: UpdateResumeContentRequest) =>
    ApiClient.authenticatedRequest(`/candidate/resume/${resumeId}/content`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    }),

  // Variable Section Management - New endpoints for hybrid structure
  addVariableSection: (resumeId: string, data: AddVariableSectionRequest) =>
    ApiClient.authenticatedRequest(`/candidate/resume/${resumeId}/sections`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    }),

  updateVariableSection: (resumeId: string, data: UpdateVariableSectionRequest) =>
    ApiClient.authenticatedRequest(`/candidate/resume/${resumeId}/sections/${data.section_key}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    }),

  removeVariableSection: (resumeId: string, data: RemoveVariableSectionRequest) =>
    ApiClient.authenticatedRequest(`/candidate/resume/${resumeId}/sections/${data.section_key}`, {
      method: 'DELETE',
    }),

  reorderVariableSections: (resumeId: string, data: ReorderVariableSectionsRequest) =>
    ApiClient.authenticatedRequest(`/candidate/resume/${resumeId}/sections/reorder`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    }),

  updateResumeName: (resumeId: string, data: { name: string }) =>
    ApiClient.authenticatedRequest(`/candidate/resume/${resumeId}/name`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    }),

  deleteResume: (resumeId: string) =>
    ApiClient.authenticatedRequest(`/candidate/resume/${resumeId}`, {
      method: 'DELETE',
    }),

  duplicateResume: (resumeId: string, newName: string) =>
    ApiClient.authenticatedRequest(`/candidate/resume/${resumeId}/duplicate?new_name=${encodeURIComponent(newName)}`, {
      method: 'POST',
    }),

  getResumeStatistics: () =>
    ApiClient.authenticatedRequest('/candidate/resume/stats'),

  bulkDeleteResumes: (resumeIds: string[]) => {
    const queryParams = resumeIds.map(id => `resume_ids=${encodeURIComponent(id)}`).join('&');
    return ApiClient.authenticatedRequest(`/candidate/resume/bulk-delete?${queryParams}`, {
      method: 'POST',
    });
  },

  // Resume Preview & Export
  generateResumePreview: (resumeId: string, data: {
    template?: string;
    format_type?: string;
    highlight_missing?: boolean;
    include_download_options?: boolean;
    sections_to_include?: string[];
    custom_css?: string;
  }) =>
    ApiClient.authenticatedRequest(`/candidate/resume/${resumeId}/preview`, {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  getResumePreviewHtml: (resumeId: string, params?: {
    template?: string;
    highlight_missing?: boolean;
    custom_css?: string;
  }) => {
    let endpoint = `/candidate/resume/${resumeId}/preview/html`;
    if (params) {
      const queryParams = new URLSearchParams();
      if (params.template) queryParams.append('template', params.template);
      if (params.highlight_missing !== undefined) {
        queryParams.append('highlight_missing', params.highlight_missing.toString());
      }
      if (params.custom_css) queryParams.append('custom_css', params.custom_css);
      if (queryParams.toString()) endpoint += `?${queryParams}`;
    }
    return fetch(`${ApiClient['baseURL']}${endpoint}`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`,
      },
    });
  },

  exportResume: (resumeId: string, data: {
    format_type?: string;
    template?: string;
    include_ai_enhancement?: boolean;
    custom_filename?: string;
    additional_metadata?: Record<string, any>;
  }) =>
    ApiClient.authenticatedRequest(`/candidate/resume/${resumeId}/export`, {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  exportResumeDirectly: (resumeId: string, data: {
    format_type?: string;
    template?: string;
    include_ai_enhancement?: boolean;
    custom_filename?: string;
    additional_metadata?: Record<string, any>;
  }) => {
    return fetch(`${ApiClient['baseURL']}/candidate/resume/${resumeId}/export-direct`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${localStorage.getItem('access_token')}`,
      },
      body: JSON.stringify(data),
    });
  },

  downloadResume: (resumeId: string, downloadId: string) => {
    return fetch(`${ApiClient['baseURL']}/candidate/resume/${resumeId}/export/${downloadId}`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`,
      },
    });
  },

  getTemplateOptions: () =>
    ApiClient.get('/candidate/resume/templates'),

  getResumeExportHistory: (resumeId: string, daysBack?: number) => {
    let endpoint = `/candidate/resume/${resumeId}/export-history`;
    if (daysBack) endpoint += `?days_back=${daysBack}`;
    return ApiClient.authenticatedRequest(endpoint);
  },

  getResumeCompletenessAnalysis: (resumeId: string) =>
    ApiClient.authenticatedRequest(`/candidate/resume/${resumeId}/completeness-analysis`),

  // Interviews - CRUD Operations
  getInterviews: (params?: {
    status?: string;
    type?: string;
    page?: number;
    page_size?: number;
    sort_by?: string;
    sort_order?: string;
  }) => {
    let endpoint = '/interviews';
    if (params) {
      const queryParams = new URLSearchParams();
      if (params.status) queryParams.append('status', params.status);
      if (params.type) queryParams.append('type', params.type);
      if (params.page) queryParams.append('page', params.page.toString());
      if (params.page_size) queryParams.append('page_size', params.page_size.toString());
      if (params.sort_by) queryParams.append('sort_by', params.sort_by);
      if (params.sort_order) queryParams.append('sort_order', params.sort_order);
      if (queryParams.toString()) endpoint += `?${queryParams}`;
    }
    return ApiClient.authenticatedRequest(endpoint);
  },

  getMyInterviews: () =>
    ApiClient.authenticatedRequest('/interviews/simple'),

  getInterview: (interviewId: string) =>
    ApiClient.authenticatedRequest(`/interviews/${interviewId}`),

  createInterview: (data: {
    interview_type: string;
    template_id?: string;
    scheduled_at?: string;
    notes?: string;
    metadata?: Record<string, any>;
  }) =>
    ApiClient.authenticatedRequest('/interviews', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  updateInterview: (interviewId: string, data: {
    status?: string;
    scheduled_at?: string;
    notes?: string;
    metadata?: Record<string, any>;
  }) =>
    ApiClient.authenticatedRequest(`/interviews/${interviewId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),

  deleteInterview: (interviewId: string) =>
    ApiClient.authenticatedRequest(`/interviews/${interviewId}`, {
      method: 'DELETE',
    }),

  // Interview Progress & Status
  getActiveInterview: () =>
    ApiClient.authenticatedRequest('/interviews/active'),

  getInterviewProgress: (interviewId: string) =>
    ApiClient.authenticatedRequest(`/interviews/${interviewId}/progress`),

  getInterviewHistory: (interviewId: string, params?: {
    include_answers?: boolean;
    include_metadata?: boolean;
  }) => {
    let endpoint = `/interviews/${interviewId}/history`;
    if (params) {
      const queryParams = new URLSearchParams();
      if (params.include_answers !== undefined) {
        queryParams.append('include_answers', params.include_answers.toString());
      }
      if (params.include_metadata !== undefined) {
        queryParams.append('include_metadata', params.include_metadata.toString());
      }
      if (queryParams.toString()) endpoint += `?${queryParams}`;
    }
    return ApiClient.authenticatedRequest(endpoint);
  },

  // Interview Templates
  getInterviewTemplates: (params?: {
    search_term?: string;
    interview_type?: string;
    difficulty_level?: string;
    is_active?: boolean;
    page?: number;
    page_size?: number;
    sort_by?: string;
    sort_order?: string;
  }) => {
    let endpoint = '/interviews/templates/';
    if (params) {
      const queryParams = new URLSearchParams();
      if (params.search_term) queryParams.append('search_term', params.search_term);
      if (params.interview_type) queryParams.append('interview_type', params.interview_type);
      if (params.difficulty_level) queryParams.append('difficulty_level', params.difficulty_level);
      if (params.is_active !== undefined) queryParams.append('is_active', params.is_active.toString());
      if (params.page) queryParams.append('page', params.page.toString());
      if (params.page_size) queryParams.append('page_size', params.page_size.toString());
      if (params.sort_by) queryParams.append('sort_by', params.sort_by);
      if (params.sort_order) queryParams.append('sort_order', params.sort_order);
      if (queryParams.toString()) endpoint += `?${queryParams}`;
    }
    return ApiClient.authenticatedRequest(endpoint);
  },

  getRecommendedTemplates: (params?: {
    interview_type?: string;
    membership_level?: string;
    max_recommendations?: number;
    include_reasoning?: boolean;
  }) => {
    let endpoint = '/interviews/templates/recommended';
    if (params) {
      const queryParams = new URLSearchParams();
      if (params.interview_type) queryParams.append('interview_type', params.interview_type);
      if (params.membership_level) queryParams.append('membership_level', params.membership_level);
      if (params.max_recommendations) queryParams.append('max_recommendations', params.max_recommendations.toString());
      if (params.include_reasoning !== undefined) queryParams.append('include_reasoning', params.include_reasoning.toString());
      if (queryParams.toString()) endpoint += `?${queryParams}`;
    }
    return ApiClient.authenticatedRequest(endpoint);
  },

  getInterviewTemplate: (templateId: string) =>
    ApiClient.authenticatedRequest(`/interviews/templates/${templateId}`),

  previewTemplate: (templateId: string, maxQuestions?: number) => {
    let endpoint = `/interviews/templates/${templateId}/preview`;
    if (maxQuestions) endpoint += `?max_questions=${maxQuestions}`;
    return ApiClient.authenticatedRequest(endpoint);
  },

  startInterviewFromTemplate: (templateId: string, data?: {
    scheduled_at?: string;
    notes?: string;
  }) =>
    ApiClient.authenticatedRequest(`/interviews/templates/${templateId}/start`, {
      method: 'POST',
      body: JSON.stringify(data || {}),
    }),

  // AI Interview Features
  getAIInterviewFeaturesStatus: () =>
    ApiClient.authenticatedRequest('/interviews/ai-features/status'),

  startAIEnhancedInterview: (data: {
    candidate_data: Record<string, any>;
    interview_type?: string;
  }) =>
    ApiClient.authenticatedRequest('/interviews/ai-enhanced/start', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  startAIInterview: (interviewId: string, data: {
    interview_id: string;
    candidate_data: Record<string, any>;
  }) =>
    ApiClient.authenticatedRequest(`/interviews/${interviewId}/start-ai`, {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  processInterviewAnswer: (interviewId: string, data: {
    question_id: string;
    answer_text: string;
  }) =>
    ApiClient.authenticatedRequest(`/interviews/${interviewId}/answer`, {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  pauseInterview: (interviewId: string, reason?: string) =>
    ApiClient.authenticatedRequest(`/interviews/${interviewId}/pause`, {
      method: 'POST',
      body: JSON.stringify({ reason }),
    }),

  resumeInterview: (interviewId: string) =>
    ApiClient.authenticatedRequest(`/interviews/${interviewId}/resume`, {
      method: 'POST',
    }),

  getInterviewAIAnalysis: (interviewId: string) =>
    ApiClient.authenticatedRequest(`/interviews/${interviewId}/ai-analysis`),

  // Interview Analytics
  getInterviewAnalyticsOverview: (params?: {
    period?: string;
    start_date?: string;
    end_date?: string;
    include_trends?: boolean;
    include_comparisons?: boolean;
  }) => {
    let endpoint = '/interviews/analytics/overview';
    if (params) {
      const queryParams = new URLSearchParams();
      if (params.period) queryParams.append('period', params.period);
      if (params.start_date) queryParams.append('start_date', params.start_date);
      if (params.end_date) queryParams.append('end_date', params.end_date);
      if (params.include_trends !== undefined) queryParams.append('include_trends', params.include_trends.toString());
      if (params.include_comparisons !== undefined) queryParams.append('include_comparisons', params.include_comparisons.toString());
      if (queryParams.toString()) endpoint += `?${queryParams}`;
    }
    return ApiClient.authenticatedRequest(endpoint);
  },

  getPerformanceReport: (params?: {
    start_date?: string;
    end_date?: string;
    include_detailed_breakdown?: boolean;
    include_recommendations?: boolean;
  }) => {
    let endpoint = '/interviews/analytics/performance';
    if (params) {
      const queryParams = new URLSearchParams();
      if (params.start_date) queryParams.append('start_date', params.start_date);
      if (params.end_date) queryParams.append('end_date', params.end_date);
      if (params.include_detailed_breakdown !== undefined) {
        queryParams.append('include_detailed_breakdown', params.include_detailed_breakdown.toString());
      }
      if (params.include_recommendations !== undefined) {
        queryParams.append('include_recommendations', params.include_recommendations.toString());
      }
      if (queryParams.toString()) endpoint += `?${queryParams}`;
    }
    return ApiClient.authenticatedRequest(endpoint);
  },

  getInterviewHistoryAnalytics: (params?: {
    include_answers?: boolean;
    include_metadata?: boolean;
    date_range_start?: string;
    date_range_end?: string;
    sort_by?: string;
    sort_order?: string;
  }) => {
    let endpoint = '/interviews/analytics/history';
    if (params) {
      const queryParams = new URLSearchParams();
      if (params.include_answers !== undefined) {
        queryParams.append('include_answers', params.include_answers.toString());
      }
      if (params.include_metadata !== undefined) {
        queryParams.append('include_metadata', params.include_metadata.toString());
      }
      if (params.date_range_start) queryParams.append('date_range_start', params.date_range_start);
      if (params.date_range_end) queryParams.append('date_range_end', params.date_range_end);
      if (params.sort_by) queryParams.append('sort_by', params.sort_by);
      if (params.sort_order) queryParams.append('sort_order', params.sort_order);
      if (queryParams.toString()) endpoint += `?${queryParams}`;
    }
    return ApiClient.authenticatedRequest(endpoint);
  },

  // Real-time Interview Features
  startRealtimeInterview: (interviewId: string) =>
    ApiClient.authenticatedRequest(`/interviews/${interviewId}/realtime/start`, {
      method: 'POST',
    }),

  submitRealtimeResponse: (interviewId: string, data: {
    question_id: string;
    response_text: string;
    metadata?: Record<string, any>;
    time_spent?: number;
    auto_progress?: boolean;
  }) =>
    ApiClient.authenticatedRequest(`/interviews/${interviewId}/realtime/respond`, {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  interviewHeartbeat: (interviewId: string, data?: Record<string, any>) =>
    ApiClient.authenticatedRequest(`/interviews/${interviewId}/realtime/heartbeat`, {
      method: 'POST',
      body: JSON.stringify(data || {}),
    }),

  getRealtimeStatus: (interviewId: string, includeSuggestions?: boolean) => {
    let endpoint = `/interviews/${interviewId}/realtime/status`;
    if (includeSuggestions !== undefined) {
      endpoint += `?include_suggestions=${includeSuggestions}`;
    }
    return ApiClient.authenticatedRequest(endpoint);
  },

  // Server-Sent Events endpoints (these return EventSource objects, not API calls)
  createProgressStream: (interviewId: string) => {
    const token = localStorage.getItem('access_token');
    return new EventSource(`${ApiClient['baseURL']}/interviews/${interviewId}/stream/progress`, {
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    } as any);
  },

  createAIFeedbackStream: (interviewId: string) => {
    const token = localStorage.getItem('access_token');
    return new EventSource(`${ApiClient['baseURL']}/interviews/${interviewId}/stream/ai-feedback`, {
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    } as any);
  },

  // User Language Preference
  getUserLanguagePreference: () => {
    // Check if we're in company context by checking current URL
    const isCompanyContext = typeof window !== 'undefined' && window.location.pathname.startsWith('/company/');
    const endpoint = isCompanyContext ? '/company/me/language' : '/user/me/language';
    return ApiClient.authenticatedRequest(endpoint);
  },

  updateUserLanguagePreference: (languageCode: string) => {
    // Check if we're in company context by checking current URL
    const isCompanyContext = typeof window !== 'undefined' && window.location.pathname.startsWith('/company/');
    const endpoint = isCompanyContext ? '/company/me/language' : '/user/me/language';
    return ApiClient.authenticatedRequest(endpoint, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ language_code: languageCode }),
    });
  },

  // Company Roles API
  listCompanyRoles: (companyId: string, activeOnly: boolean = false) =>
    ApiClient.authenticatedRequest(`/companies/${companyId}/roles?active_only=${activeOnly}`),

  getCompanyRole: (companyId: string, roleId: string) =>
    ApiClient.authenticatedRequest(`/companies/${companyId}/roles/${roleId}`),

  createCompanyRole: (companyId: string, data: { name: string; description?: string }) =>
    ApiClient.authenticatedRequest(`/companies/${companyId}/roles`, {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  updateCompanyRole: (companyId: string, roleId: string, data: { name: string; description?: string }) =>
    ApiClient.authenticatedRequest(`/companies/${companyId}/roles/${roleId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),

  deleteCompanyRole: (companyId: string, roleId: string) =>
    ApiClient.authenticatedRequest(`/companies/${companyId}/roles/${roleId}`, {
      method: 'DELETE',
    }),

  // ==================== COMPANY-SCOPED ADMIN API ====================
  // These endpoints use company slug in the URL for proper context validation

  // Admin Position Management (company-scoped)
  adminListPositions: (companySlug: string, params?: {
    search_term?: string;
    is_active?: boolean;
    page?: number;
    page_size?: number;
  }) => {
    let endpoint = `/${companySlug}/admin/positions`;
    if (params) {
      const queryParams = new URLSearchParams();
      if (params.search_term) queryParams.append('search_term', params.search_term);
      if (params.is_active !== undefined) queryParams.append('is_active', params.is_active.toString());
      if (params.page) queryParams.append('page', params.page.toString());
      if (params.page_size) queryParams.append('page_size', params.page_size.toString());
      const queryString = queryParams.toString();
      if (queryString) endpoint += `?${queryString}`;
    }
    return ApiClient.authenticatedRequest(endpoint);
  },

  adminGetPosition: (companySlug: string, positionId: string) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/positions/${positionId}`),

  adminCreatePosition: (companySlug: string, data: any) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/positions`, {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  adminUpdatePosition: (companySlug: string, positionId: string, data: any) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/positions/${positionId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),

  adminDeletePosition: (companySlug: string, positionId: string) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/positions/${positionId}`, {
      method: 'DELETE',
    }),

  adminPublishPosition: (companySlug: string, positionId: string) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/positions/${positionId}/publish`, {
      method: 'POST',
    }),

  adminHoldPosition: (companySlug: string, positionId: string) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/positions/${positionId}/hold`, {
      method: 'POST',
    }),

  adminResumePosition: (companySlug: string, positionId: string) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/positions/${positionId}/resume`, {
      method: 'POST',
    }),

  adminClosePosition: (companySlug: string, positionId: string, reason?: string) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/positions/${positionId}/close`, {
      method: 'POST',
      body: JSON.stringify({ reason: reason || '' }),
    }),

  adminArchivePosition: (companySlug: string, positionId: string) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/positions/${positionId}/archive`, {
      method: 'POST',
    }),

  adminClonePosition: (companySlug: string, positionId: string) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/positions/${positionId}/clone`, {
      method: 'POST',
    }),

  // Admin Candidate Management (company-scoped)
  adminListCandidates: (companySlug: string) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/candidates`),

  adminGetCandidate: (companySlug: string, companyCandidateId: string) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/candidates/${companyCandidateId}`),

  adminCreateCandidate: (companySlug: string, data: {
    candidate_id: string;
    job_position_id?: string;
    workflow_id?: string;
  }) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/candidates`, {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  adminUpdateCandidate: (companySlug: string, companyCandidateId: string, data: any) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/candidates/${companyCandidateId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),

  adminConfirmCandidate: (companySlug: string, companyCandidateId: string) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/candidates/${companyCandidateId}/confirm`, {
      method: 'POST',
    }),

  adminRejectCandidate: (companySlug: string, companyCandidateId: string) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/candidates/${companyCandidateId}/reject`, {
      method: 'POST',
    }),

  adminArchiveCandidate: (companySlug: string, companyCandidateId: string) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/candidates/${companyCandidateId}/archive`, {
      method: 'POST',
    }),

  adminAssignWorkflow: (companySlug: string, companyCandidateId: string, data: {
    workflow_id: string;
    start_stage_id?: string;
  }) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/candidates/${companyCandidateId}/assign-workflow`, {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  adminChangeCandidateStage: (companySlug: string, companyCandidateId: string, data: {
    stage_id: string;
    notes?: string;
  }) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/candidates/${companyCandidateId}/change-stage`, {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  adminGenerateCandidateReport: (companySlug: string, companyCandidateId: string, data?: {
    include_comments?: boolean;
    include_interviews?: boolean;
    include_reviews?: boolean;
  }) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/candidates/${companyCandidateId}/report`, {
      method: 'POST',
      body: JSON.stringify(data || {
        include_comments: true,
        include_interviews: true,
        include_reviews: true,
      }),
    }),

  // Admin Application Management (company-scoped)
  adminAssignCandidateToPosition: (companySlug: string, data: {
    candidate_id: string;
    job_position_id: string;
  }) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/applications`, {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  adminCheckCanProcessApplication: (companySlug: string, applicationId: string) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/applications/${applicationId}/can-process`),

  // Admin Interview Management (company-scoped)
  adminListInterviews: (companySlug: string, params?: {
    candidate_id?: string;
    job_position_id?: string;
    status?: string;
    from_date?: string;
    to_date?: string;
    limit?: number;
    offset?: number;
  }) => {
    let endpoint = `/${companySlug}/admin/interviews`;
    if (params) {
      const queryParams = new URLSearchParams();
      if (params.candidate_id) queryParams.append('candidate_id', params.candidate_id);
      if (params.job_position_id) queryParams.append('job_position_id', params.job_position_id);
      if (params.status) queryParams.append('status', params.status);
      if (params.from_date) queryParams.append('from_date', params.from_date);
      if (params.to_date) queryParams.append('to_date', params.to_date);
      if (params.limit) queryParams.append('limit', params.limit.toString());
      if (params.offset) queryParams.append('offset', params.offset.toString());
      const queryString = queryParams.toString();
      if (queryString) endpoint += `?${queryString}`;
    }
    return ApiClient.authenticatedRequest(endpoint);
  },

  adminGetInterviewStats: (companySlug: string) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/interviews/statistics`),

  adminGetInterview: (companySlug: string, interviewId: string) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/interviews/${interviewId}`),

  adminGetInterviewView: (companySlug: string, interviewId: string) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/interviews/${interviewId}/view`),

  adminCreateInterview: (companySlug: string, data: any) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/interviews`, {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  adminUpdateInterview: (companySlug: string, interviewId: string, data: any) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/interviews/${interviewId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),

  adminStartInterview: (companySlug: string, interviewId: string, startedBy?: string) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/interviews/${interviewId}/start`, {
      method: 'POST',
      body: JSON.stringify({ started_by: startedBy }),
    }),

  adminFinishInterview: (companySlug: string, interviewId: string, finishedBy?: string) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/interviews/${interviewId}/finish`, {
      method: 'POST',
      body: JSON.stringify({ finished_by: finishedBy }),
    }),

  // Admin Interview Template Management (company-scoped)
  adminListInterviewTemplates: (companySlug: string, params?: {
    search_term?: string;
    type?: string;
    status?: string;
    page?: number;
    page_size?: number;
  }) => {
    let endpoint = `/${companySlug}/admin/interview-templates`;
    if (params) {
      const queryParams = new URLSearchParams();
      if (params.search_term) queryParams.append('search_term', params.search_term);
      if (params.type) queryParams.append('type', params.type);
      if (params.status) queryParams.append('status', params.status);
      if (params.page) queryParams.append('page', params.page.toString());
      if (params.page_size) queryParams.append('page_size', params.page_size.toString());
      const queryString = queryParams.toString();
      if (queryString) endpoint += `?${queryString}`;
    }
    return ApiClient.authenticatedRequest(endpoint);
  },

  adminGetInterviewTemplate: (companySlug: string, templateId: string) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/interview-templates/${templateId}`),

  adminCreateInterviewTemplate: (companySlug: string, data: any) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/interview-templates`, {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  adminUpdateInterviewTemplate: (companySlug: string, templateId: string, data: any) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/interview-templates/${templateId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),

  adminDeleteInterviewTemplate: (companySlug: string, templateId: string, params?: {
    delete_reason?: string;
    force_delete?: boolean;
  }) => {
    let endpoint = `/${companySlug}/admin/interview-templates/${templateId}`;
    if (params) {
      const queryParams = new URLSearchParams();
      if (params.delete_reason) queryParams.append('delete_reason', params.delete_reason);
      if (params.force_delete !== undefined) queryParams.append('force_delete', params.force_delete.toString());
      const queryString = queryParams.toString();
      if (queryString) endpoint += `?${queryString}`;
    }
    return ApiClient.authenticatedRequest(endpoint, { method: 'DELETE' });
  },

  adminEnableInterviewTemplate: (companySlug: string, templateId: string, enableReason?: string) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/interview-templates/${templateId}/enable`, {
      method: 'POST',
      body: JSON.stringify({ enable_reason: enableReason }),
    }),

  adminDisableInterviewTemplate: (companySlug: string, templateId: string, params?: {
    disable_reason?: string;
    force_disable?: boolean;
  }) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/interview-templates/${templateId}/disable`, {
      method: 'POST',
      body: JSON.stringify(params || {}),
    }),

  // Admin Workflow Management (company-scoped)
  adminListWorkflows: (companySlug: string, params?: {
    is_active?: boolean;
    search_term?: string;
    limit?: number;
    offset?: number;
  }) => {
    let endpoint = `/${companySlug}/admin/workflows`;
    if (params) {
      const queryParams = new URLSearchParams();
      if (params.is_active !== undefined) queryParams.append('is_active', params.is_active.toString());
      if (params.search_term) queryParams.append('search_term', params.search_term);
      if (params.limit) queryParams.append('limit', params.limit.toString());
      if (params.offset) queryParams.append('offset', params.offset.toString());
      const queryString = queryParams.toString();
      if (queryString) endpoint += `?${queryString}`;
    }
    return ApiClient.authenticatedRequest(endpoint);
  },

  adminGetWorkflow: (companySlug: string, workflowId: string) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/workflows/${workflowId}`),

  adminCreateWorkflow: (companySlug: string, data: {
    name: string;
    description?: string;
    stages?: Array<{ name: string; description?: string; order: number }>;
  }) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/workflows`, {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  adminUpdateWorkflow: (companySlug: string, workflowId: string, data: {
    name?: string;
    description?: string;
  }) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/workflows/${workflowId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),

  adminActivateWorkflow: (companySlug: string, workflowId: string) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/workflows/${workflowId}/activate`, {
      method: 'POST',
    }),

  adminDeactivateWorkflow: (companySlug: string, workflowId: string) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/workflows/${workflowId}/deactivate`, {
      method: 'POST',
    }),

  adminArchiveWorkflow: (companySlug: string, workflowId: string) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/workflows/${workflowId}/archive`, {
      method: 'POST',
    }),

  adminSetDefaultWorkflow: (companySlug: string, workflowId: string) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/workflows/${workflowId}/set-default`, {
      method: 'POST',
    }),

  adminDeleteWorkflow: (companySlug: string, workflowId: string) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/workflows/${workflowId}`, {
      method: 'DELETE',
    }),

  // Admin Workflow Stage Management (company-scoped)
  adminListWorkflowStages: (companySlug: string, workflowId: string) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/workflows/${workflowId}/stages`),

  adminGetWorkflowStage: (companySlug: string, workflowId: string, stageId: string) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/workflows/${workflowId}/stages/${stageId}`),

  adminCreateWorkflowStage: (companySlug: string, workflowId: string, data: {
    name: string;
    description?: string;
    order?: number;
  }) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/workflows/${workflowId}/stages`, {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  adminUpdateWorkflowStage: (companySlug: string, workflowId: string, stageId: string, data: {
    name?: string;
    description?: string;
  }) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/workflows/${workflowId}/stages/${stageId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),

  adminDeleteWorkflowStage: (companySlug: string, workflowId: string, stageId: string) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/workflows/${workflowId}/stages/${stageId}`, {
      method: 'DELETE',
    }),

  adminReorderWorkflowStages: (companySlug: string, workflowId: string, data: {
    stage_ids: string[];
  }) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/workflows/${workflowId}/stages/reorder`, {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  // Admin Candidate Comments (company-scoped)
  adminListCandidateComments: (companySlug: string, companyCandidateId: string, params?: {
    limit?: number;
    offset?: number;
  }) => {
    let endpoint = `/${companySlug}/admin/candidates/${companyCandidateId}/comments`;
    if (params) {
      const queryParams = new URLSearchParams();
      if (params.limit) queryParams.append('limit', params.limit.toString());
      if (params.offset) queryParams.append('offset', params.offset.toString());
      const queryString = queryParams.toString();
      if (queryString) endpoint += `?${queryString}`;
    }
    return ApiClient.authenticatedRequest(endpoint);
  },

  adminCreateCandidateComment: (companySlug: string, companyCandidateId: string, data: {
    content: string;
    is_private?: boolean;
  }) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/candidates/${companyCandidateId}/comments`, {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  adminGetCandidateComment: (companySlug: string, companyCandidateId: string, commentId: string) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/candidates/${companyCandidateId}/comments/${commentId}`),

  adminUpdateCandidateComment: (companySlug: string, companyCandidateId: string, commentId: string, data: {
    content?: string;
    is_private?: boolean;
  }) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/candidates/${companyCandidateId}/comments/${commentId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),

  adminDeleteCandidateComment: (companySlug: string, companyCandidateId: string, commentId: string) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/candidates/${companyCandidateId}/comments/${commentId}`, {
      method: 'DELETE',
    }),

  // Admin Candidate Reviews (company-scoped)
  adminListCandidateReviews: (companySlug: string, companyCandidateId: string, params?: {
    limit?: number;
    offset?: number;
  }) => {
    let endpoint = `/${companySlug}/admin/candidates/${companyCandidateId}/reviews`;
    if (params) {
      const queryParams = new URLSearchParams();
      if (params.limit) queryParams.append('limit', params.limit.toString());
      if (params.offset) queryParams.append('offset', params.offset.toString());
      const queryString = queryParams.toString();
      if (queryString) endpoint += `?${queryString}`;
    }
    return ApiClient.authenticatedRequest(endpoint);
  },

  adminCreateCandidateReview: (companySlug: string, companyCandidateId: string, data: {
    rating: number;
    feedback: string;
    criteria_scores?: Record<string, number>;
  }) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/candidates/${companyCandidateId}/reviews`, {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  adminGetCandidateReview: (companySlug: string, companyCandidateId: string, reviewId: string) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/candidates/${companyCandidateId}/reviews/${reviewId}`),

  adminUpdateCandidateReview: (companySlug: string, companyCandidateId: string, reviewId: string, data: {
    rating?: number;
    feedback?: string;
    criteria_scores?: Record<string, number>;
  }) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/candidates/${companyCandidateId}/reviews/${reviewId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),

  adminDeleteCandidateReview: (companySlug: string, companyCandidateId: string, reviewId: string) =>
    ApiClient.authenticatedRequest(`/${companySlug}/admin/candidates/${companyCandidateId}/reviews/${reviewId}`, {
      method: 'DELETE',
    }),

  // Generic authenticated request
  authenticatedRequest: <T = unknown>(endpoint: string, options?: RequestInit) =>
    ApiClient.authenticatedRequest<T>(endpoint, options),
};