// Validation Rule API service
import { api } from '../lib/api';
import type {
  ValidationRule,
  CreateValidationRuleRequest,
  UpdateValidationRuleRequest,
  ValidationResult,
  ValidateStageRequest
} from '../types/workflow';

export class ValidationRuleService {
  private static readonly BASE_PATH = '/validation-rules';

  /**
   * Create a new validation rule
   */
  static async createValidationRule(request: CreateValidationRuleRequest): Promise<ValidationRule> {
    try {
      const response = await api.authenticatedRequest<ValidationRule>(this.BASE_PATH, {
        method: 'POST',
        body: JSON.stringify(request)
      });
      return response;
    } catch (error) {
      console.error('Error creating validation rule:', error);
      throw error;
    }
  }

  /**
   * Get validation rule by ID
   */
  static async getValidationRuleById(ruleId: string): Promise<ValidationRule> {
    try {
      const response = await api.authenticatedRequest<ValidationRule>(`${this.BASE_PATH}/${ruleId}`);
      return response;
    } catch (error) {
      console.error('Error fetching validation rule:', error);
      throw error;
    }
  }

  /**
   * List validation rules for a stage
   */
  static async listValidationRulesByStage(stageId: string, activeOnly = false): Promise<ValidationRule[]> {
    try {
      const url = `${this.BASE_PATH}/stage/${stageId}${activeOnly ? '?active_only=true' : ''}`;
      const response = await api.authenticatedRequest<ValidationRule[]>(url);
      return response;
    } catch (error) {
      console.error('Error listing validation rules by stage:', error);
      throw error;
    }
  }

  /**
   * List validation rules for a custom field
   */
  static async listValidationRulesByField(customFieldId: string, activeOnly = false): Promise<ValidationRule[]> {
    try {
      const url = `${this.BASE_PATH}/field/${customFieldId}${activeOnly ? '?active_only=true' : ''}`;
      const response = await api.authenticatedRequest<ValidationRule[]>(url);
      return response;
    } catch (error) {
      console.error('Error listing validation rules by field:', error);
      throw error;
    }
  }

  /**
   * Update a validation rule
   */
  static async updateValidationRule(ruleId: string, request: UpdateValidationRuleRequest): Promise<ValidationRule> {
    try {
      const response = await api.authenticatedRequest<ValidationRule>(`${this.BASE_PATH}/${ruleId}`, {
        method: 'PUT',
        body: JSON.stringify(request)
      });
      return response;
    } catch (error) {
      console.error('Error updating validation rule:', error);
      throw error;
    }
  }

  /**
   * Delete a validation rule
   */
  static async deleteValidationRule(ruleId: string): Promise<void> {
    try {
      await api.authenticatedRequest(`${this.BASE_PATH}/${ruleId}`, {
        method: 'DELETE'
      });
    } catch (error) {
      console.error('Error deleting validation rule:', error);
      throw error;
    }
  }

  /**
   * Activate a validation rule
   */
  static async activateValidationRule(ruleId: string): Promise<ValidationRule> {
    try {
      const response = await api.authenticatedRequest<ValidationRule>(`${this.BASE_PATH}/${ruleId}/activate`, {
        method: 'POST'
      });
      return response;
    } catch (error) {
      console.error('Error activating validation rule:', error);
      throw error;
    }
  }

  /**
   * Deactivate a validation rule
   */
  static async deactivateValidationRule(ruleId: string): Promise<ValidationRule> {
    try {
      const response = await api.authenticatedRequest<ValidationRule>(`${this.BASE_PATH}/${ruleId}/deactivate`, {
        method: 'POST'
      });
      return response;
    } catch (error) {
      console.error('Error deactivating validation rule:', error);
      throw error;
    }
  }

  /**
   * Validate a stage transition (preview)
   */
  static async validateStageTransition(request: ValidateStageRequest): Promise<ValidationResult> {
    try {
      const response = await api.authenticatedRequest<ValidationResult>(`${this.BASE_PATH}/validate-stage`, {
        method: 'POST',
        body: JSON.stringify(request)
      });
      return response;
    } catch (error) {
      console.error('Error validating stage transition:', error);
      throw error;
    }
  }
}
