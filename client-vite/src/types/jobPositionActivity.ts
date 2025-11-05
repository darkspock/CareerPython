/**
 * Job Position Activity Types
 * 
 * Types for tracking activity history on job positions.
 */

export const ActivityType = {
  CREATED: 'created',
  EDITED: 'edited',
  STAGE_MOVED: 'stage_moved',
  STATUS_CHANGED: 'status_changed',
  COMMENT_ADDED: 'comment_added',
} as const;

export type ActivityType = typeof ActivityType[keyof typeof ActivityType];

export interface JobPositionActivity {
  id: string;
  job_position_id: string;
  activity_type: ActivityType;
  description: string;
  performed_by_user_id: string;
  metadata: Record<string, any>;
  created_at: string; // ISO datetime string
}

export interface JobPositionActivityListResponse {
  activities: JobPositionActivity[];
  total: number;
}

/**
 * Helper functions for activity metadata
 */

export interface EditActivityMetadata {
  changed_fields: string[];
  old_values: Record<string, any>;
  new_values: Record<string, any>;
}

export interface StageMoveActivityMetadata {
  old_stage_id: string | null;
  old_stage_name: string | null;
  new_stage_id: string;
  new_stage_name: string;
}

export interface StatusChangeActivityMetadata {
  old_status: string;
  new_status: string;
}

export interface CommentAddedActivityMetadata {
  comment_id: string;
  is_global: boolean;
}

/**
 * Type guard to check activity metadata type
 */
export function isEditActivity(activity: JobPositionActivity): activity is JobPositionActivity & { metadata: EditActivityMetadata } {
  return activity.activity_type === 'edited';
}

export function isStageMoveActivity(activity: JobPositionActivity): activity is JobPositionActivity & { metadata: StageMoveActivityMetadata } {
  return activity.activity_type === 'stage_moved';
}

export function isStatusChangeActivity(activity: JobPositionActivity): activity is JobPositionActivity & { metadata: StatusChangeActivityMetadata } {
  return activity.activity_type === 'status_changed';
}

export function isCommentAddedActivity(activity: JobPositionActivity): activity is JobPositionActivity & { metadata: CommentAddedActivityMetadata } {
  return activity.activity_type === 'comment_added';
}

