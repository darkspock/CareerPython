/**
 * Resume Card Component
 *
 * Individual card component for displaying resume information
 * with actions for edit, delete, duplicate, and preview.
 */

import React, { useState } from 'react';
import {
  FileText,
  Calendar,
  MoreHorizontal,
  Edit2,
  Trash2,
  Copy,
  Eye,
  Download,
  Check,
  X
} from 'lucide-react';
import { motion } from 'framer-motion';
import type { Resume } from '../../types/resume';
import ResumeExportModal from './export/ResumeExportModal';

interface ResumeCardProps {
  resume: Resume;
  isSelected: boolean;
  onSelect: (isSelected: boolean) => void;
  onEdit: (newName: string) => void;
  onDelete: () => void;
  onDuplicate: (newName: string) => void;
  loading?: boolean;
}

const ResumeCard: React.FC<ResumeCardProps> = ({
  resume,
  isSelected,
  onSelect,
  onEdit,
  onDelete,
  onDuplicate,
  loading = false
}) => {
  const [showMenu, setShowMenu] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [editName, setEditName] = useState(resume.name);
  const [showDuplicateDialog, setShowDuplicateDialog] = useState(false);
  const [duplicateName, setDuplicateName] = useState(`${resume.name} - Copy`);
  const [showExportModal, setShowExportModal] = useState(false);

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const getResumeTypeColor = (type: string) => {
    switch (type) {
      case 'GENERAL':
        return 'bg-blue-100 text-blue-800';
      case 'POSITION':
        return 'bg-green-100 text-green-800';
      case 'ROLE':
        return 'bg-purple-100 text-purple-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getResumeTypeLabel = (type: string) => {
    switch (type) {
      case 'GENERAL':
        return 'General';
      case 'POSITION':
        return 'Position Specific';
      case 'ROLE':
        return 'Role Specific';
      default:
        return type;
    }
  };

  const handleEditSubmit = () => {
    if (editName.trim() && editName !== resume.name) {
      onEdit(editName.trim());
    }
    setIsEditing(false);
  };

  const handleEditCancel = () => {
    setEditName(resume.name);
    setIsEditing(false);
  };

  const handleDuplicate = () => {
    if (duplicateName.trim()) {
      onDuplicate(duplicateName.trim());
      setShowDuplicateDialog(false);
      setDuplicateName(`${resume.name} - Copy`);
    }
  };

  const handleEdit = () => {
    // Navigate to editor page
    window.location.href = `/candidate/profile/resumes/${resume.id}/edit`;
  };

  const handlePreview = () => {
    // Navigate to preview page
    window.open(`/candidate/profile/resumes/${resume.id}/preview`, '_blank');
  };

  const handleDownload = () => {
    // Open export modal
    setShowExportModal(true);
  };

  return (
    <>
      <motion.div
        className={`relative bg-white rounded-lg border-2 transition-all duration-200 hover:shadow-lg ${
          isSelected
            ? 'border-blue-500 shadow-md'
            : 'border-gray-200 hover:border-gray-300'
        } ${loading ? 'opacity-50' : ''}`}
        whileHover={{ y: -2 }}
      >
        {/* Selection Checkbox */}
        <div className="absolute top-3 left-3">
          <input
            type="checkbox"
            checked={isSelected}
            onChange={(e) => onSelect(e.target.checked)}
            className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
            disabled={loading}
          />
        </div>

        {/* More Options Menu */}
        <div className="absolute top-3 right-3">
          <div className="relative">
            <button
              onClick={() => setShowMenu(!showMenu)}
              className="p-1 rounded-full hover:bg-gray-100 transition-colors"
              disabled={loading}
            >
              <MoreHorizontal className="w-4 h-4 text-gray-500" />
            </button>

            {showMenu && (
              <div className="absolute right-0 top-full mt-1 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-1 z-10">
                <button
                  onClick={() => {
                    setIsEditing(true);
                    setShowMenu(false);
                  }}
                  className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 flex items-center"
                >
                  <Edit2 className="w-4 h-4 mr-2" />
                  Rename
                </button>
                <button
                  onClick={() => {
                    setShowDuplicateDialog(true);
                    setShowMenu(false);
                  }}
                  className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 flex items-center"
                >
                  <Copy className="w-4 h-4 mr-2" />
                  Duplicate
                </button>
                <button
                  onClick={() => {
                    handlePreview();
                    setShowMenu(false);
                  }}
                  className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 flex items-center"
                >
                  <Eye className="w-4 h-4 mr-2" />
                  Preview
                </button>
                <button
                  onClick={() => {
                    handleDownload();
                    setShowMenu(false);
                  }}
                  className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 flex items-center"
                >
                  <Download className="w-4 h-4 mr-2" />
                  Export
                </button>
                <hr className="my-1" />
                <button
                  onClick={() => {
                    onDelete();
                    setShowMenu(false);
                  }}
                  className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 flex items-center"
                >
                  <Trash2 className="w-4 h-4 mr-2" />
                  Delete
                </button>
              </div>
            )}
          </div>
        </div>

        <div className="p-6 pt-10">
          {/* Resume Icon and Type Badge */}
          <div className="flex items-start justify-between mb-4">
            <div className="flex items-center">
              <div className="p-2 bg-blue-100 rounded-lg">
                <FileText className="w-6 h-6 text-blue-600" />
              </div>
            </div>
            <span className={`px-2 py-1 text-xs font-medium rounded-full ${getResumeTypeColor(resume.resume_type)}`}>
              {getResumeTypeLabel(resume.resume_type)}
            </span>
          </div>

          {/* Resume Name */}
          {isEditing ? (
            <div className="mb-4">
              <input
                type="text"
                value={editName}
                onChange={(e) => setEditName(e.target.value)}
                className="w-full px-2 py-1 text-lg font-semibold border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                autoFocus
                onKeyDown={(e) => {
                  if (e.key === 'Enter') handleEditSubmit();
                  if (e.key === 'Escape') handleEditCancel();
                }}
              />
              <div className="flex gap-2 mt-2">
                <button
                  onClick={handleEditSubmit}
                  className="flex items-center px-2 py-1 text-sm bg-green-600 text-white rounded hover:bg-green-700"
                >
                  <Check className="w-3 h-3 mr-1" />
                  Save
                </button>
                <button
                  onClick={handleEditCancel}
                  className="flex items-center px-2 py-1 text-sm bg-gray-600 text-white rounded hover:bg-gray-700"
                >
                  <X className="w-3 h-3 mr-1" />
                  Cancel
                </button>
              </div>
            </div>
          ) : (
            <h3 className="text-lg font-semibold text-gray-900 mb-4 line-clamp-2">
              {resume.name}
            </h3>
          )}

          {/* Resume Details */}
          <div className="space-y-2 text-sm text-gray-600">
            <div className="flex items-center">
              <Calendar className="w-4 h-4 mr-2" />
              <span>Created: {formatDate(resume.created_at)}</span>
            </div>
            {resume.updated_at !== resume.created_at && (
              <div className="flex items-center">
                <Calendar className="w-4 h-4 mr-2" />
                <span>Updated: {formatDate(resume.updated_at)}</span>
              </div>
            )}
            {resume.last_generated_at && (
              <div className="flex items-center">
                <Download className="w-4 h-4 mr-2" />
                <span>Last exported: {formatDate(resume.last_generated_at)}</span>
              </div>
            )}
          </div>

          {/* Action Buttons */}
          <div className="flex gap-2 mt-6">
            <button
              onClick={handleEdit}
              className="flex-1 flex items-center justify-center px-3 py-2 text-sm font-medium text-green-600 border border-green-600 rounded-lg hover:bg-green-50 transition-colors"
              disabled={loading}
            >
              <Edit2 className="w-4 h-4 mr-1" />
              Edit
            </button>
            <button
              onClick={handlePreview}
              className="flex-1 flex items-center justify-center px-3 py-2 text-sm font-medium text-blue-600 border border-blue-600 rounded-lg hover:bg-blue-50 transition-colors"
              disabled={loading}
            >
              <Eye className="w-4 h-4 mr-1" />
              Preview
            </button>
            <button
              onClick={handleDownload}
              className="flex-1 flex items-center justify-center px-3 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors"
              disabled={loading}
            >
              <Download className="w-4 h-4 mr-1" />
              Export
            </button>
          </div>
        </div>

        {/* Loading Overlay */}
        {loading && (
          <div className="absolute inset-0 bg-white bg-opacity-50 flex items-center justify-center rounded-lg">
            <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
          </div>
        )}
      </motion.div>

      {/* Duplicate Dialog */}
      {showDuplicateDialog && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h3 className="text-lg font-semibold mb-4">Duplicate Resume</h3>
            <p className="text-gray-600 mb-4">
              Enter a name for the duplicated resume:
            </p>
            <input
              type="text"
              value={duplicateName}
              onChange={(e) => setDuplicateName(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent mb-4"
              placeholder="Resume name"
            />
            <div className="flex gap-3 justify-end">
              <button
                onClick={() => setShowDuplicateDialog(false)}
                className="px-4 py-2 text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                onClick={handleDuplicate}
                disabled={!duplicateName.trim()}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Duplicate
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Export Modal */}
      <ResumeExportModal
        isOpen={showExportModal}
        onClose={() => setShowExportModal(false)}
        resumeId={resume.id}
        resumeName={resume.name}
      />

      {/* Click outside to close menu */}
      {showMenu && (
        <div
          className="fixed inset-0 z-0"
          onClick={() => setShowMenu(false)}
        />
      )}
    </>
  );
};

export default ResumeCard;