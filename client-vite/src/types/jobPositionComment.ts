/**
 * Job Position Comment Types
 * 
 * Types for comments on job positions, including global and stage-specific comments.
 */

export const CommentReviewStatus = {
  PENDING: 'pending',
  REVIEWED: 'reviewed',
} as const;

export type CommentReviewStatus = typeof CommentReviewStatus[keyof typeof CommentReviewStatus];

export const CommentVisibility = {
  PRIVATE: 'private',
  SHARED: 'shared',
} as const;

export type CommentVisibility = typeof CommentVisibility[keyof typeof CommentVisibility];

export interface JobPositionComment {
  id: string;
  job_position_id: string;
  comment: string;
  workflow_id: string | null;
  stage_id: string | null; // null = global comment (visible at all stages)
  created_by_user_id: string;
  review_status: CommentReviewStatus;
  visibility: CommentVisibility;
  created_at: string; // ISO datetime string
  updated_at: string; // ISO datetime string
  is_global: boolean;
}

export interface CreateJobPositionCommentRequest {
  comment: string;
  workflow_id?: string | null;
  stage_id?: string | null;
  visibility?: CommentVisibility;
  review_status?: CommentReviewStatus;
}

export interface UpdateJobPositionCommentRequest {
  comment?: string;
  visibility?: CommentVisibility;
}

export interface JobPositionCommentListResponse {
  comments: JobPositionComment[];
  total: number;
}

