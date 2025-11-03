/**
 * StageTransitionButton Component
 * Phase 5: Button to transition application to next stage with permission check
 */

import React, { useEffect, useState } from 'react';
import { ArrowRight, Lock, AlertCircle } from 'lucide-react';
import { CandidateApplicationService } from '../../../services/candidateApplicationService';

interface StageTransitionButtonProps {
  applicationId: string;
  currentStageId?: string;
  targetStageId: string;
  targetStageName: string;
  userId: string;  // Current logged-in user
  companyId: string;  // Company of the position
  onTransition: () => void | Promise<void>;
  disabled?: boolean;
  className?: string;
}

export const StageTransitionButton: React.FC<StageTransitionButtonProps> = ({
  applicationId,
  currentStageId: _currentStageId,
  targetStageId: _targetStageId,
  targetStageName,
  userId,
  companyId,
  onTransition,
  disabled = false,
  className = ''
}) => {
  const [canProcess, setCanProcess] = useState<boolean>(false);
  const [checking, setChecking] = useState<boolean>(true);
  const [transitioning, setTransitioning] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    checkPermission();
  }, [applicationId, userId, companyId]);

  const checkPermission = async () => {
    setChecking(true);
    setError(null);

    try {
      const hasPermission = await CandidateApplicationService.canUserProcessApplication(
        applicationId,
        userId,
        companyId
      );
      setCanProcess(hasPermission);
    } catch (err) {
      console.error('Error checking permission:', err);
      setCanProcess(false);
      setError('Failed to check permissions');
    } finally {
      setChecking(false);
    }
  };

  const handleTransition = async () => {
    if (!canProcess || disabled || transitioning) return;

    setTransitioning(true);
    setError(null);

    try {
      await onTransition();
    } catch (err: any) {
      console.error('Error transitioning stage:', err);
      setError(err.message || 'Failed to transition stage');
    } finally {
      setTransitioning(false);
    }
  };

  const isDisabled = disabled || !canProcess || checking || transitioning;

  const getButtonContent = () => {
    if (checking) {
      return (
        <>
          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-current"></div>
          <span>Checking permission...</span>
        </>
      );
    }

    if (transitioning) {
      return (
        <>
          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-current"></div>
          <span>Moving to {targetStageName}...</span>
        </>
      );
    }

    if (!canProcess) {
      return (
        <>
          <Lock className="w-4 h-4" />
          <span>Move to {targetStageName}</span>
        </>
      );
    }

    return (
      <>
        <ArrowRight className="w-4 h-4" />
        <span>Move to {targetStageName}</span>
      </>
    );
  };

  const getTooltipMessage = () => {
    if (checking) return 'Checking your permissions...';
    if (!canProcess) return 'You do not have permission to move this application. You must be assigned to the current stage.';
    if (disabled) return 'This action is currently disabled';
    return `Move application to ${targetStageName}`;
  };

  return (
    <div className="relative group">
      <button
        onClick={handleTransition}
        disabled={isDisabled}
        className={`
          flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all
          ${isDisabled
            ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
            : 'bg-blue-600 text-white hover:bg-blue-700 active:bg-blue-800'
          }
          ${className}
        `}
        title={getTooltipMessage()}
      >
        {getButtonContent()}
      </button>

      {/* Tooltip */}
      <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-gray-900 text-white text-sm rounded-lg opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-10">
        {getTooltipMessage()}
        <div className="absolute top-full left-1/2 transform -translate-x-1/2 -mt-1">
          <div className="border-4 border-transparent border-t-gray-900"></div>
        </div>
      </div>

      {/* Permission Warning */}
      {!checking && !canProcess && (
        <div className="mt-2 flex items-start gap-2 p-2 bg-yellow-50 border border-yellow-200 rounded-lg text-sm">
          <AlertCircle className="w-4 h-4 text-yellow-600 flex-shrink-0 mt-0.5" />
          <div className="text-yellow-700">
            <p className="font-medium">Permission Required</p>
            <p className="text-xs mt-1">
              You must be assigned to the current workflow stage to move this application.
              Contact your administrator if you believe you should have access.
            </p>
          </div>
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="mt-2 flex items-center gap-2 p-2 bg-red-50 border border-red-200 rounded-lg text-sm">
          <AlertCircle className="w-4 h-4 text-red-600 flex-shrink-0" />
          <span className="text-red-700">{error}</span>
        </div>
      )}
    </div>
  );
};

export default StageTransitionButton;
