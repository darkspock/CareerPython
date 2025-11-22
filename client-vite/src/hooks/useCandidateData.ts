import { useState, useEffect, useCallback, useRef } from 'react';
import { companyCandidateService } from '../services/companyCandidateService';
import { workflowStageService } from '../services/workflowStageService';
import { companyWorkflowService } from '../services/companyWorkflowService';
import { phaseService } from '../services/phaseService';
import type { CompanyCandidate } from '../types/companyCandidate';
import type { WorkflowStage } from '../types/workflow';

interface UseCandidateDataOptions {
  candidateId: string | undefined;
  companyId: string | null;
  onLoadComplete?: (candidate: CompanyCandidate) => Promise<void>;
}

export function useCandidateData({ candidateId, companyId, onLoadComplete }: UseCandidateDataOptions) {
  const [candidate, setCandidate] = useState<CompanyCandidate | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [availableStages, setAvailableStages] = useState<WorkflowStage[]>([]);
  const [nextStage, setNextStage] = useState<WorkflowStage | null>(null);
  const [failStages, setFailStages] = useState<WorkflowStage[]>([]);
  
  // Use ref to store the callback to avoid recreating loadCandidate on every render
  const onLoadCompleteRef = useRef(onLoadComplete);
  useEffect(() => {
    onLoadCompleteRef.current = onLoadComplete;
  }, [onLoadComplete]);

  const loadCandidate = useCallback(async () => {
    if (!candidateId) {
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      const data = await companyCandidateService.getById(candidateId);

      // Map workflow_id to current_workflow_id for backward compatibility
      if (data.workflow_id && !data.current_workflow_id) {
        data.current_workflow_id = data.workflow_id;
      }

      setCandidate(data);

      // Load workflow stages if candidate has a workflow or phase
      const workflowId = data.current_workflow_id || data.workflow_id;
      if (workflowId) {
        try {
          const stages = await companyWorkflowService.listStagesByWorkflow(workflowId);
          setAvailableStages(stages as WorkflowStage[]);

          const currentStage = stages.find((stage: WorkflowStage) => stage.id === data.current_stage_id);
          const currentOrder = currentStage?.order || 0;

          const next = await workflowStageService.getNextStage(workflowId, currentOrder);
          setNextStage(next as WorkflowStage | null);

          const fail = await workflowStageService.getFailStages(workflowId);
          setFailStages(fail as WorkflowStage[]);
        } catch (err) {
          console.error('Error loading workflow stages:', err);
        }
      } else if (data.phase_id && companyId) {
        // If no workflow but has phase, try to load stages from phase
        try {
          const phase = await phaseService.getPhase(companyId, data.phase_id);
          if (phase.workflow_type) {
            const stages = await companyWorkflowService.listStagesByPhase(data.phase_id, phase.workflow_type);
            setAvailableStages(stages.sort((a, b) => a.order - b.order) as WorkflowStage[]);
          }
        } catch (err) {
          console.warn('Failed to load stages from phase:', err);
        }
      }

      setError(null);
      
      // Call optional callback for additional loading (using ref to avoid dependency issues)
      if (onLoadCompleteRef.current) {
        await onLoadCompleteRef.current(data);
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to load candidate';
      setError(errorMessage);
      console.error('Error loading candidate:', err);
    } finally {
      setLoading(false);
    }
  }, [candidateId, companyId]);

  useEffect(() => {
    if (candidateId) {
      loadCandidate();
    } else {
      setLoading(false);
      setCandidate(null);
    }
  }, [candidateId, loadCandidate]);

  return {
    candidate,
    loading,
    error,
    availableStages,
    nextStage,
    failStages,
    reloadCandidate: loadCandidate,
  };
}

