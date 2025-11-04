import { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { ArrowLeft, Save, Plus, X } from 'lucide-react';
import { PositionService } from '../../services/positionService';
import type { CreatePositionRequest, JobPositionWorkflow } from '../../types/position';
import { PhaseWorkflowSelector } from '../../components/workflow';
import { WysiwygEditor } from '../../components/common';

export default function CreatePositionPage() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [currentWorkflow, setCurrentWorkflow] = useState<JobPositionWorkflow | null>(null);
  const [loadingWorkflow, setLoadingWorkflow] = useState(false);

  const [formData, setFormData] = useState<CreatePositionRequest>({
    company_id: '',
    job_position_workflow_id: null,
    phase_workflows: {},  // Phase 12.8: phase_id -> workflow_id mapping
    title: '',
    description: '',
    job_category: 'Other',
    custom_fields_values: {},
    application_deadline: '',
    visibility: 'hidden',
  });



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

  // Load Job Position Workflow from URL parameter
  useEffect(() => {
    const loadWorkflow = async () => {
      const companyId = getCompanyId();
      if (!companyId) {
        return;
      }

      // Get workflow_id from URL parameter
      const workflowId = searchParams.get('workflow_id');
      
      if (!workflowId) {
        // If no workflow_id in URL, try to get default workflow
        try {
          setLoadingWorkflow(true);
          const workflows = await PositionService.getWorkflows(companyId);
          if (workflows.length > 0) {
            const defaultWorkflow = workflows.find(w => w.workflow_type === 'standard') || workflows[0];
            const fullWorkflow = await PositionService.getWorkflow(defaultWorkflow.id);
            setCurrentWorkflow(fullWorkflow);
            setFormData(prev => ({
              ...prev,
              job_position_workflow_id: defaultWorkflow.id,
              stage_id: fullWorkflow.stages && fullWorkflow.stages.length > 0 ? fullWorkflow.stages[0].id : undefined
            }));
          } else {
            setError('No workflows available. Please create a workflow first.');
          }
        } catch (err: any) {
          console.error('Error loading default workflow:', err);
          setError('Failed to load workflow. Please go back and select a workflow.');
        } finally {
          setLoadingWorkflow(false);
        }
        return;
      }

      try {
        setLoadingWorkflow(true);
        const fullWorkflow = await PositionService.getWorkflow(workflowId);
        setCurrentWorkflow(fullWorkflow);
        
        // Set workflow ID and first stage
        setFormData(prev => ({
          ...prev,
          job_position_workflow_id: workflowId,
          stage_id: fullWorkflow.stages && fullWorkflow.stages.length > 0 ? fullWorkflow.stages[0].id : undefined
        }));
      } catch (err: any) {
        console.error('Error loading workflow:', err);
        setError('Failed to load workflow. Please go back and select a workflow.');
      } finally {
        setLoadingWorkflow(false);
      }
    };

    loadWorkflow();
  }, [searchParams]);


  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    const companyId = getCompanyId();
    if (!companyId) {
      setError('Company ID not found');
      return;
    }

    // Wait for workflow to be loaded
    if (loadingWorkflow) {
      setError('Please wait while the workflow is being loaded...');
      return;
    }

    if (!formData.title) {
      setError('Title is required');
      return;
    }

    // Try to load workflow if not set - use URL parameter if available
    const workflowIdFromUrl = searchParams.get('workflow_id');
    if (!formData.job_position_workflow_id) {
      if (workflowIdFromUrl) {
        // If workflow_id is in URL but not in formData, try to load it
        setError('Workflow is still loading. Please wait a moment and try again.');
        return;
      }
      
      // If no workflow_id in URL, try to load default
      try {
        setLoadingWorkflow(true);
        const workflows = await PositionService.getWorkflows(companyId);
        if (workflows.length > 0) {
          const defaultWorkflow = workflows.find(w => w.workflow_type === 'standard') || workflows[0];
          const fullWorkflow = await PositionService.getWorkflow(defaultWorkflow.id);
          setCurrentWorkflow(fullWorkflow);
          setFormData(prev => ({
            ...prev,
            job_position_workflow_id: defaultWorkflow.id,
            stage_id: fullWorkflow.stages && fullWorkflow.stages.length > 0 ? fullWorkflow.stages[0].id : undefined
          }));
        } else {
          setError('No workflows available. Please create a workflow first.');
          setLoadingWorkflow(false);
          return;
        }
      } catch (err: any) {
        console.error('Error loading default workflow:', err);
        setError('Failed to load workflow. Please go back and select a workflow.');
        setLoadingWorkflow(false);
        return;
      } finally {
        setLoadingWorkflow(false);
      }
    }

    try {
      setLoading(true);

      // Use workflow_id from URL if formData doesn't have it (fallback)
      const finalWorkflowId = formData.job_position_workflow_id || workflowIdFromUrl;
      if (!finalWorkflowId) {
        setError('Opening Flow (Job Position Workflow) is required. Please go back and select a workflow.');
        return;
      }

      const requestData: CreatePositionRequest = {
        ...formData,
        company_id: companyId,
        job_position_workflow_id: finalWorkflowId,
      };

      await PositionService.createPosition(requestData);
      navigate('/company/positions');
    } catch (err: any) {
      setError(err.message || 'Failed to create position');
      console.error('Error creating position:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      {/* Header */}
      <div className="mb-6">
        <button
          onClick={() => navigate('/company/positions')}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-4"
        >
          <ArrowLeft className="w-5 h-5" />
          Back to Positions
        </button>
        <h1 className="text-2xl font-bold text-gray-900">
          Create Job Position
          {currentWorkflow && !loadingWorkflow && (
            <span className="text-lg font-normal text-gray-600"> ({currentWorkflow.name})</span>
          )}
        </h1>
        <p className="text-gray-600 mt-1">Post a new job opening</p>
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
            {/* Title */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Job Title <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                required
                value={formData.title}
                onChange={(e) => setFormData(prev => ({ ...prev, title: e.target.value }))}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="e.g., Senior Software Engineer"
              />
            </div>

            {/* Application Deadline */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Application Deadline</label>
              <input
                type="date"
                value={formData.application_deadline || ''}
                onChange={(e) => setFormData(prev => ({ ...prev, application_deadline: e.target.value }))}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            {/* Job Category */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Job Category <span className="text-red-500">*</span>
              </label>
              <select
                value={formData.job_category || 'Other'}
                onChange={(e) => setFormData(prev => ({ ...prev, job_category: e.target.value }))}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="Technology">Technology</option>
                <option value="Operations">Operations</option>
                <option value="Sales">Sales</option>
                <option value="Marketing">Marketing</option>
                <option value="Administration">Administration</option>
                <option value="Human Resources">Human Resources</option>
                <option value="Finance">Finance</option>
                <option value="Customer Service">Customer Service</option>
                <option value="Other">Other</option>
              </select>
            </div>

            {/* Visibility Options */}
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Visibility <span className="text-red-500">*</span>
              </label>
              <div className="flex flex-wrap items-center gap-6">
                <div className="flex items-center gap-2">
                  <input
                    type="radio"
                    id="visibility-hidden"
                    name="visibility"
                    value="hidden"
                    checked={formData.visibility === 'hidden'}
                    onChange={(e) => setFormData(prev => ({ ...prev, visibility: e.target.value as 'hidden' | 'internal' | 'public' }))}
                    className="w-4 h-4 text-blue-600 border-gray-300 focus:ring-blue-500"
                  />
                  <label htmlFor="visibility-hidden" className="text-sm font-medium text-gray-700">
                    Hidden - Only visible internally
                  </label>
                </div>
                <div className="flex items-center gap-2">
                  <input
                    type="radio"
                    id="visibility-internal"
                    name="visibility"
                    value="internal"
                    checked={formData.visibility === 'internal'}
                    onChange={(e) => setFormData(prev => ({ ...prev, visibility: e.target.value as 'hidden' | 'internal' | 'public' }))}
                    className="w-4 h-4 text-blue-600 border-gray-300 focus:ring-blue-500"
                  />
                  <label htmlFor="visibility-internal" className="text-sm font-medium text-gray-700">
                    Internal - Visible to company users
                  </label>
                </div>
                <div className="flex items-center gap-2">
                  <input
                    type="radio"
                    id="visibility-public"
                    name="visibility"
                    value="public"
                    checked={formData.visibility === 'public'}
                    onChange={(e) => setFormData(prev => ({ ...prev, visibility: e.target.value as 'hidden' | 'internal' | 'public' }))}
                    className="w-4 h-4 text-blue-600 border-gray-300 focus:ring-blue-500"
                  />
                  <label htmlFor="visibility-public" className="text-sm font-medium text-gray-700">
                    Public - Visible on job board (for candidates)
                  </label>
                </div>
              </div>
            </div>

            {/* Workflow Info (read-only, set from URL parameter) */}
            {loadingWorkflow && (
              <div className="md:col-span-2">
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <p className="text-sm text-gray-700">
                    <span className="font-medium">Opening Flow:</span> Loading workflow...
                  </p>
                </div>
              </div>
            )}
            {currentWorkflow && !loadingWorkflow && (
              <div className="md:col-span-2">
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <p className="text-sm text-gray-700">
                    <span className="font-medium">Opening Flow:</span> {currentWorkflow.name}
                  </p>
                </div>
              </div>
            )}

            {/* Phase 12.8: Phase-Workflow Configuration (Interview Process Flows) */}
            <div className="md:col-span-2">
              <PhaseWorkflowSelector
                companyId={getCompanyId() || ''}
                phaseWorkflows={formData.phase_workflows || {}}
                onChange={(phaseWorkflows) => setFormData(prev => ({ ...prev, phase_workflows: phaseWorkflows }))}
                label="Interview Process Flow Configuration"
              />
            </div>

            {/* Description */}
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Job Description <span className="text-red-500">*</span>
              </label>
              <div className="border border-gray-300 rounded-lg overflow-hidden">
                <WysiwygEditor
                  value={formData.description}
                  onChange={(content) => setFormData(prev => ({ ...prev, description: content }))}
                  placeholder="Describe the role, responsibilities, and what you're looking for. You can use rich text formatting, add images, and create structured content..."
                  height={400}
                  className="w-full"
                />
              </div>
              <p className="mt-2 text-sm text-gray-500">
                Use the toolbar above to format text, add images, create lists, and structure your job description.
              </p>
            </div>
          </div>
        </div>

        {/* Actions */}
        <div className="flex items-center justify-end gap-3">
          <button
            type="button"
            onClick={() => navigate('/company/positions')}
            className="px-6 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={loading || loadingWorkflow || (!formData.job_position_workflow_id && !searchParams.get('workflow_id'))}
            className="flex items-center gap-2 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            title={
              loadingWorkflow 
                ? 'Loading workflow...' 
                : !formData.job_position_workflow_id && !searchParams.get('workflow_id')
                  ? 'Workflow is required' 
                  : loading 
                    ? 'Creating position...' 
                    : ''
            }
          >
            <Save className="w-5 h-5" />
            {loadingWorkflow ? 'Loading workflow...' : loading ? 'Creating...' : 'Create Position'}
          </button>
        </div>
      </form>
    </div>
  );
}
