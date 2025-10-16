/**
 * Bulk Actions Bar Component
 *
 * Toolbar for performing bulk operations on selected resumes
 * with confirmation dialogs and loading states.
 */

import React, { useState } from 'react';
import { Trash2, CheckSquare, X } from 'lucide-react';
import { motion } from 'framer-motion';

interface BulkActionsBarProps {
  selectedCount: number;
  onDelete: () => void;
  onSelectAll: () => void;
  onClearSelection: () => void;
  loading?: boolean;
}

const BulkActionsBar: React.FC<BulkActionsBarProps> = ({
  selectedCount,
  onDelete,
  onSelectAll,
  onClearSelection,
  loading = false
}) => {
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  const handleDelete = () => {
    setShowDeleteConfirm(true);
  };

  const confirmDelete = () => {
    onDelete();
    setShowDeleteConfirm(false);
  };

  return (
    <>
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-blue-50 border border-blue-200 rounded-lg p-4"
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <CheckSquare className="w-5 h-5 text-blue-600" />
              <span className="text-sm font-medium text-blue-900">
                {selectedCount} resume{selectedCount !== 1 ? 's' : ''} selected
              </span>
            </div>

            <div className="flex items-center space-x-2">
              <button
                onClick={onSelectAll}
                className="text-sm text-blue-600 hover:text-blue-800 font-medium"
                disabled={loading}
              >
                Select All
              </button>
              <span className="text-gray-300">|</span>
              <button
                onClick={onClearSelection}
                className="text-sm text-blue-600 hover:text-blue-800 font-medium"
                disabled={loading}
              >
                Clear Selection
              </button>
            </div>
          </div>

          <div className="flex items-center space-x-2">
            <button
              onClick={handleDelete}
              disabled={loading || selectedCount === 0}
              className="inline-flex items-center px-3 py-2 text-sm font-medium text-red-600 bg-red-50 border border-red-200 rounded-lg hover:bg-red-100 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {loading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-red-600 mr-2"></div>
                  Deleting...
                </>
              ) : (
                <>
                  <Trash2 className="w-4 h-4 mr-2" />
                  Delete Selected
                </>
              )}
            </button>

            <button
              onClick={onClearSelection}
              className="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100 transition-colors"
              disabled={loading}
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>
      </motion.div>

      {/* Delete Confirmation Modal */}
      {showDeleteConfirm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-white rounded-lg shadow-xl w-full max-w-md"
          >
            <div className="p-6">
              <div className="flex items-center mb-4">
                <div className="p-2 bg-red-100 rounded-full mr-3">
                  <Trash2 className="w-5 h-5 text-red-600" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900">
                  Delete Selected Resumes
                </h3>
              </div>

              <p className="text-gray-600 mb-6">
                Are you sure you want to delete {selectedCount} resume{selectedCount !== 1 ? 's' : ''}?
                This action cannot be undone.
              </p>

              <div className="flex gap-3 justify-end">
                <button
                  onClick={() => setShowDeleteConfirm(false)}
                  className="px-4 py-2 text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
                  disabled={loading}
                >
                  Cancel
                </button>
                <button
                  onClick={confirmDelete}
                  disabled={loading}
                  className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  {loading ? 'Deleting...' : 'Delete'}
                </button>
              </div>
            </div>
          </motion.div>
        </div>
      )}
    </>
  );
};

export default BulkActionsBar;