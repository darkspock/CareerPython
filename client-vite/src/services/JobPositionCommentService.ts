/**
 * Job Position Comment Service
 * 
 * Service for managing comments on job positions.
 */

import { ApiClient } from '../lib/api';
import type {
  JobPositionComment,
  JobPositionCommentListResponse,
  CreateJobPositionCommentRequest,
  UpdateJobPositionCommentRequest,
} from '../types/jobPositionComment';

class JobPositionCommentService {
  /**
   * Get the company slug from localStorage
   */
  private getCompanySlug(): string {
    const slug = localStorage.getItem('company_slug');
    if (!slug) {
      throw new Error('Company slug not found. Please log in again.');
    }
    return slug;
  }

  /**
   * Get the base URL for position endpoints (company-scoped)
   */
  private getBaseUrl(): string {
    return `/${this.getCompanySlug()}/admin/positions`;
  }

  /**
   * Create a new comment for a job position
   */
  async createComment(
    positionId: string,
    data: CreateJobPositionCommentRequest
  ): Promise<void> {
    await ApiClient.authenticatedRequest(
      `${this.getBaseUrl()}/${positionId}/comments`,
      {
        method: 'POST',
        body: JSON.stringify(data),
      }
    );
  }

  /**
   * List comments for a job position
   * 
   * @param positionId - ID of the job position
   * @param stageId - Optional stage ID to filter by (null = only global comments)
   * @param includeGlobal - Include global comments (default: true)
   */
  async listComments(
    positionId: string,
    stageId?: string | null,
    includeGlobal: boolean = true
  ): Promise<JobPositionCommentListResponse> {
    const params = new URLSearchParams();
    
    if (stageId !== undefined) {
      if (stageId === null) {
        params.append('stage_id', 'null');
      } else {
        params.append('stage_id', stageId);
      }
    }
    
    params.append('include_global', includeGlobal.toString());

    return ApiClient.authenticatedRequest<JobPositionCommentListResponse>(
      `${this.getBaseUrl()}/${positionId}/comments?${params.toString()}`,
      { method: 'GET' }
    );
  }

  /**
   * Update an existing comment
   */
  async updateComment(
    commentId: string,
    data: UpdateJobPositionCommentRequest
  ): Promise<void> {
    await ApiClient.authenticatedRequest(
      `${this.getBaseUrl()}/comments/${commentId}`,
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
    await ApiClient.authenticatedRequest(
      `${this.getBaseUrl()}/comments/${commentId}`,
      { method: 'DELETE' }
    );
  }

  /**
   * Mark a comment as reviewed
   */
  async markCommentAsReviewed(commentId: string): Promise<void> {
    await ApiClient.authenticatedRequest(
      `${this.getBaseUrl()}/comments/${commentId}/mark-reviewed`,
      { method: 'POST' }
    );
  }

  /**
   * Mark a comment as pending
   */
  async markCommentAsPending(commentId: string): Promise<void> {
    await ApiClient.authenticatedRequest(
      `${this.getBaseUrl()}/comments/${commentId}/mark-pending`,
      { method: 'POST' }
    );
  }

  /**
   * Get comments for current stage + global comments
   * This is the most common use case for displaying "current comments"
   */
  async getCurrentStageComments(
    positionId: string,
    currentStageId: string
  ): Promise<JobPositionComment[]> {
    const response = await this.listComments(positionId, currentStageId, true);
    return response.comments;
  }

  /**
   * Get only global comments (visible at all stages)
   */
  async getGlobalComments(positionId: string): Promise<JobPositionComment[]> {
    const response = await this.listComments(positionId, null, true);
    return response.comments;
  }

  /**
   * Get all comments for a position (regardless of stage)
   * This makes a direct API call to get ALL comments without stage filtering
   */
  async getAllComments(positionId: string): Promise<JobPositionComment[]> {
    return ApiClient.authenticatedRequest<JobPositionComment[]>(
      `${this.getBaseUrl()}/${positionId}/comments/all`,
      { method: 'GET' }
    );
  }

  /**
   * Count pending comments for a position
   */
  countPendingComments(comments: JobPositionComment[]): number {
    return comments.filter(comment => comment.review_status === 'pending').length;
  }

  /**
   * Filter comments by stage
   */
  filterByStage(comments: JobPositionComment[], stageId: string): JobPositionComment[] {
    return comments.filter(comment => comment.stage_id === stageId);
  }

  /**
   * Get global comments from a list
   */
  getGlobalCommentsFromList(comments: JobPositionComment[]): JobPositionComment[] {
    return comments.filter(comment => comment.is_global);
  }
}

export default new JobPositionCommentService();

