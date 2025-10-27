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
  Clock
} from 'lucide-react';
import { companyCandidateService } from '../../services/companyCandidateService';
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
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">
                    Internal Notes
                  </h3>
                  {candidate.internal_notes ? (
                    <div className="prose max-w-none">
                      <p className="text-gray-700 whitespace-pre-wrap">
                        {candidate.internal_notes}
                      </p>
                    </div>
                  ) : (
                    <p className="text-gray-500 italic">No notes available</p>
                  )}
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
