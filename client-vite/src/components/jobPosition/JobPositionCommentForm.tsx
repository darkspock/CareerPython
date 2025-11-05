/**
 * Job Position Comment Form Component
 * 
 * Form for creating new comments on a job position.
 */

import React, { useState } from 'react';
import { Send } from 'lucide-react';
import { CommentVisibility, CommentReviewStatus } from '@/types/jobPositionComment';

interface JobPositionCommentFormProps {
  onSubmit: (data: {
    comment: string;
    workflow_id?: string | null;
    stage_id?: string | null;
    visibility: CommentVisibility;
    review_status: CommentReviewStatus;
  }) => Promise<void>;
  workflowId?: string | null;
  currentStageId?: string | null;
  isGlobalComment?: boolean;
  isSubmitting?: boolean;
}

export const JobPositionCommentForm: React.FC<JobPositionCommentFormProps> = ({
  onSubmit,
  workflowId,
  currentStageId,
  isGlobalComment = false,
  isSubmitting = false,
}) => {
  const [comment, setComment] = useState('');
  const [visibility, setVisibility] = useState<CommentVisibility>(CommentVisibility.SHARED);
  const [isReviewed, setIsReviewed] = useState(true);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!comment.trim()) {
      return;
    }

    await onSubmit({
      comment: comment.trim(),
      workflow_id: workflowId,
      stage_id: isGlobalComment ? null : currentStageId,
      visibility,
      review_status: isReviewed ? CommentReviewStatus.REVIEWED : CommentReviewStatus.PENDING,
    });

    // Reset form
    setComment('');
    setVisibility(CommentVisibility.SHARED);
    setIsReviewed(true);
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white border border-gray-200 rounded-lg p-4">
      {/* Comment textarea */}
      <div className="mb-3">
        <textarea
          value={comment}
          onChange={(e) => setComment(e.target.value)}
          placeholder={
            isGlobalComment
              ? 'Escribe un comentario global (visible en todas las etapas)...'
              : 'Escribe un comentario...'
          }
          rows={3}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
          disabled={isSubmitting}
        />
      </div>

      {/* Options */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          {/* Visibility toggle */}
          <label className="flex items-center gap-2 text-sm">
            <input
              type="checkbox"
              checked={visibility === CommentVisibility.SHARED}
              onChange={(e) =>
                setVisibility(
                  e.target.checked ? CommentVisibility.SHARED : CommentVisibility.PRIVATE
                )
              }
              className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              disabled={isSubmitting}
            />
            <span className="text-gray-700">Compartir con equipo</span>
          </label>

          {/* Reviewed toggle */}
          <label className="flex items-center gap-2 text-sm">
            <input
              type="checkbox"
              checked={isReviewed}
              onChange={(e) => setIsReviewed(e.target.checked)}
              className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              disabled={isSubmitting}
            />
            <span className="text-gray-700">Marcar como revisado</span>
          </label>

          {isGlobalComment && (
            <span className="text-xs text-purple-600 font-medium">
              📌 Comentario global
            </span>
          )}
        </div>

        {/* Submit button */}
        <button
          type="submit"
          disabled={!comment.trim() || isSubmitting}
          className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
        >
          {isSubmitting ? (
            <>
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
              <span>Guardando...</span>
            </>
          ) : (
            <>
              <Send className="h-4 w-4" />
              <span>Comentar</span>
            </>
          )}
        </button>
      </div>
    </form>
  );
};

