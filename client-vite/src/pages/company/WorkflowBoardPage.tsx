import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  DndContext,
  DragOverlay,
  PointerSensor,
  useSensor,
  useSensors,
} from '@dnd-kit/core';
import type { DragEndEvent, DragStartEvent } from '@dnd-kit/core';
import { SortableContext, verticalListSortingStrategy } from '@dnd-kit/sortable';
import { useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { Kanban, User, Tag, AlertCircle, RefreshCw } from 'lucide-react';
import { companyWorkflowService } from '../../services/companyWorkflowService';
import { companyCandidateService } from '../../services/companyCandidateService';
import type { CompanyWorkflow, WorkflowStage } from '../../types/workflow';
import type { CompanyCandidate } from '../../types/companyCandidate';
import { getPriorityColor } from '../../types/companyCandidate';

// Candidate Card Component
function CandidateCard({ candidate }: { candidate: CompanyCandidate }) {
  const navigate = useNavigate();
  const { attributes, listeners, setNodeRef, transform, transition, isDragging } = useSortable({
    id: candidate.id,
  });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1,
  };

  return (
    <div
      ref={setNodeRef}
      style={style}
      {...attributes}
      {...listeners}
      className="bg-white rounded-lg border border-gray-200 p-4 mb-3 cursor-move hover:shadow-md transition-shadow"
      onClick={(e) => {
        if (!isDragging) {
          e.stopPropagation();
          navigate(`/company/candidates/${candidate.id}`);
        }
      }}
    >
      <div className="flex items-start justify-between mb-2">
        <div className="flex-1">
          <h4 className="font-medium text-gray-900 text-sm mb-1">
            {candidate.candidate_name || 'N/A'}
          </h4>
          <p className="text-xs text-gray-500">{candidate.candidate_email || 'N/A'}</p>
        </div>
        <span
          className={`px-2 py-1 text-xs font-medium rounded-full ${getPriorityColor(
            candidate.priority
          )}`}
        >
          {candidate.priority}
        </span>
      </div>

      {/* Tags */}
      {candidate.tags.length > 0 && (
        <div className="flex flex-wrap gap-1 mt-2">
          {candidate.tags.slice(0, 2).map((tag, idx) => (
            <span
              key={idx}
              className="px-2 py-0.5 text-xs bg-gray-100 text-gray-700 rounded-full"
            >
              {tag}
            </span>
          ))}
          {candidate.tags.length > 2 && (
            <span className="px-2 py-0.5 text-xs bg-gray-100 text-gray-700 rounded-full">
              +{candidate.tags.length - 2}
            </span>
          )}
        </div>
      )}
    </div>
  );
}

// Stage Column Component
function StageColumn({
  stage,
  candidates,
}: {
  stage: WorkflowStage;
  candidates: CompanyCandidate[];
}) {
  const { setNodeRef } = useSortable({ id: stage.id });

  return (
    <div className="bg-gray-50 rounded-lg p-4 min-w-[300px] max-w-[300px] flex-shrink-0">
      {/* Stage Header */}
      <div className="mb-4">
        <div className="flex items-center justify-between mb-2">
          <h3 className="font-semibold text-gray-900">{stage.name}</h3>
          <span className="px-2 py-1 text-xs font-medium bg-gray-200 text-gray-700 rounded-full">
            {candidates.length}
          </span>
        </div>
        {stage.description && (
          <p className="text-xs text-gray-600 line-clamp-2">{stage.description}</p>
        )}
      </div>

      {/* Drop Zone */}
      <div ref={setNodeRef} className="min-h-[200px]">
        <SortableContext items={candidates.map((c) => c.id)} strategy={verticalListSortingStrategy}>
          {candidates.length === 0 ? (
            <div className="text-center py-8 text-gray-400 text-sm">
              Drop candidates here
            </div>
          ) : (
            candidates.map((candidate) => (
              <CandidateCard key={candidate.id} candidate={candidate} />
            ))
          )}
        </SortableContext>
      </div>
    </div>
  );
}

