import React, { useState, useEffect, useRef } from 'react';
import { useTranslation } from 'react-i18next';
import { ChevronDown, ChevronUp, Settings2 } from 'lucide-react';
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
  contextType: EntityCustomizationType;
  contexts: Array<{ id: string; name: string }>;
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
  entityId,
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
  const [expandedFields, setExpandedFields] = useState<Set<string>>(new Set());
  const isInitializedRef = useRef(false);
  const lastEntityIdRef = useRef<string | null>(null);

  const getCellKey = (contextId: string, fieldId: string) => `${contextId}-${fieldId}`;

  useEffect(() => {
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

        const stagesData = await companyWorkflowService.listStagesByWorkflow(entityId);
        setStages(stagesData);

        const newMatrix = new Map<string, MatrixCell>();

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

  // Check if a property is uniform across all stages for a field
  const isPropertyUniform = (fieldId: string, propertyKey: FieldPropertyKey): boolean => {
    if (contexts.length <= 1) return true;

    let firstValue: boolean | null = null;
    for (const context of contexts) {
      const cellKey = getCellKey(context.id, fieldId);
      const cell = matrix.get(cellKey);
      const value = cell?.properties[propertyKey] ?? DEFAULT_FIELD_PROPERTIES[propertyKey];

      if (firstValue === null) {
        firstValue = value;
      } else if (value !== firstValue) {
        return false;
      }
    }
    return true;
  };

  // Get the uniform value for a property (assumes isPropertyUniform returned true)
  const getUniformPropertyValue = (fieldId: string, propertyKey: FieldPropertyKey): boolean => {
    const firstContext = contexts[0];
    if (!firstContext) return DEFAULT_FIELD_PROPERTIES[propertyKey];

    const cellKey = getCellKey(firstContext.id, fieldId);
    const cell = matrix.get(cellKey);
    return cell?.properties[propertyKey] ?? DEFAULT_FIELD_PROPERTIES[propertyKey];
  };

  // Check if field has any non-uniform properties
  const hasAdvancedConfig = (fieldId: string): boolean => {
    return FIELD_PROPERTY_KEYS.some(key => !isPropertyUniform(fieldId, key));
  };

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

      const stage = stages.find(s => s.id === contextId);
      if (!stage) {
        throw new Error('Stage not found');
      }

      const currentConfig: FieldPropertiesConfig = stage.field_properties_config || {};
      const updatedConfig: FieldPropertiesConfig = {
        ...currentConfig,
        [fieldId]: newProperties
      };

      await companyWorkflowService.updateStage(contextId, {
        name: stage.name,
        description: stage.description || '',
        stage_type: stage.stage_type,
        allow_skip: stage.allow_skip,
        estimated_duration_days: stage.estimated_duration_days ?? undefined,
        field_properties_config: updatedConfig
      });

      setStages(prev => prev.map(s =>
        s.id === contextId
          ? { ...s, field_properties_config: updatedConfig }
          : s
      ));

      setError(null);
    } catch (err) {
      setError(`Failed to update field property`);
      console.error(err);
      const newMatrix = new Map(matrix);
      newMatrix.set(cellKey, cell);
      setMatrix(newMatrix);
    } finally {
      setSavingCell(null);
    }
  };

  // Update property for ALL stages at once (for uniform properties)
  const handleUniformPropertyChange = async (
    fieldId: string,
    propertyKey: FieldPropertyKey,
    newValue: boolean
  ) => {
    try {
      setSavingCell(`uniform-${fieldId}-${propertyKey}`);

      // First, update all local state at once
      const newMatrix = new Map(matrix);
      const updatedStages = [...stages];
      const apiCalls: Promise<unknown>[] = [];

      for (const context of contexts) {
        const cellKey = getCellKey(context.id, fieldId);
        const cell = matrix.get(cellKey);
        if (!cell) continue;

        const newProperties = {
          ...cell.properties,
          [propertyKey]: newValue
        };

        // Update matrix
        newMatrix.set(cellKey, {
          ...cell,
          properties: newProperties
        });

        const stageIndex = updatedStages.findIndex(s => s.id === context.id);
        if (stageIndex === -1) continue;

        const stage = updatedStages[stageIndex];
        const currentConfig: FieldPropertiesConfig = stage.field_properties_config || {};
        const updatedConfig: FieldPropertiesConfig = {
          ...currentConfig,
          [fieldId]: newProperties
        };

        // Update local stages array
        updatedStages[stageIndex] = { ...stage, field_properties_config: updatedConfig };

        // Queue API call
        apiCalls.push(
          companyWorkflowService.updateStage(context.id, {
            name: stage.name,
            description: stage.description || '',
            stage_type: stage.stage_type,
            allow_skip: stage.allow_skip,
            estimated_duration_days: stage.estimated_duration_days ?? undefined,
            field_properties_config: updatedConfig
          })
        );
      }

      // Apply all local state changes at once
      setMatrix(newMatrix);
      setStages(updatedStages);

      // Execute all API calls in parallel
      await Promise.all(apiCalls);

      setError(null);
    } catch (err) {
      setError(`Failed to update field property`);
      console.error(err);
    } finally {
      setSavingCell(null);
    }
  };

  const toggleFieldExpanded = (fieldId: string) => {
    setExpandedFields(prev => {
      const newSet = new Set(prev);
      if (newSet.has(fieldId)) {
        newSet.delete(fieldId);
      } else {
        newSet.add(fieldId);
      }
      return newSet;
    });
  };

  if (isLoading) {
    return <div className="p-4 text-center">{t('customization.fieldMatrix.loading', 'Loading field properties...')}</div>;
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
          {t('customization.fieldMatrix.description', 'Configure field properties. Use advanced settings to customize per stage.')}
        </p>
      </div>

      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded text-red-600">
          {error}
        </div>
      )}

      {/* Simplified Field List */}
      <div className="space-y-3">
        {fields.map((field) => {
          const isExpanded = expandedFields.has(field.id);
          const hasAdvanced = hasAdvancedConfig(field.id);
          const isSavingField = savingCell?.startsWith(`uniform-${field.id}`) ||
            contexts.some(c => savingCell === getCellKey(c.id, field.id));

          return (
            <div
              key={field.id}
              className="border rounded-lg bg-white overflow-hidden"
            >
              {/* Field Header */}
              <div className="px-4 py-3 bg-gray-50 border-b">
                <div className="flex items-center justify-between">
                  <div>
                    <div className="font-medium text-gray-900">{field.field_name}</div>
                    <div className="text-xs text-gray-500">{field.field_key}</div>
                  </div>
                  {hasAdvanced && (
                    <span className="text-xs bg-amber-100 text-amber-700 px-2 py-1 rounded">
                      {t('customization.fieldMatrix.customPerStage', 'Custom per stage')}
                    </span>
                  )}
                </div>
              </div>

              {/* Simple Properties (uniform across all stages) */}
              <div className="px-4 py-3">
                <div className={`flex flex-wrap gap-4 ${isSavingField ? 'opacity-50' : ''}`}>
                  {FIELD_PROPERTY_KEYS.map((propertyKey) => {
                    const isUniform = isPropertyUniform(field.id, propertyKey);
                    const uniformValue = getUniformPropertyValue(field.id, propertyKey);

                    return (
                      <label
                        key={propertyKey}
                        className="flex items-center gap-2 cursor-pointer hover:bg-gray-50 px-2 py-1 rounded"
                        title={t(`customization.fieldMatrix.propertyDescriptions.${propertyKey}`, getFieldPropertyDescription(propertyKey))}
                      >
                        <input
                          type="checkbox"
                          checked={isUniform ? uniformValue : false}
                          ref={(el) => {
                            // Set indeterminate state when property varies across stages
                            if (el) el.indeterminate = !isUniform;
                          }}
                          onChange={(e) => handleUniformPropertyChange(field.id, propertyKey, e.target.checked)}
                          disabled={isSavingField}
                          className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                        />
                        <span className="text-sm text-gray-700">
                          {t(`customization.fieldMatrix.properties.${propertyKey}`, getFieldPropertyLabel(propertyKey))}
                        </span>
                      </label>
                    );
                  })}
                </div>

                {/* Expand/Collapse for Advanced */}
                {(hasAdvanced || contexts.length > 1) && (
                  <button
                    onClick={() => toggleFieldExpanded(field.id)}
                    className="mt-3 flex items-center gap-1 text-sm text-blue-600 hover:text-blue-700"
                  >
                    <Settings2 className="w-4 h-4" />
                    {isExpanded ? (
                      <>
                        {t('customization.fieldMatrix.hideAdvanced', 'Hide per-stage settings')}
                        <ChevronUp className="w-4 h-4" />
                      </>
                    ) : (
                      <>
                        {t('customization.fieldMatrix.showAdvanced', 'Configure per stage')}
                        <ChevronDown className="w-4 h-4" />
                      </>
                    )}
                  </button>
                )}
              </div>

              {/* Expanded Per-Stage Configuration */}
              {isExpanded && (
                <div className="px-4 py-3 bg-gray-50 border-t">
                  <div className="text-xs font-medium text-gray-500 uppercase mb-3">
                    {t('customization.fieldMatrix.perStageConfig', 'Per-stage configuration')}
                  </div>
                  <div className="space-y-3">
                    {contexts.map((context) => {
                      const cellKey = getCellKey(context.id, field.id);
                      const cell = matrix.get(cellKey);
                      const isSaving = savingCell === cellKey;

                      return (
                        <div key={context.id} className="flex items-center gap-4 py-2 border-b border-gray-200 last:border-0">
                          <div className="w-32 font-medium text-sm text-gray-700">
                            {context.name}
                          </div>
                          <div className={`flex flex-wrap gap-3 ${isSaving ? 'opacity-50' : ''}`}>
                            {FIELD_PROPERTY_KEYS.map((propertyKey) => (
                              <label
                                key={propertyKey}
                                className="flex items-center gap-1.5 cursor-pointer hover:bg-white px-2 py-1 rounded"
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
                                  className="w-3.5 h-3.5 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                                />
                                <span className="text-xs text-gray-600">
                                  {t(`customization.fieldMatrix.properties.${propertyKey}`, getFieldPropertyLabel(propertyKey))}
                                </span>
                              </label>
                            ))}
                          </div>
                          {isSaving && (
                            <span className="text-xs text-gray-500">
                              {t('customization.fieldMatrix.saving', 'Saving...')}
                            </span>
                          )}
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Legend */}
      <div className="p-4 bg-gray-50 rounded text-sm">
        <h4 className="font-medium mb-2">{t('customization.fieldMatrix.legendTitle', 'Property Descriptions:')}</h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
          {FIELD_PROPERTY_KEYS.map((propertyKey) => (
            <div key={propertyKey} className="flex items-start gap-2">
              <span className="px-2 py-0.5 rounded bg-blue-100 text-blue-800 text-xs font-medium whitespace-nowrap">
                {t(`customization.fieldMatrix.properties.${propertyKey}`, getFieldPropertyLabel(propertyKey))}
              </span>
              <span className="text-gray-600 text-xs">
                {t(`customization.fieldMatrix.propertyDescriptions.${propertyKey}`, getFieldPropertyDescription(propertyKey))}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
