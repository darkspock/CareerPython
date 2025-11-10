import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import {
  ArrowLeft,
  ArrowRight,
  Edit,
  Archive,
  Mail,
  Phone,
  AlertCircle,
  CheckCircle,
  XCircle,
  Clock,
  X,
  Plus,
  Paperclip,
  FileText,
  Download,
  Trash2,
  MessageSquare
} from 'lucide-react';
import { companyCandidateService } from '../../services/companyCandidateService';
import { fileUploadService, type AttachedFile } from '../../services/fileUploadService';
import { workflowStageService, type WorkflowStage } from '../../services/workflowStageService';
import { customFieldValueService } from '../../services/customFieldValueService';
import { companyWorkflowService } from '../../services/companyWorkflowService';
import type { CompanyCandidate } from '../../types/companyCandidate';
import {
  getCandidateStatusColor,
  getPriorityColor,
} from '../../types/companyCandidate';
import { StageTimeline } from '../../components/candidate';
import CustomFieldsCard from '../../components/candidate/CustomFieldsCard';
import CandidateCommentsSection from '../../components/candidate/CandidateCommentsSection';
import CandidateReviewsSection from '../../components/candidate/CandidateReviewsSection';
import { candidateCommentService } from '../../services/candidateCommentService';
import type { CandidateComment } from '../../types/candidateComment';

