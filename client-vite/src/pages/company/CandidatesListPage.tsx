import { useState, useEffect } from 'react';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import {
  Plus,
  Search,
  Eye,
  Edit,
  Archive,
  UserPlus,
  Briefcase,
  Flag,
  Building2,
  User,
  MessageSquare
} from 'lucide-react';
import { companyCandidateService } from '../../services/companyCandidateService';
import type { CompanyCandidate } from '../../types/companyCandidate';
import { Tooltip } from '../../components/ui/Tooltip';

// Helper functions for icons (unused but kept for potential future use)
/*
const _getStatusIcon = (status: string) => {
  switch (status) {
    case 'ACTIVE':
      return null; // Don't show icon for active status
    case 'PENDING_INVITATION':
      return <Clock className="w-4 h-4 text-yellow-600" />;
    case 'PENDING_CONFIRMATION':
      return <AlertCircle className="w-4 h-4 text-blue-600" />;
    case 'REJECTED':
      return <XCircle className="w-4 h-4 text-red-600" />;
    case 'ARCHIVED':
      return <Archive className="w-4 h-4 text-gray-600" />;
    default:
      return <AlertCircle className="w-4 h-4 text-gray-600" />;
  }
};
*/

const getPriorityIcon = (priority: string) => {
  switch (priority) {
    case 'HIGH':
      return <Flag className="w-4 h-4 text-red-600" />;
    case 'MEDIUM':
      return null; // Don't show icon for medium priority
    case 'LOW':
      return <Flag className="w-4 h-4 text-green-600" />;
    default:
      return null;
  }
};

const getOwnershipIcon = (ownership: string) => {
  switch (ownership) {
    case 'COMPANY_OWNED':
      return <Building2 className="w-4 h-4 text-blue-600" />;
    case 'USER_OWNED':
      return <User className="w-4 h-4 text-purple-600" />;
    default:
      return <User className="w-4 h-4 text-gray-600" />;
  }
};

/*
const _getStatusLabel = (status: string) => {
  return status.replace(/_/g, ' ').toLowerCase().replace(/\b\w/g, l => l.toUpperCase());
};
*/

