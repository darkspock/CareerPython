// Position API service - Updated for workflow-based system
import { api } from '../lib/api';
import { API_BASE_URL } from '../config/api';
import type {
  Position,
  PositionFilters,
  PositionStats,
  CreatePositionRequest,
  UpdatePositionRequest,
  PositionListResponse,
  PositionActionResponse,
  JobPositionWorkflow,
  JobPositionWorkflowStage
} from '../types/position';

export class PositionService {
  private static readonly BASE_PATH = '/admin/positions';
  private static readonly WORKFLOW_BASE_PATH = '/admin/workflows';

  /**
   * Get list of positions with optional filters - simplified
   */
  static async getPositions(filters?: PositionFilters): Promise<PositionListResponse> {
    const queryParams = new URLSearchParams();

    if (filters?.company_id) queryParams.append('company_id', filters.company_id);
    if (filters?.search_term) queryParams.append('search_term', filters.search_term);
    if (filters?.job_category) queryParams.append('job_category', filters.job_category);
    if (filters?.visibility) queryParams.append('visibility', filters.visibility);
    if (filters?.page) queryParams.append('page', filters.page.toString());
    if (filters?.page_size) queryParams.append('page_size', filters.page_size.toString());

    const endpoint = `${this.BASE_PATH}${queryParams.toString() ? `?${queryParams}` : ''}`;

    console.log('[PositionService] Fetching from endpoint:', endpoint);
    console.log('[PositionService] Filters:', filters);

    try {
      const response = await api.authenticatedRequest<PositionListResponse>(endpoint);
      console.log('[PositionService] Raw API response:', response);

      return {
        positions: response.positions || [],
        total: response.total || 0,
        page: response.page || 1,
        page_size: response.page_size || 10,
        total_pages: response.total_pages || 0
      };
    } catch (error) {
      console.error('[PositionService] Error fetching positions:', error);
      throw error;
    }
  }

  /**
   * Get position statistics
   */
  static async getPositionStats(): Promise<PositionStats> {
    try {
      const response = await api.authenticatedRequest<PositionStats>(`${this.BASE_PATH}/stats`);
      return {
        total_positions: response.total_positions || 0,
        active_positions: response.active_positions || 0,
        inactive_positions: response.inactive_positions || 0,
        positions_by_type: response.positions_by_type || {},
        positions_by_level: response.positions_by_level || {},
        positions_by_company: response.positions_by_company || {}
      };
    } catch (error) {
      console.error('Error fetching position stats:', error);
      throw error;
    }
  }

  /**
   * Get single position by ID
   */
  static async getPositionById(positionId: string): Promise<Position> {
    try {
      const response = await api.authenticatedRequest<Position>(`${this.BASE_PATH}/${positionId}`);
      return response;
    } catch (error) {
      console.error(`Error fetching position ${positionId}:`, error);
      throw error;
    }
  }

