/**
 * Job Position Comments Section Component
 * 
 * Main component that combines comment form and list with tab switching.
 */

import React, { useState, useEffect } from 'react';
import { MessageSquare, Globe, AlertCircle } from 'lucide-react';
import { JobPositionCommentForm } from './JobPositionCommentForm';
import { JobPositionCommentsList } from './JobPositionCommentsList';
import JobPositionCommentService from '@/services/JobPositionCommentService';
import type { JobPositionComment } from '@/types/jobPositionComment';
// Note: Using simple alerts instead of toast for now
const toast = {
  success: (msg: string) => alert(msg),
  error: (msg: string) => alert(msg),
};

interface JobPositionCommentsSectionProps {
  positionId: string;
  currentStageId?: string;
}

type CommentTab = 'current' | 'global' | 'all';

export const JobPositionCommentsSection: React.FC<JobPositionCommentsSectionProps> = ({
  positionId,
  currentStageId,
}) => {
  const [activeTab, setActiveTab] = useState<CommentTab>('current');
  const [comments, setComments] = useState<JobPositionComment[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Load comments based on active tab
  const loadComments = async () => {
    setIsLoading(true);
    try {
      let fetchedComments: JobPositionComment[];
      
      switch (activeTab) {
        case 'current':
          fetchedComments = currentStageId
            ? await JobPositionCommentService.getCurrentStageComments(positionId, currentStageId)
            : await JobPositionCommentService.getGlobalComments(positionId);
          break;
        case 'global':
          fetchedComments = await JobPositionCommentService.getGlobalComments(positionId);
          break;
        case 'all':
          fetchedComments = await JobPositionCommentService.getAllComments(positionId);
          break;
        default:
          fetchedComments = [];
      }
      
      setComments(fetchedComments);
    } catch (error) {
      console.error('Error loading comments:', error);
      toast.error('Error al cargar comentarios');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadComments();
  }, [positionId, currentStageId, activeTab]);

  // Create comment
  const handleCreateComment = async (data: {
    comment: string;
    stage_id?: string | null;
    visibility: any;
    review_status: any;
  }) => {
    setIsSubmitting(true);
    try {
      await JobPositionCommentService.createComment(positionId, data);
      await loadComments();
    } catch (error) {
      console.error('Error creating comment:', error);
      toast.error('Error al crear comentario');
    } finally {
      setIsSubmitting(false);
    }
  };

  // Delete comment
  const handleDeleteComment = async (commentId: string) => {
    if (!confirm('¿Estás seguro de que quieres eliminar este comentario?')) {
      return;
    }

    try {
      await JobPositionCommentService.deleteComment(commentId);
      toast.success('Comentario eliminado');
      await loadComments();
    } catch (error) {
      console.error('Error deleting comment:', error);
      toast.error('Error al eliminar comentario');
    }
  };

  // Toggle review status
  const handleToggleReviewStatus = async (commentId: string) => {
    const comment = comments.find(c => c.id === commentId);
    if (!comment) return;

    try {
      if (comment.review_status === 'pending') {
        await JobPositionCommentService.markCommentAsReviewed(commentId);
      } else {
        await JobPositionCommentService.markCommentAsPending(commentId);
      }
      await loadComments();
    } catch (error) {
      console.error('Error toggling comment review status:', error);
      toast.error('Error al actualizar el estado del comentario');
    }
  };

  const pendingCount = JobPositionCommentService.countPendingComments(comments);

  return (
    <div className="space-y-4">
      {/* Tabs */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          <button
            onClick={() => setActiveTab('current')}
            className={`py-2 px-1 border-b-2 font-medium text-sm flex items-center gap-2 ${
              activeTab === 'current'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            <MessageSquare className="h-4 w-4" />
            <span>Etapa actual</span>
            {activeTab === 'current' && pendingCount > 0 && (
              <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                {pendingCount}
              </span>
            )}
          </button>

          <button
            onClick={() => setActiveTab('global')}
            className={`py-2 px-1 border-b-2 font-medium text-sm flex items-center gap-2 ${
              activeTab === 'global'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            <Globe className="h-4 w-4" />
            <span>Globales</span>
          </button>

          <button
            onClick={() => setActiveTab('all')}
            className={`py-2 px-1 border-b-2 font-medium text-sm flex items-center gap-2 ${
              activeTab === 'all'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            <AlertCircle className="h-4 w-4" />
            <span>Todos</span>
          </button>
        </nav>
      </div>

      {/* Comment form */}
      <JobPositionCommentForm
        onSubmit={handleCreateComment}
        currentStageId={currentStageId}
        isGlobalComment={activeTab === 'global'}
        isSubmitting={isSubmitting}
      />

      {/* Comments list */}
      <JobPositionCommentsList
        comments={comments}
        onDelete={handleDeleteComment}
        onToggleReviewStatus={handleToggleReviewStatus}
        isLoading={isLoading}
      />
    </div>
  );
};

