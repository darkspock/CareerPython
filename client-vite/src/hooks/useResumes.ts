/**
 * Custom hook for managing resume state and operations
 *
 * This hook provides centralized state management for resume operations
 * including loading states, error handling, and CRUD operations.
 */

import { useState, useEffect, useCallback } from 'react';
import { toast } from 'react-toastify';
import { api } from '../lib/api';
import type {
  Resume,
  ResumeListResponse,
  ResumeStatistics,
  CreateResumeRequest,
  UpdateResumeNameRequest,
  LoadingState,
  ErrorState
} from '../types/resume';

interface UseResumesState {
  resumes: Resume[];
  statistics: ResumeStatistics | null;
  loading: LoadingState;
  error: ErrorState;
}

interface UseResumesActions {
  fetchResumes: (params?: { resume_type?: string; limit?: number }) => Promise<void>;
  fetchStatistics: () => Promise<void>;
  createResume: (data: CreateResumeRequest) => Promise<Resume | null>;
  updateResumeName: (resumeId: string, data: UpdateResumeNameRequest) => Promise<Resume | null>;
  deleteResume: (resumeId: string) => Promise<void>;
  duplicateResume: (resumeId: string, newName: string) => Promise<Resume | null>;
  bulkDeleteResumes: (resumeIds: string[]) => Promise<void>;
  clearError: () => void;
  refreshResumes: () => Promise<void>;
}

