// Entity Customization API service - Generic system for customizing any entity
import { api } from '../lib/api';
import type {
  EntityCustomization,
  CustomField,
  CreateEntityCustomizationRequest,
  UpdateEntityCustomizationRequest,
  CreateCustomFieldRequest,
  EntityCustomizationType
} from '../types/customization';

export class EntityCustomizationService {
  private static readonly BASE_PATH = '/api/entity-customizations';

  /**
   * Get entity customization by entity type and entity ID
   */
  static async getCustomization(
    entityType: EntityCustomizationType,
    entityId: string
  ): Promise<EntityCustomization> {
    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}${this.BASE_PATH}/${entityType}/${entityId}`,
        {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token') || ''}`,
          },
        }
      );

      if (!response.ok) {
        const error: any = new Error(`API Error: ${response.status} ${response.statusText}`);
        error.status = response.status;
        throw error;
      }

      return await response.json();
    } catch (error: any) {
      console.error('Error fetching entity customization:', error);
      // Preserve status code for 404 handling
      if (error.status) {
        const err = new Error(error.message || 'Failed to fetch entity customization');
        (err as any).status = error.status;
        throw err;
      }
      throw error;
    }
  }

  /**
   * Get entity customization by ID
   */
  static async getCustomizationById(id: string): Promise<EntityCustomization> {
    try {
      const response = await api.authenticatedRequest<EntityCustomization>(
        `${this.BASE_PATH}/by-id/${id}`
      );
      return response;
    } catch (error) {
      console.error('Error fetching entity customization by ID:', error);
      throw error;
    }
  }

  /**
   * Create entity customization
   */
  static async createCustomization(
    request: CreateEntityCustomizationRequest
  ): Promise<EntityCustomization> {
    try {
      const response = await api.authenticatedRequest<EntityCustomization>(
        this.BASE_PATH,
        {
          method: 'POST',
          body: JSON.stringify(request)
        }
      );
      return response;
    } catch (error) {
      console.error('Error creating entity customization:', error);
      throw error;
    }
  }

  /**
   * Update entity customization
   */
  static async updateCustomization(
    customizationId: string,
    request: UpdateEntityCustomizationRequest
  ): Promise<EntityCustomization> {
    try {
      const response = await api.authenticatedRequest<EntityCustomization>(
        `${this.BASE_PATH}/${customizationId}`,
        {
          method: 'PUT',
          body: JSON.stringify(request)
        }
      );
      return response;
    } catch (error) {
      console.error('Error updating entity customization:', error);
      throw error;
    }
  }

  /**
   * Delete entity customization
   */
  static async deleteCustomization(customizationId: string): Promise<void> {
    try {
      await api.authenticatedRequest(
        `${this.BASE_PATH}/${customizationId}`,
        {
          method: 'DELETE'
        }
      );
    } catch (error) {
      console.error('Error deleting entity customization:', error);
      throw error;
    }
  }

  /**
   * List custom fields for an entity
   * This is a convenience method that gets the customization and returns its fields
   */
  static async listFieldsByEntity(
    entityType: EntityCustomizationType,
    entityId: string
  ): Promise<CustomField[]> {
    try {
      const customization = await this.getCustomization(entityType, entityId);
      return customization.fields || [];
    } catch (error: any) {
      // If customization doesn't exist, return empty array
      if (error?.status === 404) {
        return [];
      }
      console.error('Error listing fields by entity:', error);
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

