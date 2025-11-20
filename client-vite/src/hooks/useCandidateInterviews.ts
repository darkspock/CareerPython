import { useState, useEffect, useCallback, useMemo } from 'react';
import { companyInterviewService, type Interview } from '../services/companyInterviewService';

interface UseCandidateInterviewsProps {
  candidateId: string | undefined;
  companyCandidateId: string | undefined;
  currentStageId: string | null | undefined;
}

export function useCandidateInterviews({
  candidateId,
  companyCandidateId,
  currentStageId,
}: UseCandidateInterviewsProps) {
  const [allInterviews, setAllInterviews] = useState<Interview[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Computed: entrevistas de la etapa actual
  const currentStageInterviews = useMemo(() => 
    allInterviews.filter(interview => interview.workflow_stage_id === currentStageId),
    [allInterviews, currentStageId]
  );
  
  // Computed: entrevistas de otras etapas
  const otherStagesInterviews = useMemo(() =>
    allInterviews.filter(interview => interview.workflow_stage_id !== currentStageId),
    [allInterviews, currentStageId]
  );

  const loadInterviews = useCallback(async () => {
    if (!candidateId) {
      setAllInterviews([]);
      return;
    }

    try {
      setLoading(true);
      setError(null);

      // Cargar TODAS las entrevistas del candidato (sin filtro de etapa)
      // El endpoint GET /api/company/interviews acepta candidate_id como query param
      const interviews = await companyInterviewService.listInterviews({
        candidate_id: candidateId,
        limit: 100, // Obtener todas las entrevistas del candidato
      });

      setAllInterviews(interviews.interviews || []);
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to load interviews';
      setError(errorMessage);
      console.error('Error loading candidate interviews:', err);
      setAllInterviews([]);
    } finally {
      setLoading(false);
    }
  }, [candidateId]);

  // Recargar entrevistas cuando cambia el candidateId
  useEffect(() => {
    loadInterviews();
  }, [loadInterviews]);

  const createInterview = useCallback(async (data: {
    workflow_stage_id: string;
    interview_type: string;
    interview_template_id?: string | null;
    required_roles: string[];
    scheduled_at?: string | null;
    interviewers?: string[];
  }) => {
    if (!candidateId) {
      throw new Error('Candidate ID is required');
    }

    if (!data.workflow_stage_id) {
      throw new Error('workflow_stage_id is required');
    }

    if (!data.required_roles || data.required_roles.length === 0) {
      throw new Error('At least one required role is needed');
    }

    try {
      setLoading(true);
      setError(null);

      // Crear la entrevista (workflow_stage_id es obligatorio)
      await companyInterviewService.createInterview({
        candidate_id: candidateId,
        workflow_stage_id: data.workflow_stage_id,
        interview_type: data.interview_type as any, // TODO: Fix typing
        interview_mode: 'MANUAL', // Por defecto MANUAL
        interview_template_id: data.interview_template_id,
        required_roles: data.required_roles,
        scheduled_at: data.scheduled_at,
        interviewers: data.interviewers,
      });

      // Recargar todas las entrevistas
      await loadInterviews();
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to create interview';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [candidateId, loadInterviews]);

  return {
    allInterviews,
    currentStageInterviews,
    otherStagesInterviews,
    loading,
    error,
    loadInterviews,
    createInterview,
  };
}

