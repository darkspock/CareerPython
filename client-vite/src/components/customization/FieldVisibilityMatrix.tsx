import React, { useState, useEffect } from 'react';
import type {
  CustomField,
  FieldConfiguration,
  FieldVisibility,
  EntityCustomizationType
} from '../../types/customization';
import {
  getFieldVisibilityLabel,
  getFieldVisibilityColor
} from '../../types/customization';

interface FieldVisibilityMatrixProps {
  entityType: EntityCustomizationType;
  entityId: string;
  contextType: EntityCustomizationType;  // Type of context (e.g., 'WorkflowStage')
  contexts: Array<{ id: string; name: string }>;  // List of contexts (stages, etc.)
  fields: CustomField[];
  onConfigurationsChange?: (configurations: FieldConfiguration[]) => void;
}

interface MatrixCell {
  contextId: string;
  fieldId: string;
  configuration?: FieldConfiguration;
  visibility: FieldVisibility;
}

export const FieldVisibilityMatrix: React.FC<FieldVisibilityMatrixProps> = ({
  entityType,
  entityId,
  contextType: _contextType, // Not used currently but part of interface
  contexts,
  fields,
  onConfigurationsChange
}) => {
  const [matrix, setMatrix] = useState<Map<string, MatrixCell>>(new Map());
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [savingCell, setSavingCell] = useState<string | null>(null);

  const visibilityOptions: FieldVisibility[] = ['VISIBLE', 'HIDDEN', 'READ_ONLY', 'REQUIRED'];

  useEffect(() => {
    if (contexts.length > 0 && fields.length > 0) {
      loadConfigurations();
    } else {
      setIsLoading(false);
    }
  }, [contexts.length, fields.length, entityType, entityId]);

  const getCellKey = (contextId: string, fieldId: string) => `${contextId}-${fieldId}`;

  const loadConfigurations = async () => {
    if (contexts.length === 0 || fields.length === 0) {
      setIsLoading(false);
      return;
    }

    try {
      setIsLoading(true);
      setError(null);
      const newMatrix = new Map<string, MatrixCell>();

      // TODO: When backend endpoints for field configurations are available,
      // replace this with actual API calls
      // For now, initialize all cells with default visibility
      for (const context of contexts) {
        for (const field of fields) {
          const cellKey = getCellKey(context.id, field.id);
          newMatrix.set(cellKey, {
            contextId: context.id,
            fieldId: field.id,
            configuration: undefined,
            visibility: 'VISIBLE' // Default to VISIBLE
          });
        }
      }

      setMatrix(newMatrix);

      // Notify parent of all configurations
      const allConfigs = Array.from(newMatrix.values())
        .map(cell => cell.configuration)
        .filter((c): c is FieldConfiguration => c !== undefined);
      onConfigurationsChange?.(allConfigs);
    } catch (err) {
      setError('Failed to load field configurations');
      console.error('Error loading field configurations:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleVisibilityChange = async (
    contextId: string,
    fieldId: string,
    newVisibility: FieldVisibility
  ) => {
    const cellKey = getCellKey(contextId, fieldId);
    const cell = matrix.get(cellKey);
    if (!cell) return;

    try {
      setSavingCell(cellKey);

      // TODO: When backend endpoints for field configurations are available,
      // implement actual API calls here
      // For now, just update the local state
      const newMatrix = new Map(matrix);
      newMatrix.set(cellKey, {
        ...cell,
        visibility: newVisibility
      });
      setMatrix(newMatrix);

      setError(null);
    } catch (err) {
      setError(`Failed to update field visibility`);
      console.error(err);
    } finally {
      setSavingCell(null);
    }
  };

  if (isLoading) {
    return <div className="p-4 text-center">Loading field visibility matrix...</div>;
  }

  if (fields.length === 0) {
    return (
      <div className="p-8 text-center text-gray-500 border-2 border-dashed rounded">
        No custom fields yet. Add some fields first to configure their visibility per context.
      </div>
    );
  }

  if (contexts.length === 0) {
    return (
      <div className="p-8 text-center text-gray-500 border-2 border-dashed rounded">
        No contexts defined. Add contexts to configure field visibility.
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div>
        <h3 className="text-lg font-semibold mb-2">Field Visibility by Context</h3>
        <p className="text-sm text-gray-600">
          Configure which fields are visible, hidden, read-only, or required in each context.
        </p>
      </div>

      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded text-red-600">
          {error}
        </div>
      )}

      {/* Matrix Table */}
      <div className="overflow-x-auto border rounded">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider sticky left-0 bg-gray-50 z-10">
                Field
              </th>
              {contexts.map((context) => (
                <th
                  key={context.id}
                  className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider min-w-[150px]"
                >
                  <div>{context.name}</div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {fields.map((field) => (
              <tr key={field.id} className="hover:bg-gray-50">
                <td className="px-4 py-3 text-sm font-medium text-gray-900 sticky left-0 bg-white z-10">
                  <div>{field.field_name}</div>
                  <div className="text-xs text-gray-500">{field.field_key}</div>
                </td>
                {contexts.map((context) => {
                  const cellKey = getCellKey(context.id, field.id);
                  const cell = matrix.get(cellKey);
                  const isSaving = savingCell === cellKey;

                  return (
                    <td key={cellKey} className="px-4 py-3 text-sm">
                      <select
                        value={cell?.visibility || 'VISIBLE'}
                        onChange={(e) =>
                          handleVisibilityChange(
                            context.id,
                            field.id,
                            e.target.value as FieldVisibility
                          )
                        }
                        disabled={isSaving}
                        className={`w-full px-3 py-2 border rounded text-sm ${
                          isSaving ? 'opacity-50' : ''
                        } ${
                          cell?.visibility
                            ? getFieldVisibilityColor(cell.visibility).replace('text-', 'border-')
                            : ''
                        }`}
                      >
                        {visibilityOptions.map((option) => (
                          <option key={option} value={option}>
                            {getFieldVisibilityLabel(option)}
                          </option>
                        ))}
                      </select>
                      {isSaving && (
                        <div className="text-xs text-gray-500 mt-1">Saving...</div>
                      )}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Legend */}
      <div className="p-4 bg-gray-50 rounded">
        <h4 className="font-medium mb-2">Visibility Options:</h4>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
          {visibilityOptions.map((visibility) => (
            <div key={visibility} className="flex items-center gap-2">
              <span className={`px-2 py-1 rounded ${getFieldVisibilityColor(visibility)}`}>
                {getFieldVisibilityLabel(visibility)}
              </span>
              <span className="text-xs text-gray-600">
                {visibility === 'VISIBLE' && '- Can view and edit'}
                {visibility === 'HIDDEN' && '- Not shown'}
                {visibility === 'READ_ONLY' && '- Can view only'}
                {visibility === 'REQUIRED' && '- Must be filled'}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

