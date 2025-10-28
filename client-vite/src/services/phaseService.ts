/**
 * Phase Service
 * Phase 12: API service for managing phases
 */

import { ApiClient } from '../lib/api';
import type { Phase, CreatePhaseRequest, UpdatePhaseRequest } from '../types/phase';

export const phaseService = {
  /**
   * Get all phases for a company
   */
  async listPhases(companyId: string): Promise<Phase[]> {
    return ApiClient.get<Phase[]>(`/api/companies/${companyId}/phases`);
  },

  /**
   * Get a phase by ID
   */
  async getPhase(companyId: string, phaseId: string): Promise<Phase> {
    return ApiClient.get<Phase>(`/api/companies/${companyId}/phases/${phaseId}`);
  },

  /**
   * Create a new phase
   */
  async createPhase(companyId: string, data: CreatePhaseRequest): Promise<Phase> {
    return ApiClient.post<Phase>(`/api/companies/${companyId}/phases`, data);
  },

  /**
   * Update an existing phase
   */
  async updatePhase(
    companyId: string,
    phaseId: string,
    data: UpdatePhaseRequest
  ): Promise<Phase> {
    return ApiClient.put<Phase>(`/api/companies/${companyId}/phases/${phaseId}`, data);
  },

  /**
   * Delete a phase
   */
  async deletePhase(companyId: string, phaseId: string): Promise<void> {
    return ApiClient.delete<void>(`/api/companies/${companyId}/phases/${phaseId}`);
  },

  /**
   * Initialize default phases (reset configuration)
   * Creates 3 default phases with their workflows:
   * - Sourcing (Kanban)
   * - Evaluation (Kanban)
   * - Offer and Pre-Onboarding (List)
   */
  async initializeDefaultPhases(companyId: string): Promise<Phase[]> {
    return ApiClient.post<Phase[]>(`/api/companies/${companyId}/phases/initialize`);
  },

  /**
   * Archive a phase (soft delete)
   */
  async archivePhase(companyId: string, phaseId: string): Promise<Phase> {
    return ApiClient.post<Phase>(`/api/companies/${companyId}/phases/${phaseId}/archive`);
  },

  /**
   * Activate a phase
   */
  async activatePhase(companyId: string, phaseId: string): Promise<Phase> {
    return ApiClient.post<Phase>(`/api/companies/${companyId}/phases/${phaseId}/activate`);
  },
};
