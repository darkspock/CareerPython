/**
 * Talent Pool Card Component
 * Phase 8: Card component for displaying talent pool entries
 */

import React from 'react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import type { TalentPoolEntry } from '../../../types/talentPool';
import {
  getTalentPoolStatusLabel,
  getTalentPoolStatusColor,
  getRatingStars,
  getRatingColor,
  formatDate,
  formatRelativeTime
} from '../../../types/talentPool';

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
    <Card className="hover:shadow-md transition-shadow">
      <CardHeader>
        {/* Header with candidate info and status */}
        <div className="flex items-start justify-between">
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
              <CardTitle className="text-lg truncate">
                {candidateName}
              </CardTitle>
              {candidateEmail && (
                <p className="text-sm text-gray-600 truncate">{candidateEmail}</p>
              )}
            </div>
          </div>

          {/* Status badge */}
          <Badge variant="outline" className={getTalentPoolStatusColor(entry.status)}>
            {getTalentPoolStatusLabel(entry.status)}
          </Badge>
        </div>
      </CardHeader>

      <CardContent className="space-y-3">
        {/* Rating */}
        {entry.rating && (
          <div>
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
          <div>
            <p className="text-sm font-medium text-gray-700 mb-1">Added Reason:</p>
            <p className="text-sm text-gray-600 line-clamp-2">{entry.added_reason}</p>
          </div>
        )}

        {/* Tags */}
        {entry.tags && entry.tags.length > 0 && (
          <div>
            <p className="text-sm font-medium text-gray-700 mb-1">Tags:</p>
            <div className="flex flex-wrap gap-1">
              {entry.tags.slice(0, 5).map((tag: string, index: number) => (
                <Badge key={index} variant="secondary">
                  {tag}
                </Badge>
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
          <div>
            <p className="text-sm font-medium text-gray-700 mb-1">Notes:</p>
            <p className="text-sm text-gray-600 line-clamp-2">{entry.notes}</p>
          </div>
        )}

        {/* Source information */}
        {(entry.source_position_id || entry.source_application_id) && (
          <div>
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
        <div className="text-xs text-gray-500">
          <p>Added: {formatDate(entry.created_at)} ({formatRelativeTime(entry.created_at)})</p>
          {entry.updated_at !== entry.created_at && (
            <p>Updated: {formatDate(entry.updated_at)} ({formatRelativeTime(entry.updated_at)})</p>
          )}
        </div>

        {/* Actions */}
        {showActions && (
          <div className="flex items-center gap-2 pt-3 border-t border-gray-200">
            {onView && (
              <Button
                onClick={handleView}
                disabled={isLoading}
                className="flex-1"
              >
                View Details
              </Button>
            )}

            {onEdit && (
              <Button
                onClick={handleEdit}
                disabled={isLoading}
                variant="secondary"
                className="flex-1"
              >
                Edit
              </Button>
            )}

            {onChangeStatus && (
              <Button
                onClick={handleChangeStatus}
                disabled={isLoading}
                variant="secondary"
                className="flex-1"
              >
                Change Status
              </Button>
            )}

            {onRemove && (
              <Button
                onClick={handleRemove}
                disabled={isLoading}
                variant="destructive"
              >
                Remove
              </Button>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  );
};
