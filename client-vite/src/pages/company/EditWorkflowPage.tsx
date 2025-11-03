import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { ArrowLeft, Save, Plus, X, Trash2, ArrowUp, ArrowDown, Settings } from 'lucide-react';
import { companyWorkflowService } from '../../services/companyWorkflowService';
import { phaseService } from '../../services/phaseService';
import { api } from '../../lib/api';
import type { CompanyWorkflow, WorkflowStage, CustomField, FieldConfiguration, StageType } from '../../types/workflow';
import type { CompanyRole } from '../../types/company';
import type { Phase } from '../../types/phase';
import type { UpdateStageStyleRequest } from '../../types/stageStyle';
import { CustomFieldEditor, FieldVisibilityMatrix, ValidationRuleEditor, PhaseTransitionIndicator } from '../../components/workflow';
import { StageStyleEditor } from '../../components/workflow/StageStyleEditor';

interface StageFormData {
  id?: string;
  name: string;
  description: string;
  stage_type: StageType;
  order: number;
  is_active: boolean;
  isNew?: boolean;
  allow_skip?: boolean;
  estimated_duration_days?: number;
  default_role_ids?: string[];
  deadline_days?: number;
  estimated_cost?: string;
  next_phase_id?: string;
  kanban_display?: string;
  style?: {
    icon: string;
    color: string;
    background_color: string;
  };
}

