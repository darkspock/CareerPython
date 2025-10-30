import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  ArrowLeft,
  Edit,
  Archive,
  Mail,
  Phone,
  Calendar,
  Tag,
  AlertCircle,
  CheckCircle,
  XCircle,
  Clock,
  Save,
  X,
  Plus,
  Paperclip,
  FileText,
  Download,
  Trash2
} from 'lucide-react';
import { companyCandidateService } from '../../services/companyCandidateService';
import { fileUploadService, type AttachedFile } from '../../services/fileUploadService';
import type { CompanyCandidate } from '../../types/companyCandidate';
import {
  getCandidateStatusColor,
  getPriorityColor,
  getOwnershipColor
} from '../../types/companyCandidate';
import { StageTimeline } from '../../components/candidate';

export default function CandidateDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [candidate, setCandidate] = useState<CompanyCandidate | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'info' | 'notes' | 'history'>('info');
  
  // Notes editing state
  const [isEditingNotes, setIsEditingNotes] = useState(false);
  const [notesText, setNotesText] = useState('');
  const [savingNotes, setSavingNotes] = useState(false);
  
  // File attachment state
  const [attachedFiles, setAttachedFiles] = useState<AttachedFile[]>([]);
  const [uploadingFile, setUploadingFile] = useState(false);

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
      setNotesText(data.internal_notes || '');
      
      // Load attached files
      try {
        const files = await fileUploadService.getCandidateFiles(data.candidate_id);
        setAttachedFiles(files);
      } catch (fileErr) {
        console.warn('Could not load attached files:', fileErr);
        // Don't fail the entire load if files can't be loaded
        setAttachedFiles([]);
      }
      
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to load candidate');
      console.error('Error loading candidate:', err);
    } finally {
      setLoading(false);
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

  const handleStartEditingNotes = () => {
    setIsEditingNotes(true);
    setNotesText(candidate?.internal_notes || '');
  };

  const handleCancelEditingNotes = () => {
    setIsEditingNotes(false);
    setNotesText(candidate?.internal_notes || '');
  };

  const handleSaveNotes = async () => {
    if (!id) return;

    try {
      setSavingNotes(true);
      const updatedCandidate = await companyCandidateService.update(id, {
        internal_notes: notesText
      });
      setCandidate(updatedCandidate);
      setIsEditingNotes(false);
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to save notes');
      console.error('Error saving notes:', err);
    } finally {
      setSavingNotes(false);
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
        description: uploadedFile.description
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
          Back to Candidates
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
          Back to Candidates
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
              title="Edit candidate details"
            >
              <Edit className="w-4 h-4" />
              Edit
            </button>
            <button
              onClick={handleArchive}
              className="flex items-center gap-2 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
              title="Archive this candidate"
            >
              <Archive className="w-4 h-4" />
              Archive
            </button>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-6">
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
                  Information
                </button>
                <button
                  onClick={() => setActiveTab('notes')}
                  className={`py-4 border-b-2 font-medium transition-colors ${
                    activeTab === 'notes'
                      ? 'border-blue-600 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700'
                  }`}
                >
                  Notes
                </button>
                <button
                  onClick={() => setActiveTab('history')}
                  className={`py-4 border-b-2 font-medium transition-colors ${
                    activeTab === 'history'
                      ? 'border-blue-600 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700'
                  }`}
                >
                  History
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
                      Contact Information
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

                  {/* Workflow Information */}
                  {(candidate.workflow_name || candidate.stage_name) && (
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900 mb-4">
                        Workflow Status
                      </h3>
                      <div className="space-y-2">
                        {candidate.workflow_name && (
                          <div className="text-gray-700">
                            <span className="font-medium">Workflow:</span>{' '}
                            {candidate.workflow_name}
                          </div>
                        )}
                        {candidate.stage_name && (
                          <div className="text-gray-700">
                            <span className="font-medium">Current Stage:</span>{' '}
                            {candidate.stage_name}
                          </div>
                        )}
                      </div>
                    </div>
                  )}

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

              {/* Notes Tab */}
              {activeTab === 'notes' && (
                <div className="space-y-6">
                  {/* Internal Notes Section */}
                  <div>
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="text-lg font-semibold text-gray-900">
                        Internal Notes
                      </h3>
                      {!isEditingNotes && (
                        <button
                          onClick={handleStartEditingNotes}
                          className="flex items-center gap-2 px-3 py-1 text-sm text-blue-600 hover:text-blue-700 hover:bg-blue-50 rounded-lg transition-colors"
                        >
                          <Edit className="w-4 h-4" />
                          Edit Notes
                        </button>
                      )}
                    </div>

                    {isEditingNotes ? (
                      <div className="space-y-4">
                        <textarea
                          value={notesText}
                          onChange={(e) => setNotesText(e.target.value)}
                          placeholder="Add internal notes about this candidate..."
                          className="w-full h-32 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none"
                        />
                        <div className="flex items-center gap-2">
                          <button
                            onClick={handleSaveNotes}
                            disabled={savingNotes}
                            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                          >
                            <Save className="w-4 h-4" />
                            {savingNotes ? 'Saving...' : 'Save Notes'}
                          </button>
                          <button
                            onClick={handleCancelEditingNotes}
                            disabled={savingNotes}
                            className="flex items-center gap-2 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                          >
                            <X className="w-4 h-4" />
                            Cancel
                          </button>
                        </div>
                      </div>
                    ) : (
                      <div className="prose max-w-none">
                        {candidate.internal_notes ? (
                          <p className="text-gray-700 whitespace-pre-wrap">
                            {candidate.internal_notes}
                          </p>
                        ) : (
                          <p className="text-gray-500 italic">No notes available</p>
                        )}
                      </div>
                    )}
                  </div>

                  {/* File Attachments Section */}
                  <div>
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="text-lg font-semibold text-gray-900">
                        Attached Files
                      </h3>
                      <label className="flex items-center gap-2 px-3 py-1 text-sm text-blue-600 hover:text-blue-700 hover:bg-blue-50 rounded-lg transition-colors cursor-pointer">
                        <Plus className="w-4 h-4" />
                        Add File
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
                        <p className="text-gray-500 mb-2">No files attached</p>
                        <p className="text-sm text-gray-400">Click "Add File" to attach documents</p>
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
                                title="Download file"
                              >
                                <Download className="w-4 h-4" />
                              </button>
                              <button
                                onClick={() => handleDeleteFile(file.id)}
                                className="p-1 text-gray-500 hover:text-red-600 transition-colors"
                                title="Delete file"
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
                        <p className="text-sm text-gray-600">Uploading file...</p>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* History Tab - Phase 12: Stage Timeline */}
              {activeTab === 'history' && (
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Stage Timeline</h3>
                  <StageTimeline candidate={candidate} companyId={getCompanyId() || ''} />
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Status Card */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Status</h3>
            <div className="space-y-4">
              {/* Current Status */}
              <div>
                <label className="text-sm text-gray-600 block mb-2">Current Status</label>
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

              {/* Priority */}
              <div>
                <label className="text-sm text-gray-600 block mb-2">Priority</label>
                <span
                  className={`inline-block px-3 py-1 text-sm font-medium rounded-full ${getPriorityColor(
                    candidate.priority
                  )}`}
                >
                  {candidate.priority}
                </span>
              </div>

              {/* Ownership */}
              <div>
                <label className="text-sm text-gray-600 block mb-2">Ownership</label>
                <span
                  className={`inline-block px-3 py-1 text-sm font-medium rounded-full ${getOwnershipColor(
                    candidate.ownership_status
                  )}`}
                >
                  {candidate.ownership_status.replace('_', ' ')}
                </span>
              </div>
            </div>
          </div>

          {/* Dates Card */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Dates</h3>
            <div className="space-y-3 text-sm">
              <div>
                <span className="text-gray-600">Created:</span>
                <p className="font-medium text-gray-900">
                  {new Date(candidate.created_at).toLocaleDateString()}
                </p>
              </div>
              <div>
                <span className="text-gray-600">Last Updated:</span>
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
