/**
 * Talent Pool Service
 * Phase 8: Service for talent pool API calls
 */

import api from '@/lib/api';
import type {
  TalentPoolEntry,
  AddToTalentPoolRequest,
  UpdateTalentPoolEntryRequest,
  ChangeTalentPoolStatusRequest,
  TalentPoolFilters,
  TalentPoolStatus
} from '@/types/talentPool';

export class TalentPoolService {
  private static readonly BASE_PATH = '/api/company/talent-pool';

  /**
   * Add a candidate to the talent pool
   */
  static async addToTalentPool(
    companyId: string,
    data: AddToTalentPoolRequest
  ): Promise<{ message: string }> {
    const response = await api.post(`${this.BASE_PATH}/${companyId}`, data);
    return await response.json();
  }

  /**
   * Get a talent pool entry by ID
   */
  static async getEntryById(entryId: string): Promise<TalentPoolEntry> {
    const response = await api.get(`${this.BASE_PATH}/entries/${entryId}`);
    return await response.json();
  }

  /**
   * List talent pool entries for a company
   */
  static async listEntries(
    companyId: string,
    filters?: TalentPoolFilters
  ): Promise<TalentPoolEntry[]> {
    const params = new URLSearchParams();

    if (filters?.status) {
      params.append('status', filters.status);
    }
    if (filters?.tags && filters.tags.length > 0) {
      filters.tags.forEach(tag => params.append('tags', tag));
    }
    if (filters?.min_rating) {
      params.append('min_rating', filters.min_rating.toString());
    }

    const queryString = params.toString();
    const url = queryString
      ? `${this.BASE_PATH}/${companyId}/entries?${queryString}`
      : `${this.BASE_PATH}/${companyId}/entries`;

    const response = await api.get(url);
    return await response.json();
  }

  /**
   * Search talent pool entries
   */
  static async searchEntries(
    companyId: string,
    filters?: TalentPoolFilters
  ): Promise<TalentPoolEntry[]> {
    const params = new URLSearchParams();

    if (filters?.search_term) {
      params.append('search_term', filters.search_term);
    }
    if (filters?.status) {
      params.append('status', filters.status);
    }
    if (filters?.tags && filters.tags.length > 0) {
      filters.tags.forEach(tag => params.append('tags', tag));
    }
    if (filters?.min_rating) {
      params.append('min_rating', filters.min_rating.toString());
    }

    const queryString = params.toString();
    const url = queryString
      ? `${this.BASE_PATH}/${companyId}/search?${queryString}`
      : `${this.BASE_PATH}/${companyId}/search`;

    const response = await api.get(url);
    return await response.json();
  }

  /**
   * Update a talent pool entry
   */
  static async updateEntry(
    entryId: string,
    data: UpdateTalentPoolEntryRequest
  ): Promise<{ message: string }> {
    const response = await api.put(`${this.BASE_PATH}/entries/${entryId}`, data);
    return await response.json();
  }

  /**
   * Change talent pool entry status
   */
  static async changeStatus(
    entryId: string,
    data: ChangeTalentPoolStatusRequest
  ): Promise<{ message: string }> {
    const response = await api.patch(`${this.BASE_PATH}/entries/${entryId}/status`, data);
    return await response.json();
  }

  /**
   * Remove from talent pool
   */
  static async removeFromTalentPool(entryId: string): Promise<{ message: string }> {
    const response = await api.delete(`${this.BASE_PATH}/entries/${entryId}`);
    return await response.json();
  }

  // Convenience methods

  /**
   * Get active entries only
   */
  static async getActiveEntries(companyId: string): Promise<TalentPoolEntry[]> {
    return this.listEntries(companyId, { status: TalentPoolStatus.ACTIVE });
  }

  /**
   * Get entries by rating
   */
  static async getEntriesByMinRating(
    companyId: string,
    minRating: number
  ): Promise<TalentPoolEntry[]> {
    return this.listEntries(companyId, { min_rating: minRating });
  }

  /**
   * Get entries by tags
   */
  static async getEntriesByTags(
    companyId: string,
    tags: string[]
  ): Promise<TalentPoolEntry[]> {
    return this.listEntries(companyId, { tags });
  }
}
