/**
 * Generic Comment Form Component
 * 
 * Reusable form for creating comments with support for:
 * - Visibility options (private/shared)
 * - Review status (pending/reviewed)
 * - Global comments (for positions)
 * - Stage-specific comments
 */

import React, { useState } from 'react';
import { Send, Loader2 } from 'lucide-react';

export type CommentVisibility = 'private' | 'shared' | 'shared_with_candidate';
export type CommentReviewStatus = 'pending' | 'reviewed';

export interface CommentFormData {
  comment: string;
  visibility: CommentVisibility;
  review_status: CommentReviewStatus;
  is_global?: boolean;
}

interface CommentFormProps {
  onSubmit: (data: CommentFormData) => Promise<void>;
  isSubmitting?: boolean;
  isGlobalComment?: boolean;
  placeholder?: string;
  showVisibilityOption?: boolean;
  showReviewOption?: boolean;
  showGlobalOption?: boolean;
  defaultVisibility?: CommentVisibility;
  defaultReviewStatus?: CommentReviewStatus;
}

export const CommentForm: React.FC<CommentFormProps> = ({
  onSubmit,
  isSubmitting = false,
  isGlobalComment = false,
  placeholder = 'Escribe un comentario...',
  showVisibilityOption = true,
  showReviewOption = true,
  showGlobalOption = false,
  defaultVisibility = 'shared',
  defaultReviewStatus = 'reviewed',
}) => {
  const [comment, setComment] = useState('');
  const [visibility, setVisibility] = useState<CommentVisibility>(defaultVisibility);
  const [isReviewed, setIsReviewed] = useState(defaultReviewStatus === 'reviewed');
  const [isGlobal, setIsGlobal] = useState(isGlobalComment);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!comment.trim()) {
      return;
    }

    await onSubmit({
      comment: comment.trim(),
      visibility,
      review_status: isReviewed ? 'reviewed' : 'pending',
      is_global: showGlobalOption ? isGlobal : undefined,
    });

    // Reset form
    setComment('');
    setVisibility(defaultVisibility);
    setIsReviewed(defaultReviewStatus === 'reviewed');
    if (showGlobalOption) {
      setIsGlobal(isGlobalComment);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white border border-gray-200 rounded-lg p-4">
      {/* Comment textarea */}
      <div className="mb-3">
        <textarea
          value={comment}
          onChange={(e) => setComment(e.target.value)}
          placeholder={
            isGlobal
              ? 'Escribe un comentario global (visible en todas las etapas)...'
              : placeholder
          }
          rows={3}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
          disabled={isSubmitting}
        />
      </div>

      {/* Options */}
      <div className="flex items-center justify-between flex-wrap gap-3">
        <div className="flex items-center gap-4 flex-wrap">
          {/* Visibility toggle */}
          {showVisibilityOption && (
            <label className="flex items-center gap-2 text-sm">
              <input
                type="checkbox"
                checked={visibility === 'shared' || visibility === 'shared_with_candidate'}
                onChange={(e) => {
                  if (visibility === 'shared_with_candidate') {
                    setVisibility(e.target.checked ? 'shared_with_candidate' : 'private');
                  } else {
                    setVisibility(e.target.checked ? 'shared' : 'private');
                  }
                }}
                className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                disabled={isSubmitting}
              />
              <span className="text-gray-700">Compartir con equipo</span>
            </label>
          )}

          {/* Reviewed toggle */}
          {showReviewOption && (
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
          )}

          {/* Global comment indicator */}
          {showGlobalOption && isGlobal && (
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
              <Loader2 className="h-4 w-4 animate-spin" />
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

