import { useState, useEffect } from 'react';
import type { JobPositionWorkflow, JobPositionWorkflowStage } from '../../types/position';

interface DynamicCustomFieldsProps {
  workflow: JobPositionWorkflow | null;
  currentStage: JobPositionWorkflowStage | null;
  customFieldsValues: Record<string, any>;
  onChange: (values: Record<string, any>) => void;
  readOnly?: boolean;
}

export function DynamicCustomFields({
  workflow,
  currentStage,
  customFieldsValues,
  onChange,
  readOnly = false,
}: DynamicCustomFieldsProps) {
  const [visibleFields, setVisibleFields] = useState<Array<{
    name: string;
    label: string;
    type: string;
    required: boolean;
    config: any;
  }>>([]);

  useEffect(() => {
    console.log('[DynamicCustomFields] Workflow:', workflow);
    console.log('[DynamicCustomFields] Current Stage:', currentStage);
    console.log('[DynamicCustomFields] Custom Fields Config:', workflow?.custom_fields_config);
    
    if (!workflow || !workflow.custom_fields_config) {
      console.log('[DynamicCustomFields] No workflow or custom_fields_config');
      setVisibleFields([]);
      return;
    }

    const fieldsConfig = workflow.custom_fields_config.fields || {};
    const fieldLabels = workflow.custom_fields_config.field_labels || {};
    const fieldTypes = workflow.custom_fields_config.field_types || {};
    const fieldRequired = workflow.custom_fields_config.field_required || {};
    const fieldValidation = workflow.custom_fields_config.field_validation || {};

    console.log('[DynamicCustomFields] Fields Config:', fieldsConfig);
    console.log('[DynamicCustomFields] Field Labels:', fieldLabels);
    console.log('[DynamicCustomFields] Field Types:', fieldTypes);

    // Get field visibility from current stage or default
    const fieldVisibility = currentStage?.field_visibility || {};
    const defaultVisibility = workflow.custom_fields_config.field_candidate_visibility_default || {};

    console.log('[DynamicCustomFields] Field Visibility (stage):', fieldVisibility);
    console.log('[DynamicCustomFields] Default Visibility:', defaultVisibility);

    // Filter visible fields
    const visible: Array<{
      name: string;
      label: string;
      type: string;
      required: boolean;
      config: any;
    }> = [];

    for (const fieldName in fieldsConfig) {
      const fieldConfig = fieldsConfig[fieldName];
      // For admin editing, show all fields regardless of visibility setting
      // Visibility is only for candidate-facing views
      const isVisible = true; // Always show in admin edit form

      if (isVisible) {
        visible.push({
          name: fieldName,
          label: fieldLabels[fieldName] || fieldConfig?.label || fieldName,
          type: fieldTypes[fieldName] || fieldConfig?.type || 'text',
          required: fieldRequired[fieldName] || fieldConfig?.required || false,
          config: fieldValidation[fieldName] || fieldConfig?.validation || {},
        });
      }
    }

    console.log('[DynamicCustomFields] Visible Fields:', visible);
    setVisibleFields(visible);
  }, [workflow, currentStage]);

  const handleFieldChange = (fieldName: string, value: any) => {
    const updated = {
      ...customFieldsValues,
      [fieldName]: value,
    };
    onChange(updated);
  };

  if (visibleFields.length === 0) {
    return (
      <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 text-center text-gray-500 text-sm">
        No custom fields configured for this workflow
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {visibleFields.map((field) => {
        const currentValue = customFieldsValues[field.name];

        // For read-only view (detail page), render as display value
        if (readOnly) {
          return (
            <div key={field.name} className="border-b border-gray-100 pb-3 last:border-b-0 last:pb-0">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                {field.label}
              </label>
              <div className="text-gray-900">
                {renderFieldDisplay(field, currentValue)}
              </div>
            </div>
          );
        }

        return (
          <div key={field.name}>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              {field.label}
              {field.required && <span className="text-red-500 ml-1">*</span>}
            </label>
            {renderFieldInput(field, currentValue, (value) => handleFieldChange(field.name, value), readOnly)}
          </div>
        );
      })}
    </div>
  );
}

function renderFieldInput(
  field: { name: string; type: string; config: any },
  value: any,
  onChange: (value: any) => void,
  readOnly: boolean
) {
  const inputClassName = `w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
    readOnly ? 'bg-gray-100 cursor-not-allowed' : ''
  }`;

  switch (field.type) {
    case 'text':
      return (
        <input
          type="text"
          value={value || ''}
          onChange={(e) => onChange(e.target.value)}
          className={inputClassName}
          disabled={readOnly}
          required={field.config.required}
        />
      );

    case 'number':
      return (
        <input
          type="number"
          value={value || ''}
          onChange={(e) => onChange(e.target.value ? Number(e.target.value) : null)}
          className={inputClassName}
          disabled={readOnly}
          required={field.config.required}
        />
      );

    case 'date':
      return (
        <input
          type="date"
          value={value || ''}
          onChange={(e) => onChange(e.target.value)}
          className={inputClassName}
          disabled={readOnly}
          required={field.config.required}
        />
      );

    case 'select':
      const options = field.config.options || [];
      return (
        <select
          value={value || ''}
          onChange={(e) => onChange(e.target.value)}
          className={inputClassName}
          disabled={readOnly}
          required={field.config.required}
        >
          <option value="">Select...</option>
          {options.map((opt: string | { value: string; label: string }) => {
            const optionValue = typeof opt === 'string' ? opt : opt.value;
            const optionLabel = typeof opt === 'string' ? opt : opt.label;
            return (
              <option key={optionValue} value={optionValue}>
                {optionLabel}
              </option>
            );
          })}
        </select>
      );

    case 'textarea':
      return (
        <textarea
          value={value || ''}
          onChange={(e) => onChange(e.target.value)}
          rows={4}
          className={inputClassName}
          disabled={readOnly}
          required={field.config.required}
        />
      );

    case 'object':
      // For complex objects, render as JSON editor
      return (
        <textarea
          value={typeof value === 'object' ? JSON.stringify(value, null, 2) : value || ''}
          onChange={(e) => {
            try {
              const parsed = JSON.parse(e.target.value);
              onChange(parsed);
            } catch {
              onChange(e.target.value);
            }
          }}
          rows={4}
          className={`${inputClassName} font-mono text-sm`}
          disabled={readOnly}
        />
      );

    default:
      return (
        <input
          type="text"
          value={value || ''}
          onChange={(e) => onChange(e.target.value)}
          className={inputClassName}
          disabled={readOnly}
        />
      );
  }
}

function renderFieldDisplay(
  field: { name: string; type: string; config: any },
  value: any
) {
  if (value === null || value === undefined || value === '') {
    return <span className="text-gray-400 italic">Not specified</span>;
  }

  switch (field.type) {
    case 'object':
      return (
        <pre className="text-sm bg-gray-50 p-2 rounded border border-gray-200 overflow-x-auto">
          {typeof value === 'object' ? JSON.stringify(value, null, 2) : String(value)}
        </pre>
      );

    case 'date':
      return <span>{new Date(value).toLocaleDateString()}</span>;

    case 'number':
      return <span>{typeof value === 'number' ? value.toLocaleString() : value}</span>;

    case 'select':
      return <span>{String(value)}</span>;

    case 'textarea':
      return <p className="whitespace-pre-wrap">{String(value)}</p>;

    default:
      return <span>{String(value)}</span>;
  }
}

