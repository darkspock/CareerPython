import React, { useState, useEffect, useRef } from 'react';
import { Settings } from 'lucide-react';
import type { FieldType } from '../../types/workflow';
import { FieldOptionsI18nModal, type FieldOption } from './FieldOptionsI18nModal';

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
  const [localConfig, setLocalConfig] = useState<Record<string, any>>(config);
  const [showI18nModal, setShowI18nModal] = useState(false);
  const isUpdatingFromProps = useRef(false);

  // Update local config when prop changes, but avoid infinite loops
  useEffect(() => {
    if (!isUpdatingFromProps.current) {
      setLocalConfig(config);
    }
    isUpdatingFromProps.current = false;
  }, [config]);

  const updateConfig = (key: string, value: any) => {
    const newConfig = { ...localConfig, [key]: value };
    setLocalConfig(newConfig);
    // Don't call onChange immediately - let the parent handle it
  };

  const updateConfigAndNotify = (key: string, value: any) => {
    const newConfig = { ...localConfig, [key]: value };
    setLocalConfig(newConfig);
    isUpdatingFromProps.current = true;
    onChange(newConfig);
  };

  const updateArrayConfig = (key: string, value: string) => {
    const items = value.split('\n').filter(item => item.trim());
    const newConfig = { ...localConfig, [key]: items };
    setLocalConfig(newConfig);
    isUpdatingFromProps.current = true;
    onChange(newConfig);
  };

  // Render config editor based on field type
  switch (fieldType) {
    case 'DROPDOWN':
    case 'MULTI_SELECT':
    case 'RADIO':
    case 'CHECKBOX':
      // Convert options to FieldOption format for modal
      const convertToFieldOptions = (): FieldOption[] => {
        if (!localConfig.options || localConfig.options.length === 0) {
          return [];
        }

        return localConfig.options.map((opt: any, index: number) => {
          if (typeof opt === 'object' && opt.id && opt.labels) {
            // Already in new format
            return {
              id: opt.id,
              sort: opt.sort ?? index,
              labels: opt.labels || []
            };
          } else {
            // Old format (string) - convert to new format
            return {
              id: `legacy_${Date.now()}_${index}`,
              sort: index,
              labels: [
                { language: 'en', label: typeof opt === 'string' ? opt : String(opt) }
              ]
            };
          }
        });
      };

      const handleSaveOptions = (newOptions: FieldOption[]) => {
        // Convert FieldOptions to config format
        const optionsData = newOptions.map(opt => ({
          id: opt.id,
          sort: opt.sort,
          labels: opt.labels
        }));
        
        const newConfig = { ...localConfig, options: optionsData };
        setLocalConfig(newConfig);
        isUpdatingFromProps.current = true;
        onChange(newConfig);
        setShowI18nModal(false);
      };

      return (
        <>
          <div>
            <button
              type="button"
              onClick={() => setShowI18nModal(true)}
              className="flex items-center gap-1 px-2 py-1 text-sm font-medium text-blue-600 hover:text-blue-700 hover:bg-blue-50 rounded transition-colors"
              title="Edit options with i18n support"
            >
              <Settings className="w-4 h-4" />
              <span>Options</span>
            </button>
          </div>

          <FieldOptionsI18nModal
            isOpen={showI18nModal}
            options={convertToFieldOptions()}
            availableLanguages={['en', 'es']}
            onClose={() => setShowI18nModal(false)}
            onSave={handleSaveOptions}
          />
        </>
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
              value={localConfig.min ?? ''}
              onChange={(e) => updateConfig('min', e.target.value)}
              onBlur={(e) => updateConfigAndNotify('min', e.target.value ? parseFloat(e.target.value) : undefined)}
              onFocus={(e) => e.target.select()}
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
              value={localConfig.max ?? ''}
              onChange={(e) => updateConfig('max', e.target.value)}
              onBlur={(e) => updateConfigAndNotify('max', e.target.value ? parseFloat(e.target.value) : undefined)}
              onFocus={(e) => e.target.select()}
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
              value={localConfig.currency_code || 'USD'}
              onChange={(e) => updateConfig('currency_code', e.target.value)}
              onBlur={(e) => updateConfigAndNotify('currency_code', e.target.value.toUpperCase())}
              onFocus={(e) => e.target.select()}
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
              value={localConfig.min ?? ''}
              onChange={(e) => updateConfig('min', e.target.value)}
              onBlur={(e) => updateConfigAndNotify('min', e.target.value ? parseFloat(e.target.value) : undefined)}
              onFocus={(e) => e.target.select()}
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
              value={localConfig.max ?? ''}
              onChange={(e) => updateConfig('max', e.target.value)}
              onBlur={(e) => updateConfigAndNotify('max', e.target.value ? parseFloat(e.target.value) : undefined)}
              onFocus={(e) => e.target.select()}
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
              value={localConfig.allowed_extensions?.join('\n') || ''}
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
              value={localConfig.max_size_mb ?? ''}
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
            value={localConfig.max_length ?? ''}
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

    case 'TEXTAREA':
    case 'DATE':
    default:
      return (
        <div className="p-3 bg-gray-50 border rounded text-sm text-gray-600">
          No additional configuration required for this field type.
        </div>
      );
  }
};
