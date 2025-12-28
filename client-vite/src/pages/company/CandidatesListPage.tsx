import { useState, useEffect, useMemo } from 'react';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useCompanyNavigation } from '../../hooks/useCompanyNavigation';
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
  MessageSquare,
  Kanban,
  Mail,
  CheckSquare,
} from 'lucide-react';
import { companyCandidateService } from '../../services/companyCandidateService';
import { PositionService } from '../../services/positionService';
import { ApiClient } from '../../lib/api';
import type { CompanyCandidate } from '../../types/companyCandidate';
import { BulkEmailModal } from '../../components/company/email/BulkEmailModal';
import { useFilterState, type FilterConfig } from '../../hooks/useFilterState';
import { SavedFiltersDropdown } from '../../components/filters/SavedFiltersDropdown';
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
} from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

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

// Filter configuration for candidates list
const candidateFilterConfig: FilterConfig[] = [
  { key: 'search', type: 'string', defaultValue: '' },
  { key: 'status', type: 'string', defaultValue: '' },
  { key: 'priority', type: 'string', defaultValue: '' },
  { key: 'phase', type: 'string', defaultValue: '' },
];

interface CandidateFilters {
  search: string;
  status: string;
  priority: string;
  phase: string;
}

export default function CandidatesListPage() {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { getPath } = useCompanyNavigation();
  const [searchParams] = useSearchParams();

  // Get phaseId from URL for backward compatibility with workflow board links
  const phaseId = searchParams.get('phase') || '';

  // Use the new filter hook with URL persistence
  const {
    filters,
    setFilter,
    clearFilters,
    hasActiveFilters,
    activeFilterCount,
    savedFilters,
    saveFilter,
    loadFilter,
    deleteFilter,
    setDefaultFilter
  } = useFilterState<CandidateFilters>({
    config: candidateFilterConfig,
    persistToUrl: true,
    storageKey: 'candidates_filters'
  });

  const [candidates, setCandidates] = useState<CompanyCandidate[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Modal state for assigning position
  const [showPositionModal, setShowPositionModal] = useState(false);
  const [selectedCandidateForPosition, setSelectedCandidateForPosition] = useState<CompanyCandidate | null>(null);
  const [positions, setPositions] = useState<any[]>([]);
  const [loadingPositions, setLoadingPositions] = useState(false);

  // Selection state for bulk actions
  const [selectedCandidates, setSelectedCandidates] = useState<Set<string>>(new Set());
  const [showBulkEmailModal, setShowBulkEmailModal] = useState(false);

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

  const filteredCandidates = useMemo(() => {
    return candidates.filter((candidate) => {
      const searchTerm = filters.search.toLowerCase();
      const matchesSearch =
        !searchTerm ||
        candidate.candidate_name?.toLowerCase().includes(searchTerm) ||
        candidate.candidate_email?.toLowerCase().includes(searchTerm);

      const matchesStatus = !filters.status || candidate.status === filters.status;
      const matchesPriority = !filters.priority || candidate.priority === filters.priority;

      // Filter by phase_id from URL (backward compatibility with workflow board links)
      // or from filter state
      const effectivePhase = phaseId || filters.phase;
      const matchesPhase = !effectivePhase || candidate.phase_id === effectivePhase;

      return matchesSearch && matchesStatus && matchesPriority && matchesPhase;
    });
  }, [candidates, filters, phaseId]);

  // Selection handlers for bulk actions
  const toggleCandidateSelection = (candidateId: string) => {
    setSelectedCandidates(prev => {
      const next = new Set(prev);
      if (next.has(candidateId)) {
        next.delete(candidateId);
      } else {
        next.add(candidateId);
      }
      return next;
    });
  };

  const toggleSelectAll = () => {
    if (selectedCandidates.size === filteredCandidates.length) {
      setSelectedCandidates(new Set());
    } else {
      setSelectedCandidates(new Set(filteredCandidates.map(c => c.id)));
    }
  };

  const clearSelection = () => {
    setSelectedCandidates(new Set());
  };

  const getSelectedCandidatesData = (): CompanyCandidate[] => {
    return filteredCandidates.filter(c => selectedCandidates.has(c.id));
  };

  // Get workflow_id from first selected candidate (for bulk email)
  const getSelectedWorkflowId = (): string => {
    const selected = getSelectedCandidatesData();
    return selected[0]?.workflow_id || '';
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <TooltipProvider delayDuration={200} skipDelayDuration={100}>
      <div>
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">{t('company.candidates.title')}</h1>
            <p className="text-gray-600 mt-1">{t('company.candidates.managePipeline', { defaultValue: 'Manage your candidate pipeline' })}</p>
          </div>
          <Button asChild>
            <Link to={getPath('candidates/add')}>
              <Plus className="w-5 h-5" />
              {t('company.candidates.addCandidate')}
            </Link>
          </Button>
        </div>

        {/* Back to Kanban View Button */}
        {phaseId && (
          <div className="flex items-center gap-4">
            <Button variant="outline" asChild>
              <Link to={getPath(`workflow-board?phase=${phaseId}`)}>
                <Kanban className="w-4 h-4" />
                {t('company.workflowBoard.kanbanView', { defaultValue: 'Kanban View' })}
              </Link>
            </Button>
          </div>
        )}
      </div>

      {/* Bulk Actions Bar */}
      {selectedCandidates.size > 0 && (
        <div className="mb-4 p-4 bg-blue-50 border border-blue-200 rounded-lg flex items-center justify-between">
          <div className="flex items-center gap-3">
            <CheckSquare className="w-5 h-5 text-blue-600" />
            <span className="text-blue-800 font-medium">
              {selectedCandidates.size} candidate{selectedCandidates.size !== 1 ? 's' : ''} selected
            </span>
            <button
              onClick={clearSelection}
              className="text-blue-600 hover:text-blue-800 text-sm underline"
            >
              Clear selection
            </button>
          </div>
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              onClick={() => setShowBulkEmailModal(true)}
              disabled={!getSelectedWorkflowId()}
              title={!getSelectedWorkflowId() ? 'Selected candidates must have a workflow' : ''}
            >
              <Mail className="w-4 h-4" />
              Send Bulk Email
            </Button>
          </div>
        </div>
      )}

      {/* Filters */}
      <Card className="mb-6">
        <CardContent className="pt-6">
          <div className="flex flex-col gap-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {/* Search */}
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                <input
                  type="text"
                  placeholder={t('company.candidates.search')}
                  value={filters.search}
                  onChange={(e) => setFilter('search', e.target.value)}
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>

              {/* Status Filter */}
              <Select value={filters.status || "all"} onValueChange={(value) => setFilter('status', value === "all" ? "" : value)}>
                <SelectTrigger>
                  <SelectValue placeholder={t('filters.allStatus', 'All Status')} />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">{t('filters.allStatus', 'All Status')}</SelectItem>
                  <SelectItem value="PENDING_INVITATION">{t('filters.pendingInvitation', 'Pending Invitation')}</SelectItem>
                  <SelectItem value="PENDING_CONFIRMATION">{t('filters.pendingConfirmation', 'Pending Confirmation')}</SelectItem>
                  <SelectItem value="ACTIVE">{t('filters.active', 'Active')}</SelectItem>
                  <SelectItem value="REJECTED">{t('filters.rejected', 'Rejected')}</SelectItem>
                  <SelectItem value="ARCHIVED">{t('filters.archived', 'Archived')}</SelectItem>
                </SelectContent>
              </Select>

              {/* Priority Filter */}
              <Select value={filters.priority || "all"} onValueChange={(value) => setFilter('priority', value === "all" ? "" : value)}>
                <SelectTrigger>
                  <SelectValue placeholder={t('filters.allPriorities', 'All Priorities')} />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">{t('filters.allPriorities', 'All Priorities')}</SelectItem>
                  <SelectItem value="HIGH">{t('filters.high', 'High')}</SelectItem>
                  <SelectItem value="MEDIUM">{t('filters.medium', 'Medium')}</SelectItem>
                  <SelectItem value="LOW">{t('filters.low', 'Low')}</SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* Saved Filters */}
            <div className="flex justify-end">
              <SavedFiltersDropdown
                savedFilters={savedFilters}
                onSaveFilter={saveFilter}
                onLoadFilter={loadFilter}
                onDeleteFilter={deleteFilter}
                onSetDefault={setDefaultFilter}
                onClearFilters={clearFilters}
                hasActiveFilters={hasActiveFilters}
                activeFilterCount={activeFilterCount}
              />
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Error Message */}
      {error && (
        <Card className="mb-6 border-red-200 bg-red-50">
          <CardContent className="pt-6">
            <p className="text-red-800">{error}</p>
          </CardContent>
        </Card>
      )}

      {/* Candidates Table */}
      <Card>
        {filteredCandidates.length === 0 ? (
          <CardContent className="text-center py-12">
            <UserPlus className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">{t('company.candidates.noCandidates', 'No candidates found')}</h3>
            <p className="text-gray-600 mb-4">
              {hasActiveFilters
                ? t('filters.tryAdjusting', 'Try adjusting your filters')
                : t('company.candidates.addFirstCandidate', 'Start by adding your first candidate')}
            </p>
            {!hasActiveFilters && (
              <Button asChild>
                <Link to={getPath('candidates/add')}>
                  <Plus className="w-5 h-5" />
                  {t('company.candidates.addCandidate')}
                </Link>
              </Button>
            )}
          </CardContent>
        ) : (
          <CardContent className="p-0">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className="w-[40px]">
                    <input
                      type="checkbox"
                      checked={selectedCandidates.size === filteredCandidates.length && filteredCandidates.length > 0}
                      onChange={toggleSelectAll}
                      className="w-4 h-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                    />
                  </TableHead>
                  <TableHead className="w-[50px] max-w-[50px] min-w-[50px]">
                    {/* Empty header for icons column */}
                  </TableHead>
                  <TableHead className="w-1/4">Candidate</TableHead>
                  <TableHead className="w-1/4">Position / Stage</TableHead>
                  <TableHead className="w-1/6">Tags</TableHead>
                  <TableHead className="text-right w-32">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredCandidates.map((candidate) => (
                  <TableRow key={candidate.id} className={selectedCandidates.has(candidate.id) ? 'bg-blue-50' : ''}>
                    <TableCell className="w-[40px]">
                      <input
                        type="checkbox"
                        checked={selectedCandidates.has(candidate.id)}
                        onChange={() => toggleCandidateSelection(candidate.id)}
                        className="w-4 h-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                        onClick={(e) => e.stopPropagation()}
                      />
                    </TableCell>
                    <TableCell className="w-[50px] max-w-[50px] min-w-[50px]">
                      <div className="flex items-center gap-1 justify-center">
                        {getPriorityIcon(candidate.priority) && (
                          <Tooltip>
                            <TooltipTrigger asChild>
                              <span className="inline-flex">{getPriorityIcon(candidate.priority)}</span>
                            </TooltipTrigger>
                            <TooltipContent>
                              <p>{candidate.priority.charAt(0).toUpperCase() + candidate.priority.slice(1)}</p>
                            </TooltipContent>
                          </Tooltip>
                        )}
                        {candidate.ownership_status === 'COMPANY_OWNED' && (
                          <Tooltip>
                            <TooltipTrigger asChild>
                              <span className="inline-flex">{getOwnershipIcon(candidate.ownership_status)}</span>
                            </TooltipTrigger>
                            <TooltipContent>
                              <p>Company Owned</p>
                            </TooltipContent>
                          </Tooltip>
                        )}
                        {(candidate.pending_comments_count ?? 0) > 0 && (
                          <Tooltip>
                            <TooltipTrigger asChild>
                              <div className="relative">
                                <MessageSquare className="w-4 h-4 text-yellow-600" />
                                <span className="absolute -top-1 -right-1 bg-yellow-600 text-white text-xs font-bold rounded-full w-4 h-4 flex items-center justify-center">
                                  {candidate.pending_comments_count! > 9 ? '9+' : candidate.pending_comments_count}
                                </span>
                              </div>
                            </TooltipTrigger>
                            <TooltipContent>
                              <p>{candidate.pending_comments_count} pending comment{candidate.pending_comments_count! > 1 ? 's' : ''}</p>
                            </TooltipContent>
                          </Tooltip>
                        )}
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="min-w-[200px] max-w-[300px]">
                        <button
                          onClick={() => navigate(getPath(`candidates/${candidate.id}`))}
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
                    </TableCell>
                    <TableCell>
                      {candidate.job_position_title ? (
                        <>
                          <button
                            onClick={() => navigate(getPath(`positions/${candidate.job_position_id}`))}
                            className="text-sm font-medium text-blue-600 hover:text-blue-800 hover:underline cursor-pointer text-left"
                          >
                            {candidate.job_position_title}
                          </button>
                          {(candidate.workflow_name || candidate.stage_name) && (
                            <div className="text-xs text-gray-500 mt-1 flex items-center gap-1">
                              {candidate.stage_style?.icon && (
                                <span 
                                  className="text-sm"
                                  dangerouslySetInnerHTML={{ __html: candidate.stage_style.icon }}
                                />
                              )}
                              <span style={{ color: candidate.stage_style?.color || candidate.stage_style?.text_color || undefined }}>
                                {candidate.workflow_name || 'No workflow'} - {candidate.stage_name || 'No stage'}
                              </span>
                            </div>
                          )}
                        </>
                      ) : (candidate.workflow_name || candidate.stage_name) ? (
                        <>
                          <div className="text-sm font-medium text-gray-900 flex items-center gap-2">
                            {candidate.stage_style?.icon && (
                              <span 
                                className="text-base"
                                dangerouslySetInnerHTML={{ __html: candidate.stage_style.icon }}
                              />
                            )}
                            <span style={{ color: candidate.stage_style?.color || candidate.stage_style?.text_color || undefined }}>
                              {candidate.workflow_name || 'No workflow'}
                            </span>
                          </div>
                          <div className="text-xs text-gray-500">
                            {candidate.stage_name || 'No stage'}
                          </div>
                        </>
                      ) : (
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => handleOpenPositionModal(candidate)}
                          className="whitespace-nowrap"
                        >
                          <Briefcase className="w-3 h-3" />
                          Assign Position
                        </Button>
                      )}
                    </TableCell>
                    <TableCell>
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
                    </TableCell>
                    <TableCell className="text-right">
                      <div className="flex items-center justify-end gap-2">
                        <Tooltip>
                          <TooltipTrigger asChild>
                            <Button
                              variant="ghost"
                              size="icon"
                              onClick={() => navigate(getPath(`candidates/${candidate.id}`))}
                            >
                              <Eye className="w-5 h-5" />
                            </Button>
                          </TooltipTrigger>
                          <TooltipContent>
                            <p>View candidate details</p>
                          </TooltipContent>
                        </Tooltip>
                        <Tooltip>
                          <TooltipTrigger asChild>
                            <Button
                              variant="ghost"
                              size="icon"
                              onClick={() => navigate(getPath(`candidates/${candidate.id}/edit`))}
                              className="text-green-600 hover:text-green-900"
                            >
                              <Edit className="w-5 h-5" />
                            </Button>
                          </TooltipTrigger>
                          <TooltipContent>
                            <p>Edit candidate</p>
                          </TooltipContent>
                        </Tooltip>
                        <Tooltip>
                          <TooltipTrigger asChild>
                            <Button
                              variant="ghost"
                              size="icon"
                              onClick={() => handleArchive(candidate.id)}
                              className="text-red-600 hover:text-red-900"
                            >
                              <Archive className="w-5 h-5" />
                            </Button>
                          </TooltipTrigger>
                          <TooltipContent>
                            <p>Archive candidate</p>
                          </TooltipContent>
                        </Tooltip>
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        )}
      </Card>

      {/* Summary */}
      {filteredCandidates.length > 0 && (
        <div className="mt-4 text-sm text-gray-600">
          Showing {filteredCandidates.length} of {candidates.length} candidates
        </div>
      )}

      {/* Bulk Email Modal */}
      <BulkEmailModal
        isOpen={showBulkEmailModal}
        onClose={() => {
          setShowBulkEmailModal(false);
          clearSelection();
        }}
        candidates={getSelectedCandidatesData()}
        workflowId={getSelectedWorkflowId()}
        companyName="Company"
        positionTitle="Position"
      />

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
                  <Button variant="link" onClick={() => navigate(getPath('positions/create'))}>
                    Create a new position
                  </Button>
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
              <Button
                variant="outline"
                onClick={() => {
                  setShowPositionModal(false);
                  setSelectedCandidateForPosition(null);
                }}
              >
                Cancel
              </Button>
            </div>
          </div>
        </div>
      )}
      </div>
    </TooltipProvider>
  );
}
