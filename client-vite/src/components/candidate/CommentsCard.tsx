import { useState, useEffect } from 'react';
import { MessageSquare, Plus, Clock, CheckCircle } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { candidateCommentService } from '../../services/candidateCommentService';
import type { CandidateComment, CreateCandidateCommentRequest } from '../../types/candidateComment';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Textarea } from '@/components/ui/textarea';
import { Alert, AlertDescription } from '@/components/ui/alert';
import LoadingSpinner from '@/components/common/LoadingSpinner';

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
      onCommentChange?.();
    } catch (err: any) {
      setError(err.message || t('company.candidates.comments.failedToAdd'));
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
      onCommentChange?.();
    } catch (err: any) {
      setError(err.message || t('company.candidates.comments.failedToUpdate'));
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
    return null;
  }

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-4">
        <CardTitle className="text-lg flex items-center gap-2">
          <MessageSquare className="w-5 h-5 text-primary" />
          {t('company.candidates.commentsLabel')}
        </CardTitle>
        {!showAddForm && (
          <Button variant="ghost" size="sm" onClick={() => setShowAddForm(true)}>
            <Plus className="w-4 h-4 mr-2" />
            {t('company.candidates.comments.addComment')}
          </Button>
        )}
      </CardHeader>

      <CardContent>
        {error && (
          <Alert variant="destructive" className="mb-4">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {showAddForm && (
          <div className="mb-4 p-4 bg-muted rounded-lg">
            <Textarea
              value={newCommentText}
              onChange={(e) => setNewCommentText(e.target.value)}
              placeholder={t('company.candidates.comments.writeComment')}
              className="mb-3 min-h-[96px]"
            />
            <div className="flex items-center gap-2">
              <Button
                onClick={handleAddComment}
                disabled={addingComment || !newCommentText.trim()}
                size="sm"
              >
                {addingComment ? t('company.candidates.comments.loading', { defaultValue: 'Adding...' }) : t('company.candidates.comments.submit')}
              </Button>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => {
                  setShowAddForm(false);
                  setNewCommentText('');
                }}
                disabled={addingComment}
              >
                {t('company.candidates.comments.cancel')}
              </Button>
            </div>
          </div>
        )}

        {loading ? (
          <div className="text-center py-8">
            <LoadingSpinner size="md" color="blue" text={t('company.candidates.comments.loading')} />
          </div>
        ) : comments.length > 0 && (
          <div className="space-y-4">
            {comments.map((comment) => (
              <div
                key={comment.id}
                className={`p-4 rounded-lg border ${
                  comment.review_status === 'pending'
                    ? 'bg-yellow-50 border-yellow-200'
                    : 'bg-muted/50 border-border'
                }`}
              >
                <div className="flex items-start justify-between mb-2">
                  <div className="flex-1">
                    <p className="text-foreground whitespace-pre-wrap">{comment.comment}</p>
                    <div className="flex items-center gap-4 mt-2 text-xs text-muted-foreground">
                      <span className="flex items-center gap-1">
                        <Clock className="w-3 h-3" />
                        {formatDate(comment.created_at)}
                      </span>
                      {comment.created_by_user_name && (
                        <span>{t('company.candidates.detail.by')} {comment.created_by_user_name}</span>
                      )}
                    </div>
                  </div>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => handleTogglePending(comment)}
                    className={
                      comment.review_status === 'pending'
                        ? 'text-yellow-600 hover:bg-yellow-100'
                        : 'text-muted-foreground hover:bg-muted'
                    }
                    title={comment.review_status === 'pending' ? t('company.candidates.detail.markAsReviewed') : t('company.candidates.detail.markAsPending')}
                  >
                    {comment.review_status === 'pending' ? (
                      <CheckCircle className="w-4 h-4" />
                    ) : (
                      <Clock className="w-4 h-4" />
                    )}
                  </Button>
                </div>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
