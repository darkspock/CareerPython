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
import { Kanban, User, AlertCircle, RefreshCw, List, ChevronDown, Move, Plus } from 'lucide-react';
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
  allStages,
  onMoveToStage 
}: { 
  candidate: CompanyCandidate; 
  companyId: string;
  allStages: WorkflowStage[];
  onMoveToStage: (candidateId: string, stageId: string) => void;
}) {
  const { t } = useTranslation();
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

      {/* Quick Action Dropdown for Move to Stage */}
      {(() => {
        // Get current stage
        const currentStage = candidate.current_stage_id 
          ? allStages.find(s => s.id === candidate.current_stage_id)
          : null;
        
        // Get next stage (next in order)
        const nextStage = currentStage 
          ? allStages
              .filter(s => s.order > currentStage.order && s.is_active)
              .sort((a, b) => a.order - b.order)[0]
          : null;
        
        // Get stages that are ROW or HIDDEN/NONE (not visible in columns)
        const hiddenOrRowStages = allStages.filter(s => 
          s.is_active && 
          s.id !== candidate.current_stage_id &&
          (s.kanban_display === KanbanDisplay.ROW || s.kanban_display === KanbanDisplay.NONE)
        );
        
        // Combine next stage and hidden/row stages, removing duplicates
        const availableStages = [
          ...(nextStage ? [nextStage] : []),
          ...hiddenOrRowStages.filter(s => !nextStage || s.id !== nextStage.id)
        ].sort((a, b) => a.order - b.order);
        
        if (availableStages.length === 0) return null;
        
        return (
          <div ref={dropdownRef} className="mt-3 pt-2 border-t border-gray-200 relative">
            <button
              onClick={(e) => {
                e.stopPropagation();
                setShowDropdown(!showDropdown);
              }}
              className="flex items-center gap-2 px-3 py-2 text-xs bg-blue-50 hover:bg-blue-100 text-blue-700 rounded-lg transition-colors w-full justify-center"
            >
              <Move className="w-3 h-3" />
              <span>{t('company.workflowBoard.moveToStage')}</span>
              <ChevronDown className="w-3 h-3" />
            </button>
            
            {showDropdown && (
              <div className="absolute top-full left-0 right-0 mt-1 bg-white border border-gray-200 rounded-lg shadow-lg z-10">
                <div className="py-1">
                  {availableStages.map((stage) => (
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
                      <span className="text-gray-700">
                        {stage.name}
                        {nextStage && stage.id === nextStage.id && (
                          <span className="ml-2 text-blue-600 text-xs">({t('company.workflowBoard.nextStage')})</span>
                        )}
                      </span>
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
        );
      })()}
    </div>
  );
}

// Stage Column Component
function StageColumn({
  stage,
  candidates,
  companyId,
  allStages,
  onMoveToStage,
}: {
  stage: WorkflowStage;
  candidates: CompanyCandidate[];
  companyId: string;
  allStages: WorkflowStage[];
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
                allStages={allStages}
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
  const [allPhases, setAllPhases] = useState<Phase[]>([]);
  const [stages, setStages] = useState<WorkflowStage[]>([]);
  const [candidates, setCandidates] = useState<CompanyCandidate[]>([]);
  const [nextPhaseCandidates, setNextPhaseCandidates] = useState<Map<string, CompanyCandidate[]>>(new Map()); // Map: next_phase_id -> candidates in initial stage
  const [nextPhaseInitialStages, setNextPhaseInitialStages] = useState<Map<string, string>>(new Map()); // Map: next_phase_id -> initial_stage_id
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
      loadPhases();
      loadStagesAndCandidates();
    }
  }, [phaseIdFromUrl]);

  const loadPhases = async () => {
    try {
      const companyId = getCompanyId();
      if (!companyId) return;

      const phasesData = await phaseService.listPhases(companyId);
      // Filter by CANDIDATE_APPLICATION type and sort by sort_order
      const candidatePhases = phasesData
        .filter(p => p.workflow_type === 'CA')
        .sort((a, b) => a.sort_order - b.sort_order);
      setAllPhases(candidatePhases);
    } catch (err) {
      console.error('Failed to load phases:', err);
    }
  };


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

      // Load candidates from next phases for SUCCESS stages
      const nextPhaseCandidatesMap = new Map<string, CompanyCandidate[]>();
      const nextPhaseInitialStagesMap = new Map<string, string>();
      
      // Find SUCCESS stages with next_phase_id
      const successStages = stagesData.filter(s => s.stage_type === 'success' && s.next_phase_id);
      
      for (const successStage of successStages) {
        if (!successStage.next_phase_id) continue;
        
        try {
          // Load stages for the next phase
          const nextPhaseData = await phaseService.getPhase(companyId, successStage.next_phase_id);
          if (!nextPhaseData.workflow_type) continue;
          
          const nextPhaseStages = await companyWorkflowService.listStagesByPhase(successStage.next_phase_id, nextPhaseData.workflow_type);
          
          // Find the initial stage
          const initialStage = nextPhaseStages.find(s => s.stage_type === 'initial');
          if (!initialStage) continue;
          
          nextPhaseInitialStagesMap.set(successStage.next_phase_id, initialStage.id);
          
          // Load candidates in the initial stage of the next phase
          const nextPhaseCandidatesList = candidatesData.filter(
            (c) => c.phase_id === successStage.next_phase_id && c.current_stage_id === initialStage.id
          );
          
          nextPhaseCandidatesMap.set(successStage.next_phase_id, nextPhaseCandidatesList);
        } catch (err) {
          console.error(`Error loading next phase data for phase ${successStage.next_phase_id}:`, err);
        }
      }
      
      setNextPhaseCandidates(nextPhaseCandidatesMap);
      setNextPhaseInitialStages(nextPhaseInitialStagesMap);

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

    // Find candidate in current phase or next phase candidates
    let currentCandidate = candidates.find((c) => c.id === candidateId);
    if (!currentCandidate) {
      // Candidate might be from next phase, search in nextPhaseCandidates
      for (const nextPhaseCandidatesList of nextPhaseCandidates.values()) {
        currentCandidate = nextPhaseCandidatesList.find((c) => c.id === candidateId);
        if (currentCandidate) break;
      }
    }

    // Find if over is a stage or another candidate
    let targetCandidate = candidates.find((c) => c.id === newStageId);
    if (!targetCandidate) {
      // Candidate might be from next phase, search in nextPhaseCandidates
      for (const nextPhaseCandidatesList of nextPhaseCandidates.values()) {
        targetCandidate = nextPhaseCandidatesList.find((c) => c.id === newStageId);
        if (targetCandidate) break;
      }
    }

    let targetStageId = newStageId;
    if (targetCandidate) {
      // Dropped on another candidate, use that candidate's stage
      targetStageId = targetCandidate.current_stage_id || '';
    }

    // Check if it's a valid stage ID
    const isValidStage = stages.some((s) => s.id === targetStageId);
    if (!targetStageId || !isValidStage) {
      setActiveId(null);
      return;
    }

    // Check if candidate is already in this stage
    if (currentCandidate?.current_stage_id === targetStageId) {
      setActiveId(null);
      return;
    }

    // Optimistic update: update local state immediately
    if (currentCandidate) {
      setCandidates(prevCandidates =>
        prevCandidates.map(candidate =>
          candidate.id === candidateId
            ? { ...candidate, current_stage_id: targetStageId, phase_id: phaseIdFromUrl || candidate.phase_id }
            : candidate
        )
      );
      // Also update in nextPhaseCandidates if it was there
      setNextPhaseCandidates(prevMap => {
        const newMap = new Map(prevMap);
        for (const [phaseId, candidatesList] of newMap.entries()) {
          const updatedList = candidatesList.map(c =>
            c.id === candidateId
              ? { ...c, current_stage_id: targetStageId, phase_id: phaseIdFromUrl || c.phase_id }
              : c
          );
          newMap.set(phaseId, updatedList);
        }
        return newMap;
      });
    }
    setActiveId(null);

    // Update candidate stage on backend (fire and forget)
    try {
      await companyCandidateService.changeStage(candidateId, { new_stage_id: targetStageId });
      // Reload data to get updated phase assignments and next phase candidates
      await loadStagesAndCandidates();
    } catch (err: any) {
      // Revert on error
      if (currentCandidate) {
        setCandidates(prevCandidates =>
          prevCandidates.map(candidate =>
            candidate.id === candidateId
              ? { ...candidate, current_stage_id: currentCandidate.current_stage_id || '', phase_id: currentCandidate.phase_id }
              : candidate
          )
        );
        // Also revert in nextPhaseCandidates if it was there
        setNextPhaseCandidates(prevMap => {
          const newMap = new Map(prevMap);
          for (const [phaseId, candidatesList] of newMap.entries()) {
            const updatedList = candidatesList.map(c =>
              c.id === candidateId
                ? { ...c, current_stage_id: currentCandidate.current_stage_id || '', phase_id: currentCandidate.phase_id }
                : c
            );
            newMap.set(phaseId, updatedList);
          }
          return newMap;
        });
      }
      alert(t('company.workflowBoard.failedToMoveCandidateMessage', { message: err.message }));
    }
  };

  const getCandidatesByStage = (stageId: string) => {
    // Get candidates in this stage
    const stageCandidates = candidates.filter((c) => c.current_stage_id === stageId);
    
    // Find the stage to check if it's SUCCESS with next_phase_id
    const stage = stages.find(s => s.id === stageId);
    
    // If this is a SUCCESS stage with next_phase_id, also include candidates from the initial stage of the next phase
    if (stage && stage.stage_type === 'success' && stage.next_phase_id) {
      const nextPhaseCandidatesList = nextPhaseCandidates.get(stage.next_phase_id) || [];
      return [...stageCandidates, ...nextPhaseCandidatesList];
    }
    
    return stageCandidates;
  };

  const moveCandidateToStage = async (candidateId: string, stageId: string) => {
    try {
      await companyCandidateService.changeStage(candidateId, { new_stage_id: stageId });
      
      // Reload data to get updated phase assignments and next phase candidates
      await loadStagesAndCandidates();
    } catch (error) {
      console.error('Failed to move candidate:', error);
      setError(t('company.workflowBoard.failedToMoveCandidate'));
    }
  };

  // Separate stages by kanban_display
  const columnStages = stages.filter(s => s.kanban_display === KanbanDisplay.COLUMN);
  const rowStages = stages.filter(s => s.kanban_display === KanbanDisplay.ROW);

  // Check if current phase is the first phase (lowest sort_order)
  const isFirstPhase = allPhases.length > 0 && phaseIdFromUrl === allPhases[0].id;

  // Find active drag candidate in current phase or next phase candidates
  const activeDragCandidate = (() => {
    const candidate = candidates.find((c) => c.id === activeId);
    if (candidate) return candidate;
    // Search in next phase candidates
    for (const nextPhaseCandidatesList of nextPhaseCandidates.values()) {
      const found = nextPhaseCandidatesList.find((c) => c.id === activeId);
      if (found) return found;
    }
    return undefined;
  })();

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
            {t('company.workflowBoard.goToPhases')}
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

        {/* Back to List View Button and Add Candidate Button (only in first phase) */}
        {phaseIdFromUrl && (
          <div className="flex items-center gap-4">
            <Link
              to={`/company/candidates?phase=${phaseIdFromUrl}`}
              className="flex items-center gap-2 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
            >
              <List className="w-4 h-4" />
              {t('company.workflowBoard.listView')}
            </Link>
            {isFirstPhase && (
              <Link
                to="/company/candidates/add"
                className="text-blue-600 hover:text-blue-800 hover:underline"
              >
                {t('company.candidates.addCandidate')}
              </Link>
            )}
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
          <SortableContext items={[
            ...candidates.map(c => c.id),
            ...Array.from(nextPhaseCandidates.values()).flat().map(c => c.id)
          ]} strategy={verticalListSortingStrategy}>
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
                      allStages={stages}
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
