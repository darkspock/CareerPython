/**
 * Candidate Comments Section
 * 
 * Adapter component that uses the generic CommentsSection
 * with candidate-specific logic and services.
 */

import React from 'react';
import { CommentsSection, type CommentTab, type CommentFormData } from '../shared/comments';
import { candidateCommentService } from '../../services/candidateCommentService';
import type { CandidateComment } from '../../types/candidateComment';

interface CandidateCommentsSectionProps {
  companyCandidateId: string;
  stageId: string | null;
  currentWorkflowId?: string | null;
  onCommentChange?: () => void;
  defaultExpanded?: boolean;
  onNavigateToCommentsTab?: () => void;
}

export default function CandidateCommentsSection({
  companyCandidateId,
  stageId,
  currentWorkflowId,
  onCommentChange,
  defaultExpanded = false,
  onNavigateToCommentsTab,
}: CandidateCommentsSectionProps) {
  // Load comments based on tab
  const loadComments = async (tab: CommentTab): Promise<CandidateComment[]> => {
    switch (tab) {
      case 'current':
        if (!stageId) return [];
        return await candidateCommentService.getCommentsByStage(companyCandidateId, stageId);
      case 'global':
        // For candidates, "global" means all comments across all stages
        return await candidateCommentService.getCommentsByCompanyCandidate(companyCandidateId);
      case 'all':
        return await candidateCommentService.getCommentsByCompanyCandidate(companyCandidateId);
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

  if (!stageId) {
    return null; // Don't show if no stage is assigned
  }

  return (
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
      title="Comentarios"
      emptyMessage="No hay comentarios todavía"
      placeholder="Escribe un comentario..."
      defaultExpanded={defaultExpanded}
      onNavigateToCommentsTab={onNavigateToCommentsTab}
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
  );
}

