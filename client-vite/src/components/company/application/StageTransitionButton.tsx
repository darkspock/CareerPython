/**
 * StageTransitionButton Component
 * Phase 5: Button to transition application to next stage with permission check
 */

import React, { useEffect, useState } from 'react';
import { ArrowRight, Lock, AlertCircle } from 'lucide-react';
import { CandidateApplicationService } from '../../../services/candidateApplicationService';
import { Button } from '@/components/ui/button';
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '@/components/ui/tooltip';
import { Badge } from '@/components/ui/badge';

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
    <div className="relative">
      <TooltipProvider>
        <Tooltip>
          <TooltipTrigger asChild>
            <Button
              onClick={handleTransition}
              disabled={isDisabled}
              variant={isDisabled ? 'secondary' : 'default'}
              className={className}
            >
              {getButtonContent()}
            </Button>
          </TooltipTrigger>
          <TooltipContent>
            <p>{getTooltipMessage()}</p>
          </TooltipContent>
        </Tooltip>
      </TooltipProvider>

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
        <Badge variant="destructive" className="mt-2 flex items-center gap-2 w-fit">
          <AlertCircle className="w-4 h-4" />
          <span>{error}</span>
        </Badge>
      )}
    </div>
  );
};

export default StageTransitionButton;
