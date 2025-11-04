import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
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
import { Plus, Briefcase, MapPin, DollarSign, Users, Eye, Edit, Trash2, ExternalLink, Globe, GlobeLock, Kanban, List } from 'lucide-react';
import { PositionService } from '../../services/positionService';
import { recruiterCompanyService } from '../../services/recruiterCompanyService';
import type { Position, JobPositionWorkflow, JobPositionWorkflowStage } from '../../types/position';
import { getVisibilityLabel, getVisibilityColor, getStatusLabelFromStage, getStatusColorFromStage } from '../../types/position';

// Position Card Component for Kanban
function PositionCard({
  position,
  onView,
  onEdit,
  onDelete,
}: {
  position: Position;
  onView: (positionId: string) => void;
  onEdit: (positionId: string) => void;
  onDelete: (positionId: string) => void;
}) {
  const { attributes, listeners, setNodeRef, transform, transition, isDragging } = useSortable({
    id: position.id,
  });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1,
  };

  // Get custom fields from custom_fields_values
  const location = position.custom_fields_values?.location;
  const salaryRange = position.custom_fields_values?.salary_range;
  const contractType = position.custom_fields_values?.contract_type;
  const numberOfOpenings = position.custom_fields_values?.number_of_openings || 0;

  return (
    <div
      ref={setNodeRef}
      style={style}
      {...attributes}
      {...listeners}
      className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 hover:shadow-md transition-shadow cursor-move"
    >
      <div className="mb-3">
        <h3 className="text-sm font-semibold text-gray-900 mb-2 line-clamp-2">
          {position.title}
        </h3>
        {position.stage && (
          <span className={`inline-block px-2 py-1 text-xs font-medium rounded-full ${getStatusColorFromStage(position.stage)}`}>
            {getStatusLabelFromStage(position.stage)}
          </span>
        )}
      </div>

      <div className="space-y-1 mb-3 text-xs text-gray-600">
        {location && (
          <div className="flex items-center gap-1">
            <MapPin className="w-3 h-3 text-gray-400" />
            <span className="truncate">{location}</span>
          </div>
        )}
        {contractType && (
          <div className="flex items-center gap-1">
            <Briefcase className="w-3 h-3 text-gray-400" />
            <span className="truncate">{contractType}</span>
          </div>
        )}
        {salaryRange && (
          <div className="flex items-center gap-1">
            <DollarSign className="w-3 h-3 text-gray-400" />
            <span className="truncate">
              {salaryRange.currency} {salaryRange.min_amount?.toLocaleString()} - {salaryRange.max_amount?.toLocaleString()}
            </span>
          </div>
        )}
        {numberOfOpenings > 0 && (
          <div className="flex items-center gap-1">
            <Users className="w-3 h-3 text-gray-400" />
            <span>{numberOfOpenings} opening{numberOfOpenings !== 1 ? 's' : ''}</span>
          </div>
        )}
      </div>

      <div className="flex items-center gap-2 pt-3 border-t border-gray-200">
        <button
          onClick={(e) => {
            e.stopPropagation();
            onView(position.id);
          }}
          className="flex-1 px-2 py-1 text-xs bg-blue-50 text-blue-700 rounded hover:bg-blue-100 transition-colors"
          title="View details"
        >
          <Eye className="w-3 h-3 mx-auto" />
        </button>
        <button
          onClick={(e) => {
            e.stopPropagation();
            onEdit(position.id);
          }}
          className="flex-1 px-2 py-1 text-xs bg-green-50 text-green-700 rounded hover:bg-green-100 transition-colors"
          title="Edit"
        >
          <Edit className="w-3 h-3 mx-auto" />
        </button>
        <button
          onClick={(e) => {
            e.stopPropagation();
            onDelete(position.id);
          }}
          className="flex-1 px-2 py-1 text-xs bg-red-50 text-red-700 rounded hover:bg-red-100 transition-colors"
          title="Delete"
        >
          <Trash2 className="w-3 h-3 mx-auto" />
        </button>
      </div>
    </div>
  );
}

