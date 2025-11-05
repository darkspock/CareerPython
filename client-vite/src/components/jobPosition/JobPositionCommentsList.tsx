/**
 * Job Position Comments List Component
 * 
 * Displays a list of comments for a job position with filtering and actions.
 */

import React from 'react';
import { Trash2, CheckCircle, Clock, MessageSquare } from 'lucide-react';
import type { JobPositionComment } from '@/types/jobPositionComment';
// Using basic date formatting
const formatDate = (dateStr: string) => {
  const date = new Date(dateStr);
  return date.toLocaleString('es-ES', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  });
};

interface JobPositionCommentsListProps {
  comments: JobPositionComment[];
  onDelete?: (commentId: string) => void;
  onToggleReviewStatus?: (commentId: string) => void;
  isLoading?: boolean;
}

export const JobPositionCommentsList: React.FC<JobPositionCommentsListProps> = ({
  comments,
  onDelete,
  onToggleReviewStatus,
  isLoading = false,
}) => {
  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (comments.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        <MessageSquare className="mx-auto h-12 w-12 text-gray-400 mb-3" />
        <p>No hay comentarios todavía</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {comments.map((comment) => (
        <div
          key={comment.id}
          className={`bg-white border rounded-lg p-4 ${
            comment.review_status === 'pending' ? 'border-yellow-300 bg-yellow-50' : 'border-gray-200'
          }`}
        >
          <div className="flex items-start justify-between">
            <div className="flex-1">
              {/* Header */}
              <div className="flex items-center gap-2 mb-2">
                {comment.is_global && (
                  <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-purple-100 text-purple-800">
                    Global
                  </span>
                )}
                {comment.review_status === 'pending' && (
                  <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-yellow-100 text-yellow-800">
                    Pendiente de revisión
                  </span>
                )}
                {comment.visibility === 'shared' && (
                  <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-800">
                    Compartido
                  </span>
                )}
              </div>

              {/* Comment text */}
              <p className="text-gray-900 whitespace-pre-wrap mb-2">{comment.comment}</p>

              {/* Footer */}
              <div className="flex items-center gap-4 text-xs text-gray-500">
                <span>{formatDate(comment.created_at)}</span>
                {comment.created_at !== comment.updated_at && (
                  <span className="italic">(editado)</span>
                )}
              </div>
            </div>

            {/* Actions */}
            <div className="flex items-center gap-2 ml-4">
              {onToggleReviewStatus && (
                <button
                  onClick={() => onToggleReviewStatus(comment.id)}
                  className={`p-1.5 rounded transition-colors ${
                    comment.review_status === 'pending'
                      ? 'text-yellow-600 hover:bg-yellow-100'
                      : 'text-gray-400 hover:bg-gray-100'
                  }`}
                  title={comment.review_status === 'pending' ? 'Marcar como revisado' : 'Marcar como pendiente'}
                >
                  {comment.review_status === 'pending' ? (
                    <CheckCircle className="h-4 w-4" />
                  ) : (
                    <Clock className="h-4 w-4" />
                  )}
                </button>
              )}
              {onDelete && (
                <button
                  onClick={() => onDelete(comment.id)}
                  className="p-1.5 text-red-600 hover:bg-red-50 rounded transition-colors"
                  title="Eliminar comentario"
                >
                  <Trash2 className="h-4 w-4" />
                </button>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

