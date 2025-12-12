import { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Edit, Workflow, Eye, EyeOff, FileText, MessageSquare, History, Move, ChevronDown, Users } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { PositionService } from '../../services/positionService';
import type { Position, JobPositionWorkflow, CustomFieldDefinition } from '../../types/position';
import {
  getStatusColorFromStage,
  getStatusLabelFromStage,
  getDepartment,
  getRequirements,
  getBenefits,
} from '../../types/position';
import { PositionCommentsSection } from '../../components/jobPosition/PositionCommentsSection';
import { JobPositionActivityTimeline } from '../../components/jobPosition/JobPositionActivityTimeline';
import JobPositionActivityService from '../../services/JobPositionActivityService';
import JobPositionCommentService from '../../services/JobPositionCommentService';
import type { JobPositionActivity } from '../../types/jobPositionActivity';
import { companyWorkflowService } from '../../services/companyWorkflowService';
import { EntityCustomizationService } from '../../services/entityCustomizationService';
import type { WorkflowStage } from '../../types/workflow';
import { KanbanDisplay } from '../../types/workflow';
import {
  StatusBadge,
  EmploymentTypeBadge,
  LocationTypeBadge,
  ExperienceLevelBadge,
  SalaryRange,
  SkillsChips,
  LanguagesList
} from '../../components/jobPosition/publishing';

// Helper to map workflow field types to position field types
const mapFieldType = (fieldType: string): CustomFieldDefinition['field_type'] => {
  const typeMap: Record<string, CustomFieldDefinition['field_type']> = {
    'TEXT': 'TEXT',
    'TEXTAREA': 'TEXT',
    'NUMBER': 'NUMBER',
    'CURRENCY': 'NUMBER',
    'DATE': 'DATE',
    'DROPDOWN': 'SELECT',
    'MULTI_SELECT': 'MULTISELECT',
    'RADIO': 'SELECT',
    'CHECKBOX': 'BOOLEAN',
    'FILE': 'TEXT',
    'URL': 'URL',
    'EMAIL': 'TEXT',
    'PHONE': 'TEXT',
  };
  return typeMap[fieldType] || 'TEXT';
};

// Load custom fields from workflow that are visible to candidates in ANY stage
const loadCandidateVisibleFields = async (
  workflowId: string,
  stages: WorkflowStage[]
): Promise<CustomFieldDefinition[]> => {
  try {
    const customFields = await EntityCustomizationService.listFieldsByEntity('Workflow', workflowId);

    if (!customFields || customFields.length === 0) {
      return [];
    }

    const candidateVisibleFields: CustomFieldDefinition[] = [];

    for (const field of customFields) {
      let isVisibleToCandidate = false;
      let isRequired = false;

      for (const stage of stages) {
        const fieldPropsById = stage.field_properties_config?.[field.id];
        const fieldPropsByKey = stage.field_properties_config?.[field.field_key];
        const fieldProps = fieldPropsById || fieldPropsByKey;

        if (fieldProps?.visible_candidate) {
          isVisibleToCandidate = true;
          if (fieldProps.is_required) {
            isRequired = true;
          }
        }
      }

      if (isVisibleToCandidate) {
        candidateVisibleFields.push({
          field_key: field.field_key,
          label: field.field_name,
          field_type: mapFieldType(field.field_type),
          options: field.field_config?.options || null,
          is_required: isRequired,
          candidate_visible: true,
          validation_rules: null,
          sort_order: field.order_index,
          is_active: true,
        });
      }
    }

    candidateVisibleFields.sort((a, b) => a.sort_order - b.sort_order);
    return candidateVisibleFields;
  } catch (err) {
    console.error('Error loading candidate visible fields:', err);
    return [];
  }
};

