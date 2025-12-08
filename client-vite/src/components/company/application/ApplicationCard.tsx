/**
 * ApplicationCard Component
 * Phase 5: Displays candidate application with deadline and task status
 */

import React from 'react';
import { Clock, AlertCircle, CheckCircle, PauseCircle, Circle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
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
    <Card className="hover:shadow-md transition-shadow">
      <CardHeader>
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <CardTitle className="text-lg">{candidateName}</CardTitle>
            <p className="text-sm text-gray-600 mt-1">{positionTitle}</p>
          </div>

          {/* Application Status Badge */}
          <Badge className={getApplicationStatusColor(application.application_status)}>
            {getApplicationStatusLabel(application.application_status)}
          </Badge>
        </div>
      </CardHeader>

      <CardContent className="space-y-4">
        {/* Deadline and Task Status Row */}
        {(showDeadline || showTaskStatus) && (
          <div className="flex items-center gap-4">
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
              <Badge variant="outline" className={getTaskStatusColor(application.task_status)}>
                {getTaskStatusIcon(application.task_status)}
                <span className="ml-1">{getTaskStatusLabel(application.task_status)}</span>
              </Badge>
            )}
          </div>
        )}

        {/* Metadata */}
        <div className="text-xs text-gray-500">
          <p>Applied: {new Date(application.applied_at).toLocaleDateString()}</p>
          {application.stage_entered_at && (
            <p>Current stage since: {new Date(application.stage_entered_at).toLocaleDateString()}</p>
          )}
        </div>

        {/* Notes Preview */}
        {application.notes && (
          <div className="text-sm text-gray-600 line-clamp-2">
            {application.notes}
          </div>
        )}

        {/* Actions */}
        <div className="flex items-center gap-2 pt-3 border-t border-gray-100">
          {onViewDetails && (
            <Button
              onClick={onViewDetails}
              variant="default"
              className="flex-1"
            >
              View Details
            </Button>
          )}
          {onMoveStage && (
            <Button
              onClick={onMoveStage}
              variant="secondary"
              className="flex-1"
            >
              Move Stage
            </Button>
          )}
        </div>

        {/* Deadline Warning */}
        {deadlinePassed && (
          <Alert variant="destructive">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>
              This application has passed its deadline and requires immediate attention.
            </AlertDescription>
          </Alert>
        )}
      </CardContent>
    </Card>
  );
};

export default ApplicationCard;
