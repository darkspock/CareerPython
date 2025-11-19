import { useState, useCallback } from 'react';
import { candidateCommentService } from '../services/candidateCommentService';
import type { CandidateComment } from '../types/candidateComment';

interface UseCandidateCommentsOptions {
  companyCandidateId: string | undefined;
}

export function useCandidateComments({ companyCandidateId }: UseCandidateCommentsOptions) {
  const [allComments, setAllComments] = useState<CandidateComment[]>([]);
  const [pendingCommentsCount, setPendingCommentsCount] = useState(0);
  const [loadingComments, setLoadingComments] = useState(false);
  const [commentsRefreshKey, setCommentsRefreshKey] = useState(0);

  const loadAllComments = useCallback(async () => {
    if (!companyCandidateId) return;

    try {
      setLoadingComments(true);
      const comments = await candidateCommentService.getCommentsByCompanyCandidate(companyCandidateId);
      setAllComments(comments || []);

      const pendingCount = await candidateCommentService.countPendingComments(companyCandidateId);
      setPendingCommentsCount(pendingCount || 0);
    } catch (err) {
      console.error('Error loading comments:', err);
      setAllComments([]);
      setPendingCommentsCount(0);
    } finally {
      setLoadingComments(false);
    }
  }, [companyCandidateId]);

  const refreshComments = useCallback(() => {
    setCommentsRefreshKey((prev) => prev + 1);
  }, []);

  return {
    allComments,
    pendingCommentsCount,
    loadingComments,
    commentsRefreshKey,
    loadAllComments,
    refreshComments,
  };
}

