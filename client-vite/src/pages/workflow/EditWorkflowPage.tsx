import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { ArrowLeft, Save, Plus, X, Trash2, ArrowUp, ArrowDown, Settings, Palette } from 'lucide-react';
import { toast } from 'react-toastify';
import { companyWorkflowService } from '../../services/companyWorkflowService.ts';
import { phaseService } from '../../services/phaseService.ts';
import { companyInterviewTemplateService, type InterviewTemplate } from '../../services/companyInterviewTemplateService.ts';
import { api } from '../../lib/api.ts';
import type { CompanyWorkflow, WorkflowStage, StageType, InterviewConfiguration } from '../../types/workflow.ts';
import type { CompanyRole } from '../../types/company.ts';
import type { Phase } from '../../types/phase.ts';
import type { UpdateStageStyleRequest } from '../../types/stageStyle.ts';
import { PhaseTransitionIndicator } from '../../components/workflow';
import { StageStyleEditor } from '../../components/workflow/StageStyleEditor.tsx';

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
  default_assigned_users?: string[];
  email_template_id?: string;
  custom_email_text?: string;
  deadline_days?: number;
  estimated_cost?: string;
  next_phase_id?: string;
  kanban_display?: string;
  style?: {
    icon: string;
    color: string;
    background_color: string;
  };
  interview_configurations?: InterviewConfiguration[];
}