export default function EditWorkflowPage() {
  const navigate = useNavigate();
  const { workflowId } = useParams<{ workflowId: string }>();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [roles, setRoles] = useState<CompanyRole[]>([]);
  const [loadingRoles, setLoadingRoles] = useState(true);
  const [phases, setPhases] = useState<Phase[]>([]);
  const [loadingPhases, setLoadingPhases] = useState(true);

  const [workflow, setWorkflow] = useState<CompanyWorkflow | null>(null);
  const [workflowName, setWorkflowName] = useState('');
  const [workflowDescription, setWorkflowDescription] = useState('');
  const [phaseId, setPhaseId] = useState<string>('');
  const [stages, setStages] = useState<StageFormData[]>([]);
  const [deletedStageIds, setDeletedStageIds] = useState<string[]>([]);
  const [advancedModalOpen, setAdvancedModalOpen] = useState(false);
  const [selectedStageIndex, setSelectedStageIndex] = useState<number | null>(null);
  const [styleEditorOpen, setStyleEditorOpen] = useState(false);
  const [editingStageIndex, setEditingStageIndex] = useState<number | null>(null);

  // Custom fields state
  const [customFields, setCustomFields] = useState<CustomField[]>([]);
  const [fieldConfigurations, setFieldConfigurations] = useState<FieldConfiguration[]>([]);

  useEffect(() => {
    loadWorkflow();
    loadRoles();
    loadPhases();
  }, [workflowId]);

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

  const loadRoles = async () => {
    const companyId = getCompanyId();
    if (!companyId) return;

    try {
      setLoadingRoles(true);
      const response = await api.listCompanyRoles(companyId, true); // Only active roles
      setRoles(response as CompanyRole[]);
    } catch (err) {
      console.error('Failed to load roles:', err);
    } finally {
      setLoadingRoles(false);
    }
  };

  const loadPhases = async () => {
    const companyId = getCompanyId();
    if (!companyId) return;

    try {
      setLoadingPhases(true);
      const phasesData = await phaseService.listPhases(companyId);
      setPhases(phasesData.sort((a, b) => a.sort_order - b.sort_order));
    } catch (err) {
      console.error('Failed to load phases:', err);
    } finally {
      setLoadingPhases(false);
    }
  };

  const loadWorkflow = async () => {
    if (!workflowId) {
      setError('Workflow ID not found');
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      const workflowData = await companyWorkflowService.getWorkflow(workflowId);
      setWorkflow(workflowData);
      setWorkflowName(workflowData.name);
      setWorkflowDescription(workflowData.description || '');
      setPhaseId(workflowData.phase_id || '');

      // Load stages
      const stagesData = await companyWorkflowService.listStagesByWorkflow(workflowId);
      const formattedStages: StageFormData[] = stagesData.map((stage) => ({
        id: stage.id,
        name: stage.name,
        description: stage.description || '',
        stage_type: stage.stage_type,
        order: stage.order,
        is_active: stage.is_active,
        isNew: false,
        allow_skip: stage.allow_skip,
        estimated_duration_days: stage.estimated_duration_days || undefined,
        default_role_ids: stage.default_role_ids || undefined,
        deadline_days: stage.deadline_days || undefined,
        estimated_cost: stage.estimated_cost || undefined,
        next_phase_id: stage.next_phase_id || undefined,
        kanban_display: stage.kanban_display || 'column',
        style: stage.style,
      }));
      setStages(formattedStages);
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to load workflow');
      console.error('Error loading workflow:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleAddStage = () => {
    const newOrder = stages.length + 1;
    setStages([
      ...stages,
      {
        name: '',
        description: '',
        stage_type: 'standard',
        order: newOrder,
        is_active: true,
        isNew: true,
      },
    ]);
  };

  const handleRemoveStage = (index: number) => {
    const stage = stages[index];

    // If it's an existing stage, mark it for deletion
    if (stage.id && !stage.isNew) {
      setDeletedStageIds([...deletedStageIds, stage.id]);
    }

    // Remove from current stages
    const newStages = stages.filter((_, i) => i !== index);

    // Reorder remaining stages
    newStages.forEach((s, i) => {
      s.order = i + 1;
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

  const openAdvancedSettings = (index: number) => {
    setSelectedStageIndex(index);
    setAdvancedModalOpen(true);
  };

  const closeAdvancedSettings = () => {
    setAdvancedModalOpen(false);
    setSelectedStageIndex(null);
  };

  const handleEditStageStyle = (stageIndex: number) => {
    setEditingStageIndex(stageIndex);
    setStyleEditorOpen(true);
  };

  const handleSaveStageStyle = async (style: UpdateStageStyleRequest) => {
    if (editingStageIndex === null) return;

    const stage = stages[editingStageIndex];
    if (!stage.id) return;

    try {
      const updatedStage = await companyWorkflowService.updateStageStyle(stage.id, style);
      
      // Update the stage in the local state
      setStages(prevStages => 
        prevStages.map((s, index) => 
          index === editingStageIndex 
            ? { ...s, style: updatedStage.style }
            : s
        )
      );

      setStyleEditorOpen(false);
      setEditingStageIndex(null);
    } catch (error) {
      console.error('Error updating stage style:', error);
      setError('Failed to update stage style');
    }
  };

  const handleCancelStageStyle = () => {
    setStyleEditorOpen(false);
    setEditingStageIndex(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!workflowId) {
      setError('Workflow ID not found');
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
      setSaving(true);

      // Update workflow details
      await companyWorkflowService.updateWorkflow(workflowId, {
        name: workflowName,
        description: workflowDescription,
        phase_id: phaseId || undefined,
      });

      // Delete removed stages
      for (const stageId of deletedStageIds) {
        await companyWorkflowService.deleteStage(stageId);
      }

      // Update or create stages
      for (const stageData of stages) {
        if (stageData.isNew) {
          // Create new stage
          await companyWorkflowService.createStage({
            workflow_id: workflowId,
            name: stageData.name,
            description: stageData.description,
            stage_type: stageData.stage_type,
            order: stageData.order,
            is_active: stageData.is_active,
            allow_skip: stageData.allow_skip,
            estimated_duration_days: stageData.estimated_duration_days,
            default_role_ids: stageData.default_role_ids,
            deadline_days: stageData.deadline_days,
            estimated_cost: stageData.estimated_cost,
            next_phase_id: stageData.next_phase_id,
          });
        } else if (stageData.id) {
          // Update existing stage
          await companyWorkflowService.updateStage(stageData.id, {
            name: stageData.name,
            description: stageData.description,
            stage_type: stageData.stage_type,
            order: stageData.order,
            is_active: stageData.is_active,
            allow_skip: stageData.allow_skip,
            estimated_duration_days: stageData.estimated_duration_days,
            default_role_ids: stageData.default_role_ids,
            deadline_days: stageData.deadline_days,
            estimated_cost: stageData.estimated_cost,
            next_phase_id: stageData.next_phase_id,
            kanban_display: stageData.kanban_display,
          });
        }
      }

      // Reorder stages
      const stageIds = stages
        .filter((s) => s.id && !s.isNew)
        .map((s) => s.id!);

      if (stageIds.length > 0) {
        await companyWorkflowService.reorderStages(workflowId, {
          stage_ids_in_order: stageIds,
        });
      }

      navigate('/company/settings/workflows');
    } catch (err: any) {
      setError(err.message || 'Failed to update workflow');
      console.error('Error updating workflow:', err);
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

  if (!workflow) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <p className="text-red-800">Workflow not found</p>
      </div>
    );
  }

  return (
    <div>
      {/* Header */}
      <div className="mb-6">
        <button
          onClick={() => navigate('/company/settings/workflows')}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-4"
        >
          <ArrowLeft className="w-5 h-5" />
          Back to Workflows
        </button>
        <h1 className="text-2xl font-bold text-gray-900">Edit Workflow</h1>
        <p className="text-gray-600 mt-1">Update workflow details and stages</p>
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

            {/* Workflow Status Info */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <div className="flex items-center gap-2">
                <span className="text-sm font-medium text-blue-900">Status:</span>
                <span className="text-sm text-blue-800">{workflow.status}</span>
                {workflow.is_default && (
                  <span className="ml-2 px-2 py-1 text-xs font-medium bg-yellow-100 text-yellow-800 rounded">
                    Default
                  </span>
                )}
              </div>
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
              <div key={stage.id || index} className="bg-gray-50 rounded-lg p-4 border border-gray-200">
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-2">
                    <div className="flex items-center gap-2">
                      <span 
                        className="text-lg"
                        dangerouslySetInnerHTML={{ __html: stage.style?.icon || '📋' }}
                      />
                      <span className="text-sm font-medium text-gray-500">Stage {index + 1}</span>
                    </div>
                    {stage.isNew && (
                      <span className="px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded">
                        New
                      </span>
                    )}
                  </div>
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
                    {/* Style button */}
                    {!stage.isNew && (
                      <button
                        type="button"
                        onClick={() => handleEditStageStyle(index)}
                        className="p-1 text-blue-600 hover:text-blue-800"
                        title="Edit stage style"
                      >
                        <Settings className="w-4 h-4" />
                      </button>
                    )}
                    {/* Delete button */}
                    {stages.length > 1 && (
                      <button
                        type="button"
                        onClick={() => handleRemoveStage(index)}
                        className="p-1 text-red-600 hover:text-red-800"
                        title="Remove stage"
                      >
                        {stage.isNew ? <X className="w-4 h-4" /> : <Trash2 className="w-4 h-4" />}
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

                  {/* Kanban Display */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Kanban Display</label>
                    <select
                      value={stage.kanban_display || 'column'}
                      onChange={(e) => handleStageChange(index, 'kanban_display', e.target.value)}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    >
                      <option value="column">Column (Vertical)</option>
                      <option value="row">Row (Horizontal)</option>
                      <option value="none">Hidden</option>
                    </select>
                  </div>

                  {/* Next Phase (only for success/fail stages) */}
                  {(stage.stage_type === 'success' || stage.stage_type === 'fail') ? (
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Next Phase (Optional)
                      </label>
                      {loadingPhases ? (
                        <div className="text-sm text-gray-500 px-4 py-2">Loading phases...</div>
                      ) : phases.length === 0 ? (
                        <div className="text-sm text-gray-500 px-4 py-2">No phases available</div>
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
                        Auto-move to this phase when reaching this stage
                      </p>
                    </div>
                  ) : (
                    <div></div>
                  )}

                  {/* Phase Transition Visual Indicator (full width) */}
                  {(stage.stage_type === 'success' || stage.stage_type === 'fail') && stage.next_phase_id && getCompanyId() && (
                    <div className="md:col-span-2">
                      <PhaseTransitionIndicator
                        stage={{
                          ...stage,
                          workflow_id: workflowId || '',
                          stage_type: stage.stage_type.toUpperCase() as StageType,
                        } as WorkflowStage}
                        companyId={getCompanyId()!}
                        currentPhaseId={phaseId}
                      />
                    </div>
                  )}

                  {/* Description */}
                  <div className="md:col-span-2">
                    <label className="block text-sm font-medium text-gray-700 mb-2">Description</label>
                    <textarea
                      value={stage.description}
                      onChange={(e) => handleStageChange(index, 'description', e.target.value)}
                      rows={3}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      placeholder="Describe this stage..."
                    />
                  </div>

                  {/* Advanced Settings Button */}
                  <div className="md:col-span-2">
                    <button
                      type="button"
                      onClick={() => openAdvancedSettings(index)}
                      className="flex items-center gap-2 px-4 py-2 text-sm text-blue-600 hover:text-blue-800 hover:bg-blue-50 rounded-lg border border-blue-200 transition-colors"
                    >
                      <Settings className="w-4 h-4" />
                      Advanced Settings
                      {(stage.allow_skip || stage.default_role_ids?.length || stage.estimated_duration_days || stage.deadline_days || stage.estimated_cost) && (
                        <span className="ml-2 px-2 py-0.5 text-xs bg-blue-100 text-blue-700 rounded-full">Configured</span>
                      )}
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Custom Fields */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <CustomFieldEditor
            workflowId={workflowId!}
            onFieldsChange={setCustomFields}
          />
        </div>

        {/* Field Visibility Matrix */}
        {customFields.length > 0 && stages.length > 0 && (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <FieldVisibilityMatrix
              workflowId={workflowId!}
              stages={stages.map((s, idx) => ({
                ...s,
                id: s.id || `temp-${idx}`,
                workflow_id: workflowId!,
                description: s.description || null,
                is_active: s.is_active ?? true,
                allow_skip: s.allow_skip ?? false,
                estimated_duration_days: s.estimated_duration_days ?? null,
                default_role_ids: s.default_role_ids ?? null,
                default_assigned_users: s.default_assigned_users ?? null,
                email_template_id: s.email_template_id ?? null,
                custom_email_text: s.custom_email_text ?? null,
                deadline_days: s.deadline_days ?? null,
                estimated_cost: s.estimated_cost ?? null,
                created_at: new Date().toISOString(),
                updated_at: new Date().toISOString()
              } as WorkflowStage))}
              fields={customFields}
              onConfigurationsChange={setFieldConfigurations}
            />
          </div>
        )}

        {/* Validation Rules */}
        {customFields.length > 0 && stages.length > 0 && (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <ValidationRuleEditor
              workflowId={workflowId!}
              stages={stages.map((s, idx) => ({
                ...s,
                id: s.id || `temp-${idx}`,
                workflow_id: workflowId!,
                description: s.description || null,
                is_active: s.is_active ?? true,
                allow_skip: s.allow_skip ?? false,
                estimated_duration_days: s.estimated_duration_days ?? null,
                default_role_ids: s.default_role_ids ?? null,
                default_assigned_users: s.default_assigned_users ?? null,
                email_template_id: s.email_template_id ?? null,
                custom_email_text: s.custom_email_text ?? null,
                deadline_days: s.deadline_days ?? null,
                estimated_cost: s.estimated_cost ?? null,
                created_at: new Date().toISOString(),
                updated_at: new Date().toISOString()
              } as WorkflowStage))}
              customFields={customFields}
            />
          </div>
        )}

        {/* Actions */}
        <div className="flex items-center justify-end gap-3">
          <button
            type="button"
            onClick={() => navigate('/company/settings/workflows')}
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

      {/* Advanced Settings Modal */}
      {advancedModalOpen && selectedStageIndex !== null && (
        <div className="fixed inset-0 z-50 overflow-y-auto">
          <div className="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
            {/* Background overlay */}
            <div
              className="fixed inset-0 transition-opacity bg-gray-500 bg-opacity-75"
              onClick={closeAdvancedSettings}
            ></div>

            {/* Modal panel */}
            <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-2xl sm:w-full">
              <div className="bg-white px-6 py-6">
                {/* Header */}
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-lg font-semibold text-gray-900">
                    Advanced Settings - {stages[selectedStageIndex].name || 'New Stage'}
                  </h3>
                  <button
                    onClick={closeAdvancedSettings}
                    className="text-gray-400 hover:text-gray-600"
                  >
                    <X className="w-5 h-5" />
                  </button>
                </div>

                {/* Advanced Settings Form */}
                <div className="space-y-4 max-h-96 overflow-y-auto">
                  {/* Allow Skip */}
                  <div className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                    <input
                      type="checkbox"
                      id={`modal_allow_skip`}
                      checked={stages[selectedStageIndex].allow_skip || false}
                      onChange={(e) => handleStageChange(selectedStageIndex, 'allow_skip', e.target.checked)}
                      className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                    />
                    <label htmlFor={`modal_allow_skip`} className="text-sm font-medium text-gray-700">
                      Allow skipping this stage (optional)
                    </label>
                  </div>

                  {/* Estimated Duration Days */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Estimated Duration (days)</label>
                    <input
                      type="number"
                      min="0"
                      value={stages[selectedStageIndex].estimated_duration_days || ''}
                      onChange={(e) => handleStageChange(selectedStageIndex, 'estimated_duration_days', e.target.value ? parseInt(e.target.value) : undefined)}
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
                      value={stages[selectedStageIndex].deadline_days || ''}
                      onChange={(e) => handleStageChange(selectedStageIndex, 'deadline_days', e.target.value ? parseInt(e.target.value) : undefined)}
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
                      value={stages[selectedStageIndex].estimated_cost || ''}
                      onChange={(e) => handleStageChange(selectedStageIndex, 'estimated_cost', e.target.value || undefined)}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      placeholder="e.g., 100.00"
                    />
                  </div>

                  {/* Default Roles */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Default Roles</label>
                    {loadingRoles ? (
                      <div className="text-sm text-gray-500">Loading roles...</div>
                    ) : roles.length === 0 ? (
                      <div className="text-sm text-gray-500">
                        No roles available. <a href="/company/settings/roles" className="text-blue-600 hover:underline">Create roles first</a>
                      </div>
                    ) : (
                      <div className="space-y-2 p-4 border border-gray-300 rounded-lg bg-gray-50 max-h-48 overflow-y-auto">
                        {roles.map((role) => (
                          <label key={role.id} className="flex items-center gap-2 cursor-pointer hover:bg-gray-100 p-2 rounded">
                            <input
                              type="checkbox"
                              checked={(stages[selectedStageIndex].default_role_ids || []).includes(role.id)}
                              onChange={(e) => {
                                const currentRoles = stages[selectedStageIndex].default_role_ids || [];
                                const newRoles = e.target.checked
                                  ? [...currentRoles, role.id]
                                  : currentRoles.filter(id => id !== role.id);
                                handleStageChange(selectedStageIndex, 'default_role_ids', newRoles.length > 0 ? newRoles : undefined);
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

                  {/* Next Phase (only for success/fail stages) */}
                  {(stages[selectedStageIndex].stage_type === 'success' || stages[selectedStageIndex].stage_type === 'fail') && (
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Next Phase (Optional)
                      </label>
                      {loadingPhases ? (
                        <div className="text-sm text-gray-500">Loading phases...</div>
                      ) : phases.length === 0 ? (
                        <div className="text-sm text-gray-500">
                          No phases available. <a href="/company/settings/phases" className="text-blue-600 hover:underline">Create phases first</a>
                        </div>
                      ) : (
                        <select
                          value={stages[selectedStageIndex].next_phase_id || ''}
                          onChange={(e) => handleStageChange(selectedStageIndex, 'next_phase_id', e.target.value || undefined)}
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

                  {/* Active Toggle */}
                  <div className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                    <input
                      type="checkbox"
                      id={`modal_is_active`}
                      checked={stages[selectedStageIndex].is_active}
                      onChange={(e) => handleStageChange(selectedStageIndex, 'is_active', e.target.checked)}
                      className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                    />
                    <label htmlFor={`modal_is_active`} className="text-sm font-medium text-gray-700">
                      Stage is active
                    </label>
                  </div>
                </div>

                {/* Modal Actions */}
                <div className="mt-6 flex items-center justify-end gap-3">
                  <button
                    type="button"
                    onClick={closeAdvancedSettings}
                    className="px-4 py-2 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                  >
                    Done
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Stage Style Editor Modal */}
      {styleEditorOpen && editingStageIndex !== null && (
        <StageStyleEditor
          stageStyle={stages[editingStageIndex].style || { icon: '📋', color: '#374151', background_color: '#f3f4f6' }}
          onSave={handleSaveStageStyle}
          onCancel={handleCancelStageStyle}
          isOpen={styleEditorOpen}
        />
      )}
    </div>
  );
}
