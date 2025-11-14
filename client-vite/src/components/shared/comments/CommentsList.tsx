/**
 * Generic Comments List Component
 * 
 * Reusable list component for displaying comments with:
 * - Review status indicators
 * - Visibility badges
 * - Global comment indicators
 * - Actions (toggle review, delete)
 */

// import React from 'react';
import { Trash2, CheckCircle, Clock, MessageSquare, Globe, Eye, EyeOff } from 'lucide-react';

export interface BaseComment {
  id: string;
  comment: string;
  review_status: 'pending' | 'reviewed';
  visibility: 'private' | 'shared' | 'shared_with_candidate';
  created_at: string;
  updated_at: string;
  created_by_user_id: string;
  created_by_user_name?: string;
  created_by_user_email?: string;
  is_global?: boolean;
  workflow_name?: string;
  stage_name?: string;
  workflow_id?: string | null;
  stage_id?: string | null;
}

interface CommentsListProps<T extends BaseComment> {
  comments: T[];
  onDelete?: (commentId: string) => void;
  onToggleReviewStatus?: (commentId: string) => void;
  isLoading?: boolean;
  emptyMessage?: string;
  showWorkflowInfo?: boolean;
  showStageInfo?: boolean;
  showAuthorInfo?: boolean;
  formatDate?: (dateStr: string) => string;
}

const defaultFormatDate = (dateStr: string) => {
  const date = new Date(dateStr);
  return date.toLocaleString('es-ES', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  });
};

export function CommentsList<T extends BaseComment>({
  comments,
  onDelete,
  onToggleReviewStatus,
  isLoading = false,
  emptyMessage = 'No hay comentarios todavía',
  showWorkflowInfo = false,
  showStageInfo = false,
  showAuthorInfo = true,
  formatDate = defaultFormatDate,
}: CommentsListProps<T>) {
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
        <p>{emptyMessage}</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {comments.map((comment) => (
        <div
          key={comment.id}
          className={`bg-white border rounded-lg p-4 ${
            comment.review_status === 'pending' 
              ? 'border-yellow-300 bg-yellow-50' 
              : 'border-gray-200'
          }`}
        >
          <div className="flex items-start justify-between">
            <div className="flex-1">
              {/* Header with badges */}
              <div className="flex items-center gap-2 mb-2 flex-wrap">
                {comment.is_global && (
                  <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-medium bg-purple-100 text-purple-800">
                    <Globe className="h-3 w-3" />
                    Global
                  </span>
                )}
                {comment.review_status === 'pending' && (
                  <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-medium bg-yellow-100 text-yellow-800">
                    <Clock className="h-3 w-3" />
                    Pendiente de revisión
                  </span>
                )}
                {comment.visibility === 'shared' && (
                  <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-800">
                    <Eye className="h-3 w-3" />
                    Compartido
                  </span>
                )}
                {comment.visibility === 'shared_with_candidate' && (
                  <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-medium bg-green-100 text-green-800">
                    <Eye className="h-3 w-3" />
                    Compartido con candidato
                  </span>
                )}
                {comment.visibility === 'private' && (
                  <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800">
                    <EyeOff className="h-3 w-3" />
                    Privado
                  </span>
                )}
                {showWorkflowInfo && comment.workflow_name && (
                  <span className="px-2 py-0.5 bg-blue-100 text-blue-800 rounded-full text-xs">
                    {comment.workflow_name}
                  </span>
                )}
                {showStageInfo && comment.stage_name && (
                  <span className="px-2 py-0.5 bg-gray-100 text-gray-800 rounded-full text-xs">
                    {comment.stage_name}
                  </span>
                )}
              </div>

              {/* Comment text */}
              <p className="text-gray-900 whitespace-pre-wrap mb-2">{comment.comment}</p>

              {/* Footer */}
              <div className="flex items-center gap-4 text-xs text-gray-500 flex-wrap">
                <span>{formatDate(comment.created_at)}</span>
                {comment.created_at !== comment.updated_at && (
                  <span className="italic">(editado)</span>
                )}
                {showAuthorInfo && comment.created_by_user_name && (
                  <span>por {comment.created_by_user_name}</span>
                )}
                {showAuthorInfo && !comment.created_by_user_name && comment.created_by_user_id && (
                  <span>por usuario {comment.created_by_user_id.slice(0, 8)}</span>
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
}