export function useResumes(): UseResumesState & UseResumesActions {
  const [state, setState] = useState<UseResumesState>({
    resumes: [],
    statistics: null,
    loading: { isLoading: false },
    error: { hasError: false }
  });

  const setLoading = useCallback((isLoading: boolean, operation?: string) => {
    setState(prev => ({
      ...prev,
      loading: { isLoading, operation }
    }));
  }, []);

  const setError = useCallback((error: ErrorState) => {
    setState(prev => ({
      ...prev,
      error,
      loading: { isLoading: false }
    }));
  }, []);

  const clearError = useCallback(() => {
    setState(prev => ({
      ...prev,
      error: { hasError: false }
    }));
  }, []);

  const handleApiError = useCallback((error: any, operation: string) => {
    console.error(`Error in ${operation}:`, error);

    let errorMessage = 'An unexpected error occurred';
    let errorCode = 'UNKNOWN_ERROR';
    let details = {};

    if (error.message) {
      try {
        // Try to parse error message as JSON (from API)
        const errorData = JSON.parse(error.message);
        if (errorData.detail) {
          if (typeof errorData.detail === 'string') {
            errorMessage = errorData.detail;
          } else if (errorData.detail.message) {
            errorMessage = errorData.detail.message;
            errorCode = errorData.detail.error || errorCode;
            details = errorData.detail.details || {};
          }
        }
      } catch {
        // If not JSON, use the message directly
        errorMessage = error.message;
      }
    }

    setError({
      hasError: true,
      message: errorMessage,
      code: errorCode,
      details
    });

    toast.error(errorMessage);
  }, [setError]);

  const fetchResumes = useCallback(async (params?: { resume_type?: string; limit?: number }) => {
    // Check if user is authenticated before making API call
    const token = localStorage.getItem('access_token');
    if (!token) {
      setError({
        hasError: true,
        message: 'Please log in to access your resumes',
        code: 'NOT_AUTHENTICATED'
      });
      return;
    }

    setLoading(true, 'fetch_resumes');
    clearError();

    try {
      const response = await api.getResumes(params) as ResumeListResponse;
      setState(prev => ({
        ...prev,
        resumes: response.resumes,
        loading: { isLoading: false }
      }));
    } catch (error) {
      handleApiError(error, 'fetch resumes');
    }
  }, [setLoading, clearError, handleApiError, setError]);

  const fetchStatistics = useCallback(async () => {
    // Check if user is authenticated before making API call
    const token = localStorage.getItem('access_token');
    if (!token) {
      setError({
        hasError: true,
        message: 'Please log in to access resume statistics',
        code: 'NOT_AUTHENTICATED'
      });
      return;
    }

    setLoading(true, 'fetch_statistics');
    clearError();

    try {
      const statistics = await api.getResumeStatistics() as ResumeStatistics;
      setState(prev => ({
        ...prev,
        statistics,
        loading: { isLoading: false }
      }));
    } catch (error) {
      handleApiError(error, 'fetch statistics');
    }
  }, [setLoading, clearError, handleApiError, setError]);

  const createResume = useCallback(async (data: CreateResumeRequest): Promise<Resume | null> => {
    setLoading(true, 'create_resume');
    clearError();

    try {
      const resume = await api.createGeneralResume(data) as Resume;
      setState(prev => ({
        ...prev,
        resumes: [resume, ...prev.resumes],
        loading: { isLoading: false }
      }));
      toast.success('Resume created successfully!');
      return resume;
    } catch (error) {
      handleApiError(error, 'create resume');
      return null;
    }
  }, [setLoading, clearError, handleApiError]);

  const updateResumeName = useCallback(async (resumeId: string, data: UpdateResumeNameRequest): Promise<Resume | null> => {
    setLoading(true, 'update_resume_name');
    clearError();

    try {
      const updatedResume = await api.updateResumeName(resumeId, data) as Resume;
      setState(prev => ({
        ...prev,
        resumes: prev.resumes.map(resume =>
          resume.id === resumeId ? updatedResume : resume
        ),
        loading: { isLoading: false }
      }));
      toast.success('Resume name updated successfully!');
      return updatedResume;
    } catch (error) {
      handleApiError(error, 'update resume name');
      return null;
    }
  }, [setLoading, clearError, handleApiError]);

  const deleteResume = useCallback(async (resumeId: string) => {
    setLoading(true, 'delete_resume');
    clearError();

    try {
      await api.deleteResume(resumeId);
      setState(prev => ({
        ...prev,
        resumes: prev.resumes.filter(resume => resume.id !== resumeId),
        loading: { isLoading: false }
      }));
      toast.success('Resume deleted successfully!');
    } catch (error) {
      handleApiError(error, 'delete resume');
    }
  }, [setLoading, clearError, handleApiError]);

  const duplicateResume = useCallback(async (resumeId: string, newName: string): Promise<Resume | null> => {
    setLoading(true, 'duplicate_resume');
    clearError();

    try {
      const duplicatedResume = await api.duplicateResume(resumeId, newName) as Resume;
      setState(prev => ({
        ...prev,
        resumes: [duplicatedResume, ...prev.resumes],
        loading: { isLoading: false }
      }));
      toast.success('Resume duplicated successfully!');
      return duplicatedResume;
    } catch (error) {
      handleApiError(error, 'duplicate resume');
      return null;
    }
  }, [setLoading, clearError, handleApiError]);

  const bulkDeleteResumes = useCallback(async (resumeIds: string[]) => {
    setLoading(true, 'bulk_delete_resumes');
    clearError();

    try {
      await api.bulkDeleteResumes(resumeIds);
      setState(prev => ({
        ...prev,
        resumes: prev.resumes.filter(resume => !resumeIds.includes(resume.id)),
        loading: { isLoading: false }
      }));
      toast.success(`${resumeIds.length} resume(s) deleted successfully!`);
    } catch (error) {
      handleApiError(error, 'bulk delete resumes');
    }
  }, [setLoading, clearError, handleApiError]);

  const refreshResumes = useCallback(async () => {
    await fetchResumes();
  }, [fetchResumes]);

  // Auto-fetch resumes on mount
  useEffect(() => {
    fetchResumes();
  }, [fetchResumes]);

  return {
    ...state,
    fetchResumes,
    fetchStatistics,
    createResume,
    updateResumeName,
    deleteResume,
    duplicateResume,
    bulkDeleteResumes,
    clearError,
    refreshResumes
  };
}