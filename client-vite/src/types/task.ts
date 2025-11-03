// Phase 6: Task Management types with enriched information

import { ApplicationStatus, TaskStatus } from './candidateApplication';

// Re-export TaskStatus for convenience (as value, not type)
export { TaskStatus };

/**
 * Priority level for tasks
 */
export const PriorityLevel = {
  CRITICAL: 'critical',
  HIGH: 'high',
  MEDIUM: 'medium',
  LOW: 'low'
} as const;
export type PriorityLevel = typeof PriorityLevel[keyof typeof PriorityLevel];

/**
 * Task DTO with enriched candidate and position information
 * This extends the basic application with additional computed fields for task management
 */
export interface Task {
  // Application core fields
  application_id: string;
  candidate_id: string;
  job_position_id: string;
  application_status: ApplicationStatus;
  applied_at: string;
  updated_at?: string;

  // Workflow stage tracking
  current_stage_id?: string;
  current_stage_name?: string;
  stage_entered_at?: string;
  stage_deadline?: string;
  task_status: TaskStatus;

  // Enriched candidate information
  candidate_name: string;
  candidate_email?: string;
  candidate_photo_url?: string;

  // Enriched position information
  position_title: string;
  position_company_name?: string;

  // Priority and metadata
  priority_score: number;
  priority_level: PriorityLevel;
  days_in_stage: number;
  is_overdue: boolean;

  // Assignment information
  can_user_process: boolean;
}

/**
 * Request to claim a task
 */
export interface ClaimTaskRequest {
  application_id: string;
  user_id: string;
}

/**
 * Request to unclaim a task
 */
export interface UnclaimTaskRequest {
  application_id: string;
  user_id: string;
}

/**
 * Response from claim/unclaim operations
 */
export interface TaskActionResponse {
  message: string;
  application_id: string;
  user_id: string;
}

/**
 * Filters for task queries
 */
export interface TaskFilters {
  stage_id?: string;
  limit?: number;
}

// Helper functions

/**
 * Get CSS classes for priority level badge
 */
export const getPriorityColor = (level: PriorityLevel): string => {
  switch (level) {
    case PriorityLevel.CRITICAL:
      return 'bg-red-100 text-red-800 border-red-300';
    case PriorityLevel.HIGH:
      return 'bg-orange-100 text-orange-800 border-orange-300';
    case PriorityLevel.MEDIUM:
      return 'bg-yellow-100 text-yellow-800 border-yellow-300';
    case PriorityLevel.LOW:
      return 'bg-blue-100 text-blue-800 border-blue-300';
    default:
      return 'bg-gray-100 text-gray-800 border-gray-300';
  }
};

/**
 * Get human-readable priority label
 */
export const getPriorityLabel = (level: PriorityLevel): string => {
  switch (level) {
    case PriorityLevel.CRITICAL:
      return 'Critical';
    case PriorityLevel.HIGH:
      return 'High';
    case PriorityLevel.MEDIUM:
      return 'Medium';
    case PriorityLevel.LOW:
      return 'Low';
    default:
      return 'Unknown';
  }
};

/**
 * Get CSS classes for task status badge
 */
export const getTaskStatusColor = (status: TaskStatus): string => {
  switch (status) {
    case TaskStatus.PENDING:
      return 'bg-gray-100 text-gray-800 border-gray-300';
    case TaskStatus.IN_PROGRESS:
      return 'bg-blue-100 text-blue-800 border-blue-300';
    case TaskStatus.COMPLETED:
      return 'bg-green-100 text-green-800 border-green-300';
    case TaskStatus.BLOCKED:
      return 'bg-red-100 text-red-800 border-red-300';
    default:
      return 'bg-gray-100 text-gray-800 border-gray-300';
  }
};

/**
 * Get human-readable task status label
 */
export const getTaskStatusLabel = (status: TaskStatus): string => {
  switch (status) {
    case TaskStatus.PENDING:
      return 'Pending';
    case TaskStatus.IN_PROGRESS:
      return 'In Progress';
    case TaskStatus.COMPLETED:
      return 'Completed';
    case TaskStatus.BLOCKED:
      return 'Blocked';
    default:
      return 'Unknown';
  }
};

/**
 * Format deadline display
 */
export const formatDeadline = (deadline?: string): string => {
  if (!deadline) return 'No deadline';

  const deadlineDate = new Date(deadline);
  const now = new Date();
  const diffMs = deadlineDate.getTime() - now.getTime();
  const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
  const diffDays = Math.floor(diffHours / 24);

  if (diffMs < 0) {
    const overdueDays = Math.abs(diffDays);
    return overdueDays === 1 ? '1 day overdue' : `${overdueDays} days overdue`;
  } else if (diffHours < 1) {
    return 'Due very soon';
  } else if (diffHours < 24) {
    return `${diffHours}h remaining`;
  } else if (diffDays === 1) {
    return '1 day remaining';
  } else {
    return `${diffDays} days remaining`;
  }
};

/**
 * Check if deadline has passed
 */
export const isDeadlinePassed = (deadline?: string): boolean => {
  if (!deadline) return false;
  const deadlineDate = new Date(deadline);
  const now = new Date();
  return now > deadlineDate;
};

/**
 * Format date for display
 */
export const formatDate = (date: string): string => {
  const d = new Date(date);
  return d.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
};

/**
 * Format relative time (e.g., "2 days ago")
 */
export const formatRelativeTime = (date: string): string => {
  const d = new Date(date);
  const now = new Date();
  const diffMs = now.getTime() - d.getTime();
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

  if (diffDays === 0) {
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    if (diffHours === 0) {
      const diffMinutes = Math.floor(diffMs / (1000 * 60));
      return diffMinutes <= 1 ? 'Just now' : `${diffMinutes} minutes ago`;
    }
    return diffHours === 1 ? '1 hour ago' : `${diffHours} hours ago`;
  } else if (diffDays === 1) {
    return 'Yesterday';
  } else if (diffDays < 7) {
    return `${diffDays} days ago`;
  } else if (diffDays < 30) {
    const weeks = Math.floor(diffDays / 7);
    return weeks === 1 ? '1 week ago' : `${weeks} weeks ago`;
  } else {
    const months = Math.floor(diffDays / 30);
    return months === 1 ? '1 month ago' : `${months} months ago`;
  }
};
