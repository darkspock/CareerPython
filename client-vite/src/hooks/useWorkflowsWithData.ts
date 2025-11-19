import { useState, useCallback } from 'react';
import { customFieldValueService, type CustomFieldValue } from '../services/customFieldValueService';
import { companyWorkflowService } from '../services/companyWorkflowService';
import type { CompanyCandidate } from '../types/companyCandidate';
import type { CandidateComment } from '../types/candidateComment';

interface UseWorkflowsWithDataOptions {
  companyCandidateId: string | undefined;
  candidate: CompanyCandidate | null;
  allComments: CandidateComment[];
}

export function useWorkflowsWithData({
  companyCandidateId,
  candidate,
  allComments,
}: UseWorkflowsWithDataOptions) {
  const [allCustomFieldValues, setAllCustomFieldValues] = useState<Record<string, Record<string, CustomFieldValue>>>({});
  const [availableWorkflows, setAvailableWorkflows] = useState<Array<{ id: string; name: string }>>([]);
  const [selectedWorkflowId, setSelectedWorkflowId] = useState<string | null>(null);
  const [loadingWorkflows, setLoadingWorkflows] = useState(false);

  const loadWorkflowsWithData = useCallback(async () => {
    if (!companyCandidateId) return;

    try {
      setLoadingWorkflows(true);

      // Get all custom field values organized by workflow_id
      let allValues: Record<string, Record<string, CustomFieldValue>> = {};
      try {
        allValues = await customFieldValueService.getAllCustomFieldValuesByCompanyCandidate(companyCandidateId);
        setAllCustomFieldValues(allValues);
      } catch (err) {
        console.warn('Failed to load custom field values:', err);
        setAllCustomFieldValues({});
      }

      // Get unique workflow IDs from custom fields and comments
      const workflowIds = new Set<string>();

      // Add workflows with custom fields
      Object.keys(allValues).forEach((workflowId) => {
        if (Object.keys(allValues[workflowId]).length > 0) {
          workflowIds.add(workflowId);
        }
      });

      // Add workflows with comments
      allComments.forEach((comment) => {
        if (comment.workflow_id) {
          workflowIds.add(comment.workflow_id);
        }
      });

      // Add current workflow if candidate has one
      if (candidate?.current_workflow_id) {
        workflowIds.add(candidate.current_workflow_id);
      }

      // Fetch workflow names for all workflows
      const workflowsData: Array<{ id: string; name: string }> = [];
      for (const workflowId of workflowIds) {
        try {
          const workflow = await companyWorkflowService.getWorkflow(workflowId);
          workflowsData.push({ id: workflowId, name: workflow.name });
        } catch (err) {
          console.warn(`Failed to load workflow ${workflowId}:`, err);
          workflowsData.push({ id: workflowId, name: workflowId });
        }
      }

      setAvailableWorkflows(workflowsData);

      // Set selected workflow to current workflow if available, otherwise first one
      if (candidate?.current_workflow_id && workflowIds.has(candidate.current_workflow_id)) {
        setSelectedWorkflowId(candidate.current_workflow_id);
      } else if (workflowsData.length > 0) {
        setSelectedWorkflowId(workflowsData[0].id);
      } else {
        setSelectedWorkflowId(null);
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to load workflows';
      console.error('Error loading workflows with data:', errorMessage);
      setAvailableWorkflows([]);
      setSelectedWorkflowId(null);
    } finally {
      setLoadingWorkflows(false);
    }
  }, [companyCandidateId, candidate, allComments]);

  return {
    allCustomFieldValues,
    availableWorkflows,
    selectedWorkflowId,
    loadingWorkflows,
    setSelectedWorkflowId,
    loadWorkflowsWithData,
  };
}

