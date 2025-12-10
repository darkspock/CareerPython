/**
 * EmploymentTypeBadge Component
 * Displays employment type with appropriate styling
 */
import React from 'react';
import { Briefcase } from 'lucide-react';
import {
  EmploymentType,
  getEmploymentTypeLabel
} from '../../../types/position';

interface EmploymentTypeBadgeProps {
  type: EmploymentType | string;
  showIcon?: boolean;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export const EmploymentTypeBadge: React.FC<EmploymentTypeBadgeProps> = ({
  type,
  showIcon = true,
  size = 'md',
  className = ''
}) => {
  const label = getEmploymentTypeLabel(type);

  const sizeClasses = {
    sm: 'px-2 py-0.5 text-xs',
    md: 'px-2.5 py-1 text-sm',
    lg: 'px-3 py-1.5 text-base'
  };

  const iconSizes = {
    sm: 12,
    md: 14,
    lg: 16
  };

  return (
    <span
      className={`inline-flex items-center gap-1 font-medium rounded-full bg-blue-50 text-blue-700 ${sizeClasses[size]} ${className}`}
    >
      {showIcon && <Briefcase size={iconSizes[size]} />}
      {label}
    </span>
  );
};

export default EmploymentTypeBadge;
