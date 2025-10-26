/**
 * Email Template Service
 * Phase 7: Service for email template API calls
 */

import api from '@/lib/api';
import type {
  EmailTemplate,
  CreateEmailTemplateRequest,
  UpdateEmailTemplateRequest,
  EmailTemplateFilters,
  TriggerEvent
} from '@/types/emailTemplate';

export class EmailTemplateService {
  private static readonly BASE_PATH = '/api/company/email-templates';

  /**
   * Create a new email template
   */
  static async createTemplate(data: CreateEmailTemplateRequest): Promise<EmailTemplate> {
    const response = await api.post(this.BASE_PATH, data);
    return await response.json();
  }

  /**
   * Get an email template by ID
   */
  static async getTemplateById(templateId: string): Promise<EmailTemplate> {
    const response = await api.get(`${this.BASE_PATH}/${templateId}`);
    return await response.json();
  }

  /**
   * Update an existing email template
   */
  static async updateTemplate(
    templateId: string,
    data: UpdateEmailTemplateRequest
  ): Promise<{ message: string; template_id: string }> {
    const response = await api.put(`${this.BASE_PATH}/${templateId}`, data);
    return await response.json();
  }

  /**
   * Delete an email template
   */
  static async deleteTemplate(templateId: string): Promise<{ message: string }> {
    const response = await api.delete(`${this.BASE_PATH}/${templateId}`);
    return await response.json();
  }

  /**
   * Activate an email template
   */
  static async activateTemplate(templateId: string): Promise<{ message: string }> {
    const response = await api.post(`${this.BASE_PATH}/${templateId}/activate`);
    return await response.json();
  }

  /**
   * Deactivate an email template
   */
  static async deactivateTemplate(templateId: string): Promise<{ message: string }> {
    const response = await api.post(`${this.BASE_PATH}/${templateId}/deactivate`);
    return await response.json();
  }

  /**
   * List templates by workflow
   */
  static async listTemplatesByWorkflow(
    workflowId: string,
    activeOnly: boolean = false
  ): Promise<EmailTemplate[]> {
    const params = new URLSearchParams();
    if (activeOnly) params.append('active_only', 'true');

    const response = await api.get(`${this.BASE_PATH}/workflow/${workflowId}?${params.toString()}`);
    return await response.json();
  }

  /**
   * List templates by stage
   */
  static async listTemplatesByStage(
    stageId: string,
    activeOnly: boolean = false
  ): Promise<EmailTemplate[]> {
    const params = new URLSearchParams();
    if (activeOnly) params.append('active_only', 'true');

    const response = await api.get(`${this.BASE_PATH}/stage/${stageId}?${params.toString()}`);
    return await response.json();
  }

  /**
   * Get templates by trigger event
   */
  static async getTemplatesByTrigger(
    workflowId: string,
    triggerEvent: TriggerEvent,
    stageId?: string | null,
    activeOnly: boolean = true
  ): Promise<EmailTemplate[]> {
    const params = new URLSearchParams();
    if (stageId) params.append('stage_id', stageId);
    if (activeOnly) params.append('active_only', 'true');

    const response = await api.get(
      `${this.BASE_PATH}/trigger/${workflowId}/${triggerEvent}?${params.toString()}`
    );
    return await response.json();
  }

  /**
   * Get all templates with optional filters
   */
  static async listTemplates(filters?: EmailTemplateFilters): Promise<EmailTemplate[]> {
    if (filters?.workflow_id) {
      return this.listTemplatesByWorkflow(filters.workflow_id, filters.active_only);
    }

    if (filters?.stage_id) {
      return this.listTemplatesByStage(filters.stage_id, filters.active_only);
    }

    if (filters?.workflow_id && filters?.trigger_event) {
      return this.getTemplatesByTrigger(
        filters.workflow_id,
        filters.trigger_event,
        filters.stage_id,
        filters.active_only
      );
    }

    // Default: return empty array or throw error
    throw new Error('Must provide at least workflow_id or stage_id filter');
  }
}
