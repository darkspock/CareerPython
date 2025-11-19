/**
 * Review Form Component
 * 
 * Form for creating/updating a candidate review with score and optional comment
 */

import React, { useState } from 'react';
import { Send, Loader2, Globe } from 'lucide-react';
import ReviewButtons from './ReviewButtons';
import type { ReviewScore } from '@/types/candidateReview.ts';

interface ReviewFormProps {
  onSubmit: (score: ReviewScore, comment?: string | null, isGlobal?: boolean) => Promise<void>;
  isSubmitting?: boolean;
  initialScore?: ReviewScore | null;
  initialComment?: string | null;
  placeholder?: string;
  showCommentField?: boolean;
  showGlobalOption?: boolean;
}

export default function ReviewForm({
  onSubmit,
  isSubmitting = false,
  initialScore = null,
  initialComment = null,
  placeholder = 'Agregar comentario (opcional)...',
  showCommentField = true,
  showGlobalOption = false,
}: ReviewFormProps) {
  const [score, setScore] = useState<ReviewScore | null>(initialScore);
  const [comment, setComment] = useState<string>(initialComment || '');
  const [isGlobal, setIsGlobal] = useState<boolean>(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (score === null) {
      return; // Score is required
    }

    try {
      await onSubmit(score, comment.trim() || null, isGlobal);
      // Reset form after successful submission (if creating new)
      if (!initialScore) {
        setScore(null);
        setComment('');
        setIsGlobal(false);
      }
    } catch (error) {
      console.error('Error submitting review:', error);
      // Error handling is done by parent component
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Puntuación
        </label>
        <ReviewButtons
          onScoreSelect={setScore}
          currentScore={score}
          disabled={isSubmitting}
        />
      </div>

      {showCommentField && (
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Comentario (opcional)
          </label>
          <textarea
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            placeholder={placeholder}
            rows={3}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none"
            disabled={isSubmitting}
          />
        </div>
      )}

      {showGlobalOption && (
        <div>
          <label className="flex items-center gap-2 text-sm text-gray-700 cursor-pointer">
            <input
              type="checkbox"
              checked={isGlobal}
              onChange={(e) => setIsGlobal(e.target.checked)}
              className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              disabled={isSubmitting}
            />
            <Globe className="h-4 w-4 text-gray-500" />
            <span>Review global (visible en todas las etapas)</span>
          </label>
        </div>
      )}

      <div className="flex justify-end">
        <button
          type="submit"
          disabled={isSubmitting || score === null}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {isSubmitting ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" />
              <span>Guardando...</span>
            </>
          ) : (
            <>
              <Send className="w-4 h-4" />
              <span>Guardar</span>
            </>
          )}
        </button>
      </div>
    </form>
  );
}