// Stage Column Component for Kanban
function StageColumn({
  stage,
  positions,
  onView,
  onEdit,
  onDelete,
  isHorizontal = false,
}: {
  stage: JobPositionWorkflowStage;
  positions: Position[];
  onView: (positionId: string) => void;
  onEdit: (positionId: string) => void;
  onDelete: (positionId: string) => void;
  isHorizontal?: boolean;
}) {
  const { setNodeRef, isOver } = useDroppable({
    id: stage.id,
  });

  return (
    <div className={`flex flex-col ${isHorizontal ? 'w-full' : 'min-w-[280px]'} bg-gray-50 rounded-lg p-4`}>
      {/* Stage Header */}
      <div
        className="mb-4 p-3 rounded-lg"
        style={{
          backgroundColor: stage.background_color,
          color: stage.text_color,
        }}
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span
              className="text-lg"
              dangerouslySetInnerHTML={{ __html: stage.icon }}
            />
            <h3 className="font-semibold text-sm">{stage.name}</h3>
          </div>
          <span
            className="text-xs px-2 py-1 rounded-full"
            style={{
              backgroundColor: stage.text_color + '20',
              color: stage.text_color,
            }}
          >
            ({positions.length})
          </span>
        </div>
      </div>

      {/* Drop Zone */}
      <div
        ref={setNodeRef}
        className={`flex-1 min-h-[200px] max-h-[calc(100vh-300px)] overflow-y-auto overflow-x-visible p-2 rounded transition-colors ${
          isOver ? 'bg-blue-50 border-2 border-blue-300 border-dashed' : ''
        }`}
      >
        <SortableContext items={positions.map((p) => p.id)} strategy={verticalListSortingStrategy}>
          {positions.length === 0 ? (
            <div className="text-center py-8 text-gray-400 text-sm">
              Drop positions here
            </div>
          ) : (
            <div className="space-y-2">
              {positions.map((position) => (
                <PositionCard
                  key={position.id}
                  position={position}
                  onView={onView}
                  onEdit={onEdit}
                  onDelete={onDelete}
                />
              ))}
            </div>
          )}
        </SortableContext>
      </div>
    </div>
  );
}

