import { ApiClient } from '../lib/api';
import type {
  CandidateComment,
  CreateCandidateCommentRequest,
  UpdateCandidateCommentRequest
} from '../types/candidateComment';

class CandidateCommentService {
  private baseUrl = '/api/company/candidates';

  /**
   * Create a new comment for a candidate
   */
  async createComment(
    companyCandidateId: string,
    data: CreateCandidateCommentRequest
  ): Promise<CandidateComment> {
    return ApiClient.authenticatedRequest<CandidateComment>(
      `${this.baseUrl}/${companyCandidateId}/comments`,
      {
        method: 'POST',
        body: JSON.stringify(data),
      }
    );
  }

  /**
   * Get all comments for a company candidate
   */
  async getCommentsByCompanyCandidate(companyCandidateId: string): Promise<CandidateComment[]> {
    return ApiClient.authenticatedRequest<CandidateComment[]>(
      `${this.baseUrl}/${companyCandidateId}/comments`
    );
  }

  /**
   * Get all comments for a company candidate in a specific stage
   */
  async getCommentsByStage(
    companyCandidateId: string,
    stageId: string
  ): Promise<CandidateComment[]> {
    return ApiClient.authenticatedRequest<CandidateComment[]>(
      `${this.baseUrl}/${companyCandidateId}/comments/stage/${stageId}`
    );
  }

  /**
   * Count pending comments for a company candidate
   */
  async countPendingComments(companyCandidateId: string): Promise<number> {
    return ApiClient.authenticatedRequest<number>(
      `${this.baseUrl}/${companyCandidateId}/comments/pending/count`
    );
  }

  /**
   * Get a comment by ID
   */
  async getCommentById(commentId: string): Promise<CandidateComment> {
    return ApiClient.authenticatedRequest<CandidateComment>(
      `${this.baseUrl}/comments/${commentId}`
    );
  }

  /**
   * Update a comment
   */
  async updateComment(
    commentId: string,
    data: UpdateCandidateCommentRequest
  ): Promise<CandidateComment> {
    return ApiClient.authenticatedRequest<CandidateComment>(
      `${this.baseUrl}/comments/${commentId}`,
      {
        method: 'PUT',
        body: JSON.stringify(data),
      }
    );
  }

  /**
   * Delete a comment
   */
  async deleteComment(commentId: string): Promise<void> {
    await ApiClient.authenticatedRequest(`${this.baseUrl}/comments/${commentId}`, {
      method: 'DELETE',
    });
  }

  /**
   * Mark a comment as pending review
   */
  async markAsPending(commentId: string): Promise<CandidateComment> {
    return ApiClient.authenticatedRequest<CandidateComment>(
      `${this.baseUrl}/comments/${commentId}/mark-pending`,
      {
        method: 'POST',
      }
    );
  }

  /**
   * Mark a comment as reviewed
   */
  async markAsReviewed(commentId: string): Promise<CandidateComment> {
    return ApiClient.authenticatedRequest<CandidateComment>(
      `${this.baseUrl}/comments/${commentId}/mark-reviewed`,
      {
        method: 'POST',
      }
    );
  }
}

export const candidateCommentService = new CandidateCommentService();