export default function CandidateDetailPage() {
  const { t } = useTranslation();
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [candidate, setCandidate] = useState<CompanyCandidate | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'info' | 'comments' | 'reviews' | 'documents' | 'history'>('info');
  
  // File attachment state
  const [attachedFiles, setAttachedFiles] = useState<AttachedFile[]>([]);
  const [uploadingFile, setUploadingFile] = useState(false);

  // Stage transition state
  const [_availableStages, setAvailableStages] = useState<WorkflowStage[]>([]);
  const [nextStage, setNextStage] = useState<WorkflowStage | null>(null);
  const [failStages, setFailStages] = useState<WorkflowStage[]>([]);
  const [changingStage, setChangingStage] = useState(false);

  // Comments state
  const [allComments, setAllComments] = useState<CandidateComment[]>([]);
  const [pendingCommentsCount, setPendingCommentsCount] = useState(0);
  const [loadingComments, setLoadingComments] = useState(false);
  const [commentsRefreshKey, setCommentsRefreshKey] = useState(0);

  // Workflow tabs state
  const [allCustomFieldValues, setAllCustomFieldValues] = useState<Record<string, Record<string, any>>>({});
  const [availableWorkflows, setAvailableWorkflows] = useState<Array<{ id: string; name: string }>>([]);
  const [selectedWorkflowId, setSelectedWorkflowId] = useState<string | null>(null);
  const [_loadingWorkflows, setLoadingWorkflows] = useState(false);

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
    if (id) {
      loadCandidate();
    }
  }, [id]);

  const loadCandidate = async () => {
    if (!id) return;

    try {
      setLoading(true);
      const data = await companyCandidateService.getById(id);
      setCandidate(data);
      
      // Load attached files
      try {
        const files = await fileUploadService.getCandidateFiles(data.candidate_id);
        setAttachedFiles(files);
      } catch (fileErr) {
        console.warn('Could not load attached files:', fileErr);
        // Don't fail the entire load if files can't be loaded
        setAttachedFiles([]);
      }

      // Load workflow stages if candidate has a workflow
      if (data.current_workflow_id) {
        await loadWorkflowStages(data.current_workflow_id, data.current_stage_id || undefined);
      }
      
      // Load all comments
      await loadAllComments();
      
      // Load workflows with custom fields or comments (after comments are loaded)
      await loadWorkflowsWithData();
      
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to load candidate');
      console.error('Error loading candidate:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadWorkflowStages = async (workflowId: string, currentStageId?: string) => {
    try {
      const stages = await workflowStageService.getStagesByWorkflow(workflowId);
      setAvailableStages(stages);

      // Find current stage order
      const currentStage = stages.find(stage => stage.id === currentStageId);
      const currentOrder = currentStage?.order || 0;

      // Get next stage
      const next = await workflowStageService.getNextStage(workflowId, currentOrder);
      setNextStage(next);

      // Get fail stages
      const fail = await workflowStageService.getFailStages(workflowId);
      setFailStages(fail);
    } catch (err) {
      console.error('Error loading workflow stages:', err);
    }
  };

  const loadAllComments = async () => {
    if (!id) return;

    try {
      setLoadingComments(true);
      const comments = await candidateCommentService.getCommentsByCompanyCandidate(id);
      setAllComments(comments || []);
      
      // Count pending comments
      const pendingCount = await candidateCommentService.countPendingComments(id);
      setPendingCommentsCount(pendingCount || 0);
    } catch (err: any) {
      console.error('Error loading comments:', err);
      // Don't fail the entire load if comments can't be loaded
      setAllComments([]);
      setPendingCommentsCount(0);
    } finally {
      setLoadingComments(false);
    }
  };

  const loadWorkflowsWithData = async () => {
    if (!id) return;

    try {
      setLoadingWorkflows(true);
      
      // Get all custom field values organized by workflow_id
      const allValues = await customFieldValueService.getAllCustomFieldValuesByCompanyCandidate(id);
      setAllCustomFieldValues(allValues);
      
      // Get unique workflow IDs from custom fields and comments
      const workflowIds = new Set<string>();
      
      // Add workflows with custom fields
      Object.keys(allValues).forEach(workflowId => {
        if (Object.keys(allValues[workflowId]).length > 0) {
          workflowIds.add(workflowId);
        }
      });
      
      // Add workflows with comments
      allComments.forEach(comment => {
        if (comment.workflow_id) {
          workflowIds.add(comment.workflow_id);
        }
      });
      
      // Add current workflow if candidate has one
      if (candidate?.current_workflow_id) {
        workflowIds.add(candidate.current_workflow_id);
      }
      
      // Fetch workflow names for all workflows
      const workflowsData: Array<{ id: string; name: string }> = [];
      for (const workflowId of workflowIds) {
        try {
          const workflow = await companyWorkflowService.getWorkflow(workflowId);
          workflowsData.push({ id: workflowId, name: workflow.name });
        } catch (err) {
          console.warn(`Failed to load workflow ${workflowId}:`, err);
          // Use workflow_id as fallback name if we can't load it
          workflowsData.push({ id: workflowId, name: workflowId });
        }
      }
      
      setAvailableWorkflows(workflowsData);
      
      // Set selected workflow to current workflow if available, otherwise first one
      if (candidate?.current_workflow_id && workflowIds.has(candidate.current_workflow_id)) {
        setSelectedWorkflowId(candidate.current_workflow_id);
      } else if (workflowsData.length > 0) {
        setSelectedWorkflowId(workflowsData[0].id);
      } else {
        setSelectedWorkflowId(null);
      }
    } catch (err: any) {
      console.error('Error loading workflows with data:', err);
      setAvailableWorkflows([]);
      setSelectedWorkflowId(null);
    } finally {
      setLoadingWorkflows(false);
    }
  };

  const handleArchive = async () => {
    if (!id || !confirm('Are you sure you want to archive this candidate?')) return;

    try {
      await companyCandidateService.archive(id);
      navigate('/company/candidates');
    } catch (err: any) {
      alert('Failed to archive candidate: ' + err.message);
    }
  };


  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file || !candidate) return;

    try {
      setUploadingFile(true);
      const uploadedFile = await fileUploadService.uploadCandidateFile(
        candidate.candidate_id,
        file
      );
      
      const newFile: AttachedFile = {
        id: uploadedFile.id,
        filename: uploadedFile.filename,
        original_name: uploadedFile.original_name,
        size: uploadedFile.size,
        content_type: uploadedFile.content_type,
        url: uploadedFile.url,
        uploaded_at: uploadedFile.uploaded_at,
        description: (uploadedFile as any).description || ''
      };
      
      setAttachedFiles(prev => [...prev, newFile]);
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to upload file');
      console.error('Error uploading file:', err);
    } finally {
      setUploadingFile(false);
    }
  };

  const handleDeleteFile = async (fileId: string) => {
    if (!candidate) return;

    try {
      await fileUploadService.deleteCandidateFile(candidate.candidate_id, fileId);
      setAttachedFiles(prev => prev.filter(file => file.id !== fileId));
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to delete file');
      console.error('Error deleting file:', err);
    }
  };

  const formatFileDate = (dateString: string) => {
    try {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    } catch {
      return 'Unknown date';
    }
  };

  const handleDownloadFile = async (file: AttachedFile) => {
    if (!candidate) return;
    
    try {
      const blob = await fileUploadService.downloadFile(candidate.candidate_id, file.id);
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = file.original_name;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (err: any) {
      setError(err.message || 'Failed to download file');
      console.error('Error downloading file:', err);
    }
  };

  const handleChangeStage = async (newStageId: string) => {
    if (!id) return;

    try {
      setChangingStage(true);
      await companyCandidateService.changeStage(id, { new_stage_id: newStageId });
      
      // Reload candidate to get updated stage info
      await loadCandidate();
    } catch (err: any) {
      setError(err.message || 'Failed to change stage');
      console.error('Error changing stage:', err);
    } finally {
      setChangingStage(false);
    }
  };

  const handleUpdateCustomFieldValue = async (fieldKey: string, value: any) => {
    if (!id || !candidate) return;

    try {
      // Find the custom field ID from the current values
      const currentFieldValue = candidate.custom_field_values?.[fieldKey];
      if (!currentFieldValue) {
        console.error('Custom field not found:', fieldKey);
        return;
      }

      // Update the custom field value
      await customFieldValueService.upsertCustomFieldValue(
        id,
        currentFieldValue.field_id,
        value
      );

      // Reload candidate to get updated custom field values
      await loadCandidate();
    } catch (err: any) {
      setError(err.message || 'Failed to update custom field value');
      console.error('Error updating custom field value:', err);
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'ACTIVE':
        return <CheckCircle className="w-5 h-5 text-green-600" />;
      case 'PENDING_INVITATION':
      case 'PENDING_CONFIRMATION':
        return <Clock className="w-5 h-5 text-yellow-600" />;
      case 'REJECTED':
        return <XCircle className="w-5 h-5 text-red-600" />;
      case 'ARCHIVED':
        return <Archive className="w-5 h-5 text-gray-600" />;
      default:
        return <AlertCircle className="w-5 h-5 text-gray-600" />;
    }
  };

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
      <div className="mb-6">
        <button
          onClick={() => navigate('/company/candidates')}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-4"
        >
          <ArrowLeft className="w-5 h-5" />
          {t('company.candidates.backToCandidates')}
        </button>

        <div className="flex items-start justify-between">
          <div className="flex items-center gap-4">
            {/* Avatar */}
            <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center">
              <span className="text-2xl font-bold text-blue-600">
                {candidate.candidate_name?.charAt(0).toUpperCase() || 'C'}
              </span>
            </div>

            {/* Name & Email */}
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                {candidate.candidate_name || 'N/A'}
              </h1>
              <p className="text-gray-600">{candidate.candidate_email || 'N/A'}</p>
            </div>
          </div>

          {/* Actions */}
          <div className="flex items-center gap-2">
            <button
              onClick={() => navigate(`/company/candidates/${id}/edit`)}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              title={t('company.candidates.editCandidateDetails')}
            >
              <Edit className="w-4 h-4" />
              {t('company.candidates.edit')}
            </button>
            <button
              onClick={handleArchive}
              className="flex items-center gap-2 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
              title={t('company.candidates.archiveCandidate')}
            >
              <Archive className="w-4 h-4" />
              {t('company.candidates.archive')}
            </button>
          </div>
        </div>
      </div>

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
                  {pendingCommentsCount > 0 && (
                    <span className="absolute top-2 right-0 bg-red-500 text-white text-xs font-bold rounded-full w-5 h-5 flex items-center justify-center">
                      {pendingCommentsCount}
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
                        await loadAllComments();
                        await loadWorkflowsWithData();
                        setCommentsRefreshKey(prev => prev + 1);
                      }}
                      refreshKey={commentsRefreshKey}
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
                        await loadAllComments();
                        await loadWorkflowsWithData();
                      }}
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
                          onChange={handleFileUpload}
                          disabled={uploadingFile}
                          className="hidden"
                          accept=".pdf,.doc,.docx,.txt,.jpg,.jpeg,.png"
                        />
                      </label>
                    </div>

                    {attachedFiles.length === 0 ? (
                      <div className="text-center py-8 border-2 border-dashed border-gray-300 rounded-lg">
                        <Paperclip className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                        <p className="text-gray-500 mb-2">{t('company.candidates.detail.noFilesAttached')}</p>
                        <p className="text-sm text-gray-400">{t('company.candidates.detail.clickAddFile')}</p>
                      </div>
                    ) : (
                      <div className="space-y-2">
                        {attachedFiles.map((file) => (
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
                                onClick={() => handleDownloadFile(file)}
                                className="p-1 text-gray-500 hover:text-blue-600 transition-colors"
                                title={t('company.candidates.detail.download')}
                              >
                                <Download className="w-4 h-4" />
                              </button>
                              <button
                                onClick={() => handleDeleteFile(file.id)}
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

                    {uploadingFile && (
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
                  <StageTimeline candidate={candidate} companyId={getCompanyId() || ''} />
                </div>
              )}
            </div>
          </div>

          {/* Additional Data and Comments - Side by side */}
          {availableWorkflows.length > 0 ? (
            <div className="space-y-4">
              {/* Workflow Tabs - Only show if more than one workflow */}
              {availableWorkflows.length > 1 && (
                <div className="bg-white rounded-lg shadow-sm border border-gray-200">
                  <div className="border-b border-gray-200">
                    <nav className="flex gap-2 px-4 overflow-x-auto">
                      {availableWorkflows.map((workflow) => (
                        <button
                          key={workflow.id}
                          onClick={() => setSelectedWorkflowId(workflow.id)}
                          className={`px-4 py-3 border-b-2 font-medium transition-colors whitespace-nowrap ${
                            selectedWorkflowId === workflow.id
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
              {selectedWorkflowId && (
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {/* Additional Data Section */}
                  {allCustomFieldValues[selectedWorkflowId] && Object.keys(allCustomFieldValues[selectedWorkflowId]).length > 0 ? (
                    <CustomFieldsCard 
                      customFieldValues={allCustomFieldValues[selectedWorkflowId]}
                      onUpdateValue={async (fieldKey: string, value: any) => {
                        // Find the custom field ID from the current values
                        const currentFieldValue = allCustomFieldValues[selectedWorkflowId]?.[fieldKey];
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
                          await loadWorkflowsWithData();
                        } catch (err: any) {
                          setError(err.message || 'Failed to update custom field value');
                          console.error('Error updating custom field value:', err);
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
                        await loadAllComments();
                        await loadWorkflowsWithData();
                        setCommentsRefreshKey(prev => prev + 1);
                      }}
                      refreshKey={commentsRefreshKey}
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
                      await loadAllComments();
                      setCommentsRefreshKey(prev => prev + 1);
                    }}
                    refreshKey={commentsRefreshKey}
                    onNavigateToCommentsTab={() => setActiveTab('comments')}
                  />
                )}
              </div>
            )
          )}
        </div>

        {/* Sidebar */}
        <div className="lg:col-span-1 space-y-6">
          {/* Status Card */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">{t('company.candidates.applicationStatus')}</h3>
            <div className="space-y-4">
              {/* Current Status - Only show when inactive */}
              {candidate.status !== 'ACTIVE' && (
                <div>
                  <label className="text-sm text-gray-600 block mb-2">{t('company.candidates.detail.currentStatus', { defaultValue: 'Current Status' })}</label>
                  <div className="flex items-center gap-2">
                    {getStatusIcon(candidate.status)}
                    <span
                      className={`px-3 py-1 text-sm font-medium rounded-full ${getCandidateStatusColor(
                        candidate.status
                      )}`}
                    >
                      {candidate.status.replace('_', ' ')}
                    </span>
                  </div>
                </div>
              )}

              {/* Priority - Only show when not MEDIUM */}
              {candidate.priority !== 'MEDIUM' && (
                <div>
                  <label className="text-sm text-gray-600 block mb-2">{t('company.candidates.detail.priority', { defaultValue: 'Priority' })}</label>
                  <span
                    className={`inline-block px-3 py-1 text-sm font-medium rounded-full ${getPriorityColor(
                      candidate.priority
                    )}`}
                  >
                    {candidate.priority}
                  </span>
                </div>
              )}

              {/* Workflow Information */}
              {(candidate.workflow_name || candidate.stage_name || candidate.phase_name) && (
                <div>
                  <div className="space-y-2">
                    {candidate.phase_name && (
                      <div className="text-sm">
                        <span className="text-gray-600">{t('company.candidates.detail.phase')}:</span>{' '}
                        <span className="font-medium text-gray-900">{candidate.phase_name}</span>
                      </div>
                    )}
                    {candidate.workflow_name && (
                      <div className="text-sm">
                        <span className="font-medium text-gray-900">{candidate.workflow_name}</span>
                      </div>
                    )}
                    {candidate.stage_name && (
                      <div className="text-sm">
                        <span className="font-medium text-gray-900">{candidate.stage_name}</span>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Stage Transitions */}
              {candidate.current_workflow_id && (nextStage || failStages.length > 0) && (
                <div>
                  <label className="text-sm text-gray-600 block mb-2">{t('company.candidates.detail.actions', { defaultValue: 'Actions' })}</label>
                  <div className="flex flex-wrap gap-2">
                    {/* Next Stage Button */}
                    {nextStage && (
                      <div className="relative group">
                        <button
                          onClick={() => handleChangeStage(nextStage.id)}
                          disabled={changingStage}
                          className="flex items-center justify-center p-2 rounded-lg transition-colors disabled:opacity-50"
                          style={{
                            backgroundColor: nextStage.style?.background_color || '#3B82F6',
                            color: nextStage.style?.color || '#FFFFFF'
                          }}
                        >
                          {changingStage ? (
                            <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
                          ) : (
                            <>
                              {nextStage.style?.icon ? (
                                <span className="text-base" dangerouslySetInnerHTML={{ __html: nextStage.style.icon }} />
                              ) : (
                                <ArrowRight className="w-4 h-4" />
                              )}
                            </>
                          )}
                        </button>
                        {/* Tooltip */}
                        <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-gray-900 text-white text-sm rounded-lg opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-10">
                          {t('company.candidates.moveToStage', { stage: nextStage.name })}
                          <div className="absolute top-full left-1/2 transform -translate-x-1/2 -mt-1">
                            <div className="border-4 border-transparent border-t-gray-900"></div>
                          </div>
                        </div>
                      </div>
                    )}

                    {/* Fail Stages Buttons */}
                    {failStages.map((stage) => (
                      <div key={stage.id} className="relative group">
                        <button
                          onClick={() => handleChangeStage(stage.id)}
                          disabled={changingStage}
                          className="flex items-center justify-center p-2 rounded-lg transition-colors disabled:opacity-50"
                          style={{
                            backgroundColor: stage.style?.background_color || '#DC2626',
                            color: stage.style?.color || '#FFFFFF'
                          }}
                        >
                          {changingStage ? (
                            <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
                          ) : (
                            <>
                              {stage.style?.icon ? (
                                <span className="text-base" dangerouslySetInnerHTML={{ __html: stage.style.icon }} />
                              ) : (
                                <X className="w-4 h-4" />
                              )}
                            </>
                          )}
                        </button>
                        {/* Tooltip */}
                        <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-gray-900 text-white text-sm rounded-lg opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-10">
                          {t('company.candidates.moveToStage', { stage: stage.name })}
                          <div className="absolute top-full left-1/2 transform -translate-x-1/2 -mt-1">
                            <div className="border-4 border-transparent border-t-gray-900"></div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Dates Card */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">{t('company.candidates.dates')}</h3>
            <div className="space-y-3 text-sm">
              <div>
                <span className="text-gray-600">{t('company.candidates.detail.created')}:</span>
                <p className="font-medium text-gray-900">
                  {new Date(candidate.created_at).toLocaleDateString()}
                </p>
              </div>
              <div>
                <span className="text-gray-600">{t('company.candidates.detail.lastUpdated', { defaultValue: 'Last Updated' })}:</span>
                <p className="font-medium text-gray-900">
                  {new Date(candidate.updated_at).toLocaleDateString()}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
