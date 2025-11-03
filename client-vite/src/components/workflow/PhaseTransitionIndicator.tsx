/**
 * PhaseTransitionIndicator Component
 * Phase 12: Visual indicator for automatic phase transitions in workflows
 */

import { ArrowRight, CheckCircle, XCircle } from 'lucide-react';
import { useEffect, useState } from 'react';
import { phaseService } from '../../services/phaseService';
import type { Phase } from '../../types/phase';
import type { WorkflowStage } from '../../types/workflow';

interface PhaseTransitionIndicatorProps {
  stage: WorkflowStage;
  companyId: string;
  currentPhaseId?: string;
}

export function PhaseTransitionIndicator({
  stage,
  companyId,
  currentPhaseId,
}: PhaseTransitionIndicatorProps) {
  const [targetPhase, setTargetPhase] = useState<Phase | null>(null);
  const [currentPhase, setCurrentPhase] = useState<Phase | null>(null);
  const [loading, setLoading] = useState(false);

  // Only show for success or fail stages with next_phase_id
  const hasTransition =
    stage.next_phase_id &&
    (stage.stage_type === 'success' || stage.stage_type === 'fail');

  useEffect(() => {
    if (!hasTransition) return;

    const loadPhases = async () => {
      try {
        setLoading(true);

        // Load target phase
        if (stage.next_phase_id) {
          const target = await phaseService.getPhase(companyId, stage.next_phase_id);
          setTargetPhase(target);
        }

        // Load current phase
        if (currentPhaseId) {
          const current = await phaseService.getPhase(companyId, currentPhaseId);
          setCurrentPhase(current);
        }
      } catch (error) {
        console.error('Error loading phases for transition indicator:', error);
      } finally {
        setLoading(false);
      }
    };

    loadPhases();
  }, [stage.next_phase_id, currentPhaseId, companyId, hasTransition]);

  if (!hasTransition) {
    return null;
  }

  if (loading) {
    return (
      <div className="flex items-center gap-2 mt-2 text-xs text-gray-500">
        <div className="animate-pulse">Loading phase transition...</div>
      </div>
    );
  }

  const isSuccess = stage.stage_type === 'success';
  const bgColor = isSuccess ? 'bg-green-50' : 'bg-red-50';
  const borderColor = isSuccess ? 'border-green-200' : 'border-red-200';
  const textColor = isSuccess ? 'text-green-800' : 'text-red-800';
  const Icon = isSuccess ? CheckCircle : XCircle;

  return (
    <div className={`mt-3 p-3 rounded-lg border ${bgColor} ${borderColor}`}>
      <div className="flex items-center gap-2">
        <Icon className={`w-4 h-4 ${textColor}`} />
        <span className={`text-xs font-medium ${textColor}`}>
          Automatic Phase Transition
        </span>
      </div>

      <div className="mt-2 flex items-center gap-2 text-xs">
        {currentPhase && (
          <>
            <span className="px-2 py-1 bg-white rounded border font-medium">
              {currentPhase.name}
            </span>
            <ArrowRight className="w-3 h-3 text-gray-400" />
          </>
        )}
        <span className="px-2 py-1 bg-white rounded border font-medium text-blue-700">
          {targetPhase?.name || 'Next Phase'}
        </span>
      </div>

      <p className={`mt-2 text-xs ${textColor}`}>
        {isSuccess
          ? 'Candidates will automatically move to the next phase when reaching this stage'
          : 'Candidates marked as failed will be moved to the specified phase'}
      </p>
    </div>
  );
}
