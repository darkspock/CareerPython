/**
 * Email Template Types
 * Phase 7: TypeScript types for email template management
 */

export const TriggerEvent = {
  APPLICATION_CREATED: 'application_created',
  APPLICATION_UPDATED: 'application_updated',
  STAGE_ENTERED: 'stage_entered',
  STAGE_COMPLETED: 'stage_completed',
  STAGE_CHANGED: 'stage_changed',
  STATUS_ACCEPTED: 'status_accepted',
  STATUS_REJECTED: 'status_rejected',
  STATUS_WITHDRAWN: 'status_withdrawn',
  DEADLINE_APPROACHING: 'deadline_approaching',
  DEADLINE_PASSED: 'deadline_passed',
  MANUAL: 'manual'
} as const;
export type TriggerEvent = typeof TriggerEvent[keyof typeof TriggerEvent];

export interface EmailTemplate {
  id: string;
  workflow_id: string;
  stage_id: string | null;
  template_name: string;
  template_key: string;
  subject: string;
  body_html: string;
  body_text: string | null;
  available_variables: string[];
  trigger_event: TriggerEvent;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface CreateEmailTemplateRequest {
  workflow_id: string;
  template_name: string;
  template_key: string;
  subject: string;
  body_html: string;
  body_text?: string | null;
  trigger_event: TriggerEvent;
  available_variables: string[];
  stage_id?: string | null;
  is_active?: boolean;
}

export interface UpdateEmailTemplateRequest {
  template_name: string;
  subject: string;
  body_html: string;
  body_text?: string | null;
  available_variables: string[];
}

export interface EmailTemplateFilters {
  workflow_id?: string;
  stage_id?: string;
  trigger_event?: TriggerEvent;
  active_only?: boolean;
}

// Helper functions
export function getTriggerEventLabel(event: TriggerEvent): string {
  const labels: Record<TriggerEvent, string> = {
    [TriggerEvent.APPLICATION_CREATED]: 'Application Created',
    [TriggerEvent.APPLICATION_UPDATED]: 'Application Updated',
    [TriggerEvent.STAGE_ENTERED]: 'Stage Entered',
    [TriggerEvent.STAGE_COMPLETED]: 'Stage Completed',
    [TriggerEvent.STAGE_CHANGED]: 'Stage Changed',
    [TriggerEvent.STATUS_ACCEPTED]: 'Status Accepted',
    [TriggerEvent.STATUS_REJECTED]: 'Status Rejected',
    [TriggerEvent.STATUS_WITHDRAWN]: 'Status Withdrawn',
    [TriggerEvent.DEADLINE_APPROACHING]: 'Deadline Approaching',
    [TriggerEvent.DEADLINE_PASSED]: 'Deadline Passed',
    [TriggerEvent.MANUAL]: 'Manual'
  };
  return labels[event];
}

export function getTriggerEventDescription(event: TriggerEvent): string {
  const descriptions: Record<TriggerEvent, string> = {
    [TriggerEvent.APPLICATION_CREATED]: 'Sent when a new application is submitted',
    [TriggerEvent.APPLICATION_UPDATED]: 'Sent when application data is updated',
    [TriggerEvent.STAGE_ENTERED]: 'Sent when candidate enters a specific stage',
    [TriggerEvent.STAGE_COMPLETED]: 'Sent when a stage is marked as completed',
    [TriggerEvent.STAGE_CHANGED]: 'Sent whenever stage changes (any stage)',
    [TriggerEvent.STATUS_ACCEPTED]: 'Sent when application is accepted',
    [TriggerEvent.STATUS_REJECTED]: 'Sent when application is rejected',
    [TriggerEvent.STATUS_WITHDRAWN]: 'Sent when candidate withdraws application',
    [TriggerEvent.DEADLINE_APPROACHING]: 'Sent when stage deadline is approaching',
    [TriggerEvent.DEADLINE_PASSED]: 'Sent when stage deadline has passed',
    [TriggerEvent.MANUAL]: 'Manually triggered by user action'
  };
  return descriptions[event];
}

export const DEFAULT_AVAILABLE_VARIABLES = [
  'candidate_name',
  'candidate_email',
  'position_title',
  'company_name',
  'stage_name',
  'application_id',
  'changed_at'
];

export function formatVariableForDisplay(variable: string): string {
  return variable
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
}

export function getVariableDescription(variable: string): string {
  const descriptions: Record<string, string> = {
    candidate_name: "The candidate's full name",
    candidate_email: "The candidate's email address",
    position_title: 'The job position title',
    company_name: 'Your company name',
    stage_name: 'The current workflow stage name',
    application_id: 'Unique application identifier',
    changed_at: 'Date and time of the change',
    previous_stage_id: 'Previous stage identifier',
    new_stage_id: 'New stage identifier'
  };
  return descriptions[variable] || 'Custom variable';
}
