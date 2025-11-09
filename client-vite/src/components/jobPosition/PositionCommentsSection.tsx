/**
 * Job Position Comments Section
 * 
 * Adapter component that uses the generic CommentsSection
 * with job position-specific logic and services.
 */

import React from 'react';
import { CommentsSection, type CommentTab, type CommentFormData } from '../shared/comments';
import JobPositionCommentService from '../../services/JobPositionCommentService';
import type { JobPositionComment } from '../../types/jobPositionComment';

interface PositionCommentsSectionProps {
  positionId: string;
  workflowId?: string;
  currentStageId?: string;
  onCommentsChange?: () => void;
}

export function PositionCommentsSection({
  positionId,
  workflowId,
  currentStageId,
  onCommentsChange,
}: PositionCommentsSectionProps) {
  // Load comments based on tab
  const loadComments = async (tab: CommentTab): Promise<JobPositionComment[]> => {
    switch (tab) {
      case 'current':
        return currentStageId
          ? await JobPositionCommentService.getCurrentStageComments(positionId, currentStageId)
          : await JobPositionCommentService.getGlobalComments(positionId);
      case 'global':
        return await JobPositionCommentService.getGlobalComments(positionId);
      case 'all':
        return await JobPositionCommentService.getAllComments(positionId);
      default:
        return [];
    }
  };

  // Create comment
  const handleCreateComment = async (data: CommentFormData): Promise<void> => {
    await JobPositionCommentService.createComment(positionId, {
      comment: data.comment,
      workflow_id: workflowId || null,
      stage_id: data.is_global ? null : (currentStageId || null),
      visibility: data.visibility === 'shared' ? 'shared' : 'private',
      review_status: data.review_status,
    });
  };

  // Delete comment
  const handleDeleteComment = async (commentId: string): Promise<void> => {
    await JobPositionCommentService.deleteComment(commentId);
  };

  // Toggle review status
  const handleToggleReviewStatus = async (commentId: string): Promise<void> => {
    // We need to check current status first - load all comments to find it
    const allComments = await JobPositionCommentService.getAllComments(positionId);
    const comment = allComments.find(c => c.id === commentId);
    if (!comment) return;

    if (comment.review_status === 'pending') {
      await JobPositionCommentService.markCommentAsReviewed(commentId);
    } else {
      await JobPositionCommentService.markCommentAsPending(commentId);
    }
  };

  return (
    <CommentsSection<JobPositionComment>
      loadComments={loadComments}
      onCreateComment={handleCreateComment}
      onDeleteComment={handleDeleteComment}
      onToggleReviewStatus={handleToggleReviewStatus}
      currentStageId={currentStageId || null}
      workflowId={workflowId || null}
      showGlobalTab={true}
      showAllTab={true}
      showWorkflowInfo={false}
      showStageInfo={false}
      showAuthorInfo={true}
      onCommentsChange={onCommentsChange}
      title="Comentarios de la posición"
      emptyMessage="No hay comentarios todavía"
      placeholder="Escribe un comentario..."
    />
  );
}

