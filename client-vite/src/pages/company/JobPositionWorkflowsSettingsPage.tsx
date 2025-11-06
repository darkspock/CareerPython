import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Plus, Settings, Edit, Briefcase, CheckCircle, Archive } from 'lucide-react';
import { PositionService } from '../../services/positionService.ts';
import type { JobPositionWorkflow } from '../../types/position.ts';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '../../components/ui/tooltip.tsx';

export default function JobPositionWorkflowsSettingsPage() {
  const navigate = useNavigate();
  const [workflows, setWorkflows] = useState<JobPositionWorkflow[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

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
    loadWorkflows();
  }, []);

  const loadWorkflows = async () => {
    try {
      setLoading(true);
      const companyId = getCompanyId();
      if (!companyId) {
        setError('Company ID not found');
        return;
      }

      const data = await PositionService.getWorkflows(companyId);
      
      // Sort workflows: published first, then draft, then deprecated (archived) last
      const sortedWorkflows = data.sort((a, b) => {
        const statusOrder: Record<string, number> = {
          'published': 1,
          'draft': 2,
          'deprecated': 3
        };
        const orderA = statusOrder[a.status] || 999;
        const orderB = statusOrder[b.status] || 999;
        
        if (orderA !== orderB) {
          return orderA - orderB;
        }
        
        // If same status, sort by name
        return a.name.localeCompare(b.name);
      });
      
      setWorkflows(sortedWorkflows);
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to load workflows');
      console.error('Error loading workflows:', err);
    } finally {
      setLoading(false);
    }
  };

  const handlePublish = async (workflow: JobPositionWorkflow) => {
    if (!confirm(`Publish workflow "${workflow.name}"? It will become available for use.`)) return;

    try {
      await PositionService.publishWorkflow(workflow.id, {
        name: workflow.name,
        default_view: workflow.default_view
      });
      loadWorkflows();
    } catch (err: any) {
      alert(`Failed to publish workflow: ${err.message}`);
    }
  };

  const handleArchive = async (workflow: JobPositionWorkflow) => {
    if (!confirm(`Archive workflow "${workflow.name}"? It will no longer be available for new positions.`)) return;

    try {
      await PositionService.archiveWorkflow(workflow.id, {
        name: workflow.name,
        default_view: workflow.default_view
      });
      loadWorkflows();
    } catch (err: any) {
      alert(`Failed to archive workflow: ${err.message}`);
    }
  };

  const handleCreateWorkflow = () => {
    navigate('/company/settings/job-position-workflows/create');
  };

  const handleEditWorkflow = (workflowId: string) => {
    navigate(`/company/settings/job-position-workflows/${workflowId}/edit`);
  };

  const handleConfigureWorkflow = (workflowId: string) => {
    navigate(`/company/settings/job-position-workflows/${workflowId}/configure`);
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'published':
        return (
          <span className="px-2 py-1 text-xs font-medium rounded-full bg-green-100 text-green-800">
            Active
          </span>
        );
      case 'draft':
        return (
          <span className="px-2 py-1 text-xs font-medium rounded-full bg-gray-100 text-gray-800">
            Draft
          </span>
        );
      case 'deprecated':
        return (
          <span className="px-2 py-1 text-xs font-medium rounded-full bg-orange-100 text-orange-800">
            Archived
          </span>
        );
      default:
        return (
          <span className="px-2 py-1 text-xs font-medium rounded-full bg-gray-100 text-gray-800">
            {status}
          </span>
        );
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
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Job Position Workflows</h1>
          <p className="text-gray-600 mt-1">Manage workflows for job positions</p>
        </div>
        <button
          onClick={handleCreateWorkflow}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          <Plus className="w-5 h-5" />
          Create Workflow
        </button>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
          <p className="text-red-800">{error}</p>
        </div>
      )}

      {/* Workflows Grid */}
      {workflows.length === 0 ? (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-12 text-center">
          <Briefcase className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No workflows yet</h3>
          <p className="text-gray-600 mb-4">
            Create your first workflow to manage job positions through stages
          </p>
          <button
            onClick={handleCreateWorkflow}
            className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            <Plus className="w-5 h-5" />
            Create Workflow
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {workflows.map((workflow) => (
            <div
              key={workflow.id}
              className="bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow"
            >
              <div className="p-6">
                {/* Header */}
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">
                      {workflow.name}
                    </h3>
                    <div className="flex items-center gap-2">
                      {getStatusBadge(workflow.status)}
                      <span className="px-2 py-1 text-xs font-medium rounded-full bg-gray-100 text-gray-800">
                        {workflow.default_view}
                      </span>
                    </div>
                  </div>
                </div>

                {/* Stats */}
                <div className="mb-4 py-4 border-t border-b border-gray-200">
                  <div>
                    <p className="text-2xl font-bold text-gray-900">
                      {workflow.stages?.length || 0}
                    </p>
                    <p className="text-sm text-gray-600">Stages</p>
                  </div>
                </div>

                {/* Actions */}
                <TooltipProvider delayDuration={300}>
                  <div className="flex flex-wrap gap-2">
                    {/* Edit button */}
                    <Tooltip>
                      <TooltipTrigger asChild>
                        <button
                          onClick={() => handleEditWorkflow(workflow.id)}
                          className="flex-1 px-3 py-2 text-sm bg-green-50 text-green-700 rounded-lg hover:bg-green-100 transition-colors"
                        >
                          <Edit className="w-4 h-4 mx-auto" />
                        </button>
                      </TooltipTrigger>
                      <TooltipContent>
                        <p>Edit workflow name and stages</p>
                      </TooltipContent>
                    </Tooltip>

                    {/* Configure button */}
                    <Tooltip>
                      <TooltipTrigger asChild>
                        <button
                          onClick={() => handleConfigureWorkflow(workflow.id)}
                          className="flex-1 px-3 py-2 text-sm bg-blue-50 text-blue-700 rounded-lg hover:bg-blue-100 transition-colors"
                        >
                          <Settings className="w-4 h-4 mx-auto" />
                        </button>
                      </TooltipTrigger>
                      <TooltipContent>
                        <p>Configure custom fields</p>
                      </TooltipContent>
                    </Tooltip>

                    {/* Publish button (only if not published) */}
                    {workflow.status !== 'published' && (
                      <Tooltip>
                        <TooltipTrigger asChild>
                          <button
                            onClick={() => handlePublish(workflow)}
                            className="flex-1 px-3 py-2 text-sm bg-emerald-50 text-emerald-700 rounded-lg hover:bg-emerald-100 transition-colors"
                          >
                            <CheckCircle className="w-4 h-4 mx-auto" />
                          </button>
                        </TooltipTrigger>
                        <TooltipContent>
                          <p>Publish workflow</p>
                        </TooltipContent>
                      </Tooltip>
                    )}

                    {/* Archive button (only if published) */}
                    {workflow.status === 'published' && (
                      <Tooltip>
                        <TooltipTrigger asChild>
                          <button
                            onClick={() => handleArchive(workflow)}
                            className="flex-1 px-3 py-2 text-sm bg-orange-50 text-orange-700 rounded-lg hover:bg-orange-100 transition-colors"
                          >
                            <Archive className="w-4 h-4 mx-auto" />
                          </button>
                        </TooltipTrigger>
                        <TooltipContent>
                          <p>Archive workflow (no longer available for new positions)</p>
                        </TooltipContent>
                      </Tooltip>
                    )}
                  </div>
                </TooltipProvider>
              </div>

              {/* Stages Preview */}
              {workflow.stages && workflow.stages.length > 0 && (
                <div className="px-6 py-4 bg-gray-50 border-t border-gray-200">
                  <p className="text-xs font-medium text-gray-500 uppercase mb-2">Stages</p>
                  <div className="flex flex-wrap gap-1">
                    {workflow.stages.slice(0, 3).map((stage) => (
                      <span
                        key={stage.id}
                        className="px-2 py-1 text-xs bg-white border border-gray-200 rounded text-gray-700"
                        style={{
                          backgroundColor: stage.background_color + '20',
                          color: stage.text_color,
                          borderColor: stage.background_color,
                        }}
                      >
                        {stage.name}
                      </span>
                    ))}
                    {workflow.stages.length > 3 && (
                      <span className="px-2 py-1 text-xs bg-white border border-gray-200 rounded text-gray-700">
                        +{workflow.stages.length - 3} more
                      </span>
                    )}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Info Box */}
      <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
        <div className="flex items-start gap-3">
          <Settings className="w-6 h-6 text-blue-600 flex-shrink-0 mt-1" />
          <div>
            <h4 className="font-semibold text-blue-900 mb-1">About Job Position Workflows</h4>
            <p className="text-blue-800 text-sm">
              Workflows help you organize job positions through different stages. You can create custom workflows
              with stages, configure field visibility, and set up validation rules. Each stage maps to a status
              (draft, active, paused, closed, archived) and can have different custom field configurations.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

