/**
 * Review Form Component
 *
 * Form for creating/updating a candidate review with score and optional comment
 */

import React, { useState } from 'react';
import { Send, Loader2, Globe } from 'lucide-react';
import ReviewButtons from './ReviewButtons';
import type { ReviewScore } from '@/types/candidateReview.ts';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { Checkbox } from '@/components/ui/checkbox';

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
    } catch {
      // Error handling is done by parent component
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <Label>Puntuación</Label>
        <ReviewButtons
          onScoreSelect={setScore}
          currentScore={score}
          disabled={isSubmitting}
        />
      </div>

      {showCommentField && (
        <div className="space-y-2">
          <Label>Comentario (opcional)</Label>
          <Textarea
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            placeholder={placeholder}
            rows={3}
            className="resize-none"
            disabled={isSubmitting}
          />
        </div>
      )}

      {showGlobalOption && (
        <div className="flex items-center space-x-2">
          <Checkbox
            id="isGlobal"
            checked={isGlobal}
            onCheckedChange={(checked) => setIsGlobal(checked === true)}
            disabled={isSubmitting}
          />
          <label
            htmlFor="isGlobal"
            className="flex items-center gap-2 text-sm text-muted-foreground cursor-pointer"
          >
            <Globe className="h-4 w-4" />
            <span>Review global (visible en todas las etapas)</span>
          </label>
        </div>
      )}

      <div className="flex justify-end">
        <Button
          type="submit"
          disabled={isSubmitting || score === null}
        >
          {isSubmitting ? (
            <>
              <Loader2 className="w-4 h-4 mr-2 animate-spin" />
              <span>Guardando...</span>
            </>
          ) : (
            <>
              <Send className="w-4 h-4 mr-2" />
              <span>Guardar</span>
            </>
          )}
        </Button>
      </div>
    </form>
  );
}
