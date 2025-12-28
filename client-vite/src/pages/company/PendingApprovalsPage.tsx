/**
 * PendingApprovalsPage Component
 * Lists positions pending approval for authorized users
 */
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCompanyNavigation } from '../../hooks/useCompanyNavigation';
import {
  ArrowLeft,
  CheckCircle,
  XCircle,
  Eye,
  Clock,
  User,
  Calendar,
  Briefcase,
  Search,
  Filter,
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { PositionService } from '../../services/positionService';
import type { Position } from '../../types/position';
import {
  StatusBadge,
  EmploymentTypeBadge,
  RejectPositionModal,
} from '../../components/jobPosition/publishing';

export default function PendingApprovalsPage() {
  const navigate = useNavigate();
  const { getPath } = useCompanyNavigation();
  const [positions, setPositions] = useState<Position[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [actionLoading, setActionLoading] = useState<string | null>(null);

  // Filters
  const [searchQuery, setSearchQuery] = useState('');
  const [sortBy, setSortBy] = useState<'date' | 'title' | 'requester'>('date');

  // Reject modal
  const [showRejectModal, setShowRejectModal] = useState(false);
  const [selectedPosition, setSelectedPosition] = useState<Position | null>(null);

  useEffect(() => {
    loadPendingApprovals();
  }, []);

  const loadPendingApprovals = async () => {
    try {
      setLoading(true);
      const data = await PositionService.getPendingApprovals();
      setPositions(data);
      setError(null);
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to load pending approvals';
      setError(errorMessage);
      console.error('Error loading pending approvals:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async (positionId: string) => {
    setActionLoading(positionId);
    try {
      await PositionService.approve(positionId);
      await loadPendingApprovals();
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to approve';
      setError(errorMessage);
    } finally {
      setActionLoading(null);
    }
  };

  const handleReject = async (reason: string) => {
    if (!selectedPosition) return;
    setActionLoading(selectedPosition.id);
    try {
      await PositionService.reject(selectedPosition.id, reason);
      await loadPendingApprovals();
      setShowRejectModal(false);
      setSelectedPosition(null);
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to reject';
      setError(errorMessage);
    } finally {
      setActionLoading(null);
    }
  };

  const openRejectModal = (position: Position) => {
    setSelectedPosition(position);
    setShowRejectModal(true);
  };

  // Filter and sort positions
  const filteredPositions = positions
    .filter((p) => {
      if (!searchQuery) return true;
      const query = searchQuery.toLowerCase();
      return (
        p.title.toLowerCase().includes(query) ||
        p.job_category?.toLowerCase().includes(query) ||
        p.created_by_name?.toLowerCase().includes(query)
      );
    })
    .sort((a, b) => {
      switch (sortBy) {
        case 'title':
          return a.title.localeCompare(b.title);
        case 'requester':
          return (a.created_by_name || '').localeCompare(b.created_by_name || '');
        case 'date':
        default:
          return new Date(b.submitted_at || b.created_at || 0).getTime() -
                 new Date(a.submitted_at || a.created_at || 0).getTime();
      }
    });

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto p-6">
      {/* Header */}
      <div className="mb-6">
        <Button
          variant="ghost"
          onClick={() => navigate(getPath('positions'))}
          className="mb-4"
        >
          <ArrowLeft className="w-5 h-5 mr-2" />
          Back to Positions
        </Button>

        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Pending Approvals</h1>
            <p className="text-gray-600 mt-1">
              Review and approve job positions waiting for approval
            </p>
          </div>
          <Badge variant="secondary" className="text-lg px-4 py-2">
            {filteredPositions.length} pending
          </Badge>
        </div>
      </div>

      {/* Error Alert */}
      {error && (
        <Alert variant="destructive" className="mb-4">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Filters */}
      <div className="flex items-center gap-4 mb-6">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
          <Input
            type="text"
            placeholder="Search by title, category, or requester..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10"
          />
        </div>

        <div className="flex items-center gap-2">
          <Filter className="w-4 h-4 text-gray-400" />
          <Select value={sortBy} onValueChange={(v) => setSortBy(v as typeof sortBy)}>
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Sort by" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="date">Date Submitted</SelectItem>
              <SelectItem value="title">Title</SelectItem>
              <SelectItem value="requester">Requester</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      {/* Empty State */}
      {filteredPositions.length === 0 ? (
        <Card>
          <CardContent className="flex flex-col items-center justify-center py-12">
            <CheckCircle className="w-16 h-16 text-green-400 mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              All caught up!
            </h3>
            <p className="text-gray-600 text-center max-w-md">
              {searchQuery
                ? 'No positions match your search criteria'
                : 'There are no positions pending approval at this time'}
            </p>
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-4">
          {filteredPositions.map((position) => {
            const isLoading = actionLoading === position.id;

            return (
              <Card key={position.id} className="hover:shadow-md transition-shadow">
                <CardContent className="p-6">
                  <div className="flex items-start justify-between">
                    {/* Position Info */}
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <h3 className="text-lg font-semibold text-gray-900">
                          {position.title}
                        </h3>
                        <StatusBadge status={position.status} size="sm" />
                        {position.employment_type && (
                          <EmploymentTypeBadge type={position.employment_type} size="sm" />
                        )}
                      </div>

                      <div className="flex flex-wrap items-center gap-4 text-sm text-gray-600">
                        {position.job_category && (
                          <div className="flex items-center gap-1">
                            <Briefcase className="w-4 h-4" />
                            <span>{position.job_category}</span>
                          </div>
                        )}

                        {position.created_by_name && (
                          <div className="flex items-center gap-1">
                            <User className="w-4 h-4" />
                            <span>Requested by {position.created_by_name}</span>
                          </div>
                        )}

                        {(position.submitted_at || position.created_at) && (
                          <div className="flex items-center gap-1">
                            <Calendar className="w-4 h-4" />
                            <span>
                              Submitted {new Date(position.submitted_at || position.created_at!).toLocaleDateString()}
                            </span>
                          </div>
                        )}

                        {position.budget_max && (
                          <div className="flex items-center gap-1">
                            <Clock className="w-4 h-4" />
                            <span>
                              Budget: {position.salary_currency || '$'}
                              {position.budget_max.toLocaleString()}
                            </span>
                          </div>
                        )}
                      </div>

                      {position.rejection_reason && (
                        <Alert className="mt-3 bg-red-50 border-red-200">
                          <XCircle className="w-4 h-4 text-red-600" />
                          <AlertDescription className="text-red-800">
                            Previously rejected: {position.rejection_reason}
                          </AlertDescription>
                        </Alert>
                      )}
                    </div>

                    {/* Actions */}
                    <div className="flex items-center gap-2 ml-4">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => navigate(getPath(`positions/${position.id}`))}
                        disabled={isLoading}
                      >
                        <Eye className="w-4 h-4 mr-1" />
                        View
                      </Button>

                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => openRejectModal(position)}
                        disabled={isLoading}
                        className="border-red-200 text-red-700 hover:bg-red-50"
                      >
                        <XCircle className="w-4 h-4 mr-1" />
                        Reject
                      </Button>

                      <Button
                        size="sm"
                        onClick={() => handleApprove(position.id)}
                        disabled={isLoading}
                        className="bg-green-600 hover:bg-green-700"
                      >
                        {isLoading ? (
                          <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent mr-1" />
                        ) : (
                          <CheckCircle className="w-4 h-4 mr-1" />
                        )}
                        Approve
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      )}

      {/* Reject Modal */}
      <RejectPositionModal
        isOpen={showRejectModal}
        positionTitle={selectedPosition?.title || ''}
        onClose={() => {
          setShowRejectModal(false);
          setSelectedPosition(null);
        }}
        onConfirm={handleReject}
        isLoading={!!actionLoading}
      />
    </div>
  );
}
