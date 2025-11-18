import { useState, useEffect, useCallback } from 'react';
import { companyInterviewService } from '../services/companyInterviewService';
import type { Interview, InterviewScoreSummaryResponse } from '../services/companyInterviewService';
import { toast } from 'react-toastify';

export interface UseInterviewDetailReturn {
  interview: Interview | null;
  scoreSummary: InterviewScoreSummaryResponse | null;
  loading: boolean;
  actionLoading: boolean;
  error: string | null;
  loadInterview: () => Promise<void>;
  loadScoreSummary: () => Promise<void>;
  startInterview: () => Promise<void>;
  finishInterview: () => Promise<void>;
  refresh: () => Promise<void>;
}

export function useInterviewDetail(interviewId: string | undefined): UseInterviewDetailReturn {
  const [interview, setInterview] = useState<Interview | null>(null);
  const [scoreSummary, setScoreSummary] = useState<InterviewScoreSummaryResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const loadInterview = useCallback(async () => {
    if (!interviewId) return;
    
    try {
      setLoading(true);
      setError(null);
      const data = await companyInterviewService.getInterviewView(interviewId);
      setInterview(data);
    } catch (err: any) {
      const errorMessage = err.message || 'Error al cargar la entrevista';
      setError(errorMessage);
      console.error('Error loading interview:', err);
      toast.error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, [interviewId]);
  
  const loadScoreSummary = useCallback(async () => {
    if (!interviewId) return;
    
    try {
      const summary = await companyInterviewService.getInterviewScoreSummary(interviewId);
      setScoreSummary(summary);
    } catch (err: any) {
      console.warn('Could not load score summary:', err);
      // Don't fail if score summary can't be loaded
    }
  }, [interviewId]);
  
  const startInterview = useCallback(async () => {
    if (!interviewId) return;
    
    try {
      setActionLoading(true);
      await companyInterviewService.startInterview(interviewId);
      toast.success('Entrevista iniciada correctamente');
      await loadInterview();
    } catch (err: any) {
      toast.error(err.message || 'Error al iniciar la entrevista');
    } finally {
      setActionLoading(false);
    }
  }, [interviewId, loadInterview]);
  
  const finishInterview = useCallback(async () => {
    if (!interviewId) return;
    
    try {
      setActionLoading(true);
      await companyInterviewService.finishInterview(interviewId);
      toast.success('Entrevista finalizada correctamente');
      await Promise.all([loadInterview(), loadScoreSummary()]);
    } catch (err: any) {
      toast.error(err.message || 'Error al finalizar la entrevista');
    } finally {
      setActionLoading(false);
    }
  }, [interviewId, loadInterview, loadScoreSummary]);
  
  const refresh = useCallback(async () => {
    await Promise.all([loadInterview(), loadScoreSummary()]);
  }, [loadInterview, loadScoreSummary]);
  
  useEffect(() => {
    if (interviewId) {
      loadInterview();
      loadScoreSummary();
    }
  }, [interviewId, loadInterview, loadScoreSummary]);
  
  return {
    interview,
    scoreSummary,
    loading,
    actionLoading,
    error,
    loadInterview,
    loadScoreSummary,
    startInterview,
    finishInterview,
    refresh,
  };
}

