/**
 * @deprecated This service is deprecated. Use EntityCustomizationService from './entityCustomizationService' instead.
 * This service will be removed in a future version.
 * 
 * Migration guide:
 * - Replace CustomFieldService.listCustomFieldsByWorkflow(workflowId) 
 *   with EntityCustomizationService.listFieldsByEntity('Workflow', workflowId)
 * - Replace CustomFieldService.createCustomField(request) 
 *   with EntityCustomizationService.updateCustomization(id, { fields: [field] })
 * - And so on...
 */
// Custom Field API service
import { api } from '../lib/api';
import type {
  CustomField,
  FieldConfiguration,
  CreateCustomFieldRequest,
  UpdateCustomFieldRequest,
  ReorderCustomFieldRequest,
  ConfigureStageFieldRequest,
  UpdateFieldVisibilityRequest
} from '../types/workflow';

/**
 * @deprecated Use EntityCustomizationService instead.
 */
export class CustomFieldService {
  private static readonly BASE_PATH = '/api/custom-fields';

  /**
   * Create a new custom field
   */
  static async createCustomField(request: CreateCustomFieldRequest): Promise<CustomField> {
    try {
      const response = await api.authenticatedRequest<CustomField>(this.BASE_PATH, {
        method: 'POST',
        body: JSON.stringify(request)
      });
      return response;
    } catch (error) {
      console.error('Error creating custom field:', error);
      throw error;
    }
  }

  /**
   * Get custom field by ID
   */
  static async getCustomFieldById(fieldId: string): Promise<CustomField> {
    try {
      const response = await api.authenticatedRequest<CustomField>(`${this.BASE_PATH}/${fieldId}`);
      return response;
    } catch (error) {
      console.error('Error fetching custom field:', error);
      throw error;
    }
  }

  /**
   * List custom fields for a workflow
   */
  static async listCustomFieldsByWorkflow(workflowId: string): Promise<CustomField[]> {
    try {
      const response = await api.authenticatedRequest<{ fields?: CustomField[] } | CustomField[]>(`${this.BASE_PATH}/workflow/${workflowId}`);
      return Array.isArray(response) ? response : (response.fields || []);
    } catch (error) {
      console.error('Error fetching custom fields:', error);
      throw error;
    }
  }

  /**
   * Update custom field
   */
  static async updateCustomField(
    fieldId: string,
    request: UpdateCustomFieldRequest
  ): Promise<CustomField> {
    try {
      const response = await api.authenticatedRequest<CustomField>(`${this.BASE_PATH}/${fieldId}`, {
        method: 'PUT',
        body: JSON.stringify(request)
      });
      return response;
    } catch (error) {
      console.error('Error updating custom field:', error);
      throw error;
    }
  }

  /**
   * Reorder custom field
   */
  static async reorderCustomField(
    fieldId: string,
    request: ReorderCustomFieldRequest
  ): Promise<CustomField> {
    try {
      const response = await api.authenticatedRequest<CustomField>(`${this.BASE_PATH}/${fieldId}/reorder`, {
        method: 'PUT',
        body: JSON.stringify(request)
      });
      return response;
    } catch (error) {
      console.error('Error reordering custom field:', error);
      throw error;
    }
  }

  /**
   * Delete custom field
   */
  static async deleteCustomField(fieldId: string): Promise<void> {
    try {
      await api.authenticatedRequest(`${this.BASE_PATH}/${fieldId}`, {
        method: 'DELETE'
      });
    } catch (error) {
      console.error('Error deleting custom field:', error);
      throw error;
    }
  }

  /**
   * Configure stage field (set visibility for a specific stage)
   */
  static async configureStageField(
    request: ConfigureStageFieldRequest
  ): Promise<FieldConfiguration> {
    try {
      const response = await api.authenticatedRequest<FieldConfiguration>(`${this.BASE_PATH}/configurations`, {
        method: 'POST',
        body: JSON.stringify(request)
      });
      return response;
    } catch (error) {
      console.error('Error configuring stage field:', error);
      throw error;
    }
  }

  /**
   * Update field visibility for a stage
   */
  static async updateFieldVisibility(
    configId: string,
    request: UpdateFieldVisibilityRequest
  ): Promise<FieldConfiguration> {
    try {
      const response = await api.authenticatedRequest<FieldConfiguration>(
        `${this.BASE_PATH}/configurations/${configId}/visibility`,
        {
          method: 'PUT',
          body: JSON.stringify(request)
        }
      );
      return response;
    } catch (error) {
      console.error('Error updating field visibility:', error);
      throw error;
    }
  }

  /**
   * List field configurations for a stage
   */
  static async listFieldConfigurationsByStage(stageId: string): Promise<FieldConfiguration[]> {
    try {
      const response = await api.authenticatedRequest<{ configurations?: FieldConfiguration[] } | FieldConfiguration[]>(
        `${this.BASE_PATH}/configurations/stage/${stageId}`
      );
      return Array.isArray(response) ? response : (response.configurations || []);
    } catch (error) {
      console.error('Error fetching field configurations:', error);
      throw error;
    }
  }

  /**
   * Helper: Generate a valid field key from field name
   */
  static generateFieldKey(fieldName: string): string {
    return fieldName
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '_')
      .replace(/^_+|_+$/g, '');
  }

  /**
   * Helper: Validate field key format
   */
  static isValidFieldKey(key: string): boolean {
    return /^[a-z][a-z0-9_]*$/.test(key);
  }
}
