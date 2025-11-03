import React, { useEffect, useState } from 'react';
import { api } from '../../lib/api';

interface Candidate {
  id: string | { value: string };
  name: string;
  email: string;
  phone?: string;
  city?: string;
  country?: string;
  status: string;
  job_category?: string;
  years_of_experience?: number;
  created_at: string;
  has_resume: boolean;
}

interface CandidateDetails {
  candidate: {
    id: { value: string };
    name: string;
    email: string;
    phone?: string;
    city?: string;
    country?: string;
    job_category?: string;
    date_of_birth?: string;
    created_at?: string;
  };
  user: {
    id?: string;
    email: string;
    is_active: boolean;
    created_at?: string;
    last_login?: string;
    has_password: boolean;
  };
}

interface CandidatesResponse {
  candidates: Candidate[];
  total_count: number;
  has_more: boolean;
}

const CandidatesManagement: React.FC = () => {
  const [candidates, setCandidates] = useState<Candidate[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalCount, setTotalCount] = useState(0);
  const pageSize = 10;

  // Password setting modal state
  const [showPasswordModal, setShowPasswordModal] = useState(false);
  const [selectedCandidate, setSelectedCandidate] = useState<CandidateDetails | null>(null);
  const [newPassword, setNewPassword] = useState('');
  const [passwordLoading, setPasswordLoading] = useState(false);

  // User details modal state
  const [showUserModal, setShowUserModal] = useState(false);

  useEffect(() => {
    fetchCandidates();
  }, [currentPage, statusFilter, searchTerm]);

  const fetchCandidates = async () => {
    try {
      setLoading(true);
      const params = new URLSearchParams({
        limit: pageSize.toString(),
        offset: ((currentPage - 1) * pageSize).toString(),
      });

      if (searchTerm) {
        params.append('search_term', searchTerm);
      }

      if (statusFilter) {
        params.append('status', statusFilter);
      }

      const response = await api.authenticatedRequest(`/admin/candidates?${params.toString()}`) as CandidatesResponse;
      setCandidates(response.candidates);
      setTotalCount(response.total_count);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch candidates');
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setCurrentPage(1);
    fetchCandidates();
  };

  const fetchCandidateDetails = async (candidateId: string) => {
    try {
      // setUserDetailsLoading(true);
      const response = await api.authenticatedRequest(`/admin/candidates/${candidateId}`) as CandidateDetails;
      setSelectedCandidate(response);
      setShowUserModal(true);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch candidate details');
    } finally {
      // setUserDetailsLoading(false);
    }
  };

  const handleSetPassword = async () => {
    if (!selectedCandidate || !newPassword) {
      setError('Candidate or password missing');
      return;
    }

    try {
      setPasswordLoading(true);
      const response = await api.authenticatedRequest(`/admin/candidates/${getCandidateId(selectedCandidate.candidate.id)}/set-password`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ password: newPassword }),
      });

      // Check if the response indicates an error (like duplicate email)
      if (response && typeof response === 'object' && 'success' in response && !(response as { success: boolean }).success) {
        const errorResponse = response as { error?: string; message?: string };
        // Handle specific error cases
        if (errorResponse.error === 'duplicate_email') {
          setError(`Email Conflict: ${errorResponse.message || 'Email already exists'}`);
        } else {
          setError(errorResponse.message || 'Failed to set password');
        }
        return;
      }

      setShowPasswordModal(false);
      setNewPassword('');
      setSelectedCandidate(null);
      setError(null);
      // Refresh candidate details
      await fetchCandidateDetails(getCandidateId(selectedCandidate.candidate.id));
    } catch (err: any) {
      setError(err.message || 'Failed to set password');
    } finally {
      setPasswordLoading(false);
    }
  };

  const handleToggleUserStatus = async (candidateId: string, isActive: boolean) => {
    try {
      await api.authenticatedRequest(`/admin/candidates/${candidateId}/toggle-status`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ is_active: isActive }),
      });

      // Refresh candidate details
      await fetchCandidateDetails(candidateId);
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to update user status');
    }
  };

  const getCandidateId = (id: string | { value: string }): string => {
    return typeof id === 'string' ? id : id.value;
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString();
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'active':
        return 'bg-green-100 text-green-800';
      case 'pending':
        return 'bg-yellow-100 text-yellow-800';
      case 'inactive':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const totalPages = Math.ceil(totalCount / pageSize);

  if (loading && candidates.length === 0) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Candidates Management</h2>
          <p className="text-gray-600">Manage candidate profiles and applications</p>
        </div>
        <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
          Add New Candidate
        </button>
      </div>

      {/* Search and Filters */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <form onSubmit={handleSearch} className="flex gap-4 items-end">
          <div className="flex-1">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Search Candidates
            </label>
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search by name, email, or phone..."
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Status Filter
            </label>
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Statuses</option>
              <option value="active">Active</option>
              <option value="pending">Pending</option>
              <option value="inactive">Inactive</option>
            </select>
          </div>
          <button
            type="submit"
            className="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 transition-colors"
          >
            Search
          </button>
        </form>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-md p-4">
          <div className="text-red-800">
            <strong>Error:</strong> {error}
          </div>
        </div>
      )}

      {/* Candidates Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {candidates.map((candidate) => (
          <div key={getCandidateId(candidate.id)} className="bg-white rounded-lg shadow-sm border p-6 hover:shadow-md transition-shadow">
            <div className="flex items-start justify-between mb-4">
              <div className="flex-1">
                <h3 className="text-lg font-semibold text-gray-900">{candidate.name}</h3>
                <p className="text-sm text-gray-600">{candidate.email}</p>
                {candidate.phone && (
                  <p className="text-sm text-gray-600">{candidate.phone}</p>
                )}
              </div>
              <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(candidate.status)}`}>
                {candidate.status}
              </span>
            </div>

            <div className="space-y-2 mb-4">
              {candidate.job_category && (
                <div className="flex items-center text-sm">
                  <span className="text-gray-500 w-20">Category:</span>
                  <span className="text-gray-900">{candidate.job_category}</span>
                </div>
              )}
              {candidate.city && candidate.country && (
                <div className="flex items-center text-sm">
                  <span className="text-gray-500 w-20">Location:</span>
                  <span className="text-gray-900">{candidate.city}, {candidate.country}</span>
                </div>
              )}
              {candidate.years_of_experience !== undefined && (
                <div className="flex items-center text-sm">
                  <span className="text-gray-500 w-20">Experience:</span>
                  <span className="text-gray-900">{candidate.years_of_experience} years</span>
                </div>
              )}
              <div className="flex items-center text-sm">
                <span className="text-gray-500 w-20">Resume:</span>
                <span className={`text-sm ${candidate.has_resume ? 'text-green-600' : 'text-red-600'}`}>
                  {candidate.has_resume ? '✓ Uploaded' : '✗ Missing'}
                </span>
              </div>
              <div className="flex items-center text-sm">
                <span className="text-gray-500 w-20">Joined:</span>
                <span className="text-gray-900">{formatDate(candidate.created_at)}</span>
              </div>
            </div>

            <div className="flex space-x-2 pt-4 border-t">
              <button
                onClick={() => fetchCandidateDetails(getCandidateId(candidate.id))}
                className="flex-1 text-blue-600 hover:text-blue-800 text-sm font-medium py-2 border border-blue-200 rounded-md hover:bg-blue-50 transition-colors"
              >
                Manage User
              </button>
              <button
                onClick={() => fetchCandidateDetails(getCandidateId(candidate.id))}
                className="flex-1 text-green-600 hover:text-green-800 text-sm font-medium py-2 border border-green-200 rounded-md hover:bg-green-50 transition-colors"
              >
                View Details
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="bg-white rounded-lg shadow-sm border p-4 flex items-center justify-between">
          <div className="text-sm text-gray-700">
            Showing {((currentPage - 1) * pageSize) + 1} to {Math.min(currentPage * pageSize, totalCount)} of {totalCount} candidates
          </div>
          <div className="flex space-x-2">
            <button
              onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
              disabled={currentPage === 1}
              className="px-3 py-1 border border-gray-300 rounded-md text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-100"
            >
              Previous
            </button>
            <span className="px-3 py-1 text-sm">
              Page {currentPage} of {totalPages}
            </span>
            <button
              onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
              disabled={currentPage === totalPages}
              className="px-3 py-1 border border-gray-300 rounded-md text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-100"
            >
              Next
            </button>
          </div>
        </div>
      )}

      {/* User Details Modal */}
      {showUserModal && selectedCandidate && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-semibold">User Management</h3>
              <button
                onClick={() => setShowUserModal(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                ✕
              </button>
            </div>

            <div className="space-y-4">
              <div>
                <h4 className="font-medium text-gray-900">Candidate Information</h4>
                <p className="text-sm text-gray-600">Name: {selectedCandidate.candidate.name}</p>
                <p className="text-sm text-gray-600">Email: {selectedCandidate.candidate.email}</p>
              </div>

              <div>
                <h4 className="font-medium text-gray-900">User Account Status</h4>
                <div className="flex items-center justify-between mt-2">
                  <span className="text-sm text-gray-600">Account Active:</span>
                  <button
                    onClick={() => handleToggleUserStatus(
                      getCandidateId(selectedCandidate.candidate.id),
                      !selectedCandidate.user.is_active
                    )}
                    className={`px-3 py-1 rounded-full text-xs font-medium ${
                      selectedCandidate.user.is_active
                        ? 'bg-green-100 text-green-800'
                        : 'bg-red-100 text-red-800'
                    }`}
                  >
                    {selectedCandidate.user.is_active ? 'Active' : 'Inactive'}
                  </button>
                </div>
              </div>

              <div>
                <h4 className="font-medium text-gray-900">Password Status</h4>
                <div className="flex items-center justify-between mt-2">
                  <span className="text-sm text-gray-600">Has Password:</span>
                  <span className={`text-xs font-medium ${
                    selectedCandidate.user.has_password ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {selectedCandidate.user.has_password ? '✓ Set' : '✗ Not Set'}
                  </span>
                </div>
                <button
                  onClick={() => {
                    setShowUserModal(false);
                    setShowPasswordModal(true);
                  }}
                  className="w-full mt-2 bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors"
                >
                  {selectedCandidate.user.has_password ? 'Change Password' : 'Set Password'}
                </button>
              </div>
            </div>

            <div className="flex justify-end mt-6">
              <button
                onClick={() => setShowUserModal(false)}
                className="px-4 py-2 text-gray-600 hover:text-gray-800"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Password Setting Modal */}
      {showPasswordModal && selectedCandidate && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-semibold">Set Password</h3>
              <button
                onClick={() => {
                  setShowPasswordModal(false);
                  setNewPassword('');
                }}
                className="text-gray-400 hover:text-gray-600"
              >
                ✕
              </button>
            </div>

            <div className="space-y-4">
              <div>
                <p className="text-sm text-gray-600 mb-4">
                  Setting password for: <strong>{selectedCandidate.candidate.email}</strong>
                </p>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  New Password
                </label>
                <input
                  type="password"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  placeholder="Enter new password (min 8 characters)"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  minLength={8}
                />
              </div>
            </div>

            <div className="flex justify-end space-x-3 mt-6">
              <button
                onClick={() => {
                  setShowPasswordModal(false);
                  setNewPassword('');
                }}
                className="px-4 py-2 text-gray-600 hover:text-gray-800"
                disabled={passwordLoading}
              >
                Cancel
              </button>
              <button
                onClick={handleSetPassword}
                disabled={passwordLoading || newPassword.length < 8}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {passwordLoading ? 'Setting...' : 'Set Password'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CandidatesManagement;