// Main Kanban Board Component
export default function WorkflowBoardPage() {
  const [workflows, setWorkflows] = useState<CompanyWorkflow[]>([]);
  const [selectedWorkflowId, setSelectedWorkflowId] = useState<string>('');
  const [stages, setStages] = useState<WorkflowStage[]>([]);
  const [candidates, setCandidates] = useState<CompanyCandidate[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeId, setActiveId] = useState<string | null>(null);

  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 8,
      },
    })
  );

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

  useEffect(() => {
    if (selectedWorkflowId) {
      loadStagesAndCandidates();
    }
  }, [selectedWorkflowId]);

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

      // Select first active workflow by default
      const activeWorkflow = data.find((w) => w.status === 'ACTIVE');
      if (activeWorkflow) {
        setSelectedWorkflowId(activeWorkflow.id);
      }

      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to load workflows');
      console.error('Error loading workflows:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadStagesAndCandidates = async () => {
    try {
      setLoading(true);
      const companyId = getCompanyId();
      if (!companyId) return;

      // Load stages
      const stagesData = await companyWorkflowService.listStagesByWorkflow(selectedWorkflowId);
      setStages(stagesData.sort((a, b) => a.order - b.order));

      // Load candidates
      const candidatesData = await companyCandidateService.listByCompany(companyId);
      setCandidates(candidatesData.filter((c) => c.current_workflow_id === selectedWorkflowId));

      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to load data');
      console.error('Error loading stages and candidates:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDragStart = (event: DragStartEvent) => {
    setActiveId(event.active.id as string);
  };

  const handleDragEnd = async (event: DragEndEvent) => {
    const { active, over } = event;

    if (!over) {
      setActiveId(null);
      return;
    }

    const candidateId = active.id as string;
    const newStageId = over.id as string;

    // Find if over is a stage or another candidate
    const stage = stages.find((s) => s.id === newStageId);
    const candidate = candidates.find((c) => c.id === newStageId);

    let targetStageId = newStageId;
    if (candidate) {
      // Dropped on another candidate, use that candidate's stage
      targetStageId = candidate.current_stage_id || '';
    }

    if (!targetStageId) {
      setActiveId(null);
      return;
    }

    // Update candidate stage
    try {
      await companyCandidateService.changeStage(candidateId, { stage_id: targetStageId });

      // Refresh data
      loadStagesAndCandidates();
    } catch (err: any) {
      alert('Failed to move candidate: ' + err.message);
    } finally {
      setActiveId(null);
    }
  };

  const getCandidatesByStage = (stageId: string) => {
    return candidates.filter((c) => c.current_stage_id === stageId);
  };

  const activeDragCandidate = candidates.find((c) => c.id === activeId);

  if (loading && workflows.length === 0) {
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
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Workflow Board</h1>
            <p className="text-gray-600 mt-1">Drag and drop candidates through stages</p>
          </div>
          <button
            onClick={loadStagesAndCandidates}
            className="flex items-center gap-2 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
          >
            <RefreshCw className="w-4 h-4" />
            Refresh
          </button>
        </div>

        {/* Workflow Selector */}
        {workflows.length > 0 && (
          <div className="flex items-center gap-4">
            <label className="text-sm font-medium text-gray-700">Workflow:</label>
            <select
              value={selectedWorkflowId}
              onChange={(e) => setSelectedWorkflowId(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="">Select a workflow</option>
              {workflows
                .filter((w) => w.status === 'ACTIVE')
                .map((workflow) => (
                  <option key={workflow.id} value={workflow.id}>
                    {workflow.name}
                  </option>
                ))}
            </select>
          </div>
        )}
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
          <div className="flex items-center gap-2">
            <AlertCircle className="w-5 h-5 text-red-600" />
            <p className="text-red-800">{error}</p>
          </div>
        </div>
      )}

      {/* Kanban Board */}
      {!selectedWorkflowId ? (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-12 text-center">
          <Kanban className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No workflow selected</h3>
          <p className="text-gray-600">Select a workflow to view the Kanban board</p>
        </div>
      ) : stages.length === 0 ? (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-12 text-center">
          <Kanban className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No stages in this workflow</h3>
          <p className="text-gray-600">Add stages to this workflow in the Settings page</p>
        </div>
      ) : (
        <DndContext sensors={sensors} onDragStart={handleDragStart} onDragEnd={handleDragEnd}>
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 overflow-x-auto">
            <div className="flex gap-4">
              {stages.map((stage) => (
                <StageColumn
                  key={stage.id}
                  stage={stage}
                  candidates={getCandidatesByStage(stage.id)}
                />
              ))}
            </div>
          </div>

          {/* Drag Overlay */}
          <DragOverlay>
            {activeId && activeDragCandidate ? (
              <div className="bg-white rounded-lg border-2 border-blue-500 p-4 shadow-lg opacity-90">
                <h4 className="font-medium text-gray-900 text-sm">
                  {activeDragCandidate.candidate_name}
                </h4>
                <p className="text-xs text-gray-500">{activeDragCandidate.candidate_email}</p>
              </div>
            ) : null}
          </DragOverlay>
        </DndContext>
      )}

      {/* Instructions */}
      {selectedWorkflowId && stages.length > 0 && (
        <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-start gap-3">
            <User className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
            <div>
              <h4 className="font-semibold text-blue-900 text-sm mb-1">
                How to use the Kanban Board
              </h4>
              <p className="text-blue-800 text-sm">
                Drag and drop candidate cards between columns to move them through your
                workflow stages. Click on a candidate card to view their full details.
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
