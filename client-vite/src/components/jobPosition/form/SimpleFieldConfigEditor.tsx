/**
 * SimpleFieldConfigEditor - Simplified field configuration for position custom fields
 * Uses plain string options instead of i18n objects
 */
import React, { useState, useEffect } from 'react';
import { Plus, X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import type { FieldType } from '@/types/workflow';

interface SimpleFieldConfigEditorProps {
  fieldType: FieldType;
  config: Record<string, any>;
  onChange: (config: Record<string, any>) => void;
}

export const SimpleFieldConfigEditor: React.FC<SimpleFieldConfigEditorProps> = ({
  fieldType,
  config,
  onChange
}) => {
  const [options, setOptions] = useState<string[]>([]);
  const [newOption, setNewOption] = useState('');

  // Initialize options from config
  useEffect(() => {
    if (config.options && Array.isArray(config.options)) {
      // Handle both simple strings and i18n objects
      const stringOptions = config.options.map((opt: any) => {
        if (typeof opt === 'string') return opt;
        if (opt && typeof opt === 'object') {
          // i18n format: extract first label
          if (opt.labels && Array.isArray(opt.labels) && opt.labels.length > 0) {
            return String(opt.labels[0].label || opt.id || '');
          }
          return String(opt.id || opt.label || opt.value || '');
        }
        return String(opt);
      }).filter(Boolean);
      setOptions(stringOptions);
    }
  }, []);

  const handleAddOption = () => {
    if (!newOption.trim()) return;
    const updatedOptions = [...options, newOption.trim()];
    setOptions(updatedOptions);
    setNewOption('');
    onChange({ ...config, options: updatedOptions });
  };

  const handleRemoveOption = (index: number) => {
    const updatedOptions = options.filter((_, i) => i !== index);
    setOptions(updatedOptions);
    onChange({ ...config, options: updatedOptions });
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleAddOption();
    }
  };

  // Render config editor based on field type
  switch (fieldType) {
    case 'DROPDOWN':
    case 'MULTI_SELECT':
    case 'RADIO':
    case 'CHECKBOX':
      return (
        <div className="space-y-3">
          <Label>Options</Label>

          {/* Options list */}
          {options.length > 0 && (
            <div className="space-y-1">
              {options.map((option, index) => (
                <div key={index} className="flex items-center gap-2 p-2 bg-muted/50 rounded">
                  <span className="flex-1 text-sm">{option}</span>
                  <Button
                    type="button"
                    variant="ghost"
                    size="sm"
                    onClick={() => handleRemoveOption(index)}
                    className="h-6 w-6 p-0 text-muted-foreground hover:text-destructive"
                  >
                    <X className="w-4 h-4" />
                  </Button>
                </div>
              ))}
            </div>
          )}

          {/* Add new option */}
          <div className="flex gap-2">
            <Input
              value={newOption}
              onChange={(e) => setNewOption(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Add option..."
              className="flex-1"
            />
            <Button
              type="button"
              variant="outline"
              size="sm"
              onClick={handleAddOption}
              disabled={!newOption.trim()}
            >
              <Plus className="w-4 h-4" />
            </Button>
          </div>

          {options.length === 0 && (
            <p className="text-xs text-muted-foreground">
              Add at least one option for this field type
            </p>
          )}
        </div>
      );

    case 'NUMBER':
      return (
        <div className="grid grid-cols-2 gap-3">
          <div>
            <Label className="text-xs">Min Value</Label>
            <Input
              type="number"
              value={config.min ?? ''}
              onChange={(e) => onChange({ ...config, min: e.target.value ? parseFloat(e.target.value) : undefined })}
              placeholder="No min"
              className="mt-1"
            />
          </div>
          <div>
            <Label className="text-xs">Max Value</Label>
            <Input
              type="number"
              value={config.max ?? ''}
              onChange={(e) => onChange({ ...config, max: e.target.value ? parseFloat(e.target.value) : undefined })}
              placeholder="No max"
              className="mt-1"
            />
          </div>
        </div>
      );

    case 'TEXT':
      return (
        <div>
          <Label className="text-xs">Max Length</Label>
          <Input
            type="number"
            value={config.max_length ?? ''}
            onChange={(e) => onChange({ ...config, max_length: e.target.value ? parseInt(e.target.value) : undefined })}
            placeholder="No limit"
            min="1"
            className="mt-1"
          />
        </div>
      );

    case 'URL':
      return (
        <div className="p-2 bg-muted/30 rounded text-xs text-muted-foreground">
          URLs will be validated automatically
        </div>
      );

    case 'DATE':
    case 'TEXTAREA':
    case 'EMAIL':
    case 'PHONE':
    case 'CURRENCY':
    case 'FILE':
    default:
      return null;
  }
};
