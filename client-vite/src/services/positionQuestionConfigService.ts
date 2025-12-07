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

export const positionQuestionConfigService = {
  /**
   * List question configs for a position
   */
  async listConfigs(positionId: string): Promise<PositionQuestionConfig[]> {
    return ApiClient.get<PositionQuestionConfig[]>(`/api/company/positions/${positionId}/questions`);
  },

  /**
   * Get enabled questions for a position (combines workflow questions with position configs)
   */
  async getEnabledQuestions(positionId: string): Promise<EnabledQuestionForPosition[]> {
    return ApiClient.get<EnabledQuestionForPosition[]>(
      `/api/company/positions/${positionId}/questions/enabled`
    );
  },

  /**
   * Configure a question for a position (enable/disable, override settings)
   */
  async configureQuestion(
    positionId: string,
    data: ConfigurePositionQuestionRequest
  ): Promise<PositionQuestionConfig> {
    return ApiClient.post<PositionQuestionConfig>(`/api/company/positions/${positionId}/questions`, data);
  },

  /**
   * Remove question config (revert to workflow defaults)
   */
  async removeConfig(positionId: string, questionId: string): Promise<void> {
    return ApiClient.delete<void>(`/api/company/positions/${positionId}/questions/${questionId}`);
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
