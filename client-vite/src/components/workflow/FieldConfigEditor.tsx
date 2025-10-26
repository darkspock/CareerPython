import React from 'react';
import { FieldType } from '../../types/workflow';

interface FieldConfigEditorProps {
  fieldType: FieldType;
  config: Record<string, any>;
  onChange: (config: Record<string, any>) => void;
}

export const FieldConfigEditor: React.FC<FieldConfigEditorProps> = ({
  fieldType,
  config,
  onChange
}) => {
  const updateConfig = (key: string, value: any) => {
    onChange({ ...config, [key]: value });
  };

  const updateArrayConfig = (key: string, value: string) => {
    const items = value.split('\n').filter(item => item.trim());
    onChange({ ...config, [key]: items });
  };

  // Render config editor based on field type
  switch (fieldType) {
    case 'DROPDOWN':
    case 'MULTI_SELECT':
    case 'RADIO':
      return (
        <div>
          <label className="block text-sm font-medium mb-1">
            Options * (one per line)
          </label>
          <textarea
            value={config.options?.join('\n') || ''}
            onChange={(e) => updateArrayConfig('options', e.target.value)}
            className="w-full px-3 py-2 border rounded font-mono text-sm"
            rows={5}
            placeholder="Option 1&#10;Option 2&#10;Option 3"
          />
          <p className="text-xs text-gray-500 mt-1">
            Enter each option on a new line
          </p>
        </div>
      );

    case 'NUMBER':
      return (
        <div className="space-y-3">
          <div>
            <label className="block text-sm font-medium mb-1">
              Minimum Value (optional)
            </label>
            <input
              type="number"
              value={config.min ?? ''}
              onChange={(e) => updateConfig('min', e.target.value ? parseFloat(e.target.value) : undefined)}
              className="w-full px-3 py-2 border rounded"
              placeholder="No minimum"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">
              Maximum Value (optional)
            </label>
            <input
              type="number"
              value={config.max ?? ''}
              onChange={(e) => updateConfig('max', e.target.value ? parseFloat(e.target.value) : undefined)}
              className="w-full px-3 py-2 border rounded"
              placeholder="No maximum"
            />
          </div>
        </div>
      );

    case 'CURRENCY':
      return (
        <div className="space-y-3">
          <div>
            <label className="block text-sm font-medium mb-1">
              Currency Code (ISO 4217)
            </label>
            <input
              type="text"
              value={config.currency_code || 'USD'}
              onChange={(e) => updateConfig('currency_code', e.target.value.toUpperCase())}
              className="w-full px-3 py-2 border rounded"
              placeholder="USD"
              maxLength={3}
            />
            <p className="text-xs text-gray-500 mt-1">
              3-letter currency code (e.g., USD, EUR, GBP)
            </p>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">
              Minimum Value (optional)
            </label>
            <input
              type="number"
              value={config.min ?? ''}
              onChange={(e) => updateConfig('min', e.target.value ? parseFloat(e.target.value) : undefined)}
              className="w-full px-3 py-2 border rounded"
              placeholder="No minimum"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">
              Maximum Value (optional)
            </label>
            <input
              type="number"
              value={config.max ?? ''}
              onChange={(e) => updateConfig('max', e.target.value ? parseFloat(e.target.value) : undefined)}
              className="w-full px-3 py-2 border rounded"
              placeholder="No maximum"
            />
          </div>
        </div>
      );

    case 'FILE':
      return (
        <div className="space-y-3">
          <div>
            <label className="block text-sm font-medium mb-1">
              Allowed Extensions (optional, one per line)
            </label>
            <textarea
              value={config.allowed_extensions?.join('\n') || ''}
              onChange={(e) => updateArrayConfig('allowed_extensions', e.target.value)}
              className="w-full px-3 py-2 border rounded font-mono text-sm"
              rows={4}
              placeholder=".pdf&#10;.doc&#10;.docx"
            />
            <p className="text-xs text-gray-500 mt-1">
              Include the dot (e.g., .pdf, .jpg)
            </p>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">
              Maximum File Size (MB, optional)
            </label>
            <input
              type="number"
              value={config.max_size_mb ?? ''}
              onChange={(e) => updateConfig('max_size_mb', e.target.value ? parseFloat(e.target.value) : undefined)}
              className="w-full px-3 py-2 border rounded"
              placeholder="No limit"
              min="0"
              step="0.1"
            />
          </div>
        </div>
      );

    case 'TEXT':
      return (
        <div>
          <label className="block text-sm font-medium mb-1">
            Maximum Length (optional)
          </label>
          <input
            type="number"
            value={config.max_length ?? ''}
            onChange={(e) => updateConfig('max_length', e.target.value ? parseInt(e.target.value) : undefined)}
            className="w-full px-3 py-2 border rounded"
            placeholder="No limit"
            min="1"
          />
          <p className="text-xs text-gray-500 mt-1">
            Maximum number of characters allowed
          </p>
        </div>
      );

    case 'TEXT_AREA':
    case 'DATE':
    case 'CHECKBOX':
    default:
      return (
        <div className="p-3 bg-gray-50 border rounded text-sm text-gray-600">
          No additional configuration required for this field type.
        </div>
      );
  }
};
