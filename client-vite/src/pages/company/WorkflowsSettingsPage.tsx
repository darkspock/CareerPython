import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Plus, Settings, Archive, Trash2, Star, CheckCircle } from 'lucide-react';
import { companyWorkflowService } from '../../services/companyWorkflowService';
import type { CompanyWorkflow } from '../../types/workflow';
import { getWorkflowStatusColor } from '../../types/workflow';

export default function WorkflowsSettingsPage() {
  const navigate = useNavigate();
  const [workflows, setWorkflows] = useState<CompanyWorkflow[]>([]);
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

      const data = await companyWorkflowService.listWorkflowsByCompany(companyId);
      setWorkflows(data);
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to load workflows');
      console.error('Error loading workflows:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSetDefault = async (workflowId: string) => {
    try {
      await companyWorkflowService.setAsDefault(workflowId);
      loadWorkflows();
    } catch (err: any) {
      alert('Failed to set default workflow: ' + err.message);
    }
  };

  const handleDeactivate = async (workflowId: string) => {
    if (!confirm('Are you sure you want to deactivate this workflow?')) return;

    try {
      await companyWorkflowService.deactivateWorkflow(workflowId);
      loadWorkflows();
    } catch (err: any) {
      alert('Failed to deactivate workflow: ' + err.message);
    }
  };

  const handleArchive = async (workflowId: string) => {
    if (!confirm('Are you sure you want to archive this workflow?')) return;

    try {
      await companyWorkflowService.archiveWorkflow(workflowId);
      loadWorkflows();
    } catch (err: any) {
      alert('Failed to archive workflow: ' + err.message);
    }
  };

  const handleDelete = async (workflowId: string) => {
    if (!confirm('Are you sure you want to delete this workflow? This action cannot be undone.')) return;

    try {
      await companyWorkflowService.deleteWorkflow(workflowId);
      loadWorkflows();
    } catch (err: any) {
      alert('Failed to delete workflow: ' + err.message);
    }
  };

  const handleCreateWorkflow = () => {
    navigate('/company/workflows/create');
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
          <h1 className="text-2xl font-bold text-gray-900">Workflow Settings</h1>
          <p className="text-gray-600 mt-1">Manage your recruitment workflows and stages</p>
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
          <Settings className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No workflows yet</h3>
          <p className="text-gray-600 mb-4">
            Create your first workflow to organize your recruitment process
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
                    <div className="flex items-center gap-2 mb-2">
                      <h3 className="text-lg font-semibold text-gray-900">
                        {workflow.name}
                      </h3>
                      {workflow.is_default && (
                        <Star className="w-5 h-5 text-yellow-500 fill-yellow-500" />
                      )}
                    </div>
                    <span
                      className={`inline-block px-2 py-1 text-xs font-medium rounded-full ${getWorkflowStatusColor(
                        workflow.status
                      )}`}
                    >
                      {workflow.status}
                    </span>
                  </div>
                </div>

                {/* Description */}
                {workflow.description && (
                  <p className="text-sm text-gray-600 mb-4 line-clamp-2">
                    {workflow.description}
                  </p>
                )}

                {/* Stats */}
                <div className="grid grid-cols-2 gap-4 mb-4 py-4 border-t border-b border-gray-200">
                  <div>
                    <p className="text-2xl font-bold text-gray-900">
                      {workflow.stages?.length || 0}
                    </p>
                    <p className="text-sm text-gray-600">Stages</p>
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-gray-900">
                      {workflow.candidate_count || 0}
                    </p>
                    <p className="text-sm text-gray-600">Candidates</p>
                  </div>
                </div>

                {/* Actions */}
                <div className="flex flex-wrap gap-2">
                  {!workflow.is_default && workflow.status === 'ACTIVE' && (
                    <button
                      onClick={() => handleSetDefault(workflow.id)}
                      className="flex-1 px-3 py-2 text-sm bg-yellow-50 text-yellow-700 rounded-lg hover:bg-yellow-100 transition-colors"
                      title="Set as default"
                    >
                      <Star className="w-4 h-4 mx-auto" />
                    </button>
                  )}
                  {workflow.status === 'ACTIVE' && (
                    <button
                      onClick={() => handleDeactivate(workflow.id)}
                      className="flex-1 px-3 py-2 text-sm bg-gray-50 text-gray-700 rounded-lg hover:bg-gray-100 transition-colors"
                      title="Deactivate"
                    >
                      Deactivate
                    </button>
                  )}
                  {workflow.status === 'INACTIVE' && (
                    <button
                      onClick={() => handleArchive(workflow.id)}
                      className="flex-1 px-3 py-2 text-sm bg-orange-50 text-orange-700 rounded-lg hover:bg-orange-100 transition-colors"
                      title="Archive"
                    >
                      <Archive className="w-4 h-4 mx-auto" />
                    </button>
                  )}
                  {workflow.status === 'ARCHIVED' && (
                    <button
                      onClick={() => handleDelete(workflow.id)}
                      className="flex-1 px-3 py-2 text-sm bg-red-50 text-red-700 rounded-lg hover:bg-red-100 transition-colors"
                      title="Delete"
                    >
                      <Trash2 className="w-4 h-4 mx-auto" />
                    </button>
                  )}
                </div>
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
          <CheckCircle className="w-6 h-6 text-blue-600 flex-shrink-0 mt-1" />
          <div>
            <h4 className="font-semibold text-blue-900 mb-1">About Workflows</h4>
            <p className="text-blue-800 text-sm">
              Workflows help you organize your recruitment process into stages. Each workflow
              can have multiple stages, and you can assign candidates to workflows to track
              their progress through your hiring pipeline. Set one workflow as default to
              automatically assign new candidates to it.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
