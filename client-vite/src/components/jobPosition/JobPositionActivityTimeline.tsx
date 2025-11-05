/**
 * Job Position Activity Timeline Component
 * 
 * Displays a chronological timeline of activities on a job position.
 */

import React from 'react';
import { Clock, Edit, Move, TrendingUp, MessageSquare, Plus } from 'lucide-react';
import type { JobPositionActivity } from '@/types/jobPositionActivity';
import { ActivityType } from '@/types/jobPositionActivity';
// Using basic date formatting
const formatDate = (dateStr: string) => {
  const date = new Date(dateStr);
  return date.toLocaleString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
};

interface JobPositionActivityTimelineProps {
  activities: JobPositionActivity[];
  isLoading?: boolean;
}

const getActivityIcon = (activityType: string) => {
  switch (activityType) {
    case ActivityType.CREATED:
      return <Plus className="h-4 w-4" />;
    case ActivityType.EDITED:
      return <Edit className="h-4 w-4" />;
    case ActivityType.STAGE_MOVED:
      return <Move className="h-4 w-4" />;
    case ActivityType.STATUS_CHANGED:
      return <TrendingUp className="h-4 w-4" />;
    case ActivityType.COMMENT_ADDED:
      return <MessageSquare className="h-4 w-4" />;
    default:
      return <Clock className="h-4 w-4" />;
  }
};

const getActivityColor = (activityType: string) => {
  switch (activityType) {
    case ActivityType.CREATED:
      return 'bg-blue-100 text-blue-700 border-blue-200';
    case ActivityType.EDITED:
      return 'bg-green-100 text-green-700 border-green-200';
    case ActivityType.STAGE_MOVED:
      return 'bg-purple-100 text-purple-700 border-purple-200';
    case ActivityType.STATUS_CHANGED:
      return 'bg-orange-100 text-orange-700 border-orange-200';
    case ActivityType.COMMENT_ADDED:
      return 'bg-gray-100 text-gray-700 border-gray-200';
    default:
      return 'bg-gray-100 text-gray-700 border-gray-200';
  }
};

export const JobPositionActivityTimeline: React.FC<JobPositionActivityTimelineProps> = ({
  activities,
  isLoading = false,
}) => {
  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (activities.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        <Clock className="mx-auto h-12 w-12 text-gray-400 mb-3" />
        <p>No hay actividad registrada</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {activities.map((activity, index) => (
        <div key={activity.id} className="flex gap-4">
          {/* Timeline line */}
          <div className="flex flex-col items-center">
            <div
              className={`flex items-center justify-center w-8 h-8 rounded-full border-2 ${getActivityColor(
                activity.activity_type
              )}`}
            >
              {getActivityIcon(activity.activity_type)}
            </div>
            {index < activities.length - 1 && (
              <div className="w-0.5 h-full bg-gray-200 mt-2"></div>
            )}
          </div>

          {/* Activity content */}
          <div className="flex-1 pb-8">
            <div className="bg-white border border-gray-200 rounded-lg p-4">
              <p className="text-gray-900 font-medium mb-1">{activity.description}</p>
              <p className="text-xs text-gray-500">
                {formatDate(activity.created_at)}
              </p>

              {/* Metadata details (if present) */}
              {Object.keys(activity.metadata).length > 0 && (
                <div className="mt-3 pt-3 border-t border-gray-100">
                  <details className="text-xs text-gray-600">
                    <summary className="cursor-pointer hover:text-gray-900">
                      Ver detalles
                    </summary>
                    <pre className="mt-2 p-2 bg-gray-50 rounded text-xs overflow-x-auto">
                      {JSON.stringify(activity.metadata, null, 2)}
                    </pre>
                  </details>
                </div>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

