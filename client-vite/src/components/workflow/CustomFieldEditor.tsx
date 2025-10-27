import React, { useState, useEffect } from 'react';
import type {
  CustomField,
  FieldType,
  CreateCustomFieldRequest,
  UpdateCustomFieldRequest
} from '../../types/workflow';
import { getFieldTypeLabel } from '../../types/workflow';
import { CustomFieldService } from '../../services/customFieldService';
import { FieldConfigEditor } from './FieldConfigEditor';

interface CustomFieldEditorProps {
  workflowId: string;
  onFieldsChange?: (fields: CustomField[]) => void;
}

export const CustomFieldEditor: React.FC<CustomFieldEditorProps> = ({
  workflowId,
  onFieldsChange
}) => {
  const [fields, setFields] = useState<CustomField[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [editingField, setEditingField] = useState<CustomField | null>(null);
  const [isAddingNew, setIsAddingNew] = useState(false);

  // Form state for new/edit field
  const [formData, setFormData] = useState({
    field_name: '',
    field_key: '',
    field_type: 'TEXT' as FieldType,
    field_config: {} as Record<string, any>
  });

  const fieldTypes: FieldType[] = [
    'TEXT',
    'TEXT_AREA',
    'NUMBER',
    'CURRENCY',
    'DATE',
    'DROPDOWN',
    'MULTI_SELECT',
    'RADIO',
    'CHECKBOX',
    'FILE'
  ];

  useEffect(() => {
    loadFields();
  }, [workflowId]);

  const loadFields = async () => {
    try {
      setIsLoading(true);
      const loadedFields = await CustomFieldService.listCustomFieldsByWorkflow(workflowId);
      setFields(loadedFields);
      onFieldsChange?.(loadedFields);
      setError(null);
    } catch (err) {
      setError('Failed to load custom fields');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFieldNameChange = (value: string) => {
    const fieldKey = CustomFieldService.generateFieldKey(value);
    setFormData(prev => ({
      ...prev,
      field_name: value,
      field_key: fieldKey
    }));
  };

  const handleAddNew = () => {
    setIsAddingNew(true);
    setEditingField(null);
    setFormData({
      field_name: '',
      field_key: '',
      field_type: 'TEXT',
      field_config: {}
    });
  };

  const handleEdit = (field: CustomField) => {
    setEditingField(field);
    setIsAddingNew(false);
    setFormData({
      field_name: field.field_name,
      field_key: field.field_key,
      field_type: field.field_type,
      field_config: field.field_config || {}
    });
  };

  const handleCancel = () => {
    setIsAddingNew(false);
    setEditingField(null);
    setFormData({
      field_name: '',
      field_key: '',
      field_type: 'TEXT',
      field_config: {}
    });
  };

  const handleSave = async () => {
    try {
      if (isAddingNew) {
        const request: CreateCustomFieldRequest = {
          workflow_id: workflowId,
          field_key: formData.field_key,
          field_name: formData.field_name,
          field_type: formData.field_type,
          field_config: Object.keys(formData.field_config).length > 0 ? formData.field_config : undefined,
          order_index: fields.length
        };
        await CustomFieldService.createCustomField(request);
      } else if (editingField) {
        const request: UpdateCustomFieldRequest = {
          field_name: formData.field_name,
          field_type: formData.field_type,
          field_config: Object.keys(formData.field_config).length > 0 ? formData.field_config : undefined
        };
        await CustomFieldService.updateCustomField(editingField.id, request);
      }
      await loadFields();
      handleCancel();
    } catch (err) {
      setError('Failed to save custom field');
      console.error(err);
    }
  };

  const handleDelete = async (fieldId: string) => {
    if (!confirm('Are you sure you want to delete this field?')) return;

    try {
      await CustomFieldService.deleteCustomField(fieldId);
      await loadFields();
    } catch (err) {
      setError('Failed to delete custom field');
      console.error(err);
    }
  };

  const handleMoveUp = async (field: CustomField) => {
    if (field.order_index === 0) return;

    try {
      await CustomFieldService.reorderCustomField(field.id, {
        new_order_index: field.order_index - 1
      });
      await loadFields();
    } catch (err) {
      setError('Failed to reorder field');
      console.error(err);
    }
  };

  const handleMoveDown = async (field: CustomField) => {
    if (field.order_index === fields.length - 1) return;

    try {
      await CustomFieldService.reorderCustomField(field.id, {
        new_order_index: field.order_index + 1
      });
      await loadFields();
    } catch (err) {
      setError('Failed to reorder field');
      console.error(err);
    }
  };

  if (isLoading) {
    return <div className="p-4 text-center">Loading custom fields...</div>;
  }

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h3 className="text-lg font-semibold">Custom Fields</h3>
        {!isAddingNew && !editingField && (
          <button
            onClick={handleAddNew}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Add Field
          </button>
        )}
      </div>

      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded text-red-600">
          {error}
        </div>
      )}

      {/* Add/Edit Form */}
      {(isAddingNew || editingField) && (
        <div className="p-4 border rounded bg-gray-50">
          <h4 className="font-semibold mb-4">
            {isAddingNew ? 'Add New Field' : 'Edit Field'}
          </h4>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">
                Field Name *
              </label>
              <input
                type="text"
                value={formData.field_name}
                onChange={(e) => handleFieldNameChange(e.target.value)}
                className="w-full px-3 py-2 border rounded"
                placeholder="e.g., Expected Salary"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">
                Field Key * (auto-generated)
              </label>
              <input
                type="text"
                value={formData.field_key}
                onChange={(e) => setFormData(prev => ({ ...prev, field_key: e.target.value }))}
                className="w-full px-3 py-2 border rounded bg-gray-100"
                placeholder="e.g., expected_salary"
                disabled={!isAddingNew}
              />
              <p className="text-xs text-gray-500 mt-1">
                Used as identifier in database. Can only be set when creating.
              </p>
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">
                Field Type *
              </label>
              <select
                value={formData.field_type}
                onChange={(e) => setFormData(prev => ({
                  ...prev,
                  field_type: e.target.value as FieldType,
                  field_config: {} // Reset config when changing type
                }))}
                className="w-full px-3 py-2 border rounded"
              >
                {fieldTypes.map(type => (
                  <option key={type} value={type}>
                    {getFieldTypeLabel(type)}
                  </option>
                ))}
              </select>
            </div>

            {/* Field Configuration Editor */}
            <FieldConfigEditor
              fieldType={formData.field_type}
              config={formData.field_config}
              onChange={(newConfig) => setFormData(prev => ({ ...prev, field_config: newConfig }))}
            />

            <div className="flex gap-2">
              <button
                onClick={handleSave}
                disabled={!formData.field_name || !formData.field_key}
                className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-gray-400"
              >
                Save
              </button>
              <button
                onClick={handleCancel}
                className="px-4 py-2 bg-gray-300 text-gray-700 rounded hover:bg-gray-400"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Fields List */}
      <div className="space-y-2">
        {fields.length === 0 ? (
          <div className="p-8 text-center text-gray-500 border-2 border-dashed rounded">
            No custom fields yet. Click "Add Field" to create one.
          </div>
        ) : (
          fields.map((field) => (
            <div
              key={field.id}
              className="flex items-center justify-between p-4 border rounded hover:bg-gray-50"
            >
              <div className="flex-1">
                <div className="font-medium">{field.field_name}</div>
                <div className="text-sm text-gray-500">
                  {field.field_key} • {getFieldTypeLabel(field.field_type)}
                </div>
              </div>

              <div className="flex gap-2">
                <button
                  onClick={() => handleMoveUp(field)}
                  disabled={field.order_index === 0}
                  className="p-2 hover:bg-gray-200 rounded disabled:opacity-30"
                  title="Move up"
                >
                  ↑
                </button>
                <button
                  onClick={() => handleMoveDown(field)}
                  disabled={field.order_index === fields.length - 1}
                  className="p-2 hover:bg-gray-200 rounded disabled:opacity-30"
                  title="Move down"
                >
                  ↓
                </button>
                <button
                  onClick={() => handleEdit(field)}
                  className="px-3 py-1 bg-blue-100 text-blue-700 rounded hover:bg-blue-200"
                >
                  Edit
                </button>
                <button
                  onClick={() => handleDelete(field.id)}
                  className="px-3 py-1 bg-red-100 text-red-700 rounded hover:bg-red-200"
                >
                  Delete
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
