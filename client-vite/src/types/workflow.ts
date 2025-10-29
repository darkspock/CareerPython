// Workflow types

// Phase 12: Updated workflow status (INACTIVE → DRAFT)
export type WorkflowStatus = 'DRAFT' | 'ACTIVE' | 'ARCHIVED';

// Phase 12: Updated stage types (INTERMEDIATE → STANDARD, FINAL → SUCCESS, added FAIL)
export type StageType = 'initial' | 'standard' | 'success' | 'fail';

// Kanban display configuration
export enum KanbanDisplay {
  COLUMN = 'column',
  ROW = 'row', 
  NONE = 'none'
}

export interface CompanyWorkflow {
  id: string;
  company_id: string;
  phase_id?: string | null; // Phase 12: Phase association
  name: string;
  description: string | null;
  is_default: boolean;
  status: WorkflowStatus;
  created_at: string;
  updated_at: string;

  // Expanded data
  stages?: WorkflowStage[];
  candidate_count?: number;
  active_candidate_count?: number;
  active_position_count?: number;
}

export interface WorkflowStage {
  id: string;
  workflow_id: string;
  name: string;
  description: string | null;
  stage_type: StageType;
  order: number;
  is_active: boolean;
  allow_skip: boolean;
  estimated_duration_days: number | null;
  default_role_ids: string[] | null;
  default_assigned_users: string[] | null;
  email_template_id: string | null;
  custom_email_text: string | null;
  deadline_days: number | null;
  estimated_cost: string | null;
  next_phase_id?: string | null; // Phase 12: Phase transition
  kanban_display: KanbanDisplay; // Kanban display configuration
  created_at: string;
  updated_at: string;

  // Expanded data
  candidate_count?: number;
}

export interface CreateWorkflowRequest {
  company_id: string;
  name: string;
  description?: string;
  phase_id?: string | null; // Phase 12: Phase association
  is_default?: boolean;
  status?: WorkflowStatus;
}

export interface UpdateWorkflowRequest {
  name?: string;
  description?: string;
  phase_id?: string | null; // Phase 12: Phase association
  is_default?: boolean;
  status?: WorkflowStatus;
}

export interface CreateStageRequest {
  workflow_id: string;
  name: string;
  description?: string;
  stage_type: StageType;
  order?: number;
  is_active?: boolean;
  allow_skip?: boolean;
  estimated_duration_days?: number;
  default_role_ids?: string[];
  default_assigned_users?: string[];
  email_template_id?: string;
  custom_email_text?: string;
  deadline_days?: number;
  estimated_cost?: string;
  next_phase_id?: string | null; // Phase 12: Phase transition
}

export interface UpdateStageRequest {
  name?: string;
  description?: string;
  stage_type?: StageType;
  order?: number;
  is_active?: boolean;
  allow_skip?: boolean;
  estimated_duration_days?: number;
  default_role_ids?: string[];
  default_assigned_users?: string[];
  email_template_id?: string;
  custom_email_text?: string;
  deadline_days?: number;
  estimated_cost?: string;
  next_phase_id?: string | null; // Phase 12: Phase transition
}

export interface ReorderStagesRequest {
  stage_ids_in_order: string[]; // Array of stage IDs in desired order
}

// Helper functions
export const getWorkflowStatusColor = (status: WorkflowStatus): string => {
  switch (status) {
    case 'DRAFT': return 'bg-gray-100 text-gray-800'; // Phase 12: DRAFT status
    case 'ACTIVE': return 'bg-green-100 text-green-800';
    case 'ARCHIVED': return 'bg-red-100 text-red-800';
    default: return 'bg-gray-100 text-gray-800';
  }
};

export const getStageTypeColor = (type: StageType): string => {
  switch (type) {
    case 'initial': return 'bg-blue-100 text-blue-800';
    case 'standard': return 'bg-yellow-100 text-yellow-800'; // Phase 12: STANDARD
    case 'success': return 'bg-green-100 text-green-800'; // Phase 12: SUCCESS
    case 'fail': return 'bg-red-100 text-red-800'; // Phase 12: FAIL
    default: return 'bg-gray-100 text-gray-800';
  }
};

// Custom Fields Types

export type FieldType =
  | 'TEXT'
  | 'TEXT_AREA'
  | 'NUMBER'
  | 'CURRENCY'
  | 'DATE'
  | 'DROPDOWN'
  | 'MULTI_SELECT'
  | 'RADIO'
  | 'CHECKBOX'
  | 'FILE';

export type FieldVisibility =
  | 'VISIBLE'
  | 'HIDDEN'
  | 'READ_ONLY'
  | 'REQUIRED';

export interface CustomField {
  id: string;
  workflow_id: string;
  field_key: string;
  field_name: string;
  field_type: FieldType;
  field_config: Record<string, any> | null;
  order_index: number;
  created_at: string;
  updated_at: string;
}

export interface FieldConfiguration {
  id: string;
  stage_id: string;
  custom_field_id: string;
  visibility: FieldVisibility;
  created_at: string;
  updated_at: string;
}

export interface CreateCustomFieldRequest {
  workflow_id: string;
  field_key: string;
  field_name: string;
  field_type: FieldType;
  field_config?: Record<string, any>;
  order_index: number;
}

export interface UpdateCustomFieldRequest {
  field_name: string;
  field_type: FieldType;
  field_config?: Record<string, any>;
}

export interface ReorderCustomFieldRequest {
  new_order_index: number;
}

export interface ConfigureStageFieldRequest {
  stage_id: string;
  custom_field_id: string;
  visibility: FieldVisibility;
}

