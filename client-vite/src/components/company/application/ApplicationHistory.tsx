/**
 * ApplicationHistory Component
 * Phase 5: Timeline showing stage changes and application history
 */

import React from 'react';
import { Clock, ArrowRight, User, CheckCircle, XCircle, AlertCircle } from 'lucide-react';
import type { ApplicationHistoryEntry } from '../../../types/candidateApplication';

interface ApplicationHistoryProps {
  history: ApplicationHistoryEntry[];
  currentStageId?: string;
  getStage Name?: (stageId: string) => string;
  getUserName?: (userId: string) => string;
  className?: string;
}

export const ApplicationHistory: React.FC<ApplicationHistoryProps> = ({
  history,
  currentStageId,
  getStageName = (id) => `Stage ${id.substring(0, 8)}`,
  getUserName = (id) => `User ${id.substring(0, 8)}`,
  className = ''
}) => {
  const formatTimestamp = (timestamp: string): string => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    const diffDays = Math.floor(diffHours / 24);

    if (diffHours < 1) {
      return 'Just now';
    } else if (diffHours < 24) {
      return `${diffHours}h ago`;
    } else if (diffDays === 1) {
      return 'Yesterday';
    } else if (diffDays < 7) {
      return `${diffDays} days ago`;
    } else {
      return date.toLocaleDateString();
    }
  };

  const getTimeInStage = (entryIndex: number): string | null => {
    if (entryIndex >= history.length - 1) return null;

    const currentEntry = history[entryIndex];
    const nextEntry = history[entryIndex + 1];

    const currentTime = new Date(currentEntry.changed_at);
    const nextTime = new Date(nextEntry.changed_at);
    const diffMs = nextTime.getTime() - currentTime.getTime();
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    const diffDays = Math.floor(diffHours / 24);

    if (diffDays > 0) {
      return `${diffDays} day${diffDays > 1 ? 's' : ''}`;
    } else if (diffHours > 0) {
      return `${diffHours} hour${diffHours > 1 ? 's' : ''}`;
    } else {
      return '< 1 hour';
    }
  };

  if (history.length === 0) {
    return (
      <div className={`bg-gray-50 rounded-lg p-6 text-center ${className}`}>
        <Clock className="w-8 h-8 text-gray-400 mx-auto mb-2" />
        <p className="text-gray-600">No history available yet</p>
      </div>
    );
  }

  return (
    <div className={`bg-white rounded-lg shadow-sm border border-gray-200 ${className}`}>
      {/* Header */}
      <div className="px-6 py-4 border-b border-gray-200">
        <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
          <Clock className="w-5 h-5" />
          Application History
        </h3>
        <p className="text-sm text-gray-600 mt-1">
          Timeline of stage transitions and status changes
        </p>
      </div>

      {/* Timeline */}
      <div className="p-6">
        <div className="space-y-6">
          {history.map((entry, index) => {
            const isCurrentStage = entry.to_stage_id === currentStageId;
            const timeInStage = getTimeInStage(index);
            const isFirst = index === 0;
            const isLast = index === history.length - 1;

            return (
              <div key={entry.id} className="relative">
                {/* Timeline Line */}
                {!isLast && (
                  <div className="absolute left-4 top-10 bottom-0 w-0.5 bg-gray-200"></div>
                )}

                <div className="flex gap-4">
                  {/* Timeline Dot */}
                  <div className={`
                    relative z-10 flex items-center justify-center w-8 h-8 rounded-full flex-shrink-0
                    ${isCurrentStage ? 'bg-blue-100 ring-4 ring-blue-50' : 'bg-gray-100'}
                  `}>
                    {isFirst ? (
                      <CheckCircle className={`w-5 h-5 ${isCurrentStage ? 'text-blue-600' : 'text-gray-600'}`} />
                    ) : (
                      <ArrowRight className={`w-5 h-5 ${isCurrentStage ? 'text-blue-600' : 'text-gray-600'}`} />
                    )}
                  </div>

                  {/* Content */}
                  <div className="flex-1 pb-6">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        {/* Stage Transition */}
                        <div className="flex items-center gap-2 mb-1">
                          {entry.from_stage_id && (
                            <>
                              <span className="text-sm text-gray-600">
                                {getStageName(entry.from_stage_id)}
                              </span>
                              <ArrowRight className="w-4 h-4 text-gray-400" />
                            </>
                          )}
                          <span className={`text-sm font-medium ${isCurrentStage ? 'text-blue-600' : 'text-gray-900'}`}>
                            {getStageName(entry.to_stage_id)}
                          </span>
                          {isCurrentStage && (
                            <span className="px-2 py-0.5 text-xs font-medium text-blue-600 bg-blue-50 rounded-full">
                              Current
                            </span>
                          )}
                        </div>

                        {/* User and Time */}
                        <div className="flex items-center gap-3 text-xs text-gray-500 mb-2">
                          <div className="flex items-center gap-1">
                            <User className="w-3 h-3" />
                            <span>{getUserName(entry.changed_by)}</span>
                          </div>
                          <div className="flex items-center gap-1">
                            <Clock className="w-3 h-3" />
                            <span>{formatTimestamp(entry.changed_at)}</span>
                          </div>
                        </div>

                        {/* Time in Stage */}
                        {timeInStage && (
                          <div className="text-xs text-gray-500 mb-2">
                            Time in stage: {timeInStage}
                          </div>
                        )}

                        {/* Notes */}
                        {entry.notes && (
                          <div className="mt-2 p-2 bg-gray-50 rounded text-sm text-gray-700">
                            {entry.notes}
                          </div>
                        )}
                      </div>

                      {/* Status Indicator */}
                      <div>
                        {isCurrentStage && (
                          <div className="flex items-center gap-1 text-xs text-blue-600">
                            <div className="w-2 h-2 rounded-full bg-blue-600 animate-pulse"></div>
                            <span>Active</span>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Summary Footer */}
      <div className="px-6 py-4 bg-gray-50 border-t border-gray-200 rounded-b-lg">
        <div className="flex items-center justify-between text-sm">
          <div className="text-gray-600">
            <span className="font-medium">{history.length}</span> stage transition{history.length !== 1 ? 's' : ''}
          </div>
          {history.length > 0 && (
            <div className="text-gray-600">
              Started {formatTimestamp(history[0].changed_at)}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ApplicationHistory;
