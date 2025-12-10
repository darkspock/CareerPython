/**
 * PositionActionButtons Component
 * Displays available actions based on position status
 */
import React, { useState } from 'react';
import {
  Send,
  CheckCircle,
  XCircle,
  Rocket,
  Pause,
  Play,
  Archive,
  Copy,
  RotateCcw,
  X
} from 'lucide-react';
import {
  JobPositionStatus,
  getAvailableTransitions,
  ClosedReason
} from '../../../types/position';
import { ClosePositionModal } from './ClosePositionModal';
import { RejectPositionModal } from './RejectPositionModal';

interface PositionActionButtonsProps {
  positionId: string;
  positionTitle: string;
  status: JobPositionStatus | string;
  onRequestApproval?: () => Promise<void>;
  onApprove?: () => Promise<void>;
  onReject?: (reason: string) => Promise<void>;
  onPublish?: () => Promise<void>;
  onHold?: () => Promise<void>;
  onResume?: () => Promise<void>;
  onClose?: (reason: ClosedReason, note?: string) => Promise<void>;
  onArchive?: () => Promise<void>;
  onRevertToDraft?: () => Promise<void>;
  onClone?: () => Promise<void>;
  isLoading?: boolean;
  className?: string;
  layout?: 'horizontal' | 'vertical';
  size?: 'sm' | 'md' | 'lg';
}

