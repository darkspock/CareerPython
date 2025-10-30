// Candidate Comment types

export type CommentReviewStatus = 'reviewed' | 'pending';
export type CommentVisibility = 'private' | 'shared_with_candidate';

export interface CandidateComment {
  id: string;
  company_candidate_id: string;
  comment: string;
  workflow_id: string | null;
  stage_id: string | null;
  created_by_user_id: string;
  review_status: CommentReviewStatus;
  visibility: CommentVisibility;
  created_at: string;
  updated_at: string;
  // Expanded data (optional, may be populated by API)
  workflow_name?: string;
  stage_name?: string;
  created_by_user_name?: string;
  created_by_user_email?: string;
}

export interface CreateCandidateCommentRequest {
  comment: string;
  workflow_id?: string;
  stage_id?: string;
  visibility?: CommentVisibility;
  review_status?: CommentReviewStatus;
}

export interface UpdateCandidateCommentRequest {
  comment?: string;
  visibility?: CommentVisibility;
}

