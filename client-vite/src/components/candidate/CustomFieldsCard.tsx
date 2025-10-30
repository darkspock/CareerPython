import { useState } from 'react';
import { Edit2, Save, X, Calendar, DollarSign, Hash, Mail, Phone, Globe, FileText, CheckSquare, ChevronDown } from 'lucide-react';

interface CustomFieldValue {
  id: string | null;
  field_id: string;
  field_name: string;
  field_type: string;
  field_config: Record<string, any> | null;
  value: any;
  created_at: string | null;
  updated_at: string | null;
}

interface CustomFieldsCardProps {
  customFieldValues: Record<string, CustomFieldValue>;
  onUpdateValue?: (fieldKey: string, value: any) => void;
  isEditable?: boolean;
}

const getFieldIcon = (fieldType: string) => {
  switch (fieldType) {
    case 'TEXT':
    case 'TEXTAREA':
      return <FileText className="w-4 h-4" />;
    case 'NUMBER':
    case 'CURRENCY':
      return <Hash className="w-4 h-4" />;
    case 'EMAIL':
      return <Mail className="w-4 h-4" />;
    case 'PHONE':
      return <Phone className="w-4 h-4" />;
    case 'URL':
      return <Globe className="w-4 h-4" />;
    case 'DATE':
      return <Calendar className="w-4 h-4" />;
    case 'BOOLEAN':
      return <CheckSquare className="w-4 h-4" />;
    case 'DROPDOWN':
      return <ChevronDown className="w-4 h-4" />;
    default:
      return <FileText className="w-4 h-4" />;
  }
};

const formatFieldValue = (fieldValue: CustomFieldValue): string => {
  const { value, field_type, field_config } = fieldValue;
  
  if (value === null || value === undefined || value === '') {
    return 'Not specified';
  }

  switch (field_type) {
    case 'CURRENCY':
      const currency = field_config?.currency_code || 'USD';
      return `${currency} ${value}`;
    case 'DATE':
      return new Date(value).toLocaleDateString();
    case 'BOOLEAN':
      return value ? 'Yes' : 'No';
    case 'DROPDOWN':
      return String(value);
    case 'NUMBER':
      return value.toLocaleString();
    default:
      return String(value);
  }
};

const renderFieldInput = (
  fieldValue: CustomFieldValue,
  value: any,
  onChange: (value: any) => void
) => {
  const { field_type, field_config } = fieldValue;

  switch (field_type) {
    case 'TEXT':
      return (
        <input
          type="text"
          value={value || ''}
          onChange={(e) => onChange(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      );
    case 'TEXTAREA':
      return (
        <textarea
          value={value || ''}
          onChange={(e) => onChange(e.target.value)}
          rows={3}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      );
    case 'NUMBER':
    case 'CURRENCY':
      return (
        <input
          type="number"
          value={value || ''}
          onChange={(e) => onChange(e.target.value ? Number(e.target.value) : null)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      );
    case 'EMAIL':
      return (
        <input
          type="email"
          value={value || ''}
          onChange={(e) => onChange(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      );
    case 'PHONE':
      return (
        <input
          type="tel"
          value={value || ''}
          onChange={(e) => onChange(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      );
    case 'URL':
      return (
        <input
          type="url"
          value={value || ''}
          onChange={(e) => onChange(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      );
    case 'DATE':
      return (
        <input
          type="date"
          value={value ? new Date(value).toISOString().split('T')[0] : ''}
          onChange={(e) => onChange(e.target.value || null)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      );
    case 'BOOLEAN':
      return (
        <div className="flex items-center">
          <input
            type="checkbox"
            checked={value || false}
            onChange={(e) => onChange(e.target.checked)}
            className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
          />
          <span className="ml-2 text-sm text-gray-700">
            {value ? 'Yes' : 'No'}
          </span>
        </div>
      );
    case 'DROPDOWN':
      const options = field_config?.options || [];
      return (
        <select
          value={value || ''}
          onChange={(e) => onChange(e.target.value || null)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">Select an option</option>
          {options.map((option: string, index: number) => (
            <option key={index} value={option}>
              {option}
            </option>
          ))}
        </select>
      );
      default:
        return (
        <input
          type="text"
          value={value || ''}
          onChange={(e) => onChange(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      );
  }
};

export default function CustomFieldsCard({ 
  customFieldValues, 
  onUpdateValue, 
  isEditable = false 
}: CustomFieldsCardProps) {
  const [editingField, setEditingField] = useState<string | null>(null);
  const [editingValue, setEditingValue] = useState<any>(null);

  const handleEdit = (fieldKey: string, fieldValue: CustomFieldValue) => {
    setEditingField(fieldKey);
    setEditingValue(fieldValue.value);
  };

  const handleSave = (fieldKey: string) => {
    if (onUpdateValue) {
      onUpdateValue(fieldKey, editingValue);
    }
    setEditingField(null);
    setEditingValue(null);
  };

  const handleCancel = () => {
    setEditingField(null);
    setEditingValue(null);
  };

  if (!customFieldValues || Object.keys(customFieldValues).length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Additional Data</h3>
        <p className="text-gray-500 text-sm">No additional data configured for this candidate.</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Additional Data</h3>
      <div className="space-y-4">
        {Object.entries(customFieldValues).map(([fieldKey, fieldValue]) => (
          <div key={fieldKey} className="border-b border-gray-100 pb-4 last:border-b-0">
            <div className="flex items-start justify-between">
              <div className="flex items-center space-x-2 mb-2">
                {getFieldIcon(fieldValue.field_type)}
                <span className="font-medium text-gray-900">{fieldValue.field_name}</span>
                <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">
                  {fieldValue.field_type}
                </span>
              </div>
              {isEditable && (
                <button
                  onClick={() => handleEdit(fieldKey, fieldValue)}
                  className="text-blue-600 hover:text-blue-800 text-sm"
                >
                  <Edit2 className="w-4 h-4" />
                </button>
              )}
            </div>
            
            {editingField === fieldKey ? (
              <div className="space-y-3">
                {renderFieldInput(fieldValue, editingValue, setEditingValue)}
                <div className="flex space-x-2">
                  <button
                    onClick={() => handleSave(fieldKey)}
                    className="px-3 py-1 bg-blue-600 text-white text-sm rounded-md hover:bg-blue-700 flex items-center space-x-1"
                  >
                    <Save className="w-3 h-3" />
                    <span>Save</span>
                  </button>
                  <button
                    onClick={handleCancel}
                    className="px-3 py-1 bg-gray-300 text-gray-700 text-sm rounded-md hover:bg-gray-400 flex items-center space-x-1"
                  >
                    <X className="w-3 h-3" />
                    <span>Cancel</span>
                  </button>
                </div>
              </div>
            ) : (
              <div className="text-gray-700">
                {formatFieldValue(fieldValue)}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
