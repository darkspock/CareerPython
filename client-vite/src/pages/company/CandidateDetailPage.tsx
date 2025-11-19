import { useState, useEffect, useRef, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import {
  ArrowLeft,
  Plus,
  Paperclip,
  FileText,
  Download,
  Trash2,
  MessageSquare,
  AlertCircle,
  Mail,
  Phone,
} from 'lucide-react';
import { companyCandidateService } from '../../services/companyCandidateService';
import { customFieldValueService } from '../../services/customFieldValueService';
import { StageTimeline } from '../../components/candidate';
import CustomFieldsCard from '../../components/candidate/CustomFieldsCard';
import CandidateCommentsSection from '../../components/candidate/CandidateCommentsSection';
import CandidateReviewsSection from '../../components/candidate/CandidateReviewsSection';
import CandidateHeader from '../../components/candidate/CandidateHeader';
import CandidateSidebar from '../../components/candidate/CandidateSidebar';
import { useCandidateData } from '../../hooks/useCandidateData';
import { useCandidateFiles } from '../../hooks/useCandidateFiles';
import { useCandidateComments } from '../../hooks/useCandidateComments';
import { useWorkflowsWithData } from '../../hooks/useWorkflowsWithData';
import { useCompanyId } from '../../hooks/useCompanyId';

export default function CandidateDetailPage() {
  const { t } = useTranslation();
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState<'info' | 'comments' | 'reviews' | 'documents' | 'history'>('info');
  const [changingStage, setChangingStage] = useState(false);
  const [showMoveToStageDropdown, setShowMoveToStageDropdown] = useState(false);
  const [reviewsRefreshKey, setReviewsRefreshKey] = useState(0);
  const moveToStageDropdownRef = useRef<HTMLDivElement>(null);

  const companyId = useCompanyId();

  // Custom hooks - initialize in correct order
  const commentsHook = useCandidateComments({ companyCandidateId: id });
  
  const {
    candidate,
    loading,
    error,
    availableStages,
    nextStage,
    failStages,
    reloadCandidate,
  } = useCandidateData({
    candidateId: id,
    companyId,
  });

  const filesHook = useCandidateFiles({ candidateId: candidate?.candidate_id });

  const workflowsHook = useWorkflowsWithData({
    companyCandidateId: id,
    candidate,
    allComments: commentsHook.allComments,
  });

  // Load comments when candidate loads
  useEffect(() => {
    if (candidate && id) {
      commentsHook.loadAllComments();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [candidate?.candidate_id, id]);

  // Load files when candidate loads
  useEffect(() => {
    if (candidate?.candidate_id) {
      filesHook.loadFiles();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [candidate?.candidate_id]);

  // Load workflows when candidate is loaded (only once, not on every comment change)
  useEffect(() => {
    if (candidate && id) {
      workflowsHook.loadWorkflowsWithData();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [candidate?.candidate_id, id]);

  // Memoized handlers
  const handleMoveToStage = useCallback(async (stageId: string) => {
    if (!id || !candidate) return;

    try {
      setChangingStage(true);
      await companyCandidateService.changeStage(id, { new_stage_id: stageId });
      await reloadCandidate();
      setShowMoveToStageDropdown(false);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to move candidate';
      alert(t('company.workflowBoard.failedToMoveCandidateMessage', { message: errorMessage }));
    } finally {
      setChangingStage(false);
    }
  }, [id, candidate, reloadCandidate, t]);

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


  const handleChangeStage = useCallback(async (newStageId: string) => {
    if (!id) return;

    try {
      setChangingStage(true);
      await companyCandidateService.changeStage(id, { new_stage_id: newStageId });
      await reloadCandidate();
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to change stage';
      console.error('Error changing stage:', errorMessage);
    } finally {
      setChangingStage(false);
    }
  }, [id, reloadCandidate]);

  const handleUpdateCustomFieldValue = useCallback(async (fieldKey: string, value: unknown) => {
    if (!id || !candidate) return;

    try {
      const currentFieldValue = candidate.custom_field_values?.[fieldKey];
      if (!currentFieldValue) {
        console.error('Custom field not found:', fieldKey);
        return;
      }

      await customFieldValueService.upsertCustomFieldValue(
        id,
        currentFieldValue.field_id,
        value
      );

      await reloadCandidate();
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to update custom field value';
      console.error('Error updating custom field value:', errorMessage);
    }
  }, [id, candidate, reloadCandidate]);

  const formatFileDate = useCallback((dateString: string) => {
    try {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
      });
    } catch {
      return 'Unknown date';
    }
  }, []);

  const handleToggleMoveToStageDropdown = useCallback(() => {
    setShowMoveToStageDropdown((prev) => !prev);
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error || !candidate) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-6">
        <div className="flex items-center gap-3">
          <AlertCircle className="w-6 h-6 text-red-600" />
          <div>
            <h3 className="text-lg font-semibold text-red-900">Error</h3>
            <p className="text-red-800">{error || 'Candidate not found'}</p>
          </div>
        </div>
        <button
          onClick={() => navigate('/company/candidates')}
          className="mt-4 flex items-center gap-2 text-red-700 hover:text-red-900"
        >
          <ArrowLeft className="w-4 h-4" />
          {t('company.candidates.backToCandidates')}
        </button>
      </div>
    );
  }

  return (
    <div>
      {/* Header */}
      {candidate && (
        <CandidateHeader
          candidate={candidate}
          candidateId={id!}
          availableStages={availableStages}
          changingStage={changingStage}
          showMoveToStageDropdown={showMoveToStageDropdown}
          onToggleMoveToStageDropdown={handleToggleMoveToStageDropdown}
          onMoveToStage={handleMoveToStage}
          moveToStageDropdownRef={moveToStageDropdownRef}
        />
      )}

      <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
        {/* Main Content */}
        <div className="lg:col-span-4 space-y-6">
          {/* Tabs */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200">
            <div className="border-b border-gray-200">
              <nav className="flex gap-4 px-6">
                <button
                  onClick={() => setActiveTab('info')}
                  className={`py-4 border-b-2 font-medium transition-colors ${
                    activeTab === 'info'
                      ? 'border-blue-600 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700'
                  }`}
                >
                  {t('company.candidates.tabs.information')}
                </button>
                <button
                  onClick={() => setActiveTab('comments')}
                  className={`py-4 border-b-2 font-medium transition-colors relative ${
                    activeTab === 'comments'
                      ? 'border-blue-600 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700'
                  }`}
                >
                  {t('company.candidates.tabs.comments', { defaultValue: 'Comentarios' })}
                  {commentsHook.pendingCommentsCount > 0 && (
                    <span className="absolute top-2 right-0 bg-red-500 text-white text-xs font-bold rounded-full w-5 h-5 flex items-center justify-center">
                      {commentsHook.pendingCommentsCount}
                    </span>
                  )}
                </button>
                <button
                  onClick={() => setActiveTab('reviews')}
                  className={`py-4 border-b-2 font-medium transition-colors ${
                    activeTab === 'reviews'
                      ? 'border-blue-600 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700'
                  }`}
                >
                  {t('company.candidates.tabs.reviews', { defaultValue: 'Evaluaciones' })}
                </button>
                <button
                  onClick={() => setActiveTab('documents')}
                  className={`py-4 border-b-2 font-medium transition-colors ${
                    activeTab === 'documents'
                      ? 'border-blue-600 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700'
                  }`}
                >
                  {t('company.candidates.tabs.documents')}
                </button>
                <button
                  onClick={() => setActiveTab('history')}
                  className={`py-4 border-b-2 font-medium transition-colors ${
                    activeTab === 'history'
                      ? 'border-blue-600 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700'
                  }`}
                >
                  {t('company.candidates.tabs.history')}
                </button>
              </nav>
            </div>

            <div className="p-6">
              {/* Information Tab */}
              {activeTab === 'info' && (
                <div className="space-y-6">
                  {/* Contact Information */}
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">
                      {t('company.candidates.detail.contactInformation')}
                    </h3>
                    <div className="space-y-3">
                      {candidate.candidate_email && (
                        <div className="flex items-center gap-3 text-gray-700">
                          <Mail className="w-5 h-5 text-gray-400" />
                          <span>{candidate.candidate_email}</span>
                        </div>
                      )}
                      {candidate.candidate_phone && (
                        <div className="flex items-center gap-3 text-gray-700">
                          <Phone className="w-5 h-5 text-gray-400" />
                          <span>{candidate.candidate_phone}</span>
                        </div>
                      )}
                    </div>
                  </div>


                  {/* Tags */}
                  {candidate.tags.length > 0 && (
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900 mb-4">Tags</h3>
                      <div className="flex flex-wrap gap-2">
                        {candidate.tags.map((tag, idx) => (
                          <span
                            key={idx}
                            className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm"
                          >
                            {tag}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* Comments Tab */}
              {activeTab === 'comments' && candidate && (
                <div className="space-y-6">
                  {candidate.current_stage_id ? (
                    <CandidateCommentsSection
                      companyCandidateId={id!}
                      stageId={candidate.current_stage_id}
                      currentWorkflowId={candidate.current_workflow_id || undefined}
                      onCommentChange={async () => {
                        await commentsHook.loadAllComments();
                        await workflowsHook.loadWorkflowsWithData();
                        commentsHook.refreshComments();
                      }}
                      refreshKey={commentsHook.commentsRefreshKey}
                      defaultExpanded={true}
                    />
                  ) : (
                    <div className="text-center py-8 border-2 border-dashed border-gray-300 rounded-lg">
                      <MessageSquare className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                      <p className="text-gray-500 mb-2">{t('company.candidates.detail.noStageAssigned')}</p>
                      <p className="text-sm text-gray-400">{t('company.candidates.detail.assignStageToComment')}</p>
                    </div>
                  )}
                </div>
              )}

              {/* Reviews Tab */}
              {activeTab === 'reviews' && candidate && (
                <div className="space-y-6">
                  {candidate.current_stage_id ? (
                    <CandidateReviewsSection
                      companyCandidateId={id!}
                      stageId={candidate.current_stage_id}
                      currentWorkflowId={candidate.current_workflow_id || undefined}
                      onReviewChange={async () => {
                        await commentsHook.loadAllComments();
                        await workflowsHook.loadWorkflowsWithData();
                        setReviewsRefreshKey((prev) => prev + 1);
                      }}
                      refreshKey={reviewsRefreshKey}
                    />
                  ) : (
                    <div className="text-center py-8 border-2 border-dashed border-gray-300 rounded-lg">
                      <MessageSquare className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                      <p className="text-gray-500 mb-2">{t('company.candidates.detail.noStageAssigned')}</p>
                      <p className="text-sm text-gray-400">{t('company.candidates.detail.assignStageToComment')}</p>
                    </div>
                  )}
                </div>
              )}

              {/* Documents Tab */}
              {activeTab === 'documents' && (
                <div className="space-y-6">
                  {/* File Attachments Section */}
                  <div>
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="text-lg font-semibold text-gray-900">
                        {t('company.candidates.detail.fileAttachments')}
                      </h3>
                      <label className="flex items-center gap-2 px-3 py-1 text-sm text-blue-600 hover:text-blue-700 hover:bg-blue-50 rounded-lg transition-colors cursor-pointer">
                        <Plus className="w-4 h-4" />
                        {t('company.candidates.detail.addFile')}
                        <input
                          type="file"
                          onChange={filesHook.handleFileUpload}
                          disabled={filesHook.uploadingFile}
                          className="hidden"
                          accept=".pdf,.doc,.docx,.txt,.jpg,.jpeg,.png"
                        />
                      </label>
                    </div>

                    {filesHook.attachedFiles.length === 0 ? (
                      <div className="text-center py-8 border-2 border-dashed border-gray-300 rounded-lg">
                        <Paperclip className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                        <p className="text-gray-500 mb-2">{t('company.candidates.detail.noFilesAttached')}</p>
                        <p className="text-sm text-gray-400">{t('company.candidates.detail.clickAddFile')}</p>
                      </div>
                    ) : (
                      <div className="space-y-2">
                        {filesHook.attachedFiles.map((file) => (
                          <div
                            key={file.id}
                            className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                          >
                            <div className="flex items-center gap-3">
                              <FileText className="w-5 h-5 text-gray-500" />
                              <div>
                                <p className="text-sm font-medium text-gray-900">
                                  {file.original_name}
                                </p>
                                <p className="text-xs text-gray-500">
                                  {(file.size / 1024).toFixed(1)} KB • {formatFileDate(file.uploaded_at)}
                                </p>
                              </div>
                            </div>
                            <div className="flex items-center gap-2">
                              <button
                                onClick={() => filesHook.handleDownloadFile(file)}
                                className="p-1 text-gray-500 hover:text-blue-600 transition-colors"
                                title={t('company.candidates.detail.download')}
                              >
                                <Download className="w-4 h-4" />
                              </button>
                              <button
                                onClick={() => filesHook.handleDeleteFile(file.id)}
                                className="p-1 text-gray-500 hover:text-red-600 transition-colors"
                                title={t('company.candidates.detail.delete')}
                              >
                                <Trash2 className="w-4 h-4" />
                              </button>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}

                    {filesHook.uploadingFile && (
                      <div className="text-center py-4">
                        <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600 mx-auto mb-2"></div>
                        <p className="text-sm text-gray-600">{t('company.candidates.detail.uploadingFile')}</p>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* History Tab - Phase 12: Stage Timeline */}
              {activeTab === 'history' && (
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">{t('company.candidates.detail.stageTimeline', { defaultValue: 'Stage Timeline' })}</h3>
                  <StageTimeline candidate={candidate} companyId={companyId || ''} />
                </div>
              )}
            </div>
          </div>

          {/* Additional Data and Comments - Side by side */}
          {workflowsHook.availableWorkflows.length > 0 ? (
            <div className="space-y-4">
              {/* Workflow Tabs - Only show if more than one workflow */}
              {workflowsHook.availableWorkflows.length > 1 && (
                <div className="bg-white rounded-lg shadow-sm border border-gray-200">
                  <div className="border-b border-gray-200">
                    <nav className="flex gap-2 px-4 overflow-x-auto">
                      {workflowsHook.availableWorkflows.map((workflow) => (
                        <button
                          key={workflow.id}
                          onClick={() => workflowsHook.setSelectedWorkflowId(workflow.id)}
                          className={`px-4 py-3 border-b-2 font-medium transition-colors whitespace-nowrap ${
                            workflowsHook.selectedWorkflowId === workflow.id
                              ? 'border-blue-600 text-blue-600'
                              : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                          }`}
                        >
                          {workflow.name}
                        </button>
                      ))}
                    </nav>
                  </div>
                </div>
              )}

              {/* Content for selected workflow */}
              {workflowsHook.selectedWorkflowId && (
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {/* Additional Data Section */}
                  {workflowsHook.selectedWorkflowId && workflowsHook.allCustomFieldValues[workflowsHook.selectedWorkflowId] && Object.keys(workflowsHook.allCustomFieldValues[workflowsHook.selectedWorkflowId]).length > 0 ? (
                    <CustomFieldsCard 
                      customFieldValues={workflowsHook.allCustomFieldValues[workflowsHook.selectedWorkflowId]}
                      onUpdateValue={async (fieldKey: string, value: unknown) => {
                        // Find the custom field ID from the current values
                        const selectedId = workflowsHook.selectedWorkflowId;
                        if (!selectedId) return;
                        const currentFieldValue = workflowsHook.allCustomFieldValues[selectedId]?.[fieldKey];
                        if (!currentFieldValue) {
                          console.error('Custom field not found:', fieldKey);
                          return;
                        }

                        try {
                          // Update the custom field value
                          await customFieldValueService.upsertCustomFieldValue(
                            id!,
                            currentFieldValue.field_id,
                            value
                          );

                          // Reload workflows with data to refresh the display
                          await workflowsHook.loadWorkflowsWithData();
                        } catch (err) {
                          const errorMessage = err instanceof Error ? err.message : 'Failed to update custom field value';
                          console.error('Error updating custom field value:', errorMessage);
                        }
                      }}
                      isEditable={true}
                    />
                  ) : (
                    <div></div>
                  )}

                  {/* Comments Section - Shows comments for current stage with full functionality */}
                  {candidate.current_stage_id && (
                    <CandidateCommentsSection
                      companyCandidateId={id!}
                      stageId={candidate.current_stage_id}
                      currentWorkflowId={candidate.current_workflow_id || undefined}
                      onCommentChange={async () => {
                        await commentsHook.loadAllComments();
                        await workflowsHook.loadWorkflowsWithData();
                        commentsHook.refreshComments();
                      }}
                      onReviewChange={async () => {
                        // Refresh reviews section when a review is created from comments section
                        await commentsHook.loadAllComments();
                        await workflowsHook.loadWorkflowsWithData();
                        setReviewsRefreshKey((prev) => prev + 1);
                      }}
                      refreshKey={commentsHook.commentsRefreshKey}
                      onNavigateToCommentsTab={() => setActiveTab('comments')}
                    />
                  )}
                </div>
              )}
            </div>
          ) : (
            /* Fallback: Show current workflow custom fields if available, even if workflows not loaded yet */
            (candidate.current_workflow_id || candidate.current_stage_id) && (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {candidate.custom_field_values && Object.keys(candidate.custom_field_values).length > 0 ? (
                  <CustomFieldsCard 
                    customFieldValues={candidate.custom_field_values}
                    onUpdateValue={handleUpdateCustomFieldValue}
                    isEditable={true}
                  />
                ) : (
                  <div></div>
                )}
                {candidate.current_stage_id && (
                  <CandidateCommentsSection
                    companyCandidateId={id!}
                    stageId={candidate.current_stage_id}
                    currentWorkflowId={candidate.current_workflow_id || undefined}
                    onCommentChange={async () => {
                      await commentsHook.loadAllComments();
                      commentsHook.refreshComments();
                    }}
                    onReviewChange={async () => {
                      // Refresh reviews section when a review is created from comments section
                      await commentsHook.loadAllComments();
                      await workflowsHook.loadWorkflowsWithData();
                      setReviewsRefreshKey((prev) => prev + 1);
                    }}
                    refreshKey={commentsHook.commentsRefreshKey}
                    onNavigateToCommentsTab={() => setActiveTab('comments')}
                  />
                )}
              </div>
            )
          )}
        </div>

        {/* Sidebar */}
        {candidate && (
          <CandidateSidebar
            candidate={candidate}
            nextStage={nextStage}
            failStages={failStages}
            changingStage={changingStage}
            onChangeStage={handleChangeStage}
          />
        )}
      </div>
    </div>
  );
}
