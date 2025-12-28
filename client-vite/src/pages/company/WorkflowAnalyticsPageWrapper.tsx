/**
 * Workflow Analytics Page Wrapper
 * Shows a workflow selector and displays analytics for the selected workflow
 */

import { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useCompanyNavigation } from '../../hooks/useCompanyNavigation';
import { BarChart2 } from 'lucide-react';
import { WorkflowAnalyticsPage } from '../../components/company/workflowAnalytics/WorkflowAnalyticsPage';
import { workflowService } from '../../services/workflowService';
import type { CandidateApplicationWorkflow } from '../../types/workflow';

function getCompanyId(): string | null {
  const token = localStorage.getItem('access_token');
  if (!token) return null;
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    return payload.company_id;
  } catch {
    return null;
  }
}

export default function WorkflowAnalyticsPageWrapper() {
  const navigate = useNavigate();
  const { getPath } = useCompanyNavigation();
  const [searchParams, setSearchParams] = useSearchParams();
  const [workflows, setWorkflows] = useState<CandidateApplicationWorkflow[]>([]);
  const [selectedWorkflowId, setSelectedWorkflowId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const companyId = getCompanyId();

  useEffect(() => {
    loadWorkflows();
  }, [companyId]);

  useEffect(() => {
    // Get workflow ID from URL params or select first workflow
    const workflowId = searchParams.get('workflow');
    if (workflowId) {
      setSelectedWorkflowId(workflowId);
    } else if (workflows.length > 0 && !selectedWorkflowId) {
      setSelectedWorkflowId(workflows[0].id);
    }
  }, [searchParams, workflows]);

  const loadWorkflows = async () => {
    if (!companyId) return;

    try {
      setIsLoading(true);
      setError(null);
      const data = await workflowService.listWorkflows(companyId, { status: 'active' });
      setWorkflows(data);
    } catch (err) {
      setError('Failed to load workflows');
      console.error('Error loading workflows:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleWorkflowChange = (workflowId: string) => {
    setSelectedWorkflowId(workflowId);
    setSearchParams({ workflow: workflowId });
  };

  if (!companyId) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <p className="text-red-600 font-medium">Company not found</p>
          <button
            onClick={() => navigate('/company/login')}
            className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Go to Login
          </button>
        </div>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading workflows...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <p className="text-red-600 font-medium">{error}</p>
          <button
            onClick={loadWorkflows}
            className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  if (workflows.length === 0) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <div className="text-center py-12 bg-white rounded-lg border border-gray-200">
          <BarChart2 className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-900 mb-2">No Workflows Available</h2>
          <p className="text-gray-600 mb-4">
            Create a workflow first to view analytics.
          </p>
          <button
            onClick={() => navigate(getPath('settings/hiring-pipelines'))}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Go to Hiring Pipelines
          </button>
        </div>
      </div>
    );
  }

  const selectedWorkflow = workflows.find(w => w.id === selectedWorkflowId);

  return (
    <div className="max-w-7xl mx-auto">
      {/* Workflow Selector */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-6">
        <div className="flex items-center gap-4">
          <label className="text-sm font-medium text-gray-700">Select Workflow:</label>
          <select
            value={selectedWorkflowId || ''}
            onChange={(e) => handleWorkflowChange(e.target.value)}
            className="flex-1 max-w-md px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            {workflows.map((workflow) => (
              <option key={workflow.id} value={workflow.id}>
                {workflow.name}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Analytics Component */}
      {selectedWorkflowId && (
        <WorkflowAnalyticsPage
          workflowId={selectedWorkflowId}
          workflowName={selectedWorkflow?.name}
        />
      )}
    </div>
  );
}