export default function EditWorkflowPage() {
  const navigate = useNavigate();
  const { workflowId } = useParams<{ workflowId: string }>();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [roles, setRoles] = useState<CompanyRole[]>([]);
  const [loadingRoles, setLoadingRoles] = useState(true);
  const [phases, setPhases] = useState<Phase[]>([]);
  const [loadingPhases, setLoadingPhases] = useState(true);
  const [interviewTemplates, setInterviewTemplates] = useState<InterviewTemplate[]>([]);
  const [loadingTemplates, setLoadingTemplates] = useState(false);

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
      toast.error('Workflow ID not found');
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
      const formattedStages: StageFormData[] = stagesData.map((stage) => {
        // Convert interview_configurations from backend format to frontend format
        let interviewConfigs: InterviewConfiguration[] | undefined = undefined;
        if (stage.interview_configurations && Array.isArray(stage.interview_configurations)) {
          interviewConfigs = stage.interview_configurations.map((config: any) => ({
            template_id: config.template_id || config.templateId || '',
            mode: (config.mode || 'AUTOMATIC') as 'AUTOMATIC' | 'MANUAL',
          }));
          console.log('Loaded interview_configurations for stage', stage.id, ':', interviewConfigs);
        }
        
        return {
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
          interview_configurations: interviewConfigs,
        };
      });
      setStages(formattedStages);
    } catch (err: any) {
      toast.error(err.message || 'Failed to load workflow');
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

  const loadInterviewTemplates = async () => {
    const companyId = getCompanyId();
    if (!companyId) {
      console.error('Company ID not found');
      return;
    }

    try {
      setLoadingTemplates(true);
      // Load all templates (ENABLED and DRAFT) - don't filter by status
      const templates = await companyInterviewTemplateService.listTemplates({
        page_size: 100,
      });
      console.log('Loaded interview templates:', templates);
      setInterviewTemplates(templates);
      
      if (templates.length === 0) {
        console.warn('No interview templates found for company:', companyId);
      }
    } catch (err: any) {
      console.error('Failed to load interview templates:', err);
      const errorMessage = err?.message || 'Failed to load interview templates';
      toast.error(errorMessage);
      setInterviewTemplates([]);
    } finally {
      setLoadingTemplates(false);
    }
  };

  const openAdvancedSettings = async (index: number) => {
    setSelectedStageIndex(index);
    setAdvancedModalOpen(true);
    await loadInterviewTemplates();
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
      toast.error('Failed to update stage style');
    }
  };

  const handleCancelStageStyle = () => {
    setStyleEditorOpen(false);
    setEditingStageIndex(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!workflowId) {
      toast.error('Workflow ID not found');
      return;
    }

    if (!workflowName) {
      toast.error('Workflow name is required');
      return;
    }

    if (stages.length === 0) {
      toast.error('At least one stage is required');
      return;
    }

    // Validate stages
    for (const stage of stages) {
      if (!stage.name) {
        toast.error('All stages must have a name');
        return;
      }
    }

    // Validate workflow stage rules
    const initialStages = stages.filter(s => s.stage_type === 'initial');
    const successStages = stages.filter(s => s.stage_type === 'success');
    const standardStages = stages.filter(s => s.stage_type === 'standard'); // 'standard' maps to 'progress' in backend
    
    // Rule 1: Only one INITIAL stage allowed
    if (initialStages.length > 1) {
      toast.error(`Only one INITIAL stage is allowed. Found ${initialStages.length} INITIAL stages: ${initialStages.map(s => s.name).join(', ')}`);
      return;
    }
    
    // Rule 2: Only one SUCCESS stage allowed
    if (successStages.length > 1) {
      toast.error(`Only one SUCCESS stage is allowed. Found ${successStages.length} SUCCESS stages: ${successStages.map(s => s.name).join(', ')}`);
      return;
    }
    
    // Rule 3: Always must have a SUCCESS stage
    if (successStages.length === 0) {
      toast.error('A workflow must have at least one SUCCESS stage');
      return;
    }
    
    // Rule 4: If there are PROGRESS (standard) stages, there must be an INITIAL stage
    if (standardStages.length > 0 && initialStages.length === 0) {
      toast.error('If a workflow has PROGRESS stages, it must have an INITIAL stage');
      return;
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
        // Filter out empty interview configurations (template_id is empty)
        // Always send the field if it exists (even if empty array) so backend can update it
        let interviewConfigsToSend: InterviewConfiguration[] | undefined = undefined;
        if (stageData.interview_configurations !== undefined) {
          const validInterviewConfigs = stageData.interview_configurations.filter(
            config => config.template_id && config.template_id.trim() !== ''
          );
          // Always send array (even if empty) when field was modified
          interviewConfigsToSend = validInterviewConfigs;
          console.log(`Stage ${stageData.id || 'NEW'} - Original configs:`, stageData.interview_configurations);
          console.log(`Stage ${stageData.id || 'NEW'} - Valid configs to send:`, interviewConfigsToSend);
        }

        if (stageData.isNew) {
          // Create new stage
          const createData = {
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
            interview_configurations: interviewConfigsToSend,
          };
          console.log('Creating stage with data:', JSON.stringify(createData, null, 2));
          await companyWorkflowService.createStage(createData);
        } else if (stageData.id) {
          // Update existing stage
          const updateData = {
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
            interview_configurations: interviewConfigsToSend,
          };
          console.log('Updating stage', stageData.id, 'with data:', JSON.stringify(updateData, null, 2));
          await companyWorkflowService.updateStage(stageData.id, updateData);
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

      toast.success('Workflow updated successfully');
      navigate('/company/settings/workflows');
    } catch (err: any) {
      const errorMessage = err.message || 'Failed to update workflow';
      toast.error(errorMessage);
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
                    <div className="relative group">
                      <button
                        type="button"
                        onClick={() => handleMoveStageUp(index)}
                        disabled={index === 0}
                        className="p-1 text-gray-600 hover:text-gray-900 disabled:text-gray-300 disabled:cursor-not-allowed"
                      >
                        <ArrowUp className="w-4 h-4" />
                      </button>
                      <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-3 py-2 bg-gray-900 text-white text-xs rounded-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 whitespace-nowrap pointer-events-none z-10">
                        Move up
                        <div className="absolute top-full left-1/2 -translate-x-1/2 -mt-1 border-4 border-transparent border-t-gray-900"></div>
                      </div>
                    </div>
                    <div className="relative group">
                      <button
                        type="button"
                        onClick={() => handleMoveStageDown(index)}
                        disabled={index === stages.length - 1}
                        className="p-1 text-gray-600 hover:text-gray-900 disabled:text-gray-300 disabled:cursor-not-allowed"
                      >
                        <ArrowDown className="w-4 h-4" />
                      </button>
                      <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-3 py-2 bg-gray-900 text-white text-xs rounded-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 whitespace-nowrap pointer-events-none z-10">
                        Move down
                        <div className="absolute top-full left-1/2 -translate-x-1/2 -mt-1 border-4 border-transparent border-t-gray-900"></div>
                      </div>
                    </div>
                    {/* Style button */}
                    {!stage.isNew && (
                      <div className="relative group">
                        <button
                          type="button"
                          onClick={() => handleEditStageStyle(index)}
                          className="p-1 text-purple-600 hover:text-purple-800"
                          title="Edit stage style"
                        >
                          <Palette className="w-4 h-4" />
                        </button>
                        <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-3 py-2 bg-gray-900 text-white text-xs rounded-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 whitespace-nowrap pointer-events-none z-10">
                          Edit stage style
                          <div className="absolute top-full left-1/2 -translate-x-1/2 -mt-1 border-4 border-transparent border-t-gray-900"></div>
                        </div>
                      </div>
                    )}
                    {/* Delete button */}
                    {stages.length > 1 && (
                      <div className="relative group">
                        <button
                          type="button"
                          onClick={() => handleRemoveStage(index)}
                          className="p-1 text-red-600 hover:text-red-800"
                        >
                          {stage.isNew ? <X className="w-4 h-4" /> : <Trash2 className="w-4 h-4" />}
                        </button>
                        <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-3 py-2 bg-gray-900 text-white text-xs rounded-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 whitespace-nowrap pointer-events-none z-10">
                          Remove stage
                          <div className="absolute top-full left-1/2 -translate-x-1/2 -mt-1 border-4 border-transparent border-t-gray-900"></div>
                        </div>
                      </div>
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
                      <option value="archived">Archived</option>
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

                  {/* Default Role */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Responsible Role</label>
                    {loadingRoles ? (
                      <div className="text-sm text-gray-500 px-4 py-2">Loading roles...</div>
                    ) : roles.length === 0 ? (
                      <div className="text-sm text-gray-500 px-4 py-2">
                        No roles available. <a href="/company/settings/roles" className="text-blue-600 hover:underline">Create roles first</a>
                      </div>
                    ) : (
                      <select
                        value={stage.default_role_ids?.[0] || ''}
                        onChange={(e) => {
                          const roleId = e.target.value || undefined;
                          handleStageChange(index, 'default_role_ids', roleId ? [roleId] : undefined);
                        }}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      >
                        <option value="">Not assigned</option>
                        {roles.map((role) => (
                          <option key={role.id} value={role.id}>
                            {role.name}
                          </option>
                        ))}
                      </select>
                    )}
                    <p className="mt-1 text-xs text-gray-500">
                      Primary role responsible for this stage
                    </p>
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
                      {(stage.allow_skip || stage.default_role_ids?.length || stage.estimated_duration_days || stage.deadline_days || stage.estimated_cost || stage.interview_configurations?.length) && (
                        <span className="ml-2 px-2 py-0.5 text-xs bg-blue-100 text-blue-700 rounded-full">Configured</span>
                      )}
                    </button>
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
            <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-5xl sm:w-full">
              <div className="bg-white px-6 py-6">
                {/* Header */}
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-lg font-semibold text-gray-900">
                    Advanced Settings - {stages[selectedStageIndex].name || 'New Stage'}
                  </h3>
                  <div className="relative group">
                    <button
                      onClick={closeAdvancedSettings}
                      className="text-gray-400 hover:text-gray-600"
                    >
                      <X className="w-5 h-5" />
                    </button>
                    <div className="absolute bottom-full right-0 mb-2 px-3 py-2 bg-gray-900 text-white text-xs rounded-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 whitespace-nowrap pointer-events-none z-10">
                      Close
                      <div className="absolute top-full right-4 -mt-1 border-4 border-transparent border-t-gray-900"></div>
                    </div>
                  </div>
                </div>

                {/* Advanced Settings Form - Reorganized in columns */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 max-h-[600px] overflow-y-auto pr-2">
                  {/* Left Column */}
                  <div className="space-y-4">
                  {/* Allow Skip and Active Toggle */}
                  <div className="flex items-center gap-6 p-3 bg-gray-50 rounded-lg">
                    <div className="flex items-center gap-3">
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
                    <div className="flex items-center gap-3">
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

                  {/* Estimated Duration and Deadline Days */}
                  <div className="grid grid-cols-2 gap-4">
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
                  </div>

                  {/* Right Column */}
                  <div className="space-y-4">
                    {/* Interview Configurations */}
                    <div className="border border-gray-200 rounded-lg p-4 bg-blue-50">
                      <h4 className="text-sm font-semibold text-gray-900 mb-3">Interview Templates</h4>
                      <p className="text-xs text-gray-600 mb-4">
                        Configure which interview templates should be used in this stage. Interviews can be created automatically or manually.
                      </p>
                      
                      {loadingTemplates ? (
                        <div className="text-sm text-gray-500 py-4">Loading templates...</div>
                      ) : interviewTemplates.length === 0 ? (
                        <div className="text-sm text-gray-500 py-4 space-y-2">
                          <p>No interview templates available.</p>
                          <p>
                            <a href="/company/interview-templates" className="text-blue-600 hover:underline font-medium">
                              Create templates first
                            </a>
                          </p>
                          <p className="text-xs text-gray-400 mt-2">
                            (Check browser console for details)
                          </p>
                        </div>
                      ) : (
                        <div className="space-y-3">
                          {(stages[selectedStageIndex].interview_configurations || []).map((config, configIndex) => (
                            <div key={configIndex} className="flex items-center gap-3 p-3 bg-white border border-gray-300 rounded-lg">
                              <div className="flex-1">
                                <select
                                  value={config.template_id}
                                  onChange={(e) => {
                                    const currentConfigs = stages[selectedStageIndex].interview_configurations || [];
                                    const newConfigs = [...currentConfigs];
                                    newConfigs[configIndex] = { ...config, template_id: e.target.value };
                                    handleStageChange(selectedStageIndex, 'interview_configurations', newConfigs);
                                  }}
                                  className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                >
                                  <option value="">Select template...</option>
                                  {interviewTemplates.map((template) => (
                                    <option key={template.id} value={template.id}>
                                      {template.name} ({template.type})
                                    </option>
                                  ))}
                                </select>
                              </div>
                              <select
                                value={config.mode}
                                onChange={(e) => {
                                  const currentConfigs = stages[selectedStageIndex].interview_configurations || [];
                                  const newConfigs = [...currentConfigs];
                                  newConfigs[configIndex] = { ...config, mode: e.target.value as 'AUTOMATIC' | 'MANUAL' };
                                  handleStageChange(selectedStageIndex, 'interview_configurations', newConfigs);
                                }}
                                className="px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                              >
                                <option value="AUTOMATIC">Automatic</option>
                                <option value="MANUAL">Manual</option>
                              </select>
                              <button
                                type="button"
                                onClick={() => {
                                  const currentConfigs = stages[selectedStageIndex].interview_configurations || [];
                                  const newConfigs = currentConfigs.filter((_, i) => i !== configIndex);
                                  // Always set as array (empty array if no configs) so backend can process it
                                  handleStageChange(selectedStageIndex, 'interview_configurations', newConfigs);
                                }}
                                className="p-2 text-red-600 hover:text-red-800 hover:bg-red-50 rounded-lg transition-colors"
                              >
                                <X className="w-4 h-4" />
                              </button>
                            </div>
                          ))}
                          
                          <button
                            type="button"
                            onClick={() => {
                              const currentConfigs = stages[selectedStageIndex].interview_configurations || [];
                              const newConfigs = [...currentConfigs, { template_id: '', mode: 'AUTOMATIC' as const }];
                              handleStageChange(selectedStageIndex, 'interview_configurations', newConfigs);
                            }}
                            className="w-full flex items-center justify-center gap-2 px-4 py-2 text-sm text-blue-600 bg-white border border-blue-300 rounded-lg hover:bg-blue-50 transition-colors"
                          >
                            <Plus className="w-4 h-4" />
                            Add Interview Template
                          </button>
                        </div>
                      )}
                    </div>
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
