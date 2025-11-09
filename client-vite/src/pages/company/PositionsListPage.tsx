import { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
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
import { Plus, Briefcase, MapPin, DollarSign, Users, Eye, Edit, ExternalLink, Kanban, List, MessageCircle } from 'lucide-react';
import { PositionService } from '../../services/positionService';
import { recruiterCompanyService } from '../../services/recruiterCompanyService';
import { companyWorkflowService } from '../../services/companyWorkflowService.ts';
import type { Position, JobPositionWorkflow, JobPositionWorkflowStage } from '../../types/position';
import type { CompanyWorkflow, WorkflowStage } from '../../types/workflow.ts';
import { getVisibilityLabel, getVisibilityColor, getStatusLabelFromStage, getStatusColorFromStage } from '../../types/position';
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

// Position Card Component for Kanban
function PositionCard({
  position,
  onView,
  onEdit,
  onViewPublic,
  horizontalStages,
  onMoveToStage,
}: {
  position: Position;
  onView: (positionId: string) => void;
  onEdit: (positionId: string) => void;
  onViewPublic: (position: Position) => void;
  horizontalStages: JobPositionWorkflowStage[];
  onMoveToStage: (positionId: string, stageId: string) => void;
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
    <Card
      ref={setNodeRef}
      style={style}
      {...attributes}
      {...listeners}
      className="cursor-move hover:shadow-md transition-shadow"
    >
      <CardContent className="p-4">
        <div className="mb-3">
          <h3 className="text-sm font-semibold text-gray-900 mb-2 line-clamp-2">
            {position.title}
          </h3>
          <div className="flex items-center gap-2">
            {position.stage && (
              <Badge variant="secondary" className={getStatusColorFromStage(position.stage)}>
                {getStatusLabelFromStage(position.stage)}
              </Badge>
            )}
            {position.pending_comments_count !== undefined && position.pending_comments_count > 0 && (
              <Badge variant="secondary" className="bg-yellow-100 text-yellow-800 hover:bg-yellow-200">
                <MessageCircle className="w-3 h-3 mr-1" />
                {position.pending_comments_count}
              </Badge>
            )}
          </div>
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

        <div className="flex items-center justify-between gap-2 pt-3 border-t border-gray-200">
          {/* Main actions - left side */}
          <div className="flex items-center gap-2">
            <Tooltip>
              <TooltipTrigger asChild>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={(e) => {
                    e.stopPropagation();
                    onView(position.id);
                  }}
                  className="h-7 px-2 bg-blue-50 text-blue-700 hover:bg-blue-100"
                >
                  <Eye className="w-3 h-3" />
                </Button>
              </TooltipTrigger>
              <TooltipContent>
                <p>View details</p>
              </TooltipContent>
            </Tooltip>

            <Tooltip>
              <TooltipTrigger asChild>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={(e) => {
                    e.stopPropagation();
                    onEdit(position.id);
                  }}
                  className="h-7 px-2 bg-green-50 text-green-700 hover:bg-green-100"
                >
                  <Edit className="w-3 h-3" />
                </Button>
              </TooltipTrigger>
              <TooltipContent>
                <p>Edit position</p>
              </TooltipContent>
            </Tooltip>

            {position.visibility === 'public' && position.public_slug && (
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={(e) => {
                      e.stopPropagation();
                      onViewPublic(position);
                    }}
                    className="h-7 px-2 bg-purple-50 text-purple-700 hover:bg-purple-100"
                  >
                    <ExternalLink className="w-3 h-3" />
                  </Button>
                </TooltipTrigger>
                <TooltipContent>
                  <p>View public page</p>
                </TooltipContent>
              </Tooltip>
            )}
          </div>

          {/* Move to horizontal stages buttons - right side */}
          {horizontalStages.length > 0 && (
            <div className="flex items-center gap-1">
              {horizontalStages
                .filter((stage) => stage.id !== position.stage_id)
                .map((stage) => (
                  <Tooltip key={stage.id}>
                    <TooltipTrigger asChild>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={(e) => {
                          e.stopPropagation();
                          onMoveToStage(position.id, stage.id);
                        }}
                        className="h-7 px-2 hover:opacity-80"
                        style={{
                          backgroundColor: stage.background_color,
                          color: stage.text_color,
                        }}
                      >
                        <span className="text-xs">{stage.icon}</span>
                      </Button>
                    </TooltipTrigger>
                    <TooltipContent>
                      <p>Move to {stage.name}</p>
                    </TooltipContent>
                  </Tooltip>
                ))}
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}

// Stage Column Component for Kanban
function StageColumn({
  stage,
  positions,
  onView,
  onEdit,
  onViewPublic,
  horizontalStages,
  onMoveToStage,
  isHorizontal = false,
}: {
  stage: JobPositionWorkflowStage;
  positions: Position[];
  onView: (positionId: string) => void;
  onEdit: (positionId: string) => void;
  onViewPublic: (position: Position) => void;
  horizontalStages: JobPositionWorkflowStage[];
  onMoveToStage: (positionId: string, stageId: string) => void;
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
                  onViewPublic={onViewPublic}
                  horizontalStages={horizontalStages}
                  onMoveToStage={onMoveToStage}
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
  // Wrap entire page with TooltipProvider
  return (
    <TooltipProvider delayDuration={200} skipDelayDuration={100}>
      <PositionsListPageContent />
    </TooltipProvider>
  );
}

function PositionsListPageContent() {
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();
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
      // Try to get workflow_id from URL first
      const workflowIdFromUrl = searchParams.get('workflow_id');
      
      let workflowToSelect: JobPositionWorkflow | null = null;
      
      if (workflowIdFromUrl) {
        // Find workflow from URL
        workflowToSelect = workflows.find(w => w.id === workflowIdFromUrl) || null;
      }
      
      // If not found in URL or URL doesn't have it, use first workflow
      if (!workflowToSelect) {
        workflowToSelect = workflows[0];
      }
      
      if (workflowToSelect) {
        setSelectedWorkflowId(workflowToSelect.id);
        setCurrentWorkflow(workflowToSelect);
        // Update URL if it wasn't there or was invalid
        if (!workflowIdFromUrl || workflowIdFromUrl !== workflowToSelect.id) {
          setSearchParams({ workflow_id: workflowToSelect.id });
        }
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
      setLoading(true);
      const companyId = getCompanyId();
      if (!companyId) {
        setLoading(false);
        return;
      }

      // Use new system: get workflows filtered by type 'PO' (Job Position Opening)
      const workflowsList = await companyWorkflowService.listWorkflowsByCompany(companyId, 'PO');
      
      // Convert CompanyWorkflow to JobPositionWorkflow format
      const convertedWorkflows: JobPositionWorkflow[] = await Promise.all(
        workflowsList.map(async (workflow: CompanyWorkflow) => {
          // Load stages for this workflow
          let stages: JobPositionWorkflowStage[] = [];
          try {
            const workflowStages = await companyWorkflowService.listStagesByWorkflow(workflow.id);
            stages = workflowStages.map((stage: WorkflowStage) => ({
              id: stage.id,
              name: stage.name,
              icon: stage.style?.icon || '📋',
              background_color: stage.style?.background_color || '#f3f4f6',
              text_color: stage.style?.color || '#374151', // StageStyle uses 'color' not 'text_color'
              role: null,
              status_mapping: mapStageTypeToStatus(stage.stage_type),
              kanban_display: mapKanbanDisplay(typeof stage.kanban_display === 'string' ? stage.kanban_display : (stage.kanban_display || 'column')),
              field_visibility: {},
              field_validation: {},
              field_candidate_visibility: {},
            }));
          } catch (err) {
            console.error(`Error loading stages for workflow ${workflow.id}:`, err);
          }

          return {
            id: workflow.id,
            company_id: workflow.company_id,
            name: workflow.name,
            default_view: 'kanban', // Default for job positions
            status: mapWorkflowStatus(workflow.status),
            stages: stages,
            custom_fields_config: {},
            created_at: workflow.created_at,
            updated_at: workflow.updated_at,
          };
        })
      );

      setWorkflows(convertedWorkflows);

      // Load full workflow details if positions need them
      if (convertedWorkflows.length > 0) {
        const defaultWorkflow = convertedWorkflows[0]; // Use the first workflow as default
        if (defaultWorkflow) {
          setCurrentWorkflow(defaultWorkflow);
          setSelectedWorkflowId(defaultWorkflow.id);
        }
      }
    } catch (err) {
      console.error('Error loading workflows:', err);
      setError('Failed to load workflows');
    } finally {
      setLoading(false);
    }
  };

  // Helper to map WorkflowStatus to old status format
  const mapWorkflowStatus = (status: string): string => {
    switch (status) {
      case 'ACTIVE':
        return 'published';
      case 'DRAFT':
        return 'draft';
      case 'ARCHIVED':
        return 'deprecated';
      default:
        return status.toLowerCase();
    }
  };

  // Helper to map StageType to status_mapping
  const mapStageTypeToStatus = (stageType: string): string => {
    // Map stage types to job position statuses
    // This is a simplified mapping - adjust based on your business logic
    switch (stageType) {
      case 'initial':
        return 'draft';
      case 'standard':
      case 'progress':
        return 'active';
      case 'success':
        return 'closed';
      case 'fail':
        return 'archived';
      default:
        return 'draft';
    }
  };

  // Helper to map KanbanDisplay to old format
  const mapKanbanDisplay = (kanbanDisplay: string | undefined): string => {
    if (!kanbanDisplay) return 'column';
    // Map new system values to old format
    switch (kanbanDisplay) {
      case 'column':
        return 'vertical';
      case 'row':
        return 'horizontal_bottom';
      case 'none':
        return 'none';
      default:
        // If already in old format, return as is
        return kanbanDisplay;
    }
  };

  const loadPositions = async () => {
    // Delegate to loadPositionsWithWorkflow with current workflow
    await loadPositionsWithWorkflow(currentWorkflow);
  };

  const handleViewPublic = (position: Position) => {
    if (!position.public_slug || !companySlug) return;
    
    const url = `/companies/${companySlug}/positions/${position.public_slug}`;
    window.open(url, '_blank');
  };

  const handleMoveToStage = async (positionId: string, stageId: string) => {
    try {
      await PositionService.moveToStage(positionId, stageId);
      loadPositions();
    } catch (err: any) {
      // Check if it's a validation error (400)
      if (err.response?.status === 400 && err.response?.data?.detail?.validation_errors) {
        const errors = err.response.data.detail.validation_errors;
        const errorMessages = Object.entries(errors)
          .map(([field, messages]: [string, any]) => {
            const messageList = Array.isArray(messages) ? messages : [messages];
            return `• ${field}: ${messageList.join(', ')}`;
          })
          .join('\n');
        
        const shouldEdit = confirm(
          `Cannot move to this stage. The following fields need attention:\n\n${errorMessages}\n\nWould you like to edit this position now?`
        );
        
        if (shouldEdit) {
          navigate(`/company/positions/${positionId}/edit`);
        }
      } else {
        alert('Failed to move position: ' + (err.message || 'Unknown error'));
      }
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
      // Check if it's a validation error (400)
      if (err.response?.status === 400 && err.response?.data?.detail?.validation_errors) {
        const errors = err.response.data.detail.validation_errors;
        const errorMessages = Object.entries(errors)
          .map(([field, messages]: [string, any]) => {
            const messageList = Array.isArray(messages) ? messages : [messages];
            return `• ${field}: ${messageList.join(', ')}`;
          })
          .join('\n');
        
        const shouldEdit = confirm(
          `Cannot move to this stage. The following fields need attention:\n\n${errorMessages}\n\nWould you like to edit this position now?`
        );
        
        if (shouldEdit) {
          navigate(`/company/positions/${positionId}/edit`);
        }
      } else {
        alert('Failed to move position: ' + (err.message || 'Unknown error'));
      }
    } finally {
      setActiveId(null);
    }
  };


  const handleWorkflowChange = async (workflowId: string) => {
    setSelectedWorkflowId(workflowId);
    setSearchParams({ workflow_id: workflowId }); // Update URL
    setLoading(true); // Show loading state immediately
    try {
      // Use new system: get workflow and stages
      const workflow = await companyWorkflowService.getWorkflow(workflowId);
      const workflowStages = await companyWorkflowService.listStagesByWorkflow(workflowId);
      
      // Convert to JobPositionWorkflow format
      const convertedWorkflow: JobPositionWorkflow = {
        id: workflow.id,
        company_id: workflow.company_id,
        name: workflow.name,
        default_view: 'kanban',
        status: mapWorkflowStatus(workflow.status),
        stages: workflowStages.map((stage: WorkflowStage) => ({
          id: stage.id,
          name: stage.name,
          icon: stage.style?.icon || '📋',
          background_color: stage.style?.background_color || '#f3f4f6',
          text_color: stage.style?.text_color || '#374151',
          role: null,
          status_mapping: mapStageTypeToStatus(stage.stage_type),
          kanban_display: stage.kanban_display || 'column',
          field_visibility: {},
          field_validation: {},
          field_candidate_visibility: {},
        })),
        custom_fields_config: {},
        created_at: workflow.created_at,
        updated_at: workflow.updated_at,
      };
      
      setCurrentWorkflow(convertedWorkflow);
      // Reload positions when workflow changes - use the newly loaded workflow
      await loadPositionsWithWorkflow(convertedWorkflow);
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
                // Use new system: get workflow and stages
                const newWorkflow = await companyWorkflowService.getWorkflow(position.job_position_workflow_id);
                const workflowStages = await companyWorkflowService.listStagesByWorkflow(position.job_position_workflow_id);
                
                // Convert to JobPositionWorkflow format
                workflow = {
                  id: newWorkflow.id,
                  company_id: newWorkflow.company_id,
                  name: newWorkflow.name,
                  default_view: 'kanban',
                  status: mapWorkflowStatus(newWorkflow.status),
                  stages: workflowStages.map((stage: WorkflowStage) => ({
                    id: stage.id,
                    name: stage.name,
                    icon: stage.style?.icon || '📋',
                    background_color: stage.style?.background_color || '#f3f4f6',
                    text_color: stage.style?.text_color || '#374151',
                    role: null,
                    status_mapping: mapStageTypeToStatus(stage.stage_type),
                    kanban_display: stage.kanban_display || 'column',
                    field_visibility: {},
                    field_validation: {},
                    field_candidate_visibility: {},
                  })),
                  custom_fields_config: {},
                  created_at: newWorkflow.created_at,
                  updated_at: newWorkflow.updated_at,
                };
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
              <Button
                variant="outline"
                asChild
              >
                <a
                  href={publicUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="gap-2 bg-green-50 text-green-700 border-green-200 hover:bg-green-100"
                >
                  <ExternalLink className="w-5 h-5" />
                  View Public Page
                </a>
              </Button>
            )}
            <Button
              onClick={() => {
                const workflowId = selectedWorkflowId || workflows[0]?.id;
                if (workflowId) {
                  navigate(`/company/positions/create?workflow_id=${workflowId}`);
                } else {
                  navigate('/company/positions/create');
                }
              }}
            >
              <Plus className="w-5 h-5 mr-2" />
              Create Position
            </Button>
          </div>
        </div>

        {/* Workflow Selector and View Toggle */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-4">
            {workflows.length > 0 && (
              workflows.length < 4 ? (
                // Show as tabs if less than 4 workflows
                <Tabs value={selectedWorkflowId || ''} onValueChange={handleWorkflowChange}>
                  <TabsList>
                    {workflows.map((workflow) => (
                      <TabsTrigger key={workflow.id} value={workflow.id}>
                        {workflow.name}
                      </TabsTrigger>
                    ))}
                  </TabsList>
                </Tabs>
              ) : (
                // Show as dropdown if 4 or more workflows
                <Select value={selectedWorkflowId || ''} onValueChange={handleWorkflowChange}>
                  <SelectTrigger className="w-[200px]">
                    <SelectValue placeholder="Select workflow" />
                  </SelectTrigger>
                  <SelectContent>
                    {workflows.map((workflow) => (
                      <SelectItem key={workflow.id} value={workflow.id}>
                        {workflow.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              )
            )}
          </div>
          <Tabs value={viewMode} onValueChange={(value) => setViewMode(value as 'kanban' | 'list')}>
            <TabsList>
              <TabsTrigger value="kanban">
                <Kanban className="w-4 h-4 mr-2" />
                Kanban
              </TabsTrigger>
              <TabsTrigger value="list">
                <List className="w-4 h-4 mr-2" />
                List
              </TabsTrigger>
            </TabsList>
          </Tabs>
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
          <Button
            onClick={() => {
              const workflowId = selectedWorkflowId || workflows[0]?.id;
              if (workflowId) {
                navigate(`/company/positions/create?workflow_id=${workflowId}`);
              } else {
                navigate('/company/positions/create');
              }
            }}
          >
            <Plus className="w-5 h-5 mr-2" />
            Create Position
          </Button>
        </div>
      ) : viewMode === 'list' ? (
        // List View - Table format
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Title
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Stage
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Visibility
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Location
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Contract
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Salary Range
                  </th>
                  <th scope="col" className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Comments
                  </th>
                  <th scope="col" className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {positions.map((position) => {
                  const location = position.custom_fields_values?.location;
                  const salaryRange = position.custom_fields_values?.salary_range;
                  const contractType = position.custom_fields_values?.contract_type;

                  return (
                    <tr key={position.id} className="hover:bg-gray-50 transition-colors">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-gray-900">{position.title}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        {position.stage && (
                          <Badge variant="secondary" className={getStatusColorFromStage(position.stage)}>
                            {getStatusLabelFromStage(position.stage)}
                          </Badge>
                        )}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <Badge variant="outline" className={getVisibilityColor(position.visibility)}>
                          {getVisibilityLabel(position.visibility)}
                        </Badge>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-gray-600">
                          {location || '-'}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-gray-600">
                          {contractType || '-'}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-gray-600">
                          {salaryRange ? (
                            `${salaryRange.currency} ${salaryRange.min_amount?.toLocaleString()} - ${salaryRange.max_amount?.toLocaleString()}`
                          ) : (
                            '-'
                          )}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-center">
                        {position.pending_comments_count !== undefined && position.pending_comments_count > 0 ? (
                          <Badge variant="secondary" className="bg-yellow-100 text-yellow-800 hover:bg-yellow-200">
                            <MessageCircle className="w-3 h-3 mr-1" />
                            {position.pending_comments_count}
                          </Badge>
                        ) : (
                          <span className="text-sm text-gray-400">-</span>
                        )}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-right">
                        <TooltipProvider delayDuration={300}>
                          <div className="flex items-center justify-end gap-1">
                            <Tooltip>
                              <TooltipTrigger asChild>
                                <Button
                                  variant="ghost"
                                  size="sm"
                                  onClick={() => navigate(`/company/positions/${position.id}`)}
                                  className="bg-blue-50 text-blue-700 hover:bg-blue-100"
                                >
                                  <Eye className="w-4 h-4" />
                                </Button>
                              </TooltipTrigger>
                              <TooltipContent>
                                <p>View details</p>
                              </TooltipContent>
                            </Tooltip>

                            <Tooltip>
                              <TooltipTrigger asChild>
                                <Button
                                  variant="ghost"
                                  size="sm"
                                  onClick={() => navigate(`/company/positions/${position.id}/edit`)}
                                  className="bg-green-50 text-green-700 hover:bg-green-100"
                                >
                                  <Edit className="w-4 h-4" />
                                </Button>
                              </TooltipTrigger>
                              <TooltipContent>
                                <p>Edit position</p>
                              </TooltipContent>
                            </Tooltip>

                            {position.visibility === 'public' && position.public_slug && (
                              <Tooltip>
                                <TooltipTrigger asChild>
                                  <Button
                                    variant="ghost"
                                    size="sm"
                                    onClick={() => handleViewPublic(position)}
                                    className="bg-purple-50 text-purple-700 hover:bg-purple-100"
                                  >
                                    <ExternalLink className="w-4 h-4" />
                                  </Button>
                                </TooltipTrigger>
                                <TooltipContent>
                                  <p>View public page</p>
                                </TooltipContent>
                              </Tooltip>
                            )}
                          </div>
                        </TooltipProvider>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      ) : viewMode === 'kanban' && currentWorkflow && currentWorkflow.stages && currentWorkflow.stages.length > 0 ? (
        <DndContext
          sensors={sensors}
          onDragStart={handleDragStart}
          onDragEnd={handleDragEnd}
        >
          <div className="space-y-4">
            {/* Column stages (vertical) - shown in horizontal scrollable row */}
            {columnStages.length > 0 && (
              <div className="overflow-x-auto pb-4">
                <div className="flex gap-4 min-w-max">
                  {columnStages.map((stage) => {
                    const stagePositions = positions.filter(
                      (p) => p.stage_id === stage.id && p.job_position_workflow_id === currentWorkflow.id
                    );
                    console.log(`[PositionsList] Column Stage ${stage.id} (${stage.name}): ${stagePositions.length} positions`);
                    return (
                      <div key={stage.id} className="w-80 flex-shrink-0">
                        <StageColumn
                          stage={stage}
                          positions={stagePositions}
                          onView={(id) => navigate(`/company/positions/${id}`)}
                          onEdit={(id) => navigate(`/company/positions/${id}/edit`)}
                          onViewPublic={handleViewPublic}
                          horizontalStages={horizontalStages}
                          onMoveToStage={handleMoveToStage}
                        />
                      </div>
                    );
                  })}
                </div>
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
                          onViewPublic={handleViewPublic}
                          horizontalStages={horizontalStages}
                          onMoveToStage={handleMoveToStage}
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
              <div className="overflow-x-auto pb-4">
                <div className="flex gap-4 min-w-max">
                  {currentWorkflow.stages.map((stage) => {
                    const stagePositions = positions.filter(
                      (p) => p.stage_id === stage.id && p.job_position_workflow_id === currentWorkflow.id
                    );
                    return (
                      <div key={stage.id} className="w-80 flex-shrink-0">
                        <StageColumn
                          stage={stage}
                          positions={stagePositions}
                          onView={(id) => navigate(`/company/positions/${id}`)}
                          onEdit={(id) => navigate(`/company/positions/${id}/edit`)}
                          onViewPublic={handleViewPublic}
                          horizontalStages={horizontalStages}
                          onMoveToStage={handleMoveToStage}
                        />
                      </div>
                    );
                  })}
                </div>
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
      ) : null}

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
