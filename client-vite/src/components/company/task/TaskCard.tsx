// Phase 6: Task Card Component
// Displays a task with enriched information including priority, deadline, and candidate details

import React, { useState } from 'react';
import { Clock, AlertCircle, User, Briefcase, PlayCircle, XCircle } from 'lucide-react';
import type {
  Task
} from '../../../types/task';
import {
  PriorityLevel,
  TaskStatus,
  getPriorityColor,
  getPriorityLabel,
  getTaskStatusColor,
  getTaskStatusLabel,
  formatDeadline,
  formatRelativeTime,
  isDeadlinePassed
} from '../../../types/task';
import { getApplicationStatusColor, getApplicationStatusLabel } from '../../../types/candidateApplication';

interface TaskCardProps {
  task: Task;
  onClaim?: (task: Task) => void;
  onUnclaim?: (task: Task) => void;
  onViewDetails?: (task: Task) => void;
  showActions?: boolean;
  isLoading?: boolean;
}

/**
 * TaskCard Component
 *
 * Displays a task card with:
 * - Priority indicator
 * - Candidate information
 * - Position title
 * - Current stage
 * - Deadline and time tracking
 * - Task status
 * - Action buttons (claim/unclaim)
 *
 * @param task - The task to display
 * @param onClaim - Callback when user claims the task
 * @param onUnclaim - Callback when user unclaims the task
 * @param onViewDetails - Callback when user clicks to view details
 * @param showActions - Whether to show action buttons (default: true)
 * @param isLoading - Whether an action is in progress
 */
