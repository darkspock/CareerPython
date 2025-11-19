/**
 * Candidate Reviews Section
 * 
 * Adapter component that uses the generic ReviewsSection
 * with candidate-specific logic and services.
 */

import { useState, useEffect } from 'react';
import { Heart, Globe, AlertCircle, MessageSquare, Ban, ThumbsDown, ThumbsUp } from 'lucide-react';
import ReviewForm from './ReviewForm';
import ReviewsList from './ReviewsList';
import { candidateReviewService } from '../../services/candidateReviewService';
import type { CandidateReview } from '../../types/candidateReview';
import type { ReviewScore } from '../../types/candidateReview';

export type ReviewTab = 'current' | 'global' | 'all';

interface CandidateReviewsSectionProps {
  companyCandidateId: string;
  stageId: string | null;
  currentWorkflowId?: string | null;
  onReviewChange?: () => void;
  refreshKey?: number;
}

export default function CandidateReviewsSection({
  companyCandidateId,
  stageId,
  currentWorkflowId,
  onReviewChange,
  refreshKey = 0,
}: CandidateReviewsSectionProps) {
  const [activeTab, setActiveTab] = useState<ReviewTab>('current');
  const [reviews, setReviews] = useState<CandidateReview[]>([]);
  const [allReviews, setAllReviews] = useState<CandidateReview[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);
  const [totalReviewsCount, setTotalReviewsCount] = useState(0);

  // Load reviews based on tab
  const loadReviews = async (tab: ReviewTab): Promise<CandidateReview[]> => {
    switch (tab) {
      case 'current':
        if (!stageId) return [];
        return await candidateReviewService.getReviewsByStage(companyCandidateId, stageId);
      case 'global':
        return await candidateReviewService.getGlobalReviews(companyCandidateId);
      case 'all':
        return await candidateReviewService.getReviewsByCandidate(companyCandidateId);
      default:
        return [];
    }
  };

  // Load total reviews count and all reviews for average calculation
  const loadTotalReviewsCount = async () => {
    try {
      const allReviewsData = await candidateReviewService.getReviewsByCandidate(companyCandidateId);
      setAllReviews(allReviewsData);
      setTotalReviewsCount(allReviewsData.length);
    } catch (error) {
      console.error('Error loading reviews count:', error);
    }
  };

  // Calculate average score and get closest icon
  const getAverageScore = (): { average: number; closestIcon: React.ReactNode; closestScore: ReviewScore } => {
    if (allReviews.length === 0) {
      return { average: 0, closestIcon: null, closestScore: 0 };
    }

    const totalScore = allReviews.reduce((sum, review) => sum + review.score, 0);
    const average = totalScore / allReviews.length;
    const roundedAverage = Math.round(average * 10) / 10;

    // Find closest score (0, 3, 6, 10)
    const scores: ReviewScore[] = [0, 3, 6, 10];
    const closestScore = scores.reduce((prev, curr) => 
      Math.abs(curr - average) < Math.abs(prev - average) ? curr : prev
    ) as ReviewScore;

    // Get icon for closest score
    let closestIcon: React.ReactNode;
    switch (closestScore) {
      case 0:
        closestIcon = <Ban className="w-4 h-4" />;
        break;
      case 3:
        closestIcon = <ThumbsDown className="w-4 h-4" />;
        break;
      case 6:
        closestIcon = <ThumbsUp className="w-4 h-4" />;
        break;
      case 10:
        closestIcon = <Heart className="w-4 h-4" />;
        break;
      default:
        closestIcon = null;
    }

    return { average: roundedAverage, closestIcon, closestScore };
  };

  useEffect(() => {
    loadTotalReviewsCount();
    if (isExpanded) {
      handleLoadReviews();
    }
  }, [activeTab, stageId, isExpanded]);

  // Reload reviews when refreshKey changes (external updates from other instances)
  useEffect(() => {
    if (refreshKey > 0) {
      loadTotalReviewsCount();
      // If expanded, also reload the reviews list
      if (isExpanded) {
        handleLoadReviews();
      }
    }
  }, [refreshKey, isExpanded]);

  const handleLoadReviews = async () => {
    setIsLoading(true);
    try {
      const fetchedReviews = await loadReviews(activeTab);
      setReviews(fetchedReviews);
    } catch (error) {
      console.error('Error loading reviews:', error);
    } finally {
      setIsLoading(false);
    }
  };

  // Create review
  const handleCreateReview = async (score: ReviewScore, comment?: string | null, isGlobal?: boolean): Promise<void> => {
    setIsSubmitting(true);
    try {
      await candidateReviewService.createReview(companyCandidateId, {
        score,
        comment: comment || null,
        workflow_id: currentWorkflowId || null,
        stage_id: isGlobal ? null : (stageId || null),
        review_status: 'reviewed',
      });
      await loadTotalReviewsCount();
      if (isExpanded) {
        await handleLoadReviews();
      }
      onReviewChange?.();
    } catch (error) {
      console.error('Error creating review:', error);
      throw error;
    } finally {
      setIsSubmitting(false);
    }
  };

  // Delete review
  const handleDeleteReview = async (reviewId: string): Promise<void> => {
    if (!confirm('¿Estás seguro de que quieres eliminar este review?')) {
      return;
    }

    try {
      await candidateReviewService.deleteReview(reviewId);
      await loadTotalReviewsCount();
      if (isExpanded) {
        await handleLoadReviews();
      }
      onReviewChange?.();
    } catch (error) {
      console.error('Error deleting review:', error);
    }
  };

  // Toggle review status
  const handleToggleReviewStatus = async (reviewId: string): Promise<void> => {
    try {
      const review = reviews.find(r => r.id === reviewId);
      if (!review) return;

      if (review.review_status === 'pending') {
        await candidateReviewService.markAsReviewed(reviewId);
      } else {
        await candidateReviewService.markAsPending(reviewId);
      }

      if (isExpanded) {
        await handleLoadReviews();
      }
      onReviewChange?.();
    } catch (error) {
      console.error('Error toggling review status:', error);
    }
  };

  if (!stageId) {
    return null; // Don't show if no stage is assigned
  }

  const pendingCount = reviews.filter(r => r.review_status === 'pending').length;
  const { average, closestIcon } = getAverageScore();

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
          <Heart className="w-5 h-5 text-pink-600" />
          Reviews
        </h3>
        
        {/* Reviews counter and average - moved to top right */}
        {totalReviewsCount > 0 && (
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="flex items-center gap-2 text-sm text-gray-700 hover:text-gray-900 transition-colors px-3 py-1.5 rounded-lg hover:bg-gray-50"
          >
            {closestIcon && (
              <span className="flex items-center gap-1.5">
                <span className="text-gray-600">{closestIcon}</span>
                <span className="font-semibold text-gray-900">{average.toFixed(1)}</span>
              </span>
            )}
            <span className="text-gray-500 border-l border-gray-300 pl-2">
              {totalReviewsCount} {totalReviewsCount === 1 ? 'review' : 'reviews'}
            </span>
          </button>
        )}
      </div>

      {/* Review form */}
      <div className="mb-4">
        <ReviewForm
          onSubmit={handleCreateReview}
          isSubmitting={isSubmitting}
          showCommentField={true}
          showGlobalOption={true}
        />
      </div>

      {/* Reviews list (only shown when expanded) */}
      {isExpanded && (
        <div className="mt-6">
          {/* Tabs */}
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

          <ReviewsList
            reviews={reviews}
            onDelete={handleDeleteReview}
            onToggleReviewStatus={handleToggleReviewStatus}
            isLoading={isLoading}
            showWorkflowInfo={true}
            showStageInfo={true}
            showAuthorInfo={true}
          />

          {/* Collapse button */}
          <div className="mt-4">
            <button
              onClick={() => setIsExpanded(false)}
              className="text-sm text-gray-600 hover:text-gray-700 hover:underline"
            >
              Ocultar reviews
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