export default function CandidatesListPage() {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const phaseId = searchParams.get('phase'); // Get phase from URL

  const [candidates, setCandidates] = useState<CompanyCandidate[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('');
  const [priorityFilter, setPriorityFilter] = useState<string>('');

  // Modal state for assigning position
  const [showPositionModal, setShowPositionModal] = useState(false);
  const [selectedCandidateForPosition, setSelectedCandidateForPosition] = useState<CompanyCandidate | null>(null);
  const [positions, setPositions] = useState<any[]>([]);
  const [loadingPositions, setLoadingPositions] = useState(false);

  // Get company_id from JWT token
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
    loadCandidates();
  }, [phaseId]); // Reload when phase changes

  const loadCandidates = async () => {
    try {
      setLoading(true);
      const companyId = getCompanyId();
      if (!companyId) {
        setError('Company ID not found');
        return;
      }

      const data = await companyCandidateService.listByCompany(companyId);
      setCandidates(data);
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to load candidates');
      console.error('Error loading candidates:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleArchive = async (candidateId: string) => {
    if (!confirm('Are you sure you want to archive this candidate?')) return;

    try {
      await companyCandidateService.archive(candidateId);
      loadCandidates();
    } catch (err: any) {
      alert('Failed to archive candidate: ' + err.message);
    }
  };

  const handleOpenPositionModal = async (candidate: CompanyCandidate) => {
    setSelectedCandidateForPosition(candidate);
    setShowPositionModal(true);

    // Load open positions
    try {
      setLoadingPositions(true);
      const companyId = getCompanyId();
      if (!companyId) return;

      // Import PositionService dynamically to avoid circular dependencies
      const { PositionService } = await import('../../services/positionService');
      const response = await PositionService.getPositions({
        company_id: companyId,
      });
      setPositions(response.positions || []);
    } catch (err: any) {
      console.error('Error loading positions:', err);
      setPositions([]);
    } finally {
      setLoadingPositions(false);
    }
  };

  const handleAssignPosition = async (positionId: string) => {
    if (!selectedCandidateForPosition) return;

    try {
      // Import ApiClient
      const { ApiClient } = await import('../../lib/api');

      // Create candidate_application via company endpoint
      await ApiClient.post('/api/company/candidate-applications/', {
        candidate_id: selectedCandidateForPosition.candidate_id,
        job_position_id: positionId,
      }, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
      });

      // Close modal and reload candidates
      setShowPositionModal(false);
      setSelectedCandidateForPosition(null);
      loadCandidates();

      alert('Position assigned successfully!');
    } catch (err: any) {
      alert('Failed to assign position: ' + err.message);
      console.error('Error assigning position:', err);
    }
  };

  const filteredCandidates = candidates.filter((candidate) => {
    const matchesSearch =
      !searchTerm ||
      candidate.candidate_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      candidate.candidate_email?.toLowerCase().includes(searchTerm.toLowerCase());

    const matchesStatus = !statusFilter || candidate.status === statusFilter;
    const matchesPriority = !priorityFilter || candidate.priority === priorityFilter;

    // Phase 12: Filter by phase_id from URL
    const matchesPhase = !phaseId || candidate.phase_id === phaseId;

    return matchesSearch && matchesStatus && matchesPriority && matchesPhase;
  });

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div>
      {/* Header */}
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">{t('company.candidates.title')}</h1>
          <p className="text-gray-600 mt-1">{t('company.candidates.managePipeline', { defaultValue: 'Manage your candidate pipeline' })}</p>
        </div>
        <Link
          to="/company/candidates/add"
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          <Plus className="w-5 h-5" />
          {t('company.candidates.addCandidate')}
        </Link>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Search */}
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder={t('company.candidates.search')}
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          {/* Status Filter */}
          <div>
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="">All Status</option>
              <option value="PENDING_INVITATION">Pending Invitation</option>
              <option value="PENDING_CONFIRMATION">Pending Confirmation</option>
              <option value="ACTIVE">Active</option>
              <option value="REJECTED">Rejected</option>
              <option value="ARCHIVED">Archived</option>
            </select>
          </div>

          {/* Priority Filter */}
          <div>
            <select
              value={priorityFilter}
              onChange={(e) => setPriorityFilter(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="">All Priorities</option>
              <option value="HIGH">High</option>
              <option value="MEDIUM">Medium</option>
              <option value="LOW">Low</option>
            </select>
          </div>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
          <p className="text-red-800">{error}</p>
        </div>
      )}

      {/* Candidates Table */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
        {filteredCandidates.length === 0 ? (
          <div className="text-center py-12">
            <UserPlus className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No candidates found</h3>
            <p className="text-gray-600 mb-4">
              {searchTerm || statusFilter || priorityFilter
                ? 'Try adjusting your filters'
                : 'Start by adding your first candidate'}
            </p>
            {!searchTerm && !statusFilter && !priorityFilter && (
              <Link
                to="/company/candidates/add"
                className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                <Plus className="w-5 h-5" />
                Add Candidate
              </Link>
            )}
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-[90%]">
                <thead className="bg-gray-50 border-b border-gray-200">
                <tr>
                  <th className="px-2 py-3 w-[50px] max-w-[50px] min-w-[50px]">
                    {/* Empty header for icons column */}
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-1/4">
                    Candidate
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-1/4">
                    Position / Stage
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-1/6">
                    Tags
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider w-32">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {filteredCandidates.map((candidate) => (
                  <tr key={candidate.id} className="hover:bg-gray-50">
                    <td className="px-2 py-4 whitespace-nowrap w-[50px] max-w-[50px] min-w-[50px]">
                      <div className="flex items-center gap-1 justify-center">
                        {getPriorityIcon(candidate.priority) && (
                          <Tooltip text={candidate.priority.charAt(0).toUpperCase() + candidate.priority.slice(1)}>
                            {getPriorityIcon(candidate.priority)}
                          </Tooltip>
                        )}
                        {candidate.ownership_status === 'COMPANY_OWNED' && (
                          <Tooltip text="Company Owned">
                            {getOwnershipIcon(candidate.ownership_status)}
                          </Tooltip>
                        )}
                        {(candidate.pending_comments_count ?? 0) > 0 && (
                          <Tooltip text={`${candidate.pending_comments_count} pending comment${candidate.pending_comments_count! > 1 ? 's' : ''}`}>
                            <div className="relative">
                              <MessageSquare className="w-4 h-4 text-yellow-600" />
                              <span className="absolute -top-1 -right-1 bg-yellow-600 text-white text-xs font-bold rounded-full w-4 h-4 flex items-center justify-center">
                                {candidate.pending_comments_count! > 9 ? '9+' : candidate.pending_comments_count}
                              </span>
                            </div>
                          </Tooltip>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="min-w-[200px] max-w-[300px]">
                        <button
                          onClick={() => navigate(`/company/candidates/${candidate.id}`)}
                          className={`text-sm font-medium text-gray-900 truncate hover:text-blue-600 hover:underline cursor-pointer text-left ${
                            candidate.status?.toLowerCase() === 'archived' ? 'line-through' : ''
                          }`}
                        >
                          {candidate.candidate_name || 'N/A'}
                        </button>
                        <div className="text-sm text-gray-500 truncate">
                          {candidate.candidate_email || 'N/A'}
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      {candidate.job_position_title ? (
                        <>
                          <button
                            onClick={() => navigate(`/company/positions/${candidate.job_position_id}`)}
                            className="text-sm font-medium text-blue-600 hover:text-blue-800 hover:underline cursor-pointer text-left"
                          >
                            {candidate.job_position_title}
                          </button>
                          {candidate.application_status && (
                            <div className="text-xs text-gray-500">
                              Status: {candidate.application_status}
                            </div>
                          )}
                          {candidate.current_workflow_id && candidate.current_stage_id && (
                            <div className="text-xs text-gray-500">
                              {candidate.stage_name} - {candidate.workflow_name}
                            </div>
                          )}
                        </>
                      ) : candidate.current_workflow_id && candidate.current_stage_id ? (
                        <>
                          <div className="text-sm text-gray-900">
                            {candidate.stage_name || 'No stage'}
                          </div>
                          <div className="text-xs text-gray-500">
                            {candidate.workflow_name || ''}
                          </div>
                        </>
                      ) : (
                        <button
                          onClick={() => handleOpenPositionModal(candidate)}
                          className="inline-flex items-center gap-1 px-3 py-1 text-xs text-blue-600 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors whitespace-nowrap"
                        >
                          <Briefcase className="w-3 h-3" />
                          Assign Position
                        </button>
                      )}
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex flex-wrap gap-1">
                        {candidate.tags.slice(0, 2).map((tag, idx) => (
                          <span
                            key={idx}
                            className="px-2 py-1 text-xs bg-gray-100 text-gray-700 rounded-full"
                          >
                            {tag}
                          </span>
                        ))}
                        {candidate.tags.length > 2 && (
                          <span className="px-2 py-1 text-xs bg-gray-100 text-gray-700 rounded-full">
                            +{candidate.tags.length - 2}
                          </span>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <div className="flex items-center justify-end gap-2">
                        <Tooltip text="View candidate details">
                          <button
                            onClick={() => navigate(`/company/candidates/${candidate.id}`)}
                            className="text-blue-600 hover:text-blue-900 p-1 rounded hover:bg-blue-50 transition-colors"
                          >
                            <Eye className="w-5 h-5" />
                          </button>
                        </Tooltip>
                        <Tooltip text="Edit candidate">
                          <button
                            onClick={() => navigate(`/company/candidates/${candidate.id}/edit`)}
                            className="text-green-600 hover:text-green-900 p-1 rounded hover:bg-green-50 transition-colors"
                          >
                            <Edit className="w-5 h-5" />
                          </button>
                        </Tooltip>
                        <Tooltip text="Archive candidate">
                          <button
                            onClick={() => handleArchive(candidate.id)}
                            className="text-red-600 hover:text-red-900 p-1 rounded hover:bg-red-50 transition-colors"
                          >
                            <Archive className="w-5 h-5" />
                          </button>
                        </Tooltip>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Summary */}
      {filteredCandidates.length > 0 && (
        <div className="mt-4 text-sm text-gray-600">
          Showing {filteredCandidates.length} of {candidates.length} candidates
        </div>
      )}

      {/* Assign Position Modal */}
      {showPositionModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full mx-4 max-h-[80vh] overflow-hidden flex flex-col">
            {/* Modal Header */}
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-xl font-bold text-gray-900">Assign Position</h2>
              {selectedCandidateForPosition && (
                <p className="text-sm text-gray-600 mt-1">
                  Select an open position for {selectedCandidateForPosition.candidate_name}
                </p>
              )}
            </div>

            {/* Modal Body */}
            <div className="px-6 py-4 overflow-y-auto flex-1">
              {loadingPositions ? (
                <div className="flex items-center justify-center py-12">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                </div>
              ) : positions.length === 0 ? (
                <div className="text-center py-12">
                  <Briefcase className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-600">No open positions available</p>
                  <button
                    onClick={() => navigate('/company/positions/create')}
                    className="mt-4 text-blue-600 hover:text-blue-700 text-sm font-medium"
                  >
                    Create a new position
                  </button>
                </div>
              ) : (
                <div className="space-y-3">
                  {positions.map((position) => (
                    <button
                      key={position.id}
                      onClick={() => handleAssignPosition(position.id)}
                      className="w-full text-left p-4 border border-gray-200 rounded-lg hover:border-blue-500 hover:bg-blue-50 transition-all"
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <h3 className="font-semibold text-gray-900">{position.title}</h3>
                          <p className="text-sm text-gray-600 mt-1">{position.department || 'No department'}</p>
                          <div className="flex items-center gap-4 mt-2 text-xs text-gray-500">
                            <span>{position.location || 'Remote'}</span>
                            <span>•</span>
                            <span>{position.work_location || 'Full-time'}</span>
                          </div>
                        </div>
                        <div className="ml-4">
                          <span className="px-2 py-1 text-xs font-medium rounded-full bg-green-100 text-green-800">
                            Open
                          </span>
                        </div>
                      </div>
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Modal Footer */}
            <div className="px-6 py-4 border-t border-gray-200 flex justify-end">
              <button
                onClick={() => {
                  setShowPositionModal(false);
                  setSelectedCandidateForPosition(null);
                }}
                className="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
