import React, { useState, useEffect } from 'react';
import { Plus, X, AlertCircle, CheckCircle, Edit2, Trash2 } from 'lucide-react';
import { ValidationRuleService } from '../../services/validationRuleService';
import type {
  ValidationRule,
  CreateValidationRuleRequest,
  UpdateValidationRuleRequest,
  CustomField,
  WorkflowStage,
  ValidationRuleType,
  ComparisonOperator,
  ValidationSeverity
} from '../../types/workflow';
import {
  getValidationRuleTypeLabel,
  getComparisonOperatorLabel,
  getValidationSeverityLabel,
  getValidationSeverityColor
} from '../../types/workflow';

interface ValidationRuleEditorProps {
  workflowId: string;
  stages: WorkflowStage[];
  customFields: CustomField[];
  onRulesChange?: () => void;
}

interface EditingRule {
  id?: string;
  custom_field_id: string;
  stage_id: string;
  rule_type: ValidationRuleType;
  comparison_operator: ComparisonOperator;
  severity: ValidationSeverity;
  validation_message: string;
  position_field_path: string;
  comparison_value: any;
  auto_reject: boolean;
  rejection_reason: string;
  is_active: boolean;
}

const RULE_TYPES: ValidationRuleType[] = ['compare_position_field', 'range', 'pattern', 'custom'];
const COMPARISON_OPERATORS: ComparisonOperator[] = ['gt', 'gte', 'lt', 'lte', 'eq', 'neq', 'in_range', 'out_range', 'contains', 'not_contains'];
const SEVERITIES: ValidationSeverity[] = ['warning', 'error'];

