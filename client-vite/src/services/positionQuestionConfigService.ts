/**
 * Position Question Config Service
 * Service for managing position-level question configurations
 */

import { ApiClient } from '../lib/api';
import type { ApplicationQuestion } from './applicationQuestionService';

export interface PositionQuestionConfig {
  id: string;
  position_id: string;
  question_id: string;
  enabled: boolean;
  is_required_override?: boolean;
  sort_order_override?: number;
  created_at: string;
  updated_at?: string;
}

export interface EnabledQuestionForPosition {
  question: ApplicationQuestion;
  config?: PositionQuestionConfig;
  is_enabled: boolean;
  is_required: boolean;
  sort_order: number;
}

export interface ConfigurePositionQuestionRequest {
  question_id: string;
  enabled: boolean;
  is_required_override?: boolean;
  sort_order_override?: number;
}

/**
 * Get the company slug from localStorage
 */
function getCompanySlug(): string {
  const slug = localStorage.getItem('company_slug');
  if (!slug) {
    throw new Error('Company slug not found. Please log in again.');
  }
  return slug;
}

export const positionQuestionConfigService = {
  /**
   * List question configs for a position
   */
  async listConfigs(positionId: string): Promise<PositionQuestionConfig[]> {
    const companySlug = getCompanySlug();
    return ApiClient.get<PositionQuestionConfig[]>(`/${companySlug}/admin/positions/${positionId}/questions`);
  },

  /**
   * Get enabled questions for a position (combines workflow questions with position configs)
   */
  async getEnabledQuestions(positionId: string): Promise<EnabledQuestionForPosition[]> {
    const companySlug = getCompanySlug();
    return ApiClient.get<EnabledQuestionForPosition[]>(
      `/${companySlug}/admin/positions/${positionId}/questions/enabled`
    );
  },

  /**
   * Configure a question for a position (enable/disable, override settings)
   */
  async configureQuestion(
    positionId: string,
    data: ConfigurePositionQuestionRequest
  ): Promise<PositionQuestionConfig> {
    const companySlug = getCompanySlug();
    return ApiClient.post<PositionQuestionConfig>(`/${companySlug}/admin/positions/${positionId}/questions`, data);
  },

  /**
   * Remove question config (revert to workflow defaults)
   */
  async removeConfig(positionId: string, questionId: string): Promise<void> {
    const companySlug = getCompanySlug();
    return ApiClient.delete<void>(`/${companySlug}/admin/positions/${positionId}/questions/${questionId}`);
  },

  /**
   * Batch update question configs
   */
  async batchConfigure(
    positionId: string,
    configs: ConfigurePositionQuestionRequest[]
  ): Promise<void> {
    // Configure each question sequentially
    for (const config of configs) {
      await this.configureQuestion(positionId, config);
    }
  },
};
