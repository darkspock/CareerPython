export interface CandidateReview {
  id: string;
  company_candidate_id: string;
  score: number; // 0, 3, 6, 10
  comment: string | null;
  workflow_id: string | null;
  stage_id: string | null;
  review_status: 'pending' | 'reviewed';
  created_by_user_id: string;
  created_at: string;
  updated_at: string;
  // Expanded data (optional)
  workflow_name?: string | null;
  stage_name?: string | null;
  created_by_user_name?: string | null;
  created_by_user_email?: string | null;
}

export interface CreateReviewRequest {
  score: number; // 0, 3, 6, 10
  comment?: string | null;
  workflow_id?: string | null;
  stage_id?: string | null;
  review_status?: 'pending' | 'reviewed';
}

export interface UpdateReviewRequest {
  score?: number; // 0, 3, 6, 10
  comment?: string | null;
}

export type ReviewScore = 0 | 3 | 6 | 10;

