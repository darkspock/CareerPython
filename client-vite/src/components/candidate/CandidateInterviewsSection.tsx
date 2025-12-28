import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useCompanyNavigation } from '../../hooks/useCompanyNavigation';
import { toast } from 'react-toastify';
import { Plus, ChevronDown, ChevronRight, Calendar, User, AlertCircle, Clock, CheckCircle, X, Ban } from 'lucide-react';
import { useCandidateInterviews } from '../../hooks/useCandidateInterviews';
import { companyWorkflowService } from '../../services/companyWorkflowService';
import { companyInterviewService } from '../../services/companyInterviewService';
import AssignInterviewModal from './AssignInterviewModal';
import type { WorkflowStage } from '../../types/workflow';
import type { Interview } from '../../services/companyInterviewService';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import LoadingSpinner from '@/components/common/LoadingSpinner';
import EmptyState from '@/components/common/EmptyState';

interface CandidateInterviewsSectionProps {
  candidateId: string;
  companyCandidateId: string;
  currentStageId: string | null | undefined;
  currentWorkflowId: string | null | undefined;
  availableStages: WorkflowStage[];
  jobPositionId?: string;
}

export default function CandidateInterviewsSection({
  candidateId,
  companyCandidateId,
  currentStageId,
  currentWorkflowId,
  availableStages,
  jobPositionId,
}: CandidateInterviewsSectionProps) {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { getPath } = useCompanyNavigation();
  const [showOtherStages, setShowOtherStages] = useState(false);
  const [showAssignModal, setShowAssignModal] = useState(false);
  const [showPositionError, setShowPositionError] = useState(false);
  const [workflowStages, setWorkflowStages] = useState<WorkflowStage[]>(availableStages);
  const [_loadingStages, setLoadingStages] = useState(false);

  const handleAssignClick = () => {
    if (!jobPositionId) {
      setShowPositionError(true);
      setTimeout(() => setShowPositionError(false), 5000);
      return;
    }
    setShowAssignModal(true);
  };

  const interviewsHook = useCandidateInterviews({
    candidateId,
    companyCandidateId,
    currentStageId,
  });

  // Load stages from current workflow
  useEffect(() => {
    const loadWorkflowStages = async () => {
      setLoadingStages(true);
      try {
        if (currentWorkflowId) {
          const stages = await companyWorkflowService.listStagesByWorkflow(currentWorkflowId);
          setWorkflowStages(stages as WorkflowStage[]);
        } else {
          setWorkflowStages(availableStages);
        }
      } catch {
        setWorkflowStages(availableStages);
      } finally {
        setLoadingStages(false);
      }
    };

    loadWorkflowStages();
  }, [currentWorkflowId, availableStages]);

  const currentStageName = workflowStages.find(s => s.id === currentStageId)?.name || t('company.interviews.currentStage');

  // Helper to get status icon
  const getStatusIcon = useCallback((status: string) => {
    switch (status.toUpperCase()) {
      case 'PENDING':
        return <Clock className="w-4 h-4 text-yellow-600" />;
      case 'IN_PROGRESS':
        return <AlertCircle className="w-4 h-4 text-blue-600" />;
      case 'PAUSED':
        return <Clock className="w-4 h-4 text-orange-600" />;
      case 'FINISHED':
        return <CheckCircle className="w-4 h-4 text-green-600" />;
      case 'DISCARDED':
        return <X className="w-4 h-4 text-red-600" />;
      default:
        return <Clock className="w-4 h-4 text-muted-foreground" />;
    }
  }, []);

  // Helper to get status variant
  const getStatusVariant = useCallback((status: string): "default" | "secondary" | "destructive" | "outline" => {
    switch (status.toUpperCase()) {
      case 'PENDING':
      case 'IN_PROGRESS':
      case 'PAUSED':
        return 'secondary';
      case 'FINISHED':
        return 'default';
      case 'DISCARDED':
        return 'destructive';
      default:
        return 'outline';
    }
  }, []);

  // Helper to format date
  const formatDate = useCallback((dateString?: string) => {
    if (!dateString) return null;
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString(undefined, {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    } catch {
      return null;
    }
  }, []);

  // Handle cancel interview
  const handleCancelInterview = async (interview: Interview) => {
    if (!window.confirm(t('company.interviews.confirmCancel', {
      defaultValue: 'Are you sure you want to cancel this interview? This action cannot be undone.'
    }))) {
      return;
    }

    try {
      await companyInterviewService.cancelInterview(interview.id);
      toast.success(t('company.interviews.cancelSuccess', {
        defaultValue: 'Interview cancelled successfully'
      }));
      interviewsHook.loadInterviews();
    } catch (err: any) {
      toast.error(t('company.interviews.cancelError', {
        message: err.message,
        defaultValue: `Error cancelling interview: ${err.message}`
      }));
    }
  };

  // Render single interview card
  const renderInterviewCard = (interview: Interview) => {
    const formattedDate = formatDate(interview.scheduled_at);

    return (
      <Card key={interview.id} className="hover:border-primary/50 transition-colors">
        <CardContent className="pt-4">
          <div className="flex items-start justify-between gap-4">
            <div className="flex-1">
              {/* Header: Type + Status */}
              <div className="flex items-center gap-2 mb-2">
                <span className="font-medium text-foreground">
                  {t(`company.interviews.types.${interview.interview_type}`, { defaultValue: interview.interview_type })}
                </span>
                <Badge variant={getStatusVariant(interview.status)} className="gap-1">
                  {getStatusIcon(interview.status)}
                  {t(`company.interviews.status.${interview.status}`, { defaultValue: interview.status })}
                </Badge>
              </div>

              {/* Stage name */}
              {interview.workflow_stage_name && (
                <div className="text-sm text-muted-foreground mb-2">
                  <span className="font-medium">{t('company.interviews.stage')}:</span> {interview.workflow_stage_name}
                </div>
              )}

              {/* Template name */}
              {interview.interview_template_name && (
                <div className="text-sm text-muted-foreground mb-2">
                  <span className="font-medium">{t('company.interviews.template')}:</span> {interview.interview_template_name}
                </div>
              )}

              {/* Scheduled date */}
              {formattedDate && (
                <div className="flex items-center gap-1 text-sm text-muted-foreground mb-2">
                  <Calendar className="w-4 h-4" />
                  <span>{formattedDate}</span>
                </div>
              )}

              {/* Required roles */}
              {interview.required_role_names && interview.required_role_names.length > 0 && (
                <div className="text-sm text-muted-foreground mb-2">
                  <span className="font-medium">{t('company.interviews.requiredRoles')}:</span>{' '}
                  {interview.required_role_names.join(', ')}
                </div>
              )}

              {/* Interviewers */}
              {interview.interviewer_names && interview.interviewer_names.length > 0 && (
                <div className="flex items-center gap-1 text-sm text-muted-foreground">
                  <User className="w-4 h-4" />
                  <span>{interview.interviewer_names.join(', ')}</span>
                </div>
              )}
            </div>

            {/* Actions */}
            <div className="flex flex-col items-end gap-2">
              <Button
                variant="link"
                size="sm"
                onClick={() => {
                  navigate(getPath(`interviews/${interview.id}`));
                }}
                className="h-auto p-0"
              >
                {t('company.interviews.viewDetails')}
              </Button>
              {!['DISCARDED', 'FINISHED'].includes(interview.status.toUpperCase()) && (
                <Button
                  variant="link"
                  size="sm"
                  onClick={() => handleCancelInterview(interview)}
                  className="h-auto p-0 text-destructive hover:text-destructive"
                >
                  <Ban className="w-4 h-4 mr-1" />
                  {t('company.interviews.cancel', { defaultValue: 'Cancel' })}
                </Button>
              )}
            </div>
          </div>
        </CardContent>
      </Card>
    );
  };

  if (interviewsHook.loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <LoadingSpinner size="lg" color="blue" />
      </div>
    );
  }

  if (interviewsHook.error) {
    return (
      <Alert variant="destructive">
        <AlertCircle className="h-4 w-4" />
        <AlertTitle>{t('company.interviews.errorLoading')}</AlertTitle>
        <AlertDescription>{interviewsHook.error}</AlertDescription>
      </Alert>
    );
  }

  return (
    <div className="space-y-6">
      {/* Job Position Required Error */}
      {showPositionError && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertTitle>
            {t('company.interviews.errors.jobPositionRequired', { defaultValue: 'This candidate must be associated with a job position to assign interviews' })}
          </AlertTitle>
          <AlertDescription>
            {t('company.interviews.errors.assignPositionFirst', { defaultValue: 'Please assign this candidate to a job position first from the candidate details.' })}
          </AlertDescription>
          <Button
            variant="ghost"
            size="icon"
            className="absolute right-2 top-2"
            onClick={() => setShowPositionError(false)}
          >
            <X className="h-4 w-4" />
          </Button>
        </Alert>
      )}

      {/* Header with Assign button */}
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold text-foreground">
          {t('company.interviews.title')}
        </h2>
        <Button
          onClick={handleAssignClick}
          title={!jobPositionId ? t('company.interviews.errors.jobPositionRequired', { defaultValue: 'This candidate must be associated with a job position to assign interviews' }) : ''}
        >
          <Plus className="w-4 h-4 mr-2" />
          {t('company.interviews.assignInterview')}
        </Button>
      </div>

      {/* Current Stage Interviews */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">
            {t('company.interviews.currentStageInterviews', { stage: currentStageName })}
          </CardTitle>
        </CardHeader>
        <CardContent>
          {interviewsHook.currentStageInterviews.length === 0 ? (
            <EmptyState
              icon={AlertCircle}
              title={t('company.interviews.noInterviewsInCurrentStage')}
              size="sm"
            />
          ) : (
            <div className="space-y-3">
              {interviewsHook.currentStageInterviews.map(interview => renderInterviewCard(interview))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Other Stages Interviews (collapsible) */}
      {interviewsHook.otherStagesInterviews.length > 0 && (
        <Card>
          <button
            onClick={() => setShowOtherStages(!showOtherStages)}
            className="w-full flex items-center justify-between p-6 text-left hover:bg-muted/50 transition-colors"
          >
            <h3 className="text-lg font-semibold text-foreground">
              {t('company.interviews.otherStagesInterviews')} ({interviewsHook.otherStagesInterviews.length})
            </h3>
            {showOtherStages ? (
              <ChevronDown className="w-5 h-5 text-muted-foreground" />
            ) : (
              <ChevronRight className="w-5 h-5 text-muted-foreground" />
            )}
          </button>

          {showOtherStages && (
            <CardContent className="pt-0 border-t">
              <div className="space-y-3 pt-4">
                {interviewsHook.otherStagesInterviews.map(interview => renderInterviewCard(interview))}
              </div>
            </CardContent>
          )}
        </Card>
      )}

      {/* No interviews at all */}
      {interviewsHook.allInterviews.length === 0 && (
        <Card>
          <CardContent className="py-12">
            <EmptyState
              icon={AlertCircle}
              title={t('company.interviews.noInterviews')}
              description={t('company.interviews.noInterviewsDescription')}
              actionLabel={t('company.interviews.assignFirstInterview')}
              onAction={handleAssignClick}
              actionIcon={Plus}
              size="lg"
            />
          </CardContent>
        </Card>
      )}

      {/* Assign Interview Modal */}
      <AssignInterviewModal
        candidateId={candidateId}
        companyCandidateId={companyCandidateId}
        currentStageId={currentStageId}
        currentWorkflowId={currentWorkflowId}
        availableStages={workflowStages}
        jobPositionId={jobPositionId}
        isOpen={showAssignModal}
        onClose={() => setShowAssignModal(false)}
        onSuccess={() => {
          interviewsHook.loadInterviews();
        }}
      />
    </div>
  );
}