export interface UpdateFieldVisibilityRequest {
  visibility: FieldVisibility;
}

// Field config types for different field types
export interface DropdownConfig {
  options: string[];
}

export interface MultiSelectConfig {
  options: string[];
}

export interface RadioConfig {
  options: string[];
}

export interface NumberConfig {
  min?: number;
  max?: number;
}

export interface CurrencyConfig {
  currency_code?: string;
  min?: number;
  max?: number;
}

export interface FileConfig {
  allowed_extensions?: string[];
  max_size_mb?: number;
}

export interface TextConfig {
  max_length?: number;
}

// Helper functions for custom fields
export const getFieldTypeLabel = (type: FieldType): string => {
  switch (type) {
    case 'TEXT': return 'Short Text';
    case 'TEXT_AREA': return 'Long Text';
    case 'NUMBER': return 'Number';
    case 'CURRENCY': return 'Currency';
    case 'DATE': return 'Date';
    case 'DROPDOWN': return 'Dropdown';
    case 'MULTI_SELECT': return 'Multi-Select';
    case 'RADIO': return 'Radio Buttons';
    case 'CHECKBOX': return 'Checkbox';
    case 'FILE': return 'File Upload';
    default: return type;
  }
};

export const getFieldVisibilityLabel = (visibility: FieldVisibility): string => {
  switch (visibility) {
    case 'VISIBLE': return 'Visible';
    case 'HIDDEN': return 'Hidden';
    case 'READ_ONLY': return 'Read Only';
    case 'REQUIRED': return 'Required';
    default: return visibility;
  }
};

export const getFieldVisibilityColor = (visibility: FieldVisibility): string => {
  switch (visibility) {
    case 'VISIBLE': return 'bg-blue-100 text-blue-800';
    case 'HIDDEN': return 'bg-gray-100 text-gray-800';
    case 'READ_ONLY': return 'bg-yellow-100 text-yellow-800';
    case 'REQUIRED': return 'bg-red-100 text-red-800';
    default: return 'bg-gray-100 text-gray-800';
  }
};

// Validation Rule Types
export type ValidationRuleType = 'compare_position_field' | 'range' | 'pattern' | 'custom';

export type ComparisonOperator = 'gt' | 'gte' | 'lt' | 'lte' | 'eq' | 'neq' | 'in_range' | 'out_range' | 'contains' | 'not_contains';

export type ValidationSeverity = 'warning' | 'error';

export interface ValidationRule {
  id: string;
  custom_field_id: string;
  stage_id: string;
  rule_type: ValidationRuleType;
  comparison_operator: ComparisonOperator;
  position_field_path: string | null;
  comparison_value: any;
  severity: ValidationSeverity;
  validation_message: string;
  auto_reject: boolean;
  rejection_reason: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface CreateValidationRuleRequest {
  custom_field_id: string;
  stage_id: string;
  rule_type: ValidationRuleType;
  comparison_operator: ComparisonOperator;
  severity: ValidationSeverity;
  validation_message: string;
  position_field_path?: string;
  comparison_value?: any;
  auto_reject?: boolean;
  rejection_reason?: string;
  is_active?: boolean;
}

export interface UpdateValidationRuleRequest {
  comparison_operator?: ComparisonOperator;
  severity?: ValidationSeverity;
  validation_message?: string;
  position_field_path?: string;
  comparison_value?: any;
  auto_reject?: boolean;
  rejection_reason?: string;
  is_active?: boolean;
}

export interface ValidationIssue {
  field_key: string;
  field_name: string;
  message: string;
  severity: ValidationSeverity;
  rule_id: string;
  should_auto_reject: boolean;
  rejection_reason: string | null;
}

export interface ValidationResult {
  is_valid: boolean;
  has_errors: boolean;
  has_warnings: boolean;
  errors: ValidationIssue[];
  warnings: ValidationIssue[];
  should_auto_reject: boolean;
  auto_reject_reason: string | null;
}

export interface ValidateStageRequest {
  stage_id: string;
  candidate_field_values: Record<string, any>;
  position_data?: Record<string, any>;
}

// Helper functions for validation rules
export const getValidationRuleTypeLabel = (type: ValidationRuleType): string => {
  switch (type) {
    case 'compare_position_field': return 'Compare with Position Field';
    case 'range': return 'Range Validation';
    case 'pattern': return 'Pattern Validation';
    case 'custom': return 'Custom Validation';
    default: return type;
  }
};

export const getComparisonOperatorLabel = (operator: ComparisonOperator): string => {
  switch (operator) {
    case 'gt': return 'Greater Than (>)';
    case 'gte': return 'Greater Than or Equal (≥)';
    case 'lt': return 'Less Than (<)';
    case 'lte': return 'Less Than or Equal (≤)';
    case 'eq': return 'Equal (=)';
    case 'neq': return 'Not Equal (≠)';
    case 'in_range': return 'In Range';
    case 'out_range': return 'Out of Range';
    case 'contains': return 'Contains';
    case 'not_contains': return 'Does Not Contain';
    default: return operator;
  }
};

export const getValidationSeverityLabel = (severity: ValidationSeverity): string => {
  switch (severity) {
    case 'warning': return 'Warning';
    case 'error': return 'Error';
    default: return severity;
  }
};

export const getValidationSeverityColor = (severity: ValidationSeverity): string => {
  switch (severity) {
    case 'warning': return 'bg-yellow-100 text-yellow-800';
    case 'error': return 'bg-red-100 text-red-800';
    default: return 'bg-gray-100 text-gray-800';
  }
};
