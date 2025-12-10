/**
 * RejectPositionModal Component
 * Modal for rejecting a job position with reason
 */
import React, { useState } from 'react';
import { X, XCircle } from 'lucide-react';

interface RejectPositionModalProps {
  isOpen: boolean;
  positionTitle: string;
  onClose: () => void;
  onConfirm: (reason: string) => void;
  isLoading?: boolean;
}

export const RejectPositionModal: React.FC<RejectPositionModalProps> = ({
  isOpen,
  positionTitle,
  onClose,
  onConfirm,
  isLoading = false
}) => {
  const [reason, setReason] = useState('');
  const [error, setError] = useState('');

  if (!isOpen) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!reason.trim()) {
      setError('Please provide a reason for rejection');
      return;
    }

    if (reason.trim().length < 10) {
      setError('Please provide a more detailed reason (at least 10 characters)');
      return;
    }

    onConfirm(reason.trim());
  };

  const handleClose = () => {
    setReason('');
    setError('');
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      <div className="flex min-h-screen items-center justify-center p-4">
        {/* Backdrop */}
        <div
          className="fixed inset-0 bg-black bg-opacity-30 transition-opacity"
          onClick={handleClose}
        />

        {/* Modal */}
        <div className="relative bg-white rounded-lg shadow-xl max-w-md w-full">
          {/* Header */}
          <div className="flex items-center justify-between p-4 border-b">
            <div className="flex items-center gap-2">
              <XCircle className="text-red-500" size={20} />
              <h3 className="text-lg font-semibold text-gray-900">Reject Position</h3>
            </div>
            <button
              onClick={handleClose}
              className="text-gray-400 hover:text-gray-500"
            >
              <X size={20} />
            </button>
          </div>

          {/* Body */}
          <form onSubmit={handleSubmit} className="p-4 space-y-4">
            <p className="text-sm text-gray-600">
              You are about to reject the position: <strong>{positionTitle}</strong>
            </p>

            <p className="text-sm text-gray-500">
              The position will be sent back to the creator for revision.
            </p>

            {error && (
              <div className="p-3 bg-red-50 border border-red-200 rounded-md">
                <p className="text-sm text-red-600">{error}</p>
              </div>
            )}

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Reason for rejection <span className="text-red-500">*</span>
              </label>
              <textarea
                value={reason}
                onChange={(e) => setReason(e.target.value)}
                rows={4}
                className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                placeholder="Please explain why this position is being rejected and what changes are needed..."
                required
              />
              <p className="mt-1 text-xs text-gray-500">
                This reason will be visible to the position creator.
              </p>
            </div>

            {/* Footer */}
            <div className="flex justify-end gap-3 pt-4 border-t">
              <button
                type="button"
                onClick={handleClose}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
                disabled={isLoading}
              >
                Cancel
              </button>
              <button
                type="submit"
                className="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-md hover:bg-red-700 disabled:opacity-50"
                disabled={isLoading}
              >
                {isLoading ? 'Rejecting...' : 'Reject Position'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default RejectPositionModal;
