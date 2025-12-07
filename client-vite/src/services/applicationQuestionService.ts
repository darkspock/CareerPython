/**
 * Application Question Service
 * Service for managing application questions at workflow level
 */

import { ApiClient } from '../lib/api';

export type ApplicationQuestionFieldType =
  | 'TEXT'
  | 'TEXTAREA'
  | 'NUMBER'
  | 'DATE'
  | 'SELECT'
  | 'MULTISELECT'
  | 'BOOLEAN';

export interface ApplicationQuestion {
  id: string;
  workflow_id: string;
  company_id: string;
  field_key: string;
  label: string;
  description?: string;
  field_type: ApplicationQuestionFieldType;
  options?: string[];
  is_required: boolean;
  validation_rules?: Record<string, unknown>;
  sort_order: number;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

export interface CreateApplicationQuestionRequest {
  field_key: string;
  label: string;
  description?: string;
  field_type: ApplicationQuestionFieldType;
  options?: string[];
  is_required?: boolean;
  validation_rules?: Record<string, unknown>;
  sort_order?: number;
}

export interface UpdateApplicationQuestionRequest {
  label?: string;
  description?: string;
  field_type?: ApplicationQuestionFieldType;
  options?: string[];
  is_required?: boolean;
  validation_rules?: Record<string, unknown>;
  sort_order?: number;
  is_active?: boolean;
}

export const applicationQuestionService = {
  /**
   * List all questions for a workflow
   */
  async listQuestions(workflowId: string, activeOnly: boolean = false): Promise<ApplicationQuestion[]> {
    const params = activeOnly ? '?active_only=true' : '';
    return ApiClient.get<ApplicationQuestion[]>(`/api/company/workflows/${workflowId}/questions${params}`);
  },

  /**
   * Create a new question for a workflow
   */
  async createQuestion(
    workflowId: string,
    data: CreateApplicationQuestionRequest
  ): Promise<ApplicationQuestion> {
    return ApiClient.post<ApplicationQuestion>(`/api/company/workflows/${workflowId}/questions`, data);
  },

  /**
   * Update an existing question
   */
  async updateQuestion(
    workflowId: string,
    questionId: string,
    data: UpdateApplicationQuestionRequest
  ): Promise<ApplicationQuestion> {
    return ApiClient.put<ApplicationQuestion>(
      `/api/company/workflows/${workflowId}/questions/${questionId}`,
      data
    );
  },

  /**
   * Delete a question
   */
  async deleteQuestion(workflowId: string, questionId: string): Promise<void> {
    return ApiClient.delete<void>(`/api/company/workflows/${workflowId}/questions/${questionId}`);
  },

  /**
   * Reorder questions
   */
  async reorderQuestions(
    workflowId: string,
    questionOrders: { question_id: string; sort_order: number }[]
  ): Promise<void> {
    // Update each question's sort_order
    await Promise.all(
      questionOrders.map(({ question_id, sort_order }) =>
        this.updateQuestion(workflowId, question_id, { sort_order })
      )
    );
  },
};
