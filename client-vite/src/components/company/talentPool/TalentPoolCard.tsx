/**
 * Talent Pool Card Component
 * Phase 8: Card component for displaying talent pool entries
 */

import React from 'react';
import type { TalentPoolEntry } from '@/types/talentPool';
import {
  getTalentPoolStatusLabel,
  getTalentPoolStatusColor,
  getRatingStars,
  getRatingColor,
  formatDate,
  formatRelativeTime
} from '@/types/talentPool';

interface TalentPoolCardProps {
  entry: TalentPoolEntry;
  candidateName?: string;
  candidateEmail?: string;
  candidatePhotoUrl?: string;
  onView?: (entry: TalentPoolEntry) => void;
  onEdit?: (entry: TalentPoolEntry) => void;
  onChangeStatus?: (entry: TalentPoolEntry) => void;
  onRemove?: (entry: TalentPoolEntry) => void;
  isLoading?: boolean;
  showActions?: boolean;
}

export const TalentPoolCard: React.FC<TalentPoolCardProps> = ({
  entry,
  candidateName = 'Unknown Candidate',
  candidateEmail = '',
  candidatePhotoUrl,
  onView,
  onEdit,
  onChangeStatus,
  onRemove,
  isLoading = false,
  showActions = true
}) => {
  const handleView = () => {
    if (!isLoading && onView) {
      onView(entry);
    }
  };

  const handleEdit = () => {
    if (!isLoading && onEdit) {
      onEdit(entry);
    }
  };

  const handleChangeStatus = () => {
    if (!isLoading && onChangeStatus) {
      onChangeStatus(entry);
    }
  };

  const handleRemove = () => {
    if (!isLoading && onRemove && confirm(`Remove ${candidateName} from talent pool?`)) {
      onRemove(entry);
    }
  };

  return (
    <div className="bg-white rounded-lg border border-gray-200 shadow-sm hover:shadow-md transition-shadow p-4">
      {/* Header with candidate info and status */}
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-3 flex-1">
          {/* Candidate photo */}
          <div className="w-12 h-12 rounded-full bg-gray-200 flex items-center justify-center overflow-hidden flex-shrink-0">
            {candidatePhotoUrl ? (
              <img
                src={candidatePhotoUrl}
                alt={candidateName}
                className="w-full h-full object-cover"
              />
            ) : (
              <span className="text-gray-500 text-lg font-semibold">
                {candidateName.charAt(0).toUpperCase()}
              </span>
            )}
          </div>

          {/* Candidate name and email */}
          <div className="flex-1 min-w-0">
            <h3 className="text-lg font-semibold text-gray-900 truncate">
              {candidateName}
            </h3>
            {candidateEmail && (
              <p className="text-sm text-gray-600 truncate">{candidateEmail}</p>
            )}
          </div>
        </div>

        {/* Status badge */}
        <span
          className={`px-2 py-1 text-xs font-medium rounded border ${getTalentPoolStatusColor(
            entry.status
          )}`}
        >
          {getTalentPoolStatusLabel(entry.status)}
        </span>
      </div>

      {/* Rating */}
      {entry.rating && (
        <div className="mb-3">
          <span className={`text-lg ${getRatingColor(entry.rating)}`}>
            {getRatingStars(entry.rating)}
          </span>
          <span className="ml-2 text-sm text-gray-600">
            ({entry.rating}/5)
          </span>
        </div>
      )}

      {/* Added reason */}
      {entry.added_reason && (
        <div className="mb-3">
          <p className="text-sm font-medium text-gray-700 mb-1">Added Reason:</p>
          <p className="text-sm text-gray-600 line-clamp-2">{entry.added_reason}</p>
        </div>
      )}

      {/* Tags */}
      {entry.tags && entry.tags.length > 0 && (
        <div className="mb-3">
          <p className="text-sm font-medium text-gray-700 mb-1">Tags:</p>
          <div className="flex flex-wrap gap-1">
            {entry.tags.slice(0, 5).map((tag, index) => (
              <span
                key={index}
                className="px-2 py-0.5 text-xs bg-blue-100 text-blue-800 border border-blue-200 rounded"
              >
                {tag}
              </span>
            ))}
            {entry.tags.length > 5 && (
              <span className="text-xs text-gray-500 self-center">
                +{entry.tags.length - 5} more
              </span>
            )}
          </div>
        </div>
      )}

      {/* Notes preview */}
      {entry.notes && (
        <div className="mb-3">
          <p className="text-sm font-medium text-gray-700 mb-1">Notes:</p>
          <p className="text-sm text-gray-600 line-clamp-2">{entry.notes}</p>
        </div>
      )}

      {/* Source information */}
      {(entry.source_position_id || entry.source_application_id) && (
        <div className="mb-3">
          <p className="text-xs text-gray-500">
            {entry.source_position_id && (
              <span>From position: {entry.source_position_id}</span>
            )}
            {entry.source_application_id && (
              <span className="ml-2">Application: {entry.source_application_id}</span>
            )}
          </p>
        </div>
      )}

      {/* Timestamps */}
      <div className="text-xs text-gray-500 mb-3">
        <p>Added: {formatDate(entry.created_at)} ({formatRelativeTime(entry.created_at)})</p>
        {entry.updated_at !== entry.created_at && (
          <p>Updated: {formatDate(entry.updated_at)} ({formatRelativeTime(entry.updated_at)})</p>
        )}
      </div>

      {/* Actions */}
      {showActions && (
        <div className="flex items-center gap-2 pt-3 border-t border-gray-200">
          {onView && (
            <button
              onClick={handleView}
              disabled={isLoading}
              className="flex-1 px-3 py-2 text-sm font-medium text-white bg-blue-600 rounded hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              View Details
            </button>
          )}

          {onEdit && (
            <button
              onClick={handleEdit}
              disabled={isLoading}
              className="flex-1 px-3 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Edit
            </button>
          )}

          {onChangeStatus && (
            <button
              onClick={handleChangeStatus}
              disabled={isLoading}
              className="flex-1 px-3 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Change Status
            </button>
          )}

          {onRemove && (
            <button
              onClick={handleRemove}
              disabled={isLoading}
              className="px-3 py-2 text-sm font-medium text-red-700 bg-white border border-red-300 rounded hover:bg-red-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Remove
            </button>
          )}
        </div>
      )}
    </div>
  );
};