export const ValidationRuleEditor: React.FC<ValidationRuleEditorProps> = ({
  workflowId: _workflowId,
  stages,
  customFields,
  onRulesChange
}) => {
  const [rules, setRules] = useState<ValidationRule[]>([]);
  const [selectedStageId, setSelectedStageId] = useState<string>('');
  const [isAddingRule, setIsAddingRule] = useState(false);
  const [editingRule, setEditingRule] = useState<EditingRule | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (selectedStageId) {
      loadRules(selectedStageId);
    }
  }, [selectedStageId]);

  const loadRules = async (stageId: string) => {
    try {
      setLoading(true);
      const data = await ValidationRuleService.listValidationRulesByStage(stageId);
      setRules(data);
    } catch (err) {
      setError('Error loading validation rules');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleAddRule = () => {
    setEditingRule({
      custom_field_id: customFields[0]?.id || '',
      stage_id: selectedStageId,
      rule_type: 'compare_position_field',
      comparison_operator: 'lte',
      severity: 'error',
      validation_message: '',
      position_field_path: '',
      comparison_value: null,
      auto_reject: false,
      rejection_reason: '',
      is_active: true
    });
    setIsAddingRule(true);
  };

  const handleEditRule = (rule: ValidationRule) => {
    setEditingRule({
      id: rule.id,
      custom_field_id: rule.custom_field_id,
      stage_id: rule.stage_id,
      rule_type: rule.rule_type,
      comparison_operator: rule.comparison_operator,
      severity: rule.severity,
      validation_message: rule.validation_message,
      position_field_path: rule.position_field_path || '',
      comparison_value: rule.comparison_value,
      auto_reject: rule.auto_reject,
      rejection_reason: rule.rejection_reason || '',
      is_active: rule.is_active
    });
    setIsAddingRule(false);
  };

  const handleSaveRule = async () => {
    if (!editingRule) return;

    try {
      setLoading(true);
      setError(null);

      if (isAddingRule) {
        const request: CreateValidationRuleRequest = {
          custom_field_id: editingRule.custom_field_id,
          stage_id: editingRule.stage_id,
          rule_type: editingRule.rule_type,
          comparison_operator: editingRule.comparison_operator,
          severity: editingRule.severity,
          validation_message: editingRule.validation_message,
          position_field_path: editingRule.position_field_path || undefined,
          comparison_value: editingRule.comparison_value || undefined,
          auto_reject: editingRule.auto_reject,
          rejection_reason: editingRule.rejection_reason || undefined,
          is_active: editingRule.is_active
        };
        await ValidationRuleService.createValidationRule(request);
      } else if (editingRule.id) {
        const request: UpdateValidationRuleRequest = {
          comparison_operator: editingRule.comparison_operator,
          severity: editingRule.severity,
          validation_message: editingRule.validation_message,
          position_field_path: editingRule.position_field_path || undefined,
          comparison_value: editingRule.comparison_value || undefined,
          auto_reject: editingRule.auto_reject,
          rejection_reason: editingRule.rejection_reason || undefined,
          is_active: editingRule.is_active
        };
        await ValidationRuleService.updateValidationRule(editingRule.id, request);
      }

      await loadRules(selectedStageId);
      setEditingRule(null);
      setIsAddingRule(false);
      onRulesChange?.();
    } catch (err) {
      setError('Error saving validation rule');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteRule = async (ruleId: string) => {
    if (!confirm('Are you sure you want to delete this validation rule?')) return;

    try {
      setLoading(true);
      await ValidationRuleService.deleteValidationRule(ruleId);
      await loadRules(selectedStageId);
      onRulesChange?.();
    } catch (err) {
      setError('Error deleting validation rule');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleToggleActive = async (rule: ValidationRule) => {
    try {
      setLoading(true);
      if (rule.is_active) {
        await ValidationRuleService.deactivateValidationRule(rule.id);
      } else {
        await ValidationRuleService.activateValidationRule(rule.id);
      }
      await loadRules(selectedStageId);
      onRulesChange?.();
    } catch (err) {
      setError('Error toggling rule status');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getFieldName = (fieldId: string) => {
    return customFields.find(f => f.id === fieldId)?.field_name || fieldId;
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-medium text-gray-900">Validation Rules</h3>
      </div>

      {/* Stage Selector */}
      <div className="flex items-center gap-4">
        <label className="text-sm font-medium text-gray-700">Select Stage:</label>
        <select
          value={selectedStageId}
          onChange={(e) => setSelectedStageId(e.target.value)}
          className="flex-1 rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
          <option value="">-- Select a stage --</option>
          {stages && stages.map(stage => (
            <option key={stage.id} value={stage.id}>
              {stage.name}
            </option>
          ))}
        </select>
        {selectedStageId && (
          <button
            onClick={handleAddRule}
            disabled={loading || isAddingRule || !!editingRule}
            className="inline-flex items-center px-3 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400"
          >
            <Plus className="h-4 w-4 mr-1" />
            Add Rule
          </button>
        )}
      </div>

      {error && (
        <div className="rounded-md bg-red-50 p-4">
          <div className="flex">
            <AlertCircle className="h-5 w-5 text-red-400" />
            <div className="ml-3">
              <p className="text-sm text-red-800">{error}</p>
            </div>
          </div>
        </div>
      )}

      {/* Rules List */}
      {selectedStageId && !editingRule && (
        <div className="space-y-2">
          {loading && <p className="text-sm text-gray-500">Loading rules...</p>}
          {!loading && rules.length === 0 && (
            <p className="text-sm text-gray-500">No validation rules for this stage yet.</p>
          )}
          {!loading && rules && rules.map(rule => (
            <div
              key={rule.id}
              className={`border rounded-lg p-4 ${rule.is_active ? 'bg-white' : 'bg-gray-50'}`}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1 space-y-2">
                  <div className="flex items-center gap-2">
                    <span className="font-medium text-gray-900">
                      {getFieldName(rule.custom_field_id)}
                    </span>
                    <span className={`px-2 py-1 text-xs font-semibold rounded ${getValidationSeverityColor(rule.severity)}`}>
                      {getValidationSeverityLabel(rule.severity)}
                    </span>
                    {!rule.is_active && (
                      <span className="px-2 py-1 text-xs font-semibold rounded bg-gray-200 text-gray-700">
                        Inactive
                      </span>
                    )}
                    {rule.auto_reject && (
                      <span className="px-2 py-1 text-xs font-semibold rounded bg-red-100 text-red-800">
                        Auto-Reject
                      </span>
                    )}
                  </div>
                  <div className="text-sm text-gray-600">
                    <span className="font-medium">{getComparisonOperatorLabel(rule.comparison_operator)}</span>
                    {rule.position_field_path && (
                      <span> position.{rule.position_field_path}</span>
                    )}
                    {rule.comparison_value !== null && rule.comparison_value !== undefined && (
                      <span> {JSON.stringify(rule.comparison_value)}</span>
                    )}
                  </div>
                  <p className="text-sm text-gray-700">{rule.validation_message}</p>
                  {rule.auto_reject && rule.rejection_reason && (
                    <p className="text-xs text-red-600">Rejection: {rule.rejection_reason}</p>
                  )}
                </div>
                <div className="flex items-center gap-2 ml-4">
                  <button
                    onClick={() => handleToggleActive(rule)}
                    disabled={loading}
                    className="p-1 text-gray-400 hover:text-gray-600"
                    title={rule.is_active ? 'Deactivate' : 'Activate'}
                  >
                    {rule.is_active ? (
                      <CheckCircle className="h-5 w-5 text-green-500" />
                    ) : (
                      <CheckCircle className="h-5 w-5" />
                    )}
                  </button>
                  <button
                    onClick={() => handleEditRule(rule)}
                    disabled={loading}
                    className="p-1 text-gray-400 hover:text-blue-600"
                  >
                    <Edit2 className="h-4 w-4" />
                  </button>
                  <button
                    onClick={() => handleDeleteRule(rule.id)}
                    disabled={loading}
                    className="p-1 text-gray-400 hover:text-red-600"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Rule Editor Form */}
      {editingRule && (
        <div className="border rounded-lg p-4 bg-blue-50">
          <div className="space-y-4">
            <div className="flex items-center justify-between mb-4">
              <h4 className="text-md font-medium text-gray-900">
                {isAddingRule ? 'Add Validation Rule' : 'Edit Validation Rule'}
              </h4>
              <button
                onClick={() => {
                  setEditingRule(null);
                  setIsAddingRule(false);
                }}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

            {/* Field Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Custom Field *
              </label>
              <select
                value={editingRule.custom_field_id}
                onChange={(e) => setEditingRule({ ...editingRule, custom_field_id: e.target.value })}
                disabled={!isAddingRule}
                className="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              >
                {customFields && customFields.map(field => (
                  <option key={field.id} value={field.id}>
                    {field.field_name} ({field.field_type})
                  </option>
                ))}
              </select>
            </div>

            {/* Rule Type */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Rule Type *
              </label>
              <select
                value={editingRule.rule_type}
                onChange={(e) => setEditingRule({ ...editingRule, rule_type: e.target.value as ValidationRuleType })}
                disabled={!isAddingRule}
                className="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              >
                {RULE_TYPES.map(type => (
                  <option key={type} value={type}>
                    {getValidationRuleTypeLabel(type)}
                  </option>
                ))}
              </select>
            </div>

            {/* Comparison Operator */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Comparison Operator *
              </label>
              <select
                value={editingRule.comparison_operator}
                onChange={(e) => setEditingRule({ ...editingRule, comparison_operator: e.target.value as ComparisonOperator })}
                className="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              >
                {COMPARISON_OPERATORS.map(op => (
                  <option key={op} value={op}>
                    {getComparisonOperatorLabel(op)}
                  </option>
                ))}
              </select>
            </div>

            {/* Position Field Path */}
            {editingRule.rule_type === 'compare_position_field' && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Position Field Path *
                </label>
                <input
                  type="text"
                  value={editingRule.position_field_path}
                  onChange={(e) => setEditingRule({ ...editingRule, position_field_path: e.target.value })}
                  placeholder="e.g., salary.max, location.city"
                  className="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                />
                <p className="mt-1 text-xs text-gray-500">
                  Use dot notation to access nested fields (e.g., salary.max)
                </p>
              </div>
            )}

            {/* Comparison Value */}
            {editingRule.rule_type !== 'compare_position_field' && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Comparison Value
                </label>
                <input
                  type="text"
                  value={editingRule.comparison_value || ''}
                  onChange={(e) => setEditingRule({ ...editingRule, comparison_value: e.target.value })}
                  placeholder="Enter value or JSON"
                  className="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                />
              </div>
            )}

            {/* Severity */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Severity *
              </label>
              <select
                value={editingRule.severity}
                onChange={(e) => setEditingRule({ ...editingRule, severity: e.target.value as ValidationSeverity })}
                className="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              >
                {SEVERITIES.map(sev => (
                  <option key={sev} value={sev}>
                    {getValidationSeverityLabel(sev)}
                  </option>
                ))}
              </select>
            </div>

            {/* Validation Message */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Validation Message *
              </label>
              <textarea
                value={editingRule.validation_message}
                onChange={(e) => setEditingRule({ ...editingRule, validation_message: e.target.value })}
                rows={2}
                placeholder="Use variables: {{field_name}}, {{candidate_value}}, {{target_value}}"
                className="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              />
              <p className="mt-1 text-xs text-gray-500">
                Available variables: {'{{field_name}}, {{candidate_value}}, {{target_value}}'}
              </p>
            </div>

            {/* Auto Reject */}
            <div className="flex items-center">
              <input
                type="checkbox"
                checked={editingRule.auto_reject}
                onChange={(e) => setEditingRule({ ...editingRule, auto_reject: e.target.checked })}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label className="ml-2 text-sm text-gray-700">
                Auto-reject application if this rule fails
              </label>
            </div>

            {/* Rejection Reason */}
            {editingRule.auto_reject && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Rejection Reason
                </label>
                <input
                  type="text"
                  value={editingRule.rejection_reason}
                  onChange={(e) => setEditingRule({ ...editingRule, rejection_reason: e.target.value })}
                  placeholder="Reason for automatic rejection"
                  className="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                />
              </div>
            )}

            {/* Active Status */}
            <div className="flex items-center">
              <input
                type="checkbox"
                checked={editingRule.is_active}
                onChange={(e) => setEditingRule({ ...editingRule, is_active: e.target.checked })}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label className="ml-2 text-sm text-gray-700">
                Rule is active
              </label>
            </div>

            {/* Save/Cancel Buttons */}
            <div className="flex justify-end gap-2 pt-4">
              <button
                onClick={() => {
                  setEditingRule(null);
                  setIsAddingRule(false);
                }}
                disabled={loading}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                onClick={handleSaveRule}
                disabled={loading || !editingRule.validation_message}
                className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 disabled:bg-gray-400"
              >
                {loading ? 'Saving...' : 'Save Rule'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
