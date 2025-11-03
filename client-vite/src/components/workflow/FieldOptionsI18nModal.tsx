import React, { useState, useEffect } from 'react';
import { X, Plus, Trash2, GripVertical, Globe } from 'lucide-react';

export interface FieldOptionLabel {
  language: string;
  label: string;
}

export interface FieldOption {
  id: string;
  sort: number;
  labels: FieldOptionLabel[];
}

interface FieldOptionsI18nModalProps {
  isOpen: boolean;
  options: FieldOption[];
  availableLanguages?: string[]; // e.g., ['en', 'es', 'fr']
  onClose: () => void;
  onSave: (options: FieldOption[]) => void;
}

export const FieldOptionsI18nModal: React.FC<FieldOptionsI18nModalProps> = ({
  isOpen,
  options: initialOptions,
  availableLanguages = ['en', 'es'], // Default languages
  onClose,
  onSave
}) => {
  const [options, setOptions] = useState<FieldOption[]>([]);
  const [draggedIndex, setDraggedIndex] = useState<number | null>(null);

  useEffect(() => {
    if (isOpen) {
      // Deep copy options to avoid mutating props
      setOptions(JSON.parse(JSON.stringify(initialOptions)));
    }
  }, [isOpen, initialOptions]);

  if (!isOpen) return null;

  const handleAddOption = () => {
    const newOption: FieldOption = {
      id: `opt_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      sort: options.length,
      labels: availableLanguages.map(lang => ({
        language: lang,
        label: ''
      }))
    };
    setOptions([...options, newOption]);
  };

  const handleRemoveOption = (index: number) => {
    if (options.length <= 1) {
      alert('At least one option is required');
      return;
    }
    const newOptions = options.filter((_, i) => i !== index);
    // Re-sort remaining options
    const reorderedOptions = newOptions.map((opt, i) => ({
      ...opt,
      sort: i
    }));
    setOptions(reorderedOptions);
  };

  const handleUpdateLabel = (optionIndex: number, language: string, value: string) => {
    const newOptions = [...options];
    const option = newOptions[optionIndex];
    const labelIndex = option.labels.findIndex(l => l.language === language);
    
    if (labelIndex >= 0) {
      option.labels[labelIndex] = { language, label: value };
    } else {
      option.labels.push({ language, label: value });
    }
    
    setOptions(newOptions);
  };

  const handleAddLanguage = (optionIndex: number, language: string) => {
    const newOptions = [...options];
    const option = newOptions[optionIndex];
    
    // Check if language already exists
    if (option.labels.some(l => l.language === language)) {
      return;
    }
    
    option.labels.push({ language, label: '' });
    setOptions(newOptions);
  };

  const handleRemoveLanguage = (optionIndex: number, language: string) => {
    const newOptions = [...options];
    const option = newOptions[optionIndex];
    
    if (option.labels.length <= 1) {
      alert('At least one language is required');
      return;
    }
    
    option.labels = option.labels.filter(l => l.language !== language);
    setOptions(newOptions);
  };

  const handleMoveOption = (fromIndex: number, toIndex: number) => {
    const newOptions = [...options];
    const [moved] = newOptions.splice(fromIndex, 1);
    newOptions.splice(toIndex, 0, moved);
    
    // Update sort indices
    const reorderedOptions = newOptions.map((opt, i) => ({
      ...opt,
      sort: i
    }));
    
    setOptions(reorderedOptions);
  };

  const handleDragStart = (index: number) => {
    setDraggedIndex(index);
  };

  const handleDragOver = (e: React.DragEvent, index: number) => {
    e.preventDefault();
    if (draggedIndex === null || draggedIndex === index) return;
    
    handleMoveOption(draggedIndex, index);
    setDraggedIndex(index);
  };

  const handleDragEnd = () => {
    setDraggedIndex(null);
  };

  const handleSave = () => {
    // Validate all options have at least one label filled
    for (const option of options) {
      const hasLabel = option.labels.some(l => l.label.trim() !== '');
      if (!hasLabel) {
        alert(`Option at position ${option.sort + 1} must have at least one label`);
        return;
      }
    }
    
    onSave(options);
  };

  const getLabelForLanguage = (option: FieldOption, language: string): string => {
    const label = option.labels.find(l => l.language === language);
    return label?.label || '';
  };

  const getAllLanguages = (): string[] => {
    const languagesSet = new Set<string>();
    availableLanguages.forEach(lang => languagesSet.add(lang));
    options.forEach(opt => {
      opt.labels.forEach(label => languagesSet.add(label.language));
    });
    return Array.from(languagesSet).sort();
  };

  const allLanguages = getAllLanguages();

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      <div className="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
        {/* Background overlay */}
        <div
          className="fixed inset-0 transition-opacity bg-gray-500 bg-opacity-75"
          onClick={onClose}
        />

        {/* Modal panel */}
        <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-4xl sm:w-full">
          <div className="bg-white px-6 py-6">
            {/* Header */}
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center gap-2">
                <Globe className="w-5 h-5 text-blue-600" />
                <h3 className="text-lg font-semibold text-gray-900">
                  Edit Field Options (i18n)
                </h3>
              </div>
              <button
                type="button"
                onClick={onClose}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Options List */}
            <div className="space-y-4 max-h-96 overflow-y-auto">
              {options.map((option, optionIndex) => (
                <div
                  key={option.id}
                  draggable
                  onDragStart={() => handleDragStart(optionIndex)}
                  onDragOver={(e) => handleDragOver(e, optionIndex)}
                  onDragEnd={handleDragEnd}
                  className={`border rounded-lg p-4 bg-gray-50 hover:bg-gray-100 transition-colors ${
                    draggedIndex === optionIndex ? 'opacity-50' : ''
                  }`}
                >
                  <div className="flex items-start gap-3">
                    {/* Drag handle */}
                    <div className="cursor-move pt-2">
                      <GripVertical className="w-5 h-5 text-gray-400" />
                    </div>

                    {/* Option content */}
                    <div className="flex-1 space-y-3">
                      {/* Language labels */}
                      <div className="space-y-2">
                        {allLanguages.map((language) => {
                          const label = getLabelForLanguage(option, language);
                          const isDefaultLang = availableLanguages.includes(language);
                          
                          return (
                            <div key={language} className="flex items-center gap-2">
                              <span className="w-16 text-xs font-medium text-gray-600 uppercase">
                                {language}:
                              </span>
                              <input
                                type="text"
                                value={label}
                                onChange={(e) => handleUpdateLabel(optionIndex, language, e.target.value)}
                                className="flex-1 px-3 py-1.5 border border-gray-300 rounded text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                placeholder={`Label in ${language}`}
                              />
                              {!isDefaultLang && (
                                <button
                                  type="button"
                                  onClick={() => handleRemoveLanguage(optionIndex, language)}
                                  className="text-red-600 hover:text-red-700"
                                  title="Remove language"
                                >
                                  <X className="w-4 h-4" />
                                </button>
                              )}
                            </div>
                          );
                        })}
                      </div>

                      {/* Add language button */}
                      <div className="flex items-center gap-2">
                        <select
                          value=""
                          onChange={(e) => {
                            if (e.target.value) {
                              handleAddLanguage(optionIndex, e.target.value);
                              e.target.value = '';
                            }
                          }}
                          className="text-xs px-2 py-1 border border-gray-300 rounded"
                        >
                          <option value="">Add language...</option>
                          {['fr', 'de', 'it', 'pt', 'ru', 'zh', 'ja', 'ko'].map(lang => {
                            if (allLanguages.includes(lang)) return null;
                            return (
                              <option key={lang} value={lang}>
                                {lang.toUpperCase()}
                              </option>
                            );
                          })}
                        </select>
                      </div>
                    </div>

                    {/* Remove option button */}
                    <button
                      type="button"
                      onClick={() => handleRemoveOption(optionIndex)}
                      className="text-red-600 hover:text-red-700 p-2"
                      title="Remove option"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              ))}
            </div>

            {/* Add option button */}
            <div className="mt-4">
              <button
                type="button"
                onClick={handleAddOption}
                className="flex items-center gap-2 px-4 py-2 text-sm text-blue-600 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors"
              >
                <Plus className="w-4 h-4" />
                Add Option
              </button>
            </div>

            {/* Footer */}
            <div className="mt-6 flex justify-end gap-3">
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handleSave}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                Save Options
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FieldOptionsI18nModal;

