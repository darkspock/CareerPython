/**
 * LockedFieldIndicator Component
 * Shows a lock icon with tooltip explaining why a field is locked
 */
import React from 'react';
import { Lock } from 'lucide-react';
import {
  JobPositionStatus,
  getJobPositionStatusLabel
} from '../../../types/position';

export interface LockedFieldIndicatorProps {
  status: JobPositionStatus | string;
  fieldName: string;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

const getLockedMessage = (status: JobPositionStatus | string, fieldName: string): string => {
  const statusLabel = getJobPositionStatusLabel(status);

  const messages: Record<string, Record<string, string>> = {
    budget_max: {
      [JobPositionStatus.APPROVED]: 'Budget is locked after approval',
      [JobPositionStatus.PUBLISHED]: 'Budget cannot be changed while published',
      [JobPositionStatus.ON_HOLD]: 'Budget cannot be changed while on hold',
      [JobPositionStatus.CLOSED]: 'Budget cannot be changed after closing',
      [JobPositionStatus.ARCHIVED]: 'Position is archived - all fields locked'
    },
    custom_fields_config: {
      [JobPositionStatus.PUBLISHED]: 'Custom fields are frozen after publishing',
      [JobPositionStatus.ON_HOLD]: 'Custom fields are frozen',
      [JobPositionStatus.CLOSED]: 'Custom fields cannot be changed after closing',
      [JobPositionStatus.ARCHIVED]: 'Position is archived - all fields locked'
    },
    salary_min: {
      [JobPositionStatus.CLOSED]: 'Salary cannot be changed after closing',
      [JobPositionStatus.ARCHIVED]: 'Position is archived - all fields locked'
    },
    salary_max: {
      [JobPositionStatus.CLOSED]: 'Salary cannot be changed after closing',
      [JobPositionStatus.ARCHIVED]: 'Position is archived - all fields locked'
    }
  };

  const fieldMessages = messages[fieldName];
  if (fieldMessages && fieldMessages[status]) {
    return fieldMessages[status];
  }

  if (status === JobPositionStatus.ARCHIVED) {
    return 'Position is archived - all fields are locked';
  }

  return `This field is locked in ${statusLabel} status`;
};

export const LockedFieldIndicator: React.FC<LockedFieldIndicatorProps> = ({
  status,
  fieldName,
  size: _size,
  className = ''
}) => {
  const message = getLockedMessage(status, fieldName);

  return (
    <div className={`group relative inline-flex items-center ${className}`}>
      <Lock size={14} className="text-gray-400" />
      <div className="absolute left-full ml-2 hidden group-hover:block z-10">
        <div className="bg-gray-900 text-white text-xs rounded py-1 px-2 whitespace-nowrap">
          {message}
          <div className="absolute top-1/2 -left-1 transform -translate-y-1/2">
            <div className="border-4 border-transparent border-r-gray-900" />
          </div>
        </div>
      </div>
    </div>
  );
};

export default LockedFieldIndicator;
