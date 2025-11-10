import { useState, useEffect, useRef } from 'react';
import { useNavigate, useSearchParams, Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import {
  DndContext,
  DragOverlay,
  PointerSensor,
  useSensor,
  useSensors,
  useDroppable,
} from '@dnd-kit/core';
import type { DragEndEvent, DragStartEvent } from '@dnd-kit/core';
import { SortableContext, verticalListSortingStrategy } from '@dnd-kit/sortable';
import { useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { Kanban, User, AlertCircle, RefreshCw, List, ChevronDown, Move } from 'lucide-react';
import { companyWorkflowService } from '../../services/companyWorkflowService.ts';
import { companyCandidateService } from '../../services/companyCandidateService.ts';
import { phaseService } from '../../services/phaseService.ts';
import type { WorkflowStage } from '../../types/workflow.ts';
import type { CompanyCandidate } from '../../types/companyCandidate.ts';
import type { Phase } from '../../types/phase.ts';
import { getPriorityColor } from '../../types/companyCandidate.ts';
import { RowStageSection } from '../../components/kanban/RowStageSection.tsx';
import { KanbanDisplay } from '../../types/workflow.ts';
import '../../components/kanban/kanban-styles.css';

// Candidate Card Component
function CandidateCard({ 
  candidate, 
  companyId: _companyId, 
  rowStages, 
  onMoveToStage 
}: { 
  candidate: CompanyCandidate; 
  companyId: string;
  rowStages: WorkflowStage[];
  onMoveToStage: (candidateId: string, stageId: string) => void;
}) {
  const navigate = useNavigate();
  const [showDropdown, setShowDropdown] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const { attributes, listeners, setNodeRef, transform, transition, isDragging } = useSortable({
    id: candidate.id,
  });

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setShowDropdown(false);
      }
    };

    if (showDropdown) {
      document.addEventListener('mousedown', handleClickOutside);
      return () => document.removeEventListener('mousedown', handleClickOutside);
    }
  }, [showDropdown]);

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
        {candidate.priority !== 'MEDIUM' && (
          <span
            className={`px-2 py-1 text-xs font-medium rounded-full ${getPriorityColor(
              candidate.priority
            )}`}
          >
            {candidate.priority}
          </span>
        )}
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

      {/* Quick Action Dropdown for Row Stages */}
      {rowStages.length > 0 && (
        <div ref={dropdownRef} className="mt-3 pt-2 border-t border-gray-200 relative">
          <button
            onClick={(e) => {
              e.stopPropagation();
              setShowDropdown(!showDropdown);
            }}
            className="flex items-center gap-2 px-3 py-2 text-xs bg-blue-50 hover:bg-blue-100 text-blue-700 rounded-lg transition-colors w-full justify-center"
          >
            <Move className="w-3 h-3" />
            <span>Move to Stage</span>
            <ChevronDown className="w-3 h-3" />
          </button>
          
          {showDropdown && (
            <div className="absolute top-full left-0 right-0 mt-1 bg-white border border-gray-200 rounded-lg shadow-lg z-10">
              <div className="py-1">
                {rowStages.map((stage) => (
                  <button
                    key={stage.id}
                    onClick={(e) => {
                      e.stopPropagation();
                      onMoveToStage(candidate.id, stage.id);
                      setShowDropdown(false);
                    }}
                    className="flex items-center gap-2 px-3 py-2 text-xs hover:bg-gray-50 w-full text-left"
                  >
                    <span 
                      className="text-sm"
                      dangerouslySetInnerHTML={{ __html: stage.style.icon }}
                    />
                    <span className="text-gray-700">{stage.name}</span>
                  </button>
                ))}
              </div>
            </div>
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
  companyId,
  rowStages,
  onMoveToStage,
}: {
  stage: WorkflowStage;
  candidates: CompanyCandidate[];
  companyId: string;
  rowStages: WorkflowStage[];
  onMoveToStage: (candidateId: string, stageId: string) => void;
}) {
  const { t } = useTranslation();
  const { setNodeRef, isOver } = useDroppable({
    id: stage.id,
  });

  return (
    <div 
      className="rounded-lg p-4 min-w-[300px] max-w-[300px] flex-shrink-0 flex flex-col"
      style={{ 
        backgroundColor: stage.style.background_color,
        color: stage.style.color 
      }}
    >
      {/* Stage Header */}
      <div className="mb-4 flex-shrink-0">
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-2">
            <span 
              className="text-lg"
              dangerouslySetInnerHTML={{ __html: stage.style.icon }}
            />
            <h3 className="font-semibold">{stage.name}</h3>
          </div>
          <span 
            className="px-2 py-1 text-xs font-medium rounded-full"
            style={{ 
              backgroundColor: stage.style.color + '20', // 20% opacity
              color: stage.style.color 
            }}
          >
            {candidates.length}
          </span>
        </div>
        {stage.description && (
          <p className="text-xs opacity-75 line-clamp-2">{stage.description}</p>
        )}
      </div>

      {/* Drop Zone - covers full height */}
      <div 
        ref={setNodeRef} 
        className={`flex-1 min-h-[200px] ${isOver ? 'bg-opacity-20' : ''}`}
        style={isOver ? { backgroundColor: stage.style.color + '20' } : {}}
      >
        <SortableContext items={candidates.map((c) => c.id)} strategy={verticalListSortingStrategy}>
          {candidates.length === 0 ? (
            <div className="text-center py-8 text-gray-400 text-sm">
              {t('company.workflowBoard.dropCandidatesHere')}
            </div>
          ) : (
            candidates.map((candidate) => (
              <CandidateCard 
                key={candidate.id} 
                candidate={candidate} 
                companyId={companyId}
                rowStages={rowStages}
                onMoveToStage={onMoveToStage}
              />
            ))
          )}
        </SortableContext>
      </div>
    </div>
  );
}

// Main Kanban Board Component
export default function WorkflowBoardPage() {
  const { t } = useTranslation();
  const [searchParams] = useSearchParams();
  const phaseIdFromUrl = searchParams.get('phase');
  
  const [selectedPhaseId, setSelectedPhaseId] = useState<string>('');
  const [phase, setPhase] = useState<Phase | null>(null);
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
    if (phaseIdFromUrl) {
      setSelectedPhaseId(phaseIdFromUrl);
      loadStagesAndCandidates();
    }
  }, [phaseIdFromUrl]);


  const loadStagesAndCandidates = async () => {
    try {
      setLoading(true);
      const companyId = getCompanyId();
      if (!companyId || !phaseIdFromUrl) return;

      // Load phase information
      const phaseData = await phaseService.getPhase(companyId, phaseIdFromUrl);
      setPhase(phaseData);

      // Load stages for the selected phase (requires workflow_type from phase)
      if (!phaseData.workflow_type) {
        throw new Error('Phase does not have workflow_type');
      }
      const stagesData = await companyWorkflowService.listStagesByPhase(phaseIdFromUrl, phaseData.workflow_type);
      setStages(stagesData.sort((a, b) => a.order - b.order));

      // Load candidates for the selected phase
      const candidatesData = await companyCandidateService.listByCompany(companyId);
      setCandidates(candidatesData.filter((c) => c.phase_id === phaseIdFromUrl));

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
    const candidate = candidates.find((c) => c.id === newStageId);

    let targetStageId = newStageId;
    if (candidate) {
      // Dropped on another candidate, use that candidate's stage
      targetStageId = candidate.current_stage_id || '';
    }

    // Check if it's a valid stage ID
    const isValidStage = stages.some((s) => s.id === targetStageId);
    if (!targetStageId || !isValidStage) {
      setActiveId(null);
      return;
    }

    // Check if candidate is already in this stage
    const currentCandidate = candidates.find((c) => c.id === candidateId);
    if (currentCandidate?.current_stage_id === targetStageId) {
      setActiveId(null);
      return;
    }

    // Optimistic update: update local state immediately
    setCandidates(prevCandidates =>
      prevCandidates.map(candidate =>
        candidate.id === candidateId
          ? { ...candidate, current_stage_id: targetStageId }
          : candidate
      )
    );
    setActiveId(null);

    // Update candidate stage on backend (fire and forget)
    try {
      await companyCandidateService.changeStage(candidateId, { new_stage_id: targetStageId });
    } catch (err: any) {
      // Revert on error
      setCandidates(prevCandidates =>
        prevCandidates.map(candidate =>
          candidate.id === candidateId
            ? { ...candidate, current_stage_id: currentCandidate?.current_stage_id || '' }
            : candidate
        )
      );
      alert('Failed to move candidate: ' + err.message);
    }
  };

  const getCandidatesByStage = (stageId: string) => {
    return candidates.filter((c) => c.current_stage_id === stageId);
  };

  const moveCandidateToStage = async (candidateId: string, stageId: string) => {
    try {
      await companyCandidateService.changeStage(candidateId, { new_stage_id: stageId });
      
      // Update local state
      setCandidates(prevCandidates =>
        prevCandidates.map(candidate =>
          candidate.id === candidateId
            ? { ...candidate, current_stage_id: stageId }
            : candidate
        )
      );
    } catch (error) {
      console.error('Failed to move candidate:', error);
      setError('Failed to move candidate');
    }
  };

  // Separate stages by kanban_display
  const columnStages = stages.filter(s => s.kanban_display === KanbanDisplay.COLUMN);
  const rowStages = stages.filter(s => s.kanban_display === KanbanDisplay.ROW);

  const activeDragCandidate = candidates.find((c) => c.id === activeId);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!phaseIdFromUrl) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">{t('company.workflowBoard.noPhaseSelected')}</h2>
          <p className="text-gray-600 mb-6">{t('company.workflowBoard.selectPhase')}</p>
          <Link
            to="/company/phases"
            className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            <List className="w-4 h-4 mr-2" />
            Go to Phases
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div>
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">
              {phase ? phase.name : t('company.workflowBoard.title')}
            </h1>
            <p className="text-gray-600 mt-1">{t('company.workflowBoard.dragAndDropDescription')}</p>
          </div>
          <button
            onClick={loadStagesAndCandidates}
            className="flex items-center gap-2 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
          >
            <RefreshCw className="w-4 h-4" />
            {t('company.workflowBoard.refresh')}
          </button>
        </div>

        {/* Back to List View Button */}
        {phaseIdFromUrl && (
          <div className="flex items-center gap-4">
            <Link
              to={`/company/candidates?phase=${phaseIdFromUrl}`}
              className="flex items-center gap-2 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
            >
              <List className="w-4 h-4" />
              {t('company.workflowBoard.listView')}
            </Link>
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
      {!phaseIdFromUrl ? (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-12 text-center">
          <Kanban className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">{t('company.workflowBoard.noPhaseSelected')}</h3>
          <p className="text-gray-600">{t('company.workflowBoard.selectPhaseFromSidebar')}</p>
        </div>
      ) : stages.length === 0 ? (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-12 text-center">
          <Kanban className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">{t('company.workflowBoard.noStagesInPhase')}</h3>
          <p className="text-gray-600">{t('company.workflowBoard.addStagesToPhase')}</p>
        </div>
      ) : (
        <DndContext sensors={sensors} onDragStart={handleDragStart} onDragEnd={handleDragEnd}>
          <SortableContext items={candidates.map(c => c.id)} strategy={verticalListSortingStrategy}>
            <div className="space-y-6">
            {/* Column Stages */}
            {columnStages.length > 0 && (
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 overflow-x-auto">
                <div className="flex gap-4 items-stretch">
                  {columnStages.map((stage) => (
                    <StageColumn
                      key={stage.id}
                      stage={stage}
                      candidates={getCandidatesByStage(stage.id)}
                      companyId={getCompanyId() || ''}
                      rowStages={rowStages}
                      onMoveToStage={moveCandidateToStage}
                    />
                  ))}
                </div>
              </div>
            )}

            {/* Row Stages */}
            {rowStages.length > 0 && (
              <div className="space-y-4">
                {rowStages.map((stage) => (
                  <RowStageSection
                    key={stage.id}
                    stage={stage}
                    candidates={getCandidatesByStage(stage.id)}
                    onCandidateClick={(candidate) => {
                      // Navigate to candidate details
                      window.location.href = `/company/candidates/${candidate.id}`;
                    }}
                  />
                ))}
              </div>
            )}
            </div>
          </SortableContext>

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
      {selectedPhaseId && stages.length > 0 && (
        <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-start gap-3">
            <User className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
            <div>
              <h4 className="font-semibold text-blue-900 text-sm mb-1">
                {t('company.workflowBoard.howToUseTitle')}
              </h4>
              <p className="text-blue-800 text-sm">
                {t('company.workflowBoard.howToUseDescription')}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
