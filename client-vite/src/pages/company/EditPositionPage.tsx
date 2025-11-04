import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Save } from 'lucide-react';
import { PositionService } from '../../services/positionService';
import type { UpdatePositionRequest, Position, JobPositionWorkflow } from '../../types/position';
import { DynamicCustomFields } from '../../components/jobPosition/DynamicCustomFields';
import { WysiwygEditor } from '../../components/common';

export default function EditPositionPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [position, setPosition] = useState<Position | null>(null);
  const [workflows, setWorkflows] = useState<JobPositionWorkflow[]>([]);
  const [selectedWorkflow, setSelectedWorkflow] = useState<JobPositionWorkflow | null>(null);

  const [formData, setFormData] = useState<UpdatePositionRequest>({
    job_position_workflow_id: null,
    stage_id: null,
    phase_workflows: {},
    custom_fields_values: {},
    title: '',
    description: '',
    job_category: 'other',
    visibility: 'hidden',
    open_at: null,
    application_deadline: null,
    public_slug: null,
  });

  const [companyId, setCompanyId] = useState<string>('');

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
    if (id) {
      loadPosition();
      loadWorkflows();
    }
  }, [id]);

  useEffect(() => {
    if (formData.job_position_workflow_id && workflows.length > 0) {
      const workflow = workflows.find(w => w.id === formData.job_position_workflow_id);
      setSelectedWorkflow(workflow || null);
    } else {
      setSelectedWorkflow(null);
    }
  }, [formData.job_position_workflow_id, workflows]);

  const loadPosition = async () => {
    if (!id) return;

    try {
      setLoading(true);
      const positionData = await PositionService.getPositionById(id);

      // Load workflow if available
      if (positionData.job_position_workflow_id) {
        try {
          const workflowData = await PositionService.getWorkflow(positionData.job_position_workflow_id);
          console.log('[EditPositionPage] Loaded workflow:', workflowData);
          console.log('[EditPositionPage] Workflow custom_fields_config:', workflowData.custom_fields_config);
          setSelectedWorkflow(workflowData);
        } catch (err) {
          console.error('Error loading workflow:', err);
        }
      }

      setPosition(positionData);
      setCompanyId(positionData.company_id);

      // Convert Position to form data (simplified)
      setFormData({
        job_position_workflow_id: positionData.job_position_workflow_id || null,
        stage_id: positionData.stage_id || null,
        phase_workflows: positionData.phase_workflows || {},
        custom_fields_values: positionData.custom_fields_values || {},
        title: positionData.title,
        description: positionData.description || '',
        job_category: positionData.job_category || 'other',
        visibility: positionData.visibility || 'hidden',
        open_at: positionData.open_at || null,
        application_deadline: positionData.application_deadline || null,
        public_slug: positionData.public_slug || null,
      });

      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to load position');
      console.error('Error loading position:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadWorkflows = async () => {
    try {
      const companyId = getCompanyId();
      if (!companyId) return;

      const workflowsList = await PositionService.getWorkflows(companyId);
      setWorkflows(workflowsList);
    } catch (err) {
      console.error('Error loading workflows:', err);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!id) {
      setError('Position ID not found');
      return;
    }

    if (!formData.title) {
      setError('Title is required');
      return;
    }

    try {
      setSaving(true);
      await PositionService.updatePosition(id, formData);
      navigate(`/company/positions/${id}`);
    } catch (err: any) {
      setError(err.message || 'Failed to update position');
      console.error('Error updating position:', err);
    } finally {
      setSaving(false);
    }
  };

  const handleWorkflowChange = async (workflowId: string | null) => {
    setFormData({
      ...formData,
      job_position_workflow_id: workflowId,
      stage_id: null, // Reset stage when workflow changes
    });

    if (workflowId) {
      try {
        const workflowData = await PositionService.getWorkflow(workflowId);
        setSelectedWorkflow(workflowData);
      } catch (err) {
        console.error('Error loading workflow:', err);
      }
    } else {
      setSelectedWorkflow(null);
    }
  };

  const currentStage = selectedWorkflow?.stages.find(
    (s) => s.id === formData.stage_id
  ) || null;

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
          onClick={() => navigate(`/company/positions/${id}`)}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-4"
        >
          <ArrowLeft className="w-5 h-5" />
          Back to Position
        </button>
        <h1 className="text-2xl font-bold text-gray-900">Edit Position</h1>
        <p className="text-gray-600 mt-1">Update job opening details</p>
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
                Job Title <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                required
                value={formData.title}
                onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="e.g., Senior Software Engineer"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Job Category</label>
              <select
                value={formData.job_category}
                onChange={(e) => setFormData({ ...formData, job_category: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="other">Other</option>
                <option value="engineering">Engineering</option>
                <option value="design">Design</option>
                <option value="product">Product</option>
                <option value="marketing">Marketing</option>
                <option value="sales">Sales</option>
                <option value="operations">Operations</option>
                <option value="hr">HR</option>
                <option value="finance">Finance</option>
                <option value="legal">Legal</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Visibility</label>
              <select
                value={formData.visibility}
                onChange={(e) => setFormData({ ...formData, visibility: e.target.value as any })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="hidden">Hidden</option>
                <option value="internal">Internal</option>
                <option value="public">Public</option>
              </select>
            </div>

            {/* Workflow Selector */}
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-2">Workflow</label>
              <select
                value={formData.job_position_workflow_id || ''}
                onChange={(e) => handleWorkflowChange(e.target.value || null)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">No Workflow (Legacy)</option>
                {workflows.map((workflow) => (
                  <option key={workflow.id} value={workflow.id}>
                    {workflow.name} ({workflow.workflow_type})
                  </option>
                ))}
              </select>
              <p className="mt-1 text-sm text-gray-500">
                Select a workflow to manage this position through stages
              </p>
            </div>

            {/* Stage Selector */}
            {selectedWorkflow && selectedWorkflow.stages.length > 0 && (
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-2">Current Stage</label>
                <select
                  value={formData.stage_id || ''}
                  onChange={(e) => setFormData({ ...formData, stage_id: e.target.value || null })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="">No Stage</option>
                  {selectedWorkflow.stages.map((stage) => (
                    <option key={stage.id} value={stage.id}>
                      {stage.name} ({stage.status_mapping})
                    </option>
                  ))}
                </select>
                <p className="mt-1 text-sm text-gray-500">
                  Current stage in the workflow
                </p>
              </div>
            )}

            {/* Description */}
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Job Description
              </label>
              <div className="border border-gray-300 rounded-lg overflow-hidden">
                <WysiwygEditor
                  value={formData.description || ''}
                  onChange={(content) => setFormData({ ...formData, description: content })}
                  placeholder="Describe the role, responsibilities, and what you're looking for..."
                  height={400}
                  className="w-full"
                />
              </div>
            </div>

            {/* Dates */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Open At</label>
              <input
                type="datetime-local"
                value={formData.open_at ? new Date(formData.open_at).toISOString().slice(0, 16) : ''}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    open_at: e.target.value ? new Date(e.target.value).toISOString() : null,
                  })
                }
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Application Deadline</label>
              <input
                type="date"
                value={formData.application_deadline || ''}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    application_deadline: e.target.value || null,
                  })
                }
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            {/* Public Slug */}
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-2">Public Slug (SEO)</label>
              <input
                type="text"
                value={formData.public_slug || ''}
                onChange={(e) => setFormData({ ...formData, public_slug: e.target.value || null })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="e.g., senior-software-engineer"
              />
              <p className="mt-1 text-sm text-gray-500">
                URL-friendly identifier for public job board
              </p>
            </div>
          </div>
        </div>

        {/* Custom Fields */}
        {selectedWorkflow && (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Custom Fields</h2>
            <DynamicCustomFields
              workflow={selectedWorkflow}
              currentStage={currentStage}
              customFieldsValues={formData.custom_fields_values || {}}
              onChange={(values) => setFormData({ ...formData, custom_fields_values: values })}
              readOnly={false}
            />
          </div>
        )}

        {/* Actions */}
        <div className="flex items-center justify-end gap-3">
          <button
            type="button"
            onClick={() => navigate(`/company/positions/${id}`)}
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
