/**
 * Generic Comments Section Component
 * 
 * Main container component that combines:
 * - Comment form (with all options)
 * - Comments list (with filtering and actions)
 * - Tab navigation (for different comment views)
 * 
 * This component is designed to be positioned below the main card with tabs,
 * similar to the candidate detail page layout.
 */

import { useState, useEffect } from 'react';
import { MessageSquare, Globe, AlertCircle } from 'lucide-react';
import { CommentForm, type CommentFormData } from './CommentForm';
import { CommentsList, type BaseComment } from './CommentsList';

export type CommentTab = 'current' | 'global' | 'all';

interface CommentsSectionProps<T extends BaseComment> {
  // Data loading
  loadComments: (tab: CommentTab) => Promise<T[]>;
  
  // Comment creation
  onCreateComment: (data: CommentFormData) => Promise<void>;
  
  // Comment actions
  onDeleteComment?: (commentId: string) => Promise<void>;
  onToggleReviewStatus?: (commentId: string) => Promise<void>;
  
  // Configuration
  currentStageId?: string | null;
  workflowId?: string | null;
  showGlobalTab?: boolean;
  showAllTab?: boolean;
  showWorkflowInfo?: boolean;
  showStageInfo?: boolean;
  showAuthorInfo?: boolean;
  onCommentsChange?: () => void;
  refreshKey?: number; // Key that changes when comments are updated externally
  
  // UI customization
  title?: string;
  emptyMessage?: string;
  placeholder?: string;
  formatDate?: (dateStr: string) => string;
  defaultExpanded?: boolean;
  onNavigateToCommentsTab?: () => void; // Callback to navigate to comments tab instead of expanding
}

export function CommentsSection<T extends BaseComment>({
  loadComments,
  onCreateComment,
  onDeleteComment,
  onToggleReviewStatus,
  currentStageId,
  workflowId: _workflowId, // Reserved for future use
  showGlobalTab = true,
  showAllTab = true,
  showWorkflowInfo = false,
  showStageInfo = false,
  showAuthorInfo = true,
  onCommentsChange,
  refreshKey = 0,
  title = 'Comentarios',
  emptyMessage = 'No hay comentarios todavía',
  placeholder = 'Escribe un comentario...',
  formatDate,
  defaultExpanded = false,
  onNavigateToCommentsTab,
}: CommentsSectionProps<T>) {
  const [activeTab, setActiveTab] = useState<CommentTab>('current');
  const [comments, setComments] = useState<T[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isExpanded, setIsExpanded] = useState(defaultExpanded);
  const [totalCommentsCount, setTotalCommentsCount] = useState(0);

  // Load comments based on active tab
  const handleLoadComments = async () => {
    setIsLoading(true);
    try {
      const fetchedComments = await loadComments(activeTab);
      setComments(fetchedComments);
    } catch (error) {
      console.error('Error loading comments:', error);
    } finally {
      setIsLoading(false);
    }
  };

  // Load total comments count
  const loadTotalCommentsCount = async () => {
    try {
      const allComments = await loadComments('all');
      setTotalCommentsCount(allComments.length);
    } catch (error) {
      console.error('Error loading comments count:', error);
    }
  };

  // Initial load
  useEffect(() => {
    loadTotalCommentsCount();
    if (isExpanded) {
      handleLoadComments();
    }
  }, [activeTab, currentStageId, isExpanded]);

  // Reload count and list when refreshKey changes (external updates from other instances)
  useEffect(() => {
    if (refreshKey > 0) {
      loadTotalCommentsCount();
      // If expanded, also reload the comments list
      if (isExpanded) {
        handleLoadComments();
      }
    }
  }, [refreshKey, isExpanded]);

  // Create comment
  const handleCreateComment = async (data: CommentFormData) => {
    setIsSubmitting(true);
    try {
      await onCreateComment(data);
      await loadTotalCommentsCount();
      if (isExpanded) {
        await handleLoadComments();
      }
      onCommentsChange?.();
    } catch (error) {
      console.error('Error creating comment:', error);
      throw error; // Re-throw to let form handle it
    } finally {
      setIsSubmitting(false);
    }
  };

  // Delete comment
  const handleDeleteComment = async (commentId: string) => {
    if (!onDeleteComment) return;
    
    if (!confirm('¿Estás seguro de que quieres eliminar este comentario?')) {
      return;
    }

    try {
      await onDeleteComment(commentId);
      await loadTotalCommentsCount();
      if (isExpanded) {
        await handleLoadComments();
      }
      onCommentsChange?.();
    } catch (error) {
      console.error('Error deleting comment:', error);
    }
  };

  // Toggle review status
  const handleToggleReviewStatus = async (commentId: string) => {
    if (!onToggleReviewStatus) return;

    try {
      await onToggleReviewStatus(commentId);
      if (isExpanded) {
        await handleLoadComments();
      }
      onCommentsChange?.();
    } catch (error) {
      console.error('Error toggling comment review status:', error);
    }
  };

  const pendingCount = comments.filter(c => c.review_status === 'pending').length;
  const isGlobalComment = activeTab === 'global';

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
          <MessageSquare className="w-5 h-5 text-blue-600" />
          {title}
        </h3>
        {totalCommentsCount > 0 && !isExpanded && (
          <button
            onClick={() => {
              if (onNavigateToCommentsTab) {
                onNavigateToCommentsTab();
              } else {
                setIsExpanded(true);
              }
            }}
            className="text-sm text-blue-600 hover:text-blue-700 hover:underline"
          >
            {totalCommentsCount} {totalCommentsCount === 1 ? 'comentario' : 'comentarios'}
          </button>
        )}
      </div>

      {/* Comment form - only show when NOT expanded */}
      {!isExpanded && (
        <div className="mb-4">
          <CommentForm
            onSubmit={handleCreateComment}
            isSubmitting={isSubmitting}
            isGlobalComment={isGlobalComment}
            placeholder={placeholder}
            showVisibilityOption={true}
            showReviewOption={true}
            showGlobalOption={showGlobalTab && activeTab === 'global'}
            defaultVisibility="shared"
            defaultReviewStatus="reviewed"
          />
        </div>
      )}

      {/* Comments list (only shown when expanded) */}
      {isExpanded && (
        <div className="mt-6">
          {/* Tabs */}
          {(showGlobalTab || showAllTab) && (
            <div className="border-b border-gray-200 mb-4">
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

                {showGlobalTab && (
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
                )}

                {showAllTab && (
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
                )}
              </nav>
            </div>
          )}

          <CommentsList
            comments={comments}
            onDelete={onDeleteComment ? handleDeleteComment : undefined}
            onToggleReviewStatus={onToggleReviewStatus ? handleToggleReviewStatus : undefined}
            isLoading={isLoading}
            emptyMessage={emptyMessage}
            showWorkflowInfo={showWorkflowInfo}
            showStageInfo={showStageInfo}
            showAuthorInfo={showAuthorInfo}
            formatDate={formatDate}
          />
        </div>
      )}
    </div>
  );
}

