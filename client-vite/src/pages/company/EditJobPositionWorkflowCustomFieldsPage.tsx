import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { ArrowLeft, Save, Plus, X } from 'lucide-react';
import { PositionService } from '../../services/positionService';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Checkbox } from '@/components/ui/checkbox';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';

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

      navigate('/company/settings/publication-workflows');
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
        <Button
          variant="ghost"
          onClick={() => navigate('/company/settings/publication-workflows')}
          className="mb-4"
        >
          <ArrowLeft className="w-5 h-5 mr-2" />
          Back to Workflows
        </Button>
        <h1 className="text-2xl font-bold text-gray-900">Configure Custom Fields</h1>
        <p className="text-gray-600 mt-1">Configure custom fields for workflow: {workflowName}</p>
      </div>

      {/* Error Message */}
      {error && (
        <Alert variant="destructive" className="mb-6">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Form */}
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Custom Fields Configuration */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>Custom Fields</CardTitle>
                <p className="text-sm text-gray-600 mt-1">
                  Define custom fields that can be used in job positions created with this workflow
                </p>
              </div>
              <Button
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
                size="sm"
              >
                <Plus className="w-4 h-4 mr-2" />
                Add Field
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            {!customFieldsConfig.fields || Object.keys(customFieldsConfig.fields).length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                No custom fields defined. Click "Add Field" to create one.
              </div>
            ) : (
              <div className="space-y-4">
                {Object.entries(customFieldsConfig.fields || {}).map(([fieldName, fieldConfig]) => (
                  <Card key={fieldName}>
                    <CardContent className="pt-6">
                      <div className="flex items-start justify-between mb-4">
                        <div className="flex-1">
                          <h3 className="font-semibold text-gray-900 mb-2">{fieldName}</h3>
                          <div className="space-y-4">
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                              <div>
                                <Label>Field Label</Label>
                                <Input
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
                                />
                              </div>
                              <div>
                                <Label>Field Type</Label>
                                <Select
                                  value={fieldConfig.type || 'text'}
                                  onValueChange={(value) => {
                                    const newConfig = { ...customFieldsConfig };
                                    if (newConfig.fields && newConfig.fields[fieldName]) {
                                      newConfig.fields[fieldName].type = value;
                                    }
                                    if (newConfig.field_types) {
                                      newConfig.field_types[fieldName] = value;
                                    }
                                    setCustomFieldsConfig(newConfig);
                                  }}
                                >
                                  <SelectTrigger>
                                    <SelectValue />
                                  </SelectTrigger>
                                  <SelectContent>
                                    <SelectItem value="text">Text</SelectItem>
                                    <SelectItem value="number">Number</SelectItem>
                                    <SelectItem value="date">Date</SelectItem>
                                    <SelectItem value="select">Select</SelectItem>
                                    <SelectItem value="object">Object</SelectItem>
                                  </SelectContent>
                                </Select>
                              </div>
                            </div>
                            <div className="flex items-center gap-6">
                              <div className="flex items-center gap-2">
                                <Checkbox
                                  id={`required-${fieldName}`}
                                  checked={fieldConfig.required || false}
                                  onCheckedChange={(checked) => {
                                    const newConfig = { ...customFieldsConfig };
                                    if (newConfig.fields && newConfig.fields[fieldName]) {
                                      newConfig.fields[fieldName].required = checked as boolean;
                                    }
                                    if (newConfig.field_required) {
                                      newConfig.field_required[fieldName] = checked as boolean;
                                    }
                                    setCustomFieldsConfig(newConfig);
                                  }}
                                />
                                <Label htmlFor={`required-${fieldName}`} className="cursor-pointer">
                                  Required
                                </Label>
                              </div>
                              <div className="flex items-center gap-2">
                                <Checkbox
                                  id={`visible-${fieldName}`}
                                  checked={fieldConfig.candidate_visible || false}
                                  onCheckedChange={(checked) => {
                                    const newConfig = { ...customFieldsConfig };
                                    if (newConfig.fields && newConfig.fields[fieldName]) {
                                      newConfig.fields[fieldName].candidate_visible = checked as boolean;
                                      newConfig.fields[fieldName].default_visibility = checked as boolean;
                                    }
                                    if (newConfig.field_candidate_visibility_default) {
                                      newConfig.field_candidate_visibility_default[fieldName] = checked as boolean;
                                    }
                                    setCustomFieldsConfig(newConfig);
                                  }}
                                />
                                <Label htmlFor={`visible-${fieldName}`} className="cursor-pointer whitespace-nowrap">
                                  Visible to Candidates (when published)
                                </Label>
                              </div>
                            </div>
                          </div>
                        </div>
                        <Button
                          type="button"
                          variant="ghost"
                          size="sm"
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
                          title="Remove field"
                        >
                          <X className="w-4 h-4 text-red-600" />
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Field Visibility Matrix by Stage */}
        {customFieldsConfig.fields && Object.keys(customFieldsConfig.fields).length > 0 && stages.length > 0 && (
          <Card>
            <CardHeader>
              <CardTitle>Field Visibility by Stage</CardTitle>
              <p className="text-sm text-gray-600 mt-1">
                Configure which fields are visible in each workflow stage. Visibility controls whether the field appears in the admin form.
              </p>
            </CardHeader>
            <CardContent>
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
                                <div className="flex items-center gap-2">
                                  <Checkbox
                                    id={`visibility-${stage.id}-${fieldName}`}
                                    checked={isVisible}
                                    onCheckedChange={(checked) => {
                                      const newStages = [...stages];
                                      const stageIndex = newStages.findIndex(s => s.id === stage.id);
                                      if (stageIndex >= 0) {
                                        newStages[stageIndex] = {
                                          ...newStages[stageIndex],
                                          field_visibility: {
                                            ...newStages[stageIndex].field_visibility,
                                            [fieldName]: checked as boolean,
                                          },
                                        };
                                        setStages(newStages);
                                      }
                                    }}
                                  />
                                  <Label htmlFor={`visibility-${stage.id}-${fieldName}`} className="text-xs text-gray-600 cursor-pointer">
                                    {isVisible ? 'Visible' : 'Hidden'}
                                  </Label>
                                </div>
                              </td>
                            );
                          })}
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </CardContent>
          </Card>
        )}


        {/* Field Validation by Stage */}
        {customFieldsConfig.fields && Object.keys(customFieldsConfig.fields).length > 0 && stages.length > 0 && (
          <Card>
            <CardHeader>
              <CardTitle>Field Validation Rules by Stage</CardTitle>
              <p className="text-sm text-gray-600 mt-1">
                Configure validation requirements for each field in each workflow stage.
              </p>
            </CardHeader>
            <CardContent>
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
                                <Select
                                  value={validationLevel}
                                  onValueChange={(value) => {
                                    const newStages = [...stages];
                                    const stageIndex = newStages.findIndex(s => s.id === stage.id);
                                    if (stageIndex >= 0) {
                                      let newValidation: any = {};
                                      if (value === 'required') {
                                        newValidation = { required: true };
                                      } else if (value === 'recommended') {
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
                                >
                                  <SelectTrigger className="w-full">
                                    <SelectValue />
                                  </SelectTrigger>
                                  <SelectContent>
                                    <SelectItem value="optional">Opcional</SelectItem>
                                    <SelectItem value="recommended">Recomendado</SelectItem>
                                    <SelectItem value="required">Requerido</SelectItem>
                                  </SelectContent>
                                </Select>
                              </td>
                            );
                          })}
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Actions */}
        <div className="flex items-center justify-end gap-3">
          <Button
            type="button"
            variant="outline"
            onClick={() => navigate('/company/settings/publication-workflows')}
          >
            Cancel
          </Button>
          <Button type="submit" disabled={saving}>
            <Save className="w-5 h-5 mr-2" />
            {saving ? 'Saving...' : 'Save Changes'}
          </Button>
        </div>
      </form>
    </div>
  );
}
