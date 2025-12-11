import { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { PositionService } from '../../services/positionService';
import { companyWorkflowService } from '../../services/companyWorkflowService';
import type { CreatePositionRequest, UpdatePositionRequest, JobPositionWorkflow, JobPositionWorkflowStage } from '../../types/position';
import { PositionFormTabs } from '../../components/jobPosition/form';
import { Alert, AlertDescription } from '@/components/ui/alert';

export default function CreatePositionPage() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [currentWorkflow, setCurrentWorkflow] = useState<JobPositionWorkflow | null>(null);
  // Store the hiring pipeline (CA) workflow ID
  const [hiringPipelineId, setHiringPipelineId] = useState<string | null>(null);

  const getCompanyId = () => {
    const token = localStorage.getItem('access_token');
    if (!token) return null;
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return payload.company_id;
    } catch {
      return null;
    }
  };

  useEffect(() => {
    const loadWorkflow = async () => {
      const companyId = getCompanyId();
      if (!companyId) {
        setError('Company ID not found');
        setLoading(false);
        return;
      }

      // Get both workflow IDs from search params
      const publicationWorkflowId = searchParams.get('publication_workflow_id');
      const candidateApplicationWorkflowId = searchParams.get('hiring_pipeline_id');

      // If workflows were not selected (direct access to create page), redirect to workflow selection
      if (!publicationWorkflowId || !candidateApplicationWorkflowId) {
        navigate('/company/positions/select-workflows');
        return;
      }

      // Store the hiring pipeline ID
      setHiringPipelineId(candidateApplicationWorkflowId);

      // Helper to load workflow with stages including stage_type
      const loadWorkflowWithStages = async (wfId: string): Promise<JobPositionWorkflow> => {
        const fullWorkflow = await PositionService.getWorkflow(wfId);
        const stagesData = await companyWorkflowService.listStagesByWorkflow(wfId);

        const mappedStages: JobPositionWorkflowStage[] = stagesData.map((stage) => ({
          id: stage.id,
          name: stage.name,
          icon: stage.style?.icon || '📋',
          background_color: stage.style?.background_color || '#f3f4f6',
          text_color: stage.style?.color || '#374151',
          role: null,
          stage_type: stage.stage_type,
          status_mapping: stage.stage_type === 'success' ? 'closed' :
                         stage.stage_type === 'fail' ? 'closed' :
                         stage.stage_type === 'initial' ? 'draft' : 'active',
          kanban_display: stage.kanban_display || 'column',
          field_visibility: {},
          field_validation: {},
          field_candidate_visibility: {},
        }));

        return {
          ...fullWorkflow,
          stages: mappedStages,
        };
      };

      try {
        setLoading(true);

        // Load the publication workflow (PO)
        const fullWorkflow = await loadWorkflowWithStages(publicationWorkflowId);
        setCurrentWorkflow(fullWorkflow);
      } catch (err: unknown) {
        console.error('Error loading workflow:', err);
        const errorMessage = err instanceof Error ? err.message : 'Failed to load workflow';
        setError(errorMessage);
      } finally {
        setLoading(false);
      }
    };

    loadWorkflow();
  }, [searchParams, navigate]);

  const handleSave = async (data: CreatePositionRequest | UpdatePositionRequest) => {
    const companyId = getCompanyId();
    if (!companyId) {
      throw new Error('Company ID not found');
    }

    if (!currentWorkflow) {
      throw new Error('Workflow not loaded');
    }

    if (!hiringPipelineId) {
      throw new Error('Hiring pipeline not selected');
    }

    // In create mode, title is always required from the form
    const createData = data as CreatePositionRequest;
    const requestData: CreatePositionRequest = {
      ...createData,
      company_id: companyId,
      title: createData.title || 'Untitled Position',
      job_position_workflow_id: currentWorkflow.id,
      // Include the hiring pipeline (CA) workflow ID for candidate tracking
      candidate_application_workflow_id: hiringPipelineId,
      // Copy custom fields config from workflow
      custom_fields_config: currentWorkflow.custom_fields_config
        ? parseWorkflowCustomFields(currentWorkflow.custom_fields_config)
        : [],
      source_workflow_id: currentWorkflow.id,
    };

    await PositionService.createPosition(requestData);
    navigate('/company/positions');
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error && !currentWorkflow) {
    return (
      <div className="p-6">
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      </div>
    );
  }

  if (!currentWorkflow) {
    return (
      <div className="p-6">
        <Alert variant="destructive">
          <AlertDescription>No workflow available. Please select a workflow first.</AlertDescription>
        </Alert>
      </div>
    );
  }

  return (
    <div className="p-6">
      <PositionFormTabs
        mode="create"
        workflow={currentWorkflow}
        onSave={handleSave}
        isLoading={loading}
        canEditBudget={true}
      />
    </div>
  );
}

// Helper function to parse workflow custom fields config into CustomFieldDefinition[]
function parseWorkflowCustomFields(config: Record<string, unknown>): import('../../types/position').CustomFieldDefinition[] {
  const fields: import('../../types/position').CustomFieldDefinition[] = [];

  const fieldsConfig = (config.fields || {}) as Record<string, unknown>;
  const fieldLabels = (config.field_labels || {}) as Record<string, string>;
  const fieldTypes = (config.field_types || {}) as Record<string, string>;
  const fieldRequired = (config.field_required || {}) as Record<string, boolean>;
  const fieldCandidateVisibility = (config.field_candidate_visibility || {}) as Record<string, boolean>;

  let sortOrder = 0;
  for (const fieldKey in fieldsConfig) {
    const fieldConfig = fieldsConfig[fieldKey] as Record<string, unknown> | undefined;

    fields.push({
      field_key: fieldKey,
      label: fieldLabels[fieldKey] || (fieldConfig?.label as string) || fieldKey,
      field_type: (fieldTypes[fieldKey] || (fieldConfig?.type as string) || 'TEXT').toUpperCase() as 'TEXT' | 'NUMBER' | 'SELECT' | 'MULTISELECT' | 'DATE' | 'BOOLEAN' | 'URL',
      options: (fieldConfig?.options as string[]) || null,
      is_required: fieldRequired[fieldKey] || (fieldConfig?.required as boolean) || false,
      candidate_visible: fieldCandidateVisibility[fieldKey] || false,
      validation_rules: (fieldConfig?.validation as Record<string, unknown>) || null,
      sort_order: sortOrder++,
      is_active: true,
    });
  }

  return fields;
}
