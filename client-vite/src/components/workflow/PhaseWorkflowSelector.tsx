/**
 * PhaseWorkflowSelector Component
 * Phase 12.8: Allow positions to configure workflows for each recruitment phase
 *
 * According to WORKFLOW3.md:
 * - Show all phases and let user select workflow for each phase
 * - Auto-select if only one active workflow for that phase
 * - Hide configuration UI if only one active workflow exists per phase
 */

import { useEffect, useState } from 'react';
import { Workflow, AlertCircle, ChevronDown, ChevronUp } from 'lucide-react';
import { phaseService } from '../../services/phaseService';
import { workflowService } from '../../services/workflowService';
import type { Phase } from '../../types/phase';
import type { CompanyWorkflow } from '../../types/workflow';

interface PhaseWorkflowSelectorProps {
  companyId: string;
  phaseWorkflows: Record<string, string>;  // phase_id -> workflow_id
  onChange: (phaseWorkflows: Record<string, string>) => void;
  label?: string;
}

export function PhaseWorkflowSelector({
  companyId,
  phaseWorkflows,
  onChange,
  label = "Recruitment Workflow Configuration"
}: PhaseWorkflowSelectorProps) {
  const [phases, setPhases] = useState<Phase[]>([]);
  const [workflowsByPhase, setWorkflowsByPhase] = useState<Record<string, CompanyWorkflow[]>>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isExpanded, setIsExpanded] = useState(false);

  // Check if configuration UI should be hidden (only one workflow per phase)
  const [shouldHideUI, setShouldHideUI] = useState(false);

  useEffect(() => {
    if (!companyId) return;

    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);

        // Fetch all phases for the company
        const fetchedPhases = await phaseService.listPhases(companyId);
        setPhases(fetchedPhases);

        // Fetch workflows grouped by phase
        const workflowsMap: Record<string, CompanyWorkflow[]> = {};
        const newPhaseWorkflows: Record<string, string> = { ...phaseWorkflows };
        let allPhasesHaveOnlyOneWorkflow = true;

        for (const phase of fetchedPhases) {
          // Fetch active workflows for this phase
          const workflows = await workflowService.listWorkflows(companyId, {
            phase_id: phase.id,
            status: 'active'
          });

          workflowsMap[phase.id] = workflows;

          // Auto-select if only one workflow
          if (workflows.length === 1) {
            newPhaseWorkflows[phase.id] = workflows[0].id;
          } else if (workflows.length > 1) {
            allPhasesHaveOnlyOneWorkflow = false;
          }
        }

        setWorkflowsByPhase(workflowsMap);

        // If all phases have exactly one workflow, hide the UI
        setShouldHideUI(allPhasesHaveOnlyOneWorkflow);

        // Update parent component with auto-selected workflows
        onChange(newPhaseWorkflows);

      } catch (err) {
        console.error('Error fetching phases/workflows:', err);
        setError('Failed to load phase and workflow data');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [companyId]);

  const handleWorkflowChange = (phaseId: string, workflowId: string) => {
    const updated = { ...phaseWorkflows, [phaseId]: workflowId };
    onChange(updated);
  };

  if (loading) {
    return (
      <div className="border border-gray-200 rounded-lg p-4">
        <div className="flex items-center gap-2 text-gray-500">
          <Workflow className="w-5 h-5 animate-spin" />
          <span>Loading workflow configuration...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="border border-red-200 bg-red-50 rounded-lg p-4">
        <div className="flex items-center gap-2 text-red-700">
          <AlertCircle className="w-5 h-5" />
          <span>{error}</span>
        </div>
      </div>
    );
  }

  if (phases.length === 0) {
    return (
      <div className="border border-yellow-200 bg-yellow-50 rounded-lg p-4">
        <div className="flex items-center gap-2 text-yellow-700">
          <AlertCircle className="w-5 h-5" />
          <span>No recruitment phases configured. Please set up phases in company settings.</span>
        </div>
      </div>
    );
  }

  // If all phases have only one workflow, hide the configuration UI
  if (shouldHideUI) {
    return (
      <div className="border border-green-100 bg-green-50 rounded-lg p-4">
        <div className="flex items-center gap-2 text-green-700">
          <Workflow className="w-5 h-5" />
          <span>Workflow configuration automatically set (one workflow per phase)</span>
        </div>
      </div>
    );
  }

  return (
    <div className="border border-gray-200 rounded-lg">
      {/* Header */}
      <button
        type="button"
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full flex items-center justify-between p-4 hover:bg-gray-50 transition-colors"
      >
        <div className="flex items-center gap-2">
          <Workflow className="w-5 h-5 text-gray-700" />
          <span className="font-medium text-gray-900">{label}</span>
        </div>
        {isExpanded ? (
          <ChevronUp className="w-5 h-5 text-gray-500" />
        ) : (
          <ChevronDown className="w-5 h-5 text-gray-500" />
        )}
      </button>

      {/* Content */}
      {isExpanded && (
        <div className="border-t border-gray-200 p-4 space-y-4">
          <p className="text-sm text-gray-600 mb-4">
            Configure which workflow to use for each recruitment phase. Each phase represents a major
            stage in your recruitment process.
          </p>

          {phases.map((phase) => {
            const workflows = workflowsByPhase[phase.id] || [];
            const selectedWorkflowId = phaseWorkflows[phase.id];
            const hasMultipleOptions = workflows.length > 1;

            return (
              <div key={phase.id} className="border border-gray-100 rounded-lg p-4 bg-gray-50">
                <div className="flex items-start gap-3">
                  <div className="flex-1">
                    <label className="block text-sm font-medium text-gray-900 mb-1">
                      {phase.name}
                      {!hasMultipleOptions && (
                        <span className="ml-2 text-xs text-gray-500">(Auto-selected)</span>
                      )}
                    </label>
                    {phase.objective && (
                      <p className="text-xs text-gray-500 mb-3">{phase.objective}</p>
                    )}

                    {workflows.length === 0 ? (
                      <div className="text-sm text-red-600">
                        No active workflows configured for this phase
                      </div>
                    ) : workflows.length === 1 ? (
                      <div className="text-sm text-gray-700 bg-white border border-gray-200 rounded px-3 py-2">
                        {workflows[0].name}
                      </div>
                    ) : (
                      <select
                        value={selectedWorkflowId || ''}
                        onChange={(e) => handleWorkflowChange(phase.id, e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      >
                        <option value="">Select a workflow...</option>
                        {workflows.map((workflow) => (
                          <option key={workflow.id} value={workflow.id}>
                            {workflow.name}
                          </option>
                        ))}
                      </select>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
