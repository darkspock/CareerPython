// Company Interview Template API service
import { ApiClient } from '../lib/api';
import { InterviewTemplateType } from '../types/interview';

export type InterviewTemplateQuestion = {
  id: string;
  interview_template_section_id: string;
  name: string;
  description: string;
  code: string;
  sort_order: number;
  data_type: string;
  scope: string;
  status: string;
  allow_ai_followup?: boolean;
  legal_notice?: string;
  scoring_values?: Array<{ label: string; scoring: number }>;
};

export type InterviewTemplateSection = {
  id: string;
  interview_template_id: string;
  name: string;
  intro?: string;
  prompt?: string;
  goal?: string;
  section?: string;
  sort_order: number;
  status: string;
  allow_ai_questions?: boolean;
  allow_ai_override_questions?: boolean;
  legal_notice?: string;
  questions?: InterviewTemplateQuestion[];
};

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
  sections?: InterviewTemplateSection[];
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

  /**
   * Get questions for a section
   */
  async getQuestionsBySection(sectionId: string): Promise<InterviewTemplateQuestion[]> {
    return ApiClient.authenticatedRequest<InterviewTemplateQuestion[]>(
      `/api/company/interview-templates/sections/${sectionId}/questions`
    );
  },

  /**
   * List screening templates (SCREENING type only)
   */
  async listScreeningTemplates(): Promise<InterviewTemplate[]> {
    return this.listTemplates({ type: 'SCREENING', status: 'ENABLED' });
  },

  /**
   * Get template with full details including sections and questions
   */
  async getTemplateWithQuestions(templateId: string): Promise<InterviewTemplate> {
    const template = await this.getTemplate(templateId);

    // If template has sections, load questions for each section
    if (template.sections && template.sections.length > 0) {
      const sectionsWithQuestions = await Promise.all(
        template.sections.map(async (section) => {
          try {
            const questions = await this.getQuestionsBySection(section.id);
            return { ...section, questions };
          } catch (error) {
            console.warn(`Failed to load questions for section ${section.id}:`, error);
            return { ...section, questions: [] };
          }
        })
      );
      return { ...template, sections: sectionsWithQuestions };
    }

    return template;
  },

  /**
   * Create a section for a template
   */
  async createSection(data: {
    interview_template_id: string;
    name: string;
    intro?: string;
    prompt?: string;
    goal?: string;
    section?: string;
    sort_order: number;
    allow_ai_questions?: boolean;
    allow_ai_override_questions?: boolean;
    legal_notice?: string;
  }): Promise<InterviewTemplateSection> {
    return ApiClient.authenticatedRequest<InterviewTemplateSection>(
      '/api/company/interview-templates/sections',
      {
        method: 'POST',
        body: JSON.stringify(data),
      }
    );
  },

  /**
   * Create a question in a section
   */
  async createQuestion(data: {
    interview_template_section_id: string;
    name: string;
    description?: string;
    code: string;
    sort_order: number;
    data_type: string;
    scope?: string;
    allow_ai_followup?: boolean;
    legal_notice?: string;
    scoring_values?: Array<{ label: string; scoring: number }>;
  }): Promise<InterviewTemplateQuestion> {
    return ApiClient.authenticatedRequest<InterviewTemplateQuestion>(
      '/api/company/interview-templates/questions',
      {
        method: 'POST',
        body: JSON.stringify(data),
      }
    );
  },

  /**
   * Update a question
   */
  async updateQuestion(questionId: string, data: Partial<{
    name: string;
    description: string;
    code: string;
    sort_order: number;
    data_type: string;
    scope: string;
    allow_ai_followup: boolean;
    legal_notice: string;
    scoring_values: Array<{ label: string; scoring: number }>;
  }>): Promise<InterviewTemplateQuestion> {
    return ApiClient.authenticatedRequest<InterviewTemplateQuestion>(
      `/api/company/interview-templates/questions/${questionId}`,
      {
        method: 'PUT',
        body: JSON.stringify(data),
      }
    );
  },

  /**
   * Delete a question
   */
  async deleteQuestion(questionId: string): Promise<void> {
    await ApiClient.authenticatedRequest(
      `/api/company/interview-templates/questions/${questionId}`,
      {
        method: 'DELETE',
      }
    );
  },

  /**
   * Create a complete template with sections and questions in one flow
   * This handles the multi-step API calls internally
   */
  async createTemplateWithQuestions(data: {
    name: string;
    intro?: string;
    type: string;
    status?: string;
    sections: Array<{
      name: string;
      intro?: string;
      sort_order: number;
      questions: Array<{
        name: string;
        description?: string;
        code: string;
        sort_order: number;
        data_type: string;
        scope?: string;
        scoring_values?: Array<{ label: string; scoring: number }> | null;
      }>;
    }>;
  }): Promise<InterviewTemplate> {
    // Step 1: Create the template
    const template = await this.createTemplate({
      name: data.name,
      intro: data.intro,
      type: data.type as InterviewTemplateType,
      status: (data.status || 'ENABLED') as 'ENABLED' | 'DRAFT' | 'DISABLED',
    });

    // Step 2: Create sections with questions
    for (const sectionData of data.sections) {
      const section = await this.createSection({
        interview_template_id: template.id,
        name: sectionData.name,
        intro: sectionData.intro,
        sort_order: sectionData.sort_order,
      });

      // Step 3: Create questions for each section
      for (const questionData of sectionData.questions) {
        await this.createQuestion({
          interview_template_section_id: section.id,
          name: questionData.name,
          description: questionData.description || '',
          code: questionData.code,
          sort_order: questionData.sort_order,
          data_type: questionData.data_type,
          scope: questionData.scope || 'global',
          scoring_values: questionData.scoring_values || undefined,
        });
      }
    }

    // Return the full template with questions
    return this.getTemplateWithQuestions(template.id);
  },
};

