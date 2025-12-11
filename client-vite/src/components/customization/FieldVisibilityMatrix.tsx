import React, { useState, useEffect, useRef } from 'react';
import { useTranslation } from 'react-i18next';
import { companyWorkflowService } from '../../services/companyWorkflowService';
import type {
  CustomField,
  FieldConfiguration,
  FieldProperties,
  FieldPropertyKey,
  EntityCustomizationType
} from '../../types/customization';
import type { WorkflowStage, FieldPropertiesConfig } from '../../types/workflow';
import {
  DEFAULT_FIELD_PROPERTIES,
  FIELD_PROPERTY_KEYS,
  getFieldPropertyLabel,
  getFieldPropertyDescription
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
  properties: FieldProperties;
}

export const FieldVisibilityMatrix: React.FC<FieldVisibilityMatrixProps> = ({
  entityType,
  entityId,
  contextType: _contextType, // Not used currently but part of interface
  contexts,
  fields,
  onConfigurationsChange
}) => {
  const { t } = useTranslation();
  const [matrix, setMatrix] = useState<Map<string, MatrixCell>>(new Map());
  const [stages, setStages] = useState<WorkflowStage[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [savingCell, setSavingCell] = useState<string | null>(null);
  const isInitializedRef = useRef(false);
  const lastEntityIdRef = useRef<string | null>(null);

  const getCellKey = (contextId: string, fieldId: string) => `${contextId}-${fieldId}`;

  useEffect(() => {
    // Only load if we have contexts and fields, and either:
    // 1. Not initialized yet, or
    // 2. EntityId changed
    const shouldLoad = contexts.length > 0 && fields.length > 0 &&
      (!isInitializedRef.current || lastEntityIdRef.current !== entityId);

    if (!shouldLoad) {
      if (contexts.length === 0 || fields.length === 0) {
        setIsLoading(false);
      }
      return;
    }

    const loadConfigurations = async () => {
      try {
        setIsLoading(true);
        setError(null);

        // Load stages to get their current field_properties_config
        const stagesData = await companyWorkflowService.listStagesByWorkflow(entityId);
        setStages(stagesData);

        const newMatrix = new Map<string, MatrixCell>();

        // Initialize matrix cells from stages' field_properties_config
        for (const context of contexts) {
          const stage = stagesData.find(s => s.id === context.id);
          const stageConfig = stage?.field_properties_config || {};

          for (const field of fields) {
            const cellKey = getCellKey(context.id, field.id);
            const fieldConfig = stageConfig[field.id];

            newMatrix.set(cellKey, {
              contextId: context.id,
              fieldId: field.id,
              configuration: undefined,
              properties: fieldConfig || { ...DEFAULT_FIELD_PROPERTIES }
            });
          }
        }

        setMatrix(newMatrix);
        isInitializedRef.current = true;
        lastEntityIdRef.current = entityId;

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

    loadConfigurations();
  }, [entityId, contexts, fields, onConfigurationsChange]);

  const handlePropertyChange = async (
    contextId: string,
    fieldId: string,
    propertyKey: FieldPropertyKey,
    newValue: boolean
  ) => {
    const cellKey = getCellKey(contextId, fieldId);
    const cell = matrix.get(cellKey);
    if (!cell) return;

    try {
      setSavingCell(cellKey);

      // Update local state first
      const newProperties = {
        ...cell.properties,
        [propertyKey]: newValue
      };

      const newMatrix = new Map(matrix);
      newMatrix.set(cellKey, {
        ...cell,
        properties: newProperties
      });
      setMatrix(newMatrix);

      // Get the stage to update
      const stage = stages.find(s => s.id === contextId);
      if (!stage) {
        throw new Error('Stage not found');
      }

      // Build the new field_properties_config for this stage
      const currentConfig: FieldPropertiesConfig = stage.field_properties_config || {};
      const updatedConfig: FieldPropertiesConfig = {
        ...currentConfig,
        [fieldId]: newProperties
      };

      // Save to backend via updateStage
      await companyWorkflowService.updateStage(contextId, {
        name: stage.name,
        description: stage.description || '',
        stage_type: stage.stage_type,
        allow_skip: stage.allow_skip,
        estimated_duration_days: stage.estimated_duration_days ?? undefined,
        field_properties_config: updatedConfig
      });

      // Update local stages cache
      setStages(prev => prev.map(s =>
        s.id === contextId
          ? { ...s, field_properties_config: updatedConfig }
          : s
      ));

      setError(null);
    } catch (err) {
      setError(`Failed to update field property`);
      console.error(err);
      // Revert local state on error
      const newMatrix = new Map(matrix);
      newMatrix.set(cellKey, cell);
      setMatrix(newMatrix);
    } finally {
      setSavingCell(null);
    }
  };

  if (isLoading) {
    return <div className="p-4 text-center">{t('customization.fieldMatrix.loading', 'Loading field properties matrix...')}</div>;
  }

  if (fields.length === 0) {
    return (
      <div className="p-8 text-center text-gray-500 border-2 border-dashed rounded">
        {t('customization.fieldMatrix.noFields', 'No custom fields yet. Add some fields first to configure their properties per context.')}
      </div>
    );
  }

  if (contexts.length === 0) {
    return (
      <div className="p-8 text-center text-gray-500 border-2 border-dashed rounded">
        {t('customization.fieldMatrix.noContexts', 'No contexts defined. Add contexts to configure field properties.')}
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div>
        <h3 className="text-lg font-semibold mb-2">
          {t('customization.fieldMatrix.title', 'Field Properties by Context')}
        </h3>
        <p className="text-sm text-gray-600">
          {t('customization.fieldMatrix.description', 'Configure field properties for each context (stage).')}
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
                {t('customization.fieldMatrix.field', 'Field')}
              </th>
              {contexts.map((context) => (
                <th
                  key={context.id}
                  className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider min-w-[200px]"
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
                      <div className={`space-y-2 ${isSaving ? 'opacity-50' : ''}`}>
                        {FIELD_PROPERTY_KEYS.map((propertyKey) => (
                          <label
                            key={propertyKey}
                            className="flex items-center gap-2 cursor-pointer hover:bg-gray-50 p-1 rounded"
                          >
                            <input
                              type="checkbox"
                              checked={cell?.properties[propertyKey] ?? DEFAULT_FIELD_PROPERTIES[propertyKey]}
                              onChange={(e) =>
                                handlePropertyChange(
                                  context.id,
                                  field.id,
                                  propertyKey,
                                  e.target.checked
                                )
                              }
                              disabled={isSaving}
                              className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                            />
                            <span className="text-xs text-gray-700">
                              {t(`customization.fieldMatrix.properties.${propertyKey}`, getFieldPropertyLabel(propertyKey))}
                            </span>
                          </label>
                        ))}
                      </div>
                      {isSaving && (
                        <div className="text-xs text-gray-500 mt-1">
                          {t('customization.fieldMatrix.saving', 'Saving...')}
                        </div>
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
        <h4 className="font-medium mb-2">{t('customization.fieldMatrix.legendTitle', 'Property Descriptions:')}</h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
          {FIELD_PROPERTY_KEYS.map((propertyKey) => (
            <div key={propertyKey} className="flex items-start gap-2">
              <span className="px-2 py-1 rounded bg-blue-100 text-blue-800 font-medium whitespace-nowrap">
                {t(`customization.fieldMatrix.properties.${propertyKey}`, getFieldPropertyLabel(propertyKey))}
              </span>
              <span className="text-gray-600">
                {t(`customization.fieldMatrix.propertyDescriptions.${propertyKey}`, getFieldPropertyDescription(propertyKey))}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