  /**
   * Create new position
   */
  static async createPosition(positionData: CreatePositionRequest): Promise<Position> {
    try {
      const response = await api.authenticatedRequest<Position>(this.BASE_PATH, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(positionData)
      });
      return response;
    } catch (error) {
      console.error('Error creating position:', error);
      throw error;
    }
  }

  /**
   * Update existing position
   */
  static async updatePosition(positionId: string, positionData: UpdatePositionRequest): Promise<Position> {
    try {
      const response = await api.authenticatedRequest<Position>(`${this.BASE_PATH}/${positionId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(positionData)
      });
      return response;
    } catch (error) {
      console.error(`Error updating position ${positionId}:`, error);
      throw error;
    }
  }

  /**
   * Delete position
   */
  static async deletePosition(positionId: string): Promise<PositionActionResponse> {
    try {
      const response = await api.authenticatedRequest<PositionActionResponse>(`${this.BASE_PATH}/${positionId}`, {
        method: 'DELETE'
      });
      return response;
    } catch (error) {
      console.error(`Error deleting position ${positionId}:`, error);
      throw error;
    }
  }

  // ====================================
  // WORKFLOW METHODS
  // ====================================

  /**
   * Get list of workflows for a company
   */
  static async getWorkflows(companyId: string, workflowType?: string): Promise<JobPositionWorkflow[]> {
    try {
      const queryParams = new URLSearchParams();
      queryParams.append('company_id', companyId);
      if (workflowType) queryParams.append('workflow_type', workflowType);

      const endpoint = `${this.WORKFLOW_BASE_PATH}?${queryParams.toString()}`;
      const response = await api.authenticatedRequest<JobPositionWorkflow[]>(endpoint);
      return response || [];
    } catch (error) {
      console.error('Error fetching workflows:', error);
      throw error;
    }
  }

  /**
   * Get single workflow by ID
   */
  static async getWorkflow(workflowId: string): Promise<JobPositionWorkflow> {
    try {
      const response = await api.authenticatedRequest<JobPositionWorkflow>(`${this.WORKFLOW_BASE_PATH}/${workflowId}`);
      return response;
    } catch (error) {
      console.error(`Error fetching workflow ${workflowId}:`, error);
      throw error;
    }
  }

  /**
   * Create new workflow
   */
  static async createWorkflow(workflowData: {
    company_id: string;
    name: string;
    workflow_type?: string;
    default_view?: string;
    stages?: Array<{
      id: string;
      name: string;
      icon: string;
      background_color: string;
      text_color: string;
      role?: string | null;
      status_mapping: string;
      kanban_display?: string;
      field_visibility?: Record<string, boolean>;
      field_validation?: Record<string, any>;
      field_candidate_visibility?: Record<string, boolean>;
    }>;
    custom_fields_config?: Record<string, any>;
  }): Promise<JobPositionWorkflow> {
    try {
      const response = await api.authenticatedRequest<JobPositionWorkflow>(this.WORKFLOW_BASE_PATH, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(workflowData)
      });
      return response;
    } catch (error) {
      console.error('Error creating workflow:', error);
      throw error;
    }
  }

  /**
   * Update existing workflow
   */
  static async updateWorkflow(
    workflowId: string,
    workflowData: {
      name: string;
      workflow_type?: string;
      default_view?: string;
      stages?: Array<{
        id: string;
        name: string;
        icon: string;
        background_color: string;
        text_color: string;
        role?: string | null;
        status_mapping: string;
        kanban_display?: string;
        field_visibility?: Record<string, boolean>;
        field_validation?: Record<string, any>;
        field_candidate_visibility?: Record<string, boolean>;
      }>;
      custom_fields_config?: Record<string, any>;
    }
  ): Promise<JobPositionWorkflow> {
    try {
      const response = await api.authenticatedRequest<JobPositionWorkflow>(`${this.WORKFLOW_BASE_PATH}/${workflowId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(workflowData)
      });
      return response;
    } catch (error) {
      console.error(`Error updating workflow ${workflowId}:`, error);
      throw error;
    }
  }

  /**
   * Move position to a new stage
   */
  static async moveToStage(positionId: string, stageId: string, comment?: string): Promise<{ success: boolean; message: string; position_id: string }> {
    try {
      const response = await api.authenticatedRequest<{ success: boolean; message: string; position_id: string }>(
        `${this.BASE_PATH}/${positionId}/move-to-stage`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            stage_id: stageId,
            comment: comment || null
          })
        }
      );
      return response;
    } catch (error) {
      console.error(`Error moving position ${positionId} to stage ${stageId}:`, error);
      throw error;
    }
  }

  /**
   * Update custom fields values for a position
   */
  static async updateCustomFields(positionId: string, customFieldsValues: Record<string, any>): Promise<{ success: boolean; message: string; position_id: string }> {
    try {
      const response = await api.authenticatedRequest<{ success: boolean; message: string; position_id: string }>(
        `${this.BASE_PATH}/${positionId}/custom-fields`,
        {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            custom_fields_values: customFieldsValues
          })
        }
      );
      return response;
    } catch (error) {
      console.error(`Error updating custom fields for position ${positionId}:`, error);
      throw error;
    }
  }

  /**
   * Export positions data
   */
  static async exportPositions(filters?: PositionFilters, format: 'csv' | 'excel' = 'csv'): Promise<Blob> {
    const queryParams = new URLSearchParams();

    if (filters?.company_id) queryParams.append('company_id', filters.company_id);
    if (filters?.search_term) queryParams.append('search_term', filters.search_term);
    if (filters?.job_category) queryParams.append('job_category', filters.job_category);
    if (filters?.visibility) queryParams.append('visibility', filters.visibility);
    queryParams.append('format', format);

    const endpoint = `${this.BASE_PATH}/export${queryParams.toString() ? `?${queryParams}` : ''}`;

    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token') || ''}`
        }
      });
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      return await response.blob();
    } catch (error) {
      console.error('Error exporting positions:', error);
      throw error;
    }
  }
}

export default PositionService;
