import { ApiClient } from '../lib/api';
import type { CandidateReview, CreateReviewRequest, UpdateReviewRequest } from '../types/candidateReview';

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

/**
 * Get the base path for candidate endpoints (company-scoped)
 */
function getCandidatesBasePath(): string {
  return `/${getCompanySlug()}/admin/candidates`;
}

export class CandidateReviewService {
  /**
   * Create a new review for a candidate
   */
  static async createReview(
    companyCandidateId: string,
    data: CreateReviewRequest
  ): Promise<CandidateReview> {
    return await ApiClient.authenticatedRequest<CandidateReview>(
      `${getCandidatesBasePath()}/${companyCandidateId}/reviews`,
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
      `${getCandidatesBasePath()}/${companyCandidateId}/reviews`
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
      `${getCandidatesBasePath()}/${companyCandidateId}/reviews/stage/${stageId}`
    );
  }

  /**
   * Get global reviews for a candidate
   */
  static async getGlobalReviews(companyCandidateId: string): Promise<CandidateReview[]> {
    return await ApiClient.authenticatedRequest<CandidateReview[]>(
      `${getCandidatesBasePath()}/${companyCandidateId}/reviews/global`
    );
  }

  /**
   * Get a review by ID
   */
  static async getReviewById(reviewId: string): Promise<CandidateReview> {
    return await ApiClient.authenticatedRequest<CandidateReview>(
      `${getCandidatesBasePath()}/reviews/${reviewId}`
    );
  }

  /**
   * Update a review
   */
  static async updateReview(reviewId: string, data: UpdateReviewRequest): Promise<CandidateReview> {
    return await ApiClient.authenticatedRequest<CandidateReview>(
      `${getCandidatesBasePath()}/reviews/${reviewId}`,
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
    await ApiClient.authenticatedRequest(`${getCandidatesBasePath()}/reviews/${reviewId}`, {
      method: 'DELETE',
    });
  }

  /**
   * Mark a review as reviewed
   */
  static async markAsReviewed(reviewId: string): Promise<CandidateReview> {
    return await ApiClient.authenticatedRequest<CandidateReview>(
      `${getCandidatesBasePath()}/reviews/${reviewId}/mark-reviewed`,
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
      `${getCandidatesBasePath()}/reviews/${reviewId}/mark-pending`,
      {
        method: 'POST',
      }
    );
  }
}

export const candidateReviewService = CandidateReviewService;

