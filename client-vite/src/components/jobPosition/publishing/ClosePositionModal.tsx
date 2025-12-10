/**
 * ClosePositionModal Component
 * Modal for closing a job position with reason selection
 */
import React, { useState } from 'react';
import { X, AlertTriangle } from 'lucide-react';
import { ClosedReason, getClosedReasonLabel } from '../../../types/position';

interface ClosePositionModalProps {
  isOpen: boolean;
  positionTitle: string;
  onClose: () => void;
  onConfirm: (reason: ClosedReason, note?: string) => void;
  isLoading?: boolean;
}

export const ClosePositionModal: React.FC<ClosePositionModalProps> = ({
  isOpen,
  positionTitle,
  onClose,
  onConfirm,
  isLoading = false
}) => {
  const [reason, setReason] = useState<ClosedReason | ''>('');
  const [note, setNote] = useState('');
  const [error, setError] = useState('');

  if (!isOpen) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!reason) {
      setError('Please select a reason for closing');
      return;
    }

    if (reason === ClosedReason.OTHER && !note.trim()) {
      setError('Please provide details for "Other" reason');
      return;
    }

    onConfirm(reason, note.trim() || undefined);
  };

  const handleClose = () => {
    setReason('');
    setNote('');
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
              <AlertTriangle className="text-orange-500" size={20} />
              <h3 className="text-lg font-semibold text-gray-900">Close Position</h3>
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
              You are about to close the position: <strong>{positionTitle}</strong>
            </p>

            {error && (
              <div className="p-3 bg-red-50 border border-red-200 rounded-md">
                <p className="text-sm text-red-600">{error}</p>
              </div>
            )}

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Reason for closing <span className="text-red-500">*</span>
              </label>
              <select
                value={reason}
                onChange={(e) => setReason(e.target.value as ClosedReason)}
                className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                required
              >
                <option value="">Select a reason</option>
                {Object.values(ClosedReason).map((r) => (
                  <option key={r} value={r}>
                    {getClosedReasonLabel(r)}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Additional notes
                {reason === ClosedReason.OTHER && <span className="text-red-500"> *</span>}
              </label>
              <textarea
                value={note}
                onChange={(e) => setNote(e.target.value)}
                rows={3}
                className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                placeholder="Add any additional details..."
                required={reason === ClosedReason.OTHER}
              />
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
                className="px-4 py-2 text-sm font-medium text-white bg-orange-600 rounded-md hover:bg-orange-700 disabled:opacity-50"
                disabled={isLoading}
              >
                {isLoading ? 'Closing...' : 'Close Position'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ClosePositionModal;
