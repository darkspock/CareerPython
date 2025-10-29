/**
 * Stage Timeline Component
 * Phase 12: Display candidate progression through workflow stages and phases
 *
 * Note: This component currently shows current state only.
 * Once backend stage history tracking is implemented, it will display full timeline.
 */

import { CheckCircle, Circle, Clock, ArrowRight } from 'lucide-react';
import { PhaseBadge } from '../phase';
import type { CompanyCandidate } from '../../types/companyCandidate';

interface StageTimelineProps {
  candidate: CompanyCandidate;
  companyId: string;
}

interface TimelineEntry {
  id: string;
  type: 'phase' | 'stage' | 'event';
  title: string;
  description?: string;
  timestamp: string;
  status: 'completed' | 'current' | 'pending';
  phaseId?: string;
  stageId?: string;
}

export function StageTimeline({ candidate, companyId }: StageTimelineProps) {
  // Build timeline from candidate data
  // TODO: Once backend stage history endpoint is available, fetch full history
  const timeline: TimelineEntry[] = [];

  // Add candidate creation
  timeline.push({
    id: 'created',
    type: 'event',
    title: 'Candidate Added',
    description: `Added to company by ${candidate.added_by_user_id}`,
    timestamp: candidate.created_at,
    status: 'completed',
  });

  // Add invitation if applicable
  if (candidate.invited_at) {
    timeline.push({
      id: 'invited',
      type: 'event',
      title: 'Invitation Sent',
      description: 'Candidate invitation email sent',
      timestamp: candidate.invited_at,
      status: 'completed',
    });
  }

  // Add confirmation if applicable
  if (candidate.confirmed_at) {
    timeline.push({
      id: 'confirmed',
      type: 'event',
      title: 'Candidate Confirmed',
      description: 'Candidate accepted the invitation',
      timestamp: candidate.confirmed_at,
      status: 'completed',
    });
  }

  // Add current phase if available
  if (candidate.phase_id) {
    timeline.push({
      id: `phase-${candidate.phase_id}`,
      type: 'phase',
      title: 'Current Phase',
      description: 'Candidate entered this recruitment phase',
      timestamp: candidate.updated_at,
      status: 'current',
      phaseId: candidate.phase_id,
    });
  }

  // Add current stage if available
  if (candidate.current_stage_id && candidate.stage_name) {
    timeline.push({
      id: `stage-${candidate.current_stage_id}`,
      type: 'stage',
      title: candidate.stage_name,
      description: 'Current workflow stage',
      timestamp: candidate.updated_at,
      status: 'current',
      stageId: candidate.current_stage_id,
    });
  }

  // Add rejected timestamp if applicable
  if (candidate.rejected_at) {
    timeline.push({
      id: 'rejected',
      type: 'event',
      title: 'Candidate Rejected',
      description: 'Candidate was not selected for this position',
      timestamp: candidate.rejected_at,
      status: 'completed',
    });
  }

  // Add archived timestamp if applicable
  if (candidate.archived_at) {
    timeline.push({
      id: 'archived',
      type: 'event',
      title: 'Candidate Archived',
      description: 'Moved to archived status',
      timestamp: candidate.archived_at,
      status: 'completed',
    });
  }

  // Sort by timestamp
  timeline.sort((a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime());

  const getStatusIcon = (status: TimelineEntry['status']) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="w-5 h-5 text-green-600" />;
      case 'current':
        return <Clock className="w-5 h-5 text-blue-600" />;
      case 'pending':
        return <Circle className="w-5 h-5 text-gray-400" />;
    }
  };

  const getStatusColor = (status: TimelineEntry['status']) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100';
      case 'current':
        return 'bg-blue-100';
      case 'pending':
        return 'bg-gray-100';
    }
  };

  return (
    <div className="space-y-6">
      {/* Info Banner */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <p className="text-sm text-blue-800">
          <strong>Timeline Preview:</strong> This shows the candidate's current state. Full stage history tracking
          will display detailed progression through all workflow stages once backend implementation is complete.
        </p>
      </div>

      {/* Timeline */}
      <div className="relative">
        {timeline.map((entry, index) => (
          <div key={entry.id} className="relative flex gap-4 pb-8 last:pb-0">
            {/* Vertical Line */}
            {index !== timeline.length - 1 && (
              <div className="absolute left-5 top-10 bottom-0 w-0.5 bg-gray-200" />
            )}

            {/* Icon */}
            <div className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center ${getStatusColor(entry.status)}`}>
              {getStatusIcon(entry.status)}
            </div>

            {/* Content */}
            <div className="flex-1 pt-1">
              <div className="flex items-start justify-between mb-2">
                <div>
                  <h4 className="font-semibold text-gray-900">{entry.title}</h4>
                  {entry.description && (
                    <p className="text-sm text-gray-600 mt-1">{entry.description}</p>
                  )}
                </div>
                <span className="text-xs text-gray-500 whitespace-nowrap ml-4">
                  {new Date(entry.timestamp).toLocaleDateString('en-US', {
                    month: 'short',
                    day: 'numeric',
                    year: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit'
                  })}
                </span>
              </div>

              {/* Phase Badge if applicable */}
              {entry.type === 'phase' && entry.phaseId && (
                <div className="mt-2">
                  <PhaseBadge
                    phaseId={entry.phaseId}
                    companyId={companyId}
                    size="sm"
                    showIcon={true}
                  />
                </div>
              )}

              {/* Stage Badge */}
              {entry.type === 'stage' && candidate.workflow_name && (
                <div className="mt-2 flex items-center gap-2 text-sm">
                  <span className="px-2 py-1 bg-purple-100 text-purple-800 rounded text-xs font-medium">
                    {candidate.workflow_name}
                  </span>
                  <ArrowRight className="w-3 h-3 text-gray-400" />
                  <span className="px-2 py-1 bg-indigo-100 text-indigo-800 rounded text-xs font-medium">
                    {entry.title}
                  </span>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Empty State */}
      {timeline.length === 0 && (
        <div className="text-center py-12 bg-gray-50 rounded-lg">
          <Clock className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No Timeline Data</h3>
          <p className="text-gray-600">
            Timeline information will appear here as the candidate progresses through stages.
          </p>
        </div>
      )}
    </div>
  );
}
