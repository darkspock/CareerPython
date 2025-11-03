import { useState, useEffect } from 'react';
import { MessageSquare, Plus, Clock, CheckCircle } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { candidateCommentService } from '../../services/candidateCommentService';
import type { CandidateComment, CreateCandidateCommentRequest } from '../../types/candidateComment';

interface CommentsCardProps {
  companyCandidateId: string;
  stageId: string | null;
  currentWorkflowId?: string | null;
  onCommentChange?: () => void;
}

export default function CommentsCard({ companyCandidateId, stageId, currentWorkflowId, onCommentChange }: CommentsCardProps) {
  const { t } = useTranslation();
  const [comments, setComments] = useState<CandidateComment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showAddForm, setShowAddForm] = useState(false);
  const [newCommentText, setNewCommentText] = useState('');
  const [addingComment, setAddingComment] = useState(false);

  useEffect(() => {
    if (stageId) {
      loadComments();
    }
  }, [companyCandidateId, stageId]);

  const loadComments = async () => {
    if (!stageId) {
      setComments([]);
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      setError(null);
      const data = await candidateCommentService.getCommentsByStage(companyCandidateId, stageId);
      setComments(data || []);
    } catch (err: any) {
      setError(err.message || t('company.candidates.comments.failedToLoad'));
      console.error('Error loading comments:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleAddComment = async () => {
    if (!newCommentText.trim() || !stageId) return;

    try {
      setAddingComment(true);
      setError(null);
      
      const request: CreateCandidateCommentRequest = {
        comment: newCommentText.trim(),
        stage_id: stageId,
        workflow_id: currentWorkflowId || undefined,
        review_status: 'reviewed',
        visibility: 'private',
      };

      await candidateCommentService.createComment(companyCandidateId, request);
      
      setNewCommentText('');
      setShowAddForm(false);
      await loadComments();
      onCommentChange?.(); // Notify parent to refresh all comments
    } catch (err: any) {
      setError(err.message || t('company.candidates.comments.failedToAdd'));
      console.error('Error adding comment:', err);
    } finally {
      setAddingComment(false);
    }
  };

  const handleTogglePending = async (comment: CandidateComment) => {
    try {
      if (comment.review_status === 'pending') {
        await candidateCommentService.markAsReviewed(comment.id);
      } else {
        await candidateCommentService.markAsPending(comment.id);
      }
      await loadComments();
      onCommentChange?.(); // Notify parent to refresh all comments
    } catch (err: any) {
      setError(err.message || t('company.candidates.comments.failedToUpdate'));
      console.error('Error updating comment status:', err);
    }
  };

  const formatDate = (dateString: string) => {
    try {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      });
    } catch {
      return 'Unknown date';
    }
  };

  if (!stageId) {
    return null; // Don't show if no stage is assigned
  }

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
          <MessageSquare className="w-5 h-5 text-blue-600" />
          {t('company.candidates.commentsLabel')}
        </h3>
        {!showAddForm && (
          <button
            onClick={() => setShowAddForm(true)}
            className="flex items-center gap-2 px-3 py-1.5 text-sm text-blue-600 hover:text-blue-700 hover:bg-blue-50 rounded-lg transition-colors"
          >
            <Plus className="w-4 h-4" />
            {t('company.candidates.comments.addComment')}
          </button>
        )}
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-sm text-red-800">{error}</p>
        </div>
      )}

      {showAddForm && (
        <div className="mb-4 p-4 bg-gray-50 rounded-lg border border-gray-200">
          <textarea
            value={newCommentText}
            onChange={(e) => setNewCommentText(e.target.value)}
            placeholder={t('company.candidates.comments.writeComment')}
            className="w-full h-24 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none mb-3"
          />
          <div className="flex items-center gap-2">
            <button
              onClick={handleAddComment}
              disabled={addingComment || !newCommentText.trim()}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors text-sm"
            >
              {addingComment ? t('company.candidates.comments.loading', { defaultValue: 'Adding...' }) : t('company.candidates.comments.submit')}
            </button>
            <button
              onClick={() => {
                setShowAddForm(false);
                setNewCommentText('');
              }}
              disabled={addingComment}
              className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed transition-colors text-sm"
            >
              {t('company.candidates.comments.cancel')}
            </button>
          </div>
        </div>
      )}

      {loading ? (
        <div className="text-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-2"></div>
          <p className="text-sm text-gray-600">{t('company.candidates.comments.loading')}</p>
        </div>
      ) : comments.length > 0 && (
        <div className="space-y-4">
          {comments.map((comment) => (
            <div
              key={comment.id}
              className={`p-4 rounded-lg border ${
                comment.review_status === 'pending'
                  ? 'bg-yellow-50 border-yellow-200'
                  : 'bg-gray-50 border-gray-200'
              }`}
            >
              <div className="flex items-start justify-between mb-2">
                <div className="flex-1">
                  <p className="text-gray-900 whitespace-pre-wrap">{comment.comment}</p>
                  <div className="flex items-center gap-4 mt-2 text-xs text-gray-500">
                    <span className="flex items-center gap-1">
                      <Clock className="w-3 h-3" />
                      {formatDate(comment.created_at)}
                    </span>
                    {comment.created_by_user_name && (
                      <span>{t('company.candidates.detail.by')} {comment.created_by_user_name}</span>
                    )}
                  </div>
                </div>
                <button
                  onClick={() => handleTogglePending(comment)}
                  className={`p-1.5 rounded transition-colors ${
                    comment.review_status === 'pending'
                      ? 'text-yellow-600 hover:bg-yellow-100'
                      : 'text-gray-400 hover:bg-gray-100'
                  }`}
                  title={comment.review_status === 'pending' ? t('company.candidates.detail.markAsReviewed') : t('company.candidates.detail.markAsPending')}
                >
                  {comment.review_status === 'pending' ? (
                    <Clock className="w-4 h-4" />
                  ) : (
                    <CheckCircle className="w-4 h-4" />
                  )}
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

