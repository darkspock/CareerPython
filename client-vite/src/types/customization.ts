// Entity Customization Types - Generic system for customizing any entity

// Entity Types
export type EntityCustomizationType = 'JobPosition' | 'CandidateApplication' | 'Candidate' | 'Workflow';

// Field Types (same as workflow.ts for consistency)
export type FieldType =
  | 'TEXT'
  | 'TEXTAREA'
  | 'NUMBER'
  | 'CURRENCY'
  | 'DATE'
  | 'DROPDOWN'
  | 'MULTI_SELECT'
  | 'RADIO'
  | 'CHECKBOX'
  | 'FILE'
  | 'URL'
  | 'EMAIL'
  | 'PHONE';

// Field Visibility
export type FieldVisibility =
  | 'VISIBLE'
  | 'HIDDEN'
  | 'READ_ONLY'
  | 'REQUIRED';

// Custom Field (generic, no entity-specific fields)
export interface CustomField {
  id: string;
  field_key: string;
  field_name: string;
  field_type: FieldType;
  field_config: Record<string, any> | null;
  order_index: number;
  created_at: string;
  updated_at: string;
}

// Entity Customization
export interface EntityCustomization {
  id: string;
  entity_type: EntityCustomizationType;
  entity_id: string;
  fields: CustomField[];
  validation: string | null;
  metadata: Record<string, any>;
  created_at: string;
  updated_at: string;
}

// Field Configuration (generic, with context_type and context_id)
export interface FieldConfiguration {
  id: string;
  entity_customization_id: string;
  custom_field_id: string;
  context_type: EntityCustomizationType;  // Type of context (e.g., 'WorkflowStage')
  context_id: string;  // ID of the context (e.g., stage_id)
  visibility: FieldVisibility;
  created_at: string;
  updated_at: string;
}

// Request Types
export interface CreateEntityCustomizationRequest {
  entity_type: EntityCustomizationType;
  entity_id: string;
  fields: CreateCustomFieldRequest[];
  validation?: string | null;
  metadata?: Record<string, any>;
}

export interface UpdateEntityCustomizationRequest {
  fields?: CreateCustomFieldRequest[];
  validation?: string | null;
  metadata?: Record<string, any>;
}

export interface CreateCustomFieldRequest {
  field_key: string;
  field_name: string;
  field_type: FieldType;
  field_config?: Record<string, any>;
  order_index: number;
}

export interface UpdateCustomFieldRequest {
  field_name?: string;
  field_type?: FieldType;
  field_config?: Record<string, any>;
  order_index?: number;
}

export interface ConfigureFieldVisibilityRequest {
  custom_field_id: string;
  context_type: EntityCustomizationType;
  context_id: string;
  visibility: FieldVisibility;
}

export interface UpdateFieldVisibilityRequest {
  visibility: FieldVisibility;
}

// Helper functions
export const getFieldTypeLabel = (type: FieldType): string => {
  switch (type) {
    case 'TEXT': return 'Short Text';
    case 'TEXTAREA': return 'Long Text';
    case 'NUMBER': return 'Number';
    case 'CURRENCY': return 'Currency';
    case 'DATE': return 'Date';
    case 'DROPDOWN': return 'Dropdown';
    case 'MULTI_SELECT': return 'Multi-Select';
    case 'RADIO': return 'Radio Buttons';
    case 'CHECKBOX': return 'Checkbox';
    case 'FILE': return 'File Upload';
    case 'URL': return 'URL';
    case 'EMAIL': return 'Email';
    case 'PHONE': return 'Phone';
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

