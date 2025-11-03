// Position Stage Assignment API service
import { api } from '../lib/api';
import type {
  PositionStageAssignment,
  AssignUsersToStageRequest,
  AddUserToStageRequest,
  RemoveUserFromStageRequest,
  CopyWorkflowAssignmentsRequest,
  PositionStageAssignmentResponse
} from '../types/positionStageAssignment';

export class PositionStageAssignmentService {
  private static readonly BASE_PATH = '/position-stage-assignments';

  /**
   * Assign users to a stage (replaces existing assignments)
   */
  static async assignUsersToStage(
    request: AssignUsersToStageRequest
  ): Promise<PositionStageAssignmentResponse> {
    try {
      const response = await api.authenticatedRequest<PositionStageAssignmentResponse>(`${this.BASE_PATH}/assign`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(request)
      });
      return response;
    } catch (error) {
      console.error('[PositionStageAssignmentService] Error assigning users to stage:', error);
      throw error;
    }
  }

  /**
   * Add a single user to a stage
   */
  static async addUserToStage(
    request: AddUserToStageRequest
  ): Promise<PositionStageAssignmentResponse> {
    try {
      const response = await api.authenticatedRequest<PositionStageAssignmentResponse>(`${this.BASE_PATH}/add-user`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(request)
      });
      return response;
    } catch (error) {
      console.error('[PositionStageAssignmentService] Error adding user to stage:', error);
      throw error;
    }
  }

  /**
   * Remove a single user from a stage
   */
  static async removeUserFromStage(
    request: RemoveUserFromStageRequest
  ): Promise<PositionStageAssignmentResponse> {
    try {
      const response = await api.authenticatedRequest<PositionStageAssignmentResponse>(`${this.BASE_PATH}/remove-user`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(request)
      });
      return response;
    } catch (error) {
      console.error('[PositionStageAssignmentService] Error removing user from stage:', error);
      throw error;
    }
  }

  /**
   * Copy workflow default assignments to position
   */
  static async copyWorkflowAssignments(
    request: CopyWorkflowAssignmentsRequest
  ): Promise<PositionStageAssignmentResponse[]> {
    try {
      const response = await api.authenticatedRequest<PositionStageAssignmentResponse[]>(`${this.BASE_PATH}/copy-workflow`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(request)
      });
      return response;
    } catch (error) {
      console.error('[PositionStageAssignmentService] Error copying workflow assignments:', error);
      throw error;
    }
  }

  /**
   * List all stage assignments for a position
   */
  static async listStageAssignments(
    positionId: string
  ): Promise<PositionStageAssignment[]> {
    try {
      const response = await api.authenticatedRequest<PositionStageAssignment[]>(`${this.BASE_PATH}/position/${positionId}`);
      return response;
    } catch (error) {
      console.error(`[PositionStageAssignmentService] Error listing assignments for position ${positionId}:`, error);
      throw error;
    }
  }

  /**
   * Get assigned users for a specific position-stage combination
   */
  static async getAssignedUsers(
    positionId: string,
    stageId: string
  ): Promise<string[]> {
    try {
      const response = await api.authenticatedRequest<string[]>(
        `${this.BASE_PATH}/position/${positionId}/stage/${stageId}/users`
      );
      return response;
    } catch (error) {
      console.error(
        `[PositionStageAssignmentService] Error getting users for position ${positionId}, stage ${stageId}:`,
        error
      );
      throw error;
    }
  }

  /**
   * Helper method: Check if a user is assigned to a stage
   */
  static async isUserAssignedToStage(
    positionId: string,
    stageId: string,
    userId: string
  ): Promise<boolean> {
    try {
      const assignedUsers = await this.getAssignedUsers(positionId, stageId);
      return assignedUsers.includes(userId);
    } catch (error) {
      console.error('[PositionStageAssignmentService] Error checking user assignment:', error);
      return false;
    }
  }

  /**
   * Helper method: Get assignment for a specific stage
   */
  static async getStageAssignment(
    positionId: string,
    stageId: string
  ): Promise<PositionStageAssignment | null> {
    try {
      const assignments = await this.listStageAssignments(positionId);
      return assignments.find(a => a.stage_id === stageId) || null;
    } catch (error) {
      console.error('[PositionStageAssignmentService] Error getting stage assignment:', error);
      return null;
    }
  }
}

export default PositionStageAssignmentService;
