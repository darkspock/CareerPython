/**
 * Service for Candidate Application operations
 * Phase 5: Application Processing with Validations
 */

import { api } from '../lib/api';
import type { CandidateApplication, PermissionCheckResponse } from '../types/candidateApplication';

export class CandidateApplicationService {
  private static readonly BASE_PATH = '/api/company/candidate-applications';

  /**
   * Check if a user has permission to process an application
   */
  static async canUserProcessApplication(
    applicationId: string,
    userId: string,
    companyId: string
  ): Promise<boolean> {
    try {
      const response = await api.authenticatedRequest<PermissionCheckResponse>(
        `${this.BASE_PATH}/${applicationId}/can-process?user_id=${userId}&company_id=${companyId}`
      );
      return response.can_process;
    } catch (error) {
      console.error('[CandidateApplicationService] Error checking permission:', error);
      return false;
    }
  }

  /**
   * Get application by ID
   */
  static async getApplicationById(applicationId: string): Promise<CandidateApplication | null> {
    try {
      const response = await api.authenticatedRequest<CandidateApplication>(
        `${this.BASE_PATH}/${applicationId}`
      );
      return response;
    } catch (error) {
      console.error('[CandidateApplicationService] Error fetching application:', error);
      return null;
    }
  }

  /**
   * Get applications for a specific position
   */
  static async getApplicationsByPosition(positionId: string): Promise<CandidateApplication[]> {
    try {
      const response = await api.authenticatedRequest<CandidateApplication[]>(
        `${this.BASE_PATH}/position/${positionId}`
      );
      return response;
    } catch (error) {
      console.error('[CandidateApplicationService] Error fetching applications:', error);
      return [];
    }
  }

  /**
   * Get applications for a specific candidate
   */
  static async getApplicationsByCandidate(candidateId: string): Promise<CandidateApplication[]> {
    try {
      const response = await api.authenticatedRequest<CandidateApplication[]>(
        `${this.BASE_PATH}/candidate/${candidateId}`
      );
      return response;
    } catch (error) {
      console.error('[CandidateApplicationService] Error fetching applications:', error);
      return [];
    }
  }

  /**
   * Update application status
   */
  static async updateApplicationStatus(
    applicationId: string,
    status: string,
    notes?: string
  ): Promise<void> {
    try {
      await api.authenticatedRequest(
        `${this.BASE_PATH}/${applicationId}/status`,
        {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ status, notes })
        }
      );
    } catch (error) {
      console.error('[CandidateApplicationService] Error updating status:', error);
      throw error;
    }
  }

  /**
   * Move application to a different stage
   */
  static async moveToStage(
    applicationId: string,
    stageId: string,
    userId: string
  ): Promise<void> {
    try {
      await api.authenticatedRequest(
        `${this.BASE_PATH}/${applicationId}/move-stage`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ stage_id: stageId, user_id: userId })
        }
      );
    } catch (error) {
      console.error('[CandidateApplicationService] Error moving to stage:', error);
      throw error;
    }
  }
}

export default CandidateApplicationService;
