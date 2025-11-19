/**
 * Candidate Comments Section
 * 
 * Adapter component that uses the generic CommentsSection
 * with candidate-specific logic and services.
 * Now includes toggle between Comments and Reviews.
 */

import { useState } from 'react';
import { CommentsSection, type CommentTab, type CommentFormData } from '../shared/comments';
import ReviewForm from './ReviewForm';
import { candidateCommentService } from '../../services/candidateCommentService';
import { candidateReviewService } from '../../services/candidateReviewService';
import type { CandidateComment } from '../../types/candidateComment';
import type { ReviewScore } from '../../types/candidateReview';

interface CandidateCommentsSectionProps {
  companyCandidateId: string;
  stageId: string | null;
  currentWorkflowId?: string | null;
  onCommentChange?: () => void;
  onReviewChange?: () => void;
  defaultExpanded?: boolean;
  onNavigateToCommentsTab?: () => void;
  refreshKey?: number;
}

export default function CandidateCommentsSection({
  companyCandidateId,
  stageId,
  currentWorkflowId,
  onCommentChange,
  onReviewChange,
  defaultExpanded = false,
  onNavigateToCommentsTab,
  refreshKey,
}: CandidateCommentsSectionProps) {
  const [mode, setMode] = useState<'comments' | 'reviews'>('comments');
  const [isSubmittingReview, setIsSubmittingReview] = useState(false);
  // Load comments based on tab
  const loadComments = async (tab: CommentTab): Promise<CandidateComment[]> => {
    // Always fetch all comments from backend
    const allComments = await candidateCommentService.getCommentsByCompanyCandidate(companyCandidateId);

    // Filter on frontend based on tab
    switch (tab) {
      case 'current':
        // Show only comments for current stage
        if (!stageId) return [];
        return allComments.filter(comment => comment.stage_id === stageId);
      case 'global':
        // Show only global comments (without stage_id)
        return allComments.filter(comment => comment.stage_id === null || comment.stage_id === undefined);
      case 'all':
        // Show all comments
        return allComments;
      default:
        return [];
    }
  };

  // Create comment
  const handleCreateComment = async (data: CommentFormData): Promise<void> => {
    await candidateCommentService.createComment(companyCandidateId, {
      comment: data.comment,
      stage_id: data.is_global ? undefined : stageId || undefined,
      workflow_id: currentWorkflowId || undefined,
      visibility: data.visibility === 'shared' ? 'shared_with_candidate' : 'private',
      review_status: data.review_status,
    });
  };

  // Delete comment
  const handleDeleteComment = async (commentId: string): Promise<void> => {
    await candidateCommentService.deleteComment(commentId);
  };

  // Toggle review status
  const handleToggleReviewStatus = async (commentId: string): Promise<void> => {
    // We need to check current status first
    const comment = await candidateCommentService.getCommentById(commentId);
    if (comment.review_status === 'pending') {
      await candidateCommentService.markAsReviewed(commentId);
    } else {
      await candidateCommentService.markAsPending(commentId);
    }
  };

  // Create review
  const handleCreateReview = async (score: ReviewScore, comment?: string | null, isGlobal?: boolean): Promise<void> => {
    setIsSubmittingReview(true);
    try {
      await candidateReviewService.createReview(companyCandidateId, {
        score,
        comment: comment || null,
        workflow_id: currentWorkflowId || null,
        stage_id: isGlobal ? null : (stageId || null),
        review_status: 'reviewed',
      });
      onCommentChange?.();
      onReviewChange?.(); // Also notify that a review was created
    } catch (error) {
      console.error('Error creating review:', error);
      throw error;
    } finally {
      setIsSubmittingReview(false);
    }
  };

  if (!stageId) {
    return null; // Don't show if no stage is assigned
  }

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      {/* Header with toggle */}
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
          <span className="flex items-center gap-1">
            <button
              onClick={() => setMode('comments')}
              className={`transition-colors ${
                mode === 'comments'
                  ? 'text-blue-600 font-semibold'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              Comentarios
            </button>
            <span className="text-gray-400">/</span>
            <button
              onClick={() => setMode('reviews')}
              className={`transition-colors ${
                mode === 'reviews'
                  ? 'text-pink-600 font-semibold'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              Reviews
            </button>
          </span>
        </h3>
      </div>

      {/* Show comment form when in comments mode */}
      {mode === 'comments' && (
        <CommentsSection<CandidateComment>
          loadComments={loadComments}
          onCreateComment={handleCreateComment}
          onDeleteComment={handleDeleteComment}
          onToggleReviewStatus={handleToggleReviewStatus}
          currentStageId={stageId}
          workflowId={currentWorkflowId || undefined}
          showGlobalTab={true}
          showAllTab={true}
          showWorkflowInfo={true}
          showStageInfo={true}
          showAuthorInfo={true}
          onCommentsChange={onCommentChange}
          title=""
          emptyMessage="No hay comentarios todavía"
          placeholder="Escribe un comentario..."
          defaultExpanded={defaultExpanded}
          onNavigateToCommentsTab={onNavigateToCommentsTab}
          refreshKey={refreshKey}
          formatDate={(dateStr) => {
            return new Date(dateStr).toLocaleDateString('en-US', {
              year: 'numeric',
              month: 'short',
              day: 'numeric',
              hour: '2-digit',
              minute: '2-digit',
            });
          }}
        />
      )}

      {/* Show review form when in reviews mode */}
      {mode === 'reviews' && (
        <div>
          <ReviewForm
            onSubmit={handleCreateReview}
            isSubmitting={isSubmittingReview}
            showCommentField={true}
            showGlobalOption={true}
          />
        </div>
      )}
    </div>
  );
}

