/**
 * Phase Service
 * Phase 12: API service for managing phases
 */

import api from '@/lib/api';
import type { Phase, CreatePhaseRequest, UpdatePhaseRequest } from '@/types/phase';

export const phaseService = {
  /**
   * Get all phases for a company
   */
  async listPhases(companyId: string): Promise<Phase[]> {
    const response = await api.get(`/companies/${companyId}/phases`);
    return response.data;
  },

  /**
   * Get a phase by ID
   */
  async getPhase(companyId: string, phaseId: string): Promise<Phase> {
    const response = await api.get(`/companies/${companyId}/phases/${phaseId}`);
    return response.data;
  },

  /**
   * Create a new phase
   */
  async createPhase(companyId: string, data: CreatePhaseRequest): Promise<Phase> {
    const response = await api.post(`/companies/${companyId}/phases`, data);
    return response.data;
  },

  /**
   * Update an existing phase
   */
  async updatePhase(
    companyId: string,
    phaseId: string,
    data: UpdatePhaseRequest
  ): Promise<Phase> {
    const response = await api.put(`/companies/${companyId}/phases/${phaseId}`, data);
    return response.data;
  },

  /**
   * Delete a phase
   */
  async deletePhase(companyId: string, phaseId: string): Promise<void> {
    await api.delete(`/companies/${companyId}/phases/${phaseId}`);
  },
};
