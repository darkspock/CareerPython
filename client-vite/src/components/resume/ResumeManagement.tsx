/**
 * Resume Management Component
 *
 * Main component for managing resumes with CRUD operations,
 * statistics display, and comprehensive user interface.
 *
 * Requirements: 1.1, 6.1, 6.2, 6.3
 */

import React, { useState, useEffect } from 'react';
import { Plus, Search, Filter, FileText } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useResumes } from '../../hooks/useResumes';
import ResumeCard from './ResumeCard';
import CreateResumeModal from './CreateResumeModal';
import ResumeStatsCard from './ResumeStatsCard';
import BulkActionsBar from './BulkActionsBar';
import LoadingSpinner from '../common/LoadingSpinner';
import ErrorAlert from '../common/ErrorAlert';

interface ResumeManagementProps {
  className?: string;
}

const ResumeManagement: React.FC<ResumeManagementProps> = ({ className = '' }) => {
  const {
    resumes,
    statistics,
    loading,
    error,
    fetchStatistics,
    createResume,
    updateResumeName,
    deleteResume,
    duplicateResume,
    bulkDeleteResumes,
    clearError,
    refreshResumes
  } = useResumes();

  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState<string>('all');
  const [selectedResumes, setSelectedResumes] = useState<string[]>([]);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const showStats = true;

  // Filter resumes based on search term and type
  const filteredResumes = resumes.filter(resume => {
    const matchesSearch = resume.name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesType = filterType === 'all' || resume.resume_type === filterType;
    return matchesSearch && matchesType;
  });

  // Load statistics on mount
  useEffect(() => {
    fetchStatistics();
  }, [fetchStatistics]);

  const handleSelectResume = (resumeId: string, isSelected: boolean) => {
    setSelectedResumes(prev =>
      isSelected
        ? [...prev, resumeId]
        : prev.filter(id => id !== resumeId)
    );
  };

  const handleSelectAll = (isSelected: boolean) => {
    setSelectedResumes(isSelected ? filteredResumes.map(r => r.id) : []);
  };

  const handleBulkDelete = async () => {
    if (selectedResumes.length > 0) {
      await bulkDeleteResumes(selectedResumes);
      setSelectedResumes([]);
    }
  };

  const handleCreateResume = async (data: {
    name: string;
    candidate_id: string;
    include_ai_enhancement: boolean;
  }) => {
    const resume = await createResume(data);
    if (resume) {
      setShowCreateModal(false);
      // Refresh statistics after creating a resume
      fetchStatistics();
    }
  };

  const handleDuplicateResume = async (resumeId: string, newName: string) => {
    const duplicated = await duplicateResume(resumeId, newName);
    if (duplicated) {
      fetchStatistics();
    }
  };

  const handleDeleteResume = async (resumeId: string) => {
    await deleteResume(resumeId);
    setSelectedResumes(prev => prev.filter(id => id !== resumeId));
    fetchStatistics();
  };

  const handleUpdateResumeName = async (resumeId: string, newName: string) => {
    await updateResumeName(resumeId, { name: newName });
  };

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Resume Management</h1>
          <p className="text-gray-600">Create, manage, and export your professional resumes</p>
        </div>
        <button
          onClick={() => setShowCreateModal(true)}
          className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          <Plus className="w-4 h-4 mr-2" />
          Create Resume
        </button>
      </div>

      {/* Error Alert */}
      {error.hasError && (
        <div className="space-y-4">
          <ErrorAlert
            message={error.message || 'An error occurred'}
            onDismiss={clearError}
            details={error.details}
          />
          {/* Show login button for authentication errors */}
          {error.code === 'NOT_AUTHENTICATED' && (
            <div className="text-center">
              <button
                onClick={() => window.location.href = '/candidate/login'}
                className="inline-flex items-center px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
              >
                Go to Login
              </button>
              <p className="text-sm text-gray-500 mt-2">
                Don't have an account? <a href="/auth/register" className="text-blue-600 hover:text-blue-700">Sign up here</a>
              </p>
            </div>
          )}
        </div>
      )}

      {/* Statistics Cards */}
      {showStats && statistics && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4"
        >
          <ResumeStatsCard
            title="Total Resumes"
            value={statistics.total_resumes}
            icon={<FileText className="w-5 h-5" />}
            trend={statistics.total_resumes > 0 ? '+12%' : undefined}
            color="blue"
          />
          <ResumeStatsCard
            title="General Resumes"
            value={statistics.resume_types.GENERAL || 0}
            icon={<FileText className="w-5 h-5" />}
            color="green"
          />
          <ResumeStatsCard
            title="Position Specific"
            value={statistics.resume_types.POSITION || 0}
            icon={<FileText className="w-5 h-5" />}
            color="purple"
          />
          <ResumeStatsCard
            title="Role Specific"
            value={statistics.resume_types.ROLE || 0}
            icon={<FileText className="w-5 h-5" />}
            color="orange"
          />
        </motion.div>
      )}

      {/* Search and Filter Bar */}
      <div className="flex flex-col sm:flex-row gap-4 items-stretch sm:items-center">
        <div className="relative flex-1">
          <Search className="w-4 h-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
          <input
            type="text"
            placeholder="Search resumes by name..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        <div className="relative">
          <Filter className="w-4 h-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
          <select
            value={filterType}
            onChange={(e) => setFilterType(e.target.value)}
            className="pl-10 pr-8 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent appearance-none bg-white"
          >
            <option value="all">All Types</option>
            <option value="GENERAL">General</option>
            <option value="POSITION">Position Specific</option>
            <option value="ROLE">Role Specific</option>
          </select>
        </div>
        <button
          onClick={refreshResumes}
          disabled={loading.isLoading}
          className="px-4 py-2 text-blue-600 border border-blue-600 rounded-lg hover:bg-blue-50 transition-colors disabled:opacity-50"
        >
          {loading.isLoading ? 'Refreshing...' : 'Refresh'}
        </button>
      </div>

      {/* Bulk Actions Bar */}
      {selectedResumes.length > 0 && (
        <BulkActionsBar
          selectedCount={selectedResumes.length}
          onDelete={handleBulkDelete}
          onSelectAll={() => handleSelectAll(true)}
          onClearSelection={() => setSelectedResumes([])}
          loading={loading.isLoading && loading.operation === 'bulk_delete_resumes'}
        />
      )}

      {/* Resume Grid */}
      <div className="space-y-4">
        {loading.isLoading && loading.operation === 'fetch_resumes' ? (
          <div className="flex justify-center py-12">
            <LoadingSpinner size="lg" />
          </div>
        ) : filteredResumes.length === 0 ? (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center py-12"
          >
            <FileText className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              {searchTerm || filterType !== 'all' ? 'No matching resumes found' : 'No resumes yet'}
            </h3>
            <p className="text-gray-600 mb-6">
              {searchTerm || filterType !== 'all'
                ? 'Try adjusting your search criteria or filters'
                : 'Create your first resume to get started with your professional profile'
              }
            </p>
            {(!searchTerm && filterType === 'all') && (
              <button
                onClick={() => setShowCreateModal(true)}
                className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                <Plus className="w-4 h-4 mr-2" />
                Create Your First Resume
              </button>
            )}
          </motion.div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <AnimatePresence>
              {filteredResumes.map((resume) => (
                <motion.div
                  key={resume.id}
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.9 }}
                  transition={{ duration: 0.2 }}
                >
                  <ResumeCard
                    resume={resume}
                    isSelected={selectedResumes.includes(resume.id)}
                    onSelect={(isSelected) => handleSelectResume(resume.id, isSelected)}
                    onEdit={(newName) => handleUpdateResumeName(resume.id, newName)}
                    onDelete={() => handleDeleteResume(resume.id)}
                    onDuplicate={(newName) => handleDuplicateResume(resume.id, newName)}
                    loading={loading.isLoading && (
                      loading.operation === 'delete_resume' ||
                      loading.operation === 'duplicate_resume' ||
                      loading.operation === 'update_resume_name'
                    )}
                  />
                </motion.div>
              ))}
            </AnimatePresence>
          </div>
        )}
      </div>

      {/* Create Resume Modal */}
      <CreateResumeModal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        onSubmit={handleCreateResume}
        loading={loading.isLoading && loading.operation === 'create_resume'}
      />
    </div>
  );
};

export default ResumeManagement;