import { ApiClient } from '../lib/api';
import type { CandidateReview, CreateReviewRequest, UpdateReviewRequest } from '../types/candidateReview';

export class CandidateReviewService {
  /**
   * Create a new review for a candidate
   */
  static async createReview(
    companyCandidateId: string,
    data: CreateReviewRequest
  ): Promise<CandidateReview> {
    return await ApiClient.authenticatedRequest<CandidateReview>(
      `/api/company/candidates/${companyCandidateId}/reviews`,
      {
        method: 'POST',
        body: JSON.stringify(data),
      }
    );
  }

  /**
   * Get all reviews for a candidate
   */
  static async getReviewsByCandidate(companyCandidateId: string): Promise<CandidateReview[]> {
    return await ApiClient.authenticatedRequest<CandidateReview[]>(
      `/api/company/candidates/${companyCandidateId}/reviews`
    );
  }

  /**
   * Get reviews for a candidate in a specific stage
   */
  static async getReviewsByStage(
    companyCandidateId: string,
    stageId: string
  ): Promise<CandidateReview[]> {
    return await ApiClient.authenticatedRequest<CandidateReview[]>(
      `/api/company/candidates/${companyCandidateId}/reviews/stage/${stageId}`
    );
  }

  /**
   * Get global reviews for a candidate
   */
  static async getGlobalReviews(companyCandidateId: string): Promise<CandidateReview[]> {
    return await ApiClient.authenticatedRequest<CandidateReview[]>(
      `/api/company/candidates/${companyCandidateId}/reviews/global`
    );
  }

  /**
   * Get a review by ID
   */
  static async getReviewById(reviewId: string): Promise<CandidateReview> {
    return await ApiClient.authenticatedRequest<CandidateReview>(
      `/api/company/candidates/reviews/${reviewId}`
    );
  }

  /**
   * Update a review
   */
  static async updateReview(reviewId: string, data: UpdateReviewRequest): Promise<CandidateReview> {
    return await ApiClient.authenticatedRequest<CandidateReview>(
      `/api/company/candidates/reviews/${reviewId}`,
      {
        method: 'PUT',
        body: JSON.stringify(data),
      }
    );
  }

  /**
   * Delete a review
   */
  static async deleteReview(reviewId: string): Promise<void> {
    await ApiClient.authenticatedRequest(`/api/company/candidates/reviews/${reviewId}`, {
      method: 'DELETE',
    });
  }

  /**
   * Mark a review as reviewed
   */
  static async markAsReviewed(reviewId: string): Promise<CandidateReview> {
    return await ApiClient.authenticatedRequest<CandidateReview>(
      `/api/company/candidates/reviews/${reviewId}/mark-reviewed`,
      {
        method: 'POST',
      }
    );
  }

  /**
   * Mark a review as pending
   */
  static async markAsPending(reviewId: string): Promise<CandidateReview> {
    return await ApiClient.authenticatedRequest<CandidateReview>(
      `/api/company/candidates/reviews/${reviewId}/mark-pending`,
      {
        method: 'POST',
      }
    );
  }
}

export const candidateReviewService = CandidateReviewService;