export default function PositionDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [position, setPosition] = useState<Position | null>(null);
  const [workflow, setWorkflow] = useState<JobPositionWorkflow | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'info' | 'comments' | 'history'>('info');
  const [activities, setActivities] = useState<JobPositionActivity[]>([]);
  const [loadingActivities, setLoadingActivities] = useState(false);
  const [pendingCommentsCount, setPendingCommentsCount] = useState(0);

  // Stage transition state
  const [availableStages, setAvailableStages] = useState<WorkflowStage[]>([]);
  const [changingStage, setChangingStage] = useState(false);

  // Custom fields from recruitment workflows
  const [candidateVisibleFields, setCandidateVisibleFields] = useState<CustomFieldDefinition[]>([]);

  // Custom fields from publication workflow
  const [publicationWorkflowFields, setPublicationWorkflowFields] = useState<CustomFieldDefinition[]>([]);

  // Move to Stage dropdown state
  const [showMoveToStageDropdown, setShowMoveToStageDropdown] = useState(false);
  const moveToStageDropdownRef = useRef<HTMLDivElement>(null);


  // Comments refresh key
  const [commentsRefreshKey, setCommentsRefreshKey] = useState(0);

  useEffect(() => {
    if (id) {
      loadPosition();
      loadPendingCommentsCount();
      if (activeTab === 'history') {
        loadActivities();
      }
    }
  }, [id, activeTab]);

  const loadPosition = async () => {
    if (!id) return;

    try {
      setLoading(true);
      const data = await PositionService.getPositionById(id);
      setPosition(data);

      // Load workflow if available
      if (data.job_position_workflow_id) {
        try {
          const workflowData = await PositionService.getWorkflow(data.job_position_workflow_id);
          setWorkflow(workflowData);

          // Load workflow stages
          await loadWorkflowStages(data.job_position_workflow_id);

          // Load custom fields from publication workflow
          try {
            const pubCustomFields = await EntityCustomizationService.listFieldsByEntity('Workflow', data.job_position_workflow_id);
            if (pubCustomFields && pubCustomFields.length > 0) {
              const mappedFields: CustomFieldDefinition[] = pubCustomFields.map(field => ({
                field_key: field.field_key,
                label: field.field_name,
                field_type: mapFieldType(field.field_type),
                options: field.field_config?.options || null,
                is_required: false,
                candidate_visible: false,
                validation_rules: null,
                sort_order: field.order_index,
                is_active: true,
              }));
              setPublicationWorkflowFields(mappedFields);
            }
          } catch (err) {
            console.error('Error loading publication workflow fields:', err);
          }
        } catch (err) {
          console.error('Error loading workflow:', err);
        }
      }

      // Load custom fields from recruitment workflows (phase_workflows)
      if (data.phase_workflows && Object.keys(data.phase_workflows).length > 0) {
        try {
          const recruitmentWorkflowIds = [...new Set(Object.values(data.phase_workflows))];
          const allFields: CustomFieldDefinition[] = [];
          const seenFieldKeys = new Set<string>();

          for (const workflowId of recruitmentWorkflowIds) {
            try {
              const recruitmentStages = await companyWorkflowService.listStagesByWorkflow(workflowId);
              const fields = await loadCandidateVisibleFields(workflowId, recruitmentStages);

              for (const field of fields) {
                if (!seenFieldKeys.has(field.field_key)) {
                  seenFieldKeys.add(field.field_key);
                  allFields.push(field);
                }
              }
            } catch (err) {
              console.error(`Error loading fields from workflow ${workflowId}:`, err);
            }
          }

          setCandidateVisibleFields(allFields);
        } catch (err) {
          console.error('Error loading candidate visible fields:', err);
        }
      }

      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to load position');
      console.error('Error loading position:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadActivities = async () => {
    if (!id) return;

    try {
      setLoadingActivities(true);
      const fetchedActivities = await JobPositionActivityService.getActivities(id);
      setActivities(fetchedActivities);
    } catch (err) {
      console.error('Error loading activities:', err);
    } finally {
      setLoadingActivities(false);
    }
  };

  const loadPendingCommentsCount = async () => {
    if (!id) return;

    try {
      const allComments = await JobPositionCommentService.getAllComments(id);
      const pendingCount = JobPositionCommentService.countPendingComments(allComments);
      setPendingCommentsCount(pendingCount);
    } catch (err) {
      console.error('Error loading pending comments count:', err);
    }
  };

  const loadWorkflowStages = async (workflowId: string) => {
    try {
      // Use companyWorkflowService to get full stage data including kanban_display
      const stages = await companyWorkflowService.listStagesByWorkflow(workflowId);
      setAvailableStages(stages);
    } catch (err) {
      console.error('Error loading workflow stages:', err);
    }
  };

  const handleMoveToStage = async (stageId: string) => {
    if (!id || !position) return;

    try {
      setChangingStage(true);
      await PositionService.moveToStage(id, stageId);
      // Reload position to get updated stage
      await loadPosition();
      setShowMoveToStageDropdown(false);
    } catch (err: any) {
      alert(`Failed to move position: ${err.message}`);
    } finally {
      setChangingStage(false);
    }
  };


  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (moveToStageDropdownRef.current && !moveToStageDropdownRef.current.contains(event.target as Node)) {
        setShowMoveToStageDropdown(false);
      }
    };

    if (showMoveToStageDropdown) {
      document.addEventListener('mousedown', handleClickOutside);
      return () => document.removeEventListener('mousedown', handleClickOutside);
    }
  }, [showMoveToStageDropdown]);

  const getVisibilityLabel = (visibility: string) => {
    switch (visibility) {
      case 'public':
        return 'Public';
      case 'internal':
        return 'Internal';
      case 'hidden':
        return 'Hidden';
      default:
        return visibility;
    }
  };

  const getVisibilityColor = (visibility: string) => {
    switch (visibility) {
      case 'public':
        return 'bg-green-100 text-green-800';
      case 'internal':
        return 'bg-blue-100 text-blue-800';
      case 'hidden':
        return 'bg-gray-100 text-gray-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };



  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error || !position) {
    return (
      <Alert variant="destructive">
        <AlertDescription>{error || 'Position not found'}</AlertDescription>
        <Button
          variant="outline"
          onClick={() => navigate('/company/positions')}
          className="mt-4"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to Positions
        </Button>
      </Alert>
    );
  }

  return (
    <div>
      {/* Header */}
      <div className="mb-6">
        <Button
          variant="ghost"
          onClick={() => navigate('/company/positions')}
          className="mb-4"
        >
          <ArrowLeft className="w-5 h-5 mr-2" />
          Back to Positions
        </Button>

        <div className="flex items-start justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">{position.title}</h1>
            <div className="flex items-center gap-3 mt-2">
              {getDepartment(position) && (
                <p className="text-gray-600">{getDepartment(position)}</p>
              )}
              {workflow && (
                <div className="flex items-center gap-2">
                  <Workflow className="w-4 h-4 text-gray-400" />
                  <span className="text-sm text-gray-600">{workflow.name}</span>
                </div>
              )}
            </div>
          </div>

          <div className="flex items-center gap-2">
            {/* Publishing Flow Status */}
            <StatusBadge status={position.status} size="md" />

            {/* Stage Badge (if using workflow) */}
            {position.stage && (
              <Badge className={getStatusColorFromStage(position.stage)}>
                {getStatusLabelFromStage(position.stage)}
              </Badge>
            )}
            <Badge className={getVisibilityColor(position.visibility)}>
              {position.visibility === 'public' ? <Eye className="w-3 h-3 inline mr-1" /> : <EyeOff className="w-3 h-3 inline mr-1" />}
              {getVisibilityLabel(position.visibility)}
            </Badge>
            <Button
              onClick={() => navigate(`/company/positions/${id}/edit`)}
              title="Edit this position"
            >
              <Edit className="w-4 h-4 mr-2" />
              Edit
            </Button>
            {/* Move to Stage Dropdown */}
            {(() => {
              // Show dropdown if position has stages available
              if (!position || availableStages.length === 0) {
                return null;
              }

              // Get current stage
              const currentStage = position.stage_id
                ? availableStages.find(s => s.id === position.stage_id)
                : null;

              // Get next stage (next in order)
              const nextStageOption = currentStage
                ? availableStages
                    .filter(s => s.order > currentStage.order && s.is_active)
                    .sort((a, b) => a.order - b.order)[0]
                : null;

              // Get stages that are ROW or HIDDEN/NONE (not visible in columns)
              // Handle both enum and string values for kanban_display
              const hiddenOrRowStages = availableStages.filter((s: WorkflowStage) => {
                if (!s.is_active || s.id === position.stage_id) return false;
                const display = s.kanban_display as string;
                return display === KanbanDisplay.ROW ||
                       display === 'row' ||
                       display === KanbanDisplay.NONE ||
                       display === 'none';
              });

              // Combine next stage and hidden/row stages, removing duplicates
              const stagesToShow = [
                ...(nextStageOption ? [nextStageOption] : []),
                ...hiddenOrRowStages.filter(s => !nextStageOption || s.id !== nextStageOption.id)
              ].sort((a, b) => a.order - b.order);

              if (stagesToShow.length === 0) {
                return null;
              }

              return (
                <div ref={moveToStageDropdownRef} className="relative">
                  <Button
                    onClick={() => setShowMoveToStageDropdown(!showMoveToStageDropdown)}
                    disabled={changingStage}
                    variant="secondary"
                    title="Move to Stage"
                  >
                    <Move className="w-4 h-4 mr-2" />
                    Move to Stage
                    <ChevronDown className="w-4 h-4 ml-2" />
                  </Button>

                  {showMoveToStageDropdown && (
                    <div className="absolute top-full right-0 mt-1 bg-white border border-gray-200 rounded-lg shadow-lg z-10 min-w-[200px]">
                      <div className="py-1">
                        {stagesToShow.map((stage) => (
                          <button
                            key={stage.id}
                            onClick={() => handleMoveToStage(stage.id)}
                            disabled={changingStage}
                            className="flex items-center gap-2 px-3 py-2 text-sm hover:bg-gray-50 w-full text-left disabled:opacity-50 disabled:cursor-not-allowed"
                          >
                            <span
                              className="text-sm"
                              dangerouslySetInnerHTML={{ __html: stage.style?.icon || '' }}
                            />
                            <span className="text-gray-700">
                              {stage.name}
                              {nextStageOption && stage.id === nextStageOption.id && (
                                <span className="ml-2 text-blue-600 text-xs">(Next Stage)</span>
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
        </div>

      </div>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={(value) => setActiveTab(value as any)} className="mb-6">
        <TabsList>
          <TabsTrigger value="info">
            <FileText className="h-4 w-4 mr-2" />
            Information
          </TabsTrigger>
          <TabsTrigger value="comments">
            <MessageSquare className="h-4 w-4 mr-2" />
            Comments
            {pendingCommentsCount > 0 && (
              <Badge className="ml-2" variant="secondary">
                {pendingCommentsCount}
              </Badge>
            )}
          </TabsTrigger>
          <TabsTrigger value="history">
            <History className="h-4 w-4 mr-2" />
            History
          </TabsTrigger>
        </TabsList>

        {/* Tab Content */}
        <TabsContent value="info">
          <Card>
            <CardHeader>
              <CardTitle>Position Information</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Job Details Grid */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {/* Job Category */}
                {position.job_category && (
                  <div>
                    <p className="text-sm text-muted-foreground mb-1">Category</p>
                    <p className="font-medium capitalize">{position.job_category.toLowerCase().replace('_', ' ')}</p>
                  </div>
                )}

                {/* Employment Type */}
                {position.employment_type && (
                  <div>
                    <p className="text-sm text-muted-foreground mb-1">Employment Type</p>
                    <EmploymentTypeBadge type={position.employment_type} size="sm" />
                  </div>
                )}

                {/* Experience Level */}
                {position.experience_level && (
                  <div>
                    <p className="text-sm text-muted-foreground mb-1">Experience Level</p>
                    <ExperienceLevelBadge level={position.experience_level} size="sm" />
                  </div>
                )}

                {/* Work Location */}
                {position.work_location_type && (
                  <div>
                    <p className="text-sm text-muted-foreground mb-1">Work Location</p>
                    <LocationTypeBadge type={position.work_location_type} size="sm" />
                    {position.office_locations && position.office_locations.length > 0 && (
                      <p className="text-xs text-muted-foreground mt-1">
                        {position.office_locations.join(', ')}
                      </p>
                    )}
                  </div>
                )}

                {/* Salary Range - always show for company users */}
                {(position.salary_min || position.salary_max) && (
                  <div>
                    <p className="text-sm text-muted-foreground mb-1">
                      Salary Range
                      {!position.show_salary && <span className="text-xs ml-1">(hidden from public)</span>}
                    </p>
                    <SalaryRange
                      min={position.salary_min}
                      max={position.salary_max}
                      currency={position.salary_currency}
                      period={position.salary_period}
                    />
                  </div>
                )}

                {/* Budget Max */}
                {position.budget_max && (
                  <div>
                    <p className="text-sm text-muted-foreground mb-1">Budget Max</p>
                    <p className="font-medium">
                      {position.salary_currency || 'USD'} {position.budget_max.toLocaleString()}
                    </p>
                  </div>
                )}

                {/* Approved Budget */}
                {position.approved_budget_max && (
                  <div>
                    <p className="text-sm text-muted-foreground mb-1">Approved Budget</p>
                    <p className="font-medium text-green-600">
                      {position.salary_currency || 'USD'} {position.approved_budget_max.toLocaleString()}
                    </p>
                    {position.approved_at && (
                      <p className="text-xs text-muted-foreground">
                        Approved {new Date(position.approved_at).toLocaleDateString()}
                      </p>
                    )}
                  </div>
                )}

                {/* Department */}
                {position.department_id && (
                  <div>
                    <p className="text-sm text-muted-foreground mb-1">Department</p>
                    <p className="font-medium">{position.department_id}</p>
                  </div>
                )}

                {/* Number of Openings */}
                {position.number_of_openings && position.number_of_openings > 1 && (
                  <div>
                    <p className="text-sm text-muted-foreground mb-1">Openings</p>
                    <div className="flex items-center gap-2">
                      <Users className="w-4 h-4 text-muted-foreground" />
                      <span className="font-medium">{position.number_of_openings}</span>
                    </div>
                  </div>
                )}

                {/* Requisition ID */}
                {position.requisition_id && (
                  <div>
                    <p className="text-sm text-muted-foreground mb-1">Requisition ID</p>
                    <p className="font-mono text-sm">{position.requisition_id}</p>
                  </div>
                )}

                {/* Visibility */}
                {position.visibility && (
                  <div>
                    <p className="text-sm text-muted-foreground mb-1">Visibility</p>
                    <Badge className={getVisibilityColor(position.visibility)}>
                      {getVisibilityLabel(position.visibility)}
                    </Badge>
                  </div>
                )}

                {/* Application Deadline */}
                {position.application_deadline && (
                  <div>
                    <p className="text-sm text-muted-foreground mb-1">Application Deadline</p>
                    <p className="font-medium">
                      {new Date(position.application_deadline).toLocaleDateString()}
                    </p>
                  </div>
                )}

                {/* Open At */}
                {position.open_at && (
                  <div>
                    <p className="text-sm text-muted-foreground mb-1">Open At</p>
                    <p className="font-medium">
                      {new Date(position.open_at).toLocaleDateString()}
                    </p>
                  </div>
                )}

                {/* Killer Questions Indicator */}
                {((position.killer_questions && position.killer_questions.length > 0) || position.screening_template_id) && (
                  <div>
                    <p className="text-sm text-muted-foreground mb-1">Screening</p>
                    <div className="flex flex-col gap-1">
                      {position.killer_questions && position.killer_questions.length > 0 && (
                        <Badge variant="secondary" className="w-fit">
                          {position.killer_questions.length} Killer Question{position.killer_questions.length > 1 ? 's' : ''}
                        </Badge>
                      )}
                      {position.screening_template_id && (
                        <Badge variant="outline" className="w-fit">
                          Screening Template
                        </Badge>
                      )}
                    </div>
                  </div>
                )}
              </div>

              {/* Description */}
              {position.description && (
                <>
                  <div className="border-t pt-4">
                    <p className="text-sm font-medium text-muted-foreground mb-2">Description</p>
                    <div
                      className="prose prose-sm max-w-none"
                      dangerouslySetInnerHTML={{ __html: position.description }}
                    />
                  </div>
                </>
              )}

              {/* Skills */}
              {position.skills && position.skills.length > 0 && (
                <div className="border-t pt-4">
                  <p className="text-sm font-medium text-muted-foreground mb-2">Skills</p>
                  <SkillsChips skills={position.skills} />
                </div>
              )}

              {/* Languages */}
              {position.languages && position.languages.length > 0 && (
                <div className="border-t pt-4">
                  <p className="text-sm font-medium text-muted-foreground mb-2">Languages</p>
                  <LanguagesList languages={position.languages} />
                </div>
              )}

              {/* Requirements */}
              {(() => {
                const requirements = getRequirements(position);
                return requirements && requirements.length > 0 && (
                  <div className="border-t pt-4">
                    <p className="text-sm font-medium text-muted-foreground mb-2">Requirements</p>
                    <ul className="space-y-1">
                      {requirements.map((req: string, idx: number) => (
                        <li key={idx} className="flex items-start gap-2 text-sm">
                          <span className="text-primary mt-0.5">•</span>
                          <span>{req}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                );
              })()}

              {/* Benefits */}
              {(() => {
                const benefits = getBenefits(position);
                return benefits && benefits.length > 0 && (
                  <div className="border-t pt-4">
                    <p className="text-sm font-medium text-muted-foreground mb-2">Benefits</p>
                    <ul className="space-y-1">
                      {benefits.map((benefit: string, idx: number) => (
                        <li key={idx} className="flex items-start gap-2 text-sm">
                          <span className="text-green-600 mt-0.5">✓</span>
                          <span>{benefit}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                );
              })()}

              {/* Candidate Visible Fields from Recruitment Workflows */}
              {candidateVisibleFields.length > 0 && (
                <div className="border-t pt-4">
                  <p className="text-sm font-medium text-muted-foreground mb-2">Additional Information (Candidate Visible)</p>
                  <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                    {candidateVisibleFields.map((field) => {
                      const value = position.custom_fields_values?.[field.field_key];
                      return (
                        <div key={field.field_key}>
                          <p className="text-xs text-muted-foreground mb-1">
                            {field.label}
                            {field.is_required && <span className="text-red-500 ml-1">*</span>}
                          </p>
                          <p className="font-medium">
                            {value !== undefined && value !== null && value !== ''
                              ? (field.field_type === 'BOOLEAN'
                                  ? (value ? 'Yes' : 'No')
                                  : field.field_type === 'MULTISELECT' && Array.isArray(value)
                                    ? value.join(', ')
                                    : String(value))
                              : <span className="text-muted-foreground italic">Not set</span>}
                          </p>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}

              {/* Team */}
              {(position.hiring_manager_id || position.recruiter_id) && (
                <div className="border-t pt-4">
                  <p className="text-sm font-medium text-muted-foreground mb-2">Team</p>
                  <div className="flex gap-6">
                    {position.hiring_manager_id && (
                      <div>
                        <p className="text-xs text-muted-foreground">Hiring Manager</p>
                        <p className="font-medium">{position.hiring_manager_id}</p>
                      </div>
                    )}
                    {position.recruiter_id && (
                      <div>
                        <p className="text-xs text-muted-foreground">Recruiter</p>
                        <p className="font-medium">{position.recruiter_id}</p>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Workflow Info */}
              {workflow && (
                <div className="border-t pt-4">
                  <p className="text-sm font-medium text-muted-foreground mb-2">Workflow</p>
                  <div className="flex items-center gap-4">
                    <div className="flex items-center gap-2">
                      <Workflow className="w-4 h-4 text-muted-foreground" />
                      <span className="font-medium">{workflow.name}</span>
                    </div>
                    {position.stage_id && position.stage && (
                      <div className="flex items-center gap-2">
                        <span
                          className="text-lg"
                          dangerouslySetInnerHTML={{ __html: position.stage.icon }}
                        />
                        <span>{position.stage.name}</span>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Timestamps */}
              <div className="border-t pt-4 text-xs text-muted-foreground">
                <div className="flex gap-6">
                  {position.created_at && (
                    <span>Created: {new Date(position.created_at).toLocaleDateString()}</span>
                  )}
                  {position.updated_at && (
                    <span>Updated: {new Date(position.updated_at).toLocaleDateString()}</span>
                  )}
                  {position.public_slug && (
                    <span>Slug: <code className="font-mono">{position.public_slug}</code></span>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Job Position Approval Additional Info - Custom Fields from Publication Workflow */}
          {publicationWorkflowFields.length > 0 && (
            <Card className="mt-4">
              <CardHeader>
                <CardTitle className="text-base">Job Position Approval Additional Info</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                  {publicationWorkflowFields.map((field) => {
                    const value = position.custom_fields_values?.[field.field_key];
                    return (
                      <div key={field.field_key}>
                        <p className="text-xs text-muted-foreground mb-1">{field.label}</p>
                        <p className="font-medium">
                          {value !== undefined && value !== null && value !== ''
                            ? (field.field_type === 'BOOLEAN'
                                ? (value ? 'Yes' : 'No')
                                : field.field_type === 'MULTISELECT' && Array.isArray(value)
                                  ? value.join(', ')
                                  : String(value))
                            : <span className="text-muted-foreground italic">Not set</span>}
                        </p>
                      </div>
                    );
                  })}
                </div>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        {/* Comments Tab */}
        <TabsContent value="comments">
          <Card>
            <CardHeader>
              <CardTitle>Comments</CardTitle>
            </CardHeader>
            <CardContent>
              {position.stage_id ? (
                <PositionCommentsSection
                  positionId={id!}
                  workflowId={position.job_position_workflow_id || undefined}
                  currentStageId={position.stage_id || undefined}
                  onCommentsChange={async () => {
                    await loadPendingCommentsCount();
                    setCommentsRefreshKey(prev => prev + 1);
                  }}
                  refreshKey={commentsRefreshKey}
                  defaultExpanded={true}
                />
              ) : (
                <p className="text-muted-foreground">Comments are available when the position has a stage assigned.</p>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* History Tab */}
        <TabsContent value="history">
          <Card>
            <CardHeader>
              <CardTitle>Activity History</CardTitle>
            </CardHeader>
            <CardContent>
              <JobPositionActivityTimeline
                activities={activities}
                isLoading={loadingActivities}
              />
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Comments Section - Always visible at the bottom, like in CandidateDetailPage */}
      {position.stage_id && (
        <div className="mt-6">
          <PositionCommentsSection
            positionId={id!}
            workflowId={position.job_position_workflow_id || undefined}
            currentStageId={position.stage_id || undefined}
            onCommentsChange={async () => {
              await loadPendingCommentsCount();
              setCommentsRefreshKey(prev => prev + 1);
            }}
            refreshKey={commentsRefreshKey}
            onNavigateToCommentsTab={() => setActiveTab('comments')}
          />
        </div>
      )}
    </div>
  );
}
