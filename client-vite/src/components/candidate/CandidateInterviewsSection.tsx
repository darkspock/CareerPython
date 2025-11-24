import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { toast } from 'react-toastify';
import { Plus, ChevronDown, ChevronRight, Calendar, User, AlertCircle, Clock, CheckCircle, X, Ban } from 'lucide-react';
import { useCandidateInterviews } from '../../hooks/useCandidateInterviews';
import { companyWorkflowService } from '../../services/companyWorkflowService';
import { companyInterviewService } from '../../services/companyInterviewService';
import AssignInterviewModal from './AssignInterviewModal';
import type { WorkflowStage } from '../../types/workflow';
import type { Interview } from '../../services/companyInterviewService';

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
  const [showOtherStages, setShowOtherStages] = useState(false);
  const [showAssignModal, setShowAssignModal] = useState(false);
  const [showPositionError, setShowPositionError] = useState(false);
  const [workflowStages, setWorkflowStages] = useState<WorkflowStage[]>(availableStages);
  const [loadingStages, setLoadingStages] = useState(false);

  const handleAssignClick = () => {
    console.log('🔍 DEBUG: jobPositionId =', jobPositionId);
    if (!jobPositionId) {
      console.warn('⚠️ No jobPositionId provided');
      setShowPositionError(true);
      setTimeout(() => setShowPositionError(false), 5000); // Auto-hide after 5 seconds
      return;
    }
    console.log('✅ Opening assign interview modal with jobPositionId:', jobPositionId);
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
          // Have specific workflow, load its stages
          const stages = await companyWorkflowService.listStagesByWorkflow(currentWorkflowId);
          setWorkflowStages(stages as WorkflowStage[]);
        } else {
          // No workflow, use available stages from props
          setWorkflowStages(availableStages);
        }
      } catch (err) {
        console.error('Error loading workflow stages:', err);
        setWorkflowStages(availableStages);
      } finally {
        setLoadingStages(false);
      }
    };

    loadWorkflowStages();
  }, [currentWorkflowId, availableStages]);

  const currentStageName = workflowStages.find(s => s.id === currentStageId)?.name || t('company.interviews.currentStage');

  // Helper to get status icon
  const getStatusIcon = (status: string) => {
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
        return <Clock className="w-4 h-4 text-gray-600" />;
    }
  };

  // Helper to get status color
  const getStatusColor = (status: string) => {
    switch (status.toUpperCase()) {
      case 'PENDING':
        return 'bg-yellow-100 text-yellow-800';
      case 'IN_PROGRESS':
        return 'bg-blue-100 text-blue-800';
      case 'PAUSED':
        return 'bg-orange-100 text-orange-800';
      case 'FINISHED':
        return 'bg-green-100 text-green-800';
      case 'DISCARDED':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  // Helper to format date
  const formatDate = (dateString?: string) => {
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
  };

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
      // Reload interviews
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
      <div
        key={interview.id}
        className="border border-gray-200 rounded-lg p-4 hover:border-gray-300 transition-colors"
      >
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1">
            {/* Header: Type + Status */}
            <div className="flex items-center gap-2 mb-2">
              <span className="font-medium text-gray-900">
                {t(`company.interviews.types.${interview.interview_type}`, { defaultValue: interview.interview_type })}
              </span>
              <span className={`inline-flex items-center gap-1 px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(interview.status)}`}>
                {getStatusIcon(interview.status)}
                {t(`company.interviews.status.${interview.status}`, { defaultValue: interview.status })}
              </span>
            </div>

            {/* Stage name */}
            {interview.workflow_stage_name && (
              <div className="text-sm text-gray-600 mb-2">
                <span className="font-medium">{t('company.interviews.stage')}:</span> {interview.workflow_stage_name}
              </div>
            )}

            {/* Template name */}
            {interview.interview_template_name && (
              <div className="text-sm text-gray-500 mb-2">
                <span className="font-medium">{t('company.interviews.template')}:</span> {interview.interview_template_name}
              </div>
            )}

            {/* Scheduled date */}
            {formattedDate && (
              <div className="flex items-center gap-1 text-sm text-gray-600 mb-2">
                <Calendar className="w-4 h-4" />
                <span>{formattedDate}</span>
              </div>
            )}

            {/* Required roles */}
            {interview.required_role_names && interview.required_role_names.length > 0 && (
              <div className="text-sm text-gray-600 mb-2">
                <span className="font-medium">{t('company.interviews.requiredRoles')}:</span>{' '}
                {interview.required_role_names.join(', ')}
              </div>
            )}

            {/* Interviewers */}
            {interview.interviewer_names && interview.interviewer_names.length > 0 && (
              <div className="flex items-center gap-1 text-sm text-gray-600">
                <User className="w-4 h-4" />
                <span>{interview.interviewer_names.join(', ')}</span>
              </div>
            )}
          </div>

          {/* Actions */}
          <div className="flex flex-col items-end gap-2">
            <button
              onClick={() => {
                // TODO: Navigate to interview detail
                window.location.href = `/company/interviews/${interview.id}`;
              }}
              className="text-sm text-blue-600 hover:text-blue-700 font-medium"
            >
              {t('company.interviews.viewDetails')}
            </button>
            {/* Only show cancel button if interview is not already cancelled or completed */}
            {!['DISCARDED', 'FINISHED'].includes(interview.status.toUpperCase()) && (
              <button
                onClick={() => handleCancelInterview(interview)}
                className="flex items-center gap-1 text-sm text-red-600 hover:text-red-700 font-medium"
                title={t('company.interviews.cancelInterview', { defaultValue: 'Cancel Interview' })}
              >
                <Ban className="w-4 h-4" />
                {t('company.interviews.cancel', { defaultValue: 'Cancel' })}
              </button>
            )}
          </div>
        </div>
      </div>
    );
  };

  if (interviewsHook.loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (interviewsHook.error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <div className="flex items-start gap-3">
          <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
          <div>
            <h3 className="text-sm font-medium text-red-800">
              {t('company.interviews.errorLoading')}
            </h3>
            <p className="text-sm text-red-600 mt-1">{interviewsHook.error}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Job Position Required Error */}
      {showPositionError && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex items-start gap-3">
            <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
            <div className="flex-1">
              <p className="text-sm font-medium text-red-800">
                {t('company.interviews.errors.jobPositionRequired', { defaultValue: 'This candidate must be associated with a job position to assign interviews' })}
              </p>
              <p className="text-sm text-red-600 mt-1">
                {t('company.interviews.errors.assignPositionFirst', { defaultValue: 'Please assign this candidate to a job position first from the candidate details.' })}
              </p>
            </div>
            <button
              onClick={() => setShowPositionError(false)}
              className="text-red-400 hover:text-red-600 transition-colors"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}

      {/* Header with Assign button */}
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold text-gray-900">
          {t('company.interviews.title')}
        </h2>
        <button
          onClick={handleAssignClick}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          title={!jobPositionId ? t('company.interviews.errors.jobPositionRequired', { defaultValue: 'This candidate must be associated with a job position to assign interviews' }) : ''}
        >
          <Plus className="w-4 h-4" />
          {t('company.interviews.assignInterview')}
        </button>
      </div>

      {/* Current Stage Interviews */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          {t('company.interviews.currentStageInterviews', { stage: currentStageName })}
        </h3>

        {interviewsHook.currentStageInterviews.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            <AlertCircle className="w-12 h-12 mx-auto mb-3 text-gray-400" />
            <p>{t('company.interviews.noInterviewsInCurrentStage')}</p>
          </div>
        ) : (
          <div className="space-y-3">
            {interviewsHook.currentStageInterviews.map(interview => renderInterviewCard(interview))}
          </div>
        )}
      </div>

      {/* Other Stages Interviews (collapsible) */}
      {interviewsHook.otherStagesInterviews.length > 0 && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200">
          <button
            onClick={() => setShowOtherStages(!showOtherStages)}
            className="w-full flex items-center justify-between p-6 text-left hover:bg-gray-50 transition-colors"
          >
            <h3 className="text-lg font-semibold text-gray-900">
              {t('company.interviews.otherStagesInterviews')} ({interviewsHook.otherStagesInterviews.length})
            </h3>
            {showOtherStages ? (
              <ChevronDown className="w-5 h-5 text-gray-600" />
            ) : (
              <ChevronRight className="w-5 h-5 text-gray-600" />
            )}
          </button>

          {showOtherStages && (
            <div className="p-6 pt-0 space-y-3 border-t border-gray-200">
              {interviewsHook.otherStagesInterviews.map(interview => renderInterviewCard(interview))}
            </div>
          )}
        </div>
      )}

      {/* No interviews at all */}
      {interviewsHook.allInterviews.length === 0 && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-12">
          <div className="text-center text-gray-500">
            <AlertCircle className="w-16 h-16 mx-auto mb-4 text-gray-400" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              {t('company.interviews.noInterviews')}
            </h3>
            <p className="text-gray-600 mb-4">
              {t('company.interviews.noInterviewsDescription')}
            </p>
            <button
              onClick={handleAssignClick}
              className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              title={!jobPositionId ? t('company.interviews.errors.jobPositionRequired', { defaultValue: 'This candidate must be associated with a job position to assign interviews' }) : ''}
            >
              <Plus className="w-4 h-4" />
              {t('company.interviews.assignFirstInterview')}
            </button>
          </div>
        </div>
      )}

      {/* Assign Interview Modal */}
      {showAssignModal && (
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
      )}
    </div>
  );
}

