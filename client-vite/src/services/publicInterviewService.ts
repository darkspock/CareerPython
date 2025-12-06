import { ApiClient } from '../lib/api';

export interface InterviewQuestion {
  id: string;
  name: string;
  description?: string;
  code?: string;
  sort_order: number;
  interview_template_section_id: string;
  scope?: string;
  data_type?: string;
  status?: string;
  allow_ai_followup?: boolean;
  legal_notice?: string;
}

export interface InterviewSection {
  id: string;
  name: string;
  intro?: string;
  prompt?: string;
  goal?: string;
  sort_order: number;
  section?: string;
  status?: string;
  questions: InterviewQuestion[];
}

export interface InterviewTemplate {
  id: string;
  name: string;
  intro?: string;
  prompt?: string;
  goal?: string;
  scoring_mode?: 'DISTANCE' | 'ABSOLUTE' | null;
  allow_ai_questions?: boolean;
  use_conversational_mode?: boolean;
  sections: InterviewSection[];
}

export interface InterviewQuestionsResponse {
  interview_id: string;
  interview_title?: string;
  interview_description?: string;
  template?: InterviewTemplate;
  existing_answers: Record<string, string | null>;
}

export interface SubmitAnswerRequest {
  question_id: string;
  answer_text?: string;
  question_text?: string;
}

export interface SubmitAnswerResponse {
  message: string;
  status: string;
}

export const publicInterviewService = {
  /**
   * Get interview questions by token
   * No authentication required
   */
  async getInterviewQuestions(
    interviewId: string,
    token: string
  ): Promise<InterviewQuestionsResponse> {
    try {
      return await ApiClient.get<InterviewQuestionsResponse>(
        `/api/candidate/interviews/${interviewId}/questions?token=${encodeURIComponent(token)}`
      );
    } catch (error) {
      console.error('[PublicInterviewService] Error fetching interview questions:', error);
      throw error;
    }
  },

  /**
   * Submit an answer for a question
   * No authentication required
   */
  async submitAnswer(
    interviewId: string,
    token: string,
    answer: SubmitAnswerRequest
  ): Promise<SubmitAnswerResponse> {
    try {
      return await ApiClient.post<SubmitAnswerResponse>(
        `/api/candidate/interviews/${interviewId}/answers?token=${encodeURIComponent(token)}`,
        answer
      );
    } catch (error) {
      console.error('[PublicInterviewService] Error submitting answer:', error);
      throw error;
    }
  }
};

