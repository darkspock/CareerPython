// Phase 5: Candidate Application types with workflow stage tracking

export const ApplicationStatus = {
  APPLIED: 'applied',
  REVIEWING: 'reviewing',
  INTERVIEWED: 'interviewed',
  ACCEPTED: 'accepted',
  REJECTED: 'rejected',
  WITHDRAWN: 'withdrawn'
} as const;
export type ApplicationStatus = typeof ApplicationStatus[keyof typeof ApplicationStatus];

export const TaskStatus = {
  PENDING: 'pending',
  IN_PROGRESS: 'in_progress',
  COMPLETED: 'completed',
  BLOCKED: 'blocked'
} as const;
export type TaskStatus = typeof TaskStatus[keyof typeof TaskStatus];

export interface CandidateApplication {
  id: string;
  candidate_id: string;
  job_position_id: string;
  application_status: ApplicationStatus;
  applied_at: string;
  updated_at?: string;
  notes?: string;
  // Phase 5: Workflow stage tracking fields
  current_stage_id?: string;
  stage_entered_at?: string;
  stage_deadline?: string;
  task_status: TaskStatus;
  // Phase 12: Phase tracking field
  phase_id?: string;
}

export interface PermissionCheckResponse {
  can_process: boolean;
  application_id: string;
  user_id: string;
}

export interface ApplicationHistoryEntry {
  id: string;
  application_id: string;
  from_stage_id?: string;
  to_stage_id: string;
  changed_by: string;
  changed_at: string;
  notes?: string;
}

// Helper functions
export const getTaskStatusLabel = (status: TaskStatus): string => {
  const labels: Record<TaskStatus, string> = {
    [TaskStatus.PENDING]: 'Pending',
    [TaskStatus.IN_PROGRESS]: 'In Progress',
    [TaskStatus.COMPLETED]: 'Completed',
    [TaskStatus.BLOCKED]: 'Blocked'
  };
  return labels[status];
};

export const getTaskStatusColor = (status: TaskStatus): string => {
  const colors: Record<TaskStatus, string> = {
    [TaskStatus.PENDING]: 'bg-gray-100 text-gray-800',
    [TaskStatus.IN_PROGRESS]: 'bg-blue-100 text-blue-800',
    [TaskStatus.COMPLETED]: 'bg-green-100 text-green-800',
    [TaskStatus.BLOCKED]: 'bg-red-100 text-red-800'
  };
  return colors[status];
};

export const getApplicationStatusLabel = (status: ApplicationStatus): string => {
  const labels: Record<ApplicationStatus, string> = {
    [ApplicationStatus.APPLIED]: 'Applied',
    [ApplicationStatus.REVIEWING]: 'Under Review',
    [ApplicationStatus.INTERVIEWED]: 'Interviewed',
    [ApplicationStatus.ACCEPTED]: 'Accepted',
    [ApplicationStatus.REJECTED]: 'Rejected',
    [ApplicationStatus.WITHDRAWN]: 'Withdrawn'
  };
  return labels[status];
};

export const getApplicationStatusColor = (status: ApplicationStatus): string => {
  const colors: Record<ApplicationStatus, string> = {
    [ApplicationStatus.APPLIED]: 'bg-blue-100 text-blue-800',
    [ApplicationStatus.REVIEWING]: 'bg-yellow-100 text-yellow-800',
    [ApplicationStatus.INTERVIEWED]: 'bg-purple-100 text-purple-800',
    [ApplicationStatus.ACCEPTED]: 'bg-green-100 text-green-800',
    [ApplicationStatus.REJECTED]: 'bg-red-100 text-red-800',
    [ApplicationStatus.WITHDRAWN]: 'bg-gray-100 text-gray-800'
  };
  return colors[status];
};

export const isDeadlinePassed = (deadline?: string): boolean => {
  if (!deadline) return false;
  return new Date(deadline) < new Date();
};

export const formatDeadline = (deadline?: string): string => {
  if (!deadline) return 'No deadline';

  const deadlineDate = new Date(deadline);
  const now = new Date();
  const diffMs = deadlineDate.getTime() - now.getTime();
  const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
  const diffDays = Math.floor(diffHours / 24);

  if (diffMs < 0) {
    return 'Overdue';
  } else if (diffHours < 24) {
    return `${diffHours}h remaining`;
  } else if (diffDays === 1) {
    return '1 day remaining';
  } else {
    return `${diffDays} days remaining`;
  }
};
