/**
 * Talent Pool Service
 * Phase 8: Service for talent pool API calls
 */

import { api } from '../lib/api';
import type {
  TalentPoolEntry,
  AddToTalentPoolRequest,
  UpdateTalentPoolEntryRequest,
  ChangeTalentPoolStatusRequest,
  TalentPoolFilters
} from '../types/talentPool';
import { TalentPoolStatus } from '../types/talentPool';

export class TalentPoolService {
  private static readonly BASE_PATH = '/api/company/talent-pool';

  /**
   * Add a candidate to the talent pool
   */
  static async addToTalentPool(
    companyId: string,
    data: AddToTalentPoolRequest
  ): Promise<{ message: string }> {
    return await api.authenticatedRequest<{ message: string }>(`${this.BASE_PATH}/${companyId}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
  }

  /**
   * Get a talent pool entry by ID
   */
  static async getEntryById(entryId: string): Promise<TalentPoolEntry> {
    return await api.authenticatedRequest<TalentPoolEntry>(`${this.BASE_PATH}/entries/${entryId}`);
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
      filters.tags.forEach((tag: string) => params.append('tags', tag));
    }
    if (filters?.min_rating) {
      params.append('min_rating', filters.min_rating.toString());
    }

    const queryString = params.toString();
    const url = queryString
      ? `${this.BASE_PATH}/${companyId}/entries?${queryString}`
      : `${this.BASE_PATH}/${companyId}/entries`;

    return await api.authenticatedRequest<TalentPoolEntry[]>(url);
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
      filters.tags.forEach((tag: string) => params.append('tags', tag));
    }
    if (filters?.min_rating) {
      params.append('min_rating', filters.min_rating.toString());
    }

    const queryString = params.toString();
    const url = queryString
      ? `${this.BASE_PATH}/${companyId}/search?${queryString}`
      : `${this.BASE_PATH}/${companyId}/search`;

    return await api.authenticatedRequest<TalentPoolEntry[]>(url);
  }

  /**
   * Update a talent pool entry
   */
  static async updateEntry(
    entryId: string,
    data: UpdateTalentPoolEntryRequest
  ): Promise<{ message: string }> {
    return await api.authenticatedRequest<{ message: string }>(`${this.BASE_PATH}/entries/${entryId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
  }

  /**
   * Change talent pool entry status
   */
  static async changeStatus(
    entryId: string,
    data: ChangeTalentPoolStatusRequest
  ): Promise<{ message: string }> {
    return await api.authenticatedRequest<{ message: string }>(`${this.BASE_PATH}/entries/${entryId}/status`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
  }

  /**
   * Remove from talent pool
   */
  static async removeFromTalentPool(entryId: string): Promise<{ message: string }> {
    return await api.authenticatedRequest<{ message: string }>(`${this.BASE_PATH}/entries/${entryId}`, {
      method: 'DELETE'
    });
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
