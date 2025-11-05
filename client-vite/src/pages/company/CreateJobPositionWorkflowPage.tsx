import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Save, Plus, X, ArrowUp, ArrowDown } from 'lucide-react';
import { PositionService } from '../../services/positionService';
import { api } from '../../lib/api';
import type { CompanyRole } from '../../types/company';

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

export default function CreateJobPositionWorkflowPage() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [workflowName, setWorkflowName] = useState('');
  const [defaultView, setDefaultView] = useState('kanban');
  const [companyRoles, setCompanyRoles] = useState<CompanyRole[]>([]);
  const [stages, setStages] = useState<StageFormData[]>([
    {
      id: `stage-${Date.now()}`,
      name: 'Draft',
      icon: '📝',
      background_color: '#E5E7EB',
      text_color: '#374151',
      status_mapping: 'draft',
      kanban_display: 'vertical',
      field_visibility: {},
      field_validation: {},
      field_candidate_visibility: {},
    },
    {
      id: `stage-${Date.now() + 1}`,
      name: 'Active',
      icon: '✅',
      background_color: '#10B981',
      text_color: '#FFFFFF',
      status_mapping: 'active',
      kanban_display: 'vertical',
      field_visibility: {},
      field_validation: {},
      field_candidate_visibility: {},
    },
  ]);

  const getCompanyId = () => {
    const token = localStorage.getItem('access_token');
    if (!token) return null;
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return payload.company_id;
    } catch {
      return null;
    }
  };

  useEffect(() => {
    loadCompanyRoles();
  }, []);

  const loadCompanyRoles = async () => {
    const companyId = getCompanyId();
    if (!companyId) return;

    try {
      const response = await api.listCompanyRoles(companyId, false);
      setCompanyRoles(response as CompanyRole[]);
    } catch (err: any) {
      console.error('Error loading company roles:', err);
    }
  };

  const generateStageId = () => {
    return `stage-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  };

  const handleAddStage = () => {
    setStages([
      ...stages,
      {
        id: generateStageId(),
        name: '',
        icon: '📋',
        background_color: '#E5E7EB',
        text_color: '#374151',
        status_mapping: 'draft',
        kanban_display: 'vertical',
        field_visibility: {},
        field_validation: {},
        field_candidate_visibility: {},
      },
    ]);
  };

  const handleRemoveStage = (index: number) => {
    setStages(stages.filter((_, i) => i !== index));
  };

  const handleStageChange = (index: number, field: keyof StageFormData, value: any) => {
    const newStages = [...stages];
    newStages[index] = { ...newStages[index], [field]: value };
    setStages(newStages);
  };

  const handleMoveStageUp = (index: number) => {
    if (index === 0) return;
    const newStages = [...stages];
    [newStages[index - 1], newStages[index]] = [newStages[index], newStages[index - 1]];
    setStages(newStages);
  };

  const handleMoveStageDown = (index: number) => {
    if (index === stages.length - 1) return;
    const newStages = [...stages];
    [newStages[index], newStages[index + 1]] = [newStages[index + 1], newStages[index]];
    setStages(newStages);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    const companyId = getCompanyId();
    if (!companyId) {
      setError('Company ID not found');
      return;
    }

    if (!workflowName.trim()) {
      setError('Workflow name is required');
      return;
    }

    if (stages.length === 0) {
      setError('At least one stage is required');
      return;
    }

    // Validate stages
    for (const stage of stages) {
      if (!stage.name.trim()) {
        setError(`Stage ${stages.indexOf(stage) + 1} name is required`);
        return;
      }
    }

    try {
      setLoading(true);
      await PositionService.createWorkflow({
        company_id: companyId,
        name: workflowName,
        default_view: defaultView,
        stages: stages.map((stage) => ({
          id: stage.id,
          name: stage.name,
          icon: stage.icon,
          background_color: stage.background_color,
          text_color: stage.text_color,
          role: stage.role || null,
          status_mapping: stage.status_mapping,
          kanban_display: stage.kanban_display,
          field_visibility: stage.field_visibility,
          field_validation: stage.field_validation,
          field_candidate_visibility: stage.field_candidate_visibility,
        })),
        custom_fields_config: {},
      });

      navigate('/company/settings/job-position-workflows');
    } catch (err: any) {
      setError(err.message || 'Failed to create workflow');
      console.error('Error creating workflow:', err);
    } finally {
      setLoading(false);
    }
  };

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
        <h1 className="text-2xl font-bold text-gray-900">Create Job Position Workflow</h1>
        <p className="text-gray-600 mt-1">Create a new workflow for managing job positions</p>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
          <p className="text-red-800">{error}</p>
        </div>
      )}

      {/* Form */}
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Basic Information */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Basic Information</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Workflow Name <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                required
                value={workflowName}
                onChange={(e) => setWorkflowName(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="e.g., Standard Hiring Process"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Default View</label>
              <select
                value={defaultView}
                onChange={(e) => setDefaultView(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="kanban">Kanban</option>
                <option value="list">List</option>
              </select>
            </div>
          </div>
        </div>

        {/* Stages */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">Stages</h2>
            <button
              type="button"
              onClick={handleAddStage}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              <Plus className="w-4 h-4" />
              Add Stage
            </button>
          </div>

          {stages.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              No stages yet. Click "Add Stage" to create one.
            </div>
          ) : (
            <div className="space-y-4">
              {stages.map((stage, index) => (
                <div key={stage.id} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center gap-2">
                      <span className="text-lg">{stage.icon}</span>
                      <h3 className="font-semibold text-gray-900">Stage {index + 1}</h3>
                    </div>
                    <div className="flex items-center gap-2">
                      <button
                        type="button"
                        onClick={() => handleMoveStageUp(index)}
                        disabled={index === 0}
                        className="p-1 text-gray-600 hover:text-gray-900 disabled:opacity-50 disabled:cursor-not-allowed"
                        title="Move up"
                      >
                        <ArrowUp className="w-4 h-4" />
                      </button>
                      <button
                        type="button"
                        onClick={() => handleMoveStageDown(index)}
                        disabled={index === stages.length - 1}
                        className="p-1 text-gray-600 hover:text-gray-900 disabled:opacity-50 disabled:cursor-not-allowed"
                        title="Move down"
                      >
                        <ArrowDown className="w-4 h-4" />
                      </button>
                      <button
                        type="button"
                        onClick={() => handleRemoveStage(index)}
                        className="p-1 text-red-600 hover:text-red-900"
                        title="Remove stage"
                      >
                        <X className="w-4 h-4" />
                      </button>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Stage Name *</label>
                      <input
                        type="text"
                        required
                        value={stage.name}
                        onChange={(e) => handleStageChange(index, 'name', e.target.value)}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Icon (Emoji)</label>
                      <input
                        type="text"
                        value={stage.icon}
                        onChange={(e) => handleStageChange(index, 'icon', e.target.value)}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        placeholder="📝"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Background Color</label>
                      <input
                        type="color"
                        value={stage.background_color}
                        onChange={(e) => handleStageChange(index, 'background_color', e.target.value)}
                        className="w-full h-10 border border-gray-300 rounded-lg"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Text Color</label>
                      <input
                        type="color"
                        value={stage.text_color}
                        onChange={(e) => handleStageChange(index, 'text_color', e.target.value)}
                        className="w-full h-10 border border-gray-300 rounded-lg"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Status Mapping *</label>
                      <select
                        value={stage.status_mapping}
                        onChange={(e) => handleStageChange(index, 'status_mapping', e.target.value)}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        required
                      >
                        <option value="draft">Draft</option>
                        <option value="active">Active</option>
                        <option value="paused">Paused</option>
                        <option value="closed">Closed</option>
                      </select>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Kanban Display</label>
                      <select
                        value={stage.kanban_display}
                        onChange={(e) => handleStageChange(index, 'kanban_display', e.target.value)}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      >
                        <option value="vertical">Vertical (Column)</option>
                        <option value="horizontal_bottom">Horizontal (Row)</option>
                        <option value="hidden">Hidden</option>
                      </select>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Responsible Role</label>
                      <select
                        value={stage.role || ''}
                        onChange={(e) => handleStageChange(index, 'role', e.target.value || null)}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      >
                        <option value="">Not assigned</option>
                        {companyRoles.map((role) => (
                          <option key={role.id} value={role.id}>
                            {role.name}
                          </option>
                        ))}
                      </select>
                    </div>
                  </div>

                  {/* Preview */}
                  <div className="mt-4 p-3 rounded" style={{ backgroundColor: stage.background_color, color: stage.text_color }}>
                    <div className="flex items-center gap-2">
                      <span className="text-lg" dangerouslySetInnerHTML={{ __html: stage.icon }} />
                      <span className="font-semibold">{stage.name}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

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
            disabled={loading}
            className="flex items-center gap-2 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Save className="w-5 h-5" />
            {loading ? 'Creating...' : 'Create Workflow'}
          </button>
        </div>
      </form>
    </div>
  );
}

