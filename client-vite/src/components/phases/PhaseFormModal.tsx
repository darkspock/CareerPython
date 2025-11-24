import { useState, useEffect } from 'react';
import { X } from 'lucide-react';
import { phaseService } from '../../services/phaseService';
import type { Phase, CreatePhaseRequest, UpdatePhaseRequest } from '../../types/phase';
import { DefaultView, WorkflowType } from '../../types/phase';

interface PhaseFormModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
  companyId: string;
  phase?: Phase | null;
}

export default function PhaseFormModal({
  isOpen,
  onClose,
  onSuccess,
  companyId,
  phase,
}: PhaseFormModalProps) {
  const [name, setName] = useState('');
  const [workflowType, setWorkflowType] = useState<WorkflowType>(WorkflowType.CA);
  const [sortOrder, setSortOrder] = useState(0);
  const [defaultView, setDefaultView] = useState<DefaultView>(DefaultView.KANBAN);
  const [objective, setObjective] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const isEditMode = !!phase;

  useEffect(() => {
    if (isOpen) {
      if (phase) {
        // Edit mode - populate with existing data
        setName(phase.name);
        setWorkflowType(phase.workflow_type as WorkflowType);
        setSortOrder(phase.sort_order);
        setDefaultView(phase.default_view);
        setObjective(phase.objective || '');
      } else {
        // Create mode - reset form
        setName('');
        setWorkflowType(WorkflowType.CA);
        setSortOrder(0);
        setDefaultView(DefaultView.KANBAN);
        setObjective('');
      }
      setError(null);
    }
  }, [isOpen, phase]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!name.trim()) {
      setError('Phase name is required');
      return;
    }

    if (sortOrder < 0) {
      setError('Sort order must be non-negative');
      return;
    }

    try {
      setLoading(true);

      if (isEditMode && phase) {
        // Update existing phase
        const updateData: UpdatePhaseRequest = {
          name,
          sort_order: sortOrder,
          default_view: defaultView,
          objective: objective.trim() || undefined,
        };
        await phaseService.updatePhase(companyId, phase.id, updateData);
      } else {
        // Create new phase
        const createData: CreatePhaseRequest = {
          workflow_type: workflowType,
          name,
          sort_order: sortOrder,
          default_view: defaultView,
          objective: objective.trim() || undefined,
        };
        await phaseService.createPhase(companyId, createData);
      }

      onSuccess();
      onClose();
    } catch (err: any) {
      setError(err.message || `Failed to ${isEditMode ? 'update' : 'create'} phase`);
      console.error(`Error ${isEditMode ? 'updating' : 'creating'} phase:`, err);
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      <div className="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
        {/* Background overlay */}
        <div
          className="fixed inset-0 transition-opacity bg-gray-500 bg-opacity-75"
          onClick={onClose}
        ></div>

        {/* Modal panel */}
        <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <form onSubmit={handleSubmit}>
            <div className="bg-white px-6 py-6">
              {/* Header */}
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-lg font-semibold text-gray-900">
                  {isEditMode ? 'Edit Phase' : 'Create New Phase'}
                </h3>
                <button
                  type="button"
                  onClick={onClose}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              {/* Error Message */}
              {error && (
                <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
                  <p className="text-red-800 text-sm">{error}</p>
                </div>
              )}

              {/* Form Fields */}
              <div className="space-y-4">
                {/* Name */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Phase Name <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    required
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    placeholder="e.g., Sourcing & Screening"
                  />
                </div>

                {/* Workflow Type */}
                {!isEditMode && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Workflow Type <span className="text-red-500">*</span>
                    </label>
                    <select
                      value={workflowType}
                      onChange={(e) => setWorkflowType(e.target.value as WorkflowType)}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    >
                      <option value={WorkflowType.CA}>Candidate Application</option>
                      <option value={WorkflowType.PO}>Job Position Opening</option>
                      <option value={WorkflowType.CO}>Candidate Onboarding</option>
                    </select>
                    <p className="mt-1 text-xs text-gray-500">
                      Select the workflow type this phase belongs to (cannot be changed later)
                    </p>
                  </div>
                )}

                {/* Sort Order */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Sort Order <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="number"
                    required
                    min="0"
                    value={sortOrder}
                    onChange={(e) => setSortOrder(parseInt(e.target.value) || 0)}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    placeholder="0"
                  />
                  <p className="mt-1 text-xs text-gray-500">
                    Order in which phases appear in the workflow (lower numbers first)
                  </p>
                </div>

                {/* Default View */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Default View <span className="text-red-500">*</span>
                  </label>
                  <select
                    value={defaultView}
                    onChange={(e) => setDefaultView(e.target.value as DefaultView)}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value="KANBAN">Kanban</option>
                    <option value="LIST">List</option>
                  </select>
                  <p className="mt-1 text-xs text-gray-500">
                    Default view for workflows in this phase
                  </p>
                </div>

                {/* Objective */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Objective
                  </label>
                  <textarea
                    value={objective}
                    onChange={(e) => setObjective(e.target.value)}
                    rows={3}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    placeholder="Describe the objective of this phase..."
                  />
                  <p className="mt-1 text-xs text-gray-500">
                    Optional description of what this phase aims to achieve
                  </p>
                </div>
              </div>
            </div>

            {/* Footer Actions */}
            <div className="bg-gray-50 px-6 py-4 flex items-center justify-end gap-3">
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={loading}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? (isEditMode ? 'Updating...' : 'Creating...') : (isEditMode ? 'Update Phase' : 'Create Phase')}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
