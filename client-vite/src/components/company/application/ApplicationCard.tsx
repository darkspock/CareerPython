/**
 * ApplicationCard Component
 * Phase 5: Displays candidate application with deadline and task status
 */

import React from 'react';
import { Clock, AlertCircle, CheckCircle, PauseCircle, Circle } from 'lucide-react';
import type { CandidateApplication } from '../../../types/candidateApplication';
import {
  getTaskStatusLabel,
  getTaskStatusColor,
  getApplicationStatusLabel,
  getApplicationStatusColor,
  isDeadlinePassed,
  formatDeadline,
  TaskStatus
} from '../../../types/candidateApplication';

interface ApplicationCardProps {
  application: CandidateApplication;
  candidateName?: string;
  positionTitle?: string;
  onViewDetails?: () => void;
  onMoveStage?: () => void;
  showDeadline?: boolean;
  showTaskStatus?: boolean;
}

export const ApplicationCard: React.FC<ApplicationCardProps> = ({
  application,
  candidateName = 'Unknown Candidate',
  positionTitle = 'Unknown Position',
  onViewDetails,
  onMoveStage,
  showDeadline = true,
  showTaskStatus = true
}) => {
  const deadlinePassed = isDeadlinePassed(application.stage_deadline);

  const getTaskStatusIcon = (status: TaskStatus) => {
    switch (status) {
      case TaskStatus.PENDING:
        return <Circle className="w-4 h-4" />;
      case TaskStatus.IN_PROGRESS:
        return <PauseCircle className="w-4 h-4" />;
      case TaskStatus.COMPLETED:
        return <CheckCircle className="w-4 h-4" />;
      case TaskStatus.BLOCKED:
        return <AlertCircle className="w-4 h-4" />;
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 hover:shadow-md transition-shadow">
      {/* Header */}
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-gray-900">{candidateName}</h3>
          <p className="text-sm text-gray-600">{positionTitle}</p>
        </div>

        {/* Application Status Badge */}
        <span className={`px-2 py-1 text-xs font-medium rounded-full ${getApplicationStatusColor(application.application_status)}`}>
          {getApplicationStatusLabel(application.application_status)}
        </span>
      </div>

      {/* Deadline and Task Status Row */}
      {(showDeadline || showTaskStatus) && (
        <div className="flex items-center gap-4 mb-3">
          {/* Deadline Badge */}
          {showDeadline && application.stage_deadline && (
            <div className={`flex items-center gap-1 text-sm ${deadlinePassed ? 'text-red-600' : 'text-gray-600'}`}>
              <Clock className="w-4 h-4" />
              <span className={deadlinePassed ? 'font-semibold' : ''}>
                {formatDeadline(application.stage_deadline)}
              </span>
              {deadlinePassed && (
                <AlertCircle className="w-4 h-4 text-red-600" />
              )}
            </div>
          )}

          {/* Task Status Badge */}
          {showTaskStatus && (
            <div className="flex items-center gap-1.5">
              <div className={`flex items-center gap-1 px-2 py-1 text-xs font-medium rounded-full ${getTaskStatusColor(application.task_status)}`}>
                {getTaskStatusIcon(application.task_status)}
                <span>{getTaskStatusLabel(application.task_status)}</span>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Metadata */}
      <div className="text-xs text-gray-500 mb-3">
        <p>Applied: {new Date(application.applied_at).toLocaleDateString()}</p>
        {application.stage_entered_at && (
          <p>Current stage since: {new Date(application.stage_entered_at).toLocaleDateString()}</p>
        )}
      </div>

      {/* Notes Preview */}
      {application.notes && (
        <div className="text-sm text-gray-600 mb-3 line-clamp-2">
          {application.notes}
        </div>
      )}

      {/* Actions */}
      <div className="flex items-center gap-2 pt-3 border-t border-gray-100">
        {onViewDetails && (
          <button
            onClick={onViewDetails}
            className="flex-1 px-3 py-2 text-sm font-medium text-blue-600 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors"
          >
            View Details
          </button>
        )}
        {onMoveStage && (
          <button
            onClick={onMoveStage}
            className="flex-1 px-3 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
          >
            Move Stage
          </button>
        )}
      </div>

      {/* Deadline Warning */}
      {deadlinePassed && (
        <div className="mt-3 flex items-center gap-2 p-2 bg-red-50 border border-red-200 rounded-lg">
          <AlertCircle className="w-4 h-4 text-red-600 flex-shrink-0" />
          <span className="text-xs text-red-700">
            This application has passed its deadline and requires immediate attention.
          </span>
        </div>
      )}
    </div>
  );
};

export default ApplicationCard;
