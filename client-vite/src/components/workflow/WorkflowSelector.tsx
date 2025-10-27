import React, { useEffect, useState } from 'react';
import { companyWorkflowService } from '../../services/companyWorkflowService';
import type { CompanyWorkflow } from '../../types/workflow';

interface WorkflowSelectorProps {
  companyId: string;
  selectedWorkflowId?: string | null;
  onWorkflowChange: (workflowId: string | null) => void;
  label?: string;
  required?: boolean;
  disabled?: boolean;
  error?: string;
}

export const WorkflowSelector: React.FC<WorkflowSelectorProps> = ({
  companyId,
  selectedWorkflowId,
  onWorkflowChange,
  label = 'Workflow',
  required = false,
  disabled = false,
  error
}) => {
  const [workflows, setWorkflows] = useState<CompanyWorkflow[]>([]);
  const [loading, setLoading] = useState(false);
  const [loadError, setLoadError] = useState<string | null>(null);

  useEffect(() => {
    const loadWorkflows = async () => {
      if (!companyId) return;

      setLoading(true);
      setLoadError(null);

      try {
        const result = await companyWorkflowService.listWorkflowsByCompany(companyId);
        setWorkflows(result);
      } catch (err) {
        console.error('Error loading workflows:', err);
        setLoadError('Failed to load workflows');
      } finally {
        setLoading(false);
      }
    };

    loadWorkflows();
  }, [companyId]);

  const handleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const value = event.target.value;
    onWorkflowChange(value === '' ? null : value);
  };

  return (
    <div className="w-full">
      <label className="block text-sm font-medium text-gray-700 mb-1">
        {label}
        {required && <span className="text-red-500 ml-1">*</span>}
      </label>

      {loadError && (
        <div className="mb-2 text-sm text-red-600">
          {loadError}
        </div>
      )}

      <select
        value={selectedWorkflowId || ''}
        onChange={handleChange}
        disabled={disabled || loading}
        className={`
          w-full px-3 py-2 border rounded-md shadow-sm
          focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500
          ${error ? 'border-red-500' : 'border-gray-300'}
          ${disabled || loading ? 'bg-gray-100 cursor-not-allowed' : 'bg-white'}
        `}
      >
        <option value="">
          {loading ? 'Loading workflows...' : 'No workflow (use default process)'}
        </option>
        {workflows.map((workflow) => (
          <option key={workflow.id} value={workflow.id}>
            {workflow.name}
            {workflow.description && ` - ${workflow.description}`}
          </option>
        ))}
      </select>

      {error && (
        <p className="mt-1 text-sm text-red-600">{error}</p>
      )}

      {!loading && workflows.length === 0 && !loadError && (
        <p className="mt-1 text-sm text-gray-500">
          No workflows available. Create a workflow first to use it for this position.
        </p>
      )}
    </div>
  );
};
