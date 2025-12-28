/**
 * Email Template Service
 * Phase 7: Service for email template API calls
 */

import { api } from '../lib/api';
import type {
  EmailTemplate,
  CreateEmailTemplateRequest,
  UpdateEmailTemplateRequest,
  EmailTemplateFilters,
  TriggerEvent
} from '../types/emailTemplate';

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
 * Get the base path for email template endpoints (company-scoped)
 */
function getBasePath(): string {
  return `/${getCompanySlug()}/admin/email-templates`;
}

export class EmailTemplateService {
  /**
   * Create a new email template
   */
  static async createTemplate(data: CreateEmailTemplateRequest): Promise<EmailTemplate> {
    return await api.authenticatedRequest<EmailTemplate>(getBasePath(), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
  }

  /**
   * Get an email template by ID
   */
  static async getTemplateById(templateId: string): Promise<EmailTemplate> {
    return await api.authenticatedRequest<EmailTemplate>(`${getBasePath()}/${templateId}`);
  }

  /**
   * Update an existing email template
   */
  static async updateTemplate(
    templateId: string,
    data: UpdateEmailTemplateRequest
  ): Promise<{ message: string; template_id: string }> {
    return await api.authenticatedRequest<{ message: string; template_id: string }>(`${getBasePath()}/${templateId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
  }

  /**
   * Delete an email template
   */
  static async deleteTemplate(templateId: string): Promise<{ message: string }> {
    return await api.authenticatedRequest<{ message: string }>(`${getBasePath()}/${templateId}`, {
      method: 'DELETE'
    });
  }

  /**
   * Activate an email template
   */
  static async activateTemplate(templateId: string): Promise<{ message: string }> {
    return await api.authenticatedRequest<{ message: string }>(`${getBasePath()}/${templateId}/activate`, {
      method: 'POST'
    });
  }

  /**
   * Deactivate an email template
   */
  static async deactivateTemplate(templateId: string): Promise<{ message: string }> {
    return await api.authenticatedRequest<{ message: string }>(`${getBasePath()}/${templateId}/deactivate`, {
      method: 'POST'
    });
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

    return await api.authenticatedRequest<EmailTemplate[]>(`${getBasePath()}/workflow/${workflowId}?${params.toString()}`);
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

    return await api.authenticatedRequest<EmailTemplate[]>(`${getBasePath()}/stage/${stageId}?${params.toString()}`);
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

    return await api.authenticatedRequest<EmailTemplate[]>(
      `${getBasePath()}/trigger/${workflowId}/${triggerEvent}?${params.toString()}`
    );
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

  /**
   * Send bulk emails to multiple recipients
   */
  static async sendBulkEmail(
    templateId: string,
    recipients: Array<{
      email: string;
      name: string;
      template_data: Record<string, string>;
    }>
  ): Promise<{ message: string; total: number; queued: number }> {
    return await api.authenticatedRequest<{ message: string; total: number; queued: number }>(
      `${getBasePath()}/send-bulk`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ template_id: templateId, recipients })
      }
    );
  }
}
