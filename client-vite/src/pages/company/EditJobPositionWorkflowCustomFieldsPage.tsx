import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { ArrowLeft, Save, Plus, X } from 'lucide-react';
import { PositionService } from '../../services/positionService';

interface StageFormData {
  id: string;
  name: string;
  icon: string;
  background_color: string;
  text_color: string;
  role?: string | null;
  status_mapping: string;
  kanban_display: string;
  field_visibility: Record<string, boolean>;
  field_validation: Record<string, any>;
  field_candidate_visibility: Record<string, boolean>;
}

export default function EditJobPositionWorkflowCustomFieldsPage() {
  const navigate = useNavigate();
  const { workflowId } = useParams<{ workflowId: string }>();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [workflowName, setWorkflowName] = useState('');
  const [stages, setStages] = useState<StageFormData[]>([]);
  const [customFieldsConfig, setCustomFieldsConfig] = useState<{
    fields?: Record<string, {
      type?: string;
      label?: string;
      required?: boolean;
      candidate_visible?: boolean;
      default_visibility?: boolean;
      validation?: any;
    }>;
    field_types?: Record<string, string>;
    field_labels?: Record<string, string>;
    field_required?: Record<string, boolean>;
    field_validation?: Record<string, any>;
    field_candidate_visibility_default?: Record<string, boolean>;
  }>({});

  useEffect(() => {
    if (workflowId) {
      loadWorkflow();
    }
  }, [workflowId]);

  const loadWorkflow = async () => {
    if (!workflowId) return;

    try {
      setLoading(true);
      const workflow = await PositionService.getWorkflow(workflowId);

      setWorkflowName(workflow.name);

      const formattedStages: StageFormData[] = workflow.stages.map((stage) => ({
        id: stage.id,
        name: stage.name,
        icon: stage.icon,
        background_color: stage.background_color,
        text_color: stage.text_color,
        role: stage.role || null,
        status_mapping: stage.status_mapping,
        kanban_display: stage.kanban_display,
        field_visibility: stage.field_visibility || {},
        field_validation: stage.field_validation || {},
        field_candidate_visibility: stage.field_candidate_visibility || {},
      }));

      setStages(formattedStages);
      setCustomFieldsConfig(workflow.custom_fields_config || {});
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to load workflow');
      console.error('Error loading workflow:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!workflowId) {
      setError('Workflow ID not found');
      return;
    }

    try {
      setSaving(true);
      
      // Get the current workflow to preserve other fields
      const currentWorkflow = await PositionService.getWorkflow(workflowId);
      
      // Update only custom_fields_config and stages (for field visibility/validation)
      await PositionService.updateWorkflow(workflowId, {
        name: currentWorkflow.name,
        default_view: currentWorkflow.default_view,
        stages: stages.map(stage => ({
          id: stage.id,
          name: stage.name,
          icon: stage.icon,
          background_color: stage.background_color,
          text_color: stage.text_color,
          role: stage.role,
          status_mapping: stage.status_mapping,
          kanban_display: stage.kanban_display,
          field_visibility: stage.field_visibility,
          field_validation: stage.field_validation,
          field_candidate_visibility: stage.field_candidate_visibility,
        })),
        custom_fields_config: customFieldsConfig,
      });

      navigate('/company/settings/job-position-workflows');
    } catch (err: any) {
      setError(err.message || 'Failed to update custom fields configuration');
      console.error('Error updating custom fields:', err);
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div>
      {/* Header */}
      <div className="mb-6">
        <button
          onClick={() => navigate('/company/settings/job-position-workflows')}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-4"
        >
          <ArrowLeft className="w-5 h-5" />
          Back to Workflows
        </button>
        <h1 className="text-2xl font-bold text-gray-900">Configure Custom Fields</h1>
        <p className="text-gray-600 mt-1">Configure custom fields for workflow: {workflowName}</p>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
          <p className="text-red-800">{error}</p>
        </div>
      )}

      {/* Form */}
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Custom Fields Configuration */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-lg font-semibold text-gray-900">Custom Fields</h2>
              <p className="text-sm text-gray-600 mt-1">
                Define custom fields that can be used in job positions created with this workflow
              </p>
            </div>
            <button
              type="button"
              onClick={() => {
                const fieldName = prompt('Enter field name (e.g., "location", "salary_range"):');
                if (fieldName && fieldName.trim()) {
                  const normalizedName = fieldName.trim().toLowerCase().replace(/\s+/g, '_');
                  const newConfig = { ...customFieldsConfig };
                  if (!newConfig.fields) newConfig.fields = {};
                  if (!newConfig.field_types) newConfig.field_types = {};
                  if (!newConfig.field_labels) newConfig.field_labels = {};
                  if (!newConfig.field_required) newConfig.field_required = {};
                  if (!newConfig.field_candidate_visibility_default) newConfig.field_candidate_visibility_default = {};
                  
                  newConfig.fields[normalizedName] = {
                    type: 'text',
                    label: fieldName,
                    required: false,
                    candidate_visible: false,
                    default_visibility: false,
                  };
                  newConfig.field_types[normalizedName] = 'text';
                  newConfig.field_labels[normalizedName] = fieldName;
                  newConfig.field_required[normalizedName] = false;
                  newConfig.field_candidate_visibility_default[normalizedName] = false;
                  
                  setCustomFieldsConfig(newConfig);
                }
              }}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              <Plus className="w-4 h-4" />
              Add Field
            </button>
          </div>

          {!customFieldsConfig.fields || Object.keys(customFieldsConfig.fields).length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              No custom fields defined. Click "Add Field" to create one.
            </div>
          ) : (
            <div className="space-y-4">
              {Object.entries(customFieldsConfig.fields || {}).map(([fieldName, fieldConfig]) => (
                <div key={fieldName} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex-1">
                      <h3 className="font-semibold text-gray-900 mb-2">{fieldName}</h3>
                      <div className="space-y-4">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                          <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Field Label</label>
                          <input
                            type="text"
                            value={fieldConfig.label || fieldName}
                            onChange={(e) => {
                              const newConfig = { ...customFieldsConfig };
                              if (newConfig.fields && newConfig.fields[fieldName]) {
                                newConfig.fields[fieldName].label = e.target.value;
                              }
                              if (newConfig.field_labels) {
                                newConfig.field_labels[fieldName] = e.target.value;
                              }
                              setCustomFieldsConfig(newConfig);
                            }}
                            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">Field Type</label>
                          <select
                            value={fieldConfig.type || 'text'}
                            onChange={(e) => {
                              const newConfig = { ...customFieldsConfig };
                              if (newConfig.fields && newConfig.fields[fieldName]) {
                                newConfig.fields[fieldName].type = e.target.value;
                              }
                              if (newConfig.field_types) {
                                newConfig.field_types[fieldName] = e.target.value;
                              }
                              setCustomFieldsConfig(newConfig);
                            }}
                            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                          >
                            <option value="text">Text</option>
                            <option value="number">Number</option>
                            <option value="date">Date</option>
                            <option value="select">Select</option>
                            <option value="object">Object</option>
                          </select>
                        </div>
                      </div>
                      <div className="flex items-center gap-6">
                          <label className="flex items-center gap-2">
                            <input
                              type="checkbox"
                              checked={fieldConfig.required || false}
                              onChange={(e) => {
                                const newConfig = { ...customFieldsConfig };
                                if (newConfig.fields && newConfig.fields[fieldName]) {
                                  newConfig.fields[fieldName].required = e.target.checked;
                                }
                                if (newConfig.field_required) {
                                  newConfig.field_required[fieldName] = e.target.checked;
                                }
                                setCustomFieldsConfig(newConfig);
                              }}
                              className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                            />
                            <span className="text-sm font-medium text-gray-700">Required</span>
                          </label>
                          <label className="flex items-center gap-2">
                            <input
                              type="checkbox"
                              checked={fieldConfig.candidate_visible || false}
                              onChange={(e) => {
                                const newConfig = { ...customFieldsConfig };
                                if (newConfig.fields && newConfig.fields[fieldName]) {
                                  newConfig.fields[fieldName].candidate_visible = e.target.checked;
                                  newConfig.fields[fieldName].default_visibility = e.target.checked;
                                }
                                if (newConfig.field_candidate_visibility_default) {
                                  newConfig.field_candidate_visibility_default[fieldName] = e.target.checked;
                                }
                                setCustomFieldsConfig(newConfig);
                              }}
                              className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                            />
                            <span className="text-sm font-medium text-gray-700 whitespace-nowrap">Visible to Candidates (when published)</span>
                          </label>
                        </div>
                      </div>
                    </div>
                    <button
                      type="button"
                      onClick={() => {
                        const newConfig = { ...customFieldsConfig };
                        if (newConfig.fields) delete newConfig.fields[fieldName];
                        if (newConfig.field_types) delete newConfig.field_types[fieldName];
                        if (newConfig.field_labels) delete newConfig.field_labels[fieldName];
                        if (newConfig.field_required) delete newConfig.field_required[fieldName];
                        if (newConfig.field_validation) delete newConfig.field_validation[fieldName];
                        if (newConfig.field_candidate_visibility_default) delete newConfig.field_candidate_visibility_default[fieldName];
                        
                        // Also remove from all stages
                        const newStages = stages.map(stage => {
                          const newVisibility = { ...stage.field_visibility };
                          const newCandidateVisibility = { ...stage.field_candidate_visibility };
                          const newValidation = { ...stage.field_validation };
                          delete newVisibility[fieldName];
                          delete newCandidateVisibility[fieldName];
                          delete newValidation[fieldName];
                          return {
                            ...stage,
                            field_visibility: newVisibility,
                            field_candidate_visibility: newCandidateVisibility,
                            field_validation: newValidation,
                          };
                        });
                        setStages(newStages);
                        
                        setCustomFieldsConfig(newConfig);
                      }}
                      className="p-1 text-red-600 hover:text-red-900 ml-4"
                      title="Remove field"
                    >
                      <X className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Field Visibility Matrix by Stage */}
        {customFieldsConfig.fields && Object.keys(customFieldsConfig.fields).length > 0 && stages.length > 0 && (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="mb-4">
              <h2 className="text-lg font-semibold text-gray-900">Field Visibility by Stage</h2>
              <p className="text-sm text-gray-600 mt-1">
                Configure which fields are visible in each workflow stage. Visibility controls whether the field appears in the admin form.
              </p>
            </div>
            <div className="overflow-x-auto border rounded">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider sticky left-0 bg-gray-50 z-10">
                      Field
                    </th>
                    {stages.map((stage) => (
                      <th
                        key={stage.id}
                        className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider min-w-[150px]"
                      >
                        <div className="flex items-center gap-2">
                          <span dangerouslySetInnerHTML={{ __html: stage.icon }} />
                          <div>{stage.name}</div>
                        </div>
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {Object.keys(customFieldsConfig.fields || {}).map((fieldName) => {
                    const fieldLabel = customFieldsConfig.field_labels?.[fieldName] || customFieldsConfig.fields![fieldName]?.label || fieldName;
                    return (
                      <tr key={fieldName} className="hover:bg-gray-50">
                        <td className="px-4 py-3 text-sm font-medium text-gray-900 sticky left-0 bg-white z-10">
                          <div>{fieldLabel}</div>
                          <div className="text-xs text-gray-500">{fieldName}</div>
                        </td>
                        {stages.map((stage) => {
                          const isVisible = stage.field_visibility[fieldName] ?? true;
                          return (
                            <td key={`${stage.id}-${fieldName}`} className="px-4 py-3 text-sm">
                              <label className="flex items-center gap-2">
                                <input
                                  type="checkbox"
                                  checked={isVisible}
                                  onChange={(e) => {
                                    const newStages = [...stages];
                                    const stageIndex = newStages.findIndex(s => s.id === stage.id);
                                    if (stageIndex >= 0) {
                                      newStages[stageIndex] = {
                                        ...newStages[stageIndex],
                                        field_visibility: {
                                          ...newStages[stageIndex].field_visibility,
                                          [fieldName]: e.target.checked,
                                        },
                                      };
                                      setStages(newStages);
                                    }
                                  }}
                                  className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                                />
                                <span className="text-xs text-gray-600">
                                  {isVisible ? 'Visible' : 'Hidden'}
                                </span>
                              </label>
                            </td>
                          );
                        })}
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        )}


        {/* Field Validation by Stage */}
        {customFieldsConfig.fields && Object.keys(customFieldsConfig.fields).length > 0 && stages.length > 0 && (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="mb-4">
              <h2 className="text-lg font-semibold text-gray-900">Field Validation Rules by Stage</h2>
              <p className="text-sm text-gray-600 mt-1">
                Configure validation requirements for each field in each workflow stage.
              </p>
            </div>
            <div className="overflow-x-auto border rounded">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider sticky left-0 bg-gray-50 z-10">
                      Field
                    </th>
                    {stages.map((stage) => (
                      <th
                        key={stage.id}
                        className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider min-w-[150px]"
                      >
                        <div className="flex items-center gap-2">
                          <span dangerouslySetInnerHTML={{ __html: stage.icon }} />
                          <div>{stage.name}</div>
                        </div>
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {Object.keys(customFieldsConfig.fields || {}).map((fieldName) => {
                    const fieldLabel = customFieldsConfig.field_labels?.[fieldName] || customFieldsConfig.fields![fieldName]?.label || fieldName;
                    return (
                      <tr key={fieldName} className="hover:bg-gray-50">
                        <td className="px-4 py-3 text-sm font-medium text-gray-900 sticky left-0 bg-white z-10">
                          <div>{fieldLabel}</div>
                          <div className="text-xs text-gray-500">{fieldName}</div>
                        </td>
                        {stages.map((stage) => {
                          const validation = stage.field_validation[fieldName];
                          const validationLevel = validation?.required === true ? 'required' : 
                                                 validation?.recommended === true ? 'recommended' : 
                                                 'optional';
                          return (
                            <td key={`${stage.id}-${fieldName}-validation`} className="px-4 py-3 text-sm">
                              <select
                                value={validationLevel}
                                onChange={(e) => {
                                  const newStages = [...stages];
                                  const stageIndex = newStages.findIndex(s => s.id === stage.id);
                                  if (stageIndex >= 0) {
                                    let newValidation: any = {};
                                    if (e.target.value === 'required') {
                                      newValidation = { required: true };
                                    } else if (e.target.value === 'recommended') {
                                      newValidation = { recommended: true };
                                    } else {
                                      newValidation = { optional: true };
                                    }
                                    
                                    newStages[stageIndex] = {
                                      ...newStages[stageIndex],
                                      field_validation: {
                                        ...newStages[stageIndex].field_validation,
                                        [fieldName]: newValidation,
                                      },
                                    };
                                    setStages(newStages);
                                  }
                                }}
                                className="w-full px-2 py-1 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-xs"
                              >
                                <option value="optional">Opcional</option>
                                <option value="recommended">Recomendado</option>
                                <option value="required">Requerido</option>
                              </select>
                            </td>
                          );
                        })}
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Actions */}
        <div className="flex items-center justify-end gap-3">
          <button
            type="button"
            onClick={() => navigate('/company/settings/job-position-workflows')}
            className="px-6 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={saving}
            className="flex items-center gap-2 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Save className="w-5 h-5" />
            {saving ? 'Saving...' : 'Save Changes'}
          </button>
        </div>
      </form>
    </div>
  );
}

