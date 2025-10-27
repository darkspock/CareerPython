import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Save, Plus, X, ArrowUp, ArrowDown } from 'lucide-react';
import { companyWorkflowService } from '../../services/companyWorkflowService';
import { phaseService } from '../../services/phaseService';
import { api } from '../../lib/api';
import type { CompanyRole } from '../../types/company';
import type { StageType } from '../../types/workflow';
import type { Phase } from '../../types/phase';

interface StageFormData {
  name: string;
  description: string;
  stage_type: StageType;
  order: number;
  allow_skip?: boolean;
  estimated_duration_days?: number;
  default_role_ids?: string[];
  deadline_days?: number;
  estimated_cost?: string;
  next_phase_id?: string;
}

export default function CreateWorkflowPage() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [roles, setRoles] = useState<CompanyRole[]>([]);
  const [loadingRoles, setLoadingRoles] = useState(true);
  const [phases, setPhases] = useState<Phase[]>([]);
  const [loadingPhases, setLoadingPhases] = useState(true);

  const [workflowName, setWorkflowName] = useState('');
  const [workflowDescription, setWorkflowDescription] = useState('');
  const [phaseId, setPhaseId] = useState<string>('');
  const [isDefault, setIsDefault] = useState(false);
  const [stages, setStages] = useState<StageFormData[]>([
    { name: 'Applied', description: 'Candidate has applied', stage_type: 'initial', order: 1 },
    { name: 'Screening', description: 'Initial screening', stage_type: 'standard', order: 2 },
    { name: 'Interview', description: 'Interview stage', stage_type: 'standard', order: 3 },
    { name: 'Hired', description: 'Candidate hired', stage_type: 'success', order: 4 },
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

  // Load company roles and phases on mount
  useEffect(() => {
    const loadData = async () => {
      const companyId = getCompanyId();
      if (!companyId) return;

      try {
        setLoadingRoles(true);
        setLoadingPhases(true);

        const [rolesResponse, phasesData] = await Promise.all([
          api.listCompanyRoles(companyId, true), // Only active roles
          phaseService.listPhases(companyId)
        ]);

        setRoles(rolesResponse as CompanyRole[]);
        setPhases(phasesData.sort((a, b) => a.sort_order - b.sort_order));
      } catch (err) {
        console.error('Failed to load data:', err);
      } finally {
        setLoadingRoles(false);
        setLoadingPhases(false);
      }
    };

    loadData();
  }, []);

  const handleAddStage = () => {
    const newOrder = stages.length + 1;
    setStages([
      ...stages,
      { name: '', description: '', stage_type: 'standard', order: newOrder },
    ]);
  };

  const handleRemoveStage = (index: number) => {
    const newStages = stages.filter((_, i) => i !== index);
    // Reorder remaining stages
    newStages.forEach((stage, i) => {
      stage.order = i + 1;
    });
    setStages(newStages);
  };

  const handleStageChange = (index: number, field: keyof StageFormData, value: any) => {
    const newStages = [...stages];
    newStages[index] = { ...newStages[index], [field]: value };
    setStages(newStages);
  };

  const handleMoveStageUp = (index: number) => {
    if (index === 0) return; // Already at the top

    const newStages = [...stages];
    // Swap with previous stage
    [newStages[index - 1], newStages[index]] = [newStages[index], newStages[index - 1]];

    // Update order values
    newStages.forEach((stage, i) => {
      stage.order = i + 1;
    });

    setStages(newStages);
  };

  const handleMoveStageDown = (index: number) => {
    if (index === stages.length - 1) return; // Already at the bottom

    const newStages = [...stages];
    // Swap with next stage
    [newStages[index], newStages[index + 1]] = [newStages[index + 1], newStages[index]];

    // Update order values
    newStages.forEach((stage, i) => {
      stage.order = i + 1;
    });

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

    if (!workflowName) {
      setError('Workflow name is required');
      return;
    }

    if (stages.length === 0) {
      setError('At least one stage is required');
      return;
    }

    // Validate stages
    for (const stage of stages) {
      if (!stage.name) {
        setError('All stages must have a name');
        return;
      }
    }

    try {
      setLoading(true);

      // Create workflow
      const workflow = await companyWorkflowService.createWorkflow({
        company_id: companyId,
        name: workflowName,
        description: workflowDescription,
        phase_id: phaseId || undefined,
        is_default: isDefault,
      });

      // Create stages
      for (const stageData of stages) {
        await companyWorkflowService.createStage({
          workflow_id: workflow.id,
          name: stageData.name,
          description: stageData.description,
          stage_type: stageData.stage_type,
          order: stageData.order,
          is_active: true,
          allow_skip: stageData.allow_skip,
          estimated_duration_days: stageData.estimated_duration_days,
          default_role_ids: stageData.default_role_ids,
          deadline_days: stageData.deadline_days,
          estimated_cost: stageData.estimated_cost,
          next_phase_id: stageData.next_phase_id,
        });
      }

      navigate('/company/settings/workflows');
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
          onClick={() => navigate('/company/settings')}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-4"
        >
          <ArrowLeft className="w-5 h-5" />
          Back to Workflows
        </button>
        <h1 className="text-2xl font-bold text-gray-900">Create Workflow</h1>
        <p className="text-gray-600 mt-1">Define a recruitment workflow with stages</p>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
          <p className="text-red-800">{error}</p>
        </div>
      )}

      {/* Form */}
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Workflow Details */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Workflow Details</h2>
          <div className="space-y-4">
            {/* Name */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Workflow Name <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                required
                value={workflowName}
                onChange={(e) => setWorkflowName(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="e.g., Standard Recruitment Process"
              />
            </div>

            {/* Description */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Description</label>
              <textarea
                value={workflowDescription}
                onChange={(e) => setWorkflowDescription(e.target.value)}
                rows={3}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="Describe this workflow..."
              />
            </div>

            {/* Phase Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Phase (Optional)
              </label>
              {loadingPhases ? (
                <div className="text-sm text-gray-500">Loading phases...</div>
              ) : phases.length === 0 ? (
                <div className="text-sm text-gray-500">
                  No phases available. <a href="/company/settings/phases" className="text-blue-600 hover:underline">Create phases first</a>
                </div>
              ) : (
                <select
                  value={phaseId}
                  onChange={(e) => setPhaseId(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="">No Phase (Standalone Workflow)</option>
                  {phases.map((phase) => (
                    <option key={phase.id} value={phase.id}>
                      {phase.name}
                    </option>
                  ))}
                </select>
              )}
              <p className="mt-1 text-xs text-gray-500">
                Assign this workflow to a recruitment phase (optional)
              </p>
            </div>

            {/* Is Default */}
            <div className="flex items-center gap-3">
              <input
                type="checkbox"
                id="is_default"
                checked={isDefault}
                onChange={(e) => setIsDefault(e.target.checked)}
                className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
              />
              <label htmlFor="is_default" className="text-sm font-medium text-gray-700">
                Set as default workflow
              </label>
            </div>
          </div>
        </div>

        {/* Stages */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">Workflow Stages</h2>
            <button
              type="button"
              onClick={handleAddStage}
              className="flex items-center gap-2 px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm"
            >
              <Plus className="w-4 h-4" />
              Add Stage
            </button>
          </div>

          <div className="space-y-4">
            {stages.map((stage, index) => (
              <div key={index} className="bg-gray-50 rounded-lg p-4 border border-gray-200">
                <div className="flex items-start justify-between mb-3">
                  <span className="text-sm font-medium text-gray-500">Stage {index + 1}</span>
                  <div className="flex items-center gap-2">
                    {/* Move Up/Down buttons */}
                    <button
                      type="button"
                      onClick={() => handleMoveStageUp(index)}
                      disabled={index === 0}
                      className="p-1 text-gray-600 hover:text-gray-900 disabled:text-gray-300 disabled:cursor-not-allowed"
                      title="Move up"
                    >
                      <ArrowUp className="w-4 h-4" />
                    </button>
                    <button
                      type="button"
                      onClick={() => handleMoveStageDown(index)}
                      disabled={index === stages.length - 1}
                      className="p-1 text-gray-600 hover:text-gray-900 disabled:text-gray-300 disabled:cursor-not-allowed"
                      title="Move down"
                    >
                      <ArrowDown className="w-4 h-4" />
                    </button>
                    {/* Delete button */}
                    {stages.length > 1 && (
                      <button
                        type="button"
                        onClick={() => handleRemoveStage(index)}
                        className="p-1 text-red-600 hover:text-red-800"
                        title="Remove stage"
                      >
                        <X className="w-4 h-4" />
                      </button>
                    )}
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {/* Stage Name */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Stage Name <span className="text-red-500">*</span>
                    </label>
                    <input
                      type="text"
                      required
                      value={stage.name}
                      onChange={(e) => handleStageChange(index, 'name', e.target.value)}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      placeholder="e.g., Phone Screen"
                    />
                  </div>

                  {/* Stage Type */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Stage Type</label>
                    <select
                      value={stage.stage_type}
                      onChange={(e) => handleStageChange(index, 'stage_type', e.target.value)}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    >
                      <option value="initial">Initial</option>
                      <option value="standard">Standard</option>
                      <option value="success">Success</option>
                      <option value="fail">Fail</option>
                    </select>
                  </div>

                  {/* Next Phase (only for success/fail stages) */}
                  {(stage.stage_type === 'success' || stage.stage_type === 'fail') && (
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Next Phase (Optional)
                      </label>
                      {loadingPhases ? (
                        <div className="text-sm text-gray-500">Loading phases...</div>
                      ) : phases.length === 0 ? (
                        <div className="text-sm text-gray-500">No phases available</div>
                      ) : (
                        <select
                          value={stage.next_phase_id || ''}
                          onChange={(e) => handleStageChange(index, 'next_phase_id', e.target.value || undefined)}
                          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        >
                          <option value="">No automatic transition</option>
                          {phases.map((phase) => (
                            <option key={phase.id} value={phase.id}>
                              {phase.name}
                            </option>
                          ))}
                        </select>
                      )}
                      <p className="mt-1 text-xs text-gray-500">
                        Automatically move candidate to this phase when reaching this stage
                      </p>
                    </div>
                  )}

                  {/* Description */}
                  <div className="md:col-span-2">
                    <label className="block text-sm font-medium text-gray-700 mb-2">Description</label>
                    <input
                      type="text"
                      value={stage.description}
                      onChange={(e) => handleStageChange(index, 'description', e.target.value)}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      placeholder="Describe this stage..."
                    />
                  </div>

                  {/* Allow Skip */}
                  <div className="flex items-center gap-3">
                    <input
                      type="checkbox"
                      id={`allow_skip_${index}`}
                      checked={stage.allow_skip || false}
                      onChange={(e) => handleStageChange(index, 'allow_skip', e.target.checked)}
                      className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                    />
                    <label htmlFor={`allow_skip_${index}`} className="text-sm font-medium text-gray-700">
                      Allow skipping this stage (optional)
                    </label>
                  </div>

                  {/* Estimated Duration Days */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Estimated Duration (days)</label>
                    <input
                      type="number"
                      min="0"
                      value={stage.estimated_duration_days || ''}
                      onChange={(e) => handleStageChange(index, 'estimated_duration_days', e.target.value ? parseInt(e.target.value) : undefined)}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      placeholder="e.g., 3"
                    />
                  </div>

                  {/* Deadline Days */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Deadline (days)</label>
                    <input
                      type="number"
                      min="1"
                      value={stage.deadline_days || ''}
                      onChange={(e) => handleStageChange(index, 'deadline_days', e.target.value ? parseInt(e.target.value) : undefined)}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      placeholder="e.g., 5"
                    />
                  </div>

                  {/* Estimated Cost */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Estimated Cost</label>
                    <input
                      type="number"
                      min="0"
                      step="0.01"
                      value={stage.estimated_cost || ''}
                      onChange={(e) => handleStageChange(index, 'estimated_cost', e.target.value || undefined)}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      placeholder="e.g., 100.00"
                    />
                  </div>

                  {/* Default Roles */}
                  <div className="md:col-span-2">
                    <label className="block text-sm font-medium text-gray-700 mb-2">Default Roles</label>
                    {loadingRoles ? (
                      <div className="text-sm text-gray-500">Loading roles...</div>
                    ) : roles.length === 0 ? (
                      <div className="text-sm text-gray-500">
                        No roles available. <a href="/company/settings/roles" className="text-blue-600 hover:underline">Create roles first</a>
                      </div>
                    ) : (
                      <div className="space-y-2 p-4 border border-gray-300 rounded-lg bg-gray-50">
                        {roles.map((role) => (
                          <label key={role.id} className="flex items-center gap-2 cursor-pointer hover:bg-gray-100 p-2 rounded">
                            <input
                              type="checkbox"
                              checked={(stage.default_role_ids || []).includes(role.id)}
                              onChange={(e) => {
                                const currentRoles = stage.default_role_ids || [];
                                const newRoles = e.target.checked
                                  ? [...currentRoles, role.id]
                                  : currentRoles.filter(id => id !== role.id);
                                handleStageChange(index, 'default_role_ids', newRoles.length > 0 ? newRoles : undefined);
                              }}
                              className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
                            />
                            <span className="text-sm text-gray-700">{role.name}</span>
                          </label>
                        ))}
                      </div>
                    )}
                    <p className="mt-1 text-xs text-gray-500">Select one or more roles to assign to this stage</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Actions */}
        <div className="flex items-center justify-end gap-3">
          <button
            type="button"
            onClick={() => navigate('/company/settings')}
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
