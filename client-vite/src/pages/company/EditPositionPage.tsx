import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { PositionService } from '../../services/positionService';
import type {
  UpdatePositionRequest,
  Position,
  JobPositionWorkflow,
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
          setWorkflow(workflowData);
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
