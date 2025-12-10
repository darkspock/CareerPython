/**
 * StatusBadge Component
 * Displays the job position status with appropriate color coding
 */
import React from 'react';
import {
  JobPositionStatus,
  getJobPositionStatusLabel,
  getJobPositionStatusColor
} from '../../../types/position';

export interface StatusBadgeProps {
  status: JobPositionStatus | string;
  size?: 'sm' | 'md' | 'lg';
  showIcon?: boolean;
  className?: string;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({
  status,
  size = 'md',
  showIcon: _showIcon,
  className = ''
}) => {
  const label = getJobPositionStatusLabel(status);
  const colorClasses = getJobPositionStatusColor(status);

  const sizeClasses = {
    sm: 'px-2 py-0.5 text-xs',
    md: 'px-2.5 py-1 text-sm',
    lg: 'px-3 py-1.5 text-base'
  };

  return (
    <span
      className={`inline-flex items-center font-medium rounded-full ${colorClasses} ${sizeClasses[size]} ${className}`}
    >
      {label}
    </span>
  );
};

export default StatusBadge;
