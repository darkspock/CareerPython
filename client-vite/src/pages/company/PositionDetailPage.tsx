import { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Edit, Workflow, Eye, EyeOff, FileText, MessageSquare, History, Move, ChevronDown } from 'lucide-react';
import { PositionService } from '../../services/positionService';
import type { Position, JobPositionWorkflow } from '../../types/position';
import { 
  getStatusColorFromStage,
  getStatusLabelFromStage,
  getDepartment,
  getRequirements,
  getBenefits,
  getSkills
} from '../../types/position';
import { DynamicCustomFields } from '../../components/jobPosition/DynamicCustomFields';
import { PositionCommentsSection } from '../../components/jobPosition/PositionCommentsSection';
import { JobPositionActivityTimeline } from '../../components/jobPosition/JobPositionActivityTimeline';
import JobPositionActivityService from '../../services/JobPositionActivityService';
import JobPositionCommentService from '../../services/JobPositionCommentService';
import type { JobPositionActivity } from '../../types/jobPositionActivity';
import { companyWorkflowService } from '../../services/companyWorkflowService';
import type { WorkflowStage } from '../../types/workflow';
import { KanbanDisplay } from '../../types/workflow';

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
        } catch (err) {
          console.error('Error loading workflow:', err);
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
      <div className="bg-red-50 border border-red-200 rounded-lg p-6">
        <p className="text-red-800">{error || 'Position not found'}</p>
        <button
          onClick={() => navigate('/company/positions')}
          className="mt-4 flex items-center gap-2 text-red-700 hover:text-red-900"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Positions
        </button>
      </div>
    );
  }

  return (
    <div>
      {/* Header */}
      <div className="mb-6">
        <button
          onClick={() => navigate('/company/positions')}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-4"
        >
          <ArrowLeft className="w-5 h-5" />
          Back to Positions
        </button>

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
            {position.stage && (
              <span className={`px-3 py-1 text-sm font-medium rounded-full ${getStatusColorFromStage(position.stage)}`}>
                {getStatusLabelFromStage(position.stage)}
              </span>
            )}
            <span className={`px-3 py-1 text-sm font-medium rounded-full ${getVisibilityColor(position.visibility)}`}>
              {position.visibility === 'public' ? <Eye className="w-3 h-3 inline mr-1" /> : <EyeOff className="w-3 h-3 inline mr-1" />}
              {getVisibilityLabel(position.visibility)}
            </span>
            <button
              onClick={() => navigate(`/company/positions/${id}/edit`)}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              title="Edit this position"
            >
              <Edit className="w-4 h-4" />
              Edit
            </button>
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
                  <button
                    onClick={() => setShowMoveToStageDropdown(!showMoveToStageDropdown)}
                    disabled={changingStage}
                    className="flex items-center gap-2 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                    title="Move to Stage"
                  >
                    <Move className="w-4 h-4" />
                    Move to Stage
                    <ChevronDown className="w-4 h-4" />
                  </button>
                  
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
      <div className="mb-6 border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          <button
            onClick={() => setActiveTab('info')}
            className={`py-3 px-1 border-b-2 font-medium text-sm flex items-center gap-2 ${
              activeTab === 'info'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            <FileText className="h-4 w-4" />
            <span>Information</span>
          </button>

          <button
            onClick={() => setActiveTab('comments')}
            className={`py-3 px-1 border-b-2 font-medium text-sm flex items-center gap-2 ${
              activeTab === 'comments'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            <MessageSquare className="h-4 w-4" />
            <span>Comments</span>
            {pendingCommentsCount > 0 && (
              <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                {pendingCommentsCount}
              </span>
            )}
          </button>

          <button
            onClick={() => setActiveTab('history')}
            className={`py-3 px-1 border-b-2 font-medium text-sm flex items-center gap-2 ${
              activeTab === 'history'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            <History className="h-4 w-4" />
            <span>History</span>
          </button>
        </nav>
      </div>

      {/* Tab Content */}
      {activeTab === 'info' && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-6">
          {/* Description */}
          {position.description && (
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Description</h2>
              <div 
                className="text-gray-700 prose prose-sm max-w-none"
                dangerouslySetInnerHTML={{ __html: position.description || '' }}
              />
            </div>
          )}

          {/* Custom Fields */}
          {workflow && position.custom_fields_values && Object.keys(position.custom_fields_values).length > 0 && (
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Custom Fields</h2>
              <DynamicCustomFields
                workflow={workflow}
                currentStage={position.stage || null}
                customFieldsValues={position.custom_fields_values || {}}
                onChange={() => {}} // Read-only in detail view
                readOnly={true}
              />
            </div>
          )}

          {/* Requirements */}
          {(() => {
            const requirements = getRequirements(position);
            return requirements && requirements.length > 0 && (
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">Requirements</h2>
                <ul className="space-y-2">
                  {requirements.map((req: string, idx: number) => (
                    <li key={idx} className="flex items-start gap-2">
                      <span className="text-blue-600 mt-1">•</span>
                      <span className="text-gray-700">{req}</span>
                    </li>
                  ))}
                </ul>
              </div>
            );
          })()}

          {/* Skills */}
          {(() => {
            const skills = getSkills(position);
            return skills && skills.length > 0 && (
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">Required Skills</h2>
                <div className="flex flex-wrap gap-2">
                  {skills.map((skill: string, idx: number) => (
                    <span
                      key={idx}
                      className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            );
          })()}

          {/* Benefits */}
          {(() => {
            const benefits = getBenefits(position);
            return benefits && benefits.length > 0 && (
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">Benefits</h2>
                <ul className="space-y-2">
                  {benefits.map((benefit: string, idx: number) => (
                    <li key={idx} className="flex items-start gap-2">
                      <span className="text-green-600 mt-1">✓</span>
                      <span className="text-gray-700">{benefit}</span>
                    </li>
                  ))}
                </ul>
              </div>
            );
          })()}
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Workflow & Stage Info */}
          {workflow && (
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Workflow Information</h3>
              <div className="space-y-3">
                <div>
                  <p className="text-sm text-gray-600">Workflow</p>
                  <p className="font-medium text-gray-900">{workflow.name}</p>
                </div>
                {position.stage_id && position.stage && (
                  <div>
                    <p className="text-sm text-gray-600">Current Stage</p>
                    <div className="flex items-center gap-2 mt-1">
                      <span 
                        className="text-lg"
                        dangerouslySetInnerHTML={{ __html: position.stage.icon }}
                      />
                      <p className="font-medium text-gray-900">{position.stage.name}</p>
                    </div>
                    <p className="text-xs text-gray-500 mt-1">Status: {position.stage.status_mapping}</p>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Basic Details */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Basic Information</h3>
            <div className="grid grid-cols-2 gap-4">
              {position.job_category && (
                <div>
                  <p className="text-sm text-gray-600">Job Category</p>
                  <p className="font-medium text-gray-900 capitalize">{position.job_category.toLowerCase().replace('_', ' ')}</p>
                </div>
              )}

              {position.visibility && (
                <div>
                  <p className="text-sm text-gray-600">Visibility</p>
                  <span className={`inline-block px-2 py-1 text-xs font-medium rounded-full ${getVisibilityColor(position.visibility)}`}>
                    {getVisibilityLabel(position.visibility)}
                  </span>
                </div>
              )}

              {position.open_at && (
                <div>
                  <p className="text-sm text-gray-600">Open At</p>
                  <p className="font-medium text-gray-900">
                    {new Date(position.open_at).toLocaleDateString()} {new Date(position.open_at).toLocaleTimeString()}
                  </p>
                </div>
              )}

              {position.application_deadline && (
                <div>
                  <p className="text-sm text-gray-600">Application Deadline</p>
                  <p className="font-medium text-gray-900">
                    {new Date(position.application_deadline).toLocaleDateString()}
                  </p>
                </div>
              )}

              {position.public_slug && (
                <div className="col-span-2">
                  <p className="text-sm text-gray-600">Public Slug</p>
                  <p className="font-medium text-gray-900 font-mono text-sm">{position.public_slug}</p>
                </div>
              )}

              {position.created_at && (
                <div>
                  <p className="text-sm text-gray-600">Created</p>
                  <p className="font-medium text-gray-900">
                    {new Date(position.created_at).toLocaleDateString()} {new Date(position.created_at).toLocaleTimeString()}
                  </p>
                </div>
              )}

              {position.updated_at && (
                <div>
                  <p className="text-sm text-gray-600">Last Updated</p>
                  <p className="font-medium text-gray-900">
                    {new Date(position.updated_at).toLocaleDateString()} {new Date(position.updated_at).toLocaleTimeString()}
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
        </div>
      )}

      {/* Comments Tab */}
      {activeTab === 'comments' && position.stage_id && (
        <div>
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
        </div>
      )}

      {/* History Tab */}
      {activeTab === 'history' && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-6">Activity History</h2>
          <JobPositionActivityTimeline
            activities={activities}
            isLoading={loadingActivities}
          />
        </div>
      )}

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
