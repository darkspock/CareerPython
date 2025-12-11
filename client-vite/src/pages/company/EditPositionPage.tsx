import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { PositionService } from '../../services/positionService';
import { companyWorkflowService } from '../../services/companyWorkflowService';
import type {
  UpdatePositionRequest,
  Position,
  JobPositionWorkflow,
  JobPositionWorkflowStage,
} from '../../types/position';
import { PositionFormTabs } from '../../components/jobPosition/form';
import { Alert, AlertDescription } from '@/components/ui/alert';

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
      const positionData = await PositionService.getPositionById(id);
      setPosition(positionData);

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
