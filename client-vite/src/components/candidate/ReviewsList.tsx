/**
 * Reviews List Component
 * 
 * Displays a list of candidate reviews with score indicators
 */

import React from 'react';
import { Ban, ThumbsDown, ThumbsUp, Heart, Clock, CheckCircle, Trash2 } from 'lucide-react';
import type { CandidateReview } from '../../types/candidateReview';

interface ReviewsListProps {
  reviews: CandidateReview[];
  onDelete?: (reviewId: string) => void;
  onToggleReviewStatus?: (reviewId: string) => void;
  isLoading?: boolean;
  showWorkflowInfo?: boolean;
  showStageInfo?: boolean;
  showAuthorInfo?: boolean;
  formatDate?: (dateStr: string) => string;
}

const scoreConfig: Record<number, { icon: React.ReactNode; label: string; color: string; bgColor: string }> = {
  0: {
    icon: <Ban className="w-4 h-4" />,
    label: 'Prohibido',
    color: 'text-red-600',
    bgColor: 'bg-red-50',
  },
  3: {
    icon: <ThumbsDown className="w-4 h-4" />,
    label: 'No recomendado',
    color: 'text-orange-600',
    bgColor: 'bg-orange-50',
  },
  6: {
    icon: <ThumbsUp className="w-4 h-4" />,
    label: 'Recomendado',
    color: 'text-blue-600',
    bgColor: 'bg-blue-50',
  },
  10: {
    icon: <Heart className="w-4 h-4" />,
    label: 'Favorito',
    color: 'text-pink-600',
    bgColor: 'bg-pink-50',
  },
};

export default function ReviewsList({
  reviews,
  onDelete,
  onToggleReviewStatus,
  isLoading = false,
  showWorkflowInfo = false,
  showStageInfo = false,
  showAuthorInfo = true,
  formatDate,
}: ReviewsListProps) {
  const defaultFormatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const formatDateFn = formatDate || defaultFormatDate;

  if (isLoading) {
    return (
      <div className="text-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-2"></div>
        <p className="text-sm text-gray-600">Cargando reviews...</p>
      </div>
    );
  }

  if (reviews.length === 0) {
    return (
      <div className="text-center py-8 border-2 border-dashed border-gray-300 rounded-lg">
        <Heart className="w-12 h-12 text-gray-400 mx-auto mb-4" />
        <p className="text-gray-500 mb-2">No hay reviews todavía</p>
        <p className="text-sm text-gray-400">Sé el primero en puntuar este candidato</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {reviews.map((review) => {
        const config = scoreConfig[review.score as keyof typeof scoreConfig] || scoreConfig[6];

        return (
          <div
            key={review.id}
            className={`p-4 rounded-lg border ${
              review.review_status === 'pending'
                ? 'bg-yellow-50 border-yellow-200'
                : 'bg-white border-gray-200'
            }`}
          >
            <div className="flex items-start justify-between mb-2">
              <div className="flex items-center gap-3 flex-1">
                <div className={`${config.bgColor} ${config.color} p-2 rounded-lg`}>
                  {config.icon}
                </div>
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="font-semibold text-gray-900">Puntuación: {review.score}</span>
                    <span className="text-xs text-gray-500">({config.label})</span>
                  </div>
                  {review.comment && (
                    <p className="text-gray-700 whitespace-pre-wrap mb-2">{review.comment}</p>
                  )}
                  <div className="flex items-center gap-4 text-xs text-gray-500 flex-wrap">
                    <span className="flex items-center gap-1">
                      <Clock className="w-3 h-3" />
                      {formatDateFn(review.created_at)}
                    </span>
                    {showWorkflowInfo && review.workflow_name && (
                      <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded-full">
                        {review.workflow_name}
                      </span>
                    )}
                    {showStageInfo && review.stage_name && (
                      <span className="px-2 py-1 bg-gray-100 text-gray-800 rounded-full">
                        {review.stage_name}
                      </span>
                    )}
                    {showAuthorInfo && review.created_by_user_name && (
                      <span>por {review.created_by_user_name}</span>
                    )}
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-2">
                {onToggleReviewStatus && (
                  <button
                    onClick={() => onToggleReviewStatus(review.id)}
                    className={`p-1.5 rounded transition-colors ${
                      review.review_status === 'pending'
                        ? 'text-yellow-600 hover:bg-yellow-100'
                        : 'text-gray-400 hover:bg-gray-100'
                    }`}
                    title={review.review_status === 'pending' ? 'Marcar como revisado' : 'Marcar como pendiente'}
                  >
                    {review.review_status === 'pending' ? (
                      <CheckCircle className="w-4 h-4" />
                    ) : (
                      <Clock className="w-4 h-4" />
                    )}
                  </button>
                )}
                {onDelete && (
                  <button
                    onClick={() => onDelete(review.id)}
                    className="p-1.5 rounded text-red-600 hover:bg-red-100 transition-colors"
                    title="Eliminar review"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                )}
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}