export default function PositionsListPage() {
  const navigate = useNavigate();
  const [positions, setPositions] = useState<Position[]>([]);
  const [workflows, setWorkflows] = useState<JobPositionWorkflow[]>([]);
  const [selectedWorkflowId, setSelectedWorkflowId] = useState<string | null>(null);
  const [currentWorkflow, setCurrentWorkflow] = useState<JobPositionWorkflow | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [companySlug, setCompanySlug] = useState<string | null>(null);
  const [viewMode, setViewMode] = useState<'kanban' | 'list'>('kanban');
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
    loadCompanyData();
    loadWorkflows();
  }, []);

  useEffect(() => {
    if (workflows.length > 0 && !selectedWorkflowId) {
      // Select first workflow by default
      const defaultWorkflow = workflows.find(w => w.workflow_type === 'standard') || workflows[0];
      if (defaultWorkflow) {
        setSelectedWorkflowId(defaultWorkflow.id);
        setCurrentWorkflow(defaultWorkflow);
      }
    }
  }, [workflows]);

  useEffect(() => {
    // Load positions when workflow is first selected or when currentWorkflow changes
    // This handles the initial load after workflows are loaded
    if (currentWorkflow && selectedWorkflowId === currentWorkflow.id) {
      loadPositionsWithWorkflow(currentWorkflow);
    }
  }, [currentWorkflow?.id]);

  const loadCompanyData = async () => {
    try {
      const companyId = getCompanyId();
      if (!companyId) return;

      const company = await recruiterCompanyService.getCompany(companyId);
      setCompanySlug(company.slug);
    } catch (err) {
      console.error('Error loading company data:', err);
    }
  };

  const loadWorkflows = async () => {
    try {
      const companyId = getCompanyId();
      if (!companyId) return;

      const workflowsList = await PositionService.getWorkflows(companyId);
      setWorkflows(workflowsList);

      // Load full workflow details if positions need them
      if (workflowsList.length > 0) {
        const defaultWorkflow = workflowsList.find(w => w.workflow_type === 'standard') || workflowsList[0];
        if (defaultWorkflow) {
          const fullWorkflow = await PositionService.getWorkflow(defaultWorkflow.id);
          setCurrentWorkflow(fullWorkflow);
          setSelectedWorkflowId(defaultWorkflow.id);
        }
      }
    } catch (err) {
      console.error('Error loading workflows:', err);
    }
  };

  const loadPositions = async () => {
    // Delegate to loadPositionsWithWorkflow with current workflow
    await loadPositionsWithWorkflow(currentWorkflow);
  };

  const handleDelete = async (positionId: string) => {
    if (!confirm('Are you sure you want to delete this position?')) return;

    try {
      await PositionService.deletePosition(positionId);
      loadPositions();
    } catch (err: any) {
      alert('Failed to delete position: ' + err.message);
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

    const positionId = active.id as string;
    const droppedId = over.id as string;

    // Check if dropped on a stage (directly) or on another position
    let targetStageId: string | null = null;
    
    // First, check if it's a stage ID
    const stage = currentWorkflow?.stages.find(s => s.id === droppedId);
    if (stage) {
      targetStageId = droppedId;
    } else {
      // Check if dropped on another position (use that position's stage)
      const position = positions.find((p) => p.id === droppedId);
      if (position && position.stage_id) {
        targetStageId = position.stage_id;
      }
    }

    // If no valid target stage found, or same stage, cancel
    if (!targetStageId || !currentWorkflow?.stages.find(s => s.id === targetStageId)) {
      setActiveId(null);
      return;
    }

    // Don't move if already in the same stage
    const currentPosition = positions.find(p => p.id === positionId);
    if (currentPosition?.stage_id === targetStageId) {
      setActiveId(null);
      return;
    }

    // Move position to new stage
    try {
      await PositionService.moveToStage(positionId, targetStageId);
      loadPositions();
    } catch (err: any) {
      alert('Failed to move position: ' + err.message);
    } finally {
      setActiveId(null);
    }
  };

  const getPositionsByStage = (stageId: string) => {
    return positions.filter((p) => p.stage_id === stageId);
  };

  const handleWorkflowChange = async (workflowId: string) => {
    setSelectedWorkflowId(workflowId);
    setLoading(true); // Show loading state immediately
    try {
      const workflow = await PositionService.getWorkflow(workflowId);
      setCurrentWorkflow(workflow);
      // Reload positions when workflow changes - use the newly loaded workflow
      await loadPositionsWithWorkflow(workflow);
    } catch (err) {
      console.error('Error loading workflow:', err);
      setError('Failed to load workflow');
      setLoading(false);
    }
  };

  const loadPositionsWithWorkflow = async (workflowOverride?: JobPositionWorkflow | null) => {
    try {
      setLoading(true);
      const companyId = getCompanyId();
      if (!companyId) {
        setError('Company ID not found');
        return;
      }

      // Use the provided workflow override, or fall back to currentWorkflow
      const workflowToUse = workflowOverride || currentWorkflow;
      
      const response = await PositionService.getPositions({ company_id: companyId });
      
      console.log('[PositionsList] API response:', response);
      console.log('[PositionsList] Positions count:', response.positions?.length || 0);
      
      // Load workflow and stage data for each position
      const positionsWithWorkflow = await Promise.all(
        (response.positions || []).map(async (position) => {
          if (position.job_position_workflow_id) {
            // Use the workflow override if it matches, otherwise load it
            let workflow = workflowToUse;
            if (!workflow || workflow.id !== position.job_position_workflow_id) {
              try {
                workflow = await PositionService.getWorkflow(position.job_position_workflow_id);
              } catch (err) {
                console.error(`Error loading workflow ${position.job_position_workflow_id}:`, err);
                // Continue without workflow data if it fails
              }
            }
            
            if (workflow) {
              const stage = workflow.stages?.find(s => s.id === position.stage_id);
              return {
                ...position,
                workflow: workflow,
                stage: stage,
              };
            }
          }
          return position;
        })
      );

      console.log('[PositionsList] Positions with workflow:', positionsWithWorkflow.length);
      console.log('[PositionsList] Current workflow:', workflowToUse?.id);
      console.log('[PositionsList] View mode:', viewMode);
      console.log('[PositionsList] Positions details:', positionsWithWorkflow.map(p => ({
        id: p.id,
        title: p.title,
        job_position_workflow_id: p.job_position_workflow_id,
        stage_id: p.stage_id
      })));
      
      // Filter positions by selected workflow if a workflow is selected
      const filteredPositions = workflowToUse
        ? positionsWithWorkflow.filter(p => {
            const matches = p.job_position_workflow_id === workflowToUse.id;
            console.log(`[PositionsList] Position ${p.id} (${p.title}): workflow_id=${p.job_position_workflow_id}, matches=${matches}`);
            return matches;
          })
        : positionsWithWorkflow;
      
      console.log('[PositionsList] Filtered positions for workflow:', filteredPositions.length, 'out of', positionsWithWorkflow.length);
      console.log('[PositionsList] Workflow ID to filter:', workflowToUse?.id);
      
      setPositions(filteredPositions);
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to load positions');
      console.error('[PositionsList] Error loading positions:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading && positions.length === 0) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  const publicUrl = companySlug ? `/companies/${companySlug}/open-positions` : null;
  const columnStages = currentWorkflow?.stages.filter(s => s.kanban_display === 'vertical') || [];
  const horizontalStages = currentWorkflow?.stages.filter(s => s.kanban_display === 'horizontal_bottom') || [];
  const activeDragPosition = positions.find((p) => p.id === activeId);
  
  console.log('[PositionsList] All stages:', currentWorkflow?.stages.map(s => ({ id: s.id, name: s.name, kanban_display: s.kanban_display })));
  console.log('[PositionsList] Column stages:', columnStages.length, columnStages.map(s => ({ id: s.id, name: s.name, kanban_display: s.kanban_display })));
  console.log('[PositionsList] Horizontal stages:', horizontalStages.length, horizontalStages.map(s => ({ id: s.id, name: s.name, kanban_display: s.kanban_display })));
  console.log('[PositionsList] All positions for kanban:', positions.filter(p => p.job_position_workflow_id === currentWorkflow?.id).length);

  return (
    <div>
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Job Positions</h1>
            <p className="text-gray-600 mt-1">Manage your open positions and vacancies</p>
          </div>
          <div className="flex items-center gap-3">
            {publicUrl && (
              <a
                href={publicUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-2 px-4 py-2 bg-green-50 text-green-700 border border-green-200 rounded-lg hover:bg-green-100 transition-colors"
              >
                <ExternalLink className="w-5 h-5" />
                View Public Page
              </a>
            )}
            <button
              onClick={() => {
                const workflowId = selectedWorkflowId || workflows[0]?.id;
                if (workflowId) {
                  navigate(`/company/positions/create?workflow_id=${workflowId}`);
                } else {
                  navigate('/company/positions/create');
                }
              }}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              <Plus className="w-5 h-5" />
              Create Position
            </button>
          </div>
        </div>

        {/* Workflow Selector and View Toggle */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-4">
            {workflows.length > 0 && (
              workflows.length < 4 ? (
                // Show as tabs if less than 4 workflows
                <div className="flex items-center gap-2 bg-gray-100 rounded-lg p-1">
                  {workflows.map((workflow) => (
                    <button
                      key={workflow.id}
                      onClick={() => handleWorkflowChange(workflow.id)}
                      className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                        selectedWorkflowId === workflow.id
                          ? 'bg-white text-blue-600 shadow-sm'
                          : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                      }`}
                    >
                      {workflow.name}
                    </button>
                  ))}
                </div>
              ) : (
                // Show as dropdown if 4 or more workflows
                <select
                  value={selectedWorkflowId || ''}
                  onChange={(e) => handleWorkflowChange(e.target.value)}
                  className="px-4 py-2 border border-gray-300 rounded-lg bg-white text-sm"
                >
                  {workflows.map((workflow) => (
                    <option key={workflow.id} value={workflow.id}>
                      {workflow.name}
                    </option>
                  ))}
                </select>
              )
            )}
          </div>
          <div className="flex items-center gap-2 bg-gray-100 rounded-lg p-1">
            <button
              onClick={() => setViewMode('kanban')}
              className={`flex items-center gap-2 px-3 py-2 rounded text-sm transition-colors ${
                viewMode === 'kanban'
                  ? 'bg-white text-blue-600 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              <Kanban className="w-4 h-4" />
              Kanban
            </button>
            <button
              onClick={() => setViewMode('list')}
              className={`flex items-center gap-2 px-3 py-2 rounded text-sm transition-colors ${
                viewMode === 'list'
                  ? 'bg-white text-blue-600 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              <List className="w-4 h-4" />
              List
            </button>
          </div>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
          <p className="text-red-800">{error}</p>
        </div>
      )}

      {/* Positions Display */}
      {positions.length === 0 ? (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-12 text-center">
          <Briefcase className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No positions yet</h3>
          <p className="text-gray-600 mb-6">
            Create your first job position to start attracting candidates
          </p>
          <button
            onClick={() => {
              const workflowId = selectedWorkflowId || workflows[0]?.id;
              if (workflowId) {
                navigate(`/company/positions/create?workflow_id=${workflowId}`);
              } else {
                navigate('/company/positions/create');
              }
            }}
            className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            <Plus className="w-5 h-5" />
            Create Position
          </button>
        </div>
      ) : viewMode === 'kanban' && currentWorkflow && currentWorkflow.stages && currentWorkflow.stages.length > 0 ? (
        <DndContext
          sensors={sensors}
          onDragStart={handleDragStart}
          onDragEnd={handleDragEnd}
        >
          <div className="space-y-4">
            {/* Column stages (vertical) - shown in 2 columns grid */}
            {columnStages.length > 0 && (
              <div className="grid grid-cols-2 gap-4">
                {columnStages.map((stage) => {
                  const stagePositions = positions.filter(
                    (p) => p.stage_id === stage.id && p.job_position_workflow_id === currentWorkflow.id
                  );
                  console.log(`[PositionsList] Column Stage ${stage.id} (${stage.name}): ${stagePositions.length} positions`);
                  return (
                    <StageColumn
                      key={stage.id}
                      stage={stage}
                      positions={stagePositions}
                      onView={(id) => navigate(`/company/positions/${id}`)}
                      onEdit={(id) => navigate(`/company/positions/${id}/edit`)}
                      onDelete={handleDelete}
                    />
                  );
                })}
              </div>
            )}
            
            {/* Horizontal stages (horizontal_bottom) - shown in a row below */}
            {horizontalStages.length > 0 && (
              <div className="mt-6 pt-4 border-t border-gray-200 w-full">
                <h3 className="text-sm font-semibold text-gray-700 mb-3">Additional Stages</h3>
                <div className="w-full">
                  {horizontalStages.map((stage) => {
                    const stagePositions = positions.filter(
                      (p) => p.stage_id === stage.id && p.job_position_workflow_id === currentWorkflow.id
                    );
                    console.log(`[PositionsList] Horizontal Stage ${stage.id} (${stage.name}): ${stagePositions.length} positions`);
                    return (
                      <div key={stage.id} className="w-full mb-4 last:mb-0">
                        <StageColumn
                          stage={stage}
                          positions={stagePositions}
                          onView={(id) => navigate(`/company/positions/${id}`)}
                          onEdit={(id) => navigate(`/company/positions/${id}/edit`)}
                          onDelete={handleDelete}
                          isHorizontal={true}
                        />
                      </div>
                    );
                  })}
                </div>
              </div>
            )}
            
            {/* If no stages are configured, show all stages as columns */}
            {columnStages.length === 0 && horizontalStages.length === 0 && (
              <div className="grid grid-cols-2 gap-4">
                {currentWorkflow.stages.map((stage) => {
                  const stagePositions = positions.filter(
                    (p) => p.stage_id === stage.id && p.job_position_workflow_id === currentWorkflow.id
                  );
                  return (
                    <StageColumn
                      key={stage.id}
                      stage={stage}
                      positions={stagePositions}
                      onView={(id) => navigate(`/company/positions/${id}`)}
                      onEdit={(id) => navigate(`/company/positions/${id}/edit`)}
                      onDelete={handleDelete}
                    />
                  );
                })}
              </div>
            )}
          </div>
          <DragOverlay>
            {activeDragPosition && (
              <div className="bg-white rounded-lg shadow-lg border border-gray-200 p-4 w-64">
                <h3 className="text-sm font-semibold text-gray-900 mb-2">
                  {activeDragPosition.title}
                </h3>
                {activeDragPosition.stage && (
                  <span className={`inline-block px-2 py-1 text-xs font-medium rounded-full ${getStatusColorFromStage(activeDragPosition.stage)}`}>
                    {getStatusLabelFromStage(activeDragPosition.stage)}
                  </span>
                )}
              </div>
            )}
          </DragOverlay>
        </DndContext>
      ) : (
        // List View
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {positions.map((position) => {
            const location = position.custom_fields_values?.location;
            const salaryRange = position.custom_fields_values?.salary_range;
            const contractType = position.custom_fields_values?.contract_type;
            const numberOfOpenings = position.custom_fields_values?.number_of_openings || 0;

            return (
              <div
                key={position.id}
                className="bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow"
              >
                <div className="p-6">
                  {/* Header */}
                  <div className="mb-4">
                    <div className="flex items-start justify-between mb-2">
                      <h3 className="text-lg font-semibold text-gray-900 flex-1">
                        {position.title}
                      </h3>
                      {position.stage && (
                        <span className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColorFromStage(position.stage)}`}>
                          {getStatusLabelFromStage(position.stage)}
                        </span>
                      )}
                    </div>
                    <div className="flex items-center gap-2">
                      <span className={`px-2 py-1 text-xs font-medium rounded-full ${getVisibilityColor(position.visibility)}`}>
                        {getVisibilityLabel(position.visibility)}
                      </span>
                    </div>
                  </div>

                  {/* Details */}
                  <div className="space-y-2 mb-4 text-sm text-gray-600">
                    {location && (
                      <div className="flex items-center gap-2">
                        <MapPin className="w-4 h-4 text-gray-400" />
                        <span>{location}</span>
                      </div>
                    )}
                    {contractType && (
                      <div className="flex items-center gap-2">
                        <Briefcase className="w-4 h-4 text-gray-400" />
                        <span>{contractType}</span>
                      </div>
                    )}
                    {salaryRange && (
                      <div className="flex items-center gap-2">
                        <DollarSign className="w-4 h-4 text-gray-400" />
                        <span>
                          {salaryRange.currency} {salaryRange.min_amount?.toLocaleString()} - {salaryRange.max_amount?.toLocaleString()}
                        </span>
                      </div>
                    )}
                    {numberOfOpenings > 0 && (
                      <div className="flex items-center gap-2">
                        <Users className="w-4 h-4 text-gray-400" />
                        <span>{numberOfOpenings} opening{numberOfOpenings !== 1 ? 's' : ''}</span>
                      </div>
                    )}
                  </div>

                  {/* Actions */}
                  <div className="flex items-center gap-2 pt-4 border-t border-gray-200">
                    <button
                      onClick={() => navigate(`/company/positions/${position.id}`)}
                      className="flex-1 px-3 py-2 text-sm bg-blue-50 text-blue-700 rounded-lg hover:bg-blue-100 transition-colors group relative"
                      title="View details"
                    >
                      <Eye className="w-4 h-4 mx-auto" />
                    </button>
                    <button
                      onClick={() => navigate(`/company/positions/${position.id}/edit`)}
                      className="flex-1 px-3 py-2 text-sm bg-green-50 text-green-700 rounded-lg hover:bg-green-100 transition-colors group relative"
                      title="Edit"
                    >
                      <Edit className="w-4 h-4 mx-auto" />
                    </button>
                    <button
                      onClick={() => handleDelete(position.id)}
                      className="flex-1 px-3 py-2 text-sm bg-red-50 text-red-700 rounded-lg hover:bg-red-100 transition-colors group relative"
                      title="Delete"
                    >
                      <Trash2 className="w-4 h-4 mx-auto" />
                    </button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Info Box */}
      <div className="mt-8 bg-green-50 border border-green-200 rounded-lg p-6">
        <div className="flex items-start gap-3">
          <Briefcase className="w-6 h-6 text-green-600 flex-shrink-0 mt-1" />
          <div>
            <h4 className="font-semibold text-green-900 mb-1">About Job Positions</h4>
            <p className="text-green-800 text-sm">
              Job positions help you organize your open vacancies. You can create positions
              with details like title, department, location, salary range, and requirements.
              Link candidates to specific positions to track applications and hiring progress.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
