/**
 * CustomFieldInput Component
 * Renders appropriate input based on field_type
 */
import React from 'react';
import type { CustomFieldDefinition } from '../../../types/position';

interface CustomFieldInputProps {
  field: CustomFieldDefinition;
  value: unknown;
  onChange: (fieldKey: string, value: unknown) => void;
  disabled?: boolean;
  className?: string;
}

export const CustomFieldInput: React.FC<CustomFieldInputProps> = ({
  field,
  value,
  onChange,
  disabled = false,
  className = ''
}) => {
  const baseInputClasses = `
    block w-full rounded-md border-gray-300 shadow-sm
    focus:border-indigo-500 focus:ring-indigo-500
    disabled:bg-gray-100 disabled:cursor-not-allowed
    sm:text-sm
  `;

  const handleChange = (newValue: unknown) => {
    onChange(field.field_key, newValue);
  };

  const renderInput = () => {
    switch (field.field_type) {
      case 'TEXT':
        return (
          <input
            type="text"
            value={(value as string) || ''}
            onChange={(e) => handleChange(e.target.value)}
            disabled={disabled}
            required={field.is_required}
            className={baseInputClasses}
            placeholder={`Enter ${field.label.toLowerCase()}`}
          />
        );

      case 'NUMBER':
        return (
          <input
            type="number"
            value={(value as number) || ''}
            onChange={(e) => handleChange(e.target.value ? Number(e.target.value) : null)}
            disabled={disabled}
            required={field.is_required}
            className={baseInputClasses}
            placeholder={`Enter ${field.label.toLowerCase()}`}
          />
        );

      case 'DATE':
        return (
          <input
            type="date"
            value={(value as string) || ''}
            onChange={(e) => handleChange(e.target.value)}
            disabled={disabled}
            required={field.is_required}
            className={baseInputClasses}
          />
        );

      case 'BOOLEAN':
        return (
          <label className="inline-flex items-center">
            <input
              type="checkbox"
              checked={Boolean(value)}
              onChange={(e) => handleChange(e.target.checked)}
              disabled={disabled}
              className="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500 disabled:cursor-not-allowed"
            />
            <span className="ml-2 text-sm text-gray-700">{field.label}</span>
          </label>
        );

      case 'SELECT':
        return (
          <select
            value={(value as string) || ''}
            onChange={(e) => handleChange(e.target.value)}
            disabled={disabled}
            required={field.is_required}
            className={baseInputClasses}
          >
            <option value="">Select {field.label.toLowerCase()}</option>
            {field.options?.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
        );

      case 'MULTISELECT':
        const selectedValues = (value as string[]) || [];
        return (
          <div className="space-y-2">
            {field.options?.map((option) => (
              <label key={option} className="inline-flex items-center mr-4">
                <input
                  type="checkbox"
                  checked={selectedValues.includes(option)}
                  onChange={(e) => {
                    if (e.target.checked) {
                      handleChange([...selectedValues, option]);
                    } else {
                      handleChange(selectedValues.filter((v) => v !== option));
                    }
                  }}
                  disabled={disabled}
                  className="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500 disabled:cursor-not-allowed"
                />
                <span className="ml-2 text-sm text-gray-700">{option}</span>
              </label>
            ))}
          </div>
        );

      case 'URL':
        return (
          <input
            type="url"
            value={(value as string) || ''}
            onChange={(e) => handleChange(e.target.value)}
            disabled={disabled}
            required={field.is_required}
            className={baseInputClasses}
            placeholder="https://example.com"
          />
        );

      default:
        return (
          <input
            type="text"
            value={(value as string) || ''}
            onChange={(e) => handleChange(e.target.value)}
            disabled={disabled}
            className={baseInputClasses}
          />
        );
    }
  };

  // Don't render label for BOOLEAN since it's inline
  if (field.field_type === 'BOOLEAN') {
    return <div className={className}>{renderInput()}</div>;
  }

  return (
    <div className={className}>
      <label className="block text-sm font-medium text-gray-700 mb-1">
        {field.label}
        {field.is_required && <span className="text-red-500 ml-1">*</span>}
      </label>
      {renderInput()}
    </div>
  );
};

export default CustomFieldInput;