export const PositionActionButtons: React.FC<PositionActionButtonsProps> = ({
  positionId: _positionId,
  positionTitle,
  status,
  onRequestApproval,
  onApprove,
  onReject,
  onPublish,
  onHold,
  onResume,
  onClose,
  onArchive,
  onRevertToDraft,
  onClone,
  isLoading = false,
  className = '',
  layout = 'horizontal',
  size = 'md'
}) => {
  const [showCloseModal, setShowCloseModal] = useState(false);
  const [showRejectModal, setShowRejectModal] = useState(false);
  const [actionLoading, setActionLoading] = useState<string | null>(null);

  const availableTransitions = getAvailableTransitions(status);

  const handleAction = async (action: () => Promise<void>, actionName: string) => {
    setActionLoading(actionName);
    try {
      await action();
    } finally {
      setActionLoading(null);
    }
  };

  const sizeClasses = {
    sm: 'px-2.5 py-1.5 text-xs',
    md: 'px-3 py-2 text-sm',
    lg: 'px-4 py-2.5 text-base'
  };

  const iconSizes = {
    sm: 14,
    md: 16,
    lg: 18
  };

  const buttonBase = `inline-flex items-center gap-1.5 font-medium rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed ${sizeClasses[size]}`;

  const buttons: React.ReactNode[] = [];

  // Request Approval (DRAFT → PENDING_APPROVAL)
  if (
    status === JobPositionStatus.DRAFT &&
    availableTransitions.includes(JobPositionStatus.PENDING_APPROVAL) &&
    onRequestApproval
  ) {
    buttons.push(
      <button
        key="request-approval"
        onClick={() => handleAction(onRequestApproval, 'request-approval')}
        disabled={isLoading || actionLoading !== null}
        className={`${buttonBase} bg-yellow-50 text-yellow-700 hover:bg-yellow-100 border border-yellow-200`}
      >
        <Send size={iconSizes[size]} />
        Request Approval
      </button>
    );
  }

  // Publish (DRAFT → PUBLISHED quick mode, or APPROVED → PUBLISHED)
  if (
    availableTransitions.includes(JobPositionStatus.PUBLISHED) &&
    onPublish
  ) {
    buttons.push(
      <button
        key="publish"
        onClick={() => handleAction(onPublish, 'publish')}
        disabled={isLoading || actionLoading !== null}
        className={`${buttonBase} bg-green-600 text-white hover:bg-green-700`}
      >
        <Rocket size={iconSizes[size]} />
        Publish
      </button>
    );
  }

  // Approve (PENDING_APPROVAL → APPROVED)
  if (
    status === JobPositionStatus.PENDING_APPROVAL &&
    availableTransitions.includes(JobPositionStatus.APPROVED) &&
    onApprove
  ) {
    buttons.push(
      <button
        key="approve"
        onClick={() => handleAction(onApprove, 'approve')}
        disabled={isLoading || actionLoading !== null}
        className={`${buttonBase} bg-blue-600 text-white hover:bg-blue-700`}
      >
        <CheckCircle size={iconSizes[size]} />
        Approve
      </button>
    );
  }

  // Reject (PENDING_APPROVAL → REJECTED)
  if (
    status === JobPositionStatus.PENDING_APPROVAL &&
    availableTransitions.includes(JobPositionStatus.REJECTED) &&
    onReject
  ) {
    buttons.push(
      <button
        key="reject"
        onClick={() => setShowRejectModal(true)}
        disabled={isLoading || actionLoading !== null}
        className={`${buttonBase} bg-red-50 text-red-700 hover:bg-red-100 border border-red-200`}
      >
        <XCircle size={iconSizes[size]} />
        Reject
      </button>
    );
  }

  // Hold (PUBLISHED → ON_HOLD)
  if (
    status === JobPositionStatus.PUBLISHED &&
    availableTransitions.includes(JobPositionStatus.ON_HOLD) &&
    onHold
  ) {
    buttons.push(
      <button
        key="hold"
        onClick={() => handleAction(onHold, 'hold')}
        disabled={isLoading || actionLoading !== null}
        className={`${buttonBase} bg-orange-50 text-orange-700 hover:bg-orange-100 border border-orange-200`}
      >
        <Pause size={iconSizes[size]} />
        Put on Hold
      </button>
    );
  }

  // Resume (ON_HOLD → PUBLISHED)
  if (
    status === JobPositionStatus.ON_HOLD &&
    availableTransitions.includes(JobPositionStatus.PUBLISHED) &&
    onResume
  ) {
    buttons.push(
      <button
        key="resume"
        onClick={() => handleAction(onResume, 'resume')}
        disabled={isLoading || actionLoading !== null}
        className={`${buttonBase} bg-green-600 text-white hover:bg-green-700`}
      >
        <Play size={iconSizes[size]} />
        Resume
      </button>
    );
  }

  // Close (PUBLISHED/ON_HOLD → CLOSED)
  if (
    availableTransitions.includes(JobPositionStatus.CLOSED) &&
    onClose
  ) {
    buttons.push(
      <button
        key="close"
        onClick={() => setShowCloseModal(true)}
        disabled={isLoading || actionLoading !== null}
        className={`${buttonBase} bg-gray-50 text-gray-700 hover:bg-gray-100 border border-gray-200`}
      >
        <X size={iconSizes[size]} />
        Close
      </button>
    );
  }

  // Archive (CLOSED → ARCHIVED)
  if (
    status === JobPositionStatus.CLOSED &&
    availableTransitions.includes(JobPositionStatus.ARCHIVED) &&
    onArchive
  ) {
    buttons.push(
      <button
        key="archive"
        onClick={() => handleAction(onArchive, 'archive')}
        disabled={isLoading || actionLoading !== null}
        className={`${buttonBase} bg-purple-50 text-purple-700 hover:bg-purple-100 border border-purple-200`}
      >
        <Archive size={iconSizes[size]} />
        Archive
      </button>
    );
  }

  // Revert to Draft (REJECTED/APPROVED/CLOSED → DRAFT)
  if (
    availableTransitions.includes(JobPositionStatus.DRAFT) &&
    status !== JobPositionStatus.DRAFT &&
    onRevertToDraft
  ) {
    buttons.push(
      <button
        key="revert"
        onClick={() => handleAction(onRevertToDraft, 'revert')}
        disabled={isLoading || actionLoading !== null}
        className={`${buttonBase} bg-gray-50 text-gray-700 hover:bg-gray-100 border border-gray-200`}
      >
        <RotateCcw size={iconSizes[size]} />
        Revert to Draft
      </button>
    );
  }

  // Clone (always available)
  if (onClone) {
    buttons.push(
      <button
        key="clone"
        onClick={() => handleAction(onClone, 'clone')}
        disabled={isLoading || actionLoading !== null}
        className={`${buttonBase} bg-indigo-50 text-indigo-700 hover:bg-indigo-100 border border-indigo-200`}
      >
        <Copy size={iconSizes[size]} />
        Clone
      </button>
    );
  }

  const layoutClasses = layout === 'vertical' ? 'flex-col' : 'flex-row flex-wrap';

  return (
    <>
      <div className={`flex gap-2 ${layoutClasses} ${className}`}>
        {buttons}
      </div>

      {/* Close Modal */}
      <ClosePositionModal
        isOpen={showCloseModal}
        positionTitle={positionTitle}
        onClose={() => setShowCloseModal(false)}
        onConfirm={async (reason, note) => {
          if (onClose) {
            setActionLoading('close');
            try {
              await onClose(reason, note);
              setShowCloseModal(false);
            } finally {
              setActionLoading(null);
            }
          }
        }}
        isLoading={actionLoading === 'close'}
      />

      {/* Reject Modal */}
      <RejectPositionModal
        isOpen={showRejectModal}
        positionTitle={positionTitle}
        onClose={() => setShowRejectModal(false)}
        onConfirm={async (reason) => {
          if (onReject) {
            setActionLoading('reject');
            try {
              await onReject(reason);
              setShowRejectModal(false);
            } finally {
              setActionLoading(null);
            }
          }
        }}
        isLoading={actionLoading === 'reject'}
      />
    </>
  );
};

export default PositionActionButtons;
