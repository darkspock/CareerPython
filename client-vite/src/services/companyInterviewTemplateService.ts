// Company Interview Template API service
import { ApiClient } from '../lib/api';
import { InterviewTemplateType } from '../types/interview';

export type InterviewTemplate = {
  id: string;
  name: string;
  intro?: string;
  prompt?: string;
  goal?: string;
  status: 'ENABLED' | 'DRAFT' | 'DISABLED';
  type: InterviewTemplateType;
  job_category?: string;
  section?: string;
  tags?: string[];
  company_id?: string;
};

export type TemplateFilters = {
  search_term?: string;
  type?: string;
  status?: string;
  job_category?: string;
  section?: string;
  page?: number;
  page_size?: number;
};

export const companyInterviewTemplateService = {
  /**
   * List all interview templates for the company
   */
  async listTemplates(filters?: TemplateFilters): Promise<InterviewTemplate[]> {
    const queryParams = new URLSearchParams();
    if (filters?.search_term) queryParams.append('search_term', filters.search_term);
    if (filters?.type) queryParams.append('type', filters.type);
    if (filters?.status) queryParams.append('status', filters.status);
    if (filters?.job_category) queryParams.append('job_category', filters.job_category);
    if (filters?.section) queryParams.append('section', filters.section);
    if (filters?.page) queryParams.append('page', filters.page.toString());
    if (filters?.page_size) queryParams.append('page_size', filters.page_size.toString());

    const endpoint = `/api/company/interview-templates${queryParams.toString() ? `?${queryParams}` : ''}`;
    try {
      const response = await ApiClient.authenticatedRequest<InterviewTemplate[]>(endpoint);
      console.log('[companyInterviewTemplateService] Raw response:', response);
      
      // Handle different response formats
      if (Array.isArray(response)) {
        return response;
      } else if (response && typeof response === 'object' && 'items' in response) {
        // Handle paginated response
        return (response as any).items || [];
      } else if (response && typeof response === 'object' && 'templates' in response) {
        // Handle wrapped response
        return (response as any).templates || [];
      }
      
      console.warn('[companyInterviewTemplateService] Unexpected response format:', response);
      return [];
    } catch (error) {
      console.error('[companyInterviewTemplateService] Error fetching templates:', error);
      throw error;
    }
  },

  /**
   * Get a single interview template by ID
   */
  async getTemplate(templateId: string): Promise<InterviewTemplate> {
    return ApiClient.authenticatedRequest<InterviewTemplate>(`/api/company/interview-templates/${templateId}`);
  },

  /**
   * Create a new interview template
   */
  async createTemplate(data: Partial<InterviewTemplate>): Promise<InterviewTemplate> {
    return ApiClient.authenticatedRequest<InterviewTemplate>('/api/company/interview-templates', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  /**
   * Update an interview template
   */
  async updateTemplate(templateId: string, data: Partial<InterviewTemplate>): Promise<InterviewTemplate> {
    return ApiClient.authenticatedRequest<InterviewTemplate>(`/api/company/interview-templates/${templateId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },

  /**
   * Delete an interview template
   */
  async deleteTemplate(templateId: string, deleteReason?: string, forceDelete: boolean = false): Promise<void> {
    const queryParams = new URLSearchParams();
    if (deleteReason) queryParams.append('delete_reason', deleteReason);
    if (forceDelete) queryParams.append('force_delete', 'true');

    await ApiClient.authenticatedRequest(`/api/company/interview-templates/${templateId}?${queryParams.toString()}`, {
      method: 'DELETE',
    });
  },

  /**
   * Enable an interview template
   */
  async enableTemplate(templateId: string, enableReason?: string): Promise<void> {
    const body: any = {};
    if (enableReason) body.enable_reason = enableReason;

    await ApiClient.authenticatedRequest(`/api/company/interview-templates/${templateId}/enable`, {
      method: 'POST',
      body: JSON.stringify(body),
    });
  },

  /**
   * Disable an interview template
   */
  async disableTemplate(templateId: string, disableReason?: string, forceDisable: boolean = false): Promise<void> {
    const body: any = {};
    if (disableReason) body.disable_reason = disableReason;
    if (forceDisable) body.force_disable = forceDisable;

    await ApiClient.authenticatedRequest(`/api/company/interview-templates/${templateId}/disable`, {
      method: 'POST',
      body: JSON.stringify(body),
    });
  },
};

