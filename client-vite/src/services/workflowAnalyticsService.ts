/**
 * Workflow Analytics Service
 * Phase 9: Service for workflow analytics API calls
 */

import api from '@/lib/api';
import type { WorkflowAnalytics, StageBottleneck } from '@/types/workflowAnalytics';

export interface AnalyticsFilters {
  date_range_start?: string; // ISO date string
  date_range_end?: string; // ISO date string
}

export interface BottleneckFilters extends AnalyticsFilters {
  min_bottleneck_score?: number; // 0-100
}

export class WorkflowAnalyticsService {
  private static readonly BASE_PATH = '/api/company/workflows';

  /**
   * Get comprehensive analytics for a workflow
   */
  static async getWorkflowAnalytics(
    workflowId: string,
    filters?: AnalyticsFilters
  ): Promise<WorkflowAnalytics> {
    const params = new URLSearchParams();

    if (filters?.date_range_start) {
      params.append('date_range_start', filters.date_range_start);
    }
    if (filters?.date_range_end) {
      params.append('date_range_end', filters.date_range_end);
    }

    const queryString = params.toString();
    const url = queryString
      ? `${this.BASE_PATH}/${workflowId}/analytics?${queryString}`
      : `${this.BASE_PATH}/${workflowId}/analytics`;

    const response = await api.get(url);
    return await response.json();
  }

  /**
   * Get list of bottleneck stages in a workflow
   */
  static async getStageBottlenecks(
    workflowId: string,
    filters?: BottleneckFilters
  ): Promise<StageBottleneck[]> {
    const params = new URLSearchParams();

    if (filters?.date_range_start) {
      params.append('date_range_start', filters.date_range_start);
    }
    if (filters?.date_range_end) {
      params.append('date_range_end', filters.date_range_end);
    }
    if (filters?.min_bottleneck_score !== undefined) {
      params.append('min_bottleneck_score', filters.min_bottleneck_score.toString());
    }

    const queryString = params.toString();
    const url = queryString
      ? `${this.BASE_PATH}/${workflowId}/bottlenecks?${queryString}`
      : `${this.BASE_PATH}/${workflowId}/bottlenecks`;

    const response = await api.get(url);
    return await response.json();
  }

  // Convenience methods

  /**
   * Get analytics for the last 30 days
   */
  static async getAnalyticsLast30Days(workflowId: string): Promise<WorkflowAnalytics> {
    const endDate = new Date();
    const startDate = new Date();
    startDate.setDate(startDate.getDate() - 30);

    return this.getWorkflowAnalytics(workflowId, {
      date_range_start: startDate.toISOString(),
      date_range_end: endDate.toISOString()
    });
  }

  /**
   * Get analytics for the last 90 days
   */
  static async getAnalyticsLast90Days(workflowId: string): Promise<WorkflowAnalytics> {
    const endDate = new Date();
    const startDate = new Date();
    startDate.setDate(startDate.getDate() - 90);

    return this.getWorkflowAnalytics(workflowId, {
      date_range_start: startDate.toISOString(),
      date_range_end: endDate.toISOString()
    });
  }

  /**
   * Get only critical bottlenecks (score >= 70)
   */
  static async getCriticalBottlenecks(workflowId: string): Promise<StageBottleneck[]> {
    return this.getStageBottlenecks(workflowId, {
      min_bottleneck_score: 70
    });
  }
}
