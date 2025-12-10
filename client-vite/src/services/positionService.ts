// Position API service - Updated for workflow-based system
// Includes Publishing Flow methods (PRD v2.1)
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
  StatusTransitionResponse,
  PositionStatusStats
} from '../types/position';
import { ClosedReason } from '../types/position';

export class PositionService {
  private static readonly BASE_PATH = '/api/company/positions';
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
    if (filters?.is_active !== undefined) queryParams.append('is_active', filters.is_active.toString());
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
  static async getWorkflows(companyId: string): Promise<JobPositionWorkflow[]> {
    try {
      const queryParams = new URLSearchParams();
      queryParams.append('company_id', companyId);

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
   * Update existing workflow
   */
  static async updateWorkflow(
    workflowId: string,
    workflowData: {
      name: string;
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
   * Publish/Activate workflow (set status to 'published')
   */
  static async publishWorkflow(workflowId: string, workflowData: { name: string; default_view: string }): Promise<JobPositionWorkflow> {
    try {
      const response = await api.authenticatedRequest<JobPositionWorkflow>(`${this.WORKFLOW_BASE_PATH}/${workflowId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          ...workflowData,
          status: 'published'
        })
      });
      return response;
    } catch (error) {
      console.error(`Error publishing workflow ${workflowId}:`, error);
      throw error;
    }
  }

  /**
   * Archive workflow (set status to 'deprecated')
   */
  static async archiveWorkflow(workflowId: string, workflowData: { name: string; default_view: string }): Promise<JobPositionWorkflow> {
    try {
      const response = await api.authenticatedRequest<JobPositionWorkflow>(`${this.WORKFLOW_BASE_PATH}/${workflowId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          ...workflowData,
          status: 'deprecated'
        })
      });
      return response;
    } catch (error) {
      console.error(`Error archiving workflow ${workflowId}:`, error);
      throw error;
    }
  }

  /**
   * Create new workflow
   */
  static async createWorkflow(workflowData: {
    company_id: string;
    name: string;
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
   * Initialize default job position workflows
   * Creates default workflows for managing job positions through stages
   */
  static async initializeDefaultWorkflows(companyId: string): Promise<JobPositionWorkflow[]> {
    try {
      const response = await api.authenticatedRequest<JobPositionWorkflow[]>(
        `/admin/workflows/initialize?company_id=${companyId}`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          }
        }
      );
      return response;
    } catch (error) {
      console.error('Error initializing default workflows:', error);
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

  // ====================================
  // PUBLISHING FLOW METHODS
  // ====================================

  /**
   * Request approval for a position
   * Transition: DRAFT → PENDING_APPROVAL
   */
  static async requestApproval(positionId: string): Promise<StatusTransitionResponse> {
    try {
      const response = await api.authenticatedRequest<StatusTransitionResponse>(
        `${this.BASE_PATH}/${positionId}/request-approval`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' }
        }
      );
      return response;
    } catch (error) {
      console.error(`Error requesting approval for position ${positionId}:`, error);
      throw error;
    }
  }

  /**
   * Approve a position
   * Transition: PENDING_APPROVAL → APPROVED
   */
  static async approve(positionId: string): Promise<StatusTransitionResponse> {
    try {
      const response = await api.authenticatedRequest<StatusTransitionResponse>(
        `${this.BASE_PATH}/${positionId}/approve`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' }
        }
      );
      return response;
    } catch (error) {
      console.error(`Error approving position ${positionId}:`, error);
      throw error;
    }
  }

  /**
   * Reject a position
   * Transition: PENDING_APPROVAL → REJECTED
   */
  static async reject(positionId: string, reason: string): Promise<StatusTransitionResponse> {
    try {
      const response = await api.authenticatedRequest<StatusTransitionResponse>(
        `${this.BASE_PATH}/${positionId}/reject`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ reason })
        }
      );
      return response;
    } catch (error) {
      console.error(`Error rejecting position ${positionId}:`, error);
      throw error;
    }
  }

  /**
   * Publish a position
   * Transition: APPROVED → PUBLISHED or DRAFT → PUBLISHED (quick mode)
   */
  static async publish(positionId: string): Promise<StatusTransitionResponse> {
    try {
      const response = await api.authenticatedRequest<StatusTransitionResponse>(
        `${this.BASE_PATH}/${positionId}/publish`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' }
        }
      );
      return response;
    } catch (error) {
      console.error(`Error publishing position ${positionId}:`, error);
      throw error;
    }
  }

  /**
   * Put a position on hold
   * Transition: PUBLISHED → ON_HOLD
   */
  static async hold(positionId: string): Promise<StatusTransitionResponse> {
    try {
      const response = await api.authenticatedRequest<StatusTransitionResponse>(
        `${this.BASE_PATH}/${positionId}/hold`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' }
        }
      );
      return response;
    } catch (error) {
      console.error(`Error holding position ${positionId}:`, error);
      throw error;
    }
  }

  /**
   * Resume a position from on-hold
   * Transition: ON_HOLD → PUBLISHED
   */
  static async resume(positionId: string): Promise<StatusTransitionResponse> {
    try {
      const response = await api.authenticatedRequest<StatusTransitionResponse>(
        `${this.BASE_PATH}/${positionId}/resume`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' }
        }
      );
      return response;
    } catch (error) {
      console.error(`Error resuming position ${positionId}:`, error);
      throw error;
    }
  }

  /**
   * Close a position
   * Transition: PUBLISHED/ON_HOLD → CLOSED
   */
  static async close(positionId: string, closedReason: ClosedReason, note?: string): Promise<StatusTransitionResponse> {
    try {
      const response = await api.authenticatedRequest<StatusTransitionResponse>(
        `${this.BASE_PATH}/${positionId}/close`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ closed_reason: closedReason, note })
        }
      );
      return response;
    } catch (error) {
      console.error(`Error closing position ${positionId}:`, error);
      throw error;
    }
  }

  /**
   * Archive a position
   * Transition: CLOSED → ARCHIVED
   */
  static async archive(positionId: string): Promise<StatusTransitionResponse> {
    try {
      const response = await api.authenticatedRequest<StatusTransitionResponse>(
        `${this.BASE_PATH}/${positionId}/archive`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' }
        }
      );
      return response;
    } catch (error) {
      console.error(`Error archiving position ${positionId}:`, error);
      throw error;
    }
  }

  /**
   * Revert a position to draft
   * Transition: REJECTED/APPROVED/CLOSED → DRAFT
   */
  static async revertToDraft(positionId: string): Promise<StatusTransitionResponse> {
    try {
      const response = await api.authenticatedRequest<StatusTransitionResponse>(
        `${this.BASE_PATH}/${positionId}/revert-to-draft`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' }
        }
      );
      return response;
    } catch (error) {
      console.error(`Error reverting position ${positionId} to draft:`, error);
      throw error;
    }
  }

  /**
   * Clone a position
   * Creates a new position in DRAFT with copied data
   */
  static async clone(positionId: string, newTitle?: string): Promise<Position> {
    try {
      const response = await api.authenticatedRequest<Position>(
        `${this.BASE_PATH}/${positionId}/clone`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ new_title: newTitle })
        }
      );
      return response;
    } catch (error) {
      console.error(`Error cloning position ${positionId}:`, error);
      throw error;
    }
  }

  /**
   * Get position stats by status
   */
  static async getStatusStats(companyId?: string): Promise<PositionStatusStats> {
    try {
      const queryParams = companyId ? `?company_id=${companyId}` : '';
      const response = await api.authenticatedRequest<PositionStatusStats>(
        `${this.BASE_PATH}/status-stats${queryParams}`
      );
      return response;
    } catch (error) {
      console.error('Error fetching position status stats:', error);
      throw error;
    }
  }

  /**
   * Get positions pending approval for current user
   */
  static async getPendingApprovals(): Promise<Position[]> {
    try {
      const response = await api.authenticatedRequest<Position[]>(
        `${this.BASE_PATH}/pending-approvals`
      );
      return response;
    } catch (error) {
      console.error('Error fetching pending approvals:', error);
      throw error;
    }
  }
}

export default PositionService;
