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
 * Get the base path for custom field value endpoints (company-scoped)
 */
function getBasePath(): string {
  return `/${getCompanySlug()}/admin/custom-field-values`;
}

class CustomFieldValueService {
  /**
   * Get all custom field values for a company candidate (current workflow only)
   */
  async getCustomFieldValuesByCompanyCandidate(companyCandidateId: string): Promise<Record<string, CustomFieldValue>> {
    return ApiClient.authenticatedRequest<Record<string, CustomFieldValue>>(
      `${getBasePath()}/company-candidate/${companyCandidateId}`
    );
  }

  /**
   * Get all custom field values for a company candidate, organized by workflow_id
   */
  async getAllCustomFieldValuesByCompanyCandidate(companyCandidateId: string): Promise<Record<string, Record<string, CustomFieldValue>>> {
    return ApiClient.authenticatedRequest<Record<string, Record<string, CustomFieldValue>>>(
      `${getBasePath()}/company-candidate/${companyCandidateId}/all`
    );
  }

  /**
   * Create a new custom field value
   */
  async createCustomFieldValue(data: CreateCustomFieldValueRequest): Promise<CustomFieldValue> {
    return ApiClient.authenticatedRequest<CustomFieldValue>(getBasePath(), {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  /**
   * Update an existing custom field value
   */
  async updateCustomFieldValue(customFieldValueId: string, data: UpdateCustomFieldValueRequest): Promise<CustomFieldValue> {
    return ApiClient.authenticatedRequest<CustomFieldValue>(`${getBasePath()}/${customFieldValueId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  /**
   * Delete a custom field value
   */
  async deleteCustomFieldValue(customFieldValueId: string): Promise<void> {
    await ApiClient.authenticatedRequest(`${getBasePath()}/${customFieldValueId}`, {
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
      `${getBasePath()}/company-candidate/${companyCandidateId}/field/${customFieldId}`,
      {
        method: 'PUT',
        body: JSON.stringify({ value: fieldValue }),
      }
    );
  }
}

export const customFieldValueService = new CustomFieldValueService();
