// Phase 6: Task Management Service
// Handles API calls for task assignment and processing

import api from '@/lib/api';
import {
  Task,
  TaskFilters,
  ClaimTaskRequest,
  UnclaimTaskRequest,
  TaskActionResponse
} from '@/types/task';

/**
 * Service for task management operations
 */
export class TaskService {
  private static readonly BASE_PATH = '/api/company/tasks';

  /**
   * Get all tasks assigned to the current user
   *
   * @param userId - ID of the user requesting tasks
   * @param filters - Optional filters (stage_id, limit)
   * @returns Promise with array of tasks sorted by priority
   */
  static async getMyAssignedTasks(
    userId: string,
    filters?: TaskFilters
  ): Promise<Task[]> {
    try {
      const params = new URLSearchParams({
        user_id: userId
      });

      if (filters?.stage_id) {
        params.append('stage_id', filters.stage_id);
      }

      if (filters?.limit) {
        params.append('limit', filters.limit.toString());
      }

      const response = await api.get(`${this.BASE_PATH}/my-tasks?${params.toString()}`);

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to fetch assigned tasks');
      }

      const tasks: Task[] = await response.json();
      return tasks;
    } catch (error) {
      console.error('Error fetching assigned tasks:', error);
      throw error;
    }
  }

  /**
   * Claim a task for processing
   * This updates the task status from PENDING to IN_PROGRESS
   *
   * @param applicationId - ID of the application to claim
   * @param userId - ID of the user claiming the task
   * @returns Promise with action response
   */
  static async claimTask(
    applicationId: string,
    userId: string
  ): Promise<TaskActionResponse> {
    try {
      const request: ClaimTaskRequest = {
        application_id: applicationId,
        user_id: userId
      };

      const response = await api.post(`${this.BASE_PATH}/claim`, request);

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to claim task');
      }

      const result: TaskActionResponse = await response.json();
      return result;
    } catch (error) {
      console.error('Error claiming task:', error);
      throw error;
    }
  }

  /**
   * Unclaim a task (release it back to pending status)
   * This updates the task status from IN_PROGRESS back to PENDING
   *
   * @param applicationId - ID of the application to unclaim
   * @param userId - ID of the user unclaiming the task
   * @returns Promise with action response
   */
  static async unclaimTask(
    applicationId: string,
    userId: string
  ): Promise<TaskActionResponse> {
    try {
      const request: UnclaimTaskRequest = {
        application_id: applicationId,
        user_id: userId
      };

      const response = await api.post(`${this.BASE_PATH}/unclaim`, request);

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to unclaim task');
      }

      const result: TaskActionResponse = await response.json();
      return result;
    } catch (error) {
      console.error('Error unclaiming task:', error);
      throw error;
    }
  }

  /**
   * Get tasks by stage
   * Convenience method to filter tasks by specific stage
   *
   * @param userId - ID of the user requesting tasks
   * @param stageId - ID of the stage to filter by
   * @param limit - Optional limit on number of results
   * @returns Promise with array of tasks for that stage
   */
  static async getTasksByStage(
    userId: string,
    stageId: string,
    limit?: number
  ): Promise<Task[]> {
    return this.getMyAssignedTasks(userId, { stage_id: stageId, limit });
  }

  /**
   * Get high priority tasks
   * Convenience method to get top priority tasks
   *
   * @param userId - ID of the user requesting tasks
   * @param limit - Number of top priority tasks to retrieve (default: 10)
   * @returns Promise with array of high priority tasks
   */
  static async getHighPriorityTasks(
    userId: string,
    limit: number = 10
  ): Promise<Task[]> {
    const tasks = await this.getMyAssignedTasks(userId, { limit });

    // Tasks are already sorted by priority from backend
    // Filter for high and critical priority only
    return tasks.filter(task =>
      task.priority_level === 'critical' || task.priority_level === 'high'
    );
  }

  /**
   * Get overdue tasks
   * Convenience method to get only overdue tasks
   *
   * @param userId - ID of the user requesting tasks
   * @returns Promise with array of overdue tasks
   */
  static async getOverdueTasks(userId: string): Promise<Task[]> {
    const tasks = await this.getMyAssignedTasks(userId);
    return tasks.filter(task => task.is_overdue);
  }

  /**
   * Get tasks in progress
   * Convenience method to get tasks user is currently working on
   *
   * @param userId - ID of the user requesting tasks
   * @returns Promise with array of in-progress tasks
   */
  static async getTasksInProgress(userId: string): Promise<Task[]> {
    const tasks = await this.getMyAssignedTasks(userId);
    return tasks.filter(task => task.task_status === 'in_progress');
  }
}

export default TaskService;
