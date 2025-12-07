/**
 * Public Question Service
 * Service for getting public-facing application questions
 */

import { ApiClient } from '../lib/api';
import type { ApplicationQuestionFieldType } from './applicationQuestionService';

export interface PublicApplicationQuestion {
  id: string;
  field_key: string;
  label: string;
  description?: string;
  field_type: ApplicationQuestionFieldType;
  options?: string[];
  is_required: boolean;
  sort_order: number;
}

export interface ApplicationAnswerValue {
  question_id: string;
  field_key: string;
  value: string | string[] | number | boolean;
}

export interface SaveAnswersRequest {
  answers: ApplicationAnswerValue[];
}

export const publicQuestionService = {
  /**
   * Get enabled questions for a public position
   */
  async getQuestionsForPosition(positionId: string): Promise<PublicApplicationQuestion[]> {
    return ApiClient.get<PublicApplicationQuestion[]>(
      `/api/public/positions/${positionId}/questions`
    );
  },

  /**
   * Save answers for an application (requires authentication)
   */
  async saveAnswers(applicationId: string, data: SaveAnswersRequest): Promise<void> {
    return ApiClient.post<void>(`/api/applications/${applicationId}/answers`, data);
  },

  /**
   * Get answers for an application (requires authentication)
   */
  async getAnswers(applicationId: string): Promise<ApplicationAnswerValue[]> {
    return ApiClient.get<ApplicationAnswerValue[]>(`/api/applications/${applicationId}/answers`);
  },
};
