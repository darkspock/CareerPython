import { ApiClient } from '../lib/api';

export interface CustomFieldValue {
  id: string | null;
  field_id: string;
  field_name: string;
  field_type: string;
  field_config: Record<string, any> | null;
  value: any;
  created_at: string | null;
  updated_at: string | null;
}

export interface CreateCustomFieldValueRequest {
  company_candidate_id: string;
  custom_field_id: string;
  field_value: any;
}

export interface UpdateCustomFieldValueRequest {
  field_value: any;
}

class CustomFieldValueService {
  private baseUrl = '/api/company-workflow/custom-field-values';

  /**
   * Get all custom field values for a company candidate (current workflow only)
   */
  async getCustomFieldValuesByCompanyCandidate(companyCandidateId: string): Promise<Record<string, CustomFieldValue>> {
    return ApiClient.authenticatedRequest<Record<string, CustomFieldValue>>(
      `${this.baseUrl}/company-candidate/${companyCandidateId}`
    );
  }

  /**
   * Get all custom field values for a company candidate, organized by workflow_id
   */
  async getAllCustomFieldValuesByCompanyCandidate(companyCandidateId: string): Promise<Record<string, Record<string, CustomFieldValue>>> {
    return ApiClient.authenticatedRequest<Record<string, Record<string, CustomFieldValue>>>(
      `${this.baseUrl}/company-candidate/${companyCandidateId}/all`
    );
  }

  /**
   * Create a new custom field value
   */
  async createCustomFieldValue(data: CreateCustomFieldValueRequest): Promise<CustomFieldValue> {
    return ApiClient.authenticatedRequest<CustomFieldValue>(this.baseUrl, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  /**
   * Update an existing custom field value
   */
  async updateCustomFieldValue(customFieldValueId: string, data: UpdateCustomFieldValueRequest): Promise<CustomFieldValue> {
    return ApiClient.authenticatedRequest<CustomFieldValue>(`${this.baseUrl}/${customFieldValueId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  /**
   * Delete a custom field value
   */
  async deleteCustomFieldValue(customFieldValueId: string): Promise<void> {
    await ApiClient.authenticatedRequest(`${this.baseUrl}/${customFieldValueId}`, {
      method: 'DELETE',
    });
  }

  /**
   * Update or create a custom field value for a company candidate
   * This is a convenience method that handles both create and update
   */
  async upsertCustomFieldValue(
    companyCandidateId: string, 
    customFieldId: string, 
    fieldValue: any
  ): Promise<CustomFieldValue> {
    // Use the new endpoint that handles upsert directly
    return ApiClient.authenticatedRequest<CustomFieldValue>(
      `${this.baseUrl}/company-candidate/${companyCandidateId}/field/${customFieldId}`,
      {
        method: 'PUT',
        body: JSON.stringify({ value: fieldValue }),
      }
    );
  }
}

export const customFieldValueService = new CustomFieldValueService();
