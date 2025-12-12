import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { PositionService } from '../../services/positionService';
import { companyWorkflowService } from '../../services/companyWorkflowService';
import { EntityCustomizationService } from '../../services/entityCustomizationService';
import type {
  UpdatePositionRequest,
  Position,
  JobPositionWorkflow,
  JobPositionWorkflowStage,
  CustomFieldDefinition,
} from '../../types/position';
import type { WorkflowStage } from '../../types/workflow';
import { PositionFormTabs } from '../../components/jobPosition/form';
import { Alert, AlertDescription } from '@/components/ui/alert';

// Helper to map workflow field types to position field types
const mapFieldType = (fieldType: string): CustomFieldDefinition['field_type'] => {
  const typeMap: Record<string, CustomFieldDefinition['field_type']> = {
    'TEXT': 'TEXT',
    'TEXTAREA': 'TEXT',
    'NUMBER': 'NUMBER',
    'CURRENCY': 'NUMBER',
    'DATE': 'DATE',
    'DROPDOWN': 'SELECT',
    'MULTI_SELECT': 'MULTISELECT',
    'RADIO': 'SELECT',
    'CHECKBOX': 'BOOLEAN',
    'FILE': 'TEXT',
    'URL': 'URL',
    'EMAIL': 'TEXT',
    'PHONE': 'TEXT',
  };
  return typeMap[fieldType] || 'TEXT';
};

// Load custom fields from workflow that are visible to candidates in ANY stage
const loadCandidateVisibleFields = async (
  workflowId: string,
  stages: WorkflowStage[]
): Promise<CustomFieldDefinition[]> => {
  try {
    // Load all custom fields for the workflow using EntityCustomizationService
    const customFields = await EntityCustomizationService.listFieldsByEntity('Workflow', workflowId);

    console.log('Custom fields from workflow:', customFields);
    console.log('Stages with field_properties_config:', stages.map(s => ({
      id: s.id,
      name: s.name,
      field_properties_config: s.field_properties_config
    })));

    if (!customFields || customFields.length === 0) {
      return [];
    }

    // Check which fields are visible to candidates in at least one stage
    const candidateVisibleFields: CustomFieldDefinition[] = [];

    for (const field of customFields) {
      // Check if this field has visible_candidate: true in ANY stage
      // field_properties_config uses field.id as key
      let isVisibleToCandidate = false;
      let isRequired = false;

      for (const stage of stages) {
        // Try both field.id and field.field_key as keys
        const fieldPropsById = stage.field_properties_config?.[field.id];
        const fieldPropsByKey = stage.field_properties_config?.[field.field_key];
        const fieldProps = fieldPropsById || fieldPropsByKey;

        console.log(`Checking field ${field.id}/${field.field_key} in stage ${stage.name}:`, fieldProps);

        if (fieldProps?.visible_candidate) {
          isVisibleToCandidate = true;
          // If required in any stage where it's visible, mark as required
          if (fieldProps.is_required) {
            isRequired = true;
          }
        }
      }

      if (isVisibleToCandidate) {
        candidateVisibleFields.push({
          field_key: field.field_key,
          label: field.field_name,
          field_type: mapFieldType(field.field_type),
          options: field.field_config?.options || null,
          is_required: isRequired,
          candidate_visible: true,
          validation_rules: null,
          sort_order: field.order_index,
          is_active: true,
        });
      }
    }

    // Sort by sort_order
    candidateVisibleFields.sort((a, b) => a.sort_order - b.sort_order);

    console.log('Candidate visible fields result:', candidateVisibleFields);
    return candidateVisibleFields;
  } catch (err) {
    console.error('Error loading candidate visible fields:', err);
    return [];
  }
};

export default function EditPositionPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [position, setPosition] = useState<Position | null>(null);
  const [workflow, setWorkflow] = useState<JobPositionWorkflow | null>(null);

  useEffect(() => {
    if (id) {
      loadPosition();
    }
  }, [id]);

  const loadPosition = async () => {
    if (!id) return;

    try {
      setLoading(true);
      setError(null);

      // Load position
      let positionData = await PositionService.getPositionById(id);

      // Load workflow if available
      if (positionData.job_position_workflow_id) {
        try {
          const workflowData = await PositionService.getWorkflow(
            positionData.job_position_workflow_id
          );

          // Load stages with stage_type from the stages endpoint
          const stagesData = await companyWorkflowService.listStagesByWorkflow(
            positionData.job_position_workflow_id
          );

          // Load custom fields from ALL RECRUITMENT workflows (phase_workflows)
          // and filter those visible to candidates
          let customFieldsConfig: CustomFieldDefinition[] = [];
          if (positionData.phase_workflows && Object.keys(positionData.phase_workflows).length > 0) {
            // Get all unique workflow IDs from phase_workflows
            const recruitmentWorkflowIds = [...new Set(Object.values(positionData.phase_workflows))];
            console.log('Recruitment workflow IDs from phase_workflows:', recruitmentWorkflowIds);

            // Load custom fields from each recruitment workflow
            const allFields: CustomFieldDefinition[] = [];
            const seenFieldKeys = new Set<string>();

            for (const workflowId of recruitmentWorkflowIds) {
              try {
                // Load stages from the recruitment workflow
                const recruitmentStages = await companyWorkflowService.listStagesByWorkflow(workflowId);
                const fields = await loadCandidateVisibleFields(workflowId, recruitmentStages);

                // Add only unique fields (by field_key)
                for (const field of fields) {
                  if (!seenFieldKeys.has(field.field_key)) {
                    seenFieldKeys.add(field.field_key);
                    allFields.push(field);
                  }
                }
              } catch (err) {
                console.error(`Error loading fields from workflow ${workflowId}:`, err);
              }
            }

            customFieldsConfig = allFields;
          }

          console.log('Loaded candidate visible fields:', customFieldsConfig);

          // Update position with custom fields config if not already set
          if (customFieldsConfig.length > 0) {
            positionData = {
              ...positionData,
              custom_fields_config: customFieldsConfig,
            };
          }

          // Map stages to JobPositionWorkflowStage format
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

          setWorkflow({
            ...workflowData,
            stages: mappedStages,
          });
        } catch (err) {
          console.error('Error loading workflow:', err);
        }
      }

      // Set position after all data is loaded
      setPosition(positionData);
    } catch (err: unknown) {
      console.error('Error loading position:', err);
      const errorMessage = err instanceof Error ? err.message : 'Failed to load position';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async (data: UpdatePositionRequest) => {
    if (!id) {
      throw new Error('Position ID not found');
    }

    await PositionService.updatePosition(id, data);
    navigate(`/company/positions/${id}`);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error && !position) {
    return (
      <div className="p-6">
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      </div>
    );
  }

  if (!workflow) {
    return (
      <div className="p-6">
        <Alert variant="destructive">
          <AlertDescription>No workflow available for this position.</AlertDescription>
        </Alert>
      </div>
    );
  }

  return (
    <div className="p-6">
      {error && (
        <Alert variant="destructive" className="mb-4">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      <PositionFormTabs
        mode="edit"
        position={position}
        workflow={workflow}
        onSave={handleSave}
        isLoading={loading}
        canEditBudget={true}
      />
    </div>
  );
}
