import { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useCompanyNavigation } from '../../hooks/useCompanyNavigation';
import { toast } from 'react-toastify';
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
  User,
  Clock,
  Eye,
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { companyCandidateService } from '../../services/companyCandidateService';
import { customFieldValueService } from '../../services/customFieldValueService';
import { StageTimeline } from '../../components/candidate';
import CustomFieldsCard from '../../components/candidate/CustomFieldsCard';
import CandidateCommentsSection from '../../components/candidate/CandidateCommentsSection';
import CandidateReviewsSection from '../../components/candidate/CandidateReviewsSection';
import CandidateInterviewsSection from '../../components/candidate/CandidateInterviewsSection';
import CandidateHeader from '../../components/candidate/CandidateHeader';
import CandidateSidebar from '../../components/candidate/CandidateSidebar';
import CandidateAnswersSection from '../../components/candidate/CandidateAnswersSection';
import { useCandidateData } from '../../hooks/useCandidateData';
import { useCandidateFiles } from '../../hooks/useCandidateFiles';
import { useCandidateComments } from '../../hooks/useCandidateComments';
import { useWorkflowsWithData } from '../../hooks/useWorkflowsWithData';
import { useCompanyId } from '../../hooks/useCompanyId';

export default function CandidateDetailPage() {
  const { t } = useTranslation();
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { getPath } = useCompanyNavigation();
  const [activeTab, setActiveTab] = useState<'info' | 'profile' | 'answers' | 'comments' | 'reviews' | 'documents' | 'interviews' | 'history'>('info');
  const [showLiveProfile, setShowLiveProfile] = useState(false);
  const [changingStage, setChangingStage] = useState(false);
  const [reviewsRefreshKey, setReviewsRefreshKey] = useState(0);

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
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to move candidate';
      toast.error(t('company.workflowBoard.failedToMoveCandidateMessage', { message: errorMessage }));
    } finally {
      setChangingStage(false);
    }
  }, [id, candidate, reloadCandidate, t]);

  const handleChangeStage = useCallback(async (newStageId: string) => {
    if (!id) return;

    try {
      setChangingStage(true);
      await companyCandidateService.changeStage(id, { new_stage_id: newStageId });
      await reloadCandidate();
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to change stage';
      console.error('Error changing stage:', errorMessage);
      toast.error(t('company.workflowBoard.failedToMoveCandidateMessage', { message: errorMessage }));
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

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error || !candidate) {
    return (
      <Alert variant="destructive">
        <AlertCircle className="h-4 w-4" />
        <AlertDescription>
          {error || 'Candidate not found'}
        </AlertDescription>
        <Button
          variant="outline"
          onClick={() => navigate(getPath('candidates'))}
          className="mt-4"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          {t('company.candidates.backToCandidates')}
        </Button>
      </Alert>
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
          onMoveToStage={handleMoveToStage}
        />
      )}

      <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
        {/* Main Content */}
        <div className="lg:col-span-4 space-y-6">
          {/* Tabs */}
          <Card>
            <Tabs value={activeTab} onValueChange={(value) => setActiveTab(value as any)}>
              <CardHeader className="pb-3">
                <TabsList>
                  <TabsTrigger value="info">
                    {t('company.candidates.tabs.information')}
                  </TabsTrigger>
                  <TabsTrigger value="profile">
                    <User className="w-4 h-4 mr-1" />
                    {t('company.candidates.tabs.profile', { defaultValue: 'Profile' })}
                  </TabsTrigger>
                  <TabsTrigger value="answers">
                    {t('company.candidates.tabs.answers', { defaultValue: 'Answers' })}
                  </TabsTrigger>
                  <TabsTrigger value="comments" className="relative">
                    {t('company.candidates.tabs.comments', { defaultValue: 'Comentarios' })}
                    {commentsHook.pendingCommentsCount > 0 && (
                      <Badge className="ml-2 h-5 w-5 flex items-center justify-center p-0" variant="destructive">
                        {commentsHook.pendingCommentsCount}
                      </Badge>
                    )}
                  </TabsTrigger>
                  <TabsTrigger value="reviews">
                    {t('company.candidates.tabs.reviews', { defaultValue: 'Evaluaciones' })}
                  </TabsTrigger>
                  <TabsTrigger value="documents">
                    {t('company.candidates.tabs.documents')}
                  </TabsTrigger>
                  <TabsTrigger value="interviews">
                    {t('company.candidates.tabs.interviews', { defaultValue: 'Interviews' })}
                  </TabsTrigger>
                  <TabsTrigger value="history">
                    {t('company.candidates.tabs.history')}
                  </TabsTrigger>
                </TabsList>
              </CardHeader>

              <CardContent>
                {/* Information Tab */}
                <TabsContent value="info">
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
                            <Badge key={idx} variant="secondary">
                              {tag}
                            </Badge>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </TabsContent>

                {/* Profile Tab - Shows profile snapshot from application time */}
                <TabsContent value="profile">
                  <div className="space-y-6">
                    {/* Toggle between snapshot and live profile */}
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <Clock className="w-5 h-5 text-gray-500" />
                        <span className="text-sm text-gray-600">
                          {showLiveProfile
                            ? t('company.candidates.profile.viewingLive', { defaultValue: 'Viewing current profile' })
                            : t('company.candidates.profile.viewingSnapshot', { defaultValue: 'Viewing profile at application time' })}
                        </span>
                      </div>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => setShowLiveProfile(!showLiveProfile)}
                        className="flex items-center gap-2"
                      >
                        <Eye className="w-4 h-4" />
                        {showLiveProfile
                          ? t('company.candidates.profile.showSnapshot', { defaultValue: 'Show application snapshot' })
                          : t('company.candidates.profile.showLive', { defaultValue: 'Show current profile' })}
                      </Button>
                    </div>

                    {/* Profile content */}
                    {showLiveProfile ? (
                      // Live profile - show structured data
                      <div className="prose max-w-none">
                        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
                          <p className="text-sm text-blue-800">
                            {t('company.candidates.profile.liveDataNotice', {
                              defaultValue: 'This shows the candidate\'s current profile data, which may have been updated since they applied.'
                            })}
                          </p>
                        </div>
                        {/* Tags as skills indicator */}
                        {candidate.tags && candidate.tags.length > 0 && (
                          <div className="mb-6">
                            <h3 className="text-lg font-semibold text-gray-900 mb-3">
                              {t('company.candidates.profile.tags', { defaultValue: 'Tags' })}
                            </h3>
                            <div className="flex flex-wrap gap-2">
                              {candidate.tags.map((tag: string, idx: number) => (
                                <Badge key={idx} variant="secondary">{tag}</Badge>
                              ))}
                            </div>
                          </div>
                        )}
                        {/* Additional live data can be added here */}
                      </div>
                    ) : (
                      // Snapshot profile - show markdown
                      <div className="prose max-w-none">
                        {(candidate as any).profile_snapshot_markdown ? (
                          <>
                            <div className="bg-amber-50 border border-amber-200 rounded-lg p-4 mb-4">
                              <p className="text-sm text-amber-800">
                                {t('company.candidates.profile.snapshotNotice', {
                                  defaultValue: 'This is a snapshot of the candidate\'s profile at the time they applied. It may differ from their current profile.'
                                })}
                              </p>
                            </div>
                            <div
                              className="bg-white border rounded-lg p-6"
                              dangerouslySetInnerHTML={{
                                __html: ((candidate as any).profile_snapshot_markdown as string)
                                  .replace(/^### (.*$)/gim, '<h3 class="text-lg font-semibold mt-4 mb-2">$1</h3>')
                                  .replace(/^## (.*$)/gim, '<h2 class="text-xl font-bold mt-6 mb-3">$1</h2>')
                                  .replace(/^# (.*$)/gim, '<h1 class="text-2xl font-bold mb-4">$1</h1>')
                                  .replace(/^\*\*(.*)\*\*$/gim, '<strong>$1</strong>')
                                  .replace(/^\*(.*)\*$/gim, '<em>$1</em>')
                                  .replace(/^- (.*$)/gim, '<li class="ml-4">$1</li>')
                                  .replace(/\n/g, '<br/>')
                              }}
                            />
                          </>
                        ) : (
                          <div className="text-center py-8 border-2 border-dashed border-gray-300 rounded-lg">
                            <User className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                            <p className="text-gray-500 mb-2">
                              {t('company.candidates.profile.noSnapshot', { defaultValue: 'No profile snapshot available' })}
                            </p>
                            <p className="text-sm text-gray-400">
                              {t('company.candidates.profile.noSnapshotHint', {
                                defaultValue: 'Profile snapshots are created when candidates apply through the new application flow.'
                              })}
                            </p>
                          </div>
                        )}
                      </div>
                    )}

                    {/* CV Download */}
                    {(candidate as any).cv_file_id && (
                      <div className="border-t pt-4">
                        <Button variant="outline" className="flex items-center gap-2">
                          <Download className="w-4 h-4" />
                          {t('company.candidates.profile.downloadCV', { defaultValue: 'Download CV' })}
                        </Button>
                      </div>
                    )}
                  </div>
                </TabsContent>

                {/* Answers Tab */}
                <TabsContent value="answers">
                  {candidate && id && (
                    <CandidateAnswersSection applicationId={id} />
                  )}
                </TabsContent>

                {/* Comments Tab */}
                <TabsContent value="comments">
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
                </TabsContent>

                {/* Reviews Tab */}
                <TabsContent value="reviews">
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
                </TabsContent>

                {/* Documents Tab */}
                <TabsContent value="documents">
                  <div className="space-y-6">
                    {/* File Attachments Section */}
                    <div>
                      <div className="flex items-center justify-between mb-4">
                        <h3 className="text-lg font-semibold text-gray-900">
                          {t('company.candidates.detail.fileAttachments')}
                        </h3>
                        <label className="cursor-pointer">
                          <Button variant="outline" size="sm" asChild>
                            <span>
                              <Plus className="w-4 h-4 mr-2" />
                              {t('company.candidates.detail.addFile')}
                            </span>
                          </Button>
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
                                <Button
                                  variant="ghost"
                                  size="icon"
                                  onClick={() => filesHook.handleDownloadFile(file)}
                                  title={t('company.candidates.detail.download')}
                                >
                                  <Download className="w-4 h-4" />
                                </Button>
                                <Button
                                  variant="ghost"
                                  size="icon"
                                  onClick={() => filesHook.handleDeleteFile(file.id)}
                                  title={t('company.candidates.detail.delete')}
                                >
                                  <Trash2 className="w-4 h-4" />
                                </Button>
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
                </TabsContent>

                {/* Interviews Tab */}
                <TabsContent value="interviews">
                  {candidate && (
                    <CandidateInterviewsSection
                      candidateId={candidate.candidate_id}
                      companyCandidateId={id || ''}
                      currentStageId={candidate.current_stage_id}
                      currentWorkflowId={candidate.current_workflow_id}
                      availableStages={availableStages}
                      jobPositionId={candidate.job_position_id}
                    />
                  )}
                </TabsContent>

                {/* History Tab - Phase 12: Stage Timeline */}
                <TabsContent value="history">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">{t('company.candidates.detail.stageTimeline', { defaultValue: 'Stage Timeline' })}</h3>
                    <StageTimeline candidate={candidate} companyId={companyId || ''} />
                  </div>
                </TabsContent>
              </CardContent>
            </Tabs>
          </Card>

          {/* Additional Data and Comments - Side by side */}
          {workflowsHook.availableWorkflows.length > 0 ? (
            <div className="space-y-4">
              {/* Workflow Tabs - Only show if more than one workflow */}
              {workflowsHook.availableWorkflows.length > 1 && (
                <Card>
                  <Tabs value={workflowsHook.selectedWorkflowId || undefined} onValueChange={(value) => workflowsHook.setSelectedWorkflowId(value)}>
                    <CardHeader className="pb-3">
                      <TabsList>
                        {workflowsHook.availableWorkflows.map((workflow) => (
                          <TabsTrigger key={workflow.id} value={workflow.id}>
                            {workflow.name}
                          </TabsTrigger>
                        ))}
                      </TabsList>
                    </CardHeader>
                  </Tabs>
                </Card>
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
