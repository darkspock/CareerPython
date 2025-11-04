// Position API service
import { api } from '../lib/api';
import { API_BASE_URL } from '../config/api';
import type {
  Position,
  PositionFilters,
  PositionStats,
  CreatePositionRequest,
  UpdatePositionRequest,
  PositionListResponse,
  PositionActionResponse
} from '../types/position';

export class PositionService {
  private static readonly BASE_PATH = '/admin/positions';

  /**
   * Get list of positions with optional filters
   */
  static async getPositions(filters?: PositionFilters): Promise<PositionListResponse> {
    const queryParams = new URLSearchParams();

    if (filters?.company_id) queryParams.append('company_id', filters.company_id);
    if (filters?.search_term) queryParams.append('search_term', filters.search_term);
    if (filters?.department) queryParams.append('department', filters.department);
    if (filters?.location) queryParams.append('location', filters.location);
    if (filters?.employment_type) queryParams.append('employment_type', filters.employment_type);
    if (filters?.experience_level) queryParams.append('experience_level', filters.experience_level);
    if (filters?.is_remote !== undefined) queryParams.append('is_remote', filters.is_remote.toString());
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

  /**
   * Activate position (changes status from DRAFT to ACTIVE)
   */
  static async activatePosition(positionId: string): Promise<PositionActionResponse> {
    try {
      const response = await api.authenticatedRequest<PositionActionResponse>(`${this.BASE_PATH}/${positionId}/activate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      });
      return response;
    } catch (error) {
      console.error(`Error activating position ${positionId}:`, error);
      throw error;
    }
  }

  /**
   * Pause position (changes status from ACTIVE to PAUSED)
   */
  static async pausePosition(positionId: string): Promise<PositionActionResponse> {
    try {
      const response = await api.authenticatedRequest<PositionActionResponse>(`${this.BASE_PATH}/${positionId}/pause`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      });
      return response;
    } catch (error) {
      console.error(`Error pausing position ${positionId}:`, error);
      throw error;
    }
  }

  /**
   * Resume position (changes status from PAUSED to ACTIVE)
   */
  static async resumePosition(positionId: string): Promise<PositionActionResponse> {
    try {
      const response = await api.authenticatedRequest<PositionActionResponse>(`${this.BASE_PATH}/${positionId}/resume`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      });
      return response;
    } catch (error) {
      console.error(`Error resuming position ${positionId}:`, error);
      throw error;
    }
  }

  /**
   * Close position
   */
  static async closePosition(positionId: string): Promise<PositionActionResponse> {
    try {
      const response = await api.authenticatedRequest<PositionActionResponse>(`${this.BASE_PATH}/${positionId}/close`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      });
      return response;
    } catch (error) {
      console.error(`Error closing position ${positionId}:`, error);
      throw error;
    }
  }

  /**
   * Archive position (changes status to ARCHIVED)
   */
  static async archivePosition(positionId: string): Promise<PositionActionResponse> {
    try {
      const response = await api.authenticatedRequest<PositionActionResponse>(`${this.BASE_PATH}/${positionId}/archive`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      });
      return response;
    } catch (error) {
      console.error(`Error archiving position ${positionId}:`, error);
      throw error;
    }
  }

  /**
   * Deactivate position
   */
  static async deactivatePosition(positionId: string): Promise<PositionActionResponse> {
    try {
      const response = await api.authenticatedRequest<PositionActionResponse>(`${this.BASE_PATH}/${positionId}/deactivate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      });
      return response;
    } catch (error) {
      console.error(`Error deactivating position ${positionId}:`, error);
      throw error;
    }
  }

  /**
   * Bulk operations
   */
  static async bulkActivatePositions(positionIds: string[]): Promise<PositionActionResponse> {
    try {
      const response = await api.authenticatedRequest<PositionActionResponse>(`${this.BASE_PATH}/bulk/activate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ position_ids: positionIds })
      });
      return response;
    } catch (error) {
      console.error('Error bulk activating positions:', error);
      throw error;
    }
  }

  static async bulkDeactivatePositions(positionIds: string[]): Promise<PositionActionResponse> {
    try {
      const response = await api.authenticatedRequest<PositionActionResponse>(`${this.BASE_PATH}/bulk/deactivate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ position_ids: positionIds })
      });
      return response;
    } catch (error) {
      console.error('Error bulk deactivating positions:', error);
      throw error;
    }
  }

  static async bulkDeletePositions(positionIds: string[]): Promise<PositionActionResponse> {
    try {
      const response = await api.authenticatedRequest<PositionActionResponse>(`${this.BASE_PATH}/bulk/delete`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ position_ids: positionIds })
      });
      return response;
    } catch (error) {
      console.error('Error bulk deleting positions:', error);
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
    if (filters?.department) queryParams.append('department', filters.department);
    if (filters?.location) queryParams.append('location', filters.location);
    if (filters?.employment_type) queryParams.append('employment_type', filters.employment_type);
    if (filters?.experience_level) queryParams.append('experience_level', filters.experience_level);
    if (filters?.is_remote !== undefined) queryParams.append('is_remote', filters.is_remote.toString());
    if (filters?.is_active !== undefined) queryParams.append('is_active', filters.is_active.toString());
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