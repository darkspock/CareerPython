/**
 * Public Position Service
 * Phase 10: Public job board - no authentication required
 */

import { ApiClient } from '../lib/api';
import type { Position } from '../types/position';

export interface PublicPositionFilters {
  search?: string;
  department?: string;
  location?: string;
  employment_type?: string;
  experience_level?: string;
  is_remote?: boolean;
  company_id?: string;
  page?: number;
  page_size?: number;
}

export interface PublicPositionListResponse {
  positions: Position[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export const publicPositionService = {
  /**
   * List all public (published) job positions
   * No authentication required
   */
  async listPublicPositions(filters?: PublicPositionFilters): Promise<PublicPositionListResponse> {
    const queryParams = new URLSearchParams();

    if (filters?.search) queryParams.append('search', filters.search);
    if (filters?.department) queryParams.append('department', filters.department);
    if (filters?.location) queryParams.append('location', filters.location);
    if (filters?.employment_type) queryParams.append('employment_type', filters.employment_type);
    if (filters?.experience_level) queryParams.append('experience_level', filters.experience_level);
    if (filters?.is_remote !== undefined) queryParams.append('is_remote', filters.is_remote.toString());
    if (filters?.company_id) queryParams.append('company_id', filters.company_id);
    if (filters?.page) queryParams.append('page', filters.page.toString());
    if (filters?.page_size) queryParams.append('page_size', filters.page_size.toString());

    const endpoint = `/public/positions${queryParams.toString() ? `?${queryParams}` : ''}`;

    try {
      const response = await ApiClient.get<PublicPositionListResponse>(endpoint);
      return {
        positions: response.positions || [],
        total: response.total || 0,
        page: response.page || 1,
        page_size: response.page_size || 10,
        total_pages: response.total_pages || 0
      };
    } catch (error) {
      console.error('[PublicPositionService] Error fetching public positions:', error);
      throw error;
    }
  },

  /**
   * Get a single public position by slug or ID
   * No authentication required
   */
  async getPublicPosition(slugOrId: string): Promise<Position> {
    try {
      return await ApiClient.get<Position>(`/public/positions/${slugOrId}`);
    } catch (error) {
      console.error('[PublicPositionService] Error fetching public position:', error);
      throw error;
    }
  },

  /**
   * Submit an application to a public position
   * Requires candidate authentication
   */
  async submitApplication(
    slugOrId: string,
    data: {
      cover_letter?: string;
      referral_source?: string;
    }
  ): Promise<{ application_id: string; message: string }> {
    try {
      return await ApiClient.post<{ application_id: string; message: string }>(
        `/public/positions/${slugOrId}/apply`,
        data
      );
    } catch (error) {
      console.error('[PublicPositionService] Error submitting application:', error);
      throw error;
    }
  }
};
