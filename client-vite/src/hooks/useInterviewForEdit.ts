import { useState, useEffect, useCallback } from 'react';
import { companyInterviewService } from '../services/companyInterviewService';
import type { Interview } from '../services/companyInterviewService';
import { toast } from 'react-toastify';

export interface UseInterviewForEditReturn {
  interview: Interview | null;
  loading: boolean;
  error: string | null;
  loadInterview: () => Promise<void>;
  refresh: () => Promise<void>;
}

export function useInterviewForEdit(interviewId: string | undefined): UseInterviewForEditReturn {
  const [interview, setInterview] = useState<Interview | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  const loadInterview = useCallback(async () => {
    if (!interviewId) return;
    
    try {
      setLoading(true);
      setError(null);
      // Use getInterview for edit page (not getInterviewView)
      const data = await companyInterviewService.getInterview(interviewId);
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
  
  const refresh = useCallback(async () => {
    await loadInterview();
  }, [loadInterview]);
  
  useEffect(() => {
    if (interviewId) {
      loadInterview();
    }
  }, [interviewId, loadInterview]);
  
  return {
    interview,
    loading,
    error,
    loadInterview,
    refresh,
  };
}

