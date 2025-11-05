/**
 * Job Position Activity Service
 * 
 * Service for fetching activity history for job positions.
 */

import { ApiClient } from '../lib/api';
import type {
  JobPositionActivity,
  JobPositionActivityListResponse,
} from '../types/jobPositionActivity';

class JobPositionActivityService {
  private baseUrl = '/admin/positions';

  /**
   * List activities for a job position
   * 
   * @param positionId - ID of the job position
   * @param limit - Maximum number of activities to return (default: 50)
   */
  async listActivities(
    positionId: string,
    limit: number = 50
  ): Promise<JobPositionActivityListResponse> {
    const params = new URLSearchParams();
    params.append('limit', limit.toString());

    return ApiClient.authenticatedRequest<JobPositionActivityListResponse>(
      `${this.baseUrl}/${positionId}/activities?${params.toString()}`,
      { method: 'GET' }
    );
  }

  /**
   * Get all activities for a position
   */
  async getActivities(positionId: string, limit?: number): Promise<JobPositionActivity[]> {
    const response = await this.listActivities(positionId, limit);
    return response.activities;
  }

  /**
   * Filter activities by type
   */
  filterByType(activities: JobPositionActivity[], activityType: string): JobPositionActivity[] {
    return activities.filter(activity => activity.activity_type === activityType);
  }

  /**
   * Get activities for a specific date range
   */
  filterByDateRange(
    activities: JobPositionActivity[],
    startDate: Date,
    endDate: Date
  ): JobPositionActivity[] {
    return activities.filter(activity => {
      const activityDate = new Date(activity.created_at);
      return activityDate >= startDate && activityDate <= endDate;
    });
  }

  /**
   * Get activities by user
   */
  filterByUser(activities: JobPositionActivity[], userId: string): JobPositionActivity[] {
    return activities.filter(activity => activity.performed_by_user_id === userId);
  }

  /**
   * Format activity description for display
   * Can be extended with more sophisticated formatting logic
   */
  formatDescription(activity: JobPositionActivity): string {
    return activity.description;
  }

  /**
   * Get activity icon/color based on type (for UI)
   */
  getActivityIcon(activityType: string): string {
    const icons: Record<string, string> = {
      created: '✨',
      edited: '✏️',
      stage_moved: '🔄',
      status_changed: '📊',
      comment_added: '💬',
    };
    return icons[activityType] || '📝';
  }

  /**
   * Get activity color based on type (for UI)
   */
  getActivityColor(activityType: string): string {
    const colors: Record<string, string> = {
      created: 'blue',
      edited: 'green',
      stage_moved: 'purple',
      status_changed: 'orange',
      comment_added: 'gray',
    };
    return colors[activityType] || 'gray';
  }
}

export default new JobPositionActivityService();