export const TaskCard: React.FC<TaskCardProps> = ({
  task,
  onClaim,
  onUnclaim,
  onViewDetails,
  showActions = true,
  isLoading = false
}) => {
  const [actionInProgress, setActionInProgress] = useState(false);
  const deadlinePassed = isDeadlinePassed(task.stage_deadline);

  const handleClaim = async () => {
    if (!onClaim || actionInProgress) return;
    setActionInProgress(true);
    try {
      await onClaim(task);
    } finally {
      setActionInProgress(false);
    }
  };

  const handleUnclaim = async () => {
    if (!onUnclaim || actionInProgress) return;
    setActionInProgress(true);
    try {
      await onUnclaim(task);
    } finally {
      setActionInProgress(false);
    }
  };

  const handleViewDetails = () => {
    if (onViewDetails) {
      onViewDetails(task);
    }
  };

  const canClaim = task.task_status === TaskStatus.PENDING && task.can_user_process;
  const canUnclaim = task.task_status === TaskStatus.IN_PROGRESS && task.can_user_process;
  const loading = isLoading || actionInProgress;

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow duration-200">
      <div className="p-4">
        {/* Header: Priority and Status */}
        <div className="flex items-start justify-between mb-3">
          <div className="flex items-center gap-2">
            <span className={`px-2 py-1 text-xs font-medium rounded border ${getPriorityColor(task.priority_level as PriorityLevel)}`}>
              {getPriorityLabel(task.priority_level as PriorityLevel)} Priority
            </span>
            <span className={`px-2 py-1 text-xs font-medium rounded border ${getTaskStatusColor(task.task_status)}`}>
              {getTaskStatusLabel(task.task_status)}
            </span>
          </div>
          <span className={`px-2 py-1 text-xs font-medium rounded ${getApplicationStatusColor(task.application_status)}`}>
            {getApplicationStatusLabel(task.application_status)}
          </span>
        </div>

        {/* Candidate Information */}
        <div className="mb-3">
          <div className="flex items-center gap-2 mb-2">
            {task.candidate_photo_url ? (
              <img
                src={task.candidate_photo_url}
                alt={task.candidate_name}
                className="w-10 h-10 rounded-full object-cover"
              />
            ) : (
              <div className="w-10 h-10 rounded-full bg-gray-200 flex items-center justify-center">
                <User className="w-5 h-5 text-gray-500" />
              </div>
            )}
            <div className="flex-1 min-w-0">
              <h3 className="text-base font-semibold text-gray-900 truncate">
                {task.candidate_name}
              </h3>
              {task.candidate_email && (
                <p className="text-sm text-gray-500 truncate">{task.candidate_email}</p>
              )}
            </div>
          </div>
        </div>

        {/* Position and Stage */}
        <div className="space-y-2 mb-3">
          <div className="flex items-center gap-2 text-sm">
            <Briefcase className="w-4 h-4 text-gray-400 flex-shrink-0" />
            <span className="text-gray-700 truncate">{task.position_title}</span>
          </div>
          {task.current_stage_name && (
            <div className="flex items-center gap-2 text-sm">
              <div className="w-4 h-4 flex-shrink-0 flex items-center justify-center">
                <div className="w-2 h-2 rounded-full bg-blue-500"></div>
              </div>
              <span className="text-gray-600">{task.current_stage_name}</span>
            </div>
          )}
        </div>

        {/* Deadline and Time in Stage */}
        {(task.stage_deadline || task.stage_entered_at) && (
          <div className="border-t pt-3 mb-3 space-y-2">
            {task.stage_deadline && (
              <div className={`flex items-center gap-2 text-sm ${deadlinePassed ? 'text-red-600' : 'text-gray-600'}`}>
                <Clock className="w-4 h-4" />
                <span className="font-medium">{formatDeadline(task.stage_deadline)}</span>
              </div>
            )}
            {task.stage_entered_at && (
              <div className="flex items-center gap-2 text-sm text-gray-500">
                <div className="w-4 h-4"></div>
                <span>In stage for {task.days_in_stage} {task.days_in_stage === 1 ? 'day' : 'days'}</span>
                <span className="text-gray-400">• Applied {formatRelativeTime(task.applied_at)}</span>
              </div>
            )}
          </div>
        )}

        {/* Overdue Warning */}
        {deadlinePassed && (
          <div className="mb-3 flex items-center gap-2 p-2 bg-red-50 border border-red-200 rounded-lg">
            <AlertCircle className="w-4 h-4 text-red-600 flex-shrink-0" />
            <span className="text-xs text-red-700">
              This task is overdue and requires immediate attention
            </span>
          </div>
        )}

        {/* Priority Score Info */}
        <div className="text-xs text-gray-500 mb-3">
          Priority Score: {task.priority_score} / 150
        </div>

        {/* Action Buttons */}
        {showActions && (
          <div className="flex gap-2 border-t pt-3">
            {canClaim && onClaim && (
              <button
                onClick={handleClaim}
                disabled={loading}
                className="flex-1 flex items-center justify-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
              >
                {loading ? (
                  <span className="text-sm">Processing...</span>
                ) : (
                  <>
                    <PlayCircle className="w-4 h-4" />
                    <span className="text-sm font-medium">Claim Task</span>
                  </>
                )}
              </button>
            )}

            {canUnclaim && onUnclaim && (
              <button
                onClick={handleUnclaim}
                disabled={loading}
                className="flex-1 flex items-center justify-center gap-2 px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
              >
                {loading ? (
                  <span className="text-sm">Processing...</span>
                ) : (
                  <>
                    <XCircle className="w-4 h-4" />
                    <span className="text-sm font-medium">Release Task</span>
                  </>
                )}
              </button>
            )}

            {onViewDetails && (
              <button
                onClick={handleViewDetails}
                disabled={loading}
                className="flex items-center justify-center gap-2 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 disabled:bg-gray-100 disabled:cursor-not-allowed transition-colors"
              >
                <span className="text-sm font-medium">View Details</span>
              </button>
            )}
          </div>
        )}

        {/* No Actions Message */}
        {!task.can_user_process && showActions && (
          <div className="border-t pt-3">
            <div className="text-sm text-gray-500 text-center">
              You don't have permission to process this task
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default TaskCard;
